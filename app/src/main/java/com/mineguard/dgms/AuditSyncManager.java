package com.mineguard.dgms;

import android.content.Context;
import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.MqttCallback;
import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttConnectOptions;
import org.eclipse.paho.client.mqttv3.MqttMessage;
import org.eclipse.paho.client.mqttv3.persist.MemoryPersistence;

public class AuditSyncManager {
    private static final String BROKER_URL = "tcp://broker.emqx.io:1883";
    private static final String TOPIC_AUDIT = "mineguard/colliery/shared_audit_ledger";
    private final AlarmLogManager alarmLogManager;
    private MqttClient mqttClient;

    public interface SyncListener {
        void onRemoteAuditReceived(String officerName, String category, boolean isDanger);
    }
    private SyncListener listener;

    public AuditSyncManager(Context context, AlarmLogManager alarmLogManager) {
        this.alarmLogManager = alarmLogManager;
        initNetworkSync();
    }

    public void setListener(SyncListener listener) { this.listener = listener; }

    private void initNetworkSync() {
        new Thread(() -> {
            try {
                String clientId = "Miner_" + System.currentTimeMillis();
                mqttClient = new MqttClient(BROKER_URL, clientId, new MemoryPersistence());
                MqttConnectOptions options = new MqttConnectOptions();
                options.setAutomaticReconnect(true);
                options.setCleanSession(true);
                options.setConnectionTimeout(10);

                mqttClient.setCallback(new MqttCallback() {
                    @Override
                    public void connectionLost(Throwable cause) {}

                    @Override
                    public void messageArrived(String topic, MqttMessage message) {
                        handleIncomingPayload(new String(message.getPayload()));
                    }

                    @Override
                    public void deliveryComplete(IMqttDeliveryToken token) {}
                });

                mqttClient.connect(options);
                mqttClient.subscribe(TOPIC_AUDIT, 1);
            } catch (Throwable ignored) {}
        }).start();
    }

    public void broadcastAudit(AlarmLogManager.AuditEntry entry) {
        new Thread(() -> {
            try {
                if (mqttClient != null && mqttClient.isConnected()) {
                    String payload = entry.entryId + "~~~" + entry.timestamp + "~~~" + entry.officerName 
                            + "~~~" + entry.officerId + "~~~" + entry.role + "~~~" + entry.category 
                            + "~~~" + entry.remarks + "~~~" + entry.isDanger;
                    mqttClient.publish(TOPIC_AUDIT, new MqttMessage(payload.getBytes()));
                }
            } catch (Throwable ignored) {}
        }).start();
    }

    private void handleIncomingPayload(String raw) {
        try {
            String[] p = raw.split("~~~");
            if (p.length >= 7) {
                boolean isDanger = (p.length >= 8) && Boolean.parseBoolean(p[7]);
                boolean isNew = alarmLogManager.mergeRemoteEntry(p[0], p[1], p[2], p[3], p[4], p[5], p[6], isDanger);
                if (isNew && listener != null) {
                    listener.onRemoteAuditReceived(p[2], p[5], isDanger);
                }
            }
        } catch (Throwable ignored) {}
    }

    public void close() {
        try {
            if (mqttClient != null) { mqttClient.disconnect(); mqttClient.close(); }
        } catch (Throwable ignored) {}
    }
}
