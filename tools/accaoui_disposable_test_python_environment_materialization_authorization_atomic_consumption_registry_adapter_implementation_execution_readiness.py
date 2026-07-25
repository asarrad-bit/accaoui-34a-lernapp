from __future__ import annotations

import copy
import json
from collections.abc import Mapping

EXPECTED_EXECUTION_CONTRACT = json.loads(
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

INPUT_KEYS = frozenset({
    "acceptedExecutionDescriptorResult",
    "executionCapabilityFacts",
})

SOURCE_KEYS = frozenset({
    "status",
    "reason",
    "accepted",
    "acceptedDescriptor",
    *LOCKED_FLAGS,
})

DESCRIPTOR_KEYS = frozenset({
    "descriptorVersion",
    "sourceContractVersion",
    "sourceContractStatus",
    "contractFacts",
    "executionGrant",
})

EXPECTED_EXECUTION_CAPABILITY_FACTS = {
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
    "readiness_ready_execution_locked"
)
SUCCESS_REASON = (
    "authorization_atomic_consumption_registry_adapter_"
    "implementation_execution_readiness_ready_execution_locked"
)
BLOCKED_STATUS = (
    "atomic_consumption_registry_adapter_implementation_execution_"
    "readiness_blocked_execution_locked"
)


def locked_flags() -> dict[str, bool]:
    return {key: False for key in LOCKED_FLAGS}


def blocked(reason: str) -> dict[str, object]:
    return {
        "status": BLOCKED_STATUS,
        "reason": reason,
        "ready": False,
        "readiness": None,
        **locked_flags(),
    }


def resolve_atomic_consumption_registry_adapter_implementation_execution_readiness(
    value: object,
) -> dict[str, object]:
    if not isinstance(value, Mapping):
        return blocked("implementation_execution_readiness_invalid_input")

    source = dict(value)
    if set(source) != INPUT_KEYS:
        return blocked(
            "implementation_execution_readiness_structure_invalid"
        )

    accepted = source["acceptedExecutionDescriptorResult"]
    if not isinstance(accepted, Mapping):
        return blocked(
            "implementation_execution_readiness_source_invalid"
        )

    accepted_data = dict(accepted)
    if set(accepted_data) != SOURCE_KEYS:
        return blocked(
            "implementation_execution_readiness_source_structure_invalid"
        )
    if accepted_data["status"] != (
        "accepted_atomic_consumption_registry_adapter_implementation_"
        "execution_descriptor_execution_locked"
    ):
        return blocked(
            "implementation_execution_readiness_source_status_invalid"
        )
    if accepted_data["reason"] != (
        "authorization_atomic_consumption_registry_adapter_"
        "implementation_execution_descriptor_accepted_execution_locked"
    ):
        return blocked(
            "implementation_execution_readiness_source_reason_invalid"
        )
    if accepted_data["accepted"] is not True:
        return blocked(
            "implementation_execution_readiness_source_acceptance_invalid"
        )

    for key in LOCKED_FLAGS:
        if accepted_data[key] is not False:
            return blocked(
                "implementation_execution_readiness_source_boundary_open"
            )

    descriptor = accepted_data["acceptedDescriptor"]
    if not isinstance(descriptor, Mapping):
        return blocked(
            "implementation_execution_readiness_descriptor_invalid"
        )

    descriptor_data = dict(descriptor)
    if set(descriptor_data) != DESCRIPTOR_KEYS:
        return blocked(
            "implementation_execution_readiness_"
            "descriptor_structure_invalid"
        )
    if descriptor_data["descriptorVersion"] != 1:
        return blocked(
            "implementation_execution_readiness_"
            "descriptor_version_invalid"
        )
    if descriptor_data["sourceContractVersion"] != "v27.33n":
        return blocked(
            "implementation_execution_readiness_"
            "descriptor_source_version_invalid"
        )
    if descriptor_data["sourceContractStatus"] != (
        "planned_atomic_consumption_registry_adapter_"
        "implementation_execution_fully_locked_not_implemented"
    ):
        return blocked(
            "implementation_execution_readiness_"
            "descriptor_source_status_invalid"
        )
    if type(descriptor_data["contractFacts"]) is not dict:
        return blocked(
            "implementation_execution_readiness_contract_facts_invalid"
        )
    if descriptor_data["contractFacts"] != EXPECTED_EXECUTION_CONTRACT:
        return blocked(
            "implementation_execution_readiness_contract_facts_invalid"
        )
    if descriptor_data["executionGrant"] is not False:
        return blocked(
            "implementation_execution_readiness_"
            "descriptor_boundary_open"
        )

    facts = source["executionCapabilityFacts"]
    if not isinstance(facts, Mapping):
        return blocked(
            "implementation_execution_readiness_capability_facts_invalid"
        )
    if dict(facts) != EXPECTED_EXECUTION_CAPABILITY_FACTS:
        return blocked(
            "implementation_execution_readiness_capability_facts_invalid"
        )

    readiness = {
        "readinessVersion": 1,
        "sourceStatus": accepted_data["status"],
        "sourceReason": accepted_data["reason"],
        "acceptedDescriptor": copy.deepcopy(descriptor_data),
        "executionCapabilityFacts": copy.deepcopy(
            EXPECTED_EXECUTION_CAPABILITY_FACTS
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
        "readiness": readiness,
        **locked_flags(),
    }
