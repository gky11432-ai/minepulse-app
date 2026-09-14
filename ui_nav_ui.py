# ui_nav_ui.py - 100% Strict Clean Dashboard: Only Siren on Main Page + 3-Pai (☰) Drawer

NAV_UI_MARKUP = """
<style>
  /* ==============================================================
     STRICT CLEAN-ROOM RULE:
     मेन पेज (mode-home) पर Siren, Top Bar और Drawer के अलावा 
     स्क्रीन की हर पुरानी चीज़ को 100% Hide कर दो!
     ============================================================== */
  body.mode-home > *:not(.mg-nav-core):not(#mineguard-gatekeeper):not(#mineguard-evac-hud):not(#mineguard-header-auth-bar) {
      display: none !important;
  }

  /* जब फोकस मोड में कोई कार्ड खुले, तब सिर्फ वही कार्ड दिखेगा */
  body.mode-focus > *:not(.mg-nav-core):not(.active-focus-card):not(#mineguard-gatekeeper):not(#mineguard-evac-hud):not(#mineguard-header-auth-bar) {
      display: none !important;
  }
  body.mode-focus #dashboard-quick-grid {
      display: none !important;
  }
  body.mode-focus #card-focus-bar {
      display: flex !important;
  }
  body.mode-focus .active-focus-card {
      display: block !important;
      width: 100% !important;
      box-sizing: border-box !important;
      padding: 12px !important;
  }

  /* 1. Top Navigation Bar */
  #mineguard-navbar {
      position: sticky;
      top: 0;
      left: 0;
      width: 100%;
      background: #020617;
      border-bottom: 2px solid #1e293b;
      padding: 10px 14px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      z-index: 99999;
      box-sizing: border-box;
      font-family: system-ui, -apple-system, sans-serif;
  }
  .nav-left-group {
      display: flex;
      align-items: center;
      gap: 12px;
  }
  .hamburger-btn {
      background: #0f172a;
      border: 1px solid #38bdf8;
      color: #38bdf8;
      width: 42px;
      height: 42px;
      border-radius: 8px;
      font-size: 26px;
      line-height: 1;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      box-shadow: 0 0 12px rgba(56, 189, 248, 0.3);
  }
  .hamburger-btn:active {
      background: #0284c7;
      color: #ffffff;
  }

  /* 2. Main Center Screen: ONLY SIREN */
  #dashboard-quick-grid {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      min-height: 75vh;
      padding: 20px;
      box-sizing: border-box;
      font-family: system-ui, sans-serif;
  }

  @keyframes sirenPulseAnim {
      0% { transform: scale(1); box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.85); }
      70% { transform: scale(1.05); box-shadow: 0 0 0 26px rgba(239, 68, 68, 0); }
      100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
  }

  .main-siren-card {
      background: radial-gradient(circle, #7f1d1d 0%, #450a0a 100%);
      border: 3px solid #ef4444;
      border-radius: 24px;
      width: 100%;
      max-width: 320px;
      padding: 40px 20px;
      display: flex;
      flex-direction: column;
      align-items: center;
      text-align: center;
      cursor: pointer;
      animation: sirenPulseAnim 2s infinite ease-in-out;
      box-shadow: 0 12px 35px rgba(0,0,0,0.85);
  }
  .main-siren-card:active {
      transform: scale(0.96);
      background: #991b1b;
  }

  /* 3. Side Drawer (3-Pai List Menu) */
  #mineguard-drawer-overlay {
      display: none;
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      background: rgba(0, 0, 0, 0.8);
      z-index: 999999;
      backdrop-filter: blur(2px);
  }
  #mineguard-drawer {
      position: fixed;
      top: 0;
      left: -320px;
      width: 295px;
      height: 100vh;
      background: #0f172a;
      border-right: 2px solid #334155;
      z-index: 1000000;
      display: flex;
      flex-direction: column;
      transition: left 0.25s cubic-bezier(0.4, 0, 0.2, 1);
      box-shadow: 10px 0 30px rgba(0,0,0,0.8);
      font-family: system-ui, sans-serif;
  }
  #mineguard-drawer.open {
      left: 0;
  }
  .drawer-header {
      background: #020617;
      padding: 14px;
      border-bottom: 1px solid #1e293b;
      display: flex;
      justify-content: space-between;
      align-items: center;
  }
  .drawer-body {
      flex: 1;
      overflow-y: auto;
      padding: 10px;
  }
  .drawer-cat-title {
      font-size: 10px;
      font-weight: 900;
      color: #38bdf8;
      letter-spacing: 0.5px;
      text-transform: uppercase;
      padding: 12px 8px 4px 8px;
  }
  .drawer-item {
      display: flex;
      align-items: center;
      gap: 10px;
      padding: 10px 12px;
      margin-bottom: 3px;
      border-radius: 6px;
      background: #020617;
      border: 1px solid #1e293b;
      color: #f1f5f9;
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
  }
  .drawer-item:active {
      background: #0284c7;
      border-color: #38bdf8;
  }

  /* 4. Return Bar */
  #card-focus-bar {
      display: none;
      background: #1e293b;
      border-bottom: 1px solid #334155;
      padding: 8px 14px;
      justify-content: space-between;
      align-items: center;
      font-family: system-ui, sans-serif;
  }
</style>

<!-- TOP NAVBAR -->
<div id="mineguard-navbar" class="mg-nav-core">
    <div class="nav-left-group">
        <button type="button" class="hamburger-btn" onclick="toggleMineGuardDrawer()" title="Open Menu">☰</button>
        <div>
            <div style="font-size:14px; font-weight:900; color:#38bdf8; letter-spacing:0.5px;">MINEGUARD</div>
            <div style="font-size:9px; color:#94a3b8;">DGMS Safe Mining Console</div>
        </div>
    </div>
    <div style="display:flex; align-items:center; gap:8px;">
        <button type="button" id="btn-quick-torch" onclick="toggleHardwareTorch()" style="background:#1e293b; border:1px solid #334155; color:#f8fafc; padding:6px 10px; border-radius:8px; font-size:11px; cursor:pointer;">
            🔦 Torch
        </button>
    </div>
</div>

<!-- FOCUS RETURN BAR (Sirf tab dikhega jab koi register open hoga) -->
<div id="card-focus-bar" class="mg-nav-core">
    <button type="button" onclick="showDashboardHome()" style="background:#0284c7; color:#fff; font-weight:bold; border:none; padding:7px 14px; border-radius:6px; font-size:11px; cursor:pointer;">
        ← Back to Dashboard
    </button>
    <span id="active-card-title" style="font-size:11px; color:#38bdf8; font-weight:bold;">Module View</span>
</div>

<!-- MAIN PAGE: ONLY EMERGENCY SIREN (Zero Clutter) -->
<div id="dashboard-quick-grid" class="mg-nav-core">
    <div class="main-siren-card" onclick="triggerUniversalCollierySOS()">
        <span style="font-size:64px; line-height:1; margin-bottom:12px;">🚨</span>
        <b style="color:#f87171; font-size:19px; letter-spacing:0.5px;">EMERGENCY SIREN</b>
        <span style="color:#fca5a5; font-size:11px; margin-top:6px; font-weight:600;">Touch to Sound All-Phone Evacuation</span>
        <div style="margin-top:16px; background:#ef4444; color:#fff; font-size:10px; font-weight:bold; padding:5px 14px; border-radius:20px;">
            TAP TO SOUND ALARM
        </div>
    </div>
    
    <div style="margin-top:24px; text-align:center; color:#64748b; font-size:11px; line-height:1.5;">
        बाकी सभी 28 रजिस्टर्स और रिपोर्ट्स के लिए<br>ऊपर बाईं तरफ <b>☰ (3-पाई)</b> टच करें
    </div>
</div>

<!-- 3-PAI DRAWER OVERLAY & FULL REGISTER LIST -->
<div id="mineguard-drawer-overlay" class="mg-nav-core" onclick="toggleMineGuardDrawer()"></div>
<div id="mineguard-drawer" class="mg-nav-core">
    <div class="drawer-header">
        <div style="display:flex; align-items:center; gap:8px;">
            <span style="font-size:20px;">⛑️</span>
            <div>
                <div style="font-size:12px; font-weight:bold; color:#f8fafc;">STATUTORY REGISTERS</div>
                <div style="font-size:9px; color:#94a3b8;">Mines Act 1952 & CMR 2017</div>
            </div>
        </div>
        <button type="button" onclick="toggleMineGuardDrawer()" style="background:transparent; border:none; color:#94a3b8; font-size:18px; cursor:pointer;">✕</button>
    </div>

    <!-- Search Box inside Drawer -->
    <div style="padding:10px 10px 4px 10px;">
        <input type="text" id="drawer-search-input" onkeyup="filterDrawerItems()" placeholder="🔍 रजिस्टर खोजें..." style="width:100%; background:#020617; border:1px solid #334155; color:#fff; padding:8px; border-radius:6px; font-size:11px; box-sizing:border-box;">
    </div>

    <div class="drawer-body" id="drawer-items-list">
        <!-- Reports & Downloads -->
        <div class="drawer-cat-title">📑 Reports & Document Downloads</div>
        <div class="drawer-item" onclick="openForm6ReportDirect()"><span>📄</span> Form 6 (Save as PDF / Print)</div>
        <div class="drawer-item" onclick="openSingleModule('statutory-backup-card', 'Audit Export & Backup')"><span>💾</span> All Statutory Logs (Excel/CSV Export)</div>

        <!-- Shift & Attendance -->
        <div class="drawer-cat-title">📋 Shift & Personnel</div>
        <div class="drawer-item" onclick="openSingleModule('statutory-attendance-card', 'Form-B Attendance')"><span>⏱️</span> Form B हाजिरी (Badge Punch)</div>
        <div class="drawer-item" onclick="openSingleModule('statutory-tracking-card', 'P2P Tracking Radar')"><span>📍</span> Personnel ट्रैकिंग (P2P Mesh)</div>
        <div class="drawer-item" onclick="openSingleModule('statutory-diary-card', 'Sirdar Shift Diary')"><span>📖</span> माइनिंग सरदार डायरी (CMR 48)</div>
        <div class="drawer-item" onclick="openSingleModule('statutory-lamproom-card', 'Lamp Room Register')"><span>💡</span> Lamp Room Register</div>
        <div class="drawer-item" onclick="openSingleModule('statutory-handover-card', 'Shift Handover')"><span>🤝</span> Shift Handover Register</div>
        <div class="drawer-item" onclick="openSingleModule('statutory-muster-card', 'Muster Roll')"><span>👥</span> Muster Roll (Form A)</div>

        <!-- Safety Audits -->
        <div class="drawer-cat-title">🛡️ Statutory Safety Audits</div>
        <div class="drawer-item" onclick="openSingleModule('statutory-ventilation-card', 'Ventilation Audit')"><span>💨</span> Ventilation & Gas Audit (Reg 153)</div>
        <div class="drawer-item" onclick="openSingleModule('statutory-strata-card', 'Strata Control')"><span>🪨</span> Strata & Roof Support (Reg 48)</div>
        <div class="drawer-item" onclick="openSingleModule('statutory-blasting-card', 'Blasting Audit')"><span>💥</span> Blasting & Explosives (Reg 184)</div>
        <div class="drawer-item" onclick="openSingleModule('statutory-inundation-card', 'Inundation Register')"><span>🌊</span> Inundation & Water Danger</div>
        <div class="drawer-item" onclick="openSingleModule('statutory-dust-card', 'Coal Dust Register')"><span>🌫️</span> Coal Dust & Water Spraying</div>
        <div class="drawer-item" onclick="openSingleModule('statutory-fire-card', 'Mine Fire Audit')"><span>🔥</span> Spontaneous Combustion & Fire</div>
        <div class="drawer-item" onclick="openSingleModule('statutory-medical-card', 'Medical PME')"><span>🏥</span> Initial & Periodic Medical (PME)</div>
        <div class="drawer-item" onclick="openSingleModule('statutory-smp-card', 'Safety Management')"><span>📋</span> Safety Management Plan (SMP)</div>

        <!-- Plant & Machinery -->
        <div class="drawer-cat-title">🚜 Machinery & Electrical</div>
        <div class="drawer-item" onclick="openSingleModule('statutory-machinery-card', 'HEMM Machinery')"><span>🚜</span> HEMM & Machinery Fitness</div>
        <div class="drawer-item" onclick="openSingleModule('statutory-haulage-card', 'Haulage Track')"><span>🚂</span> Haulage & Track Inspection</div>
        <div class="drawer-item" onclick="openSingleModule('statutory-electrical-card', 'Electrical Flameproof')"><span>⚡</span> Flameproof Electrical Apparatus</div>
        <div class="drawer-item" onclick="openSingleModule('statutory-winding-card', 'Shaft Winding')"><span>🏗️</span> Shaft & Winding Installation</div>
        <div class="drawer-item" onclick="openSingleModule('statutory-calibration-card', 'Gas Calibration')"><span>🎛️</span> Methanometer / Gas Calibration</div>

        <!-- Emergency & Compliance -->
        <div class="drawer-cat-title">🚨 Emergency & Compliance</div>
        <div class="drawer-item" onclick="openSingleModule('statutory-accident-card', 'Accident Form IV')"><span>⚠️</span> Accident & Occurrence (Form IV-A)</div>
        <div class="drawer-item" onclick="openSingleModule('statutory-rescue-card', 'Rescue Apparatus')"><span>🤿</span> Rescue & SCSR Apparatus</div>
        <div class="drawer-item" onclick="openSingleModule('statutory-simulator-card', 'Hazard Simulator')"><span>🎮</span> Pit Safety Hazard Simulator</div>
        <div class="drawer-item" onclick="openSingleModule('statutory-voice-card', 'Voice Log')"><span>🎙️</span> Statutory Voice Log</div>
    </div>
</div>

<script>
  // पेज लोड होते ही तुरंत होम मोड लागू करो ताकि पुरानी कोई चीज़ 1 सेकंड भी न दिखे
  document.body.classList.add('mode-home');
</script>
"""
