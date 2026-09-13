# ui.py - Master UI Assembler exporting DASHBOARD_HTML & get_form_vi_html
from ui_part1 import PART1
from ui_part3 import PART3
from ui_offline import OFFLINE_SCRIPT
from ui_part2 import PART2

# 1. Main Dashboard Complete HTML Export
DASHBOARD_HTML = PART1 + PART3 + OFFLINE_SCRIPT + PART2
HTML = DASHBOARD_HTML

# 2. Form-VI Statutory Printable Sheet
def get_form_vi_html(inspections, collieries):
    rows = ""
    for o in inspections:
        rows += f"""
        <tr>
          <td style="padding: 8px; border: 1px solid #cbd5e1;">{getattr(o, 'timestamp', '')}</td>
          <td style="padding: 8px; border: 1px solid #cbd5e1; font-weight: bold;">{getattr(o, 'mine_name', 'Gevra Sector B')}</td>
          <td style="padding: 8px; border: 1px solid #cbd5e1;">{getattr(o, 'officer_name', '')} ({getattr(o, 'officer_role', '')})</td>
          <td style="padding: 8px; border: 1px solid #cbd5e1; font-family: monospace;">{getattr(o, 'dgms_cert_no', '')}</td>
          <td style="padding: 8px; border: 1px solid #cbd5e1;">{getattr(o, 'category', '')}</td>
          <td style="padding: 8px; border: 1px solid #cbd5e1;">{getattr(o, 'notes', '')}</td>
          <td style="padding: 8px; border: 1px solid #cbd5e1; font-weight: bold; color: {'#dc2626' if getattr(o, 'severity', '') == 'Critical' else '#16a34a'};">{getattr(o, 'severity', '')}</td>
          <td style="padding: 8px; border: 1px solid #cbd5e1; font-family: monospace; font-size: 10px;">{str(getattr(o, 'sha256_hash', ''))[:18]}...</td>
        </tr>
        """
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
    .btn {{ background: #000; color: #fff; padding: 8px 16px; font-size: 12px; border: none; cursor: pointer; border-radius: 4px; }}
  </style>
</head>
<body>
  <div class="no-print" style="margin-bottom: 16px; display: flex; justify-content: space-between; align-items: center;">
    <span style="font-size: 12px; font-weight: bold; color: #475569;">OFFICIAL DGMS STATUTORY COMPLIANCE ARCHIVE</span>
    <button class="btn" onclick="window.print()">🖨️ Print / Save as PDF</button>
  </div>
  <div class="header-box">
    <h2 style="margin: 0; font-size: 16px; text-transform: uppercase;">Directorate General of Mines Safety (DGMS)</h2>
    <h3 style="margin: 4px 0; font-size: 14px;">FORM VI - STATUTORY REGISTER OF INSPECTIONS & RECORD OF DAILY FINDINGS</h3>
    <p style="margin: 2px 0; font-size: 11px;">[Under Coal Mines Regulations, 2017 - Regulation 27 & 153]</p>
  </div>
  <table>
    <thead>
      <tr>
        <th>Date & Time</th>
        <th>Colliery / Pit</th>
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
    <div><strong>Prepared By:</strong> Autonomous MinePulse Core</div>
    <div><strong>Countersigned:</strong> Agent / Colliery Manager</div>
  </div>
</body>
</html>"""
  
