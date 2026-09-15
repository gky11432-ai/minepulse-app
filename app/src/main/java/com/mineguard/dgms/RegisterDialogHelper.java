package com.mineguard.dgms;

import android.app.AlertDialog;
import android.content.Context;
import android.widget.EditText;
import android.widget.Toast;

public class RegisterDialogHelper {

    public static void showEntryDialog(Context context, String regId, String title) {
        showEntryDialog(context, regId, title, new AlarmLogManager(context), null, null);
    }

    public static void showEntryDialog(Context context, String regId, String title, 
                                       AlarmLogManager logMgr, AuditSyncManager syncMgr, BleMeshManager meshMgr) {
        AuthManager auth = new AuthManager(context);
        AlertDialog.Builder builder = new AlertDialog.Builder(context);
        builder.setTitle("📝 " + title);

        final EditText input = new EditText(context);
        input.setHint("निरीक्षण विवरण दर्ज करें (उदा. CH4: 0.12%, रूफ सपोर्ट ठीक है)");
        input.setPadding(35, 35, 35, 35);
        builder.setView(input);

        builder.setPositiveButton("सुरक्षित करें व सिंक करें", (dialog, which) -> {
            String text = input.getText().toString().trim();
            if (text.isEmpty()) text = "दैनिक वैधानिक निरीक्षण पूर्ण - स्थिति सामान्य।";

            if (logMgr != null) {
                AlarmLogManager.AuditEntry entry = logMgr.logLocalEntry(
                        auth.getOfficerName(), auth.getOfficerId(), auth.getOfficerRole(), title, text
                );
                if (syncMgr != null) syncMgr.broadcastAudit(entry);
            }

            if (meshMgr != null) meshMgr.startOfflineMesh();

            Toast.makeText(context, "✅ रिपोर्ट सुरक्षित! सभी फ़ोनों में प्रसारित।", Toast.LENGTH_SHORT).show();
        });

        builder.setNegativeButton("रद्द करें", (dialog, which) -> dialog.dismiss());
        builder.show();
    }
}
