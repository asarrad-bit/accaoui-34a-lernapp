# Supabase Participant Dashboard Certificate Data Export Approval Status State Test

Stand: v26.96b
Bereich: Teilnehmer-Dashboard-Zertifikats-Datenexport-Freigabestatus-State
Datei: data/supabase-client-adapter.js

## Ziel
Der vorbereitete Zertifikats-Datenexport-Freigabestatus-State soll lokal verfügbar sein, aber verborgen bleiben.

## Browser-Test
window.ACCAOUI_SUPABASE_ADAPTER.getParticipantDashboardCertificateDataExportApprovalStatusState()

## Erwartetes Ergebnis
version: "v26.96a"
status: "local_dashboard_certificate_data_export_approval_status_hidden"
dependencyStatusMode: "reference_only_no_nested_state_execution"
isVisible: false
canRender: false
canTrackCertificateDataExportApprovalStatus: false
canRefreshCertificateDataExportApprovalStatus: false
isLocalDashboardAccessAllowed: true

## Bewertung
Keine echte Freigabestatus-Prüfung, keine Teilnehmerdaten, keine Supabase-Kommunikation, kein UI-Blocker.

Status: erledigt
