# ui_handover.py - Standalone DGMS Shift Handover & Manager Review Module (CMR Reg 27 & 43)

HANDOVER_MODULE = """
<script>
(function() {
    // Autonomous DOM Injector: Purani files ko chhede bina UI card inject karega
    function injectHandoverUI() {
        if (document.getElementById('shift-handover-card')) return;

        var container = document.querySelector('.grid-container') || document.body;
        
        var card = document.createElement('div');
        card.id = 'shift-handover-card';
        card.style.cssText = 'background:#0f172a; border:1px solid #334155; border-radius:10px; padding:16px; margin:14px 0; color:#f8fafc; font-family:system-ui, sans-serif; box-shadow:0 4px 6px -1px rgba(0,0,0,0.5);';
        
        card.innerHTML = `
            <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #1e293b; padding-bottom:10px; margin-bottom:12px;">
                <div style="display:flex; align-items:center; gap:8px;">
                    <span style="font-size:18px;">📋</span>
                    <div>
                        <div style="font-size:13px; font-weight:bold; color:#38bdf8;">SHIFT HANDOVER & STATUTORY REVIEW</div>
                        <div style="font-size:10px; color:#94a3b8;">DGMS CMR 2017 - Regulation 27 & 43 Compliance</div>
                    </div>
                </div>
                <span id="active-shift-badge" style="background:#1e293b; color:#38bdf8; border:1px solid #38bdf8; font-size:10px; padding:3px 8px; border-radius:12px; font-weight:bold;">1st Shift (General)</span>
            </div>

            <form id="shift-handover-form" onsubmit="saveShiftHandover(event)">
                <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap:10px; margin-bottom:10px;">
                    <div>
                        <label style="font-size:11px; color:#94a3b8;">Shift Timing</label>
                        <select id="shift-id" style="width:100%; background:#020617; border:1px solid #334155; color:#fff; padding:8px; border-radius:6px; font-size:11px; margin-top:4px;">
                            <option value="Shift 1 (08:00 - 16:00)">1st Shift (08:00 - 16:00)</option>
                            <option value="Shift 2 (16:00 - 00:00)">2nd Shift (16:00 - 00:00)</option>
                            <option value="Shift 3 (00:00 - 08:00)">3rd Shift / Night (00:00 - 08:00)</option>
                        </select>
                    </div>
                    <div>
                        <label style="font-size:11px; color:#94a3b8;">Outgoing Statutory Officer</label>
                        <input type="text" id="officer-out" required placeholder="Name & Overman Cert No." style="width:100%; background:#020617; border:1px solid #334155; color:#fff; padding:8px; border-radius:6px; font-size:11px; margin-top:4px;">
                    </div>
                    <div>
                        <label style="font-size:11px; color:#94a3b8;">Incoming Officer (Taking Charge)</label>
                        <input type="text" id="officer-in" required placeholder="Relieving Officer Name" style="width:100%; background:#020617; border:1px solid #334155; color:#fff; padding:8px; border-radius:6px; font-size:11px; margin-top:4px;">
                    </div>
                </div>

                <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap:8px; margin-bottom:10px;">
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Face Ventilation</span>
                        <select id="vent-status" style="width:100%; background:transparent; border:none; color:#4ade80; font-weight:bold; font-size:11px; margin-top:2px;">
                            <option value="Adequate (Air Velocity OK)">Adequate (Velocity OK)</option>
                            <option value="Restricted (Brattice Required)">Restricted (Brattice Req)</option>
                            <option value="Sluggish / Critical">Sluggish / Critical</option>
                        </select>
                    </div>
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Strata / Highwall</span>
                        <select id="strata-status" style="width:100%; background:transparent; border:none; color:#4ade80; font-weight:bold; font-size:11px; margin-top:2px;">
                            <option value="Stable / No Cracks">Stable / No Cracks</option>
                            <option value="Under Observation">Under Observation</option>
                            <option value="Tension Cracks Detected">Tension Cracks Detected</option>
                        </select>
                    </div>
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Gas Clearance (CH4)</span>
                        <select id="gas-clearance" style="width:100%; background:transparent; border:none; color:#4ade80; font-weight:bold; font-size:11px; margin-top:2px;">
                            <option value="Zero / Under Limit (<0.2%)">Under Limit (<0.2%)</option>
                            <option value="Elevated (0.5% - 0.8%)">Elevated (0.5% - 0.8%)</option>
                            <option value="Gas Outburst Alert">Gas Outburst Alert</option>
                        </select>
                    </div>
                </div>

                <div style="margin-bottom:10px;">
                    <label style="font-size:11px; color:#94a3b8;">Critical Handover Notes / Directives to Next Shift</label>
                    <textarea id="handover-notes" rows="2" required placeholder="Face advance status, blasting clearance, machinery downtime..." style="width:100%; background:#020617; border:1px solid #334155; color:#fff; padding:8px; border-radius:6px; font-size:11px; margin-top:4px; box-sizing:border-box;"></textarea>
                </div>

                <div style="display:flex; gap:10px; align-items:center;">
                    <button type="submit" style="flex:1; background:#0284c7; color:#fff; font-weight:bold; border:none; padding:10px; border-radius:6px; cursor:pointer; font-size:12px;">
                        ✍️ Log Shift Handover (CMR 43)
                    </button>
                    <button type="button" onclick="managerCounterSign()" style="background:#059669; color:#fff; font-weight:bold; border:none; padding:10px 14px; border-radius:6px; cursor:pointer; font-size:12px;">
                        🛡️ Manager Counter-Sign (CMR 27)
                    </button>
                </div>
            </form>

            <div style="margin-top:14px; border-top:1px solid #1e293b; padding-top:10px;">
                <div style="font-size:11px; font-weight:bold; color:#cbd5e1; margin-bottom:6px;">Latest Statutory Handover Register</div>
                <div id="handover-log-list" style="max-height:120px; overflow-y:auto; font-size:11px; color:#94a3b8;">
                    No handover recorded for current cycle.
                </div>
            </div>
        `;

        // Card ko page par render karein
        container.appendChild(card);
        renderHandoverLogs();
    }

    // Handover Save Logic (100% Offline Vault)
    window.saveShiftHandover = function(e) {
        if (e) e.preventDefault();
        var shift = document.getElementById('shift-id').value;
        var outOff = document.getElementById('officer-out').value;
        var inOff = document.getElementById('officer-in').value;
        var vent = document.getElementById('vent-status').value;
        var strata = document.getElementById('strata-status').value;
        var gas = document.getElementById('gas-clearance').value;
        var notes = document.getElementById('handover-notes').value;
        var time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        var date = new Date().toLocaleDateString();

        var seal = 'DGMS-CMR43-' + Math.random().toString(36).substring(2, 10).toUpperCase();

        var entry = {
            id: 'HO-' + Date.now(),
            shift: shift,
            date: date,
            time: time,
            outOfficer: outOff,
            inOfficer: inOff,
            ventilation: vent,
            strata: strata,
            gas: gas,
            notes: notes,
            seal: seal,
            managerSigned: false
        };

        var logs = JSON.parse(localStorage.getItem('dgms_handovers') || '[]');
        logs.unshift(entry);
        localStorage.setItem('dgms_handovers', JSON.stringify(logs));

        document.getElementById('handover-notes').value = '';
        renderHandoverLogs();
        alert('✅ Shift Handover Logged Successfully! Relieving officer in charge.');
    };

    // Colliery Manager Counter-Signature
    window.managerCounterSign = function() {
        var logs = JSON.parse(localStorage.getItem('dgms_handovers') || '[]');
        if (logs.length === 0) {
            alert('Koi handover log record nahi hai. Pehle shift handover bharein.');
            return;
        }

        var mgrName = prompt("Colliery Manager / Agent Name:", "Er. R. K. Sharma (First Class Mgr No. 1104)");
        if (!mgrName) return;

        logs[0].managerSigned = true;
        logs[0].managerName = mgrName;
        logs[0].managerSeal = 'MGR-SEAL-CMR27-' + Math.random().toString(36).substring(2, 8).toUpperCase();
        logs[0].signedAt = new Date().toLocaleTimeString();

        localStorage.setItem('dgms_handovers', JSON.stringify(logs));
        renderHandoverLogs();
        alert('🛡️ Statutory CMR 27 Countersignature Applied by ' + mgrName);
    };

    // Render Handover Log History
    function renderHandoverLogs() {
        var list = document.getElementById('handover-log-list');
        if (!list) return;
        var logs = JSON.parse(localStorage.getItem('dgms_handovers') || '[]');

        if (logs.length === 0) {
            list.innerHTML = '<div style="color:#64748b; padding:4px;">No handover recorded for current cycle.</div>';
            return;
        }

        list.innerHTML = logs.map(function(item) {
            var mgrStatus = item.managerSigned 
                ? '<span style="color:#34d399;">✓ Countersigned by ' + item.managerName + ' (' + item.managerSeal + ')</span>'
                : '<span style="color:#f59e0b;">⏳ Pending Manager Countersignature (CMR 27)</span>';

            return `
                <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px; margin-bottom:6px;">
                    <div style="display:flex; justify-content:space-between; font-weight:bold; color:#38bdf8;">
                        <span>${item.shift} - ${item.date} ${item.time}</span>
                        <span style="font-family:monospace; font-size:9px; color:#f59e0b;">${item.seal}</span>
                    </div>
                    <div style="color:#cbd5e1; margin:3px 0;">
                        <b>Handover:</b> ${item.outOfficer} ➔ <b>Relieved by:</b> ${item.inOfficer}
                    </div>
                    <div style="color:#94a3b8; font-size:10px;">
                        <b>Vent:</b> ${item.ventilation} | <b>Strata:</b> ${item.strata} | <b>Gas:</b> ${item.gas}
                    </div>
                    <div style="color:#e2e8f0; font-size:10px; margin-top:2px;"><b>Notes:</b> ${item.notes}</div>
                    <div style="font-size:10px; margin-top:4px; border-top:1px dashed #1e293b; padding-top:3px;">${mgrStatus}</div>
                </div>
            `;
        }).join('');
    }

    // Auto-mount on load
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', injectHandoverUI);
    } else {
        injectHandoverUI();
    }
    setTimeout(injectHandoverUI, 1200);
})();
</script>
"""
