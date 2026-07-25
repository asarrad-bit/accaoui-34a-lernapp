from __future__ import annotations

import copy
import json
from collections.abc import Mapping

EXPECTED_CONTRACT_FACTS = json.loads(
    '{"atomicityBoundary":{"alreadyConsumedIsTerminal":true,"assumeCommittedAllowed":false,"assumeUnusedAllowed":false,"bindingConflictIsTerminal":true,"commitAmbiguousTerminalForAutomaticRetry":true,"compareAndSetAndConsumptionRecordSingleTransactionRequired":true,"consumptionRecordRequiredOnCommitted":true,"evidenceDerivedOnlyFromConfirmedRecord":true,"expiredIsTerminal":true,"maximumParallelWinners":1,"resetConsumedToUnusedAllowed":false,"singleTransactionRequired":true},"contractVersion":1,"executionInterfaceBoundary":{"adapterKind":"single_use_consumption_registry","automaticRetryAfterAmbiguousAllowed":false,"connectTimeoutMilliseconds":3000,"databaseConnectionAllowed":false,"dependencyInjectionRequired":true,"desiredState":"consumed","driverImportAllowed":false,"environmentVariableReadAllowed":false,"exactInputFields":["operationId","requestId","authorizationNonce","planFingerprint","actorId","purpose","expectedState","desiredState","consumptionRecord","evidenceTemplate"],"exactResultKinds":["committed","already_consumed","parallel_conflict","binding_conflict","expired","adapter_unavailable","atomicity_unavailable","commit_ambiguous","operation_failed"],"executionGrant":false,"expectedState":"unused","factoryName":"build_atomic_consumption_registry_adapter","hardCodedCredentialsAllowed":false,"lockTimeoutMilliseconds":2000,"maximumParallelWinners":1,"operationName":"consume_materialization_authorization_atomically","operationTimeoutMilliseconds":15000,"plannedModulePath":"tools/accaoui_disposable_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter.py","protocolName":"AtomicConsumptionRegistryAdapter","rawErrorSuppressed":true,"reconciliationMayReadByOperationIdLater":true,"reconciliationMayWriteAllowed":false,"reconciliationRequired":true,"requiredCapability":"atomic_compare_and_set_with_consumption_record","singleAdapterInvocationRequired":true,"statementTimeoutMilliseconds":5000},"futureBoundary":{"adapterFactoryImplemented":false,"adapterImported":false,"adapterInstantiated":false,"adapterInterfaceImplemented":false,"adapterInvoked":false,"adapterModuleCreated":false,"atomicConsumptionExecuted":false,"databaseTestExecuted":false,"directAppExecutionGrant":false,"executionDescriptorAcceptanceGuardImplemented":false,"executionDescriptorImplemented":false,"frontendIntegration":false,"registryAccessPerformed":false},"implementationBoundary":{"adapterFactoryImplemented":false,"adapterImported":false,"adapterInstantiated":false,"adapterInterfaceImplemented":false,"adapterInvoked":false,"adapterModuleCreated":false,"atomicCompareAndSetPerformed":false,"authorizationConsumed":false,"authorizationGranted":false,"authorizationTokenGenerated":false,"databaseConnectionCreated":false,"databaseTestExecuted":false,"driverImported":false,"executionDescriptorImplemented":false,"executionGrant":false,"filesystemMutationPerformed":false,"filesystemReadPerformed":false,"frontendIntegration":false,"implementationExecutionContractPrepared":true,"networkExecuted":false,"processExecuted":false,"registryReadPerformed":false,"registryWritePerformed":false,"sqlMigrationCreated":false,"trustedClockRead":false},"productiveReleaseAllowed":false,"securityBoundary":{"adapterImplementationAllowed":false,"adapterImportAllowed":false,"adapterInstantiationAllowed":false,"adapterInvocationAllowed":false,"atomicCompareAndSetAllowed":false,"authorizationConsumptionAllowed":false,"authorizationGrantAllowed":false,"authorizationTokenAllowed":false,"connectionStringAllowed":false,"databaseConnectionAllowed":false,"databaseUrlAllowed":false,"directAppExecutionGrantAllowed":false,"driverImportAllowed":false,"filesystemMutationAllowed":false,"filesystemReadAllowed":false,"frontendReferenceAllowed":false,"networkExecutionAllowed":false,"passwordAllowed":false,"processEnvironmentReadAllowed":false,"processExecutionAllowed":false,"productionSecretAllowed":false,"realParticipantDataAllowed":false,"reconciliationReadAllowed":false,"registryReadAllowed":false,"registryWriteAllowed":false,"serviceRoleKeyAllowed":false,"trustedClockReadAllowed":false},"sourceBoundary":{"allSourceSecurityFlagsMustBeFalse":true,"exactCanonicalAcceptedPlanRequired":true,"requiredAccepted":true,"requiredAcceptedReason":"authorization_atomic_consumption_registry_adapter_implementation_plan_accepted_execution_locked","requiredAcceptedStatus":"accepted_atomic_consumption_registry_adapter_implementation_plan_execution_locked","requiredExecutionGrant":false,"requiredPlanVersion":1,"requiredSourceStatus":"implemented_pure_atomic_consumption_registry_adapter_implementation_plan_acceptance_execution_locked","requiredSourceVersion":"v27.33m","requiredStepCount":10},"status":"planned_atomic_consumption_registry_adapter_implementation_execution_fully_locked_not_implemented","version":"v27.33n"}'
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
    "descriptor",
    *LOCKED_FLAGS,
})

DESCRIPTOR_KEYS = frozenset({
    "descriptorVersion",
    "sourceContractVersion",
    "sourceContractStatus",
    "contractFacts",
    "executionGrant",
})

SOURCE_STATUS = (
    "atomic_consumption_registry_adapter_implementation_execution_"
    "descriptor_ready_execution_locked"
)
SOURCE_REASON = (
    "authorization_atomic_consumption_registry_adapter_"
    "implementation_execution_descriptor_ready_execution_locked"
)
ACCEPTED_STATUS = (
    "accepted_atomic_consumption_registry_adapter_implementation_"
    "execution_descriptor_execution_locked"
)
ACCEPTED_REASON = (
    "authorization_atomic_consumption_registry_adapter_"
    "implementation_execution_descriptor_accepted_execution_locked"
)
BLOCKED_STATUS = (
    "atomic_consumption_registry_adapter_implementation_execution_"
    "descriptor_acceptance_blocked_execution_locked"
)


def locked_flags() -> dict[str, bool]:
    return {key: False for key in LOCKED_FLAGS}


def blocked(reason: str) -> dict[str, object]:
    return {
        "status": BLOCKED_STATUS,
        "reason": reason,
        "accepted": False,
        "acceptedDescriptor": None,
        **locked_flags(),
    }


def accept_atomic_consumption_registry_adapter_implementation_execution_descriptor(
    candidate: object,
) -> dict[str, object]:
    if not isinstance(candidate, Mapping):
        return blocked(
            "implementation_execution_descriptor_acceptance_invalid_input"
        )

    source = dict(candidate)
    if set(source) != SOURCE_KEYS:
        return blocked(
            "implementation_execution_descriptor_acceptance_structure_invalid"
        )
    if source["status"] != SOURCE_STATUS:
        return blocked(
            "implementation_execution_descriptor_acceptance_status_invalid"
        )
    if source["reason"] != SOURCE_REASON:
        return blocked(
            "implementation_execution_descriptor_acceptance_reason_invalid"
        )
    if source["ready"] is not True:
        return blocked(
            "implementation_execution_descriptor_acceptance_ready_invalid"
        )

    for key in LOCKED_FLAGS:
        if source[key] is not False:
            return blocked(
                "implementation_execution_descriptor_acceptance_"
                "source_boundary_open"
            )

    descriptor = source["descriptor"]
    if not isinstance(descriptor, Mapping):
        return blocked(
            "implementation_execution_descriptor_acceptance_"
            "descriptor_invalid"
        )

    data = dict(descriptor)
    if set(data) != DESCRIPTOR_KEYS:
        return blocked(
            "implementation_execution_descriptor_acceptance_"
            "descriptor_structure_invalid"
        )
    if data["descriptorVersion"] != 1:
        return blocked(
            "implementation_execution_descriptor_acceptance_"
            "descriptor_version_invalid"
        )
    if data["sourceContractVersion"] != "v27.33n":
        return blocked(
            "implementation_execution_descriptor_acceptance_"
            "source_version_invalid"
        )
    if data["sourceContractStatus"] != (
        "planned_atomic_consumption_registry_adapter_"
        "implementation_execution_fully_locked_not_implemented"
    ):
        return blocked(
            "implementation_execution_descriptor_acceptance_"
            "source_status_invalid"
        )
    if type(data["contractFacts"]) is not dict:
        return blocked(
            "implementation_execution_descriptor_acceptance_"
            "contract_facts_invalid"
        )
    if data["contractFacts"] != EXPECTED_CONTRACT_FACTS:
        return blocked(
            "implementation_execution_descriptor_acceptance_"
            "contract_facts_invalid"
        )
    if data["executionGrant"] is not False:
        return blocked(
            "implementation_execution_descriptor_acceptance_"
            "descriptor_boundary_open"
        )

    return {
        "status": ACCEPTED_STATUS,
        "reason": ACCEPTED_REASON,
        "accepted": True,
        "acceptedDescriptor": copy.deepcopy(data),
        **locked_flags(),
    }
