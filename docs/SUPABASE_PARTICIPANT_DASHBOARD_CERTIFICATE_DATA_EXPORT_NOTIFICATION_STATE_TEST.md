# Supabase Participant Dashboard Certificate Data Export Notification State Test

Stand: v26.85b
Bereich: Teilnehmer-Dashboard-Zertifikats-Datenexport-Benachrichtigungs-State
Datei: data/supabase-client-adapter.js

## Ziel
Der vorbereitete Zertifikats-Datenexport-Benachrichtigungs-State soll lokal verfügbar sein, aber verborgen bleiben.

## Browser-Test
window.ACCAOUI_SUPABASE_ADAPTER.getParticipantDashboardCertificateDataExportNotificationState()

## Erwartetes Ergebnis
version: "v26.85a"
status: "local_dashboard_certificate_data_export_notification_hidden"
dependencyStatusMode: "reference_only_no_nested_state_execution"
isVisible: false
canRender: false
canSendCertificateDataExportNotification: false
canRefreshCertificateDataExportNotification: false
isLocalDashboardAccessAllowed: true

## Bewertung
Keine echte Benachrichtigung, keine Teilnehmerdaten, keine Supabase-Kommunikation, kein UI-Blocker.

Status: erledigt
