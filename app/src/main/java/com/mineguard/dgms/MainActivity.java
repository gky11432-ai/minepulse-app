package com.mineguard.dgms;

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
    private SirenRelayManager sirenRelayManager;
    private TextView tvMeshStatus, tvShiftHud, tvSirenTitle;
    private MaterialButton btnLangToggle, btnTorchToggle;
    private boolean isHindi = true;
    private Handler timerHandler = new Handler(Looper.getMainLooper());

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        hardwareController = new HardwareController(this);
        sirenRelayManager = new SirenRelayManager(this, hardwareController);

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

        cardSiren.setOnClickListener(v -> {
            if (hardwareController.isSirenActive()) {
                hardwareController.stopCollierySiren();
                Toast.makeText(this, isHindi ? "सायरन बंद किया गया" : "Siren Muted", Toast.LENGTH_SHORT).show();
            } else {
                sirenRelayManager.triggerCollieryBroadcast();
                Toast.makeText(this, isHindi ? "🚨 सायरन बजाया गया - सभी फोन में प्रसारित!" : "🚨 Evacuation Siren Triggered!", Toast.LENGTH_LONG).show();
            }
        });

        btnTorchToggle.setOnClickListener(v -> {
            boolean state = hardwareController.toggleTorch();
            btnTorchToggle.setText(state ? "🔦 ON" : "🔦 Torch");
        });

        btnLangToggle.setOnClickListener(v -> toggleLanguage());

        sirenRelayManager.setListener(new SirenRelayManager.SirenStateListener() {
            @Override
            public void onSirenReceived(String officer, String time) {
                Toast.makeText(MainActivity.this, "🚨 EVACUATION ALERT FROM: " + officer, Toast.LENGTH_LONG).show();
            }

            @Override
            public void onConnectionStateChanged(boolean isConnected) {
                tvMeshStatus.setText(isConnected ? "🟢 MESH: ACTIVE" : "🟠 MESH: CONNECTING");
                tvMeshStatus.setTextColor(isConnected ? 0xFF34D399 : 0xFFFBBF24);
            }
        });

        startShiftClock();
    }

    private void toggleLanguage() {
        isHindi = !isHindi;
        btnLangToggle.setText(isHindi ? "🌐 English" : "🌐 हिन्दी");
        tvSirenTitle.setText(isHindi ? "आपातकालीन सायरन" : "EMERGENCY SIREN");
    }

    private void startShiftClock() {
        timerHandler.postDelayed(new Runnable() {
            @Override
            public void run() {
                int hour = Integer.parseInt(new SimpleDateFormat("HH", Locale.getDefault()).format(new Date()));
                String shift = (hour >= 6 && hour < 14) ? "SHIFT 1 (06-14)" : (hour >= 14 && hour < 22) ? "SHIFT 2 (14-22)" : "SHIFT 3 (22-06)";
                String time = new SimpleDateFormat("HH:mm:ss", Locale.getDefault()).format(new Date());
                tvShiftHud.setText("⏱️ " + shift + " • " + time);
                timerHandler.postDelayed(this, 1000);
            }
        }, 1000);
    }

    @Override
    public boolean onNavigationItemSelected(@NonNull MenuItem item) {
        drawerLayout.closeDrawer(GravityCompat.START);
        int id = item.getItemId();

        if (id == R.id.nav_sos) {
            sirenRelayManager.triggerCollieryBroadcast();
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
        hardwareController.stopCollierySiren();
        sirenRelayManager.stopService();
    }
}
