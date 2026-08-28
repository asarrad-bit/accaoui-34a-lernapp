# Teilnehmerzugang – Browser-Loader v27.36f

## Ziel

Der kontrollierte Browser-Aktivierungsweg verbindet die vorhandenen
Teilnehmerzugangs-Bausteine nur auf ausdrückliche Anforderung. Die bestehende
Fachlogik und der lokale Standardbetrieb bleiben unverändert.

## Schalter

Der eindeutige Loader-Tag `accaoui-participant-access-browser-loader` steht
standardmäßig auf `data-enabled="false"`. Nur der exakte Wert `"true"`
fordert die Aktivierung an. Andere Werte laden keine zusätzlichen Ressourcen
und installieren keinen Provider.

## Ladefolge

Bei angeforderter Aktivierung lädt der Loader strikt nacheinander:

1. `data/supabase-participant-access-adapter.js`
2. `data/supabase-participant-access-bootstrap-bridge.js`
3. `data/supabase-participant-access-browser-provider.js`

Nach jedem Schritt wird ausschließlich die erforderliche Factory- oder
Provider-Oberfläche geprüft. Es gibt keine parallele Scriptladung, keine
automatische Client-Erzeugung und keine duplizierte Fachlogik.

## Readiness

Die Readiness-Grenze
`window.ACCAOUI_PARTICIPANT_ACCESS_BROWSER_LOADER_READY` wird synchron als
Promise installiert, bevor die asynchrone Ladefolge abgeschlossen ist. Der
einzige erfolgreiche Zustand lautet exakt
`{ requested: true, ready: true, status: "ready" }`. Die Oberfläche enthält
keine Client-, Nutzer-, Session-, Teilnehmer-, Kurs-, Key-, Config- oder
internen Fehlerdaten.

## Fail-closed-Grenze

Bei angeforderter Aktivierung führen fehlende Ressourcen, ungültige
Dependencies, Kollisionen, ungültige Readiness-Zustände und Providerfehler zu
einem generischen Fehlerzustand. `app.js` zeigt dann den bestehenden
`access_error`; es gibt keinen lokalen Fallback. Bei deaktiviertem Schalter
bleibt dagegen der bisherige v27.36d-Startweg unverändert.

## lokale synthetische Tests

Der Checker prüft Default-off, ausschließlich exaktes `true`, die feste
Ladefolge, frühe Readiness-Installation, den strengen Erfolgszustand,
Fail-closed-Verhalten, Kollisionsschutz, den vorhandenen v27.36d-Providervertrag
mit `resolveAccess()`, Regressionen und echte Manipulationsfälle. Alle Tests
arbeiten lokal mit synthetischen Browserzuständen und ohne externen Zugriff.

Supabase live: NEIN

echte Keys: NEIN

echte Teilnehmerdaten: NEIN
