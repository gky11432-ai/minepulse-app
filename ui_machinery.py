# ui_machinery.py - Standalone DGMS CMR 83 & 84 HEMM & Mobile Machinery Pre-Shift Fitness Engine

MACHINERY_MODULE = """
<script>
(function() {
    function injectMachineryUI() {
        if (document.getElementById('statutory-machinery-card')) return;

        var container = document.querySelector('.grid-container') || document.body;

        var card = document.createElement('div');
        card.id = 'statutory-machinery-card';
        card.style.cssText = 'background:#0f172a; border:1px solid #334155; border-radius:10px; padding:16px; margin:14px 0; color:#f8fafc; font-family:system-ui, sans-serif; box-shadow:0 4px 6px -1px rgba(0,0,0,0.5);';

        card.innerHTML = `
            <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #1e293b; padding-bottom:10px; margin-bottom:12px;">
                <div style="display:flex; align-items:center; gap:8px;">
                    <span style="font-size:18px;">🚜</span>
                    <div>
                        <div style="font-size:13px; font-weight:bold; color:#f59e0b;">HEMM & PIT MACHINERY FITNESS REGISTER</div>
                        <div style="font-size:10px; color:#94a3b8;">DGMS CMR 2017 Reg 83 & 84 - Pre-Shift Brake, AVLA & AFDSS Safety Audit</div>
                    </div>
                </div>
                <div id="machinery-safety-badge" style="background:#14532d; color:#4ade80; border:1px solid #22c55e; font-size:10px; padding:3px 8px; border-radius:12px; font-weight:bold;">
                    ✓ FLEET PIT-FIT (NORMAL)
                </div>
            </div>

            <!-- Pre-Shift Equipment Inspection Form -->
            <form id="machinery-inspection-form" onsubmit="recordMachineryAudit(event)">
                <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap:10px; margin-bottom:10px;">
                    <div>
                        <label style="font-size:11px; color:#94a3b8;">Equipment Category & Unit No.</label>
                        <select id="equip-id" style="width:100%; background:#020617; border:1px solid #334155; color:#fff; padding:8px; border-radius:6px; font-size:11px; margin-top:4px;">
                            <option value="Dumper CAT-777D (Fleet No. D-104)">Dumper CAT-777D (Fleet No. D-104)</option>
                            <option value="Hydraulic Shovel PC-1250 (Ex-08)">Hydraulic Shovel PC-1250 (Ex-08)</option>
                            <option value="Side Discharge Loader SDL-03">Side Discharge Loader SDL-03</option>
                            <option value="Load Haul Dumper LHD-06">Load Haul Dumper LHD-06</option>
                            <option value="Crawler Dozer D-375 (DZ-02)">Crawler Dozer D-375 (DZ-02)</option>
                            <option value="Main Direct Rope Hauler Engine">Main Direct Rope Hauler Engine</option>
                        </select>
                    </div>
                    <div>
                        <label style="font-size:11px; color:#94a3b8;">Certified Operator / Driver</label>
                        <input type="text" id="operator-name" required placeholder="Name & VTC / Badge No." style="width:100%; background:#020617; border:1px solid #334155; color:#fff; padding:8px; border-radius:6px; font-size:11px; margin-top:4px;">
                    </div>
                    <div>
                        <label style="font-size:11px; color:#94a3b8;">Dynamic Service & Parking Brake Test</label>
                        <select id="brake-test" onchange="evaluateBrakeRisk(this.value)" style="width:100%; background:#020617; border:1px solid #334155; color:#4ade80; font-weight:bold; padding:8px; border-radius:6px; font-size:11px; margin-top:4px;">
                            <option value="PASS: Held Firm on 1:10 Gradient">PASS: Held Firm on 1:10 Gradient</option>
                            <option value="FAIL: Brake Slip / Pressure Lag">FAIL: Brake Slip / Pressure Lag</option>
                            <option value="PASS: Static Stall Test Validated">PASS: Static Stall Test Validated</option>
                        </select>
                    </div>
                </div>

                <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap:8px; margin-bottom:12px;">
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">AVLA Reverse Siren</span>
                        <select id="avla-status" style="width:100%; background:transparent; border:none; color:#4ade80; font-weight:bold; font-size:11px; margin-top:2px;">
                            <option value="Audible >110 dB (DGMS Circular OK)">Audible >110 dB (OK)</option>
                            <option value="DEFECTIVE / MUTED">⚠️ DEFECTIVE / MUTED</option>
                            <option value="Intermittent Fault">Intermittent Fault</option>
                        </select>
                    </div>
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Fire Suppression (AFDSS)</span>
                        <select id="afdss-status" style="width:100%; background:transparent; border:none; color:#4ade80; font-weight:bold; font-size:11px; margin-top:2px;">
                            <option value="Pressure Green / Charged">Pressure Green (Charged)</option>
                            <option value="Low N2 Cylinder Pressure">Low N2 Pressure</option>
                            <option value="Auto-Actuation Disengaged">Disengaged Fault</option>
                        </select>
                    </div>
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Hydraulic & Steering Play</span>
                        <select id="hydraulic-status" style="width:100%; background:transparent; border:none; color:#4ade80; font-weight:bold; font-size:11px; margin-top:2px;">
                            <option value="Zero Leakage / Steering Firm">Zero Leak / Steering Firm</option>
                            <option value="Minor Weeping Hose">Minor Weeping Hose</option>
                            <option value="Severe Leak / Spongy Control">Severe Leak / Spongy</option>
                        </select>
                    </div>
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Pit Shift Engineer / Foreman</span>
                        <input type="text" id="foreman-name" required placeholder="Cert No." style="width:100%; background:transparent; border:none; color:#cbd5e1; font-size:11px; margin-top:2px;">
                    </div>
                </div>

                <button type="submit" id="submit-machinery-btn" style="width:100%; background:#d97706; color:#fff; font-weight:bold; border:none; padding:10px; border-radius:6px; font-size:12px; cursor:pointer;">
                    🚜 Certify Pre-Shift Roadworthiness (CMR 84)
                </button>
            </form>

            <!-- Machinery Audit History Table -->
            <div style="margin-top:14px; border-top:1px solid #1e293b; padding-top:10px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                    <div style="font-size:11px; font-weight:bold; color:#cbd5e1;">Statutory Fleet Examination Ledger</div>
                    <span id="machinery-count-badge" style="background:#334155; color:#cbd5e1; font-size:9px; padding:2px 6px; border-radius:8px;">0 Checks</span>
                </div>
                <div id="machinery-history-list" style="max-height:120px; overflow-y:auto; font-size:10px; color:#94a3b8;">
                    No machinery pre-shift audits registered in this shift.
                </div>
            </div>
        `;

        container.appendChild(card);
        renderMachineryLogs();
    }

    window.evaluateBrakeRisk = function(val) {
        var badge = document.getElementById('machinery-safety-badge');
        var select = document.getElementById('brake-test');
        var btn = document.getElementById('submit-machinery-btn');
        if (!badge) return;

        if (val.indexOf('FAIL') !== -1) {
            badge.style.background = '#7f1d1d';
            badge.style.color = '#fca5a5';
            badge.style.borderColor = '#ef4444';
            badge.innerText = '🚨 BRAKE DEFECT: GROUND IMMEDIATELY (CMR 84)';
            select.style.color = '#ef4444';
            if (btn) btn.style.background = '#dc2626';
        } else {
            badge.style.background = '#14532d';
            badge.style.color = '#4ade80';
            badge.style.borderColor = '#22c55e';
            badge.innerText = '✓ FLEET PIT-FIT (NORMAL)';
            select.style.color = '#4ade80';
            if (btn) btn.style.background = '#d97706';
        }
    };

    window.recordMachineryAudit = function(e) {
        if (e) e.preventDefault();
        var equip = document.getElementById('equip-id').value;
        var op = document.getElementById('operator-name').value;
        var brake = document.getElementById('brake-test').value;
        var avla = document.getElementById('avla-status').value;
        var afdss = document.getElementById('afdss-status').value;
        var hyd = document.getElementById('hydraulic-status').value;
        var foreman = document.getElementById('foreman-name').value;

        var isGrounded = (brake.indexOf('FAIL') !== -1 || avla.indexOf('DEFECTIVE') !== -1 || hyd.indexOf('Severe') !== -1);
        var certStatus = isGrounded ? 'GROUNDED / DEFECT TAGGED' : 'FIT FOR PIT DUTY';

        var entry = {
            id: 'HEMM-' + Date.now(),
            date: new Date().toLocaleDateString(),
            time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
            equipment: equip,
            operator: op,
            brake: brake,
            avla: avla,
            afdss: afdss,
            hydraulic: hyd,
            foreman: foreman,
            status: certStatus,
            seal: 'HEMM-SEAL-' + Math.random().toString(36).substring(2, 8).toUpperCase()
        };

        var store = JSON.parse(localStorage.getItem('dgms_machinery_logs') || '[]');
        store.unshift(entry);
        localStorage.setItem('dgms_machinery_logs', JSON.stringify(store));

        document.getElementById('operator-name').value = '';
        renderMachineryLogs();
        
        if (isGrounded) {
            alert('🚨 SAFETY WARNING: Machine has failed statutory check! Equipment grounded under CMR 84.');
        } else {
            alert('✅ Machine Pre-Shift Fitness Certified with Seal ' + entry.seal);
        }
    };

    function renderMachineryLogs() {
        var el = document.getElementById('machinery-history-list');
        var badge = document.getElementById('machinery-count-badge');
        if (!el) return;
        var store = JSON.parse(localStorage.getItem('dgms_machinery_logs') || '[]');

        if (badge) badge.innerText = store.length + ' Checks';

        if (store.length === 0) {
            el.innerHTML = '<div style="color:#64748b; padding:4px;">No machinery pre-shift audits registered in this shift.</div>';
            return;
        }

        el.innerHTML = store.map(function(item) {
            var isBad = item.status.indexOf('GROUNDED') !== -1;
            var col = isBad ? '#ef4444' : '#4ade80';
            return `
                <div style="background:#020617; border:1px solid #1e293b; padding:6px 8px; border-radius:4px; margin-bottom:4px;">
                    <div style="display:flex; justify-content:space-between; font-weight:bold;">
                        <span style="color:#38bdf8;">${item.equipment}</span>
                        <span style="font-family:monospace; color:#f59e0b; font-size:9px;">${item.seal}</span>
                    </div>
                    <div style="display:flex; justify-content:space-between; color:#cbd5e1; margin-top:2px;">
                        <span>Brakes: <b>${item.brake.slice(0, 15)}...</b> | AVLA: <b>${item.avla.slice(0, 12)}</b></span>
                        <span style="color:${col}; font-weight:bold;">${item.status}</span>
                    </div>
                    <div style="color:#64748b; font-size:9px; margin-top:2px;">
                        ${item.date} ${item.time} • Operator: ${item.operator} • Certified by Engineer: ${item.foreman}
                    </div>
                </div>
            `;
        }).join('');
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', injectMachineryUI);
    } else {
        injectMachineryUI();
    }
    setTimeout(injectMachineryUI, 2600);
})();
</script>
"""
