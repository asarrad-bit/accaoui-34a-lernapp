#!/usr/bin/env python3
"""Local synthetic v27.37f app-start contract and mutation checks."""
import json
from pathlib import Path
import re
import runpy
import shutil
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[1]

HARNESS = r'''
"use strict";
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");
const root = process.argv[1];
const source = fs.readFileSync(0, "utf8");
const A = "accaoui-participant-auth-session-browser-loader";
const Z = "accaoui-participant-access-browser-loader";
const AR = "ACCAOUI_PARTICIPANT_AUTH_SESSION_BROWSER_LOADER_READY";
const ZR = "ACCAOUI_PARTICIPANT_ACCESS_BROWSER_LOADER_READY";
const AP = "ACCAOUI_PARTICIPANT_AUTH_SESSION_APP_PROVIDER";
const ZP = "ACCAOUI_PARTICIPANT_ACCESS_APP_PROVIDER";
const READY = 'Object.freeze({requested:true,ready:true,status:"ready"})';
const SESSION = 'Object.freeze({ok:true,code:"session_available"})';
const PRIVATE = "PRIVATE_AUTH_DIAGNOSTIC";
const own = (o, key) => Object.prototype.hasOwnProperty.call(o, key);
async function flush() { for (let i=0;i<25;i++) await Promise.resolve(); }
function fixture(options = {}) {
  const stats = {starts:0, notices:[], sessionCalls:0, accessCalls:0, accessOps:0,
    config:0, configLogs:0, healthLogs:0, reads:{}, events:[], forbidden:[],
    getSession:0, getClient:0, queries:[], logs:[], contexts:[]};
  const settings = {...options};
  const callbacks = [];
  const win = {};
  const document = {
    addEventListener(type, callback) { if (type === "DOMContentLoaded") callbacks.push(callback); },
    getElementById(id) {
      if (settings.lookupThrows) throw Error(PRIVATE);
      if (id !== A && id !== Z) return null;
      if ((id === A && settings.missingA) || (id === Z && settings.missingZ)) return null;
      return {getAttribute(name) {
        stats.reads[id] = (stats.reads[id] || 0) + 1;
        if (settings.attributeThrows === id) throw Error(PRIVATE);
        return name === "data-enabled" ? (id === A ? settings.a : settings.z) : null;
      }};
    }
  };
  if (settings.noLookup) delete document.getElementById;
  if (settings.lookupGetterThrows) Object.defineProperty(document, "getElementById", {
    get() { throw Error(PRIVATE); }
  });
  const context = vm.createContext({
    window:win, self:win, document,
    localStorage:{getItem(){return settings.guard || "";},setItem(){},removeItem(){}},
    console:Object.fromEntries(["log","info","warn","error"].map(name =>
      [name,(...args)=>stats.logs.push(args.map(String).join(" "))])),
    setTimeout,clearTimeout,setInterval,clearInterval,
    __forbidden(name) { stats.forbidden.push(name); throw Error(PRIVATE); },
    __sessionCalled(receiver, args) {
      stats.sessionCalls++; stats.events.push("session");
      assert.equal(receiver, win[AP]); assert.equal(args.length,0);
      if (settings.sessionThrows) throw Error(PRIVATE);
    },
    __accessCalled() {stats.accessOps++;},
    __realSession() {
      stats.getSession++;
      stats.events.push("getSession");
      const missing = settings.loseSession && stats.getSession >= 2;
      return evaluate(missing ? "null" : '({user:{id:"11111111-1111-4111-8111-111111111111"}})');
    },
    __clientRead() {stats.getClient++;},
    __query(table, column, value) {stats.queries.push([table,column,value]);},
    fetch(){stats.forbidden.push("fetch"); throw Error(PRIVATE);},
    XMLHttpRequest(){stats.forbidden.push("XHR"); throw Error(PRIVATE);}
  });
  const evaluate = expression => vm.runInContext(expression, context);
  function boundary(name, expression, kind) {
    if (kind === "absent") return;
    const value = kind === "undefined" ? undefined : evaluate(expression);
    if (kind === "inherited") {
      Object.setPrototypeOf(win, Object.assign(Object.create(Object.getPrototypeOf(win)),{[name]:value}));
    } else if (kind === "getter") {
      Object.defineProperty(win,name,{get(){throw Error(PRIVATE);},enumerable:true});
    } else {
      Object.defineProperty(win,name,{value,enumerable:true,
        writable:kind === "mutable",configurable:kind === "mutable"});
    }
  }
  const pending = name => 'Object.freeze(new Promise(resolve => {globalThis.'+name+' = resolve;}))';
  boundary(AR, settings.pendingA ? pending("__finishA") :
    (settings.authPromise || 'Object.freeze(Promise.resolve('+(settings.authState || READY)+'))'),
    settings.authBoundary);
  boundary(ZR, settings.pendingZ ? pending("__finishZ") :
    (settings.accessPromise || 'Promise.resolve('+(settings.accessState || READY)+')'),
    settings.accessBoundary);
  if (!settings.real) {
    boundary(AP, settings.provider || 'Object.freeze({resolveSession(){__sessionCalled(this,arguments);return '+
      (settings.sessionResult || SESSION)+';},signIn(){__forbidden("signIn");},signOut(){__forbidden("signOut");}})',
      settings.providerBoundary);
    if (!settings.noAccessProvider) {
      boundary(ZP, settings.accessProvider || '({resolveAccess(){__accessCalled();return '+
        (settings.accessResult || '({allowed:true,code:"access_allowed"})')+';}})');
    }
  } else {
    evaluate('window.ACCAOUI_SUPABASE_BOOTSTRAP = Object.freeze({getClient(){__clientRead();return __client;},initializeClient(){__forbidden("initializeClient");}})');
    const rows = {
      participants:[{id:"22222222-2222-4222-8222-222222222222",
        auth_user_id:"11111111-1111-4111-8111-111111111111",status:settings.participantStatus || "active"}],
      enrollments:[{id:"33333333-3333-4333-8333-333333333333",
        participant_id:"22222222-2222-4222-8222-222222222222",
        course_id:"44444444-4444-4444-8444-444444444444",
        access_status:settings.enrollmentStatus || "allowed",access_starts_at:null,access_ends_at:null}],
      courses:[{id:"44444444-4444-4444-8444-444444444444",
        status:settings.courseStatus || "active",start_date:null,end_date:null}]
    };
    evaluate('globalThis.__rows = '+JSON.stringify(rows)+'; globalThis.__client = {'+
      'auth:{getSession(){return Promise.resolve({error:null,data:{session:__realSession()}});},'+
      'signInWithPassword(){__forbidden("signInWithPassword");},signOut(){__forbidden("signOut");}},'+
      'from(table){return {select(){return {eq(column,value){__query(table,column,value);'+
      'return Promise.resolve({error:null,data:__rows[table]});}};}};}}');
    for (const file of [
      "data/supabase-participant-auth-session-adapter.js",
      "data/supabase-participant-auth-session-bootstrap-bridge.js",
      "data/supabase-participant-auth-session-browser-provider.js",
      "data/supabase-participant-access-adapter.js",
      "data/supabase-participant-access-bootstrap-bridge.js",
      "data/supabase-participant-access-browser-provider.js"
    ]) vm.runInContext(fs.readFileSync(path.join(root,file),"utf8"),context,{filename:file});
    assert.equal(stats.getSession,0); assert.equal(stats.getClient,0);
  }
  const originalGlobals = Object.getOwnPropertyDescriptors(win);
  vm.runInContext(source + '\n;globalThis.__entry = {boot:initAppBoot,flow:initAuthFlow,'+
    'hooks(start,notice,config,health,configLog,healthLog,access){'+
    'startLocalApp=start;renderLoginOrAccessNotice=notice;loadOptionalSupabaseConfig=config;'+
    'getSupabaseAdapterHealthState=health;logSupabaseConfigState=configLog;'+
    'logSupabaseAdapterHealthState=healthLog;'+
    'const original=resolveParticipantAccessAppProviderV2736D;'+
    'resolveParticipantAccessAppProviderV2736D=()=>{access();return original();};}};',context);
  context.__entry.hooks(
    ()=>{stats.starts++;stats.events.push("start");},
    notice=>{stats.notices.push(notice.status);stats.events.push("notice:"+notice.status);
      if(settings.renderThrows) throw Error(PRIVATE);},
    async()=>{stats.config++;stats.events.push("config");
      if(settings.configRejects) throw Error(PRIVATE);return {status:"local_test"};},
    ()=>({isLocalAccessAllowed:!settings.healthBlocked,status:"local_test"}),
    ()=>{stats.configLogs++;},()=>{stats.healthLogs++;},
    ()=>{stats.accessCalls++;stats.events.push("access");}
  );
  function verifySafe() {
    assert.deepEqual(stats.forbidden,[]);
    assert(!stats.logs.some(text=>text.includes(PRIVATE)));
    for(const [name,descriptor] of Object.entries(originalGlobals)) {
      assert.deepEqual(Object.getOwnPropertyDescriptor(win,name),descriptor,"global overwritten: "+name);
    }
  }
  return {stats,settings,context,win,evaluate,verifySafe,
    boot:()=>context.__entry.boot(),flow:()=>context.__entry.flow(),
    dom:()=>{for(const callback of callbacks) callback();},
    readyA:expression=>context.__finishA(evaluate(expression || READY)),
    readyZ:expression=>context.__finishZ(evaluate(expression || READY))};
}
function allowed(f) {assert.equal(f.stats.starts,1);assert.deepEqual(f.stats.notices,[]);f.verifySafe();}
function denied(f,status="access_error") {assert.equal(f.stats.starts,0);assert.deepEqual(f.stats.notices,[status]);f.verifySafe();}
async function main() {
  let positive=0,negative=0;
  for(const a of ["false","true"]) for(const z of ["false","true"]) {
    const f=fixture({a,z});f.dom();await f.boot();allowed(f);
    assert.equal(f.stats.sessionCalls,a==="true"?1:0);
    assert.equal(f.stats.accessCalls,1);assert.equal(f.stats.accessOps,1);
    assert.equal(f.stats.config,a==="true"?0:1);
    assert.equal(f.stats.configLogs,a==="true"?0:1);
    assert.equal(f.stats.healthLogs,a==="true"?0:1);
    if(a==="true") assert.deepEqual(f.stats.events,["session","access","start"]);
    positive++;
  }
  for(const a of [undefined,null,"","TRUE","True"," true","true ","1",true,1,false]) {
    const f=fixture({a,noAccessProvider:true,providerBoundary:"getter"});
    await f.boot();allowed(f);assert.equal(f.stats.sessionCalls,0);assert.equal(f.stats.config,1);positive++;
  }
  for(const options of [{missingA:true},{noLookup:true}]) {
    const f=fixture({...options,a:"true",noAccessProvider:true});await f.flow();allowed(f);
    assert.equal(f.stats.sessionCalls,0);positive++;
  }
  for(const z of ["false","true"]) {
    const f=fixture({a:"true",z,noAccessProvider:true});await f.boot();denied(f);
    assert.equal(f.stats.sessionCalls,1);assert.equal(f.stats.accessCalls,1);negative++;
  }
  for(const guard of ["login_required","blocked","expired","no_course","access_error"]) {
    for(const mode of ["boot","flow"]) {
      const f=fixture({a:"true",z:"true",guard,pendingA:true,pendingZ:true,
        providerBoundary:"getter",attributeThrows:A});
      await f[mode]();denied(f,guard);
      assert.equal(f.stats.sessionCalls,0);assert.equal(f.stats.accessCalls,0);negative++;
    }
  }
  {
    const f=fixture({a:"true",healthBlocked:true,pendingA:true});await f.boot();
    denied(f,"local_test");assert.equal(f.stats.sessionCalls,0);negative++;
  }
  for(const options of [{lookupThrows:true},{lookupGetterThrows:true},{attributeThrows:A},{attributeThrows:Z}]) {
    const f=fixture({a:"true",...options});await f.boot();denied(f);
    assert.equal(f.stats.config,0);assert.equal(f.stats.sessionCalls,0);negative++;
  }
  for(const kind of ["absent","undefined","inherited","getter","mutable"]) {
    const f=fixture({a:"true",authBoundary:kind});await f.boot();denied(f);
    assert.equal(f.stats.sessionCalls,0);negative++;
    const p=fixture({a:"true",providerBoundary:kind});await p.boot();denied(p);
    assert.equal(p.stats.sessionCalls,0);negative++;
  }
  for(const authPromise of [
    "null","undefined","42","({})",
    '({get then(){throw Error("'+PRIVATE+'");}})',
    '({then(resolve,reject){reject(Error("'+PRIVATE+'"));}})'
  ]) {
    const f=fixture({a:"true",authPromise});await f.boot();denied(f);negative++;
  }
  for(const authState of [
    '({requested:true,ready:true,status:"ready"})',
    'Object.freeze({requested:true,ready:false,status:"error"})',
    'Object.freeze({requested:false,ready:true,status:"ready"})',
    'Object.freeze({requested:true,ready:true,status:"error"})',
    'Object.freeze({requested:true,ready:true,status:"ready",extra:true})',
    'Object.freeze(Object.create({requested:true,ready:true,status:"ready"}))',
    'Object.freeze({requested:true,ready:true,get status(){throw Error("'+PRIVATE+'");}})',
    'Object.freeze({requested:true,ready:true,status:"ready",[Symbol("extra")]:true})',
    "null","undefined","[]"
  ]) {
    const f=fixture({a:"true",authState});await f.boot();denied(f);
    assert.equal(f.stats.sessionCalls,0);negative++;
  }
  for(const provider of [
    "null","undefined","[]","Object.freeze({})",
    '({resolveSession(){return '+SESSION+';},signIn(){},signOut(){}})',
    'Object.freeze({resolveSession:1,signIn(){},signOut(){}})',
    'Object.freeze({resolveSession(){return '+SESSION+';},signIn:1,signOut(){}})',
    'Object.freeze({get resolveSession(){throw Error("'+PRIVATE+'");},signIn(){},signOut(){}})',
    'Object.freeze(Object.create({resolveSession(){return '+SESSION+';},signIn(){},signOut(){}}))'
  ]) {
    const f=fixture({a:"true",provider});await f.boot();denied(f);negative++;
  }
  for(const code of ["session_missing","session_invalid","auth_error"]) {
    const f=fixture({a:"true",sessionResult:'Object.freeze({ok:false,code:'+JSON.stringify(code)+'})'});
    await f.boot();denied(f,code==="auth_error"?"access_error":"login_required");
    assert.equal(f.stats.sessionCalls,1);assert.equal(f.stats.accessCalls,0);negative++;
  }
  for(const sessionResult of [
    "null","undefined","[]","42",'({ok:true,code:"session_available"})',
    'Object.freeze({ok:false,code:"session_available"})',
    'Object.freeze({ok:true,code:"session_missing"})',
    'Object.freeze({ok:"true",code:"session_available"})',
    'Object.freeze({ok:true,code:"unknown"})',
    'Object.freeze({ok:false,code:"unknown"})',
    'Object.freeze({ok:true,code:"session_available",extra:true})',
    'Object.freeze({ok:true,code:"session_available",[Symbol("extra")]:true})',
    'Object.freeze(Object.create({ok:true,code:"session_available"}))',
    'Object.freeze({ok:true,get code(){throw Error("'+PRIVATE+'");}})',
    'Promise.reject(Error("'+PRIVATE+'"))',
    '({then(resolve,reject){reject(Error("'+PRIVATE+'"));}})'
  ]) {
    const f=fixture({a:"true",sessionResult});await f.boot();denied(f);
    assert.equal(f.stats.accessCalls,0);negative++;
  }
  {
    const f=fixture({a:"true",sessionThrows:true});await f.boot();denied(f);
    assert.equal(f.stats.sessionCalls,1);negative++;
  }
  for(const [code,notice] of [
    ["participant_blocked","blocked"],["enrollment_blocked","blocked"],
    ["participant_expired","expired"],["course_inactive","no_course"],
    ["session_missing","login_required"],["session_invalid","login_required"],
    ["unknown","access_error"]
  ]) {
    const f=fixture({a:"true",accessResult:'({allowed:false,code:'+JSON.stringify(code)+'})'});
    await f.boot();denied(f,notice);assert.equal(f.stats.sessionCalls,1);
    assert.equal(f.stats.accessCalls,1);negative++;
  }
  for(const accessProvider of ["null","({})",'({resolveAccess(){throw Error("'+PRIVATE+'");}})',
    '({resolveAccess(){return Promise.reject(Error("'+PRIVATE+'"));}})']) {
    const f=fixture({a:"true",accessProvider});await f.boot();denied(f);negative++;
  }
  for(const accessResult of ["null",'({allowed:true,code:"wrong"})','({allowed:false,code:"access_allowed"})']) {
    const f=fixture({a:"true",accessResult});await f.boot();denied(f);negative++;
  }
  for(const options of [
    {accessBoundary:"absent"},{accessState:'Object.freeze({requested:true,ready:false,status:"error"})'},
    {accessPromise:'({then(resolve,reject){reject(Error("'+PRIVATE+'"));}})'}
  ]) {
    const f=fixture({a:"true",z:"true",...options});await f.boot();denied(f);
    assert.equal(f.stats.accessCalls,0);negative++;
  }
  {
    const f=fixture({a:"true",z:"true",pendingA:true,pendingZ:true});
    f.dom();const runs=[f.boot(),f.boot(),f.flow(),f.flow()];await flush();
    assert.equal(f.stats.sessionCalls,0);assert.equal(f.stats.accessCalls,0);assert.equal(f.stats.starts,0);
    f.settings.a="false";f.settings.z="false";
    f.readyA();await flush();
    assert.equal(f.stats.sessionCalls,1);assert.equal(f.stats.accessCalls,0);
    f.readyZ();await Promise.all(runs);allowed(f);
    assert.equal(f.stats.accessCalls,1);assert.equal(f.stats.accessOps,1);
    assert.equal(f.stats.config,0);
    assert.equal(f.stats.reads[A],1);assert.equal(f.stats.reads[Z],1);
    f.dom();await Promise.all([f.boot(),f.flow()]);allowed(f);
    assert.equal(f.stats.sessionCalls,1);assert.equal(f.stats.accessCalls,1);positive++;
  }
  for(const result of ['Object.freeze({ok:false,code:"auth_error"})',SESSION]) {
    const f=fixture({a:"true",sessionResult:
      'new Promise(resolve=>{globalThis.__finishSession=resolve;})'});
    const runs=[f.flow(),f.boot(),f.flow()];await flush();
    assert.equal(f.stats.sessionCalls,1);assert.equal(f.stats.accessCalls,0);
    f.context.__finishSession(f.evaluate(result));await Promise.all(runs);
    if(result===SESSION) allowed(f);else denied(f);
    await Promise.all([f.flow(),f.boot()]);assert.equal(f.stats.sessionCalls,1);positive++;
  }
  {
    const f=fixture({a:"true",pendingA:true});const run=f.boot();await flush();
    f.readyA('Object.freeze({requested:true,ready:false,status:"error"})');await run;denied(f);
    f.readyA();await Promise.all([f.boot(),f.flow()]);denied(f);
    assert.equal(f.stats.sessionCalls,0);negative++;
  }
  {
    const f=fixture({a:"false",noAccessProvider:true});
    f.dom();await Promise.all([f.boot(),f.boot()]);allowed(f);
    assert.equal(f.stats.config,1);assert.equal(f.stats.accessCalls,1);positive++;
  }
  {
    const f=fixture({a:"true",accessResult:
      'new Promise(resolve=>{globalThis.__finishAccess=resolve;})'});
    const runs=[f.boot(),f.flow(),f.flow()];await flush();
    assert.equal(f.stats.accessOps,1);assert.equal(f.stats.starts,0);
    f.context.__finishAccess(f.evaluate('({allowed:true,code:"access_allowed"})'));
    await Promise.all(runs);allowed(f);assert.equal(f.stats.sessionCalls,1);
    assert.equal(f.stats.accessCalls,1);positive++;
  }
  for(const options of [{sessionThrows:true},{sessionThrows:true,renderThrows:true}]) {
    const f=fixture({a:"true",...options});await Promise.all([f.boot(),f.flow(),f.flow()]);
    denied(f);assert.equal(f.stats.sessionCalls,1);negative++;
  }
  for(const options of [
    {},{participantStatus:"blocked"},{enrollmentStatus:"blocked"},
    {courseStatus:"inactive"},{loseSession:true}
  ]) {
    const f=fixture({a:"true",z:"true",real:true,...options});await f.boot();
    if(!Object.keys(options).length) allowed(f);
    else denied(f,options.loseSession?"login_required":options.courseStatus?"no_course":"blocked");
    assert.equal(f.stats.getSession,2);assert.equal(f.stats.getClient,2);
    assert.equal(f.stats.accessCalls,1);assert.equal(f.stats.config,0);
    if(options.loseSession) assert.equal(f.stats.queries.length,0);
    else assert.deepEqual(f.stats.queries[0],["participants","auth_user_id","11111111-1111-4111-8111-111111111111"]);
    positive++;
  }
  console.log(JSON.stringify({positive,negative}));
}
main().catch(error=>{console.error(error.stack || String(error));process.exitCode=1;});

'''

def require(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    try:
        control = runpy.run_path(str(ROOT / "tools/check-project-continuity-control.py"))
        phase = control["detect_v2737f_phase"]()
        require(phase in {
            "v2737f_implementation_prepared", "v2737f_implementation_committed",
            "v2737f_closure_prepared", "v2737f_closure_committed",
        }, "Kein autorisierter Implementierungs-/Abschlusszustand")
        source = (ROOT / "app.js").read_text(encoding="utf-8")
        document = (ROOT / "docs/PARTICIPANT_AUTH_SESSION_APP_ENTRY_V2737F.md").read_text(
            encoding="utf-8")
        require(source.endswith("\n") and not source.startswith("\ufeff"),
                "App benötigt UTF-8 ohne BOM und abschließenden Zeilenumbruch")
        for marker in (
            "# v27.37f", 'data-enabled="true"', 'data-enabled="false"',
            "Auth-Readiness", "resolveSession()", "Teilnehmerzugangsprüfung",
            "A=false, Z=false", "A=false, Z=true", "A=true, Z=false", "A=true, Z=true",
            "Supabase bleibt NICHT LIVE.", "v2737f_implementation_prepared",
            "Keine Client-Erzeugung", "Keine SDK-/Config-Nachladung",
        ):
            require(marker in document, "Dokumentationsvertrag fehlt: " + marker)
        # The shared continuity validator also freezes everything outside these
        # two functions and the single, explicitly authorized helper block.
        helper = source.split("// BEGIN v27.37f auth/session app entry\n", 1)[1].split(
            "// END v27.37f auth/session app entry\n", 1)[0]
        flow = source.split("async function initAuthFlow() {", 1)[1].split(
            "\nfunction isParticipantAccessBrowserLoaderRequestedV2736F()", 1)[0]
        for pattern in (
            r"\b(?:fetch|XMLHttpRequest|WebSocket|eval|importScripts)\s*\(",
            r"\b(?:initializeClient|createClient|getClient|getSession|signInWithPassword)\s*\(",
            r"\.(?:signIn|signOut|from)\s*\(", r"\bconsole\s*\.",
            r"\b(?:localStorage|sessionStorage|indexedDB)\b",
            r"\b(?:import|require)\s*\(",
        ):
            require(re.search(pattern, helper + flow) is None,
                    "Unerlaubte Operation im neuen Auth-Pfad: " + pattern)
        node = shutil.which("node")
        require(node is not None, "Node.js fehlt")

        def execute(text):
            return subprocess.run(
                [node, "-e", HARNESS, str(ROOT)], input=text, cwd=ROOT,
                capture_output=True, text=True, encoding="utf-8", errors="strict",
                timeout=60, check=False,
            )

        result = execute(source)
        require(result.returncode == 0, "App-Einstiegsharness fehlgeschlagen:\n" + result.stderr)
        summary = json.loads(result.stdout)
        require(summary["positive"] >= 25 and summary["negative"] >= 80,
                "Unvollständige Positiv-/Negativmatrix")
        print("v27.37f App-Einstieg:", result.stdout.strip(), "/ PASS")
        mutations = (
            ('authElement.getAttribute("data-enabled") === "true"',
             'authElement.getAttribute("data-enabled") !== null'),
            ('const state = await readiness;',
             'const state = Object.freeze({requested:true,ready:true,status:"ready"});'),
            ('const result = await provider.resolveSession.call(provider);',
             'const result = Object.freeze({ok:true,code:"session_available"});'),
            ('if (result.ok === true && result.code === "session_available")',
             'if (result.ok === true || result.code === "session_available")'),
            ('if (loaderRequested || authRequested)', 'if (loaderRequested)'),
            ('const providerAccessState = await resolveParticipantAccessAppProviderV2736D();',
             'const providerAccessState = {isAllowed:true};'),
            ('if (participantAuthFlowPromiseV2737F !== null)', 'if (false)'),
            ('if (participantAppBootPromiseV2737F !== null)', 'if (false)'),
            ('activation.authRequested || activation.failed ||',
             'false || activation.failed ||'),
            ('if (!accessState.isAllowed)', 'if (false)'),
        )
        for before, after in mutations:
            require(source.count(before) == 1, "Mutationsanker uneindeutig: " + before)
            mutated = source.replace(before, after, 1)
            syntax = subprocess.run(
                [node, "--check"], input=mutated, cwd=ROOT,
                capture_output=True, text=True, encoding="utf-8", errors="strict",
                timeout=30, check=False,
            )
            require(syntax.returncode == 0, "Mutation ist kein gültiges JavaScript: " + before)
            changed = execute(mutated)
            require(changed.returncode != 0, "Semantische Manipulation nicht erkannt: " + before)
        print(f"v27.37f semantische Manipulationen: {len(mutations)} / vollständig blockiert")
        print("v27.37f Lifecycle-Phase:", phase)
        print("PASS: Reihenfolge, paralleler Start, fail-closed, echte lokale Testketten.")
        print("Supabase NICHT LIVE; keine echten Daten; keine Git-Mutation.")
        return 0
    except (ValueError, OSError, subprocess.SubprocessError) as exc:
        print("STOPP: v27.37f App-Einstiegschecker: " + str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
