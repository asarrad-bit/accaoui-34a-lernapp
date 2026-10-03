# v27.37k – Browser-End-to-End-Abnahme

## Testumgebung

Basis-Commit: `84eebad64e290ff045dffd8ce6714cea44533818`
Gate-Commit: `c8bf0445feee5c23d40bdd7e1ea600abe0836c4c`
Getesteter Arbeitsstand: HEAD und frisch abgeglichenes origin/main entsprechen dem Gate-Commit; Branch main; anfangs Working Tree und Index leer.
Testdatum: 2026-10-03
Browser: Codex In-app Chromium, Chrome 154.0.0.0, Windows 10 x64
Test-Origin: `http://127.0.0.1:55484`
Viewports: Desktop 1280 × 720; Mobile 390 × 844 (Viewport-Emulation, kein physisches Gerät).
Browserzeit der beobachteten Abläufe: ungefähr 09:20–09:45 Europe/Berlin.

Die unveränderte App wurde mit einem temporären HTTP-Server ausschließlich an 127.0.0.1 auf einem freien Port bedient. Dieser neue Origin hatte vor den Lernaktionen leeren localStorage und sessionStorage, keine Cookies und keine IndexedDB-Datenbanken. Keine echten Teilnehmerdaten, Produktionsdomain oder Supabase-Schlüssel wurden verwendet. Beide Supabase-Browser-Loader blieben data-enabled=false; die optionale lokale Konfiguration war nicht vorhanden; der Bootstrap meldete lokalen Modus und deaktivierte Live-Schaltung.

Keine Produktänderung.
Supabase NICHT LIVE.

Methodik: echte gerenderte UI, Klicks auf vorhandene Buttons, echte Reloads, DOM-/Accessibility-Zustände und Screenshots an den wesentlichen Ansichten. Ergänzend wurden die tatsächlich laufende App und ihre gespeicherten Versuchsdaten lesend untersucht. Antworten wurden über die UI gewählt, nicht in Storage injiziert. Keine Funktionsersetzung, kein Stub, keine manipulierte Uhr und kein Fake-PASS. Der wiederholte Abschluss wurde zusätzlich durch zweimaligen Aufruf der unveränderten vorhandenen finishExamMode-Funktion geprüft. Der browser-act-Skill führte zur gerenderten Browser-Prüfung; weil browser-act/uv lokal nicht verfügbar waren, wurde der vorhandene integrierte Browser verwendet, ohne Installation.

Die technische Basis und der Gate-Commit sind verschiedene Lifecycle-Rollen. Geprüft wurde die Produktfassung am Gate-Commit. Der einzige autorisierte Repository-Schreibpfad dieses Audits ist dieses Dokument. Kontrolltools und Closure-Dokumente bleiben unverändert.

## Schriftliche Prüfung

| Fall | Erwartung | Beobachtung | Ergebnis |
| --- | --- | --- | --- |
| W01 | Dashboard startet ohne uncaught App-JavaScript-Error und ist bedienbar. | Reales Dashboard mehrfach geladen; Karten, Themen und Navigation funktionieren. Kein App-uncaught-Error beobachtet; die Einschränkung der vollständigen Protokollhistorie steht unter C01. | PASS |
| W02 | Bereitschaft ohne belastbare Grundlage zeigt Nicht berechnet statt erfundenem Prozentwert. | Beim leeren Test-Origin und nach den Testabläufen zeigt das Dashboard Nicht berechnet. | PASS |
| W03 | Schriftlicher und mündlicher Bereich sind über die App erreichbar. | Dashboard-Prüfungsauswahl und mündliche Übersicht über Desktop-/Mobilnavigation tatsächlich geöffnet. | PASS |
| W04 | Vollsimulation enthält genau 82 Fragen. | Neue Vollsimulationen zeigen Frage 1/82 und speichern jeweils genau 82 Fragen. | PASS |
| W05 | Vollsimulation bietet genau 120 Punkte und einen 120-Minuten-Timer. | Tatsächliche Fragenpunkte ergeben 120; Startanzeige 120:00 und Ergebnismaximum 120. | PASS |
| W06 | Pause um Frage 10, Reload und Resume behalten dieselbe Versuchs-ID und vollständige Fragen-/Antwortreihenfolge. | Versuch b7c63452-a32e-4939-90d7-f6d1d160c97e bei Index 9 pausiert; Dashboard-Resume nach Reload behält ID und sämtliche 82 Fragen einschließlich Antwortreihenfolge identisch. | PASS |
| W07 | Pause/Resume behält Position und alle bereits gewählten Antworten; kein zweiter Versuch entsteht. | Acht Antworten bei Frage 10 vorhanden; Position Index 9 und gespeicherte Antwortauswahl vor Pause und nach Resume identisch; dieselbe ID. | PASS |
| W08 | Resume setzt den Timer nicht auf 120:00 zurück. | Pausierte Restzeit 7136 Sekunden beziehungsweise 118:56 nach Reload/Resume unverändert übernommen. | PASS |
| W09 | Vollständig richtige Auswahl einer 2-Punkte-Frage mit nur einer richtigen Antwort ergibt 2/2. | uvv_008 im ersten Versuch über UI korrekt beantwortet; unveränderte App-Bewertung ergibt 2/2. | PASS |
| W10 | Nur ein Teil der richtigen Mehrfachantworten ohne falsche Auswahl erhält die vorgesehenen Teilpunkte. | straf_002 im ersten Versuch mit einer von zwei richtigen Antworten gewählt; tatsächliche App-Bewertung 1/2. | PASS |
| W11 | Richtige plus falsche Auswahl erhält keine unzulässigen Teilpunkte. | roso_005 im 60-Punkte-Versuch mit Auswahl [2,0] bewertet: 0 Punkte; Auswahl beim einfachen Abschluss erhalten. Doppelklick-Sonderfehler separat unter W14. | PASS |
| W12 | Unbeantwortete Fragen ergeben 0 Punkte und werden als unbeantwortet gezählt. | straf_001 zunächst bewusst übersprungen; App-Bewertung 0. Im ersten Endergebnis 72, im 59-Punkte-Versuch 42 unbeantwortete Fragen korrekt geführt. | PASS |
| W13 | 60/120 ist bestanden, 59/120 ist nicht bestanden. | Reale UI-Antwortfolgen erzeugen 60/120, 50%, Bestanden und 59/120, 49%, Nicht bestanden; zwei separate IDs und echte Verlaufseinträge. | PASS |
| W14 | Abschluss zeigt Ergebnis, zählt genau einmal und verändert auch bei schnellem Doppelklick keine zuvor gewählten Antworten. | Einmalige Verlaufszählung, wiederholter Abschluss und Reload bestehen. Doppelklick auf Prüfung jetzt abgeben verändert jedoch vor der Bestätigung Auswahl [2,0] zu [2]; dadurch 1 statt 0 Punkte. Reproduzierbar ohne Produktänderung. | FAIL |
| W15 | Neuer Versuch erhält neue ID, bleibt unabhängig und pausierbar; alte Historie unverändert, abgeschlossene Prüfung nicht fortsetzbar. | Neuer Versuch bae5ae45-446a-48c4-9c6c-b324ef98db9e tatsächlich pausiert/fortgesetzt; alter Verlauf identisch. Dashboard/Reload bieten keine abgeschlossene Prüfung zum Fortsetzen an. Auch nach Zusatzversuch bleiben die ersten drei Verlaufseinträge unverändert. | PASS |
| W16 | Fehleransicht und Training enthalten genau falsch beziehungsweise nicht vollständig richtig beantwortete und unbeantwortete Fragen, mit Lösungen und Erklärungen. | Erster Versuch: 75 Fehlerkarten = 3 nicht vollständig richtige + 72 unbeantwortete, keine der 7 vollständig richtigen Fragen zusätzlich; 75 Lösungen und Erklärungen. Gestartetes Fehlertraining enthält genau dieselben 75 eindeutigen Frage-IDs, zulässig neu sortiert. | PASS |

Versuchsprotokoll:

- `b7c63452-a32e-4939-90d7-f6d1d160c97e`: Pause/Resume, Teilpunkte, Fehleranalyse; tatsächliches Endergebnis 12/120, 7 richtig, 3 falsch/nicht vollständig richtig, 72 unbeantwortet. Die zuvor gewählte Mischantwort bei Frage 12 änderte sich während des Doppelklick-Abgabeablaufs von [0,2] zu [0]. Diese Beobachtung wurde im Zusatzversuch gezielt reproduziert und nicht als bestandene Mischantwortprüfung gewertet.
- `bae5ae45-446a-48c4-9c6c-b324ef98db9e`: neuer pausierbarer Versuch, Mischantwort unverändert [2,0] = 0 Punkte, einfache Abgabe, 60/120 bestanden; 41 richtig, 1 falsch, 40 unbeantwortet.
- `34fc111c-1145-400e-8f85-93bc7b8eb900`: weitere neue ID, einfache Abgabe, 59/120 nicht bestanden; 40 richtig, 0 falsch, 42 unbeantwortet; beide älteren Einträge unverändert.
- `78f22328-feff-44aa-84ac-3d682232c1ed`: gezielter Doppelklick-Zusatzversuch; Auswahländerung schon beim Öffnen der Abgabewarnung, vor Trotzdem abgeben, nachgewiesen; Endergebnis 1/120.

Die Verlaufsanzahl stieg im ersten Abschluss von 0 auf 1 und im Zusatzversuch von 3 auf 4, nie doppelt. Zweimaliges erneutes finishExamMode nach dem ersten Abschluss sowie anschließender Reload ließen den Verlauf unverändert. Der terminale Versuch blieb completed. Eine gespeicherte separate Lerneinheit erschien nach Reload als Lerneinheit fortsetzen; dies ist keine Fortsetzung einer abgeschlossenen Prüfung.

## Mündliche Prüfung

| Fall | Erwartung | Beobachtung | Ergebnis |
| --- | --- | --- | --- |
| O01 | Prüfungsbogen A startet separat mit richtigem Titel, Frage, Reveal und Bewertung. | Titel 15-Minuten-Simulation · Prüfungsbogen A; 15 Fragen, erste oral_a_001; Antwort zunächst verdeckt, Musterantwort anzeigen zeigt Antwort und Prüferhinweis; Noch üben wechselt zur nächsten Frage und speichert genau einen Fehler. | PASS |
| O02 | Prüfungsbogen B startet separat mit richtigem Titel, Frage, Reveal und Bewertung. | Titel Prüfungsbogen B innerhalb der 15-Minuten-Simulation; erste oral-b-001, 15 Fragen; tatsächliche Musterantwort sichtbar nach Reveal; Sicher beantwortet wechselt zu Frage 2/15. | PASS |
| O03 | Prüfungsbogen C startet separat mit richtigem Titel, Frage, Reveal und Bewertung. | Titel Prüfungsbogen C; erste oral-c-001, 15 Fragen; Antwort verdeckt und nach Reveal tatsächlich sichtbar; Sicher beantwortet wechselt zu Frage 2/15. | PASS |
| O04 | Prüfungsbogen D startet separat mit richtigem Titel, Frage, Reveal und Bewertung. | Titel Prüfungsbogen D; erste oral-d-001, 15 Fragen; Antwort verdeckt und nach Reveal sichtbar; Sicher beantwortet wechselt zu Frage 2/15. | PASS |
| O05 | Prüfungsbogen E startet separat mit richtigem Titel, Frage, Reveal und Bewertung. | Titel Prüfungsbogen E; erste oral-e-001, 15 Fragen; Antwort verdeckt und nach Reveal sichtbar; Sicher beantwortet wechselt zu Frage 2/15. | PASS |
| O06 | Zufallsprüfung enthält genau 15 eindeutige Fragen mit Herkunft aus A/B/C/D/E. | Tatsächliche Runde hat 15 eindeutige IDs, 15 eindeutige Texte und 15 eindeutige sourceQuestionIds; sourceSheetId/sourceSheetTitle decken alle fünf Bögen A–E ab. Alle 15 Fragen über UI aufgedeckt und bewertet. | PASS |
| O07 | 15-Minuten-Simulation startet mit Prüferdarstellung; Fragenwechsel und vorgesehene Bewertungen funktionieren. | Prüfer 1, Vorsitz und Prüfer 3 sichtbar; beim Durchlauf Rollenwechsel bei Frage 6 und 11; nach 15 sicheren Bewertungen echte Ergebnisansicht mit 15 sicher, 0 Noch üben, 100%. Dies ist manueller Abschluss, kein Timeoutnachweis. | PASS |
| O08 | Mündlicher Fehlertrainer zeigt neutral mündliche Vorbereitung, richtige Karte/Zähler, verdeckte Antwort sowie Reveal und Noch üben/Collapse. | Aus Bogen A entstand genau oral_a_001. Trainer zeigt 1 offenen Fehler und eine Karte, neutralen Herkunftstext, keinen falschen Herkunftshinweis; Antwort-CSS zunächst display:none, Reveal display:block, Noch üben wieder display:none bei unverändert einem Fehler. | PASS |
| O09 | Als sicher markieren entfernt den letzten Fehler; Storage exakt [], echter Leerzustand ohne alte Karte/Zähler, keine Zwangsnavigation und nach Reload weiterhin leer. | Letzten Fehler über UI entfernt: Key accaoui_oral_exam_mistakes_v2324 enthält exakt den String []; 0 Karten, kein alter Zähler, geforderter Leerzustand samt zwei Aktionen. URL bleibt im Trainer-Origin, kein Dashboard-Zwang. Nach Reload Storage weiterhin [], keine alte Karte; Schlüsselmenge im Trainer unverändert. | PASS |

Leerzustand unmittelbar nach letzter Entfernung: Mündliche Fehler; Keine offenen mündlichen Fehler; Alle aktuell gespeicherten mündlichen Fehler wurden bearbeitet.; Zur Fehlerübersicht; Zurück zum Dashboard. Die CSS-Großschreibung der Überschrift ändert den tatsächlichen Text nicht. Der Reload öffnet das normale Dashboard, legt aber keinen mündlichen Fehler neu an.

Für die getrennten Bögen und die Zufallsrunde wurden keine App-uncaught-Errors oder Storage-Ausnahmen beobachtet. Die Einschränkung eines lückenlosen Gesamtprotokolls wird nicht verschwiegen: siehe C01.

## Timer

| Fall | Erwartung | Beobachtung | Ergebnis |
| --- | --- | --- | --- |
| T01 | Schriftlicher Timer zählt natürlich herunter und Pause/Resume erhält seine Restzeit. | Sichtbar 120:00 zu 119:40 und 118:56; gespeicherte Restzeit beim Resume 7136 Sekunden statt Reset auf 7200. Weitere echte Versuche ebenfalls mit abnehmender Anzeige. | PASS |
| T02 | Mündlicher 15-Minuten-Timer zählt natürlich herunter. | Bogen A sichtbar 15:00 zu 14:02/14:01/13:47; Zufallsrunde 15:00 zu 14:19/13:54/13:48. Keine Uhr oder Timerfunktion verändert. | PASS |
| T03 | Natürlicher 120-Minuten-Timeout führt belastbar zum vorgesehenen vollständigen Abschluss. | Keine einzelne schriftliche Sitzung 120 Minuten natürlich bis zum Timeout laufen gelassen. Frühzeitige UI-Abgaben sind kein Nachweis des Timeoutpfads. | NOT VERIFIED |
| T04 | Natürlicher 15-Minuten-Timeout führt belastbar zum vorgesehenen vollständigen Abschluss. | Keine einzelne mündliche Sitzung natürlich bis 00:00 laufen gelassen; die 15 Bewertungen beendeten die Zufallsrunde manuell. Kein beschleunigter oder simulierter Timeout. | NOT VERIFIED |

## Responsive

Prüfung durch tatsächliches Umschalten der Browser-Viewports und Betrachten der gerenderten Ansichten. documentElement.scrollWidth überschritt die jeweilige clientWidth nicht. Desktop mit Scrollbar: 1265/1265 bei innerWidth 1280; mobile Ansichten je nach Scrollbar 375/375 oder 390/390. Vertikales Scrollen ist erforderlich und erlaubt; die Buttons wurden tatsächlich bedient und waren erreichbar. Keine wesentliche Überlagerung oder unlesbare Beschriftung beobachtet. Der Doppelklick-Reflow-Fehler betrifft die Abgabeinteraktion und ist unabhängig von dieser visuellen Beurteilung dokumentiert.

| Fall | Erwartung | Beobachtung | Ergebnis |
| --- | --- | --- | --- |
| R01-D | Dashboard bei 1280 × 720 ohne horizontalen Overflow, lesbar und navigierbar. | Gerendertes Desktop-Dashboard mit erreichbaren Karten und Sidebar; Breite innerhalb des Viewports, keine wesentliche Überlagerung. | PASS |
| R01-M | Dashboard bei 390 × 844 ohne horizontalen Overflow, lesbar und navigierbar. | Mobile Karten und feste Hauptnavigation tatsächlich sichtbar/bedient; Breite innerhalb des Viewports, Inhalte per vertikalem Scrollen erreichbar. | PASS |
| R02-D | Schriftliche Prüfung bei 1280 × 720 ohne Overflow, lesbare Fragen und erreichbare Aktionen. | Desktop-Frage, Antworten, Timer, Vor/Zurück, Pause und Abgabe bedient; scrollWidth/clientWidth 1265/1265 im Zusatzversuch. | PASS |
| R02-M | Schriftliche Prüfung bei 390 × 844 ohne Overflow, lesbare Fragen und erreichbare Aktionen. | Mobile Prüfungsansicht betrachtet und bedient; Umbruch/vertikales Scrollen ermöglichen Antworten und Navigationsbuttons ohne horizontales Ausweichen. | PASS |
| R03-D | Ergebnis bei 1280 × 720 ohne Overflow, lesbar und Aktionen erreichbar. | Schriftliche Ergebnisübersicht mit 82 Fragen, Punktebox, Themenanalyse und unteren Aktionsbuttons korrekt gerendert und bedient. | PASS |
| R03-M | Ergebnis bei 390 × 844 ohne Overflow, lesbar und Aktionen erreichbar. | Mobile Ergebnisansicht samt Themen und Aktionen geprüft; vertikales Scrollen erforderlich, keine wesentliche Überlagerung oder horizontale Überbreite. | PASS |
| R04-D | Fehleransicht bei 1280 × 720 ohne Overflow und mit bedienbarem Training. | Lösungen/Erklärungen der Fehlerkarten lesbar; Fehlertraining starten aus der tatsächlichen Ansicht bedient. | PASS |
| R04-M | Fehleransicht bei 390 × 844 ohne Overflow und mit bedienbarem Training. | Mobile Fehlerkarten und Lösungs-/Erklärungstexte umbrechen; Navigation und Trainingsaktion erreichbar. | PASS |
| R05-D | Mündliche Übersicht bei 1280 × 720 ohne Overflow; Bögen und Modi erreichbar. | Desktop-Übersicht und Auswahl A–E/Zufallsprüfung lesbar und tatsächlich bedient; keine wesentliche Überlagerung. | PASS |
| R05-M | Mündliche Übersicht bei 390 × 844 ohne Overflow; Bögen und Modi erreichbar. | Mobile Übersicht/Modusauswahl sichtbar; Mündliche Prüfung über sichtbare Mobilnavigation geöffnet und Auswahlbuttons erreichbar. | PASS |
| R06-D | Mündliche Simulation bei 1280 × 720 ohne Overflow; Timer, Prüfer und Aktionen bedienbar. | Desktop-Simulation mit Frage, Prüferdarstellung, Reveal und Bewertungen gerendert und durchlaufen; Texte/Buttons lesbar. | PASS |
| R06-M | Mündliche Simulation bei 390 × 844 ohne Overflow; Timer, Prüfer und Aktionen bedienbar. | Mobile Simulation mit scrollWidth/clientWidth 390/390; Reveal/Bewertung und Zurück-Aktion per Scrollen erreichbar, keine wesentliche Überlagerung. | PASS |
| R07-D | Fehlertrainer bei 1280 × 720 ohne Overflow; Karte, Antwort und Aktionen bedienbar. | Desktop-Fehlertrainer mit einer Karte, Zähler, neutralem Text und erreichbaren Trainingsbuttons geprüft. | PASS |
| R07-M | Fehlertrainer bei 390 × 844 ohne Overflow; Trainingsaktionen und Leerzustand lesbar. | Mobile Karte, Reveal/Collapse/Sicher bedient; anschließend echter Leerzustand mit beiden Aktionen und scrollWidth/clientWidth 390/390. | PASS |

Physische Android-/iPhone-Geräte: NOT VERIFIED. Die Mobilbefunde beziehen sich ausschließlich auf den Chromium-Viewport; keine Aussage über echte Geräte, Safari/iOS oder weitere Browser.

## Console

| Fall | Erwartung | Beobachtung | Ergebnis |
| --- | --- | --- | --- |
| C01 | Sämtliche App-uncaught-Errors, relevanten Warnungen und Storage-Fehler über den ganzen Audit werden lückenlos belegt, ohne Konsole zu leeren. | Wiederholte warn/error-Abfragen leer, keine App-uncaught- oder Storage-Ausnahme beobachtet. Lokale 404 für optionale Konfiguration und favicon vorhanden. Retrospektiver CDP-Puffer meldet truncated:true; daher kein PASS für lückenlose Gesamthistorie. | NOT VERIFIED |

Die Konsole wurde zu keinem Zeitpunkt künstlich geleert. Browser-Warnungen/Errors wurden mehrfach während der Abläufe abgefragt; die vorhandene Console-API lieferte dabei jeweils keine warn/error-Einträge. Der Netzwerk-/Runtime-Ereignispuffer wurde ebenfalls ausgelesen. Seine abschließende Abfrage ab Cursor 64 hatte cursor 1387, hasMore=false, truncated=true. Im erhaltenen Ausschnitt: sieben Netzwerk-404 für die absichtlich nicht vorhandene optionale data/supabase-config.local.js, keine Runtime.exceptionThrown-Einträge, 116 Requests ausschließlich an den Test-Origin. Der frühe Serverabschnitt zeigt außerdem favicon.ico 404. Das ist kein Nachweis einer vollständigen frühen Netzwerk-/Exception-Historie; ältere CDP-Ereignisse wurden durch die begrenzte Pufferkapazität verdrängt, nicht durch einen Aufruf zum Leeren.

Zwei fehlerhafte eigene Inspektionsausdrücke wurden als Tooling-Befunde festgehalten: ReferenceError wegen des zunächst falsch angenommenen Variablennamens examIndex sowie SyntaxError durch await außerhalb einer async-Funktion. Beide kamen aus Audit-Ausdrücken ohne App-Quell-URL, nicht aus einem Produktablauf. Die Ausdrücke wurden korrigiert, nicht die App. DOMStorage-CDP-Zugriff und direkter JSON-Tabaufruf waren mit dem vorhandenen Browser nicht unterstützt; lesender Zugriff auf den tatsächlichen App-Storage im geladenen lokalen Origin funktionierte. Ein zunächst versteckter gleichnamiger Mobilnavigationstext wurde gezielt auf das sichtbare UI-Element eingegrenzt. Keiner dieser Tooling-Befunde wurde als bestandener semantischer Produkttest verwendet.

Der letzte Ereignisabschnitt bis cursor 1420 war nicht abgeschnitten und enthielt nur die Navigation zur statischen Bereinigungsseite. Keine beobachtete Storage-Ausnahme, kein Zugriff auf einen produktiven Supabase-Origin und keine tatsächliche Supabase-Anmeldung.

## Storage

| Fall | Erwartung | Beobachtung | Ergebnis |
| --- | --- | --- | --- |
| S01 | Neuer isolierter Loopback-Origin startet ohne lokale/session Daten, relevante Cookies/IndexedDB-Altlasten oder echte Teilnehmerdaten; kein Live-Supabase. | Vor Aktionen localStorage {}, sessionStorage {}, Cookies leer, IndexedDB []; keine lokale Schlüsselkonfiguration, beide Browser-Loader deaktiviert, lokaler Bootstrap-Modus. Alle Testdaten synthetisch durch UI erzeugt. | PASS |
| S02 | Am Ende wird ausschließlich Wegwerf-Storage dieses Test-Origin bereinigt und der Testserver ordentlich beendet. | Nach App-Verlassen auf statische /data/-Seite desselben Origins localStorage und sessionStorage geleert; anschließend beide [], Cookies leer, IndexedDB []; Audittab geschlossen, Viewport zurückgesetzt, Server beendet und kein Listener auf Port 55484. | PASS |

Vor Bereinigung entstanden ausschließlich diese sieben bestehenden Keys:

- accaoui_active_learning_session
- accaoui_active_session
- accaoui_answered_questions
- accaoui_exam_history
- accaoui_oral_exam_mistakes_v2324
- accaoui_topic_mistakes
- accaoui_topic_stats

Der mündliche Fehlertrainer veränderte die Schlüsselmenge nicht. Der letzte mündliche Fehler war schon vor der abschließenden Testbereinigung exakt [] und blieb nach Reload leer. Die Bereinigung erfolgte erst auf einer skriptfreien Seite desselben Origins, damit App-Pagehide/Autosave keine Testdaten wiederherstellt. Andere Browser-Origins, reale Teilnehmerdaten, Repository-Stashes und Patch-Sicherungen wurden nicht bereinigt oder verändert. Nur synthetische Wegwerf-Testdaten wurden entfernt.

## Reproduzierbare Fehler

### F01 – Doppelklick auf schriftliche Abgabe verändert Antwort vor der Bestätigung

Betroffener Fall: W14. Basis der Reproduktion: unveränderter Gate-Arbeitsstand, Desktop 1280 × 720, isolierter Test-Origin.

1. Neue Vollsimulation über Dashboard und Vollsimulation starten.
2. Bei einer Mehrfachantwort eine richtige und eine falsche Option wählen; mindestens eine andere Frage unbeantwortet lassen.
3. Schnellen Doppelklick auf Prüfung jetzt abgeben ausführen.
4. Bereits nach Einblenden der Warnung, noch vor Trotzdem abgeben, gespeicherte Auswahl mit dem unmittelbar zuvor gelesenen Zustand vergleichen.
5. Danach abgeben und Ergebnis/Verlauf prüfen.

Gezielte Reproduktion im Versuch 78f22328-feff-44aa-84ac-3d682232c1ed, erste Frage v23_gewo_007, zwei richtige Optionen [2,3]: Über die UI wurden richtige Option 2 und falsche Option 0 gewählt. Unmittelbar davor gespeicherte answers[0]=[2,0]. Unmittelbar nach dem Doppelklick und vor Bestätigung answers[0]=[2]. Die Warnung verschiebt die gerenderte Frage/Antwort-Anordnung; das sichtbare Verhalten ist mit einem zweiten Klick auf die nun darunter liegende Antwort vereinbar. Diese Reflow-Erklärung ist eine Inferenz, keine durch Reparatur oder Debug-Monkeypatch bewiesene Ursache.

Nach Bestätigung gespeichert [2], 1/120 Punkte, 0 vollständig richtige, 1 falsch/nicht vollständig richtige, 81 unbeantwortete. Die ursprüngliche Mischantwort [2,0] hätte nach unveränderter Punktefunktion 0 Punkte ergeben. Verlauf genau einmal von 3 auf 4; die drei älteren Einträge inhaltlich und im originalen JSON-Auszug unverändert. Schon im ersten Auditversuch trat eine entsprechende Auswahländerung bei Frage 12 auf. Der gezielte Zusatzversuch weist nach, dass der Fehler vor der Bestätigungsabgabe entsteht.

Keine Reparatur durchgeführt. Unabhängige Browserfälle konnten weiterhin belastbar geprüft werden. Einfachklick-Abgaben der 60-/59-Punkte-Versuche bewahrten ihre Auswahl und bestanden die Bewertungsfälle. Die Doppelzählung selbst besteht; die Datenintegrität des Doppelklick-Abgabeablaufs besteht nicht. Kein weiterer reproduzierbarer Produkt-FAIL wurde beobachtet; dies ist keine Behauptung einer vollständigen Fehlerfreiheit.

## Nicht verifiziert

- T03: natürlicher vollständiger 120-Minuten-Timeoutpfad.
- T04: natürlicher vollständiger 15-Minuten-Timeoutpfad.
- C01: lückenlose vollständige frühe Console-/Runtime-/Netzwerkhistorie, weil der CDP-Ereignispuffer ältere Ereignisse verdrängt hatte. Die einzelnen beobachteten Befunde bleiben dokumentiert.
- Physische Android-/iPhone-Geräte, Safari/iOS und andere Browser: nicht tatsächlich getestet. Mobile 390 × 844 ist nur Viewport-Emulation.

## Gesamtfazit

| Fall | Erwartung | Beobachtung | Ergebnis |
| --- | --- | --- | --- |
| P01 | Nur das autorisierte Audit-Dokument ändern; keine Produktreparatur, Kontrolltooländerung, Closure oder Task-Erweiterung. | Sämtliche Browseraktionen betreffen nur den isolierten Origin; keine Produktdatei bearbeitet. Repository-Ausgabepfad ausschließlich docs/BROWSER_END_TO_END_ACCEPTANCE_V2737K.md; keine Closure und kein neuer Task begonnen. | PASS |

Audit-Gesamtfazit: FAIL

47 Pflichtfälle: 43 PASS, 1 FAIL, 3 NOT VERIFIED. Der eine reproduzierbare Produktbefund F01 verhindert eine uneingeschränkte Browser-Abnahme. Die positiv beobachteten Funktionen und die nicht verifizierten Grenzen werden davon getrennt ausgewiesen. Ein technischer Kontroll-PASS für Lifecycle/Audit-Matrix bedeutet ausdrücklich nicht Produkt-PASS und darf F01 nicht beschönigen. Ein späterer Audit-Commit dokumentiert diesen Befund; er repariert oder schließt den Task nicht.
