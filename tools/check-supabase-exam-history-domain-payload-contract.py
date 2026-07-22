from pathlib import Path
import json
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

if contract["version"] != "v27.31l":
    fail("Fach-Payload-Vertrag besitzt nicht v27.31l.")

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

if outer_contract.get("version") != "v27.31l":
    fail("Äußerer RPC-Vertrag besitzt nicht v27.31l.")

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

v2731l_sql_files = sorted(
    path.name
    for path in MIGRATIONS.glob("*v2731l*.sql")
)

if v2731l_sql_files:
    fail(
        "v27.31l darf keine SQL-Migration erzeugen: "
        f"{v2731l_sql_files}"
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
