# v27.37g – Prüfungsabschluss gegen Wiederaufnahme und Doppelverbuchung absichern

## Vertrag und Ursache

Autorisiert durch CURRENT_TASK im Gate 423682d18977de999103f62c6b2502229c993a66.
Funktionaler Ausgangsstand bleibt v27.35g. Keine allgemeine Unterrichtsfreigabe.

Die letzte wirksame finishExamMode-Deklaration löschte die aktive Sitzung,
ließ aber currentMode auf exam. beforeunload/pagehide und Timer-Autosave konnten
deshalb den abgegebenen Versuch erneut speichern. Resume und Dashboard prüften
keinen Abschlussstatus. saveExamResult hängte jeden Aufruf erneut an; auch die
Themenstatistik wurde bei wiederholtem Abschluss nochmals verändert.

## Umsetzung und Speichervertrag

Jeder neue schriftliche Versuch erhält vor seiner ersten Speicherung eine UUID
über crypto.randomUUID(). Die aktive Sitzung ergänzt attemptVersion: 1,
attemptId und attemptStatus (active oder completed). Der Verlauf speichert
dieselbe attemptId. Pause, Navigation, Autosave und Resume behalten die Kennung
und den Lernstand. Eine neue Prüfung nach Abschluss erhält eine neue Kennung,
auch bei identischen Antworten. Ein vorhandener laufender Versuch wird beim
Start einer weiteren Prüfung nicht stillschweigend verworfen.

Der Abschluss setzt den synchronen Wächter vor jedem Speicherzugriff auf closing,
verlässt den aktiven Prüfungsmodus und beendet Timer sowie ausstehendes Autosave.
Ein vollständiger terminaler Sitzungsschnappschuss wird vor den bisherigen
Trainings- und Verlaufsnebenwirkungen gespeichert. Die benötigten Fragen und
Antworten bleiben für Ergebnisansicht, Themenauswertung und Fehlertraining im
Arbeitsspeicher erhalten. Die vorhandene Punkte- und Teilpunktelogik bleibt bestehen.

Jede Verbuchung liest den tatsächlich gespeicherten Verlauf erneut und prüft die
Kennung. Bestehende Einträge einschließlich alter Duplikate bleiben in derselben
Reihenfolge erhalten. Gleiche Ergebnisse unterschiedlicher Kennungen zählen
weiterhin als verschiedene Versuche. Es gibt keine pauschale Verlaufsbereinigung.

Terminale Sitzungen und Sitzungen mit exakt passender Ergebnis-ID sind weder im
Dashboard noch direkt fortsetzbar. Lesen löscht oder migriert keine Nutzdaten.
Ungültige JSON-Daten, ungültige neue Kennungen/Statusfelder sowie Speicherfehler
führen zu einem generischen Hinweis. Beschädigte Speicher werden nicht durch
leere Defaults überschrieben. Nach einem fehlgeschlagenen Abschluss wird im
aktuellen Dokument kein weiterer Abschlussversuch automatisch verbucht.

## Grenze bei Altbeständen

Ohne ID und Status lässt sich eine alte abgegebene Sitzung nicht zuverlässig von
einer pausierten unterscheiden. Es gibt keine Heuristik anhand Antwortvollständigkeit,
Position, Zeit, Titel, Punkten oder ähnlichen Verlaufseinträgen.

Dashboard und direkter Resume führen zur ausdrücklich zu prüfenden gespeicherten
Prüfung. Ein lokaler Dialog bietet drei gleichwertige Entscheidungen:

- Bereits abgegeben: Fragen, Antworten und Zeit bleiben erhalten; nur terminale
  Metadaten werden ergänzt. Kein neuer Verlaufseintrag und keine Trainingszählung.
- Noch nicht abgegeben: Eine dauerhafte Kennung wird ergänzt und derselbe
  gespeicherte Lernstand fortgesetzt.
- Abbrechen (auch Escape): Keine Speicheränderung und keine automatische Fortsetzung.

Ändert sich die Speicherung während des Dialogs, wird die Entscheidung nicht auf
den veränderten Stand angewandt. Eine bewusste Benutzerklärung ist hier erforderlich;
automatische Erkennung früherer Abschlüsse wird nicht behauptet.

## Umfang und Grenzen

Genau app.js, tools/check-written-exam-completion-v2737g.py,
docs/WRITTEN_EXAM_COMPLETION_REPAIR_V2737G.md und tools/preflight.py.
app.js ändert nur die acht freigegebenen Funktionen und den markierten Hilfsblock
unmittelbar vor getActiveSession. Die frühere finishExamMode-Deklaration bleibt
unverändert. preflight.py ersetzt ausschließlich die vorbereitete Checker-Zuweisung.

localStorage bietet keine Transaktion über mehrere Schlüssel. Tritt nach der
terminalen Speicherung ein Schreibfehler bei Trainingsdaten oder Verlauf auf,
können bereits ausgeführte Teiländerungen bestehen bleiben. Es wird keine
Erfolgsansicht gezeigt und der terminale Versuch nicht automatisch wiederholt.
Kein automatischer Rollback, keine verteilte Mehrgeräte-/Mehrtab-Transaktion und
keine spekulative Nachverbuchung sind Bestandteil dieses Reparaturschritts.

Keine Änderungen an Fragenbanken, anderen Lernarten, Auth-Kette, historischen
Checkern oder Backups. Keine weiteren Auditfehler behoben. Beide Loader bleiben
data-enabled="false". Keine SDK-/Config-Aktivierung, Supabase NICHT LIVE.

## Prüfungen

Der neue Checker führt die tatsächliche app.js in frischen Node-VM-Kontexten aus.
Nur Darstellung und externe Grenzen werden simuliert; Abschluss, Punktelogik,
Speicherzugriffe, Trainingszählung, Resume und Dashboard-Auswahl laufen real.
Die Speicher sind ausschließlich synthetische In-Memory-Maps, ohne Netzwerk.

34 Verhaltensfälle: leere, teilweise, vollständig richtige/falsche Prüfungen;
50-Prozent-Grenze und Teilpunkte; Vollsimulation mit 82 Fragen; mehrfacher und
reentranter Abschluss; Timer plus Klick; verzögertes Autosave, Verlassen und
Neuladen; zwei identische neue Versuche; Pause/Resume; frischer Verlauf statt
veralteter globaler Kopie; terminaler Status/exakte Ergebnis-ID; alle drei
Altbestandsentscheidungen; geänderter Dialogstand; beschädigtes JSON, ungültige
Metadaten und Lese-/Schreibfehler einschließlich der ersten Speicherung.

Sechs semantische Mutationen: fehlender terminaler Autosave-Schutz, fehlender
synchroner Abschlusswächter, unbedingtes Verlaufs-Anhängen, neue ID beim Resume,
wiederverwendete ID beim Neustart und ungeklärter Altbestands-Resume. Jede Mutation
muss zuerst syntaktisch gültig sein und danach an einer Verhaltensassertion scheitern.

Entwurfsprüfung außerhalb des Repositorys: 34/34 Verhaltensfälle PASS,
6/6 semantische Mutationen erkannt. Repository-Checker, Kontinuität/Lifecycle,
vollständiger Preflight und isolierter Browser-Smoke-Test folgen nach Übernahme;
dieser Zwischenstand behauptet dafür noch keinen PASS.
