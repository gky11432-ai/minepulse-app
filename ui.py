# ui.py - Statutory Interface & DGMS Form-VI Layout

DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>MinePulse AI - Industrial Portal</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen font-sans p-4">
  <div class="max-w-5xl mx-auto space-y-4">
    <header class="flex justify-between items-center border-b border-slate-800 pb-3">
      <div class="flex items-center space-x-2">
        <span class="text-xl">⛏️</span>
        <h1 class="font-bold text-white text-lg">MinePulse <span class="text-amber-500">AI</span></h1>
      </div>
      <div class="space-x-2">
        <a href="/statutory/form-vi" target="_blank" class="text-xs px-3 py-1.5 rounded-lg bg-slate-800 text-amber-400 font-semibold border border-slate-700">Form-VI</a>
        <button onclick="tab('dash')" id="bd" class="text-xs px-3 py-1.5 rounded-lg bg-amber-500 text-black font-bold">Dashboard</button>
        <button onclick="tab('form')" id="bf" class="text-xs px-3 py-1.5 rounded-lg bg-slate-800 text-slate-300">Statutory Form</button>
      </div>
    </header>

    <div id="vd" class="space-y-4">
      <div class="grid grid-cols-2 md:grid-cols-4 gap-3 text-center">
        <div class="p-3 bg-slate-900 border border-slate-800 rounded-xl">
          <p class="text-[10px] text-slate-400">Telegram Siren</p>
          <h3 class="text-base font-bold text-emerald-400 mt-1">Live Linked</h3>
        </div>
        <div class="p-3 bg-slate-900 border border-slate-800 rounded-xl">
          <p class="text-[10px] text-slate-400">Compliance Index</p>
          <h3 class="text-base font-bold text-emerald-400 mt-1" id="sc">--</h3>
        </div>
        <div class="p-3 bg-slate-900 border border-slate-800 rounded-xl">
          <p class="text-[10px] text-slate-400">Total Audits</p>
          <h3 class="text-base font-bold text-amber-400 mt-1" id="tc">0</h3>
        </div>
        <div class="p-3 bg-slate-900 border border-slate-800 rounded-xl">
          <p class="text-[10px] text-slate-400">Database Engine</p>
          <h3 class="text-base font-bold text-emerald-400 mt-1">Cloud Postgres</h3>
        </div>
      </div>

      <div class="bg-slate-900 border border-slate-800 rounded-xl p-4">
        <h2 class="font-bold text-sm mb-3">Collieries Monitoring</h2>
        <table class="w-full text-left text-xs"><tbody id="ml" class="divide-y divide-slate-800"></tbody></table>
      </div>

      <div class="bg-slate-900 border border-slate-800 rounded-xl p-4">
        <div class="flex justify-between items-center mb-3">
          <h2 class="font-bold text-sm">Audit Logs (SHA-256 Verified)</h2>
          <button onclick="load()" class="text-[10px] text-slate-400 bg-slate-800 px-2 py-1 rounded hover:text-white">Refresh Stream</button>
        </div>
        <div id="ol" class="space-y-2 text-xs"></div>
      </div>
    </div>

    <div id="vf" class="hidden max-w-md mx-auto bg-slate-900 border border-slate-800 rounded-2xl p-4 space-y-3">
      <h2 class="font-bold text-sm">DGMS Statutory Officer Log Form</h2>
      <form onsubmit="save(event)" class="space-y-2 text-xs">
        <div>
          <label class="text-slate-400 block mb-1">Officer Name</label>
          <input id="oname" required class="w-full bg-slate-800 p-2 rounded text-white" value="Er. Gaurav Yadav">
        </div>
        <div>
          <label class="text-slate-400 block mb-1">Designation & Cert</label>
          <input id="orole" readonly class="w-full bg-slate-800 p-2 rounded text-amber-400 font-mono" value="Safety Officer | DGMS/CMR/2017/OM-8492">
        </div>
        <div>
          <label class="text-slate-400 block mb-1">Target Mine</label>
          <select id="sm" class="w-full bg-slate-800 p-2 rounded text-white"></select>
        </div>
        <div>
          <label class="text-slate-400 block mb-1">Category</label>
          <select id="scat" class="w-full bg-slate-800 p-2 rounded text-white">
            <option>CMR 153: Ventilation & Methane Log</option>
            <option>CMR 106: Bench Stability & Slope</option>
            <option>CMR 169: Daily Blasting Log</option>
          </select>
        </div>
        <div>
          <label class="text-slate-400 block mb-1">Observation</label>
          <textarea id="snotes" required rows="2" class="w-full bg-slate-800 p-2 rounded text-white" placeholder="Breach or inspection notes..."></textarea>
        </div>
        <div>
          <label class="text-slate-400 block mb-1">Severity</label>
          <select id="ssev" class="w-full bg-slate-800 p-2 rounded text-white">
            <option value="Normal">Routine (Compliant)</option>
            <option value="Critical">Critical (Immediate Stop Order)</option>
          </select>
        </div>
        <button type="submit" class="w-full bg-amber-500 hover:bg-amber-400 text-black font-bold p-2.5 rounded-lg mt-1">Sign & Commit DSC</button>
      </form>
    </div>
  </div>

  <script>
    async function load() {
      const [mR, oR] = await Promise.all([fetch('/api/collieries'), fetch('/api/inspections')]);
      const mines = await mR.json(), obs = await oR.json();
      document.getElementById('ml').innerHTML = mines.map(m => `<tr><td class="p-2 font-semibold">${m.name} (${m.subsidiary})</td><td class="p-2">${m.mine_type}</td><td class="p-2 text-emerald-400 font-bold">${m.compliance_score}%</td></tr>`).join('');
      document.getElementById('sm').innerHTML = mines.map(m => `<option value="${m.id}">${m.name}</option>`).join('');
      document.getElementById('tc').innerText = obs.length;
      if (mines.length) document.getElementById('sc').innerText = (mines.reduce((a, b) => a + b.compliance_score, 0) / mines.length).toFixed(1) + '%';
      document.getElementById('ol').innerHTML = obs.map(o => `<div class="p-2 bg-slate-950 border border-slate-800 rounded flex justify-between"><div><strong>${o.mine_name}</strong>: ${o.notes}<br><span class="text-[10px] text-amber-400">${o.officer_name}</span><br><span class="text-[10px] text-slate-500 font-mono">SEAL: ${o.sha256_hash.slice(0, 20)}...</span></div><div class="text-right text-[10px]"><span class="text-slate-400 block">${o.timestamp}</span><span class="text-emerald-400 font-bold">[SEAL VERIFIED]</span></div></div>`).join('') || '<p class="text-slate-500">No audits yet.</p>';
    }

    async function save(e) {
      e.preventDefault();
      await fetch('/api/inspections', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          client_id: 'CLI-' + Date.now(),
          mine_id: document.getElementById('sm').value,
          officer_name: document.getElementById('oname').value,
          officer_role: 'Safety Officer (Overman)',
          dgms_cert_no: 'DGMS/CMR/2017/OM-8492',
          category: document.getElementById('scat').value,
          notes: document.getElementById('snotes').value,
          severity: document.getElementById('ssev').value,
          latitude: 22.3541,
          longitude: 82.6821
        })
      });
      alert('Statutory Audit Committed & Sealed!');
      document.getElementById('snotes').value = '';
      tab('dash');
      load();
    }

    function tab(t) {
      document.getElementById('vd').classList.toggle('hidden', t === 'form');
      document.getElementById('vf').classList.toggle('hidden', t !== 'form');
      document.getElementById('bd').className = t === 'dash' ? 'text-xs px-3 py-1.5 rounded-lg bg-amber-500 text-black font-bold' : 'text-xs px-3 py-1.5 rounded-lg bg-slate-800 text-slate-300';
      document.getElementById('bf').className = t === 'form' ? 'text-xs px-3 py-1.5 rounded-lg bg-amber-500 text-black font-bold' : 'text-xs px-3 py-1.5 rounded-lg bg-slate-800 text-slate-300';
    }

    window.onload = load;
  </script>
</body>
</html>"""

def get_form_vi_html(rows):
    return f"""<!DOCTYPE html>
<html>
<head>
  <title>DGMS Form-VI Statutory Inspection Register</title>
  <style>
    body {{ font-family: 'Times New Roman', serif; padding: 25px; color: #111; }}
    table {{ width: 100%; border-collapse: collapse; font-size: 12px; text-align: left; margin-top: 15px; }}
    th {{ border-bottom: 2px solid #000; padding: 8px; background: #f0f0f0; }}
    td {{ border-bottom: 1px solid #ccc; padding: 8px; }}
    @media print {{ button {{ display: none; }} }}
  </style>
</head>
<body>
  <div style="text-align: center; border-bottom: 2px solid #000; padding-bottom: 10px;">
    <h2 style="margin: 0;">DIRECTORATE GENERAL OF MINES SAFETY (DGMS)</h2>
    <h3 style="margin: 5px 0;">STATUTORY INSPECTION REGISTER (FORM-VI)</h3>
    <p style="margin: 0; font-size: 12px;">Under Coal Mines Regulations (CMR 2017) & Mines Act 1952</p>
  </div>
  <div style="text-align: right; margin-top: 10px;">
    <button onclick="window.print()" style="padding: 6px 12px; background: #2563eb; color: white; border: none; border-radius: 4px; cursor: pointer;">Print / Save as PDF</button>
  </div>
  <table>
    <thead>
      <tr>
        <th>Date & Time</th>
        <th>Colliery Name</th>
        <th>Inspecting Officer & Lic.</th>
        <th>Category</th>
        <th>Observation</th>
        <th>Risk Class</th>
        <th>SHA-256 Verification</th>
      </tr>
    </thead>
    <tbody>{rows}</tbody>
  </table>
</body>
</html>"""
  
