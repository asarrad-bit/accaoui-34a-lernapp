# v27.37j – Neutraler Herkunftshinweis im mündlichen Fehlertraining

## Ursache und Reparatur

Der gemeinsame Storage-Key `accaoui_oral_exam_mistakes_v2324` wird durch
verschiedene mündliche Übungswege gefüllt. Die Einträge enthalten keine belastbare
Provenienz. Die bisherigen Hinweise behaupteten dennoch eine 15-Minuten-Simulation
beziehungsweise eine mündliche Simulation als Herkunft.

Die drei betroffenen Texte verwenden jetzt neutral **mündliche Vorbereitung**:

- Übersicht (v23.2.4): Diese Fragen wurden in der mündlichen Vorbereitung mit „Noch üben“ bewertet.
- Historischer Renderer (v23.2.4): Hier erscheinen Fragen, die in der mündlichen Vorbereitung mit „Noch üben“ bewertet wurden.
- Führender Renderer (v23.4.0): Hier erscheinen Fragen, die in der mündlichen Vorbereitung mit „Noch üben“ bewertet wurden. Die Musterantwort bleibt zuerst verdeckt.

Keine neue Persistenz. Keine Migration. Keine neuen source-, mode- oder
provenance-Felder und kein zusätzlicher Storage-Key. Legitime Modusnamen außerhalb
der beiden Zielblöcke bleiben unverändert.

## Unverändertes Storage-/UI-Verhalten

Key, Datenformat und Lesen/Schreiben/Löschen bleiben identisch. 0, 1 und mehrere
Fehler, Karten, Zähler, Reveal/Collapse, Noch üben und Als sicher markieren behalten
ihre vorhandene Semantik. Der v27.37i-Leerzustand bleibt erhalten: Nach dem letzten
gelösten Fehler zeigt `.main-content` keine alte Karte und keinen alten Zähler;
Storage enthält exakt `[]`. Beschädigtes JSON bleibt fail-safe und wird nicht
überschrieben. Es gibt keine erzwungene Navigation.

Fragen, Prüfungsbögen, Timer und Bewertung bleiben unverändert. Auth, Session,
Teilnehmerzugang, Config, SDK, SQL und Migrationen bleiben unverändert.
Supabase bleibt NICHT LIVE.

## Ausführender Checker und Regressionen

Der neue Checker führt die tatsächlichen v23.2.4- und v23.4.0-Blöcke isoliert mit
synthetischem DOM/Storage aus. Er prüft gerenderte Herkunftsabsätze, Übersicht,
Karten/Zähler, unveränderte Altbestände sowie Speichern, Aktualisieren und Entfernen
ohne neue Herkunftsfelder. Zusätzlich führt er den unveränderten v27.37i-Harness
gegen die aktuelle echte v23.4.0-Logik aus. Syntaxgültige Laufzeitmutationen und
Byte-/Scope-Mutationen werden getrennt geprüft; Syntaxfehler zählen niemals als
bestandene semantische Mutation.

Alle Bytes außerhalb der Zielblöcke, sämtliche übrigen Produktbytes und die
historischen Checker bleiben eingefroren. Preflight aktiviert ausschließlich die
vorbereitete feste Checker-Registrierung. Der Gate-Repair bleibt unverändert:
Der vollständige historische v27.37i-Checker läuft weiter im echten temporären
Closure-Checkout, ohne Monkeypatch, Stub oder Fake-Phase. Der v27.34e-Vertrag bleibt
verbindlich. Eine Closure ist nicht Teil dieses Implementierungsauftrags.

## Exakter Fünf-Dateien-Scope

1. `patch-v21.js` – zwei Herkunftstexte im bestehenden v23.2.4-Block.
2. `oral-exam.js` – ein Herkunftstext im bestehenden v23.4.0-Block.
3. `tools/check-oral-mistake-origin-label-v2737j.py` – ausführender Checker.
4. `docs/ORAL_MISTAKE_ORIGIN_LABEL_V2737J.md` – diese Dokumentation.
5. `tools/preflight.py` – ausschließlich Aktivierung des vorbereiteten Checker-Pfads.

Keine sechste Datei. Insbesondere app.js, index.html, style.css, oral-exam.css,
test/*, questions.json, Fragenbanken, oral-sheets-Dateien und Steuerungsdokumente
bleiben unverändert. Keine Live-Verbindung und keine echten Teilnehmerdaten.
