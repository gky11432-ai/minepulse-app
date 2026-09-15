package com.mineguard.dgms;

import android.app.AlertDialog;
import android.content.Context;
import android.text.InputType;
import android.widget.CheckBox;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;

public class RegisterDialogHelper {

    public static void showDedicatedDialog(Context context, String menuTitle, 
                                          AlarmLogManager logMgr, AuditSyncManager syncMgr, MineSafetyService safetyService) {
        AuthManager auth = new AuthManager(context);
        AlertDialog.Builder builder = new AlertDialog.Builder(context);

        if (menuTitle.contains("Attendance") || menuTitle.contains("Form B") || menuTitle.contains("हाजिरी")) {
            showAttendanceForm(context, builder, auth, logMgr, syncMgr);
        } else if (menuTitle.contains("Ventilation") || menuTitle.contains("Gas") || menuTitle.contains("153")) {
            showGasVentilationForm(context, builder, auth, logMgr, syncMgr, safetyService);
        } else if (menuTitle.contains("Strata") || menuTitle.contains("Roof") || menuTitle.contains("123")) {
            showStrataControlForm(context, builder, auth, logMgr, syncMgr, safetyService);
        } else {
            showGenericStatutoryForm(context, builder, menuTitle, auth, logMgr, syncMgr);
        }
    }

    private static void showAttendanceForm(Context ctx, AlertDialog.Builder b, AuthManager auth, AlarmLogManager logMgr, AuditSyncManager sync) {
        b.setTitle("⏱️ Form B: Statutory Attendance Roll");
        LinearLayout layout = createBaseLayout(ctx);

        final EditText etWorkers = addField(ctx, layout, "कुल कामगार संख्या (Total Present Workers):", "e.g. 42", InputType.TYPE_CLASS_NUMBER);
        final EditText etSection = addField(ctx, layout, "कार्य क्षेत्र / डिपो (Working Face/District):", "e.g. Seam 3 Face A", InputType.TYPE_CLASS_TEXT);

        b.setView(layout);
        b.setPositiveButton("हाजिरी दर्ज करें", (dialog, w) -> {
            String count = etWorkers.getText().toString().trim();
            String sec = etSection.getText().toString().trim();
            if (count.isEmpty()) count = "0";
            String details = "Present Miners: " + count + " | District: " + (sec.isEmpty() ? "Main Seam" : sec);

            saveAndSync(ctx, auth, logMgr, sync, "ATTENDANCE", details, false, null);
            Toast.makeText(ctx, "✅ Form B हाजिरी दर्ज हुई!", Toast.LENGTH_SHORT).show();
        });
        b.setNegativeButton("रद्द करें", (d, w) -> d.dismiss());
        b.show();
    }

    private static void showGasVentilationForm(Context ctx, AlertDialog.Builder b, AuthManager auth, AlarmLogManager logMgr, AuditSyncManager sync, MineSafetyService safety) {
        b.setTitle("💨 CMR 153: Gas & Air Audit");
        LinearLayout layout = createBaseLayout(ctx);

        final EditText etCh4 = addField(ctx, layout, "Methane CH4 (%) [Danger if > 0.75%]:", "e.g. 0.12", InputType.TYPE_CLASS_NUMBER | InputType.TYPE_NUMBER_FLAG_DECIMAL);
        final EditText etCo = addField(ctx, layout, "Carbon Monoxide CO (PPM) [Danger > 50]:", "e.g. 0", InputType.TYPE_CLASS_NUMBER);

        b.setView(layout);
        b.setPositiveButton("ऑडिट सुरक्षित करें", (dialog, w) -> {
            double ch4 = parseDouble(etCh4.getText().toString().trim(), 0.0);
            int co = (int) parseDouble(etCo.getText().toString().trim(), 0.0);

            boolean isDanger = (ch4 >= 0.75 || co >= 50);
            String details = "CH4: " + ch4 + "% | CO: " + co + " PPM | Status: " + (isDanger ? "🚨 CRITICAL DANGER" : "🟢 SAFE");

            saveAndSync(ctx, auth, logMgr, sync, "GAS", details, isDanger, safety);
        });
        b.setNegativeButton("रद्द करें", (d, w) -> d.dismiss());
        b.show();
    }

    private static void showStrataControlForm(Context ctx, AlertDialog.Builder b, AuthManager auth, AlarmLogManager logMgr, AuditSyncManager sync, MineSafetyService safety) {
        b.setTitle("🪨 CMR 123: Strata & Roof Bolting");
        LinearLayout layout = createBaseLayout(ctx);

        final EditText etTension = addField(ctx, layout, "Anchor Load (Tonnes) [Normal > 6.0T]:", "e.g. 8.5", InputType.TYPE_CLASS_NUMBER | InputType.TYPE_NUMBER_FLAG_DECIMAL);
        final CheckBox cbCracks = new CheckBox(ctx);
        cbCracks.setText("रूफ में नई दरारें / साइड फॉल दिखा? (Active Cracks)");
        cbCracks.setTextColor(0xfff87171);
        layout.addView(cbCracks);

        b.setView(layout);
        b.setPositiveButton("स्ट्रैटा रिपोर्ट दर्ज करें", (dialog, w) -> {
            double load = parseDouble(etTension.getText().toString().trim(), 8.0);
            boolean crack = cbCracks.isChecked();
            boolean isDanger = crack || (load < 5.0);

            String details = "Anchor Load: " + load + "T | Cracks: " + (crack ? "YES (HAZARD)" : "NONE") + " | " + (isDanger ? "🚨 ROOF UNSTABLE" : "🟢 SECURE");

            saveAndSync(ctx, auth, logMgr, sync, "STRATA", details, isDanger, safety);
        });
        b.setNegativeButton("रद्द करें", (d, w) -> d.dismiss());
        b.show();
    }

    private static void showGenericStatutoryForm(Context ctx, AlertDialog.Builder b, String title, AuthManager auth, AlarmLogManager logMgr, AuditSyncManager sync) {
        b.setTitle("📝 " + title);
        LinearLayout layout = createBaseLayout(ctx);
        final EditText input = addField(ctx, layout, "निरीक्षण विवरण:", "स्थिति सामान्य है", InputType.TYPE_CLASS_TEXT);

        b.setView(layout);
        b.setPositiveButton("सुरक्षित करें", (dialog, w) -> {
            String text = input.getText().toString().trim();
            saveAndSync(ctx, auth, logMgr, sync, "GENERAL", text.isEmpty() ? "निरीक्षण पूर्ण" : text, false, null);
        });
        b.setNegativeButton("रद्द करें", (d, w) -> d.dismiss());
        b.show();
    }

    private static void saveAndSync(Context ctx, AuthManager auth, AlarmLogManager logMgr, AuditSyncManager sync, String cat, String details, boolean danger, MineSafetyService safety) {
        AlarmLogManager.AuditEntry entry = logMgr.logLocalEntry(auth.getOfficerName(), auth.getOfficerId(), auth.getOfficerRole(), cat, details, danger);
        if (sync != null) sync.broadcastAudit(entry);

        if (danger && safety != null) {
            safety.triggerDualSos();
            Toast.makeText(ctx, "🚨 ख़तरा डिटेक्ट हुआ! आपातकालीन सायरन स्वतः बजाया गया!", Toast.LENGTH_LONG).show();
        } else {
            Toast.makeText(ctx, "✅ रिपोर्ट सुरक्षित व प्रसारित की गई।", Toast.LENGTH_SHORT).show();
        }
    }

    private static LinearLayout createBaseLayout(Context ctx) {
        LinearLayout l = new LinearLayout(ctx);
        l.setOrientation(LinearLayout.VERTICAL);
        l.setPadding(35, 20, 35, 20);
        return l;
    }

    private static EditText addField(Context ctx, LinearLayout parent, String label, String hint, int inputType) {
        TextView tv = new TextView(ctx);
        tv.setText(label);
        tv.setTextSize(12);
        tv.setTextColor(0xff94a3b8);
        tv.setPadding(0, 10, 0, 4);
        parent.addView(tv);

        EditText et = new EditText(ctx);
        et.setHint(hint);
        et.setInputType(inputType);
        et.setTextSize(13);
        parent.addView(et);
        return et;
    }

    private static double parseDouble(String val, double def) {
        try { return Double.parseDouble(val); } catch (Exception e) { return def; }
    }
          }
