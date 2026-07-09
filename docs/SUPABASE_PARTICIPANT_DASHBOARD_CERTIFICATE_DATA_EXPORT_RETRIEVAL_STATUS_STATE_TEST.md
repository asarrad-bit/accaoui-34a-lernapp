# Supabase Participant Dashboard Certificate Data Export Retrieval Status State Test

Stand: v27.05b
Bereich: Teilnehmer-Dashboard-Zertifikats-Datenexport-Abrufstatus-State
Datei: data/supabase-client-adapter.js

## Ziel
Der vorbereitete Zertifikats-Datenexport-Abrufstatus-State soll lokal verfügbar sein, aber verborgen bleiben.

## Browser-Test
window.ACCAOUI_SUPABASE_ADAPTER.getParticipantDashboardCertificateDataExportRetrievalStatusState()

## Erwartetes Ergebnis
version: "v27.05a"
status: "local_dashboard_certificate_data_export_retrieval_status_hidden"
dependencyStatusMode: "reference_only_no_nested_state_execution"
isVisible: false
canRender: false
canTrackCertificateDataExportRetrievalStatus: false
canRefreshCertificateDataExportRetrievalStatus: false
isLocalDashboardAccessAllowed: true

## Bewertung
Keine echte Abrufstatus-Prüfung, keine Teilnehmerdaten, keine Supabase-Kommunikation, kein UI-Blocker.

Status: erledigt
