# Synthetischer Fixture- und Harness-Vertrag

Stand: v27.31x
Status: verbindlicher Vertrag, nicht live ausgeführt

## Ziel

Dieser Vertrag definiert deterministische synthetische
Testwerte und die spätere Harness-Grenze für den äußeren
Fachmutations-Datenbanktest.

v27.31x implementiert noch keinen Fixture-Katalog und keinen
Datenbank-Harness. Es wird keine Datenbank gestartet.

## Sicherheitsgrenze

Erlaubt sind ausschließlich:

- synthetische UUIDs
- synthetische Ressourcenidentitäten
- deterministische 256-Bit-Client-Schlüssel
- kleine kanonische Test-Payloads
- Testbeobachtung nur im kontrollierten Harness

Ausgeschlossen bleiben:

- echte Teilnehmerdaten
- echte Namen und E-Mail-Adressen
- Datenbank-URLs
- Produktionsgeheimnisse
- Service-Role-Schlüssel
- Netzwerk- oder Datenbankausführung
- Frontend-Referenzen

## Testnutzer

- `user_alpha`: primärer synthetischer Eigentümer
- `user_beta`: Prüfung der Nutzertrennung

Beide besitzen feste synthetische UUID-v4-Werte.

## Ressourcen

Der Vertrag enthält feste Ressourcen für:

- primären Snapshot
- konkurrierenden Snapshot-Write
- konkurrierenden Snapshot-Create
- primäres Zyklusregister
- fremden Snapshot des zweiten Nutzers

Alle Ressourcenidentitäten beginnen mit `fixture:`.

## Client-Wiederholungsschlüssel

Jedes Szenario verwendet einen festen, eindeutigen
SHA-256-formatigen Testschlüssel.

Gleiche Retry-Szenarien verwenden bewusst denselben Schlüssel.
Unabhängige und konkurrierende Szenarien besitzen getrennte
Schlüssel.

## Payloads

Enthalten sind:

- Snapshot Version 1
- Snapshot Version 2
- zwei konkurrierende Snapshot-Payloads
- Zyklusregister Version 1
- Delete als `null`

Alle Write-Payloads verwenden `schema_version = 1`.

## Versionsstände

Deterministisch festgelegt sind:

- Create: 0
- nach Create: 1
- nach Update: 2
- nach Delete: 3
- stale: 0

## Szenarien

Der Vertrag bindet Nutzer, Ressource, Client-Schlüssel,
Operation, Payload und erwarteten Versionsstand für:

- Snapshot-Create
- identischen Completed-Retry
- exaktes Update
- stale Update
- exaktes Delete
- Zyklusregister-Create
- Nutzertrennung

## Konkurrenzbarrieren

Zwei Zwei-Parteien-Barrieren sind festgelegt:

1. zwei Writes mit demselben erwarteten Versionsstand
2. zwei Creates derselben Ressourcenidentität

Beide werden später gleichzeitig freigegeben und erwarten genau
einen Gewinner sowie genau einen geschlossenen Konflikt.

## Harness-Lebenszyklus

Der spätere Harness muss:

- Migrationen nach Dateinamenreihenfolge anwenden
- vor jedem Szenario zurücksetzen
- ausschließlich synthetische Auth-Nutzer anlegen
- `auth.uid()` nur innerhalb der Testtransaktion setzen
- zuerst die Clientantwort und danach interne Tabellen prüfen
- die Szenariotransaktion nach den Assertions zurückrollen
- keine Fixture-Zeilen zwischen Szenarien behalten
- Konkurrenztests mit genau zwei Workern ausführen

## Fehlerinjektion

Der Fehlerpunkt

`after_domain_mutation_before_idempotency_completion`

ist ausschließlich als testseitiges Harness-Konzept erlaubt.

Er darf nicht vom Client auswählbar und nicht als
Produktions-Hook implementiert werden.

## Noch offen

- tatsächlicher Fixture-Katalog
- tatsächlicher disposable Datenbank-Harness
- testseitige Fehlerinjektion
- Datenbank-, Konkurrenz- und Autorisierungstestläufe
- direkte App-Freigabe
- UI-Anbindung

## Automatische Prüfung

`tools/check-supabase-exam-history-outer-domain-mutation-fixture-harness-contract.py`

Der Prüfer ist dauerhaft in `tools/preflight.py` eingebunden.
