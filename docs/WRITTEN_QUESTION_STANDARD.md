# Accaoui §34a Lern-App – Standard für schriftliche Fragen

Stand: v23.5.3 Vorbereitung
Zweck: Einheitlicher Aufbau für alle neuen schriftlichen Fragen in der Accaoui §34a Lern-App.

## 1. Grundprinzip

Alle neuen schriftlichen Fragen sollen sich an der Struktur einer typischen Sachkundeprüfung orientieren:

1. Frage-Nummer oder eindeutige ID
2. Kategorie / Sachgebiet
3. Fragetext
4. mögliche Punktzahl
5. Antwortoptionen a–d oder a–e
6. richtige Antwort oder richtige Antworten
7. kurze Erklärung für den Lernmodus
8. Schwierigkeit
9. Prüfungsrelevanz

Die hochgeladene Musterprüfung dient nur als Strukturvorbild. Die Fragen werden nicht 1:1 kopiert, sondern als eigene Accaoui-Fragen formuliert.

## 2. Zulässige Punktzahl

Jede schriftliche Frage hat eine Punktzahl:

1. 1 Punkt
2. 2 Punkte

Regel:

1. Eine 1-Punkt-Frage hat in der Regel eine richtige Antwort.
2. Eine 2-Punkte-Frage hat in der Regel zwei richtige Antworten.
3. Es sollen maximal 1–2 richtige Antworten verwendet werden.

## 3. Antwortoptionen

Antwortoptionen werden immer klar mit Buchstaben gekennzeichnet:

1. a)
2. b)
3. c)
4. d)
5. optional e)

Standard:

1. Normale Fragen: a–d
2. Kombinationsfragen: häufig a–e

## 4. Fragetyp 1: einfache Auswahlfrage

Beispiel-Struktur:

Frage:
Welche Aussage zur Erlaubnis nach § 34a GewO ist richtig?

Mögliche Punktzahl: 1

a) Die Erlaubnis wird automatisch durch die IHK erteilt.
b) Die Erlaubnis wird von der zuständigen Behörde geprüft und erteilt.
c) Die Erlaubnis ist nur für Mitarbeiter im Objektschutz erforderlich.
d) Die Erlaubnis ersetzt die Zuverlässigkeitsprüfung.

Richtige Antwort: b

Erklärung:
Die Erlaubnis nach § 34a GewO wird durch die zuständige Behörde geprüft und erteilt. Die IHK ist für Unterrichtung und Sachkundeprüfung zuständig, nicht für die Gewerbeerlaubnis.

## 5. Fragetyp 2: Kombinationsfrage

Beispiel-Struktur:

Frage:
Welche Aussagen zum Hausrecht sind richtig?

1. Das Hausrecht erlaubt dem Berechtigten, den Zutritt zu Räumen oder Grundstücken zu regeln.
2. Ein Sicherheitsmitarbeiter darf auf Grundlage des Hausrechts immer Personen durchsuchen.
3. Ein Hausverbot kann im Auftrag des Hausrechtsinhabers ausgesprochen werden.
4. Das Hausrecht ersetzt polizeiliche Befugnisse.

Mögliche Punktzahl: 1

a) Nur die Aussagen 1 und 2 sind richtig.
b) Nur die Aussagen 1 und 3 sind richtig.
c) Nur die Aussagen 2 und 4 sind richtig.
d) Nur die Aussagen 3 und 4 sind richtig.
e) Alle Aussagen sind richtig.

Richtige Antwort: b

Erklärung:
Das Hausrecht ermöglicht Regelungen zu Zutritt und Aufenthalt. Ein Sicherheitsmitarbeiter kann im Auftrag des Hausrechtsinhabers handeln. Es erlaubt jedoch nicht automatisch Durchsuchungen und ersetzt keine polizeilichen Befugnisse.

## 6. Pflichtfelder für neue schriftliche Fragen

Jede neue schriftliche Frage soll intern diese Felder haben:

1. id
2. category
3. question
4. points
5. answers
6. correctAnswers
7. explanation
8. difficulty
9. examRelevance

## 7. Beispiel im App-Format

```js
{
  id: "q_083",
  category: "Gewerberecht",
  question: "Welche Aussage zur Erlaubnis nach § 34a GewO ist richtig?",
  points: 1,
  answers: [
    { id: "a", text: "Die Erlaubnis wird automatisch durch die IHK erteilt." },
    { id: "b", text: "Die Erlaubnis wird von der zuständigen Behörde geprüft und erteilt." },
    { id: "c", text: "Die Erlaubnis ist nur für Mitarbeiter im Objektschutz erforderlich." },
    { id: "d", text: "Die Erlaubnis ersetzt die Zuverlässigkeitsprüfung." }
  ],
  correctAnswers: ["b"],
  explanation: "Die Erlaubnis nach § 34a GewO wird durch die zuständige Behörde geprüft und erteilt. Die IHK ist für Unterrichtung und Sachkundeprüfung zuständig, nicht für die Gewerbeerlaubnis.",
  difficulty: "mittel",
  examRelevance: "hoch"
}
```

## 8. Kanonische Kategorien

Neue schriftliche Fragen dürfen nur diesen Kategorien zugeordnet werden:

1. Recht der öffentlichen Sicherheit und Ordnung
2. Gewerberecht
3. Datenschutzrecht
4. Bürgerliches Gesetzbuch
5. Strafgesetzbuch und Strafverfahrensrecht
6. Unfallverhütungsvorschriften Wach- und Sicherungsdienste
7. Umgang mit Waffen
8. Umgang mit Menschen
9. Grundzüge der Sicherheitstechnik

## 9. Fachliche Qualitätsregeln

Jede neue Frage muss vor dem Einbau geprüft werden:

1. Ist die Kategorie korrekt?
2. Ist die Frage eindeutig?
3. Gibt es keine doppeldeutige richtige Antwort?
4. Stimmen Punktzahl und Anzahl richtiger Antworten zusammen?
5. Ist die Erklärung fachlich korrekt?
6. Ist die Formulierung verständlich?
7. Ist die Frage prüfungsnah, aber nicht 1:1 kopiert?
8. Enthält die Frage keine veralteten Begriffe?
9. Gibt es keine Dublette zu bestehenden Fragen?

## 10. Rechtliche Schutzregel

Offizielle oder fremde Prüfungsfragen dürfen nicht 1:1 übernommen werden.

Erlaubt:

1. Struktur als Vorbild nutzen
2. eigene Accaoui-Fragen formulieren
3. typische Prüfungssituationen nachbilden
4. fachliche Lernziele übernehmen

Nicht erlaubt:

1. komplette fremde Fragen kopieren
2. komplette Antwortoptionen übernehmen
3. offizielle Prüfungsbögen als eigene Fragenbank ausgeben
4. IHK-Fragen als Accaoui-eigene Inhalte kennzeichnen

## 11. Import-Regel

Neue Fragen werden nicht direkt massenhaft in questions.json eingefügt.

Ablauf:

1. 10 Fragen als Testblock erstellen
2. fachlich prüfen
3. Dubletten prüfen
4. Format prüfen
5. Preflight ausführen
6. Browser-Test machen
7. erst danach erweitern

## 12. Ziel

Die schriftliche Fragenbank soll prüfungsnah, klar, rechtlich sauber und didaktisch stärker sein als eine reine Sammlung von Musterfragen.

Die App soll nicht nur richtige Antworten abfragen, sondern durch Erklärungen echtes Verständnis aufbauen.
