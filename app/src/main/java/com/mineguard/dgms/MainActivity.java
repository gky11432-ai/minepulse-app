package com.mineguard.dgms;

import android.content.ComponentName;
import android.content.Context;
import android.content.Intent;
import android.content.ServiceConnection;
import android.os.Bundle;
import android.os.IBinder;
import android.widget.TextView;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {
    private MineSafetyService safetyService;
    private AuthManager authManager;
    private AlarmLogManager alarmLogManager;
    private AuditSyncManager auditSyncManager;
    private boolean isBound = false;

    private TextView tvOfficerName, tvOfficerRole, tvPeerCount;

    private final ServiceConnection serviceConn = new ServiceConnection() {
        @Override
        public void onServiceConnected(ComponentName name, IBinder service) {
            MineSafetyService.LocalBinder binder = (MineSafetyService.LocalBinder) service;
            safetyService = binder.getService();
            isBound = true;
            RadarActivity.setMeshManager(safetyService.getBleMeshManager());
            setupMeshListeners();
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

        tvOfficerName = findViewById(R.id.tv_officer_name);
        tvOfficerRole = findViewById(R.id.tv_officer_role);
        tvPeerCount = findViewById(R.id.tv_peer_count);

        tvOfficerName.setText(authManager.getOfficerName());
        tvOfficerRole.setText(authManager.getOfficerRole());

        // Bento Actions
        findViewById(R.id.btn_roll_call).setOnClickListener(v ->
                RegisterDialogHelper.showDedicatedDialog(this, "Form B Attendance", alarmLogManager, auditSyncManager, safetyService)
        );

        findViewById(R.id.btn_roof_log).setOnClickListener(v ->
                RegisterDialogHelper.showDedicatedDialog(this, "CMR 123 Strata", alarmLogManager, auditSyncManager, safetyService)
        );

        // Emergency SOS Action
        findViewById(R.id.card_sos_action).setOnClickListener(v -> {
            if (safetyService != null) {
                safetyService.triggerDualSos();
                alarmLogManager.logAlarmEvent(authManager.getOfficerName(), authManager.getOfficerId(), authManager.getOfficerRole(), "SOS_EVACUATION");
                Toast.makeText(this, "🚨 COLLIERY SOS EVACUATION TRIGGERED!", Toast.LENGTH_LONG).show();
            }
        });

        // Floating Dock Buttons
        findViewById(R.id.dock_btn_radar).setOnClickListener(v -> startActivity(new Intent(this, RadarActivity.class)));
        findViewById(R.id.dock_btn_logs).setOnClickListener(v -> startActivity(new Intent(this, ReportsActivity.class)));
        findViewById(R.id.dock_btn_pdf).setOnClickListener(v -> AuditPdfPrinter.printOrDownload(this, "ALL", "DGMS_Master_Shift_Dossier"));

        // Bottom Nav Bar
        findViewById(R.id.nav_reports).setOnClickListener(v -> startActivity(new Intent(this, ReportsActivity.class)));
        findViewById(R.id.nav_map).setOnClickListener(v -> startActivity(new Intent(this, RadarActivity.class)));

        startService(new Intent(this, MineSafetyService.class));
        bindService(new Intent(this, MineSafetyService.class), serviceConn, Context.BIND_AUTO_CREATE);
    }

    private void setupMeshListeners() {
        if (safetyService == null || safetyService.getBleMeshManager() == null) return;
        safetyService.getBleMeshManager().setListener(new BleMeshManager.MeshListener() {
            @Override
            public void onMinerUpdated(java.util.concurrent.ConcurrentHashMap<String, BleMeshManager.PeerMiner> miners) {
                runOnUiThread(() -> tvPeerCount.setText("ᛒ " + miners.size() + " Peers Linked • BLE"));
            }
            @Override
            public void onEmergencyReceived(String minerId, double distance) {
                runOnUiThread(() -> Toast.makeText(MainActivity.this, "🚨 INCOMING SOS: " + minerId, Toast.LENGTH_LONG).show());
            }
        });
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        if (isBound) {
            try { unbindService(serviceConn); } catch (Throwable ignored) {}
            isBound = false;
        }
    }
}
