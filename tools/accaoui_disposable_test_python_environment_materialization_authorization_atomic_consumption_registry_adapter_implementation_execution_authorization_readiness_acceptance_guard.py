from __future__ import annotations

import copy
import json
from collections.abc import Mapping

EXPECTED_READINESS = json.loads(
    '{"acceptedDescriptor":{"authorizationGrantCreated":false,"authorizationMayBeConsumed":false,"authorizationTokenGenerated":false,"contractFacts":{"atomicityBoundary":{"alreadyConsumedIsTerminal":true,"assumeCommittedAllowed":false,"assumeUnusedAllowed":false,"bindingConflictIsTerminal":true,"commitAmbiguousTerminalForAutomaticRetry":true,"compareAndSetAndConsumptionRecordSingleTransactionRequired":true,"consumptionRecordRequiredOnCommitted":true,"evidenceDerivedOnlyFromConfirmedRecord":true,"expiredIsTerminal":true,"maximumParallelWinners":1,"parallelConflictIsTerminal":true,"resetConsumedToUnusedAllowed":false,"singleAdapterInvocationRequired":true,"singleTransactionRequired":true},"authorizationBoundary":{"authorizationContractPrepared":true,"authorizationGrantCreated":false,"authorizationMayBeConsumed":false,"authorizationTokenGenerated":false,"desiredState":"consumed","executionGrant":false,"expectedState":"unused","maximumParallelWinners":1,"replayAllowed":false,"requiredResultKinds":["committed","already_consumed","parallel_conflict","binding_conflict","expired","adapter_unavailable","atomicity_unavailable","commit_ambiguous","operation_failed"],"singleUseRequired":true},"contractVersion":1,"failureBoundary":{"adapterUnavailableResultKind":"adapter_unavailable","atomicityUnavailableResultKind":"atomicity_unavailable","automaticRetryAfterAmbiguousAllowed":false,"commitAmbiguousResultKind":"commit_ambiguous","failureMayAssumeConsumption":false,"failureMayGrantAuthorization":false,"failureMayResetConsumption":false,"rawErrorExposed":false,"unknownFailureResultKind":"operation_failed"},"futureBoundary":{"adapterFactoryImplemented":false,"adapterImported":false,"adapterInstantiated":false,"adapterInterfaceImplemented":false,"adapterInvoked":false,"adapterModuleCreated":false,"atomicConsumptionExecuted":false,"authorizationDescriptorAcceptanceGuardImplemented":false,"authorizationDescriptorImplemented":false,"authorizationReadinessImplemented":false,"databaseTestExecuted":false,"directAppExecutionGrant":false,"frontendIntegration":false,"registryAccessPerformed":false},"identityBoundary":{"actorIdSubstitutionAllowed":false,"allIdentityFieldsMustBeNonEmptyStrings":true,"allIdentityFieldsRequired":true,"authorizationNonceReuseAllowed":false,"exactIdentityFields":["operationId","requestId","authorizationNonce","planFingerprint","actorId","purpose"],"identityFieldsImmutable":true,"identitySubstitutionAllowed":false,"operationIdReuseWithDifferentBindingAllowed":false,"planFingerprintMustEqualAcceptedPlanFingerprint":true,"purposeSubstitutionAllowed":false,"requestIdReuseWithDifferentBindingAllowed":false},"implementationBoundary":{"adapterFactoryImplemented":false,"adapterImported":false,"adapterInstantiated":false,"adapterInterfaceImplemented":false,"adapterInvoked":false,"adapterModuleCreated":false,"atomicCompareAndSetPerformed":false,"authorizationConsumed":false,"authorizationDescriptorAcceptanceGuardImplemented":false,"authorizationDescriptorImplemented":false,"authorizationGranted":false,"authorizationTokenGenerated":false,"databaseConnectionCreated":false,"databaseTestExecuted":false,"driverImported":false,"executionGrant":false,"filesystemMutationPerformed":false,"filesystemReadPerformed":false,"frontendIntegration":false,"implementationExecutionAuthorizationContractPrepared":true,"networkExecuted":false,"processExecuted":false,"registryReadPerformed":false,"registryWritePerformed":false,"sqlMigrationCreated":false,"trustedClockRead":false},"productiveReleaseAllowed":false,"reconciliationBoundary":{"reconciliationExecutionPerformed":false,"reconciliationIdentityField":"operationId","reconciliationMayGrantAuthorization":false,"reconciliationMayReadByOperationIdLater":true,"reconciliationMayResetConsumedState":false,"reconciliationMayWriteAllowed":false,"reconciliationRequired":true},"securityBoundary":{"adapterImplementationAllowed":false,"adapterImportAllowed":false,"adapterInstantiationAllowed":false,"adapterInvocationAllowed":false,"atomicCompareAndSetAllowed":false,"authorizationConsumptionAllowed":false,"authorizationGrantAllowed":false,"authorizationTokenAllowed":false,"connectionStringAllowed":false,"databaseConnectionAllowed":false,"databaseUrlAllowed":false,"directAppExecutionGrantAllowed":false,"driverImportAllowed":false,"filesystemMutationAllowed":false,"filesystemReadAllowed":false,"frontendReferenceAllowed":false,"networkExecutionAllowed":false,"passwordAllowed":false,"processEnvironmentReadAllowed":false,"processExecutionAllowed":false,"productionSecretAllowed":false,"realParticipantDataAllowed":false,"reconciliationReadAllowed":false,"registryReadAllowed":false,"registryWriteAllowed":false,"serviceRoleKeyAllowed":false,"trustedClockReadAllowed":false},"sourceBoundary":{"allSourceSecurityFlagsMustBeFalse":true,"canonicalFingerprintEncoding":"json_utf8_sorted_keys_compact","exactCanonicalAcceptedPlanRequired":true,"requiredAccepted":true,"requiredAcceptedPlanFingerprint":"6669d79ab9a3a64bc5399092e55a508248dab01575eda4caeb07a7b73d1b4dd7","requiredAcceptedReason":"authorization_atomic_consumption_registry_adapter_implementation_execution_plan_accepted_execution_locked","requiredAcceptedStatus":"accepted_atomic_consumption_registry_adapter_implementation_execution_plan_execution_locked","requiredExecutionGrant":false,"requiredPlanVersion":1,"requiredSourceStatus":"implemented_pure_atomic_consumption_registry_adapter_implementation_execution_plan_acceptance_execution_locked","requiredSourceVersion":"v27.33t","requiredStepCount":12},"status":"planned_atomic_consumption_registry_adapter_implementation_execution_authorization_fully_locked_not_implemented","timeoutBoundary":{"connectTimeoutMilliseconds":3000,"lockTimeoutMilliseconds":2000,"operationTimeoutMilliseconds":15000,"statementTimeoutMilliseconds":5000,"timeoutExpansionAllowed":false,"timeoutValuesImmutable":true},"version":"v27.33u"},"descriptorVersion":1,"executionGrant":false,"sourceContractStatus":"planned_atomic_consumption_registry_adapter_implementation_execution_authorization_fully_locked_not_implemented","sourceContractVersion":"v27.33u"},"adapterImplementationAllowed":false,"adapterImportAllowed":false,"adapterInstantiationAllowed":false,"adapterInvocationAllowed":false,"atomicCompareAndSetAllowed":false,"authorizationCapabilityFacts":{"atomicityBoundary":{"alreadyConsumedIsTerminal":true,"assumeCommittedAllowed":false,"assumeUnusedAllowed":false,"bindingConflictIsTerminal":true,"commitAmbiguousTerminalForAutomaticRetry":true,"compareAndSetAndConsumptionRecordSingleTransactionRequired":true,"consumptionRecordRequiredOnCommitted":true,"evidenceDerivedOnlyFromConfirmedRecord":true,"expiredIsTerminal":true,"maximumParallelWinners":1,"parallelConflictIsTerminal":true,"resetConsumedToUnusedAllowed":false,"singleAdapterInvocationRequired":true,"singleTransactionRequired":true},"authorizationBoundary":{"authorizationContractPrepared":true,"authorizationGrantCreated":false,"authorizationMayBeConsumed":false,"authorizationTokenGenerated":false,"desiredState":"consumed","executionGrant":false,"expectedState":"unused","maximumParallelWinners":1,"replayAllowed":false,"requiredResultKinds":["committed","already_consumed","parallel_conflict","binding_conflict","expired","adapter_unavailable","atomicity_unavailable","commit_ambiguous","operation_failed"],"singleUseRequired":true},"failureBoundary":{"adapterUnavailableResultKind":"adapter_unavailable","atomicityUnavailableResultKind":"atomicity_unavailable","automaticRetryAfterAmbiguousAllowed":false,"commitAmbiguousResultKind":"commit_ambiguous","failureMayAssumeConsumption":false,"failureMayGrantAuthorization":false,"failureMayResetConsumption":false,"rawErrorExposed":false,"unknownFailureResultKind":"operation_failed"},"identityBoundary":{"actorIdSubstitutionAllowed":false,"allIdentityFieldsMustBeNonEmptyStrings":true,"allIdentityFieldsRequired":true,"authorizationNonceReuseAllowed":false,"exactIdentityFields":["operationId","requestId","authorizationNonce","planFingerprint","actorId","purpose"],"identityFieldsImmutable":true,"identitySubstitutionAllowed":false,"operationIdReuseWithDifferentBindingAllowed":false,"planFingerprintMustEqualAcceptedPlanFingerprint":true,"purposeSubstitutionAllowed":false,"requestIdReuseWithDifferentBindingAllowed":false},"implementationBoundary":{"adapterFactoryImplemented":false,"adapterImported":false,"adapterInstantiated":false,"adapterInterfaceImplemented":false,"adapterInvoked":false,"adapterModuleCreated":false,"atomicCompareAndSetPerformed":false,"authorizationConsumed":false,"authorizationDescriptorAcceptanceGuardImplemented":false,"authorizationDescriptorImplemented":false,"authorizationGranted":false,"authorizationTokenGenerated":false,"databaseConnectionCreated":false,"databaseTestExecuted":false,"driverImported":false,"executionGrant":false,"filesystemMutationPerformed":false,"filesystemReadPerformed":false,"frontendIntegration":false,"implementationExecutionAuthorizationContractPrepared":true,"networkExecuted":false,"processExecuted":false,"registryReadPerformed":false,"registryWritePerformed":false,"sqlMigrationCreated":false,"trustedClockRead":false},"reconciliationBoundary":{"reconciliationExecutionPerformed":false,"reconciliationIdentityField":"operationId","reconciliationMayGrantAuthorization":false,"reconciliationMayReadByOperationIdLater":true,"reconciliationMayResetConsumedState":false,"reconciliationMayWriteAllowed":false,"reconciliationRequired":true},"securityBoundary":{"adapterImplementationAllowed":false,"adapterImportAllowed":false,"adapterInstantiationAllowed":false,"adapterInvocationAllowed":false,"atomicCompareAndSetAllowed":false,"authorizationConsumptionAllowed":false,"authorizationGrantAllowed":false,"authorizationTokenAllowed":false,"connectionStringAllowed":false,"databaseConnectionAllowed":false,"databaseUrlAllowed":false,"directAppExecutionGrantAllowed":false,"driverImportAllowed":false,"filesystemMutationAllowed":false,"filesystemReadAllowed":false,"frontendReferenceAllowed":false,"networkExecutionAllowed":false,"passwordAllowed":false,"processEnvironmentReadAllowed":false,"processExecutionAllowed":false,"productionSecretAllowed":false,"realParticipantDataAllowed":false,"reconciliationReadAllowed":false,"registryReadAllowed":false,"registryWriteAllowed":false,"serviceRoleKeyAllowed":false,"trustedClockReadAllowed":false},"timeoutBoundary":{"connectTimeoutMilliseconds":3000,"lockTimeoutMilliseconds":2000,"operationTimeoutMilliseconds":15000,"statementTimeoutMilliseconds":5000,"timeoutExpansionAllowed":false,"timeoutValuesImmutable":true}},"authorizationConsumptionAllowed":false,"authorizationGrantAllowed":false,"authorizationGrantCreated":false,"authorizationMayBeConsumed":false,"authorizationTokenAllowed":false,"authorizationTokenGenerated":false,"databaseConnectionAllowed":false,"directAppExecutionGrantAllowed":false,"executionGrant":false,"networkExecutionAllowed":false,"readinessVersion":1,"reconciliationReadAllowed":false,"registryReadAllowed":false,"registryWriteAllowed":false,"sourceReason":"authorization_atomic_consumption_registry_adapter_implementation_execution_authorization_descriptor_accepted_execution_locked","sourceStatus":"accepted_atomic_consumption_registry_adapter_implementation_execution_authorization_descriptor_execution_locked","trustedClockReadAllowed":false}'
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
    "authorization_readiness_ready_execution_locked"
)
SOURCE_REASON = (
    "authorization_atomic_consumption_registry_adapter_"
    "implementation_execution_authorization_readiness_"
    "ready_execution_locked"
)
ACCEPTED_STATUS = (
    "accepted_atomic_consumption_registry_adapter_implementation_"
    "execution_authorization_readiness_execution_locked"
)
ACCEPTED_REASON = (
    "authorization_atomic_consumption_registry_adapter_"
    "implementation_execution_authorization_readiness_"
    "accepted_execution_locked"
)
BLOCKED_STATUS = (
    "atomic_consumption_registry_adapter_implementation_execution_"
    "authorization_readiness_acceptance_blocked_execution_locked"
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


def accept_atomic_consumption_registry_adapter_implementation_execution_authorization_readiness(
    candidate: object,
) -> dict[str, object]:
    if not isinstance(candidate, Mapping):
        return blocked(
            "implementation_execution_authorization_readiness_"
            "acceptance_invalid_input"
        )

    source = dict(candidate)
    if set(source) != SOURCE_KEYS:
        return blocked(
            "implementation_execution_authorization_readiness_"
            "acceptance_structure_invalid"
        )
    if source["status"] != SOURCE_STATUS:
        return blocked(
            "implementation_execution_authorization_readiness_"
            "acceptance_status_invalid"
        )
    if source["reason"] != SOURCE_REASON:
        return blocked(
            "implementation_execution_authorization_readiness_"
            "acceptance_reason_invalid"
        )
    if source["ready"] is not True:
        return blocked(
            "implementation_execution_authorization_readiness_"
            "acceptance_ready_invalid"
        )

    for key in LOCKED_FLAGS:
        if source[key] is not False:
            return blocked(
                "implementation_execution_authorization_readiness_"
                "acceptance_source_boundary_open"
            )

    readiness = source["readiness"]
    if type(readiness) is not dict:
        return blocked(
            "implementation_execution_authorization_readiness_"
            "acceptance_readiness_invalid"
        )
    if readiness != EXPECTED_READINESS:
        return blocked(
            "implementation_execution_authorization_readiness_"
            "acceptance_readiness_invalid"
        )

    return {
        "status": ACCEPTED_STATUS,
        "reason": ACCEPTED_REASON,
        "accepted": True,
        "acceptedReadiness": copy.deepcopy(readiness),
        **locked_flags(),
    }
