from __future__ import annotations

import copy
import json
from collections.abc import Mapping

_EXPECTED_CONTRACT_FACTS = json.loads('{"ambiguityBoundary":{"assumeCommittedAllowed":false,"assumeUnusedAllowed":false,"automaticRetryAfterAmbiguousAllowed":false,"commitAmbiguousTerminalForAutomaticRetry":true,"reconciliationMayReadByOperationIdLater":true,"reconciliationMayWriteAllowed":false,"reconciliationRequired":true},"atomicityBoundary":{"alreadyConsumedIsTerminal":true,"bindingConflictIsTerminal":true,"compareAndSetAndConsumptionRecordSingleTransactionRequired":true,"consumptionRecordRequiredOnCommitted":true,"evidenceDerivedOnlyFromConfirmedRecord":true,"expiredIsTerminal":true,"parallelWinnerCountMaximum":1,"resetConsumedToUnusedAllowed":false},"contractVersion":1,"dependencyBoundary":{"connectionStringAllowed":false,"databaseConnectionAllowed":false,"databaseUrlAllowed":false,"dependencyInjectionRequired":true,"driverImportAllowed":false,"environmentVariableReadAllowed":false,"hardCodedCredentialsAllowed":false,"productionSecretAllowed":false,"realParticipantDataAllowed":false,"serviceRoleKeyAllowed":false},"implementationBoundary":{"adapterFactoryImplemented":false,"adapterImported":false,"adapterInstantiated":false,"adapterInterfaceImplemented":false,"adapterInvoked":false,"adapterModuleCreated":false,"atomicCompareAndSetPerformed":false,"authorizationConsumed":false,"authorizationGranted":false,"authorizationTokenGenerated":false,"databaseConnectionCreated":false,"databaseTestExecuted":false,"driverImported":false,"executionGrant":false,"filesystemMutationPerformed":false,"filesystemReadPerformed":false,"frontendIntegration":false,"implementationContractPrepared":true,"networkExecuted":false,"processExecuted":false,"registryReadPerformed":false,"registryWritePerformed":false,"sqlMigrationCreated":false,"trustedClockRead":false},"interfaceBoundary":{"adapterKind":"single_use_consumption_registry","connectTimeoutMilliseconds":3000,"desiredState":"consumed","exactInputFields":["operationId","requestId","authorizationNonce","planFingerprint","actorId","purpose","expectedState","desiredState","consumptionRecord","evidenceTemplate"],"exactResultKinds":["committed","already_consumed","parallel_conflict","binding_conflict","expired","adapter_unavailable","atomicity_unavailable","commit_ambiguous","operation_failed"],"executionGrant":false,"expectedState":"unused","factoryName":"build_atomic_consumption_registry_adapter","interfaceVersion":1,"lockTimeoutMilliseconds":2000,"maximumParallelWinners":1,"operationName":"consume_materialization_authorization_atomically","operationTimeoutMilliseconds":15000,"plannedModulePath":"tools/accaoui_disposable_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter.py","protocolName":"AtomicConsumptionRegistryAdapter","rawErrorSuppressed":true,"requiredCapability":"atomic_compare_and_set_with_consumption_record","singleAdapterInvocationRequired":true,"statementTimeoutMilliseconds":5000},"productiveReleaseAllowed":false,"securityBoundary":{"adapterImplementationAllowed":false,"adapterImportAllowed":false,"adapterInstantiationAllowed":false,"adapterInvocationAllowed":false,"atomicCompareAndSetAllowed":false,"authorizationConsumptionAllowed":false,"authorizationGrantAllowed":false,"authorizationTokenAllowed":false,"connectionStringAllowed":false,"databaseConnectionAllowed":false,"databaseUrlAllowed":false,"directAppExecutionGrantAllowed":false,"driverImportAllowed":false,"filesystemMutationAllowed":false,"filesystemReadAllowed":false,"frontendReferenceAllowed":false,"networkExecutionAllowed":false,"passwordAllowed":false,"processEnvironmentReadAllowed":false,"processExecutionAllowed":false,"productionSecretAllowed":false,"realParticipantDataAllowed":false,"reconciliationReadAllowed":false,"registryReadAllowed":false,"registryWriteAllowed":false,"serviceRoleKeyAllowed":false,"trustedClockReadAllowed":false},"sourceBoundary":{"allSourceSecurityFlagsMustBeFalse":true,"requiredAccepted":true,"requiredAcceptedReason":"authorization_atomic_consumption_registry_adapter_execution_plan_accepted_execution_locked","requiredAcceptedStatus":"accepted_atomic_consumption_registry_adapter_execution_plan_execution_locked","requiredExecutionGrant":false,"requiredSourceStatus":"implemented_pure_atomic_consumption_registry_adapter_execution_plan_acceptance_execution_locked","requiredSourceVersion":"v27.33f"},"status":"planned_atomic_consumption_registry_adapter_implementation_fully_locked_not_implemented","unresolvedRequirements":{"databaseTestExecution":true,"directAppExecutionGrant":true,"environmentEvidenceCollector":true,"environmentMaterializer":true,"environmentRollbackImplementation":true,"frontendIntegration":true,"materializationAuthorizationConsumptionReceipt":true,"registryAdapterExecution":true,"registryAdapterImplementation":true,"registryAdapterImplementationDescriptor":true,"registryAdapterInstantiation":true,"registryAdapterReconciliation":true},"version":"v27.33g"}')
_INPUT_KEYS = {"contractFacts"}
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

_SUCCESS_STATUS = (
    "atomic_consumption_registry_adapter_implementation_descriptor_"
    "ready_execution_locked"
)
_SUCCESS_REASON = (
    "authorization_atomic_consumption_registry_adapter_"
    "implementation_descriptor_ready_execution_locked"
)
_BLOCKED_STATUS = (
    "atomic_consumption_registry_adapter_implementation_descriptor_"
    "blocked_execution_locked"
)
_BLOCKED_REASON = (
    "authorization_atomic_consumption_registry_adapter_"
    "implementation_descriptor_contract_invalid"
)


def _locked_flags() -> dict[str, bool]:
    return {key: False for key in _LOCKED_FLAGS}


def _blocked() -> dict[str, object]:
    return {
        "status": _BLOCKED_STATUS,
        "reason": _BLOCKED_REASON,
        "ready": False,
        "descriptor": None,
        **_locked_flags(),
    }


def resolve_atomic_consumption_registry_adapter_implementation_descriptor(
    value: object,
) -> dict[str, object]:
    """Validate exact v27.33g facts and return a locked canonical copy."""
    if not isinstance(value, Mapping):
        return _blocked()

    if set(value.keys()) != _INPUT_KEYS:
        return _blocked()

    contract_facts = value.get("contractFacts")
    if type(contract_facts) is not dict:
        return _blocked()

    if contract_facts != _EXPECTED_CONTRACT_FACTS:
        return _blocked()

    descriptor = {
        "descriptorVersion": 1,
        "sourceContractVersion": "v27.33g",
        "sourceContractStatus": (
            "planned_atomic_consumption_registry_adapter_implementation_"
            "fully_locked_not_implemented"
        ),
        "contractFacts": copy.deepcopy(_EXPECTED_CONTRACT_FACTS),
        "executionGrant": False,
    }

    return {
        "status": _SUCCESS_STATUS,
        "reason": _SUCCESS_REASON,
        "ready": True,
        "descriptor": descriptor,
        **_locked_flags(),
    }
