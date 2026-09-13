# ui_part1.py - Self-Contained Industrial Layout with Online/Offline Network Status

PART1 = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>MinePulse AI - Industrial DGMS Statutory Portal</title>
  <link rel="manifest" href="/manifest.json">
  <meta name="theme-color" content="#dc2626">
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
  <script>
    if ('serviceWorker' in navigator) {
      window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js')
          .then(reg => console.log('✅ Coalmine Offline Engine Activated:', reg.scope))
          .catch(err => console.log('SW registration error:', err));
      });
    }
  </script>
  <style>
    body { background-color: #020617; color: #f8fafc; font-family: ui-sans-serif, system-ui, -apple-system, sans-serif; }
    @keyframes siren-blink { 0%, 100% { background-color: #991b1b; } 50% { background-color: #dc2626; } }
    .siren-active { animation: siren-blink 0.6s infinite; }
    @keyframes sos-glow { 0%, 100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(225, 29, 72, 0.7); } 50% { transform: scale(1.06); box-shadow: 0 0 0 8px rgba(225, 29, 72, 0); } }
    .pulse-sos { animation: sos-glow 1.8s infinite; }
  </style>
</head>
<body id="main-body" class="min-h-screen flex flex-col transition-colors duration-300">

  <!-- Emergency Evacuation Siren Flashing Banner -->
  <div id="siren-banner" class="hidden siren-active text-white font-bold p-3 text-center flex justify-between items-center px-4 sm:px-6 z-50">
    <div class="flex items-center space-x-2">
      <span class="text-2xl animate-bounce">🚨</span>
      <span class="text-xs sm:text-sm uppercase tracking-wider font-black">DGMS CMR 153: PIT EVACUATION ALARM ACTIVE</span>
    </div>
    <button onclick="silenceSiren()" class="bg-black text-white text-xs px-3 py-1.5 rounded-lg border border-white font-mono hover:bg-slate-900">MUTE SIREN</button>
  </div>

  <!-- Header with Network Status Indicator -->
  <header class="border-b border-slate-800 bg-slate-900 sticky top-0 z-40 p-3 sm:p-4">
    <div class="max-w-7xl mx-auto flex justify-between items-center w-full">
      <div class="flex items-center space-x-2">
        <span class="text-xl">⛏️</span>
        <h1 class="font-bold text-white text-sm sm:text-base">MinePulse <span class="text-amber-500">AI</span></h1>
        <!-- Dynamic Online/Offline Badge -->
        <span id="net-badge" class="ml-2 text-[10px] px-2 py-0.5 rounded-full font-bold bg-emerald-950 text-emerald-400 border border-emerald-800">ONLINE</span>
      </div>
      
      <div class="flex items-center space-x-1.5 sm:space-x-3">
        <a href="/statutory/form-vi" target="_blank" class="text-[11px] sm:text-xs px-2.5 sm:px-3 py-1.5 rounded-lg bg-amber-500/10 border border-amber-500/30 text-amber-400 font-bold flex items-center space-x-1">
          <span>📄</span>
          <span>Print Form-VI</span>
        </a>

        <button onclick="triggerBroadcastSOS()" title="Trigger Emergency Siren" class="pulse-sos bg-rose-600 hover:bg-rose-500 text-white font-black text-xs px-2.5 sm:px-3 py-1.5 rounded-full border border-rose-300 shadow-md flex items-center space-x-1 cursor-pointer">
          <span class="text-sm">🚨</span>
          <span class="tracking-wider">SOS</span>
        </button>

        <button onclick="tab('dash')" id="bd" class="text-[11px] sm:text-xs px-2.5 sm:px-3 py-1.5 rounded-lg bg-amber-500 text-black font-bold">Dashboard</button>
        <button onclick="tab('field')" id="bf" class="text-[11px] sm:text-xs px-2.5 sm:px-3 py-1.5 rounded-lg bg-slate-800 text-slate-300 font-medium">Statutory Form</button>
      </div>
    </div>
  </header>

  <main class="max-w-7xl mx-auto p-4 flex-1 w-full space-y-4">
    <!-- DASHBOARD VIEW -->
    <div id="vd" class="space-y-4">
      <!-- Sync Status Alert (Only appears when offline records are waiting) -->
      <div id="sync-notice" class="hidden bg-amber-950/70 border border-amber-500/50 p-3 rounded-xl flex items-center justify-between text-xs text-amber-200">
        <div class="flex items-center space-x-2">
          <span class="animate-spin text-base">🔄</span>
          <span><strong id="pending-count">0</strong> inspection log(s) saved in Phone Memory. Network milte hi auto-sync ho jayenge.</span>
        </div>
        <button onclick="forceSync()" class="bg-amber-500 text-black font-bold px-2.5 py-1 rounded text-[11px]">Sync Now</button>
      </div>

      <!-- KPI Status Cards -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
        <div class="p-3 bg-slate-900 border border-slate-800 rounded-xl">
          <p class="text-[10px] text-slate-400 font-medium">Storage Engine</p>
          <h3 class="text-base sm:text-lg font-bold text-emerald-400 mt-1" id="storage-status">IndexedDB Vault</h3>
        </div>
        <div class="p-3 bg-slate-900 border border-slate-800 rounded-xl">
          <p class="text-[10px] text-slate-400 font-medium">Compliance Index</p>
          <h3 class="text-base sm:text-lg font-bold text-emerald-400 mt-1" id="sc">--</h3>
        </div>
        <div class="p-3 bg-slate-900 border border-slate-800 rounded-xl">
          <p class="text-[10px] text-slate-400 font-medium">Total Audits</p>
          <h3 class="text-base sm:text-lg font-bold text-amber-400 mt-1" id="tc">0</h3>
        </div>
        <div class="p-3 bg-slate-900 border border-slate-800 rounded-xl">
          <p class="text-[10px] text-slate-400 font-medium">Network Tunnel</p>
          <h3 class="text-base sm:text-lg font-bold text-emerald-400 mt-1" id="net-label">Online Linked</h3>
        </div>
      </div>

      <!-- Live IoT Telemetry Simulator Strip -->
      <div class="bg-slate-900 border border-slate-800 rounded-xl p-4">
        <div class="flex justify-between items-center mb-3">
          <div>
            <h2 class="font-bold text-sm">Subsurface Telemetry Optical Daemon</h2>
            <p class="text-[11px] text-slate-400">Autonomous sensor pipeline (Runs locally offline)</p>
          </div>
          <button onclick="triggerSimulatedHazard()" class="text-xs bg-slate-800 hover:bg-slate-700 text-amber-400 font-semibold px-3 py-1.5 rounded border border-slate-700">Simulate Gas Spike</button>
        </div>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-2 text-xs">
          <div class="p-2.5 bg-slate-950 rounded border border-slate-800">
            <span class="text-slate-400 block text-[10px]">Methane (CH4)</span>
            <span id="tel-ch4" class="text-base font-mono font-bold text-emerald-400">0.21 %</span>
            <span class="text-[10px] text-slate-500 block">CMR Limit: 1.25%</span>
          </div>
          <div class="p-2.5 bg-slate-950 rounded border border-slate-800">
            <span class="text-slate-400 block text-[10px]">Carbon Monoxide (CO)</span>
            <span id="tel-co" class="text-base font-mono font-bold text-emerald-400">14 ppm</span>
            <span class="text-[10px] text-slate-500 block">Threshold: 50 ppm</span>
          </div>
          <div class="p-2.5 bg-slate-950 rounded border border-slate-800">
            <span class="text-slate-400 block text-[10px]">CAAQMS PM2.5</span>
            <span id="tel-pm" class="text-base font-mono font-bold text-amber-400">72 ug/m3</span>
            <span class="text-[10px] text-slate-500 block">Threshold: 150 ug/m3</span>
          </div>
          <div class="p-2.5 bg-slate-950 rounded border border-slate-800">
            <span class="text-slate-400 block text-[10px]">Bench Seismic Tilt</span>
            <span id="tel-vib" class="text-base font-mono font-bold text-emerald-400">0.02 mm/s</span>
            <span class="text-[10px] text-slate-500 block">Threshold: 5.0 mm/s</span>
          </div>
        </div>
      </div>

      <!-- GIS Interactive Satellite Mine Map -->
      <div class="bg-slate-900 border border-slate-800 rounded-xl p-4">
        <div class="flex justify-between items-center mb-2">
          <div>
            <h2 class="font-bold text-sm">GIS Spatial & Boundary Layout</h2>
            <p class="text-[11px] text-slate-400">Mine Sector Coordinates & Geofencing</p>
          </div>
          <span id="map-status-tag" class="text-[10px] bg-emerald-950 border border-emerald-800 text-emerald-400 px-2 py-1 rounded">Vector Active</span>
        </div>
        <div id="mine-map" class="h-64 w-full rounded-lg border border-slate-800 z-0 bg-slate-950"></div>
      </div>

      <!-- Analytics Charts Section -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div class="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <h2 class="font-bold text-sm mb-2">Colliery Safety Scores (%)</h2>
          <div class="h-52"><canvas id="barChart"></canvas></div>
        </div>
        <div class="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <h2 class="font-bold text-sm mb-2">Statutory Risk Distribution</h2>
          <div class="h-52 flex justify-center"><canvas id="pieChart"></canvas></div>
        </div>
      </div>

      <!-- Collieries Table -->
      <div class="bg-slate-900 border border-slate-800 rounded-xl p-4">
        <h2 class="font-bold text-sm mb-3">Collieries Monitoring & Compliance</h2>
        <div class="overflow-x-auto"><table class="w-full text-left text-xs"><tbody id="ml" class="divide-y divide-slate-800"></tbody></table></div>
      </div>

      <!-- Tamper-Proof Audit Ledger (SHA-256) -->
      <div class="bg-slate-900 border border-slate-800 rounded-xl p-4">
        <div class="flex justify-between items-center mb-3">
          <div>
            <h2 class="font-bold text-sm text-white">Tamper-Proof Audit Ledger (SHA-256)</h2>
            <p class="text-[11px] text-slate-400">Stores both Cloud and Offline Local Vault records</p>
          </div>
          <div class="flex items-center space-x-2">
            <a href="/statutory/form-vi" target="_blank" class="text-[11px] text-amber-400 bg-amber-500/10 border border-amber-500/30 px-3 py-1.5 rounded-lg">🖨️ Print</a>
            <button onclick="load()" class="text-[11px] text-slate-300 bg-slate-800 px-3 py-1.5 rounded-lg border border-slate-700">Refresh</button>
          </div>
        </div>
        <div id="ol" class="space-y-2 text-xs">
          <p class="text-slate-500">Loading statutory inspection records...</p>
        </div>
      </div>
    </div>
"""
