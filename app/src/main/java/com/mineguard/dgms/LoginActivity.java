package com.mineguard.dgms;

import android.content.Intent;
import android.os.Bundle;
import android.widget.ArrayAdapter;
import android.widget.EditText;
import android.widget.Spinner;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;
import com.google.android.material.button.MaterialButton;

public class LoginActivity extends AppCompatActivity {
    private AuthManager authManager;
    private EditText etName, etId, etPin;
    private Spinner spRole;

    private final String[] ROLES = {
            "Mining Sirdar (CMR 48)",
            "Overman (CMR 47)",
            "Colliery Manager (CMR 27)",
            "Safety Officer (CMR 29)",
            "Ventilation Officer (CMR 153)"
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        authManager = new AuthManager(this);

        // If already logged in, jump straight to Main Console
        if (authManager.isLoggedIn()) {
            launchMainConsole();
            return;
        }

        setContentView(R.layout.activity_login);

        etName = findViewById(R.id.et_login_name);
        etId = findViewById(R.id.et_login_id);
        etPin = findViewById(R.id.et_login_pin);
        spRole = findViewById(R.id.sp_login_role);
        MaterialButton btnLogin = findViewById(R.id.btn_submit_login);

        ArrayAdapter<String> adapter = new ArrayAdapter<>(this, android.R.layout.simple_spinner_dropdown_item, ROLES);
        spRole.setAdapter(adapter);

        btnLogin.setOnClickListener(v -> processLogin());
    }

    private void processLogin() {
        String name = etName.getText().toString().trim();
        String id = etId.getText().toString().trim();
        String role = spRole.getSelectedItem().toString();
        String pin = etPin.getText().toString().trim();

        if (name.isEmpty() || id.isEmpty() || pin.length() != 4) {
            Toast.makeText(this, "कृपया नाम, ID और 4 अंकों का PIN सही से दर्ज करें!", Toast.LENGTH_SHORT).show();
            return;
        }

        boolean success = authManager.authenticate(id, name, role, pin);
        if (success) {
            Toast.makeText(this, "प्रमाणीकरण सफल: स्वागत है " + name, Toast.LENGTH_SHORT).show();
            launchMainConsole();
        } else {
            Toast.makeText(this, "गलत पिन! अधिकृत पिन दर्ज करें।", Toast.LENGTH_SHORT).show();
        }
    }

    private void launchMainConsole() {
        Intent intent = new Intent(this, MainActivity.class);
        startActivity(intent);
        finish();
    }
}
