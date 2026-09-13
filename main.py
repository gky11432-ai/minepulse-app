import hashlib
import json
import urllib.request
from datetime import datetime

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from sqlalchemy import Column, DateTime, Float, String, Text, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


# =========================================================
# DATABASE
# =========================================================

SQLALCHEMY_DATABASE_URL = "sqlite:///./minepulse.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


# =========================================================
# DATABASE MODELS
# =========================================================

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


# =========================================================
# GEVRA LEASE BOUNDARY
# =========================================================

SECL_GEVRA_BOUNDARY = [
    (22.3400, 82.6700),
    (22.3700, 82.6700),
    (22.3700, 82.7100),
    (22.3400, 82.7100)
]


def is_within_mine_lease(lat: float, lon: float, boundary: list) -> bool:
    try:
        n = len(boundary)
        inside = False

        p1x, p1y = boundary[0]

        for i in range(n + 1):
            p2x, p2y = boundary[i % n]

            if lat > min(p1x, p2x):
                if lat <= max(p1x, p2x):
                    if lon <= max(p1y, p2y):

                        if p1x != p2x:
                            xinters = (
                                (lat - p1x)
                                * (p2y - p1y)
                                / (p2x - p1x)
                            ) + p1y

                            if p1y == p2y or lon <= xinters:
                                inside = not inside

            p1x, p1y = p2x, p2y

        return inside

    except Exception:
        return True


# =========================================================
# TELEGRAM EMERGENCY DISPATCH
# =========================================================

def trigger_emergency_dispatch(mine_name: str, issue: str):

    # IMPORTANT:
    # Apna Telegram Bot Token yahan set karein.
    bot_token = "YOUR_TELEGRAM_BOT_TOKEN"

    chat_id = "YOUR_CHAT_ID"

    now_time = datetime.utcnow().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    text = (
        "🚨 MINEPULSE DGMS CRITICAL BREACH\n\n"
        f"Colliery: {mine_name}\n"
        f"Hazard: {issue}\n"
        f"Timestamp: {now_time} UTC\n\n"
        "Action: CMR 2017 Immediate Isolation Triggered."
    )

    try:

        url = (
            f"https://api.telegram.org/bot"
            f"{bot_token}/sendMessage"
        )

        payload = json.dumps({
            "chat_id": chat_id,
            "text": text
        }).encode("utf-8")

        req = urllib.request.Request(
            url,
            data=payload,
            headers={
                "Content-Type": "application/json"
            }
        )

        urllib.request.urlopen(
            req,
            timeout=5
        )

    except Exception as exc:
        print("[DISPATCH ERROR]", exc)


# =========================================================
# INITIAL DATABASE DATA
# =========================================================

def init_db():

    db = SessionLocal()

    try:

        if db.query(Colliery).count() == 0:

            db.add_all([

                Colliery(
                    id="BCCL-JH-01",
                    name="Jharia Colliery Pit 7",
                    subsidiary="BCCL",
                    mine_type="Underground",
                    compliance_score=76.0,
                    risk_level="Moderate"
                ),

                Colliery(
                    id="SECL-GV-04",
                    name="Gevra Opencast Sector B",
                    subsidiary="SECL",
                    mine_type="Opencast",
                    compliance_score=94.5,
                    risk_level="Safe"
                ),

                Colliery(
                    id="ECL-RJ-02",
                    name="Rajmahal Deep OCP",
                    subsidiary="ECL",
                    mine_type="Opencast",
                    compliance_score=68.0,
                    risk_level="Critical"
                )
            ])

            db.commit()

    except Exception as e:
        print("[INIT DB WARNING]", e)

    finally:
        db.close()


init_db()


# =========================================================
# FASTAPI
# =========================================================

app = FastAPI(
    title="MinePulse AI Platform"
)


# =========================================================
# REQUEST MODEL
# =========================================================

class BatchItem(BaseModel):

    client_id: str
    mine_id: str

    officer_name: str = (
        "Automated Telemetry Daemon"
    )

    officer_role: str = (
        "IoT Gateway Service"
    )

    dgms_cert_no: str = (
        "DGMS/SYS/TELEMETRY-01"
    )

    category: str
    notes: str
    severity: str

    latitude: float
    longitude: float


# =========================================================
# HTML DASHBOARD
# =========================================================

HTML_APP = """
<!DOCTYPE html>

<html lang="en">

<head>

<meta charset="UTF-8">

<meta
name="viewport"
content="width=device-width, initial-scale=1.0"
>

<title>MinePulse AI - Industrial Portal</title>

<script src="https://cdn.tailwindcss.com"></script>

</head>


<body class="bg-slate-950 text-slate-100 min-h-screen font-sans flex flex-col">


<header class="border-b border-slate-800 bg-slate-900 sticky top-0 z-50 p-4">

<div class="max-w-7xl mx-auto flex justify-between items-center w-full">

<div class="flex items-center space-x-2">

<span class="text-xl">⛏️</span>

<h1 class="font-bold text-white text-base">
MinePulse
<span class="text-amber-500">AI</span>
</h1>

</div>


<div class="flex space-x-2">

<a
href="/statutory/form-vi"
target="_blank"
class="text-xs px-3 py-1.5 rounded-lg bg-slate-800 border border-slate-700 text-amber-400 font-semibold flex items-center"
>
Export DGMS Form-VI
</a>


<button
onclick="tab('dash')"
id="bd"
class="text-xs px-3 py-1.5 rounded-lg bg-amber-500 text-black font-bold"
>
Dashboard
</button>


<button
onclick="tab('field')"
id="bf"
class="text-xs px-3 py-1.5 rounded-lg bg-slate-800 text-slate-300"
>
Statutory Officer Form
</button>

</div>

</div>

</header>


<main class="max-w-7xl mx-auto p-4 flex-1 w-full space-y-4">


<div id="vd" class="space-y-4">


<div class="grid grid-cols-2 md:grid-cols-4 gap-3">


<div class="p-3 bg-slate-900 border border-slate-800 rounded-xl">

<p class="text-[10px] text-slate-400">
Telegram Bot Siren
</p>

<h3 class="text-lg font-bold text-emerald-400 mt-1">
Live Linked
</h3>

</div>


<div class="p-3 bg-slate-900 border border-slate-800 rounded-xl">

<p class="text-[10px] text-slate-400">
Compliance Index
</p>

<h3
class="text-lg font-bold text-emerald-400 mt-1"
id="sc"
>
--
</h3>

</div>


<div class="p-3 bg-slate-900 border border-slate-800 rounded-xl">

<p class="text-[10px] text-slate-400">
Total Audits
</p>

<h3
class="text-lg font-bold text-amber-400 mt-1"
id="tc"
>
0
</h3>

</div>


<div class="p-3 bg-slate-900 border border-slate-800 rounded-xl">

<p class="text-[10px] text-slate-400">
Tamper Seal
</p>

<h3 class="text-lg font-bold text-emerald-400 mt-1">
SHA-256 Lock
</h3>

</div>

</div>


<div class="bg-slate-900 border border-slate-800 rounded-xl p-4">

<h2 class="font-bold text-sm mb-3">
Collieries Monitoring
</h2>

<div class="overflow-x-auto">

<table class="w-full text-left text-xs">

<tbody
id="ml"
class="divide-y divide-slate-800"
>
</tbody>

</table>

</div>

</div>


<div class="bg-slate-900 border border-slate-800 rounded-xl p-4">

<div class="flex justify-between items-center mb-3">

<h2 class="font-bold text-sm">
Audit Logs & Cryptographic Proof
</h2>

<button
onclick="load()"
class="text-[11px] text-slate-400 hover:text-white bg-slate-800 px-2 py-1 rounded"
>
Refresh Stream
</button>

</div>

<div
id="ol"
class="space-y-2 text-xs"
>
</div>

</div>

</div>


<div
id="vf"
class="hidden max-w-lg mx-auto bg-slate-900 border border-slate-800 rounded-2xl p-5 space-y-4"
>

<h2 class="font-bold text-base">
DGMS Competent Officer Log Form
</h2>


<form
onsubmit="save(event)"
class="space-y-3 text-xs"
>


<div class="grid grid-cols-2 gap-2">


<div>

<label class="text-slate-400 block mb-1">
Officer Name
</label>

<input
id="soname"
required
class="w-full bg-slate-800 p-2 rounded-lg text-white"
value="Er. Gaurav Yadav"
/>

</div>


<div>

<label class="text-slate-400 block mb-1">
Designation / Role
</label>

<select
id="sorole"
class="w-full bg-slate-800 p-2 rounded-lg text-white"
>

<option value="Safety Officer (Overman)">
Safety Officer (Overman)
</option>

<option value="First Class Colliery Manager">
Colliery Manager (1st Class)
</option>

<option value="Dispatch Weighbridge Officer">
Weighbridge Officer
</option>

</select>

</div>

</div>


<div>

<label class="text-slate-400 block mb-1">
DGMS Certificate / License No.
</label>

<input
id="socert"
required
class="w-full bg-slate-800 p-2 rounded-lg text-white font-mono"
value="DGMS/CMR/2017/OM-8492"
/>

</div>


<div>

<label class="text-slate-400 block mb-1">
Target Mine
</label>

<select
id="sm"
class="w-full bg-slate-800 p-2 rounded-lg text-white"
>
</select>

</div>


<div>

<label class="text-slate-400 block mb-1">
Statutory Regulation Category
</label>

<select
id="scat"
class="w-full bg-slate-800 p-2 rounded-lg text-white"
>

<option>
CMR 153: Ventilation & Methane Log
</option>

<option>
CMR 106: Bench Stability & Slope
</option>

<option>
CMR 169: Daily Blasting & Explosives Log
</option>

<option>
CAAQMS: Environmental Dust Standard
</option>

</select>

</div>


<div>

<label class="text-slate-400 block mb-1">
Statutory Observation
</label>

<textarea
id="sn"
required
rows="2"
class="w-full bg-slate-800 p-2 rounded-lg text-white"
placeholder="Hazard or violation detail..."
></textarea>

</div>


<div class="grid grid-cols-2 gap-2">


<div>

<label class="text-slate-400 block mb-1">
Severity
</label>

<select
id="ss"
class="w-full bg-slate-800 p-2 rounded-lg text-white"
>

<option value="Normal">
Routine (Compliant)
</option>

<option value="Critical">
Critical (Immediate Stop Order)
</option>

</select>

</div>


<div>

<label class="text-slate-400 block mb-1">
Lease Boundary Check
</label>

<select
id="sgps"
class="w-full bg-slate-800 p-2 rounded-lg text-emerald-400"
>

<option value="inside">
Inside Gevra Lease
</option>

<option value="outside">
Outside Lease (Geofence Breach)
</option>

</select>

</div>

</div>


<button
type="submit"
class="w-full bg-amber-500 hover:bg-amber-400 text-black font-bold p-3 rounded-xl mt-2"
>
Sign & Commit with DSC Seal
</button>


</form>

</div>

</main>


<script>


async function load() {

try {

const [
mR,
oR
] = await Promise.all([

fetch('/api/collieries'),

fetch('/api/inspections')

]);


const mines = await mR.json();

const obs = await oR.json();


document.getElementById('ml').innerHTML =

(mines || []).map(m => `

<tr>

<td class="p-2 font-semibold">
${m.name} (${m.subsidiary})
</td>

<td class="p-2">
${m.mine_type}
</td>

<td class="p-2 text-emerald-400">
${m.compliance_score}%
</td>

<td class="p-2">
${m.risk_level}
</td>

</tr>

`).join('');


document.getElementById('sm').innerHTML =

(mines || []).map(m => `

<option value="${m.id}">
${m.name}
</option>

`).join('');


document.getElementById('tc').innerText =
(obs || []).length;


if (mines && mines.length > 0) {

document.getElementById('sc').innerText =

(

mines.reduce(
(a, b) => a + b.compliance_score,
0
)
/
mines.length

).toFixed(1) + '%';

}


document.getElementById('ol').innerHTML =

(obs || []).map(o => `

<div
class="p-2.5 bg-slate-900 border border-slate-800 rounded flex justify-between items-center"
>

<div>

<div>
<strong>
${o.mine_name || 'Mine'}
</strong>:

${o.notes || ''}
</div>

<div class="text-[10px] text-amber-400">

Officer:
${o.officer_name || ''}

(${o.officer_role || ''})

|

Cert:
${o.dgms_cert_no || ''}

</div>

<div class="text-[10px] text-slate-500 font-mono">

SEAL:
${(o.sha256_hash || '').slice(0, 20)}...

</div>

</div>


<div class="text-right">

<span
class="text-slate-400 text-[10px] block"
>
${o.timestamp || ''}
</span>

<span
class="text-[10px] ${
o.is_valid
? 'text-emerald-400'
: 'text-rose-500 font-bold'
} font-mono"
>

${
o.is_valid
? 'SEAL VERIFIED'
: 'TAMPER DETECTED'
}

</span>

</div>

</div>

`).join('')

||

'<p class="text-slate-500">
No audits yet.
</p>';


}

catch (err) {

console.error(err);

}

}


async function save(e) {

e.preventDefault();


const mode =
document.getElementById('sgps').value;


const lat =
mode === 'inside'
? 22.3541
: 28.6139;


const lng =
mode === 'inside'
? 82.6821
: 77.2090;


const res = await fetch(
'/api/inspections',
{

method: 'POST',

headers: {
'Content-Type': 'application/json'
},

body: JSON.stringify({

client_id:
'CLI-' + Date.now(),

mine_id:
document.getElementById('sm').value,

officer_name:
document.getElementById('soname').value,

officer_role:
document.getElementById('sorole').value,

dgms_cert_no:
document.getElementById('socert').value,

category:
document.getElementById('scat').value,

notes:
document.getElementById('sn').value,

severity:
document.getElementById('ss').value,

latitude: lat,

longitude: lng

})

});


if (!res.ok) {

const err =
await res.json();

alert(
'SUBMISSION REJECTED: '
+
err.detail
);

return;

}


alert(
'Statutory Inspection Signed & Sealed successfully!'
);


document.getElementById('sn').value = '';

tab('dash');

load();

}


function tab(t) {

document
.getElementById('vd')
.classList
.toggle('hidden', t === 'field');


document
.getElementById('vf')
.classList
.toggle('hidden', t !== 'field');


document.getElementById('bd').className =

t === 'dash'

? 'text-xs px-3 py-1.5 rounded-lg bg-amber-500 text-black font-bold'

: 'text-xs px-3 py-1.5 rounded-lg bg-slate-800 text-slate-300';


document.getElementById('bf').className =

t === 'field'

? 'text-xs px-3 py-1.5 rounded-lg bg-amber-500 text-black font-bold'

: 'text-xs px-3 py-1.5 rounded-lg bg-slate-800 text-slate-300';

}


window.onload = load;


</script>


</body>

</html>
"""


# =========================================================
# FORM VI PAGE
# =========================================================

FORM_VI_PAGE = """
<!DOCTYPE html>

<html>

<head>

<title>
DGMS Form-VI Statutory Inspection Register
</title>

<style>

body {
    font-family: 'Times New Roman', serif;
    padding: 25px;
    color: #111;
}

.header {
    text-align: center;
    border-bottom: 2px solid #000;
    padding-bottom: 10px;
    margin-bottom: 20px;
}

table {
    width: 100%;
    border-collapse: collapse;
    text-align: left;
    font-size: 12px;
}

th {
    border: 1px solid #000;
    padding: 8px;
    background: #f0f0f0;
}

td {
    border: 1px solid #000;
    padding: 8px;
}

.footer {
    margin-top: 40px;
    display: flex;
    justify-content: space-between;
    font-size: 12px;
}

.critical {
    color: red;
    font-weight: bold;
}

.normal {
    color: black;
}

.hash {
    font-family: monospace;
    font-size: 9px;
    word-break: break-all;
}

@media print {

    button {
        display: none;
    }

}

</style>

</head>


<body>


<div class="header">

<h2 style="margin: 0;">
DIRECTORATE GENERAL OF MINES SAFETY (DGMS)
</h2>

<h3 style="margin: 5px 0;">
STATUTORY INSPECTION & BREACH REGISTER (FORM-VI)
</h3>

<p style="margin: 0; font-size: 12px;">
Under Coal Mines Regulations (CMR 2017) & Mines Act 1952
</p>

</div>


<div style="margin-bottom: 15px; text-align: right;">

<button
onclick="window.print()"
style="
padding: 6px 12px;
background: #2563eb;
color: white;
border: none;
border-radius: 4px;
cursor: pointer;
"
>
Print / Save as PDF
</button>

</div>


<table>

<thead>

<tr>

<th>Date & Time</th>

<th>Colliery Name</th>

<th>Inspecting Officer & DGMS Lic.</th>

<th>Statutory Category</th>

<th>Observations & Findings</th>

<th>Risk Class</th>

<th>SHA-256 Verification</th>

</tr>

</thead>


<tbody>

__ROWS_PLACEHOLDER__

</tbody>


</table>


<div class="footer">

<div>

<p>
Generated by:
<strong>
MinePulse Statutory AI Engine
</strong>
</p>

<p>
Certified Cryptographically Valid Logbook
</p>

</div>


<div style="text-align: right;">

<p>
_____________________________________
</p>

<p>
<strong>
Colliery Manager / Safety Officer Signature
</strong>
</p>

<p>
Certified DGMS Competent Person
</p>

</div>

</div>


</body>

</html>
"""


# =========================================================
# ROUTES
# =========================================================

@app.get(
    "/",
    response_class=HTMLResponse
)
def root():

    return HTMLResponse(
        content=HTML_APP
    )


# =========================================================
# GET COLLIERIES
# =========================================================

@app.get("/api/collieries")
def get_collieries():

    db = SessionLocal()

    try:

        return db.query(
            Colliery
        ).all()

    finally:

        db.close()


# =========================================================
# GET INSPECTIONS
# =========================================================

@app.get("/api/inspections")
def get_inspections():

    db = SessionLocal()

    try:

        res = (
            db.query(InspectionAudit)
            .order_by(
                InspectionAudit.timestamp.desc()
            )
            .all()
        )

        out = []

        for a in res:

            try:

                time_val = (
                    a.timestamp.strftime(
                        "%Y-%m-%d %H:%M"
                    )
                    if a.timestamp
                    else "N/A"
                )

            except Exception:

                time_val = "N/A"


            out.append({

                "id": str(a.id or ""),

                "mine_name":
                    str(
                        a.mine_name
                        or "Unknown Mine"
                    ),

                "officer_name":
                    str(
                        a.officer_name
                        or "Officer"
                    ),

                "officer_role":
                    str(
                        a.officer_role
                        or "Inspector"
                    ),

                "dgms_cert_no":
                    str(
                        a.dgms_cert_no
                        or "N/A"
                    ),

                "category":
                    str(
                        a.category
                        or "General"
                    ),

                "notes":
         
