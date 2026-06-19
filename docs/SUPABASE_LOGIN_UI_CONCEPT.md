# Accaoui §34a Lern-App – Login-UI-Konzept

Stand: v26.3c

Ziel: Vor der echten Supabase-Anbindung wird festgelegt, wie Login, Kurszugang und Sperrhinweise in der App aussehen sollen.

---

## 1. Aktueller App-Einstieg

Die App startet aktuell direkt in `app.js` über `DOMContentLoaded`.

Aktueller Ablauf:

1. lokale Daten laden
2. Dashboard-Buttons aktivieren
3. Fragen laden
4. Dashboard anzeigen

Es gibt noch keinen Auth-State und keine Login-Seite.

---

## 2. Ziel-Ablauf später

Nach Supabase-Einbindung soll der Ablauf so sein:

1. App startet
2. Auth-Status prüfen
3. nicht eingeloggt → Login-Seite anzeigen
4. eingeloggt → Teilnehmerprofil laden
5. Kurszugang prüfen
6. gültiger Zugang → Dashboard anzeigen
7. ungültiger Zugang → Hinweis-/Sperrseite anzeigen

---

## 3. Login-Seite

Die Login-Seite soll klar, seriös und einfach sein.

Elemente:

1. Accaoui Bildung Logo
2. Titel: Teilnehmer-Login
3. Hinweis: Zugang nur für freigeschaltete Kursteilnehmer
4. E-Mail-Feld
5. Passwort-Feld
6. Button: Einloggen
7. Hinweis bei Fehlern

Beispieltext:

Teilnehmer-Login
Melden Sie sich mit Ihren Zugangsdaten an. Der Zugriff ist nur mit aktivem Kurs möglich.

---

## 4. Gültiger Zugang

Wenn der Teilnehmer gültig ist:

1. Dashboard anzeigen
2. Kursname anzeigen
3. Ablaufdatum anzeigen
4. Lernmodule freigeben

Beispiel:

Willkommen zurück.
Ihr Kurszugang ist aktiv bis: TT.MM.JJJJ

---

## 5. Kein aktiver Kurs

Wenn kein aktiver Kurs vorhanden ist:

Ihrem Konto ist aktuell kein aktiver Kurs zugeordnet.
Bitte wenden Sie sich an Accaoui Bildung.

---

## 6. Abgelaufener Kurs

Wenn der Kurs oder Teilnehmerzugang abgelaufen ist:

Ihr Kurszugang ist abgelaufen.
Bitte wenden Sie sich an Accaoui Bildung.

---

## 7. Gesperrter Zugang

Wenn enrollment_status = blocked:

Ihr Zugang ist aktuell gesperrt.
Bitte wenden Sie sich an die Verwaltung.

---

## 8. Technischer Hook später

Die Login-Logik soll später vor dem bisherigen Dashboard-Start laufen.

Geplanter Einstieg:

1. `DOMContentLoaded`
2. `initAuthFlow()`
3. bei gültigem Zugang: bisherige App-Initialisierung starten
4. bei ungültigem Zugang: Login- oder Sperrseite rendern

Wichtig: Die bestehende App-Logik soll nicht direkt zerstört werden.

---

## 9. Nicht in v26.3c

Noch nicht umsetzen:

1. Supabase-Key einbauen
2. echte Verbindung herstellen
3. echte Tabellen abfragen
4. Passwort-Reset
5. Adminbereich
6. Dozentenbereich

Status v26.3c: UI-Konzept erstellt, noch kein App-Code geändert.
