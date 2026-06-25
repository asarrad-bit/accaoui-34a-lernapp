# Accaoui §34a Lern-App – Teilnehmer-Kursstatus-State-Test

Stand: v26.22b

Ziel: Prüfen und dokumentieren, ob der Adapter einen vorbereiteten Teilnehmer-Kursstatus-State bereitstellt, ohne echten Supabase-Login, ohne Client, ohne Kursabruf und ohne Live-Verbindung.

## 1. Testgegenstand

Getestet wurde:

1. data/supabase-client-adapter.js
2. getParticipantCourseState()
3. participantCourseStatus im Supabase-Safety-Summary
4. isParticipantCourseRequired im Supabase-Safety-Summary
5. canLoadParticipantCourse im Supabase-Safety-Summary
6. isParticipantCourseLoaded im Supabase-Safety-Summary
7. isParticipantCourseExpired im Supabase-Safety-Summary
8. participantCourseState im Adapter-Health-State
9. lokaler App-Zugriff ohne Login-Zwang

## 2. Erwarteter Normalzustand

Im lokalen Normalmodus gilt:

1. Teilnehmer-Kursstatus-State ist sichtbar.
2. Kursabruf ist vorbereitet, aber deaktiviert.
3. Es gibt keinen echten Teilnehmerkurs.
4. Es gibt keinen Supabase-Client.
5. Es gibt keine Live-Verbindung.
6. Ein Kursstatus ist lokal nicht erforderlich.
7. Der Kurs ist lokal nicht abgelaufen.
8. Lokaler Zugriff bleibt erlaubt.

## 3. Browser-Test

Erwartetes und bestätigtes Ergebnis:

1. adapter version: v26.22a
2. course status: local_course_stub
3. course hasCourse: false
4. course canLoadCourse: false
5. course required: false
6. course expired: false
7. course localAccess: true
8. summary participantCourseStatus: local_course_stub
9. summary isParticipantCourseRequired: false
10. summary canLoadParticipantCourse: false
11. summary isParticipantCourseLoaded: false
12. summary isParticipantCourseExpired: false
13. health course object: local_course_stub

## 4. Sicherheitsbewertung

Der Test ist bestanden.

Bedeutung:

1. Der spätere Teilnehmer-Kursstatus kann vorbereitet werden.
2. Aktuell wird weiterhin kein Login erzwungen.
3. Supabase bleibt deaktiviert.
4. Es gibt keinen Client.
5. Es gibt keinen Kursabruf.
6. Es gibt keine Kursablauf-Sperre.
7. Der lokale Unterrichts- und App-Betrieb bleibt unverändert möglich.

## 5. Status

Status v26.22b: Teilnehmer-Kursstatus-State-Test dokumentiert. Der Kursstatus-State ist vorbereitet, lokal sicher und ohne Live-Verbindung.
