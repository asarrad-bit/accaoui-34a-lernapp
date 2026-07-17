# Accaoui §34a Lern-App – Projekt-Masterliste

Stand: v27.28a
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
- `tools/accaoui-helper.py`
- `tools/audit-categories.py`
- `.nojekyll` (GitHub Pages: Jekyll deaktiviert, statische App bleibt direkt auslieferbar)

---

## 5. Aktueller Versionsstand (bis v26.75c)

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
| v26.19a | Supabase-Safety-Summary ergänzt: `getSupabaseSafetySummary()`, `safetySummaryStatus`, `isSafeLocalMode`, `blockingReasons`, `nextRequiredSteps`; zentraler Sicherheitsstatus bestätigt lokalen sicheren Modus – **erledigt** |
| v26.19b | Supabase-Safety-Summary-Test dokumentiert: Summary sichtbar, Supabase nicht live, kein Client, keine Sessionprüfung, lokaler Zugriff erlaubt – **erledigt** |
| v26.19c | Masterliste um Supabase-Safety-Summary und Testdokument ergänzt – **erledigt** |
| v26.20a | Teilnehmer-Session-State vorbereitet: `getParticipantSessionState()`, `local_session_stub`, keine Sessionpflicht, keine Sessionprüfung, lokaler Zugriff bleibt erlaubt – **erledigt** |
| v26.20b | Teilnehmer-Session-State-Test dokumentiert: Session-State sichtbar, `isSessionRequired=false`, `canCheckSession=false`, lokaler Zugriff weiterhin erlaubt – **erledigt** |
| v26.20c | Masterliste um Teilnehmer-Session-State und Testdokument ergänzt – **erledigt** |
| v26.21a | Teilnehmer-Profil-State vorbereitet: `getParticipantProfileState()`, `local_profile_stub`, kein Profilabruf, keine Profilpflicht, lokaler Zugriff bleibt erlaubt – **erledigt** |
| v26.21b | Teilnehmer-Profil-State-Test dokumentiert: Profil-State sichtbar, `isProfileRequired=false`, `canLoadProfile=false`, kein Profilabruf, lokaler Zugriff weiterhin erlaubt – **erledigt** |
| v26.21c | Masterliste um Teilnehmer-Profil-State und Testdokument ergänzt – **erledigt** |
| v26.22a | Teilnehmer-Kursstatus-State vorbereitet: `getParticipantCourseState()`, `local_course_stub`, kein Kursabruf, keine Kursstatus-Pflicht, kein Ablaufstatus aktiv, lokaler Zugriff bleibt erlaubt – **erledigt** |
| v26.22b | Teilnehmer-Kursstatus-State-Test dokumentiert: Kursstatus-State sichtbar, `isCourseRequired=false`, `canLoadCourse=false`, `isCourseExpired=false`, lokaler Zugriff weiterhin erlaubt – **erledigt** |
| v26.22c | Masterliste um Teilnehmer-Kursstatus-State und Testdokument ergänzt – **erledigt** |
| v26.23a | Teilnehmer-Zugriffsentscheidung zentralisiert: `getParticipantAccessDecisionState()`, `local_access_decision_allowed`, kein Login-Zwang, keine Sperre, lokaler Zugriff bleibt erlaubt – **erledigt** |
| v26.23b | Teilnehmer-Zugriffsentscheidung-Test dokumentiert: Access-Decision sichtbar, Zugriff lokal erlaubt, Login nicht erforderlich, keine Blocking-Reasons – **erledigt** |
| v26.23c | Masterliste um Teilnehmer-Zugriffsentscheidung und Testdokument ergänzt – **erledigt** |
| v26.24a | Login-Gate-Status vorbereitet: `getLoginGateState()`, `local_login_gate_disabled`, Gate deaktiviert, kein Login-Zwang, keine Sperre, lokaler Zugriff bleibt erlaubt – **erledigt** |
| v26.24b | Login-Gate-Status-Test dokumentiert: Gate sichtbar, `isGateEnabled=false`, `isLoginRequired=false`, `canBlockAccess=false`, lokaler Zugriff weiterhin erlaubt – **erledigt** |
| v26.24c | Masterliste um Login-Gate-Status und Testdokument ergänzt – **erledigt** |
| v26.25a | Login-Gate-UI-State vorbereitet: `getLoginGateUiState()`, `local_login_gate_ui_hidden`, keine sichtbare Login-Maske, kein UI-Blocker, lokaler Zugriff bleibt erlaubt – **erledigt** |
| v26.25b | Login-Gate-UI-State-Test dokumentiert: UI-State sichtbar, `isVisible=false`, `canRender=false`, `canBlockAccess=false`, kein Login-Zwang – **erledigt** |
| v26.25c | Masterliste um Login-Gate-UI-State und Testdokument ergänzt – **erledigt** |
| v26.26a | Login-Formular-State vorbereitet: `getLoginFormState()`, `local_login_form_disabled`, Formular unsichtbar, keine Eingabeprüfung, keine Authentifizierung, lokaler Zugriff bleibt erlaubt – **erledigt** |
| v26.26b | Login-Formular-State-Test dokumentiert: Formular-State sichtbar, `canSubmit=false`, `canValidateInput=false`, `canAuthenticate=false`, kein Login-Zwang – **erledigt** |
| v26.26c | Masterliste um Login-Formular-State und Testdokument ergänzt – **erledigt** |
| v26.27a | Login-Fehler-State vorbereitet: `getLoginErrorState()`, `local_login_error_none`, kein aktiver Fehler, keine Fehlermeldung, keine Authentifizierung, lokaler Zugriff bleibt erlaubt – **erledigt** |
| v26.27b | Login-Fehler-State-Test dokumentiert: Fehler-State sichtbar, `hasError=false`, `canShowError=false`, `errorCode=null`, kein Login-Zwang – **erledigt** |
| v26.27c | Masterliste um Login-Fehler-State und Testdokument ergänzt – **erledigt** |
| v26.28a | Login-Erfolg-State vorbereitet: `getLoginSuccessState()`, `local_login_success_none`, kein aktiver Login-Erfolg, keine Session, keine Weiterleitung, lokaler Zugriff bleibt erlaubt – **erledigt** |
| v26.28b | Login-Erfolg-State-Test dokumentiert: Erfolg-State sichtbar, `hasSuccess=false`, `hasSession=false`, `canFinalizeLogin=false`, keine Weiterleitung – **erledigt** |
| v26.28c | Masterliste um Login-Erfolg-State und Testdokument ergänzt – **erledigt** |
| v26.29a | Login-Abmelde-State vorbereitet: `getLogoutState()`, `local_logout_disabled`, keine aktive Session, kein Logout, keine Session-Löschung, lokaler Zugriff bleibt erlaubt – **erledigt** |
| v26.29b | Login-Abmelde-State-Test dokumentiert: Logout-State sichtbar, `isAvailable=false`, `canLogout=false`, `canClearSession=false`, keine aktive Session – **erledigt** |
| v26.29c | Masterliste um Login-Abmelde-State und Testdokument ergänzt – **erledigt** |
| v26.30a | Teilnehmer-Dashboard-Auth-State vorbereitet: `getParticipantDashboardAuthState()`, `local_dashboard_auth_disabled`, kein sichtbarer Auth-Bereich, kein Login-Zwang, keine Dashboard-Sperre, lokaler Zugriff bleibt erlaubt – **erledigt** |
| v26.30b | Teilnehmer-Dashboard-Auth-State-Test dokumentiert: Dashboard-Auth-State sichtbar, `isVisible=false`, `canRender=false`, `isAuthRequired=false`, `canBlockDashboardAccess=false` – **erledigt** |
| v26.30c | Masterliste um Teilnehmer-Dashboard-Auth-State und Testdokument ergänzt – **erledigt** |
| v26.31a | Teilnehmer-Dashboard-Kurszugriff-State vorbereitet: `getParticipantDashboardCourseAccessState()`, `local_dashboard_course_access_allowed`, keine Kursprüfung, keine Kurs-Sperre, kein Kurs-Lock, lokaler Zugriff bleibt erlaubt – **erledigt** |
| v26.31b | Teilnehmer-Dashboard-Kurszugriff-State-Test dokumentiert: Kurszugriff-State sichtbar, `canCheckCourseAccess=false`, `canBlockCourseAccess=false`, `canShowCourseLock=false` – **erledigt** |
| v26.31c | Masterliste um Teilnehmer-Dashboard-Kurszugriff-State und Testdokument ergänzt – **erledigt** |
| v26.32a | Teilnehmer-Dashboard-Ablaufdatum-State vorbereitet: `getParticipantDashboardExpiryState()`, `local_dashboard_expiry_check_disabled`, keine Ablaufdatum-Prüfung, kein Ablaufdatum, keine Ablauf-Warnung, lokaler Zugriff bleibt erlaubt – **erledigt** |
| v26.32b | Teilnehmer-Dashboard-Ablaufdatum-State-Test dokumentiert: Ablaufdatum-State sichtbar, `canCheckExpiry=false`, `canBlockOnExpiry=false`, `isExpired=false`, keine Sperre – **erledigt** |
| v26.32c | Masterliste um Teilnehmer-Dashboard-Ablaufdatum-State und Testdokument ergänzt – **erledigt** |
| v26.33a | Teilnehmer-Dashboard-Zugriffsentscheidung-State vorbereitet: `getParticipantDashboardAccessDecisionState()`, `local_dashboard_access_decision_allowed`, Dashboard-Zugriff lokal erlaubt, keine Auth-Sperre, keine Kurs-Sperre, keine Ablaufdatum-Sperre – **erledigt** |
| v26.33b | Teilnehmer-Dashboard-Zugriffsentscheidung-State-Test dokumentiert: Entscheidung verfügbar, `isDashboardAccessAllowed=true`, `canBlockDashboardAccess=false`, kein Blockiergrund – **erledigt** |
| v26.33c | Masterliste um Teilnehmer-Dashboard-Zugriffsentscheidung-State und Testdokument ergänzt – **erledigt** |
| v26.34a | Teilnehmer-Dashboard-Readiness-State vorbereitet: `getParticipantDashboardReadinessState()`, `local_dashboard_readiness_ready`, Dashboard lokal bereit, renderbar, startbar, kein Login-Zwang, keine Sperre – **erledigt** |
| v26.34b | Teilnehmer-Dashboard-Readiness-State-Test dokumentiert: Readiness verfügbar, `isReady=true`, `canRenderDashboard=true`, `canStartLocalDashboard=true`, nicht blockierend – **erledigt** |
| v26.34c | Masterliste um Teilnehmer-Dashboard-Readiness-State und Testdokument ergänzt – **erledigt** |
| v26.35a | Teilnehmer-Dashboard-Status-Badge-State vorbereitet: `getParticipantDashboardStatusBadgeState()`, `local_dashboard_status_badge_hidden`, Badge-State verfügbar, Badge lokal verborgen, kein UI-Blocker, Dashboard bleibt lokal bereit – **erledigt** |
| v26.35b | Teilnehmer-Dashboard-Status-Badge-State-Test dokumentiert: Badge-State verfügbar, `isVisible=false`, `canRender=false`, `canBlockDashboardAccess=false`, kein Login-Zwang – **erledigt** |
| v26.35c | Masterliste um Teilnehmer-Dashboard-Status-Badge-State und Testdokument ergänzt – **erledigt** |
| v26.36a | Teilnehmer-Dashboard-Hinweisbanner-State vorbereitet: `getParticipantDashboardNoticeBannerState()`, `local_dashboard_notice_banner_hidden`, Banner-State verfügbar, Banner lokal verborgen, nicht renderbar, kein UI-Blocker – **erledigt** |
| v26.36b | Teilnehmer-Dashboard-Hinweisbanner-State-Test dokumentiert: Banner-State verfügbar, `isVisible=false`, `canRender=false`, `canDismiss=false`, `canBlockDashboardAccess=false` – **erledigt** |
| v26.36c | Masterliste um Teilnehmer-Dashboard-Hinweisbanner-State und Testdokument ergänzt – **erledigt** |
| v26.37a | Teilnehmer-Dashboard-Profilkopf-State vorbereitet: `getParticipantDashboardProfileHeaderState()`, `local_dashboard_profile_header_hidden`, Profilkopf verfügbar, lokal verborgen, keine Teilnehmerdaten sichtbar, kein UI-Blocker – **erledigt** |
| v26.37b | Teilnehmer-Dashboard-Profilkopf-State-Test dokumentiert: Profilkopf-State verfügbar, `isVisible=false`, `canRender=false`, `canShowParticipantIdentity=false`, `canShowCourseInfo=false` – **erledigt** |
| v26.37c | Masterliste um Teilnehmer-Dashboard-Profilkopf-State und Testdokument ergänzt – **erledigt** |
| v26.38a | Teilnehmer-Dashboard-Kurskarte-State vorbereitet: `getParticipantDashboardCourseCardState()`, `local_dashboard_course_card_hidden`, Kurskarte verfügbar, lokal verborgen, keine Kursdaten sichtbar, kein UI-Blocker – **erledigt** |
| v26.38b | Teilnehmer-Dashboard-Kurskarte-State-Test dokumentiert: Kurskarte-State verfügbar, `isVisible=false`, `canRender=false`, `canShowCourseProgress=false`, nicht blockierend – **erledigt** |
| v26.38c | Masterliste um Teilnehmer-Dashboard-Kurskarte-State und Testdokument ergänzt – **erledigt** |
| v26.39a | Teilnehmer-Dashboard-Fortschritt-State vorbereitet: `getParticipantDashboardProgressState()`, `local_dashboard_progress_hidden`, Fortschritt verfügbar, lokal verborgen, keine Fortschrittsdaten sichtbar, kein UI-Blocker – **erledigt** |
| v26.39b | Teilnehmer-Dashboard-Fortschritt-State-Test dokumentiert: Fortschritt-State verfügbar, `isVisible=false`, `canRender=false`, `canCalculateProgress=false`, keine Fortschrittsdaten – **erledigt** |
| v26.39c | Masterliste um Teilnehmer-Dashboard-Fortschritt-State und Testdokument ergänzt – **erledigt** |
| v26.40a | Teilnehmer-Dashboard-Aktivitätsliste-State vorbereitet: `getParticipantDashboardActivityListState()`, `local_dashboard_activity_list_hidden`, Aktivitätsliste verfügbar, lokal verborgen, keine Aktivitätsdaten sichtbar, kein UI-Blocker – **erledigt** |
| v26.40b | Teilnehmer-Dashboard-Aktivitätsliste-State-Test dokumentiert: Aktivitätsliste-State verfügbar, `isVisible=false`, `canRender=false`, `canLoadActivities=false`, keine Aktivitätsdaten – **erledigt** |
| v26.40c | Masterliste um Teilnehmer-Dashboard-Aktivitätsliste-State und Testdokument ergänzt – **erledigt** |
| v26.41a | Teilnehmer-Dashboard-Empfehlungen-State vorbereitet: `getParticipantDashboardRecommendationsState()`, `local_dashboard_recommendations_hidden`, Empfehlungen verfügbar, lokal verborgen, keine Empfehlungsdaten sichtbar, kein UI-Blocker – **erledigt** |
| v26.41b | Teilnehmer-Dashboard-Empfehlungen-State-Test dokumentiert: Empfehlungen-State verfügbar, `isVisible=false`, `canRender=false`, `canLoadRecommendations=false`, keine Empfehlungsdaten – **erledigt** |
| v26.41c | Masterliste um Teilnehmer-Dashboard-Empfehlungen-State und Testdokument ergänzt – **erledigt** |
| v26.42a | Teilnehmer-Dashboard-Prüfungsstatus-State vorbereitet: `getParticipantDashboardExamStatusState()`, `local_dashboard_exam_status_hidden`, Prüfungsstatus verfügbar, lokal verborgen, keine Prüfungsdaten sichtbar, kein UI-Blocker – **erledigt** |
| v26.42b | Teilnehmer-Dashboard-Prüfungsstatus-State-Test dokumentiert: Prüfungsstatus-State verfügbar, `isVisible=false`, `canRender=false`, `canLoadExamStatus=false`, keine Prüfungsdaten – **erledigt** |
| v26.42c | Masterliste um Teilnehmer-Dashboard-Prüfungsstatus-State und Testdokument ergänzt – **erledigt** |
| v26.43a | Teilnehmer-Dashboard-Zertifikat-State vorbereitet: `getParticipantDashboardCertificateState()`, `local_dashboard_certificate_hidden`, Zertifikat verfügbar, lokal verborgen, keine Zertifikatsdaten sichtbar, kein Download aktiv – **erledigt** |
| v26.43b | Teilnehmer-Dashboard-Zertifikat-State-Test dokumentiert: Zertifikat-State verfügbar, `isVisible=false`, `canRender=false`, `canLoadCertificate=false`, `canDownloadCertificate=false` – **erledigt** |
| v26.43c | Masterliste um Teilnehmer-Dashboard-Zertifikat-State und Testdokument ergänzt – **erledigt** |
| v26.44a | Teilnehmer-Dashboard-Dokumente-State vorbereitet: `getParticipantDashboardDocumentsState()`, `local_dashboard_documents_hidden`, Dokumente verfügbar, lokal verborgen, keine Dokumentdaten sichtbar, kein Download aktiv – **erledigt** |
| v26.44b | Teilnehmer-Dashboard-Dokumente-State-Test dokumentiert: Dokumente-State verfügbar, `isVisible=false`, `canRender=false`, `canLoadDocuments=false`, `canDownloadDocuments=false` – **erledigt** |
| v26.44c | Masterliste um Teilnehmer-Dashboard-Dokumente-State und Testdokument ergänzt – **erledigt** |
| v26.45a | Teilnehmer-Dashboard-Nachrichten-State vorbereitet: `getParticipantDashboardMessagesState()`, `local_dashboard_messages_hidden`, Nachrichten verfügbar, lokal verborgen, keine Nachrichtendaten sichtbar, kein Senden aktiv – **erledigt** |
| v26.45b | Teilnehmer-Dashboard-Nachrichten-State-Test dokumentiert: Nachrichten-State verfügbar, `isVisible=false`, `canRender=false`, `canLoadMessages=false`, `canSendMessage=false` – **erledigt** |
| v26.45c | Masterliste um Teilnehmer-Dashboard-Nachrichten-State und Testdokument ergänzt – **erledigt** |
| v26.53a | Teilnehmer-Dashboard-Kursmaterial-State vorbereitet: `getParticipantDashboardCourseMaterialsState()`, `local_dashboard_course_materials_hidden`, Kursmaterial verfügbar, lokal verborgen, keine Kursmaterial-Daten sichtbar, kein Öffnen, kein Download, kein Gelesen-Status aktiv – **erledigt** |
| v26.53b | Teilnehmer-Dashboard-Kursmaterial-State-Test dokumentiert: Kursmaterial-State verfügbar, `isVisible=false`, `canRender=false`, `canLoadCourseMaterials=false`, `canOpenCourseMaterial=false`, `canDownloadCourseMaterial=false` – **erledigt** |
| v26.53c | Masterliste um Teilnehmer-Dashboard-Kursmaterial-State und Testdokument ergänzt – **erledigt** |
| v26.54a | Teilnehmer-Dashboard-Lernfortschritt-Details-State vorbereitet: `getParticipantDashboardLearningProgressDetailsState()`, `local_dashboard_learning_progress_details_hidden`, Lernfortschritt-Details verfügbar, lokal verborgen, keine Detaildaten sichtbar, keine Prozentanzeige, kein aktuelles Lernthema sichtbar – **erledigt** |
| v26.54b | Teilnehmer-Dashboard-Lernfortschritt-Details-State-Test dokumentiert: Lernfortschritt-Details-State verfügbar, `isVisible=false`, `canRender=false`, `canLoadLearningProgressDetails=false`, `canShowLearningProgressPercent=false`, `canShowCurrentLearningTopic=false` – **erledigt** |
| v26.54c | Masterliste um Teilnehmer-Dashboard-Lernfortschritt-Details-State und Testdokument ergänzt – **erledigt** |
| v26.55a | Teilnehmer-Dashboard-Fehlertraining-Details-State vorbereitet: `getParticipantDashboardMistakeTrainingDetailsState()`, `local_dashboard_mistake_training_details_hidden`, Fehlertraining-Details verfügbar, lokal verborgen, keine Detaildaten sichtbar, keine offenen Fehler sichtbar, keine Wiederholungs-Empfehlung sichtbar – **erledigt** |
| v26.55b | Teilnehmer-Dashboard-Fehlertraining-Details-State-Test dokumentiert: Fehlertraining-Details-State verfügbar, `isVisible=false`, `canRender=false`, `canLoadMistakeTrainingDetails=false`, `canStartMistakeReview=false`, `canShowRecommendedReviewMode=false` – **erledigt** |
| v26.55c | Masterliste um Teilnehmer-Dashboard-Fehlertraining-Details-State und Testdokument ergänzt – **erledigt** |
| v26.56a | Teilnehmer-Dashboard-Prüfungssimulation-Details-State vorbereitet: `getParticipantDashboardExamSimulationDetailsState()`, `local_dashboard_exam_simulation_details_hidden`, Prüfungssimulation-Details verfügbar, lokal verborgen, keine Simulationsdaten sichtbar, kein Score sichtbar, keine Simulationsempfehlung sichtbar – **erledigt** |
| v26.56b | Teilnehmer-Dashboard-Prüfungssimulation-Details-State-Test dokumentiert: Prüfungssimulation-Details-State verfügbar, `isVisible=false`, `canRender=false`, `canLoadExamSimulationDetails=false`, `canStartExamSimulationReview=false`, `canShowExamSimulationRecommendation=false` – **erledigt** |
| v26.56c | Masterliste um Teilnehmer-Dashboard-Prüfungssimulation-Details-State und Testdokument ergänzt – **erledigt** |
| v26.57a | Teilnehmer-Dashboard-Mündliche-Prüfung-Details-State vorbereitet: `getParticipantDashboardOralExamDetailsState()`, `local_dashboard_oral_exam_details_hidden`, mündliche Prüfung verfügbar, lokal verborgen, keine mündlichen Prüfungsdaten sichtbar, keine offenen Fragen sichtbar, keine Übungsempfehlung sichtbar – **erledigt** |
| v26.57b | Teilnehmer-Dashboard-Mündliche-Prüfung-Details-State-Test dokumentiert: Mündliche-Prüfung-Details-State verfügbar, `isVisible=false`, `canRender=false`, `canLoadOralExamDetails=false`, `canStartOralExamPracticeReview=false`, `canShowOralPracticeRecommendation=false` – **erledigt** |
| v26.57c | Masterliste um Teilnehmer-Dashboard-Mündliche-Prüfung-Details-State und Testdokument ergänzt – **erledigt** |
| v26.58a | Teilnehmer-Dashboard-Lernkarten-Details-State vorbereitet: `getParticipantDashboardFlashcardsDetailsState()`, `local_dashboard_flashcards_details_hidden`, Lernkarten verfügbar, lokal verborgen, keine Lernkarten-Daten sichtbar, keine fälligen Karten sichtbar, keine Lernkarten-Empfehlung sichtbar – **erledigt** |
| v26.58b | Teilnehmer-Dashboard-Lernkarten-Details-State-Test dokumentiert: Lernkarten-Details-State verfügbar, `isVisible=false`, `canRender=false`, `canLoadFlashcardsDetails=false`, `canStartFlashcardPracticeReview=false`, `canShowFlashcardPracticeRecommendation=false` – **erledigt** |
| v26.58c | Masterliste um Teilnehmer-Dashboard-Lernkarten-Details-State und Testdokument ergänzt – **erledigt** |
| v26.59a | Teilnehmer-Dashboard-Musterfragen-Details-State vorbereitet: `getParticipantDashboardSampleQuestionsDetailsState()`, `local_dashboard_sample_questions_details_hidden`, Musterfragen verfügbar, lokal verborgen, keine Musterfragen-Daten sichtbar, keine offenen Fragen sichtbar, keine Musterfragen-Empfehlung sichtbar – **erledigt** |
| v26.59b | Teilnehmer-Dashboard-Musterfragen-Details-State-Test dokumentiert: Musterfragen-Details-State verfügbar, `isVisible=false`, `canRender=false`, `canLoadSampleQuestionsDetails=false`, `canStartSampleQuestionPracticeReview=false`, `canShowSampleQuestionPracticeRecommendation=false` – **erledigt** |
| v26.59c | Masterliste um Teilnehmer-Dashboard-Musterfragen-Details-State und Testdokument ergänzt – **erledigt** |
| v26.60a | Teilnehmer-Dashboard-Prüfungshistorie-State vorbereitet: `getParticipantDashboardExamHistoryState()`, `local_dashboard_exam_history_hidden`, Prüfungshistorie verfügbar, lokal verborgen, keine Prüfungsdaten sichtbar, kein Score-Verlauf, kein Bestwert, keine Review-Funktion – **erledigt** |
| v26.60b | Teilnehmer-Dashboard-Prüfungshistorie-State-Test dokumentiert: Prüfungshistorie-State verfügbar, `isVisible=false`, `canRender=false`, `canLoadExamHistory=false`, `canOpenExamHistoryAttemptReview=false`, `canShowExamHistoryScoreTrend=false` – **erledigt** |
| v26.60c | Masterliste um Teilnehmer-Dashboard-Prüfungshistorie-State und Testdokument ergänzt – **erledigt** |
| v26.61a | Teilnehmer-Dashboard-Zertifikats-Historie-State vorbereitet: `getParticipantDashboardCertificateHistoryState()`, `local_dashboard_certificate_history_hidden`, Zertifikats-Historie verfügbar, lokal verborgen, keine Zertifikatsdaten sichtbar, kein Ausstellungsstatus, keine Download-Aktion, kein Öffnen einzelner Einträge – **erledigt** |
| v26.61b | Teilnehmer-Dashboard-Zertifikats-Historie-State-Test dokumentiert: Zertifikats-Historie-State verfügbar, `isVisible=false`, `canRender=false`, `canLoadCertificateHistory=false`, `canDownloadCertificateFromHistory=false`, `canOpenCertificateHistoryEntry=false` – **erledigt** |
| v26.61c | Masterliste um Teilnehmer-Dashboard-Zertifikats-Historie-State und Testdokument ergänzt – **erledigt** |
| v26.62a | Teilnehmer-Dashboard-Zertifikats-Download-State vorbereitet: `getParticipantDashboardCertificateDownloadState()`, `local_dashboard_certificate_download_hidden`, Zertifikats-Download verfügbar, lokal verborgen, keine Download-Daten sichtbar, kein Download-Button, kein Download-Start, keine Vorschau, kein Tracking – **erledigt** |
| v26.62b | Teilnehmer-Dashboard-Zertifikats-, keine Download-Daten sichtbar, kein Download-Button, kein Download-Start, keine Vorschau, kein Tracking – **erledigt** |
| v26.62b |Download-State-Test dokumentiert: Zertifikats-Download-State verfügbar, `isVisible=false`, `canRender=false`, `canLoadCertificateDownload=false`, `canStartCertificateDownload=false`, `canOpenCertificateDownloadPreview=false` – **erledigt** |
| v26.62c | Masterliste um Teilnehmer-Dashboard-Zertifikats-Download-State und Testdokument ergänzt – **erledigt** |
| v26.63a | Teilnehmer-Dashboard-Zertifikats-Vorschau-State vorbereitet: `getParticipantDashboardCertificatePreviewState()`, `local_dashboard_certificate_preview_hidden`, Zertifikats-Vorschau verfügbar, lokal verborgen, keine Vorschau-Daten sichtbar, kein Vorschau-Button, kein Vorschau-Frame, kein Aktualisieren, kein Drucken – **erledigt** |
| v26.63b | Teilnehmer-Dashboard-Zertifikats-Vorschau-State-Test dokumentiert: Zertifikats-Vorschau-State verfügbar, `isVisible=false`, `canRender=false`, `canLoadCertificatePreview=false`, `canOpenCertificatePreview=false`, `canPrintCertificatePreview=false` – **erledigt** |
| v26.63c | Masterliste um Teilnehmer-Dashboard-Zertifikats-Vorschau-State und Testdokument ergänzt – **erledigt** |
| v26.64a | Lokaler Projekt-Helfer `tools/accaoui-helper.py` ergänzt: zeigt Masterlisten-Stand und führt Preflight, `git diff --check` und `git status --short` kompakt aus – **erledigt** |
| v26.64b | Masterliste um lokalen Projekt-Helfer ergänzt – **erledigt** |
| v26.64c | Preflight robuster gemacht: Kategorien-Audit nutzt denselben Python-Interpreter wie der gestartete Preflight (`sys.executable`) – **erledigt** |
| v26.65a | Teilnehmer-Dashboard-Zertifikats-Druck-State vorbereitet: `getParticipantDashboardCertificatePrintState()`, `local_dashboard_certificate_print_hidden`, Druck-State verfügbar, lokal verborgen, kein Druck-Start, kein Druckdialog, kein UI-Blocker – **erledigt** |
| v26.65b | Teilnehmer-Dashboard-Zertifikats-Druck-State-Test dokumentiert: Druck-State verfügbar, `isVisible=false`, `canRender=false`, `canStartCertificatePrint=false`, lokaler Zugriff bleibt erlaubt – **erledigt** |
| v26.65c | Masterliste um Teilnehmer-Dashboard-Zertifikats-Druck-State und Testdokument ergänzt – **erledigt** |
| v26.66a | Teilnehmer-Dashboard-Zertifikats-Teilen-State vorbereitet: `getParticipantDashboardCertificateShareState()`, `local_dashboard_certificate_share_hidden`, Teilen-State verfügbar, lokal verborgen, kein Teilen-Link, keine Teilen-E-Mail, kein UI-Blocker – **erledigt** |
| v26.66b | Teilnehmer-Dashboard-Zertifikats-Teilen-State-Test dokumentiert: Teilen-State verfügbar, `isVisible=false`, `canRender=false`, `canCreateCertificateShareLink=false`, `canSendCertificateShareEmail=false`, lokaler Zugriff bleibt erlaubt – **erledigt** |
| v26.66c | Masterliste um Teilnehmer-Dashboard-Zertifikats-Teilen-State und Testdokument ergänzt – **erledigt** |
| v26.67a | Teilnehmer-Dashboard-Zertifikats-Verifizierungs-State vorbereitet: `getParticipantDashboardCertificateVerificationState()`, `local_dashboard_certificate_verification_hidden`, Verifizierungs-State verfügbar, lokal verborgen, kein QR-Code, keine Prüfseite, keine Online-Verifizierung, kein UI-Blocker – **erledigt** |
| v26.67b | Teilnehmer-Dashboard-Zertifikats-Verifizierungs-State-Test dokumentiert: Verifizierungs-State verfügbar, `isVisible=false`, `canRender=false`, `canCreateCertificateVerificationCode=false`, `canOpenCertificateVerificationPage=false`, `canVerifyCertificateOnline=false`, lokaler Zugriff bleibt erlaubt – **erledigt** |
| v26.67c | Masterliste um Teilnehmer-Dashboard-Zertifikats-Verifizierungs-State und Testdokument ergänzt – **erledigt** |
| v26.68a | Teilnehmer-Dashboard-Zertifikats-QR-Code-State vorbereitet: `getParticipantDashboardCertificateQrCodeState()`, `local_dashboard_certificate_qr_code_hidden`, QR-Code-State verfügbar, lokal verborgen, kein QR-Code, kein QR-Code-Bild, kein Download, kein Druck, kein UI-Blocker – **erledigt** |
| v26.68b | Teilnehmer-Dashboard-Zertifikats-QR-Code-State-Test dokumentiert: QR-Code-State verfügbar, `isVisible=false`, `canRender=false`, `canCreateCertificateQrCode=false`, `canRenderCertificateQrCodeImage=false`, `canDownloadCertificateQrCode=false`, lokaler Zugriff bleibt erlaubt – **erledigt** |
| v26.68c | GitHub-Pages-Build stabilisiert: `.nojekyll` im Root ergänzt, damit die statische HTML/CSS/JS-App nicht als Jekyll-Seite verarbeitet wird – **erledigt** |
| v26.68d | Masterliste um Teilnehmer-Dashboard-Zertifikats-QR-Code-State, Testdokument und GitHub-Pages-`.nojekyll` ergänzt – **erledigt** |
| v26.69a | Teilnehmer-Dashboard-Zertifikats-Gültigkeits-State vorbereitet: `getParticipantDashboardCertificateValidityState()`, `local_dashboard_certificate_validity_hidden`, Gültigkeits-State verfügbar, lokal verborgen, keine echte Gültigkeitsprüfung, keine Ablaufprüfung, keine Widerrufsprüfung, keine Badge-Anzeige, kein UI-Blocker – **erledigt** |
| v26.69b | Teilnehmer-Dashboard-Zertifikats-Gültigkeits-State-Test dokumentiert: Gültigkeits-State verfügbar, `isVisible=false`, `canRender=false`, `canCheckCertificateValidity=false`, `canRefreshCertificateValidity=false`, `canShowCertificateValidBadge=false`, `canShowCertificateExpiredBadge=false`, `canShowCertificateRevokedBadge=false`, lokaler Zugriff bleibt erlaubt – **erledigt** |
| v26.69c | Masterliste um Teilnehmer-Dashboard-Zertifikats-Gültigkeits-State und Testdokument ergänzt – **erledigt** |
| v26.70a | Teilnehmer-Dashboard-Zertifikats-Widerrufs-State vorbereitet: `getParticipantDashboardCertificateRevocationState()`, `local_dashboard_certificate_revocation_hidden`, Widerrufs-State verfügbar, lokal verborgen, kein echter Widerruf, keine Widerrufsbestätigung, kein Widerrufsgrund, keine Widerrufs-Anzeige, kein UI-Blocker – **erledigt** |
| v26.70b | Teilnehmer-Dashboard-Zertifikats-Widerrufs-State-Test dokumentiert: Widerrufs-State verfügbar, `isVisible=false`, `canRender=false`, `canRequestCertificateRevocation=false`, `canConfirmCertificateRevocation=false`, `canCancelCertificateRevocation=false`, `canShowCertificateRevokedNotice=false`, lokaler Zugriff bleibt erlaubt – **erledigt** |
| v26.70c | Masterliste um Teilnehmer-Dashboard-Zertifikats-Widerrufs-State und Testdokument ergänzt – **erledigt** |
| v26.71a | Teilnehmer-Dashboard-Zertifikats-Audit-Log-State vorbereitet: `getParticipantDashboardCertificateAuditLogState()`, `local_dashboard_certificate_audit_log_hidden`, Audit-Log-State verfügbar, lokal verborgen, kein echtes Zertifikats-Protokoll, keine Teilnehmerdaten, keine IP-Speicherung, kein Export, kein UI-Blocker – **erledigt** |
| v26.71b | Teilnehmer-Dashboard-Zertifikats-Audit-Log-State-Test dokumentiert: Audit-Log-State verfügbar, `isVisible=false`, `canRender=false`, `canLoadCertificateAuditLog=false`, `canRefreshCertificateAuditLog=false`, `canExportCertificateAuditLog=false`, lokaler Zugriff bleibt erlaubt – **erledigt** |
| v26.71c | Masterliste um Teilnehmer-Dashboard-Zertifikats-Audit-Log-State und Testdokument ergänzt – **erledigt** |
| v26.72a | Teilnehmer-Dashboard-Zertifikats-Einwilligungs-State vorbereitet: `getParticipantDashboardCertificateConsentState()`, `local_dashboard_certificate_consent_hidden`, Einwilligungs-State verfügbar, lokal verborgen, keine echte Einwilligung, keine Teilnehmerdaten, keine Freigabe, keine Einwilligungs-Abfrage, kein UI-Blocker – **erledigt** |
| v26.72b | Teilnehmer-Dashboard-Zertifikats-Einwilligungs-State-Test dokumentiert: Einwilligungs-State verfügbar, `isVisible=false`, `canRender=false`, `canLoadCertificateConsent=false`, `canGrantCertificateConsent=false`, `canRevokeCertificateConsent=false`, `canRefreshCertificateConsent=false`, lokaler Zugriff bleibt erlaubt – **erledigt** |
| v26.72c | Masterliste um Teilnehmer-Dashboard-Zertifikats-Einwilligungs-State und Testdokument ergänzt – **erledigt** |
| v26.73a | Teilnehmer-Dashboard-Zertifikats-Datenschutz-Hinweis-State vorbereitet: `getParticipantDashboardCertificatePrivacyNoticeState()`, `local_dashboard_certificate_privacy_notice_hidden`, Datenschutz-Hinweis-State verfügbar, lokal verborgen, kein echter Datenschutz-Hinweis, keine Teilnehmerdaten, keine Zustimmung, keine Hinweis-Anzeige, kein UI-Blocker – **erledigt** |
| v26.73b | Teilnehmer-Dashboard-Zertifikats-Datenschutz-Hinweis-State-Test dokumentiert: Datenschutz-Hinweis-State verfügbar, `isVisible=false`, `canRender=false`, `canLoadCertificatePrivacyNotice=false`, `canAcceptCertificatePrivacyNotice=false`, `canRefreshCertificatePrivacyNotice=false`, lokaler Zugriff bleibt erlaubt – **erledigt** |
| v26.73c | Masterliste um Teilnehmer-Dashboard-Zertifikats-Datenschutz-Hinweis-State und Testdokument ergänzt – **erledigt** |
| v26.74a | Teilnehmer-Dashboard-Zertifikats-Aufbewahrungs- und Lösch-State vorbereitet: `getParticipantDashboardCertificateRetentionState()`, `local_dashboard_certificate_retention_hidden`, Retention-State verfügbar, lokal verborgen, keine echte Aufbewahrungsfrist, keine echte Löschanforderung, keine Löschbestätigung, keine Anonymisierung, kein UI-Blocker – **erledigt** |
| v26.74b | Teilnehmer-Dashboard-Zertifikats-Aufbewahrungs- und Lösch-State-Test dokumentiert: Retention-State verfügbar, `isVisible=false`, `canRender=false`, `canLoadCertificateRetention=false`, `canRequestCertificateDeletion=false`, `canConfirmCertificateDeletion=false`, `canRefreshCertificateRetention=false`, lokaler Zugriff bleibt erlaubt – **erledigt** |
| v26.74c | Masterliste um Teilnehmer-Dashboard-Zertifikats-Aufbewahrungs- und Lösch-State und Testdokument ergänzt – **erledigt** |
| v26.75a | Teilnehmer-Dashboard-Zertifikats-Datenauskunft-State vorbereitet: `getParticipantDashboardCertificateDataAccessState()`, `local_dashboard_certificate_data_access_hidden`, Datenauskunft-State verfügbar, lokal verborgen, keine echte Datenauskunft, kein echter Datenexport, kein echter Download, keine Teilnehmerdaten, kein UI-Blocker – **erledigt** |
| v26.75b | Teilnehmer-Dashboard-Zertifikats-Datenauskunft-State-Test dokumentiert: Datenauskunft-State verfügbar, `isVisible=false`, `canRender=false`, `canLoadCertificateDataAccess=false`, `canRequestCertificateDataAccess=false`, `canPrepareCertificateDataExport=false`, `canDownloadCertificateDataExport=false`, `canRefreshCertificateDataAccess=false`, lokaler Zugriff bleibt erlaubt – **erledigt** |
| v26.75c | Masterliste um Teilnehmer-Dashboard-Zertifikats-Datenauskunft-State und Testdokument ergänzt – **erledigt** |
| v26.76a | Teilnehmer-Dashboard-Zertifikats-Datenberichtigung-State vorbereitet: `getParticipantDashboardCertificateDataCorrectionState()`, `local_dashboard_certificate_data_correction_hidden`, Datenberichtigung-State verfügbar, lokal verborgen, keine echte Datenberichtigung, keine Prüfung, keine Freigabe, keine Ablehnung, keine Teilnehmerdaten, kein UI-Blocker – **erledigt** |
| v26.76b | Teilnehmer-Dashboard-Zertifikats-Datenberichtigung-State-Test dokumentiert: Datenberichtigung-State verfügbar, `isVisible=false`, `canRender=false`, `canLoadCertificateDataCorrection=false`, `canRequestCertificateDataCorrection=false`, `canReviewCertificateDataCorrection=false`, `canApproveCertificateDataCorrection=false`, `canRejectCertificateDataCorrection=false`, `canRefreshCertificateDataCorrection=false`, lokaler Zugriff bleibt erlaubt – **erledigt** |
| v26.76c | Masterliste um Teilnehmer-Dashboard-Zertifikats-Datenberichtigung-State und Testdokument ergänzt – **erledigt** |
| v26.77a | Teilnehmer-Dashboard-Zertifikats-Datenlöschungs-Anfrage-State vorbereitet: `getParticipantDashboardCertificateDataDeletionRequestState()`, `local_dashboard_certificate_data_deletion_request_hidden`, Datenlöschungs-Anfrage-State verfügbar, lokal verborgen, keine echte Datenlöschungs-Anfrage, keine Prüfung, keine Freigabe, keine Ablehnung, keine Löschung, keine Teilnehmerdaten, kein UI-Blocker – **erledigt** |
| v26.77b | Teilnehmer-Dashboard-Zertifikats-Datenlöschungs-Anfrage-State-Test dokumentiert: Datenlöschungs-Anfrage-State verfügbar, `isVisible=false`, `canRender=false`, `canLoadCertificateDataDeletionRequest=false`, `canRequestCertificateDataDeletion=false`, `canReviewCertificateDataDeletionRequest=false`, `canApproveCertificateDataDeletionRequest=false`, `canRejectCertificateDataDeletionRequest=false`, `canCompleteCertificateDataDeletionRequest=false`, `canRefreshCertificateDataDeletionRequest=false`, lokaler Zugriff bleibt erlaubt – **erledigt** |
| v26.77c | Masterliste um Teilnehmer-Dashboard-Zertifikats-Datenlöschungs-Anfrage-State und Testdokument ergänzt – **erledigt** |
| v26.78a | Teilnehmer-Dashboard-Zertifikats-Datenlöschungs-Bestätigungs-State vorbereitet: `getParticipantDashboardCertificateDataDeletionConfirmationState()`, `local_dashboard_certificate_data_deletion_confirmation_hidden`, Datenlöschungs-Bestätigungs-State verfügbar, lokal verborgen, keine echte Datenlöschungs-Bestätigung, kein echter Bestätigungs-Download, keine Teilnehmerdaten, kein UI-Blocker – **erledigt** |
| v26.78b | Teilnehmer-Dashboard-Zertifikats-Datenlöschungs-Bestätigungs-State-Test dokumentiert: Datenlöschungs-Bestätigungs-State verfügbar, `isVisible=false`, `canRender=false`, `canLoadCertificateDataDeletionConfirmation=false`, `canConfirmCertificateDataDeletion=false`, `canDownloadCertificateDataDeletionConfirmation=false`, `canRefreshCertificateDataDeletionConfirmation=false`, lokaler Zugriff bleibt erlaubt – **erledigt** |
| v26.78c | Masterliste um Teilnehmer-Dashboard-Zertifikats-Datenlöschungs-Bestätigungs-State und Testdokument ergänzt – **erledigt** |
| v26.79a | Teilnehmer-Dashboard-Zertifikats-Datenexport-Datei-State vorbereitet: `getParticipantDashboardCertificateDataExportFileState()`, `local_dashboard_certificate_data_export_file_hidden`, Datenexport-Datei-State verfügbar, lokal verborgen, keine echte Datenexport-Datei, keine Datei-Erzeugung, kein Download, keine Teilnehmerdaten, kein UI-Blocker – **erledigt** |
| v26.79b | Teilnehmer-Dashboard-Zertifikats-Datenexport-Datei-State-Test dokumentiert: Datenexport-Datei-State verfügbar, `isVisible=false`, `canRender=false`, `canLoadCertificateDataExportFile=false`, `canPrepareCertificateDataExportFile=false`, `canGenerateCertificateDataExportFile=false`, `canDownloadCertificateDataExportFile=false`, `canRefreshCertificateDataExportFile=false`, lokaler Zugriff bleibt erlaubt – **erledigt** |
| v26.79c | Masterliste um Teilnehmer-Dashboard-Zertifikats-Datenexport-Datei-State und Testdokument ergänzt – **erledigt** |
| v26.80a | Teilnehmer-Dashboard-Zertifikats-Datenexport-Ablauf-State vorbereitet: `getParticipantDashboardCertificateDataExportExpiryState()`, `local_dashboard_certificate_data_export_expiry_hidden`, Datenexport-Ablauf-State verfügbar, lokal verborgen, keine echte Ablaufprüfung, keine Ablaufwarnung, keine Ablaufmarkierung, keine Teilnehmerdaten, kein UI-Blocker – **erledigt** |
| v26.80b | Teilnehmer-Dashboard-Zertifikats-Datenexport-Ablauf-State-Test dokumentiert: Datenexport-Ablauf-State verfügbar, `isVisible=false`, `canRender=false`, `canLoadCertificateDataExportExpiry=false`, `canCheckCertificateDataExportExpiry=false`, `canMarkCertificateDataExportExpired=false`, `canRefreshCertificateDataExportExpiry=false`, lokaler Zugriff bleibt erlaubt – **erledigt** |
| v26.80c | Masterliste um Teilnehmer-Dashboard-Zertifikats-Datenexport-Ablauf-State und Testdokument ergänzt – **erledigt** |
| v26.81a | Teilnehmer-Dashboard-Zertifikats-Datenexport-Download-Protokoll-State vorbereitet: `getParticipantDashboardCertificateDataExportDownloadLogState()`, `local_dashboard_certificate_data_export_download_log_hidden`, Download-Protokoll-State verfügbar, lokal verborgen, kein echtes Download-Protokoll, keine Download-Erfassung, keine Download-Liste, keine Teilnehmerdaten, kein UI-Blocker – **erledigt** |
| v26.81b | Teilnehmer-Dashboard-Zertifikats-Datenexport-Download-Protokoll-State-Test dokumentiert: Download-Protokoll-State verfügbar, `isVisible=false`, `canRender=false`, `canLoadCertificateDataExportDownloadLog=false`, `canRecordCertificateDataExportDownload=false`, `canRefreshCertificateDataExportDownloadLog=false`, lokaler Zugriff bleibt erlaubt – **erledigt** |
| v26.81c | Masterliste um Teilnehmer-Dashboard-Zertifikats-Datenexport-Download-Protokoll-State und Testdokument ergänzt – **erledigt** |
| v26.82a | Teilnehmer-Dashboard-Zertifikats-Datenexport-Fehler-State vorbereitet: `getParticipantDashboardCertificateDataExportErrorState()`, `local_dashboard_certificate_data_export_error_hidden`, Datenexport-Fehler-State verfügbar, lokal verborgen, keine echte Fehlererfassung, keine Fehleranzeige, keine Fehlerbehebung, keine Teilnehmerdaten, kein UI-Blocker – **erledigt** |
| v26.82b | Teilnehmer-Dashboard-Zertifikats-Datenexport-Fehler-State-Test dokumentiert: Datenexport-Fehler-State verfügbar, `isVisible=false`, `canRender=false`, `canLoadCertificateDataExportError=false`, `canRecordCertificateDataExportError=false`, `canResolveCertificateDataExportError=false`, `canRefreshCertificateDataExportError=false`, lokaler Zugriff bleibt erlaubt – **erledigt** |
| v26.82c | Masterliste um Teilnehmer-Dashboard-Zertifikats-Datenexport-Fehler-State und Testdokument ergänzt – **erledigt** |
| v26.83a | Teilnehmer-Dashboard-Zertifikats-Datenexport-Wiederholung-State vorbereitet: `getParticipantDashboardCertificateDataExportRetryState()`, `local_dashboard_certificate_data_export_retry_hidden`, Datenexport-Wiederholung-State verfügbar, lokal verborgen, keine echte Wiederholungsanfrage, keine Wiederholungsausführung, keine Fehlerbehebung, keine Teilnehmerdaten, kein UI-Blocker – **erledigt** |
| v26.83b | Teilnehmer-Dashboard-Zertifikats-Datenexport-Wiederholung-State-Test dokumentiert: Datenexport-Wiederholung-State verfügbar, `isVisible=false`, `canRender=false`, `canLoadCertificateDataExportRetry=false`, `canRequestCertificateDataExportRetry=false`, `canResolveCertificateDataExportRetry=false`, `canRefreshCertificateDataExportRetry=false`, lokaler Zugriff bleibt erlaubt – **erledigt** |
| v26.83c | Masterliste um Teilnehmer-Dashboard-Zertifikats-Datenexport-Wiederholung-State und Testdokument ergänzt – **erledigt** |
| v26.84a | Teilnehmer-Dashboard-Zertifikats-Datenexport-Status-Zusammenfassung-State vorbereitet: `getParticipantDashboardCertificateDataExportStatusSummaryState()`, `local_dashboard_certificate_data_export_status_summary_hidden`, leichte Version ohne Nested-State-Ausführung, lokal verborgen, keine echte Statusberechnung, keine Statusanzeige, keine Teilnehmerdaten, kein UI-Blocker – **erledigt** |
| v26.84b | Teilnehmer-Dashboard-Zertifikats-Datenexport-Status-Zusammenfassung-State-Test dokumentiert: `dependencyStatusMode=reference_only_no_nested_state_execution`, `isVisible=false`, `canRender=false`, `canComputeCertificateDataExportStatusSummary=false`, lokaler Zugriff bleibt erlaubt – **erledigt** |
| v26.84c | Masterliste um Teilnehmer-Dashboard-Zertifikats-Datenexport-Status-Zusammenfassung-State und Testdokument ergänzt – **erledigt** |
| v26.85a | Teilnehmer-Dashboard-Zertifikats-Datenexport-Benachrichtigungs-State vorbereitet: `getParticipantDashboardCertificateDataExportNotificationState()`, `local_dashboard_certificate_data_export_notification_hidden`, lokal verborgen, keine echte Benachrichtigung, keine Teilnehmerdaten, kein UI-Blocker – **erledigt** |
| v26.85b | Teilnehmer-Dashboard-Zertifikats-Datenexport-Benachrichtigungs-State-Test dokumentiert: `isVisible=false`, `canRender=false`, `canSendCertificateDataExportNotification=false`, `canRefreshCertificateDataExportNotification=false`, lokaler Zugriff bleibt erlaubt – **erledigt** |
| v26.85c | Masterliste um Teilnehmer-Dashboard-Zertifikats-Datenexport-Benachrichtigungs-State und Testdokument ergänzt – **erledigt** |
| v26.86a | Teilnehmer-Dashboard-Zertifikats-Datenexport-Zustellstatus-State vorbereitet: `getParticipantDashboardCertificateDataExportDeliveryStatusState()`, `local_dashboard_certificate_data_export_delivery_status_hidden`, lokal verborgen, keine echte Zustellstatus-Prüfung, keine Teilnehmerdaten, kein UI-Blocker – **erledigt** |
| v26.86b | Teilnehmer-Dashboard-Zertifikats-Datenexport-Zustellstatus-State-Test dokumentiert: `isVisible=false`, `canRender=false`, `canTrackCertificateDataExportDeliveryStatus=false`, `canRefreshCertificateDataExportDeliveryStatus=false`, lokaler Zugriff bleibt erlaubt – **erledigt** |
| v26.86c | Masterliste um Teilnehmer-Dashboard-Zertifikats-Datenexport-Zustellstatus-State und Testdokument ergänzt – **erledigt** |
| v26.87a | Teilnehmer-Dashboard-Zertifikats-Datenexport-Lesebestätigung-State vorbereitet: `getParticipantDashboardCertificateDataExportReadReceiptState()`, `local_dashboard_certificate_data_export_read_receipt_hidden`, lokal verborgen, keine echte Lesebestätigung, keine Teilnehmerdaten, kein UI-Blocker – **erledigt** |
| v26.87b | Teilnehmer-Dashboard-Zertifikats-Datenexport-Lesebestätigung-State-Test dokumentiert: `isVisible=false`, `canRender=false`, `canTrackCertificateDataExportReadReceipt=false`, `canRefreshCertificateDataExportReadReceipt=false`, lokaler Zugriff bleibt erlaubt – **erledigt** |
| v26.87c | Masterliste um Teilnehmer-Dashboard-Zertifikats-Datenexport-Lesebestätigung-State und Testdokument ergänzt – **erledigt** |
| v26.88a | Teilnehmer-Dashboard-Zertifikats-Datenexport-Abschlussstatus-State vorbereitet: `getParticipantDashboardCertificateDataExportCompletionStatusState()`, `local_dashboard_certificate_data_export_completion_status_hidden`, lokal verborgen, keine echte Abschlussstatus-Prüfung, keine Teilnehmerdaten, kein UI-Blocker – **erledigt** |
| v26.88b | Teilnehmer-Dashboard-Zertifikats-Datenexport-Abschlussstatus-State-Test dokumentiert: `isVisible=false`, `canRender=false`, `canTrackCertificateDataExportCompletionStatus=false`, `canRefreshCertificateDataExportCompletionStatus=false`, lokaler Zugriff bleibt erlaubt – **erledigt** |
| v26.88c | Masterliste um Teilnehmer-Dashboard-Zertifikats-Datenexport-Abschlussstatus-State und Testdokument ergänzt – **erledigt** |
| v26.89a | Teilnehmer-Dashboard-Zertifikats-Datenexport-Archivstatus-State vorbereitet: `getParticipantDashboardCertificateDataExportArchiveStatusState()`, `local_dashboard_certificate_data_export_archive_status_hidden`, lokal verborgen, keine echte Archivstatus-Prüfung, keine Teilnehmerdaten, kein UI-Blocker – **erledigt** |
| v26.89b | Teilnehmer-Dashboard-Zertifikats-Datenexport-Archivstatus-State-Test dokumentiert: `isVisible=false`, `canRender=false`, `canTrackCertificateDataExportArchiveStatus=false`, `canRefreshCertificateDataExportArchiveStatus=false`, lokaler Zugriff bleibt erlaubt – **erledigt** |
| v26.89c | Masterliste um Teilnehmer-Dashboard-Zertifikats-Datenexport-Archivstatus-State und Testdokument ergänzt – **erledigt** |
| v26.90a | Teilnehmer-Dashboard-Zertifikats-Datenexport-Löschstatus-State vorbereitet: `getParticipantDashboardCertificateDataExportDeletionStatusState()`, `local_dashboard_certificate_data_export_deletion_status_hidden`, lokal verborgen, keine echte Löschstatus-Prüfung, keine Teilnehmerdaten, kein UI-Blocker – **erledigt** |
| v26.90b | Teilnehmer-Dashboard-Zertifikats-Datenexport-Löschstatus-State-Test dokumentiert: `isVisible=false`, `canRender=false`, `canTrackCertificateDataExportDeletionStatus=false`, `canRefreshCertificateDataExportDeletionStatus=false`, lokaler Zugriff bleibt erlaubt – **erledigt** |
| v26.90c | Masterliste um Teilnehmer-Dashboard-Zertifikats-Datenexport-Löschstatus-State und Testdokument ergänzt – **erledigt** |
| v26.91a | Teilnehmer-Dashboard-Zertifikats-Datenexport-Aufbewahrungsstatus-State vorbereitet: `getParticipantDashboardCertificateDataExportRetentionStatusState()`, `local_dashboard_certificate_data_export_retention_status_hidden`, lokal verborgen, keine echte Aufbewahrungsstatus-Prüfung, keine Teilnehmerdaten, kein UI-Blocker – **erledigt** |
| v26.91b | Teilnehmer-Dashboard-Zertifikats-Datenexport-Aufbewahrungsstatus-State-Test dokumentiert: `isVisible=false`, `canRender=false`, `canTrackCertificateDataExportRetentionStatus=false`, `canRefreshCertificateDataExportRetentionStatus=false`, lokaler Zugriff bleibt erlaubt – **erledigt** |
| v26.91c | Masterliste um Teilnehmer-Dashboard-Zertifikats-Datenexport-Aufbewahrungsstatus-State und Testdokument ergänzt – **erledigt** |
| v26.92a | Teilnehmer-Dashboard-Zertifikats-Datenexport-Sicherheitsstatus-State vorbereitet: `getParticipantDashboardCertificateDataExportSecurityStatusState()`, `local_dashboard_certificate_data_export_security_status_hidden`, lokal verborgen, keine echte Sicherheitsstatus-Prüfung, keine Teilnehmerdaten, kein UI-Blocker – **erledigt** |
| v26.92b | Teilnehmer-Dashboard-Zertifikats-Datenexport-Sicherheitsstatus-State-Test dokumentiert: `isVisible=false`, `canRender=false`, `canTrackCertificateDataExportSecurityStatus=false`, `canRefreshCertificateDataExportSecurityStatus=false`, lokaler Zugriff bleibt erlaubt – **erledigt** |
| v26.92c | Masterliste um Teilnehmer-Dashboard-Zertifikats-Datenexport-Sicherheitsstatus-State und Testdokument ergänzt – **erledigt** |
| v26.93a | Teilnehmer-Dashboard-Zertifikats-Datenexport-Integritätsstatus-State vorbereitet: `getParticipantDashboardCertificateDataExportIntegrityStatusState()`, `local_dashboard_certificate_data_export_integrity_status_hidden`, lokal verborgen, keine echte Integritätsstatus-Prüfung, keine Teilnehmerdaten, kein UI-Blocker – **erledigt** |
| v26.93b | Teilnehmer-Dashboard-Zertifikats-Datenexport-Integritätsstatus-State-Test dokumentiert: `isVisible=false`, `canRender=false`, `canTrackCertificateDataExportIntegrityStatus=false`, `canRefreshCertificateDataExportIntegrityStatus=false`, lokaler Zugriff bleibt erlaubt – **erledigt** |
| v26.93c | Masterliste um Teilnehmer-Dashboard-Zertifikats-Datenexport-Integritätsstatus-State und Testdokument ergänzt – **erledigt** |
| v26.94a | Teilnehmer-Dashboard-Zertifikats-Datenexport-Auditstatus-State vorbereitet: `getParticipantDashboardCertificateDataExportAuditStatusState()`, `local_dashboard_certificate_data_export_audit_status_hidden`, lokal verborgen, keine echte Auditstatus-Prüfung, keine Teilnehmerdaten, kein UI-Blocker – **erledigt** |
| v26.94b | Teilnehmer-Dashboard-Zertifikats-Datenexport-Auditstatus-State-Test dokumentiert: `isVisible=false`, `canRender=false`, `canTrackCertificateDataExportAuditStatus=false`, `canRefreshCertificateDataExportAuditStatus=false`, lokaler Zugriff bleibt erlaubt – **erledigt** |
| v26.94c | Masterliste um Teilnehmer-Dashboard-Zertifikats-Datenexport-Auditstatus-State und Testdokument ergänzt – **erledigt** |
| v26.95a | Teilnehmer-Dashboard-Zertifikats-Datenexport-Prüfprotokollstatus-State vorbereitet: `getParticipantDashboardCertificateDataExportAuditTrailStatusState()`, `local_dashboard_certificate_data_export_audit_trail_status_hidden`, lokal verborgen, keine echte Prüfprotokollstatus-Prüfung, keine Teilnehmerdaten, kein UI-Blocker – **erledigt** |
| v26.95b | Teilnehmer-Dashboard-Zertifikats-Datenexport-Prüfprotokollstatus-State-Test dokumentiert: `isVisible=false`, `canRender=false`, `canTrackCertificateDataExportAuditTrailStatus=false`, `canRefreshCertificateDataExportAuditTrailStatus=false`, lokaler Zugriff bleibt erlaubt – **erledigt** |
| v26.95c | Masterliste um Teilnehmer-Dashboard-Zertifikats-Datenexport-Prüfprotokollstatus-State und Testdokument ergänzt – **erledigt** |
| v26.96a | Teilnehmer-Dashboard-Zertifikats-Datenexport-Freigabestatus-State vorbereitet: `getParticipantDashboardCertificateDataExportApprovalStatusState()`, `local_dashboard_certificate_data_export_approval_status_hidden`, lokal verborgen, keine echte Freigabestatus-Prüfung, keine Teilnehmerdaten, kein UI-Blocker – **erledigt** |
| v26.96b | Teilnehmer-Dashboard-Zertifikats-Datenexport-Freigabestatus-State-Test dokumentiert: `isVisible=false`, `canRender=false`, `canTrackCertificateDataExportApprovalStatus=false`, `canRefreshCertificateDataExportApprovalStatus=false`, lokaler Zugriff bleibt erlaubt – **erledigt** |
| v26.96c | Masterliste um Teilnehmer-Dashboard-Zertifikats-Datenexport-Freigabestatus-State und Testdokument ergänzt – **erledigt** |
| v26.97a | Teilnehmer-Dashboard-Zertifikats-Datenexport-Ablehnungsstatus-State vorbereitet: `getParticipantDashboardCertificateDataExportRejectionStatusState()`, `local_dashboard_certificate_data_export_rejection_status_hidden`, lokal verborgen, keine echte Ablehnungsstatus-Prüfung, keine Teilnehmerdaten, kein UI-Blocker – **erledigt** |
| v26.97b | Teilnehmer-Dashboard-Zertifikats-Datenexport-Ablehnungsstatus-State-Test dokumentiert: `isVisible=false`, `canRender=false`, `canTrackCertificateDataExportRejectionStatus=false`, `canRefreshCertificateDataExportRejectionStatus=false`, lokaler Zugriff bleibt erlaubt – **erledigt** |
| v26.97c | Masterliste um Teilnehmer-Dashboard-Zertifikats-Datenexport-Ablehnungsstatus-State und Testdokument ergänzt – **erledigt** |
| v26.98a | Teilnehmer-Dashboard-Zertifikats-Datenexport-Wartestatus-State vorbereitet: `getParticipantDashboardCertificateDataExportPendingStatusState()`, `local_dashboard_certificate_data_export_pending_status_hidden`, lokal verborgen, keine echte Wartestatus-Prüfung, keine Teilnehmerdaten, kein UI-Blocker – **erledigt** |
| v26.98b | Teilnehmer-Dashboard-Zertifikats-Datenexport-Wartestatus-State-Test dokumentiert: `isVisible=false`, `canRender=false`, `canTrackCertificateDataExportPendingStatus=false`, `canRefreshCertificateDataExportPendingStatus=false`, lokaler Zugriff bleibt erlaubt – **erledigt** |
| v26.98c | Masterliste um Teilnehmer-Dashboard-Zertifikats-Datenexport-Wartestatus-State und Testdokument ergänzt – **erledigt** |
| v26.99a | Teilnehmer-Dashboard-Zertifikats-Datenexport-Nachprüfungsstatus-State vorbereitet: `getParticipantDashboardCertificateDataExportReviewStatusState()`, `local_dashboard_certificate_data_export_review_status_hidden`, lokal verborgen, keine echte Nachprüfungsstatus-Prüfung, keine Teilnehmerdaten, kein UI-Blocker – **erledigt** |
| v26.99b | Teilnehmer-Dashboard-Zertifikats-Datenexport-Nachprüfungsstatus-State-Test dokumentiert: `isVisible=false`, `canRender=false`, `canTrackCertificateDataExportReviewStatus=false`, `canRefreshCertificateDataExportReviewStatus=false`, lokaler Zugriff bleibt erlaubt – **erledigt** |
| v26.99c | Masterliste um Teilnehmer-Dashboard-Zertifikats-Datenexport-Nachprüfungsstatus-State und Testdokument ergänzt – **erledigt** |
| v27.00a | Teilnehmer-Dashboard-Zertifikats-Datenexport-Endstatus-State vorbereitet: `getParticipantDashboardCertificateDataExportFinalStatusState()`, `local_dashboard_certificate_data_export_final_status_hidden`, lokal verborgen, keine echte Endstatus-Prüfung, keine Teilnehmerdaten, kein UI-Blocker – **erledigt** |
| v27.00b | Teilnehmer-Dashboard-Zertifikats-Datenexport-Endstatus-State-Test dokumentiert: `isVisible=false`, `canRender=false`, `canTrackCertificateDataExportFinalStatus=false`, `canRefreshCertificateDataExportFinalStatus=false`, lokaler Zugriff bleibt erlaubt – **erledigt** |
| v27.00c | Masterliste um Teilnehmer-Dashboard-Zertifikats-Datenexport-Endstatus-State und Testdokument ergänzt – **erledigt** |
| v27.01a | Teilnehmer-Dashboard-Zertifikats-Datenexport-Übergabestatus-State vorbereitet: `getParticipantDashboardCertificateDataExportHandoverStatusState()`, `local_dashboard_certificate_data_export_handover_status_hidden`, lokal verborgen, keine echte Übergabestatus-Prüfung, keine Teilnehmerdaten, kein UI-Blocker – **erledigt** |
| v27.01b | Teilnehmer-Dashboard-Zertifikats-Datenexport-Übergabestatus-State-Test dokumentiert: `isVisible=false`, `canRender=false`, `canTrackCertificateDataExportHandoverStatus=false`, `canRefreshCertificateDataExportHandoverStatus=false`, lokaler Zugriff bleibt erlaubt – **erledigt** |
| v27.01c | Masterliste um Teilnehmer-Dashboard-Zertifikats-Datenexport-Übergabestatus-State und Testdokument ergänzt – **erledigt** |
| v27.02a | Teilnehmer-Dashboard-Zertifikats-Datenexport-Empfangsstatus-State vorbereitet: `getParticipantDashboardCertificateDataExportReceptionStatusState()`, `local_dashboard_certificate_data_export_reception_status_hidden`, lokal verborgen, keine echte Empfangsstatus-Prüfung, keine Teilnehmerdaten, kein UI-Blocker – **erledigt** |
| v27.02b | Teilnehmer-Dashboard-Zertifikats-Datenexport-Empfangsstatus-State-Test dokumentiert: `isVisible=false`, `canRender=false`, `canTrackCertificateDataExportReceptionStatus=false`, `canRefreshCertificateDataExportReceptionStatus=false`, lokaler Zugriff bleibt erlaubt – **erledigt** |
| v27.02c | Masterliste um Teilnehmer-Dashboard-Zertifikats-Datenexport-Empfangsstatus-State und Testdokument ergänzt – **erledigt** |
| v27.03a | Teilnehmer-Dashboard-Zertifikats-Datenexport-Bestätigungsstatus-State vorbereitet: `getParticipantDashboardCertificateDataExportConfirmationStatusState()`, `local_dashboard_certificate_data_export_confirmation_status_hidden`, lokal verborgen, keine echte Bestätigungsstatus-Prüfung, keine Teilnehmerdaten, kein UI-Blocker – **erledigt** |
| v27.03b | Teilnehmer-Dashboard-Zertifikats-Datenexport-Bestätigungsstatus-State-Test dokumentiert: `isVisible=false`, `canRender=false`, `canTrackCertificateDataExportConfirmationStatus=false`, `canRefreshCertificateDataExportConfirmationStatus=false`, lokaler Zugriff bleibt erlaubt – **erledigt** |
| v27.03c | Masterliste um Teilnehmer-Dashboard-Zertifikats-Datenexport-Bestätigungsstatus-State und Testdokument ergänzt – **erledigt** |
| v27.04a | Teilnehmer-Dashboard-Zertifikats-Datenexport-Freigabestatus-State vorbereitet: `getParticipantDashboardCertificateDataExportReleaseStatusState()`, `local_dashboard_certificate_data_export_release_status_hidden`, lokal verborgen, keine echte Freigabestatus-Prüfung, keine Teilnehmerdaten, kein UI-Blocker – **erledigt** |
| v27.04b | Teilnehmer-Dashboard-Zertifikats-Datenexport-Freigabestatus-State-Test dokumentiert: `isVisible=false`, `canRender=false`, `canTrackCertificateDataExportReleaseStatus=false`, `canRefreshCertificateDataExportReleaseStatus=false`, lokaler Zugriff bleibt erlaubt – **erledigt** |
| v27.04c | Masterliste um Teilnehmer-Dashboard-Zertifikats-Datenexport-Freigabestatus-State und Testdokument ergänzt – **erledigt** |
| v27.05a | Teilnehmer-Dashboard-Zertifikats-Datenexport-Abrufstatus-State vorbereitet: `getParticipantDashboardCertificateDataExportRetrievalStatusState()`, `local_dashboard_certificate_data_export_retrieval_status_hidden`, lokal verborgen, keine echte Abrufstatus-Prüfung, keine Teilnehmerdaten, kein UI-Blocker – **erledigt** |
| v27.05b | Teilnehmer-Dashboard-Zertifikats-Datenexport-Abrufstatus-State-Test dokumentiert: `isVisible=false`, `canRender=false`, `canTrackCertificateDataExportRetrievalStatus=false`, `canRefreshCertificateDataExportRetrievalStatus=false`, lokaler Zugriff bleibt erlaubt – **erledigt** |
| v27.05c | Masterliste um Teilnehmer-Dashboard-Zertifikats-Datenexport-Abrufstatus-State und Testdokument ergänzt – **erledigt** |
| v27.06a | Teilnehmer-Dashboard-Zertifikats-Datenexport-Protokollstatus-State vorbereitet: `getParticipantDashboardCertificateDataExportProtocolStatusState()`, `local_dashboard_certificate_data_export_protocol_status_hidden`, lokal verborgen, keine echte Protokollstatus-Prüfung, keine Teilnehmerdaten, kein UI-Blocker – **erledigt** |
| v27.06b | Teilnehmer-Dashboard-Zertifikats-Datenexport-Protokollstatus-State-Test dokumentiert: `isVisible=false`, `canRender=false`, `canTrackCertificateDataExportProtocolStatus=false`, `canRefreshCertificateDataExportProtocolStatus=false`, lokaler Zugriff bleibt erlaubt – **erledigt** |
| v27.06c | Masterliste um Teilnehmer-Dashboard-Zertifikats-Datenexport-Protokollstatus-State und Testdokument ergänzt – **erledigt** |
| v27.07a | Teilnehmer-Dashboard-Zertifikats-Datenexport-Übergabeprotokollstatus-State vorbereitet: `getParticipantDashboardCertificateDataExportHandoverProtocolStatusState()`, `local_dashboard_certificate_data_export_handover_protocol_status_hidden`, lokal verborgen, keine echte Übergabeprotokollstatus-Prüfung, keine Teilnehmerdaten, kein UI-Blocker – **erledigt** |
| v27.07b | Teilnehmer-Dashboard-Zertifikats-Datenexport-Übergabeprotokollstatus-State-Test dokumentiert: `isVisible=false`, `canRender=false`, `canTrackCertificateDataExportHandoverProtocolStatus=false`, `canRefreshCertificateDataExportHandoverProtocolStatus=false`, lokaler Zugriff bleibt erlaubt – **erledigt** |
| v27.07c | Masterliste um Teilnehmer-Dashboard-Zertifikats-Datenexport-Übergabeprotokollstatus-State und Testdokument ergänzt – **erledigt** |
| v27.08a | Teilnehmer-Dashboard-Zertifikats-Datenexport-Abschlussprotokollstatus-State vorbereitet: `getParticipantDashboardCertificateDataExportCompletionProtocolStatusState()`, `local_dashboard_certificate_data_export_completion_protocol_status_hidden`, lokal verborgen, keine echte Abschlussprotokollstatus-Prüfung, keine Teilnehmerdaten, kein UI-Blocker – **erledigt** |
| v27.08b | Teilnehmer-Dashboard-Zertifikats-Datenexport-Abschlussprotokollstatus-State-Test dokumentiert: `isVisible=false`, `canRender=false`, `canTrackCertificateDataExportCompletionProtocolStatus=false`, `canRefreshCertificateDataExportCompletionProtocolStatus=false`, lokaler Zugriff bleibt erlaubt – **erledigt** |
| v27.08c | Masterliste um Teilnehmer-Dashboard-Zertifikats-Datenexport-Abschlussprotokollstatus-State und Testdokument ergänzt – **erledigt** |
| v27.09a | Teilnehmer-Dashboard-Zertifikats-Datenexport-Endnachweisstatus-State vorbereitet: `getParticipantDashboardCertificateDataExportFinalProofStatusState()`, `local_dashboard_certificate_data_export_final_proof_status_hidden`, lokal verborgen, keine echte Endnachweisstatus-Prüfung, keine Teilnehmerdaten, kein UI-Blocker – **erledigt** |
| v27.09b | Teilnehmer-Dashboard-Zertifikats-Datenexport-Endnachweisstatus-State-Test dokumentiert: `isVisible=false`, `canRender=false`, `canTrackCertificateDataExportFinalProofStatus=false`, `canRefreshCertificateDataExportFinalProofStatus=false`, lokaler Zugriff bleibt erlaubt – **erledigt** |
| v27.09c | Masterliste um Teilnehmer-Dashboard-Zertifikats-Datenexport-Endnachweisstatus-State und Testdokument ergänzt – **erledigt** |
| v27.10a | Teilnehmer-Dashboard-Zertifikats-Datenexport-Abgabebestätigungsstatus-State vorbereitet: `getParticipantDashboardCertificateDataExportSubmissionConfirmationStatusState()`, `local_dashboard_certificate_data_export_submission_confirmation_status_hidden`, lokal verborgen, keine echte Abgabebestätigungsstatus-Prüfung, keine Teilnehmerdaten, kein UI-Blocker – **erledigt** |
| v27.10b | Teilnehmer-Dashboard-Zertifikats-Datenexport-Abgabebestätigungsstatus-State-Test dokumentiert: `isVisible=false`, `canRender=false`, `canTrackCertificateDataExportSubmissionConfirmationStatus=false`, `canRefreshCertificateDataExportSubmissionConfirmationStatus=false`, lokaler Zugriff bleibt erlaubt – **erledigt** |
| v27.10c | Masterliste um Teilnehmer-Dashboard-Zertifikats-Datenexport-Abgabebestätigungsstatus-State und Testdokument ergänzt – **erledigt** |
| v27.11a | Teilnehmer-Dashboard-Zertifikats-Datenexport-Empfangsbestätigungsstatus-State vorbereitet: `getParticipantDashboardCertificateDataExportReceiptConfirmationStatusState()`, `local_dashboard_certificate_data_export_receipt_confirmation_status_hidden`, lokal verborgen, keine echte Empfangsbestätigungsstatus-Prüfung, keine Teilnehmerdaten, kein UI-Blocker – **erledigt** |
| v27.11b | Teilnehmer-Dashboard-Zertifikats-Datenexport-Empfangsbestätigungsstatus-State-Test dokumentiert: `isVisible=false`, `canRender=false`, `canTrackCertificateDataExportReceiptConfirmationStatus=false`, `canRefreshCertificateDataExportReceiptConfirmationStatus=false`, lokaler Zugriff bleibt erlaubt – **erledigt** |
| v27.11c | Masterliste um Teilnehmer-Dashboard-Zertifikats-Datenexport-Empfangsbestätigungsstatus-State und Testdokument ergänzt – **erledigt** |
| v27.12a | Teilnehmer-Dashboard-Zertifikats-Datenexport-Zustellnachweisstatus-State vorbereitet: `getParticipantDashboardCertificateDataExportDeliveryProofStatusState()`, `local_dashboard_certificate_data_export_delivery_proof_status_hidden`, lokal verborgen, keine echte Zustellnachweisstatus-Prüfung, keine Teilnehmerdaten, kein UI-Blocker – **erledigt** |
| v27.12b | Teilnehmer-Dashboard-Zertifikats-Datenexport-Zustellnachweisstatus-State-Test dokumentiert: `isVisible=false`, `canRender=false`, `canTrackCertificateDataExportDeliveryProofStatus=false`, `canRefreshCertificateDataExportDeliveryProofStatus=false`, lokaler Zugriff bleibt erlaubt – **erledigt** |
| v27.12c | Masterliste um Teilnehmer-Dashboard-Zertifikats-Datenexport-Zustellnachweisstatus-State und Testdokument ergänzt – **erledigt** |
| v27.13a | Teilnehmer-Dashboard-Zertifikats-Datenexport-Nachweisarchivstatus-State vorbereitet: `getParticipantDashboardCertificateDataExportProofArchiveStatusState()`, `local_dashboard_certificate_data_export_proof_archive_status_hidden`, lokal verborgen, keine echte Nachweisarchivstatus-Prüfung, keine Teilnehmerdaten, kein UI-Blocker – **erledigt** |
| v27.13b | Teilnehmer-Dashboard-Zertifikats-Datenexport-Nachweisarchivstatus-State-Test dokumentiert: `isVisible=false`, `canRender=false`, `canTrackCertificateDataExportProofArchiveStatus=false`, `canRefreshCertificateDataExportProofArchiveStatus=false`, lokaler Zugriff bleibt erlaubt – **erledigt** |
| v27.13c | Masterliste um Teilnehmer-Dashboard-Zertifikats-Datenexport-Nachweisarchivstatus-State und Testdokument ergänzt – **erledigt** |
| v27.14a | Teilnehmer-Dashboard-Zertifikats-Datenexport-Nachweisfreigabestatus-State vorbereitet: `getParticipantDashboardCertificateDataExportProofReleaseStatusState()`, `local_dashboard_certificate_data_export_proof_release_status_hidden`, lokal verborgen, keine echte Nachweisfreigabestatus-Prüfung, keine Teilnehmerdaten, kein UI-Blocker – **erledigt** |
| v27.14b | Teilnehmer-Dashboard-Zertifikats-Datenexport-Nachweisfreigabestatus-State-Test dokumentiert: `isVisible=false`, `canRender=false`, `canTrackCertificateDataExportProofReleaseStatus=false`, `canRefreshCertificateDataExportProofReleaseStatus=false`, lokaler Zugriff bleibt erlaubt – **erledigt** |
| v27.14c | Masterliste um Teilnehmer-Dashboard-Zertifikats-Datenexport-Nachweisfreigabestatus-State und Testdokument ergänzt – **erledigt** |
| v27.15a | Teilnehmer-Dashboard-Zertifikats-Datenexport-Nachweissperrstatus-State vorbereitet: `getParticipantDashboardCertificateDataExportProofBlockStatusState()`, `local_dashboard_certificate_data_export_proof_block_status_hidden`, lokal verborgen, keine echte Nachweissperrstatus-Prüfung, keine Teilnehmerdaten, kein UI-Blocker – **erledigt** |
| v27.15b | Teilnehmer-Dashboard-Zertifikats-Datenexport-Nachweissperrstatus-State-Test dokumentiert: `isVisible=false`, `canRender=false`, `canTrackCertificateDataExportProofBlockStatus=false`, `canRefreshCertificateDataExportProofBlockStatus=false`, lokaler Zugriff bleibt erlaubt – **erledigt** |
| v27.15c | Masterliste um Teilnehmer-Dashboard-Zertifikats-Datenexport-Nachweissperrstatus-State und Testdokument ergänzt – **erledigt** |
| v27.16a | Teilnehmer-Dashboard-Zertifikats-Datenexport-Nachweisprüfstatus-State vorbereitet: `getParticipantDashboardCertificateDataExportProofCheckStatusState()`, `local_dashboard_certificate_data_export_proof_check_status_hidden`, lokal verborgen, keine echte Nachweisprüfstatus-Prüfung, keine Teilnehmerdaten, kein UI-Blocker – **erledigt** |
| v27.16b | Teilnehmer-Dashboard-Zertifikats-Datenexport-Nachweisprüfstatus-State-Test dokumentiert: `isVisible=false`, `canRender=false`, `canTrackCertificateDataExportProofCheckStatus=false`, `canRefreshCertificateDataExportProofCheckStatus=false`, lokaler Zugriff bleibt erlaubt – **erledigt** |
| v27.16c | Masterliste um Teilnehmer-Dashboard-Zertifikats-Datenexport-Nachweisprüfstatus-State und Testdokument ergänzt – **erledigt** |
| v27.17a | Teilnehmer-Dashboard-Zertifikats-Datenexport-Nachweisvalidierungsstatus-State vorbereitet: `getParticipantDashboardCertificateDataExportProofValidationStatusState()`, `local_dashboard_certificate_data_export_proof_validation_status_hidden`, lokal verborgen, keine echte Nachweisvalidierung, keine Teilnehmerdaten, kein UI-Blocker – **erledigt** |
| v27.17b | Teilnehmer-Dashboard-Zertifikats-Datenexport-Nachweisvalidierungsstatus-State-Test dokumentiert: `isVisible=false`, `canRender=false`, `canTrackCertificateDataExportProofValidationStatus=false`, `canRefreshCertificateDataExportProofValidationStatus=false`, lokaler Zugriff bleibt erlaubt – **erledigt** |
| v27.17c | Masterliste um Teilnehmer-Dashboard-Zertifikats-Datenexport-Nachweisvalidierungsstatus-State und Testdokument ergänzt – **erledigt** |
| v27.18a | Teilnehmer-Dashboard-Zertifikats-Datenexport-Nachweisfreigabeprüfstatus-State vorbereitet: `getParticipantDashboardCertificateDataExportProofReleaseCheckStatusState()`, `local_dashboard_certificate_data_export_proof_release_check_status_hidden`, lokal verborgen, keine echte Nachweisfreigabeprüfung, keine Teilnehmerdaten, kein UI-Blocker – **erledigt** |
| v27.18b | Teilnehmer-Dashboard-Zertifikats-Datenexport-Nachweisfreigabeprüfstatus-State-Test dokumentiert: `isVisible=false`, `canRender=false`, `canTrackCertificateDataExportProofReleaseCheckStatus=false`, `canRefreshCertificateDataExportProofReleaseCheckStatus=false`, lokaler Zugriff bleibt erlaubt – **erledigt** |
| v27.18c | Masterliste um Teilnehmer-Dashboard-Zertifikats-Datenexport-Nachweisfreigabeprüfstatus-State und Testdokument ergänzt – **erledigt** |
| v27.19a | MVP-Endspurt-Plan erstellt; MVP-Ziel, Qualitätsregeln, Phasen und Fertigdefinition festgelegt – **erledigt** |
| v27.20a | Supabase-MVP-Tabellenplan für Teilnehmer, Kurse, Zuordnungen, Prüfungen, Zertifikate und Rollen dokumentiert – **erledigt** |
| v27.20b | Supabase-MVP-Schema-Migration vorbereitet; Tabellen, Relationen, Prüfregeln, Indexe und RLS-Aktivierung angelegt, nicht live ausgeführt – **erledigt** |
| v27.20c | Supabase-MVP-RLS-Policy-Plan mit Teilnehmer-, Admin-/Dozent-Rechten und Sicherheitsgrenzen dokumentiert – **erledigt** |
| v27.21a | SQL-RLS-Migration mit Rollen-Helpern und tabellenspezifischen Policies vorbereitet, nicht live ausgeführt – **erledigt** |
| v27.21b | SQL-RLS-Migration statisch geprüft und Testgrenzen für die spätere Live-Prüfung dokumentiert – **erledigt** |
| v27.21c | Masterliste auf den vollständigen MVP-Endspurt-Stand v27.21c aktualisiert – **erledigt** |
| v27.22a | Lokales Supabase-Migrationsprüftool erstellt; Reihenfolge, acht MVP-Tabellen, RLS-Aktivierung, 17 Policies, Rollen-Helper und sensitive Inhalte werden statisch geprüft – **erledigt** |
| v27.22b | Supabase-Migrationsprüfung sicher vor dem bestehenden Preflight in `tools/accaoui-helper.py` integriert – **erledigt** |
| v27.22c | Helper-Integration dokumentiert und Masterliste auf v27.22c aktualisiert – **erledigt** |
| v27.23a | Sicheren manuellen Supabase-Client-Bootstrap mit Live-Schalter, zweiter Bestätigung und ausdrücklicher Initialisierung vorbereitet; keine automatische Verbindung – **erledigt** |
| v27.23b | Bootstrap-Sicherheitsverhalten, lokaler Standardzustand, blockierter Initialisierungsaufruf und Ladefolge dokumentiert; Masterliste aktualisiert – **erledigt** |
| v27.24a | Sicherheitsreview der Prüfungsintegrität abgeschlossen; Manipulationsrisiken dokumentiert und Live-Freigabe gesperrt – **erledigt** |
| v27.24b | Direkte Teilnehmer-Inserts für `exam_attempts` und `exam_answers` gesperrt; Migrationsprüfer auf 15 effektive Policies erweitert – **erledigt** |
| v27.24c | Prüfungsintegrität-Lockdown dokumentiert und Masterliste aktualisiert – **erledigt** |
| v27.25a | Sichere RPC-Architektur für Prüfungsstart, Abgabe, serverseitige Bewertung und Ergebnisabruf festgelegt – **erledigt** |
| v27.25b | Datenbankplan für versionierte Fragen, private Lösungsschlüssel und feste Prüfungs-Snapshots erstellt – **erledigt** |
| v27.25c | Sichere Schema-Migration für `exam_questions`, `exam_question_answer_keys` und `exam_attempt_questions` vorbereitet – **erledigt** |
| v27.25d | Engen Rollen-Helper und drei sichere RLS-Policies für Prüfungsinhalte und eigene Snapshots vorbereitet – **erledigt** |
| v27.25e | Fragen-Schema und RLS statisch dokumentiert und Masterliste auf v27.25e aktualisiert – **erledigt** |
| v27.26a | Lokalen Fragenbankprüfer für 86 Pool-Fragen, vier Fragetypen, gültige Antwortindizes sowie 82 Core-Fragen und 120 Punkte erstellt – **erledigt** |
| v27.26b | Fragenbankprüfung als ersten Sicherheitscheck in `tools/accaoui-helper.py` integriert – **erledigt** |
| v27.26c | Privaten Lösungsschlüssel-Snapshot pro Versuchsfrage ergänzt; alte Prüfungsversuche bleiben von späteren Schlüsseländerungen unabhängig – **erledigt** |
| v27.26d | Versuchsschlüssel-Bewertungsregel auf `per_correct_selection_no_penalty` korrigiert: ein Punkt pro ausgewählter richtiger Antwort, keine Punkte für falsche Auswahlen und kein Punktabzug – **erledigt** |
| v27.26e | Alten `exam_answers`-Speicher abgesichert: `correct_answers` und freie `question_id` entfernt, Antworten eindeutig an `attempt_question_id` gekoppelt und direkte Schreibrechte entzogen – **erledigt** |
| v27.26f | Fehlerhaften und doppelten SQL-Block aus der `exam_answers`-Integritätsmigration entfernt und den Prüfer gegen diese Fehler verstärkt – **erledigt** |
| v27.27a | Sicheren Prüfungsstart-RPC vorbereitet: Teilnehmeridentität über `auth.uid()`, aktiver Kurszugang, Advisory Lock, idempotentes Fortsetzen, exakt 82/120 und atomare sichtbare und private Snapshots ohne Schlüsselrückgabe – **erledigt** |
| v27.27b | Sicheren Antwortspeicher-RPC vorbereitet: nur eigene offene Versuchsfragen, keine Browserpunkte oder Lösungsschlüssel, Indizes validiert und normalisiert – **erledigt** |
| v27.27c | Auswahlbegrenzung korrigiert: Punktewert begrenzt nicht die Zahl möglicher Kreuze; `single`/`combination` maximal eine Auswahl, `multiple`/`praxisfall` mehrere gültige Auswahlen – **erledigt** |
| v27.27d | Sicheren Prüfungsabschluss-RPC vorbereitet: eigener Vollsimulationsversuch, 82/120-Snapshotprüfung, serverseitige Teilpunkte ohne Punktabzug, Bestehensgrenze 60 Punkte sowie atomarer und idempotenter Abschluss ohne Browserpunkte oder Lösungsschlüssel – **erledigt** |
| v27.27e | Manipulationsschutz für Antwortauswahl ergänzt: zulässige Auswahlzahl aus privatem Versuchsschlüssel abgeleitet, Überauswahl beim Speichern und erneut vor der Bewertung gesperrt, ohne Lösungsschlüssel offenzulegen – **erledigt** |
| v27.27f | Sicheren Ergebnisabruf-RPC vorbereitet: nur eigener abgeschlossener Vollsimulationsversuch, historische Ergebnisse für `active`, `expired` und `completed`, `blocked` ausgeschlossen, 82/120-Integritäts-, Punkte- und Bestehensabgleich sowie sichere Ergebniszusammenfassung ohne Lösungsschlüssel, Erklärungen oder richtige Indizes – **erledigt** |
| v27.28a | End-to-End-Sicherheitsaudit des schriftlichen Prüfungs-RPC-Flows dokumentiert; Migrationsprüfer erzwingt jetzt zusätzlich, dass richtige, teilweise richtige, falsche und unbeantwortete Kategorien zusammen exakt 82 ergeben; keine SQL- oder Live-Ausführung – **erledigt** |

**Hinweis:** Supabase ist geplant, aber noch **nicht live** in der App eingebunden (vorbereitete SQL-Migrationen vorhanden, aber nicht live ausgeführt; keine echte Supabase-Verbindung). Seit v26.3a ist der Login-/Teilnehmerzugang-Plan vorhanden; seit v26.3c ist das Login-UI-Konzept dokumentiert; seit v26.3e ist der spätere Auth-Einstiegspunkt geprüft; seit v26.4a existiert ein lokales Auth-Guard-Gerüst ohne Login-Zwang; seit v26.4c sind lokale Teststatus für Login-/Sperr-/Ablaufseiten vorhanden; seit v26.4e sind diese Hinweisseiten optisch verbessert; seit v26.5a ist der Supabase-Konfigurations- und Sicherheitsplan dokumentiert; seit v26.5c existiert ein sicherer Config-Platzhalter ohne echte Keys; seit v26.5e ist der spätere Config-Ladeweg dokumentiert; seit v26.6a erkennt die App lokal den Supabase-Config-Status ohne Live-Verbindung; seit v26.6c ist ein optionaler lokaler Config-Loader vorhanden; seit v26.6e ist dieser Loader lokal getestet; seit v26.7a ist die spätere Supabase-Adapter-Schicht geplant; seit v26.7c existiert ein Adapter-Gerüst ohne SDK und ohne Live-Verbindung; seit v26.7e ist dieses Adapter-Gerüst lokal getestet; seit v26.8a ist der spätere Supabase-SDK-Ladeweg geplant; seit v26.8c erkennt der Adapter zusätzlich den SDK-Status ohne SDK-Live-Anbindung; seit v26.8e ist dieser SDK-Status lokal getestet; seit v26.9a ist die Client-Readiness-Auswertung im Adapter vorbereitet; seit v26.9c ist diese Readiness lokal getestet; seit v26.10a ist die Auth-Readiness im Adapter vorbereitet; seit v26.10c ist diese Auth-Readiness lokal getestet; seit v26.11a ist die Teilnehmerzugangs-Readiness im Adapter vorbereitet.

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
| `docs/SUPABASE_SAFETY_SUMMARY_TEST.md` | Lokaler Test des Supabase-Safety-Summary: `getSupabaseSafetySummary()`, `supabase_local_safe`, `blockingReasons`, `nextRequiredSteps`, kein Client, keine Sessionprüfung – **vorhanden (v26.19b)** |
| `docs/SUPABASE_PARTICIPANT_SESSION_STATE_TEST.md` | Lokaler Test des vorbereiteten Teilnehmer-Session-State: `getParticipantSessionState()`, `local_session_stub`, keine Sessionpflicht, keine Sessionprüfung, lokaler Zugriff erlaubt – **vorhanden (v26.20b)** |
| `docs/SUPABASE_PARTICIPANT_PROFILE_STATE_TEST.md` | Lokaler Test des vorbereiteten Teilnehmer-Profil-State: `getParticipantProfileState()`, `local_profile_stub`, keine Profilpflicht, kein Profilabruf, lokaler Zugriff erlaubt – **vorhanden (v26.21b)** |
| `docs/SUPABASE_PARTICIPANT_COURSE_STATE_TEST.md` | Lokaler Test des vorbereiteten Teilnehmer-Kursstatus-State: `getParticipantCourseState()`, `local_course_stub`, keine Kursstatus-Pflicht, kein Kursabruf, kein Ablaufstatus aktiv, lokaler Zugriff erlaubt – **vorhanden (v26.22b)** |
| `docs/SUPABASE_PARTICIPANT_ACCESS_DECISION_TEST.md` | Lokaler Test der zentralen Teilnehmer-Zugriffsentscheidung: `getParticipantAccessDecisionState()`, `local_access_decision_allowed`, kein Login-Zwang, keine Sperre, lokaler Zugriff erlaubt – **vorhanden (v26.23b)** |
| `docs/SUPABASE_LOGIN_GATE_STATE_TEST.md` | Lokaler Test des vorbereiteten Login-Gate-Status: `getLoginGateState()`, `local_login_gate_disabled`, kein Login-Zwang, Gate kann nicht blockieren, lokaler Zugriff erlaubt – **vorhanden (v26.24b)** |
| `docs/SUPABASE_LOGIN_GATE_UI_STATE_TEST.md` | Lokaler Test des vorbereiteten Login-Gate-UI-State: `getLoginGateUiState()`, `local_login_gate_ui_hidden`, keine sichtbare Login-Maske, kein UI-Blocker, lokaler Zugriff erlaubt – **vorhanden (v26.25b)** |
| `docs/SUPABASE_LOGIN_FORM_STATE_TEST.md` | Lokaler Test des vorbereiteten Login-Formular-State: `getLoginFormState()`, `local_login_form_disabled`, kein sichtbares Formular, keine Eingabeprüfung, keine Authentifizierung, lokaler Zugriff erlaubt – **vorhanden (v26.26b)** |
| `docs/SUPABASE_LOGIN_ERROR_STATE_TEST.md` | Lokaler Test des vorbereiteten Login-Fehler-State: `getLoginErrorState()`, `local_login_error_none`, kein aktiver Fehler, keine Fehlermeldung, lokaler Zugriff erlaubt – **vorhanden (v26.27b)** |
| `docs/SUPABASE_LOGIN_SUCCESS_STATE_TEST.md` | Lokaler Test des vorbereiteten Login-Erfolg-State: `getLoginSuccessState()`, `local_login_success_none`, kein aktiver Login-Erfolg, keine Session, keine Weiterleitung, lokaler Zugriff erlaubt – **vorhanden (v26.28b)** |
| `docs/SUPABASE_LOGOUT_STATE_TEST.md` | Lokaler Test des vorbereiteten Login-Abmelde-State: `getLogoutState()`, `local_logout_disabled`, keine aktive Session, kein Logout, keine Session-Löschung, lokaler Zugriff erlaubt – **vorhanden (v26.29b)** |
| `docs/SUPABASE_PARTICIPANT_DASHBOARD_AUTH_STATE_TEST.md` | Lokaler Test des vorbereiteten Teilnehmer-Dashboard-Auth-State: `getParticipantDashboardAuthState()`, `local_dashboard_auth_disabled`, kein sichtbarer Auth-Bereich, keine Dashboard-Sperre, lokaler Zugriff erlaubt – **vorhanden (v26.30b)** |
| `docs/SUPABASE_PARTICIPANT_DASHBOARD_COURSE_ACCESS_STATE_TEST.md` | Lokaler Test des vorbereiteten Teilnehmer-Dashboard-Kurszugriff-State: `getParticipantDashboardCourseAccessState()`, `local_dashboard_course_access_allowed`, keine Kursprüfung, keine Kurs-Sperre, lokaler Zugriff erlaubt – **vorhanden (v26.31b)** |
| `docs/SUPABASE_PARTICIPANT_DASHBOARD_EXPIRY_STATE_TEST.md` | Lokaler Test des vorbereiteten Teilnehmer-Dashboard-Ablaufdatum-State: `getParticipantDashboardExpiryState()`, `local_dashboard_expiry_check_disabled`, keine Ablaufdatum-Prüfung, keine Ablauf-Warnung, keine Sperre, lokaler Zugriff erlaubt – **vorhanden (v26.32b)** |
| `docs/SUPABASE_PARTICIPANT_DASHBOARD_ACCESS_DECISION_STATE_TEST.md` | Lokaler Test der vorbereiteten Teilnehmer-Dashboard-Zugriffsentscheidung: `getParticipantDashboardAccessDecisionState()`, `local_dashboard_access_decision_allowed`, Dashboard-Zugriff lokal erlaubt, keine Sperre, kein Login-Zwang – **vorhanden (v26.33b)** |
| `docs/SUPABASE_PARTICIPANT_DASHBOARD_READINESS_STATE_TEST.md` | Lokaler Test des vorbereiteten Teilnehmer-Dashboard-Readiness-State: `getParticipantDashboardReadinessState()`, `local_dashboard_readiness_ready`, Dashboard lokal bereit, startbar, renderbar, keine Sperre, kein Login-Zwang – **vorhanden (v26.34b)** |
| `docs/SUPABASE_PARTICIPANT_DASHBOARD_STATUS_BADGE_STATE_TEST.md` | Lokaler Test des vorbereiteten Teilnehmer-Dashboard-Status-Badge-State: `getParticipantDashboardStatusBadgeState()`, `local_dashboard_status_badge_hidden`, Badge lokal verborgen, nicht renderbar, nicht blockierend, kein Login-Zwang – **vorhanden (v26.35b)** |
| `docs/SUPABASE_PARTICIPANT_DASHBOARD_NOTICE_BANNER_STATE_TEST.md` | Lokaler Test des vorbereiteten Teilnehmer-Dashboard-Hinweisbanner-State: `getParticipantDashboardNoticeBannerState()`, `local_dashboard_notice_banner_hidden`, Banner lokal verborgen, nicht renderbar, nicht blockierend, kein Login-Zwang – **vorhanden (v26.36b)** |
| `docs/SUPABASE_PARTICIPANT_DASHBOARD_PROFILE_HEADER_STATE_TEST.md` | Lokaler Test des vorbereiteten Teilnehmer-Dashboard-Profilkopf-State: `getParticipantDashboardProfileHeaderState()`, `local_dashboard_profile_header_hidden`, Profilkopf lokal verborgen, keine Teilnehmerdaten sichtbar, nicht blockierend, kein Login-Zwang – **vorhanden (v26.37b)** |
| `docs/SUPABASE_PARTICIPANT_DASHBOARD_COURSE_CARD_STATE_TEST.md` | Lokaler Test des vorbereiteten Teilnehmer-Dashboard-Kurskarte-State: `getParticipantDashboardCourseCardState()`, `local_dashboard_course_card_hidden`, Kurskarte lokal verborgen, keine Kursdaten sichtbar, nicht blockierend, kein Login-Zwang – **vorhanden (v26.38b)** |
| `docs/SUPABASE_PARTICIPANT_DASHBOARD_PROGRESS_STATE_TEST.md` | Lokaler Test des vorbereiteten Teilnehmer-Dashboard-Fortschritt-State: `getParticipantDashboardProgressState()`, `local_dashboard_progress_hidden`, Fortschritt lokal verborgen, keine Fortschrittsdaten sichtbar, nicht blockierend, kein Login-Zwang – **vorhanden (v26.39b)** |
| `docs/SUPABASE_PARTICIPANT_DASHBOARD_ACTIVITY_LIST_STATE_TEST.md` | Lokaler Test des vorbereiteten Teilnehmer-Dashboard-Aktivitätsliste-State: `getParticipantDashboardActivityListState()`, `local_dashboard_activity_list_hidden`, Aktivitätsliste lokal verborgen, keine Aktivitätsdaten sichtbar, nicht blockierend, kein Login-Zwang – **vorhanden (v26.40b)** |
| `docs/SUPABASE_PARTICIPANT_DASHBOARD_RECOMMENDATIONS_STATE_TEST.md` | Lokaler Test des vorbereiteten Teilnehmer-Dashboard-Empfehlungen-State: `getParticipantDashboardRecommendationsState()`, `local_dashboard_recommendations_hidden`, Empfehlungen lokal verborgen, keine Empfehlungsdaten sichtbar, nicht blockierend, kein Login-Zwang – **vorhanden (v26.41b)** |
| `docs/SUPABASE_PARTICIPANT_DASHBOARD_EXAM_STATUS_STATE_TEST.md` | Lokaler Test des vorbereiteten Teilnehmer-Dashboard-Prüfungsstatus-State: `getParticipantDashboardExamStatusState()`, `local_dashboard_exam_status_hidden`, Prüfungsstatus lokal verborgen, keine Prüfungsdaten sichtbar, nicht blockierend, kein Login-Zwang – **vorhanden (v26.42b)** |
| `docs/SUPABASE_PARTICIPANT_DASHBOARD_CERTIFICATE_STATE_TEST.md` | Lokaler Test des vorbereiteten Teilnehmer-Dashboard-Zertifikat-State: `getParticipantDashboardCertificateState()`, `local_dashboard_certificate_hidden`, Zertifikat lokal verborgen, keine Zertifikatsdaten sichtbar, kein Download, nicht blockierend, kein Login-Zwang – **vorhanden (v26.43b)** |
| `docs/SUPABASE_PARTICIPANT_DASHBOARD_DOCUMENTS_STATE_TEST.md` | Lokaler Test des vorbereiteten Teilnehmer-Dashboard-Dokumente-State: `getParticipantDashboardDocumentsState()`, `local_dashboard_documents_hidden`, Dokumente lokal verborgen, keine Dokumentdaten sichtbar, kein Download, nicht blockierend, kein Login-Zwang – **vorhanden (v26.44b)** |
| `docs/SUPABASE_PARTICIPANT_DASHBOARD_MESSAGES_STATE_TEST.md` | Lokaler Test des vorbereiteten Teilnehmer-Dashboard-Nachrichten-State: `getParticipantDashboardMessagesState()`, `local_dashboard_messages_hidden`, Nachrichten lokal verborgen, keine Nachrichtendaten sichtbar, kein Senden, nicht blockierend, kein Login-Zwang – **vorhanden (v26.45b)** |
| `docs/SUPABASE_PARTICIPANT_DASHBOARD_COURSE_MATERIALS_STATE_TEST.md` | Lokaler Test des vorbereiteten Teilnehmer-Dashboard-Kursmaterial-State: `getParticipantDashboardCourseMaterialsState()`, `local_dashboard_course_materials_hidden`, Kursmaterial lokal verborgen, keine Kursmaterial-Daten sichtbar, kein Öffnen, kein Download, nicht blockierend, kein Login-Zwang – **vorhanden (v26.53b)** |
| `docs/SUPABASE_PARTICIPANT_DASHBOARD_LEARNING_PROGRESS_DETAILS_STATE_TEST.md` | Lokaler Test des vorbereiteten Teilnehmer-Dashboard-Lernfortschritt-Details-State: `getParticipantDashboardLearningProgressDetailsState()`, `local_dashboard_learning_progress_details_hidden`, Details lokal verborgen, keine Detaildaten sichtbar, keine Prozentanzeige, kein aktuelles Lernthema, nicht blockierend, kein Login-Zwang – **vorhanden (v26.54b)** |
| `docs/SUPABASE_PARTICIPANT_DASHBOARD_MISTAKE_TRAINING_DETAILS_STATE_TEST.md` | Lokaler Test des vorbereiteten Teilnehmer-Dashboard-Fehlertraining-Details-State: `getParticipantDashboardMistakeTrainingDetailsState()`, `local_dashboard_mistake_training_details_hidden`, Details lokal verborgen, keine Fehlertraining-Detaildaten sichtbar, keine offenen Fehler, keine Wiederholungs-Empfehlung, keine Startfunktion, nicht blockierend, kein Login-Zwang – **vorhanden (v26.55b)** |
| `docs/SUPABASE_PARTICIPANT_DASHBOARD_EXAM_SIMULATION_DETAILS_STATE_TEST.md` | Lokaler Test des vorbereiteten Teilnehmer-Dashboard-Prüfungssimulation-Details-State: `getParticipantDashboardExamSimulationDetailsState()`, `local_dashboard_exam_simulation_details_hidden`, Details lokal verborgen, keine Simulationsdaten sichtbar, kein Score, keine Empfehlung, keine Startfunktion, nicht blockierend, kein Login-Zwang – **vorhanden (v26.56b)** |
| `docs/SUPABASE_PARTICIPANT_DASHBOARD_ORAL_EXAM_DETAILS_STATE_TEST.md` | Lokaler Test des vorbereiteten Teilnehmer-Dashboard-Mündliche-Prüfung-Details-State: `getParticipantDashboardOralExamDetailsState()`, `local_dashboard_oral_exam_details_hidden`, Details lokal verborgen, keine mündlichen Prüfungsdaten sichtbar, keine offenen Fragen, keine Übungsempfehlung, keine Startfunktion, nicht blockierend, kein Login-Zwang – **vorhanden (v26.57b)** |
| `docs/SUPABASE_PARTICIPANT_DASHBOARD_FLASHCARDS_DETAILS_STATE_TEST.md` | Lokaler Test des vorbereiteten Teilnehmer-Dashboard-Lernkarten-Details-State: `getParticipantDashboardFlashcardsDetailsState()`, `local_dashboard_flashcards_details_hidden`, Details lokal verborgen, keine Lernkarten-Daten sichtbar, keine fälligen Karten, keine Empfehlung, keine Startfunktion, nicht blockierend, kein Login-Zwang – **vorhanden (v26.58b)** |
| `docs/SUPABASE_PARTICIPANT_DASHBOARD_SAMPLE_QUESTIONS_DETAILS_STATE_TEST.md` | Lokaler Test des vorbereiteten Teilnehmer-Dashboard-Musterfragen-Details-State: `getParticipantDashboardSampleQuestionsDetailsState()`, `local_dashboard_sample_questions_details_hidden`, Details lokal verborgen, keine Musterfragen-Daten sichtbar, keine offenen Fragen, keine Empfehlung, keine Startfunktion, nicht blockierend, kein Login-Zwang – **vorhanden (v26.59b)** |
| `docs/SUPABASE_PARTICIPANT_DASHBOARD_EXAM_HISTORY_STATE_TEST.md` | Lokaler Test des vorbereiteten Teilnehmer-Dashboard-Prüfungshistorie-State: `getParticipantDashboardExamHistoryState()`, `local_dashboard_exam_history_hidden`, Historie lokal verborgen, keine Prüfungsdaten sichtbar, kein Score-Verlauf, kein Bestwert, keine Review-Funktion, nicht blockierend, kein Login-Zwang – **vorhanden (v26.60b)** |
| `docs/SUPABASE_PARTICIPANT_DASHBOARD_CERTIFICATE_HISTORY_STATE_TEST.md` | Lokaler Test des vorbereiteten Teilnehmer-Dashboard-Zertifikats-Historie-State: `getParticipantDashboardCertificateHistoryState()`, `local_dashboard_certificate_history_hidden`, Historie lokal verborgen, keine Zertifikatsdaten sichtbar, kein Ausstellungsstatus, keine Download-Aktion, kein Öffnen einzelner Einträge, nicht blockierend, kein Login-Zwang – **vorhanden (v26.61b)** |
| `docs/SUPABASE_PARTICIPANT_DASHBOARD_CERTIFICATE_DOWNLOAD_STATE_TEST.md` | Lokaler Test des vorbereiteten Teilnehmer-Dashboard-Zertifikats-Download-State: `getParticipantDashboardCertificateDownloadState()`, `local_dashboard_certificate_download_hidden`, Downloadbereich lokal verborgen, keine Download-Daten sichtbar, kein Download-Button, kein Download-Start, keine Vorschau, kein Tracking, nicht blockierend, kein Login-Zwang – **vorhanden (v26.62b)** |
| `docs/SUPABASE_PARTICIPANT_DASHBOARD_CERTIFICATE_PREVIEW_STATE_TEST.md` | Lokaler Test des vorbereiteten Teilnehmer-Dashboard-Zertifikats-Vorschau-State: `getParticipantDashboardCertificatePreviewState()`, `local_dashboard_certificate_preview_hidden`, Vorschaubereich lokal verborgen, keine Vorschau-Daten sichtbar, kein Vorschau-Button, kein Vorschau-Frame, kein Aktualisieren, kein Drucken, nicht blockierend, kein Login-Zwang – **vorhanden (v26.63b)** |
| `docs/SUPABASE_PARTICIPANT_DASHBOARD_CERTIFICATE_PRINT_STATE_TEST.md` | Lokaler Test des vorbereiteten Teilnehmer-Dashboard-Zertifikats-Druck-State: `getParticipantDashboardCertificatePrintState()`, `local_dashboard_certificate_print_hidden`, Druck lokal verborgen, kein Druck-Start, kein Druckdialog, nicht blockierend, kein Login-Zwang – **vorhanden (v26.65b)** |
| `docs/SUPABASE_PARTICIPANT_DASHBOARD_CERTIFICATE_SHARE_STATE_TEST.md` | Lokaler Test des vorbereiteten Teilnehmer-Dashboard-Zertifikats-Teilen-State: `getParticipantDashboardCertificateShareState()`, `local_dashboard_certificate_share_hidden`, Teilen lokal verborgen, kein Teilen-Link, keine Teilen-E-Mail, kein UI-Blocker, kein Login-Zwang – **vorhanden (v26.66b)** |
| `docs/SUPABASE_PARTICIPANT_DASHBOARD_CERTIFICATE_VERIFICATION_STATE_TEST.md` | Lokaler Test des vorbereiteten Teilnehmer-Dashboard-Zertifikats-Verifizierungs-State: `getParticipantDashboardCertificateVerificationState()`, `local_dashboard_certificate_verification_hidden`, Verifizierung lokal verborgen, kein QR-Code, keine Prüfseite, keine Online-Verifizierung, kein UI-Blocker, kein Login-Zwang – **vorhanden (v26.67b)** |
| `docs/SUPABASE_PARTICIPANT_DASHBOARD_CERTIFICATE_QR_CODE_STATE_TEST.md` | Lokaler Test des vorbereiteten Teilnehmer-Dashboard-Zertifikats-QR-Code-State: `getParticipantDashboardCertificateQrCodeState()`, `local_dashboard_certificate_qr_code_hidden`, QR-Code lokal verborgen, kein QR-Code-Bild, kein Download, kein Druck, kein UI-Blocker, kein Login-Zwang – **vorhanden (v26.68b)** |
| `docs/SUPABASE_PARTICIPANT_DASHBOARD_CERTIFICATE_VALIDITY_STATE_TEST.md` | Lokaler Test des vorbereiteten Teilnehmer-Dashboard-Zertifikats-Gültigkeits-State: `getParticipantDashboardCertificateValidityState()`, `local_dashboard_certificate_validity_hidden`, Gültigkeit lokal verborgen, keine echte Gültigkeitsprüfung, keine Ablaufprüfung, keine Widerrufsprüfung, keine Badge-Anzeige, kein UI-Blocker, kein Login-Zwang – **vorhanden (v26.69b)** |
| `docs/SUPABASE_PARTICIPANT_DASHBOARD_CERTIFICATE_REVOCATION_STATE_TEST.md` | Lokaler Test des vorbereiteten Teilnehmer-Dashboard-Zertifikats-Widerrufs-State: `getParticipantDashboardCertificateRevocationState()`, `local_dashboard_certificate_revocation_hidden`, Widerruf lokal verborgen, kein echter Widerruf, keine Widerrufsbestätigung, kein Widerrufsgrund, keine Widerrufs-Anzeige, kein UI-Blocker, kein Login-Zwang – **vorhanden (v26.70b)** |
| `docs/SUPABASE_PARTICIPANT_DASHBOARD_CERTIFICATE_AUDIT_LOG_STATE_TEST.md` | Lokaler Test des vorbereiteten Teilnehmer-Dashboard-Zertifikats-Audit-Log-State: `getParticipantDashboardCertificateAuditLogState()`, `local_dashboard_certificate_audit_log_hidden`, Audit-Log lokal verborgen, kein echtes Zertifikats-Protokoll, keine Teilnehmerdaten, keine IP-Speicherung, kein Export, kein UI-Blocker, kein Login-Zwang – **vorhanden (v26.71b)** |
| `docs/SUPABASE_PARTICIPANT_DASHBOARD_CERTIFICATE_CONSENT_STATE_TEST.md` | Lokaler Test des vorbereiteten Teilnehmer-Dashboard-Zertifikats-Einwilligungs-State: `getParticipantDashboardCertificateConsentState()`, `local_dashboard_certificate_consent_hidden`, Einwilligung lokal verborgen, keine echte Einwilligung, keine Teilnehmerdaten, keine Freigabe, keine Einwilligungs-Abfrage, kein UI-Blocker, kein Login-Zwang – **vorhanden (v26.72b)** |
| `docs/SUPABASE_PARTICIPANT_DASHBOARD_CERTIFICATE_PRIVACY_NOTICE_STATE_TEST.md` | Lokaler Test des vorbereiteten Teilnehmer-Dashboard-Zertifikats-Datenschutz-Hinweis-State: `getParticipantDashboardCertificatePrivacyNoticeState()`, `local_dashboard_certificate_privacy_notice_hidden`, Datenschutz-Hinweis lokal verborgen, kein echter Datenschutz-Hinweis, keine Teilnehmerdaten, keine Zustimmung, keine Hinweis-Anzeige, kein UI-Blocker, kein Login-Zwang – **vorhanden (v26.73b)** |
| `docs/SUPABASE_PARTICIPANT_DASHBOARD_CERTIFICATE_RETENTION_STATE_TEST.md` | Lokaler Test des vorbereiteten Teilnehmer-Dashboard-Zertifikats-Aufbewahrungs- und Lösch-State: `getParticipantDashboardCertificateRetentionState()`, `local_dashboard_certificate_retention_hidden`, Retention lokal verborgen, keine echte Aufbewahrungsfrist, keine echte Löschanforderung, keine Löschbestätigung, keine Anonymisierung, keine Teilnehmerdaten, kein UI-Blocker, kein Login-Zwang – **vorhanden (v26.74b)** |
| `docs/SUPABASE_PARTICIPANT_DASHBOARD_CERTIFICATE_DATA_ACCESS_STATE_TEST.md` | Lokaler Test des vorbereiteten Teilnehmer-Dashboard-Zertifikats-Datenauskunft-State: `getParticipantDashboardCertificateDataAccessState()`, `local_dashboard_certificate_data_access_hidden`, Datenauskunft lokal verborgen, keine echte Datenauskunft, kein echter Datenexport, kein echter Download, keine Teilnehmerdaten, kein UI-Blocker, kein Login-Zwang – **vorhanden (v26.75b)** |
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
