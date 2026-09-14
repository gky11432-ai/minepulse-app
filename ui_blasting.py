# ui_blasting.py - Standalone DGMS CMR 186-205 Shotfirer's Statutory Blasting & Magazine Register

BLASTING_MODULE = """
<script>
(function() {
    function injectBlastingUI() {
        if (document.getElementById('statutory-blasting-card')) return;

        var container = document.querySelector('.grid-container') || document.body;

        var card = document.createElement('div');
        card.id = 'statutory-blasting-card';
        card.style.cssText = 'background:#0f172a; border:1px solid #334155; border-radius:10px; padding:16px; margin:14px 0; color:#f8fafc; font-family:system-ui, sans-serif; box-shadow:0 4px 6px -1px rgba(0,0,0,0.5);';

        card.innerHTML = `
            <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #1e293b; padding-bottom:10px; margin-bottom:12px;">
                <div style="display:flex; align-items:center; gap:8px;">
                    <span style="font-size:18px;">🧨</span>
                    <div>
                        <div style="font-size:13px; font-weight:bold; color:#f59e0b;">STATUTORY SHOTFIRING & EXPLOSIVES REGISTER</div>
                        <div style="font-size:10px; color:#94a3b8;">DGMS CMR 2017 Reg 186-205 - Pre-Blast Gas Verification & Misfire Guard</div>
                    </div>
                </div>
                <div id="blast-clearance-status" style="background:#14532d; color:#4ade80; border:1px solid #22c55e; font-size:10px; padding:3px 8px; border-radius:12px; font-weight:bold;">
                    ✓ CLEAR TO CHARGE
                </div>
            </div>

            <!-- Blasting Round Entry Form -->
            <form id="shotfire-entry-form" onsubmit="recordBlastingRound(event)">
                <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap:10px; margin-bottom:10px;">
                    <div>
                        <label style="font-size:11px; color:#94a3b8;">Blasting Heading / Face</label>
                        <input type="text" id="blast-face" required placeholder="e.g. 2nd Dip Heading No. 5" style="width:100%; background:#020617; border:1px solid #334155; color:#fff; padding:8px; border-radius:6px; font-size:11px; margin-top:4px;">
                    </div>
                    <div>
                        <label style="font-size:11px; color:#94a3b8;">Authorized Shotfirer</label>
                        <input type="text" id="shotfirer-name" required placeholder="Name & Blaster Cert No." style="width:100%; background:#020617; border:1px solid #334155; color:#fff; padding:8px; border-radius:6px; font-size:11px; margin-top:4px;">
                    </div>
                    <div>
                        <label style="font-size:11px; color:#94a3b8;">Explosive Class & Qty (Kg)</label>
                        <div style="display:flex; gap:6px; margin-top:4px;">
                            <select id="explosive-class" style="background:#020617; border:1px solid #334155; color:#fff; padding:8px; border-radius:6px; font-size:11px;">
                                <option value="P1 Permitted">P1 Permitted</option>
                                <option value="P3 Solid Blasting">P3 Solid Blasting</option>
                                <option value="P5 Special Drift">P5 Special Drift</option>
                                <option value="Slurry Booster">Slurry Booster</option>
                            </select>
                            <input type="number" step="0.25" id="explosive-qty" required placeholder="Kg" style="width:70px; background:#020617; border:1px solid #334155; color:#fff; padding:8px; border-radius:6px; font-size:11px;">
                        </div>
                    </div>
                </div>

                <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap:8px; margin-bottom:12px;">
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Detonators Fired</span>
                        <input type="number" id="detonators-count" required placeholder="e.g. 18" style="width:100%; background:transparent; border:none; color:#fff; font-weight:bold; font-size:13px; margin-top:2px;">
                    </div>
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Pre-Blast CH4 (20m radius)</span>
                        <input type="number" step="0.05" id="blast-ch4" required placeholder="< 0.5%" oninput="verifyPreBlastGas(this.value)" style="width:100%; background:transparent; border:none; color:#4ade80; font-weight:bold; font-size:13px; margin-top:2px;">
                    </div>
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Post-Blast Examination</span>
                        <select id="misfire-check" style="width:100%; background:transparent; border:none; color:#4ade80; font-weight:bold; font-size:11px; margin-top:2px;">
                            <option value="All Holes Fired (Zero Misfire)">All Clear (Zero Misfire)</option>
                            <option value="MISFIRE DETECTED">⚠️ MISFIRE DETECTED</option>
                            <option value="Socket Relieved & Inspected">Socket Cleared</option>
                        </select>
                    </div>
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Fume Clearance Time</span>
                        <select id="fume-time" style="width:100%; background:transparent; border:none; color:#cbd5e1; font-size:11px; margin-top:2px;">
                            <option value="30 mins (Standard)">30 Minutes</option>
                            <option value="45 mins (Extended)">45 Minutes</option>
                            <option value="60 mins (Heavy Round)">60 Minutes</option>
                        </select>
                    </div>
                </div>

                <button type="submit" id="submit-blast-btn" style="width:100%; background:#d97706; color:#fff; font-weight:bold; border:none; padding:10px; border-radius:6px; font-size:12px; cursor:pointer;">
                    ⚡ Certify Blasting Round (CMR 204)
                </button>
            </form>

            <!-- Blasting History Register -->
            <div style="margin-top:14px; border-top:1px solid #1e293b; padding-top:10px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                    <div style="font-size:11px; font-weight:bold; color:#cbd5e1;">Shotfiring Log History (Form-VII Annexure)</div>
                    <span id="blast-count-badge" style="background:#334155; color:#cbd5e1; font-size:9px; padding:2px 6px; border-radius:8px;">0 Rounds</span>
                </div>
                <div id="blasting-log-list" style="max-height:120px; overflow-y:auto; font-size:10px; color:#94a3b8;">
                    No blasting rounds registered in current shift.
                </div>
            </div>
        `;

        container.appendChild(card);
        renderBlastingLogs();
    }

    window.verifyPreBlastGas = function(val) {
        var ch4 = parseFloat(val);
        var statusBadge = document.getElementById('blast-clearance-status');
        var input = document.getElementById('blast-ch4');
        var submitBtn = document.getElementById('submit-blast-btn');
        if (isNaN(ch4) || !statusBadge) return;

        // DGMS Regulation 204: Prohibited to charge or fire if CH4 exceeds 0.5%
        if (ch4 >= 0.5) {
            statusBadge.style.background = '#7f1d1d';
            statusBadge.style.color = '#fca5a5';
            statusBadge.style.borderColor = '#ef4444';
            statusBadge.innerText = '🚨 BLASTING PROHIBITED (CH4 ≥ 0.5%)';
            input.style.color = '#ef4444';
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.style.background = '#475569';
                submitBtn.style.cursor = 'not-allowed';
            }
        } else {
            statusBadge.style.background = '#14532d';
            statusBadge.style.color = '#4ade80';
            statusBadge.style.borderColor = '#22c55e';
            statusBadge.innerText = '✓ CLEAR TO CHARGE';
            input.style.color = '#4ade80';
            if (submitBtn) {
                submitBtn.disabled = false;
                submitBtn.style.background = '#d97706';
                submitBtn.style.cursor = 'pointer';
            }
        }
    };

    window.recordBlastingRound = function(e) {
        if (e) e.preventDefault();
        var face = document.getElementById('blast-face').value;
        var shotfirer = document.getElementById('shotfirer-name').value;
        var expClass = document.getElementById('explosive-class').value;
        var expQty = document.getElementById('explosive-qty').value;
        var dets = document.getElementById('detonators-count').value;
        var ch4 = parseFloat(document.getElementById('blast-ch4').value) || 0;
        var misfire = document.getElementById('misfire-check').value;
        var fumes = document.getElementById('fume-time').value;

        if (ch4 >= 0.5) {
            alert('CMR 204 VIOLATION: Cannot fire round with CH4 ≥ 0.5%!');
            return;
        }

        var entry = {
            id: 'BLAST-' + Date.now(),
            date: new Date().toLocaleDateString(),
            time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
            face: face,
            shotfirer: shotfirer,
            explosive: expQty + ' Kg (' + expClass + ')',
            dets: dets,
            ch4: ch4 + '%',
            misfire: misfire,
            fumes: fumes,
            seal: 'BLAST-SEAL-' + Math.random().toString(36).substring(2, 8).toUpperCase()
        };

        var store = JSON.parse(localStorage.getItem('dgms_blasting_logs') || '[]');
        store.unshift(entry);
        localStorage.setItem('dgms_blasting_logs', JSON.stringify(store));

        document.getElementById('blast-face').value = '';
        document.getElementById('explosive-qty').value = '';
        document.getElementById('detonators-count').value = '';
        renderBlastingLogs();
        alert('✅ Shotfiring Round Certified with Authority Seal ' + entry.seal);
    };

    function renderBlastingLogs() {
        var el = document.getElementById('blasting-log-list');
        var badge = document.getElementById('blast-count-badge');
        if (!el) return;
        var store = JSON.parse(localStorage.getItem('dgms_blasting_logs') || '[]');

        if (badge) badge.innerText = store.length + ' Rounds';

        if (store.length === 0) {
            el.innerHTML = '<div style="color:#64748b; padding:4px;">No blasting rounds registered in current shift.</div>';
            return;
        }

        el.innerHTML = store.map(function(item) {
            var misfireColor = (item.misfire.indexOf('MISFIRE') !== -1) ? '#ef4444' : '#4ade80';
            return `
                <div style="background:#020617; border:1px solid #1e293b; padding:6px 8px; border-radius:4px; margin-bottom:4px;">
                    <div style="display:flex; justify-content:space-between; font-weight:bold;">
                        <span style="color:#f59e0b;">${item.face}</span>
                        <span style="font-family:monospace; color:#38bdf8; font-size:9px;">${item.seal}</span>
                    </div>
                    <div style="display:flex; justify-content:space-between; color:#cbd5e1; margin-top:2px;">
                        <span>Exp: <b>${item.explosive}</b> (${item.dets} Dets)</span>
                        <span>Pre-Blast CH4: <b>${item.ch4}</b></span>
                        <span style="color:${misfireColor}; font-weight:bold;">${item.misfire}</span>
                    </div>
                    <div style="color:#64748b; font-size:9px; margin-top:2px;">
                        ${item.date} ${item.time} • Shotfirer: ${item.shotfirer} • Fume Interval: ${item.fumes}
                    </div>
                </div>
            `;
        }).join('');
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', injectBlastingUI);
    } else {
        injectBlastingUI();
    }
    setTimeout(injectBlastingUI, 2000);
})();
</script>
"""
