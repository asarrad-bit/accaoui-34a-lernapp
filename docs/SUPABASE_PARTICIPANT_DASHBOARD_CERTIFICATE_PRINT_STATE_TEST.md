# Supabase Participant Dashboard Certificate Print State Test

Stand: v26.65b
Bereich: Teilnehmer-Dashboard-Zertifikats-Druck-State
Datei: data/supabase-client-adapter.js

## Ziel

Der vorbereitete Zertifikats-Druck-State soll lokal verfügbar sein, aber im lokalen Modus verborgen bleiben.

Supabase bleibt weiterhin nicht live:
- keine echte Supabase-Verbindung
- keine echten Keys
- kein Login-Zwang
- kein Druck-Start
- keine Teilnehmerdaten
- kein UI-Blocker

## Browser-Test

Konsole:

window.ACCAOUI_SUPABASE_ADAPTER.getParticipantDashboardCertificatePrintState()

## Erwartetes Ergebnis

version: "v26.65a"
status: "local_dashboard_certificate_print_hidden"
isVisible: false
canRender: false
canLoadCertificatePrint: false
canOpenCertificatePrintDialog: false
canStartCertificatePrint: false
isLocalDashboardAccessAllowed: true

## Testergebnis

Bestanden.

Der Zertifikats-Druck-State ist vorhanden, lokal verborgen und blockiert das Teilnehmer-Dashboard nicht.

## Bewertung

Der State ist nur vorbereitet. Es findet kein echter Druck, kein Zertifikatsabruf und keine Supabase-Kommunikation statt.

Status: erledigt
