# ui_nav_logic.py - Navigation Engine, Single-Card Focus & Hardware Controls

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

    // 3. Open Single Module in Focus Mode
    window.openSingleModule = function(cardId, titleName) {
        var drawer = document.getElementById('mineguard-drawer');
        if (drawer && drawer.classList.contains('open')) {
            window.toggleMineGuardDrawer();
        }

        var grid = document.getElementById('dashboard-quick-grid');
        if (grid) grid.style.display = 'none';

        var focusBar = document.getElementById('card-focus-bar');
        var titleEl = document.getElementById('active-card-title');
        if (focusBar) focusBar.style.display = 'flex';
        if (titleEl) titleEl.innerText = titleName || 'Module';

        var allCards = document.querySelectorAll('div[id^="statutory-"]');
        allCards.forEach(function(card) {
            if (card.id === cardId) {
                card.style.display = 'block';
                card.scrollIntoView({ behavior: 'smooth' });
            } else {
                card.style.display = 'none';
            }
        });
    };

    // 4. Return Back to Clean Dashboard Home
    window.showDashboardHome = function() {
        var grid = document.getElementById('dashboard-quick-grid');
        if (grid) grid.style.display = 'grid';

        var focusBar = document.getElementById('card-focus-bar');
        if (focusBar) focusBar.style.display = 'none';

        var allCards = document.querySelectorAll('div[id^="statutory-"]');
        allCards.forEach(function(card) {
            card.style.display = 'none';
        });
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

    // Initial Startup: Hide bulky cards, keep dashboard neat
    setTimeout(function() {
        window.showDashboardHome();
    }, 1200);
})();
</script>
"""
