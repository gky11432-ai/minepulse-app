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
        List<AlarmLogManager.AuditEntry> allEntries = logMgr.getAllEntries();

        PdfDocument doc = new PdfDocument();
        PdfDocument.PageInfo pageInfo = new PdfDocument.PageInfo.Builder(595, 842, 1).create();
        PdfDocument.Page page = doc.startPage(pageInfo);
        Canvas canvas = page.getCanvas();
        Paint paint = new Paint();

        paint.setStyle(Paint.Style.STROKE);
        paint.setStrokeWidth(2);
        paint.setColor(Color.BLACK);
        canvas.drawRect(20, 20, 575, 822, paint);

        paint.setStyle(Paint.Style.FILL);
        paint.setTextAlign(Paint.Align.CENTER);
        paint.setTextSize(13);
        paint.setFakeBoldText(true);
        canvas.drawText("DIRECTORATE GENERAL OF MINES SAFETY (DGMS)", 297, 50, paint);
        paint.setTextSize(11);
        canvas.drawText(reportTitle.toUpperCase(), 297, 68, paint);
        paint.setTextSize(8.5f);
        paint.setFakeBoldText(false);
        canvas.drawText("CENTRAL MULTI-OFFICER SHARED COLLIERY LEDGER", 297, 82, paint);
        canvas.drawLine(30, 90, 565, 90, paint);

        paint.setTextAlign(Paint.Align.LEFT);
        paint.setTextSize(9f);
        String dateStr = new SimpleDateFormat("dd/MM/yyyy HH:mm", Locale.getDefault()).format(new Date());
        canvas.drawText("Viewing Official: " + auth.getOfficerName() + " (" + auth.getOfficerRole() + ")", 35, 108, paint);
        canvas.drawText("Colliery: Central Underground Colliery", 35, 122, paint);
        canvas.drawText("Generated: " + dateStr, 380, 108, paint);
        canvas.drawText("Total Synced Logs: " + allEntries.size(), 380, 122, paint);

        paint.setStyle(Paint.Style.STROKE);
        canvas.drawRect(35, 138, 560, 160, paint);
        paint.setStyle(Paint.Style.FILL);
        paint.setFakeBoldText(true);
        canvas.drawText("Time", 40, 153, paint);
        canvas.drawText("Officer & Designation", 125, 153, paint);
        canvas.drawText("Category / Register", 275, 153, paint);
        canvas.drawText("Inspection Findings / Status", 410, 153, paint);

        paint.setFakeBoldText(false);
        int y = 178;
        if (allEntries.isEmpty()) {
            canvas.drawText("No inspection records logged in this shift ledger.", 40, y, paint);
        } else {
            for (int i = 0; i < Math.min(allEntries.size(), 24); i++) {
                AlarmLogManager.AuditEntry e = allEntries.get(i);
                canvas.drawText(e.timestamp, 40, y, paint);
                String officerTag = e.officerName + " (" + (e.role.length() > 8 ? e.role.substring(0, 8) : e.role) + ")";
                canvas.drawText(officerTag, 125, y, paint);
                String cat = e.category.length() > 18 ? e.category.substring(0, 18) : e.category;
                canvas.drawText(cat, 275, y, paint);
                String rem = e.remarks.length() > 24 ? e.remarks.substring(0, 24) + ".." : e.remarks;
                canvas.drawText(rem, 410, y, paint);
                canvas.drawLine(35, y + 4, 560, y + 4, paint);
                y += 18;
            }
        }

        paint.setTextSize(9);
        canvas.drawLine(60, 760, 220, 760, paint);
        canvas.drawText("Shift Sirdar / Overman", 75, 775, paint);
        canvas.drawLine(370, 760, 530, 760, paint);
        canvas.drawText("Colliery Manager Signature", 390, 775, paint);

        doc.finishPage(page);

        try {
            File file = new File(context.getExternalFilesDir(null), "DGMS_Shared_Ledger.pdf");
            doc.writeTo(new FileOutputStream(file));
            doc.close();
            return file;
        } catch (Exception e) {
            doc.close();
            return null;
        }
    }

    public static void printOrDownload(Context context) {
        printOrDownload(context, "ALL", "DGMS_Master_Shift_Dossier");
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
