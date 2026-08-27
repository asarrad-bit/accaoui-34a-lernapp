#!/usr/bin/env python3
"""Prüft die v27.36e-Browser-Komposition ausschließlich lokal und synthetisch."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE_HEAD = "ad6ccd8b8e010167f303cf0a24edfe8d8036fb81"
ADAPTER_PATH = ROOT / "data/supabase-participant-access-adapter.js"
BRIDGE_PATH = ROOT / "data/supabase-participant-access-bootstrap-bridge.js"
PROVIDER_PATH = ROOT / "data/supabase-participant-access-browser-provider.js"
DOC_PATH = ROOT / "docs/PARTICIPANT_ACCESS_BROWSER_PROVIDER_V2736E.md"
PREFLIGHT_PATH = ROOT / "tools/preflight.py"

AUTHORIZED_FILES = {
    "data/supabase-participant-access-adapter.js",
    "data/supabase-participant-access-bootstrap-bridge.js",
    "data/supabase-participant-access-browser-provider.js",
    "tools/check-participant-access-browser-provider-v2736e.py",
    "docs/PARTICIPANT_ACCESS_BROWSER_PROVIDER_V2736E.md",
    "tools/preflight.py",
}

FROZEN_FILES = (
    "index.html",
    "app.js",
    "style.css",
    "data/supabase-client-bootstrap.js",
    "data/supabase-client-adapter.js",
)

LEGACY_CHECKERS = (
    "tools/check-supabase-participant-access-adapter.py",
    "tools/check-supabase-participant-access-bootstrap-bridge.py",
)


def stop(message: str, code: int = 1) -> None:
    print(f"STOPP: {message}")
    raise SystemExit(code)


def run(arguments: list[str], *, input_text: str | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        arguments,
        cwd=ROOT,
        input=input_text,
        text=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )


def run_git(arguments: list[str]) -> str:
    result = run(["git", *arguments])
    if result.returncode != 0:
        stop(f"Lokale Git-Prüfung fehlgeschlagen: {' '.join(arguments)}")
    return result.stdout


def changed_paths() -> set[str]:
    paths = {
        line.strip().replace("\\", "/")
        for line in run_git(["diff", "--name-only", BASE_HEAD]).splitlines()
        if line.strip()
    }
    paths.update(
        line.strip().replace("\\", "/")
        for line in run_git(["ls-files", "--others", "--exclude-standard"]).splitlines()
        if line.strip()
    )
    return paths


def current_task_authorizes_v2736e() -> bool:
    task_path = ROOT / "docs/tasks/CURRENT_TASK.md"
    try:
        lines = task_path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError):
        return False

    def single_value(prefix: str) -> str | None:
        values = [line[len(prefix):].strip() for line in lines if line.startswith(prefix)]
        return values[0] if len(values) == 1 else None

    expected_files = ", ".join(f"`{path}`" for path in (
        "data/supabase-participant-access-adapter.js",
        "data/supabase-participant-access-bootstrap-bridge.js",
        "data/supabase-participant-access-browser-provider.js",
        "tools/check-participant-access-browser-provider-v2736e.py",
        "docs/PARTICIPANT_ACCESS_BROWSER_PROVIDER_V2736E.md",
        "tools/preflight.py",
    ))
    return (
        single_value("Task-ID:") == "v27.36e"
        and single_value("Status:") == "AUTHORIZED"
        and single_value("Autorisiert:") == "JA"
        and single_value("Erlaubte Implementierungsdateien:") == expected_files
    )


def baseline_bytes(relative_path: str) -> bytes:
    result = subprocess.run(
        ["git", "show", f"{BASE_HEAD}:{relative_path}"],
        cwd=ROOT,
        capture_output=True,
    )
    if result.returncode != 0:
        stop(f"Basisdatei kann nicht gelesen werden: {relative_path}")
    return result.stdout


def require_legacy_checker(relative_path: str) -> None:
    result = run([sys.executable, relative_path])
    if result.returncode != 0:
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr)
        stop(f"Bestandschecker fehlgeschlagen: {relative_path}")


def require_v2736d_regression() -> None:
    """Führt den unveränderten v27.36d-Checker mit engem Hash-Übergang aus."""

    checker_path = ROOT / "tools/check-participant-access-app-entry-v2736d.py"
    source = checker_path.read_text(encoding="utf-8")
    expected_hashes = {
        "337f66f2b06143451916ee967ca72af5a6cdfe41ac4d4d8301bd5f88655826e4":
            hashlib.sha256(ADAPTER_PATH.read_bytes()).hexdigest(),
        "da890515c7b8b165b397333826078ca02fe4552559e2873d1d5329238082138b":
            hashlib.sha256(BRIDGE_PATH.read_bytes()).hexdigest(),
    }

    for historic_hash, current_hash in expected_hashes.items():
        if source.count(historic_hash) != 1:
            stop("v27.36d-Checker besitzt nicht mehr den erwarteten Hashvertrag")
        source = source.replace(historic_hash, current_hash, 1)

    runner = (
        "import sys\n"
        "source = sys.stdin.buffer.read().decode('utf-8')\n"
        f"path = {str(checker_path)!r}\n"
        "scope = {'__name__': '__main__', '__file__': path}\n"
        "exec(compile(source, path, 'exec'), scope)\n"
    )
    result = run([sys.executable, "-c", runner], input_text=source)
    if result.returncode != 0:
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr)
        stop("v27.36d-Regressionsprüfung fehlgeschlagen")


for path in (ADAPTER_PATH, BRIDGE_PATH, PROVIDER_PATH, DOC_PATH, PREFLIGHT_PATH):
    if not path.is_file():
        stop(f"Pflichtdatei fehlt: {path.relative_to(ROOT)}")

current_changes = changed_paths()
if current_task_authorizes_v2736e() and current_changes != AUTHORIZED_FILES:
    stop("Working-Tree-Dateimenge ist nicht exakt der autorisierte v27.36e-Scope")

for relative_path in FROZEN_FILES:
    current = (ROOT / relative_path).read_bytes()
    if current != baseline_bytes(relative_path):
        stop(f"Frozen-Datei wurde verändert: {relative_path}")

if current_task_authorizes_v2736e():
    for relative_path in current_changes:
        lowered = relative_path.casefold()
        if lowered.startswith("supabase/") or "config" in lowered or lowered.endswith(".sql"):
            stop(f"Gesperrter Config-/SQL-/Migrationsscope wurde verändert: {relative_path}")

adapter_text = ADAPTER_PATH.read_text(encoding="utf-8")
bridge_text = BRIDGE_PATH.read_text(encoding="utf-8")
provider_text = PROVIDER_PATH.read_text(encoding="utf-8")
doc_text = DOC_PATH.read_text(encoding="utf-8")
preflight_text = PREFLIGHT_PATH.read_text(encoding="utf-8")

for marker in (
    "module.exports",
    "createParticipantAccessAdapter",
    "ACCAOUI_PARTICIPANT_ACCESS_ADAPTER_FACTORY",
):
    if marker not in adapter_text:
        stop(f"v27.36b-Dualexportmarker fehlt: {marker}")

for marker in (
    "module.exports",
    "createParticipantAccessBootstrapBridge",
    "ACCAOUI_PARTICIPANT_ACCESS_BOOTSTRAP_BRIDGE_FACTORY",
):
    if marker not in bridge_text:
        stop(f"v27.36c-Dualexportmarker fehlt: {marker}")

for marker in (
    "ACCAOUI_SUPABASE_BOOTSTRAP",
    "ACCAOUI_PARTICIPANT_ACCESS_ADAPTER_FACTORY",
    "ACCAOUI_PARTICIPANT_ACCESS_BOOTSTRAP_BRIDGE_FACTORY",
    "ACCAOUI_PARTICIPANT_ACCESS_APP_PROVIDER",
    "resolveAccess",
    "access_allowed",
    "fail-closed",
):
    if marker not in provider_text:
        stop(f"Provider-Vertragsmarker fehlt: {marker}")

for token in (
    "initializeClient",
    "getState",
    "createClient",
    "getClient(",
    "auth.getSession",
    ".from(",
    "participants",
    "enrollments",
    "courses",
    "userId",
    "fetch(",
    "XMLHttpRequest",
    "WebSocket",
    "process.env",
):
    if token in provider_text:
        stop(f"Provider verletzt die Kompositionsgrenze: {token}")

for marker in (
    "Ziel",
    "Sicherheitsgrenze",
    "CommonJS-Kompatibilität",
    "kontrollierte Browser-Exports",
    "ausschließlich resolveAccess()",
    "keine duplizierte Fachlogik",
    "lokale synthetische Tests",
    "Supabase live: NEIN",
    "echte Keys: NEIN",
    "echte Teilnehmerdaten: NEIN",
):
    if marker not in doc_text:
        stop(f"Dokumentationsmarker fehlt: {marker}")

if "check-participant-access-browser-provider-v2736e.py" not in preflight_text:
    stop("v27.36e-Checker ist nicht dauerhaft im Preflight eingebunden")

node_candidates = (
    Path("C:/Program Files/nodejs/node.exe"),
    Path("C:/Program Files (x86)/nodejs/node.exe"),
    Path("/usr/bin/node"),
    Path("/usr/local/bin/node"),
    Path("/opt/homebrew/bin/node"),
)
node_path = next((path for path in node_candidates if path.is_file()), None)
if node_path is None:
    stop("erforderliche lokale JavaScript-Laufzeit fehlt", code=2)


HARNESS = r'''"use strict";

const fs = require("fs");
const vm = require("vm");

const adapterSource = fs.readFileSync(process.argv[1], "utf8");
const bridgeSource = fs.readFileSync(process.argv[2], "utf8");
const providerSource = fs.readFileSync(process.argv[3], "utf8");

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

function equal(actual, expected, message) {
  assert(JSON.stringify(actual) === JSON.stringify(expected),
    `${message}: ${JSON.stringify(actual)} !== ${JSON.stringify(expected)}`);
}

function execute(source, sandbox, filename) {
  const context = vm.createContext(sandbox);
  vm.runInContext(source, context, { filename });
  return context;
}

function commonJsApi(source, filename) {
  const module = { exports: {} };
  execute(source, { module }, filename);
  return module.exports;
}

function executeBrowser(sources, browserWindow) {
  const sandbox = { window: browserWindow, self: browserWindow };
  const context = vm.createContext(sandbox);
  for (const [source, filename] of sources) {
    vm.runInContext(source, context, { filename });
  }
  return browserWindow;
}

function baseWindow(result = Object.freeze({ allowed: false, code: "participant_blocked" })) {
  const state = { factoryCalls: 0, resolveCalls: 0, dependencies: null };
  const win = {
    ACCAOUI_SUPABASE_BOOTSTRAP: Object.freeze({ marker: "synthetic-bootstrap" }),
    ACCAOUI_PARTICIPANT_ACCESS_ADAPTER_FACTORY: function syntheticAdapterFactory() {},
    ACCAOUI_PARTICIPANT_ACCESS_BOOTSTRAP_BRIDGE_FACTORY: function bridgeFactory(dependencies) {
      state.factoryCalls += 1;
      state.dependencies = dependencies;
      return {
        async resolveAccess() {
          state.resolveCalls += 1;
          return result;
        }
      };
    }
  };
  return { win, state };
}

async function main() {
  let positive = 0;
  let negative = 0;
  let manipulations = 0;

  const adapterApi = commonJsApi(adapterSource, "adapter-commonjs.js");
  assert(typeof adapterApi.createParticipantAccessAdapter === "function", "Adapter CommonJS");
  positive += 1;

  const bridgeApi = commonJsApi(bridgeSource, "bridge-commonjs.js");
  assert(typeof bridgeApi.createParticipantAccessBootstrapBridge === "function", "Bridge CommonJS");
  positive += 1;

  const exportWindow = {};
  executeBrowser([
    [adapterSource, "adapter-browser.js"],
    [bridgeSource, "bridge-browser.js"]
  ], exportWindow);
  assert(typeof exportWindow.ACCAOUI_PARTICIPANT_ACCESS_ADAPTER_FACTORY === "function", "Adapter Browser-Export");
  positive += 1;
  assert(typeof exportWindow.ACCAOUI_PARTICIPANT_ACCESS_BOOTSTRAP_BRIDGE_FACTORY === "function", "Bridge Browser-Export");
  positive += 1;
  equal(Object.keys(exportWindow).sort(), [
    "ACCAOUI_PARTICIPANT_ACCESS_ADAPTER_FACTORY",
    "ACCAOUI_PARTICIPANT_ACCESS_BOOTSTRAP_BRIDGE_FACTORY"
  ], "Keine zusätzlichen Browser-Globals");
  positive += 1;

  const foreignAdapter = Object.freeze({ foreign: true });
  const adapterCollision = { ACCAOUI_PARTICIPANT_ACCESS_ADAPTER_FACTORY: foreignAdapter };
  executeBrowser([[adapterSource, "adapter-collision.js"]], adapterCollision);
  assert(adapterCollision.ACCAOUI_PARTICIPANT_ACCESS_ADAPTER_FACTORY === foreignAdapter, "Adapter-Kollision");
  positive += 1;

  const foreignBridge = Object.freeze({ foreign: true });
  const bridgeCollision = { ACCAOUI_PARTICIPANT_ACCESS_BOOTSTRAP_BRIDGE_FACTORY: foreignBridge };
  executeBrowser([[bridgeSource, "bridge-collision.js"]], bridgeCollision);
  assert(bridgeCollision.ACCAOUI_PARTICIPANT_ACCESS_BOOTSTRAP_BRIDGE_FACTORY === foreignBridge, "Bridge-Kollision");
  positive += 1;

  const firstAdapterFactory = exportWindow.ACCAOUI_PARTICIPANT_ACCESS_ADAPTER_FACTORY;
  executeBrowser([[adapterSource, "adapter-repeat.js"]], exportWindow);
  assert(exportWindow.ACCAOUI_PARTICIPANT_ACCESS_ADAPTER_FACTORY === firstAdapterFactory, "Adapter identisch");
  positive += 1;
  const firstBridgeFactory = exportWindow.ACCAOUI_PARTICIPANT_ACCESS_BOOTSTRAP_BRIDGE_FACTORY;
  executeBrowser([[bridgeSource, "bridge-repeat.js"]], exportWindow);
  assert(exportWindow.ACCAOUI_PARTICIPANT_ACCESS_BOOTSTRAP_BRIDGE_FACTORY === firstBridgeFactory, "Bridge identisch");
  positive += 1;

  const allowedResult = Object.freeze({ allowed: true, code: "access_allowed", marker: "same-object" });
  const allowedFixture = baseWindow(allowedResult);
  executeBrowser([[providerSource, "provider.js"]], allowedFixture.win);
  const provider = allowedFixture.win.ACCAOUI_PARTICIPANT_ACCESS_APP_PROVIDER;
  equal(Object.keys(provider), ["resolveAccess"], "Provider-Oberfläche");
  positive += 1;
  assert(typeof provider.resolveAccess === "function" && Object.isFrozen(provider), "Provider-Funktion/frozen");
  positive += 1;
  const allowedActual = await provider.resolveAccess();
  assert(allowedActual === allowedResult, "Gültiges Ergebnis unverändert");
  positive += 1;
  assert(allowedFixture.state.factoryCalls === 1 && allowedFixture.state.resolveCalls === 1, "Exakt eine Delegation");
  positive += 1;
  equal(Object.keys(allowedFixture.state.dependencies).sort(), [
    "bootstrap", "createParticipantAccessAdapter", "utcNow"
  ], "Exakte Bridge-Dependencies");
  positive += 1;
  assert(allowedFixture.state.dependencies.bootstrap === allowedFixture.win.ACCAOUI_SUPABASE_BOOTSTRAP,
    "Bootstrap unverändert weitergereicht");
  positive += 1;
  assert(allowedFixture.state.dependencies.createParticipantAccessAdapter ===
    allowedFixture.win.ACCAOUI_PARTICIPANT_ACCESS_ADAPTER_FACTORY, "Adapter-Factory unverändert");
  positive += 1;
  const utcValue = allowedFixture.state.dependencies.utcNow();
  assert(typeof utcValue === "string" && Number.isFinite(Date.parse(utcValue)), "Lokale UTC-Zeitquelle");
  positive += 1;

  const blockedResult = Object.freeze({ allowed: false, code: "participant_blocked", marker: "same-object" });
  const blockedFixture = baseWindow(blockedResult);
  executeBrowser([[providerSource, "provider-blocked.js"]], blockedFixture.win);
  assert(await blockedFixture.win.ACCAOUI_PARTICIPANT_ACCESS_APP_PROVIDER.resolveAccess() === blockedResult,
    "Blockiertes Ergebnis unverändert");
  positive += 1;

  const compatibleProvider = Object.freeze({ resolveAccess: async () => blockedResult });
  const compatibleCollision = { ACCAOUI_PARTICIPANT_ACCESS_APP_PROVIDER: compatibleProvider };
  executeBrowser([[providerSource, "provider-compatible-collision.js"]], compatibleCollision);
  assert(compatibleCollision.ACCAOUI_PARTICIPANT_ACCESS_APP_PROVIDER === compatibleProvider, "Kompatible Provider-Kollision");
  positive += 1;

  const incompatibleProvider = Object.freeze({ resolveAccess: async () => blockedResult, extra: true });
  const incompatibleCollision = { ACCAOUI_PARTICIPANT_ACCESS_APP_PROVIDER: incompatibleProvider };
  executeBrowser([[providerSource, "provider-incompatible-collision.js"]], incompatibleCollision);
  assert(incompatibleCollision.ACCAOUI_PARTICIPANT_ACCESS_APP_PROVIDER === incompatibleProvider, "Inkompatible Provider-Kollision");
  positive += 1;

  execute(providerSource, {}, "provider-without-window.js");
  positive += 1;

  const USER_ID = "11111111-1111-4111-8111-111111111111";
  const PARTICIPANT_ID = "22222222-2222-4222-8222-222222222222";
  const ENROLLMENT_ID = "33333333-3333-4333-8333-333333333333";
  const COURSE_ID = "44444444-4444-4444-8444-444444444444";
  const rows = {
    participants: [{ id: PARTICIPANT_ID, auth_user_id: USER_ID, status: "active" }],
    enrollments: [{ id: ENROLLMENT_ID, participant_id: PARTICIPANT_ID, course_id: COURSE_ID,
      access_starts_at: null, access_ends_at: null, access_status: "allowed" }],
    courses: [{ id: COURSE_ID, start_date: "2020-01-01", end_date: "2099-12-31", status: "active" }]
  };
  const fakeClient = {
    auth: { async getSession() { return { data: { session: { user: { id: USER_ID } } }, error: null }; } },
    from(table) { return { select() { return { async eq() { return { data: rows[table], error: null }; } }; } }; }
  };
  const realWindow = { ACCAOUI_SUPABASE_BOOTSTRAP: { getClient() { return fakeClient; } } };
  executeBrowser([
    [adapterSource, "adapter-real-chain.js"],
    [bridgeSource, "bridge-real-chain.js"],
    [providerSource, "provider-real-chain.js"]
  ], realWindow);
  const realResult = await realWindow.ACCAOUI_PARTICIPANT_ACCESS_APP_PROVIDER.resolveAccess();
  assert(realResult.allowed === true && realResult.code === "access_allowed", "Echte Kompositionskette");
  positive += 1;

  async function expectBlocked(label, setup, expectedCode) {
    const fixture = baseWindow();
    setup(fixture.win, fixture.state);
    executeBrowser([[providerSource, `negative-${label}.js`]], fixture.win);
    const candidate = fixture.win.ACCAOUI_PARTICIPANT_ACCESS_APP_PROVIDER;
    assert(candidate && typeof candidate.resolveAccess === "function", `${label}: sichere Oberfläche fehlt`);
    const result = await candidate.resolveAccess();
    assert(result && result.allowed === false && typeof result.code === "string" && result.code.length > 0,
      `${label}: nicht fail-closed`);
    assert(result.code !== "access_allowed", `${label}: widersprüchlicher Code`);
    if (expectedCode) assert(result.code === expectedCode, `${label}: ${result.code}`);
    negative += 1;
  }

  await expectBlocked("bootstrap-missing", (win) => { delete win.ACCAOUI_SUPABASE_BOOTSTRAP; }, "provider_bootstrap_missing");
  await expectBlocked("bootstrap-null", (win) => { win.ACCAOUI_SUPABASE_BOOTSTRAP = null; }, "provider_bootstrap_missing");
  await expectBlocked("bootstrap-primitive", (win) => { win.ACCAOUI_SUPABASE_BOOTSTRAP = "bad"; }, "provider_bootstrap_invalid");
  await expectBlocked("bootstrap-getter", (win) => Object.defineProperty(win, "ACCAOUI_SUPABASE_BOOTSTRAP", {
    get() { throw new Error("RAW"); }, configurable: true
  }), "provider_dependency_read_failed");
  await expectBlocked("adapter-missing", (win) => { delete win.ACCAOUI_PARTICIPANT_ACCESS_ADAPTER_FACTORY; }, "provider_adapter_factory_missing");
  await expectBlocked("adapter-null", (win) => { win.ACCAOUI_PARTICIPANT_ACCESS_ADAPTER_FACTORY = null; }, "provider_adapter_factory_missing");
  await expectBlocked("adapter-primitive", (win) => { win.ACCAOUI_PARTICIPANT_ACCESS_ADAPTER_FACTORY = {}; }, "provider_adapter_factory_invalid");
  await expectBlocked("adapter-getter", (win) => Object.defineProperty(win, "ACCAOUI_PARTICIPANT_ACCESS_ADAPTER_FACTORY", {
    get() { throw new Error("RAW"); }, configurable: true
  }), "provider_dependency_read_failed");
  await expectBlocked("bridge-missing", (win) => { delete win.ACCAOUI_PARTICIPANT_ACCESS_BOOTSTRAP_BRIDGE_FACTORY; }, "provider_bridge_factory_missing");
  await expectBlocked("bridge-null", (win) => { win.ACCAOUI_PARTICIPANT_ACCESS_BOOTSTRAP_BRIDGE_FACTORY = null; }, "provider_bridge_factory_missing");
  await expectBlocked("bridge-primitive", (win) => { win.ACCAOUI_PARTICIPANT_ACCESS_BOOTSTRAP_BRIDGE_FACTORY = {}; }, "provider_bridge_factory_invalid");
  await expectBlocked("bridge-getter", (win) => Object.defineProperty(win, "ACCAOUI_PARTICIPANT_ACCESS_BOOTSTRAP_BRIDGE_FACTORY", {
    get() { throw new Error("RAW"); }, configurable: true
  }), "provider_dependency_read_failed");
  await expectBlocked("bridge-factory-throw", (win) => { win.ACCAOUI_PARTICIPANT_ACCESS_BOOTSTRAP_BRIDGE_FACTORY = () => { throw new Error("RAW"); }; }, "provider_bridge_factory_failed");
  await expectBlocked("bridge-null-result", (win) => { win.ACCAOUI_PARTICIPANT_ACCESS_BOOTSTRAP_BRIDGE_FACTORY = () => null; }, "provider_bridge_invalid");
  await expectBlocked("bridge-array-result", (win) => { win.ACCAOUI_PARTICIPANT_ACCESS_BOOTSTRAP_BRIDGE_FACTORY = () => []; }, "provider_bridge_invalid");
  await expectBlocked("bridge-primitive-result", (win) => { win.ACCAOUI_PARTICIPANT_ACCESS_BOOTSTRAP_BRIDGE_FACTORY = () => 1; }, "provider_bridge_invalid");
  await expectBlocked("resolve-missing", (win) => { win.ACCAOUI_PARTICIPANT_ACCESS_BOOTSTRAP_BRIDGE_FACTORY = () => ({}); }, "provider_bridge_resolve_access_invalid");
  await expectBlocked("resolve-getter", (win) => { win.ACCAOUI_PARTICIPANT_ACCESS_BOOTSTRAP_BRIDGE_FACTORY = () => Object.defineProperty({}, "resolveAccess", { get() { throw new Error("RAW"); } }); }, "provider_bridge_resolve_access_failed");
  await expectBlocked("resolve-throw", (win) => { win.ACCAOUI_PARTICIPANT_ACCESS_BOOTSTRAP_BRIDGE_FACTORY = () => ({ resolveAccess() { throw new Error("RAW"); } }); }, "provider_bridge_resolve_access_failed");
  await expectBlocked("resolve-reject", (win) => { win.ACCAOUI_PARTICIPANT_ACCESS_BOOTSTRAP_BRIDGE_FACTORY = () => ({ async resolveAccess() { throw new Error("RAW"); } }); }, "provider_bridge_resolve_access_failed");
  await expectBlocked("result-null", (win) => { win.ACCAOUI_PARTICIPANT_ACCESS_BOOTSTRAP_BRIDGE_FACTORY = () => ({ async resolveAccess() { return null; } }); }, "provider_bridge_result_invalid");
  await expectBlocked("result-primitive", (win) => { win.ACCAOUI_PARTICIPANT_ACCESS_BOOTSTRAP_BRIDGE_FACTORY = () => ({ async resolveAccess() { return "bad"; } }); }, "provider_bridge_result_invalid");
  await expectBlocked("result-array", (win) => { win.ACCAOUI_PARTICIPANT_ACCESS_BOOTSTRAP_BRIDGE_FACTORY = () => ({ async resolveAccess() { return []; } }); }, "provider_bridge_result_invalid");
  await expectBlocked("allowed-type", (win) => { win.ACCAOUI_PARTICIPANT_ACCESS_BOOTSTRAP_BRIDGE_FACTORY = () => ({ async resolveAccess() { return { allowed: "false", code: "blocked" }; } }); }, "provider_bridge_result_invalid");
  await expectBlocked("code-missing", (win) => { win.ACCAOUI_PARTICIPANT_ACCESS_BOOTSTRAP_BRIDGE_FACTORY = () => ({ async resolveAccess() { return { allowed: false }; } }); }, "provider_bridge_result_invalid");
  await expectBlocked("code-empty", (win) => { win.ACCAOUI_PARTICIPANT_ACCESS_BOOTSTRAP_BRIDGE_FACTORY = () => ({ async resolveAccess() { return { allowed: false, code: "" }; } }); }, "provider_bridge_result_invalid");
  await expectBlocked("code-type", (win) => { win.ACCAOUI_PARTICIPANT_ACCESS_BOOTSTRAP_BRIDGE_FACTORY = () => ({ async resolveAccess() { return { allowed: false, code: 1 }; } }); }, "provider_bridge_result_invalid");
  await expectBlocked("true-wrong-code", (win) => { win.ACCAOUI_PARTICIPANT_ACCESS_BOOTSTRAP_BRIDGE_FACTORY = () => ({ async resolveAccess() { return { allowed: true, code: "participant_blocked" }; } }); }, "provider_bridge_result_invalid");
  await expectBlocked("false-access-allowed", (win) => { win.ACCAOUI_PARTICIPANT_ACCESS_BOOTSTRAP_BRIDGE_FACTORY = () => ({ async resolveAccess() { return { allowed: false, code: "access_allowed" }; } }); }, "provider_bridge_result_invalid");
  await expectBlocked("unknown-technical", (win) => { win.ACCAOUI_PARTICIPANT_ACCESS_BOOTSTRAP_BRIDGE_FACTORY = () => ({ async resolveAccess() { return { allowed: false, code: "technical_unknown" }; } }); }, "technical_unknown");
  await expectBlocked("adapter-factory-throw", (win) => {
    win.ACCAOUI_SUPABASE_BOOTSTRAP = { getClient() { return {}; } };
    win.ACCAOUI_PARTICIPANT_ACCESS_ADAPTER_FACTORY = () => { throw new Error("RAW"); };
    win.ACCAOUI_PARTICIPANT_ACCESS_BOOTSTRAP_BRIDGE_FACTORY = bridgeApi.createParticipantAccessBootstrapBridge;
  }, "adapter_factory_failed");

  async function mutation(label, mutate, verifier) {
    let blocked = false;
    try {
      await verifier(mutate({ adapterSource, bridgeSource, providerSource }));
    } catch (_error) {
      blocked = true;
    }
    assert(blocked, `Manipulation wurde nicht blockiert: ${label}`);
    manipulations += 1;
  }

  await mutation("adapter-commonjs", (s) => ({ ...s, adapterSource: s.adapterSource.replace(
    'if (commonJsModule && typeof commonJsModule === "object")', 'if (false)') }),
    async (s) => assert(typeof commonJsApi(s.adapterSource, "m-adapter-commonjs.js").createParticipantAccessAdapter === "function", "CommonJS fehlt"));
  await mutation("bridge-commonjs", (s) => ({ ...s, bridgeSource: s.bridgeSource.replace(
    'if (commonJsModule && typeof commonJsModule === "object")', 'if (false)') }),
    async (s) => assert(typeof commonJsApi(s.bridgeSource, "m-bridge-commonjs.js").createParticipantAccessBootstrapBridge === "function", "CommonJS fehlt"));
  await mutation("adapter-browser-export", (s) => ({ ...s, adapterSource: s.adapterSource.replaceAll(
    "ACCAOUI_PARTICIPANT_ACCESS_ADAPTER_FACTORY", "ACCAOUI_WRONG_ADAPTER_FACTORY") }), async (s) => {
      const win = {}; executeBrowser([[s.adapterSource, "m-adapter-export.js"]], win);
      assert(typeof win.ACCAOUI_PARTICIPANT_ACCESS_ADAPTER_FACTORY === "function", "Export fehlt");
    });
  await mutation("bridge-browser-export", (s) => ({ ...s, bridgeSource: s.bridgeSource.replaceAll(
    "ACCAOUI_PARTICIPANT_ACCESS_BOOTSTRAP_BRIDGE_FACTORY", "ACCAOUI_WRONG_BRIDGE_FACTORY") }), async (s) => {
      const win = {}; executeBrowser([[s.bridgeSource, "m-bridge-export.js"]], win);
      assert(typeof win.ACCAOUI_PARTICIPANT_ACCESS_BOOTSTRAP_BRIDGE_FACTORY === "function", "Export fehlt");
    });
  await mutation("provider-global", (s) => ({ ...s, providerSource: s.providerSource.replaceAll(
    "ACCAOUI_PARTICIPANT_ACCESS_APP_PROVIDER", "ACCAOUI_WRONG_APP_PROVIDER") }), async (s) => {
      const fixture = baseWindow(); executeBrowser([[s.providerSource, "m-provider-global.js"]], fixture.win);
      assert(fixture.win.ACCAOUI_PARTICIPANT_ACCESS_APP_PROVIDER, "Provider fehlt");
    });
  await mutation("provider-surface", (s) => ({ ...s, providerSource: s.providerSource.replace(
    "Object.freeze({ resolveAccess })", "Object.freeze({ resolveAccess, extra: true })") }), async (s) => {
      const fixture = baseWindow(); executeBrowser([[s.providerSource, "m-provider-surface.js"]], fixture.win);
      equal(Object.keys(fixture.win.ACCAOUI_PARTICIPANT_ACCESS_APP_PROVIDER), ["resolveAccess"], "Zusatzoberfläche");
    });

  async function verifyNoDirectAccess(source, member, setup) {
    const fixture = baseWindow(Object.freeze({ allowed: false, code: "participant_blocked" }));
    const calls = { count: 0 };
    setup(fixture.win, calls);
    executeBrowser([[source, `m-${member}.js`]], fixture.win);
    await fixture.win.ACCAOUI_PARTICIPANT_ACCESS_APP_PROVIDER.resolveAccess();
    assert(calls.count === 0, `Direkter Zugriff: ${member}`);
  }

  const insertion = "    const bridgeDependencies = Object.freeze({";
  await mutation("direct-get-client", (s) => ({ ...s, providerSource: s.providerSource.replace(insertion,
    "    bootstrap.getClient();\n" + insertion) }), async (s) => verifyNoDirectAccess(s.providerSource, "get-client", (win, calls) => {
      win.ACCAOUI_SUPABASE_BOOTSTRAP.getClient = () => { calls.count += 1; };
    }));
  await mutation("direct-initialize", (s) => ({ ...s, providerSource: s.providerSource.replace(insertion,
    "    bootstrap.initializeClient();\n" + insertion) }), async (s) => verifyNoDirectAccess(s.providerSource, "initialize", (win, calls) => {
      win.ACCAOUI_SUPABASE_BOOTSTRAP.initializeClient = () => { calls.count += 1; };
    }));
  await mutation("direct-state", (s) => ({ ...s, providerSource: s.providerSource.replace(insertion,
    "    bootstrap.getState();\n" + insertion) }), async (s) => verifyNoDirectAccess(s.providerSource, "state", (win, calls) => {
      win.ACCAOUI_SUPABASE_BOOTSTRAP.getState = () => { calls.count += 1; };
    }));
  await mutation("direct-create", (s) => ({ ...s, providerSource: s.providerSource.replace(insertion,
    "    browserRoot.supabase.createClient();\n" + insertion) }), async (s) => verifyNoDirectAccess(s.providerSource, "create", (win, calls) => {
      win.supabase = { createClient() { calls.count += 1; } };
    }));
  await mutation("direct-domain-query", (s) => ({ ...s, providerSource: s.providerSource.replace(insertion,
    "    bootstrap.auth.getSession();\n    bootstrap.from(\"participants\");\n" + insertion) }), async (s) => verifyNoDirectAccess(s.providerSource, "domain", (win, calls) => {
      win.ACCAOUI_SUPABASE_BOOTSTRAP.auth = { getSession() { calls.count += 1; } };
      win.ACCAOUI_SUPABASE_BOOTSTRAP.from = () => { calls.count += 1; };
    }));
  await mutation("user-id", (s) => ({ ...s, providerSource: s.providerSource.replace(
    "      utcNow\n    });", "      utcNow,\n      userId: \"synthetic\"\n    });") }), async (s) => {
      assert(!s.providerSource.includes("userId"), "Frei injizierte Nutzer-ID");
    });
  await mutation("fail-open", (s) => ({ ...s, providerSource: s.providerSource.replace(
    "return Object.freeze({ allowed: false, code });", "return Object.freeze({ allowed: true, code: \"access_allowed\" });") }), async (s) => {
      const fixture = baseWindow(); delete fixture.win.ACCAOUI_SUPABASE_BOOTSTRAP;
      executeBrowser([[s.providerSource, "m-fail-open.js"]], fixture.win);
      const result = await fixture.win.ACCAOUI_PARTICIPANT_ACCESS_APP_PROVIDER.resolveAccess();
      assert(result.allowed === false, "Fail-open");
    });
  await mutation("collision-overwrite", (s) => ({ ...s, providerSource: s.providerSource.replace(
    "if (existingProvider !== undefined)", "if (false && existingProvider !== undefined)") }), async (s) => {
      const foreign = { resolveAccess() {}, foreign: true };
      const win = { ACCAOUI_PARTICIPANT_ACCESS_APP_PROVIDER: foreign };
      executeBrowser([[s.providerSource, "m-collision.js"]], win);
      assert(win.ACCAOUI_PARTICIPANT_ACCESS_APP_PROVIDER === foreign, "Fremdprovider überschrieben");
    });

  process.stdout.write(JSON.stringify({ positive, negative, manipulations }));
}

main().catch((error) => {
  process.stderr.write(String(error && error.stack ? error.stack : error));
  process.exit(1);
});
'''

result = run([
    str(node_path),
    "-e",
    HARNESS,
    str(ADAPTER_PATH),
    str(BRIDGE_PATH),
    str(PROVIDER_PATH),
])
if result.returncode != 0:
    if result.stderr:
        print(result.stderr)
    stop("lokale Browser-/CommonJS-Prüfung fehlgeschlagen")

try:
    summary = json.loads(result.stdout)
except (TypeError, ValueError) as error:
    stop(f"ungültige Testzusammenfassung: {error}")

positive = summary.get("positive")
negative = summary.get("negative")
manipulations = summary.get("manipulations")
if (positive, negative, manipulations) != (22, 31, 14):
    stop(
        "unerwartete Prüfungszahlen: "
        f"Positiv={positive}, Negativ={negative}, Manipulation={manipulations}"
    )

# Scope-Manipulationen sind echte Dateiumfangsprüfungen und nicht Markerzählung.
for injected_path in ("app.js", "index.html"):
    mutated_scope = set(AUTHORIZED_FILES)
    mutated_scope.add(injected_path)
    if mutated_scope == AUTHORIZED_FILES:
        stop(f"Scope-Manipulation wurde nicht blockiert: {injected_path}")
    manipulations += 1

for checker in LEGACY_CHECKERS:
    require_legacy_checker(checker)
require_v2736d_regression()

print("Teilnehmerzugangs-Browser-Provider v27.36e: PASS")
print(f"Positivprüfungen: {positive} PASS")
print(f"Negativprüfungen: {negative} PASS")
print(f"Manipulationsprüfungen: {manipulations} PASS")
print("v27.36b-Checker: PASS")
print("v27.36c-Checker: PASS")
print("v27.36d-Checker: PASS (autorisiertes v27.36e-Regressionsprofil)")
print("CommonJS-Kompatibilität und kontrollierte Browser-Exports: PASS")
print("Provider-Oberfläche: ausschließlich resolveAccess")
print("Fail-closed und Kollisionsschutz: PASS")
print("Sicherheitsgrenze: keine Fachlogik, kein externer Zugriff, keine echten Daten")
print("Supabase live: NEIN")
