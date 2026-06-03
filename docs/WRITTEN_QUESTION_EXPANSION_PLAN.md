# Accaoui §34a Lern-App – Ausbauplan schriftliche Fragenbank

Stand: v23.5.13  
Zweck: Plan für den kontrollierten Ausbau der schriftlichen Fragenbank von **51** auf **86** Fragen – ohne bestehende Inhalte zu löschen.  
Bezug: `docs/WRITTEN_QUESTION_STANDARD.md`, `docs/CURSOR_MASTER_CONTEXT_ACCAOUI.md`, `docs/QUESTION_DATABASE_PLAN.md`

---

## 1. Zweck des Ausbauplans

Die Accaoui §34a Lern-App soll die **Sachkundeprüfung schriftlich** realistisch abbilden. Dafür braucht die App:

1. eine **ausreichend große Fragenbank** pro Sachgebiet (Üben, Alle Fragen, Lernkarten, Fehlertraining),
2. später einen **Prüfungsmodus mit exakt 82 Fragen** nach offizieller Gewichtung,
3. **eigene Accaoui-Fragen** – rechtlich geprüft, nicht 1:1 aus IHK-Mustern.

Dieser Plan beschreibt **nur** die inhaltliche und organisatorische Erweiterung. Er enthält **keine** neuen Fragen in `questions.json` und **keine** Code-Änderungen.

---

## 2. Aktueller Stand: 51 Fragen

Die Datei `questions.json` enthält aktuell **51** schriftliche Fragen in **9 kanonischen Sachgebieten**.

Verteilung (Stand v23.5.13, aus Kategorie-Audit / `questions.json`):

| # | Sachgebiet | Aktuell |
|---|------------|--------:|
| 1 | Recht der öffentlichen Sicherheit und Ordnung | 8 |
| 2 | Gewerberecht | 8 |
| 3 | Datenschutzrecht | 5 |
| 4 | Bürgerliches Gesetzbuch | 5 |
| 5 | Strafgesetzbuch und Strafverfahrensrecht | 5 |
| 6 | Unfallverhütungsvorschriften Wach- und Sicherungsdienste | 5 |
| 7 | Umgang mit Waffen | 5 |
| 8 | Umgang mit Menschen | 5 |
| 9 | Grundzüge der Sicherheitstechnik | 5 |
| | **Gesamt** | **51** |

Mehrere Sachgebiete sind **unter** der späteren Prüfungszielverteilung (82 Fragen). Einige sind **leicht über** dem Ziel – das ist beabsichtigt und bleibt erhalten.

---

## 3. Zielgewichtung der 82-Fragen-Prüfung

Die reale Sachkundeprüfung schriftlich umfasst **82 geschlossene Aufgaben** in **120 Minuten** (mindestens 50 % zum Bestehen). Accaoui orientiert sich an dieser Struktur:

| Sachgebiet | Fragen in Prüfung | Punkte |
|------------|------------------:|-------:|
| Recht der öffentlichen Sicherheit und Ordnung | 7 | 11 |
| Gewerberecht | 5 | 8 |
| Datenschutzrecht | 5 | 8 |
| Bürgerliches Gesetzbuch | 13 | 21 |
| Strafgesetzbuch und Strafverfahrensrecht | 13 | 21 |
| Unfallverhütungsvorschriften Wach- und Sicherungsdienste | 8 | 13 |
| Umgang mit Waffen | 5 | 8 |
| Umgang mit Menschen | 19 | 19 |
| Grundzüge der Sicherheitstechnik | 7 | 11 |
| **Gesamt Prüfung** | **82** | **120** |

**Wichtig:** Die **Fragenbank** darf größer als 82 sein. Der **Prüfungsmodus** wählt später **exakt 82 Fragen** nach dieser Gewichtung aus dem Pool (Zufall/Rotation innerhalb des Sachgebiets).

---

## 4. Warum keine Fragen gelöscht werden

| Grund | Erläuterung |
|-------|-------------|
| Stabilität | Bestehende Fragen sind in App, Statistik und ggf. `localStorage` verankert |
| Kein Datenverlust | Teilnehmer-Fortschritt und Fehlerhistorie beziehen sich auf Frage-IDs |
| Überhang ist erlaubt | Sachgebiete mit mehr Fragen als Prüfungsziel (z. B. 8 statt 7) erhöhen Übungsvielfalt |
| Prüfungsmodus später | Auswahl 82 aus Pool – Überbestand wird nicht mitgelöscht, sondern genutzt |

**Regel:** Nur **auffüllen**, nicht **kürzen**, bis ein separater Migrations- und Review-Prozess ausdrücklich eine Archivierung einzelner Dubletten vorsieht.

---

## 5. Ausbau auf 86 Fragen

### Strategie

Unterversorgte Sachgebiete werden um die fehlende Differenz zum **Prüfungsziel** (Spalte „Ziel 82“) ergänzt. Überbestand in anderen Sachgebieten bleibt.

### Neue Fragen (gesamt +35)

| Sachgebiet | Neue Fragen |
|------------|------------:|
| Bürgerliches Gesetzbuch | +8 |
| Strafgesetzbuch und Strafverfahrensrecht | +8 |
| Unfallverhütungsvorschriften Wach- und Sicherungsdienste | +3 |
| Umgang mit Menschen | +14 |
| Grundzüge der Sicherheitstechnik | +2 |
| **Summe neu** | **+35** |

### Ergebnis

```txt
51 (aktuell) + 35 (neu) = 86 Fragen in der Fragenbank
```

Die Bank hat damit **4 Fragen mehr** als die 82er-Prüfung – bewusst als Puffer für Rotation und Qualitätsreserve.

---

## 6. Tabelle: Verteilung, Ziel, Differenz, Maßnahme

| Sachgebiet | Aktuell | Ziel (82-Prüfung) | Differenz (Ziel − Aktuell) | Maßnahme |
|------------|--------:|------------------:|---------------------------:|----------|
| Recht der öffentlichen Sicherheit und Ordnung | 8 | 7 | +1 (Überbestand) | **Keine Löschung** – Pool für Prüfungsziehung |
| Gewerberecht | 8 | 5 | +3 (Überbestand) | **Keine Löschung** |
| Datenschutzrecht | 5 | 5 | 0 | **Keine Änderung** nötig |
| Bürgerliches Gesetzbuch | 5 | 13 | **−8** (fehlen 8) | **+8 neue Fragen** |
| Strafgesetzbuch und Strafverfahrensrecht | 5 | 13 | **−8** (fehlen 8) | **+8 neue Fragen** |
| Unfallverhütungsvorschriften Wach- und Sicherungsdienste | 5 | 8 | **−3** (fehlen 3) | **+3 neue Fragen** |
| Umgang mit Waffen | 5 | 5 | 0 | **Keine Änderung** nötig |
| Umgang mit Menschen | 5 | 19 | **−14** (fehlen 14) | **+14 neue Fragen** |
| Grundzüge der Sicherheitstechnik | 5 | 7 | **−2** (fehlen 2) | **+2 neue Fragen** |
| **Gesamt** | **51** | **82** (nur Prüfung) | **−31** zum Prüfungsziel | **+35** in Bank → **86** |

**Hinweis zur Summe:** Die +35 neuen Fragen decken die Unterdeckung in fünf Sachgebieten ab. Die vier zusätzlichen Fragen gegenüber der reinen 82er-Summe entstehen durch bewussten **Überbestand** in zwei Sachgebieten (8+8 statt 7+5), der nicht entfernt wird.

### Zielverteilung nach Ausbau (86 Fragen in Bank)

| Sachgebiet | Nach Ausbau (geplant) |
|------------|----------------------:|
| Recht der öffentlichen Sicherheit und Ordnung | 8 |
| Gewerberecht | 8 |
| Datenschutzrecht | 5 |
| Bürgerliches Gesetzbuch | 13 |
| Strafgesetzbuch und Strafverfahrensrecht | 13 |
| Unfallverhütungsvorschriften Wach- und Sicherungsdienste | 8 |
| Umgang mit Waffen | 5 |
| Umgang mit Menschen | 19 |
| Grundzüge der Sicherheitstechnik | 7 |
| **Gesamt** | **86** |

Jedes Sachgebiet hat damit mindestens so viele Fragen wie in der 82er-Prüfung vorgesehen.

---

## 7. Qualitätsregeln für neue Fragen

Jede der **35 neuen Fragen** muss vor Aufnahme in `questions.json` geprüft werden:

1. **Kategorie** – exakt eines der 9 kanonischen Sachgebiete  
2. **Eindeutigkeit** – klare Fragestellung, keine doppelte richtige Lösung  
3. **Punktzahl** – 1 oder 2 Punkte; Anzahl richtiger Antworten passend (1 bzw. 2)  
4. **Antwortoptionen** – a–d oder a–e bei Kombinationsfragen  
5. **Erklärung** – fachlich korrekt, verständlich, Lernwert  
6. **Dubletten** – keine inhaltliche Duplikate zu bestehenden 51 Fragen  
7. **Formulierung** – prüfungsnah, aber **eigene Accaoui-Sprache**  
8. **IDs** – eindeutige neue `id` (z. B. fortlaufend `q_052` … `q_086`)  
9. **Metadaten** – `difficulty`, `examRelevance` sinnvoll setzen  
10. **Review** – Status in Review-Datei vor Merge (siehe §11)

Checkliste vor Merge: `python tools/audit-categories.py`, `python tools/preflight.py`, Browser-Test (Alle Fragen, Prüfung, Lernkarten).

---

## 8. Keine 1:1-Kopie von IHK-/Musterfragen

Entsprechend Master Context und Fragen-Datenbank-Plan:

**Nicht erlaubt:**

- offizielle IHK-Fragen oder Musterprüfungen **1:1** übernehmen  
- gleiche Antwortoptionen oder Reihenfolge kopieren  
- App als offizielle IHK-Prüfung darstellen  

**Erlaubt:**

- Sachgebiete und Prüfungsstruktur als **Orientierung**  
- Lernziele aus Mustern ableiten und **neu formulieren**  
- `sourceStyle: accaoui_original` (langfristig auch in Supabase)

Musterprüfungen sind **Analysequelle**, nicht Veröffentlichungsquelle.

---

## 9. Neue Fragen nur nach `docs/WRITTEN_QUESTION_STANDARD.md`

Alle neuen Fragen folgen dem verbindlichen Standard:

- Pflichtfelder: `id`, `category`, `question`, `points`, `answers`, `correctAnswers`, `explanation`, `difficulty`, `examRelevance`  
- Kanonische Kategorienamen (keine alten Kurzbezeichnungen)  
- Fragetypen: einfache Auswahl oder Kombinationsfrage (siehe Standard §4–§5)  
- App-Format wie in Standard §7 (Beispiel-JSON)

Abweichungen nur nach dokumentierter Ausnahme im Review.

---

## 10. Spätere technische Aufgabe: Prüfungsmodus mit 82 Fragen

**Noch nicht umsetzen** in v23.5.13 – nur als Ziel dokumentiert.

| Anforderung | Beschreibung |
|-------------|--------------|
| Pool | `questions.json` mit ≥ 82 Fragen, pro Sachgebiet ≥ Prüfungsziel |
| Auswahl | Bei Start „Prüfung“: **exakt 82 Fragen** nach Tabelle §3 |
| Zufall | Pro Sachgebiet zufällige Auswahl aus verfügbaren Fragen des Themas |
| Punkte | Summe **120 Punkte** entsprechend Gewichtung |
| Zeit | 120 Minuten (bestehende Logik prüfen/anpassen) |
| Bestehen | ≥ 50 % der Punkte |

**Beispiel-Logik (konzeptionell):**

```txt
Für jedes Sachgebiet:
  n = Anzahl laut Prüfungsgewichtung (z. B. BGB = 13)
  ziehe n Fragen zufällig aus allen Fragen dieser category in der Bank
Gesamt = 82 Fragen
```

Überbestand (z. B. 8 Fragen Öffentliches Recht, Ziel 7) erhöht die **Varianz** zwischen Prüfungsläufen.

Umsetzung geplant in **v25 – Schriftliche Prüfung ausbauen** (siehe `docs/CURSOR_MASTER_CONTEXT_ACCAOUI.md`).

---

## 11. Nächster praktischer Schritt

**Nicht** die 35 Fragen direkt in `questions.json` einfügen.

**Stattdessen:**

1. **Review-Dateien** anlegen (z. B. `docs/review/WRITTEN_EXPANSION_BLOCK_BGB.md` mit 8 Fragenentwürfen) – pro Sachgebiet oder in Blöcken à 10–15 Fragen  
2. Pro Frage: Kategorie, Entwurf, Antworten, Lösung, Erklärung, Dubletten-Check  
3. Fachliche Freigabe (Accaoui / Dozent)  
4. Erst danach kontrollierter Merge in `questions.json` (eigener Cursor-Task mit erlaubter Datei + Preflight)  
5. `audit-categories.py` und Browser-Test  

**Empfohlene Reihenfolge der Blöcke:**

1. Bürgerliches Gesetzbuch (+8)  
2. Strafgesetzbuch und Strafverfahrensrecht (+8)  
3. Umgang mit Menschen (+14) – größter Block, ggf. in zwei Review-Dateien  
4. Unfallverhütungsvorschriften (+3)  
5. Grundzüge der Sicherheitstechnik (+2)  

---

## Anhang – Bezugsdokumente

| Dokument | Inhalt |
|----------|--------|
| `docs/WRITTEN_QUESTION_STANDARD.md` | Format und Pflichtfelder |
| `docs/QUESTION_DATABASE_PLAN.md` | Review, Supabase, Veröffentlichung |
| `docs/PROJECT_MASTERLIST.md` | Projektstand, nächste Aufgaben |
| `docs/CURSOR_MASTER_CONTEXT_ACCAOUI.md` | 82-Fragen-Gewichtung, Roadmap v25 |

Dieser Ausbauplan ist die verbindliche Grundlage für v23.5.13 bis zum geplanten Merge der 35 neuen Fragen.
