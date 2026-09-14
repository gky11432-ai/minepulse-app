# ui_medical.py - Standalone Mines Rules 1955 (PME) & MVTR 1966 Gate Pass Engine

MEDICAL_MODULE = """
<script>
(function() {
    function injectMedicalUI() {
        if (document.getElementById('statutory-medical-card')) return;

        var container = document.querySelector('.grid-container') || document.body;

        var card = document.createElement('div');
        card.id = 'statutory-medical-card';
        card.style.cssText = 'background:#0f172a; border:1px solid #334155; border-radius:10px; padding:16px; margin:14px 0; color:#f8fafc; font-family:system-ui, sans-serif; box-shadow:0 4px 6px -1px rgba(0,0,0,0.5);';

        card.innerHTML = `
            <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #1e293b; padding-bottom:10px; margin-bottom:12px;">
                <div style="display:flex; align-items:center; gap:8px;">
                    <span style="font-size:18px;">🩺</span>
                    <div>
                        <div style="font-size:13px; font-weight:bold; color:#38bdf8;">PME & VTC STATUTORY PIT GATE-PASS</div>
                        <div style="font-size:10px; color:#94a3b8;">Mines Rules 1955 Rule 29B & MVTR 1966 - Medical Fitness & Safety Training Audit</div>
                    </div>
                </div>
                <div id="medical-clearance-badge" style="background:#14532d; color:#4ade80; border:1px solid #22c55e; font-size:10px; padding:3px 8px; border-radius:12px; font-weight:bold;">
                    ✓ CLEAR FOR PIT ENTRY
                </div>
            </div>

            <!-- Miner Medical & VTC Clearance Form -->
            <form id="medical-gatepass-form" onsubmit="recordMedicalGatepass(event)">
                <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap:10px; margin-bottom:10px;">
                    <div>
                        <label style="font-size:11px; color:#94a3b8;">Miner Name & Token No.</label>
                        <input type="text" id="miner-id" required placeholder="e.g. Ramesh Mahto (TK-842)" style="width:100%; background:#020617; border:1px solid #334155; color:#fff; padding:8px; border-radius:6px; font-size:11px; margin-top:4px;">
                    </div>
                    <div>
                        <label style="font-size:11px; color:#94a3b8;">Miner Age (Years)</label>
                        <input type="number" id="miner-age" required placeholder="e.g. 48" oninput="validatePmeCompliance()" style="width:100%; background:#020617; border:1px solid #334155; color:#fff; padding:8px; border-radius:6px; font-size:11px; margin-top:4px;">
                    </div>
                    <div>
                        <label style="font-size:11px; color:#94a3b8;">Designated Trade / Craft</label>
                        <select id="miner-trade" style="width:100%; background:#020617; border:1px solid #334155; color:#fff; padding:8px; border-radius:6px; font-size:11px; margin-top:4px;">
                            <option value="Face Drill Operator">Face Drill Operator</option>
                            <option value="SDL / LHD Driver">SDL / LHD Driver</option>
                            <option value="Shotfirer / Blasting Crew">Shotfirer / Blasting Crew</option>
                            <option value="Roof Support Mason">Roof Support Mason</option>
                            <option value="Haulage Engine Driver">Haulage Engine Driver</option>
                            <option value="Underground Electrician">Underground Electrician</option>
                        </select>
                    </div>
                </div>

                <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap:8px; margin-bottom:12px;">
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Last PME Date (Form O)</span>
                        <input type="date" id="pme-date" required onchange="validatePmeCompliance()" style="width:100%; background:transparent; border:none; color:#38bdf8; font-weight:bold; font-size:11px; margin-top:2px;">
                    </div>
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Form O Fitness Finding</span>
                        <select id="pme-result" onchange="validatePmeCompliance()" style="width:100%; background:transparent; border:none; color:#4ade80; font-weight:bold; font-size:11px; margin-top:2px;">
                            <option value="Unconditionally Fit (Grade A)">Unconditionally Fit</option>
                            <option value="Temporary Unfit / Follow-up">⚠️ Temporary Unfit</option>
                            <option value="Medically Unfit for Pit">🚨 Unfit (Pneumoconiosis/Defect)</option>
                        </select>
                    </div>
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">VTC Refresher Training Date</span>
                        <input type="date" id="vtc-date" required onchange="validatePmeCompliance()" style="width:100%; background:transparent; border:none; color:#38bdf8; font-weight:bold; font-size:11px; margin-top:2px;">
                    </div>
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Attesting Safety Officer</span>
                        <input type="text" id="attesting-officer" required placeholder="Name & Reg No." style="width:100%; background:transparent; border:none; color:#cbd5e1; font-size:11px; margin-top:2px;">
                    </div>
                </div>

                <div id="gatepass-statutory-msg" style="background:#020617; border:1px dashed #334155; padding:8px; border-radius:6px; margin-bottom:12px; font-size:11px; color:#cbd5e1;">
                    Rule 29B Verification: Enter PME and VTC records to determine underground shift access clearance.
                </div>

                <button type="submit" id="submit-gatepass-btn" style="width:100%; background:#0284c7; color:#fff; font-weight:bold; border:none; padding:10px; border-radius:6px; font-size:12px; cursor:pointer;">
                    📋 Authorize Shift Gate-Pass (Mines Rule 29B)
                </button>
            </form>

            <!-- Gate Pass History Ledger -->
            <div style="margin-top:14px; border-top:1px solid #1e293b; padding-top:10px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                    <div style="font-size:11px; font-weight:bold; color:#cbd5e1;">PME & VTC Authorization Archive</div>
                    <span id="gatepass-count-badge" style="background:#334155; color:#cbd5e1; font-size:9px; padding:2px 6px; border-radius:8px;">0 Passes</span>
                </div>
                <div id="medical-pass-list" style="max-height:120px; overflow-y:auto; font-size:10px; color:#94a3b8;">
                    No medical gate-pass records issued today.
                </div>
            </div>
        `;

        container.appendChild(card);
        renderMedicalLogs();
    }

    window.validatePmeCompliance = function() {
        var age = parseInt(document.getElementById('miner-age').value) || 30;
        var pmeVal = document.getElementById('pme-date').value;
        var vtcVal = document.getElementById('vtc-date').value;
        var pmeResult = document.getElementById('pme-result').value;
        var badge = document.getElementById('medical-clearance-badge');
        var msg = document.getElementById('gatepass-statutory-msg');
        var btn = document.getElementById('submit-gatepass-btn');

        if (!badge || !msg) return;

        // Rule 29B: Interval is 5 years if age < 45, and 3 years if age >= 45
        var maxPmeYears = (age >= 45) ? 3 : 5;
        var now = new Date();
        var pmeExpired = false;
        var vtcExpired = false;
        var pmeYearsDiff = 0;
        var vtcYearsDiff = 0;

        if (pmeVal) {
            var pDate = new Date(pmeVal);
            pmeYearsDiff = (now - pDate) / (1000 * 60 * 60 * 24 * 365.25);
            if (pmeYearsDiff > maxPmeYears) pmeExpired = true;
        }

        if (vtcVal) {
            var vDate = new Date(vtcVal);
            vtcYearsDiff = (now - vDate) / (1000 * 60 * 60 * 24 * 365.25);
            if (vtcYearsDiff > 1.0) vtcExpired = true; // Annual refresher standard
        }

        var isMedicallyUnfit = (pmeResult.indexOf('Unfit') !== -1);

        if (isMedicallyUnfit || pmeExpired) {
            badge.style.background = '#7f1d1d';
            badge.style.color = '#fca5a5';
            badge.style.borderColor = '#ef4444';
            badge.innerText = '🚨 ENTRY FORBIDDEN: PME BREACH';

            var reason = isMedicallyUnfit ? 'Worker classified Medically Unfit on Form O.' : ('PME overdue by ' + (pmeYearsDiff - maxPmeYears).toFixed(1) + ' years (Max cycle: ' + maxPmeYears + ' yrs for age ' + age + ').');
            msg.innerHTML = '<span style="color:#ef4444; font-weight:bold;">ACCESS DENIED:</span> ' + reason + ' Deployment violates Mines Rules 1955 Rule 29B.';
            if (btn) { btn.style.background = '#dc2626'; btn.innerText = '⛔ Gate-Pass Blocked (Statutory Violation)'; }
            return false;
        } else if (vtcExpired) {
            badge.style.background = '#78350f';
            badge.style.color = '#fde68a';
            badge.style.borderColor = '#f59e0b';
            badge.innerText = '⚠️ CONDITIONAL: VTC REFRESHER DUE';
            msg.innerHTML = '<span style="color:#f59e0b; font-weight:bold;">VTC EXPIRED:</span> Annual refresher training expired (>1 yr). Requires immediate re-training schedule under MVTR 1966.';
            if (btn) { btn.style.background = '#d97706'; btn.innerText = '⚠️ Issue Conditional 24-Hr Slip'; }
            return true;
        } else {
            badge.style.background = '#14532d';
            badge.style.color = '#4ade80';
            badge.style.borderColor = '#22c55e';
            badge.innerText = '✓ CLEAR FOR PIT ENTRY';
            msg.innerHTML = '<span style="color:#4ade80; font-weight:bold;">STATUTORY COMPLIANT:</span> Valid Form O medical fitness and active VTC training. Authorized for shift duty.';
            if (btn) { btn.style.background = '#0284c7'; btn.innerText = '📋 Authorize Shift Gate-Pass (Mines Rule 29B)'; }
            return true;
        }
    };

    window.recordMedicalGatepass = function(e) {
        if (e) e.preventDefault();
        var miner = document.getElementById('miner-id').value;
        var age = document.getElementById('miner-age').value;
        var trade = document.getElementById('miner-trade').value;
        var pmeDate = document.getElementById('pme-date').value;
        var pmeRes = document.getElementById('pme-result').value;
        var vtcDate = document.getElementById('vtc-date').value;
        var officer = document.getElementById('attesting-officer').value;

        var isCleared = window.validatePmeCompliance();
        var statusLabel = (pmeRes.indexOf('Unfit') !== -1) ? 'BLOCKED: MEDICALLY UNFIT' : (isCleared ? 'GRANTED: STATUTORY FIT' : 'BLOCKED: PME OVERDUE');

        var entry = {
            id: 'PASS-' + Date.now(),
            date: new Date().toLocaleDateString(),
            time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
            miner: miner,
            age: age + ' yrs',
            trade: trade,
            pmeDate: pmeDate,
            vtcDate: vtcDate,
            result: pmeRes,
            officer: officer,
            status: statusLabel,
            seal: 'MED-SEAL-' + Math.random().toString(36).substring(2, 8).toUpperCase()
        };

        var store = JSON.parse(localStorage.getItem('dgms_medical_logs') || '[]');
        store.unshift(entry);
        localStorage.setItem('dgms_medical_logs', JSON.stringify(store));

        document.getElementById('miner-id').value = '';
        renderMedicalLogs();

        if (statusLabel.indexOf('BLOCKED') !== -1) {
            alert('🚨 STATUTORY GATE-PASS DENIED: Deployment blocked under Mines Rules 1955. Token recorded in breach register.');
        } else {
            alert('✅ Statutory Pit Gate-Pass Issued with Seal ' + entry.seal);
        }
    };

    function renderMedicalLogs() {
        var el = document.getElementById('medical-pass-list');
        var badge = document.getElementById('gatepass-count-badge');
        if (!el) return;
        var store = JSON.parse(localStorage.getItem('dgms_medical_logs') || '[]');

        if (badge) badge.innerText = store.length + ' Passes';

        if (store.length === 0) {
            el.innerHTML = '<div style="color:#64748b; padding:4px;">No medical gate-pass records issued today.</div>';
            return;
        }

        el.innerHTML = store.map(function(item) {
            var isBlocked = item.status.indexOf('BLOCKED') !== -1;
            var col = isBlocked ? '#ef4444' : '#4ade80';
            return `
                <div style="background:#020617; border:1px solid #1e293b; padding:6px 8px; border-radius:4px; margin-bottom:4px;">
                    <div style="display:flex; justify-content:space-between; font-weight:bold;">
                        <span style="color:#38bdf8;">${item.miner} (${item.trade})</span>
                        <span style="font-family:monospace; color:#f59e0b; font-size:9px;">${item.seal}</span>
                    </div>
                    <div style="display:flex; justify-content:space-between; color:#cbd5e1; margin-top:2px;">
                        <span>PME: <b>${item.pmeDate}</b> | VTC: <b>${item.vtcDate}</b></span>
                        <span style="color:${col}; font-weight:bold;">${item.status}</span>
                    </div>
                    <div style="color:#64748b; font-size:9px; margin-top:2px;">
                        ${item.date} ${item.time} • Age: ${item.age} • Attesting Safety Officer: ${item.officer}
                    </div>
                </div>
            `;
        }).join('');
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', injectMedicalUI);
    } else {
        injectMedicalUI();
    }
    setTimeout(injectMedicalUI, 3800);
})();
</script>
"""
