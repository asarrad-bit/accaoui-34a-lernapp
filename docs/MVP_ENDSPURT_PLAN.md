# Accaoui §34a Lern-App – MVP-Endspurt-Plan

Stand: v27.19a  
Ziel: Web-App MVP sauber, stabil und nutzbar fertigstellen.

---

## 1. MVP-Ziel

Die erste produktiv nutzbare Web-Version soll:

- Lernen ermöglichen
- Prüfungssimulation ermöglichen
- Ergebnisse speichern
- Teilnehmer-Login ermöglichen
- Teilnehmer-Dashboard anzeigen
- Dozent/Admin-Grundansicht ermöglichen
- Zertifikat/Bestätigung vorbereiten
- Online stabil laufen

---

## 2. Nicht-MVP / wird geparkt

Für den MVP werden vorerst geparkt:

- weitere Detail-Status-States
- App Store / Google Play Verpackung
- große Admin-Sonderfunktionen
- komplexe Automationen
- perfekte Design-Extras
- Spezialfälle ohne direkten Nutzen für Teilnehmer

---

## 3. Qualitätsregel

Kein Schnellbau auf Kosten der Qualität.

Jeder Schritt braucht:

- Git sauber
- Helper/Preflight sauber
- Browser-Test
- klaren Commit
- GitHub-Prüfung
- keine echten Keys im Repo
- keine Teilnehmerdaten im Code
- keine unsichere Live-Verbindung

---

## 4. Endspurt-Reihenfolge

### Phase 1 – Supabase live vorbereiten
- echte Supabase-Projektstruktur festlegen
- Tabellen planen
- RLS/Sicherheitsregeln planen
- Env/Config sauber trennen

### Phase 2 – Login aktivieren
- Teilnehmer-Login
- Session-Erkennung
- Logout
- lokale Fallback-Sicherheit

### Phase 3 – Teilnehmerdaten speichern
- Teilnehmerprofil
- Kursstatus
- Laufzeit/Enddatum
- Zugriff erlaubt/gesperrt

### Phase 4 – Prüfungsergebnisse speichern
- Simulationsergebnis speichern
- Punkte speichern
- bestanden/nicht bestanden speichern
- Verlauf anzeigen

### Phase 5 – Dashboard nutzbar machen
- Fortschritt
- Ergebnisse
- Zertifikat/Bestätigung
- Hinweise
- Support/Dozent-Kontakt

### Phase 6 – Admin/Dozent-Grundansicht
- Teilnehmerliste
- Kursstatus
- Prüfungsergebnisse
- Zertifikatsstatus

### Phase 7 – Stabilisierung
- Fehlerprüfung
- Ladezeit prüfen
- Mobile Ansicht prüfen
- Datenschutz/Impressum prüfen
- Online-Test

---

## 5. MVP-Definition fertig

Der MVP gilt als fertig, wenn:

- ein Teilnehmer sich anmelden kann
- Lernen/Simulation nutzbar ist
- Ergebnis gespeichert wird
- Dashboard relevante Daten zeigt
- Admin/Dozent Grunddaten sehen kann
- keine Sicherheitslücke offensichtlich ist
- GitHub und lokale Version übereinstimmen
- App online testbar ist

---

## 6. Empfehlung

Ab v27.20 beginnt der MVP-Fertigstellungsmodus.

Status: erledigt
