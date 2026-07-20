# Prüfungsergebnishistorie-Snapshot-Persistenzvertrag

Stand: v27.29w

Status: lokal vorbereitet und ausführbar, ohne Browser-Storage

## Funktion

`mapParticipantFullExamResultHistorySnapshotPersistenceContract(input)`

## Unterstützte Intents

- Save
- Load
- Delete

## Speicherschlüssel

Fester Namensraum:

`accaoui.exam_history.snapshot.v1`

Der vollständige Schlüssel besteht ausschließlich aus dem
Namensraum und der kanonischen Anfrageidentität.

## Sicherheitsregeln

- keine Teilnehmer-ID im Speicherschlüssel
- Schlüssel wird vollständig neu validiert
- Save akzeptiert nur einen sicheren Serialisierungsstate
- Load deserialisiert und normalisiert den gespeicherten Wert erneut
- Schlüssel- und Snapshot-Identität müssen übereinstimmen
- Delete akzeptiert nur einen kanonischen Schlüssel
- kein Local-, Session- oder IndexedDB-Zugriff
- kein echter Save-, Load- oder Delete-Aufruf
- kein RPC-Aufruf
- kein Supabase-Client
- kein Netzwerk
- keine sichtbare UI
