# mg_siren_network.py - Real-Time Cross-Phone WebSocket Relay & Evac HUD (< 190 Lines)

SIREN_NETWORK_MODULE = """
<div id="mg-evac-hud" style="display:none; position:fixed; top:0; left:0; width:100vw; height:100vh; background:rgba(185,28,28,0.98); z-index:99999999; flex-direction:column; justify-content:center; align-items:center; text-align:center; padding:16px; box-sizing:border-box; font-family:system-ui, sans-serif; color:#ffffff;">
    <style>
        @keyframes pulseStrobe { 0% { background: rgba(185,28,28,0.98); } 100% { background: rgba(127,29,29,1); } }
        @keyframes alertBounce { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.2); } }
        #mg-evac-hud { animation: pulseStrobe 0.8s infinite alternate; }
        .evac-icon { font-size: 64px; animation: alertBounce 0.7s infinite ease-in-out; }
    </style>
    <div class="evac-icon">🚨</div>
    <div style="font-size:22px; font-weight:900; letter-spacing:1px; margin-top:8px;">EMERGENCY EVACUATION ALARM</div>
    <div style="font-size:13px; font-weight:bold; color:#fef08a; margin-top:4px;">खदान खाली करने का आपातकालीन आदेश (CMR 240)</div>

    <div style="background:#020617; border:2px solid #ef4444; border-radius:10px; padding:12px; margin:14px 0; max-width:380px; width:100%; text-align:left;">
        <div style="font-size:10px; color:#94a3b8;">Triggered By / Official:</div>
        <div id="evac-source-text" style="font-size:13px; font-weight:bold; color:#38bdf8; margin-bottom:6px;">Underground Safety SOS</div>
        <div style="font-size:10px; color:#94a3b8;">Hazard Reason:</div>
        <div id="evac-reason-text" style="font-size:12px; font-weight:bold; color:#f87171; margin-bottom:6px;">Immediate Evacuation Order</div>
        <div style="font-size:10px; color:#94a3b8;">Time & Verification Seal:</div>
        <div id="evac-time-seal" style="font-size:11px; color:#cbd5e1; font-family:monospace;">--:--:--</div>
    </div>

    <div style="font-size:11px; color:#fef08a; font-weight:bold; max-width:380px; margin-bottom:16px;">
        ⚠️ सभी कर्मचारी तुरंत अपना SCSR पहनें और Intake Escape Roadway की ओर बढ़ें!
    </div>

    <button type="button" onclick="dismissEvacuationAlert()" style="background:#ffffff; color:#991b1b; font-weight:900; border:none; padding:12px 28px; border-radius:30px; font-size:12px; cursor:pointer;">
        ✓ ACKNOWLEDGE & MUTE SIREN
    </button>
</div>

<script>
(function() {
    var WS_URL = "wss://broker.hivemq.com:8884/mqtt";
    var TOPIC = "mineguard/colliery/siren/broadcast/v1";
    var lastAlertId = null;
    var ws = null;

    function encodeStr(s) {
        var b = [];
        for (var i = 0; i < s.length; i++) {
            var c = s.charCodeAt(i);
            if (c < 128) b.push(c);
            else if (c < 2048) { b.push(192 | (c >> 6)); b.push(128 | (c & 63)); }
            else { b.push(224 | (c >> 12)); b.push(128 | ((c >> 6) & 63)); b.push(128 | (c & 63)); }
        }
        return b;
    }

    function initWebSocketRelay() {
        try {
            ws = new WebSocket(WS_URL, ["mqtt"]);
            ws.binaryType = "arraybuffer";
        } catch(e) {
            setTimeout(initWebSocketRelay, 3000);
            return;
        }

        ws.onopen = function() {
            var proto = encodeStr("MQTT");
            var clientId = encodeStr("mg_" + Math.random().toString(36).substring(2, 9));
            var vh = [0x00, 0x04].concat(proto).concat([0x04, 0x02, 0x00, 0x3c]);
            var pl = [0x00, clientId.length].concat(clientId);
            var pkt = [0x10, vh.length + pl.length].concat(vh).concat(pl);
            ws.send(new Uint8Array(pkt));
        };

        ws.onmessage = function(evt) {
            var buf = new Uint8Array(evt.data);
            var type = buf[0] >> 4;

            if (type === 2) { // Connected -> Subscribe
                var top = encodeStr(TOPIC);
                var vh = [0x00, 0x01];
                var pl = [0x00, top.length].concat(top).concat([0x00]);
                var pkt = [0x82, vh.length + pl.length].concat(vh).concat(pl);
                ws.send(new Uint8Array(pkt));
            } else if (type === 3) { // Incoming Siren Alert
                var i = 1;
                while (i < buf.length && (buf[i++] & 128) !== 0);
                var tLen = (buf[i] << 8) | buf[i+1];
                i += 2 + tLen;
                var raw = "";
                for (; i < buf.length; i++) raw += String.fromCharCode(buf[i]);
                try {
                    var data = JSON.parse(raw);
                    handleIncomingSiren(data);
                } catch(err) {}
            }
        };

        ws.onclose = function() { setTimeout(initWebSocketRelay, 2500); };
        ws.onerror = function() { try { ws.close(); } catch(e){} };

        // Keepalive Ping every 25 seconds
        setInterval(function() {
            if (ws && ws.readyState === WebSocket.OPEN) ws.send(new Uint8Array([0xc0, 0x00]));
        }, 25000);
    }

    window.broadcastCollierySOS = function(reason) {
        var user = null;
        try { user = JSON.parse(localStorage.getItem('mineguard_active_user') || 'null'); } catch(e){}
        var officer = user ? (user.name + ' (' + user.token + ')') : 'Underground Personnel (SOS)';
        var payload = {
            id: 'SOS-' + Date.now() + '-' + Math.random().toString(36).substring(2, 6).toUpperCase(),
            officer: officer,
            reason: reason || 'Emergency Colliery Evacuation Required',
            time: new Date().toLocaleTimeString(),
            timestamp: Date.now()
        };

        if (ws && ws.readyState === WebSocket.OPEN) {
            var top = encodeStr(TOPIC);
            var pay = encodeStr(JSON.stringify(payload));
            var pkt = [0x30, (2 + top.length) + pay.length, 0x00, top.length].concat(top).concat(pay);
            ws.send(new Uint8Array(pkt));
        }

        handleIncomingSiren(payload);
    };

    function handleIncomingSiren(payload) {
        if (!payload || !payload.id || payload.id === lastAlertId) return;
        if (Date.now() - payload.timestamp > 45000) return;
        lastAlertId = payload.id;

        var hud = document.getElementById('mg-evac-hud');
        if (hud) {
            document.getElementById('evac-source-text').innerText = payload.officer || 'Mine Safety Official';
            document.getElementById('evac-reason-text').innerText = payload.reason || 'Immediate Evacuation';
            document.getElementById('evac-time-seal').innerText = payload.time + ' • ' + payload.id;
            hud.style.display = 'flex';
        }

        if (typeof window.playDGMSSirenAudio === 'function') window.playDGMSSirenAudio(15000);
        if (typeof window.speakSirenVoice === 'function') window.speakSirenVoice();
    }

    window.dismissEvacuationAlert = function() {
        var hud = document.getElementById('mg-evac-hud');
        if (hud) hud.style.display = 'none';
        if (typeof window.stopDGMSSirenAudio === 'function') window.stopDGMSSirenAudio();
        if ('speechSynthesis' in window) window.speechSynthesis.cancel();
    };

    initWebSocketRelay();
})();
</script>
"""
