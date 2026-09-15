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
import android.widget.TextView;
import android.widget.Toast;
import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;
import androidx.core.view.GravityCompat;
import androidx.drawerlayout.widget.DrawerLayout;
import com.google.android.material.appbar.MaterialToolbar;
import com.google.android.material.button.MaterialButton;
import com.google.android.material.card.MaterialCardView;
import com.google.android.material.navigation.NavigationView;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.List;
import java.util.concurrent.ConcurrentHashMap;

public class MainActivity extends AppCompatActivity implements NavigationView.OnNavigationItemSelectedListener {
    private DrawerLayout drawerLayout;
    private MineSafetyService safetyService;
    private AuthManager authManager;
    private AlarmLogManager alarmLogManager;
    private AuditSyncManager auditSyncManager;
    private boolean isBound = false;

    private TextView tvMeshStatus, tvShiftInfo, tvGasBadge, tvGasReadout;
    private TextView tvManpowerCount, tvStrataStatus, tvSonarDetail, tvSirenLabel;
    private MaterialButton btnTorchToggle;

    private final ServiceConnection serviceConn = new ServiceConnection() {
        @Override
        public void onServiceConnected(ComponentName name, IBinder service) {
            try {
                MineSafetyService.LocalBinder binder = (MineSafetyService.LocalBinder) service;
                safetyService = binder.getService();
                isBound = true;
                RadarActivity.setMeshManager(safetyService.getBleMeshManager());
                setupLiveMeshListeners();
            } catch (Throwable ignored) {}
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
        initViews();
        setupDynamicShift();
        refreshLiveLedgerData();

        auditSyncManager.setListener((officer, cat, isDanger) -> runOnUiThread(() -> {
            refreshLiveLedgerData();
            if (isDanger && safetyService != null) safetyService.triggerDualSos();
        }));

        startService(new Intent(this, MineSafetyService.class));
        bindService(new Intent(this, MineSafetyService.class), serviceConn, Context.BIND_AUTO_CREATE);
        checkPermissions();
    }

    private void initViews() {
        drawerLayout = findViewById(R.id.drawer_layout);
        MaterialToolbar toolbar = findViewById(R.id.top_toolbar);
        NavigationView navView = findViewById(R.id.nav_view);

        tvMeshStatus = findViewById(R.id.tv_mesh_status);
        tvShiftInfo = findViewById(R.id.tv_shift_info);
        tvGasBadge = findViewById(R.id.tv_gas_badge);
        tvGasReadout = findViewById(R.id.tv_gas_readout);
        tvManpowerCount = findViewById(R.id.tv_manpower_count);
        tvStrataStatus = findViewById(R.id.tv_strata_status);
        tvSonarDetail = findViewById(R.id.tv_sonar_detail);
        tvSirenLabel = findViewById(R.id.tv_siren_label);
        btnTorchToggle = findViewById(R.id.btn_torch_toggle);

        toolbar.setSubtitle(authManager.getOfficerName() + " (" + authManager.getOfficerRole() + ")");
        toolbar.setNavigationOnClickListener(v -> drawerLayout.openDrawer(GravityCompat.START));
        navView.setNavigationItemSelectedListener(this);

        btnTorchToggle.setOnClickListener(v -> {
            if (isBound && safetyService != null) {
                boolean state = safetyService.getHardwareController().toggleTorch();
                btnTorchToggle.setText(state ? "🔦 ON" : "🔦 Torch");
            }
        });

        findViewById(R.id.card_gas_audit).setOnClickListener(v ->
                RegisterDialogHelper.showDedicatedDialog(this, "CMR 153 Ventilation Gas", alarmLogManager, auditSyncManager, safetyService)
        );

        findViewById(R.id.card_attendance).setOnClickListener(v ->
                RegisterDialogHelper.showDedicatedDialog(this, "Form B Attendance", alarmLogManager, auditSyncManager, safetyService)
        );

        findViewById(R.id.card_strata).setOnClickListener(v ->
                RegisterDialogHelper.showDedicatedDialog(this, "CMR 123 Strata", alarmLogManager, auditSyncManager, safetyService)
        );

        findViewById(R.id.card_radar_open).setOnClickListener(v -> startActivity(new Intent(this, RadarActivity.class)));
        findViewById(R.id.btn_print_master).setOnClickListener(v -> AuditPdfPrinter.printOrDownload(this, "ALL", "DGMS_Master_Shift_Dossier"));

        findViewById(R.id.card_emergency_siren).setOnClickListener(v -> {
            if (!isBound || safetyService == null) return;
            if (safetyService.getHardwareController().isSirenActive()) {
                safetyService.cancelDualSos();
                tvSirenLabel.setText("🚨 TAP TO BROADCAST COLLIERY SIREN");
                Toast.makeText(this, "सायरन बंद किया गया", Toast.LENGTH_SHORT).show();
            } else {
                safetyService.triggerDualSos();
                alarmLogManager.logAlarmEvent(authManager.getOfficerName(), authManager.getOfficerId(), authManager.getOfficerRole(), "MANUAL_SOS");
                tvSirenLabel.setText("🛑 SIREN ACTIVE - TAP TO SILENCE");
                Toast.makeText(this, "🚨 सायरन बजाया गया!", Toast.LENGTH_LONG).show();
            }
        });
    }

    private void setupDynamicShift() {
        int h = Calendar.getInstance().get(Calendar.HOUR_OF_DAY);
        if (h >= 6 && h < 14) tvShiftInfo.setText("⏱️ SHIFT 1 (06:00 - 14:00)");
        else if (h >= 14 && h < 22) tvShiftInfo.setText("⏱️ SHIFT 2 (14:00 - 22:00)");
        else tvShiftInfo.setText("⏱️ SHIFT 3 NIGHT (22:00 - 06:00)");
    }

    private void setupLiveMeshListeners() {
        if (safetyService == null || safetyService.getBleMeshManager() == null) return;
        safetyService.getBleMeshManager().setListener(new BleMeshManager.MeshListener() {
            @Override
            public void onMinerUpdated(ConcurrentHashMap<String, BleMeshManager.PeerMiner> miners) {
                runOnUiThread(() -> {
                    tvMeshStatus.setText("🟢 OFFLINE MESH: " + miners.size() + " PEERS");
                    if (miners.isEmpty()) {
                        tvSonarDetail.setText("🔍 खदान में आसपास साथियों की खोज जारी...");
                    } else {
                        StringBuilder sb = new StringBuilder("निकटतम साथी: ");
                        for (BleMeshManager.PeerMiner p : miners.values()) {
                            sb.append(p.officerName).append(" (").append(p.distanceMeters).append("m) ");
                        }
                        tvSonarDetail.setText(sb.toString().trim());
                    }
                });
            }
            @Override
            public void onEmergencyReceived(String minerId, double distance) {
                runOnUiThread(() -> Toast.makeText(MainActivity.this, "🚨 OFFLINE SOS: " + minerId + " (" + distance + "m)", Toast.LENGTH_LONG).show());
            }
        });
    }

    private void refreshLiveLedgerData() {
        List<AlarmLogManager.AuditEntry> logs = alarmLogManager.getAllEntries();
        for (AlarmLogManager.AuditEntry e : logs) {
            if ("ATTENDANCE".equals(e.category) && e.remarks.contains("Present Miners:")) {
                try {
                    String count = e.remarks.split("Present Miners:")[1].split("\\|")[0].trim();
                    tvManpowerCount.setText(count + " Miners Active");
                } catch (Exception ignored) {}
            } else if ("GAS".equals(e.category)) {
                tvGasBadge.setText(e.isDanger ? "DANGER" : "SAFE");
                tvGasBadge.setTextColor(e.isDanger ? Color.RED : Color.parseColor("#22C55E"));
                tvGasReadout.setText(e.remarks);
            } else if ("STRATA".equals(e.category)) {
                tvStrataStatus.setText(e.remarks);
            }
        }
    }

    @Override
    public boolean onNavigationItemSelected(@NonNull android.view.MenuItem item) {
        drawerLayout.closeDrawer(GravityCompat.START);
        int id = item.getItemId();
        if (id == R.id.nav_sos) {
            if (safetyService != null) safetyService.triggerDualSos();
        } else if (id == R.id.nav_tracking) {
            startActivity(new Intent(this, RadarActivity.class));
        } else if (id == R.id.nav_form6) {
            startActivity(new Intent(this, ReportsActivity.class));
        } else {
            RegisterDialogHelper.showDedicatedDialog(this, item.getTitle().toString(), alarmLogManager, auditSyncManager, safetyService);
        }
        return true;
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
        for (String p : perms) {
            if (ContextCompat.checkSelfPermission(this, p) != PackageManager.PERMISSION_GRANTED) needed.add(p);
        }
        if (!needed.isEmpty()) ActivityCompat.requestPermissions(this, needed.toArray(new String[0]), 102);
    }

    @Override
    protected void onResume() {
        super.onResume();
        refreshLiveLedgerData();
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        if (auditSyncManager != null) auditSyncManager.close();
        if (isBound) {
            try { unbindService(serviceConn); } catch (Throwable ignored) {}
            isBound = false;
        }
    }
          }
