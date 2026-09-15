package com.mineguard.dgms;

import android.content.Context;
import android.content.SharedPreferences;

public class AuthManager {
    private static final String PREF_AUTH = "MineGuard_Auth_Session";
    private static final String KEY_LOGGED_IN = "is_logged_in";
    private static final String KEY_OFFICER_NAME = "officer_name";
    private static final String KEY_OFFICER_ID = "officer_id";
    private static final String KEY_OFFICER_ROLE = "officer_role";
    private static final String KEY_OFFICER_PIN = "officer_pin";

    private final SharedPreferences prefs;

    public AuthManager(Context context) {
        this.prefs = context.getSharedPreferences(PREF_AUTH, Context.MODE_PRIVATE);
    }

    public boolean isLoggedIn() {
        return prefs.getBoolean(KEY_LOGGED_IN, false);
    }

    public boolean authenticate(String officerId, String name, String role, String pin) {
        String savedPin = prefs.getString(KEY_OFFICER_PIN, null);

        // First-time setup: registers the officer and sets PIN
        if (savedPin == null) {
            prefs.edit()
                    .putBoolean(KEY_LOGGED_IN, true)
                    .putString(KEY_OFFICER_NAME, name)
                    .putString(KEY_OFFICER_ID, officerId)
                    .putString(KEY_OFFICER_ROLE, role)
                    .putString(KEY_OFFICER_PIN, pin)
                    .apply();
            return true;
        }

        // Subsequent logins: verify PIN & ID
        if (savedPin.equals(pin)) {
            prefs.edit()
                    .putBoolean(KEY_LOGGED_IN, true)
                    .putString(KEY_OFFICER_NAME, name)
                    .putString(KEY_OFFICER_ID, officerId)
                    .putString(KEY_OFFICER_ROLE, role)
                    .apply();
            return true;
        }
        return false;
    }

    public void logout() {
        prefs.edit().putBoolean(KEY_LOGGED_IN, false).apply();
    }

    public String getOfficerName() {
        return prefs.getString(KEY_OFFICER_NAME, "Statutory Official");
    }

    public String getOfficerId() {
        return prefs.getString(KEY_OFFICER_ID, "CMR-OFFICER");
    }

    public String getOfficerRole() {
        return prefs.getString(KEY_OFFICER_ROLE, "Mining Sirdar (CMR 48)");
    }
}
