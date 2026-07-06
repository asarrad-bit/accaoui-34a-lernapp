# Supabase Participant Dashboard Certificate Data Export File State Test

Stand: v26.79b
Bereich: Teilnehmer-Dashboard-Zertifikats-Datenexport-Datei-State
Datei: data/supabase-client-adapter.js

## Ziel

Der vorbereitete Zertifikats-Datenexport-Datei-State soll lokal verfügbar sein, aber im lokalen Modus verborgen bleiben.

Supabase bleibt weiterhin nicht live:
- keine echte Supabase-Verbindung
- keine echten Keys
- kein Login-Zwang
- keine echte Datenexport-Datei
- keine echte Datei-Erzeugung
- kein echter Download
- keine Teilnehmerdaten
- kein UI-Blocker

## Browser-Test

Konsole:

window.ACCAOUI_SUPABASE_ADAPTER.getParticipantDashboardCertificateDataExportFileState()

## Erwartetes Ergebnis

version: "v26.79a"
status: "local_dashboard_certificate_data_export_file_hidden"
isVisible: false
canRender: false
canLoadCertificateDataExportFile: false
canPrepareCertificateDataExportFile: false
canGenerateCertificateDataExportFile: false
canDownloadCertificateDataExportFile: false
canRefreshCertificateDataExportFile: false
isLocalDashboardAccessAllowed: true

## Geplante spätere Datenexport-Datei-Aktionen

- certificate_data_export_file_prepare_later
- certificate_data_export_file_generate_later
- certificate_data_export_file_download_later
- certificate_data_export_file_expiry_later

## Testergebnis

Bestanden.

Der Zertifikats-Datenexport-Datei-State ist vorhanden, lokal verborgen und blockiert das Teilnehmer-Dashboard nicht.

## Bewertung

Der State ist nur vorbereitet. Es findet keine echte Datenexport-Datei-Erzeugung, kein echter Download, keine Teilnehmerdaten-Verarbeitung und keine Supabase-Kommunikation statt.

Status: erledigt
