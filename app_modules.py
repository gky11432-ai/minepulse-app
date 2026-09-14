# app_modules.py - Focus Viewport, Form Generator & History Ledger (< 180 Lines)

MODULES_ENGINE = """
<div id="view-module">
  <!-- Dynamic Form and Ledger Viewport Injected Here -->
</div>

<script>
(function() {
  window.openModule = function(key, title) {
    var vHome = document.getElementById('view-home');
    var vMod = document.getElementById('view-module');
    var bBack = document.getElementById('bar-back');
    var tMod = document.getElementById('txt-active-module');

    if (vHome) vHome.style.display = 'none';
    if (vMod) { vMod.style.display = 'block'; vMod.innerHTML = renderModuleForm(key, title); }
    if (bBack) bBack.style.display = 'flex';
    if (tMod) tMod.innerText = title;

    window.toggleAppDrawer();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  window.navigateHome = function() {
    var vHome = document.getElementById('view-home');
    var vMod = document.getElementById('view-module');
    var bBack = document.getElementById('bar-back');

    if (vMod) { vMod.style.display = 'none'; vMod.innerHTML = ''; }
    if (bBack) bBack.style.display = 'none';
    if (vHome) vHome.style.display = 'flex';
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  function renderModuleForm(key, title) {
    var storeKey = 'mg_' + key + '_logs';
    var logs = JSON.parse(localStorage.getItem(storeKey) || '[]');
    var rows = '';

    if (logs.length === 0) {
      rows = '<tr><td colspan="4" style="text-align:center; padding:10px; color:#64748b;">No statutory records logged yet.</td></tr>';
    } else {
      logs.slice(0, 5).forEach(function(l) {
        rows += '<tr><td style="border:1px solid #334155; padding:6px;">' + l.time + '</td><td style="border:1px solid #334155; padding:6px;">' + l.officer + '</td><td style="border:1px solid #334155; padding:6px; color:#34d399;">' + l.status + '</td><td style="border:1px solid #334155; padding:6px;">' + l.remarks + '</td></tr>';
      });
    }

    var isHi = (localStorage.getItem('mg_lang') || 'HI') === 'HI';

    return `
      <div style="background:#0f172a; border:1px solid #334155; border-radius:12px; padding:16px; font-family:system-ui, sans-serif; color:#f8fafc; max-width:600px; margin:0 auto; box-shadow:0 10px 25px rgba(0,0,0,0.8);">
        <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #1e293b; padding-bottom:8px; margin-bottom:12px;">
          <div><b style="color:#38bdf8; font-size:14px;">${title}</b><div style="font-size:10px; color:#94a3b8;">DGMS Statutory Register (CMR 2017)</div></div>
          <span style="background:#0369a1; color:#fff; font-size:9px; padding:2px 8px; border-radius:4px; font-weight:bold;">OFFLINE SECURE</span>
        </div>

        <form onsubmit="saveModuleRecord(event, '${storeKey}', '${title}')" style="display:flex; flex-direction:column; gap:10px;">
          <div>
            <label style="font-size:11px; color:#94a3b8;">${isHi ? 'स्थान / सीम (Location / Seam)' : 'District / Working Seam'}</label>
            <input type="text" id="inp-loc" required placeholder="e.g. 2nd Dip Gallery / District 3" style="width:100%; background:#020617; border:1px solid #334155; color:#fff; padding:8px; border-radius:6px; font-size:11px; box-sizing:border-box; margin-top:4px;">
          </div>
          <div>
            <label style="font-size:11px; color:#94a3b8;">${isHi ? 'सुरक्षा निरीक्षण / टेस्ट रीडिंग (Observation)' : 'Observation / Test Reading'}</label>
            <input type="text" id="inp-obs" required placeholder="e.g. Roof tested sound, ventilation verified" style="width:100%; background:#020617; border:1px solid #334155; color:#fff; padding:8px; border-radius:6px; font-size:11px; box-sizing:border-box; margin-top:4px;">
          </div>
          <div>
            <label style="font-size:11px; color:#94a3b8;">${isHi ? 'अनुपालन स्थिति (Status)' : 'Compliance Status'}</label>
            <select id="inp-stat" style="width:100%; background:#020617; border:1px solid #334155; color:#fff; padding:8px; border-radius:6px; font-size:11px; box-sizing:border-box; margin-top:4px;">
              <option value="SATISFACTORY">✅ Satisfactory & Compliant</option>
              <option value="ATTENTION">⚠️ Attention Needed</option>
              <option value="DANGER_STOP">⛔ Unsafe - Work Stopped</option>
            </select>
          </div>
          <button type="submit" style="background:#0284c7; color:#fff; font-weight:bold; border:none; padding:10px; border-radius:6px; font-size:12px; cursor:pointer; margin-top:6px;">
            📝 ${isHi ? 'प्रमाणित करें एवं सील लगाएं' : 'Sign & Certify Statutory Entry'}
          </button>
        </form>

        <div style="margin-top:16px;">
          <b style="font-size:11px; color:#cbd5e1;">${isHi ? 'प्रमाणित रिकॉर्ड लेजर (History)' : 'Certified History Ledger'}</b>
          <table style="width:100%; border-collapse:collapse; font-size:10px; margin-top:6px; text-align:left;">
            <thead><tr style="background:#1e293b; color:#94a3b8;"><th style="border:1px solid #334155; padding:6px;">Time</th><th style="border:1px solid #334155; padding:6px;">Officer</th><th style="border:1px solid #334155; padding:6px;">Status</th><th style="border:1px solid #334155; padding:6px;">Remarks</th></tr></thead>
            <tbody>${rows}</tbody>
          </table>
        </div>
      </div>
    `;
  }

  window.saveModuleRecord = function(e, storeKey, title) {
    e.preventDefault();
    var entry = {
      id: 'REG-' + Date.now(),
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      officer: 'Mining Sirdar / Overman',
      location: document.getElementById('inp-loc').value,
      remarks: document.getElementById('inp-obs').value,
      status: document.getElementById('inp-stat').value
    };

    var logs = JSON.parse(localStorage.getItem(storeKey) || '[]');
    logs.unshift(entry);
    localStorage.setItem(storeKey, JSON.stringify(logs));

    alert('✅ Statutory entry certified & sealed successfully.');
    document.getElementById('view-module').innerHTML = renderModuleForm(storeKey.replace('mg_', '').replace('_logs', ''), title);
  };
})();
</script>
"""
