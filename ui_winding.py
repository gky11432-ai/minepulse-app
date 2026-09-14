# ui_winding.py - Standalone DGMS CMR 71-82 Shaft & Winding Engine Statutory Examination Engine

WINDING_MODULE = """
<script>
(function() {
    function injectWindingUI() {
        if (document.getElementById('statutory-winding-card')) return;

        var container = document.querySelector('.grid-container') || document.body;

        var card = document.createElement('div');
        card.id = 'statutory-winding-card';
        card.style.cssText = 'background:#0f172a; border:1px solid #334155; border-radius:10px; padding:16px; margin:14px 0; color:#f8fafc; font-family:system-ui, sans-serif; box-shadow:0 4px 6px -1px rgba(0,0,0,0.5);';

        card.innerHTML = `
            <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #1e293b; padding-bottom:10px; margin-bottom:12px;">
                <div style="display:flex; align-items:center; gap:8px;">
                    <span style="font-size:18px;">🛗</span>
                    <div>
                        <div style="font-size:13px; font-weight:bold; color:#38bdf8;">SHAFT & WINDING ENGINE SAFETY AUDIT</div>
                        <div style="font-size:10px; color:#94a3b8;">DGMS CMR 2017 Reg 71-82 - Overwind Contrivance, CSG & Shaft Examination</div>
                    </div>
                </div>
                <div id="winding-safety-badge" style="background:#14532d; color:#4ade80; border:1px solid #22c55e; font-size:10px; padding:3px 8px; border-radius:12px; font-weight:bold;">
                    ✓ WINDING SYSTEM CERTIFIED FIT
                </div>
            </div>

            <!-- Shaft & Winding Pre-Shift Examination Form -->
            <form id="winding-audit-form" onsubmit="recordWindingAudit(event)">
                <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap:10px; margin-bottom:10px;">
                    <div>
                        <label style="font-size:11px; color:#94a3b8;">Shaft Unit / Winding Installation</label>
                        <select id="shaft-unit-id" style="width:100%; background:#020617; border:1px solid #334155; color:#fff; padding:8px; border-radius:6px; font-size:11px; margin-top:4px;">
                            <option value="Main Man-Riding Pit Shaft (No. 1 Cage)">Main Man-Riding Pit Shaft (No. 1 Cage)</option>
                            <option value="Mineral Hoisting Skip Shaft (No. 2)">Mineral Hoisting Skip Shaft (No. 2)</option>
                            <option value="Auxiliary Emergency Escape Shaft">Auxiliary Emergency Escape Shaft</option>
                            <option value="Direct Haulage Drift Incline Man-Car">Direct Haulage Drift Incline Man-Car</option>
                            <option value="Ventilation Upcast Shaft Air-Lock">Ventilation Upcast Shaft Air-Lock</option>
                        </select>
                    </div>
                    <div>
                        <label style="font-size:11px; color:#94a3b8;">Automatic Overwind & Overspeed Contrivance</label>
                        <select id="overwind-test" onchange="evaluateWindingRisk(this.value)" style="width:100%; background:#020617; border:1px solid #334155; color:#4ade80; font-weight:bold; padding:8px; border-radius:6px; font-size:11px; margin-top:4px;">
                            <option value="TEST PASS: Tripped Instantly at Landing Threshold">TEST PASS: Tripped Instantly</option>
                            <option value="TEST FAIL: Contrivance Failed to Trip Power">⚠️ TEST FAIL: FAILED TO TRIP</option>
                            <option value="TEST PASS: Slow-Banking Mechanism Validated">TEST PASS: Slow-Banking OK</option>
                        </select>
                    </div>
                    <div>
                        <label style="font-size:11px; color:#94a3b8;">Dual Mechanical Brakes Holding Test</label>
                        <select id="brake-holding" style="width:100%; background:#020617; border:1px solid #334155; color:#4ade80; font-weight:bold; padding:8px; border-radius:6px; font-size:11px; margin-top:4px;">
                            <option value="Held Full Load at Maximum Torque (Zero Slip)">Held Full Load (Zero Slip)</option>
                            <option value="Brake Lining Worn / Slippage Detected">⚠️ Brake Slippage Detected</option>
                            <option value="Pneumatic/Hydraulic Pressure Normal">Pressure Normal (Pass)</option>
                        </select>
                    </div>
                </div>

                <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap:8px; margin-bottom:12px;">
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Detaching Hook & Safety Catches</span>
                        <select id="detaching-hook" style="width:100%; background:transparent; border:none; color:#4ade80; font-weight:bold; font-size:11px; margin-top:2px;">
                            <option value="Clean, Calibrated & Greased (Free Play)">Clean & Greased (OK)</option>
                            <option value="Copper Shear Pin Deformed / Loose">⚠️ Copper Pin Deformed</option>
                            <option value="Due for 6-Monthly Heat Treatment">Due for Heat Treatment</option>
                        </select>
                    </div>
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Cage Suspension Gear (CSG) Chains</span>
                        <select id="csg-chains" style="width:100%; background:transparent; border:none; color:#4ade80; font-weight:bold; font-size:11px; margin-top:2px;">
                            <option value="Bridle Chains Free of Flaws / Cracks">Chains Flaw-Free (OK)</option>
                            <option value="Elongation / Wear Near 5% Limit">Wear Near 5% Limit</option>
                            <option value="Excessive Wear / Crack Tagged">⚠️ Excessive Wear / Crack</option>
                        </select>
                    </div>
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Shaft Guides & Signaling (Keps)</span>
                        <select id="shaft-signals" style="width:100%; background:transparent; border:none; color:#4ade80; font-weight:bold; font-size:11px; margin-top:2px;">
                            <option value="Electrical Bells & Visual Indicators Clear">Bells & Visual OK</option>
                            <option value="Guide Rope Tension Normal">Guide Tension Normal</option>
                            <option value="Signal Intermittent / Bell Dead">⚠️ Signal Intermittent</option>
                        </select>
                    </div>
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Statutory Winding Engineman / Engineer</span>
                        <input type="text" id="winding-engineer" required placeholder="Name & 1st Class Cert" style="width:100%; background:transparent; border:none; color:#cbd5e1; font-size:11px; margin-top:2px;">
                    </div>
                </div>

                <button type="submit" id="submit-winding-btn" style="width:100%; background:#0284c7; color:#fff; font-weight:bold; border:none; padding:10px; border-radius:6px; font-size:12px; cursor:pointer;">
                    🛗 Certify Shaft & Man-Winding Safety (CMR 74)
                </button>
            </form>

            <!-- Winding Register History Table -->
            <div style="margin-top:14px; border-top:1px solid #1e293b; padding-top:10px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                    <div style="font-size:11px; font-weight:bold; color:#cbd5e1;">Statutory Shaft Examination Register (CMR 71 Log)</div>
                    <span id="winding-count-badge" style="background:#334155; color:#cbd5e1; font-size:9px; padding:2px 6px; border-radius:8px;">0 Logs</span>
                </div>
                <div id="winding-history-list" style="max-height:120px; overflow-y:auto; font-size:10px; color:#94a3b8;">
                    No shaft examination logs registered.
                </div>
            </div>
        `;

        container.appendChild(card);
        renderWindingLogs();
    }

    window.evaluateWindingRisk = function(val) {
        var badge = document.getElementById('winding-safety-badge');
        var select = document.getElementById('overwind-test');
        var btn = document.getElementById('submit-winding-btn');
        if (!badge) return;

        if (val.indexOf('FAIL') !== -1) {
            badge.style.background = '#7f1d1d';
            badge.style.color = '#fca5a5';
            badge.style.borderColor = '#ef4444';
            badge.innerText = '🚨 MAN-WINDING PROHIBITED: OVERWIND DEFECT (CMR 76)';
            select.style.color = '#ef4444';
            if (btn) btn.style.background = '#dc2626';
        } else {
            badge.style.background = '#14532d';
            badge.style.color = '#4ade80';
            badge.style.borderColor = '#22c55e';
            badge.innerText = '✓ WINDING SYSTEM CERTIFIED FIT';
            select.style.color = '#4ade80';
            if (btn) btn.style.background = '#0284c7';
        }
    };

    window.recordWindingAudit = function(e) {
        if (e) e.preventDefault();
        var shaft = document.getElementById('shaft-unit-id').value;
        var overwind = document.getElementById('overwind-test').value;
        var brakes = document.getElementById('brake-holding').value;
        var hook = document.getElementById('detaching-hook').value;
        var csg = document.getElementById('csg-chains').value;
        var signals = document.getElementById('shaft-signals').value;
        var engineer = document.getElementById('winding-engineer').value;

        var isBreach = (overwind.indexOf('FAIL') !== -1 || brakes.indexOf('Slippage') !== -1 || hook.indexOf('Deformed') !== -1 || csg.indexOf('Excessive') !== -1);
        var certStatus = isBreach ? 'SUSPENDED / STATUTORY GROUNDING' : 'FIT FOR MAN-HOISTING';

        var entry = {
            id: 'WIND-' + Date.now(),
            date: new Date().toLocaleDateString(),
            time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
            shaft: shaft,
            overwind: overwind,
            brakes: brakes,
            hook: hook,
            csg: csg,
            signals: signals,
            engineer: engineer,
            status: certStatus,
            seal: 'WIND-SEAL-' + Math.random().toString(36).substring(2, 8).toUpperCase()
        };

        var store = JSON.parse(localStorage.getItem('dgms_winding_logs') || '[]');
        store.unshift(entry);
        localStorage.setItem('dgms_winding_logs', JSON.stringify(store));

        renderWindingLogs();

        if (isBreach) {
            alert('🚨 CMR 74/76 PROHIBITION: Winding apparatus has statutory defects! Man-winding suspended until rectified.');
        } else {
            alert('✅ Shaft & Winding Engine Fitness Certified with Seal ' + entry.seal);
        }
    };

    function renderWindingLogs() {
        var el = document.getElementById('winding-history-list');
        var badge = document.getElementById('winding-count-badge');
        if (!el) return;
        var store = JSON.parse(localStorage.getItem('dgms_winding_logs') || '[]');

        if (badge) badge.innerText = store.length + ' Logs';

        if (store.length === 0) {
            el.innerHTML = '<div style="color:#64748b; padding:4px;">No shaft examination logs registered.</div>';
            return;
        }

        el.innerHTML = store.map(function(item) {
            var isBad = item.status.indexOf('SUSPENDED') !== -1;
            var col = isBad ? '#ef4444' : '#4ade80';
            return `
                <div style="background:#020617; border:1px solid #1e293b; padding:6px 8px; border-radius:4px; margin-bottom:4px;">
                    <div style="display:flex; justify-content:space-between; font-weight:bold;">
                        <span style="color:#38bdf8;">${item.shaft}</span>
                        <span style="font-family:monospace; color:#f59e0b; font-size:9px;">${item.seal}</span>
                    </div>
                    <div style="display:flex; justify-content:space-between; color:#cbd5e1; margin-top:2px;">
                        <span>Overwind: <b>${item.overwind.slice(0, 15)}...</b></span>
                        <span>Brakes: <b>${item.brakes.slice(0, 15)}...</b></span>
                        <span style="color:${col}; font-weight:bold;">${item.status}</span>
                    </div>
                    <div style="color:#64748b; font-size:9px; margin-top:2px;">
                        ${item.date} ${item.time} • Hook: ${item.hook.slice(0, 12)} • CSG: ${item.csg.slice(0, 12)} • Eng: ${item.engineer}
                    </div>
                </div>
            `;
        }).join('');
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', injectWindingUI);
    } else {
        injectWindingUI();
    }
    setTimeout(injectWindingUI, 3400);
})();
</script>
"""
