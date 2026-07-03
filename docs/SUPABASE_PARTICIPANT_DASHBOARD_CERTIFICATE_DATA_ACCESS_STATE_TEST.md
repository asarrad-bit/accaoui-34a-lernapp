# Supabase Participant Dashboard Certificate Data Access State Test

Stand: v26.75b
Bereich: Teilnehmer-Dashboard-Zertifikats-Datenauskunft-State
Datei: data/supabase-client-adapter.js

## Ziel

Der vorbereitete Zertifikats-Datenauskunft-State soll lokal verfügbar sein, aber im lokalen Modus verborgen bleiben.

Supabase bleibt weiterhin nicht live:
- keine echte Supabase-Verbindung
- keine echten Keys
- kein Login-Zwang
- keine echte Datenauskunft
- kein echter Datenexport
- kein echter Download
- keine Teilnehmerdaten
- kein UI-Blocker

## Browser-Test

Konsole:

window.ACCAOUI_SUPABASE_ADAPTER.getParticipantDashboardCertificateDataAccessState()

## Erwartetes Ergebnis

version: "v26.75a"
status: "local_dashboard_certificate_data_access_hidden"
isVisible: false
canRender: false
canLoadCertificateDataAccess: false
canRequestCertificateDataAccess: false
canPrepareCertificateDataExport: false
canDownloadCertificateDataExport: false
canRefreshCertificateDataAccess: false
isLocalDashboardAccessAllowed: true

## Geplante spätere Datenauskunft-Aktionen

- certificate_data_access_request_later
- certificate_data_export_prepare_later
- certificate_data_export_download_later
- certificate_data_export_expiry_later

## Testergebnis

Bestanden.

Der Zertifikats-Datenauskunft-State ist vorhanden, lokal verborgen und blockiert das Teilnehmer-Dashboard nicht.

## Bewertung

Der State ist nur vorbereitet. Es findet keine echte Datenauskunft, kein echter Datenexport, kein echter Download, keine Teilnehmerdaten-Verarbeitung und keine Supabase-Kommunikation statt.

Status: erledigt
