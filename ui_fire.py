# ui_fire.py - Standalone DGMS CMR 137-148 Spontaneous Combustion & Isolation Stoppings Engine

FIRE_MODULE = """
<script>
(function() {
    function injectFireUI() {
        if (document.getElementById('statutory-fire-card')) return;

        var container = document.querySelector('.grid-container') || document.body;

        var card = document.createElement('div');
        card.id = 'statutory-fire-card';
        card.style.cssText = 'background:#0f172a; border:1px solid #334155; border-radius:10px; padding:16px; margin:14px 0; color:#f8fafc; font-family:system-ui, sans-serif; box-shadow:0 4px 6px -1px rgba(0,0,0,0.5);';

        card.innerHTML = `
            <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #1e293b; padding-bottom:10px; margin-bottom:12px;">
                <div style="display:flex; align-items:center; gap:8px;">
                    <span style="font-size:18px;">🔥</span>
                    <div>
                        <div style="font-size:13px; font-weight:bold; color:#ef4444;">SPONTANEOUS HEATING & ISOLATION STOPPINGS</div>
                        <div style="font-size:10px; color:#94a3b8;">DGMS CMR 2017 Reg 137-148 - Graham's Ratio & Sealed-off Goaf Audit</div>
                    </div>
                </div>
                <div id="fire-statutory-badge" style="background:#14532d; color:#4ade80; border:1px solid #22c55e; font-size:10px; padding:3px 8px; border-radius:12px; font-weight:bold;">
                    ✓ SEAL STABLE (NO HEATING)
                </div>
            </div>

            <!-- Isolation Stopping Sampling & Graham's Ratio Form -->
            <form id="fire-stopping-form" onsubmit="recordFireInspection(event)">
                <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap:10px; margin-bottom:10px;">
                    <div>
                        <label style="font-size:11px; color:#94a3b8;">Isolation Stopping (Seal No.)</label>
                        <select id="stopping-no" style="width:100%; background:#020617; border:1px solid #334155; color:#fff; padding:8px; border-radius:6px; font-size:11px; margin-top:4px;">
                            <option value="Stopping No. S-12 (District 1 Goaf)">Stopping No. S-12 (District 1 Goaf)</option>
                            <option value="Stopping No. S-15 (Depillared Panel A)">Stopping No. S-15 (Depillared Panel A)</option>
                            <option value="Stopping No. S-04 (Old Seam Workings)">Stopping No. S-04 (Old Seam Workings)</option>
                            <option value="Explosion-Proof Bulkhead B-01">Explosion-Proof Bulkhead B-01</option>
                            <option value="Return Stopping S-22 (Sealed Horizon)">Return Stopping S-22 (Sealed Horizon)</option>
                        </select>
                    </div>
                    <div>
                        <label style="font-size:11px; color:#94a3b8;">Carbon Monoxide (CO in PPM)</label>
                        <input type="number" step="1" id="stopping-co" required placeholder="Behind Seal (e.g. 15)" oninput="computeGrahamsRatio()" style="width:100%; background:#020617; border:1px solid #334155; color:#fff; padding:8px; border-radius:6px; font-size:11px; margin-top:4px;">
                    </div>
                    <div>
                        <label style="font-size:11px; color:#94a3b8;">Oxygen Deficiency (% O2 in Goaf)</label>
                        <input type="number" step="0.1" id="stopping-o2" required placeholder="e.g. 14.5% (Fresh 20.93%)" oninput="computeGrahamsRatio()" style="width:100%; background:#020617; border:1px solid #334155; color:#fff; padding:8px; border-radius:6px; font-size:11px; margin-top:4px;">
                    </div>
                </div>

                <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap:8px; margin-bottom:12px;">
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Graham's Ratio (G.R.)</span>
                        <div id="disp-grahams-ratio" style="font-size:14px; font-weight:bold; color:#4ade80; margin-top:3px;">0.00 (Normal)</div>
                    </div>
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Seal Temperature (°C)</span>
                        <input type="number" step="0.5" id="stopping-temp" required placeholder="Behind pipe (°C)" style="width:100%; background:transparent; border:none; color:#fff; font-weight:bold; font-size:13px; margin-top:2px;">
                    </div>
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Diff. Pressure (Water Gauge)</span>
                        <select id="water-gauge-status" style="width:100%; background:transparent; border:none; color:#38bdf8; font-weight:bold; font-size:11px; margin-top:2px;">
                            <option value="+5 mm WG (Outbreathing)">+5 mm WG (Outbreathing)</option>
                            <option value="-4 mm WG (Inbreathing Danger)">-4 mm WG (Inbreathing)</option>
                            <option value="0 mm WG (Equilibrium)">0 mm WG (Neutral)</option>
                        </select>
                    </div>
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Ventilation Officer / Chemist</span>
                        <input type="text" id="stopping-officer" required placeholder="Name & Cert No." style="width:100%; background:transparent; border:none; color:#cbd5e1; font-size:11px; margin-top:2px;">
                    </div>
                </div>

                <div style="display:grid; grid-template-columns: 1fr 1fr; gap:8px; margin-bottom:12px;">
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Stopping Plaster & Cracking Inspection</span>
                        <select id="plaster-condition" style="width:100%; background:transparent; border:none; color:#4ade80; font-weight:bold; font-size:11px; margin-top:2px;">
                            <option value="Intact / Air-Tight (White-Washed)">Intact / Air-Tight (White-Washed)</option>
                            <option value="Hairline Cracks Resealed">Hairline Cracks Resealed</option>
                            <option value="Air Leakage Detected">⚠️ Air Leakage Detected</option>
                        </select>
                    </div>
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">CH4 Behind Seal (%)</span>
                        <input type="number" step="0.1" id="stopping-ch4" required placeholder="e.g. 18.5% (Extinctive)" style="width:100%; background:transparent; border:none; color:#fff; font-weight:bold; font-size:13px; margin-top:2px;">
                    </div>
                </div>

                <button type="submit" id="submit-fire-btn" style="width:100%; background:#dc2626; color:#fff; font-weight:bold; border:none; padding:10px; border-radius:6px; font-size:12px; cursor:pointer;">
                    🔥 Certify Stopping Examination & Heating Index (CMR 144)
                </button>
            </form>

            <!-- Fire & Stopping History Register Archive -->
            <div style="margin-top:14px; border-top:1px solid #1e293b; padding-top:10px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                    <div style="font-size:11px; font-weight:bold; color:#cbd5e1;">Isolation Stopping Inspection Register (CMR 144 Log)</div>
                    <span id="fire-count-badge" style="background:#334155; color:#cbd5e1; font-size:9px; padding:2px 6px; border-radius:8px;">0 Inspections</span>
                </div>
                <div id="fire-history-list" style="max-height:120px; overflow-y:auto; font-size:10px; color:#94a3b8;">
                    No isolation stopping records registered.
                </div>
            </div>
        `;

        container.appendChild(card);
        renderFireLogs();
    }

    // Graham's Ratio Calculator: G.R. = (CO formed in % / O2 absorbed in %) * 100
    // Simplified DGMS Practical Formula: [ CO (ppm) / (0.265 * N2 - O2) ]
    window.computeGrahamsRatio = function() {
        var coPpm = parseFloat(document.getElementById('stopping-co').value) || 0;
        var o2Measured = parseFloat(document.getElementById('stopping-o2').value) || 20.9;
        var disp = document.getElementById('disp-grahams-ratio');
        var badge = document.getElementById('fire-statutory-badge');
        var btn = document.getElementById('submit-fire-btn');

        var o2Deficiency = 20.93 - o2Measured;
        if (o2Deficiency <= 0.1) o2Deficiency = 0.1; // Avoid division by zero

        var coPercent = coPpm / 10000.0;
        var gr = (coPercent / o2Deficiency) * 100.0;

        if (coPpm === 0) gr = 0.0;

        if (disp) {
            disp.innerText = gr.toFixed(2) + ' ';
        }

        if (!badge) return;

        if (gr >= 1.0 || coPpm > 100) {
            badge.style.background = '#7f1d1d';
            badge.style.color = '#fca5a5';
            badge.style.borderColor = '#ef4444';
            badge.innerText = '🚨 ACTIVE FIRE / HEATING IN GOAF (G.R. ≥ 1.0)';
            if (disp) { disp.innerText += '(ACTIVE FIRE)'; disp.style.color = '#ef4444'; }
            if (btn) btn.style.background = '#b91c1c';
        } else if (gr >= 0.5 || coPpm > 30) {
            badge.style.background = '#78350f';
            badge.style.color = '#fde68a';
            badge.style.borderColor = '#f59e0b';
            badge.innerText = '⚠️ INCIPIENT HEATING DETECTED (G.R. 0.5 - 1.0)';
            if (disp) { disp.innerText += '(INCIPIENT HEATING)'; disp.style.color = '#f59e0b'; }
            if (btn) btn.style.background = '#d97706';
        } else {
            badge.style.background = '#14532d';
            badge.style.color = '#4ade80';
            badge.style.borderColor = '#22c55e';
            badge.innerText = '✓ SEAL STABLE (NO HEATING)';
            if (disp) { disp.innerText += '(Normal)'; disp.style.color = '#4ade80'; }
            if (btn) btn.style.background = '#dc2626';
        }
    };

    window.recordFireInspection = function(e) {
        if (e) e.preventDefault();
        var stopping = document.getElementById('stopping-no').value;
        var co = document.getElementById('stopping-co').value;
        var o2 = document.getElementById('stopping-o2').value;
        var ch4 = document.getElementById('stopping-ch4').value;
        var temp = document.getElementById('stopping-temp').value;
        var wg = document.getElementById('water-gauge-status').value;
        var plaster = document.getElementById('plaster-condition').value;
        var officer = document.getElementById('stopping-officer').value;
        var grText = document.getElementById('disp-grahams-ratio').innerText;

        var isAlert = (grText.indexOf('ACTIVE') !== -1 || grText.indexOf('INCIPIENT') !== -1);
        var certStatus = isAlert ? 'SPONTANEOUS HEATING ALERT' : 'NORMAL / EXTINCTIVE ATMOSPHERE';

        var entry = {
            id: 'FIRE-' + Date.now(),
            date: new Date().toLocaleDateString(),
            time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
            stopping: stopping,
            co: co + ' PPM',
            o2: o2 + '%',
            ch4: ch4 + '%',
            gr: grText,
            temp: temp + ' °C',
            wg: wg,
            plaster: plaster,
            officer: officer,
            status: certStatus,
            seal: 'FIRE-SEAL-' + Math.random().toString(36).substring(2, 8).toUpperCase()
        };

        var store = JSON.parse(localStorage.getItem('dgms_fire_logs') || '[]');
        store.unshift(entry);
        localStorage.setItem('dgms_fire_logs', JSON.stringify(store));

        document.getElementById('stopping-co').value = '';
        document.getElementById('stopping-o2').value = '';
        document.getElementById('disp-grahams-ratio').innerText = '0.00 (Normal)';
        renderFireLogs();

        if (isAlert) {
            alert('🚨 STATUTORY FIRE ALERT: Graham\\'s ratio indicates spontaneous heating in sealed goaf! CMR 144 action initiated.');
        } else {
            alert('✅ Isolation Stopping Inspection Certified with Seal ' + entry.seal);
        }
    };

    function renderFireLogs() {
        var el = document.getElementById('fire-history-list');
        var badge = document.getElementById('fire-count-badge');
        if (!el) return;
        var store = JSON.parse(localStorage.getItem('dgms_fire_logs') || '[]');

        if (badge) badge.innerText = store.length + ' Inspections';

        if (store.length === 0) {
            el.innerHTML = '<div style="color:#64748b; padding:4px;">No isolation stopping records registered.</div>';
            return;
        }

        el.innerHTML = store.map(function(item) {
            var isBad = item.status.indexOf('ALERT') !== -1;
            var col = isBad ? '#ef4444' : '#4ade80';
            return `
                <div style="background:#020617; border:1px solid #1e293b; padding:6px 8px; border-radius:4px; margin-bottom:4px;">
                    <div style="display:flex; justify-content:space-between; font-weight:bold;">
                        <span style="color:#ef4444;">${item.stopping}</span>
                        <span style="font-family:monospace; color:#f59e0b; font-size:9px;">${item.seal}</span>
                    </div>
                    <div style="display:flex; justify-content:space-between; color:#cbd5e1; margin-top:2px;">
                        <span>CO: <b>${item.co}</b> | O2: <b>${item.o2}</b> | CH4: <b>${item.ch4}</b></span>
                        <span style="color:${col}; font-weight:bold;">${item.status}</span>
                    </div>
                    <div style="color:#94a3b8; font-size:9px; margin-top:2px;">
                        G.R.: <b style="color:${col};">${item.gr}</b> • Temp: ${item.temp} • WG: ${item.wg} • Insp: ${item.officer}
                    </div>
                </div>
            `;
        }).join('');
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', injectFireUI);
    } else {
        injectFireUI();
    }
    setTimeout(injectFireUI, 3000);
})();
</script>
"""
