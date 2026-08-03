# Punkteberechnung schriftliche Prüfung korrigiert – v27.35g

## 1. Task und getesteter HEAD

- Task-ID: v27.35g
- Titel: Punkteberechnung schriftliche Prüfung korrigieren
- Funktionaler Ausgangsstand: v27.35d
- Erwarteter Ausgangscommit: `db2f12a1af7792c59e9e6411bb127b2f68401713`
- Verbindlicher aktueller HEAD zu Beginn dieses Schritts: `0018334aba07e3098111e80b4eb6218b2ca898c0`
- Branch: `main`, Arbeitsbaum vor der Änderung sauber; lokaler HEAD und
  `refs/heads/main` auf GitHub stimmten exakt überein.
- Ausschließlich geänderte Dateien: `app.js`, `docs/WRITTEN_EXAM_SCORING_FIX_V2735G.md`.
- Der bestehende Testbericht `docs/WRITTEN_EXAM_REGRESSION_V2735E.md` wurde
  nicht verändert.

## 2. Vorheriger Fehler (Regression aus v27.35e)

`getExamQuestionReachedPoints()` zählte lediglich die Anzahl korrekt
ausgewählter Antwortindizes und begrenzte das Ergebnis mit
`Math.min(reached, getQuestionPoints(question))`. Für Zwei-Punkte-Fragen mit
nur **einer** richtigen Antwortoption (`question.correct.length === 1`)
konnte `reached` rechnerisch niemals den Wert `2` erreichen, selbst bei
vollständig korrekter Beantwortung. Betroffen waren im 82-Fragen-Kernpool 13
Fragen: `straf_009`, `bgb_009`, `waffen_004`, `straf_004`, `v23_roso_007`,
`technik_004`, `straf_006`, `bgb_012`, `bgb_004`, `straf_013`, `bgb_006`,
`uvv_004`, `uvv_008`. Zusätzlich vergab die alte Logik bei einer Mischung aus
einer richtigen und einer falschen Auswahl fälschlich Teilpunkte, statt die
Frage vollständig mit 0 Punkten zu bewerten.

## 3. Genaue Codekorrektur

Datei: `app.js`, Funktion `getExamQuestionReachedPoints(question, selectedAnswersForQuestion)`.
`isExamAnswerCorrect()` und `getQuestionPoints()` wurden nicht verändert.
Keine Fragen- oder `points`-Daten wurden verändert. Keine neue Speicherung,
keine neuen Storage-Keys.

```javascript
function getExamQuestionReachedPoints(question, selectedAnswersForQuestion) {
  if (!question || !Array.isArray(selectedAnswersForQuestion) || selectedAnswersForQuestion.length === 0) {
    return 0;
  }

  if (!Array.isArray(question.correct) || question.correct.length === 0) {
    return 0;
  }

  const correctIndexes = new Set(question.correct);
  const selectedUnique = [...new Set(selectedAnswersForQuestion)];

  const hasWrongSelection = selectedUnique.some(index => !correctIndexes.has(index));
  if (hasWrongSelection) {
    return 0;
  }

  const points = getQuestionPoints(question);

  if (selectedUnique.length === correctIndexes.size) {
    return points;
  }

  if (points === 2 && correctIndexes.size >= 2) {
    return 1;
  }

  return 0;
}
```

Implementierungsdetails:

- `selectedUnique = [...new Set(selectedAnswersForQuestion)]` entfernt
  doppelte ausgewählte Indizes defensiv.
- Der Vergleich erfolgt ausschließlich über `Set`-Mitgliedschaft und
  `size`/`length`; die Reihenfolge der Antworten spielt keine Rolle.
- Eine ungültige `question.correct`-Struktur (kein Array oder leer) wird
  defensiv mit 0 Punkten bewertet, bevor `correctIndexes` gebildet wird.
- Sobald mindestens eine falsche Option ausgewählt wurde
  (`hasWrongSelection`), wird sofort 0 zurückgegeben – unabhängig vom
  Punktwert der Frage.
- Entspricht die ausgewählte Menge exakt der vollständigen richtigen
  Antwortmenge (`selectedUnique.length === correctIndexes.size`), wird die
  volle hinterlegte Punktzahl (`getQuestionPoints(question)`) zurückgegeben.
- Nur wenn die Frage `points === 2` trägt und mindestens zwei richtige
  Optionen besitzt (`correctIndexes.size >= 2`), ergibt eine nicht leere
  echte Teilmenge ausschließlich richtiger Optionen ohne falsche Auswahl
  exakt 1 Punkt.
- In allen übrigen, nicht vollständig richtigen Fällen wird 0 zurückgegeben.

## 4. Verbindlicher Bewertungsvertrag

1. Keine oder ungültige Antwort: 0 Punkte.
2. Ausgewählte eindeutige Antwortmenge entspricht exakt der vollständigen
   richtigen Antwortmenge: volle hinterlegte Fragepunktzahl.
3. Zwei-Punkte-Frage mit mindestens zwei richtigen Optionen: eine nicht
   leere echte Teilmenge ausschließlich richtiger Optionen, ohne falsche
   Auswahl: exakt 1 Punkt.
4. Sobald mindestens eine falsche Option gewählt wurde: 0 Punkte.
5. Zwei-Punkte-Frage mit nur einer richtigen Option: vollständig richtig
   ergibt exakt 2 Punkte.
6. Ein-Punkt-Frage: nur vollständig richtig ergibt 1 Punkt, sonst 0.
7. Andere Punktwerte: nur vollständig richtig ergibt die volle Punktzahl,
   sonst 0.

## 5. Testmatrix

| Nr. | Prüfung | Erwartung | Ergebnis | Status |
|---|---|---|---|---|
| 1 | Statische Logikprüfung: alle 82 Core-Fragen vollständig richtig (Node, `questions.json` gegen neue Funktion) | 120/120 | 120/120 | PASS |
| 2 | Statische Logikprüfung: jede der 13 Regressionsfragen einzeln vollständig richtig | jeweils 2/2 | jeweils 2/2 (alle 13 einzeln bestätigt) | PASS |
| 3 | `roso_002` vollständig richtig | 2/2 | 2/2 | PASS |
| 4 | `roso_005` eine von zwei richtigen Optionen, keine falsche | 1/2 | 1/2 | PASS |
| 5 | `roso_005` eine richtige plus eine falsche Option | 0/2 | 0/2 | PASS |
| 6 | `roso_001` vollständig richtig | 1/1 | 1/1 | PASS |
| 7 | `roso_001` unvollständig (nur eine von zwei richtigen) | 0/1 | 0/1 | PASS |
| 8 | `roso_001` mit einer falschen Option | 0/1 | 0/1 | PASS |
| 9 | Statische Simulation der v27.35e-Testkonstellation (13 Regressionsfragen korrekt, `ds_001`/`gewo_002` falsch, `gewo_004`/`ds_002` unbeantwortet, `roso_005` teilrichtig, alle übrigen 77 Fragen korrekt) | 114/120, Richtig 77 / Falsch 3 / Unbeantwortet 2 | 114/120, 77/3/2 | PASS |
| 10 | Browser: Vollsimulation starten | 82 Fragen, 120 Punkte, 120-Minuten-Timer sichtbar | `examQuestions.length === 82`, `getExamMaxPoints() === 120`, Timer „119:xx“ sichtbar | PASS |
| 11 | Browser: reale Testkonstellation aus Zeile 9 vollständig per UI-Klicks (Fragen 1–10) und Skript-Klicks (Fragen 11–82) durchgeführt, `getExamReachedPoints()` vor Abgabe geprüft | 114/120 | Dry-Run vor Abgabe: 114/120; nach Abgabe angezeigt: „Punkte: 114/120“, „Gesamtfragen: 82“, „Richtig: 77“, „Falsch: 3“, „Unbeantwortet: 2“, „95%“ | PASS |
| 12 | Browser: Pause bei Frage 10/82, Seite neu geladen, über Dashboard-Karte fortgesetzt | Fragenreihenfolge, Position, Antworten erhalten | Dashboard zeigte „Frage 11/82 · gespeichert am 3.8.2026, 16:20:10“; nach Fortsetzen: `examQuestionIndex === 10`, `examAnswers` für Index 0–9 identisch, aktuelle Frage `umgang_004` korrekt | PASS |
| 13 | Browser: „Fehler ansehen“ nach Abgabe der Testkonstellation | genau die 3 falschen und 2 unbeantworteten Fragen erscheinen | genau 5 Fragen angezeigt (`gewo_002`, `ds_001`, `ds_002`, `gewo_004`, `roso_005`) mit korrekter Lösung und Erklärung | PASS |
| 14 | Browser: „Fehlertraining starten“ / „Alle Fehler trainieren“ | Fehlertrainingsmodus startet mit den gespeicherten Fehlerfragen | Lernmodus „Fehlertraining alle Themen“ startete korrekt mit der ersten Fehlerfrage | PASS |
| 15 | Browser: unbeantwortete Fragen in der Fragenübersicht vor Abgabe | genau Fragen 8 und 46 (1-indexed) als unbeantwortet markiert | `exam-nav-btn` ohne Klasse `answered`: genau `[8, 46]` | PASS |
| 16 | Browser: alle 82 Fragen vollständig korrekt (zweiter, unabhängiger Durchlauf, Mobilansicht) | 120/120, 100 % | Dry-Run `getExamReachedPoints() === 120`; nach Abgabe: „Punkte: 120/120“, „Richtig: 82“, „Falsch: 0“, „Unbeantwortet: 0“, „100%“ | PASS |
| 17 | Browser: Desktop-Ansicht | kein horizontaler Überlauf, keine neuen Konsolenfehler | Dashboard und Prüfungsseiten vollständig nutzbar, keine Fehler | PASS |
| 18 | Browser: Mobilansicht 390 × 844 (Dashboard, Prüfungsfrage, Endauswertung) | kein horizontaler Überlauf, keine neuen Konsolenfehler | `document.documentElement.scrollWidth === window.innerWidth === 390` in allen drei Ansichten; Endauswertung „Punkte: 120/120“ vollständig lesbar ohne Überlauf | PASS |
| 19 | Konsolenstatus während des gesamten Browsertests | keine neuen Konsolenfehler, keine unbehandelten Promise-Fehler | `window.__testErrors` blieb in allen überwachten Phasen leer (`[]`); zusätzliche Navigation durch alle Hauptbereiche (Statistik, Alle Fragen, Lernkarten, Fehlerübersicht, Mündliche Prüfung, Prüfungsstart) ohne Ausnahme | PASS |
| 20 | Speicherwiederherstellung | `localStorage`/`sessionStorage` nach Test exakt auf Ausgangszustand (0 Einträge) | Vor Test: 0/0 Einträge; nach Test `localStorage.clear()`/`sessionStorage.clear()` ausgeführt, erneut 0/0 Einträge bestätigt; lokaler Testserver beendet | PASS |
| 21 | `node --check app.js` | keine Syntaxfehler | keine Ausgabe, Exit-Code 0 | PASS |

## 6. Nachweis 82/120

Statische Prüfung (Node, `questions.json` gegen die neue Funktion): Summe
`getQuestionPoints()` über alle 82 Core-Fragen-IDs (`EXAM_CORE_QUESTION_IDS_V244`)
ergibt 120; bei vollständig korrekter Beantwortung aller 82 Fragen ergibt
`getExamQuestionReachedPoints()` in Summe ebenfalls 120.

Browserbasiert (zweiter, unabhängiger Durchlauf in der Mobilansicht): alle
82 Fragen der Vollsimulation vollständig korrekt beantwortet, Endauswertung
zeigt „Gesamtfragen: 82“, „Richtig: 82“, „Falsch: 0“, „Unbeantwortet: 0“,
„Punkte: 120/120“, „100%“, „Bestanden“.

## 7. Nachweis aller 13 Fragen

Statisch (Node) für jede der 13 Fragen einzeln geprüft: `straf_009`,
`bgb_009`, `waffen_004`, `straf_004`, `v23_roso_007`, `technik_004`,
`straf_006`, `bgb_012`, `bgb_004`, `straf_013`, `bgb_006`, `uvv_004`,
`uvv_008` – jede Frage hat `points = 2` und genau eine richtige Option
(`correct.length = 1`); bei vollständig korrekter Beantwortung liefert
`getExamQuestionReachedPoints()` für jede der 13 Fragen exakt 2 Punkte
(zuvor 1 Punkt).

Browserbasiert wurden alle 13 Fragen als Teil der Testkonstellation (Zeile
11 der Testmatrix) vollständig korrekt beantwortet und trugen vollständig
zu den zusätzlichen 13 Punkten bei, die den Unterschied zwischen 101/120
(alter Fehler) und 114/120 (korrigiert) ausmachen.

## 8. Nachweis 114/120

Statische Simulation (Node) der exakten v27.35e-Testkonstellation (13
Regressionsfragen vollständig korrekt, `ds_001` und `gewo_002` absichtlich
falsch, `gewo_004` und `ds_002` unbeantwortet, `roso_005` teilrichtig mit
einer von zwei richtigen Optionen, alle übrigen 77 Fragen vollständig
korrekt): Summe der neuen `getExamQuestionReachedPoints()`-Aufrufe ergibt
exakt 114; „richtig“-artige Zählung (exakte Übereinstimmung) ergibt 77,
„falsch“ 3, „unbeantwortet“ 2, Summe 82.

Browserbasiert wurde dieselbe Konstellation real in der Vollsimulation
durchgeführt: vor Abgabe lieferte `getExamReachedPoints()` bereits 114; nach
Abgabe zeigte die Endauswertung „Gesamtfragen: 82“, „Richtig: 77“,
„Falsch: 3“, „Unbeantwortet: 2“, „Punkte: 114/120“, „Bestehensgrenze: 60
Punkte“, „95%“, „Bestanden“ – exakt die geforderten 114/120 statt der
vormals fehlerhaften 101/120.

## 9. Pause/Fortsetzen

Nach Beantwortung der Fragen 1–10 (inklusive der absichtlich falschen
Antwort bei `gewo_002`) wurde die Prüfung über „Prüfung pausieren“
gespeichert. Die Seite wurde vollständig neu geladen (Simulation von
„App verlassen“). Das Dashboard zeigte korrekt die Karte „Prüfung
fortsetzen“ mit „Frage 11/82 · gespeichert am 3.8.2026, 16:20:10“. Nach
Klick auf „Prüfung fortsetzen“ war `examQuestionIndex` wieder exakt 10, alle
zuvor gespeicherten Antworten (Indizes 0–9) waren byte-identisch erhalten,
und die aktuell angezeigte Frage entsprach der erwarteten Frage
(`umgang_004`). Ergebnis: PASS.

## 10. Fehleranalyse und Fehlertraining

Nach Abgabe der Testkonstellation (114/120) wurde „Fehler ansehen“
aufgerufen: Es erschienen exakt die 5 erwarteten Fragen (3 falsch: `gewo_002`,
`ds_001`, `roso_005`; 2 unbeantwortet: `ds_002`, `gewo_004`), jeweils mit der
gegebenen bzw. fehlenden Antwort, der korrekten Lösung und der Erklärung.
Anschließend wurde „Fehlertraining starten“ und darin „Alle Fehler
trainieren“ aufgerufen; der Fehlertrainingsmodus startete korrekt im
Lernmodus mit der ersten Fehlerfrage. Beide Ansichten funktionierten ohne
Fehler. Ergebnis: PASS.

## 11. Desktop und Mobil

- Desktop: Dashboard, Prüfungsstart, Prüfungsfragen, Fehleranalyse und
  Fehlertraining wurden vollständig und fehlerfrei dargestellt.
- Mobil (390 × 844, Emulation via `Emulation.setDeviceMetricsOverride`):
  Dashboard, eine Prüfungsfrage und die vollständige Endauswertung (120/120)
  wurden geprüft. `document.documentElement.scrollWidth` entsprach in allen
  drei Ansichten exakt `window.innerWidth` (390), es trat kein horizontaler
  Überlauf auf.

Ergebnis: PASS.

## 12. Konsolenstatus

Während der gesamten Prüfungsdurchführung (Start, 82 Antworten, Pause,
Neuladen, Fortsetzen, Abgabe, Fehleranalyse, Fehlertraining, zweiter
Vollsimulationsdurchlauf in Mobilansicht sowie zusätzliche Navigation durch
Statistik, Alle Fragen, Lernkarten, Fehlerübersicht, Mündliche Prüfung und
Prüfungsstart) wurden über `window.error`, `window.unhandledrejection` und
einen `console.error`-Abfangpunkt keine neuen Konsolenfehler und keine
unbehandelten Promise-Fehler erfasst (`window.__testErrors` blieb in jeder
überwachten Phase leer).

## 13. Speicherwiederherstellung

- Ausgangszustand vor dem Test: `localStorage` und `sessionStorage` jeweils
  mit 0 Einträgen (verifiziert vor dem ersten Testschritt).
- Während der Tests wurden durch die Prüfungs-, Pause/Fortsetzen- und
  Fehlertrainingsdurchführung folgende `localStorage`-Schlüssel befüllt:
  `accaoui_topic_stats`, `accaoui_answered_questions`,
  `accaoui_active_session`, `accaoui_exam_history`,
  `accaoui_active_learning_session`, `accaoui_topic_mistakes`.
- Nach Testende wurden `localStorage.clear()` und `sessionStorage.clear()`
  ausgeführt; beide wurden anschließend erneut mit 0 Einträgen bestätigt.
- Der lokale Testserver (`python -m http.server 8765`) wurde ordentlich
  beendet.
- Es wurden ausschließlich mit dem Testskript erzeugte, synthetische
  Prüfungsantworten verwendet. Keine echten Teilnehmerdaten.

## 14. Gesamtergebnis

**PASS**

Die Korrektur von `getExamQuestionReachedPoints()` in `app.js` behebt die in
`docs/WRITTEN_EXAM_REGRESSION_V2735E.md` dokumentierte Regression
vollständig. Alle Pflichtprüfungen aus dem verbindlichen Bewertungsvertrag
(vollständig korrekte Antwort ergibt volle Punktzahl, definierte
Teilpunktlogik bei Zwei-Punkte-Fragen mit mindestens zwei richtigen
Optionen, 0 Punkte bei jeder falschen Auswahl, korrekte 1-Punkt- und
Zwei-Punkte-Sonderfälle) sind bestanden, sowohl in statischer Logikprüfung
als auch in vollständigen Browsertests (Desktop und Mobil, Pause/Fortsetzen,
Fehleranalyse, Fehlertraining, Konsolenstatus, Speicherwiederherstellung).
`isExamAnswerCorrect()` und `getQuestionPoints()` wurden nicht verändert, es
wurden keine Fragen- oder `points`-Daten verändert, keine neue Speicherung
und keine neuen Storage-Keys eingeführt. Es erfolgte kein Commit und kein
Push.
