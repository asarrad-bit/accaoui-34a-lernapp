# W02 – vorhandene Lern- und Prüfungsabläufe
Status: FUNKTIONALE NUTZERFÄLLE PASS; VOLLSTÄNDIGE ENDGATES UND VERÖFFENTLICHUNG AUSSTEHEND.

Beim vorhandenen Prüfungsbogen A zählte die Gesamtauswertung alle Antworten, die Auswertung nach drei Prüferblöcken blieb jedoch aus. Die aktuelle lokale Datenquelle benennt A als oral_sheet_a_v2340; vier bestehende Routing-/Reset-/Review-Prädikate in patch-v21.js erkannten ausschließlich oral_sheet_a_v2320. Genau diese vier Prädikate erkennen jetzt beide vorhandenen A-Kennungen. Alle übrigen Programmbytes dieses Patches sowie Fragen und Lösungen bleiben unverändert.

Der eigenständige lokale Prüfer tools/run-w02-user-flows-v1.js verwendet den vorhandenen signierten Edge und isolierte synthetische Kontexte. Er bedient die sichtbare Desktop- beziehungsweise mobile Navigation und die vorhandenen Szenenknöpfe. Er verändert keine Uhr und ruft keine externen Dienste auf. Der ursprüngliche fehlgeschlagene strenge Bogen-A-Test bleibt erhalten; seine Erwartung wurde nicht gelockert.

## Tatsächlich neuer Browsernachweis
run-07 am24.10.2026,18:13:39.860–18:14:30.158UTC: nativer Node-Exit0,50.298 beobachtete UTC-Sekunden,40 Fälle (20 je Ansicht) und32 Ansichten. Desktop1440×1000, mobiler Viewport390×844. Beide vollständigen Schutzabgleiche identisch, keine unbehandelten Browserfehler oder externen Anfragen.
Privater Ergebnisbericht: product-acceptance-v1/run-07/result.json,542682Bytes/SHA2565a682f0633348e2be5de2601211cafab6c4a98294980d8e8b849eea4123ac3ef.
Vollständige Nachlesung: functional-readback-07.json SHA256 7ce4d8fc06f1a793a8c5dad268d192b4e8c04f20e5689585b6d84099aef653eb.
Aktuelle Laufzeitbindung: Edge156.0.4314.42, Browser-SHA256bb74db4c753133706f4ab0a483a87aa28a90ddd6eeb305fe001376ba73a40fc3; genau vier unabhängig gebundene Laufzeiten einschließlich nativer Signatur-/Versionsprüfung.
Die erwartete fehlende lokale optionale Konfigurationsdatei erzeugt einen dokumentierten404; die App bleibt im lokalen Modus.

| Konkreter Fall | Desktop | Mobiler Viewport |
|---|---|---|
| dates-save-independent-and-reload | PASS | PASS |
| date-delete-preserves-other-date | PASS | PASS |
| date-quota-error-preserves-storage | PASS | PASS |
| learning-keyboard-answer-score-and-autosave | PASS | PASS |
| learning-pause-reload-resume-review | PASS | PASS |
| category-route-preserves-written-learning-mode | PASS | PASS |
| flashcard-reveal-and-rating | PASS | PASS |
| flashcard-pause-reload-resume | PASS | PASS |
| oral-practice-reveal-and-separate-rating | PASS | PASS |
| oral-mistake-reveal-collapse-resolve-last | PASS | PASS |
| oral-sheet-A-manual-all-known-blocks | PASS | PASS |
| written-full-manual-flow-start-no-clock-patch | PASS | PASS |
| written-pause-reload-resume-identity-and-answers | PASS | PASS |
| written-unanswered-warning-preserves-answers | PASS | PASS |
| written-manual-confirmation-grades-once | PASS | PASS |
| written-mistake-training-and-real-partial-result | PASS | PASS |
| written-reload-history-no-false-resume | PASS | PASS |
| statistics-actual-ui-after-synthetic-result | PASS | PASS |
| corrupt-written-storage-rejected-without-deletion | PASS | PASS |
| layout-width-and-native-button-focus | PASS | PASS |

Bogen A zeigt nach15manuellen sicheren Bewertungen drei Blöcke mit jeweils5sicher/0üben/0offen. Die schriftliche manuelle Bedienprüfung liefert je82Fragen,4/120Punkte,2richtig/2falsch/78offen sowie genau einen Verlauf nach Reload. Das schriftliche Fehlertraining enthält80falsche/teilweise/offene Fragen; nach einer richtigen Antwort zeigt die echte Zwischenauswertung1/80bearbeitet,1richtig,0falsch,79offen. Mündliche Fehler bleiben dabei unverändert.
Termine, Lern- und Kartensitzungen wurden tatsächlich gespeichert und nach Reload fortgesetzt. Quotenfehler und beschädigtes JSON wurden gezielt in den isolierten Browserkontext injiziert und führten weder zu vorgetäuschtem Erfolg noch Löschung des betroffenen gespeicherten Zustands.

## Erhaltene vorherige Belege
run-01: Prüfer verwendete auf Mobil die verborgene Desktopnavigation, Exit1.
run-02: korrigierte Bestandsaufnahme,16Ansichten,Exit0.
run-03: verborgene Legacy-Oralkontrolle angesprochen,Exit1.
run-04:36konkrete Fälle,Exit0; diese Teilabnahme bleibt separat.
run-05: zusätzlicher strenger Bogen-A-Test deckte den Produktfehler auf,Exit1.
run-06: Reflow ließ den Prüfer kurz die alte Bedienfläche auswählen,Exit1.
run-07: ausschließlich vorhandene Szenenkontrollen verwendet; alle40Fälle inklusive unverändert strenger Bogen-A-Erwartung PASS.
Die alten Ergebnisse, Quellenfassungen und Manifeste liegen unverändert im privaten Paketbereich. Kein FAIL wurde überschrieben.

## Grenzen und Pflichtgates
Dies sind lokale synthetische Bedienprüfungen mit manueller Selbsteinschätzung im mündlichen Training. Viewporttests sind keine physischen Gerätetests; weder echte Sprachbewertung noch vollständige Geräteabnahme wird behauptet.
Die manuellen schriftlichen Bedienversuche sind keine natürlichen Timeoutnachweise. Historische W01-Belege und die beiden damaligen W01-Appstarts (erster abgebrochen) bleiben unverändert; kein weiterer W01-Naturlauf oder neutraler Ersatztest.
Die frühere volle Sechspfad-Bindungsprüfung ist kein neuer PASS für diese Produkt-/Prüfer-/Berichtsfassung. Vor sinnvollem Paketcommit und normalem Push müssen auf den endgültigen Bytes die vollständige Original-Kontinuität, der volle Original-Preflight/Python3 mit unverändertem innerem1800s-Budget, Diff und exakter Schutz tatsächlich bestehen. GitHub ist danach direkt zu bestätigen.
Die23Bindungs-/Abnahmekriterien werden einzeln in criteria-matrix-functional-07.json eingeordnet; bedingte und nur teilweise belegte Punkte bleiben gekennzeichnet. W03–W08 folgen erst nach den kanonischen Abhängigkeiten.
Supabase NICHT LIVE; keine Produktion/Stores, echten Daten/Schlüssel/Nachrichten, bezahlten Dienste oder System-/Rechte-/Sicherheitsänderungen. v27.37n und die alte Auditdatei bleiben STOPP / NOT VERIFIED, unverändert und unversioniert.
