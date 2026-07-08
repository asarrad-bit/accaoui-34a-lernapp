# Supabase Participant Dashboard Certificate Data Export Handover Status State Test

Stand: v27.01b
Bereich: Teilnehmer-Dashboard-Zertifikats-Datenexport-Übergabestatus-State
Datei: data/supabase-client-adapter.js

## Ziel
Der vorbereitete Zertifikats-Datenexport-Übergabestatus-State soll lokal verfügbar sein, aber verborgen bleiben.

## Browser-Test
window.ACCAOUI_SUPABASE_ADAPTER.getParticipantDashboardCertificateDataExportHandoverStatusState()

## Erwartetes Ergebnis
version: "v27.01a"
status: "local_dashboard_certificate_data_export_handover_status_hidden"
dependencyStatusMode: "reference_only_no_nested_state_execution"
isVisible: false
canRender: false
canTrackCertificateDataExportHandoverStatus: false
canRefreshCertificateDataExportHandoverStatus: false
isLocalDashboardAccessAllowed: true

## Bewertung
Keine echte Übergabestatus-Prüfung, keine Teilnehmerdaten, keine Supabase-Kommunikation, kein UI-Blocker.

Status: erledigt
