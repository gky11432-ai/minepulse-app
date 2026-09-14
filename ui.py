# ui.py - Clean Modular Combiner with Isolated Map
from ui_part1 import PART1
from ui_map import PART_MAP
from ui_part3 import PART3
from ui_part2 import PART2

# Order: Layout -> Map -> Form -> JS Engine
DASHBOARD_HTML = PART1 + PART_MAP + PART3 + PART2
HTML = DASHBOARD_HTML

def get_form_vi_html(inspections=None, collieries=None, *args, **kwargs):
    rows = ""
    try:
        data = inspections or []
        for o in data:
            def val(obj, k, d=""):
                if isinstance(obj, dict):
                    return obj.get(k, d)
                return getattr(obj, k, d)

            ts = str(val(o, 'timestamp', ''))
            mine = str(val(o, 'mine_name', 'Gevra Sector B (SECL)'))
            officer = f"{val(o, 'officer_name', 'Officer')} ({val(o, 'officer_role', 'Overman')})"
            cert = str(val(o, 'dgms_cert_no', 'DGMS/CMR/2017'))
            cat = str(val(o, 'category', 'CMR 153'))
            notes = str(val(o, 'notes', ''))
            sev = str(val(o, 'severity', 'Normal'))
            h = str(val(o, 'sha256_hash', 'SEAL'))
            seal = (h[:18] + "...") if len(h) >= 18 else h

            color = "#dc2626" if sev.lower() == "critical" else "#16a34a"

            rows += f"""
            <tr>
              <td style="padding: 8px; border: 1px solid #cbd5e1;">{ts}</td>
              <td style="padding: 8px; border: 1px solid #cbd5e1; font-weight: bold;">{mine}</td>
              <td style="padding: 8px; border: 1px solid #cbd5e1;">{officer}</td>
              <td style="padding: 8px; border: 1px solid #cbd5e1;">{cert}</td>
              <td style="padding: 8px; border: 1px solid #cbd5e1;">{cat}</td>
              <td style="padding: 8px; border: 1px solid #cbd5e1;">{notes}</td>
              <td style="padding: 8px; border: 1px solid #cbd5e1; font-weight: bold; color: {color};">{sev}</td>
              <td style="padding: 8px; border: 1px solid #cbd5e1; font-family: monospace; font-size: 10px;">{seal}</td>
            </tr>
            """
    except Exception as e:
        rows = f'<tr><td colspan="8" style="padding: 12px; text-align: center; color: red;">Report generation error: {str(e)}</td></tr>'

    if not rows:
        rows = '<tr><td colspan="8" style="padding: 12px; text-align: center; border: 1px solid #cbd5e1; color: #64748b;">No statutory inspection records registered yet.</td></tr>'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>DGMS Form-VI Statutory Log Book</title>
  <style>
    @media print {{
      .no-print {{ display: none !important; }}
      body {{ font-size: 11px; }}
    }}
    body {{ font-family: 'Times New Roman', serif; padding: 24px; color: #000; background: #fff; }}
    table {{ width: 100%; border-collapse: collapse; margin-top: 14px; font-size: 11px; }}
    th {{ background: #f1f5f9; border: 1px solid #94a3b8; padding: 8px; text-align: left; }}
    .header-box {{ border-bottom: 2px solid #000; padding-bottom: 12px; text-align: center; }}
    .btn {{ background: #000; color: #fff; padding: 8px 16px; font-size: 12px; border: none; cursor: pointer; border-radius: 4px; font-weight: bold; }}
  </style>
</head>
<body>
  <div class="no-print" style="margin-bottom: 16px; display: flex; justify-content: space-between; align-items: center;">
    <span style="font-size: 12px; font-weight: bold; color: #475569;">OFFICIAL DGMS STATUTORY COMPLIANCE ARCHIVE</span>
    <button class="btn" onclick="window.print()">🖨️ Print / Save as PDF</button>
  </div>
  <div class="header-box">
    <h2 style="margin: 0; font-size: 16px; text-transform: uppercase;">Directorate General of Mines Safety (DGMS)</h2>
    <h3 style="margin: 4px 0; font-size: 14px;">FORM VI - STATUTORY REGISTER OF DAILY INSPECTIONS</h3>
    <p style="margin: 2px 0; font-size: 11px;">[Under Coal Mines Regulations, 2017 - Regulation 27 & 153]</p>
  </div>
  <table>
    <thead>
      <tr>
        <th>Timestamp</th>
        <th>Colliery Unit</th>
        <th>Statutory Officer</th>
        <th>DGMS Cert No.</th>
        <th>Regulation</th>
        <th>Observations & Findings</th>
        <th>Severity</th>
        <th>SHA-256 Digital Seal</th>
      </tr>
    </thead>
    <tbody>
      {rows}
    </tbody>
  </table>
  <div style="margin-top: 40px; display: flex; justify-content: space-between; font-size: 11px;">
    <div><strong>Verified By:</strong> Autonomous MinePulse Core</div>
    <div><strong>Countersigned:</strong> Agent / Colliery Manager</div>
  </div>
</body>
</html>"""
  
