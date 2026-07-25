from __future__ import annotations

import copy
import json
from collections.abc import Mapping

EXPECTED_IMPLEMENTATION_CONTRACT = json.loads(
    '{"ambiguityBoundary":{"assumeCommittedAllowed":false,"assumeUnusedAllowed":false,"automaticRetryAfterAmbiguousAllowed":false,"commitAmbiguousTerminalForAutomaticRetry":true,"reconciliationMayReadByOperationIdLater":true,"reconciliationMayWriteAllowed":false,"reconciliationRequired":true},"atomicityBoundary":{"alreadyConsumedIsTerminal":true,"bindingConflictIsTerminal":true,"compareAndSetAndConsumptionRecordSingleTransactionRequired":true,"consumptionRecordRequiredOnCommitted":true,"evidenceDerivedOnlyFromConfirmedRecord":true,"expiredIsTerminal":true,"parallelWinnerCountMaximum":1,"resetConsumedToUnusedAllowed":false},"contractVersion":1,"dependencyBoundary":{"connectionStringAllowed":false,"databaseConnectionAllowed":false,"databaseUrlAllowed":false,"dependencyInjectionRequired":true,"driverImportAllowed":false,"environmentVariableReadAllowed":false,"hardCodedCredentialsAllowed":false,"productionSecretAllowed":false,"realParticipantDataAllowed":false,"serviceRoleKeyAllowed":false},"implementationBoundary":{"adapterFactoryImplemented":false,"adapterImported":false,"adapterInstantiated":false,"adapterInterfaceImplemented":false,"adapterInvoked":false,"adapterModuleCreated":false,"atomicCompareAndSetPerformed":false,"authorizationConsumed":false,"authorizationGranted":false,"authorizationTokenGenerated":false,"databaseConnectionCreated":false,"databaseTestExecuted":false,"driverImported":false,"executionGrant":false,"filesystemMutationPerformed":false,"filesystemReadPerformed":false,"frontendIntegration":false,"implementationContractPrepared":true,"networkExecuted":false,"processExecuted":false,"registryReadPerformed":false,"registryWritePerformed":false,"sqlMigrationCreated":false,"trustedClockRead":false},"interfaceBoundary":{"adapterKind":"single_use_consumption_registry","connectTimeoutMilliseconds":3000,"desiredState":"consumed","exactInputFields":["operationId","requestId","authorizationNonce","planFingerprint","actorId","purpose","expectedState","desiredState","consumptionRecord","evidenceTemplate"],"exactResultKinds":["committed","already_consumed","parallel_conflict","binding_conflict","expired","adapter_unavailable","atomicity_unavailable","commit_ambiguous","operation_failed"],"executionGrant":false,"expectedState":"unused","factoryName":"build_atomic_consumption_registry_adapter","interfaceVersion":1,"lockTimeoutMilliseconds":2000,"maximumParallelWinners":1,"operationName":"consume_materialization_authorization_atomically","operationTimeoutMilliseconds":15000,"plannedModulePath":"tools/accaoui_disposable_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter.py","protocolName":"AtomicConsumptionRegistryAdapter","rawErrorSuppressed":true,"requiredCapability":"atomic_compare_and_set_with_consumption_record","singleAdapterInvocationRequired":true,"statementTimeoutMilliseconds":5000},"productiveReleaseAllowed":false,"securityBoundary":{"adapterImplementationAllowed":false,"adapterImportAllowed":false,"adapterInstantiationAllowed":false,"adapterInvocationAllowed":false,"atomicCompareAndSetAllowed":false,"authorizationConsumptionAllowed":false,"authorizationGrantAllowed":false,"authorizationTokenAllowed":false,"connectionStringAllowed":false,"databaseConnectionAllowed":false,"databaseUrlAllowed":false,"directAppExecutionGrantAllowed":false,"driverImportAllowed":false,"filesystemMutationAllowed":false,"filesystemReadAllowed":false,"frontendReferenceAllowed":false,"networkExecutionAllowed":false,"passwordAllowed":false,"processEnvironmentReadAllowed":false,"processExecutionAllowed":false,"productionSecretAllowed":false,"realParticipantDataAllowed":false,"reconciliationReadAllowed":false,"registryReadAllowed":false,"registryWriteAllowed":false,"serviceRoleKeyAllowed":false,"trustedClockReadAllowed":false},"sourceBoundary":{"allSourceSecurityFlagsMustBeFalse":true,"requiredAccepted":true,"requiredAcceptedReason":"authorization_atomic_consumption_registry_adapter_execution_plan_accepted_execution_locked","requiredAcceptedStatus":"accepted_atomic_consumption_registry_adapter_execution_plan_execution_locked","requiredExecutionGrant":false,"requiredSourceStatus":"implemented_pure_atomic_consumption_registry_adapter_execution_plan_acceptance_execution_locked","requiredSourceVersion":"v27.33f"},"status":"planned_atomic_consumption_registry_adapter_implementation_fully_locked_not_implemented","unresolvedRequirements":{"databaseTestExecution":true,"directAppExecutionGrant":true,"environmentEvidenceCollector":true,"environmentMaterializer":true,"environmentRollbackImplementation":true,"frontendIntegration":true,"materializationAuthorizationConsumptionReceipt":true,"registryAdapterExecution":true,"registryAdapterImplementation":true,"registryAdapterImplementationDescriptor":true,"registryAdapterInstantiation":true,"registryAdapterReconciliation":true},"version":"v27.33g"}'
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

SOURCE_KEYS = frozenset({
    "status",
    "reason",
    "ready",
    "plan",
    *LOCKED_FLAGS,
})

PLAN_KEYS = frozenset({
    "planVersion",
    "sourceStatus",
    "sourceReason",
    "acceptedReadiness",
    "implementationPlanFacts",
    "implementationSequence",
    "adapterImplementationAllowed",
    "adapterImportAllowed",
    "adapterInstantiationAllowed",
    "adapterInvocationAllowed",
    "registryReadAllowed",
    "registryWriteAllowed",
    "atomicCompareAndSetAllowed",
    "authorizationConsumptionAllowed",
    "executionGrant",
})

EXPECTED_SEQUENCE = [
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

EXPECTED_IMPLEMENTATION_FACTS = {
    "adapterKind": "single_use_consumption_registry",
    "plannedModulePath": (
        "tools/accaoui_disposable_test_python_environment_"
        "materialization_authorization_atomic_consumption_"
        "registry_adapter.py"
    ),
    "interfaceVersion": 1,
    "protocolName": "AtomicConsumptionRegistryAdapter",
    "factoryName": "build_atomic_consumption_registry_adapter",
    "operationName": (
        "consume_materialization_authorization_atomically"
    ),
    "requiredCapability": (
        "atomic_compare_and_set_with_consumption_record"
    ),
    "expectedState": "unused",
    "desiredState": "consumed",
    "exactInputFields": [
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
    ],
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
    "singleAdapterInvocationRequired": True,
    "maximumParallelWinners": 1,
    "operationTimeoutMilliseconds": 15000,
    "connectTimeoutMilliseconds": 3000,
    "statementTimeoutMilliseconds": 5000,
    "lockTimeoutMilliseconds": 2000,
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

EXPECTED_ACCEPTED_DESCRIPTOR = {
    "descriptorVersion": 1,
    "sourceContractVersion": "v27.33g",
    "sourceContractStatus": (
        "planned_atomic_consumption_registry_adapter_"
        "implementation_fully_locked_not_implemented"
    ),
    "contractFacts": EXPECTED_IMPLEMENTATION_CONTRACT,
    "executionGrant": False,
}

EXPECTED_ACCEPTED_READINESS = {
    "readinessVersion": 1,
    "sourceStatus": (
        "accepted_atomic_consumption_registry_adapter_"
        "implementation_descriptor_execution_locked"
    ),
    "sourceReason": (
        "authorization_atomic_consumption_registry_adapter_"
        "implementation_descriptor_accepted_execution_locked"
    ),
    "acceptedDescriptor": EXPECTED_ACCEPTED_DESCRIPTOR,
    "implementationFacts": EXPECTED_IMPLEMENTATION_FACTS,
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

EXPECTED_PLAN_FACTS = {
    "adapterKind": "single_use_consumption_registry",
    "plannedModulePath": (
        "tools/accaoui_disposable_test_python_environment_"
        "materialization_authorization_atomic_consumption_"
        "registry_adapter.py"
    ),
    "protocolName": "AtomicConsumptionRegistryAdapter",
    "factoryName": "build_atomic_consumption_registry_adapter",
    "operationName": (
        "consume_materialization_authorization_atomically"
    ),
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
    "implementationSequence": EXPECTED_SEQUENCE,
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

SUCCESS_SOURCE_STATUS = (
    "atomic_consumption_registry_adapter_implementation_plan_"
    "ready_execution_locked"
)
SUCCESS_SOURCE_REASON = (
    "authorization_atomic_consumption_registry_adapter_"
    "implementation_plan_ready_execution_locked"
)
ACCEPTED_STATUS = (
    "accepted_atomic_consumption_registry_adapter_implementation_"
    "plan_execution_locked"
)
ACCEPTED_REASON = (
    "authorization_atomic_consumption_registry_adapter_"
    "implementation_plan_accepted_execution_locked"
)
BLOCKED_STATUS = (
    "atomic_consumption_registry_adapter_implementation_plan_"
    "acceptance_blocked_execution_locked"
)


def locked_flags() -> dict[str, bool]:
    return {key: False for key in LOCKED_FLAGS}


def blocked(reason: str) -> dict[str, object]:
    return {
        "status": BLOCKED_STATUS,
        "reason": reason,
        "accepted": False,
        "acceptedPlan": None,
        **locked_flags(),
    }


def accept_atomic_consumption_registry_adapter_implementation_plan(
    candidate: object,
) -> dict[str, object]:
    if not isinstance(candidate, Mapping):
        return blocked("implementation_plan_acceptance_invalid_input")

    source = dict(candidate)
    if set(source) != SOURCE_KEYS:
        return blocked(
            "implementation_plan_acceptance_structure_invalid"
        )
    if source["status"] != SUCCESS_SOURCE_STATUS:
        return blocked(
            "implementation_plan_acceptance_status_invalid"
        )
    if source["reason"] != SUCCESS_SOURCE_REASON:
        return blocked(
            "implementation_plan_acceptance_reason_invalid"
        )
    if source["ready"] is not True:
        return blocked(
            "implementation_plan_acceptance_ready_invalid"
        )

    for key in LOCKED_FLAGS:
        if source[key] is not False:
            return blocked(
                "implementation_plan_acceptance_source_boundary_open"
            )

    plan = source["plan"]
    if not isinstance(plan, Mapping):
        return blocked(
            "implementation_plan_acceptance_plan_invalid"
        )

    data = dict(plan)
    if set(data) != PLAN_KEYS:
        return blocked(
            "implementation_plan_acceptance_plan_structure_invalid"
        )
    if data["planVersion"] != 1:
        return blocked(
            "implementation_plan_acceptance_version_invalid"
        )
    if data["sourceStatus"] != (
        "accepted_atomic_consumption_registry_adapter_"
        "implementation_readiness_execution_locked"
    ):
        return blocked(
            "implementation_plan_acceptance_bound_status_invalid"
        )
    if data["sourceReason"] != (
        "authorization_atomic_consumption_registry_adapter_"
        "implementation_readiness_accepted_execution_locked"
    ):
        return blocked(
            "implementation_plan_acceptance_bound_reason_invalid"
        )

    accepted_readiness = data["acceptedReadiness"]
    if type(accepted_readiness) is not dict:
        return blocked(
            "implementation_plan_acceptance_readiness_invalid"
        )
    if accepted_readiness != EXPECTED_ACCEPTED_READINESS:
        return blocked(
            "implementation_plan_acceptance_readiness_invalid"
        )

    plan_facts = data["implementationPlanFacts"]
    if type(plan_facts) is not dict:
        return blocked(
            "implementation_plan_acceptance_facts_invalid"
        )
    if plan_facts != EXPECTED_PLAN_FACTS:
        return blocked(
            "implementation_plan_acceptance_facts_invalid"
        )

    if data["implementationSequence"] != EXPECTED_SEQUENCE:
        return blocked(
            "implementation_plan_acceptance_sequence_invalid"
        )

    for key in (
        "adapterImplementationAllowed",
        "adapterImportAllowed",
        "adapterInstantiationAllowed",
        "adapterInvocationAllowed",
        "registryReadAllowed",
        "registryWriteAllowed",
        "atomicCompareAndSetAllowed",
        "authorizationConsumptionAllowed",
        "executionGrant",
    ):
        if data[key] is not False:
            return blocked(
                "implementation_plan_acceptance_plan_boundary_open"
            )

    return {
        "status": ACCEPTED_STATUS,
        "reason": ACCEPTED_REASON,
        "accepted": True,
        "acceptedPlan": copy.deepcopy(data),
        **locked_flags(),
    }
