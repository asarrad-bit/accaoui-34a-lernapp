# Supabase Participant Dashboard Certificate Data Export Proof Release Status State Test

Stand: v27.14b
Bereich: Teilnehmer-Dashboard-Zertifikats-Datenexport-Nachweisfreigabestatus-State
Datei: data/supabase-client-adapter.js

## Ziel
Der vorbereitete Zertifikats-Datenexport-Nachweisfreigabestatus-State soll lokal verfügbar sein, aber verborgen bleiben.

## Browser-Test
window.ACCAOUI_SUPABASE_ADAPTER.getParticipantDashboardCertificateDataExportProofReleaseStatusState()

## Erwartetes Ergebnis
version: "v27.14a"
status: "local_dashboard_certificate_data_export_proof_release_status_hidden"
dependencyStatusMode: "reference_only_no_nested_state_execution"
isVisible: false
canRender: false
canTrackCertificateDataExportProofReleaseStatus: false
canRefreshCertificateDataExportProofReleaseStatus: false
isLocalDashboardAccessAllowed: true

## Bewertung
Keine echte Nachweisfreigabestatus-Prüfung, keine Teilnehmerdaten, keine Supabase-Kommunikation, kein UI-Blocker.

Status: erledigt
