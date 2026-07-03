# Supabase Participant Dashboard Certificate Share State Test

Stand: v26.66b
Bereich: Teilnehmer-Dashboard-Zertifikats-Teilen-State
Datei: data/supabase-client-adapter.js

## Ziel

Der vorbereitete Zertifikats-Teilen-State soll lokal verfügbar sein, aber im lokalen Modus verborgen bleiben.

Supabase bleibt weiterhin nicht live:
- keine echte Supabase-Verbindung
- keine echten Keys
- kein Login-Zwang
- kein Teilen-Link
- keine Teilen-E-Mail
- kein UI-Blocker

## Browser-Test

Konsole:

window.ACCAOUI_SUPABASE_ADAPTER.getParticipantDashboardCertificateShareState()

## Erwartetes Ergebnis

version: "v26.66a"
status: "local_dashboard_certificate_share_hidden"
isVisible: false
canRender: false
canLoadCertificateShare: false
canCreateCertificateShareLink: false
canCopyCertificateShareLink: false
canSendCertificateShareEmail: false
canRevokeCertificateShareLink: false
isLocalDashboardAccessAllowed: true

## Testergebnis

Bestanden.

Der Zertifikats-Teilen-State ist vorhanden, lokal verborgen und blockiert das Teilnehmer-Dashboard nicht.

## Bewertung

Der State ist nur vorbereitet. Es findet kein echtes Teilen, keine Link-Erstellung, kein E-Mail-Versand und keine Supabase-Kommunikation statt.

Status: erledigt
