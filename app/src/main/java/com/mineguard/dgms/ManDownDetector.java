package com.mineguard.dgms;

import android.content.Context;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.os.CountDownTimer;

public class ManDownDetector implements SensorEventListener {
    private final Context context;
    private final BleMeshManager bleMeshManager;
    private final SensorManager sensorManager;
    private final Sensor accelerometer;
    private boolean isMonitoring = false;
    private long lastMovementTime;
    private CountDownTimer countdownTimer;

    public interface ManDownListener {
        void onWarningCountdown(int secondsRemaining);
        void onFallDetectedAlarm();
        void onMovementRestored();
    }
    private ManDownListener listener;

    public ManDownDetector(Context context, BleMeshManager bleMeshManager) {
        this.context = context;
        this.bleMeshManager = bleMeshManager;
        this.sensorManager = (SensorManager) context.getSystemService(Context.SENSOR_SERVICE);
        this.accelerometer = (sensorManager != null) ? sensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER) : null;
        this.lastMovementTime = System.currentTimeMillis();
    }

    public void setListener(ManDownListener listener) {
        this.listener = listener;
    }

    public void startMonitoring() {
        if (accelerometer == null || isMonitoring) return;
        sensorManager.registerListener(this, accelerometer, SensorManager.SENSOR_DELAY_UI);
        isMonitoring = true;
        lastMovementTime = System.currentTimeMillis();
    }

    public void stopMonitoring() {
        if (!isMonitoring) return;
        sensorManager.unregisterListener(this);
        isMonitoring = false;
        if (countdownTimer != null) countdownTimer.cancel();
    }

    @Override
    public void onSensorChanged(SensorEvent event) {
        float x = event.values[0];
        float y = event.values[1];
        float z = event.values[2];

        double gMagnitude = Math.sqrt(x * x + y * y + z * z);
        double delta = Math.abs(gMagnitude - SensorManager.GRAVITY_EARTH);

        // Movement detected
        if (delta > 1.8) {
            lastMovementTime = System.currentTimeMillis();
            if (countdownTimer != null) {
                countdownTimer.cancel();
                countdownTimer = null;
                if (listener != null) listener.onMovementRestored();
            }
        } else {
            // Still / No movement for more than 25 seconds
            long stillDuration = System.currentTimeMillis() - lastMovementTime;
            if (stillDuration > 25000 && countdownTimer == null) {
                startPreAlarmCountdown();
            }
        }
    }

    private void startPreAlarmCountdown() {
        countdownTimer = new CountDownTimer(10000, 1000) {
            @Override
            public void onTick(long millisUntilFinished) {
                int sec = (int) (millisUntilFinished / 1000);
                if (listener != null) listener.onWarningCountdown(sec);
            }

            @Override
            public void onFinish() {
                // Auto trigger SOS across all phones
                bleMeshManager.triggerOfflineSos("AUTOFALL-WORKER");
                if (listener != null) listener.onFallDetectedAlarm();
            }
        }.start();
    }

    @Override
    public void onAccuracyChanged(Sensor sensor, int accuracy) {}
}
