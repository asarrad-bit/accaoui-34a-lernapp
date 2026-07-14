# Accaoui §34a Lern-App – Supabase Client Bootstrap Test

Stand: v27.23b
Prüfdatei: data/supabase-client-bootstrap.js

## Ziel

Der vorbereitete Supabase-Client-Bootstrap bleibt im normalen lokalen Betrieb vollständig inaktiv.

## Sicherheitsvoraussetzungen

Eine Client-Erstellung ist nur möglich, wenn gleichzeitig:

1. der Supabase-Adapter vorhanden ist
2. eine gültige öffentliche Konfiguration vorhanden ist
3. das Supabase-SDK geladen ist
4. `ACCAOUI_SUPABASE_LIVE_ENABLED === true` gesetzt ist
5. `ACCAOUI_SUPABASE_CLIENT_INIT_CONFIRMED === true` gesetzt ist
6. `initializeClient()` ausdrücklich aufgerufen wird

## Lokaler Standardzustand

Erwartet:

- `status: "live_switch_disabled"`
- `hasClient: false`
- `canInitializeClient: false`
- `isManualOnly: true`
- `autoInitializationAttempted: false`

## Blockierter Initialisierungsaufruf

Auch bei:

`window.ACCAOUI_SUPABASE_BOOTSTRAP.initializeClient()`

darf ohne vollständige Freigabe kein Client erstellt werden.

Erwartet:

- `hasClient: false`
- keine Supabase-Verbindung
- kein Login-Zwang
- lokaler App-Betrieb bleibt erhalten

## Ladefolge

1. Supabase-Config-Loader
2. Supabase-Client-Adapter
3. Supabase-Client-Bootstrap
4. App

## Sicherheitsgrenze

Dieser Test verwendet keine echten Keys und keine echte Supabase-Verbindung.

Die tatsächliche Client- und Datenbankfunktion wird später ausschließlich in einer getrennten Testumgebung geprüft.

Status: statisch und lokal geprüft
