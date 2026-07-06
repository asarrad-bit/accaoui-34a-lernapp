# Supabase Participant Dashboard Certificate Data Export Expiry State Test

Stand: v26.80b
Bereich: Teilnehmer-Dashboard-Zertifikats-Datenexport-Ablauf-State
Datei: data/supabase-client-adapter.js

## Ziel

Der vorbereitete Zertifikats-Datenexport-Ablauf-State soll lokal verfügbar sein, aber im lokalen Modus verborgen bleiben.

Supabase bleibt weiterhin nicht live:
- keine echte Supabase-Verbindung
- keine echten Keys
- kein Login-Zwang
- keine echte Ablaufprüfung
- keine echte Ablaufwarnung
- keine echte Ablaufmarkierung
- keine Teilnehmerdaten
- kein UI-Blocker

## Browser-Test

Konsole:

window.ACCAOUI_SUPABASE_ADAPTER.getParticipantDashboardCertificateDataExportExpiryState()

## Erwartetes Ergebnis

version: "v26.80a"
status: "local_dashboard_certificate_data_export_expiry_hidden"
isVisible: false
canRender: false
canLoadCertificateDataExportExpiry: false
canCheckCertificateDataExportExpiry: false
canMarkCertificateDataExportExpired: false
canRefreshCertificateDataExportExpiry: false
isLocalDashboardAccessAllowed: true

## Geplante spätere Datenexport-Ablauf-Aktionen

- certificate_data_export_expiry_check_later
- certificate_data_export_expiry_warning_later
- certificate_data_export_expired_mark_later
- certificate_data_export_expiry_refresh_later

## Testergebnis

Bestanden.

Der Zertifikats-Datenexport-Ablauf-State ist vorhanden, lokal verborgen und blockiert das Teilnehmer-Dashboard nicht.

## Bewertung

Der State ist nur vorbereitet. Es findet keine echte Ablaufprüfung, keine Ablaufwarnung, keine Ablaufmarkierung, keine Teilnehmerdaten-Verarbeitung und keine Supabase-Kommunikation statt.

Status: erledigt
