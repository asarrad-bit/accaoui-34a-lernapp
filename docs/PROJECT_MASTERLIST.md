# Accaoui §34a Lern-App – Projekt-Masterliste

Stand: v23.4.8 / Vorbereitung v23.4.9
Branch: refactor/oral-exam-module
Projektordner: C:\xampp\htdocs\accaoui\v4-dashboard

## 1. Arbeitsregel

Keine Blind-Fixes.

Immer in dieser Reihenfolge arbeiten:

1. Prüfen
2. Klein ändern
3. Browser testen
4. Preflight ausführen
5. Committen
6. Pushen

Vor jedem Commit ausführen:

python tools/preflight.py
git diff --check
git status --short

Nur committen, wenn:

1. Preflight bestanden
2. git diff --check keine Ausgabe zeigt
3. nur erlaubte Dateien geändert wurden
4. Browser-Test bestanden ist

## 2. Cursor-Regel

Cursor bekommt nur enge Aufträge.

Jeder Cursor-Auftrag enthält:

1. Ziel
2. erlaubte Dateien
3. verbotene Dateien
4. konkrete Änderung
5. was nicht geändert werden darf
6. Prüf-Befehle danach
7. kein Commit durch Cursor
8. keine Zusatzoptimierungen

Cursor darf nicht:

1. große Dateien komplett neu formatieren
2. Zeilenenden ändern
3. mehrere Bereiche gleichzeitig umbauen
4. Refactoring ohne Freigabe machen
5. test/ ändern, außer ausdrücklich erlaubt

## 3. Technische Schutzregeln

Nicht mehr auf großen Dateien verwenden:

sed -i

Betroffene große Dateien:

1. app.js
2. patch-v21.js
3. style.css
4. questions.json

Für gezielte Änderungen lieber Python mit Trefferkontrolle verwenden.

.editorconfig ist aktiv.

## 4. Aktive Hauptdateien

index.html lädt aktiv:

1. style.css
2. oral-exam.css
3. app.js
4. patch-v21.js
5. data/oral-question-bank.js
6. data/oral-sheets-bank.js
7. oral-sheets.js
8. oral-sheets-v23.js
9. oral-exam.js

Der Root-Ordner ist führend.

Der Ordner test/ ist aktuell nicht führend und darf nicht als Referenz genutzt werden.

## 5. Aktueller Versionsstand

v23.4.0
Mündlicher Fehlertrainer: stabiler Renderer.

v23.4.1
FRAGT JETZT Badge verbessert.

v23.4.2
Fehlerübersicht bereinigt.

v23.4.3
Kategorien in app.js und patch-v21.js normalisiert.

v23.4.4
Mündliche Prüfung in patch-v21.js normalisiert.

v23.4.5
Mündliche Datenquellen normalisiert.

v23.4.6
Schriftliche Fragenkategorien normalisiert.

v23.4.7
Kategorie-Audit-Skript erstellt.

v23.4.8
Preflight-Check erstellt.

## 6. Kanonische Kategorien

Feste Reihenfolge:

1. Recht der öffentlichen Sicherheit und Ordnung
2. Gewerberecht
3. Datenschutzrecht
4. Bürgerliches Gesetzbuch
5. Strafgesetzbuch und Strafverfahrensrecht
6. Unfallverhütungsvorschriften Wach- und Sicherungsdienste
7. Umgang mit Waffen
8. Umgang mit Menschen
9. Grundzüge der Sicherheitstechnik

Alte Begriffe dürfen nur noch als Mapping in normalizeCategoryName() stehen.

## 7. Prüfskripte

Kategorie-Audit:

python tools/audit-categories.py

Preflight:

python tools/preflight.py

Preflight ist Pflicht vor jedem Commit.

## 8. Mündlicher Fehlertrainer

Führend ist:

showOralMistakeTrainingV2340()

Alte Funktionen werden auf den neuen Renderer umgeleitet:

1. showOralMistakeTrainingV2324
2. showOralMistakeTrainingV2325
3. showOralMistakeTrainingV2326

Keine weiteren Hotfixes an alten mündlichen Fehlertrainer-Renderern.

## 9. Werkzeuge

Installiert:

1. Node.js v24.16.0
2. npm 11.13.0
3. Python 3.13.3

## 10. Nächste sinnvolle Aufgaben

1. Projektstruktur prüfen: aktive Dateien gegen alte/test Dateien.
2. Schriftlichen Prüfungsmodus vollständig testen.
3. Fragenbank erweitern und validieren.
4. Supabase-/Login-Architektur planen.
5. Datenschutz, Impressum, Nutzungsbedingungen vorbereiten.
6. Mündliche Prüfung später als Prüfermodus weiter ausbauen.

## 11. Start in neuem Chat

Bei neuem Chat zuerst diese Datei nennen:

docs/PROJECT_MASTERLIST.md

Dann ausführen:

git status
git log -1 --oneline
python tools/preflight.py
