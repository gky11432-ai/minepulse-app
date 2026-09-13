# ⛏️ MinePulse AI — Industrial Mining Safety & Compliance Engine

MinePulse AI is an enterprise-grade statutory compliance and edge telemetry platform designed for coal mining environments (Coal India Ltd. subsidiaries: SECL, BCCL, ECL) under the **Mines Act 1952** and **Coal Mines Regulations (CMR 2017)**.

The system bridges physical colliery pit hardware (weighbridges, CAAQMS dust monitors, NDIR methane sensors) with zero-network offline resilience, mathematical spatial validation, and cryptographic audit logging for **DGMS Form-VI** inspections.

---

## 🏗️ Technical Architecture

```text
[ Physical Weighbridge / RS-232 / TCP ]
                    │
                    ▼
[ Edge Gateway Ingestion (Termux / Linux Node) ]
                    │
                    ├──► [ Zero-Network Offline SQLite Buffer ]
                    │
                    ▼
[ Continuous Cloud Sync Daemon (SHA-256 Hashing) ]
                    │
                    ▼  (HTTPS / TLS)
[ Central Cloud Engine (FastAPI on Render) ]
    ├──► Ray-Casting Polygon Geofencing (SECL Gevra Boundary)
    ├──► DGMS Officer DSC & Licensing Validation
    ├──► Automated Emergency Siren Webhooks
    └──► Printable DGMS Form-VI Inspection Register
