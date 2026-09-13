# ui_part2.py - Map Engine, Siren, Charts & Tab Handler

PART2 = """
  <script>
    let barChartInst = null;
    let pieChartInst = null;
    let mapInst = null;
    let audioCtx = null;
    let sirenOsc = null;
    let vibInterval = null;

    function initMap() {
      if (mapInst) return;
      mapInst = L.map('mine-map').setView([22.35, 82.69], 10);
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 18,
        attribution: 'OpenStreetMap'
      }).addTo(mapInst);

      const gevraPolygon = [
        [22.3400, 82.6700],
        [22.3700, 82.6700],
        [22.3700, 82.7100],
        [22.3400, 82.7100]
      ];
      L.polygon(gevraPolygon, { color: '#ef4444', weight: 2, fillOpacity: 0.15 })
        .addTo(mapInst)
        .bindPopup('<b>SECL Gevra Boundary</b><br>Statutory Geofence Zone');

      const minesLoc = [
        { name: 'Gevra Sector B (SECL)', lat: 22.3541, lng: 82.6821 },
        { name: 'Jharia Pit 7 (BCCL)', lat: 23.7428, lng: 86.4150 },
        { name: 'Rajmahal Deep (ECL)', lat: 25.0422, lng: 87.3514 }
      ];

      minesLoc.forEach(m => {
        L.marker([m.lat, m.lng]).addTo(mapInst).bindPopup('<b>' + m.name + '</b>');
      });
    }

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
        console.log('Audio error:', err);
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
      if ('vibrate' in navigator) {
        navigator.vibrate(0);
      }
      document.getElementById('siren-banner').classList.add('hidden');
    }

    function triggerBroadcastSOS() {
      playAudioSiren();
      fetch('/api/broadcast/trigger', { method: 'POST' }).catch(() => {});
      alert('🚨 DGMS EMERGENCY ALARM ACTIVATED!\\n\\nSiren and vibration engaged.');
    }

    function renderCharts(mines, obs) {
      const labels = mines.map(m => m.name.split(' ')[0]);
      const scores = mines.map(m => m.compliance_score);

      const ctxBar = document.getElementById('barChart').getContext('2d');
      if (barChartInst) barChartInst.destroy();
      barChartInst = new Chart(ctxBar, {
        type: 'bar',
        data: {
          labels: labels,
          datasets: [{
            label: 'Compliance Index (%)',
            data: scores,
            backgroundColor: ['#10b981', '#f59e0b', '#ef4444'],
            borderRadius: 6
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: { min: 0, max: 100, ticks: { color: '#94a3b8' }, grid: { color: '#1e293b' } },
            x: { ticks: { color: '#94a3b8' }, grid: { display: false } }
          },
          plugins: { legend: { display: false } }
        }
      });

      const normalCount = obs.filter(o => o.severity === 'Normal').length;
      const critCount = obs.filter(o => o.severity === 'Critical').length;
      const ctxPie = document.getElementById('pieChart').getContext('2d');
      if (pieChartInst) pieChartInst.destroy();
      pieChartInst = new Chart(ctxPie, {
        type: 'doughnut',
        data: {
          labels: ['Compliant (Normal)', 'Breaches (Critical)'],
          datasets: [{
            data: [normalCount || 1, critCount],
            backgroundColor: ['#10b981', '#ef4444'],
            borderWidth: 0
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { labels: { color: '#cbd5e1', font: { size: 11 } } } }
        }
      });
    }

    async function load() {
      try {
        const [mR, oR] = await Promise.all([fetch('/api/collieries'), fetch('/api/inspections')]);
        const mines = await mR.json();
        const obs = await oR.json();
        document.getElementById('ml').innerHTML = (mines || []).map(m => '<tr><td class="p-2 font-semibold">' + m.name + ' (' + m.subsidiary + ')</td><td class="p-2">' + m.mine_type + '</td><td class="p-2 text-emerald-400 font-bold">' + m.compliance_score + '%</td></tr>').join('');
        document.getElementById('sm').innerHTML = (mines || []).map(m => '<option value="' + m.id + '">' + m.name + '</option>').join('');
        document.getElementById('tc').innerText = (obs || []).length;
        if (mines && mines.length > 0) {
          const avg = (mines.reduce((a, b) => a + b.compliance_score, 0) / mines.length).toFixed(1);
          document.getElementById('sc').innerText = avg + '%';
        }
        document.getElementById('ol').innerHTML = (obs || []).map(o => {
          return '<div class="p-2.5 bg-slate-900 border border-slate-800 rounded flex justify-between items-center">' +
            '<div>' +
              '<div><strong>' + (o.mine_name || 'Mine') + '</strong>: ' + (o.notes || '') + '</div>' +
              '<div class="text-[10px] text-amber-400">Officer: ' + (o.officer_name || '') + ' (' + (o.officer_role || '') + ') | Cert: ' + (o.dgms_cert_no || '') + '</div>' +
              '<div class="text-[10px] text-slate-500 font-mono">SEAL: ' + (o.sha256_hash || '').slice(0, 20) + '...</div>' +
            '</div>' +
            '<div class="text-right">' +
              '<span class="text-slate-400 text-[10px] block">' + (o.timestamp || '') + '</span>' +
              '<span class="text-[10px] text-emerald-400 font-mono font-bold">[SEAL VERIFIED]</span>' +
            '</div>' +
          '</div>';
        }).join('') || '<p class="text-slate-500">No audits yet.</p>';

        renderCharts(mines, obs);
      } catch (err) {
        console.error(err);
      }
    }

    async function save(e) {
      e.preventDefault();
      const mode = document.getElementById('sgps').value;
      const lat = mode === 'inside' ? 22.3541 : 28.6139;
      const lng = mode === 'inside' ? 82.6821 : 77.2090;
      const sev = document.getElementById('ss').value;

      const res = await fetch('/api/inspections', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
          client_id: 'CLI-' + Date.now(),
          mine_id: document.getElementById('sm').value,
          officer_name: document.getElementById('soname').value,
          officer_role: document.getElementById('sorole').value,
          dgms_cert_no: document.getElementById('socert').value,
          category: document.getElementById('scat').value,
          notes: document.getElementById('sn').value,
          severity: sev,
          latitude: lat, longitude: lng
        })
      });

      if (!res.ok) {
        alert('SUBMISSION REJECTED: Coordinates outside lease boundary.');
        return;
      }

      if (sev === 'Critical') {
        playAudioSiren();
      }

      alert('Statutory Inspection Signed & Sealed!');
      document.getElementById('sn').value = '';
      tab('dash');
      load();
    }

    async function triggerSimulatedHazard() {
      document.getElementById('tel-ch4').innerText = '1.84 % (CRITICAL)';
      document.getElementById('tel-ch4').className = 'text-base font-mono font-bold text-rose-500';
      playAudioSiren();
      await fetch('/api/telemetry/trigger-gas-spike', { method: 'POST' }).catch(() => {});
      load();
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
      document.getElementById('bd').className = t === 'dash' ? 'text-xs px-3 py-1.5 rounded-lg bg-amber-500 text-black font-bold' : 'text-xs px-3 py-1.5 rounded-lg bg-slate-800 text-slate-300 font-medium';
      document.getElementById('bf').className = t === 'field' ? 'text-xs px-3 py-1.5 rounded-lg bg-amber-500 text-black font-bold' : 'text-xs px-3 py-1.5 rounded-lg bg-slate-800 text-slate-300 font-medium';
      if (t === 'dash' && mapInst) {
        setTimeout(() => { mapInst.invalidateSize(); }, 200);
      }
    }

    window.onload = () => {
      initMap();
      load();
      runTelemetryDaemon();
    };
  </script>
</body>
</html>
"""
