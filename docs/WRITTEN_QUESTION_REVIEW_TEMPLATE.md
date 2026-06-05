# Accaoui §34a Lern-App – Review-Vorlage für neue schriftliche Fragen

Stand: v23.5.14
Zweck: Einheitliche **Arbeits- und Prüfvorlage** für den Ausbau der schriftlichen Fragenbank von **51** auf **86** Fragen.
Bezug: `docs/WRITTEN_QUESTION_EXPANSION_PLAN.md`, `docs/WRITTEN_QUESTION_STANDARD.md`, `docs/QUESTION_DATABASE_PLAN.md`, `docs/CURSOR_MASTER_CONTEXT_ACCAOUI.md`

---

## 1. Zweck der Review-Datei

Diese Vorlage dient dazu, **neue Accaoui-Trainingsfragen** vor dem Einbau in `questions.json` fachlich und formal zu prüfen.

Ziele:

1. **Qualität** – einheitliches Format, klare Antwortlogik, verständliche Erklärungen
2. **Rechtssicherheit** – keine 1:1-Übernahme von IHK- oder Musterprüfungsfragen
3. **Nachvollziehbarkeit** – Review-ID, Prüfer, Status, Notizen pro Frage
4. **Planbarer Ausbau** – 35 neue Fragen in fünf Sachgebieten kontrolliert freigeben

**Verwendung:** Kopie dieser Datei oder Abschnitt in eine Block-Datei (z. B. `docs/review/WRITTEN_EXPANSION_BLOCK_BGB.md`) und pro Frage ausfüllen.

---

## 2. Grundregel

```txt
Neue Fragen werden zuerst geprüft und freigegeben,
bevor sie in questions.json kommen.
```

| Schritt | Ort | Aktion |
|---------|-----|--------|
| 1 | Review-Datei (diese Vorlage) | Entwurf + Checkliste |
| 2 | Review | Status `reviewed` / `approved` |
| 3 | Freigabe | Status `ready_for_import` |
| 4 | Separater Import-Task | Übertrag nach `questions.json` + Preflight + Browser-Test |

**Nicht erlaubt:** Massenimport ungeprüfter Fragen direkt in `questions.json`.

---

## 3. Rechtliche Schutzregel

| Regel | Bedeutung |
|-------|-----------|
| **Keine IHK-/Musterfragen 1:1** | Kein wörtlicher oder strukturell identischer Übernahme von offiziellen oder fremden Prüfungsaufgaben |
| **Rohfragen nur intern** | Analysierte Ausgangsfragen bleiben in Review-Notizen oder später Supabase `raw_questions` – nicht in der App |
| **Nur Accaoui-Trainingsfragen** | Veröffentlicht werden ausschließlich **eigen formulierte** Fragen mit `sourceStyle: accaoui_original` |
| **Kein IHK-Branding** | Keine Darstellung als offizielle IHK-Prüfung |

Musterprüfungen dürfen **Lernziele und Sachgebiete** orientieren, nicht den Wortlaut.

---

## 4. Review-Status

Jede Frage in der Review-Datei hat genau einen Status:

| Status | Bedeutung | Nächster Schritt |
|--------|-----------|------------------|
| `draft` | Entwurf, noch nicht zur Prüfung | Ausfüllen / vervollständigen |
| `needs_review` | Zur fachlichen Prüfung vorgelegt | Dozent/Reviewer prüfen |
| `rewrite_required` | Umformulierung nötig (z. B. hohes Ähnlichkeitsrisiko) | Autor überarbeiten |
| `reviewed` | Fachlich geprüft, noch nicht final freigegeben | Endfreigabe |
| `approved` | Inhaltlich freigegeben | Optional → `ready_for_import` |
| `rejected` | Nicht verwendbar | Archivieren / ersetzen |
| `ready_for_import` | Darf in separaten Task nach `questions.json` | Import + Audit + Browser-Test |

**Hinweis:** Status in Supabase (`published`, `archived`) gelten erst nach Datenbank-Einführung. Für den JSON-Ausbau v23.5.x reicht die Kette bis `ready_for_import`.

---

## 5. Pflichtfelder je Frage

Jede Frage im Review muss diese Felder enthalten (auch wenn einzelne Werte noch `-` sind):

| Feld | Beschreibung | Beispiel |
|------|--------------|----------|
| **Review-ID** | Eindeutige ID in der Review-Datei | `REV-BGB-01` |
| **Ziel-ID** | Geplante `id` in `questions.json` | `q_052` |
| **Kategorie** | Kanonisches Sachgebiet (1 von 9) | Bürgerliches Gesetzbuch |
| **Unterthema** | Feines Thema optional | Schadensersatz, Hausrecht, … |
| **Fragetyp** | `single`, `multiple`, `combination` | `single` |
| **Punktzahl** | `1` oder `2` | `1` |
| **Schwierigkeit** | `leicht`, `mittel`, `schwer` | `mittel` |
| **Prüfungsrelevanz** | `niedrig`, `mittel`, `hoch` | `hoch` |
| **IHK-Ähnlichkeitsrisiko** | `low`, `medium`, `high` | `low` |
| **sourceStyle** | Immer für Import | `accaoui_original` |
| **Frage** | Vollständiger Fragetext | … |
| **Antwortoptionen** | a–d oder a–e mit Text | a) … b) … |
| **Richtige Antwort(en)** | Buchstabe(n) | `b` oder `b`, `d` |
| **Erklärung** | Lern-Erklärung | … |
| **Fachliche Prüfung** | Wer, wann, Ergebnis | z. B. „OK, 2026-06-02, Name“ |
| **Dublettenprüfung** | Vergleich mit 51+ bestehenden | „keine Dublette“ / Verweis |
| **Freigabestatus** | Siehe §4 | `draft` |
| **Notizen** | Interne Hinweise, Quelle (nur Analyse) | … |

Langfristig zusätzlich (optional in Review): `ihkSimilarityRisk` als Alias zu IHK-Ähnlichkeitsrisiko – Import mappt auf App-Feld.

---

## 6. Qualitätscheckliste

Vor Status `reviewed` oder höher **alle** Punkte prüfen:

| # | Prüfpunkt | OK | Anmerkung |
|---|-----------|:--:|-----------|
| 1 | **Kategorie korrekt?** | ☐ | Exakt eines der 9 kanonischen Sachgebiete |
| 2 | **Frage eindeutig?** | ☐ | Keine Mehrdeutigkeit im Fragetext |
| 3 | **Antwortlogik korrekt?** | ☐ | Genau die markierte(n) Antwort(en) richtig |
| 4 | **Maximal 1–2 richtige Antworten?** | ☐ | Passt zu Punktzahl |
| 5 | **Punktzahl passend?** | ☐ | 1 Punkt → meist 1 richtig; 2 Punkte → meist 2 richtig |
| 6 | **Erklärung verständlich?** | ☐ | Fachlich korrekt, für Lernmodus geeignet |
| 7 | **Keine 1:1-Kopie?** | ☐ | Formulierung und Optionen eigenständig |
| 8 | **Keine veralteten Begriffe?** | ☐ | Aktuelle Rechts-/Fachsprache |
| 9 | **Keine Dublette?** | ☐ | Abgleich mit `questions.json` + andere Review-Einträge |

**Freigabe nur wenn alle Punkte erfüllt** (oder begründete Ausnahme in Notizen).

---

## 7. Leere Vorlage für eine einzelne Frage

Kopieren und pro Frage ausfüllen:

---

### Frage: `[Review-ID]` → Ziel `[q_XXX]`

| Meta | Wert |
|------|------|
| Review-ID | |
| Ziel-ID (`questions.json`) | |
| Kategorie | |
| Unterthema | |
| Fragetyp | `single` / `multiple` / `combination` |
| Punktzahl | 1 / 2 |
| Schwierigkeit | leicht / mittel / schwer |
| Prüfungsrelevanz | niedrig / mittel / hoch |
| IHK-Ähnlichkeitsrisiko | low / medium / high |
| sourceStyle | accaoui_original |
| Freigabestatus | draft |

**Frage:**

>

**Antwortoptionen:**

- a)
- b)
- c)
- d)
- e) *(nur bei Kombinationsfrage)*

**Richtige Antwort(en):**

>

**Erklärung:**

>

**Qualitätscheckliste (§6):** ☐ alle 9 Punkte

| Prüfung | Ergebnis |
|---------|----------|
| Fachliche Prüfung | |
| Dublettenprüfung | |
| Notizen | |

---

## 8. Geplante 35 Fragen – Platzhalter

Ausbau laut `docs/WRITTEN_QUESTION_EXPANSION_PLAN.md`.
Status initial: `draft`. Ziel-IDs fortlaufend ab `q_052` (anpassen, falls beim Import andere IDs nötig).

### Block A – Bürgerliches Gesetzbuch (+8)

| Nr | Review-ID | Ziel-ID | Freigabestatus |
|----|-----------|---------|----------------|
| 01 | REV-BGB-01 | q_052 | draft |
| 02 | REV-BGB-02 | q_053 | draft |
| 03 | REV-BGB-03 | q_054 | draft |
| 04 | REV-BGB-04 | q_055 | draft |
| 05 | REV-BGB-05 | q_056 | draft |
| 06 | REV-BGB-06 | q_057 | draft |
| 07 | REV-BGB-07 | q_058 | draft |
| 08 | REV-BGB-08 | q_059 | draft |

<details>
<summary>Frage REV-BGB-01 (Vorlage einfügen)</summary>

*(Abschnitt aus §7 hier einfügen)*

</details>

---

### Block B – Strafgesetzbuch und Strafverfahrensrecht (+8)

| Nr | Review-ID | Ziel-ID | Freigabestatus |
|----|-----------|---------|----------------|
| 01 | REV-STGB-01 | q_060 | draft |
| 02 | REV-STGB-02 | q_061 | draft |
| 03 | REV-STGB-03 | q_062 | draft |
| 04 | REV-STGB-04 | q_063 | draft |
| 05 | REV-STGB-05 | q_064 | draft |
| 06 | REV-STGB-06 | q_065 | draft |
| 07 | REV-STGB-07 | q_066 | draft |
| 08 | REV-STGB-08 | q_067 | draft |

<details>
<summary>Frage REV-STGB-01 (Vorlage einfügen)</summary>

*(Abschnitt aus §7 hier einfügen)*

</details>

---

### Block C – Unfallverhütungsvorschriften Wach- und Sicherungsdienste (+3)

| Nr | Review-ID | Ziel-ID | Freigabestatus |
|----|-----------|---------|----------------|
| 01 | REV-UVV-01 | q_068 | draft |
| 02 | REV-UVV-02 | q_069 | draft |
| 03 | REV-UVV-03 | q_070 | draft |

<details>
<summary>Frage REV-UVV-01 (Vorlage einfügen)</summary>

*(Abschnitt aus §7 hier einfügen)*

</details>

---

### Block D – Umgang mit Menschen (+14)

| Nr | Review-ID | Ziel-ID | Freigabestatus |
|----|-----------|---------|----------------|
| 01 | REV-MENSCH-01 | q_071 | draft |
| 02 | REV-MENSCH-02 | q_072 | draft |
| 03 | REV-MENSCH-03 | q_073 | draft |
| 04 | REV-MENSCH-04 | q_074 | draft |
| 05 | REV-MENSCH-05 | q_075 | draft |
| 06 | REV-MENSCH-06 | q_076 | draft |
| 07 | REV-MENSCH-07 | q_077 | draft |
| 08 | REV-MENSCH-08 | q_078 | draft |
| 09 | REV-MENSCH-09 | q_079 | draft |
| 10 | REV-MENSCH-10 | q_080 | draft |
| 11 | REV-MENSCH-11 | q_081 | draft |
| 12 | REV-MENSCH-12 | q_082 | draft |
| 13 | REV-MENSCH-13 | q_083 | draft |
| 14 | REV-MENSCH-14 | q_084 | draft |

<details>
<summary>Frage REV-MENSCH-01 (Vorlage einfügen)</summary>

*(Abschnitt aus §7 hier einfügen)*

</details>

---

### Block E – Grundzüge der Sicherheitstechnik (+2)

| Nr | Review-ID | Ziel-ID | Freigabestatus |
|----|-----------|---------|----------------|
| 01 | REV-TECH-01 | q_085 | draft |
| 02 | REV-TECH-02 | q_086 | draft |

<details>
<summary>Frage REV-TECH-01 (Vorlage einfügen)</summary>

*(Abschnitt aus §7 hier einfügen)*

</details>

---

### Übersicht Ausbau

| Block | Sachgebiet | Anzahl | Review-IDs |
|-------|------------|-------:|------------|
| A | Bürgerliches Gesetzbuch | 8 | REV-BGB-01 … 08 |
| B | Strafgesetzbuch und Strafverfahrensrecht | 8 | REV-STGB-01 … 08 |
| C | Unfallverhütungsvorschriften … | 3 | REV-UVV-01 … 03 |
| D | Umgang mit Menschen | 14 | REV-MENSCH-01 … 14 |
| E | Grundzüge der Sicherheitstechnik | 2 | REV-TECH-01 … 02 |
| | **Gesamt neu** | **35** | |
| | **Bank nach Import** | **86** | 51 + 35 |

---

## 9. Import-Regel

Eine Frage darf **erst** in `questions.json` übertragen werden, wenn:

1. **Freigabestatus** = `ready_for_import`
2. **sourceStyle** = `accaoui_original`
3. **Qualitätscheckliste** §6 vollständig erfüllt
4. **Ziel-ID** eindeutig und noch nicht in `questions.json` vergeben
5. **Kategorie** kanonisch (Audit-kompatibel)

**Nach Import (separater Task):**

```bash
python tools/audit-categories.py
python tools/preflight.py
```

Dann Browser-Test: Alle Fragen, Prüfung, Lernkarten, Fehlertraining.

**Preflight:** Bei Änderung an `questions.json` nur mit freigegebenem Task; ggf. `ACCAOUI_ALLOW_PROTECTED=questions.json`.

---

## 10. Hinweis

> **Diese Datei ist nur eine Review- und Arbeitsvorlage – nicht die endgültige Fragenbank.**

- Die **produktive** Quelle für die App bleibt `questions.json` (bis Supabase-Export live ist).
- Inhaltliche Wahrheit nach Import: `questions.json` + Audit.
- Review-Dateien können Duplikate, Entwürfe und `rejected` Einträge enthalten – das ist gewollt.
- Keine IHK-/Muster- oder Rohfragen als „fertige“ Aufgaben in dieser Vorlage ablegen.

---

## Anhang – Kanonische Kategorien (Auswahl)

Nur diese Namen in **Kategorie** verwenden:

1. Recht der öffentlichen Sicherheit und Ordnung
2. Gewerberecht
3. Datenschutzrecht
4. Bürgerliches Gesetzbuch
5. Strafgesetzbuch und Strafverfahrensrecht
6. Unfallverhütungsvorschriften Wach- und Sicherungsdienste
7. Umgang mit Waffen
8. Umgang mit Menschen
9. Grundzüge der Sicherheitstechnik

---

## Anhang – JSON-Zielformat (Referenz)

Nach Import entspricht jede Frage `docs/WRITTEN_QUESTION_STANDARD.md` §7, z. B.:

```js
{
  id: "q_052",
  category: "Bürgerliches Gesetzbuch",
  question: "…",
  points: 1,
  answers: [
    { id: "a", text: "…" },
    { id: "b", text: "…" },
    { id: "c", text: "…" },
    { id: "d", text: "…" }
  ],
  correctAnswers: ["b"],
  explanation: "…",
  difficulty: "mittel",
  examRelevance: "hoch"
}
```

Review-Felder `Unterthema`, `IHK-Ähnlichkeitsrisiko`, `sourceStyle` können im JSON ergänzt werden, sobald die App sie unterstützt – bis dahin mindestens Standard-Pflichtfelder.
