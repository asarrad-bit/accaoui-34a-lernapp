from __future__ import annotations

import copy
import json
from collections.abc import Mapping

EXPECTED_READINESS = json.loads(
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

SOURCE_KEYS = frozenset({
    "status",
    "reason",
    "ready",
    "readiness",
    *LOCKED_FLAGS,
})

SOURCE_STATUS = (
    "atomic_consumption_registry_adapter_implementation_execution_"
    "readiness_ready_execution_locked"
)
SOURCE_REASON = (
    "authorization_atomic_consumption_registry_adapter_"
    "implementation_execution_readiness_ready_execution_locked"
)
ACCEPTED_STATUS = (
    "accepted_atomic_consumption_registry_adapter_implementation_"
    "execution_readiness_execution_locked"
)
ACCEPTED_REASON = (
    "authorization_atomic_consumption_registry_adapter_"
    "implementation_execution_readiness_accepted_execution_locked"
)
BLOCKED_STATUS = (
    "atomic_consumption_registry_adapter_implementation_execution_"
    "readiness_acceptance_blocked_execution_locked"
)


def locked_flags() -> dict[str, bool]:
    return {key: False for key in LOCKED_FLAGS}


def blocked(reason: str) -> dict[str, object]:
    return {
        "status": BLOCKED_STATUS,
        "reason": reason,
        "accepted": False,
        "acceptedReadiness": None,
        **locked_flags(),
    }


def accept_atomic_consumption_registry_adapter_implementation_execution_readiness(
    candidate: object,
) -> dict[str, object]:
    if not isinstance(candidate, Mapping):
        return blocked(
            "implementation_execution_readiness_acceptance_invalid_input"
        )

    source = dict(candidate)
    if set(source) != SOURCE_KEYS:
        return blocked(
            "implementation_execution_readiness_acceptance_"
            "structure_invalid"
        )
    if source["status"] != SOURCE_STATUS:
        return blocked(
            "implementation_execution_readiness_acceptance_status_invalid"
        )
    if source["reason"] != SOURCE_REASON:
        return blocked(
            "implementation_execution_readiness_acceptance_reason_invalid"
        )
    if source["ready"] is not True:
        return blocked(
            "implementation_execution_readiness_acceptance_ready_invalid"
        )

    for key in LOCKED_FLAGS:
        if source[key] is not False:
            return blocked(
                "implementation_execution_readiness_acceptance_"
                "source_boundary_open"
            )

    readiness = source["readiness"]
    if type(readiness) is not dict:
        return blocked(
            "implementation_execution_readiness_acceptance_"
            "readiness_invalid"
        )
    if readiness != EXPECTED_READINESS:
        return blocked(
            "implementation_execution_readiness_acceptance_"
            "readiness_invalid"
        )

    return {
        "status": ACCEPTED_STATUS,
        "reason": ACCEPTED_REASON,
        "accepted": True,
        "acceptedReadiness": copy.deepcopy(readiness),
        **locked_flags(),
    }
