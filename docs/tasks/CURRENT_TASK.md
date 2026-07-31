# Verbindlicher aktueller Task

Task-ID: v27.35g
Status: AUTHORIZED
Autorisiert: JA
Titel: Punkteberechnung schriftliche Prüfung korrigieren
Funktionaler Ausgangsstand: v27.35d
Letzter abgeschlossener Kontrollschritt: v27.35e
Erwarteter Ausgangscommit: `db2f12a1af7792c59e9e6411bb127b2f68401713`
Erlaubte Dateien: `app.js`, `docs/WRITTEN_EXAM_SCORING_FIX_V2735G.md`
Commit erlaubt: NEIN
Push erlaubt: NEIN

## Ziel von v27.35g

Die Punkteberechnung der schriftlichen Prüfung so korrigieren, dass
vollständig korrekt beantwortete Fragen stets ihre volle hinterlegte
Punktzahl ergeben.

## Verbindlicher Bewertungsvertrag

1. Keine Antwort: 0 Punkte.
2. Ausgewählte Antwortmenge entspricht exakt der vollständigen richtigen
   Antwortmenge: volle hinterlegte Fragepunktzahl.
3. Zwei-Punkte-Frage mit mindestens zwei richtigen Optionen: eine nicht
   leere echte Teilmenge ausschließlich richtiger Optionen, ohne falsch
   ausgewählte Option: exakt 1 Punkt.
4. Falsch ausgewählte Option oder sonstige nicht vollständig
   beziehungsweise nicht zulässig teilrichtige Kombination: 0 Punkte.
5. Zwei-Punkte-Frage mit nur einer richtigen Antwort: vollständig richtig
   = exakt 2 Punkte.
6. Ein-Punkt-Frage: nur vollständig richtig = 1 Punkt, sonst 0.

## Akzeptanzkriterien

1. Alle 82 Core-Fragen vollständig richtig: exakt 120/120 Punkte.
2. Diese 13 Fragen vollständig richtig ergeben jeweils exakt 2/2 Punkte:
   `straf_009`, `bgb_009`, `waffen_004`, `straf_004`, `v23_roso_007`,
   `technik_004`, `straf_006`, `bgb_012`, `bgb_004`, `straf_013`,
   `bgb_006`, `uvv_004`, `uvv_008`.
3. `roso_002` vollständig richtig: 2/2 Punkte.
4. `roso_005` nur eine der zwei richtigen Optionen, keine falsche Option:
   1/2 Punkte.
5. `roso_005` eine richtige plus eine falsche Option: 0/2 Punkte.
6. `roso_001` vollständig richtig: 1/1 Punkt.
7. `roso_001` unvollständig oder mit falscher Option: 0/1 Punkte.
8. Die im v27.35e-Bericht verwendete Testkonstellation muss nach der
   Korrektur rechnerisch exakt 114/120 ergeben.
9. Richtig + falsch + unbeantwortet bleibt konsistent.
10. Pause/Fortsetzen bleibt unverändert funktionsfähig.
11. Fehleranalyse und Fehlertraining müssen vollständig browserbasiert
    geprüft werden.
12. Desktop und Mobil ca. 390 × 844 müssen geprüft werden.
13. Kein neuer Konsolenfehler.
14. localStorage und sessionStorage müssen nach den Tests vollständig auf
    den Ausgangszustand zurückgesetzt werden.
15. Der bestehende Bericht `docs/WRITTEN_EXAM_REGRESSION_V2735E.md` darf
    nicht verändert werden.

## Verboten

- `questions.json`
- `index.html`
- `style.css`
- `patch-v21.js`
- `oral-exam.js`
- `tools/preflight.py`
- Supabase-, SQL- und Migrationsdateien
- alle anderen Dateien
- Frageninhalte oder `points`-Felder ändern
- neue Speicherung
- neue Storage-Keys
- Netzwerk- oder Supabase-Anbindung

## Hinweis zu v27.35f

`v27.35f` bleibt ausschließlich für die später vorgemerkte Wettbewerbsbeobachtungsnotiz reserviert. `v27.35f` ist nicht autorisiert und wird jetzt nicht bearbeitet.

## Abgeschlossener Regressionstest v27.35e (FAIL)

Der Regressionstest der schriftlichen Prüfung wurde durchgeführt und mit
Gesamtergebnis FAIL abgeschlossen. Testbericht-Commit:
`db2f12a1af7792c59e9e6411bb127b2f68401713`.

Ursache: Bei Zwei-Punkte-Fragen mit nur einer richtigen Antwortoption
wurde bei vollständig korrekter Beantwortung nur 1 statt 2 Punkte
vergeben. Betroffen waren im getesteten Kernfragenpool 13 Fragen:
`straf_009`, `bgb_009`, `waffen_004`, `straf_004`, `v23_roso_007`,
`technik_004`, `straf_006`, `bgb_012`, `bgb_004`, `straf_013`,
`bgb_006`, `uvv_004`, `uvv_008`.

Es wurde keine Codekorrektur vorgenommen; der Testbericht
`docs/WRITTEN_EXAM_REGRESSION_V2735E.md` bleibt unverändert.

## Verbindliche Sperre

- Ausschließlich v27.35g und ausschließlich die Dateien `app.js` und
  `docs/WRITTEN_EXAM_SCORING_FIX_V2735G.md` sind für die spätere
  Umsetzung freigegeben.
- In diesem Steuerungsschritt wird `app.js` noch nicht verändert.
- Kein Folgeschritt nach v27.35g wird automatisch gewählt oder autorisiert.
- `v27.35f` ist nicht autorisiert und wird jetzt nicht bearbeitet.
- Aus Versionsfolgen, früheren Chats oder Erinnerung darf kein weiterer
  Task abgeleitet werden.
- Commit und Push bleiben bis zu einer gesonderten ausdrücklichen
  Freigabe gesperrt.

## Pflichtfelder eines später autorisierten Tasks

- Task-ID
- Ziel
- Erwarteter Ausgangsstand
- Erlaubte Dateien
- Verbotene Dateien
- Akzeptanzkriterien
- Tests
- Commit-Freigabe
- Push-Freigabe
