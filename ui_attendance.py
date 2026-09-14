# ui_attendance.py - Standalone Form-B Attendance & Offline QR/Barcode Camera Scanner Engine

ATTENDANCE_MODULE = """
<script>
(function() {
    var videoStream = null;
    var scanAnimId = null;
    var detector = null;

    function injectAttendanceUI() {
        if (document.getElementById('statutory-attendance-card')) return;

        var container = document.querySelector('.grid-container') || document.body;
        var card = document.createElement('div');
        card.id = 'statutory-attendance-card';
        card.style.cssText = 'background:#0f172a; border:1px solid #334155; border-radius:10px; padding:16px; margin:14px 0; color:#f8fafc; font-family:system-ui, sans-serif; box-shadow:0 4px 6px rgba(0,0,0,0.5);';

        card.innerHTML = `
            <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #1e293b; padding-bottom:10px; margin-bottom:12px;">
                <div style="display:flex; align-items:center; gap:8px;">
                    <span style="font-size:18px;">⏱️</span>
                    <div>
                        <div style="font-size:13px; font-weight:bold; color:#38bdf8;">WORKER DIGITAL ATTENDANCE (FORM B)</div>
                        <div style="font-size:10px; color:#94a3b8;">Mines Act Sec 48 - Offline QR/Barcode Badge Attendance</div>
                    </div>
                </div>
                <button type="button" onclick="openBadgeCam()" style="background:#0284c7; color:#fff; font-weight:bold; border:none; padding:5px 12px; border-radius:12px; font-size:11px; cursor:pointer; display:flex; align-items:center; gap:4px;">
                    📷 Scan Badge
                </button>
            </div>

            <form id="attendance-form" onsubmit="punchAttendance(event)">
                <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap:10px; margin-bottom:10px;">
                    <div>
                        <label style="font-size:11px; color:#94a3b8;">Punch Type</label>
                        <select id="att-type" style="width:100%; background:#020617; border:1px solid #334155; color:#38bdf8; font-weight:bold; padding:7px; border-radius:6px; font-size:11px; margin-top:3px;">
                            <option value="IN">🟢 PIT ENTRY (Shaft In)</option>
                            <option value="OUT">🔴 PIT EXIT (Shift Out)</option>
                        </select>
                    </div>
                    <div>
                        <label style="font-size:11px; color:#94a3b8;">Miner Name</label>
                        <input type="text" id="att-name" required placeholder="Full Name" style="width:100%; background:#020617; border:1px solid #334155; color:#fff; padding:7px; border-radius:6px; font-size:11px; margin-top:3px; box-sizing:border-box;">
                    </div>
                    <div>
                        <label style="font-size:11px; color:#94a3b8;">Token ID / Badge No.</label>
                        <input type="text" id="att-token" required placeholder="e.g. TK-402" style="width:100%; background:#020617; border:1px solid #334155; color:#fff; padding:7px; border-radius:6px; font-size:11px; margin-top:3px; box-sizing:border-box;">
                    </div>
                </div>

                <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap:8px; margin-bottom:12px;">
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Assigned Shift</span>
                        <select id="att-shift" style="width:100%; background:transparent; border:none; color:#cbd5e1; font-size:11px; margin-top:2px;">
                            <option value="Shift 1">Shift 1 (08:00-16:00)</option>
                            <option value="Shift 2">Shift 2 (16:00-00:00)</option>
                            <option value="Shift 3">Shift 3 (00:00-08:00)</option>
                            <option value="General">General Shift</option>
                        </select>
                    </div>
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">District / Seam</span>
                        <input type="text" id="att-district" required placeholder="e.g. 2nd Dip Face" style="width:100%; background:transparent; border:none; color:#cbd5e1; font-size:11px; margin-top:2px;">
                    </div>
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Trade</span>
                        <input type="text" id="att-trade" placeholder="e.g. SDL Operator" style="width:100%; background:transparent; border:none; color:#cbd5e1; font-size:11px; margin-top:2px;">
                    </div>
                </div>

                <button type="submit" style="width:100%; background:#16a34a; color:#fff; font-weight:bold; border:none; padding:10px; border-radius:6px; font-size:12px; cursor:pointer;">
                    ✅ Punch Form-B Digital Attendance
                </button>
            </form>

            <div style="margin-top:12px; border-top:1px solid #1e293b; padding-top:8px;">
                <div style="display:flex; justify-content:space-between; font-size:11px; color:#94a3b8; margin-bottom:4px;">
                    <b>Attendance Roll (Current Shift)</b>
                    <span id="att-count-label">0 Punches</span>
                </div>
                <div id="att-logs-list" style="max-height:110px; overflow-y:auto; font-size:10px; color:#cbd5e1;"></div>
            </div>
        `;

        container.insertBefore(card, container.firstChild);
        injectScannerModal();
        renderLogs();
    }

    function injectScannerModal() {
        if (document.getElementById('badge-scanner-modal')) return;
        var modal = document.createElement('div');
        modal.id = 'badge-scanner-modal';
        modal.style.cssText = 'display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.92); z-index:11000; justify-content:center; align-items:center; flex-direction:column; font-family:system-ui, sans-serif;';
        modal.innerHTML = `
            <div style="background:#0f172a; border:1px solid #38bdf8; border-radius:12px; padding:14px; width:90%; max-width:360px; color:#fff; text-align:center;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                    <b style="font-size:12px; color:#38bdf8;">📷 Scanner Viewfinder</b>
                    <button type="button" onclick="closeBadgeCam()" style="background:transparent; border:none; color:#94a3b8; font-size:18px; cursor:pointer;">✕</button>
                </div>
                <div style="position:relative; width:100%; height:220px; background:#020617; border-radius:8px; overflow:hidden;">
                    <video id="badge-vid" playsinline style="width:100%; height:100%; object-fit:cover;"></video>
                    <div style="position:absolute; top:25%; left:15%; width:70%; height:50%; border:2px solid #38bdf8; border-radius:6px; box-shadow:0 0 0 2000px rgba(0,0,0,0.5);"></div>
                </div>
                <div style="display:flex; gap:6px; margin-top:10px;">
                    <button type="button" onclick="testBadge()" style="flex:1; background:#1e293b; border:1px solid #334155; color:#cbd5e1; font-size:10px; padding:7px; border-radius:4px; cursor:pointer;">
                        🧪 Test Badge
                    </button>
                    <button type="button" onclick="closeBadgeCam()" style="flex:1; background:#dc2626; color:#fff; font-size:10px; padding:7px; border-radius:4px; border:none; cursor:pointer;">
                        Close
                    </button>
                </div>
            </div>
        `;
        document.body.appendChild(modal);
    }

    window.openBadgeCam = function() {
        var m = document.getElementById('badge-scanner-modal');
        if (m) m.style.display = 'flex';

        if ('BarcodeDetector' in window) {
            detector = new BarcodeDetector({ formats: ['qr_code', 'code_128', 'code_39', 'ean_13'] });
        }
        var vid = document.getElementById('badge-vid');
        if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
            navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } }).then(function(stream) {
                videoStream = stream;
                vid.srcObject = stream;
                vid.play();
                startScan(vid);
            }).catch(function(e) {});
        }
    };

    window.closeBadgeCam = function() {
        var m = document.getElementById('badge-scanner-modal');
        if (m) m.style.display = 'none';
        if (scanAnimId) cancelAnimationFrame(scanAnimId);
        if (videoStream) {
            videoStream.getTracks().forEach(function(t) { t.stop(); });
            videoStream = null;
        }
    };

    function startScan(vid) {
        if (!detector) return;
        function loop() {
            if (!videoStream) return;
            if (vid.readyState === vid.HAVE_ENOUGH_DATA) {
                detector.detect(vid).then(function(codes) {
                    if (codes && codes.length > 0) processBadge(codes[0].rawValue);
                    else scanAnimId = requestAnimationFrame(loop);
                }).catch(function() { scanAnimId = requestAnimationFrame(loop); });
            } else { scanAnimId = requestAnimationFrame(loop); }
        }
        scanAnimId = requestAnimationFrame(loop);
    }

    function processBadge(txt) {
        if (navigator.vibrate) navigator.vibrate([100, 50, 100]);
        window.closeBadgeCam();

        var token = txt.trim(), name = '', trade = '', dist = '';
        try {
            if (txt.startsWith('{')) {
                var o = JSON.parse(txt);
                token = o.token || o.id || token;
                name = o.name || '';
                trade = o.trade || '';
                dist = o.district || '';
            } else if (txt.indexOf('|') !== -1) {
                var p = txt.split('|');
                token = p[0].trim();
                name = p[1] ? p[1].trim() : '';
                trade = p[2] ? p[2].trim() : '';
                dist = p[3] ? p[3].trim() : '';
            }
        } catch(e) {}

        if (token) document.getElementById('att-token').value = token;
        if (name) document.getElementById('att-name').value = name;
        if (trade) document.getElementById('att-trade').value = trade;
        if (dist) document.getElementById('att-district').value = dist;

        alert('✅ Scanned Badge: ' + token + (name ? ' (' + name + ')' : ''));
    }

    window.testBadge = function() {
        processBadge('TK-842|Ramesh Mahto|SDL Operator|2nd Dip Face');
    };

    window.punchAttendance = function(e) {
        if (e) e.preventDefault();
        var type = document.getElementById('att-type').value;
        var name = document.getElementById('att-name').value.trim();
        var token = document.getElementById('att-token').value.trim();
        var shift = document.getElementById('att-shift').value;
        var dist = document.getElementById('att-district').value.trim();
        var trade = document.getElementById('att-trade').value.trim();

        var entry = {
            id: 'ATT-' + Date.now(),
            date: new Date().toLocaleDateString(),
            time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
            type: type,
            miner: name,
            token: token,
            shift: shift,
            district: dist,
            trade: trade,
            seal: 'ATT-SEAL-' + Math.random().toString(36).substring(2, 8).toUpperCase()
        };

        var logs = JSON.parse(localStorage.getItem('dgms_form_b_attendance') || '[]');
        logs.unshift(entry);
        localStorage.setItem('dgms_form_b_attendance', JSON.stringify(logs));

        document.getElementById('att-name').value = '';
        renderLogs();
        alert('✅ Form-B Attendance Punched [' + type + '] for ' + name);
    };

    function renderLogs() {
        var el = document.getElementById('att-logs-list');
        var countEl = document.getElementById('att-count-label');
        if (!el) return;

        var logs = JSON.parse(localStorage.getItem('dgms_form_b_attendance') || '[]');
        if (countEl) countEl.innerText = logs.length + ' Punches';

        if (logs.length === 0) {
            el.innerHTML = '<div style="color:#64748b; padding:4px;">No worker punches logged today.</div>';
            return;
        }

        el.innerHTML = logs.map(function(item) {
            var col = item.type === 'IN' ? '#4ade80' : '#f59e0b';
            return `
                <div style="background:#020617; border:1px solid #1e293b; padding:5px 8px; border-radius:4px; margin-bottom:3px; display:flex; justify-content:space-between;">
                    <div>
                        <span style="color:#38bdf8; font-weight:bold;">${item.miner} (${item.token})</span>
                        <span style="color:#64748b; margin-left:4px;">${item.district}</span>
                    </div>
                    <div>
                        <span style="color:${col}; font-weight:bold;">[${item.type}] ${item.time}</span>
                    </div>
                </div>
            `;
        }).join('');
    }

    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', injectAttendanceUI);
    else injectAttendanceUI();
    setTimeout(injectAttendanceUI, 3000);
})();
</script>
"""
