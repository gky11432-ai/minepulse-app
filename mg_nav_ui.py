# mg_nav_ui.py - Minimal Siren Dashboard, Bilingual HUD & Drawer Markup (< 180 Lines)

NAV_UI_MARKUP = """
<style>
  .grid-container, main, #main-content { padding-top: 10px !important; }
  body.mode-home .mg-legacy-item, body.mode-home #card-focus-bar, body.mode-home #dynamic-module-viewport { display: none !important; }
  body.mode-home #dashboard-quick-grid { display: flex !important; }
  body.mode-focus #dashboard-quick-grid { display: none !important; }
  body.mode-focus .mg-legacy-item:not(.active-focus-target) { display: none !important; }
  body.mode-focus #card-focus-bar { display: flex !important; }
  body.mode-focus .active-focus-target, body.mode-focus #dynamic-module-viewport { display: block !important; width: 100% !important; box-sizing: border-box !important; padding: 12px !important; }

  #mineguard-navbar { position: sticky; top: 0; left: 0; width: 100%; background: #020617; border-bottom: 2px solid #1e293b; padding: 8px 12px; display: flex; justify-content: space-between; align-items: center; z-index: 99999; box-sizing: border-box; font-family: system-ui, sans-serif; }
  .hamburger-btn { background: #0f172a; border: 1px solid #38bdf8; color: #38bdf8; width: 40px; height: 40px; border-radius: 8px; font-size: 24px; display: flex; align-items: center; justify-content: center; cursor: pointer; }
  .hamburger-btn:active { background: #0284c7; color: #fff; }

  #telemetry-status-strip { background: #0f172a; border-bottom: 1px solid #1e293b; padding: 4px 12px; display: flex; justify-content: space-between; align-items: center; font-family: system-ui, sans-serif; font-size: 10px; color: #94a3b8; }
  .lang-toggle-btn { background: #1e293b; border: 1px solid #38bdf8; color: #38bdf8; font-weight: 800; padding: 4px 10px; border-radius: 14px; font-size: 11px; cursor: pointer; }

  #dashboard-quick-grid { display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 70vh; padding: 20px; box-sizing: border-box; font-family: system-ui, sans-serif; }
  @keyframes sirenPulseAnim { 0% { transform: scale(1); box-shadow: 0 0 0 0 rgba(239,68,68,0.85); } 70% { transform: scale(1.05); box-shadow: 0 0 0 24px rgba(239,68,68,0); } 100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(239,68,68,0); } }
  .main-siren-card { background: radial-gradient(circle, #7f1d1d 0%, #450a0a 100%); border: 3px solid #ef4444; border-radius: 24px; width: 100%; max-width: 320px; padding: 38px 20px; display: flex; flex-direction: column; align-items: center; text-align: center; cursor: pointer; animation: sirenPulseAnim 2s infinite ease-in-out; }
  .main-siren-card:active { transform: scale(0.96); background: #991b1b; }

  #mineguard-drawer-overlay { display: none; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(0,0,0,0.8); z-index: 999999; backdrop-filter: blur(2px); }
  #mineguard-drawer { position: fixed; top: 0; left: -320px; width: 295px; height: 100vh; background: #0f172a; border-right: 2px solid #334155; z-index: 1000000; display: flex; flex-direction: column; transition: left 0.25s ease; font-family: system-ui, sans-serif; }
  #mineguard-drawer.open { left: 0; }
  .drawer-cat-title { font-size: 10px; font-weight: 900; color: #38bdf8; text-transform: uppercase; padding: 12px 8px 4px 8px; }
  .drawer-item { display: flex; align-items: center; gap: 10px; padding: 11px 12px; margin-bottom: 4px; border-radius: 6px; background: #020617; border: 1px solid #1e293b; color: #f1f5f9; font-size: 12px; font-weight: 600; cursor: pointer; }
  .drawer-item:active { background: #0284c7; border-color: #38bdf8; }
  #card-focus-bar { display: none; background: #1e293b; border-bottom: 1px solid #334155; padding: 8px 14px; justify-content: space-between; align-items: center; font-family: system-ui, sans-serif; }
</style>

<div id="mineguard-navbar">
    <div style="display:flex; align-items:center; gap:10px;">
        <button type="button" class="hamburger-btn" onclick="toggleMineGuardDrawer()">☰</button>
        <div>
            <div style="font-size:14px; font-weight:900; color:#38bdf8;">MINEGUARD</div>
            <div id="hdr-subtext" style="font-size:8.5px; color:#94a3b8;" data-en="DGMS Safe Mining Console" data-hi="डीजीएमएस भूमिगत सुरक्षा कंसोल">डीजीएमएस भूमिगत सुरक्षा कंसोल</div>
        </div>
    </div>
    <div style="display:flex; align-items:center; gap:6px;">
        <button type="button" class="lang-toggle-btn" onclick="toggleAppLanguage()" id="app-lang-pill">🌐 English</button>
        <button type="button" id="btn-quick-torch" onclick="toggleHardwareTorch()" style="background:#1e293b; border:1px solid #334155; color:#f8fafc; padding:5px 8px; border-radius:8px; font-size:11px; cursor:pointer;">🔦 Torch</button>
    </div>
</div>

<div id="telemetry-status-strip">
    <div style="display:flex; align-items:center; gap:8px;">
        <span id="telemetry-shift-pill" style="background:#0284c7; color:#fff; font-weight:bold; padding:2px 6px; border-radius:4px; font-size:9px;">⏱️ SHIFT 1</span>
        <span id="telemetry-time" style="font-family:monospace; color:#cbd5e1;">--:--:--</span>
    </div>
    <div style="display:flex; align-items:center; gap:8px;">
        <span id="telemetry-battery">🔋 100%</span>
        <span id="telemetry-network" style="color:#fbbf24; font-weight:bold;">🟠 OFFLINE</span>
    </div>
</div>

<div id="card-focus-bar">
    <button type="button" onclick="showDashboardHome()" id="btn-back-home" style="background:#0284c7; color:#fff; font-weight:bold; border:none; padding:7px 14px; border-radius:6px; font-size:11px; cursor:pointer;" data-en="← Back to Dashboard" data-hi="← मुख्य डैशबोर्ड">← मुख्य डैशबोर्ड</button>
    <span id="active-card-title" style="font-size:11px; color:#38bdf8; font-weight:bold;">Module View</span>
</div>

<div id="dashboard-quick-grid">
    <div class="main-siren-card" onclick="triggerUniversalCollierySOS()">
        <span style="font-size:62px; line-height:1; margin-bottom:12px;">🚨</span>
        <b id="txt-siren-title" style="color:#f87171; font-size:18px;" data-en="EMERGENCY SIREN" data-hi="आपातकालीन सायरन">आपातकालीन सायरन</b>
        <span id="txt-siren-desc" style="color:#fca5a5; font-size:11px; margin-top:6px;" data-en="Touch to Sound All-Phone Evacuation" data-hi="सभी फोन में निकासी सायरन बजाएं">सभी फोन में निकासी सायरन बजाएं</span>
        <div id="txt-siren-pill" style="margin-top:16px; background:#ef4444; color:#fff; font-size:10px; font-weight:bold; padding:5px 14px; border-radius:20px;" data-en="TAP TO SOUND ALARM" data-hi="सायरन बजाने के लिए छुएं">सायरन बजाने के लिए छुएं</div>
    </div>
    <div id="txt-home-hint" style="margin-top:22px; text-align:center; color:#64748b; font-size:11px;" data-en="Touch <b>☰ (3-Pai)</b> for all 28 statutory registers" data-hi="सभी 28 वैधानिक रजिस्टर्स के लिए <b>☰ (3-पाई)</b> पर टच करें">सभी 28 वैधानिक रजिस्टर्स के लिए <b>☰ (3-पाई)</b> पर टच करें</div>
</div>

<div id="dynamic-module-viewport"></div>

<div id="mineguard-drawer-overlay" onclick="toggleMineGuardDrawer()"></div>
<div id="mineguard-drawer">
    <div style="background:#020617; padding:14px; border-bottom:1px solid #1e293b; display:flex; justify-content:space-between; align-items:center;">
        <div style="display:flex; align-items:center; gap:8px;">
            <span style="font-size:20px;">⛑️</span>
            <div>
                <div style="font-size:12px; font-weight:bold; color:#f8fafc;" data-en="STATUTORY REGISTERS" data-hi="वैधानिक रजिस्टर्स एवं ऑडिट">वैधानिक रजिस्टर्स एवं ऑडिट</div>
                <div style="font-size:9px; color:#94a3b8;">Mines Act 1952 & CMR 2017</div>
            </div>
        </div>
        <button type="button" onclick="toggleMineGuardDrawer()" style="background:transparent; border:none; color:#94a3b8; font-size:18px; cursor:pointer;">✕</button>
    </div>
    <div style="padding:10px 10px 4px 10px;">
        <input type="text" id="drawer-search-input" onkeyup="filterDrawerItems()" placeholder="🔍 खोजें / Search register..." style="width:100%; background:#020617; border:1px solid #334155; color:#fff; padding:8px; border-radius:6px; font-size:11px; box-sizing:border-box;">
    </div>
    <div style="flex:1; overflow-y:auto; padding:10px;" id="drawer-items-list">
        <div class="drawer-cat-title" style="color:#ef4444;" data-en="🚨 Emergency Actions" data-hi="🚨 आपातकालीन कार्रवाई">🚨 आपातकालीन कार्रवाई</div>
        <div class="drawer-item" onclick="triggerUniversalCollierySOS()" style="background:#450a0a; border-color:#ef4444; color:#fca5a5;">
            <span>🚨</span> <b data-en="Trigger All-Mobile Siren (SOS)" data-hi="सभी मोबाइलों में सायरन बजाएं (SOS)">सभी मोबाइलों में सायरन बजाएं (SOS)</b>
        </div>
        <div class="drawer-cat-title" data-en="📑 Reports & Downloads" data-hi="📑 रिपोर्ट एवं दस्तावेज डाउनलोड">📑 रिपोर्ट एवं दस्तावेज डाउनलोड</div>
        <div class="drawer-item" onclick="openForm6ReportDirect()"><span>📄</span> <span data-en="Form 6 (Save as PDF / Print)" data-hi="फॉर्म 6 शिफ्ट रिपोर्ट (PDF / प्रिंट)">फॉर्म 6 शिफ्ट रिपोर्ट (PDF / प्रिंट)</span></div>
        <div class="drawer-item" onclick="exportMasterCollieryCSV()"><span>💾</span> <span data-en="Master Audit (Excel/CSV Export)" data-hi="मास्टर ऑडिट रजिस्टर (Excel/CSV)">मास्टर ऑडिट रजिस्टर (Excel/CSV)</span></div>
        <div class="drawer-cat-title" data-en="📋 Shift & Personnel" data-hi="📋 शिफ्ट एवं कामगार हाजिरी">📋 शिफ्ट एवं कामगार हाजिरी</div>
        <div class="drawer-item" onclick="openUniversalModule('attendance', 'Form-B Attendance Roll')"><span>⏱️</span> <span data-en="Form B Attendance (Badge Punch)" data-hi="फॉर्म बी हाजिरी (बैज पंच)">फॉर्म बी हाजिरी (बैज पंच)</span></div>
        <div class="drawer-item" onclick="openUniversalModule('tracking', 'Personnel Radar')"><span>📍</span> <span data-en="Personnel Tracking (P2P Mesh)" data-hi="कामगार ट्रैकिंग रडार (P2P Mesh)">कामगार ट्रैकिंग रडार (P2P Mesh)</span></div>
        <div class="drawer-item" onclick="openUniversalModule('diary', 'Mining Sirdar Diary (CMR 48)')"><span>📖</span> <span data-en="Mining Sirdar Diary (CMR 48)" data-hi="माइनिंग सरदार डायरी (CMR 48)">माइनिंग सरदार डायरी (CMR 48)</span></div>
        <div class="drawer-item" onclick="openUniversalModule('lamproom', 'Lamp Room Register')"><span>💡</span> <span data-en="Lamp Room Register" data-hi="लैम्प रूम रजिस्टर">लैम्प रूम रजिस्टर</span></div>
        <div class="drawer-item" onclick="openUniversalModule('handover', 'Shift Handover Register')"><span>🤝</span> <span data-en="Shift Handover Register" data-hi="शिफ्ट हैंडओवर रजिस्टर">शिफ्ट हैंडओवर रजिस्टर</span></div>
        <div class="drawer-item" onclick="openUniversalModule('muster', 'Muster Roll (Form A)')"><span>👥</span> <span data-en="Muster Roll (Form A)" data-hi="मस्टर रोल (फॉर्म ए)">मस्टर रोल (फॉर्म ए)</span></div>
        <div class="drawer-cat-title" data-en="🛡️ Statutory Safety Audits" data-hi="🛡️ वैधानिक सुरक्षा ऑडिट">🛡️ वैधानिक सुरक्षा ऑडिट</div>
        <div class="drawer-item" onclick="openUniversalModule('ventilation', 'Ventilation & Gas Audit')"><span>💨</span> <span data-en="Ventilation & Gas (Reg 153)" data-hi="वेंटिलेशन एवं गैस ऑडिट (Reg 153)">वेंटिलेशन एवं गैस ऑडिट (Reg 153)</span></div>
        <div class="drawer-item" onclick="openUniversalModule('strata', 'Strata & Roof Support')"><span>🪨</span> <span data-en="Strata & Roof Support (Reg 48)" data-hi="रूफ सपोर्ट एवं स्ट्रेटा (Reg 48)">रूफ सपोर्ट एवं स्ट्रेटा (Reg 48)</span></div>
        <div class="drawer-item" onclick="openUniversalModule('blasting', 'Blasting & Explosives')"><span>💥</span> <span data-en="Blasting & Explosives (Reg 184)" data-hi="ब्लास्टिंग एवं विस्फोटक (Reg 184)">ब्लास्टिंग एवं विस्फोटक (Reg 184)</span></div>
        <div class="drawer-item" onclick="openUniversalModule('inundation', 'Inundation Register')"><span>🌊</span> <span data-en="Inundation & Water Danger" data-hi="जलभराव एवं खतरा रजिस्टर">जलभराव एवं खतरा रजिस्टर</span></div>
        <div class="drawer-item" onclick="openUniversalModule('dust', 'Coal Dust Register')"><span>🌫️</span> <span data-en="Coal Dust & Water Spraying" data-hi="कोयला धूल एवं छिड़काव">कोयला धूल एवं छिड़काव</span></div>
        <div class="drawer-item" onclick="openUniversalModule('fire', 'Mine Fire Register')"><span>🔥</span> <span data-en="Spontaneous Combustion & Fire" data-hi="खदान आग एवं दहन जांच">खदान आग एवं दहन जांच</span></div>
        <div class="drawer-item" onclick="openUniversalModule('medical', 'Medical Examination (PME)')"><span>🏥</span> <span data-en="Medical Examination (PME)" data-hi="कामगार मेडिकल जांच (PME)">कामगार मेडिकल जांच (PME)</span></div>
        <div class="drawer-item" onclick="openUniversalModule('smp', 'Safety Management Plan')"><span>📋</span> <span data-en="Safety Management Plan (SMP)" data-hi="सुरक्षा प्रबंधन योजना (SMP)">सुरक्षा प्रबंधन योजना (SMP)</span></div>
        <div class="drawer-cat-title" data-en="🚜 Plant & Machinery" data-hi="🚜 संयंत्र एवं मशीनरी">🚜 संयंत्र एवं मशीनरी</div>
        <div class="drawer-item" onclick="openUniversalModule('machinery', 'HEMM Machinery Fitness')"><span>🚜</span> <span data-en="HEMM & Machinery Fitness" data-hi="भारी मशीनरी फिटनेस रजिस्टर">भारी मशीनरी फिटनेस रजिस्टर</span></div>
        <div class="drawer-item" onclick="openUniversalModule('haulage', 'Haulage & Track')"><span>🚂</span> <span data-en="Haulage & Track Inspection" data-hi="हॉलेज एवं ट्रैक निरीक्षण">हॉलेज एवं ट्रैक निरीक्षण</span></div>
        <div class="drawer-item" onclick="openUniversalModule('electrical', 'Flameproof Electrical')"><span>⚡</span> <span data-en="Flameproof Electrical" data-hi="फ्लेमप्रूफ विद्युत उपकरण">फ्लेमप्रूफ विद्युत उपकरण</span></div>
        <div class="drawer-item" onclick="openUniversalModule('winding', 'Shaft & Winding')"><span>🏗️</span> <span data-en="Shaft & Winding Installation" data-hi="शाफ्ट एवं वाइंडिंग">शाफ्ट एवं वाइंडिंग</span></div>
        <div class="drawer-item" onclick="openUniversalModule('calibration', 'Gas Calibration')"><span>🎛️</span> <span data-en="Methanometer Calibration" data-hi="गैस डिटेक्टर कैलिब्रेशन">गैस डिटेक्टर कैलिब्रेशन</span></div>
        <div class="drawer-cat-title" data-en="🚨 Emergency & Compliance" data-hi="🚨 आपातकाल एवं अनुपालन">🚨 आपातकाल एवं अनुपालन</div>
        <div class="drawer-item" onclick="openUniversalModule('accident', 'Accident Register')"><span>⚠️</span> <span data-en="Accident (Form IV-A)" data-hi="दुर्घटना रजिस्टर (फॉर्म 4-ए)">दुर्घटना रजिस्टर (फॉर्म 4-ए)</span></div>
        <div class="drawer-item" onclick="openUniversalModule('rescue', 'Rescue Apparatus')"><span>🤿</span> <span data-en="Rescue & SCSR Apparatus" data-hi="बचाव उपकरण एवं SCSR">बचाव उपकरण एवं SCSR</span></div>
        <div class="drawer-item" onclick="openUniversalModule('simulator', 'Hazard Simulator')"><span>🎮</span> <span data-en="Pit Hazard Simulator" data-hi="खदान सुरक्षा सिम्युलेटर">खदान सुरक्षा सिम्युलेटर</span></div>
        <div class="drawer-item" onclick="openUniversalModule('voice', 'Voice Log')"><span>🎙️</span> <span data-en="Statutory Voice Log" data-hi="वैधानिक वॉयस लॉग">वैधानिक वॉयस लॉग</span></div>
    </div>
</div>
"""
