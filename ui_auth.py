# ui_auth.py - Standalone DGMS Role-Based Access Control, Barcode/QR Badge Scanner & Form-B Attendance Engine

AUTH_MODULE = """
<script>
(function() {
    var CURRENT_USER = null;
    var videoStream = null;
    var scanAnimationId = null;
    var barcodeDetectorInstance = null;

    function initAuth() {
        var savedUser = localStorage.getItem('mineguard_active_user');
        if (savedUser) {
            try { CURRENT_USER = JSON.parse(savedUser); } catch(e) { CURRENT_USER = null; }
        }
        if (!CURRENT_USER) {
            CURRENT_USER = {
                name: 'Worker (Self-Service)',
                role: 'WORKER',
                token: 'GUEST-PIT',
                designation: 'General Underground Miner'
            };
        }
        injectAuthHeaderUI();
        injectAttendanceCardUI();
        injectScannerModalUI();
        enforceRolePermissions();
    }

    function injectAuthHeaderUI() {
        if (document.getElementById('mineguard-auth-bar')) {
            updateAuthHeaderDisplay();
            return;
        }

        var bar = document.createElement('div');
        bar.id = 'mineguard-auth-bar';
        bar.style.cssText = 'background:#020617; border-bottom:1px solid #334155; padding:8px 14px; display:flex; justify-content:space-between; align-items:center; font-family:system-ui, sans-serif; position:sticky; top:0; z-index:9999; box-shadow:0 2px 4px rgba(0,0,0,0.5);';

        bar.innerHTML = `
            <div style="display:flex; align-items:center; gap:8px;">
                <span id="auth-role-icon" style="font-size:16px;">👷</span>
                <div>
                    <div style="display:flex; align-items:center; gap:6px;">
                        <span id="auth-user-name" style="font-size:12px; font-weight:bold; color:#f8fafc;">Worker Mode</span>
                        <span id="auth-role-tag" style="background:#334155; color:#cbd5e1; font-size:9px; font-weight:bold; padding:2px 6px; border-radius:4px;">WORKER</span>
                    </div>
                    <div id="auth-user-sub" style="font-size:9px; color:#64748b;">Token: GUEST-PIT • Read-Only Statutory Rights</div>
                </div>
            </div>

            <div style="display:flex; gap:6px;">
                <button type="button" onclick="openLoginModal()" id="btn-auth-switch" style="background:#0284c7; color:#fff; font-weight:bold; border:none; padding:5px 10px; border-radius:4px; font-size:10px; cursor:pointer;">
                    🔑 Switch / Officer Login
                </button>
                <button type="button" onclick="logoutUser()" id="btn-auth-logout" style="background:#334155; color:#cbd5e1; border:none; padding:5px 8px; border-radius:4px; font-size:10px; cursor:pointer; display:none;">
                    🚪 Logout
                </button>
            </div>
        `;

        document.body.insertBefore(bar, document.body.firstChild);
        injectLoginModal();
        updateAuthHeaderDisplay();
    }

    function injectLoginModal() {
        if (document.getElementById('mineguard-login-modal')) return;

        var modal = document.createElement('div');
        modal.id = 'mineguard-login-modal';
        modal.style.cssText = 'display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.85); z-index:10000; justify-content:center; align-items:center; font-family:system-ui, sans-serif;';

        modal.innerHTML = `
            <div style="background:#0f172a; border:1px solid #334155; border-radius:10px; padding:20px; width:90%; max-width:380px; color:#fff; box-shadow:0 10px 25px rgba(0,0,0,0.8);">
                <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #1e293b; padding-bottom:10px; margin-bottom:14px;">
                    <div style="font-size:14px; font-weight:bold; color:#38bdf8;">🔐 Statutory Role Authentication</div>
                    <button type="button" onclick="closeLoginModal()" style="background:transparent; border:none; color:#94a3b8; font-size:16px; cursor:pointer;">✕</button>
                </div>

                <form onsubmit="handleUserLogin(event)">
                    <div style="margin-bottom:10px;">
                        <label style="font-size:11px; color:#94a3b8;">Select Identity Role</label>
                        <select id="login-role-select" onchange="toggleLoginFormFields()" style="width:100%; background:#020617; border:1px solid #334155; color:#38bdf8; font-weight:bold; padding:8px; border-radius:6px; font-size:11px; margin-top:4px;">
                            <option value="WORKER">👷 Shramik / Underground Miner</option>
                            <option value="OFFICER">👮 Mining Sirdar / Overman (Statutory)</option>
                            <option value="MANAGER">🎖️ Safety Officer / Colliery Manager</option>
                        </select>
                    </div>

                    <div style="margin-bottom:10px;">
                        <label style="font-size:11px; color:#94a3b8;">Officer / Miner Full Name</label>
                        <input type="text" id="login-name" required placeholder="e.g. Ramesh Kumar / R.N. Sharma" style="width:100%; background:#020617; border:1px solid #334155; color:#fff; padding:8px; border-radius:6px; font-size:11px; margin-top:4px; box-sizing:border-box;">
                    </div>

                    <div style="margin-bottom:10px;">
                        <label style="font-size:11px; color:#94a3b8;" id="login-token-label">Token / Gate-Pass ID</label>
                        <input type="text" id="login-token-id" required placeholder="e.g. TK-402 or Cert #7821" style="width:100%; background:#020617; border:1px solid #334155; color:#fff; padding:8px; border-radius:6px; font-size:11px; margin-top:4px; box-sizing:border-box;">
                    </div>

                    <div id="login-pin-container" style="margin-bottom:14px; display:none;">
                        <label style="font-size:11px; color:#f59e0b;">Statutory Authorization PIN / Passcode</label>
                        <input type="password" id="login-pin" placeholder="Enter 4-digit PIN (Default: 9999)" style="width:100%; background:#020617; border:1px solid #f59e0b; color:#fff; padding:8px; border-radius:6px; font-size:11px; margin-top:4px; box-sizing:border-box;">
                        <div style="font-size:9px; color:#94a3b8; margin-top:2px;">* Default Officer/Manager Authorization PIN is <b>9999</b></div>
                    </div>

                    <button type="submit" style="width:100%; background:#0284c7; color:#fff; font-weight:bold; border:none; padding:10px; border-radius:6px; font-size:12px; cursor:pointer;">
                        Authorize Session & Unlock Tools
                    </button>
                </form>
            </div>
        `;
        document.body.appendChild(modal);
    }

    window.openLoginModal = function() {
        var m = document.getElementById('mineguard-login-modal');
        if (m) {
            m.style.display = 'flex';
            toggleLoginFormFields();
        }
    };

    window.closeLoginModal = function() {
        var m = document.getElementById('mineguard-login-modal');
        if (m) m.style.display = 'none';
    };

    window.toggleLoginFormFields = function() {
        var role = document.getElementById('login-role-select').value;
        var pinBox = document.getElementById('login-pin-container');
        var pinInput = document.getElementById('login-pin');
        var tokenLabel = document.getElementById('login-token-label');

        if (role === 'WORKER') {
            if (pinBox) pinBox.style.display = 'none';
            if (pinInput) pinInput.required = false;
            if (tokenLabel) tokenLabel.innerText = 'Miner Token Number (e.g. TK-402)';
        } else {
            if (pinBox) pinBox.style.display = 'block';
            if (pinInput) pinInput.required = true;
            if (tokenLabel) tokenLabel.innerText = 'Statutory Certificate / Reg No.';
        }
    };

    window.handleUserLogin = function(e) {
        if (e) e.preventDefault();
        var role = document.getElementById('login-role-select').value;
        var name = document.getElementById('login-name').value.trim();
        var token = document.getElementById('login-token-id').value.trim();
        var pin = document.getElementById('login-pin').value;

        if (role !== 'WORKER') {
            if (pin !== '9999' && pin !== 'MineGuard@2026') {
                alert('⛔ AUTHORIZATION DENIED: Incorrect Statutory Security PIN. Default PIN is 9999.');
                return;
            }
        }

        var desig = (role === 'MANAGER') ? 'Colliery Manager / Safety Head' : ((role === 'OFFICER') ? 'Certified Overman / Sirdar' : 'Underground Coal Miner');

        CURRENT_USER = {
            name: name,
            role: role,
            token: token,
            designation: desig,
            loginTime: new Date().toLocaleTimeString()
        };

        localStorage.setItem('mineguard_active_user', JSON.stringify(CURRENT_USER));
        closeLoginModal();
        updateAuthHeaderDisplay();
        enforceRolePermissions();
        alert('✅ Welcome, ' + name + ' (' + role + '). Statutory access levels granted.');
    };

    window.logoutUser = function() {
        CURRENT_USER = {
            name: 'Worker (Self-Service)',
            role: 'WORKER',
            token: 'GUEST-PIT',
            designation: 'General Underground Miner'
        };
        localStorage.removeItem('mineguard_active_user');
        updateAuthHeaderDisplay();
        enforceRolePermissions();
        alert('🚪 Session ended. System locked to Worker Self-Service mode.');
    };

    function updateAuthHeaderDisplay() {
        var nameEl = document.getElementById('auth-user-name');
        var tagEl = document.getElementById('auth-role-tag');
        var subEl = document.getElementById('auth-user-sub');
        var iconEl = document.getElementById('auth-role-icon');
        var logoutBtn = document.getElementById('btn-auth-logout');

        if (!nameEl) return;

        nameEl.innerText = CURRENT_USER.name;
        tagEl.innerText = CURRENT_USER.role;
        subEl.innerText = CURRENT_USER.designation + ' • ID: ' + CURRENT_USER.token;

        if (CURRENT_USER.role === 'MANAGER') {
            iconEl.innerText = '🎖️';
            tagEl.style.background = '#701a75';
            tagEl.style.color = '#f5d0fe';
            if (logoutBtn) logoutBtn.style.display = 'block';
        } else if (CURRENT_USER.role === 'OFFICER') {
            iconEl.innerText = '👮';
            tagEl.style.background = '#1e3a5f';
            tagEl.style.color = '#38bdf8';
            if (logoutBtn) logoutBtn.style.display = 'block';
        } else {
            iconEl.innerText = '👷';
            tagEl.style.background = '#334155';
            tagEl.style.color = '#cbd5e1';
            if (logoutBtn) logoutBtn.style.display = 'none';
        }
    }

    function injectAttendanceCardUI() {
        if (document.getElementById('statutory-attendance-card')) return;

        var container = document.querySelector('.grid-container') || document.body;

        var card = document.createElement('div');
        card.id = 'statutory-attendance-card';
        card.style.cssText = 'background:#0f172a; border:1px solid #334155; border-radius:10px; padding:16px; margin:14px 0; color:#f8fafc; font-family:system-ui, sans-serif; box-shadow:0 4px 6px -1px rgba(0,0,0,0.5);';

        card.innerHTML = `
            <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #1e293b; padding-bottom:10px; margin-bottom:12px;">
                <div style="display:flex; align-items:center; gap:8px;">
                    <span style="font-size:18px;">⏱️</span>
                    <div>
                        <div style="font-size:13px; font-weight:bold; color:#38bdf8;">WORKER DIGITAL ATTENDANCE (FORM B REGISTER)</div>
                        <div style="font-size:10px; color:#94a3b8;">Mines Act 1952 Sec 48 & CMR 48 - Offline QR/Barcode Badge Attendance</div>
                    </div>
                </div>
                <div style="display:flex; gap:6px;">
                    <button type="button" onclick="openBadgeScanner()" style="background:#0284c7; color:#fff; font-weight:bold; border:none; padding:4px 10px; border-radius:12px; font-size:11px; cursor:pointer; display:flex; align-items:center; gap:4px; box-shadow:0 2px 4px rgba(0,0,0,0.3);">
                        📷 Scan Badge
                    </button>
                    <div id="attendance-status-badge" style="background:#14532d; color:#4ade80; border:1px solid #22c55e; font-size:10px; padding:3px 8px; border-radius:12px; font-weight:bold;">
                        READY
                    </div>
                </div>
            </div>

            <!-- Self-Attendance Punch Form -->
            <form id="worker-punch-form" onsubmit="recordSelfAttendance(event)">
                <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); gap:10px; margin-bottom:10px;">
                    <div>
                        <label style="font-size:11px; color:#94a3b8;">Punch Type (CMR In/Out)</label>
                        <select id="att-punch-type" style="width:100%; background:#020617; border:1px solid #334155; color:#38bdf8; font-weight:bold; padding:8px; border-radius:6px; font-size:11px; margin-top:4px;">
                            <option value="IN">🟢 PIT ENTRY (Shaft / Incline In)</option>
                            <option value="OUT">🔴 PIT EXIT (Shift Completed Out)</option>
                        </select>
                    </div>
                    <div>
                        <div style="display:flex; justify-content:space-between;">
                            <label style="font-size:11px; color:#94a3b8;">Miner Name</label>
                            <span id="badge-scanned-status" style="font-size:10px; color:#38bdf8;"></span>
                        </div>
                        <input type="text" id="att-miner-name" required placeholder="Full Name" style="width:100%; background:#020617; border:1px solid #334155; color:#fff; padding:8px; border-radius:6px; font-size:11px; margin-top:4px; box-sizing:border-box;">
                    </div>
                    <div>
                        <label style="font-size:11px; color:#94a3b8;">Token / Biometric Badge ID</label>
                        <div style="display:flex; gap:4px; margin-top:4px;">
                            <input type="text" id="att-token-no" required placeholder="e.g. TK-402" style="flex:1; background:#020617; border:1px solid #334155; color:#fff; padding:8px; border-radius:6px; font-size:11px; box-sizing:border-box;">
                            <button type="button" onclick="openBadgeScanner()" title="Scan Camera QR/Barcode" style="background:#1e293b; border:1px solid #334155; color:#38bdf8; padding:0 10px; border-radius:6px; cursor:pointer; font-size:14px;">
                                📷
                            </button>
                        </div>
                    </div>
                </div>

                <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap:8px; margin-bottom:12px;">
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Assigned Shift</span>
                        <select id="att-shift" style="width:100%; background:transparent; border:none; color:#cbd5e1; font-size:11px; margin-top:2px;">
                            <option value="Shift 1 (08:00 - 16:00)">Shift 1 (08:00 - 16:00)</option>
                            <option value="Shift 2 (16:00 - 00:00)">Shift 2 (16:00 - 00:00)</option>
                            <option value="Shift 3 (00:00 - 08:00)">Shift 3 (00:00 - 08:00)</option>
                            <option value="General Shift">General Shift</option>
                        </select>
                    </div>
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Working Seam / District</span>
                        <input type="text" id="att-district" required placeholder="e.g. 2nd Dip Face" style="width:100%; background:transparent; border:none; color:#cbd5e1; font-size:11px; margin-top:2px;">
                    </div>
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Trade / Designation</span>
                        <select id="att-trade" style="width:100%; background:transparent; border:none; color:#cbd5e1; font-size:11px; margin-top:2px;">
                            <option value="Coal Loader / Face Worker">Coal Loader / Face Worker</option>
                            <option value="Drill Operator">Drill Operator</option>
                            <option value="SDL / LHD Operator">SDL / LHD Operator</option>
                            <option value="Support Mason / Timberman">Support Mason / Timberman</option>
                            <option value="Trammer / Haulage Crew">Trammer / Haulage Crew</option>
                            <option value="Underground Electrician">Underground Electrician</option>
                        </select>
                    </div>
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Fit for Shift (Self-Check)</span>
                        <select id="att-fitness" style="width:100%; background:transparent; border:none; color:#4ade80; font-weight:bold; font-size:11px; margin-top:2px;">
                            <option value="Physically Fit & Alert">Fit & Alert (No Illness)</option>
                            <option value="Fatigued / Reporting Sick">Reporting Sick / Unfit</option>
                        </select>
                    </div>
                </div>

                <button type="submit" id="btn-submit-punch" style="width:100%; background:#16a34a; color:#fff; font-weight:bold; border:none; padding:10px; border-radius:6px; font-size:12px; cursor:pointer;">
                    ✅ Punch Form-B Digital Attendance
                </button>
            </form>

            <!-- Live Shift Attendance Ledger -->
            <div style="margin-top:14px; border-top:1px solid #1e293b; padding-top:10px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                    <div style="font-size:11px; font-weight:bold; color:#cbd5e1;">Today's Digital Form-B Attendance Roll</div>
                    <span id="att-count-badge" style="background:#334155; color:#cbd5e1; font-size:9px; padding:2px 6px; border-radius:8px;">0 Punches</span>
                </div>
                <div id="att-history-list" style="max-height:120px; overflow-y:auto; font-size:10px; color:#94a3b8;">
                    No worker punches recorded yet for this shift.
                </div>
            </div>
        `;

        container.insertBefore(card, container.firstChild);
        renderAttendanceLogs();
    }

    // Modal for Camera QR & Barcode Badge Scanning
    function injectScannerModalUI() {
        if (document.getElementById('mineguard-scanner-modal')) return;

        var modal = document.createElement('div');
        modal.id = 'mineguard-scanner-modal';
        modal.style.cssText = 'display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.92); z-index:11000; justify-content:center; align-
