# Supabase Participant Dashboard Certificate Data Export Deletion Status State Test

Stand: v26.90b
Bereich: Teilnehmer-Dashboard-Zertifikats-Datenexport-Löschstatus-State
Datei: data/supabase-client-adapter.js

## Ziel
Der vorbereitete Zertifikats-Datenexport-Löschstatus-State soll lokal verfügbar sein, aber verborgen bleiben.

## Browser-Test
window.ACCAOUI_SUPABASE_ADAPTER.getParticipantDashboardCertificateDataExportDeletionStatusState()

## Erwartetes Ergebnis
version: "v26.90a"
status: "local_dashboard_certificate_data_export_deletion_status_hidden"
dependencyStatusMode: "reference_only_no_nested_state_execution"
isVisible: false
canRender: false
canTrackCertificateDataExportDeletionStatus: false
canRefreshCertificateDataExportDeletionStatus: false
isLocalDashboardAccessAllowed: true

## Bewertung
Keine echte Löschstatus-Prüfung, keine Teilnehmerdaten, keine Supabase-Kommunikation, kein UI-Blocker.

Status: erledigt
