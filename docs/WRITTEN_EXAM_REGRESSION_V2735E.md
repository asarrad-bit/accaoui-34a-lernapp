# Regressionstest der schriftlichen Prüfung – v27.35e

## 1. Task und Testdatum

- Task-ID: v27.35e
- Titel: Regressionstest der schriftlichen Prüfung
- Testdatum: 31.07.2026
- Getesteter HEAD: `902124236cc0ff6c3d4785d8c29cf189469711d1`
- Funktionaler Ausgangscommit (Baseline): `260e6527208769f18018d1db6e6e3b7fbe9d7d7e`
- Zwischen Baseline und getestetem HEAD wurde ausschließlich die
  nichtfunktionale v27.35e-Autorisierung committet
  (`9021242 v27.35e authorize written exam regression test`);
  `app.js`, `index.html`, `style.css`, `patch-v21.js`, `questions.json`
  und `oral-exam.js` sind seit der Baseline unverändert.

## 2. Testumgebung

- Repository: `C:\xampp\htdocs\accaoui\v4-dashboard`
- Branch: `main`, Arbeitsbaum vor und nach dem Test sauber, vorhandene
  Git-Stashes unverändert (`home-safety-before-sync-20260731-0951`,
  `wip v24.6c active exam session pause resume`).
- Isolierter lokaler Server: `python -m http.server 8765`
  (nur für die Testdauer gestartet, danach beendet).
- Browser: Cursor-eigener Browser-Tab (Chromium/CDP), Desktop-Viewport
  sowie geplanter Mobil-Viewport ca. 390 × 844 (siehe Abschnitt 8 –
  wegen STOPP nicht mehr durchgeführt).
- Ausgangszustand `localStorage`/`sessionStorage`: leer (0 Einträge),
  vor jeder Testhandlung geprüft und protokolliert.
- Es wurden ausschließlich mit dem Testskript erzeugte, synthetische
  Prüfungsantworten verwendet. Keine produktiven oder echten
  Teilnehmerdaten.

## 3. Prüfungsumfang (Kriterium B)

- Die Vollsimulation (`§34a Vollsimulation`) zeigt auf der
  Auswahlseite exakt **82 Fragen** an (`EXAM_FULL_QUESTION_LIMIT_V20 = 82`,
  fester Fragenpool `EXAM_CORE_QUESTION_IDS_V244`).
- Rechnerisch nachgewiesen (Summe des Feldes `points` aller 82
  Core-Fragen-IDs aus `questions.json` gegen `app.js`):
  **Maximalpunktzahl = 120 Punkte.**
- Beim tatsächlichen Start der Vollsimulation im Browser wurde bestätigt:
  `examQuestions.length === 82` und `getExamMaxPoints() === 120`.
- Ergebnis: **PASS**

## 4. Testmatrix

| Schritt | Erwartung | Tatsächliches Ergebnis | Status |
|---|---|---|---|
| A. App-Start | App lädt vollständig, keine neuen Konsolenfehler, Navigation zur schriftlichen Prüfung funktioniert | App lädt fehlerfrei, Dashboard zeigt „86 Fragen verfügbar“, Navigation zu „Prüfung starten“ → „Vollsimulation“ funktioniert | PASS |
| B. Prüfungsumfang | Vollsimulation = 82 Fragen, 120 Punkte | Bestätigt: 82 Fragen, 120 Punkte (siehe Abschnitt 3) | PASS |
| C. Fragentypen: Einzelauswahl | Einzelauswahlfrage korrekt bewertbar | `v23_roso_006` (single, 1 Punkt) korrekt beantwortet und im Endergebnis als richtig gezählt | PASS |
| C. Fragentypen: Mehrfachauswahl | Mehrfachauswahlfrage korrekt bewertbar | `roso_001` (multiple, 1 Punkt, 2 richtige Antworten) vollständig korrekt ausgewählt, als richtig gezählt | PASS |
| C. Ein-Punkt-Frage korrekt/falsch | Ein-Punkt-Frage korrekt und falsch je einmal getestet | `v23_roso_006` korrekt (1/1 Punkt erreicht); `ds_001` und `gewo_002` (je 1 Punkt) absichtlich falsch beantwortet, je 0 Punkte erreicht, als „falsch“ gezählt | PASS |
| C. Zwei-Punkte-Frage vollständig korrekt | Zwei-Punkte-Frage korrekt beantwortet ergibt volle Punktzahl | `roso_002` (multiple, 2 Punkte, 2 richtige Antworten) vollständig korrekt ausgewählt → 2/2 Punkte erreicht (korrekt) | PASS |
| C. Zwei-Punkte-Frage teilrichtig | Teilrichtige Antwort ergibt exakt 1 Punkt | `roso_005` (multiple, 2 Punkte, 2 richtige Antworten) – nur 1 der 2 richtigen Antworten ausgewählt → `getExamQuestionReachedPoints()` liefert exakt 1 Punkt | PASS |
| **C. Zwei-Punkte-Frage mit nur einer richtigen Antwortoption, vollständig korrekt beantwortet** | Vollständig korrekte Antwort auf eine 2-Punkte-Frage muss 2/2 Punkte ergeben | **REGRESSION:** 13 Fragen der 82 Core-Fragen sind mit `points = 2`, aber besitzen nur **eine** richtige Antwortoption (`correct.length = 1`). Bei vollständig korrekter Beantwortung liefert `getExamQuestionReachedPoints()` nur **1 von 2 Punkten**, obwohl die Frage laut `isExamAnswerCorrect()` als vollständig „richtig“ gezählt wird. Betroffene Fragen-IDs im getesteten Lauf: `straf_009`, `bgb_009`, `waffen_004`, `straf_004`, `v23_roso_007`, `technik_004`, `straf_006`, `bgb_012`, `bgb_004`, `straf_013`, `bgb_006`, `uvv_004`, `uvv_008`. Summe des Punktverlusts: **13 Punkte**. | **FAIL** |
| D. Pause und Fortsetzen | Fragenreihenfolge, Position, Antworten und Punktestand bleiben nach Pause/Fortsetzen erhalten | Nach Beantwortung der Fragen 1–10 pausiert, Seite neu geladen (Server-Neuladen simuliert „App verlassen“), über Dashboard-Karte „Prüfung fortsetzen“ (Anzeige „Frage 10/82 · gespeichert am 31.7.2026, 12:32:10“) fortgesetzt. Vergleich vor/nach: `currentIndex` 9 = 9, `examAnswers` (Fragen 0–9) byte-identisch, `orderIds` (alle 82 Fragen-IDs in Reihenfolge) identisch. Timer lief nach Fortsetzen korrekt weiter (kein Zurücksetzen). | PASS |
| E. Unbeantwortete Fragen | Endauswertung zeigt exakt die absichtlich unbeantwortet gelassenen Fragen | `gewo_004` und `ds_002` absichtlich nicht beantwortet. Endauswertung zeigt „Unbeantwortet: 2“, exakt übereinstimmend mit den beiden vorgesehenen Fragen-IDs (programmatisch verifiziert vor Abgabe) | PASS (im Rahmen der vor dem STOPP durchgeführten Prüfung) |
| F. Fehlertraining | Fehlertraining/Fehleranalyse zeigt ausschließlich tatsächlich falsche bzw. unbeantwortete Fragen | Absichtlich falsch beantwortet: `ds_001`, `gewo_002`, `roso_005` (teilrichtig, dennoch laut `isExamAnswerCorrect()` als „falsch“ gewertet). Endergebnis zeigt „Falsch: 3“, exakt übereinstimmend. Die Ansicht „Fehler ansehen“ bzw. „Fehlertraining“ ist laut Code (`finishExamMode()`/`showExamReview()`) so konzipiert, dass sie sowohl falsch beantwortete als auch unbeantwortete Fragen zusammenfasst (bestehendes, unverändertes Verhalten) – dies wurde anhand der Zahlen nachvollzogen, aber wegen des STOPP nach der Regression nicht mehr im UI bis zum Ende durchgeklickt (siehe Abschnitt 6) | Teilweise geprüft, wegen STOPP nicht vollständig abgeschlossen |
| G. Endauswertung – rechnerische Konsistenz | Richtig + Falsch + Unbeantwortet = Gesamtfragen; Punkte konsistent | Richtig 77 + Falsch 3 + Unbeantwortet 2 = 82 (korrekt). Punkte: 101/120 angezeigt. Die 101 Punkte sind rechnerisch **nicht** die erwarteten 114 Punkte (120 − 6 aus den absichtlichen Fehlern/Teilpunkten/unbeantworteten Fragen), sondern um zusätzliche 13 Punkte niedriger – exakt der in Abschnitt „Zwei-Punkte-Frage mit nur einer richtigen Antwortoption“ dokumentierte Fehler | **FAIL** (Ursache: siehe C) |
| H. Desktop und Mobil | Desktop und Mobilansicht (ca. 390 × 844) ohne Überlauf/Überlagerung nutzbar | **Nicht mehr durchgeführt** – Testabbruch (STOPP) nach gefundener Regression, bevor dieser Schritt erreicht wurde | Nicht durchgeführt (STOPP) |
| I. Speicherwiederherstellung | `localStorage`/`sessionStorage` nach Test vollständig auf Ausgangszustand zurückgesetzt, Testserver ordentlich beendet | `localStorage.clear()`/`sessionStorage.clear()` ausgeführt, beide wieder mit 0 Einträgen bestätigt (Ausgangszustand war ebenfalls 0 Einträge). Lokaler Testserver (`python -m http.server 8765`) beendet | PASS |

## 5. Konkrete Nachweise

- **Einzelauswahl:** `v23_roso_006` (Typ `single`, 1 Punkt) – vollständig korrekt beantwortet, im Endergebnis unter den 77 richtigen Fragen.
- **Mehrfachauswahl:** `roso_001` (Typ `multiple`, 1 Punkt, 2 richtige Antworten) – vollständig korrekt beantwortet.
- **Ein-Punkt-Bewertung:** `v23_roso_006` korrekt → 1/1 Punkt; `ds_001` und `gewo_002` absichtlich falsch → je 0/1 Punkt.
- **Zwei-Punkte-Bewertung (korrekt):** `roso_002` vollständig korrekt → 2/2 Punkte.
- **Zwei-Punkte-Bewertung (fehlerhaft, Regression):** 13 Fragen (siehe Liste oben) vollständig korrekt beantwortet, aber nur 1/2 Punkte erreicht.
- **Teilpunkt:** `roso_005` (2 Punkte, 2 richtige Antworten), nur 1 richtige Antwort ausgewählt → exakt 1 Punkt erreicht (`getExamQuestionReachedPoints` bestätigt).
- **Pause/Fortsetzen:** siehe Testmatrix Zeile D – Reihenfolge, Position, Antworten, Restzeit vollständig erhalten.
- **Unbeantwortete Fragen:** `gewo_004`, `ds_002` – Endauswertung zeigt „Unbeantwortet: 2“.
- **Endauswertung (Screenshot):** Ergebnisseite zeigt „Bestanden“, „84%“, „Gesamtfragen: 82“, „Richtig: 77“, „Falsch: 3“, „Unbeantwortet: 2“, „Punkte: 101/120“, „Bestehensgrenze: 60 Punkte“.

## 6. Fehlerregel – STOPP

Gemäß der verbindlichen Fehlerregel für v27.35e wurde nach dem Auffinden
der Punktebewertungs-Regression sofort gestoppt:

- Der Fehler wurde reproduziert und oben exakt dokumentiert
  (betroffene Fragen-IDs, erwarteter vs. tatsächlicher Punktwert,
  Ursache in `getExamQuestionReachedPoints()`/Datenstruktur der
  betroffenen Fragen).
- Es wurde **keine Codekorrektur** durchgeführt.
- Es wurde **keine weitere Datei** außer diesem Testbericht verändert.
- Die Testschritte H (Desktop/Mobil) sowie das vollständige
  Durchklicken von Fehleranalyse/Fehlertraining im UI wurden nach dem
  STOPP nicht mehr durchgeführt.
- Es erfolgte **kein Commit** und **kein Push**.

## 7. Technische Ursachenbeschreibung (zur Dokumentation, keine Korrektur)

In `app.js` berechnet `getExamQuestionReachedPoints(question, selected)`
die erreichten Punkte je Frage als Anzahl der korrekt ausgewählten
Antwortindizes, begrenzt auf `getQuestionPoints(question)`:

```3773:3789:app.js
function getExamQuestionReachedPoints(question, selectedAnswersForQuestion) {
  ...
  const correctIndexes = new Set(question.correct);
  const selectedUnique = [...new Set(selectedAnswersForQuestion)];
  let reached = 0;

  selectedUnique.forEach(index => {
    if (correctIndexes.has(index)) {
      reached += 1;
    }
  });

  return Math.min(reached, getQuestionPoints(question));
}
```

Für Fragen, bei denen `question.correct.length` kleiner ist als
`question.points` (im getesteten Fragenpool: 13 Fragen mit
`points = 2` und genau einer richtigen Antwortoption), kann `reached`
rechnerisch niemals den Wert `points` erreichen, selbst bei
vollständig korrekter Beantwortung. Dies führt zu einer systematisch
zu niedrigen Gesamtpunktzahl bei der Vollsimulation.

Diese Beschreibung dient ausschließlich der Dokumentation der
Regression. Es wurde bewusst keine Code- oder Datenänderung
vorgenommen.

## 8. Konsolenstatus

- Während des gesamten Tests (App-Start, Navigation, 82 Fragen
  beantwortet/übersprungen, Pause, Seiten-Neuladen, Fortsetzen,
  Abgabe) wurden **keine neuen Konsolenfehler** und keine
  unbehandelten Promise-Fehler erfasst (`window.__testErrors` blieb
  leer; zusätzlich wurde `console.error` temporär überwacht).

## 9. Speicherwiederherstellung

- Ausgangszustand vor dem Test: `localStorage` und `sessionStorage`
  jeweils mit 0 Einträgen.
- Nach dem Test wurden durch die Prüfungsdurchführung folgende
  `localStorage`-Schlüssel befüllt: `accaoui_topic_stats`,
  `accaoui_answered_questions`, `accaoui_exam_history`,
  `accaoui_topic_mistakes`.
- Beide Storages wurden anschließend vollständig geleert
  (`localStorage.clear()`, `sessionStorage.clear()`) und auf den
  ursprünglichen Zustand (0 Einträge) zurückgeführt und verifiziert.
- Der lokale Testserver wurde ordentlich beendet.

## 10. Gesamtergebnis

**FAIL**

Ursache: Systematische Punktebewertungs-Regression bei
Zwei-Punkte-Fragen mit nur einer richtigen Antwortoption
(13 betroffene Fragen im 82-Fragen-Kernpool, Punktverlust 13 Punkte
gegenüber der rechnerisch korrekten Erwartung). Alle übrigen bis zum
STOPP geprüften Kriterien (App-Start, Prüfungsumfang 82/120,
Einzel-/Mehrfachauswahl, Ein-Punkt-Bewertung, Zwei-Punkte-Bewertung
bei mehreren richtigen Antworten, Teilpunkt, Pause/Fortsetzen,
unbeantwortete Fragen, Konsolenstatus, Speicherwiederherstellung)
waren PASS. Die Prüfschritte H (Desktop/Mobil) und der vollständige
UI-Durchlauf von Fehleranalyse/Fehlertraining wurden wegen des
sofortigen STOPP nach Fehlerregel nicht mehr durchgeführt.

Es wurde keine Codekorrektur vorgenommen. Kein Commit. Kein Push.
