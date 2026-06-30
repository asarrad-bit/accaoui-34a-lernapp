# Accaoui §34a Lern-App – Teilnehmer-Dashboard-Ablaufdatum-State-Test

Stand: v26.32b

Ziel: Prüfen und dokumentieren, ob der Adapter einen vorbereiteten Teilnehmer-Dashboard-Ablaufdatum-State bereitstellt, ohne aktive Ablaufdatum-Prüfung, ohne gesetztes Ablaufdatum, ohne Ablauf-Warnung, ohne Sperre und ohne Live-Verbindung.

## 1. Testgegenstand

Getestet wurde:

1. data/supabase-client-adapter.js
2. getParticipantDashboardExpiryState()
3. participantDashboardExpiryStatus im Supabase-Safety-Summary
4. isParticipantDashboardExpiryCheckRequired im Supabase-Safety-Summary
5. canCheckParticipantDashboardExpiry im Supabase-Safety-Summary
6. canBlockParticipantDashboardOnExpiry im Supabase-Safety-Summary
7. hasParticipantDashboardExpiryDate im Supabase-Safety-Summary
8. participantDashboardExpiresAt im Supabase-Safety-Summary
9. isParticipantDashboardExpired im Supabase-Safety-Summary
10. participantDashboardDaysRemaining im Supabase-Safety-Summary
11. canShowParticipantDashboardExpiryWarning im Supabase-Safety-Summary
12. isLocalDashboardExpiryAccessAllowed im Supabase-Safety-Summary
13. participantDashboardExpiryState im Adapter-Health-State

## 2. Erwarteter Normalzustand

Im lokalen Normalmodus gilt:

1. Dashboard-Ablaufdatum-State ist sichtbar.
2. Ablaufdatum-Prüfung ist lokal deaktiviert.
3. Es ist kein Ablaufdatum gesetzt.
4. Teilnehmerzugriff ist nicht abgelaufen.
5. Es gibt keine Ablauf-Warnung.
6. Ablaufdatum kann lokal nicht geprüft werden.
7. Dashboard kann lokal nicht wegen Ablaufdatum gesperrt werden.
8. Login ist lokal nicht erforderlich.
9. Lokaler Dashboard-Zugriff bleibt erlaubt.

## 3. Browser-Test

Erwartetes und bestätigtes Ergebnis:

1. adapter version: v26.32a
2. expiry status: local_dashboard_expiry_check_disabled
3. expiry required: false
4. expiry canCheck: false
5. expiry canBlock: false
6. expiry hasDate: false
7. expiry expiresAt: null
8. expiry isExpired: false
9. expiry warning: false
10. expiry localAccess: true
11. summary expiry status: local_dashboard_expiry_check_disabled
12. summary expiry required: false
13. summary expiry block: false
14. summary expiry expired: false
15. health expiry object: local_dashboard_expiry_check_disabled

## 4. Sicherheitsbewertung

Der Test ist bestanden.

Bedeutung:

1. Eine spätere Teilnehmer- oder Kurs-Zeitbegrenzung kann vorbereitet werden.
2. Aktuell wird kein Ablaufdatum geprüft.
3. Aktuell ist kein Ablaufdatum gesetzt.
4. Aktuell wird keine Ablauf-Warnung angezeigt.
5. Aktuell wird kein Dashboard wegen Ablaufdatum gesperrt.
6. Supabase bleibt deaktiviert.
7. Der lokale Unterrichts- und App-Betrieb bleibt unverändert möglich.

## 5. Status

Status v26.32b: Teilnehmer-Dashboard-Ablaufdatum-State-Test dokumentiert. Der Dashboard-Ablaufdatum-State ist vorbereitet, lokal deaktiviert, nicht blockierend und ohne Live-Verbindung.
