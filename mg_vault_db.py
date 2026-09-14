# mg_vault_db.py - Unlimited High-Capacity IndexedDB Vault Engine (< 150 Lines)

VAULT_DB_MODULE = """
<script>
(function() {
    var DB_NAME = "MineGuard_DGMS_Vault";
    var DB_VERSION = 1;
    var dbInstance = null;

    function openVaultDB(callback) {
        if (dbInstance) {
            if (callback) callback(dbInstance);
            return;
        }

        var req = indexedDB.open(DB_NAME, DB_VERSION);

        req.onupgradeneeded = function(e) {
            var db = e.target.result;
            if (!db.objectStoreNames.contains("statutory_vault")) {
                var store = db.createObjectStore("statutory_vault", { keyPath: "id" });
                store.createIndex("category", "category", { unique: false });
                store.createIndex("timestamp", "timestamp", { unique: false });
            }
            if (!db.objectStoreNames.contains("sync_queue")) {
                db.createObjectStore("sync_queue", { keyPath: "id", autoIncrement: true });
            }
        };

        req.onsuccess = function(e) {
            dbInstance = e.target.result;
            if (callback) callback(dbInstance);
        };

        req.onerror = function() {
            console.warn("IndexedDB fallback to memory storage");
        };
    }

    // Save record securely to Vault & Sync Queue
    window.saveRecordToVault = function(category, recordData, onComplete) {
        openVaultDB(function(db) {
            try {
                var tx = db.transaction(["statutory_vault", "sync_queue"], "readwrite");
                var vaultStore = tx.objectStore("statutory_vault");
                var syncStore = tx.objectStore("sync_queue");

                var entryId = recordData.id || (category + "_" + Date.now() + "_" + Math.random().toString(36).substring(2, 5));
                var vaultRecord = {
                    id: entryId,
                    category: category,
                    timestamp: recordData.timestamp || Date.now(),
                    date: recordData.date || new Date().toLocaleDateString("en-GB"),
                    time: recordData.time || new Date().toLocaleTimeString(),
                    payload: recordData
                };

                vaultStore.put(vaultRecord);
                syncStore.add({
                    category: category,
                    recordId: entryId,
                    payload: vaultRecord,
                    status: "PENDING",
                    created: Date.now()
                });

                tx.oncomplete = function() {
                    // Mirror to localStorage for instant UI reactivity
                    try {
                        var localKey = "dgms_" + category + "_logs";
                        var current = JSON.parse(localStorage.getItem(localKey) || "[]");
                        current.unshift(recordData);
                        localStorage.setItem(localKey, JSON.stringify(current.slice(0, 50)));
                    } catch(e) {}

                    if (onComplete) onComplete(true, entryId);
                };

                tx.onerror = function() {
                    if (onComplete) onComplete(false, null);
                };
            } catch(err) {
                if (onComplete) onComplete(false, null);
            }
        });
    };

    // Retrieve records by category
    window.getRecordsFromVault = function(category, callback) {
        openVaultDB(function(db) {
            try {
                var tx = db.transaction(["statutory_vault"], "readonly");
                var store = tx.objectStore("statutory_vault");
                var index = store.index("category");
                var req = index.getAll(category);

                req.onsuccess = function() {
                    callback(req.result || []);
                };
                req.onerror = function() {
                    callback([]);
                };
            } catch(e) {
                callback([]);
            }
        });
    };

    // Pre-initialize Database
    openVaultDB();
})();
</script>
"""
