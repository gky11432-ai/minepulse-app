# ui_haulage.py - Standalone DGMS CMR 87-103 Haulage Roadways & Safety Devices Engine

HAULAGE_MODULE = """
<script>
(function() {
    function injectHaulageUI() {
        if (document.getElementById('statutory-haulage-card')) return;

        var container = document.querySelector('.grid-container') || document.body;

        var card = document.createElement('div');
        card.id = 'statutory-haulage-card';
        card.style.cssText = 'background:#0f172a; border:1px solid #334155; border-radius:10px; padding:16px; margin:14px 0; color:#f8fafc; font-family:system-ui, sans-serif; box-shadow:0 4px 6px -1px rgba(0,0,0,0.5);';

        card.innerHTML = `
            <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #1e293b; padding-bottom:10px; margin-bottom:12px;">
                <div style="display:flex; align-items:center; gap:8px;">
                    <span style="font-size:18px;">🛤️</span>
                    <div>
                        <div style="font-size:13px; font-weight:bold; color:#f59e0b;">HAULAGE ROADWAY & SAFETY DEVICES REGISTER</div>
                        <div style="font-size:10px; color:#94a3b8;">DGMS CMR 2017 Reg 87-103 - Stop-Blocks, Runaway Switches & Wire Rope Audit</div>
                    </div>
                </div>
                <div id="haulage-safety-badge" style="background:#14532d; color:#4ade80; border:1px solid #22c55e; font-size:10px; padding:3px 8px; border-radius:12px; font-weight:bold;">
                    ✓ HAULAGE TRACK OPERATIONAL
                </div>
            </div>

            <!-- Haulage Examination Form -->
            <form id="haulage-audit-form" onsubmit="recordHaulageAudit(event)">
                <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap:10px; margin-bottom:10px;">
                    <div>
                        <label style="font-size:11px; color:#94a3b8;">Haulage Roadway / Incline Track</label>
                        <select id="haulage-track-id" style="width:100%; background:#020617; border:1px solid #334155; color:#fff; padding:8px; border-radius:6px; font-size:11px; margin-top:4px;">
                            <option value="Main Dip Direct Rope Incline (1 in 8)">Main Dip Direct Rope Incline (1 in 8)</option>
                            <option value="Endless Haulage Level 5 East">Endless Haulage Level 5 East</option>
                            <option value="District 2 Gravity Incline (Jig)">District 2 Gravity Incline (Jig)</option>
                            <option value="Trunk Locomotive Haulage Drift">Trunk Locomotive Haulage Drift</option>
                            <option value="Tail-Rope Supply Incline Drift C">Tail-Rope Supply Incline Drift C</option>
                        </select>
                    </div>
                    <div>
                        <label style="font-size:11px; color:#94a3b8;">Stop-Block & Runway Switch Test (CMR 92)</label>
                        <select id="stop-block-status" onchange="evaluateHaulageRisk()" style="width:100%; background:#020617; border:1px solid #334155; color:#4ade80; font-weight:bold; padding:8px; border-radius:6px; font-size:11px; margin-top:4px;">
                            <option value="PASS: Stop-Block Interlocked & Closed">PASS: Stop-Block Interlocked & Closed</option>
                            <option value="FAIL: Stop-Block Jammed / Missing">⚠️ FAIL: Stop-Block Defective</option>
                            <option value="FAIL: Runaway Switch Failed to Derail">⚠️ FAIL: Runaway Switch Failed</option>
                        </select>
                    </div>
                    <div>
                        <label style="font-size:11px; color:#94a3b8;">Jazz-Rails & Drop-Warrant Check</label>
                        <select id="jazz-rail-status" onchange="evaluateHaulageRisk()" style="width:100%; background:#020617; border:1px solid #334155; color:#4ade80; font-weight:bold; padding:8px; border-radius:6px; font-size:11px; margin-top:4px;">
                            <option value="Operational (Counter-Weighted)">Operational (Counter-Weighted)</option>
                            <option value="Back-Stay Drag In Position">Back-Stay Drag In Position</option>
                            <option value="Defective / Damaged Springs">⚠️ Defective / Damaged Springs</option>
                        </select>
                    </div>
                </div>

                <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap:8px; margin-bottom:12px;">
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Manholes Clearance (Every 10m)</span>
                        <select id="manhole-check" style="width:100%; background:transparent; border:none; color:#4ade80; font-weight:bold; font-size:11px; margin-top:2px;">
                            <option value="All Clear, Clean & Whitewashed">All Clear & Whitewashed</option>
                            <option value="Obstructed by Debris / Coal">⚠️ Obstructed by Debris</option>
                            <option value="Whitewashing Faded / Number Illegible">Whitewash Faded</option>
                        </select>
                    </div>
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Rope Recapping Date (Max 6 Mos)</span>
                        <input type="date" id="recapping-date" required onchange="evaluateRopeCapping()" style="width:100%; background:transparent; border:none; color:#38bdf8; font-weight:bold; font-size:11px; margin-top:2px;">
                    </div>
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Wire Rope Factor of Safety</span>
                        <input type="number" step="0.1" id="rope-fos" required placeholder="Min 6.5" style="width:100%; background:transparent; border:none; color:#fff; font-weight:bold; font-size:13px; margin-top:2px;">
                    </div>
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Signaling Bells (CMR 91)</span>
                        <select id="signals-status" style="width:100%; background:transparent; border:none; color:#4ade80; font-weight:bold; font-size:11px; margin-top:2px;">
                            <option value="Audible from All Incline Points">Audible Everywhere (OK)</option>
                            <option value="Bare Wire Signal Defective">⚠️ Bare Wire Defective</option>
                            <option value="Intermittent Bell Ring">Intermittent Bell</option>
                        </select>
                    </div>
                </div>

                <div style="display:grid; grid-template-columns: 1fr 1fr; gap:8px; margin-bottom:12px;">
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Rollers & Pulleys Condition</span>
                        <select id="rollers-condition" style="width:100%; background:transparent; border:none; color:#4ade80; font-weight:bold; font-size:11px; margin-top:2px;">
                            <option value="Free Rotating / Adequately Greased">Free Rotating / Greased</option>
                            <option value="Grooved / Stagnant Rollers">Grooved / Stagnant Rollers</option>
                            <option value="Missing Pulleys on Curve">⚠️ Missing Pulleys on Curve</option>
                        </select>
                    </div>
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Competent Haulage Examiner</span>
                        <input type="text" id="haulage-officer" required placeholder="Name & Sirdar/Overman Cert" style="width:100%; background:transparent; border:none; color:#cbd5e1; font-size:11px; margin-top:2px;">
                    </div>
                </div>

                <button type="submit" id="submit-haulage-btn" style="width:100%; background:#d97706; color:#fff; font-weight:bold; border:none; padding:10px; border-radius:6px; font-size:12px; cursor:pointer;">
                    🛤️ Certify Haulage Roadway Fitness (CMR 87)
                </button>
            </form>

            <!-- Haulage Register Archive -->
            <div style="margin-top:14px; border-top:1px solid #1e293b; padding-top:10px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                    <div style="font-size:11px; font-weight:bold; color:#cbd5e1;">Statutory Haulage Examination Ledger</div>
                    <span id="haulage-count-badge" style="background:#334155; color:#cbd5e1; font-size:9px; padding:2px 6px; border-radius:8px;">0 Checks</span>
                </div>
                <div id="haulage-history-list" style="max-height:120px; overflow-y:auto; font-size:10px; color:#94a3b8;">
                    No haulage examinations logged today.
                </div>
            </div>
        `;

        container.appendChild(card);
        renderHaulageLogs();
    }

    window.evaluateRopeCapping = function() {
        var val = document.getElementById('recapping-date').value;
        if (!val) return;
        var capDate = new Date(val);
        var now = new Date();
        var diffDays = (now - capDate) / (1000 * 60 * 60 * 24);

        var badge = document.getElementById('haulage-safety-badge');
        var btn = document.getElementById('submit-haulage-btn');

        // CMR 97: Haulage rope shall be re-capped once at least in every six months (180 days)
        if (diffDays > 180) {
            badge.style.background = '#7f1d1d';
            badge.style.color = '#fca5a5';
            badge.style.borderColor = '#ef4444';
            badge.innerText = '🚨 ROPE RECAPPING OVERDUE (>6 MOS)';
            if (btn) { btn.style.background = '#dc2626'; btn.innerText = '⛔ Haulage Prohibited: Re-Capping Overdue'; }
        } else {
            window.evaluateHaulageRisk();
        }
    };

    window.evaluateHaulageRisk = function() {
        var sb = document.getElementById('stop-block-status').value;
        var jr = document.getElementById('jazz-rail-status').value;
        var badge = document.getElementById('haulage-safety-badge');
        var btn = document.getElementById('submit-haulage-btn');
        if (!badge) return;

        var isDefective = (sb.indexOf('FAIL') !== -1 || jr.indexOf('Defective') !== -1);

        if (isDefective) {
            badge.style.background = '#7f1d1d';
            badge.style.color = '#fca5a5';
            badge.style.borderColor = '#ef4444';
            badge.innerText = '🚨 HAULAGE INTERLOCKED: STOP-BLOCK / SWITCH DEFECT';
            if (btn) { btn.style.background = '#dc2626'; btn.innerText = '⛔ Track Blocked (CMR 92 Breach)'; }
        } else {
            badge.style.background = '#14532d';
            badge.style.color = '#4ade80';
            badge.style.borderColor = '#22c55e';
            badge.innerText = '✓ HAULAGE TRACK OPERATIONAL';
            if (btn) { btn.style.background = '#d97706'; btn.innerText = '🛤️ Certify Haulage Roadway Fitness (CMR 87)'; }
        }
    };

    window.recordHaulageAudit = function(e) {
        if (e) e.preventDefault();
        var track = document.getElementById('haulage-track-id').value;
        var sb = document.getElementById('stop-block-status').value;
        var jr = document.getElementById('jazz-rail-status').value;
        var manhole = document.getElementById('manhole-check').value;
        var capDate = document.getElementById('recapping-date').value;
        var fos = document.getElementById('rope-fos').value;
        var signals = document.getElementById('signals-status').value;
        var officer = document.getElementById('haulage-officer').value;

        var isBreach = (sb.indexOf('FAIL') !== -1 || jr.indexOf('Defective') !== -1 || manhole.indexOf('Obstructed') !== -1);
        var certStatus = isBreach ? 'HAULAGE SUSPENDED / DEFECTIVE' : 'CERTIFIED FIT FOR TRAMMING';

        var entry = {
            id: 'HAUL-' + Date.now(),
            date: new Date().toLocaleDateString(),
            time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
            track: track,
            stopBlock: sb,
            jazzRail: jr,
            manhole: manhole,
            capDate: capDate,
            fos: fos,
            signals: signals,
            officer: officer,
            status: certStatus,
            seal: 'HAUL-SEAL-' + Math.random().toString(36).substring(2, 8).toUpperCase()
        };

        var store = JSON.parse(localStorage.getItem('dgms_haulage_logs') || '[]');
        store.unshift(entry);
        localStorage.setItem('dgms_haulage_logs', JSON.stringify(store));

        renderHaulageLogs();

        if (isBreach) {
            alert('🚨 CMR 92 STATUTORY BREACH: Haulage safety device defective! Tramming operations interlocked.');
        } else {
            alert('✅ Haulage Roadway Fitness Certified with Seal ' + entry.seal);
        }
    };

    function renderHaulageLogs() {
        var el = document.getElementById('haulage-history-list');
        var badge = document.getElementById('haulage-count-badge');
        if (!el) return;
        var store = JSON.parse(localStorage.getItem('dgms_haulage_logs') || '[]');

        if (badge) badge.innerText = store.length + ' Checks';

        if (store.length === 0) {
            el.innerHTML = '<div style="color:#64748b; padding:4px;">No haulage examinations logged today.</div>';
            return;
        }

        el.innerHTML = store.map(function(item) {
            var isBad = item.status.indexOf('SUSPENDED') !== -1;
            var col = isBad ? '#ef4444' : '#4ade80';
            return `
                <div style="background:#020617; border:1px solid #1e293b; padding:6px 8px; border-radius:4px; margin-bottom:4px;">
                    <div style="display:flex; justify-content:space-between; font-weight:bold;">
                        <span style="color:#38bdf8;">${item.track}</span>
                        <span style="font-family:monospace; color:#f59e0b; font-size:9px;">${item.seal}</span>
                    </div>
                    <div style="display:flex; justify-content:space-between; color:#cbd5e1; margin-top:2px;">
                        <span>Stop-Block: <b>${item.stopBlock.slice(0, 15)}...</b> | FOS: <b>${item.fos}</b></span>
                        <span style="color:${col}; font-weight:bold;">${item.status}</span>
                    </div>
                    <div style="color:#64748b; font-size:9px; margin-top:2px;">
                        ${item.date} ${item.time} • Manholes: ${item.manhole.slice(0, 14)} • Re-Capped: ${item.capDate} • Insp: ${item.officer}
                    </div>
                </div>
            `;
        }).join('');
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', injectHaulageUI);
    } else {
        injectHaulageUI();
    }
    setTimeout(injectHaulageUI, 4000);
})();
</script>
"""
