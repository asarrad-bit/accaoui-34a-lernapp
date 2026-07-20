# Prüfungsergebnishistorie-Snapshot-Deserialisierungsstate

Stand: v27.29v

Status: lokal vorbereitet und ausführbar, ohne Speicherung

## Funktion

`mapParticipantFullExamResultHistorySnapshotDeserializationState(input)`

## Aufgabe

Serialisiertes Snapshot-JSON wird zuerst nach Typ und
UTF-8-Größe geprüft. Erst danach darf das JSON geparst werden.

## Sicherheitsregeln

- maximal 4096 UTF-8-Bytes vor dem Parsen
- keine führenden oder nachgestellten Leerzeichen
- JSON muss kanonisch und objektförmig sein
- Snapshot-Normalizer muss die Struktur vollständig akzeptieren
- Snapshot wird anschließend kanonisch neu erstellt
- erneute Serialisierung muss bytegleich sein
- Snapshot-Wiederaufnahme-State muss erfolgreich sein
- keine rohe JSON-Eingabe im Rückgabestate
- kein Local-, Session- oder anderer Browser-Storage
- kein RPC-Aufruf
- kein Supabase-Client
- kein Netzwerk
- keine Teilnehmer-ID
- keine sichtbare UI
