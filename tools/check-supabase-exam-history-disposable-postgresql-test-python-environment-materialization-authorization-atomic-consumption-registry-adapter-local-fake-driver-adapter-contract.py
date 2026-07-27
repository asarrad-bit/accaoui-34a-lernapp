#!/usr/bin/env python3
"""Prüft den vollständig gesperrten lokalen Adapter-Verhaltensvertrag v27.34e."""

from __future__ import annotations

import ast
import copy
import hashlib
import json
from pathlib import Path
from typing import Any, Iterator


ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / (
    "docs/contracts/"
    "exam-history-disposable-postgresql-test-python-environment-"
    "materialization-authorization-atomic-consumption-registry-adapter-"
    "local-fake-driver-adapter-contract.json"
)
DOCUMENT_PATH = ROOT / (
    "docs/"
    "SUPABASE_EXAM_RESULT_HISTORY_DISPOSABLE_POSTGRESQL_TEST_PYTHON_"
    "ENVIRONMENT_MATERIALIZATION_AUTHORIZATION_ATOMIC_CONSUMPTION_"
    "REGISTRY_ADAPTER_LOCAL_FAKE_DRIVER_ADAPTER_CONTRACT.md"
)
SOURCE_CONTRACT_PATH = ROOT / (
    "docs/contracts/"
    "exam-history-disposable-postgresql-test-python-environment-"
    "materialization-authorization-atomic-consumption-registry-adapter-"
    "local-fake-driver-interface-contract.json"
)
FAKE_DRIVER_PATH = ROOT / (
    "tools/accaoui_disposable_test_python_environment_materialization_"
    "authorization_atomic_consumption_registry_local_fake_driver.py"
)
ADAPTER_MODULE_PATH = ROOT / (
    "tools/accaoui_disposable_test_python_environment_materialization_"
    "authorization_atomic_consumption_registry_adapter.py"
)
MASTERLIST_PATH = ROOT / "docs/PROJECT_MASTERLIST.md"
STATE_PATH = ROOT / "docs/PROJECT_STATE_CURRENT.md"
TASK_PATH = ROOT / "docs/tasks/CURRENT_TASK.md"
DATABASE_PLAN_PATH = ROOT / "docs/SUPABASE_EXAM_QUESTION_DATABASE_PLAN.md"
CONTINUITY_CHECKER_PATH = ROOT / "tools/check-project-continuity-control.py"
PREFLIGHT_PATH = ROOT / "tools/preflight.py"

CHECKER_RELATIVE_PATH = (
    "tools/check-supabase-exam-history-disposable-postgresql-test-python-"
    "environment-materialization-authorization-atomic-consumption-registry-"
    "adapter-local-fake-driver-adapter-contract.py"
)

HISTORICAL_MASTERLIST_TABLE_ENTRY_MARKER = "| v27.34e |"
HISTORICAL_MASTERLIST_SECTION_MARKER = (
    "### Vollständig gesperrter lokaler Adapter-Verhaltensvertrag v27.34e"
)

FORBIDDEN_CURRENT_TASK_ACCESS_PHRASES = (
    "Registryzugriff: ja",
    "Datenbankzugriff: ja",
    "SQL-Zugriff: ja",
    "Supabase-Zugriff: ja",
    "Netzwerkzugriff: ja",
    "authorizationGrant",
    "authorizationToken",
    "executionGrant",
)

EXPECTED_CONTRACT_FILE_SHA256 = (
    "5faca9b213ef4018d0ef00a42aa75c3f6ea1fb91a0609b46fb031f7a596fa2f8"
)
EXPECTED_CONTRACT_CANONICAL_SHA256 = (
    "c7828d913b68c55638f6c7ebb9c0aa748b7e2f89da754eac98cb5e31f128ddfd"
)
EXPECTED_PREDECESSOR_SHA = "84729c58c5fcb61b7f7ad72d1d695ee2d7095b86"

EXPECTED_BOUND_FILE_HASHES = {
    (
        "docs/SUPABASE_EXAM_RESULT_HISTORY_DISPOSABLE_POSTGRESQL_TEST_"
        "PYTHON_ENVIRONMENT_MATERIALIZATION_AUTHORIZATION_ATOMIC_"
        "CONSUMPTION_REGISTRY_ADAPTER_LOCAL_FAKE_DRIVER_INTERFACE_CONTRACT.md"
    ): "67f6f24da7aab04e00a90da129e3b4884eebe5c4963ee4184f8b9fd2b4ffa547",
    (
        "docs/contracts/exam-history-disposable-postgresql-test-python-"
        "environment-materialization-authorization-atomic-consumption-"
        "registry-adapter-local-fake-driver-interface-contract.json"
    ): "77d2528a4e46d69fecec9f40499f19aaedcca167e27a4b949915cff253adee6c",
    (
        "docs/SUPABASE_EXAM_RESULT_HISTORY_DISPOSABLE_POSTGRESQL_TEST_"
        "PYTHON_ENVIRONMENT_MATERIALIZATION_AUTHORIZATION_ATOMIC_"
        "CONSUMPTION_REGISTRY_ADAPTER_LOCAL_FAKE_DRIVER.md"
    ): "2d225021a0cf270cc6338055ff678495dc50f674bcb1be5a3215d16519d43e4a",
    (
        "tools/accaoui_disposable_test_python_environment_materialization_"
        "authorization_atomic_consumption_registry_local_fake_driver.py"
    ): "49a229332edc4c60a69f3356b35e18a79ba926e7512b9b1d82f849c2daf3793c",
    (
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-"
        "environment-materialization-authorization-atomic-consumption-"
        "registry-adapter-local-fake-driver-interface-contract.py"
    ): "55c87ecaa044219c3f09256cff0026ecee2f0ad1bd125293e427a731eb440506",
    (
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-"
        "environment-materialization-authorization-atomic-consumption-"
        "registry-adapter-local-fake-driver.py"
    ): "e7b6b9c9b8e62f6a7eafdaa7d1dc1c0a263788afab58d1a6637569fc92b09965",
}

EXPECTED_INTERFACE_SECTION_HASHES = {
    "pythonInterfaceBoundarySha256": (
        "0df1618f11f9d96fe12d82a3f200aee66f0d74fbf0c99bf8c403ada47a5eeed9"
    ),
    "inputBoundarySha256": (
        "0b3675d7e154e7325fe3da9ccf72ba4d4eecfc5536f142f035b9852cc38ab6cf"
    ),
    "resultBoundarySha256": (
        "1242675e3864291ef4c6ef61f446dc47d95d5173f2591a486977ef6ffea64819"
    ),
    "reconciliationBoundarySha256": (
        "7537275e8241b6b883626fe86cbcb97d1f599f10b7bfd33baa21214cf72db08e"
    ),
    "timeoutBoundarySha256": (
        "dafb9e7fd54399c9c7609c50c53b25a5b3afa2f35deae39a2f48218a62f0d917"
    ),
    "fakeDriverBoundarySha256": (
        "492b4c1659462076941aafae3321d5bb559a32c2c3398c93a1bb3c5a7d18236e"
    ),
    "sourceTypesProtocolsAndFactorySha256": (
        "bcbfb90b18cc4b835c82b9d32a0c693defcf0606a0694b634b04328c114b4e8e"
    ),
}

EXPECTED_HISTORICAL_HASHES = {
    (
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-"
        "environment-materialization-authorization-atomic-consumption-"
        "operation-contract.py"
    ): "05b84b72ca36c08cf08e2396804206eadccb6bdc73375ddecad2b8f04184107e",
    (
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-"
        "environment-materialization-authorization-atomic-consumption-"
        "registry-adapter-contract.py"
    ): "0c07b87e6268060af97dd0c0da3b56032fa45d8572e6b64c176ec64fadbeecdb",
    (
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-"
        "environment-materialization-authorization-atomic-consumption-"
        "registry-adapter-descriptor.py"
    ): "ba39cd9c95b9a938353a20cb70bf5ba7aff4f99ceb2a83938f83132bac067b53",
    (
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-"
        "environment-materialization-authorization-atomic-consumption-"
        "registry-adapter-descriptor-acceptance-guard.py"
    ): "39b92bb060ca5eff19fdaaa1092f38deb8faf5341af1736e6ce27dfb687754fd",
    (
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-"
        "environment-materialization-authorization-atomic-consumption-"
        "registry-adapter-execution-plan-acceptance-guard.py"
    ): "23c99f68439facbc8a7b03866ff1e16a9793561609ebe3a21e2b5fc431ac41d8",
    (
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-"
        "environment-materialization-authorization-atomic-consumption-"
        "registry-adapter-implementation-contract.py"
    ): "7b7e431398d6be0f1712123ae747fd2857b6d1a10079633cd2f58e5eb1ad99bb",
    (
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-"
        "environment-materialization-authorization-atomic-consumption-"
        "registry-adapter-implementation-descriptor.py"
    ): "5e265167f1bddac5274b5f64d004ae51a59acad78457d3ab074a3a698f85bf44",
    (
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-"
        "environment-materialization-authorization-atomic-consumption-"
        "registry-adapter-implementation-descriptor-acceptance-guard.py"
    ): "8977efc0d680d4adde00e1aeff241ba029cfe6237ff6f20ea0ea476392fc1fc6",
    (
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-"
        "environment-materialization-authorization-atomic-consumption-"
        "registry-adapter-implementation-execution-authorization-contract.py"
    ): "63beafe77e83086bcca69b1869599cd6b66ee3af364a71cb047044eca1fd9601",
    (
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-"
        "environment-materialization-authorization-atomic-consumption-"
        "registry-adapter-implementation-execution-authorization-descriptor.py"
    ): "6865a8db332a936c18d93caaafb7a4d66312ec3f49d2130e685c669c0ca9aa87",
    (
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-"
        "environment-materialization-authorization-atomic-consumption-"
        "registry-adapter-implementation-execution-authorization-descriptor-"
        "acceptance-guard.py"
    ): "c2fedeb03c196d8d76dbbb7bf5f7d28bdf9d2eaa33d0291604d6e28c8ee15ed4",
    (
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-"
        "environment-materialization-authorization-atomic-consumption-"
        "registry-adapter-implementation-execution-authorization-readiness.py"
    ): "b91f521e55e76cbdebf9b0132c229f6d84b6fbcb508ae7de099fe07e299194ea",
    (
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-"
        "environment-materialization-authorization-atomic-consumption-"
        "registry-adapter-implementation-execution-authorization-readiness-"
        "acceptance-guard.py"
    ): "4cb6b18658c2566d621b47dd116aed351240c062ae5326ecf1841fd0ac535fdd",
    (
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-"
        "environment-materialization-authorization-atomic-consumption-"
        "registry-adapter-implementation-execution-contract.py"
    ): "8db240d43c307a6df61b025b0b354c4279ef78f0d8306f149bea48e204b5500d",
    (
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-"
        "environment-materialization-authorization-atomic-consumption-"
        "registry-adapter-implementation-execution-descriptor.py"
    ): "1d94be5d04fcf82258f9781a13da4efb251b495b3b767b74ae48a3fde50320da",
    (
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-"
        "environment-materialization-authorization-atomic-consumption-"
        "registry-adapter-implementation-execution-descriptor-acceptance-"
        "guard.py"
    ): "599f9fbbff4631de7bff37427d4bc0eed37b3b747529e532af4b8302010cad67",
    (
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-"
        "environment-materialization-authorization-atomic-consumption-"
        "registry-adapter-implementation-execution-plan.py"
    ): "b04d8863bf8e87f4b02bbab8f22cf273e389eb151d47ea86d2cbd754f8389df2",
    (
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-"
        "environment-materialization-authorization-atomic-consumption-"
        "registry-adapter-implementation-execution-plan-acceptance-guard.py"
    ): "fcdf51eeb90ba7cdc667a8e790aedee6017482421f1fb1166a048b5fb4205037",
    (
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-"
        "environment-materialization-authorization-atomic-consumption-"
        "registry-adapter-implementation-execution-readiness.py"
    ): "a5ad4b5fce4ed33d76981fa09f3a415e2d2a7a72e777819b760d2fb73bd30709",
    (
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-"
        "environment-materialization-authorization-atomic-consumption-"
        "registry-adapter-implementation-execution-readiness-acceptance-"
        "guard.py"
    ): "866a5e323f5f6560c1a15db4674e2d5513fa0326104152630513911d578ce03b",
    (
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-"
        "environment-materialization-authorization-atomic-consumption-"
        "registry-adapter-implementation-plan.py"
    ): "e650afedeb5fbf2103610d8ede358613b4480343067aa941d8f2c2a50809dc27",
    (
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-"
        "environment-materialization-authorization-atomic-consumption-"
        "registry-adapter-implementation-plan-acceptance-guard.py"
    ): "b027750ce3e7b6999b6527827f5689e106341c6f5b1d6d4f35c5b50e7b33bef7",
    (
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-"
        "environment-materialization-authorization-atomic-consumption-"
        "registry-adapter-implementation-readiness.py"
    ): "5ea9defd6b24d4432a33dfe16043882aa35af605a4d964177cf65185df18e826",
    (
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-"
        "environment-materialization-authorization-atomic-consumption-"
        "registry-adapter-implementation-readiness-acceptance-guard.py"
    ): "6c54941e8882e36cda88680e5a2a9eeb64fedd979ca9c7b2ab58e8b3cd49a6ca",
    (
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-"
        "environment-materialization-authorization-atomic-consumption-"
        "registry-adapter-local-fake-driver.py"
    ): "e7b6b9c9b8e62f6a7eafdaa7d1dc1c0a263788afab58d1a6637569fc92b09965",
    (
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-"
        "environment-materialization-authorization-atomic-consumption-"
        "registry-adapter-local-fake-driver-interface-contract.py"
    ): "55c87ecaa044219c3f09256cff0026ecee2f0ad1bd125293e427a731eb440506",
    (
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-"
        "environment-materialization-authorization-atomic-consumption-"
        "registry-adapter-readiness.py"
    ): "3dd15d35e706f5a9013dc5f550b04f589b720681e6c14df36d2e4ddc488fd5e0",
    (
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-"
        "environment-materialization-authorization-atomic-consumption-"
        "registry-adapter-readiness-acceptance-guard.py"
    ): "e2c8ddee2dd4967790e8654113cbf4a7e5bb5c590f20130fa421fa9cb3786209",
}

EXPECTED_TOP_LEVEL_KEYS = (
    "version",
    "contractVersion",
    "status",
    "productiveReleaseAllowed",
    "sourceBoundary",
    "adapterDefinitionBoundary",
    "factoryBoundary",
    "atomicOperationBoundary",
    "atomicExceptionBoundary",
    "reconciliationBoundary",
    "resultValidationBoundary",
    "timeoutBoundary",
    "importBoundary",
    "historicalCheckerInventoryBoundary",
    "implementationBoundary",
    "securityBoundary",
    "futureBoundary",
)

EXPECTED_ATOMIC_KINDS = (
    "committed",
    "already_consumed",
    "parallel_conflict",
    "binding_conflict",
    "expired",
    "adapter_unavailable",
    "atomicity_unavailable",
    "commit_ambiguous",
    "operation_failed",
)
EXPECTED_RECONCILIATION_KINDS = ("confirmed", "not_found", "ambiguous")


class ValidationError(RuntimeError):
    """Der v27.34e-Verhaltensvertrag ist verletzt."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def canonical_sha256(value: Any) -> str:
    encoded = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return sha256_bytes(encoded)


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValidationError(f"Doppelter JSON-Schlüssel: {key}")
        result[key] = value
    return result


def parse_json_strict(raw: bytes, label: str) -> dict[str, Any]:
    require(not raw.startswith(b"\xef\xbb\xbf"), f"{label}: UTF-8-BOM unzulässig")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValidationError(f"{label}: ungültiges UTF-8: {exc}") from exc
    require(text.endswith("\n"), f"{label}: abschließender Zeilenumbruch fehlt")
    try:
        value = json.loads(text, object_pairs_hook=strict_object)
    except json.JSONDecodeError as exc:
        raise ValidationError(f"{label}: ungültiges JSON: {exc}") from exc
    require(type(value) is dict, f"{label}: oberste Ebene muss ein Objekt sein")
    return value


def read_text(path: Path, label: str) -> str:
    require(path.is_file(), f"{label} fehlt: {path.relative_to(ROOT).as_posix()}")
    raw = path.read_bytes()
    require(not raw.startswith(b"\xef\xbb\xbf"), f"{label}: UTF-8-BOM unzulässig")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValidationError(f"{label}: ungültiges UTF-8: {exc}") from exc
    require(text.endswith("\n"), f"{label}: abschließender Zeilenumbruch fehlt")
    return text


def validate_contract_fingerprint(contract: dict[str, Any]) -> None:
    require(
        canonical_sha256(contract) == EXPECTED_CONTRACT_CANONICAL_SHA256,
        "Kanonischer Vertragsfingerprint ist ungültig",
    )


def validate_bound_sources(contract: dict[str, Any]) -> dict[str, Any]:
    source = contract["sourceBoundary"]
    require(
        source["requiredPredecessorCommit"] == EXPECTED_PREDECESSOR_SHA,
        "v27.34d-Ausgangscommit ist nicht kanonisch gebunden",
    )
    contract_files = {
        entry["path"]: entry["sha256"] for entry in source["boundFiles"]
    }
    require(
        contract_files == EXPECTED_BOUND_FILE_HASHES,
        "Gebundene v27.34a-/v27.34b-Quelldateien sind nicht exakt",
    )
    for relative_path, expected_hash in EXPECTED_BOUND_FILE_HASHES.items():
        path = ROOT / relative_path
        require(path.is_file(), f"Gebundene Quelldatei fehlt: {relative_path}")
        require(
            sha256_bytes(path.read_bytes()) == expected_hash,
            f"Gebundene Quelldatei verändert: {relative_path}",
        )

    source_contract_raw = SOURCE_CONTRACT_PATH.read_bytes()
    source_contract = parse_json_strict(
        source_contract_raw,
        "v27.34a-Schnittstellenvertrag",
    )
    section_values = {
        "pythonInterfaceBoundarySha256": source_contract[
            "pythonInterfaceBoundary"
        ],
        "inputBoundarySha256": source_contract["inputBoundary"],
        "resultBoundarySha256": source_contract["resultBoundary"],
        "reconciliationBoundarySha256": source_contract[
            "reconciliationBoundary"
        ],
        "timeoutBoundarySha256": source_contract["timeoutBoundary"],
        "fakeDriverBoundarySha256": source_contract["fakeDriverBoundary"],
        "sourceTypesProtocolsAndFactorySha256": {
            "exactTypeNames": source_contract["pythonInterfaceBoundary"][
                "exactTypeNames"
            ],
            "fakeDriverProtocol": source_contract["pythonInterfaceBoundary"][
                "fakeDriverProtocol"
            ],
            "fakeDriverFactory": source_contract["pythonInterfaceBoundary"][
                "fakeDriverFactory"
            ],
            "driverAtomicOperation": source_contract[
                "pythonInterfaceBoundary"
            ]["driverAtomicOperation"],
            "driverReconciliationOperation": source_contract[
                "pythonInterfaceBoundary"
            ]["driverReconciliationOperation"],
        },
    }
    actual_section_hashes = {
        key: canonical_sha256(value) for key, value in section_values.items()
    }
    require(
        actual_section_hashes == EXPECTED_INTERFACE_SECTION_HASHES,
        "Kanonische v27.34a-Schnittstellenabschnitte wurden verändert",
    )
    require(
        source["boundInterfaceSections"] == EXPECTED_INTERFACE_SECTION_HASHES,
        "Vertrag bindet nicht alle kanonischen v27.34a-Abschnitte",
    )
    return source_contract


def _defined_names(tree: ast.Module) -> set[str]:
    names: set[str] = set()
    for node in tree.body:
        if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            names.add(node.name)
        elif isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            for target in targets:
                if isinstance(target, ast.Name):
                    names.add(target.id)
    return names


def _find_class(tree: ast.Module, name: str) -> ast.ClassDef:
    matches = [
        node
        for node in tree.body
        if isinstance(node, ast.ClassDef) and node.name == name
    ]
    require(len(matches) == 1, f"Quellklasse muss exakt einmal existieren: {name}")
    return matches[0]


def _find_function(tree: ast.Module, name: str) -> ast.FunctionDef:
    matches = [
        node
        for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name == name
    ]
    require(
        len(matches) == 1,
        f"Quellfactory muss exakt einmal existieren: {name}",
    )
    return matches[0]


def _annotation(node: ast.expr | None) -> str:
    require(node is not None, "Erforderliche Typannotation fehlt")
    return ast.unparse(node)


def validate_fake_driver_definitions() -> None:
    source = read_text(FAKE_DRIVER_PATH, "v27.34b-Fake-Treibermodul")
    tree = ast.parse(source, filename=str(FAKE_DRIVER_PATH))
    names = _defined_names(tree)
    required_names = {
        "AtomicConsumptionRequest",
        "AtomicConsumptionResult",
        "ReconciliationResult",
        "LocalFakeAtomicConsumptionRegistryDriver",
        "_LocalFakeAtomicConsumptionRegistryDriver",
        "build_local_fake_atomic_consumption_registry_driver",
    }
    require(required_names <= names, "Gebundene v27.34b-Typen oder Factory fehlen")
    require(
        "AtomicConsumptionRegistryAdapter" not in names,
        "Adapter-Protocol wurde parallel im Fake-Treibermodul definiert",
    )

    protocol = _find_class(tree, "LocalFakeAtomicConsumptionRegistryDriver")
    require(
        [ast.unparse(base) for base in protocol.bases] == ["Protocol"],
        "Fake-Treiber-Protocol besitzt eine unerwartete Form",
    )
    methods = {
        node.name: node
        for node in protocol.body
        if isinstance(node, ast.FunctionDef)
    }
    require(
        set(methods) == {
            "compare_and_set_with_consumption_record",
            "read_consumption_by_operation_id",
        },
        "Fake-Treiber-Protocol besitzt unerwartete Operationen",
    )
    atomic_method = methods["compare_and_set_with_consumption_record"]
    require(
        [arg.arg for arg in atomic_method.args.args] == ["self", "request"],
        "Fake-Treiber-CAS-Signatur ist ungültig",
    )
    require(
        _annotation(atomic_method.args.args[1].annotation)
        == "AtomicConsumptionRequest",
        "Fake-Treiber-CAS-Requesttyp ist ungültig",
    )
    require(
        _annotation(atomic_method.returns) == "AtomicConsumptionResult",
        "Fake-Treiber-CAS-Rückgabetyp ist ungültig",
    )
    reconciliation_method = methods["read_consumption_by_operation_id"]
    require(
        [arg.arg for arg in reconciliation_method.args.args]
        == ["self", "operation_id"],
        "Fake-Treiber-Reconciliation-Signatur ist ungültig",
    )
    require(
        _annotation(reconciliation_method.args.args[1].annotation) == "str",
        "Fake-Treiber-Reconciliation-ID-Typ ist ungültig",
    )
    require(
        _annotation(reconciliation_method.returns) == "ReconciliationResult",
        "Fake-Treiber-Reconciliation-Rückgabetyp ist ungültig",
    )

    _find_class(tree, "_LocalFakeAtomicConsumptionRegistryDriver")
    factory = _find_function(
        tree,
        "build_local_fake_atomic_consumption_registry_driver",
    )
    require(not factory.args.args, "Fake-Treiber-Factory besitzt Positionsparameter")
    require(
        [arg.arg for arg in factory.args.kwonlyargs]
        == ["initial_state", "simulation_directives", "clock"],
        "Fake-Treiber-Factory besitzt falsche Keyword-Parameter",
    )
    require(
        factory.args.kw_defaults == [None, None, None],
        "Fake-Treiber-Factory besitzt unerlaubte Defaults",
    )
    require(
        [_annotation(arg.annotation) for arg in factory.args.kwonlyargs]
        == [
            "tuple[FakeRegistryEntry, ...]",
            "tuple[FakeSimulationDirective, ...]",
            "InjectedUtcClock",
        ],
        "Fake-Treiber-Factory besitzt falsche Parametertypen",
    )
    require(
        _annotation(factory.returns) == "LocalFakeAtomicConsumptionRegistryDriver",
        "Fake-Treiber-Factory besitzt falschen Rückgabetyp",
    )


def validate_result_bindings(
    contract: dict[str, Any],
    source_contract: dict[str, Any],
) -> None:
    boundary = contract["resultValidationBoundary"]
    atomic_source = source_contract["resultBoundary"]
    reconciliation_source = source_contract["reconciliationBoundary"]
    require(
        tuple(atomic_source["exactResultKinds"]) == EXPECTED_ATOMIC_KINDS,
        "v27.34a besitzt nicht exakt neun kanonische Ergebnisarten",
    )
    require(
        tuple(
            schema["resultKind"] for schema in atomic_source["resultSchemas"]
        )
        == EXPECTED_ATOMIC_KINDS,
        "v27.34a-Ergebnis-Schemafolge ist ungültig",
    )
    require(
        tuple(reconciliation_source["exactReconciliationKinds"])
        == EXPECTED_RECONCILIATION_KINDS,
        "v27.34a besitzt nicht exakt drei Reconciliation-Arten",
    )
    require(
        tuple(
            schema["reconciliationKind"]
            for schema in reconciliation_source["resultSchemas"]
        )
        == EXPECTED_RECONCILIATION_KINDS,
        "v27.34a-Reconciliation-Schemafolge ist ungültig",
    )
    require(
        tuple(boundary["exactAtomicResultKinds"]) == EXPECTED_ATOMIC_KINDS
        and boundary["exactAtomicResultKindCount"] == 9,
        "v27.34e bindet nicht exakt neun Ergebnisarten",
    )
    require(
        tuple(boundary["exactReconciliationKinds"])
        == EXPECTED_RECONCILIATION_KINDS
        and boundary["exactReconciliationKindCount"] == 3,
        "v27.34e bindet nicht exakt drei Reconciliation-Arten",
    )
    require(
        boundary["atomicCommonFieldOrder"]
        == atomic_source["commonRequiredFields"],
        "Atomare Ergebnisfeldreihenfolge weicht von v27.34a ab",
    )
    require(
        boundary["reconciliationCommonFieldOrder"]
        == reconciliation_source["commonRequiredFields"],
        "Reconciliation-Feldreihenfolge weicht von v27.34a ab",
    )
    for schema in atomic_source["resultSchemas"]:
        require(
            schema["retryAllowed"] is False
            and schema["executionGrant"] is False,
            f"Atomare Sicherheitsflags offen: {schema['resultKind']}",
        )
    for schema in reconciliation_source["resultSchemas"]:
        require(
            schema["retryPerformed"] is False
            and schema["writePerformed"] is False
            and schema["executionGrant"] is False,
            f"Reconciliation-Sicherheitsflags offen: {schema['reconciliationKind']}",
        )
    require(
        source_contract["evidenceBoundary"]["derivedOnlyFromConfirmedRecord"]
        is True,
        "Evidence ist nicht ausschließlich an bestätigten Record gebunden",
    )
    require(
        source_contract["consumptionRecordBoundary"][
            "compareAndSetAndConfirmedRecordSingleAtomicSectionRequired"
        ]
        is True,
        "Bestätigter Record ist nicht atomar gebunden",
    )


def validate_historical_inventory(contract: dict[str, Any]) -> None:
    boundary = contract["historicalCheckerInventoryBoundary"]
    require(boundary["expectedCheckerCount"] == 28, "Inventurzahl ist nicht 28")
    require(
        boundary[
            "eachCheckerInheritsHistoricalLockKindAndLaterConditionalSwitchRule"
        ]
        is True,
        "Sperrart und Umschaltregel gelten nicht für jeden Checker",
    )
    inventory = {
        entry["path"]: entry["sha256"] for entry in boundary["checkers"]
    }
    require(len(boundary["checkers"]) == 28, "Inventur enthält nicht 28 Einträge")
    require(len(inventory) == 28, "Inventur enthält doppelte Checkerpfade")
    require(
        inventory == EXPECTED_HISTORICAL_HASHES,
        "Historische Checker-Inventur ist nicht kanonisch",
    )

    future_adapter_guard = "if FUTURE_ADAPTER." + "exists():"
    direct_adapter_guard = "not ADAPTER_MODULE_PATH." + "exists()"
    discovered: set[str] = set()
    for path in (ROOT / "tools").glob("check-*.py"):
        text = path.read_text(encoding="utf-8")
        if (
            future_adapter_guard in text
            or direct_adapter_guard in text
        ):
            discovered.add(path.relative_to(ROOT).as_posix())
    require(
        discovered == set(EXPECTED_HISTORICAL_HASHES),
        "Ermittelte historische Sperrchecker weichen von der 28er-Inventur ab",
    )
    for relative_path, expected_hash in EXPECTED_HISTORICAL_HASHES.items():
        path = ROOT / relative_path
        require(path.is_file(), f"Historischer Checker fehlt: {relative_path}")
        require(
            sha256_bytes(path.read_bytes()) == expected_hash,
            f"Historischer Checker wurde verändert: {relative_path}",
        )


def validate_historical_masterlist_markers(masterlist: str) -> None:
    require(
        masterlist.count(HISTORICAL_MASTERLIST_TABLE_ENTRY_MARKER) == 1,
        "Masterliste: historischer v27.34e-Tabelleneintrag fehlt oder ist dupliziert",
    )
    require(
        masterlist.count(HISTORICAL_MASTERLIST_SECTION_MARKER) == 1,
        "Masterliste: historischer v27.34e-Abschnitt fehlt oder ist dupliziert",
    )


def must_reject_historical_masterlist_markers(candidate: str, label: str) -> None:
    try:
        validate_historical_masterlist_markers(candidate)
    except ValidationError:
        return
    raise ValidationError(f"Manipulation wurde nicht blockiert: {label}")


def run_historical_masterlist_manipulation_checks(masterlist: str) -> int:
    checks = 0
    must_reject_historical_masterlist_markers(
        masterlist.replace(HISTORICAL_MASTERLIST_TABLE_ENTRY_MARKER, "", 1),
        "historischer v27.34e-Tabelleneintrag entfernt",
    )
    checks += 1
    must_reject_historical_masterlist_markers(
        masterlist + "\n" + HISTORICAL_MASTERLIST_TABLE_ENTRY_MARKER + "\n",
        "historischer v27.34e-Tabelleneintrag dupliziert",
    )
    checks += 1
    must_reject_historical_masterlist_markers(
        masterlist.replace(HISTORICAL_MASTERLIST_SECTION_MARKER, "", 1),
        "historischer v27.34e-Abschnitt entfernt",
    )
    checks += 1
    must_reject_historical_masterlist_markers(
        masterlist + "\n" + HISTORICAL_MASTERLIST_SECTION_MARKER + "\n",
        "historischer v27.34e-Abschnitt dupliziert",
    )
    checks += 1
    return checks


def validate_current_task_safety_boundaries(task: str) -> None:
    require("Commit erlaubt: NEIN" in task, "CURRENT_TASK: Commit-Sperre fehlt")
    require("Push erlaubt: NEIN" in task, "CURRENT_TASK: Push-Sperre fehlt")
    adapter_relative_path = ADAPTER_MODULE_PATH.relative_to(ROOT).as_posix()
    require(
        adapter_relative_path not in task,
        "CURRENT_TASK: Adapterdatei ist als erlaubte Datei eingetragen",
    )
    for phrase in FORBIDDEN_CURRENT_TASK_ACCESS_PHRASES:
        require(
            phrase not in task,
            f"CURRENT_TASK: verbotene Freigabe eingetragen: {phrase}",
        )


def must_reject_current_task_safety_boundaries(candidate: str, label: str) -> None:
    try:
        validate_current_task_safety_boundaries(candidate)
    except ValidationError:
        return
    raise ValidationError(f"Manipulation wurde nicht blockiert: {label}")


def run_current_task_manipulation_checks(task: str) -> int:
    checks = 0
    must_reject_current_task_safety_boundaries(
        task.replace("Commit erlaubt: NEIN", "Commit erlaubt: JA", 1),
        "Commit erlaubt: JA",
    )
    checks += 1
    must_reject_current_task_safety_boundaries(
        task.replace("Push erlaubt: NEIN", "Push erlaubt: JA", 1),
        "Push erlaubt: JA",
    )
    checks += 1
    adapter_relative_path = ADAPTER_MODULE_PATH.relative_to(ROOT).as_posix()
    must_reject_current_task_safety_boundaries(
        task + "\n- `" + adapter_relative_path + "`\n",
        "Adapterdatei als erlaubte Datei eingetragen",
    )
    checks += 1
    for phrase in FORBIDDEN_CURRENT_TASK_ACCESS_PHRASES:
        must_reject_current_task_safety_boundaries(
            task + "\n" + phrase + "\n",
            f"verbotene Freigabe eingetragen: {phrase}",
        )
        checks += 1
    return checks


def validate_project_documents() -> int:
    document = read_text(DOCUMENT_PATH, "v27.34e-Vertragsdokumentation")
    document_markers = (
        "Stand: v27.34e",
        "Dieser Schritt erstellt, importiert, instanziiert und verwendet keinen",
        "`_LocalFakeAtomicConsumptionRegistryAdapter`",
        "type(driver) is _LocalFakeAtomicConsumptionRegistryDriver",
        "defensive `deepcopy`",
        "authorization_consumption_operation_failed",
        "operation_id must be a canonical lowercase UUID v4",
        "authorization_consumption_reconciliation_ambiguous",
        "Der Vertrag inventarisiert exakt 28 unveränderte historische Checker",
        "`v27.34f` wird nicht automatisch ausgewählt.",
    )
    for marker in document_markers:
        require(marker in document, f"Vertragsdokumentation: Marker fehlt: {marker}")

    masterlist = read_text(MASTERLIST_PATH, "PROJECT_MASTERLIST")
    for marker in (
        "Der letzte abgeschlossene funktionale Stand bleibt v27.34b.",
        "Kein Adapter wurde implementiert",
        "`v27.34f` wird nicht automatisch ausgewählt oder autorisiert.",
    ):
        require(marker in masterlist, f"Masterliste: Marker fehlt: {marker}")
    validate_historical_masterlist_markers(masterlist)
    masterlist_manipulation_checks = run_historical_masterlist_manipulation_checks(
        masterlist
    )

    state = read_text(STATE_PATH, "PROJECT_STATE_CURRENT")
    for marker in (
        "Letzter abgeschlossener funktionaler Stand: v27.34b",
        "Aktueller HEAD: DYNAMISCH ZU PRÜFEN",
        "Weiterer funktionaler Schritt autorisiert: NEIN",
    ):
        require(marker in state, f"Projektzustand: Marker fehlt: {marker}")

    task = read_text(TASK_PATH, "CURRENT_TASK")
    validate_current_task_safety_boundaries(task)
    task_manipulation_checks = run_current_task_manipulation_checks(task)

    database_plan = read_text(DATABASE_PLAN_PATH, "Datenbankplan")
    for marker in (
        "Stand: v27.34e",
        "## Lokaler Registry-Adapter-Verhaltensvertrag v27.34e",
        "Kein Adapter wurde implementiert, importiert, instanziiert oder aufgerufen.",
        "v27.34e ist als vollständig gesperrter lokaler Adapter-Verhaltensvertrag umgesetzt.",
    ):
        require(marker in database_plan, f"Datenbankplan: Marker fehlt: {marker}")

        continuity = read_text(CONTINUITY_CHECKER_PATH, "Kontinuitäts-Checker")
    for marker in (
        "| v27.34e |",
        "### Vollständig gesperrter lokaler Adapter-Verhaltensvertrag v27.34e",
    ):
        require(
            continuity.count(marker) == 1,
            (
                "Kontinuitäts-Checker: Historischer v27.34e-Marker "
                f"nicht exakt einmal vorhanden: {marker}"
            ),
        )

    preflight = read_text(PREFLIGHT_PATH, "Preflight")
    require(
        preflight.count(CHECKER_RELATIVE_PATH) >= 2,
        "v27.34e-Vertragschecker fehlt als Preflight-Pflichtdatei oder Ausführung",
    )
    require(
        (
            "def check_exam_result_history_disposable_postgresql_test_python_"
            "environment_materialization_authorization_atomic_consumption_"
            "registry_adapter_local_fake_driver_adapter_contract():"
        )
        in preflight,
        "Preflight-Funktion für v27.34e fehlt",
    )

    return masterlist_manipulation_checks + task_manipulation_checks


def validate_security_boundaries(contract: dict[str, Any]) -> None:
    implementation = contract["implementationBoundary"]
    allowed_true = {
        "adapterBehaviorContractPrepared",
        "historicalCheckerInventoryPrepared",
    }
    for key, value in implementation.items():
        if key in allowed_true:
            require(value is True, f"Implementierungsmarker fehlt: {key}")
        elif type(value) is bool:
            require(value is False, f"Implementierungsgrenze offen: {key}")

    for key, value in contract["securityBoundary"].items():
        if type(value) is bool:
            require(value is False, f"Sicherheitsgrenze offen: {key}")

    future = contract["futureBoundary"]
    require(
        future["nextVersionAutomaticallySelected"] is False
        and future["automaticallyForbiddenVersion"] == "v27.34f"
        and future["nextTaskAuthorized"] is False
        and future["adapterImplementationAuthorized"] is False
        and future["adapterModuleCreated"] is False
        and future["historicalCheckerChangesAllowedInV27_34e"] is False,
        "Zukunftsgrenze ist offen",
    )
    require(
        ADAPTER_MODULE_PATH.is_file() is False,
        "Adapterdatei wurde in v27.34e unzulässig erstellt",
    )


def iter_scalar_paths(
    value: Any,
    path: tuple[str | int, ...] = (),
) -> Iterator[tuple[str | int, ...]]:
    if type(value) is dict:
        for key, child in value.items():
            yield from iter_scalar_paths(child, path + (key,))
    elif type(value) is list:
        for index, child in enumerate(value):
            yield from iter_scalar_paths(child, path + (index,))
    else:
        yield path


def mutated_scalar(value: Any) -> Any:
    if type(value) is bool:
        return not value
    if type(value) is int:
        return value + 1
    if type(value) is str:
        return value + "__manipulated__"
    if value is None:
        return "unexpected"
    raise ValidationError(f"Nicht unterstützter Skalar in Matrix: {type(value)}")


def set_at_path(value: Any, path: tuple[str | int, ...], replacement: Any) -> None:
    parent = value
    for part in path[:-1]:
        parent = parent[part]
    parent[path[-1]] = replacement


def must_reject_candidate(candidate: dict[str, Any], label: str) -> None:
    try:
        validate_contract_fingerprint(candidate)
    except ValidationError:
        return
    raise ValidationError(f"Manipulation wurde nicht blockiert: {label}")


def run_manipulation_matrix(contract: dict[str, Any]) -> int:
    checks = 0
    for path in iter_scalar_paths(contract):
        manipulated = copy.deepcopy(contract)
        current = manipulated
        for part in path:
            current = current[part]
        set_at_path(manipulated, path, mutated_scalar(current))
        must_reject_candidate(manipulated, ".".join(map(str, path)))
        checks += 1

    for key in EXPECTED_TOP_LEVEL_KEYS:
        manipulated = copy.deepcopy(contract)
        del manipulated[key]
        must_reject_candidate(manipulated, f"oberster Schlüssel fehlt: {key}")
        checks += 1

    manipulated = copy.deepcopy(contract)
    manipulated["unexpected"] = True
    must_reject_candidate(manipulated, "unbekannter oberster Schlüssel")
    checks += 1

    duplicate_was_rejected = False
    try:
        parse_json_strict(b'{"version":"a","version":"b"}\n', "Duplikattest")
    except ValidationError:
        duplicate_was_rejected = True
    require(duplicate_was_rejected, "Doppelter JSON-Schlüssel wurde akzeptiert")
    checks += 1
    return checks


def validate_contract(contract: dict[str, Any]) -> int:
    require(
        tuple(contract) == EXPECTED_TOP_LEVEL_KEYS,
        "Oberste Vertragsstruktur besitzt fehlende, zusätzliche oder umgeordnete Schlüssel",
    )
    validate_contract_fingerprint(contract)
    require(contract["version"] == "v27.34e", "Vertragsversion ist ungültig")
    require(contract["contractVersion"] == 1, "Vertragsschema ist ungültig")
    require(
        contract["status"]
        == (
            "planned_local_fake_atomic_consumption_registry_adapter_behavior_"
            "fully_locked_not_implemented"
        ),
        "Vertragsstatus ist ungültig",
    )
    require(
        contract["productiveReleaseAllowed"] is False,
        "Produktive Freigabe ist offen",
    )
    source_contract = validate_bound_sources(contract)
    validate_fake_driver_definitions()
    validate_result_bindings(contract, source_contract)
    validate_historical_inventory(contract)
    validate_security_boundaries(contract)
    document_manipulation_checks = validate_project_documents()
    return run_manipulation_matrix(contract) + document_manipulation_checks


def main() -> int:
    try:
        require(CONTRACT_PATH.is_file(), "v27.34e-JSON-Vertrag fehlt")
        raw = CONTRACT_PATH.read_bytes()
        require(
            sha256_bytes(raw) == EXPECTED_CONTRACT_FILE_SHA256,
            "v27.34e-Vertragsdateifingerprint ist ungültig",
        )
        contract = parse_json_strict(raw, "v27.34e-Vertrag")
        manipulation_checks = validate_contract(contract)
    except (ValidationError, OSError, SyntaxError) as exc:
        print(f"FEHLER: {exc}")
        print("STOPP: v27.34e-Adapter-Verhaltensvertrag verletzt.")
        return 1

    print("Lokaler Adapter-Verhaltensvertrag v27.34e: OK")
    print("Factory, Deepcopy, Resultatvalidierung und Exception-Mapping: gesperrt")
    print("Reconciliation und Timeout-Zuständigkeit: gesperrt")
    print("Historische Sperrchecker: 28 / unverändert")
    print("Adapterdatei: nicht vorhanden")
    print(f"Manipulationsmatrix: {manipulation_checks} Blockierungen bestätigt")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
