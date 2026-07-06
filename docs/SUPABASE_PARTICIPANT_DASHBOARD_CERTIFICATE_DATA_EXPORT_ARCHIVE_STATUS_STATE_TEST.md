# Supabase Participant Dashboard Certificate Data Export Archive Status State Test

Stand: v26.89b
Bereich: Teilnehmer-Dashboard-Zertifikats-Datenexport-Archivstatus-State
Datei: data/supabase-client-adapter.js

## Ziel
Der vorbereitete Zertifikats-Datenexport-Archivstatus-State soll lokal verfügbar sein, aber verborgen bleiben.

## Browser-Test
window.ACCAOUI_SUPABASE_ADAPTER.getParticipantDashboardCertificateDataExportArchiveStatusState()

## Erwartetes Ergebnis
version: "v26.89a"
status: "local_dashboard_certificate_data_export_archive_status_hidden"
dependencyStatusMode: "reference_only_no_nested_state_execution"
isVisible: false
canRender: false
canTrackCertificateDataExportArchiveStatus: false
canRefreshCertificateDataExportArchiveStatus: false
isLocalDashboardAccessAllowed: true

## Bewertung
Keine echte Archivstatus-Prüfung, keine Teilnehmerdaten, keine Supabase-Kommunikation, kein UI-Blocker.

Status: erledigt
