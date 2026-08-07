# Verbindlicher aktueller Task

Task-ID: v27.35f
Status: AUTHORIZED
Autorisiert: JA
Titel: Wettbewerbsbeobachtung und Accaoui-Positionierung dokumentieren
Funktionaler Ausgangsstand: v27.35g
Erwarteter Ausgangscommit: `601dc6f751b6a603a27c4b3405150bf1d75e09fd`
Erlaubte Dateien: `docs/COMPETITOR_POSITIONING_NOTE_V2735F.md`
Commit erlaubt: NEIN
Push erlaubt: NEIN

## Verbindliche Committrennung und Gate-Korrektur

Der Commit `003112eaeb9a071a6396634b6da92fa11ae8921a` ist der funktionale
Ausgangs- und Vorautorisierungsstand. Der historische
v27.35f-Autorisierungscommit
`601dc6f751b6a603a27c4b3405150bf1d75e09fd` ist die verbindliche
Umsetzungsbasis. Der Commit
`d4e46edc48e967509e09ddd1096b54eb0bed5971` ist ein legitimer
nichtfunktionaler v27.35f-Gate-Fix-Commit, der ausschließlich die vier
Steuerungsdokumente und `tools/check-project-continuity-control.py`
verändert hat.

Der separate nichtfunktionale v27.35f-Implementierungs-Gate-
Korrekturschritt darf ausschließlich die vier Steuerungsdokumente und
`tools/check-project-continuity-control.py` verändern. Ursache dieser
fortgeführten Korrektur ist die unzulässige starre Checker-Forderung
`HEAD == 601dc6f751b6a603a27c4b3405150bf1d75e09fd`, durch die der legitime
Gate-Fix-Commit `d4e46edc48e967509e09ddd1096b54eb0bed5971` blockiert wurde.

Der frühere Notiz-SHA
`cff217d2b8cd0e9c50c3c1a351ff3de8ee595f0e3c59ed0def0ae1a3f8a799f7`
gehört zur Fassung vor der autorisierten Ergänzung „Reaktivierung nach
Lernunterbrechung“ und ist kein aktueller Prüfwert mehr. Die fertig
ergänzte Wettbewerbsnotiz ist als finaler v27.35f-Notiz-Snapshot mit
SHA-256
`983af73fb711cb2b77eb69b51d38ae5f4cf2991d1d976274eee0b4379ef9b023`
dokumentiert und muss während dieses Gate-Schritts unverändert bleiben.

Der Checker verlangt künftig, dass der Autorisierungscommit
`601dc6f751b6a603a27c4b3405150bf1d75e09fd` ein Vorfahr des aktuellen
HEAD ist und dass der gesamte bereits committete Bereich von dieser
Basis bis HEAD ausschließlich die fünf Gate-Dateien enthält. Eine starre
Gleichheit des HEAD mit einem einzelnen Gate-Commit ist verboten. Im
Working Tree sind ausschließlich zwei Zustände zulässig: vor dem
Gate-Commit exakt fünf modifizierte Gate-Dateien plus die ungetrackte
Notiz oder nach dem Gate-Commit ausschließlich die ungetrackte Notiz.
Für die Umsetzung bleibt ausschließlich
`docs/COMPETITOR_POSITIONING_NOTE_V2735F.md` erlaubt; sie darf ungetrackt
vorliegen. Keine weitere ungetrackte Datei ist zulässig.

v27.35f bleibt der einzige aktive Task. Commit und Push bleiben verboten,
und ein Folgetask wird nicht ausgewählt oder autorisiert.

## Ziel

Eine interne strategische Dokumentation erstellen, die allgemeine
Verkaufs- und Positionierungsmechanismen eines beobachteten
Wettbewerberangebots analysiert und daraus eine eigenständige,
ehrliche Accaoui-Positionierung ableitet.

## Verbindliche Grundlage

Die folgenden Punkte dürfen ausschließlich als beobachtete und nicht
extern verifizierte Wettbewerber-Werbeaussagen beschrieben werden:

- niedriger Einmalpreis im Vergleich zu möglichen Wiederholungs- und Prüfungskosten
- zeitlich unbegrenzte Prüfungssimulationen
- behauptete Abdeckung aller IHK-Fragen
- behauptetes KI-basiertes Erkennen von Schwächen
- Rückerstattungs- oder Risikoumkehr-Versprechen
- dauerhafter Besitz beziehungsweise unbegrenzter Zugang
- Nutzerzahlen, Bewertungen oder sonstiger Social Proof

## Zulässige allgemeine Marketingmechanismen

- Preisanker
- Verlustvermeidung
- klare Nutzenkommunikation
- Risikoumkehr
- Social Proof
- Einfachheit des Angebots
- persönliche Schwächenanalyse
- Prüfungssimulation als konkretes Leistungsversprechen

## Verbindliche Accaoui-Differenzierung

- Wissen verständlich vermitteln
- typische Fehler erkennen und gezielt bearbeiten
- Inhalte langfristig festigen
- realistische schriftliche und mündliche Prüfungsvorbereitung
- nachvollziehbare persönliche Lernführung
- Teilnehmer bis zur Prüfungsreife begleiten
- echte Unterrichts- und Prüfungsvorbereitungserfahrung
- nicht nur Fragen beantworten, sondern Inhalte verstehen

## Qualitätsmaßstab

> „Mit dieser App habe ich es endlich verstanden.“

Die Leitidee aus `docs/PROJECT_MASTERLIST.md` bleibt verbindlich.

## Verboten

- Wettbewerbertexte kopieren
- geschützte Formulierungen nachahmen
- behaupten, der Wettbewerber lüge oder handle rechtswidrig
- nicht belegte Nutzerzahlen oder Bewertungen als Tatsachen darstellen
- behaupten, Accaoui besitze alle originalen IHK-Fragen
- Bestehensgarantien
- unbelegte KI-Versprechen
- unbelegte Rückerstattungsversprechen
- konkrete Preise verbindlich festlegen
- App-Code, UI, Fragenbanken oder Marketingmaterial verändern
- Webrecherche oder externe Behauptungen ohne gesonderten Auftrag
- Funktions-, Fragen-, UI-, Supabase-, SQL- oder Netzwerkänderungen
- automatische Auswahl oder Autorisierung eines Folgetasks

## Akzeptanzkriterien

1. Beobachtung, Bewertung und Accaoui-Empfehlung sind klar getrennt.
2. Wettbewerberaussagen sind ausdrücklich als nicht verifiziert markiert.
3. Keine Formulierung wird vom Wettbewerber übernommen.
4. Chancen und Risiken der Marketingmechanismen werden sachlich erklärt.
5. Eine eigenständige Accaoui-Kernpositionierung wird formuliert.
6. Zulässige und unzulässige Werbeaussagen werden getrennt dokumentiert.
7. Die Leitidee aus `docs/PROJECT_MASTERLIST.md` bleibt verbindlich.
8. Keine Funktions-, Fragen-, UI-, Supabase-, SQL- oder Netzwerkänderung.
9. Ausschließlich `docs/COMPETITOR_POSITIONING_NOTE_V2735F.md` wird im späteren Umsetzungsschritt verändert.
10. Kein Commit und kein Push ohne gesonderte Freigabe.

## Historische Grenze des Autorisierungsschritts

`docs/COMPETITOR_POSITIONING_NOTE_V2735F.md` wurde im abgeschlossenen
Autorisierungsschritt noch nicht erstellt oder verändert. In diesem
Schritt wurde keine Wettbewerbsnotiz erstellt und keine App-Datei
verändert.

Die spätere Umsetzung darf ausschließlich diesen `CURRENT_TASK`
bearbeiten. Nach Abschluss wird kein Folgetask automatisch ausgewählt.
