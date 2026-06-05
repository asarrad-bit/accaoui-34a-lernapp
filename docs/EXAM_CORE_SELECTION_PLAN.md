# Accaoui §34a – Core-ID-Liste für Vollsimulation (Option A)

Stand: **v24.2** (Dokumentation, keine Umsetzung)
Projekt: Accaoui §34a Lern-App
Grundlage: `docs/EXAM_POINTS_PLAN.md`, `docs/EXAM_SIMULATION_AUDIT.md`, `questions.json` (86 Fragen, nur gelesen)

**Hinweis:** Diese Datei definiert den **festen Simulationskern**. In v24.2 werden **keine** App-Dateien und **keine** `questions.json`-Einträge geändert.

---

## 1. Zweck

- Vorbereitung der **echten schriftlichen Vollsimulation** nach §-34a-Struktur.
- Die Vollsimulation soll **exakt 82 Fragen** ziehen.
- Diese Datei definiert den **festen Simulationskern** (Core-ID-Liste).
- **Keine technische Umsetzung** in diesem Task.

---

## 2. Grundentscheidung

### Option A (gewählt)

Die Vollsimulation verwendet später eine **feste Core-ID-Liste**.

| Aspekt | Regel |
|--------|--------|
| `questions.json` | Bleibt **Trainingspool** (aktuell 86 Fragen) |
| Vollsimulation | Nutzt **nur** die 82 Kern-IDs aus dieser Datei |
| Reservefragen | Bleiben für Training, Lernkarten, Themenübungen und **spätere** Rotation verfügbar |

**Abgrenzung zu Option B (nicht gewählt):** Zufallsauswahl pro Sachgebiet aus dem Pool ohne feste ID-Liste. Option A ist **deterministisch**, **prüfbar** und passt zum Punkteplan in `docs/EXAM_POINTS_PLAN.md`.

---

## 3. Zielstruktur

| Sachgebiet | Kernfragen |
|------------|----------:|
| Recht der öffentlichen Sicherheit und Ordnung | 7 |
| Gewerberecht | 5 |
| Datenschutzrecht | 5 |
| Bürgerliches Gesetzbuch | 13 |
| Strafgesetzbuch und Strafverfahrensrecht | 13 |
| Unfallverhütungsvorschriften Wach- und Sicherungsdienste | 8 |
| Umgang mit Waffen | 5 |
| Umgang mit Menschen | 19 |
| Grundzüge der Sicherheitstechnik | 7 |
| **Gesamt** | **82** |

---

## 4. Feste Core-IDs nach Sachgebiet

### Recht der öffentlichen Sicherheit und Ordnung (7 Kern)

- `roso_001`
- `roso_002`
- `roso_003`
- `roso_005`
- `v23_roso_006`
- `v23_roso_007`
- `v23_roso_008`

**Reserve (1):**

- `roso_004`

---

### Gewerberecht (5 Kern)

- `gewo_002`
- `gewo_004`
- `v23_gewo_006`
- `v23_gewo_007`
- `v23_gewo_008`

**Reserve (3):**

- `gewo_001`
- `gewo_003`
- `gewo_005`

---

### Datenschutzrecht (5 Kern)

- `ds_001`
- `ds_002`
- `ds_003`
- `ds_004`
- `ds_005`

---

### Bürgerliches Gesetzbuch (13 Kern)

- `bgb_001`
- `bgb_002`
- `bgb_003`
- `bgb_004`
- `bgb_005`
- `bgb_006`
- `bgb_007`
- `bgb_008`
- `bgb_009`
- `bgb_010`
- `bgb_011`
- `bgb_012`
- `bgb_013`

---

### Strafgesetzbuch und Strafverfahrensrecht (13 Kern)

- `straf_001`
- `straf_002`
- `straf_003`
- `straf_004`
- `straf_005`
- `straf_006`
- `straf_007`
- `straf_008`
- `straf_009`
- `straf_010`
- `straf_011`
- `straf_012`
- `straf_013`

---

### Unfallverhütungsvorschriften Wach- und Sicherungsdienste (8 Kern)

- `uvv_001`
- `uvv_002`
- `uvv_003`
- `uvv_004`
- `uvv_005`
- `uvv_006`
- `uvv_007`
- `uvv_008`

---

### Umgang mit Waffen (5 Kern)

- `waffen_001`
- `waffen_002`
- `waffen_003`
- `waffen_004`
- `waffen_005`

---

### Umgang mit Menschen (19 Kern)

- `umgang_001`
- `umgang_002`
- `umgang_003`
- `umgang_004`
- `umgang_005`
- `umgang_006`
- `umgang_007`
- `umgang_008`
- `umgang_009`
- `umgang_010`
- `umgang_011`
- `umgang_012`
- `umgang_013`
- `umgang_014`
- `umgang_015`
- `umgang_016`
- `umgang_017`
- `umgang_018`
- `umgang_019`

---

### Grundzüge der Sicherheitstechnik (7 Kern)

- `technik_001`
- `technik_002`
- `technik_003`
- `technik_004`
- `technik_005`
- `technik_006`
- `technik_007`

---

### Vollständige Core-ID-Liste (82, maschinenlesbar)

```txt
roso_001,roso_002,roso_003,roso_005,v23_roso_006,v23_roso_007,v23_roso_008,
gewo_002,gewo_004,v23_gewo_006,v23_gewo_007,v23_gewo_008,
ds_001,ds_002,ds_003,ds_004,ds_005,
bgb_001,bgb_002,bgb_003,bgb_004,bgb_005,bgb_006,bgb_007,bgb_008,bgb_009,bgb_010,bgb_011,bgb_012,bgb_013,
straf_001,straf_002,straf_003,straf_004,straf_005,straf_006,straf_007,straf_008,straf_009,straf_010,straf_011,straf_012,straf_013,
uvv_001,uvv_002,uvv_003,uvv_004,uvv_005,uvv_006,uvv_007,uvv_008,
waffen_001,waffen_002,waffen_003,waffen_004,waffen_005,
umgang_001,umgang_002,umgang_003,umgang_004,umgang_005,umgang_006,umgang_007,umgang_008,umgang_009,umgang_010,umgang_011,umgang_012,umgang_013,umgang_014,umgang_015,umgang_016,umgang_017,umgang_018,umgang_019,
technik_001,technik_002,technik_003,technik_004,technik_005,technik_006,technik_007
```

**Reserve-IDs (4):** `roso_004`, `gewo_001`, `gewo_003`, `gewo_005`

---

## 5. Kontrollsummen

| Prüfung | Ziel | Ergebnis |
|---------|-----:|---------:|
| Core-ID-Anzahl | 82 | **82** |
| Reserve-ID-Anzahl | 4 | **4** |
| Recht Kern | 7 | **7** |
| Gewerbe Kern | 5 | **5** |
| Umgang mit Menschen Kern | 19 | **19** |
| Alle Core-IDs in `questions.json` | 82/82 | **82/82** (v24.2 geprüft) |
| Doppelte Core-IDs | 0 | **0** |

### Kontrolle je Sachgebiet

| Sachgebiet | Kern-IDs | Reserve |
|------------|--------:|--------:|
| Recht der öffentlichen Sicherheit und Ordnung | 7 | 1 |
| Gewerberecht | 5 | 3 |
| Datenschutzrecht | 5 | 0 |
| Bürgerliches Gesetzbuch | 13 | 0 |
| Strafgesetzbuch und Strafverfahrensrecht | 13 | 0 |
| UVV Wach- und Sicherungsdienste | 8 | 0 |
| Umgang mit Waffen | 5 | 0 |
| Umgang mit Menschen | 19 | 0 |
| Grundzüge der Sicherheitstechnik | 7 | 0 |
| **Gesamt** | **82** | **4** |

**Fragenbank gesamt:** 86 Fragen = 82 Kern + 4 Reserve.

---

## 6. Technische Regel für spätere Umsetzung

Die spätere Vollsimulation darf **nicht** mehr nur `shuffleArray([...allQuestions]).slice(0, 82)` verwenden.

Sie muss stattdessen:

1. die **Core-ID-Liste** laden (aus dieser Datei oder daraus abgeleiteter Konstante),
2. **genau diese 82 Fragen** aus `questions.json` finden,
3. **fehlende IDs** als Fehler melden,
4. **doppelte IDs** verhindern,
5. **Kategorieanzahl** prüfen (7/5/5/13/13/8/5/19/7),
6. **Punkte** später aus dem `points`-Feld berechnen (nach `docs/EXAM_POINTS_PLAN.md`).

**Reihenfolge in der Prüfung:** Kann nach Sachgebiet sortiert oder gemischt werden – das ist eine **separate** UX-Entscheidung in v24.4. Die **Menge** der IDs ist fest.

---

## 7. Spätere Tasks

| Task | Inhalt |
|------|--------|
| **v24.3** | `points`-Felder auf Grundlage von `docs/EXAM_POINTS_PLAN.md` **kontrolliert** in `questions.json` ergänzen |
| **v24.4** | Core-ID-Auswahlfunktion in der App vorbereiten |
| **v24.5** | Vollsimulation **82 Fragen / 120 Punkte** testen |
| **v24.6** | Browser- und Online-Test dokumentieren |

**v24.2 (dieser Task):** Nur Core-ID-Plan – **kein Code**, keine `questions.json`-Änderung.

---

## 8. Wichtige Regel

- **Keine automatische Rotation** in der ersten Umsetzung.
- **Reservefragen bleiben Reserve** – nicht Teil der Vollsimulation v1.
- **Spätere Rotation** erst nach **stabiler Kernsimulation**.
- **`points`-Felder** folgen **erst nach** dieser Core-ID-Planung (v24.3), nicht vorher.

---

## Verweise

- `docs/EXAM_POINTS_PLAN.md` – Punkte 1/2 pro Kern-ID (v24.1)
- `docs/EXAM_SIMULATION_AUDIT.md` – Ist-Stand App (v24.0)
- `docs/PROJECT_MASTERLIST.md` – §7 Prüfungsaufbau, §8.2

---

*Accaoui-eigene Trainingsfragen – keine 1:1-Übernahme aus IHK- oder Musterprüfungen.*
