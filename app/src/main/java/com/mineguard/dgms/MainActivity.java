package com.mineguard.dgms;

import android.Manifest;
import android.content.ComponentName;
import android.content.Context;
import android.content.Intent;
import android.content.ServiceConnection;
import android.content.pm.PackageManager;
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
import java.util.List;

public class MainActivity extends AppCompatActivity implements NavigationView.OnNavigationItemSelectedListener {
    private DrawerLayout drawerLayout;
    private MineSafetyService safetyService;
    private AuthManager authManager;
    private AlarmLogManager alarmLogManager;
    private AuditSyncManager auditSyncManager;
    private boolean isBound = false;
    private TextView tvMeshStatus;
    private MaterialButton btnTorchToggle;

    private final ServiceConnection serviceConn = new ServiceConnection() {
        @Override
        public void onServiceConnected(ComponentName name, IBinder service) {
            try {
                MineSafetyService.LocalBinder binder = (MineSafetyService.LocalBinder) service;
                safetyService = binder.getService();
                isBound = true;
                RadarActivity.setMeshManager(safetyService.getBleMeshManager());
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
        drawerLayout = findViewById(R.id.drawer_layout);
        MaterialToolbar toolbar = findViewById(R.id.top_toolbar);
        NavigationView navView = findViewById(R.id.nav_view);
        tvMeshStatus = findViewById(R.id.tv_mesh_status);
        btnTorchToggle = findViewById(R.id.btn_torch_toggle);
        MaterialCardView cardSiren = findViewById(R.id.card_emergency_siren);

        toolbar.setSubtitle(authManager.getOfficerName() + " (" + authManager.getOfficerRole() + ")");
        toolbar.setNavigationOnClickListener(v -> drawerLayout.openDrawer(GravityCompat.START));
        navView.setNavigationItemSelectedListener(this);

        // Remote Audit Received Listener (Auto-Alarm on Danger)
        auditSyncManager.setListener((officerName, category, isDanger) -> runOnUiThread(() -> {
            if (isDanger && safetyService != null) {
                safetyService.triggerDualSos();
                Toast.makeText(MainActivity.this, "🚨 डेंजर अलर्ट: " + officerName + " (" + category + ") - सायरन सक्रिय!", Toast.LENGTH_LONG).show();
            } else {
                Toast.makeText(MainActivity.this, "🔄 सिंक प्राप्त: " + officerName + " (" + category + ")", Toast.LENGTH_SHORT).show();
            }
        }));

        btnTorchToggle.setOnClickListener(v -> {
            if (isBound && safetyService != null) {
                boolean state = safetyService.getHardwareController().toggleTorch();
                btnTorchToggle.setText(state ? "🔦 ON" : "🔦 Torch");
            }
        });

        cardSiren.setOnClickListener(v -> {
            if (!isBound || safetyService == null) return;
            if (safetyService.getHardwareController().isSirenActive()) {
                safetyService.cancelDualSos();
                Toast.makeText(this, "सायरन बंद किया गया", Toast.LENGTH_SHORT).show();
            } else {
                safetyService.triggerDualSos();
                AlarmLogManager.AuditEntry sosEntry = alarmLogManager.logLocalEntry(
                        authManager.getOfficerName(), authManager.getOfficerId(), authManager.getOfficerRole(), "SIREN", "MANUAL_SOS", true
                );
                auditSyncManager.broadcastAudit(sosEntry);
                Toast.makeText(this, "🚨 सायरन बजाया गया!", Toast.LENGTH_LONG).show();
            }
        });

        startService(new Intent(this, MineSafetyService.class));
        bindService(new Intent(this, MineSafetyService.class), serviceConn, Context.BIND_AUTO_CREATE);
        checkPermissions();
    }

    private void checkPermissions() {
        List<String> perms = new ArrayList<>();
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
            perms.add(Manifest.permission.BLUETOOTH_SCAN);
            perms.add(Manifest.permission.BLUETOOTH_ADVERTISE);
            perms.add(Manifest.permission.BLUETOOTH_CONNECT);
        }
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            perms.add(Manifest.permission.POST_NOTIFICATIONS);
        }
        perms.add(Manifest.permission.ACCESS_FINE_LOCATION);
        perms.add(Manifest.permission.CAMERA);

        List<String> needed = new ArrayList<>();
        for (String p : perms) {
            if (ContextCompat.checkSelfPermission(this, p) != PackageManager.PERMISSION_GRANTED) needed.add(p);
        }
        if (!needed.isEmpty()) {
            ActivityCompat.requestPermissions(this, needed.toArray(new String[0]), 102);
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
