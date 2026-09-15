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
    private String minerToken = "TK-" + (int)(100 + Math.random() * 900);

    public class LocalBinder extends Binder {
        public MineSafetyService getService() {
            return MineSafetyService.this;
        }
    }

    @Override
    public void onCreate() {
        super.onCreate();

        PowerManager pm = (PowerManager) getSystemService(Context.POWER_SERVICE);
        if (pm != null) {
            wakeLock = pm.newWakeLock(PowerManager.PARTIAL_WAKE_LOCK, "MineGuard:SafetyLock");
            wakeLock.acquire();
        }

        hardwareController = new HardwareController(this);
        bleMeshManager = new BleMeshManager(this, hardwareController);
        sirenRelayManager = new SirenRelayManager(this, hardwareController);
        manDownDetector = new ManDownDetector(this, bleMeshManager);

        createNotificationChannel();
        startForeground(NOTIF_ID, buildForegroundNotification("🟢 DGMS Safety Mesh Active (Underground Ready)"));

        bleMeshManager.startOfflineMesh(minerToken);
        manDownDetector.startMonitoring();
    }

    private void createNotificationChannel() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            NotificationChannel channel = new NotificationChannel(
                    CHANNEL_ID,
                    "MineGuard Underground Safety",
                    NotificationManager.IMPORTANCE_HIGH
            );
            channel.setDescription("Keeps offline mesh active when phone is locked");
            NotificationManager nm = (NotificationManager) getSystemService(Context.NOTIFICATION_SERVICE);
            if (nm != null) nm.createNotificationChannel(channel);
        }
    }

    private Notification buildForegroundNotification(String statusText) {
        Intent notificationIntent = new Intent(this, MainActivity.class);
        PendingIntent pendingIntent = PendingIntent.getActivity(
                this, 0, notificationIntent,
                PendingIntent.FLAG_IMMUTABLE | PendingIntent.FLAG_UPDATE_CURRENT
        );

        return new NotificationCompat.Builder(this, CHANNEL_ID)
                .setContentTitle("MineGuard 24/7 Underground Console")
                .setContentText(statusText)
                .setSmallIcon(android.R.drawable.ic_dialog_alert)
                .setContentIntent(pendingIntent)
                .setOngoing(true)
                .setPriority(NotificationCompat.PRIORITY_HIGH)
                .build();
    }

    public void triggerDualSos() {
        sirenRelayManager.triggerCollieryBroadcast();
        bleMeshManager.triggerOfflineSos(minerToken);
    }

    public void cancelDualSos() {
        hardwareController.stopCollierySiren();
        bleMeshManager.cancelOfflineSos(minerToken);
    }

    public HardwareController getHardwareController() { return hardwareController; }
    public BleMeshManager getBleMeshManager() { return bleMeshManager; }
    public SirenRelayManager getSirenRelayManager() { return sirenRelayManager; }
    public ManDownDetector getManDownDetector() { return manDownDetector; }
    public String getMinerToken() { return minerToken; }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        return START_STICKY;
    }

    @Override
    public IBinder onBind(Intent intent) {
        return binder;
    }

    @Override
    public void onDestroy() {
        super.onDestroy();
        if (wakeLock != null && wakeLock.isHeld()) wakeLock.release();
        if (bleMeshManager != null) bleMeshManager.stopMesh();
        if (manDownDetector != null) manDownDetector.stopMonitoring();
        if (hardwareController != null) hardwareController.stopCollierySiren();
        if (sirenRelayManager != null) sirenRelayManager.stopService();
    }
}
