-- Accaoui §34a Lern-App
-- Direkte Schreibzugriffe auf Prüfungsdaten vollständig sperren
-- Stand: v27.28d
-- Status: vorbereitet, nicht live ausgeführt

drop policy if exists "exam_attempts_staff_manage"
on public.exam_attempts;

drop policy if exists "exam_answers_staff_manage"
on public.exam_answers;

revoke insert, update, delete
on table public.exam_attempts
from public, anon, authenticated;

revoke insert, update, delete
on table public.exam_answers
from public, anon, authenticated;

-- Lesen bleibt über die bestehenden geprüften Select-Policies möglich.
-- Schreiben erfolgt ausschließlich über Security-Definer-RPCs.
