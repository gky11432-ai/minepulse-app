package com.mineguard.dgms;

import android.os.Bundle;
import androidx.appcompat.app.AppCompatActivity;

public class ReportsActivity extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_reports);

        findViewById(R.id.btn_print_master).setOnClickListener(v ->
                AuditPdfPrinter.printOrDownload(this, "ALL", "DGMS_Master_Shift_Dossier")
        );

        findViewById(R.id.btn_print_siren).setOnClickListener(v ->
                AuditPdfPrinter.printOrDownload(this, "SIREN", "DGMS_Emergency_Siren_Ledger")
        );

        findViewById(R.id.btn_print_gas).setOnClickListener(v ->
                AuditPdfPrinter.printOrDownload(this, "GAS", "DGMS_Gas_Ventilation_Register")
        );

        findViewById(R.id.btn_print_strata).setOnClickListener(v ->
                AuditPdfPrinter.printOrDownload(this, "STRATA", "DGMS_Roof_Support_Register")
        );
    }
}
