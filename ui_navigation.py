# ui_navigation.py - Clean Dashboard with 3-Line Hamburger Drawer (☰), Top Emergency SOS & Single-Card Focus

NAVIGATION_MODULE = """
<style>
  /* 1. Top Fixed Navigation Bar */
  #mineguard-navbar {
      position: sticky;
      top: 0;
      left: 0;
      width: 100%;
      background: #020617;
      border-bottom: 2px solid #1e293b;
      padding: 8px 12px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      z-index: 10000;
      box-sizing: border-box;
      font-family: system-ui, -apple-system, sans-serif;
  }
  .nav-left-group {
      display: flex;
      align-items: center;
      gap: 10px;
  }
  .hamburger-btn {
      background: #0f172a;
      border: 1px solid #38bdf8;
      color: #38bdf8;
      width: 36px;
      height: 36px;
      border-radius: 8px;
      font-size: 20px;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      box-shadow: 0 0 10px rgba(56, 189, 248, 0.2);
  }
  .hamburger-btn:active {
      background: #0284c7;
      color: #fff;
  }

  /* Pulsing High-Visibility Top SOS Button */
  @keyframes sosPulseAnim {
      0% {
          transform: scale(1);
          box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.9);
      }
      70% {
          transform: scale(1.06);
          box-shadow: 0 0 0 12px rgba(239, 68, 68, 0);
      }
      100% {
          transform: scale(1);
          box-shadow: 0 0 0 0 rgba(239, 68, 68, 0);
      }
  }
  .top-sos-btn {
      background: #dc2626;
      color: #ffffff;
      font-weight: 900;
      border: 2px solid #ef4444;
      padding: 6px 14px;
      border-radius: 20px;
      font-size: 11px;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 5px;
      animation: sosPulseAnim 1.4s infinite;
      letter-spacing: 0.5px;
  }
  .top-sos-btn:active {
      background: #991b1b;
      transform: scale(0.95);
  }

  /* 2. Side Drawer (3-Pai List Menu) */
  #mineguard-drawer-overlay {
      display: none;
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      background: rgba(0, 0, 0, 0.75);
      z-index: 999999;
      backdrop-filter: blur(2px);
  }
  #mineguard-drawer {
      position: fixed;
      top: 0;
      left: -320px;
      width: 290px;
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
      padding: 10px 8px 4px 8px;
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

  /* 3. Clean Dashboard Quick-Grid */
  #dashboard-quick-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 12px;
      padding: 16px;
      font-family: system-ui, sans-serif;
  }
  .quick-tile {
      background: #0f172a;
      border: 1px solid #334155;
      border-radius: 10px;
      padding: 16px 12px;
      display: flex;
      flex-direction: column;
      align-items: center;
      text-align: center;
      cursor: pointer;
      box-shadow: 0 4px 10px rgba(0,0,0,0.4);
      transition: transform 0.1s;
  }
  .quick-tile:active {
      transform: scale(0.97);
      background: #1e293b;
      border-color: #38bdf8;
  }

  /* 4. Active Card Focus Mode Bar */
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

<!-- TOP NAVBAR (3-Pai Button + Top SOS Emergency Siren + Flashlight) -->
<div id="mineguard-navbar">
    <div class="nav-left-group">
        <!-- 3-Pai Hamburger Touch Button -->
        <button type="button" class="hamburger-btn" onclick="toggleMineGuardDrawer()" title="Open Menu">
            ☰
        </button>
        <div>
            <div style="font-size:13px; font-weight:900; color:#38bdf8; letter-spacing:0.5px;">MINEGUARD</div>
            <div style="font-size:8px; color:#94a3b8;">DGMS Underground Console</div>
        </div>
    </div>

    <!-- TOP EMERGENCY ALL-PHONE SOS SIREN TRIGGER -->
    <button type="button" class="top-sos-btn" onclick="triggerUniversalCollierySOS()" title="Trigger All-Phone Siren">
        🚨 <span>SOS सायरन</span>
    </button>

    <div style="display:flex; align-items:center; gap:6px;">
        <!-- Torch Toggle -->
        <button type="button" id="btn-quick-torch" onclick="toggleHardwareTorch()" style="background:#1e293b; border:1px solid #334155; color:#f8fafc; padding:6px 8px; border-radius:8px; font-size:10px; cursor:pointer;">
            🔦 Torch
        </button>
    </div>
</div>

<!-- FOCUS RETURN BAR (Shown when a single module is open) -->
<div id="card-focus-bar">
    <button type="button" onclick="showDashboardHome()" style="background:#0284c7; color:#fff; font-weight:bold; border:none; padding:6px 12px; border-radius:6px; font-size:11px; cursor:pointer;">
        ← Back to Dashboard
    </button>
    <span id="active-card-title" style="font-size:11px; color:#38bdf8; font-weight:bold;">Module View</span>
</div>

<!-- DASHBOARD 6 QUICK ACTION TILES (Main Clean Screen) -->
<div id="dashboard-quick-grid">
    <!-- Big SOS Siren Tile on Dashboard -->
    <div class="quick-tile" onclick="triggerUniversalCollierySOS()" style="border:1px solid #ef4444; background:#450a0a;">
        <span style="font-size:32px; margin-bottom:4px;">🚨</span>
        <b style="color:#f87171; font-size:12px;">Emergency सायरन</b>
        <span style="color:#fca5a5; font-size:9px; margin-top:2px;">All-Phone P2P Evacuation</span>
    </div>

    <div class="quick-tile" onclick="openSingleModule('statutory-attendance-card', 'Form-B Attendance')">
        <span style="font-size:32px; margin-bottom:4px;">⏱️</span>
        <b style="color:#f8fafc; font-size:12px;">Form B हाजिरी</b>
        <span style="color:#94a3b8; font-size:9px; margin-top:2px;">Scan Badge / Shift In-Out</span>
    </div>

    <div class="quick-tile" onclick="openSingleModule('statutory-tracking-card', 'P2P Location Radar')">
        <span style="font-size:32px; margin-bottom:4px;">📍</span>
        <b style="color:#38bdf8; font-size:12px;">Worker ट्रैकिंग</b>
        <span style="color:#94a3b8; font-size:9px; margin-top:2px;">Offline P2P Mesh Radar</span>
    </div>

    <div class="quick-tile" onclick="openForm6ReportDirect()">
        <span style="font-size:32px; margin-bottom:4px;">📄</span>
        <b style="color:#34d399; font-size:12px;">Form 6 रिपोर्ट</b>
        <span style="color:#94a3b8; font-size:9px; margin-top:2px;">View & Save as PDF</span>
    </div>

    <div class="quick-tile" onclick="openSingleModule('statutory-diary-card', 'Sirdar & Overman Diary')">
        <span style="font-size:32px; margin-bottom:4px;">📖</span>
        <b style="color:#facc15; font-size:12px;">सरदार डायरी</b>
        <span style="color:#94a3b8; font-size:9px; margin-top:2px;">CMR 48 Statutory Diary</span>
    </div>

    <div class="quick-tile" onclick="toggleMineGuardDrawer()">
        <span style="font-size:32px; margin-bottom:4px;">☰</span>
        <b style="color:#c084fc; font-size:12px;">सभी 28 रजिस्टर्स</b>
        <span style="color:#94a3b8; font-size:9px; margin-top:2px;">Open Full Menu List</span>
    </div>
</div>

<!-- SLIDE-OUT 3-PAI DRAWER MENU -->
<div id="mineguard-drawer-overlay" onclick="toggleMineGuardDrawer()"></div>
<div id="mineguard-drawer">
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
        <input type="text" id="drawer-search-input" onkeyup="filterDrawerItems()" placeholder="🔍 रजिस्टर या ऑडिट खोजें..." style="width:100%; background:#020617; border:1px solid #334155; color:#fff; padding:8px; border-radius:6px; font-size:11px; box-sizing:border-box;">
    </div>

    <div class="drawer-body" id="drawer-items-list">
        
        <!-- Emergency Section in Drawer -->
        <div class="drawer-cat-title" style="color:#ef4444;">🚨 Emergency Actions</div>
        <div class="drawer-item" onclick="triggerUniversalCollierySOS()" style="background:#450a0a; border-color:#ef4444; color:#fca5a5;">
            <span>🚨</span> <b>Trigger All-Mobile Emergency Siren</b>
        </div>

        <!-- Reports & Downloads -->
        <div class="drawer-cat-title">📑 Reports & Document Downloads</div>
        <div class="drawer-item" onclick="openForm6ReportDirect()">
            <span>📄</span> Form 6 (Save as PDF / Print)
        </div>
        <div class="drawer-item" onclick="openSingleModule('statutory-backup-card', 'Audit Export & Backup')">
            <span>💾</span> All Statutory Logs (Excel/CSV Export)
        </div>

        <!-- Shift & Attendance -->
        <div class="drawer-cat-title">📋 Shift & Personnel</div>
        <div class="drawer-item" onclick="openSingleModule('statutory-attendance-card', 'Form-B Attendance')">
            <span>⏱️</span> Form B हाजिरी (Badge Punch)
        </div>
        <div class="drawer-item" onclick="openSingleModule('statutory-tracking-card', 'P2P Tracking Radar')">
            <span>📍</span> Personnel ट्रैकिंग (P2P Mesh)
        </div>
        <div class="drawer-item" onclick="openSingleModule('statutory-diary-card', 'Sirdar Shift Diary')">
            <span>📖</span> माइनिंग सरदार डायरी (CMR 48)
        </div>
        <div class="drawer-item" onclick="openSingleModule('statutory-lamproom-card', 'Lamp Room Register')">
            <span>💡</span> Lamp Room Register
        </div>
        <div class="drawer-item" onclick="openSingleModule('statutory-handover-card', 'Shift Handover')">
            <span>🤝</span> Shift Handover Register
        </div>
        <div class="drawer-item" onclick="openSingleModule('statutory-muster-card', 'Muster Roll')">
            <span>👥</span> Muster Roll (Form A)
        </div>

        <!-- Safety Audits -->
        <div class="drawer-cat-title">🛡️ Statutory Safety Audits</div>
        <div class="drawer-item" onclick="openSingleModule('statutory-ventilation-card', 'Ventilation Audit')">
            <span>💨</span> Ventilation & Gas Audit (Reg 153)
        </div>
        <div class="drawer-item" onclick="openSingleModule('statutory-strata-card', 'Strata Control')">
            <span>🪨</span> Strata & Roof Support (Reg 48)
        </div>
        <div class="drawer-item" onclick="openSingleModule('statutory-blasting-card', 'Blasting Audit')">
            <span>💥</span> Blasting & Explosives (Reg 184)
        </div>
        <div class="drawer-item" onclick="openSingleModule('statutory-inundation-card', 'Inundation Register')">
            <span>🌊</span> Inundation & Water Danger
        </div>
        <div class="drawer-item" onclick="openSingleModule('statutory-dust-card', 'Coal Dust Register')">
            <span>🌫️</span> Coal Dust & Water Spraying
        </div>
        <div class="drawer-item" onclick="openSingleModule('statutory-fire-card', 'Mine Fire Audit')">
            <span>🔥</span> Spontaneous Combustion & Fire
        </div>
        <div class="drawer-item" onclick="openSingleModule('statutory-medical-card', 'Medical PME')">
            <span>🏥</span> Initial & Periodic Medical (PME)
        </div>
        <div class="drawer-item" onclick="openSingleModule('statutory-smp-card', 'Safety Management')">
            <span>📋</span> Safety Management Plan (SMP)
        </div>

        <!-- Plant & Machinery -->
        <div class="drawer-cat-title">🚜 Machinery & Electrical</div>
        <div class="drawer-item" onclick="openSingleModule('statutory-machinery-card', 'HEMM Machinery')">
            <span>🚜</span> HEMM & Machinery Fitness
        </div>
        <div class="drawer-item" onclick="openSingleModule('statutory-haulage-card', 'Haulage Track')">
            <span>🚂</span> Haulage & Track Inspection
        </div>
        <div class="drawer-item" onclick="openSingleModule('statutory-electrical-card', 'Electrical Flameproof')">
            <span>⚡</span> Flameproof Electrical Apparatus
        </div>
        <div class="drawer-item" onclick="openSingleModule('statutory-winding-card', 'Shaft Winding')">
            <span>🏗️</span> Shaft & Winding Installation
        </div>
        <div class="drawer-item" onclick="openSingleModule('statutory-calibration-card', 'Gas Calibration')">
            <span>🎛️</span> Methanometer / Gas Calibration
        </div>

        <!-- Emergency & Compliance -->
        <div class="drawer-cat-title">🚨 Emergency & Compliance</div>
        <div class="drawer-item" onclick="openSingleModule('statutory-accident-card', 'Accident Form IV')">
            <span>⚠️</span> Accident & Occurrence (Form IV-A)
        </div>
        <div class="drawer-item" onclick="openSingleModule('statutory-rescue-card', 'Rescue Apparatus')">
            <span>🤿</span> Rescue & SCSR Apparatus
        </div>
        <div class="drawer-item" onclick="openSingleModule('statutory-simulator-card', 'Hazard Simulator')">
            <span>🎮</span> Pit Safety Hazard Simulator
        </div>
        <div class="drawer-item" onclick="openSingleModule('statutory-voice-card', 'Voice Log')">
            <span>🎙️</span> Statutory Voice Log
        </div>

    </div>
</div>

<script>
(function() {
    var torchTrack = null;
    var isTorchOn = false;

    // Universal One-Touch Emergency SOS (Broadcasts to EVERY mobile phone)
    window.triggerUniversalCollierySOS = function() {
        var proceed = confirm("🚨 चेतावनी / WARNING:\\n\\nक्या आप पूरी खदान में आपातकालीन सायरन (Colliery Evacuation Siren) बजाना चाहते हैं?\\n\\nयह सभी वर्कर्स और ऑफिसर्स के फोन में एक साथ ज़ोर-ज़ोर से सायरन बजाएगा!");
        if (!proceed) return;

        if (typeof window.triggerCollieryEvacuationSiren === 'function') {
            window.triggerCollieryEvacuationSiren('Emergency Distress SOS Triggered');
        } else if (typeof window.playDGMSSiren === 'function') {
            window.playDGMSSiren(15000);
            alert('🚨 EMERGENCY SOS ACTIVATED!');
        } else {
            alert('🚨 SOS Triggered! Evacuate workings immediately!');
        }
    };

    // 1. Drawer Open / Close Toggle
    window.toggleMineGuardDrawer = function() {
        var drawer = document.getElementById('mineguard-drawer');
        var overlay = document.getElementById('mineguard-drawer-overlay');
        if (!drawer || !overlay) return;

        if (drawer.classList.contains('open')) {
            drawer.classList.remove('open');
            overlay.style.display = 'none';
        } else {
            drawer.classList.add('open');
            overlay.style.display = 'block';
            var search = document.getElementById('drawer-search-input');
            if (search) search.value = '';
            filterDrawerItems();
        }
    };

    // 2. Open Single Module from Drawer or Dashboard (Clean Focus Mode)
    window.openSingleModule = function(cardId, titleName) {
        window.toggleMineGuardDrawer();

        var grid = document.getElementById('dashboard-quick-grid');
        if (grid) grid.style.display = 'none';

        var focusBar = document.getElementById('card-focus-bar');
        var titleEl = document.getElementById('active-card-title');
        if (focusBar) focusBar.style.display = 'flex';
        if (titleEl) titleEl.innerText = titleName || 'Module';

        var allCards = document.querySelectorAll('div[id^="statutory-"]');
        allCards.forEach(function(card) {
            if (card.id === cardId) {
                card.style.display = 'block';
                card.scrollIntoView({ behavior: 'smooth' });
            } else {
                card.style.display = 'none';
            }
        });
    };

    // 3. Return Back to Clean Dashboard Home
    window.showDashboardHome = function() {
        var grid = document.getElementById('dashboard-quick-grid');
        if (grid) grid.style.display = 'grid';

        var focusBar = document.getElementById('card-focus-bar');
        if (focusBar) focusBar.style.display = 'none';

        var allCards = document.querySelectorAll('div[id^="statutory-"]');
        allCards.forEach(function(card) {
            card.style.display = 'none';
        });
    };

    // 4. Form 6 Direct Opener
    window.openForm6ReportDirect = function() {
        if (document.getElementById('mineguard-drawer').classList.contains('open')) {
            window.toggleMineGuardDrawer();
        }
        if (typeof window.openForm6Report === 'function') {
            window.openForm6Report();
        } else {
            alert('Opening DGMS Form 6...');
        }
    };

    // 5. Drawer Search Filter
    window.filterDrawerItems = function() {
        var q = (document.getElementById('drawer-search-input').value || '').toLowerCase();
        var items = document.querySelectorAll('.drawer-item');
        items.forEach(function(item) {
            var txt = (item.innerText || '').toLowerCase();
            item.style.display = (txt.indexOf(q) !== -1) ? 'flex' : 'none';
        });
    };

    // 6. Hardware Torch Toggle
    window.toggleHardwareTorch = function() {
        var btn = document.getElementById('btn-quick-torch');
        if (!isTorchOn) {
            if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
                navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } }).then(function(stream) {
                    var track = stream.getVideoTracks()[0];
                    var cap = track.getCapabilities ? track.getCapabilities() : {};
                    if (cap.torch) {
                        track.applyConstraints({ advanced: [{ torch: true }] }).then(function() {
                            torchTrack = track;
                            isTorchOn = true;
                            if (btn) { btn.style.background = '#f59e0b'; btn.style.color = '#000'; }
                        });
                    } else {
                        alert('Device camera does not support hardware torch.');
                        track.stop();
                    }
                }).catch(function() { alert('Camera permission required for Torch.'); });
            }
        } else {
            if (torchTrack) { torchTrack.stop(); torchTrack = null; }
            isTorchOn = false;
            if (btn) { btn.style.background = '#1e293b'; btn.style.color = '#f8fafc'; }
        }
    };

    // Initial State: Hide all 28 cards on load, show only Clean Dashboard Grid
    s
