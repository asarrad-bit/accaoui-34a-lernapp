from pathlib import Path
import json
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
    "Domain-Speichervertrag",
)

if contract.get("version") != "v27.31q":
    fail("Domain-Speichervertrag besitzt nicht v27.31q.")

if contract.get("contractVersion") != 1:
    fail("Domain-Speichervertrag besitzt nicht Schema 1.")

if contract.get("status") != "prepared_not_live":
    fail("Domain-Speichervertrag ist nicht vorbereitet.")

if contract.get("productiveReleaseAllowed") is not False:
    fail("Domain-Speicher darf noch nicht produktiv sein.")

if contract.get("implementationPresent") is not False:
    fail("Domain-Speicher darf noch nicht umgesetzt sein.")

storage = contract.get("storageModel", {})

expected_identity = [
    "auth_user_id",
    "operation_scope",
    "resource_identity",
]

if storage.get("rowIdentityFields") != expected_identity:
    fail("Domain-Speicheridentität ist nicht kanonisch.")

for field in (
    "oneCurrentRowPerIdentity",
    "uniqueIdentityRequired",
    "softDeleteTombstoneRequired",
    "monotonicStorageVersionRequired",
):
    if storage.get(field) is not True:
        fail(f"Domain-Speicherregel fehlt: {field}")

for field in (
    "physicalDeleteByMutationRpcAllowed",
    "versionResetAfterDeleteAllowed",
):
    if storage.get(field) is not False:
        fail(f"Unsichere Domain-Speicherregel: {field}")

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

expected_version = contract.get(
    "expectedVersionInput",
    {},
)

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

if write_rules.get(
    "successfulWriteIncrementsVersionBy"
) != 1:
    fail("Write erhöht storage_version nicht exakt um 1.")

if write_rules.get("samePayloadStillIncrementsVersion") is not False:
    fail("Identischer Payload darf keine unnötige Version erzeugen.")

if write_rules.get("silentLastWriteWinsAllowed") is not False:
    fail("Stilles Last-Write-Wins ist erlaubt.")

if write_rules.get("upsertWithoutVersionGuardAllowed") is not False:
    fail("Upsert ohne Versionsschutz ist erlaubt.")

delete_rules = contract.get("deleteSemantics", {})

for field in (
    "payloadMustBeNull",
    "existingLiveRowRequiresExactVersion",
    "successfulDeleteCreatesTombstone",
    "tombstonePayloadMustBeNull",
    "tombstoneFingerprintMustBeNull",
):
    if delete_rules.get(field) is not True:
        fail(f"Delete-Regel fehlt: {field}")

if delete_rules.get(
    "successfulDeleteIncrementsVersionBy"
) != 1:
    fail("Delete erhöht storage_version nicht exakt um 1.")

if delete_rules.get(
    "alreadyDeletedDoesNotIncrementVersion"
) is not True:
    fail("Bereits gelöschte Ressource erhöht die Version.")

if delete_rules.get("physicalDeleteAllowed") is not False:
    fail("Physisches Löschen ist im Mutationsweg erlaubt.")

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

identity_binding = contract.get(
    "identityBinding",
    {},
)

if identity_binding != {
    "expectedStorageVersionMustAffectRequestIdentity": True,
    "currentIssuanceHelperBindsExpectedVersion": True,
    "currentReservationHelperBindsExpectedVersion": False,
    "outerRpcMayBeImplementedBeforeBinding": False,
}:
    fail("Versionsstand-Identitätsbindung ist ungültig.")

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

expected_failures = [
    "domain_storage_expected_version_invalid",
    "domain_storage_version_conflict",
    "domain_storage_resource_identity_invalid",
    "domain_storage_scope_invalid",
    "domain_storage_payload_invalid",
    "domain_storage_state_invalid",
]

if contract.get("stableFailures") != expected_failures:
    fail("Stabile Domain-Speicherfehler sind ungültig.")

expected_unresolved = {
    "expectedVersionIdentityBinding": True,
    "storageTableImplementation": True,
    "storageMutationHelperImplementation": True,
    "outerDomainMutationRpcImplementation": True,
    "liveDatabaseTests": True,
    "concurrencyTests": True,
    "authorizationTests": True,
}

if contract.get(
    "unresolvedRequirements"
) != expected_unresolved:
    fail("Offene Domain-Speicheranforderungen sind ungültig.")

outer = read_json(
    OUTER_CONTRACT_PATH,
    "Äußerer Fachmutations-RPC-Vertrag",
)

if outer.get("version") != "v27.31n":
    fail("Äußerer RPC-Vertrag besitzt nicht v27.31n.")

outer_parameters = outer.get(
    "publicInterface",
    {},
).get("allowedParameters")

expected_outer_parameters = [
    {
        "name": "p_client_request_key",
        "type": "text",
    },
    {
        "name": "p_operation_scope",
        "type": "text",
    },
    {
        "name": "p_operation",
        "type": "text",
    },
    {
        "name": "p_resource_identity",
        "type": "text",
    },
    {
        "name": "p_expected_storage_version",
        "type": "bigint",
    },
    {
        "name": "p_domain_payload",
        "type": "jsonb",
        "default": None,
    },
]

if outer_parameters != expected_outer_parameters:
    fail("Äußerer RPC besitzt keinen Versionsschutzparameter.")

if outer.get(
    "unresolvedRequirements",
    {},
).get(
    "expectedStorageVersionIdentityBinding"
) is not True:
    fail("Versionsbindung ist im äußeren Vertrag nicht offen.")

payload = read_json(
    PAYLOAD_CONTRACT_PATH,
    "Fach-Payload-Vertrag",
)

if payload.get("version") != "v27.31m":
    fail("Fach-Payload-Vertrag besitzt nicht v27.31m.")

if not VALIDATION_RPC_PATH.is_file():
    fail("Fach-Payload-Validierungs-RPC fehlt.")

v2731n_sql_files = sorted(
    path.name
    for path in MIGRATIONS.glob("*v2731n*.sql")
)

if v2731n_sql_files:
    fail(
        "v27.31n darf keine SQL-Migration erzeugen: "
        f"{v2731n_sql_files}"
    )

print("Domain-Speichervertrag: OK")
print(
    "Nutzerbindung: ausschließlich auth.uid() und "
    "eindeutige Ressourcenidentität"
)
print(
    "Versionsschutz: Create mit 0, Änderung und Delete "
    "nur gegen exakten aktuellen Stand"
)
print(
    "Konkurrenzschutz: Row Lock, Versionsvergleich und "
    "kein stilles Last-Write-Wins"
)
print(
    "Delete: monotone Tombstone-Version statt "
    "physischem Löschen"
)
print(
    "ABA-Schutz: Speicher-Version wird nach Delete "
    "nicht wiederverwendet"
)
print(
    "Operationsidentität: Ausstellungshelper bindet Version; "
    "Reservierungshelper bleibt offen"
)
print("Speichertabelle implementiert: nein")
print("Produktive Freigabe: nein")
print("Live-Ausführung: nein")
