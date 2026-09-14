# app_nav.py - Top Navigation, Offline Bilingual & Telemetry (< 170 Lines)

NAV_MODULE = """
<div class="app-topbar">
  <div style="display:flex; align-items:center; gap:10px;">
    <button type="button" class="btn-icon" onclick="toggleAppDrawer()">☰</button>
    <div>
      <div style="font-size:14px; font-weight:900; color:#38bdf8;">MINEGUARD</div>
      <div id="txt-subhead" style="font-size:8.5px; color:#94a3b8;" data-en="DGMS Safe Mining Console" data-hi="डीजीएमएस भूमिगत सुरक्षा कंसोल">डीजीएमएस भूमिगत सुरक्षा कंसोल</div>
    </div>
  </div>
  <div style="display:flex; align-items:center; gap:6px;">
    <button type="button" id="btn-lang" onclick="toggleLanguage()" style="background:#1e293b; border:1px solid #38bdf8; color:#38bdf8; font-weight:800; padding:4px 10px; border-radius:14px; font-size:11px; cursor:pointer;">🌐 English</button>
    <button type="button" id="btn-torch" onclick="toggleTorch()" style="background:#1e293b; border:1px solid #334155; color:#f8fafc; padding:5px 8px; border-radius:8px; font-size:11px; cursor:pointer;">🔦 Torch</button>
  </div>
</div>

<div class="telemetry-bar">
  <div style="display:flex; align-items:center; gap:8px;">
    <span id="pill-shift" style="background:#0284c7; color:#fff; font-weight:bold; padding:2px 6px; border-radius:4px; font-size:9px;">⏱️ SHIFT 1</span>
    <span id="pill-time" style="font-family:monospace; color:#cbd5e1;">--:--:--</span>
  </div>
  <div style="display:flex; align-items:center; gap:8px;">
    <span id="pill-battery">🔋 100%</span>
    <span id="pill-mesh" style="color:#fbbf24; font-weight:bold;">🟠 MESH: CONNECTING</span>
  </div>
</div>

<div id="bar-back">
  <button type="button" class="btn-back" onclick="navigateHome()" id="btn-back-lbl" data-en="← Back to Dashboard" data-hi="← मुख्य डैशबोर्ड">← मुख्य डैशबोर्ड</button>
  <span id="txt-active-module" style="font-size:11px; color:#38bdf8; font-weight:bold;">Module</span>
</div>

<script>
(function() {
  var isTorch = false;
  var track = null;
  var lang = localStorage.getItem('mg_lang') || 'HI';

  window.toggleLanguage = function() {
    lang = (lang === 'HI') ? 'EN' : 'HI';
    localStorage.setItem('mg_lang', lang);
    applyLang();
  };

  function applyLang() {
    var b = document.getElementById('btn-lang');
    if (b) b.innerText = (lang === 'HI') ? '🌐 English' : '🌐 हिन्दी';
    document.querySelectorAll('[data-en][data-hi]').forEach(function(el) {
      el.innerHTML = (lang === 'HI') ? el.getAttribute('data-hi') : el.getAttribute('data-en');
    });
  }

  window.updateTelemetry = function() {
    var now = new Date();
    var h = now.getHours();
    var s = (h >= 6 && h < 14) ? 'SHIFT 1 (06-14)' : (h >= 14 && h < 22) ? 'SHIFT 2 (14-22)' : 'SHIFT 3 (22-06)';
    var sp = document.getElementById('pill-shift');
    if (sp) sp.innerText = '⏱️ ' + s;
    var tp = document.getElementById('pill-time');
    if (tp) tp.innerText = now.toLocaleTimeString();

    if (navigator.getBattery) {
      navigator.getBattery().then(function(bat) {
        var bp = document.getElementById('pill-battery');
        if (bp) bp.innerText = (bat.level * 100 > 20 ? '🔋 ' : '🪫 ') + Math.round(bat.level * 100) + '%';
      }).catch(function(){});
    }
  };

  window.toggleTorch = function() {
    var btn = document.getElementById('btn-torch');
    if (!isTorch) {
      if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } }).then(function(s) {
          track = s.getVideoTracks()[0];
          var c = track.getCapabilities ? track.getCapabilities() : {};
          if (c.torch) {
            track.applyConstraints({ advanced: [{ torch: true }] });
            isTorch = true;
            if (btn) { btn.style.background = '#f59e0b'; btn.style.color = '#000'; }
          } else { alert('Torch not supported'); track.stop(); }
        }).catch(function(){ alert('Camera permission needed'); });
      }
    } else {
      if (track) { track.stop(); track = null; }
      isTorch = false;
      if (btn) { btn.style.background = '#1e293b'; btn.style.color = '#f8fafc'; }
    }
  };

  document.addEventListener('DOMContentLoaded', function() {
    applyLang();
    window.updateTelemetry();
    setInterval(window.updateTelemetry, 1000);
  });
})();
</script>
"""
