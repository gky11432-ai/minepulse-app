package com.mineguard.dgms;

import android.content.Context;
import android.hardware.camera2.CameraCharacteristics;
import android.hardware.camera2.CameraManager;
import android.media.AudioFormat;
import android.media.AudioManager;
import android.media.AudioTrack;
import android.os.Vibrator;
import android.speech.tts.TextToSpeech;
import java.util.Locale;

public class HardwareController {
    private final Context context;
    private CameraManager cameraManager;
    private Vibrator vibrator;
    private TextToSpeech tts;
    private boolean isTorchOn = false;
    private boolean isSirenActive = false;
    private AudioTrack audioTrack;
    private Thread sirenThread;
    private String cameraId;

    public HardwareController(Context context) {
        this.context = context;
        try {
            this.cameraManager = (CameraManager) context.getSystemService(Context.CAMERA_SERVICE);
            this.vibrator = (Vibrator) context.getSystemService(Context.VIBRATOR_SERVICE);
            if (cameraManager != null) {
                for (String id : cameraManager.getCameraIdList()) {
                    CameraCharacteristics c = cameraManager.getCameraCharacteristics(id);
                    Boolean hasFlash = c.get(CameraCharacteristics.FLASH_INFO_AVAILABLE);
                    Integer facing = c.get(CameraCharacteristics.LENS_FACING);
                    if (hasFlash != null && hasFlash && facing != null && facing == CameraCharacteristics.LENS_FACING_BACK) {
                        cameraId = id;
                        break;
                    }
                }
                if (cameraId == null && cameraManager.getCameraIdList().length > 0) {
                    cameraId = cameraManager.getCameraIdList()[0];
                }
            }
        } catch (Throwable ignored) {}

        try {
            tts = new TextToSpeech(context, status -> {
                if (status == TextToSpeech.SUCCESS && tts != null) {
                    tts.setLanguage(new Locale("hi", "IN"));
                }
            });
        } catch (Throwable ignored) {}
    }

    public synchronized boolean toggleTorch() {
        if (cameraManager == null || cameraId == null) return false;
        try {
            isTorchOn = !isTorchOn;
            cameraManager.setTorchMode(cameraId, isTorchOn);
            return isTorchOn;
        } catch (Throwable e) {
            isTorchOn = false;
            return false;
        }
    }

    public synchronized void startCollierySiren() {
        if (isSirenActive) return;
        isSirenActive = true;

        try {
            if (vibrator != null) {
                long[] pattern = {0, 800, 200, 1000, 200, 1200};
                vibrator.vibrate(pattern, 0);
            }
        } catch (Throwable ignored) {}

        sirenThread = new Thread(() -> {
            int sampleRate = 44100;
            int bufferSize = AudioTrack.getMinBufferSize(sampleRate, AudioFormat.CHANNEL_OUT_MONO, AudioFormat.ENCODING_PCM_16BIT);
            if (bufferSize <= 0) bufferSize = 4096;

            try {
                audioTrack = new AudioTrack(AudioManager.STREAM_ALARM, sampleRate,
                        AudioFormat.CHANNEL_OUT_MONO, AudioFormat.ENCODING_PCM_16BIT,
                        bufferSize, AudioTrack.MODE_STREAM);
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
                            currentFreq += 0.12;
                            if (currentFreq >= 1200.0) ascending = false;
                        } else {
                            currentFreq -= 0.12;
                            if (currentFreq <= 800.0) ascending = true;
                        }
                    }
                    audioTrack.write(buffer, 0, buffer.length);
                }
            } catch (Throwable ignored) {}
        });
        sirenThread.start();

        try {
            if (tts != null) {
                tts.speak("आपातकालीन सायरन! सभी तुरंत सुरक्षित बाहर निकलें।", TextToSpeech.QUEUE_FLUSH, null, "SOS");
            }
        } catch (Throwable ignored) {}
    }

    public synchronized void stopCollierySiren() {
        isSirenActive = false;
        try {
            if (audioTrack != null) { audioTrack.stop(); audioTrack.release(); audioTrack = null; }
            if (sirenThread != null) { sirenThread.interrupt(); sirenThread = null; }
            if (vibrator != null) vibrator.cancel();
            if (tts != null) tts.stop();
        } catch (Throwable ignored) {}
    }

    public boolean isSirenActive() { return isSirenActive; }
}
