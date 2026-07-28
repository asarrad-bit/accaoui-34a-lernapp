# Verbindlicher aktueller Task

Task-ID: v27.35b
Status: AUTHORIZED
Autorisiert: JA
Funktionaler Ausgangsstand: v27.34b
Letzter abgeschlossener Kontrollschritt: v27.35a
Erwarteter Ausgangscommit: `62947209611c17b5a700fb78cfcfa785f055b2f3`
Erlaubte Dateien: `app.js`
Commit erlaubt: NEIN
Push erlaubt: NEIN

## Ziel von v27.35b

Auf dem Dashboard aus vorhandenen lokalen Lernständen genau einen
sinnvollen nächsten Lernschritt anzeigen.

## Priorität des nächsten Lernschritts

1. angefangene Prüfung, Lerneinheit oder Lernkarten fortsetzen
2. vorhandene Fehlerfragen trainieren
3. schwächstes ausreichend belegtes Sachgebiet üben
4. unbekannte Lernkarten wiederholen
5. andernfalls neue Prüfung starten

## Verbindliche Grenzen für v27.35b

- ausschließlich `app.js`
- keine HTML-, CSS- oder `questions.json`-Änderung
- keine Supabase-, SQL-, Datenbank- oder Netzwerkänderung
- keine neue Speicherung
- vorhandene localStorage-Daten nur defensiv lesen
- ungültige oder fehlende Daten sicher ignorieren
- keine Zusatzoptimierungen

## Verbindliche Sperre

- Ausschließlich v27.35b und ausschließlich die Datei `app.js` sind für die funktionale Umsetzung freigegeben.
- Kein Folgeschritt nach v27.35b wird automatisch gewählt oder autorisiert.
- Der übernächste Task darf ausschließlich durch den Projekteigentümer und den verbindlichen Projektchat ausgewählt werden.
- Aus Versionsfolgen, früheren Chats oder Erinnerung darf kein weiterer Task abgeleitet werden.
- Commit und Push bleiben bis zu einer gesonderten ausdrücklichen Freigabe gesperrt.

## Abgeschlossener nichtfunktionaler Kontrollschritt v27.35a

Die Projektsteuerung wurde von Task-ID NONE, Status BLOCKED und
Autorisiert NEIN auf den einzigen autorisierten Task v27.35b
umgestellt und im Kontinuitäts-Checker gegen eine falsche Task-ID,
einen falschen Status, Autorisiert NEIN, einen anderen funktionalen
Ausgangsstand, einen anderen Ausgangscommit, zusätzliche oder andere
erlaubte Dateien, Commit erlaubt JA, Push erlaubt JA und die
automatische Auswahl eines weiteren Tasks abgesichert.

Der funktionale Ausgangsstand bleibt v27.34b. Es wurde keine App-,
Funktions-, Vertrags-, Adapter-, Datenbank-, Supabase-, Fragen-, UI-
oder Migrationsdatei verändert. app.js wurde in v27.35a nicht
verändert.

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
