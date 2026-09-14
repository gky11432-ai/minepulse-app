# ui_siren_network.py - Standalone DGMS Colliery-Wide P2P Siren & Evacuation Alarm Relay Network

SIREN_NETWORK_MODULE = """
<script>
(function() {
    var SIREN_EVENT_KEY = 'dgms_active_siren_broadcast';
    var lastHandledSirenId = null;

    // Full-Screen Red Emergency Alert Modal (Appears on ALL phones when alarm sounds)
    function injectEmergencyHUD() {
        if (document.getElementById('mineguard-evac-hud')) return;

        var hud = document.createElement('div');
        hud.id = 'mineguard-evac-hud';
        hud.style.cssText = 'display:none; position:fixed; top:0; left:0; width:100vw; height:100vh; background:rgba(185,28,28,0.96); z-index:9999999; flex-direction:column; justify-content:center; align-items:center; text-align:center; padding:20px; box-sizing:border-box; font-family:system-ui, sans-serif; color:#ffffff; animation:strobeRed 1s infinite alternate;';

        hud.innerHTML = `
            <style>
                @keyframes strobeRed {
                    0% { background: rgba(185, 28, 28, 0.96); }
                    100% { background: rgba(127, 29, 29, 0.98); }
                }
                @keyframes iconBounce {
                    0%, 100% { transform: scale(1); }
                    50% { transform: scale(1.2); }
                }
            </style>
            <div style="font-size:64px; animation:iconBounce 0.8s infinite ease-in-out;">🚨</div>
            <div style="font-size:24px; font-weight:900; letter-spacing:1px; margin-top:8px; text-shadow:0 2px 8px rgba(0,0,0,0.8);">
                EMERGENCY EVACUATION ALARM
            </div>
            <div style="font-size:14px; font-weight:bold; color:#fef08a; margin-top:6px;">
                खदान खाली करने का आपातकालीन आदेश (CMR 2017 REG 240)
            </div>

            <div style="background:#020617; border:2px solid #ef4444; border-radius:10px; padding:14px; margin:20px 0; max-width:420px; width:100%; box-shadow:0 10px 25px rgba(0,0,0,0.8); text-align:left;">
                <div style="font-size:11px; color:#94a3b8;">Triggered By Officer:</div>
                <div id="evac-officer-name" style="font-size:14px; font-weight:bold; color:#38bdf8; margin-bottom:6px;">Officer In-Charge</div>

                <div style="font-size:11px; color:#94a3b8;">Reason / Hazard:</div>
                <div id="evac-reason-text" style="font-size:12px; font-weight:bold; color:#f87171; margin-bottom:6px;">Immediate Pit Evacuation Order</div>

                <div style="font-size:11px; color:#94a3b8;">Timestamp / Seal:</div>
                <div id="evac-time-text" style="font-size:11px; color:#cbd5e1; font-family:monospace;">--:--:--</div>
            </div>

            <div style="font-size:13px; color:#fef08a; font-weight:bold; line-height:1.5; max-width:420px; margin-bottom:20px;">
                ⚠️ सभी कर्मचारी तुरंत अपना SCSR (Self-Rescuer) पहनें और मार्क किए गए Intake Escape Roadway की ओर बढ़ें!
            </div>

            <button type="button" onclick="acknowledgeEvacuationAlert()" style="background:#ffffff; color:#991b1b; font-weight:900; border:none; padding:14px 28px; border-radius:30px; font-size:14px; cursor:pointer; box-shadow:0 4px 15px rgba(0,0,0,0.5);">
                ✓ ACKNOWLEDGE & MUTE SIREN
            </button>
        `;

        document.body.appendChild(hud);
    }

    // Officer Triggers Siren -> Broadcasts across the Mesh Network to ALL phones
    window.triggerCollieryEvacuationSiren = function(reason) {
        var user = null;
        try {
            user = JSON.parse(localStorage.getItem('mineguard_active_user') || 'null');
        } catch(e) { user = null; }

        if (!user || (user.role !== 'OFFICER' && user.role !== 'MANAGER')) {
            alert('⛔ STATUTORY VIOLATION: Only certified Mining Sirdars, Overmen, or Managers are legally permitted to sound the Mine Evacuation Siren (CMR 240).');
            return;
        }

        reason = reason || 'Immediate Evacuation Required (CMR 240)';
        var eventId = 'SIREN-' + Date.now() + '-' + Math.random().toString(36).substring(2, 6).toUpperCase();

        var alertPayload = {
            id: eventId,
            officer: user.name + ' (' + user.role + ' - ' + user.token + ')',
            reason: reason,
            time: new Date().toLocaleTimeString(),
            timestamp: Date.now()
        };

        // 1. Save to local broadcast registry
        localStorage.setItem(SIREN_EVENT_KEY, JSON.stringify(alertPayload));

        // 2. Relay via Store-and-Forward Mesh Vault (carried to all phones)
        try {
            var meshStore = JSON.parse(localStorage.getItem('dgms_p2p_mesh_roster') || '{}');
            meshStore['EMERGENCY_ALARM'] = {
                token: 'ALARM-P2P',
                name: '🚨 EVACUATION SIREN',
                role: 'OFFICER',
                designation: user.name,
                zone: 'ALL DISTRICTS / HORIZONS',
                status: 'EMERGENCY_SOS',
                rawTime: Date.now(),
                timestamp: alertPayload.time,
                payload: alertPayload
            };
            localStorage.setItem('dgms_p2p_mesh_roster', JSON.stringify(meshStore));
        } catch(e) {}

        // 3. Execute immediately on Officer's phone
        executeSirenOnThisDevice(alertPayload);
        alert('📢 COLLIERY-WIDE SIREN BROADCASTED! Propagating across all worker & officer devices via P2P Mesh.');
    };

    // Siren Execution on Any Device (Worker or Officer)
    function executeSirenOnThisDevice(payload) {
        injectEmergencyHUD();
        var hud = document.getElementById('mineguard-evac-hud');
        if (hud) {
            document.getElementById('evac-officer-name').innerText = payload.officer || 'Mine Safety Officer';
            document.getElementById('evac-reason-text').innerText = payload.reason || 'Immediate Evacuation Order';
            document.getElementById('evac-time-text').innerText = payload.time + ' • ' + payload.id;
            hud.style.display = 'flex';
        }

        // 1. Sound 800Hz - 1200Hz Hardware Audio Siren
        if (typeof window.playDGMSSiren === 'function') {
            window.playDGMSSiren(15000);
        }

        // 2. Hardware Vibration
        if (navigator.vibrate) {
            navigator.vibrate([1000, 300, 1000, 300, 1500, 400, 2000]);
        }

        // 3. Offline Hindi Speech Synthesis Announcement
        if ('speechSynthesis' in window) {
            try {
                window.speechSynthesis.cancel();
                var msg = new SpeechSynthesisUtterance("सावधान! आपातकालीन सायरन बजाया गया है। सभी खदान कर्मचारी तुरंत सुरक्षित निकासी मार्ग की ओर बढ़ें।");
                msg.lang = 'hi-IN';
                msg.rate = 0.9;
                window.speechSynthesis.speak(msg);
            } catch(e) {}
        }
    }

    window.acknowledgeEvacuationAlert = function() {
        var hud = document.getElementById('mineguard-evac-hud');
        if (hud) hud.style.display = 'none';

        if (typeof window.stopDGMSSiren === 'function') {
            window.stopDGMSSiren();
        }
        if (navigator.vibrate) navigator.vibrate(0);
        if ('speechSynthesis' in window) window.speechSynthesis.cancel();
    };

    // Background Daemon: Continuously polls local mesh / storage for incoming siren broadcast
    function pollIncomingSirenNetwork() {
        try {
            var raw = localStorage.getItem(SIREN_EVENT_KEY);
            if (!raw) {
                // Also check if carried via P2P mesh
                var mesh = JSON.parse(localStorage.getItem('dgms_p2p_mesh_roster') || '{}');
                if (mesh['EMERGENCY_ALARM'] && mesh['EMERGENCY_ALARM'].payload) {
                    raw = JSON.stringify(mesh['EMERGENCY_ALARM'].payload);
                }
            }

            if (raw) {
                var payload = JSON.parse(raw);
                var now = Date.now();
                // If siren event was broadcasted within last 60 seconds and not handled yet
                if (payload.timestamp && (now - payload.timestamp) < 60000) {
                    if (payload.id !== lastHandledSirenId) {
                        lastHandledSirenId = payload.id;
                        executeSirenOnThisDevice(payload);
                    }
                }
            }
        } catch(e) {}
    }

    // Intercept default triggerAlarm calls
    window.triggerAlarm = function() {
        window.triggerCollieryEvacuationSiren('General Emergency Hazard Triggered');
    };

    // Storage event for instantaneous cross-tab/process synchronization
    window.addEventListener('storage', function(e) {
        if (e.key === SIREN_EVENT_KEY && e.newValue) {
            try {
                var p = JSON.parse(e.newValue);
                if (p.id !== lastHandledSirenId) {
                    lastHandledSirenId = p.id;
                    executeSirenOnThisDevice(p);
                }
            } catch(err) {}
        }
    });

    setInterval(pollIncomingSirenNetwork, 1200);

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', injectEmergencyHUD);
    } else {
        injectEmergencyHUD();
    }
})();
</script>
"""
