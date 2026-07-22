# Operations-ID-/Idempotenz-Integrationsaudit

Stand: v27.31j

Status: statischer Sicherheits-Audit, keine Live-Ausführung

## Geprüfte Bestandteile

1. Operations-ID-Ausstellungstabelle v27.31h
2. Operations-ID-Ausstellungs-RPC v27.31i
3. Idempotenz-Reservierungs-RPC v27.31c
4. Idempotenz-Abschluss-RPC v27.31d
5. Operations-ID-Ausstellungsvertrag
6. transaktionaler Fachmutationsvertrag

## Browsergrenze

Der spätere äußere Fachmutations-RPC darf vom Browser nur den
unvertrauenswürdigen `client_request_key` erhalten.

Eine `external_operation_id` darf nicht als Browserparameter
der Ausstellungsgrenze akzeptiert werden.

## Interne UUID-Ausstellung

Der Ausstellungs-RPC:

- akzeptiert keine externe Operations-ID
- hasht den Client-Wiederholungsschlüssel serverseitig
- hasht die kanonische Anfrage serverseitig
- lässt die UUID durch den Datenbank-Default erzeugen
- gibt sie erst nach erfolgreicher Speicherung zurück
- verwendet sie bei identischen Retries erneut

## Übergabe an die Idempotenzgrenze

Reservierung und Abschluss verwenden exakt:

- intern ausgestellte UUID
- Operationsbereich
- Mutation
- Ressourcenidentität
- Payload-Fingerprint

Die vier kanonischen Fachparameter stimmen mit dem
Ausstellungs-RPC überein.

## Zugriffsschutz

Ausstellungs-, Reservierungs- und Abschluss-RPC:

- sind interne Security-Definer-Helfer
- besitzen einen festen `search_path`
- sind für `public`, `anon` und `authenticated` vollständig
  entzogen
- werden nicht direkt im Frontend referenziert
- besitzen kein direktes `GRANT EXECUTE`

## Noch fehlende Verbindung

Ein äußerer transaktionaler Fachmutations-RPC ist noch nicht
implementiert.

Er muss später innerhalb einer einzigen Datenbanktransaktion:

1. den Nutzer authentifizieren
2. die Operations-ID intern ausstellen oder wiederverwenden
3. ausschließlich diese intern erhaltene UUID reservieren
4. nur bei `reserved_new` fachlich mutieren
5. den Vorgang terminal abschließen
6. vorhandene Pending- oder Terminalzustände ohne erneute
   Fachmutation behandeln

Eine browserseitig gelieferte Operations-ID ist unzulässig.

## Auditergebnis

Die vorhandenen internen Schnittstellen sind strukturell
kompatibel und geschlossen geschützt.

Die produktive Freigabe bleibt dennoch gesperrt, bis der äußere
Fachmutations-RPC implementiert und mit Live- und
Parallelitätstests geprüft wurde.

## Automatische Prüfung

`tools/check-supabase-exam-history-operation-identity-idempotency-integration.py`

Der Audit ist dauerhaft in `tools/preflight.py` eingebunden.

## Sicherheitsgrenze

- keine neue SQL-Migration
- kein äußerer Fachmutations-RPC
- keine direkte Helper-Freigabe
- keine echten Teilnehmerdaten
- keine Live-Ausführung
- keine UI-Änderung


## Äußerer RPC-Schnittstellenvertrag v27.31k

Der spätere äußere Fachmutations-RPC darf ausschließlich
folgende Browserparameter akzeptieren:

- Client-Wiederholungsschlüssel
- Operationsbereich
- Mutation
- Ressourcenidentität
- Fach-Payload

Nicht als Browserparameter erlaubt sind insbesondere:

- Operations-UUID
- Operationsidentität
- Payload-Fingerprint
- Nutzer- oder Teilnehmer-ID
- Ergebnis- oder Fehlerstatus

Der äußere RPC muss den Payload kanonisieren und den
Payload-Fingerprint serverseitig ableiten.

Die intern ausgestellte UUID darf ausschließlich intern an
Reservierung und Abschluss weitergegeben werden. Sie wird nicht
Teil der Clientantwort.

Maschinenlesbarer Vertrag:

`docs/contracts/exam-history-outer-domain-mutation-rpc-interface-contract.json`
