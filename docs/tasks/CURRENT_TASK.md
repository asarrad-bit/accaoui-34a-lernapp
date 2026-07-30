# Verbindlicher aktueller Task

Task-ID: v27.35d
Status: AUTHORIZED
Autorisiert: JA
Funktionaler Ausgangsstand: v27.35b
Letzter abgeschlossener Kontrollschritt: v27.35c
Erwarteter Ausgangscommit: `e4b6929af552e4245290d3eb5db97815365162e6`
Erlaubte Dateien: `app.js`, `index.html`, `style.css`
Commit erlaubt: NEIN
Push erlaubt: NEIN

## Ziel von v27.35d

Lernmodus und Lernkarten für Teilnehmer klarer unterscheiden.

- Lernmodus als echte Wissensabfrage klar erklären
- Lernkarten als Selbsteinschätzung klar erklären
- Active-Recall-Führung verständlicher machen
- Ergebnis- und Hinweistexte zwischen beiden Modi vereinheitlichen
- keine neue Lernstrategie-Engine
- keine neue Speicherung
- keine neuen Storage-Keys
- keine Fragenänderung
- keine Supabase-, SQL-, Datenbank- oder Netzwerkänderung

## Akzeptanzkriterien

1. Lernmodus und Lernkarten werden sprachlich eindeutig getrennt.
2. Lernmodus erklärt: erst selbst beantworten, danach Lösung prüfen.
3. Lernkarten erklären: Antwort selbst einschätzen und als sicher oder noch üben markieren.
4. Keine zusätzliche oder doppelte Empfehlungskarte.
5. Bestehende Prüfungs-, Lern-, Lernkarten- und Speicherlogik bleibt erhalten.
6. Keine neue Speicherung und keine neuen Storage-Keys.
7. Desktop und Mobil bleiben sauber nutzbar.
8. Nur minimale gezielte Änderungen.

## Tests

- `node --check app.js`
- `git diff --check`
- `python tools/preflight.py` mit kontrollierter Freigabe
- Browser-Test Lernmodus
- Browser-Test Lernkarten
- Browser-Test Dashboard
- Browser-Test Mobilansicht

## Verbotene Dateien

- `questions.json`
- `AGENTS.md`
- `docs/**`
- `tools/**`
- Supabase-, SQL-, Datenbank- und Migrationsdateien

## Verbindliche Sperre

- Ausschließlich v27.35d und ausschließlich die Dateien `app.js`,
  `index.html` und `style.css` sind für die funktionale Umsetzung
  freigegeben.
- Kein Folgeschritt nach v27.35d wird automatisch gewählt oder autorisiert.
- Der übernächste Task darf ausschließlich durch den Projekteigentümer
  und den verbindlichen Projektchat ausgewählt werden.
- Aus Versionsfolgen, früheren Chats oder Erinnerung darf kein weiterer
  Task abgeleitet werden.
- Commit und Push bleiben bis zu einer gesonderten ausdrücklichen
  Freigabe gesperrt.

## Abgeschlossener nichtfunktionaler Kontrollschritt v27.35c

Die Projektsteuerung wurde von Task-ID NONE, Status BLOCKED und
Autorisiert NEIN auf den einzigen autorisierten Task v27.35d
umgestellt und im Kontinuitäts-Checker gegen eine falsche Task-ID,
einen falschen Status, Autorisiert NEIN, einen anderen funktionalen
Ausgangsstand, einen anderen Ausgangscommit, zusätzliche oder andere
erlaubte Dateien, Commit erlaubt JA, Push erlaubt JA und die
automatische Auswahl eines weiteren Tasks abgesichert.

Der funktionale Ausgangsstand bleibt v27.35b. Es wurde keine App-,
Funktions-, Vertrags-, Adapter-, Datenbank-, Supabase-, Fragen-, UI-
oder Migrationsdatei verändert. `app.js`, `index.html` und `style.css`
wurden in v27.35c nicht verändert.

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
