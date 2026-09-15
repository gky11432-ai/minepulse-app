package com.mineguard.dgms;

import android.content.Context;
import android.hardware.camera2.CameraAccessException;
import android.hardware.camera2.CameraManager;
import android.media.AudioFormat;
import android.media.AudioManager;
import android.media.AudioTrack;
import android.os.Vibrator;
import android.speech.tts.TextToSpeech;
import java.util.Locale;

public class HardwareController {
    private final Context context;
    private final CameraManager cameraManager;
    private final Vibrator vibrator;
    private TextToSpeech tts;
    private boolean isTorchOn = false;
    private boolean isSirenActive = false;
    private AudioTrack audioTrack;
    private Thread sirenThread;
    private String cameraId;

    public HardwareController(Context context) {
        this.context = context;
        this.cameraManager = (CameraManager) context.getSystemService(Context.CAMERA_SERVICE);
        this.vibrator = (Vibrator) context.getSystemService(Context.VIBRATOR_SERVICE);

        try {
            if (cameraManager != null && cameraManager.getCameraIdList().length > 0) {
                cameraId = cameraManager.getCameraIdList()[0];
            }
        } catch (CameraAccessException ignored) {}

        tts = new TextToSpeech(context, status -> {
            if (status == TextToSpeech.SUCCESS) {
                tts.setLanguage(new Locale("hi", "IN"));
            }
        });
    }

    public boolean toggleTorch() {
        if (cameraManager == null || cameraId == null) return false;
        try {
            isTorchOn = !isTorchOn;
            cameraManager.setTorchMode(cameraId, isTorchOn);
            return isTorchOn;
        } catch (Exception e) {
            return false;
        }
    }

    public synchronized void startCollierySiren() {
        if (isSirenActive) return;
        isSirenActive = true;

        if (vibrator != null) {
            long[] pattern = {0, 1000, 300, 1200, 300, 1500};
            vibrator.vibrate(pattern, 0);
        }

        sirenThread = new Thread(() -> {
            int sampleRate = 44100;
            int bufferSize = AudioTrack.getMinBufferSize(
                sampleRate,
                AudioFormat.CHANNEL_OUT_MONO,
                AudioFormat.ENCODING_PCM_16BIT
            );

            audioTrack = new AudioTrack(
                AudioManager.STREAM_ALARM,
                sampleRate,
                AudioFormat.CHANNEL_OUT_MONO,
                AudioFormat.ENCODING_PCM_16BIT,
                bufferSize,
                AudioTrack.MODE_STREAM
            );

            audioTrack.play();
            short[] buffer = new short[bufferSize];
            double currentFreq = 800.0;
            boolean ascending = true;
            double phase = 0.0;

            while (isSirenActive) {
                for (int i = 0; i < buffer.length; i++) {
                    buffer[i] = (short) (Math.sin(phase) * 32767);
                    phase += 2.0 * Math.PI * currentFreq / sampleRate;
                    if (phase > 2.0 * Math.PI) phase -= 2.0 * Math.PI;

                    if (ascending) {
                        currentFreq += 0.08;
                        if (currentFreq >= 1200.0) ascending = false;
                    } else {
                        currentFreq -= 0.08;
                        if (currentFreq <= 800.0) ascending = true;
                    }
                }
                audioTrack.write(buffer, 0, buffer.length);
            }
        });
        sirenThread.start();

        if (tts != null) {
            tts.speak("सावधान! आपातकालीन सायरन बजाया गया है। सभी खदान कर्मचारी सुरक्षित निकासी मार्ग की ओर बढ़ें।",
                    TextToSpeech.QUEUE_FLUSH, null, "SIREN_ALERT");
        }
    }

    public synchronized void stopCollierySiren() {
        isSirenActive = false;
        if (audioTrack != null) {
            try {
                audioTrack.stop();
                audioTrack.release();
            } catch (Exception ignored) {}
            audioTrack = null;
        }
        if (sirenThread != null) {
            sirenThread.interrupt();
            sirenThread = null;
        }
        if (vibrator != null) vibrator.cancel();
        if (tts != null) tts.stop();
    }

    public boolean isSirenActive() {
        return isSirenActive;
    }
}
