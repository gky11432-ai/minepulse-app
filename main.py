# main.py - MinePulse AI Core Production Server
import os
import glob
import importlib.util
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional

from database import engine, Base, get_db
from models import Colliery, Inspection
from ui import DASHBOARD_HTML, get_form_vi_html

# Initialize PostgreSQL / SQLite Tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MinePulse AI DGMS Statutory Portal",
    description="Zero-Network Pit Compliance & Industrial Safety Gateway",
    version="2.0.0"
)

# CORS Policy for Local PWA & Native Android Apps
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Pydantic Schemas ---
class InspectionCreate(BaseModel):
    client_id: Optional[str] = None
    mine_id: str
    mine_name: str
    officer_name: str
    officer_role: str
    dgms_cert_no: str
    category: str
    notes: str
    severity: str
    latitude: float
    longitude: float
    timestamp: str
    sha256_hash: Optional[str] = None

# --- Seed Initial Collieries (If Database Empty) ---
def seed_default_collieries():
    db = next(get_db())
    try:
        if db.query(Colliery).count() == 0:
            defaults = [
                Colliery(id="SECL-GV-04", name="Gevra Sector B (SECL)", subsidiary="SECL", mine_type="Opencast", compliance_score=94.2),
                Colliery(id="BCCL-JH-07", name="Jharia Pit 7 (BCCL)", subsidiary="BCCL", mine_type="Underground", compliance_score=82.5),
                Colliery(id="ECL-RJ-02", name="Rajmahal Deep (ECL)", subsidiary="ECL", mine_type="Opencast", compliance_score=88.0)
            ]
            db.add_all(defaults)
            db.commit()
    except Exception as e:
        db.rollback()
    finally:
        db.close()

seed_default_collieries()

# --- Root HTML Dashboard ---
@app.get("/", response_class=HTMLResponse)
def get_dashboard():
    return HTMLResponse(content=DASHBOARD_HTML)

# --- Core REST APIs ---
@app.get("/api/collieries")
def get_collieries(db: Session = Depends(get_db)):
    return db.query(Colliery).all()

@app.get("/api/inspections")
def get_inspections(db: Session = Depends(get_db)):
    return db.query(Inspection).order_by(Inspection.id.desc()).all()

@app.post("/api/inspections")
def create_inspection(item: InspectionCreate, db: Session = Depends(get_db)):
    # Avoid duplicate records via client_id or sha256
    if item.client_id:
        existing = db.query(Inspection).filter(Inspection.client_id == item.client_id).first()
        if existing:
            return existing

    record = Inspection(
        client_id=item.client_id or f"CLI-{os.urandom(4).hex()}",
        mine_id=item.mine_id,
        mine_name=item.mine_name,
        officer_name=item.officer_name,
        officer_role=item.officer_role,
        dgms_cert_no=item.dgms_cert_no,
        category=item.category,
        notes=item.notes,
        severity=item.severity,
        latitude=item.latitude,
        longitude=item.longitude,
        timestamp=item.timestamp,
        sha256_hash=item.sha256_hash or f"SEAL-{os.urandom(8).hex().upper()}"
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

# --- Form-VI Printable Register (Fixed: Safe Arguments) ---
@app.get("/statutory/form-vi", response_class=HTMLResponse)
def export_form_vi(db: Session = Depends(get_db)):
    inspections = db.query(Inspection).order_by(Inspection.id.desc()).all()
    collieries = db.query(Colliery).all()
    return HTMLResponse(content=get_form_vi_html(inspections, collieries))

# --- Emergency Broadcast Mock Router ---
@app.post("/api/broadcast/trigger")
def trigger_broadcast():
    return {"status": "ACTIVE", "message": "Emergency Siren & Vibration Dispatched Globally"}

# --- Dynamic Router Loader for 'modules/' Folder ---
# Automatically loads sync_engine.py, pdf_engine.py, pit_vault.py, pwa.py if present
modules_dir = os.path.join(os.path.dirname(__file__), "modules")
if os.path.exists(modules_dir):
    for filepath in glob.glob(os.path.join(modules_dir, "*.py")):
        mod_name = os.path.splitext(os.path.basename(filepath))[0]
        if mod_name.startswith("__"):
            continue
        try:
            spec = importlib.util.spec_from_file_location(mod_name, filepath)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            if hasattr(module, "router"):
                app.include_router(module.router)
                print(f"✅ Loaded Router Module: {mod_name}")
        except Exception as err:
            print(f"⚠️ Could not auto-load module {mod_name}: {err}")
