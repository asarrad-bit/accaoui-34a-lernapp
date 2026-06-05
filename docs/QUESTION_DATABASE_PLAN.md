# Accaoui §34a Lern-App – Fragen-Datenbank-Plan

Stand: v23.5.4 Vorbereitung
Zweck: Professioneller Plan für Import, Prüfung, Freigabe und spätere Datenbanknutzung von schriftlichen und mündlichen Fragen.

## 1. Ziel

Die Accaoui §34a Lern-App soll langfristig nicht nur mit festen JSON-Dateien arbeiten, sondern mit einer sauberen Fragen-Datenbank.

Ziel ist:

1. schriftliche Fragen professionell verwalten
2. mündliche Fragen professionell verwalten
3. Rohfragen getrennt von veröffentlichten Accaoui-Fragen halten
4. keine offiziellen oder fremden Fragen 1:1 übernehmen
5. jede Frage fachlich prüfen
6. Dubletten vermeiden
7. später Supabase, Login und Teilnehmerfortschritt anbinden

## 2. Grundregel

Es gibt zwei Ebenen:

1. Rohmaterial
2. veröffentlichbare Accaoui-Fragen

Rohmaterial darf nur intern zur Analyse genutzt werden.

Veröffentlicht werden dürfen nur eigene Accaoui-Fragen, die fachlich geprüft, umformuliert und freigegeben wurden.

## 3. Nicht erlaubt

Nicht erlaubt ist:

1. offizielle IHK-Fragen 1:1 übernehmen
2. fremde Musterfragen 1:1 übernehmen
3. gleiche Antwortoptionen 1:1 übernehmen
4. gleiche Reihenfolge übernehmen
5. IHK-Logos oder offizielle Bezeichnungen verwenden
6. die App als offizielle IHK-App darstellen
7. „Original IHK Prüfung“ oder ähnliche Formulierungen verwenden

## 4. Erlaubt

Erlaubt ist:

1. Sachgebiete als Orientierung nutzen
2. Prüfungsstruktur als Orientierung nutzen
3. Lernziele erkennen
4. eigene Accaoui-Fragen formulieren
5. eigene Antwortoptionen erstellen
6. eigene Erklärungen schreiben
7. eigene Trainingsbewertung nutzen

## 5. Tabellen-Idee für Supabase

Später können folgende Tabellen entstehen:

1. question_sources
2. raw_questions
3. written_questions
4. oral_questions
5. question_reviews
6. question_versions
7. courses
8. profiles
9. enrollments
10. user_question_progress
11. user_oral_progress
12. exam_attempts
13. mistake_history

## 6. Tabelle: question_sources

Zweck:
Speichert Quellen, aus denen Lernziele oder Strukturen analysiert wurden.

Mögliche Felder:

1. id
2. source_title
3. source_type
4. source_note
5. uploaded_at
6. imported_by
7. usage_allowed
8. copyright_note

Beispiel:
Eine hochgeladene Musterprüfung wird hier nur als Analysequelle dokumentiert, nicht als veröffentlichbare Fragenbank.

## 7. Tabelle: raw_questions

Zweck:
Speichert interne Rohfragen oder analysierte Ausgangsfragen.

Wichtig:
Diese Tabelle ist nicht für Veröffentlichung gedacht.

Mögliche Felder:

1. id
2. source_id
3. original_question_number
4. mode
5. topic
6. raw_question_text
7. raw_answers
8. raw_correct_answer
9. points
10. question_type
11. similarity_risk
12. status
13. notes

Status:
imported, needs_review, rewrite_required, archived

## 8. Tabelle: written_questions

Zweck:
Speichert eigene geprüfte schriftliche Accaoui-Fragen.

Mögliche Felder:

1. id
2. mode
3. topic
4. subtopic
5. question_type
6. points
7. difficulty
8. exam_relevance
9. ihk_similarity_risk
10. source_style
11. question
12. answers
13. correct
14. explanation
15. status
16. created_at
17. updated_at
18. reviewed_by
19. published_at

Pflicht:
source_style muss accaoui_original sein.

## 9. Tabelle: oral_questions

Zweck:
Speichert eigene geprüfte mündliche Accaoui-Fragen.

Mögliche Felder:

1. id
2. mode
3. topic
4. subtopic
5. examiner_question
6. model_answer
7. follow_up_questions
8. examiner_notes
9. critical_mistakes
10. difficulty
11. exam_relevance
12. ihk_similarity_risk
13. source_style
14. status
15. created_at
16. updated_at
17. reviewed_by
18. published_at

## 10. Tabelle: question_reviews

Zweck:
Dokumentiert die Prüfung einer Frage.

Mögliche Felder:

1. id
2. question_id
3. question_mode
4. review_step
5. review_status
6. reviewer_note
7. reviewed_by
8. reviewed_at

Review-Schritte:

1. fachlich geprüft
2. Dubletten geprüft
3. IHK-Ähnlichkeitsrisiko geprüft
4. Formulierung geprüft
5. Antwortlogik geprüft
6. Erklärung geprüft
7. Freigabe geprüft

## 11. Status-System

Jede Frage bekommt einen Status:

1. imported
2. needs_review
3. rewrite_required
4. reviewed
5. approved
6. published
7. archived

Nur Fragen mit Status published dürfen in der App sichtbar sein.

## 12. Schriftliche Fragen – Qualitätsregeln

Jede schriftliche Frage muss geprüft werden auf:

1. richtige Kategorie
2. eindeutige Fragestellung
3. passende Punktzahl
4. maximal 1–2 richtige Antworten
5. klare Antwortoptionen a–d oder a–e
6. keine doppeldeutige Lösung
7. verständliche Erklärung
8. keine 1:1-Kopie
9. keine veralteten Begriffe
10. prüfungsnahe, aber eigene Accaoui-Formulierung

## 13. Mündliche Fragen – Qualitätsregeln

Jede mündliche Frage muss geprüft werden auf:

1. realistische Prüferfrage
2. klare Musterantwort
3. typische Folgefragen
4. kritische Fehler
5. passendes Sachgebiet
6. passende Schwierigkeit
7. hohe Prüfungsrelevanz
8. keine 1:1-Kopie
9. klare rechtliche Begründung, wenn nötig
10. verständliche Sprache für Teilnehmer

## 14. Kanonische Sachgebiete

Alle Fragen müssen einem dieser 9 Sachgebiete zugeordnet werden:

1. Recht der öffentlichen Sicherheit und Ordnung
2. Gewerberecht
3. Datenschutzrecht
4. Bürgerliches Gesetzbuch
5. Strafgesetzbuch und Strafverfahrensrecht
6. Unfallverhütungsvorschriften Wach- und Sicherungsdienste
7. Umgang mit Waffen
8. Umgang mit Menschen
9. Grundzüge der Sicherheitstechnik

## 15. Review-Prozess

Ablauf für neue Fragen:

1. Quelle erfassen
2. Rohfrage analysieren
3. Lernziel bestimmen
4. Frage neu als Accaoui-Frage formulieren
5. Antwortoptionen neu erstellen
6. richtige Antwort festlegen
7. Erklärung schreiben
8. Kategorie und Punktzahl prüfen
9. IHK-Ähnlichkeitsrisiko prüfen
10. Status auf reviewed setzen
11. nach Endprüfung auf approved setzen
12. erst danach published

## 16. Aktueller Zwischenstand Review-Blöcke

Bereits vorbereitet:

1. QUESTION_REVIEW_BLOCK_01.md
   Fragen 1–12
   Öffentliches Recht und Gewerberecht

2. QUESTION_REVIEW_BLOCK_02.md
   Fragen 13–30
   Datenschutzrecht und Bürgerliches Gesetzbuch

3. QUESTION_REVIEW_BLOCK_03.md
   Fragen 31–43
   Strafgesetzbuch und Strafverfahrensrecht

4. QUESTION_REVIEW_BLOCK_04.md
   Fragen 44–56
   Umgang mit Waffen und Unfallverhütungsvorschriften

5. QUESTION_REVIEW_BLOCK_05.md
   Fragen 57–75
   Umgang mit Menschen

6. QUESTION_REVIEW_BLOCK_06.md
   Fragen 76–82
   Grundzüge der Sicherheitstechnik

## 17. Export-Strategie

Kurzfristig:
Die App arbeitet weiter mit bestehenden Dateien:

1. questions.json
2. data/oral-question-bank.js
3. data/oral-sheets-bank.js

Mittelfristig:
Geprüfte Fragen werden aus der Datenbank exportiert und kontrolliert in diese Dateien übernommen.

Langfristig:
Die App kann veröffentlichte Fragen direkt aus Supabase laden.

## 18. Supabase-Regel

Supabase wird später nur mit sauberem Zugriff genutzt:

1. Supabase Auth
2. user_id pro Teilnehmer
3. course_id pro Kurs
4. Teilnehmerstatus aktiv/inaktiv
5. Row Level Security
6. Rollenmodell Teilnehmer / Dozent / Admin
7. kein Service Role Key im Frontend
8. keine offenen Tabellen für Teilnehmerdaten

## 19. localStorage-Regel

localStorage bleibt nur Übergang für die lokale Entwicklungsphase.

Später gehören diese Daten pro Nutzer in Supabase:

1. Lernfortschritt
2. Prüfungsergebnisse
3. Fehlerhistorie
4. Lernkartenfortschritt
5. mündliche Prüfungsergebnisse
6. Kursstatus

## 20. Veröffentlichungsregel

Eine Frage darf erst veröffentlicht werden, wenn:

1. sie Accaoui-eigen formuliert ist
2. sie fachlich geprüft ist
3. sie keine Dublette ist
4. sie keine 1:1-Kopie ist
5. Antwort und Erklärung stimmen
6. Kategorie und Punktzahl stimmen
7. Status published gesetzt wurde

## 21. Zielbild

Die Accaoui §34a Lern-App soll eine professionelle Fragenbank bekommen, die:

1. prüfungsnah ist
2. rechtlich sauber ist
3. didaktisch stärker ist als reine Musterfragen
4. schriftliche und mündliche Prüfung abdeckt
5. Teilnehmerfortschritt speichert
6. später Login und Supabase unterstützt
7. langfristig app-store-tauglich bleibt
