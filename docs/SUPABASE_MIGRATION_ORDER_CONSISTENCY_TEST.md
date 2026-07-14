# Accaoui §34a Lern-App – Supabase-Migrationsprüfung

Stand: v27.22a

## Prüftool

`tools/check-supabase-migrations.py`

## Geprüft wird

- Grundschema existiert
- RLS-Migration existiert
- Grundschema steht vor der RLS-Migration
- acht MVP-Tabellen sind vorhanden
- RLS ist für alle acht Tabellen aktiviert
- genau 17 Policies sind vorhanden
- alle Policies verwenden bekannte Tabellen
- zwei Rollen-Helper sind vorhanden
- alle Policies sind auf `authenticated` begrenzt
- `auth.uid()` wird verwendet
- keine sensitiven Schlüssel oder Datenbank-URLs im SQL-Code

## Sicherheitsgrenze

Die Prüfung ist lokal und statisch.

Sie führt keine Migration aus und ersetzt noch keinen Test in einer echten Supabase-Testdatenbank.

Status: vorbereitet
