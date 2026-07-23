from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
MIGRATIONS = ROOT / "supabase" / "migrations"

CONTRACT_PATH = (
    ROOT
    / "docs"
    / "contracts"
    / "exam-history-idempotency-transactional-mutation-contract.json"
)
RPC_PATH = (
    MIGRATIONS
    / "20260723_v2731u_"
      "exam_history_outer_domain_mutation_rpc.sql"
)


def fail(message: str) -> None:
    print(f"FEHLER: {message}")
    sys.exit(1)


if not CONTRACT_PATH.is_file():
    fail("Transaktionaler Fachmutationsvertrag fehlt.")

try:
    contract = json.loads(
        CONTRACT_PATH.read_text(encoding="utf-8")
    )
except Exception as exc:
    fail(f"Transaktionaler Fachmutationsvertrag ungültig: {exc}")

if contract.get("version") != "v27.31u":
    fail("Transaktionsvertrag besitzt nicht v27.31u.")
if contract.get("contractVersion") != 1:
    fail("Transaktionsvertrag besitzt nicht Schema 1.")
if contract.get("status") != "prepared_not_live":
    fail("Transaktionsvertrag ist nicht vorbereitet.")
if contract.get("productiveReleaseAllowed") is not False:
    fail("Produktive Freigabe darf noch nicht erlaubt sein.")

identity = contract.get("identity", {})
if identity.get("source") != "trusted_server_or_database_issued":
    fail("Operationsidentitätsquelle ist nicht vertrauenswürdig.")
if identity.get("browserGeneratedAllowed") is not False:
    fail("Browsergenerierte Operations-ID ist erlaubt.")
if identity.get("operationIdentityInputAllowed") is not False:
    fail("Externe Operationsidentität ist erlaubt.")
if identity.get("verifiedNow") is not True:
    fail("Operationsidentität ist nicht als umgesetzt markiert.")
if identity.get("requiredParameters") != [
    "external_operation_id",
    "operation_scope",
    "operation",
    "resource_identity",
    "expected_storage_version",
    "payload_fingerprint",
]:
    fail("Transaktionale Identitätsparameter sind ungültig.")

implementation = contract.get("implementation", {})
if implementation != {
    "outerRpc": "public.accaoui_mutate_exam_history_domain",
    "migrationPath": (
        "supabase/migrations/"
        "20260723_v2731u_"
        "exam_history_outer_domain_mutation_rpc.sql"
    ),
    "implementationPresent": True,
    "migrationLiveExecuted": False,
    "singleDatabaseTransaction": True,
    "expectedFailureSubtransaction": True,
    "unexpectedFailureReraises": True,
    "directExecutionGrantPresent": False,
}:
    fail("Transaktionale Implementierung ist ungültig.")

unresolved = contract.get("unresolvedRequirements", {})
if unresolved != {
    "trustedOperationIdentityIssuance": False,
    "domainMutationRpcImplementation": False,
    "liveDatabaseTests": True,
    "concurrencyTests": True,
}:
    fail("Offene Transaktionsanforderungen sind ungültig.")

if not RPC_PATH.is_file():
    fail("Äußerer Fachmutations-RPC fehlt.")

sql = RPC_PATH.read_text(encoding="utf-8")
clean = re.sub(
    r"--.*?$",
    "",
    sql,
    flags=re.MULTILINE,
)
compact = re.sub(r"\s+", " ", clean.lower()).strip()

required = (
    "security definer",
    "set search_path = pg_catalog, public",
    "set row_security = off",
    "public.accaoui_issue_exam_history_operation_identity(",
    "public.accaoui_reserve_exam_history_idempotency_operation(",
    "'reserved_new'",
    "'reserved_existing_pending'",
    "'reserved_existing_completed'",
    "'reserved_existing_failed'",
    "begin select mutation.outcome",
    "exception when sqlstate '22023' or sqlstate '40001' "
    "or sqlstate '23514'",
    "get stacked diagnostics v_failure_code = message_text",
    "public.accaoui_complete_exam_history_idempotency_operation(",
    "'failed'",
    "'completed'",
)
for marker in required:
    if marker not in compact:
        fail(f"Transaktionsanweisung fehlt: {marker}")

if compact.count(
    "public.accaoui_complete_exam_history_idempotency_operation("
) < 2:
    fail("Beide terminalen Abschlusswege fehlen.")

if "when others" in compact:
    fail("Unerwartete Fehler werden pauschal abgefangen.")
if "sqlerrm" in compact:
    fail("Roher SQL-Fehlertext wird verwendet.")
if "grant execute" in compact:
    fail("Äußerer RPC besitzt bereits eine Ausführungsfreigabe.")

for forbidden in (
    "insert into public.",
    "update public.",
    "delete from public.",
    "dblink",
    "pg_background",
    "service_role",
):
    if forbidden in compact:
        fail(f"Transaktionsgrenze enthält unzulässigen Inhalt: {forbidden}")

print("Transaktionaler Fachmutationsvertrag: OK")
print(
    "Reihenfolge: Authentifizieren, kanonisieren, ausstellen, "
    "reservieren, verzweigen, mutieren, abschließen"
)
print(
    "Existing Pending/Terminal: keine erneute Domain-Mutation"
)
print(
    "Erwarteter Domain-Fehler: Teilmutation zurückgerollt und "
    "stabil als Failed abgeschlossen"
)
print(
    "Unerwarteter Fehler: wird erneut ausgelöst und rollt den "
    "gesamten Datenbankaufruf zurück"
)
print("Produktive Freigabe: nein")
print("Live-Ausführung: nein")
