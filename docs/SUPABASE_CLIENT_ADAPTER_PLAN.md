# Accaoui §34a Lern-App – Supabase Client Adapter Plan

Stand: v26.7a

Ziel: Vor der echten Supabase-Anbindung festlegen, wie die App später sauber mit Supabase spricht, ohne bestehende Lern-, Prüfungs- und Pausenlogik zu beschädigen.

## 1. Grundsatz

Supabase soll später nicht direkt überall in app.js verwendet werden.

Stattdessen soll eine klare Adapter-Schicht entstehen.

Ziel:

1. App-Logik bleibt stabil.
2. Supabase-Code bleibt gekapselt.
3. Auth, Profil, Kurszugang und Fortschritt werden getrennt behandelt.
4. Lokaler Modus bleibt als Fallback möglich.

## 2. Aktueller Stand

Aktuell vorhanden:

1. lokales Auth-Guard-Gerüst
2. lokale Auth-Testzustände
3. Auth-Hinweisseiten
4. Config-State-Check
5. optionaler lokaler Config-Loader
6. erfolgreicher Loader-Test mit Fake-Config

Noch nicht vorhanden:

1. Supabase-SDK
2. echte Supabase-Verbindung
3. echter Login
4. echte Profilabfrage
5. echte Kursabfrage
6. Fortschritt pro user_id

## 3. Spätere Adapter-Aufgaben

Ein späterer Supabase-Adapter soll diese Aufgaben kapseln:

1. Supabase-Konfiguration prüfen
2. Supabase-Client erzeugen
3. aktuelle Session prüfen
4. Login durchführen
5. Logout durchführen
6. Teilnehmerprofil laden
7. Kursfreischaltung prüfen
8. Ablaufdatum prüfen
9. Sperrstatus prüfen
10. Fortschritt speichern und laden

## 4. Empfohlene spätere Funktionsnamen

Mögliche spätere Funktionen:

1. createSupabaseClient()
2. getSupabaseClientState()
3. getCurrentSupabaseSession()
4. signInParticipant()
5. signOutParticipant()
6. loadParticipantProfile()
7. loadParticipantEnrollment()
8. getParticipantAccessState()
9. saveUserProgress()
10. loadUserProgress()

## 5. Klare Grenze zur bestehenden App

Die bestehende App soll später nur mit einem Ergebnis arbeiten:

accessState

Beispiel:

1. isAllowed: true
2. status: active
3. role: participant
4. courseId: ...
5. expiresAt: ...

Oder bei Sperre:

1. isAllowed: false
2. status: blocked
3. message: Zugang gesperrt

Die Lern-App muss nicht wissen, wie Supabase intern arbeitet.

## 6. Sicherheitsregeln

Niemals im Frontend verwenden:

1. service_role key
2. Datenbank-Passwort
3. JWT secret
4. Admin-Schlüssel
5. private Server-Schlüssel

Erlaubt später nur:

1. Supabase URL
2. Supabase anon/public key

Voraussetzung:

1. RLS aktiv
2. Default-Deny
3. klare Policies
4. Teilnehmer sehen nur eigene Daten

## 7. Lokaler Modus bleibt erhalten

Wenn keine Supabase-Konfiguration vorhanden ist:

1. App startet weiter lokal
2. Auth-Guard-Testmodus bleibt nutzbar
3. keine Verbindung wird versucht
4. keine Fehlermeldung für Teilnehmer

## 8. Spätere technische Reihenfolge

Empfohlene Reihenfolge:

1. Adapter-Datei planen
2. Supabase-SDK-Ladeweg prüfen
3. Client-Erzeugung mit Config-State koppeln
4. Session-Abfrage vorbereiten
5. Login-UI mit Auth-State verbinden
6. Profil- und Kurszugang abfragen
7. Fortschritt pro Nutzer speichern

## 9. Nicht in v26.7a

Noch nicht umsetzen:

1. Supabase-SDK einbinden
2. echte Verbindung herstellen
3. echte Login-Daten verwenden
4. echte Datenbankabfragen ausführen
5. App-Zugang erzwingen

## 10. Status

Status v26.7a: Supabase-Client-Adapter geplant. Noch keine echte Supabase-Verbindung, kein SDK, keine echten Keys.
