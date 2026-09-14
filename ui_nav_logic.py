# ui_nav_logic.py - Strict Single-Card Focus, Deep Clean Engine & Controls

NAV_LOGIC_SCRIPT = """
<script>
(function() {
    var torchTrack = null;
    var isTorchOn = false;

    // 1. Universal One-Touch Emergency SOS
    window.triggerUniversalCollierySOS = function() {
        var proceed = confirm("🚨 चेतावनी / WARNING:\\n\\nक्या आप पूरी खदान में आपातकालीन सायरन बजाना चाहते हैं?\\n\\nयह सभी के फोन में एक साथ बजेगा!");
        if (!proceed) return;

        if (typeof window.triggerCollieryEvacuationSiren === 'function') {
            window.triggerCollieryEvacuationSiren('Emergency Distress SOS Triggered');
        } else if (typeof window.playDGMSSiren === 'function') {
            window.playDGMSSiren(15000);
            alert('🚨 EMERGENCY SOS ACTIVATED!');
        }
    };

    // 2. Drawer Open / Close Toggle
    window.toggleMineGuardDrawer = function() {
        var drawer = document.getElementById('mineguard-drawer');
        var overlay = document.getElementById('mineguard-drawer-overlay');
        if (!drawer || !overlay) return;

        if (drawer.classList.contains('open')) {
            drawer.classList.remove('open');
            overlay.style.display = 'none';
        } else {
            drawer.classList.add('open');
            overlay.style.display = 'block';
            var search = document.getElementById('drawer-search-input');
            if (search) search.value = '';
            filterDrawerItems();
        }
    };

    // 3. Open Single Module in Focus Mode (बाकी सब कुछ स्क्रीन से हटाकर सिर्फ यह कार्ड खोलो)
    window.openSingleModule = function(cardId, titleName) {
        var drawer = document.getElementById('mineguard-drawer');
        if (drawer && drawer.classList.contains('open')) {
            window.toggleMineGuardDrawer();
        }

        // Switch to Focus Mode
        document.body.classList.remove('mode-home');
        document.body.classList.add('mode-focus');

        var titleEl = document.getElementById('active-card-title');
        if (titleEl) titleEl.innerText = titleName || 'Statutory Register';

        // Clear previous active cards
        document.querySelectorAll('.active-focus-card').forEach(function(el) {
            el.classList.remove('active-focus-card');
        });

        // Target and unhide selected card
        var target = document.getElementById(cardId);
        if (!target) {
            target = document.querySelector('.' + cardId) || document.querySelector('[data-card="' + cardId + '"]');
        }

        if (target) {
            target.classList.add('active-focus-card');
            target.style.display = 'block';

            // Agar card kisi wrapper/parent ke andar ho, toh parent ko bhi active karo taaki CSS hide na kare
            var p = target.parentElement;
            while (p && p !== document.body) {
                p.classList.add('active-focus-card');
                p.style.display = 'block';
                p = p.parentElement;
            }
            window.scrollTo({ top: 0, behavior: 'smooth' });
        } else {
            alert('Opening ' + titleName + '...');
        }
    };

    // 4. Return Back to Clean Home (सिर्फ सायरन वाली होम स्क्रीन पर वापस जाओ)
    window.showDashboardHome = function() {
        document.body.classList.remove('mode-focus');
        document.body.classList.add('mode-home');

        document.querySelectorAll('.active-focus-card').forEach(function(el) {
            el.classList.remove('active-focus-card');
        });

        window.scrollTo({ top: 0, behavior: 'smooth' });
    };

    // 5. Form 6 Direct Opener
    window.openForm6ReportDirect = function() {
        var drawer = document.getElementById('mineguard-drawer');
        if (drawer && drawer.classList.contains('open')) {
            window.toggleMineGuardDrawer();
        }
        if (typeof window.openForm6Report === 'function') {
            window.openForm6Report();
        } else {
            alert('Opening DGMS Form 6...');
        }
    };

    // 6. Drawer Search Filter
    window.filterDrawerItems = function() {
        var q = (document.getElementById('drawer-search-input').value || '').toLowerCase();
        var items = document.querySelectorAll('.drawer-item');
        items.forEach(function(item) {
            var txt = (item.innerText || '').toLowerCase();
            item.style.display = (txt.indexOf(q) !== -1) ? 'flex' : 'none';
        });
    };

    // 7. Hardware Torch Toggle
    window.toggleHardwareTorch = function() {
        var btn = document.getElementById('btn-quick-torch');
        if (!isTorchOn) {
            if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
                navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } }).then(function(stream) {
                    var track = stream.getVideoTracks()[0];
                    var cap = track.getCapabilities ? track.getCapabilities() : {};
                    if (cap.torch) {
                        track.applyConstraints({ advanced: [{ torch: true }] }).then(function() {
                            torchTrack = track;
                            isTorchOn = true;
                            if (btn) { btn.style.background = '#f59e0b'; btn.style.color = '#000'; }
                        });
                    } else {
                        alert('Device camera does not support hardware torch.');
                        track.stop();
                    }
                }).catch(function() { alert('Camera permission required for Torch.'); });
            }
        } else {
            if (torchTrack) { torchTrack.stop(); torchTrack = null; }
            isTorchOn = false;
            if (btn) { btn.style.background = '#1e293b'; btn.style.color = '#f8fafc'; }
        }
    };

    // Initial Enforcement
    document.addEventListener('DOMContentLoaded', window.showDashboardHome);
    setTimeout(window.showDashboardHome, 500);
})();
</script>
"""
