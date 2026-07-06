# Supabase Participant Dashboard Certificate Data Export Retry State Test

Stand: v26.83b
Bereich: Teilnehmer-Dashboard-Zertifikats-Datenexport-Wiederholung-State
Datei: data/supabase-client-adapter.js

## Ziel

Der vorbereitete Zertifikats-Datenexport-Wiederholung-State soll lokal verfügbar sein, aber im lokalen Modus verborgen bleiben.

Supabase bleibt weiterhin nicht live:
- keine echte Supabase-Verbindung
- keine echten Keys
- kein Login-Zwang
- keine echte Wiederholungsanfrage
- keine echte Wiederholungsausführung
- keine echte Fehlerbehebung
- keine Teilnehmerdaten
- kein UI-Blocker

## Browser-Test

Konsole:

window.ACCAOUI_SUPABASE_ADAPTER.getParticipantDashboardCertificateDataExportRetryState()

## Erwartetes Ergebnis

version: "v26.83a"
status: "local_dashboard_certificate_data_export_retry_hidden"
isVisible: false
canRender: false
canLoadCertificateDataExportRetry: false
canRequestCertificateDataExportRetry: false
canResolveCertificateDataExportRetry: false
canRefreshCertificateDataExportRetry: false
isLocalDashboardAccessAllowed: true

## Geplante spätere Datenexport-Wiederholung-Aktionen

- certificate_data_export_retry_request_later
- certificate_data_export_retry_resolve_later
- certificate_data_export_retry_refresh_later

## Testergebnis

Bestanden.

Der Zertifikats-Datenexport-Wiederholung-State ist vorhanden, lokal verborgen und blockiert das Teilnehmer-Dashboard nicht.

## Bewertung

Der State ist nur vorbereitet. Es findet keine echte Wiederholungsanfrage, keine echte Wiederholungsausführung, keine echte Fehlerbehebung, keine Teilnehmerdaten-Verarbeitung und keine Supabase-Kommunikation statt.

Status: erledigt
