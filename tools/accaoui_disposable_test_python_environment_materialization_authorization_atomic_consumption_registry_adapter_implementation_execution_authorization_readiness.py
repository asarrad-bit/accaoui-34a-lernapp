from __future__ import annotations

import copy
import hashlib
import json
from collections.abc import Mapping

EXPECTED_ACCEPTED_DESCRIPTOR_FINGERPRINT = (
    "e3a1debf37035e4cf3f5553415daf65935dc53e5e9eaa335297e15f156638e8e"
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
    "acceptedAuthorizationDescriptorResult",
    "authorizationCapabilityFacts",
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
    "authorizationGrantCreated",
    "authorizationTokenGenerated",
    "authorizationMayBeConsumed",
    "executionGrant",
})

EXPECTED_AUTHORIZATION_CAPABILITY_FACTS = {
    "identityBoundary": {
        "exactIdentityFields": [
            "operationId",
            "requestId",
            "authorizationNonce",
            "planFingerprint",
            "actorId",
            "purpose",
        ],
        "allIdentityFieldsRequired": True,
        "allIdentityFieldsMustBeNonEmptyStrings": True,
        "identityFieldsImmutable": True,
        "identitySubstitutionAllowed": False,
        "operationIdReuseWithDifferentBindingAllowed": False,
        "requestIdReuseWithDifferentBindingAllowed": False,
        "authorizationNonceReuseAllowed": False,
        "planFingerprintMustEqualAcceptedPlanFingerprint": True,
        "actorIdSubstitutionAllowed": False,
        "purposeSubstitutionAllowed": False,
    },
    "authorizationBoundary": {
        "authorizationContractPrepared": True,
        "authorizationGrantCreated": False,
        "authorizationTokenGenerated": False,
        "authorizationMayBeConsumed": False,
        "singleUseRequired": True,
        "replayAllowed": False,
        "maximumParallelWinners": 1,
        "expectedState": "unused",
        "desiredState": "consumed",
        "requiredResultKinds": [
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
        "executionGrant": False,
    },
    "atomicityBoundary": {
        "singleAdapterInvocationRequired": True,
        "singleTransactionRequired": True,
        "compareAndSetAndConsumptionRecordSingleTransactionRequired": True,
        "consumptionRecordRequiredOnCommitted": True,
        "evidenceDerivedOnlyFromConfirmedRecord": True,
        "maximumParallelWinners": 1,
        "resetConsumedToUnusedAllowed": False,
        "alreadyConsumedIsTerminal": True,
        "parallelConflictIsTerminal": True,
        "bindingConflictIsTerminal": True,
        "expiredIsTerminal": True,
        "commitAmbiguousTerminalForAutomaticRetry": True,
        "assumeCommittedAllowed": False,
        "assumeUnusedAllowed": False,
    },
    "timeoutBoundary": {
        "operationTimeoutMilliseconds": 15000,
        "connectTimeoutMilliseconds": 3000,
        "statementTimeoutMilliseconds": 5000,
        "lockTimeoutMilliseconds": 2000,
        "timeoutValuesImmutable": True,
        "timeoutExpansionAllowed": False,
    },
    "failureBoundary": {
        "rawErrorExposed": False,
        "automaticRetryAfterAmbiguousAllowed": False,
        "unknownFailureResultKind": "operation_failed",
        "adapterUnavailableResultKind": "adapter_unavailable",
        "atomicityUnavailableResultKind": "atomicity_unavailable",
        "commitAmbiguousResultKind": "commit_ambiguous",
        "failureMayGrantAuthorization": False,
        "failureMayAssumeConsumption": False,
        "failureMayResetConsumption": False,
    },
    "reconciliationBoundary": {
        "reconciliationRequired": True,
        "reconciliationIdentityField": "operationId",
        "reconciliationMayReadByOperationIdLater": True,
        "reconciliationMayWriteAllowed": False,
        "reconciliationMayGrantAuthorization": False,
        "reconciliationMayResetConsumedState": False,
        "reconciliationExecutionPerformed": False,
    },
    "implementationBoundary": {
        "implementationExecutionAuthorizationContractPrepared": True,
        "authorizationDescriptorImplemented": False,
        "authorizationDescriptorAcceptanceGuardImplemented": False,
        "adapterModuleCreated": False,
        "adapterInterfaceImplemented": False,
        "adapterFactoryImplemented": False,
        "adapterImported": False,
        "adapterInstantiated": False,
        "adapterInvoked": False,
        "registryReadPerformed": False,
        "registryWritePerformed": False,
        "atomicCompareAndSetPerformed": False,
        "authorizationConsumed": False,
        "authorizationGranted": False,
        "authorizationTokenGenerated": False,
        "trustedClockRead": False,
        "filesystemReadPerformed": False,
        "filesystemMutationPerformed": False,
        "processExecuted": False,
        "networkExecuted": False,
        "driverImported": False,
        "databaseConnectionCreated": False,
        "databaseTestExecuted": False,
        "sqlMigrationCreated": False,
        "frontendIntegration": False,
        "executionGrant": False,
    },
    "securityBoundary": {
        "adapterImplementationAllowed": False,
        "adapterImportAllowed": False,
        "adapterInstantiationAllowed": False,
        "adapterInvocationAllowed": False,
        "authorizationConsumptionAllowed": False,
        "authorizationGrantAllowed": False,
        "authorizationTokenAllowed": False,
        "registryReadAllowed": False,
        "registryWriteAllowed": False,
        "atomicCompareAndSetAllowed": False,
        "reconciliationReadAllowed": False,
        "trustedClockReadAllowed": False,
        "processEnvironmentReadAllowed": False,
        "filesystemReadAllowed": False,
        "filesystemMutationAllowed": False,
        "processExecutionAllowed": False,
        "networkExecutionAllowed": False,
        "driverImportAllowed": False,
        "databaseConnectionAllowed": False,
        "passwordAllowed": False,
        "databaseUrlAllowed": False,
        "connectionStringAllowed": False,
        "serviceRoleKeyAllowed": False,
        "productionSecretAllowed": False,
        "realParticipantDataAllowed": False,
        "frontendReferenceAllowed": False,
        "directAppExecutionGrantAllowed": False,
    },
}

SUCCESS_STATUS = (
    "atomic_consumption_registry_adapter_implementation_execution_"
    "authorization_readiness_ready_execution_locked"
)
SUCCESS_REASON = (
    "authorization_atomic_consumption_registry_adapter_"
    "implementation_execution_authorization_readiness_"
    "ready_execution_locked"
)
BLOCKED_STATUS = (
    "atomic_consumption_registry_adapter_implementation_execution_"
    "authorization_readiness_blocked_execution_locked"
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


def canonical_fingerprint(value: object) -> str | None:
    try:
        canonical = json.dumps(
            value,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
    except (TypeError, ValueError):
        return None
    return hashlib.sha256(canonical).hexdigest()


def resolve_atomic_consumption_registry_adapter_implementation_execution_authorization_readiness(
    value: object,
) -> dict[str, object]:
    if not isinstance(value, Mapping):
        return blocked(
            "implementation_execution_authorization_readiness_"
            "invalid_input"
        )

    source = dict(value)
    if set(source) != INPUT_KEYS:
        return blocked(
            "implementation_execution_authorization_readiness_"
            "structure_invalid"
        )

    accepted = source["acceptedAuthorizationDescriptorResult"]
    if not isinstance(accepted, Mapping):
        return blocked(
            "implementation_execution_authorization_readiness_"
            "source_invalid"
        )

    accepted_data = dict(accepted)
    if set(accepted_data) != SOURCE_KEYS:
        return blocked(
            "implementation_execution_authorization_readiness_"
            "source_structure_invalid"
        )
    if accepted_data["status"] != (
        "accepted_atomic_consumption_registry_adapter_implementation_"
        "execution_authorization_descriptor_execution_locked"
    ):
        return blocked(
            "implementation_execution_authorization_readiness_"
            "source_status_invalid"
        )
    if accepted_data["reason"] != (
        "authorization_atomic_consumption_registry_adapter_"
        "implementation_execution_authorization_descriptor_"
        "accepted_execution_locked"
    ):
        return blocked(
            "implementation_execution_authorization_readiness_"
            "source_reason_invalid"
        )
    if accepted_data["accepted"] is not True:
        return blocked(
            "implementation_execution_authorization_readiness_"
            "source_acceptance_invalid"
        )

    for key in LOCKED_FLAGS:
        if accepted_data[key] is not False:
            return blocked(
                "implementation_execution_authorization_readiness_"
                "source_boundary_open"
            )

    descriptor = accepted_data["acceptedDescriptor"]
    if not isinstance(descriptor, Mapping):
        return blocked(
            "implementation_execution_authorization_readiness_"
            "descriptor_invalid"
        )

    descriptor_data = dict(descriptor)
    if set(descriptor_data) != DESCRIPTOR_KEYS:
        return blocked(
            "implementation_execution_authorization_readiness_"
            "descriptor_structure_invalid"
        )
    if descriptor_data["descriptorVersion"] != 1:
        return blocked(
            "implementation_execution_authorization_readiness_"
            "descriptor_version_invalid"
        )
    if descriptor_data["sourceContractVersion"] != "v27.33u":
        return blocked(
            "implementation_execution_authorization_readiness_"
            "descriptor_source_version_invalid"
        )
    if descriptor_data["sourceContractStatus"] != (
        "planned_atomic_consumption_registry_adapter_implementation_"
        "execution_authorization_fully_locked_not_implemented"
    ):
        return blocked(
            "implementation_execution_authorization_readiness_"
            "descriptor_source_status_invalid"
        )
    if type(descriptor_data["contractFacts"]) is not dict:
        return blocked(
            "implementation_execution_authorization_readiness_"
            "contract_facts_invalid"
        )
    if canonical_fingerprint(descriptor_data) != (
        EXPECTED_ACCEPTED_DESCRIPTOR_FINGERPRINT
    ):
        return blocked(
            "implementation_execution_authorization_readiness_"
            "descriptor_fingerprint_invalid"
        )
    for key in (
        "authorizationGrantCreated",
        "authorizationTokenGenerated",
        "authorizationMayBeConsumed",
        "executionGrant",
    ):
        if descriptor_data[key] is not False:
            return blocked(
                "implementation_execution_authorization_readiness_"
                "descriptor_boundary_open"
            )

    facts = source["authorizationCapabilityFacts"]
    if not isinstance(facts, Mapping):
        return blocked(
            "implementation_execution_authorization_readiness_"
            "capability_facts_invalid"
        )
    if dict(facts) != EXPECTED_AUTHORIZATION_CAPABILITY_FACTS:
        return blocked(
            "implementation_execution_authorization_readiness_"
            "capability_facts_invalid"
        )

    readiness = {
        "readinessVersion": 1,
        "sourceStatus": accepted_data["status"],
        "sourceReason": accepted_data["reason"],
        "acceptedDescriptor": copy.deepcopy(descriptor_data),
        "authorizationCapabilityFacts": copy.deepcopy(
            EXPECTED_AUTHORIZATION_CAPABILITY_FACTS
        ),
        "authorizationGrantCreated": False,
        "authorizationTokenGenerated": False,
        "authorizationMayBeConsumed": False,
        "authorizationGrantAllowed": False,
        "authorizationTokenAllowed": False,
        "authorizationConsumptionAllowed": False,
        "adapterImplementationAllowed": False,
        "adapterImportAllowed": False,
        "adapterInstantiationAllowed": False,
        "adapterInvocationAllowed": False,
        "registryReadAllowed": False,
        "registryWriteAllowed": False,
        "atomicCompareAndSetAllowed": False,
        "reconciliationReadAllowed": False,
        "trustedClockReadAllowed": False,
        "databaseConnectionAllowed": False,
        "networkExecutionAllowed": False,
        "directAppExecutionGrantAllowed": False,
        "executionGrant": False,
    }

    return {
        "status": SUCCESS_STATUS,
        "reason": SUCCESS_REASON,
        "ready": True,
        "readiness": readiness,
        **locked_flags(),
    }
