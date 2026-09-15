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

    private boolean impactDetected = false;
    private long impactTimestamp = 0;
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
    }

    public void setListener(ManDownListener listener) {
        this.listener = listener;
    }

    public void startMonitoring() {
        if (accelerometer == null || isMonitoring) return;
        sensorManager.registerListener(this, accelerometer, SensorManager.SENSOR_DELAY_UI);
        isMonitoring = true;
        resetState();
    }

    public void stopMonitoring() {
        if (!isMonitoring) return;
        sensorManager.unregisterListener(this);
        isMonitoring = false;
        resetState();
    }

    private void resetState() {
        impactDetected = false;
        impactTimestamp = 0;
        if (countdownTimer != null) {
            countdownTimer.cancel();
            countdownTimer = null;
        }
    }

    @Override
    public void onSensorChanged(SensorEvent event) {
        float x = event.values[0];
        float y = event.values[1];
        float z = event.values[2];

        double gMagnitude = Math.sqrt(x * x + y * y + z * z);

        // Stage 1: केवल असली गिरने या भारी झटके पर ही ट्रिगर होगा (> 24 m/s²)
        // मेज पर सामान्य रखने पर यह वैल्यू 9.8 से 12 तक ही रहती है
        if (gMagnitude > 24.0 && !impactDetected) {
            impactDetected = true;
            impactTimestamp = System.currentTimeMillis();
            return;
        }

        // Stage 2: यदि झटका लगा है, तो चेक करें कि व्यक्ति बेहोश पड़ा है या उठ गया
        if (impactDetected) {
            double delta = Math.abs(gMagnitude - SensorManager.GRAVITY_EARTH);

            // यदि गिरने के बाद व्यक्ति हिल-डुल गया या फ़ोन उठा लिया, तो अलार्म तुरंत रद्द
            if (delta > 2.5) {
                resetState();
                if (listener != null) listener.onMovementRestored();
                return;
            }

            // झटके के बाद 15 सेकंड तक बिल्कुल शून्य हलचल होने पर ही काउंटडाउन शुरू होगा
            long timeSinceImpact = System.currentTimeMillis() - impactTimestamp;
            if (timeSinceImpact > 15000 && countdownTimer == null) {
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
                bleMeshManager.triggerOfflineSos("FALL-EMERGENCY");
                if (listener != null) listener.onFallDetectedAlarm();
                resetState();
            }
        }.start();
    }

    @Override
    public void onAccuracyChanged(Sensor sensor, int accuracy) {}
}
