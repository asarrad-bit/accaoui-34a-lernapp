# Accaoui §34a Lern-App – Supabase-Live-Schalter-Dry-Run-Test

Stand: v26.14a

Ziel: Prüfen, ob der vorbereitete Supabase-Live-Schalter testweise auf true gesetzt werden kann, ohne dass Supabase wirklich live geht.

## 1. Testgegenstand

Getestet wurde:

1. window.ACCAOUI_SUPABASE_LIVE_ENABLED
2. window.ACCAOUI_SUPABASE_ADAPTER.isSupabaseLiveEnabled()
3. window.ACCAOUI_SUPABASE_ADAPTER.getAdapterHealthState()
4. Client-Readiness im lokalen Modus
5. Rücksetzung des Live-Schalters auf false

## 2. Testablauf

In der Browser-Konsole wurde der Live-Schalter testweise aktiviert:

window.ACCAOUI_SUPABASE_LIVE_ENABLED = true

Danach wurde der Adapter-Health-State gelesen und anschließend der Schalter wieder deaktiviert:

window.ACCAOUI_SUPABASE_LIVE_ENABLED = false

## 3. Testergebnis

Erwartetes und bestätigtes Ergebnis:

1. Live enabled: true
2. status: local_access_granted
3. isSupabaseLive: false
4. isLiveEnabled: true
5. isLocalAccessAllowed: true
6. hasConfig: false
7. hasSdk: false
8. canCreateClient: false
9. canCheckSession: false
10. clientStatus: local_mode
11. clientReason: no_config_loaded
12. Live reset: false

## 4. Sicherheitsbewertung

Der Dry-Run ist bestanden.

Bedeutung:

1. Der Live-Schalter funktioniert technisch.
2. Der Schalter allein macht Supabase nicht live.
3. Ohne echte Config bleibt der Client blockiert.
4. Ohne SDK bleibt der Client blockiert.
5. Es wird kein Supabase-Client erzeugt.
6. Es wird keine Session geprüft.
7. Es gibt keinen Login-Zwang.
8. Die App bleibt lokal nutzbar.

## 5. Status

Status v26.14a: Supabase-Live-Schalter-Dry-Run dokumentiert. Auch bei testweise aktiviertem Live-Schalter bleibt Supabase ohne Config, SDK und Client-Erzeugung sicher lokal blockiert.
