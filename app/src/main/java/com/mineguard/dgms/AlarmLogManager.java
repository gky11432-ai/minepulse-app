package com.mineguard.dgms;

import android.content.Context;
import android.content.SharedPreferences;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.HashSet;
import java.util.List;
import java.util.Locale;
import java.util.Set;
import java.util.UUID;

public class AlarmLogManager {
    private static final String PREF_AUDIT = "MineGuard_Shared_Audits";
    private static final String KEY_LOG_ENTRIES = "colliery_master_entries";
    private final SharedPreferences prefs;

    public static class AuditEntry {
        public String entryId;
        public String timestamp;
        public String officerName;
        public String officerId;
        public String role;
        public String category;
        public String remarks;

        public AuditEntry(String id, String time, String name, String offId, String role, String cat, String rem) {
            this.entryId = id;
            this.timestamp = time;
            this.officerName = name;
            this.officerId = offId;
            this.role = role;
            this.category = cat;
            this.remarks = rem;
        }
    }

    public AlarmLogManager(Context context) {
        this.prefs = context.getSharedPreferences(PREF_AUDIT, Context.MODE_PRIVATE);
    }

    // New entry created on THIS phone
    public AuditEntry logLocalEntry(String name, String id, String role, String cat, String remarks) {
        String entryId = UUID.randomUUID().toString().substring(0, 8);
        String time = new SimpleDateFormat("dd/MM/yy HH:mm", Locale.getDefault()).format(new Date());
        AuditEntry entry = new AuditEntry(entryId, time, name, id, role, cat, remarks);
        saveEntry(entry);
        return entry;
    }

    // Remote entry received from OTHER phone (via Online MQTT or Offline BLE)
    public boolean mergeRemoteEntry(String entryId, String time, String name, String offId, String role, String cat, String rem) {
        List<AuditEntry> existing = getAllEntries();
        for (AuditEntry e : existing) {
            if (e.entryId.equalsIgnoreCase(entryId)) return false; // Already present
        }
        AuditEntry newEntry = new AuditEntry(entryId, time, name, offId, role, cat, rem);
        saveEntry(newEntry);
        return true;
    }

    private synchronized void saveEntry(AuditEntry e) {
        String serialized = e.entryId + "###" + e.timestamp + "###" + e.officerName + "###" 
                + e.officerId + "###" + e.role + "###" + e.category + "###" + e.remarks;
        String existing = prefs.getString(KEY_LOG_ENTRIES, "");
        String updated = serialized + "\n" + existing;
        prefs.edit().putString(KEY_LOG_ENTRIES, updated).apply();
    }

    public List<AuditEntry> getAllEntries() {
        List<AuditEntry> list = new ArrayList<>();
        String raw = prefs.getString(KEY_LOG_ENTRIES, "");
        if (raw.trim().isEmpty()) return list;

        String[] lines = raw.split("\n");
        for (String line : lines) {
            String[] p = line.split("###");
            if (p.length >= 7) {
                list.add(new AuditEntry(p[0], p[1], p[2], p[3], p[4], p[5], p[6]));
            }
        }
        return list;
    }

    public void logAlarmEvent(String officerName, String officerId, String role, String triggerType) {
        logLocalEntry(officerName, officerId, role, "EMERGENCY_SOS", triggerType);
    }

    public List<AuditEntry> getAlarmHistory() {
        return getAllEntries();
    }
}
