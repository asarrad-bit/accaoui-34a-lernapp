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

INPUT_KEYS = frozenset({"contractFacts"})

SUCCESS_STATUS = (
    "atomic_consumption_registry_adapter_implementation_execution_"
    "descriptor_ready_execution_locked"
)
SUCCESS_REASON = (
    "authorization_atomic_consumption_registry_adapter_"
    "implementation_execution_descriptor_ready_execution_locked"
)
BLOCKED_STATUS = (
    "atomic_consumption_registry_adapter_implementation_execution_"
    "descriptor_blocked_execution_locked"
)
BLOCKED_REASON = (
    "authorization_atomic_consumption_registry_adapter_"
    "implementation_execution_descriptor_contract_invalid"
)


def locked_flags() -> dict[str, bool]:
    return {key: False for key in LOCKED_FLAGS}


def blocked() -> dict[str, object]:
    return {
        "status": BLOCKED_STATUS,
        "reason": BLOCKED_REASON,
        "ready": False,
        "descriptor": None,
        **locked_flags(),
    }


def resolve_atomic_consumption_registry_adapter_implementation_execution_descriptor(
    value: object,
) -> dict[str, object]:
    if not isinstance(value, Mapping):
        return blocked()

    source = dict(value)
    if set(source) != INPUT_KEYS:
        return blocked()

    facts = source["contractFacts"]
    if type(facts) is not dict:
        return blocked()
    if facts != EXPECTED_CONTRACT_FACTS:
        return blocked()

    descriptor = {
        "descriptorVersion": 1,
        "sourceContractVersion": "v27.33n",
        "sourceContractStatus": (
            "planned_atomic_consumption_registry_adapter_"
            "implementation_execution_fully_locked_not_implemented"
        ),
        "contractFacts": copy.deepcopy(EXPECTED_CONTRACT_FACTS),
        "executionGrant": False,
    }

    return {
        "status": SUCCESS_STATUS,
        "reason": SUCCESS_REASON,
        "ready": True,
        "descriptor": descriptor,
        **locked_flags(),
    }
