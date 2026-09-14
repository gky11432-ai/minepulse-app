# ui_part1.py - Industrial Shell & Clean DOM Structure

PART1 = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>MinePulse AI - Autonomous Pit Portal</title>
  <link rel="manifest" href="/manifest.json">
  <meta name="theme-color" content="#dc2626">
  <script>
    if ('serviceWorker' in navigator) {
      navigator.serviceWorker.register('/sw.js').catch(function(){});
    }
  </script>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { background: #020617; color: #f8fafc; font-family: system-ui, -apple-system, sans-serif; padding-bottom: 40px; }
    .container { max-width: 1100px; margin: 0 auto; padding: 12px; }
    header { background: #0f172a; border-bottom: 1px solid #1e293b; padding: 12px 16px; position: sticky; top: 0; z-index: 50; }
    .nav { max-width: 1100px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center; }
    .brand { font-size: 16px; font-weight: 800; color: #fff; display: flex; align-items: center; gap: 6px; }
    .brand span { color: #f59e0b; }
    .badge { font-size: 10px; font-weight: bold; padding: 3px 8px; border-radius: 9999px; }
    .badge-off { background: #450a0a; color: #f87171; border: 1px solid #991b1b; }
    .badge-on { background: #064e3b; color: #34d399; border: 1px solid #059669; }
    .btn-sos { background: #dc2626; color: #fff; font-weight: 900; font-size: 11px; padding: 6px 12px; border-radius: 9999px; border: 1px solid #fca5a5; cursor: pointer; }
    .btn-action { background: #1e293b; color: #cbd5e1; border: 1px solid #334155; font-size: 11px; font-weight: 600; padding: 6px 10px; border-radius: 8px; cursor: pointer; text-decoration: none; }
    .btn-action.active { background: #f59e0b; color: #000; font-weight: bold; border-color: #f59e0b; }
    .card { background: #0f172a; border: 1px solid #1e293b; border-radius: 12px; padding: 14px; margin-bottom: 12px; }
    .grid-4 { display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px; margin-bottom: 12px; }
    @media(min-width: 768px) { .grid-4 { grid-template-columns: repeat(4, 1fr); } }
    .lbl { font-size: 10px; color: #94a3b8; font-weight: 600; text-transform: uppercase; }
    .val { font-size: 18px; font-weight: bold; margin-top: 4px; }
    .hidden { display: none !important; }
    input, select, textarea { width: 100%; background: #020617; border: 1px solid #334155; color: #fff; padding: 9px; border-radius: 8px; font-size: 12px; margin-top: 4px; margin-bottom: 10px; outline: none; }
    @keyframes siren-blink { 0%, 100% { background: #7f1d1d; } 50% { background: #dc2626; } }
    .siren-bar { background: #dc2626; animation: siren-blink 0.6s infinite; color: white; padding: 10px; font-size: 12px; font-weight: 900; text-align: center; display: flex; justify-content: space-between; align-items: center; }
  </style>
</head>
<body>

  <!-- Emergency Siren Bar -->
  <div id="siren-banner" class="hidden siren-bar">
    <span>🚨 DGMS CMR 153: PIT EVACUATION SIREN ACTIVE</span>
    <button onclick="silenceSiren()" style="background:#000; color:#fff; border:1px solid #fff; padding:4px 8px; border-radius:6px; font-size:11px; cursor:pointer;">MUTE</button>
  </div>

  <!-- Header -->
  <header>
    <div class="nav">
      <div class="brand">
        <span>⛏️</span> MinePulse <span>AI</span>
        <span id="net-badge" class="badge badge-off">CHECKING...</span>
      </div>
      <div style="display: flex; gap: 6px; align-items: center;">
        <a href="/statutory/form-vi" target="_blank" class="btn-action" style="color:#f59e0b; border-color:rgba(245,158,11,0.4);">📄 Print Form-VI</a>
        <button onclick="triggerBroadcastSOS()" class="btn-sos">🚨 SOS</button>
        <button onclick="tab('dash')" id="bd" class="btn-action active">Dashboard</button>
        <button onclick="tab('field')" id="bf" class="btn-action">Statutory Form</button>
      </div>
    </div>
  </header>

  <div class="container">
    <!-- DASHBOARD VIEW -->
    <div id="vd">
      <div id="sync-notice" class="card hidden" style="background:#451a03; border-color:#d97706; color:#fef3c7; display:flex; justify-content:space-between; align-items:center;">
        <div style="font-size:12px;">🔄 <strong id="pending-count">0</strong> log(s) local vault me hain. Network aane par sync honge.</div>
        <button onclick="forceSync()" style="background:#f59e0b; color:#000; border:none; padding:4px 8px; border-radius:6px; font-weight:bold; font-size:11px; cursor:pointer;">Sync</button>
      </div>

      <div class="grid-4">
        <div class="card" style="margin:0;">
          <div class="lbl">Storage Engine</div>
          <div class="val" style="color:#34d399;">IndexedDB Vault</div>
        </div>
        <div class="card" style="margin:0;">
          <div class="lbl">Compliance Index</div>
          <div class="val" style="color:#34d399;" id="sc">91.4%</div>
        </div>
        <div class="card" style="margin:0;">
          <div class="lbl">Total Audits</div>
          <div class="val" style="color:#f59e0b;" id="tc">0</div>
        </div>
        <div class="card" style="margin:0;">
          <div class="lbl">Network Tunnel</div>
          <div class="val" style="color:#f87171;" id="net-label">Local Storage</div>
        </div>
      </div>

      <div class="card">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
          <span style="font-size:13px; font-weight:bold;">Subsurface Telemetry Optical Daemon</span>
          <button onclick="triggerSimulatedHazard()" style="background:#1e293b; color:#f59e0b; border:1px solid #334155; padding:4px 8px; border-radius:6px; font-size:11px; cursor:pointer;">Simulate Spike</button>
        </div>
        <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap:8px;">
          <div style="background:#020617; border:1px solid #1e293b; border-radius:8px; padding:8px;">
            <div class="lbl">Methane (CH4)</div>
            <div id="tel-ch4" style="font-size:15px; font-weight:bold; color:#34d399;">0.21 %</div>
            <div style="font-size:9px; color:#64748b;">Limit: 1.25%</div>
          </div>
          <div style="background:#020617; border:1px solid #1e293b; border-radius:8px; padding:8px;">
            <div class="lbl">Carbon Monoxide</div>
            <div id="tel-co" style="font-size:15px; font-weight:bold; color:#34d399;">14 ppm</div>
            <div style="font-size:9px; color:#64748b;">Limit: 50 ppm</div>
          </div>
          <div style="background:#020617; border:1px solid #1e293b; border-radius:8px; padding:8px;">
            <div class="lbl">CAAQMS PM2.5</div>
            <div id="tel-pm" style="font-size:15px; font-weight:bold; color:#f59e0b;">72 ug/m3</div>
            <div style="font-size:9px; color:#64748b;">Limit: 150 ug/m3</div>
          </div>
          <div style="background:#020617; border:1px solid #1e293b; border-radius:8px; padding:8px;">
            <div class="lbl">Bench Seismic Tilt</div>
            <div id="tel-vib" style="font-size:15px; font-weight:bold; color:#34d399;">0.02 mm/s</div>
            <div style="font-size:9px; color:#64748b;">Limit: 5.0 mm/s</div>
          </div>
        </div>
      </div>

      <div class="card">
        <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
          <span style="font-size:13px; font-weight:bold;">Autonomous Spatial Geofence Grid</span>
          <span style="font-size:10px; color:#34d399;">SECL Gevra Pit Active</span>
        </div>
        <canvas id="mine-map-canvas" height="120" style="width:100%; height:120px; background:#020617; border-radius:8px; border:1px solid #1e293b;"></canvas>
      </div>

      <div class="card">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
          <span style="font-size:13px; font-weight:bold;">Tamper-Proof Audit Ledger (SHA-256)</span>
          <button onclick="load()" style="background:#1e293b; color:#cbd5e1; border:1px solid #334155; padding:4px 8px; border-radius:6px; font-size:11px; cursor:pointer;">Refresh</button>
        </div>
        <div id="ol" style="display:flex; flex-direction:column; gap:8px;"></div>
      </div>
    </div>
"""
