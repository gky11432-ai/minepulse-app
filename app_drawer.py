# app_drawer.py - 3-Pai Categorized Drawer & Instant Search Engine (< 180 Lines)

DRAWER_MODULE = """
<div id="drawer-overlay" onclick="toggleAppDrawer()"></div>
<div id="drawer-menu">
  <div style="background:#020617; padding:14px; border-bottom:1px solid #1e293b; display:flex; justify-content:space-between; align-items:center;">
    <div style="display:flex; align-items:center; gap:8px;">
      <span style="font-size:22px;">⛑️</span>
      <div>
        <div style="font-size:12px; font-weight:bold; color:#f8fafc;" data-en="STATUTORY REGISTERS" data-hi="वैधानिक रजिस्टर्स (CMR 2017)">वैधानिक रजिस्टर्स (CMR 2017)</div>
        <div style="font-size:9px; color:#94a3b8;">DGMS Compliance Ledger</div>
      </div>
    </div>
    <button type="button" onclick="toggleAppDrawer()" style="background:transparent; border:none; color:#94a3b8; font-size:20px; cursor:pointer;">✕</button>
  </div>

  <div style="padding:10px 10px 4px 10px;">
    <input type="text" id="inp-drawer-search" onkeyup="filterDrawer()" placeholder="🔍 खोजें / Search register..." style="width:100%; background:#020617; border:1px solid #334155; color:#fff; padding:8px 10px; border-radius:6px; font-size:11px; outline:none;">
  </div>

  <div style="flex:1; overflow-y:auto; padding:10px;" id="drawer-list">
    <!-- 1. Emergency SOS -->
    <div style="font-size:10px; font-weight:900; color:#ef4444; text-transform:uppercase; padding:10px 6px 4px 6px;" data-en="🚨 Emergency" data-hi="🚨 आपातकालीन कार्रवाई">🚨 आपातकालीन कार्रवाई</div>
    <div class="drawer-item" onclick="triggerUniversalSiren(); toggleAppDrawer();" style="background:#450a0a; border-color:#ef4444; color:#fca5a5;">
      <span>🚨</span> <b data-en="Sound All-Mobile Siren" data-hi="सभी मोबाइलों में सायरन बजाएं">सभी मोबाइलों में सायरन बजाएं</b>
    </div>

    <!-- 2. Reports & Audits -->
    <div style="font-size:10px; font-weight:900; color:#38bdf8; text-transform:uppercase; padding:12px 6px 4px 6px;" data-en="📑 Reports & PDF" data-hi="📑 रिपोर्ट एवं दस्तावेज">📑 रिपोर्ट एवं दस्तावेज</div>
    <div class="drawer-item" onclick="openForm6Modal(); toggleAppDrawer();"><span>📄</span> <span data-en="Form 6 Shift Audit (PDF)" data-hi="फॉर्म 6 शिफ्ट रिपोर्ट (PDF)">फॉर्म 6 शिफ्ट रिपोर्ट (PDF)</span></div>
    <div class="drawer-item" onclick="exportMasterCSV(); toggleAppDrawer();"><span>💾</span> <span data-en="Master Audit (Excel/CSV)" data-hi="मास्टर ऑडिट रजिस्टर (Excel/CSV)">मास्टर ऑडिट रजिस्टर (Excel/CSV)</span></div>

    <!-- 3. Shift & Personnel -->
    <div style="font-size:10px; font-weight:900; color:#38bdf8; text-transform:uppercase; padding:12px 6px 4px 6px;" data-en="📋 Shift & Attendance" data-hi="📋 शिफ्ट एवं हाजिरी">📋 शिफ्ट एवं हाजिरी</div>
    <div class="drawer-item" onclick="openModule('attendance', 'Form B Attendance')"><span>⏱️</span> <span data-en="Form B Attendance (Punch)" data-hi="फॉर्म बी हाजिरी रजिस्टर">फॉर्म बी हाजिरी रजिस्टर</span></div>
    <div class="drawer-item" onclick="openModule('tracking', 'Personnel Radar')"><span>📍</span> <span data-en="Personnel Tracking (Radar)" data-hi="कामगार ट्रैकिंग रडार">कामगार ट्रैकिंग रडार</span></div>
    <div class="drawer-item" onclick="openModule('diary', 'Sirdar Shift Diary')"><span>📖</span> <span data-en="Mining Sirdar Diary (CMR 48)" data-hi="माइनिंग सरदार डायरी (CMR 48)">माइनिंग सरदार डायरी (CMR 48)</span></div>
    <div class="drawer-item" onclick="openModule('lamproom', 'Lamp Room Register')"><span>💡</span> <span data-en="Lamp Room Register" data-hi="लैम्प रूम रजिस्टर">लैम्प रूम रजिस्टर</span></div>
    <div class="drawer-item" onclick="openModule('handover', 'Shift Handover')"><span>🤝</span> <span data-en="Shift Handover Register" data-hi="शिफ्ट हैंडओवर रजिस्टर">शिफ्ट हैंडओवर रजिस्टर</span></div>
    <div class="drawer-item" onclick="openModule('muster', 'Muster Roll (Form A)')"><span>👥</span> <span data-en="Muster Roll (Form A)" data-hi="मस्टर रोल (फॉर्म ए)">मस्टर रोल (फॉर्म ए)</span></div>

    <!-- 4. Safety Audits -->
    <div style="font-size:10px; font-weight:900; color:#38bdf8; text-transform:uppercase; padding:12px 6px 4px 6px;" data-en="🛡️ Statutory Safety" data-hi="🛡️ वैधानिक सुरक्षा ऑडिट">🛡️ वैधानिक सुरक्षा ऑडिट</div>
    <div class="drawer-item" onclick="openModule('ventilation', 'Ventilation & Gas')"><span>💨</span> <span data-en="Ventilation & Gas (Reg 153)" data-hi="वेंटिलेशन एवं गैस (Reg 153)">वेंटिलेशन एवं गैस (Reg 153)</span></div>
    <div class="drawer-item" onclick="openModule('strata', 'Strata & Support')"><span>🪨</span> <span data-en="Strata & Roof Support (Reg 48)" data-hi="रूफ सपोर्ट एवं स्ट्रेटा (Reg 48)">रूफ सपोर्ट एवं स्ट्रेटा (Reg 48)</span></div>
    <div class="drawer-item" onclick="openModule('blasting', 'Blasting Register')"><span>💥</span> <span data-en="Blasting & Explosives (Reg 184)" data-hi="ब्लास्टिंग एवं विस्फोटक">ब्लास्टिंग एवं विस्फोटक</span></div>
    <div class="drawer-item" onclick="openModule('inundation', 'Water Danger')"><span>🌊</span> <span data-en="Inundation & Water Danger" data-hi="जलभराव एवं खतरा रजिस्टर">जलभराव एवं खतरा रजिस्टर</span></div>
    <div class="drawer-item" onclick="openModule('dust', 'Coal Dust Register')"><span>🌫️</span> <span data-en="Coal Dust & Water Spraying" data-hi="कोयला धूल एवं छिड़काव">कोयला धूल एवं छिड़काव</span></div>
    <div class="drawer-item" onclick="openModule('fire', 'Mine Fire Inspection')"><span>🔥</span> <span data-en="Spontaneous Fire Register" data-hi="खदान आग एवं दहन जांच">खदान आग एवं दहन जांच</span></div>
    <div class="drawer-item" onclick="openModule('medical', 'Medical PME')"><span>🏥</span> <span data-en="Worker Medical (PME/IME)" data-hi="कामगार मेडिकल जांच (PME)">कामगार मेडिकल जांच (PME)</span></div>
    <div class="drawer-item" onclick="openModule('smp', 'Safety Management')"><span>📋</span> <span data-en="Safety Management Plan (SMP)" data-hi="सुरक्षा प्रबंधन योजना (SMP)">सुरक्षा प्रबंधन योजना (SMP)</span></div>

    <!-- 5. Machinery & Plant -->
    <div style="font-size:10px; font-weight:900; color:#38bdf8; text-transform:uppercase; padding:12px 6px 4px 6px;" data-en="🚜 Plant & Machinery" data-hi="🚜 संयंत्र एवं मशीनरी">🚜 संयंत्र एवं मशीनरी</div>
    <div class="drawer-item" onclick="openModule('machinery', 'HEMM Fitness')"><span>🚜</span> <span data-en="HEMM Machinery Fitness" data-hi="भारी मशीनरी फिटनेस रजिस्टर">भारी मशीनरी फिटनेस रजिस्टर</span></div>
    <div class="drawer-item" onclick="openModule('haulage', 'Haulage Track')"><span>🚂</span> <span data-en="Haulage & Track Inspection" data-hi="हॉलेज एवं ट्रैक निरीक्षण">हॉलेज एवं ट्रैक निरीक्षण</span></div>
    <div class="drawer-item" onclick="openModule('electrical', 'Flameproof Equipment')"><span>⚡</span> <span data-en="Flameproof Electrical" data-hi="फ्लेमप्रूफ विद्युत उपकरण">फ्लेमप्रूफ विद्युत उपकरण</span></div>
    <div class="drawer-item" onclick="openModule('winding', 'Shaft & Winding')"><span>🏗️</span> <span data-en="Shaft Winding Installation" data-hi="शाफ्ट एवं वाइंडिंग">शाफ्ट एवं वाइंडिंग</span></div>
    <div class="drawer-item" onclick="openModule('calibration', 'Gas Calibration')"><span>🎛️</span> <span data-en="Methanometer Calibration" data-hi="गैस डिटेक्टर कैलिब्रेशन">गैस डिटेक्टर कैलिब्रेशन</span></div>

    <!-- 6. Emergency & Response -->
    <div style="font-size:10px; font-weight:900; color:#38bdf8; text-transform:uppercase; padding:12px 6px 4px 6px;" data-en="🚨 Emergency Response" data-hi="🚨 आपातकालीन तंत्र">🚨 आपातकालीन तंत्र</div>
    <div class="drawer-item" onclick="openModule('accident', 'Accident (Form IV-A)')"><span>⚠️</span> <span data-en="Accident (Form IV-A)" data-hi="दुर्घटना रजिस्टर (फॉर्म 4-ए)">दुर्घटना रजिस्टर (फॉर्म 4-ए)</span></div>
    <div class="drawer-item" onclick="openModule('rescue', 'Rescue & SCSR')"><span>🤿</span> <span data-en="Rescue Apparatus & SCSR" data-hi="बचाव उपकरण एवं SCSR">बचाव उपकरण एवं SCSR</span></div>
    <div class="drawer-item" onclick="openModule('simulator', 'Hazard Simulator')"><span>🎮</span> <span data-en="Pit Safety Simulator" data-hi="खदान सुरक्षा सिम्युलेटर">खदान सुरक्षा सिम्युलेटर</span></div>
    <div class="drawer-item" onclick="openModule('voice', 'Statutory Voice Log')"><span>🎙️</span> <span data-en="Statutory Voice Log" data-hi="वैधानिक वॉयस लॉग">वैधानिक वॉयस लॉग</span></div>
  </div>
</div>

<script>
(function() {
  window.toggleAppDrawer = function() {
    var d = document.getElementById('drawer-menu');
    var o = document.getElementById('drawer-overlay');
    if (!d || !o) return;
    var open = d.classList.contains('open');
    d.classList.toggle('open', !open);
    o.style.display = !open ? 'block' : 'none';
    if (!open) {
      var s = document.getElementById('inp-drawer-search');
      if (s) { s.value = ''; filterDrawer(); }
    }
  };

  window.filterDrawer = function() {
    var q = (document.getElementById('inp-drawer-search').value || '').toLowerCase();
    document.querySelectorAll('#drawer-list .drawer-item').forEach(function(item) {
      item.style.display = (item.innerText || '').toLowerCase().indexOf(q) !== -1 ? 'flex' : 'none';
    });
  };
})();
</script>
"""
