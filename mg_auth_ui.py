# mg_auth_ui.py - Full-Screen Gatekeeper & Header User Identity HUD (< 170 Lines)

AUTH_UI_MARKUP = """
<style>
  #mineguard-header-auth-bar {
      background: #020617;
      border-bottom: 1px solid #1e293b;
      padding: 4px 12px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-family: system-ui, sans-serif;
      font-size: 10px;
  }
  .role-badge-pill {
      padding: 2px 8px;
      border-radius: 12px;
      font-weight: 800;
      font-size: 9px;
      letter-spacing: 0.5px;
      text-transform: uppercase;
  }
  .role-worker { background: #1e3a5f; color: #38bdf8; border: 1px solid #0284c7; }
  .role-officer { background: #064e3b; color: #34d399; border: 1px solid #059669; }

  /* Gatekeeper Fullscreen Overlay */
  #mineguard-gatekeeper-modal {
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      background: rgba(2, 6, 23, 0.98);
      z-index: 999999999;
      display: flex;
      justify-content: center;
      align-items: center;
      padding: 16px;
      box-sizing: border-box;
      font-family: system-ui, sans-serif;
  }
  .auth-card-box {
      background: #0f172a;
      border: 2px solid #38bdf8;
      border-radius: 16px;
      width: 100%;
      max-width: 400px;
      padding: 24px 20px;
      box-shadow: 0 20px 50px rgba(0, 0, 0, 0.9);
      text-align: center;
  }
  .auth-toggle-tab {
      flex: 1;
      padding: 9px;
      font-size: 11px;
      font-weight: bold;
      border: 1px solid #334155;
      background: #020617;
      color: #94a3b8;
      border-radius: 8px;
      cursor: pointer;
  }
  .auth-toggle-tab.active {
      background: #0284c7;
      color: #fff;
      border-color: #38bdf8;
  }
</style>

<!-- Top Identity & Role Status Strip -->
<div id="mineguard-header-auth-bar">
    <div style="display:flex; align-items:center; gap:8px;">
        <span style="color:#64748b;">👤 User:</span>
        <span id="auth-display-name" style="color:#f8fafc; font-weight:bold;">Loading...</span>
        <span id="auth-display-role" class="role-badge-pill role-worker">WORKER</span>
    </div>
    <button type="button" onclick="openGatekeeperLogin()" style="background:#1e293b; border:1px solid #334155; color:#38bdf8; font-size:10px; font-weight:bold; padding:3px 8px; border-radius:6px; cursor:pointer;">
        🔄 Switch Role
    </button>
</div>

<!-- Full-Screen Statutory Gatekeeper Login Screen -->
<div id="mineguard-gatekeeper-modal" style="display:none;">
    <div class="auth-card-box">
        <div style="font-size:36px; margin-bottom:6px;">⛑️</div>
        <div style="font-size:17px; font-weight:900; color:#38bdf8; letter-spacing:0.5px;">MINEGUARD AUTHENTICATION</div>
        <div style="font-size:10px; color:#94a3b8; margin-bottom:16px;">Mines Act 1952 & DGMS Statutory Role Gatekeeper</div>

        <div style="display:flex; gap:8px; margin-bottom:16px;">
            <button type="button" id="tab-btn-worker" class="auth-toggle-tab active" onclick="switchGatekeeperRole('WORKER')">
                👷 Worker Mode (Read-Only)
            </button>
            <button type="button" id="tab-btn-officer" class="auth-toggle-tab" onclick="switchGatekeeperRole('OFFICER')">
                🛡️ Officer Mode (Sign/Certify)
            </button>
        </div>

        <!-- Worker Login Fields -->
        <div id="auth-box-worker">
            <div style="text-align:left; margin-bottom:12px;">
                <label style="font-size:11px; color:#94a3b8;">Worker Name / Token ID</label>
                <input type="text" id="gk-worker-token" placeholder="e.g. TK-402 (Ramesh Mahto)" value="Ramesh Mahto (TK-402)" style="width:100%; background:#020617; border:1px solid #334155; color:#fff; padding:9px; border-radius:6px; font-size:11px; box-sizing:border-box; margin-top:4px;">
            </div>
            <button type="button" onclick="loginAsWorker()" style="width:100%; background:#0284c7; color:#fff; font-weight:bold; border:none; padding:11px; border-radius:8px; font-size:12px; cursor:pointer;">
                Enter Dashboard as Worker
            </button>
        </div>

        <!-- Officer Login Fields (PIN Protected) -->
        <div id="auth-box-officer" style="display:none;">
            <div style="text-align:left; margin-bottom:10px;">
                <label style="font-size:11px; color:#94a3b8;">Statutory Officer Designation</label>
                <select id="gk-officer-desig" style="width:100%; background:#020617; border:1px solid #334155; color:#fff; padding:9px; border-radius:6px; font-size:11px; box-sizing:border-box; margin-top:4px;">
                    <option value="Mining Sirdar">Mining Sirdar (CMR 48 Certified)</option>
                    <option value="Overman">Overman (CMR 47 Certified)</option>
                    <option value="Ventilation Officer">Ventilation Officer (Reg 153)</option>
                    <option value="Colliery Safety Officer">Colliery Safety Officer</option>
                    <option value="Colliery Manager">First/Second Class Colliery Manager</option>
                </select>
            </div>
            <div style="text-align:left; margin-bottom:14px;">
                <label style="font-size:11px; color:#94a3b8;">Officer Security PIN (Default: 9999)</label>
                <input type="password" id="gk-officer-pin" maxlength="6" placeholder="Enter 4-digit PIN" value="9999" style="width:100%; background:#020617; border:1px solid #334155; color:#fff; padding:9px; border-radius:6px; font-size:12px; box-sizing:border-box; margin-top:4px; letter-spacing:3px;">
            </div>
            <button type="button" onclick="loginAsOfficer()" style="width:100%; background:#16a34a; color:#fff; font-weight:bold; border:none; padding:11px; border-radius:8px; font-size:12px; cursor:pointer;">
                Verify PIN & Certify Rights
            </button>
        </div>

        <div style="margin-top:14px; font-size:9.5px; color:#64748b;">
            Offline DGMS Compliant • Digital Signature Token Active
        </div>
    </div>
</div>
"""
