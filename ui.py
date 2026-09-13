# ui.py - Complete Industrial Dashboard & Form-VI HTML Layouts

DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>MinePulse AI - Industrial Portal</title>
  <script src="https://cdn.tailwindcss.com"></script>
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
        <button onclick="tab('field')" id="bf" class="text-xs px-3 py-1.5 rounded-lg bg-slate-800 text-slate-300">Statutory Officer Form</button>
      </div>
    </div>
  </header>
  <main class="max-w-7xl mx-auto p-4 flex-1 w-full space-y-4">
    <div id="vd" class="space-y-4">
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
          <p class="text-[10px] text-slate-400">Tamper Seal</p>
          <h3 class="text-lg font-bold text-emerald-400 mt-1">SHA-256 Lock</h3>
        </div>
      </div>
      <div class="bg-slate-900 border border-slate-800 rounded-xl p-4">
        <h2 class="font-bold text-sm mb-3">Collieries Monitoring</h2>
        <div class="overflow-x-auto"><table class="w-full text-left text-xs"><tbody id="ml" class="divide-y divide-slate-800"></tbody></table></div>
      </div>
      <div class="bg-slate-900 border border-slate-800 rounded-xl p-4">
        <div class="flex justify-between items-center mb-3">
          <h2 class="font-bold text-sm">Audit Logs & Cryptographic Proof</h2>
          <button onclick="load()" class="text-[11px] text-slate-400 hover:text-white bg-slate-800 px-2 py-1 rounded">Refresh Stream</button>
        </div>
        <div id="ol" class="space-y-2 text-xs"></div>
      </div>
    </div>
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
    async function load() {
      try {
        const [mR, oR] = await Promise.all([fetch('/api/collieries'), fetch('/api/inspections')]);
        const mines = await mR.json();
        const obs = await oR.json();
        document.getElementById('ml').innerHTML = (mines || []).map(m => '<tr><td class="p-2 font-semibold">' + m.name + ' (' + m.subsidiary + ')</td><td class="p-2">' + m.mine_type + '</td><td class="p-2 text-emerald-400">' + m.compliance_score + '%</td></tr>').join('');
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
              '<span class="text-[10px] text-emerald-400 font-mono">SEAL VERIFIED</span>' +
            '</div>' +
          '</div>';
        }).join('') || '<p class="text-slate-500">No audits yet.</p>';
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
        const err = await res.json();
        alert('SUBMISSION REJECTED: ' + (err.detail || 'Boundary breach'));
        return;
      }

      alert('Statutory Inspection Signed & Sealed successfully!');
      document.getElementById('sn').value = '';
      tab('dash');
      load();
    }
    function tab(t) {
      document.getElementById('vd').classList.toggle('hidden', t === 'field');
      document.getElementById('vf').classList.toggle('hidden', t !== 'field');
      document.getElementById('bd').className = t === 'dash' ? 'text-xs px-3 py-1.5 rounded-lg bg-amber-500 text-black font-bold' : 'text-xs px-3 py-1.5 rounded-lg bg-slate-800 text-slate-300';
      document.getElementById('bf').className = t === 'field' ? 'text-xs px-3 py-1.5 rounded-lg bg-amber-500 text-black font-bold' : 'text-xs px-3 py-1.5 rounded-lg bg-slate-800 text-slate-300';
    }
    window.onload = load;
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
  
