# Supabase Participant Dashboard Certificate QR Code State Test

Stand: v26.68b
Bereich: Teilnehmer-Dashboard-Zertifikats-QR-Code-State
Datei: data/supabase-client-adapter.js

## Ziel

Der vorbereitete Zertifikats-QR-Code-State soll lokal verfügbar sein, aber im lokalen Modus verborgen bleiben.

Supabase bleibt weiterhin nicht live:
- keine echte Supabase-Verbindung
- keine echten Keys
- kein Login-Zwang
- kein QR-Code
- kein QR-Code-Bild
- kein QR-Code-Download
- kein QR-Code-Druck
- kein UI-Blocker

## Browser-Test

Konsole:

window.ACCAOUI_SUPABASE_ADAPTER.getParticipantDashboardCertificateQrCodeState()

## Erwartetes Ergebnis

version: "v26.68a"
status: "local_dashboard_certificate_qr_code_hidden"
isVisible: false
canRender: false
canLoadCertificateQrCode: false
canCreateCertificateQrCode: false
canRenderCertificateQrCodeImage: false
canDownloadCertificateQrCode: false
canPrintCertificateQrCode: false
isLocalDashboardAccessAllowed: true

## Testergebnis

Bestanden.

Der Zertifikats-QR-Code-State ist vorhanden, lokal verborgen und blockiert das Teilnehmer-Dashboard nicht.

## Bewertung

Der State ist nur vorbereitet. Es findet keine echte QR-Code-Erstellung, keine QR-Bildanzeige, kein Download, kein Druck und keine Supabase-Kommunikation statt.

Status: erledigt
