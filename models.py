# models.py - Database Models for DGMS Compliance
from sqlalchemy import Column, Integer, String, Float, Text
from database import Base

class Colliery(Base):
    __tablename__ = "collieries"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    subsidiary = Column(String, nullable=False)
    mine_type = Column(String, nullable=False)
    compliance_score = Column(Float, default=90.0)

class Inspection(Base):
    __tablename__ = "inspections"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    client_id = Column(String, unique=True, index=True, nullable=True)
    mine_id = Column(String, nullable=False)
    mine_name = Column(String, nullable=False)
    officer_name = Column(String, nullable=False)
    officer_role = Column(String, nullable=False)
    dgms_cert_no = Column(String, nullable=False)
    category = Column(String, nullable=False)
    notes = Column(Text, nullable=False)
    severity = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    timestamp = Column(String, nullable=False)
    sha256_hash = Column(String, nullable=False)
  
