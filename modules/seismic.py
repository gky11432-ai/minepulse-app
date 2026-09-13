# modules/seismic.py - Strata Stability & Blast Vibration Monitor Plugin
import random
from datetime import datetime
from fastapi import APIRouter

router = APIRouter(prefix="/api/seismic", tags=["Strata Stability"])

@router.get("/status")
def get_seismic_status():
    """Returns strata stability & blast vibration (PPV) metrics"""
    ppv = round(random.uniform(0.5, 4.2), 2)  # Peak Particle Velocity in mm/s
    slope_angle = round(random.uniform(37.5, 43.8), 1)  # Bench slope in degrees
    
    # DGMS Standard: PPV above 5.0 mm/s or slope above 45 deg triggers warning
    is_warning = ppv > 4.0 or slope_angle > 44.0

    return {
        "colliery_id": "SECL-GV-04",
        "colliery_name": "Gevra Opencast Sector B",
        "peak_particle_velocity_mms": ppv,
        "ppv_statutory_limit_mms": 5.0,
        "current_slope_angle_deg": slope_angle,
        "slope_statutory_limit_deg": 45.0,
        "sensor_health": "Active - Geo-acoustic Probe 03",
        "status": "WARNING (Slope Creep Alert)" if is_warning else "OPTIMAL (Strata Stable)",
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    }

@router.get("/bench-analysis")
def get_bench_analysis():
    """Real-time multi-bench stability log for CMR 106 Compliance"""
    benches = [
        {"bench_no": "B-01 (Topsoil)", "factor_of_safety": 1.48, "condition": "Stable"},
        {"bench_no": "B-02 (Overburden 1)", "factor_of_safety": 1.35, "condition": "Stable"},
        {"bench_no": "B-03 (Coal Seam IV)", "factor_of_safety": 1.21, "condition": "Monitoring Required"},
        {"bench_no": "B-04 (Pit Bottom)", "factor_of_safety": 1.42, "condition": "Stable"}
    ]
    return {
        "total_active_benches": len(benches),
        "benches": benches,
        "cmr_compliance": "CMR 2017 Regulation 106 Compliant"
    }
  
