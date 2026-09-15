package com.mineguard.dgms;

import android.content.Context;
import android.content.SharedPreferences;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.Locale;

public class AlarmLogManager {
    private static final String PREF_ALARM_LOG = "MineGuard_Alarm_Audits";
    private static final String KEY_LOGS = "alarm_event_history";
    private final SharedPreferences prefs;

    public static class AlarmEntry {
        public String timestamp;
        public String officerName;
        public String officerId;
        public String role;
        public String triggerType;

        public AlarmEntry(String timestamp, String officerName, String officerId, String role, String triggerType) {
            this.timestamp = timestamp;
            this.officerName = officerName;
            this.officerId = officerId;
            this.role = role;
            this.triggerType = triggerType;
        }
    }

    public AlarmLogManager(Context context) {
        this.prefs = context.getSharedPreferences(PREF_ALARM_LOG, Context.MODE_PRIVATE);
    }

    public void logAlarmEvent(String officerName, String officerId, String role, String triggerType) {
        String time = new SimpleDateFormat("dd/MM/yyyy HH:mm:ss", Locale.getDefault()).format(new Date());
        String serialized = time + "###" + officerName + "###" + officerId + "###" + role + "###" + triggerType;

        String oldLogs = prefs.getString(KEY_LOGS, "");
        String updated = serialized + "\n" + oldLogs;
        prefs.edit().putString(KEY_LOGS, updated).apply();
    }

    public List<AlarmEntry> getAlarmHistory() {
        List<AlarmEntry> list = new ArrayList<>();
        String raw = prefs.getString(KEY_LOGS, "");
        if (raw.isEmpty()) return list;

        String[] lines = raw.split("\n");
        for (String line : lines) {
            String[] parts = line.split("###");
            if (parts.length >= 5) {
                list.add(new AlarmEntry(parts[0], parts[1], parts[2], parts[3], parts[4]));
            }
        }
        return list;
    }
}
