# mg_reports_ui.py - DGMS Statutory Form 6 Printable Layout (< 150 Lines)

REPORTS_UI_MARKUP = """
<style>
  @media print {
      body * { visibility: hidden !important; }
      #mineguard-form6-modal, #form6-printable-document, #form6-printable-document * {
          visibility: visible !important;
      }
      #mineguard-form6-modal {
          position: absolute !important;
          left: 0 !important;
          top: 0 !important;
          width: 100% !important;
          height: auto !important;
          background: #ffffff !important;
          padding: 0 !important;
          margin: 0 !important;
      }
      .no-print-bar { display: none !important; }
  }
  #mineguard-form6-modal {
      display: none;
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      background: rgba(2, 6, 23, 0.96);
      z-index: 9999999;
      justify-content: center;
      align-items: center;
      padding: 10px;
      box-sizing: border-box;
      font-family: system-ui, sans-serif;
  }
  .form6-sheet-container {
      background: #0f172a;
      border: 2px solid #38bdf8;
      border-radius: 12px;
      width: 100%;
      max-width: 650px;
      max-height: 94vh;
      display: flex;
      flex-direction: column;
      box-shadow: 0 25px 50px rgba(0, 0, 0, 0.9);
      overflow: hidden;
  }
  .form6-header-bar {
      background: #1e293b;
      padding: 10px 14px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid #334155;
  }
  #form6-printable-document {
      flex: 1;
      overflow-y: auto;
      padding: 14px;
      background: #ffffff;
      color: #0f172a;
      font-family: 'Times New Roman', Times, serif;
      font-size: 11px;
      line-height: 1.4;
  }
  .form6-action-bar {
      background: #020617;
      padding: 10px 12px;
      display: flex;
      gap: 6px;
      flex-wrap: wrap;
      border-top: 1px solid #1e293b;
  }
</style>

<div id="mineguard-form6-modal">
    <div class="form6-sheet-container">
        <div class="form6-header-bar no-print-bar">
            <div style="display:flex; align-items:center; gap:8px;">
                <span style="font-size:18px;">📄</span>
                <div>
                    <div style="font-size:13px; font-weight:bold; color:#38bdf8;">DGMS STATUTORY FORM VI (FORM 6)</div>
                    <div style="font-size:9px; color:#94a3b8;">CMR 2017 Reg 47/48 Daily Shift Inspection & Audit</div>
                </div>
            </div>
            <button type="button" onclick="closeForm6Modal()" style="background:#334155; border:none; color:#f8fafc; width:28px; height:28px; border-radius:50%; font-size:14px; cursor:pointer;">✕</button>
        </div>

        <div id="form6-printable-document">
            <!-- Dynamic Form 6 Engine Injects Formal Schedule Here -->
        </div>

        <div class="form6-action-bar no-print-bar">
            <button type="button" onclick="triggerNativePrint()" style="flex:2; min-width:130px; background:#0284c7; color:#fff; font-weight:bold; border:none; padding:10px 8px; border-radius:6px; font-size:11px; cursor:pointer;">
                🖨️ Save as PDF / Print
            </button>
            <button type="button" onclick="shareForm6Report()" style="flex:1; min-width:90px; background:#16a34a; color:#fff; font-weight:bold; border:none; padding:10px 8px; border-radius:6px; font-size:11px; cursor:pointer;">
                📤 Share
            </button>
            <button type="button" onclick="copyForm6Text()" style="flex:1; min-width:80px; background:#475569; color:#fff; font-weight:bold; border:none; padding:10px 8px; border-radius:6px; font-size:11px; cursor:pointer;">
                📋 Copy
            </button>
            <button type="button" onclick="closeForm6Modal()" style="flex:1; min-width:60px; background:#334155; color:#cbd5e1; border:none; padding:10px 8px; border-radius:6px; font-size:11px; cursor:pointer;">
                ✕
            </button>
        </div>
    </div>
</div>
"""
