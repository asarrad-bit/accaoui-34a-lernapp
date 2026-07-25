from __future__ import annotations

import copy
import json
from collections.abc import Mapping


_EXPECTED_READINESS = json.loads('{"adapterFacts":{"adapterImplementationReportedAvailable":true,"adapterInvocationAllowed":false,"adapterKind":"single_use_consumption_registry","ambiguousCommitReconciliationReportedAvailable":true,"atomicCompareAndSetAllowed":false,"atomicCompareAndSetWithRecordReportedAvailable":true,"authorizationConsumptionAllowed":false,"automaticRetryAfterAmbiguousAllowed":false,"connectTimeoutMilliseconds":3000,"consumedResetReportedAllowed":false,"consumptionRecordInSameTransactionReportedSupported":true,"evidenceFromConfirmedRecordReportedSupported":true,"exactInputFieldsReportedSupported":["operationId","requestId","authorizationNonce","planFingerprint","actorId","purpose","expectedState","desiredState","consumptionRecord","evidenceTemplate"],"exactResultKindsReportedSupported":["committed","already_consumed","parallel_conflict","binding_conflict","expired","adapter_unavailable","atomicity_unavailable","commit_ambiguous","operation_failed"],"executionGrant":false,"lockTimeoutMilliseconds":2000,"maximumParallelWinnersReported":1,"operationName":"consume_materialization_authorization_atomically","operationTimeoutMilliseconds":15000,"rawErrorSuppressed":true,"reconciliationReadByOperationIdReportedAvailable":true,"registryReadAllowed":false,"registryWriteAllowed":false,"requiredCapabilityReportedAvailable":true,"singleAdapterInvocationReportedSupported":true,"statementTimeoutMilliseconds":5000},"adapterImplementationAllowed":false,"adapterInvocationAllowed":false,"atomicCompareAndSetAllowed":false,"authorizationConsumptionAllowed":false,"descriptor":{"contractFacts":{"ambiguityBoundary":{"assumeCommittedAllowed":false,"assumeUnusedAllowed":false,"automaticRetryAfterAmbiguousAllowed":false,"commitAmbiguousTerminalForAutomaticRetry":true,"reconciliationMayReadByOperationIdLater":true,"reconciliationMayWriteAllowed":false,"reconciliationRequired":true},"atomicityBoundary":{"alreadyConsumedIsTerminal":true,"bindingConflictIsTerminal":true,"compareAndSetAndConsumptionRecordSingleTransactionRequired":true,"consumptionRecordRequiredOnCommitted":true,"evidenceDerivedOnlyFromConfirmedRecord":true,"expiredIsTerminal":true,"parallelWinnerCountMaximum":1,"resetConsumedToUnusedAllowed":false},"contractVersion":1,"executionBoundary":{"adapterKind":"single_use_consumption_registry","connectTimeoutMilliseconds":3000,"desiredState":"consumed","exactResultKinds":["committed","already_consumed","parallel_conflict","binding_conflict","expired","adapter_unavailable","atomicity_unavailable","commit_ambiguous","operation_failed"],"executionGrant":false,"expectedState":"unused","inputFields":["operationId","requestId","authorizationNonce","planFingerprint","actorId","purpose","expectedState","desiredState","consumptionRecord","evidenceTemplate"],"inputMutationAllowed":false,"lockTimeoutMilliseconds":2000,"maximumParallelWinners":1,"missingInputFieldsAllowed":false,"operationName":"consume_materialization_authorization_atomically","operationTimeoutMilliseconds":15000,"rawErrorSuppressed":true,"requiredCapability":"atomic_compare_and_set_with_consumption_record","singleAdapterInvocationRequired":true,"statementTimeoutMilliseconds":5000,"unknownInputFieldsAllowed":false},"implementationBoundary":{"atomicCompareAndSetPerformed":false,"authorizationConsumed":false,"authorizationGranted":false,"authorizationTokenGenerated":false,"databaseConnectionCreated":false,"databaseTestExecuted":false,"driverImported":false,"executionContractPrepared":true,"filesystemMutationPerformed":false,"filesystemReadPerformed":false,"frontendIntegration":false,"networkExecuted":false,"processExecuted":false,"registryAdapterImplemented":false,"registryAdapterInvoked":false,"registryReadPerformed":false,"registryWritePerformed":false,"sqlMigrationCreated":false,"trustedClockRead":false},"productiveReleaseAllowed":false,"securityBoundary":{"adapterImplementationAllowed":false,"adapterInvocationAllowed":false,"atomicCompareAndSetAllowed":false,"authorizationConsumptionAllowed":false,"authorizationGrantAllowed":false,"authorizationTokenAllowed":false,"connectionStringAllowed":false,"databaseConnectionAllowed":false,"databaseUrlAllowed":false,"driverImportAllowed":false,"filesystemMutationAllowed":false,"filesystemReadAllowed":false,"frontendReferenceAllowed":false,"networkExecutionAllowed":false,"passwordAllowed":false,"processEnvironmentReadAllowed":false,"processExecutionAllowed":false,"productionSecretAllowed":false,"realParticipantDataAllowed":false,"reconciliationReadAllowed":false,"registryReadAllowed":false,"registryWriteAllowed":false,"serviceRoleKeyAllowed":false,"trustedClockReadAllowed":false},"sourceBoundary":{"allSourceSecurityFlagsMustBeFalse":true,"requiredAccepted":true,"requiredAcceptedReason":"authorization_atomic_consumption_registry_adapter_readiness_accepted_execution_locked","requiredAcceptedStatus":"accepted_atomic_consumption_registry_adapter_readiness_execution_locked","requiredExecutionGrant":false,"requiredSourceStatus":"implemented_pure_atomic_consumption_registry_adapter_readiness_acceptance_execution_locked","requiredSourceVersion":"v27.32y"},"status":"planned_atomic_consumption_registry_adapter_execution_fully_locked_not_implemented","unresolvedRequirements":{"databaseTestExecution":true,"directAppExecutionGrant":true,"environmentEvidenceCollector":true,"environmentMaterializer":true,"environmentRollbackImplementation":true,"frontendIntegration":true,"materializationAuthorizationConsumptionReceipt":true,"registryAdapterExecution":true,"registryAdapterExecutionDescriptor":true,"registryAdapterExecutionPlan":true,"registryAdapterImplementation":true,"registryAdapterReconciliation":true},"version":"v27.32z"},"descriptorVersion":1,"executionGrant":false,"sourceContractStatus":"planned_atomic_consumption_registry_adapter_execution_fully_locked_not_implemented","sourceContractVersion":"v27.32z"},"executionGrant":false,"readinessVersion":1,"registryReadAllowed":false,"registryWriteAllowed":false,"sourceReason":"authorization_atomic_consumption_registry_adapter_execution_descriptor_accepted_execution_locked","sourceStatus":"accepted_atomic_consumption_registry_adapter_execution_descriptor_execution_locked"}')
_VALID_OPERATION_FACTS = json.loads('{"actorId":"actor-v2733e-test","authorizationNonce":"nonce-v2733e-0001","consumptionRecord":{"actorId":"actor-v2733e-test","authorizationNonce":"nonce-v2733e-0001","confirmed":false,"desiredState":"consumed","expectedState":"unused","operationId":"operation-v2733e-0001","planFingerprint":"sha256:v2733e-test-plan-fingerprint","purpose":"materialize-disposable-postgresql-test-python-environment","recordVersion":1,"requestId":"request-v2733e-0001"},"desiredState":"consumed","evidenceTemplate":{"confirmedRecordRequired":true,"evidenceVersion":1,"operationId":"operation-v2733e-0001","recordSource":"confirmed_consumption_record_only","unconfirmedEvidenceAllowed":false},"expectedState":"unused","operationId":"operation-v2733e-0001","planFingerprint":"sha256:v2733e-test-plan-fingerprint","purpose":"materialize-disposable-postgresql-test-python-environment","requestId":"request-v2733e-0001"}')
_LOCKED_FLAGS = ('adapterImplemented', 'adapterInvoked', 'registryReadPerformed', 'registryWritePerformed', 'atomicCompareAndSetPerformed', 'authorizationConsumed', 'authorizationGranted', 'authorizationTokenGenerated', 'trustedClockRead', 'filesystemReadPerformed', 'filesystemMutationPerformed', 'processExecuted', 'networkExecuted', 'driverImported', 'databaseConnectionCreated', 'databaseTestExecuted', 'sqlMigrationCreated', 'frontendIntegration', 'executionGrant')

_INPUT_KEYS = frozenset({
    "acceptedExecutionReadinessResult",
    "operationFacts",
})
_SOURCE_KEYS = frozenset({
    "status",
    "reason",
    "accepted",
    "acceptedReadiness",
    *_LOCKED_FLAGS,
})
_OPERATION_FIELDS = ('operationId', 'requestId', 'authorizationNonce', 'planFingerprint', 'actorId', 'purpose', 'expectedState', 'desiredState', 'consumptionRecord', 'evidenceTemplate')
_RECORD_FIELDS = ('recordVersion', 'operationId', 'requestId', 'authorizationNonce', 'planFingerprint', 'actorId', 'purpose', 'expectedState', 'desiredState', 'confirmed')
_EVIDENCE_FIELDS = ('evidenceVersion', 'operationId', 'recordSource', 'confirmedRecordRequired', 'unconfirmedEvidenceAllowed')
_PLAN_STEPS = ('validate_accepted_execution_readiness', 'validate_operation_facts', 'bind_operation_to_single_use_registry_adapter', 'prepare_single_adapter_invocation', 'require_atomic_compare_and_set_with_consumption_record', 'classify_exact_result_kind', 'derive_evidence_from_confirmed_record_only', 'reconcile_commit_ambiguous_without_automatic_retry')

_SUCCESS_STATUS = (
    "atomic_consumption_registry_adapter_execution_plan_"
    "ready_execution_locked"
)
_SUCCESS_REASON = (
    "authorization_atomic_consumption_registry_adapter_execution_"
    "plan_ready_execution_locked"
)
_BLOCKED_STATUS = (
    "atomic_consumption_registry_adapter_execution_plan_"
    "blocked_execution_locked"
)


def _locked_flags() -> dict[str, bool]:
    return {key: False for key in _LOCKED_FLAGS}


def _blocked(reason: str) -> dict[str, object]:
    return {
        "status": _BLOCKED_STATUS,
        "reason": reason,
        "ready": False,
        "plan": None,
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
    if evidence_data["recordSource"] != (
        "confirmed_consumption_record_only"
    ):
        return None
    if evidence_data["confirmedRecordRequired"] is not True:
        return None
    if evidence_data["unconfirmedEvidenceAllowed"] is not False:
        return None

    return {key: copy.deepcopy(source[key]) for key in _OPERATION_FIELDS}


def resolve_atomic_consumption_registry_adapter_execution_plan(
    candidate: object,
) -> dict[str, object]:
    """Build only a canonical locked execution plan; execute nothing."""
    if not isinstance(candidate, Mapping):
        return _blocked(
            "authorization_atomic_consumption_registry_adapter_execution_"
            "plan_invalid_input"
        )

    source = dict(candidate)
    if set(source) != _INPUT_KEYS:
        return _blocked(
            "authorization_atomic_consumption_registry_adapter_execution_"
            "plan_structure_invalid"
        )

    accepted = source["acceptedExecutionReadinessResult"]
    if not isinstance(accepted, Mapping):
        return _blocked(
            "authorization_atomic_consumption_registry_adapter_execution_"
            "plan_readiness_invalid"
        )
    accepted_data = dict(accepted)
    if set(accepted_data) != _SOURCE_KEYS:
        return _blocked(
            "authorization_atomic_consumption_registry_adapter_execution_"
            "plan_readiness_structure_invalid"
        )
    if accepted_data["status"] != (
        "accepted_atomic_consumption_registry_adapter_execution_"
        "readiness_execution_locked"
    ):
        return _blocked(
            "authorization_atomic_consumption_registry_adapter_execution_"
            "plan_readiness_status_invalid"
        )
    if accepted_data["reason"] != (
        "authorization_atomic_consumption_registry_adapter_execution_"
        "readiness_accepted_execution_locked"
    ):
        return _blocked(
            "authorization_atomic_consumption_registry_adapter_execution_"
            "plan_readiness_reason_invalid"
        )
    if accepted_data["accepted"] is not True:
        return _blocked(
            "authorization_atomic_consumption_registry_adapter_execution_"
            "plan_readiness_acceptance_invalid"
        )
    for key in _LOCKED_FLAGS:
        if accepted_data[key] is not False:
            return _blocked(
                "authorization_atomic_consumption_registry_adapter_execution_"
                "plan_readiness_boundary_open"
            )
    if type(accepted_data["acceptedReadiness"]) is not dict or (
        accepted_data["acceptedReadiness"] != _EXPECTED_READINESS
    ):
        return _blocked(
            "authorization_atomic_consumption_registry_adapter_execution_"
            "plan_readiness_binding_invalid"
        )

    operation_facts = _normalize_operation_facts(source["operationFacts"])
    if operation_facts is None:
        return _blocked(
            "authorization_atomic_consumption_registry_adapter_execution_"
            "plan_operation_facts_invalid"
        )

    steps = [
        {
            "position": index,
            "name": name,
            "executionAllowed": False,
        }
        for index, name in enumerate(_PLAN_STEPS, start=1)
    ]
    plan = {
        "planVersion": 1,
        "sourceStatus": accepted_data["status"],
        "sourceReason": accepted_data["reason"],
        "readiness": copy.deepcopy(_EXPECTED_READINESS),
        "operationFacts": operation_facts,
        "steps": steps,
        "singleAdapterInvocationRequired": True,
        "maximumParallelWinners": 1,
        "automaticRetryAfterAmbiguousAllowed": False,
        "reconciliationRequired": True,
        "evidenceFromConfirmedRecordOnly": True,
        "executionGrant": False,
    }
    return {
        "status": _SUCCESS_STATUS,
        "reason": _SUCCESS_REASON,
        "ready": True,
        "plan": plan,
        **_locked_flags(),
    }
