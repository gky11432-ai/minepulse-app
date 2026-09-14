# ui_alerts.py - Standalone DGMS CMR 153 & 106 Automated Threshold & Emergency Evacuation Engine

ALERTS_MODULE = """
<script>
(function() {
    var CH4_TRIP_LIMIT = 1.25;  // CMR 2017 Regulation 153 statutory limit (%)
    var CO_WARN_LIMIT = 50.0;    // Carbon Monoxide dangerous threshold (PPM)
    var TILT_WARN_LIMIT = 4.5;   // Highwall bench deformation limit (mm)
    var isEmergencyActive = false;

    function injectAlertsUI() {
        if (document.getElementById('statutory-alerts-card')) return;

        var container = document.querySelector('.grid-container') || document.body;

        var card = document.createElement('div');
        card.id = 'statutory-alerts-card';
        card.style.cssText = 'background:#0f172a; border:1px solid #334155; border-radius:10px; padding:16px; margin:14px 0; color:#f8fafc; font-family:system-ui, sans-serif; box-shadow:0 4px 6px -1px rgba(0,0,0,0.5);';

        card.innerHTML = `
            <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #1e293b; padding-bottom:10px; margin-bottom:12px;">
                <div style="display:flex; align-items:center; gap:8px;">
                    <span style="font-size:18px;">⚠️</span>
                    <div>
                        <div style="font-size:13px; font-weight:bold; color:#ef4444;">DGMS STATUTORY THRESHOLD MONITOR</div>
                        <div style="font-size:10px; color:#94a3b8;">Autonomous CMR 153 Trip & CMR 106 Strata Guard</div>
                    </div>
                </div>
                <div id="grid-trip-status" style="background:#14532d; color:#4ade80; border:1px solid #22c55e; font-size:10px; padding:3px 8px; border-radius:12px; font-weight:bold;">
                    ⚡ PIT POWER: ENERGIZED (NORMAL)
                </div>
            </div>

            <!-- Real-time Threshold Indicators -->
            <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap:10px; margin-bottom:12px;">
                <div style="background:#020617; border:1px solid #1e293b; padding:10px; border-radius:6px; text-align:center;">
                    <div style="font-size:10px; color:#94a3b8;">CH4 Cutoff Rule</div>
                    <div style="font-size:15px; font-weight:bold; color:#f59e0b; margin-top:2px;">> 1.25%</div>
                    <div style="font-size:9px; color:#64748b;">CMR 153 Mandate</div>
                </div>
                <div style="background:#020617; border:1px solid #1e293b; padding:10px; border-radius:6px; text-align:center;">
                    <div style="font-size:10px; color:#94a3b8;">CO Gas Hazard</div>
                    <div style="font-size:15px; font-weight:bold; color:#f59e0b; margin-top:2px;">> 50 PPM</div>
                    <div style="font-size:9px; color:#64748b;">Spontaneous Comb.</div>
                </div>
                <div style="background:#020617; border:1px solid #1e293b; padding:10px; border-radius:6px; text-align:center;">
                    <div style="font-size:10px; color:#94a3b8;">Strata Displacement</div>
                    <div style="font-size:15px; font-weight:bold; color:#f59e0b; margin-top:2px;">> 4.5 mm</div>
                    <div style="font-size:9px; color:#64748b;">CMR 106 Bench Guard</div>
                </div>
            </div>

            <!-- Manual Drill & Emergency Test Controls -->
            <div style="display:flex; gap:8px; margin-bottom:12px;">
                <button type="button" onclick="simulateMethaneExceedance()" style="flex:1; background:#7f1d1d; color:#fca5a5; border:1px solid #ef4444; padding:8px; border-radius:6px; font-size:11px; font-weight:bold; cursor:pointer;">
                    💥 Test CH4 Trip (>1.25%)
                </button>
                <button type="button" onclick="simulateStrataInstability()" style="flex:1; background:#78350f; color:#fde68a; border:1px solid #f59e0b; padding:8px; border-radius:6px; font-size:11px; font-weight:bold; cursor:pointer;">
                    🏔️ Test Strata Shear
                </button>
                <button type="button" onclick="resetStatutoryEmergency()" style="background:#1e293b; color:#94a3b8; border:1px solid #475569; padding:8px 12px; border-radius:6px; font-size:11px; cursor:pointer;">
                    🔄 Reset Normal
                </button>
            </div>

            <!-- Dangerous Occurrences Incident Register -->
            <div style="border-top:1px solid #1e293b; padding-top:10px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                    <div style="font-size:11px; font-weight:bold; color:#cbd5e1;">Statutory Incident Log (CMR Reg 8)</div>
                    <span id="incident-count-badge" style="background:#334155; color:#cbd5e1; font-size:9px; padding:2px 6px; border-radius:8px;">0 Events</span>
                </div>
                <div id="statutory-incidents-list" style="max-height:100px; overflow-y:auto; font-size:10px; color:#94a3b8;">
                    No regulatory exceedance breaches recorded.
                </div>
            </div>
        `;

        container.appendChild(card);
        renderIncidents();
    }

    // Telemetry Sensor Reader Loop
    function monitorTelemetryElements() {
        if (isEmergencyActive) return;

        var textNodes = document.body.innerText || "";
        
        // Dynamic Methane Checker
        var ch4Match = textNodes.match(/CH4[:\s]+([0-9.]+)\s*%/i) || textNodes.match(/Methane[:\s]+([0-9.]+)\s*%/i);
        if (ch4Match && parseFloat(ch4Match[1]) >= CH4_TRIP_LIMIT) {
            triggerBreachEmergency("CMR 153: Methane Concentration Exceeded", parseFloat(ch4Match[1]) + "%", "ELECTRICAL_TRIP");
        }

        // Dynamic Carbon Monoxide Checker
        var coMatch = textNodes.match(/CO[:\s]+([0-9.]+)\s*ppm/i) || textNodes.match(/Carbon Monoxide[:\s]+([0-9.]+)\s*ppm/i);
        if (coMatch && parseFloat(coMatch[1]) >= CO_WARN_LIMIT) {
            triggerBreachEmergency("Spontaneous Combustion: High CO Level", parseFloat(coMatch[1]) + " PPM", "TOXIC_GAS_ALERT");
        }
    }

    // Statutory Emergency Routine
    window.triggerBreachEmergency = function(reason, measuredVal, actionType) {
        if (isEmergencyActive) return;
        isEmergencyActive = true;

        // Sound / Siren Engagement
        if (typeof window.playDGMSSiren === 'function') {
            window.playDGMSSiren(15000);
        } else if (typeof window.triggerAlarm === 'function') {
            window.triggerAlarm();
        } else if (navigator.vibrate) {
            navigator.vibrate([1000, 300, 1000, 300, 2000]);
        }

        // Update UI Power Trip Status
        var tripBadge = document.getElementById('grid-trip-status');
        if (tripBadge) {
            tripBadge.style.background = '#7f1d1d';
            tripBadge.style.color = '#fecaca';
            tripBadge.style.borderColor = '#ef4444';
            tripBadge.innerHTML = '🚨 SECTION POWER TRIPPED (ISOLATED)';
        }

        // Flashing Warning Banner
        var banner = document.createElement('div');
        banner.id = 'statutory-emergency-overlay';
        banner.style.cssText = 'position:fixed; top:0; left:0; width:100vw; background:#dc2626; color:#ffffff; font-family:sans-serif; text-align:center; padding:12px; z-index:9999999; font-weight:bold; font-size:13px; box-shadow:0 4px 12px rgba(0,0,0,0.8);';
        banner.innerHTML = `
            🚨 DGMS CMR 153 STATUTORY EVACUATION DIRECTIVE 🚨<br>
            <span style="font-size:11px; font-weight:normal;">Breach: ${reason} (Value: ${measuredVal}) | All underground personnel withdraw to intake drift immediately.</span>
            <button onclick="document.getElementById('statutory-emergency-overlay').remove()" style="margin-left:14px; background:#000; color:#fff; border:none; padding:4px 10px; border-radius:4px; cursor:pointer; font-size:10px;">Acknowledge</button>
        `;
        document.body.appendChild(banner);

        // Store into Incident Ledger
        logDangerousOccurrence(reason, measuredVal, actionType);
    };

    function logDangerousOccurrence(title, value, action) {
        var logs = JSON.parse(localStorage.getItem('dgms_incidents') || '[]');
        var entry = {
            id: 'INC-' + Date.now(),
            time: new Date().toLocaleTimeString(),
            date: new Date().toLocaleDateString(),
            title: title,
            val: value,
            action: action,
            seal: 'INC-SEAL-' + Math.random().toString(36).substring(2, 8).toUpperCase()
        };
        logs.unshift(entry);
        localStorage.setItem('dgms_incidents', JSON.stringify(logs));
        renderIncidents();
    }

    function renderIncidents() {
        var el = document.getElementById('statutory-incidents-list');
        var badge = document.getElementById('incident-count-badge');
        if (!el) return;

        var logs = JSON.parse(localStorage.getItem('dgms_incidents') || '[]');
        if (badge) badge.innerText = logs.length + ' Events';

        if (logs.length === 0) {
            el.innerHTML = '<div style="color:#64748b; padding:4px;">No regulatory exceedance breaches recorded.</div>';
            return;
        }

        el.innerHTML = logs.map(function(item) {
            return `
                <div style="background:#020617; border:1px solid #334155; padding:6px; border-radius:4px; margin-bottom:4px;">
                    <div style="display:flex; justify-content:space-between; color:#ef4444; font-weight:bold;">
                        <span>${item.title} (${item.val})</span>
                        <span style="font-family:monospace; color:#f59e0b; font-size:9px;">${item.seal}</span>
                    </div>
                    <div style="color:#94a3b8; font-size:9px; margin-top:2px;">
                        ${item.date} ${item.time} | Action: <b style="color:#38bdf8;">${item.action}</b>
                    </div>
                </div>
            `;
        }).join('');
    }

    // Interactive Trigger Buttons
    window.simulateMethaneExceedance = function() {
        triggerBreachEmergency("CMR 153 Methane Spike (1.82%)", "1.82%", "AUTO_POWER_TRIP_EVACUATE");
    };

    window.simulateStrataInstability = function() {
        triggerBreachEmergency("CMR 106 Highwall Bench Slope Shear", "6.4 mm Displacement", "BENCH_ZONE_CLEARANCE");
    };

    window.resetStatutoryEmergency = function() {
        isEmergencyActive = false;
        var banner = document.getElementById('statutory-emergency-overlay');
        if (banner) banner.remove();

        var tripBadge = document.getElementById('grid-trip-status');
        if (tripBadge) {
            tripBadge.style.background = '#14532d';
            tripBadge.style.color = '#4ade80';
            tripBadge.style.borderColor = '#22c55e';
            tripBadge.innerHTML = '⚡ PIT POWER: ENERGIZED (NORMAL)';
        }

        if (typeof window.stopDGMSSiren === 'function') {
            window.stopDGMSSiren();
        }
    };

    // Auto-Mount & Loop
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', injectAlertsUI);
    } else {
        injectAlertsUI();
    }
    setTimeout(injectAlertsUI, 1400);
    setInterval(monitorTelemetryElements, 3000);
})();
</script>
"""
