package com.mineguard.dgms;

import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.app.Service;
import android.content.Context;
import android.content.Intent;
import android.os.Binder;
import android.os.Build;
import android.os.IBinder;
import android.os.PowerManager;
import androidx.core.app.NotificationCompat;

public class MineSafetyService extends Service {
    private static final String CHANNEL_ID = "MineGuard_Background_Service";
    private static final int NOTIF_ID = 1001;

    private final IBinder binder = new LocalBinder();
    private PowerManager.WakeLock wakeLock;
    private HardwareController hardwareController;
    private BleMeshManager bleMeshManager;
    private SirenRelayManager sirenRelayManager;
    private ManDownDetector manDownDetector;
    private TelemetryEngine telemetryEngine;
    private boolean autoSirenTriggered = false;

    public class LocalBinder extends Binder {
        public MineSafetyService getService() { return MineSafetyService.this; }
    }

    @Override
    public void onCreate() {
        super.onCreate();
        try {
            PowerManager pm = (PowerManager) getSystemService(Context.POWER_SERVICE);
            if (pm != null) {
                wakeLock = pm.newWakeLock(PowerManager.PARTIAL_WAKE_LOCK, "MineGuard:UnbrokenLock");
                wakeLock.setReferenceCounted(false);
                wakeLock.acquire();
            }

            hardwareController = new HardwareController(this);
            bleMeshManager = new BleMeshManager(this, hardwareController);
            sirenRelayManager = new SirenRelayManager(this, hardwareController);
            manDownDetector = new ManDownDetector(this, bleMeshManager);
            telemetryEngine = new TelemetryEngine();

            createNotificationChannel();
            startForeground(NOTIF_ID, buildForegroundNotification("🟢 24/7 Mine Mesh & Telemetry Active"));

            AuthManager auth = new AuthManager(this);
            bleMeshManager.configureOfficer(auth.getOfficerName(), auth.getOfficerRole());
            bleMeshManager.startOfflineMesh();
            manDownDetector.startMonitoring();
            
            // Listen for genuine hardware/manual threshold breaches
            setupTelemetryAutoSiren();
        } catch (Throwable ignored) {}
    }

    private void setupTelemetryAutoSiren() {
        telemetryEngine.setListener((ch4, co, o2, airflow, isDanger) -> {
            if (isDanger && !autoSirenTriggered) {
                autoSirenTriggered = true;
                triggerDualSos();
            }
        });
    }

    private void createNotificationChannel() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            try {
                NotificationChannel channel = new NotificationChannel(
                        CHANNEL_ID, "MineGuard Underground Safety", NotificationManager.IMPORTANCE_LOW
                );
                channel.setDescription("Ensures background siren & telemetry reception");
                NotificationManager nm = (NotificationManager) getSystemService(Context.NOTIFICATION_SERVICE);
                if (nm != null) nm.createNotificationChannel(channel);
            } catch (Throwable ignored) {}
        }
    }

    private Notification buildForegroundNotification(String statusText) {
        Intent intent = new Intent(this, MainActivity.class);
        PendingIntent pi = PendingIntent.getActivity(this, 0, intent, PendingIntent.FLAG_IMMUTABLE | PendingIntent.FLAG_UPDATE_CURRENT);
        return new NotificationCompat.Builder(this, CHANNEL_ID)
                .setContentTitle("MineGuard 24/7 Mission Control")
                .setContentText(statusText)
                .setSmallIcon(android.R.drawable.ic_dialog_alert)
                .setContentIntent(pi)
                .setOngoing(true)
                .setPriority(NotificationCompat.PRIORITY_LOW)
                .build();
    }

    public void triggerDualSos() {
        if (sirenRelayManager != null) sirenRelayManager.triggerCollieryBroadcast();
        if (bleMeshManager != null) bleMeshManager.triggerOfflineSos();
    }

    public void cancelDualSos() {
        autoSirenTriggered = false; // Reset lock so it can trigger again if needed
        if (hardwareController != null) hardwareController.stopCollierySiren();
        if (bleMeshManager != null) bleMeshManager.cancelOfflineSos();
    }

    public HardwareController getHardwareController() { return hardwareController; }
    public BleMeshManager getBleMeshManager() { return bleMeshManager; }
    public TelemetryEngine getTelemetryEngine() { return telemetryEngine; }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) { return START_STICKY; }
    @Override
    public IBinder onBind(Intent intent) { return binder; }

    @Override
    public void onDestroy() {
        super.onDestroy();
        try {
            if (wakeLock != null && wakeLock.isHeld()) wakeLock.release();
            if (bleMeshManager != null) bleMeshManager.stopMesh();
            if (manDownDetector != null) manDownDetector.stopMonitoring();
            if (hardwareController != null) hardwareController.stopCollierySiren();
            if (sirenRelayManager != null) sirenRelayManager.stopService();
        } catch (Throwable ignored) {}
    }
}
