from __future__ import annotations

import copy
import json
from collections.abc import Mapping


_EXPECTED_CONTRACT_FACTS = json.loads('{"ambiguityBoundary":{"assumeCommittedAllowed":false,"assumeUnusedAllowed":false,"automaticRetryAfterAmbiguousAllowed":false,"commitAmbiguousTerminalForAutomaticRetry":true,"reconciliationMayReadByOperationIdLater":true,"reconciliationMayWriteAllowed":false,"reconciliationRequired":true},"atomicityBoundary":{"alreadyConsumedIsTerminal":true,"bindingConflictIsTerminal":true,"compareAndSetAndConsumptionRecordSingleTransactionRequired":true,"consumptionRecordRequiredOnCommitted":true,"evidenceDerivedOnlyFromConfirmedRecord":true,"expiredIsTerminal":true,"parallelWinnerCountMaximum":1,"resetConsumedToUnusedAllowed":false},"contractVersion":1,"executionBoundary":{"adapterKind":"single_use_consumption_registry","connectTimeoutMilliseconds":3000,"desiredState":"consumed","exactResultKinds":["committed","already_consumed","parallel_conflict","binding_conflict","expired","adapter_unavailable","atomicity_unavailable","commit_ambiguous","operation_failed"],"executionGrant":false,"expectedState":"unused","inputFields":["operationId","requestId","authorizationNonce","planFingerprint","actorId","purpose","expectedState","desiredState","consumptionRecord","evidenceTemplate"],"inputMutationAllowed":false,"lockTimeoutMilliseconds":2000,"maximumParallelWinners":1,"missingInputFieldsAllowed":false,"operationName":"consume_materialization_authorization_atomically","operationTimeoutMilliseconds":15000,"rawErrorSuppressed":true,"requiredCapability":"atomic_compare_and_set_with_consumption_record","singleAdapterInvocationRequired":true,"statementTimeoutMilliseconds":5000,"unknownInputFieldsAllowed":false},"implementationBoundary":{"atomicCompareAndSetPerformed":false,"authorizationConsumed":false,"authorizationGranted":false,"authorizationTokenGenerated":false,"databaseConnectionCreated":false,"databaseTestExecuted":false,"driverImported":false,"executionContractPrepared":true,"filesystemMutationPerformed":false,"filesystemReadPerformed":false,"frontendIntegration":false,"networkExecuted":false,"processExecuted":false,"registryAdapterImplemented":false,"registryAdapterInvoked":false,"registryReadPerformed":false,"registryWritePerformed":false,"sqlMigrationCreated":false,"trustedClockRead":false},"productiveReleaseAllowed":false,"securityBoundary":{"adapterImplementationAllowed":false,"adapterInvocationAllowed":false,"atomicCompareAndSetAllowed":false,"authorizationConsumptionAllowed":false,"authorizationGrantAllowed":false,"authorizationTokenAllowed":false,"connectionStringAllowed":false,"databaseConnectionAllowed":false,"databaseUrlAllowed":false,"driverImportAllowed":false,"filesystemMutationAllowed":false,"filesystemReadAllowed":false,"frontendReferenceAllowed":false,"networkExecutionAllowed":false,"passwordAllowed":false,"processEnvironmentReadAllowed":false,"processExecutionAllowed":false,"productionSecretAllowed":false,"realParticipantDataAllowed":false,"reconciliationReadAllowed":false,"registryReadAllowed":false,"registryWriteAllowed":false,"serviceRoleKeyAllowed":false,"trustedClockReadAllowed":false},"sourceBoundary":{"allSourceSecurityFlagsMustBeFalse":true,"requiredAccepted":true,"requiredAcceptedReason":"authorization_atomic_consumption_registry_adapter_readiness_accepted_execution_locked","requiredAcceptedStatus":"accepted_atomic_consumption_registry_adapter_readiness_execution_locked","requiredExecutionGrant":false,"requiredSourceStatus":"implemented_pure_atomic_consumption_registry_adapter_readiness_acceptance_execution_locked","requiredSourceVersion":"v27.32y"},"status":"planned_atomic_consumption_registry_adapter_execution_fully_locked_not_implemented","unresolvedRequirements":{"databaseTestExecution":true,"directAppExecutionGrant":true,"environmentEvidenceCollector":true,"environmentMaterializer":true,"environmentRollbackImplementation":true,"frontendIntegration":true,"materializationAuthorizationConsumptionReceipt":true,"registryAdapterExecution":true,"registryAdapterExecutionDescriptor":true,"registryAdapterExecutionPlan":true,"registryAdapterImplementation":true,"registryAdapterReconciliation":true},"version":"v27.32z"}')
_EXPECTED_ADAPTER_FACTS = json.loads('{"adapterImplementationReportedAvailable":true,"adapterInvocationAllowed":false,"adapterKind":"single_use_consumption_registry","ambiguousCommitReconciliationReportedAvailable":true,"atomicCompareAndSetAllowed":false,"atomicCompareAndSetWithRecordReportedAvailable":true,"authorizationConsumptionAllowed":false,"automaticRetryAfterAmbiguousAllowed":false,"connectTimeoutMilliseconds":3000,"consumedResetReportedAllowed":false,"consumptionRecordInSameTransactionReportedSupported":true,"evidenceFromConfirmedRecordReportedSupported":true,"exactInputFieldsReportedSupported":["operationId","requestId","authorizationNonce","planFingerprint","actorId","purpose","expectedState","desiredState","consumptionRecord","evidenceTemplate"],"exactResultKindsReportedSupported":["committed","already_consumed","parallel_conflict","binding_conflict","expired","adapter_unavailable","atomicity_unavailable","commit_ambiguous","operation_failed"],"executionGrant":false,"lockTimeoutMilliseconds":2000,"maximumParallelWinnersReported":1,"operationName":"consume_materialization_authorization_atomically","operationTimeoutMilliseconds":15000,"rawErrorSuppressed":true,"reconciliationReadByOperationIdReportedAvailable":true,"registryReadAllowed":false,"registryWriteAllowed":false,"requiredCapabilityReportedAvailable":true,"singleAdapterInvocationReportedSupported":true,"statementTimeoutMilliseconds":5000}')

_LOCKED_FLAGS = ('adapterImplemented', 'adapterInvoked', 'registryReadPerformed', 'registryWritePerformed', 'atomicCompareAndSetPerformed', 'authorizationConsumed', 'authorizationGranted', 'authorizationTokenGenerated', 'trustedClockRead', 'filesystemReadPerformed', 'filesystemMutationPerformed', 'processExecuted', 'networkExecuted', 'driverImported', 'databaseConnectionCreated', 'databaseTestExecuted', 'sqlMigrationCreated', 'frontendIntegration', 'executionGrant')

_SOURCE_KEYS = frozenset({
    "status",
    "reason",
    "ready",
    "readiness",
    *_LOCKED_FLAGS,
})

_READINESS_KEYS = frozenset({
    "readinessVersion",
    "sourceStatus",
    "sourceReason",
    "descriptor",
    "adapterFacts",
    "adapterImplementationAllowed",
    "adapterInvocationAllowed",
    "registryReadAllowed",
    "registryWriteAllowed",
    "atomicCompareAndSetAllowed",
    "authorizationConsumptionAllowed",
    "executionGrant",
})

_DESCRIPTOR_KEYS = frozenset({
    "descriptorVersion",
    "sourceContractVersion",
    "sourceContractStatus",
    "contractFacts",
    "executionGrant",
})

_SUCCESS_SOURCE_STATUS = (
    "atomic_consumption_registry_adapter_execution_readiness_"
    "ready_execution_locked"
)
_SUCCESS_SOURCE_REASON = (
    "authorization_atomic_consumption_registry_adapter_execution_"
    "readiness_ready_execution_locked"
)
_ACCEPTED_STATUS = (
    "accepted_atomic_consumption_registry_adapter_execution_"
    "readiness_execution_locked"
)
_ACCEPTED_REASON = (
    "authorization_atomic_consumption_registry_adapter_execution_"
    "readiness_accepted_execution_locked"
)
_BLOCKED_STATUS = (
    "atomic_consumption_registry_adapter_execution_readiness_"
    "acceptance_blocked_execution_locked"
)


def _locked_flags() -> dict[str, bool]:
    return {key: False for key in _LOCKED_FLAGS}


def _blocked(reason: str) -> dict[str, object]:
    return {
        "status": _BLOCKED_STATUS,
        "reason": reason,
        "accepted": False,
        "acceptedReadiness": None,
        **_locked_flags(),
    }


def accept_atomic_consumption_registry_adapter_execution_readiness(
    candidate: object,
) -> dict[str, object]:
    """Accept only the exact locked v27.33c execution readiness."""
    if not isinstance(candidate, Mapping):
        return _blocked(
            "authorization_atomic_consumption_registry_adapter_execution_"
            "readiness_acceptance_invalid_input"
        )

    source = dict(candidate)
    if set(source) != _SOURCE_KEYS:
        return _blocked(
            "authorization_atomic_consumption_registry_adapter_execution_"
            "readiness_acceptance_structure_invalid"
        )
    if source["status"] != _SUCCESS_SOURCE_STATUS:
        return _blocked(
            "authorization_atomic_consumption_registry_adapter_execution_"
            "readiness_acceptance_source_status_invalid"
        )
    if source["reason"] != _SUCCESS_SOURCE_REASON:
        return _blocked(
            "authorization_atomic_consumption_registry_adapter_execution_"
            "readiness_acceptance_source_reason_invalid"
        )
    if source["ready"] is not True:
        return _blocked(
            "authorization_atomic_consumption_registry_adapter_execution_"
            "readiness_acceptance_source_ready_invalid"
        )

    for key in _LOCKED_FLAGS:
        if source[key] is not False:
            return _blocked(
                "authorization_atomic_consumption_registry_adapter_execution_"
                "readiness_acceptance_source_boundary_open"
            )

    readiness = source["readiness"]
    if not isinstance(readiness, Mapping):
        return _blocked(
            "authorization_atomic_consumption_registry_adapter_execution_"
            "readiness_acceptance_readiness_invalid"
        )

    data = dict(readiness)
    if set(data) != _READINESS_KEYS:
        return _blocked(
            "authorization_atomic_consumption_registry_adapter_execution_"
            "readiness_acceptance_readiness_structure_invalid"
        )
    if data["readinessVersion"] != 1:
        return _blocked(
            "authorization_atomic_consumption_registry_adapter_execution_"
            "readiness_acceptance_readiness_version_invalid"
        )
    if data["sourceStatus"] != (
        "accepted_atomic_consumption_registry_adapter_execution_"
        "descriptor_execution_locked"
    ) or data["sourceReason"] != (
        "authorization_atomic_consumption_registry_adapter_execution_"
        "descriptor_accepted_execution_locked"
    ):
        return _blocked(
            "authorization_atomic_consumption_registry_adapter_execution_"
            "readiness_acceptance_readiness_source_invalid"
        )

    descriptor = data["descriptor"]
    if not isinstance(descriptor, Mapping):
        return _blocked(
            "authorization_atomic_consumption_registry_adapter_execution_"
            "readiness_acceptance_descriptor_invalid"
        )
    descriptor_data = dict(descriptor)
    if set(descriptor_data) != _DESCRIPTOR_KEYS:
        return _blocked(
            "authorization_atomic_consumption_registry_adapter_execution_"
            "readiness_acceptance_descriptor_structure_invalid"
        )
    if descriptor_data["descriptorVersion"] != 1:
        return _blocked(
            "authorization_atomic_consumption_registry_adapter_execution_"
            "readiness_acceptance_descriptor_version_invalid"
        )
    if descriptor_data["sourceContractVersion"] != "v27.32z" or (
        descriptor_data["sourceContractStatus"] !=
        "planned_atomic_consumption_registry_adapter_execution_"
        "fully_locked_not_implemented"
    ):
        return _blocked(
            "authorization_atomic_consumption_registry_adapter_execution_"
            "readiness_acceptance_descriptor_source_invalid"
        )
    if type(descriptor_data["contractFacts"]) is not dict or (
        descriptor_data["contractFacts"] != _EXPECTED_CONTRACT_FACTS
    ):
        return _blocked(
            "authorization_atomic_consumption_registry_adapter_execution_"
            "readiness_acceptance_contract_facts_invalid"
        )
    if descriptor_data["executionGrant"] is not False:
        return _blocked(
            "authorization_atomic_consumption_registry_adapter_execution_"
            "readiness_acceptance_descriptor_boundary_open"
        )

    facts = data["adapterFacts"]
    if not isinstance(facts, Mapping) or dict(facts) != _EXPECTED_ADAPTER_FACTS:
        return _blocked(
            "authorization_atomic_consumption_registry_adapter_execution_"
            "readiness_acceptance_adapter_facts_invalid"
        )

    for key in (
        "adapterImplementationAllowed",
        "adapterInvocationAllowed",
        "registryReadAllowed",
        "registryWriteAllowed",
        "atomicCompareAndSetAllowed",
        "authorizationConsumptionAllowed",
        "executionGrant",
    ):
        if data[key] is not False:
            return _blocked(
                "authorization_atomic_consumption_registry_adapter_execution_"
                "readiness_acceptance_readiness_boundary_open"
            )

    return {
        "status": _ACCEPTED_STATUS,
        "reason": _ACCEPTED_REASON,
        "accepted": True,
        "acceptedReadiness": copy.deepcopy(data),
        **_locked_flags(),
    }
