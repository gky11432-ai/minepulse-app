package com.mineguard.dgms;

/**
 * Real IoT Telemetry Bridge
 * Future-Proof Architecture: Connect actual BLE/MQTT sensors to this class
 * by calling injectIotData(...) when a hardware packet arrives.
 */
public class TelemetryEngine {
    private double lastCh4 = 0.0;
    private int lastCo = 0;
    private double lastO2 = 20.9;
    private int lastAirflow = 1250;
    
    private TelemetryListener listener;

    public interface TelemetryListener {
        void onSensorUpdate(double ch4, int co, double o2, int airflow, boolean isDanger);
    }

    public void setListener(TelemetryListener listener) {
        this.listener = listener;
        // Send immediate state upon binding
        if (listener != null) {
            listener.onSensorUpdate(lastCh4, lastCo, lastO2, lastAirflow, checkDanger(lastCh4, lastCo, lastO2));
        }
    }

    /**
     * @apiNote Future IoT Hardware (BLE GATT / MQTT Callback) will pass data here.
     * Currently being driven by manual Statutory Form inputs as the primary data source.
     */
    public void injectIotData(double ch4, int co, double o2, int airflow) {
        this.lastCh4 = ch4;
        this.lastCo = co;
        this.lastO2 = o2;
        this.lastAirflow = airflow;

        boolean isDanger = checkDanger(ch4, co, o2);

        if (listener != null) {
            listener.onSensorUpdate(ch4, co, o2, airflow, isDanger);
        }
    }

    private boolean checkDanger(double ch4, int co, double o2) {
        return (ch4 >= 0.75 || co >= 50 || o2 < 19.0);
    }

    // Getters for on-demand fetch
    public double getCh4() { return lastCh4; }
    public int getCo() { return lastCo; }
}
