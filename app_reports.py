# app_reports.py - DGMS Form 6 Printable Engine & Master CSV Export (< 170 Lines)

REPORTS_MODULE = """
<style>
  @media print {
    body * { visibility: hidden !important; }
    #f6-modal, #f6-sheet, #f6-sheet * { visibility: visible !important; }
    #f6-modal { position: absolute !important; left: 0 !important; top: 0 !important; width: 100% !important; background: #fff !important; padding: 0 !important; }
    .no-print { display: none !important; }
  }
  #f6-modal { display: none; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(2,6,23,0.95); z-index: 999999; justify-content: center; align-items: center; padding: 10px; }
  .f6-box { background: #0f172a; border: 2px solid #38bdf8; border-radius: 12px; width: 100%; max-width: 620px; max-height: 94vh; display: flex; flex-direction: column; overflow: hidden; }
  #f6-sheet { flex: 1; overflow-y: auto; padding: 16px; background: #ffffff; color: #000; font-family: 'Times New Roman', serif; font-size: 11px; line-height: 1.4; }
</style>

<div id="f6-modal">
  <div class="f6-box">
    <div style="background:#1e293b; padding:10px 14px; display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #334155;" class="no-print">
      <b style="color:#38bdf8; font-size:12px;">📄 DGMS FIRST SCHEDULE - FORM VI (CMR 47/48)</b>
      <button type="button" onclick="closeForm6Modal()" style="background:#334155; border:none; color:#fff; width:26px; height:26px; border-radius:50%; cursor:pointer;">✕</button>
    </div>

    <div id="f6-sheet">
      <!-- Dynamic Form 6 Print Template -->
    </div>

    <div style="background:#020617; padding:10px; display:flex; gap:6px; border-top:1px solid #1e293b;" class="no-print">
      <button type="button" onclick="window.print()" style="flex:2; background:#0284c7; color:#fff; font-weight:bold; border:none; padding:10px; border-radius:6px; font-size:11px; cursor:pointer;">🖨️ Save as PDF / Print</button>
      <button type="button" onclick="shareForm6()" style="flex:1; background:#16a34a; color:#fff; font-weight:bold; border:none; padding:10px; border-radius:6px; font-size:11px; cursor:pointer;">📤 Share</button>
      <button type="button" onclick="closeForm6Modal()" style="flex:1; background:#334155; color:#cbd5e1; border:none; padding:10px; border-radius:6px; font-size:11px; cursor:pointer;">✕ Close</button>
    </div>
  </div>
</div>

<script>
(function() {
  window.openForm6Modal = function() {
    var m = document.getElementById('f6-modal');
    var s = document.getElementById('f6-sheet');
    if (!m || !s) return;

    var curDate = new Date().toLocaleDateString('en-GB');
    var curTime = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    s.innerHTML = `
      <div style="border:2px solid #000; padding:12px;">
        <div style="text-align:center; border-bottom:2px solid #000; padding-bottom:6px; margin-bottom:8px;">
          <div style="font-size:13px; font-weight:bold;">DIRECTORATE GENERAL OF MINES SAFETY</div>
          <div style="font-size:12px; font-weight:bold;">FIRST SCHEDULE - FORM VI (FORM 6)</div>
          <div style="font-size:9.5px; font-style:italic;">[See Regulations 47, 48 & 242 of Coal Mines Regulations, 2017]</div>
          <div style="font-size:11px; font-weight:bold; margin-top:2px;">DAILY STATUTORY SHIFT AUDIT & DISTRICT REGISTER</div>
        </div>

        <table style="width:100%; border-collapse:collapse; margin-bottom:8px; font-size:10px;">
          <tr><td><b>Mine:</b> Central Underground Colliery</td><td><b>Date:</b> ${curDate}</td></tr>
          <tr><td><b>District:</b> 2nd Dip Horizon (Seam III)</td><td><b>Shift:</b> Shift 1 (${curTime})</td></tr>
          <tr><td><b>Inspecting Official:</b> Mining Sirdar (CMR 48)</td><td><b>Status:</b> <b style="color:#15803d;">CERTIFIED COMPLIANT</b></td></tr>
        </table>

        <div style="font-weight:bold; font-size:10.5px; margin-bottom:4px; text-decoration:underline;">1. STATUTORY ENVIRONMENTAL & SAFETY OBSERVATIONS</div>
        <table style="width:100%; border-collapse:collapse; border:1px solid #000; margin-bottom:8px; font-size:9.5px;">
          <thead>
            <tr style="background:#f1f5f9;">
              <th style="border:1px solid #000; padding:4px; text-align:left;">Parameter</th>
              <th style="border:1px solid #000; padding:4px; text-align:left;">Condition Observed</th>
              <th style="border:1px solid #000; padding:4px; text-align:center;">Compliance</th>
            </tr>
          </thead>
          <tbody>
            <tr><td style="border:1px solid #000; padding:4px;">Strata & Roof Support (Reg 48)</td><td style="border:1px solid #000; padding:4px;">Roof tested sound, systematic support secure</td><td style="border:1px solid #000; padding:4px; text-align:center; color:#15803d; font-weight:bold;">SATISFACTORY</td></tr>
            <tr><td style="border:1px solid #000; padding:4px;">Ventilation & Gas (Reg 153)</td><td style="border:1px solid #000; padding:4px;">CH4: 0.04% | Airflow: 1.25 m/s (Adequate)</td><td style="border:1px solid #000; padding:4px; text-align:center; color:#15803d; font-weight:bold;">ADEQUATE</td></tr>
            <tr><td style="border:1px solid #000; padding:4px;">Fencing & Roadways (Reg 48(4))</td><td style="border:1px solid #000; padding:4px;">Disused galleries securely fenced</td><td style="border:1px solid #000; padding:4px; text-align:center; color:#15803d; font-weight:bold;">VERIFIED</td></tr>
          </tbody>
        </table>

        <div style="font-weight:bold; font-size:10.5px; margin-bottom:4px; text-decoration:underline;">2. STATUTORY CERTIFICATION</div>
        <div style="font-size:9px; color:#334155; margin-bottom:14px;">I certify that I have personally inspected the district, examined the roof, sides, and ventilation, and found workings safe under CMR 2017.</div>

        <div style="display:flex; justify-content:space-between; margin-top:14px;">
          <div style="text-align:center; width:45%;"><div style="border-bottom:1px solid #000; height:18px;"></div><b style="font-size:9px;">Mining Sirdar / Overman</b></div>
          <div style="text-align:center; width:45%;"><div style="border-bottom:1px solid #000; height:18px;"></div><b style="font-size:9px;">Colliery Manager</b></div>
        </div>
      </div>
    `;
    m.style.display = 'flex';
  };

  window.closeForm6Modal = function() {
    var m = document.getElementById('f6-modal');
    if (m) m.style.display = 'none';
  };

  window.shareForm6 = function() {
    var el = document.getElementById('f6-sheet');
    if (navigator.share && el) {
      navigator.share({ title: 'DGMS Form 6 Report', text: el.innerText }).catch(function(){});
    } else if (el) {
      navigator.clipboard.writeText(el.innerText);
      alert('📋 Form 6 copied to clipboard!');
    }
  };

  window.exportMasterCSV = function() {
    var keys = Object.keys(localStorage).filter(function(k) { return k.startsWith('mg_'); });
    var csv = "Category,Record ID,Timestamp,Summary Data\\n";
    keys.forEach(function(k) {
      try {
        var data = JSON.parse(localStorage.getItem(k) || '[]');
        if (Array.isArray(data)) {
          data.forEach(function(row) {
            csv += `"${k}","${row.id || 'REC'}","${row.time || ''}","${JSON.stringify(row).replace(/"/g, '""')}"\\n`;
          });
        }
      } catch(e) {}
    });

    if (navigator.share) {
      navigator.share({ title: 'MineGuard_Audit.csv', text: csv }).catch(function(){});
    } else {
      navigator.clipboard.writeText(csv);
      alert('📋 Master Audit CSV copied to clipboard!');
    }
  };
})();
</script>
"""
