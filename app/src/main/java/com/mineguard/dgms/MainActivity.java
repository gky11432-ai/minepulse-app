package com.mineguard.dgms;

import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.view.MenuItem;
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
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;

public class MainActivity extends AppCompatActivity implements NavigationView.OnNavigationItemSelectedListener {

    private DrawerLayout drawerLayout;
    private HardwareController hardwareController;
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

        // Offline Big Siren Click
        cardSiren.setOnClickListener(v -> {
            if (hardwareController.isSirenActive()) {
                bleMeshManager.cancelOfflineSos(myMinerToken);
                Toast.makeText(this, isHindi ? "सायरन बंद किया गया" : "Siren Muted", Toast.LENGTH_SHORT).show();
            } else {
                bleMeshManager.triggerOfflineSos(myMinerToken);
                Toast.makeText(this, isHindi ? "🚨 ऑफ़लाइन सायरन बजाया गया - 50m के सभी मोबाइलों में प्रसारित!" : "🚨 Offline SOS Broadcasted!", Toast.LENGTH_LONG).show();
            }
        });

        btnTorchToggle.setOnClickListener(v -> {
            boolean state = hardwareController.toggleTorch();
            btnTorchToggle.setText(state ? "🔦 ON" : "🔦 Torch");
        });

        btnLangToggle.setOnClickListener(v -> toggleLanguage());

        // Mesh Alert Listener
        bleMeshManager.setListener(new BleMeshManager.MeshListener() {
            @Override
            public void onMinerUpdated(java.util.concurrent.ConcurrentHashMap<String, BleMeshManager.PeerMiner> miners) {
                runOnUiThread(() -> tvMeshStatus.setText("🟢 OFFLINE MESH: " + miners.size() + " PEERS"));
            }

            @Override
            public void onEmergencyReceived(String minerId, double distance) {
                runOnUiThread(() -> Toast.makeText(MainActivity.this, "🚨 OFFLINE SOS FROM: " + minerId + " (" + distance + "m away)", Toast.LENGTH_LONG).show());
            }
        });

        // Man-Down Detector
        manDownDetector.setListener(new ManDownDetector.ManDownListener() {
            @Override
            public void onWarningCountdown(int sec) {
                runOnUiThread(() -> Toast.makeText(MainActivity.this, "⚠️ FALL WARNING: No motion! Siren in " + sec + "s", Toast.LENGTH_SHORT).show());
            }
            @Override
            public void onFallDetectedAlarm() {
                runOnUiThread(() -> Toast.makeText(MainActivity.this, "🚨 MAN-DOWN ACTIVATED: Miner Collapsed!", Toast.LENGTH_LONG).show());
            }
            @Override
            public void onMovementRestored() {}
        });

        bleMeshManager.startOfflineMesh(myMinerToken);
        manDownDetector.startMonitoring();
    }

    private void toggleLanguage() {
        isHindi = !isHindi;
        btnLangToggle.setText(isHindi ? "🌐 English" : "🌐 हिन्दी");
        tvSirenTitle.setText(isHindi ? "आपातकालीन सायरन" : "EMERGENCY SIREN");
    }

    @Override
    public boolean onNavigationItemSelected(@NonNull MenuItem item) {
        drawerLayout.closeDrawer(GravityCompat.START);
        int id = item.getItemId();

        if (id == R.id.nav_sos) {
            bleMeshManager.triggerOfflineSos(myMinerToken);
        } else if (id == R.id.nav_tracking) {
            startActivity(new Intent(this, RadarActivity.class));
        } else if (id == R.id.nav_form6) {
            Form6PdfGenerator.generateAndShareForm6(this);
        } else {
            RegisterDialogHelper.showEntryDialog(this, String.valueOf(item.getItemId()), item.getTitle().toString());
        }
        return true;
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        bleMeshManager.stopMesh();
        manDownDetector.stopMonitoring();
        hardwareController.stopCollierySiren();
    }
}
