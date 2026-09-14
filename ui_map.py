# ui_map.py - Standalone Tactical Pit Radar & Geofence Map Component

PART_MAP = """
      <!-- High-Definition Tactical Pit Map Component -->
      <div class="card">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
          <div>
            <span style="font-size:13px; font-weight:bold;">Autonomous Spatial Geofence Grid</span>
            <span style="font-size:10px; color:#34d399; margin-left:6px;">● Live Pit Telemetry</span>
          </div>
          <span style="font-size:10px; color:#94a3b8; font-family:monospace;">SECL GEVRA SECTOR B</span>
        </div>
        
        <div style="width:100%; height:200px; background:#050c1a; border-radius:8px; border:1px solid #1e293b; overflow:hidden; position:relative;">
          <svg viewBox="0 0 600 210" preserveAspectRatio="xMidYMid meet" style="width:100%; height:100%; display:block;">
            <defs>
              <pattern id="surveyGrid" width="30" height="30" patternUnits="userSpaceOnUse">
                <path d="M 30 0 L 0 0 0 30" fill="none" stroke="#0e2338" stroke-width="0.8"/>
              </pattern>
              <linearGradient id="radarSweepGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#10b981" stop-opacity="0.35"/>
                <stop offset="100%" stop-color="#10b981" stop-opacity="0"/>
              </linearGradient>
            </defs>

            <!-- Background Grid -->
            <rect width="600" height="210" fill="#050c1a"/>
            <rect width="600" height="210" fill="url(#surveyGrid)"/>

            <!-- DGMS Statutory Leasehold Perimeter -->
            <polygon points="45,20 555,20 535,190 65,190" fill="rgba(239, 68, 68, 0.07)" stroke="#ef4444" stroke-width="1.8" stroke-dasharray="6,4"/>

            <!-- Highwall Terraces / Opencast Benches -->
            <ellipse cx="300" cy="105" rx="210" ry="72" fill="none" stroke="#16385c" stroke-width="1.5"/>
            <ellipse cx="300" cy="105" rx="145" ry="48" fill="none" stroke="#1d4b7c" stroke-width="1.5"/>
            <ellipse cx="300" cy="105" rx="75" ry="26" fill="none" stroke="#2563eb" stroke-width="1.2"/>

            <!-- Haul Road Ramp Track -->
            <path d="M 90,170 Q 220,130 300,105" fill="none" stroke="#f59e0b" stroke-width="2" stroke-dasharray="4,3"/>

            <!-- Radar Scanner Beam (Rotating) -->
            <g class="radar-rotator">
              <path d="M 300 105 L 390 65 A 100 100 0 0 1 400 105 Z" fill="url(#radarSweepGrad)"/>
            </g>

            <!-- Active Colliery Beacon Station Pin -->
            <circle cx="300" cy="105" r="5" fill="#10b981"/>
            <circle class="beacon-pulse" cx="300" cy="105" r="10" fill="none" stroke="#34d399" stroke-width="2"/>

            <!-- Text Data Overlays -->
            <text x="58" y="38" fill="#f8fafc" font-size="11" font-weight="bold" font-family="monospace">SECL GEVRA PIT - SECTOR B</text>
            <text x="58" y="52" fill="#38bdf8" font-size="9" font-family="monospace">Lat: 22.3541°N | Long: 82.6821°E [DGMS Safe Zone]</text>
            <text x="310" y="100" fill="#10b981" font-size="9" font-weight="bold" font-family="sans-serif">Central Sump Beacon</text>
            <text x="100" y="180" fill="#f59e0b" font-size="8" font-family="sans-serif">Main Incline Haul Road</text>
            <text x="390" y="182" fill="#f87171" font-size="9" font-family="sans-serif">DGMS Highwall Leasehold Boundary</text>
          </svg>
        </div>
      </div>

      <!-- Tamper-Proof Audit Ledger Header -->
      <div class="card">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
          <span style="font-size:13px; font-weight:bold;">Tamper-Proof Audit Ledger (SHA-256)</span>
          <button onclick="load()" style="background:#1e293b; color:#cbd5e1; border:1px solid #334155; padding:4px 8px; border-radius:6px; font-size:11px; cursor:pointer;">Refresh</button>
        </div>
        <div id="ol" style="display:flex; flex-direction:column; gap:8px;"></div>
      </div>
    </div>
"""
