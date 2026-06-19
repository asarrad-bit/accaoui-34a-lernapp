# Accaoui §34a Lern-App – Supabase Konfigurations- und Sicherheitsplan

Stand: v26.5a

Ziel: Vor der echten Supabase-Anbindung festlegen, wie URL, Anon-Key, Rollen und Sicherheitsgrenzen sauber behandelt werden.

## 1. Grundsatz

Supabase wird erst angebunden, wenn die Konfiguration sicher vorbereitet ist.

In v26.5a wird noch keine Live-Verbindung eingebaut.

## 2. Erlaubt im Frontend

Im Frontend darf später nur verwendet werden:

1. Supabase Project URL
2. Supabase anon/public key

Der anon key ist für Browser-Apps vorgesehen, aber nur sicher, wenn Row Level Security aktiv ist.

## 3. Verboten im Frontend

Niemals in app.js, index.html oder andere öffentliche Dateien einbauen:

1. service_role key
2. Datenbank-Passwort
3. JWT secret
4. private API-Schlüssel
5. Admin-Zugangsdaten

## 4. Sicherheitsregel

Alle sensiblen Zugriffe müssen über Supabase RLS geschützt werden.

Grundsatz:

1. Tabellen nur mit RLS
2. Default-Deny
3. Zugriff nur über klare Policies
4. Teilnehmer sehen nur eigene Daten
5. Admin-Rechte nicht im Frontend erzwingen

## 5. Spätere Konfigurationsdatei

Für die spätere echte Verbindung wird eine eigene Datei empfohlen:

data/supabase-config.js

Diese Datei soll nur Platzhalter oder öffentliche Konfiguration enthalten.

Beispiel später:

SUPABASE_URL
SUPABASE_ANON_KEY

Noch nicht in v26.5a einbauen.

## 6. Empfohlene Reihenfolge

1. Supabase-Projekt prüfen
2. Tabellen prüfen
3. RLS prüfen
4. Auth aktivieren
5. Testnutzer anlegen
6. erst danach Frontend-Verbindung einbauen

## 7. Entscheidung für nächste Version

Nächster sinnvoller Schritt nach v26.5a:

v26.5b – Masterliste aktualisieren

Danach:

v26.5c – Supabase-Frontend-Konfigurationsplatzhalter vorbereiten, ohne echte Keys

## 8. Status

Status v26.5a: Sicherheitsplan erstellt. Noch keine echte Supabase-Verbindung. Keine Keys im Code.
