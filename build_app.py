# build_app.py - Standalone HTML Production Assembler (< 50 Lines)

import os
from app_core import CORE_HEAD, CORE_FOOT
from app_nav import NAV_MODULE
from app_siren import SIREN_MODULE
from app_drawer import DRAWER_MODULE
from app_modules import MODULES_ENGINE
from app_reports import REPORTS_MODULE

def assemble_production_html():
    full_html = (
        CORE_HEAD +
        NAV_MODULE +
        SIREN_MODULE +
        DRAWER_MODULE +
        MODULES_ENGINE +
        REPORTS_MODULE +
        CORE_FOOT
    )
    
    # 1. Root index.html
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(full_html)
    print("✅ Successfully generated: index.html")
    
    # 2. Android WebView assets folder (if exists)
    android_asset_dir = os.path.join("app", "src", "main", "assets")
    if os.path.exists(android_asset_dir):
        dest = os.path.join(android_asset_dir, "index.html")
        with open(dest, "w", encoding="utf-8") as f:
            f.write(full_html)
        print(f"✅ Successfully synced: {dest}")

if __name__ == "__main__":
    assemble_production_html()
  
