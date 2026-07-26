from __future__ import annotations

import base64
import copy
import hashlib
import json
import re
import threading
import unicodedata
import uuid
from datetime import datetime, timezone
from typing import Literal, Protocol, TypeAlias, TypedDict, Union, cast


PURPOSE = "disposable_test_python_environment_materialization"
CONSUMED_STATUS = "authorization_consumed_execution_locked"

REQUEST_FIELDS = (
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
)
RECORD_DRAFT_FIELDS = (
    "recordVersion",
    "operationId",
    "requestId",
    "authorizationNonce",
    "planFingerprint",
    "actorId",
    "purpose",
    "expectedState",
    "desiredState",
    "confirmed",
)
CONFIRMED_RECORD_FIELDS = RECORD_DRAFT_FIELDS + ("consumedAtUtc",)
EVIDENCE_TEMPLATE_FIELDS = (
    "evidenceVersion",
    "operationId",
    "recordSource",
    "confirmedRecordRequired",
    "unconfirmedEvidenceAllowed",
)
FAKE_REGISTRY_ENTRY_FIELDS = (
    "requestId",
    "authorizationNonce",
    "planFingerprint",
    "actorId",
    "purpose",
    "state",
    "expiresAtUtc",
    "consumptionRecord",
)
SIMULATION_DIRECTIVE_FIELDS = (
    "operationId",
    "phase",
    "resultKind",
    "commitVisibleToReconciliation",
)

UUID_V4_LOWERCASE_PATTERN = re.compile(
    r"[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-"
    r"[89ab][0-9a-f]{3}-[0-9a-f]{12}"
)
SHA256_LOWERCASE_PATTERN = re.compile(r"[0-9a-f]{64}")
BASE64URL_32_BYTE_PATTERN = re.compile(r"[A-Za-z0-9_-]{43}")
UTC_RFC3339_SECONDS_PATTERN = re.compile(
    r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z"
)


class ConsumptionRecordDraft(TypedDict):
    recordVersion: Literal[1]
    operationId: str
    requestId: str
    authorizationNonce: str
    planFingerprint: str
    actorId: str
    purpose: Literal["disposable_test_python_environment_materialization"]
    expectedState: Literal["unused"]
    desiredState: Literal["consumed"]
    confirmed: Literal[False]


class ConfirmedConsumptionRecord(TypedDict):
    recordVersion: Literal[1]
    operationId: str
    requestId: str
    authorizationNonce: str
    planFingerprint: str
    actorId: str
    purpose: Literal["disposable_test_python_environment_materialization"]
    expectedState: Literal["unused"]
    desiredState: Literal["consumed"]
    confirmed: Literal[True]
    consumedAtUtc: str


class EvidenceTemplate(TypedDict):
    evidenceVersion: Literal[1]
    operationId: str
    recordSource: Literal["confirmed_consumption_record_only"]
    confirmedRecordRequired: Literal[True]
    unconfirmedEvidenceAllowed: Literal[False]


class ConsumptionEvidence(TypedDict):
    evidenceVersion: Literal[1]
    operationId: str
    requestId: str
    authorizationNonceFingerprint: str
    planFingerprint: str
    actorId: str
    purpose: Literal["disposable_test_python_environment_materialization"]
    consumedAtUtc: str
    recordFingerprint: str
    singleUse: Literal[True]
    status: Literal["authorization_consumed_execution_locked"]
    executionGrant: Literal[False]


class AtomicConsumptionRequest(TypedDict):
    operationId: str
    requestId: str
    authorizationNonce: str
    planFingerprint: str
    actorId: str
    purpose: Literal["disposable_test_python_environment_materialization"]
    expectedState: Literal["unused"]
    desiredState: Literal["consumed"]
    consumptionRecord: ConsumptionRecordDraft
    evidenceTemplate: EvidenceTemplate


class FakeRegistryEntry(TypedDict):
    requestId: str
    authorizationNonce: str
    planFingerprint: str
    actorId: str
    purpose: Literal["disposable_test_python_environment_materialization"]
    state: Literal["unused", "consumed"]
    expiresAtUtc: str
    consumptionRecord: ConfirmedConsumptionRecord | None


class FakeSimulationDirective(TypedDict):
    operationId: str
    phase: Literal["operation", "connect", "statement", "lock", "commit"]
    resultKind: Literal[
        "adapter_unavailable",
        "atomicity_unavailable",
        "commit_ambiguous",
        "operation_failed",
    ]
    commitVisibleToReconciliation: bool


class CommittedAtomicConsumptionResult(TypedDict):
    status: Literal["authorization_consumed_execution_locked"]
    reason: Literal["authorization_consumption_committed"]
    resultKind: Literal["committed"]
    operationId: str
    consumptionStatus: Literal["confirmed_consumed"]
    reconciliationRequired: Literal[False]
    retryAllowed: Literal[False]
    executionGrant: Literal[False]
    consumptionRecord: ConfirmedConsumptionRecord
    evidence: ConsumptionEvidence


class AlreadyConsumedAtomicConsumptionResult(TypedDict):
    status: Literal["authorization_consumption_blocked_execution_locked"]
    reason: Literal["authorization_consumption_already_consumed"]
    resultKind: Literal["already_consumed"]
    operationId: str
    consumptionStatus: Literal["confirmed_already_consumed"]
    reconciliationRequired: Literal[False]
    retryAllowed: Literal[False]
    executionGrant: Literal[False]


class ParallelConflictAtomicConsumptionResult(TypedDict):
    status: Literal["authorization_consumption_blocked_execution_locked"]
    reason: Literal["authorization_consumption_parallel_conflict"]
    resultKind: Literal["parallel_conflict"]
    operationId: str
    consumptionStatus: Literal["not_consumed_by_operation"]
    reconciliationRequired: Literal[False]
    retryAllowed: Literal[False]
    executionGrant: Literal[False]


class BindingConflictAtomicConsumptionResult(TypedDict):
    status: Literal["authorization_consumption_blocked_execution_locked"]
    reason: Literal["authorization_consumption_binding_conflict"]
    resultKind: Literal["binding_conflict"]
    operationId: str
    consumptionStatus: Literal["not_consumed_by_operation"]
    reconciliationRequired: Literal[False]
    retryAllowed: Literal[False]
    executionGrant: Literal[False]


class ExpiredAtomicConsumptionResult(TypedDict):
    status: Literal["authorization_consumption_blocked_execution_locked"]
    reason: Literal["authorization_consumption_expired"]
    resultKind: Literal["expired"]
    operationId: str
    consumptionStatus: Literal["not_consumed_by_operation"]
    reconciliationRequired: Literal[False]
    retryAllowed: Literal[False]
    executionGrant: Literal[False]


class AdapterUnavailableAtomicConsumptionResult(TypedDict):
    status: Literal["authorization_consumption_blocked_execution_locked"]
    reason: Literal["authorization_consumption_adapter_unavailable"]
    resultKind: Literal["adapter_unavailable"]
    operationId: str
    consumptionStatus: Literal["not_consumed_by_operation"]
    reconciliationRequired: Literal[False]
    retryAllowed: Literal[False]
    executionGrant: Literal[False]


class AtomicityUnavailableAtomicConsumptionResult(TypedDict):
    status: Literal["authorization_consumption_blocked_execution_locked"]
    reason: Literal["authorization_consumption_atomicity_unavailable"]
    resultKind: Literal["atomicity_unavailable"]
    operationId: str
    consumptionStatus: Literal["not_consumed_by_operation"]
    reconciliationRequired: Literal[False]
    retryAllowed: Literal[False]
    executionGrant: Literal[False]


class CommitAmbiguousAtomicConsumptionResult(TypedDict):
    status: Literal[
        "authorization_consumption_reconciliation_required_execution_locked"
    ]
    reason: Literal["authorization_consumption_commit_ambiguous"]
    resultKind: Literal["commit_ambiguous"]
    operationId: str
    consumptionStatus: Literal["unknown"]
    reconciliationRequired: Literal[True]
    retryAllowed: Literal[False]
    executionGrant: Literal[False]


class OperationFailedAtomicConsumptionResult(TypedDict):
    status: Literal["authorization_consumption_blocked_execution_locked"]
    reason: Literal["authorization_consumption_operation_failed"]
    resultKind: Literal["operation_failed"]
    operationId: str
    consumptionStatus: Literal["not_consumed_by_operation"]
    reconciliationRequired: Literal[False]
    retryAllowed: Literal[False]
    executionGrant: Literal[False]


AtomicConsumptionResult: TypeAlias = Union[
    CommittedAtomicConsumptionResult,
    AlreadyConsumedAtomicConsumptionResult,
    ParallelConflictAtomicConsumptionResult,
    BindingConflictAtomicConsumptionResult,
    ExpiredAtomicConsumptionResult,
    AdapterUnavailableAtomicConsumptionResult,
    AtomicityUnavailableAtomicConsumptionResult,
    CommitAmbiguousAtomicConsumptionResult,
    OperationFailedAtomicConsumptionResult,
]


class ConfirmedReconciliationResult(TypedDict):
    status: Literal[
        "authorization_consumption_reconciliation_confirmed_execution_locked"
    ]
    reason: Literal["authorization_consumption_reconciliation_confirmed"]
    reconciliationKind: Literal["confirmed"]
    operationId: str
    consumptionStatus: Literal["confirmed_consumed"]
    writePerformed: Literal[False]
    retryPerformed: Literal[False]
    executionGrant: Literal[False]
    consumptionRecord: ConfirmedConsumptionRecord
    evidence: ConsumptionEvidence


class NotFoundReconciliationResult(TypedDict):
    status: Literal[
        "authorization_consumption_reconciliation_not_found_execution_locked"
    ]
    reason: Literal["authorization_consumption_reconciliation_not_found"]
    reconciliationKind: Literal["not_found"]
    operationId: str
    consumptionStatus: Literal["unknown"]
    writePerformed: Literal[False]
    retryPerformed: Literal[False]
    executionGrant: Literal[False]


class AmbiguousReconciliationResult(TypedDict):
    status: Literal[
        "authorization_consumption_reconciliation_ambiguous_execution_locked"
    ]
    reason: Literal["authorization_consumption_reconciliation_ambiguous"]
    reconciliationKind: Literal["ambiguous"]
    operationId: str
    consumptionStatus: Literal["unknown"]
    writePerformed: Literal[False]
    retryPerformed: Literal[False]
    executionGrant: Literal[False]


ReconciliationResult: TypeAlias = Union[
    ConfirmedReconciliationResult,
    NotFoundReconciliationResult,
    AmbiguousReconciliationResult,
]


class InjectedUtcClock(Protocol):
    def now_utc(self) -> datetime:
        ...


class LocalFakeAtomicConsumptionRegistryDriver(Protocol):
    def compare_and_set_with_consumption_record(
        self,
        request: AtomicConsumptionRequest,
    ) -> AtomicConsumptionResult:
        ...

    def read_consumption_by_operation_id(
        self,
        operation_id: str,
    ) -> ReconciliationResult:
        ...


RegistryIdentity: TypeAlias = tuple[str, str, str, str, str]


def _require_exact_mapping(
    value: object,
    fields: tuple[str, ...],
    label: str,
) -> dict[str, object]:
    if type(value) is not dict:
        raise ValueError(f"{label} must be an exact dict")
    data = value
    if tuple(data) != fields:
        raise ValueError(f"{label} fields or field order are invalid")
    return data


def _require_uuid_v4_lowercase(value: object, label: str) -> str:
    if type(value) is not str or UUID_V4_LOWERCASE_PATTERN.fullmatch(value) is None:
        raise ValueError(f"{label} must be a lowercase UUID v4")
    parsed = uuid.UUID(value)
    if parsed.version != 4 or str(parsed) != value:
        raise ValueError(f"{label} must be a canonical lowercase UUID v4")
    return value


def _require_nonce(value: object, label: str) -> str:
    if type(value) is not str or BASE64URL_32_BYTE_PATTERN.fullmatch(value) is None:
        raise ValueError(f"{label} must be an unpadded 32-byte base64url value")
    try:
        decoded = base64.urlsafe_b64decode(value + "=")
    except (ValueError, TypeError) as exc:
        raise ValueError(f"{label} is not valid base64url") from exc
    if len(decoded) != 32:
        raise ValueError(f"{label} must decode to exactly 32 bytes")
    encoded = base64.urlsafe_b64encode(decoded).decode("ascii").rstrip("=")
    if encoded != value:
        raise ValueError(f"{label} must be canonical base64url")
    return value


def _require_sha256(value: object, label: str) -> str:
    if type(value) is not str or SHA256_LOWERCASE_PATTERN.fullmatch(value) is None:
        raise ValueError(f"{label} must be lowercase SHA-256 hex")
    return value


def _require_actor_id(value: object, label: str) -> str:
    if type(value) is not str or value == "" or value != value.strip():
        raise ValueError(f"{label} must be a non-empty trimmed string")
    if len(value) > 256:
        raise ValueError(f"{label} exceeds 256 characters")
    if any(unicodedata.category(character) == "Cc" for character in value):
        raise ValueError(f"{label} contains control characters")
    return value


def _require_purpose(value: object, label: str) -> str:
    if value != PURPOSE or type(value) is not str:
        raise ValueError(f"{label} has an invalid purpose")
    return value


def _parse_utc_rfc3339_seconds(value: object, label: str) -> datetime:
    if type(value) is not str or UTC_RFC3339_SECONDS_PATTERN.fullmatch(value) is None:
        raise ValueError(f"{label} must use UTC RFC3339 seconds with Z")
    try:
        parsed = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError as exc:
        raise ValueError(f"{label} contains an invalid UTC time") from exc
    return parsed.replace(tzinfo=timezone.utc)


def _format_injected_utc(value: object) -> str:
    if not isinstance(value, datetime):
        raise ValueError("InjectedUtcClock.now_utc() must return datetime")
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("InjectedUtcClock.now_utc() must return an aware time")
    normalized = value.astimezone(timezone.utc).replace(microsecond=0)
    return normalized.strftime("%Y-%m-%dT%H:%M:%SZ")


def _registry_identity_from_values(
    request_id: str,
    authorization_nonce: str,
    plan_fingerprint: str,
    actor_id: str,
    purpose: str,
) -> RegistryIdentity:
    return (
        request_id,
        authorization_nonce,
        plan_fingerprint,
        actor_id,
        purpose,
    )


def _registry_identity_from_request(
    request: AtomicConsumptionRequest,
) -> RegistryIdentity:
    return _registry_identity_from_values(
        request["requestId"],
        request["authorizationNonce"],
        request["planFingerprint"],
        request["actorId"],
        request["purpose"],
    )


def _validate_record_identity_values(
    value: dict[str, object],
    label: str,
) -> None:
    _require_uuid_v4_lowercase(value["operationId"], f"{label}.operationId")
    _require_uuid_v4_lowercase(value["requestId"], f"{label}.requestId")
    _require_nonce(value["authorizationNonce"], f"{label}.authorizationNonce")
    _require_sha256(value["planFingerprint"], f"{label}.planFingerprint")
    _require_actor_id(value["actorId"], f"{label}.actorId")
    _require_purpose(value["purpose"], f"{label}.purpose")
    if value["expectedState"] != "unused":
        raise ValueError(f"{label}.expectedState must be unused")
    if value["desiredState"] != "consumed":
        raise ValueError(f"{label}.desiredState must be consumed")


def _validate_confirmed_record(
    value: object,
    label: str,
) -> ConfirmedConsumptionRecord:
    record = _require_exact_mapping(value, CONFIRMED_RECORD_FIELDS, label)
    if type(record["recordVersion"]) is not int or record["recordVersion"] != 1:
        raise ValueError(f"{label}.recordVersion must be integer 1")
    _validate_record_identity_values(record, label)
    if record["confirmed"] is not True:
        raise ValueError(f"{label}.confirmed must be true")
    _parse_utc_rfc3339_seconds(record["consumedAtUtc"], f"{label}.consumedAtUtc")
    return cast(ConfirmedConsumptionRecord, copy.deepcopy(record))


def _validate_request(value: object) -> AtomicConsumptionRequest:
    request = _require_exact_mapping(value, REQUEST_FIELDS, "request")
    _require_uuid_v4_lowercase(request["operationId"], "request.operationId")
    _require_uuid_v4_lowercase(request["requestId"], "request.requestId")
    _require_nonce(request["authorizationNonce"], "request.authorizationNonce")
    _require_sha256(request["planFingerprint"], "request.planFingerprint")
    _require_actor_id(request["actorId"], "request.actorId")
    _require_purpose(request["purpose"], "request.purpose")
    if request["expectedState"] != "unused":
        raise ValueError("request.expectedState must be unused")
    if request["desiredState"] != "consumed":
        raise ValueError("request.desiredState must be consumed")

    draft = _require_exact_mapping(
        request["consumptionRecord"],
        RECORD_DRAFT_FIELDS,
        "request.consumptionRecord",
    )
    if type(draft["recordVersion"]) is not int or draft["recordVersion"] != 1:
        raise ValueError("request.consumptionRecord.recordVersion must be integer 1")
    _validate_record_identity_values(draft, "request.consumptionRecord")
    if draft["confirmed"] is not False:
        raise ValueError("request.consumptionRecord.confirmed must be false")
    for field in (
        "operationId",
        "requestId",
        "authorizationNonce",
        "planFingerprint",
        "actorId",
        "purpose",
        "expectedState",
        "desiredState",
    ):
        if draft[field] != request[field]:
            raise ValueError(
                f"request.consumptionRecord.{field} must equal request.{field}"
            )

    template = _require_exact_mapping(
        request["evidenceTemplate"],
        EVIDENCE_TEMPLATE_FIELDS,
        "request.evidenceTemplate",
    )
    if type(template["evidenceVersion"]) is not int or template["evidenceVersion"] != 1:
        raise ValueError("request.evidenceTemplate.evidenceVersion must be integer 1")
    if template["operationId"] != request["operationId"]:
        raise ValueError("request.evidenceTemplate.operationId must match request")
    if template["recordSource"] != "confirmed_consumption_record_only":
        raise ValueError("request.evidenceTemplate.recordSource is invalid")
    if template["confirmedRecordRequired"] is not True:
        raise ValueError(
            "request.evidenceTemplate.confirmedRecordRequired must be true"
        )
    if template["unconfirmedEvidenceAllowed"] is not False:
        raise ValueError(
            "request.evidenceTemplate.unconfirmedEvidenceAllowed must be false"
        )
    return cast(AtomicConsumptionRequest, copy.deepcopy(request))


def _validate_initial_entry(value: object) -> FakeRegistryEntry:
    entry = _require_exact_mapping(
        value,
        FAKE_REGISTRY_ENTRY_FIELDS,
        "initial_state entry",
    )
    _require_uuid_v4_lowercase(entry["requestId"], "entry.requestId")
    _require_nonce(entry["authorizationNonce"], "entry.authorizationNonce")
    _require_sha256(entry["planFingerprint"], "entry.planFingerprint")
    _require_actor_id(entry["actorId"], "entry.actorId")
    _require_purpose(entry["purpose"], "entry.purpose")
    _parse_utc_rfc3339_seconds(entry["expiresAtUtc"], "entry.expiresAtUtc")
    if entry["state"] not in ("unused", "consumed"):
        raise ValueError("entry.state must be unused or consumed")
    if entry["state"] == "unused":
        if entry["consumptionRecord"] is not None:
            raise ValueError("unused entry must have null consumptionRecord")
    else:
        record = _validate_confirmed_record(
            entry["consumptionRecord"],
            "entry.consumptionRecord",
        )
        for field in (
            "requestId",
            "authorizationNonce",
            "planFingerprint",
            "actorId",
            "purpose",
        ):
            if record[field] != entry[field]:
                raise ValueError(
                    f"entry.consumptionRecord.{field} must equal entry.{field}"
                )
        entry = copy.deepcopy(entry)
        entry["consumptionRecord"] = record
    return cast(FakeRegistryEntry, copy.deepcopy(entry))


def _validate_simulation_directive(
    value: object,
) -> FakeSimulationDirective:
    directive = _require_exact_mapping(
        value,
        SIMULATION_DIRECTIVE_FIELDS,
        "simulation directive",
    )
    _require_uuid_v4_lowercase(
        directive["operationId"],
        "simulation directive.operationId",
    )
    if directive["phase"] not in (
        "operation",
        "connect",
        "statement",
        "lock",
        "commit",
    ):
        raise ValueError("simulation directive.phase is invalid")
    if directive["resultKind"] not in (
        "adapter_unavailable",
        "atomicity_unavailable",
        "commit_ambiguous",
        "operation_failed",
    ):
        raise ValueError("simulation directive.resultKind is invalid")
    if type(directive["commitVisibleToReconciliation"]) is not bool:
        raise ValueError(
            "simulation directive.commitVisibleToReconciliation must be bool"
        )
    if (
        directive["commitVisibleToReconciliation"] is True
        and directive["resultKind"] != "commit_ambiguous"
    ):
        raise ValueError(
            "commit visibility is allowed only for commit_ambiguous"
        )
    return cast(FakeSimulationDirective, copy.deepcopy(directive))


def _canonical_fingerprint(value: object) -> str:
    encoded = json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _build_evidence(
    record: ConfirmedConsumptionRecord,
) -> ConsumptionEvidence:
    if record["confirmed"] is not True:
        raise ValueError("Evidence requires a confirmed consumption record")
    evidence: ConsumptionEvidence = {
        "evidenceVersion": 1,
        "operationId": record["operationId"],
        "requestId": record["requestId"],
        "authorizationNonceFingerprint": hashlib.sha256(
            record["authorizationNonce"].encode("utf-8")
        ).hexdigest(),
        "planFingerprint": record["planFingerprint"],
        "actorId": record["actorId"],
        "purpose": record["purpose"],
        "consumedAtUtc": record["consumedAtUtc"],
        "recordFingerprint": _canonical_fingerprint(record),
        "singleUse": True,
        "status": CONSUMED_STATUS,
        "executionGrant": False,
    }
    return evidence


def _build_confirmed_record(
    request: AtomicConsumptionRequest,
    consumed_at_utc: str,
) -> ConfirmedConsumptionRecord:
    return {
        "recordVersion": 1,
        "operationId": request["operationId"],
        "requestId": request["requestId"],
        "authorizationNonce": request["authorizationNonce"],
        "planFingerprint": request["planFingerprint"],
        "actorId": request["actorId"],
        "purpose": request["purpose"],
        "expectedState": "unused",
        "desiredState": "consumed",
        "confirmed": True,
        "consumedAtUtc": consumed_at_utc,
    }


def _build_atomic_result(
    result_kind: str,
    operation_id: str,
    record: ConfirmedConsumptionRecord | None = None,
) -> AtomicConsumptionResult:
    definitions = {
        "committed": (
            "authorization_consumed_execution_locked",
            "authorization_consumption_committed",
            "confirmed_consumed",
            False,
        ),
        "already_consumed": (
            "authorization_consumption_blocked_execution_locked",
            "authorization_consumption_already_consumed",
            "confirmed_already_consumed",
            False,
        ),
        "parallel_conflict": (
            "authorization_consumption_blocked_execution_locked",
            "authorization_consumption_parallel_conflict",
            "not_consumed_by_operation",
            False,
        ),
        "binding_conflict": (
            "authorization_consumption_blocked_execution_locked",
            "authorization_consumption_binding_conflict",
            "not_consumed_by_operation",
            False,
        ),
        "expired": (
            "authorization_consumption_blocked_execution_locked",
            "authorization_consumption_expired",
            "not_consumed_by_operation",
            False,
        ),
        "adapter_unavailable": (
            "authorization_consumption_blocked_execution_locked",
            "authorization_consumption_adapter_unavailable",
            "not_consumed_by_operation",
            False,
        ),
        "atomicity_unavailable": (
            "authorization_consumption_blocked_execution_locked",
            "authorization_consumption_atomicity_unavailable",
            "not_consumed_by_operation",
            False,
        ),
        "commit_ambiguous": (
            "authorization_consumption_reconciliation_required_execution_locked",
            "authorization_consumption_commit_ambiguous",
            "unknown",
            True,
        ),
        "operation_failed": (
            "authorization_consumption_blocked_execution_locked",
            "authorization_consumption_operation_failed",
            "not_consumed_by_operation",
            False,
        ),
    }
    if result_kind not in definitions:
        raise ValueError("Unknown atomic consumption result kind")
    status, reason, consumption_status, reconciliation_required = definitions[
        result_kind
    ]
    result: dict[str, object] = {
        "status": status,
        "reason": reason,
        "resultKind": result_kind,
        "operationId": operation_id,
        "consumptionStatus": consumption_status,
        "reconciliationRequired": reconciliation_required,
        "retryAllowed": False,
        "executionGrant": False,
    }
    if result_kind == "committed":
        if record is None or record["confirmed"] is not True:
            raise ValueError("committed result requires a confirmed record")
        result["consumptionRecord"] = copy.deepcopy(record)
        result["evidence"] = _build_evidence(record)
    elif record is not None:
        raise ValueError("Only committed may contain a record")
    return cast(AtomicConsumptionResult, result)


def _build_reconciliation_result(
    reconciliation_kind: str,
    operation_id: str,
    record: ConfirmedConsumptionRecord | None = None,
) -> ReconciliationResult:
    definitions = {
        "confirmed": (
            "authorization_consumption_reconciliation_confirmed_execution_locked",
            "authorization_consumption_reconciliation_confirmed",
            "confirmed_consumed",
        ),
        "not_found": (
            "authorization_consumption_reconciliation_not_found_execution_locked",
            "authorization_consumption_reconciliation_not_found",
            "unknown",
        ),
        "ambiguous": (
            "authorization_consumption_reconciliation_ambiguous_execution_locked",
            "authorization_consumption_reconciliation_ambiguous",
            "unknown",
        ),
    }
    if reconciliation_kind not in definitions:
        raise ValueError("Unknown reconciliation kind")
    status, reason, consumption_status = definitions[reconciliation_kind]
    result: dict[str, object] = {
        "status": status,
        "reason": reason,
        "reconciliationKind": reconciliation_kind,
        "operationId": operation_id,
        "consumptionStatus": consumption_status,
        "writePerformed": False,
        "retryPerformed": False,
        "executionGrant": False,
    }
    if reconciliation_kind == "confirmed":
        if record is None or record["confirmed"] is not True:
            raise ValueError("confirmed reconciliation requires a record")
        result["consumptionRecord"] = copy.deepcopy(record)
        result["evidence"] = _build_evidence(record)
    elif record is not None:
        raise ValueError("Only confirmed reconciliation may contain a record")
    return cast(ReconciliationResult, result)


class _LocalFakeAtomicConsumptionRegistryDriver:
    def __init__(
        self,
        *,
        initial_state: tuple[FakeRegistryEntry, ...],
        simulation_directives: tuple[FakeSimulationDirective, ...],
        clock: InjectedUtcClock,
    ) -> None:
        if type(initial_state) is not tuple:
            raise ValueError("initial_state must be an exact tuple")
        if type(simulation_directives) is not tuple:
            raise ValueError("simulation_directives must be an exact tuple")
        clock_operation = getattr(clock, "now_utc", None)
        if not callable(clock_operation):
            raise ValueError("clock must provide callable now_utc")

        self._clock = clock
        self._lock = threading.Lock()
        self._entries: dict[RegistryIdentity, FakeRegistryEntry] = {}
        self._operation_bindings: dict[str, RegistryIdentity] = {}
        self._confirmed_records_by_operation_id: dict[
            str,
            ConfirmedConsumptionRecord,
        ] = {}
        self._ambiguous_operation_ids: set[str] = set()
        self._terminal_results_by_operation_id: dict[
            str,
            AtomicConsumptionResult,
        ] = {}
        self._directives_by_operation_id: dict[
            str,
            FakeSimulationDirective,
        ] = {}

        for raw_entry in initial_state:
            entry = _validate_initial_entry(raw_entry)
            identity = _registry_identity_from_values(
                entry["requestId"],
                entry["authorizationNonce"],
                entry["planFingerprint"],
                entry["actorId"],
                entry["purpose"],
            )
            if identity in self._entries:
                raise ValueError("initial_state contains duplicate registry identity")
            self._entries[identity] = entry
            record = entry["consumptionRecord"]
            if record is not None:
                operation_id = record["operationId"]
                if operation_id in self._operation_bindings:
                    raise ValueError(
                        "initial_state contains duplicate operationId"
                    )
                self._operation_bindings[operation_id] = identity
                self._confirmed_records_by_operation_id[operation_id] = (
                    copy.deepcopy(record)
                )

        for raw_directive in simulation_directives:
            directive = _validate_simulation_directive(raw_directive)
            operation_id = directive["operationId"]
            if operation_id in self._directives_by_operation_id:
                raise ValueError(
                    "simulation_directives contains duplicate operationId"
                )
            if operation_id in self._operation_bindings:
                raise ValueError(
                    "simulation directive targets a confirmed operationId"
                )
            self._directives_by_operation_id[operation_id] = directive

    def _remember_terminal_result(
        self,
        operation_id: str,
        identity: RegistryIdentity,
        result: AtomicConsumptionResult,
    ) -> AtomicConsumptionResult:
        self._operation_bindings[operation_id] = identity
        self._terminal_results_by_operation_id[operation_id] = copy.deepcopy(
            result
        )
        return copy.deepcopy(result)

    def _commit_consumption(
        self,
        request: AtomicConsumptionRequest,
        entry: FakeRegistryEntry,
        identity: RegistryIdentity,
    ) -> ConfirmedConsumptionRecord:
        consumed_at_utc = _format_injected_utc(self._clock.now_utc())
        expires_at = _parse_utc_rfc3339_seconds(
            entry["expiresAtUtc"],
            "entry.expiresAtUtc",
        )
        consumed_at = _parse_utc_rfc3339_seconds(
            consumed_at_utc,
            "consumedAtUtc",
        )
        if consumed_at >= expires_at:
            raise _ExpiredConsumption

        record = _build_confirmed_record(request, consumed_at_utc)
        updated_entry = copy.deepcopy(entry)
        updated_entry["state"] = "consumed"
        updated_entry["consumptionRecord"] = copy.deepcopy(record)
        self._entries[identity] = cast(FakeRegistryEntry, updated_entry)
        self._operation_bindings[request["operationId"]] = identity
        self._confirmed_records_by_operation_id[request["operationId"]] = (
            copy.deepcopy(record)
        )
        return record

    def compare_and_set_with_consumption_record(
        self,
        request: AtomicConsumptionRequest,
    ) -> AtomicConsumptionResult:
        normalized_request = _validate_request(request)
        operation_id = normalized_request["operationId"]
        identity = _registry_identity_from_request(normalized_request)

        if not self._lock.acquire(blocking=False):
            return _build_atomic_result("parallel_conflict", operation_id)

        try:
            existing_binding = self._operation_bindings.get(operation_id)
            if existing_binding is not None and existing_binding != identity:
                return _build_atomic_result("binding_conflict", operation_id)
            if operation_id in self._confirmed_records_by_operation_id:
                return _build_atomic_result("already_consumed", operation_id)
            previous_terminal = self._terminal_results_by_operation_id.get(
                operation_id
            )
            if previous_terminal is not None:
                return copy.deepcopy(previous_terminal)

            entry = self._entries.get(identity)
            if entry is None:
                return self._remember_terminal_result(
                    operation_id,
                    identity,
                    _build_atomic_result("binding_conflict", operation_id),
                )
            if entry["state"] == "consumed":
                return self._remember_terminal_result(
                    operation_id,
                    identity,
                    _build_atomic_result("already_consumed", operation_id),
                )

            directive = self._directives_by_operation_id.pop(
                operation_id,
                None,
            )
            if directive is not None and directive["resultKind"] != (
                "commit_ambiguous"
            ):
                return self._remember_terminal_result(
                    operation_id,
                    identity,
                    _build_atomic_result(
                        directive["resultKind"],
                        operation_id,
                    ),
                )
            if (
                directive is not None
                and directive["commitVisibleToReconciliation"] is False
            ):
                self._operation_bindings[operation_id] = identity
                self._ambiguous_operation_ids.add(operation_id)
                return self._remember_terminal_result(
                    operation_id,
                    identity,
                    _build_atomic_result("commit_ambiguous", operation_id),
                )

            try:
                record = self._commit_consumption(
                    normalized_request,
                    entry,
                    identity,
                )
            except _ExpiredConsumption:
                return self._remember_terminal_result(
                    operation_id,
                    identity,
                    _build_atomic_result("expired", operation_id),
                )

            if directive is not None:
                ambiguous_result = _build_atomic_result(
                    "commit_ambiguous",
                    operation_id,
                )
                self._terminal_results_by_operation_id[operation_id] = (
                    copy.deepcopy(ambiguous_result)
                )
                return ambiguous_result
            return _build_atomic_result(
                "committed",
                operation_id,
                record,
            )
        finally:
            self._lock.release()

    def read_consumption_by_operation_id(
        self,
        operation_id: str,
    ) -> ReconciliationResult:
        normalized_operation_id = _require_uuid_v4_lowercase(
            operation_id,
            "operation_id",
        )
        with self._lock:
            record = self._confirmed_records_by_operation_id.get(
                normalized_operation_id
            )
            if record is not None:
                return _build_reconciliation_result(
                    "confirmed",
                    normalized_operation_id,
                    record,
                )
            if normalized_operation_id in self._ambiguous_operation_ids:
                return _build_reconciliation_result(
                    "ambiguous",
                    normalized_operation_id,
                )
            return _build_reconciliation_result(
                "not_found",
                normalized_operation_id,
            )


class _ExpiredConsumption(Exception):
    pass


def build_local_fake_atomic_consumption_registry_driver(
    *,
    initial_state: tuple[FakeRegistryEntry, ...],
    simulation_directives: tuple[FakeSimulationDirective, ...],
    clock: InjectedUtcClock,
) -> LocalFakeAtomicConsumptionRegistryDriver:
    return _LocalFakeAtomicConsumptionRegistryDriver(
        initial_state=initial_state,
        simulation_directives=simulation_directives,
        clock=clock,
    )
