# mg_siren_audio.py - Hardware Siren Oscillator & Speech Engine (< 150 Lines)

SIREN_AUDIO_MODULE = """
<script>
(function() {
    var audioCtx = null;
    var sirenOsc = null;
    var sirenGain = null;
    var isAudioUnlocked = false;
    var isSirenPlaying = false;

    function getAudioContext() {
        if (!audioCtx) {
            var AudioClass = window.AudioContext || window.webkitAudioContext;
            audioCtx = new AudioClass();
        }
        if (audioCtx.state === 'suspended') {
            audioCtx.resume();
        }
        return audioCtx;
    }

    // Android WebView Audio Autoplay Unlocker
    window.unlockSirenAudio = function() {
        if (isAudioUnlocked) return;
        try {
            var ctx = getAudioContext();
            var buf = ctx.createBuffer(1, 1, 22050);
            var src = ctx.createBufferSource();
            src.buffer = buf;
            src.connect(ctx.destination);
            src.start(0);
            isAudioUnlocked = true;
        } catch(e) {}
    };

    window.addEventListener('touchstart', window.unlockSirenAudio, { passive: true });
    window.addEventListener('click', window.unlockSirenAudio, { passive: true });

    // 800Hz - 1200Hz Statutory Sweep Wave
    window.playDGMSSirenAudio = function(durationMs) {
        durationMs = durationMs || 15000;
        try {
            var ctx = getAudioContext();
            if (ctx.state === 'suspended') ctx.resume();
            if (isSirenPlaying) return;
            isSirenPlaying = true;

            if (navigator.vibrate) {
                navigator.vibrate([1000, 250, 1000, 250, 1500, 300, 2000]);
            }

            sirenOsc = ctx.createOscillator();
            sirenGain = ctx.createGain();
            sirenOsc.type = 'sawtooth';

            sirenGain.gain.setValueAtTime(0.01, ctx.currentTime);
            sirenGain.gain.exponentialRampToValueAtTime(0.95, ctx.currentTime + 0.2);

            sirenOsc.connect(sirenGain);
            sirenGain.connect(ctx.destination);

            var t = ctx.currentTime;
            sirenOsc.frequency.setValueAtTime(800, t);

            var cycle = 2.4;
            var loops = Math.ceil(durationMs / 1000 / cycle);
            for (var i = 0; i < loops; i++) {
                var s = t + (i * cycle);
                sirenOsc.frequency.exponentialRampToValueAtTime(1200, s + (cycle * 0.6));
                sirenOsc.frequency.exponentialRampToValueAtTime(800, s + cycle);
            }

            sirenOsc.start(t);
            setTimeout(function() { window.stopDGMSSirenAudio(); }, durationMs);
        } catch(e) {}
    };

    window.stopDGMSSirenAudio = function() {
        if (!isSirenPlaying) return;
        try {
            if (sirenGain && audioCtx) {
                sirenGain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.3);
                setTimeout(function() {
                    if (sirenOsc) { sirenOsc.stop(); sirenOsc.disconnect(); sirenOsc = null; }
                    isSirenPlaying = false;
                }, 300);
            } else {
                if (sirenOsc) { sirenOsc.stop(); sirenOsc = null; }
                isSirenPlaying = false;
            }
            if (navigator.vibrate) navigator.vibrate(0);
        } catch(e) {
            isSirenPlaying = false;
        }
    };

    window.speakSirenVoice = function(customText) {
        if (!('speechSynthesis' in window)) return;
        try {
            window.speechSynthesis.cancel();
            var text = customText || "सावधान! आपातकालीन सायरन बजाया गया है। सभी खदान कर्मचारी तुरंत सुरक्षित निकासी मार्ग की ओर बढ़ें।";
            var msg = new SpeechSynthesisUtterance(text);
            msg.lang = 'hi-IN';
            msg.rate = 0.92;
            msg.pitch = 1.05;
            window.speechSynthesis.speak(msg);
        } catch(e) {}
    };
})();
</script>
"""
