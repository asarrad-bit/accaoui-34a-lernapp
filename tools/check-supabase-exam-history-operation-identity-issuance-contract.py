from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

CONTRACT_PATH = (
    ROOT
    / "docs"
    / "contracts"
    / "exam-history-operation-identity-issuance-contract.json"
)

TRANSACTION_CONTRACT_PATH = (
    ROOT
    / "docs"
    / "contracts"
    / "exam-history-idempotency-transactional-mutation-contract.json"
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
    "Operations-ID-Ausstellungsvertrag",
)

expected_top_level_keys = {
    "version",
    "contractVersion",
    "status",
    "productiveReleaseAllowed",
    "identityAuthority",
    "clientCorrelation",
    "issuanceRequest",
    "verifiedIdentityRecord",
    "reuseRules",
    "conflictRules",
    "securityRules",
    "unresolvedRequirements",
}

if set(contract) != expected_top_level_keys:
    fail(
        "Unerwartete Ausstellungsvertragsfelder: "
        f"{sorted(set(contract) - expected_top_level_keys)}"
    )

if contract["version"] != "v27.31u":
    fail("Ausstellungsvertragsversion ist nicht v27.31u.")

if contract["contractVersion"] != 1:
    fail("Ausstellungsvertragsschema ist nicht Version 1.")

if contract["status"] != "prepared_not_live":
    fail("Ausstellungsvertrag ist nicht als vorbereitet markiert.")

if contract["productiveReleaseAllowed"] is not False:
    fail("Produktive Freigabe darf noch nicht erlaubt sein.")

expected_authority = {
    "authority": "database_persisted_issuance_record",
    "issuer": "trusted_security_definer_rpc",
    "externalOperationIdAlgorithm": "uuid_v4",
    "generatedInsideDatabase": True,
    "clientSuppliedOperationIdTrusted": False,
    "clientSuppliedOperationIdAcceptedAsAuthority": False,
    "operationIdAloneSufficientForVerification": False,
    "verificationNow": True,
    "liveExecution": False,
}

if contract["identityAuthority"] != expected_authority:
    fail("Operations-ID-Autoritätsgrenze ist nicht kanonisch.")

expected_client_correlation = {
    "fieldName": "client_request_key",
    "source": "untrusted_client_correlation_hint",
    "browserGeneratedAllowed": True,
    "trusted": False,
    "purpose": "retry_lookup_only",
    "minimumEntropyBits": 128,
    "rawStorageAllowed": False,
    "storedRepresentation": "sha256_hash",
    "mayAuthorizeMutation": False,
    "becomesOperationIdentity": False,
    "reuseRequiredForRetry": True,
}

if contract["clientCorrelation"] != expected_client_correlation:
    fail("Client-Wiederholungsschlüssel ist nicht sicher begrenzt.")

expected_issuance_request = {
    "authUserSource": "auth_uid_only",
    "authorizationRequiredBeforeIssuance": True,
    "canonicalFields": [
        "operation_scope",
        "operation",
        "resource_identity",
        "expected_storage_version",
        "payload_fingerprint",
    ],
    "clientRequestKeyIncludedInRequestFingerprint": False,
    "requestFingerprintAlgorithm": "sha256_canonical_json",
    "requestFingerprintGeneratedBy": (
        "database_or_trusted_server"
    ),
    "operationIdReturnedOnlyAfterPersistence": True,
}

if contract["issuanceRequest"] != expected_issuance_request:
    fail("Operations-ID-Ausstellungsanfrage ist nicht kanonisch.")

expected_record = {
    "requiredFields": [
        "auth_user_id",
        "client_request_key_hash",
        "request_fingerprint",
        "external_operation_id",
        "operation_scope",
        "operation",
        "resource_identity",
        "expected_storage_version",
        "payload_fingerprint",
        "issued_at",
    ],
    "lookupRequiresFullCanonicalRequest": True,
    "foreignUserLookupAllowed": False,
    "missingRecordMeansUnverified": True,
}

if contract["verifiedIdentityRecord"] != expected_record:
    fail("Verifizierter Operations-ID-Datensatz ist unvollständig.")

expected_reuse_rules = {
    "sameUserSameClientRequestKeySameFingerprintReturnsSameOperationId": True,
    "sameUserSameClientRequestKeyDifferentFingerprintAllowed": False,
    "sameOperationIdWithoutIssuanceRecordAllowed": False,
    "retryMayExecuteDomainMutationWithoutReservation": False,
    "identityReuseAcrossUsersAllowed": False,
}

if contract["reuseRules"] != expected_reuse_rules:
    fail("Operations-ID-Wiederverwendungsregeln sind unsicher.")

expected_conflict_rules = {
    "sameRequestKeyDifferentRequestFingerprint": (
        "reject_request_key_conflict"
    ),
    "suppliedOperationIdWithoutRecord": (
        "reject_unverified_operation_id"
    ),
    "suppliedOperationIdRecordMismatch": (
        "reject_operation_identity_mismatch"
    ),
    "foreignUserRecord": "reject_operation_owner_conflict",
    "sameRequestKeyDifferentExpectedStorageVersion": (
        "reject_request_key_conflict"
    ),
    "rawExistingValuesReturned": False,
}

if contract["conflictRules"] != expected_conflict_rules:
    fail("Operations-ID-Konfliktregeln sind nicht kanonisch.")

expected_security_rules = {
    "authUserFromAuthUidOnly": True,
    "participantIdParameterAllowed": False,
    "authUserIdParameterAllowed": False,
    "serviceRoleInFrontendAllowed": False,
    "directIssuanceTableGrantAllowed": False,
    "directIssuanceHelperGrantAllowed": False,
    "rawDatabaseErrorReturned": False,
}

if contract["securityRules"] != expected_security_rules:
    fail("Operations-ID-Sicherheitsregeln sind nicht kanonisch.")

expected_unresolved = {
    "issuanceTableImplementation": False,
    "issuanceRpcImplementation": False,
    "issuanceExpectedStorageVersionBinding": False,
    "domainMutationRpcImplementation": False,
    "liveDatabaseTests": True,
    "concurrencyTests": True,
}

if contract["unresolvedRequirements"] != expected_unresolved:
    fail("Offene Operations-ID-Anforderungen sind unvollständig.")

transaction_contract = read_json(
    TRANSACTION_CONTRACT_PATH,
    "Transaktionaler Fachmutationsvertrag",
)

if transaction_contract.get(
    "productiveReleaseAllowed"
) is not False:
    fail(
        "Transaktionaler Vertrag darf noch nicht "
        "produktiv freigegeben sein."
    )

transaction_unresolved = transaction_contract.get(
    "unresolvedRequirements",
    {},
)

if transaction_unresolved.get(
    "trustedOperationIdentityIssuance"
) is not False:
    fail(
        "Vertrauenswürdige Operations-ID-Ausstellung "
        "ist nicht vollständig integriert."
    )

ISSUANCE_TABLE_PATH = (
    ROOT
    / "supabase"
    / "migrations"
    / "20260722_v2731h_exam_history_operation_identity_issuances.sql"
)

if not ISSUANCE_TABLE_PATH.is_file():
    fail("Operations-ID-Ausstellungstabelle fehlt.")

issuance_sql = ISSUANCE_TABLE_PATH.read_text(
    encoding="utf-8"
)

issuance_without_comments = re.sub(
    r"--.*?$",
    "",
    issuance_sql.lower(),
    flags=re.MULTILINE,
)

issuance_compact = re.sub(
    r"\s+",
    " ",
    issuance_without_comments,
).strip()

required_issuance_markers = (
    "create table if not exists "
    "public.exam_history_operation_identity_issuances",
    "auth_user_id uuid not null",
    "client_request_key_hash text not null",
    "client_request_key_hash ~ '^[0-9a-f]{64}$'",
    "request_fingerprint text not null",
    "request_fingerprint ~ '^[0-9a-f]{64}$'",
    "external_operation_id uuid not null "
    "default gen_random_uuid()",
    "external_operation_id::text ~ "
    "'^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-"
    "[89ab][0-9a-f]{3}-[0-9a-f]{12}$'",
    "operation_scope in ( 'snapshot', 'cycle_registry' )",
    "operation in ( 'write', 'delete' )",
    "resource_identity = trim(resource_identity)",
    "length(resource_identity) between 1 and 512",
    "unique ( auth_user_id, client_request_key_hash )",
    "unique ( external_operation_id )",
    "payload_fingerprint ~ '^[0-9a-f]{64}$'",
    "alter table "
    "public.exam_history_operation_identity_issuances "
    "enable row level security",
    "alter table "
    "public.exam_history_operation_identity_issuances "
    "force row level security",
    "revoke all on table "
    "public.exam_history_operation_identity_issuances "
    "from public, anon, authenticated",
)

for marker in required_issuance_markers:
    if marker not in issuance_compact:
        fail(
            "Operations-ID-Ausstellungstabelle: "
            f"Anweisung fehlt: {marker}"
        )

for forbidden in (
    "create policy",
    "grant ",
    "security definer",
    "auth.uid()",
    "service_role",
    "client_request_key text",
    "insert into",
    "update public.",
    "delete from",
    "drop table",
    "truncate ",
):
    if forbidden in issuance_without_comments:
        fail(
            "Unzulässiger Inhalt in der "
            "Operations-ID-Ausstellungstabelle: "
            f"{forbidden}"
        )


ISSUANCE_RPC_PATH = (
    ROOT
    / "supabase"
    / "migrations"
    / "20260722_v2731q_"
      "exam_history_operation_identity_expected_version_rpc.sql"
)

if not ISSUANCE_RPC_PATH.is_file():
    fail("Operations-ID-Ausstellungs-RPC fehlt.")

issuance_rpc = ISSUANCE_RPC_PATH.read_text(
    encoding="utf-8"
)

issuance_rpc_lower = issuance_rpc.lower()

issuance_rpc_without_comments = re.sub(
    r"--.*?$",
    "",
    issuance_rpc_lower,
    flags=re.MULTILINE,
)

issuance_rpc_compact = re.sub(
    r"\s+",
    " ",
    issuance_rpc_without_comments,
).strip()

required_rpc_markers = (
    "create or replace function "
    "public.accaoui_issue_exam_history_operation_identity(",
    "language plpgsql",
    "security definer",
    "set search_path = pg_catalog, public",
    "set row_security = off",
    "v_auth_user_id := auth.uid()",
    "message = 'authentication_required'",
    "p_client_request_key !~ '^[0-9a-f]{64}$'",
    "message = 'client_request_key_invalid'",
    "message = 'operation_scope_invalid'",
    "message = 'operation_invalid'",
    "message = 'resource_identity_invalid'",
    "p_expected_storage_version bigint",
    "message = 'expected_storage_version_invalid'",
    "message = 'payload_fingerprint_invalid'",
    "message = 'delete_payload_fingerprint_not_allowed'",
    "digest( convert_to( p_client_request_key, 'utf8' ), "
    "'sha256' )",
    "jsonb_build_object(",
    "'operation_scope', p_operation_scope",
    "'operation', p_operation",
    "'resource_identity', p_resource_identity",
    "'expected_storage_version', "
    "p_expected_storage_version",
    "'payload_fingerprint', p_payload_fingerprint",
    "insert into "
    "public.exam_history_operation_identity_issuances "
    "as issuance",
    "on conflict do nothing",
    "issuance.external_operation_id",
    "'issued_new'::text",
    "select issuance.* into v_existing",
    "for update",
    "message = "
    "'operation_identity_issuance_conflict_unresolved'",
    "v_existing.request_fingerprint <> "
    "v_request_fingerprint",
    "v_existing.expected_storage_version <> "
    "p_expected_storage_version",
    "v_existing.payload_fingerprint "
    "is distinct from p_payload_fingerprint",
    "message = "
    "'operation_identity_request_key_conflict'",
    "'issued_existing'::text",
)

for marker in required_rpc_markers:
    if marker not in issuance_rpc_compact:
        fail(
            "Operations-ID-Ausstellungs-RPC: "
            f"Anweisung fehlt: {marker}"
        )

if len(
    re.findall(
        r"create\s+or\s+replace\s+function\s+"
        r"public\.accaoui_issue_exam_history_"
        r"operation_identity\s*\(",
        issuance_rpc,
        flags=re.IGNORECASE,
    )
) != 1:
    fail(
        "Operations-ID-Ausstellungs-RPC muss genau einmal "
        "vorhanden sein."
    )

rpc_match = re.search(
    r"function\s+"
    r"public\.accaoui_issue_exam_history_operation_identity"
    r"\s*\((.*?)\)\s*returns\s+table\s*"
    r"\((.*?)\)\s*language\s+plpgsql",
    issuance_rpc,
    flags=re.IGNORECASE | re.DOTALL,
)

if not rpc_match:
    fail(
        "Signatur des Operations-ID-Ausstellungs-RPC fehlt."
    )

rpc_parameters = re.sub(
    r"\s+",
    " ",
    rpc_match.group(1).strip().lower(),
)

expected_rpc_parameters = (
    "p_client_request_key text, "
    "p_operation_scope text, "
    "p_operation text, "
    "p_resource_identity text, "
    "p_expected_storage_version bigint, "
    "p_payload_fingerprint text default null"
)

if rpc_parameters != expected_rpc_parameters:
    fail(
        "Operations-ID-Ausstellungs-RPC besitzt "
        "unerwartete Parameter: "
        f"{rpc_parameters}"
    )

rpc_returns = re.sub(
    r"\s+",
    " ",
    rpc_match.group(2).strip().lower(),
)

expected_rpc_returns = (
    "external_operation_id uuid, "
    "issuance_status text, "
    "issued_at timestamptz, "
    "is_new boolean"
)

if rpc_returns != expected_rpc_returns:
    fail(
        "Operations-ID-Ausstellungs-RPC gibt "
        "unerwartete Spalten zurück: "
        f"{rpc_returns}"
    )

for forbidden_parameter in (
    "p_auth_user_id",
    "p_participant_id",
    "p_external_operation_id",
    "p_client_request_key_hash",
    "p_request_fingerprint",
    "p_issued_at",
):
    if forbidden_parameter in rpc_parameters:
        fail(
            "Verbotener Browserparameter im "
            "Operations-ID-Ausstellungs-RPC: "
            f"{forbidden_parameter}"
        )

for role in (
    "public",
    "anon",
    "authenticated",
):
    revoke_pattern = (
        r"revoke\s+all\s+on\s+function\s+"
        r"public\.accaoui_issue_exam_history_"
        r"operation_identity\s*\(\s*"
        r"text\s*,\s*text\s*,\s*text\s*,\s*"
        r"text\s*,\s*bigint\s*,\s*text\s*"
        r"\)\s+from\s+"
        + re.escape(role)
        + r"\s*;"
    )

    if not re.search(
        revoke_pattern,
        issuance_rpc,
        flags=re.IGNORECASE | re.DOTALL,
    ):
        fail(
            "Operations-ID-Ausstellungs-RPC-Revoke fehlt für: "
            f"{role}"
        )

if (
    "'client_request_key', p_client_request_key"
    in issuance_rpc_compact
):
    fail(
        "Roher Client-Wiederholungsschlüssel darf nicht im "
        "kanonischen Anfragefingerprint liegen."
    )

if "expected_storage_version" not in issuance_rpc_compact:
    fail("Ausstellungs-RPC bindet den Versionsstand nicht.")

mutation_targets = [
    (
        re.sub(r"\s+", " ", action.lower()),
        table.lower(),
    )
    for action, table in re.findall(
        r"\b(insert\s+into|update|delete\s+from)\s+"
        r"(?:public\.)?([a-z_]+)",
        issuance_rpc_without_comments,
        flags=re.IGNORECASE,
    )
]

if mutation_targets != [
    (
        "insert into",
        "exam_history_operation_identity_issuances",
    ),
]:
    fail(
        "Operations-ID-Ausstellungs-RPC verändert "
        "unerwartete Tabellen: "
        f"{mutation_targets}"
    )

for forbidden_content in (
    "grant execute",
    "create policy",
    "service_role",
    "sqlerrm",
    "stacked diagnostics",
    "insert into public.exam_history_idempotency_operations",
    "update public.exam_history_operation_identity_issuances",
    "delete from public.exam_history_operation_identity_issuances",
    "public.exam_attempts",
    "public.exam_answers",
    "public.exam_attempt_questions",
    "public.exam_question_answer_keys",
    "public.exam_attempt_question_answer_keys",
):
    if forbidden_content in issuance_rpc_without_comments:
        fail(
            "Unzulässiger Inhalt im "
            "Operations-ID-Ausstellungs-RPC: "
            f"{forbidden_content}"
        )

for frontend_path in (
    ROOT / "index.html",
    ROOT / "app.js",
    ROOT / "patch-v21.js",
):
    frontend_text = frontend_path.read_text(
        encoding="utf-8"
    ).lower()

    if CONTRACT_PATH.name.lower() in frontend_text:
        fail(
            "Operations-ID-Vertrag darf nicht im Frontend "
            f"geladen werden: {frontend_path.name}"
        )

print("Operations-ID-Ausstellungsvertrag: OK")
print(
    "Ausstellungstabelle: gehashter Retry-Schlüssel, "
    "Anfragefingerprint und UUID gesperrt gespeichert"
)
print(
    "Ausstellungs-RPC: Client-Schlüssel separat gehasht; "
    "kanonische Anfrage bindet den erwarteten Versionsstand"
)
print(
    "Ausstellungs-RPC: neue UUID gespeichert oder "
    "identische UUID wiederverwendet"
)
print(
    "Browser-Schlüssel: erlaubt, aber ausschließlich "
    "unvertrauenswürdiger Wiederholungshinweis"
)
print(
    "Operations-UUID: nur serverseitig ausgestellt und "
    "persistiert vertrauenswürdig"
)
print(
    "Wiederholung: gleicher Nutzer, Schlüssel und Fingerprint "
    "erhalten dieselbe UUID"
)
print(
    "Konflikt: gleicher Schlüssel mit anderem Vorgang "
    "geschlossen abgelehnt"
)
print(
    "Operations-ID allein: kein ausreichender "
    "Vertrauensnachweis"
)
print(
    "Äußere Integration: Ausstellung wird ausschließlich "
    "innerhalb des gesperrten Fachmutations-RPC verwendet"
)
print("Produktive Freigabe: nein")
print("Live-Ausführung: nein")
