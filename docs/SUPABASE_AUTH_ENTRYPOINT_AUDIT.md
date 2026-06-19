# Accaoui §34a Lern-App – Auth-Einstiegspunkt-Audit

Stand: v26.3e

Ziel: Prüfen, wo Supabase/Login später sauber in den bestehenden App-Start eingebunden werden kann, ohne die stabile lokale App-Logik zu beschädigen.

## 1. Aktueller Einstieg

Die App startet aktuell direkt in app.js über DOMContentLoaded.

Aktuelle Reihenfolge:

1. App-Version ausgeben
2. registerActiveSessionAutoSaveListeners()
3. loadAllLocalData()
4. activateDashboardButtons()
5. renderDashboardResumeExamCard()
6. renderDashboardResumeLearningCard()
7. loadQuestions()

Danach lädt loadQuestions die questions.json, normalisiert die Fragen, baut die Kategorie-Karten und aktualisiert die Dashboard-Zahlen.

## 2. Aktuelle HTML-Struktur

index.html enthält aktuell die bestehende Layout-Struktur mit:

1. aside.sidebar
2. main.main-content
3. header.topbar
4. hero-grid
5. Dashboard-Karten

Es gibt aktuell keinen separaten Login-Container und keinen Auth-State im HTML.

## 3. Aktuelle Navigation

Mehrere Zurück-/Dashboard-Buttons nutzen location.reload().

Das ist aktuell akzeptabel, weil die App lokal ohne Login läuft.

Bei späterer Auth-Einbindung bedeutet das:
Jeder Reload muss zuerst wieder durch die Auth-Prüfung laufen.

## 4. Risiko bei falscher Einbindung

Login darf später nicht nachträglich innerhalb einzelner Lernmodule eingebaut werden.

Risiken:

1. Fragen würden vor Zugangskontrolle geladen
2. Dashboard wäre kurz sichtbar, obwohl kein gültiger Zugang besteht
3. Reload könnte gesperrte Teilnehmer zurück ins Dashboard bringen
4. bestehende Pause-/Fortsetzen-Logik könnte beschädigt werden

## 5. Empfohlener Ziel-Einstieg

Spätere Zielstruktur:

1. DOMContentLoaded
2. initAppBoot()
3. initAuthFlow()
4. bei gültigem Zugang: startLocalApp()
5. bei ungültigem Zugang: renderLoginOrAccessNotice()

Die bisherige Startlogik wird später in startLocalApp() verschoben.

## 6. Geplante Funktionen später

Mögliche spätere Funktionen:

1. initAppBoot()
2. initAuthFlow()
3. startLocalApp()
4. renderLoginScreen()
5. renderAccessExpiredScreen()
6. renderAccessBlockedScreen()
7. renderNoCourseScreen()
8. getCurrentAccessState()

## 7. Entscheidung für nächsten Code-Schritt

Vor echter Supabase-Verbindung kann zunächst ein lokaler Auth-Guard vorbereitet werden.

Empfehlung:

1. kein Supabase-Key in v26.3e
2. keine echte API-Verbindung in v26.3e
3. zuerst nur Einstiegspunkt dokumentieren
4. danach optional lokales Auth-Guard-Gerüst ohne echte Verbindung vorbereiten

## 8. Status

Status v26.3e: Code-Einstiegspunkte geprüft und dokumentiert. Noch kein App-Code geändert.
