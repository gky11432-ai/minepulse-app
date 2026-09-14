# app_core.py - Core Architecture, CSS Reset & Main Viewport (< 160 Lines)

CORE_HEAD = """<!DOCTYPE html>
<html lang="hi">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>MineGuard - DGMS Safe Mining Console</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; user-select: none; -webkit-tap-highlight-color: transparent; }
    body { background: #020617; color: #f8fafc; font-family: system-ui, -apple-system, sans-serif; overflow-x: hidden; min-height: 100vh; }
    
    /* Strict Viewport Controller */
    #view-home { display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: calc(100vh - 90px); padding: 20px; }
    #view-module { display: none; padding: 14px; min-height: calc(100vh - 90px); }
    
    /* Top Bar */
    .app-topbar { position: sticky; top: 0; left: 0; width: 100%; background: #020617; border-bottom: 2px solid #1e293b; padding: 8px 12px; display: flex; justify-content: space-between; align-items: center; z-index: 9999; }
    .btn-icon { background: #0f172a; border: 1px solid #38bdf8; color: #38bdf8; width: 40px; height: 40px; border-radius: 8px; font-size: 24px; display: flex; align-items: center; justify-content: center; cursor: pointer; }
    .btn-icon:active { background: #0284c7; color: #fff; }
    
    /* Telemetry HUD Strip */
    .telemetry-bar { background: #0f172a; border-bottom: 1px solid #1e293b; padding: 4px 12px; display: flex; justify-content: space-between; align-items: center; font-size: 10px; color: #94a3b8; }
    
    /* Focus Return Bar */
    #bar-back { display: none; background: #1e293b; border-bottom: 1px solid #334155; padding: 8px 14px; justify-content: space-between; align-items: center; }
    .btn-back { background: #0284c7; color: #fff; font-weight: bold; border: none; padding: 7px 14px; border-radius: 6px; font-size: 11px; cursor: pointer; }
    .btn-back:active { background: #0369a1; }
    
    /* Master Siren Card */
    @keyframes sirenPulseAnim { 0% { transform: scale(1); box-shadow: 0 0 0 0 rgba(239,68,68,0.85); } 70% { transform: scale(1.05); box-shadow: 0 0 0 24px rgba(239,68,68,0); } 100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(239,68,68,0); } }
    .siren-card { background: radial-gradient(circle, #7f1d1d 0%, #450a0a 100%); border: 3px solid #ef4444; border-radius: 24px; width: 100%; max-width: 320px; padding: 40px 20px; display: flex; flex-direction: column; align-items: center; text-align: center; cursor: pointer; animation: sirenPulseAnim 2s infinite ease-in-out; }
    .siren-card:active { transform: scale(0.96); background: #991b1b; }
    
    /* 3-Pai Drawer */
    #drawer-overlay { display: none; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(0,0,0,0.8); z-index: 99998; backdrop-filter: blur(2px); }
    #drawer-menu { position: fixed; top: 0; left: -320px; width: 295px; height: 100vh; background: #0f172a; border-right: 2px solid #334155; z-index: 99999; display: flex; flex-direction: column; transition: left 0.25s ease; }
    #drawer-menu.open { left: 0; }
    .drawer-item { display: flex; align-items: center; gap: 10px; padding: 11px 12px; margin-bottom: 4px; border-radius: 6px; background: #020617; border: 1px solid #1e293b; color: #f1f5f9; font-size: 12px; font-weight: 600; cursor: pointer; }
    .drawer-item:active { background: #0284c7; border-color: #38bdf8; }
  </style>
</head>
<body>
"""

CORE_FOOT = """
</body>
</html>
"""
