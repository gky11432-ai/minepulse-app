# ui_siren_network.py - True Cross-Phone Real-Time P2P WebSocket & MQTT Siren Relay

SIREN_NETWORK_MODULE = """
<style>
  #siren-mesh-status-indicator {
      position: fixed;
      bottom: 8px;
      right: 10px;
      z-index: 99998;
      font-size: 9px;
      font-weight: 800;
      font-family: system-ui, sans-serif;
      padding: 3px 8px;
      border-radius: 12px;
      background: #020617;
      border: 1px solid #334155;
      color: #94a3b8;
      display: flex;
      align-items: center;
      gap: 5px;
  }
</style>

<div id="siren-mesh-status-indicator">
    <span id="mesh-status-dot" style="color:#fbbf24;">🟠</span>
    <span id="mesh-status-text">Mesh Connecting...</span>
</div>

<script>
(function() {
    var SIREN_TOPIC = "mineguard/colliery/siren/broadcast/v1";
    var BROKER_WS_URL = "wss://broker.hivemq.com:8884/mqtt";
    var lastHandledSirenId = null;
    var mqttClient = null;

    // 1. Pure Vanilla JS Micro-MQTT WebSocket Client (Zero external libraries needed)
    function createMicroMQTT(brokerUrl, topic, onMessageCallback) {
        var ws = null;
        var isConnected = false;
        var clientId = 'mg_' + Math.random().toString(36).substring(2, 9);

        function encodeUTF8(str) {
            var bytes = [];
            for (var i = 0; i < str.length; i++) {
                var c = str.charCodeAt(i);
                if (c < 128) bytes.push(c);
                else if (c < 2048) { bytes.push(192 | (c >> 6)); bytes.push(128 | (c & 63)); }
                else { bytes.push(224 | (c >> 12)); bytes.push(128 | ((c >> 6) & 63)); bytes.push(128 | (c & 63)); }
            }
            return bytes;
        }

        function decodeUTF8(bytes) {
            var str = '';
            var i = 0;
            while (i < bytes.length) {
                var c = bytes[i++];
                if (c < 128) str += String.fromCharCode(c);
                else if (c > 191 && c < 224) { str += String.fromCharCode(((c & 31) << 6) | (bytes[i++] & 63)); }
                else { str += String.fromCharCode(((c & 15) << 12) | ((bytes[i++] & 63) << 6) | (bytes[i++] & 63)); }
            }
            return str;
        }

        function updateMeshUI(connected) {
            var dot = document.getElementById('mesh-status-dot');
            var txt = document.getElementById('mesh-status-text');
            if (!dot || !txt) return;

            if (connected) {
                dot.style.color = '#34d399';
                dot.innerText = '🟢';
                txt.innerText = 'Siren Mesh: Live';
                txt.style.color = '#34d399';
            } else {
                dot.style.color = '#fbbf24';
                dot.innerText = '🟠';
                txt.innerText = 'Mesh Connecting...';
                txt.style.color = '#94a3b8';
            }
        }

        function connect() {
            try {
                ws = new WebSocket(brokerUrl, ["mqtt"]);
                ws.binaryType = "arraybuffer";
            } catch(e) {
                setTimeout(connect, 3500);
                return;
            }

            ws.onopen = function() {
                var proto = encodeUTF8("MQTT");
                var cId = encodeUTF8(clientId);
                var varHeader = [0x00, 0x04].concat(proto).concat([0x04, 0x02, 0x00, 0x3c]);
                var payload = [0x00, cId.length].concat(cId);
                var remLen = varHeader.length + payload.length;
                var pkt = [0x10, remLen].concat(varHeader).concat(payload);
                ws.send(new Uint8Array(pkt));
            };

            ws.onmessage = function(evt) {
                var buf = new Uint8Array(evt.data);
                var msgType = buf[0] >> 4;

                if (msgType === 2) { // CONNACK
                    isConnected = true;
                    updateMeshUI(true);

                    // Subscribe to Emergency Siren Channel
                    var top = encodeUTF8(topic);
                    var varHeader = [0x00, 0x01];
                    var payload = [0x00, top.length].concat(top).concat([0x00]);
                    var remLen = varHeader.length + payload.length;
                    var pkt = [0x82, remLen].concat(varHeader).concat(payload);
                    ws.send(new Uint8Array(pkt));
                } else if (msgType === 3) { // PUBLISH (Incoming Siren from another phone)
                    var i = 1;
                    var remLen = 0;
                    var mul = 1;
                    while (i < buf.length) {
                        var digit = buf[i++];
                        remLen += (digit & 127) * mul;
                        mul *= 128;
                        if ((digit & 128) === 0) break;
                    }
                    var topLen = (buf[i] << 8) | buf[i+1];
                    i += 2 + topLen;

                    var msgBytes = [];
                    for (; i < buf.length; i++) msgBytes.push(buf[i]);
                    var rawText = decodeUTF8(msgBytes);

                    try {
                        var parsed = JSON.parse(rawText);
                        onMessageCallback(parsed);
                    } catch(err) {}
                }
            };

            ws.onclose = function() {
                isConnected = false;
                updateMeshUI(false);
                setTimeout(connect, 3000);
            };

            ws.onerror = function() {
                try { ws.close(); } catch(e) {}
            };
        }

        function publish(dataObj) {
            var text = typeof dataObj === 'string' ? dataObj : JSON.stringify(dataObj);
            var top = encodeUTF8(topic);
            var pay = encodeUTF8(text);
            var remLen = (2 + top.length) + pay.length;
            var pkt = [0x30, remLen, 0x00, top.length].concat(top).concat(pay);

            if (ws && ws.readyState === WebSocket.OPEN && isConnected) {
                ws.send(new Uint8Array(pkt));
            }
        }

        connect();
        return {
            publish: publish,
            isConnected: function() { return isConnected; }
        };
    }

    // 2. Full-Screen Emergency HUD on Ringing Device
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
                <div style="font-size:10px; color:#94a3b8;">Triggered By Phone / Official:</div>
                <div id="evac-officer-name" style="font-size:13px; font-weight:bold; color:#38bdf8; margin-bottom:6px;">Underground Safety SOS</div>

                <div style="font-size:10px; color:#94a3b8;">Hazard Reason:</div>
                <div id="evac-reason-text" style="font-size:12px; font-weight:bold; color:#f87171; margin-bottom:6px;">Emergency Evacuation Order</div>

                <div style="font-size:10px; color:#94a3b8;">Time & Verification Seal:</div>
                <div id="evac-time-text" style="font-size:11px; color:#cbd5e1; font-family:monospace;">--:--:--</div>
            </div>

            <div style="font-size:12px; color:#fef08a; font-weight:bold; line-height:1.4; max-width:400px; margin-bottom:18px;">
                ⚠️ सभी कर्मचारी तुरंत अपना SCSR पहनें और मार्क किए गए Intake Escape Roadway की ओर बढ़ें!
            </div>

            <button type="button" onclick="acknowledgeEvacuationAlert()" style="background:#ffffff; color:#991b1b; font-weight:900; border:none; padding:12px 28px; border-radius:30px; font-size:13px; cursor:pointer; box-shadow:0 4px 15px rgba(0,0,0,0.5);">
                ✓ ACKNOWLEDGE & MUTE SIREN
            </button>
        `;

        document.body.appendChild(hud);
    }

    // 3. Sender Action: Broadcasts to All Other Phones Over Network
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

        // Broadcast to all other phones via WebSocket Relay
        if (mqttClient) {
            mqttClient.publish(alertPayload);
        }

        // Sound on this phone immediately
        executeSirenOnThisDevice(alertPayload);
    };

    // 4. Receiver Action: Sound siren when message arrives from another phone
    function executeSirenOnThisDevice(payload) {
        injectEmergencyHUD();
        var hud = document.getElementById('mineguard-evac-hud');
        if (hud) {
            document.getElementById('evac-officer-name').innerText = payload.officer || 'Mine Safety Personnel';
            document.getElementById('evac-reason-text').innerText = payload.reason || 'Immediate Evacuation Order';
            document.getElementById('evac-time-text').innerText = payload.time + ' • ' + payload.id;
            hud.style.display = 'flex';
        }

        // Sound Hardware Siren
        if (typeof window.playDGMSSiren === 'function') {
            window.playDGMSSiren(15000);
        }

        // Vibrate Phone
        if (navigator.vibrate) {
            navigator.vibrate([1000, 300, 1000, 300, 1500, 400, 2000]);
        }

        // Hindi Voice Evacuation Announcement
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

    // Initialize Network Relay
    function initNetworkRelay() {
        injectEmergencyHUD();

        mqttClient = createMicroMQTT(BROKER_WS_URL, SIREN_TOPIC, function(payload) {
            if (!payload || !payload.id) return;
            var now = Date.now();
            // Trigger siren only if broadcast is fresh (< 45 sec) and not already sounded
            if (payload.timestamp && (now - payload.timestamp) < 45000) {
                if (payload.id !== lastHandledSirenId) {
                    lastHandledSirenId = payload.id;
                    executeSirenOnThisDevice(payload);
                }
            }
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initNetworkRelay);
    } else {
        initNetworkRelay();
    }
})();
</script>
"""
