from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MIGRATIONS = ROOT / "supabase" / "migrations"

CONTRACT = ROOT / "docs" / "contracts" / (
    "exam-history-disposable-postgresql-test-python-environment-"
    "materialization-authorization-atomic-consumption-registry-"
    "adapter-implementation-execution-authorization-contract.json"
)
SOURCE_CONTRACT = ROOT / "docs" / "contracts" / (
    "exam-history-disposable-postgresql-test-python-environment-"
    "materialization-authorization-atomic-consumption-registry-"
    "adapter-implementation-execution-plan-acceptance-guard-contract.json"
)
EXECUTION_CONTRACT = ROOT / "docs" / "contracts" / (
    "exam-history-disposable-postgresql-test-python-environment-"
    "materialization-authorization-atomic-consumption-registry-"
    "adapter-implementation-execution-contract.json"
)

DESCRIPTOR_MODULE = ROOT / "tools" / (
    "accaoui_disposable_test_python_environment_materialization_"
    "authorization_atomic_consumption_registry_adapter_"
    "implementation_execution_descriptor.py"
)
DESCRIPTOR_ACCEPTANCE_MODULE = ROOT / "tools" / (
    "accaoui_disposable_test_python_environment_materialization_"
    "authorization_atomic_consumption_registry_adapter_"
    "implementation_execution_descriptor_acceptance_guard.py"
)
READINESS_MODULE = ROOT / "tools" / (
    "accaoui_disposable_test_python_environment_materialization_"
    "authorization_atomic_consumption_registry_adapter_"
    "implementation_execution_readiness.py"
)
READINESS_ACCEPTANCE_MODULE = ROOT / "tools" / (
    "accaoui_disposable_test_python_environment_materialization_"
    "authorization_atomic_consumption_registry_adapter_"
    "implementation_execution_readiness_acceptance_guard.py"
)
PLAN_MODULE = ROOT / "tools" / (
    "accaoui_disposable_test_python_environment_materialization_"
    "authorization_atomic_consumption_registry_adapter_"
    "implementation_execution_plan.py"
)
PLAN_ACCEPTANCE_MODULE = ROOT / "tools" / (
    "accaoui_disposable_test_python_environment_materialization_"
    "authorization_atomic_consumption_registry_adapter_"
    "implementation_execution_plan_acceptance_guard.py"
)

FUTURE_DESCRIPTOR = ROOT / "tools" / (
    "accaoui_disposable_test_python_environment_materialization_"
    "authorization_atomic_consumption_registry_adapter_"
    "implementation_execution_authorization_descriptor.py"
)
FUTURE_ADAPTER = ROOT / "tools" / (
    "accaoui_disposable_test_python_environment_materialization_"
    "authorization_atomic_consumption_registry_adapter.py"
)
FUTURE_EXECUTION = ROOT / "tools" / (
    "accaoui_disposable_test_python_environment_materialization_"
    "authorization_atomic_consumption_registry_adapter_execution.py"
)

LOCKED_FLAGS = (
    "adapterModuleCreated",
    "adapterInterfaceImplemented",
    "adapterFactoryImplemented",
    "adapterImported",
    "adapterInstantiated",
    "adapterInvoked",
    "registryReadPerformed",
    "registryWritePerformed",
    "atomicCompareAndSetPerformed",
    "authorizationConsumed",
    "authorizationGranted",
    "authorizationTokenGenerated",
    "trustedClockRead",
    "filesystemReadPerformed",
    "filesystemMutationPerformed",
    "processExecuted",
    "networkExecuted",
    "driverImported",
    "databaseConnectionCreated",
    "databaseTestExecuted",
    "sqlMigrationCreated",
    "frontendIntegration",
    "executionGrant",
)


def fail(message):
    print(f"FEHLER: {message}")
    raise SystemExit(1)


def load_json(path, label):
    if not path.is_file():
        fail(f"{label} fehlt.")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"{label} ungültig: {exc}")


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        fail(f"Modul nicht ladbar: {path.name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def clone(value):
    return copy.deepcopy(value)


def fingerprint(value):
    canonical = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


contract = load_json(CONTRACT, "v27.33u-Vertrag")
source_contract = load_json(
    SOURCE_CONTRACT,
    "v27.33t-Quellvertrag",
)
execution_contract = load_json(
    EXECUTION_CONTRACT,
    "v27.33n-Ausführungsvertrag",
)

if contract.get("version") != "v27.33u":
    fail("Autorisierungsvertrag besitzt nicht v27.33u.")
if contract.get("contractVersion") != 1:
    fail("Autorisierungsvertrag besitzt nicht Schema 1.")
if contract.get("status") != (
    "planned_atomic_consumption_registry_adapter_implementation_"
    "execution_authorization_fully_locked_not_implemented"
):
    fail("Autorisierungsvertragsstatus ist ungültig.")
if contract.get("productiveReleaseAllowed") is not False:
    fail("Produktive Freigabe ist offen.")

if source_contract.get("version") != "v27.33t":
    fail("Quellvertrag besitzt nicht v27.33t.")
if source_contract.get("status") != (
    "implemented_pure_atomic_consumption_registry_adapter_"
    "implementation_execution_plan_acceptance_execution_locked"
):
    fail("Quellvertragsstatus ist ungültig.")

descriptor_module = load_module(
    DESCRIPTOR_MODULE,
    "v2733u_descriptor",
)
descriptor_acceptance_module = load_module(
    DESCRIPTOR_ACCEPTANCE_MODULE,
    "v2733u_descriptor_acceptance",
)
readiness_module = load_module(
    READINESS_MODULE,
    "v2733u_readiness",
)
readiness_acceptance_module = load_module(
    READINESS_ACCEPTANCE_MODULE,
    "v2733u_readiness_acceptance",
)
plan_module = load_module(
    PLAN_MODULE,
    "v2733u_plan",
)
plan_acceptance_module = load_module(
    PLAN_ACCEPTANCE_MODULE,
    "v2733u_plan_acceptance",
)

descriptor_result = (
    descriptor_module
    .resolve_atomic_consumption_registry_adapter_implementation_execution_descriptor({
        "contractFacts": clone(execution_contract),
    })
)
accepted_descriptor = (
    descriptor_acceptance_module
    .accept_atomic_consumption_registry_adapter_implementation_execution_descriptor(
        descriptor_result
    )
)
readiness_result = (
    readiness_module
    .resolve_atomic_consumption_registry_adapter_implementation_execution_readiness({
        "acceptedExecutionDescriptorResult": accepted_descriptor,
        "executionCapabilityFacts": clone(
            readiness_module.EXPECTED_EXECUTION_CAPABILITY_FACTS
        ),
    })
)
accepted_readiness = (
    readiness_acceptance_module
    .accept_atomic_consumption_registry_adapter_implementation_execution_readiness(
        readiness_result
    )
)
plan_result = (
    plan_module
    .resolve_atomic_consumption_registry_adapter_implementation_execution_plan({
        "acceptedExecutionReadinessResult": accepted_readiness,
        "executionPlanFacts": clone(
            plan_module.EXPECTED_EXECUTION_PLAN_FACTS
        ),
    })
)
accepted_plan = (
    plan_acceptance_module
    .accept_atomic_consumption_registry_adapter_implementation_execution_plan(
        plan_result
    )
)

if accepted_plan.get("status") != (
    "accepted_atomic_consumption_registry_adapter_implementation_"
    "execution_plan_execution_locked"
):
    fail("Quell-Plan-Annahme liefert keinen Erfolgsstatus.")
if accepted_plan.get("reason") != (
    "authorization_atomic_consumption_registry_adapter_"
    "implementation_execution_plan_accepted_execution_locked"
):
    fail("Quell-Plan-Annahmegrund ist ungültig.")
if accepted_plan.get("accepted") is not True:
    fail("Quell-Plan wurde nicht angenommen.")

for key in LOCKED_FLAGS:
    if accepted_plan.get(key) is not False:
        fail(f"Quell-Plan-Annahme öffnet Grenze: {key}")

plan = accepted_plan.get("acceptedPlan")
if not isinstance(plan, dict):
    fail("Kanonischer angenommener Plan fehlt.")

source = contract.get("sourceBoundary", {})
expected_source = {
    "requiredSourceVersion": "v27.33t",
    "requiredSourceStatus": source_contract["status"],
    "requiredAcceptedStatus": accepted_plan["status"],
    "requiredAcceptedReason": accepted_plan["reason"],
    "requiredAccepted": True,
    "requiredPlanVersion": 1,
    "requiredStepCount": 12,
    "requiredAcceptedPlanFingerprint": fingerprint(plan),
    "canonicalFingerprintEncoding": "json_utf8_sorted_keys_compact",
    "requiredExecutionGrant": False,
    "allSourceSecurityFlagsMustBeFalse": True,
    "exactCanonicalAcceptedPlanRequired": True,
}
for key, expected in expected_source.items():
    if source.get(key) != expected:
        fail(f"Quellgrenze ist ungültig: {key}")

if plan.get("planVersion") != 1:
    fail("Angenommener Plan besitzt nicht Version 1.")
if len(plan.get("implementationSequence", [])) != 12:
    fail("Angenommener Plan besitzt nicht zwölf Schritte.")
if plan.get("executionGrant") is not False:
    fail("Angenommener Plan öffnet den Grant.")

identity = contract.get("identityBoundary", {})
if identity.get("exactIdentityFields") != [
    "operationId",
    "requestId",
    "authorizationNonce",
    "planFingerprint",
    "actorId",
    "purpose",
]:
    fail("Identitätsfelder sind ungültig.")
for key in (
    "allIdentityFieldsRequired",
    "allIdentityFieldsMustBeNonEmptyStrings",
    "identityFieldsImmutable",
    "planFingerprintMustEqualAcceptedPlanFingerprint",
):
    if identity.get(key) is not True:
        fail(f"Identitätsgrenze fehlt: {key}")
for key in (
    "identitySubstitutionAllowed",
    "operationIdReuseWithDifferentBindingAllowed",
    "requestIdReuseWithDifferentBindingAllowed",
    "authorizationNonceReuseAllowed",
    "actorIdSubstitutionAllowed",
    "purposeSubstitutionAllowed",
):
    if identity.get(key) is not False:
        fail(f"Identitätsgrenze ist offen: {key}")

authorization = contract.get("authorizationBoundary", {})
if authorization.get("authorizationContractPrepared") is not True:
    fail("Autorisierungsvertrag ist nicht vorbereitet.")
if authorization.get("singleUseRequired") is not True:
    fail("Einmalverbrauch ist nicht verpflichtend.")
if authorization.get("replayAllowed") is not False:
    fail("Replay ist erlaubt.")
if authorization.get("maximumParallelWinners") != 1:
    fail("Parallelgewinnergrenze ist ungültig.")
if authorization.get("expectedState") != "unused":
    fail("Erwarteter Zustand ist ungültig.")
if authorization.get("desiredState") != "consumed":
    fail("Zielzustand ist ungültig.")
if len(authorization.get("requiredResultKinds", [])) != 9:
    fail("Ergebnisarten sind unvollständig.")
for key in (
    "authorizationGrantCreated",
    "authorizationTokenGenerated",
    "authorizationMayBeConsumed",
    "executionGrant",
):
    if authorization.get(key) is not False:
        fail(f"Autorisierungsgrenze ist offen: {key}")

atomicity = contract.get("atomicityBoundary", {})
for key in (
    "singleAdapterInvocationRequired",
    "singleTransactionRequired",
    "compareAndSetAndConsumptionRecordSingleTransactionRequired",
    "consumptionRecordRequiredOnCommitted",
    "evidenceDerivedOnlyFromConfirmedRecord",
    "alreadyConsumedIsTerminal",
    "parallelConflictIsTerminal",
    "bindingConflictIsTerminal",
    "expiredIsTerminal",
    "commitAmbiguousTerminalForAutomaticRetry",
):
    if atomicity.get(key) is not True:
        fail(f"Atomaritätsgrenze fehlt: {key}")
if atomicity.get("maximumParallelWinners") != 1:
    fail("Atomaritäts-Parallelgrenze ist ungültig.")
for key in (
    "resetConsumedToUnusedAllowed",
    "assumeCommittedAllowed",
    "assumeUnusedAllowed",
):
    if atomicity.get(key) is not False:
        fail(f"Atomaritätsgrenze ist offen: {key}")

timeouts = contract.get("timeoutBoundary", {})
expected_timeouts = {
    "operationTimeoutMilliseconds": 15000,
    "connectTimeoutMilliseconds": 3000,
    "statementTimeoutMilliseconds": 5000,
    "lockTimeoutMilliseconds": 2000,
    "timeoutValuesImmutable": True,
    "timeoutExpansionAllowed": False,
}
for key, expected in expected_timeouts.items():
    if timeouts.get(key) != expected:
        fail(f"Zeitlimitgrenze ist ungültig: {key}")

failure = contract.get("failureBoundary", {})
if failure.get("rawErrorExposed") is not False:
    fail("Rohfehler werden offengelegt.")
if failure.get("automaticRetryAfterAmbiguousAllowed") is not False:
    fail("Automatischer Retry nach unklarem Commit ist offen.")
if failure.get("unknownFailureResultKind") != "operation_failed":
    fail("Unbekannter Fehler wird falsch abgebildet.")
for key in (
    "failureMayGrantAuthorization",
    "failureMayAssumeConsumption",
    "failureMayResetConsumption",
):
    if failure.get(key) is not False:
        fail(f"Fehlergrenze ist offen: {key}")

reconciliation = contract.get("reconciliationBoundary", {})
if reconciliation.get("reconciliationRequired") is not True:
    fail("Reconciliation ist nicht verpflichtend.")
if reconciliation.get("reconciliationIdentityField") != "operationId":
    fail("Reconciliation-Identität ist ungültig.")
if reconciliation.get(
    "reconciliationMayReadByOperationIdLater"
) is not True:
    fail("Spätere Reconciliation ist nicht beschrieben.")
for key in (
    "reconciliationMayWriteAllowed",
    "reconciliationMayGrantAuthorization",
    "reconciliationMayResetConsumedState",
    "reconciliationExecutionPerformed",
):
    if reconciliation.get(key) is not False:
        fail(f"Reconciliation-Grenze ist offen: {key}")

implementation = contract.get("implementationBoundary", {})
if implementation.get(
    "implementationExecutionAuthorizationContractPrepared"
) is not True:
    fail("Autorisierungsvertrag ist nicht markiert.")
for key, value in implementation.items():
    if key == (
        "implementationExecutionAuthorizationContractPrepared"
    ):
        continue
    if value is not False:
        fail(f"Implementierungsgrenze ist offen: {key}")

for block in ("securityBoundary", "futureBoundary"):
    values = contract.get(block, {})
    if not isinstance(values, dict) or not values:
        fail(f"{block} fehlt.")
    for key, value in values.items():
        if value is not False:
            fail(f"{block} ist offen: {key}")

if FUTURE_DESCRIPTOR.exists():
    fail("v27.33u darf noch keinen Autorisierungsdescriptor umsetzen.")
if FUTURE_ADAPTER.exists():
    fail("v27.33u darf noch keinen Registry-Adapter implementieren.")
if FUTURE_EXECUTION.exists():
    fail("v27.33u darf noch keine Adapter-Ausführung umsetzen.")
if list(MIGRATIONS.glob("*v2733u*.sql")):
    fail("v27.33u darf keine SQL-Migration erzeugen.")

print(
    "Registry-Adapter-Implementierungsausführungs-"
    "Autorisierungsvertrag: OK"
)
print("Quell-Plan-Annahme: v27.33t")
print("Kanonischer Planfingerprint: geprüft")
print("Identitätsbindung: sechs unveränderliche Felder")
print("Einmalverbrauch und Replay-Sperre: geprüft")
print("Atomarität und Zeitlimits: geprüft")
print("Fehler- und Reconciliation-Grenzen: geprüft")
print("Autorisierungsgrant erstellt: nein")
print("Autorisierung verbraucht: nein")
print("Adaptermodul erstellt: nein")
print("Adapter aufgerufen: nein")
print("Registryzugriff: keiner")
print("Datenbankverbindung: keine")
print("SQL-Migration v27.33u: keine")
print("Produktive Freigabe: nein")
