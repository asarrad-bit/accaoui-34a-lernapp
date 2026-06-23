# Accaoui §34a Lern-App – Supabase SDK Ladeweg-Plan

Stand: v26.8a

Ziel: Vor der echten Supabase-Anbindung festlegen, wie das Supabase-SDK später sicher geladen und vom Adapter genutzt werden soll.

## 1. Grundsatz

Das Supabase-SDK wird noch nicht eingebaut.

In v26.8a wird nur geplant:

1. wo das SDK später geladen wird,
2. wie der Adapter darauf zugreift,
3. wann ein Client erzeugt werden darf,
4. wann die App im lokalen Modus bleiben muss.

## 2. Aktueller Stand

Aktuell vorhanden:

1. Supabase Config Safety Plan
2. Supabase Config Placeholder
3. optionaler lokaler Config-Loader
4. Supabase Config-State-Check
5. Supabase Client Adapter Stub
6. lokaler Adapter-Test

Noch nicht vorhanden:

1. Supabase-SDK
2. echter Supabase-Client
3. echte Auth-Session
4. echte Datenbankabfragen
5. echter Login-Zwang

## 3. Späterer SDK-Ladeweg

Empfohlener späterer Ablauf:

1. index.html lädt Supabase-SDK
2. index.html lädt data/supabase-client-adapter.js
3. index.html lädt app.js
4. app.js startet initAppBoot()
5. Adapter prüft Config-State
6. Adapter prüft, ob SDK vorhanden ist
7. nur bei gültiger Config und vorhandenem SDK wird später ein Client erzeugt

## 4. Sicherheitsregel

Ein Supabase-Client darf später nur erzeugt werden, wenn:

1. window.ACCAOUI_SUPABASE_CONFIG vorhanden ist,
2. URL nicht leer ist,
3. anonKey nicht leer ist,
4. keine Platzhalterwerte verwendet werden,
5. Supabase-SDK vorhanden ist,
6. kein service_role-Key verwendet wird.

## 5. Lokaler Fallback

Wenn eine Bedingung fehlt:

1. kein Fehler für Teilnehmer,
2. App bleibt im lokalen Modus,
3. Auth-Guard-Testmodus bleibt nutzbar,
4. Dashboard startet weiter normal,
5. Konsole zeigt nur einen klaren Status.

## 6. Adapter-Grenze

app.js soll später nicht direkt mit Supabase sprechen.

Die Kommunikation läuft über:

window.ACCAOUI_SUPABASE_ADAPTER

Der Adapter entscheidet:

1. local_mode
2. placeholder_config
3. config_available
4. sdk_missing
5. client_ready
6. auth_required
7. access_allowed
8. access_blocked
9. access_expired
10. no_course

## 7. Nicht in v26.8a

Noch nicht umsetzen:

1. Supabase-SDK einbinden
2. CDN-Link eintragen
3. echte URL eintragen
4. echten anon key eintragen
5. echten Client erzeugen
6. Login erzwingen
7. Datenbank abfragen

## 8. Status

Status v26.8a: Supabase-SDK-Ladeweg geplant. Keine App-Code-Änderung, kein SDK, keine Live-Verbindung, keine echten Keys.
