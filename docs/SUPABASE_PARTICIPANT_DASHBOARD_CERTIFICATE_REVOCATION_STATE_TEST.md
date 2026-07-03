# Supabase Participant Dashboard Certificate Revocation State Test

Stand: v26.70b
Bereich: Teilnehmer-Dashboard-Zertifikats-Widerrufs-State
Datei: data/supabase-client-adapter.js

## Ziel

Der vorbereitete Zertifikats-Widerrufs-State soll lokal verfügbar sein, aber im lokalen Modus verborgen bleiben.

Supabase bleibt weiterhin nicht live:
- keine echte Supabase-Verbindung
- keine echten Keys
- kein Login-Zwang
- kein echter Widerruf
- keine Widerrufsbestätigung
- kein Widerrufsgrund
- keine Widerrufs-Anzeige
- kein UI-Blocker

## Browser-Test

Konsole:

window.ACCAOUI_SUPABASE_ADAPTER.getParticipantDashboardCertificateRevocationState()

## Erwartetes Ergebnis

version: "v26.70a"
status: "local_dashboard_certificate_revocation_hidden"
isVisible: false
canRender: false
canLoadCertificateRevocation: false
canRequestCertificateRevocation: false
canConfirmCertificateRevocation: false
canCancelCertificateRevocation: false
canShowCertificateRevokedNotice: false
isLocalDashboardAccessAllowed: true

## Testergebnis

Bestanden.

Der Zertifikats-Widerrufs-State ist vorhanden, lokal verborgen und blockiert das Teilnehmer-Dashboard nicht.

## Bewertung

Der State ist nur vorbereitet. Es findet kein echter Widerruf, keine Widerrufsbestätigung, keine Widerrufsgrund-Anzeige und keine Supabase-Kommunikation statt.

Status: erledigt
