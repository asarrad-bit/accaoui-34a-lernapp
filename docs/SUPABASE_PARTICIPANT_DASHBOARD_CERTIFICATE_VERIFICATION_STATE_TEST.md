# Supabase Participant Dashboard Certificate Verification State Test

Stand: v26.67b
Bereich: Teilnehmer-Dashboard-Zertifikats-Verifizierungs-State
Datei: data/supabase-client-adapter.js

## Ziel

Der vorbereitete Zertifikats-Verifizierungs-State soll lokal verfügbar sein, aber im lokalen Modus verborgen bleiben.

Supabase bleibt weiterhin nicht live:
- keine echte Supabase-Verbindung
- keine echten Keys
- kein Login-Zwang
- kein QR-Code
- keine Prüfseite
- keine Online-Verifizierung
- kein UI-Blocker

## Browser-Test

Konsole:

window.ACCAOUI_SUPABASE_ADAPTER.getParticipantDashboardCertificateVerificationState()

## Erwartetes Ergebnis

version: "v26.67a"
status: "local_dashboard_certificate_verification_hidden"
isVisible: false
canRender: false
canLoadCertificateVerification: false
canCreateCertificateVerificationCode: false
canCopyCertificateVerificationCode: false
canOpenCertificateVerificationPage: false
canVerifyCertificateOnline: false
isLocalDashboardAccessAllowed: true

## Testergebnis

Bestanden.

Der Zertifikats-Verifizierungs-State ist vorhanden, lokal verborgen und blockiert das Teilnehmer-Dashboard nicht.

## Bewertung

Der State ist nur vorbereitet. Es findet keine echte QR-Code-Erstellung, keine Prüfseitenöffnung, keine Online-Verifizierung und keine Supabase-Kommunikation statt.

Status: erledigt
