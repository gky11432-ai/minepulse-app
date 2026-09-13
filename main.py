import hashlib
from datetime import datetime
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from sqlalchemy import Column, DateTime, Float, String, Text, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Database Setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./minepulse.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class MineSite(Base):
    __tablename__ = "mine_sites"
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    subsidiary = Column(String, nullable=False)
    mine_type = Column(String, nullable=False)
    compliance_score = Column(Float, default=100.0)
    risk_level = Column(String, default="Safe")
    pm10_reading = Column(Float, default=85.0)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

class InspectionObservation(Base):
    __tablename__ = "inspection_observations"
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
    escalation_status = Column(String, default="Open")

Base.metadata.create_all(bind=engine)

def seed_initial_data():
    db = SessionLocal()
    if db.query(MineSite).count() == 0:
        sample_mines = [
            MineSite(id="M101", name="Jharia Colliery Pit 7", subsidiary="BCCL", mine_type="Underground", compliance_score=72.0, risk_level="Critical", pm10_reading=168.0, latitude=23.7412, longitude=86.4189),
            MineSite(id="M102", name="Gevra Opencast Sector B", subsidiary="SECL", mine_type="Opencast", compliance_score=94.0, risk_level="Safe", pm10_reading=92.0, latitude=22.3541, longitude=82.6821),
            MineSite(id="M103", name="Rajmahal Deep Haul Road", subsidiary="ECL", mine_type="Opencast", compliance_score=79.0, risk_level="Moderate", pm10_reading=128.0, latitude=25.0410, longitude=87.3512),
        ]
        db.add_all(sample_mines)
        db.commit()
    db.close()

seed_initial_data()

app = FastAPI(title="MinePulse AI Compliance Engine")

HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>MinePulse AI - Smart Governance & Compliance</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://unpkg.com/lucide@latest"></script>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen font-sans flex flex-col">
  <header class="border-b border-slate-800 bg-slate-900 sticky top-0 z-50 p-4">
    <div class="max-w-7xl mx-auto flex items-center justify-between">
      <div class="flex items-center space-x-2">
        <span class="p-2 bg-amber-500/20 text-amber-500 rounded-lg font-bold text-lg">⛏️</span>
        <div>
          <h1 class="font-bold text-white text-base">MinePulse <span class="text-amber-500">AI</span></h1>
          <p class="text-[11px] text-slate-400">Coal India Ltd. Statutory Compliance</p>
        </div>
      </div>
      <div class="flex space-x-2">
        <button onclick="switchTab('dashboard')" id="btn-dash" class="text-xs px-3 py-1.5 rounded-lg bg-amber-500 text-black font-bold">HQ Dashboard</button>
        <button onclick="switchTab('mobile')" id="btn-mob" class="text-xs px-3 py-1.5 rounded-lg bg-slate-800 text-slate-300">Field Inspector</button>
      </div>
    </div>
  </header>

  <main class="max-w-7xl mx-auto p-4 flex-1 w-full space-y-6">
    <div id="view-dashboard" class="space-y-4">
      <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
        <div class="p-3 bg-slate-900 border border-slate-800 rounded-xl">
          <p class="text-[10px] text-slate-400">Extraction Discrepancy</p>
          <h3 class="text-lg font-bold text-rose-400 mt-1">-380 MT Siding</h3>
        </div>
        <div class="p-3 bg-slate-900 border border-slate-800 rounded-xl">
          <p class="text-[10px] text-slate-400">Compliance Index</p>
          <h3 class="text-lg font-bold text-emerald-400 mt-1" id="compliance-index">91.2%</h3>
        </div>
        <div class="p-3 bg-slate-900 border border-slate-800 rounded-xl">
          <p class="text-[10px] text-slate-400">Logged Inspections</p>
          <h3 class="text-lg font-bold text-amber-400 mt-1" id="total-logs">0</h3>
        </div>
        <div class="p-3 bg-slate-900 border border-slate-800 rounded-xl">
          <p class="text-[10px] text-slate-400">Air Quality (PM10)</p>
          <h3 class="text-lg font-bold text-rose-400 mt-1">168 µg/m³</h3>
        </div>
      </div>

      <div class="bg-slate-900 border border-slate-800 rounded-xl p-4">
        <h2 class="font-bold text-sm text-white mb-3">Active Colliery Monitoring (BCCL, SECL, ECL)</h2>
        <div class="overflow-x-auto">
          <table class="w-full text-left text-xs">
            <thead class="bg-slate-950 text-slate-400 border-b border-slate-800">
              <tr>
                <th class="p-2">Mine Site</th>
                <th class="p-2">Type</th>
                <th class="p-2">Compliance Score</th>
                <th class="p-2">PM10</th>
              </tr>
            </thead>
            <tbody id="mines-body" class="divide-y divide-slate-800"></tbody>
          </table>
        </div>
      </div>

      <div class="bg-slate-900 border border-slate-800 rounded-xl p-4">
        <h2 class="font-bold text-sm text-white mb-3">Live Statutory Observations Feed</h2>
        <div id="obs-feed" class="space-y-2"></div>
      </div>
    </div>

    <div id="view-mobile" class="hidden max-w-lg mx-auto bg-slate-900 border border-slate-800 rounded-2xl p-5 space-y-4">
      <h2 class="font-bold text-base text-white">Geotagged Field Inspection</h2>
      <form onsubmit="submitForm(event)" class="space-y-3 text-xs">
        <div>
          <label class="block text-slate-400 mb-1">Target Mine</label>
          <select id="sel-mine" class="w-full bg-slate-800 border border-slate-700 p-2 rounded-lg text-white"></select>
        </div>
        <div>
          <label class="block text-slate-400 mb-1">Regulation Domain</label>
          <select id="sel-cat" class="w-full bg-slate-800 border border-slate-700 p-2 rounded-lg text-white">
            <option>Safety (CMR 2017: Ventilation / Slope)</option>
            <option>Environmental (Dust / Water Sprinkling)</option>
            <option>Contractor Labour (CMPFO Wages)</option>
            <option>Explosive Storage Protocols</option>
          </select>
        </div>
        <div>
          <label class="block text-slate-400 mb-1">Observation Details</label>
          <textarea id="inp-notes" required rows="3" placeholder="Enter findings..." class="w-full bg-slate-800 border border-slate-700 p-2 rounded-lg text-white"></textarea>
        </div>
        <div class="grid grid-cols-2 gap-2">
          <div>
            <label class="block text-slate-400 mb-1">Severity</label>
            <select id="sel-sev" class="w-full bg-slate-800 border border-slate-700 p-2 rounded-lg text-white">
              <option value="Normal">Routine</option>
              <option value="Medium">Medium (72h SLA)</option>
              <option value="Critical">Critical (Immediate DGMS)</option>
            </select>
          </div>
          <div>
            <label class="block text-slate-400 mb-1">GPS Lock</label>
            <button type="button" onclick="lockGPS()" id="btn-gps" class="w-full bg-slate-800 border border-slate-700 p-2 rounded-lg text-emerald-400">Lock Real GPS</button>
          </div>
        </div>
        <button type="submit" class="w-full bg-amber-500 hover:bg-amber-400 text-black font-bold p-3 rounded-xl mt-2">Submit to SHA-256 Audit Trail</button>
      </form>
    </div>
  </main>

  <script>
    let lat = 23.7412, lng = 86.4189;
    async function loadData() {
      const [mRes, oRes] = await Promise.all([fetch('/api/v1/mines'), fetch('/api/v1/observations')]);
      const mines = await mRes.json();
      const obs = await oRes.json();
      
      document.getElementById('mines-body').innerHTML = mines.map(m => `
        <tr>
          <td class="p-2 font-medium">${m.name} (${m.subsidiary})</td>
          <td class="p-2 text-slate-400">${m.mine_type}</td>
          <td class="p-2"><span class="px-2 py-0.5 rounded text-[11px] ${m.risk_level==='Safe'?'bg-emerald-500/20 text-emerald-400':'bg-rose-500/20 text-rose-400'}">${m.compliance_score}% (${m.risk_level})</span></td>
          <td class="p-2">${m.pm10_reading} µg/m³</td>
        </tr>
      `).join('');

      document.getElementById('sel-mine').innerHTML = mines.map(m => `<option value="${m.id}">${m.name} (${m.subsidiary})</option>`).join('');
      document.getElementById('total-logs').innerText = obs.length;
      
      document.getElementById('obs-feed').innerHTML = obs.length ? obs.map(o => `
        <div class="p-2.5 bg-slate-950 border border-slate-800 rounded-lg text-xs space-y-1">
          <div class="flex justify-between font-bold text-white"><span>${o.mine_name}</span><span class="text-[10px] text-slate-500 font-mono">${o.timestamp}</span></div>
          <p class="text-slate-300">${o.notes}</p>
          <div class="text-[10px] font-mono text-emerald-400 flex justify-between"><span>${o.category}</span><span>GPS: ${o.latitude.toFixed(3)}, ${o.longitude.toFixed(3)}</span></div>
        </div>
      `).join('') : '<p class="text-xs text-slate-500">No logs yet. Use Field Inspector to add.</p>';
    }

    function lockGPS() {
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(p => {
          lat = p.coords.latitude; lng = p.coords.longitude;
          document.getElementById('btn-gps').innerText = `${lat.toFixed(2)}, ${lng.toFixed(2)}`;
        }, () => { document.getElementById('btn-gps').innerText = "Geo-locked"; });
      }
    }

    async function submitForm(e) {
      e.preventDefault();
      await fetch('/api/v1/observations', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
          mine_id: document.getElementById('sel-mine').value,
          category: document.getElementById('sel-cat').value,
          notes: document.getElementById('inp-notes').value,
          severity: document.getElementById('sel-sev').value,
          latitude: lat, longitude: lng
        })
      });
      alert('Saved with SHA-256 Audit Trail!');
      document.getElementById('inp-notes').value = '';
      switchTab('dashboard');
      loadData();
    }

    function switchTab(t) {
      document.getElementById('view-dashboard').classList.toggle('hidden', t === 'mobile');
      document.getElementById('view-mobile').classList.toggle('hidden', t !== 'mobile');
      document.getElementById('btn-dash').className = t === 'dashboard' ? 'text-xs px-3 py-1.5 rounded-lg bg-amber-500 text-black font-bold' : 'text-xs px-3 py-1.5 rounded-lg bg-slate-800 text-slate-300';
      document.getElementById('btn-mob').className = t === 'mobile' ? 'text-xs px-3 py-1.5 rounded-lg bg-amber-500 text-black font-bold' : 'text-xs px-3 py-1.5 rounded-lg bg-slate-800 text-slate-300';
    }

    window.onload = loadData;
  </script>
</body>
</html>
"""

class ObservationCreate(BaseModel):
    mine_id: str
    category: str
    notes: str
    severity: str
    latitude: float
    longitude: float

@app.get("/", response_class=HTMLResponse)
def index():
    return HTMLResponse(content=HTML_CONTENT)

@app.get("/api/v1/mines")
def get_mines():
    db = SessionLocal()
    mines = db.query(MineSite).all()
    db.close()
    return mines

@app.get("/api/v1/observations")
def get_observations():
    db = SessionLocal()
    obs = db.query(InspectionObservation).order_by(InspectionObservation.timestamp.desc()).all()
    db.close()
    return [
        {
            "id": o.id, "mine_name": o.mine_name, "category": o.category,
            "notes": o.notes, "severity": o.severity, "latitude": o.latitude,
            "longitude": o.longitude, "timestamp": o.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "sha256_hash": o.sha256_hash, "escalation_status": o.escalation_status
        }
        for o in obs
    ]

@app.post("/api/v1/observations")
def add_observation(data: ObservationCreate):
    db = SessionLocal()
    mine = db.query(MineSite).filter(MineSite.id == data.mine_id).first()
    if not mine:
        db.close()
        raise HTTPException(status_code=404, detail="Mine not found")
    
    now = datetime.utcnow()
    raw = f"{data.mine_id}:{data.notes}:{data.latitude}:{data.longitude}:{now}"
    sha = hashlib.sha256(raw.encode('utf-8')).hexdigest()
    
    new_obs = InspectionObservation(
        id=f"OBS-{int(now.timestamp())}",
        mine_id=mine.id,
        mine_name=mine.name,
        category=data.category,
        notes=data.notes,
        severity=data.severity,
        latitude=data.latitude,
        longitude=data.longitude,
        timestamp=now,
        sha256_hash=sha,
        escalation_status="Immediate DGMS SLA" if data.severity == "Critical" else "Routine"
    )
    db.add(new_obs)
    
    # Update mine score
    pen = 15.0 if data.severity == "Critical" else (8.0 if data.severity == "Medium" else 2.0)
    mine.compliance_score = max(0.0, round(mine.compliance_score - pen, 1))
    mine.risk_level = "Critical" if mine.compliance_score < 75.0 else ("Moderate" if mine.compliance_score < 88.0 else "Safe")
    
    db.commit()
    db.close()
    return {"status": "SUCCESS"}
  
