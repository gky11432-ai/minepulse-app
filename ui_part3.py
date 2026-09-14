# ui_part3.py - Form UI Component with Proper Closing Tags

PART3 = """
    <!-- STATUTORY FORM VIEW -->
    <div id="vf" class="hidden">
      <div class="card" style="max-width: 650px; margin: 0 auto;">
        <div style="border-bottom: 1px solid #1e293b; padding-bottom: 8px; margin-bottom: 12px; display:flex; justify-content:space-between; align-items:center;">
          <div>
            <h2 style="font-size:14px; font-weight:bold; color:#fff;">DGMS Statutory Form-VI Inspection Log</h2>
            <p style="font-size:11px; color:#94a3b8;">Coal Mines Regulations (CMR 2017) Shift Log</p>
          </div>
          <span style="font-size:10px; color:#f59e0b; font-weight:bold;">DIGITAL SEAL</span>
        </div>

        <form onsubmit="save(event)">
          <div style="display:grid; grid-template-columns: 1fr 1fr; gap:10px;">
            <div>
              <label class="lbl">Colliery Unit</label>
              <select id="sm"></select>
            </div>
            <div>
              <label class="lbl">Statutory GPS Check</label>
              <input value="Inside Leasehold Zone" readonly style="color:#34d399; font-weight:bold;">
            </div>
          </div>

          <div style="display:grid; grid-template-columns: 1fr 1fr; gap:10px;">
            <div>
              <label class="lbl">Statutory Officer Name</label>
              <input id="soname" required value="Er. Gaurav Yadav">
            </div>
            <div>
              <label class="lbl">Statutory Capacity</label>
              <select id="sorole">
                <option value="Safety Officer (Overman)">Safety Officer (Overman / Dy. Mgr)</option>
                <option value="First Class Colliery Manager">First Class Colliery Manager</option>
                <option value="Ventilation Officer">Ventilation Officer (CMR 153)</option>
              </select>
            </div>
          </div>

          <div style="display:grid; grid-template-columns: 1fr 1fr; gap:10px;">
            <div>
              <label class="lbl">DGMS Certificate Number</label>
              <input id="socert" required value="DGMS/CMR/2017/0914" style="color:#f59e0b; font-family:monospace;">
            </div>
            <div>
              <label class="lbl">Severity Classification</label>
              <select id="ss">
                <option value="Normal">Normal - Statutory Compliant</option>
                <option value="Critical">Critical - Evacuation Breach</option>
              </select>
            </div>
          </div>

          <div>
            <label class="lbl">Statutory Regulation Domain</label>
            <select id="scat">
              <option value="CMR 153: Face Ventilation & Methane Log">CMR 153: Face Ventilation & Methane Log</option>
              <option value="CMR 106: Highwall Bench Stability">CMR 106: Highwall Bench Stability</option>
              <option value="CMR 169: Deep Hole Blasting Vibration">CMR 169: Deep Hole Blasting Vibration</option>
            </select>
          </div>

          <div>
            <label class="lbl">Statutory Observations & Mitigation Orders</label>
            <textarea id="sn" rows="3" required placeholder="Log gas concentration, bench cracks, ventilation velocity..."></textarea>
          </div>

          <button type="submit" style="width:100%; background:#f59e0b; color:#000; font-weight:bold; padding:12px; border:none; border-radius:8px; cursor:pointer; font-size:13px;">
            Sign, Seal & Save Inspection
          </button>
        </form>
      </div>
    </div>
  </div>
"""
