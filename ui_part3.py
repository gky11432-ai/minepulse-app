# ui_part3.py - Full Detailed Statutory Officer Form & DGMS Form-VI Register Generator

FORM_UI = """
    <!-- Full-Width Detailed Statutory Form -->
    <div id="vf" class="hidden max-w-4xl mx-auto bg-slate-900 border border-slate-800 rounded-2xl p-6 sm:p-8 space-y-6 shadow-2xl">
      <div class="border-b border-slate-800 pb-4 flex justify-between items-center">
        <div>
          <h2 class="font-bold text-lg text-white">DGMS Statutory Shift Log & Inspection Protocol</h2>
          <p class="text-xs text-slate-400 mt-0.5">Under Coal Mines Regulations (CMR 2017) & Mines Act 1952 statutory compliance mandate</p>
        </div>
        <span class="text-xs bg-amber-500/10 text-amber-400 border border-amber-500/30 px-3 py-1 rounded-full font-mono">DSC Cryptographic Signing Active</span>
      </div>

      <form onsubmit="save(event)" class="space-y-4 text-xs">
        <!-- Officer Credential Section -->
        <div class="bg-slate-950/60 p-4 rounded-xl border border-slate-800 space-y-3">
          <h3 class="font-semibold text-slate-300 text-xs uppercase tracking-wider">Statutory Authority Identification</h3>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
            <div>
              <label class="text-slate-400 block mb-1 font-medium">Competent Inspecting Officer Name</label>
              <input id="soname" required class="w-full bg-slate-800 p-2.5 rounded-lg text-white border border-slate-700 focus:border-amber-500 outline-none" value="Er. Gaurav Yadav">
            </div>
            <div>
              <label class="text-slate-400 block mb-1 font-medium">Statutory Designation / Capacity</label>
              <select id="sorole-select" onchange="onRoleFormChange()" class="w-full bg-slate-800 p-2.5 rounded-lg text-amber-400 font-semibold border border-slate-700 focus:border-amber-500 outline-none">
                <option value="overman">Safety Officer (Overman / Dy. Manager)</option>
                <option value="manager">First Class Colliery Manager (Agent / In-Charge)</option>
                <option value="ventilation">Ventilation Officer (CMR 153 Gas In-Charge)</option>
                <option value="surveyor">Statutory Mine Surveyor (CMR 106 Geodetics)</option>
                <option value="weighbridge">Weighbridge Coal Dispatch Inspector</option>
              </select>
              <input type="hidden" id="sorole" value="Safety Officer (Overman)">
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-3 pt-1">
            <div>
              <label class="text-slate-400 block mb-1 font-medium">DGMS Certificate of Competency / License No.</label>
              <input id="socert" readonly class="w-full bg-slate-900 p-2.5 rounded-lg text-slate-300 font-mono border border-slate-800" value="DGMS/CMR/2017/OM-8492">
            </div>
            <div>
              <label class="text-slate-400 block mb-1 font-medium">Shift & Working Time Window</label>
              <select id="sshift" class="w-full bg-slate-800 p-2.5 rounded-lg text-white border border-slate-700 outline-none">
                <option value="Shift-A">Shift-A (06:00 - 14:00 hrs IST)</option>
                <option value="Shift-B">Shift-B (14:00 - 22:00 hrs IST)</option>
                <option value="Shift-C">Shift-C (22:00 - 06:00 hrs IST - Night Blast & Drill)</option>
                <option value="General">General Administrative Shift</option>
              </select>
            </div>
          </div>
        </div>

        <!-- Colliery & Spatial Section -->
        <div class="bg-slate-950/60 p-4 rounded-xl border border-slate-800 space-y-3">
          <h3 class="font-semibold text-slate-300 text-xs uppercase tracking-wider">Colliery & Spatial Verification</h3>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
            <div>
              <label class="text-slate-400 block mb-1 font-medium">Target Colliery / Mine Leasehold</label>
              <select id="sm" class="w-full bg-slate-800 p-2.5 rounded-lg text-white border border-slate-700 outline-none"></select>
            </div>
            <div>
              <label class="text-slate-400 block mb-1 font-medium">Seam / Working Section / District</label>
              <input id="sseam" class="w-full bg-slate-800 p-2.5 rounded-lg text-white border border-slate-700 outline-none" placeholder="e.g. Seam IV Top Bench / West District" value="Sector B - Bench 03 (Coal Face)">
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-3 pt-1">
            <div>
              <label class="text-slate-400 block mb-1 font-medium">Statutory Boundary & GPS Integrity</label>
              <select id="sgps" class="w-full bg-slate-800 p-2.5 rounded-lg text-emerald-400 font-semibold border border-slate-700 outline-none">
                <option value="inside">Compliant: Inside Statutory Leasehold Polygon (Lat 22.3541, Lng 82.6821)</option>
                <option value="outside">BREACH: Outside Approved Boundary (Geofence Breach Trigger)</option>
              </select>
            </div>
            <div>
              <label class="text-slate-400 block mb-1 font-medium">Risk & Incident Classification</label>
              <select id="ss" class="w-full bg-slate-800 p-2.5 rounded-lg text-white border border-slate-700 outline-none font-semibold">
                <option value="Normal">Routine Observation (Statutory Compliant)</option>
                <option value="Critical">Critical Breach (Immediate Stop-Work Order + Audio Siren)</option>
              </select>
            </div>
          </div>
        </div>

        <!-- Regulation & Observation Notes -->
        <div class="space-y-3">
          <div>
            <label class="text-slate-400 block mb-1 font-medium">Statutory Regulation Domain</label>
            <select id="scat" class="w-full bg-slate-800 p-2.5 rounded-lg text-white border border-slate-700 outline-none">
              <option>CMR 153: Underground & Pit Face Ventilation, Methane (CH4) & Toxic Gas Monitoring</option>
              <option>CMR 106: Opencast Bench Stability, Highwall Slope Angle & Haul Road Berms</option>
              <option>CMR 169: Daily Deep Hole Blasting, Shotfiring & Explosives Usage Audit</option>
              <option>CMR 140: Machinery Ergonomics, Heavy Earth Moving Machinery (HEMM) Safety Inspection</option>
              <option>CAAQMS: Environmental Ambient Dust, PM2.5, PM10 & Water Spray Protocol</option>
            </select>
          </div>

          <div>
            <label class="text-slate-400 block mb-1 font-medium">Detailed Statutory Finding & Corrective Directive</label>
            <textarea id="sn" required rows="3" class="w-full bg-slate-800 p-3 rounded-lg text-white border border-slate-700 focus:border-amber-500 outline-none" placeholder="Provide precise measurement, seam location, observed hazard, and statutory direction issued to the colliery supervisor..."></textarea>
          </div>
        </div>

        <!-- Action Button -->
        <button type="submit" class="w-full bg-amber-500 hover:bg-amber-400 text-black font-bold p-3.5 rounded-xl shadow-lg transition flex items-center justify-center space-x-2 text-sm">
          <span>🔏</span>
          <span>Digitally Sign & Commit to Cryptographic Audit Ledger (SHA-256)</span>
        </button>
      </form>
    </div>
  </main>

  <script>
    const DETAILED_ROLES = {
      'overman': { role: 'Safety Officer (Overman / Dy. Manager)', cert: 'DGMS/CMR/2017/OM-8492' },
      'manager': { role: 'First Class Colliery Manager (Agent)', cert: 'DGMS/CMR/2017/FCM-1094' },
      'ventilation': { role: 'Ventilation Officer (Gas In-Charge)', cert: 'DGMS/CMR/2017/VO-4419' },
      'surveyor': { role: 'Statutory Mine Surveyor', cert: 'DGMS/CMR/2017/SRV-2103' },
      'weighbridge': { role: 'Weighbridge Dispatch Inspector', cert: 'DGMS/CMR/2017/WBO-3312' }
    };

    function onRoleFormChange() {
      const sel = document.getElementById('sorole-select').value;
      const data = DETAILED_ROLES[sel];
      if (data) {
        document.getElementById('sorole').value = data.role;
        document.getElementById('socert').value = data.cert;
      }
    }
  </script>
"""

def get_form_vi_html(rows):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>DGMS Form-VI Statutory Inspection Register</title>
    <style>
        body {{ font-family: 'Times New Roman', serif; padding: 25px; color: #111; line-height: 1.4; }}
        .header {{ text-align: center; border-bottom: 2px solid #000; padding-bottom: 12px; margin-bottom: 18px; }}
        table {{ width: 100%; border-collapse: collapse; text-align: left; font-size: 11px; margin-top: 10px; }}
        th {{ border: 1px solid #333; padding: 8px; background: #e5e7eb; font-weight: bold; }}
        td {{ border: 1px solid #666; padding: 8px; vertical-align: top; }}
        .footer {{ margin-top: 40px; display: flex; justify-content: space-between; font-size: 11px; }}
        @media print {{ button {{ display: none; }} }}
    </style>
</head>
<body>
    <div class="header">
        <h2 style="margin: 0; font-size: 18px; letter-spacing: 0.5px;">DIRECTORATE GENERAL OF MINES SAFETY (DGMS)</h2>
        <h3 style="margin: 5px 0; font-size: 14px;">FORM-VI STATUTORY LOGBOOK & BREACH REGISTER</h3>
        <p style="margin: 0; font-size: 11px; color: #444;">Maintained in accordance with Section 23 of Mines Act 1952 & Regulation 153/106/169 of CMR 2017</p>
    </div>
    <div style="margin-bottom: 12px; text-align: right;">
        <button onclick="window.print()" style="padding: 6px 14px; background: #1e293b; color: #f8fafc; border: 1px solid #475569; border-radius: 4px; cursor: pointer; font-size: 12px;">Print Official Register / Export PDF</button>
    </div>
    <table>
        <thead>
            <tr>
                <th style="width: 13%;">Timestamp (UTC)</th>
                <th style="width: 14%;">Colliery / Unit</th>
                <th style="width: 18%;">Inspecting Officer & DGMS Lic.</th>
                <th style="width: 15%;">CMR Category</th>
                <th>Observation & Directives</th>
                <th style="width: 10%;">Class</th>
                <th style="width: 15%;">SHA-256 DSC Seal</th>
            </tr>
        </thead>
        <tbody>
            {rows}
        </tbody>
    </table>
    <div class="footer">
        <div>
            <p>Generated by: <strong>MinePulse Statutory AI Core</strong></p>
            <p>Cryptographic Tamper-Proof Audit Record</p>
        </div>
        <div style="text-align: right;">
            <p>_____________________________________________</p>
            <p><strong>Inspecting Authority / Manager Signature</strong></p>
            <p>Statutory Competency Certified under CMR 2017</p>
        </div>
    </div>
</body>
</html>"""
  
