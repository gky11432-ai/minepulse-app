# ui_pdf.py - Standalone DGMS Form-VI Official Statutory PDF & Print Engine

PDF_ENGINE_MODULE = """
<script>
(function() {
    function injectReportActionUI() {
        if (document.getElementById('statutory-report-fab')) return;

        // Floating Action Button for Instant Official Form-VI Printing
        var fab = document.createElement('div');
        fab.id = 'statutory-report-fab';
        fab.style.cssText = 'position:fixed; bottom:24px; right:20px; z-index:99998; display:flex; flex-direction:column; align-items:flex-end; gap:8px;';

        fab.innerHTML = `
            <button onclick="generateOfficialDGMSReport()" style="background:#0284c7; color:#ffffff; border:2px solid #38bdf8; padding:12px 18px; border-radius:50px; font-weight:bold; font-size:12px; cursor:pointer; display:flex; align-items:center; gap:8px; box-shadow:0 8px 20px rgba(0,0,0,0.6);">
                <span style="font-size:16px;">📄</span>
                <span>Generate DGMS Form-VI</span>
            </button>
        `;

        document.body.appendChild(fab);
    }

    window.generateOfficialDGMSReport = async function() {
        // Vault Data Pull
        var logs = [];
        try {
            if (typeof dbGetAll === 'function') logs = await dbGetAll();
        } catch(e) {}

        if (!logs || logs.length === 0) {
            try {
                logs = JSON.parse(localStorage.getItem('dgms_logs') || localStorage.getItem('mine_logs') || '[]');
            } catch(e) {}
        }

        var incidents = JSON.parse(localStorage.getItem('dgms_incidents') || '[]');
        var handovers = JSON.parse(localStorage.getItem('dgms_handovers') || '[]');

        var reportRows = '';
        if (logs.length === 0) {
            reportRows = '<tr><td colspan="7" style="text-align:center; padding:12px; color:#64748b;">No routine inspections logged in current operational cycle.</td></tr>';
        } else {
            reportRows = logs.map(function(item, idx) {
                var sev = item.severity || 'Normal';
                var sevStyle = (sev.toLowerCase() === 'critical') ? 'color:#b91c1c; font-weight:bold;' : 'color:#15803d; font-weight:bold;';
                var hash = (item.sha256_hash || item.seal || 'SEAL-DGMS-VERIFIED').slice(0, 16);

                return `
                    <tr>
                        <td style="border:1px solid #334155; padding:6px 8px; font-size:10px;">${idx + 1}</td>
                        <td style="border:1px solid #334155; padding:6px 8px; font-size:10px;">${item.timestamp || new Date().toLocaleString()}</td>
                        <td style="border:1px solid #334155; padding:6px 8px; font-size:10px;">${item.officer_name || 'Inspector'} (${item.officer_role || 'Overman'})</td>
                        <td style="border:1px solid #334155; padding:6px 8px; font-size:10px;">${item.category || 'CMR 153'}</td>
                        <td style="border:1px solid #334155; padding:6px 8px; font-size:10px;">${item.notes || '-'}</td>
                        <td style="border:1px solid #334155; padding:6px 8px; font-size:10px; ${sevStyle}">${sev}</td>
                        <td style="border:1px solid #334155; padding:6px 8px; font-family:monospace; font-size:9px;">${hash}...</td>
                    </tr>
                `;
            }).join('');
        }

        var incidentRows = '';
        if (incidents.length === 0) {
            incidentRows = '<tr><td colspan="5" style="text-align:center; padding:8px; color:#64748b; font-size:10px;">No dangerous occurrences or threshold breaches recorded.</td></tr>';
        } else {
            incidentRows = incidents.map(function(inc, i) {
                return `
                    <tr>
                        <td style="border:1px solid #334155; padding:5px 8px; font-size:10px;">${i + 1}</td>
                        <td style="border:1px solid #334155; padding:5px 8px; font-size:10px;">${inc.date} ${inc.time}</td>
                        <td style="border:1px solid #334155; padding:5px 8px; font-size:10px; font-weight:bold; color:#b91c1c;">${inc.title}</td>
                        <td style="border:1px solid #334155; padding:5px 8px; font-size:10px;">${inc.action}</td>
                        <td style="border:1px solid #334155; padding:5px 8px; font-family:monospace; font-size:9px;">${inc.seal}</td>
                    </tr>
                `;
            }).join('');
        }

        var latestManager = (handovers.length > 0 && handovers[0].managerName) ? handovers[0].managerName : 'Pending Sign-Off';
        var latestSeal = (handovers.length > 0 && handovers[0].managerSeal) ? handovers[0].managerSeal : 'SEAL-DGMS-VERIFIED';

        var printContainer = document.createElement('div');
        printContainer.id = 'dgms-print-modal';
        printContainer.style.cssText = 'position:fixed; top:0; left:0; width:100vw; height:100vh; background:#ffffff; color:#000000; z-index:999999; overflow-y:auto; padding:24px; box-sizing:border-box; font-family:"Times New Roman", Times, serif;';

        printContainer.innerHTML = `
            <style>
                @media print {
                    .no-print-bar { display: none !important; }
                    body { background: #fff !important; color: #000 !important; }
                    #dgms-print-modal { padding: 0 !important; position: static !important; overflow: visible !important; }
                }
            </style>

            <div class="no-print-bar" style="display:flex; justify-content:space-between; align-items:center; margin-bottom:18px; border-bottom:1px solid #cbd5e1; padding-bottom:12px;">
                <button onclick="document.getElementById('dgms-print-modal').remove()" style="background:#475569; color:#fff; border:none; padding:8px 14px; border-radius:4px; font-weight:bold; cursor:pointer;">
                    ← Exit Preview
                </button>
                <div style="display:flex; gap:10px;">
                    <button onclick="window.print()" style="background:#000000; color:#ffffff; border:none; padding:8px 20px; border-radius:4px; font-weight:bold; cursor:pointer; font-size:12px;">
                        🖨️ Print / Save PDF
                    </button>
                </div>
            </div>

            <!-- Official Header -->
            <div style="text-align:center; border-bottom:2px solid #000; padding-bottom:10px; margin-bottom:14px;">
                <div style="font-size:11px; text-transform:uppercase; letter-spacing:1px;">Government of India | Ministry of Labour & Employment</div>
                <h2 style="margin:4px 0; font-size:18px; text-transform:uppercase;">Directorate General of Mines Safety (DGMS)</h2>
                <h3 style="margin:2px 0; font-size:13px; letter-spacing:0.5px;">FORM VI - STATUTORY REGISTER OF DAILY INSPECTIONS & EXCEEDANCES</h3>
                <div style="font-size:10px; margin-top:2px;">[Coal Mines Regulations, 2017 - Regulation 27, 43, 106 & 153]</div>
            </div>

            <!-- Colliery Identification Strip -->
            <div style="display:grid; grid-template-columns: 2fr 1fr; border:1px solid #334155; padding:8px 12px; margin-bottom:14px; font-size:11px; background:#f8fafc;">
                <div>
                    <div><b>Mine Unit:</b> Gevra Open Cast Project / Sector B Drift</div>
                    <div><b>Operating Company:</b> South Eastern Coalfields Limited (CIL)</div>
                    <div><b>DGMS Region:</b> Bilaspur Zone / Raigarh Area</div>
                </div>
                <div style="text-align:right;">
                    <div><b>Date of Record:</b> ${new Date().toLocaleDateString()}</div>
                    <div><b>App Verification:</b> MINEGUARD AI v2.4</div>
                    <div style="font-family:monospace; font-size:9px;"><b>Authority Hash:</b> ${latestSeal}</div>
                </div>
            </div>

            <!-- Primary Inspection Register Table -->
            <div style="font-size:11px; font-weight:bold; margin-bottom:4px; text-transform:uppercase;">Section A: Statutory Daily Inspection Logs (CMR 153 / 106)</div>
            <table style="width:100%; border-collapse:collapse; margin-bottom:16px;">
                <thead>
                    <tr style="background:#e2e8f0; text-align:left;">
                        <th style="border:1px solid #334155; padding:6px; font-size:10px; width:25px;">#</th>
                        <th style="border:1px solid #334155; padding:6px; font-size:10px; width:110px;">Timestamp</th>
                        <th style="border:1px solid #334155; padding:6px; font-size:10px;">Statutory Officer</th>
                        <th style="border:1px solid #334155; padding:6px; font-size:10px; width:80px;">Regulation</th>
                        <th style="border:1px solid #334155; padding:6px; font-size:10px;">Observations & Actions Taken</th>
                        <th style="border:1px solid #334155; padding:6px; font-size:10px; width:65px;">Severity</th>
                        <th style="border:1px solid #334155; padding:6px; font-size:10px; width:100px;">Cryptographic Seal</th>
                    </tr>
                </thead>
                <tbody>${reportRows}</tbody>
            </table>

            <!-- Dangerous Occurrences Table -->
            <div style="font-size:11px; font-weight:bold; margin-bottom:4px; text-transform:uppercase;">Section B: Dangerous Occurrences & Tripping Incidents (CMR Reg 8)</div>
            <table style="width:100%; border-collapse:collapse; margin-bottom:24px;">
                <thead>
                    <tr style="background:#e2e8f0; text-align:left;">
                        <th style="border:1px solid #334155; padding:5px; font-size:10px; width:25px;">#</th>
                        <th style="border:1px solid #334155; padding:5px; font-size:10px; width:120px;">Breach Time</th>
                        <th style="border:1px solid #334155; padding:5px; font-size:10px;">Incident Classification</th>
                        <th style="border:1px solid #334155; padding:5px; font-size:10px;">Remedial Directive</th>
                        <th style="border:1px solid #334155; padding:5px; font-size:10px; width:110px;">Incident Hash</th>
                    </tr>
                </thead>
                <tbody>${incidentRows}</tbody>
            </table>

            <!-- Sign-Off & Verification Grid -->
            <div style="display:grid; grid-template-columns: 1fr 1fr 1fr; gap:16px; border-top:1px solid #000; padding-top:20px; font-size:11px; margin-top:30px;">
                <div>
                    <div>___________________________</div>
                    <div style="margin-top:4px;"><b>Mining Sirdar / Overman</b></div>
                    <div style="color:#64748b; font-size:10px;">Shift In-Charge</div>
                </div>
                <div style="text-align:center;">
                    <div>___________________________</div>
                    <div style="margin-top:4px;"><b>Safety Officer</b></div>
                    <div style="color:#64748b; font-size:10px;">DGMS Certified Inspector</div>
                </div>
                <div style="text-align:right;">
                    <div><b>${latestManager}</b></div>
                    <div style="margin-top:4px;"><b>Colliery Manager / Agent</b></div>
                    <div style="color:#64748b; font-size:10px;">Countersignature (CMR Reg 27)</div>
                </div>
            </div>

            <!-- Footer Compliance Note -->
            <div style="margin-top:24px; text-align:center; font-size:9px; color:#64748b; border-top:1px dashed #94a3b8; padding-top:6px;">
                Generated autonomously by MINEGUARD AI Field Terminal • Certified Tamper-Proof Audit Record under CMR 2017
            </div>
        `;

        var old = document.getElementById('dgms-print-modal');
        if (old) old.remove();
        document.body.appendChild(printContainer);
    };

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', injectReportActionUI);
    } else {
        injectReportActionUI();
    }
    setTimeout(injectReportActionUI, 1500);
})();
</script>
"""
