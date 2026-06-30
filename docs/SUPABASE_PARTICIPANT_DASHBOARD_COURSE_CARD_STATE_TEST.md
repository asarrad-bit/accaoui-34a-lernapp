# Accaoui §34a Lern-App – Teilnehmer-Dashboard-Kurskarte-State-Test

Stand: v26.38b

Ziel: Prüfen und dokumentieren, ob der Adapter einen vorbereiteten Teilnehmer-Dashboard-Kurskarte-State bereitstellt, ohne sichtbare Kurskarte, ohne sichtbare Kursdaten, ohne UI-Blocker, ohne Login-Zwang und ohne Live-Verbindung.

## 1. Testgegenstand

Getestet wurde:

1. data/supabase-client-adapter.js
2. getParticipantDashboardCourseCardState()
3. participantDashboardCourseCardStatus im Supabase-Safety-Summary
4. isParticipantDashboardCourseCardAvailable im Supabase-Safety-Summary
5. isParticipantDashboardCourseCardVisible im Supabase-Safety-Summary
6. canRenderParticipantDashboardCourseCard im Supabase-Safety-Summary
7. canShowParticipantDashboardCourseTitle im Supabase-Safety-Summary
8. canShowParticipantDashboardCourseStatus im Supabase-Safety-Summary
9. canShowParticipantDashboardCourseProgress im Supabase-Safety-Summary
10. canShowParticipantDashboardCourseExpiryInfo im Supabase-Safety-Summary
11. participantDashboardCourseCardTitle im Supabase-Safety-Summary
12. participantDashboardCourseCardCourseStatus im Supabase-Safety-Summary
13. participantDashboardCourseCardProgressPercent im Supabase-Safety-Summary
14. canBlockParticipantDashboardByCourseCard im Supabase-Safety-Summary
15. participantDashboardCourseCardState im Adapter-Health-State

## 2. Erwarteter Normalzustand

Im lokalen Normalmodus gilt:

1. Dashboard-Kurskarte-State ist sichtbar.
2. Kurskarte-State ist verfügbar.
3. Kurskarte ist lokal verborgen.
4. Kurskarte kann lokal nicht rendern.
5. Kurstitel wird lokal nicht angezeigt.
6. Kursstatus wird lokal nicht angezeigt.
7. Kursfortschritt wird lokal nicht angezeigt.
8. Ablaufdatum-Information wird lokal nicht angezeigt.
9. Kurskarte kann lokal nicht blockieren.
10. Lokaler Dashboard-Zugriff bleibt erlaubt.

## 3. Browser-Test

Erwartetes und bestätigtes Ergebnis:

1. adapter version: v26.38a
2. card status: local_dashboard_course_card_hidden
3. card available: true
4. card visible: false
5. card canRender: false
6. card title visible: false
7. card status visible: false
8. card progress visible: false
9. card courseTitle: null
10. card courseStatus: null
11. card progress: null
12. card canBlock: false
13. card loginRequired: false
14. card localAccess: true
15. summary card status: local_dashboard_course_card_hidden
16. summary card visible: false
17. summary card render: false
18. summary card block: false
19. health card object: local_dashboard_course_card_hidden

## 4. Sicherheitsbewertung

Der Test ist bestanden.

Bedeutung:

1. Eine spätere Teilnehmer-Dashboard-Kurskarte kann vorbereitet werden.
2. Aktuell wird keine Kurskarte angezeigt.
3. Aktuell werden keine Kursdaten angezeigt.
4. Aktuell wird kein Kursfortschritt angezeigt.
5. Aktuell wird kein Login erzwungen.
6. Aktuell gibt es keinen UI-Blocker.
7. Supabase bleibt deaktiviert.
8. Der lokale Unterrichts- und App-Betrieb bleibt unverändert möglich.

## 5. Status

Status v26.38b: Teilnehmer-Dashboard-Kurskarte-State-Test dokumentiert. Die Kurskarte ist vorbereitet, lokal verborgen, nicht blockierend und ohne Live-Verbindung.
