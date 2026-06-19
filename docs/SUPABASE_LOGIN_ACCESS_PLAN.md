# Accaoui §34a Lern-App – Supabase Login- und Teilnehmerzugang-Plan

Stand: v26.3a
Repository: asarrad-bit/accaoui-34a-lernapp

## Ziel

Teilnehmer sollen sich später einloggen und nur dann Zugriff auf die Lern-App bekommen, wenn ein gültiger Kurszugang besteht.

## Strategische Entscheidung

Die App wird nicht sofort vollständig auf Supabase umgestellt.

Priorität:

1. Login / Auth
2. Teilnehmerprofil
3. Kursfreischaltung
4. Ablaufdatum / Zugangsdauer
5. Fortschritt pro Nutzer speichern

Nicht zuerst:

1. Fragenbank aus Supabase laden
2. Admin-Import der Fragen
3. vollständige Cloud-Migration

Begründung: Die lokale App ist stabil. Der nächste Business-Wert ist Zugangskontrolle für echte Teilnehmer.

## Zugriffsregel

Ein Teilnehmer bekommt Zugriff, wenn:

1. Profil existiert
2. Rolle ist participant
3. aktive Kurseinschreibung existiert
4. Kurs ist aktiv
5. Zugang ist nicht abgelaufen
6. Teilnehmer ist nicht gesperrt

Logische Regel:

profiles.role = participant
course_enrollments.enrollment_status = active
courses.is_active = true
expires_at ist leer oder liegt in der Zukunft
courses.ends_at ist leer oder noch nicht erreicht

## Rollen

| Rolle | DB-Wert | Zweck |
|------|---------|-------|
| Teilnehmer | participant | Lernen, Prüfungen, Lernkarten, eigener Fortschritt |
| Dozent | instructor | später Fortschritte eigener Kurse sehen |
| Admin | admin | Kurse, Teilnehmer, Laufzeiten, Sperren, Support |

## Kursdauer

Zwei Ebenen sind vorgesehen:

1. Kursdauer über courses.starts_at und courses.ends_at
2. individuelle Freischaltung über course_enrollments.expires_at

blocked überschreibt immer active.
expired bedeutet kein Zugriff auf Lernmodule.

## Minimaler technischer Start

1. Supabase-Projekt prüfen
2. Auth aktivieren
3. Tabellen profiles, courses, course_enrollments nutzen
4. Basis-RLS aktivieren
5. Login-UI in der App vorbereiten
6. nach Login Zugang prüfen
7. bei gültigem Zugang Dashboard anzeigen
8. bei ungültigem Zugang Sperrseite anzeigen

## App-Verhalten

Gültiger Teilnehmer:
Dashboard und Lernmodule werden freigegeben.

Abgelaufener Zugang:
Ihr Kurszugang ist abgelaufen. Bitte wenden Sie sich an Accaoui Bildung.

Gesperrter Zugang:
Ihr Zugang ist aktuell gesperrt. Bitte wenden Sie sich an die Verwaltung.

Kein Kurs zugeordnet:
Ihrem Konto ist aktuell kein aktiver Kurs zugeordnet. Bitte wenden Sie sich an Accaoui Bildung.

## Entscheidung Gastmodus

Empfehlung:

1. Teilnehmer: Login erforderlich
2. Admin/Dozent: Login erforderlich
3. öffentliche Demo später separat möglich

Begründung: Für bezahlte Teilnehmer, Kursdauer und Zugriffskontrolle ist Login sauberer als ein offener Gastmodus.

## Nächste Reihenfolge

1. v26.3b – Supabase-Dokumente gegen aktuellen Stand prüfen
2. v26.3c – Login-UI-Konzept erstellen
3. v26.3d – Auth-State und Zugriffssperre lokal vorbereiten
4. v27.0 – erste echte Supabase-Anbindung

## Nicht sofort umsetzen

1. Fragenimport aus Supabase
2. vollständiges Admin-Dashboard
3. Dozentenansicht
4. Zahlungsstatus
5. Zertifikate
6. mehrere Standorte oder Mandanten

Status v26.3a: Plan erstellt, noch kein App-Code geändert.
