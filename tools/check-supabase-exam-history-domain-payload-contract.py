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
    / "exam-history-domain-payload-contract.json"
)

OUTER_CONTRACT_PATH = (
    ROOT
    / "docs"
    / "contracts"
    / "exam-history-outer-domain-mutation-rpc-interface-contract.json"
)


def fail(message: str) -> None:
    print(f"FEHLER: {message}")
    sys.exit(1)


def read_json(path: Path, label: str):
    if not path.is_file():
        fail(f"{label} fehlt.")

    try:
        return json.loads(
            path.read_text(encoding="utf-8")
        )
    except Exception as exc:
        fail(f"{label} ungültig: {exc}")


contract = read_json(
    CONTRACT_PATH,
    "Fach-Payload-Vertrag",
)

expected_top_level_keys = {
    "version",
    "contractVersion",
    "status",
    "productiveReleaseAllowed",
    "canonicalization",
    "sharedRules",
    "scopes",
    "operationRules",
    "stableCommonFailures",
    "unresolvedRequirements",
}

if set(contract) != expected_top_level_keys:
    fail(
        "Unerwartete Fach-Payload-Vertragsfelder: "
        f"{sorted(set(contract) - expected_top_level_keys)}"
    )

if contract["version"] != "v27.31m":
    fail("Fach-Payload-Vertrag besitzt nicht v27.31m.")

if contract["contractVersion"] != 1:
    fail("Fach-Payload-Vertrag besitzt nicht Schema 1.")

if contract["status"] != "prepared_not_live":
    fail("Fach-Payload-Vertrag ist nicht vorbereitet.")

if contract["productiveReleaseAllowed"] is not False:
    fail("Produktive Freigabe darf noch nicht erlaubt sein.")

expected_canonicalization = {
    "inputType": "jsonb",
    "canonicalTextSource": "postgres_jsonb_text",
    "textEncoding": "UTF8",
    "fingerprintAlgorithm": "sha256",
    "fingerprintFormat": "lowercase_hex_64",
    "fingerprintGeneratedServerSide": True,
    "clientFingerprintAllowed": False,
    "canonicalByteLengthGeneratedServerSide": True,
    "validationHelper": (
        "public."
        "accaoui_validate_exam_history_domain_payload"
    ),
    "validationHelperImplementationPresent": True,
    "validationHelperDirectExecutionAllowed": False,
}

if contract["canonicalization"] != expected_canonicalization:
    fail("Payload-Kanonisierung ist nicht kanonisch.")

expected_shared_rules = {
    "writePayloadRequired": True,
    "writePayloadMustBeObject": True,
    "deletePayloadMustBeNull": True,
    "additionalEnvelopeFieldsAllowed": False,
    "maximumNestingDepth": 16,
    "rawDatabaseErrorAllowed": False,
    "rawPayloadStoredInIssuanceTable": False,
    "rawPayloadStoredInIdempotencyTable": False,
    "forbiddenRecursiveKeys": [
        "external_operation_id",
        "operation_identity",
        "payload_fingerprint",
        "client_request_key_hash",
        "request_fingerprint",
        "service_role",
        "raw_database_error",
    ],
}

if contract["sharedRules"] != expected_shared_rules:
    fail("Gemeinsame Payload-Regeln sind nicht kanonisch.")

expected_snapshot = {
    "operationScope": "snapshot",
    "writeEnvelopeFields": [
        "schema_version",
        "snapshot",
    ],
    "schemaVersion": 1,
    "contentField": "snapshot",
    "contentType": "object",
    "emptyContentAllowed": False,
    "maximumCanonicalBytes": 262144,
    "deletePayload": None,
    "stableFailures": [
        "snapshot_payload_required",
        "snapshot_payload_must_be_object",
        "snapshot_payload_fields_invalid",
        "snapshot_schema_version_invalid",
        "snapshot_content_invalid",
        "snapshot_payload_too_large",
        "snapshot_payload_depth_exceeded",
        "snapshot_payload_forbidden_key",
    ],
}

expected_registry = {
    "operationScope": "cycle_registry",
    "writeEnvelopeFields": [
        "schema_version",
        "registry",
    ],
    "schemaVersion": 1,
    "contentField": "registry",
    "contentType": "object",
    "emptyContentAllowed": True,
    "maximumCanonicalBytes": 131072,
    "deletePayload": None,
    "stableFailures": [
        "cycle_registry_payload_required",
        "cycle_registry_payload_must_be_object",
        "cycle_registry_payload_fields_invalid",
        "cycle_registry_schema_version_invalid",
        "cycle_registry_content_invalid",
        "cycle_registry_payload_too_large",
        "cycle_registry_payload_depth_exceeded",
        "cycle_registry_payload_forbidden_key",
    ],
}

scopes = contract["scopes"]

if set(scopes) != {
    "snapshot",
    "cycle_registry",
}:
    fail("Fach-Payload-Bereiche sind unvollständig.")

if scopes["snapshot"] != expected_snapshot:
    fail("Snapshot-Payload-Vertrag ist nicht kanonisch.")

if scopes["cycle_registry"] != expected_registry:
    fail("Zyklusregister-Payload-Vertrag ist nicht kanonisch.")

expected_operation_rules = {
    "write": {
        "payloadRequired": True,
        "payloadFingerprintRequired": True,
        "payloadFingerprintSource": (
            "server_canonical_payload"
        ),
    },
    "delete": {
        "payloadRequired": False,
        "payloadMustBeNull": True,
        "payloadFingerprint": None,
    },
}

if contract["operationRules"] != expected_operation_rules:
    fail("Write-/Delete-Payload-Regeln sind nicht kanonisch.")

expected_common_failures = [
    "domain_payload_scope_invalid",
    "domain_payload_operation_invalid",
    "domain_payload_delete_must_be_null",
    "domain_payload_canonicalization_failed",
]

if contract["stableCommonFailures"] != expected_common_failures:
    fail("Gemeinsame stabile Fachfehler sind unvollständig.")

all_failures = (
    expected_common_failures
    + expected_snapshot["stableFailures"]
    + expected_registry["stableFailures"]
)

if len(all_failures) != len(set(all_failures)):
    fail("Stabile Fachfehler sind nicht eindeutig.")

for failure in all_failures:
    if (
        not failure
        or failure.lower() != failure
        or any(
            character not in
            "abcdefghijklmnopqrstuvwxyz0123456789_"
            for character in failure
        )
    ):
        fail(f"Ungültiger stabiler Fachfehler: {failure}")

expected_unresolved = {
    "outerDomainMutationRpcImplementation": True,
    "domainStorageImplementation": True,
    "payloadValidationHelperImplementation": False,
    "liveDatabaseTests": True,
    "concurrencyTests": True,
    "authorizationTests": True,
}

if contract["unresolvedRequirements"] != expected_unresolved:
    fail("Offene Fach-Payload-Anforderungen sind unvollständig.")

outer_contract = read_json(
    OUTER_CONTRACT_PATH,
    "Äußerer Fachmutations-RPC-Vertrag",
)

if outer_contract.get("version") != "v27.31n":
    fail("Äußerer RPC-Vertrag besitzt nicht v27.31n.")

if outer_contract.get(
    "productiveReleaseAllowed"
) is not False:
    fail("Äußerer RPC-Vertrag ist unerwartet produktiv.")

if outer_contract.get(
    "implementationPresent"
) is not False:
    fail("Äußerer RPC darf noch nicht umgesetzt sein.")

payload_rules = outer_contract.get(
    "payloadRules",
    {},
)

if payload_rules.get(
    "scopeSpecificSchemaStillRequired"
) is not False:
    fail(
        "Bereichsspezifische Payload-Verträge wurden im "
        "äußeren RPC-Vertrag nicht abgeschlossen."
    )

outer_unresolved = outer_contract.get(
    "unresolvedRequirements",
    {},
)

if outer_unresolved.get(
    "scopeSpecificPayloadSchemas"
) is not False:
    fail(
        "Payload-Schemas sind im äußeren Vertrag noch offen."
    )

if outer_unresolved.get(
    "outerDomainMutationRpcImplementation"
) is not True:
    fail(
        "Äußerer Fachmutations-RPC muss noch offen bleiben."
    )

VALIDATION_RPC_PATH = (
    MIGRATIONS
    / "20260722_v2731m_"
    "exam_history_domain_payload_validate_rpc.sql"
)

if not VALIDATION_RPC_PATH.is_file():
    fail("Fach-Payload-Validierungs-RPC fehlt.")

validation_sql = VALIDATION_RPC_PATH.read_text(
    encoding="utf-8"
)

validation_without_comments = re.sub(
    r"--.*?$",
    "",
    validation_sql.lower(),
    flags=re.MULTILINE,
)

validation_compact = re.sub(
    r"\s+",
    " ",
    validation_without_comments,
).strip()

function_name = (
    "public."
    "accaoui_validate_exam_history_domain_payload"
)

function_match = re.search(
    r"function\s+"
    r"public\.accaoui_validate_exam_history_domain_payload"
    r"\s*\((.*?)\)\s*returns\s+table\s*"
    r"\((.*?)\)\s*language\s+plpgsql",
    validation_sql,
    flags=re.IGNORECASE | re.DOTALL,
)

if not function_match:
    fail("Signatur des Fach-Payload-Validierungs-RPC fehlt.")

parameters = re.sub(
    r"\s+",
    " ",
    function_match.group(1).strip().lower(),
)

expected_parameters = (
    "p_operation_scope text, "
    "p_operation text, "
    "p_domain_payload jsonb default null"
)

if parameters != expected_parameters:
    fail(
        "Fach-Payload-Validierungs-RPC besitzt "
        "unerwartete Parameter: "
        f"{parameters}"
    )

returns = re.sub(
    r"\s+",
    " ",
    function_match.group(2).strip().lower(),
)

expected_returns = (
    "canonical_payload jsonb, "
    "payload_fingerprint text, "
    "canonical_byte_length integer"
)

if returns != expected_returns:
    fail(
        "Fach-Payload-Validierungs-RPC besitzt "
        "unerwartete Rückgabe: "
        f"{returns}"
    )

required_markers = (
    "security definer",
    "set search_path = pg_catalog, public",
    "set row_security = off",
    "p_operation_scope not in ( "
    "'snapshot', 'cycle_registry' )",
    "p_operation not in ( 'write', 'delete' )",
    "jsonb_object_length(p_domain_payload) <> 2",
    "p_domain_payload ? 'schema_version'",
    "p_domain_payload ? 'snapshot'",
    "p_domain_payload ? 'registry'",
    "p_domain_payload ->> 'schema_version' <> '1'",
    "p_domain_payload -> 'snapshot' = '{}'::jsonb",
    "with recursive payload_nodes(value, depth) as",
    "v_max_depth > 16",
    "jsonb_object_keys(",
    "v_canonical_text := p_domain_payload::text",
    "octet_length( convert_to( "
    "v_canonical_text, 'utf8' ) )",
    "v_canonical_bytes > 262144",
    "v_canonical_bytes > 131072",
    "public.digest(",
    "'sha256'",
    "v_payload_fingerprint !~ '^[0-9a-f]{64}$'",
    "select null::jsonb, null::text, 0::integer",
    "select p_domain_payload, "
    "v_payload_fingerprint, v_canonical_bytes",
)

for marker in required_markers:
    if marker not in validation_compact:
        fail(
            "Fach-Payload-Validierungs-RPC: "
            f"Anweisung fehlt: {marker}"
        )

stable_failures = (
    contract["stableCommonFailures"]
    + contract["scopes"]["snapshot"]["stableFailures"]
    + contract["scopes"]["cycle_registry"]["stableFailures"]
)

for failure_code in stable_failures:
    marker = f"message = '{failure_code}'"

    if marker not in validation_compact:
        fail(
            "Stabiler Fachfehler fehlt im SQL-Helfer: "
            f"{failure_code}"
        )

for forbidden_parameter in (
    "p_external_operation_id",
    "p_operation_identity",
    "p_payload_fingerprint",
    "p_client_request_key",
    "p_auth_user_id",
    "p_participant_id",
):
    if forbidden_parameter in parameters:
        fail(
            "Verbotener Parameter im Payload-Helfer: "
            f"{forbidden_parameter}"
        )

mutation_targets = [
    (
        re.sub(r"\s+", " ", action.lower()),
        table.lower(),
    )
    for action, table in re.findall(
        r"\b(insert\s+into|update|delete\s+from)\s+"
        r"(?:public\.)?([a-z_]+)",
        validation_without_comments,
        flags=re.IGNORECASE,
    )
]

if mutation_targets:
    fail(
        "Payload-Helfer verändert unerwartete Tabellen: "
        f"{mutation_targets}"
    )

for forbidden_content in (
    "grant execute",
    "create policy",
    "auth.uid()",
    "sqlerrm",
    "stacked diagnostics",
    "accaoui_issue_exam_history_operation_identity",
    "accaoui_reserve_exam_history_idempotency_operation",
    "accaoui_complete_exam_history_idempotency_operation",
    "public.exam_history_idempotency_operations",
    "public.exam_history_operation_identity_issuances",
):
    if forbidden_content in validation_without_comments:
        fail(
            "Unzulässiger Inhalt im Payload-Helfer: "
            f"{forbidden_content}"
        )

for role in (
    "public",
    "anon",
    "authenticated",
):
    revoke_pattern = (
        r"revoke\s+all\s+on\s+function\s+"
        r"public\.accaoui_validate_exam_history_domain_payload"
        r"\s*\(\s*text\s*,\s*text\s*,\s*jsonb\s*\)"
        r"\s+from\s+"
        + re.escape(role)
        + r"\s*;"
    )

    if not re.search(
        revoke_pattern,
        validation_sql,
        flags=re.IGNORECASE | re.DOTALL,
    ):
        fail(
            "Payload-Helfer-Revoke fehlt für: "
            f"{role}"
        )

v2731m_sql_files = sorted(
    path.name
    for path in MIGRATIONS.glob("*v2731m*.sql")
)

if v2731m_sql_files != [
    "20260722_v2731m_"
    "exam_history_domain_payload_validate_rpc.sql"
]:
    fail(
        "Unerwartete v27.31m-SQL-Dateien: "
        f"{v2731m_sql_files}"
    )

for frontend_path in (
    ROOT / "index.html",
    ROOT / "app.js",
    ROOT / "patch-v21.js",
    ROOT / "data" / "supabase-client-adapter.js",
):
    frontend_text = frontend_path.read_text(
        encoding="utf-8"
    ).lower()

    if CONTRACT_PATH.name.lower() in frontend_text:
        fail(
            "Fach-Payload-Vertrag darf nicht im Frontend "
            f"geladen werden: {frontend_path.name}"
        )

print("Kanonischer Fach-Payload-Vertrag: OK")
print(
    "Payload-Validierungs-RPC: Hülle, Tiefe, "
    "Schlüssel und Größe serverseitig geprüft"
)
print(
    "Payload-Fingerprint-Helfer: kanonisches JSONB "
    "mit SHA-256 abgeleitet"
)
print(
    "Payload-Helfer-Mutationen: keine"
)
print(
    "Snapshot Write: schema_version und Snapshot-Objekt, "
    "maximal 262144 kanonische Bytes"
)
print(
    "Zyklusregister Write: schema_version und Register-Objekt, "
    "maximal 131072 kanonische Bytes"
)
print(
    "Delete-Payload: für beide Bereiche ausschließlich null"
)
print(
    "Kanonisierung: PostgreSQL-JSONB-Text in UTF-8"
)
print(
    "Payload-Fingerprint: serverseitiges SHA-256 als "
    "64-stelliges Lowercase-Hex"
)
print(
    "Zusätzliche Hüllenfelder und interne Identitätsfelder: "
    "gesperrt"
)
print("Äußerer RPC implementiert: nein")
print("Produktive Freigabe: nein")
print("Live-Ausführung: nein")
