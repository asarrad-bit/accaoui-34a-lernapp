# v27.37l – Schriftliche Prüfungsabgabe: Doppelklickschutz

## Ursache von F01

Die letzte wirksame `showExamSubmitWarning()` fügt `examWarningBox` mit
`prepend()` vor die Frage ein und startet `scrollIntoView()` mit smooth scrolling.
Die Position der Antwortbuttons verändert sich während derselben Pointerfolge.
Die bisherige Abgabe schützt nur den Abschluss vor Doppelverbuchung, nicht den
weiteren Klick auf einen durch Reflow verschobenen Antwortbutton. Dessen echter
`toggleExamAnswer()` entfernt eine erneut angeklickte Auswahl unmittelbar und
speichert sie. Aus [2,0] kann so [2] werden: falsch + richtig wird zu Teilpunkt.

Die lokale Browserdiagnose zeigte wechselnde Ziele beim zweiten Klick (unter
anderem Fragecontainer statt Abgabebutton). Die exakte F01-Ausprägung wurde im
geladenen Altcode tatsächlich reproduziert: [2,0] wurde vor Bestätigung zu [2],
auch im Storage, und 0 Punkte wurden zu 1. Die Kontrolle der geladenen Funktion
bestätigte ausdrücklich die alte Abgabelogik ohne Schutzfunktion. Ein bloßer
Reload hatte die alte app.js aus dem Browsercache behalten. Daher wurde die
Reparatur anschließend auf einem weiteren frischen Origin geprüft und der dort
geladene neue Funktionskörper ausdrücklich bestätigt. Nicht jeder Doppelklick
reproduziert den Altfehler; Fenstergröße, Scrollposition und Abstand spielen mit.
Der historische v27.37k-Audit bleibt unverändert FAIL.

## Reparatur und Grenzen

Unmittelbar vor der wirksamen Abgabeanforderung schützt ein kleiner Hilfsblock den
aktuellen `examQuestionArea` für 600 ms per Capture-Listener. Pointer-, Maus-,
Click- und Dblclick-Folgeereignisse werden vor Antwort- und Inline-Handlern
abgefangen. Der bereits laufende erste Klick bleibt wirksam. Tastaturaktivierung
(`click` mit `detail=0`) bleibt verfügbar. Nach 600 ms werden die Listener entfernt;
Antwortbearbeitung und bewusste Bestätigung funktionieren wieder normal.
Kein dauerhafter Lock, kein Debounce der Bewertung, keine Antwortnormalisierung.

Warnung, Nachholen offener Fragen und ausdrückliches „Trotzdem abgeben“ bleiben
erhalten. Bereits vollständig beantwortete Prüfungen werden normal abgeschlossen.
`finishExamMode()` und historische doppelte Funktionsdefinitionen bleiben
byte-identisch. Punkte, Teilpunkte, 60/59-Grenze, Pause/Resume, Timer, Versuchs-ID,
Fragenreihenfolge, Verlauf, Fehleranalyse und Fehlertraining bleiben unverändert.
Keine Änderung an Storage-Keys, Fragenbank, Auth, Session-Zugang oder Supabase.
Supabase bleibt NICHT LIVE.

## Ausführender Checker

`tools/check-written-exam-submit-doubleclick-v2737l.py` führt die vollständige
aktuelle app.js in isolierten Node-VM-Kontexten aus. Synthetische Fragen,
In-Memory-Storage und ein DOM mit tatsächlicher Capture-/Target-/Bubble-Reihenfolge
prüfen die realen Render-, Antwort-, Abgabe- und Abschlussfunktionen. Ein zweiter
Klick wird adversarial auf jede verschobene Antwort sowie Bestätigung gerichtet;
auch `detail=1` bei gewechseltem Ziel muss blockiert werden. Kein Produktstub.

Positivfälle schützen Einfachklick, [2,0] beim Warnungsrendern und nach dem zweiten
Klick, ausdrückliche Bestätigung mit 0 Punkten, Abschluss genau einmal,
Tastaturbedienung, abgelaufenen Pointer-Schutz, offene Fragen, Teilpunkte,
unbeantwortete Fragen, Pause/Reload/Resume sowie Vollsimulation 82/120/7200 und
60/59. Die bestehende v27.37g-Ausführungsregression läuft zusätzlich gegen den
aktuellen Quelltext; historische Lifecycle-Prüfungen bleiben unangetastet.

Elf Negativfälle: zweiter Antwortklick durchgelassen, Mutation beim Warnungsrendern,
Schutz entfernt, Einfachklick defekt, Warnung übersprungen, automatischer Abschluss,
Doppelverbuchung, falsche Punkte, zusätzlicher Storage-Key, Änderung außerhalb
erlaubter app.js-Grenzen und fremde Produktdatei. Alle JS-Mutationen müssen vorher
syntaktisch gültig sein; nur tatsächliche Assertion-Rejections zählen. Eingefrorene
Dateien werden gegen echte Git-Blobs der Autorisierungsbasis geprüft.

## Echter Browser-Smoke

PASS auf dem neuen isolierten Origin `http://127.0.0.1:55539/`, ohne vorhandene
Lernstände (Storage vor Start leer). Der reale Browser lud nachweislich die neue
Schutzfunktion und den neuen Abgabe-Funktionskörper. Vollsimulation: 82 Fragen,
120 Maximalpunkte und 7200 Sekunden. Keine injizierten Antworten, kein synthetischer
JS-Klick: Auswahl und Abgabe erfolgten über echte Browser-UI-Interaktionen.

- Doppelklick-Versuch `62ba4644-0884-4654-807c-0d15a9cab2c5`, Frage `ds_004`,
  richtige Indizes [1,2]: über Antwortbuttons zuerst 2, dann 0 gewählt.
  Vor Klick [2,0], 0 Punkte; echter schneller Doppelklick auf Abgabebutton;
  vor Bestätigung weiterhin [2,0] im laufenden Zustand und Storage, 0 Punkte,
  Warnung sichtbar, noch kein Verlaufseintrag. Nach „Trotzdem abgeben“ genau ein
  Ergebnis: 82 Fragen, 1 falsch, 81 unbeantwortet, 0/120 Punkte, Grenze 60.
- Separater Einfachklick-Versuch `d9d04760-638a-45d1-a485-2343602aa9c0`,
  Frage `roso_005`, richtige Indizes [1,2]: [2,0] vor und nach normalem Einfachklick,
  Storage [2,0], Warnung, kein vorzeitiger neuer Verlaufseintrag. Nach bewusster
  Bestätigung 0/120 Punkte. Verlauf enthält genau die zwei getrennten Versuche.
- Nur fünf vorhandene Storage-Keys: aktive Prüfung, Verlauf, Themenstatistik,
  Themenfehler und beantwortete Fragen. Keine Supabase-/Auth-/Session-Freigabe.

Der separate ausführende Checker ist PASS: 18 Positivfälle und 11 semantische
Negativfälle; zusätzlich die unveränderte aktuelle Abschlussregression mit
34 Positivfällen und 6 semantischen Mutationen. Syntaxfehler zählen nicht als PASS.
F01 in v27.37l repariert und separat nachgetestet; keine Umschreibung des alten Audits.

## Exakter Implementierungsscope

1. `app.js`: nur wirksame Abgabeanforderung und direkt zugehöriger kleiner Schutzblock.
2. `tools/check-written-exam-submit-doubleclick-v2737l.py`: neuer ausführender Checker.
3. `docs/WRITTEN_EXAM_SUBMIT_DOUBLECLICK_V2737L.md`: dieser separate Reparaturnachweis.
4. `tools/preflight.py`: ausschließlich vorbereitete Checker-Registrierung aktiviert.

Keine fünfte Implementierungsdatei. Kein Folgetask autorisiert.
