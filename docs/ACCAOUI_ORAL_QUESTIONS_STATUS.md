# Accaoui §34a Lern-App – Mündliche Fragen-Status

Stand: v24.5y
Projekt: Accaoui §34a Lern-App

---

## 1. Zweck

Diese Datei dokumentiert den **Status der mündlichen Prüfung** und der **mündlichen Musterfragen** in der Accaoui §34a Lern-App.

Ziel: Klar trennen, was in der App bereits funktioniert und was bei der Auswertung von Quellenpaketen noch offen ist.

---

## 2. Aktueller App-Stand

| Bereich | Status |
|---------|--------|
| Mündliche Prüfung (Modul) | **vorhanden** |
| Training nach Themen | **vorhanden** |
| Simulation A | **vorhanden** |
| Simulation B | **vorhanden** |
| Musterantworten | **vorhanden** |
| Bewertungslogik (Sicher / Noch üben) | **vorhanden** |
| Fehlertraining mündlich | **vorhanden** |

Technische Hauptdateien (Referenz, nicht in diesem Task ändern):

- `oral-exam.js`
- `oral-sheets.js`, `oral-sheets-v23.js`
- `data/oral-question-bank.js`, `data/oral-sheets-bank.js`
- `patch-v21.js` (Patch-Schichten)

---

## 3. Offen

| Aufgabe | Status |
|---------|--------|
| Zusätzliche mündliche Musterfragen aus Quellenpaketen prüfen | **offen** |
| Eigene Accaoui-Fragen daraus erstellen | **offen** |
| Musterantworten fachlich prüfen | **offen** |
| Prüfermodus später erweitern | **geplant** |
| Bogen-Auswahl skalierbar machen (A, B, C, D …) | **geplant** |

Quellenbasis: siehe `docs/ACCAOUI_SOURCE_MATERIAL_STATUS.md`.

---

## 4. Rechtliche Regel

1. **Keine fremden Fragen 1:1 übernehmen.**
2. Nur **eigene Accaoui-Formulierungen** veröffentlichen.
3. Quellen dienen Analyse und Struktur – nicht Copy-Paste.
4. App klar als **Trainingsplattform**, nicht als offizielle IHK-Prüfung kennzeichnen.

---

## 5. Nächster empfohlener Schritt

**Nach v24.6b** (Wiederholungslogik schriftliche Prüfung):

1. Mündliche Quellen aus den Quellenpaketen **gezielt** analysieren (nicht alles auf einmal).
2. Geprüfte Inhalte in eine **Accaoui-Mündlich-Fragenliste** überführen (Review vor Veröffentlichung).
3. Musterantworten und Prüfer-Hinweise fachlich freigeben.
4. Erst danach App-Datenbanken kontrolliert erweitern.

---

## 6. Verknüpfung

| Dokument | Inhalt |
|----------|--------|
| `docs/ACCAOUI_SOURCE_MATERIAL_STATUS.md` | Quellenpakete und PDF-ZIPs |
| `docs/PROJECT_MASTERLIST.md` | §12 Mündlicher Fehlertrainer, Roadmap Oral Exam Cleanup |
| `docs/CURSOR_MASTER_CONTEXT_ACCAOUI.md` | §7 Mündliche Prüfung, Roadmap v24 |
