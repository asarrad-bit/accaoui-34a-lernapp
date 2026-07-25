from __future__ import annotations

import copy
import json
from collections.abc import Mapping

_EXPECTED_CONTRACT_FACTS = json.loads('{"ambiguityBoundary":{"assumeCommittedAllowed":false,"assumeUnusedAllowed":false,"automaticRetryAfterAmbiguousAllowed":false,"commitAmbiguousTerminalForAutomaticRetry":true,"reconciliationMayReadByOperationIdLater":true,"reconciliationMayWriteAllowed":false,"reconciliationRequired":true},"atomicityBoundary":{"alreadyConsumedIsTerminal":true,"bindingConflictIsTerminal":true,"compareAndSetAndConsumptionRecordSingleTransactionRequired":true,"consumptionRecordRequiredOnCommitted":true,"evidenceDerivedOnlyFromConfirmedRecord":true,"expiredIsTerminal":true,"parallelWinnerCountMaximum":1,"resetConsumedToUnusedAllowed":false},"contractVersion":1,"dependencyBoundary":{"connectionStringAllowed":false,"databaseConnectionAllowed":false,"databaseUrlAllowed":false,"dependencyInjectionRequired":true,"driverImportAllowed":false,"environmentVariableReadAllowed":false,"hardCodedCredentialsAllowed":false,"productionSecretAllowed":false,"realParticipantDataAllowed":false,"serviceRoleKeyAllowed":false},"implementationBoundary":{"adapterFactoryImplemented":false,"adapterImported":false,"adapterInstantiated":false,"adapterInterfaceImplemented":false,"adapterInvoked":false,"adapterModuleCreated":false,"atomicCompareAndSetPerformed":false,"authorizationConsumed":false,"authorizationGranted":false,"authorizationTokenGenerated":false,"databaseConnectionCreated":false,"databaseTestExecuted":false,"driverImported":false,"executionGrant":false,"filesystemMutationPerformed":false,"filesystemReadPerformed":false,"frontendIntegration":false,"implementationContractPrepared":true,"networkExecuted":false,"processExecuted":false,"registryReadPerformed":false,"registryWritePerformed":false,"sqlMigrationCreated":false,"trustedClockRead":false},"interfaceBoundary":{"adapterKind":"single_use_consumption_registry","connectTimeoutMilliseconds":3000,"desiredState":"consumed","exactInputFields":["operationId","requestId","authorizationNonce","planFingerprint","actorId","purpose","expectedState","desiredState","consumptionRecord","evidenceTemplate"],"exactResultKinds":["committed","already_consumed","parallel_conflict","binding_conflict","expired","adapter_unavailable","atomicity_unavailable","commit_ambiguous","operation_failed"],"executionGrant":false,"expectedState":"unused","factoryName":"build_atomic_consumption_registry_adapter","interfaceVersion":1,"lockTimeoutMilliseconds":2000,"maximumParallelWinners":1,"operationName":"consume_materialization_authorization_atomically","operationTimeoutMilliseconds":15000,"plannedModulePath":"tools/accaoui_disposable_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter.py","protocolName":"AtomicConsumptionRegistryAdapter","rawErrorSuppressed":true,"requiredCapability":"atomic_compare_and_set_with_consumption_record","singleAdapterInvocationRequired":true,"statementTimeoutMilliseconds":5000},"productiveReleaseAllowed":false,"securityBoundary":{"adapterImplementationAllowed":false,"adapterImportAllowed":false,"adapterInstantiationAllowed":false,"adapterInvocationAllowed":false,"atomicCompareAndSetAllowed":false,"authorizationConsumptionAllowed":false,"authorizationGrantAllowed":false,"authorizationTokenAllowed":false,"connectionStringAllowed":false,"databaseConnectionAllowed":false,"databaseUrlAllowed":false,"directAppExecutionGrantAllowed":false,"driverImportAllowed":false,"filesystemMutationAllowed":false,"filesystemReadAllowed":false,"frontendReferenceAllowed":false,"networkExecutionAllowed":false,"passwordAllowed":false,"processEnvironmentReadAllowed":false,"processExecutionAllowed":false,"productionSecretAllowed":false,"realParticipantDataAllowed":false,"reconciliationReadAllowed":false,"registryReadAllowed":false,"registryWriteAllowed":false,"serviceRoleKeyAllowed":false,"trustedClockReadAllowed":false},"sourceBoundary":{"allSourceSecurityFlagsMustBeFalse":true,"requiredAccepted":true,"requiredAcceptedReason":"authorization_atomic_consumption_registry_adapter_execution_plan_accepted_execution_locked","requiredAcceptedStatus":"accepted_atomic_consumption_registry_adapter_execution_plan_execution_locked","requiredExecutionGrant":false,"requiredSourceStatus":"implemented_pure_atomic_consumption_registry_adapter_execution_plan_acceptance_execution_locked","requiredSourceVersion":"v27.33f"},"status":"planned_atomic_consumption_registry_adapter_implementation_fully_locked_not_implemented","unresolvedRequirements":{"databaseTestExecution":true,"directAppExecutionGrant":true,"environmentEvidenceCollector":true,"environmentMaterializer":true,"environmentRollbackImplementation":true,"frontendIntegration":true,"materializationAuthorizationConsumptionReceipt":true,"registryAdapterExecution":true,"registryAdapterImplementation":true,"registryAdapterImplementationDescriptor":true,"registryAdapterInstantiation":true,"registryAdapterReconciliation":true},"version":"v27.33g"}')
_LOCKED_FLAGS = (
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
_SOURCE_KEYS = frozenset({
    "status",
    "reason",
    "ready",
    "descriptor",
    *_LOCKED_FLAGS,
})
_DESCRIPTOR_KEYS = frozenset({
    "descriptorVersion",
    "sourceContractVersion",
    "sourceContractStatus",
    "contractFacts",
    "executionGrant",
})

_SUCCESS_SOURCE_STATUS = (
    "atomic_consumption_registry_adapter_implementation_descriptor_"
    "ready_execution_locked"
)
_SUCCESS_SOURCE_REASON = (
    "authorization_atomic_consumption_registry_adapter_"
    "implementation_descriptor_ready_execution_locked"
)
_ACCEPTED_STATUS = (
    "accepted_atomic_consumption_registry_adapter_implementation_"
    "descriptor_execution_locked"
)
_ACCEPTED_REASON = (
    "authorization_atomic_consumption_registry_adapter_"
    "implementation_descriptor_accepted_execution_locked"
)
_BLOCKED_STATUS = (
    "atomic_consumption_registry_adapter_implementation_descriptor_"
    "acceptance_blocked_execution_locked"
)


def _locked_flags() -> dict[str, bool]:
    return {key: False for key in _LOCKED_FLAGS}


def _blocked(reason: str) -> dict[str, object]:
    return {
        "status": _BLOCKED_STATUS,
        "reason": reason,
        "accepted": False,
        "acceptedDescriptor": None,
        **_locked_flags(),
    }


def accept_atomic_consumption_registry_adapter_implementation_descriptor(
    candidate: object,
) -> dict[str, object]:
    """Accept only the exact locked v27.33h implementation descriptor."""
    if not isinstance(candidate, Mapping):
        return _blocked(
            "authorization_atomic_consumption_registry_adapter_"
            "implementation_descriptor_acceptance_invalid_input"
        )

    source = dict(candidate)
    if set(source) != _SOURCE_KEYS:
        return _blocked(
            "authorization_atomic_consumption_registry_adapter_"
            "implementation_descriptor_acceptance_structure_invalid"
        )
    if source["status"] != _SUCCESS_SOURCE_STATUS:
        return _blocked(
            "authorization_atomic_consumption_registry_adapter_"
            "implementation_descriptor_acceptance_source_status_invalid"
        )
    if source["reason"] != _SUCCESS_SOURCE_REASON:
        return _blocked(
            "authorization_atomic_consumption_registry_adapter_"
            "implementation_descriptor_acceptance_source_reason_invalid"
        )
    if source["ready"] is not True:
        return _blocked(
            "authorization_atomic_consumption_registry_adapter_"
            "implementation_descriptor_acceptance_source_ready_invalid"
        )

    for key in _LOCKED_FLAGS:
        if source[key] is not False:
            return _blocked(
                "authorization_atomic_consumption_registry_adapter_"
                "implementation_descriptor_acceptance_source_boundary_open"
            )

    descriptor = source["descriptor"]
    if not isinstance(descriptor, Mapping):
        return _blocked(
            "authorization_atomic_consumption_registry_adapter_"
            "implementation_descriptor_acceptance_descriptor_invalid"
        )

    data = dict(descriptor)
    if set(data) != _DESCRIPTOR_KEYS:
        return _blocked(
            "authorization_atomic_consumption_registry_adapter_"
            "implementation_descriptor_acceptance_descriptor_structure_invalid"
        )
    if data["descriptorVersion"] != 1:
        return _blocked(
            "authorization_atomic_consumption_registry_adapter_"
            "implementation_descriptor_acceptance_descriptor_version_invalid"
        )
    if data["sourceContractVersion"] != "v27.33g":
        return _blocked(
            "authorization_atomic_consumption_registry_adapter_"
            "implementation_descriptor_acceptance_source_version_invalid"
        )
    if data["sourceContractStatus"] != (
        "planned_atomic_consumption_registry_adapter_implementation_"
        "fully_locked_not_implemented"
    ):
        return _blocked(
            "authorization_atomic_consumption_registry_adapter_"
            "implementation_descriptor_acceptance_source_contract_invalid"
        )
    if type(data["contractFacts"]) is not dict or (
        data["contractFacts"] != _EXPECTED_CONTRACT_FACTS
    ):
        return _blocked(
            "authorization_atomic_consumption_registry_adapter_"
            "implementation_descriptor_acceptance_contract_facts_invalid"
        )
    if data["executionGrant"] is not False:
        return _blocked(
            "authorization_atomic_consumption_registry_adapter_"
            "implementation_descriptor_acceptance_descriptor_boundary_open"
        )

    return {
        "status": _ACCEPTED_STATUS,
        "reason": _ACCEPTED_REASON,
        "accepted": True,
        "acceptedDescriptor": copy.deepcopy(data),
        **_locked_flags(),
    }
