#!/usr/bin/env python3
"""Prüft den v27.36d-App-Einstieg mit lokalen synthetischen Providern."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP_PATH = ROOT / "app.js"
DOC_PATH = ROOT / "docs/PARTICIPANT_ACCESS_APP_ENTRY_V2736D.md"
PREFLIGHT_PATH = ROOT / "tools/preflight.py"
AUTHORIZATION_HEAD = "9321db1651c3daf1f211a22784c1543db9a7530a"

UNCHANGED_FILES = {
    "data/supabase-client-bootstrap.js": "b1e81a6f37e11777b1af52a240e5ee5aa557d6a784d4c1c40f6c289be2f94ac8",
    "data/supabase-client-adapter.js": "91b07dcba4d39362eed8f335cb15e7ab2b1743520a5b0a49286b02a24dff2148",
    "data/supabase-participant-access-adapter.js": "337f66f2b06143451916ee967ca72af5a6cdfe41ac4d4d8301bd5f88655826e4",
    "data/supabase-participant-access-bootstrap-bridge.js": "da890515c7b8b165b397333826078ca02fe4552559e2873d1d5329238082138b",
}


def stop(message: str, code: int = 1) -> None:
    print(f"STOPP: {message}")
    raise SystemExit(code)


def run_git(arguments: list[str]) -> str:
    result = subprocess.run(
        ["git", *arguments],
        cwd=ROOT,
        text=True,
        capture_output=True,
        encoding="utf-8",
        errors="strict",
    )
    if result.returncode != 0:
        stop(f"Lokale Git-Prüfung fehlgeschlagen: {' '.join(arguments)}")
    return result.stdout


for required_path in (APP_PATH, DOC_PATH, PREFLIGHT_PATH):
    if not required_path.is_file():
        stop(f"Pflichtdatei fehlt: {required_path.relative_to(ROOT)}")

app_text = APP_PATH.read_text(encoding="utf-8")
doc_text = DOC_PATH.read_text(encoding="utf-8")
preflight_text = PREFLIGHT_PATH.read_text(encoding="utf-8")

required_app_markers = (
    "window.ACCAOUI_PARTICIPANT_ACCESS_APP_PROVIDER",
    "resolveParticipantAccessAppProviderV2736D",
    "resolveAccess",
    'resultAllowed === true && resultCode === "access_allowed"',
    "startLocalApp()",
    "login_required",
    "blocked",
    "expired",
    "no_course",
    "access_error",
)
for marker in required_app_markers:
    if marker not in app_text:
        stop(f"App-Vertragsmarker fehlt: {marker}")

app_diff = run_git(["diff", "--unified=0", AUTHORIZATION_HEAD, "--", "app.js"])
added_app_lines = "\n".join(
    line[1:]
    for line in app_diff.splitlines()
    if line.startswith("+") and not line.startswith("+++")
)

forbidden_added_tokens = (
    "client.auth.getSession" + "(",
    "client.from" + "(",
    ".from" + "(",
    "bootstrap.initializeClient" + "(",
    "supabase.createClient" + "(",
    "createClient" + "(",
    "initializeClient" + "(",
    "getClient" + "(",
    "getState" + "(",
    "getConfig" + "(",
    "fet" + "ch(",
    "XML" + "HttpRequest",
    "Web" + "Socket",
    "auth_user_id",
    "access_starts_at",
    "access_ends_at",
    "user" + "Id",
    "supabase-participant-access-adapter",
    "supabase-participant-access-bootstrap-bridge",
    "supabase-client-bootstrap",
)
added_folded = added_app_lines.casefold()
for token in forbidden_added_tokens:
    if token.casefold() in added_folded:
        stop(f"Neue App-Integration verletzt die lokale Sicherheitsgrenze: {token}")

for relative_path, expected_hash in UNCHANGED_FILES.items():
    path = ROOT / relative_path
    if not path.is_file():
        stop(f"Unveränderte Bestandsdatei fehlt: {relative_path}")
    actual_hash = hashlib.sha256(path.read_bytes()).hexdigest()
    if actual_hash != expected_hash:
        stop(f"v27.36b/v27.36c-Bestandsdatei wurde verändert: {relative_path}")

required_doc_markers = (
    "Ziel",
    "Sicherheitsgrenze",
    "optionaler Provider",
    "resolveAccess()",
    "fail-closed",
    "lokaler synthetischer Provider",
    "getestete Fälle",
    "unveränderte Bestandsmodule",
    "Supabase live: NEIN",
    "echte Keys: NEIN",
    "echte Teilnehmerdaten: NEIN",
    "keine Browser-Verbindung zu v27.36b/v27.36c",
)
for marker in required_doc_markers:
    if marker not in doc_text:
        stop(f"v27.36d-Dokumentationsmarker fehlt: {marker}")

if "check-participant-access-app-entry-v2736d.py" not in preflight_text:
    stop("v27.36d-Checker ist nicht dauerhaft im Preflight eingebunden")

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

const appPath = process.argv[1];
const originalSource = fs.readFileSync(appPath, "utf8");

function assert(condition, message) {
  if (!condition) {
    throw new Error(message);
  }
}

function own(object, key) {
  return Object.prototype.hasOwnProperty.call(object, key);
}

function replaceOnce(source, needle, replacement, label) {
  const first = source.indexOf(needle);
  assert(first >= 0, `Mutation nicht anwendbar: ${label}`);
  assert(source.indexOf(needle, first + needle.length) < 0, `Mutation nicht eindeutig: ${label}`);
  return source.slice(0, first) + replacement + source.slice(first + needle.length);
}

async function runCase(source, options = {}) {
  const state = {
    startCalls: 0,
    renderCalls: 0,
    resolveCalls: 0,
    providerReads: 0,
    notices: []
  };
  const windowObject = {};

  if (options.providerGetterThrows) {
    Object.defineProperty(windowObject, "ACCAOUI_PARTICIPANT_ACCESS_APP_PROVIDER", {
      configurable: true,
      get() {
        state.providerReads += 1;
        throw new Error("synthetic provider getter failure");
      }
    });
  } else if (own(options, "provider")) {
    windowObject.ACCAOUI_PARTICIPANT_ACCESS_APP_PROVIDER = options.provider;
  } else if (options.providerKind !== "absent") {
    let provider;
    if (options.providerKind === "null") {
      provider = null;
    } else if (options.providerKind === "primitive") {
      provider = "invalid-provider";
    } else if (options.providerKind === "missing_resolve") {
      provider = {};
    } else if (options.providerKind === "resolve_getter_throws") {
      provider = {};
      Object.defineProperty(provider, "resolveAccess", {
        get() {
          throw new Error("synthetic resolve getter failure");
        }
      });
    } else {
      provider = {
        resolveAccess() {
          state.resolveCalls += 1;
          if (options.providerKind === "throws") {
            throw new Error("synthetic provider failure");
          }
          if (options.providerKind === "rejects") {
            return Promise.reject(new Error("synthetic provider rejection"));
          }
          return options.result;
        }
      };
    }
    Object.defineProperty(windowObject, "ACCAOUI_PARTICIPANT_ACCESS_APP_PROVIDER", {
      configurable: true,
      get() {
        state.providerReads += 1;
        return provider;
      }
    });
  }

  const context = {
    window: windowObject,
    document: { addEventListener() {} },
    localStorage: {
      getItem(key) {
        return key === "accaoui_auth_guard_test_state"
          ? (options.localGuardState || "")
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
  };
  vm.createContext(context);
  vm.runInContext(
    source + `
      ;globalThis.__v2736dTestApi = {
        run: initAuthFlow,
        setHooks(startHook, renderHook, healthHook) {
          startLocalApp = startHook;
          renderLoginOrAccessNotice = renderHook;
          getSupabaseAdapterHealthState = healthHook;
        }
      };
    `,
    context,
    { filename: "app.js" }
  );
  context.__v2736dTestApi.setHooks(
    () => { state.startCalls += 1; },
    (notice) => {
      state.renderCalls += 1;
      state.notices.push(notice);
    },
    () => ({
      status: "local_adapter_ready",
      isSupabaseLive: false,
      isLocalAccessAllowed: true,
      reason: "synthetic-local-test"
    })
  );
  await context.__v2736dTestApi.run();
  return state;
}

function assertStartedOnce(state, label) {
  assert(state.startCalls === 1, `${label}: startLocalApp ${state.startCalls} statt 1`);
  assert(state.renderCalls === 0, `${label}: unerwarteter Auth-Hinweis`);
}

function assertBlocked(state, expectedStatus, label) {
  assert(state.startCalls === 0, `${label}: unzulässiger lokaler Fallback`);
  assert(state.renderCalls === 1, `${label}: Auth-Hinweis nicht exakt einmal`);
  assert(state.notices[0].status === expectedStatus, `${label}: Status ${state.notices[0].status} statt ${expectedStatus}`);
}

async function verifyNoProvider(source) {
  const state = await runCase(source, { providerKind: "absent" });
  assertStartedOnce(state, "kein Provider");
  assert(state.resolveCalls === 0, "kein Provider: resolveAccess wurde aufgerufen");
}

async function verifyAllowed(source) {
  const state = await runCase(source, {
    providerKind: "result",
    result: { allowed: true, code: "access_allowed" }
  });
  assertStartedOnce(state, "access_allowed");
  assert(state.resolveCalls === 1, `access_allowed: resolveAccess ${state.resolveCalls} statt 1`);
}

async function verifyBlockedResult(source, result, expectedStatus, label) {
  const state = await runCase(source, { providerKind: "result", result });
  assertBlocked(state, expectedStatus, label);
  assert(state.resolveCalls === 1, `${label}: resolveAccess ${state.resolveCalls} statt 1`);
}

async function verifyLocalGuardPriority(source, localGuardState) {
  const state = await runCase(source, {
    providerKind: "result",
    result: { allowed: true, code: "access_allowed" },
    localGuardState
  });
  assertBlocked(state, localGuardState, `Auth-Guard ${localGuardState}`);
  assert(state.providerReads === 0, `Auth-Guard ${localGuardState}: Provider wurde gelesen`);
  assert(state.resolveCalls === 0, `Auth-Guard ${localGuardState}: resolveAccess wurde aufgerufen`);
}

async function main() {
  let positive = 0;
  let negative = 0;
  let manipulations = 0;

  await verifyNoProvider(originalSource);
  positive += 1;
  await verifyAllowed(originalSource);
  positive += 1;

  const mappings = {
    login_required: [
      "session_missing", "session_invalid", "session_user_missing",
      "session_user_id_invalid"
    ],
    blocked: ["participant_blocked", "enrollment_blocked"],
    expired: [
      "participant_expired", "enrollment_expired",
      "enrollment_access_ended", "course_ended"
    ],
    no_course: [
      "participant_completed", "enrollment_missing", "enrollment_completed",
      "enrollment_access_not_started", "course_missing", "course_inactive",
      "course_archived", "course_not_started"
    ]
  };
  const accessContractFailures = [
    ["unbekannter Code", { allowed: false, code: "unknown_internal_code" }],
    ["allowed true mit falschem Code", { allowed: true, code: "session_missing" }],
    ["allowed false mit access_allowed", { allowed: false, code: "access_allowed" }]
  ];
  const invalidResults = [
    ["null Ergebnis", null],
    ["Array-Ergebnis", []],
    ["fehlendes allowed", { code: "session_missing" }],
    ["fehlender code", { allowed: false }]
  ];
  const invalidProviderCases = [
    ["null Provider", { providerKind: "null" }],
    ["primitiver Provider", { providerKind: "primitive" }],
    ["resolveAccess fehlt", { providerKind: "missing_resolve" }],
    ["resolveAccess wirft", { providerKind: "throws" }],
    ["resolveAccess rejected", { providerKind: "rejects" }],
    ["Provider-Getter wirft", { providerGetterThrows: true }],
    ["resolveAccess-Getter wirft", { providerKind: "resolve_getter_throws" }]
  ];
  const localGuardStates = ["login_required", "blocked", "expired", "no_course"];
  const negativeCaseIds = [
    ...Object.entries(mappings).flatMap(([status, codes]) =>
      codes.map((code) => `mapping:${status}:${code}`)
    ),
    ...accessContractFailures.map(([label]) => `access-contract:${label}`),
    ...invalidResults.map(([label]) => `invalid-result:${label}`),
    ...invalidProviderCases.map(([label]) => `invalid-provider:${label}`),
    ...localGuardStates.map((state) => `local-guard:${state}`)
  ];
  const expectedNegative = negativeCaseIds.length;
  assert(
    new Set(negativeCaseIds).size === expectedNegative,
    "Negativtestdefinition enthält Duplikate"
  );

  for (const [status, codes] of Object.entries(mappings)) {
    for (const code of codes) {
      await verifyBlockedResult(originalSource, { allowed: false, code }, status, code);
      negative += 1;
    }
  }

  for (const [label, result] of accessContractFailures) {
    await verifyBlockedResult(originalSource, result, "access_error", label);
    negative += 1;
  }

  for (const [label, result] of invalidResults) {
    const state = await runCase(originalSource, { providerKind: "result", result });
    assertBlocked(state, "access_error", label);
    assert(state.resolveCalls === 1, `${label}: resolveAccess nicht exakt einmal`);
    negative += 1;
  }

  for (const [label, options] of invalidProviderCases) {
    const state = await runCase(originalSource, options);
    assertBlocked(state, "access_error", label);
    negative += 1;
  }

  for (const localGuardState of localGuardStates) {
    await verifyLocalGuardPriority(originalSource, localGuardState);
    negative += 1;
  }

  const mutationCases = [
    [
      "null als fehlender Provider",
      replaceOnce(originalSource, "if (provider === undefined) {", "if (provider == null) {", "undefined-Grenze"),
      async (source) => {
        const state = await runCase(source, { providerKind: "null" });
        assertBlocked(state, "access_error", "null Provider");
      }
    ],
    [
      "allowed-Vertrag aufgeweicht",
      replaceOnce(originalSource, 'resultAllowed === true && resultCode === "access_allowed"', 'resultAllowed === true || resultCode === "access_allowed"', "access_allowed-Vertrag"),
      async (source) => verifyBlockedResult(source, { allowed: false, code: "access_allowed" }, "access_error", "allowed-Vertrag")
    ],
    [
      "resolveAccess doppelt",
      replaceOnce(originalSource, "result = await providerResolveAccess.call(provider);", "result = await providerResolveAccess.call(provider);\n    result = await providerResolveAccess.call(provider);", "resolveAccess-Aufrufzahl"),
      verifyAllowed
    ],
    [
      "startLocalApp doppelt",
      replaceOnce(originalSource, "if (providerAccessState.isAllowed) {\n    startLocalApp();\n    return;\n  }", "if (providerAccessState.isAllowed) {\n    startLocalApp();\n    startLocalApp();\n    return;\n  }", "Start-Aufrufzahl"),
      verifyAllowed
    ],
    [
      "login_required-Mapping entfernt",
      replaceOnce(originalSource, 'session_missing: "login_required"', 'session_missing: "access_error"', "Login-Mapping"),
      async (source) => verifyBlockedResult(source, { allowed: false, code: "session_missing" }, "login_required", "Login-Mapping")
    ],
    [
      "blocked-Mapping entfernt",
      replaceOnce(originalSource, 'participant_blocked: "blocked"', 'participant_blocked: "access_error"', "Blocked-Mapping"),
      async (source) => verifyBlockedResult(source, { allowed: false, code: "participant_blocked" }, "blocked", "Blocked-Mapping")
    ],
    [
      "expired-Mapping entfernt",
      replaceOnce(originalSource, 'participant_expired: "expired"', 'participant_expired: "access_error"', "Expired-Mapping"),
      async (source) => verifyBlockedResult(source, { allowed: false, code: "participant_expired" }, "expired", "Expired-Mapping")
    ],
    [
      "no_course-Mapping entfernt",
      replaceOnce(originalSource, 'participant_completed: "no_course"', 'participant_completed: "access_error"', "No-course-Mapping"),
      async (source) => verifyBlockedResult(source, { allowed: false, code: "participant_completed" }, "no_course", "No-course-Mapping")
    ],
    [
      "Auth-Guard-Vorrang entfernt",
      replaceOnce(originalSource, "if (!accessState.isAllowed) {", "if (false) {", "Auth-Guard-Vorrang"),
      async (source) => verifyLocalGuardPriority(source, "blocked")
    ],
    [
      "unbekannter Code nicht generisch",
      replaceOnce(originalSource, 'PARTICIPANT_ACCESS_CODE_TO_NOTICE_STATUS_V2736D[resultCode] ||\n    "access_error"', 'PARTICIPANT_ACCESS_CODE_TO_NOTICE_STATUS_V2736D[resultCode] ||\n    "login_required"', "unbekannter Code"),
      async (source) => verifyBlockedResult(source, { allowed: false, code: "unknown_internal_code" }, "access_error", "unbekannter Code")
    ]
  ];

  for (const [label, mutatedSource, verifier] of mutationCases) {
    let blocked = false;
    try {
      await verifier(mutatedSource);
    } catch (error) {
      if (error && error.name === "SyntaxError") {
        throw error;
      }
      blocked = true;
    }
    assert(blocked, `Manipulation wurde nicht blockiert: ${label}`);
    manipulations += 1;
  }

  process.stdout.write(JSON.stringify({
    positive,
    negative,
    expectedNegative,
    manipulations
  }));
}

main().catch((error) => {
  process.stderr.write(String(error && error.stack ? error.stack : error));
  process.exit(1);
});
'''

result = subprocess.run(
    [str(node_path), "-e", HARNESS, str(APP_PATH)],
    cwd=ROOT,
    text=True,
    capture_output=True,
    encoding="utf-8",
    errors="strict",
)
if result.returncode != 0:
    if result.stderr:
        print(result.stderr)
    stop("lokale synthetische Provider-Prüfung fehlgeschlagen")

try:
    summary = json.loads(result.stdout)
except (TypeError, ValueError) as error:
    stop(f"ungültige Testzusammenfassung: {error}")

positive = summary.get("positive")
negative = summary.get("negative")
expected_negative = summary.get("expectedNegative")
manipulations = summary.get("manipulations")
if (
    positive != 2
    or not isinstance(expected_negative, int)
    or isinstance(expected_negative, bool)
    or negative != expected_negative
    or manipulations != 10
):
    stop(
        "unerwartete Prüfungszahlen: "
        f"Positiv={positive}, Negativ={negative}, "
        f"Erwartet-Negativ={expected_negative}, Manipulation={manipulations}"
    )

print("Teilnehmerzugangs-App-Einstieg v27.36d: PASS")
print(f"Positivprüfungen: {positive} PASS")
print(f"Negativprüfungen: {negative} PASS")
print(f"Manipulationsprüfungen: {manipulations} PASS")
print("Provider: lokaler synthetischer Provider")
print("resolveAccess: exakt einmal je Provider-Entscheidung")
print("access_allowed: startLocalApp exakt einmal")
print("Mapping: login_required, blocked, expired und no_course vollständig")
print("Fail-closed und Auth-Guard-Vorrang: PASS")
print("Direkte Supabase-/DB-Fachlogik: NEIN")
print("v27.36b/v27.36c-Bestandsmodule: unverändert")
print("Supabase live: NEIN")
