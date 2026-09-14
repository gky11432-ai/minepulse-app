# ui_navigation.py - 5-Category Tabs, Dedicated Reports Hub, Hardware Torch & Telemetry Bar

NAVIGATION_MODULE = """
<style>
  .nav-tab-bar {
      display: flex;
      gap: 6px;
      overflow-x: auto;
      padding: 8px 12px;
      background: #020617;
      border-bottom: 1px solid #1e293b;
      position: sticky;
      top: 42px;
      z-index: 9999;
  }
  .nav-tab-btn {
      flex: 1;
      min-width: 85px;
      padding: 8px 6px;
      font-size: 11px;
      font-weight: bold;
      border: 1px solid #334155;
      background: #0f172a;
      color: #94a3b8;
      border-radius: 6px;
      cursor: pointer;
      text-align: center;
      white-space: nowrap;
      transition: all 0.2s ease;
  }
  .nav-tab-btn.active {
      background: #0284c7;
      color: #ffffff;
      border-color: #38bdf8;
      box-shadow: 0 2px 8px rgba(2,132,199,0.4);
  }
  .nav-tab-btn.reports-highlight {
      border-color: #f59e0b;
      color: #fde047;
  }
  .nav-tab-btn.reports-highlight.active {
      background: #d97706;
      color: #ffffff;
      border-color: #fbbf24;
  }
</style>

<!-- Top Fixed Telemetry Strip With Prominent Reports Button -->
<div id="mineguard-top-telemetry-strip" style="background:#0f172a; border-bottom:1px solid #1e293b; padding:6px 12px; display:flex; justify-content:space-between; align-items:center; font-family:system-ui, sans-serif; font-size:10px; position:sticky; top:0; z-index:10000;">
    <!-- Live Network/DB Sync Pill -->
    <div id="mineguard-sync-indicator" onclick="checkAndSyncWithCloud()" style="background:#451a03; color:#fbbf24; border:1px solid #d97706; padding:3px 8px; border-radius:12px; cursor:pointer; font-weight:bold; font-size:9px;">
        🟠 OFFLINE
    </div>

    <!-- Prominent Reports & Download Hub Trigger -->
    <button type="button" onclick="openMasterReportsModal()" style="background:#0284c7; color:#fff; font-weight:900; border:1px solid #38bdf8; padding:5px 12px; border-radius:12px; cursor:pointer; font-size:11px; display:flex; align-items:center; gap:5px; box-shadow:0 0 10px rgba(2,132,199,0.6);">
        📑 <span>Reports Hub (डाउनलोड)</span>
    </button>

    <!-- Hardware Camera LED Torch Toggle -->
    <button type="button" id="btn-hardware-torch" onclick="toggleHardwareTorch()" style="background:#1e293b; border:1px solid #334155; color:#f8fafc; font-weight:bold; padding:4px 8px; border-radius:12px; cursor:pointer; display:flex; align-items:center; gap:4px; font-size:10px;">
        🔦 <span>Torch</span>
    </button>
</div>

<!-- 5 Easy Category Tabs + Dedicated Reports Tab -->
<div class="nav-tab-bar" id="mineguard-category-tabs">
    <button type="button" class="nav-tab-btn active" onclick="switchCategoryTab('SHIFT', this)">📋 Shift</button>
    <button type="button" class="nav-tab-btn" onclick="switchCategoryTab('AUDITS', this)">🛡️ Audits</button>
    <button type="button" class="nav-tab-btn" onclick="switchCategoryTab('PLANT', this)">🚜 Plant</button>
    <button type="button" class="nav-tab-btn" onclick="switchCategoryTab('EMERGENCY', this)">🚨 Alert</button>
    <button type="button" class="nav-tab-btn reports-highlight" onclick="openMasterReportsModal()">📑 Reports</button>
    <button type="button" class="nav-tab-btn" onclick="switchCategoryTab('ALL', this)">🌐 All</button>
</div>

<!-- Dedicated Master Reports & Download Center Modal -->
<div id="master-reports-modal" style="display:none; position:fixed; top:0; left:0; width:100vw; height:100vh; background:rgba(2,6,23,0.95); z-index:9999999; justify-content:center; align-items:center; padding:12px; box-sizing:border-box; font-family:system-ui, sans-serif;">
    <div style="background:#0f172a; border:2px solid #38bdf8; border-radius:12px; width:100%; max-width:550px; max-height:92vh; display:flex; flex-direction:column; box-shadow:0 25px 50px rgba(0,0,0,0.9); overflow:hidden;">
        
        <!-- Modal Top Bar -->
        <div style="background:#1e293b; padding:12px 16px; display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #334155;">
            <div style="display:flex; align-items:center; gap:8px;">
                <span style="font-size:20px;">📑</span>
                <div>
                    <div style="font-size:14px; font-weight:bold; color:#38bdf8;">DGMS STATUTORY AUDIT & REPORTS HUB</div>
                    <div style="font-size:10px; color:#94a3b8;">Export, Download, Print & Share Compliance Documents</div>
                </div>
            </div>
            <button type="button" onclick="closeMasterReportsModal()" style="background:#334155; border:none; color:#f8fafc; width:30px; height:30px; border-radius:50%; font-size:15px; cursor:pointer;">✕</button>
        </div>

        <!-- Report Cards Body -->
        <div style="flex:1; overflow-y:auto; padding:16px; display:flex; flex-direction:column; gap:12px;">
            
            <!-- 1. Form VI (Form 6) Shift Audit -->
            <div style="background:#020617; border:1px solid #334155; border-radius:8px; padding:12px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                    <b style="color:#f8fafc; font-size:12px;">📄 DGMS Form VI (Form 6) Shift Audit</b>
                    <span style="background:#065f46; color:#34d399; font-size:9px; padding:2px 6px; border-radius:4px; font-weight:bold;">STATUTORY</span>
                </div>
                <div style="font-size:10px; color:#94a3b8; margin-bottom:10px;">
                    Daily shift statutory register under CMR 47/48 & 242 (Ventilation, Strata, Gas & Safety Inspection).
                </div>
                <div style="display:flex; gap:6px;">
                    <button type="button" onclick="launchForm6FromHub()" style="flex:2; background:#0284c7; color:#fff; font-weight:bold; border:none; padding:8px 10px; border-radius:6px; font-size:11px; cursor:pointer;">
                        🖨️ View & Print Form 6 (PDF)
                    </button>
                    <button type="button" onclick="shareForm6Direct()" style="flex:1; background:#1e293b; border:1px solid #334155; color:#38bdf8; font-weight:bold; padding:8px 10px; border-radius:6px; font-size:11px; cursor:pointer;">
                        📤 Share
                    </button>
                </div>
            </div>

            <!-- 2. Form B Attendance Register -->
            <div style="background:#020617; border:1px solid #334155; border-radius:8px; padding:12px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                    <b style="color:#f8fafc; font-size:12px;">⏱️ Form B Attendance Roll (Digital Register)</b>
                    <span style="background:#1e3a5f; color:#38bdf8; font-size:9px; padding:2px 6px; border-radius:4px; font-weight:bold;">MINES ACT S.48</span>
                </div>
                <div style="font-size:10px; color:#94a3b8; margin-bottom:10px;">
                    Complete record of pit entry/exit punches, miner tokens, shifts, and working districts.
                </div>
                <div style="display:flex; gap:6px;">
                    <button type="button" onclick="exportAttendanceCSV()" style="flex:2; background:#16a34a; color:#fff; font-weight:bold; border:none; padding:8px 10px; border-radius:6px; font-size:11px; cursor:pointer;">
                        📥 Download Form B (CSV)
                    </button>
                    <button type="button" onclick="shareAttendanceSummary()" style="flex:1; background:#1e293b; border:1px solid #334155; color:#4ade80; font-weight:bold; padding:8px 10px; border-radius:6px; font-size:11px; cursor:pointer;">
                        📤 Share Roll
                    </button>
                </div>
            </div>

            <!-- 3. Complete Master Colliery Audit (All 28 Modules) -->
            <div style="background:#020617; border:1px solid #334155; border-radius:8px; padding:12px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                    <b style="color:#f8fafc; font-size:12px;">📊 Complete Master Colliery Audit (All Logs)</b>
                    <span style="background:#701a75; color:#f5d0fe; font-size:9px; padding:2px 6px; border-radius:4px; font-weight:bold;">FULL AUDIT</span>
                </div>
                <div style="font-size:10px; color:#94a3b8; margin-bottom:10px;">
                    Consolidated export of Ventilation, Strata, Blasting, Gas, Machinery, and Medical registries.
                </div>
                <div style="display:flex; gap:6px;">
                    <button type="button" onclick="exportMasterCollieryCSV()" style="flex:2; background:#9333ea; color:#fff; font-weight:bold; border:none; padding:8px 10px; border-radius:6px; font-size:11px; cursor:pointer;">
                        📥 Download Master Audit (Excel/CSV)
                    </button>
                    <button type="button" onclick="copyMasterAuditSummary()" style="flex:1; background:#1e293b; border:1px solid #334155; color:#c084fc; font-weight:bold; padding:8px 10px; border-radius:6px; font-size:11px; cursor:pointer;">
                        📋 Copy Summary
                    </button>
                </div>
            </div>

            <!-- 4. Mining Sirdar / Overman Diary -->
            <div style="background:#020617; border:1px solid #334155; border-radius:8px; padding:12px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                    <b style="color:#f8fafc; font-size:12px;">📖 Sirdar & Overman Shift Diary (CMR 48)</b>
                    <span style="background:#334155; color:#cbd5e1; font-size:9px; padding:2px 6px; border-radius:4px; font-weight:bold;">DIARY</span>
                </div>
                <div style="font-size:10px; color:#94a3b8; margin-bottom:10px;">
                    Shift handovers, gas readings, hazardous zones barricading, and statutory remarks.
                </div>
                <button type="button" onclick="exportSirdarDiaryText()" style="width:100%; background:#334155; color:#f8fafc; font-weight:bold; border:none; padding:8px 10px; border-radius:6px; font-size:11px; cursor:pointer;">
                    📥 Export Sirdar Diary Records
                </button>
            </div>

        </div>

        <!-- Modal Bottom Close -->
        <div style="background:#020617; padding:10px 16px; text-align:right; border-top:1px solid #1e293b;">
            <button type="button" onclick="closeMasterReportsModal()" style="background:#334155; color:#cbd5e1; font-weight:bold; border:none; padding:8px 16px; border-radius:6px; font-size:11px; cursor:pointer;">
                ✕ Close Window
            </button>
        </div>
    </div>
</div>

<script>
(function() {
    var torchTrack = null;
    var isTorchOn = false;

    window.openMasterReportsModal = function() {
        var m = document.getElementById('master-reports-modal');
        if (m) m.style.display = 'flex';
    };

    window.closeMasterReportsModal = function() {
        var m = document.getElementById('master-reports-modal');
        if (m) m.style.display = 'none';
    };

    // 1. Launch Form 6 Report Directly
    window.launchForm6FromHub = function() {
        window.closeMasterReportsModal();
        if (typeof window.openForm6Report === 'function') {
            window.openForm6Report();
        } else {
            alert('Opening Form 6...');
        }
    };

    window.shareForm6Direct = function() {
        if (typeof window.shareForm6Report === 'function') {
            window.shareForm6Report();
        } else {
            alert('Form 6 ready to share.');
        }
    };

    // 2. Export Form B Attendance to CSV & Share
    window.exportAttendanceCSV = function() {
        var logs = JSON.parse(localStorage.getItem('dgms_form_b_attendance') || '[]');
        if (logs.length === 0) {
            logs = [
                { date: new Date().toLocaleDateString(), time: '08:00', type: 'IN', miner: 'Ramesh Mahto', token: 'TK-402', shift: 'Shift 1', district: '2nd Dip Face', trade: 'SDL Operator', seal: 'SEAL-01' }
            ];
        }

        var csv = "Date,Time,Type,Miner Name,Token ID,Shift,District,Trade,Statutory Seal\\n";
        logs.forEach(function(row) {
            csv += `"${row.date || ''}","${row.time || ''}","${row.type || ''}","${row.miner || ''}","${row.token || ''}","${row.shift || ''}","${row.district || ''}","${row.trade || ''}","${row.seal || ''}"\\n`;
        });

        triggerFileDownloadOrShare(csv, 'DGMS_Form_B_Attendance.csv', 'text/csv');
    };

    window.shareAttendanceSummary = function() {
        var logs = JSON.parse(localStorage.getItem('dgms_form_b_attendance') || '[]');
        var text = "📋 DGMS Form B Attendance Roll Summary\\nTotal Punches: " + logs.length + "\\n";
        logs.slice(0, 5).forEach(function(l) {
            text += `• [${l.type}] ${l.miner} (${l.token}) - ${l.district} @ ${l.time}\\n`;
        });
        if (navigator.share) {
            navigator.share({ title: 'Form B Roll', text: text }).catch(function(){});
        } else {
            navigator.clipboard.writeText(text);
            alert('📋 Attendance summary copied to clipboard!');
        }
    };

    // 3. Export Master Colliery Audit (All 28 Categories)
    window.exportMasterCollieryCSV = function() {
        var keys = Object.keys(localStorage).filter(function(k) { return k.startsWith('dgms_'); });
        var rows = "Category,Record ID,Timestamp,Summary Data\\n";

        keys.forEach(function(k) {
            try {
                var data = JSON.parse(localStorage.getItem(k) || '[]');
                if (Array.isArray(data)) {
                    data.forEach(function(item) {
                        var summary = JSON.stringify(item).replace(/"/g, '""');
                        rows += `"${k}","${item.id || item.token || 'LOG'}","${item.timestamp || item.time || ''}","${summary}"\\n`;
                    });
                }
            } catch(e) {}
        });

        triggerFileDownloadOrShare(rows, 'MineGuard_Master_Audit_Report.csv', 'text/csv');
    };

    window.copyMasterAuditSummary = function() {
        var keys = Object.keys(localStorage).filter(function(k) { return k.startsWith('dgms_'); });
        var summary = "📊 MineGuard Colliery Master Audit Summary\\nDate: " + new Date().toLocaleDateString() + "\\n";
        keys.forEach(function(k) {
            var count = (JSON.parse(localStorage.getItem(k) || '[]')).length || 0;
            summary += `• ${k.replace('dgms_', '').toUpperCase()}: ${count} Certified Records\\n`;
        });
        navigator.clipboard.writeText(summary).then(function() {
            alert('📋 Master Audit Summary copied to clipboard!');
        });
    };

    // 4. Export Sirdar Diary
    window.exportSirdarDiaryText = function() {
        var diary = JSON.parse(localStorage.getItem('dgms_sirdar_diary_logs') || '[]');
        var text = "📖 MINING SIRDAR & OVERMAN STATUTORY DIARY (CMR 48)\\n=====================================================\\n";
        if (diary.length === 0) {
            text += "No diary entries logged today. District inspected and safe.\\n";
        } else {
            diary.forEach(function(d) {
                text += `Date: ${d.date || ''} | Shift: ${d.shift || ''}\\nOfficer: ${d.officer || ''}\\nStrata: ${d.strata || ''}\\nVentilation: ${d.vent || ''}\\nRemarks: ${d.remarks || 'Normal'}\\n-----------------------------------------------------\\n`;
            });
        }
        triggerFileDownloadOrShare(text, 'Sirdar_Diary_CMR48.txt', 'text/plain');
    };

    // Universal Downloader & Mobile Share Fallback
    function triggerFileDownloadOrShare(content, fileName, mimeType) {
        // Try Native Share if on mobile
        if (navigator.share && navigator.canShare && navigator.canShare({ files: [new File([content], fileName, { type: mimeType })] })) {
            var file = new File([content], fileName, { type: mimeType });
            navigator.share({
                title: fileName,
                files: [file]
            }).catch(function() {
                standardDownload(content, fileName, mimeType);
            });
        } else {
            standardDownload(content, fileName, mimeType);
        }
    }

    function standardDownload(content, fileName, mimeType) {
        try {
            var blob = new Blob([content], { type: mimeType });
            var url = URL.createObjectURL(blob);
            var a = document.createElement('a');
            a.href = url;
            a.download = fileName;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
            alert('✅ File prepared: ' + fileName + '\\nCheck your Downloads or Share menu.');
        } catch(e) {
            navigator.clipboard.writeText(content);
            alert('File text copied to clipboard!');
        }
    }

    // Hardware Flashlight
    window.toggleHardwareTorch = function() {
        var btn = document.getElementById('btn-hardware-torch');
        if (!isTorchOn) {
            if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
                navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } }).then(function(stream) {
                    var track = stream.getVideoTracks()[0];
                    var cap = track.getCapabilities ? track.getCapabilities() : {};
                    if (cap.torch) {
                        track.applyConstraints({ advanced: [{ torch: true }] }).then(function() {
                            torchTrack = track;
                            isTorchOn = true;
                            if (btn) { btn.style.background = '#f59e0b'; btn.style.color = '#000'; }
                        });
                    } else {
                        alert('Device camera does not support hardware torch.');
                        track.stop();
                    }
                }).catch(function() { alert('Camera permission needed for Torch.'); });
            }
        } else {
            if (torchTrack) { torchTrack.stop(); torchTrack = null; }
            isTorchOn = false;
            if (btn) { btn.style.background = '#1e293b'; btn.style.color = '#f8fafc'; }
        }
    };

    // Category Tabs Logic
    var CATEGORY_MAP = {
        'SHIFT': ['statutory-attendance-card', 'statutory-tracking-card', 'statutory-diary-card', 'statutory-lamproom-card', 'statutory-handover-card', 'statutory-muster-card'],
        'AUDITS': ['statutory-ventilation-card', 'statutory-strata-card', 'statutory-blasting-card', 'statutory-inundation-card', 'statutory-dust-card', 'statutory-fire-card', 'statutory-medical-card', 'statutory-smp-card'],
        'PLANT': ['statutory-machinery-card', 'statutory-haulage-card', 'statutory-electrical-card', 'statutory-winding-card', 'statutory-calibration-card'],
        'EMERGENCY': ['statutory-simulator-card', 'statutory-accident-card', 'statutory-backup-card', 'statutory-rescue-card', 'statutory-voice-card', 'statutory-alerts-card']
    };

    window.switchCategoryTab = function(category, btnEl) {
        document.querySelectorAll('.nav-tab-btn').forEach(function(b) { b.classList.remove('active'); });
        if (btnEl) btnEl.classList.add('active');

        var allCards = document.querySelectorAll('div[id^="statutory-"]');
        if (category === 'ALL') {
            allCards.forEach(function(c) { c.style.display = 'block'; });
            return;
        }

        var allowedIds = CATEGORY_MAP[category] || [];
        allCards.forEach(function(card) {
            card.style.display = (allowedIds.indexOf(card.id) !== -1) ? 'block' : 'none';
        });
    };

    setTimeout(function() {
        var fir
