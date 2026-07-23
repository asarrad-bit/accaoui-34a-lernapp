from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import uuid
from pathlib import Path

from accaoui_disposable_connection_adapter_readiness import (
    build_connection_adapter_readiness,
)
from accaoui_disposable_environment_gate import (
    REQUIRED_KEYS as DISPOSABLE_GATE_KEYS,
    evaluate_environment,
)

ROOT = Path(__file__).resolve().parents[1]

SOURCE_CONTRACT_PATH = (
    ROOT
    / "docs"
    / "contracts"
    / "exam-history-outer-domain-mutation-fixture-harness-contract.json"
)
FIXTURE_CATALOG_PATH = (
    ROOT
    / "tools"
    / "fixtures"
    / "exam-history-outer-domain-mutation-fixtures.json"
)
READINESS_CONTRACT_PATH = (
    ROOT
    / "docs"
    / "contracts"
    / "exam-history-outer-domain-mutation-harness-readiness-contract.json"
)


class HarnessValidationError(RuntimeError):
    pass


def load_json(path: Path, label: str):
    if not path.is_file():
        raise HarnessValidationError(f"{label} fehlt: {path}")

    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise HarnessValidationError(
            f"{label} ist ungültig: {exc}"
        ) from exc


def canonical_sha256(value: object) -> str:
    payload = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def source_projection(source: dict) -> dict:
    required_keys = (
        "users",
        "resources",
        "clientRequestKeys",
        "payloads",
        "expectedVersions",
        "scenarios",
        "concurrencyBarriers",
        "harnessLifecycle",
        "faultInjectionContract",
    )

    for key in required_keys:
        if key not in source:
            raise HarnessValidationError(
                f"Quellvertrag enthält nicht: {key}"
            )

    return {
        "version": "v27.31y",
        "catalogVersion": 1,
        "status": "synthetic_not_executed",
        "sourceContractPath": (
            "docs/contracts/"
            "exam-history-outer-domain-mutation-"
            "fixture-harness-contract.json"
        ),
        "sourceContractVersion": "v27.31x",
        "syntheticOnly": True,
        "databaseExecutionAllowed": False,
        "users": source["users"],
        "resources": source["resources"],
        "clientRequestKeys": source["clientRequestKeys"],
        "payloads": source["payloads"],
        "expectedVersions": source["expectedVersions"],
        "scenarios": source["scenarios"],
        "concurrencyBarriers": source["concurrencyBarriers"],
        "harnessLifecycle": source["harnessLifecycle"],
        "faultInjectionContract": source["faultInjectionContract"],
    }


def validate_catalog(
    source: dict,
    catalog: dict,
    readiness: dict,
) -> None:
    if source.get("version") != "v27.31x":
        raise HarnessValidationError(
            "Quellvertrag besitzt nicht v27.31x."
        )

    expected_catalog = source_projection(source)
    if catalog != expected_catalog:
        raise HarnessValidationError(
            "Fixture-Katalog weicht vom v27.31x-Quellvertrag ab."
        )

    if readiness.get("version") != "v27.31y":
        raise HarnessValidationError(
            "Readiness-Vertrag besitzt nicht v27.31y."
        )

    integrity = readiness.get("catalogIntegrity", {})
    actual_fingerprint = canonical_sha256(catalog)

    if integrity.get("canonicalSha256") != actual_fingerprint:
        raise HarnessValidationError(
            "Fixture-Katalog-Fingerprint ist ungültig."
        )

    expected_counts = {
        "userCount": len(catalog["users"]),
        "resourceCount": len(catalog["resources"]),
        "clientRequestKeyCount": len(
            catalog["clientRequestKeys"]
        ),
        "payloadCount": len(catalog["payloads"]),
        "scenarioCount": len(catalog["scenarios"]),
        "concurrencyBarrierCount": len(
            catalog["concurrencyBarriers"]
        ),
    }

    for key, expected in expected_counts.items():
        if integrity.get(key) != expected:
            raise HarnessValidationError(
                f"Fixture-Katalog-Anzahl ist ungültig: {key}"
            )

    user_ids = set()
    for user in catalog["users"]:
        user_id = user.get("id")
        auth_user_id = user.get("authUserId")

        if user_id in user_ids:
            raise HarnessValidationError(
                f"Doppelte Fixture-Nutzer-ID: {user_id}"
            )
        user_ids.add(user_id)

        try:
            parsed = uuid.UUID(auth_user_id)
        except ValueError as exc:
            raise HarnessValidationError(
                f"Ungültige synthetische UUID: {auth_user_id}"
            ) from exc

        if parsed.version != 4:
            raise HarnessValidationError(
                f"Fixture-UUID ist nicht Version 4: {auth_user_id}"
            )

    resource_ids = set()
    for resource in catalog["resources"]:
        resource_id = resource.get("id")
        identity = resource.get("resourceIdentity")
        owner = resource.get("ownerUserId")

        if resource_id in resource_ids:
            raise HarnessValidationError(
                f"Doppelte Fixture-Ressource: {resource_id}"
            )
        resource_ids.add(resource_id)

        if not isinstance(identity, str) or not identity.startswith(
            "fixture:"
        ):
            raise HarnessValidationError(
                f"Nicht synthetische Ressourcenidentität: {identity}"
            )
        if owner not in user_ids:
            raise HarnessValidationError(
                f"Unbekannter Fixture-Eigentümer: {owner}"
            )

    client_keys = catalog["clientRequestKeys"]
    values = list(client_keys.values())
    if len(values) != len(set(values)):
        raise HarnessValidationError(
            "Client-Wiederholungsschlüssel sind nicht eindeutig."
        )

    for key_id, value in client_keys.items():
        if not re.fullmatch(r"[0-9a-f]{64}", value):
            raise HarnessValidationError(
                f"Client-Schlüssel ist nicht 256 Bit: {key_id}"
            )

    payload_ids = set(catalog["payloads"])
    for scenario in catalog["scenarios"]:
        if scenario.get("userId") not in user_ids:
            raise HarnessValidationError(
                f"Unbekannter Szenarionutzer: {scenario.get('id')}"
            )
        if scenario.get("resourceId") not in resource_ids:
            raise HarnessValidationError(
                f"Unbekannte Szenarioressource: {scenario.get('id')}"
            )
        if scenario.get("clientKeyId") not in client_keys:
            raise HarnessValidationError(
                f"Unbekannter Szenarioschlüssel: {scenario.get('id')}"
            )
        if scenario.get("payloadId") not in payload_ids:
            raise HarnessValidationError(
                f"Unbekannter Szenariopayload: {scenario.get('id')}"
            )

    for barrier in catalog["concurrencyBarriers"]:
        if barrier.get("resourceId") not in resource_ids:
            raise HarnessValidationError(
                f"Unbekannte Barrierenressource: {barrier.get('id')}"
            )
        if barrier.get("parties") != 2:
            raise HarnessValidationError(
                f"Barriere besitzt nicht zwei Parteien: {barrier.get('id')}"
            )
        if any(
            key_id not in client_keys
            for key_id in barrier.get("clientKeyIds", [])
        ):
            raise HarnessValidationError(
                f"Barriere besitzt unbekannten Clientschlüssel: "
                f"{barrier.get('id')}"
            )
        if any(
            payload_id not in payload_ids
            for payload_id in barrier.get("payloadIds", [])
        ):
            raise HarnessValidationError(
                f"Barriere besitzt unbekannten Payload: "
                f"{barrier.get('id')}"
            )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Validiert den synthetischen Accaoui-"
            "Fachmutations-Fixture-Katalog."
        )
    )

    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--validate-only",
        action="store_true",
        help="Nur lokale Vertrags- und Fixture-Validierung.",
    )
    mode.add_argument(
        "--run-database",
        action="store_true",
        help=(
            "Spätere disposable Datenbankausführung; "
            "in v27.32b weiterhin vor jeder Verbindung gesperrt."
        ),
    )

    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        source = load_json(
            SOURCE_CONTRACT_PATH,
            "v27.31x-Quellvertrag",
        )
        catalog = load_json(
            FIXTURE_CATALOG_PATH,
            "synthetischer Fixture-Katalog",
        )
        readiness = load_json(
            READINESS_CONTRACT_PATH,
            "v27.31y-Readiness-Vertrag",
        )

        validate_catalog(source, catalog, readiness)

    except HarnessValidationError as exc:
        print(f"FEHLER: {exc}")
        return 1

    requested_environment = {
        key: os.environ.get(key, "")
        for key in DISPOSABLE_GATE_KEYS
        if key in os.environ
    }

    if args.run_database or requested_environment:
        gate_result = evaluate_environment(requested_environment)
        adapter_state = build_connection_adapter_readiness(gate_result)

        print("Gate-Entscheidung: " + str(gate_result.get("decision")))
        print("Gate-Grund: " + str(gate_result.get("reason")))
        print("Adapterstatus: " + str(adapter_state.get("status")))
        print("Adaptergrund: " + str(adapter_state.get("reason")))
        print("Datenbanktreiber geladen: nein")
        print("Datenbankverbindung geöffnet: nein")
        print("Netzwerkzugriff: nein")
        print("Datenbanktest ausgeführt: nein")
        return 2

    print("Synthetischer Fixture-Katalog: OK")
    print("Harness-Modus: validate_only")
    print("Datenbanktreiber geladen: nein")
    print("Datenbankverbindung geöffnet: nein")
    print("Netzwerkzugriff: nein")
    print("Datenbanktest ausgeführt: nein")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
