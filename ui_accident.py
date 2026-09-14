# ui_accident.py - Standalone DGMS CMR 242 Accidents & Dangerous Occurrences Register

ACCIDENT_MODULE = """
<script>
(function() {
    function injectAccidentUI() {
        if (document.getElementById('statutory-accident-card')) return;

        var container = document.querySelector('.grid-container') || document.body;

        var card = document.createElement('div');
        card.id = 'statutory-accident-card';
        card.style.cssText = 'background:#0f172a; border:1px solid #334155; border-radius:10px; padding:16px; margin:14px 0; color:#f8fafc; font-family:system-ui, sans-serif; box-shadow:0 4px 6px -1px rgba(0,0,0,0.5);';

        card.innerHTML = `
            <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #1e293b; padding-bottom:10px; margin-bottom:12px;">
                <div style="display:flex; align-items:center; gap:8px;">
                    <span style="font-size:18px;">⚠️</span>
                    <div>
                        <div style="font-size:13px; font-weight:bold; color:#ef4444;">ACCIDENT & DANGEROUS OCCURRENCE REGISTER</div>
                        <div style="font-size:10px; color:#94a3b8;">DGMS CMR 2017 Reg 242 & Mines Act Sec 23 - Form IV / IV-A Notice Draft</div>
                    </div>
                </div>
                <div id="accident-severity-badge" style="background:#14532d; color:#4ade80; border:1px solid #22c55e; font-size:10px; padding:3px 8px; border-radius:12px; font-weight:bold;">
                    ZERO FATAL / REPORTABLE
                </div>
            </div>

            <!-- Accident & Dangerous Occurrence Form -->
            <form id="accident-report-form" onsubmit="recordAccidentIncident(event)">
                <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap:10px; margin-bottom:10px;">
                    <div>
                        <label style="font-size:11px; color:#94a3b8;">Incident Classification</label>
                        <select id="accident-class" onchange="evaluateIncidentSeverity()" style="width:100%; background:#020617; border:1px solid #334155; color:#f59e0b; font-weight:bold; padding:8px; border-radius:6px; font-size:11px; margin-top:4px;">
                            <option value="Near Miss (No Injury / Property Safe)">Near Miss (No Injury / Minor)</option>
                            <option value="Dangerous Occurrence (CMR 242 Sub-Reg 1)">🚨 Dangerous Occurrence (No Injury)</option>
                            <option value="Serious Bodily Injury (>20 Days Absent)">🚨 Serious Bodily Injury (Permanent/Fracture)</option>
                            <option value="Reportable Injury (>72 Hrs Absent)">⚠️ Reportable Injury (>72 Hrs Lost)</option>
                            <option value="Minor / First Aid Injury">Minor First Aid Case</option>
                        </select>
                    </div>
                    <div>
                        <label style="font-size:11px; color:#94a3b8;">Specific Nature / Hazard Agent</label>
                        <select id="accident-hazard-type" style="width:100%; background:#020617; border:1px solid #334155; color:#fff; padding:8px; border-radius:6px; font-size:11px; margin-top:4px;">
                            <option value="Fall of Roof / Side Strata">Fall of Roof / Side Strata</option>
                            <option value="Winding Rope Breakage / Overwind">Winding Rope Breakage / Overwind</option>
                            <option value="Inflammable / Toxic Gas Outburst">Inflammable / Toxic Gas Outburst</option>
                            <option value="Spontaneous Combustion / Fire Smoke">Spontaneous Combustion / Fire Smoke</option>
                            <option value="Inundation / Sudden Water Inrush">Inundation / Sudden Water Inrush</option>
                            <option value="Premature Explosion / Misfire Event">Premature Explosion / Misfire Event</option>
                            <option value="Haulage Runaway / Tramming Derailment">Haulage Runaway / Tramming Derailment</option>
                            <option value="HEMM / Dumper Interaction">HEMM / Dumper Interaction</option>
                            <option value="Electrical Flashover / Shock">Electrical Flashover / Shock</option>
                            <option value="Slip / Trip / Fall of Person">Slip / Trip / Fall of Person</option>
                        </select>
                    </div>
                    <div>
                        <label style="font-size:11px; color:#94a3b8;">Underground Location / District</label>
                        <input type="text" id="accident-location" required placeholder="e.g. 3rd Dip Junction / Level 4 East" style="width:100%; background:#020617; border:1px solid #334155; color:#fff; padding:8px; border-radius:6px; font-size:11px; margin-top:4px;">
                    </div>
                </div>

                <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap:8px; margin-bottom:12px;">
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Person Affected (Name & Token)</span>
                        <input type="text" id="accident-person" placeholder="e.g. Suresh Ram (TK-502) / Nil" style="width:100%; background:transparent; border:none; color:#38bdf8; font-size:11px; margin-top:2px;">
                    </div>
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Injury / Impact Sustained</span>
                        <input type="text" id="accident-injury" placeholder="e.g. Right tibia fracture / Equipment damaged" style="width:100%; background:transparent; border:none; color:#cbd5e1; font-size:11px; margin-top:2px;">
                    </div>
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Immediate Protective Action</span>
                        <select id="accident-action" style="width:100%; background:transparent; border:none; color:#4ade80; font-weight:bold; font-size:11px; margin-top:2px;">
                            <option value="Area Fenced Off & Work Suspended">Area Fenced & Work Suspended</option>
                            <option value="First Aid Given & Shifted to Pithead">First Aid & Evacuated</option>
                            <option value="Equipment De-energized / Tagged">De-energized & Locked Out</option>
                            <option value="Ventilation Airflow Doubled">Ventilation Doubled</option>
                        </select>
                    </div>
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Investigating Officer</span>
                        <input type="text" id="accident-officer" required placeholder="Name & First/Second Class Cert" style="width:100%; background:transparent; border:none; color:#cbd5e1; font-size:11px; margin-top:2px;">
                    </div>
                </div>

                <div id="accident-statutory-msg" style="background:#020617; border:1px dashed #334155; padding:8px; border-radius:6px; margin-bottom:12px; font-size:11px; color:#cbd5e1;">
                    CMR 242 Requirement: Enter incident details. For Serious Bodily Injury or Dangerous Occurrence, Form IV notice must be transmitted to DGMS within 24 hours.
                </div>

                <button type="submit" id="submit-accident-btn" style="width:100%; background:#d97706; color:#fff; font-weight:bold; border:none; padding:10px; border-radius:6px; font-size:12px; cursor:pointer;">
                    ⚠️ Log Statutory Incident & Generate Notice Draft
                </button>
            </form>

            <!-- Incident Archive Ledger -->
            <div style="margin-top:14px; border-top:1px solid #1e293b; padding-top:10px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                    <div style="font-size:11px; font-weight:bold; color:#cbd5e1;">DGMS Form IV / IV-A Incident Register Archive</div>
                    <span id="accident-count-badge" style="background:#334155; color:#cbd5e1; font-size:9px; padding:2px 6px; border-radius:8px;">0 Incidents</span>
                </div>
                <div id="accident-history-list" style="max-height:120px; overflow-y:auto; font-size:10px; color:#94a3b8;">
                    Zero statutory accidents recorded in this pit horizon.
                </div>
            </div>
        `;

        container.appendChild(card);
        renderAccidentLogs();
    }

    window.evaluateIncidentSeverity = function() {
        var cls = document.getElementById('accident-class').value;
        var badge = document.getElementById('accident-severity-badge');
        var msg = document.getElementById('accident-statutory-msg');
        var btn = document.getElementById('submit-accident-btn');

        if (!badge || !msg) return;

        if (cls.indexOf('Serious') !== -1 || cls.indexOf('Dangerous') !== -1) {
            badge.style.background = '#7f1d1d';
            badge.style.color = '#fca5a5';
            badge.style.borderColor = '#ef4444';
            badge.innerText = '🚨 MANDATORY DGMS 24-HR NOTICE';

            msg.innerHTML = '<span style="color:#ef4444; font-weight:bold;">STATUTORY DIRECTIVE (CMR 242):</span> Formal notice on Form IV/IV-A must be dispatched to Dy. DGMS / Inspector within 24 hours. Area must remain undisturbed until inspection.';
            if (btn) {
                btn.style.background = '#dc2626';
                btn.innerText = '🚨 Record Dangerous Occurrence & Freeze Site';
            }
        } else if (cls.indexOf('Reportable') !== -1) {
            badge.style.background = '#78350f';
            badge.style.color = '#fde68a';
            badge.style.borderColor = '#f59e0b';
            badge.innerText = '⚠️ REPORTABLE INJURY LOGGED';

            msg.innerHTML = '<span style="color:#f59e0b; font-weight:bold;">REPORTABLE:</span> Record in Form J. If worker remains absent exceeding 20 days, auto-reclassify to Serious Bodily Injury.';
            if (btn) {
                btn.style.background = '#d97706';
                btn.innerText = '⚠️ Log Reportable Incident (Form J)';
            }
        } else {
            badge.style.background = '#14532d';
            badge.style.color = '#4ade80';
            badge.style.borderColor = '#22c55e';
            badge.innerText = 'ZERO FATAL / REPORTABLE';

            msg.innerHTML = 'Internal Mine Safety Record: Minor/Near Miss event logged for safety audit and root cause prevention.';
            if (btn) {
                btn.style.background = '#0284c7';
                btn.innerText = '📋 Log Safety Occurrence (Internal)';
            }
        }
    };

    window.recordAccidentIncident = function(e) {
        if (e) e.preventDefault();
        var cls = document.getElementById('accident-class').value;
        var hazard = document.getElementById('accident-hazard-type').value;
        var location = document.getElementById('accident-location').value;
        var person = document.getElementById('accident-person').value || 'None (Equipment/Strata Event)';
        var injury = document.getElementById('accident-injury').value || 'Nil / Property Hazard';
        var action = document.getElementById('accident-action').value;
        var officer = document.getElementById('accident-officer').value;

        var isMandatoryNotice = (cls.indexOf('Serious') !== -1 || cls.indexOf('Dangerous') !== -1);

        var entry = {
            id: 'INC-' + Date.now(),
            date: new Date().toLocaleDateString(),
            time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
            category: cls,
            hazard: hazard,
            location: location,
            person: person,
            injury: injury,
            action: action,
            officer: officer,
            seal: 'ACC-SEAL-' + Math.random().toString(36).substring(2, 8).toUpperCase()
        };

        var store = JSON.parse(localStorage.getItem('dgms_accident_logs') || '[]');
        store.unshift(entry);
        localStorage.setItem('dgms_accident_logs', JSON.stringify(store));

        document.getElementById('accident-location').value = '';
        renderAccidentLogs();

        if (isMandatoryNotice) {
            alert('🚨 STATUTORY BREACH/NOTICE REQUIRED: Incident recorded. CMR 242 Form IV-A draft generated with Seal ' + entry.seal + '. Notice must reach DGMS within 24 hours.');
        } else {
            alert('✅ Incident Logged into Safety Register with Seal ' + entry.seal);
        }
    };

    function renderAccidentLogs() {
        var el = document.getElementById('accident-history-list');
        var badge = document.getElementById('accident-count-badge');
        if (!el) return;

        var store = JSON.parse(localStorage.getItem('dgms_accident_logs') || '[]');
        if (badge) badge.innerText = store.length + ' Incidents';

        if (store.length === 0) {
            el.innerHTML = '<div style="color:#64748b; padding:4px;">Zero statutory accidents recorded in this pit horizon.</div>';
            return;
        }

        el.innerHTML = store.map(function(item) {
            var isRed = (item.category.indexOf('Serious') !== -1 || item.category.indexOf('Dangerous') !== -1);
            var col = isRed ? '#ef4444' : '#f59e0b';
            return `
                <div style="background:#020617; border:1px solid #1e293b; padding:6px 8px; border-radius:4px; margin-bottom:4px;">
                    <div style="display:flex; justify-content:space-between; font-weight:bold;">
                        <span style="color:${col};">${item.category} (${item.hazard})</span>
                        <span style="font-family:monospace; color:#38bdf8; font-size:9px;">${item.seal}</span>
                    </div>
                    <div style="display:flex; justify-content:space-between; color:#cbd5e1; margin-top:2px;">
                        <span>Location: <b>${item.location}</b> | Person: <b>${item.person}</b></span>
                        <span style="color:#94a3b8; font-size:9px;">${item.action}</span>
                    </div>
                    <div style="color:#64748b; font-size:9px; margin-top:2px;">
                        ${item.date} ${item.time} • Injury: ${item.injury} • Investigating Officer: ${item.officer}
                    </div>
                </div>
            `;
        }).join('');
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', injectAccidentUI);
    } else {
        injectAccidentUI();
    }
    setTimeout(injectAccidentUI, 5200);
})();
</script>
"""
