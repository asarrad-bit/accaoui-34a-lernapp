from __future__ import annotations

import copy
from collections.abc import Mapping

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

INPUT_KEYS = frozenset({
    "acceptedImplementationReadinessResult",
    "implementationPlanFacts",
})

SOURCE_KEYS = frozenset({
    "status",
    "reason",
    "accepted",
    "acceptedReadiness",
    *LOCKED_FLAGS,
})

IMPLEMENTATION_SEQUENCE = [
    "validate_dependency_injection_boundary",
    "define_protocol_and_result_types",
    "implement_factory_without_default_credentials",
    "implement_transaction_boundary",
    "implement_atomic_compare_and_set_with_consumption_record",
    "map_exact_result_kinds",
    "implement_commit_ambiguity_terminal_handling",
    "implement_operation_id_reconciliation_read_contract",
    "add_pure_adapter_unit_fixtures",
    "keep_adapter_uninstantiated_and_uninvoked",
]

EXPECTED_PLAN_FACTS = {
    "adapterKind": "single_use_consumption_registry",
    "plannedModulePath": (
        "tools/accaoui_disposable_test_python_environment_"
        "materialization_authorization_atomic_consumption_"
        "registry_adapter.py"
    ),
    "protocolName": "AtomicConsumptionRegistryAdapter",
    "factoryName": "build_atomic_consumption_registry_adapter",
    "operationName": "consume_materialization_authorization_atomically",
    "requiredCapability": (
        "atomic_compare_and_set_with_consumption_record"
    ),
    "expectedState": "unused",
    "desiredState": "consumed",
    "exactResultKinds": [
        "committed",
        "already_consumed",
        "parallel_conflict",
        "binding_conflict",
        "expired",
        "adapter_unavailable",
        "atomicity_unavailable",
        "commit_ambiguous",
        "operation_failed",
    ],
    "implementationSequence": list(IMPLEMENTATION_SEQUENCE),
    "singleAdapterInvocationRequired": True,
    "maximumParallelWinners": 1,
    "dependencyInjectionRequired": True,
    "hardCodedCredentialsAllowed": False,
    "environmentVariableReadAllowed": False,
    "driverImportAllowed": False,
    "databaseConnectionAllowed": False,
    "rawErrorSuppressed": True,
    "automaticRetryAfterAmbiguousAllowed": False,
    "reconciliationRequired": True,
    "adapterModuleCreated": False,
    "adapterInterfaceImplemented": False,
    "adapterFactoryImplemented": False,
    "adapterImported": False,
    "adapterInstantiated": False,
    "adapterInvoked": False,
    "executionGrant": False,
}

SUCCESS_STATUS = (
    "atomic_consumption_registry_adapter_implementation_plan_"
    "ready_execution_locked"
)
SUCCESS_REASON = (
    "authorization_atomic_consumption_registry_adapter_"
    "implementation_plan_ready_execution_locked"
)
BLOCKED_STATUS = (
    "atomic_consumption_registry_adapter_implementation_plan_"
    "blocked_execution_locked"
)


def locked_flags() -> dict[str, bool]:
    return {key: False for key in LOCKED_FLAGS}


def blocked(reason: str) -> dict[str, object]:
    return {
        "status": BLOCKED_STATUS,
        "reason": reason,
        "ready": False,
        "plan": None,
        **locked_flags(),
    }


def resolve_atomic_consumption_registry_adapter_implementation_plan(
    value: object,
) -> dict[str, object]:
    if not isinstance(value, Mapping):
        return blocked("implementation_plan_invalid_input")

    source = dict(value)
    if set(source) != INPUT_KEYS:
        return blocked("implementation_plan_structure_invalid")

    accepted = source["acceptedImplementationReadinessResult"]
    if not isinstance(accepted, Mapping):
        return blocked("implementation_plan_source_invalid")

    accepted_data = dict(accepted)
    if set(accepted_data) != SOURCE_KEYS:
        return blocked("implementation_plan_source_structure_invalid")
    if accepted_data["status"] != (
        "accepted_atomic_consumption_registry_adapter_implementation_"
        "readiness_execution_locked"
    ):
        return blocked("implementation_plan_source_status_invalid")
    if accepted_data["reason"] != (
        "authorization_atomic_consumption_registry_adapter_"
        "implementation_readiness_accepted_execution_locked"
    ):
        return blocked("implementation_plan_source_reason_invalid")
    if accepted_data["accepted"] is not True:
        return blocked("implementation_plan_source_acceptance_invalid")

    for key in LOCKED_FLAGS:
        if accepted_data[key] is not False:
            return blocked("implementation_plan_source_boundary_open")

    accepted_readiness = accepted_data["acceptedReadiness"]
    if not isinstance(accepted_readiness, Mapping):
        return blocked("implementation_plan_readiness_invalid")

    facts = source["implementationPlanFacts"]
    if not isinstance(facts, Mapping):
        return blocked("implementation_plan_facts_invalid")
    if dict(facts) != EXPECTED_PLAN_FACTS:
        return blocked("implementation_plan_facts_invalid")

    plan = {
        "planVersion": 1,
        "sourceStatus": accepted_data["status"],
        "sourceReason": accepted_data["reason"],
        "acceptedReadiness": copy.deepcopy(dict(accepted_readiness)),
        "implementationPlanFacts": copy.deepcopy(EXPECTED_PLAN_FACTS),
        "implementationSequence": list(IMPLEMENTATION_SEQUENCE),
        "adapterImplementationAllowed": False,
        "adapterImportAllowed": False,
        "adapterInstantiationAllowed": False,
        "adapterInvocationAllowed": False,
        "registryReadAllowed": False,
        "registryWriteAllowed": False,
        "atomicCompareAndSetAllowed": False,
        "authorizationConsumptionAllowed": False,
        "executionGrant": False,
    }

    return {
        "status": SUCCESS_STATUS,
        "reason": SUCCESS_REASON,
        "ready": True,
        "plan": plan,
        **locked_flags(),
    }
