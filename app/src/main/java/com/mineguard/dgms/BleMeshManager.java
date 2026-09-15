package com.mineguard.dgms;

import android.bluetooth.BluetoothAdapter;
import android.bluetooth.le.AdvertiseCallback;
import android.bluetooth.le.AdvertiseData;
import android.bluetooth.le.AdvertiseSettings;
import android.bluetooth.le.BluetoothLeAdvertiser;
import android.bluetooth.le.BluetoothLeScanner;
import android.bluetooth.le.ScanCallback;
import android.bluetooth.le.ScanResult;
import android.bluetooth.le.ScanSettings;
import android.content.Context;
import java.nio.charset.StandardCharsets;
import java.util.concurrent.ConcurrentHashMap;

public class BleMeshManager {
    public static final int MESH_COMPANY_ID = 0xFFFE;
    private final Context context;
    private final HardwareController hardwareController;
    private BluetoothAdapter bluetoothAdapter;
    private BluetoothLeAdvertiser advertiser;
    private BluetoothLeScanner scanner;
    private final ConcurrentHashMap<String, PeerMiner> nearbyMiners = new ConcurrentHashMap<>();
    private String currentOfficerTag = "Miner";

    public static class PeerMiner {
        public String id;
        public String officerName;
        public String officerRole;
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
        try { this.bluetoothAdapter = BluetoothAdapter.getDefaultAdapter(); } catch (Exception ignored) {}
    }

    public void setListener(MeshListener listener) { this.listener = listener; }

    public void startOfflineMesh() {
        startOfflineMesh("Miner");
    }

    public void startOfflineMesh(String officerTag) {
        if (officerTag != null && !officerTag.isEmpty()) {
            this.currentOfficerTag = officerTag;
        }
        try {
            if (bluetoothAdapter == null || !bluetoothAdapter.isEnabled()) return;
            advertiser = bluetoothAdapter.getBluetoothLeAdvertiser();
            scanner = bluetoothAdapter.getBluetoothLeScanner();

            broadcastPacket(false);
            startScanning();
        } catch (Exception ignored) {}
    }

    public void triggerOfflineSos() {
        broadcastPacket(true);
        hardwareController.startCollierySiren();
    }

    public void triggerOfflineSos(String minerId) {
        triggerOfflineSos();
    }

    public void cancelOfflineSos() {
        hardwareController.stopCollierySiren();
        broadcastPacket(false);
    }

    public void cancelOfflineSos(String minerId) {
        cancelOfflineSos();
    }

    private void broadcastPacket(boolean isSos) {
        try {
            if (advertiser == null) return;
            try { advertiser.stopAdvertising(advCallback); } catch (Exception ignored) {}

            AdvertiseSettings settings = new AdvertiseSettings.Builder()
                    .setAdvertiseMode(AdvertiseSettings.ADVERTISE_MODE_LOW_LATENCY)
                    .setTxPowerLevel(AdvertiseSettings.ADVERTISE_TX_POWER_HIGH)
                    .setConnectable(false)
                    .setTimeout(0)
                    .build();

            String raw = (isSos ? "!" : "#") + currentOfficerTag;
            byte[] payload = raw.getBytes(StandardCharsets.UTF_8);

            AdvertiseData data = new AdvertiseData.Builder()
                    .addManufacturerData(MESH_COMPANY_ID, payload)
                    .setIncludeDeviceName(false)
                    .build();

            advertiser.startAdvertising(settings, data, advCallback);
        } catch (Exception ignored) {}
    }

    private void startScanning() {
        try {
            if (scanner == null) return;
            ScanSettings settings = new ScanSettings.Builder()
                    .setScanMode(ScanSettings.SCAN_MODE_LOW_LATENCY)
                    .setReportDelay(0)
                    .build();
            scanner.startScan(null, settings, scanCallback);
        } catch (Exception ignored) {}
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
                String info = msg.substring(1);

                String[] parts = info.split("~");
                String name = parts.length > 0 ? parts[0] : "Miner";
                String role = parts.length > 1 ? parts[1] : "Worker";
                int rssi = result.getRssi();

                double distance = Math.pow(10.0, (-59 - rssi) / 20.0);
                distance = Math.round(distance * 10.0) / 10.0;

                PeerMiner miner = new PeerMiner();
                miner.id = name;
                miner.officerName = name;
                miner.officerRole = role;
                miner.rssi = rssi;
                miner.distanceMeters = distance;
                miner.isEmergency = isEmergency;
                miner.lastSeen = System.currentTimeMillis();

                nearbyMiners.put(name, miner);

                if (listener != null) {
                    listener.onMinerUpdated(nearbyMiners);
                    if (isEmergency) {
                        hardwareController.startCollierySiren();
                        listener.onEmergencyReceived(name + " (" + role + ")", distance);
                    }
                }
            } catch (Exception ignored) {}
        }
    };

    public ConcurrentHashMap<String, PeerMiner> getNearbyMiners() { return nearbyMiners; }

    public void stopMesh() {
        try {
            if (advertiser != null) advertiser.stopAdvertising(advCallback);
            if (scanner != null) scanner.stopScan(scanCallback);
        } catch (Exception ignored) {}
    }
}
