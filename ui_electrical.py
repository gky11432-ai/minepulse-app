# ui_electrical.py - Standalone DGMS CMR 153 & CEA Mines Regs Flameproof (FLP) & Earth Leakage Relay Engine

ELECTRICAL_MODULE = """
<script>
(function() {
    function injectElectricalUI() {
        if (document.getElementById('statutory-electrical-card')) return;

        var container = document.querySelector('.grid-container') || document.body;

        var card = document.createElement('div');
        card.id = 'statutory-electrical-card';
        card.style.cssText = 'background:#0f172a; border:1px solid #334155; border-radius:10px; padding:16px; margin:14px 0; color:#f8fafc; font-family:system-ui, sans-serif; box-shadow:0 4px 6px -1px rgba(0,0,0,0.5);';

        card.innerHTML = `
            <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #1e293b; padding-bottom:10px; margin-bottom:12px;">
                <div style="display:flex; align-items:center; gap:8px;">
                    <span style="font-size:18px;">⚡</span>
                    <div>
                        <div style="font-size:13px; font-weight:bold; color:#38bdf8;">FLAMEPROOF (FLP) & EARTH LEAKAGE AUDIT</div>
                        <div style="font-size:10px; color:#94a3b8;">CEA Mines Regs 2010 & CMR 153 - Intrinsic Safety & Electrical Trip Test</div>
                    </div>
                </div>
                <div id="electrical-safety-badge" style="background:#14532d; color:#4ade80; border:1px solid #22c55e; font-size:10px; padding:3px 8px; border-radius:12px; font-weight:bold;">
                    ✓ FLP APPARATUS INTRINSICALLY SAFE
                </div>
            </div>

            <!-- Flameproof & ELR Testing Form -->
            <form id="electrical-audit-form" onsubmit="recordElectricalAudit(event)">
                <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap:10px; margin-bottom:10px;">
                    <div>
                        <label style="font-size:11px; color:#94a3b8;">Sub-Station / Switchgear Unit</label>
                        <select id="switchgear-id" style="width:100%; background:#020617; border:1px solid #334155; color:#fff; padding:8px; border-radius:6px; font-size:11px; margin-top:4px;">
                            <option value="Gate End Box (GEB-04) Face-1 SDL">Gate End Box (GEB-04) Face-1 SDL</option>
                            <option value="Drill Control Panel (DCP-02) 125V">Drill Control Panel (DCP-02) 125V</option>
                            <option value="Section Transwitch Unit (3.3kV / 550V)">Section Transwitch Unit (3.3kV / 550V)</option>
                            <option value="Haulage Motor Stator Panel (75 kW)">Haulage Motor Stator Panel (75 kW)</option>
                            <option value="Main Pump House Starter Switch">Main Pump House Starter Switch</option>
                        </select>
                    </div>
                    <div>
                        <label style="font-size:11px; color:#94a3b8;">FLP Flange Joint Gap (mm)</label>
                        <input type="number" step="0.05" id="flange-gap" required placeholder="Max 0.40 mm" oninput="evaluateFlpGap(this.value)" style="width:100%; background:#020617; border:1px solid #334155; color:#4ade80; font-weight:bold; padding:8px; border-radius:6px; font-size:11px; margin-top:4px;">
                    </div>
                    <div>
                        <label style="font-size:11px; color:#94a3b8;">Earth Leakage Relay (ELR) Test</label>
                        <select id="elr-test-result" onchange="evaluateElrRisk(this.value)" style="width:100%; background:#020617; border:1px solid #334155; color:#4ade80; font-weight:bold; padding:8px; border-radius:6px; font-size:11px; margin-top:4px;">
                            <option value="TRIPPED INSTANTLY (<50 ms)">TRIPPED INSTANTLY (<50 ms)</option>
                            <option value="FAILED TO TRIP / COIL JAMMED">⚠️ FAILED TO TRIP (COIL JAM)</option>
                            <option value="DELAYED TRIP (>150 ms Fault)">DELAYED TRIP (>150 ms Fault)</option>
                        </select>
                    </div>
                </div>

                <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap:8px; margin-bottom:12px;">
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Insulation Resistance (IR)</span>
                        <input type="number" step="0.1" id="ir-val" required placeholder="Min 5.0 MegaOhms" style="width:100%; background:transparent; border:none; color:#fff; font-weight:bold; font-size:13px; margin-top:2px;">
                    </div>
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Earth Continuity (<0.5 Ohm)</span>
                        <select id="earth-continuity" style="width:100%; background:transparent; border:none; color:#4ade80; font-weight:bold; font-size:11px; margin-top:2px;">
                            <option value="0.22 Ohm (Healthy Bond)">0.22 Ohm (Healthy)</option>
                            <option value="High Resistance (>1.0 Ohm)">High Resistance (>1.0 Ω)</option>
                            <option value="Pilot Core Broken">Pilot Core Broken</option>
                        </select>
                    </div>
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Trailing Cable Sheath</span>
                        <select id="cable-sheath" style="width:100%; background:transparent; border:none; color:#4ade80; font-weight:bold; font-size:11px; margin-top:2px;">
                            <option value="Intact / Vulcanized Joint OK">Intact / Vulcanized OK</option>
                            <option value="Armor Exposed / Cut">⚠️ Armor Exposed / Cut</option>
                            <option value="Temporary Tape Joint">Temporary Tape Joint</option>
                        </select>
                    </div>
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Statutory Electrical Supervisor</span>
                        <input type="text" id="elec-supervisor" required placeholder="Name & Mines Cert No." style="width:100%; background:transparent; border:none; color:#cbd5e1; font-size:11px; margin-top:2px;">
                    </div>
                </div>

                <button type="submit" id="submit-elec-btn" style="width:100%; background:#0284c7; color:#fff; font-weight:bold; border:none; padding:10px; border-radius:6px; font-size:12px; cursor:pointer;">
                    ⚡ Certify FLP & Electrical Apparatus Fitness (CEA Regs)
                </button>
            </form>

            <!-- Electrical Audit Register Archive -->
            <div style="margin-top:14px; border-top:1px solid #1e293b; padding-top:10px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                    <div style="font-size:11px; font-weight:bold; color:#cbd5e1;">Statutory Electrical Test Register (CEA Log)</div>
                    <span id="elec-count-badge" style="background:#334155; color:#cbd5e1; font-size:9px; padding:2px 6px; border-radius:8px;">0 Checks</span>
                </div>
                <div id="elec-history-list" style="max-height:120px; overflow-y:auto; font-size:10px; color:#94a3b8;">
                    No electrical apparatus tests recorded.
                </div>
            </div>
        `;

        container.appendChild(card);
        renderElectricalLogs();
    }

    window.evaluateFlpGap = function(val) {
        var gap = parseFloat(val);
        var badge = document.getElementById('electrical-safety-badge');
        var input = document.getElementById('flange-gap');
        var btn = document.getElementById('submit-elec-btn');
        if (isNaN(gap) || !badge) return;

        // DGMS Flameproof Standard: Gap must not exceed 0.40 mm for Methane (Group I)
        if (gap > 0.40) {
            badge.style.background = '#7f1d1d';
            badge.style.color = '#fca5a5';
            badge.style.borderColor = '#ef4444';
            badge.innerText = '🚨 FLP BREACH: GAP > 0.40 mm (ISOLATE POWER)';
            input.style.color = '#ef4444';
            if (btn) btn.style.background = '#dc2626';
        } else {
            badge.style.background = '#14532d';
            badge.style.color = '#4ade80';
            badge.style.borderColor = '#22c55e';
            badge.innerText = '✓ FLP APPARATUS INTRINSICALLY SAFE';
            input.style.color = '#4ade80';
            if (btn) btn.style.background = '#0284c7';
        }
    };

    window.evaluateElrRisk = function(val) {
        var badge = document.getElementById('electrical-safety-badge');
        var select = document.getElementById('elr-test-result');
        var btn = document.getElementById('submit-elec-btn');
        if (!badge) return;

        if (val.indexOf('FAILED') !== -1) {
            badge.style.background = '#7f1d1d';
            badge.style.color = '#fca5a5';
            badge.style.borderColor = '#ef4444';
            badge.innerText = '🚨 ELR DEFECTIVE: SHOCK & SPARK HAZARD';
            select.style.color = '#ef4444';
            if (btn) btn.style.background = '#dc2626';
        } else {
            badge.style.background = '#14532d';
            badge.style.color = '#4ade80';
            badge.style.borderColor = '#22c55e';
            badge.innerText = '✓ FLP APPARATUS INTRINSICALLY SAFE';
            select.style.color = '#4ade80';
            if (btn) btn.style.background = '#0284c7';
        }
    };

    window.recordElectricalAudit = function(e) {
        if (e) e.preventDefault();
        var gear = document.getElementById('switchgear-id').value;
        var gap = parseFloat(document.getElementById('flange-gap').value) || 0;
        var elr = document.getElementById('elr-test-result').value;
        var ir = document.getElementById('ir-val').value;
        var earth = document.getElementById('earth-continuity').value;
        var cable = document.getElementById('cable-sheath').value;
        var supervisor = document.getElementById('elec-supervisor').value;

        var isBreach = (gap > 0.40 || elr.indexOf('FAILED') !== -1 || cable.indexOf('Exposed') !== -1);
        var certStatus = isBreach ? 'ISOLATED / STATUTORY DEFECT' : 'SAFE FOR GASSY HORIZON';

        var entry = {
            id: 'ELEC-' + Date.now(),
            date: new Date().toLocaleDateString(),
            time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
            switchgear: gear,
            gap: gap + ' mm',
            elr: elr,
            ir: ir + ' MΩ',
            earth: earth,
            cable: cable,
            supervisor: supervisor,
            status: certStatus,
            seal: 'FLP-SEAL-' + Math.random().toString(36).substring(2, 8).toUpperCase()
        };

        var store = JSON.parse(localStorage.getItem('dgms_electrical_logs') || '[]');
        store.unshift(entry);
        localStorage.setItem('dgms_electrical_logs', JSON.stringify(store));

        document.getElementById('flange-gap').value = '';
        document.getElementById('ir-val').value = '';
        renderElectricalLogs();

        if (isBreach) {
            alert('🚨 CEA MINES SAFETY BREACH: FLP gap exceeds 0.40mm or ELR trip failed! Power supply must remain tripped under CMR 153.');
        } else {
            alert('✅ Flameproof & Electrical Fitness Certified with Seal ' + entry.seal);
        }
    };

    function renderElectricalLogs() {
        var el = document.getElementById('elec-history-list');
        var badge = document.getElementById('elec-count-badge');
        if (!el) return;
        var store = JSON.parse(localStorage.getItem('dgms_electrical_logs') || '[]');

        if (badge) badge.innerText = store.length + ' Checks';

        if (store.length === 0) {
            el.innerHTML = '<div style="color:#64748b; padding:4px;">No electrical apparatus tests recorded.</div>';
            return;
        }

        el.innerHTML = store.map(function(item) {
            var isBad = item.status.indexOf('DEFECT') !== -1;
            var col = isBad ? '#ef4444' : '#4ade80';
            return `
                <div style="background:#020617; border:1px solid #1e293b; padding:6px 8px; border-radius:4px; margin-bottom:4px;">
                    <div style="display:flex; justify-content:space-between; font-weight:bold;">
                        <span style="color:#38bdf8;">${item.switchgear}</span>
                        <span style="font-family:monospace; color:#f59e0b; font-size:9px;">${item.seal}</span>
                    </div>
                    <div style="display:flex; justify-content:space-between; color:#cbd5e1; margin-top:2px;">
                        <span>FLP Gap: <b style="color:${col};">${item.gap}</b> | IR: <b>${item.ir}</b></span>
                        <span>ELR: <b>${item.elr.slice(0, 15)}...</b></span>
                        <span style="color:${col}; font-weight:bold;">${item.status}</span>
                    </div>
                    <div style="color:#64748b; font-size:9px; margin-top:2px;">
                        ${item.date} ${item.time} • Earth: ${item.earth} • Cable: ${item.cable} • Supv: ${item.supervisor}
                    </div>
                </div>
            `;
        }).join('');
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', injectElectricalUI);
    } else {
        injectElectricalUI();
    }
    setTimeout(injectElectricalUI, 3200);
})();
</script>
"""
