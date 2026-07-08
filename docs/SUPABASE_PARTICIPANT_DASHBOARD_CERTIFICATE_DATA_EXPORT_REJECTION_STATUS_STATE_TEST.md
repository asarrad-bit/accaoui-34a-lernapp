# Supabase Participant Dashboard Certificate Data Export Rejection Status State Test

Stand: v26.97b
Bereich: Teilnehmer-Dashboard-Zertifikats-Datenexport-Ablehnungsstatus-State
Datei: data/supabase-client-adapter.js

## Ziel
Der vorbereitete Zertifikats-Datenexport-Ablehnungsstatus-State soll lokal verfügbar sein, aber verborgen bleiben.

## Browser-Test
window.ACCAOUI_SUPABASE_ADAPTER.getParticipantDashboardCertificateDataExportRejectionStatusState()

## Erwartetes Ergebnis
version: "v26.97a"
status: "local_dashboard_certificate_data_export_rejection_status_hidden"
dependencyStatusMode: "reference_only_no_nested_state_execution"
isVisible: false
canRender: false
canTrackCertificateDataExportRejectionStatus: false
canRefreshCertificateDataExportRejectionStatus: false
isLocalDashboardAccessAllowed: true

## Bewertung
Keine echte Ablehnungsstatus-Prüfung, keine Teilnehmerdaten, keine Supabase-Kommunikation, kein UI-Blocker.

Status: erledigt
