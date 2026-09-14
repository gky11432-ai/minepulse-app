# ui_siren_network.py - Standalone DGMS Colliery-Wide P2P Siren & Evacuation Alarm Relay Network

SIREN_NETWORK_MODULE = """
<script>
(function() {
    var SIREN_EVENT_KEY = 'dgms_active_siren_broadcast';
    var lastHandledSirenId = null;

    function injectEmergencyHUD() {
        if (document.getElementById('mineguard-evac-hud')) return;

        var hud = document.createElement('div');
        hud.id = 'mineguard-evac-hud';
        hud.style.cssText = 'display:none; position:fixed; top:0; left:0; width:100vw; height:100vh; background:rgba(185,28,28,0.98); z-index:99999999; flex-direction:column; justify-content:center; align-items:center; text-align:center; padding:16px; box-sizing:border-box; font-family:system-ui, sans-serif; color:#ffffff; animation:strobeRed 0.8s infinite alternate;';

        hud.innerHTML = `
            <style>
                @keyframes strobeRed {
                    0% { background: rgba(185, 28, 28, 0.98); }
                    100% { background: rgba(127, 29, 29, 1); }
                }
                @keyframes iconBounce {
                    0%, 100% { transform: scale(1); }
                    50% { transform: scale(1.25); }
                }
            </style>
            <div style="font-size:64px; animation:iconBounce 0.7s infinite ease-in-out;">🚨</div>
            <div style="font-size:24px; font-weight:900; letter-spacing:1px; margin-top:8px; text-shadow:0 2px 8px rgba(0,0,0,0.8);">
                EMERGENCY EVACUATION ALARM
            </div>
            <div style="font-size:14px; font-weight:bold; color:#fef08a; margin-top:4px;">
                खदान खाली करने का आपातकालीन आदेश (CMR 2017 REG 240)
            </div>

            <div style="background:#020617; border:2px solid #ef4444; border-radius:10px; padding:12px; margin:16px 0; max-width:400px; width:100%; box-shadow:0 10px 25px rgba(0,0,0,0.8); text-align:left;">
                <div style="font-size:10px; color:#94a3b8;">Triggered By / Source:</div>
                <div id="evac-officer-name" style="font-size:13px; font-weight:bold; color:#38bdf8; margin-bottom:6px;">Underground Safety SOS</div>

                <div style="font-size:10px; color:#94a3b8;">Hazard Reason:</div>
                <div id="evac-reason-text" style="font-size:12px; font-weight:bold; color:#f87171; margin-bottom:6px;">Emergency Evacuation Order</div>

                <div style="font-size:10px; color:#94a3b8;">Time & Verification Seal:</div>
                <div id="evac-time-text" style="font-size:11px; color:#cbd5e1; font-family:monospace;">--:--:--</div>
            </div>

            <div style="font-size:12px; color:#fef08a; font-weight:bold; line-height:1.4; max-width:400px; margin-bottom:18px;">
                ⚠️ सभी कर्मचारी तुरंत अपना SCSR (Self-Rescuer) पहनें और मार्क किए गए Intake Escape Roadway की ओर बढ़ें!
            </div>

            <button type="button" onclick="acknowledgeEvacuationAlert()" style="background:#ffffff; color:#991b1b; font-weight:900; border:none; padding:12px 28px; border-radius:30px; font-size:13px; cursor:pointer; box-shadow:0 4px 15px rgba(0,0,0,0.5);">
                ✓ ACKNOWLEDGE & MUTE SIREN
            </button>
        `;

        document.body.appendChild(hud);
    }

    // Broadcasts across the Mesh Network to ALL phones
    window.triggerCollieryEvacuationSiren = function(reason) {
        var user = null;
        try {
            user = JSON.parse(localStorage.getItem('mineguard_active_user') || 'null');
        } catch(e) { user = null; }

        var initiator = user ? (user.name + ' (' + user.role + ' - ' + user.token + ')') : 'Underground Personnel (SOS)';
        reason = reason || 'Immediate Pit Evacuation Required (CMR 240)';
        var eventId = 'SIREN-' + Date.now() + '-' + Math.random().toString(36).substring(2, 6).toUpperCase();

        var alertPayload = {
            id: eventId,
            officer: initiator,
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
                role: 'EMERGENCY',
                designation: initiator,
                zone: 'ALL DISTRICTS',
                status: 'EMERGENCY_SOS',
                rawTime: Date.now(),
                timestamp: alertPayload.time,
                payload: alertPayload
            };
            localStorage.setItem('dgms_p2p_mesh_roster', JSON.stringify(meshStore));
        } catch(e) {}

        // 3. Execute immediately on this phone
        executeSirenOnThisDevice(alertPayload);
    };

    function executeSirenOnThisDevice(payload) {
        injectEmergencyHUD();
        var hud = document.getElementById('mineguard-evac-hud');
        if (hud) {
            document.getElementById('evac-officer-name').innerText = payload.officer || 'Mine Safety Personnel';
            document.getElementById('evac-reason-text').innerText = payload.reason || 'Immediate Evacuation Order';
            document.getElementById('evac-time-text').innerText = payload.time + ' • ' + payload.id;
            hud.style.display = 'flex';
        }

        // 1. Hardware 800-1200Hz Audio Siren
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

    function pollIncomingSirenNetwork() {
        try {
            var raw = localStorage.getItem(SIREN_EVENT_KEY);
            if (!raw) {
                var mesh = JSON.parse(localStorage.getItem('dgms_p2p_mesh_roster') || '{}');
                if (mesh['EMERGENCY_ALARM'] && mesh['EMERGENCY_ALARM'].payload) {
                    raw = JSON.stringify(mesh['EMERGENCY_ALARM'].payload);
                }
            }

            if (raw) {
                var payload = JSON.parse(raw);
                var now = Date.now();
                if (payload.timestamp && (now - payload.timestamp) < 60000) {
                    if (payload.id !== lastHandledSirenId) {
                        lastHandledSirenId = payload.id;
                        executeSirenOnThisDevice(payload);
                    }
                }
            }
        } catch(e) {}
    }

    window.triggerAlarm = function() {
        window.triggerCollieryEvacuationSiren('General Colliery Hazard Detected');
    };

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
