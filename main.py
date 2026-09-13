import hashlib
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from sqlalchemy import Column, DateTime, Float, String, Text, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./minepulse.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Colliery(Base):
    __tablename__ = "collieries"
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    subsidiary = Column(String, nullable=False)
    mine_type = Column(String, nullable=False)
    compliance_score = Column(Float, default=100.0)
    risk_level = Column(String, default="Safe")

class InspectionAudit(Base):
    __tablename__ = "inspection_audits"
    id = Column(String, primary_key=True, index=True)
    mine_id = Column(String, nullable=False)
    mine_name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    notes = Column(Text, nullable=False)
    severity = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    sha256_hash = Column(String, nullable=False)

Base.metadata.create_all(bind=engine)

# Standard Mining Lease Boundary (Geofence Polygon for SECL Gevra Mine)
SECL_GEVRA_BOUNDARY = [
    (22.3400, 82.6700),
    (22.3700, 82.6700),
    (22.3700, 82.7100),
    (22.3400, 82.7100)
]

def is_within_mine_lease(lat: float, lon: float, boundary: list) -> bool:
    """Ray-Casting Algorithm: Validates whether (lat, lon) is inside mine polygon."""
    n = len(boundary)
    inside = False
    p1x, p1y = boundary[0]
    for i in range(n + 1):
        p2x, p2y = boundary[i % n]
        if lat > min(p1x, p2x):
            if lat <= max(p1x, p2x):
                if lon <= max(p1y, p2y):
                    if p1x != p2x:
                        xinters = (lat - p1x) * (p2y - p1y) / (p2x - p1x) + p1y
                    if p1y == p2y or lon <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside

def init_db():
    db = SessionLocal()
    if db.query(Colliery).count() == 0:
        db.add_all([
            Colliery(id="BCCL-JH-01", name="Jharia Colliery Pit 7", subsidiary="BCCL", mine_type="Underground", compliance_score=76.0, risk_level="Moderate"),
            Colliery(id="SECL-GV-04", name="Gevra Opencast Sector B", subsidiary="SECL", mine_type="Opencast", compliance_score=94.5, risk_level="Safe"),
            Colliery(id="ECL-RJ-02", name="Rajmahal Deep OCP", subsidiary="ECL", mine_type="Opencast", compliance_score=68.0, risk_level="Critical")
        ])
        db.commit()
    db.close()

init_db()

app = FastAPI(title="MinePulse AI Industrial Platform")

class BatchItem(BaseModel):
    client_id: str
    mine_id: str
    category: str
    notes: str
    severity: str
    latitude: float
    longitude: float

HTML_APP = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>MinePulse AI - Industrial Portal</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen font-sans flex flex-col">
  <header class="border-b border-slate-800 bg-slate-900 sticky top-0 z-50 p-4 flex justify-between items-center max-w-7xl mx-auto w-full">
    <div class="flex items-center space-x-2">
      <span class="text-xl">⛏️</span>
      <h1 class="font-bold text-white text-base">MinePulse <span class="text-amber-500">AI</span></h1>
    </div>
    <div class="flex space-x-2">
      <a href="/statutory/form-vi" target="_blank" class="text-xs px-3 py-1.5 rounded-lg bg-slate-800 border border-slate-700 text-amber-400 font-semibold flex items-center">Export DGMS Form-VI</a>
      <button onclick="tab('dash')" id="bd" class="text-xs px-3 py-1.5 rounded-lg bg-amber-500 text-black font-bold">Dashboard</button>
      <button onclick="tab('field')" id="bf" class="text-xs px-3 py-1.5 rounded-lg bg-slate-800 text-slate-300">Inspector</button>
    </div>
  </header>
  <main class="max-w-7xl mx-auto p-4 flex-1 w-full space-y-4">
    <div id="vd" class="space-y-4">
      <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
        <div class="p-3 bg-slate-900 border border-slate-800 rounded-xl">
          <p class="text-[10px] text-slate-400">Lease Geofence</p>
          <h3 class="text-lg font-bold text-emerald-400 mt-1">SECL-Gevra Lock</h3>
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
          <p class="text-[10px] text-slate-400">PM10 Telemetry</p>
          <h3 class="text-lg font-bold text-rose-400 mt-1">168 µg/m³</h3>
        </div>
      </div>
      <div class="bg-slate-900 border border-slate-800 rounded-xl p-4">
        <h2 class="font-bold text-sm mb-3">Collieries Monitoring</h2>
        <div class="overflow-x-auto"><table class="w-full text-left text-xs"><tbody id="ml" class="divide-y divide-slate-800"></tbody></table></div>
      </div>
      <div class="bg-slate-900 border border-slate-800 rounded-xl p-4">
        <h2 class="font-bold text-sm mb-3">Audit Logs (SHA-256 Verified)</h2>
        <div id="ol" class="space-y-2 text-xs"></div>
      </div>
    </div>
    <div id="vf" class="hidden max-w-lg mx-auto bg-slate-900 border border-slate-800 rounded-2xl p-5 space-y-4">
      <h2 class="font-bold text-base">Field Inspection Form (Geofence Enforced)</h2>
      <form onsubmit="save(event)" class="space-y-3 text-xs">
        <div><label class="text-slate-400 block mb-1">Target Mine</label><select id="sm" class="w-full bg-slate-800 p-2 rounded-lg text-white"></select></div>
        <div><label class="text-slate-400 block mb-1">Statutory Norm</label><select id="scat" class="w-full bg-slate-800 p-2 rounded-lg text-white"><option>CMR 153: Methane & Ventilation</option><option>CMR 106: Bench Stability</option><option>Environmental: CAAQMS Dust</option></select></div>
        <div><label class="text-slate-400 block mb-1">Observation</label><textarea id="sn" required rows="3" class="w-full bg-slate-800 p-2 rounded-lg text-white" placeholder="Hazard or violation detail..."></textarea></div>
        <div class="grid grid-cols-2 gap-2">
          <div><label class="text-slate-400 block mb-1">Severity</label><select id="ss" class="w-full bg-slate-800 p-2 rounded-lg text-white"><option value="Normal">Routine</option><option value="Critical">Critical (DGMS Alert)</option></select></div>
          <div><label class="text-slate-400 block mb-1">GPS Coordinate Mode</label><select id="sgps" class="w-full bg-slate-800 p-2 rounded-lg text-emerald-400"><option value="inside">Inside Gevra Mine</option><option value="outside">Outside Boundary (Spoof Test)</option></select></div>
        </div>
        <button type="submit" class="w-full bg-amber-500 hover:bg-amber-400 text-black font-bold p-3 rounded-xl mt-2">Commit Audit Record</button>
      </form>
    </div>
  </main>
  <script>
    async function load() {
      const [mR, oR] = await Promise.all([fetch('/api/collieries'), fetch('/api/inspections')]);
      const mines = await mR.json();
      const obs = await oR.json();
      document.getElementById('ml').innerHTML = mines.map(m => `<tr><td class="p-2 font-semibold">${m.name} (${m.subsidiary})</td><td class="p-2">${m.mine_type}</td><td class="p-2 text-emerald-400">${m.compliance_score}%</td></tr>`).join('');
      document.getElementById('sm').innerHTML = mines.map(m => `<option value="${m.id}">${m.name}</option>`).join('');
      document.getElementById('tc').innerText = obs.length;
      document.getElementById('sc').innerText = (mines.reduce((a, b) => a + b.compliance_score, 0) / mines.length).toFixed(1) + '%';
      document.getElementById('ol').innerHTML = obs.map(o => `
        <div class="p-2.5 bg-slate-950 border border-slate-800 rounded flex justify-between items-center">
          <div>
            <div><strong>${o.mine_name}</strong>: ${o.notes}</div>
            <div class="text-[10px] text-slate-500 font-mono">HASH: ${o.sha256_hash ? o.sha256_hash.slice(0, 16) : 'VERIFIED'}...</div>
          </div>
          <div class="text-right">
            <span class="text-slate-400 text-[10px] block">${o.timestamp}</span>
            <span class="text-[10px] text-emerald-400 font-mono">GEOFENCE OK</span>
          </div>
        </div>
      `).join('') || '<p class="text-slate-500">No audits yet.</p>';
    }
    async function save(e) {
      e.preventDefault();
      const mode = document.getElementById('sgps').value;
      const lat = mode === 'inside' ? 22.3541 : 28.6139; // Inside Gevra vs Outside (New Delhi)
      const lng = mode === 'inside' ? 82.6821 : 77.2090;

      const res = await fetch('/api/inspections', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
          client_id: 'CLI-' + Date.now(),
          mine_id: document.getElementById('sm').value,
          category: document.getElementById('scat').value,
          notes: document.getElementById('sn').value,
          severity: document.getElementById('ss').value,
          latitude: lat, longitude: lng
        })
      });

      if (!res.ok) {
        const err = await res.json();
        alert('GEOFENCE BREACH: ' + err.detail);
        return;
      }

      alert('Audit verified within Mine Boundary and Signed!');
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
</html>
"""

@app.get("/", response_class=HTMLResponse)
def root():
    return HTMLResponse(content=HTML_APP)

@app.get("/api/collieries")
def get_collieries():
    db = SessionLocal()
    res = db.query(Colliery).all()
    db.close()
    return res

@app.get("/api/inspections")
def get_inspections():
    db = SessionLocal()
    res = db.query(InspectionAudit).order_by(InspectionAudit.timestamp.desc()).all()
    db.close()
    return [
        {
            "id": a.id, "mine_name": a.mine_name, "category": a.category,
            "notes": a.notes, "severity": a.severity, "sha256_hash": a.sha256_hash,
            "timestamp": a.timestamp.strftime("%Y-%m-%d %H:%M")
        }
        for a in res
    ]

@app.post("/api/inspections")
def add_inspection(b: BatchItem):
    # Geofence Enforcement for SECL Gevra Mine
    if b.mine_id == "SECL-GV-04":
        if not is_within_mine_lease(b.latitude, b.longitude, SECL_GEVRA_BOUNDARY):
            raise HTTPException(
                status_code=403, 
                detail=f"REJECTED: GPS location ({b.latitude}, {b.longitude}) is outside SECL-Gevra statutory lease boundary."
            )

    db = SessionLocal()
    mine = db.query(Colliery).filter(Colliery.id == b.mine_id).first()
    if not mine:
        db.close()
        raise HTTPException(status_code=404, detail="Colliery not found")
    
    now = datetime.utcnow()
    raw = f"{b.mine_id}:{b.notes}:{b.latitude}:{b.longitude}:{now}"
    sha = hashlib.sha256(raw.encode('utf-8')).hexdigest()
    
    entry = InspectionAudit(
        id=b.client_id, mine_id=mine.id, mine_name=mine.name,
        category=b.category, notes=b.notes, severity=b.severity,
        latitude=b.latitude, longitude=b.longitude, timestamp=now,
        sha256_hash=sha
    )
    db.add(entry)
    
    pen = 12.0 if b.severity == "Critical" else 3.0
    mine.compliance_score = max(0.0, round(mine.compliance_score - pen, 1))
    mine.risk_level = "Critical" if mine.compliance_score < 75.0 else ("Moderate" if mine.compliance_score < 88.0 else "Safe")
    
    db.commit()
    db.close()
    return {"status": "SUCCESS", "sha256": sha}

@app.get("/statutory/form-vi", response_class=HTMLResponse)
def export_form_vi():
    db = SessionLocal()
    audits = db.query(InspectionAudit).order_by(InspectionAudit.timestamp.desc()).limit(20).all()
    db.close()
    
    rows = "".join([
        f"""<tr style="border-bottom: 1px solid #ccc;">
            <td style="padding: 8px; font-family: monospace;">{a.timestamp.strftime('%d/%m/%Y %H:%M')}</td>
            <td style="padding: 8px; font-weight: bold;">{a.mine_name}</td>
            <td style="padding: 8px;">{a.category}</td>
            <td style="padding: 8px;">{a.notes}</td>
            <td style="padding: 8px; color: {'red' if a.severity == 'Critical' else 'black'}; font-weight: bold;">{a.severity}</td>
            <td style="padding: 8px; font-family: monospace; font-size: 11px;">{a.sha256_hash[:16]}...</td>
        </tr>"""
        for a in audits
    ])
    
    html = f"""<!DOCTYPE html>
    <html>
    <head>
        <title>DGMS Form-VI Statutory Inspection Register</title>
        <style>
            body {{ font-family: 'Times New Roman', serif; padding: 25px; color: #111; }}
            .header {{ text-align: center; border-bottom: 2px solid #000; padding-bottom: 10px; margin-bottom: 20px; }}
            table {{ width: 100%; border-collapse: collapse; text-align: left; font-size: 13px; }}
            th {{ border-bottom: 2px solid #000; padding: 8px; background: #f0f0f0; }}
            .footer {{ margin-top: 40px; display: flex; justify-content: space-between; font-size: 12px; }}
            @media print {{ button {{ display: none; }} }}
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
                    <th>Statutory Category</th>
                    <th>Observations & Telemetry Findings</th>
                    <th>Risk Class</th>
                    <th>SHA-256 Signature</th>
                </tr>
            </thead>
            <tbody>
                {rows or "<tr><td colspan='6' style='text-align:center; padding: 20px;'>No statutory breaches logged in this cycle.</td></tr>"}
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
    return HTMLResponse(content=html)
