# W04 – persönliche Lernführung: Abnahmeumfang

Stand 27.10.2026, 08:12 UTC: Produkt umgesetzt; datierter dritter Funktionslauf mit26Regel- und30Browserfällen tatsächlich bestanden. Diese letzte Abdeckungsrevision benötigt noch einen vollständigen26+32-Funktionslauf und alle endgültigen Originalpflichtgates. Kein W04-Paket-PASS, kein Gesamtproduktabschluss und kein Produktivstart.

Die Umsetzung umfasst lokalen Tagesplan mit Lernzeit und Pausen, Fortschritts-/Terminbezug, Pause und Neuplanung, Active Recall, zeitlich verteilte Kartenwiederholung, freiwillige In-App-Erinnerung und getrennte Darstellung fachlich geprüfter Antworten sowie Karten-Selbsteinschätzungen. Vorhandene Lernpfade, Fragenbanken und Speicher bleiben die Grundlage.

## Verbindlicher Prüfungsumfang

Der eigene Runner tools/run-w04-learning-guidance-v1.js prüft 26 deterministische Regel-/Speicherfälle und je 16 Bedienfälle in Desktop-1440×1000 und Mobilviewport-390×844:

1. Kalender-/Schaltjahr-/DST-Grenzen und konservative Einordnung alter oder beschädigter Kartenwerte.
2. Fälligkeit, steigende Abstände nach fälliger späterer Selbstbewertung, Rücksetzen nach Nicht-gewusst sowie unveränderte Fälligkeit bei frühem Wiederholen.
3. Standardwerte ohne Schreibzugriff, gültige und ungültige Einstellungen, beschädigter Speicher, Lesesperre, Quota und unbestätigte Schreibvorgänge.
4. Tatsächliche fachliche Bewertungszähler gegenüber Karten-Selbstbewertungen, Tageswechsel und Erhalt der Summen bei Einstellungsänderung.
5. Pause/Resume, nächster gültiger Termin, begrenztes Lernbudget und ausschließlich geöffnete lokale In-App-Erinnerung.
6. Tatsächliche native Bedienung der Plan- und Einstellungsfelder, Reload, vorhandene Fortsetzen-Reihenfolge, fällige Karte aufdecken/bewerten und fachliche Lernantwort per Tastatur.
7. Neuplanung anhand eines tatsächlich gespeicherten Termins, gezielte Planwiederherstellung mit Erhalt aller anderen Speicher, zwei Tabs mit Änderungskonflikt sowie Fokus/Viewport.

Der Browserlauf verwendet frische synthetische Browserkontexte und ausschließlich vorab gepinnte lokale Assets. Vorher und nachher wird der vollständige exakte aktuelle Schutz geprüft; unbehandelte Seitenfehler und externe Anfragen sind nicht zulässig. Die Regeltests mit festen Zeitpunkten sind kein natürlicher W01-Zeitnachweis. Zwei Browser-Tabs sind kein physischer Gerätewechsel und keine echte DB/Auth-Abnahme.

## Datierte tatsächliche Funktionsbelege

Der dritte Lauf unter fest bestätigter Node-/Edge-Laufzeit endete am27.10.2026 um08:12:56.599100UTC nativ0 nach32.7773181s:26Regelfälle und15Desktop- sowie15Mobilviewportfälle PASS,32Screens. Alle79initialen Artefakte wurden vollständig nativ gelesen/gehasht und exakt scoped; alle56Fallrecords gelesen, zweiScreens visuell geprüft. Vor-/Nachschutz identisch:116Autoritätsfälle,591Dateien/1182Attribute. Keine unbehandelten Seitenfehler oder externen Anfragen;42lokale Missingconfig-Anfragen/40Console404 der unveränderten Verfügbarkeitsprobe blieben ausdrücklich protokolliert. Kein Zugriff auf lokale Schlüsseldateien.

Nachlesebericht product-03/functional-01/result-readback.json:31600Bytes/SHA25667260ffcebdaa9951c11f804503153105c5b68fa11f46c910ffdc25cd83c9af3; Quittung539Bytes/SHA256a3fb6e0086cb19489fad1b111241c6d694801c062c6bb38f69e4e15a7fc8ddf9. Zwei frühere fehlgeschlagene Läufe bleiben vollständig erhalten: zuerst nichtisolierte aktive Lerneinheit in der synthetischen Fixture, dann nativer Mobilklick nach Zweittab durch Scroll-/Navigation überlagert. Gezielte Korrekturen bewahrten alle strengen Erwartungen; keine Force-/DOM-Klicks und keine Timeoutabschwächung.

Zusätzlicher verbindlicher Fall jeViewport: eine echte native manuell abgeschlossene schriftliche Prüfung mit einer beantworteten und81offenen Fragen. Nur die beantwortete Frage darf den objektiven Tageszähler erhöhen; Reload darf den Abschluss nicht erneut zählen. Das ist ein kurzer manueller Bedienfall ohne Uhränderung und kein W01-Naturzeitnachweis. Kein alter PASS gilt automatisch für neue Bytes.

## Abschlussgrenze

Alle bisherigen 116 Autoritäts-/Schutzfälle und die fachlichen Originalchecker samt Zeitbudgets bleiben unverändert. Nach tatsächlicher Funktionsabnahme werden Kontinuität, voller Original-Preflight mit Python3 und unverändertem inneren 1800s-Budget, Diff und exakter Nachschutz auf den endgültigen neuen Bytes vollständig ausgeführt und nativ nachgelesen. Erst danach ist ein sinnvoller normaler W04-Produkt-/Testcommit mit normalem Push und direkter GitHub-Bestätigung zulässig.

W03 bleibt von der konkret noch zu klärenden isolierten lokalen DB/Auth-Umgebung abhängig. Supabase NICHT LIVE; Audit/v27.37n STOPP / NOT VERIFIED. Keine echten Teilnehmerdaten, externen Nachrichten oder Produktionsfreigabe.
