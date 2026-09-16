package com.mineguard.dgms;

import android.Manifest;
import android.content.ComponentName;
import android.content.Context;
import android.content.Intent;
import android.content.ServiceConnection;
import android.content.pm.PackageManager;
import android.graphics.Color;
import android.os.Build;
import android.os.Bundle;
import android.os.IBinder;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.SeekBar;
import android.widget.TextView;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;
import com.mineguard.dgms.ui.NeonGaugeView;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.ConcurrentHashMap;

public class MainActivity extends AppCompatActivity {
    private MineSafetyService safetyService;
    private AuthManager authManager;
    private AlarmLogManager alarmLogManager;
    private AuditSyncManager auditSyncManager;
    private boolean isBound = false;

    private NeonGaugeView gaugeCh4;
    private TextView tvSensorCh4, tvSensorCo, tvSensorO2;
    private TextView tvPeerCount, tvSonarNodes, tvNearestMiner, tvNearestDist;
    private TextView tvManpowerCount, tvStrataLoad, tvOfficerName;
    private SeekBar seekSos;

    private final ServiceConnection serviceConn = new ServiceConnection() {
        @Override
        public void onServiceConnected(ComponentName name, IBinder service) {
            MineSafetyService.LocalBinder binder = (MineSafetyService.LocalBinder) service;
            safetyService = binder.getService();
            isBound = true;
            RadarActivity.setMeshManager(safetyService.getBleMeshManager());
            
            setupIoTTelemetryBinding();
            setupLiveMeshListeners();
            refreshStaticLedgerData(); 
        }
        @Override
        public void onServiceDisconnected(ComponentName name) { isBound = false; }
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        authManager = new AuthManager(this);
        alarmLogManager = new AlarmLogManager(this);
        auditSyncManager = new AuditSyncManager(this, alarmLogManager);

        if (!authManager.isLoggedIn()) {
            startActivity(new Intent(this, LoginActivity.class));
            finish();
            return;
        }

        setContentView(R.layout.activity_main);
        
        gaugeCh4 = findViewById(R.id.gauge_ch4);
        tvSensorCh4 = findViewById(R.id.tv_sensor_ch4);
        tvSensorCo = findViewById(R.id.tv_sensor_co);
        tvSensorO2 = findViewById(R.id.tv_sensor_o2);
        tvPeerCount = findViewById(R.id.tv_peer_count);
        tvSonarNodes = findViewById(R.id.tv_sonar_nodes);
        tvNearestMiner = findViewById(R.id.tv_nearest_miner);
        tvNearestDist = findViewById(R.id.tv_nearest_dist);
        tvManpowerCount = findViewById(R.id.tv_manpower_count);
        tvStrataLoad = findViewById(R.id.tv_strata_load);
        seekSos = findViewById(R.id.seek_sos_slider);
        tvOfficerName = findViewById(R.id.tv_officer_name);

        if (tvOfficerName != null) {
            tvOfficerName.setText(authManager.getOfficerName() + "\n" + authManager.getOfficerRole());
        }

        // Action Cards
        if (findViewById(R.id.card_telemetry) != null) 
            findViewById(R.id.card_telemetry).setOnClickListener(v -> RegisterDialogHelper.showDedicatedDialog(this, "CMR 153 Ventilation Gas", alarmLogManager, auditSyncManager, safetyService));
        if (findViewById(R.id.card_attendance) != null) 
            findViewById(R.id.card_attendance).setOnClickListener(v -> RegisterDialogHelper.showDedicatedDialog(this, "Form B Attendance", alarmLogManager, auditSyncManager, safetyService));
        if (findViewById(R.id.card_strata) != null) 
            findViewById(R.id.card_strata).setOnClickListener(v -> RegisterDialogHelper.showDedicatedDialog(this, "CMR 123 Strata", alarmLogManager, auditSyncManager, safetyService));
        
        setupSlideToSos();
        setupBottomNav();
        checkPermissions();

        startService(new Intent(this, MineSafetyService.class));
        bindService(new Intent(this, MineSafetyService.class), serviceConn, Context.BIND_AUTO_CREATE);
    }

    private void setupBottomNav() {
        View navHome = findViewById(R.id.nav_home);
        View navMap = findViewById(R.id.nav_map);
        View navReports = findViewById(R.id.nav_reports);
        View dockPdf = findViewById(R.id.dock_btn_pdf);

        if (navHome != null) {
            highlightTab(navHome, true); // Active
            highlightTab(navMap, false);
            highlightTab(navReports, false);

            navMap.setOnClickListener(v -> startActivity(new Intent(this, RadarActivity.class)));
            navReports.setOnClickListener(v -> startActivity(new Intent(this, ReportsActivity.class)));
        }
        if (dockPdf != null) dockPdf.setOnClickListener(v -> AuditPdfPrinter.printOrDownload(this, "ALL", "DGMS_Master_Shift_Dossier"));
    }

    private void highlightTab(View tab, boolean isActive) {
        if (tab instanceof ViewGroup) {
            ViewGroup group = (ViewGroup) tab;
            ImageView icon = (ImageView) group.getChildAt(0);
            TextView text = (TextView) group.getChildAt(1);
            int color = isActive ? Color.parseColor("#0EA5E9") : Color.parseColor("#64748B");
            icon.setColorFilter(color);
            text.setTextColor(color);
        }
    }

    private void setupSlideToSos() {
        if (seekSos == null) return;
        seekSos.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar s, int progress, boolean fromUser) {}
            @Override
            public void onStartTrackingTouch(SeekBar s) {}
            @Override
            public void onStopTrackingTouch(SeekBar s) {
                if (s.getProgress() > 90) {
                    if (safetyService != null) {
                        if (safetyService.getHardwareController().isSirenActive()) {
                            safetyService.cancelDualSos();
                            Toast.makeText(MainActivity.this, "🛑 SIREN STOPPED", Toast.LENGTH_SHORT).show();
                        } else {
                            safetyService.triggerDualSos();
                            alarmLogManager.logAlarmEvent(authManager.getOfficerName(), authManager.getOfficerId(), authManager.getOfficerRole(), "SOS_EVACUATION");
                            Toast.makeText(MainActivity.this, "🚨 EMERGENCY SOS BROADCASTED!", Toast.LENGTH_LONG).show();
                        }
                    }
                }
                s.setProgress(0);
            }
        });
    }

    private void setupIoTTelemetryBinding() {
        if (safetyService == null || safetyService.getTelemetryEngine() == null || gaugeCh4 == null) return;
        safetyService.getTelemetryEngine().setListener((ch4, co, o2, airflow, isDanger) -> {
            runOnUiThread(() -> {
                gaugeCh4.updateData((float) ch4, isDanger); 
                if (tvSensorCh4 != null) tvSensorCh4.setText(String.format("[ CH4 ] Methane\n%.2f%% (%s)", ch4, isDanger ? "DANGER" : "Safe"));
                if (tvSensorCo != null) tvSensorCo.setText(String.format("[ CO ] Carbon Monoxide\n%d PPM", co));
                if (tvSensorO2 != null) tvSensorO2.setText(String.format("[ O2 ] Oxygen\n%.1f%%", o2));
                int color = isDanger ? Color.parseColor("#EF4444") : Color.parseColor("#0EA5E9");
                if (tvSensorCh4 != null) tvSensorCh4.setTextColor(color);
            });
        });
    }

    private void setupLiveMeshListeners() {
        if (safetyService == null || safetyService.getBleMeshManager() == null) return;
        safetyService.getBleMeshManager().setListener(new BleMeshManager.MeshListener() {
            @Override
            public void onMinerUpdated(ConcurrentHashMap<String, BleMeshManager.PeerMiner> miners) {
                runOnUiThread(() -> {
                    if (tvPeerCount != null) tvPeerCount.setText(miners.size() + " Peers Linked | BLE");
                    if (miners.isEmpty()) {
                        if (tvSonarNodes != null) tvSonarNodes.setText("O YOU --- SCANNING...");
                        if (tvNearestMiner != null) tvNearestMiner.setText("Searching");
                        if (tvNearestDist != null) tvNearestDist.setText("");
                    } else {
                        StringBuilder nodes = new StringBuilder("O YOU ");
                        BleMeshManager.PeerMiner nearest = null;
                        for (BleMeshManager.PeerMiner p : miners.values()) {
                            nodes.append(" --- O ").append(p.officerName.toUpperCase());
                            if (nearest == null || p.distanceMeters < nearest.distanceMeters) nearest = p;
                        }
                        if (tvSonarNodes != null) tvSonarNodes.setText(nodes.toString());
                        if (nearest != null) {
                            if (tvNearestMiner != null) tvNearestMiner.setText(nearest.officerName + "\n" + nearest.officerRole);
                            if (tvNearestDist != null) tvNearestDist.setText("» " + nearest.distanceMeters + "m away");
                        }
                    }
                });
            }
            @Override
            public void onEmergencyReceived(String minerId, double distance) {}
        });
    }

    private void refreshStaticLedgerData() {
        List<AlarmLogManager.AuditEntry> logs = alarmLogManager.getAllEntries();
        for (AlarmLogManager.AuditEntry e : logs) {
            if ("ATTENDANCE".equals(e.category) && e.remarks.contains("Present Miners:")) {
                try {
                    String count = e.remarks.split("Present Miners:")[1].split("\\|")[0].trim();
                    if (tvManpowerCount != null) tvManpowerCount.setText(count + " / 45 Active");
                } catch (Exception ignored) {}
            } else if ("GAS".equals(e.category)) {
                try {
                    double parsedCh4 = Double.parseDouble(e.remarks.split("CH4: ")[1].split("%")[0]);
                    int parsedCo = Integer.parseInt(e.remarks.split("CO: ")[1].split(" PPM")[0]);
                    if (safetyService != null && safetyService.getTelemetryEngine() != null) {
                        safetyService.getTelemetryEngine().injectIotData(parsedCh4, parsedCo, 20.9, 1280);
                    }
                } catch (Exception ignored) {}
            } else if ("STRATA".equals(e.category)) {
                if (tvStrataLoad != null) {
                    tvStrataLoad.setText(e.isDanger ? "4.2T  UNSTABLE" : "8.6T  SECURE");
                    tvStrataLoad.setTextColor(e.isDanger ? Color.RED : Color.parseColor("#0EA5E9"));
                }
            }
        }
    }

    private void checkPermissions() {
        List<String> perms = new ArrayList<>();
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
            perms.add(Manifest.permission.BLUETOOTH_SCAN);
            perms.add(Manifest.permission.BLUETOOTH_ADVERTISE);
            perms.add(Manifest.permission.BLUETOOTH_CONNECT);
        }
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) perms.add(Manifest.permission.POST_NOTIFICATIONS);
        perms.add(Manifest.permission.ACCESS_FINE_LOCATION);
        perms.add(Manifest.permission.CAMERA);

        List<String> needed = new ArrayList<>();
        for (String p : perms) if (ContextCompat.checkSelfPermission(this, p) != PackageManager.PERMISSION_GRANTED) needed.add(p);
        if (!needed.isEmpty()) ActivityCompat.requestPermissions(this, needed.toArray(new String[0]), 102);
    }

    @Override
    protected void onResume() { super.onResume(); refreshStaticLedgerData(); }
    @Override
    protected void onDestroy() {
        super.onDestroy();
        if (isBound) {
            try { unbindService(serviceConn); } catch (Throwable ignored) {}
            isBound = false;
        }
    }
                  }
