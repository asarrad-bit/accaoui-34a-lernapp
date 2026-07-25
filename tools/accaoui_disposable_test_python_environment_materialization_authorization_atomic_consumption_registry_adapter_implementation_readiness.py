from __future__ import annotations

import copy
import json
from collections.abc import Mapping

_EXPECTED_IMPLEMENTATION_CONTRACT = json.loads('{"ambiguityBoundary":{"assumeCommittedAllowed":false,"assumeUnusedAllowed":false,"automaticRetryAfterAmbiguousAllowed":false,"commitAmbiguousTerminalForAutomaticRetry":true,"reconciliationMayReadByOperationIdLater":true,"reconciliationMayWriteAllowed":false,"reconciliationRequired":true},"atomicityBoundary":{"alreadyConsumedIsTerminal":true,"bindingConflictIsTerminal":true,"compareAndSetAndConsumptionRecordSingleTransactionRequired":true,"consumptionRecordRequiredOnCommitted":true,"evidenceDerivedOnlyFromConfirmedRecord":true,"expiredIsTerminal":true,"parallelWinnerCountMaximum":1,"resetConsumedToUnusedAllowed":false},"contractVersion":1,"dependencyBoundary":{"connectionStringAllowed":false,"databaseConnectionAllowed":false,"databaseUrlAllowed":false,"dependencyInjectionRequired":true,"driverImportAllowed":false,"environmentVariableReadAllowed":false,"hardCodedCredentialsAllowed":false,"productionSecretAllowed":false,"realParticipantDataAllowed":false,"serviceRoleKeyAllowed":false},"implementationBoundary":{"adapterFactoryImplemented":false,"adapterImported":false,"adapterInstantiated":false,"adapterInterfaceImplemented":false,"adapterInvoked":false,"adapterModuleCreated":false,"atomicCompareAndSetPerformed":false,"authorizationConsumed":false,"authorizationGranted":false,"authorizationTokenGenerated":false,"databaseConnectionCreated":false,"databaseTestExecuted":false,"driverImported":false,"executionGrant":false,"filesystemMutationPerformed":false,"filesystemReadPerformed":false,"frontendIntegration":false,"implementationContractPrepared":true,"networkExecuted":false,"processExecuted":false,"registryReadPerformed":false,"registryWritePerformed":false,"sqlMigrationCreated":false,"trustedClockRead":false},"interfaceBoundary":{"adapterKind":"single_use_consumption_registry","connectTimeoutMilliseconds":3000,"desiredState":"consumed","exactInputFields":["operationId","requestId","authorizationNonce","planFingerprint","actorId","purpose","expectedState","desiredState","consumptionRecord","evidenceTemplate"],"exactResultKinds":["committed","already_consumed","parallel_conflict","binding_conflict","expired","adapter_unavailable","atomicity_unavailable","commit_ambiguous","operation_failed"],"executionGrant":false,"expectedState":"unused","factoryName":"build_atomic_consumption_registry_adapter","interfaceVersion":1,"lockTimeoutMilliseconds":2000,"maximumParallelWinners":1,"operationName":"consume_materialization_authorization_atomically","operationTimeoutMilliseconds":15000,"plannedModulePath":"tools/accaoui_disposable_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter.py","protocolName":"AtomicConsumptionRegistryAdapter","rawErrorSuppressed":true,"requiredCapability":"atomic_compare_and_set_with_consumption_record","singleAdapterInvocationRequired":true,"statementTimeoutMilliseconds":5000},"productiveReleaseAllowed":false,"securityBoundary":{"adapterImplementationAllowed":false,"adapterImportAllowed":false,"adapterInstantiationAllowed":false,"adapterInvocationAllowed":false,"atomicCompareAndSetAllowed":false,"authorizationConsumptionAllowed":false,"authorizationGrantAllowed":false,"authorizationTokenAllowed":false,"connectionStringAllowed":false,"databaseConnectionAllowed":false,"databaseUrlAllowed":false,"directAppExecutionGrantAllowed":false,"driverImportAllowed":false,"filesystemMutationAllowed":false,"filesystemReadAllowed":false,"frontendReferenceAllowed":false,"networkExecutionAllowed":false,"passwordAllowed":false,"processEnvironmentReadAllowed":false,"processExecutionAllowed":false,"productionSecretAllowed":false,"realParticipantDataAllowed":false,"reconciliationReadAllowed":false,"registryReadAllowed":false,"registryWriteAllowed":false,"serviceRoleKeyAllowed":false,"trustedClockReadAllowed":false},"sourceBoundary":{"allSourceSecurityFlagsMustBeFalse":true,"requiredAccepted":true,"requiredAcceptedReason":"authorization_atomic_consumption_registry_adapter_execution_plan_accepted_execution_locked","requiredAcceptedStatus":"accepted_atomic_consumption_registry_adapter_execution_plan_execution_locked","requiredExecutionGrant":false,"requiredSourceStatus":"implemented_pure_atomic_consumption_registry_adapter_execution_plan_acceptance_execution_locked","requiredSourceVersion":"v27.33f"},"status":"planned_atomic_consumption_registry_adapter_implementation_fully_locked_not_implemented","unresolvedRequirements":{"databaseTestExecution":true,"directAppExecutionGrant":true,"environmentEvidenceCollector":true,"environmentMaterializer":true,"environmentRollbackImplementation":true,"frontendIntegration":true,"materializationAuthorizationConsumptionReceipt":true,"registryAdapterExecution":true,"registryAdapterImplementation":true,"registryAdapterImplementationDescriptor":true,"registryAdapterInstantiation":true,"registryAdapterReconciliation":true},"version":"v27.33g"}')

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

_INPUT_KEYS = frozenset({
    "acceptedImplementationDescriptorResult",
    "implementationFacts",
})
_SOURCE_KEYS = frozenset({
    "status",
    "reason",
    "accepted",
    "acceptedDescriptor",
    *_LOCKED_FLAGS,
})
_DESCRIPTOR_KEYS = frozenset({
    "descriptorVersion",
    "sourceContractVersion",
    "sourceContractStatus",
    "contractFacts",
    "executionGrant",
})

_EXPECTED_IMPLEMENTATION_FACTS = {
    "adapterKind": "single_use_consumption_registry",
    "plannedModulePath": (
        "tools/accaoui_disposable_test_python_environment_"
        "materialization_authorization_atomic_consumption_"
        "registry_adapter.py"
    ),
    "interfaceVersion": 1,
    "protocolName": "AtomicConsumptionRegistryAdapter",
    "factoryName": "build_atomic_consumption_registry_adapter",
    "operationName": "consume_materialization_authorization_atomically",
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

_SUCCESS_STATUS = (
    "atomic_consumption_registry_adapter_implementation_readiness_"
    "ready_execution_locked"
)
_SUCCESS_REASON = (
    "authorization_atomic_consumption_registry_adapter_"
    "implementation_readiness_ready_execution_locked"
)
_BLOCKED_STATUS = (
    "atomic_consumption_registry_adapter_implementation_readiness_"
    "blocked_execution_locked"
)


def _locked_flags() -> dict[str, bool]:
    return {key: False for key in _LOCKED_FLAGS}


def _blocked(reason: str) -> dict[str, object]:
    return {
        "status": _BLOCKED_STATUS,
        "reason": reason,
        "ready": False,
        "readiness": None,
        **_locked_flags(),
    }


def resolve_atomic_consumption_registry_adapter_implementation_readiness(
    value: object,
) -> dict[str, object]:
    """Resolve only an exact locked descriptor and exact readiness facts."""
    if not isinstance(value, Mapping):
        return _blocked(
            "authorization_atomic_consumption_registry_adapter_"
            "implementation_readiness_invalid_input"
        )

    source = dict(value)
    if set(source) != _INPUT_KEYS:
        return _blocked(
            "authorization_atomic_consumption_registry_adapter_"
            "implementation_readiness_structure_invalid"
        )

    accepted = source["acceptedImplementationDescriptorResult"]
    if not isinstance(accepted, Mapping):
        return _blocked(
            "authorization_atomic_consumption_registry_adapter_"
            "implementation_readiness_source_invalid"
        )

    accepted_data = dict(accepted)
    if set(accepted_data) != _SOURCE_KEYS:
        return _blocked(
            "authorization_atomic_consumption_registry_adapter_"
            "implementation_readiness_source_structure_invalid"
        )
    if accepted_data["status"] != (
        "accepted_atomic_consumption_registry_adapter_implementation_"
        "descriptor_execution_locked"
    ):
        return _blocked(
            "authorization_atomic_consumption_registry_adapter_"
            "implementation_readiness_source_status_invalid"
        )
    if accepted_data["reason"] != (
        "authorization_atomic_consumption_registry_adapter_"
        "implementation_descriptor_accepted_execution_locked"
    ):
        return _blocked(
            "authorization_atomic_consumption_registry_adapter_"
            "implementation_readiness_source_reason_invalid"
        )
    if accepted_data["accepted"] is not True:
        return _blocked(
            "authorization_atomic_consumption_registry_adapter_"
            "implementation_readiness_source_acceptance_invalid"
        )

    for key in _LOCKED_FLAGS:
        if accepted_data[key] is not False:
            return _blocked(
                "authorization_atomic_consumption_registry_adapter_"
                "implementation_readiness_source_boundary_open"
            )

    descriptor = accepted_data["acceptedDescriptor"]
    if not isinstance(descriptor, Mapping):
        return _blocked(
            "authorization_atomic_consumption_registry_adapter_"
            "implementation_readiness_descriptor_invalid"
        )
    descriptor_data = dict(descriptor)
    if set(descriptor_data) != _DESCRIPTOR_KEYS:
        return _blocked(
            "authorization_atomic_consumption_registry_adapter_"
            "implementation_readiness_descriptor_structure_invalid"
        )
    if descriptor_data["descriptorVersion"] != 1:
        return _blocked(
            "authorization_atomic_consumption_registry_adapter_"
            "implementation_readiness_descriptor_version_invalid"
        )
    if descriptor_data["sourceContractVersion"] != "v27.33g":
        return _blocked(
            "authorization_atomic_consumption_registry_adapter_"
            "implementation_readiness_descriptor_source_version_invalid"
        )
    if descriptor_data["sourceContractStatus"] != (
        "planned_atomic_consumption_registry_adapter_implementation_"
        "fully_locked_not_implemented"
    ):
        return _blocked(
            "authorization_atomic_consumption_registry_adapter_"
            "implementation_readiness_descriptor_source_status_invalid"
        )
    if type(descriptor_data["contractFacts"]) is not dict or (
        descriptor_data["contractFacts"] != _EXPECTED_IMPLEMENTATION_CONTRACT
    ):
        return _blocked(
            "authorization_atomic_consumption_registry_adapter_"
            "implementation_readiness_contract_facts_invalid"
        )
    if descriptor_data["executionGrant"] is not False:
        return _blocked(
            "authorization_atomic_consumption_registry_adapter_"
            "implementation_readiness_descriptor_boundary_open"
        )

    facts = source["implementationFacts"]
    if not isinstance(facts, Mapping):
        return _blocked(
            "authorization_atomic_consumption_registry_adapter_"
            "implementation_readiness_facts_invalid"
        )
    if dict(facts) != _EXPECTED_IMPLEMENTATION_FACTS:
        return _blocked(
            "authorization_atomic_consumption_registry_adapter_"
            "implementation_readiness_facts_invalid"
        )

    readiness = {
        "readinessVersion": 1,
        "sourceStatus": accepted_data["status"],
        "sourceReason": accepted_data["reason"],
        "acceptedDescriptor": copy.deepcopy(descriptor_data),
        "implementationFacts": copy.deepcopy(
            _EXPECTED_IMPLEMENTATION_FACTS
        ),
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
        "status": _SUCCESS_STATUS,
        "reason": _SUCCESS_REASON,
        "ready": True,
        "readiness": readiness,
        **_locked_flags(),
    }
