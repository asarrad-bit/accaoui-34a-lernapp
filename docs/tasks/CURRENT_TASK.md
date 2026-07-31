# Verbindlicher aktueller Task

Task-ID: v27.35e
Status: AUTHORIZED
Autorisiert: JA
Titel: Regressionstest der schriftlichen Prüfung
Funktionaler Ausgangsstand: v27.35d
Erwarteter Ausgangscommit: `260e6527208769f18018d1db6e6e3b7fbe9d7d7e`
Erlaubte Dateien: `docs/WRITTEN_EXAM_REGRESSION_V2735E.md`
Commit erlaubt: NEIN
Push erlaubt: NEIN

## Ziel

Die schriftliche Prüfung nach v27.35d vollständig regressionsprüfen. Es wird
keine neue Funktion entwickelt.

Dieser Schritt autorisiert nur den Testtask. Noch keine Browsertests
durchgeführt.

## Während der Testdurchführung verboten

- app.js
- index.html
- style.css
- patch-v21.js
- questions.json
- oral-exam.js
- tools/preflight.py
- alle Supabase-, SQL- und Migrationsdateien
- alle weiteren Dateien

## Akzeptanzkriterien

1. App startet ohne neue Konsolenfehler.
2. Vollsimulation enthält exakt 82 Fragen.
3. Maximalpunktzahl beträgt exakt 120 Punkte.
4. Ein- und Mehrfachauswahl funktionieren.
5. Ein- und Zwei-Punkte-Fragen werden korrekt bewertet.
6. Teilrichtige Zwei-Punkte-Antworten ergeben korrekt einen Punkt.
7. Pause und Fortsetzen erhalten Fragenreihenfolge, aktuelle Position,
   bereits gewählte Antworten und bisherigen Punktestand.
8. Unbeantwortete Fragen und Fehlertraining zeigen nur die tatsächlich
   vorgesehenen Fragen.
9. Endauswertung, richtige, falsche und unbeantwortete Antworten sowie
   Gesamtpunkte sind rechnerisch konsistent.
10. Desktop und Mobilansicht ca. 390 × 844 sind benutzbar.
11. Kein horizontaler Überlauf und keine Überlagerungen.
12. localStorage wird nach dem Test vollständig restauriert.
13. Es wird ausschließlich der Testbericht erstellt.

## Fehlerregel

Wird eine Regression gefunden: sofort STOPP, Fehler im Testbericht exakt
dokumentieren, keine Codekorrektur durchführen, keinen zusätzlichen
Dateiumfang öffnen.

## Verbindlich festhalten

- Kein Folgetask ist ausgewählt.
- Kein Task darf aus Versionsfolge, Erinnerung oder früheren Chats
  abgeleitet werden.
- Ein neuer Task muss ausdrücklich durch Projekteigentümer,
  verbindlichen Projektchat und `CURRENT_TASK` autorisiert werden.
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
