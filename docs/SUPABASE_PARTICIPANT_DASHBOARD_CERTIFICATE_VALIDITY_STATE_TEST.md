# Supabase Participant Dashboard Certificate Validity State Test

Stand: v26.69b
Bereich: Teilnehmer-Dashboard-Zertifikats-Gültigkeits-State
Datei: data/supabase-client-adapter.js

## Ziel

Der vorbereitete Zertifikats-Gültigkeits-State soll lokal verfügbar sein, aber im lokalen Modus verborgen bleiben.

Supabase bleibt weiterhin nicht live:
- keine echte Supabase-Verbindung
- keine echten Keys
- kein Login-Zwang
- keine echte Gültigkeitsprüfung
- keine Abgelaufen-Prüfung
- keine Widerrufsprüfung
- keine Badge-Anzeige
- kein UI-Blocker

## Browser-Test

Konsole:

window.ACCAOUI_SUPABASE_ADAPTER.getParticipantDashboardCertificateValidityState()

## Erwartetes Ergebnis

version: "v26.69a"
status: "local_dashboard_certificate_validity_hidden"
isVisible: false
canRender: false
canLoadCertificateValidity: false
canCheckCertificateValidity: false
canRefreshCertificateValidity: false
canShowCertificateValidBadge: false
canShowCertificateExpiredBadge: false
canShowCertificateRevokedBadge: false
isLocalDashboardAccessAllowed: true

## Testergebnis

Bestanden.

Der Zertifikats-Gültigkeits-State ist vorhanden, lokal verborgen und blockiert das Teilnehmer-Dashboard nicht.

## Bewertung

Der State ist nur vorbereitet. Es findet keine echte Gültigkeitsprüfung, keine Ablaufprüfung, keine Widerrufsprüfung, keine Badge-Anzeige und keine Supabase-Kommunikation statt.

Status: erledigt
