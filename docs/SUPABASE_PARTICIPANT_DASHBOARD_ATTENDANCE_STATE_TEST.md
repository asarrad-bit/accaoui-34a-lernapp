# Accaoui §34a Lern-App – Teilnehmer-Dashboard-Anwesenheit-State-Test

Stand: v26.51b

Ziel: Prüfen und dokumentieren, ob der Adapter einen vorbereiteten Teilnehmer-Dashboard-Anwesenheit-State bereitstellt, ohne sichtbaren Anwesenheitsbereich, ohne Anwesenheitsdaten, ohne Anwesenheitsquote, ohne UI-Blocker, ohne Login-Zwang und ohne Live-Verbindung.

## 1. Testgegenstand

Getestet wurde:

1. data/supabase-client-adapter.js
2. getParticipantDashboardAttendanceState()
3. participantDashboardAttendanceStatus im Supabase-Safety-Summary
4. isParticipantDashboardAttendanceAvailable im Supabase-Safety-Summary
5. isParticipantDashboardAttendanceVisible im Supabase-Safety-Summary
6. canRenderParticipantDashboardAttendance im Supabase-Safety-Summary
7. canLoadParticipantDashboardAttendance im Supabase-Safety-Summary
8. hasParticipantDashboardAttendanceData im Supabase-Safety-Summary
9. participantDashboardTotalAttendanceCount im Supabase-Safety-Summary
10. participantDashboardPresentCount im Supabase-Safety-Summary
11. participantDashboardAbsentCount im Supabase-Safety-Summary
12. participantDashboardExcusedAbsenceCount im Supabase-Safety-Summary
13. participantDashboardAttendanceRatePercent im Supabase-Safety-Summary
14. participantDashboardLastAttendanceAt im Supabase-Safety-Summary
15. canShowParticipantDashboardAttendanceList im Supabase-Safety-Summary
16. canShowParticipantDashboardAttendanceCard im Supabase-Safety-Summary
17. canShowParticipantDashboardAttendanceRate im Supabase-Safety-Summary
18. canBlockParticipantDashboardByAttendance im Supabase-Safety-Summary
19. participantDashboardAttendanceState im Adapter-Health-State

## 2. Erwarteter Normalzustand

Im lokalen Normalmodus gilt:

1. Dashboard-Anwesenheit-State ist vorhanden.
2. Anwesenheit-State ist verfügbar.
3. Anwesenheitsbereich ist lokal verborgen.
4. Anwesenheitsbereich kann lokal nicht rendern.
5. Anwesenheit kann lokal nicht geladen werden.
6. Es gibt keine Anwesenheitsdaten.
7. Gesamtanzahl der Anwesenheiten ist null.
8. Anzahl anwesend ist null.
9. Anzahl abwesend ist null.
10. Anzahl entschuldigter Abwesenheiten ist null.
11. Anwesenheitsquote ist null.
12. Letzter Anwesenheitseintrag ist null.
13. Anwesenheitsliste wird lokal nicht angezeigt.
14. Anwesenheitskarte wird lokal nicht angezeigt.
15. Anwesenheitsquote wird lokal nicht angezeigt.
16. Anwesenheit-State kann lokal nicht blockieren.
17. Lokaler Dashboard-Zugriff bleibt erlaubt.

## 3. Browser-Test

Erwartetes und bestätigtes Ergebnis:

1. adapter version: v26.51a
2. attendance status: local_dashboard_attendance_hidden
3. attendance available: true
4. attendance visible: false
5. attendance canRender: false
6. attendance canLoad: false
7. attendance hasData: false
8. attendance total: null
9. attendance present: null
10. attendance absent: null
11. attendance excused: null
12. attendance rate: null
13. attendance last: null
14. attendance list: false
15. attendance card: false
16. attendance rateVisible: false
17. attendance canBlock: false
18. attendance loginRequired: false
19. attendance localAccess: true
20. summary attendance status: local_dashboard_attendance_hidden
21. summary attendance visible: false
22. summary attendance render: false
23. summary attendance rate: false
24. summary attendance block: false
25. health attendance object: local_dashboard_attendance_hidden

## 4. Sicherheitsbewertung

Der Test ist bestanden.

Bedeutung:

1. Ein späterer Anwesenheitsbereich kann vorbereitet werden.
2. Aktuell wird kein Anwesenheitsbereich angezeigt.
3. Aktuell werden keine Anwesenheitsdaten geladen.
4. Aktuell wird keine Anwesenheitsquote angezeigt.
5. Aktuell wird kein Login erzwungen.
6. Aktuell gibt es keinen UI-Blocker.
7. Supabase bleibt deaktiviert.
8. Der lokale Unterrichts- und App-Betrieb bleibt unverändert möglich.

## 5. Status

Status v26.51b: Teilnehmer-Dashboard-Anwesenheit-State-Test dokumentiert. Der Anwesenheitsbereich ist vorbereitet, lokal verborgen, ohne Anwesenheitsdaten, ohne Quote, nicht blockierend und ohne Live-Verbindung.
