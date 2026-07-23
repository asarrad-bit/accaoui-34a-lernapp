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
    / "exam-history-domain-storage-contract.json"
)

OUTER_CONTRACT_PATH = (
    ROOT
    / "docs"
    / "contracts"
    / "exam-history-outer-domain-mutation-rpc-interface-contract.json"
)

PAYLOAD_CONTRACT_PATH = (
    ROOT
    / "docs"
    / "contracts"
    / "exam-history-domain-payload-contract.json"
)

VALIDATION_RPC_PATH = (
    MIGRATIONS
    / "20260722_v2731m_"
      "exam_history_domain_payload_validate_rpc.sql"
)

STORAGE_TABLE_PATH = (
    MIGRATIONS
    / "20260723_v2731s_"
      "exam_history_domain_resources.sql"
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


def without_comments(text: str) -> str:
    return re.sub(
        r"--.*?$",
        "",
        text,
        flags=re.MULTILINE,
    )


def compact(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


contract = read_json(CONTRACT_PATH, "Domain-Speichervertrag")

if contract.get("version") != "v27.31s":
    fail("Domain-Speichervertrag besitzt nicht v27.31s.")

if contract.get("contractVersion") != 1:
    fail("Domain-Speichervertrag besitzt nicht Schema 1.")

if contract.get("status") != "prepared_not_live":
    fail("Domain-Speichervertrag ist nicht vorbereitet.")

if contract.get("productiveReleaseAllowed") is not False:
    fail("Domain-Speicher darf noch nicht produktiv sein.")

if contract.get("implementationPresent") is not True:
    fail("Domain-Speichertabelle ist nicht als vorbereitet markiert.")

storage = contract.get("storageModel", {})

if storage.get("proposedTable") != (
    "public.exam_history_domain_resources"
):
    fail("Domain-Speichertabellenname ist nicht kanonisch.")

if storage.get("rowIdentityFields") != [
    "auth_user_id",
    "operation_scope",
    "resource_identity",
]:
    fail("Domain-Speicheridentität ist nicht kanonisch.")

for field in (
    "oneCurrentRowPerIdentity",
    "uniqueIdentityRequired",
    "softDeleteTombstoneRequired",
    "monotonicStorageVersionRequired",
    "implementationPresent",
):
    if storage.get(field) is not True:
        fail(f"Domain-Speicherregel fehlt: {field}")

for field in (
    "physicalDeleteByMutationRpcAllowed",
    "versionResetAfterDeleteAllowed",
    "migrationLiveExecuted",
):
    if storage.get(field) is not False:
        fail(f"Unsichere Domain-Speicherregel: {field}")

if storage.get("migrationPath") != (
    "supabase/migrations/"
    "20260723_v2731s_exam_history_domain_resources.sql"
):
    fail("Domain-Speicher-Migrationspfad ist ungültig.")

stored_fields = contract.get("storedFields", [])
expected_field_names = [
    "id",
    "auth_user_id",
    "operation_scope",
    "resource_identity",
    "schema_version",
    "domain_payload",
    "payload_fingerprint",
    "canonical_byte_length",
    "storage_version",
    "is_deleted",
    "created_at",
    "updated_at",
]

if [field.get("name") for field in stored_fields] != expected_field_names:
    fail("Gespeicherte Domain-Felder sind nicht kanonisch.")

ownership = contract.get("ownershipRules", {})
if ownership != {
    "authUserFromAuthUidOnly": True,
    "authUserIdParameterAllowed": False,
    "participantIdParameterAllowed": False,
    "crossUserReadAllowed": False,
    "crossUserWriteAllowed": False,
    "crossUserDeleteAllowed": False,
}:
    fail("Domain-Speicher-Nutzerbindung ist ungültig.")

expected_version = contract.get("expectedVersionInput", {})
if expected_version != {
    "parameter": "p_expected_storage_version",
    "type": "bigint",
    "minimum": 0,
    "requiredForWrite": True,
    "requiredForDelete": True,
    "zeroMeansCreateOnly": True,
    "positiveMeansExactCurrentVersion": True,
    "clientMayInventCurrentVersion": False,
}:
    fail("Erwarteter Speicher-Versionsstand ist ungültig.")

write_rules = contract.get("writeSemantics", {})
if write_rules.get("newResourceExpectedVersion") != 0:
    fail("Neue Ressource verlangt nicht Version 0.")
if write_rules.get("newResourceStoredVersion") != 1:
    fail("Neue Ressource beginnt nicht mit Version 1.")
for field in (
    "existingLiveRowRequiresExactVersion",
    "existingTombstoneRequiresExactVersion",
):
    if write_rules.get(field) is not True:
        fail(f"Write-Versionsregel fehlt: {field}")
if write_rules.get("successfulWriteIncrementsVersionBy") != 1:
    fail("Write erhöht storage_version nicht exakt um 1.")
for field in (
    "samePayloadStillIncrementsVersion",
    "silentLastWriteWinsAllowed",
    "upsertWithoutVersionGuardAllowed",
):
    if write_rules.get(field) is not False:
        fail(f"Unsichere Write-Regel: {field}")

if write_rules.get("rowLockRequired") != "select_for_update":
    fail("Write verlangt keine Zeilensperre.")

if write_rules.get("payloadValidationHelper") != (
    "public.accaoui_validate_exam_history_domain_payload"
):
    fail("Fach-Payload-Validierungshelfer ist nicht kanonisch.")

delete_rules = contract.get("deleteSemantics", {})
for field in (
    "payloadMustBeNull",
    "existingLiveRowRequiresExactVersion",
    "successfulDeleteCreatesTombstone",
    "tombstonePayloadMustBeNull",
    "tombstoneFingerprintMustBeNull",
    "alreadyDeletedDoesNotIncrementVersion",
):
    if delete_rules.get(field) is not True:
        fail(f"Delete-Regel fehlt: {field}")
if delete_rules.get("successfulDeleteIncrementsVersionBy") != 1:
    fail("Delete erhöht storage_version nicht exakt um 1.")
if delete_rules.get("physicalDeleteAllowed") is not False:
    fail("Physisches Löschen ist im Mutationsweg erlaubt.")
if delete_rules.get("rowLockRequired") != "select_for_update":
    fail("Delete verlangt keine Zeilensperre.")

concurrency = contract.get("concurrencyRules", {})
for field in (
    "resourceRowLockedBeforeDecision",
    "uniqueCreateConflictMustBeReevaluated",
    "expectedVersionComparedInsideLock",
    "staleWriteRejected",
    "staleDeleteRejected",
    "abaVersionReusePreventedByTombstone",
    "domainMutationAndIdempotencyCompletionSameTransaction",
):
    if concurrency.get(field) is not True:
        fail(f"Konkurrenzregel fehlt: {field}")

identity_binding = contract.get("identityBinding", {})
if identity_binding != {
    "expectedStorageVersionMustAffectRequestIdentity": True,
    "currentIssuanceHelperBindsExpectedVersion": True,
    "currentReservationHelperBindsExpectedVersion": True,
    "outerRpcMayBeImplementedBeforeBinding": False,
}:
    fail("Versionsstand-Identitätsbindung ist ungültig.")

scope_limits = contract.get("scopeLimits", {})
if scope_limits != {
    "snapshot": {
        "maximumCanonicalBytes": 262144,
        "payloadRequiredWhenLive": True,
    },
    "cycle_registry": {
        "maximumCanonicalBytes": 131072,
        "payloadRequiredWhenLive": True,
    },
}:
    fail("Bereichsspezifische Speichergrenzen sind ungültig.")

access = contract.get("accessRules", {})
for field in (
    "rowLevelSecurityEnabled",
    "rowLevelSecurityForced",
):
    if access.get(field) is not True:
        fail(f"Tabellenschutzregel fehlt: {field}")
for field in (
    "directPoliciesAllowed",
    "publicTableRightsAllowed",
    "anonTableRightsAllowed",
    "authenticatedTableRightsAllowed",
    "directFrontendAccessAllowed",
    "serviceRoleInFrontendAllowed",
    "liveExecution",
):
    if access.get(field) is not False:
        fail(f"Unsichere Tabellenzugriffsregel: {field}")

if contract.get("stableOutcomes") != [
    "created",
    "updated",
    "deleted",
    "already_absent",
    "already_deleted",
]:
    fail("Stabile Domain-Speicherergebnisse sind ungültig.")

if contract.get("stableFailures") != [
    "domain_storage_expected_version_invalid",
    "domain_storage_version_conflict",
    "domain_storage_resource_identity_invalid",
    "domain_storage_scope_invalid",
    "domain_storage_payload_invalid",
    "domain_storage_state_invalid",
]:
    fail("Stabile Domain-Speicherfehler sind ungültig.")

expected_unresolved = {
    "expectedVersionIdentityBinding": True,
    "storageTableImplementation": False,
    "storageMutationHelperImplementation": True,
    "outerDomainMutationRpcImplementation": True,
    "liveDatabaseTests": True,
    "concurrencyTests": True,
    "authorizationTests": True,
}
if contract.get("unresolvedRequirements") != expected_unresolved:
    fail("Offene Domain-Speicheranforderungen sind ungültig.")

outer = read_json(
    OUTER_CONTRACT_PATH,
    "Äußerer Fachmutations-RPC-Vertrag",
)
if outer.get("version") != "v27.31n":
    fail("Äußerer RPC-Vertrag besitzt nicht v27.31n.")
if outer.get("unresolvedRequirements", {}).get(
    "expectedStorageVersionIdentityBinding"
) is not True:
    fail("End-to-End-Versionsbindung ist im äußeren Vertrag nicht offen.")

payload = read_json(PAYLOAD_CONTRACT_PATH, "Fach-Payload-Vertrag")
if payload.get("version") != "v27.31m":
    fail("Fach-Payload-Vertrag besitzt nicht v27.31m.")

if not VALIDATION_RPC_PATH.is_file():
    fail("Fach-Payload-Validierungs-RPC fehlt.")

if not STORAGE_TABLE_PATH.is_file():
    fail("Domain-Speichertabellen-Migration fehlt.")

sql = STORAGE_TABLE_PATH.read_text(encoding="utf-8")
sql_clean = without_comments(sql)
sql_lower = sql_clean.lower()
sql_compact = compact(sql_clean)

required_markers = (
    "message = 'exam_history_domain_resources_already_exists'",
    "create table public.exam_history_domain_resources (",
    "id uuid primary key default gen_random_uuid()",
    "auth_user_id uuid not null",
    "operation_scope text not null",
    "operation_scope in ( 'snapshot', 'cycle_registry' )",
    "resource_identity text not null",
    "resource_identity = trim(resource_identity)",
    "length(resource_identity) between 1 and 512",
    "schema_version smallint not null default 1",
    "check (schema_version = 1)",
    "domain_payload jsonb",
    "payload_fingerprint text",
    "canonical_byte_length integer",
    "storage_version bigint not null",
    "check (storage_version >= 1)",
    "is_deleted boolean not null default false",
    "created_at timestamptz not null default now()",
    "updated_at timestamptz not null default now()",
    "unique ( auth_user_id, operation_scope, resource_identity )",
    "payload_fingerprint ~ '^[0-9a-f]{64}$'",
    "jsonb_typeof(domain_payload) = 'object'",
    "operation_scope = 'snapshot'",
    "canonical_byte_length <= 262144",
    "operation_scope = 'cycle_registry'",
    "canonical_byte_length <= 131072",
    "is_deleted = true",
    "domain_payload is null",
    "payload_fingerprint is null",
    "canonical_byte_length is null",
    "check (updated_at >= created_at)",
    "idx_exam_history_domain_resources_user_scope_updated",
    "alter table public.exam_history_domain_resources enable row level security",
    "alter table public.exam_history_domain_resources force row level security",
    "revoke all on table public.exam_history_domain_resources from public, anon, authenticated",
)

for marker in required_markers:
    if marker not in sql_compact:
        fail(f"Domain-Speichertabellen-Anweisung fehlt: {marker}")

if len(re.findall(
    r"create\s+table\s+public\.exam_history_domain_resources\s*\(",
    sql,
    flags=re.IGNORECASE,
)) != 1:
    fail("Domain-Speichertabelle muss genau einmal erstellt werden.")

storage_version_declaration = re.search(
    r"storage_version\s+bigint\s+not\s+null(.*?)(?:,\s*\n|\n\s*is_deleted)",
    sql,
    flags=re.IGNORECASE | re.DOTALL,
)
if not storage_version_declaration:
    fail("storage_version-Deklaration fehlt.")
if re.search(
    r"\bdefault\b",
    storage_version_declaration.group(1),
    flags=re.IGNORECASE,
):
    fail("storage_version darf keinen Default besitzen.")

for forbidden in (
    "create policy",
    "grant ",
    "create or replace function",
    "auth.uid()",
    "service_role",
    "participant_id",
):
    if forbidden in sql_lower:
        fail(f"Unzulässiger Inhalt in Domain-Speichertabelle: {forbidden}")

if re.search(
    r"\b(insert\s+into|update\s+public\.|delete\s+from)\b",
    sql_clean,
    flags=re.IGNORECASE,
):
    fail("Domain-Speichertabellen-Migration darf keine Daten verändern.")

v2731s_sql_files = sorted(
    path.name for path in MIGRATIONS.glob("*v2731s*.sql")
)
if v2731s_sql_files != [
    "20260723_v2731s_exam_history_domain_resources.sql"
]:
    fail(f"Unerwartete v27.31s-SQL-Dateien: {v2731s_sql_files}")

for frontend_path in (
    ROOT / "index.html",
    ROOT / "app.js",
    ROOT / "patch-v21.js",
    ROOT / "data" / "supabase-client-adapter.js",
):
    frontend_text = frontend_path.read_text(encoding="utf-8").lower()
    for forbidden_reference in (
        "exam_history_domain_resources",
        CONTRACT_PATH.name.lower(),
        STORAGE_TABLE_PATH.name.lower(),
    ):
        if forbidden_reference in frontend_text:
            fail(
                "Domain-Speicher wird direkt im Frontend referenziert: "
                f"{frontend_path.name}: {forbidden_reference}"
            )

v2731n_sql_files = sorted(
    path.name for path in MIGRATIONS.glob("*v2731n*.sql")
)
if v2731n_sql_files:
    fail(f"v27.31n darf keine SQL-Migration besitzen: {v2731n_sql_files}")

print("Domain-Speichervertrag: OK")
print(
    "Speichertabelle: Nutzer, Bereich und Ressource eindeutig gebunden"
)
print(
    "Versionsstand: storage_version beginnt bei 1 und besitzt keinen Default"
)
print(
    "Live-Zustand: Payload, Fingerprint und Bereichsgrößenlimit erzwungen"
)
print(
    "Delete-Zustand: monotone Tombstone-Zeile ohne Payload oder Fingerprint"
)
print(
    "Direkter Zugriff: RLS erzwungen und App-Rollen vollständig gesperrt"
)
print("Speichertabelle implementiert: vorbereitet, nicht live")
print("Mutationshelper implementiert: nein")
print("Produktive Freigabe: nein")
print("Live-Ausführung: nein")
