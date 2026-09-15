package com.mineguard.dgms;

import android.content.ComponentName;
import android.content.Context;
import android.content.Intent;
import android.content.ServiceConnection;
import android.os.Bundle;
import android.os.IBinder;
import android.widget.TextView;
import android.widget.Toast;
import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.view.GravityCompat;
import androidx.drawerlayout.widget.DrawerLayout;
import com.google.android.material.appbar.MaterialToolbar;
import com.google.android.material.button.MaterialButton;
import com.google.android.material.card.MaterialCardView;
import com.google.android.material.navigation.NavigationView;

public class MainActivity extends AppCompatActivity implements NavigationView.OnNavigationItemSelectedListener {
    private DrawerLayout drawerLayout;
    private MineSafetyService safetyService;
    private AuthManager authManager;
    private AlarmLogManager alarmLogManager;
    private boolean isBound = false;
    private TextView tvMeshStatus;

    private final ServiceConnection serviceConn = new ServiceConnection() {
        @Override
        public void onServiceConnected(ComponentName name, IBinder service) {
            MineSafetyService.LocalBinder binder = (MineSafetyService.LocalBinder) service;
            safetyService = binder.getService();
            isBound = true;
            RadarActivity.setMeshManager(safetyService.getBleMeshManager());
            setupAlertListeners();
        }
        @Override
        public void onServiceDisconnected(ComponentName name) { isBound = false; }
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        authManager = new AuthManager(this);
        alarmLogManager = new AlarmLogManager(this);

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
        MaterialCardView cardSiren = findViewById(R.id.card_emergency_siren);

        toolbar.setSubtitle(authManager.getOfficerName() + " (" + authManager.getOfficerId() + ")");
        toolbar.setNavigationOnClickListener(v -> drawerLayout.openDrawer(GravityCompat.START));
        navView.setNavigationItemSelectedListener(this);

        cardSiren.setOnClickListener(v -> {
            if (!isBound || safetyService == null) return;
            if (safetyService.getHardwareController().isSirenActive()) {
                safetyService.cancelDualSos();
                Toast.makeText(this, "सायरन बंद किया गया", Toast.LENGTH_SHORT).show();
            } else {
                safetyService.triggerDualSos();
                alarmLogManager.logAlarmEvent(authManager.getOfficerName(), authManager.getOfficerId(), authManager.getOfficerRole(), "MANUAL_SOS");
                Toast.makeText(this, "🚨 सायरन बजाया गया - लेजर में दर्ज!", Toast.LENGTH_LONG).show();
            }
        });

        bindService(new Intent(this, MineSafetyService.class), serviceConn, Context.BIND_AUTO_CREATE);
    }

    private void setupAlertListeners() {
        safetyService.getBleMeshManager().setListener(new BleMeshManager.MeshListener() {
            @Override
            public void onMinerUpdated(java.util.concurrent.ConcurrentHashMap<String, BleMeshManager.PeerMiner> miners) {
                runOnUiThread(() -> tvMeshStatus.setText("🟢 OFFLINE MESH: " + miners.size() + " PEERS"));
            }
            @Override
            public void onEmergencyReceived(String minerId, double distance) {
                alarmLogManager.logAlarmEvent(minerId, "REMOTE_MINER", "Underground Peer", "BLE_MESH_INBOUND");
                runOnUiThread(() -> Toast.makeText(MainActivity.this, "🚨 INCOMING SOS: " + minerId, Toast.LENGTH_LONG).show());
            }
        });
    }

    @Override
    public boolean onNavigationItemSelected(@NonNull android.view.MenuItem item) {
        drawerLayout.closeDrawer(GravityCompat.START);
        int id = item.getItemId();
        if (id == R.id.nav_sos) {
            if (safetyService != null) safetyService.triggerDualSos();
            alarmLogManager.logAlarmEvent(authManager.getOfficerName(), authManager.getOfficerId(), authManager.getOfficerRole(), "DRAWER_SOS");
        } else if (id == R.id.nav_tracking) {
            startActivity(new Intent(this, RadarActivity.class));
        } else if (id == R.id.nav_form6) {
            AuditPdfPrinter.printOrDownload(this);
        } else {
            RegisterDialogHelper.showEntryDialog(this, String.valueOf(id), item.getTitle().toString());
        }
        return true;
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        if (isBound) { unbindService(serviceConn); isBound = false; }
    }
}
