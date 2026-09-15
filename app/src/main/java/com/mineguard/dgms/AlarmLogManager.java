package com.mineguard.dgms;

import android.content.Context;
import android.content.SharedPreferences;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.Locale;
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
        public boolean isDanger;

        public AuditEntry(String id, String time, String name, String offId, String role, String cat, String rem, boolean danger) {
            this.entryId = id;
            this.timestamp = time;
            this.officerName = name;
            this.officerId = offId;
            this.role = role;
            this.category = cat;
            this.remarks = rem;
            this.isDanger = danger;
        }
    }

    public AlarmLogManager(Context context) {
        this.prefs = context.getSharedPreferences(PREF_AUDIT, Context.MODE_PRIVATE);
    }

    public AuditEntry logLocalEntry(String name, String id, String role, String cat, String remarks) {
        return logLocalEntry(name, id, role, cat, remarks, false);
    }

    public AuditEntry logLocalEntry(String name, String id, String role, String cat, String remarks, boolean danger) {
        String entryId = UUID.randomUUID().toString().substring(0, 8);
        String time = new SimpleDateFormat("dd/MM/yy HH:mm", Locale.getDefault()).format(new Date());
        AuditEntry entry = new AuditEntry(entryId, time, name, id, role, cat, remarks, danger);
        saveEntry(entry);
        return entry;
    }

    public boolean mergeRemoteEntry(String entryId, String time, String name, String offId, String role, String cat, String rem) {
        return mergeRemoteEntry(entryId, time, name, offId, role, cat, rem, false);
    }

    public boolean mergeRemoteEntry(String entryId, String time, String name, String offId, String role, String cat, String rem, boolean danger) {
        List<AuditEntry> existing = getAllEntries();
        for (AuditEntry e : existing) {
            if (e.entryId.equalsIgnoreCase(entryId)) return false;
        }
        AuditEntry newEntry = new AuditEntry(entryId, time, name, offId, role, cat, rem, danger);
        saveEntry(newEntry);
        return true;
    }

    private synchronized void saveEntry(AuditEntry e) {
        String serialized = e.entryId + "###" + e.timestamp + "###" + e.officerName + "###" 
                + e.officerId + "###" + e.role + "###" + e.category + "###" + e.remarks + "###" + e.isDanger;
        String existing = prefs.getString(KEY_LOG_ENTRIES, "");
        prefs.edit().putString(KEY_LOG_ENTRIES, serialized + "\n" + existing).apply();
    }

    public List<AuditEntry> getAllEntries() {
        List<AuditEntry> list = new ArrayList<>();
        String raw = prefs.getString(KEY_LOG_ENTRIES, "");
        if (raw.trim().isEmpty()) return list;

        for (String line : raw.split("\n")) {
            String[] p = line.split("###");
            if (p.length >= 8) {
                list.add(new AuditEntry(p[0], p[1], p[2], p[3], p[4], p[5], p[6], Boolean.parseBoolean(p[7])));
            } else if (p.length >= 7) {
                list.add(new AuditEntry(p[0], p[1], p[2], p[3], p[4], p[5], p[6], false));
            }
        }
        return list;
    }

    public List<AuditEntry> getEntriesByCategory(String targetCategory) {
        List<AuditEntry> filtered = new ArrayList<>();
        for (AuditEntry entry : getAllEntries()) {
            if (entry.category.equalsIgnoreCase(targetCategory)) {
                filtered.add(entry);
            }
        }
        return filtered;
    }

    public void logAlarmEvent(String officerName, String officerId, String role, String triggerType) {
        logLocalEntry(officerName, officerId, role, "SIREN", triggerType, true);
    }

    public List<AuditEntry> getAlarmHistory() {
        return getEntriesByCategory("SIREN");
    }
}
