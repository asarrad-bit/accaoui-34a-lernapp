#!/usr/bin/env python3
"""Prüft v27.37a vollständig lokal mit synthetischem In-Memory Fake Auth."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ADAPTER_PATH = ROOT / "data/supabase-participant-auth-session-adapter.js"
ACCESS_ADAPTER_PATH = ROOT / "data/supabase-participant-access-adapter.js"
REPORT_PATH = ROOT / "docs/SUPABASE_PARTICIPANT_AUTH_SESSION_ADAPTER_V2737A.md"


def stop(message: str) -> None:
    print(f"STOPP: {message}")
    raise SystemExit(1)


def find_node() -> Path:
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
            return Path(candidate)
    stop("erforderliche lokale JavaScript-Laufzeit fehlt")
    raise AssertionError("unreachable")


def get_checker_temp_root() -> Path:
    git_marker = ROOT / ".git"
    if git_marker.is_dir():
        git_dir = git_marker
    else:
        completed = subprocess.run(
            ["git", "rev-parse", "--git-dir"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )
        git_dir_text = completed.stdout.strip()
        if completed.returncode != 0 or not git_dir_text:
            details = "\n".join(
                part.strip()
                for part in (completed.stdout, completed.stderr)
                if part.strip()
            )
            stop(f"lokales Git-Verzeichnis nicht ermittelbar: {details}")
        git_dir = Path(git_dir_text)
        if not git_dir.is_absolute():
            git_dir = (ROOT / git_dir).resolve()

    if not git_dir.is_dir():
        stop(f"lokales Git-Verzeichnis fehlt: {git_dir}")

    checker_temp_root = git_dir / "accaoui-checker-temp" / "v2737a-auth"
    try:
        checker_temp_root.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(
            prefix="write-check-", dir=checker_temp_root
        ) as temp_dir:
            probe_path = Path(temp_dir) / "probe.txt"
            probe_path.write_text("ok\n", encoding="utf-8", newline="\n")
    except OSError as exc:
        stop(f"lokaler Git-Temp-Root nicht beschreibbar: {exc}")
    return checker_temp_root


def source_contract_errors(source: str) -> list[str]:
    errors: list[str] = []
    required_exact = (
        "function createParticipantAuthSessionAdapter(dependencies)",
        "return Object.freeze({ ok, code });",
        "return Object.freeze({ resolveSession, signIn, signOut });",
        "module.exports = Object.freeze({ createParticipantAuthSessionAdapter });",
    )
    for marker in required_exact:
        if source.count(marker) != 1:
            errors.append(f"Quellvertrag nicht exakt: {marker}")
    required_calls = (
        "await auth.getSession()",
        "await auth.signInWithPassword({",
        "await auth.signOut()",
    )
    for marker in required_calls:
        if source.count(marker) != 1:
            errors.append(f"Auth-Aufruf nicht exakt einmal vorhanden: {marker}")
    if source.count("module.exports") != 1:
        errors.append("CommonJS-Export ist nicht exakt einmal vorhanden")
    forbidden_tokens = (
        "window",
        "document",
        "localStorage",
        "sessionStorage",
        "indexedDB",
        "caches.",
        "cookie",
        "access_token",
        "refresh_token",
        "createClient",
        "initializeClient",
        "fetch(",
        "XMLHttpRequest",
        "WebSocket",
        "EventSource",
        "sendBeacon",
        ".from(",
        "participants",
        "enrollments",
        "courses",
        "dependencies.userId",
        "error.message",
        "process.env",
    )
    for token in forbidden_tokens:
        if token in source:
            errors.append(f"Verbotene Konstruktion im Adapter: {token}")
    if re.search(r"\b(client|bootstrap|config)\b", source, re.IGNORECASE):
        errors.append("Verbotene Client-, Bootstrap- oder Config-Dependency")
    auth_members = set(re.findall(r"\bauth\.([A-Za-z_$][\w$]*)", source))
    if auth_members != {"getSession", "signInWithPassword", "signOut"}:
        errors.append(f"Unerlaubte Auth-Oberfläche: {sorted(auth_members)}")
    return errors


HARNESS = r'''"use strict";

const authAdapterPath = process.argv[2];
const accessAdapterPath = process.argv[3];
const api = require(authAdapterPath);
const accessApi = require(accessAdapterPath);

const USER_ID = "11111111-1111-4111-8111-111111111111";
const PARTICIPANT_ID = "22222222-2222-4222-8222-222222222222";
const ENROLLMENT_ID = "33333333-3333-4333-8333-333333333333";
const COURSE_ID = "44444444-4444-4444-8444-444444444444";
const PASSWORD = "  synthetic-secret  ";

let positive = 0;
let negative = 0;
const failures = [];

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

function same(actual, expected, message) {
  assert(JSON.stringify(actual) === JSON.stringify(expected),
    `${message}: ${JSON.stringify(actual)} !== ${JSON.stringify(expected)}`);
}

function validSession() {
  return {
    user: { id: USER_ID, email: "synthetic@example.invalid" },
    access_token: "SYNTHETIC_ACCESS_TOKEN",
    refresh_token: "SYNTHETIC_REFRESH_TOKEN"
  };
}

function validateResult(value, expected, label) {
  assert(value !== null && typeof value === "object" && !Array.isArray(value), `${label}: kein Objekt`);
  assert(Object.getPrototypeOf(value) === Object.prototype, `${label}: kein Plain Object`);
  assert(Object.isFrozen(value), `${label}: nicht frozen`);
  same(Object.keys(value).sort(), ["code", "ok"], `${label}: Ergebnisfelder`);
  assert(typeof value.ok === "boolean" && typeof value.code === "string", `${label}: Typen`);
  same(value, expected, label);
  const serialized = JSON.stringify(value);
  for (const secret of [PASSWORD, USER_ID, "synthetic@example.invalid", "SYNTHETIC_ACCESS_TOKEN", "SYNTHETIC_REFRESH_TOKEN", "RAW_SECRET_ERROR"]) {
    assert(!serialized.includes(secret), `${label}: sensitives Datum im Ergebnis`);
  }
}

async function test(kind, name, body) {
  try {
    await body();
    if (kind === "positive") positive += 1;
    else negative += 1;
  } catch (error) {
    failures.push(`${name}: ${error && error.message ? error.message : error}`);
  }
}

function makeAuth(options = {}) {
  let session = Object.prototype.hasOwnProperty.call(options, "session")
    ? options.session
    : validSession();
  const calls = { getSession: 0, signInWithPassword: 0, signOut: 0 };
  const auth = {
    calls,
    async getSession() {
      calls.getSession += 1;
      if (options.getSessionThrow) throw new Error("RAW_SECRET_ERROR");
      if (Object.prototype.hasOwnProperty.call(options, "getSessionResponse")) {
        return options.getSessionResponse;
      }
      return { data: { session }, error: null };
    },
    async signInWithPassword(credentials) {
      calls.signInWithPassword += 1;
      auth.lastCredentials = credentials;
      if (options.signInThrow) throw new Error("RAW_SECRET_ERROR");
      if (Object.prototype.hasOwnProperty.call(options, "signInResponse")) {
        return options.signInResponse;
      }
      session = validSession();
      return { data: { session }, error: null };
    },
    async signOut() {
      calls.signOut += 1;
      if (options.signOutThrow) throw new Error("RAW_SECRET_ERROR");
      if (Object.prototype.hasOwnProperty.call(options, "signOutResponse")) {
        return options.signOutResponse;
      }
      session = null;
      return { error: null };
    }
  };
  return auth;
}

function adapterFor(auth, extra) {
  const dependencies = extra ? { auth, ...extra } : { auth };
  return api.createParticipantAuthSessionAdapter(dependencies);
}

async function expectMethod(auth, method, args, expected, label) {
  const adapter = adapterFor(auth);
  const value = args === undefined ? await adapter[method]() : await adapter[method](args);
  validateResult(value, expected, label);
  return { adapter, value };
}

async function main() {
  await test("positive", "P01 CommonJS-Factory", async () => {
    same(Object.keys(api), ["createParticipantAuthSessionAdapter"], "Module-API");
    assert(Object.isFrozen(api), "Module-API nicht frozen");
    assert(typeof api.createParticipantAuthSessionAdapter === "function", "Factory fehlt");
  });
  await test("positive", "P02 Adapteroberfläche und Side Effects", async () => {
    const auth = makeAuth();
    const adapter = adapterFor(auth);
    same(Object.keys(adapter).sort(), ["resolveSession", "signIn", "signOut"], "Adapter-API");
    assert(Object.isFrozen(adapter), "Adapter nicht frozen");
    same(auth.calls, { getSession: 0, signInWithPassword: 0, signOut: 0 }, "Factory-Side-Effects");
  });
  await test("positive", "P03 resolveSession Erfolg", async () => {
    const auth = makeAuth();
    await expectMethod(auth, "resolveSession", undefined, { ok: true, code: "session_available" }, "resolveSession");
    assert(auth.calls.getSession === 1, "getSession nicht exakt einmal");
  });
  await test("positive", "P04 signIn Erfolg", async () => {
    const auth = makeAuth({ session: null });
    const input = { email: "  synthetic@example.invalid  ", password: PASSWORD };
    await expectMethod(auth, "signIn", input, { ok: true, code: "signed_in" }, "signIn");
    assert(auth.calls.signInWithPassword === 1, "signInWithPassword nicht exakt einmal");
    same(auth.lastCredentials, { email: "synthetic@example.invalid", password: PASSWORD }, "Credentials");
    assert(input.password === PASSWORD, "Passwort mutiert");
  });
  await test("positive", "P05 signOut Erfolg", async () => {
    const auth = makeAuth();
    await expectMethod(auth, "signOut", undefined, { ok: true, code: "signed_out" }, "signOut");
    assert(auth.calls.signOut === 1, "signOut nicht exakt einmal");
  });
  await test("positive", "P06 unabhängige Instanzen", async () => {
    const first = adapterFor(makeAuth());
    const second = adapterFor(makeAuth({ session: null }));
    validateResult(await first.resolveSession(), { ok: true, code: "session_available" }, "Instanz 1");
    validateResult(await second.resolveSession(), { ok: false, code: "session_missing" }, "Instanz 2");
  });
  await test("positive", "P07 Shared Fake Integration", async () => {
    const auth = makeAuth({ session: null });
    const tables = {
      participants: [{ id: PARTICIPANT_ID, auth_user_id: USER_ID, status: "active" }],
      enrollments: [{
        id: ENROLLMENT_ID,
        participant_id: PARTICIPANT_ID,
        course_id: COURSE_ID,
        access_starts_at: "2026-08-01T00:00:00.000Z",
        access_ends_at: "2026-10-31T23:59:59.999Z",
        access_status: "allowed"
      }],
      courses: [{ id: COURSE_ID, start_date: "2026-08-01", end_date: "2026-10-31", status: "active" }]
    };
    const client = {
      auth,
      from(table) {
        return {
          select() {
            return {
              async eq(column, value) {
                return { data: tables[table].filter((row) => row[column] === value), error: null };
              }
            };
          }
        };
      }
    };
    const authAdapter = adapterFor(auth);
    const accessAdapter = accessApi.createParticipantAccessAdapter({
      client,
      utcNow: () => "2026-09-02T12:00:00.000Z"
    });
    const before = await accessAdapter.resolveAccess();
    assert(before.allowed === false && before.code === "session_missing", "Vor Login nicht session_missing");
    validateResult(await authAdapter.signIn({ email: "synthetic@example.invalid", password: PASSWORD }), { ok: true, code: "signed_in" }, "Shared signIn");
    const allowed = await accessAdapter.resolveAccess();
    assert(allowed.allowed === true && allowed.code === "access_allowed", "Nach Login nicht access_allowed");
    validateResult(await authAdapter.signOut(), { ok: true, code: "signed_out" }, "Shared signOut");
    const after = await accessAdapter.resolveAccess();
    assert(after.allowed === false && after.code === "session_missing", "Nach Logout nicht session_missing");
  });

  const resolveCases = [
    ["session null", { session: null }, { ok: false, code: "session_missing" }],
    ["session undefined", { session: undefined }, { ok: false, code: "session_missing" }],
    ["Response null", { getSessionResponse: null }, { ok: false, code: "session_invalid" }],
    ["Response Array", { getSessionResponse: [] }, { ok: false, code: "session_invalid" }],
    ["error fehlt", { getSessionResponse: { data: { session: validSession() } } }, { ok: false, code: "session_invalid" }],
    ["data fehlt", { getSessionResponse: { error: null } }, { ok: false, code: "session_invalid" }],
    ["data Array", { getSessionResponse: { data: [], error: null } }, { ok: false, code: "session_invalid" }],
    ["session Feld fehlt", { getSessionResponse: { data: {}, error: null } }, { ok: false, code: "session_invalid" }],
    ["session String", { session: "bad" }, { ok: false, code: "session_invalid" }],
    ["user fehlt", { session: {} }, { ok: false, code: "session_invalid" }],
    ["user null", { session: { user: null } }, { ok: false, code: "session_invalid" }],
    ["user Array", { session: { user: [] } }, { ok: false, code: "session_invalid" }],
    ["id fehlt", { session: { user: {} } }, { ok: false, code: "session_invalid" }],
    ["id leer", { session: { user: { id: "" } } }, { ok: false, code: "session_invalid" }],
    ["id falscher Typ", { session: { user: { id: 7 } } }, { ok: false, code: "session_invalid" }],
    ["id Syntax", { session: { user: { id: "not-a-uuid" } } }, { ok: false, code: "session_invalid" }],
    ["Response Error", { getSessionResponse: { data: null, error: { message: "RAW_SECRET_ERROR" } } }, { ok: false, code: "auth_error" }],
    ["getSession Throw", { getSessionThrow: true }, { ok: false, code: "auth_error" }]
  ];
  for (const [name, options, expected] of resolveCases) {
    await test("negative", `R ${name}`, async () => {
      await expectMethod(makeAuth(options), "resolveSession", undefined, expected, name);
    });
  }
  await test("negative", "R getSession Reject", async () => {
    const auth = makeAuth();
    auth.getSession = () => Promise.reject(new Error("RAW_SECRET_ERROR"));
    await expectMethod(auth, "resolveSession", undefined, { ok: false, code: "auth_error" }, "Reject");
  });
  for (const [name, replacement] of [["fehlt", undefined], ["keine Funktion", 7]]) {
    await test("negative", `R Methode ${name}`, async () => {
      const auth = makeAuth();
      if (replacement === undefined) delete auth.getSession;
      else auth.getSession = replacement;
      await expectMethod(auth, "resolveSession", undefined, { ok: false, code: "auth_error" }, name);
    });
  }

  const invalidCredentials = [
    ["Argument fehlt", undefined], ["null", null], ["Array", []],
    ["email fehlt", { password: PASSWORD }], ["email Zahl", { email: 7, password: PASSWORD }],
    ["email leer", { email: "", password: PASSWORD }], ["email Whitespace", { email: "   ", password: PASSWORD }],
    ["password fehlt", { email: "a@example.invalid" }], ["password Zahl", { email: "a@example.invalid", password: 7 }],
    ["password leer", { email: "a@example.invalid", password: "" }]
  ];
  for (const [name, credentials] of invalidCredentials) {
    await test("negative", `S ${name}`, async () => {
      const auth = makeAuth({ session: null });
      await expectMethod(auth, "signIn", credentials, { ok: false, code: "credentials_invalid" }, name);
      assert(auth.calls.signInWithPassword === 0, `${name}: Auth trotz ungültiger Eingabe aufgerufen`);
    });
  }
  const signInCases = [
    ["Response Error", { signInResponse: { data: null, error: { message: "RAW_SECRET_ERROR" } } }, "sign_in_failed"],
    ["Response null", { signInResponse: null }, "sign_in_failed"],
    ["Response Array", { signInResponse: [] }, "sign_in_failed"],
    ["error fehlt", { signInResponse: { data: { session: validSession() } } }, "sign_in_failed"],
    ["data fehlt", { signInResponse: { error: null } }, "sign_in_failed"],
    ["Session fehlt", { signInResponse: { data: {}, error: null } }, "sign_in_failed"],
    ["Session null", { signInResponse: { data: { session: null }, error: null } }, "sign_in_failed"],
    ["ID ungültig", { signInResponse: { data: { session: { user: { id: "bad" } } }, error: null } }, "sign_in_failed"],
    ["Throw", { signInThrow: true }, "auth_error"]
  ];
  for (const [name, options, code] of signInCases) {
    await test("negative", `S ${name}`, async () => {
      await expectMethod(makeAuth(options), "signIn", { email: "a@example.invalid", password: PASSWORD }, { ok: false, code }, name);
    });
  }
  await test("negative", "S Reject", async () => {
    const auth = makeAuth();
    auth.signInWithPassword = () => Promise.reject(new Error("RAW_SECRET_ERROR"));
    await expectMethod(auth, "signIn", { email: "a@example.invalid", password: PASSWORD }, { ok: false, code: "auth_error" }, "Reject");
  });
  for (const [name, replacement] of [["fehlt", undefined], ["keine Funktion", 7]]) {
    await test("negative", `S Methode ${name}`, async () => {
      const auth = makeAuth();
      if (replacement === undefined) delete auth.signInWithPassword;
      else auth.signInWithPassword = replacement;
      await expectMethod(auth, "signIn", { email: "a@example.invalid", password: PASSWORD }, { ok: false, code: "auth_error" }, name);
    });
  }

  const signOutCases = [
    ["Response Error", { signOutResponse: { error: { message: "RAW_SECRET_ERROR" } } }, "sign_out_failed"],
    ["Response null", { signOutResponse: null }, "sign_out_failed"],
    ["Response Array", { signOutResponse: [] }, "sign_out_failed"],
    ["error fehlt", { signOutResponse: {} }, "sign_out_failed"],
    ["Throw", { signOutThrow: true }, "auth_error"]
  ];
  for (const [name, options, code] of signOutCases) {
    await test("negative", `O ${name}`, async () => {
      await expectMethod(makeAuth(options), "signOut", undefined, { ok: false, code }, name);
    });
  }
  await test("negative", "O Reject", async () => {
    const auth = makeAuth();
    auth.signOut = () => Promise.reject(new Error("RAW_SECRET_ERROR"));
    await expectMethod(auth, "signOut", undefined, { ok: false, code: "auth_error" }, "Reject");
  });
  for (const [name, replacement] of [["fehlt", undefined], ["keine Funktion", 7]]) {
    await test("negative", `O Methode ${name}`, async () => {
      const auth = makeAuth();
      if (replacement === undefined) delete auth.signOut;
      else auth.signOut = replacement;
      await expectMethod(auth, "signOut", undefined, { ok: false, code: "auth_error" }, name);
    });
  }

  const dependencyCases = [
    ["Argument fehlt", undefined], ["null", null], ["Array", []],
    ["auth fehlt", {}], ["auth null", { auth: null }], ["Zusatzfeld", { auth: makeAuth(), client: {} }]
  ];
  for (const [name, dependencies] of dependencyCases) {
    await test("negative", `D ${name}`, async () => {
      const adapter = api.createParticipantAuthSessionAdapter(dependencies);
      validateResult(await adapter.resolveSession(), { ok: false, code: "auth_error" }, `${name} resolve`);
      validateResult(await adapter.signIn({ email: "a@example.invalid", password: PASSWORD }), { ok: false, code: "auth_error" }, `${name} signIn`);
      validateResult(await adapter.signOut(), { ok: false, code: "auth_error" }, `${name} signOut`);
    });
  }

  if (failures.length) {
    for (const failure of failures) console.error(failure);
    process.exitCode = 1;
    return;
  }
  console.log(JSON.stringify({ positive, negative, sharedSignIn: true, sharedSignOut: true }));
}

main().catch((error) => {
  console.error(error && error.stack ? error.stack : error);
  process.exitCode = 1;
});
'''


def run_behavior_tests(
    node_path: Path, checker_temp_root: Path
) -> dict[str, object]:
    with tempfile.TemporaryDirectory(
        prefix="behavior-", dir=checker_temp_root
    ) as temp_dir:
        harness_path = Path(temp_dir) / "harness.js"
        harness_path.write_text(HARNESS, encoding="utf-8", newline="\n")
        completed = subprocess.run(
            [
                str(node_path),
                str(harness_path),
                str(ADAPTER_PATH),
                str(ACCESS_ADAPTER_PATH),
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )
    if completed.returncode != 0:
        details = "\n".join(
            part.strip() for part in (completed.stdout, completed.stderr) if part.strip()
        )
        stop(f"JavaScript-Verhaltensprüfung fehlgeschlagen: {details}")
    try:
        result = json.loads(completed.stdout.strip())
    except (json.JSONDecodeError, TypeError) as exc:
        stop(f"Ungültige JavaScript-Prüfausgabe: {exc}")
    if not (
        isinstance(result, dict)
        and isinstance(result.get("positive"), int)
        and isinstance(result.get("negative"), int)
        and result.get("sharedSignIn") is True
        and result.get("sharedSignOut") is True
    ):
        stop("JavaScript-Prüfsummen oder Shared-Fake-Nachweis ungültig")
    return result


def run_mutation_tests(source: str, checker_temp_root: Path) -> int:
    mutations = (
        ("vierte Methode", "return Object.freeze({ resolveSession, signIn, signOut });", "return Object.freeze({ resolveSession, signIn, signOut, debug() {} });"),
        ("zusätzliche Ergebnisproperty", "return Object.freeze({ ok, code });", "return Object.freeze({ ok, code, detail: null });"),
        ("Object.freeze entfernt", "return Object.freeze({ ok, code });", "return { ok, code };"),
        ("Session-Leak", "return Object.freeze({ ok, code });", "return Object.freeze({ ok, code, session: null });"),
        ("User-Leak", "return Object.freeze({ ok, code });", "return Object.freeze({ ok, code, user: null });"),
        ("Passwort-Leak", "return Object.freeze({ ok, code });", "return Object.freeze({ ok, code, password: null });"),
        ("Error-Message-Leak", "\"use strict\";", "\"use strict\"; void error.message;"),
        ("getSession ersetzt", "await auth.getSession()", "await auth.signOut()"),
        ("signInWithPassword ersetzt", "await auth.signInWithPassword({", "await auth.getSession({"),
        ("signOut ersetzt", "await auth.signOut()", "await auth.getSession()"),
        ("getSession doppelt", "const response = await auth.getSession();", "await auth.getSession(); const response = await auth.getSession();"),
        ("freie userId", "function createParticipantAuthSessionAdapter(dependencies) {", "function createParticipantAuthSessionAdapter(dependencies) { void dependencies.userId;"),
        ("localStorage", "\"use strict\";", "\"use strict\"; void localStorage;"),
        ("sessionStorage", "\"use strict\";", "\"use strict\"; void sessionStorage;"),
        ("fetch", "\"use strict\";", "\"use strict\"; fetch(\"/\");"),
        ("createClient", "\"use strict\";", "\"use strict\"; createClient();"),
        ("initializeClient", "\"use strict\";", "\"use strict\"; initializeClient();"),
        ("Tabellenzugriff", "\"use strict\";", "\"use strict\"; auth.from(\"x\");"),
        ("Participant-Abfrage", "\"use strict\";", "\"use strict\"; void auth.participants;"),
        ("Browser-window", "\"use strict\";", "\"use strict\"; void window;"),
    )
    passed = 0
    with tempfile.TemporaryDirectory(
        prefix="mutation-", dir=checker_temp_root
    ) as temp_dir:
        temp_root = Path(temp_dir)
        for index, (label, needle, replacement) in enumerate(mutations, start=1):
            if source.count(needle) != 1:
                stop(f"Manipulation M{index:02d} hat kein eindeutiges Ziel: {label}")
            mutated = source.replace(needle, replacement, 1)
            if mutated == source:
                stop(f"Manipulation M{index:02d} ist wirkungslos: {label}")
            mutation_path = temp_root / f"mutation-{index:02d}.js"
            mutation_path.write_text(mutated, encoding="utf-8", newline="\n")
            if not source_contract_errors(mutation_path.read_text(encoding="utf-8")):
                stop(f"Manipulation M{index:02d} wurde nicht blockiert: {label}")
            passed += 1
    return passed


def validate_report() -> None:
    if not REPORT_PATH.is_file():
        stop("v27.37a-Umsetzungsbericht fehlt")
    report = REPORT_PATH.read_text(encoding="utf-8")
    markers = (
        "Ziel",
        "Isolation",
        "createParticipantAuthSessionAdapter({ auth })",
        "resolveSession()",
        "signIn({ email, password })",
        "signOut()",
        "session_available",
        "session_missing",
        "session_invalid",
        "signed_in",
        "credentials_invalid",
        "sign_in_failed",
        "signed_out",
        "sign_out_failed",
        "auth_error",
        "Datenminimierung",
        "synthetischer In-Memory Fake Auth",
        "unveränderten v27.36b-Teilnehmerzugangs-Adapter",
        "Sicherheitsgrenzen",
        "kein Browser-Wiring",
        "Supabase NICHT LIVE",
        "keine echten Keys",
        "keine echten Teilnehmerdaten",
        "Keine App- oder index.html-Änderung",
        "kein Folgetask vor Closure",
    )
    missing = [marker for marker in markers if marker not in report]
    if missing:
        stop("Umsetzungsbericht unvollständig: " + ", ".join(missing))
    if re.search(r"\b[0-9a-f]{40}\b", report):
        stop("Umsetzungsbericht darf keine zukünftige Commit-SHA enthalten")


def main() -> None:
    if not ADAPTER_PATH.is_file():
        stop("data/supabase-participant-auth-session-adapter.js fehlt")
    if not ACCESS_ADAPTER_PATH.is_file():
        stop("bestehender v27.36b-Teilnehmerzugangs-Adapter fehlt")
    source = ADAPTER_PATH.read_text(encoding="utf-8")
    errors = source_contract_errors(source)
    if errors:
        stop("; ".join(errors))
    validate_report()
    node_path = find_node()
    checker_temp_root = get_checker_temp_root()
    behavior = run_behavior_tests(node_path, checker_temp_root)
    manipulation_count = run_mutation_tests(source, checker_temp_root)
    print("Teilnehmer-Auth-/Session-Adapter v27.37a: PASS")
    print(f"Positivprüfungen: {behavior['positive']} PASS")
    print(f"Negativprüfungen: {behavior['negative']} PASS")
    print(f"Manipulationsprüfungen: {manipulation_count} PASS")
    print("Shared-Fake signIn -> access_allowed: PASS")
    print("Shared-Fake signOut -> session_missing: PASS")
    print("Ergebnisse exakt {ok,code}, Plain Object und frozen: PASS")
    print("Sicherheits-, Isolations- und Datenminimierungsgrenzen: PASS")
    print("Supabase NICHT LIVE")
    print(f"Lokale JavaScript-Laufzeit: {node_path.name}")


if __name__ == "__main__":
    main()
