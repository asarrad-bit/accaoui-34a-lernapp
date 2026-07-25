from __future__ import annotations

import builtins
import copy
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MIGRATIONS = ROOT / "supabase" / "migrations"

MODULE = ROOT / "tools" / (
    "accaoui_disposable_test_python_environment_materialization_"
    "authorization_atomic_consumption_registry_adapter_execution_"
    "descriptor.py"
)
CONTRACT = ROOT / "docs" / "contracts" / (
    "exam-history-disposable-postgresql-test-python-environment-"
    "materialization-authorization-atomic-consumption-registry-"
    "adapter-execution-descriptor-contract.json"
)
SOURCE = ROOT / "docs" / "contracts" / (
    "exam-history-disposable-postgresql-test-python-environment-"
    "materialization-authorization-atomic-consumption-registry-"
    "adapter-execution-contract.json"
)
FUTURE_GUARD = ROOT / "tools" / (
    "accaoui_disposable_test_python_environment_materialization_"
    "authorization_atomic_consumption_registry_adapter_execution_"
    "descriptor_acceptance_guard.py"
)
FUTURE_EXECUTION = ROOT / "tools" / (
    "accaoui_disposable_test_python_environment_materialization_"
    "authorization_atomic_consumption_registry_adapter_execution.py"
)

SUCCESS_STATUS = (
    "atomic_consumption_registry_adapter_execution_descriptor_"
    "ready_execution_locked"
)
SUCCESS_REASON = (
    "authorization_atomic_consumption_registry_adapter_execution_"
    "descriptor_ready_execution_locked"
)
BLOCKED_STATUS = (
    "atomic_consumption_registry_adapter_execution_descriptor_"
    "blocked_execution_locked"
)
BLOCKED_REASON = (
    "authorization_atomic_consumption_registry_adapter_execution_"
    "descriptor_contract_invalid"
)


def fail(message):
    print(f"FEHLER: {message}")
    raise SystemExit(1)


def load_json(path, label):
    if not path.is_file():
        fail(f"{label} fehlt.")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"{label} ungültig: {exc}")


def load_module():
    if not MODULE.is_file():
        fail("v27.33a-Descriptor fehlt.")
    spec = importlib.util.spec_from_file_location("v2733a_descriptor", MODULE)
    if spec is None or spec.loader is None:
        fail("v27.33a-Descriptor kann nicht geladen werden.")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def iter_scalar_paths(value, path=()):
    if isinstance(value, dict):
        for key, item in value.items():
            yield from iter_scalar_paths(item, path + (key,))
        return
    if isinstance(value, list):
        for index, item in enumerate(value):
            yield from iter_scalar_paths(item, path + (index,))
        return
    yield path


def mutate_scalar(value):
    if isinstance(value, bool):
        return not value
    if isinstance(value, int):
        return value + 1
    if isinstance(value, str):
        return value + "_tampered"
    if value is None:
        return "tampered"
    return {"tampered": True}


def set_path(value, path):
    target = value
    for part in path[:-1]:
        target = target[part]
    leaf = path[-1]
    target[leaf] = mutate_scalar(target[leaf])


def assert_blocked(result, label):
    if result.get("status") != BLOCKED_STATUS:
        fail(f"Manipulation wurde nicht blockiert: {label}")
    if result.get("reason") != BLOCKED_REASON:
        fail(f"Blockgrund ist ungültig: {label}")
    if result.get("ready") is not False:
        fail(f"Blockiertes Ergebnis ist bereit: {label}")
    if result.get("descriptor") is not None:
        fail(f"Blockiertes Ergebnis enthält Descriptor: {label}")
    if result.get("executionGrant") is not False:
        fail(f"Blockiertes Ergebnis öffnet den Grant: {label}")


contract = load_json(CONTRACT, "v27.33a-Vertrag")
source = load_json(SOURCE, "v27.32z-Quellvertrag")
module = load_module()
resolver = getattr(
    module,
    "resolve_atomic_consumption_registry_adapter_execution_descriptor",
    None,
)
if not callable(resolver):
    fail("Descriptor-Resolver fehlt.")

if contract.get("version") != "v27.33a":
    fail("Descriptorvertrag besitzt nicht v27.33a.")
if contract.get("contractVersion") != 1:
    fail("Descriptorvertrag besitzt nicht Schema 1.")
if contract.get("status") != (
    "implemented_pure_atomic_consumption_registry_adapter_execution_"
    "descriptor_execution_locked"
):
    fail("Descriptorvertragsstatus ist ungültig.")
if contract.get("productiveReleaseAllowed") is not False:
    fail("Produktive Freigabe ist offen.")
if source.get("version") != "v27.32z":
    fail("Quellvertrag besitzt nicht v27.32z.")
if source.get("status") != (
    "planned_atomic_consumption_registry_adapter_execution_"
    "fully_locked_not_implemented"
):
    fail("Quellvertragsstatus ist ungültig.")

implementation = contract.get("implementation", {})
if implementation.get("executionDescriptorImplemented") is not True:
    fail("Descriptor ist nicht als implementiert markiert.")
for key, value in implementation.items():
    if key.endswith("Path") or key == "executionDescriptorImplemented":
        continue
    if value is not False:
        fail(f"Implementierungsgrenze ist offen: {key}")

input_boundary = contract.get("inputBoundary", {})
required_input = {
    "mappingOnly": True,
    "exactFields": ["contractFacts"],
    "requiredSourceVersion": "v27.32z",
    "requiredSourceStatus": (
        "planned_atomic_consumption_registry_adapter_execution_"
        "fully_locked_not_implemented"
    ),
    "exactContractFactsRequired": True,
    "unknownFieldsAllowed": False,
    "missingFieldsAllowed": False,
    "inputMutationAllowed": False,
}
for key, expected in required_input.items():
    if input_boundary.get(key) != expected:
        fail(f"Eingabegrenze ist ungültig: {key}")

descriptor_boundary = contract.get("descriptorBoundary", {})
required_descriptor = {
    "descriptorVersion": 1,
    "successStatus": SUCCESS_STATUS,
    "successReason": SUCCESS_REASON,
    "blockedStatus": BLOCKED_STATUS,
    "blockedReason": BLOCKED_REASON,
    "ready": True,
    "canonicalCopyRequired": True,
    "sourceContractVersion": "v27.32z",
    "sourceContractStatus": (
        "planned_atomic_consumption_registry_adapter_execution_"
        "fully_locked_not_implemented"
    ),
    "executionGrant": False,
}
for key, expected in required_descriptor.items():
    if descriptor_boundary.get(key) != expected:
        fail(f"Descriptorgrenze ist ungültig: {key}")

for key, value in contract.get("securityBoundary", {}).items():
    if value is not False:
        fail(f"Sicherheitsgrenze ist offen: {key}")
for key, value in contract.get("futureBoundary", {}).items():
    if value is not False:
        fail(f"Zukunftsgrenze ist offen: {key}")

valid_input = {"contractFacts": copy.deepcopy(source)}
input_before = copy.deepcopy(valid_input)

original_open = builtins.open

def forbidden_open(*args, **kwargs):
    raise AssertionError("Descriptor darf keine Datei öffnen.")

builtins.open = forbidden_open
try:
    result = resolver(valid_input)
finally:
    builtins.open = original_open

if valid_input != input_before:
    fail("Descriptor hat die Eingabe verändert.")
if result.get("status") != SUCCESS_STATUS:
    fail("Erfolgsstatus ist ungültig.")
if result.get("reason") != SUCCESS_REASON:
    fail("Erfolgsgrund ist ungültig.")
if result.get("ready") is not True:
    fail("Gültiger Descriptor ist nicht bereit.")
if result.get("executionGrant") is not False:
    fail("Descriptor öffnet den Ausführungsgrant.")

descriptor = result.get("descriptor")
if not isinstance(descriptor, dict):
    fail("Kanonischer Descriptor fehlt.")
if descriptor.get("descriptorVersion") != 1:
    fail("Descriptorversion ist ungültig.")
if descriptor.get("sourceContractVersion") != "v27.32z":
    fail("Descriptor-Quellversion ist ungültig.")
if descriptor.get("sourceContractStatus") != source.get("status"):
    fail("Descriptor-Quellstatus ist ungültig.")
if descriptor.get("contractFacts") != source:
    fail("Vertragsfakten wurden nicht kanonisch kopiert.")
if descriptor.get("contractFacts") is valid_input["contractFacts"]:
    fail("Vertragsfakten wurden nicht tief kopiert.")
if descriptor.get("executionGrant") is not False:
    fail("Kanonischer Descriptor öffnet den Grant.")

for key, value in result.items():
    if key in {"status", "reason", "ready", "descriptor"}:
        continue
    if value is not False:
        fail(f"Ergebnisgrenze ist offen: {key}")

valid_input["contractFacts"]["version"] = "mutated_after_result"
if descriptor["contractFacts"] != source:
    fail("Descriptor ist nicht von späterer Eingabemutation getrennt.")

assert_blocked(resolver(None), "nicht Mapping")
assert_blocked(resolver({}), "fehlendes Feld")
assert_blocked(
    resolver({"contractFacts": copy.deepcopy(source), "unknown": True}),
    "unbekanntes Feld",
)
assert_blocked(resolver({"contractFacts": []}), "falscher Faktentyp")

for key in source:
    candidate = copy.deepcopy(source)
    candidate.pop(key)
    assert_blocked(
        resolver({"contractFacts": candidate}),
        f"fehlender Vertragsblock {key}",
    )

unknown_candidate = copy.deepcopy(source)
unknown_candidate["unknownContractFact"] = True
assert_blocked(
    resolver({"contractFacts": unknown_candidate}),
    "unbekannter Vertragsblock",
)

leaf_count = 0
for path in iter_scalar_paths(source):
    candidate = copy.deepcopy(source)
    set_path(candidate, path)
    assert_blocked(
        resolver({"contractFacts": candidate}),
        "manipulierter Pfad " + ".".join(map(str, path)),
    )
    leaf_count += 1

source_text = MODULE.read_text(encoding="utf-8")
for forbidden in (
    "subprocess",
    "socket",
    "psycopg",
    "supabase",
    "requests",
    "urllib",
    "sqlite3",
):
    if forbidden in source_text:
        fail(f"Descriptor enthält verbotenen Zugriff: {forbidden}")

if FUTURE_EXECUTION.exists():
    fail("v27.33a darf noch keine Adapter-Ausführung umsetzen.")
if list(MIGRATIONS.glob("*v2733a*.sql")):
    fail("v27.33a darf keine SQL-Migration erzeugen.")

print("Registry-Adapter-Ausführungsdescriptor: OK")
print("Quellvertrag: v27.32z")
print(f"Manipulierte Vertragsblätter blockiert: {leaf_count}")
print("Kanonische Tiefenkopie: geprüft")
print("Eingabemutation: keine")
print("Dateizugriff des Resolvers: keiner")
print("Adapter implementiert: nein")
print("Adapter aufgerufen: nein")
print("Registryzugriff: keiner")
print("Verbrauch ausgeführt: nein")
print("Datenbankverbindung: keine")
print("SQL-Migration v27.33a: keine")
print("Produktive Freigabe: nein")
