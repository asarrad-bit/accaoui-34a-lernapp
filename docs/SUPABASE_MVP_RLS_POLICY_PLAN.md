# Accaoui §34a Lern-App – Supabase MVP RLS-Policy-Plan

Stand: v27.28d
Status: Planungsdokument, keine Live-Ausführung, keine echten Keys.

---

## 1. Ziel

Dieser Plan beschreibt die Row-Level-Security-Regeln für den MVP.

Grundsatz:

- Teilnehmer sehen nur eigene Daten.
- Admin/Dozent sieht nur notwendige Daten.
- Service-Role-Key bleibt niemals im Frontend.
- Lokaler Modus bleibt ohne Live-Zwang startbar.

---

## 2. Identitätsbasis

Supabase Auth liefert:

- auth.uid()

Mapping:

- participants.auth_user_id = auth.uid()
- admin_profiles.auth_user_id = auth.uid()

Admin-/Dozent-Prüfung erfolgt später über:

- admin_profiles.role
- admin_profiles.status = active

---

## 3. Teilnehmer-Regeln

### participants

Teilnehmer darf:

- eigenes Profil lesen
- eigenes Profil begrenzt aktualisieren

Teilnehmer darf nicht:

- andere Teilnehmer lesen
- eigenen Status selbst auf active setzen
- andere Profile ändern

---

### enrollments

Teilnehmer darf:

- eigene Kurszuordnung lesen
- eigenen access_status lesen
- eigenes access_ends_at lesen

Teilnehmer darf nicht:

- Kurslaufzeit ändern
- Zugriff selbst verlängern
- fremde Kurszuordnungen lesen

---

### exam_attempts

Teilnehmer darf:

- eigene Prüfungsergebnisse lesen
- eigene Prüfungsergebnisse ausschließlich über geprüfte RPCs erzeugen

Teilnehmer darf nicht:

- fremde Ergebnisse lesen
- fremde Ergebnisse ändern
- alte Ergebnisse manipulieren

---

### exam_answers

Teilnehmer darf:

- eigene Antworten über eigene exam_attempts lesen
- eigene Antworten ausschließlich über geprüfte RPCs speichern

Teilnehmer darf nicht:

- fremde Antworten lesen
- fremde Antworten ändern

---

### certificates

Teilnehmer darf:

- eigenen Zertifikats-/Bestätigungsstatus lesen

Teilnehmer darf nicht:

- Zertifikate selbst ausstellen
- Zertifikate selbst sperren
- Zertifikate selbst widerrufen

---

## 4. Admin-/Dozent-Regeln

Admin/Dozent darf:

- Teilnehmerliste lesen
- Kurszuordnungen lesen
- Prüfungsergebnisse lesen
- Zertifikatsstatus lesen
- Teilnehmerstatus verwalten

Admin/Dozent darf nur aktiv sein, wenn:

- admin_profiles.auth_user_id = auth.uid()
- admin_profiles.status = active
- role in admin, dozent, support

---

## 5. Tabellen-Policy-Übersicht

| Tabelle | Teilnehmer lesen | Teilnehmer schreiben | Admin/Dozent lesen | Admin/Dozent schreiben |
|---|---:|---:|---:|---:|
| participants | eigene Daten | begrenzt | ja | ja |
| courses | aktive Kurse | nein | ja | ja |
| enrollments | eigene Daten | nein | ja | ja |
| exam_attempts | eigene Daten | nur über RPC | ja | nur über geprüfte RPCs |
| exam_answers | eigene Daten | nur über RPC | ja | nur über geprüfte RPCs |
| certificates | eigene Daten | nein | ja | ja |
| admin_profiles | nein | nein | eigene Rolle | admin |
| audit_logs | nein | automatisch | ja | automatisch |

---

## 6. Aktueller Sicherheits-Override v27.28d

Die ursprüngliche MVP-Planung wurde nach dem
Prüfungsintegritätsreview verschärft.

Für `exam_attempts` und `exam_answers` gilt jetzt:

- keine App-Rolle besitzt direkte Schreibrechte
- Teilnehmer schreiben ausschließlich über Prüfungs-RPCs
- Admin, Dozent und Support schreiben nicht direkt in die Tabellen
- Support besitzt nur den erforderlichen Lesezugriff
- administrative Korrekturen benötigen später einen eigenen
  geprüften und protokollierten Admin-RPC
- die alten Mitarbeiter-Policies mit `FOR ALL` wurden entfernt

## 7. Sicherheitsrisiken

Besonders kritisch:

- falsche participant_id-Prüfung
- offene select policies
- zu breite update policies
- Zertifikatsfreigabe durch Teilnehmer
- Service-Role-Key im Frontend
- Admin-Rolle ohne status active

---

## 8. MVP-Policy-Reihenfolge

1. Admin-Helper-Funktion planen
2. Teilnehmer-Select-Policies planen
3. Teilnehmer-Insert-Policies für Prüfungsergebnisse planen
4. Admin-/Dozent-Policies planen
5. Zertifikats-Schreibrechte absichern
6. Audit-Logs nur serverseitig/administrativ vorbereiten
7. SQL-RLS-Migration separat erstellen

---

## 9. Qualitätsentscheidung

Keine Policy wird live genutzt, bevor sie geprüft ist.

Nächster technischer Schritt:

- SQL-RLS-Migration vorbereiten
- keine Live-Ausführung
- keine echten Teilnehmerdaten

Status: erledigt
