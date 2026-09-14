# mg_nav_logic.py - Offline Language Switcher, Shift HUD & Module Engine (< 190 Lines)

NAV_LOGIC_SCRIPT = """
<script>
(function() {
    var torchTrack = null;
    var isTorchOn = false;
    var currentLang = localStorage.getItem('mineguard_lang') || 'HI';

    // 1. Language Switcher Engine (Instant Offline Translation)
    window.toggleAppLanguage = function() {
        currentLang = (currentLang === 'HI') ? 'EN' : 'HI';
        localStorage.setItem('mineguard_lang', currentLang);
        applyLanguageStrings();
    };

    function applyLanguageStrings() {
        var pill = document.getElementById('app-lang-pill');
        if (pill) pill.innerHTML = (currentLang === 'HI') ? '🌐 English' : '🌐 हिन्दी';
        document.querySelectorAll('[data-en][data-hi]').forEach(function(el) {
            var val = (currentLang === 'HI') ? el.getAttribute('data-hi') : el.getAttribute('data-en');
            if (val) el.innerHTML = val;
        });
        var search = document.getElementById('drawer-search-input');
        if (search) search.placeholder = (currentLang === 'HI') ? '🔍 खोजें / Search...' : '🔍 Search register...';
    }

    // 2. Shift & Battery Telemetry Engine
    function updateTelemetryHUD() {
        var now = new Date();
        var hrs = now.getHours();
        var shift = (hrs >= 6 && hrs < 14) ? 'SHIFT 1 (06-14)' : (hrs >= 14 && hrs < 22) ? 'SHIFT 2 (14-22)' : 'SHIFT 3 (22-06)';
        var pill = document.getElementById('telemetry-shift-pill');
        if (pill) pill.innerText = '⏱️ ' + shift;
        var clock = document.getElementById('telemetry-time');
        if (clock) clock.innerText = now.toLocaleTimeString();

        if (navigator.getBattery) {
            navigator.getBattery().then(function(b) {
                var el = document.getElementById('telemetry-battery');
                if (el) el.innerText = (b.level * 100 > 20 ? '🔋 ' : '🪫 ') + Math.round(b.level * 100) + '%';
            }).catch(function(){});
        }
        var net = document.getElementById('telemetry-network');
        if (net) {
            net.innerText = navigator.onLine ? '🟢 ONLINE' : '🟠 OFFLINE';
            net.style.color = navigator.onLine ? '#34d399' : '#fbbf24';
        }
    }

    // 3. Hide legacy clutter from clean home screen
    function tagLegacyElements() {
        var allowed = ['mineguard-navbar', 'telemetry-status-strip', 'card-focus-bar', 'dashboard-quick-grid', 'mineguard-drawer', 'mineguard-drawer-overlay', 'mg-evac-hud', 'mineguard-form6-modal', 'dynamic-module-viewport'];
        for (var i = 0; i < document.body.children.length; i++) {
            var c = document.body.children[i];
            if (c.id && allowed.indexOf(c.id) !== -1) continue;
            if (c.tagName === 'SCRIPT' || c.tagName === 'STYLE') continue;
            c.classList.add('mg-legacy-item');
        }
        document.querySelectorAll('.card, [class*="card"], div[id^="statutory-"]').forEach(function(el) {
            el.classList.add('mg-legacy-item');
        });
    }

    // 4. Drawer Toggle & Search
    window.toggleMineGuardDrawer = function() {
        var d = document.getElementById('mineguard-drawer');
        var o = document.getElementById('mineguard-drawer-overlay');
        if (!d || !o) return;
        var isOpen = d.classList.contains('open');
        d.classList.toggle('open', !isOpen);
        o.style.display = !isOpen ? 'block' : 'none';
        if (!isOpen) {
            var s = document.getElementById('drawer-search-input');
            if (s) { s.value = ''; filterDrawerItems(); }
        }
    };

    window.filterDrawerItems = function() {
        var q = (document.getElementById('drawer-search-input').value || '').toLowerCase();
        document.querySelectorAll('.drawer-item').forEach(function(item) {
            item.style.display = (item.innerText || '').toLowerCase().indexOf(q) !== -1 ? 'flex' : 'none';
        });
    };

    // 5. Clean Home & Single-Card Focus Engine
    window.showDashboardHome = function() {
        document.body.classList.remove('mode-focus');
        document.body.classList.add('mode-home');
        document.querySelectorAll('.active-focus-target').forEach(function(el) { el.classList.remove('active-focus-target'); });
        var dyn = document.getElementById('dynamic-module-viewport');
        if (dyn) { dyn.innerHTML = ''; dyn.style.display = 'none'; }
        window.scrollTo({ top: 0, behavior: 'smooth' });
    };

    window.openUniversalModule = function(key, title) {
        var d = document.getElementById('mineguard-drawer');
        if (d && d.classList.contains('open')) window.toggleMineGuardDrawer();

        document.body.classList.remove('mode-home');
        document.body.classList.add('mode-focus');
        var titleEl = document.getElementById('active-card-title');
        if (titleEl) titleEl.innerText = title || 'Statutory Register';
        document.querySelectorAll('.active-focus-target').forEach(function(el) { el.classList.remove('active-focus-target'); });

        var target = document.getElementById('statutory-' + key + '-card') || document.getElementById(key + '-card') || document.getElementById('statutory-' + key);
        var dyn = document.getElementById('dynamic-module-viewport');

        if (target) {
            if (dyn) dyn.style.display = 'none';
            target.classList.add('active-focus-target');
            var p = target.parentElement;
            while (p && p !== document.body) { p.classList.add('active-focus-target'); p = p.parentElement; }
        } else if (dyn) {
            dyn.style.display = 'block';
            dyn.innerHTML = buildDynamicStatutoryCard(key, title);
        }
        window.scrollTo({ top: 0, behavior: 'smooth' });
    };

    function buildDynamicStatutoryCard(key, title) {
        var storageKey = 'dgms_dyn_' + key + '_logs';
        var logs = JSON.parse(localStorage.getItem(storageKey) || '[]');
        var rows = logs.length === 0 ? '<tr><td colspan="4" style="text-align:center; padding:10px; color:#64748b;">No records logged yet.</td></tr>' : '';
        logs.slice(0, 5).forEach(function(l) {
            rows += '<tr><td style="border:1px solid #334155; padding:6px;">' + l.time + '</td><td style="border:1px solid #334155; padding:6px;">' + l.officer + '</td><td style="border:1px solid #334155; padding:6px;">' + l.status + '</td><td style="border:1px solid #334155; padding:6px;">' + l.remarks + '</td></tr>';
        });
        var isHi = (currentLang === 'HI');
        return `
            <div style="background:#0f172a; border:1px solid #334155; border-radius:12px; padding:16px; font-family:system-ui, sans-serif; color:#f8fafc; max-width:600px; margin:0 auto;">
                <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #1e293b; padding-bottom:8px; margin-bottom:12px;">
                    <div><b style="color:#38bdf8; font-size:14px;">${title}</b><div style="font-size:10px; color:#94a3b8;">DGMS Statutory Register (CMR 2017)</div></div>
                    <span style="background:#0369a1; color:#fff; font-size:9px; padding:2px 8px; border-radius:4px; font-weight:bold;">LIVE REGISTER</span>
                </div>
                <form onsubmit="handleDynamicSubmit(event, '${storageKey}', '${title}')" style="display:flex; flex-direction:column; gap:10px;">
                    <div><label style="font-size:11px; color:#94a3b8;">${isHi ? 'स्थान / सीम (Location / Seam)' : 'District / Working Seam'}</label><input type="text" id="dyn-loc" required placeholder="e.g. 2nd Dip Face" style="width:100%; background:#020617; border:1px solid #334155; color:#fff; padding:8px; border-radius:6px; font-size:11px; box-sizing:border-box;"></div>
                    <div><label style="font-size:11px; color:#94a3b8;">${isHi ? 'रीडिंग / निरीक्षण (Observation)' : 'Observation / Test Reading'}</label><input type="text" id="dyn-read" required placeholder="e.g. Roof sound & safe" style="width:100%; background:#020617; border:1px solid #334155; color:#fff; padding:8px; border-radius:6px; font-size:11px; box-sizing:border-box;"></div>
                    <div><label style="font-size:11px; color:#94a3b8;">${isHi ? 'स्थिति (Status)' : 'Status'}</label><select id="dyn-stat" style="width:100%; background:#020617; border:1px solid #334155; color:#fff; padding:8px; border-radius:6px; font-size:11px; box-sizing:border-box;"><option value="SATISFACTORY">✅ Satisfactory</option><option value="ATTENTION">⚠️ Attention Needed</option><option value="DANGER">⛔ Danger Stopped</option></select></div>
                    <button type="submit" style="background:#0284c7; color:#fff; font-weight:bold; border:none; padding:10px; border-radius:6px; font-size:12px; cursor:pointer;">📝 ${isHi ? 'प्रमाणित करें एवं सील लगाएं' : 'Sign & Certify Entry'}</button>
                </form>
                <div style="margin-top:16px;"><b style="font-size:11px; color:#cbd5e1;">${isHi ? 'प्रमाणित रिकॉर्ड लेजर' : 'Certified History Ledger'}</b><table style="width:100%; border-collapse:collapse; font-size:10px; margin-top:6px; text-align:left;"><thead><tr style="background:#1e293b; color:#94a3b8;"><th style="border:1px solid #334155; padding:6px;">Time</th><th style="border:1px solid #334155; padding:6px;">Officer</th><th style="border:1px solid #334155; padding:6px;">Status</th><th style="border:1px solid #334155; padding:6px;">Remarks</th></tr></thead><tbody>${rows}</tbody></table></div>
            </div>
        `;
    }

    window.handleDynamicSubmit = function(e, key, title) {
        e.preventDefault();
        var user = JSON.parse(localStorage.getItem('mineguard_active_user') || 'null');
        if (user && user.role === 'WORKER') {
            alert(currentLang === 'HI' ? '⛔ केवल प्रमाणित अधिकारी ही साइन कर सकते हैं।' : '⛔ Officers only: Workers have read-only rights.');
            return;
        }
        var entry = { id: 'REG-' + Date.now(), time: new Date().toLocaleTimeString(), officer: user ? user.name : 'Mining Sirdar', status: document.getElementById('dyn-stat').value, remarks: document.getElementById('dyn-read').value };
        var logs = JSON.parse(localStorage.getItem(key) || '[]');
        logs.unshift(entry);
        localStorage.setItem(key, JSON.stringify(logs));
        alert(currentLang === 'HI' ? '✅ रिकॉर्ड सफलतापूर्वक दर्ज किया गया।' : '✅ Statutory entry certified.');
        window.openUniversalModule(key.replace('dgms_dyn_', '').replace('_logs', ''), title);
    };

    // 6. Universal SOS Trigger Bridge
    window.triggerUniversalCollierySOS = function() {
        var warn = (currentLang === 'HI') ? "🚨 चेतावनी: क्या आप पूरी खदान में आपातकालीन सायरन बजाना चाहते हैं?\\n\\nयह सभी फोन में एक साथ बजेगा!" : "🚨 Trigger emergency siren across ALL colliery phones?";
        if (!confirm(warn)) return;
        if (typeof window.broadcastCollierySOS === 'function') window.broadcastCollierySOS('Emergency Distress SOS Triggered');
        else if (typeof window.playDGMSSirenAudio === 'function') window.playDGMSSirenAudio(15000);
    };

    // 7. Hardware Torch
    window.toggleHardwareTorch = function() {
        var btn = document.getElementById('btn-quick-torch');
        if (!isTorchOn) {
            if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
                navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } }).then(function(stream) {
                    var track = stream.getVideoTracks()[0];
                    var cap = track.getCapabilities ? track.getCapabilities() : {};
                    if (cap.torch) {
                        track.applyConstraints({ advanced: [{ torch: true }] }).then(function() {
                            torchTrack = track; isTorchOn = true;
                            if (btn) { btn.style.background = '#f59e0b'; btn.style.color = '#000'; }
                        });
                    } else { alert('Torch not supported on this camera.'); track.stop(); }
                }).catch(function() { alert('Camera permission needed for Torch.'); });
            }
        } else {
            if (torchTrack) { torchTrack.stop(); torchTrack = null; }
            isTorchOn = false;
            if (btn) { btn.style.background = '#1e293b'; btn.style.color = '#f8fafc'; }
        }
    };

    document.addEventListener('DOMContentLoaded', function() {
        tagLegacyElements();
        window.showDashboardHome();
        applyLanguageStrings();
        updateTelemetryHUD();
    });
    setInterval(updateTelemetryHUD, 1000);
})();
</script>
"""
