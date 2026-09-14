# app_siren.py - Main Siren Dashboard, Audio Synth & Cross-Phone Relay (< 190 Lines)

SIREN_MODULE = """
<div id="view-home">
  <div class="siren-card" onclick="triggerUniversalSiren()">
    <span style="font-size:64px; line-height:1; margin-bottom:12px;">🚨</span>
    <b id="txt-s-title" style="color:#f87171; font-size:19px;" data-en="EMERGENCY SIREN" data-hi="आपातकालीन सायरन">आपातकालीन सायरन</b>
    <span id="txt-s-desc" style="color:#fca5a5; font-size:11px; margin-top:6px;" data-en="Touch to Sound All-Phone Evacuation" data-hi="सभी फोन में निकासी सायरन बजाएं">सभी फोन में निकासी सायरन बजाएं</span>
    <div id="txt-s-btn" style="margin-top:16px; background:#ef4444; color:#fff; font-size:10px; font-weight:bold; padding:6px 16px; border-radius:20px;" data-en="TAP TO SOUND ALARM" data-hi="सायरन बजाने के लिए छुएं">सायरन बजाने के लिए छुएं</div>
  </div>
  <div id="txt-s-hint" style="margin-top:22px; text-align:center; color:#64748b; font-size:11px;" data-en="For all 28 statutory registers touch <b>☰</b> at top left" data-hi="सभी 28 वैधानिक रजिस्टर्स के लिए ऊपर <b>☰ (3-पाई)</b> टच करें">सभी 28 वैधानिक रजिस्टर्स के लिए ऊपर <b>☰ (3-पाई)</b> टच करें</div>
</div>

<!-- Full-Screen Emergency Strobe HUD on Incoming Alarm -->
<div id="siren-evac-hud" style="display:none; position:fixed; top:0; left:0; width:100vw; height:100vh; background:rgba(185,28,28,0.98); z-index:9999999; flex-direction:column; justify-content:center; align-items:center; text-align:center; padding:16px;">
  <div style="font-size:64px;">🚨</div>
  <div style="font-size:22px; font-weight:900; color:#fff;">EMERGENCY EVACUATION ALARM</div>
  <div style="font-size:13px; font-weight:bold; color:#fef08a; margin-top:4px;">खदान खाली करने का आपातकालीन आदेश (CMR 240)</div>
  <div id="hud-details" style="background:#020617; border:2px solid #ef4444; border-radius:10px; padding:12px; margin:14px 0; max-width:380px; width:100%; text-align:left; font-size:11px; color:#cbd5e1;"></div>
  <button type="button" onclick="stopUniversalSiren()" style="background:#fff; color:#991b1b; font-weight:900; border:none; padding:12px 28px; border-radius:30px; font-size:12px; cursor:pointer;">✓ ACKNOWLEDGE & MUTE</button>
</div>

<script>
(function() {
  var WS_URL = "wss://broker.hivemq.com:8884/mqtt";
  var TOPIC = "mineguard/colliery/siren/live/v2";
  var audioCtx = null, osc = null, gain = null, ws = null, lastId = null;

  function unlockAudio() {
    if (!audioCtx) {
      var A = window.AudioContext || window.webkitAudioContext;
      audioCtx = new A();
    }
    if (audioCtx.state === 'suspended') audioCtx.resume();
  }
  window.addEventListener('touchstart', unlockAudio, { passive: true });
  window.addEventListener('click', unlockAudio, { passive: true });

  function playTone(dur) {
    unlockAudio();
    if (osc) return;
    if (navigator.vibrate) navigator.vibrate([1000, 250, 1000, 250, 1500]);
    osc = audioCtx.createOscillator();
    gain = audioCtx.createGain();
    osc.type = 'sawtooth';
    gain.gain.setValueAtTime(0.01, audioCtx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.9, audioCtx.currentTime + 0.2);
    osc.connect(gain);
    gain.connect(audioCtx.destination);
    var t = audioCtx.currentTime;
    osc.frequency.setValueAtTime(800, t);
    for (var i = 0; i < Math.ceil(dur / 2.4); i++) {
      var s = t + (i * 2.4);
      osc.frequency.exponentialRampToValueAtTime(1200, s + 1.4);
      osc.frequency.exponentialRampToValueAtTime(800, s + 2.4);
    }
    osc.start(t);
  }

  function speakHindi() {
    if (!('speechSynthesis' in window)) return;
    try {
      window.speechSynthesis.cancel();
      var m = new SpeechSynthesisUtterance("सावधान! आपातकालीन सायरन बजाया गया है। सभी कर्मचारी सुरक्षित मार्ग की ओर बढ़ें।");
      m.lang = 'hi-IN';
      window.speechSynthesis.speak(m);
    } catch(e) {}
  }

  function connectRelay() {
    try { ws = new WebSocket(WS_URL, ["mqtt"]); ws.binaryType = "arraybuffer"; } catch(e) { setTimeout(connectRelay, 3000); return; }
    ws.onopen = function() {
      var cId = "mg_" + Math.random().toString(36).substring(2, 8);
      var vh = [0x00, 0x04, 77, 81, 84, 84, 0x04, 0x02, 0x00, 0x3c];
      var pl = [0x00, cId.length];
      for (var i = 0; i < cId.length; i++) pl.push(cId.charCodeAt(i));
      var pkt = [0x10, vh.length + pl.length].concat(vh).concat(pl);
      ws.send(new Uint8Array(pkt));
    };
    ws.onmessage = function(e) {
      var buf = new Uint8Array(e.data);
      if ((buf[0] >> 4) === 2) {
        var top = []; for (var i = 0; i < TOPIC.length; i++) top.push(TOPIC.charCodeAt(i));
        var sub = [0x82, 5 + top.length, 0x00, 0x01, 0x00, top.length].concat(top).concat([0x00]);
        ws.send(new Uint8Array(sub));
        var p = document.getElementById('pill-mesh');
        if (p) { p.innerText = '🟢 SIREN MESH: LIVE'; p.style.color = '#34d399'; }
      } else if ((buf[0] >> 4) === 3) {
        var idx = 1; while (idx < buf.length && (buf[idx++] & 128) !== 0);
        var tLen = (buf[idx] << 8) | buf[idx+1]; idx += 2 + tLen;
        var txt = ""; for (; idx < buf.length; idx++) txt += String.fromCharCode(buf[idx]);
        try { handleAlert(JSON.parse(txt)); } catch(err) {}
      }
    };
    ws.onclose = function() {
      var p = document.getElementById('pill-mesh');
      if (p) { p.innerText = '🟠 MESH: OFFLINE'; p.style.color = '#fbbf24'; }
      setTimeout(connectRelay, 2500);
    };
  }

  window.triggerUniversalSiren = function() {
    var payload = { id: 'SOS-' + Date.now(), time: new Date().toLocaleTimeString(), officer: 'Mine Official' };
    if (ws && ws.readyState === WebSocket.OPEN) {
      var top = [], pay = [];
      var str = JSON.stringify(payload);
      for (var i = 0; i < TOPIC.length; i++) top.push(TOPIC.charCodeAt(i));
      for (var j = 0; j < str.length; j++) pay.push(str.charCodeAt(j));
      var pkt = [0x30, 2 + top.length + pay.length, 0x00, top.length].concat(top).concat(pay);
      ws.send(new Uint8Array(pkt));
    }
    handleAlert(payload);
  };

  function handleAlert(p) {
    if (!p || p.id === lastId) return;
    lastId = p.id;
    var hud = document.getElementById('siren-evac-hud');
    var det = document.getElementById('hud-details');
    if (det) det.innerHTML = "<b>Triggered:</b> " + p.time + "<br><b>Status:</b> Full Underground Evacuation Active";
    if (hud) hud.style.display = 'flex';
    playTone(15);
    speakHindi();
  }

  window.stopUniversalSiren = function() {
    var hud = document.getElementById('siren-evac-hud');
    if (hud) hud.style.display = 'none';
    if (osc) { osc.stop(); osc.disconnect(); osc = null; }
    if ('speechSynthesis' in window) window.speechSynthesis.cancel();
  };

  connectRelay();
})();
</script>
"""
