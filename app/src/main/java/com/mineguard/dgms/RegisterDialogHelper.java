package com.mineguard.dgms;

import android.app.AlertDialog;
import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

public class RegisterDialogHelper {

    public static void showEntryDialog(Context context, String regId, String title, 
                                       AlarmLogManager logMgr, AuditSyncManager syncMgr, BleMeshManager meshMgr) {
        AuthManager auth = new AuthManager(context);
        AlertDialog.Builder builder = new AlertDialog.Builder(context);
        builder.setTitle("📝 " + title);

        final EditText input = new EditText(context);
        input.setHint("निरीक्षण विवरण दर्ज करें (उदा. CH4: 0.1%, रूफ सपोर्ट ठीक है)");
        input.setPadding(30, 30, 30, 30);
        builder.setView(input);

        builder.setPositiveButton("सुरक्षित करें व सभी फ़ोनों में सिंक करें", (dialog, which) -> {
            String text = input.getText().toString().trim();
            if (text.isEmpty()) text = "दैनिक वैधानिक निरीक्षण पूर्ण - स्थिति सामान्य पाई गई।";

            // 1. Save Locally
            AlarmLogManager.AuditEntry entry = logMgr.logLocalEntry(
                    auth.getOfficerName(), auth.getOfficerId(), auth.getOfficerRole(), title, text
            );

            // 2. Broadcast Online to Phone 2, Phone 3...
            if (syncMgr != null) {
                syncMgr.broadcastAudit(entry);
            }

            // 3. Broadcast Offline BLE Beacon
            if (meshMgr != null) {
                meshMgr.startOfflineMesh();
            }

            Toast.makeText(context, "✅ रिपोर्ट दर्ज! सभी फ़ोनों में प्रसारित की गई।", Toast.LENGTH_LONG).show();
        });

        builder.setNegativeButton("रद्द करें", (dialog, which) -> dialog.dismiss());
        builder.show();
    }
}
