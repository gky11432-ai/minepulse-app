# ui_offline.py - Robust Offline Vault, Reliable Ping & Auto-Sync Engine

OFFLINE_SCRIPT = """
  <script>
    let audioCtx = null;
    let sirenOsc = null;
    let vibInterval = null;
    let isTrulyOnline = navigator.onLine;

    // 1. IndexedDB Local Vault
    let dbInstance = null;
    function initDB() {
      return new Promise((resolve) => {
        if (dbInstance) return resolve(dbInstance);
        const req = indexedDB.open('MinePulseLocalVault', 1);
        req.onupgradeneeded = (e) => {
          const db = e.target.result;
          if (!db.objectStoreNames.contains('inspections')) {
            db.createObjectStore('inspections', { keyPath: 'client_id' });
          }
        };
        req.onsuccess = (e) => {
          dbInstance = e.target.result;
          resolve(dbInstance);
        };
        req.onerror = () => resolve(null);
      });
    }

    async function dbPut(record) {
      try {
        const db = await initDB();
        if (!db) return;
        const tx = db.transaction('inspections', 'readwrite');
        tx.objectStore('inspections').put(record);
      } catch(e){}
    }

    async function dbGetAll() {
      try {
        const db = await initDB();
        if (!db) return [];
        return new Promise((res) => {
          const tx = db.transaction('inspections', 'readonly');
          const req = tx.objectStore('inspections').getAll();
          req.onsuccess = () => res(req.result || []);
          req.onerror = () => res([]);
        });
      } catch(e) {
        return [];
      }
    }

    // 2. Real Network Ping & UI Update (Using GET instead of HEAD)
    function setOnlineUI() {
      isTrulyOnline = true;
      const badge = document.getElementById('net-badge');
      const label = document.getElementById('net-label');
      if (badge) {
        badge.innerText = 'ONLINE';
        badge.className = 'ml-2 text-[10px] px-2 py-0.5 rounded-full font-bold bg-emerald-950 text-emerald-400 border border-emerald-800';
      }
      if (label) {
        label.innerText = 'Cloud Synced';
        label.className = 'text-base sm:text-lg font-bold text-emerald-400 mt-1';
      }
      if (typeof syncOfflineRecords === 'function') {
        syncOfflineRecords();
      }
    }

    function setOfflineUI() {
      isTrulyOnline = false;
      const badge = document.getElementById('net-badge');
      const label = document.getElementById('net-label');
      if (badge) {
        badge.innerText = 'OFFLINE (PIT MODE)';
        badge.className = 'ml-2 text-[10px] px-2 py-0.5 rounded-full font-bold bg-rose-950 text-rose-400 border border-rose-800 animate-pulse';
      }
      if (label) {
        label.innerText = 'Local Storage Only';
        label.className = 'text-base sm:text-lg font-bold text-amber-400 mt-1';
      }
    }

    async function checkTrueNetwork() {
      if (!navigator.onLine) {
        setOfflineUI();
        return;
      }
      try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 2000);
        // GET request use ho rahi hai with cache burst
        const resp = await fetch('/api/collieries?t=' + Date.now(), { 
          method: 'GET', 
          signal: controller.signal 
        });
        clearTimeout(timeoutId);
        if (resp.ok) {
          setOnlineUI();
        } else {
          setOfflineUI();
        }
      } catch (err) {
        setOfflineUI();
      }
    }

    // Initial state set on page load
    if (navigator.onLine) {
      setOnlineUI();
    } else {
      setOfflineUI();
    }

    window.addEventListener('online', checkTrueNetwork);
    window.addEventListener('offline', setOfflineUI);

    // 3. Audio Siren Synth & Hardware Vibration
    function triggerHardwareVibration() {
      if ('vibrate' in navigator) {
        navigator.vibrate([1000, 300, 1000, 300, 1500]);
        if (!vibInterval) {
          vibInterval = setInterval(() => {
            navigator.vibrate([1000, 300, 1000, 300, 1500]);
          }, 4500);
        }
      }
    }

    function playAudioSiren() {
      try {
        triggerHardwareVibration();
        if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        if (sirenOsc) return;

        sirenOsc = audioCtx.createOscillator();
        const gainNode = audioCtx.createGain();
        sirenOsc.type = 'sawtooth';

        const now = audioCtx.currentTime;
        sirenOsc.frequency.setValueAtTime(800, now);
        sirenOsc.frequency.linearRampToValueAtTime(1200, now + 0.4);
        sirenOsc.frequency.linearRampToValueAtTime(800, now + 0.8);
        sirenOsc.frequency.linearRampToValueAtTime(1200, now + 1.2);

        gainNode.gain.setValueAtTime(0.20, now);
        sirenOsc.connect(gainNode);
        gainNode.connect(audioCtx.destination);
        sirenOsc.start();
        const banner = document.getElementById('siren-banner');
        if (banner) banner.classList.remove('hidden');
      } catch (err) {}
    }

    function silenceSiren() {
      if (sirenOsc) {
        try { sirenOsc.stop(); } catch(e){}
        sirenOsc = null;
      }
      if (vibInterval) {
        clearInterval(vibInterval);
        vibInterval = null;
      }
      if ('vibrate' in navigator) navigator.vibrate(0);
      const banner = document.getElementById('siren-banner');
      if (banner) banner.classList.add('hidden');
    }

    function triggerBroadcastSOS() {
      playAudioSiren();
      if (isTrulyOnline) {
        fetch('/api/broadcast/trigger', { method: 'POST' }).catch(() => {});
      }
      alert('🚨 DGMS EMERGENCY ALARM ACTIVATED!\\n\\nContinuous horn & vibration active locally.');
    }

    // 4. Auto-Sync Queue Safe Execution
    async function syncOfflineRecords() {
      if (!isTrulyOnline) return;
      const allRecords = await dbGetAll();
      const pending = allRecords.filter(r => r.sync_pending);
      if (pending.length === 0) return;

      for (const item of pending) {
        try {
          const res = await fetch('/api/inspections', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(item)
          });
          if (res.ok) {
            item.sync_pending = false;
            await dbPut(item);
          }
        } catch(e) {
          setOfflineUI();
          break;
        }
      }
      if (typeof load === 'function') load();
    }

    function forceSync() {
      if (!isTrulyOnline) {
        alert('Abhi phone offline hai. Network aane par Sync karein.');
        return;
      }
      syncOfflineRecords();
    }
  </script>
"""
