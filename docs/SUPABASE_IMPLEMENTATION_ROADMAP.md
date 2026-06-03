# Accaoui §34a Lern-App – Supabase Umsetzungsreihenfolge (Roadmap)

Stand: v23.5.9  
Zweck: Klare, risikoarme Reihenfolge für die spätere Einführung von Supabase – ohne die aktuell funktionierende Root-App zu destabilisieren.  
Bezug: `docs/CURSOR_MASTER_CONTEXT_ACCAOUI.md`, `docs/QUESTION_DATABASE_PLAN.md`, `docs/SUPABASE_QUESTION_SCHEMA.md`, `docs/SUPABASE_USER_PROGRESS_SCHEMA.md`

---

## 1. Zweck der Roadmap

Diese Roadmap beantwortet **wann** und **in welcher Reihenfolge** Supabase in die Accaoui §34a Lern-App kommt – nicht **wie** jede Zeile SQL lautet (dafür gelten die beiden Schema-Dokumente).

Ziele:

1. **Stabilität** – Schriftliche und mündliche Prüfung, Dashboard und `localStorage` bleiben bis zur bewussten Umschaltung nutzbar.
2. **Nachvollziehbarkeit** – Jede Phase hat klare Abnahme und Rollback (meist: Feature aus, JSON-Dateien bleiben führend).
3. **Rechtssicherheit** – Fragen-Workflow (Roh → Review → Publish) und Datenschutz vor Live-Teilnehmern in der Cloud.
4. **Abstimmung mit App-Roadmap** – v24 (Oral Cleanup), v25 (82 Fragen), v26 (Rechtstexte), v27 (Login/Supabase), v28 (PWA/Store) aus dem Master Context.

---

## 2. Grundsatz: App zuerst stabil, Supabase schrittweise

| Regel | Bedeutung |
|-------|-----------|
| **JSON/JS bleibt Fallback** | `questions.json`, `data/oral-question-bank.js`, `data/oral-sheets-bank.js` bleiben bis Phase 7 die produktive Quelle für alle Nutzer ohne Login. |
| **Kein Big Bang** | Keine Phase darf alle Module gleichzeitig auf Supabase umstellen. |
| **Feature-Flags** | Später z. B. `ACCAOUI_USE_SUPABASE_AUTH`, `ACCAOUI_USE_SUPABASE_PROGRESS` – standardmäßig `false` in Produktion bis Abnahme. |
| **Geschützte Kern-Dateien** | Änderungen an `app.js`, `questions.json`, `data/` nur in freigegebenen Tasks; Preflight + `ACCAOUI_ALLOW_PROTECTED` beachten. |
| **Root ist führend** | Nicht `test/`; keine parallele Logik in Patch-Dateien für Supabase ohne Plan. |
| **Service Role nie im Frontend** | Nur Anon-Key + RLS für Teilnehmer; Admin-Export/Migration serverseitig. |

```txt
Heute:  Browser → JSON/JS + localStorage
Ziel:   Browser → Supabase (Auth, Fragen published, Fortschritt)
         ↘ Fallback JSON/JS wenn Offline oder Flag aus
```

---

## 3. Phase 1: Dokumentation und Datenmodell abgeschlossen

**Status:** abgeschlossen (v23.5.5 – v23.5.9)

| Dokument | Inhalt |
|----------|--------|
| `docs/QUESTION_DATABASE_PLAN.md` | Prozess Rohfragen → Accaoui-Fragen, Review, Export-Idee |
| `docs/WRITTEN_QUESTION_STANDARD.md` | Format schriftlicher Fragen |
| `docs/SUPABASE_QUESTION_SCHEMA.md` | Fragentabellen, Status, RLS-Fragen, Export-Regeln |
| `docs/SUPABASE_USER_PROGRESS_SCHEMA.md` | Profile, Kurse, Fortschritt, Teilnehmerstatus, App-Store-Datenarten |
| `docs/SUPABASE_IMPLEMENTATION_ROADMAP.md` | Diese Umsetzungsreihenfolge |

**Abnahme Phase 1:**

- Tabellen und Felder sind benannt und konsistent zwischen Fragen- und Nutzer-Schema.
- Kein Widerspruch zu IHK-/Musterfragen-Regel und kanonischen 9 Sachgebieten.
- Team kann SQL und App-Tasks daraus ableiten.

**Parallel erlaubt (ohne Supabase):** v23.5.x Fragen-Review in Markdown, v24 Oral Cleanup, v25 Erweiterung `questions.json` – getrennte Cursor-Tasks.

---

## 4. Phase 2: SQL-Schema vorbereiten, aber noch nicht verbinden

**Ziel:** Versionierte Migrationen im Repository, **ohne** dass die Live-App eine Supabase-URL lädt.

| Schritt | Beschreibung |
|---------|--------------|
| 2.1 | Ordner anlegen, z. B. `supabase/migrations/` (nur wenn im Task erlaubt) |
| 2.2 | SQL aus `SUPABASE_QUESTION_SCHEMA.md` und `SUPABASE_USER_PROGRESS_SCHEMA.md` ableiten |
| 2.3 | Enums/Checks für Status (`imported` … `published`, `active` … `blocked`) |
| 2.4 | RLS-Policies als separate Migration oder Kommentarblöcke mit Referenz auf Schema §14/§17 |
| 2.5 | Seed nur für **Entwicklung** (Test-Admin, Test-Kurs) – keine echten Teilnehmerdaten |
| 2.6 | Lokale Prüfung: `supabase db reset` oder SQL-Review – **kein** Eintrag in `index.html` |

**Abnahme Phase 2:**

- Migrationen laufen auf leerer Dev-Datenbank fehlerfrei.
- App im Browser verhält sich **identisch** wie vorher (kein Supabase-Client).

**Nicht in Phase 2:** App-Code, API-Keys in Repo committen (nur `.env.example` mit Platzhaltern).

---

## 5. Phase 3: Supabase-Projekt vorbereiten

**Ziel:** Cloud-Instanz (Dev/Staging), noch ohne Teilnehmer-Massenbetrieb.

| Schritt | Beschreibung |
|---------|--------------|
| 3.1 | Supabase-Projekt anlegen (EU-Region bevorzugt – DSGVO) |
| 3.2 | Migrationen aus Phase 2 auf Dev anwenden |
| 3.3 | Auth-Einstellungen: E-Mail/Passwort (später Magic Link optional) |
| 3.4 | Anon-Key und URL in lokaler `.env` / CI-Secrets – **nicht** in `app.js` hardcoden |
| 3.5 | Storage-Buckets nur wenn nötig (Avatare, Import-PDFs) – RLS auf Buckets |
| 3.6 | Backup- und Zugriffsrichtlinie dokumentieren (wer hat Dashboard-Zugang) |

**Abnahme Phase 3:**

- Tabellen in Dev sichtbar; RLS aktiv (Default-Deny getestet).
- Keine Produktions-Teilnehmer importiert.

---

## 6. Phase 4: Auth / Login planen

**Ziel:** Technisches Konzept und minimale UI – Login optional, App ohne Account weiter nutzbar.

| Schritt | Beschreibung |
|---------|--------------|
| 4.1 | Auth-Flow dokumentieren: Registrierung nur durch Admin vs. Einladungslink |
| 4.2 | Trigger/Function: bei `auth.users` insert → Zeile in `profiles` |
| 4.3 | Session-Handling: `@supabase/supabase-js`, Refresh, Logout |
| 4.4 | UI: Login-Modal oder eigene Seite – **kein** Blockieren des Gastmodus bis Phase 5 |
| 4.5 | Rolle aus `profiles.role` nach Login laden |
| 4.6 | Preflight-Regel: keine sensiblen Tokens in `localStorage` |

**Abnahme Phase 4:**

- Testnutzer kann sich ein- und ausloggen.
- Ohne Login: bestehende Module unverändert (JSON + localStorage).

**Abhängigkeit:** Phase 3 (Dev-Projekt).

---

## 7. Phase 5: Teilnehmer, Kurse, aktiv/inaktiv einbauen

**Ziel:** Zugangssteuerung – nur berechtigte Teilnehmer sehen Lerninhalte nach Login.

| Schritt | Beschreibung |
|---------|--------------|
| 5.1 | Tabellen `courses`, `course_enrollments` befüllen (Admin) |
| 5.2 | App prüft nach Login: `enrollment_status = active`, Kurs aktiv, nicht `expired`/`blocked` |
| 5.3 | UI-Hinweise: „Kurs nicht aktiv“, „Zugang abgelaufen“ |
| 5.4 | Gastmodus: Feature-Flag – entweder weiter alles lokal oder eingeschränkte Demo |
| 5.5 | Admin legt Teilnehmer an / weist Kurs zu (kein Self-Service ohne Freigabe) |

**Abnahme Phase 5:**

- Inaktiver Teilnehmer kann sich einloggen, sieht aber keinen Lerninhalt (klarer Hinweis).
- Aktiver Teilnehmer sieht Dashboard – **Fortschritt noch localStorage** (Phase 6).

**Schema-Referenz:** `SUPABASE_USER_PROGRESS_SCHEMA.md` §6, §15, §17.

---

## 8. Phase 6: Fortschrittsspeicherung – Migration localStorage → Supabase

**Ziel:** Lernfortschritt pro `user_id`; schrittweise Module, nicht alles auf einmal.

**Reihenfolge innerhalb Phase 6:**

| Reihenfolge | Modul | Tabellen | Bisheriger Key |
|-------------|--------|----------|----------------|
| 6.1 | Alle Fragen / beantwortet | `written_question_progress` | `accaoui_answered_questions` |
| 6.2 | Schriftliche Prüfung | `written_exam_attempts`, `written_exam_answers` | `accaoui_exam_history` |
| 6.3 | Statistik / Themen | aus Fortschritt ableiten oder View | `accaoui_topic_stats` |
| 6.4 | Fehlertraining schriftlich | `mistake_history` | `accaoui_topic_mistakes` |
| 6.5 | Lernkarten | `flashcard_progress` | `accaoui_flashcard_progress` |
| 6.6 | Mündliche Prüfung | `oral_exam_attempts`, `oral_exam_answers` | mündliche Keys in Oral-Modul |
| 6.7 | Mündliches Fehlertraining | `oral_mistake_history` | z. B. Oral-Mistake-Keys |

| Schritt | Beschreibung |
|---------|--------------|
| 6.A | Abstraktion `readProgress` / `writeProgress`: Supabase wenn eingeloggt + Flag, sonst localStorage |
| 6.B | Einmal-Migration beim ersten Login: localStorage → Supabase (Opt-in, Konflikt: neuerer Zeitstempel gewinnt) |
| 6.C | Nach erfolgreicher Migration: localStorage für diese Keys leeren oder nur Cache |
| 6.D | Offline: Queue oder Fallback localStorage (später PWA) |

**Abnahme Phase 6:**

- Gleicher Nutzer auf zweitem Gerät sieht Fortschritt nach Login.
- Gast/localStorage-Nutzer ohne Regression.

**Voraussetzung:** v24 Oral Cleanup reduziert Patch-Komplexität vor 6.6–6.7.

---

## 9. Phase 7: Fragenbank – Export aus Supabase oder Laden

**Ziel:** Supabase als **Redaktions- und Freigabe-System**; App weiter über Dateien oder optional API.

**Zwei Betriebsmodi (langfristig):**

| Modus | Beschreibung | Wann |
|-------|--------------|------|
| **A – Export (empfohlen zuerst)** | Tool exportiert nur `published` + `accaoui_original` → `questions.json`, `oral-question-bank.js`, `oral-sheets-bank.js` | Phase 7.1 |
| **B – Live-Laden** | App lädt veröffentlichte Fragen per Supabase Client | Phase 7.2+ |

| Schritt | Beschreibung |
|---------|--------------|
| 7.1 | Export-Skript (tools/, Service Role serverseitig) mit Preflight vor Commit |
| 7.2 | Rohfragen-Import in `raw_questions` (nur Admin, nie Export) |
| 7.3 | Review-Workflow in DB oder weiter Markdown → Eintrag in `written_questions` |
| 7.4 | Optional: App-Feature-Flag „Fragen aus Supabase“ mit JSON-Fallback |
| 7.5 | Cache-Version in `index.html` nur bei Export-Task bumpen |

**Abnahme Phase 7:**

- Export erzeugt valides JSON/JS; Kategorien-Audit und Browser-Test grün.
- Keine Rohfrage in Teilnehmer-App.

**Schema-Referenz:** `SUPABASE_QUESTION_SCHEMA.md` §15–§16.

---

## 10. Phase 8: Admin- und Dozentenbereich vorbereiten

**Ziel:** Interne Verwaltung ohne Teilnehmer-Zugriff auf Rohdaten.

| Bereich | Rolle | Funktionen (geplant) |
|---------|-------|----------------------|
| Fragen | Admin | Import, Status, Publish, Archiv |
| Fragen | Dozent | Review, Kommentar, `needs_review` → `reviewed` |
| Kurse | Admin | Kurse, Einschreibungen, `active`/`blocked` |
| Kurse | Dozent | Teilnehmerliste eigener Kurse, Fortschritt lesen |
| Export | Admin | Export-Job, Versions-Bump |

| Schritt | Beschreibung |
|---------|--------------|
| 8.1 | Separater Admin-Pfad (Subdomain, `/admin`, oder Supabase Studio + spätere kleine UI) |
| 8.2 | Keine Admin-Funktionen in `app.js` Haupt-Dashboard ohne Rolle |
| 8.3 | RLS-Tests: Teilnehmer sieht keine `raw_questions`, kein `question_imports` |

**Abnahme Phase 8:**

- Dozent kann Review schreiben, aber nicht `published` setzen.
- Admin kann Publish und Export auslösen.

**Hinweis:** Kann parallel zu Phase 6/7 beginnen, sobald Phase 3–5 stehen.

---

## 11. Phase 9: Datenschutz, Impressum, Nutzungsbedingungen

**Ziel:** Rechtliche Mindestanforderungen **vor** öffentlichem Login und App Store (Master Context v26).

| Schritt | Beschreibung |
|---------|--------------|
| 9.1 | Impressum |
| 9.2 | Datenschutzerklärung (Supabase, Auth, gespeicherte Fortschrittsdaten – siehe User-Schema §19) |
| 9.3 | Nutzungsbedingungen inkl. Trainingscharakter, keine offizielle IHK-Prüfung |
| 9.4 | Lösch-/Auskunftsprozess (Admin-Workflow zu `profiles` / Fortschritt) |
| 9.5 | Cookie-/Session-Hinweis nur wenn technisch nötig |
| 9.6 | Verknüpfung in `index.html` (eigener Task) |

**Abnahme Phase 9:**

- Nutzer muss vor erstem Login Datenschutz/Nutzung bestätigen können.
- Datenarten aus Roadmap Phase 10 sind in der Datenschutzerklärung benannt.

**Abhängigkeit:** Vor breitem Rollout von Phase 5–6 in Produktion; vor Phase 10 Store.

---

## 12. Phase 10: PWA / App-Store-Vorbereitung

**Ziel:** Installierbare App, Store-Listing (Master Context v28).

| Schritt | Beschreibung |
|---------|--------------|
| 10.1 | PWA: `manifest`, Service Worker, Offline-Strategie (Fragen gecacht, Fortschritt sync) |
| 10.2 | Capacitor optional für native Hülle |
| 10.3 | Google Play Data Safety ← Mapping aus `SUPABASE_USER_PROGRESS_SCHEMA.md` §19 |
| 10.4 | Apple App Privacy Labels |
| 10.5 | Keine neuen Tracker; Supabase-Region und AV-Vertrag dokumentiert |
| 10.6 | Store-Texte: Accaoui Training, nicht IHK-offiziell |

**Abnahme Phase 10:**

- App installierbar; bei Offline klare Grenzen (kein Datenverlust).
- Store-Angaben stimmen mit tatsächlicher Supabase-Nutzung überein.

---

## 13. Risiken

| Risiko | Auswirkung | Gegenmaßnahme |
|--------|------------|----------------|
| Big-Bang-Umstellung | App bricht für alle Nutzer | Phasen + Feature-Flags + JSON-Fallback |
| RLS falsch konfiguriert | Datenleck oder leere App | Policy-Tests pro Rolle; Default-Deny |
| Service Role im Frontend | Vollzugriff auf DB | Nur Server/CI; Code-Review |
| Migration localStorage | Datenverlust | Opt-in, Backup, Zeitstempel-Konfliktregel |
| Oral-Patch-Schichten | Fortschritt mündlich instabil | v24 Cleanup vor Phase 6.6 |
| Fragen-Export fehlerhaft | Falsche Kategorien / JSON kaputt | `audit-categories.py`, Preflight, Browser-Test |
| IHK-1:1-Inhalte in DB | Rechtliches Risiko | Nur `accaoui_original`, Review-Pflicht, Rohfragen intern |
| Supabase-Region USA | DSGVO-Bedenken | EU-Projekt, AVV |
| Geschützte Dateien versehentlich geändert | Unbeabsichtigter Commit | `tools/preflight.py` + `ACCAOUI_ALLOW_PROTECTED` |
| Team arbeitet in `test/` | Falsche Referenz | Master Context: Root führend |
| Rechtstexte fehlen | Store-Ablehnung / Abmahnung | Phase 9 vor Produktions-Login |

---

## 14. Nicht jetzt umsetzen

Folgendes gehört **nicht** zu v23.5.9 und soll erst in der genannten Phase starten:

| Nicht jetzt | Gehört zu |
|-------------|-----------|
| SQL-Dateien anlegen / Migration ausführen | Phase 2–3 (eigener Task) |
| Supabase-URL oder Anon-Key in `index.html` / `app.js` | Phase 4+ |
| Login-Pflicht für alle Nutzer | Phase 5 |
| localStorage entfernen | Phase 6 (erst nach Sync) |
| Live-Fragen nur aus Supabase ohne Export-Test | Phase 7.2 |
| Admin-UI produktiv | Phase 8 |
| Impressum/Datenschutz in App | Phase 9 |
| PWA / Store-Upload | Phase 10 |
| Rohfragen-Massenimport ohne Review | Verboten bis Workflow steht |
| Commits mit `.env` Secrets | Immer verboten |

**Bewusst parallel möglich (ohne Supabase):**

- v24 Oral Exam Cleanup  
- v25 Schriftliche Prüfung / 82-Fragen-Logik in JSON  
- Fragen-Review in `docs/` (Markdown-Blöcke)  
- Preflight- und Kategorie-Audit  

---

## 15. Nächster konkreter technischer Schritt nach dieser Roadmap

**Empfohlener nächster Task (v23.5.10 oder v23.6.0):**

> **SQL-Migrationsentwurf im Repository vorbereiten (Phase 2)** – noch ohne App-Anbindung.

Konkret:

1. Ordner `supabase/migrations/` anlegen (nur wenn im Cursor-Task erlaubt).
2. Erste Migration `001_question_schema.sql` aus `docs/SUPABASE_QUESTION_SCHEMA.md` ableiten.
3. Zweite Migration `002_user_progress_schema.sql` aus `docs/SUPABASE_USER_PROGRESS_SCHEMA.md` ableiten.
4. Dritte Migration `003_rls_policies.sql` – Policies als Kommentar-Checkliste oder ausführbare Policies für Dev.
5. Optional `supabase/README.md` mit Hinweis: Dev-only, keine Keys im Repo.
6. **Keine** Änderung an `app.js`, `index.html`, `questions.json`, `data/`.
7. Abnahme: SQL-Review + manuelles Anwenden auf lokales/ Dev-Supabase-Projekt (Phase 3), App unverändert im Browser testen.

**Alternativ**, wenn SQL noch zurückgestellt wird:

> **Export-Prozess dokumentieren** (`docs/QUESTION_EXPORT_PROCESS.md`) – beschreibt Phase 7.1, Preflight, erlaubte Dateien für Export-Tool – weiterhin ohne App-Code.

**Priorität gegenüber App-Roadmap:**

| Priorität | Task | Begründung |
|-----------|------|------------|
| Hoch | Phase 2 SQL (nächster Supabase-Schritt) | Fundament für alles Weitere |
| Hoch | v24 Oral Cleanup | Reduziert Risiko für Phase 6.6 |
| Mittel | v25 Fragenbank JSON erweitern | Unabhängig von Supabase |
| Mittel | Phase 9 Rechtstexte | Vor Produktions-Login |
| Niedriger | Phase 7.2 Live-Laden | Erst nach Export stabil |

---

## Übersicht: Phasen auf einen Blick

| Phase | Kurzname | App-Verhalten | Supabase |
|-------|----------|---------------|----------|
| 1 | Dokumentation | Unverändert | Keins |
| 2 | SQL vorbereiten | Unverändert | Nur Repo-Migrationen |
| 3 | Projekt Dev | Unverändert | Cloud Dev |
| 4 | Auth planen | Gast + optional Login | Auth + profiles |
| 5 | Kurse/Zugang | Login + Zugangscheck | enrollments |
| 6 | Fortschritt | Sync + Fallback | Fortschrittstabellen |
| 7 | Fragenbank | Export oder API | Fragen + Export |
| 8 | Admin/Dozent | Zusatz-UI | Reviews, Verwaltung |
| 9 | Recht | Footer/Consent | AVV/Doku |
| 10 | PWA/Store | Installierbar | wie Phase 6–7 |

---

## Anhang – Dokumentenindex

| Datei | Rolle in Roadmap |
|-------|------------------|
| `docs/CURSOR_MASTER_CONTEXT_ACCAOUI.md` | Gesamtziele, v24–v28, IHK-Regel, Preflight |
| `docs/QUESTION_DATABASE_PLAN.md` | Review-Prozess, localStorage-Übergang |
| `docs/SUPABASE_QUESTION_SCHEMA.md` | Phase 7, 8 (Fragen) |
| `docs/SUPABASE_USER_PROGRESS_SCHEMA.md` | Phase 4–6, 9–10 |
| `docs/SUPABASE_IMPLEMENTATION_ROADMAP.md` | Diese Reihenfolge (v23.5.9) |

Diese Roadmap ist die verbindliche Umsetzungsreihenfolge für Supabase in der Accaoui §34a Lern-App, bis ein späterer Task sie durch Versionierung oder Checklisten ersetzt.
