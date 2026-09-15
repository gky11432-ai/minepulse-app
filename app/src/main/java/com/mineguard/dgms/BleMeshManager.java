package com.mineguard.dgms;

import android.bluetooth.BluetoothAdapter;
import android.bluetooth.le.AdvertiseCallback;
import android.bluetooth.le.AdvertiseData;
import android.bluetooth.le.AdvertiseSettings;
import android.bluetooth.le.BluetoothLeAdvertiser;
import android.bluetooth.le.BluetoothLeScanner;
import android.bluetooth.le.ScanCallback;
import android.bluetooth.le.ScanFilter;
import android.bluetooth.le.ScanResult;
import android.bluetooth.le.ScanSettings;
import android.content.Context;
import java.nio.charset.StandardCharsets;
import java.util.Collections;
import java.util.concurrent.ConcurrentHashMap;

public class BleMeshManager {
    public static final int MESH_COMPANY_ID = 0xFFFE;
    private final Context context;
    private final HardwareController hardwareController;
    private BluetoothAdapter bluetoothAdapter;
    private BluetoothLeAdvertiser advertiser;
    private BluetoothLeScanner scanner;
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
        try {
            this.bluetoothAdapter = BluetoothAdapter.getDefaultAdapter();
        } catch (Exception ignored) {}
    }

    public void setListener(MeshListener listener) {
        this.listener = listener;
    }

    public void startOfflineMesh(String myMinerId) {
        try {
            if (bluetoothAdapter == null || !bluetoothAdapter.isEnabled()) return;
            advertiser = bluetoothAdapter.getBluetoothLeAdvertiser();
            scanner = bluetoothAdapter.getBluetoothLeScanner();

            broadcastPacket(myMinerId, false);
            startScanning();
        } catch (SecurityException | Exception ignored) {}
    }

    public void triggerOfflineSos(String myMinerId) {
        broadcastPacket(myMinerId, true);
        hardwareController.startCollierySiren();
    }

    public void cancelOfflineSos(String myMinerId) {
        hardwareController.stopCollierySiren();
        broadcastPacket(myMinerId, false);
    }

    private void broadcastPacket(String minerId, boolean isSos) {
        try {
            if (advertiser == null) return;
            try { advertiser.stopAdvertising(advCallback); } catch (Exception ignored) {}

            AdvertiseSettings settings = new AdvertiseSettings.Builder()
                    .setAdvertiseMode(AdvertiseSettings.ADVERTISE_MODE_LOW_LATENCY)
                    .setTxPowerLevel(AdvertiseSettings.ADVERTISE_TX_POWER_HIGH)
                    .setConnectable(false)
                    .setTimeout(0)
                    .build();

            String cleanId = minerId.length() > 5 ? minerId.substring(0, 5) : minerId;
            String raw = (isSos ? "!" : "#") + cleanId;
            byte[] payload = raw.getBytes(StandardCharsets.UTF_8);

            AdvertiseData data = new AdvertiseData.Builder()
                    .addManufacturerData(MESH_COMPANY_ID, payload)
                    .setIncludeDeviceName(false)
                    .setIncludeTxPowerLevel(false)
                    .build();

            advertiser.startAdvertising(settings, data, advCallback);
        } catch (SecurityException | Exception ignored) {}
    }

    private void startScanning() {
        try {
            if (scanner == null) return;
            ScanFilter filter = new ScanFilter.Builder()
                    .setManufacturerData(MESH_COMPANY_ID, new byte[]{})
                    .build();

            ScanSettings settings = new ScanSettings.Builder()
                    .setScanMode(ScanSettings.SCAN_MODE_LOW_LATENCY)
                    .setReportDelay(0)
                    .build();

            scanner.startScan(Collections.singletonList(filter), settings, scanCallback);
        } catch (SecurityException | Exception ignored) {}
    }

    private final AdvertiseCallback advCallback = new AdvertiseCallback() {
        @Override
        public void onStartSuccess(AdvertiseSettings settingsInEffect) {}
    };

    private final ScanCallback scanCallback = new ScanCallback() {
        @Override
        public void onScanResult(int callbackType, ScanResult result) {
            try {
                if (result.getScanRecord() == null) return;
                byte[] data = result.getScanRecord().getManufacturerSpecificData(MESH_COMPANY_ID);
                if (data == null || data.length == 0) return;

                String msg = new String(data, StandardCharsets.UTF_8);
                boolean isEmergency = msg.startsWith("!");
                String peerId = msg.substring(1);
                int rssi = result.getRssi();

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
            } catch (Exception ignored) {}
        }
    };

    public ConcurrentHashMap<String, PeerMiner> getNearbyMiners() {
        return nearbyMiners;
    }

    public void stopMesh() {
        try {
            if (advertiser != null) advertiser.stopAdvertising(advCallback);
            if (scanner != null) scanner.stopScan(scanCallback);
        } catch (SecurityException | Exception ignored) {}
    }
}
