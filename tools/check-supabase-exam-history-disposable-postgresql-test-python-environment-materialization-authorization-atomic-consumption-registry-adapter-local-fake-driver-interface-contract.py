from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / (
    "docs/contracts/exam-history-disposable-postgresql-test-python-"
    "environment-materialization-authorization-atomic-consumption-"
    "registry-adapter-local-fake-driver-interface-contract.json"
)
SOURCE_CONTRACT_PATH = ROOT / (
    "docs/contracts/exam-history-disposable-postgresql-test-python-"
    "environment-materialization-authorization-atomic-consumption-"
    "registry-adapter-implementation-execution-authorization-"
    "readiness-acceptance-guard-contract.json"
)
DOCUMENT_PATH = ROOT / (
    "docs/SUPABASE_EXAM_RESULT_HISTORY_DISPOSABLE_POSTGRESQL_TEST_"
    "PYTHON_ENVIRONMENT_MATERIALIZATION_AUTHORIZATION_ATOMIC_"
    "CONSUMPTION_REGISTRY_ADAPTER_LOCAL_FAKE_DRIVER_INTERFACE_"
    "CONTRACT.md"
)
MASTERLIST_PATH = ROOT / "docs/PROJECT_MASTERLIST.md"
DATABASE_PLAN_PATH = ROOT / "docs/SUPABASE_EXAM_QUESTION_DATABASE_PLAN.md"
PREFLIGHT_PATH = ROOT / "tools/preflight.py"
ADAPTER_MODULE_PATH = ROOT / (
    "tools/accaoui_disposable_test_python_environment_materialization_"
    "authorization_atomic_consumption_registry_adapter.py"
)
FAKE_DRIVER_MODULE_PATH = ROOT / (
    "tools/accaoui_disposable_test_python_environment_materialization_"
    "authorization_atomic_consumption_registry_local_fake_driver.py"
)
FAKE_DRIVER_DOCUMENT_PATH = ROOT / (
    "docs/SUPABASE_EXAM_RESULT_HISTORY_DISPOSABLE_POSTGRESQL_TEST_"
    "PYTHON_ENVIRONMENT_MATERIALIZATION_AUTHORIZATION_ATOMIC_"
    "CONSUMPTION_REGISTRY_ADAPTER_LOCAL_FAKE_DRIVER.md"
)
FAKE_DRIVER_CHECKER_PATH = ROOT / (
    "tools/check-supabase-exam-history-disposable-postgresql-test-"
    "python-environment-materialization-authorization-atomic-"
    "consumption-registry-adapter-local-fake-driver.py"
)

EXPECTED_CONTRACT_FINGERPRINT = (
    "e41efc9592cefffb2c9ffc8bc4a7611a6933cbc57f765f55812d703d08fd2b70"
)
EXPECTED_SOURCE_FINGERPRINT = (
    "6168a5e986f1dd656db4769cadc8d13d62551e0daaacf8e43546d3755d748096"
)
EXPECTED_INPUT_FIELDS = [
    "operationId",
    "requestId",
    "authorizationNonce",
    "planFingerprint",
    "actorId",
    "purpose",
    "expectedState",
    "desiredState",
    "consumptionRecord",
    "evidenceTemplate",
]
EXPECTED_RESULT_KINDS = [
    "committed",
    "already_consumed",
    "parallel_conflict",
    "binding_conflict",
    "expired",
    "adapter_unavailable",
    "atomicity_unavailable",
    "commit_ambiguous",
    "operation_failed",
]
EXPECTED_RESULT_DEFINITIONS = {
    "committed": (
        "authorization_consumed_execution_locked",
        "authorization_consumption_committed",
        "confirmed_consumed",
        True,
        False,
    ),
    "already_consumed": (
        "authorization_consumption_blocked_execution_locked",
        "authorization_consumption_already_consumed",
        "confirmed_already_consumed",
        False,
        False,
    ),
    "parallel_conflict": (
        "authorization_consumption_blocked_execution_locked",
        "authorization_consumption_parallel_conflict",
        "not_consumed_by_operation",
        False,
        False,
    ),
    "binding_conflict": (
        "authorization_consumption_blocked_execution_locked",
        "authorization_consumption_binding_conflict",
        "not_consumed_by_operation",
        False,
        False,
    ),
    "expired": (
        "authorization_consumption_blocked_execution_locked",
        "authorization_consumption_expired",
        "not_consumed_by_operation",
        False,
        False,
    ),
    "adapter_unavailable": (
        "authorization_consumption_blocked_execution_locked",
        "authorization_consumption_adapter_unavailable",
        "not_consumed_by_operation",
        False,
        False,
    ),
    "atomicity_unavailable": (
        "authorization_consumption_blocked_execution_locked",
        "authorization_consumption_atomicity_unavailable",
        "not_consumed_by_operation",
        False,
        False,
    ),
    "commit_ambiguous": (
        "authorization_consumption_reconciliation_required_execution_locked",
        "authorization_consumption_commit_ambiguous",
        "unknown",
        False,
        True,
    ),
    "operation_failed": (
        "authorization_consumption_blocked_execution_locked",
        "authorization_consumption_operation_failed",
        "not_consumed_by_operation",
        False,
        False,
    ),
}
EXPECTED_TIMEOUTS = {
    "operation": ("operationTimeoutMilliseconds", 15000),
    "connect": ("connectTimeoutMilliseconds", 3000),
    "statement": ("statementTimeoutMilliseconds", 5000),
    "lock": ("lockTimeoutMilliseconds", 2000),
}
EXPECTED_RECONCILIATION_KINDS = [
    "confirmed",
    "not_found",
    "ambiguous",
]
EXPECTED_TOP_LEVEL_KEYS = {
    "version",
    "contractVersion",
    "status",
    "productiveReleaseAllowed",
    "sourceBoundary",
    "auditClosureBoundary",
    "pythonInterfaceBoundary",
    "inputBoundary",
    "consumptionRecordBoundary",
    "evidenceBoundary",
    "resultBoundary",
    "timeoutBoundary",
    "fakeDriverBoundary",
    "reconciliationBoundary",
    "implementationBoundary",
    "securityBoundary",
    "futureBoundary",
}


def fail(message: str) -> None:
    raise SystemExit(f"FEHLER: {message}")


def reject_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            fail(f"Doppelter JSON-Schlüssel: {key}")
        result[key] = value
    return result


def load_json(path: Path) -> dict[str, object]:
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        fail(f"UTF-8-BOM nicht erlaubt: {path}")
    if b"\r" in raw:
        fail(f"Nur LF-Zeilenenden erlaubt: {path}")
    if not raw.endswith(b"\n"):
        fail(f"Abschließender Zeilenumbruch fehlt: {path}")
    try:
        value = json.loads(
            raw.decode("utf-8"),
            object_pairs_hook=reject_duplicate_keys,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        fail(f"Ungültiges JSON in {path}: {exc}")
    if type(value) is not dict:
        fail(f"JSON-Wurzel muss ein Objekt sein: {path}")
    return value


def canonical_fingerprint(value: object) -> str:
    canonical = json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def require_exact_keys(
    value: object,
    keys: set[str],
    label: str,
) -> dict[str, object]:
    require(type(value) is dict, f"{label} muss ein Objekt sein")
    data = value
    require(set(data) == keys, f"{label} besitzt keine exakte Struktur")
    return data


def require_all_false(value: object, label: str) -> None:
    require(type(value) is dict, f"{label} muss ein Objekt sein")
    for key, item in value.items():
        require(item is False, f"{label}.{key} muss false sein")


def value_at(root: object, path: tuple[object, ...]) -> object:
    value = root
    for part in path:
        value = value[part]
    return value


def parent_at(
    root: object,
    path: tuple[object, ...],
) -> tuple[object, object]:
    return value_at(root, path[:-1]), path[-1]


def walk(
    value: object,
    path: tuple[object, ...] = (),
):
    if type(value) is dict:
        yield "mapping", path, value
        for key, item in value.items():
            yield from walk(item, path + (key,))
    elif type(value) is list:
        yield "list", path, value
        for index, item in enumerate(value):
            yield from walk(item, path + (index,))
    else:
        yield "scalar", path, value


def changed_scalar(value: object) -> object:
    if type(value) is bool:
        return not value
    if type(value) is int:
        return value + 1
    if type(value) is str:
        return f"{value}_manipulated"
    if value is None:
        return "manipulated"
    fail(f"Nicht unterstützter Manipulationstyp: {type(value).__name__}")


def candidate_is_exact(value: object) -> bool:
    return (
        type(value) is dict
        and canonical_fingerprint(value) == EXPECTED_CONTRACT_FINGERPRINT
    )


def run_manipulation_matrix(contract: dict[str, object]) -> tuple[int, int, int]:
    missing_checks = 0
    additional_checks = 0
    changed_checks = 0

    snapshot = list(walk(contract))
    for kind, path, value in snapshot:
        if kind == "mapping":
            for key in list(value):
                candidate = copy.deepcopy(contract)
                target = value_at(candidate, path)
                del target[key]
                require(
                    not candidate_is_exact(candidate),
                    f"Fehlendes Feld wurde akzeptiert: {path + (key,)}",
                )
                missing_checks += 1

            candidate = copy.deepcopy(contract)
            target = value_at(candidate, path)
            target["unexpectedField"] = "forbidden"
            require(
                not candidate_is_exact(candidate),
                f"Zusätzliches Feld wurde akzeptiert: {path}",
            )
            additional_checks += 1
        elif kind == "list":
            candidate = copy.deepcopy(contract)
            target = value_at(candidate, path)
            target.append("unexpected_list_item")
            require(
                not candidate_is_exact(candidate),
                f"Veränderte Liste wurde akzeptiert: {path}",
            )
            changed_checks += 1
        else:
            candidate = copy.deepcopy(contract)
            parent, key = parent_at(candidate, path)
            parent[key] = changed_scalar(value)
            require(
                not candidate_is_exact(candidate),
                f"Veränderter Wert wurde akzeptiert: {path}",
            )
            changed_checks += 1

    return missing_checks, additional_checks, changed_checks


contract = load_json(CONTRACT_PATH)
source_contract = load_json(SOURCE_CONTRACT_PATH)

require(
    canonical_fingerprint(contract) == EXPECTED_CONTRACT_FINGERPRINT,
    "Kanonischer v27.34a-Vertragsfingerprint stimmt nicht",
)
require(
    canonical_fingerprint(source_contract) == EXPECTED_SOURCE_FINGERPRINT,
    "Kanonischer v27.33y-Quellfingerprint stimmt nicht",
)
require(
    set(contract) == EXPECTED_TOP_LEVEL_KEYS,
    "Top-Level-Vertragsstruktur ist nicht exakt",
)
require(contract["version"] == "v27.34a", "Version ist nicht v27.34a")
require(contract["contractVersion"] == 1, "contractVersion muss 1 sein")
require(
    contract["status"]
    == (
        "planned_local_fake_atomic_consumption_registry_driver_interface_"
        "fully_locked_not_implemented"
    ),
    "Vertragsstatus ist ungültig",
)
require(
    contract["productiveReleaseAllowed"] is False,
    "Produktive Freigabe muss false sein",
)

source = require_exact_keys(
    contract["sourceBoundary"],
    {
        "requiredSourceVersion",
        "requiredSourceContractStatus",
        "requiredAcceptedStatus",
        "requiredAcceptedReason",
        "requiredAccepted",
        "requiredSourceContractFingerprint",
        "canonicalFingerprintEncoding",
        "requiredAuthorizationGrantCreated",
        "requiredAuthorizationTokenGenerated",
        "requiredAuthorizationMayBeConsumed",
        "requiredExecutionGrant",
        "allSourceSecurityFlagsMustBeFalse",
    },
    "sourceBoundary",
)
require(source["requiredSourceVersion"] == "v27.33y", "Quellversion ungültig")
require(
    source["requiredSourceContractFingerprint"]
    == EXPECTED_SOURCE_FINGERPRINT,
    "Quellfingerprint-Bindung ungültig",
)
for key in (
    "requiredAuthorizationGrantCreated",
    "requiredAuthorizationTokenGenerated",
    "requiredAuthorizationMayBeConsumed",
    "requiredExecutionGrant",
):
    require(source[key] is False, f"sourceBoundary.{key} muss false sein")

audit = contract["auditClosureBoundary"]
require(audit["contractOnlyResolution"] is True, "Nur Vertragsauflösung erlaubt")
require(audit["interfaceFullySpecified"] is True, "Schnittstelle nicht vollständig")
for key in (
    "fakeDriverImplemented",
    "adapterImplemented",
    "implementationAuthorized",
    "executionGrant",
):
    require(audit[key] is False, f"auditClosureBoundary.{key} muss false sein")

python_boundary = contract["pythonInterfaceBoundary"]
require(
    python_boundary["adapterFactory"]["exactSignature"]
    == (
        "def build_atomic_consumption_registry_adapter(*, driver: "
        "LocalFakeAtomicConsumptionRegistryDriver) -> "
        "AtomicConsumptionRegistryAdapter"
    ),
    "Adapter-Factory-Signatur ungültig",
)
require(
    python_boundary["fakeDriverFactory"]["exactSignature"]
    == (
        "def build_local_fake_atomic_consumption_registry_driver(*, "
        "initial_state: tuple[FakeRegistryEntry, ...], "
        "simulation_directives: tuple[FakeSimulationDirective, ...], "
        "clock: InjectedUtcClock) -> "
        "LocalFakeAtomicConsumptionRegistryDriver"
    ),
    "Fake-Treiber-Factory-Signatur ungültig",
)
require(
    python_boundary["adapterAtomicOperation"]["name"]
    == "consume_materialization_authorization_atomically",
    "Atomare Adapteroperation ungültig",
)
require(
    python_boundary["adapterReconciliationOperation"]["name"]
    == "reconcile_materialization_authorization_consumption",
    "Adapter-Reconciliation ungültig",
)
require(
    python_boundary["driverAtomicOperation"]["name"]
    == "compare_and_set_with_consumption_record",
    "Atomare Treiberoperation ungültig",
)
require(
    python_boundary["driverReconciliationOperation"]["name"]
    == "read_consumption_by_operation_id",
    "Treiber-Reconciliation ungültig",
)
for key in (
    "dynamicSignaturesAllowed",
    "variadicArgumentsAllowed",
    "optionalParametersAllowed",
    "implicitDependencyResolutionAllowed",
):
    require(
        python_boundary[key] is False,
        f"pythonInterfaceBoundary.{key} muss false sein",
    )

input_boundary = contract["inputBoundary"]
require(
    input_boundary["exactFieldOrder"] == EXPECTED_INPUT_FIELDS,
    "Zehn Eingabefelder sind nicht exakt",
)
require(
    [item["name"] for item in input_boundary["fieldSchemas"]]
    == EXPECTED_INPUT_FIELDS,
    "Eingabefeldschemas sind nicht vollständig geordnet",
)
for field in input_boundary["fieldSchemas"]:
    require(
        set(field)
        == {
            "name",
            "pythonType",
            "required",
            "allowedValueRule",
            "emptyAllowed",
            "immutable",
        },
        f"Feldschema {field.get('name')} ist nicht exakt",
    )
    require(field["required"] is True, f"{field['name']} muss Pflichtfeld sein")
    require(
        field["emptyAllowed"] is False,
        f"{field['name']} darf nicht leer sein",
    )
    require(
        field["immutable"] is True,
        f"{field['name']} muss unveränderlich sein",
    )
for key in (
    "unknownFieldsAllowed",
    "missingFieldsAllowed",
    "inputMutationAllowed",
    "extraNestedFieldsAllowed",
):
    require(input_boundary[key] is False, f"inputBoundary.{key} muss false sein")

record = contract["consumptionRecordBoundary"]
require(
    record["draftExactFields"]
    == [
        "recordVersion",
        "operationId",
        "requestId",
        "authorizationNonce",
        "planFingerprint",
        "actorId",
        "purpose",
        "expectedState",
        "desiredState",
        "confirmed",
    ],
    "Consumption-Record-Draft-Felder sind nicht exakt",
)
require(
    record["confirmedExactFields"]
    == record["draftExactFields"] + ["consumedAtUtc"],
    "Bestätigter Consumption-Record ist nicht exakt",
)
require(
    set(record["draftFieldTypes"]) == set(record["draftExactFields"]),
    "Draft-Typen sind unvollständig",
)
require(
    set(record["confirmedFieldTypes"])
    == set(record["confirmedExactFields"]),
    "Bestätigte Record-Typen sind unvollständig",
)
for key in (
    "allIdentityBindingsMustEqualRequest",
    "compareAndSetAndConfirmedRecordSingleAtomicSectionRequired",
    "singleUseRequired",
):
    require(record[key] is True, f"consumptionRecordBoundary.{key} muss true sein")
for key in (
    "replayAllowed",
    "confirmedBeforeCommitAllowed",
    "recordWithoutCommittedTransitionAllowed",
    "committedTransitionWithoutRecordAllowed",
    "resetConsumedToUnusedAllowed",
    "unknownDraftFieldsAllowed",
    "unknownConfirmedFieldsAllowed",
):
    require(record[key] is False, f"consumptionRecordBoundary.{key} muss false sein")
require(record["maximumParallelWinners"] == 1, "Es darf nur einen Gewinner geben")

evidence = contract["evidenceBoundary"]
require(
    set(evidence["templateFieldTypes"]) == set(evidence["templateExactFields"]),
    "Evidence-Template-Typen sind unvollständig",
)
require(
    set(evidence["evidenceFieldTypes"]) == set(evidence["evidenceExactFields"]),
    "Evidence-Typen sind unvollständig",
)
require(
    evidence["derivedOnlyFromConfirmedRecord"] is True,
    "Evidence muss aus bestätigtem Record stammen",
)
for key in (
    "evidenceWithoutConfirmedRecordAllowed",
    "unconfirmedEvidenceAllowed",
    "rawAuthorizationNonceAllowed",
    "rawErrorAllowed",
    "credentialFieldsAllowed",
    "participantDataFieldsAllowed",
    "unknownTemplateFieldsAllowed",
    "unknownEvidenceFieldsAllowed",
):
    require(evidence[key] is False, f"evidenceBoundary.{key} muss false sein")

result = contract["resultBoundary"]
require(
    result["exactResultKinds"] == EXPECTED_RESULT_KINDS,
    "Neun Ergebnisarten sind nicht exakt",
)
require(
    len(result["resultSchemas"]) == 9,
    "Es müssen exakt neun Ergebnis-Payloads existieren",
)
conditional_fields = set(result["onlyConditionalPayloadFields"])
require(
    conditional_fields == {"consumptionRecord", "evidence"},
    "Bedingte Ergebnisfelder sind ungültig",
)
for schema in result["resultSchemas"]:
    require(
        set(schema)
        == {
            "resultKind",
            "status",
            "reason",
            "requiredPayloadFields",
            "forbiddenPayloadFields",
            "consumptionStatus",
            "evidenceRule",
            "terminal",
            "reconciliationRequired",
            "retryAllowed",
            "executionGrant",
        },
        f"Ergebnisschema {schema.get('resultKind')} ist nicht exakt",
    )
    kind = schema["resultKind"]
    require(kind in EXPECTED_RESULT_DEFINITIONS, f"Unbekannte Ergebnisart: {kind}")
    status, reason, consumption, payload_required, reconciliation = (
        EXPECTED_RESULT_DEFINITIONS[kind]
    )
    require(schema["status"] == status, f"Status für {kind} ist ungültig")
    require(schema["reason"] == reason, f"Grund für {kind} ist ungültig")
    require(
        schema["consumptionStatus"] == consumption,
        f"Verbrauchsstatus für {kind} ist ungültig",
    )
    require(schema["terminal"] is True, f"{kind} muss terminal sein")
    require(
        schema["reconciliationRequired"] is reconciliation,
        f"Reconciliation-Regel für {kind} ist ungültig",
    )
    require(schema["retryAllowed"] is False, f"Retry für {kind} muss gesperrt sein")
    require(
        schema["executionGrant"] is False,
        f"executionGrant für {kind} muss false sein",
    )
    required_payload = set(schema["requiredPayloadFields"])
    forbidden_payload = set(schema["forbiddenPayloadFields"])
    require(
        required_payload.isdisjoint(forbidden_payload),
        f"Payload-Felder für {kind} widersprechen sich",
    )
    require(
        required_payload | forbidden_payload == conditional_fields,
        f"Payload-Felder für {kind} sind unvollständig",
    )
    require(
        (required_payload == conditional_fields) is payload_required,
        f"Payload-Pflicht für {kind} ist ungültig",
    )
for key in (
    "unknownResultKindsAllowed",
    "unknownResultFieldsAllowed",
    "rawErrorFieldsAllowed",
    "rawRegistryValueFieldsAllowed",
    "automaticRetryAllowed",
    "executionGrant",
):
    require(result[key] is False, f"resultBoundary.{key} muss false sein")

timeouts = contract["timeoutBoundary"]
require(
    {
        "operation": timeouts["operationTimeoutMilliseconds"],
        "connect": timeouts["connectTimeoutMilliseconds"],
        "statement": timeouts["statementTimeoutMilliseconds"],
        "lock": timeouts["lockTimeoutMilliseconds"],
    }
    == {
        "operation": 15000,
        "connect": 3000,
        "statement": 5000,
        "lock": 2000,
    },
    "Zeitlimitwerte sind nicht exakt",
)
require(
    len(timeouts["phaseMappings"]) == 4,
    "Es müssen exakt vier Timeout-Phasen existieren",
)
for mapping in timeouts["phaseMappings"]:
    field, milliseconds = EXPECTED_TIMEOUTS[mapping["phase"]]
    require(mapping["timeoutField"] == field, "Timeout-Feldzuordnung ungültig")
    require(
        mapping["timeoutMilliseconds"] == milliseconds,
        "Timeout-Phasenwert ungültig",
    )
for key in (
    "newTimeoutValuesAllowed",
    "timeoutExpansionAllowed",
    "fakeDriverMaySleep",
    "fakeDriverMayReadWallClockForTimeouts",
    "timeoutAutomaticRetryAllowed",
):
    require(timeouts[key] is False, f"timeoutBoundary.{key} muss false sein")

fake = contract["fakeDriverBoundary"]
for key in (
    "fullyLocalRequired",
    "deterministicRequired",
    "inMemoryOnlyRequired",
    "inMemoryStateOwnedPerDriverInstance",
    "singleAtomicSectionRequired",
    "ambiguousResultSimulationRequired",
    "simulationDirectivesInjectedAtConstruction",
):
    require(fake[key] is True, f"fakeDriverBoundary.{key} muss true sein")
for key in (
    "globalMutableStateAllowed",
    "readThenWriteSplitAllowed",
    "replayAllowed",
    "confirmedConsumptionMayBeOverwritten",
    "resetConsumedToUnusedAllowed",
    "simulationMayGrantAuthorization",
    "simulationMayCreateToken",
    "simulationMaySetExecutionGrant",
    "realDatabaseAllowed",
    "postgresqlConnectionAllowed",
    "supabaseAllowed",
    "networkAllowed",
    "filesystemAllowed",
    "processAllowed",
    "environmentVariableReadAllowed",
    "realKeysAllowed",
    "realParticipantDataAllowed",
    "nonInjectedClockReadAllowed",
):
    require(fake[key] is False, f"fakeDriverBoundary.{key} muss false sein")
require(fake["maximumParallelWinners"] == 1, "Fake-Treiber: nur ein Gewinner")

reconciliation = contract["reconciliationBoundary"]
require(
    reconciliation["lookupField"] == "operationId",
    "Reconciliation darf nur operationId verwenden",
)
require(
    reconciliation["exactReconciliationKinds"]
    == EXPECTED_RECONCILIATION_KINDS,
    "Reconciliation-Zustände sind nicht exakt",
)
require(
    len(reconciliation["resultSchemas"]) == 3,
    "Es müssen exakt drei Reconciliation-Payloads existieren",
)
for key in (
    "additionalLookupFieldsAllowed",
    "writeAllowed",
    "consumptionOperationAllowed",
    "automaticRetryAllowed",
    "notFoundMayAssumeUnused",
    "ambiguousMayAssumeCommitted",
    "unknownKindsAllowed",
    "unknownFieldsAllowed",
):
    require(
        reconciliation[key] is False,
        f"reconciliationBoundary.{key} muss false sein",
    )
for schema in reconciliation["resultSchemas"]:
    require(schema["writePerformed"] is False, "Reconciliation darf nicht schreiben")
    require(schema["retryPerformed"] is False, "Reconciliation darf nicht retryen")
    require(schema["executionGrant"] is False, "Reconciliation-Grant muss false sein")

implementation = contract["implementationBoundary"]
require(
    implementation["localFakeDriverInterfaceContractPrepared"] is True,
    "Schnittstellenvertrag muss als vorbereitet markiert sein",
)
for key, value in implementation.items():
    if key != "localFakeDriverInterfaceContractPrepared":
        require(value is False, f"implementationBoundary.{key} muss false sein")

require_all_false(contract["securityBoundary"], "securityBoundary")

future = contract["futureBoundary"]
require(future["nextVersion"] == "v27.34b", "Nächste Version muss v27.34b sein")
for key, value in future.items():
    if key not in {"nextVersion", "nextStep"}:
        require(value is False, f"futureBoundary.{key} muss false sein")

require(not ADAPTER_MODULE_PATH.exists(), "Adaptermodul wurde vorzeitig erstellt")
if FAKE_DRIVER_MODULE_PATH.exists():
    require(
        FAKE_DRIVER_DOCUMENT_PATH.is_file(),
        "v27.34b-Fake-Treiber existiert ohne Dokumentation",
    )
    require(
        FAKE_DRIVER_CHECKER_PATH.is_file(),
        "v27.34b-Fake-Treiber existiert ohne Checker",
    )
    future_document_text = FAKE_DRIVER_DOCUMENT_PATH.read_text(
        encoding="utf-8"
    )
    for token in (
        "Stand: v27.34b",
        "v27.34a-Schnittstellenvertrag bleibt unverändert",
        "kein echter Registry-Adapter",
    ):
        require(
            token in future_document_text,
            f"v27.34b-Folgeschritt ist nicht sicher dokumentiert: {token}",
        )
else:
    require(
        not FAKE_DRIVER_DOCUMENT_PATH.exists(),
        "v27.34b-Dokument existiert ohne Fake-Treibermodul",
    )
    require(
        not FAKE_DRIVER_CHECKER_PATH.exists(),
        "v27.34b-Checker existiert ohne Fake-Treibermodul",
    )

document_text = DOCUMENT_PATH.read_text(encoding="utf-8")
master_text = MASTERLIST_PATH.read_text(encoding="utf-8")
database_plan_text = DATABASE_PLAN_PATH.read_text(encoding="utf-8")
preflight_text = PREFLIGHT_PATH.read_text(encoding="utf-8")

for token in (
    "Stand: v27.34a",
    "NO-GO",
    "Schnittstelle vollständig festgelegt",
    "v27.34b",
    "noch nicht autorisiert",
):
    require(token in document_text, f"Vertragsdokument fehlt: {token}")
require("| v27.34a |" in master_text, "Masterliste enthält v27.34a nicht")
require(
    "Local-Fake-Registry-Treiber-Schnittstellenvertrag v27.34a"
    in database_plan_text,
    "Datenbankplan enthält v27.34a nicht",
)
if FAKE_DRIVER_MODULE_PATH.exists():
    require(
        (
            "v27.34b ist als erstes lokales Fake-Registry-Treibermodul "
            "umgesetzt."
        )
        in database_plan_text,
        "Datenbankplan dokumentiert v27.34b nicht als umgesetzt",
    )
else:
    require(
        "Nächster Schritt ist ausschließlich `v27.34b`"
        in database_plan_text,
        "Datenbankplan bindet den nächsten Schritt nicht an v27.34b",
    )

actual_checker_relative = Path(__file__).resolve().relative_to(ROOT).as_posix()
require(
    actual_checker_relative in preflight_text,
    "Neuer Checker ist nicht im Preflight referenziert",
)
require(
    CONTRACT_PATH.relative_to(ROOT).as_posix() in preflight_text,
    "Neuer Vertrag ist nicht in der Preflight-Dateiliste",
)
require(
    DOCUMENT_PATH.relative_to(ROOT).as_posix() in preflight_text,
    "Neues Vertragsdokument ist nicht in der Preflight-Dateiliste",
)

missing_count, additional_count, changed_count = run_manipulation_matrix(
    contract
)
require(candidate_is_exact(contract), "Originalvertrag wurde nicht akzeptiert")

print("Local-Fake-Registry-Treiber-Schnittstellenvertrag v27.34a: OK")
print("Quellbindung: v27.33y mit kanonischem SHA-256")
print("Python-Signaturen und Rückgabetypen: vollständig")
print("Eingabefelder: exakt 10")
print("Ergebnis-Payloads: exakt 9")
print("Timeout-Phasen: exakt 4")
print("Reconciliation-Zustände: exakt 3, nur lesend")
print(
    "Manipulationsmatrix: "
    f"{missing_count} fehlende, "
    f"{additional_count} zusätzliche, "
    f"{changed_count} veränderte Strukturen blockiert"
)
print(
    "Fake-Treiber implementiert: ja, ausschließlich lokal in v27.34b"
    if FAKE_DRIVER_MODULE_PATH.exists()
    else "Fake-Treiber implementiert: nein"
)
print("Adapter implementiert: nein")
print("Datenbank-, Netzwerk-, SQL-, Supabase- und UI-Zugriff: keiner")
print("Produktive Freigabe: nein")
