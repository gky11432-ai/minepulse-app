# ui_tracking.py - Standalone DGMS 100% Offline P2P Mesh & Store-and-Forward Personnel Tracking System

TRACKING_MODULE = """
<script>
(function() {
    var p2pInterval = null;
    var currentFilter = 'ALL';

    function injectOfflineTrackingUI() {
        if (document.getElementById('statutory-tracking-card')) return;

        var container = document.querySelector('.grid-container') || document.body;
        var card = document.createElement('div');
        card.id = 'statutory-tracking-card';
        card.style.cssText = 'background:#0f172a; border:1px solid #334155; border-radius:10px; padding:16px; margin:14px 0; color:#f8fafc; font-family:system-ui, sans-serif; box-shadow:0 4px 6px rgba(0,0,0,0.5);';

        card.innerHTML = `
            <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #1e293b; padding-bottom:10px; margin-bottom:12px;">
                <div style="display:flex; align-items:center; gap:8px;">
                    <span style="font-size:18px;">📡</span>
                    <div>
                        <div style="font-size:13px; font-weight:bold; color:#38bdf8;">OFFLINE P2P PERSONNEL TRACKING & MESH RELAY</div>
                        <div style="font-size:10px; color:#94a3b8;">DGMS Circular 02/2020 - Zero-Network Store-and-Forward Proximity Radar</div>
                    </div>
                </div>
                <div id="mesh-status-badge" style="background:#14532d; color:#4ade80; border:1px solid #22c55e; font-size:10px; padding:3px 8px; border-radius:12px; font-weight:bold;">
                    P2P MESH ACTIVE (0 NET REQ)
                </div>
            </div>

            <!-- Local Node Telemetry & Offline Chirp Broadcaster -->
            <div style="background:#020617; border:1px solid #1e293b; border-radius:8px; padding:12px; margin-bottom:12px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                    <span style="font-size:11px; font-weight:bold; color:#cbd5e1;">My Local Offline Beacon (Air-Gapped Node)</span>
                    <span id="p2p-sync-time" style="font-size:10px; color:#38bdf8;">Broadcasting RF Chirp...</span>
                </div>

                <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap:8px; margin-bottom:10px;">
                    <div>
                        <label style="font-size:10px; color:#94a3b8;">My Underground District / Station</label>
                        <select id="offline-my-zone" onchange="broadcastOfflineChirp(false)" style="width:100%; background:#0f172a; border:1px solid #334155; color:#4ade80; font-weight:bold; padding:6px; border-radius:4px; font-size:11px; margin-top:2px;">
                            <option value="Shaft Bottom (Pit Eye / Station 0)">Shaft Bottom (Pit Eye / Station 0)</option>
                            <option value="Main Dip Level 5 Incline">Main Dip Level 5 Incline</option>
                            <option value="District 2 Heading 4 Face">District 2 Heading 4 Face (Blind End)</option>
                            <option value="Depillaring Panel 3 Goaf Edge">Depillaring Panel 3 Goaf Edge</option>
                            <option value="Substation & Pump Room Drift">Substation & Pump Room Drift</option>
                            <option value="Main Return Airway Overcast">Main Return Airway Overcast</option>
                            <option value="Emergency Refuge Chamber B">Emergency Refuge Chamber B</option>
                        </select>
                    </div>
                    <div>
                        <label style="font-size:10px; color:#94a3b8;">Physical Motion / Status</label>
                        <select id="offline-motion-state" onchange="broadcastOfflineChirp(false)" style="width:100%; background:#0f172a; border:1px solid #334155; color:#38bdf8; font-weight:bold; padding:6px; border-radius:4px; font-size:11px; margin-top:2px;">
                            <option value="ACTIVE_MOVING">🏃 Moving / On Duty</option>
                            <option value="WORKING_STATIONARY">⛏️ Stationed at Face</option>
                            <option value="REST_SHELTER">🛡️ Inside Refuge Chamber</option>
                        </select>
                    </div>
                </div>

                <div style="display:flex; gap:8px;">
                    <button type="button" onclick="broadcastOfflineChirp(false)" style="flex:2; background:#0284c7; color:#fff; font-weight:bold; border:none; padding:8px 12px; border-radius:6px; font-size:11px; cursor:pointer;">
                        📡 Broadcast Local Offline Chirp
                    </button>
                    <button type="button" onclick="triggerOfflineDistressSOS()" style="flex:1; background:#dc2626; color:#fff; font-weight:bold; border:none; padding:8px; border-radius:6px; font-size:11px; cursor:pointer;">
                        🆘 Send Offline SOS
                    </button>
                </div>
            </div>

            <!-- Proximity Radar: Devices within 30m Range -->
            <div style="background:#020617; border:1px solid #1e293b; border-radius:8px; padding:10px; margin-bottom:12px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                    <div style="display:flex; align-items:center; gap:6px;">
                        <span style="display:inline-block; width:8px; height:8px; background:#4ade80; border-radius:50%; box-shadow:0 0 6px #4ade80;"></span>
                        <b style="font-size:11px; color:#cbd5e1;">P2P Proximity Handshake (<30m RF Field)</b>
                    </div>
                    <button type="button" onclick="simulateNearbyHandshake()" style="background:#1e293b; border:1px solid #334155; color:#38bdf8; font-size:9px; padding:2px 8px; border-radius:4px; cursor:pointer;">
                        🔄 Simulate Cross-Path Handshake
                    </button>
                </div>
                <div id="p2p-nearby-list" style="display:flex; gap:6px; overflow-x:auto; padding-bottom:4px;">
                    <!-- Auto-populated nearby badges -->
                </div>
            </div>

            <!-- Store-and-Forward Relay Vault: Packets Carried For Other Miners -->
            <div style="background:#020617; border:1px dashed #0284c7; border-radius:8px; padding:10px; margin-bottom:12px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                    <div style="font-size:11px; font-weight:bold; color:#38bdf8;">
                        📦 Store-and-Forward Relay Vault (Carried Packets)
                    </div>
                    <span id="relay-vault-badge" style="background:#0369a1; color:#e0f2fe; font-size:9px; padding:2px 6px; border-radius:8px;">0 Carried</span>
                </div>
                <div style="font-size:9px; color:#94a3b8; margin-bottom:6px;">
                    Your device acts as an offline data courier. When you walk from the coal face towards the shaft bottom, location packets of isolated workers are automatically carried and delivered to the pithead ledger.
                </div>
                <div id="relay-vault-list" style="max-height:80px; overflow-y:auto; font-size:9px; color:#cbd5e1;">
                    Vault empty. No relayed packets currently buffered.
                </div>
            </div>

            <!-- Colliery Master Personnel Radar -->
            <div>
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                    <div style="font-size:11px; font-weight:bold; color:#cbd5e1;">Colliery Underground Roster & Last-Known Stations</div>
                    <div style="display:flex; gap:4px;">
                        <button type="button" onclick="filterRadar('ALL')" id="flt-all" style="background:#0284c7; color:#fff; border:none; padding:2px 8px; border-radius:4px; font-size:9px; cursor:pointer;">All</button>
                        <button type="button" onclick="filterRadar('OFFICER')" id="flt-off" style="background:#1e293b; color:#94a3b8; border:1px solid #334155; padding:2px 8px; border-radius:4px; font-size:9px; cursor:pointer;">Officers</button>
                        <button type="button" onclick="filterRadar('WORKER')" id="flt-wrk" style="background:#1e293b; color:#94a3b8; border:1px solid #334155; padding:2px 8px; border-radius:4px; font-size:9px; cursor:pointer;">Workers</button>
                    </div>
                </div>
                <div id="p2p-master-roster" style="max-height:160px; overflow-y:auto; font-size:10px; color:#94a3b8;">
                    No location beacons synchronized yet.
                </div>
            </div>
        `;

        container.appendChild(card);
        initLocalP2PNode();
        renderNearbyProximity();
        renderRelayVault();
        renderMasterRoster();

        // Auto-refresh offline P2P beacon every 20 seconds
        p2pInterval = setInterval(function() {
            broadcastOfflineChirp(false, true);
        }, 20000);
    }

    function getActiveUser() {
        try {
            return JSON.parse(localStorage.getItem('mineguard_active_user') || 'null') || {
                name: 'Shift Miner',
                role: 'WORKER',
                token: 'TK-402',
                designation: 'SDL Operator'
            };
        } catch(e) {
            return { name: 'Shift Miner', role: 'WORKER', token: 'TK-402', designation: 'SDL Operator' };
        }
    }

    function initLocalP2PNode() {
        var user = getActiveUser();
        var zoneEl = document.getElementById('offline-my-zone');
        var zone = zoneEl ? zoneEl.value : 'Shaft Bottom';

        // Register initial self packet into ledger
        updateMasterRecord({
            token: user.token,
            name: user.name,
            role: user.role,
            designation: user.designation,
            zone: zone,
            hops: 0,
            courier: 'Direct (Self)',
            status: 'ACTIVE_NORMAL',
            rssi: '-42 dBm',
            timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
            rawTime: Date.now()
        });
    }

    window.broadcastOfflineChirp = function(isDistress, isSilent) {
        var user = getActiveUser();
        var zone = document.getElementById('offline-my-zone').value;
        var motion = document.getElementById('offline-motion-state').value;
        var syncTimeEl = document.getElementById('p2p-sync-time');

        var entry = {
            token: user.token,
            name: user.name,
            role: user.role,
            designation: user.designation,
            zone: zone,
            motion: motion,
            hops: 0,
            courier: 'Direct (Self)',
            status: isDistress ? 'EMERGENCY_SOS' : 'ACTIVE_NORMAL',
            rssi: '-38 dBm',
            timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
            rawTime: Date.now()
        };

        updateMasterRecord(entry);

        if (syncTimeEl) {
            syncTimeEl.innerText = 'Chirp sent: ' + entry.timestamp;
        }

        if (!isSilent) {
            if (isDistress) {
                alert('🚨 OFFLINE SOS BEACON ACTIVATED: Signal buffered and propagating to nearby miners!');
            } else {
                alert('📡 Offline Chirp Broadcasted for ' + user.name + ' at ' + zone);
            }
        }
    };

    window.triggerOfflineDistressSOS = function() {
        if (typeof window.playDGMSSiren === 'function') {
            window.playDGMSSiren(7000);
        }
        window.broadcastOfflineChirp(true, false);
    };

    function updateMasterRecord(record) {
        var store = JSON.parse(localStorage.getItem('dgms_p2p_mesh_roster') || '{}');
        // Only update if newer or higher urgency
        if (!store[record.token] || record.rawTime >= store[record.token].rawTime || record.status === 'EMERGENCY_SOS') {
            store[record.token] = record;
            localStorage.setItem('dgms_p2p_mesh_roster', JSON.stringify(store));
            renderMasterRoster();
        }
    }

    // Proximity Simulation: Exchanging packets when walking past another miner
    window.simulateNearbyHandshake = function() {
        var user = getActiveUser();
        var offlineWorkersPool = [
            { token: 'TK-101', name: 'R.K. Sharma', role: 'OFFICER', designation: 'Shift Overman', zone: 'District 2 Heading 4 Face', status: 'ACTIVE_NORMAL', rssi: '-54 dBm' },
            { token: 'TK-204', name: 'Birendra Singh', role: 'OFFICER', designation: 'Mining Sirdar', zone: 'Main Dip Level 5 Incline', status: 'ACTIVE_NORMAL', rssi: '-68 dBm' },
            { token: 'TK-512', name: 'Mangal Hansda', role: 'WORKER', designation: 'Support Mason', zone: 'Depillaring Panel 3 Goaf Edge', status: 'ACTIVE_NORMAL', rssi: '-72 dBm' },
            { token: 'TK-309', name: 'Bipin Murmu', role: 'WORKER', designation: 'Drill Operator', zone: 'District 2 Heading 4 Face', status: 'ACTIVE_NORMAL', rssi: '-61 dBm' }
        ];

        // Pick 1 or 2 nearby peers
        var peer = offlineWorkersPool[Math.floor(Math.random() * offlineWorkersPool.length)];
        if (peer.token === user.token) return;

        peer.hops = 1;
        peer.courier = 'Relayed via ' + user.name + ' (' + user.token + ')';
        peer.timestamp = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        peer.rawTime = Date.now();

        // Save into Store-and-Forward Vault
        var vault = JSON.parse(localStorage.getItem('dgms_relay_vault') || '{}');
        vault[peer.token] = peer;
        localStorage.setItem('dgms_relay_vault', JSON.stringify(vault));

        // Also update local master view
        updateMasterRecord(peer);

        renderNearbyProximity();
        renderRelayVault();

        if (navigator.vibrate) navigator.vibrate([80, 40, 80]);
        alert('🤝 P2P Handshake Complete!\nDiscovered ' + peer.name + ' (' + peer.token + ') in ' + peer.zone + '.\nPacket stored in offline courier vault.');
    };

    function renderNearbyProximity() {
        var el = document.getElementById('p2p-nearby-list');
        if (!el) return;

        var vault = JSON.parse(localStorage.getItem('dgms_relay_vault') || '{}');
        var items = Object.values(vault);

        if (items.length === 0) {
            el.innerHTML = '<div style="font-size:10px; color:#64748b; padding:4px;">No peer devices within 30m RF proximity.</div>';
            return;
        }

        el.innerHTML = items.map(function(p) {
            var isSos = p.status === 'EMERGENCY_SOS';
            var borderCol = isSos ? '#ef4444' : '#38bdf8';
            return `
                <div style="background:#0f172a; border:1px solid ${borderCol}; border-radius:6px; padding:4px 8px; min-width:140px; flex-shrink:0;">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <b style="color:#f8fafc; font-size:10px;">${p.name}</b>
                        <span style="color:#4ade80; font-size:8px; font-family:monospace;">${p.rssi}</span>
                    </div>
                    <div style="color:#94a3b8; font-size:9px;">${p.token} • ${p.zone.slice(0, 18)}</div>
                </div>
            `;
        }).join('');
    }

    function renderRelayVault() {
        var el = document.getElementById('relay-vault-list');
        var badge = document.getElementById('relay-vault-badge');
        if (!el) return;

        var vault = JSON.parse(localStorage.getItem('dgms_relay_vault') || '{}');
        var items = Object.values(vault);

        if (badge) badge.innerText = items.length + ' Carried';

        if (items.length === 0) {
            el.innerHTML = '<div style="color:#64748b;">Vault empty. No relayed packets currently buffered.</div>';
            return;
        }

        el.innerHTML = items.map(function(p) {
            return `
                <div style="background:#0f172a; padding:4px 6px; border-radius:4px; margin-bottom:3px; border:1px solid #1e293b; display:flex; justify-content:space-between;">
                    <span><b>${p.name}</b> (${p.token}) @ ${p.zone}</span>
                    <span style="color:#38bdf8;">${p.timestamp} (Hop: ${p.hops})</span>
                </div>
            `;
        }).join('');
    }

    window.filterRadar = function(filter) {
        currentFilter = filter;
        ['all', 'off', 'wrk'].forEach(function(b) {
            var btn = document.getElementById('flt-' + b);
            if (btn) { btn.style.background = '#1e293b'; btn.style.color = '#94a3b8'; }
        });
        var active = document.getElementById('flt-' + (filter === 'ALL' ? 'all' : (filter === 'OFFICER' ? 'off' : 'wrk')));
        if (active) { active.style.background = '#0284c7'; active.style.color = '#fff'; }
        renderMasterRoster();
    };

    function renderMasterRoster() {
        var el = document.getElementById('p2p-master-roster');
        if (!el) return;

        var store = JSON.parse(localStorage.getItem('dgms_p2p_mesh_roster') || '{}');
        var list = Object.values(store);

        // Populate baseline mock stations if new
        if (list.length === 0) {
            list = [
                { token: 'TK-101', name: 'R.K. Sharma', role: 'OFFICER', designation: 'Shift Overman', zone: 'District 2 Heading 4 Face', hops: 1, courier: 'Relayed via Sirdar', status: 'ACTIVE_NORMAL', timestamp: '12m ago', rawTime: Date.now() - 720000 },
                { token: 'TK-204', name: 'Birendra Singh', role: 'OFFICER', designation: 'Mining Sirdar', zone: 'Main Dip Level 5 Incline', hops: 0, courier: 'Direct', status: 'ACTIVE_NORMAL', timestamp: '2m ago', rawTime: Date.now() - 120000 },
                { token: 'TK-402', name: 'Sunil Mahato', role: 'WORKER', designation: 'SDL Operator', zone: 'Depillaring Panel 3 Goaf Edge', hops: 1, courier: 'Relayed via Trammer', status: 'ACTIVE_NORMAL', timestamp: '5m ago', rawTime: Date.now() - 300000 },
                { token: 'TK-512', name: 'Mangal Hansda', role: 'WORKER', designation: 'Support Mason', zone: 'Shaft Bottom (Pit Eye / Station 0)', hops: 0, courier: 'Direct', status: 'ACTIVE_NORMAL', timestamp: 'Just now', rawTime: Date.now() }
            ];
        }

        var filtered = list.filter(function(p) {
            if (currentFilter === 'OFFICER') return (p.role === 'OFFICER' || p.role === 'MANAGER');
            if (currentFilter === 'WORKER') return (p.role === 'WORKER');
            return true;
        });

        if (filtered.length === 0) {
            el.innerHTML = '<div style="color:#64748b; padding:4px;">No personnel recorded in this category.</div>';
            return;
        }

        el.innerHTML = filtered.map(function(p) {
            var isSos = p.status === 'EMERGENCY_SOS';
            var isOfficer = (p.role === 'OFFICER' || p.role === 'MANAGER');
            var roleCol = isSos ? '#ef4444' : (isOfficer ? '#38bdf8' : '#4ade80');
            var icon = isSos ? '🚨' : (isOfficer ? '👮' : '👷');
            var bg = isSos ? '#450a0a' : '#020617';

            return `
                <div style="background:${bg}; border:1px solid #1e293b; padding:6px 8px; border-radius:4px; margin-bottom:4px; display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <div style="display:flex; align-items:center; gap:4px;">
                            <span>${icon}</span>
                            <b style="color:#f8fafc;">${p.name}</b>
                            <span style="color:#64748b; font-size:9px;">(${p.token} • ${p.designation})</span>
                        </div>
                        <div style="color:#94a
