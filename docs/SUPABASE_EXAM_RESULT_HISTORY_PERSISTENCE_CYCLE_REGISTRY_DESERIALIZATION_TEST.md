# Prüfungsergebnishistorie-Zyklusregister-Deserialisierung

Stand: v27.30k

Status: lokal vorbereitet und ausführbar, ohne Storage- oder UI-Aufruf

## Funktion

`mapParticipantFullExamResultHistorySnapshotPersistenceCycleRegistryDeserializationState(input)`

## Aufgabe

Ein serialisierter Persistenz-Zyklusregister-Payload wird erst
nach einer Größenprüfung geparst und anschließend vollständig
als kanonischer Register-State rekonstruiert.

## Sicherheitsregeln

- maximales Größenlimit von 32768 UTF-8-Bytes vor dem Parsing
- ausschließlich JSON-Objekte mit zwei definierten Feldern
- feste Registerversion 1
- maximal 100 Zyklusidentitäten
- keine Zusatzfelder
- JSON muss bereits kanonisch serialisiert sein
- Identitäten werden erneut über den Register-Mapper geprüft
- rekonstruierter Payload muss dem Eingabe-JSON exakt entsprechen
- erneute Serialisierung muss denselben String und dieselbe Größe ergeben
- Getter und Setter werden nicht ausgeführt
- rohes Eingabe-JSON wird nicht in den Ergebnisstate übernommen
- kein Browser-Storage
- keine Storage-Methode
- kein RPC-Aufruf
- kein Supabase-Client
- kein Netzwerk
- keine sichtbare UI
