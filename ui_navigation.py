# ui_navigation.py - 4-Category Fast Navigation Tabs, Hardware Torch & Telemetry Bar

NAVIGATION_MODULE = """
<style>
  .nav-tab-bar {
      display: flex;
      gap: 6px;
      overflow-x: auto;
      padding: 10px 14px;
      background: #020617;
      border-bottom: 1px solid #1e293b;
      position: sticky;
      top: 48px;
      z-index: 9999;
  }
  .nav-tab-btn {
      flex: 1;
      min-width: 110px;
      padding: 8px 10px;
      font-size: 11px;
      font-weight: bold;
      border: 1px solid #334155;
      background: #0f172a;
      color: #94a3b8;
      border-radius: 6px;
      cursor: pointer;
      text-align: center;
      white-space: nowrap;
      transition: all 0.2s ease;
  }
  .nav-tab-btn.active {
      background: #0284c7;
      color: #ffffff;
      border-color: #38bdf8;
      box-shadow: 0 2px 8px rgba(2,132,199,0.4);
  }
</style>

<div id="mineguard-top-telemetry-strip" style="background:#0f172a; border-bottom:1px solid #1e293b; padding:6px 14px; display:flex; justify-content:space-between; align-items:center; font-family:system-ui, sans-serif; font-size:10px;">
    <!-- Live Network/DB Sync Pill -->
    <div id="mineguard-sync-indicator" onclick="checkAndSyncWithCloud()" style="background:#451a03; color:#fbbf24; border:1px solid #d97706; padding:3px 10px; border-radius:12px; cursor:pointer; font-weight:bold;">
        🟠 <b>OFFLINE</b> • Stored in Vault
    </div>

    <!-- Hardware Camera LED Torch Toggle -->
    <button type="button" id="btn-hardware-torch" onclick="toggleHardwareTorch()" style="background:#1e293b; border:1px solid #334155; color:#f8fafc; font-weight:bold; padding:4px 10px; border-radius:12px; cursor:pointer; display:flex; align-items:center; gap:4px;">
        🔦 <span>Torch: OFF</span>
    </button>
</div>

<!-- 4 Easy Category Tabs -->
<div class="nav-tab-bar" id="mineguard-category-tabs">
    <button type="button" class="nav-tab-btn active" onclick="switchCategoryTab('SHIFT', this)">
        📋 Shift & Duty
    </button>
    <button type="button" class="nav-tab-btn" onclick="switchCategoryTab('AUDITS', this)">
        🛡️ Safety Audits
    </button>
    <button type="button" class="nav-tab-btn" onclick="switchCategoryTab('PLANT', this)">
        🚜 Machinery
    </button>
    <button type="button" class="nav-tab-btn" onclick="switchCategoryTab('EMERGENCY', this)">
        🚨 Emergency
    </button>
</div>

<script>
(function() {
    var torchTrack = null;
    var isTorchOn = false;

    // 1. Hardware Flashlight (Torch) Engine
    window.toggleHardwareTorch = function() {
        var btn = document.getElementById('btn-hardware-torch');
        if (!isTorchOn) {
            if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
                navigator.mediaDevices.getUserMedia({
                    video: { facingMode: 'environment' }
                }).then(function(stream) {
                    var track = stream.getVideoTracks()[0];
                    var capabilities = track.getCapabilities ? track.getCapabilities() : {};
                    if (capabilities.torch) {
                        track.applyConstraints({ advanced: [{ torch: true }] }).then(function() {
                            torchTrack = track;
                            isTorchOn = true;
                            if (btn) {
                                btn.style.background = '#f59e0b';
                                btn.style.color = '#000000';
                                btn.innerHTML = '🔦 <span>Torch: ON</span>';
                            }
                        });
                    } else {
                        alert('Notice: Device camera does not support hardware torch mode.');
                        track.stop();
                    }
                }).catch(function(e) {
                    alert('Torch error: Camera permission required.');
                });
            }
        } else {
            if (torchTrack) {
                torchTrack.stop();
                torchTrack = null;
            }
            isTorchOn = false;
            if (btn) {
                btn.style.background = '#1e293b';
                btn.style.color = '#f8fafc';
                btn.innerHTML = '🔦 <span>Torch: OFF</span>';
            }
        }
    };

    // 2. 4-Category Layout Router
    var CATEGORY_MAP = {
        'SHIFT': [
            'statutory-attendance-card',
            'statutory-tracking-card',
            'statutory-diary-card',
            'statutory-lamproom-card',
            'statutory-handover-card',
            'statutory-muster-card'
        ],
        'AUDITS': [
            'statutory-ventilation-card',
            'statutory-strata-card',
            'statutory-blasting-card',
            'statutory-inundation-card',
            'statutory-dust-card',
            'statutory-fire-card',
            'statutory-medical-card',
            'statutory-smp-card'
        ],
        'PLANT': [
            'statutory-machinery-card',
            'statutory-haulage-card',
            'statutory-electrical-card',
            'statutory-winding-card',
            'statutory-calibration-card'
        ],
        'EMERGENCY': [
            'statutory-simulator-card',
            'statutory-accident-card',
            'statutory-backup-card',
            'statutory-rescue-card',
            'statutory-voice-card',
            'statutory-alerts-card'
        ]
    };

    window.switchCategoryTab = function(category, btnEl) {
        document.querySelectorAll('.nav-tab-btn').forEach(function(b) {
            b.classList.remove('active');
        });
        if (btnEl) btnEl.classList.add('active');

        var allowedIds = CATEGORY_MAP[category] || [];
        var allCards = document.querySelectorAll('div[id^="statutory-"]');

        allCards.forEach(function(card) {
            if (allowedIds.indexOf(card.id) !== -1) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    };

    // Initialize Default Tab on Startup
    setTimeout(function() {
        var firstTab = document.querySelector('.nav-tab-btn');
        if (firstTab) window.switchCategoryTab('SHIFT', firstTab);
    }, 1000);
})();
</script>
"""
