# Accaoui §34a – Review: Grundzüge der Sicherheitstechnik (+2 Fragen)

Stand: v23.5.37
Block: E (Ausbauplan `docs/WRITTEN_QUESTION_EXPANSION_PLAN.md`)
Vorlage: `docs/WRITTEN_QUESTION_REVIEW_TEMPLATE.md`
**Status aller Fragen:** `needs_review`
**Hinweis:** Nur Review-Arbeitsdatei – noch **nicht** in `questions.json`.

---

## Block-Übersicht

| Nr | Review-ID | Ziel-ID | Unterthema | Punkte | IHK-Risiko |
|----|-----------|---------|------------|-------:|------------|
| 01 | REV-TECH-01 | sicherheit_006 | Einbruchmeldeanlage / Alarmmeldung / Verhalten bei Alarm | 1 | low |
| 02 | REV-TECH-02 | sicherheit_007 | Videoüberwachung / Zutrittskontrolle / technische Sicherung | 2 | medium |

**Summe Punkte (wenn alle richtig):** 3

---

## Frage REV-TECH-01 → Ziel sicherheit_006

| Meta | Wert |
|------|------|
| Review-ID | REV-TECH-01 |
| Ziel-ID (`questions.json`) | sicherheit_006 |
| Kategorie | Grundzüge der Sicherheitstechnik |
| Unterthema | Einbruchmeldeanlage / Alarmmeldung / Verhalten bei Alarm |
| Fragetyp | single |
| Punktzahl | 1 |
| Schwierigkeit | mittel |
| Prüfungsrelevanz | hoch |
| IHK-Ähnlichkeitsrisiko | low |
| sourceStyle | accaoui_original |
| Freigabestatus | needs_review |

**Frage:**

> Gegen 2:00 Uhr meldet die **Einbruchmeldeanlage** (EMA) einen Alarm in einem **abgesperrten Lagerbereich**. Der Sicherheitsmitarbeiter sieht auf dem Monitor zunächst **niemanden**. Welche **Verhaltensweise** ist im Grundsatz richtig?

**Antwortoptionen:**

- a) Den Alarm ignorieren, weil niemand sichtbar ist – vermutlich Fehlalarm
- b) Den Alarm **ernst nehmen**, nach **Dienstanweisung** den Bereich **prüfen/absichern**, die **Meldung an Leitstelle/Auftraggeber** weitergeben und die Anlage **nicht eigenmächtig dauerhaft zurückstellen**
- c) Die EMA **dauerhaft abschalten**, um weitere Störungen zu vermeiden
- d) **Eigenmächtig** in jeden Bereich eindringen, auch ohne Schlüssel oder Freigabe

**Richtige Antwort(en):** b

**Erklärung:**

> **Einbruchmeldeanlagen** dienen der **Erkennung und Meldung** von Einbruchversuchen. Ein Alarm ist **auch ohne sichtbare Person** ernst zu nehmen (Fehlalarm erst nach **geordneter Prüfung**). Der Sicherheitsmitarbeiter handelt nach **Dienstanweisung**: Ort prüfen/absichern, **Meldung weitergeben**, ggf. Polizei/Technik einbinden. **Rückstellung** oder Abschaltung nur im **befugten Rahmen**, nicht eigenmächtig.

| Prüfung | Ergebnis |
|---------|----------|
| Fachliche Prüfung | Ausstehend – Review v23.5.37 |
| Dublettenprüfung | Thematische Nähe zu technik_001/technik_005 (EMA allgemein); vertieft **Verhalten bei Alarm** – Abgleich `questions.json` vor Import |
| Notizen | Accaoui-Fall Nachtdienst Lager; Abgrenzung technik_003 (BMA) |

---

## Frage REV-TECH-02 → Ziel sicherheit_007

| Meta | Wert |
|------|------|
| Review-ID | REV-TECH-02 |
| Ziel-ID (`questions.json`) | sicherheit_007 |
| Kategorie | Grundzüge der Sicherheitstechnik |
| Unterthema | Videoüberwachung / Zutrittskontrolle / technische Sicherung |
| Fragetyp | multiple |
| Punktzahl | 2 |
| Schwierigkeit | mittel |
| Prüfungsrelevanz | hoch |
| IHK-Ähnlichkeitsrisiko | medium |
| sourceStyle | accaoui_original |
| Freigabestatus | needs_review |

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

> **Zutrittskontrolle:** Technische Systeme (Karten, Codes, Schleusen) steuern **berechtigten Zutritt** und können **Versuche** protokollieren – ergänzend zu **menschlicher Kontrolle**, nicht als Ersatz für alle Pflichten. **Videoüberwachung:** Nur bei **rechtlicher Grundlage** und unter Beachtung von **Datenschutz** (u. a. Kennzeichnung, Zweckbindung, Zugriffsbeschränkung). Keine Weitergabe oder Veröffentlichung von Aufnahmen ohne Befugnis.

| Prüfung | Ergebnis |
|---------|----------|
| Fachliche Prüfung | Ausstehend – Review v23.5.37 |
| Dublettenprüfung | Thematische Nähe zu technik_004 (Zutrittskontrolle allgemein); vertieft **Video + Datenschutz** – Abgleich `questions.json` vor Import |
| Notizen | 2-Punkte-Frage; Verknüpfung Datenschutzrecht (Sachgebiet 3) nur als Kontext |

---

## Block-Abschluss

| Kennzahl | Wert |
|----------|------|
| Fragen in dieser Datei | 2 |
| Ziel-IDs | sicherheit_006 … sicherheit_007 |
| Status | alle `needs_review` |
| Nächster Schritt | Fachliche Prüfung → `approved` → Dublettenprüfung → `ready_for_import` → Import-Task |

**Hinweis zu bestehenden Fragen:** In `questions.json` existieren bereits technik_001–technik_005 (EMA, Funktionsprüfung, BMA, Zutrittskontrolle, EMA-Aufgabe). Die neuen Fragen **vertiefen** und **ergänzen**, ersetzen sie nicht. Ziel-IDs `sicherheit_006`/`sicherheit_007` sind bewusst vom Präfix `technik_` abweichend (Import-Task prüft Eindeutigkeit).

---

*Accaoui-eigene Trainingsfragen – keine 1:1-Übernahme aus IHK- oder Musterprüfungen.*
