#!/usr/bin/env python3
"""Prueft die v27.37b-Bruecke lokal mit Fakes und echten Quellmutationen."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BRIDGE_PATH = ROOT / "data/supabase-participant-auth-session-bootstrap-bridge.js"
AUTH_PATH = ROOT / "data/supabase-participant-auth-session-adapter.js"
ACCESS_PATH = ROOT / "data/supabase-participant-access-adapter.js"
REPORT_PATH = ROOT / "docs/SUPABASE_PARTICIPANT_AUTH_SESSION_BOOTSTRAP_BRIDGE_V2737B.md"
FACTORY = "createParticipantAuthSessionBootstrapBridge"
BROWSER_FACTORY = (
    "ACCAOUI_PARTICIPANT_AUTH_SESSION_BOOTSTRAP_BRIDGE_FACTORY"
)


def stop(message: str) -> None:
    print(f"STOPP: {message}")
    raise SystemExit(1)


def find_node() -> Path:
    for candidate in (
        shutil.which("node"),
        "C:/Program Files/nodejs/node.exe",
        "C:/Program Files (x86)/nodejs/node.exe",
        "/usr/bin/node", "/usr/local/bin/node", "/opt/homebrew/bin/node",
    ):
        if candidate and Path(candidate).is_file():
            return Path(candidate)
    stop("erforderliche lokale JavaScript-Laufzeit fehlt")
    raise AssertionError("unreachable")


def run_node(node: Path, arguments: list[str]) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            [str(node), *arguments], cwd=ROOT, capture_output=True,
            text=True, encoding="utf-8", check=False, timeout=25,
        )
    except (OSError, subprocess.TimeoutExpired):
        stop("lokale JavaScript-Pruefung nicht ausfuehrbar oder Zeitlimit erreicht")
    raise AssertionError("unreachable")


def get_checker_temp_root() -> Path:
    # Absichtlich kein System-Temp-Fallback und kein alternativer Schreibort.
    git_dir = ROOT / ".git"
    if not git_dir.is_dir():
        stop("lokales .git-Verzeichnis fuer den vorgeschriebenen Tempbereich fehlt")
    target = git_dir / "accaoui-checker-temp" / "v2737b-auth-bridge"
    try:
        target.mkdir(parents=True, exist_ok=True)
    except OSError:
        stop("UMGEBUNGSBLOCKER: vorgeschriebener Git-Tempbereich nicht beschreibbar")
    return target


def source_contract_errors(source: str) -> list[str]:
    errors: list[str] = []
    code = re.sub(r"//[^\n]*|/\*[\s\S]*?\*/", "", source)
    commonjs_exports = re.findall(
        r"\b(?:module|commonJsModule)\s*\.\s*exports\s*=", code
    )
    if len(commonjs_exports) != 1:
        errors.append("CommonJS-Export fehlt oder ist mehrfach vorhanden")
    if not re.search(r"\bfunction\s+" + FACTORY + r"\s*\(\s*dependencies\s*\)", code):
        errors.append("erwartete injizierte Factory fehlt")

    required_browser = (
        "(function exposeParticipantAuthSessionBootstrapBridge(",
        "commonJsModule.exports = participantAuthSessionBootstrapBridgeApi;",
        "browserRoot." + BROWSER_FACTORY + ";",
        '"' + BROWSER_FACTORY + '",',
        "if (existingFactory === undefined) {",
        "Object.defineProperty(",
        "value: createParticipantAuthSessionBootstrapBridge,",
        "enumerable: true,",
        "configurable: false,",
        "writable: false",
        'typeof window !== "undefined" ? window : null,',
        'typeof module !== "undefined" ? module : null',
    )
    for marker in required_browser:
        if source.count(marker) != 1:
            errors.append("Browser-Export-Vertrag nicht exakt: " + marker)

    if source.count("window") != 2:
        errors.append("Browser-window darf nur in der kontrollierten Grenze vorkommen")
    if source.count(BROWSER_FACTORY) != 2:
        errors.append("Browser-Factory-Grenze ist nicht exakt")

    forbidden = (
        r"\b(?:self|globalThis|document|DOM)\b",
        r"\b(?:localStorage|sessionStorage|indexedDB|caches|CacheStorage|cookies?)\b",
        r"\b(?:fetch|XMLHttpRequest|WebSocket|EventSource|sendBeacon)\b",
        r"\b(?:initializeClient|createClient|getState)\b",
        r"\.\s*from\s*\(",
        r"\b(?:participants|enrollments|courses|SQL|migrations?)\b",
        r"\b(?:require|import|export)\b",
        r"\b(?:process|console|setTimeout|setInterval)\b",
        r"\b(?:access_token|refresh_token|password|email|config|session|user)\b",
        r"\b\w*error\s*\.\s*message\b",
    )
    for pattern in forbidden:
        if re.search(pattern, code, re.IGNORECASE):
            errors.append("verbotene Konstruktion: " + pattern)
    if re.search(r"\b(?:eval|Function)\s*\(", code):
        errors.append("dynamische Codeausfuehrung")
    for receiver, allowed in (("bootstrap", {"getClient"}), ("client", {"auth"})):
        members = set(re.findall(r"\b" + receiver + r"\s*\.\s*([A-Za-z_$][\w$]*)", code))
        if members != allowed:
            errors.append(receiver + "-Oberflaeche nicht exakt: " + ",".join(sorted(members)))
        if re.search(r"\b" + receiver + r"\s*\[", code):
            errors.append("dynamischer Zugriff auf " + receiver)
    if re.search(r"\bauth\s*(?:\.|\[)", code):
        errors.append("eigene Auth-Operation in der Bruecke")
    return errors


HARNESS = r'''"use strict";
const fs = require("fs");
const vm = require("vm");
const bridgePath = process.argv[2];
const authPath = process.argv[3];
const accessPath = process.argv[4];
const bridgeSource = fs.readFileSync(bridgePath,"utf8");
const BROWSER_FACTORY =
  "ACCAOUI_PARTICIPANT_AUTH_SESSION_BOOTSTRAP_BRIDGE_FACTORY";
const METHODS = ["resolveSession", "signIn", "signOut"];
const PAIRS = {
  resolveSession: [[true,"session_available"],[false,"session_missing"],[false,"session_invalid"],[false,"auth_error"]],
  signIn: [[true,"signed_in"],[false,"credentials_invalid"],[false,"sign_in_failed"],[false,"auth_error"]],
  signOut: [[true,"signed_out"],[false,"sign_out_failed"],[false,"auth_error"]]
};
const SECRET = "SYNTHETIC_PRIVATE_ERROR";
const USER_ID = "11111111-1111-4111-8111-111111111111";
const PARTICIPANT_ID = "22222222-2222-4222-8222-222222222222";
const ENROLLMENT_ID = "33333333-3333-4333-8333-333333333333";
const COURSE_ID = "44444444-4444-4444-8444-444444444444";
let positive = 0;
let negative = 0;
let sharedSignIn = false;
let sharedSignOut = false;
const failures = [];
let createBridge;

function assert(condition, label) {
  if (!condition) throw new Error(label);
}
function equal(actual, expected, label) {
  assert(JSON.stringify(actual) === JSON.stringify(expected), label);
}
async function test(kind, label, body) {
  try {
    await body();
    if (kind === "positive") positive += 1;
    else negative += 1;
  } catch (_) {
    // Nur synthetische Testnamen, niemals eine rohe Exception ausgeben.
    failures.push(label);
  }
}
function frozen(ok, code) { return Object.freeze({ok, code}); }
function success(method) { return frozen(...PAIRS[method][0]); }
function validate(value, ok, code) {
  assert(value !== null && typeof value === "object", "Objekttyp");
  assert(Object.getPrototypeOf(value) === Object.prototype, "Plain Object");
  assert(Object.isFrozen(value), "frozen");
  equal(Reflect.ownKeys(value).sort(), ["code", "ok"], "exakte eigene Keys");
  for (const key of ["ok", "code"]) {
    const field = Object.getOwnPropertyDescriptor(value, key);
    assert(field && field.enumerable && Object.hasOwn(field,"value"), "Datenproperty");
  }
  assert(typeof value.ok === "boolean" && typeof value.code === "string", "Typen");
  assert(value.ok === ok && value.code === code, "Ergebnispaar");
  const serialized = JSON.stringify(value);
  for (const secret of [SECRET,USER_ID,"synthetic@example.invalid","SYNTHETIC_ACCESS_TOKEN","SYNTHETIC_REFRESH_TOKEN"]) {
    assert(!serialized.includes(secret), "keine sensitiven Werte");
  }
}
function validateError(value) { validate(value,false,"auth_error"); }
function invoke(bridge, method, credentials) {
  return method === "signIn" ? bridge.signIn(credentials) : bridge[method]();
}
function throwing() { throw new Error(SECRET); }
function revoked() {
  const entry = Proxy.revocable({},{}); entry.revoke(); return entry.proxy;
}

// Pro Operation entstehen neue Auth-/Client-/Adapteridentitaeten. Die Fakes
// verweigern jeden nicht autorisierten Propertyzugriff und kontrollieren this.
function probe(resultFor = (method) => success(method)) {
  const state = {
    getReads:0, getCalls:0, authReads:0, factoryCalls:0,
    methodReads:{resolveSession:0,signIn:0,signOut:0},
    methodCalls:{resolveSession:0,signIn:0,signOut:0},
    clients:[], auths:[], adapters:[], received:[],
  };
  let pendingAuth;
  const bootstrap = {};
  Object.defineProperty(bootstrap,"getClient",{
    enumerable:true,
    get() {
      state.getReads += 1;
      return function() {
        assert(this === bootstrap && arguments.length === 0,"Bootstrap Receiver/Argumente");
        state.getCalls += 1;
        const auth = new Proxy({}, {get:throwing});
        const client = new Proxy({auth}, {
          get(target,key) {
            assert(key === "auth","ausschliesslich client.auth");
            state.authReads += 1;
            return target.auth;
          }
        });
        pendingAuth = auth;
        state.auths.push(auth); state.clients.push(client);
        return client;
      };
    }
  });
  function createParticipantAuthSessionAdapter(dependencies) {
    assert(arguments.length === 1,"genau ein Factoryargument");
    equal(Reflect.ownKeys(dependencies),["auth"],"exakt auth Dependency");
    assert(Object.getPrototypeOf(dependencies) === Object.prototype,"Factorydatenobjekt");
    assert(dependencies.auth === pendingAuth,"aktuelle Authidentitaet");
    state.factoryCalls += 1;
    const auth = dependencies.auth;
    let adapter;
    adapter = new Proxy({}, {
      get(_target,key) {
        assert(METHODS.includes(key),"ausschliesslich passende Adaptermethode");
        state.methodReads[key] += 1;
        return function(...args) {
          assert(this === adapter,"Adapter Receiver");
          assert(args.length === (key === "signIn" ? 1 : 0),"Methodenargumentanzahl");
          state.methodCalls[key] += 1;
          state.received.push({method:key,args,auth});
          return resultFor(key,args,auth);
        };
      }
    });
    state.adapters.push(adapter);
    return adapter;
  }
  return {state,dependencies:{bootstrap,createParticipantAuthSessionAdapter}};
}
function counts(state, methods) {
  const expected = {resolveSession:0,signIn:0,signOut:0};
  for (const method of methods) expected[method] += 1;
  for (const key of ["getReads","getCalls","authReads","factoryCalls"]) {
    assert(state[key] === methods.length,key);
  }
  equal(state.methodReads,expected,"Methodenlesezugriffe");
  equal(state.methodCalls,expected,"Methodenaufrufe");
  for (const key of ["clients","auths","adapters"]) {
    assert(state[key].length === methods.length && new Set(state[key]).size === methods.length,"frische Identitaeten");
  }
}
function depsReturning(value) {
  return {bootstrap:{getClient:()=>({auth:{}})}, createParticipantAuthSessionAdapter:()=>({
    resolveSession:()=>value,signIn:()=>value,signOut:()=>value,
  })};
}
async function expectedBoundaryError(dependencies, method) {
  const bridge = createBridge(dependencies);
  validateError(await invoke(bridge,method,revoked()));
}

async function main() {
  await test("positive","CommonJS require ohne Seiteneffekte",async()=>{
    const sandbox = {module:{exports:{}}};
    sandbox.exports = sandbox.module.exports;
    for (const key of ["self","globalThis","document","localStorage","sessionStorage","indexedDB","caches","fetch","XMLHttpRequest","WebSocket","EventSource","navigator","console","process","setTimeout","setInterval","require","bootstrap","auth","createParticipantAuthSessionAdapter"]) {
      Object.defineProperty(sandbox,key,{get:throwing,set:throwing});
    }
    vm.runInNewContext(bridgeSource,sandbox,{timeout:2000});
    equal(Reflect.ownKeys(sandbox.module.exports),["createParticipantAuthSessionBootstrapBridge"],"CommonJS Export");
    assert(Object.isFrozen(sandbox.module.exports),"Module frozen");
  });

  await test("positive","Browser-Export ohne Ladezugriff",async()=>{
    const browserWindow = {};
    const moduleBox = {exports:{}};
    const sandbox = {window:browserWindow,module:moduleBox};

    for (const key of ["bootstrap","auth","createParticipantAuthSessionAdapter","document","localStorage","sessionStorage","fetch"]) {
      Object.defineProperty(sandbox,key,{get:throwing,set:throwing});
    }

    vm.runInNewContext(bridgeSource,sandbox,{timeout:2000});

    const descriptor =
      Object.getOwnPropertyDescriptor(browserWindow,BROWSER_FACTORY);
    assert(descriptor,"Browser-Descriptor fehlt");
    assert(
      browserWindow[BROWSER_FACTORY] ===
        moduleBox.exports.createParticipantAuthSessionBootstrapBridge,
      "Browser-/CommonJS-Factory nicht identisch"
    );
    assert(descriptor.enumerable === true,"Browser-Factory nicht enumerable");
    assert(descriptor.configurable === false,"Browser-Factory configurable");
    assert(descriptor.writable === false,"Browser-Factory writable");
  });

  await test("positive","Browser-only Export",async()=>{
    const browserWindow = {};
    vm.runInNewContext(
      bridgeSource,
      {window:browserWindow},
      {timeout:2000}
    );
    assert(
      typeof browserWindow[BROWSER_FACTORY] === "function",
      "Browser-only Factory fehlt"
    );
  });

  await test("positive","Bestehende Browser-Grenze bleibt erhalten",async()=>{
    for (const existing of [null,false,0,"occupied",{},function occupied(){}]) {
      const browserWindow = {};
      Object.defineProperty(browserWindow,BROWSER_FACTORY,{
        value:existing,
        enumerable:false,
        configurable:true,
        writable:true
      });
      vm.runInNewContext(
        bridgeSource,
        {window:browserWindow},
        {timeout:2000}
      );
      assert(
        browserWindow[BROWSER_FACTORY] === existing,
        "bestehende Browser-Grenze überschrieben"
      );
    }
  });

  await test("positive","Fehlerhafte Browser-Grenzen bleiben passiv",async()=>{
    const throwingWindow = {};
    Object.defineProperty(throwingWindow,BROWSER_FACTORY,{
      configurable:true,
      get:throwing
    });
    vm.runInNewContext(
      bridgeSource,
      {window:throwingWindow},
      {timeout:2000}
    );

    const sealedWindow = Object.preventExtensions({});
    vm.runInNewContext(
      bridgeSource,
      {window:sealedWindow},
      {timeout:2000}
    );
    assert(
      !Object.prototype.hasOwnProperty.call(sealedWindow,BROWSER_FACTORY),
      "nicht beschreibbare Browser-Grenze verändert"
    );
  });
  const api = require(bridgePath);
  createBridge = api.createParticipantAuthSessionBootstrapBridge;
  await test("positive","exakte CommonJS Factory und frozen API",async()=>{
    equal(Reflect.ownKeys(api),["createParticipantAuthSessionBootstrapBridge"],"Module Keys");
    assert(Object.isFrozen(api) && typeof createBridge === "function","Module API");
    const fake = probe(); const bridge = createBridge(fake.dependencies);
    equal(Reflect.ownKeys(bridge).sort(),METHODS.slice().sort(),"genau drei Methoden");
    assert(Object.isFrozen(bridge),"frozen API");
    for (const method of METHODS) assert(typeof bridge[method] === "function","Methodentyp");
    counts(fake.state,[]);
  });
  await test("positive","Factory liest keine Dependencies oder Getter",async()=>{
    let touches = 0;
    const poison = new Proxy({}, {
      get(){touches += 1;throwing();},ownKeys(){touches += 1;throwing();},
      getPrototypeOf(){touches += 1;throwing();},getOwnPropertyDescriptor(){touches += 1;throwing();}
    });
    const bridge = createBridge(poison);
    assert(touches === 0 && Object.isFrozen(bridge),"Factory nicht lazy");
  });
  for (const method of METHODS) {
    for (const [ok,code] of PAIRS[method]) {
      for (const asynchronous of [false,true]) {
        await test("positive",`${method} ${code} identisch ${asynchronous}`,async()=>{
          const original = frozen(ok,code);
          const fake = probe(()=>asynchronous ? Promise.resolve(original) : original);
          const credentials = Object.freeze({email:"synthetic@example.invalid",password:SECRET});
          const value = await invoke(createBridge(fake.dependencies),method,credentials);
          assert(value === original,"Ergebnisidentitaet"); validate(value,ok,code);
          counts(fake.state,[method]);
          if (method === "signIn") assert(fake.state.received[0].args[0] === credentials,"Credentialsidentitaet");
        });
      }
    }
  }
  const credentialsCases = [undefined,null,true,0," raw credentials ",Symbol("opaque"),[],{},revoked()];
  const accessorCredentials = Object.defineProperty({},"email",{get:throwing});
  credentialsCases.push(accessorCredentials);
  for (let index=0;index<credentialsCases.length;index+=1) {
    await test("positive",`Credentials ohne eigene Validierung ${index}`,async()=>{
      const credentials = credentialsCases[index];
      const fake = probe(); const bridge = createBridge(fake.dependencies);
      validate(await bridge.signIn(credentials),true,"signed_in");
      assert(fake.state.received[0].args[0] === credentials,"Credentials unveraendert");
      counts(fake.state,["signIn"]);
    });
  }
  for (const parallel of [false,true]) {
    await test("positive",`Client-/Adapterwechsel und Einzelaufrufe ${parallel}`,async()=>{
      const fake = probe(); const bridge = createBridge(fake.dependencies);
      const sequence = [...METHODS,...METHODS,...METHODS];
      if (parallel) await Promise.all(sequence.map(method=>invoke(bridge,method,SECRET)));
      else for (const method of sequence) validate(await invoke(bridge,method,SECRET),...PAIRS[method][0]);
      counts(fake.state,sequence);
    });
  }
  await test("positive","unabhaengige Brueckeninstanzen",async()=>{
    const first=probe(), second=probe();
    await createBridge(first.dependencies).resolveSession();
    await createBridge(second.dependencies).signOut();
    counts(first.state,["resolveSession"]); counts(second.state,["signOut"]);
  });

  const invalidResultFactories = [
    ["undefined",()=>undefined],["null",()=>null],["Boolean",()=>true],
    ["Zahl",()=>1],["String",()=>"auth_error"],["Array",()=>Object.freeze([])],
    ["Funktion",()=>Object.freeze(function(){})],["Date",()=>Object.freeze(new Date(0))],
    ["Klasseninstanz",()=>Object.freeze(new (class Result{constructor(){this.ok=false;this.code="auth_error";}})())],
    ["null Prototyp",()=>Object.freeze(Object.assign(Object.create(null),{ok:false,code:"auth_error"}))],
    ["fremder Prototyp",()=>Object.freeze(Object.create({ok:false,code:"auth_error"}))],
    ["nicht frozen",()=>({ok:false,code:"auth_error"})],
    ["sealed",()=>Object.seal({ok:false,code:"auth_error"})],
    ["ok fehlt",()=>Object.freeze({code:"auth_error"})],
    ["code fehlt",()=>Object.freeze({ok:false})],
    ["ok String",()=>frozen("false","auth_error")],
    ["ok Zahl",()=>frozen(0,"auth_error")],
    ["code Zahl",()=>frozen(false,1)],
    ["code Symbol",()=>frozen(false,Symbol("code"))],
    ["unbekannter Code",()=>frozen(false,"unmapped_internal_error")],
    ["falsches Paar",()=>frozen(true,"auth_error")],
    ["Symbol Zusatzkey",()=>Object.freeze({ok:false,code:"auth_error",[Symbol("private")]:SECRET})],
    ["nicht enumerable Zusatzkey",()=>Object.freeze(Object.defineProperty({ok:false,code:"auth_error"},"private",{value:SECRET}))],
    ["nicht enumerable ok",()=>Object.freeze(Object.defineProperty({code:"auth_error"},"ok",{value:false}))],
    ["nicht enumerable code",()=>Object.freeze(Object.defineProperty({ok:false},"code",{value:"auth_error"}))],
    ["ok Getter",()=>Object.freeze({get ok(){return false;},code:"auth_error"})],
    ["code Getter",()=>Object.freeze({ok:false,get code(){return "auth_error";}})],
    ["werfender ok Getter",()=>Object.freeze({get ok(){throwing();},code:"auth_error"})],
    ["werfender code Getter",()=>Object.freeze({ok:false,get code(){throwing();}})],
    ["revoked Proxy",revoked],
    ["then Getter",()=>Object.defineProperty({},"then",{get:throwing})],
  ];
  for (const field of ["session","user","id","email","password","token","access_token","refresh_token","client","auth","config","key","error","message","rawResponse"]) {
    invalidResultFactories.push([`sensitives Zusatzfeld ${field}`,()=>Object.freeze({ok:false,code:"auth_error",[field]:SECRET})]);
  }
  for (const trap of ["getPrototypeOf","ownKeys","isExtensible","getOwnPropertyDescriptor"]) {
    invalidResultFactories.push([`Result Proxy ${trap}`,()=>new Proxy(frozen(false,"auth_error"),{[trap]:throwing})]);
  }
  for (const field of ["ok","code"]) {
    invalidResultFactories.push([`Result Proxy get ${field}`,()=>new Proxy(frozen(false,"auth_error"),{
      get(target,key){if(key===field)throwing();return Reflect.get(target,key);}
    })]);
  }
  for (const method of METHODS) {
    for (const [name,maker] of invalidResultFactories) {
      await test("negative",`${method} Result ${name}`,async()=>{
        validateError(await invoke(createBridge(depsReturning(maker())),method,SECRET));
      });
    }
    const ownCodes = new Set(PAIRS[method].map(pair=>pair[1]));
    for (const [other,pairs] of Object.entries(PAIRS)) {
      if(other===method)continue;
      for (const [ok,code] of pairs) {
        if(ownCodes.has(code))continue;
        await test("negative",`${method} methodenfremd ${code}`,async()=>{
          validateError(await invoke(createBridge(depsReturning(frozen(ok,code))),method,SECRET));
        });
      }
    }
    for (const [name,makeDeps] of [
      ["Argument fehlt",()=>undefined],["null",()=>null],["Zahl",()=>3],
      ["Array",()=>[]],["Funktion",()=>function(){}],["leer",()=>({})],
      ["bootstrap fehlt",()=>({createParticipantAuthSessionAdapter:()=>({})})],
      ["Factory fehlt",()=>({bootstrap:{}})],
      ["dritte Dependency",()=>({...probe().dependencies,extra:{}})],
      ["Symbol Dependency",()=>({...probe().dependencies,[Symbol("extra")]:{}})],
      ["nicht enumerable Dependency",()=>Object.defineProperty(probe().dependencies,"extra",{value:{}})],
      ["geerbte Dependencies",()=>Object.create(probe().dependencies)],
      ["bootstrap Getter",()=>Object.defineProperty(probe().dependencies,"bootstrap",{get:throwing})],
      ["Factory Getter",()=>Object.defineProperty(probe().dependencies,"createParticipantAuthSessionAdapter",{get:throwing})],
      ["Dependencies ownKeys Proxy",()=>new Proxy(probe().dependencies,{ownKeys:throwing})],
      ["Dependencies get Proxy",()=>new Proxy(probe().dependencies,{get:throwing})],
      ["Dependencies revoked Proxy",revoked],
    ]) {
      await test("negative",`${method} Dependencies ${name}`,async()=>{
        await expectedBoundaryError(makeDeps(),method);
      });
    }
    const boundaryCases = [];
    for (const bad of [null,undefined,1,"x",[],function(){}]) {
      boundaryCases.push([`bootstrap Typ ${typeof bad} ${Array.isArray(bad)}`,()=>({bootstrap:bad,createParticipantAuthSessionAdapter:()=>({})})]);
      boundaryCases.push([`Factory Typ ${typeof bad} ${Array.isArray(bad)}`,()=>({bootstrap:{getClient:()=>({auth:{}})},createParticipantAuthSessionAdapter:bad})]);
      boundaryCases.push([`Client Typ ${typeof bad} ${Array.isArray(bad)}`,()=>({bootstrap:{getClient:()=>bad},createParticipantAuthSessionAdapter:throwing})]);
      boundaryCases.push([`Auth Typ ${typeof bad} ${Array.isArray(bad)}`,()=>({bootstrap:{getClient:()=>({auth:bad})},createParticipantAuthSessionAdapter:throwing})]);
      boundaryCases.push([`Adapter Typ ${typeof bad} ${Array.isArray(bad)}`,()=>({bootstrap:{getClient:()=>({auth:{}})},createParticipantAuthSessionAdapter:()=>bad})]);
      boundaryCases.push([`Methode Typ ${typeof bad} ${Array.isArray(bad)}`,()=>({bootstrap:{getClient:()=>({auth:{}})},createParticipantAuthSessionAdapter:()=>({[method]:bad})})]);
    }
    boundaryCases.push(
      ["getClient fehlt",()=>({bootstrap:{},createParticipantAuthSessionAdapter:throwing})],
      ["getClient keine Funktion",()=>({bootstrap:{getClient:7},createParticipantAuthSessionAdapter:throwing})],
      ["getClient Getter",()=>({bootstrap:Object.defineProperty({},"getClient",{get:throwing}),createParticipantAuthSessionAdapter:throwing})],
      ["getClient Throw",()=>({bootstrap:{getClient:throwing},createParticipantAuthSessionAdapter:throwing})],
      ["bootstrap Proxy",()=>({bootstrap:new Proxy({},{get:throwing}),createParticipantAuthSessionAdapter:throwing})],
      ["bootstrap revoked",()=>({bootstrap:revoked(),createParticipantAuthSessionAdapter:throwing})],
      ["Client auth fehlt",()=>({bootstrap:{getClient:()=>({})},createParticipantAuthSessionAdapter:throwing})],
      ["Client auth Getter",()=>({bootstrap:{getClient:()=>Object.defineProperty({},"auth",{get:throwing})},createParticipantAuthSessionAdapter:throwing})],
      ["Client Proxy",()=>({bootstrap:{getClient:()=>new Proxy({},{get:throwing})},createParticipantAuthSessionAdapter:throwing})],
      ["Client revoked",()=>({bootstrap:{getClient:revoked},createParticipantAuthSessionAdapter:throwing})],
      ["Auth revoked",()=>({bootstrap:{getClient:()=>({auth:revoked()})},createParticipantAuthSessionAdapter:throwing})],
      ["Factory Throw",()=>({bootstrap:{getClient:()=>({auth:{}})},createParticipantAuthSessionAdapter:throwing})],
      ["Factory Proxy apply",()=>({bootstrap:{getClient:()=>({auth:{}})},createParticipantAuthSessionAdapter:new Proxy(()=>({}),{apply:throwing})})],
      ["Adapter Proxy",()=>({bootstrap:{getClient:()=>({auth:{}})},createParticipantAuthSessionAdapter:()=>new Proxy({},{get:throwing})})],
      ["Adapter revoked",()=>({bootstrap:{getClient:()=>({auth:{}})},createParticipantAuthSessionAdapter:revoked})],
      ["Methode fehlt",()=>({bootstrap:{getClient:()=>({auth:{}})},createParticipantAuthSessionAdapter:()=>({})})],
      ["Methode Getter",()=>({bootstrap:{getClient:()=>({auth:{}})},createParticipantAuthSessionAdapter:()=>Object.defineProperty({},method,{get:throwing})})],
      ["Methode Throw",()=>({bootstrap:{getClient:()=>({auth:{}})},createParticipantAuthSessionAdapter:()=>({[method]:throwing})})],
      ["Methode Reject",()=>({bootstrap:{getClient:()=>({auth:{}})},createParticipantAuthSessionAdapter:()=>({[method]:()=>Promise.reject(new Error(SECRET))})})],
      ["Methode Proxy apply",()=>({bootstrap:{getClient:()=>({auth:{}})},createParticipantAuthSessionAdapter:()=>({[method]:new Proxy(()=>({}),{apply:throwing})})})],
      ["Promise als synchroner Client",()=>({bootstrap:{getClient:()=>Promise.resolve({auth:{}})},createParticipantAuthSessionAdapter:throwing})],
      ["Promise als synchroner Adapter",()=>({bootstrap:{getClient:()=>({auth:{}})},createParticipantAuthSessionAdapter:()=>Promise.resolve({})})],
    );
    for (const [name,makeDeps] of boundaryCases) {
      await test("negative",`${method} Grenze ${name}`,async()=>{
        await expectedBoundaryError(makeDeps(),method);
      });
    }
  }

  const authApi = require(authPath);
  const accessApi = require(accessPath);
  let session = null;
  const auth = {
    async getSession(){return {data:{session},error:null};},
    async signInWithPassword(credentials){
      assert(credentials.email==="synthetic@example.invalid" && credentials.password===SECRET,"Shared Credentials");
      session={user:{id:USER_ID,email:"synthetic@example.invalid"},access_token:"SYNTHETIC_ACCESS_TOKEN",refresh_token:"SYNTHETIC_REFRESH_TOKEN"};
      return {data:{session},error:null};
    },
    async signOut(){session=null;return {error:null};},
  };
  const tables = {
    participants:[{id:PARTICIPANT_ID,auth_user_id:USER_ID,status:"active"}],
    enrollments:[{id:ENROLLMENT_ID,participant_id:PARTICIPANT_ID,course_id:COURSE_ID,access_starts_at:"2026-08-01T00:00:00.000Z",access_ends_at:"2026-10-31T23:59:59.999Z",access_status:"allowed"}],
    courses:[{id:COURSE_ID,start_date:"2026-08-01",end_date:"2026-10-31",status:"active"}],
  };
  const client = {auth,from(table){return {select(){return {async eq(column,value){return {data:tables[table].filter(row=>row[column]===value),error:null};}};}};}};
  const sharedBridge = createBridge({bootstrap:{getClient:()=>client},createParticipantAuthSessionAdapter:authApi.createParticipantAuthSessionAdapter});
  const access = accessApi.createParticipantAccessAdapter({client,utcNow:()=>"2026-09-02T12:00:00.000Z"});
  await test("positive","Shared Fake signIn zu bestehendem access_allowed",async()=>{
    validate(await sharedBridge.resolveSession(),false,"session_missing");
    const before = await access.resolveAccess();
    assert(before.allowed===false && before.code==="session_missing","Shared vor Login");
    validate(await sharedBridge.signIn({email:"synthetic@example.invalid",password:SECRET}),true,"signed_in");
    const allowed=await access.resolveAccess();
    assert(allowed.allowed===true && allowed.code==="access_allowed","Shared Zugriff");
    sharedSignIn=true;
  });
  await test("positive","Shared Fake signOut zu resolveSession session_missing",async()=>{
    validate(await sharedBridge.signOut(),true,"signed_out");
    validate(await sharedBridge.resolveSession(),false,"session_missing");
    const after=await access.resolveAccess();
    assert(after.allowed===false && after.code==="session_missing","Shared nach Logout");
    sharedSignOut=true;
  });
  console.log(JSON.stringify({positive,negative,sharedSignIn,sharedSignOut,failures}));
  if(failures.length)process.exitCode=1;
}
main().catch(()=>{console.error("Synthetischer Harness abgebrochen");process.exitCode=1;});
'''


def behavior_result(node: Path, harness: Path, source_path: Path) -> tuple[bool, dict[str, object]]:
    completed = run_node(node, [str(harness), str(source_path), str(AUTH_PATH), str(ACCESS_PATH)])
    try:
        payload = json.loads(completed.stdout.strip())
    except (ValueError, TypeError):
        return False, {}
    if not isinstance(payload, dict):
        return False, {}
    valid = (
        completed.returncode == 0
        and type(payload.get("positive")) is int and payload["positive"] > 0
        and type(payload.get("negative")) is int and payload["negative"] > 0
        and payload.get("sharedSignIn") is True
        and payload.get("sharedSignOut") is True
        and payload.get("failures") == []
    )
    return valid, payload


def run_mutation_tests(node: Path, harness: Path, source: str, temp_root: Path) -> tuple[int, int]:
    public = "return Object.freeze({ resolveSession, signIn, signOut });"
    error_result = 'return Object.freeze({ ok: false, code: "auth_error" });'
    client = "const client = getClient.call(bootstrap);"
    adapter = "const adapter = createParticipantAuthSessionAdapter({ auth });"
    method_call = "const adapterResult = await adapterMethod.apply(adapter, args);"
    invoke_head = "async function invoke(methodName, args) {"
    dependency_keys = '"bootstrap", "createParticipantAuthSessionAdapter"'
    semantic = [
        ("dritte erforderliche Dependency", [(dependency_keys, dependency_keys + ', "extra"')]),
        ("dritte Dependency akzeptieren", [('!hasExactKeys(dependencies, [\n          "bootstrap", "createParticipantAuthSessionAdapter"\n        ])', 'false')]),
        ("vierte oeffentliche Methode", [(public, "return Object.freeze({ resolveSession, signIn, signOut, debug() {} });")]),
        ("oeffentliche Zusatzproperty", [(public, "return Object.freeze({ resolveSession, signIn, signOut, debug: true });")]),
        ("oeffentliche Symbolproperty", [(public, 'return Object.freeze({ resolveSession, signIn, signOut, [Symbol("debug")]: true });')]),
        ("public freeze entfernt", [(public, "return { resolveSession, signIn, signOut };")]),
        ("getClient entfernt", [(client, "const client = {};")]),
        ("getClient doppelt", [(client, "getClient.call(bootstrap); " + client)]),
        ("Client gecacht", [(invoke_head,"let cachedClient;\n  " + invoke_head),(client,"const client = cachedClient || (cachedClient = getClient.call(bootstrap));")]),
        ("ganzer Client weitergegeben", [(adapter,"const adapter = createParticipantAuthSessionAdapter(client);")]),
        ("zusaetzliche Factorydependency", [(adapter,"const adapter = createParticipantAuthSessionAdapter({ auth, bootstrap });")]),
        ("zusaetzliches Factoryargument", [(adapter,"const adapter = createParticipantAuthSessionAdapter({ auth }, bootstrap);")]),
        ("Adapter gecacht", [(invoke_head,"let cachedAdapter;\n  " + invoke_head),(adapter,"const adapter = cachedAdapter || (cachedAdapter = createParticipantAuthSessionAdapter({ auth }));")]),
        ("falsche Adaptermethode", [("const adapterMethod = adapter[methodName];","const adapterMethod = adapter.signOut;")]),
        ("Adaptermethode doppelt", [(method_call,"await adapterMethod.apply(adapter, args); " + method_call)]),
        ("Credentials kopiert", [('return invoke("signIn", [credentials]);','return invoke("signIn", [{ ...credentials }]);')]),
        ("Factory liest Dependencies sofort", [("function " + FACTORY + "(dependencies) {","function " + FACTORY + "(dependencies) {\n  void dependencies.bootstrap;")]),
        ("require Seiteneffekt", [('"use strict";', '"use strict";\nconsole.log("UNEXPECTED_REQUIRE_EFFECT");')]),
        ("gueltiges Result rewrapped", [("return adapterResult;","return Object.freeze({ ok: adapterResult.ok, code: adapterResult.code });")]),
        ("ungueltiges Result akzeptiert", [("if (!isValidAdapterResult(adapterResult, methodName)) {","if (false) {")]),
        ("Fehler freeze entfernt", [(error_result,'return { ok: false, code: "auth_error" };')]),
        ("Fehler Zusatzproperty", [(error_result,'return Object.freeze({ ok: false, code: "auth_error", detail: null });')]),
        ("Error-Message geleakt", [('} catch (_error) {\n      return authError();','} catch (_error) {\n      return Object.freeze({ ok: false, code: _error.message });')]),
        ("Result freeze Pruefung entfernt", [("!Object.isFrozen(value)","false")]),
        ("auth doppelt gelesen", [("const auth = client.auth;","const auth = (client.auth, client.auth);")]),
        ("getClient Getter doppelt gelesen", [("const getClient = bootstrap.getClient;","const getClient = (bootstrap.getClient, bootstrap.getClient);")]),
    ]
    forbidden = [
        ("initializeClient", "initializeClient();"), ("createClient", "createClient();"),
        ("getState", "getState();"), ("window", "void window;"),
        ("document", "void document;"), ("self", "void self;"),
        ("globalThis", "void globalThis;"), ("localStorage", "void localStorage;"),
        ("sessionStorage", "void sessionStorage;"), ("IndexedDB", "void indexedDB;"),
        ("caches", "void caches;"), ("CacheStorage", "void CacheStorage;"),
        ("Cookies", "void cookie;"), ("fetch", 'fetch("/");'),
        ("XMLHttpRequest", "new XMLHttpRequest();"),
        ("WebSocket", 'new WebSocket("synthetic");'), ("EventSource", 'new EventSource("synthetic");'),
        ("sendBeacon", "sendBeacon();"), ("Tabellenzugriff", 'client.from("synthetic");'),
        ("participants", "void participants;"), ("enrollments", "void enrollments;"),
        ("courses", "void courses;"), ("SQL", 'const SQL = "synthetic";'),
    ]
    passed = 0
    behavior_blocked = 0
    all_mutations = [(name, edits, True) for name, edits in semantic]
    for name, statement in forbidden:
        # Syntaxgueltige, inaktive Probe: der Scanner muss die verbotene Logik
        # unabhaengig von einer zufaelligen Laufzeitexception entdecken.
        all_mutations.append((name, [('"use strict";', '"use strict";\nif (false) { ' + statement + ' }')], False))
    for index, (label, edits, requires_behavior) in enumerate(all_mutations, 1):
        mutated = source
        for needle, replacement in edits:
            if mutated.count(needle) != 1:
                stop(f"Manipulation M{index:02d} ohne eindeutiges Ziel: {label}")
            mutated = mutated.replace(needle, replacement, 1)
        if mutated == source:
            stop(f"Manipulation M{index:02d} wirkungslos: {label}")
        mutation_path = temp_root / f"mutation-{index:02d}.js"
        mutation_path.write_text(mutated, encoding="utf-8", newline="\n")
        reread = mutation_path.read_text(encoding="utf-8")
        if reread != mutated:
            stop(f"Manipulation M{index:02d} nicht exakt materialisiert")
        if run_node(node, ["--check", str(mutation_path)]).returncode != 0:
            stop(f"Manipulation M{index:02d} nicht syntaxgueltig: {label}")
        if requires_behavior:
            accepted, _ = behavior_result(node, harness, mutation_path)
            if accepted:
                stop(f"Manipulation M{index:02d} im Verhalten nicht erkannt: {label}")
            behavior_blocked += 1
        elif not source_contract_errors(reread):
            stop(f"Manipulation M{index:02d} statisch nicht erkannt: {label}")
        passed += 1
    return passed, behavior_blocked


def validate_report() -> None:
    if not REPORT_PATH.is_file():
        stop("v27.37b-Vertragsdokument fehlt")
    report = REPORT_PATH.read_text(encoding="utf-8")
    for marker in (FACTORY, "resolveSession()", "signIn(credentials)", "signOut()", "Fehlergrenzen", "Tests", "v2737b-auth-bridge"):
        if marker not in report:
            stop("v27.37b-Vertragsdokument unvollstaendig: " + marker)
    if not re.search(r"Supabase\s+(?:bleibt\s+)?NICHT LIVE", report):
        stop("Nicht-Live-Grenze fehlt im Vertragsdokument")


def main() -> None:
    for path in (BRIDGE_PATH, AUTH_PATH, ACCESS_PATH):
        if not path.is_file():
            stop("erforderliches isoliertes Modul fehlt: " + path.name)
    source = BRIDGE_PATH.read_text(encoding="utf-8")
    errors = source_contract_errors(source)
    if errors:
        stop("; ".join(errors))
    validate_report()
    node = find_node()
    checker_temp_root = get_checker_temp_root()
    try:
        with tempfile.TemporaryDirectory(prefix="checks-", dir=checker_temp_root) as temp_dir:
            temp_root = Path(temp_dir)
            harness = temp_root / "harness.js"
            harness.write_text(HARNESS, encoding="utf-8", newline="\n")
            for path in (BRIDGE_PATH, harness):
                if run_node(node, ["--check", str(path)]).returncode != 0:
                    stop("JavaScript-Syntax ungueltig: " + path.name)
            accepted, behavior = behavior_result(node, harness, BRIDGE_PATH)
            if not accepted:
                names = behavior.get("failures", [])
                details = ", ".join(names[:12]) if isinstance(names, list) else ""
                stop("JavaScript-Verhaltenspruefung fehlgeschlagen" + (": " + details if details else ""))
            count, behavior_count = run_mutation_tests(node, harness, source, temp_root)
    except OSError:
        stop("UMGEBUNGSBLOCKER: vorgeschriebener Git-Tempbereich nicht beschreibbar oder nicht aufraeumbar")
    print("Teilnehmer-Auth-/Session-Bootstrap-Bruecke v27.37b: PASS")
    print(f"Positivpruefungen: {behavior['positive']} PASS")
    print(f"Negativpruefungen: {behavior['negative']} PASS")
    print(f"Manipulationspruefungen: {count} PASS")
    print(f"Semantische Manipulationen dynamisch abgelehnt: {behavior_count} PASS")
    print("Shared-Fake signIn -> access_allowed: PASS")
    print("Shared-Fake signOut -> session_missing: PASS")
    print("Exakt zwei Dependencies, drei frozen Methoden, keine Side Effects: PASS")
    print("getClient einmal, nur auth, frischer Adapter, unveraenderte Credentials: PASS")
    print("Gueltige Ergebnisse identisch; Fehler exakt frozen {ok:false,code:auth_error}: PASS")
    print("Getter-/Proxy-/Throw-/Reject-, Isolations- und Datenminimierungsgrenzen: PASS")
    print("Supabase NICHT LIVE")


if __name__ == "__main__":
    main()
