# W06 – Materialien, Trainingsnachweise, Exporte und lokale Mitteilungen

Status: sämtliche lokalen Funktionsfälle tatsächlich qualifiziert; vollständige ursprüngliche Abschlussgates und reguläre Publikation stehen noch aus. Abnahme ausschließlich im persönlich genehmigten isolierten synthetischen lokalen Entwicklungsumfang.

## Verhalten

Die bestehende Root-App nutzt den bereits gelieferten SDK-Client und echte Sitzungs-/Kurs-/Teilnahmeprüfung. Zugeordnete aktive Dozenten/Admins verwalten Material und lokale Mitteilungen; ausschließlich zugeordnete Admins stellen synthetische Trainingsbestätigungen aus oder widerrufen sie. Support erhält keinen pauschalen Zugriff. Teilnehmer sehen nur ihre berechtigten Dokumente, Zielmitteilungen und eigenen Quittungen. Jede Serveraktion prüft aktuelle Sitzung, Rolle, Kurs, Enrollment, Status und Ablauf; auch noch nicht abgelaufene alte JWTs sind nach Logout gesperrt.

Ausstellungsinhalt und SHA256 bleiben unverändert. QR-Verweise erfordern einen berechtigten lokalen Kontozugang und prüfen den aktuellen Status. Vor Vorschau/Druck/HTML-Download wird der Serverstand erneut gelesen; Widerruf/Ablauf schließen spätere gültige Ausgaben. Bereits gespeicherte lokale Dateien werden nicht gelöscht. Die Dokumente tragen ausdrücklich die Kennzeichnung synthetischer Trainingsbestätigungen und behaupten keine amtliche Prüfung oder Qualifikation.

CAS-Versionen, idempotente Vorgänge und getrennte owner/course-Caches erhalten Eingaben bei Konflikten, verlorenen Antworten und Netzunterbrechung. Wiederherstellung erzeugt eine neue Speicherung und bewahrt beschädigte Altbytes. Eigene Archive erhalten frühere Entwürfe/Vorgänge. Fremde Caches werden weder angezeigt noch exportiert; offene Eingaben verhindern unbemerkte Konto-/Kurswechsel. Native Storage-Implementierungen und ursprünglicher anonymer Lernbestand bleiben unverändert.

## Tatsächliche Validierung

| Ebene | Fälle | Nachweis |
| --- | ---: | --- |
| Reine Modelle/DTOs |66|36Material+30Dokument/Inbox; SDK-Antworten ausdrücklich Fakes |
| Echter privater SDK/Auth/DB-Zugriff |67|32Material+35Dokument/Inbox; keine erfundenen Antworten |
| Tatsächliche Root-App/Browserführung |32|652echte interne HTTP-Antworten, getrennte Clients/Sitzungen |
| Tatsächliche QR-Ausgaben |3|Vorschau, nativer HTML-Download und native Druckansicht erneut unabhängig aus PNG-Pixeln dekodiert |
| Autoritäts-/Schutzregeln |256|210alte+46neue Fälle;609Dateipins und unveränderter Index |

Geprüft sind native Downloads/Quittungen, sichere Inhalte/CSV-Formeln, tatsächliche Rollen-/Konto-/Empfängerisolation, native UI-Druckfensteraktion/PDF-beforeprint, lokale Lesebestätigungen, Exporte, aktuelle Kurs-/Rollenänderungen, echte CAS-Konflikte, Wiederverbindung/verlorene Antwort, Widerruf, echte Ablaufzeit, beschädigte/fremde Caches, Kontowechsel, Erhalt anonymer Daten und390px/Desktopsicht mit Tastatur/Labels/Überlauf. Korrigiert wurden eine konkret reproduzierte leere Vorschaufläche und während Ladephasen noch klickbare Aktionen; alte Fehlversuche sind vollständig erhalten. Der endgültige Mobil-Schließen-Text ist nativ einzeilig bei99x44px.

Hauptnachweis: `C:\Users\asarr\.codex\visualizations\2026\10\08\01a11cc6-ee66-7890-9520-7fd190f6e687\development-sequence-20261021-v1\W06\execution-20261030-v1\FINAL_FUNCTIONAL_INDEPENDENT_READBACK_02.json`; 184172Bytes/SHA25615c522158b9d9da9b1bb8dee5de74d0727a2230dcca35153bb12f5cc88110032.
Material: `C:\Users\asarr\.codex\visualizations\2026\10\08\01a11cc6-ee66-7890-9520-7fd190f6e687\development-sequence-20261021-v1\W06\execution-20261030-v1\backend-01\MATERIAL_CORE_INDEPENDENT_READBACK.json`.
Dokumente/Inbox: `C:\Users\asarr\.codex\visualizations\2026\10\08\01a11cc6-ee66-7890-9520-7fd190f6e687\development-sequence-20261021-v1\W06\execution-20261030-v1\documents-01\DOCUMENT_INBOX_INDEPENDENT_READBACK.json`.
Browser/Pixel: `C:\Users\asarr\.codex\visualizations\2026\10\08\01a11cc6-ee66-7890-9520-7fd190f6e687\development-sequence-20261021-v1\W06\execution-20261030-v1\ui-10\ACTUAL_BROWSER_INDEPENDENT_READBACK.json` und `C:\Users\asarr\.codex\visualizations\2026\10\08\01a11cc6-ee66-7890-9520-7fd190f6e687\development-sequence-20261021-v1\W06\execution-20261030-v1\ui-10\INDEPENDENT_ACTUAL_QR_PIXEL_READBACK.json`.

Die vorhandene private Umgebung internal-v3 verwendet vier fest gepinnte Dienste ohne veröffentlichte Backendhostports. Browser-SDK-Anfragen wurden durch private Prozesspipes an tatsächliches internes HTTP weitergegeben; Status/Bytes/Hashes blieben erhalten. Kein direkter Browser-Backend-TCP-/physischer Geräte-/Druckernachweis, kein dekodiertes PDF-Raster und kein externer Versand. Alle eigenen synthetischen Fixtures sind bereinigt, alle19Datenbankfunktionskörper/ACLs/Views/Policies und ursprünglichen zehn Umgebungseingaben erhalten, Dienste gestoppt/Daten behalten. Die SQL wurde bereits angewandt und wird nicht erneut ausgeführt. Einzige ausdrücklich qualifizierte alte Tabellenrechteänderung: certificates RPC-only. Keine echten Teilnehmerdaten oder privaten Admin-/Signierschlüssel im Browser/Beleg.

## Abschlussgrenze

Genau17Pfade, alle zehn Produkt-/Test-/SQL-Dateien bleiben nach dem letzten tatsächlichen Funktionsnachweis unverändert. Originale Fachchecker/META/GATE_SOURCE/HISTORICAL_FUNCTION, alle36/32ursprünglichen Materialfälle und Zeitbudgets sind erhalten. Vor Commit/Push müssen alle sechs vollständigen ursprünglichen Pflichtgates auf den finalen gestagten Bytes bestehen und sämtliche30sPräfixe vollständig nachgelesen werden. Danach nur sinnvoller normaler Commit/Push mit direkter GitHub-Prüfung. Noch kein vollständigesW06-PASS/Verwaltungscommit.

W00/W01/W02/W04 und W03 im freigegebenen lokalen Entwicklungsumfang sind abgeschlossen. W05 bleibt vollständig BLOCKED_EXTERNAL trotz regulär publiziertem lokalem Teil; Eigentümerquellen/Rechte/redaktionelle Rollen-/Inhaltsintegration sind offen. Auditv27.37n STOPP / NOT VERIFIED, ausschließlich in place hashen, unversioniert/unkopiert; App-Supabase NICHT LIVE, öffentliche Live-/Init-Schalter aus. Keine neuen W01-Naturläufe, Produktion, echten Daten/Nachrichten, privaten Schlüsselübertragungen, bezahlten Dienste oder System-/Sicherheitsänderungen.
