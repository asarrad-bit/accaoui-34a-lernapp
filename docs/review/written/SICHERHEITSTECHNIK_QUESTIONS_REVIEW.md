# Accaoui §34a – Review: Grundzüge der Sicherheitstechnik (+2 Fragen)

Stand: v23.5.40 (Dublettenprüfung dokumentiert)
Block: E (Ausbauplan `docs/WRITTEN_QUESTION_EXPANSION_PLAN.md`)
Vorlage: `docs/WRITTEN_QUESTION_REVIEW_TEMPLATE.md`
**Status aller Fragen:** `ready_for_import`
**Hinweis:** Nur Review-Arbeitsdatei – noch **nicht** in `questions.json`. Block ist importbereit; Import erfolgt erst im separaten Import-Task.

---

## Block-Übersicht

| Nr | Review-ID | Ziel-ID | Unterthema | Punkte | Status |
|----|-----------|---------|------------|-------:|--------|
| 01 | REV-TECH-01 | technik_006 | Einbruchmeldeanlage / Alarmmeldung / Verhalten bei Alarm | 1 | ready_for_import |
| 02 | REV-TECH-02 | technik_007 | Videoüberwachung / Zutrittskontrolle / technische Sicherung | 2 | ready_for_import |

**Summe Punkte (wenn alle richtig):** 3

---

## Frage REV-TECH-01 → Ziel technik_006

| Meta | Wert |
|------|------|
| Review-ID | REV-TECH-01 |
| Ziel-ID (`questions.json`) | technik_006 |
| Kategorie | Grundzüge der Sicherheitstechnik |
| Unterthema | Einbruchmeldeanlage / Alarmmeldung / Verhalten bei Alarm |
| Fragetyp | single |
| Punktzahl | 1 |
| Schwierigkeit | mittel |
| Prüfungsrelevanz | hoch |
| IHK-Ähnlichkeitsrisiko | low |
| sourceStyle | accaoui_original |
| Freigabestatus | ready_for_import |

**Frage:**

> Gegen 2:00 Uhr meldet die **Einbruchmeldeanlage** (EMA) einen Alarm in einem **abgesperrten Lagerbereich**. Der Sicherheitsmitarbeiter sieht auf dem Monitor zunächst **niemanden**. Welche **Verhaltensweise** ist im Grundsatz richtig?

**Antwortoptionen:**

- a) Den Alarm ignorieren, weil niemand sichtbar ist – vermutlich Fehlalarm
- b) Den Alarm **ernst nehmen**, nach **Dienstanweisung** den Bereich **prüfen/absichern**, die **Meldung an Leitstelle/Auftraggeber** weitergeben und die Anlage **nicht eigenmächtig dauerhaft zurückstellen**
- c) Die EMA **dauerhaft abschalten**, um weitere Störungen zu vermeiden
- d) **Eigenmächtig** in jeden Bereich eindringen, auch ohne Schlüssel oder Freigabe

**Richtige Antwort(en):** b

**Erklärung:**

> **Einbruchmeldeanlagen** dienen der **Erkennung und Meldung** von Einbruchversuchen. Ein **EMA-Alarm** ist **auch ohne sichtbare Person** ernst zu nehmen. Der Sicherheitsmitarbeiter handelt nach **Dienstanweisung**: Bereich **prüfen/absichern**, **Meldung an Leitstelle/Auftraggeber** weitergeben. **Rückstellung** oder **Abschaltung** nur im **befugten Rahmen** – **kein eigenmächtiges dauerhaftes Abschalten**.

| Prüfung | Ergebnis |
|---------|----------|
| Fachliche Prüfung | OK – Review v23.5.38 |
| Dublettenprüfung | OK – v23.5.40, keine direkte Dublette (siehe Abschnitt unten) |
| Notizen | Accaoui-Fall Nachtdienst Lager; Abgrenzung technik_003 (BMA) |

---

## Frage REV-TECH-02 → Ziel technik_007

| Meta | Wert |
|------|------|
| Review-ID | REV-TECH-02 |
| Ziel-ID (`questions.json`) | technik_007 |
| Kategorie | Grundzüge der Sicherheitstechnik |
| Unterthema | Videoüberwachung / Zutrittskontrolle / technische Sicherung |
| Fragetyp | multiple |
| Punktzahl | 2 |
| Schwierigkeit | mittel |
| Prüfungsrelevanz | hoch |
| IHK-Ähnlichkeitsrisiko | medium |
| sourceStyle | accaoui_original |
| Freigabestatus | ready_for_import |

**Frage:**

> Ein Einkaufszentrum nutzt **Videoüberwachung** und ein **elektronisches Zutrittskontrollsystem** für Nebenräume. Welche **zwei** Aussagen zu **technischer Sicherung** im Sicherheitsdienst sind im Grundsatz zutreffend?

**Antwortoptionen:**

- a) Videoüberwachung darf ohne Kennzeichnung und ohne rechtliche Grundlage beliebig in Umkleiden aufgenommen werden
- b) **Zutrittskontrollsysteme** können den Zutritt **nur berechtigten Personen** ermöglichen und **Zutrittsversuche** dokumentieren
- c) Sicherheitsmitarbeiter dürfen **Videoaufzeichnungen** beliebig privat weitergeben oder in sozialen Medien veröffentlichen
- d) Technische Sicherung **ersetzt** vollständig **Datenschutz**, **Hausrecht** und **menschliche Kontrolle**
- e) **Videoüberwachung** unterliegt u. a. **Kennzeichnungs-** und **Zweckbindungspflichten**; der Einsatz muss **rechtlich zulässig** sein (z. B. DS-GVO, Betriebsvereinbarung, Auftraggebervorgaben)

**Richtige Antwort(en):** b, e

**Erklärung:**

> **Zutrittskontrollsysteme** steuern **berechtigten Zutritt** und können **Zutrittsversuche dokumentieren**. **Videoüberwachung** braucht eine **rechtliche Grundlage**, **Zweckbindung**, **Kennzeichnung** und **Zugriffsbeschränkung**. Technische Sicherung **ergänzt** Hausrecht, Datenschutz und menschliche Kontrolle, **ersetzt** sie aber **nicht**. **Keine private Weitergabe** oder **Veröffentlichung** von Aufnahmen.

| Prüfung | Ergebnis |
|---------|----------|
| Fachliche Prüfung | OK – Review v23.5.38, Antwortlogik b + e |
| Dublettenprüfung | OK – v23.5.40, keine direkte Dublette (siehe Abschnitt unten) |
| Notizen | 2-Punkte-Frage; Verknüpfung Datenschutzrecht (Sachgebiet 3) nur als Kontext |

---

## Dublettenprüfung gegen questions.json (v23.5.40)

Geprüft wurden die 2 Review-Fragen (Ziel-IDs `technik_006`–`technik_007`) gegen die **5 bestehenden** Sicherheitstechnik-Fragen in `questions.json`.

### Bestehende Sicherheitstechnik-Fragen in questions.json

| ID | Kurzinhalt |
|----|------------|
| technik_001 | Einbruchmeldeanlagen allgemein |
| technik_002 | Funktionsprüfung / Bedienung / Störungen |
| technik_003 | Brandmeldeanlage Alarm |
| technik_004 | Zutrittskontrolle allgemein |
| technik_005 | Aufgabe einer Einbruchmeldeanlage |

### Prüfergebnis

| Review-ID | Ergebnis |
|-----------|----------|
| REV-TECH-01 | Keine direkte Dublette; **thematische Nähe** zu technik_001/technik_005 (EMA), aber **Vertiefung** – **technik_006** vertieft konkretes **Verhalten bei EMA-Alarm** |
| REV-TECH-02 | Keine direkte Dublette; **thematische Nähe** zu technik_004 (Zutrittskontrolle), aber **Vertiefung** – **technik_007** ergänzt **Videoüberwachung**, Zutrittskontrolle und **Datenschutz** |

**Gesamt:** Keine direkte Dublette. Thematische Nähe bei Einbruchmeldeanlage und Zutrittskontrolle; die neuen Fragen sind **Vertiefungen**, keine Wiederholungen. Der Block darf auf **`ready_for_import`** gesetzt werden.

**Prüfdatum / Task:** v23.5.40

---

## Block-Abschluss

| Kennzahl | Wert |
|----------|------|
| Fragen in dieser Datei | 2 |
| Ziel-IDs | technik_006 … technik_007 |
| Status | alle `ready_for_import` |

## Review-Zusammenfassung (v23.5.40)

| Status | Anzahl | Review-IDs |
|--------|-------:|------------|
| **reviewed** | 0 | — |
| **approved** | 0 | — |
| **ready_for_import** | 2 | REV-TECH-01 … REV-TECH-02 |
| **rewrite_required** | 0 | — |

### Fachliche Prüfung (v23.5.38) – abgeschlossen

- **REV-TECH-01:** EMA-Alarm ernst nehmen, Dienstanweisung, Meldung, keine eigenmächtige Dauer-Rückstellung
- **REV-TECH-02:** Zutrittskontrolle + Videoüberwachung mit Datenschutz – Antworten **b + e**
- **Ziel-IDs:** `technik_006`/`technik_007` (einheitlicher Präfix zu technik_001–technik_005)

### Freigabe (v23.5.39) – abgeschlossen

- Beide Fragen fachlich **approved**

### Dublettenprüfung (v23.5.40) – abgeschlossen

- Abgleich mit 5 bestehenden Sicherheitstechnik-Fragen in `questions.json` (technik_001–technik_005) durchgeführt
- Keine direkte Dublette; technik_006 vertieft EMA-Alarmverhalten, technik_007 ergänzt Video/Datenschutz
- Beide Fragen: **`ready_for_import`**

### Kennzahlen

| Kennzahl | Wert |
|----------|------|
| Fragen in dieser Datei | 2 |
| Summe Punkte (wenn alle richtig) | 3 |
| Nächster Schritt | **Separater Import-Task** → `questions.json` (`technik_006`–`technik_007`) |

### Import-Regel

**Hinweis:** Der Block ist **`ready_for_import`**, aber **noch nicht importiert**. Der Import in `questions.json` erfolgt **erst in einem eigenen Import-Task** (mit Preflight, `audit-categories.py`, Browser-Test).

**Nicht in dieser Aufgabe:** Keine Einträge in `questions.json` – Import bleibt bis zum Import-Task ausstehend.

**Hinweis zu bestehenden Fragen:** technik_001–technik_005 bleiben unverändert; technik_006–technik_007 **ergänzen** und **vertiefen**.

---

*Accaoui-eigene Trainingsfragen – keine 1:1-Übernahme aus IHK- oder Musterprüfungen.*
