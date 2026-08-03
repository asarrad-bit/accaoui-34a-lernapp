# Verbindlicher aktueller Task

Task-ID: NONE
Status: BLOCKED
Autorisiert: NEIN
Titel: Kein Task autorisiert
Letzter abgeschlossener funktionaler Stand: v27.35g
Abschlusscommit: `f5f261fee67fc17c170ee714ae23761ff1668f17`
Erlaubte Dateien: KEINE
Commit erlaubt: NEIN
Push erlaubt: NEIN

## Abgeschlossener funktionaler Stand v27.35g

Die Punkteberechnung der schriftlichen Prüfung wurde korrigiert: eine vollständig richtige Antwort ergibt stets die volle hinterlegte Punktzahl; eine zulässige Teilantwort bei einer Zwei-Punkte-Frage mit mindestens zwei richtigen Optionen ergibt exakt 1 Punkt; jede falsch ausgewählte Option ergibt 0 Punkte.

Bestätigte Ergebnisse:

- 82 Fragen, 120 Maximalpunkte.
- Alle 13 zuvor betroffenen Fragen (`straf_009`, `bgb_009`, `waffen_004`, `straf_004`, `v23_roso_007`, `technik_004`, `straf_006`, `bgb_012`, `bgb_004`, `straf_013`, `bgb_006`, `uvv_004`, `uvv_008`) liefern bei vollständig korrekter Beantwortung jeweils exakt 2/2 Punkte.
- Die im v27.35e-Bericht verwendete Testkonstellation ergibt jetzt exakt 114/120 statt vormals 101/120.
- Alle 82 Fragen vollständig korrekt beantwortet ergeben jetzt exakt 120/120.
- Pause/Fortsetzen: PASS.
- Fehleranalyse: PASS.
- Fehlertraining: PASS.
- Desktop: PASS.
- Mobil ca. 390 × 844: PASS.
- Keine neuen Konsolenfehler.
- `localStorage` und `sessionStorage` nach den Tests vollständig restauriert.

Testbericht: `docs/WRITTEN_EXAM_SCORING_FIX_V2735G.md`. Funktionaler Abschlusscommit: `f5f261fee67fc17c170ee714ae23761ff1668f17`.

Vor der funktionalen Umsetzung wurde ein getrennter, nichtfunktionaler Implementierungs-Gate-Korrekturschritt (Commit `bbe5f6ea5366e026327c3fc0c866e1ef37ead6f0`) durchgeführt, der ausschließlich den Kontinuitäts-Checker und die vier Steuerungsdokumente ergänzte und im Arbeitsbaum ausschließlich `app.js` sowie `docs/WRITTEN_EXAM_SCORING_FIX_V2735G.md` freigab.

Der bestehende v27.35e-FAIL-Bericht `docs/WRITTEN_EXAM_REGRESSION_V2735E.md` bleibt unverändert als historische Fehlerdokumentation erhalten.

`v27.35f` bleibt ausschließlich für die später vorgemerkte Wettbewerbsbeobachtungsnotiz reserviert. `v27.35f` ist nicht autorisiert und wird jetzt nicht bearbeitet.

## Verbindliche Sperre

- Kein neuer funktionaler oder nichtfunktionaler Task wird automatisch ausgewählt oder autorisiert.
- Die Auswahl eines weiteren Tasks erfolgt ausschließlich durch den Projekteigentümer, den verbindlichen Projektchat und diese Datei.
- Aus Versionsfolgen, früheren Chats oder Erinnerung darf kein weiterer Task abgeleitet werden.
- Commit und Push bleiben bis zu einer gesonderten ausdrücklichen Freigabe gesperrt.

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
