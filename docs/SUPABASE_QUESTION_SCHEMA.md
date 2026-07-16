# Accaoui §34a Lern-App – Supabase-Fragen-Datenmodell (Planung)

Stand: v23.5.7
Zweck: Technische Planungsgrundlage für das spätere Supabase/Postgres-Datenmodell der Fragenbank.
Bezug: `docs/CURSOR_MASTER_CONTEXT_ACCAOUI.md`, `docs/QUESTION_DATABASE_PLAN.md`, `docs/WRITTEN_QUESTION_STANDARD.md`

---

## 1. Zweck des Supabase-Fragenmodells

Das Supabase-Fragenmodell soll die Accaoui §34a Lern-App langfristig von festen JSON-/JS-Dateien auf eine professionelle, rollenbasierte Fragenverwaltung umstellen.

Konkrete Ziele:

1. **Rohmaterial und Veröffentlichung trennen** – Importe und Analyse bleiben intern; die App sieht nur freigegebene Inhalte.
2. **Schriftliche und mündliche Fragen einheitlich verwalten** – inklusive Review, Versionierung und Status-Workflow.
3. **Prüfungsbögen skalierbar abbilden** – mündliche Simulationen (A, B, C, …) über `oral_exam_sheets` und Zuordnungstabellen.
4. **Rechtssicherheit** – keine 1:1-Übernahme offizieller oder fremder Prüfungsfragen; nur `accaoui_original` wird exportiert.
5. **Vorbereitung für Auth und Fortschritt** – Fragen in Supabase; Lernfortschritt später getrennt pro `user_id` (eigene Tabellen, nicht in Fragentexten).
6. **Kontrollierter Export** – veröffentlichte Fragen werden gezielt nach `questions.json`, `data/oral-question-bank.js` und `data/oral-sheets-bank.js` exportiert.

Dieses Dokument beschreibt **nur** das geplante Schema und die Regeln. Es enthält kein SQL, keine Migration und keine App-Anbindung.

---

## 2. Grundregel: Rohfragen vs. veröffentlichte Fragen

| Ebene | Speicherort (geplant) | Sichtbarkeit | Verwendung |
|--------|------------------------|--------------|------------|
| **Rohmaterial** | `question_imports`, `raw_questions` | Nur Admin (Import/Archiv); Dozent ggf. lesend zur Prüfung | Analyse, Lernziele, Umformulierung |
| **Accaoui-Fragen** | `written_questions`, `oral_questions` | Teilnehmer nur bei `status = published` | Lern-App, Export |

**Verbindliche Regel:**

- Rohfragen bleiben **intern** und werden **niemals** direkt an Teilnehmer oder in Export-Dateien ausgeliefert.
- Veröffentlicht werden **nur** geprüfte, eigen formulierte Accaoui-Fragen mit `source_style = accaoui_original` und `status = published`.
- Musterprüfungen und IHK-nahe Unterlagen sind ausschließlich **Analysequelle** (siehe Master Context §8).

---

## 3. Tabellenübersicht

| Tabelle | Zweck | Beziehung zu anderen Tabellen |
|---------|--------|-------------------------------|
| `question_imports` | Ein Import-Vorgang (Datei/Batch, Metadaten, Rechtshinweis) | 1:n → `raw_questions` |
| `raw_questions` | Interne Roh- bzw. Ausgangsfragen aus Importen | n:1 ← `question_imports`; optional Vorlage für neue `written_questions` / `oral_questions` |
| `written_questions` | Geprüfte schriftliche Accaoui-Fragen | 1:n → `question_reviews`, `question_versions` |
| `oral_questions` | Geprüfte mündliche Accaoui-Fragen | 1:n → `question_reviews`, `question_versions`; n:m über `oral_exam_sheet_questions` |
| `question_reviews` | Prüfschritte und Kommentare pro Frage | n:1 → `written_questions` oder `oral_questions` (über `question_mode`) |
| `question_versions` | Historie bei inhaltlichen Änderungen | n:1 → `written_questions` oder `oral_questions` |
| `oral_exam_sheets` | Prüfungsbogen (z. B. Simulation A/B/C) | 1:n → `oral_exam_sheet_questions` |
| `oral_exam_sheet_questions` | Frageposition auf einem Bogen (1–15, Prüferrolle) | n:1 ← `oral_exam_sheets`, `oral_questions` |

**Hinweis:** Tabellen für Nutzer, Kurse und Fortschritt (`profiles`, `courses`, `user_question_progress`, …) gehören zur späteren Auth-/Lernarchitektur und sind hier nicht spezifiziert, werden aber über RLS mit diesem Modell verknüpft.

---

## 4. Felder: `question_imports`

Dokumentiert einen Import-Batch (z. B. hochgeladene Musterprüfung, Excel, manueller Stapel).

| Feld | Typ (geplant) | Pflicht | Beschreibung |
|------|----------------|---------|--------------|
| `id` | `uuid` | ja | Primärschlüssel |
| `import_title` | `text` | ja | Bezeichnung des Imports (z. B. „Musterprüfung Analyse 2026-05“) |
| `import_type` | `text` | ja | z. B. `pdf`, `docx`, `xlsx`, `manual`, `json_legacy` |
| `source_note` | `text` | nein | Interne Notiz zur Herkunft |
| `copyright_note` | `text` | nein | Urheber-/Nutzungshinweis |
| `usage_allowed` | `boolean` | ja | Darf nur zur internen Analyse genutzt werden (`true` = intern erlaubt) |
| `ihk_similarity_flag` | `boolean` | nein | Markierung: Quelle ist IHK-/Musterprüfungs-nah |
| `file_path` | `text` | nein | Referenz auf abgelegte Datei (Storage, nicht öffentlich) |
| `record_count` | `integer` | nein | Anzahl erzeugter `raw_questions` |
| `status` | `text` | ja | z. B. `imported`, `processing`, `completed`, `archived` |
| `imported_by` | `uuid` | ja | FK → `auth.users` / Admin-Profil |
| `imported_at` | `timestamptz` | ja | Zeitpunkt des Imports |
| `archived_at` | `timestamptz` | nein | Archivierung des Imports |

---

## 5. Felder: `raw_questions`

Interne Rohfragen – **nicht** für Export oder Teilnehmer-App.

| Feld | Typ (geplant) | Pflicht | Beschreibung |
|------|----------------|---------|--------------|
| `id` | `uuid` | ja | Primärschlüssel |
| `import_id` | `uuid` | ja | FK → `question_imports.id` |
| `legacy_id` | `text` | nein | Alte Nummer/ID aus Quelldatei |
| `mode` | `text` | ja | `written` oder `oral` |
| `topic` | `text` | ja | Kanonisches Sachgebiet (9 Kategorien) |
| `subtopic` | `text` | nein | Feineres Thema |
| `raw_question_text` | `text` | ja | Original- oder Ausgangsfragetext |
| `raw_answers` | `jsonb` | nein | Roh-Antwortoptionen (schriftlich) |
| `raw_correct_answer` | `text` | nein | Roh-Lösungshinweis |
| `raw_model_answer` | `text` | nein | Roh-Musterantwort (mündlich) |
| `points` | `smallint` | nein | Punktzahl aus Quelle (1 oder 2) |
| `question_type` | `text` | nein | z. B. `single`, `multiple`, `praxisfall`, `combination` |
| `similarity_risk` | `text` | nein | `low`, `medium`, `high` (IHK-Ähnlichkeit) |
| `status` | `text` | ja | Siehe Status-Stufen (Rohpfad: oft `imported` … `archived`) |
| `linked_written_id` | `uuid` | nein | FK → `written_questions.id`, wenn daraus umformuliert |
| `linked_oral_id` | `uuid` | nein | FK → `oral_questions.id`, wenn daraus umformuliert |
| `notes` | `text` | nein | Interne Bearbeitungsnotiz |
| `created_at` | `timestamptz` | ja | |
| `updated_at` | `timestamptz` | ja | |

---

## 6. Felder: `written_questions`

Geprüfte schriftliche Accaoui-Fragen; entspricht langfristig `docs/WRITTEN_QUESTION_STANDARD.md` und App-Feld `questions.json`.

| Feld | Typ (geplant) | Pflicht | Beschreibung |
|------|----------------|---------|--------------|
| `id` | `uuid` | ja | Primärschlüssel |
| `public_id` | `text` | ja | Eindeutige App-ID (z. B. `q_083`), unique |
| `mode` | `text` | ja | Konstant `written` |
| `topic` | `text` | ja | Kanonisches Sachgebiet |
| `subtopic` | `text` | nein | |
| `question_type` | `text` | ja | `single`, `multiple`, `praxisfall`, `combination` |
| `points` | `smallint` | ja | `1` oder `2` |
| `difficulty` | `text` | ja | z. B. `leicht`, `mittel`, `schwer` |
| `exam_relevance` | `text` | ja | z. B. `niedrig`, `mittel`, `hoch` |
| `ihk_similarity_risk` | `text` | ja | Bewertung nach Review |
| `source_style` | `text` | ja | Pflicht für Export: `accaoui_original` |
| `question` | `text` | ja | Fragetext |
| `answers` | `jsonb` | ja | Array `{ id, text }` (a–d / a–e) |
| `correct_answers` | `jsonb` | ja | Array der richtigen Buchstaben-IDs |
| `explanation` | `text` | ja | Lern-Erklärung |
| `status` | `text` | ja | Workflow-Status (siehe §12) |
| `raw_question_id` | `uuid` | nein | FK → `raw_questions.id` (Herkunft) |
| `created_by` | `uuid` | nein | FK → Bearbeiter |
| `reviewed_by` | `uuid` | nein | FK → letzter Prüfer |
| `approved_by` | `uuid` | nein | FK → Freigeber (Admin) |
| `published_at` | `timestamptz` | nein | Zeitpunkt Veröffentlichung |
| `archived_at` | `timestamptz` | nein | |
| `created_at` | `timestamptz` | ja | |
| `updated_at` | `timestamptz` | ja | |

**Export-Mapping (geplant):** `public_id` → `id`, `topic` → `category`, `correct_answers` → `correctAnswers` in `questions.json`.

---

## 7. Felder: `oral_questions`

Geprüfte mündliche Accaoui-Fragen für Training und Prüfungssimulation.

| Feld | Typ (geplant) | Pflicht | Beschreibung |
|------|----------------|---------|--------------|
| `id` | `uuid` | ja | Primärschlüssel |
| `public_id` | `text` | ja | Eindeutige App-ID (z. B. `oral_q_042`), unique |
| `mode` | `text` | ja | Konstant `oral` |
| `topic` | `text` | ja | Kanonisches Sachgebiet |
| `subtopic` | `text` | nein | |
| `examiner_question` | `text` | ja | Prüferfrage |
| `model_answer` | `text` | ja | Musterantwort |
| `follow_up_questions` | `jsonb` | nein | Array typischer Folgefragen |
| `examiner_notes` | `text` | nein | Hinweise für Dozenten/Review |
| `critical_mistakes` | `jsonb` | nein | Array häufiger Fehler |
| `difficulty` | `text` | ja | |
| `exam_relevance` | `text` | ja | |
| `ihk_similarity_risk` | `text` | ja | |
| `source_style` | `text` | ja | Pflicht für Export: `accaoui_original` |
| `status` | `text` | ja | Workflow-Status |
| `raw_question_id` | `uuid` | nein | FK → `raw_questions.id` |
| `created_by` | `uuid` | nein | |
| `reviewed_by` | `uuid` | nein | |
| `approved_by` | `uuid` | nein | |
| `published_at` | `timestamptz` | nein | |
| `archived_at` | `timestamptz` | nein | |
| `created_at` | `timestamptz` | ja | |
| `updated_at` | `timestamptz` | ja | |

---

## 8. Felder: `question_reviews`

Dokumentiert einzelne Prüfschritte; mehrere Zeilen pro Frage möglich.

| Feld | Typ (geplant) | Pflicht | Beschreibung |
|------|----------------|---------|--------------|
| `id` | `uuid` | ja | Primärschlüssel |
| `question_id` | `uuid` | ja | FK → `written_questions` oder `oral_questions` |
| `question_mode` | `text` | ja | `written` oder `oral` |
| `review_step` | `text` | ja | z. B. `fachlich`, `dublette`, `ihk_risk`, `formulierung`, `antwortlogik`, `erklaerung`, `freigabe` |
| `review_status` | `text` | ja | `open`, `passed`, `failed`, `needs_change` |
| `reviewer_note` | `text` | nein | Kommentar des Dozenten/Admins |
| `reviewed_by` | `uuid` | ja | FK → `auth.users` |
| `reviewed_at` | `timestamptz` | ja | |

---

## 9. Felder: `question_versions`

Versionierung bei inhaltlichen Änderungen an freigegebenen oder veröffentlichten Fragen.

| Feld | Typ (geplant) | Pflicht | Beschreibung |
|------|----------------|---------|--------------|
| `id` | `uuid` | ja | Primärschlüssel |
| `question_id` | `uuid` | ja | FK → `written_questions` oder `oral_questions` |
| `question_mode` | `text` | ja | `written` oder `oral` |
| `version_number` | `integer` | ja | Fortlaufend pro Frage |
| `snapshot` | `jsonb` | ja | Vollständiger Inhaltssnapshot zum Zeitpunkt |
| `change_summary` | `text` | nein | Kurzbeschreibung der Änderung |
| `status_at_version` | `text` | ja | Status zum Zeitpunkt der Version |
| `created_by` | `uuid` | ja | |
| `created_at` | `timestamptz` | ja | |

---

## 10. Felder: `oral_exam_sheets`

Repräsentiert einen mündlichen Prüfungsbogen (Simulation A, B, C, …).

| Feld | Typ (geplant) | Pflicht | Beschreibung |
|------|----------------|---------|--------------|
| `id` | `uuid` | ja | Primärschlüssel |
| `sheet_code` | `text` | ja | z. B. `A`, `B`, `C` (unique) |
| `sheet_title` | `text` | ja | Anzeigename (z. B. „Simulation B“) |
| `description` | `text` | nein | Kurzbeschreibung für UI |
| `duration_minutes` | `smallint` | ja | Standard: `15` |
| `question_count` | `smallint` | ja | Standard: `15` |
| `structure_note` | `text` | nein | z. B. Prüfer 1 (1–5), Vorsitz (6–10), Prüfer 3 (11–15) |
| `status` | `text` | ja | `draft`, `approved`, `published`, `archived` |
| `sort_order` | `integer` | nein | Reihenfolge in der App-Auswahl |
| `published_at` | `timestamptz` | nein | |
| `created_at` | `timestamptz` | ja | |
| `updated_at` | `timestamptz` | ja | |

---

## 11. Felder: `oral_exam_sheet_questions`

Verknüpft mündliche Fragen mit einem Bogen in fester Reihenfolge.

| Feld | Typ (geplant) | Pflicht | Beschreibung |
|------|----------------|---------|--------------|
| `id` | `uuid` | ja | Primärschlüssel |
| `sheet_id` | `uuid` | ja | FK → `oral_exam_sheets.id` |
| `oral_question_id` | `uuid` | ja | FK → `oral_questions.id` |
| `position` | `smallint` | ja | 1–15 auf dem Bogen |
| `examiner_role` | `text` | ja | `examiner_1`, `chair`, `examiner_3` |
| `phase_label` | `text` | nein | Optional für UI (z. B. „Prüfer 1 fragt“) |
| `is_active` | `boolean` | ja | Frage auf diesem Bogen aktiv |
| `created_at` | `timestamptz` | ja | |

**Constraint (geplant):** `unique (sheet_id, position)` und `unique (sheet_id, oral_question_id)`.

---

## 12. Status-Stufen

Einheitlicher Workflow für `raw_questions`, `written_questions` und `oral_questions` (soweit anwendbar):

| Status | Bedeutung | Wer setzt | Export / App |
|--------|-----------|-----------|----------------|
| `imported` | Neu importiert, noch nicht geprüft | Admin (Import) | Nein |
| `needs_review` | Zur fachlichen Prüfung vorgesehen | Admin / System | Nein |
| `rewrite_required` | Umformulierung nötig (z. B. hohes Ähnlichkeitsrisiko) | Dozent / Admin | Nein |
| `reviewed` | Fachlich geprüft, noch nicht final freigegeben | Dozent | Nein |
| `approved` | Freigegeben, noch nicht live | Admin | Nein (nur intern/vorbereitet) |
| `published` | In der App und für Export freigegeben | Admin | Ja (mit Export-Regeln §15) |
| `archived` | Nicht mehr aktiv, Historie bleibt | Admin | Nein |

**Übergänge (vereinfacht):**

```txt
imported → needs_review → reviewed → approved → published
                ↓              ↑
         rewrite_required ─────┘
published / approved → archived
```

Nur `published` ist für **Teilnehmer-Lesezugriff** und **Export** vorgesehen (`oral_exam_sheets`: analog `published` für Bogen-Export).

---

## 13. Rollen

Rollen werden über Supabase Auth + `profiles.role` (oder JWT-Custom-Claim) abgebildet.

| Rolle | Fragenbank – Lesen | Fragenbank – Schreiben | Typische Aufgaben |
|-------|--------------------|-------------------------|-------------------|
| **Teilnehmer** | Nur `written_questions` / `oral_questions` mit `status = published`; veröffentlichte Bögen | Keine Frageninhalte | Lernen, Prüfungssimulation, eigener Fortschritt (spätere Tabellen) |
| **Dozent** | Rohfragen (lesend), alle Accaoui-Fragen außer Löschung/Archiv; Reviews | `question_reviews` anlegen/aktualisieren; Status bis `reviewed` / Kommentar `rewrite_required` | Fachprüfung, Dubletten, Formulierung |
| **Admin** | Vollzugriff auf alle Tabellen dieses Modells | Import, Anlegen/Umformulieren, `approved`, `published`, `archived`; Versionen | Import, Freigabe, Export-Vorbereitung, Archiv |

**Service Role Key:** nur serverseitig (Edge Functions, Export-Tool), **niemals** im Frontend.

---

## 14. Row-Level-Security – Grundidee

RLS wird auf allen Tabellen dieses Modells aktiviert. Grobe Policy-Richtung:

### Teilnehmer

- **SELECT** auf `written_questions`, `oral_questions`: nur `status = 'published'`.
- **SELECT** auf `oral_exam_sheets` + `oral_exam_sheet_questions`: nur veröffentlichte Bögen und zugehörige veröffentlichte Fragen.
- **Kein Zugriff** auf `question_imports`, `raw_questions`, `question_reviews`, `question_versions` (außer ggf. aggregierte, anonyme Statistiken später – nicht im Fragenmodell).
- Fortschritt, Prüfungsergebnisse, Fehlerhistorie: **eigene Tabellen**, Policy `user_id = auth.uid()`.

### Dozent

- **SELECT** auf Roh- und Accaoui-Tabellen (ohne Service-Role-Bypass).
- **INSERT/UPDATE** auf `question_reviews`.
- **UPDATE** auf `written_questions` / `oral_questions` nur bis Status `reviewed` / Kommentarfelder; **kein** Setzen von `published` oder `archived`.
- **Kein** DELETE auf Importen; Archivierung nur Admin.

### Admin

- Voller CRUD auf `question_imports`, `raw_questions`, Fragen, Reviews, Versionen, Bögen.
- Einzige Rolle, die `status` auf `approved`, `published`, `archived` setzen und Imports ausführen darf.

### Allgemein

- Policies nutzen `auth.uid()` und Rolle aus `profiles`.
- Anon-Key im Frontend: nur Policies erlauben, die für eingeloggte Teilnehmer definiert sind.
- Export-Jobs laufen mit Service Role oder dediziertem Admin-Backend, nicht mit Teilnehmer-Session.

---

## 15. Export-Regel

Export aus Supabase in die bestehenden App-Dateien ist **nur** erlaubt, wenn **beide** Bedingungen erfüllt sind:

1. `status = 'published'`
2. `source_style = 'accaoui_original'`

Zusätzlich für mündliche Bögen:

- `oral_exam_sheets.status = 'published'`
- Alle verknüpften `oral_questions` erfüllen die obigen Bedingungen.

**Nicht exportieren:**

- `raw_questions` und Inhalte aus `question_imports`
- Fragen mit `rewrite_required`, `approved` (ohne erneute Publish-Freigabe), `archived`
- Jeder Eintrag mit `source_style` ≠ `accaoui_original`
- Fragen mit `ihk_similarity_risk = 'high'` ohne abgeschlossenes Review und Freigabe

Export erfolgt über ein **gesondertes Tool** (später unter `tools/`, nicht Teil dieses Dokuments), mit Preflight und `git diff --check` vor Übernahme in den Root.

---

## 16. Export-Ziele

| Ziel-Datei | Quelle (Supabase) | Inhalt |
|------------|-------------------|--------|
| `questions.json` | `written_questions` (gefiltert) | Array schriftlicher Fragen im App-Format |
| `data/oral-question-bank.js` | `oral_questions` (gefiltert) | Mündliche Trainingsfragen (JS-Export/Variable) |
| `data/oral-sheets-bank.js` | `oral_exam_sheets` + `oral_exam_sheet_questions` + verknüpfte `oral_questions` | Bogen A/B/C mit 15 Positionen und Prüferrollen |

Langfristig kann die App Fragen direkt per API laden; bis dahin bleiben diese Dateien die **kontrollierte Verteilungsschicht** nach jedem Export-Lauf.

---

## 17. Datenschutzregel

1. **Keine personenbezogenen Daten in Fragentexten** – keine Namen, Adressen, Geburtsdaten oder klar identifizierbare Fälle realer Personen in `question`, `answers`, `explanation`, `model_answer` usw.
2. **Rohimporte** können intern Quellhinweise enthalten; diese Felder sind nicht exportierbar und nicht für Teilnehmer sichtbar.
3. **Fortschritt getrennt speichern** – Lernstand, Prüfungsergebnisse, Fehlerhistorie und Lernkarten später in eigenen Tabellen mit `user_id`, `course_id`, ohne Duplizierung von Frageinhalten.
4. **Minimierung** – nur für Betrieb nötige Metadaten (`imported_by`, `reviewed_by`) als UUID-Referenz; keine unnötigen Logs in Fragentabellen.
5. **Kein Service Role Key im Frontend** – siehe Master Context §10 und §11.

---

## 18. Was in v23.5.7 noch nicht umgesetzt wird

Explizit **außerhalb** dieses Planungsschritts:

| Nicht umgesetzt | Anmerkung |
|-----------------|-----------|
| SQL / Migrationen | Erst nach Freigabe des Schemas |
| Supabase-Projekt / Verbindung | Keine Keys, keine Tabellen in der Cloud |
| App-Anbindung | `app.js`, `questions.json`, `data/*` unverändert |
| Import-Pipeline | Keine Rohfragen-Uploads |
| Export-Skript | Kein automatischer Schreibzugriff auf JSON/JS |
| Auth / `profiles` / Fortschrittstabellen | Folge-Tasks v27+ |

**Nächste sinnvolle Schritte (Roadmap, nur Referenz):**

- v23.5.8 – Export-Prozess und Preflight-Integration planen
- Rohfragen importieren (nur intern, `raw_questions`)
- v27 – Supabase Auth, RLS-Policies als SQL, Admin-UI

---

## Anhang A – Kanonische Sachgebiete (`topic`)

Alle Fragen (roh und veröffentlicht) verwenden exakt eine dieser neun Kategorien:

1. Recht der öffentlichen Sicherheit und Ordnung
2. Gewerberecht
3. Datenschutzrecht
4. Bürgerliches Gesetzbuch
5. Strafgesetzbuch und Strafverfahrensrecht
6. Unfallverhütungsvorschriften Wach- und Sicherungsdienste
7. Umgang mit Waffen
8. Umgang mit Menschen
9. Grundzüge der Sicherheitstechnik

Alte Bezeichnungen nur in App-Mapping (`normalizeCategoryName()`), nicht in neuen DB-Einträgen.

---

## Anhang B – Bezug zu bestehenden Docs

| Thema | Dokument |
|-------|----------|
| App-Kontext, IHK-Regel, Roadmap | `docs/CURSOR_MASTER_CONTEXT_ACCAOUI.md` |
| Prozess Import → Review → Publish | `docs/QUESTION_DATABASE_PLAN.md` |
| Schriftliches Fragenformat | `docs/WRITTEN_QUESTION_STANDARD.md` |

Dieses Schema ergänzt den Fragen-Datenbank-Plan um die konkrete Supabase-Tabellen- und RLS-Vorbereitung für v23.5.7.
