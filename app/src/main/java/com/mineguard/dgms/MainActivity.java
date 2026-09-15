package com.mineguard.dgms;

import android.Manifest;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.os.Build;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.view.MenuItem;
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
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.Locale;

public class MainActivity extends AppCompatActivity implements NavigationView.OnNavigationItemSelectedListener {

    private DrawerLayout drawerLayout;
    private HardwareController hardwareController;
    private SirenRelayManager sirenRelayManager;
    private BleMeshManager bleMeshManager;
    private ManDownDetector manDownDetector;
    private TextView tvMeshStatus, tvShiftHud, tvSirenTitle;
    private MaterialButton btnLangToggle, btnTorchToggle;
    private boolean isHindi = true;
    private final String myMinerToken = "TK-" + (int)(100 + Math.random() * 900);

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        hardwareController = new HardwareController(this);
        sirenRelayManager = new SirenRelayManager(this, hardwareController);
        bleMeshManager = new BleMeshManager(this, hardwareController);
        manDownDetector = new ManDownDetector(this, bleMeshManager);
        RadarActivity.setMeshManager(bleMeshManager);

        drawerLayout = findViewById(R.id.drawer_layout);
        MaterialToolbar toolbar = findViewById(R.id.top_toolbar);
        NavigationView navView = findViewById(R.id.nav_view);
        tvMeshStatus = findViewById(R.id.tv_mesh_status);
        tvShiftHud = findViewById(R.id.tv_shift_hud);
        tvSirenTitle = findViewById(R.id.tv_siren_title);
        btnLangToggle = findViewById(R.id.btn_lang_toggle);
        btnTorchToggle = findViewById(R.id.btn_torch_toggle);
        MaterialCardView cardSiren = findViewById(R.id.card_emergency_siren);

        toolbar.setNavigationOnClickListener(v -> drawerLayout.openDrawer(GravityCompat.START));
        navView.setNavigationItemSelectedListener(this);

        // Hybrid Dual Trigger: Online + Offline Together
        cardSiren.setOnClickListener(v -> {
            if (hardwareController.isSirenActive()) {
                hardwareController.stopCollierySiren();
                bleMeshManager.cancelOfflineSos(myMinerToken);
                Toast.makeText(this, isHindi ? "सायरन बंद किया गया" : "Siren Muted", Toast.LENGTH_SHORT).show();
            } else {
                sirenRelayManager.triggerCollieryBroadcast(); // Online
                bleMeshManager.triggerOfflineSos(myMinerToken); // Offline
                Toast.makeText(this, isHindi ? "🚨 सायरन सक्रिय (ऑनलाइन + ऑफ़लाइन प्रसारित)!" : "🚨 Emergency Broadcasted (Dual Engine)!", Toast.LENGTH_LONG).show();
            }
        });

        btnTorchToggle.setOnClickListener(v -> {
            boolean state = hardwareController.toggleTorch();
            btnTorchToggle.setText(state ? "🔦 ON" : "🔦 Torch");
        });

        btnLangToggle.setOnClickListener(v -> toggleLanguage());

        // Listeners for incoming alarms
        sirenRelayManager.setListener(new SirenRelayManager.SirenStateListener() {
            @Override
            public void onSirenReceived(String officer, String time) {
                runOnUiThread(() -> Toast.makeText(MainActivity.this, "🚨 [ONLINE] EMERGENCY FROM: " + officer, Toast.LENGTH_LONG).show());
            }
            @Override
            public void onConnectionStateChanged(boolean isConnected) {
                runOnUiThread(() -> updateNetworkHUD(isConnected, 0));
            }
        });

        bleMeshManager.setListener(new BleMeshManager.MeshListener() {
            @Override
            public void onMinerUpdated(java.util.concurrent.ConcurrentHashMap<String, BleMeshManager.PeerMiner> miners) {
                runOnUiThread(() -> updateNetworkHUD(true, miners.size()));
            }
            @Override
            public void onEmergencyReceived(String minerId, double distance) {
                runOnUiThread(() -> Toast.makeText(MainActivity.this, "🚨 [OFFLINE MESH] SOS: " + minerId + " (" + distance + "m)", Toast.LENGTH_LONG).show());
            }
        });

        checkAndRequestPermissions();
        startShiftClock();
    }

    private void checkAndRequestPermissions() {
        List<String> needed = new ArrayList<>();
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
            needed.add(Manifest.permission.BLUETOOTH_SCAN);
            needed.add(Manifest.permission.BLUETOOTH_ADVERTISE);
            needed.add(Manifest.permission.BLUETOOTH_CONNECT);
        }
        needed.add(Manifest.permission.ACCESS_FINE_LOCATION);
        needed.add(Manifest.permission.CAMERA);

        List<String> askList = new ArrayList<>();
        for (String perm : needed) {
            if (ContextCompat.checkSelfPermission(this, perm) != PackageManager.PERMISSION_GRANTED) {
                askList.add(perm);
            }
        }

        if (!askList.isEmpty()) {
            ActivityCompat.requestPermissions(this, askList.toArray(new String[0]), 101);
        } else {
            startEngines();
        }
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        startEngines();
    }

    private void startEngines() {
        bleMeshManager.startOfflineMesh(myMinerToken);
        manDownDetector.startMonitoring();
    }

    private void updateNetworkHUD(boolean online, int offlinePeers) {
        String txt = (online ? "🟢 ONLINE" : "🟠 OFFLINE") + " • MESH: " + offlinePeers + " PEERS";
        tvMeshStatus.setText(txt);
        tvMeshStatus.setTextColor(online ? 0xFF34D399 : 0xFFFBBF24);
    }

    private void toggleLanguage() {
        isHindi = !isHindi;
        btnLangToggle.setText(isHindi ? "🌐 English" : "🌐 हिन्दी");
        tvSirenTitle.setText(isHindi ? "आपातकालीन सायरन" : "EMERGENCY SIREN");
    }

    private void startShiftClock() {
        new Handler(Looper.getMainLooper()).postDelayed(new Runnable() {
            @Override
            public void run() {
                int hour = Integer.parseInt(new SimpleDateFormat("HH", Locale.getDefault()).format(new Date()));
                String shift = (hour >= 6 && hour < 14) ? "SHIFT 1 (06-14)" : (hour >= 14 && hour < 22) ? "SHIFT 2 (14-22)" : "SHIFT 3 (22-06)";
                tvShiftHud.setText("⏱️ " + shift + " • " + new SimpleDateFormat("HH:mm:ss", Locale.getDefault()).format(new Date()));
                new Handler(Looper.getMainLooper()).postDelayed(this, 1000);
            }
        }, 1000);
    }

    @Override
    public boolean onNavigationItemSelected(@NonNull MenuItem item) {
        drawerLayout.closeDrawer(GravityCompat.START);
        int id = item.getItemId();
        if (id == R.id.nav_sos) {
            sirenRelayManager.triggerCollieryBroadcast();
            bleMeshManager.triggerOfflineSos(myMinerToken);
        } else if (id == R.id.nav_tracking) {
            startActivity(new Intent(this, RadarActivity.class));
        } else if (id == R.id.nav_form6) {
            Form6PdfGenerator.generateAndShareForm6(this);
        } else {
            RegisterDialogHelper.showEntryDialog(this, String.valueOf(id), item.getTitle().toString());
        }
        return true;
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        bleMeshManager.stopMesh();
        manDownDetector.stopMonitoring();
        hardwareController.stopCollierySiren();
        sirenRelayManager.stopService();
    }
        }
