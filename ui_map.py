# ui_map.py - Dedicated High-Definition Tactical GIS Spatial Pit Map Engine

MAP_SCRIPT = """
  <script>
    var mapAnimFrame = null;
    var radarAngle = 0;

    function drawMap() {
      var cv = document.getElementById('mine-map-canvas');
      if (!cv || !cv.getContext) return;
      var ctx = cv.getContext('2d');

      var rect = cv.getBoundingClientRect();
      var dpr = window.devicePixelRatio || 1;
      var w = rect.width || (cv.parentElement ? cv.parentElement.clientWidth : 340);
      var h = 180;

      cv.width = w * dpr;
      cv.height = h * dpr;
      ctx.scale(dpr, dpr);

      // Deep Mine Topographic Background
      ctx.fillStyle = '#050c1a';
      ctx.fillRect(0, 0, w, h);

      // Mining Survey Grid Lines
      ctx.strokeStyle = '#0f233a';
      ctx.lineWidth = 1;
      for (var x = 0; x < w; x += 35) { ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, h); ctx.stroke(); }
      for (var y = 0; y < h; y += 30) { ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(w, y); ctx.stroke(); }

      // Opencast Quarry Bench Contours
      var cx = w * 0.5;
      var cy = h * 0.52;

      var contours = [
        { rx: w * 0.42, ry: 65, color: '#163354' },
        { rx: w * 0.32, ry: 48, color: '#1a416d' },
        { rx: w * 0.20, ry: 30, color: '#235691' }
      ];

      contours.forEach(function(c) {
        ctx.beginPath();
        ctx.ellipse(cx, cy, c.rx, c.ry, 0, 0, Math.PI * 2);
        ctx.strokeStyle = c.color;
        ctx.lineWidth = 1.5;
        ctx.stroke();
      });

      // Statutory DGMS Leasehold Geofence
      ctx.beginPath();
      var bL = w * 0.08, bR = w * 0.92, bT = 16, bB = h - 18;
      ctx.moveTo(bL, bT);
      ctx.lineTo(bR, bT);
      ctx.lineTo(bR - 15, bB);
      ctx.lineTo(bL + 15, bB);
      ctx.closePath();
      ctx.strokeStyle = '#ef4444';
      ctx.lineWidth = 2;
      ctx.fillStyle = 'rgba(239, 68, 68, 0.08)';
      ctx.fill();
      ctx.stroke();

      // Radar Sweep Effect
      radarAngle += 0.04;
      ctx.save();
      ctx.beginPath();
      ctx.moveTo(cx, cy);
      ctx.arc(cx, cy, Math.min(w * 0.4, 75), radarAngle, radarAngle + 0.5);
      ctx.closePath();
      ctx.fillStyle = 'rgba(16, 185, 129, 0.18)';
      ctx.fill();
      ctx.restore();

      // Pit Active Beacon Pin
      ctx.fillStyle = '#10b981';
      ctx.beginPath();
      ctx.arc(cx, cy, 5, 0, Math.PI * 2);
      ctx.fill();

      // Beacon Ping Ring
      var pingR = 7 + (Math.sin(Date.now() / 250) + 1) * 3;
      ctx.strokeStyle = 'rgba(16, 185, 129, 0.6)';
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      ctx.arc(cx, cy, pingR, 0, Math.PI * 2);
      ctx.stroke();

      // Geotags & Statutory Identifiers
      ctx.fillStyle = '#f8fafc';
      ctx.font = 'bold 11px monospace';
      ctx.fillText('SECL GEVRA SECTOR B', bL + 8, bT + 16);

      ctx.fillStyle = '#38bdf8';
      ctx.font = '9px monospace';
      ctx.fillText('Lat: 22.3541°N | Long: 82.6821°E [CMR 106 Safe]', bL + 8, bT + 29);

      ctx.fillStyle = '#f87171';
      ctx.font = '9px sans-serif';
      ctx.fillText('DGMS Highwall Lease Boundary', bR - 165, bB - 6);
    }

    function startMapLoop() {
      if (mapAnimFrame) cancelAnimationFrame(mapAnimFrame);
      function loop() {
        var cv = document.getElementById('mine-map-canvas');
        var vd = document.getElementById('vd');
        if (cv && vd && !vd.classList.contains('hidden')) {
          drawMap();
        }
        mapAnimFrame = requestAnimationFrame(loop);
      }
      loop();
    }

    window.addEventListener('resize', drawMap);
    window.addEventListener('DOMContentLoaded', startMapLoop);
  </script>
"""
