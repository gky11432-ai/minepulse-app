# mg_auth_lock.py - RBAC State Engine & Worker Statutory Lockdown (< 160 Lines)

AUTH_LOCK_SCRIPT = """
<script>
(function() {
    var STORAGE_KEY = 'mineguard_active_user';
    var activeRole = 'WORKER';

    window.switchGatekeeperRole = function(role) {
        activeRole = role;
        var btnWorker = document.getElementById('tab-btn-worker');
        var btnOfficer = document.getElementById('tab-btn-officer');
        var boxWorker = document.getElementById('auth-box-worker');
        var boxOfficer = document.getElementById('auth-box-officer');

        if (role === 'WORKER') {
            btnWorker.classList.add('active');
            btnOfficer.classList.remove('active');
            boxWorker.style.display = 'block';
            boxOfficer.style.display = 'none';
        } else {
            btnOfficer.classList.add('active');
            btnWorker.classList.remove('active');
            boxOfficer.style.display = 'block';
            boxWorker.style.display = 'none';
        }
    };

    window.openGatekeeperLogin = function() {
        var m = document.getElementById('mineguard-gatekeeper-modal');
        if (m) m.style.display = 'flex';
    };

    window.loginAsWorker = function() {
        var token = document.getElementById('gk-worker-token').value || 'Miner (TK-402)';
        var user = {
            name: token,
            role: 'WORKER',
            token: 'TK-' + Math.floor(100 + Math.random() * 900),
            loginTime: new Date().toLocaleTimeString()
        };
        localStorage.setItem(STORAGE_KEY, JSON.stringify(user));
        closeGatekeeperApply(user);
    };

    window.loginAsOfficer = function() {
        var pin = document.getElementById('gk-officer-pin').value;
        if (pin !== '9999') {
            alert('❌ गलत सिक्योरिटी पिन! (Default PIN: 9999)');
            return;
        }
        var desig = document.getElementById('gk-officer-desig').value;
        var user = {
            name: desig,
            role: 'OFFICER',
            token: 'CERT-' + Math.floor(1000 + Math.random() * 9000),
            loginTime: new Date().toLocaleTimeString()
        };
        localStorage.setItem(STORAGE_KEY, JSON.stringify(user));
        closeGatekeeperApply(user);
    };

    function closeGatekeeperApply(user) {
        var m = document.getElementById('mineguard-gatekeeper-modal');
        if (m) m.style.display = 'none';
        updateAuthHeaderUI(user);
        applyStatutoryRoleLock(user.role);
    }

    function updateAuthHeaderUI(user) {
        var nameEl = document.getElementById('auth-display-name');
        var roleEl = document.getElementById('auth-display-role');
        if (!nameEl || !roleEl) return;

        nameEl.innerText = user.name;
        if (user.role === 'OFFICER') {
            roleEl.innerText = 'OFFICER (CERTIFIED)';
            roleEl.className = 'role-badge-pill role-officer';
        } else {
            roleEl.innerText = 'WORKER (READ-ONLY)';
            roleEl.className = 'role-badge-pill role-worker';
        }
    }

    // Enforces Read-Only state across forms for workers
    window.applyStatutoryRoleLock = function(role) {
        var isWorker = (role === 'WORKER');
        var inputs = document.querySelectorAll('#dynamic-module-viewport input, #dynamic-module-viewport select, #dynamic-module-viewport textarea');
        var submitButtons = document.querySelectorAll('#dynamic-module-viewport button[type="submit"]');

        inputs.forEach(function(el) {
            el.disabled = isWorker;
            el.style.opacity = isWorker ? '0.6' : '1';
            el.style.cursor = isWorker ? 'not-allowed' : 'text';
        });

        submitButtons.forEach(function(btn) {
            btn.disabled = isWorker;
            btn.style.opacity = isWorker ? '0.5' : '1';
            btn.style.cursor = isWorker ? 'not-allowed' : 'pointer';
            if (isWorker) {
                btn.innerText = '🔒 Read-Only (Officer Signature Required)';
            }
        });
    };

    // Auto-check session on launch
    function initAuthSession() {
        var raw = localStorage.getItem(STORAGE_KEY);
        if (!raw) {
            // First time launch: default to worker and open gatekeeper
            window.openGatekeeperLogin();
        } else {
            try {
                var user = JSON.parse(raw);
                updateAuthHeaderUI(user);
                applyStatutoryRoleLock(user.role);
            } catch(e) {
                window.openGatekeeperLogin();
            }
        }
    }

    document.addEventListener('DOMContentLoaded', initAuthSession);
    setInterval(function() {
        var user = null;
        try { user = JSON.parse(localStorage.getItem(STORAGE_KEY) || 'null'); } catch(e){}
        if (user) applyStatutoryRoleLock(user.role);
    }, 2000);
})();
</script>
"""
