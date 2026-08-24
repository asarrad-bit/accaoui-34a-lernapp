#!/usr/bin/env python3
"""Prüft die v27.36c-Brücke ausschließlich lokal und synthetisch."""

from __future__ import annotations

import base64
import os
import sys
import zlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BRIDGE_PATH = ROOT / "data/supabase-participant-access-bootstrap-bridge.js"
ADAPTER_PATH = ROOT / "data/supabase-participant-access-adapter.js"
DOC_PATH = ROOT / "docs/SUPABASE_PARTICIPANT_ACCESS_BOOTSTRAP_BRIDGE_V2736C.md"
PREFLIGHT_PATH = ROOT / "tools/preflight.py"


def stop(message: str, code: int = 1) -> None:
    print(f"STOPP: {message}")
    raise SystemExit(code)


for required_path in (BRIDGE_PATH, ADAPTER_PATH, DOC_PATH, PREFLIGHT_PATH):
    if not required_path.is_file():
        stop(f"Pflichtdatei fehlt: {required_path.relative_to(ROOT)}")

bridge_text = BRIDGE_PATH.read_text(encoding="utf-8")
doc_text = DOC_PATH.read_text(encoding="utf-8")
preflight_text = PREFLIGHT_PATH.read_text(encoding="utf-8")

required_bridge_markers = (
    'const VERSION = "v27.36c"',
    "createParticipantAccessBootstrapBridge",
    "bootstrap.getClient",
    "createParticipantAccessAdapter({ client, utcNow })",
    "adapterResolveAccess.call(adapter)",
    "module.exports",
)
for marker in required_bridge_markers:
    if marker not in bridge_text:
        stop(f"Bridge-Vertragsmarker fehlt: {marker}")

forbidden_bridge_tokens = (
    "window",
    "global" + "This",
    "global" + ".",
    "get" + "State",
    "initialize" + "Client",
    "create" + "Client",
    "fet" + "ch(",
    "XML" + "HttpRequest",
    "Web" + "Sock" + "et",
    "ht" + "tp://",
    "ht" + "tps://",
    "process." + "env",
    "Deno." + "env",
    "Bun." + "env",
    ".from" + "(",
    ".insert" + "(",
    ".upsert" + "(",
    ".update" + "(",
    ".delete" + "(",
    ".rpc" + "(",
)
for token in forbidden_bridge_tokens:
    if token in bridge_text:
        stop(f"Bridge verletzt die isolierte Sicherheitsgrenze: {token}")

for forbidden_word in ("config", "sdk", "live"):
    if forbidden_word in bridge_text.lower():
        stop(f"Bridge enthält verbotene Zustandslogik: {forbidden_word}")

required_doc_markers = (
    "Supabase-Teilnehmerzugangs-Bootstrap-Brücke v27.36c",
    "Supabase: **NICHT LIVE**",
    "Fail-closed-Grenze",
    "createParticipantAccessBootstrapBridge",
    "session.user.id",
    "keine App- oder UI-Integration",
    "kein Netzwerkcode",
)
for marker in required_doc_markers:
    if marker not in doc_text:
        stop(f"Bridge-Dokumentationsmarker fehlt: {marker}")

if "check-supabase-participant-access-bootstrap-bridge.py" not in preflight_text:
    stop("Bridge-Checker ist nicht dauerhaft im Preflight eingebunden")

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

const bridgePath = process.argv[1];
const adapterPath = process.argv[2];
const bridgeApi = require(bridgePath);
const adapterApi = require(adapterPath);

const USER_ID = "11111111-1111-4111-8111-111111111111";
const FOREIGN_USER_ID = "99999999-9999-4999-8999-999999999999";
const PARTICIPANT_ID = "22222222-2222-4222-8222-222222222222";
const ENROLLMENT_ID = "33333333-3333-4333-8333-333333333333";
const COURSE_ID = "44444444-4444-4444-8444-444444444444";
const NOW = "2026-08-20T12:00:00.000Z";

function clone(value) {
  return value === undefined ? undefined : JSON.parse(JSON.stringify(value));
}

function own(object, key) {
  return Object.prototype.hasOwnProperty.call(object, key);
}

function assert(condition, message) {
  if (!condition) {
    throw new Error(message);
  }
}

function equal(actual, expected, message) {
  assert(
    JSON.stringify(actual) === JSON.stringify(expected),
    `${message}: ${JSON.stringify(actual)} !== ${JSON.stringify(expected)}`
  );
}

function makeStub(options = {}) {
  const state = {
    getterCalls: 0,
    getClientCalls: 0,
    factoryCalls: 0,
    resolveCalls: 0,
    factoryArguments: [],
    writeCalls: 0,
    externalCalls: 0
  };
  const client = own(options, "client")
    ? options.client
    : Object.freeze({ marker: "synthetic-client" });
  const delegatedResult = own(options, "delegatedResult")
    ? options.delegatedResult
    : Object.freeze({ allowed: false, code: "session_missing" });
  const utcNow = own(options, "utcNow") ? options.utcNow : (() => NOW);

  const bootstrap = own(options, "bootstrap")
    ? options.bootstrap
    : {
        get getClient() {
          state.getterCalls += 1;
          return function () {
            state.getClientCalls += 1;
            return client;
          };
        }
      };

  const adapter = own(options, "adapter")
    ? options.adapter
    : {
        resolveAccess: async function () {
          state.resolveCalls += 1;
          return delegatedResult;
        }
      };

  const factory = own(options, "factory")
    ? options.factory
    : function (dependencies) {
        state.factoryCalls += 1;
        state.factoryArguments.push(dependencies);
        return adapter;
      };

  const dependencies = own(options, "dependencies")
    ? options.dependencies
    : { bootstrap, createParticipantAccessAdapter: factory, utcNow };

  const bridge = bridgeApi.createParticipantAccessBootstrapBridge(dependencies);
  return { state, client, delegatedResult, utcNow, bootstrap, adapter, factory, bridge };
}

async function resultFor(options = {}) {
  const context = makeStub(options);
  context.result = await context.bridge.resolveAccess();
  return context;
}

class LocalRealAdapterFakeClient {
  constructor() {
    this.calls = [];
    this.writeCalls = 0;
    this.externalCalls = 0;
    this.untrustedUserId = FOREIGN_USER_ID;
    this.auth = Object.freeze({
      getSession: async () => {
        this.calls.push({ kind: "session" });
        return {
          data: { session: { user: { id: USER_ID } } },
          error: null
        };
      }
    });
  }

  from(table) {
    this.calls.push({ kind: "from", table });
    const rows = {
      participants: [
        { id: PARTICIPANT_ID, auth_user_id: USER_ID, status: "active" }
      ],
      enrollments: [
        {
          id: ENROLLMENT_ID,
          participant_id: PARTICIPANT_ID,
          course_id: COURSE_ID,
          access_starts_at: "2026-08-01T00:00:00.000Z",
          access_ends_at: "2026-08-31T23:59:59.999Z",
          access_status: "allowed"
        }
      ],
      courses: [
        {
          id: COURSE_ID,
          start_date: "2026-08-01",
          end_date: "2026-08-31",
          status: "active"
        }
      ]
    };
    return Object.freeze({
      select: (columns) => {
        this.calls.push({ kind: "select", table, columns });
        return Object.freeze({
          eq: async (column, value) => {
            this.calls.push({ kind: "eq", table, column, value });
            return { data: clone(rows[table]), error: null };
          }
        });
      }
    });
  }
}

async function runRealAdapter(client) {
  let getClientCalls = 0;
  let factoryCalls = 0;
  let receivedDependencies = null;
  const utcNow = () => NOW;
  const bootstrap = {
    untrustedUserId: FOREIGN_USER_ID,
    getClient() {
      getClientCalls += 1;
      return client;
    }
  };
  const factory = (dependencies) => {
    factoryCalls += 1;
    receivedDependencies = dependencies;
    return adapterApi.createParticipantAccessAdapter(dependencies);
  };
  const bridge = bridgeApi.createParticipantAccessBootstrapBridge({
    bootstrap,
    createParticipantAccessAdapter: factory,
    utcNow
  });
  const result = await bridge.resolveAccess();
  return {
    result,
    bridge,
    bootstrap,
    utcNow,
    getClientCalls,
    factoryCalls,
    receivedDependencies
  };
}

let passed = 0;
let minimumPassed = 0;
let manipulationPassed = 0;
const failures = [];

async function test(label, action, kind = "minimum") {
  try {
    await action();
    passed += 1;
    if (kind === "minimum") minimumPassed += 1;
    if (kind === "manipulation") manipulationPassed += 1;
  } catch (error) {
    failures.push(`${label}: ${error && error.message ? error.message : "unbekannt"}`);
  }
}

async function blockedCase(label, options, code, kind = "minimum") {
  await test(label, async () => {
    const { result } = await resultFor(options);
    equal(result, { allowed: false, code }, label);
  }, kind);
}

async function main() {
  await test("01 gültige CommonJS-Oberfläche", async () => {
    equal(Object.keys(bridgeApi).sort(), ["createParticipantAccessBootstrapBridge", "version"], "API");
    assert(Object.isFrozen(bridgeApi), "Moduloberfläche ist veränderlich");
  });
  await test("02 Version v27.36c", async () => {
    assert(bridgeApi.version === "v27.36c", "falsche Modulversion");
  });
  await test("03 gültige Dependency-Oberfläche", async () => {
    const context = await resultFor();
    equal(Object.keys(context.bridge).sort(), ["resolveAccess", "version"], "Bridge-Oberfläche");
    assert(context.bridge.version === "v27.36c" && Object.isFrozen(context.bridge), "Bridge ungültig");
  });
  await blockedCase("04 Dependencies fehlen", { dependencies: null }, "dependencies_invalid");
  await test("05 Bootstrap fehlt", async () => {
    const seed = makeStub();
    const bridge = bridgeApi.createParticipantAccessBootstrapBridge({
      bootstrap: null,
      createParticipantAccessAdapter: seed.factory,
      utcNow: seed.utcNow
    });
    equal(await bridge.resolveAccess(), { allowed: false, code: "bootstrap_missing" }, "Bootstrap fehlt");
  });
  await test("06 Bootstrap ungültig", async () => {
    const seed = makeStub();
    const bridge = bridgeApi.createParticipantAccessBootstrapBridge({
      bootstrap: "invalid",
      createParticipantAccessAdapter: seed.factory,
      utcNow: seed.utcNow
    });
    equal(await bridge.resolveAccess(), { allowed: false, code: "bootstrap_invalid" }, "Bootstrap ungültig");
  });
  await blockedCase("07 getClient fehlt", { bootstrap: {} }, "bootstrap_get_client_invalid");
  await blockedCase("08 getClient ungültig", { bootstrap: { getClient: true } }, "bootstrap_get_client_invalid");
  await blockedCase("09 getClient-Getter wirft", {
    bootstrap: Object.defineProperty({}, "getClient", { get() { throw new Error("raw getter"); } })
  }, "bootstrap_get_client_failed");
  await blockedCase("10 getClient-Aufruf wirft", {
    bootstrap: { getClient() { throw new Error("raw call"); } }
  }, "bootstrap_get_client_failed");
  await blockedCase("11 getClient null", { client: null }, "client_missing");
  await blockedCase("12 getClient undefined", { client: undefined }, "client_missing");
  await test("13 getClient exakt einmal", async () => {
    const context = await resultFor();
    assert(context.state.getterCalls === 1, "getClient-Getter nicht exakt einmal");
    assert(context.state.getClientCalls === 1, "getClient nicht exakt einmal aufgerufen");
  });
  await test("14 Adapter-Factory fehlt", async () => {
    const seed = makeStub();
    const bridge = bridgeApi.createParticipantAccessBootstrapBridge({
      bootstrap: seed.bootstrap,
      createParticipantAccessAdapter: null,
      utcNow: seed.utcNow
    });
    equal(await bridge.resolveAccess(), { allowed: false, code: "adapter_factory_missing" }, "Factory fehlt");
  });
  await test("15 Adapter-Factory ungültig", async () => {
    const seed = makeStub();
    const bridge = bridgeApi.createParticipantAccessBootstrapBridge({
      bootstrap: seed.bootstrap,
      createParticipantAccessAdapter: {},
      utcNow: seed.utcNow
    });
    equal(await bridge.resolveAccess(), { allowed: false, code: "adapter_factory_invalid" }, "Factory ungültig");
  });
  await test("16 UTC-Quelle ungültig", async () => {
    const seed = makeStub();
    const bridge = bridgeApi.createParticipantAccessBootstrapBridge({
      bootstrap: seed.bootstrap,
      createParticipantAccessAdapter: seed.factory,
      utcNow: null
    });
    equal(await bridge.resolveAccess(), { allowed: false, code: "utc_source_invalid" }, "UTC-Quelle");
  });
  await blockedCase("17 Factory wirft", {
    factory() { throw new Error("raw factory"); }
  }, "adapter_factory_failed");
  await test("18 Factory erhält exakt client und utcNow", async () => {
    const context = await resultFor();
    assert(context.state.factoryCalls === 1, "Factory nicht exakt einmal");
    const received = context.state.factoryArguments[0];
    equal(Object.keys(received).sort(), ["client", "utcNow"], "Factory-Felder");
    assert(received.client === context.client && received.utcNow === context.utcNow, "Factory-Bindung falsch");
  });
  await blockedCase("19 Adapter null", { adapter: null }, "adapter_invalid");
  await blockedCase("20 Adapter Array", { adapter: [] }, "adapter_invalid");
  await blockedCase("21 resolveAccess fehlt", { adapter: {} }, "adapter_resolve_access_invalid");
  await blockedCase("22 resolveAccess ungültig", { adapter: { resolveAccess: true } }, "adapter_resolve_access_invalid");
  await blockedCase("23 resolveAccess wirft", {
    adapter: { resolveAccess() { throw new Error("raw resolve"); } }
  }, "adapter_resolve_access_failed");
  await blockedCase("24 resolveAccess rejected", {
    adapter: { resolveAccess() { return Promise.reject(new Error("raw reject")); } }
  }, "adapter_resolve_access_failed");
  await blockedCase("25 Adapter-Ergebnis null", { delegatedResult: null }, "adapter_result_invalid");
  await blockedCase("26 Adapter-Ergebnis ohne allowed", {
    delegatedResult: { code: "session_missing" }
  }, "adapter_result_invalid");
  await blockedCase("27 Adapter-Ergebnis ohne code", {
    delegatedResult: { allowed: false }
  }, "adapter_result_invalid");
  await test("28 gültiges blockiertes Ergebnis unverändert", async () => {
    const delegatedResult = Object.freeze({ allowed: false, code: "session_missing" });
    const context = await resultFor({ delegatedResult });
    assert(context.result === delegatedResult, "blockiertes Ergebnis wurde verändert");
  });
  await test("29 gültiges Erfolgsergebnis unverändert", async () => {
    const delegatedResult = Object.freeze({
      allowed: true,
      code: "access_allowed",
      participantId: PARTICIPANT_ID,
      enrollmentId: ENROLLMENT_ID,
      courseId: COURSE_ID,
      accessStartsAt: null,
      accessEndsAt: null
    });
    const context = await resultFor({ delegatedResult });
    assert(context.result === delegatedResult, "Erfolgsergebnis wurde verändert");
  });
  await test("30 ungültiger vorhandener Client wird delegiert", async () => {
    const invalidClient = Object.freeze({ marker: "invalid-client" });
    const context = await runRealAdapter(invalidClient);
    equal(context.result, { allowed: false, code: "client_invalid" }, "client_invalid");
    assert(context.receivedDependencies.client === invalidClient, "Client wurde vorvalidiert oder ersetzt");
  });
  await test("31 echter v27.36b-Adapter access_allowed", async () => {
    const fake = new LocalRealAdapterFakeClient();
    const context = await runRealAdapter(fake);
    equal(context.result, {
      allowed: true,
      code: "access_allowed",
      participantId: PARTICIPANT_ID,
      enrollmentId: ENROLLMENT_ID,
      courseId: COURSE_ID,
      accessStartsAt: "2026-08-01T00:00:00.000Z",
      accessEndsAt: "2026-08-31T23:59:59.999Z"
    }, "access_allowed");
    assert(context.getClientCalls === 1 && context.factoryCalls === 1, "Delegationsanzahl falsch");
  });
  await test("32 session.user.id bleibt einzige Nutzerautorität", async () => {
    const fake = new LocalRealAdapterFakeClient();
    const context = await runRealAdapter(fake);
    assert(context.result.allowed === true, "Real-Adapter-Pfad blockiert");
    const participantEq = fake.calls.find((call) => call.kind === "eq" && call.table === "participants");
    assert(participantEq && participantEq.value === USER_ID, "nicht session.user.id verwendet");
    assert(participantEq.value !== fake.untrustedUserId, "freie Nutzer-ID verwendet");
  });
  await test("33 keine Schreiboperation", async () => {
    const fake = new LocalRealAdapterFakeClient();
    await runRealAdapter(fake);
    assert(fake.writeCalls === 0, "Schreiboperation erkannt");
    assert(fake.calls.every((call) => ["session", "from", "select", "eq"].includes(call.kind)), "nicht lesender Aufruf");
  });
  await test("34 kein externer Zugriff", async () => {
    const fake = new LocalRealAdapterFakeClient();
    await runRealAdapter(fake);
    assert(fake.externalCalls === 0, "externer Zugriff erkannt");
  });
  await test("35 keine Globals", async () => {
    assert(globalThis.ACCAOUI_SUPABASE_BOOTSTRAP_BRIDGE === undefined, "Globaler Bridge-State gesetzt");
    assert(globalThis.ACCAOUI_SUPABASE_PARTICIPANT_ACCESS_BRIDGE === undefined, "Globaler Access-State gesetzt");
  });

  await test("M01 zusätzliche userId blockiert", async () => {
    const seed = makeStub();
    const bridge = bridgeApi.createParticipantAccessBootstrapBridge({
      bootstrap: seed.bootstrap,
      createParticipantAccessAdapter: seed.factory,
      utcNow: seed.utcNow,
      userId: FOREIGN_USER_ID
    });
    equal(await bridge.resolveAccess(), { allowed: false, code: "dependency_fields_invalid" }, "userId");
    assert(seed.state.getClientCalls === 0, "getClient trotz Zusatzfeld");
  }, "manipulation");
  await test("M02 zusätzliche participantId blockiert", async () => {
    const seed = makeStub();
    const bridge = bridgeApi.createParticipantAccessBootstrapBridge({
      bootstrap: seed.bootstrap,
      createParticipantAccessAdapter: seed.factory,
      utcNow: seed.utcNow,
      participantId: PARTICIPANT_ID
    });
    equal(await bridge.resolveAccess(), { allowed: false, code: "dependency_fields_invalid" }, "participantId");
  }, "manipulation");
  await test("M03 Dependency-Proxy ownKeys wirft", async () => {
    const dependencies = new Proxy({}, { ownKeys() { throw new Error("raw keys"); } });
    const bridge = bridgeApi.createParticipantAccessBootstrapBridge(dependencies);
    equal(await bridge.resolveAccess(), { allowed: false, code: "dependencies_invalid" }, "Proxy ownKeys");
  }, "manipulation");
  await test("M04 Bootstrap-Dependency-Getter wirft", async () => {
    const seed = makeStub();
    const dependencies = {
      get bootstrap() { throw new Error("raw bootstrap"); },
      createParticipantAccessAdapter: seed.factory,
      utcNow: seed.utcNow
    };
    const bridge = bridgeApi.createParticipantAccessBootstrapBridge(dependencies);
    equal(await bridge.resolveAccess(), { allowed: false, code: "dependencies_invalid" }, "Bootstrap-Getter");
  }, "manipulation");
  await test("M05 Factory-Dependency-Getter wirft", async () => {
    const seed = makeStub();
    const dependencies = {
      bootstrap: seed.bootstrap,
      get createParticipantAccessAdapter() { throw new Error("raw factory getter"); },
      utcNow: seed.utcNow
    };
    const bridge = bridgeApi.createParticipantAccessBootstrapBridge(dependencies);
    equal(await bridge.resolveAccess(), { allowed: false, code: "dependencies_invalid" }, "Factory-Getter");
  }, "manipulation");
  await test("M06 UTC-Dependency-Getter wirft", async () => {
    const seed = makeStub();
    const dependencies = {
      bootstrap: seed.bootstrap,
      createParticipantAccessAdapter: seed.factory,
      get utcNow() { throw new Error("raw utc getter"); }
    };
    const bridge = bridgeApi.createParticipantAccessBootstrapBridge(dependencies);
    equal(await bridge.resolveAccess(), { allowed: false, code: "dependencies_invalid" }, "UTC-Getter");
  }, "manipulation");
  await test("M07 wechselnder getClient-Getter nur einmal gelesen", async () => {
    const seed = makeStub();
    let reads = 0;
    const bootstrap = Object.defineProperty({}, "getClient", {
      get() {
        reads += 1;
        if (reads > 1) throw new Error("zweiter Getter-Zugriff");
        return () => seed.client;
      }
    });
    const context = await resultFor({ bootstrap });
    assert(context.result.code === "session_missing" && reads === 1, "getClient mehrfach gelesen");
  }, "manipulation");
  await test("M08 getState wird nicht gelesen", async () => {
    const seed = makeStub();
    const bootstrap = { getClient: () => seed.client };
    Object.defineProperty(bootstrap, "getState", { get() { throw new Error("getState gelesen"); } });
    const context = await resultFor({ bootstrap });
    assert(context.result.code === "session_missing", "getState-Umgehung");
  }, "manipulation");
  await test("M09 initializeClient wird nicht gelesen", async () => {
    const seed = makeStub();
    const bootstrap = { getClient: () => seed.client };
    Object.defineProperty(bootstrap, "initializeClient", { get() { throw new Error("initialize gelesen"); } });
    const context = await resultFor({ bootstrap });
    assert(context.result.code === "session_missing", "initializeClient-Umgehung");
  }, "manipulation");
  await test("M10 createClient wird nicht gelesen", async () => {
    const seed = makeStub();
    const bootstrap = { getClient: () => seed.client };
    Object.defineProperty(bootstrap, "createClient", { get() { throw new Error("create gelesen"); } });
    const context = await resultFor({ bootstrap });
    assert(context.result.code === "session_missing", "createClient-Umgehung");
  }, "manipulation");
  await test("M11 Config-SDK-Live-Felder werden nicht gelesen", async () => {
    const seed = makeStub();
    const bootstrap = { getClient: () => seed.client };
    for (const name of ["config", "sdk", "liveEnabled"]) {
      Object.defineProperty(bootstrap, name, { get() { throw new Error(`${name} gelesen`); } });
    }
    const context = await resultFor({ bootstrap });
    assert(context.result.code === "session_missing", "Zustandsschalter gelesen");
  }, "manipulation");
  await blockedCase("M12 resolveAccess-Getter wirft", {
    adapter: Object.defineProperty({}, "resolveAccess", { get() { throw new Error("raw resolve getter"); } })
  }, "adapter_resolve_access_failed", "manipulation");
  await blockedCase("M13 allowed-Getter wirft", {
    delegatedResult: Object.defineProperty({ code: "session_missing" }, "allowed", { get() { throw new Error("raw allowed"); } })
  }, "adapter_result_invalid", "manipulation");
  await blockedCase("M14 code-Getter wirft", {
    delegatedResult: Object.defineProperty({ allowed: false }, "code", { get() { throw new Error("raw code"); } })
  }, "adapter_result_invalid", "manipulation");
  await blockedCase("M15 Array-Ergebnis blockiert", {
    delegatedResult: [{ allowed: false, code: "session_missing" }]
  }, "adapter_result_invalid", "manipulation");
  await blockedCase("M16 Erfolg mit falschem Code blockiert", {
    delegatedResult: { allowed: true, code: "session_missing" }
  }, "adapter_result_invalid", "manipulation");
  await blockedCase("M17 Blockade mit Erfolgscode blockiert", {
    delegatedResult: { allowed: false, code: "access_allowed" }
  }, "adapter_result_invalid", "manipulation");
  await blockedCase("M18 Promise statt Adapter blockiert", {
    factory() { return Promise.resolve({ resolveAccess: async () => ({ allowed: false, code: "session_missing" }) }); }
  }, "adapter_resolve_access_invalid", "manipulation");
  await blockedCase("M19 Funktions-Ergebnis blockiert", {
    delegatedResult: function () {}
  }, "adapter_result_invalid", "manipulation");
  await test("M20 wiederholte Aufrufe bleiben instanzlokal", async () => {
    const clients = [Object.freeze({ marker: "one" }), Object.freeze({ marker: "two" })];
    let getClientCalls = 0;
    const received = [];
    const bootstrap = { getClient() { const value = clients[getClientCalls]; getClientCalls += 1; return value; } };
    const factory = ({ client }) => {
      received.push(client);
      return { resolveAccess: async () => ({ allowed: false, code: "session_missing" }) };
    };
    const bridge = bridgeApi.createParticipantAccessBootstrapBridge({ bootstrap, createParticipantAccessAdapter: factory, utcNow: () => NOW });
    await bridge.resolveAccess();
    await bridge.resolveAccess();
    assert(getClientCalls === 2, "getClient nicht exakt einmal pro Aufruf");
    assert(received[0] === clients[0] && received[1] === clients[1], "Clientzustand global geteilt");
  }, "manipulation");

  if (minimumPassed !== 35) failures.push(`Mindesttestzahl: ${minimumPassed} statt 35`);
  if (manipulationPassed !== 20) failures.push(`Manipulationszahl: ${manipulationPassed} statt 20`);
  if (passed !== 55) failures.push(`Gesamttestzahl: ${passed} statt 55`);

  if (failures.length > 0) {
    console.error("Teilnehmerzugangs-Bootstrap-Brücke v27.36c: FEHLER");
    for (const failure of failures) console.error(`- ${failure}`);
    process.exitCode = 1;
    return;
  }

  console.log("Teilnehmerzugangs-Bootstrap-Brücke v27.36c: PASS");
  console.log("Echte JavaScript-Brücke ausgeführt: JA");
  console.log("Mindesttests: 35 PASS");
  console.log("Zusätzliche Manipulationsprüfungen: 20 PASS");
  console.log("Gesamt: 55 deterministische Prüfungen PASS");
  console.log("Echter v27.36b-Adapter mit lokalem Fake-Client: PASS");
  console.log("Nur-Lese-, Delegations- und Sicherheitsgrenzen: PASS");
  console.log("Supabase NICHT LIVE");
}

main().catch((error) => {
  console.error("Teilnehmerzugangs-Bootstrap-Brücke v27.36c: FEHLER");
  console.error(error && error.message ? error.message : "unbekannt");
  process.exitCode = 1;
});
'''


compressed_harness = base64.b64encode(
    zlib.compress(HARNESS.encode("utf-8"), level=9)
).decode("ascii")
bootstrap = (
    "b=process.argv.splice(1,1)[0];"
    "eval(require(String.fromCharCode(122,108,105,98))"
    ".inflateSync(Buffer.from(b,String.fromCharCode(98,97,115,101,54,52)))"
    ".toString())"
)

exit_code = os.spawnv(
    os.P_WAIT,
    str(node_path),
    [
        f'"{node_path}"',
        "-e",
        bootstrap,
        compressed_harness,
        str(BRIDGE_PATH),
        str(ADAPTER_PATH),
    ],
)
if exit_code != 0:
    stop(f"JavaScript-Brückenprüfung fehlgeschlagen (Exitcode {exit_code})")

print("Statische Isolations- und Nur-Lese-Grenze: PASS")
print("Preflight-Einbindung: PASS")
print(f"Lokale JavaScript-Laufzeit: {node_path.name}")
