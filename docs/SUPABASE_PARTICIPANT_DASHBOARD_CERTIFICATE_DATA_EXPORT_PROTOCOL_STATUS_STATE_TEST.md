# Supabase Participant Dashboard Certificate Data Export Protocol Status State Test

Stand: v27.06b
Bereich: Teilnehmer-Dashboard-Zertifikats-Datenexport-Protokollstatus-State
Datei: data/supabase-client-adapter.js

## Ziel
Der vorbereitete Zertifikats-Datenexport-Protokollstatus-State soll lokal verfügbar sein, aber verborgen bleiben.

## Browser-Test
window.ACCAOUI_SUPABASE_ADAPTER.getParticipantDashboardCertificateDataExportProtocolStatusState()

## Erwartetes Ergebnis
version: "v27.06a"
status: "local_dashboard_certificate_data_export_protocol_status_hidden"
dependencyStatusMode: "reference_only_no_nested_state_execution"
isVisible: false
canRender: false
canTrackCertificateDataExportProtocolStatus: false
canRefreshCertificateDataExportProtocolStatus: false
isLocalDashboardAccessAllowed: true

## Bewertung
Keine echte Protokollstatus-Prüfung, keine Teilnehmerdaten, keine Supabase-Kommunikation, kein UI-Blocker.

Status: erledigt
