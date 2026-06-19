# Accaoui §34a Lern-App – Supabase Config Ladeweg-Audit

Stand: v26.5e

Ziel: Prüfen und dokumentieren, wie die Supabase-Konfiguration später sicher in die App geladen werden soll, ohne echte Keys im Repository zu speichern.

## 1. Aktueller Stand

Aktuell lädt index.html folgende Hauptskripte:

1. app.js
2. patch-v21.js
3. data/oral-question-bank.js
4. data/oral-sheets-bank.js
5. oral-sheets.js
6. oral-sheets-v23.js
7. oral-exam.js

Eine Supabase-Konfiguration wird aktuell noch nicht geladen.

## 2. Vorhandener Platzhalter

Seit v26.5c existiert:

data/supabase-config.example.js

Diese Datei enthält nur Platzhalter:

1. YOUR-PROJECT
2. YOUR_PUBLIC_ANON_KEY

Es sind keine echten Keys enthalten.

## 3. Geschützte lokale Datei

Die spätere lokale Datei soll heißen:

data/supabase-config.local.js

Diese Datei ist über .gitignore geschützt und darf nicht committed werden.

## 4. Sicherheitsregel

Echte lokale Supabase-Werte dürfen niemals in diese Dateien:

1. app.js
2. index.html
3. patch-v21.js
4. questions.json
5. docs-Dateien
6. data/supabase-config.example.js

## 5. Späterer Ladeweg

Empfohlener späterer Ladeweg:

1. index.html lädt optional data/supabase-config.local.js
2. danach lädt index.html app.js
3. app.js prüft window.ACCAOUI_SUPABASE_CONFIG
4. wenn keine Config vorhanden ist, bleibt die App im lokalen Modus
5. wenn Config vorhanden ist, kann später Supabase initialisiert werden

Wichtig: In v26.5e wird dieser Ladeweg nur dokumentiert, noch nicht technisch eingebaut.

## 6. Kein service_role-Key

Der service_role-Key darf niemals im Frontend stehen.

Erlaubt für spätere Browser-App ist nur:

1. Supabase URL
2. Supabase anon/public key

Auch der anon key ist nur sicher, wenn RLS korrekt aktiv ist.

## 7. Empfehlung für nächste technische Version

Nächster sinnvoller technischer Schritt:

v26.5f oder v26.6a – optionaler Config-Loader im lokalen Modus

Dieser Loader darf:

1. prüfen, ob window.ACCAOUI_SUPABASE_CONFIG existiert
2. Platzhalter erkennen
3. Warnung in der Konsole ausgeben
4. App weiterhin lokal starten

Dieser Loader darf noch nicht:

1. Supabase-SDK laden
2. echte Verbindung herstellen
3. Login erzwingen
4. echte Datenbankabfragen ausführen

## 8. Status

Status v26.5e: Config-Ladeweg geprüft und dokumentiert. Keine App-Code-Änderung. Keine echte Supabase-Verbindung.
