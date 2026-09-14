# ui_simulator.py - Standalone DGMS CMR 240/241 Pit Safety Drill & Gas Telemetry Simulator

SIMULATOR_MODULE = """
<script>
(function() {
    function injectSimulatorUI() {
        if (document.getElementById('statutory-simulator-card')) return;

        var container = document.querySelector('.grid-container') || document.body;

        var card = document.createElement('div');
        card.id = 'statutory-simulator-card';
        card.style.cssText = 'background:#0f172a; border:1px solid #334155; border-radius:10px; padding:16px; margin:14px 0; color:#f8fafc; font-family:system-ui, sans-serif; box-shadow:0 4px 6px -1px rgba(0,0,0,0.5);';

        card.innerHTML = `
            <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #1e293b; padding-bottom:10px; margin-bottom:12px;">
                <div style="display:flex; align-items:center; gap:8px;">
                    <span style="font-size:18px;">🎛️</span>
                    <div>
                        <div style="font-size:13px; font-weight:bold; color:#38bdf8;">PIT SAFETY DRILL & TELEMETRY SIMULATOR</div>
                        <div style="font-size:10px; color:#94a3b8;">CMR 2017 Reg 240/241 - Mock Evacuation Drills & Dynamic Sensor Spike Testing</div>
                    </div>
                </div>
                <div id="sim-drill-status-badge" style="background:#14532d; color:#4ade80; border:1px solid #22c55e; font-size:10px; padding:3px 8px; border-radius:12px; font-weight:bold;">
                    SIMULATOR READY (BASELINE)
                </div>
            </div>

            <!-- Telemetry Injection Panel -->
            <div style="background:#020617; border:1px solid #1e293b; border-radius:8px; padding:12px; margin-bottom:12px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                    <span style="font-size:11px; font-weight:bold; color:#cbd5e1;">Environmental Telemetry Override (Simulated Face Feed)</span>
                    <span id="sim-telemetry-warning" style="font-size:10px; color:#4ade80; font-weight:bold;">All Atmospheric Channels Normal</span>
                </div>

                <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap:10px; margin-bottom:10px;">
                    <div style="background:#0f172a; padding:8px; border-radius:6px; border:1px solid #1e293b;">
                        <div style="display:flex; justify-content:space-between; font-size:10px; color:#94a3b8;">
                            <span>CH4 Methane</span>
                            <b id="disp-sim-ch4" style="color:#4ade80;">0.20%</b>
                        </div>
                        <input type="range" id="sim-ch4" min="0" max="4.0" step="0.05" value="0.20" oninput="updateSimTelemetry()" style="width:100%; margin-top:6px;">
                    </div>
                    <div style="background:#0f172a; padding:8px; border-radius:6px; border:1px solid #1e293b;">
                        <div style="display:flex; justify-content:space-between; font-size:10px; color:#94a3b8;">
                            <span>CO Gas</span>
                            <b id="disp-sim-co" style="color:#4ade80;">2 ppm</b>
                        </div>
                        <input type="range" id="sim-co" min="0" max="60" step="1" value="2" oninput="updateSimTelemetry()" style="width:100%; margin-top:6px;">
                    </div>
                    <div style="background:#0f172a; padding:8px; border-radius:6px; border:1px solid #1e293b;">
                        <div style="display:flex; justify-content:space-between; font-size:10px; color:#94a3b8;">
                            <span>O2 Oxygen</span>
                            <b id="disp-sim-o2" style="color:#4ade80;">20.9%</b>
                        </div>
                        <input type="range" id="sim-o2" min="15.0" max="21.0" step="0.1" value="20.9" oninput="updateSimTelemetry()" style="width:100%; margin-top:6px;">
                    </div>
                    <div style="background:#0f172a; padding:8px; border-radius:6px; border:1px solid #1e293b;">
                        <div style="display:flex; justify-content:space-between; font-size:10px; color:#94a3b8;">
                            <span>Air Velocity</span>
                            <b id="disp-sim-air" style="color:#4ade80;">2.4 m/s</b>
                        </div>
                        <input type="range" id="sim-air" min="0.0" max="5.0" step="0.1" value="2.4" oninput="updateSimTelemetry()" style="width:100%; margin-top:6px;">
                    </div>
                </div>

                <!-- One-Click Drill Scenario Presets -->
                <div style="display:flex; flex-wrap:wrap; gap:6px;">
                    <button type="button" onclick="loadSimPreset('normal')" style="background:#1e293b; color:#cbd5e1; border:1px solid #334155; font-size:10px; padding:4px 8px; border-radius:4px; cursor:pointer;">
                        🔄 Normal Baseline
                    </button>
                    <button type="button" onclick="loadSimPreset('ch4_surge')" style="background:#7f1d1d; color:#fca5a5; border:1px solid #ef4444; font-size:10px; padding:4px 8px; border-radius:4px; font-weight:bold; cursor:pointer;">
                        ⚡ Methane Outburst (2.3% CH4)
                    </button>
                    <button type="button" onclick="loadSimPreset('fan_stoppage')" style="background:#78350f; color:#fde68a; border:1px solid #f59e0b; font-size:10px; padding:4px 8px; border-radius:4px; font-weight:bold; cursor:pointer;">
                        ⚠️ Main Fan Stoppage (0.0 m/s Air)
                    </button>
                    <button type="button" onclick="loadSimPreset('fire_spontaneous')" style="background:#581c87; color:#e9d5ff; border:1px solid #a855f7; font-size:10px; padding:4px 8px; border-radius:4px; font-weight:bold; cursor:pointer;">
                        🔥 Spontaneous Heating (42 ppm CO)
                    </button>
                </div>
            </div>

            <!-- Mock Evacuation Drill Execution -->
            <form id="sim-drill-form" onsubmit="recordMockDrill(event)">
                <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); gap:10px; margin-bottom:10px;">
                    <div>
                        <label style="font-size:11px; color:#94a3b8;">Drill Exercise Title</label>
                        <select id="sim-drill-type" style="width:100%; background:#020617; border:1px solid #334155; color:#38bdf8; font-weight:bold; padding:8px; border-radius:6px; font-size:11px; margin-top:4px;">
                            <option value="Quarterly Pit Evacuation Drill (CMR 240)">Quarterly Pit Evacuation Drill (CMR 240)</option>
                            <option value="Unannounced Gas Outburst Response Test">Gas Outburst Response Test</option>
                            <option value="Self-Contained Self-Rescuer (SCSR) Donning Drill">SCSR Donning Drill</option>
                            <option value="Emergency Refuge Chamber Escape Test">Refuge Chamber Escape Test</option>
                        </select>
                    </div>
                    <div>
                        <label style="font-size:11px; color:#94a3b8;">Participating Horizon / Seam</label>
                        <input type="text" id="sim-drill-zone" required placeholder="e.g. Seam 3 Bottom / East District" style="width:100%; background:#020617; border:1px solid #334155; color:#fff; padding:8px; border-radius:6px; font-size:11px; margin-top:4px;">
                    </div>
                    <div>
                        <label style="font-size:11px; color:#94a3b8;">Evacuation Commander (Safety Officer)</label>
                        <input type="text" id="sim-drill-officer" required placeholder="Name & Colliery Manager Cert" style="width:100%; background:#020617; border:1px solid #334155; color:#fff; padding:8px; border-radius:6px; font-size:11px; margin-top:4px;">
                    </div>
                </div>

                <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap:8px; margin-bottom:12px;">
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Miners Participated</span>
                        <input type="number" id="sim-miners-count" required placeholder="e.g. 42" oninput="evaluateDrillPerformance()" style="width:100%; background:transparent; border:none; color:#38bdf8; font-weight:bold; font-size:13px; margin-top:2px;">
                    </div>
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Muster Roll Headcount %</span>
                        <input type="number" id="sim-muster-pct" required placeholder="Target 100%" oninput="evaluateDrillPerformance()" style="width:100%; background:transparent; border:none; color:#4ade80; font-weight:bold; font-size:13px; margin-top:2px;">
                    </div>
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Evacuation Clearance Time</span>
                        <input type="number" step="0.5" id="sim-clearance-time" required placeholder="Minutes (Max 15)" oninput="evaluateDrillPerformance()" style="width:100%; background:transparent; border:none; color:#f59e0b; font-weight:bold; font-size:13px; margin-top:2px;">
                    </div>
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Auditory Alarm Audibility</span>
                        <select id="sim-alarm-audibility" style="width:100%; background:transparent; border:none; color:#cbd5e1; font-size:11px; margin-top:2px;">
                            <option value="Audible at 100% Blind Headings">Audible Everywhere (100%)</option>
                            <option value="Faint at Auxiliary Drift">Faint at Auxiliary Drift</option>
                            <option value="Siren Failed in Return District">⚠️ Siren Inaudible in Return</option>
                        </select>
                    </div>
                </div>

                <div id="sim-drill-eval-msg" style="background:#020617; border:1px dashed #334155; padding:8px; border-radius:6px; margin-bottom:12px; font-size:11px; color:#cbd5e1;">
                    CMR 240 Standard: Total district evacuation must complete within 15 minutes with 100% personnel muster verification.
                </div>

                <div style="display:flex; gap:8px;">
                    <button type="submit" id="submit-drill-btn" style="flex:2; background:#0284c7; color:#fff; font-weight:bold; border:none; padding:10px; border-radius:6px; font-size:12px; cursor:pointer;">
                        ⏱️ Certify Mock Drill Statutory Audit (CMR 240)
                    </button>
                    <button type="button" onclick="triggerSimulatorAlarm()" style="flex:1; background:#dc2626; color:#fff; font-weight:bold; border:none; padding:10px; border-radius:6px; font-size:12px; cursor:pointer;">
                        🚨 Test Siren & Alarm
                    </button>
                </div>
            </form>

            <!-- Drill History Archive -->
            <div style="margin-top:14px; border-top:1px solid #1e293b; padding-top:10px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                    <div style="font-size:11px; font-weight:bold; color:#cbd5e1;">Statutory Safety Mock Drill Register</div>
                    <span id="sim-drill-count-badge" style="background:#334155; color:#cbd5e1; font-size:9px; padding:2px 6px; border-radius:8px;">0 Drills</span>
                </div>
                <div id="sim-drill-history-list" style="max-height:120px; overflow-y:auto; font-size:10px; color:#94a3b8;">
                    No emergency mock drills logged in current quarter.
                </div>
            </div>
        `;

        container.appendChild(card);
        renderSimulatorLogs();
    }

    window.updateSimTelemetry = function() {
        var ch4 = parseFloat(document.getElementById('sim-ch4').value);
        var co = parseInt(document.getElementById('sim-co').value);
        var o2 = parseFloat(document.getElementById('sim-o2').value);
        var air = parseFloat(document.getElementById('sim-air').value);

        document.getElementById('disp-sim-ch4').innerText = ch4.toFixed(2) + '%';
        document.getElementById('disp-sim-co').innerText = co + ' ppm';
        document.getElementById('disp-sim-o2').innerText = o2.toFixed(1) + '%';
        document.getElementById('disp-sim-air').innerText = air.toFixed(1) + ' m/s';

        var warnEl = document.getElementById('sim-telemetry-warning');
        var badge = document.getElementById('sim-drill-status-badge');

        var isCh4Danger = ch4 >= 1.25;
        var isCoDanger = co >= 30;
        var isO2Danger = o2 < 19.0;
        var isAirDanger = air < 0.3;

        // Color coding channels
        document.getElementById('disp-sim-ch4').style.color = isCh4Danger ? '#ef4444' : (ch4 > 0.75 ? '#f59e0b' : '#4ade80');
        document.getElementById('disp-sim-co').style.color = isCoDanger ? '#ef4444' : (co > 15 ? '#f59e0b' : '#4ade80');
        document.getElementById('disp-sim-o2').style.color = isO2Danger ? '#ef4444' : '#4ade80';
        document.getElementById('disp-sim-air').style.color = isAirDanger ? '#ef4444' : '#4ade80';

        if (isCh4Danger || isCoDanger || isO2Danger || isAirDanger) {
            badge.style.background = '#7f1d1d';
            badge.style.color = '#fca5a5';
            badge.style.borderColor = '#ef4444';
            badge.innerText = '🚨 STATUTORY TELEMETRY BREACH';

            var reasons = [];
            if (isCh4Danger) reasons.push('CH4 ' + ch4.toFixed(2) + '% (>1.25%)');
            if (isCoDanger) reasons.push('CO ' + co + 'ppm (>30ppm)');
            if (isO2Danger) reasons.push('O2 Deficient ' + o2.toFixed(1) + '%');
            if (isAirDanger) reasons.push('Airflow Stagnant ' + air.toFixed(1) + 'm/s');

            warnEl.style.color = '#ef4444';
            warnEl.innerText = '⚠️ BREACH: ' + reasons.join(' | ');
        } else {
            badge.style.background = '#14532d';
            badge.style.color = '#4ade80';
            badge.style.borderColor = '#22c55e';
            badge.innerText = 'SIMULATOR READY (BASELINE)';

            warnEl.style.color = '#4ade80';
            warnEl.innerText = 'All Atmospheric Channels Normal';
        }
    };

    window.loadSimPreset = function(preset) {
        var ch4El = document.getElementById('sim-ch4');
        var coEl = document.getElementById('sim-co');
        var o2El = document.getElementById('sim-o2');
        var airEl = document.getElementById('sim-air');

        if (preset === 'normal') {
            ch4El.value = 0.20;
            coEl.value = 2;
            o2El.value = 20.9;
            airEl.value = 2.4;
        } else if (preset === 'ch4_surge') {
            ch4El.value = 2.30;
            coEl.value = 6;
            o2El.value = 20.1;
            airEl.value = 1.8;
            if (typeof window.playDGMSSiren === 'function') window.playDGMSSiren(4000);
        } else if (preset === 'fan_stoppage') {
            ch4El.value = 0.85;
            coEl.value = 8;
            o2El.value = 19.8;
            airEl.value = 0.05;
            if (typeof window.playDGMSSiren === 'function') window.playDGMSSiren(3000);
        } else if (preset === 'fire_spontaneous') {
            ch4El.value = 0.40;
            coEl.value = 42;
            o2El.value = 18.6;
            airEl.value = 1.5;
            if (typeof window.playDGMSSiren === 'function') window.playDGMSSiren(4000);
        }
        window.updateSimTelemetry();
    };

    window.triggerSimulatorAlarm = function() {
        if (typeof window.playDGMSSiren === 'function') {
            window.playDGMSSiren(8000);
            alert('🚨 DGMS Emergency Auditory Siren activated (800Hz-1200Hz sweep for 8 seconds).');
        } else {
            alert('Siren engine activated.');
        }
    };

    window.evaluateDrillPerformance = function() {
        var muster = parseFloat(document.getElementById('sim-muster-pct').value) || 0;
        var time = parseFloat(document.getElementById('sim-clearance-time').value) || 0;
        var msg = document.getElementById('sim-drill-eval-msg');
        var btn = document.getElementById('submit-drill-btn');

        if (!msg) return;

        var isFailed = (muster < 95 || time > 15);

        if (isFailed) {
            msg.innerHTML = '<span style="color:#ef4444; font-weight:bold;">DRILL SUB-STANDARD:</span> Evacuation time exceeded 15 minutes or muster accountability below 95%. Re-drill required within 7 days under CMR 240.';
            if (btn) {
                btn.style.background = '#dc2626';
                btn.innerText = '⚠️ Certify Drill (Flagged: Repeat Required)';
            }
        } else {
            msg.innerHTML = '<span style="color:#4ade80; font-weight:bold;">EXEMPLARY DRILL:</span> 100% headcount accounted for in ' + time + ' minutes. Meets DGMS Emergency Preparedness Standard.';
            if (btn) {
                btn.style.background = '#0284c7';
                btn.innerText = '⏱️ Certify Mock Drill Statutory Audit (CMR 240)';
            }
        }
    };

    window.recordMockDrill = function(e) {
        if (e) e.preventDefault();
        var drillType = document.getElementById('sim-drill-type').value;
        var zone = document.getElementById('sim-drill-zone').value;
        var officer = document.getElementById('sim-drill-officer').value;
        var miners = document.getElementById('sim-miners-count').value;
        var muster = document.getElementById('sim-muster-pct').value;
        var time = document.getElementById('sim-clearance-time').value;
        var alarm = document.getElementById('sim-alarm-audibility').value;

        var isPassed = (parseFloat(muster) >= 95 && parseFloat(time) <= 15);
        var perfText = isPassed ? 'PASSED: FULL COMPLIANCE' : 'MARGINAL: ACTION PLAN REQUIRED';

        var entry = {
            id: 'DRILL-' + Date.now(),
            date: new Date().toLocaleDateString(),
            time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
            drillType: drillType,
            zone: zone,
            officer: officer,
            miners: miners + ' personnel',
            muster: muster + '% accounted',
            clearanceTime: time + ' mins',
            alarmAudibility: alarm,
            status: perfText,
            seal: 'SIM-SEAL-' + Math.random().toString(36).substring(2, 8).toUpperCase()
        };

        var store = JSON.parse(localStorage.getItem('dgms_simulator_logs') || '[]');
        store.unshift(entry);
        localStorage.setItem('dgms_simulator_logs', JSON.stringify(store));

        document.getElementById('sim-drill-zone').value = '';
        renderSimulatorLogs();

        alert('✅ Statutory Mock Drill Recorded & Certified with Seal ' + entry.seal);
    };

    function renderSimulatorLogs() {
        var el = document.getElementById('sim-drill-history-list');
        var badge = document.getElementById('sim-drill-count-badge');
        if (!el) return;

        var store = JSON.parse(localStorage.getItem('dgms_simulator_logs') || '[]');
        if (badge) badge.innerText = store.length + ' Drills';

        if (store.length === 0) {
