package com.mineguard.dgms.ui;

import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.DashPathEffect;
import android.graphics.Paint;
import android.graphics.RectF;
import android.util.AttributeSet;
import android.view.View;

public class NeonGaugeView extends View {
    private Paint bgArcPaint, fgArcPaint, textPaint, labelPaint;
    private RectF rectF;
    private float progress = 0.12f;
    private boolean isDanger = false;

    public NeonGaugeView(Context context, AttributeSet attrs) {
        super(context, attrs);
        init();
    }

    private void init() {
        bgArcPaint = new Paint(Paint.ANTI_ALIAS_FLAG);
        bgArcPaint.setStyle(Paint.Style.STROKE);
        bgArcPaint.setStrokeWidth(12f);
        bgArcPaint.setColor(Color.parseColor("#102A45"));
        // Creates the tactical dashed HUD look
        bgArcPaint.setPathEffect(new DashPathEffect(new float[]{15f, 10f}, 0)); 

        fgArcPaint = new Paint(Paint.ANTI_ALIAS_FLAG);
        fgArcPaint.setStyle(Paint.Style.STROKE);
        fgArcPaint.setStrokeWidth(16f);
        fgArcPaint.setStrokeCap(Paint.Cap.ROUND);

        textPaint = new Paint(Paint.ANTI_ALIAS_FLAG);
        textPaint.setTextAlign(Paint.Align.CENTER);
        textPaint.setColor(Color.WHITE);
        textPaint.setTextSize(65f);
        textPaint.setFakeBoldText(true);

        labelPaint = new Paint(Paint.ANTI_ALIAS_FLAG);
        labelPaint.setTextAlign(Paint.Align.CENTER);
        labelPaint.setTextSize(26f);
        labelPaint.setFakeBoldText(true);
        labelPaint.setLetterSpacing(0.05f);

        rectF = new RectF();
    }

    @Override
    protected void onSizeChanged(int w, int h, int oldw, int oldh) {
        super.onSizeChanged(w, h, oldw, oldh);
        float pad = 40f;
        rectF.set(pad, pad, w - pad, h - pad);
    }

    @Override
    protected void onDraw(Canvas canvas) {
        super.onDraw(canvas);
        canvas.drawArc(rectF, 135, 270, false, bgArcPaint);

        fgArcPaint.setColor(isDanger ? Color.parseColor("#EF4444") : Color.parseColor("#22C55E"));
        fgArcPaint.setShadowLayer(20, 0, 0, fgArcPaint.getColor());
        labelPaint.setColor(fgArcPaint.getColor());
        
        float sweep = (progress / 1.0f) * 270f; 
        canvas.drawArc(rectF, 135, Math.min(sweep, 270), false, fgArcPaint);

        float cx = getWidth() / 2f;
        float cy = getHeight() / 2f;
        canvas.drawText(String.format("%.2f%%", progress), cx, cy + 15, textPaint);
        canvas.drawText(isDanger ? "CRITICAL" : "NORMAL", cx, cy + 60, labelPaint);
        
        labelPaint.setColor(Color.parseColor("#94A3B8"));
        labelPaint.setTextSize(22f);
        canvas.drawText("CH4", cx, cy - 45, labelPaint);
    }

    public void updateData(float ch4, boolean danger) {
        this.progress = ch4;
        this.isDanger = danger;
        invalidate();
    }
}
