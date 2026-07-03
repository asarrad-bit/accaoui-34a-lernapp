# Supabase Participant Dashboard Certificate Consent State Test

Stand: v26.72b
Bereich: Teilnehmer-Dashboard-Zertifikats-Einwilligungs-State
Datei: data/supabase-client-adapter.js

## Ziel

Der vorbereitete Zertifikats-Einwilligungs-State soll lokal verfügbar sein, aber im lokalen Modus verborgen bleiben.

Supabase bleibt weiterhin nicht live:
- keine echte Supabase-Verbindung
- keine echten Keys
- kein Login-Zwang
- keine echte Einwilligung
- keine Teilnehmerdaten
- keine Freigabe
- keine Einwilligungs-Abfrage
- kein UI-Blocker

## Browser-Test

Konsole:

window.ACCAOUI_SUPABASE_ADAPTER.getParticipantDashboardCertificateConsentState()

## Erwartetes Ergebnis

version: "v26.72a"
status: "local_dashboard_certificate_consent_hidden"
isVisible: false
canRender: false
canLoadCertificateConsent: false
canGrantCertificateConsent: false
canRevokeCertificateConsent: false
canRefreshCertificateConsent: false
isLocalDashboardAccessAllowed: true

## Geplante spätere Einwilligungs-Bereiche

- certificate_display_later
- certificate_download_later
- certificate_share_later
- certificate_online_verification_later

## Testergebnis

Bestanden.

Der Zertifikats-Einwilligungs-State ist vorhanden, lokal verborgen und blockiert das Teilnehmer-Dashboard nicht.

## Bewertung

Der State ist nur vorbereitet. Es findet keine echte Einwilligung, keine Teilnehmerdaten-Verarbeitung, keine Freigabe, keine Einwilligungs-Abfrage und keine Supabase-Kommunikation statt.

Status: erledigt
