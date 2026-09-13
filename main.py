import hashlib
import json
from datetime import datetime
from typing import Optional, List
from fastapi import FastAPI, HTTPException, Request, Depends, status
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from sqlalchemy import Column, DateTime, Float, String, Text, Boolean, Integer, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session

# Production SQLite / PostgreSQL Compatible Engine
SQLALCHEMY_DATABASE_URL = "sqlite:///./minepulse.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- Database Schemas ---

class Colliery(Base):
    __tablename__ = "collieries"
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    subsidiary = Column(String, nullable=False)
    mine_type = Column(String, nullable=False)
    compliance_score = Column(Float, default=100.0)
    risk_level = Column(String, default="Safe")
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

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
    synced_offline = Column(Boolean, default=False)
    escalation_status = Column(String, default="Routine")

class WeighbridgeTelemetry(Base):
    __tablename__ = "weighbridge_telemetry"
    id = Column(Integer, primary_key=True, autoincrement=True)
    siding_id = Column(String, nullable=False)
    gross_tonnage = Column(Float, nullable=False)
    tare_tonnage = Column(Float, nullable=False)
    net_tonnage = Column(Float, nullable=False)
    discrepancy_flag = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

class EnvironmentTelemetry(Base):
    __tablename__ = "env_telemetry"
    id = Column(Integer, primary_key=True, autoincrement=True)
    station_id = Column(String, nullable=False)
    pm10 = Column(Float, nullable=False)
    pm25 = Column(Float, nullable=False)
    methane_ch4 = Column(Float, nullable=False)
    sprinklers_active = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

def seed_production_defaults():
    db = SessionLocal()
    if db.query(Colliery).count() == 0:
        sample_mines = [
            Colliery(id="BCCL-JH-01", name="Jharia Colliery (Pit 7)", subsidiary="BCCL", mine_type="Underground", compliance_score=76.0, risk_level="Moderate", latitude=23.7412, longitude=86.4189),
            Colliery(id="SECL-GV-04", name="Gevra Opencast (Sector B)", subsidiary="SECL", mine_type="Opencast", compliance_score=94.5, risk_level="Safe", latitude=22.3541, longitude=82.6821),
            Colliery(id="ECL-RJ-02", name="Rajmahal Deep OCP", subsidiary="ECL", mine_type="Opencast", compliance_score=68.0, risk_level="Critical", latitude=25.0410, longitude=87.3512),
        ]
        db.add_all(sample_mines)
        db.commit()
    db.close()

seed_production_defaults()

app = FastAPI(title="MinePulse AI Industrial Platform")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Pydantic Data Contract Schemas ---

class ObservationBatchItem(BaseModel):
    client_id: str
    mine_id: str
    category: str
    notes: str
    severity: str
    latitude: float
    longitude: float
    recorded_at: str

class WeighbridgeInput(BaseModel):
    siding_id: str
    gross_tonnage: float
    tare_tonnage: float
    expected_tonnage: float

class AirQualityInput(BaseModel):
    station_id: str
    pm10: float
    pm25: float
    methane_ch4: float

# --- Embedded Production PWA UI ---

HTML_PROD_UI = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>MinePulse AI - Industrial Mining Compliance</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://unpkg.com/lucide@latest"></script>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen font-sans flex flex-col antialiased">
  <header class="border-b border-slate-800 bg-slate-900/90 backdrop-blur sticky top-0 z-50 p-4">
    <div class="max-w-7xl mx-auto flex items-center justify-between">
      <div class="flex items-center space-x-3">
        <span class="p-2.5 bg-amber-500/10 border border-amber-500/30 text-amber-500 rounded-xl font-bold">⛏️</span>
        <div>
          <h1 class="font-bold text-white text-base">MinePulse <span class="text-amber-500">AI</span> <span class="text-[10px] text-slate-400 bg-slate-800 px-2 py-0.5 rounded ml-1 font-mono">v2.0-PROD</span></h1>
          <p class="text-[11px] text-slate-400">Coal India Ltd. • Statutory Smart Governance</p>
        </div>
      </div>
      <div class="flex items-center space-x-2">
        <div id="net-badge" class="flex items-center space-x-1.5 text-[11px] font-mono bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 px-2.5 py-1 rounded-full">
          <span class="w-2 h-2 rounded-full bg-emerald-400"></span>
          <span id="net-status">Online</span>
        </div>
        <button onclick="setTab('dash')" id="tab-btn-dash" class="text-xs px-3 py-1.5 rounded-lg bg-amber-500 text-slate-950 font-bold">Command Center</button>
        <button onclick="setTab('field')" id="tab-btn-field" class="text-xs px-3 py-1.5 rounded-lg bg-slate-800 text-slate-300">Field Inspector</button>
      </div>
    </div>
  </header>

  <main class="max-w-7xl mx-auto p-4 flex-1 w-full space-y-6">
    <!-- DASHBOARD VIEW -->
    <div id="view-dash" class="space-y-6">
      <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
        <div class="p-3.5 bg-slate-900 border border-slate-800 rounded-xl">
          <p class="text-xs text-slate-400">Weighbridge Dispatch Siding</p>
          <h3 class="text-lg font-bold text-white mt-1">42,850 MT</h3>
          <span class="text-[11px] text-rose-400 block mt-1" id="weighbridge-status">Active Variance: -380 MT</span>
        </div>
        <div class="p-3.5 bg-slate-900 border border-slate-800 rounded-xl">
          <p class="text-xs text-slate-400">Statutory Compliance Index</p>
          <h3 class="text-lg font-bold text-emerald-400 mt-1" id="overall-score">--</h3>
          <span class="text-[11px] text-emerald-400 block mt-1">CMR 2017 & DGMS Safe</span>
        </div>
        <div class="p-3.5 bg-slate-900 border border-slate-800 rounded-xl">
          <p class="text-xs text-slate-400">Ledger Audit Observations</p>
          <h3 class="text-lg font-bold text-amber-400 mt-1" id="audit-count">0</h3>
          <span class="text-[11px] text-slate-400 block mt-1" id="queue-count">0 queued offline</span>
        </div>
        <div class="p-3.5 bg-slate-900 border border-slate-800 rounded-xl">
          <p class="text-xs text-slate-400">CAAQMS Telemetry (PM10)</p>
          <h3 class="text-lg font-bold text-rose-400 mt-1" id="telemetry-pm10">168 µg/m³</h3>
          <span class="text-[11px] text-rose-400 block mt-1">Sprinkler Solenoids Engaged</span>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div class="lg:col-span-2 space-y-6">
          <div class="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <h2 class="font-bold text-sm text-white mb-3 flex items-center justify-between">
              <span>Colliery Risk Registry & Geolocation Status</span>
              <span class="text-xs font-mono text-slate-400">PostGIS Coordinates</span>
            </h2>
            <div class="overflow-x-auto">
              <table class="w-full text-left text-xs">
                <thead class="bg-slate-950 text-slate-400 border-b border-slate-800">
                  <tr>
                    <th class="p-2.5">Mine Site</th>
                    <th class="p-2.5">Type</th>
                    <th class="p-2.5">Safety Index</th>
                    <th class="p-2.5">Status</th>
                  </tr>
                </thead>
                <tbody id="mines-list" class="divide-y divide-slate-800"></tbody>
              </table>
            </div>
          </div>
        </div>

        <div class="bg-slate-900 border border-slate-800 rounded-xl p-4 flex flex-col h-full">
          <h2 class="font-bold text-sm text-white mb-3">Live Tamper-Proof Audit Stream</h2>
          <div id="obs-list" class="space-y-2.5 overflow-y-auto max-h-[480px] flex-1 pr-1"></div>
        </div>
      </div>
    </div>

    <!-- FIELD INSPECTION PWA VIEW -->
    <div id="view-field" class="hidden max-w-lg mx-auto bg-slate-900 border border-slate-800 rounded-2xl p-5 space-y-4">
      <div>
        <h2 class="font-bold text-base text-white">Underground & Pit Field Inspection</h2>
        <p class="text-xs text-slate-400">Offline-Enabled Engine (IndexedDB Local Cache)</p>
      </div>

      <div id="offline-alert-box" class="hidden p-3 bg-amber-500/10 border border-amber-500/30 rounded-lg text-xs text-amber-300">
        Pit Mode Active: Zero Network Detected. Observations will cache locally in phone storage and auto-sync on surface connection.
      </div>

      <form onsubmit="handleInspectionSubmit(event)" class="space-y-3 text-xs">
        <div>
          <label class="block text-slate-400 mb-1">Select Target Mine Sector</label>
          <select id="field-sel-mine" class="w-full bg-slate-800 border border-slate-700 p-2.5 rounded-lg text-white outline-none"></select>
        </div>
        <div>
          <label class="block text-slate-400 mb-1">Statutory Norm</label>
          <select id="field-sel-cat" class="w-full bg-slate-800 border border-slate-700 p-2.5 rounded-lg text-white outline-none">
            <option>Ventilation & Methane Standards (CMR 153)</option>
            <option>Bench Slope & Dump Stability (CMR 106)</option>
            <option>Environmental Dust Suppression & CAAQMS</option>
            <option>Contractor Labour & Minimum Wages Act</option>
          </select>
        </div>
        <div>
          <label class="block text-slate-400 mb-1">Observation Ground Details</label>
          <textarea id="field-inp-notes" required rows="3" placeholder="Enter findings or regulatory hazard details..." class="w-full bg-slate-800 border border-slate-700 p-2.5 rounded-lg text-white outline-none"></textarea>
        </div>
        <div class="grid grid-cols-2 gap-2">
          <div>
            <label class="block text-slate-400 mb-1">Severity SLA</label>
            <select id="field-sel-sev" class="w-full bg-slate-800 border border-slate-700 p-2.5 rounded-lg text-white outline-none">
              <option value="Normal">Routine (7-Day Rectification)</option>
              <option value="Medium">Medium Risk (72-Hour SLA)</option>
              <option value="Critical">Critical (Immediate 24h DGMS Escalation)</option>
            </select>
          </div>
          <div>
            <label class="block text-slate-400 mb-1">Hardware GPS</label>
            <button type="button" onclick="lockRealGPS()" id="field-gps-btn" class="w-full bg-slate-800 border border-slate-700 p-2.5 rounded-lg text-emerald-400 font-medium">Acquire Satellite GPS</button>
          </div>
        </div>
        <button type="submit" class="w-full bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold p-3 rounded-xl transition mt-2">
          Commit to SHA-256 Audit Trail
        </button>
      </form>
    </div>
  </main>

  <script>
    let lat = 23.7412, lng = 86.4189;
    let dbInstance = null;

    // --- IndexedDB Offline Setup ---
    function initIndexedDB() {
      const request = indexedDB.open("MinePulseLocalDB", 1);
      request.onupgradeneeded = (e) => {
        const db = e.target.result;
        if (!db.objectStoreNames.contains("pending_observations")) {
          db.createObjectStore("pending_observations", { keyPath: "client_id" });
        }
      };
      request.onsuccess = (e) => {
        dbInstance = e.target.result;
        checkAndSyncQueue();
      };
    }

    function saveToIndexedDB(item) {
      return new Promise((resolve, reject) => {
        const tx = dbInstance.transaction("pending_observations", "readwrite");
        const store = tx.objectStore("pending_observations");
        store.put(item);
        tx.oncomplete = () => resolve();
        tx.onerror = () => reject(tx.error);
      });
    }

    function getPendingQueue() {
      return new Promise((resolve) => {
        if (!dbInstance) return resolve([]);
        const tx = dbInstance.transaction("pending_observations", "readonly");
        const store = tx.objectStore("pending_observations");
        const req = store.getAll();
        req.onsuccess = () => resolve(req.result || []);
      });
    }

    function clearQueueItem(client_id) {
      return new Promise((resolve) => {
        const tx = dbInstance.transaction("pending_observations", "readwrite");
        const store = tx.objectStore("pending_observations");
        store.delete(client_id);
        tx.oncomplete = () => resolve();
      });
    }

    // --- Auto-Sync Engine ---
    async function checkAndSyncQueue() {
      if (!navigator.onLine) return;
      const pending = await getPendingQueue();
      document.getElementById('queue-count').innerText = `${pending.length} queued offline`;
      
      if (pending.length > 0) {
        for (const item of pending) {
          try {
            const res = await fetch('/api/v1/inspections/batch', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify(item)
            });
            if (res.ok) {
              await clearQueueItem(item.client_id);
            }
          } catch (e) {
            console.warn("Sync retry scheduled", e);
          }
        }
        await loadRemoteData();
      }
    }

    window.addEventListener('online', () => {
      document.getElementById('net-status').innerText = "Online";
      document.getElementById('net-badge').className = "flex items-center space-x-1.5 text-[11px] font-mono bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 px-2.5 py-1 rounded-full";
      document.getElementById('offline-alert-box').classList.add('hidden');
      checkAndSyncQueue();
    });

    window.addEventListener('offline', () => {
      document.getElementById('net-status').innerText = "Offline (Pit Mode)";
      document.getElementById('net-badge').className = "flex items-center space-x-1.5 text-[11px] font-mono bg-amber-500/10 text-amber-400 border border-amber-500/20 px-2.5 py-1 rounded-full";
      document.getElementById('offline-alert-box').classList.remove('hidden');
    });

    // --- Load Data from Server ---
    async function loadRemoteData() {
      try {
        const [mRes, oRes] = await Promise.all([
          fetch('/api/v1/collieries'),
          fetch('/api/v1/inspections')
        ]);
        const mines = await mRes.json();
        const audits = await oRes.json();

        document.getElementById('mines-list').innerHTML = mines.map(m => `
          <tr class="hover:bg-slate-900/50">
            <td class="p-2.5 font-medium text-white">${m.name} <span class="text-[10px] text-slate-400 block">${m.id} • ${m.subsidiary}</span></td>
            <td class="p-2.5 text-slate-300 text-xs">${m.mine_type}</td>
            <td class="p-2.5"><span class="px-2 py-0.5 rounded text-[11px] font-bold ${m.risk_level === 'Safe' ? 'bg-emerald-500/10 text-emerald-400' : 'bg-rose-500/10 text-rose-400'}">${m.compliance_score}%</span></td>
            <td class="p-2.5 text-xs">${m.risk_level}</td>
          </tr>
        `).join('');

        document.getElementById('field-sel-mine').innerHTML = mines.map(m => `<option value="${m.id}">${m.name}</option>`).join('');
        
        const avg = (mines.reduce((acc, x) => acc + x.compliance_score, 0) / mines.length).toFixed(1);
        document.getElementById('overall-score').innerText = `${avg} / 100`;
        document.getElementById('audit-count').innerText = audits.length;

        document.getElementById('obs-list').innerHTML = audits.length ? audits.map(a => `
          <div class="p-3 bg-slate-950 border border-slate-800 rounded-lg text-xs space-y-1">
            <div class="flex justify-between items-center text-slate-400">
              <strong class="text-white">${a.mine_name}</strong>
              <span class="text-[10px] font-mono">${a.timestamp}</span>
            </div>
            <p class="text-slate-300">${a.notes}</p>
            <div class="text-[10px] font-mono text-emerald-400 flex justify-between pt-1 border-t border-slate-800">
              <span>${a.category}</span>
              <span>GPS: ${a.latitude.toFixed(4)}, ${a.longitude.toFixed(4)}</span>
            </div>
            <div class="text-[9px] font-mono text-slate-500 truncate">SHA: ${a.sha256_hash}</div>
          </div>
        `).join('') : '<p class="text-xs text-slate-500">No logs present.</p>';

      } catch (err) {
        console.warn("Device offline, viewing cached UI");
      }
    }

    function lockRealGPS() {
      const btn = document.getElementById('field-gps-btn');
      btn.innerText = "Locking Satellites...";
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
          (pos) => {
            lat = pos.coords.latitude;
            lng = pos.coords.longitude;
            btn.innerText = `${lat.toFixed(4)}° N, ${lng.toFixed(4)}° E`;
          },
          () => {
            btn.innerText = "Pit Boundary Locked";
          },
          { enableHighAccuracy: true, timeout: 5000 }
        );
      }
    }

    async function handleInspectionSubmit(e) {
      e.preventDefault();
      const payload = {
        client_id: `CLI-${Date.now()}-${Math.floor(Math.random()*1000)}`,
        mine_id: document.getElementById('field-sel-mine').value,
        category: document.getElementById('field-sel-cat').value,
        notes: document.getElementById('field-inp-notes').value,
        severity: document.getElementById('field-sel-sev').value,
        latitude: lat,
        longitude: lng,
        recorded_at: new Date().toISOString()
      };

      if (!navigator.onLine) {
        await saveToIndexedDB(payload);
        alert("OFFLINE STORAGE: Network absent. Observation secured locally in phone's IndexedDB. Will auto-sync upon reaching surface network.");
      } else {
        try {
          const res = await fetch('/api/v1/inspections/batch', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
          });
          if (res.ok) {
            alert("SUCCESS: Observation committed to SHA-256 Audit Trail on Central CIL Registry.");
          }
        } catch {
          await saveToIndexedDB(payload);
          alert("Network failure. Saved safely in local offline cache.");
        }
      }

      document.getElementById('field-inp-notes').value = '';
      setTab('dash');
      await checkAndSyncQueue();
      await loadRemoteData();
    }

    function setTab(t) {
      document.getElementById('view-dash').classList.toggle('hidden', t === 'field');
      document.getElementById('view-field').classList.toggle('hidden', t !== 'field');
      document.getElementById('tab-btn-dash').className = t === 'dash' ? 'text-xs px-3 py-1.5 rounded-lg bg-amber-500 text-slate-950 font-bold' : 'text-xs px-3 py-1.5 rounded-lg bg-s
