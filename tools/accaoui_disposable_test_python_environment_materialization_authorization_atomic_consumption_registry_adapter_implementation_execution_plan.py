from __future__ import annotations

import copy
import json
from collections.abc import Mapping

EXPECTED_ACCEPTED_READINESS = json.loads(
    '{"acceptedDescriptor":{"contractFacts":{"atomicityBoundary":{"alreadyConsumedIsTerminal":true,"assumeCommittedAllowed":false,"assumeUnusedAllowed":false,"bindingConflictIsTerminal":true,"commitAmbiguousTerminalForAutomaticRetry":true,"compareAndSetAndConsumptionRecordSingleTransactionRequired":true,"consumptionRecordRequiredOnCommitted":true,"evidenceDerivedOnlyFromConfirmedRecord":true,"expiredIsTerminal":true,"maximumParallelWinners":1,"resetConsumedToUnusedAllowed":false,"singleTransactionRequired":true},"contractVersion":1,"executionInterfaceBoundary":{"adapterKind":"single_use_consumption_registry","automaticRetryAfterAmbiguousAllowed":false,"connectTimeoutMilliseconds":3000,"databaseConnectionAllowed":false,"dependencyInjectionRequired":true,"desiredState":"consumed","driverImportAllowed":false,"environmentVariableReadAllowed":false,"exactInputFields":["operationId","requestId","authorizationNonce","planFingerprint","actorId","purpose","expectedState","desiredState","consumptionRecord","evidenceTemplate"],"exactResultKinds":["committed","already_consumed","parallel_conflict","binding_conflict","expired","adapter_unavailable","atomicity_unavailable","commit_ambiguous","operation_failed"],"executionGrant":false,"expectedState":"unused","factoryName":"build_atomic_consumption_registry_adapter","hardCodedCredentialsAllowed":false,"lockTimeoutMilliseconds":2000,"maximumParallelWinners":1,"operationName":"consume_materialization_authorization_atomically","operationTimeoutMilliseconds":15000,"plannedModulePath":"tools/accaoui_disposable_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter.py","protocolName":"AtomicConsumptionRegistryAdapter","rawErrorSuppressed":true,"reconciliationMayReadByOperationIdLater":true,"reconciliationMayWriteAllowed":false,"reconciliationRequired":true,"requiredCapability":"atomic_compare_and_set_with_consumption_record","singleAdapterInvocationRequired":true,"statementTimeoutMilliseconds":5000},"futureBoundary":{"adapterFactoryImplemented":false,"adapterImported":false,"adapterInstantiated":false,"adapterInterfaceImplemented":false,"adapterInvoked":false,"adapterModuleCreated":false,"atomicConsumptionExecuted":false,"databaseTestExecuted":false,"directAppExecutionGrant":false,"executionDescriptorAcceptanceGuardImplemented":false,"executionDescriptorImplemented":false,"frontendIntegration":false,"registryAccessPerformed":false},"implementationBoundary":{"adapterFactoryImplemented":false,"adapterImported":false,"adapterInstantiated":false,"adapterInterfaceImplemented":false,"adapterInvoked":false,"adapterModuleCreated":false,"atomicCompareAndSetPerformed":false,"authorizationConsumed":false,"authorizationGranted":false,"authorizationTokenGenerated":false,"databaseConnectionCreated":false,"databaseTestExecuted":false,"driverImported":false,"executionDescriptorImplemented":false,"executionGrant":false,"filesystemMutationPerformed":false,"filesystemReadPerformed":false,"frontendIntegration":false,"implementationExecutionContractPrepared":true,"networkExecuted":false,"processExecuted":false,"registryReadPerformed":false,"registryWritePerformed":false,"sqlMigrationCreated":false,"trustedClockRead":false},"productiveReleaseAllowed":false,"securityBoundary":{"adapterImplementationAllowed":false,"adapterImportAllowed":false,"adapterInstantiationAllowed":false,"adapterInvocationAllowed":false,"atomicCompareAndSetAllowed":false,"authorizationConsumptionAllowed":false,"authorizationGrantAllowed":false,"authorizationTokenAllowed":false,"connectionStringAllowed":false,"databaseConnectionAllowed":false,"databaseUrlAllowed":false,"directAppExecutionGrantAllowed":false,"driverImportAllowed":false,"filesystemMutationAllowed":false,"filesystemReadAllowed":false,"frontendReferenceAllowed":false,"networkExecutionAllowed":false,"passwordAllowed":false,"processEnvironmentReadAllowed":false,"processExecutionAllowed":false,"productionSecretAllowed":false,"realParticipantDataAllowed":false,"reconciliationReadAllowed":false,"registryReadAllowed":false,"registryWriteAllowed":false,"serviceRoleKeyAllowed":false,"trustedClockReadAllowed":false},"sourceBoundary":{"allSourceSecurityFlagsMustBeFalse":true,"exactCanonicalAcceptedPlanRequired":true,"requiredAccepted":true,"requiredAcceptedReason":"authorization_atomic_consumption_registry_adapter_implementation_plan_accepted_execution_locked","requiredAcceptedStatus":"accepted_atomic_consumption_registry_adapter_implementation_plan_execution_locked","requiredExecutionGrant":false,"requiredPlanVersion":1,"requiredSourceStatus":"implemented_pure_atomic_consumption_registry_adapter_implementation_plan_acceptance_execution_locked","requiredSourceVersion":"v27.33m","requiredStepCount":10},"status":"planned_atomic_consumption_registry_adapter_implementation_execution_fully_locked_not_implemented","version":"v27.33n"},"descriptorVersion":1,"executionGrant":false,"sourceContractStatus":"planned_atomic_consumption_registry_adapter_implementation_execution_fully_locked_not_implemented","sourceContractVersion":"v27.33n"},"adapterImplementationAllowed":false,"adapterImportAllowed":false,"adapterInstantiationAllowed":false,"adapterInvocationAllowed":false,"atomicCompareAndSetAllowed":false,"authorizationConsumptionAllowed":false,"executionCapabilityFacts":{"adapterFactoryImplemented":false,"adapterImported":false,"adapterInstantiated":false,"adapterInterfaceImplemented":false,"adapterInvoked":false,"adapterKind":"single_use_consumption_registry","adapterModuleCreated":false,"assumeCommittedAllowed":false,"assumeUnusedAllowed":false,"automaticRetryAfterAmbiguousAllowed":false,"compareAndSetAndConsumptionRecordSingleTransactionRequired":true,"connectTimeoutMilliseconds":3000,"consumptionRecordRequiredOnCommitted":true,"databaseConnectionAllowed":false,"dependencyInjectionRequired":true,"desiredState":"consumed","driverImportAllowed":false,"environmentVariableReadAllowed":false,"evidenceDerivedOnlyFromConfirmedRecord":true,"exactInputFields":["operationId","requestId","authorizationNonce","planFingerprint","actorId","purpose","expectedState","desiredState","consumptionRecord","evidenceTemplate"],"exactResultKinds":["committed","already_consumed","parallel_conflict","binding_conflict","expired","adapter_unavailable","atomicity_unavailable","commit_ambiguous","operation_failed"],"executionGrant":false,"expectedState":"unused","factoryName":"build_atomic_consumption_registry_adapter","hardCodedCredentialsAllowed":false,"lockTimeoutMilliseconds":2000,"maximumParallelWinners":1,"operationName":"consume_materialization_authorization_atomically","operationTimeoutMilliseconds":15000,"plannedModulePath":"tools/accaoui_disposable_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter.py","protocolName":"AtomicConsumptionRegistryAdapter","rawErrorSuppressed":true,"reconciliationMayReadByOperationIdLater":true,"reconciliationMayWriteAllowed":false,"reconciliationRequired":true,"requiredCapability":"atomic_compare_and_set_with_consumption_record","resetConsumedToUnusedAllowed":false,"singleAdapterInvocationRequired":true,"singleTransactionRequired":true,"statementTimeoutMilliseconds":5000},"executionGrant":false,"readinessVersion":1,"reconciliationReadAllowed":false,"registryReadAllowed":false,"registryWriteAllowed":false,"sourceReason":"authorization_atomic_consumption_registry_adapter_implementation_execution_descriptor_accepted_execution_locked","sourceStatus":"accepted_atomic_consumption_registry_adapter_implementation_execution_descriptor_execution_locked"}'
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

INPUT_KEYS = frozenset({
    "acceptedExecutionReadinessResult",
    "executionPlanFacts",
})

SOURCE_KEYS = frozenset({
    "status",
    "reason",
    "accepted",
    "acceptedReadiness",
    *LOCKED_FLAGS,
})

IMPLEMENTATION_SEQUENCE = [
    "validate_accepted_readiness_boundary",
    "validate_dependency_injection_boundary",
    "prepare_protocol_and_result_types",
    "prepare_factory_without_default_credentials",
    "prepare_single_transaction_boundary",
    "prepare_atomic_compare_and_set_with_consumption_record",
    "prepare_exact_result_mapping",
    "prepare_timeout_configuration",
    "prepare_commit_ambiguity_terminal_handling",
    "prepare_operation_id_reconciliation",
    "prepare_pure_adapter_unit_fixtures",
    "keep_adapter_unimplemented_uninstantiated_and_uninvoked",
]

EXPECTED_EXECUTION_PLAN_FACTS = {
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
    "implementationSequence": IMPLEMENTATION_SEQUENCE,
    "singleAdapterInvocationRequired": True,
    "singleTransactionRequired": True,
    "compareAndSetAndConsumptionRecordSingleTransactionRequired": True,
    "consumptionRecordRequiredOnCommitted": True,
    "evidenceDerivedOnlyFromConfirmedRecord": True,
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
    "reconciliationMayReadByOperationIdLater": True,
    "reconciliationMayWriteAllowed": False,
    "resetConsumedToUnusedAllowed": False,
    "assumeCommittedAllowed": False,
    "assumeUnusedAllowed": False,
    "adapterModuleCreated": False,
    "adapterInterfaceImplemented": False,
    "adapterFactoryImplemented": False,
    "adapterImported": False,
    "adapterInstantiated": False,
    "adapterInvoked": False,
    "executionGrant": False,
}

SUCCESS_STATUS = (
    "atomic_consumption_registry_adapter_implementation_execution_"
    "plan_ready_execution_locked"
)
SUCCESS_REASON = (
    "authorization_atomic_consumption_registry_adapter_"
    "implementation_execution_plan_ready_execution_locked"
)
BLOCKED_STATUS = (
    "atomic_consumption_registry_adapter_implementation_execution_"
    "plan_blocked_execution_locked"
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


def resolve_atomic_consumption_registry_adapter_implementation_execution_plan(
    value: object,
) -> dict[str, object]:
    if not isinstance(value, Mapping):
        return blocked("implementation_execution_plan_invalid_input")

    source = dict(value)
    if set(source) != INPUT_KEYS:
        return blocked("implementation_execution_plan_structure_invalid")

    accepted = source["acceptedExecutionReadinessResult"]
    if not isinstance(accepted, Mapping):
        return blocked("implementation_execution_plan_source_invalid")

    accepted_data = dict(accepted)
    if set(accepted_data) != SOURCE_KEYS:
        return blocked(
            "implementation_execution_plan_source_structure_invalid"
        )
    if accepted_data["status"] != (
        "accepted_atomic_consumption_registry_adapter_implementation_"
        "execution_readiness_execution_locked"
    ):
        return blocked(
            "implementation_execution_plan_source_status_invalid"
        )
    if accepted_data["reason"] != (
        "authorization_atomic_consumption_registry_adapter_"
        "implementation_execution_readiness_accepted_execution_locked"
    ):
        return blocked(
            "implementation_execution_plan_source_reason_invalid"
        )
    if accepted_data["accepted"] is not True:
        return blocked(
            "implementation_execution_plan_source_acceptance_invalid"
        )

    for key in LOCKED_FLAGS:
        if accepted_data[key] is not False:
            return blocked(
                "implementation_execution_plan_source_boundary_open"
            )

    accepted_readiness = accepted_data["acceptedReadiness"]
    if type(accepted_readiness) is not dict:
        return blocked(
            "implementation_execution_plan_readiness_invalid"
        )
    if accepted_readiness != EXPECTED_ACCEPTED_READINESS:
        return blocked(
            "implementation_execution_plan_readiness_invalid"
        )

    facts = source["executionPlanFacts"]
    if not isinstance(facts, Mapping):
        return blocked(
            "implementation_execution_plan_facts_invalid"
        )
    if dict(facts) != EXPECTED_EXECUTION_PLAN_FACTS:
        return blocked(
            "implementation_execution_plan_facts_invalid"
        )

    plan = {
        "planVersion": 1,
        "sourceStatus": accepted_data["status"],
        "sourceReason": accepted_data["reason"],
        "acceptedReadiness": copy.deepcopy(accepted_readiness),
        "executionPlanFacts": copy.deepcopy(
            EXPECTED_EXECUTION_PLAN_FACTS
        ),
        "implementationSequence": copy.deepcopy(
            IMPLEMENTATION_SEQUENCE
        ),
        "adapterImplementationAllowed": False,
        "adapterImportAllowed": False,
        "adapterInstantiationAllowed": False,
        "adapterInvocationAllowed": False,
        "registryReadAllowed": False,
        "registryWriteAllowed": False,
        "atomicCompareAndSetAllowed": False,
        "authorizationConsumptionAllowed": False,
        "reconciliationReadAllowed": False,
        "executionGrant": False,
    }

    return {
        "status": SUCCESS_STATUS,
        "reason": SUCCESS_REASON,
        "ready": True,
        "plan": plan,
        **locked_flags(),
    }
