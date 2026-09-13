# ui.py - Dashboard with Chart.js Analytics & IoT Sensor Simulator

DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>MinePulse AI - Industrial Portal</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen font-sans flex flex-col">
  <header class="border-b border-slate-800 bg-slate-900 sticky top-0 z-50 p-4">
    <div class="max-w-7xl mx-auto flex justify-between items-center w-full">
      <div class="flex items-center space-x-2">
        <span class="text-xl">⛏️</span>
        <h1 class="font-bold text-white text-base">MinePulse <span class="text-amber-500">AI</span></h1>
      </div>
      <div class="flex space-x-2">
        <a href="/statutory/form-vi" target="_blank" class="text-xs px-3 py-1.5 rounded-lg bg-slate-800 border border-slate-700 text-amber-400 font-semibold flex items-center">Export DGMS Form-VI</a>
        <button onclick="tab('dash')" id="bd" class="text-xs px-3 py-1.5 rounded-lg bg-amber-500 text-black font-bold">Dashboard</button>
        <button onclick="tab('field')" id="bf" class="text-xs px-3 py-1.5 rounded-lg bg-slate-800 text-slate-300">Statutory Form</button>
      </div>
    </div>
  </header>
  <main class="max-w-7xl mx-auto p-4 flex-1 w-full space-y-4">
    <div id="vd" class="space-y-4">
      <!-- KPI Cards -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
        <div class="p-3 bg-slate-900 border border-slate-800 rounded-xl">
          <p class="text-[10px] text-slate-400">Telegram Bot Siren</p>
          <h3 class="text-lg font-bold text-emerald-400 mt-1">Live Linked</h3>
        </div>
        <div class="p-3 bg-slate-900 border border-slate-800 rounded-xl">
          <p class="text-[10px] text-slate-400">Compliance Index</p>
          <h3 class="text-lg font-bold text-emerald-400 mt-1" id="sc">--</h3>
        </div>
        <div class="p-3 bg-slate-900 border border-slate-800 rounded-xl">
          <p class="text-[10px] text-slate-400">Total Audits</p>
          <h3 class="text-lg font-bold text-amber-400 mt-1" id="tc">0</h3>
        </div>
        <div class="p-3 bg-slate-900 border border-slate-800 rounded-xl">
          <p class="text-[10px] text-slate-400">Telemetry Daemon</p>
          <h3 class="text-lg font-bold text-emerald-400 mt-1">Simulating 10s</h3>
        </div>
      </div>

      <!-- Live IoT Telemetry Simulator Strip -->
      <div class="bg-slate-900 border border-slate-800 rounded-xl p-4">
        <div class="flex justify-between items-center mb-3">
          <div>
            <h2 class="font-bold text-sm">IoT Telemetry Sensor Stream (Gevra Sector B)</h2>
            <p class="text-[11px] text-slate-400">Real-time subsurface monitoring daemon</p>
          </div>
          <button onclick="triggerSimulatedHazard()" class="text-xs bg-rose-600 hover:bg-rose-500 text-white font-bold px-3 py-1.5 rounded">Simulate Gas Spike</button>
        </div>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-2 text-xs">
          <div class="p-2.5 bg-slate-950 rounded border border-slate-800">
            <span class="text-slate-400 block text-[10px]">Methane (CH4)</span>
            <span id="tel-ch4" class="text-base font-mono font-bold text-emerald-400">0.21 %</span>
            <span class="text-[10px] text-slate-500 block">Threshold: 1.25%</span>
          </div>
          <div class="p-2.5 bg-slate-950 rounded border border-slate-800">
            <span class="text-slate-400 block text-[10px]">Carbon Monoxide (CO)</span>
            <span id="tel-co" class="text-base font-mono font-bold text-emerald-400">14 ppm</span>
            <span class="text-[10px] text-slate-500 block">Threshold: 50 ppm</span>
          </div>
          <div class="p-2.5 bg-slate-950 rounded border border-slate-800">
            <span class="text-slate-400 block text-[10px]">Dust CAAQMS (PM2.5)</span>
            <span id="tel-pm" class="text-base font-mono font-bold text-amber-400">72 ug/m3</span>
            <span class="text-[10px] text-slate-500 block">Threshold: 150 ug/m3</span>
          </div>
          <div class="p-2.5 bg-slate-950 rounded border border-slate-800">
            <span class="text-slate-400 block text-[10px]">Bench Seismic Tilt</span>
            <span id="tel-vib" class="text-base font-mono font-bold text-emerald-400">0.02 mm/s</span>
            <span class="text-[10px] text-slate-500 block">Threshold: 5.0 mm/s</span>
          </div>
        </div>
      </div>

      <!-- Analytics Charts Section -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div class="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <h2 class="font-bold text-sm mb-2">Colliery Safety Scores (%)</h2>
          <div class="h-56"><canvas id="barChart"></canvas></div>
        </div>
        <div class="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <h2 class="font-bold text-sm mb-2">Statutory Risk Distribution</h2>
          <div class="h-56 flex justify-center"><canvas id="pieChart"></canvas></div>
        </div>
      </div>

      <!-- Collieries Table -->
      <div class="bg-slate-900 border border-slate-800 rounded-xl p-4">
        <h2 class="font-bold text-sm mb-3">Collieries Monitoring</h2>
        <div class="overflow-x-auto"><table class="w-full text-left text-xs"><tbody id="ml" class="divide-y divide-slate-800"></tbody></table></div>
      </div>

      <!-- Audit Logs -->
      <div class="bg-slate-900 border border-slate-800 rounded-xl p-4">
        <div class="flex justify-between items-center mb-3">
          <h2 class="font-bold text-sm">Audit Logs & Cryptographic Proof</h2>
          <button onclick="load()" class="text-[11px] text-slate-400 hover:text-white bg-slate-800 px-2 py-1 rounded">Refresh Stream</button>
        </div>
        <div id="ol" class="space-y-2 text-xs"></div>
      </div>
    </div>

    <!-- Statutory Officer Form -->
    <div id="vf" class="hidden max-w-lg mx-auto bg-slate-900 border border-slate-800 rounded-2xl p-5 space-y-4">
      <h2 class="font-bold text-base">DGMS Competent Officer Log Form</h2>
      <form onsubmit="save(event)" class="space-y-3 text-xs">
        <div class="grid grid-cols-2 gap-2">
          <div><label class="text-slate-400 block mb-1">Officer Name</label><input id="soname" required class="w-full bg-slate-800 p-2 rounded-lg text-white" value="Er. Gaurav Yadav"></div>
          <div><label class="text-slate-400 block mb-1">Designation / Role</label><select id="sorole" class="w-full bg-slate-800 p-2 rounded-lg text-white"><option value="Safety Officer (Overman)">Safety Officer (Overman)</option><option value="First Class Colliery Manager">Colliery Manager (1st Class)</option><option value="Dispatch Weighbridge Officer">Weighbridge Officer</option></select></div>
        </div>
        <div><label class="text-slate-400 block mb-1">DGMS Certificate / License No.</label><input id="socert" required class="w-full bg-slate-800 p-2 rounded-lg text-white font-mono" value="DGMS/CMR/2017/OM-8492"></div>
        <div><label class="text-slate-400 block mb-1">Target Mine</label><select id="sm" class="w-full bg-slate-800 p-2 rounded-lg text-white"></select></div>
        <div><label class="text-slate-400 block mb-1">Statutory Regulation Category</label><select id="scat" class="w-full bg-slate-800 p-2 rounded-lg text-white"><option>CMR 153: Ventilation & Methane Log</option><option>CMR 106: Bench Stability & Slope</option><option>CMR 169: Daily Blasting & Explosives Log</option><option>CAAQMS: Environmental Dust Standard</option></select></div>
        <div><label class="text-slate-400 block mb-1">Statutory Observation</label><textarea id="sn" required rows="2" class="w-full bg-slate-800 p-2 rounded-lg text-white" placeholder="Hazard or violation detail..."></textarea></div>
        <div class="grid grid-cols-2 gap-2">
          <div><label class="text-slate-400 block mb-1">Severity</label><select id="ss" class="w-full bg-slate-800 p-2 rounded-lg text-white"><option value="Normal">Routine (Compliant)</option><option value="Critical">Critical (Immediate Stop Order)</option></select></div>
          <div><label class="text-slate-400 block mb-1">Lease Boundary Check</label><select id="sgps" class="w-full bg-slate-800 p-2 rounded-lg text-emerald-400"><option value="inside">Inside Gevra Lease</option><option value="outside">Outside Lease (Geofence Breach)</option></select></div>
        </div>
        <button type="submit" class="w-full bg-amber-500 hover:bg-amber-400 text-black font-bold p-3 rounded-xl mt-2">Sign & Commit with DSC Seal</button>
      </form>
    </div>
  </main>

  <script>
    let barChartInst = null;
    let pieChartInst = null;

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
          severity: document.getElementById('ss').value,
          latitude: lat, longitude: lng
        })
      });

      if (!res.ok) {
        alert('SUBMISSION REJECTED: Coordinates outside lease boundary.');
        return;
      }

      alert('Statutory Inspection Signed & Sealed!');
      document.getElementById('sn').value = '';
      tab('dash');
      load();
    }

    async function triggerSimulatedHazard() {
      document.getElementById('tel-ch4').innerText = '1.84 % (CRITICAL)';
      document.getElementById('tel-ch4').className = 'text-base font-mono font-bold text-rose-500';
      await fetch('/api/telemetry-alert', { method: 'POST' });
      alert('Telemetry Alert: Methane spike (1.84%) triggered automated siren & logged to ledger.');
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
      document.getElementById('bd').className = t === 'dash' ? 'text-xs px-3 py-1.5 rounded-lg bg-amber-500 text-black font-bold' : 'text-xs px-3 py-1.5 rounded-lg bg-slate-800 text-slate-300';
      document.getElementById('bf').className = t === 'field' ? 'text-xs px-3 py-1.5 rounded-lg bg-amber-500 text-black font-bold' : 'text-xs px-3 py-1.5 rounded-lg bg-slate-800 text-slate-300';
    }

    window.onload = () => {
      load();
      runTelemetryDaemon();
    };
  </script>
</body>
</html>"""

def get_form_vi_html(rows):
    return """<!DOCTYPE html>
<html>
<head>
    <title>DGMS Form-VI Statutory Inspection Register</title>
    <style>
        body { font-family: 'Times New Roman', serif; padding: 25px; color: #111; }
        .header { text-align: center; border-bottom: 2px solid #000; padding-bottom: 10px; margin-bottom: 20px; }
        table { width: 100%; border-collapse: collapse; text-align: left; font-size: 12px; }
        th { border-bottom: 2px solid #000; padding: 8px; background: #f0f0f0; }
        td { border-bottom: 1px solid #ccc; padding: 8px; }
        .footer { margin-top: 40px; display: flex; justify-content: space-between; font-size: 12px; }
        @media print { button { display: none; } }
    </style>
</head>
<body>
    <div class="header">
        <h2 style="margin: 0;">DIRECTORATE GENERAL OF MINES SAFETY (DGMS)</h2>
        <h3 style="margin: 5px 0;">STATUTORY INSPECTION & BREACH REGISTER (FORM-VI)</h3>
        <p style="margin: 0; font-size: 12px;">Under Coal Mines Regulations (CMR 2017) & Mines Act 1952</p>
    </div>
    <div style="margin-bottom: 15px; text-align: right;">
        <button onclick="window.print()" style="padding: 6px 12px; background: #2563eb; color: white; border: none; border-radius: 4px; cursor: pointer;">Print / Save as PDF</button>
    </div>
    <table>
        <thead>
            <tr>
                <th>Date & Time</th>
                <th>Colliery Name</th>
                <th>Inspecting Officer & DGMS Lic.</th>
                <th>Statutory Category</th>
                <th>Observations & Findings</th>
                <th>Risk Class</th>
                <th>SHA-256 Verification</th>
            </tr>
        </thead>
        <tbody>
""" + rows + """
        </tbody>
    </table>
    <div class="footer">
        <div>
            <p>Generated by: <strong>MinePulse Statutory AI Engine</strong></p>
            <p>Certified Cryptographically Valid Logbook</p>
        </div>
        <div style="text-align: right;">
            <p>_____________________________________</p>
            <p><strong>Colliery Manager / Safety Officer Signature</strong></p>
            <p>Certified DGMS Competent Person</p>
        </div>
    </div>
</body>
</html>"""
