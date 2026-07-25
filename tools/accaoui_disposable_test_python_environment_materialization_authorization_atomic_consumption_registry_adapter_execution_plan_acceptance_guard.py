from __future__ import annotations

import copy
import json
from collections.abc import Mapping


_EXPECTED_READINESS = json.loads('{"adapterFacts":{"adapterImplementationReportedAvailable":true,"adapterInvocationAllowed":false,"adapterKind":"single_use_consumption_registry","ambiguousCommitReconciliationReportedAvailable":true,"atomicCompareAndSetAllowed":false,"atomicCompareAndSetWithRecordReportedAvailable":true,"authorizationConsumptionAllowed":false,"automaticRetryAfterAmbiguousAllowed":false,"connectTimeoutMilliseconds":3000,"consumedResetReportedAllowed":false,"consumptionRecordInSameTransactionReportedSupported":true,"evidenceFromConfirmedRecordReportedSupported":true,"exactInputFieldsReportedSupported":["operationId","requestId","authorizationNonce","planFingerprint","actorId","purpose","expectedState","desiredState","consumptionRecord","evidenceTemplate"],"exactResultKindsReportedSupported":["committed","already_consumed","parallel_conflict","binding_conflict","expired","adapter_unavailable","atomicity_unavailable","commit_ambiguous","operation_failed"],"executionGrant":false,"lockTimeoutMilliseconds":2000,"maximumParallelWinnersReported":1,"operationName":"consume_materialization_authorization_atomically","operationTimeoutMilliseconds":15000,"rawErrorSuppressed":true,"reconciliationReadByOperationIdReportedAvailable":true,"registryReadAllowed":false,"registryWriteAllowed":false,"requiredCapabilityReportedAvailable":true,"singleAdapterInvocationReportedSupported":true,"statementTimeoutMilliseconds":5000},"adapterImplementationAllowed":false,"adapterInvocationAllowed":false,"atomicCompareAndSetAllowed":false,"authorizationConsumptionAllowed":false,"descriptor":{"contractFacts":{"ambiguityBoundary":{"assumeCommittedAllowed":false,"assumeUnusedAllowed":false,"automaticRetryAfterAmbiguousAllowed":false,"commitAmbiguousTerminalForAutomaticRetry":true,"reconciliationMayReadByOperationIdLater":true,"reconciliationMayWriteAllowed":false,"reconciliationRequired":true},"atomicityBoundary":{"alreadyConsumedIsTerminal":true,"bindingConflictIsTerminal":true,"compareAndSetAndConsumptionRecordSingleTransactionRequired":true,"consumptionRecordRequiredOnCommitted":true,"evidenceDerivedOnlyFromConfirmedRecord":true,"expiredIsTerminal":true,"parallelWinnerCountMaximum":1,"resetConsumedToUnusedAllowed":false},"contractVersion":1,"executionBoundary":{"adapterKind":"single_use_consumption_registry","connectTimeoutMilliseconds":3000,"desiredState":"consumed","exactResultKinds":["committed","already_consumed","parallel_conflict","binding_conflict","expired","adapter_unavailable","atomicity_unavailable","commit_ambiguous","operation_failed"],"executionGrant":false,"expectedState":"unused","inputFields":["operationId","requestId","authorizationNonce","planFingerprint","actorId","purpose","expectedState","desiredState","consumptionRecord","evidenceTemplate"],"inputMutationAllowed":false,"lockTimeoutMilliseconds":2000,"maximumParallelWinners":1,"missingInputFieldsAllowed":false,"operationName":"consume_materialization_authorization_atomically","operationTimeoutMilliseconds":15000,"rawErrorSuppressed":true,"requiredCapability":"atomic_compare_and_set_with_consumption_record","singleAdapterInvocationRequired":true,"statementTimeoutMilliseconds":5000,"unknownInputFieldsAllowed":false},"implementationBoundary":{"atomicCompareAndSetPerformed":false,"authorizationConsumed":false,"authorizationGranted":false,"authorizationTokenGenerated":false,"databaseConnectionCreated":false,"databaseTestExecuted":false,"driverImported":false,"executionContractPrepared":true,"filesystemMutationPerformed":false,"filesystemReadPerformed":false,"frontendIntegration":false,"networkExecuted":false,"processExecuted":false,"registryAdapterImplemented":false,"registryAdapterInvoked":false,"registryReadPerformed":false,"registryWritePerformed":false,"sqlMigrationCreated":false,"trustedClockRead":false},"productiveReleaseAllowed":false,"securityBoundary":{"adapterImplementationAllowed":false,"adapterInvocationAllowed":false,"atomicCompareAndSetAllowed":false,"authorizationConsumptionAllowed":false,"authorizationGrantAllowed":false,"authorizationTokenAllowed":false,"connectionStringAllowed":false,"databaseConnectionAllowed":false,"databaseUrlAllowed":false,"driverImportAllowed":false,"filesystemMutationAllowed":false,"filesystemReadAllowed":false,"frontendReferenceAllowed":false,"networkExecutionAllowed":false,"passwordAllowed":false,"processEnvironmentReadAllowed":false,"processExecutionAllowed":false,"productionSecretAllowed":false,"realParticipantDataAllowed":false,"reconciliationReadAllowed":false,"registryReadAllowed":false,"registryWriteAllowed":false,"serviceRoleKeyAllowed":false,"trustedClockReadAllowed":false},"sourceBoundary":{"allSourceSecurityFlagsMustBeFalse":true,"requiredAccepted":true,"requiredAcceptedReason":"authorization_atomic_consumption_registry_adapter_readiness_accepted_execution_locked","requiredAcceptedStatus":"accepted_atomic_consumption_registry_adapter_readiness_execution_locked","requiredExecutionGrant":false,"requiredSourceStatus":"implemented_pure_atomic_consumption_registry_adapter_readiness_acceptance_execution_locked","requiredSourceVersion":"v27.32y"},"status":"planned_atomic_consumption_registry_adapter_execution_fully_locked_not_implemented","unresolvedRequirements":{"databaseTestExecution":true,"directAppExecutionGrant":true,"environmentEvidenceCollector":true,"environmentMaterializer":true,"environmentRollbackImplementation":true,"frontendIntegration":true,"materializationAuthorizationConsumptionReceipt":true,"registryAdapterExecution":true,"registryAdapterExecutionDescriptor":true,"registryAdapterExecutionPlan":true,"registryAdapterImplementation":true,"registryAdapterReconciliation":true},"version":"v27.32z"},"descriptorVersion":1,"executionGrant":false,"sourceContractStatus":"planned_atomic_consumption_registry_adapter_execution_fully_locked_not_implemented","sourceContractVersion":"v27.32z"},"executionGrant":false,"readinessVersion":1,"registryReadAllowed":false,"registryWriteAllowed":false,"sourceReason":"authorization_atomic_consumption_registry_adapter_execution_descriptor_accepted_execution_locked","sourceStatus":"accepted_atomic_consumption_registry_adapter_execution_descriptor_execution_locked"}')
_LOCKED_FLAGS = ('adapterImplemented', 'adapterInvoked', 'registryReadPerformed', 'registryWritePerformed', 'atomicCompareAndSetPerformed', 'authorizationConsumed', 'authorizationGranted', 'authorizationTokenGenerated', 'trustedClockRead', 'filesystemReadPerformed', 'filesystemMutationPerformed', 'processExecuted', 'networkExecuted', 'driverImported', 'databaseConnectionCreated', 'databaseTestExecuted', 'sqlMigrationCreated', 'frontendIntegration', 'executionGrant')
_SOURCE_KEYS = frozenset({
    "status",
    "reason",
    "ready",
    "plan",
    *_LOCKED_FLAGS,
})
_PLAN_KEYS = frozenset({
    "planVersion",
    "sourceStatus",
    "sourceReason",
    "readiness",
    "operationFacts",
    "steps",
    "singleAdapterInvocationRequired",
    "maximumParallelWinners",
    "automaticRetryAfterAmbiguousAllowed",
    "reconciliationRequired",
    "evidenceFromConfirmedRecordOnly",
    "executionGrant",
})
_OPERATION_FIELDS = ('operationId', 'requestId', 'authorizationNonce', 'planFingerprint', 'actorId', 'purpose', 'expectedState', 'desiredState', 'consumptionRecord', 'evidenceTemplate')
_RECORD_FIELDS = ('recordVersion', 'operationId', 'requestId', 'authorizationNonce', 'planFingerprint', 'actorId', 'purpose', 'expectedState', 'desiredState', 'confirmed')
_EVIDENCE_FIELDS = ('evidenceVersion', 'operationId', 'recordSource', 'confirmedRecordRequired', 'unconfirmedEvidenceAllowed')
_PLAN_STEPS = ('validate_accepted_execution_readiness', 'validate_operation_facts', 'bind_operation_to_single_use_registry_adapter', 'prepare_single_adapter_invocation', 'require_atomic_compare_and_set_with_consumption_record', 'classify_exact_result_kind', 'derive_evidence_from_confirmed_record_only', 'reconcile_commit_ambiguous_without_automatic_retry')

_SUCCESS_SOURCE_STATUS = (
    "atomic_consumption_registry_adapter_execution_plan_"
    "ready_execution_locked"
)
_SUCCESS_SOURCE_REASON = (
    "authorization_atomic_consumption_registry_adapter_execution_"
    "plan_ready_execution_locked"
)
_ACCEPTED_STATUS = (
    "accepted_atomic_consumption_registry_adapter_execution_plan_"
    "execution_locked"
)
_ACCEPTED_REASON = (
    "authorization_atomic_consumption_registry_adapter_execution_plan_"
    "accepted_execution_locked"
)
_BLOCKED_STATUS = (
    "atomic_consumption_registry_adapter_execution_plan_acceptance_"
    "blocked_execution_locked"
)


def _locked_flags() -> dict[str, bool]:
    return {key: False for key in _LOCKED_FLAGS}


def _blocked(reason: str) -> dict[str, object]:
    return {
        "status": _BLOCKED_STATUS,
        "reason": reason,
        "accepted": False,
        "acceptedPlan": None,
        **_locked_flags(),
    }


def _valid_scalar(value: object) -> bool:
    return (
        type(value) is str
        and 1 <= len(value) <= 256
        and value == value.strip()
        and not any(ord(char) < 32 for char in value)
    )


def _normalize_operation_facts(value: object):
    if not isinstance(value, Mapping):
        return None
    source = dict(value)
    if set(source) != set(_OPERATION_FIELDS):
        return None

    for key in (
        "operationId",
        "requestId",
        "authorizationNonce",
        "planFingerprint",
        "actorId",
        "purpose",
    ):
        if not _valid_scalar(source[key]):
            return None

    if source["expectedState"] != "unused":
        return None
    if source["desiredState"] != "consumed":
        return None

    record = source["consumptionRecord"]
    if not isinstance(record, Mapping):
        return None
    record_data = dict(record)
    if set(record_data) != set(_RECORD_FIELDS):
        return None
    if record_data["recordVersion"] != 1:
        return None
    if record_data["confirmed"] is not False:
        return None
    for key in (
        "operationId",
        "requestId",
        "authorizationNonce",
        "planFingerprint",
        "actorId",
        "purpose",
        "expectedState",
        "desiredState",
    ):
        if record_data[key] != source[key]:
            return None

    evidence = source["evidenceTemplate"]
    if not isinstance(evidence, Mapping):
        return None
    evidence_data = dict(evidence)
    if set(evidence_data) != set(_EVIDENCE_FIELDS):
        return None
    if evidence_data["evidenceVersion"] != 1:
        return None
    if evidence_data["operationId"] != source["operationId"]:
        return None
    if evidence_data["recordSource"] != "confirmed_consumption_record_only":
        return None
    if evidence_data["confirmedRecordRequired"] is not True:
        return None
    if evidence_data["unconfirmedEvidenceAllowed"] is not False:
        return None

    return {key: copy.deepcopy(source[key]) for key in _OPERATION_FIELDS}


def _valid_steps(value: object) -> bool:
    if type(value) is not list or len(value) != len(_PLAN_STEPS):
        return False
    for index, (item, expected_name) in enumerate(
        zip(value, _PLAN_STEPS, strict=True),
        start=1,
    ):
        if not isinstance(item, Mapping):
            return False
        data = dict(item)
        if set(data) != {"position", "name", "executionAllowed"}:
            return False
        if data["position"] != index:
            return False
        if data["name"] != expected_name:
            return False
        if data["executionAllowed"] is not False:
            return False
    return True


def accept_atomic_consumption_registry_adapter_execution_plan(
    candidate: object,
) -> dict[str, object]:
    """Accept only the exact canonical locked v27.33e execution plan."""
    if not isinstance(candidate, Mapping):
        return _blocked(
            "authorization_atomic_consumption_registry_adapter_execution_"
            "plan_acceptance_invalid_input"
        )

    source = dict(candidate)
    if set(source) != _SOURCE_KEYS:
        return _blocked(
            "authorization_atomic_consumption_registry_adapter_execution_"
            "plan_acceptance_structure_invalid"
        )
    if source["status"] != _SUCCESS_SOURCE_STATUS:
        return _blocked(
            "authorization_atomic_consumption_registry_adapter_execution_"
            "plan_acceptance_source_status_invalid"
        )
    if source["reason"] != _SUCCESS_SOURCE_REASON:
        return _blocked(
            "authorization_atomic_consumption_registry_adapter_execution_"
            "plan_acceptance_source_reason_invalid"
        )
    if source["ready"] is not True:
        return _blocked(
            "authorization_atomic_consumption_registry_adapter_execution_"
            "plan_acceptance_source_ready_invalid"
        )
    for key in _LOCKED_FLAGS:
        if source[key] is not False:
            return _blocked(
                "authorization_atomic_consumption_registry_adapter_execution_"
                "plan_acceptance_source_boundary_open"
            )

    plan = source["plan"]
    if not isinstance(plan, Mapping):
        return _blocked(
            "authorization_atomic_consumption_registry_adapter_execution_"
            "plan_acceptance_plan_invalid"
        )
    data = dict(plan)
    if set(data) != _PLAN_KEYS:
        return _blocked(
            "authorization_atomic_consumption_registry_adapter_execution_"
            "plan_acceptance_plan_structure_invalid"
        )
    if data["planVersion"] != 1:
        return _blocked(
            "authorization_atomic_consumption_registry_adapter_execution_"
            "plan_acceptance_plan_version_invalid"
        )
    if data["sourceStatus"] != (
        "accepted_atomic_consumption_registry_adapter_execution_"
        "readiness_execution_locked"
    ) or data["sourceReason"] != (
        "authorization_atomic_consumption_registry_adapter_execution_"
        "readiness_accepted_execution_locked"
    ):
        return _blocked(
            "authorization_atomic_consumption_registry_adapter_execution_"
            "plan_acceptance_plan_source_invalid"
        )
    if type(data["readiness"]) is not dict or (
        data["readiness"] != _EXPECTED_READINESS
    ):
        return _blocked(
            "authorization_atomic_consumption_registry_adapter_execution_"
            "plan_acceptance_readiness_binding_invalid"
        )

    operation_facts = _normalize_operation_facts(data["operationFacts"])
    if operation_facts is None or operation_facts != data["operationFacts"]:
        return _blocked(
            "authorization_atomic_consumption_registry_adapter_execution_"
            "plan_acceptance_operation_facts_invalid"
        )
    if not _valid_steps(data["steps"]):
        return _blocked(
            "authorization_atomic_consumption_registry_adapter_execution_"
            "plan_acceptance_steps_invalid"
        )
    if data["singleAdapterInvocationRequired"] is not True:
        return _blocked(
            "authorization_atomic_consumption_registry_adapter_execution_"
            "plan_acceptance_single_invocation_invalid"
        )
    if data["maximumParallelWinners"] != 1:
        return _blocked(
            "authorization_atomic_consumption_registry_adapter_execution_"
            "plan_acceptance_parallel_boundary_invalid"
        )
    if data["automaticRetryAfterAmbiguousAllowed"] is not False:
        return _blocked(
            "authorization_atomic_consumption_registry_adapter_execution_"
            "plan_acceptance_retry_boundary_open"
        )
    if data["reconciliationRequired"] is not True:
        return _blocked(
            "authorization_atomic_consumption_registry_adapter_execution_"
            "plan_acceptance_reconciliation_invalid"
        )
    if data["evidenceFromConfirmedRecordOnly"] is not True:
        return _blocked(
            "authorization_atomic_consumption_registry_adapter_execution_"
            "plan_acceptance_evidence_boundary_invalid"
        )
    if data["executionGrant"] is not False:
        return _blocked(
            "authorization_atomic_consumption_registry_adapter_execution_"
            "plan_acceptance_plan_boundary_open"
        )

    return {
        "status": _ACCEPTED_STATUS,
        "reason": _ACCEPTED_REASON,
        "accepted": True,
        "acceptedPlan": copy.deepcopy(data),
        **_locked_flags(),
    }
