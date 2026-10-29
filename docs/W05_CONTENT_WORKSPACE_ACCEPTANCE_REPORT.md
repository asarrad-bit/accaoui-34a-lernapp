# W05 – lokaler Redaktions- und Kursentwurf

Stand: 27.10.2026, Produktrevision 05. Funktionsnachweis und vollständige Originalendgates stehen für diese neuen Bytes noch aus.

## Umfang und Bedienung

„Redaktion“ öffnet eine eigene modale Oberfläche. Der echte Redaktionszugang bleibt standardmäßig gesperrt. Nur auf localhost/127.0.0.1 kann nach ausdrücklicher Bestätigung ein lokaler Arbeitsentwurf mit synthetischen Testrollen geöffnet werden. Die Testrollen sind keine Anmeldung und kein nachgewiesener Zugriffsschutz.

Der Entwurf bietet Kurse mit Zeitraum/Archivstatus/Dozentenzuordnung, Quellenangaben mit ungeklärter, Analyse- oder Eigennutzung, getrennte schriftliche Fragen, mündliche Fragen und Lernkarten, neun kanonische Sachgebiete, Suche und Filter. Antworten, Punkte, Musterantworten, Folgefragen und kritische Fehler werden passend zum Banktyp erfasst. Alle Texte werden als Text gerendert.

Der Ablauf lautet Entwurf → Review → Freigabe durch eine zweite Testperson → lokale Veröffentlichung → Archivierung. Sieben Reviewpunkte, Prüfdatum, bestätigte eigene Formulierung/Nutzungsprüfung und unterschiedliche Review-/Freigabeperson sind erforderlich. Eine Frage oder Quellenänderung entzieht die bisherige Freigabe. Gespeicherte Freigabeperson und sämtliche Review-Punkte werden vor Freigabe und in der veröffentlichten Auswahl erneut geprüft; Änderungen/Import/Export entfernen die Freigabeidentität. Versionen und ein begrenztes Änderungsprotokoll machen Änderungen nachvollziehbar. Dozenten dürfen nur in zugeordneten Kursen bearbeiten; Freigaben sowie Kurs-/Quellenverwaltung bleiben der Administration vorbehalten. Die Regeln werden im injizierten Service bei jeder Aktion erneut geprüft; eine spätere echte serverseitige Durchsetzung und Auth-Anbindung bleibt erforderlich.

Die Teilnehmer-Vorschau zeigt ausschließlich lokal veröffentlichte Inhalte eines aktiven zugeordneten Kurses im Zugangszeitraum. Sie übernimmt nichts in die vorhandenen Teilnehmerbanken. Die unveränderten Fragen-, Antwort- und Kartenbestände behalten ihren bisherigen Status; aus diesem lokalen Workflow entsteht keine neue fachliche Freigabe.

## Dateien und Daten

Die neuen Module sind data/content-workspace-v1.js (Modell/Service/Repositorygrenze) und data/content-workspace-ui-v1.js (Oberfläche). Nur der eigene Schlüssel accaoui_content_workspace_v1 wird geschrieben. Leere Ansichten schreiben nichts. Beschädigte Daten werden gemeldet und nicht überschrieben. Quota-/Speicherfehler erhalten Eingabe und vorherigen Stand. Native Web Locks koordinieren den lokalen Schreibzugriff; ohne Locks wird kein unsicherer Schreibersatz verwendet. Revision und Inhaltsversion verhindern blindes Überschreiben aus anderen Tabs. Das ersetzt keine echte Datenbanktransaktion oder Gerätesynchronisation.

Ein lokaler JSON-Import verarbeitet atomar 1–100 synthetische Entwürfe bis 500 KB. IDs, Typen, Formate, Referenzen und normalisierte Dubletten werden vor Speicherung geprüft; mitgebrachte Reviews/Freigaben werden abgelehnt. Exporte tragen ausschließlich Entwurfsstatus und keine Veröffentlichungsbefugnis. Kein Drive-Zugriff, kein Zugriff auf unbenannte Eigentümerquellen, keine Originaländerung und kein produktiver Import.

## Abnahme auf neuen Bytes – noch auszuführen

Der neue Funktionsprüfer verlangt 20 isolierte Modell-/Regelfälle und je zwölf echte Bedienfälle in Desktop1440×1000 und Mobilviewport390×844. Fälle decken Standardverweigerung, Rollen/Kurszuordnung, Kalender, drei Banken, Validierung/Dubletten, atomaren Import, Review/Quellen/zweite Person, Teilnehmerfilter, Freigabeentzug, Version/Revisionskonflikte, Quota, fehlende Locks, Export, literale Darstellung und native Tastatur-/Dialogbedienung ab. Mobilviewport ist kein physischer Gerätetest. Keine Uhrmanipulation, kein natürlicher Prüfungslauf, keine externen Anfragen aus dem neuen Modul.

Zusätzlich sind voller aktueller Schutz mit allen151Autoritätsfällen, unveränderte volle Originalkontinuität, vollständiger Originalpreflight mit Python3 und unverändertem innerem1800s-Budget, diff und exakter Nachschutz auf den endgültigen Bytes erforderlich. Alte W04-PASSE gelten nicht für diese neuen Bytes.

## Noch offene vollständige W05-Abnahme

Die konkrete Eigentümerfrage zu Drive-Ordnern/Dateien und Nutzungseinschränkungen wurde einmal gestellt und ist unbeantwortet. Fachliche Aktualität, tatsächliche Nutzungsrechte, Sichtung/Umformulierung/Review der konkret benannten Inhalte und Freigabe durch den Eigentümer bleiben offen. Keine Annahme aus einer Testcheckbox.

Geeignete isolierte echte DB/Auth-Umgebung ist bei W03 weiter offen. Echte Anmeldung, serverseitige Admin-/Dozentenrollen und Kursisolation, dauerhafte Verwaltung, Mehrclient-/Recoveryverhalten sowie kontrollierte Anbindung freigegebener Inhalte an den Teilnehmerfluss sind nicht durch lokale Testrollen bestanden. Der vollständige W05-Zielumfang bleibt erhalten; diese unabhängige Umsetzung ist kein pauschaler W05-PASS und kein gekürzter Full-Feature-Abschluss.

Audit/v27.37n STOPP / NOT VERIFIED; Supabase NICHT LIVE. Keine echten Teilnehmerdaten, Schlüssel, Nachrichten, paid Dienste, Produktion oder System-/Rechteänderung.

## Datierter erster Funktionsbefund und gezielte Korrektur

Der erste tatsächliche Regel-/Funktionslauf vom27.10.2026 10:02UTC endete nativ1: neunRegelfällePASS, der positive gültige Import im zehntenFallFAIL, Browser noch nicht gestartet. Strikte Modellvalidierung verlangt approval:null an jedem Entwurf. Der Importkonstruktor hatte dieses Pflichtfeld ausgelassen; ergänzt wird ausschließlich dieses Feld. Der volle ursprüngliche FAIL-Lauf und seine Streams bleiben separat erhalten. Alle Validierungen, zwanzigRegelfälle, vierundzwanzigBrowserfälle und Budgets bleiben unverändert. Neue tatsächliche Abnahme auf den korrigierten Bytes steht aus.

## Datierter zweiter Funktionsbefund und Abschlussbeobachtung

Der zweite tatsächliche Lauf vom27.10.2026 10:06UTC bestand alle20Regelfälle und den erstenDesktopbedienfall. Der nächste Fall las unmittelbar nach dem nativen Speicherklick noch den vorherigen Stand; der nachfolgende volle Fehlerscreenshot zeigt den tatsächlich gespeicherten Kurs/Stand1. Die neue UI kennzeichnet die laufende asynchrone Aktion mit aria-busy und sperrt Doppelaktionen bis zum echten Abschluss. Der Bedienprüfer wartet auf diesen sichtbaren Abschluss und behält sämtliche bisherigen Ergebnisbehauptungen und Zeitbudgets unverändert. Alter FAIL, Streams und Screens bleiben erhalten; neuer vollständiger Lauf steht aus.

## Datierter dritter Funktionsbefund und Versionskorrektur

Der dritte tatsächliche Lauf vom27.10.2026 10:11UTC bestand20Regelfälle und10Desktopbedienfälle. Der Zweittabfall scheiterte streng: Nach abgewiesenem Speichern aktualisierte der UI-Handler die geladene Inhaltsversion trotzdem, obwohl die alte Eingabe im Formular stand. Dadurch wurde nach Laden der aktuellen Revision eine veraltete Eingabe zugelassen. Die Korrektur gibt Erfolg/Fehler aus dem Schreibhandler zurück und aktualisiert Auswahl/Version ausschließlich nach Erfolg. Modellprüfung, sämtliche20+24Testfälle, Ergebnisasserts und Budgets bleiben bytegleich. Alter FAIL bleibt erhalten; neue vollständige Abnahme steht aus.
