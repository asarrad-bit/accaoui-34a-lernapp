# Idempotenz-Operationstabelle

Stand: v27.31b

Status: SQL-Migration vorbereitet, nicht live ausgeführt

## Migration

`supabase/migrations/20260722_v2731b_exam_history_idempotency_operations.sql`

## Tabelle

`public.exam_history_idempotency_operations`

## Aufgabe

Die Tabelle bereitet eine spätere atomare und nicht rekursive
Idempotenzlösung für Prüfungshistorie-Snapshot- und
Zyklusregister-Mutationen vor.

## Abgesicherte Felder

- serverseitig bestimmter Nutzerbezug
- kanonische Operationsidentität
- externe UUID Version 4
- Bereich `snapshot` oder `cycle_registry`
- Mutation `write` oder `delete`
- serverseitig bestimmte Ressourcenidentität
- SHA-256-Payload-Fingerprint für Write
- Status `pending`, `completed` oder `failed`
- gespeicherter kanonischer Ergebnis-Payload
- stabiler Fehlercode ohne rohe Fehlerdetails
- Erstellungs-, Aktualisierungs- und Abschlusszeit

## Eindeutigkeit

Zwei Datenbankbedingungen verhindern doppelte Vorgänge:

1. vollständige `operation_identity`
2. Kombination aus Bereich, Mutation und externer UUID

Die Operationsidentität wird zusätzlich aus Bereich,
Mutation und UUID kanonisch gegengeprüft.

## Zustandsintegrität

- `pending`: noch kein Ergebnis und keine Abschlusszeit
- `completed`: Ergebnisobjekt und Abschlusszeit erforderlich
- `failed`: stabiler Fehlercode und Abschlusszeit erforderlich
- Write benötigt exakt 64 kleingeschriebene Hex-Zeichen
- Delete darf keinen Payload-Fingerprint enthalten
- Zeitwerte dürfen nicht vor der Erstellung liegen

## Zugriffsschutz

- Row Level Security aktiviert
- Row Level Security erzwungen
- alle Rechte für `public`, `anon` und `authenticated` entzogen
- keine Direktpolicy
- keine direkte App-Rollenfreigabe
- spätere Nutzung nur durch einen gesondert geprüften RPC

## Sicherheitsgrenze

- keine Live-Migration
- kein Browserzugriff
- kein Service-Role-Schlüssel
- keine echten Teilnehmerdaten
- kein neuer sichtbarer App-Bereich
