# ui_dust.py - Standalone DGMS CMR 135 & 136 Coal Dust Explosion Prevention & Stone Dust Barrier Engine

DUST_MODULE = """
<script>
(function() {
    function injectDustUI() {
        if (document.getElementById('statutory-dust-card')) return;

        var container = document.querySelector('.grid-container') || document.body;

        var card = document.createElement('div');
        card.id = 'statutory-dust-card';
        card.style.cssText = 'background:#0f172a; border:1px solid #334155; border-radius:10px; padding:16px; margin:14px 0; color:#f8fafc; font-family:system-ui, sans-serif; box-shadow:0 4px 6px -1px rgba(0,0,0,0.5);';

        card.innerHTML = `
            <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #1e293b; padding-bottom:10px; margin-bottom:12px;">
                <div style="display:flex; align-items:center; gap:8px;">
                    <span style="font-size:18px;">🌫️</span>
                    <div>
                        <div style="font-size:13px; font-weight:bold; color:#38bdf8;">COAL DUST SUPPRESSION & STONE DUST BARRIERS</div>
                        <div style="font-size:10px; color:#94a3b8;">DGMS CMR 2017 Reg 135 & 136 - Explosive Dust Sampling & Barrier Audit</div>
                    </div>
                </div>
                <div id="dust-statutory-badge" style="background:#14532d; color:#4ade80; border:1px solid #22c55e; font-size:10px; padding:3px 8px; border-radius:12px; font-weight:bold;">
                    ✓ DUST EXPLOSION PROOF (≥75% INCOMBUSTIBLE)
                </div>
            </div>

            <!-- Roadway Dust Sampling & Barrier Form -->
            <form id="dust-sampling-form" onsubmit="recordDustAudit(event)">
                <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap:10px; margin-bottom:10px;">
                    <div>
                        <label style="font-size:11px; color:#94a3b8;">Sampling Zone / Roadway Segment</label>
                        <select id="dust-zone" style="width:100%; background:#020617; border:1px solid #334155; color:#fff; padding:8px; border-radius:6px; font-size:11px; margin-top:4px;">
                            <option value="Main Belt Conveyor Roadway (Zone A)">Main Belt Conveyor Roadway (Zone A)</option>
                            <option value="Return Airway Sector 2 (Zone R)">Return Airway Sector 2 (Zone R)</option>
                            <option value="Haulage Track Level 12 (Zone H)">Haulage Track Level 12 (Zone H)</option>
                            <option value="Transfer Chute & Loading Point">Transfer Chute & Loading Point</option>
                            <option value="Intake Splitting Heading 4">Intake Splitting Heading 4</option>
                        </select>
                    </div>
                    <div>
                        <label style="font-size:11px; color:#94a3b8;">Sampling Horizon / Location</label>
                        <select id="sampling-horizon" style="width:100%; background:#020617; border:1px solid #334155; color:#fff; padding:8px; border-radius:6px; font-size:11px; margin-top:4px;">
                            <option value="Floor Dust (Strip Sampling)">Floor Dust (Strip Sampling)</option>
                            <option value="Roof & Sides (Perimeter Dust)">Roof & Sides (Perimeter Dust)</option>
                            <option value="Combined Spot Cross-Section">Combined Spot Cross-Section</option>
                        </select>
                    </div>
                    <div>
                        <label style="font-size:11px; color:#94a3b8;">Incombustible Matter (Stone Dust %)</label>
                        <input type="number" step="0.5" id="incombustible-pct" required placeholder="Min 75.0%" oninput="evaluateDustCompliance(this.value)" style="width:100%; background:#020617; border:1px solid #334155; color:#4ade80; font-weight:bold; padding:8px; border-radius:6px; font-size:11px; margin-top:4px;">
                    </div>
                </div>

                <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap:8px; margin-bottom:12px;">
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Stone Dust Barrier Type</span>
                        <select id="barrier-type" style="width:100%; background:transparent; border:none; color:#38bdf8; font-weight:bold; font-size:11px; margin-top:2px;">
                            <option value="Heavy Barrier (Primary 390 kg/m²)">Heavy (390 kg/m²)</option>
                            <option value="Light Barrier (Secondary 195 kg/m²)">Light (195 kg/m²)</option>
                            <option value="No Barrier (Intermediate Zone)">No Barrier Zone</option>
                        </select>
                    </div>
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Barrier Distance to Face (m)</span>
                        <input type="number" id="barrier-dist" required placeholder="135m - 365m" style="width:100%; background:transparent; border:none; color:#fff; font-weight:bold; font-size:13px; margin-top:2px;">
                    </div>
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Shelf Condition & Dust Mobility</span>
                        <select id="shelf-condition" style="width:100%; background:transparent; border:none; color:#4ade80; font-weight:bold; font-size:11px; margin-top:2px;">
                            <option value="Dry & Free Flowing (Dispersible)">Dry & Free Flowing</option>
                            <option value="Caked / Damp (Defective)">⚠️ Caked / Damp (Defective)</option>
                            <option value="Dust Depleted / Insufficient">Depleted / Low Dust</option>
                        </select>
                    </div>
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Sampling Overman / Chemist</span>
                        <input type="text" id="dust-officer" required placeholder="Name & Cert No." style="width:100%; background:transparent; border:none; color:#cbd5e1; font-size:11px; margin-top:2px;">
                    </div>
                </div>

                <button type="submit" id="submit-dust-btn" style="width:100%; background:#0284c7; color:#fff; font-weight:bold; border:none; padding:10px; border-radius:6px; font-size:12px; cursor:pointer;">
                    🌫️ Certify Coal Dust Sampling & Barrier Integrity (CMR 136)
                </button>
            </form>

            <!-- Dust Sampling Register Archive -->
            <div style="margin-top:14px; border-top:1px solid #1e293b; padding-top:10px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                    <div style="font-size:11px; font-weight:bold; color:#cbd5e1;">Statutory Dust Sampling Register (Form-IV Log)</div>
                    <span id="dust-count-badge" style="background:#334155; color:#cbd5e1; font-size:9px; padding:2px 6px; border-radius:8px;">0 Samples</span>
                </div>
                <div id="dust-history-list" style="max-height:120px; overflow-y:auto; font-size:10px; color:#94a3b8;">
                    No coal dust sampling records registered.
                </div>
            </div>
        `;

        container.appendChild(card);
        renderDustLogs();
    }

    window.evaluateDustCompliance = function(val) {
        var incombustible = parseFloat(val);
        var badge = document.getElementById('dust-statutory-badge');
        var input = document.getElementById('incombustible-pct');
        var btn = document.getElementById('submit-dust-btn');
        if (isNaN(incombustible) || !badge) return;

        // DGMS Regulation 135: Incombustible matter shall not be less than 75%
        if (incombustible < 75.0) {
            badge.style.background = '#7f1d1d';
            badge.style.color = '#fca5a5';
            badge.style.borderColor = '#ef4444';
            badge.innerText = '🚨 EXPLOSION RISK: INCOMBUSTIBLE < 75% (RE-DUSTING REQUIRED)';
            input.style.color = '#ef4444';
            if (btn) btn.style.background = '#dc2626';
        } else {
            badge.style.background = '#14532d';
            badge.style.color = '#4ade80';
            badge.style.borderColor = '#22c55e';
            badge.innerText = '✓ DUST EXPLOSION PROOF (≥75% INCOMBUSTIBLE)';
            input.style.color = '#4ade80';
            if (btn) btn.style.background = '#0284c7';
        }
    };

    window.recordDustAudit = function(e) {
        if (e) e.preventDefault();
        var zone = document.getElementById('dust-zone').value;
        var horizon = document.getElementById('sampling-horizon').value;
        var incomb = parseFloat(document.getElementById('incombustible-pct').value) || 0;
        var barrier = document.getElementById('barrier-type').value;
        var dist = document.getElementById('barrier-dist').value;
        var shelf = document.getElementById('shelf-condition').value;
        var officer = document.getElementById('dust-officer').value;

        var isBreach = (incomb < 75.0 || shelf.indexOf('Defective') !== -1);
        var certStatus = isBreach ? 'STATUTORY BREACH (ACTION REQ)' : 'COMPLIANT (SAFE)';

        var entry = {
            id: 'DUST-' + Date.now(),
            date: new Date().toLocaleDateString(),
            time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
            zone: zone,
            horizon: horizon,
            incombustible: incomb + '%',
            barrier: barrier + ' @ ' + dist + 'm',
            shelf: shelf,
            officer: officer,
            status: certStatus,
            seal: 'DUST-SEAL-' + Math.random().toString(36).substring(2, 8).toUpperCase()
        };

        var store = JSON.parse(localStorage.getItem('dgms_dust_logs') || '[]');
        store.unshift(entry);
        localStorage.setItem('dgms_dust_logs', JSON.stringify(store));

        document.getElementById('incombustible-pct').value = '';
        document.getElementById('barrier-dist').value = '';
        renderDustLogs();

        if (isBreach) {
            alert('⚠️ CMR 135 VIOLATION: Roadway dust has less than 75% incombustible matter or barrier is defective! Immediate heavy stone dusting ordered.');
        } else {
            alert('✅ Dust Sampling & Barrier Audit Certified with Seal ' + entry.seal);
        }
    };

    function renderDustLogs() {
        var el = document.getElementById('dust-history-list');
        var badge = document.getElementById('dust-count-badge');
        if (!el) return;
        var store = JSON.parse(localStorage.getItem('dgms_dust_logs') || '[]');

        if (badge) badge.innerText = store.length + ' Samples';

        if (store.length === 0) {
            el.innerHTML = '<div style="color:#64748b; padding:4px;">No coal dust sampling records registered.</div>';
            return;
        }

        el.innerHTML = store.map(function(item) {
            var isBad = item.status.indexOf('BREACH') !== -1;
            var col = isBad ? '#ef4444' : '#4ade80';
            return `
                <div style="background:#020617; border:1px solid #1e293b; padding:6px 8px; border-radius:4px; margin-bottom:4px;">
                    <div style="display:flex; justify-content:space-between; font-weight:bold;">
                        <span style="color:#38bdf8;">${item.zone} (${item.horizon.slice(0, 10)}...)</span>
                        <span style="font-family:monospace; color:#f59e0b; font-size:9px;">${item.seal}</span>
                    </div>
                    <div style="display:flex; justify-content:space-between; color:#cbd5e1; margin-top:2px;">
                        <span>Incombustible: <b style="color:${col};">${item.incombustible}</b> (Min 75%)</span>
                        <span>Barrier: <b>${item.barrier}</b></span>
                        <span style="color:${col}; font-weight:bold;">${item.status}</span>
                    </div>
                    <div style="color:#64748b; font-size:9px; margin-top:2px;">
                        ${item.date} ${item.time} • Shelves: ${item.shelf} • Sampling Officer: ${item.officer}
                    </div>
                </div>
            `;
        }).join('');
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', injectDustUI);
    } else {
        injectDustUI();
    }
    setTimeout(injectDustUI, 2800);
})();
</script>
"""
