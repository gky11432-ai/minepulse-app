# ui_sirdar_diary.py - Standalone DGMS CMR 47-48 Sirdar & Overman Statutory Shift Diary

SIRDAR_DIARY_MODULE = """
<script>
(function() {
    function injectSirdarDiaryUI() {
        if (document.getElementById('statutory-diary-card')) return;

        var container = document.querySelector('.grid-container') || document.body;

        var card = document.createElement('div');
        card.id = 'statutory-diary-card';
        card.style.cssText = 'background:#0f172a; border:1px solid #334155; border-radius:10px; padding:16px; margin:14px 0; color:#f8fafc; font-family:system-ui, sans-serif; box-shadow:0 4px 6px -1px rgba(0,0,0,0.5);';

        card.innerHTML = `
            <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #1e293b; padding-bottom:10px; margin-bottom:12px;">
                <div style="display:flex; align-items:center; gap:8px;">
                    <span style="font-size:18px;">📘</span>
                    <div>
                        <div style="font-size:13px; font-weight:bold; color:#38bdf8;">MINING SIRDAR & OVERMAN STATUTORY SHIFT DIARY</div>
                        <div style="font-size:10px; color:#94a3b8;">DGMS CMR 2017 Reg 47 & 48 - District Inspection, Strata Soundness & Relieving Ledger</div>
                    </div>
                </div>
                <div id="diary-status-badge" style="background:#14532d; color:#4ade80; border:1px solid #22c55e; font-size:10px; padding:3px 8px; border-radius:12px; font-weight:bold;">
                    ✓ DISTRICT SAFE & CERTIFIED
                </div>
            </div>

            <!-- Statutory Shift Diary Form -->
            <form id="sirdar-diary-form" onsubmit="recordSirdarDiary(event)">
                <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap:10px; margin-bottom:10px;">
                    <div>
                        <label style="font-size:11px; color:#94a3b8;">Working Shift & Time Span</label>
                        <select id="diary-shift" style="width:100%; background:#020617; border:1px solid #334155; color:#38bdf8; font-weight:bold; padding:8px; border-radius:6px; font-size:11px; margin-top:4px;">
                            <option value="1st Shift (08:00 - 16:00)">1st Shift (08:00 - 16:00)</option>
                            <option value="2nd Shift (16:00 - 00:00)">2nd Shift (16:00 - 00:00)</option>
                            <option value="3rd Night Shift (00:00 - 08:00)">3rd Night Shift (00:00 - 08:00)</option>
                            <option value="General Shift (09:00 - 17:00)">General Shift (09:00 - 17:00)</option>
                        </select>
                    </div>
                    <div>
                        <label style="font-size:11px; color:#94a3b8;">Assigned District / Panel Section</label>
                        <input type="text" id="diary-district" required placeholder="e.g. 2nd Dip Face / Depillaring District East" style="width:100%; background:#020617; border:1px solid #334155; color:#fff; padding:8px; border-radius:6px; font-size:11px; margin-top:4px;">
                    </div>
                    <div>
                        <label style="font-size:11px; color:#94a3b8;">Inspecting Sirdar / Overman Name & Cert</label>
                        <input type="text" id="diary-sirdar-name" required placeholder="Name & Sirdar/Overman Cert No." style="width:100%; background:#020617; border:1px solid #334155; color:#fff; padding:8px; border-radius:6px; font-size:11px; margin-top:4px;">
                    </div>
                </div>

                <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap:8px; margin-bottom:12px;">
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Roof & Side Examination (CMR 48)</span>
                        <select id="diary-strata-status" onchange="evaluateDiaryCompliance()" style="width:100%; background:transparent; border:none; color:#4ade80; font-weight:bold; font-size:11px; margin-top:2px;">
                            <option value="Sound & Fully Supported">Sound & Fully Supported</option>
                            <option value="Minor Sloughing (Dressed Down)">Minor Sloughing (Dressed)</option>
                            <option value="Heavy Weighting / Cracks Observed">⚠️ Heavy Weighting / Cracks</option>
                            <option value="Unsupported Span Exceeded">🚨 Unsupported Span Exceeded</option>
                        </select>
                    </div>
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Ventilation & Airflow Condition</span>
                        <select id="diary-vent-status" onchange="evaluateDiaryCompliance()" style="width:100%; background:transparent; border:none; color:#4ade80; font-weight:bold; font-size:11px; margin-top:2px;">
                            <option value="Adequate Airflow / CH4 Clean">Adequate Air / CH4 Clean</option>
                            <option value="Sluggish Airflow at Face">⚠️ Sluggish Airflow</option>
                            <option value="Auxiliary Fan Stoppage">🚨 Auxiliary Fan Stoppage</option>
                        </select>
                    </div>
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Danger Fencing (CMR 48 Sub 4)</span>
                        <select id="diary-fencing-status" onchange="evaluateDiaryCompliance()" style="width:100%; background:transparent; border:none; color:#4ade80; font-weight:bold; font-size:11px; margin-top:2px;">
                            <option value="All Unused Places Securely Fenced">All Danger Places Fenced</option>
                            <option value="Fence Damaged (Repaired on Shift)">Fence Repaired on Shift</option>
                            <option value="Disused Roadway Fence Missing">🚨 Fence Missing on Heading</option>
                        </select>
                    </div>
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Manpower Supervised</span>
                        <input type="number" id="diary-men-count" required placeholder="e.g. 24 Miners" style="width:100%; background:transparent; border:none; color:#38bdf8; font-weight:bold; font-size:12px; margin-top:2px;">
                    </div>
                </div>

                <div style="display:grid; grid-template-columns: 1fr 1fr; gap:8px; margin-bottom:10px;">
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Face Machinery & Signal Bells</span>
                        <select id="diary-machinery-status" style="width:100%; background:transparent; border:none; color:#cbd5e1; font-size:11px; margin-top:2px;">
                            <option value="SDL/LHD & Bells in Normal Order">SDL/LHD & Bells Operational</option>
                            <option value="Conveyor Belt Slip Switch Tested">Conveyor Switches Tested</option>
                            <option value="Face Drill Ground Fault Repaired">Face Drill Checked</option>
                            <option value="Haulage Signals Defective">⚠️ Haulage Signal Defective</option>
                        </select>
                    </div>
                    <div style="background:#020617; border:1px solid #1e293b; padding:8px; border-radius:6px;">
                        <span style="font-size:10px; color:#94a3b8;">Manager / Asst. Manager Countersignature</span>
                        <input type="text" id="diary-manager-sign" required placeholder="Countersigning Official Name & Reg" style="width:100%; background:transparent; border:none; color:#cbd5e1; font-size:11px; margin-top:2px;">
                    </div>
                </div>

                <div style="margin-bottom:10px;">
                    <label style="font-size:11px; color:#94a3b8;">Statutory Handover Remarks / Instructions to Relieving Sirdar</label>
                    <textarea id="diary-remarks" rows="2" required placeholder="e.g. Check prop density at junction. Dressing completed at 3rd slice. Relieving Sirdar warned of water seepage." style="width:100%; background:#020617; border:1px solid #334155; color:#fff; padding:8px; border-radius:6px; font-size:11px; margin-top:4px; box-sizing:border-box;"></textarea>
                </div>

                <div id="diary-statutory-msg" style="background:#020617; border:1px dashed #334155; padding:8px; border-radius:6px; margin-bottom:12px; font-size:11px; color:#cbd5e1;">
                    CMR 47/48 Mandatory Requirement: Sirdar shall not leave the mine until relieved by successor or having personally certified the district safe.
                </div>

                <button type="submit" id="submit-diary-btn" style="width:100%; background:#0284c7; color:#fff; font-weight:bold; border:none; padding:10px; border-radius:6px; font-size:12px; cursor:pointer;">
                    ✍️ Sign & Submit Statutory Shift Diary (CMR 47/48)
                </button>
            </form>

            <!-- Shift Diary Archive Ledger -->
            <div style="margin-top:14px; border-top:1px solid #1e293b; padding-top:10px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                    <div style="font-size:11px; font-weight:bold; color:#cbd5e1;">Certified Statutory Shift Diaries Ledger</div>
                    <span id="diary-count-badge" style="background:#334155; color:#cbd5e1; font-size:9px; padding:2px 6px; border-radius:8px;">0 Shifts</span>
                </div>
                <div id="diary-history-list" style="max-height:130px; overflow-y:auto; font-size:10px; color:#94a3b8;">
                    No shift diary entries recorded for today.
                </div>
            </div>
        `;

        container.appendChild(card);
        renderDiaryLogs();
    }

    window.evaluateDiaryCompliance = function() {
        var strata = document.getElementById('diary-strata-status').value;
        var vent = document.getElementById('diary-vent-status').value;
        var fence = document.getElementById('diary-fencing-status').value;
        var badge = document.getElementById('diary-status-badge');
        var msg = document.getElementById('diary-statutory-msg');
        var btn = document.getElementById('submit-diary-btn');

        if (!badge || !msg) return;

        var isDanger = (strata.indexOf('Exceeded') !== -1 || strata.indexOf('Heavy') !== -1 || vent.indexOf('Stoppage') !== -1 || fence.indexOf('Missing') !== -1);

        if (isDanger) {
            badge.style.background = '#7f1d1d';
            badge.style.color = '#fca5a5';
            badge.style.borderColor = '#ef4444';
            badge.innerText = '🚨 STATUTORY DEFECTS LOGGED: CAUTION';

            msg.innerHTML = '<span style="color:#ef4444; font-weight:bold;">STATUTORY WARNING (CMR 47/48):</span> Unsafe strata condition, deficient ventilation, or un-fenced dangerous place logged. Directives must be highlighted to Manager and relieving shift.';
            if (btn) {
                btn.style.background = '#dc2626';
                btn.innerText = '⚠️ Submit Diary with Statutory Exception Tags';
            }
            return false;
        } else {
            badge.style.background = '#14532d';
            badge.style.color = '#4ade80';
            badge.style.borderColor = '#22c55e';
            badge.innerText = '✓ DISTRICT SAFE & CERTIFIED';

            msg.innerHTML = '<span style="color:#4ade80; font-weight:bold;">COMPLIANT:</span> District inspected, ventilation adequate, strata fully supported. Handover cleared.';
            if (btn) {
                btn.style.background = '#0284c7';
                btn.innerText = '✍️ Sign & Submit Statutory Shift Diary (CMR 47/48)';
            }
            return true;
        }
    };

    window.recordSirdarDiary = function(e) {
        if (e) e.preventDefault();
        var shift = document.getElementById('diary-shift').value;
        var district = document.getElementById('diary-district').value;
        var sirdar = document.getElementById('diary-sirdar-name').value;
        var strata = document.getElementById('diary-strata-status').value;
        var vent = document.getElementById('diary-vent-status').value;
        var fence = document.getElementById('diary-fencing-status').value;
        var men = document.getElementById('diary-men-count').value;
        var machinery = document.getElementById('diary-machinery-status').value;
        var mgr = document.getElementById('diary-manager-sign').value;
        var remarks = document.getElementById('diary-remarks').value;

        var isDefective = (strata.indexOf('Exceeded') !== -1 || strata.indexOf('Heavy') !== -1 || vent.indexOf('Stoppage') !== -1 || fence.indexOf('Missing') !== -1);
        var statusText = isDefective ? 'DEFECT TAGGED / ACTION REQ' : 'CERTIFIED SAFE FOR CONTINUATION';

        var entry = {
            id: 'DIARY-' + Date.now(),
            date: new Date().toLocaleDateString(),
            time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
            shift: shift,
            district: district,
            sirdar: sirdar,
            strata: strata,
            vent: vent,
            fence: fence,
            men: men + ' men',
            machinery: machinery,
            manager: mgr,
            remarks: remarks,
            status: statusText,
            seal: 'SIRDAR-SEAL-' + Math.random().toString(36).substring(2, 8).toUpperCase()
        };

        var store = JSON.parse(localStorage.getItem('dgms_sirdar_diary_logs') || '[]');
        store.unshift(entry);
        localStorage.setItem('dgms_sirdar_diary_logs', JSON.stringify(store));

        document.getElementById('diary-remarks').value = '';
        renderDiaryLogs();

        alert('✅ Statutory Shift Diary Signed & Locked with Seal ' + entry.seal);
    };

    function renderDiaryLogs() {
        var el = document.getElementById('diary-history-list');
        var badge = document.getElementById('diary-count-badge');
        if (!el) return;

        var store = JSON.parse(localStorage.getItem('dgms_sirdar_diary_logs') || '[]');
        if (badge) badge.innerText = store.length + ' Shifts';

        if (store.length === 0) {
            el.innerHTML = '<div style="color:#64748b; padding:4px;">No shift diary entries recorded for today.</div>';
            return;
        }

        el.innerHTML = store.map(function(item) {
            var isDefect = item.status.indexOf('DEFECT') !== -1;
            var col = isDefect ? '#ef4444' : '#4ade80';
            return `
                <div style="background:#020617; border:1px solid #1e293b; padding:6px 8px; border-radius:4px; margin-bottom:4px;">
                    <div style="display:flex; justify-content:space-between; font-weight:bold;">
                        <span style="color:#38bdf8;">${item.shift} - ${item.district}</span>
                        <span style="font-family:monospace; color:#f59e0b; font-size:9px;">${item.seal}</span>
                    </div>
                    <div style="display:flex; justify-content:space-between; color:#cbd5e1; margin-top:2px;">
                        <span>Strata: <b>${item.strata.slice(0, 18)}</b> | Men: <b>${item.men}</b></span>
                        <span style="color:${col}; font-weight:bold;">${item.status}</span>
                    </div>
                    <div style="color:#cbd5e1; font-size:10px; margin-top:2px; font-style:italic;">
                        "${item.remarks.slice(0, 70)}..."
                    </div>
                    <div style="color:#64748b; font-size:9px; margin-top:2px;">
                        ${item.date} ${item.time} • Sirdar: ${item.sirdar} • Counter-Signed: ${item.manager}
                    </div>
                </div>
            `;
        }).join('');
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', injectSirdarDiaryUI);
    } else {
        injectSirdarDiaryUI();
    }
    setTimeout(injectSirdarDiaryUI, 5400);
})();
</script>
"""
