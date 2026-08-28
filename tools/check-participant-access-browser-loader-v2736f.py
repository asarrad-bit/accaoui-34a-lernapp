#!/usr/bin/env python3
"""Prüft den v27.36f-Browser-Loader ausschließlich lokal und synthetisch."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE_HEAD = "88337d5951bffdb3b1591ea5d6d9e5741a4c7477"
LOADER_ID = "accaoui-participant-access-browser-loader"
READY_NAME = "ACCAOUI_PARTICIPANT_ACCESS_BROWSER_LOADER_READY"

INDEX_PATH = ROOT / "index.html"
APP_PATH = ROOT / "app.js"
LOADER_PATH = ROOT / "data/supabase-participant-access-browser-loader.js"
ADAPTER_PATH = ROOT / "data/supabase-participant-access-adapter.js"
BRIDGE_PATH = ROOT / "data/supabase-participant-access-bootstrap-bridge.js"
PROVIDER_PATH = ROOT / "data/supabase-participant-access-browser-provider.js"
DOC_PATH = ROOT / "docs/PARTICIPANT_ACCESS_BROWSER_LOADER_V2736F.md"
PREFLIGHT_PATH = ROOT / "tools/preflight.py"

AUTHORIZED_FILES = {
    "index.html",
    "app.js",
    "data/supabase-participant-access-browser-loader.js",
    "tools/check-participant-access-browser-loader-v2736f.py",
    "docs/PARTICIPANT_ACCESS_BROWSER_LOADER_V2736F.md",
    "tools/preflight.py",
}

FROZEN_FILES = (
    "data/supabase-client-adapter.js",
    "data/supabase-client-bootstrap.js",
    "data/supabase-config-loader.js",
    "data/supabase-participant-access-adapter.js",
    "data/supabase-participant-access-bootstrap-bridge.js",
    "data/supabase-participant-access-browser-provider.js",
    "style.css",
    "questions.json",
)


class ContractError(RuntimeError):
    """Ein lokaler v27.36f-Vertrag wurde verletzt."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ContractError(message)


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


def baseline_bytes(relative_path: str) -> bytes:
    result = subprocess.run(
        ["git", "show", f"{BASE_HEAD}:{relative_path}"],
        cwd=ROOT,
        capture_output=True,
    )
    if result.returncode != 0:
        stop(f"Basisdatei kann nicht gelesen werden: {relative_path}")
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


def task_authorizes_v2736f() -> bool:
    lines = (ROOT / "docs/tasks/CURRENT_TASK.md").read_text(
        encoding="utf-8"
    ).splitlines()

    def single_value(prefix: str) -> str | None:
        values = [line[len(prefix):].strip() for line in lines if line.startswith(prefix)]
        return values[0] if len(values) == 1 else None

    expected_files = ", ".join(f"`{path}`" for path in (
        "index.html",
        "app.js",
        "data/supabase-participant-access-browser-loader.js",
        "tools/check-participant-access-browser-loader-v2736f.py",
        "docs/PARTICIPANT_ACCESS_BROWSER_LOADER_V2736F.md",
        "tools/preflight.py",
    ))
    return (
        single_value("Task-ID:") == "v27.36f"
        and single_value("Status:") == "AUTHORIZED"
        and single_value("Autorisiert:") == "JA"
        and single_value("Erlaubte Implementierungsdateien:") == expected_files
        and single_value("Commit erlaubt:") == "NEIN"
        and single_value("Push erlaubt:") == "NEIN"
    )


def validate_source_contract(
    index_text: str,
    app_text: str,
    loader_text: str,
    doc_text: str,
    preflight_text: str,
) -> None:
    loader_pattern = re.compile(
        rf'<script\b(?=[^>]*\bid=["\']{re.escape(LOADER_ID)}["\'])'
        rf'(?=[^>]*\bsrc=["\']data/supabase-participant-access-browser-loader\.js["\'])'
        r'(?=[^>]*\bdata-enabled=["\']false["\'])[^>]*>\s*</script>',
        re.IGNORECASE,
    )
    loader_tags = tuple(loader_pattern.finditer(index_text))
    require(len(loader_tags) == 1, "index.html benötigt exakt einen Default-off-Loader")
    require(index_text.count(LOADER_ID) == 1, "Loader-ID ist nicht eindeutig")
    require(
        index_text.count("data/supabase-participant-access-browser-loader.js") == 1,
        "Loader-Ressource ist nicht eindeutig",
    )
    app_tag = re.search(
        r'<script\b[^>]*\bsrc=["\']app\.js[^"\']*["\'][^>]*>\s*</script>',
        index_text,
        re.IGNORECASE,
    )
    require(app_tag is not None, "app.js-Script-Tag fehlt")
    between = index_text[loader_tags[0].end():app_tag.start()]
    require(
        loader_tags[0].end() <= app_tag.start() and not between.strip(),
        "Loader muss unmittelbar vor app.js stehen",
    )

    dependencies = (
        "data/supabase-participant-access-adapter.js",
        "data/supabase-participant-access-bootstrap-bridge.js",
        "data/supabase-participant-access-browser-provider.js",
    )
    positions = tuple(loader_text.find(path) for path in dependencies)
    require(
        all(position >= 0 for position in positions)
        and list(positions) == sorted(positions),
        "Ladefolge ist nicht Adapter -> Brücke -> Provider",
    )
    for marker in (
        LOADER_ID,
        'enabled !== "true"',
        READY_NAME,
        "ACCAOUI_PARTICIPANT_ACCESS_ADAPTER_FACTORY",
        "ACCAOUI_PARTICIPANT_ACCESS_BOOTSTRAP_BRIDGE_FACTORY",
        "ACCAOUI_PARTICIPANT_ACCESS_APP_PROVIDER",
        "requested: true",
        "ready: true",
        'status: "ready"',
        "ready: false",
        'status: "error"',
    ):
        require(marker in loader_text, f"Loader-Vertragsmarker fehlt: {marker}")
    require("Promise.all" not in loader_text, "Parallele Scriptladung ist unzulässig")
    for token in (
        "localStorage",
        "sessionStorage",
        "document.cookie",
        "location.search",
        "initializeClient(",
        "createClient(",
        "getSession(",
        ".from(",
        "fetch(",
        "XMLHttpRequest",
        "WebSocket",
        "userId",
    ):
        require(token.casefold() not in loader_text.casefold(), f"Loader verletzt Sicherheitsgrenze: {token}")

    for marker in (
        LOADER_ID,
        READY_NAME,
        "isParticipantAccessBrowserLoaderRequestedV2736F",
        "awaitParticipantAccessBrowserLoaderV2736F",
        "access_error",
        "ACCAOUI_PARTICIPANT_ACCESS_APP_PROVIDER",
        "resolveAccess",
    ):
        require(marker in app_text, f"app.js-Vertragsmarker fehlt: {marker}")

    for marker in (
        "Ziel",
        "Schalter",
        "Ladefolge",
        "Readiness",
        "Fail-closed-Grenze",
        "lokale synthetische Tests",
        "Supabase live: NEIN",
        "echte Keys: NEIN",
        "echte Teilnehmerdaten: NEIN",
    ):
        require(marker in doc_text, f"Dokumentationsmarker fehlt: {marker}")
    require(
        preflight_text.count("check-participant-access-browser-loader-v2736f.py") >= 2,
        "v27.36f-Checker ist nicht vollständig im Preflight eingebunden",
    )
    require(
        "check_participant_access_browser_loader_v2736f()" in preflight_text,
        "v27.36f-Checker wird im normalen Preflight-Ablauf nicht aufgerufen",
    )


def require_regression(relative_path: str) -> None:
    result = run([sys.executable, relative_path])
    if result.returncode != 0:
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr)
        stop(f"Bestandschecker fehlgeschlagen: {relative_path}")


def validate_v2736e_regression_sources(
    adapter_source: bytes,
    bridge_source: bytes,
    provider_source: bytes,
) -> None:
    sources = {
        "data/supabase-participant-access-adapter.js": adapter_source,
        "data/supabase-participant-access-bootstrap-bridge.js": bridge_source,
        "data/supabase-participant-access-browser-provider.js": provider_source,
    }
    for relative_path, source in sources.items():
        require(
            source == baseline_bytes(relative_path),
            f"v27.36e-Bestandsmodul wurde gegenüber {BASE_HEAD} verändert: {relative_path}",
        )

    adapter_text = adapter_source.decode("utf-8")
    bridge_text = bridge_source.decode("utf-8")
    provider_text = provider_source.decode("utf-8")
    for marker in (
        "module.exports",
        "createParticipantAccessAdapter",
        "ACCAOUI_PARTICIPANT_ACCESS_ADAPTER_FACTORY",
    ):
        require(marker in adapter_text, f"v27.36e-Adaptervertrag fehlt: {marker}")
    for marker in (
        "module.exports",
        "createParticipantAccessBootstrapBridge",
        "ACCAOUI_PARTICIPANT_ACCESS_BOOTSTRAP_BRIDGE_FACTORY",
    ):
        require(marker in bridge_text, f"v27.36e-Brückenvertrag fehlt: {marker}")
    for marker in (
        "ACCAOUI_PARTICIPANT_ACCESS_APP_PROVIDER",
        "Object.freeze({ resolveAccess })",
        "existingProvider !== undefined",
        "access_allowed",
        "fail-closed",
    ):
        require(marker in provider_text, f"v27.36e-Providervertrag fehlt: {marker}")
    for token in (
        "initializeClient",
        "createClient",
        "auth.getSession",
        ".from(",
        "participants",
        "enrollments",
        "courses",
        "userId",
        "process.env",
    ):
        require(token not in provider_text, f"v27.36e-Provider verletzt Sicherheitsgrenze: {token}")


def require_v2736e_regression() -> int:
    """Führt den echten v27.36e-Vertrag im engen v27.36f-Scope aus."""

    adapter_source = ADAPTER_PATH.read_bytes()
    bridge_source = BRIDGE_PATH.read_bytes()
    provider_source = PROVIDER_PATH.read_bytes()
    validate_v2736e_regression_sources(
        adapter_source,
        bridge_source,
        provider_source,
    )

    regression_mutations = (
        (adapter_source + b"\n// synthetic mutation\n", bridge_source, provider_source, "Adapter verändert"),
        (adapter_source, bridge_source + b"\n// synthetic mutation\n", provider_source, "Brücke verändert"),
        (adapter_source, bridge_source, provider_source + b"\n// synthetic mutation\n", "Provider verändert"),
        (adapter_source, bridge_source, provider_source.replace(b"Object.freeze({ resolveAccess })", b"Object.freeze({})", 1), "resolveAccess entfernt"),
        (adapter_source, bridge_source, provider_source.replace(b"existingProvider !== undefined", b"false", 1), "Überschreibschutz entfernt"),
        (adapter_source, bridge_source, provider_source.replace(b"allowed: false, code", b"allowed: true, code", 1), "fail-closed zu allow"),
        (adapter_source, bridge_source, provider_source + b"\ninitializeClient();\n", "initializeClient eingeschleust"),
        (adapter_source, bridge_source, provider_source + b"\ncreateClient();\n", "createClient eingeschleust"),
        (adapter_source, bridge_source, provider_source + b"\nauth.getSession();\n", "Auth-Abfrage eingeschleust"),
        (adapter_source, bridge_source, provider_source + b"\nclient.from('participants');\n", "Tabellenabfrage eingeschleust"),
    )
    blocked_mutations = 0
    for mutated_adapter, mutated_bridge, mutated_provider, label in regression_mutations:
        try:
            validate_v2736e_regression_sources(
                mutated_adapter,
                mutated_bridge,
                mutated_provider,
            )
        except ContractError:
            blocked_mutations += 1
            continue
        stop(f"v27.36e-Regressionsmanipulation wurde nicht blockiert: {label}")

    checker_path = ROOT / "tools/check-participant-access-browser-provider-v2736e.py"
    source = checker_path.read_text(encoding="utf-8")
    original = '''FROZEN_FILES = (
    "index.html",
    "app.js",
    "style.css",
    "data/supabase-client-bootstrap.js",
    "data/supabase-client-adapter.js",
)'''
    replacement = '''FROZEN_FILES = (
    "style.css",
    "data/supabase-client-bootstrap.js",
    "data/supabase-client-adapter.js",
)'''
    require(source.count(original) == 1, "v27.36e-Regressionsprofil ist nicht eindeutig anwendbar")
    source = source.replace(original, replacement, 1)
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
        stop("v27.36e-Regressionsprofil fehlgeschlagen")
    return blocked_mutations


required_paths = (
    INDEX_PATH,
    APP_PATH,
    LOADER_PATH,
    ADAPTER_PATH,
    BRIDGE_PATH,
    PROVIDER_PATH,
    DOC_PATH,
    PREFLIGHT_PATH,
)
for required_path in required_paths:
    if not required_path.is_file():
        stop(f"Pflichtdatei fehlt: {required_path.relative_to(ROOT)}")

if not task_authorizes_v2736f():
    stop("CURRENT_TASK autorisiert v27.36f nicht exakt")
if changed_paths() != AUTHORIZED_FILES:
    stop("Working-Tree-Dateimenge ist nicht exakt der autorisierte v27.36f-Scope")

for relative_path in FROZEN_FILES:
    if (ROOT / relative_path).read_bytes() != baseline_bytes(relative_path):
        stop(f"Eingefrorene Bestandsdatei wurde verändert: {relative_path}")

index_text = INDEX_PATH.read_text(encoding="utf-8")
app_text = APP_PATH.read_text(encoding="utf-8")
loader_text = LOADER_PATH.read_text(encoding="utf-8")
doc_text = DOC_PATH.read_text(encoding="utf-8")
preflight_text = PREFLIGHT_PATH.read_text(encoding="utf-8")

try:
    validate_source_contract(index_text, app_text, loader_text, doc_text, preflight_text)
except ContractError as error:
    stop(str(error))

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

const loaderSource = fs.readFileSync(process.argv[1], "utf8");
const adapterSource = fs.readFileSync(process.argv[2], "utf8");
const bridgeSource = fs.readFileSync(process.argv[3], "utf8");
const providerSource = fs.readFileSync(process.argv[4], "utf8");
const appSource = fs.readFileSync(process.argv[5], "utf8");

const LOADER_ID = "accaoui-participant-access-browser-loader";
const READY_NAME = "ACCAOUI_PARTICIPANT_ACCESS_BROWSER_LOADER_READY";
const paths = [
  "data/supabase-participant-access-adapter.js",
  "data/supabase-participant-access-bootstrap-bridge.js",
  "data/supabase-participant-access-browser-provider.js"
];
const originalResources = new Map([
  [paths[0], adapterSource],
  [paths[1], bridgeSource],
  [paths[2], providerSource]
]);

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

function equal(actual, expected, message) {
  assert(JSON.stringify(actual) === JSON.stringify(expected),
    `${message}: ${JSON.stringify(actual)} !== ${JSON.stringify(expected)}`);
}

function own(object, key) {
  return Object.prototype.hasOwnProperty.call(object, key);
}

function execute(source, context, filename) {
  vm.runInContext(source, context, { filename });
}

function createLoaderFixture(options = {}) {
  const state = { loads: [], maxActive: 0, active: 0 };
  const browserWindow = options.window || { ACCAOUI_SUPABASE_BOOTSTRAP: {} };
  const resources = new Map(originalResources);
  for (const [path, source] of Object.entries(options.resources || {})) {
    resources.set(path, source);
  }
  const loaderElement = {
    parentNode: {
      insertBefore(script, reference) {
        assert(reference === loaderElement, "Script nicht relativ zum Loader eingefügt");
        state.loads.push(script.src);
        state.active += 1;
        state.maxActive = Math.max(state.maxActive, state.active);
        Promise.resolve().then(() => {
          state.active -= 1;
          if ((options.failPaths || []).includes(script.src)) {
            script.onerror();
            return;
          }
          const source = resources.get(script.src);
          if (source === undefined) {
            script.onerror();
            return;
          }
          execute(source, context, script.src);
          script.onload();
        }).catch(() => script.onerror());
      }
    },
    getAttribute(name) {
      return name === "data-enabled" ? options.enabled : null;
    }
  };
  const documentObject = {
    getElementById(id) {
      return id === LOADER_ID && !options.missingTag ? loaderElement : null;
    },
    createElement(name) {
      assert(name === "script", "Loader erstellt unerwartetes Element");
      return {};
    }
  };
  const context = vm.createContext({
    window: browserWindow,
    self: browserWindow,
    document: documentObject,
    console: { log() {}, info() {}, warn() {}, error() {} },
    Promise,
    Object,
    Array,
    String,
    Number,
    Boolean,
    Date,
    Error,
    setTimeout,
    clearTimeout
  });
  if (options.readinessGetterThrows) {
    Object.defineProperty(browserWindow, READY_NAME, {
      configurable: true,
      get() { throw new Error("synthetic readiness getter"); }
    });
  } else if (own(options, "existingReadiness")) {
    browserWindow[READY_NAME] = options.existingReadiness;
  }
  execute(options.source || loaderSource, context, "browser-loader.js");
  let readiness;
  try { readiness = browserWindow[READY_NAME]; } catch (_error) { readiness = undefined; }
  return { state, window: browserWindow, readiness };
}

async function settle(fixture) {
  return fixture.readiness === undefined ? undefined : await fixture.readiness;
}

async function runAppCase(options = {}) {
  const state = {
    starts: 0,
    renders: 0,
    resolves: 0,
    providerReads: 0,
    readinessReads: 0,
    notices: []
  };
  const win = {};
  if (options.readinessGetterThrows) {
    Object.defineProperty(win, READY_NAME, {
      get() { state.readinessReads += 1; throw new Error("synthetic readiness getter"); }
    });
  } else if (own(options, "readiness")) {
    Object.defineProperty(win, READY_NAME, {
      get() { state.readinessReads += 1; return options.readiness; }
    });
  }
  if (options.providerGetterThrows) {
    Object.defineProperty(win, "ACCAOUI_PARTICIPANT_ACCESS_APP_PROVIDER", {
      get() { state.providerReads += 1; throw new Error("synthetic provider getter"); }
    });
  } else if (own(options, "provider")) {
    Object.defineProperty(win, "ACCAOUI_PARTICIPANT_ACCESS_APP_PROVIDER", {
      get() { state.providerReads += 1; return options.provider; }
    });
  } else if (options.providerAbsent !== true) {
    Object.defineProperty(win, "ACCAOUI_PARTICIPANT_ACCESS_APP_PROVIDER", {
      get() {
        state.providerReads += 1;
        return {
          async resolveAccess() {
            state.resolves += 1;
            if (options.providerRejects) throw new Error("synthetic provider reject");
            return options.providerResult;
          }
        };
      }
    });
  }
  const loaderElement = {
    getAttribute(name) {
      return name === "data-enabled" ? options.enabled : null;
    }
  };
  const documentObject = {
    addEventListener() {},
    getElementById(id) {
      return id === LOADER_ID && !options.missingTag ? loaderElement : null;
    }
  };
  const context = vm.createContext({
    window: win,
    document: documentObject,
    localStorage: {
      getItem(key) {
        return key === "accaoui_auth_guard_test_state"
          ? (options.localGuard || "")
          : null;
      },
      setItem() {},
      removeItem() {}
    },
    console: { log() {}, info() {}, warn() {}, error() {} },
    setTimeout,
    clearTimeout,
    setInterval,
    clearInterval,
    Date,
    Math,
    JSON,
    Object,
    Array,
    String,
    Number,
    Boolean,
    Promise
  });
  execute(appSource + `
    ;globalThis.__v2736fTestApi = {
      run: initAuthFlow,
      setHooks(startHook, renderHook, healthHook) {
        startLocalApp = startHook;
        renderLoginOrAccessNotice = renderHook;
        getSupabaseAdapterHealthState = healthHook;
      }
    };
  `, context, "app.js");
  context.__v2736fTestApi.setHooks(
    () => { state.starts += 1; },
    (notice) => { state.renders += 1; state.notices.push(notice); },
    () => ({
      status: "local_adapter_ready",
      isSupabaseLive: false,
      isLocalAccessAllowed: true,
      reason: "synthetic"
    })
  );
  await context.__v2736fTestApi.run();
  return state;
}

function assertStarted(state, label) {
  assert(state.starts === 1, `${label}: lokaler Start nicht exakt einmal`);
  assert(state.renders === 0, `${label}: unerwarteter Zugangshinweis`);
}

function assertAccessError(state, label) {
  assert(state.starts === 0, `${label}: unzulässiger lokaler Fallback`);
  assert(state.renders === 1, `${label}: Zugangshinweis nicht exakt einmal`);
  assert(state.notices[0].status === "access_error", `${label}: nicht generisch access_error`);
}

async function main() {
  let positive = 0;
  let negative = 0;
  let manipulations = 0;

  for (const value of ["false", "", "TRUE", "True", " true", "true ", "1", null, undefined]) {
    const fixture = createLoaderFixture({ enabled: value });
    assert(fixture.state.loads.length === 0, `Default/off lädt Ressourcen: ${String(value)}`);
    assert(!own(fixture.window, READY_NAME), `Default/off installiert Readiness: ${String(value)}`);
    assert(!own(fixture.window, "ACCAOUI_PARTICIPANT_ACCESS_APP_PROVIDER"), `Default/off installiert Provider: ${String(value)}`);
    positive += 1;
  }

  const valid = createLoaderFixture({ enabled: "true" });
  assert(valid.readiness && typeof valid.readiness.then === "function", "Readiness nicht synchron installiert");
  assert(valid.state.loads.length === 1, "Erster Load wurde nicht synchron angestoßen");
  const validResult = await settle(valid);
  equal(valid.state.loads, paths, "Feste Ladefolge");
  assert(valid.state.maxActive === 1, "Scriptladung war parallel");
  equal(validResult, { requested: true, ready: true, status: "ready" }, "Readiness-Erfolg");
  equal(Object.keys(validResult).sort(), ["ready", "requested", "status"], "Readiness-Oberfläche");
  assert(typeof valid.window.ACCAOUI_PARTICIPANT_ACCESS_APP_PROVIDER.resolveAccess === "function", "Provider fehlt nach Readiness");
  positive += 5;

  const collisionValue = Object.freeze({ foreign: true });
  const collision = createLoaderFixture({ enabled: "true", existingReadiness: collisionValue });
  assert(collision.window[READY_NAME] === collisionValue, "Readiness-Kollision überschrieben");
  assert(collision.state.loads.length === 0, "Kollision startete Ressourcen");
  positive += 2;

  const offApp = await runAppCase({ enabled: "false", providerAbsent: true });
  assertStarted(offApp, "data-enabled=false");
  assert(offApp.readinessReads === 0 && offApp.providerReads === 0, "Off-Pfad las Browser-Kette");
  positive += 2;

  const missingTagApp = await runAppCase({ missingTag: true, providerAbsent: true });
  assertStarted(missingTagApp, "fehlender Default-off-Tag");
  positive += 1;

  const successState = Object.freeze({ requested: true, ready: true, status: "ready" });
  const allowedApp = await runAppCase({
    enabled: "true",
    readiness: Promise.resolve(successState),
    providerResult: { allowed: true, code: "access_allowed" }
  });
  assertStarted(allowedApp, "aktivierter access_allowed-Pfad");
  assert(allowedApp.resolves === 1 && allowedApp.providerReads === 1, "Provider nicht exakt einmal delegiert");
  positive += 2;

  const mapping = {
    session_missing: "login_required",
    session_invalid: "login_required",
    session_user_missing: "login_required",
    session_user_id_invalid: "login_required",
    participant_blocked: "blocked",
    enrollment_blocked: "blocked",
    participant_expired: "expired",
    enrollment_expired: "expired",
    enrollment_access_ended: "expired",
    course_ended: "expired",
    participant_completed: "no_course",
    enrollment_missing: "no_course",
    enrollment_completed: "no_course",
    enrollment_access_not_started: "no_course",
    course_missing: "no_course",
    course_inactive: "no_course",
    course_archived: "no_course",
    course_not_started: "no_course"
  };
  for (const [code, status] of Object.entries(mapping)) {
    const state = await runAppCase({
      enabled: "true",
      readiness: Promise.resolve(successState),
      providerResult: { allowed: false, code }
    });
    assert(state.starts === 0 && state.renders === 1, `${code}: nicht blockiert`);
    assert(state.notices[0].status === status, `${code}: falsches Mapping`);
    assert(state.resolves === 1, `${code}: Provider nicht exakt einmal`);
    positive += 1;
  }

  const guard = await runAppCase({
    enabled: "true",
    readinessGetterThrows: true,
    providerGetterThrows: true,
    localGuard: "blocked"
  });
  assert(guard.starts === 0 && guard.renders === 1, "Lokaler Auth-Guard blockiert nicht");
  assert(guard.readinessReads === 0 && guard.providerReads === 0, "Lokaler Auth-Guard verlor Vorrang");
  positive += 2;

  async function loaderFailure(label, options, expectedLoads) {
    const fixture = createLoaderFixture({ enabled: "true", ...options });
    const result = await settle(fixture);
    equal(result, { requested: true, ready: false, status: "error" }, `${label}: Fehlerzustand`);
    equal(Object.keys(result).sort(), ["ready", "requested", "status"], `${label}: Rohdatenleck`);
    if (expectedLoads !== undefined) assert(fixture.state.loads.length === expectedLoads, `${label}: falsche Loadzahl`);
    negative += 1;
  }

  await loaderFailure("Adapter-Ladefehler", { failPaths: [paths[0]] }, 1);
  await loaderFailure("Adapter fehlt", { resources: { [paths[0]]: "" } }, 1);
  await loaderFailure("Adapter ungültig", { resources: { [paths[0]]: "window.ACCAOUI_PARTICIPANT_ACCESS_ADAPTER_FACTORY = {};" } }, 1);
  await loaderFailure("Brücken-Ladefehler", { failPaths: [paths[1]] }, 2);
  await loaderFailure("Brücke fehlt", { resources: { [paths[1]]: "" } }, 2);
  await loaderFailure("Brücke ungültig", { resources: { [paths[1]]: "window.ACCAOUI_PARTICIPANT_ACCESS_BOOTSTRAP_BRIDGE_FACTORY = {};" } }, 2);
  await loaderFailure("Provider-Ladefehler", { failPaths: [paths[2]] }, 3);
  await loaderFailure("Provider fehlt", { resources: { [paths[2]]: "" } }, 3);
  await loaderFailure("Provider null", { resources: { [paths[2]]: "window.ACCAOUI_PARTICIPANT_ACCESS_APP_PROVIDER = null;" } }, 3);
  await loaderFailure("resolveAccess fehlt", { resources: { [paths[2]]: "window.ACCAOUI_PARTICIPANT_ACCESS_APP_PROVIDER = {};" } }, 3);
  await loaderFailure("resolveAccess ungültig", { resources: { [paths[2]]: "window.ACCAOUI_PARTICIPANT_ACCESS_APP_PROVIDER = { resolveAccess: true };" } }, 3);

  async function appFailure(label, options) {
    const state = await runAppCase({ enabled: "true", ...options });
    assertAccessError(state, label);
    negative += 1;
  }

  await appFailure("Readiness fehlt", { providerAbsent: true });
  await appFailure("Readiness null", { readiness: null, providerAbsent: true });
  await appFailure("Readiness Plain-Object", { readiness: successState, providerAbsent: true });
  await appFailure("Readiness Getter wirft", { readinessGetterThrows: true, providerAbsent: true });
  await appFailure("Readiness rejected", { readiness: Promise.reject(new Error("synthetic")), providerAbsent: true });
  await appFailure("Readiness Ergebnis null", { readiness: Promise.resolve(null), providerAbsent: true });
  await appFailure("Readiness wrong requested", { readiness: Promise.resolve({ requested: false, ready: true, status: "ready" }), providerAbsent: true });
  await appFailure("Readiness wrong ready", { readiness: Promise.resolve({ requested: true, ready: false, status: "ready" }), providerAbsent: true });
  await appFailure("Readiness wrong status", { readiness: Promise.resolve({ requested: true, ready: true, status: "error" }), providerAbsent: true });
  await appFailure("Readiness Zusatzfeld", { readiness: Promise.resolve({ requested: true, ready: true, status: "ready", detail: "raw" }), providerAbsent: true });
  await appFailure("Provider fehlt nach Ready", { readiness: Promise.resolve(successState), providerAbsent: true });
  await appFailure("Provider null nach Ready", { readiness: Promise.resolve(successState), provider: null });
  await appFailure("Provider resolve fehlt", { readiness: Promise.resolve(successState), provider: {} });
  await appFailure("Provider wirft", { readiness: Promise.resolve(successState), providerRejects: true });
  await appFailure("Provider Ergebnis ungültig", { readiness: Promise.resolve(successState), providerResult: { allowed: true, code: "participant_blocked" } });
  await appFailure("Provider technischer Code", { readiness: Promise.resolve(successState), providerResult: { allowed: false, code: "technical_internal" } });

  async function mutation(label, mutate, verifier) {
    let blocked = false;
    try { await verifier(mutate(loaderSource)); } catch (_error) { blocked = true; }
    assert(blocked, `Manipulation wurde nicht blockiert: ${label}`);
    manipulations += 1;
  }

  await mutation("nonexact-accepted", (source) => source.replace('enabled !== "true"', 'enabled !== "TRUE"'), async (source) => {
    const fixture = createLoaderFixture({ enabled: "TRUE", source });
    assert(fixture.state.loads.length === 0, "Nicht-exakter Wert aktiviert");
  });
  await mutation("adapter-check-removed", (source) => source.replace('typeof browserRoot.ACCAOUI_PARTICIPANT_ACCESS_ADAPTER_FACTORY !==\n        "function"', 'false'), async (source) => {
    const fixture = createLoaderFixture({ enabled: "true", source, resources: { [paths[0]]: "" } });
    await settle(fixture);
    assert(fixture.state.loads.length === 1, "Ohne Adapterprüfung weitergeladen");
  });
  await mutation("bridge-check-removed", (source) => source.replace('typeof browserRoot\n          .ACCAOUI_PARTICIPANT_ACCESS_BOOTSTRAP_BRIDGE_FACTORY !==\n        "function"', 'false'), async (source) => {
    const fixture = createLoaderFixture({ enabled: "true", source, resources: { [paths[1]]: "" } });
    await settle(fixture);
    assert(fixture.state.loads.length === 2, "Ohne Brückenprüfung weitergeladen");
  });
  await mutation("provider-check-removed", (source) => source.replace('typeof provider.resolveAccess !== "function"', 'false'), async (source) => {
    const fixture = createLoaderFixture({ enabled: "true", source, resources: { [paths[2]]: "window.ACCAOUI_PARTICIPANT_ACCESS_APP_PROVIDER = {};" } });
    const result = await settle(fixture);
    assert(result.ready === false, "Ungültiger Provider wurde ready");
  });
  await mutation("fail-open-ready", (source) => source.replace('ready: false,\n        status: "error"', 'ready: true,\n        status: "ready"'), async (source) => {
    const fixture = createLoaderFixture({ enabled: "true", source, failPaths: [paths[0]] });
    const result = await settle(fixture);
    assert(result.ready === false, "Fehler wurde ready");
  });
  await mutation("readiness-overwrite", (source) => source.replace('if (existingReadiness !== undefined)', 'if (false && existingReadiness !== undefined)'), async (source) => {
    const foreign = { foreign: true };
    const fixture = createLoaderFixture({ enabled: "true", source, existingReadiness: foreign });
    assert(fixture.window[READY_NAME] === foreign, "Kollision überschrieben");
  });
  await mutation("raw-error", (source) => source.replace('status: "error"', 'status: String(_error)'), async (source) => {
    const fixture = createLoaderFixture({ enabled: "true", source, failPaths: [paths[0]] });
    const result = await settle(fixture);
    equal(result, { requested: true, ready: false, status: "error" }, "Rohfehler veröffentlicht");
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
    str(LOADER_PATH),
    str(ADAPTER_PATH),
    str(BRIDGE_PATH),
    str(PROVIDER_PATH),
    str(APP_PATH),
])
if result.returncode != 0:
    if result.stderr:
        print(result.stderr)
    stop("lokale Loader-/App-Browserprüfung fehlgeschlagen")

try:
    summary = json.loads(result.stdout)
except (TypeError, ValueError) as error:
    stop(f"ungültige Testzusammenfassung: {error}")

positive = summary.get("positive")
negative = summary.get("negative")
manipulations = summary.get("manipulations")
if not all(isinstance(value, int) for value in (positive, negative, manipulations)):
    stop("Prüfungszahlen fehlen")
if positive < 40 or negative < 25 or manipulations < 7:
    stop(
        "Mindestumfang der Laufzeitprüfungen unterschritten: "
        f"Positiv={positive}, Negativ={negative}, Manipulation={manipulations}"
    )

# Zusätzliche echte Vertragsmutationen gegen Index, Loader, App, Bericht und Preflight.
source_mutations = (
    (index_text.replace('data-enabled="false"', 'data-enabled="true"', 1), app_text, loader_text, doc_text, preflight_text, "Default true"),
    (index_text.replace(f'id="{LOADER_ID}"', 'id="wrong-loader"', 1), app_text, loader_text, doc_text, preflight_text, "Loader-ID"),
    (index_text.replace('<script src="app.js?v=24.8"></script>', '<script src="other.js"></script>', 1), app_text, loader_text, doc_text, preflight_text, "app.js-Tag"),
    (index_text, app_text, loader_text.replace("data/supabase-participant-access-adapter.js", "data/wrong-adapter.js", 1), doc_text, preflight_text, "Adapterpfad"),
    (index_text, app_text, loader_text.replace("data/supabase-participant-access-bootstrap-bridge.js", "data/wrong-bridge.js", 1), doc_text, preflight_text, "Brückenpfad"),
    (index_text, app_text, loader_text.replace("data/supabase-participant-access-browser-provider.js", "data/wrong-provider.js", 1), doc_text, preflight_text, "Providerpfad"),
    (index_text, app_text, loader_text + "\nPromise.all([]);\n", doc_text, preflight_text, "Parallelladung"),
    (index_text, app_text, loader_text + "\nlocalStorage.getItem('flag');\n", doc_text, preflight_text, "Storage-Schalter"),
    (index_text, app_text.replace(READY_NAME, "WRONG_READY"), loader_text, doc_text, preflight_text, "App-Readiness"),
    (index_text, app_text.replace("access_error", "internal_error"), loader_text, doc_text, preflight_text, "generischer App-Fehler"),
    (index_text, app_text, loader_text, doc_text.replace("Fail-closed-Grenze", "Fehlergrenze", 1), preflight_text, "Berichtsgrenze"),
    (index_text, app_text, loader_text, doc_text.replace("lokale synthetische Tests", "synthetische Tests", 1), preflight_text, "lokale synthetische Tests"),
    (index_text, app_text, loader_text, doc_text, preflight_text.replace("check-participant-access-browser-loader-v2736f.py", "removed-checker.py"), "Preflight-Einbindung"),
    (index_text, app_text, loader_text.replace('enabled !== "true"', 'enabled !== "TRUE"', 1), doc_text, preflight_text, "exaktes true"),
    (index_text, app_text, loader_text.replace("ACCAOUI_PARTICIPANT_ACCESS_APP_PROVIDER", "WRONG_PROVIDER"), doc_text, preflight_text, "Provideroberfläche"),
)
for args in source_mutations:
    try:
        validate_source_contract(*args[:-1])
    except ContractError:
        manipulations += 1
        continue
    stop(f"Quellmanipulation wurde nicht blockiert: {args[-1]}")

require_regression("tools/check-supabase-participant-access-adapter.py")
require_regression("tools/check-supabase-participant-access-bootstrap-bridge.py")
manipulations += require_v2736e_regression()

print("Teilnehmerzugangs-Browser-Loader v27.36f: PASS")
print(f"Positivprüfungen: {positive} PASS")
print(f"Negativprüfungen: {negative} PASS")
print(f"Manipulationsprüfungen: {manipulations} PASS")
print("v27.36b-Checker: PASS")
print("v27.36c-Checker: PASS")
print("v27.36d-Checker: PASS (enges v27.36e/v27.36f-Regressionsprofil)")
print("v27.36e-Checker: PASS (enges v27.36f-Regressionsprofil)")
print("Default data-enabled=false und ausschließlich exaktes true: PASS")
print("Feste Ladefolge und Readiness-Grenze: PASS")
print("Angeforderte Aktivierung fail-closed; kein Fallback: PASS")
print("Supabase live: NEIN")
