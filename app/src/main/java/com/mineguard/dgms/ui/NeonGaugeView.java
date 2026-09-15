package com.mineguard.dgms.ui;

import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.RectF;
import android.util.AttributeSet;
import android.view.View;

public class NeonGaugeView extends View {
    private Paint bgArcPaint, fgArcPaint, textPaint, labelPaint;
    private RectF rectF;
    private float progress = 0.12f; // Actual CH4
    private boolean isDanger = false;

    public NeonGaugeView(Context context, AttributeSet attrs) {
        super(context, attrs);
        init();
    }

    private void init() {
        bgArcPaint = new Paint(Paint.ANTI_ALIAS_FLAG);
        bgArcPaint.setStyle(Paint.Style.STROKE);
        bgArcPaint.setStrokeWidth(12f);
        bgArcPaint.setColor(Color.parseColor("#163859")); // Dark border

        fgArcPaint = new Paint(Paint.ANTI_ALIAS_FLAG);
        fgArcPaint.setStyle(Paint.Style.STROKE);
        fgArcPaint.setStrokeWidth(18f);
        fgArcPaint.setStrokeCap(Paint.Cap.ROUND);
        fgArcPaint.setShadowLayer(15, 0, 0, Color.parseColor("#22C55E")); // Neon Glow

        textPaint = new Paint(Paint.ANTI_ALIAS_FLAG);
        textPaint.setTextAlign(Paint.Align.CENTER);
        textPaint.setColor(Color.WHITE);
        textPaint.setTextSize(55f);
        textPaint.setFakeBoldText(true);

        labelPaint = new Paint(Paint.ANTI_ALIAS_FLAG);
        labelPaint.setTextAlign(Paint.Align.CENTER);
        labelPaint.setColor(Color.parseColor("#22C55E"));
        labelPaint.setTextSize(26f);
        labelPaint.setFakeBoldText(true);

        rectF = new RectF();
    }

    @Override
    protected void onSizeChanged(int w, int h, int oldw, int oldh) {
        super.onSizeChanged(w, h, oldw, oldh);
        float pad = 30f;
        rectF.set(pad, pad, w - pad, h - pad);
    }

    @Override
    protected void onDraw(Canvas canvas) {
        super.onDraw(canvas);
        // Draw Background full circle
        canvas.drawArc(rectF, 135, 270, false, bgArcPaint);

        // Draw Progress arc
        fgArcPaint.setColor(isDanger ? Color.parseColor("#EF4444") : Color.parseColor("#22C55E"));
        fgArcPaint.setShadowLayer(15, 0, 0, fgArcPaint.getColor());
        labelPaint.setColor(fgArcPaint.getColor());
        
        float sweep = (progress / 1.0f) * 270f; 
        canvas.drawArc(rectF, 135, Math.min(sweep, 270), false, fgArcPaint);

        // Center Text
        float cx = getWidth() / 2f;
        float cy = getHeight() / 2f;
        canvas.drawText(String.format("%.2f%%", progress), cx, cy + 10, textPaint);
        canvas.drawText(isDanger ? "CRITICAL" : "NORMAL", cx, cy + 50, labelPaint);
        
        labelPaint.setColor(Color.parseColor("#94A3B8"));
        labelPaint.setTextSize(20f);
        canvas.drawText("CH4", cx, cy - 35, labelPaint);
    }

    public void updateData(float ch4, boolean danger) {
        this.progress = ch4;
        this.isDanger = danger;
        invalidate(); // Redraw LIVE
    }
}
