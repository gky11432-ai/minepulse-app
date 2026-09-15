package com.mineguard.dgms;

import android.bluetooth.BluetoothAdapter;
import android.bluetooth.le.AdvertiseCallback;
import android.bluetooth.le.AdvertiseData;
import android.bluetooth.le.AdvertiseSettings;
import android.bluetooth.le.BluetoothLeAdvertiser;
import android.bluetooth.le.BluetoothLeScanner;
import android.bluetooth.le.ScanCallback;
import android.bluetooth.le.ScanResult;
import android.content.Context;
import android.os.ParcelUuid;
import java.nio.charset.StandardCharsets;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;

public class BleMeshManager {
    public static final UUID MESH_UUID = UUID.fromString("00001802-0000-1000-8000-00805f9b34fb");
    private final Context context;
    private final HardwareController hardwareController;
    private BluetoothAdapter bluetoothAdapter;
    private BluetoothLeAdvertiser advertiser;
    private BluetoothLeScanner scanner;
    private boolean isSosActive = false;
    private final ConcurrentHashMap<String, PeerMiner> nearbyMiners = new ConcurrentHashMap<>();

    public static class PeerMiner {
        public String id;
        public int rssi;
        public double distanceMeters;
        public boolean isEmergency;
        public long lastSeen;
    }

    public interface MeshListener {
        void onMinerUpdated(ConcurrentHashMap<String, PeerMiner> miners);
        void onEmergencyReceived(String minerId, double distance);
    }
    private MeshListener listener;

    public BleMeshManager(Context context, HardwareController hardwareController) {
        this.context = context;
        this.hardwareController = hardwareController;
        this.bluetoothAdapter = BluetoothAdapter.getDefaultAdapter();
    }

    public void setListener(MeshListener listener) {
        this.listener = listener;
    }

    public void startOfflineMesh(String myMinerId) {
        if (bluetoothAdapter == null || !bluetoothAdapter.isEnabled()) return;
        advertiser = bluetoothAdapter.getBluetoothLeAdvertiser();
        scanner = bluetoothAdapter.getBluetoothLeScanner();

        startAdvertising(myMinerId, false);
        startScanning();
    }

    public void triggerOfflineSos(String myMinerId) {
        isSosActive = true;
        startAdvertising(myMinerId, true);
        hardwareController.startCollierySiren();
    }

    public void cancelOfflineSos(String myMinerId) {
        isSosActive = false;
        hardwareController.stopCollierySiren();
        startAdvertising(myMinerId, false);
    }

    private void startAdvertising(String minerId, boolean sos) {
        if (advertiser == null) return;
        try {
            advertiser.stopAdvertising(advCallback);
        } catch (Exception ignored) {}

        AdvertiseSettings settings = new AdvertiseSettings.Builder()
                .setAdvertiseMode(AdvertiseSettings.ADVERTISE_MODE_LOW_LATENCY)
                .setTxPowerLevel(AdvertiseSettings.ADVERTISE_TX_POWER_HIGH)
                .setConnectable(false)
                .build();

        String payload = (sos ? "SOS:" : "OK:") + minerId;
        AdvertiseData data = new AdvertiseData.Builder()
                .addServiceUuid(new ParcelUuid(MESH_UUID))
                .addServiceData(new ParcelUuid(MESH_UUID), payload.getBytes(StandardCharsets.UTF_8))
                .setIncludeDeviceName(false)
                .build();

        advertiser.startAdvertising(settings, data, advCallback);
    }

    private void startScanning() {
        if (scanner == null) return;
        scanner.startScan(scanCallback);
    }

    private final AdvertiseCallback advCallback = new AdvertiseCallback() {
        @Override
        public void onStartSuccess(AdvertiseSettings settingsInEffect) {}
    };

    private final ScanCallback scanCallback = new ScanCallback() {
        @Override
        public void onScanResult(int callbackType, ScanResult result) {
            if (result.getScanRecord() == null) return;
            byte[] data = result.getScanRecord().getServiceData(new ParcelUuid(MESH_UUID));
            if (data == null) return;

            String msg = new String(data, StandardCharsets.UTF_8);
            boolean isEmergency = msg.startsWith("SOS:");
            String peerId = msg.substring(4);
            int rssi = result.getRssi();

            // RSSI to Meters Approximation Formula
            double distance = Math.pow(10.0, (-59 - rssi) / (20.0));
            distance = Math.round(distance * 10.0) / 10.0;

            PeerMiner miner = new PeerMiner();
            miner.id = peerId;
            miner.rssi = rssi;
            miner.distanceMeters = distance;
            miner.isEmergency = isEmergency;
            miner.lastSeen = System.currentTimeMillis();

            nearbyMiners.put(peerId, miner);

            if (listener != null) {
                listener.onMinerUpdated(nearbyMiners);
                if (isEmergency) {
                    hardwareController.startCollierySiren();
                    listener.onEmergencyReceived(peerId, distance);
                }
            }
        }
    };

    public ConcurrentHashMap<String, PeerMiner> getNearbyMiners() {
        return nearbyMiners;
    }

    public void stopMesh() {
        try {
            if (advertiser != null) advertiser.stopAdvertising(advCallback);
            if (scanner != null) scanner.stopScan(scanCallback);
        } catch (Exception ignored) {}
    }
}
