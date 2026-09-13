import base64
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
    text = f"🚨 MINEPULSE DGMS CRITICAL BREACH\n\nColliery: {mine_name}\nHazard: {issue}\nTimestamp: {now_time} UTC\n\nAction: CMR 2017 Immediate Isolation Triggered."
    try:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = json.dumps({"chat_id": chat_id, "text": text}).encode("utf-8")
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

INDEX_B64 = (
    b"PCFET0NUWVBFIGh0bWw+PGh0bWwgbGFuZz0iZW4iPjxoZWFkPjxtZXRhIGNoYXJzZXQ9IlVURi04"
    b"Ij48bWV0YSBuYW1lPSJ2aWV3cG9ydCIgY29udGVudD0id2lkdGg9ZGV2aWNlLXdpZHRoLCBpbml0"
    b"aWFsLXNjYWxlPTEuMCI+PHRpdGxlPk1pbmVQdWxzZSBBSTwvdGl0bGU+PHNjcmlwdCBzcmM9Imh0"
    b"dHBzOi8vY2RuLnRhaWx3aW5kY3NzLmNvbSI+PC9zY3JpcHQ+PC9oZWFkPjxib2R5IGNsYXNzPSJi"
    b"Zy1zbGF0ZS05NTUgdGV4dC1zbGF0ZS0xMDAgbWluLWgtc2NyZWVuIGZvbnQtc2FucyBmbGV4IGZs"
    b"ZXgtY29sIj48aGVhZGVyIGNsYXNzPSJib3JkZXItYiBib3JkZXItc2xhdGUtODAwIGJnLXNsYXRl"
    b"LTkwMCBzdGlja3kgdG9wLTAgei01MCBwLTQiPjxkaXYgY2xhc3M9Im1heC13LTd4bCBteC1hdXRv"
    b"IGZsZXgganVzdGlmeS1iZXR3ZWVuIGl0ZW1zLWNlbnRlciB3LWZ1bGwiPjxkaXYgY2xhc3M9ImZs"
    b"ZXggaXRlbXMtY2VudGVyIHNwYWNlLXgtMiI+PHNwYW4gY2xhc3M9InRleHQteGwiPtePjzwvc3Bh"
    b"bj48aDEgY2xhc3M9ImZvbnQtYm9sZCB0ZXh0LXdoaXRlIHRleHQtYmFzZSI+TWluZVB1bHNlIDxz"
    b"cGFuIGNsYXNzPSJ0ZXh0LWFtYmVyLTUwMCI+QTwvc3Bhbj48L2gxPjwvZGl2PjxkaXYgY2xhc3M9"
    b"ImZsZXggc3BhY2UteC0yIj48YSBocmVmPSIvc3RhdHV0b3J5L2Zvcm0tdmkiIHRhcmdldD0iX2Js"
    b"YW5rIiBjbGFzcz0idGV4dC14cyBweC0zIHB5LTEuNSByb3VuZGVkLWxnIGJnLXNsYXRlLTgwMCBi"
    b"b3JkZXIgYm9yZGVyLXNsYXRlLTcwMCB0ZXh0LWFtYmVyLTQwMCBmb250LXNlbWlib2xkIGZsZXgg"
    b"aXRlbXMtY2VudGVyIj5FeHBvcnQgREdNUyBGb3JtLVZJPC9hPjxidXR0b24gb25jbGljaz0idGFi"
    b"KCdkYXNoJykiIGlkPSJiZCIgY2xhc3M9InRleHQteHMgcHgtMyBweS0xLjUgcm91bmRlZC1sZyBi"
    b"Zy1hbWJlci01MDAgdGV4dC1ibGFjayBmb250LWJvbGQiPkRhc2hib2FyZDwvYnV0dG9uPjxidXR0"
    b"b24gb25jbGljaz0idGFiKCdmaWVsZCcpIiBpZD0iYmYiIGNsYXNzPSJ0ZXh0LXhzIHB4LTMgcHkt"
    b"MS41IHJvdW5kZWQtbGcgYmctc2xhdGUtODAwIHRleHQtc2xhdGUtMzAwIj5TdGF0dXRvcnkgT2Zm"
    b"aWNlciBGb3JtPC9idXR0b24+PC9kaXY+PC9kaXY+PC9oZWFkZXI+PG1haW4gY2xhc3M9Im1heC13"
    b"LTd4bCBteC1hdXRvIHAtNCBmbGV4LTEgdy1mdWxsIHNwYWNlLXktNCI+PGRpdiBpZD0idmQiIGNs"
    b"YXNzPSJzcGFjZS15LTQiPjxkaXYgY2xhc3M9ImdyaWQgZ3JpZC1jb2xzLTIgbWQtZ3JpZC1jb2xz"
    b"LTQgZ2FwLTMiPjxkaXYgY2xhc3M9InAtMyBiZy1zbGF0ZS05MDAgYm9yZGVyIGJvcmRlci1zbGF0"
    b"ZS04MDAgcm91bmRlZC14bCI+PHAgY2xhc3M9InRleHQtWzEwcHhdIHRleHQtc2xhdGUtNDAwIj5U"
    b"ZWxlZ3JhbSBCb3QgU2lyZW48L3A+PGgzIGNsYXNzPSJ0ZXh0LWxnIGZvbnQtYm9sZCB0ZXh0LWVt"
    b"ZXJhbGQtNDAwIG10LTEiPkxpdmUgTGlua2VkPC9oMz48L2Rpdj48ZGl2IGNsYXNzPSJwLTMgYmct"
    b"c2xhdGUtOTAwIGJvcmRlciBib3JkZXItc2xhdGUtODAwIHJvdW5kZWQteGwiPjxwIGNsYXNzPSJ0"
    b"ZXh0LVsxMHB4XSB0ZXh0LXNsYXRlLTQwMCI+Q29tcGxpYW5jZSBJbmRleDwvcD48aDMgY2xhc3M9"
    b"InRleHQtbWcgZm9udC1ib2xkIHRleHQtZW1lcmFsZC00MDAgbXQtMSIgaWQ9InNjIj4tLTwvaDM+"
    b"PC9kaXY+PGRpdiBjbGFzcz0icC0zIGJnLXNsYXRlLTkwMCBib3JkZXIgYm9yZGVyLXNsYXRlLTgw"
    b"MCByb3VuZGVkLXhsIj48cCBjbGFzcz0idGV4dC1bMTBweF0gdGV4dC1zbGF0ZS00MDAiPlRvdGFs"
    b"IEF1ZGl0czwvcD48aDMgY2xhc3M9InRleHQtbWcgZm9udC1ib2xkIHRleHQtYW1iZXItNDAwIG10"
    b"LTEiIGlkPSJ0YyI+MDwvaDM+PC9kaXY+PGRpdiBjbGFzcz0icC0zIGJnLXNsYXRlLTkwMCBib3Jk"
    b"ZXIgYm9yZGVyLXNsYXRlLTgwMCByb3VuZGVkLXhsIj48cCBjbGFzcz0idGV4dC1bMTBweF0gdGV4"
    b"dC1zbGF0ZS00MDAiPlRhbXBlciBTZWFsPC9wPjxoMyBjbGFzcz0idGV4dC1sZyBmb250LWJvbGQg"
    b"dGV4dC1lbWVyYWxkLTQwMCBtdC0xIj5TSEEtMjU2IExvY2s8L2gzPjwvZGl2PjwvZGl2PjxkaXYg"
    b"Y2xhc3M9ImJnLXNsYXRlLTkwMCBib3JkZXIgYm9yZGVyLXNsYXRlLTgwMCByb3VuZGVkLXhsIHAt"
    b"NCI+PGgyIGNsYXNzPSJmb250LWJvbGQgdGV4dC1zbSBtYi0zIj5Db2xsaWVyaWVzIE1vbml0b3Jp"
    b"bmc8L2gyPjxkaXYgY2xhc3M9Im92ZXJmbG93LXgtYXV0byI+PHRhYmxlIGNsYXNzPSJ3LWZ1bGwg"
    b"dGV4dC1sZWZ0IHRleHQteHMiPjx0Ym9keSBpZD0ibWwiIGNsYXNzPSJkaXZpZGUteSBkaXZpZGUt"
    b"c2xhdGUtODAwIj48L3Rib2R5PjwvdGFibGU+PC9kaXY+PC9kaXY+PGRpdiBjbGFzcz0iYmctc2xh"
    b"dGUtOTAwIGJvcmRlciBib3JkZXItc2xhdGUtODAwIHJvdW5kZWQteGwgcC00Ij48ZGl2IGNsYXNz"
    b"PSJmbGV4IGp1c3RpZnktYmV0d2VlbiBpdGVtcy1jZW50ZXIgbWItMyI+PGgyIGNsYXNzPSJmb250"
    b"LWJvbGQgdGV4dC1zbSI+QXVkaXQgTG9ncyAmIENyeXB0b2dyYXBoaWMgUHJvb2Y8L2gyPjxidXR0"
    b"b24gb25jbGljaz0ibG9hZCgpIiBjbGFzcz0idGV4dC1bMTFweF0gdGV4dC1zbGF0ZS00MDAgaG92"
    b"ZXI6dGV4dC13aGl0ZSBiZy1zbGF0ZS04MDAgcHgtMiBweS0xIHJvdW5kZWQiPlJlZnJlc2ggU3Ry"
    b"ZWFtPC9idXR0b24+PC9kaXY+PGRpdiBpZD0ib2wiIGNsYXNzPSJzcGFjZS15LTIgdGV4dC14cyI+"
    b"PC9kaXY+PC9kaXY+PC9kaXY+PGRpdiBpZD0idmYiIGNsYXNzPSJoaWRkZW4gbWF4LXctbGcgbXgt"
    b"YXV0byBiZy1zbGF0ZS05MDAgYm9yZGVyIGJvcmRlci1zbGF0ZS04MDAgcm91bmRlZC0yemwgcC01"
    b"IHNwYWNlLXktNCI+PGgyIGNsYXNzPSJmb250LWJvbGQgdGV4dC1iYXNlIj5ER01TIENvbXBldGVu"
    b"dCBPZmZpY2VyIExvZyBGb3JtPC9oMj48Zm9ybSBvbnN1Ym1pdD0ic2F2ZShldmVudCkiIGNsYXNz"
    b"PSJzcGFjZS15LTMgdGV4dC14cyI+PGRpdiBjbGFzcz0iZ3JpZCBncmlkLWNvbHMtMiBnYXAtMiI+"
    b"PGRpdj48bGFiZWwgY2xhc3M9InRleHQtc2xhdGUtNDAwIGJsb2NrIG1iLTEiPk9mZmljZXIgTmFt"
    b"ZTwvbGFiZWw+PGlucHV0IGlkPSJzb25hbWUiIHJlcXVpcmVkIGNsYXNzPSJ3LWZ1bGwgYmctc2xh"
    b"dGUtODAwIHAtMiByb3VuZGVkLWxnIHRleHQtd2hpdGUiIHZhbHVlPSJFei4gR2F1cmF2IFlhZGF2"
    b"Ij48L2Rpdj48ZGl2PjxsYWJlbCBjbGFzcz0idGV4dC1zbGF0ZS00MDAgYmxvY2sgbWItMSI+RGVz"
    b"aWduYXRpb24gLyBSb2xlPC9sYWJlbD48c2VsZWN0IGlkPSJzb3JvbGUiIGNsYXNzPSJ3LWZ1bGwg"
    b"Ymctc2xhdGUtODAwIHAtMiByb3VuZGVkLWxnIHRleHQtd2hpdGUiPjxvcHRpb24gdmFsdWU9IlNh"
    b"ZmV0eSBPZmZpY2VyIChPdmVybWFuKSI+U2FmZXR5IE9mZmljZXIgKE92ZXJtYW4pPC9vcHRpb24+"
    b"PG9wdGlvbiB2YWx1ZT0iRmlyc3QgQ2xhc3MgQ29sbGllcnkgTWFuYWdlciI+Q29sbGllcnkgTWFu"
    b"YWdlciAoMXN0IENsYXNzKTwvb3B0aW9uPjxvcHRpb24gdmFsdWU9IkRpc3BhdGNoIFdlaWdoYnJp"
    b"ZGdlIE9mZmljZXIiPldlaWdoYnJpZGdlIE9mZmljZXI8L29wdGlvbj48L3NlbGVjdD48L2Rpdj48"
    b"L2Rpdj48ZGl2PjxsYWJlbCBjbGFzcz0idGV4dC1zbGF0ZS00MDAgYmxvY2sgbWItMSI+REdNUyBD"
    b"ZXJ0aWZpY2F0ZSAvIExpY2Vuc2UgTm8uPC9sYWJlbD48aW5wdXQgaWQ9InNvY2VydCIgcmVxdWly"
    b"ZWQgY2xhc3M9InctZnVsbCBiZy1zbGF0ZS04MDAgcC0yIHJvdW5kZWQtbGcgdGV4dC13aGl0ZSBm"
    b"b250LW1vbm8iIHZhbHVlPSJER01TL0NNUi8yMDE3L09NLTg0OTIiPjwvZGl2PjxkaXY+PGxhYmVs"
    b"IGNsYXNzPSJ0ZXh0LXNsYXRlLTQwMCBibG9jayBtYi0xIj5UYXJnZXQgTWluZTwvbGFiZWw+PHNl"
    b"bGVjdCBpZD0ic20iIGNsYXNzPSJ3LWZ1bGwgYmctc2xhdGUtODAwIHAtMiByb3VuZGVkLWxnIHRl"
    b"eHQtd2hpdGUiPjwvc2VsZWN0PjwvZGl2PjxkaXY+PGxhYmVsIGNsYXNzPSJ0ZXh0LXNsYXRlLTQw"
    b"MCBibG9jayBtYi0xIj5TdGF0dXRvcnkgUmVndWxhdGlvbiBDYXRlZ29yeTwvbGFiZWw+PHNlbGVj"
    b"dCBpZD0ic2NhdCIgY2xhc3M9InctZnVsbCBiZy1zbGF0ZS04MDAgcC0yIHJvdW5kZWQtbGcgdGV4"
    b"dC13aGl0ZSI+PG9wdGlvbj5DTVIgMTUzOiBWZW50aWxhdGlvbiAmIE1ldGhhbmUgTG9nPC9vcHRp"
    b"b24+PG9wdGlvbj5DTVIgMTA2OiBCZW5jaCBTdGFiaWxpdHkgJiBTbG9wZTwvb3B0aW9uPjxvcHRp"
    b"b24+Q01SIDE2OTogRGFpbHkgQmxhc3RpbmcgJiBFeHBsb3NpdmVzIExvZzwvb3B0aW9uPjxvcHRp"
    b"b24+Q0FBUU1TOiBFbnZpcm9ubWVudGFsIER1c3QgU3RhbmRhcmQ8L29wdGlvbj48L3NlbGVjdD48"
    b"L2Rpdj48ZGl2PjxsYWJlbCBjbGFzcz0idGV4dC1zbGF0ZS00MDAgYmxvY2sgbWItMSI+U3RhdHV0"
    b"b3J5IE9ic2VydmF0aW9uPC9sYWJlbD48dGV4dGFyZWEgaWQ9InNuIiByZXF1aXJlZCByb3dzPSIy"
    b"IiBjbGFzcz0idy1mdWxsIGJnLXNsYXRlLTgwMCBwLTIgcm91bmRlZC1sZyB0ZXh0LXdoaXRlIiBw"
    b"bGFjZWhvbGRlcj0iSGF6YXJkIG9yIHZpb2xhdGlvbiBkZXRhaWwuLi4iPjwvdGV4dGFyZWE+PC9k"
    b"aXY+PGRpdiBjbGFzcz0iZ3JpZCBncmlkLWNvbHMtMiBnYXAtMiI+PGRpdj48bGFiZWwgY2xhc3M9"
    b"InRleHQtc2xhdGUtNDAwIGJsb2NrIG1iLTEiPlNldmVyaXR5PC9sYWJlbD48c2VsZWN0IGlkPSJz"
    b"cyIgY2xhc3M9InctZnVsbCBiZy1zbGF0ZS04MDAgcC0yIHJvdW5kZWQtbGcgdGV4dC13aGl0ZSI+"
    b"PG9wdGlvbiB2YWx1ZT0iTm9ybWFsIj5Sb3V0aW5lIChDb21wbGlhbnQpPC9vcHRpb24+PG9wdGlv"
    b"biB2YWx1ZT0iQ3JpdGljYWwiPkNyaXRpY2FsIChJbW1lZGlhdGUgU3RvcCBPcmRlcik8L29wdGlv"
    b"bj48L3NlbGVjdD48L2Rpdj48ZGl2PjxsYWJlbCBjbGFzcz0idGV4dC1zbGF0ZS00MDAgYmxvY2sg"
    b"bWItMSI+TGVhc2UgQm91bmRhcnkgQ2hlY2s8L2xhYmVsPjxzZWxlY3QgaWQ9InNncHMiIGNsYXNz"
    b"PSJ3LWZ1bGwgYmctc2xhdGUtODAwIHAtMiByb3VuZGVkLWxnIHRleHQtZW1lcmFsZC00MDAiPjxv"
    b"cHRpb24gdmFsdWU9Imluc2lkZSI+SW5zaWRlIEdldnJhIExlYXNlPC9vcHRpb24+PG9wdGlvbiB2"
    b"YWx1ZT0ib3V0c2lkZSI+T3V0c2lkZSBMZWFzZSAoR2VvZmVuY2UgQnJlYWNoKTwvb3B0aW9uPjwv"
    b"c2VsZWN0PjwvZGl2PjwvZGl2PjxidXR0b24gdHlwZT0ic3VibWl0IiBjbGFzcz0idy1mdWxsIGJn"
    b"LWFtYmVyLTUwMCBob3ZlcjpiZy1hbWJlci00MDAgdGV4dC1ibGFjayBmb250LWJvbGQgcC0zIHJv"
    b"dW5kZWQteGwgbXQtMiI+U2lnbiAmIENvbW1pdCB3aXRoIERTQyBTZWFsPC9idXR0b24+PC9mb3Jt"
    b"PjwvZGl2PjwvbWFpbj48c2NyaXB0PmFzeW5jIGZ1bmN0aW9uIGxvYWQoKXt0cnl7Y29uc3RbbVIs"
    b"b1JdPWF3YWl0IFByb21pc2UuYWxsKFtmZXRjaCgnL2FwaS9jb2xsaWVyaWVzJyksZmV0Y2goJy9h"
    b"cGkvaW5zcGVjdGlvbnMnKV0pO2NvbnN0IG1pbmVzPWF3YWl0IG1SLmpzb24oKTtjb25zdCBvYnM9"
    b"YXdhaXQgb1IuanNvbigpO2RvY3VtZW50LmdldEVsZW1lbnRCeUlkKCdtbCcpLmlubmVySFRNTD0o"
    b"bWluZXN8fFtdKS5tYXAobT0+Jzx0cj48dGQgY2xhc3M9InAtMiBmb250LXNlbWlib2xkIj4nK20u"
    b"bmFtZSsnICgnK20uc3Vic2lkaWFyeSsnKTwvdGQ+PHRkIGNsYXNzPSJwLTIiPicrbS5taW5lX3R5"
    b"cGUrJzwvdGQ+PHRkIGNsYXNzPSJwLTIgdGV4dC1lbWVyYWxkLTQwMCI+JyttLmNvbXBsaWFuY2Vf"
    b"c2NvcmUrJyU8L3RkPjwvdHI+Jykjam9pbignJyk7ZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoJ3Nt"
    b"JykuaW5uZXJIVE1MPShtaW5lc3x8W10pLm1hcChtPT4nPG9wdGlvbiB2YWx1ZT0iJyttLmlkKyci"
    b"PicrbS5uYW1lKyc8L29wdGlvbj4nKS5qb2luKCcnKTtkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgn"
    b"dGMnKS5pbm5lclRleHQ9KG9ic3x8W10pLmxlbmd0aDtpZihtaW5lcyYmbWluZXMubGVuZ3RoPjAp"
    b"e2NvbnN0IGF2Zz0obWluZXMucmVkdWNlKChhLGIpPT5hK2IuY29tcGxpYW5jZV9zY29yZSwwKS9t"
    b"aW5lcy5sZW5ndGgpLnRvRml4ZWQoMSk7ZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoJ3NjJykuaW5u"
    b"ZXJUZXh0PWF2ZysnJSc7fWRvY3VtZW50LmdldEVsZW1lbnRCeUlkKCdvbCcpLmlubmVySFRNTD0o"
    b"b2JzfHxbXSkubWFwKG89PnsgcmV0dXJuICc8ZGl2IGNsYXNzPSJwLTIuNSBiZy1zbGF0ZS05MDAg"
    b"Ym9yZGVyIGJvcmRlci1zbGF0ZS04MDAgcm91bmRlZCBmbGV4IGp1c3RpZnktYmV0d2VlbiBpdGVt"
    b"cy1jZW50ZXIiPjxkaXY+PGRpdj48c3Ryb25nPicrKG8ubWluZV9uYW1lfHwnTWluZScpKyc8L3N0"
    b"cm9uZz46ICcrKG8ubm90ZXN8fCcnKSsnPC9kaXY+PGRpdiBjbGFzcz0idGV4dC1bMTBweF0gdGV4"
    b"dC1hbWJlci00MDAiPk9mZmljZXI6ICcrKG8ub2ZmaWNlcl9uYW1lfHwnJykrJyAoJysob29mZmlj"
    b"ZXJfcm9sZXx8JycpKycpIHwgQ2VydDogJysoby5kZ21zX2NlcnRfbm98fCcnKSsnPC9kaXY+PGRp"
    b"diBjbGFzcz0idGV4dC1bMTBweF0gdGV4dC1zbGF0ZS01MDAgZm9udC1tb25vIj5TRUFMOiAnKyhv"
    b"LnNoYTI1Nl9oYXNofHwnJykuY2xpY2UoMCwyMCkrJy4uLTwvZGl2PjwvZGl2PjxkaXYgY2xhc3M9"
    b"InRleHQtcmlnaHQiPjxzcGFuIGNsYXNzPSJ0ZXh0LXNsYXRlLTQwMCB0ZXh0LVsxMHB4XSBibG9j"
    b"ayI+Jysoby50aW1lc3RhbXB8fCcnKSsnPC9zcGFuPjxzcGFuIGNsYXNzPSJ0ZXh0LVsxMHB4XSB0"
    b"ZXh0LWVtZXJhbGQtNDAwIGZvbnQtbW9ubyI+U0VBTCBWRVJJRklFRDwvc3Bhbj48L2Rpdj48L2Rp"
    b"dj4nO30pLmpvaW4oJycpfHwnPHAgY2xhc3M9InRleHQtc2xhdGUtNTAwIj5ObyBhdWRpdHMgeWV0"
    b"LjwvcD4nO31jYXRjaChlcnIpe2NvbnNvbGUuZXJyb3IoZXJyKTt9fWFzeW5jIGZ1bmN0aW9uIHNh"
    b"dmUoZSl7ZS5wcmV2ZW50RGVmYXVsdCgpO2NvbnN0IG1vZGU9ZG9jdW1lbnQuZ2V0RWxlbWVudEJ5"
    b"SWQoJ3NncHMnKS52YWx1ZTtjb25zdCBsYXQ9bW9kZT09PSdpbnNpZGUnPzIyLjM1NDE6MjguNjEz"
    b"OTtjb25zdCBsbmc9bW9kZT09PSdpbnNpZGUnPzgyLjY4MjE6NzcuMjA5MDtjb25zdCByZXM9YXdh"
    b"aXQgZmV0Y2goJy9hcGkvaW5zcGVjdGlvbnMnLHtldGhvZDonUE9TVCcsZGVhZGVyczp7J0NvbnRl"
    b"bnQtVHlwZSc6J2FwcGxpY2F0aW9uL2pzb24nfSxvZHk6SlNPTi5zdHJpbmdpZnkoe2NsaWVudF9p"
    b"ZDonQ0xJLScrRGF0ZS5ub3coKSxtaW5lX2lkOmRvY3VtZW50LmdldEVsZW1lbnRCeUlkKCdzbScp"
    b"LnZhbHVlLG9mZmljZXJfbmFtZTpkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgnc29uYW1lJykudmFs"
    b"dWUsb2ZmaWNlcl9yb2xlOmRvY3VtZW50LmdldEVsZW1lbnRCeUlkKCdzb3JvbGUnKS52YWx1ZSxk"
    b"Z21zX2NlcnRfbm86ZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoJ3NvY2VydCcpLnZhbHVlLGNhdGVn"
    b"b3J5OmRvY3VtZW50LmdldEVsZW1lbnRCeUlkKCdzY2F0JykudmFsdWUsbm90ZXM6ZG9jdW1lbnQu"
    b"Z2V0RWxlbWVudEJ5SWQoJ3NuJykudmFsdWUsc2V2ZXJpdHk6ZG9jdW1lbnQuZ2V0RWxlbWVudEJ5"
    b"SWQoJ3NzJykudmFsdWUsbGF0aXR1ZGU6bGF0LGxvbmdpdHVkZTpsbmd9KX0pO2lmKCFyZXMub2sp"
    b"e2FsZXJ0KCdSRUpFQ1RFRDogTGVhc2UgYm91bmRhcnkgYnJlYWNoJyk7cmV0dXJuO31hbGVydCgn"
    b"U3RhdHV0b3J5IEluc3BlY3Rpb24gU2lnbmVkICYgU2VhbGVkIScpO2RvY3VtZW50LmdldEVsZW1l"
    b"bnRCeUlkKCdzbicpLnZhbHVlPScnO3RhYignZGFzaCcpO2xvYWQoKTt9ZnVuY3Rpb24gdGFiKHQp"
    b"e2RvY3VtZW50LmdldEVsZW1lbnRCeUlkKCd2ZCcpLmNsYXNzTGlzdC50b2dnbGUoJ2hpZGRlbics"
    b"dD09PSdmaWVsZCcpO2RvY3VtZW50LmdldEVsZW1lbnRCeUlkKCd2ZicpLmNsYXNzTGlzdC50b2dn"
    b"bGUoJ2hpZGRlbicsdCE9PSdmaWVsZCcpO2RvY3VtZW50LmdldEVsZW1lbnRCeUlkKCdiZCcpLmNs"
    b"YXNzTmFtZT10PT09J2Rhc2gnPyd0ZXh0LXhzIHB4LTMgcHktMS41IHJvdW5kZWQtbGcgYmctYW1i"
    b"ZXItNTAwIHRleHQtYmxhY2sgZm9udC1ib2xkJzondGV4dC14cyBweC0zIHB5LTEuNSByb3VuZGVk"
    b"LWxnIGJnLXNsYXRlLTgwMCB0ZXh0LXNsYXRlLTMwMCc7ZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQo"
    b"J2JmJykuY2xhc3NOYW1lPXQ9PT0nZmllbGQnPyd0ZXh0LXhzIHB4LTMgcHktMS41IHJvdW5kZWQt"
    b"bGcgYmctYW1iZXItNTAwIHRleHQtYmxhY2sgZm9udC1ib2xkJzondGV4dC14cyBweC0zIHB5LTEu"
    b"NSByb3VuZGVkLWxnIGJnLXNsYXRlLTgwMCB0ZXh0LXNsYXRlLTMwMCc7fXdpbmRvdy5vbmxvYWQ9"
    b"bG9hZDs8L3NjcmlwdD48L2JvZHk+PC9odG1sPg=="
)

FORM_HEAD_B64 = (
    b"PCFET0NUWVBFIGh0bWw+PGh0bWw+PGhlYWQ+PHRpdGxlPkRHTVMgRm9ybS1WSSBTdGF0dXRvcnkg"
    b"SW5zcGVjdGlvbiBSZWdpc3RlcjwvdGl0bGU+PHN0eWxlPmJvZHl7Zm9udC1mYW1pbHk6J1RpbWVz"
    b"IE5ldyBSb21hbicsIHNlcmlmO3BhZGRpbmc6MjVweDtjb2xvcjojMTExO30uaGVhZGVye3RleHQt"
    b"YWxpZ246Y2VudGVyO2JvcmRlci1ib3R0b206MnB4IHNvbGlkICMwMDA7cGFkZGluZy1ib3R0b206"
    b"MTBweDttYXJnaW4tYm90dG9tOjIwcHg7fXRhYmxle3dpZHRoOjEwMCU7Ym9yZGVyLWNvbGxhcHNl"
    b"OmNvbGxhcHNlO3RleHQtYWxpZ246bGVmdDtmb250LXNpemU6MTJweDt9dGh7Ym9yZGVyLWJvdHRv"
    b"bToycHggc29saWQgIzAwMDtwYWRkaW5nOjhweDtiYWNrZ3JvdW5kOiNmMGYwZjA7fXRke2JvcmRl"
    b"ci1ib3R0b206MXB4IHNvbGlkICNjY2M7cGFkZGluZzo4cHg7fS5mb290ZXJ7bWFyZ2luLXRvcDo0"
    b"MHB4O2Rpc3BsYXk6ZmxleDtqdXN0aWZ5LWNvbnRlbnQ6c3BhY2UtYmV0d2Vlbjtmb250LXNpemU6"
    b"MTJweDt9QG1lZGlhIHByaW50e2J1dHRvbntkaXNwbGF5Om5vbmU7fX08L3N0eWxlPjwvaGVhZD48"
    b"Ym9keT48ZGl2IGNsYXNzPSJoZWFkZXIiPjxoMiBzdHlsZT0ibWFyZ2luOjA7Ij5ESVJFQ1RPUkFU"
    b"QSBHRU5FUkFMIE9GIE1JTkVTIENBTEFNSVRJRVMgJiBTQUZFVFkgKERHTVMpPC9oMj48aDMgc3R5"
    b"bGU9Im1hcmdpbjo1cHggMDsiPlNUQVRVVE9SWSBJTlNQRUNUSU9OICYgQlJFQUNIIFJFR0lTVEVS"
    b"IChGT1JNLVZJKTwvaDM+PHAgc3R5bGU9Im1hcmdpbjowO2ZvbnQtc2l6ZToxMnB4OyI+VW5kZXIg"
    b"Q29hbCBNaW5lcyBSZWd1bGF0aW9ucyAoQ01SIDIwMTcpICYgTWluZXMgQWN0IDE5NTI8L3A+PC9k"
    b"aXY+PGRpdiBzdHlsZT0ibWFyZ2luLWJvdHRvbToxNXB4O3RleHQtYWxpZ246cmlnaHQ7Ij48YnV0"
    b"dG9uIG9uY2xpY2s9IndpbmRvdy5wcmludCgpIiBzdHlsZT0icGFkZGluZzo2cHggMTJweDtiYWNr"
    b"Z3JvdW5kOiMyNTYzZWI7Y29sb3I6d2hpdGU7Ym9yZGVyOm5vbmU7Ym9yZGVyLXJhZGl1czo0cHg7"
    b"Y3Vyc29yOnBvaW50ZXI7Ij5QcmludCAvIFNhdmUgYXMgUERGPC9idXR0b24+PC9kaXY+PHRhYmxl"
    b"Pjx0aGVhZD48dHI+PHRoPkRhdGUgJiBUaW1lPC90aD48dGg+Q29sbGllcnkgTmFtZTwvdGg+PHRo"
    b"Pkluc3BlY3RpbmcgT2ZmaWNlciAmIERHTVMgTGljLjwvdGg+PHRoPlN0YXR1dG9yeSBDYXRlZ29y"
    b"eTwvdGg+PHRoPk9ic2VydmF0aW9ucyAmIEZpbmRpbmdzPC90aD48dGg+UmlzayBDbGFzczwvdGg+"
    b"PHRoPlNIQS0yNTYgVmVyaWZpY2F0aW9uPC90aD48L3RyPjwvdGhlYWQ+PHRib2R5Pg=="
)

FORM_TAIL_B64 = (
    b"PC90Ym9keT48L3RhYmxlPjxkaXYgY2xhc3M9ImZvb3RlciI+PGRpdj48cD5HZW5lcmF0ZWQgYnk6"
    b"IDxzdHJvbmc+TWluZVB1bHNlIFN0YXR1dG9yeSBJbmR1c3RyaWFsIEFJIEVuZ2luZTwvc3Ryb25n"
    b"PjwvcD48cD5DZXJ0aWZpZWQgQ3J5cHRvZ3JhcGhpY2FsbHkgVmFsaWQgTG9nYm9vazwvcD48L2Rp"
    b"dj48ZGl2IHN0eWxlPSJ0ZXh0LWFsaWduOnJpZ2h0OyI+PHA+X19fX19fX19fX19fX19fX19fX19f"
    b"X19fX19fX19fX19fX19fXzwvcD48cD48c3Ryb25nPkNvbGxpZXJ5IE1hbmFnZXIgLyBTYWZldHkg"
    b"T2ZmaWNlciBTaWduYXR1cmU8L3N0cm9uZz48L3A+PHA+Q2VydGlmaWVkIERHTVMgQ29tcGV0ZW50"
    b"IFBlcnNvbjwvcD48L2Rpdj48L2Rpdj48L2JvZHk+PC9odG1sPg=="
)

@app.get("/", response_class=HTMLResponse)
def root():
    return HTMLResponse(content=base64.b64decode(INDEX_B64).decode("utf-8"))

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
            id=b.client_id,
            mine_id=mine.id,
            mine_name=mine.name,
            officer_name=b.officer_name,
            officer_role=b.officer_role,
         
