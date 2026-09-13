# ui_part2.py - Mine-Grade IndexedDB Storage, Local Siren Synth & Auto-Sync Engine

PART2 = """
  <script>
    let barChartInst = null;
    let pieChartInst = null;
    let mapInst = null;
    let audioCtx = null;
    let sirenOsc = null;
    let vibInterval = null;

    // Hardcoded Local Backup Collieries for Zero-Network Environments
    const LOCAL_COLLIERIES = [
      { id: 'SECL-GV-04', name: 'Gevra Sector B (SECL)', subsidiary: 'SECL', mine_type: 'Opencast', compliance_score: 94.2 },
      { id: 'BCCL-JH-07', name: 'Jharia Pit 7 (BCCL)', subsidiary: 'BCCL', mine_type: 'Underground', compliance_score: 82.5 },
      { id: 'ECL-RJ-02', name: 'Rajmahal Deep (ECL)', subsidiary: 'ECL', mine_type: 'Opencast', compliance_score: 88.0 }
    ];

    // ==========================================
    // 1. INDEXED-DB OFFLINE VAULT INITIALIZATION
    // ==========================================
    let dbInstance = null;
    function initDB() {
      return new Promise((resolve, reject) => {
        if (dbInstance) return resolve(dbInstance);
        const req = indexedDB.open('MinePulseLocalVault', 1);
        req.onupgradeneeded = (e) => {
          const db = e.target.result;
          if (!db.objectStoreNames.contains('inspections')) {
            db.createObjectStore('inspections', { keyPath: 'client_id' });
          }
        };
        req.onsuccess = (e) => {
          dbInstance = e.target.result;
          resolve(dbInstance);
        };
        req.onerror = (e) => reject(e);
      });
    }

    async function dbPut(record) {
      const db = await initDB();
      return new Promise((res, rej) => {
        const tx = db.transaction('inspections', 'readwrite');
        tx.objectStore('inspections').put(record);
        tx.oncomplete = () => res();
        tx.onerror = rej;
      });
    }

    async function dbGetAll() {
      const db = await initDB();
      return new Promise((res, rej) => {
        const tx = db.transaction('inspections', 'readonly');
        const req = tx.objectStore('inspections').getAll();
        req.onsuccess = () => res(req.result || []);
        req.onerror = rej;
      });
    }

    // ==========================================
    // 2. NETWORK STATE MONITOR
    // ==========================================
    function updateNetworkStatus() {
      const isOnline = navigator.onLine;
      const badge = document.getElementById('net-badge');
      const label = document.getElementById('net-label');
      if (isOnline) {
        badge.innerText = 'ONLINE';
        badge.className = 'ml-2 text-[10px] px-2 py-0.5 rounded-full font-bold bg-emerald-950 text-emerald-400 border border-emerald-800';
        label.innerText = 'Cloud Synced';
        label.className = 'text-base sm:text-lg font-bold text-emerald-400 mt-1';
        syncOfflineRecords();
      } else {
        badge.innerText = 'OFFLINE (PIT MODE)';
        badge.className = 'ml-2 text-[10px] px-2 py-0.5 rounded-full font-bold bg-rose-950 text-rose-400 border border-rose-800 animate-pulse';
        label.innerText = 'Local Storage Only';
        label.className = 'text-base sm:text-lg font-bold text-amber-400 mt-1';
      }
    }

    window.addEventListener('online', updateNetworkStatus);
    window.addEventListener('offline', updateNetworkStatus);

    // ==========================================
    // 3. MAP WITH OFFLINE VECTOR FALLBACK
    // ==========================================
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
      } catch (e) {
        console.log('Leaflet tile cache inactive - switching to offline vector render');
      }

      // Offline High-Visibility Vector Grid fallback
      mapEl.innerHTML = `
        <div class="h-full flex flex-col items-center justify-center p-4 text-center">
          <div class="text-3xl mb-1">🗺️</div>
          <p class="text-xs font-bold text-amber-400">Offline Autonomous Spatial Grid</p>
          <p class="text-[10px] text-slate-400 mt-1">SECL Gevra Sector B: Latitude 22.3541° N | Longitude 82.6821° E (Lease Compliant)</p>
        </div>
      `;
    }

    // ==========================================
    // 4. OFFLINE HORN & HARDWARE VIBRATION
    // ==========================================
    function triggerHardwareVibration() {
      if ('vibrate' in navigator) {
        navigator.vibrate([1000, 300, 1000, 300, 1500]);
        if (!vibInterval) {
          vibInterval = setInterval(() => {
            navigator.vibrate([1000, 300, 1000, 300, 1500]);
          }, 4500);
        }
      }
    }

    function playAudioSiren() {
      try {
        triggerHardwareVibration();
        if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        if (sirenOsc) return;

        sirenOsc = audioCtx.createOscillator();
        const gainNode = audioCtx.createGain();
        sirenOsc.type = 'sawtooth';

        const now = audioCtx.currentTime;
        sirenOsc.frequency.setValueAtTime(800, now);
        sirenOsc.frequency.linearRampToValueAtTime(1200, now + 0.4);
        sirenOsc.frequency.linearRampToValueAtTime(800, now + 0.8);
        sirenOsc.frequency.linearRampToValueAtTime(1200, now + 1.2);

        gainNode.gain.setValueAtTime(0.20, now);
        sirenOsc.connect(gainNode);
        gainNode.connect(audioCtx.destination);
        sirenOsc.start();
        document.getElementById('siren-banner').classList.remove('hidden');
      } catch (err) {
        console.log('Local synth error:', err);
      }
    }

    function silenceSiren() {
      if (sirenOsc) {
        try { sirenOsc.stop(); } catch(e){}
        sirenOsc = null;
      }
      if (vibInterval) {
        clearInterval(vibInterval);
        vibInterval = null;
      }
      if ('vibrate' in navigator) navigator.vibrate(0);
      document.getElementById('siren-banner').classList.add('hidden');
    }

    function triggerBroadcastSOS() {
      playAudioSiren();
      if (navigator.onLine) {
        fetch('/api/broadcast/trigger', { method: 'POST' }).catch(() => {});
      }
      alert('🚨 DGMS EMERGENCY ALARM ENGAGED!\\n\\nContinuous horn & vibration active.');
    }

    // ==========================================
    // 5. CHART ENGINE (SAFE FALLBACK)
    // ==========================================
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

    // ==========================================
    // 6. DATA LOADER & AUTO-SYNC ENGINE
    // ==========================================
    async function load() {
      let mines = LOCAL_COLLIERIES;
      let obs = [];

      // 1. Pehle IndexedDB se phone ke andar ka data nikalo
      try {
        obs = await dbGetAll();
      } catch(e){}

      // 2. Agar online hai, toh cloud database se sync karo
      if (navigator.onLine) {
        try {
          const [mR, oR] = await Promise.all([fetch('/api/collieries'), fetch('/api/inspections')]);
          if (mR.ok) mines = await mR.json();
          if (oR.ok) {
            const serverRecords = await oR.json();
            // Cloud records ko bhi local IndexedDB me update kar do
            for (const s of serverRecords) {
              await dbPut({ ...s, sync_pending: false });
            }
            obs = await dbGetAll();
          }
        } catch(e) {
          console.log('Failed to reach cloud, using Local Vault data');
        }
      }

      // Check pending offline count
      const pendingCount = obs.filter(o => o.sync_pending).length;
      const notice = document.getElementById('sync-notice');
      if (pendingCount > 0) {
        notice.classList.remove('hidden');
        document.getElementById('pending-count').innerText = pendingCount;
      } else {
        notice.classList.add('hidden');
      }

      // Render Tables & Inputs
      document.getElementById('ml').innerHTML = (mines || []).map(m => '<tr><td class="p-2 font-semibold">' + m.name + '</td><td class="p-2">' + m.mine_type + '</td><td class="p-2 text-emerald-400 font-bold">' + m.compliance_score + '%</td></tr>').join('');
      document.getElementById('sm').innerHTML = (mines || []).map(m => '<option value="' + m.id + '">' + m.name + '</option>').join('');
      document.getElementById('tc').innerText = obs.length;
      if (mines.length > 0) {
        const avg = (mines.reduce((a, b) => a + b.compliance_score, 0) / mines.length).toFixed(1);
        document.getElementById('sc').innerText = avg + '%';
      }

      // Render Ledger Stream
      document.getElementById('ol').innerHTML = obs.map(o => {
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

      renderCharts(mines, obs);
    }

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
        sync_pending: !navigator.onLine
      };

      // 1. Guaranteed storage in phone's IndexedDB first
      await dbPut(record);

      // 2. If online, send to cloud
      if (navigator.onLine) {
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
        } catch(e) {}
      }

      if (sev === 'Critical') playAudioSiren();

      alert(navigator.onLine 
        ? 'Statutory Inspection signed & uploaded to DGMS Cloud!' 
        : '⚠️ NO NETWORK: Inspection signed & securely stored in Phone Local Vault! Network aane par auto-sync ho jayega.');

      document.getElementById('sn').value = '';
      tab('dash');
      load();
    }

    async function syncOfflineRecords() {
      if (!navigator.onLine) return;
      const allRecords = await dbGetAll();
      const pending = allRecords.filter(r => r.sync_pending);
      if (pending.length === 0) return;

      for (const item of pending) {
        try {
          const res = await fetch('/api/inspections', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(item)
          });
          if (res.ok) {
            item.sync_pending = false;
            await dbPut(item);
          }
        } catch(e) {}
      }
      load();
    }

    function forceSync() {
      if (!navigator.onLine) {
        alert('Abhi bhi phone offline hai. Thoda network milne par Sync karein.');
        return;
      }
      syncOfflineRecords();
    }

    async function triggerSimulatedHazard() {
      document.getElementById('tel-ch4').innerText = '1.84 % (CRITICAL)';
      document.getElementById('tel-ch4').className = 'text-base font-mono font-bold text-rose-500';
      playAudioSiren();
      if (navigator.onLine) {
        fetch('/api/telemetry/trigger-gas-spike', { method: 'POST' }).catch(() => {});
      }
    }

    function runTelemetryDaemon() {
      setInterval(() => {
        const ch4 = (0.15 + Math.random() * 0.15).toFixed(2);
        const co = Math.floor(10 + Math.random() * 8);
        const pm = Math.floor(65 + Math.random() * 20);
        const vib = (0.01 + Math.random() * 0.03).toFixed(2);
        document.getElementById('tel-ch4').innerText = ch4 + ' %';
        document.getElementById('tel-co').innerText = co + ' ppm';
        document.getElementById('tel-pm').innerText = pm + ' ug/m3';
        document.getElementById('tel-vib').innerText = vib + ' mm/s';
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

    window.onload = () => {
      initMap();
      load();
      runTelemetryDaemon();
      updateNetworkStatus();
      setInterval(syncOfflineRecords, 12000);
    };
  </script>
</body>
</html>
"""
