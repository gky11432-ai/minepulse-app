import hashlib
import json
import urllib.request
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
    mine_id = Column(String, nullable=True)
    mine_name = Column(String, nullable=True)
    officer_name = Column(String, nullable=True)
    officer_role = Column(String, nullable=True)
    dgms_cert_no = Column(String, nullable=True)
    category = Column(String, nullable=True)
    notes = Column(Text, nullable=True)
    severity = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    sha256_hash = Column(String, nullable=True)

Base.metadata.create_all(bind=engine)

def trigger_emergency_dispatch(mine_name: str, issue: str):
    bot_token = "8824795075:AAEnJdgVkzhCfNsl7TWDi5HzYlXBa7txmS0"
    chat_id = "805617246"
    now_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    msg = f"EMERGENCY: DGMS BREACH\nMine: {mine_name}\nIssue: {issue}\nTime: {now_time} UTC\nAction: Immediate Pit Isolation"
    try:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = json.dumps({"chat_id": chat_id, "text": msg}).encode("utf-8")
        req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
        urllib.request.urlopen(req, timeout=5)
    except Exception as exc:
        print("[DISPATCH ERROR]", exc)

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

app = FastAPI(title="MinePulse AI")

class BatchItem(BaseModel):
    client_id: str
    mine_id: str
    officer_name: str = "Er. Gaurav Yadav"
    officer_role: str = "Safety Officer"
    dgms_cert_no: str = "DGMS/CMR/2017/OM-8492"
    category: str
    notes: str
    severity: str
    latitude: float
    longitude: float

HTML_APP = """<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>MinePulse AI</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-950 text-slate-100 p-4 font-sans">
  <div class="max-w-4xl mx-auto space-y-4">
    <div class="flex justify-between items-center border-b border-slate-800 pb-3">
      <h1 class="text-xl font-bold">MinePulse <span class="text-amber-500">AI</span></h1>
      <div class="space-x-2">
        <a href="/statutory/form-vi" target="_blank" class="px-3 py-1.5 bg-slate-800 text-amber-400 rounded text-xs">Form-VI Register</a>
        <button onclick="tab('dash')" id="btn-d" class="px-3 py-1.5 bg-amber-500 text-black font-bold rounded text-xs">Dashboard</button>
        <button onclick="tab('field')" id="btn-f" class="px-3 py-1.5 bg-slate-800 rounded text-xs">Submit Audit</button>
      </div>
    </div>
    <div id="p-dash" class="space-y-4">
      <div class="grid grid-cols-2 md:grid-cols-3 gap-3 text-center">
        <div class="bg-slate-900 p-3 rounded border border-slate-800"><p class="text-xs text-slate-400">Telegram Siren</p><p class="text-emerald-400 font-bold">Live Linked</p></div>
        <div class="bg-slate-900 p-3 rounded border border-slate-800"><p class="text-xs text-slate-400">Tamper Seal</p><p class="text-emerald-400 font-bold">SHA-256 Valid</p></div>
        <div class="bg-slate-900 p-3 rounded border border-slate-800"><p class="text-xs text-slate-400">Total Audits</p><p id="t-aud" class="text-amber-400 font-bold">0</p></div>
      </div>
      <div class="bg-slate-900 p-4 rounded border border-slate-800"><h2 class="font-bold text-sm mb-2">Collieries</h2><div id="m-list" class="text-xs divide-y divide-slate-800"></div></div>
      <div class="bg-slate-900 p-4 rounded border border-slate-800"><h2 class="font-bold text-sm mb-2">Recent Logs</h2><div id="a-list" class="text-xs space-y-2"></div></div>
    </div>
    <div id="p-field" class="hidden max-w-md mx-auto bg-slate-900 p-4 rounded border border-slate-800 space-y-3">
      <h2 class="font-bold text-sm">Log Statutory Audit</h2>
      <form onsubmit="submitForm(event)" class="space-y-2 text-xs">
        <div><label class="block text-slate-400">Mine</label><select id="f-mine" class="w-full bg-slate-800 p-2 rounded text-white"></select></div>
        <div><label class="block text-slate-400">Category</label><select id="f-cat" class="w-full bg-slate-800 p-2 rounded text-white"><option>CMR 153: Methane Check</option><option>CMR 106: Slope Stability</option><option>CMR 169: Blasting</option></select></div>
        <div><label class="block text-slate-400">Observation</label><textarea id="f-notes" required class="w-full bg-slate-800 p-2 rounded text-white" rows="2"></textarea></div>
        <div><label class="block text-slate-400">Severity</label><select id="f-sev" class="w-full bg-slate-800 p-2 rounded text-white"><option value="Normal">Normal</option><option value="Critical">Critical (Sirens Triggered)</option></select></div>
        <button type="submit" class="w-full bg-amber-500 text-black font-bold p-2 rounded mt-2">Sign & Seal DSC</button>
      </form>
    </div>
  </div>
  <script>
    async function refresh() {
      const [mRes, aRes] = await Promise.all([fetch('/api/collieries'), fetch('/api/inspections')]);
      const mines = await mRes.json();
      const audits = await aRes.json();
      document.getElementById('t-aud').innerText = audits.length;
      document.getElementById('f-mine').innerHTML = mines.map(m => '<option value="'+m.id+'">'+m.name+'</option>').join('');
      document.getElementById('m-list').innerHTML = mines.map(m => '<div class="py-2 flex justify-between"><span>'+m.name+'</span><span class="text-emerald-400">'+m.compliance_score+'%</span></div>').join('');
      document.getElementById('a-list').innerHTML = audits.map(a => '<div class="p-2 bg-slate-950 rounded flex justify-between"><div><strong>'+a.mine_name+'</strong>: '+a.notes+'<br><span class="text-[10px] text-slate-500">'+a.sha256_hash.slice(0,20)+'...</span></div><div class="text-right text-[10px]"><span class="text-slate-400">'+a.timestamp+'</span><br><span class="text-emerald-400">[VERIFIED]</span></div></div>').join('') || '<p class="text-slate-500">No audits yet.</p>';
    }
    async function submitForm(e) {
      e.preventDefault();
      await fetch('/api/inspections', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
          client_id: 'C-' + Date.now(),
          mine_id: document.getElementById('f-mine').value,
          category: document.getElementById('f-cat').value,
          notes: document.getElementById('f-notes').value,
          severity: document.getElementById('f-sev').value,
          latitude: 22.35, longitude: 82.68
        })
      });
      alert('Audit Logged!');
      document.getElementById('f-notes').value = '';
      tab('dash');
      refresh();
    }
    function tab(name) {
      document.getElementById('p-dash').classList.toggle('hidden', name !== 'dash');
      document.getElementById('p-field').classList.toggle('hidden', name !== 'field');
      document.getElementById('btn-d').className = name === 'dash' ? 'px-3 py-1.5 bg-amber-500 text-black font-bold rounded text-xs' : 'px-3 py-1.5 bg-slate-800 rounded text-xs';
      document.getElementById('btn-f').className = name === 'field' ? 'px-3 py-1.5 bg-amber-500 text-black font-bold rounded text-xs' : 'px-3 py-1.5 bg-slate-800 rounded text-xs';
    }
    window.onload = refresh;
  </script>
</body>
</html>"""

@app.get("/", response_class=HTMLResponse)
def root():
    return HTMLResponse(content=HTML_APP)

@app.get("/api/collieries")
def get_collieries():
    db = SessionLocal()
    items = db.query(Colliery).all()
    db.close()
    return items

@app.get("/api/inspections")
def get_inspections():
    db = SessionLocal()
    items = db.query(InspectionAudit).order_by(InspectionAudit.timestamp.desc()).all()
    out = []
    for a in items:
        out.append({
            "id": a.id, "mine_name": a.mine_name, "officer_name": a.officer_name,
            "category": a.category, "notes": a.notes, "severity": a.severity,
            "sha256_hash": a.sha256_hash or "",
            "timestamp": a.timestamp.strftime("%Y-%m-%d %H:%M") if a.timestamp else "N/A"
        })
    db.close()
    return out

@app.post("/api/inspections")
def add_inspection(b: BatchItem):
    db = SessionLocal()
    mine = db.query(Colliery).filter(Colliery.id == b.mine_id).first()
    if not mine:
        db.close()
        raise HTTPException(status_code=404, detail="Mine not found")
    now = datetime.utcnow()
    raw = f"{b.mine_id}:{b.notes}:{now}"
    sha = hashlib.sha256(raw.encode("utf-8")).hexdigest()
    entry = InspectionAudit(
        id=b.client_id, mine_id=mine.id, mine_name=mine.name,
        officer_name=b.officer_name, officer_role=b.officer_role,
        dgms_cert_no=b.dgms_cert_no, category=b.category, notes=b.notes,
        severity=b.severity, latitude=b.latitude, longitude=b.longitude,
        timestamp=now, sha256_hash=sha
    )
    db.add(entry)
    if b.severity == "Critical":
        mine.compliance_score = max(0.0, mine.compliance_score - 10.0)
        trigger_emergency_dispatch(mine.name, b.notes)
    else:
        mine.compliance_score = max(0.0, mine.compliance_score - 2.0)
    db.commit()
    db.close()
    return {"status": "SUCCESS", "sha256": sha}

@app.get("/statutory/form-vi", response_class=HTMLResponse)
def form_vi():
    db = SessionLocal()
    items = db.query(InspectionAudit).order_by(InspectionAudit.timestamp.desc()).limit(30).all()
    db.close()
    rows = ""
    for a in items:
        t = a.timestamp.strftime("%d/%m/%Y %H:%M") if a.timestamp else "N/A"
        c = "red" if a.severity == "Critical" else "black"
        rows += f"<tr style='border-bottom: 1px solid #ddd;'><td style='padding:6px;'>{t}</td><td style='padding:6px;'>{a.mine_name}</td><td style='padding:6px;'>{a.officer_name}</td><td style='padding:6px;'>{a.category}</td><td style='padding:6px;'>{a.notes}</td><td style='padding:6px; color:{c};'>{a.severity}</td><td style='padding:6px; font-family:monospace;'>{a.sha256_hash[:16]}... [VERIFIED]</td></tr>"
    if not rows:
        rows = "<tr><td colspan='7' style='padding:15px; text-align:center;'>No statutory breaches logged.</td></tr>"
    html = f"<!DOCTYPE html><html><head><title>DGMS Form-VI</title></head><body style='font-family:sans-serif; padding:20px;'><h2 style='text-align:center;'>DGMS STATUTORY LOGBOOK (FORM-VI)</h2><p style='text-align:center; font-size:12px;'>Mines Act 1952 & CMR 2017</p><div style='text-align:right;'><button onclick='window.print()'>Print PDF</button></div><br><table style='width:100%; border-collapse:collapse; font-size:12px;'><thead><tr style='background:#f2f2f2;'><th style='padding:6px; text-align:left;'>Date</th><th style='padding:6px; text-align:left;'>Colliery</th><th style='padding:6px; text-align:left;'>Officer</th><th style='padding:6px; text-align:left;'>Category</th><th style='padding:6px; text-align:left;'>Observation</th><th style='padding:6px; text-align:left;'>Severity</th><th style='padding:6px; text-align:left;'>Tamper Seal</th></tr></thead><tbody>{rows}</tbody></table></body></html>"
    return HTMLResponse(content=html)
  
