package com.mineguard.dgms;

import android.Manifest;
import android.content.ComponentName;
import android.content.Context;
import android.content.Intent;
import android.content.ServiceConnection;
import android.content.pm.PackageManager;
import android.location.LocationManager;
import android.os.Build;
import android.os.Bundle;
import android.os.IBinder;
import android.provider.Settings;
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
    private MineSafetyService safetyService;
    private boolean isBound = false;
    private TextView tvMeshStatus, tvShiftHud, tvSirenTitle;
    private MaterialButton btnLangToggle, btnTorchToggle;
    private boolean isHindi = true;

    private final ServiceConnection serviceConn = new ServiceConnection() {
        @Override
        public void onServiceConnected(ComponentName name, IBinder service) {
            MineSafetyService.LocalBinder binder = (MineSafetyService.LocalBinder) service;
            safetyService = binder.getService();
            isBound = true;
            RadarActivity.setMeshManager(safetyService.getBleMeshManager());
            setupListeners();
        }
        @Override
        public void onServiceDisconnected(ComponentName name) { isBound = false; }
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

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
            if (!isBound || safetyService == null) return;
            if (safetyService.getHardwareController().isSirenActive()) {
                safetyService.cancelDualSos();
                Toast.makeText(this, isHindi ? "सायरन बंद किया गया" : "Siren Muted", Toast.LENGTH_SHORT).show();
            } else {
                safetyService.triggerDualSos();
                Toast.makeText(this, isHindi ? "🚨 ऑफ़लाइन + ऑनलाइन सायरन प्रसारित!" : "🚨 Emergency Broadcasted!", Toast.LENGTH_LONG).show();
            }
        });

        btnTorchToggle.setOnClickListener(v -> {
            if (isBound && safetyService != null) {
                boolean state = safetyService.getHardwareController().toggleTorch();
                btnTorchToggle.setText(state ? "🔦 ON" : "🔦 Torch");
            }
        });

        btnLangToggle.setOnClickListener(v -> toggleLanguage());

        checkPermissionsAndStartService();
        verifyLocationEnabled();
    }

    private void setupListeners() {
        safetyService.getBleMeshManager().setListener(new BleMeshManager.MeshListener() {
            @Override
            public void onMinerUpdated(java.util.concurrent.ConcurrentHashMap<String, BleMeshManager.PeerMiner> miners) {
                runOnUiThread(() -> tvMeshStatus.setText("🟢 OFFLINE MESH: " + miners.size() + " PEERS"));
            }
            @Override
            public void onEmergencyReceived(String minerId, double distance) {
                runOnUiThread(() -> Toast.makeText(MainActivity.this, "🚨 OFFLINE SOS: " + minerId + " (" + distance + "m)", Toast.LENGTH_LONG).show());
            }
        });
    }

    private void checkPermissionsAndStartService() {
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

        List<String> requestList = new ArrayList<>();
        for (String p : perms) {
            if (ContextCompat.checkSelfPermission(this, p) != PackageManager.PERMISSION_GRANTED) requestList.add(p);
        }

        if (!requestList.isEmpty()) {
            ActivityCompat.requestPermissions(this, requestList.toArray(new String[0]), 101);
        } else {
            bindSafetyService();
        }
    }

    private void verifyLocationEnabled() {
        LocationManager lm = (LocationManager) getSystemService(Context.LOCATION_SERVICE);
        if (lm != null && !lm.isProviderEnabled(LocationManager.GPS_PROVIDER)) {
            Toast.makeText(this, "⚠️ कृपया फ़ोन का Location/GPS टॉगल चालू करें ताकि ऑफ़लाइन ब्लूटूथ मेश सिग्नल पकड़ सके!", Toast.LENGTH_LONG).show();
        }
    }

    private void bindSafetyService() {
        Intent sIntent = new Intent(this, MineSafetyService.class);
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            startForegroundService(sIntent);
        } else {
            startService(sIntent);
        }
        bindService(sIntent, serviceConn, Context.BIND_AUTO_CREATE);
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        bindSafetyService();
    }

    private void toggleLanguage() {
        isHindi = !isHindi;
        btnLangToggle.setText(isHindi ? "🌐 English" : "🌐 हिन्दी");
        tvSirenTitle.setText(isHindi ? "आपातकालीन सायरन" : "EMERGENCY SIREN");
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
            Form6PdfGenerator.generateAndShareForm6(this);
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
