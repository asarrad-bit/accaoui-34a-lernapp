# Accaoui §34a Lern-App – Supabase-Live-Schalter-Test

Stand: v26.13b

Ziel: Prüfen, ob Supabase auch bei vorbereiteter Adapter-Struktur nicht versehentlich live geht.

## 1. Testgegenstand

Getestet wurde:

1. data/supabase-client-adapter.js
2. window.ACCAOUI_SUPABASE_LIVE_ENABLED
3. isSupabaseLiveEnabled()
4. getClientReadinessState()
5. getAdapterHealthState()
6. index.html Cache-Version des Supabase-Adapters

## 2. Erwarteter Zustand im lokalen Modus

Ohne echte Supabase-Config und ohne SDK muss gelten:

1. Adapter-Version: v26.13a
2. window.ACCAOUI_SUPABASE_ADAPTER.isSupabaseLiveEnabled(): false
3. isSupabaseLive: false
4. isLiveEnabled: false
5. isLocalAccessAllowed: true
6. hasConfig: false
7. hasSdk: false
8. canCreateClient: false
9. canCheckSession: false
10. Kein Login-Zwang

## 3. Sicherheitsbewertung

Der Live-Modus ist nur vorbereitet, aber nicht aktiv.

Wichtig:

1. Supabase wird nicht automatisch live geschaltet.
2. Ein echter Client wird weiterhin nicht erzeugt.
3. Echte Keys werden nicht benötigt.
4. Die App bleibt lokal nutzbar.
5. Der spätere Live-Betrieb braucht einen bewussten Schalter:
   window.ACCAOUI_SUPABASE_LIVE_ENABLED === true

## 4. Browser-Test

In der Browser-Konsole wurde geprüft:

1. window.ACCAOUI_SUPABASE_ADAPTER.version
2. window.ACCAOUI_SUPABASE_ADAPTER.isSupabaseLiveEnabled()
3. window.ACCAOUI_SUPABASE_APP_HEALTH_STATE

Erwartetes Ergebnis:

1. v26.13a
2. false
3. isSupabaseLive: false
4. isLiveEnabled: false
5. isLocalAccessAllowed: true

## 5. Status

Status v26.13b: Supabase-Live-Schalter-Test dokumentiert. Der Live-Schalter ist vorbereitet, aber Supabase bleibt im lokalen Modus gesperrt.
