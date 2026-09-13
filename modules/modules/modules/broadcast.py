# modules/broadcast.py - Real-time Multi-Device Emergency Sync Engine
from fastapi import APIRouter
from fastapi.responses import HTMLResponse, JSONResponse
from datetime import datetime

router = APIRouter(tags=["Global Multi-Device Broadcast"])

# In-memory Global Alarm State across all connected phones
ALARM_STATE = {
    "is_active": False,
    "triggered_by": None,
    "triggered_at": None,
    "location": "SECL Gevra Sector B"
}

@router.get("/api/broadcast/status")
def get_alarm_status():
    return JSONResponse(content=ALARM_STATE)

@router.post("/api/broadcast/trigger")
def trigger_global_alarm():
    ALARM_STATE["is_active"] = True
    ALARM_STATE["triggered_by"] = "Field Worker / Mobile MCP"
    ALARM_STATE["triggered_at"] = datetime.utcnow().strftime("%H:%M:%S UTC")
    return JSONResponse(content={"status": "TRIGGERED", "broadcast": ALARM_STATE})

@router.post("/api/broadcast/silence")
def silence_global_alarm():
    ALARM_STATE["is_active"] = False
    ALARM_STATE["triggered_by"] = None
    ALARM_STATE["triggered_at"] = None
    return JSONResponse(content={"status": "SILENCED"})

BROADCAST_RECEIVER_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>MinePulse - Multi-Device Receiver Station</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    @keyframes blast-blink {
      0%, 100% { background-color: #450a0a; }
      50% { background-color: #dc2626; }
    }
    .alarm-active {
      animation: blast-blink 0.5s infinite;
    }
    @keyframes pulse-btn {
      0%, 100% { transform: scale(0.96); box-shadow: 0 0 0 0 rgba(220, 38, 38, 0.7); }
      50% { transform: scale(1.02); box-shadow: 0 0 0 25px rgba(220, 38, 38, 0); }
    }
    .pulse-ring {
      animation: pulse-btn 1.8s infinite;
    }
  </style>
</head>
<body id="page" class="bg-slate-950 text-white min-h-screen flex flex-col justify-between p-6 transition-colors">
  <div class="text-center pt-2">
    <div class="inline-flex items-center space-x-2 bg-slate-900 border border-slate-800 px-3 py-1 rounded-full text-xs text-amber-400 mb-2">
      <span class="w-2 h-2 rounded-full bg-emerald-500 animate-ping"></span>
      <span>Broadcast Mesh Active (All Devices Linked)</span>
    </div>
    <h1 class="text-xl sm:text-2xl font-black">MULTI-DEVICE EMERGENCY BEACON</h1>
    <p class="text-xs text-slate-400 mt-1">If anyone triggers the siren, ALL connected phones will blast the evacuation alarm simultaneously.</p>
  </div>

  <div class="flex flex-col items-center justify-center my-auto">
    <button id="sos-btn" onclick="activateEverywhere()" class="pulse-ring w-64 h-64 sm:w-72 sm:h-72 rounded-full bg-gradient-to-tr from-rose-700 to-red-500 border-4 border-rose-300 shadow-2xl flex flex-col items-center justify-center active:scale-95 transition-transform">
      <span class="text-6xl">🚨</span>
      <span class="text-xl sm:text-2xl font-black tracking-widest mt-2 text-white">BROADCAST SOS</span>
      <span class="text-[11px] uppercase tracking-wider text-rose-100 font-semibold mt-1">Blast on All Phones</span>
    </button>
    <div id="status" class="mt-6 text-sm font-semibold text-slate-400">Status: Listening to Network Mesh...</div>
  </div>

  <div class="w-full max-w-md mx-auto space-y-3 pb-2">
    <button id="mute-btn" onclick="silenceEverywhere()" class="hidden w-full bg-black/90 border-2 border-white text-white font-bold p-3.5 rounded-xl text-xs tracking-widest uppercase">
      MUTE ALARM ON ALL PHONES
    </button>
    <a href="/" class="block text-center text-xs text-slate-500 hover:text-slate-300 transition">&larr; Return to Dashboard</a>
  </div>

  <script>
    let audioCtx = null;
    let osc = null;
    let vibInterval = null;
    let isLocallyPlaying = false;

    function startLocalSiren() {
      if (isLocallyPlaying) return;
      isLocallyPlaying = true;
      document.getElementById('page').classList.add('alarm-active');
      document.getElementById('mute-btn').classList.remove('hidden');
      document.getElementById('status').innerHTML = '<span class="text-rose-400 font-bold animate-pulse">🚨 PIT EVACUATION ALARM ENGAGED GLOBALLY!</span>';

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

        gain.gain.setValueAtTime(0.30, now);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start();
      } catch(e) {
        console.log('Audio error:', e);
      }

      if ('vibrate' in navigator) {
        navigator.vibrate([1000, 300, 1000, 300, 1500]);
        vibInterval = setInterval(() => {
          navigator.vibrate([1000, 300, 1000, 300, 1500]);
        }, 4500);
      }
    }

    function stopLocalSiren() {
      if (osc) {
        try { osc.stop(); } catch(e){}
        osc = null;
      }
      if (vibInterval) {
        clearInterval(vibInterval);
        vibInterval = null;
      }
      if ('vibrate' in navigator) {
        navigator.vibrate(0);
      }
      document.getElementById('page').classList.remove('alarm-active');
      document.getElementById('mute-btn').classList.add('hidden');
      document.getElementById('status').innerText = 'Status: Listening to Network Mesh...';
      isLocallyPlaying = false;
    }

    async function activateEverywhere() {
      startLocalSiren();
      try {
        await fetch('/api/broadcast/trigger', { method: 'POST' });
      } catch(e) {
        console.log('Broadcast request failed:', e);
      }
    }

    async function silenceEverywhere() {
      stopLocalSiren();
      try {
        await fetch('/api/broadcast/silence', { method: 'POST' });
      } catch(e) {
        console.log('Silence request failed:', e);
      }
    }

    // Continuous Real-Time Mesh Polling (Every 1.5 seconds)
    setInterval(async () => {
      try {
        const res = await fetch('/api/broadcast/status');
        const data = await res.json();
        if (data.is_active && !isLocallyPlaying) {
          startLocalSiren();
        } else if (!data.is_active && isLocallyPlaying) {
          stopLocalSiren();
        }
      } catch(e) {}
    }, 1500);
  </script>
</body>
</html>"""

@router.get("/broadcast", response_class=HTMLResponse)
@router.get("/mesh", response_class=HTMLResponse)
def get_broadcast_page():
    return HTMLResponse(content=BROADCAST_RECEIVER_HTML)
  
