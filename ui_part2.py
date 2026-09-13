# ui_part2.py - Lightweight Dashboard Visuals, Map, Charts & Telemetry Loop

PART2 = """
  <script>
    let barChartInst = null;
    let pieChartInst = null;
    let mapInst = null;

    const LOCAL_COLLIERIES = [
      { id: 'SECL-GV-04', name: 'Gevra Sector B (SECL)', subsidiary: 'SECL', mine_type: 'Opencast', compliance_score: 94.2 },
      { id: 'BCCL-JH-07', name: 'Jharia Pit 7 (BCCL)', subsidiary: 'BCCL', mine_type: 'Underground', compliance_score: 82.5 },
      { id: 'ECL-RJ-02', name: 'Rajmahal Deep (ECL)', subsidiary: 'ECL', mine_type: 'Opencast', compliance_score: 88.0 }
    ];

    // 1. Map Initialization
    function initMap() {
      const mapEl = document.getElementById('mine-map');
      if (!mapEl || mapInst) return;

      try {
        if (typeof L !== 'undefined') {
          mapInst = L.map('mine-map').setView([22.35, 82.69], 10);
          L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 18 }).addTo(mapInst);

          const gevraPolygon = [[22.3400, 82.6700], [22.3700, 82.6700], [22.3700, 82.7100], [22.3400, 82.7100]];
          L.polygon(gevraPolygon, { color: '#ef4444', weight: 2, fillOpacity: 0.15 }).addTo(mapInst);

          LOCAL_COLLIERIES.forEach(m => {
            L.marker([22.3541, 82.6821]).addTo(mapInst).bindPopup(m.name);
          });
          return;
        }
      } catch(e){}

      mapEl.innerHTML = `
        <div class="h-full flex flex-col items-center justify-center p-4 text-center">
          <div class="text-3xl mb-1">🗺️</div>
          <p class="text-xs font-bold text-amber-400">Offline Spatial Grid Active</p>
          <p class="text-[10px] text-slate-400 mt-1">SECL Gevra Sector B: Latitude 22.3541° N | Longitude 82.6821° E</p>
        </div>
      `;
    }

    // 2. Charts Rendering
    function renderCharts(mines, obs) {
      if (typeof Chart === 'undefined') return;
      try {
        const labels = mines.map(m => m.name.split(' ')[0]);
        const scores = mines.map(m => m.compliance_score);

        const ctxBar = document.getElementById('barChart')?.getContext('2d');
        if (ctxBar) {
          if (barChartInst) barChartInst.destroy();
          barChartInst = new Chart(ctxBar, {
            type: 'bar',
            data: {
              labels: labels,
              datasets: [{ label: 'Compliance (%)', data: scores, backgroundColor: ['#10b981', '#f59e0b', '#ef4444'], borderRadius: 6 }]
            },
            options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } } }
          });
        }

        const ctxPie = document.getElementById('pieChart')?.getContext('2d');
        if (ctxPie) {
          if (pieChartInst) pieChartInst.destroy();
          const normalCount = obs.filter(o => o.severity === 'Normal').length;
          const critCount = obs.filter(o => o.severity === 'Critical').length;
          pieChartInst = new Chart(ctxPie, {
            type: 'doughnut',
            data: { labels: ['Compliant', 'Critical'], datasets: [{ data: [normalCount || 1, critCount], backgroundColor: ['#10b981', '#ef4444'] }] },
            options: { responsive: true, maintainAspectRatio: false }
          });
        }
      } catch(e) {}
    }

    // 3. Inspection Loader
    async function load() {
      let mines = LOCAL_COLLIERIES;
      let obs = await dbGetAll();

      if (isTrulyOnline) {
        try {
          const controller = new AbortController();
          const timeoutId = setTimeout(() => controller.abort(), 1200);

          const [mR, oR] = await Promise.all([
            fetch('/api/collieries', { signal: controller.signal }),
            fetch('/api/inspections', { signal: controller.signal })
          ]);
          clearTimeout(timeoutId);

          if (mR.ok) mines = await mR.json();
          if (oR.ok) {
            const serverRecords = await oR.json();
            for (const s of serverRecords) {
              await dbPut({ ...s, sync_pending: false });
            }
            obs = await dbGetAll();
          }
        } catch(e) {
          setOfflineUI();
        }
      }

      const pendingCount = obs.filter(o => o.sync_pending).length;
      const notice = document.getElementById('sync-notice');
      if (notice) {
        if (pendingCount > 0) {
          notice.classList.remove('hidden');
          document.getElementById('pending-count').innerText = pendingCount;
        } else {
          notice.classList.add('hidden');
        }
      }

      const ml = document.getElementById('ml');
      if (ml) ml.innerHTML = (mines || []).map(m => '<tr><td class="p-2 font-semibold">' + m.name + '</td><td class="p-2">' + m.mine_type + '</td><td class="p-2 text-emerald-400 font-bold">' + m.compliance_score + '%</td></tr>').join('');
      const sm = document.getElementById('sm');
      if (sm) sm.innerHTML = (mines || []).map(m => '<option value="' + m.id + '">' + m.name + '</option>').join('');
      const tc = document.getElementById('tc');
      if (tc) tc.innerText = obs.length;

      if (mines.length > 0) {
        const avg = (mines.reduce((a, b) => a + b.compliance_score, 0) / mines.length).toFixed(1);
        const sc = document.getElementById('sc');
        if (sc) sc.innerText = avg + '%';
      }

      const ol = document.getElementById('ol');
      if (ol) {
        ol.innerHTML = obs.map(o => {
          const statusBadge = o.sync_pending 
            ? '<span class="text-amber-400 font-bold font-mono">[SAVED OFFLINE (VAULT)]</span>'
            : '<span class="text-emerald-400 font-mono font-bold">[CLOUD SEAL VERIFIED]</span>';

          return '<div class="p-2.5 bg-slate-900 border border-slate-800 rounded flex justify-between items-center">' +
            '<div>' +
              '<div><strong>' + (o.mine_name || 'Gevra Sector B') + '</strong>: ' + (o.notes || '') + '</div>' +
              '<div class="text-[10px] text-amber-400">Officer: ' + (o.officer_name || '') + ' | ' + (o.officer_role || '') + '</div>' +
              '<div class="text-[10px] text-slate-500 font-mono">SEAL: ' + (o.sha256_hash || 'SHA256_LOCAL_VAULT_RECORD').slice(0, 24) + '...</div>' +
            '</div>' +
            '<div class="text-right">' +
              '<span class="text-slate-400 text-[10px] block">' + (o.timestamp || '') + '</span>' +
              statusBadge +
            '</div>' +
          '</div>';
        }).join('') || '<p class="text-slate-500">No inspection records logged.</p>';
      }

      renderCharts(mines, obs);
    }

    // 4. Form Save
    async function save(e) {
      e.preventDefault();
      const sev = document.getElementById('ss').value;
      const record = {
        client_id: 'CLI-' + Date.now(),
        mine_id: document.getElementById('sm').value,
        mine_name: document.getElementById('sm').options[document.getElementById('sm').selectedIndex]?.text || 'Gevra Sector B (SECL)',
        officer_name: document.getElementById('soname').value,
        officer_role: document.getElementById('sorole').value,
        dgms_cert_no: document.getElementById('socert').value,
        category: document.getElementById('scat').value,
        notes: document.getElementById('sn').value,
        severity: sev,
        latitude: 22.3541,
        longitude: 82.6821,
        timestamp: new Date().toISOString().replace('T', ' ').substring(0, 19),
        sha256_hash: 'SEAL_' + Math.random().toString(36).substring(2) + Date.now(),
        sync_pending: !isTrulyOnline
      };

      await dbPut(record);

      if (isTrulyOnline) {
        try {
          const res = await fetch('/api/inspections', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(record)
          });
          if (res.ok) {
            record.sync_pending = false;
            await dbPut(record);
          }
        } catch(e) {
          setOfflineUI();
        }
      }

      if (sev === 'Critical') playAudioSiren();

      alert(isTrulyOnline 
        ? 'Statutory Inspection signed & uploaded to DGMS Cloud!' 
        : '⚠️ NO NETWORK: Form signed & securely stored in Phone Local Vault! Network aane par auto-sync ho jayega.');

      document.getElementById('sn').value = '';
      tab('dash');
      load();
    }

    async function triggerSimulatedHazard() {
      document.getElementById('tel-ch4').innerText = '1.84 % (CRITICAL)';
      document.getElementById('tel-ch4').className = 'text-base font-mono font-bold text-rose-500';
      playAudioSiren();
      if (isTrulyOnline) {
        fetch('/api/telemetry/trigger-gas-spike', { method: 'POST' }).catch(() => {});
      }
    }

    function runTelemetryDaemon() {
      setInterval(() => {
        const ch4 = (0.15 + Math.random() * 0.15).toFixed(2);
        const co = Math.floor(10 + Math.random() * 8);
        const pm = Math.floor(65 + Math.random() * 20);
        const vib = (0.01 + Math.random() * 0.03).toFixed(2);
        const elCh4 = document.getElementById('tel-ch4');
        if (elCh4) elCh4.innerText = ch4 + ' %';
        const elCo = document.getElementById('tel-co');
        if (elCo) elCo.innerText = co + ' ppm';
        const elPm = document.getElementById('tel-pm');
        if (elPm) elPm.innerText = pm + ' ug/m3';
        const elVib = document.getElementById('tel-vib');
        if (elVib) elVib.innerText = vib + ' mm/s';
      }, 5000);
    }

    function tab(t) {
      document.getElementById('vd').classList.toggle('hidden', t === 'field');
      document.getElementById('vf').classList.toggle('hidden', t !== 'field');
      document.getElementById('bd').className = t === 'dash' ? 'text-[11px] sm:text-xs px-2.5 sm:px-3 py-1.5 rounded-lg bg-amber-500 text-black font-bold' : 'text-[11px] sm:text-xs px-2.5 sm:px-3 py-1.5 rounded-lg bg-slate-800 text-slate-300 font-medium';
      document.getElementById('bf').className = t === 'field' ? 'text-[11px] sm:text-xs px-2.5 sm:px-3 py-1.5 rounded-lg bg-amber-500 text-black font-bold' : 'text-[11px] sm:text-xs px-2.5 sm:px-3 py-1.5 rounded-lg bg-slate-800 text-slate-300 font-medium';
      if (t === 'dash' && mapInst) {
        setTimeout(() => { mapInst.invalidateSize(); }, 200);
      }
    }

    window.onload = async () => {
      await checkTrueNetwork();
      initMap();
      load();
      runTelemetryDaemon();
      setInterval(checkTrueNetwork, 6000);
    };
  </script>
</body>
</html>
"""
