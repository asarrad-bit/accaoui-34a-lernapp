#!/usr/bin/env python3
"""Prüft den v27.37d-Auth-/Session-Browser-Provider lokal und synthetisch."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE_HEAD = "28b17480d1b99ccef7a6f4b78ed9bc32091109ef"

PROVIDER_PATH = (
    ROOT / "data/supabase-participant-auth-session-browser-provider.js"
)
TASK_PATH = ROOT / "docs/tasks/CURRENT_TASK.md"

IMPLEMENTATION_FILES = {
    "data/supabase-participant-auth-session-browser-provider.js",
    "tools/check-participant-auth-session-browser-provider-v2737d.py",
    "docs/PARTICIPANT_AUTH_SESSION_BROWSER_PROVIDER_V2737D.md",
    "tools/preflight.py",
}

FROZEN_FILES = (
    "index.html",
    "app.js",
    "data/supabase-participant-auth-session-adapter.js",
    "data/supabase-participant-auth-session-bootstrap-bridge.js",
)


def stop(message: str) -> None:
    print(f"STOPP: {message}")
    raise SystemExit(1)


def run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )


def git_output(args: list[str]) -> str:
    result = run(["git", *args])
    if result.returncode != 0:
        stop("Git-Prüfung fehlgeschlagen: " + " ".join(args))
    return result.stdout


def changed_paths() -> set[str]:
    paths = {
        line.strip().replace("\\", "/")
        for line in git_output(
            ["diff", "--name-only", BASE_HEAD]
        ).splitlines()
        if line.strip()
    }
    paths.update(
        line.strip().replace("\\", "/")
        for line in git_output(
            ["ls-files", "--others", "--exclude-standard"]
        ).splitlines()
        if line.strip()
    )
    return paths


def baseline_bytes(path: str) -> bytes:
    result = subprocess.run(
        ["git", "show", f"{BASE_HEAD}:{path}"],
        cwd=ROOT,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        stop(f"Basisdatei nicht lesbar: {path}")
    return result.stdout


def require_authorized_task() -> None:
    try:
        text = TASK_PATH.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        stop("CURRENT_TASK nicht lesbar")

    required = (
        "Task-ID: v27.37d",
        "Status: AUTHORIZED",
        "Autorisiert: JA",
        "Titel: v27.37d – Isolierter Browser-Provider für "
        "Teilnehmer-Auth-/Session-Kette",
        "Commit erlaubt: NEIN",
        "Push erlaubt: NEIN",
    )

    for marker in required:
        if marker not in text:
            stop(f"CURRENT_TASK-Vertrag fehlt: {marker}")

    expected_scope = (
        "Erlaubte Implementierungsdateien: "
        "`data/supabase-participant-auth-session-browser-provider.js`, "
        "`tools/check-participant-auth-session-browser-provider-v2737d.py`, "
        "`docs/PARTICIPANT_AUTH_SESSION_BROWSER_PROVIDER_V2737D.md`, "
        "`tools/preflight.py`"
    )
    if text.count(expected_scope) != 1:
        stop("v27.37d-Implementierungsscope in CURRENT_TASK ungültig")


def find_node() -> str:
    candidates = (
        shutil.which("node"),
        "C:/Program Files/nodejs/node.exe",
        "C:/Program Files (x86)/nodejs/node.exe",
        "/usr/bin/node",
        "/usr/local/bin/node",
        "/opt/homebrew/bin/node",
    )
    for candidate in candidates:
        if candidate and Path(candidate).is_file():
            return str(candidate)
    stop("erforderliche lokale JavaScript-Laufzeit fehlt")
    raise AssertionError("unreachable")


if not PROVIDER_PATH.is_file():
    stop("Provider-Datei fehlt")

require_authorized_task()

changes = changed_paths()
if not changes:
    stop("keine v27.37d-Implementierungsänderung gefunden")

if not changes.issubset(IMPLEMENTATION_FILES):
    stop(
        "Working Tree enthält nicht autorisierte Dateien: "
        + ", ".join(sorted(changes - IMPLEMENTATION_FILES))
    )

for relative_path in FROZEN_FILES:
    current = (ROOT / relative_path).read_bytes()
    if current != baseline_bytes(relative_path):
        stop(f"Frozen-Datei wurde verändert: {relative_path}")

source = PROVIDER_PATH.read_text(encoding="utf-8")

required_source = (
    "ACCAOUI_SUPABASE_BOOTSTRAP",
    "ACCAOUI_PARTICIPANT_AUTH_SESSION_ADAPTER_FACTORY",
    "ACCAOUI_PARTICIPANT_AUTH_SESSION_BOOTSTRAP_BRIDGE_FACTORY",
    "ACCAOUI_PARTICIPANT_AUTH_SESSION_APP_PROVIDER",
    "resolveSession",
    "signIn",
    "signOut",
    'code: "auth_error"',
    "Object.freeze",
    "Object.defineProperty",
)

for marker in required_source:
    if marker not in source:
        stop(f"Provider-Vertragsmarker fehlt: {marker}")

for token in (
    "initializeClient(",
    "createClient(",
    "getState(",
    "getClient(",
    ".from(",
    "fetch(",
    "XMLHttpRequest",
    "WebSocket",
    "EventSource",
    "sendBeacon",
    "localStorage",
    "sessionStorage",
    "indexedDB",
    "document.",
    "process.env",
    "auth.getSession",
    "auth.signIn",
    "auth.signOut",
):
    if token in source:
        stop(f"Provider verletzt Kompositionsgrenze: {token}")

HARNESS = r'''
"use strict";

const fs = require("fs");
const vm = require("vm");

const source = fs.readFileSync(process.argv[1], "utf8");
const PROVIDER =
  "ACCAOUI_PARTICIPANT_AUTH_SESSION_APP_PROVIDER";

let positive = 0;
let negative = 0;

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

function same(actual, expected, message) {
  assert(
    JSON.stringify(actual) === JSON.stringify(expected),
    message
  );
}

function execute(win) {
  const context = vm.createContext({ window: win });
  vm.runInContext(source, context, {
    filename: "provider-v2737d.js",
    timeout: 2000
  });
  return context;
}

function validateAuthError(value) {
  assert(value && typeof value === "object", "auth_error Objekt");
  assert(Object.isFrozen(value), "auth_error nicht frozen");
  same(
    Reflect.ownKeys(value).sort(),
    ["code", "ok"],
    "auth_error Keys"
  );
  assert(value.ok === false, "auth_error ok");
  assert(value.code === "auth_error", "auth_error code");
}

async function testPositive(name, body) {
  await body();
  positive += 1;
}

async function testNegative(name, body) {
  await body();
  negative += 1;
}

async function main() {
  await testPositive("P01 passiver Modul-Load", async () => {
    let reads = 0;
    const win = {};

    for (const key of [
      "ACCAOUI_SUPABASE_BOOTSTRAP",
      "ACCAOUI_PARTICIPANT_AUTH_SESSION_ADAPTER_FACTORY",
      "ACCAOUI_PARTICIPANT_AUTH_SESSION_BOOTSTRAP_BRIDGE_FACTORY"
    ]) {
      Object.defineProperty(win, key, {
        configurable: true,
        get() {
          reads += 1;
          throw new Error("unerlaubter Ladezugriff");
        }
      });
    }

    execute(win);
    assert(reads === 0, "Dependencies beim Laden gelesen");
    assert(win[PROVIDER], "Provider nicht installiert");
  });

  await testPositive("P02 Provider-Oberfläche", async () => {
    const win = {};
    execute(win);

    const provider = win[PROVIDER];
    assert(Object.isFrozen(provider), "Provider nicht frozen");
    same(
      Object.keys(provider).sort(),
      ["resolveSession", "signIn", "signOut"],
      "Provider-Oberfläche"
    );

    const descriptor =
      Object.getOwnPropertyDescriptor(win, PROVIDER);

    assert(descriptor, "Provider-Descriptor fehlt");
    assert(descriptor.enumerable === true, "nicht enumerable");
    assert(descriptor.configurable === false, "configurable");
    assert(descriptor.writable === false, "writable");
  });

  await testPositive("P03 lazy und unveränderte Ergebnisse", async () => {
    const win = {};
    const context = execute(win);
    const state = {
      factoryCalls: 0,
      dependencies: [],
      credentials: null
    };

    const bootstrap = Object.freeze({ synthetic: true });
    const adapterFactory = function adapterFactory() {};

    const results = {
      resolveSession: vm.runInContext(
        'Object.freeze({ok:true,code:"session_available"})',
        context
      ),
      signIn: vm.runInContext(
        'Object.freeze({ok:true,code:"signed_in"})',
        context
      ),
      signOut: vm.runInContext(
        'Object.freeze({ok:true,code:"signed_out"})',
        context
      )
    };

    win.ACCAOUI_SUPABASE_BOOTSTRAP = bootstrap;
    win.ACCAOUI_PARTICIPANT_AUTH_SESSION_ADAPTER_FACTORY =
      adapterFactory;

    win.ACCAOUI_PARTICIPANT_AUTH_SESSION_BOOTSTRAP_BRIDGE_FACTORY =
      function bridgeFactory(dependencies) {
        state.factoryCalls += 1;
        state.dependencies.push(dependencies);

        return {
          async resolveSession() {
            return results.resolveSession;
          },
          async signIn(credentials) {
            state.credentials = credentials;
            return results.signIn;
          },
          async signOut() {
            return results.signOut;
          }
        };
      };

    assert(state.factoryCalls === 0, "nicht lazy");

    const credentials = Object.freeze({
      email: "synthetic@example.invalid",
      password: "synthetic-password"
    });

    const provider = win[PROVIDER];

    assert(
      await provider.resolveSession() === results.resolveSession,
      "resolveSession Ergebnis verändert"
    );
    assert(
      await provider.signIn(credentials) === results.signIn,
      "signIn Ergebnis verändert"
    );
    assert(
      await provider.signOut() === results.signOut,
      "signOut Ergebnis verändert"
    );

    assert(state.factoryCalls === 3, "Bridge-Factory Aufrufzahl");
    assert(state.credentials === credentials, "Credentials verändert");

    for (const dependencies of state.dependencies) {
      assert(Object.isFrozen(dependencies), "Dependencies nicht frozen");
      same(
        Reflect.ownKeys(dependencies).sort(),
        ["bootstrap", "createParticipantAuthSessionAdapter"],
        "Dependency-Oberfläche"
      );
      assert(
        dependencies.bootstrap === bootstrap,
        "Bootstrap-Identität verändert"
      );
      assert(
        dependencies.createParticipantAuthSessionAdapter ===
          adapterFactory,
        "Adapter-Factory-Identität verändert"
      );
    }
  });

  await testPositive("P04 bestehende undefined-Grenze", async () => {
    const win = {};
    Object.defineProperty(win, PROVIDER, {
      value: undefined,
      enumerable: false,
      configurable: true,
      writable: true
    });

    execute(win);

    const descriptor =
      Object.getOwnPropertyDescriptor(win, PROVIDER);

    assert(descriptor.value === undefined, "undefined überschrieben");
    assert(descriptor.configurable === true, "Descriptor verändert");
    assert(descriptor.writable === true, "Descriptor verändert");
  });

  await testPositive("P05 geerbte Grenze bleibt erhalten", async () => {
    const proto = {};
    Object.defineProperty(proto, PROVIDER, {
      value: undefined,
      configurable: true
    });

    const win = Object.create(proto);
    execute(win);

    assert(
      !Object.prototype.hasOwnProperty.call(win, PROVIDER),
      "geerbte Grenze überschrieben"
    );
  });

  await testNegative("N01 fehlende Dependencies", async () => {
    const win = {};
    execute(win);
    validateAuthError(await win[PROVIDER].resolveSession());
  });

  await testNegative("N02 ungültige Dependencies", async () => {
    const win = {};
    execute(win);

    win.ACCAOUI_SUPABASE_BOOTSTRAP = [];
    win.ACCAOUI_PARTICIPANT_AUTH_SESSION_ADAPTER_FACTORY = {};
    win.ACCAOUI_PARTICIPANT_AUTH_SESSION_BOOTSTRAP_BRIDGE_FACTORY =
      "invalid";

    validateAuthError(await win[PROVIDER].signOut());
  });

  await testNegative("N03 Bridge-Factory wirft", async () => {
    const win = {};
    execute(win);

    win.ACCAOUI_SUPABASE_BOOTSTRAP = {};
    win.ACCAOUI_PARTICIPANT_AUTH_SESSION_ADAPTER_FACTORY =
      function adapterFactory() {};
    win.ACCAOUI_PARTICIPANT_AUTH_SESSION_BOOTSTRAP_BRIDGE_FACTORY =
      function bridgeFactory() {
        throw new Error("synthetic private error");
      };

    validateAuthError(await win[PROVIDER].resolveSession());
  });

  await testNegative("N04 Bridge ungültig", async () => {
    const win = {};
    execute(win);

    win.ACCAOUI_SUPABASE_BOOTSTRAP = {};
    win.ACCAOUI_PARTICIPANT_AUTH_SESSION_ADAPTER_FACTORY =
      function adapterFactory() {};
    win.ACCAOUI_PARTICIPANT_AUTH_SESSION_BOOTSTRAP_BRIDGE_FACTORY =
      function bridgeFactory() {
        return null;
      };

    validateAuthError(await win[PROVIDER].resolveSession());
  });

  await testNegative("N05 Bridge-Methode wirft", async () => {
    const win = {};
    execute(win);

    win.ACCAOUI_SUPABASE_BOOTSTRAP = {};
    win.ACCAOUI_PARTICIPANT_AUTH_SESSION_ADAPTER_FACTORY =
      function adapterFactory() {};
    win.ACCAOUI_PARTICIPANT_AUTH_SESSION_BOOTSTRAP_BRIDGE_FACTORY =
      function bridgeFactory() {
        return {
          async resolveSession() {
            throw new Error("synthetic private error");
          }
        };
      };

    validateAuthError(await win[PROVIDER].resolveSession());
  });

  await testNegative("N06 manipuliertes Ergebnis", async () => {
    const win = {};
    const context = execute(win);

    const malformed = vm.runInContext(
      'Object.freeze({ok:true,code:"session_available",extra:true})',
      context
    );

    win.ACCAOUI_SUPABASE_BOOTSTRAP = {};
    win.ACCAOUI_PARTICIPANT_AUTH_SESSION_ADAPTER_FACTORY =
      function adapterFactory() {};
    win.ACCAOUI_PARTICIPANT_AUTH_SESSION_BOOTSTRAP_BRIDGE_FACTORY =
      function bridgeFactory() {
        return {
          async resolveSession() {
            return malformed;
          }
        };
      };

    validateAuthError(await win[PROVIDER].resolveSession());
  });

  await testNegative("N07 falsches Ergebnispaar", async () => {
    const win = {};
    const context = execute(win);

    const malformed = vm.runInContext(
      'Object.freeze({ok:true,code:"signed_in"})',
      context
    );

    win.ACCAOUI_SUPABASE_BOOTSTRAP = {};
    win.ACCAOUI_PARTICIPANT_AUTH_SESSION_ADAPTER_FACTORY =
      function adapterFactory() {};
    win.ACCAOUI_PARTICIPANT_AUTH_SESSION_BOOTSTRAP_BRIDGE_FACTORY =
      function bridgeFactory() {
        return {
          async resolveSession() {
            return malformed;
          }
        };
      };

    validateAuthError(await win[PROVIDER].resolveSession());
  });

  await testNegative("N08 nicht erweiterbares Window", async () => {
    const win = Object.preventExtensions({});
    execute(win);

    assert(
      !Object.prototype.hasOwnProperty.call(win, PROVIDER),
      "Provider trotz gesperrter Grenze installiert"
    );
  });

  console.log(
    `v27.37d Browser-Provider: ${positive} Positivtests / PASS; ` +
    `${negative} Negativtests / vollständig blockiert`
  );
}

main().catch((error) => {
  console.error(error && error.message ? error.message : error);
  process.exit(1);
});
'''

node = find_node()

result = subprocess.run(
    [node, "-e", HARNESS, str(PROVIDER_PATH)],
    cwd=ROOT,
    capture_output=True,
    text=True,
    encoding="utf-8",
    errors="replace",
    check=False,
    timeout=30,
)

if result.stdout:
    print(result.stdout.strip())

if result.returncode != 0:
    if result.stderr:
        print(result.stderr.strip())
    stop("synthetische v27.37d-Browser-Provider-Prüfung fehlgeschlagen")

print("OK: v27.37d Browser-Provider-Checker bestanden.")
