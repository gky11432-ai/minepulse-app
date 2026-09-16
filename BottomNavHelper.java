package com.mineguard.dgms;

import android.app.Activity;
import android.content.Intent;
import android.graphics.Color;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.TextView;

public class BottomNavHelper {
    
    public static void setupNav(Activity activity, String currentScreen) {
        View navHome = activity.findViewById(R.id.nav_home);
        View navMap = activity.findViewById(R.id.nav_map);
        View navReports = activity.findViewById(R.id.nav_reports);
        View dockPdf = activity.findViewById(R.id.dock_btn_pdf);

        if (navHome == null) return;

        // जो स्क्रीन खुली है उसे Blue (हाईलाइट) करें, बाकी को Grey रखें
        highlightTab(navHome, currentScreen.equals("HUD"));
        highlightTab(navMap, currentScreen.equals("RADAR"));
        highlightTab(navReports, currentScreen.equals("LOGS"));

        // HUD बटन क्लिक - वापस मेन स्क्रीन पर जाने के लिए
        navHome.setOnClickListener(v -> {
            if (!currentScreen.equals("HUD")) {
                Intent intent = new Intent(activity, MainActivity.class);
                intent.setFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP | Intent.FLAG_ACTIVITY_SINGLE_TOP);
                activity.startActivity(intent);
            }
        });

        // RADAR बटन क्लिक
        navMap.setOnClickListener(v -> {
            if (!currentScreen.equals("RADAR")) {
                activity.startActivity(new Intent(activity, RadarActivity.class));
            }
        });

        // LOGS बटन क्लिक
        navReports.setOnClickListener(v -> {
            if (!currentScreen.equals("LOGS")) {
                activity.startActivity(new Intent(activity, ReportsActivity.class));
            }
        });

        // PDF बटन क्लिक
        dockPdf.setOnClickListener(v -> AuditPdfPrinter.printOrDownload(activity, "ALL", "DGMS_Master_Shift_Dossier"));
    }

    private static void highlightTab(View tab, boolean isActive) {
        ImageView icon = (ImageView) ((ViewGroup) tab).getChildAt(0);
        TextView text = (TextView) ((ViewGroup) tab).getChildAt(1);
        
        int color = isActive ? Color.parseColor("#0EA5E9") : Color.parseColor("#64748B");
        icon.setColorFilter(color);
        text.setTextColor(color);
    }
}
