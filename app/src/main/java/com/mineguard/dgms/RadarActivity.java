package com.mineguard.dgms;

import android.os.Bundle;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import android.widget.TextView;
import androidx.appcompat.app.AppCompatActivity;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.ConcurrentHashMap;

public class RadarActivity extends AppCompatActivity {
    private ListView lvMiners;
    private TextView tvRadarCount;
    private ArrayAdapter<String> adapter;
    private final List<String> minerDisplayList = new ArrayList<>();
    private static BleMeshManager sharedMeshManager;

    public static void setMeshManager(BleMeshManager manager) {
        sharedMeshManager = manager;
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_radar);
        lvMiners = findViewById(R.id.lv_miners);
        tvRadarCount = findViewById(R.id.tv_radar_count);

        adapter = new ArrayAdapter<>(this, android.R.layout.simple_list_item_1, minerDisplayList);
        lvMiners.setAdapter(adapter);

        if (sharedMeshManager != null) {
            sharedMeshManager.setListener(new BleMeshManager.MeshListener() {
                @Override
                public void onMinerUpdated(ConcurrentHashMap<String, BleMeshManager.PeerMiner> miners) {
                    runOnUiThread(() -> updateRadarUI(miners));
                }
                @Override
                public void onEmergencyReceived(String minerId, double distance) {}
            });
            updateRadarUI(sharedMeshManager.getNearbyMiners());
        }
    }

    private void updateRadarUI(ConcurrentHashMap<String, BleMeshManager.PeerMiner> miners) {
        minerDisplayList.clear();
        int count = 0;
        long now = System.currentTimeMillis();

        for (BleMeshManager.PeerMiner m : miners.values()) {
            if (now - m.lastSeen < 30000) {
                count++;
                String alert = m.isEmergency ? "🚨 DANGER / SOS ACTIVE" : "🟢 NORMAL (SAFE)";
                String card = "👷 " + m.officerName + " [" + m.officerRole + "]\n"
                        + "📍 Approx Distance: " + m.distanceMeters + " Meters (Signal: " + m.rssi + " dBm)\n"
                        + "Status: " + alert;
                minerDisplayList.add(card);
            }
        }

        tvRadarCount.setText("⚡ Detected Personnel (Underground): " + count);
        adapter.notifyDataSetChanged();
    }
}
