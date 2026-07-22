# End-to-End-Idempotenz-RPC-Flow-Audit

Stand: v27.31e

Status: statischer Sicherheits-Audit, keine Live-Ausführung

## Geprüfte Bestandteile

1. Idempotenz-Operationstabelle v27.31b
2. Idempotenz-Reservierungs-RPC v27.31c
3. Idempotenz-Abschluss-RPC v27.31d

## Gemeinsame Identitätsgrenze

Reservierung und Abschluss verwenden dieselben fünf
Identitätsparameter:

- externe Operations-UUID
- Operationsbereich
- Mutation
- Ressourcenidentität
- Payload-Fingerprint

Beide RPCs berechnen daraus dieselbe kanonische
Operationsidentität.

## Atomare Reservierung

Eine neue Operation wird über die eindeutigen
Datenbankbedingungen als `pending` reserviert.

Bei Konflikten wird kein zweiter Vorgang angelegt. Der
bestehende Datensatz wird gesperrt und vollständig
gegengeprüft.

## Atomarer Abschluss

Nur ein vorhandener `pending`-Vorgang kann zu `completed`
oder `failed` wechseln.

Bereits terminale identische Abschlüsse werden unverändert
zurückgegeben. Abweichende zweite Abschlüsse werden blockiert.

## Zugriffsschutz

- Tabelle mit aktiviertem und erzwungenem RLS
- keine direkte Tabellenpolicy
- keine direkten Tabellenrechte für App-Rollen
- beide internen RPCs vollständig für `public`, `anon` und
  `authenticated` entzogen
- keine direkte Ausführungsfreigabe
- keine Service-Role-Daten im Projekt

## Fachmutationsgrenze

Reservierungs- und Abschluss-RPC verändern ausschließlich die
Idempotenz-Operationstabelle.

Sie verändern nicht:

- Prüfungsversuche
- Prüfungsantworten
- Fragen-Snapshots
- private Lösungsschlüssel
- andere Fach- oder Teilnehmerdaten

## Wichtiges Auditergebnis

Die drei Sicherheitsbestandteile sind strukturell konsistent.

Die eigentliche spätere Snapshot- oder
Zyklusregister-Fachmutation ist aber noch nicht mit dieser
Transaktionsgrenze verbunden.

Eine produktive Mutation darf erst freigegeben werden, wenn ein
geprüfter Security-Definer-Mutations-RPC innerhalb derselben
Datenbanktransaktion:

1. die Operation reserviert
2. nur bei neuer Pending-Reservierung die Fachmutation ausführt
3. den passenden terminalen Abschluss speichert
4. bei vorhandenen terminalen Operationen das gespeicherte
   Ergebnis unverändert wiederverwendet
5. keine Fachmutation außerhalb der Reservierung bestätigt

## Automatische Prüfung

`tools/check-supabase-exam-history-idempotency-flow.py`

Der Audit ist zusätzlich dauerhaft in `tools/preflight.py`
eingebunden.

## Sicherheitsgrenze

- keine Live-Migration
- kein Live-RPC
- keine echten Teilnehmerdaten
- kein Browser-Storage
- keine UI-Änderung
