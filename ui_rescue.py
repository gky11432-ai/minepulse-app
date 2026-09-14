# ui_rescue.py - Standalone DGMS CMR 239-240 & Mines Rescue Rules Statutory Emergency Engine

RESCUE_MODULE = """
<script>
(function() {
    function injectRescueUI() {
        if (document.getElementById('statutory-rescue-card')) return;

        var container = document.querySelector('.grid-container') || document.body;

        var card = document.createElement('div');
        card.id = 'statutory-rescue-card';
        card.style.cssText = 'background:#0f172a; border:1px solid #334155; border-radius:10px; padding:16px; margin:14px 0; color:#f8fafc; font-family:system-ui, sans-serif; box-shadow:0 4px 6px -1px rgba(0,0,0,0.5);';

        card.innerHTML = `
            <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #1e293b; padding-bottom:10px; margin-bottom:12px;">
                <div style="display:flex; align-items:center; gap:8px;">
                    <span style="font-size:18px;">🩺</span>
                    <div>
                        <div style="font-size:13px; font-weight:bold; color:#ef4444;">EMERGENCY RESCUE & FIRST AID READINESS</div>
                        <div style="font-size:10px; color:#94a3b8;">DGMS CMR 2017 Reg 239 & 240 - Self-Rescuer (SCSR) & Rescue Station Audit</div>
                    </div>
                </div>
                <div id="rescue-readiness-badge" style="background:#14532d; color:#4ade80; border:1px solid #22c55e; font-size:10px; padding:3px 8px; border-radius:12px; font-weight:bold;">
                    ✓ RESCUE APPARATUS COMBAT-READY
                </div>
            </div>

            <!-- Rescue & SCSR Inspection Form -->
            <form id="rescue-audit-form" onsubmit="recordRescueAudit(event)">
                <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap:10px; margin-bottom:10px;">
                    <div>
                        <label style="font-size:11px; color:#94a3b8;">Rescue Station / First Aid Post</label>
                        <select id="rescue-station-id" style="width:100%; background:#020617; border:1px solid #334155; color:#fff; padding:8px; border-radius:6px; font-size:11px; margin-top:4px;">
                            <option value="Pithead Surface Rescue Room (Main)">Pithead Surface Rescue Room (Main)</option>
                            <option value="Underground First Aid Post (Shaft Bottom)">Underground First Aid Post (Shaft Bottom)</option>
                            <option value="Depillaring Section Inbye First Aid Box">Depillaring Section Inbye First Aid Box</option>
                            <option value="Continuous Miner District Aid Station">Continuous Miner District Aid Station</option>
                            <option value="Heavy Machinery Workshop Aid Post">Heavy Machinery Workshop Aid Post</option>
                        </select>
                    </div>
                    <div>
                        <label style="font-size:11px; color:#94a3b8;">SCSR Batch / Test Unit No.</label>
                        <input type="text" id="scsr-unit-no" required placeholder="e.g. SCSR-60M-1082" style="width:100%; background:#020617; border:1px solid #334155; color:#fff; padding:8px; border-radius:6px; font-size:11px; margin-top:4px;">
                    </div>
                    <div>
                        <label style="font-size:11px; color:#94a3b8;">SCSR Weight Difference (Grams)</label>
                        <input type="number" step="0.5" id="scsr-weight-diff" required placeholder="Max +10.0g (Moisture)" oninput="evaluateScsrWeight(this.value)" style="width:100%; background:#020617; border:1px solid #334155; color:#4ade80; font-weight:bold; padding:8px; border-radius:6px; font-size:11px; margin-top:4px;">
                    </div>
                </div>

                <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap:8px; margin-bottom:12px;">
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Reviving O2 Pressure (Bar)</span>
                        <input type="number" id="o2-pressure" required placeholder="Min 150 Bar" oninput="evaluateO2Pressure(this.value)" style="width:100%; background:transparent; border:none; color:#4ade80; font-weight:bold; font-size:13px; margin-top:2px;">
                    </div>
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Neil Robertson Stretcher</span>
                        <select id="stretcher-status" style="width:100%; background:transparent; border:none; color:#4ade80; font-weight:bold; font-size:11px; margin-top:2px;">
                            <option value="Straps & Canvas Intact (Clean)">Straps & Canvas Intact</option>
                            <option value="Damaged Harness / Defective">⚠️ Damaged / Defective</option>
                            <option value="Missing from Aid Post">⚠️ Missing from Post</option>
                        </select>
                    </div>
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Trained Rescue Crew on Shift</span>
                        <select id="rescue-crew-count" style="width:100%; background:transparent; border:none; color:#38bdf8; font-weight:bold; font-size:11px; margin-top:2px;">
                            <option value="Full Team (1 Captain + 5 Brigade)">Full Team (1 Capt + 5)</option>
                            <option value="Minimum Quorum (4 Trained)">Minimum Quorum (4)</option>
                            <option value="Deficient (<3 Trained Members)">⚠️ Crew Deficient (<3)</option>
                        </select>
                    </div>
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Rescue Superintendent / Officer</span>
                        <input type="text" id="rescue-officer" required placeholder="Name & Rescue Cert No." style="width:100%; background:transparent; border:none; color:#cbd5e1; font-size:11px; margin-top:2px;">
                    </div>
                </div>

                <div style="margin-bottom:12px;">
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Statutory First Aid Consumables & Anti-Venom Kit Check</span>
                        <select id="first-aid-kits" style="width:100%; background:transparent; border:none; color:#4ade80; font-weight:bold; font-size:11px; margin-top:2px;">
                            <option value="Sterile Dressings, Splints, Burn Sheets & Resuscitator Complete">Complete (Dressings, Splints, Burn Sheets & Resuscitator Valid)</option>
                            <option value="Partial Stock: Replenishment Indent Issued">Partial Stock (Indent Issued)</option>
                            <option value="Critical Shortage of Trauma Supplies">⚠️ Critical Shortage of Trauma Supplies</option>
                        </select>
                    </div>
                </div>

                <button type="submit" id="submit-rescue-btn" style="width:100%; background:#dc2626; color:#fff; font-weight:bold; border:none; padding:10px; border-radius:6px; font-size:12px; cursor:pointer;">
                    🩺 Certify Emergency Rescue & Life-Support Fitness (CMR 240)
                </button>
            </form>

            <!-- Rescue Audit History Table -->
            <div style="margin-top:14px; border-top:1px solid #1e293b; padding-top:10px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                    <div style="font-size:11px; font-weight:bold; color:#cbd5e1;">Statutory Rescue & Life-Support Log (Form-VIII Log)</div>
                    <span id="rescue-count-badge" style="background:#334155; color:#cbd5e1; font-size:9px; padding:2px 6px; border-radius:8px;">0 Checks</span>
                </div>
                <div id="rescue-history-list" style="max-height:120px; overflow-y:auto; font-size:10px; color:#94a3b8;">
                    No rescue equipment logs registered for current shift.
                </div>
            </div>
        `;

        container.appendChild(card);
        renderRescueLogs();
    }

    window.evaluateScsrWeight = function(val) {
        var diff = parseFloat(val);
        var badge = document.getElementById('rescue-readiness-badge');
        var input = document.getElementById('scsr-weight-diff');
        var btn = document.getElementById('submit-rescue-btn');
        if (isNaN(diff) || !badge) return;

        // DGMS CMR 239: Weight increase > 10 grams indicates KO2 / catalyst moisture spoilage
        if (diff > 10.0) {
            badge.style.background = '#7f1d1d';
            badge.style.color = '#fca5a5';
            badge.style.borderColor = '#ef4444';
            badge.innerText = '🚨 SCSR CONDEMNED: WEIGHT GAIN > 10g (DEFECTIVE)';
            input.style.color = '#ef4444';
            if (btn) btn.style.background = '#991b1b';
        } else {
            badge.style.background = '#14532d';
            badge.style.color = '#4ade80';
            badge.style.borderColor = '#22c55e';
            badge.innerText = '✓ RESCUE APPARATUS COMBAT-READY';
            input.style.color = '#4ade80';
            if (btn) btn.style.background = '#dc2626';
        }
    };

    window.evaluateO2Pressure = function(val) {
        var pressure = parseFloat(val);
        var badge = document.getElementById('rescue-readiness-badge');
        var input = document.getElementById('o2-pressure');
        if (isNaN(pressure) || !badge) return;

        if (pressure < 150) {
            badge.style.background = '#78350f';
            badge.style.color = '#fde68a';
            badge.style.borderColor = '#f59e0b';
            badge.innerText = '⚠️ REVIVING APPARATUS LOW PRESSURE (<150 BAR)';
            input.style.color = '#f59e0b';
        } else {
            input.style.color = '#4ade80';
        }
    };

    window.recordRescueAudit = function(e) {
        if (e) e.preventDefault();
        var station = document.getElementById('rescue-station-id').value;
        var unitNo = document.getElementById('scsr-unit-no').value;
        var weightDiff = parseFloat(document.getElementById('scsr-weight-diff').value) || 0;
        var o2 = parseFloat(document.getElementById('o2-pressure').value) || 0;
        var stretcher = document.getElementById('stretcher-status').value;
        var crew = document.getElementById('rescue-crew-count').value;
        var kit = document.getElementById('first-aid-kits').value;
        var officer = document.getElementById('rescue-officer').value;

        var isBreach = (weightDiff > 10.0 || o2 < 120 || stretcher.indexOf('Damaged') !== -1 || crew.indexOf('Deficient') !== -1);
        var certStatus = isBreach ? 'CONDEMNED / RESCUE DEFICIT' : 'CERTIFIED FIT FOR SERVICE';

        var entry = {
            id: 'RESCUE-' + Date.now(),
            date: new Date().toLocaleDateString(),
            time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
            station: station,
            unitNo: unitNo,
            weightDiff: (weightDiff >= 0 ? '+' : '') + weightDiff + ' g',
            o2: o2 + ' Bar',
            stretcher: stretcher,
            crew: crew,
            kit: kit,
            officer: officer,
            status: certStatus,
            seal: 'RESCUE-SEAL-' + Math.random().toString(36).substring(2, 8).toUpperCase()
        };

        var store = JSON.parse(localStorage.getItem('dgms_rescue_logs') || '[]');
        store.unshift(entry);
        localStorage.setItem('dgms_rescue_logs', JSON.stringify(store));

        document.getElementById('scsr-unit-no').value = '';
        document.getElementById('scsr-weight-diff').value = '';
        document.getElementById('o2-pressure').value = '';
        renderRescueLogs();

        if (isBreach) {
            alert('🚨 CMR 239/240 STATUTORY DEFECT: SCSR weight threshold breached or rescue brigade deficient! Quarantine unit immediately.');
        } else {
            alert('✅ Rescue & First Aid Readiness Certified with Seal ' + entry.seal);
        }
    };

    function renderRescueLogs() {
        var el = document.getElementById('rescue-history-list');
        var badge = document.getElementById('rescue-count-badge');
        if (!el) return;
        var store = JSON.parse(localStorage.getItem('dgms_rescue_logs') || '[]');

        if (badge) badge.innerText = store.length + ' Checks';

        if (store.length === 0) {
            el.innerHTML = '<div style="color:#64748b; padding:4px;">No rescue equipment logs registered for current shift.</div>';
            return;
        }

        el.innerHTML = store.map(function(item) {
            var isBad = item.status.indexOf('DEFICIT') !== -1 || item.status.indexOf('CONDEMNED') !== -1;
            var col = isBad ? '#ef4444' : '#4ade80';
            return `
                <div style="background:#020617; border:1px solid #1e293b; padding:6px 8px; border-radius:4px; margin-bottom:4px;">
                    <div style="display:flex; justify-content:space-between; font-weight:bold;">
                        <span style="color:#38bdf8;">${item.station} (${item.unitNo})</span>
                        <span style="font-family:monospace; color:#f59e0b; font-size:9px;">${item.seal}</span>
                    </div>
                    <div style="display:flex; justify-content:space-between; color:#cbd5e1; margin-top:2px;">
                        <span>SCSR ΔW: <b style="color:${col};">${item.weightDiff}</b> | O2: <b>${item.o2}</b></span>
                        <span>Crew: <b>${item.crew.slice(0, 14)}...</b></span>
                        <span style="color:${col}; font-weight:bold;">${item.status}</span>
                    </div>
                    <div style="color:#64748b; font-size:9px; margin-top:2px;">
                        ${item.date} ${item.time} • Stretcher: ${item.stretcher.slice(0, 14)} • Supt: ${item.officer}
                    </div>
                </div>
            `;
        }).join('');
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', injectRescueUI);
    } else {
        injectRescueUI();
    }
    setTimeout(injectRescueUI, 3600);
})();
</script>
"""
