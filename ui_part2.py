# ui_part2.py - Autonomous Native Logic & Harsh DGMS Industrial Klaxon Horn

PART2 = """
  <script>
    var audioCtx = null;
    var sirenOsc = null;
    var sirenGain = null;
    var sirenTimer = null;
    var vibInterval = null;
    var isOnline = false;

    var LOCAL_MINES = [
      { id: 'SECL-GV-04', name: 'Gevra Sector B (SECL)', subsidiary: 'SECL', mine_type: 'Opencast', compliance_score: 94 },
      { id: 'BCCL-JH-07', name: 'Jharia Pit 7 (BCCL)', subsidiary: 'BCCL', mine_type: 'Underground', compliance_score: 83 },
      { id: 'ECL-RJ-02', name: 'Rajmahal Deep (ECL)', subsidiary: 'ECL', mine_type: 'Opencast', compliance_score: 88 }
    ];

    // 1. IndexedDB Storage
    function getDB() {
      return new Promise(function(resolve) {
        var req = indexedDB.open('MinePulseLocalDB_v2', 1);
        req.onupgradeneeded = function(e) {
          e.target.result.createObjectStore('logs', { keyPath: 'client_id' });
        };
        req.onsuccess = function(e) { resolve(e.target.result); };
        req.onerror = function() { resolve(null); };
      });
    }

    async function dbPut(item) {
      var db = await getDB();
      if (!db) return;
      var tx = db.transaction('logs', 'readwrite');
      tx.objectStore('logs').put(item);
    }

    async function dbGetAll() {
      var db = await getDB();
      if (!db) return [];
      return new Promise(function(resolve) {
        var tx = db.transaction('logs', 'readonly');
        var req = tx.objectStore('logs').getAll();
        req.onsuccess = function() { resolve(req.result || []); };
        req.onerror = function() { resolve([]); };
      });
    }

    // 2. Network State Switcher
    function setNetState(online) {
      isOnline = online;
      var b = document.getElementById('net-badge');
      var l = document.getElementById('net-label');
      if (online) {
        if (b) { b.innerText = 'ONLINE'; b.className = 'badge badge-on'; }
        if (l) { l.innerText = 'Cloud Synced'; l.style.color = '#34d399'; }
        syncPending();
      } else {
        if (b) { b.innerText = 'OFFLINE (PIT MODE)'; b.className = 'badge badge-off'; }
        if (l) { l.innerText = 'Local Storage Only'; l.style.color = '#f87171'; }
      }
    }

    async function checkPing() {
      if (!navigator.onLine) {
        setNetState(false);
        return;
      }
      try {
        var ctrl = new AbortController();
        var tid = setTimeout(function() { ctrl.abort(); }, 1200);
        var r = await fetch('/api/collieries?t=' + Date.now(), { signal: ctrl.signal, cache: 'no-store' });
        clearTimeout(tid);
        setNetState(r.ok);
      } catch(e) {
        setNetState(false);
      }
    }

    window.addEventListener('online', checkPing);
    window.addEventListener('offline', function() { setNetState(false); });

    // 3. Hard Industrial Klaxon Alarm (Zero-Music, Harsh Danger Tone)
    function initAudio() {
      if (!audioCtx) {
        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
      }
      if (audioCtx.state === 'suspended') {
        audioCtx.resume();
      }
    }

    function triggerHardwareVibration() {
      if ('vibrate' in navigator) {
        navigator.vibrate([600, 200, 600, 200, 900]);
        if (!vibInterval) {
          vibInterval = setInterval(function() {
            navigator.vibrate([600, 200, 600, 200, 900]);
          }, 2500);
        }
      }
    }

    function playAudioSiren() {
      try {
        initAudio();
        triggerHardwareVibration();

        if (sirenOsc) return;

        // Harsh Square waveform (Industrial buzzer / Klaxon sound)
        sirenOsc = audioCtx.createOscillator();
        sirenGain = audioCtx.createGain();
        sirenOsc.type = 'square';

        var highTone = true;
        sirenOsc.frequency.setValueAtTime(950, audioCtx.currentTime);
        sirenGain.gain.setValueAtTime(0.40, audioCtx.currentTime);

        sirenOsc.connect(sirenGain);
        sirenGain.connect(audioCtx.destination);
        sirenOsc.start();

        // Rapid dual-pitch harsh pulse (No musical glides)
        sirenTimer = setInterval(function() {
          if (!sirenOsc || !audioCtx) return;
          var t = audioCtx.currentTime;
          highTone = !highTone;
          // Switches instantly between 950 Hz and 600 Hz
          sirenOsc.frequency.setValueAtTime(highTone ? 950 : 600, t);
        }, 220);

        var b = document.getElementById('siren-banner');
        if (b) b.classList.remove('hidden');
      } catch(e) {
        console.error('Audio engine start failed:', e);
      }
    }

    function silenceSiren() {
      if (sirenOsc) {
        try { sirenOsc.stop(); } catch(e){}
        sirenOsc = null;
      }
      if (sirenTimer) {
        clearInterval(sirenTimer);
        sirenTimer = null;
      }
      if (vibInterval) {
        clearInterval(vibInterval);
        vibInterval = null;
      }
      if ('vibrate' in navigator) navigator.vibrate(0);
      var b = document.getElementById('siren-banner');
      if (b) b.classList.add('hidden');
    }

    function triggerBroadcastSOS() {
      initAudio();
      playAudioSiren();
      if (isOnline) fetch('/api/broadcast/trigger', { method: 'POST' }).catch(function(){});
      alert('🚨 DGMS STATUTORY DANGER EVACUATION ALARM ENGAGED!\\n\\nContinuous klaxon horn and vibration active.');
    }

    // 4. Map Drawing (Native Canvas)
    function drawMap() {
      var cv = document.getElementById('mine-map-canvas');
      if (!cv || !cv.getContext) return;
      var ctx = cv.getContext('2d');
      var w = cv.width = cv.offsetWidth;
      var h = cv.height = 120;
      ctx.clearRect(0, 0, w, h);

      ctx.strokeStyle = '#1e293b';
      for (var x = 0; x < w; x += 30) { ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, h); ctx.stroke(); }
      for (var y = 0; y < h; y += 30) { ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(w, y); ctx.stroke(); }

      ctx.fillStyle = 'rgba(239, 68, 68, 0.15)';
      ctx.strokeStyle = '#ef4444';
      ctx.fillRect(w * 0.2, 20, w * 0.6, 80);
      ctx.strokeRect(w * 0.2, 20, w * 0.6, 80);

      ctx.fillStyle = '#10b981';
      ctx.beginPath();
      ctx.arc(w * 0.5, 60, 6, 0, Math.PI * 2);
      ctx.fill();

      ctx.fillStyle = '#fff';
      ctx.font = '11px sans-serif';
      ctx.fillText('SECL Gevra Pit [Safe Leasehold]', w * 0.2 + 8, 38);
    }

    // 5. Data Loader & Render
    async function load() {
      var mines = LOCAL_MINES;
      var obs = await dbGetAll();

      if (isOnline) {
        try {
          var ctrl = new AbortController();
          var tid = setTimeout(function() { ctrl.abort(); }, 1200);
          var res = await Promise.all([
            fetch('/api/collieries', { signal: ctrl.signal }),
            fetch('/api/inspections', { signal: ctrl.signal })
          ]);
          clearTimeout(tid);
          if (res[0].ok) mines = await res[0].json();
          if (res[1].ok) {
            var cloudObs = await res[1].json();
            for (var i = 0; i < cloudObs.length; i++) {
              await dbPut(Object.assign({}, cloudObs[i], { sync_pending: false }));
            }
            obs = await dbGetAll();
          }
        } catch(e) {
          setNetState(false);
        }
      }

      var pending = obs.filter(function(o) { return o.sync_pending; }).length;
      var sn = document.getElementById('sync-notice');
      if (sn) {
        sn.classList.toggle('hidden', pending === 0);
        var pc = document.getElementById('pending-count');
        if (pc) pc.innerText = pending;
      }

      var tc = document.getElementById('tc');
      if (tc) tc.innerText = obs.length;

      var sm = document.getElementById('sm');
      if (sm) {
        sm.innerHTML = mines.map(function(m) {
          return '<option value="' + m.id + '">' + m.name + '</option>';
        }).join('');
      }

      var ol = document.getElementById('ol');
      if (ol) {
        if (obs.length === 0) {
          ol.innerHTML = '<p style="color:#64748b; font-size:12px;">No inspection logs stored yet.</p>';
        } else {
          ol.innerHTML = obs.slice().reverse().map(function(o) {
            var tag = o.sync_pending ? '<span style="color:#f59e0b; font-weight:bold;">[SAVED OFFLINE]</span>' : '<span style="color:#34d399; font-weight:bold;">[CLOUD VERIFIED]</span>';
            return '<div style="background:#020617; border:1px solid #1e293b; border-radius:8px; padding:10px; display:flex; justify-content:space-between; align-items:center; font-size:12px;">' +
              '<div>' +
                '<div style="font-weight:bold; color:#fff;">' + (o.mine_name || 'Gevra Sector B') + ': ' + (o.notes || '') + '</div>' +
                '<div style="color:#f59e0b; font-size:10px; margin-top:2px;">Officer: ' + (o.officer_name || '') + ' (' + (o.officer_role || '') + ')</div>' +
                '<div style="color:#64748b; font-size:9px; font-family:monospace;">SEAL: ' + (o.sha256_hash || '').slice(0, 20) + '...</div>' +
              '</div>' +
              '<div style="text-align:right;">' +
                '<div style="color:#64748b; font-size:10px;">' + (o.timestamp || '') + '</div>' +
                tag +
              '</div>' +
            '</div>';
          }).join('');
        }
      }

      drawMap();
    }

    // 6. Form Save
    async function save(e) {
      e.preventDefault();
      var smEl = document.getElementById('sm');
      var sev = document.getElementById('ss') ? document.getElementById('ss').value : 'Normal';
      var rec = {
        client_id: 'CLI-' + Date.now(),
        mine_id: smEl ? smEl.value : 'SECL-GV-04',
        mine_name: (smEl && smEl.options[smEl.selectedIndex]) ? smEl.options[smEl.selectedIndex].text : 'Gevra Sector B (SECL)',
        officer_name: document.getElementById('soname').value,
        officer_role: document.getElementById('sorole').value,
        dgms_cert_no: document.getElementById('socert').value,
        category: document.getElementById('scat').value,
        notes: document.getElementById('sn').value,
        severity: sev,
        latitude: 22.3541,
        longitude: 82.6821,
        timestamp: new Date().toLocaleTimeString(),
        sha256_hash: 'SEAL_' + Math.random().toString(36).substring(2).toUpperCase(),
        sync_pending: !isOnline
      };

      await dbPut(rec);

      if (isOnline) {
        try {
          var res = await fetch('/api/inspections', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(rec)
          });
          if (res.ok) {
            rec.sync_pending = false;
            await dbPut(rec);
          }
        } catch(err) {
          setNetState(false);
        }
      }

      if (sev === 'Critical') {
        initAudio();
        playAudioSiren();
      }

      alert(isOnline ? 'DGMS Inspection saved & uploaded to Cloud!' : '⚠️ OFFLINE: Inspection saved in Phone Vault! Will auto-sync when online.');
      document.getElementById('sn').value = '';
      tab('dash');
      load();
    }

    // 7. Auto-Sync
    async function syncPending() {
      if (!isOnline) return;
      var all = await dbGetAll();
      var pending = all.filter(function(o) { return o.sync_pending; });
      if (pending.length === 0) return;

      for (var i = 0; i < pending.length; i++) {
        try {
          var r = await fetch('/api/inspections', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(pending[i])
          });
          if (r.ok) {
            pending[i].sync_pending = false;
            await dbPut(pending[i]);
          }
        } catch(e) {
          setNetState(false);
          break;
        }
      }
      load();
    }

    function forceSync() {
      if (!isOnline) {
        alert('Abhi network nahi mila hai.');
        return;
      }
      syncPending();
    }

    function triggerSimulatedHazard() {
      var ch4 = document.getElementById('tel-ch4');
      if (ch4) { ch4.innerText = '1.84 % (CRITICAL)'; ch4.style.color = '#ef4444'; }
      initAudio();
      playAudioSiren();
      if (isOnline) fetch('/api/telemetry/trigger-gas-spike', { method: 'POST' }).catch(function(){});
    }

    function runSensors() {
      setInterval(function() {
        var ch4 = (0.15 + Math.random() * 0.15).toFixed(2);
        var co = Math.floor(10 + Math.random() * 8);
        var pm = Math.floor(65 + Math.random() * 20);
        var vib = (0.01 + Math.random() * 0.03).toFixed(2);
        var e1 = document.getElementById('tel-ch4'); if (e1) e1.innerText = ch4 + ' %';
        var e2 = document.getElementById('tel-co'); if (e2) e2.innerText = co + ' ppm';
        var e3 = document.getElementById('tel-pm'); if (e3) e3.innerText = pm + ' ug/m3';
        var e4 = document.getElementById('tel-vib'); if (e4) e4.innerText = vib + ' mm/s';
      }, 5000);
    }

    function tab(t) {
      var vd = document.getElementById('vd');
      var vf = document.getElementById('vf');
      var bd = document.getElementById('bd');
      var bf = document.getElementById('bf');
      if (vd) vd.classList.toggle('hidden', t === 'field');
      if (vf) vf.classList.toggle('hidden', t !== 'field');
      if (bd) bd.className = (t === 'dash') ? 'btn-action active' : 'btn-action';
      if (bf) bf.className = (t === 'field') ? 'btn-action active' : 'btn-action';
      if (t === 'dash') drawMap();
    }

    setNetState(navigator.onLine);
    window.onload = async function() {
      document.body.addEventListener('click', initAudio, { once: true });
      document.body.addEventListener('touchstart', initAudio, { once: true });
      await checkPing();
      await load();
      runSensors();
      setInterval(checkPing, 6000);
    };
  </script>
</body>
</html>
"""
