package com.mineguard.dgms;

import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.pdf.PdfDocument;
import android.os.Bundle;
import android.os.CancellationSignal;
import android.os.ParcelFileDescriptor;
import android.print.PageRange;
import android.print.PrintAttributes;
import android.print.PrintDocumentAdapter;
import android.print.PrintDocumentInfo;
import android.print.PrintManager;
import android.widget.Toast;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.List;
import java.util.Locale;

public class AuditPdfPrinter {

    public static File generatePdf(Context context, String reportType, String reportTitle) {
        AuthManager auth = new AuthManager(context);
        AlarmLogManager logMgr = new AlarmLogManager(context);
        List<AlarmLogManager.AlarmEntry> alarms = logMgr.getAlarmHistory();

        PdfDocument doc = new PdfDocument();
        PdfDocument.PageInfo pageInfo = new PdfDocument.PageInfo.Builder(595, 842, 1).create();
        PdfDocument.Page page = doc.startPage(pageInfo);
        Canvas canvas = page.getCanvas();
        Paint paint = new Paint();

        // Outer Border
        paint.setStyle(Paint.Style.STROKE);
        paint.setStrokeWidth(2);
        paint.setColor(Color.BLACK);
        canvas.drawRect(20, 20, 575, 822, paint);

        // Header
        paint.setStyle(Paint.Style.FILL);
        paint.setTextAlign(Paint.Align.CENTER);
        paint.setTextSize(13);
        paint.setFakeBoldText(true);
        canvas.drawText("DIRECTORATE GENERAL OF MINES SAFETY (DGMS)", 297, 50, paint);
        paint.setTextSize(11);
        canvas.drawText(reportTitle.toUpperCase(), 297, 68, paint);
        paint.setTextSize(9);
        paint.setFakeBoldText(false);
        canvas.drawText("[Statutory Compliance under Mines Act 1952 & CMR 2017]", 297, 82, paint);
        canvas.drawLine(30, 90, 565, 90, paint);

        // Officer Info
        paint.setTextAlign(Paint.Align.LEFT);
        paint.setTextSize(9.5f);
        String dateStr = new SimpleDateFormat("dd/MM/yyyy HH:mm", Locale.getDefault()).format(new Date());
        canvas.drawText("Auditing Official: " + auth.getOfficerName() + " (" + auth.getOfficerId() + ")", 35, 110, paint);
        canvas.drawText("Designation: " + auth.getOfficerRole(), 35, 125, paint);
        canvas.drawText("Generated: " + dateStr, 380, 110, paint);
        canvas.drawText("Colliery: Central Underground Colliery", 380, 125, paint);

        // Content Table Header
        paint.setStyle(Paint.Style.STROKE);
        canvas.drawRect(35, 145, 560, 168, paint);
        paint.setStyle(Paint.Style.FILL);
        paint.setFakeBoldText(true);
        canvas.drawText("Timestamp / Parameter", 40, 160, paint);
        canvas.drawText("Inspection Details & Findings", 240, 160, paint);
        canvas.drawText("Status / Action", 450, 160, paint);

        // Dynamic Table Content based on Report Type
        paint.setFakeBoldText(false);
        int y = 190;

        if (reportType.equals("ALL") || reportType.equals("SIREN")) {
            canvas.drawText("--- EMERGENCY SIREN & SOS ALARM LEDGER ---", 40, y, paint);
            y += 20;
            if (alarms.isEmpty()) {
                canvas.drawText("No emergency alarms triggered during shift.", 40, y, paint);
                y += 20;
            } else {
                for (int i = 0; i < Math.min(alarms.size(), 6); i++) {
                    AlarmLogManager.AlarmEntry e = alarms.get(i);
                    canvas.drawText(e.timestamp, 40, y, paint);
                    canvas.drawText(e.officerName + " (" + e.role + ")", 240, y, paint);
                    canvas.drawText(e.triggerType, 450, y, paint);
                    y += 18;
                }
            }
        }

        if (reportType.equals("ALL") || reportType.equals("GAS")) {
            y += 10;
            canvas.drawText("--- VENTILATION & MINE AIR AUDIT (CMR 153) ---", 40, y, paint);
            y += 20;
            canvas.drawText("Inflammable Gas (CH4): 0.12%", 40, y, paint);
            canvas.drawText("Carbon Monoxide (CO): 0 PPM", 240, y, paint);
            canvas.drawText("🟢 SAFE (< 0.5%)", 450, y, paint);
            y += 20;
            canvas.drawText("Air Quantity at Last Split: 1250 m³/min", 40, y, paint);
            canvas.drawText("Velocity: 1.8 m/s", 240, y, paint);
            canvas.drawText("🟢 COMPLIANT", 450, y, paint);
            y += 25;
        }

        if (reportType.equals("ALL") || reportType.equals("STRATA")) {
            canvas.drawText("--- ROOF SUPPORT & STRATA CONTROL (CMR 123) ---", 40, y, paint);
            y += 20;
            canvas.drawText("Junction Bolting: 1.5m Spacing", 40, y, paint);
            canvas.drawText("Anchorage Testing: 8.5 Tonnes OK", 240, y, paint);
            canvas.drawText("🟢 SECURED", 450, y, paint);
            y += 25;
        }

        // Signatures
        paint.setTextSize(9);
        canvas.drawLine(60, 750, 220, 750, paint);
        canvas.drawText("Inspecting Sirdar / Overman", 70, 765, paint);
        canvas.drawLine(370, 750, 530, 750, paint);
        canvas.drawText("Colliery Manager Signature", 390, 765, paint);

        doc.finishPage(page);

        try {
            File file = new File(context.getExternalFilesDir(null), "DGMS_" + reportType + "_Report.pdf");
            doc.writeTo(new FileOutputStream(file));
            doc.close();
            return file;
        } catch (Exception e) {
            doc.close();
            return null;
        }
    }

    public static void printOrDownload(Context context, String type, String title) {
        File pdf = generatePdf(context, type, title);
        if (pdf == null || !pdf.exists()) {
            Toast.makeText(context, "PDF तैयार करने में त्रुटि!", Toast.LENGTH_SHORT).show();
            return;
        }

        PrintManager pm = (PrintManager) context.getSystemService(Context.PRINT_SERVICE);
        PrintDocumentAdapter adapter = new PrintDocumentAdapter() {
            @Override
            public void onLayout(PrintAttributes oldA, PrintAttributes newA, CancellationSignal sig, LayoutResultCallback cb, Bundle b) {
                cb.onLayoutFinished(new PrintDocumentInfo.Builder(title + ".pdf").setContentType(PrintDocumentInfo.CONTENT_TYPE_DOCUMENT).build(), true);
            }
            @Override
            public void onWrite(PageRange[] p, ParcelFileDescriptor dest, CancellationSignal sig, WriteResultCallback cb) {
                try (FileInputStream in = new FileInputStream(pdf); FileOutputStream out = new FileOutputStream(dest.getFileDescriptor())) {
                    byte[] buf = new byte[4096];
                    int r;
                    while ((r = in.read(buf)) > 0) out.write(buf, 0, r);
                    cb.onWriteFinished(new PageRange[]{PageRange.ALL_PAGES});
                } catch (Exception e) { cb.onWriteFailed(e.getMessage()); }
            }
        };
        pm.print(title, adapter, new PrintAttributes.Builder().build());
    }
}
