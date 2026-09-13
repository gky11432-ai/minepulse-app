# ui_part1.py - Industrial UI with Clean Corner SOS & Full Form Container

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
  <style>
    @keyframes siren-blink {
      0%, 100% { background-color: #991b1b; }
      50% { background-color: #dc2626; }
    }
    .siren-active {
      animation: siren-blink 0.6s infinite;
    }
    @keyframes sos-glow {
      0%, 100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(225, 29, 72, 0.7); }
      50% { transform: scale(1.06); box-shadow: 0 0 0 8px rgba(225, 29, 72, 0); }
    }
    .pulse-sos {
      animation: sos-glow 1.8s infinite;
    }
  </style>
</head>
<body id="main-body" class="bg-slate-950 text-slate-100 min-h-screen font-sans flex flex-col transition-colors duration-300">

  <!-- Emergency Evacuation Siren Flashing Banner -->
  <div id="siren-banner" class="hidden siren-active text-white font-bold p-3 text-center flex justify-between items-center px-4 sm:px-6 z-50">
    <div class="flex items-center space-x-2">
      <span class="text-2xl animate-bounce">🚨</span>
      <span class="text-xs sm:text-sm uppercase tracking-wider font-black">DGMS CMR 153: PIT EVACUATION ALARM ACTIVE</span>
    </div>
    <button onclick="silenceSiren()" class="bg-black text-white text-xs px-3 py-1.5 rounded-lg border border-white font-mono hover:bg-slate-900">MUTE SIREN</button>
  </div>

  <!-- Header with Single Corner SOS Beacon -->
  <header class="border-b border-slate-800 bg-slate-900 sticky top-0 z-40 p-3 sm:p-4">
    <div class="max-w-7xl mx-auto flex justify-between items-center w-full">
      <div class="flex items-center space-x-2">
        <span class="text-xl">⛏️</span>
        <h1 class="font-bold text-white text-base">MinePulse <span class="text-amber-500">AI</span></h1>
      </div>
      
      <div class="flex items-center space-x-2 sm:space-x-3">
        <!-- Minimal Compact Corner SOS Beacon -->
        <button onclick="triggerBroadcastSOS()" title="Trigger Mesh Emergency Siren" class="pulse-sos bg-rose-600 hover:bg-rose-500 text-white font-black text-xs px-3 py-1.5 rounded-full border border-rose-300 shadow-md flex items-center space-x-1 cursor-pointer">
          <span class="text-sm">🚨</span>
          <span class="tracking-wider">SOS</span>
        </button>

        <a href="/statutory/form-vi" target="_blank" class="hidden sm:flex text-xs px-3 py-1.5 rounded-lg bg-slate-800 border border-slate-700 text-amber-400 font-semibold items-center">Export Form-VI</a>
        <button onclick="tab('dash')" id="bd" class="text-xs px-3 py-1.5 rounded-lg bg-amber-500 text-black font-bold">Dashboard</button>
        <button onclick="tab('field')" id="bf" class="text-xs px-3 py-1.5 rounded-lg bg-slate-800 text-slate-300 font-medium">Statutory Form</button>
      </div>
    </div>
  </header>

  <main class="max-w-7xl mx-auto p-4 flex-1 w-full space-y-4">
    <div id="vd" class="space-y-4">
      <!-- KPI Status Cards -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
        <div class="p-3 bg-slate-900 border border-slate-800 rounded-xl">
          <p class="text-[10px] text-slate-400 font-medium">Telegram Siren Bot</p>
          <h3 class="text-base sm:text-lg font-bold text-emerald-400 mt-1">Live Linked</h3>
        </div>
        <div class="p-3 bg-slate-900 border border-slate-800 rounded-xl">
          <p class="text-[10px] text-slate-400 font-medium">Compliance Index</p>
          <h3 class="text-base sm:text-lg font-bold text-emerald-400 mt-1" id="sc">--</h3>
        </div>
        <div class="p-3 bg-slate-900 border border-slate-800 rounded-xl">
          <p class="text-[10px] text-slate-400 font-medium">Total Statutory Audits</p>
          <h3 class="text-base sm:text-lg font-bold text-amber-400 mt-1" id="tc">0</h3>
        </div>
        <div class="p-3 bg-slate-900 border border-slate-800 rounded-xl">
          <p class="text-[10px] text-slate-400 font-medium">Database Persistence</p>
          <h3 class="text-base sm:text-lg font-bold text-emerald-400 mt-1">Cloud Postgres</h3>
        </div>
      </div>

      <!-- Live IoT Telemetry Simulator Strip -->
      <div class="bg-slate-900 border border-slate-800 rounded-xl p-4">
        <div class="flex justify-between items-center mb-3">
          <div>
            <h2 class="font-bold text-sm">Subsurface Telemetry Optical Daemon</h2>
            <p class="text-[11px] text-slate-400">SECL Gevra Sector B optical sensor pipeline</p>
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
            <h2 class="font-bold text-sm">GIS Satellite Geo-Fence & Spatial Map</h2>
            <p class="text-[11px] text-slate-400">Lease boundaries (Gevra Red Polygon) and colliery status</p>
          </div>
          <span class="text-[10px] bg-emerald-950 border border-emerald-800 text-emerald-400 px-2 py-1 rounded">OpenStreetMap Active</span>
        </div>
        <div id="mine-map" class="h-64 w-full rounded-lg border border-slate-800 z-0"></div>
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

      <!-- Audit Logs Stream -->
      <div class="bg-slate-900 border border-slate-800 rounded-xl p-4">
        <div class="flex justify-between items-center mb-3">
          <h2 class="font-bold text-sm">Tamper-Proof Audit Ledger (SHA-256)</h2>
          <button onclick="load()" class="text-[11px] text-slate-400 hover:text-white bg-slate-800 px-2.5 py-1 rounded">Refresh Stream</button>
        </div>
        <div id="ol" class="space-y-2 text-xs"></div>
      </div>
    </div>
"""
