# Accaoui §34a Lern-App – Teilnehmer-Dashboard-Kurszugriff-State-Test

Stand: v26.31b

Ziel: Prüfen und dokumentieren, ob der Adapter einen vorbereiteten Teilnehmer-Dashboard-Kurszugriff-State bereitstellt, ohne aktive Kursprüfung, ohne Kurs-Sperre, ohne Kurs-Lock, ohne Login-Zwang und ohne Live-Verbindung.

## 1. Testgegenstand

Getestet wurde:

1. data/supabase-client-adapter.js
2. getParticipantDashboardCourseAccessState()
3. participantDashboardCourseAccessStatus im Supabase-Safety-Summary
4. isParticipantDashboardCourseAccessRequired im Supabase-Safety-Summary
5. canCheckParticipantDashboardCourseAccess im Supabase-Safety-Summary
6. canBlockParticipantDashboardCourseAccess im Supabase-Safety-Summary
7. hasAssignedDashboardCourse im Supabase-Safety-Summary
8. canShowDashboardCourseLock im Supabase-Safety-Summary
9. canShowDashboardCourseAccessWarning im Supabase-Safety-Summary
10. isLocalDashboardCourseAccessAllowed im Supabase-Safety-Summary
11. participantDashboardCourseAccessState im Adapter-Health-State

## 2. Erwarteter Normalzustand

Im lokalen Normalmodus gilt:

1. Dashboard-Kurszugriff-State ist sichtbar.
2. Kurszugriff ist lokal erlaubt.
3. Kurszugriff-Prüfung ist lokal nicht aktiv.
4. Kurszugriff kann lokal nicht blockiert werden.
5. Es ist kein Kurs zugewiesen.
6. Es gibt keinen Kurs-Lock.
7. Es gibt keine Kurszugriff-Warnung.
8. Login ist lokal nicht erforderlich.
9. Lokaler Dashboard-Zugriff bleibt erlaubt.

## 3. Browser-Test

Erwartetes und bestätigtes Ergebnis:

1. adapter version: v26.31a
2. course access status: local_dashboard_course_access_allowed
3. course access required: false
4. course access canCheck: false
5. course access canBlock: false
6. course assigned: false
7. course lock: false
8. course warning: false
9. course localAccess: true
10. summary course status: local_dashboard_course_access_allowed
11. summary course required: false
12. summary course block: false
13. summary course localAccess: true
14. health course object: local_dashboard_course_access_allowed

## 4. Sicherheitsbewertung

Der Test ist bestanden.

Bedeutung:

1. Eine spätere Kurszugriff-Prüfung kann vorbereitet werden.
2. Aktuell wird kein Kurszugriff geprüft.
3. Aktuell wird kein Kurszugriff blockiert.
4. Aktuell wird kein Kurs-Lock angezeigt.
5. Aktuell wird kein Login erzwungen.
6. Supabase bleibt deaktiviert.
7. Der lokale Unterrichts- und App-Betrieb bleibt unverändert möglich.

## 5. Status

Status v26.31b: Teilnehmer-Dashboard-Kurszugriff-State-Test dokumentiert. Der Dashboard-Kurszugriff-State ist vorbereitet, lokal erlaubt, nicht blockierend und ohne Live-Verbindung.
