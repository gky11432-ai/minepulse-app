# ui_muster.py - Standalone DGMS CMR 241 Emergency Evacuation Muster & Headcount Roll-Call

MUSTER_MODULE = """
<script>
(function() {
    function injectMusterUI() {
        if (document.getElementById('muster-accountability-card')) return;

        var container = document.querySelector('.grid-container') || document.body;

        var card = document.createElement('div');
        card.id = 'muster-accountability-card';
        card.style.cssText = 'background:#0f172a; border:1px solid #334155; border-radius:10px; padding:16px; margin:14px 0; color:#f8fafc; font-family:system-ui, sans-serif; box-shadow:0 4px 6px -1px rgba(0,0,0,0.5);';

        card.innerHTML = `
            <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #1e293b; padding-bottom:10px; margin-bottom:12px;">
                <div style="display:flex; align-items:center; gap:8px;">
                    <span style="font-size:18px;">👷</span>
                    <div>
                        <div style="font-size:13px; font-weight:bold; color:#38bdf8;">UNDERGROUND PERSONNEL MUSTER ROLL</div>
                        <div style="font-size:10px; color:#94a3b8;">CMR 2017 Reg 241 - Shift Evacuation Headcount & Accountability</div>
                    </div>
                </div>
                <div id="muster-summary-stats" style="display:flex; gap:6px;">
                    <span id="stat-total" style="background:#1e293b; color:#cbd5e1; border:1px solid #475569; font-size:10px; padding:3px 8px; border-radius:10px; font-weight:bold;">Total: 0</span>
                    <span id="stat-underground" style="background:#7f1d1d; color:#fca5a5; border:1px solid #ef4444; font-size:10px; padding:3px 8px; border-radius:10px; font-weight:bold;">Pit: 0</span>
                    <span id="stat-safe" style="background:#14532d; color:#86efac; border:1px solid #22c55e; font-size:10px; padding:3px 8px; border-radius:10px; font-weight:bold;">Surface: 0</span>
                </div>
            </div>

            <!-- Fast Check-in / Tag-in Form -->
            <form id="muster-entry-form" onsubmit="addMusterWorker(event)" style="display:grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap:8px; margin-bottom:12px;">
                <input type="text" id="worker-name" placeholder="Miner Name / Token No." required style="background:#020617; border:1px solid #334155; color:#fff; padding:7px 10px; border-radius:6px; font-size:11px;">
                <select id="worker-craft" style="background:#020617; border:1px solid #334155; color:#fff; padding:7px 10px; border-radius:6px; font-size:11px;">
                    <option value="SDL/LHD Operator">SDL/LHD Operator</option>
                    <option value="Drill Operator / Blaster">Drill Operator / Blaster</option>
                    <option value="Support Timberman">Support Timberman</option>
                    <option value="Underground Electrician">Underground Electrician</option>
                    <option value="Overman / Sirdar">Overman / Sirdar</option>
                    <option value="General Trammer">General Trammer</option>
                </select>
                <select id="worker-zone" style="background:#020617; border:1px solid #334155; color:#fff; padding:7px 10px; border-radius:6px; font-size:11px;">
                    <option value="Face-1 Development Drift">Face-1 Development Drift</option>
                    <option value="Depillaring District A">Depillaring District A</option>
                    <option value="Main Return Airway">Main Return Airway</option>
                    <option value="Haulage Engine Pit">Haulage Engine Pit</option>
                    <option value="Intake Shaft Bottom">Intake Shaft Bottom</option>
                </select>
                <button type="submit" style="background:#0284c7; color:#fff; border:none; padding:7px 14px; border-radius:6px; font-weight:bold; font-size:11px; cursor:pointer;">
                    + Tag Into Pit
                </button>
            </form>

            <!-- Emergency Actions Bar -->
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px; background:#020617; padding:8px 10px; border-radius:6px; border:1px solid #1e293b;">
                <span style="font-size:11px; color:#94a3b8;">Emergency Accountability Actions:</span>
                <div style="display:flex; gap:6px;">
                    <button type="button" onclick="evacuateAllPersonnel()" style="background:#15803d; color:#fff; border:none; padding:5px 10px; border-radius:4px; font-size:10px; font-weight:bold; cursor:pointer;">
                        🟢 Tag All Evacuated (Clear Pit)
                    </button>
                    <button type="button" onclick="resetDefaultShiftMuster()" style="background:#334155; color:#cbd5e1; border:none; padding:5px 10px; border-radius:4px; font-size:10px; cursor:pointer;">
                        🔄 Load Shift Crew
                    </button>
                </div>
            </div>

            <!-- Live Muster Roll Call Table -->
            <div style="max-height:160px; overflow-y:auto; border:1px solid #1e293b; border-radius:6px;">
                <table style="width:100%; border-collapse:collapse; text-align:left; font-size:11px;">
                    <thead>
                        <tr style="background:#1e293b; color:#94a3b8;">
                            <th style="padding:6px 8px;">Token / Name</th>
                            <th style="padding:6px 8px;">Role</th>
                            <th style="padding:6px 8px;">Assigned Pit Sector</th>
                            <th style="padding:6px 8px;">Status</th>
                            <th style="padding:6px 8px; text-align:right;">Roll Call Action</th>
                        </tr>
                    </thead>
                    <tbody id="muster-table-body">
                        <!-- Dynamic Records -->
                    </tbody>
                </table>
            </div>
        `;

        container.appendChild(card);
        initMusterData();
    }

    function getMusterStore() {
        var raw = localStorage.getItem('dgms_muster_crew');
        if (!raw) return null;
        try { return JSON.parse(raw); } catch(e) { return null; }
    }

    function saveMusterStore(data) {
        localStorage.setItem('dgms_muster_crew', JSON.stringify(data));
        renderMusterTable();
    }

    function initMusterData() {
        var crew = getMusterStore();
        if (!crew || crew.length === 0) {
            crew = [
                { id: 'TK-101', name: 'R. K. Soren (TK-101)', craft: 'Overman / Sirdar', zone: 'Face-1 Development Drift', status: 'Underground', time: '08:15 AM' },
                { id: 'TK-104', name: 'Manish Oraon (TK-104)', craft: 'SDL/LHD Operator', zone: 'Face-1 Development Drift', status: 'Underground', time: '08:20 AM' },
                { id: 'TK-112', name: 'Subodh Kumar (TK-112)', craft: 'Drill Operator / Blaster', zone: 'Depillaring District A', status: 'Underground', time: '08:30 AM' },
                { id: 'TK-118', name: 'Birender Mahato (TK-118)', craft: 'Support Timberman', zone: 'Face-1 Development Drift', status: 'Surface Safe', time: '11:45 AM' },
                { id: 'TK-125', name: 'P. Beck (TK-125)', craft: 'Underground Electrician', zone: 'Haulage Engine Pit', status: 'Underground', time: '09:10 AM' }
            ];
            saveMusterStore(crew);
        } else {
            renderMusterTable();
        }
    }

    window.addMusterWorker = function(e) {
        if (e) e.preventDefault();
        var name = document.getElementById('worker-name').value.trim();
        var craft = document.getElementById('worker-craft').value;
        var zone = document.getElementById('worker-zone').value;
        if (!name) return;

        var crew = getMusterStore() || [];
        var id = 'TK-' + Math.floor(100 + Math.random() * 900);
        var time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

        crew.unshift({
            id: id,
            name: name,
            craft: craft,
            zone: zone,
            status: 'Underground',
            time: time
        });

        saveMusterStore(crew);
        document.getElementById('worker-name').value = '';
    };

    window.toggleMusterStatus = function(idx) {
        var crew = getMusterStore() || [];
        if (!crew[idx]) return;
        crew[idx].status = (crew[idx].status === 'Underground') ? 'Surface Safe' : 'Underground';
        crew[idx].time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        saveMusterStore(crew);
    };

    window.evacuateAllPersonnel = function() {
        var crew = getMusterStore() || [];
        var time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        crew.forEach(function(m) {
            m.status = 'Surface Safe';
            m.time = time;
        });
        saveMusterStore(crew);
        alert('🟢 ALL CREW MARKED AS SURFACE SAFE - Pit Clear Confirmed for Rescue Team.');
    };

    window.resetDefaultShiftMuster = function() {
        localStorage.removeItem('dgms_muster_crew');
        initMusterData();
    };

    function renderMusterTable() {
        var tbody = document.getElementById('muster-table-body');
        if (!tbody) return;
        var crew = getMusterStore() || [];

        var total = crew.length;
        var inPit = 0;
        var safe = 0;

        tbody.innerHTML = crew.map(function(worker, idx) {
            var isUnderground = worker.status === 'Underground';
            if (isUnderground) inPit++; else safe++;

            var statusBadge = isUnderground 
                ? '<span style="background:rgba(239,68,68,0.2); color:#f87171; border:1px solid #ef4444; padding:2px 6px; border-radius:4px; font-weight:bold; font-size:10px;">⚠️ In Pit (' + worker.time + ')</span>'
                : '<span style="background:rgba(34,197,94,0.2); color:#4ade80; border:1px solid #22c55e; padding:2px 6px; border-radius:4px; font-weight:bold; font-size:10px;">✓ Surface Safe</span>';

            var actionBtn = isUnderground
                ? '<button type="button" onclick="toggleMusterStatus(' + idx + ')" style="background:#15803d; color:#fff; border:none; padding:3px 8px; border-radius:4px; font-size:10px; cursor:pointer;">Mark Surface</button>'
                : '<button type="button" onclick="toggleMusterStatus(' + idx + ')" style="background:#334155; color:#94a3b8; border:none; padding:3px 8px; border-radius:4px; font-size:10px; cursor:pointer;">Re-enter Pit</button>';

            return `
                <tr style="border-bottom:1px solid #1e293b; background:#020617;">
                    <td style="padding:6px 8px; font-weight:bold; color:#e2e8f0;">${worker.name}</td>
                    <td style="padding:6px 8px; color:#94a3b8;">${worker.craft}</td>
                    <td style="padding:6px 8px; color:#38bdf8;">${worker.zone}</td>
                    <td style="padding:6px 8px;">${statusBadge}</td>
                    <td style="padding:6px 8px; text-align:right;">${actionBtn}</td>
                </tr>
            `;
        }).join('');

        var tEl = document.getElementById('stat-total');
        var uEl = document.getElementById('stat-underground');
        var sEl = document.getElementById('stat-safe');
        if (tEl) tEl.innerText = 'Total: ' + total;
        if (uEl) uEl.innerText = 'Pit: ' + inPit;
        if (sEl) sEl.innerText = 'Surface: ' + safe;
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', injectMusterUI);
    } else {
        injectMusterUI();
    }
    setTimeout(injectMusterUI, 1600);
})();
</script>
"""
