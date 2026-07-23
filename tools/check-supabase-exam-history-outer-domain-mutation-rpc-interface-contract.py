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
    / "exam-history-outer-domain-mutation-rpc-interface-contract.json"
)
TRANSACTION_CONTRACT_PATH = (
    ROOT
    / "docs"
    / "contracts"
    / "exam-history-idempotency-transactional-mutation-contract.json"
)
DOMAIN_CONTRACT_PATH = (
    ROOT
    / "docs"
    / "contracts"
    / "exam-history-domain-storage-contract.json"
)
RPC_PATH = (
    MIGRATIONS
    / "20260723_v2731u_"
      "exam_history_outer_domain_mutation_rpc.sql"
)


def fail(message: str) -> None:
    print(f"FEHLER: {message}")
    sys.exit(1)


def read_json(path: Path, label: str):
    if not path.is_file():
        fail(f"{label} fehlt.")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"{label} ungültig: {exc}")


def compact(text: str) -> str:
    text = re.sub(
        r"--.*?$",
        "",
        text,
        flags=re.MULTILINE,
    )
    return re.sub(r"\s+", " ", text.lower()).strip()


contract = read_json(
    CONTRACT_PATH,
    "Äußerer Fachmutations-RPC-Vertrag",
)

if contract.get("version") != "v27.31u":
    fail("Äußerer RPC-Vertrag besitzt nicht v27.31u.")
if contract.get("contractVersion") != 1:
    fail("Äußerer RPC-Vertrag besitzt nicht Schema 1.")
if contract.get("status") != "prepared_not_live":
    fail("Äußerer RPC-Vertrag ist nicht vorbereitet.")
if contract.get("productiveReleaseAllowed") is not False:
    fail("Äußerer RPC darf noch nicht produktiv sein.")
if contract.get("implementationPresent") is not True:
    fail("Äußerer RPC ist nicht als vorbereitet markiert.")

expected_parameters = [
    {"name": "p_client_request_key", "type": "text"},
    {"name": "p_operation_scope", "type": "text"},
    {"name": "p_operation", "type": "text"},
    {"name": "p_resource_identity", "type": "text"},
    {"name": "p_expected_storage_version", "type": "bigint"},
    {
        "name": "p_domain_payload",
        "type": "jsonb",
        "default": None,
    },
]

interface = contract.get("publicInterface", {})
if interface.get("allowedParameters") != expected_parameters:
    fail("Äußere RPC-Parameter sind nicht kanonisch.")
if interface.get("authenticatedExecutionOnly") is not True:
    fail("Äußerer RPC ist nicht für spätere Auth-Ausführung begrenzt.")
if interface.get("publicExecutionAllowed") is not False:
    fail("Public-Ausführung ist erlaubt.")
if interface.get("anonExecutionAllowed") is not False:
    fail("Anonyme Ausführung ist erlaubt.")

implementation = contract.get("implementation", {})
if implementation != {
    "name": "public.accaoui_mutate_exam_history_domain",
    "migrationPath": (
        "supabase/migrations/"
        "20260723_v2731u_"
        "exam_history_outer_domain_mutation_rpc.sql"
    ),
    "implementationPresent": True,
    "migrationLiveExecuted": False,
    "directExecutionGrantPresent": False,
    "singleDatabaseTransaction": True,
    "returnsInternalOperationId": False,
    "returnsInternalFingerprints": False,
    "directTableMutation": False,
}:
    fail("Äußere RPC-Implementierungsgrenze ist ungültig.")

unresolved = contract.get("unresolvedRequirements", {})
if unresolved != {
    "scopeSpecificPayloadSchemas": False,
    "outerDomainMutationRpcImplementation": False,
    "liveDatabaseTests": True,
    "concurrencyTests": True,
    "authorizationTests": True,
    "expectedStorageVersionIdentityBinding": False,
}:
    fail("Offene äußere RPC-Anforderungen sind ungültig.")

transaction = read_json(
    TRANSACTION_CONTRACT_PATH,
    "Transaktionaler Fachmutationsvertrag",
)
if transaction.get("version") != "v27.31u":
    fail("Transaktionsvertrag besitzt nicht v27.31u.")

domain = read_json(
    DOMAIN_CONTRACT_PATH,
    "Domain-Speichervertrag",
)
if domain.get("version") != "v27.31u":
    fail("Domain-Speichervertrag besitzt nicht v27.31u.")

if not RPC_PATH.is_file():
    fail("Äußere Fachmutations-RPC-Migration fehlt.")

sql = RPC_PATH.read_text(encoding="utf-8")
sql_compact = compact(sql)

signature = re.search(
    r"function\s+"
    r"public\.accaoui_mutate_exam_history_domain"
    r"\s*\((.*?)\)\s*returns\s+table\s*"
    r"\((.*?)\)\s*language\s+plpgsql",
    sql,
    flags=re.IGNORECASE | re.DOTALL,
)
if not signature:
    fail("Äußere RPC-Signatur fehlt.")

parameters = re.sub(
    r"\s+",
    " ",
    signature.group(1).strip().lower(),
)
if parameters != (
    "p_client_request_key text, "
    "p_operation_scope text, "
    "p_operation text, "
    "p_resource_identity text, "
    "p_expected_storage_version bigint, "
    "p_domain_payload jsonb default null"
):
    fail(f"Unerwartete äußere RPC-Parameter: {parameters}")

returns = re.sub(
    r"\s+",
    " ",
    signature.group(2).strip().lower(),
)
if returns != (
    "outcome text, "
    "operation_status text, "
    "result jsonb, "
    "failure_code text, "
    "retryable boolean"
):
    fail(f"Unerwartete äußere RPC-Rückgabe: {returns}")

required_markers = (
    "language plpgsql",
    "security definer",
    "set search_path = pg_catalog, public",
    "set row_security = off",
    "v_auth_user_id := auth.uid()",
    "message = 'authentication_required'",
    "public.accaoui_validate_exam_history_domain_payload(",
    "public.accaoui_issue_exam_history_operation_identity(",
    "public.accaoui_reserve_exam_history_idempotency_operation(",
    "public.accaoui_mutate_exam_history_domain_resource(",
    "public.accaoui_complete_exam_history_idempotency_operation(",
    "p_expected_storage_version",
    "v_payload_fingerprint",
    "'reserved_existing_pending'",
    "'reserved_existing_completed'",
    "'reserved_existing_failed'",
    "'reserved_new'",
    "'in_progress'::text",
    "get stacked diagnostics v_failure_code = message_text",
    "'domain_storage_version_conflict'",
    "'failed'",
    "'completed'",
    "jsonb_build_object(",
)
for marker in required_markers:
    if marker not in sql_compact:
        fail(f"Äußere RPC-Anweisung fehlt: {marker}")

helper_order = [
    "public.accaoui_validate_exam_history_domain_payload(",
    "public.accaoui_issue_exam_history_operation_identity(",
    "public.accaoui_reserve_exam_history_idempotency_operation(",
    "public.accaoui_mutate_exam_history_domain_resource(",
    "public.accaoui_complete_exam_history_idempotency_operation(",
]
positions = [sql_compact.find(marker) for marker in helper_order]
if any(position < 0 for position in positions):
    fail("Äußere RPC-Helperreihenfolge ist unvollständig.")
if positions != sorted(positions):
    fail(f"Äußere RPC-Helperreihenfolge ist falsch: {positions}")

if sql_compact.count(
    "public.accaoui_complete_exam_history_idempotency_operation("
) < 2:
    fail("Completed- und Failed-Abschluss sind nicht beide vorhanden.")

for call_name in (
    "public.accaoui_issue_exam_history_operation_identity",
    "public.accaoui_reserve_exam_history_idempotency_operation",
    "public.accaoui_mutate_exam_history_domain_resource",
):
    call_match = re.search(
        re.escape(call_name)
        + r"\s*\((.*?)\)",
        sql,
        flags=re.IGNORECASE | re.DOTALL,
    )
    if not call_match:
        fail(f"Helperaufruf fehlt: {call_name}")
    if "p_expected_storage_version" not in call_match.group(1):
        fail(
            "Erwarteter Versionsstand wird nicht an alle "
            f"Helper übergeben: {call_name}"
        )

for forbidden_field in (
    "external_operation_id uuid,",
    "operation_identity text,",
    "payload_fingerprint text,",
    "client_request_key_hash",
    "request_fingerprint",
    "auth_user_id uuid,",
    "participant_id",
    "canonical_byte_length integer,",
):
    if forbidden_field in returns:
        fail(f"Internes Rückgabefeld ist erlaubt: {forbidden_field}")

if "'payload_fingerprint'," in sql_compact:
    fail("Payload-Fingerprint wird im Clientresultat aufgebaut.")
if "'external_operation_id'," in sql_compact:
    fail("Operations-UUID wird im Clientresultat aufgebaut.")

for role in ("public", "anon", "authenticated"):
    pattern = (
        r"revoke\s+all\s+on\s+function\s+"
        r"public\.accaoui_mutate_exam_history_domain"
        r"\s*\(\s*text\s*,\s*text\s*,\s*text\s*,\s*"
        r"text\s*,\s*bigint\s*,\s*jsonb\s*\)\s+from\s+"
        + re.escape(role)
        + r"\s*;"
    )
    if not re.search(
        pattern,
        sql,
        flags=re.IGNORECASE | re.DOTALL,
    ):
        fail(f"Äußerer RPC-Revoke fehlt: {role}")

for forbidden in (
    "grant execute",
    "create policy",
    "service_role",
    "sqlerrm",
    "insert into public.",
    "update public.",
    "delete from public.",
    "exam_history_domain_resources",
    "exam_history_idempotency_operations",
    "exam_history_operation_identity_issuances",
):
    if forbidden in sql_compact:
        fail(f"Unzulässiger Inhalt im äußeren RPC: {forbidden}")

v2731u_files = sorted(
    path.name for path in MIGRATIONS.glob("*v2731u*.sql")
)
if v2731u_files != [
    "20260723_v2731u_"
    "exam_history_outer_domain_mutation_rpc.sql"
]:
    fail(f"Unerwartete v27.31u-SQL-Dateien: {v2731u_files}")

for frontend_path in (
    ROOT / "index.html",
    ROOT / "app.js",
    ROOT / "patch-v21.js",
    ROOT / "data" / "supabase-client-adapter.js",
):
    frontend = frontend_path.read_text(encoding="utf-8").lower()
    if "accaoui_mutate_exam_history_domain" in frontend:
        fail(
            "Äußerer RPC ist vor Live-Freigabe im Frontend "
            f"referenziert: {frontend_path.name}"
        )

print("Äußerer Fachmutations-RPC-Vertrag: OK")
print(
    "Transaktion: Payload, Ausstellung, Reservierung, Mutation "
    "und Abschluss in einem Datenbankaufruf"
)
print(
    "Retry: Pending ohne Wiederholung, Completed/Failed aus "
    "gespeichertem Ergebnis"
)
print(
    "Fehler: erwartete Domain-Fehler nach Teilrollback stabil "
    "als Failed abgeschlossen"
)
print(
    "Clientantwort: keine UUIDs, Hashes, Fingerprints oder "
    "rohen Datenbankfehler"
)
print("Direkte Ausführung: vollständig gesperrt")
print("Produktive Freigabe: nein")
print("Live-Ausführung: nein")
