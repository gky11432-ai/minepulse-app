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

    public static File createAuditReportPdf(Context context) {
        AuthManager auth = new AuthManager(context);
        AlarmLogManager logMgr = new AlarmLogManager(context);
        List<AlarmLogManager.AlarmEntry> alarms = logMgr.getAlarmHistory();

        PdfDocument document = new PdfDocument();
        PdfDocument.PageInfo pageInfo = new PdfDocument.PageInfo.Builder(595, 842, 1).create();
        PdfDocument.Page page = document.startPage(pageInfo);
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
        canvas.drawText("DIRECTORATE GENERAL OF MINES SAFETY", 297, 50, paint);
        paint.setTextSize(11);
        canvas.drawText("STATUTORY SHIFT AUDIT & EMERGENCY SIREN LEDGER", 297, 68, paint);
        paint.setTextSize(9);
        paint.setFakeBoldText(false);
        canvas.drawText("[Under Coal Mines Regulations, 2017 & Mines Act, 1952]", 297, 82, paint);
        canvas.drawLine(30, 90, 565, 90, paint);

        paint.setTextAlign(Paint.Align.LEFT);
        paint.setTextSize(9.5f);
        String dateStr = new SimpleDateFormat("dd/MM/yyyy HH:mm", Locale.getDefault()).format(new Date());
        canvas.drawText("Certified Official: " + auth.getOfficerName() + " (" + auth.getOfficerId() + ")", 35, 110, paint);
        canvas.drawText("Designation: " + auth.getOfficerRole(), 35, 125, paint);
        canvas.drawText("Audit Generated: " + dateStr, 380, 110, paint);
        canvas.drawText("Colliery: Central Underground Colliery", 380, 125, paint);

        paint.setStyle(Paint.Style.STROKE);
        canvas.drawRect(35, 145, 560, 168, paint);
        paint.setStyle(Paint.Style.FILL);
        paint.setFakeBoldText(true);
        canvas.drawText("Time", 40, 160, paint);
        canvas.drawText("Triggered By", 160, 160, paint);
        canvas.drawText("Designation / ID", 310, 160, paint);
        canvas.drawText("Alarm Mode", 460, 160, paint);

        paint.setFakeBoldText(false);
        int y = 185;
        if (alarms.isEmpty()) {
            canvas.drawText("No emergency siren events recorded in this shift cycle.", 40, y, paint);
        } else {
            for (int i = 0; i < Math.min(alarms.size(), 12); i++) {
                AlarmLogManager.AlarmEntry e = alarms.get(i);
                canvas.drawText(e.timestamp, 40, y, paint);
                canvas.drawText(e.officerName, 160, y, paint);
                canvas.drawText(e.role + " (" + e.officerId + ")", 310, y, paint);
                canvas.drawText(e.triggerType, 460, y, paint);
                canvas.drawLine(35, y + 5, 560, y + 5, paint);
                y += 20;
            }
        }

        paint.setTextSize(9);
        canvas.drawLine(60, 750, 220, 750, paint);
        canvas.drawText("Inspecting Sirdar / Overman", 70, 765, paint);
        canvas.drawLine(370, 750, 530, 750, paint);
        canvas.drawText("Colliery Manager Signature", 390, 765, paint);

        document.finishPage(page);

        try {
            File file = new File(context.getExternalFilesDir(null), "DGMS_Audit_Report.pdf");
            document.writeTo(new FileOutputStream(file));
            document.close();
            return file;
        } catch (Exception e) {
            document.close();
            return null;
        }
    }

    public static void printOrDownload(Context context) {
        File pdfFile = createAuditReportPdf(context);
        if (pdfFile == null || !pdfFile.exists()) {
            Toast.makeText(context, "PDF तैयार करने में त्रुटि!", Toast.LENGTH_SHORT).show();
            return;
        }

        try {
            PrintManager printManager = (PrintManager) context.getSystemService(Context.PRINT_SERVICE);
            PrintDocumentAdapter pda = new PrintDocumentAdapter() {
                @Override
                public void onLayout(PrintAttributes oldAttributes, PrintAttributes newAttributes, CancellationSignal cancellationSignal, LayoutResultCallback callback, Bundle extras) {
                    callback.onLayoutFinished(new PrintDocumentInfo.Builder("DGMS_Form6_Audit.pdf").setContentType(PrintDocumentInfo.CONTENT_TYPE_DOCUMENT).build(), true);
                }
                @Override
                public void onWrite(PageRange[] pages, ParcelFileDescriptor destination, CancellationSignal cancellationSignal, WriteResultCallback callback) {
                    try (FileInputStream in = new FileInputStream(pdfFile); FileOutputStream out = new FileOutputStream(destination.getFileDescriptor())) {
                        byte[] buf = new byte[4096];
                        int bytesRead;
                        while ((bytesRead = in.read(buf)) > 0) out.write(buf, 0, bytesRead);
                        callback.onWriteFinished(new PageRange[]{PageRange.ALL_PAGES});
                    } catch (Exception e) { callback.onWriteFailed(e.getMessage()); }
                }
            };
            printManager.print("DGMS_Audit_Report", pda, new PrintAttributes.Builder().build());
        } catch (Exception e) {
            Toast.makeText(context, "प्रिंटर डायलॉग खोलने में असमर्थ", Toast.LENGTH_SHORT).show();
        }
    }
}
