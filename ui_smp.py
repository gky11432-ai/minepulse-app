# ui_smp.py - Standalone DGMS CMR 104 Safety Management Plan (SMP) & Dynamic TARP Engine

SMP_MODULE = """
<script>
(function() {
    function injectSMPUI() {
        if (document.getElementById('statutory-smp-card')) return;

        var container = document.querySelector('.grid-container') || document.body;

        var card = document.createElement('div');
        card.id = 'statutory-smp-card';
        card.style.cssText = 'background:#0f172a; border:1px solid #334155; border-radius:10px; padding:16px; margin:14px 0; color:#f8fafc; font-family:system-ui, sans-serif; box-shadow:0 4px 6px -1px rgba(0,0,0,0.5);';

        card.innerHTML = `
            <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #1e293b; padding-bottom:10px; margin-bottom:12px;">
                <div style="display:flex; align-items:center; gap:8px;">
                    <span style="font-size:18px;">📋</span>
                    <div>
                        <div style="font-size:13px; font-weight:bold; color:#38bdf8;">SAFETY MANAGEMENT PLAN (SMP) & DYNAMIC TARP</div>
                        <div style="font-size:10px; color:#94a3b8;">DGMS CMR 2017 Reg 104 - Hazard Identification, Risk Matrix (5x5) & TARP Trigger</div>
                    </div>
                </div>
                <div id="tarp-status-badge" style="background:#14532d; color:#4ade80; border:1px solid #22c55e; font-size:10px; padding:3px 8px; border-radius:12px; font-weight:bold;">
                    LEVEL 0: GREEN (NORMAL SOP)
                </div>
            </div>

            <!-- Dynamic Risk Matrix & TARP Form -->
            <form id="smp-risk-form" onsubmit="recordSMPAssessment(event)">
                <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap:10px; margin-bottom:10px;">
                    <div>
                        <label style="font-size:11px; color:#94a3b8;">Principal Hazard Domain</label>
                        <select id="smp-hazard-domain" onchange="updateSuggestedTriggers()" style="width:100%; background:#020617; border:1px solid #334155; color:#fff; padding:8px; border-radius:6px; font-size:11px; margin-top:4px;">
                            <option value="Strata & Roof/Side Fall">Strata & Roof/Side Fall</option>
                            <option value="Gaseous Accumulation (CH4/CO/CO2)">Gaseous Accumulation (CH4/CO/CO2)</option>
                            <option value="Inundation / Water Influx">Inundation / Water Influx</option>
                            <option value="Spontaneous Combustion / Fire">Spontaneous Combustion / Fire</option>
                            <option value="HEMM / Transport Interaction">HEMM / Transport Interaction</option>
                            <option value="Explosive Coal Dust Propagation">Explosive Coal Dust Propagation</option>
                            <option value="Incline Haulage Runaway">Incline Haulage Runaway</option>
                        </select>
                    </div>
                    <div>
                        <label style="font-size:11px; color:#94a3b8;">Working District / Specific Location</label>
                        <input type="text" id="smp-location" required placeholder="e.g. 2nd Dip Face / Depillaring Panel 3" style="width:100%; background:#020617; border:1px solid #334155; color:#fff; padding:8px; border-radius:6px; font-size:11px; margin-top:4px;">
                    </div>
                    <div>
                        <label style="font-size:11px; color:#94a3b8;">Observed Operational Trigger / Event</label>
                        <input type="text" id="smp-trigger-event" required placeholder="e.g. Convergence >5mm / Airflow drop" style="width:100%; background:#020617; border:1px solid #334155; color:#fff; padding:8px; border-radius:6px; font-size:11px; margin-top:4px;">
                    </div>
                </div>

                <!-- 5x5 Risk Matrix Calculation -->
                <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap:8px; margin-bottom:12px;">
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Consequence (C: 1-5)</span>
                        <select id="smp-consequence" onchange="calculateRiskScore()" style="width:100%; background:transparent; border:none; color:#38bdf8; font-weight:bold; font-size:11px; margin-top:2px;">
                            <option value="1">1 - Insignificant (First Aid)</option>
                            <option value="2">2 - Minor (Reportable)</option>
                            <option value="3" selected>3 - Moderate (Serious Injury)</option>
                            <option value="4">4 - Major (Single Fatality)</option>
                            <option value="5">5 - Catastrophic (Disaster)</option>
                        </select>
                    </div>
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Likelihood (L: 1-5)</span>
                        <select id="smp-likelihood" onchange="calculateRiskScore()" style="width:100%; background:transparent; border:none; color:#38bdf8; font-weight:bold; font-size:11px; margin-top:2px;">
                            <option value="1">1 - Rare (<1 in 10 yrs)</option>
                            <option value="2" selected>2 - Unlikely (Occurred)</option>
                            <option value="3">3 - Possible (Annual)</option>
                            <option value="4">4 - Likely (Monthly)</option>
                            <option value="5">5 - Almost Certain (Shift)</option>
                        </select>
                    </div>
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Computed Risk Index</span>
                        <div id="disp-risk-score" style="font-size:15px; font-weight:bold; color:#4ade80; margin-top:3px;">Score: 6 (Low)</div>
                    </div>
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Safety Officer / Incharge</span>
                        <input type="text" id="smp-officer" required placeholder="Name & Cert No." style="width:100%; background:transparent; border:none; color:#cbd5e1; font-size:11px; margin-top:2px;">
                    </div>
                </div>

                <!-- Mandatory TARP Directive Container -->
                <div id="tarp-action-box" style="background:#020617; border:1px dashed #22c55e; padding:10px; border-radius:6px; margin-bottom:12px; font-size:11px; color:#cbd5e1;">
                    <b style="color:#4ade80;">LEVEL 0 ACTION:</b> Normal operational controls in effect. Standard operating procedures (SOP) and routine shift inspection continue.
                </div>

                <button type="submit" id="submit-smp-btn" style="width:100%; background:#0284c7; color:#fff; font-weight:bold; border:none; padding:10px; border-radius:6px; font-size:12px; cursor:pointer;">
                    📋 Certify SMP Risk Assessment & Action Plan (CMR 104)
                </button>
            </form>

            <!-- SMP / TARP Register Archive -->
            <div style="margin-top:14px; border-top:1px solid #1e293b; padding-top:10px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                    <div style="font-size:11px; font-weight:bold; color:#cbd5e1;">Safety Management Plan Audit Trail (HIRA Ledger)</div>
                    <span id="smp-count-badge" style="background:#334155; color:#cbd5e1; font-size:9px; padding:2px 6px; border-radius:8px;">0 Logs</span>
                </div>
                <div id="smp-history-list" style="max-height:120px; overflow-y:auto; font-size:10px; color:#94a3b8;">
                    No SMP risk assessments recorded in current shift.
                </div>
            </div>
        `;

        container.appendChild(card);
        calculateRiskScore();
        renderSMPLogs();
    }

    window.calculateRiskScore = function() {
        var c = parseInt(document.getElementById('smp-consequence').value) || 1;
        var l = parseInt(document.getElementById('smp-likelihood').value) || 1;
        var score = c * l;

        var disp = document.getElementById('disp-risk-score');
        var badge = document.getElementById('tarp-status-badge');
        var box = document.getElementById('tarp-action-box');
        var btn = document.getElementById('submit-smp-btn');

        if (!disp || !badge || !box) return;

        // DGMS TARP Threshold Classification
        if (score >= 20) {
            // Level 3 (Red) - Emergency Action / Stop Work
            badge.style.background = '#7f1d1d';
            badge.style.color = '#fca5a5';
            badge.style.borderColor = '#ef4444';
            badge.innerText = 'LEVEL 3: RED (EMERGENCY WITHDRAWAL)';
            disp.innerText = 'Score: ' + score + ' (Extreme Risk)';
            disp.style.color = '#ef4444';
            box.style.borderColor = '#ef4444';
            box.innerHTML = '<b style="color:#ef4444;">🚨 LEVEL 3 MANDATORY DIRECTIVE (CMR 104):</b> Immediate cessation of all mining operations. Power isolation to district, withdraw all miners to intake shaft bottom, notify Colliery Manager & Internal Safety Organization (ISO).';
            if (btn) { btn.style.background = '#dc2626'; btn.innerText = '🚨 Execute Level 3 Emergency Order (Withdraw Men)'; }
        } else if (score >= 12) {
            // Level 2 (Orange) - Operational Warning / Restricted Work
            badge.style.background = '#7c2d12';
            badge.style.color = '#fdba74';
            badge.style.borderColor = '#f97316';
            badge.innerText = 'LEVEL 2: ORANGE (RESTRICTED OPS)';
            disp.innerText = 'Score: ' + score + ' (High Risk)';
            disp.style.color = '#f97316';
            box.style.borderColor = '#f97316';
            box.innerHTML = '<b style="color:#f97316;">⚠️ LEVEL 2 MANDATORY DIRECTIVE:</b> Restrict face production. Deploy certified timberman for supplementary reinforcement / double auxiliary ventilation. Manager personal site inspection required within 1 hour.';
            if (btn) { btn.style.background = '#ea580c'; btn.innerText = '⚠️ Certify Level 2 Restrictive Actions'; }
        } else if (score >= 7) {
            // Level 1 (Yellow) - Alert / Increased Monitoring
            badge.style.background = '#78350f';
            badge.style.color = '#fde68a';
            badge.style.borderColor = '#f59e0b';
            badge.innerText = 'LEVEL 1: YELLOW (ALERT / CAUTION)';
            disp.innerText = 'Score: ' + score + ' (Moderate Risk)';
            disp.style.color = '#f59e0b';
            box.style.borderColor = '#f59e0b';
            box.innerHTML = '<b style="color:#f59e0b;">⚡ LEVEL 1 MANDATORY DIRECTIVE:</b> Increase inspection frequency to hourly checks. Verify continuous gas monitoring / tell-tale indicators. Alert Overman and shift supervisor.';
            if (btn) { btn.style.background = '#d97706'; btn.innerText = '⚡ Certify Level 1 Alert Protocol'; }
        } else {
            // Level 0 (Green) - Normal Operation
            badge.style.background = '#14532d';
            badge.style.color = '#4ade80';
            badge.style.borderColor = '#22c55e';
            badge.innerText = 'LEVEL 0: GREEN (NORMAL SOP)';
            disp.innerText = 'Score: ' + score + ' (Low Risk)';
            disp.style.color = '#4ade80';
            box.style.borderColor = '#22c55e';
            box.innerHTML = '<b style="color:#4ade80;">LEVEL 0 ACTION:</b> Normal operational controls in effect. Standard operating procedures (SOP) and routine shift inspection continue.';
            if (btn) { btn.style.background = '#0284c7'; btn.innerText = '📋 Certify SMP Risk Assessment & Action Plan (CMR 104)'; }
        }
    };

    window.updateSuggestedTriggers = function() {
        var domain = document.getElementById('smp-hazard-domain').value;
        var triggerInput = document.getElementById('smp-trigger-event');
        if (!triggerInput) return;

        var suggestions = {
            'Strata & Roof/Side Fall': 'Tell-Tale Lower anchor >4mm / audible rib cracking',
            'Gaseous Accumulation (CH4/CO/CO2)': 'Return airway CH4 >0.75% / CO weeping detected',
            'Inundation / Water Influx': 'Barrier borehole weeping / sump level rising >0.5m/hr',
            'Spontaneous Combustion / Fire': 'Graham Ratio >0.5 / warm smell at return stopping',
            'HEMM / Transport Interaction': 'Brake efficiency loss / AVLA audio dead on Dumper',
            'Explosive Coal Dust Propagation': 'Roadway dust sample incombustible <75%',
            'Incline Haulage Runaway': 'Stop-block lever binding / signal bell intermittent'
        };

        if (suggestions[domain]) {
            triggerInput.value = suggestions[domain];
        }
        calculateRiskScore();
    };

    window.recordSMPAssessment = function(e) {
        if (e) e.preventDefault();
        var domain = document.getElementById('smp-hazard-domain').value;
        var location = document.getElementById('smp-location').value;
        var trigger = document.getElementById('smp-trigger-event').value;
        var c = document.getElementById('smp-consequence').value;
        var l = document.getElementById('smp-likelihood').value;
        var score = parseInt(c) * parseInt(l);
        var officer = document.getElementById('smp-officer').value;
        var tarpLevel = (score >= 20) ? 'Level 3 (Red)' : (score >= 12 ? 'Level 2 (Orange)' : (score >= 7 ? 'Level 1 (Yellow)' : 'Level 0 (Green)'));

        var entry = {
            id: 'SMP-' + Date.now(),
            date: new Date().toLocaleDateString(),
            time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
            domain: domain,
            location: location,
            trigger: trigger,
            matrix: 'C:' + c + ' x L:' + l + ' = ' + score,
            level: tarpLevel,
            officer: officer,
            seal: 'SMP-TARP-' + Math.random().toString(36).substring(2, 8).toUpperCase()
        };

        var store = JSON.parse(localStorage.getItem('dgms_smp_tarp_logs') || '[]');
        store.unshift(entry);
        localStorage.setItem('dgms_smp_tarp_logs', JSON.stringify(store));

        document.getElementById('smp-location').value = '';
        renderSMPLogs();

        if (score >= 20) {
            alert('🚨 DGMS STATUTORY TARP LEVEL 3: Immediate cessation of work and personnel evacuation mandatory!');
        } else {
            alert('✅ SMP Risk Assessment Certified with Seal ' + entry.seal);
        }
    };

    function renderSMPLogs() {
        var el = document.getElementById('smp-history-list');
        var badge = document.getElementById('smp-count-badge');
        if (!el) return;
        var store = JSON.parse(localStorage.getItem('dgms_smp_tarp_logs') || '[]');

        if (badge) badge.innerText = store.length + ' Logs';

        if (store.length === 0) {
            el.innerHTML = '<div style="color:#64748b; padding:4px;">No SMP risk assessments recorded in current shift.</div>';
            return;
        }

        el.innerHTML = store.map(function(item) {
            var col = item.level.indexOf('Red') !== -1 ? '#ef4444' : (item.level.indexOf('Orange') !== -1 ? '#f97316' : (item.level.indexOf('Yellow') !== -1 ? '#f59e0b' : '#4ade80'));
            return `
                <div style="background:#020617; border:1px solid #1e293b; padding:6px 8px; border-radius:4px; margin-bottom:4px;">
                    <div style="display:flex; justify-content:space-between; font-weight:bold;">
                        <span style="color:#38bdf8;">${item.domain} (${item.location})</span>
                        <span style="font-family:monospace; color:#f59e0b; font-size:9px;">${item.seal}</span>
                    </div>
                    <div style="display:flex; justify-content:space-between; color:#cbd5e1; margin-top:2px;">
                        <span>Trigger: <b>${item.trigger.slice(0, 32)}...</b></span>
                        <span style="color:${col}; font-weight:bold;">${item.level} [${item.matrix}]</span>
                    </div>
                    <div style="color:#64748b; font-size:9px; margin-top:2px;">
                        ${item.date} ${item.time} • Attesting Safety Officer: ${item.officer}
                    </div>
                </div>
            `;
        }).join('');
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', injectSMPUI);
    } else {
        injectSMPUI();
    }
    setTimeout(injectSMPUI, 4200);
})();
</script>
"""
