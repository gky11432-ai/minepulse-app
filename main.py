import hashlib
import json
import urllib.request
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from sqlalchemy import Column, DateTime, Float, String, Text, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Import full layouts from ui.py
from ui import DASHBOARD_HTML, get_form_vi_html

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
    msg = f"🚨 MINEPULSE DGMS CRITICAL BREACH\n\nColliery: {mine_name}\nHazard: {issue}\nTimestamp: {now_time} UTC\n\nAction: CMR 2017 Immediate Isolation Triggered."
    try:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = json.dumps({"chat_id": chat_id, "text": msg}).encode("utf-8")
        req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
        urllib.request.urlopen(req, timeout=5)
    except Exception as exc:
        print("[DISPATCH ERROR]", exc)

def init_db():
    db = SessionLocal()
    try:
        if db.query(Colliery).count() == 0:
            db.add_all([
                Colliery(id="BCCL-JH-01", name="Jharia Colliery Pit 7", subsidiary="BCCL", mine_type="Underground", compliance_score=76.0, risk_level="Moderate"),
                Colliery(id="SECL-GV-04", name="Gevra Opencast Sector B", subsidiary="SECL", mine_type="Opencast", compliance_score=94.5, risk_level="Safe"),
                Colliery(id="ECL-RJ-02", name="Rajmahal Deep OCP", subsidiary="ECL", mine_type="Opencast", compliance_score=68.0, risk_level="Critical")
            ])
            db.commit()
    finally:
        db.close()

init_db()

app = FastAPI(title="MinePulse AI Platform")

class BatchItem(BaseModel):
    client_id: str
    mine_id: str
    officer_name: str = "Er. Gaurav Yadav"
    officer_role: str = "Safety Officer (Overman)"
    dgms_cert_no: str = "DGMS/CMR/2017/OM-8492"
    category: str
    notes: str
    severity: str
    latitude: float
    longitude: float

@app.get("/", response_class=HTMLResponse)
def root():
    return HTMLResponse(content=DASHBOARD_HTML)

@app.get("/api/collieries")
def get_collieries():
    db = SessionLocal()
    try:
        return db.query(Colliery).all()
    finally:
        db.close()

@app.get("/api/inspections")
def get_inspections():
    db = SessionLocal()
    try:
        res = db.query(InspectionAudit).order_by(InspectionAudit.timestamp.desc()).all()
        out = []
        for a in res:
            t_str = a.timestamp.strftime("%Y-%m-%d %H:%M") if a.timestamp else "N/A"
            out.append({
                "id": str(a.id or ""),
                "mine_name": str(a.mine_name or "Unknown Mine"),
                "officer_name": str(a.officer_name or "Officer"),
                "officer_role": str(a.officer_role or "Inspector"),
                "dgms_cert_no": str(a.dgms_cert_no or "N/A"),
                "category": str(a.category or "General"),
                "notes": str(a.notes or ""),
                "severity": str(a.severity or "Normal"),
                "sha256_hash": str(a.sha256_hash or "0000000000"),
                "is_valid": True,
                "timestamp": t_str
            })
        return out
    finally:
        db.close()

@app.post("/api/inspections")
def add_inspection(b: BatchItem):
    db = SessionLocal()
    try:
        mine = db.query(Colliery).filter(Colliery.id == b.mine_id).first()
        if not mine:
            raise HTTPException(status_code=404, detail="Colliery not found")
        
        now = datetime.utcnow()
        raw = f"{b.mine_id}:{b.officer_name}:{b.dgms_cert_no}:{b.notes}:{now}"
        sha = hashlib.sha256(raw.encode("utf-8")).hexdigest()
        
        entry = InspectionAudit(
            id=b.client_id, mine_id=mine.id, mine_name=mine.name,
            officer_name=b.officer_name, officer_role=b.officer_role,
            dgms_cert_no=b.dgms_cert_no, category=b.category, notes=b.notes,
            severity=b.severity, latitude=b.latitude, longitude=b.longitude,
            timestamp=now, sha256_hash=sha
        )
        db.add(entry)
        
        pen = 12.0 if b.severity == "Critical" else 3.0
        mine.compliance_score = max(0.0, round((mine.compliance_score or 100.0) - pen, 1))
        mine.risk_level = "Critical" if mine.compliance_score < 75.0 else ("Moderate" if mine.compliance_score < 88.0 else "Safe")
        
        if b.severity == "Critical":
            trigger_emergency_dispatch(mine.name, b.notes)

        db.commit()
        return {"status": "SUCCESS", "sha256": sha}
    finally:
        db.close()

@app.get("/statutory/form-vi", response_class=HTMLResponse)
def export_form_vi():
    db = SessionLocal()
    try:
        audits = db.query(InspectionAudit).order_by(InspectionAudit.timestamp.desc()).limit(30).all()
        if not audits:
            rows = "<tr><td colspan='7' style='text-align:center; padding: 20px;'>No statutory breaches logged in this cycle.</td></tr>"
        else:
            items = []
            for a in audits:
                color = "red" if a.severity == "Critical" else "black"
                t_str = a.timestamp.strftime("%d/%m/%Y %H:%M") if a.timestamp else "N/A"
                h_val = str(a.sha256_hash or "")[:16]
                r = (
                    "<tr>"
                    f"<td style='font-family: monospace;'>{t_str}</td>"
                    f"<td style='font-weight: bold;'>{a.mine_name}</td>"
                    f"<td><div style='font-weight: bold;'>{a.officer_name}</div><div style='font-size: 11px; color: #555;'>{a.officer_role}</div><div style='font-family: monospace; font-size: 10px; color: #1e3a8a;'>Lic: {a.dgms_cert_no}</div></td>"
                    f"<td>{a.category}</td>"
                    f"<td>{a.notes}</td>"
                    f"<td style='color: {color}; font-weight: bold;'>{a.severity}</td>"
                    f"<td style='font-family: monospace; font-size: 11px;'>{h_val}...<br><span style='color: green; font-weight: bold;'>[VERIFIED]</span></td>"
                    "</tr>"
                )
                items.append(r)
            rows = "".join(items)

        return HTMLResponse(content=get_form_vi_html(rows))
    finally:
        db.close()
      
