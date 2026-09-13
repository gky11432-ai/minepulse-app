import hashlib
import json
from datetime import datetime
from typing import List, Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from sqlalchemy import Column, DateTime, Float, Integer, String, Text, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Database Setup (SQLite file-based database)
SQLALCHEMY_DATABASE_URL = "sqlite:///./minepulse.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- Database Models ---
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

# --- Pre-seed Initial Mines Data ---
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

# --- Pydantic Request Schemas ---
class ObservationCreate(BaseModel):
    mine_id: str
    category: str
    notes: str
    severity: str
    latitude: float
    longitude: float

class ObservationResponse(BaseModel):
    id: str
    mine_name: str
    category: str
    notes: str
    severity: str
    latitude: float
    longitude: float
    timestamp: str
    sha256_hash: str
    escalation_status: str

# FastAPI Init
app = FastAPI(title="MinePulse AI Compliance Engine")
templates = Jinja2Templates(directory="templates")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Core Business Logic: Cryptographic Ledger & Dynamic Scoring ---
def compute_sha256_audit_hash(mine_id: str, notes: str, lat: float, lng: float, timestamp: str) -> str:
    raw_payload = f"{mine_id}:{notes}:{lat}:{lng}:{timestamp}"
    return hashlib.sha256(raw_payload.encode('utf-8')).hexdigest()

def update_mine_risk_index(db, mine_id: str, new_severity: str):
    mine = db.query(MineSite).filter(MineSite.id == mine_id).first()
    if not mine:
        return
    
    # Impact scoring according to severity
    penalty = 15.0 if new_severity == "Critical" else (8.0 if new_severity == "Medium" else 2.0)
    mine.compliance_score = max(0.0, round(mine.compliance_score - penalty, 1))
    
    if mine.compliance_score < 75.0:
        mine.risk_level = "Critical"
    elif mine.compliance_score < 88.0:
        mine.risk_level = "Moderate"
    else:
        mine.risk_level = "Safe"
    
    db.commit()

# --- API Endpoints ---
@app.get("/", response_class=HTMLResponse)
async def serve_dashboard(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/v1/mines")
def get_all_mines():
    db = SessionLocal()
    mines = db.query(MineSite).all()
    db.close()
    return mines

@app.get("/api/v1/observations")
def get_all_observations():
    db = SessionLocal()
    records = db.query(InspectionObservation).order_by(InspectionObservation.timestamp.desc()).all()
    db.close()
    return [
        {
            "id": r.id,
            "mine_name": r.mine_name,
            "category": r.category,
            "notes": r.notes,
            "severity": r.severity,
            "latitude": r.latitude,
            "longitude": r.longitude,
            "timestamp": r.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "sha256_hash": r.sha256_hash,
            "escalation_status": r.escalation_status
        }
        for r in records
    ]

@app.post("/api/v1/observations")
def submit_observation(data: ObservationCreate):
    db = SessionLocal()
    mine = db.query(MineSite).filter(MineSite.id == data.mine_id).first()
    if not mine:
        db.close()
        raise HTTPException(status_code=404, detail="Colliery site not found")

    now = datetime.utcnow()
    obs_id = f"OBS-{int(now.timestamp())}"
    
    # Generate tamper-proof SHA-256 hash
    audit_hash = compute_sha256_audit_hash(
        data.mine_id, data.notes, data.latitude, data.longitude, str(now)
    )

    escalation = "Escalated to GM (24h DGMS SLA)" if data.severity == "Critical" else "Routine Monitoring"

    new_record = InspectionObservation(
        id=obs_id,
        mine_id=mine.id,
        mine_name=mine.name,
        category=data.category,
        notes=data.notes,
        severity=data.severity,
        latitude=data.latitude,
        longitude=data.longitude,
        timestamp=now,
        sha256_hash=audit_hash,
        escalation_status=escalation
    )

    db.add(new_record)
    db.commit()

    # Recalculate AI Risk Index
    update_mine_risk_index(db, data.mine_id, data.severity)
    db.close()

    return {"status": "SUCCESS", "observation_id": obs_id, "hash": audit_hash}
  
