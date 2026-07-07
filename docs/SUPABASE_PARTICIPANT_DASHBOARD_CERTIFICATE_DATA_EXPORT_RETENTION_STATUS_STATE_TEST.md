# Supabase Participant Dashboard Certificate Data Export Retention Status State Test

Stand: v26.91b
Bereich: Teilnehmer-Dashboard-Zertifikats-Datenexport-Aufbewahrungsstatus-State
Datei: data/supabase-client-adapter.js

## Ziel
Der vorbereitete Zertifikats-Datenexport-Aufbewahrungsstatus-State soll lokal verfügbar sein, aber verborgen bleiben.

## Browser-Test
window.ACCAOUI_SUPABASE_ADAPTER.getParticipantDashboardCertificateDataExportRetentionStatusState()

## Erwartetes Ergebnis
version: "v26.91a"
status: "local_dashboard_certificate_data_export_retention_status_hidden"
dependencyStatusMode: "reference_only_no_nested_state_execution"
isVisible: false
canRender: false
canTrackCertificateDataExportRetentionStatus: false
canRefreshCertificateDataExportRetentionStatus: false
isLocalDashboardAccessAllowed: true

## Bewertung
Keine echte Aufbewahrungsstatus-Prüfung, keine Teilnehmerdaten, keine Supabase-Kommunikation, kein UI-Blocker.

Status: erledigt
