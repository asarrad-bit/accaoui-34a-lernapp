# Accaoui §34a Lern-App – Supabase MVP Tabellenplan

Stand: v27.20a  
Status: Planungsdokument, keine Live-Anbindung, keine echten Keys.

---

## 1. Ziel

Für den MVP braucht die App eine klare, sichere Supabase-Datenstruktur.

Der MVP soll speichern können:

- Teilnehmer
- Kurse
- Teilnehmer-Kurs-Zuordnung
- Prüfungsergebnisse
- Zertifikats-/Bestätigungsstatus
- Admin-/Dozent-Grundzugriff
- einfache Änderungs-/Audit-Historie

---

## 2. Sicherheitsgrundsatz

Keine sensiblen Daten im Frontend-Code.

Für Supabase gilt:

- keine Service-Role-Keys im Repo
- RLS aktivieren
- Teilnehmer sehen nur eigene Daten
- Admin/Dozent sieht nur notwendige Teilnehmerdaten
- Schreibrechte klar begrenzen
- lokale App bleibt ohne Live-Zwang startbar

---

## 3. MVP-Tabellen

### 3.1 participants

Zweck: Teilnehmer-Stammdaten.

Felder:

- id
- auth_user_id
- first_name
- last_name
- email
- phone
- status
- created_at
- updated_at

Status-Beispiele:

- active
- blocked
- expired
- completed

---

### 3.2 courses

Zweck: Kursarten und Kursdaten.

Felder:

- id
- title
- course_type
- start_date
- end_date
- status
- created_at
- updated_at

course_type-Beispiele:

- sachkunde_34a
- grosser_schein
- intensiv_10_tage
- drei_monate
- sechs_monate

---

### 3.3 enrollments

Zweck: Verbindung Teilnehmer zu Kurs.

Felder:

- id
- participant_id
- course_id
- access_starts_at
- access_ends_at
- access_status
- created_at
- updated_at

access_status-Beispiele:

- allowed
- blocked
- expired
- completed

---

### 3.4 exam_attempts

Zweck: Prüfungssimulationen speichern.

Felder:

- id
- participant_id
- course_id
- mode
- score_points
- max_points
- passed
- started_at
- finished_at
- created_at

mode-Beispiele:

- full_simulation
- training
- category_test
- repeat_mistakes

---

### 3.5 exam_answers

Zweck: Einzelantworten einer Prüfung speichern.

Felder:

- id
- exam_attempt_id
- question_id
- selected_answers
- correct_answers
- earned_points
- max_points
- is_correct
- created_at

---

### 3.6 certificates

Zweck: Zertifikat/Bestätigung vorbereiten.

Felder:

- id
- participant_id
- course_id
- certificate_type
- status
- issued_at
- revoked_at
- created_at
- updated_at

status-Beispiele:

- prepared
- issued
- blocked
- revoked

---

### 3.7 admin_profiles

Zweck: Admin-/Dozent-Grundrollen.

Felder:

- id
- auth_user_id
- display_name
- role
- status
- created_at
- updated_at

role-Beispiele:

- admin
- dozent
- support

---

### 3.8 audit_logs

Zweck: einfache Nachvollziehbarkeit wichtiger Aktionen.

Felder:

- id
- actor_user_id
- action
- target_table
- target_id
- metadata
- created_at

---

## 4. RLS-Grundregeln

### Teilnehmer

Teilnehmer dürfen:

- eigene Profilbasis lesen
- eigene Kurszuordnung lesen
- eigene Prüfungsergebnisse lesen
- eigene Prüfungsergebnisse erstellen
- eigene Zertifikatsstatus lesen

Teilnehmer dürfen nicht:

- andere Teilnehmer sehen
- Admin-Daten sehen
- Zertifikate selbst freigeben
- Kurslaufzeiten ändern

---

### Admin/Dozent

Admin/Dozent darf:

- Teilnehmerliste lesen
- Kursstatus lesen
- Prüfungsergebnisse lesen
- Zertifikatsstatus prüfen
- Teilnehmerstatus verwalten

Admin/Dozent darf nicht:

- Supabase-Sicherheitsregeln umgehen
- Service-Role-Key im Frontend nutzen
- unnötige sensible Daten exportieren

---

## 5. MVP-Reihenfolge

1. Tabellen final bestätigen
2. SQL-Migration vorbereiten
3. RLS-Regeln vorbereiten
4. lokale Adapter-Funktionen an echte Tabellen mappen
5. Login aktivieren
6. Ergebnis-Speicherung aktivieren
7. Dashboard-Daten live lesen
8. Admin-Grundansicht anbinden

---

## 6. Qualitätsentscheidung

Dieser Plan ersetzt die weitere lange Detail-Status-State-Kette.

Ab jetzt Fokus:

- echte Datenstruktur
- echte Speicherung
- echter MVP-Nutzen
- weiterhin sichere lokale Fallbacks

Status: erledigt
