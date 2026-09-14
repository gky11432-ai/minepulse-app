# ui_voice.py - Standalone DGMS CMR 241 Offline Hindi Voice Evacuation & Siren Broadcast Engine

VOICE_MODULE = """
<script>
(function() {
    function injectVoiceUI() {
        if (document.getElementById('statutory-voice-card')) return;

        var container = document.querySelector('.grid-container') || document.body;

        var card = document.createElement('div');
        card.id = 'statutory-voice-card';
        card.style.cssText = 'background:#0f172a; border:1px solid #334155; border-radius:10px; padding:16px; margin:14px 0; color:#f8fafc; font-family:system-ui, sans-serif; box-shadow:0 4px 6px -1px rgba(0,0,0,0.5);';

        card.innerHTML = `
            <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #1e293b; padding-bottom:10px; margin-bottom:12px;">
                <div style="display:flex; align-items:center; gap:8px;">
                    <span style="font-size:18px;">📢</span>
                    <div>
                        <div style="font-size:13px; font-weight:bold; color:#ef4444;">PIT VOICE EVACUATION & SIREN BROADCAST</div>
                        <div style="font-size:10px; color:#94a3b8;">CMR 2017 Reg 241 & Emergency Action Plan - Offline Hindi Auditory Directives</div>
                    </div>
                </div>
                <div id="voice-broadcast-badge" style="background:#14532d; color:#4ade80; border:1px solid #22c55e; font-size:10px; padding:3px 8px; border-radius:12px; font-weight:bold;">
                    VOICE ENGINE STANDBY
                </div>
            </div>

            <!-- Pre-Configured Statutory Voice Directives -->
            <form id="voice-broadcast-form" onsubmit="executeVoiceBroadcast(event)">
                <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap:10px; margin-bottom:10px;">
                    <div>
                        <label style="font-size:11px; color:#94a3b8;">Statutory Emergency Scenario</label>
                        <select id="voice-scenario-select" onchange="loadPresetVoiceText()" style="width:100%; background:#020617; border:1px solid #334155; color:#38bdf8; font-weight:bold; padding:8px; border-radius:6px; font-size:11px; margin-top:4px;">
                            <option value="ch4_breach">Methane Breach (>1.25% CH4) Evacuation</option>
                            <option value="roof_fall">Imminent Roof Fall / Strata Collapse</option>
                            <option value="inundation">Water Inrush / Sump Inundation Danger</option>
                            <option value="mine_fire">Underground Fire / Graham Ratio Alert</option>
                            <option value="blasting">Blasting Siren & Personnel Clearance</option>
                            <option value="custom">Custom Mining Emergency Announcement</option>
                        </select>
                    </div>
                    <div>
                        <label style="font-size:11px; color:#94a3b8;">Affected Mine District / Zone</label>
                        <input type="text" id="voice-zone" required placeholder="e.g. District 1 / Panel 4 Dip Face" oninput="loadPresetVoiceText()" style="width:100%; background:#020617; border:1px solid #334155; color:#fff; padding:8px; border-radius:6px; font-size:11px; margin-top:4px;">
                    </div>
                    <div>
                        <label style="font-size:11px; color:#94a3b8;">Broadcast Authorization Officer</label>
                        <input type="text" id="voice-officer" required placeholder="Manager / Overman Reg No." style="width:100%; background:#020617; border:1px solid #334155; color:#fff; padding:8px; border-radius:6px; font-size:11px; margin-top:4px;">
                    </div>
                </div>

                <!-- Speech Script in Hindi -->
                <div style="margin-bottom:10px;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
                        <label style="font-size:11px; color:#94a3b8;">Hindi Speech Script (Offline Text-to-Speech)</label>
                        <span id="voice-repeat-label" style="font-size:10px; color:#f59e0b;">Broadcast Repeats: 2 Cycles</span>
                    </div>
                    <textarea id="voice-script-text" rows="3" required style="width:100%; background:#020617; border:1px solid #334155; color:#f8fafc; font-family:sans-serif; padding:8px; border-radius:6px; font-size:12px; resize:vertical; box-sizing:border-box; line-height:1.4;"></textarea>
                </div>

                <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap:8px; margin-bottom:12px;">
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Siren & Tone Mode</span>
                        <select id="voice-siren-mode" style="width:100%; background:transparent; border:none; color:#4ade80; font-weight:bold; font-size:11px; margin-top:2px;">
                            <option value="siren_voice">Siren First, Then Voice</option>
                            <option value="voice_only">Voice Only (No Siren)</option>
                            <option value="siren_continuous">Siren + Voice Loop</option>
                        </select>
                    </div>
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Broadcast Rate & Pitch</span>
                        <select id="voice-speed" style="width:100%; background:transparent; border:none; color:#38bdf8; font-weight:bold; font-size:11px; margin-top:2px;">
                            <option value="0.9">Urgent & Clear (0.9x)</option>
                            <option value="1.0">Standard Speed (1.0x)</option>
                            <option value="0.8">Slow & Loud (0.8x)</option>
                        </select>
                    </div>
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Repetition Cycles</span>
                        <select id="voice-cycles" style="width:100%; background:transparent; border:none; color:#f59e0b; font-weight:bold; font-size:11px; margin-top:2px;">
                            <option value="2">Repeat 2 Times</option>
                            <option value="3">Repeat 3 Times</option>
                            <option value="1">Play Once</option>
                        </select>
                    </div>
                </div>

                <div style="display:flex; gap:8px;">
                    <button type="submit" id="btn-start-broadcast" style="flex:2; background:#dc2626; color:#fff; font-weight:bold; border:none; padding:10px; border-radius:6px; font-size:12px; cursor:pointer;">
                        🚨 Broadcast Emergency Siren & Hindi Voice
                    </button>
                    <button type="button" onclick="stopVoiceBroadcast()" style="flex:1; background:#334155; color:#cbd5e1; font-weight:bold; border:none; padding:10px; border-radius:6px; font-size:12px; cursor:pointer;">
                        ⏹️ Silence / Stop
                    </button>
                </div>
            </form>

            <!-- Voice Broadcast Ledger Archive -->
            <div style="margin-top:14px; border-top:1px solid #1e293b; padding-top:10px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                    <div style="font-size:11px; font-weight:bold; color:#cbd5e1;">Emergency Auditory Dispatch Log</div>
                    <span id="voice-logs-count" style="background:#334155; color:#cbd5e1; font-size:9px; padding:2px 6px; border-radius:8px;">0 Broadcasts</span>
                </div>
                <div id="voice-history-list" style="max-height:120px; overflow-y:auto; font-size:10px; color:#94a3b8;">
                    No emergency voice broadcasts transmitted in current shift.
                </div>
            </div>
        `;

        container.appendChild(card);
        loadPresetVoiceText();
        renderVoiceLogs();
    }

    var speechInstance = null;
    var broadcastActive = false;

    window.loadPresetVoiceText = function() {
        var scenario = document.getElementById('voice-scenario-select').value;
        var zone = document.getElementById('voice-zone').value.trim() || 'डिस्ट्रिक्ट नंबर 1';
        var scriptBox = document.getElementById('voice-script-text');
        if (!scriptBox) return;

        var presets = {
            'ch4_breach': 'सावधान! सभी कामगार ध्यान दें। ' + zone + ' में मिथेन गैस का स्तर सुरक्षित सीमा से अधिक पाया गया है। सभी खनन कार्य तुरंत रोकें, बिजली सप्लाई काटें और इंटेक एयरवे से बाहर निकलें।',
            'roof_fall': 'खतरा! रूफ फॉल अलर्ट। ' + zone + ' में स्ट्रैटा का भारी दबाव दर्ज हुआ है। फेस तुरंत खाली करें और कोई भी व्यक्ति अनसपोर्टेड रूफ के नीचे न जाए।',
            'inundation': 'आपातकालीन सूचना! इनंडेशन का खतरा। ' + zone + ' में पानी का अचानक रिसाव देखा गया है। सभी कामगार तुरंत निचले हिस्से खाली करके मेन शाफ्ट की ओर बढ़ें।',
            'mine_fire': 'फायर अलर्ट! सीलबंद इलाके के पास कार्बन मोनोऑक्साइड और तापमान में वृद्धि हुई है। डिस्ट्रिक्ट इनचार्ज तुरंत वेंटिलेशन डोर्स चेक करें और मेन स्टेशन पर रिपोर्ट करें।',
            'blasting': 'ब्लास्टिंग सायरन! ' + zone + ' में हेडिंग ब्लास्टिंग की जा रही है। सभी रास्तों के डेंजर फेंसिंग के पीछे रहें और तीन सौ मीटर के सुरक्षित दायरे में आ जाएं।'
        };

        if (scenario !== 'custom') {
            scriptBox.value = presets[scenario] || '';
        }
    };

    window.executeVoiceBroadcast = function(e) {
        if (e) e.preventDefault();
        var scenario = document.getElementById('voice-scenario-select').value;
        var zone = document.getElementById('voice-zone').value;
        var officer = document.getElementById('voice-officer').value;
        var text = document.getElementById('voice-script-text').value;
        var mode = document.getElementById('voice-siren-mode').value;
        var speed = parseFloat(document.getElementById('voice-speed').value) || 0.9;
        var cycles = parseInt(document.getElementById('voice-cycles').value) || 2;

        var badge = document.getElementById('voice-broadcast-badge');

        if (!('speechSynthesis' in window)) {
            alert('Speech Synthesis not supported by this device browser engine.');
            return;
        }

        window.stopVoiceBroadcast();
        broadcastActive = true;

        if (badge) {
            badge.style.background = '#7f1d1d';
            badge.style.color = '#fca5a5';
            badge.style.borderColor = '#ef4444';
            badge.innerText = '🚨 BROADCASTING ACTIVE';
        }

        // Trigger hardware siren first if requested
        if (mode === 'siren_voice' || mode === 'siren_continuous') {
            if (typeof window.playDGMSSiren === 'function') {
                window.playDGMSSiren(5000);
            }
        }

        var delayVoiceMs = (mode === 'siren_voice') ? 4500 : 200;

        setTimeout(function() {
            if (!broadcastActive) return;
            playHindiUtterance(text, speed, cycles);
        }, delayVoiceMs);

        // Record statutory broadcast log
        var entry = {
            id: 'VOICE-' + Date.now(),
            date: new Date().toLocaleDateString(),
            time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
            scenario: scenario,
            zone: zone,
            officer: officer,
            script: text,
            seal: 'VOX-SEAL-' + Math.random().toString(36).substring(2, 8).toUpperCase()
        };

        var store = JSON.parse(localStorage.getItem('dgms_voice_logs') || '[]');
        store.unshift(entry);
        localStorage.setItem('dgms_voice_logs', JSON.stringify(store));
        renderVoiceLogs();
    };

    function playHindiUtterance(text, speed, remainingCycles) {
        if (!broadcastActive || remainingCycles <= 0) {
            window.stopVoiceBroadcast();
            return;
        }

        window.speechSynthesis.cancel();
        speechInstance = new SpeechSynthesisUtterance(text);
        speechInstance.rate = speed;
        speechInstance.pitch = 1.0;

        // Auto-select Hindi voice if installed on Android, else system default
        var voices = window.speechSynthesis.getVoices();
        for (var i = 0; i < voices.length; i++) {
            if (voices[i].lang === 'hi-IN' || voices[i].lang.indexOf('hi') === 0) {
                speechInstance.voice = voices[i];
                break;
            }
        }

        speechInstance.onend = function() {
            if (broadcastActive && remainingCycles > 1) {
                setTimeout(function() {
                    playHindiUtterance(text, speed, remainingCycles - 1);
                }, 1000);
            } else {
                window.stopVoiceBroadcast();
            }
        };

        speechInstance.onerror = function() {
            window.stopVoiceBroadcast();
        };

        window.speechSynthesis.speak(speechInstance);
    }

    window.stopVoiceBroadcast = function() {
        broadcastActive = false;
        if ('speechSynthesis' in window) {
            window.speechSynthesis.cancel();
        }
        if (typeof window.stopDGMSSiren === 'function') {
            window.stopDGMSSiren();
        }
        var badge = document.getElementById('voice-broadcast-badge');
        if (badge) {
            badge.style.background = '#14532d';
            badge.style.color = '#4ade80';
            badge.style.borderColor = '#22c55e';
            badge.innerText = 'VOICE ENGINE STANDBY';
        }
    };

    function renderVoiceLogs() {
        var el = document.getElementById('voice-history-list');
        var badge = document.getElementById('voice-logs-count');
        if (!el) return;

        var store = JSON.parse(localStorage.getItem('dgms_voice_logs') || '[]');
        if (badge) badge.innerText = store.length + ' Broadcasts';

        if (store.length === 0) {
            el.innerHTML = '<div style="color:#64748b; padding:4px;">No emergency voice broadcasts transmitted in current shift.</div>';
            return;
        }

        el.innerHTML = store.map(function(item) {
            return `
                <div style="background:#020617; border:1px solid #1e293b; padding:6px 8px; border-radius:4px; margin-bottom:4px;">
                    <div style="display:flex; justify-content:space-between; font-weight:bold;">
                        <span style="color:#ef4444;">🚨 ${item.scenario.toUpperCase()} (${item.zone})</span>
                        <span style="font-family:monospace; color:#f59e0b; font-size:9px;">${item.seal}</span>
                    </div>
                    <div style="color:#cbd5e1; font-size:10px; margin-top:2px; line-height:1.3;">
                        "${item.script.slice(0, 75)}..."
                    </div>
                    <div style="color:#64748b; font-size:9px; margin-top:2px;">
                        ${item.date} ${item.time} • Authorized by Officer: ${item.officer}
                    </div>
                </div>
            `;
        }).join('');
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', injectVoiceUI);
    } else {
        injectVoiceUI();
    }
    setTimeout(injectVoiceUI, 4800);
})();
</script>
"""
