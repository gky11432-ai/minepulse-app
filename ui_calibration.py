# ui_calibration.py - Standalone DGMS CMR 152 Multi-Gas Detector Bump-Test & Calibration Engine

CALIBRATION_MODULE = """
<script>
(function() {
    function injectCalibrationUI() {
        if (document.getElementById('statutory-calibration-card')) return;

        var container = document.querySelector('.grid-container') || document.body;

        var card = document.createElement('div');
        card.id = 'statutory-calibration-card';
        card.style.cssText = 'background:#0f172a; border:1px solid #334155; border-radius:10px; padding:16px; margin:14px 0; color:#f8fafc; font-family:system-ui, sans-serif; box-shadow:0 4px 6px -1px rgba(0,0,0,0.5);';

        card.innerHTML = `
            <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #1e293b; padding-bottom:10px; margin-bottom:12px;">
                <div style="display:flex; align-items:center; gap:8px;">
                    <span style="font-size:18px;">📟</span>
                    <div>
                        <div style="font-size:13px; font-weight:bold; color:#38bdf8;">MULTI-GAS DETECTOR BUMP-TEST & CALIBRATION</div>
                        <div style="font-size:10px; color:#94a3b8;">DGMS CMR 2017 Reg 152 - Pre-Shift Sensor Verification (CH4, CO, O2, H2S)</div>
                    </div>
                </div>
                <div id="calibration-status-badge" style="background:#14532d; color:#4ade80; border:1px solid #22c55e; font-size:10px; padding:3px 8px; border-radius:12px; font-weight:bold;">
                    ✓ DETECTOR CERTIFIED FIT
                </div>
            </div>

            <!-- Detector Pre-Shift Bump & Span Verification Form -->
            <form id="calibration-form" onsubmit="recordCalibrationAudit(event)">
                <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap:10px; margin-bottom:10px;">
                    <div>
                        <label style="font-size:11px; color:#94a3b8;">Detector Model & Serial No.</label>
                        <input type="text" id="detector-id" required placeholder="e.g. MSA Altair 4XR (SN: 98412)" style="width:100%; background:#020617; border:1px solid #334155; color:#fff; padding:8px; border-radius:6px; font-size:11px; margin-top:4px;">
                    </div>
                    <div>
                        <label style="font-size:11px; color:#94a3b8;">Issued To (Mining Officer)</label>
                        <input type="text" id="issued-to-officer" required placeholder="Name & Sirdar/Overman Cert" style="width:100%; background:#020617; border:1px solid #334155; color:#fff; padding:8px; border-radius:6px; font-size:11px; margin-top:4px;">
                    </div>
                    <div>
                        <label style="font-size:11px; color:#94a3b8;">Daily Span Gas Bump-Test Result</label>
                        <select id="bump-test-result" onchange="evaluateCalibrationStatus()" style="width:100%; background:#020617; border:1px solid #334155; color:#4ade80; font-weight:bold; padding:8px; border-radius:6px; font-size:11px; margin-top:4px;">
                            <option value="PASS: All 4 Sensors Responded (<15 sec)">PASS: All 4 Sensors Responded (<15s)</option>
                            <option value="FAIL: CH4 Sensor Unresponsive">⚠️ FAIL: CH4 Sensor Defective</option>
                            <option value="FAIL: O2 Sensor Drifted (<19.5% Fresh)">⚠️ FAIL: O2 Sensor Drifted</option>
                            <option value="FAIL: CO Sensor Delayed Response">⚠️ FAIL: CO Sensor Sluggish</option>
                            <option value="FAIL: Audible/Visual Alarm Muted">⚠️ FAIL: Siren / Strobe Defective</option>
                        </select>
                    </div>
                </div>

                <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap:8px; margin-bottom:12px;">
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Last Span Calibration Date</span>
                        <input type="date" id="span-cal-date" required onchange="evaluateCalibrationStatus()" style="width:100%; background:transparent; border:none; color:#38bdf8; font-weight:bold; font-size:11px; margin-top:2px;">
                    </div>
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Fresh Air O2 Zero Reading</span>
                        <input type="number" step="0.1" id="fresh-o2" required placeholder="Target 20.9%" oninput="evaluateCalibrationStatus()" style="width:100%; background:transparent; border:none; color:#4ade80; font-weight:bold; font-size:13px; margin-top:2px;">
                    </div>
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Battery Charge Level (%)</span>
                        <input type="number" id="battery-pct" required placeholder="Min 60%" oninput="evaluateCalibrationStatus()" style="width:100%; background:transparent; border:none; color:#fff; font-weight:bold; font-size:13px; margin-top:2px;">
                    </div>
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Lamp Room / Safety Incharge</span>
                        <input type="text" id="lamproom-officer" required placeholder="Name & Token" style="width:100%; background:transparent; border:none; color:#cbd5e1; font-size:11px; margin-top:2px;">
                    </div>
                </div>

                <div id="cal-statutory-msg" style="background:#020617; border:1px dashed #334155; padding:8px; border-radius:6px; margin-bottom:12px; font-size:11px; color:#cbd5e1;">
                    CMR 152 Verification: Detector must pass pre-shift challenge gas bump-test and possess a valid span calibration within the last 30 days.
                </div>

                <button type="submit" id="submit-calibration-btn" style="width:100%; background:#0284c7; color:#fff; font-weight:bold; border:none; padding:10px; border-radius:6px; font-size:12px; cursor:pointer;">
                    📟 Certify Detector & Authorize Pit Issue (CMR 152)
                </button>
            </form>

            <!-- Calibration History Ledger -->
            <div style="margin-top:14px; border-top:1px solid #1e293b; padding-top:10px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                    <div style="font-size:11px; font-weight:bold; color:#cbd5e1;">Lamp Room Gas Detector Calibration Log</div>
                    <span id="cal-count-badge" style="background:#334155; color:#cbd5e1; font-size:9px; padding:2px 6px; border-radius:8px;">0 Checked</span>
                </div>
                <div id="calibration-history-list" style="max-height:120px; overflow-y:auto; font-size:10px; color:#94a3b8;">
                    No gas detector tests logged in current shift.
                </div>
            </div>
        `;

        container.appendChild(card);
        renderCalibrationLogs();
    }

    window.evaluateCalibrationStatus = function() {
        var bump = document.getElementById('bump-test-result').value;
        var calDateVal = document.getElementById('span-cal-date').value;
        var o2Val = parseFloat(document.getElementById('fresh-o2').value) || 20.9;
        var battVal = parseInt(document.getElementById('battery-pct').value) || 100;

        var badge = document.getElementById('calibration-status-badge');
        var msg = document.getElementById('cal-statutory-msg');
        var btn = document.getElementById('submit-calibration-btn');

        if (!badge || !msg) return;

        var isBumpFailed = (bump.indexOf('FAIL') !== -1);
        var isCalOverdue = false;
        var daysSinceCal = 0;

        if (calDateVal) {
            var cDate = new Date(calDateVal);
            var now = new Date();
            daysSinceCal = Math.floor((now - cDate) / (1000 * 60 * 60 * 24));
            if (daysSinceCal > 30) isCalOverdue = true; // DGMS 30-day statutory calibration cycle
        }

        var isO2Abnormal = (o2Val < 20.7 || o2Val > 21.1);
        var isLowBattery = (battVal < 50);

        if (isBumpFailed || isCalOverdue) {
            badge.style.background = '#7f1d1d';
            badge.style.color = '#fca5a5';
            badge.style.borderColor = '#ef4444';
            badge.innerText = '🚨 QUARANTINED: PIT ISSUE FORBIDDEN';

            var errorReason = isBumpFailed ? bump : ('Span Calibration Overdue (' + daysSinceCal + ' days ago, Limit: 30 days)');
            msg.innerHTML = '<span style="color:#ef4444; font-weight:bold;">QUARANTINE ORDER:</span> ' + errorReason + '. Unit withdrawn under CMR 152.';
            if (btn) {
                btn.style.background = '#dc2626';
                btn.innerText = '⛔ Detector Quarantined (Issue Blocked)';
            }
            return false;
        } else if (isO2Abnormal || isLowBattery) {
            badge.style.background = '#78350f';
            badge.style.color = '#fde68a';
            badge.style.borderColor = '#f59e0b';
            badge.innerText = '⚠️ CAUTION: RE-ZERO / CHARGE REQ';

            msg.innerHTML = '<span style="color:#f59e0b; font-weight:bold;">ATTENTION:</span> O2 sensor zero drift (' + o2Val + '%) or battery low (' + battVal + '%). Clean air zeroing recommended.';
            if (btn) {
                btn.style.background = '#d97706';
                btn.innerText = '⚠️ Authorize with Caution Tag';
            }
            return true;
        } else {
            badge.style.background = '#14532d';
            badge.style.color = '#4ade80';
            badge.style.borderColor = '#22c55e';
            badge.innerText = '✓ DETECTOR CERTIFIED FIT';

            msg.innerHTML = '<span style="color:#4ade80; font-weight:bold;">STATUTORY COMPLIANT:</span> Bump-test verified and calibration valid (' + (30 - daysSinceCal) + ' days remaining). Authorized for shift issue.';
            if (btn) {
                btn.style.background = '#0284c7';
                btn.innerText = '📟 Certify Detector & Authorize Pit Issue (CMR 152)';
            }
            return true;
        }
    };

    window.recordCalibrationAudit = function(e) {
        if (e) e.preventDefault();
        var detId = document.getElementById('detector-id').value;
        var officer = document.getElementById('issued-to-officer').value;
        var bump = document.getElementById('bump-test-result').value;
        var calDate = document.getElementById('span-cal-date').value;
        var o2 = document.getElementById('fresh-o2').value;
        var batt = document.getElementById('battery-pct').value;
        var incharge = document.getElementById('lamproom-officer').value;

        var isPassed = window.evaluateCalibrationStatus();
        var statusText = isPassed ? 'ISSUED: FIT FOR UNDERGROUND' : 'QUARANTINED: DEFECTIVE / OVERDUE';

        var entry = {
            id: 'CAL-' + Date.now(),
            date: new Date().toLocaleDateString(),
            time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
            detectorId: detId,
            officer: officer,
            bump: bump,
            calDate: calDate,
            o2: o2 + '%',
            battery: batt + '%',
            incharge: incharge,
            status: statusText,
            seal: 'CAL-SEAL-' + Math.random().toString(36).substring(2, 8).toUpperCase()
        };

        var store = JSON.parse(localStorage.getItem('dgms_calibration_logs') || '[]');
        store.unshift(entry);
        localStorage.setItem('dgms_calibration_logs', JSON.stringify(store));

        document.getElementById('detector-id').value = '';
        renderCalibrationLogs();

        if (!isPassed) {
            alert('🚨 STATUTORY BREACH: Gas detector failed verification! Unit quarantined under CMR 152.');
        } else {
            alert('✅ Detector Certified Fit & Issued with Seal ' + entry.seal);
        }
    };

    function renderCalibrationLogs() {
        var el = document.getElementById('calibration-history-list');
        var badge = document.getElementById('cal-count-badge');
        if (!el) return;
        var store = JSON.parse(localStorage.getItem('dgms_calibration_logs') || '[]');

        if (badge) badge.innerText = store.length + ' Checked';

        if (store.length === 0) {
            el.innerHTML = '<div style="color:#64748b; padding:4px;">No gas detector tests logged in current shift.</div>';
            return;
        }

        el.innerHTML = store.map(function(item) {
            var isQuarantined = (item.status.indexOf('QUARANTINED') !== -1);
            var col = isQuarantined ? '#ef4444' : '#4ade80';
            return `
                <div style="background:#020617; border:1px solid #1e293b; padding:6px 8px; border-radius:4px; margin-bottom:4px;">
                    <div style="display:flex; justify-content:space-between; font-weight:bold;">
                        <span style="color:#38bdf8;">${item.detectorId}</span>
                        <span style="font-family:monospace; color:#f59e0b; font-size:9px;">${item.seal}</span>
                    </div>
                    <div style="display:flex; justify-content:space-between; color:#cbd5e1; margin-top:2px;">
                        <span>Issued To: <b>${item.officer}</b></span>
                        <span style="color:${col}; font-weight:bold;">${item.status}</span>
                    </div>
                    <div style="color:#64748b; font-size:9px; margin-top:2px;">
                        ${item.date} ${item.time} • O2: ${item.o2} | Batt: ${item.battery} • Cal Date: ${item.calDate} • Incharge: ${item.incharge}
                    </div>
                </div>
            `;
        }).join('');
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', injectCalibrationUI);
    } else {
        injectCalibrationUI();
    }
    setTimeout(injectCalibrationUI, 4400);
})();
</script>
"""
