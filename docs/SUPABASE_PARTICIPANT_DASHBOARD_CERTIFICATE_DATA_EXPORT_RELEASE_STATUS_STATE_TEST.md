# Supabase Participant Dashboard Certificate Data Export Release Status State Test

Stand: v27.04b
Bereich: Teilnehmer-Dashboard-Zertifikats-Datenexport-Freigabestatus-State
Datei: data/supabase-client-adapter.js

## Ziel
Der vorbereitete Zertifikats-Datenexport-Freigabestatus-State soll lokal verfügbar sein, aber verborgen bleiben.

## Browser-Test
window.ACCAOUI_SUPABASE_ADAPTER.getParticipantDashboardCertificateDataExportReleaseStatusState()

## Erwartetes Ergebnis
version: "v27.04a"
status: "local_dashboard_certificate_data_export_release_status_hidden"
dependencyStatusMode: "reference_only_no_nested_state_execution"
isVisible: false
canRender: false
canTrackCertificateDataExportReleaseStatus: false
canRefreshCertificateDataExportReleaseStatus: false
isLocalDashboardAccessAllowed: true

## Bewertung
Keine echte Freigabestatus-Prüfung, keine Teilnehmerdaten, keine Supabase-Kommunikation, kein UI-Blocker.

Status: erledigt
