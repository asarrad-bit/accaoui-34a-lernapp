# Accaoui §34a Lern-App – Supabase-Fail-Safe-Status-Test

Stand: v26.15b

Ziel: Prüfen, ob der Supabase-Adapter klare Fail-Safe-Statuswerte liefert, ohne Supabase live zu schalten.

## 1. Testgegenstand

Getestet wurde:

1. data/supabase-client-adapter.js
2. getSupabaseFailSafeState()
3. getAdapterHealthState()
4. failSafeStatus
5. isFailSafeSafe
6. Normalmodus mit Live-Schalter false
7. Dry-Run mit Live-Schalter true

## 2. Normalmodus

Im Normalmodus gilt:

1. window.ACCAOUI_SUPABASE_LIVE_ENABLED ist nicht aktiv.
2. Es gibt keine echte Supabase-Config.
3. Es gibt kein Supabase-SDK.
4. Es wird kein Client erzeugt.
5. Es wird keine Session geprüft.

Erwartetes und bestätigtes Ergebnis:

1. Adapter-Version: v26.15a
2. live: false
3. failSafeStatus: local_mode_safe
4. isFailSafeSafe: true
5. isSupabaseLive: false
6. canCreateClient: false
7. canCheckSession: false

## 3. Dry-Run mit Live-Schalter true

Im Dry-Run wurde der Live-Schalter testweise aktiviert:

window.ACCAOUI_SUPABASE_LIVE_ENABLED = true

Erwartetes und bestätigtes Ergebnis:

1. live: true
2. failSafeStatus: live_switch_enabled_but_config_and_sdk_missing
3. isFailSafeSafe: true
4. isSupabaseLive: false
5. canCreateClient: false
6. canCheckSession: false

Danach wurde der Live-Schalter zurückgesetzt:

window.ACCAOUI_SUPABASE_LIVE_ENABLED = false

Erwartetes und bestätigtes Ergebnis:

1. reset live: false

## 4. Sicherheitsbewertung

Der Test ist bestanden.

Bedeutung:

1. Der Adapter meldet klar, warum Supabase nicht live geht.
2. Ohne Live-Schalter bleibt Supabase gesperrt.
3. Auch mit testweise aktivem Live-Schalter bleibt Supabase gesperrt, wenn Config und SDK fehlen.
4. Es wird kein Supabase-Client erzeugt.
5. Es wird keine Session geprüft.
6. Es gibt keinen Login-Zwang.
7. Die App bleibt lokal nutzbar.

## 5. Status

Status v26.15b: Supabase-Fail-Safe-Status-Test dokumentiert. Der Adapter liefert klare Sicherheitszustände und bleibt ohne Config, SDK und Client-Erzeugung sicher im lokalen Modus.
