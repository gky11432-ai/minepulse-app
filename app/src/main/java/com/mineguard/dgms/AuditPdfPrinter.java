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

        List<AlarmLogManager.AuditEntry> records = reportType.equals("ALL") 
                ? logMgr.getAllEntries() 
                : logMgr.getEntriesByCategory(reportType);

        PdfDocument doc = new PdfDocument();
        PdfDocument.PageInfo pageInfo = new PdfDocument.PageInfo.Builder(595, 842, 1).create();
        PdfDocument.Page page = doc.startPage(pageInfo);
        Canvas canvas = page.getCanvas();
        Paint paint = new Paint();

        // Border
        paint.setStyle(Paint.Style.STROKE);
        paint.setStrokeWidth(2);
        paint.setColor(Color.BLACK);
        canvas.drawRect(20, 20, 575, 822, paint);

        // Header
        paint.setStyle(Paint.Style.FILL);
        paint.setTextAlign(Paint.Align.CENTER);
        paint.setTextSize(13);
        paint.setFakeBoldText(true);
        canvas.drawText("DIRECTORATE GENERAL OF MINES SAFETY", 297, 48, paint);
        paint.setTextSize(11);
        canvas.drawText(reportTitle.toUpperCase(), 297, 66, paint);
        paint.setTextSize(8.5f);
        paint.setFakeBoldText(false);
        String sub = reportType.equals("ALL") ? "CONSOLIDATED MULTI-REGISTER SHIFT DOSSIER" : "STATUTORY INDIVIDUAL REGISTER RECORD";
        canvas.drawText(sub, 297, 80, paint);
        canvas.drawLine(30, 88, 565, 88, paint);

        // Meta Info
        paint.setTextAlign(Paint.Align.LEFT);
        paint.setTextSize(9f);
        String dateStr = new SimpleDateFormat("dd/MM/yyyy HH:mm", Locale.getDefault()).format(new Date());
        canvas.drawText("Auditing Official: " + auth.getOfficerName() + " (" + auth.getOfficerRole() + ")", 35, 106, paint);
        canvas.drawText("Colliery: Central Underground Colliery", 35, 120, paint);
        canvas.drawText("Audit Generated: " + dateStr, 380, 106, paint);
        canvas.drawText("Total Shift Records: " + records.size(), 380, 120, paint);

        // Table Header
        paint.setStyle(Paint.Style.STROKE);
        canvas.drawRect(35, 136, 560, 158, paint);
        paint.setStyle(Paint.Style.FILL);
        paint.setFakeBoldText(true);
        canvas.drawText("Time", 40, 151, paint);
        canvas.drawText("Officer & Designation", 125, 151, paint);
        canvas.drawText("Section / Type", 280, 151, paint);
        canvas.drawText("Inspection Findings / Hazard State", 390, 151, paint);

        // Content
        paint.setFakeBoldText(false);
        int y = 175;
        if (records.isEmpty()) {
            canvas.drawText("No entries recorded for this specific category in current shift.", 40, y, paint);
        } else {
            for (int i = 0; i < Math.min(records.size(), 25); i++) {
                AlarmLogManager.AuditEntry e = records.get(i);
                canvas.drawText(e.timestamp, 40, y, paint);

                String officerTag = e.officerName + " (" + (e.role.length() > 8 ? e.role.substring(0, 8) : e.role) + ")";
                canvas.drawText(officerTag, 125, y, paint);
                canvas.drawText(e.category, 280, y, paint);

                String rem = e.remarks.length() > 28 ? e.remarks.substring(0, 28) + ".." : e.remarks;
                if (e.isDanger) paint.setColor(Color.RED);
                canvas.drawText(rem, 390, y, paint);
                paint.setColor(Color.BLACK);

                canvas.drawLine(35, y + 4, 560, y + 4, paint);
                y += 18;
            }
        }

        // Bottom Signatures
        paint.setTextSize(9);
        canvas.drawLine(60, 760, 220, 760, paint);
        canvas.drawText("Shift Sirdar / Overman", 75, 775, paint);
        canvas.drawLine(370, 760, 530, 760, paint);
        canvas.drawText("Colliery Manager Signature", 390, 775, paint);

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
