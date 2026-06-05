# Accaoui §34a Lern-App – Lernstrategie-Modul (Vergessenskurve)

Stand: v23.5.29  
Status: **Konzept / Dokumentation** – noch **kein** App-Code  
Bezug: `docs/CURSOR_MASTER_CONTEXT_ACCAOUI.md`, `docs/PROJECT_MASTERLIST.md`, `docs/WRITTEN_QUESTION_EXPANSION_PLAN.md`

---

## 1. Zweck des Lernstrategie-Moduls

Das Lernstrategie-Modul soll Teilnehmern **verständlich erklären**, warum einmaliges Lesen nicht ausreicht und warum die Accaoui-App mit **Wiederholung**, **aktiver Abfrage** und **Praxisbezug** arbeitet.

Ziele:

1. **Motivation** – Lernen ist ein Prozess, kein Einmal-Ereignis  
2. **Orientierung** – sinnvolle Nutzung von Lernkarten, Fehlertraining und Prüfungssimulation  
3. **Didaktik** – Vergessenskurve als **Lernhilfe**, nicht als Angstbotschaft  
4. **Premium-Gefühl** – professionelles Lernsystem statt reiner Fragenliste  

**Wichtig:** Dieses Dokument beschreibt nur das **geplante** Modul. Umsetzung erfolgt **später** (v24.x oder v25.x), ohne sofortigen Code-Task.

---

## 2. Didaktischer Hintergrund

### Lernen braucht Wiederholung

Neues Wissen wird im Kurzzeitgedächtnis aufgenommen. Ohne gezielte Wiederholung und Abruf wird es nicht zuverlässig im Langzeitgedächtnis verankert.

### Wissen geht ohne Wiederholung schnell verloren

Die **Vergessenskurve** (Ebbinghaus-Prinzip) beschreibt, dass abrufbares Wissen nach dem ersten Lernen **rasch abfällt**, wenn nicht wiederholt oder angewendet wird.

### Rolle der Accaoui-Module

| Modul | Funktion im Lernprozess |
|-------|-------------------------|
| **Lernkarten** | Aktive Abfrage, kurze Wiederholungseinheiten |
| **Fehlertraining** | Gezielte Wiederholung falsch beantworteter Inhalte |
| **Prüfungssimulation** | Anwendung unter Zeitdruck, Prüfungsrealität |

Diese Bausteine sollen den natürlichen Vergessensprozess **auffangen** und in **planbare Lernzyklen** übersetzen.

---

## 3. Vergessenskurve – Richtwerte

Die folgenden Prozentwerte beschreiben **ca.-Richtwerte** für **abrufbares Wissen** nach dem ersten Lernen **ohne** gezielte Wiederholung:

| Zeit nach dem Lernen | Ca. abrufbares Wissen |
|----------------------|----------------------:|
| ca. 20 Minuten | **60 %** |
| ca. 1 Stunde | **45 %** |
| ca. 24 Stunden | **34 %** |
| ca. 6 Tagen | **23 %** |
| langfristig | **15 %** |

Diese Werte dienen der **didaktischen Visualisierung** in der App, nicht als individuelle Lernprognose.

---

## 4. Wichtiger Hinweis zu den Prozentwerten

Die genannten Prozentwerte sind **Richtwerte** auf Basis des bekannten Vergessenskurven-Modells.

Sie sind **keine**:

- festen medizinischen Werte  
- wissenschaftlich absoluten Messgrößen für jede Person  
- Garantie für individuelles Lernverhalten  

Abweichungen sind normal und hängen u. a. ab von:

- Vorwissen und Motivation  
- Schwierigkeit des Stoffs  
- Qualität der Erklärung  
- **Wiederholung**, **Anwendung** und **aktiver Abruf**  

In der App soll ein kurzer Hinweis erscheinen: *„Richtwerte – individuell kann es abweichen.“*

---

## 5. Darstellungsidee in der App

Das Modul soll **nicht** als statisches Bild eingebunden werden, sondern als **echtes App-Modul** mit Interaktion und konsistentem Accaoui-Design.

### UI-Idee

- **Farbige Prozent-Karten** oder **Chips** für jeden Zeitpunkt  
- **Kurze Erklärung** unter jedem Wert (z. B. „Nach einem Tag ohne Wiederholung …“)  
- Optional: sanfte Animation beim Einblenden (dezent, nicht ablenkend)  
- Verknüpfung mit **Call-to-Action**: „Jetzt Lernkarten starten“ / „Fehler wiederholen“  

### Beispieltext für die App

> **Wissen bleibt nicht durch einmaliges Lesen, sondern durch Wiederholung, Anwendung und aktive Abfrage.**

Ergänzende Kurztexte (optional):

- „Deshalb: kurze Einheiten, regelmäßig wiederholen.“  
- „Fehler sind Lernchancen – nutze das Fehlertraining.“  

---

## 6. Farbliche Idee (Prozent-Chips)

| Abrufbar (ca.) | Farbe | Bedeutung |
|----------------|-------|-----------|
| **60 %** | Grün | Noch gut präsent – Wiederholung jetzt besonders wirksam |
| **45 %** | Gelb | Abfall beginnt – aktiv abfragen |
| **34 %** | Orange | deutlicher Verlust ohne Wiederholung |
| **23 %** | Rot | nur noch Bruchteil ohne Training |
| **15 %** | Dunkel / Grau | langfristig ohne Wiederholung kaum abrufbar |

Farben sollen zur bestehenden Accaoui-UI passen (Dark-Mode-fähig, ausreichender Kontrast).

---

## 7. Drei Lernprinzipien

Das Modul verknüpft die Vergessenskurve mit drei Prinzipien, die die App bereits ansatzweise abbildet:

### Active Recall (aktiver Abruf)

Wissen wird durch **aktives Beantworten** gefestigt – nicht durch passives Lesen.  
**App-Bezug:** Lernkarten, Prüfungsmodus, Fehlertraining.

### Spaced Repetition (verteilte Wiederholung)

Wiederholung in **Abständen** ist effektiver als einmaliges Pauken.  
**App-Bezug:** Wiederholen-Karten, Fehlertraining, erneute Prüfungssimulation.

### Praxisbezug

Recht und Sicherheitspraxis müssen **anwendbar** sein – Fallbezug und Begründung wie in der mündlichen Prüfung.  
**App-Bezug:** Praxisfälle, Erklärungen, mündliche Prüfungssimulation.

---

## 8. Mögliche Einbauorte in der App

| Ort | Nutzen |
|-----|--------|
| **Dashboard** | Einstieg: „So lernst du nachhaltig“ |
| **Lernkarten-Übersicht** | Kontext vor dem Start einer Lernsession |
| **Fehlertraining** | Motivation: Fehler gezielt gegen Vergessen wirken |
| **Prüfungsergebnis** | Hinweis nach schlechtem/gutem Lauf: Wiederholung planen |
| **Onboarding (später)** | Neue Teilnehmer: Lernlogik der App verstehen |

Priorität für erste Umsetzung: **Dashboard** oder **Lernkarten-Übersicht** (geringer Eingriff, hoher Lerneffekt).

---

## 9. Technische Umsetzung (später)

| Aspekt | Stand v23.5.29 |
|--------|----------------|
| Code | **Noch nicht** umsetzen |
| Geplante Version | **v24.x** oder **v25.x** |
| Datenbank | Optional später Fortschritt/Wiederholungsintervalle (Supabase) |
| Abhängigkeiten | Keine Änderung an `app.js` / `questions.json` in diesem Task |

### Umsetzungsschritte (Grobraster)

1. UI-Komponente: Vergessenskurve als Karten/Chips  
2. Einbindung an einem Pilot-Ort (z. B. Dashboard)  
3. Browser-Test (Mobile + Desktop, Dark Mode)  
4. Optional: Verknüpfung mit Statistik / Wiederholungsempfehlung  

---

## 10. Bezug zur Sachkundeprüfung

Die §-34a-Prüfung verlangt **viel Stoff in begrenzter Zeit** (82 Fragen / 120 Punkte schriftlich). Das Lernstrategie-Modul erklärt, warum die App nicht nur „alle Fragen einmal durchklicken“ anbietet, sondern **Wiederholung und Simulation** als Kernwerkzeuge positioniert.

Details zum Prüfungsaufbau: `docs/PROJECT_MASTERLIST.md` (Abschnitt Sachkundeprüfung), `docs/CURSOR_MASTER_CONTEXT_ACCAOUI.md` §4.

---

*Accaoui-internes Didaktik-Konzept – keine medizinische oder psychologische Beratung.*
