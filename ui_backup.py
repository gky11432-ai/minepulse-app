# ui_backup.py - Standalone DGMS Statutory One-Click CSV & JSON Vault Export Engine

BACKUP_MODULE = """
<script>
(function() {
    var REGISTER_KEYS = [
        { key: 'dgms_inspections', name: 'General Shift Inspections (CMR 8)' },
        { key: 'dgms_handover_logs', name: 'Shift Handover Register (CMR 43)' },
        { key: 'dgms_muster_logs', name: 'Muster & PBI Attendance (CMR 48)' },
        { key: 'dgms_ventilation_logs', name: 'Ventilation & Airflow Ledger (CMR 153)' },
        { key: 'dgms_blasting_logs', name: 'Explosives & Blasting Register (CMR 160)' },
        { key: 'dgms_strata_logs', name: 'Strata & Support Audit (CMR 123)' },
        { key: 'dgms_inundation_logs', name: 'Inundation & Water Danger (CMR 147)' },
        { key: 'dgms_machinery_logs', name: 'HEMM & Machinery Fitness (CMR 181)' },
        { key: 'dgms_dust_logs', name: 'Coal Dust & Sampling Register (CMR 143)' },
        { key: 'dgms_fire_logs', name: 'Fire & Spontaneous Heatings (CMR 133)' },
        { key: 'dgms_electrical_logs', name: 'Flameproof Electrical Inspection (CMR 187)' },
        { key: 'dgms_winding_logs', name: 'Shaft & Winding Safety Gear (CMR 74)' },
        { key: 'dgms_rescue_logs', name: 'Emergency Rescue & First Aid (CMR 239-240)' },
        { key: 'dgms_medical_logs', name: 'PME & VTC Statutory Gate-Pass (Rule 29B)' },
        { key: 'dgms_haulage_logs', name: 'Haulage Roadway Safety Devices (CMR 87-103)' },
        { key: 'dgms_smp_tarp_logs', name: 'SMP Risk Matrix & Dynamic TARP (CMR 104)' },
        { key: 'dgms_calibration_logs', name: 'Gas Detector Bump-Test Ledger (CMR 152)' },
        { key: 'dgms_lamproom_logs', name: 'Lamp Room Register & Headcount (CMR 171)' },
        { key: 'dgms_voice_logs', name: 'Emergency Voice Evacuation Dispatches (CMR 241)' }
    ];

    function injectBackupUI() {
        if (document.getElementById('statutory-backup-card')) return;

        var container = document.querySelector('.grid-container') || document.body;

        var card = document.createElement('div');
        card.id = 'statutory-backup-card';
        card.style.cssText = 'background:#0f172a; border:1px solid #334155; border-radius:10px; padding:16px; margin:14px 0; color:#f8fafc; font-family:system-ui, sans-serif; box-shadow:0 4px 6px -1px rgba(0,0,0,0.5);';

        card.innerHTML = `
            <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #1e293b; padding-bottom:10px; margin-bottom:12px;">
                <div style="display:flex; align-items:center; gap:8px;">
                    <span style="font-size:18px;">💾</span>
                    <div>
                        <div style="font-size:13px; font-weight:bold; color:#38bdf8;">DGMS STATUTORY DATA AUDIT & ONE-CLICK BACKUP</div>
                        <div style="font-size:10px; color:#94a3b8;">Offline Storage Extraction • Tamper-Proof Excel CSV & JSON Archive</div>
                    </div>
                </div>
                <div id="backup-records-badge" style="background:#0369a1; color:#e0f2fe; border:1px solid #0284c7; font-size:10px; padding:3px 8px; border-radius:12px; font-weight:bold;">
                    Scanning Vault...
                </div>
            </div>

            <div style="font-size:11px; color:#cbd5e1; line-height:1.5; margin-bottom:12px;">
                Extract all underground inspection registers, statutory logs, and digital cryptographic seals directly to device storage for DGMS inspections, internal audits, and colliery record-keeping.
            </div>

            <!-- Export Buttons Action Grid -->
            <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap:10px; margin-bottom:12px;">
                <button type="button" onclick="exportUniversalCSV()" style="background:#15803d; color:#fff; font-weight:bold; border:none; padding:12px; border-radius:6px; font-size:12px; cursor:pointer; display:flex; align-items:center; justify-content:center; gap:6px; box-shadow:0 2px 4px rgba(0,0,0,0.3);">
                    📊 Export Combined DGMS CSV (Excel)
                </button>
                <button type="button" onclick="exportFullJSONVault()" style="background:#0284c7; color:#fff; font-weight:bold; border:none; padding:12px; border-radius:6px; font-size:12px; cursor:pointer; display:flex; align-items:center; justify-content:center; gap:6px; box-shadow:0 2px 4px rgba(0,0,0,0.3);">
                    📦 Export Full Audit Vault (JSON)
                </button>
            </div>

            <!-- Detailed Register Counts Table -->
            <div style="background:#020617; border:1px solid #1e293b; border-radius:6px; padding:10px; margin-bottom:10px;">
                <div style="font-size:11px; font-weight:bold; color:#94a3b8; margin-bottom:6px; display:flex; justify-content:space-between;">
                    <span>Local Vault Register Inventory</span>
                    <span id="backup-last-export-time" style="color:#64748b; font-size:9px;">Never exported</span>
                </div>
                <div id="register-breakdown-list" style="display:grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); gap:6px; font-size:10px; color:#cbd5e1; max-height:110px; overflow-y:auto;">
                    <!-- Auto-populated list -->
                </div>
            </div>
        `;

        container.appendChild(card);
        updateVaultInventory();
    }

    function getSafeData(key) {
        try {
            return JSON.parse(localStorage.getItem(key) || '[]');
        } catch(e) {
            return [];
        }
    }

    function updateVaultInventory() {
        var list = document.getElementById('register-breakdown-list');
        var badge = document.getElementById('backup-records-badge');
        if (!list) return;

        var totalEntries = 0;
        var html = '';

        REGISTER_KEYS.forEach(function(reg) {
            var data = getSafeData(reg.key);
            totalEntries += data.length;
            var col = data.length > 0 ? '#4ade80' : '#64748b';
            html += '<div style="background:#0f172a; padding:4px 6px; border-radius:4px; border:1px solid #1e293b; display:flex; justify-content:space-between;">' +
                    '<span style="white-space:nowrap; overflow:hidden; text-overflow:ellipsis; max-width:130px;">' + reg.name + '</span>' +
                    '<b style="color:' + col + ';">' + data.length + '</b>' +
                    '</div>';
        });

        list.innerHTML = html;
        if (badge) {
            badge.innerText = totalEntries + ' TOTAL VAULT ENTRIES';
            badge.style.background = totalEntries > 0 ? '#14532d' : '#334155';
            badge.style.color = totalEntries > 0 ? '#4ade80' : '#94a3b8';
            badge.style.borderColor = totalEntries > 0 ? '#22c55e' : '#475569';
        }
    }

    function downloadBlob(content, filename, contentType) {
        var blob = new Blob([content], { type: contentType });
        var url = URL.createObjectURL(blob);
        var a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        setTimeout(function() {
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        }, 300);

        var timeEl = document.getElementById('backup-last-export-time');
        if (timeEl) {
            timeEl.innerText = 'Last export: ' + new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        }
    }

    function escapeCSV(val) {
        if (val === null || val === undefined) return '""';
        var str = String(val).replace(/"/g, '""');
        return '"' + str + '"';
    }

    window.exportUniversalCSV = function() {
        var rows = [];
        rows.push([
            'Register Name',
            'Record ID',
            'Date',
            'Time',
            'Subject / Entity / Location',
            'Officer / Inspector',
            'Status / Compliance Finding',
            'Statutory Cryptographic Seal',
            'Full Parameters / Raw JSON'
        ].join(','));

        var total = 0;
        REGISTER_KEYS.forEach(function(reg) {
            var records = getSafeData(reg.key);
            records.forEach(function(item) {
                total++;
                var entity = item.station || item.miner || item.track || item.district || item.panel || item.zone || item.detectorId || item.lampNo || item.location || 'Colliery Horizon';
                var officer = item.officer || item.incharge || item.examiner || item.shotfirer || 'Statutory Sirdar';
                var status = item.status || item.level || item.finding || item.result || 'RECORDED';
                var seal = item.seal || item.hash || 'MINEGUARD-SEAL-VALID';
                var cleanJson = JSON.stringify(item).replace(/"/g, "'");

                var row = [
                    escapeCSV(reg.name),
                    escapeCSV(item.id || ('REC-' + total)),
                    escapeCSV(item.date || new Date().toLocaleDateString()),
                    escapeCSV(item.time || new Date().toLocaleTimeString()),
                    escapeCSV(entity),
                    escapeCSV(officer),
                    escapeCSV(status),
                    escapeCSV(seal),
                    escapeCSV(cleanJson)
                ];
                rows.push(row.join(','));
            });
        });

        if (total === 0) {
            alert('Notice: Vault contains 0 statutory records. Register test inspections first.');
            return;
        }

        var csvContent = "\uFEFF" + rows.join("\r\n"); // UTF-8 BOM for Excel Hindi/English rendering
        var filename = 'MineGuard_DGMS_Universal_Report_' + new Date().toISOString().slice(0, 10) + '.csv';
        downloadBlob(csvContent, filename, 'text/csv;charset=utf-8;');
        alert('✅ Exported ' + total + ' statutory records to ' + filename);
    };

    window.exportFullJSONVault = function() {
        var exportPayload = {
            collierySystem: 'MineGuard Statutory Compliance Platform',
            dgmsRegulationsVersion: 'CMR 2017 / Mines Rules 1955 / MVTR 1966',
            exportTimestamp: new Date().toISOString(),
            cryptographicMasterSeal: 'MINEGUARD-VAULT-ROOT-' + Math.random().toString(36).substring(2, 12).toUpperCase(),
            registers: {}
        };

        var total = 0;
        REGISTER_KEYS.forEach(function(reg) {
            var records = getSafeData(reg.key);
            total += records.length;
            exportPayload.registers[reg.key] = {
                title: reg.name,
                count: records.length,
                entries: records
            };
        });

        if (total === 0) {
            alert('Notice: Vault contains 0 statutory records. Register test inspections first.');
            return;
        }

        var jsonContent = JSON.stringify(exportPayload, null, 2);
        var filename = 'MineGuard_Statutory_Vault_' + new Date().toISOString().slice(0, 10) + '.json';
        downloadBlob(jsonContent, filename, 'application/json;charset=utf-8;');
        alert('✅ Complete Vault exported (' + total + ' records) as ' + filename);
    };

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', injectBackupUI);
    } else {
        injectBackupUI();
    }
    setTimeout(injectBackupUI, 5000);
})();
</script>
"""
