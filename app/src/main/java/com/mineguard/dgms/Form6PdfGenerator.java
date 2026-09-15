package com.mineguard.dgms;

import android.content.Context;
import android.content.Intent;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.pdf.PdfDocument;
import android.net.Uri;
import android.widget.Toast;
import androidx.core.content.FileProvider;
import java.io.File;
import java.io.FileOutputStream;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;

public class Form6PdfGenerator {

    public static void generateAndShareForm6(Context context) {
        PdfDocument document = new PdfDocument();
        PdfDocument.PageInfo pageInfo = new PdfDocument.PageInfo.Builder(595, 842, 1).create();
        PdfDocument.Page page = document.startPage(pageInfo);
        Canvas canvas = page.getCanvas();
        Paint paint = new Paint();

        // 1. Outer Border
        paint.setStyle(Paint.Style.STROKE);
        paint.setStrokeWidth(2);
        paint.setColor(Color.BLACK);
        canvas.drawRect(20, 20, 575, 822, paint);

        // 2. Header
        paint.setStyle(Paint.Style.FILL);
        paint.setTextAlign(Paint.Align.CENTER);
        paint.setTextSize(14);
        paint.setFakeBoldText(true);
        canvas.drawText("DIRECTORATE GENERAL OF MINES SAFETY", 297, 50, paint);

        paint.setTextSize(12);
        canvas.drawText("FIRST SCHEDULE - FORM VI (FORM 6)", 297, 68, paint);

        paint.setTextSize(9);
        paint.setFakeBoldText(false);
        canvas.drawText("[See Regulations 47, 48 & 242 of Coal Mines Regulations, 2017]", 297, 82, paint);
        canvas.drawLine(30, 92, 565, 92, paint);

        // 3. Meta Data
        paint.setTextAlign(Paint.Align.LEFT);
        paint.setTextSize(10);
        String dateStr = new SimpleDateFormat("dd/MM/yyyy", Locale.getDefault()).format(new Date());
        String timeStr = new SimpleDateFormat("HH:mm", Locale.getDefault()).format(new Date());

        canvas.drawText("Mine: Central Underground Colliery", 35, 115, paint);
        canvas.drawText("Date: " + dateStr, 380, 115, paint);
        canvas.drawText("District: 2nd Dip Horizon (Seam III)", 35, 135, paint);
        canvas.drawText("Shift: Shift 1 (" + timeStr + ")", 380, 135, paint);
        canvas.drawText("Inspecting Official: Mining Sirdar (CMR 48)", 35, 155, paint);
        canvas.drawText("Status: SATISFACTORY / COMPLIANT", 380, 155, paint);

        // 4. Observations Table
        paint.setStyle(Paint.Style.STROKE);
        canvas.drawRect(35, 175, 560, 290, paint);
        canvas.drawLine(35, 200, 560, 200, paint);
        canvas.drawLine(250, 175, 250, 290, paint);
        canvas.drawLine(440, 175, 440, 290, paint);

        paint.setStyle(Paint.Style.FILL);
        paint.setFakeBoldText(true);
        canvas.drawText("Statutory Regulation", 40, 192, paint);
        canvas.drawText("Condition Observed", 255, 192, paint);
        canvas.drawText("Compliance", 450, 192, paint);

        paint.setFakeBoldText(false);
        canvas.drawText("Strata & Roof Support (Reg 48)", 40, 220, paint);
        canvas.drawText("Systematic support intact & safe", 255, 220, paint);
        canvas.drawText("SECURE", 450, 220, paint);

        canvas.drawText("Ventilation & Gas (Reg 153)", 40, 250, paint);
        canvas.drawText("CH4: 0.04% | Air Velocity: 1.2 m/s", 255, 250, paint);
        canvas.drawText("ADEQUATE", 450, 250, paint);

        canvas.drawText("Danger Place Barricading (Reg 48)", 40, 280, paint);
        canvas.drawText("Disused galleries fenced properly", 255, 280, paint);
        canvas.drawText("VERIFIED", 450, 280, paint);

        // 5. Certification & Signatures
        paint.setTextSize(9);
        canvas.drawText("I certify that I have personally inspected the district, examined the roof, sides, and ventilation,", 35, 330, paint);
        canvas.drawText("and found workings safe under the provisions of Coal Mines Regulations, 2017.", 35, 345, paint);

        canvas.drawLine(60, 430, 220, 430, paint);
        canvas.drawText("Mining Sirdar / Overman", 75, 445, paint);

        canvas.drawLine(370, 430, 530, 430, paint);
        canvas.drawText("Colliery Manager", 410, 445, paint);

        document.finishPage(page);

        // Save and share file
        try {
            File pdfDir = new File(context.getCacheDir(), "documents");
            if (!pdfDir.exists()) pdfDir.mkdirs();
            File file = new File(pdfDir, "DGMS_Form6_" + System.currentTimeMillis() + ".pdf");
            document.writeTo(new FileOutputStream(file));
            document.close();

            Uri uri = FileProvider.getUriForFile(context, context.getPackageName() + ".provider", file);
            Intent intent = new Intent(Intent.ACTION_SEND);
            intent.setType("application/pdf");
            intent.putExtra(Intent.EXTRA_STREAM, uri);
            intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);
            context.startActivity(Intent.createChooser(intent, "Share DGMS Form 6 PDF"));
        } catch (Exception e) {
            document.close();
            Toast.makeText(context, "PDF बनाने में त्रुटि: " + e.getMessage(), Toast.LENGTH_LONG).show();
        }
    }
}
