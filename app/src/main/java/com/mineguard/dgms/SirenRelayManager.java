package com.mineguard.dgms;

import android.content.Context;
import android.os.Handler;
import android.os.Looper;
import android.os.PowerManager;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.Socket;
import java.nio.charset.StandardCharsets;

public class SirenRelayManager {
    private static final String BROKER_HOST = "broker.hivemq.com";
    private static final int BROKER_PORT = 1883;
    private static final String TOPIC = "mineguard/colliery/siren/live/v3";

    private final Context context;
    private final HardwareController hardwareController;
    private final Handler mainHandler;
    private PowerManager.WakeLock wakeLock;
    private Socket socket;
    private OutputStream outputStream;
    private boolean isRunning = true;
    private String lastAlertId = "";

    public interface SirenStateListener {
        void onSirenReceived(String officer, String time);
        void onConnectionStateChanged(boolean isConnected);
    }
    private SirenStateListener listener;

    public SirenRelayManager(Context context, HardwareController hardwareController) {
        this.context = context;
        this.hardwareController = hardwareController;
        this.mainHandler = new Handler(Looper.getMainLooper());

        PowerManager pm = (PowerManager) context.getSystemService(Context.POWER_SERVICE);
        if (pm != null) {
            wakeLock = pm.newWakeLock(PowerManager.PARTIAL_WAKE_LOCK | PowerManager.ACQUIRE_CAUSES_WAKEUP, "MineGuard:SirenWakeLock");
        }
        startNetworkListener();
    }

    public void setListener(SirenStateListener listener) {
        this.listener = listener;
    }

    private void startNetworkListener() {
        new Thread(() -> {
            while (isRunning) {
                try {
                    socket = new Socket(BROKER_HOST, BROKER_PORT);
                    outputStream = socket.getOutputStream();
                    InputStream in = socket.getInputStream();

                    sendMqttConnect();
                    sendMqttSubscribe();
                    notifyConnection(true);

                    byte[] buffer = new byte[2048];
                    int read;
                    while ((read = in.read(buffer)) != -1) {
                        if ((buffer[0] >> 4) == 3) {
                            parseIncomingMessage(buffer, read);
                        }
                    }
                } catch (Exception e) {
                    notifyConnection(false);
                    try { Thread.sleep(3500); } catch (InterruptedException ignored) {}
                }
            }
        }).start();
    }

    private void sendMqttConnect() throws Exception {
        String clientId = "MG_" + System.currentTimeMillis();
        byte[] clientBytes = clientId.getBytes(StandardCharsets.UTF_8);
        byte[] pkt = new byte[14 + clientBytes.length];
        pkt[0] = 0x10;
        pkt[1] = (byte) (12 + clientBytes.length);
        pkt[3] = 0x04; pkt[4] = 'M'; pkt[5] = 'Q'; pkt[6] = 'T'; pkt[7] = 'T';
        pkt[8] = 0x04; pkt[9] = 0x02; pkt[11] = 60;
        pkt[13] = (byte) clientBytes.length;
        System.arraycopy(clientBytes, 0, pkt, 14, clientBytes.length);
        outputStream.write(pkt);
        outputStream.flush();
    }

    private void sendMqttSubscribe() throws Exception {
        byte[] topBytes = TOPIC.getBytes(StandardCharsets.UTF_8);
        byte[] pkt = new byte[7 + topBytes.length];
        pkt[0] = (byte) 0x82;
        pkt[1] = (byte) (5 + topBytes.length);
        pkt[3] = 0x01; pkt[5] = (byte) topBytes.length;
        System.arraycopy(topBytes, 0, pkt, 6, topBytes.length);
        pkt[pkt.length - 1] = 0x00;
        outputStream.write(pkt);
        outputStream.flush();
    }

    public void triggerCollieryBroadcast() {
        new Thread(() -> {
            try {
                String payload = "SOS:" + System.currentTimeMillis() + ":Mining Sirdar";
                byte[] topBytes = TOPIC.getBytes(StandardCharsets.UTF_8);
                byte[] payBytes = payload.getBytes(StandardCharsets.UTF_8);
                byte[] pkt = new byte[4 + topBytes.length + payBytes.length];
                pkt[0] = 0x30;
                pkt[1] = (byte) (2 + topBytes.length + payBytes.length);
                pkt[3] = (byte) topBytes.length;
                System.arraycopy(topBytes, 0, pkt, 4, topBytes.length);
                System.arraycopy(payBytes, 0, pkt, 4 + topBytes.length, payBytes.length);

                if (outputStream != null) {
                    outputStream.write(pkt);
                    outputStream.flush();
                }
                handleAlert(payload);
            } catch (Exception ignored) {}
        }).start();
    }

    private void parseIncomingMessage(byte[] data, int len) {
        String msg = new String(data, 0, len, StandardCharsets.UTF_8);
        if (msg.contains("SOS:")) {
            int start = msg.indexOf("SOS:");
            String clean = msg.substring(start);
            handleAlert(clean);
        }
    }

    private void handleAlert(String raw) {
        String[] parts = raw.split(":");
        if (parts.length >= 2) {
            String alertId = parts[1];
            if (alertId.equals(lastAlertId)) return;
            lastAlertId = alertId;

            if (wakeLock != null && !wakeLock.isHeld()) {
                wakeLock.acquire(30000);
            }
            hardwareController.startCollierySiren();

            mainHandler.post(() -> {
                if (listener != null) listener.onSirenReceived(parts.length > 2 ? parts[2] : "Emergency", "Just Now");
            });
        }
    }

    private void notifyConnection(boolean isConnected) {
        mainHandler.post(() -> {
            if (listener != null) listener.onConnectionStateChanged(isConnected);
        });
    }

    public void stopService() {
        isRunning = false;
        try { if (socket != null) socket.close(); } catch (Exception ignored) {}
    }
}
