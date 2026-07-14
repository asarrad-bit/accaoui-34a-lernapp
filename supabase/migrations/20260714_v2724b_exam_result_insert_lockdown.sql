-- Accaoui §34a Lern-App – Prüfungsintegrität Lockdown
-- Stand: v27.24b
-- Status: vorbereitet, nicht live ausgeführt
--
-- Teilnehmer dürfen keine autoritativen Prüfungsdaten direkt eintragen.
-- Ein geprüfter RPC-/Server-Weg folgt später separat.

drop policy if exists "exam_attempts_insert_own"
on exam_attempts;

drop policy if exists "exam_answers_insert_own"
on exam_answers;

-- Keine Ersatz-Insert-Policy für Teilnehmer.
-- Lesen eigener Ergebnisse und Verwaltung durch berechtigte Mitarbeiter
-- bleiben durch die bestehenden Policies geregelt.
