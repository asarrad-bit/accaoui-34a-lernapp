# Accaoui §34a Lern-App – Teilnehmer-Dashboard-Unterrichtsplan-State-Test

Stand: v26.52b

Ziel: Prüfen und dokumentieren, ob der Adapter einen vorbereiteten Teilnehmer-Dashboard-Unterrichtsplan-State bereitstellt, ohne sichtbaren Unterrichtsplan, ohne Unterrichtsplan-Daten, ohne nächsten Unterrichtshinweis, ohne UI-Blocker, ohne Login-Zwang und ohne Live-Verbindung.

## 1. Testgegenstand

Getestet wurde:

1. data/supabase-client-adapter.js
2. getParticipantDashboardLessonPlanState()
3. participantDashboardLessonPlanStatus im Supabase-Safety-Summary
4. isParticipantDashboardLessonPlanAvailable im Supabase-Safety-Summary
5. isParticipantDashboardLessonPlanVisible im Supabase-Safety-Summary
6. canRenderParticipantDashboardLessonPlan im Supabase-Safety-Summary
7. canLoadParticipantDashboardLessonPlan im Supabase-Safety-Summary
8. hasParticipantDashboardLessonPlanData im Supabase-Safety-Summary
9. participantDashboardTotalLessonCount im Supabase-Safety-Summary
10. participantDashboardNextLessonAt im Supabase-Safety-Summary
11. participantDashboardCurrentTopic im Supabase-Safety-Summary
12. participantDashboardCurrentModule im Supabase-Safety-Summary
13. canShowParticipantDashboardLessonPlanList im Supabase-Safety-Summary
14. canShowParticipantDashboardLessonPlanCard im Supabase-Safety-Summary
15. canShowParticipantDashboardNextLessonHint im Supabase-Safety-Summary
16. canBlockParticipantDashboardByLessonPlan im Supabase-Safety-Summary
17. participantDashboardLessonPlanState im Adapter-Health-State

## 2. Erwarteter Normalzustand

Im lokalen Normalmodus gilt:

1. Dashboard-Unterrichtsplan-State ist vorhanden.
2. Unterrichtsplan-State ist verfügbar.
3. Unterrichtsplan ist lokal verborgen.
4. Unterrichtsplan kann lokal nicht rendern.
5. Unterrichtsplan kann lokal nicht geladen werden.
6. Es gibt keine Unterrichtsplan-Daten.
7. Gesamtanzahl der Unterrichtseinheiten ist null.
8. Nächster Unterricht ist null.
9. Aktuelles Thema ist null.
10. Aktuelles Modul ist null.
11. Unterrichtsplan-Liste wird lokal nicht angezeigt.
12. Unterrichtsplan-Karte wird lokal nicht angezeigt.
13. Nächster-Unterricht-Hinweis wird lokal nicht angezeigt.
14. Unterrichtsplan-State kann lokal nicht blockieren.
15. Lokaler Dashboard-Zugriff bleibt erlaubt.

## 3. Browser-Test

Erwartetes und bestätigtes Ergebnis:

1. adapter version: v26.52a
2. lessonPlan status: local_dashboard_lesson_plan_hidden
3. lessonPlan available: true
4. lessonPlan visible: false
5. lessonPlan canRender: false
6. lessonPlan canLoad: false
7. lessonPlan hasData: false
8. lessonPlan total: null
9. lessonPlan next: null
10. lessonPlan topic: null
11. lessonPlan module: null
12. lessonPlan list: false
13. lessonPlan card: false
14. lessonPlan nextHint: false
15. lessonPlan canBlock: false
16. lessonPlan loginRequired: false
17. lessonPlan localAccess: true
18. summary lessonPlan status: local_dashboard_lesson_plan_hidden
19. summary lessonPlan visible: false
20. summary lessonPlan render: false
21. summary lessonPlan nextHint: false
22. summary lessonPlan block: false
23. health lessonPlan object: local_dashboard_lesson_plan_hidden

## 4. Sicherheitsbewertung

Der Test ist bestanden.

Bedeutung:

1. Ein späterer Unterrichtsplan-Bereich kann vorbereitet werden.
2. Aktuell wird kein Unterrichtsplan angezeigt.
3. Aktuell werden keine Unterrichtsplan-Daten geladen.
4. Aktuell wird kein nächster Unterricht angezeigt.
5. Aktuell wird kein Login erzwungen.
6. Aktuell gibt es keinen UI-Blocker.
7. Supabase bleibt deaktiviert.
8. Der lokale Unterrichts- und App-Betrieb bleibt unverändert möglich.

## 5. Status

Status v26.52b: Teilnehmer-Dashboard-Unterrichtsplan-State-Test dokumentiert. Der Unterrichtsplan-Bereich ist vorbereitet, lokal verborgen, ohne Unterrichtsdaten, ohne nächsten Unterrichtshinweis, nicht blockierend und ohne Live-Verbindung.
