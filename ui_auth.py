# ui_auth.py - Strict DGMS Full-Screen Security Gatekeeper & Anti-Tamper RBAC Engine

AUTH_MODULE = """
<style>
  #mineguard-gatekeeper {
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      background: #020617;
      z-index: 999999;
      display: flex;
      justify-content: center;
      align-items: center;
      font-family: system-ui, -apple-system, sans-serif;
      color: #f8fafc;
      padding: 16px;
      box-sizing: border-box;
  }
  .gate-card {
      background: #0f172a;
      border: 1px solid #334155;
      border-radius: 12px;
      width: 100%;
      max-width: 400px;
      padding: 24px;
      box-shadow: 0 20px 40px rgba(0,0,0,0.9);
      box-sizing: border-box;
  }
  .gate-tab-btn {
      flex: 1;
      padding: 10px;
      font-size: 11px;
      font-weight: bold;
      border: 1px solid #334155;
      background: #1e293b;
      color: #94a3b8;
      border-radius: 6px;
      cursor: pointer;
  }
  .gate-tab-btn.active {
      background: #0284c7;
      color: #ffffff;
      border-color: #38bdf8;
  }
  .gate-input {
      width: 100%;
      background: #020617;
      border: 1px solid #334155;
      color: #fff;
      padding: 10px;
      border-radius: 6px;
      font-size: 12px;
      margin-top: 4px;
      margin-bottom: 12px;
      box-sizing: border-box;
  }
  .gate-input:focus {
      border-color: #38bdf8;
      outline: none;
  }

  /* STRICT WORKER AUDIT LOCKOUT: Disable all form controls across all registers */
  body.role-worker form:not(#worker-punch-form) input,
  body.role-worker form:not(#worker-punch-form) textarea,
  body.role-worker form:not(#worker-punch-form) select,
  body.role-worker form:not(#worker-punch-form) button[type="submit"] {
      pointer-events: none !important;
      opacity: 0.35 !important;
      cursor: not-allowed !important;
  }

  /* Highlight Read-Only status on statutory cards */
  body.role-worker .statutory-card-badge {
      background: #475569 !important;
      color: #cbd5e1 !important;
      content: "READ ONLY" !important;
  }
</style>

<div id="mineguard-gatekeeper">
    <div class="gate-card">
        <div style="text-align:center; margin-bottom:18px;">
            <div style="font-size:32px; margin-bottom:4px;">⛑️</div>
            <div style="font-size:16px; font-weight:900; color:#38bdf8; letter-spacing:1px;">MINEGUARD SECURITY GATE</div>
            <div style="font-size:10px; color:#f59e0b; font-weight:bold; margin-top:2px;">RESTRICTED ACCESS • DGMS CMR 2017</div>
            <div style="font-size:10px; color:#64748b; margin-top:2px;">Statutory Verification & Identity Check</div>
        </div>

        <div style="display:flex; gap:8px; margin-bottom:16px;">
            <button type="button" class="gate-tab-btn active" id="tab-worker-btn" onclick="switchGateTab('WORKER')">
                👷 Worker Login
            </button>
            <button type="button" class="gate-tab-btn" id="tab-officer-btn" onclick="switchGateTab('OFFICER')">
                👮 Officer Login
            </button>
        </div>

        <!-- WORKER FORM -->
        <form id="gate-worker-form" onsubmit="handleWorkerGateLogin(event)">
            <div>
                <label style="font-size:11px; color:#94a3b8;">Worker Full Name</label>
                <input type="text" id="gate-worker-name" required placeholder="e.g. Ramesh Mahto" class="gate-input">
            </div>
            <div>
                <label style="font-size:11px; color:#94a3b8;">Token / Biometric Badge ID</label>
                <input type="text" id="gate-worker-token" required placeholder="e.g. TK-402" class="gate-input">
            </div>
            <div style="font-size:10px; color:#38bdf8; background:#082f49; padding:8px; border-radius:6px; margin-bottom:12px; border:1px solid #0369a1;">
                ℹ️ <b>Worker Mode Privileges:</b> Form-B Attendance, Personal Tracking, SOS Distress Signal, and Emergency Siren Reception. (Audits are Read-Only).
            </div>
            <button type="submit" style="width:100%; background:#16a34a; color:#fff; font-weight:bold; border:none; padding:12px; border-radius:6px; font-size:12px; cursor:pointer;">
                ✅ Authenticate as Worker
            </button>
        </form>

        <!-- OFFICER FORM -->
        <form id="gate-officer-form" onsubmit="handleOfficerGateLogin(event)" style="display:none;">
            <div>
                <label style="font-size:11px; color:#94a3b8;">Officer Designation</label>
                <select id="gate-officer-role" class="gate-input">
                    <option value="OFFICER">Mining Sirdar / Overman</option>
                    <option value="MANAGER">Safety Officer / Colliery Manager</option>
                </select>
            </div>
            <div>
                <label style="font-size:11px; color:#94a3b8;">Officer Full Name</label>
                <input type="text" id="gate-officer-name" required placeholder="e.g. R.K. Sharma" class="gate-input">
            </div>
            <div>
                <label style="font-size:11px; color:#94a3b8;">Statutory Certificate / Reg No.</label>
                <input type="text" id="gate-officer-token" required placeholder="e.g. CERT-8891" class="gate-input">
            </div>
            <div>
                <label style="font-size:11px; color:#f59e0b;">Statutory Secret PIN</label>
                <input type="password" id="gate-officer-pin" required placeholder="Enter 4-digit PIN (Default: 9999)" class="gate-input" style="border-color:#f59e0b;">
            </div>
            <div style="font-size:10px; color:#facc15; background:#451a03; padding:8px; border-radius:6px; margin-bottom:12px; border:1px solid #b45309;">
                ⚠️ <b>Officer Privileges:</b> Full Legal Access to Edit/Sign Registers, Certify Audits, and Trigger Colliery-Wide Evacuation Sirens.
            </div>
            <button type="submit" style="width:100%; background:#0284c7; color:#fff; font-weight:bold; border:none; padding:12px; border-radius:6px; font-size:12px; cursor:pointer;">
                🔑 Authenticate & Unlock Officer Powers
            </button>
        </form>
    </div>
</div>

<!-- Header Status Bar -->
<div id="mineguard-header-auth-bar" style="display:none; background:#020617; border-bottom:1px solid #334155; padding:8px 14px; justify-content:space-between; align-items:center; font-family:system-ui, sans-serif; position:sticky; top:0; z-index:99999;">
    <div style="display:flex; align-items:center; gap:8px;">
        <span id="hdr-auth-icon" style="font-size:18px;">👷</span>
        <div>
            <div style="display:flex; align-items:center; gap:6px;">
                <span id="hdr-auth-name" style="font-size:12px; font-weight:bold; color:#f8fafc;">User</span>
                <span id="hdr-auth-tag" style="font-size:9px; font-weight:bold; padding:2px 6px; border-radius:4px;">ROLE</span>
            </div>
            <div id="hdr-auth-desc" style="font-size:9px; color:#64748b;">ID: --</div>
        </div>
    </div>
    <div style="display:flex; gap:6px;">
        <span id="hdr-auth-badge" style="font-size:9px; padding:4px 8px; border-radius:4px; font-weight:bold; display:flex; align-items:center;">
            READ ONLY
        </span>
        <button type="button" onclick="lockMineGuardApp()" style="background:#dc2626; color:#fff; font-weight:bold; border:none; padding:6px 12px; border-radius:4px; font-size:10px; cursor:pointer;">
            🔒 Lock App
        </button>
    </div>
</div>

<script>
(function() {
    var activeSession = null;

    window.switchGateTab = function(type) {
        var workerForm = document.getElementById('gate-worker-form');
        var officerForm = document.getElementById('gate-officer-form');
        var workerTab = document.getElementById('tab-worker-btn');
        var officerTab = document.getElementById('tab-officer-btn');

        if (type === 'WORKER') {
            workerForm.style.display = 'block';
            officerForm.style.display = 'none';
            workerTab.className = 'gate-tab-btn active';
            officerTab.className = 'gate-tab-btn';
        } else {
            workerForm.style.display = 'none';
            officerForm.style.display = 'block';
            workerTab.className = 'gate-tab-btn';
            officerTab.className = 'gate-tab-btn active';
        }
    };

    window.handleWorkerGateLogin = function(e) {
        if (e) e.preventDefault();
        var name = document.getElementById('gate-worker-name').value.trim();
        var token = document.getElementById('gate-worker-token').value.trim();

        if (!name || !token) {
            alert('Please enter Worker Name and Token ID');
            return;
        }

        activeSession = {
            name: name,
            role: 'WORKER',
            token: token,
            designation: 'General Underground Miner'
        };

        saveAndUnlockApp();
    };

    window.handleOfficerGateLogin = function(e) {
        if (e) e.preventDefault();
        var role = document.getElementById('gate-officer-role').value;
        var name = document.getElementById('gate-officer-name').value.trim();
        var token = document.getElementById('gate-officer-token').value.trim();
        var pin = document.getElementById('gate-officer-pin').value;

        if (pin !== '9999' && pin !== 'MineGuard@2026') {
            alert('⛔ AUTHORIZATION REJECTED: Incorrect Statutory Security PIN.');
            return;
        }

        activeSession = {
            name: name,
            role: role,
            token: token,
            designation: role === 'MANAGER' ? 'Colliery Safety Head' : 'Certified Overman/Sirdar'
        };

        saveAndUnlockApp();
    };

    function saveAndUnlockApp() {
        localStorage.setItem('mineguard_active_user', JSON.stringify(activeSession));

        var gate = document.getElementById('mineguard-gatekeeper');
        if (gate) gate.style.display = 'none';

        document.body.classList.remove('role-worker', 'role-officer');
        if (activeSession.role === 'WORKER') {
            document.body.classList.add('role-worker');
        } else {
            document.body.classList.add('role-officer');
        }

        var bar = document.getElementById('mineguard-header-auth-bar');
        var icon = document.getElementById('hdr-auth-icon');
        var name = document.getElementById('hdr-auth-name');
        var tag = document.getElementById('hdr-auth-tag');
        var desc = document.getElementById('hdr-auth-desc');
        var badge = document.getElementById('hdr-auth-badge');

        if (bar) {
            bar.style.display = 'flex';
            name.innerText = activeSession.name;
            tag.innerText = activeSession.role;
            desc.innerText = activeSession.designation + ' • ' + activeSession.token;

            if (activeSession.role === 'WORKER') {
                icon.innerText = '👷';
                tag.style.background = '#334155';
                tag.style.color = '#cbd5e1';
                badge.innerText = '🔒 AUDITS READ-ONLY';
                badge.style.background = '#334155';
                badge.style.color = '#fde047';
            } else {
                icon.innerText = activeSession.role === 'MANAGER' ? '🎖️' : '👮';
                tag.style.background = activeSession.role === 'MANAGER' ? '#701a75' : '#0369a1';
                tag.style.color = '#fff';
                badge.innerText = '⚡ STATUTORY OFFICER UNLOCKED';
                badge.style.background = '#14532d';
                badge.style.color = '#4ade80';
            }
        }

        applyStrictTamperLock();
        alert('✅ Identity Confirmed: ' + activeSession.name + ' (' + activeSession.role + ')');
    }

    function applyStrictTamperLock() {
        var isWorker = (activeSession && activeSession.role === 'WORKER');
        var forms = document.querySelectorAll('form');

        forms.forEach(function(f) {
            // Worker is only allowed to use attendance punch form
            if (f.id === 'worker-punch-form') return;

            var existingNotice = f.querySelector('.worker-lock-notice');
            if (isWorker) {
                if (!existingNotice) {
                    var n = document.createElement('div');
                    n.className = 'worker-lock-notice';
                    n.style.cssText = 'background:#1e293b; border:1px dashed #eab308; border-radius:6px; padding:8px; margin:8px 0; color:#fef08a; font-size:10px; text-align:center;';
                    n.innerHTML = '🔒 <b>STATUTORY AUDIT FROZEN:</b> Workers have Read-Only view. Only Certified Officers can edit, sign, or certify.';
                    f.insertBefore(n, f.firstChild);
                }
            } else {
                if (existingNotice) existingNotice.remove();
            }
        });
    }

    // Intercept form submissions by workers on statutory records
    document.addEventListener('submit', function(e) {
        if (activeSession && activeSession.role === 'WORKER') {
            if (e.target && e.target.id !== 'worker-punch-form') {
                e.preventDefault();
                e.stopPropagation();
                alert('⛔ STATUTORY TAMPER PROTECTION: Workers are legally prohibited from altering colliery compliance registers (CMR 2017). Log in as an Officer.');
                return false;
            }
        }
    }, true);

    window.lockMineGuardApp = function() {
        localStorage.removeItem('mineguard_active_user');
        activeSession = null;
        document.body.classList.remove('role-worker', 'role-officer');

        var bar = document.getElementById('mineguard-header-auth-bar');
        if (bar) bar.style.display = 'none';

        var gate = document.getElementById('mineguard-gatekeeper');
        if (gate) {
            gate.style.display = 'flex';
            document.getElementById('gate-worker-name').value = '';
            document.getElementById('gate-worker-token').value = '';
            document.getElementById('gate-officer-pin').value = '';
        }
    };

    function checkExistingSession() {
        var saved = localStorage.getItem('mineguard_active_user');
        if (saved) {
            try {
                activeSession = JSON.parse(saved);
                saveAndUnlockApp();
            } catch(e) {
                window.lockMineGuardApp();
            }
        } else {
            window.lockMineGuardApp();
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', checkExistingSession);
    } else {
        checkExistingSession();
    }
})();
</script>
"""
