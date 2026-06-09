# Accaoui §34a – Punkteplan schriftliche Vollsimulation

Stand: **v24.3x** (Teilpunkte-Audit ergänzt; Punkteplan v24.1)
Projekt: Accaoui §34a Lern-App
Grundlage: `docs/EXAM_SIMULATION_AUDIT.md`, `docs/WRITTEN_QUESTION_EXPANSION_PLAN.md`, `questions.json` (86 Fragen, nur gelesen)

**Hinweis:** Diese Datei ist **nur Planungsgrundlage**. In v24.1 werden **keine** `points`-Felder in `questions.json` eingefügt und **kein Code** geändert.

---

## 1. Zweck

- Vorbereitung der **echten schriftlichen Vollsimulation** nach §-34a-Struktur.
- **Ziel:** 82 Fragen / 120 Punkte / 120 Minuten / Bestehen ab **50 Prozent**.
- Diese Datei ist **nur Planung**, keine technische Umsetzung.

---

## 2. Ausgangslage

| Befund | Detail |
|--------|--------|
| Fragenbank | **86 Fragen** in `questions.json` |
| Punktefelder | **Keine** `points`-, `score`- oder `weight`-Felder vorhanden |
| Technischer Fallback | Fehlende Punkte werden in `app.js` vermutlich als **1 Punkt** behandelt (`DEFAULT_QUESTION_POINTS`) |
| Folge | Für echte **120-Punkte-Logik** müssen später kontrolliert **`points`-Felder** ergänzt werden |

---

## 3. Zielstruktur schriftliche Prüfung

| Sachgebiet | Simulationsfragen | Zielpunkte | Zweipunktfragen nötig |
|------------|------------------:|-----------:|----------------------:|
| Recht der öffentlichen Sicherheit und Ordnung | 7 | 11 | 4 |
| Gewerberecht | 5 | 8 | 3 |
| Datenschutzrecht | 5 | 8 | 3 |
| Bürgerliches Gesetzbuch | 13 | 21 | 8 |
| Strafgesetzbuch und Strafverfahrensrecht | 13 | 21 | 8 |
| Unfallverhütungsvorschriften Wach- und Sicherungsdienste | 8 | 13 | 5 |
| Umgang mit Waffen | 5 | 8 | 3 |
| Umgang mit Menschen | 19 | 19 | 0 |
| Grundzüge der Sicherheitstechnik | 7 | 11 | 4 |
| **Gesamt** | **82** | **120** | **38** |

Rechnerisch: **38 × 2 + 44 × 1 = 120 Punkte**.

---

## 4. Wichtige Regel

- **Umgang mit Menschen** bleibt vollständig **1 Punkt** (19 Fragen / 19 Punkte).
- **2-Punkte-Fragen** sollen **fachlich begründet** sein.
- Geeignet für **2 Punkte** sind eher:
  - Mehrfachauswahl (`multiple`)
  - Kombinationsfragen (`combination`)
  - Fallfragen (`praxisfall`)
  - Abgrenzungsfragen
  - Fragen mit höherer Prüfungsrelevanz
- **Einfache Begriffsfragen** (`single`, Grundlagenwissen) bleiben eher **1 Punkt**.
- **Keine automatische** Punktevergabe nach Fragetyp allein – die Begründungsspalte ist maßgeblich.

---

## 5. Aktueller Fragenbestand (Pool vs. Vollsimulation)

| Sachgebiet | Vorhanden | Benötigt | Reserve | Anmerkung |
|------------|----------:|---------:|--------:|-----------|
| Recht der öffentlichen Sicherheit und Ordnung | 8 | 7 | **+1** | 1 Frage als rotierende Reserve |
| Gewerberecht | 8 | 5 | **+3** | 3 Fragen als Pool-/Reservefragen |
| Datenschutzrecht | 5 | 5 | 0 | Alle Fragen = Simulationskern |
| Bürgerliches Gesetzbuch | 13 | 13 | 0 | Alle Fragen = Simulationskern |
| Strafgesetzbuch und Strafverfahrensrecht | 13 | 13 | 0 | Alle Fragen = Simulationskern |
| Unfallverhütungsvorschriften Wach- und Sicherungsdienste | 8 | 8 | 0 | Alle Fragen = Simulationskern |
| Umgang mit Waffen | 5 | 5 | 0 | Alle Fragen = Simulationskern |
| Umgang mit Menschen | 19 | 19 | 0 | Alle Fragen = Simulationskern, alle 1 Punkt |
| Grundzüge der Sicherheitstechnik | 7 | 7 | 0 | Alle Fragen = Simulationskern |
| **Gesamt** | **86** | **82** | **+4** | |

**Besonderheit Reserve-Pools:**

- **Recht der öffentlichen Sicherheit und Ordnung:** 8 Fragen vorhanden, Vollsimulation braucht 7 → **1 Reserve** (`roso_004`). Die Auswahlfunktion (v24.3) muss Reservefragen **nicht** in den festen Simulationskern ziehen, kann sie aber für Variationen nutzen.
- **Gewerberecht:** 8 Fragen vorhanden, Vollsimulation braucht 5 → **3 Reserve** (`gewo_001`, `gewo_003`, `gewo_005`). Gleiche Logik für spätere Zufallsauswahl innerhalb des Pools.

---

## 6. Konkrete Punkteplanung pro Sachgebiet

**Legende:** Simulationskern **ja** = feste Prüfungsmenge (82 gesamt); **nein** = Reserve/Pool. Empfohlene Punkte gelten auch für Reservefragen (falls sie in Training oder Rotation genutzt werden).

---

### 6.1 Recht der öffentlichen Sicherheit und Ordnung (8 vorhanden → 7 Kern)

| ID | Kurzthema / Frage gekürzt | Punkte | Simulationskern | Begründung | Hinweis |
|----|---------------------------|-------:|:---------------:|------------|---------|
| roso_001 | Polizei im staatsrechtlichen Sinn | 1 | ja | Grundlagen-Multiple; eher Begriffsabfrage | Kern |
| roso_002 | Private Sicherheitsmitarbeiter rechtlich | 2 | ja | Multiple; Abgrenzung öffentlich/privat | Kern |
| roso_003 | Gefahrenabwehr grundsätzlich | 1 | ja | Multiple; Grundbegriff | Kern |
| roso_004 | Aussage zur öffentlichen Sicherheit | 1 | **nein** | Überlappt thematisch mit roso_003/007 | **Reserve** |
| roso_005 | Straftat im Objekt – Pflichten | 2 | ja | Multiple; praxisrelevante Pflichtenlage | Kern |
| v23_roso_006 | Grenze Sicherheitsdienst / Polizei | 1 | ja | Single; klare Abgrenzungsfrage, kompakt | Kern |
| v23_roso_007 | Kombination öffentliche Sicherheit (4 Aussagen) | 2 | ja | Combination; mehrere richtige Aussagen | Kern |
| v23_roso_008 | Fall EKZ – wiederholte Störung | 2 | ja | Multiple mit Fallbezug | Kern |

**Kern-Summe:** 7 Fragen · 11 Punkte (3×1 + 4×2) · 4 Zweipunktfragen

---

### 6.2 Gewerberecht (8 vorhanden → 5 Kern)

| ID | Kurzthema / Frage gekürzt | Punkte | Simulationskern | Begründung | Hinweis |
|----|---------------------------|-------:|:---------------:|------------|---------|
| gewo_001 | §-34a-GewO besonders wichtig | 1 | **nein** | Einfache Single-Grundlage | **Reserve** |
| gewo_002 | Gewerbsmäßiges Bewachen – Voraussetzungen | 2 | ja | Multiple; mehrere Aspekte | Kern |
| gewo_003 | Voraussetzung Bewachungsgewerbe | 1 | **nein** | Überlappt mit gewo_002/004 | **Reserve** |
| gewo_004 | Tätigkeit mit Sachkundeprüfung § 34a | 2 | ja | Multiple; Zuordnung Tätigkeiten | Kern |
| gewo_005 | Behörde bei fehlender Zuverlässigkeit | 1 | **nein** | Grundlagen-Multiple | **Reserve** |
| v23_gewo_006 | Sachkundeprüfung § 34a – Aussage | 1 | ja | Single; prüfungsrelevant, kompakt | Kern |
| v23_gewo_007 | Zuverlässigkeit – mehrere Aussagen | 2 | ja | Multiple; Abgrenzung | Kern |
| v23_gewo_008 | Fall Diskothek – Erlaubnispflicht | 2 | ja | Multiple mit Fallbezug | Kern |

**Kern-Summe:** 5 Fragen · 8 Punkte (2×1 + 3×2) · 3 Zweipunktfragen

---

### 6.3 Datenschutzrecht (5 vorhanden → 5 Kern)

| ID | Kurzthema / Frage gekürzt | Punkte | Simulationskern | Begründung | Hinweis |
|----|---------------------------|-------:|:---------------:|------------|---------|
| ds_001 | Datenschutz-Grundsatz | 1 | ja | Grundlagen-Multiple | Kern |
| ds_002 | Personenbezogene Daten | 1 | ja | Begriffs-Multiple | Kern |
| ds_003 | Videoüberwachung im Sicherheitsdienst | 2 | ja | Multiple; praxisrelevant, mehrere Pflichten | Kern |
| ds_004 | Auskunft über gespeicherte Daten | 2 | ja | Multiple; Betroffenenrechte | Kern |
| ds_005 | Problematische Handlung mit Daten | 2 | ja | Multiple; Abgrenzung erlaubt/unzulässig | Kern |

**Kern-Summe:** 5 Fragen · 8 Punkte (2×1 + 3×2) · 3 Zweipunktfragen

---

### 6.4 Bürgerliches Gesetzbuch (13 vorhanden → 13 Kern)

| ID | Kurzthema / Frage gekürzt | Punkte | Simulationskern | Begründung | Hinweis |
|----|---------------------------|-------:|:---------------:|------------|---------|
| bgb_001 | Was regelt das BGB? | 1 | ja | Einfache Single-Grundlage | Kern |
| bgb_002 | Rechte für Sicherheitsmitarbeiter im Objekt | 2 | ja | Multiple; Hausrecht/Besitz | Kern |
| bgb_003 | Fall: Besucher verlässt Gelände nicht | 2 | ja | Praxisfall; Hausrecht | Kern |
| bgb_004 | Kombination Hausrecht (4 Aussagen) | 2 | ja | Combination | Kern |
| bgb_005 | Schadensersatz – wann relevant? | 1 | ja | Single; Grundbegriff | Kern |
| bgb_006 | Fall: Vermietung Lagerhalle an Sicherheitsunternehmen | 2 | ja | Single mit Fall; Besitz/Miete | Kern |
| bgb_007 | Versiegelung ohne richterliche Anordnung | 1 | ja | Single; Abgrenzung Selbsthilfe | Kern |
| bgb_008 | Fall: Werkzeugkoffer – berechtigte Verteidigung | 2 | ja | Multiple mit Fall | Kern |
| bgb_009 | Fall: Kaufhaus – Hausrecht tagsüber | 2 | ja | Single mit Fallbezug | Kern |
| bgb_010 | Blockieren von Fahrzeugen ohne Titel | 1 | ja | Single; Selbsthilfe-Grenzen | Kern |
| bgb_011 | Fall: Faustschlag – Körperverletzung BGB | 2 | ja | Multiple mit Fall | Kern |
| bgb_012 | Kombination Notstand BGB (§ 228, § 904) | 2 | ja | Combination; Abgrenzung | Kern |
| bgb_013 | Fall: 17-jähriger Azubi – Minderjährigenhaftung | 1 | ja | Single mit Fall; § 828 BGB | Kern |

**Kern-Summe:** 13 Fragen · 21 Punkte (5×1 + 8×2) · 8 Zweipunktfragen

---

### 6.5 Strafgesetzbuch und Strafverfahrensrecht (13 vorhanden → 13 Kern)

| ID | Kurzthema / Frage gekürzt | Punkte | Simulationskern | Begründung | Hinweis |
|----|---------------------------|-------:|:---------------:|------------|---------|
| straf_001 | Was ist eine Straftat? | 1 | ja | Grundlagen-Single | Kern |
| straf_002 | Notwehr grundsätzlich | 2 | ja | Multiple; § 32 StGB | Kern |
| straf_003 | Fall: Ladendieb flieht – Festnahme | 2 | ja | Praxisfall; § 127 StPO | Kern |
| straf_004 | Kombination Notwehr (4 Aussagen) | 2 | ja | Combination | Kern |
| straf_005 | Körperverletzung grundsätzlich | 1 | ja | Grundlagen-Single | Kern |
| straf_006 | Fall: Baustelle – OWiG vs. Straftat | 2 | ja | Single mit Fall; wichtige Abgrenzung | Kern |
| straf_007 | Fall: Stolpern – Vorsatz/Fahrlässigkeit | 1 | ja | Single mit Fall | Kern |
| straf_008 | Fall: Betrunkener schlägt mit Flasche | 2 | ja | Multiple mit Fall; Notwehr | Kern |
| straf_009 | Fall: Brand – Gasflasche | 2 | ja | Single mit Fall; Notstand | Kern |
| straf_010 | Fall: Ladendieb – § 127 Abs. 1 StPO | 2 | ja | Multiple mit Fall | Kern |
| straf_011 | Fall: blauer Fleck – Körperverletzung | 1 | ja | Single mit Fall | Kern |
| straf_012 | Fall: Ausgang blockiert – Nötigung | 1 | ja | Single mit Fall; § 240 StGB | Kern |
| straf_013 | Kombination Diebstahl / Hausfriedensbruch | 2 | ja | Combination; Abgrenzung | Kern |

**Kern-Summe:** 13 Fragen · 21 Punkte (5×1 + 8×2) · 8 Zweipunktfragen

---

### 6.6 Unfallverhütungsvorschriften Wach- und Sicherungsdienste (8 vorhanden → 8 Kern)

| ID | Kurzthema / Frage gekürzt | Punkte | Simulationskern | Begründung | Hinweis |
|----|---------------------------|-------:|:---------------:|------------|---------|
| uvv_001 | Dienstanweisungen – Zweck | 1 | ja | Grundlagen-Single | Kern |
| uvv_002 | Dienstantritt – wichtige Punkte | 2 | ja | Multiple | Kern |
| uvv_003 | Fall: defekte Notbeleuchtung | 2 | ja | Praxisfall; Meldepflicht | Kern |
| uvv_004 | Kombination Eigenschutz (4 Aussagen) | 2 | ja | Combination | Kern |
| uvv_005 | SRS-Waffen – Aussage | 1 | ja | Single; Spezialthema kompakt | Kern |
| uvv_006 | Fall: neuer Objektauftrag – DGUV Vorschrift 23 | 1 | ja | Single mit Fall; Unternehmerpflichten | Kern |
| uvv_007 | Fall: Alkohol vor Dienstbeginn | 2 | ja | Multiple mit Fall; Dienstfähigkeit | Kern |
| uvv_008 | Fall: Knall/Rauch – akutes Vorkommnis | 2 | ja | Single mit Fall; Eigenschutz/Meldung | Kern |

**Kern-Summe:** 8 Fragen · 13 Punkte (3×1 + 5×2) · 5 Zweipunktfragen

---

### 6.7 Umgang mit Waffen (5 vorhanden → 5 Kern)

| ID | Kurzthema / Frage gekürzt | Punkte | Simulationskern | Begründung | Hinweis |
|----|---------------------------|-------:|:---------------:|------------|---------|
| waffen_001 | Anscheinswaffen | 1 | ja | Grundlagen-Single | Kern |
| waffen_002 | Waffenrecht – wichtige Punkte | 2 | ja | Multiple | Kern |
| waffen_003 | Fall: erlaubnispflichtige Schusswaffe im Dienst | 2 | ja | Praxisfall | Kern |
| waffen_004 | Kombination kleiner Waffenschein | 2 | ja | Combination | Kern |
| waffen_005 | Führen von Waffen – Aussage | 1 | ja | Grundlagen-Single | Kern |

**Kern-Summe:** 5 Fragen · 8 Punkte (2×1 + 3×2) · 3 Zweipunktfragen

---

### 6.8 Umgang mit Menschen (19 vorhanden → 19 Kern, alle 1 Punkt)

| ID | Kurzthema / Frage gekürzt | Punkte | Simulationskern | Begründung | Hinweis |
|----|---------------------------|-------:|:---------------:|------------|---------|
| umgang_001 | Verbale Konfliktsituation – ruhige Ansprache | 1 | ja | Grundlagen-Single | Kern; Prüfungsvorgabe 19/19 |
| umgang_002 | Professionelles Verhalten | 1 | ja | Multiple, aber Sachgebiet nur 1-Punkte-Fragen | Kern |
| umgang_003 | Fall: alkoholisierte aggressive Person | 1 | ja | Praxisfall; Gewichtung 1 Punkt laut Zielstruktur | Kern |
| umgang_004 | Kombination Deeskalation | 1 | ja | Combination; Sachgebiet ohne 2-Punkte-Fragen | Kern |
| umgang_005 | Gute Kommunikation | 1 | ja | Grundlagen-Single | Kern |
| umgang_006 | Fall: aggressiver Besucher Objekteingang | 1 | ja | Fall; Deeskalation | Kern |
| umgang_007 | Fall: Lieferant ohne Freigabe | 1 | ja | Fall; professionelle Kommunikation | Kern |
| umgang_008 | Fall: Beschwerde Wartezeit – aktives Zuhören | 1 | ja | Fall; Gesprächsführung | Kern |
| umgang_009 | Fall: Streit im Flur – Konflikt/Eigenschutz | 1 | ja | Fall; Eskalation | Kern |
| umgang_010 | Fall: alkoholisierter Gast Firmenfeier | 1 | ja | Fall; Alkohol | Kern |
| umgang_011 | Fall: Gedränge nach Konzert | 1 | ja | Fall; Menschenmenge | Kern |
| umgang_012 | Fall: internationaler Besucher – Sprache | 1 | ja | Fall; interkulturell | Kern |
| umgang_013 | Fall: Vorurteil im Funk | 1 | ja | Fall; respektvolle Ansprache | Kern |
| umgang_014 | Fall: Beleidigung – Selbstkontrolle | 1 | ja | Fall; Stress | Kern |
| umgang_015 | Fall: Nähe/Distanz Körpersprache | 1 | ja | Fall; Deeskalation | Kern |
| umgang_016 | Fall: Mieterbeschwerde | 1 | ja | Fall; Beschwerdemanagement | Kern |
| umgang_017 | Fall: Provokation Jugendliche/Film | 1 | ja | Fall; Provokation | Kern |
| umgang_018 | Fall: Fotos Sicherheitsbereich – Übergabe | 1 | ja | Fall; Teamkommunikation | Kern |
| umgang_019 | Fall: verbale Auseinandersetzung – Dokumentation | 1 | ja | Fall; Dokumentation | Kern |

**Kern-Summe:** 19 Fragen · 19 Punkte (19×1) · 0 Zweipunktfragen

---

### 6.9 Grundzüge der Sicherheitstechnik (7 vorhanden → 7 Kern)

| ID | Kurzthema / Frage gekürzt | Punkte | Simulationskern | Begründung | Hinweis |
|----|---------------------------|-------:|:---------------:|------------|---------|
| technik_001 | Grundzüge Sicherheitstechnik | 1 | ja | Grundlagen-Single | Kern |
| technik_002 | Technische Sicherheitseinrichtungen | 2 | ja | Multiple | Kern |
| technik_003 | Fall: BMA-Alarm ohne sichtbaren Rauch | 2 | ja | Praxisfall | Kern |
| technik_004 | Kombination Zutrittskontrolle | 2 | ja | Combination | Kern |
| technik_005 | Aufgabe Einbruchmeldeanlage | 1 | ja | Grundlagen-Single | Kern |
| technik_006 | Fall: EMA-Alarm Nacht – Verhalten | 1 | ja | Single mit Fall; Vertiefung EMA | Kern |
| technik_007 | Videoüberwachung und Zutrittskontrolle | 2 | ja | Multiple; Datenschutz/Technik | Kern |

**Kern-Summe:** 7 Fragen · 11 Punkte (3×1 + 4×2) · 4 Zweipunktfragen

---

## 7. Qualitätsprüfung

| Prüfung | Ziel | Ergebnis |
|---------|-----:|---------:|
| Simulationskern Fragen | 82 | **82** |
| Simulationskern Punkte | 120 | **120** |
| Zweipunktfragen | 38 | **38** |
| Einpunktfragen | 44 | **44** |
| Umgang mit Menschen Punkte | 19 | **19** |

### Prüfung je Sachgebiet (Simulationskern)

| Sachgebiet | Fragen | Punkte | 2-Pkt | 1-Pkt |
|------------|-------:|-------:|------:|------:|
| Recht der öffentlichen Sicherheit und Ordnung | 7 | 11 | 4 | 3 |
| Gewerberecht | 5 | 8 | 3 | 2 |
| Datenschutzrecht | 5 | 8 | 3 | 2 |
| Bürgerliches Gesetzbuch | 13 | 21 | 8 | 5 |
| Strafgesetzbuch und Strafverfahrensrecht | 13 | 21 | 8 | 5 |
| UVV Wach- und Sicherungsdienste | 8 | 13 | 5 | 3 |
| Umgang mit Waffen | 5 | 8 | 3 | 2 |
| Umgang mit Menschen | 19 | 19 | 0 | 19 |
| Grundzüge der Sicherheitstechnik | 7 | 11 | 4 | 3 |
| **Gesamt** | **82** | **120** | **38** | **44** |

### Reservefragen (nicht im festen Kern)

| ID | Sachgebiet | Geplante Punkte | Rolle |
|----|------------|----------------:|-------|
| roso_004 | Recht der öffentlichen Sicherheit und Ordnung | 1 | Reserve (Rotation/Pool) |
| gewo_001 | Gewerberecht | 1 | Reserve |
| gewo_003 | Gewerberecht | 1 | Reserve |
| gewo_005 | Gewerberecht | 1 | Reserve |

---

## 8. Umsetzung später

| Task | Inhalt |
|------|--------|
| **v24.2** | Feste 82 Core-IDs dokumentiert (`docs/EXAM_CORE_SELECTION_PLAN.md`) |
| **v24.3a–f** | `points`-Felder je Sachgebiet in `questions.json` ergänzen |
| **v24.3x** | **Teilpunkte-Bewertung** auditiert (§10) – **kein Code** |
| **v24.4** | Restliche `points`-Felder fertigstellen |
| **v24.5** | Teilpunkte-Logik technisch prüfen und umsetzen |
| **v24.6** | Vollsimulation **82/120** mit Teilbewertung testen |

**v24.1:** Fachliche Punkteplanung – **keine** automatische JSON-Umsetzung in einem Schritt.

---

## 9. Wichtig

- **Keine automatische Umsetzung** – jede `points`-Zuweisung in v24.2 manuell bzw. kontrolliert aus diesem Plan übernehmen.
- **Keine Änderung** an `questions.json` in v24.1.
- Diese Datei ist die **fachliche Planungsgrundlage** für v24.2 ff.
- Reservefragen erhalten ebenfalls geplante Punkte (für Training), sind aber **nicht** Teil des festen 82-Fragen-Kerns.

---

## 10. Teilpunkte-Bewertung (Audit v24.3x, ab 01.07.2025)

**Hinweis:** Nur Dokumentation – **keine** Änderung an `questions.json` und **kein Code** in v24.3x.

### 10.1 Bewertungsgrundlage

| Merkmal | Vorgabe |
|---------|---------|
| Gültig ab | **01.07.2025** |
| Teilrichtige Antworten | **werden berücksichtigt** |
| Pro richtige Lösung | **1 Punkt** |
| Aufgabe mit 2 richtigen Lösungen | **max. 2 Punkte** |
| Nur 1 von 2 richtig | **1 Punkt** möglich |
| Maximal schriftlich | **120 Punkte** |
| Bestehen | **50 %** = **60 Punkte** |

### 10.2 Konsequenz für die App und `points`-Feld

- Mehrfachantworten dürfen **nicht** nur binär (ganz richtig / ganz falsch) ausgewertet werden.
- Die App muss später **Teilpunkte** berechnen (`docs/EXAM_SIMULATION_AUDIT.md` §10).
- **`points`** = maximale erreichbare Punkte der Frage; soll zur **Anzahl richtiger Antworten** passen:
  - **1** richtige Lösung → in der Regel `points: 1`
  - **2** richtige Lösungen → in der Regel `points: 2`
- Die Tabellen in §6 dieses Plans ordnen `points: 1` oder `points: 2` **fachlich** – nicht automatisch nach `type`.

### 10.3 Noch offen zu prüfen

- Bewertung **falscher Zusatzmarkierungen** (nur ignorieren vs. Punktabzug).
- Fachliche Entscheidung **vor** Code-Task v24.5.

### 10.4 Vorläufige technische Zielregel (Code-Task v24.5)

- **Single:** richtige Antwort = volle Punkte · falsche Antwort = 0 Punkte.
- **Multiple:** pro korrekt gesetztem Kreuz = 1 Punkt · falsche Zusatzantworten nicht belohnen · Abzugslogik **separat** festlegen.

---

## Verweise

- `docs/EXAM_SIMULATION_AUDIT.md` – Ist-Stand Vollsimulation (v24.0)
- `docs/PROJECT_MASTERLIST.md` – §7 Prüfungsaufbau, §8.2
- `docs/WRITTEN_QUESTION_EXPANSION_PLAN.md` – Fragenbank-Ausbau

---

*Accaoui-eigene Trainingsfragen – keine 1:1-Übernahme aus IHK- oder Musterprüfungen.*
