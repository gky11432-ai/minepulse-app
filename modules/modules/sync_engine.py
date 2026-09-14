# modules/sync_engine.py - Production Grade Offline-to-Cloud Batch Sync
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import List, Optional
import hashlib
from datetime import datetime

from database import get_db
from models import Inspection, Colliery

router = APIRouter(prefix="/api/sync", tags=["Industrial Sync Engine"])

class AuditLogItem(BaseModel):
    client_id: str
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

class BatchSyncPayload(BaseModel):
    device_id: str
    batch_timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    records: List[AuditLogItem]

class BatchSyncResponse(BaseModel):
    status: str
    accepted_count: int
    synced_ids: List[str]
    conflicts: List[str]
    server_time: str

def compute_record_hash(rec: AuditLogItem) -> str:
    raw_payload = f"{rec.client_id}|{rec.mine_id}|{rec.officer_name}|{rec.category}|{rec.timestamp}"
    return hashlib.sha256(raw_payload.encode()).hexdigest().upper()

@router.post("/batch", response_model=BatchSyncResponse)
def process_offline_batch(payload: BatchSyncPayload, db: Session = Depends(get_db)):
    synced_ids = []
    conflicts = []

    for item in payload.records:
        # Check for existing record to avoid duplication
        existing = db.query(Inspection).filter(
            (Inspection.client_id == item.client_id) | 
            (Inspection.sha256_hash == item.sha256_hash)
        ).first()

        if existing:
            conflicts.append(item.client_id)
            continue

        verified_hash = item.sha256_hash or compute_record_hash(item)

        new_inspection = Inspection(
            client_id=item.client_id,
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
            sha256_hash=verified_hash
        )
        db.add(new_inspection)
        synced_ids.append(item.client_id)

    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database commit failed: {str(e)}")

    return BatchSyncResponse(
        status="SUCCESS",
        accepted_count=len(synced_ids),
        synced_ids=synced_ids,
        conflicts=conflicts,
        server_time=datetime.utcnow().isoformat()
    )
  
