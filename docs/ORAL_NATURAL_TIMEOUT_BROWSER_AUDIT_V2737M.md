# v27.37m – Natürlicher mündlicher 15-Minuten-Abschluss

Basis-Commit: 0f6f8a2c26998abf094315996b83d28fb4f9818a
Gate-Commit: b566460c44329bee63e5f6c6b4c0e8bd5623d710
Test-Origin: http://127.0.0.1:64398
Testdatum: 2026-10-06
Browser: Codex In-app Chromium, Chrome 154.0.0.0, Windows 10 x64
Start-UTC: 2026-10-06T21:29:25.557Z
Null-UTC: 2026-10-06T21:44:25.579Z
Reale-Sekunden: 900.007
Zeitmanipulation: NEIN
Manueller Abschluss: NEIN
Keine Produktänderung.
Supabase NICHT LIVE.

## Testumgebung

Der zuvor vollständig geprüfte Autorisierungs-Gate-Commit war bereits auf main gepusht. Die unveränderte App wurde mit einem temporären HTTP-Server ausschließlich an 127.0.0.1 auf dem neuen Port 64398 bedient. Vor dem ersten App-Aufruf auf einer statischen Seite desselben Origins: localStorage 0 Schlüssel, sessionStorage 0 Schlüssel, Cookies 0, IndexedDB []. Keine echten Teilnehmerdaten oder Schlüssel. Beide Supabase-Browser-Loader hatten data-enabled=false; die optionale lokale Konfiguration fehlte.

Der browser-act-Skill wurde verwendet. Weil browser-act und uv lokal nicht verfügbar waren, erfolgte der reale Audit mit dem bereits vorhandenen integrierten Chromium-Browser, ohne Installation. Kein synthetischer DOM-Harness wurde als Browsernachweis ausgegeben.

Start und Bewertungen erfolgten ausschließlich über vorhandene UI-Buttons: Mündliche Prüfung, Modusauswahl, Prüfungsbogen A, erste Musterantwort/Sicher beantwortet, zweite Musterantwort/Noch üben. Anschließend blieb Frage 3/15 bis zum Timeout offen. Nur zwei von 15 Fragen wurden bewertet; keine vollständige Bewertungsfolge und keine manuelle Abschlussfunktion wurden ausgeführt.

## Zeitprotokoll

Die bestehenden Timer-, Date- und performance-Funktionen sowie App-Funktionen und App-Zustandsvariablen wurden nicht ersetzt oder verändert. Ein eigener passiver DOM-MutationObserver zeichnete tatsächlich hinzugefügte Timertexte mitsamt UTC und performance.now() auf. Er steuerte weder Countdown noch Navigation oder Storage. Eigene passive error-/unhandledrejection-Listener unterdrückten keine Ausnahme. Die Aufzeichnung begann vor dem Startbutton.

Alle 901 Zustände sind tatsächlich aufgezeichnet: 15:00, dann jeder einzelne Sekundenwert exakt einmal und streng absteigend bis 00:00. Kein fehlender Wert, Sprung oder Reset. Die Nullanzeige wurde als reale DOM-Mutation erfasst, bevor die Ergebnisansicht den Timer im selben Timeoutablauf ersetzte; sie ist keine nachträglich berechnete oder injizierte Anzeige.

Monotone Messwerte: Start 140399.59999996424 ms, Null 1040406.3000000119 ms; Differenz 900.0067000000477 Sekunden. UTC-Differenz 900.022 Sekunden. Der automatische Ergebnis-DOM wurde um 2026-10-06T21:44:25.580Z hinzugefügt, unmittelbar nach der Nullmutation.

| Timerstand | Aufgezeichnete UTC |
| --- | --- |
| 15:00 | 2026-10-06T21:29:25.557Z |
| 14:00 | 2026-10-06T21:30:25.567Z |
| 13:00 | 2026-10-06T21:31:25.573Z |
| 12:00 | 2026-10-06T21:32:25.573Z |
| 11:00 | 2026-10-06T21:33:25.572Z |
| 10:00 | 2026-10-06T21:34:25.577Z |
| 09:00 | 2026-10-06T21:35:25.577Z |
| 08:00 | 2026-10-06T21:36:25.567Z |
| 07:00 | 2026-10-06T21:37:25.575Z |
| 06:00 | 2026-10-06T21:38:25.569Z |
| 05:00 | 2026-10-06T21:39:25.570Z |
| 04:00 | 2026-10-06T21:40:25.582Z |
| 03:00 | 2026-10-06T21:41:25.583Z |
| 02:00 | 2026-10-06T21:42:25.584Z |
| 01:00 | 2026-10-06T21:43:25.583Z |
| 00:00 | 2026-10-06T21:44:25.579Z |

Die vollständige Rohaufzeichnung wurde vor dem Reload außerhalb des Repositorys gesichert. SHA-256 von timer-trace.json: e6312c8d7f5b2f1f18ec362fdb40a402e2198fe8d713efdb4a099b010c1e99f7. Lokaler Belegordner: C:\Users\asarr\AppData\Local\Temp\accaoui-v2737m-evidence-gQYa0k. Er enthält Timer-Rohdaten, native Ereignisse, End-/Reloadzustand und echte Screenshots. Diese temporären Belege sind keine zusätzlichen versionierten Audit- oder Gate-Dateien.

## Prüffälle

| ID | Erwartung | Tatsächliche Beobachtung | Ergebnis |
| --- | --- | --- | --- |
| T01 | Echter vorgesehener Start mit 15 Minuten. | Prüfungsbogen A per UI gestartet; tatsächlich sichtbare 15:00 und Frage 1/15 um 21:29:25.557 UTC. | PASS |
| T02 | Countdown läuft ohne Beschleunigung natürlich herunter. | 901 reale DOM-Timerstände; jeder Sekundenwert von 900 bis 0, monotone Dauer 900.007 Sekunden. | PASS |
| T03 | Keine unerwartete Verlängerung oder Zurücksetzung. | Alle 901 Werte streng um eine Sekunde absteigend; auch Reveal und zwei Bewertungen setzten die Zeit nicht zurück. | PASS |
| T04 | Natürlicher Countdown erreicht tatsächlich 00:00. | Nullmutation um 21:44:25.579 UTC im echten Browser erfasst, vor Entfernung des Timers durch die Ergebnisansicht. | PASS |
| T05 | Vorgesehener Timeout löst automatisch den Abschluss aus. | Ergebnis-DOM um 21:44:25.580 UTC; Hinweis Die 15 Minuten sind abgelaufen; keine manuelle Abschlussaktion. | PASS |
| T06 | Ergebnisansicht passt zur Runde und zu den bestehenden Zählern. | Trainingsrunde abgeschlossen, Bezug Prüfungsbogen A, 15 Fragen, 1 sicher, 1 Noch üben, vorhandene Bestandsanzeige 7 Prozent. | PASS |
| T07 | Kein doppelter automatischer Abschluss. | Genau eine Ergebnis-DOM-Einfügung; um 21:46:16.871 UTC weiterhin 901 Timerstände, eine Ergebnisansicht und keine weitere Fertigstellung. | PASS |
| T08 | Keine doppelte Verbuchung oder nachträgliche Fehlererzeugung. | Vor/nach Timeout und nach Reload gleicher einziger Fehler oral_a_002; History und aktive Sitzung nicht angelegt; Storage byte-identisch. | PASS |
| T09 | Abgeschlossene Prüfung wird nicht fälschlich fortgesetzt. | Nach Timeout keine Timer-/Frageansicht; echter Reload führt zum Dashboard mit Neue Prüfung starten, ohne Fortsetzen und ohne mündlichen Timer. | PASS |
| T10 | Keine uncaught App-Ausnahme im vollständig protokollierten Ablauf. | 0 Runtime.exceptionThrown und 0 passive App-Fehler; alle CDP-Abschnitte ohne truncation, nur Info/Log und erklärbare lokale Netzwerk-404. | PASS |
| T11 | Storage und Prüfungszustand sind nach Timeout konsistent. | Index 2, sicher 1, Noch üben 1, Gesamt 15; ein unveränderter bekannter Fehler, sessionStorage leer, kein aktiver Versuch und keine neuen Keys beim Timeout. | PASS |

## Endzustand

Die vorhandene generische Abschlussansicht lautet Trainingsrunde abgeschlossen und nennt ausdrücklich 15-Minuten-Simulation · Prüfungsbogen A. Die sichtbaren Zähler entsprechen genau den zwei UI-Bewertungen: total 15, sicher 1, Noch üben 1. Die bestehende Prozentformel des realen finish-Screens ist Math.round(known / total * 100); daher 7 Prozent, nicht eine neu eingeführte Bewertung bezogen auf nur zwei bearbeitete Fragen. Die 13 übrigen Fragen wurden nicht automatisch als sicher oder als neue gespeicherte Fehler verbucht. Dies ist keine neue Abnahme oder Änderung einer Prüferblock-/Teilpunktebewertung.

Nach dem Timeout: Timer-DOM 0, Ergebniswrapper 1, Frageindex unverändert 2. Es blieb über 110 Sekunden bei genau einer Fertigstellung. Keine zusätzliche Interaktion löste den Timeout aus. Das Klicken der bereits abgeschlossenen Überschrift diente nur dem Scrollen für den Nachweis-Screenshot; es startete keine neue Runde.

Nach echtem Reload um 21:50:38.873 UTC: Dashboard, kein Fortsetzen, kein mündlicher Timer, keine aktive Sitzung. Der mündliche Fehler blieb byte-identisch gespeichert. Die rein beobachtende Instrumentierung war durch den Reload vollständig entfernt.

## Console und Storage

Runtime, Log und Network wurden auf einer statischen Seite des neuen Origins aktiviert, bevor die App erstmals geladen wurde. Ereignisse wurden mit fortgeschriebenen Cursors während des Ablaufs gelesen und gespeichert; hasMore wurde vollständig abgearbeitet. Kein Leeren von Console oder Ereignispuffer. Bis zum Ablauf und stabilen Ergebnis waren 48 relevante native Ereignisse gesichert; einschließlich Reload und Bereinigung 97, finaler Cursor 396, truncated=false. Der Timertrace blieb zusätzlich unabhängig vom begrenzten CDP-Puffer vollständig im eigenen Speicher und wurde vor dem Reload als Rohdatei gesichert.

Insgesamt 0 Runtime-Ausnahmen. Die 24 Console-Aufrufe waren ausschließlich 14 info und 10 log, keine error/warning/assert-Aufrufe. Separate Netzwerk-Logeinträge: favicon.ico 404 auf der statischen Vorbereitung und die absichtlich fehlende optionale data/supabase-config.local.js 404 beim Appstart sowie beim Reload. Keine uncaught App-Ausnahme und kein produktiver Netzwerkzugriff: sämtliche aufgezeichneten Request-Origins waren ausschließlich der Test-Origin.

Einziger localStorage-Key nach den Bewertungen: accaoui_oral_exam_mistakes_v2324, genau ein Eintrag mit key/id oral_a_002, sheetId oral_sheet_a_v2340, sheetTitle Prüfungsbogen A, savedAt 2026-10-06T21:29:44.079Z. Der vollständige String blieb beim Timeout und beim Reload unverändert. sessionStorage leer; accaoui_exam_history und accaoui_active_session nicht vorhanden. Keine Zusatz-Keys beim Ablauf.

Erst nach vollständiger Sicherung des End-/Reloadbefunds wurde die App auf die statische Seite desselben Origins verlassen. Mit exakter Identitäts-/Wertprüfung wurde ausschließlich der eigene synthetische Fehler-Key entfernt; keine fremden Daten. Danach localStorage 0, sessionStorage 0, Cookies 0, IndexedDB []. Audittab geschlossen, selbst gestarteter Testserver PID 26468 beendet, kein Listener mehr auf Port 64398.

## Grenzen und Befunde

Ein eigener Setup-Leseausdruck in der schreibgeschützten Playwright-Ansicht auf der statischen Vorbereitungsseite scheiterte vor dem ersten App-Aufruf mit TypeError: Cannot read properties of undefined (reading 'length'). Der Aufruf meldete unerwartet 9657.6534 Sekunden Tool-Laufzeit. Zu diesem Zeitpunkt lief weder App noch Prüfung. Der reine Lesezugriff wurde über die dokumentierte CDP-Schnittstelle korrigiert, nicht durch Änderung der App. Dies ist kein Produktfehler und kein bestandener Produkttest.

Der Audit belegt genau den natürlichen Timeout von Prüfungsbogen A in diesem Chromium-Ablauf. Er behauptet keinen natürlichen 120-Minuten-Abschluss, keine Wiederholung für alle anderen mündlichen Bögen, keine physischen Mobilgeräte und keine Neubewertung sämtlicher Scoring-/Prüferblockfunktionen. Eine manuelle Abgabe oder ein synthetisch beschleunigter Countdown wurde nicht als Ersatz verwendet.

Der historische v27.37k-Bericht bleibt byte-identisch und historisch korrekt mit Gesamtfazit FAIL sowie seinem damaligen NOT VERIFIED für den natürlichen 15-Minuten-Pfad. Dieser spätere Nachweis wird ausschließlich hier dokumentiert. F01 wurde separat in v27.37l behoben; keine rückwirkende Umdeutung des alten Audits.

Versionierter Audit-Scope: ausschließlich docs/ORAL_NATURAL_TIMEOUT_BROWSER_AUDIT_V2737M.md. app.js, patch-v21.js, oral-exam.js, HTML/CSS, Testkopien, Fragenbanken, oral-sheets*, Herkunftsbezeichnungen, Auth/Session/Zugang, Config, SDK, SQL und Migrationen unverändert.

## Gesamtfazit

Audit-Gesamtfazit: PASS

11 Pflichtfälle PASS, 0 FAIL, 0 NOT VERIFIED. Echter UI-Start, natürliche vollständige 15 Minuten, tatsächliche Nullmutation, automatische einmalige Abschlussansicht, konsistente bestehende Zähler und unveränderter Storage sind nachgewiesen. Die technischen Lifecycle-/Preflight-Prüfungen bleiben hiervon getrennt und müssen vor und nach jedem vorgesehenen Commit vollständig ausgeführt werden.
