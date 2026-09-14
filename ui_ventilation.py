# ui_ventilation.py - Standalone DGMS CMR 154 & 155 Statutory Ventilation Survey Engine

VENTILATION_MODULE = """
<script>
(function() {
    function injectVentilationUI() {
        if (document.getElementById('statutory-ventilation-card')) return;

        var container = document.querySelector('.grid-container') || document.body;

        var card = document.createElement('div');
        card.id = 'statutory-ventilation-card';
        card.style.cssText = 'background:#0f172a; border:1px solid #334155; border-radius:10px; padding:16px; margin:14px 0; color:#f8fafc; font-family:system-ui, sans-serif; box-shadow:0 4px 6px -1px rgba(0,0,0,0.5);';

        card.innerHTML = `
            <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #1e293b; padding-bottom:10px; margin-bottom:12px;">
                <div style="display:flex; align-items:center; gap:8px;">
                    <span style="font-size:18px;">💨</span>
                    <div>
                        <div style="font-size:13px; font-weight:bold; color:#38bdf8;">STATUTORY VENTILATION & AIR SURVEY</div>
                        <div style="font-size:10px; color:#94a3b8;">CMR 2017 Reg 154 & 155 - Airflow, Velocity & Heat Index</div>
                    </div>
                </div>
                <div id="vent-statutory-flag" style="background:#14532d; color:#4ade80; border:1px solid #22c55e; font-size:10px; padding:3px 8px; border-radius:12px; font-weight:bold;">
                    ✓ VENTILATION ADEQUATE
                </div>
            </div>

            <!-- Fast Airflow Calculation & Entry Form -->
            <form id="vent-survey-form" onsubmit="recordVentSurvey(event)">
                <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap:10px; margin-bottom:10px;">
                    <div>
                        <label style="font-size:11px; color:#94a3b8;">Air Measurement Station</label>
                        <select id="air-station" style="width:100%; background:#020617; border:1px solid #334155; color:#fff; padding:8px; border-radius:6px; font-size:11px; margin-top:4px;">
                            <option value="District 1 Face Intake Drift">District 1 Face Intake Drift</option>
                            <option value="District 1 Main Return Split">District 1 Main Return Split</option>
                            <option value="Shaft Bottom Intake Airway">Shaft Bottom Intake Airway</option>
                            <option value="Depillaring Section Last Splitting Station">Depillaring Section Last Splitting Station</option>
                            <option value="Haulage Engine Roadway">Haulage Engine Roadway</option>
                        </select>
                    </div>
                    <div>
                        <label style="font-size:11px; color:#94a3b8;">Cross Section Area (A in sq.m)</label>
                        <input type="number" step="0.1" id="roadway-area" required placeholder="e.g. 12.5" oninput="calculateAirDischarge()" style="width:100%; background:#020617; border:1px solid #334155; color:#fff; padding:8px; border-radius:6px; font-size:11px; margin-top:4px;">
                    </div>
                    <div>
                        <label style="font-size:11px; color:#94a3b8;">Air Velocity (V in m/sec)</label>
                        <input type="number" step="0.05" id="air-velocity" required placeholder="e.g. 1.2" oninput="calculateAirDischarge()" style="width:100%; background:#020617; border:1px solid #334155; color:#fff; padding:8px; border-radius:6px; font-size:11px; margin-top:4px;">
                    </div>
                </div>

                <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap:8px; margin-bottom:12px;">
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Computed Quantity (Q)</span>
                        <div id="disp-quantity" style="font-size:14px; font-weight:bold; color:#38bdf8; margin-top:3px;">0.0 m³/min</div>
                    </div>
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Dry Bulb Temp (°C)</span>
                        <input type="number" step="0.1" id="temp-dry" required placeholder="32.0" style="width:100%; background:transparent; border:none; color:#fff; font-weight:bold; font-size:13px; margin-top:2px;">
                    </div>
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Wet Bulb Temp (°C)</span>
                        <input type="number" step="0.1" id="temp-wet" required placeholder="28.5" oninput="checkWetBulbLimit(this.value)" style="width:100%; background:transparent; border:none; color:#4ade80; font-weight:bold; font-size:13px; margin-top:2px;">
                    </div>
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Statutory Surveyor</span>
                        <input type="text" id="surveyor-name" required placeholder="Overman / Cert No." style="width:100%; background:transparent; border:none; color:#cbd5e1; font-size:11px; margin-top:2px;">
                    </div>
                </div>

                <button type="submit" style="width:100%; background:#0284c7; color:#fff; font-weight:bold; border:none; padding:10px; border-radius:6px; font-size:12px; cursor:pointer;">
                    💨 Certify Ventilation Survey (CMR 154)
                </button>
            </form>

            <!-- Survey History Table -->
            <div style="margin-top:14px; border-top:1px solid #1e293b; padding-top:10px;">
                <div style="font-size:11px; font-weight:bold; color:#cbd5e1; margin-bottom:6px;">Airway Measurement Archive</div>
                <div id="vent-survey-list" style="max-height:120px; overflow-y:auto; font-size:10px; color:#94a3b8;">
                    No ventilation logs registered.
                </div>
            </div>
        `;

        container.appendChild(card);
        renderVentLogs();
    }

    window.calculateAirDischarge = function() {
        var area = parseFloat(document.getElementById('roadway-area').value) || 0;
        var vel = parseFloat(document.getElementById('air-velocity').value) || 0;
        var q_sec = area * vel;
        var q_min = q_sec * 60;
        var disp = document.getElementById('disp-quantity');
        if (disp) {
            disp.innerText = q_min.toFixed(1) + ' m³/min (' + q_sec.toFixed(2) + ' m³/s)';
        }
    };

    window.checkWetBulbLimit = function(val) {
        var wb = parseFloat(val);
        var flag = document.getElementById('vent-statutory-flag');
        var input = document.getElementById('temp-wet');
        if (isNaN(wb) || !flag) return;

        if (wb > 30.5) {
            flag.style.background = '#7f1d1d';
            flag.style.color = '#fca5a5';
            flag.style.borderColor = '#ef4444';
            flag.innerText = '⚠️ CMR 155 BREACH (>30.5°C WET BULB)';
            input.style.color = '#ef4444';
        } else {
            flag.style.background = '#14532d';
            flag.style.color = '#4ade80';
            flag.style.borderColor = '#22c55e';
            flag.innerText = '✓ VENTILATION ADEQUATE';
            input.style.color = '#4ade80';
        }
    };

    window.recordVentSurvey = function(e) {
        if (e) e.preventDefault();
        var station = document.getElementById('air-station').value;
        var area = parseFloat(document.getElementById('roadway-area').value) || 0;
        var vel = parseFloat(document.getElementById('air-velocity').value) || 0;
        var dry = parseFloat(document.getElementById('temp-dry').value) || 0;
        var wet = parseFloat(document.getElementById('temp-wet').value) || 0;
        var surveyor = document.getElementById('surveyor-name').value;
        var q = (area * vel * 60).toFixed(1);

        var compliance = (wet <= 30.5 && vel >= 0.5) ? 'Statutory Pass' : 'Breach Flagged';

        var entry = {
            id: 'VENT-' + Date.now(),
            date: new Date().toLocaleDateString(),
            time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
            station: station,
            quantity: q,
            velocity: vel,
            dry: dry,
            wet: wet,
            surveyor: surveyor,
            status: compliance,
            seal: 'VENT-SEAL-' + Math.random().toString(36).substring(2, 8).toUpperCase()
        };

        var store = JSON.parse(localStorage.getItem('dgms_vent_surveys') || '[]');
        store.unshift(entry);
        localStorage.setItem('dgms_vent_surveys', JSON.stringify(store));

        document.getElementById('roadway-area').value = '';
        document.getElementById('air-velocity').value = '';
        document.getElementById('disp-quantity').innerText = '0.0 m³/min';
        renderVentLogs();
        alert('✅ Ventilation Survey Registered with Seal ' + entry.seal);
    };

    function renderVentLogs() {
        var el = document.getElementById('vent-survey-list');
        if (!el) return;
        var store = JSON.parse(localStorage.getItem('dgms_vent_surveys') || '[]');

        if (store.length === 0) {
            el.innerHTML = '<div style="color:#64748b; padding:4px;">No ventilation survey records logged yet.</div>';
            return;
        }

        el.innerHTML = store.map(function(item) {
            var col = item.status === 'Statutory Pass' ? '#4ade80' : '#ef4444';
            return `
                <div style="background:#020617; border:1px solid #1e293b; padding:6px 8px; border-radius:4px; margin-bottom:4px;">
                    <div style="display:flex; justify-content:space-between; font-weight:bold;">
                        <span style="color:#38bdf8;">${item.station}</span>
                        <span style="font-family:monospace; color:#f59e0b; font-size:9px;">${item.seal}</span>
                    </div>
                    <div style="display:flex; justify-content:space-between; color:#cbd5e1; margin-top:2px;">
                        <span>Q: <b>${item.quantity} m³/min</b> (Vel: ${item.velocity} m/s)</span>
                        <span>Dry: ${item.dry}°C | Wet: <b>${item.wet}°C</b></span>
                        <span style="color:${col}; font-weight:bold;">${item.status}</span>
                    </div>
                    <div style="color:#64748b; font-size:9px; margin-top:2px;">
                        ${item.date} ${item.time} • Surveyor: ${item.surveyor}
                    </div>
                </div>
            `;
        }).join('');
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', injectVentilationUI);
    } else {
        injectVentilationUI();
    }
    setTimeout(injectVentilationUI, 1800);
})();
</script>
"""
