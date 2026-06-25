# Accaoui §34a Lern-App – Projekt-Masterliste

Stand: v26.18c
Branch: `main`
Projektordner: `C:\xampp\htdocs\accaoui\v4-dashboard`
Repository: `asarrad-bit/accaoui-34a-lernapp`

---

## 1. Arbeitsregel

Keine Blind-Fixes.

Immer in dieser Reihenfolge arbeiten:

1. Prüfen
2. Klein ändern
3. Browser testen
4. Preflight ausführen
5. Committen
6. Pushen

Vor jedem Commit ausführen:

```bash
python tools/preflight.py
git diff --check
git status --short
```

Nur committen, wenn:

1. Preflight bestanden
2. `git diff --check` keine Ausgabe zeigt
3. nur erlaubte Dateien geändert wurden
4. Browser-Test bestanden ist

Optional bei bewusst freigegebenen Kern-Datei-Änderungen:

```powershell
$env:ACCAOUI_ALLOW_PROTECTED="index.html,app.js"
python tools/preflight.py
```

### Projektarbeitsregel: Arbeit / Zuhause

Bevor an der Accaoui §34a Lern-App gearbeitet wird, zuerst fragen:

> **„Bist du gerade auf Arbeit oder zuhause?“**

Danach immer klären:

1. richtiger Laptop / richtiger Arbeitsstand
2. `git status` prüfen
3. `git pull --ff-only` ausführen
4. nach der Arbeit **Commit + Push** nicht vergessen

Details: `docs/CURSOR_MASTER_CONTEXT_ACCAOUI.md` → Arbeitsworkflow / Git-Synchronisation.

---

## 2. Cursor-Regel

Cursor bekommt nur enge Aufträge.

Jeder Cursor-Auftrag enthält:

1. Ziel
2. erlaubte Dateien
3. verbotene Dateien
4. konkrete Änderung
5. was nicht geändert werden darf
6. Prüf-Befehle danach
7. kein Commit durch Cursor (außer ausdrücklich gewünscht)
8. keine Zusatzoptimierungen

Cursor darf nicht:

1. große Dateien komplett neu formatieren
2. Zeilenenden ändern
3. mehrere Bereiche gleichzeitig umbauen
4. Refactoring ohne Freigabe machen
5. `test/` ändern, außer ausdrücklich erlaubt

Referenz für neue Chats: `docs/CURSOR_MASTER_CONTEXT_ACCAOUI.md`

### Kennzeichnungs- und Sicherheitsregel

1. Cursor-Aufträge immer mit **„NUR FÜR CURSOR – NICHT IN GIT BASH“** kennzeichnen.
2. Git-Bash-Befehle immer mit **„NUR IN GIT BASH AUSFÜHREN“** kennzeichnen.
3. Cursor darf **keinen Commit** und **keinen Push** ausführen (außer ausdrücklich vom Nutzer gewünscht).

---

## 3. Technische Schutzregeln

Nicht mehr auf großen Dateien verwenden:

```bash
sed -i
```

Betroffene große Dateien:

1. `app.js`
2. `patch-v21.js`
3. `style.css`
4. `questions.json`

Für gezielte Änderungen lieber Python mit Trefferkontrolle verwenden.

`.editorconfig` ist aktiv.

### Preflight-Schutz für Kern-Dateien (ab v23.5.6)

`tools/preflight.py` prüft per `git status --short`, ob geschützte Kern-Dateien geändert wurden:

- `app.js`, `patch-v21.js`, `index.html`, `style.css`
- `oral-exam.css`, `oral-exam.js`, `oral-sheets.js`, `oral-sheets-v23.js`
- `questions.json`
- `data/oral-question-bank.js`, `data/oral-sheets-bank.js`

Bei Treffer ohne Freigabe: Preflight-Fehler mit Hinweis, nur zu committen, wenn die Datei für den Task freigegeben wurde.

Kontrollierte Freigabe: Umgebungsvariable `ACCAOUI_ALLOW_PROTECTED` (kommagetrennte Pfade).

---

## 4. Aktive Hauptdateien

**Der Root-Ordner ist führend.**

**Der Ordner `test/` ist nicht führend und darf nicht als Referenz genutzt werden.**

`index.html` lädt aktiv (Reihenfolge laut Einbindung):

1. `style.css`
2. `oral-exam.css`
3. `app.js`
4. `patch-v21.js`
5. `data/oral-question-bank.js`
6. `data/oral-sheets-bank.js`
7. `oral-sheets.js`
8. `oral-sheets-v23.js`
9. `oral-exam.js`

Weitere führende Dateien im Root:

- `index.html`
- `questions.json`

Werkzeuge (nicht in der App geladen, aber Pflicht vor Commit):

- `tools/preflight.py`
- `tools/audit-categories.py`

---

## 5. Aktueller Versionsstand (bis v26.18c)

### App und mündliche Prüfung (Auszug)

| Version | Inhalt |
|---------|--------|
| v23.4.0 | Mündlicher Fehlertrainer: stabiler Renderer `showOralMistakeTrainingV2340()` |
| v23.4.1 | „FRAGT JETZT“-Badge (Prüfersimulation) |
| v23.4.2 | Fehlerübersicht schriftlich bereinigt |
| v23.4.3 | Kanonische Kategorien + `normalizeCategoryName()` |
| v23.4.4–v23.4.6 | Mündliche/schriftliche Datenquellen und Kategorien normalisiert |
| v23.4.7 | `tools/audit-categories.py` |
| v23.4.8 | `tools/preflight.py` (Basis) |
| v23.5.1 | Simulation B: Button/Start im Modus-Select (Patch) |
| v23.5.2 | Mündliche Prüfung funktional getestet (Simulation A/B, Musterantworten, Bewertung, Fehlertraining, Online-Anzeige) |
| v23.5.6 | Preflight: Schutz geschützter Kern-Dateien + `ACCAOUI_ALLOW_PROTECTED` |

### Dokumentation und Supabase-Planung (v23.5.5–v23.5.10)

| Version | Dokument / Inhalt |
|---------|-------------------|
| v23.5.5 | `docs/QUESTION_DATABASE_PLAN.md` |
| v23.5.5 | `docs/WRITTEN_QUESTION_STANDARD.md` (Vorbereitung) |
| v23.5.7 | `docs/SUPABASE_QUESTION_SCHEMA.md` |
| v23.5.8 | `docs/SUPABASE_USER_PROGRESS_SCHEMA.md` |
| v23.5.9 | `docs/SUPABASE_IMPLEMENTATION_ROADMAP.md` |
| v23.5.10 | `docs/PROJECT_MASTERLIST.md` und `README.md` aktualisiert |
| v23.5.29 | `docs/LEARNING_STRATEGY_MODULE.md` (Vergessenskurve, Lernprinzipien); Prüfungsaufbau § 34a in `PROJECT_MASTERLIST.md` §7 |
| v23.5.48 | Fragenbank-Ausbau abgeschlossen: **86 Fragen** in `questions.json` (inkl. Umgang mit Menschen `umgang_006`–`umgang_019`) |
| v24.0 | `docs/EXAM_SIMULATION_AUDIT.md` – Prüfungssimulation 82/120 auditiert; **kein Code-Task** |
| v24.1 | `docs/EXAM_POINTS_PLAN.md` – Punktefelder fachlich geplant (86 Fragen, Simulationskern 82/120); **keine** `questions.json`-Änderung |
| v24.2 | `docs/EXAM_CORE_SELECTION_PLAN.md` – **Option A:** feste 82 Core-IDs; 4 Reserve-IDs |
| v24.3a–i | `points`-Felder in `questions.json` für alle **9 Sachgebiete** vollständig gesetzt |
| v24.3j | Globaler `points`-Check: **82 Core-Fragen / 120 Punkte / 38 Zweipunktfragen** erfolgreich |
| v24.3x | Teilpunkte-Bewertung ab 01.07.2025 auditiert (`EXAM_SIMULATION_AUDIT.md` §10, `EXAM_POINTS_PLAN.md` §10) – **Dokumentation** |
| v24.4b | Vollsimulation nutzt feste **82-Core-Fragen** (`EXAM_CORE_QUESTION_IDS_V244` in `app.js`) |
| v24.5 | Teilpunkte-Logik für Mehrfachantworten im Prüfungsmodus eingebaut (+1 pro richtigem Kreuz) |
| v24.6b | Wiederholungslogik/offene Fragen nach Prüfung; frühe Abgabe; offene Fragen in Auswertung sichtbar – **erledigt** |
| v24.6d | Fragenreihenfolge in Lern-/Wiederholungs-/Fehlermodi wird gemischt – **erledigt** |
| v24.6e | Antwortreihenfolge wird gemischt; korrekte Indizes intern korrekt; `questions.json` unverändert – **erledigt** |
| v24.6f | Prüfungsanalyse responsive stabil (Desktop/Mobile, keine Überlappung) – **erledigt** |
| v24.6g | Fehlerübersicht nach Themen: Premium-Kartenlook, responsive stabil – **erledigt** |
| v24.6x | Prüfungsanalyse optisch/funktional verbessert; Buttontexte; nutzerfreundlicher – **erledigt** |
| v24.6c | Prüfung pausieren / Prüfung fortsetzen; aktive Prüfung wird in `localStorage` gespeichert; Dashboard-Karte „Angefangene Prüfung“; nach Abgabe wird die aktive Session gelöscht – **erledigt** |
| v24.6a | Doppelten Button „Prüfung pausieren“ in der Vollsimulation entfernt; nur ein Pause-Button bleibt sichtbar – **erledigt** |
| v24.7a | Prüfungsnavigation kompakter/einklappbar: 82 Zahlen nicht dauerhaft sichtbar; Summary zeigt aktuelle Frage, beantwortete und offene Fragen; Fragenübersicht per Button ein-/ausblendbar – **erledigt** |
| v24.7b | Lernmodus pausieren / fortsetzen: aktive Lerneinheit wird in `localStorage` gespeichert; Dashboard-Karte „Angefangene Lerneinheit“; Button „Lernen pausieren“ neben „Auswertung anzeigen“; gespeicherte Lerneinheit kann fortgesetzt oder gelöscht werden – **erledigt** |
| v24.7c | Lernmodus-Fortsetzen stabilisiert: ausgewählte Antworten bleiben nach Pause/Fortsetzen sichtbar; bereits ausgewertete Fragen stellen Erklärung, Markierungen und „Nächste Frage“ korrekt wieder her – **erledigt** |
| v24.7d | Automatisches Sicherheits-Speichern bei App-Verlassen: laufende Prüfung oder Lerneinheit wird bei Tab-Wechsel, Browser-Hintergrund, Neuladen oder Schließen automatisch in `localStorage` gesichert – **erledigt** |
| v24.7e | Auto-Save Feintest bestanden: Lernmodus bei Tab-Wechsel, Lernmodus bei Browser-Neuladen und Prüfung bei Browser-Neuladen wurden erfolgreich getestet; Dashboard-Karten „Angefangene Lerneinheit“ und „Angefangene Prüfung“ erscheinen korrekt – **erledigt** |
| v24.8 | Auto-Save-Anzeige ergänzt: nach automatischer Sicherung erscheint eine kleine, unaufdringliche Statusanzeige „Automatisch gespeichert“; Cache-Versionen für `app.js` und `style.css` in `index.html` auf v24.8 gesetzt – **erledigt** |
| v24.9 | Stabilitätstest nach Auto-Save/Pause/Fortsetzen bestanden: Lernmodus-Pause, Lernmodus-Auto-Save, Prüfung-Pause, Prüfung-Auto-Save bei Reload und Session-Löschung nach Abgabe erfolgreich geprüft – **erledigt** |
| v25.0 | Kompletter Qualitätscheck der App durchgeführt: Dashboard, Alle Fragen, Lernkarten, Prüfung, Fehlertraining und mündliche Prüfung geprüft; aktuell keine Fehler festgestellt – **erledigt** |
| v25.1 | Mündliche Prüfung erweitert: vorhandener Prüfungsbogen B aus `oral-sheets-v23.js` ist jetzt in der Modusauswahl startbar; 15 Fallfragen mit Musterantworten, Prüferhinweisen und Auswertung erfolgreich getestet – **erledigt** |
| v25.2a | Mündliche Prüfung erweitert: Prüfungsbogen C als vollständiger Datensatz mit 15 Accaoui-original Fallfragen in `oral-sheets-v23.js` ergänzt – **erledigt** |
| v25.2b | Prüfungsbogen C in der Modusauswahl startbar gemacht; Browser-Test bestanden; Prüfungsbögen A/B/C sind jetzt aktiv – **erledigt** |
| v25.2c | `PROJECT_MASTERLIST.md` auf aktuellen Stand aktualisiert: A/B/C aktiv, insgesamt 45 mündliche Simulationsfragen dokumentiert – **erledigt** |
| v25.3a | Mündliche Prüfung erweitert: Prüfungsbogen D als vollständiger Datensatz mit 15 Accaoui-original Fallfragen in `oral-sheets-v23.js` ergänzt – **erledigt** |
| v25.3b | Prüfungsbogen D in der Modusauswahl startbar gemacht; Browser-Test bestanden; Prüfungsbögen A/B/C/D sind jetzt aktiv – **erledigt** |
| v25.3c | `PROJECT_MASTERLIST.md` auf aktuellen Stand aktualisiert: A/B/C/D aktiv, insgesamt 60 mündliche Simulationsfragen dokumentiert – **erledigt** |
| v25.4a | Mündliche Prüfung erweitert: Prüfungsbogen E als vollständiger Datensatz mit 15 Accaoui-original Fallfragen in `oral-sheets-v23.js` ergänzt – **erledigt** |
| v25.4b | Prüfungsbogen E in der Modusauswahl startbar gemacht; Prüfungsbögen A/B/C/D/E sind jetzt aktiv – **erledigt** |
| v25.4c | `PROJECT_MASTERLIST.md` auf aktuellen Stand aktualisiert: A/B/C/D/E aktiv, insgesamt 75 mündliche Simulationsfragen dokumentiert – **erledigt** |
| v25.5 | Qualitäts-/Stabilitätstest der mündlichen Prüfung A/B/C/D/E bestanden: alle fünf Prüfungsbögen sichtbar und startbar; Frageanzeige, Musterantwort, Weiter-Navigation und Prüferanzeige geprüft – **erledigt** |
| v25.6 | UI-Feinschliff mündliche Prüfung: Buttonlabel der bisherigen 15-Minuten-Simulation zu `Prüfungsbogen A` vereinheitlicht; A/B/C/D/E optisch konsistent – **erledigt** |
| v25.6c | `PROJECT_MASTERLIST.md` auf aktuellen Stand aktualisiert: Prüfungsbogen A Label vereinheitlicht, A/B/C/D/E weiterhin aktiv, insgesamt 75 mündliche Simulationsfragen dokumentiert – **erledigt** |
| v25.7 | Auswahlfenster der mündlichen Prüfung geprüft: Prüfungsbögen A/B/C/D/E sichtbar, Reihenfolge korrekt, Darstellung im Browser sauber; keine weitere UI-Änderung erforderlich – **erledigt** |
| v25.8a | Zufallsprüfung für die mündliche Prüfung eingebaut: 15 zufällige Fragen aus Prüfungsbogen A/B/C/D/E, eigene sheetId `oral_random_v258a`, keine doppelte Fragenlogik innerhalb einer Runde – **erledigt** |
| v25.8b | Zufallsprüfung im Browser getestet: Button sichtbar, Start funktioniert, Frageanzeige/Musterantwort/Navigation sauber, keine Fehlermeldung gemeldet – **erledigt** |
| v25.9 | Abschluss-Audit mündliche Prüfung: Prüfungsbögen A/B/C/D/E, Zufallsprüfung, Auswahlfenster, Startlogik, Navigation und Dokumentation geprüft; Modulstand stabil – **erledigt** |
| v26.0a | Schriftliche Prüfung Dokumentations-Audit bereinigt: alte offene Hinweise zu Browser-Endtest und Pause/Fortsetzen korrigiert; 82-Core-Fragen, 120 Punkte, Teilpunkte, Mix, Fokusnavigation und Pause/Fortsetzen als umgesetzter Stand dokumentiert – **erledigt** |
| v26.0b | Schriftliche Prüfung Live-Code-Audit durchgeführt: `EXAM_FULL_QUESTION_LIMIT_V20 = 82`, feste Core-ID-Liste `EXAM_CORE_QUESTION_IDS_V244`, 120-Minuten-Timer, 50-Prozent-Bestehensgrenze, Punkte-/Teilpunkte-Berechnung sowie Pause/Fortsetzen im Code bestätigt – **erledigt** |
| v26.0c | Browser-Endtest schriftliche Vollsimulation bestanden: 82 Fragen sichtbar, 120-Minuten-Timer sichtbar, Prüfung pausieren und fortsetzen funktioniert, Antworten bleiben erhalten – **erledigt** |
| v26.1c | Lernkarten pausieren / fortsetzen eingebaut und browsergetestet: Lernkartenrunde wird lokal gespeichert, Dashboard-Karte „Angefangene Lernkarten“ erscheint, Fortsetzen stellt Karte und Fortschritt wieder her; Premium-Leiste optisch verbessert – **erledigt** |
| v26.1d | Masterliste auf Lernkarten-Abschluss aktualisiert; offene Retest-Hinweise bereinigt und Lernkartenstatus auf v26.1c gesetzt – **erledigt** |
| v26.2a | Masterliste-Altlasten bereinigt: alte Hinweise zu „späterer Vollsimulation“, offenem Pausieren/Fortsetzen und geplantem UX-/Lernlogik-Audit an den tatsächlichen App-Stand angepasst – **erledigt** |
| v26.3a | Supabase Login- und Teilnehmerzugang-Plan erstellt: Login/Auth, Teilnehmerprofil, Kursfreischaltung, Ablaufdatum/Zugangsdauer, Rollenmodell und v27.0-Startentscheidung dokumentiert – **erledigt** |
| v26.3b | Masterliste auf Supabase/Login-Plan aktualisiert; neues Dokument `docs/SUPABASE_LOGIN_ACCESS_PLAN.md` als verbindlicher nächster Business-Block verankert – **erledigt** |
| v26.3c | Login-UI-Konzept erstellt: künftiger App-Start über Auth-Status, Login-Seite, gültiger Zugang, abgelaufener Kurs, gesperrter Zugang und fehlende Kurszuordnung dokumentiert – **erledigt** |
| v26.3d | Masterliste auf Login-UI-Konzept aktualisiert; neues Dokument `docs/SUPABASE_LOGIN_UI_CONCEPT.md` verankert – **erledigt** |
| v26.3e | Auth-Einstiegspunkt-Audit erstellt: bestehender DOMContentLoaded-Start, loadAllLocalData, activateDashboardButtons, loadQuestions und location.reload-Risiken für späteren Login geprüft – **erledigt** |
| v26.3f | Masterliste auf Auth-Einstiegspunkt-Audit aktualisiert; neues Dokument `docs/SUPABASE_AUTH_ENTRYPOINT_AUDIT.md` verankert – **erledigt** |
| v26.4a | Lokales Auth-Guard-Gerüst in `app.js` ergänzt: App-Start läuft jetzt über `initAppBoot()`, `initAuthFlow()` und `startLocalApp()`; Supabase bewusst noch nicht verbunden, App bleibt offen und startet wie bisher – **erledigt** |
| v26.4b | Masterliste auf lokalen Auth-Guard aktualisiert; v26.4a als erster technischer Login-Vorbereitungsschritt verankert – **erledigt** |
| v26.4c | Lokaler Auth-Guard-Testmodus ergänzt: Teststatus über `accaoui_auth_guard_test_state` für `login_required`, `expired`, `blocked` und `no_course`; Standard bleibt weiterhin offener App-Zugang – **erledigt** |
| v26.4d | Masterliste auf Auth-Guard-Testmodus aktualisiert; v26.4c als lokaler Testschritt vor echter Supabase-Anbindung verankert – **erledigt** |
| v26.4e | Auth-Hinweisseiten optisch verbessert: Login erforderlich, Kurs abgelaufen, Zugang gesperrt und kein aktiver Kurs erhalten professionelles Card-Design mit Statusanzeige und Reset-Button – **erledigt** |
| v26.4f | Masterliste auf Auth-Hinweisdesign aktualisiert; v26.4e als UI-Qualitätsschritt vor echter Supabase-Anbindung verankert – **erledigt** |
| v26.5a | Supabase-Konfigurations- und Sicherheitsplan erstellt: erlaubte Frontend-Konfiguration, Verbot von service_role-Key im Frontend, RLS-Grundsätze und spätere Konfigurationsdatei vorbereitet – **erledigt** |
| v26.5b | Masterliste auf Supabase-Konfigurations- und Sicherheitsplan aktualisiert; neues Dokument `docs/SUPABASE_CONFIG_SAFETY_PLAN.md` verankert – **erledigt** |
| v26.5c | Supabase-Konfigurationsplatzhalter erstellt: `data/supabase-config.example.js` ohne echte Keys ergänzt und `data/supabase-config.local.js` über `.gitignore` vor versehentlichem Commit geschützt – **erledigt** |
| v26.5d | Masterliste auf Supabase-Konfigurationsplatzhalter aktualisiert; v26.5c als sicherer Vorbereitungsschritt ohne echte Supabase-Keys verankert – **erledigt** |
| v26.5e | Supabase-Config-Ladeweg-Audit erstellt: aktueller Script-Ladeweg, `supabase-config.example.js`, geschützte `supabase-config.local.js`, service_role-Verbot und späterer optionaler Config-Loader dokumentiert – **erledigt** |
| v26.5f | Masterliste auf Supabase-Config-Ladeweg-Audit aktualisiert; neues Dokument `docs/SUPABASE_CONFIG_LOADING_AUDIT.md` verankert – **erledigt** |
| v26.6a | Supabase-Config-State-Check in `app.js` ergänzt: `getSupabaseConfigState()` erkennt `local_mode`, `placeholder_config` und `config_available`; keine echte Supabase-Verbindung, kein SDK, kein Login-Zwang – **erledigt** |
| v26.6b | Masterliste auf Supabase-Config-State-Check aktualisiert; v26.6a als sicherer technischer Vorbereitungsschritt ohne Live-Verbindung verankert – **erledigt** |
| v26.6c | Optionaler lokaler Supabase-Config-Loader ergänzt: App versucht `data/supabase-config.local.js` zu laden, bleibt bei fehlender Datei im lokalen Modus; keine echte Supabase-Verbindung, kein SDK, kein Login-Zwang – **erledigt** |
| v26.6d | Masterliste auf optionalen Supabase-Config-Loader aktualisiert; v26.6c als sicherer Ladeweg ohne Live-Verbindung verankert – **erledigt** |
| v26.6e | Optionaler Supabase-Config-Loader lokal getestet: `data/supabase-config.local.js` mit Fake-Testwerten wurde erkannt, Konsole zeigte `local_config_loaded` und `config_available`; Datei danach gelöscht, keine echten Keys, keine Live-Verbindung – **erledigt** |
| v26.6f | Masterliste auf Config-Loader-Test aktualisiert; neues Dokument `docs/SUPABASE_CONFIG_LOADER_TEST.md` verankert – **erledigt** |
| v26.7a | Supabase-Client-Adapter-Plan erstellt: klare Adapter-Schicht für spätere Supabase-Kommunikation, Auth, Session, Profil, Kurszugang und Fortschritt geplant; kein SDK, keine echte Verbindung, keine echten Keys – **erledigt** |
| v26.7b | Masterliste auf Supabase-Client-Adapter-Plan aktualisiert; neues Dokument `docs/SUPABASE_CLIENT_ADAPTER_PLAN.md` verankert – **erledigt** |
| v26.7c | Supabase-Client-Adapter-Gerüst ohne SDK ergänzt: `data/supabase-client-adapter.js` eingebunden, Adapter stellt `ACCAOUI_SUPABASE_ADAPTER`, Config-State, Client-State, Session-Stub und Access-State-Stub bereit; keine echte Verbindung, keine echten Keys, kein Login-Zwang – **erledigt** |
| v26.7d | Masterliste auf Supabase-Adapter-Gerüst aktualisiert; v26.7c als sicherer technischer Adapter-Schritt ohne SDK verankert – **erledigt** |
| v26.7e | Supabase-Client-Adapter-Gerüst lokal getestet: `ACCAOUI_SUPABASE_ADAPTER` vorhanden, Version `v26.7c`, `getClientState()`, `getCurrentSession()` und `getParticipantAccessState()` geprüft; Ergebnis: lokaler Modus, keine Session, `local_access_granted`, kein SDK, keine Live-Verbindung – **erledigt** |
| v26.7f | Masterliste auf Supabase-Adapter-Test aktualisiert; neues Dokument `docs/SUPABASE_CLIENT_ADAPTER_TEST.md` verankert – **erledigt** |
| v26.8a | Supabase-SDK-Ladeweg-Plan erstellt: späterer SDK-Ladeweg, Client-Erzeugung nur bei gültiger Config, lokaler Fallback, Adapter-Grenze und service_role-Verbot dokumentiert; kein SDK, keine Live-Verbindung, keine echten Keys – **erledigt** |
| v26.8b | Masterliste auf Supabase-SDK-Ladeweg-Plan aktualisiert; neues Dokument `docs/SUPABASE_SDK_LOADING_PLAN.md` verankert – **erledigt** |
| v26.8c | Supabase-Adapter um SDK-Status vorbereitet: `getSdkState()` ergänzt, Status `sdk_missing`, `sdk_invalid`, `sdk_available` vorbereitet; `getClientState()` trennt jetzt Config-State und SDK-State; kein SDK eingebunden, keine Live-Verbindung, keine echten Keys – **erledigt** |
| v26.8d | Masterliste auf Supabase-SDK-Status im Adapter aktualisiert; v26.8c als sicherer technischer Vorbereitungsschritt ohne SDK verankert – **erledigt** |
| v26.8e | Supabase-SDK-Status-Test dokumentiert: Adapter meldet ohne SDK korrekt `sdk_missing`, `hasSdk: false`, `window_supabase_missing`; App bleibt lokal stabil, keine Live-Verbindung, keine echten Keys – **erledigt** |
| v26.8f | Masterliste auf Supabase-SDK-Status-Test aktualisiert; neues Dokument `docs/SUPABASE_SDK_STATE_TEST.md` verankert – **erledigt** |
| v26.9a | Supabase-Client-Readiness im Adapter vorbereitet: `getClientReadinessState()` ergänzt, Gründe für `local_mode`, `placeholder_config`, `sdk_missing`, `sdk_invalid` und späteres `client_ready_later` getrennt; `canCreateClient: false` bleibt aktiv, kein SDK, keine Live-Verbindung, keine echten Keys – **erledigt** |
| v26.9b | Masterliste auf Supabase-Client-Readiness aktualisiert; v26.9a als sicherer Adapter-Vorbereitungsschritt ohne Client-Erzeugung verankert – **erledigt** |
| v26.9c | Supabase-Client-Readiness-Test dokumentiert: ohne Config und ohne SDK meldet der Adapter korrekt `local_mode`, `sdk_missing`, `canCreateClient: false` und `no_config_loaded`; App bleibt lokal stabil – **erledigt** |
| v26.9d | Masterliste auf Supabase-Client-Readiness-Test aktualisiert; neues Dokument `docs/SUPABASE_CLIENT_READINESS_TEST.md` verankert – **erledigt** |
| v26.10a | Supabase-Auth-Readiness im Adapter vorbereitet: `getAuthReadinessState()` ergänzt, Status `client_not_ready` und späterer Zustand `auth_ready_later` vorbereitet; `getCurrentSession()` liefert bei fehlendem Client `no_session_client_not_ready`; kein SDK, keine Live-Verbindung, keine echten Keys, kein Login-Zwang – **erledigt** |
| v26.10b | Masterliste auf Supabase-Auth-Readiness aktualisiert; v26.10a als sicherer Adapter-Vorbereitungsschritt ohne Auth-Prüfung und ohne Client-Erzeugung verankert – **erledigt** |
| v26.10c | Supabase-Auth-Readiness-Test dokumentiert: ohne Config, ohne SDK und ohne Client meldet der Adapter korrekt `client_not_ready`, `canCheckSession: false`, `no_session_client_not_ready` und `local_access_granted`; App bleibt lokal stabil – **erledigt** |
| v26.10d | Masterliste auf Supabase-Auth-Readiness-Test aktualisiert; neues Dokument `docs/SUPABASE_AUTH_READINESS_TEST.md` verankert – **erledigt** |
| v26.11a | Teilnehmerzugangs-Readiness im Supabase-Adapter vorbereitet: `getParticipantAccessReadinessState()` ergänzt, lokaler Zugriff bleibt bei nicht bereitem Supabase bewusst erlaubt (`local_access_granted`), spätere Status `participant_active_later`, `course_expired_later`, `participant_blocked_later`, `no_course_later` und `no_session_later` vorbereitet; kein SDK, keine Live-Verbindung, keine echten Keys, kein Login-Zwang – **erledigt** |
| v26.11b | Masterliste auf Teilnehmerzugangs-Readiness aktualisiert; v26.11a als sicherer Adapter-Vorbereitungsschritt ohne echten Teilnehmerzugang und ohne Login-Zwang verankert – **erledigt** |
| v26.11c | Teilnehmerzugangs-Readiness-Test dokumentiert: lokaler Zugriff bleibt ohne Supabase bewusst erlaubt; `local_access_granted`, `supabase_not_ready_local_access` und spätere Status vorbereitet – **erledigt** |
| v26.11d | Supabase-Adapter-Health-State ergänzt: `getAdapterHealthState()` bündelt Config-State, SDK-State, Client-Readiness, Auth-Readiness und Teilnehmerzugangs-Readiness – **erledigt** |
| v26.11e | Supabase-Adapter-Health-State-Test dokumentiert: zentrale Gesamtübersicht geprüft; lokaler Modus bleibt stabil, kein SDK, keine Live-Verbindung, keine echten Keys, kein Login-Zwang – **erledigt** |
| v26.12a | `app.js` an Supabase-Adapter-Health-State angebunden: `getSupabaseAdapterHealthState()`, `logSupabaseAdapterHealthState()` und `window.ACCAOUI_SUPABASE_APP_HEALTH_STATE` ergänzt – **erledigt** |
| v26.12b | Supabase-App-Health-Hook-Test dokumentiert: App liest zentralen Adapter-Health-State im lokalen Modus – **erledigt** |
| v26.12c | Access-Flow an Adapter-Health-State angebunden: `getCurrentAccessState()` nutzt den Health-State, lokaler Zugriff bleibt erlaubt, solange Supabase nicht live ist – **erledigt** |
| v26.12d | Supabase-Access-Flow-Health-Test dokumentiert: Dashboard, Lernkarten und Prüfung bleiben lokal nutzbar, kein Login-Zwang – **erledigt** |
| v26.12e | Masterliste auf Teilnehmerzugang, Adapter-Health-State, App-Health-Hook und Access-Flow-Health aktualisiert; neue Testdokumente verankert – **erledigt** |
| v26.13a | Supabase-Live-Schalter vorbereitet: `window.ACCAOUI_SUPABASE_LIVE_ENABLED === true` als bewusster späterer Aktivierungsschalter; Supabase bleibt ohne Schalter lokal gesperrt – **erledigt** |
| v26.13b | Supabase-Live-Schalter-Test dokumentiert: Adapter-Version, Live-Schalter, Health-State und lokale Freigabe geprüft – **erledigt** |
| v26.13c | Masterliste auf Supabase-Live-Schalter und Testdokument aktualisiert – **erledigt** |
| v26.14a | Supabase-Live-Schalter-Dry-Run dokumentiert: Live-Schalter testweise auf `true`, aber ohne Config, SDK, Client-Erzeugung und Sessionprüfung bleibt Supabase sicher lokal blockiert – **erledigt** |
| v26.14b | Masterliste um Supabase-Live-Schalter-Dry-Run und neues Testdokument ergänzt – **erledigt** |
| v26.15a | Supabase-Fail-Safe-Status ergänzt: `getSupabaseFailSafeState()`, `failSafeStatus` und `isFailSafeSafe`; der Adapter meldet klar, warum Supabase nicht live geht – **erledigt** |
| v26.15b | Supabase-Fail-Safe-Status-Test dokumentiert: Normalmodus und Dry-Run geprüft, Supabase bleibt ohne Config, SDK und Client-Erzeugung sicher lokal blockiert – **erledigt** |
| v26.15c | Masterliste um Supabase-Fail-Safe-Status und Testdokument ergänzt – **erledigt** |
| v26.16a | Sicherer Supabase-Config-Loader ergänzt: `data/supabase-config-loader.js`, Loader-State im Adapter-Health-State, weiterhin ohne echte Keys, SDK, Client und Live-Verbindung – **erledigt** |
| v26.16b | Supabase-Config-Loader-Test dokumentiert: Loader lädt sicher, Autoload bleibt aus, Adapter erkennt Loader, Supabase bleibt lokal blockiert – **erledigt** |
| v26.16c | Masterliste um Supabase-Config-Loader und Testdokument ergänzt – **erledigt** |
| v26.17a | Supabase-Config-Loader-Boot-State ergänzt: `getBootLoadState()`, Boot-Status `local_config_autoload_disabled`, `loadStatus: skipped`, weiterhin ohne Autoload, Client und Sessionprüfung – **erledigt** |
| v26.17b | Supabase-Config-Loader-Boot-State-Test dokumentiert: Boot-State sichtbar, Autoload bleibt aus, App bleibt lokal sicher – **erledigt** |
| v26.17c | Masterliste um Config-Loader-Boot-State und Testdokument ergänzt – **erledigt** |
| v26.18a | Adapter-Health-State erweitert: `configLoaderBootStatus`, `configLoaderBootLoadStatus`, `isConfigLoaderBootSafe`, `isConfigLoaderAutoLoadEnabled`; Boot-State des Config-Loaders ist nun im Adapter sichtbar – **erledigt** |
| v26.18b | Adapter-Health-Boot-State-Test dokumentiert: Adapter erkennt Boot-State, Autoload bleibt aus, kein Client, keine Sessionprüfung – **erledigt** |
| v26.18c | Masterliste um Adapter-Health-Boot-State und Testdokument ergänzt – **erledigt** |

**Hinweis:** Supabase ist geplant, aber noch **nicht live** in der App eingebunden (kein SQL, keine echte Supabase-Verbindung). Seit v26.3a ist der Login-/Teilnehmerzugang-Plan vorhanden; seit v26.3c ist das Login-UI-Konzept dokumentiert; seit v26.3e ist der spätere Auth-Einstiegspunkt geprüft; seit v26.4a existiert ein lokales Auth-Guard-Gerüst ohne Login-Zwang; seit v26.4c sind lokale Teststatus für Login-/Sperr-/Ablaufseiten vorhanden; seit v26.4e sind diese Hinweisseiten optisch verbessert; seit v26.5a ist der Supabase-Konfigurations- und Sicherheitsplan dokumentiert; seit v26.5c existiert ein sicherer Config-Platzhalter ohne echte Keys; seit v26.5e ist der spätere Config-Ladeweg dokumentiert; seit v26.6a erkennt die App lokal den Supabase-Config-Status ohne Live-Verbindung; seit v26.6c ist ein optionaler lokaler Config-Loader vorhanden; seit v26.6e ist dieser Loader lokal getestet; seit v26.7a ist die spätere Supabase-Adapter-Schicht geplant; seit v26.7c existiert ein Adapter-Gerüst ohne SDK und ohne Live-Verbindung; seit v26.7e ist dieses Adapter-Gerüst lokal getestet; seit v26.8a ist der spätere Supabase-SDK-Ladeweg geplant; seit v26.8c erkennt der Adapter zusätzlich den SDK-Status ohne SDK-Live-Anbindung; seit v26.8e ist dieser SDK-Status lokal getestet; seit v26.9a ist die Client-Readiness-Auswertung im Adapter vorbereitet; seit v26.9c ist diese Readiness lokal getestet; seit v26.10a ist die Auth-Readiness im Adapter vorbereitet; seit v26.10c ist diese Auth-Readiness lokal getestet; seit v26.11a ist die Teilnehmerzugangs-Readiness im Adapter vorbereitet.

---

## 6. Kanonische Kategorien

Feste Reihenfolge (9 Sachgebiete):

1. Recht der öffentlichen Sicherheit und Ordnung
2. Gewerberecht
3. Datenschutzrecht
4. Bürgerliches Gesetzbuch
5. Strafgesetzbuch und Strafverfahrensrecht
6. Unfallverhütungsvorschriften Wach- und Sicherungsdienste
7. Umgang mit Waffen
8. Umgang mit Menschen
9. Grundzüge der Sicherheitstechnik

Alte Begriffe dürfen nur noch als Mapping in `normalizeCategoryName()` stehen.

---

## 7. Sachkundeprüfung nach § 34a GewO – Prüfungsaufbau (Grundlage)

Der offizielle Aufbau der **Sachkundeprüfung nach § 34a GewO** ist für die App-Planung dokumentiert (siehe auch `docs/CURSOR_MASTER_CONTEXT_ACCAOUI.md` §4, `docs/WRITTEN_QUESTION_EXPANSION_PLAN.md`).

### Schriftliche Prüfung

| Merkmal | Vorgabe |
|---------|---------|
| Aufgaben | **82 geschlossene Aufgaben** |
| Bearbeitungszeit | **120 Minuten** |
| Bestehensgrenze | mindestens **50 Prozent** der Punkte |
| Hilfsmittel | **nicht erlaubt** |
| Mündliche Zulassung | nur bei **bestandenem schriftlichen Teil** |

### Punkte- und Fragengewichtung (schriftlich)

| Nr | Sachgebiet | Fragen | Punkte |
|----|------------|-------:|-------:|
| 1 | Recht der öffentlichen Sicherheit und Ordnung | 7 | 11 |
| 2 | Gewerberecht | 5 | 8 |
| 3 | Datenschutzrecht | 5 | 8 |
| 4 | Bürgerliches Gesetzbuch | 13 | 21 |
| 5 | Strafgesetzbuch und Strafverfahrensrecht | 13 | 21 |
| 6 | Unfallverhütungsvorschriften Wach- und Sicherungsdienste | 8 | 13 |
| 7 | Umgang mit Waffen | 5 | 8 |
| 8 | Umgang mit Menschen | 19 | 19 |
| 9 | Grundzüge der Sicherheitstechnik | 7 | 11 |
| | **Gesamt** | **82** | **120** |

### Wichtige App-Regel (Fragenbank vs. Prüfung)

Die **Fragenbank** in `questions.json` darf **größer als 82 Fragen** sein (Ziel nach Ausbauplan: **86** Fragen als Pool mit Reserve).

Die **Vollsimulation** der schriftlichen Prüfung nutzt inzwischen **exakt 82 Core-Fragen** mit **120 Punkten** nach Sachgebiet und Punktegewichtung. Die zusätzliche Fragenbank bleibt als Pool/Reserve erhalten.

**Stand v26.2a:** **86 Fragen** im Pool, **82 Core-Fragen / 120 Punkte** in der Vollsimulation umgesetzt; `points`-Felder vollständig, Teilpunkte-Code vorhanden, Browser-Endtest bestanden. Details: `docs/EXAM_SIMULATION_AUDIT.md`, `docs/EXAM_POINTS_PLAN.md`, `docs/EXAM_CORE_SELECTION_PLAN.md`.

### Mündliche Prüfung

| Merkmal | Vorgabe |
|---------|---------|
| Dauer | etwa **15 Minuten** |
| Form | **Einzelprüfung** oder **Gruppe bis zu 5 Teilnehmer** |
| Inhalt | häufig **Praxisfälle** |
| Anforderung | **richtiges Verhalten beschreiben** und **rechtlich begründen** |

**App-Stand v25.9:** Der Bereich mündliche Prüfung ist als stabiles Trainingsmodul aufgebaut. Prüfungsbogen A, B, C, D und E sind startbar, im Browser getestet und im Auswahlfenster optisch einheitlich benannt. Jeder Bogen enthält 15 Fragen. Zusätzlich ist eine Zufallsprüfung startbar, die 15 zufällige Fragen aus den 75 mündlichen Simulationsfragen nutzt.

---

## 8. Lernstrategie-Modul (geplant)

| Aspekt | Stand v23.5.29 |
|--------|----------------|
| Dokument | `docs/LEARNING_STRATEGY_MODULE.md` – **vorhanden** |
| Inhalt | Vergessenskurve, Active Recall, Spaced Repetition, Praxisbezug |
| App-Status | **vorgemerkt**, noch **kein Code** |
| Einbau (später) | farbige Infobox / Modul in **Dashboard**, **Lernkarten** oder **Fehlertraining** |
| Geplante Version | **v24.x** oder **v25.x** |

Kernbotschaft für die App (Beispieltext):

> *Wissen bleibt nicht durch einmaliges Lesen, sondern durch Wiederholung, Anwendung und aktive Abfrage.*

**Hinweis:** Kein sofortiger Code-Task – nur Konzept und Masterlist-Verankerung.

---

## 8.1 UX- und Lernlogik-Audit (teilweise erledigt, fortlaufend)

| Aspekt | Stand |
|--------|--------|
| App-Status | **teilweise erledigt** – schriftliche Prüfung, mündliche Prüfung und Lernkarten wurden geprüft und stabilisiert |
| Aktueller Stand | v26.2a |
| Fortlaufend | Weitere UX-Verbesserungen bleiben möglich, aber keine offene Kernfunktion |

### Inhalt des Audits

1. **Ergebnisdarstellung** prüfen und vereinheitlichen.
2. **Unterschied zwischen Lernmodus und Lernkarten** klar erklären:
   - **Lernmodus** = echte Wissensabfrage mit richtig/falsch.
   - **Lernkarten** = Selbsteinschätzung mit gewusst/wiederholen/offen.
3. Optional später in der App einen kurzen Hinweis ergänzen:
   > *Lernmodus prüft Ihre Antworten. Lernkarten bewerten Ihre Selbsteinschätzung.*
4. **Themenbereich-Üben:** Nächste Frage erst nach Antwort grundsätzlich beibehalten, weil dies **Active Recall** unterstützt.
5. **Optional später prüfen:**
   - Button „Frage später beantworten“
   - Button „Überspringen und später üben“
   - offene Fragen separat speichern
   - offene Fragen gezielt nachtrainieren
6. **Ziel:** Lernlogik verständlicher machen, **ohne** die aktuelle stabile Funktion zu verändern.

**Hinweis:** Kein Sofort-Code-Task. Die Kernbereiche schriftliche Prüfung, mündliche Prüfung und Lernkarten sind stabilisiert; weiterer Feinschliff ist fortlaufend.

### UI-Hinweis: Prüfungsanalyse nach Themen

**Erledigt (v24.6f / v24.6x):** responsive stabil, Premium-Kartenlook, bessere Buttontexte. Fehlerübersicht nach Themen zusätzlich in **v24.6g** überarbeitet.

---

## 8.2 Prüfungssimulation 82/120 (Stand v26.0c)

| Aspekt | Stand v26.0c |
|--------|-------------|
| Dokument | `docs/EXAM_SIMULATION_AUDIT.md` – **vorhanden** |
| Fragenbank | **86 Fragen** in `questions.json` (Pool-Ziel erreicht) |
| `points`-Felder | **vollständig** in `questions.json` (v24.3a–i); globaler Check **82/120/38** (v24.3j) |
| Vollsimulation (Ist) | **82 feste Core-Fragen** nach `EXAM_CORE_QUESTION_IDS_V244` (v24.4b) |
| Vollsimulation (Soll) | **82 Fragen / 120 Punkte** nach Sachgebietstabelle §7 – **umgesetzt** |
| Punkteplan | `docs/EXAM_POINTS_PLAN.md` – **vorhanden** und in JSON umgesetzt |
| Core-ID-Plan | `docs/EXAM_CORE_SELECTION_PLAN.md` – **vorhanden** und in App umgesetzt (Option A) |
| Teilpunkte-Audit | **v24.3x** dokumentiert; **v24.5** Code umgesetzt |
| App-Status | Timer (120 min), Bestehen (50 %), Core-Auswahl, Teilpunkte und **Fokusnavigation offener Fragen** (v24.6b) **vorhanden** |
| Frühzeitige Abgabe | Button **„Prüfung jetzt abgeben“** – normal: Warnung bei offenen Fragen; Fokusmodus: direktes Ergebnis (offene = unbeantwortet) |
| Prüfungsanalyse UI | **erledigt** (v24.6f, v24.6x) – responsive, Premium-Look |
| Fehlerübersicht UI | **erledigt** (v24.6g) – Premium-Kartenlook, keine Überlappung |
| Fragen-/Antwort-Mix | **erledigt** (v24.6d, v24.6e) – Reihenfolge gemischt, Indizes korrekt |
| Browser-Endtest | **erledigt** – Vollsimulation 82/120 mit Teilbewertung, Core-Auswahl, Mix, Fokusnavigation und Pause/Fortsetzen geprüft bzw. dokumentiert |

### Status nach v26.0c

- **v24.6c** – Prüfung/Lernen pausieren und später fortsetzen: **erledigt**.
- **v24.6** – Vollsimulation 82/120 mit Teilbewertung im Browser testen und dokumentieren: **erledigt**.
- Künftige Änderungen am schriftlichen Prüfungsmodus müssen als Regressionstest erneut gegen 82 Fragen / 120 Punkte / 60 Punkte Bestehen / Teilpunkte / Pause-Fortsetzen geprüft werden.

---

## 8.3 Teilpunkte-Bewertung (Stand v26.0c)

| Aspekt | Stand |
|--------|--------|
| Gültig ab | **01.07.2025** – teilrichtige Antworten zählen |
| Regel | Pro **richtige Lösung** 1 Punkt; max. schriftlich **120**; Bestehen **60** (50 %) |
| `points`-Feld | **Anzahl richtiger Antworten** in `questions.json` gesetzt (1 oder 2 in der Regel) |
| App (Ist) | Teilpunkte-Logik im **Prüfungsmodus umgesetzt** (v24.5): +1 pro richtigem Kreuz, Deckelung über `points` |
| Lernmodus | Weiterhin **binär** (alles-oder-nichts) – bewusst getrennt vom Prüfungsmodus |
| Dokumentation | `docs/EXAM_SIMULATION_AUDIT.md` §10, `docs/EXAM_POINTS_PLAN.md` §10 |
| Code-Regel (Prüfung) | Single: voll/0 · Multiple: +1 pro richtigem Kreuz, falsche Zusatzkreuze zählen nicht |
| Offen | Keine offene Kernfunktion; bei späteren Code-Änderungen Regressionstest empfohlen |

### Roadmap (Teilpunkte und Vollsimulation)

| Task | Inhalt |
|------|--------|
| **v24.3x** | Teilpunkte-Bewertung **dokumentiert** |
| **v24.3a–i/j** | `points`-Felder vollständig + globaler Check **erledigt** |
| **v24.4b** | Core-Auswahl in App **erledigt** |
| **v24.5** | Teilpunkte-Logik **erledigt** |
| **v24.6** | Vollsimulation 82/120 **mit Teilbewertung** im Browser testen – **erledigt** |
| **v24.6b** | Wiederholungslogik offener Fragen + frühzeitige Abgabe – **erledigt** (§8.4) |
| **v24.6d/e** | Fragen- und Antwortreihenfolge gemischt – **erledigt** |
| **v24.6f/x/g** | Prüfungsanalyse + Fehlerübersicht UI – **erledigt** |
| **v24.6c** | Pausieren/Fortsetzen Prüfung und Lernen – **erledigt** |

---

## 8.4 Wiederholungslogik nach Prüfung (erledigt: v24.6b)

| Aspekt | Stand |
|--------|--------|
| Problem (behoben) | Wiederholungsrunden für unbeantwortete Fragen dürfen **nicht** das volle Prüfungsset durchlaufen |
| Beispiel | Nur Fragen **34, 45, 56, 60** unbeantwortet → Nachbearbeitung nur diese vier Fragen |
| Falsch (vorher) | Nach Frage 34 weiter mit **35, 36, 37** aus dem normalen Prüfungsset |
| Richtig (jetzt) | **34 → 45 → 56 → 60** – gefilterte Indexliste `examFocusQuestionIndexes` in `app.js` |
| Frühzeitige Abgabe | **„Prüfung jetzt abgeben“** jederzeit sichtbar; im Fokusmodus direkt `finishExamMode()`, sonst Warnung mit „Trotzdem abgeben“ |
| Offene bei Abgabe | Unbeantwortete Fragen werden in der Auswertung als **unbeantwortet** gezählt (0 Punkte) |
| Commit | `a169595` – v24.6b fix unanswered exam navigation and early submit |
| Status | **erledigt** – Task **v24.6b** |

---

## 8.5 Pausieren und Fortsetzen (erledigt)

| Aspekt | Stand |
|--------|--------|
| Ziel | Prüfung, Lernmodus und Lernkarten pausieren, später exakt fortsetzen |
| Umsetzung | Aktive Prüfung, aktive Lerneinheit und aktive Lernkartenrunde werden lokal gespeichert |
| Enthalten | Fragenreihenfolge, Antwortreihenfolge bzw. Kartenreihenfolge, aktuelle Position, ausgewählte Antworten/Status, Timer bei Prüfung, Modus/Sessiontyp |
| Status | **erledigt** – Prüfung/Lernmodus ab v24.6c/v24.7b, Lernkarten ab v26.1c |

---

## 9. Prüfskripte

Kategorie-Audit:

```bash
python tools/audit-categories.py
```

Preflight (Pflicht vor jedem Commit):

```bash
python tools/preflight.py
```

---

## 10. Planungsdokumente (Stand v24.6h)

| Dokument | Status |
|----------|--------|
| `docs/CURSOR_MASTER_CONTEXT_ACCAOUI.md` | Master-Kontext, Roadmap v24–v28, Prüfungsaufbau §4 |
| `docs/WRITTEN_QUESTION_STANDARD.md` | Schriftlicher Fragenstandard – **vorhanden** |
| `docs/WRITTEN_QUESTION_EXPANSION_PLAN.md` | Ausbau 51 → 86 Fragen, Prüfungsziel 82 – **vorhanden** (Pool **86** erreicht) |
| `docs/EXAM_SIMULATION_AUDIT.md` | Prüfungssimulation 82/120 – **vorhanden** (Audit v24.0, kein Code) |
| `docs/EXAM_POINTS_PLAN.md` | Punktevergabe 1/2 pro Frage, Simulationskern 82/120 – **vorhanden** (Plan v24.1, kein JSON) |
| `docs/EXAM_CORE_SELECTION_PLAN.md` | Feste 82 Core-IDs, 4 Reserve – **vorhanden** (Plan v24.2, Option A, kein Code) |
| `docs/QUESTION_DATABASE_PLAN.md` | Fragen-Datenbank, Review, Export – **vorhanden** |
| `docs/LEARNING_STRATEGY_MODULE.md` | Lernstrategie, Vergessenskurve – **vorhanden** (Konzept, kein Code) |
| `docs/SUPABASE_QUESTION_SCHEMA.md` | Supabase-Fragenmodell – **vorhanden** |
| `docs/SUPABASE_USER_PROGRESS_SCHEMA.md` | Nutzer, Kurse, Fortschritt – **vorhanden** |
| `docs/SUPABASE_IMPLEMENTATION_ROADMAP.md` | Umsetzungsreihenfolge Supabase – **vorhanden** |
| `docs/SUPABASE_PARTICIPANT_ACCESS_READINESS_TEST.md` | Lokaler Test der Teilnehmerzugangs-Readiness: lokaler Zugriff erlaubt, keine echte Teilnehmerprüfung – **vorhanden (v26.11c)** |
| `docs/SUPABASE_ADAPTER_HEALTH_STATE_TEST.md` | Lokaler Test des Adapter-Health-State: zentrale Gesamtübersicht über Config, SDK, Client, Auth und Teilnehmerzugang – **vorhanden (v26.11e)** |
| `docs/SUPABASE_APP_HEALTH_HOOK_TEST.md` | Lokaler Test des App-Health-Hooks: `app.js` liest Adapter-Health-State und stellt ihn global bereit – **vorhanden (v26.12b)** |
| `docs/SUPABASE_ACCESS_FLOW_HEALTH_TEST.md` | Lokaler Test des Access-Flows mit Adapter-Health-State: lokaler Zugriff bleibt erlaubt, kein Login-Zwang – **vorhanden (v26.12d)** |
| `docs/SUPABASE_LIVE_SWITCH_TEST.md` | Lokaler Test des Supabase-Live-Schalters: Live-Modus bleibt ohne bewussten Schalter deaktiviert, kein Client, keine Live-Verbindung – **vorhanden (v26.13b)** |
| `docs/SUPABASE_LIVE_SWITCH_DRY_RUN_TEST.md` | Dry-Run-Test des Supabase-Live-Schalters: Schalter testweise aktiv, Supabase bleibt ohne Config, SDK und Client-Erzeugung lokal blockiert – **vorhanden (v26.14a)** |
| `docs/SUPABASE_FAIL_SAFE_STATUS_TEST.md` | Lokaler Test des Supabase-Fail-Safe-Status: Normalmodus und Dry-Run geprüft, klare Sicherheitszustände, kein Client, keine Sessionprüfung – **vorhanden (v26.15b)** |
| `docs/SUPABASE_CONFIG_LOADER_BOOT_STATE_TEST.md` | Lokaler Test des Supabase-Config-Loader-Boot-State: `getBootLoadState()`, `local_config_autoload_disabled`, `loadStatus: skipped`, kein Client, keine Sessionprüfung – **vorhanden (v26.17b)** |
| `docs/SUPABASE_ADAPTER_HEALTH_BOOT_STATE_TEST.md` | Lokaler Test des Adapter-Health-Boot-State: `configLoaderBootStatus`, `configLoaderBootLoadStatus`, `isConfigLoaderBootSafe`, `isConfigLoaderAutoLoadEnabled`, kein Client, keine Sessionprüfung – **vorhanden (v26.18b)** |
| `docs/ACCAOUI_SOURCE_MATERIAL_STATUS.md` | Quellenpakete / Musterunterlagen – Status v24.5y – **vorhanden** |
| `docs/ACCAOUI_ORAL_QUESTIONS_STATUS.md` | Mündliche Prüfung / Musterfragen – Status v24.5y – **vorhanden** |
| `docs/PROJECT_MASTERLIST.md` | Diese Datei |

---

## 11. Funktionaler Teststand

| Bereich | Status |
|---------|--------|
| Schriftlicher Prüfungsmodus | **getestet** (Simulation, Statistik, Historie, Fehlertraining) |
| Mündliche Prüfung | **getestet** (Training, Simulation, Bewertung, Fehlertraining; A/B/C/D/E sichtbar, startbar und einheitlich benannt; Zufallsprüfung sichtbar und startbar; Abschluss-Audit v25.9) |
| Simulation A | **vorhanden** (15-Minuten-Bogen, 15 Fragen) |
| Simulation B | **vorhanden und startbar** (Prüfungsbogen B, 15 Fragen) |
| Simulation C | **vorhanden und startbar** (Prüfungsbogen C, 15 Fragen; v25.2a/b) |
| Simulation D | **vorhanden und startbar** (Prüfungsbogen D, 15 Fragen; v25.3a/b) |
| Simulation E | **vorhanden und startbar** (Prüfungsbogen E, 15 Fragen; v25.4a/b) |
| Lernkarten | **umgesetzt und browsergetestet** (Kategorien, Lernkartenstart, Antwort anzeigen, Gewusst/Nicht gewusst, Fehler-Lernkarten, Pause/Fortsetzen, Dashboard-Karte „Angefangene Lernkarten“; v26.1c erledigt) |
| Schriftliche Fragenbank | **86 Fragen** in `questions.json` (Pool-Ziel erreicht); Vollsimulation nutzt **82 Core-Fragen** (v24.4b) |
| Prüfungssimulation 82/120 | **umgesetzt, dokumentiert und browsergetestet** (82 Core-Fragen, 120 Punkte, 60 Punkte Bestehen, Teilpunkte, Mix, Fokusnavigation, Pause/Fortsetzen; v26.0c Browser-Endtest erledigt) |
| Lernstrategie-Modul | **geplant** – siehe `docs/LEARNING_STRATEGY_MODULE.md` |
| UX- und Lernlogik-Audit | **teilweise erledigt** – schriftliche Prüfung, mündliche Prüfung und Lernkarten wurden geprüft; weiterer Feinschliff bleibt fortlaufend |

Langfristiges Ziel mündlich: skalierbare Bogen-Auswahl A/B/C/D unter einem Hauptmodus „Prüfungssimulation“ (siehe v24 Oral Exam Cleanup).

---

## 12. Mündlicher Fehlertrainer

Führend ist:

`showOralMistakeTrainingV2340()`

Alte Funktionen werden auf den neuen Renderer umgeleitet:

1. `showOralMistakeTrainingV2324`
2. `showOralMistakeTrainingV2325`
3. `showOralMistakeTrainingV2326`

Keine weiteren Hotfixes an alten mündlichen Fehlertrainer-Renderern.

---

## 13. Werkzeuge (Entwicklungsumgebung)

Installiert (Referenz):

1. Node.js v24.16.0
2. npm 11.13.0
3. Python 3.13.3

---

## 14. Nächste sinnvolle Aufgaben

1. **Schriftliche Prüfung Regressionstest bei Änderungen** – Vollsimulation 82/120, Teilpunkte, Pause/Fortsetzen, Mix und Auswertung nach späteren Code-Änderungen erneut prüfen.
2. **Lernkarten nach größeren UI-Änderungen kurz regressionsprüfen** – Stand v26.1c ist browsergetestet.
3. **Lernstrategie-Modul** – Vergessenskurve als UI-Modul, siehe `docs/LEARNING_STRATEGY_MODULE.md` – **kein sofortiger Code-Task**.
4. **UX- und Lernlogik weiter verfeinern** – Ergebnisdarstellung, Lernmodus vs. Lernkarten, Active Recall, siehe §8.1.
5. **Später Oral Exam Cleanup** – Patch-Schichten reduzieren, einheitliche Bogenlogik A/B/C/D/E/Zufall.
6. **Spätere SQL-Planung** – Phase 2 laut `docs/SUPABASE_IMPLEMENTATION_ROADMAP.md`.
7. **Später Datenschutz / Rechtstexte** – Impressum, Datenschutz, Nutzungsbedingungen.
8. **Supabase / Login als nächster Hauptblock** – Auth, Kurse, Teilnehmerzugang, Ablaufdatum und Fortschritt pro `user_id`; Plan v26.3a, Login-UI-Konzept v26.3c, Auth-Einstiegspunkt-Audit v26.3e, lokales Auth-Guard-Gerüst v26.4a, lokaler Testmodus v26.4c, Auth-Hinweisdesign v26.4e, Supabase-Sicherheitsplan v26.5a, Config-Platzhalter v26.5c, Config-Ladeweg-Audit v26.5e, Config-State-Check v26.6a, optionaler Config-Loader v26.6c, lokaler Loader-Test v26.6e, Client-Adapter-Plan v26.7a, Adapter-Gerüst v26.7c, Adapter-Test v26.7e, SDK-Ladeweg-Plan v26.8a, SDK-Status im Adapter v26.8c und SDK-Status-Test v26.8e, Client-Readiness v26.9a und Client-Readiness-Test v26.9c, Auth-Readiness v26.10a, Auth-Readiness-Test v26.10c und Teilnehmerzugangs-Readiness v26.11a vorhanden.
9. **Quellenpakete und mündliche Musterfragen gezielt auswerten** – nicht vollständig in neuen Chat laden; siehe `docs/ACCAOUI_SOURCE_MATERIAL_STATUS.md` und `docs/ACCAOUI_ORAL_QUESTIONS_STATUS.md`.

**Erledigt:** v24.5 (Teilpunkte); v24.6b (Wiederholung/offene Fragen); v24.6c (Pause/Fortsetzen); v24.6d/e (Mix Fragen/Antworten); v24.6f/x (Prüfungsanalyse UI); v24.6g (Fehlerübersicht UI); v25.9 (mündliche Prüfung Abschluss-Audit); v26.0a (schriftliche Prüfung Dokumentations-Audit); v26.0b (Live-Code-Audit); v26.0c (Browser-Endtest schriftliche Vollsimulation); v26.1c (Lernkarten pausieren/fortsetzen + Premium-Leiste); v26.1d (Masterliste aktualisiert); v26.2a (Masterliste-Altlasten bereinigt); v26.3a (Supabase Login-Plan); v26.3b (Masterliste Supabase/Login aktualisiert); v26.3c (Login-UI-Konzept); v26.3d (Masterliste Login-UI aktualisiert); v26.3e (Auth-Einstiegspunkt-Audit); v26.3f (Masterliste Auth-Audit aktualisiert); v26.4a (lokales Auth-Guard-Gerüst); v26.4b (Masterliste Auth-Guard aktualisiert); v26.4c (lokaler Auth-Guard-Testmodus); v26.4d (Masterliste Auth-Testmodus aktualisiert); v26.4e (Auth-Hinweisdesign); v26.4f (Masterliste Auth-Hinweisdesign aktualisiert); v26.5a (Supabase-Konfigurations- und Sicherheitsplan); v26.5b (Masterliste Supabase-Sicherheitsplan aktualisiert); v26.5c (Supabase-Config-Platzhalter); v26.5d (Masterliste Config-Platzhalter aktualisiert); v26.5e (Supabase-Config-Ladeweg-Audit); v26.5f (Masterliste Config-Ladeweg aktualisiert); v26.6a (Supabase-Config-State-Check); v26.6b (Masterliste Config-State aktualisiert); v26.6c (optionaler lokaler Config-Loader); v26.6d (Masterliste Config-Loader aktualisiert); v26.6e (lokaler Config-Loader-Test); v26.6f (Masterliste Config-Loader-Test aktualisiert); v26.7a (Supabase-Client-Adapter-Plan); v26.7b (Masterliste Client-Adapter aktualisiert); v26.7c (Supabase-Adapter-Gerüst ohne SDK); v26.7d (Masterliste Adapter-Gerüst aktualisiert); v26.7e (Supabase-Adapter-Test); v26.7f (Masterliste Adapter-Test aktualisiert); v26.8a (Supabase-SDK-Ladeweg-Plan); v26.8b (Masterliste SDK-Ladeweg aktualisiert); v26.8c (SDK-Status im Adapter); v26.8d (Masterliste SDK-Status aktualisiert); v26.8e (SDK-Status-Test); v26.8f (Masterliste SDK-Status-Test aktualisiert); v26.9a (Client-Readiness im Adapter); v26.9b (Masterliste Client-Readiness aktualisiert); v26.9c (Client-Readiness-Test); v26.9d (Masterliste Client-Readiness-Test aktualisiert); v26.10a (Auth-Readiness im Adapter); v26.10b (Masterliste Auth-Readiness aktualisiert); v26.10c (Auth-Readiness-Test); v26.10d (Masterliste Auth-Readiness-Test aktualisiert); v26.11a (Teilnehmerzugangs-Readiness im Adapter); v26.11b (Masterliste Teilnehmerzugangs-Readiness aktualisiert).

Optional parallel: Projektstruktur gegen alte Kopien prüfen; mündliche Prüfung später als erweiterter Prüfermodus.

---

## 15. Start in neuem Chat

Zuerst nennen:

```txt
docs/PROJECT_MASTERLIST.md
docs/CURSOR_MASTER_CONTEXT_ACCAOUI.md
docs/EXAM_SIMULATION_AUDIT.md
docs/EXAM_POINTS_PLAN.md
docs/EXAM_CORE_SELECTION_PLAN.md
```

Dann **NUR IN GIT BASH AUSFÜHREN**:

```bash
git status
git pull --ff-only
git log -1 --oneline
python tools/preflight.py
```

**Hinweis:** Alte Chat-Uploads und Prüfungsmuster sind **nicht automatisch** Arbeitsgrundlage im neuen Chat. Bei Bedarf Prüfungsmuster erneut hochladen oder im Repo dokumentieren.

Keine Änderung ohne sauberen Arbeitsstand.

v23.5.12
Lernkarten funktional getestet und Layout-Fix umgesetzt. Lange Fragen, Antwortansicht, Erklärungen, Buttons, Gewusst/Nicht gewusst und Wiederholen-Karten werden sauber dargestellt.
