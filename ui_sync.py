# ui_sync.py - High-Capacity IndexedDB Vault & Auto-Sync Engine (Online + Offline Hybrid)

SYNC_SCRIPT = """
<script>
(function() {
    var DB_NAME = 'MineGuard_Statutory_Vault';
    var DB_VERSION = 1;
    var db = null;
    var SYNC_API_ENDPOINT = 'https://minepulse-app.onrender.com/api/sync/bulk';
    var isSyncing = false;

    // 1. Initialize High-Capacity IndexedDB (No 5MB Limit)
    function initIndexedDB() {
        var request = indexedDB.open(DB_NAME, DB_VERSION);

        request.onupgradeneeded = function(event) {
            var d = event.target.result;
            if (!d.objectStoreNames.contains('records')) {
                d.createObjectStore('records', { keyPath: 'id' });
            }
            if (!d.objectStoreNames.contains('sync_queue')) {
                var queueStore = d.createObjectStore('sync_queue', { keyPath: 'queueId', autoIncrement: true });
                queueStore.createIndex('synced', 'synced', { unique: false });
            }
        };

        request.onsuccess = function(event) {
            db = event.target.result;
            flushLocalStorageToIndexedDB();
            checkAndSyncWithCloud();
        };

        request.onerror = function() {
            console.warn('[MineGuard DB] IndexedDB unavailable, fallback active.');
        };
    }

    // 2. Mirror & Upgrade: Automatically pushes every statutory save into IndexedDB & Sync Queue
    var originalSetItem = localStorage.setItem;
    localStorage.setItem = function(key, value) {
        originalSetItem.apply(this, arguments);

        if (key.startsWith('dgms_') && db) {
            try {
                var parsed = JSON.parse(value);
                if (Array.isArray(parsed) && parsed.length > 0) {
                    var latestRecord = parsed[0];
                    latestRecord.registerCategory = key;
                    latestRecord.localTimestamp = Date.now();

                    var tx = db.transaction(['records', 'sync_queue'], 'readwrite');
                    tx.objectStore('records').put(latestRecord);
                    tx.objectStore('sync_queue').add({
                        register: key,
                        payload: latestRecord,
                        synced: 0,
                        created: Date.now()
                    });

                    tx.oncomplete = function() {
                        updateSyncBadge('OFFLINE_BUFFERED');
                        if (navigator.onLine) {
                            checkAndSyncWithCloud();
                        }
                    };
                }
            } catch(e) {}
        }
    };

    function flushLocalStorageToIndexedDB() {
        if (!db) return;
        var keys = Object.keys(localStorage);
        keys.forEach(function(k) {
            if (k.startsWith('dgms_')) {
                try {
                    var items = JSON.parse(localStorage.getItem(k) || '[]');
                    if (Array.isArray(items)) {
                        var tx = db.transaction(['records'], 'readwrite');
                        var store = tx.objectStore('records');
                        items.forEach(function(rec) {
                            if (rec && rec.id) {
                                rec.registerCategory = k;
                                store.put(rec);
                            }
                        });
                    }
                } catch(e) {}
            }
        });
    }

    // 3. Online Auto-Sync Dispatcher
    window.checkAndSyncWithCloud = function() {
        if (!navigator.onLine || isSyncing || !db) return;
        isSyncing = true;
        updateSyncBadge('SYNCING');

        var tx = db.transaction(['sync_queue'], 'readwrite');
        var store = tx.objectStore('sync_queue');
        var req = store.getAll();

        req.onsuccess = function() {
            var queue = req.result || [];
            var unsynced = queue.filter(function(item) { return item.synced === 0; });

            if (unsynced.length === 0) {
                isSyncing = false;
                updateSyncBadge('ALL_SYNCED');
                return;
            }

            // Push pending offline logs to Cloud Server
            fetch(SYNC_API_ENDPOINT, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ batch: unsynced })
            }).then(function(res) {
                if (res.ok) {
                    var clearTx = db.transaction(['sync_queue'], 'readwrite');
                    var qStore = clearTx.objectStore('sync_queue');
                    unsynced.forEach(function(item) {
                        item.synced = 1;
                        qStore.put(item);
                    });
                    clearTx.oncomplete = function() {
                        isSyncing = false;
                        updateSyncBadge('ALL_SYNCED');
                    };
                } else {
                    isSyncing = false;
                    updateSyncBadge('OFFLINE_BUFFERED');
                }
            }).catch(function() {
                isSyncing = false;
                updateSyncBadge('OFFLINE_BUFFERED');
            });
        };

        req.onerror = function() {
            isSyncing = false;
        };
    };

    function updateSyncBadge(state) {
        var el = document.getElementById('mineguard-sync-indicator');
        if (!el) return;

        if (state === 'ALL_SYNCED') {
            el.innerHTML = '🟢 <b>ONLINE</b> • Cloud Synced';
            el.style.background = '#064e3b';
            el.style.color = '#34d399';
            el.style.borderColor = '#059669';
        } else if (state === 'SYNCING') {
            el.innerHTML = '🔄 <b>UPLOADING</b> • Syncing Vault...';
            el.style.background = '#1e3a5f';
            el.style.color = '#38bdf8';
            el.style.borderColor = '#0284c7';
        } else {
            el.innerHTML = '🟠 <b>OFFLINE</b> • Stored in Vault';
            el.style.background = '#451a03';
            el.style.color = '#fbbf24';
            el.style.borderColor = '#d97706';
        }
    }

    // Network State Listeners (Auto Trigger)
    window.addEventListener('online', function() {
        updateSyncBadge('SYNCING');
        setTimeout(window.checkAndSyncWithCloud, 1200);
    });

    window.addEventListener('offline', function() {
        updateSyncBadge('OFFLINE_BUFFERED');
    });

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initIndexedDB);
    } else {
        initIndexedDB();
    }
})();
</script>
"""
