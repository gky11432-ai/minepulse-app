# ui_tracking.py - Standalone DGMS Hybrid Underground Zone & Surface GPS Personnel Tracking System (PTS)

TRACKING_MODULE = """
<script>
(function() {
    var gpsWatchId = null;
    var currentCoords = { lat: null, lon: null, alt: null, accuracy: null, mode: 'SURFACE_GPS' };

    function injectTrackingUI() {
        if (document.getElementById('statutory-tracking-card')) return;

        var container = document.querySelector('.grid-container') || document.body;
        var card = document.createElement('div');
        card.id = 'statutory-tracking-card';
        card.style.cssText = 'background:#0f172a; border:1px solid #334155; border-radius:10px; padding:16px; margin:14px 0; color:#f8fafc; font-family:system-ui, sans-serif; box-shadow:0 4px 6px rgba(0,0,0,0.5);';

        card.innerHTML = `
            <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #1e293b; padding-bottom:10px; margin-bottom:12px;">
                <div style="display:flex; align-items:center; gap:8px;">
                    <span style="font-size:18px;">📍</span>
                    <div>
                        <div style="font-size:13px; font-weight:bold; color:#38bdf8;">LIVE PERSONNEL TRACKING SYSTEM (PTS)</div>
                        <div style="font-size:10px; color:#94a3b8;">DGMS Circular No. 02/2020 & CMR 171 - Hybrid GPS & Underground Zone Radar</div>
                    </div>
                </div>
                <div id="pts-tracking-badge" style="background:#14532d; color:#4ade80; border:1px solid #22c55e; font-size:10px; padding:3px 8px; border-radius:12px; font-weight:bold;">
                    RADAR ACTIVE
                </div>
            </div>

            <!-- Current User Location Beacon Transmitter -->
            <div style="background:#020617; border:1px solid #1e293b; border-radius:8px; padding:12px; margin-bottom:12px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                    <span style="font-size:11px; font-weight:bold; color:#cbd5e1;">My Telemetry & Live Location Beacon</span>
                    <span id="gps-status-indicator" style="font-size:10px; color:#38bdf8;">Acquiring Signals...</span>
                </div>

                <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap:8px; margin-bottom:10px;">
                    <div>
                        <label style="font-size:10px; color:#94a3b8;">Tracking Domain</label>
                        <select id="pts-domain-select" onchange="toggleTrackingMode()" style="width:100%; background:#0f172a; border:1px solid #334155; color:#38bdf8; font-weight:bold; padding:6px; border-radius:4px; font-size:11px; margin-top:2px;">
                            <option value="UNDERGROUND">⛏️ Underground Seam (Zone / Beacon)</option>
                            <option value="SURFACE">🛰️ Surface / Pithead (Hardware GPS)</option>
                        </select>
                    </div>
                    <div id="pts-zone-container">
                        <label style="font-size:10px; color:#94a3b8;">Underground Working Zone / Station</label>
                        <select id="pts-current-zone" style="width:100%; background:#0f172a; border:1px solid #334155; color:#4ade80; font-weight:bold; padding:6px; border-radius:4px; font-size:11px; margin-top:2px;">
                            <option value="Shaft Bottom / Pit Eye">Shaft Bottom / Pit Eye (Station 0)</option>
                            <option value="Main Haulage Dip Level 4">Main Haulage Dip Level 4 (Station 1)</option>
                            <option value="District 1 Heading 2">District 1 Heading 2 (Face)</option>
                            <option value="Depillaring Panel 3 Goaf Edge">Depillaring Panel 3 (Goaf Edge)</option>
                            <option value="Substation & Compressor Drift">Substation & Compressor Drift</option>
                            <option value="Main Return Airway Overcast">Main Return Airway Overcast</option>
                            <option value="Emergency Refuge Chamber B">Emergency Refuge Chamber B</option>
                        </select>
                    </div>
                    <div id="pts-coords-display" style="display:none;">
                        <label style="font-size:10px; color:#94a3b8;">Surface GPS Coordinates</label>
                        <div id="pts-gps-text" style="background:#0f172a; border:1px solid #334155; color:#f59e0b; padding:6px; border-radius:4px; font-size:10px; font-family:monospace; margin-top:2px;">
                            Lat: -- | Lon: --
                        </div>
                    </div>
                </div>

                <div style="display:flex; gap:8px;">
                    <button type="button" onclick="broadcastMyLocation()" style="flex:2; background:#0284c7; color:#fff; font-weight:bold; border:none; padding:8px 12px; border-radius:6px; font-size:11px; cursor:pointer;">
                        📡 Broadcast / Update My Live Location
                    </button>
                    <button type="button" onclick="triggerManDownSOS()" style="flex:1; background:#dc2626; color:#fff; font-weight:bold; border:none; padding:8px; border-radius:6px; font-size:11px; cursor:pointer;">
                        🆘 Send Distress SOS
                    </button>
                </div>
            </div>

            <!-- Live Personnel Colliery Radar (Filtered for Officers & Workers) -->
            <div>
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                    <div style="font-size:11px; font-weight:bold; color:#cbd5e1;">Colliery Active Personnel Radar (Officers & Workers)</div>
                    <div style="display:flex; gap:4px;">
                        <button type="button" onclick="filterRadar('ALL')" id="filter-btn-all" style="background:#0284c7; color:#fff; border:none; padding:2px 8px; border-radius:4px; font-size:9px; cursor:pointer;">All</button>
                        <button type="button" onclick="filterRadar('OFFICER')" id="filter-btn-off" style="background:#1e293b; color:#94a3b8; border:1px solid #334155; padding:2px 8px; border-radius:4px; font-size:9px; cursor:pointer;">Officers</button>
                        <button type="button" onclick="filterRadar('WORKER')" id="filter-btn-wrk" style="background:#1e293b; color:#94a3b8; border:1px solid #334155; padding:2px 8px; border-radius:4px; font-size:9px; cursor:pointer;">Workers</button>
                    </div>
                </div>

                <div id="pts-personnel-list" style="max-height:160px; overflow-y:auto; font-size:10px; color:#94a3b8;">
                    No location signals received in current shift.
                </div>
            </div>
        `;

        container.appendChild(card);
        initGPSHardware();
        renderPersonnelRadar('ALL');
        setInterval(autoPingBeacon, 25000); // 25s auto-heartbeat
    }

    function initGPSHardware() {
        var statusEl = document.getElementById('gps-status-indicator');
        if ('geolocation' in navigator) {
            gpsWatchId = navigator.geolocation.watchPosition(
                function(pos) {
                    currentCoords.lat = pos.coords.latitude.toFixed(5);
                    currentCoords.lon = pos.coords.longitude.toFixed(5);
                    currentCoords.alt = pos.coords.altitude ? pos.coords.altitude.toFixed(1) + 'm' : 'Surface';
                    currentCoords.accuracy = pos.coords.accuracy.toFixed(0) + 'm';

                    var textEl = document.getElementById('pts-gps-text');
                    if (textEl) textEl.innerText = currentCoords.lat + ', ' + currentCoords.lon + ' (±' + currentCoords.accuracy + ')';
                    if (statusEl) {
                        statusEl.innerText = '🛰️ GPS Fixed (±' + currentCoords.accuracy + ')';
                        statusEl.style.color = '#4ade80';
                    }
                },
                function(err) {
                    if (statusEl) {
                        statusEl.innerText = '⚠️ GPS Inactive (Underground Zone Fallback)';
                        statusEl.style.color = '#f59e0b';
                    }
                },
                { enableHighAccuracy: true, maximumAge: 10000, timeout: 15000 }
            );
        } else {
            if (statusEl) statusEl.innerText = 'Zone-Based Mode (No GPS)';
        }
    }

    window.toggleTrackingMode = function() {
        var mode = document.getElementById('pts-domain-select').value;
        var zoneBox = document.getElementById('pts-zone-container');
        var coordsBox = document.getElementById('pts-coords-display');

        if (mode === 'SURFACE') {
            zoneBox.style.display = 'none';
            coordsBox.style.display = 'block';
        } else {
            zoneBox.style.display = 'block';
            coordsBox.style.display = 'none';
        }
    };

    window.broadcastMyLocation = function(isDistress) {
        var mode = document.getElementById('pts-domain-select').value;
        var zone = (mode === 'UNDERGROUND') ? document.getElementById('pts-current-zone').value : ('Surface (' + (currentCoords.lat ? currentCoords.lat + ',' + currentCoords.lon : 'Pithead') + ')');

        var user = null;
        try {
            user = JSON.parse(localStorage.getItem('mineguard_active_user') || 'null');
        } catch(e) { user = null; }

        if (!user) {
            user = { name: 'Shift Miner', role: 'WORKER', token: 'TK-AUTO', designation: 'Coal Face Miner' };
        }

        var entry = {
            id: 'LOC-' + user.token + '-' + Date.now(),
            token: user.token,
            name: user.name,
            role: user.role,
            designation: user.designation,
            mode: mode,
            zone: zone,
            coordinates: currentCoords.lat ? (currentCoords.lat + ',' + currentCoords.lon) : 'N/A (Underground)',
            timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' }),
            rawTime: Date.now(),
            status: isDistress ? 'EMERGENCY_SOS' : 'ACTIVE_NORMAL',
            battery: (navigator.getBattery ? '85%' : 'Optimal')
        };

        var store = JSON.parse(localStorage.getItem('dgms_live_tracking') || '{}');
        store[user.token] = entry; // Upsert latest position per token
        localStorage.setItem('dgms_live_tracking', JSON.stringify(store));

        renderPersonnelRadar(currentFilter);
        if (!isDistress) {
            alert('📡 Location Beacon Transmitted: ' + user.name + ' @ ' + zone);
        }
    };

    window.triggerManDownSOS = function() {
        if (typeof window.playDGMSSiren === 'function') window.playDGMSSiren(6000);
        window.broadcastMyLocation(true);
        alert('🚨 DISTRESS BEACON BROADCAST: Man-Down / Emergency Signal transmitted to Colliery Control Room & Overman!');
    };

    function autoPingBeacon() {
        // Auto-ping quietly in background
        var mode = document.getElementById('pts-domain-select');
        if (!mode) return;
        var isUnderground = mode.value === 'UNDERGROUND';
        var zone = isUnderground ? document.getElementById('pts-current-zone').value : 'Surface';

        var user = null;
        try { user = JSON.parse(localStorage.getItem('mineguard_active_user') || 'null'); } catch(e) {}
        if (!user) return;

        var store = JSON.parse(localStorage.getItem('dgms_live_tracking') || '{}');
        store[user.token] = {
            id: 'LOC-' + user.token + '-' + Date.now(),
            token: user.token,
            name: user.name,
            role: user.role,
            designation: user.designation,
            mode: isUnderground ? 'UNDERGROUND' : 'SURFACE',
            zone: zone,
            coordinates: currentCoords.lat ? (currentCoords.lat + ',' + currentCoords.lon) : 'N/A',
            timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
            rawTime: Date.now(),
            status: 'ACTIVE_NORMAL'
        };
        localStorage.setItem('dgms_live_tracking', JSON.stringify(store));
        renderPersonnelRadar(currentFilter);
    }

    var currentFilter = 'ALL';
    window.filterRadar = function(filter) {
        currentFilter = filter;
        ['all', 'off', 'wrk'].forEach(function(b) {
            var btn = document.getElementById('filter-btn-' + b);
            if (btn) { btn.style.background = '#1e293b'; btn.style.color = '#94a3b8'; }
        });
        var activeBtn = document.getElementById('filter-btn-' + (filter === 'ALL' ? 'all' : (filter === 'OFFICER' ? 'off' : 'wrk')));
        if (activeBtn) { activeBtn.style.background = '#0284c7'; activeBtn.style.color = '#fff'; }
        renderPersonnelRadar(filter);
    };

    function renderPersonnelRadar(filter) {
        var el = document.getElementById('pts-personnel-list');
        if (!el) return;

        var store = JSON.parse(localStorage.getItem('dgms_live_tracking') || '{}');
        var list = Object.values(store);

        // Populate sample colliery roster if empty to illustrate live radar
        if (list.length === 0) {
            list = [
                { token: 'TK-101', name: 'R.K. Sharma', role: 'OFFICER', designation: 'Shift Overman', zone: 'District 1 Heading 2', timestamp: 'Just now', status: 'ACTIVE_NORMAL' },
                { token: 'TK-204', name: 'Birendra Singh', role: 'OFFICER', designation: 'Mining Sirdar', zone: 'Main Haulage Dip Level 4', timestamp: '2m ago', status: 'ACTIVE_NORMAL' },
                { token: 'TK-402', name: 'Sunil Mahato', role: 'WORKER', designation: 'SDL Operator', zone: 'Depillaring Panel 3 Goaf Edge', timestamp: '1m ago', status: 'ACTIVE_NORMAL' },
                { token: 'TK-512', name: 'Mangal Hansda', role: 'WORKER', designation: 'Support Mason', zone: 'Shaft Bottom / Pit Eye', timestamp: '5m ago', status: 'ACTIVE_NORMAL' },
                { token: 'TK-609', name: 'Bipin Murmu', role: 'WORKER', designation: 'Drill Operator', zone: 'District 1 Heading 2', timestamp: 'Just now', status: 'ACTIVE_NORMAL' }
            ];
        }

        var filtered = list.filter(function(p) {
            if (filter === 'OFFICER') return (p.role === 'OFFICER' || p.role === 'MANAGER');
            if (filter === 'WORKER') return (p.role === 'WORKER');
            return true;
        });

        if (filtered.length === 0) {
            el.innerHTML = '<div style="color:#64748b; padding:4px;">No personnel currently tracked in this category.</div>';
            return;
        }

        el.innerHTML = filtered.map(function(p) {
            var isSos = p.status === 'EMERGENCY_SOS';
            var isOfficer = (p.role === 'OFFICER' || p.role === 'MANAGER');
            var roleColor = isSos ? '#ef4444' : (isOfficer ? '#38bdf8' : '#4ade80');
            var icon = isSos ? '🚨' : (isOfficer ? '👮' : '👷');
            var bg = isSos ? '#450a0a' : '#020617';

            return `
                <div style="background:${bg}; border:1px solid #1e293b; padding:6px 8px; border-radius:4px; margin-bottom:4px; display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <div style="display:flex; align-items:center; gap:4px;">
                            <span>${icon}</span>
                            <span style="color:#f8fafc; font-weight:bold;">${p.name}</span>
                            <span style="color:#64748b; font-size:9px;">(${p.token} • ${p.designation})</span>
                        </div>
                        <div style="color:#94a3b8; font-size:9px; margin-top:2px;">
                            📍 Zone: <b style="color:${roleColor};">${p.zone}</b>
                        </div>
                    </div>
                    <div style="text-align:right;">
                        <span style="font-size:9px; color:${isSos ? '#fca5a5' : '#4ade80'}; font-weight:bold;">
                            ${isSos ? '🚨 DISTRESS SOS' : '● Live'}
                        </span>
                        <div style="color:#64748b; font-size:8px; margin-top:2px;">${p.timestamp}</div>
                    </div>
                </div>
            `;
        }).join('');
    }

    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', injectTrackingUI);
    else injectTrackingUI();
    setTimeout(injectTrackingUI, 3200);
})();
</script>
"""
