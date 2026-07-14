# Accaoui §34a Lern-App – Supabase MVP RLS-Migration-Test

Stand: v27.21b
Prüfdatei: supabase/migrations/20260710_v2721a_mvp_rls_policies.sql

## Testumfang

Statische Prüfung der vorbereiteten SQL-Datei.

Keine Live-Ausführung in Supabase oder PostgreSQL.

## Erwartete Struktur

- Version: v27.21a
- zwei Rollen-Helper-Funktionen
- 17 RLS-Policies
- Zugriff nur für authenticated
- Teilnehmerzugriff über auth.uid()
- eigene Prüfungsergebnisse und Antworten
- Zertifikate für Teilnehmer nur lesbar
- Admin-Profile nur durch Admin verwaltbar
- keine direkte Teilnehmer-Profiländerung
- keine Keys oder Teilnehmerdaten

## Sicherheitsgrenzen

Dieser Test bestätigt nur die Dateistruktur.

Noch nicht geprüft:

- SQL-Ausführung in einer echten Datenbank
- tatsächliches Verhalten der Policies
- Rollen- und Benutzerintegration
- Performance unter Live-Bedingungen

Vor einer Live-Aktivierung folgen:

1. SQL-Syntaxprüfung
2. Testprojekt-Migration
3. RLS-Tests mit Teilnehmer-, Dozent- und Admin-Konten
4. Sicherheitsprüfung
5. dokumentierte Freigabe

Status: statisch geprüft und dokumentiert
