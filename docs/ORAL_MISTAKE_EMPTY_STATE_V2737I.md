# v27.37i – Leerzustand des mündlichen Fehlertrainers

## Ursache

Der führende Renderer `showOralMistakeTrainingV2340()` las bei einer leeren
Fehlerliste zwar korrekt `[]` aus dem bestehenden Storage, zeigte aber nur
optional einen kleinen Hinweis und kehrte anschließend zurück. Dadurch wurde
`.main-content` nicht neu gerendert. Nach dem sicheren Markieren des letzten
Fehlers konnten deshalb die zuvor gerenderte Fehlerkarte und ihr alter Zähler
sichtbar bleiben.

## Reparatur

Der Leerzweig des bestehenden v23.4.0-Mündliche-Fehlertrainer-Blocks ersetzt
den Inhalt von `.main-content` jetzt sofort durch einen echten Leerzustand.
Der vorhandene kleine Hinweis bleibt ergänzend bestehen, ersetzt das Rendern
aber nicht. Es gibt keine automatische Navigation und kein Wiederanlegen eines
gelöschten Fehlers.

## Leerzustand

Der Leerzustand enthält:

- `Mündliche Fehler`
- `Keine offenen mündlichen Fehler`
- `Alle aktuell gespeicherten mündlichen Fehler wurden bearbeitet.`
- die Aktion `Zur Fehlerübersicht`
- die Aktion `Zurück zum Dashboard`

Eine alte Fehlerkarte und der Fehlerzähler werden im Leerzustand nicht
gerendert.

## Verhalten bei 0, 1 und mehreren Fehlern

- Bei 0 Fehlern erscheint unmittelbar der Leerzustand.
- Bei 1 Fehler bleibt die vorhandene Karte mit dem Zähler 1 sichtbar.
- Bei mehreren Fehlern bleiben alle Karten und der korrekte Zähler sichtbar.
- Wird der erste von mehreren Fehlern als sicher markiert, wird nur dieser
  Eintrag entfernt und die verbleibende Liste mit reduziertem Zähler neu
  gerendert.
- Wird der letzte Fehler als sicher markiert, erscheint sofort der
  Leerzustand.
- Reveal, Collapse über `Noch üben` und `Als sicher markieren` verwenden
  weiterhin die bestehende v23.4.0-Logik.

## Storage-Semantik

Der einzige verwendete Schlüssel bleibt
`accaoui_oral_exam_mistakes_v2324`. Nach dem Entfernen des letzten Fehlers
enthält er exakt `[]`. Beim erneuten Öffnen mit `[]` entsteht kein neuer
Fehler und kein zusätzlicher Storage-Key. Beschädigtes JSON behält das
bisherige fail-safe Verhalten: Es wird für die Anzeige wie eine leere Liste
behandelt, aber weder migriert noch automatisch überschrieben.

## Ausdrückliche Ausschlüsse

P3 ist ausdrücklich ausgeschlossen. Die Herkunftsbezeichnung
`15-Minuten-Simulation` wird nicht verändert. Mündliche Fragen,
Prüfungsbögen, Timer und Bewertung bleiben unverändert. Es gibt keine Änderung
an Auth, Session, Zugang, Config, SDK, SQL oder Migrationen. Supabase bleibt
NICHT LIVE.

## Exakter Vier-Dateien-Scope

Die Implementation umfasst ausschließlich:

1. `oral-exam.js`
2. `tools/check-oral-mistake-empty-state-v2737i.py`
3. `docs/ORAL_MISTAKE_EMPTY_STATE_V2737I.md`
4. `tools/preflight.py`

`oral-exam.js` wird ausschließlich innerhalb des bestehenden
v23.4.0-Mündliche-Fehlertrainer-Blocks geändert. Alle eingefrorenen Produkt-,
Test- und historischen Prüfdateien bleiben unverändert.
