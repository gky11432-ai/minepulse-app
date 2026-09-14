# ui_inundation.py - Standalone DGMS CMR 149 & 150 Inundation & Sump Dewatering Engine

INUNDATION_MODULE = """
<script>
(function() {
    function injectInundationUI() {
        if (document.getElementById('statutory-inundation-card')) return;

        var container = document.querySelector('.grid-container') || document.body;

        var card = document.createElement('div');
        card.id = 'statutory-inundation-card';
        card.style.cssText = 'background:#0f172a; border:1px solid #334155; border-radius:10px; padding:16px; margin:14px 0; color:#f8fafc; font-family:system-ui, sans-serif; box-shadow:0 4px 6px -1px rgba(0,0,0,0.5);';

        card.innerHTML = `
            <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #1e293b; padding-bottom:10px; margin-bottom:12px;">
                <div style="display:flex; align-items:center; gap:8px;">
                    <span style="font-size:18px;">🌊</span>
                    <div>
                        <div style="font-size:13px; font-weight:bold; color:#38bdf8;">INUNDATION & WATER DANGER MONITOR</div>
                        <div style="font-size:10px; color:#94a3b8;">DGMS CMR 2017 Reg 149 & 150 - 60m Barrier Guard & Sump Dewatering</div>
                    </div>
                </div>
                <div id="inundation-risk-badge" style="background:#14532d; color:#4ade80; border:1px solid #22c55e; font-size:10px; padding:3px 8px; border-radius:12px; font-weight:bold;">
                    ✓ SAFE BARRIER (>60m)
                </div>
            </div>

            <!-- Inundation & Sump Audit Form -->
            <form id="inundation-form" onsubmit="recordInundationInspection(event)">
                <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap:10px; margin-bottom:10px;">
                    <div>
                        <label style="font-size:11px; color:#94a3b8;">Underground Sump / District</label>
                        <select id="sump-location" style="width:100%; background:#020617; border:1px solid #334155; color:#fff; padding:8px; border-radius:6px; font-size:11px; margin-top:4px;">
                            <option value="Main Dip Sump (Shaft Bottom)">Main Dip Sump (Shaft Bottom)</option>
                            <option value="District 2 Low-Lying Working Sump">District 2 Low-Lying Working Sump</option>
                            <option value="Boundary Barrier Section (Adjoining Lease)">Boundary Barrier Section (Adjoining Lease)</option>
                            <option value="Sub-Station Intermediate Sump">Sub-Station Intermediate Sump</option>
                            <option value="Drift Drainage Heading B">Drift Drainage Heading B</option>
                        </select>
                    </div>
                    <div>
                        <label style="font-size:11px; color:#94a3b8;">Barrier to Waterlogged Goaf (Meters)</label>
                        <input type="number" step="0.5" id="barrier-distance" required placeholder="e.g. 75 (Warning <60m)" oninput="evaluateInundationRisk(this.value)" style="width:100%; background:#020617; border:1px solid #334155; color:#fff; padding:8px; border-radius:6px; font-size:11px; margin-top:4px;">
                    </div>
                    <div>
                        <label style="font-size:11px; color:#94a3b8;">Current Sump Water Depth (Meters)</label>
                        <input type="number" step="0.1" id="water-depth" required placeholder="e.g. 2.4 (Max 5.0m)" oninput="evaluateSumpCapacity(this.value)" style="width:100%; background:#020617; border:1px solid #334155; color:#fff; padding:8px; border-radius:6px; font-size:11px; margin-top:4px;">
                    </div>
                </div>

                <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap:8px; margin-bottom:12px;">
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Main Pumps Running</span>
                        <select id="pumps-active" style="width:100%; background:transparent; border:none; color:#38bdf8; font-weight:bold; font-size:12px; margin-top:2px;">
                            <option value="2 Operating + 1 Standby">2 Operating + 1 Standby</option>
                            <option value="1 Operating + 2 Standby">1 Operating + 2 Standby</option>
                            <option value="All Running (Peak Monsoon)">All Running (Peak)</option>
                            <option value="Pumps Tripped / Power Off">⚠️ PUMPS TRIPPED</option>
                        </select>
                    </div>
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Pump Discharge Rate (GPM)</span>
                        <input type="number" id="pump-discharge" required placeholder="e.g. 1200 GPM" style="width:100%; background:transparent; border:none; color:#fff; font-weight:bold; font-size:13px; margin-top:2px;">
                    </div>
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Advance Pilot Boreholes</span>
                        <select id="pilot-boreholes" style="width:100%; background:transparent; border:none; color:#4ade80; font-weight:bold; font-size:11px; margin-top:2px;">
                            <option value="Tested Dry (Clear Ahead)">Tested Dry (Clear)</option>
                            <option value="Water Weeping Detected">Water Weeping</option>
                            <option value="Statutory Drilling Active">Drilling Active</option>
                        </select>
                    </div>
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Statutory Inundation Officer</span>
                        <input type="text" id="inundation-officer" required placeholder="Overman / Cert No." style="width:100%; background:transparent; border:none; color:#cbd5e1; font-size:11px; margin-top:2px;">
                    </div>
                </div>

                <button type="submit" id="submit-inundation-btn" style="width:100%; background:#0284c7; color:#fff; font-weight:bold; border:none; padding:10px; border-radius:6px; font-size:12px; cursor:pointer;">
                    💧 Certify Sump & Inundation Examination (CMR 149)
                </button>
            </form>

            <!-- Inundation Register Archive -->
            <div style="margin-top:14px; border-top:1px solid #1e293b; padding-top:10px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                    <div style="font-size:11px; font-weight:bold; color:#cbd5e1;">Inundation & Dewatering Log History</div>
                    <span id="inundation-count-badge" style="background:#334155; color:#cbd5e1; font-size:9px; padding:2px 6px; border-radius:8px;">0 Logs</span>
                </div>
                <div id="inundation-history-list" style="max-height:120px; overflow-y:auto; font-size:10px; color:#94a3b8;">
                    No inundation inspection records registered.
                </div>
            </div>
        `;

        container.appendChild(card);
        renderInundationLogs();
    }

    window.evaluateInundationRisk = function(val) {
        var dist = parseFloat(val);
        var badge = document.getElementById('inundation-risk-badge');
        var input = document.getElementById('barrier-distance');
        if (isNaN(dist) || !badge) return;

        // DGMS Regulation 149: Working within 60 meters of waterlogged area is DANGER ZONE
        if (dist <= 45.0) {
            badge.style.background = '#7f1d1d';
            badge.style.color = '#fca5a5';
            badge.style.borderColor = '#ef4444';
            badge.innerText = '🚨 CRITICAL: ADVANCE STOPPED (<45m BARRIER)';
            input.style.color = '#ef4444';
        } else if (dist <= 60.0) {
            badge.style.background = '#78350f';
            badge.style.color = '#fde68a';
            badge.style.borderColor = '#f59e0b';
            badge.innerText = '⚠️ STATUTORY WARNING: PILOT BORES MANDATORY (<60m)';
            input.style.color = '#f59e0b';
        } else {
            badge.style.background = '#14532d';
            badge.style.color = '#4ade80';
            badge.style.borderColor = '#22c55e';
            badge.innerText = '✓ SAFE BARRIER (>60m)';
            input.style.color = '#4ade80';
        }
    };

    window.evaluateSumpCapacity = function(val) {
        var depth = parseFloat(val);
        var input = document.getElementById('water-depth');
        if (isNaN(depth) || !input) return;

        if (depth >= 4.2) {
            input.style.color = '#ef4444';
        } else {
            input.style.color = '#38bdf8';
        }
    };

    window.recordInundationInspection = function(e) {
        if (e) e.preventDefault();
        var loc = document.getElementById('sump-location').value;
        var barrier = parseFloat(document.getElementById('barrier-distance').value) || 0;
        var depth = parseFloat(document.getElementById('water-depth').value) || 0;
        var pumps = document.getElementById('pumps-active').value;
        var discharge = document.getElementById('pump-discharge').value;
        var pilot = document.getElementById('pilot-boreholes').value;
        var officer = document.getElementById('inundation-officer').value;

        var status = (barrier <= 45.0 || depth >= 4.5 || pumps.indexOf('TRIPPED') !== -1) ? 'Critical' : (barrier <= 60.0 ? 'Caution' : 'Normal');

        var entry = {
            id: 'INUN-' + Date.now(),
            date: new Date().toLocaleDateString(),
            time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
            location: loc,
            barrier: barrier + ' m',
            depth: depth + ' m',
            pumps: pumps,
            discharge: discharge + ' GPM',
            pilot: pilot,
            officer: officer,
            status: status,
            seal: 'INUN-SEAL-' + Math.random().toString(36).substring(2, 8).toUpperCase()
        };

        var store = JSON.parse(localStorage.getItem('dgms_inundation_logs') || '[]');
        store.unshift(entry);
        localStorage.setItem('dgms_inundation_logs', JSON.stringify(store));

        document.getElementById('barrier-distance').value = '';
        document.getElementById('water-depth').value = '';
        document.getElementById('pump-discharge').value = '';
        renderInundationLogs();
        alert('✅ Inundation Safety Record Certified with Authority Seal ' + entry.seal);
    };

    function renderInundationLogs() {
        var el = document.getElementById('inundation-history-list');
        var badge = document.getElementById('inundation-count-badge');
        if (!el) return;
        var store = JSON.parse(localStorage.getItem('dgms_inundation_logs') || '[]');

        if (badge) badge.innerText = store.length + ' Logs';

        if (store.length === 0) {
            el.innerHTML = '<div style="color:#64748b; padding:4px;">No inundation inspection records registered.</div>';
            return;
        }

        el.innerHTML = store.map(function(item) {
            var color = (item.status === 'Critical') ? '#ef4444' : (item.status === 'Caution' ? '#f59e0b' : '#4ade80');
            return `
                <div style="background:#020617; border:1px solid #1e293b; padding:6px 8px; border-radius:4px; margin-bottom:4px;">
                    <div style="display:flex; justify-content:space-between; font-weight:bold;">
                        <span style="color:#38bdf8;">${item.location}</span>
                        <span style="font-family:monospace; color:#f59e0b; font-size:9px;">${item.seal}</span>
                    </div>
                    <div style="display:flex; justify-content:space-between; color:#cbd5e1; margin-top:2px;">
                        <span>Barrier: <b style="color:${color};">${item.barrier}</b> | Sump Depth: <b>${item.depth}</b></span>
                        <span>Discharge: <b>${item.discharge}</b></span>
                        <span style="color:${color}; font-weight:bold;">${item.status}</span>
                    </div>
                    <div style="color:#64748b; font-size:9px; margin-top:2px;">
                        ${item.date} ${item.time} • Pilot Bores: ${item.pilot} • Pumps: ${item.pumps} • Officer: ${item.officer}
                    </div>
                </div>
            `;
        }).join('');
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', injectInundationUI);
    } else {
        injectInundationUI();
    }
    setTimeout(injectInundationUI, 2400);
})();
</script>
"""
