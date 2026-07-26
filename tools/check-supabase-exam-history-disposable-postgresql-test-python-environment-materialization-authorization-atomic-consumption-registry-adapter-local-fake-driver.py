from __future__ import annotations

import ast
import base64
import copy
import hashlib
import importlib.util
import inspect
import json
import sys
import threading
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / (
    "docs/contracts/exam-history-disposable-postgresql-test-python-"
    "environment-materialization-authorization-atomic-consumption-"
    "registry-adapter-local-fake-driver-interface-contract.json"
)
MODULE_PATH = ROOT / (
    "tools/accaoui_disposable_test_python_environment_materialization_"
    "authorization_atomic_consumption_registry_local_fake_driver.py"
)
DOCUMENT_PATH = ROOT / (
    "docs/SUPABASE_EXAM_RESULT_HISTORY_DISPOSABLE_POSTGRESQL_TEST_"
    "PYTHON_ENVIRONMENT_MATERIALIZATION_AUTHORIZATION_ATOMIC_"
    "CONSUMPTION_REGISTRY_ADAPTER_LOCAL_FAKE_DRIVER.md"
)
MASTERLIST_PATH = ROOT / "docs/PROJECT_MASTERLIST.md"
DATABASE_PLAN_PATH = ROOT / "docs/SUPABASE_EXAM_QUESTION_DATABASE_PLAN.md"
PREFLIGHT_PATH = ROOT / "tools/preflight.py"
V27_34A_CHECKER_PATH = ROOT / (
    "tools/check-supabase-exam-history-disposable-postgresql-test-"
    "python-environment-materialization-authorization-atomic-"
    "consumption-registry-adapter-local-fake-driver-interface-contract.py"
)
ADAPTER_MODULE_PATH = ROOT / (
    "tools/accaoui_disposable_test_python_environment_materialization_"
    "authorization_atomic_consumption_registry_adapter.py"
)

EXPECTED_CONTRACT_FINGERPRINT = (
    "e41efc9592cefffb2c9ffc8bc4a7611a6933cbc57f765f55812d703d08fd2b70"
)
PURPOSE = "disposable_test_python_environment_materialization"
REQUEST_FIELDS = (
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
)
RECORD_DRAFT_FIELDS = (
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
)
CONFIRMED_RECORD_FIELDS = RECORD_DRAFT_FIELDS + ("consumedAtUtc",)
EVIDENCE_FIELDS = (
    "evidenceVersion",
    "operationId",
    "requestId",
    "authorizationNonceFingerprint",
    "planFingerprint",
    "actorId",
    "purpose",
    "consumedAtUtc",
    "recordFingerprint",
    "singleUse",
    "status",
    "executionGrant",
)
ENTRY_FIELDS = (
    "requestId",
    "authorizationNonce",
    "planFingerprint",
    "actorId",
    "purpose",
    "state",
    "expiresAtUtc",
    "consumptionRecord",
)
DIRECTIVE_FIELDS = (
    "operationId",
    "phase",
    "resultKind",
    "commitVisibleToReconciliation",
)
RESULT_KINDS = (
    "committed",
    "already_consumed",
    "parallel_conflict",
    "binding_conflict",
    "expired",
    "adapter_unavailable",
    "atomicity_unavailable",
    "commit_ambiguous",
    "operation_failed",
)
RECONCILIATION_KINDS = (
    "confirmed",
    "not_found",
    "ambiguous",
)
ALLOWED_IMPORT_ROOTS = {
    "__future__",
    "base64",
    "copy",
    "datetime",
    "hashlib",
    "json",
    "re",
    "threading",
    "typing",
    "unicodedata",
    "uuid",
}
FORBIDDEN_CALL_NAMES = {
    "breakpoint",
    "compile",
    "eval",
    "exec",
    "input",
    "open",
    "__import__",
}
FORBIDDEN_CALL_ATTRIBUTES = {
    "connect",
    "execute",
    "getenv",
    "open",
    "popen",
    "read_bytes",
    "read_text",
    "sleep",
    "system",
    "time",
    "utcnow",
    "write_bytes",
    "write_text",
}


def fail(message: str) -> None:
    raise SystemExit(f"FEHLER: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def reject_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            fail(f"Doppelter JSON-Schlüssel: {key}")
        result[key] = value
    return result


def load_contract() -> dict[str, object]:
    raw = CONTRACT_PATH.read_bytes()
    require(not raw.startswith(b"\xef\xbb\xbf"), "v27.34a-Vertrag hat BOM")
    require(b"\r" not in raw, "v27.34a-Vertrag hat nicht nur LF")
    require(raw.endswith(b"\n"), "v27.34a-Vertrag ohne Schlusszeile")
    try:
        value = json.loads(
            raw.decode("utf-8"),
            object_pairs_hook=reject_duplicate_keys,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        fail(f"Ungültiger v27.34a-Vertrag: {exc}")
    require(type(value) is dict, "v27.34a-Vertragswurzel ist kein Objekt")
    return value


def canonical_fingerprint(value: object) -> str:
    encoded = json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def load_module():
    spec = importlib.util.spec_from_file_location(
        "accaoui_v27_34b_local_fake_driver",
        MODULE_PATH,
    )
    require(spec is not None and spec.loader is not None, "Modul nicht ladbar")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def synthetic_uuid(index: int) -> str:
    return f"{index:08x}-0000-4000-8000-{index:012x}"


def synthetic_nonce(seed: int = 0) -> str:
    raw = bytes((seed + index) % 256 for index in range(32))
    return base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")


def make_request(
    operation_id: str,
    *,
    request_id: str | None = None,
    nonce: str | None = None,
    plan_fingerprint: str | None = None,
    actor_id: str = "synthetic-human-operator",
) -> dict[str, object]:
    request_id = request_id or synthetic_uuid(1001)
    nonce = nonce or synthetic_nonce(1)
    plan_fingerprint = plan_fingerprint or ("a" * 64)
    draft = {
        "recordVersion": 1,
        "operationId": operation_id,
        "requestId": request_id,
        "authorizationNonce": nonce,
        "planFingerprint": plan_fingerprint,
        "actorId": actor_id,
        "purpose": PURPOSE,
        "expectedState": "unused",
        "desiredState": "consumed",
        "confirmed": False,
    }
    template = {
        "evidenceVersion": 1,
        "operationId": operation_id,
        "recordSource": "confirmed_consumption_record_only",
        "confirmedRecordRequired": True,
        "unconfirmedEvidenceAllowed": False,
    }
    return {
        "operationId": operation_id,
        "requestId": request_id,
        "authorizationNonce": nonce,
        "planFingerprint": plan_fingerprint,
        "actorId": actor_id,
        "purpose": PURPOSE,
        "expectedState": "unused",
        "desiredState": "consumed",
        "consumptionRecord": draft,
        "evidenceTemplate": template,
    }


def make_entry(
    request: dict[str, object],
    *,
    expires_at_utc: str = "2035-01-01T00:00:00Z",
    state: str = "unused",
    record: dict[str, object] | None = None,
) -> dict[str, object]:
    return {
        "requestId": request["requestId"],
        "authorizationNonce": request["authorizationNonce"],
        "planFingerprint": request["planFingerprint"],
        "actorId": request["actorId"],
        "purpose": request["purpose"],
        "state": state,
        "expiresAtUtc": expires_at_utc,
        "consumptionRecord": copy.deepcopy(record),
    }


def make_directive(
    operation_id: str,
    result_kind: str,
    *,
    phase: str = "operation",
    visible: bool = False,
) -> dict[str, object]:
    return {
        "operationId": operation_id,
        "phase": phase,
        "resultKind": result_kind,
        "commitVisibleToReconciliation": visible,
    }


class FixedClock:
    def __init__(self, value: datetime) -> None:
        self.value = value
        self.calls = 0

    def now_utc(self) -> datetime:
        self.calls += 1
        return self.value


class BlockingClock:
    def __init__(self, value: datetime) -> None:
        self.value = value
        self.entered = threading.Event()
        self.release = threading.Event()
        self.calls = 0

    def now_utc(self) -> datetime:
        self.calls += 1
        self.entered.set()
        if not self.release.wait(timeout=5):
            raise AssertionError("Paralleltest-Uhr wurde nicht freigegeben")
        return self.value


def fixed_clock() -> FixedClock:
    return FixedClock(datetime(2030, 1, 1, tzinfo=timezone.utc))


def build_driver(
    module,
    request: dict[str, object],
    *,
    clock=None,
    directives: tuple[dict[str, object], ...] = (),
    expires_at_utc: str = "2035-01-01T00:00:00Z",
):
    selected_clock = clock or fixed_clock()
    initial_state = (
        make_entry(request, expires_at_utc=expires_at_utc),
    )
    driver = module.build_local_fake_atomic_consumption_registry_driver(
        initial_state=initial_state,
        simulation_directives=directives,
        clock=selected_clock,
    )
    return driver, selected_clock, initial_state


def result_schema_map(contract: dict[str, object]) -> dict[str, dict[str, object]]:
    return {
        schema["resultKind"]: schema
        for schema in contract["resultBoundary"]["resultSchemas"]
    }


def reconciliation_schema_map(
    contract: dict[str, object],
) -> dict[str, dict[str, object]]:
    return {
        schema["reconciliationKind"]: schema
        for schema in contract["reconciliationBoundary"]["resultSchemas"]
    }


def validate_confirmed_record(
    record: object,
    request: dict[str, object] | None = None,
) -> None:
    require(type(record) is dict, "Bestätigter Record ist kein Objekt")
    require(
        tuple(record) == CONFIRMED_RECORD_FIELDS,
        "Bestätigter Record besitzt nicht die exakten Felder",
    )
    require(record["recordVersion"] == 1, "Recordversion ist ungültig")
    require(record["confirmed"] is True, "Record ist nicht bestätigt")
    require(
        record["expectedState"] == "unused"
        and record["desiredState"] == "consumed",
        "Record-Zustandsübergang ist ungültig",
    )
    require(
        record["consumedAtUtc"].endswith("Z"),
        "Record-Zeit ist nicht UTC-Z",
    )
    if request is not None:
        for field in (
            "operationId",
            "requestId",
            "authorizationNonce",
            "planFingerprint",
            "actorId",
            "purpose",
            "expectedState",
            "desiredState",
        ):
            require(
                record[field] == request[field],
                f"Record-Bindung weicht ab: {field}",
            )


def validate_evidence(
    evidence: object,
    record: dict[str, object],
) -> None:
    require(type(evidence) is dict, "Evidence ist kein Objekt")
    require(
        tuple(evidence) == EVIDENCE_FIELDS,
        "Evidence besitzt nicht die exakten Felder",
    )
    for field in (
        "operationId",
        "requestId",
        "planFingerprint",
        "actorId",
        "purpose",
        "consumedAtUtc",
    ):
        require(
            evidence[field] == record[field],
            f"Evidence-Bindung weicht ab: {field}",
        )
    require(
        evidence["authorizationNonceFingerprint"]
        == hashlib.sha256(
            record["authorizationNonce"].encode("utf-8")
        ).hexdigest(),
        "Evidence-Nonce-Fingerprint ist inkonsistent",
    )
    require(
        evidence["recordFingerprint"] == canonical_fingerprint(record),
        "Evidence-Record-Fingerprint ist inkonsistent",
    )
    require(evidence["singleUse"] is True, "Evidence ist nicht single-use")
    require(
        evidence["status"] == "authorization_consumed_execution_locked",
        "Evidence-Status ist ungültig",
    )
    require(evidence["executionGrant"] is False, "Evidence-Grant ist offen")
    forbidden = {
        "authorizationNonce",
        "authorizationGrant",
        "authorizationToken",
        "rawError",
        "password",
        "participantId",
    }
    require(
        forbidden.isdisjoint(evidence),
        "Evidence enthält ein verbotenes Feld",
    )


def validate_result(
    contract: dict[str, object],
    result: object,
    expected_kind: str,
    operation_id: str,
    request: dict[str, object] | None = None,
) -> None:
    require(type(result) is dict, f"{expected_kind}: Ergebnis ist kein Objekt")
    schema = result_schema_map(contract)[expected_kind]
    common_fields = tuple(contract["resultBoundary"]["commonRequiredFields"])
    payload_fields = tuple(schema["requiredPayloadFields"])
    require(
        tuple(result) == common_fields + payload_fields,
        f"{expected_kind}: Ergebnisfelder sind nicht exakt",
    )
    require(result["resultKind"] == expected_kind, "Ergebnisart weicht ab")
    require(result["operationId"] == operation_id, "Operations-ID weicht ab")
    for field in (
        "status",
        "reason",
        "consumptionStatus",
        "reconciliationRequired",
        "retryAllowed",
        "executionGrant",
    ):
        require(
            result[field] == schema[field],
            f"{expected_kind}: {field} weicht vom Vertrag ab",
        )
    require(result["retryAllowed"] is False, "Automatischer Retry ist offen")
    require(result["executionGrant"] is False, "executionGrant ist offen")
    if expected_kind == "committed":
        validate_confirmed_record(result["consumptionRecord"], request)
        validate_evidence(result["evidence"], result["consumptionRecord"])
    else:
        require(
            "consumptionRecord" not in result and "evidence" not in result,
            f"{expected_kind}: Record oder Evidence ist unzulässig",
        )


def validate_reconciliation(
    contract: dict[str, object],
    result: object,
    expected_kind: str,
    operation_id: str,
) -> None:
    require(type(result) is dict, "Reconciliation-Ergebnis ist kein Objekt")
    schema = reconciliation_schema_map(contract)[expected_kind]
    common_fields = tuple(
        contract["reconciliationBoundary"]["commonRequiredFields"]
    )
    payload_fields = tuple(schema["requiredPayloadFields"])
    require(
        tuple(result) == common_fields + payload_fields,
        f"{expected_kind}: Reconciliation-Felder sind nicht exakt",
    )
    require(
        result["reconciliationKind"] == expected_kind,
        "Reconciliation-Art weicht ab",
    )
    require(result["operationId"] == operation_id, "Reconciliation-ID weicht ab")
    for field in (
        "status",
        "reason",
        "consumptionStatus",
        "writePerformed",
        "retryPerformed",
        "executionGrant",
    ):
        require(
            result[field] == schema[field],
            f"{expected_kind}: Reconciliation-{field} weicht ab",
        )
    require(result["writePerformed"] is False, "Reconciliation hat geschrieben")
    require(result["retryPerformed"] is False, "Reconciliation hat wiederholt")
    require(result["executionGrant"] is False, "Reconciliation-Grant ist offen")
    if expected_kind == "confirmed":
        validate_confirmed_record(result["consumptionRecord"])
        validate_evidence(result["evidence"], result["consumptionRecord"])
    else:
        require(
            "consumptionRecord" not in result and "evidence" not in result,
            f"{expected_kind}: Reconciliation-Payload ist unzulässig",
        )


def snapshot_driver_state(driver) -> object:
    return (
        copy.deepcopy(driver._entries),
        copy.deepcopy(driver._operation_bindings),
        copy.deepcopy(driver._confirmed_records_by_operation_id),
        copy.deepcopy(driver._ambiguous_operation_ids),
        copy.deepcopy(driver._terminal_results_by_operation_id),
        copy.deepcopy(driver._directives_by_operation_id),
    )


def expect_value_error(action, label: str) -> None:
    try:
        action()
    except ValueError:
        return
    except Exception as exc:
        fail(f"{label}: falscher Fehlertyp {type(exc).__name__}: {exc}")
    fail(f"{label}: ungültige Manipulation wurde akzeptiert")


def walk_mappings_and_scalars(
    value: object,
    path: tuple[object, ...] = (),
):
    if type(value) is dict:
        yield "mapping", path, value
        for key, item in value.items():
            yield from walk_mappings_and_scalars(item, path + (key,))
    else:
        yield "scalar", path, value


def value_at(root: object, path: tuple[object, ...]) -> object:
    value = root
    for part in path:
        value = value[part]
    return value


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


def run_request_manipulation_matrix(module) -> tuple[int, int, int]:
    request = make_request(synthetic_uuid(2001))
    missing = 0
    additional = 0
    changed = 0

    def exercise(candidate: dict[str, object]) -> None:
        driver, _, _ = build_driver(module, request)
        driver.compare_and_set_with_consumption_record(candidate)

    for kind, path, value in list(walk_mappings_and_scalars(request)):
        if kind == "mapping":
            for key in tuple(value):
                candidate = copy.deepcopy(request)
                target = value_at(candidate, path)
                del target[key]
                expect_value_error(
                    lambda candidate=candidate: exercise(candidate),
                    f"fehlendes Request-Feld {path + (key,)}",
                )
                missing += 1
            candidate = copy.deepcopy(request)
            target = value_at(candidate, path)
            target["unexpectedField"] = "forbidden"
            expect_value_error(
                lambda candidate=candidate: exercise(candidate),
                f"zusätzliches Request-Feld {path}",
            )
            additional += 1
        else:
            candidate = copy.deepcopy(request)
            parent = value_at(candidate, path[:-1])
            parent[path[-1]] = changed_scalar(value)
            expect_value_error(
                lambda candidate=candidate: exercise(candidate),
                f"verändertes Request-Feld {path}",
            )
            changed += 1

    reordered = {
        key: copy.deepcopy(request[key])
        for key in reversed(REQUEST_FIELDS)
    }
    expect_value_error(
        lambda: exercise(reordered),
        "veränderte Request-Feldreihenfolge",
    )
    changed += 1
    return missing, additional, changed


def run_constructor_manipulation_matrix(module) -> tuple[int, int, int]:
    request = make_request(synthetic_uuid(2101))
    entry = make_entry(request)
    directive = make_directive(
        synthetic_uuid(2102),
        "operation_failed",
    )
    missing = 0
    additional = 0
    changed = 0

    for key in ENTRY_FIELDS:
        candidate = copy.deepcopy(entry)
        del candidate[key]
        expect_value_error(
            lambda candidate=candidate: module.build_local_fake_atomic_consumption_registry_driver(
                initial_state=(candidate,),
                simulation_directives=(),
                clock=fixed_clock(),
            ),
            f"fehlendes Initial-State-Feld {key}",
        )
        missing += 1

    extra_entry = copy.deepcopy(entry)
    extra_entry["unexpectedField"] = "forbidden"
    expect_value_error(
        lambda: module.build_local_fake_atomic_consumption_registry_driver(
            initial_state=(extra_entry,),
            simulation_directives=(),
            clock=fixed_clock(),
        ),
        "zusätzliches Initial-State-Feld",
    )
    additional += 1

    invalid_entry_values = {
        "requestId": "invalid",
        "authorizationNonce": "invalid",
        "planFingerprint": "invalid",
        "actorId": " invalid",
        "purpose": "invalid",
        "state": "invalid",
        "expiresAtUtc": "invalid",
        "consumptionRecord": "invalid",
    }
    for key, invalid in invalid_entry_values.items():
        candidate = copy.deepcopy(entry)
        candidate[key] = invalid
        expect_value_error(
            lambda candidate=candidate: module.build_local_fake_atomic_consumption_registry_driver(
                initial_state=(candidate,),
                simulation_directives=(),
                clock=fixed_clock(),
            ),
            f"verändertes Initial-State-Feld {key}",
        )
        changed += 1

    for key in DIRECTIVE_FIELDS:
        candidate = copy.deepcopy(directive)
        del candidate[key]
        expect_value_error(
            lambda candidate=candidate: module.build_local_fake_atomic_consumption_registry_driver(
                initial_state=(entry,),
                simulation_directives=(candidate,),
                clock=fixed_clock(),
            ),
            f"fehlendes Simulationsfeld {key}",
        )
        missing += 1

    extra_directive = copy.deepcopy(directive)
    extra_directive["unexpectedField"] = "forbidden"
    expect_value_error(
        lambda: module.build_local_fake_atomic_consumption_registry_driver(
            initial_state=(entry,),
            simulation_directives=(extra_directive,),
            clock=fixed_clock(),
        ),
        "zusätzliches Simulationsfeld",
    )
    additional += 1

    invalid_directive_values = {
        "operationId": "invalid",
        "phase": "invalid",
        "resultKind": "invalid",
        "commitVisibleToReconciliation": True,
    }
    for key, invalid in invalid_directive_values.items():
        candidate = copy.deepcopy(directive)
        candidate[key] = invalid
        expect_value_error(
            lambda candidate=candidate: module.build_local_fake_atomic_consumption_registry_driver(
                initial_state=(entry,),
                simulation_directives=(candidate,),
                clock=fixed_clock(),
            ),
            f"verändertes Simulationsfeld {key}",
        )
        changed += 1

    expect_value_error(
        lambda: module.build_local_fake_atomic_consumption_registry_driver(
            initial_state=[entry],
            simulation_directives=(),
            clock=fixed_clock(),
        ),
        "Initial-State-Liste statt Tupel",
    )
    changed += 1
    expect_value_error(
        lambda: module.build_local_fake_atomic_consumption_registry_driver(
            initial_state=(entry,),
            simulation_directives=[directive],
            clock=fixed_clock(),
        ),
        "Simulationsliste statt Tupel",
    )
    changed += 1
    expect_value_error(
        lambda: module.build_local_fake_atomic_consumption_registry_driver(
            initial_state=(entry, copy.deepcopy(entry)),
            simulation_directives=(),
            clock=fixed_clock(),
        ),
        "doppelte Registry-Identität",
    )
    changed += 1
    expect_value_error(
        lambda: module.build_local_fake_atomic_consumption_registry_driver(
            initial_state=(entry,),
            simulation_directives=(
                directive,
                copy.deepcopy(directive),
            ),
            clock=fixed_clock(),
        ),
        "doppelte Simulations-Operations-ID",
    )
    changed += 1
    expect_value_error(
        lambda: module.build_local_fake_atomic_consumption_registry_driver(
            initial_state=(entry,),
            simulation_directives=(),
            clock=object(),
        ),
        "fehlende injizierte Uhr",
    )
    changed += 1
    return missing, additional, changed


contract = load_contract()
require(
    canonical_fingerprint(contract) == EXPECTED_CONTRACT_FINGERPRINT,
    "v27.34a-Vertrag wurde verändert",
)
require(contract["version"] == "v27.34a", "Quellvertrag ist nicht v27.34a")
require(
    contract["pythonInterfaceBoundary"]["fakeDriverModulePath"]
    == MODULE_PATH.relative_to(ROOT).as_posix(),
    "Fake-Treibermodulpfad weicht vom Vertrag ab",
)
require(
    tuple(contract["inputBoundary"]["exactFieldOrder"]) == REQUEST_FIELDS,
    "Vertrag besitzt nicht die zehn erwarteten Eingabefelder",
)
require(
    tuple(contract["resultBoundary"]["exactResultKinds"]) == RESULT_KINDS,
    "Vertrag besitzt nicht die neun erwarteten Ergebnisarten",
)
require(
    tuple(contract["reconciliationBoundary"]["exactReconciliationKinds"])
    == RECONCILIATION_KINDS,
    "Vertrag besitzt nicht die drei Reconciliation-Arten",
)
require(MODULE_PATH.is_file(), "v27.34b-Fake-Treibermodul fehlt")
require(not ADAPTER_MODULE_PATH.exists(), "Echter Registry-Adapter wurde erstellt")

module_source = MODULE_PATH.read_text(encoding="utf-8")
module_tree = ast.parse(module_source, filename=str(MODULE_PATH))
for node in ast.walk(module_tree):
    if isinstance(node, ast.Import):
        for alias in node.names:
            require(
                alias.name.split(".")[0] in ALLOWED_IMPORT_ROOTS,
                f"Verbotener Import im Fake-Treiber: {alias.name}",
            )
    elif isinstance(node, ast.ImportFrom):
        root = (node.module or "").split(".")[0]
        require(
            root in ALLOWED_IMPORT_ROOTS,
            f"Verbotener Import im Fake-Treiber: {node.module}",
        )
    elif isinstance(node, ast.Call):
        if isinstance(node.func, ast.Name):
            require(
                node.func.id not in FORBIDDEN_CALL_NAMES,
                f"Verbotener Aufruf im Fake-Treiber: {node.func.id}",
            )
        elif isinstance(node.func, ast.Attribute):
            require(
                node.func.attr not in FORBIDDEN_CALL_ATTRIBUTES,
                f"Verbotener Aufruf im Fake-Treiber: .{node.func.attr}",
            )
require("datetime.now" not in module_source, "Nicht injizierter Uhrzugriff")
require("datetime.utcnow" not in module_source, "Nicht injizierter UTC-Zugriff")
require("os.environ" not in module_source, "Umgebungsvariablenzugriff erkannt")
require("AtomicConsumptionRegistryAdapter" not in module_source, "Adapter umgesetzt")
require(
    "build_atomic_consumption_registry_adapter" not in module_source,
    "Adapter-Factory umgesetzt",
)

module = load_module()
for type_name in (
    "AtomicConsumptionRequest",
    "ConsumptionRecordDraft",
    "ConfirmedConsumptionRecord",
    "EvidenceTemplate",
    "ConsumptionEvidence",
    "AtomicConsumptionResult",
    "ReconciliationResult",
    "FakeRegistryEntry",
    "FakeSimulationDirective",
    "InjectedUtcClock",
    "LocalFakeAtomicConsumptionRegistryDriver",
):
    require(hasattr(module, type_name), f"Python-Typ fehlt: {type_name}")

factory = module.build_local_fake_atomic_consumption_registry_driver
factory_signature = inspect.signature(factory)
require(
    tuple(factory_signature.parameters)
    == ("initial_state", "simulation_directives", "clock"),
    "Fake-Treiber-Factory-Parameter sind nicht exakt",
)
for parameter in factory_signature.parameters.values():
    require(
        parameter.kind is inspect.Parameter.KEYWORD_ONLY,
        f"Factory-Parameter ist nicht keyword-only: {parameter.name}",
    )
    require(
        parameter.default is inspect.Parameter.empty,
        f"Factory-Parameter besitzt Default: {parameter.name}",
    )
factory_annotations = factory.__annotations__
require(
    factory_annotations
    == {
        "initial_state": "tuple[FakeRegistryEntry, ...]",
        "simulation_directives": "tuple[FakeSimulationDirective, ...]",
        "clock": "InjectedUtcClock",
        "return": "LocalFakeAtomicConsumptionRegistryDriver",
    },
    "Fake-Treiber-Factory-Annotationen sind nicht exakt",
)

signature_request = make_request(synthetic_uuid(3001))
signature_driver, _, _ = build_driver(module, signature_request)
atomic_signature = inspect.signature(
    signature_driver.compare_and_set_with_consumption_record
)
require(
    tuple(atomic_signature.parameters) == ("request",),
    "Atomare Treiberoperation besitzt nicht exakt request",
)
atomic_parameter = atomic_signature.parameters["request"]
require(
    atomic_parameter.kind is inspect.Parameter.POSITIONAL_OR_KEYWORD,
    "request ist nicht positional-or-keyword",
)
require(
    atomic_parameter.annotation == "AtomicConsumptionRequest"
    and atomic_signature.return_annotation == "AtomicConsumptionResult",
    "Atomare Treiberannotationsbindung ist ungültig",
)
reconciliation_signature = inspect.signature(
    signature_driver.read_consumption_by_operation_id
)
require(
    tuple(reconciliation_signature.parameters) == ("operation_id",),
    "Reconciliation besitzt nicht exakt operation_id",
)
reconciliation_parameter = reconciliation_signature.parameters["operation_id"]
require(
    reconciliation_parameter.kind is inspect.Parameter.POSITIONAL_OR_KEYWORD,
    "operation_id ist nicht positional-or-keyword",
)
require(
    reconciliation_parameter.annotation == "str"
    and reconciliation_signature.return_annotation == "ReconciliationResult",
    "Reconciliation-Annotationsbindung ist ungültig",
)

results: dict[str, dict[str, object]] = {}

committed_request = make_request(synthetic_uuid(3101))
committed_driver, committed_clock, committed_initial = build_driver(
    module,
    committed_request,
)
committed_request_before = copy.deepcopy(committed_request)
committed_initial_before = copy.deepcopy(committed_initial)
committed = committed_driver.compare_and_set_with_consumption_record(
    committed_request
)
validate_result(
    contract,
    committed,
    "committed",
    committed_request["operationId"],
    committed_request,
)
require(
    committed_request == committed_request_before,
    "Erfolgsrequest wurde verändert",
)
require(committed_initial == committed_initial_before, "Initial-State wurde verändert")
require(committed_clock.calls == 1, "Injizierte Uhr wurde nicht exakt einmal gelesen")
results["committed"] = committed

replay_request = make_request(
    synthetic_uuid(3102),
    request_id=committed_request["requestId"],
    nonce=committed_request["authorizationNonce"],
    plan_fingerprint=committed_request["planFingerprint"],
    actor_id=committed_request["actorId"],
)
already_consumed = committed_driver.compare_and_set_with_consumption_record(
    replay_request
)
validate_result(
    contract,
    already_consumed,
    "already_consumed",
    replay_request["operationId"],
)
require(committed_clock.calls == 1, "Replay hat die Uhr erneut gelesen")
results["already_consumed"] = already_consumed

binding_request = make_request(
    synthetic_uuid(3103),
    request_id=committed_request["requestId"],
    nonce=committed_request["authorizationNonce"],
    plan_fingerprint="b" * 64,
    actor_id=committed_request["actorId"],
)
binding_driver, _, _ = build_driver(module, committed_request)
binding_conflict = binding_driver.compare_and_set_with_consumption_record(
    binding_request
)
validate_result(
    contract,
    binding_conflict,
    "binding_conflict",
    binding_request["operationId"],
)
results["binding_conflict"] = binding_conflict

expired_request = make_request(synthetic_uuid(3104))
expired_driver, expired_clock, _ = build_driver(
    module,
    expired_request,
    expires_at_utc="2029-12-31T23:59:59Z",
)
expired = expired_driver.compare_and_set_with_consumption_record(expired_request)
validate_result(
    contract,
    expired,
    "expired",
    expired_request["operationId"],
)
require(expired_clock.calls == 1, "Ablaufprüfung nutzte nicht die injizierte Uhr")
results["expired"] = expired

for index, (result_kind, phase) in enumerate(
    (
        ("adapter_unavailable", "connect"),
        ("atomicity_unavailable", "statement"),
        ("operation_failed", "operation"),
    ),
    start=3110,
):
    request = make_request(synthetic_uuid(index))
    clock = fixed_clock()
    driver, _, _ = build_driver(
        module,
        request,
        clock=clock,
        directives=(
            make_directive(
                request["operationId"],
                result_kind,
                phase=phase,
            ),
        ),
    )
    request_before = copy.deepcopy(request)
    result = driver.compare_and_set_with_consumption_record(request)
    validate_result(
        contract,
        result,
        result_kind,
        request["operationId"],
    )
    require(request == request_before, f"{result_kind}: Request wurde verändert")
    require(clock.calls == 0, f"{result_kind}: Uhr wurde unnötig gelesen")
    results[result_kind] = result

ambiguous_request = make_request(synthetic_uuid(3120))
ambiguous_driver, ambiguous_clock, _ = build_driver(
    module,
    ambiguous_request,
    directives=(
        make_directive(
            ambiguous_request["operationId"],
            "commit_ambiguous",
            phase="commit",
            visible=False,
        ),
    ),
)
ambiguous = ambiguous_driver.compare_and_set_with_consumption_record(
    ambiguous_request
)
validate_result(
    contract,
    ambiguous,
    "commit_ambiguous",
    ambiguous_request["operationId"],
)
require(ambiguous_clock.calls == 0, "Unsichtbare Ambiguität las die Uhr")
results["commit_ambiguous"] = ambiguous

blocking_request = make_request(synthetic_uuid(3130))
blocking_clock = BlockingClock(datetime(2030, 1, 1, tzinfo=timezone.utc))
parallel_driver, _, _ = build_driver(
    module,
    blocking_request,
    clock=blocking_clock,
)
winner_result: list[dict[str, object]] = []
winner_error: list[BaseException] = []


def run_parallel_winner() -> None:
    try:
        winner_result.append(
            parallel_driver.compare_and_set_with_consumption_record(
                blocking_request
            )
        )
    except BaseException as exc:
        winner_error.append(exc)


winner_thread = threading.Thread(target=run_parallel_winner)
winner_thread.start()
require(
    blocking_clock.entered.wait(timeout=5),
    "Parallelgewinner erreichte den atomaren Abschnitt nicht",
)
parallel_loser_request = make_request(
    synthetic_uuid(3131),
    request_id=blocking_request["requestId"],
    nonce=blocking_request["authorizationNonce"],
    plan_fingerprint=blocking_request["planFingerprint"],
    actor_id=blocking_request["actorId"],
)
parallel_conflict = parallel_driver.compare_and_set_with_consumption_record(
    parallel_loser_request
)
blocking_clock.release.set()
winner_thread.join(timeout=5)
require(not winner_thread.is_alive(), "Parallelgewinner-Thread hängt")
require(not winner_error, f"Parallelgewinner fehlgeschlagen: {winner_error}")
require(len(winner_result) == 1, "Parallelgewinner-Ergebnis fehlt")
validate_result(
    contract,
    winner_result[0],
    "committed",
    blocking_request["operationId"],
    blocking_request,
)
validate_result(
    contract,
    parallel_conflict,
    "parallel_conflict",
    parallel_loser_request["operationId"],
)
require(
    sum(
        result["resultKind"] == "committed"
        for result in (winner_result[0], parallel_conflict)
    )
    == 1,
    "Parallelversuch besitzt nicht exakt einen Gewinner",
)
results["parallel_conflict"] = parallel_conflict

require(set(results) == set(RESULT_KINDS), "Nicht alle neun Ergebnisse ausgeführt")

confirmed_before = snapshot_driver_state(committed_driver)
confirmed_reconciliation = (
    committed_driver.read_consumption_by_operation_id(
        committed_request["operationId"]
    )
)
confirmed_after = snapshot_driver_state(committed_driver)
validate_reconciliation(
    contract,
    confirmed_reconciliation,
    "confirmed",
    committed_request["operationId"],
)
require(
    confirmed_before == confirmed_after,
    "Confirmed-Reconciliation hat Zustand verändert",
)
require(
    confirmed_reconciliation["consumptionRecord"]
    == committed["consumptionRecord"],
    "Confirmed-Reconciliation-Record weicht vom Commit ab",
)
require(
    confirmed_reconciliation["evidence"] == committed["evidence"],
    "Confirmed-Reconciliation-Evidence weicht vom Commit ab",
)

not_found_operation_id = synthetic_uuid(3140)
not_found_before = snapshot_driver_state(committed_driver)
not_found_reconciliation = (
    committed_driver.read_consumption_by_operation_id(
        not_found_operation_id
    )
)
not_found_after = snapshot_driver_state(committed_driver)
validate_reconciliation(
    contract,
    not_found_reconciliation,
    "not_found",
    not_found_operation_id,
)
require(
    not_found_before == not_found_after,
    "Not-found-Reconciliation hat Zustand verändert",
)
require(
    not_found_reconciliation["consumptionStatus"] == "unknown",
    "not_found nimmt unzulässig unused an",
)

ambiguous_before = snapshot_driver_state(ambiguous_driver)
ambiguous_reconciliation = (
    ambiguous_driver.read_consumption_by_operation_id(
        ambiguous_request["operationId"]
    )
)
ambiguous_after = snapshot_driver_state(ambiguous_driver)
validate_reconciliation(
    contract,
    ambiguous_reconciliation,
    "ambiguous",
    ambiguous_request["operationId"],
)
require(
    ambiguous_before == ambiguous_after,
    "Ambiguous-Reconciliation hat Zustand verändert",
)

visible_request = make_request(synthetic_uuid(3150))
visible_driver, visible_clock, _ = build_driver(
    module,
    visible_request,
    directives=(
        make_directive(
            visible_request["operationId"],
            "commit_ambiguous",
            phase="commit",
            visible=True,
        ),
    ),
)
visible_ambiguous = visible_driver.compare_and_set_with_consumption_record(
    visible_request
)
validate_result(
    contract,
    visible_ambiguous,
    "commit_ambiguous",
    visible_request["operationId"],
)
require(visible_clock.calls == 1, "Sichtbarer Commit las Uhr nicht exakt einmal")
visible_confirmed = visible_driver.read_consumption_by_operation_id(
    visible_request["operationId"]
)
validate_reconciliation(
    contract,
    visible_confirmed,
    "confirmed",
    visible_request["operationId"],
)

retry_request = make_request(synthetic_uuid(3160))
retry_clock = fixed_clock()
retry_driver, _, _ = build_driver(
    module,
    retry_request,
    clock=retry_clock,
    directives=(
        make_directive(
            retry_request["operationId"],
            "operation_failed",
        ),
    ),
)
first_failure = retry_driver.compare_and_set_with_consumption_record(
    retry_request
)
retry_state_after_first = snapshot_driver_state(retry_driver)
second_failure = retry_driver.compare_and_set_with_consumption_record(
    retry_request
)
retry_state_after_second = snapshot_driver_state(retry_driver)
validate_result(
    contract,
    first_failure,
    "operation_failed",
    retry_request["operationId"],
)
require(first_failure == second_failure, "Fehler-Replay wurde erneut ausgeführt")
require(
    retry_state_after_first == retry_state_after_second,
    "Fehler-Replay hat Zustand verändert",
)
require(retry_clock.calls == 0, "Fehler-Replay hat Uhr gelesen")

instance_request_one = make_request(synthetic_uuid(3170))
instance_request_two = make_request(
    synthetic_uuid(3171),
    request_id=instance_request_one["requestId"],
    nonce=instance_request_one["authorizationNonce"],
    plan_fingerprint=instance_request_one["planFingerprint"],
    actor_id=instance_request_one["actorId"],
)
shared_initial_state = (make_entry(instance_request_one),)
shared_initial_before = copy.deepcopy(shared_initial_state)
instance_one = module.build_local_fake_atomic_consumption_registry_driver(
    initial_state=shared_initial_state,
    simulation_directives=(),
    clock=fixed_clock(),
)
instance_two = module.build_local_fake_atomic_consumption_registry_driver(
    initial_state=shared_initial_state,
    simulation_directives=(),
    clock=fixed_clock(),
)
instance_one_result = instance_one.compare_and_set_with_consumption_record(
    instance_request_one
)
instance_two_result = instance_two.compare_and_set_with_consumption_record(
    instance_request_two
)
validate_result(
    contract,
    instance_one_result,
    "committed",
    instance_request_one["operationId"],
)
validate_result(
    contract,
    instance_two_result,
    "committed",
    instance_request_two["operationId"],
)
require(
    shared_initial_state == shared_initial_before,
    "Geteilter Initial-State wurde verändert",
)

request_missing, request_additional, request_changed = (
    run_request_manipulation_matrix(module)
)
constructor_missing, constructor_additional, constructor_changed = (
    run_constructor_manipulation_matrix(module)
)

document_text = DOCUMENT_PATH.read_text(encoding="utf-8")
master_text = MASTERLIST_PATH.read_text(encoding="utf-8")
database_plan_text = DATABASE_PLAN_PATH.read_text(encoding="utf-8")
preflight_text = PREFLIGHT_PATH.read_text(encoding="utf-8")
v27_34a_checker_text = V27_34A_CHECKER_PATH.read_text(encoding="utf-8")
for token in (
    "Stand: v27.34b",
    "vollständig lokal",
    "In-Memory",
    "neun Ergebnisarten",
    "Reconciliation",
    "kein echter Registry-Adapter",
):
    require(token in document_text, f"v27.34b-Dokument fehlt: {token}")
require("| v27.34b |" in master_text, "Masterliste enthält v27.34b nicht")
require(
    "Erstes lokales Fake-Registry-Treibermodul v27.34b"
    in database_plan_text,
    "Datenbankplan enthält v27.34b nicht",
)
module_relative = MODULE_PATH.relative_to(ROOT).as_posix()
checker_relative = Path(__file__).resolve().relative_to(ROOT).as_posix()
document_relative = DOCUMENT_PATH.relative_to(ROOT).as_posix()
for relative in (module_relative, checker_relative, document_relative):
    require(relative in preflight_text, f"Preflight-Dateiliste fehlt: {relative}")
require(
    checker_relative in preflight_text,
    "v27.34b-Checker ist nicht im Preflight eingebunden",
)
require(
    "v27.34b" in v27_34a_checker_text
    and "FAKE_DRIVER_MODULE_PATH.exists()" in v27_34a_checker_text,
    "Historischer v27.34a-Checker ist nicht sicher auf v27.34b erweitert",
)

print("Lokaler Fake-Registry-Treiber v27.34b: OK")
print("Quellvertrag: v27.34a, kanonischer SHA-256 unverändert")
print("Fake-Treiber: vollständig lokal, deterministisch und In-Memory")
print("Eingabefelder: exakt 10, unverändert")
print("Ergebnisarten: exakt 9, vollständig ausgeführt")
print("Einmalverbrauch und Replay-Sperre: bestätigt")
print("Parallelgewinner: exakt einer, Konflikt geschlossen")
print("Consumption-Record und Evidence: konsistent und bestätigt")
print("Ambiguität: kontrolliert, kein automatischer Retry")
print("Reconciliation: confirmed, not_found und ambiguous, nur lesend")
print("Getrennte Instanzen: getrennter In-Memory-Zustand")
print(
    "Manipulationsmatrix Request: "
    f"{request_missing} fehlende, "
    f"{request_additional} zusätzliche, "
    f"{request_changed} veränderte Eingaben blockiert"
)
print(
    "Manipulationsmatrix Konstruktion: "
    f"{constructor_missing} fehlende, "
    f"{constructor_additional} zusätzliche, "
    f"{constructor_changed} veränderte Eingaben blockiert"
)
print("Echter Registry-Adapter: nicht implementiert")
print("Datenbank-, PostgreSQL-, SQL-, Supabase- und Netzwerkzugriff: keiner")
print("Datei-, Prozess-, Umgebungsvariablen- und UI-Zugriff: keiner")
print("Grant, Token und executionGrant: nicht erzeugt beziehungsweise false")
