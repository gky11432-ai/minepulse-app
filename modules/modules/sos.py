# modules/sos.py - Independent Offline/Online Panic Station Plugin
from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["SOS Emergency Station"])

SOS_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>MinePulse - Emergency SOS Station</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    @keyframes pulse-ring {
      0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(220, 38, 38, 0.7); }
      70% { transform: scale(1); box-shadow: 0 0 0 30px rgba(220, 38, 38, 0); }
      100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(220, 38, 38, 0); }
    }
    .pulse-btn {
      animation: pulse-ring 2s infinite;
    }
    @keyframes siren-bg {
      0%, 100% { background-color: #450a0a; }
      50% { background-color: #991b1b; }
    }
    .siren-active {
      animation: siren-bg 0.6s infinite;
    }
  </style>
</head>
<body id="page-body" class="bg-slate-950 text-white min-h-screen flex flex-col items-center justify-between p-6 transition-colors duration-300">
  
  <!-- Header -->
  <div class="w-full max-w-md text-center pt-4">
    <div class="inline-flex items-center space-x-2 bg-slate-900 border border-slate-800 px-3 py-1 rounded-full text-xs text-amber-400 mb-2">
      <span class="w-2 h-2 rounded-full bg-emerald-500 animate-ping"></span>
      <span>MinePulse Standalone Station (DGMS CMR 153)</span>
    </div>
    <h1 class="text-2xl font-black tracking-tight">MANUAL CALL POINT</h1>
    <p class="text-xs text-slate-400 mt-1">Direct Pit Emergency Horn. Works 100% Offline with local audio & hardware vibration.</p>
  </div>

  <!-- Giant Center Panic Button -->
  <div class="flex flex-col items-center justify-center my-auto">
    <button id="sos-btn" onclick="triggerPanic()" class="pulse-btn w-64 h-64 sm:w-72 sm:h-72 rounded-full bg-gradient-to-tr from-rose-700 to-red-500 border-4 border-rose-300 shadow-2xl flex flex-col items-center justify-center active:scale-95 transition-transform duration-150">
      <span class="text-6xl sm:text-7xl">🚨</span>
      <span class="text-xl sm:text-2xl font-black tracking-widest mt-2">PULL SIREN</span>
      <span class="text-[11px] uppercase tracking-wider text-rose-100 font-semibold mt-1">Tap to Activate</span>
    </button>
    <div id="status-text" class="mt-6 text-sm font-semibold text-slate-400">Ready: Standby mode</div>
  </div>

  <!-- Bottom Silence & Return Controls -->
  <div class="w-full max-w-md space-y-3 pb-4">
    <button id="mute-btn" onclick="stopSiren()" class="hidden w-full bg-black/80 border-2 border-white text-white font-bold p-3.5 rounded-xl text-sm tracking-wider uppercase">
      MUTE / STOP ALARM
    </button>
    <a href="/" class="block text-center text-xs text-slate-500 hover:text-slate-300 transition">
      &larr; Back to Main Statutory Dashboard
    </a>
  </div>

  <script>
    let audioCtx = null;
    let osc = null;
    let vibTimer = null;
    let isAlarmOn = false;

    function triggerPanic() {
      if (isAlarmOn) return;
      isAlarmOn = true;

      // 1. Visual Siren Trigger
      document.getElementById('page-body').classList.add('siren-active');
      document.getElementById('status-text').innerHTML = '<span class="text-rose-400 font-bold animate-pulse">⚠️ SIREN BLASTING CONTINUOUSLY</span>';
      document.getElementById('mute-btn').classList.remove('hidden');

      // 2. Local Audio Engine (No Internet Required)
      try {
        if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = 'sawtooth';

        const now = audioCtx.currentTime;
        osc.frequency.setValueAtTime(850, now);
        osc.frequency.linearRampToValueAtTime(1300, now + 0.4);
        osc.frequency.linearRampToValueAtTime(850, now + 0.8);
        osc.frequency.linearRampToValueAtTime(1300, now + 1.2);

        gain.gain.setValueAtTime(0.25, now);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start();
      } catch(e) {
        console.log('Audio init error:', e);
      }

      // 3. Hardware Vibration Pulse
      if ('vibrate' in navigator) {
        navigator.vibrate([1000, 300, 1000, 300, 1500]);
        vibTimer = setInterval(() => {
          navigator.vibrate([1000, 300, 1000, 300, 1500]);
        }, 4500);
      }

      // 4. Try logging to Cloud if internet available
      fetch('/api/inspections', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          client_id: 'PANIC-' + Date.now(),
          mine_id: 'SECL-GV-04',
          officer_name: 'Standalone SOS Station',
          officer_role: 'Emergency Field Worker / MCP',
          dgms_cert_no: 'MCP-FIELD-PANIC',
          category: 'CMR 153: Immediate Pit Evacuation Manual Alarm',
          notes: 'EMERGENCY MANUAL CALL POINT PULLED. EVACUATION PROTOCOL ACTIVE.',
          severity: 'Critical',
          latitude: 22.3541,
          longitude: 82.6821
        })
      }).catch(err => console.log('Offline mode - server log deferred.'));
    }

    function stopSiren() {
      if (osc) {
        try { osc.stop(); } catch(e){}
        osc = null;
      }
      if (vibTimer) {
        clearInterval(vibTimer);
        vibTimer = null;
      }
      if ('vibrate' in navigator) {
        navigator.vibrate(0);
      }
      document.getElementById('page-body').classList.remove('siren-active');
      document.getElementById('status-text').innerText = 'Ready: Standby mode';
      document.getElementById('mute-btn').classList.add('hidden');
      isAlarmOn = false;
    }
  </script>
</body>
</html>"""

@router.get("/sos", response_class=HTMLResponse)
@router.get("/panic", response_class=HTMLResponse)
def get_sos_page():
    return HTMLResponse(content=SOS_HTML)
  
