from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
MIGRATIONS = ROOT / "supabase" / "migrations"

SCHEMA = "20260710_v2720b_mvp_schema.sql"
RLS = "20260710_v2721a_mvp_rls_policies.sql"
LOCKDOWN = "20260714_v2724b_exam_result_insert_lockdown.sql"

EXPECTED_TABLES = {
    "participants",
    "courses",
    "enrollments",
    "exam_attempts",
    "exam_answers",
    "certificates",
    "admin_profiles",
    "audit_logs",
}


def fail(message: str) -> None:
    print(f"FEHLER: {message}")
    sys.exit(1)


if not MIGRATIONS.is_dir():
    fail("Migrationsordner fehlt.")

files = sorted(p.name for p in MIGRATIONS.glob("*.sql"))

for required in (SCHEMA, RLS, LOCKDOWN):
    if required not in files:
        fail(f"Migration fehlt: {required}")

if files.index(SCHEMA) >= files.index(RLS):
    fail("RLS-Migration steht vor dem Grundschema.")

if files.index(RLS) >= files.index(LOCKDOWN):
    fail("Prüfungs-Lockdown steht vor der RLS-Migration.")

schema = (MIGRATIONS / SCHEMA).read_text(encoding="utf-8")
rls = (MIGRATIONS / RLS).read_text(encoding="utf-8")
lockdown = (MIGRATIONS / LOCKDOWN).read_text(encoding="utf-8")

tables = set(
    re.findall(
        r"create\s+table\s+if\s+not\s+exists\s+([a-z_]+)",
        schema,
        flags=re.IGNORECASE,
    )
)

missing_tables = EXPECTED_TABLES - tables
if missing_tables:
    fail(f"Tabellen fehlen: {sorted(missing_tables)}")

for table in EXPECTED_TABLES:
    pattern = rf"alter\s+table\s+{table}\s+enable\s+row\s+level\s+security"
    if not re.search(pattern, schema, flags=re.IGNORECASE):
        fail(f"RLS-Aktivierung fehlt für: {table}")

policies = re.findall(
    r'create\s+policy\s+"[^"]+"\s+on\s+([a-z_]+)',
    rls,
    flags=re.IGNORECASE,
)

if len(policies) != 17:
    fail(f"Erwartet: 17 Basis-Policies, gefunden: {len(policies)}")

required_drops = (
    'drop policy if exists "exam_attempts_insert_own"',
    'drop policy if exists "exam_answers_insert_own"',
)

for statement in required_drops:
    if statement not in lockdown.lower():
        fail(f"Lockdown-Anweisung fehlt: {statement}")

if "create policy" in lockdown.lower():
    fail("Lockdown darf keine neue Policy erstellen.")

effective_policy_count = len(policies) - len(required_drops)

if effective_policy_count != 15:
    fail(
        f"Erwartet: 15 effektive Policies, gefunden: "
        f"{effective_policy_count}"
    )

unknown_policy_tables = set(policies) - EXPECTED_TABLES
if unknown_policy_tables:
    fail(f"Policies verweisen auf unbekannte Tabellen: {sorted(unknown_policy_tables)}")

if rls.count("create or replace function public.accaoui_is_") != 2:
    fail("Die zwei Rollen-Helper-Funktionen fehlen oder sind doppelt.")

if len(re.findall(r"\bto\s+authenticated\b", rls, flags=re.IGNORECASE)) != 17:
    fail("Nicht alle 17 Policies sind auf authenticated begrenzt.")

if "auth.uid()" not in rls:
    fail("auth.uid()-Prüfung fehlt.")

all_sql = "\n".join(
    (MIGRATIONS / name).read_text(encoding="utf-8")
    for name in files
)

sql_without_comments = re.sub(
    r"--.*?$",
    "",
    all_sql,
    flags=re.MULTILINE,
)
for forbidden in ("service_role", "SUPABASE_SERVICE_ROLE_KEY", "postgresql://", "postgres://"):
    if forbidden.lower() in sql_without_comments.lower():
        fail(f"Verbotener sensitiver Inhalt gefunden: {forbidden}")

print("Supabase-Migrationsprüfung: OK")
print(f"SQL-Dateien: {len(files)}")
print(f"MVP-Tabellen: {len(EXPECTED_TABLES)}")
print(f"Basis-RLS-Policies: {len(policies)}")
print(f"Effektive RLS-Policies: {effective_policy_count}")
print("Direkte Prüfungs-Inserts für Teilnehmer: gesperrt")
print("Reihenfolge: Schema vor RLS vor Prüfungs-Lockdown")
print("Live-Ausführung: nein")
