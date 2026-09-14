# ui_lamproom.py - Standalone DGMS CMR 171 Lamp Room Register & Cap Lamp Battery Health Engine

LAMPROOM_MODULE = """
<script>
(function() {
    function injectLampRoomUI() {
        if (document.getElementById('statutory-lamproom-card')) return;

        var container = document.querySelector('.grid-container') || document.body;

        var card = document.createElement('div');
        card.id = 'statutory-lamproom-card';
        card.style.cssText = 'background:#0f172a; border:1px solid #334155; border-radius:10px; padding:16px; margin:14px 0; color:#f8fafc; font-family:system-ui, sans-serif; box-shadow:0 4px 6px -1px rgba(0,0,0,0.5);';

        card.innerHTML = `
            <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #1e293b; padding-bottom:10px; margin-bottom:12px;">
                <div style="display:flex; align-items:center; gap:8px;">
                    <span style="font-size:18px;">💡</span>
                    <div>
                        <div style="font-size:13px; font-weight:bold; color:#38bdf8;">LAMP ROOM ATTENDANCE & BATTERY HEALTH REGISTER</div>
                        <div style="font-size:10px; color:#94a3b8;">DGMS CMR 2017 Reg 171 - Cap Lamp Issuance, Underground Headcount & Lux Audit</div>
                    </div>
                </div>
                <div id="lamproom-headcount-badge" style="background:#14532d; color:#4ade80; border:1px solid #22c55e; font-size:10px; padding:3px 8px; border-radius:12px; font-weight:bold;">
                    0 MINERS UNDERGROUND
                </div>
            </div>

            <!-- Cap Lamp Issue / Return Form -->
            <form id="lamproom-form" onsubmit="recordLampAction(event)">
                <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap:10px; margin-bottom:10px;">
                    <div>
                        <label style="font-size:11px; color:#94a3b8;">Action Type</label>
                        <select id="lamp-action-type" onchange="toggleLampAction()" style="width:100%; background:#020617; border:1px solid #334155; color:#38bdf8; font-weight:bold; padding:8px; border-radius:6px; font-size:11px; margin-top:4px;">
                            <option value="ISSUE">ISSUE: Lamp In to Pit (Entry)</option>
                            <option value="RETURN">RETURN: Lamp Out of Pit (Exit)</option>
                        </select>
                    </div>
                    <div>
                        <label style="font-size:11px; color:#94a3b8;">Cap Lamp Number</label>
                        <input type="text" id="lamp-number" required placeholder="e.g. L-418" style="width:100%; background:#020617; border:1px solid #334155; color:#fff; padding:8px; border-radius:6px; font-size:11px; margin-top:4px;">
                    </div>
                    <div>
                        <label style="font-size:11px; color:#94a3b8;">Miner Name & Token / Bio-ID</label>
                        <input type="text" id="lamp-miner-id" required placeholder="e.g. Sunil Mahato (TK-309)" style="width:100%; background:#020617; border:1px solid #334155; color:#fff; padding:8px; border-radius:6px; font-size:11px; margin-top:4px;">
                    </div>
                </div>

                <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap:8px; margin-bottom:12px;">
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Battery Terminal Voltage</span>
                        <input type="number" step="0.05" id="lamp-voltage" required placeholder="Min 4.0V" oninput="evaluateLampHealth()" style="width:100%; background:transparent; border:none; color:#4ade80; font-weight:bold; font-size:13px; margin-top:2px;">
                    </div>
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Photometric Lux Output</span>
                        <select id="lamp-lux-status" onchange="evaluateLampHealth()" style="width:100%; background:transparent; border:none; color:#4ade80; font-weight:bold; font-size:11px; margin-top:2px;">
                            <option value="Adequate (>1500 Lux Peak)">Adequate (>1500 Lux)</option>
                            <option value="Marginal (1000-1500 Lux)">Marginal (1000-1500 Lux)</option>
                            <option value="Dim (<1000 Lux Defective)">⚠️ Dim (<1000 Lux Defective)</option>
                        </select>
                    </div>
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Magnetic Lock & Cable Sheath</span>
                        <select id="lamp-lock-status" onchange="evaluateLampHealth()" style="width:100%; background:transparent; border:none; color:#4ade80; font-weight:bold; font-size:11px; margin-top:2px;">
                            <option value="Locked & Lead-Sealed Intact">Locked & Sealed Intact</option>
                            <option value="Lead Seal Broken">⚠️ Lead Seal Broken</option>
                            <option value="Cable Armor Cut / Exposed">⚠️ Cable Exposed</option>
                        </select>
                    </div>
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Certified Lamp Incharge</span>
                        <input type="text" id="lamp-incharge" required placeholder="Name & Token" style="width:100%; background:transparent; border:none; color:#cbd5e1; font-size:11px; margin-top:2px;">
                    </div>
                </div>

                <div id="lamproom-statutory-msg" style="background:#020617; border:1px dashed #334155; padding:8px; border-radius:6px; margin-bottom:12px; font-size:11px; color:#cbd5e1;">
                    CMR 171 Check: Cap lamps must maintain >4.0V battery voltage, intact magnetic lock, and valid photometrics before entering flammable coal horizons.
                </div>

                <button type="submit" id="submit-lamp-btn" style="width:100%; background:#0284c7; color:#fff; font-weight:bold; border:none; padding:10px; border-radius:6px; font-size:12px; cursor:pointer;">
                    💡 Register Lamp Issuance (Entry to Pit)
                </button>
            </form>

            <!-- Lamp Ledger & Currently Underground Table -->
            <div style="margin-top:14px; border-top:1px solid #1e293b; padding-top:10px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                    <div style="font-size:11px; font-weight:bold; color:#cbd5e1;">Statutory Lamp Accountability Ledger (CMR 171)</div>
                    <span id="lamproom-logs-count" style="background:#334155; color:#cbd5e1; font-size:9px; padding:2px 6px; border-radius:8px;">0 Transactions</span>
                </div>
                <div id="lamproom-history-list" style="max-height:130px; overflow-y:auto; font-size:10px; color:#94a3b8;">
                    No lamp room transactions logged for current shift.
                </div>
            </div>
        `;

        container.appendChild(card);
        renderLampLogs();
    }

    window.toggleLampAction = function() {
        var action = document.getElementById('lamp-action-type').value;
        var btn = document.getElementById('submit-lamp-btn');
        if (!btn) return;

        if (action === 'ISSUE') {
            btn.style.background = '#0284c7';
            btn.innerText = '💡 Register Lamp Issuance (Entry to Pit)';
        } else {
            btn.style.background = '#16a34a';
            btn.innerText = '📥 Register Lamp Return (Pit Exit & Recharge)';
        }
        window.evaluateLampHealth();
    };

    window.evaluateLampHealth = function() {
        var action = document.getElementById('lamp-action-type').value;
        var voltage = parseFloat(document.getElementById('lamp-voltage').value) || 4.2;
        var lux = document.getElementById('lamp-lux-status').value;
        var lock = document.getElementById('lamp-lock-status').value;
        var msg = document.getElementById('lamproom-statutory-msg');
        var btn = document.getElementById('submit-lamp-btn');

        if (!msg) return;

        var isDefective = (voltage < 3.8 || lux.indexOf('Dim') !== -1 || lock.indexOf('Broken') !== -1 || lock.indexOf('Exposed') !== -1);

        if (action === 'ISSUE' && isDefective) {
            msg.innerHTML = '<span style="color:#ef4444; font-weight:bold;">DEFECT TAGGED:</span> Lamp failed pre-entry standard (Voltage <3.8V, seal breached, or dim output). Under CMR 171, issuance is prohibited.';
            if (btn) {
                btn.style.background = '#dc2626';
                btn.innerText = '⛔ Lamp Issue Blocked (Defective Safety Apparatus)';
            }
            return false;
        } else {
            msg.innerHTML = '<span style="color:#4ade80; font-weight:bold;">READY:</span> Lamp verified fit. Lead seal intact and battery condition optimal for full 8-hour shift.';
            if (btn && action === 'ISSUE') {
                btn.style.background = '#0284c7';
                btn.innerText = '💡 Register Lamp Issuance (Entry to Pit)';
            }
            return true;
        }
    };

    window.recordLampAction = function(e) {
        if (e) e.preventDefault();
        var action = document.getElementById('lamp-action-type').value;
        var lampNo = document.getElementById('lamp-number').value.trim();
        var miner = document.getElementById('lamp-miner-id').value.trim();
        var voltage = document.getElementById('lamp-voltage').value;
        var lux = document.getElementById('lamp-lux-status').value;
        var lock = document.getElementById('lamp-lock-status').value;
        var incharge = document.getElementById('lamp-incharge').value.trim();

        var isIssue = (action === 'ISSUE');
        var isFit = window.evaluateLampHealth();

        if (isIssue && !isFit) {
            alert('🚨 STATUTORY PROHIBITION: Defective safety lamp cannot be taken underground (CMR 171). Replace lamp or battery unit.');
            return;
        }

        var store = JSON.parse(localStorage.getItem('dgms_lamproom_logs') || '[]');

        var entry = {
            id: 'LAMP-' + Date.now(),
            action: action,
            date: new Date().toLocaleDateString(),
            time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
            lampNo: lampNo,
            miner: miner,
            voltage: voltage + 'V',
            lux: lux,
            lock: lock,
            incharge: incharge,
            seal: 'LAMP-SEAL-' + Math.random().toString(36).substring(2, 8).toUpperCase()
        };

        store.unshift(entry);
        localStorage.setItem('dgms_lamproom_logs', JSON.stringify(store));

        document.getElementById('lamp-number').value = '';
        document.getElementById('lamp-miner-id').value = '';
        renderLampLogs();

        alert((isIssue ? '✅ Lamp Issued (Pit Entry Registered)' : '✅ Lamp Returned (Shift Exit Cleared)') + ' | Seal ' + entry.seal);
    };

    function renderLampLogs() {
        var el = document.getElementById('lamproom-history-list');
        var badge = document.getElementById('lamproom-headcount-badge');
        var countEl = document.getElementById('lamproom-logs-count');
        if (!el) return;

        var store = JSON.parse(localStorage.getItem('dgms_lamproom_logs') || '[]');
        if (countEl) countEl.innerText = store.length + ' Transactions';

        // Calculate current active underground lamps (Issued minus Returned per lamp)
        var activeLamps = {};
        for (var i = store.length - 1; i >= 0; i--) {
            var item = store[i];
            if (item.action === 'ISSUE') {
                activeLamps[item.lampNo] = item.miner;
            } else if (item.action === 'RETURN') {
                delete activeLamps[item.lampNo];
            }
        }

        var undergroundCount = Object.keys(activeLamps).length;
        if (badge) {
            badge.innerText = undergroundCount + ' MINERS UNDERGROUND';
            if (undergroundCount > 0) {
                badge.style.background = '#78350f';
                badge.style.color = '#fde68a';
                badge.style.borderColor = '#f59e0b';
            } else {
                badge.style.background = '#14532d';
                badge.style.color = '#4ade80';
                badge.style.borderColor = '#22c55e';
            }
        }

        if (store.length === 0) {
            el.innerHTML = '<div style="color:#64748b; padding:4px;">No lamp room transactions logged for current shift.</div>';
            return;
        }

        el.innerHTML = store.map(function(item) {
            var isIssue = (item.action === 'ISSUE');
            var col = isIssue ? '#38bdf8' : '#4ade80';
            var tagBg = isIssue ? '#082f49' : '#052e16';
            return `
                <div style="background:#020617; border:1px solid #1e293b; padding:6px 8px; border-radius:4px; margin-bottom:4px;">
                    <div style="display:flex; justify-content:space-between; font-weight:bold;">
                        <span style="color:${col};">${item.action === 'ISSUE' ? '📤' : '📥'} Lamp ${item.lampNo} (${item.miner})</span>
                        <span style="font-family:monospace; color:#f59e0b; font-size:9px;">${item.seal}</span>
                    </div>
                    <div style="display:flex; justify-content:space-between; color:#cbd5e1; margin-top:2px;">
                        <span>Batt: <b>${item.voltage}</b> | Lock: <b>${item.lock.slice(0, 14)}...</b></span>
                        <span style="background:${tagBg}; color:${col}; padding:1px 6px; border-radius:4px; font-weight:bold; font-size:9px;">${item.action}</span>
                    </div>
                    <div style="color:#64748b; font-size:9px; margin-top:2px;">
                        ${item.date} ${item.time} • Lux: ${item.lux.slice(0, 12)} • Issued By: ${item.incharge}
                    </div>
                </div>
            `;
        }).join('');
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', injectLampRoomUI);
    } else {
        injectLampRoomUI();
    }
    setTimeout(injectLampRoomUI, 4600);
})();
</script>
"""
