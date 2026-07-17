# Prüfungsergebnishistorie-Fixture-Test

Stand: v27.29g

Status: lokal ausführbar, ohne Live-Daten oder Netzwerk

## Ziel

Normalizer und Aggregator der sicheren Prüfungsergebnisliste
werden mit festen lokalen Beispieldaten tatsächlich ausgeführt.

## Werkzeug

`tools/test-supabase-exam-history-fixtures.js`

Ausführung:

`node tools/test-supabase-exam-history-fixtures.js`

Der Test wird zusätzlich durch `tools/preflight.py` ausgeführt.

## Geprüfte Normalizer-Fälle

- gültige Ergebniszeile
- Umwandlung von `total_count` in eine Zahl
- Ausschluss unbekannter und privater Felder
- falscher Bestehensstatus
- falsche Maximalpunkte
- gültige Ergebnisliste
- doppelte Prüfungsversuchs-ID
- inkonsistentes `total_count`
- `total_count` kleiner als die Zeilenanzahl
- stabiler leerer Zustand

## Geprüfte Aggregator-Fälle

- Seitenanzahl
- bestanden und nicht bestanden
- Seitenbestwert
- Seitendurchschnitt
- Seitenbestehensquote
- neuester Seiteneintrag
- stabiler leerer Zustand
- geschlossene Ablehnung ungültiger Daten
- keine Ableitung globaler Ergebniszahlen

## Sicherheitsgrenze

Der Test verwendet:

- ausschließlich feste lokale Beispieldaten
- einen isolierten Node-VM-Kontext
- keinen Supabase-Client
- keinen echten RPC-Aufruf
- kein Netzwerk
- keine echten Teilnehmerdaten
- keine Antworten oder Lösungsschlüssel
- keine sichtbare UI
