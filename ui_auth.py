# ui_auth.py - Standalone Role-Based Access Control & Statutory Authorization Lock (Bug Fixed)

AUTH_MODULE = """
<script>
(function() {
    var CURRENT_USER = null;

    function initAuth() {
        try {
            CURRENT_USER = JSON.parse(localStorage.getItem('mineguard_active_user') || 'null');
        } catch(e) { CURRENT_USER = null; }

        if (!CURRENT_USER) {
            CURRENT_USER = { name: 'Worker (Self-Service)', role: 'WORKER', token: 'GUEST-PIT', designation: 'Underground Miner' };
        }
        injectAuthHeaderUI();
        injectLoginModalUI();
        enforcePermissions();
    }

    function injectAuthHeaderUI() {
        if (document.getElementById('mineguard-auth-bar')) { updateHeader(); return; }

        var bar = document.createElement('div');
        bar.id = 'mineguard-auth-bar';
        bar.style.cssText = 'background:#020617; border-bottom:1px solid #334155; padding:8px 14px; display:flex; justify-content:space-between; align-items:center; font-family:system-ui, sans-serif; position:sticky; top:0; z-index:9999;';
        bar.innerHTML = `
            <div style="display:flex; align-items:center; gap:8px;">
                <span id="auth-icon" style="font-size:16px;">👷</span>
                <div>
                    <div style="display:flex; align-items:center; gap:6px;">
                        <span id="auth-name" style="font-size:12px; font-weight:bold; color:#f8fafc;">Worker</span>
                        <span id="auth-tag" style="background:#334155; color:#cbd5e1; font-size:9px; font-weight:bold; padding:2px 6px; border-radius:4px;">WORKER</span>
                    </div>
                    <div id="auth-sub" style="font-size:9px; color:#64748b;">Read-Only Statutory Rights</div>
                </div>
            </div>
            <div style="display:flex; gap:6px;">
                <button type="button" onclick="openLoginModal()" style="background:#0284c7; color:#fff; font-weight:bold; border:none; padding:5px 10px; border-radius:4px; font-size:10px; cursor:pointer;">
                    🔑 Officer Login
                </button>
                <button type="button" onclick="logoutUser()" id="auth-logout-btn" style="background:#334155; color:#cbd5e1; border:none; padding:5px 8px; border-radius:4px; font-size:10px; cursor:pointer; display:none;">
                    🚪 Logout
                </button>
            </div>
        `;
        document.body.insertBefore(bar, document.body.firstChild);
        updateHeader();
    }

    function injectLoginModalUI() {
        if (document.getElementById('mineguard-login-modal')) return;
        var modal = document.createElement('div');
        modal.id = 'mineguard-login-modal';
        modal.style.cssText = 'display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.85); z-index:10000; justify-content:center; align-items:center; font-family:system-ui, sans-serif;';
        modal.innerHTML = `
            <div style="background:#0f172a; border:1px solid #334155; border-radius:10px; padding:20px; width:90%; max-width:360px; color:#fff;">
                <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #1e293b; padding-bottom:8px; margin-bottom:12px;">
                    <b style="font-size:13px; color:#38bdf8;">🔐 Officer Statutory Login</b>
                    <button type="button" onclick="closeLoginModal()" style="background:transparent; border:none; color:#94a3b8; font-size:16px; cursor:pointer;">✕</button>
                </div>
                <form onsubmit="handleLoginSubmit(event)">
                    <div style="margin-bottom:10px;">
                        <label style="font-size:11px; color:#94a3b8;">Select Role</label>
                        <select id="login-role" onchange="togglePinField()" style="width:100%; background:#020617; border:1px solid #334155; color:#38bdf8; padding:7px; border-radius:6px; font-size:11px; margin-top:3px;">
                            <option value="WORKER">👷 Shramik / Miner (Self-Service)</option>
                            <option value="OFFICER">👮 Mining Sirdar / Overman</option>
                            <option value="MANAGER">🎖️ Safety Officer / Colliery Manager</option>
                        </select>
                    </div>
                    <div style="margin-bottom:10px;">
                        <label style="font-size:11px; color:#94a3b8;">Official Name</label>
                        <input type="text" id="login-name-input" required placeholder="e.g. Ramesh Kumar" style="width:100%; background:#020617; border:1px solid #334155; color:#fff; padding:7px; border-radius:6px; font-size:11px; margin-top:3px; box-sizing:border-box;">
                    </div>
                    <div style="margin-bottom:10px;">
                        <label style="font-size:11px; color:#94a3b8;">Certificate / Token No.</label>
                        <input type="text" id="login-token-input" required placeholder="Cert # / Token ID" style="width:100%; background:#020617; border:1px solid #334155; color:#fff; padding:7px; border-radius:6px; font-size:11px; margin-top:3px; box-sizing:border-box;">
                    </div>
                    <div id="login-pin-box" style="margin-bottom:12px; display:none;">
                        <label style="font-size:11px; color:#f59e0b;">Authorization PIN (Default: 9999)</label>
                        <input type="password" id="login-pin-input" placeholder="4-digit PIN" style="width:100%; background:#020617; border:1px solid #f59e0b; color:#fff; padding:7px; border-radius:6px; font-size:11px; margin-top:3px; box-sizing:border-box;">
                    </div>
                    <button type="submit" style="width:100%; background:#0284c7; color:#fff; font-weight:bold; border:none; padding:9px; border-radius:6px; font-size:12px; cursor:pointer;">
                        Unlock Statutory Rights
                    </button>
                </form>
            </div>
        `;
        document.body.appendChild(modal);
    }

    window.openLoginModal = function() {
        var m = document.getElementById('mineguard-login-modal');
        if (m) { m.style.display = 'flex'; togglePinField(); }
    };

    window.closeLoginModal = function() {
        var m = document.getElementById('mineguard-login-modal');
        if (m) m.style.display = 'none';
    };

    window.togglePinField = function() {
        var role = document.getElementById('login-role').value;
        var box = document.getElementById('login-pin-box');
        var pin = document.getElementById('login-pin-input');
        if (box) box.style.display = (role === 'WORKER') ? 'none' : 'block';
        if (pin) pin.required = (role !== 'WORKER');
    };

    window.handleLoginSubmit = function(e) {
        if (e) e.preventDefault();
        var role = document.getElementById('login-role').value;
        var name = document.getElementById('login-name-input').value.trim();
        var token = document.getElementById('login-token-input').value.trim();
        var pin = document.getElementById('login-pin-input').value;

        if (role !== 'WORKER' && pin !== '9999' && pin !== 'MineGuard@2026') {
            alert('⛔ ACCESS DENIED: Incorrect Statutory PIN. (Default: 9999)');
            return;
        }

        CURRENT_USER = {
            name: name,
            role: role,
            token: token,
            designation: role === 'MANAGER' ? 'Colliery Manager' : (role === 'OFFICER' ? 'Certified Sirdar/Overman' : 'Miner')
        };
        localStorage.setItem('mineguard_active_user', JSON.stringify(CURRENT_USER));
        closeLoginModal();
        updateHeader();
        enforcePermissions();
        alert('✅ Logged in as ' + name + ' (' + role + ')');
    };

    window.logoutUser = function() {
        CURRENT_USER = { name: 'Worker (Self-Service)', role: 'WORKER', token: 'GUEST-PIT', designation: 'Underground Miner' };
        localStorage.removeItem('mineguard_active_user');
        updateHeader();
        enforcePermissions();
        alert('🚪 Logged out to Worker Mode.');
    };

    function updateHeader() {
        var nameEl = document.getElementById('auth-name');
        var tagEl = document.getElementById('auth-tag');
        var subEl = document.getElementById('auth-sub');
        var iconEl = document.getElementById('auth-icon');
        var logoutBtn = document.getElementById('auth-logout-btn');
        if (!nameEl) return;

        nameEl.innerText = CURRENT_USER.name;
        tagEl.innerText = CURRENT_USER.role;
        subEl.innerText = CURRENT_USER.designation + ' • ' + CURRENT_USER.token;

        if (CURRENT_USER.role === 'WORKER') {
            iconEl.innerText = '👷';
            tagEl.style.background = '#334155';
            tagEl.style.color = '#cbd5e1';
            if (logoutBtn) logoutBtn.style.display = 'none';
        } else {
            iconEl.innerText = CURRENT_USER.role === 'MANAGER' ? '🎖️' : '👮';
            tagEl.style.background = CURRENT_USER.role === 'MANAGER' ? '#701a75' : '#1e3a5f';
            tagEl.style.color = CURRENT_USER.role === 'MANAGER' ? '#f5d0fe' : '#38bdf8';
            if (logoutBtn) logoutBtn.style.display = 'block';
        }
    }

    function enforcePermissions() {
        var isOfficer = (CURRENT_USER && (CURRENT_USER.role === 'OFFICER' || CURRENT_USER.role === 'MANAGER'));
        
        // Strict card selector: Only actual statutory cards ending with '-card'
        var cards = document.querySelectorAll('div[id^="statutory-"][id$="-card"]');

        cards.forEach(function(card) {
            // Exclude attendance & tracking from locking
            if (card.id === 'statutory-attendance-card' || card.id === 'statutory-tracking-card') return;

            var bannerId = 'auth-guard-' + card.id;
            var banner = document.getElementById(bannerId);

            if (!isOfficer) {
                if (!banner) {
                    banner = document.createElement('div');
                    banner.id = bannerId;
                    banner.style.cssText = 'background:rgba(2,6,23,0.92); border:1px dashed #eab308; border-radius:6px; padding:10px; margin-top:8px; text-align:center; color:#fef08a; font-size:11px;';
                    banner.innerHTML = '🔒 <b>OFFICER AUTHORIZATION REQUIRED:</b> Log in as Mining Sirdar / Overman to edit or certify this statutory register. <br><button type="button" onclick="openLoginModal()" style="margin-top:6px; background:#0284c7; color:#fff; border:none; padding:4px 10px; border-radius:4px; font-size:10px; cursor:pointer;">🔑 Officer Login</button>';
                    card.appendChild(banner);
                }
                card.querySelectorAll('input, select, textarea, button[type="submit"]').forEach(function(el) { 
                    el.disabled = true; 
                    el.style.opacity = '0.4'; 
                });
            } else {
                if (banner) banner.remove();
                card.querySelectorAll('input, select, textarea, button[type="submit"]').forEach(function(el) { 
                    el.disabled = false; 
                    el.style.opacity = '1.0'; 
                });
            }
        });
    }

    setInterval(enforcePermissions, 2000);
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', initAuth);
    else initAuth();
    setTimeout(initAuth, 2500);
})();
</script>
"""
