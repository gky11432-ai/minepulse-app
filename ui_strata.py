# ui_strata.py - Standalone DGMS CMR 123 Support Management Plan (SMP) & Roof Convergence Engine

STRATA_MODULE = """
<script>
(function() {
    function injectStrataUI() {
        if (document.getElementById('statutory-strata-card')) return;

        var container = document.querySelector('.grid-container') || document.body;

        var card = document.createElement('div');
        card.id = 'statutory-strata-card';
        card.style.cssText = 'background:#0f172a; border:1px solid #334155; border-radius:10px; padding:16px; margin:14px 0; color:#f8fafc; font-family:system-ui, sans-serif; box-shadow:0 4px 6px -1px rgba(0,0,0,0.5);';

        card.innerHTML = `
            <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #1e293b; padding-bottom:10px; margin-bottom:12px;">
                <div style="display:flex; align-items:center; gap:8px;">
                    <span style="font-size:18px;">🏗️</span>
                    <div>
                        <div style="font-size:13px; font-weight:bold; color:#38bdf8;">SUPPORT MANAGEMENT PLAN (SMP) & ROOF CONTROL</div>
                        <div style="font-size:10px; color:#94a3b8;">DGMS CMR 2017 Reg 123 - Tell-Tale Convergence & Roof Bolt Audit</div>
                    </div>
                </div>
                <div id="strata-condition-badge" style="background:#14532d; color:#4ade80; border:1px solid #22c55e; font-size:10px; padding:3px 8px; border-radius:12px; font-weight:bold;">
                    ✓ STRATA STABLE (NORMAL)
                </div>
            </div>

            <!-- Strata Convergence Logging Form -->
            <form id="strata-audit-form" onsubmit="recordStrataInspection(event)">
                <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap:10px; margin-bottom:10px;">
                    <div>
                        <label style="font-size:11px; color:#94a3b8;">Convergence Station / Junction</label>
                        <select id="strata-location" style="width:100%; background:#020617; border:1px solid #334155; color:#fff; padding:8px; border-radius:6px; font-size:11px; margin-top:4px;">
                            <option value="Junction 4 / 2nd East Heading">Junction 4 / 2nd East Heading</option>
                            <option value="Depillaring Slice Face 2B">Depillaring Slice Face 2B</option>
                            <option value="Main Dip Airway Station TT-09">Main Dip Airway Station TT-09</option>
                            <option value="Belt Conveyor Transfer Drift">Belt Conveyor Transfer Drift</option>
                            <option value="Longwall Gate Roadway G-1">Longwall Gate Roadway G-1</option>
                        </select>
                    </div>
                    <div>
                        <label style="font-size:11px; color:#94a3b8;">Tell-Tale Lower Anchor (<2m) (mm)</label>
                        <input type="number" step="0.5" id="tell-tale-lower" required placeholder="e.g. 2.0" oninput="evaluateStrataRisk()" style="width:100%; background:#020617; border:1px solid #334155; color:#fff; padding:8px; border-radius:6px; font-size:11px; margin-top:4px;">
                    </div>
                    <div>
                        <label style="font-size:11px; color:#94a3b8;">Tell-Tale Upper Anchor (>4m) (mm)</label>
                        <input type="number" step="0.5" id="tell-tale-upper" required placeholder="e.g. 1.0" oninput="evaluateStrataRisk()" style="width:100%; background:#020617; border:1px solid #334155; color:#fff; padding:8px; border-radius:6px; font-size:11px; margin-top:4px;">
                    </div>
                </div>

                <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap:8px; margin-bottom:12px;">
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Total Convergence</span>
                        <div id="disp-total-convergence" style="font-size:14px; font-weight:bold; color:#38bdf8; margin-top:3px;">0.0 mm</div>
                    </div>
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Roof Bolt Torque (Nm)</span>
                        <input type="number" id="bolt-torque" required placeholder="Min 120 Nm" style="width:100%; background:transparent; border:none; color:#fff; font-weight:bold; font-size:13px; margin-top:2px;">
                    </div>
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Side Spalling / Sloughing</span>
                        <select id="spalling-check" style="width:100%; background:transparent; border:none; color:#4ade80; font-weight:bold; font-size:11px; margin-top:2px;">
                            <option value="None / Sound Ribs">None (Sound Ribs)</option>
                            <option value="Minor Flaking (<50mm)">Minor Flaking</option>
                            <option value="Severe Guttering / Crack">Severe Guttering</option>
                        </select>
                    </div>
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Inspecting Overman</span>
                        <input type="text" id="strata-inspector" required placeholder="Name & Cert No." style="width:100%; background:transparent; border:none; color:#cbd5e1; font-size:11px; margin-top:2px;">
                    </div>
                </div>

                <button type="submit" id="submit-strata-btn" style="width:100%; background:#0284c7; color:#fff; font-weight:bold; border:none; padding:10px; border-radius:6px; font-size:12px; cursor:pointer;">
                    🛡️ Log Strata & Roof Bolt Examination (CMR 123)
                </button>
            </form>

            <!-- Strata Registry Log Table -->
            <div style="margin-top:14px; border-top:1px solid #1e293b; padding-top:10px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                    <div style="font-size:11px; font-weight:bold; color:#cbd5e1;">Strata Monitoring Register (Form-V SMP Log)</div>
                    <span id="strata-count-badge" style="background:#334155; color:#cbd5e1; font-size:9px; padding:2px 6px; border-radius:8px;">0 Logs</span>
                </div>
                <div id="strata-history-list" style="max-height:120px; overflow-y:auto; font-size:10px; color:#94a3b8;">
                    No strata convergence records logged.
                </div>
            </div>
        `;

        container.appendChild(card);
        renderStrataLogs();
    }

    window.evaluateStrataRisk = function() {
        var lower = parseFloat(document.getElementById('tell-tale-lower').value) || 0;
        var upper = parseFloat(document.getElementById('tell-tale-upper').value) || 0;
        var total = lower + upper;

        var disp = document.getElementById('disp-total-convergence');
        var badge = document.getElementById('strata-condition-badge');
        if (disp) disp.innerText = total.toFixed(1) + ' mm';

        if (!badge) return;

        if (total >= 10.0 || lower >= 8.0) {
            badge.style.background = '#7f1d1d';
            badge.style.color = '#fca5a5';
            badge.style.borderColor = '#ef4444';
            badge.innerText = '🚨 RED ALERT: WITHDRAW MEN (CMR 123)';
            if (disp) disp.style.color = '#ef4444';
        } else if (total >= 5.0 || lower >= 4.0) {
            badge.style.background = '#78350f';
            badge.style.color = '#fde68a';
            badge.style.borderColor = '#f59e0b';
            badge.innerText = '⚠️ AMBER: EXTRA SUPPORTS MANDATORY';
            if (disp) disp.style.color = '#f59e0b';
        } else {
            badge.style.background = '#14532d';
            badge.style.color = '#4ade80';
            badge.style.borderColor = '#22c55e';
            badge.innerText = '✓ STRATA STABLE (NORMAL)';
            if (disp) disp.style.color = '#38bdf8';
        }
    };

    window.recordStrataInspection = function(e) {
        if (e) e.preventDefault();
        var loc = document.getElementById('strata-location').value;
        var lower = parseFloat(document.getElementById('tell-tale-lower').value) || 0;
        var upper = parseFloat(document.getElementById('tell-tale-upper').value) || 0;
        var total = (lower + upper).toFixed(1);
        var torque = document.getElementById('bolt-torque').value;
        var spalling = document.getElementById('spalling-check').value;
        var inspector = document.getElementById('strata-inspector').value;

        var alertLevel = (total >= 10.0) ? 'Critical' : (total >= 5.0 ? 'Warning' : 'Normal');

        var entry = {
            id: 'SMP-' + Date.now(),
            date: new Date().toLocaleDateString(),
            time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
            location: loc,
            totalConv: total + ' mm',
            lower: lower + ' mm',
            upper: upper + ' mm',
            torque: torque + ' Nm',
            spalling: spalling,
            inspector: inspector,
            level: alertLevel,
            seal: 'SMP-SEAL-' + Math.random().toString(36).substring(2, 8).toUpperCase()
        };

        var store = JSON.parse(localStorage.getItem('dgms_strata_logs') || '[]');
        store.unshift(entry);
        localStorage.setItem('dgms_strata_logs', JSON.stringify(store));

        document.getElementById('tell-tale-lower').value = '';
        document.getElementById('tell-tale-upper').value = '';
        document.getElementById('disp-total-convergence').innerText = '0.0 mm';
        renderStrataLogs();
        alert('✅ Strata Convergence Record Certified with Seal ' + entry.seal);
    };

    function renderStrataLogs() {
        var el = document.getElementById('strata-history-list');
        var badge = document.getElementById('strata-count-badge');
        if (!el) return;
        var store = JSON.parse(localStorage.getItem('dgms_strata_logs') || '[]');

        if (badge) badge.innerText = store.length + ' Logs';

        if (store.length === 0) {
            el.innerHTML = '<div style="color:#64748b; padding:4px;">No strata convergence records logged.</div>';
            return;
        }

        el.innerHTML = store.map(function(item) {
            var color = (item.level === 'Critical') ? '#ef4444' : (item.level === 'Warning' ? '#f59e0b' : '#4ade80');
            return `
                <div style="background:#020617; border:1px solid #1e293b; padding:6px 8px; border-radius:4px; margin-bottom:4px;">
                    <div style="display:flex; justify-content:space-between; font-weight:bold;">
                        <span style="color:#38bdf8;">${item.location}</span>
                        <span style="font-family:monospace; color:#f59e0b; font-size:9px;">${item.seal}</span>
                    </div>
                    <div style="display:flex; justify-content:space-between; color:#cbd5e1; margin-top:2px;">
                        <span>Conv: <b style="color:${color};">${item.totalConv}</b> (L:${item.lower} / U:${item.upper})</span>
                        <span>Bolt Torque: <b>${item.torque}</b></span>
                        <span style="color:${color}; font-weight:bold;">${item.level}</span>
                    </div>
                    <div style="color:#64748b; font-size:9px; margin-top:2px;">
                        ${item.date} ${item.time} • Rib Status: ${item.spalling} • Officer: ${item.inspector}
                    </div>
                </div>
            `;
        }).join('');
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', injectStrataUI);
    } else {
        injectStrataUI();
    }
    setTimeout(injectStrataUI, 2200);
})();
</script>
"""
