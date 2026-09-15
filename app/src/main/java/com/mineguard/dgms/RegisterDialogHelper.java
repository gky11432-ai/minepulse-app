package com.mineguard.dgms;

import android.content.Context;
import android.content.SharedPreferences;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;
import com.google.android.material.dialog.MaterialAlertDialogBuilder;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;

public class RegisterDialogHelper {

    private static final String PREF_NAME = "MineGuard_Statutory_Prefs";

    public static void showEntryDialog(Context context, String moduleKey, String moduleTitle) {
        MaterialAlertDialogBuilder builder = new MaterialAlertDialogBuilder(context);
        builder.setTitle(moduleTitle);

        LinearLayout layout = new LinearLayout(context);
        layout.setOrientation(LinearLayout.VERTICAL);
        layout.setPadding(50, 20, 50, 10);

        TextView tvSub = new TextView(context);
        tvSub.setText("Mines Act 1952 & CMR 2017 Compliance Entry");
        tvSub.setTextSize(11);
        tvSub.setTextColor(0xFF94A3B8);
        tvSub.setPadding(0, 0, 0, 20);
        layout.addView(tvSub);

        EditText etLocation = new EditText(context);
        etLocation.setHint("District / Working Seam Location");
        etLocation.setTextSize(13);
        layout.addView(etLocation);

        EditText etObservation = new EditText(context);
        etObservation.setHint("Safety Observation / Test Reading");
        etObservation.setTextSize(13);
        layout.addView(etObservation);

        TextView tvStatusLbl = new TextView(context);
        tvStatusLbl.setText("Compliance Status:");
        tvStatusLbl.setTextSize(12);
        tvStatusLbl.setTextColor(0xFFCBD5E1);
        tvStatusLbl.setPadding(0, 20, 0, 10);
        layout.addView(tvStatusLbl);

        Spinner spStatus = new Spinner(context);
        String[] options = {
            "✅ SATISFACTORY & SAFE",
            "⚠️ ATTENTION REQUIRED",
            "⛔ WORK STOPPED (DANGER)"
        };
        ArrayAdapter<String> adapter = new ArrayAdapter<>(context, android.R.layout.simple_spinner_dropdown_item, options);
        spStatus.setAdapter(adapter);
        layout.addView(spStatus);

        builder.setView(layout);

        builder.setPositiveButton("Sign & Certify", (dialog, which) -> {
            String loc = etLocation.getText().toString().trim();
            String obs = etObservation.getText().toString().trim();
            String status = spStatus.getSelectedItem().toString();

            if (loc.isEmpty() || obs.isEmpty()) {
                Toast.makeText(context, "कृपया सभी विवरण भरें!", Toast.LENGTH_SHORT).show();
                return;
            }

            saveRecord(context, moduleKey, loc, obs, status);
            Toast.makeText(context, "✅ " + moduleTitle + " प्रमाणित एवं सुरक्षित किया गया!", Toast.LENGTH_SHORT).show();
        });

        builder.setNegativeButton("Cancel", (dialog, which) -> dialog.dismiss());
        builder.show();
    }

    private static void saveRecord(Context context, String key, String loc, String obs, String status) {
        SharedPreferences prefs = context.getSharedPreferences(PREF_NAME, Context.MODE_PRIVATE);
        String time = new SimpleDateFormat("dd/MM/yyyy HH:mm:ss", Locale.getDefault()).format(new Date());
        String newRecord = time + " | " + loc + " | " + status + " | " + obs;

        String oldLogs = prefs.getString("log_" + key, "");
        String updatedLogs = newRecord + "\n" + oldLogs;

        prefs.edit().putString("log_" + key, updatedLogs).apply();
    }

    public static String getLatestLog(Context context, String key) {
        SharedPreferences prefs = context.getSharedPreferences(PREF_NAME, Context.MODE_PRIVATE);
        return prefs.getString("log_" + key, "No records logged yet.");
    }
}
