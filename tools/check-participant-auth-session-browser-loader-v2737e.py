#!/usr/bin/env python3
"""Local v27.37e loader contract; synthetic DOM/VM, no browser or live service."""

from pathlib import Path
import re
import runpy
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
LOADER = ROOT / "data/supabase-participant-auth-session-browser-loader.js"
DOCUMENT = ROOT / "docs/PARTICIPANT_AUTH_SESSION_BROWSER_LOADER_V2737E.md"
HARNESS = r'''
"use strict";
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");
const rootPath = process.argv[1];
const loaderSource = fs.readFileSync(0, "utf8");
const loaderId = "accaoui-participant-auth-session-browser-loader";
const readyName = "ACCAOUI_PARTICIPANT_AUTH_SESSION_BROWSER_LOADER_READY";
const names = [
  "ACCAOUI_PARTICIPANT_AUTH_SESSION_ADAPTER_FACTORY",
  "ACCAOUI_PARTICIPANT_AUTH_SESSION_BOOTSTRAP_BRIDGE_FACTORY",
  "ACCAOUI_PARTICIPANT_AUTH_SESSION_APP_PROVIDER"
];
const files = [
  "data/supabase-participant-auth-session-adapter.js",
  "data/supabase-participant-auth-session-bootstrap-bridge.js",
  "data/supabase-participant-auth-session-browser-provider.js"
];
const modules = files.map(file => fs.readFileSync(path.join(rootPath, file), "utf8"));
const privateError = () => { throw new Error("SYNTHETIC_PRIVATE_DETAIL"); };
let positive = 0;
let negative = 0;
async function flush() {
  for (let n = 0; n < 6; n += 1) await Promise.resolve();
}

function environment(options = {}) {
  const prototype = {};
  const target = Object.create(prototype);
  const requested = [];
  const timers = new Map();
  const created = [];
  let timerId = 0;
  let sensitiveReads = 0;
  let calls = 0;
  let insertCount = 0;
  const page = options.page || "https://local.test/accaoui/v4-dashboard/index.html";
  target.setTimeout = (fn, delay) => {
    if (options.timerThrow) privateError();
    assert.equal(delay, 15000, "bounded stage timeout");
    const id = ++timerId;
    timers.set(id, fn);
    return id;
  };
  target.clearTimeout = id => {
    if (options.clearTimerThrow) privateError();
    timers.delete(id);
  };
  for (const name of [
    "ACCAOUI_SUPABASE_BOOTSTRAP", "ACCAOUI_SUPABASE_CONFIG", "supabase",
    "localStorage", "sessionStorage", "fetch", "XMLHttpRequest", "WebSocket"
  ]) {
    Object.defineProperty(target, name, {
      configurable: true,
      get() { sensitiveReads += 1; return privateError(); }
    });
  }
  const browserRoot = options.proxy ? new Proxy(target, options.proxy) : target;
  const parent = {
    insertBefore(script, anchor) {
      if (options.insertThrow === insertCount++) privateError();
      assert.equal(anchor, element);
      assert.equal(script.async, false, "classic sequential script");
      assert.equal(script.src, new URL(files[requested.length], page).href,
        "only the next fixed local URL may be requested");
      requested.push(script);
      script.parentNode = parent;
      return script;
    },
    removeChild(script) {
      if (options.removeThrow) privateError();
      script.parentNode = null;
      return script;
    }
  };
  const element = {
    tagName: options.tagName || "SCRIPT",
    parentNode: options.parentMissing ? null : parent,
    getAttribute(name) {
      assert.equal(name, "data-enabled");
      if (options.attributeThrow) privateError();
      return Object.hasOwn(options, "enabled") ? options.enabled : "true";
    }
  };
  const documentRef = {
    URL: page,
    currentScript: options.otherScript ? {} : element,
    getElementById(id) {
      assert.equal(id, loaderId);
      if (options.lookupThrow) privateError();
      return options.elementMissing ? null : element;
    },
    createElement(tag) {
      if (options.createThrow) privateError();
      assert.equal(tag, "script", "no iframe, SDK or other DOM resources");
      let source = "";
      const script = {
        parentNode: null,
        get src() { return source; },
        set src(value) {
          if (options.srcThrow) privateError();
          source = options.rewriteSrc ? "https://external.test/evil.js"
            : new URL(value, options.foreignBase || page).href;
        }
      };
      if (options.handlerThrow) {
        Object.defineProperty(script, "onload", {set: privateError});
      }
      created.push(script);
      return script;
    }
  };
  Object.defineProperty(documentRef, "baseURI", {get: privateError});
  if (options.urlThrow) Object.defineProperty(documentRef, "URL", {get: privateError});
  if (options.currentScriptThrow) {
    Object.defineProperty(documentRef, "currentScript", {get: privateError});
  }
  if (options.insertMissing) parent.insertBefore = null;
  const context = vm.createContext({
    window: browserRoot, document: documentRef, URL,
    console: new Proxy({}, {get: () => privateError}),
    fetch: privateError, XMLHttpRequest: privateError,
    __countCall: () => { calls += 1; return privateError(); }
  });
  function run() {
    vm.runInContext(loaderSource, context, {timeout: 1000, filename: "v2737e-loader.js"});
  }
  function define(index, expression, descriptor = {}) {
    const value = vm.runInContext(expression, context);
    Object.defineProperty(target, names[index], {
      value, enumerable: true, configurable: false, writable: false, ...descriptor
    });
  }
  async function complete(index, mode = "real", beforeEvent = () => {}) {
    assert.equal(requested.length, index + 1, "no next stage before load event");
    const script = requested[index];
    const event = script.onload;
    if (mode === "real") {
      documentRef.currentScript = script;
      vm.runInContext(modules[index], context, {timeout: 1000, filename: files[index]});
      documentRef.currentScript = element;
    } else if (typeof mode === "function") {
      mode();
    }
    beforeEvent();
    event();
    await flush();
  }
  async function completePrefix(count) {
    for (let index = 0; index < count; index += 1) await complete(index);
  }
  function passive() {
    assert.equal(sensitiveReads, 0, "bootstrap/config/client/storage/network read on load");
    assert.equal(calls, 0, "factory or provider method invoked on load");
  }
  async function state(expected) {
    const descriptor = Object.getOwnPropertyDescriptor(target, readyName);
    assert.ok(descriptor && Object.hasOwn(descriptor, "value"));
    assert.equal(descriptor.writable, false);
    assert.equal(descriptor.configurable, false);
    assert.equal(descriptor.enumerable, true);
    assert.ok(Object.isFrozen(descriptor.value), "readiness promise frozen");
    let value;
    let settled = false;
    descriptor.value.then(result => { value = result; settled = true; });
    await flush();
    assert.equal(settled, true, "readiness must settle deterministically");
    assert.equal(Object.getPrototypeOf(value), vm.runInContext("Object.prototype", context));
    assert.ok(Object.isFrozen(value), "terminal state frozen");
    assert.deepEqual(Reflect.ownKeys(value).sort(), ["ready", "requested", "status"]);
    assert.equal(value.requested, true);
    assert.equal(value.ready, expected === "ready");
    assert.equal(value.status, expected);
    assert.ok(!JSON.stringify(value).includes("SYNTHETIC_PRIVATE_DETAIL"));
    passive();
    return value;
  }
  function idle() {
    assert.equal(requested.length, 0);
    assert.equal(created.length, 0);
    assert.equal(timers.size, 0);
    assert.equal(Object.hasOwn(target, readyName), false);
    passive();
  }
  return {
    target, prototype, root: browserRoot, element, documentRef, context,
    requested, created, timers, run, define, complete, completePrefix, state, idle, passive
  };
}

async function main() {
  for (const enabled of [
    undefined, null, false, true, 0, 1, "", "false", "TRUE", "True",
    " true", "true ", "1", "\ntrue", "true\n", ["true"], new String("true")
  ]) {
    const h = environment({enabled});
    const before = Reflect.ownKeys(h.target);
    h.run();
    h.idle();
    assert.deepEqual(Reflect.ownKeys(h.target), before);
    negative += 1;
  }
  for (const options of [
    {elementMissing: true}, {lookupThrow: true}, {attributeThrow: true},
    {otherScript: true}, {currentScriptThrow: true}, {tagName: "DIV"}
  ]) {
    const h = environment(options);
    h.run();
    h.idle();
    negative += 1;
  }
  for (const globals of [{}, {window: {}}, {document: {}}]) {
    vm.runInNewContext(loaderSource, globals, {timeout: 1000});
    positive += 1;
  }
  for (const options of [
    {}, {foreignBase: "https://external.test/"},
    {page: "http://localhost:8080/nested/app/?query=yes#fragment"}
  ]) {
    const h = environment(options);
    h.run();
    const readiness = h.target[readyName];
    let settled = false;
    readiness.then(() => { settled = true; });
    await flush();
    assert.equal(settled, false);
    assert.equal(h.requested.length, 1);
    h.run();
    assert.equal(h.target[readyName], readiness);
    assert.equal(h.requested.length, 1);
    await h.complete(0);
    assert.equal(settled, false);
    h.run();
    assert.equal(h.requested.length, 2);
    await h.complete(1);
    assert.equal(settled, false);
    await h.complete(2);
    const result = await h.state("ready");
    h.run();
    assert.equal(h.target[readyName], readiness);
    assert.equal(await h.target[readyName], result);
    assert.equal(h.requested.length, 3);
    assert.equal(h.timers.size, 0);
    for (const script of h.requested) {
      assert.equal(script.onload, null);
      assert.equal(script.onerror, null);
    }
    assert.deepEqual(Object.keys(h.target[names[2]]).sort(),
      ["resolveSession", "signIn", "signOut"]);
    positive += 1;
  }
  {
    const h = environment();
    h.run();
    await h.complete(0, () => h.define(0, "() => __countCall()"));
    await h.complete(1, () => h.define(1, "() => __countCall()"));
    await h.complete(2, () => h.define(2,
      "Object.freeze({resolveSession(){__countCall()},signIn(){__countCall()},signOut(){__countCall()}})"));
    await h.state("ready");
    positive += 1;
  }
  for (const name of [readyName, ...names]) {
    for (const inherited of [false, true]) {
      for (const kind of ["undefined", "value", "getter"]) {
        const h = environment();
        const owner = inherited ? h.prototype : h.target;
        let reads = 0;
        const descriptor = kind === "getter"
          ? {get() { reads += 1; return privateError(); }, configurable: true}
          : {value: kind === "undefined" ? undefined : Object.freeze({occupied: true}),
             configurable: true, writable: true};
        Object.defineProperty(owner, name, descriptor);
        const before = Object.getOwnPropertyDescriptor(owner, name);
        h.run();
        assert.equal(h.requested.length, 0, "occupied boundary must block all resource requests");
        assert.deepEqual(Object.getOwnPropertyDescriptor(owner, name), before);
        assert.equal(reads, 0, "occupied getter must not execute");
        if (name === readyName) {
          assert.equal(Object.hasOwn(h.target, name), !inherited);
          h.passive();
        } else {
          await h.state("error");
          assert.equal(Object.hasOwn(h.target, name), !inherited);
        }
        negative += 1;
      }
    }
  }
  {
    const h = environment();
    Object.preventExtensions(h.target);
    h.run();
    h.idle();
    negative += 1;
  }
  for (const index of [1, 2]) {
    for (const inherited of [false, true]) {
      for (const value of [undefined, "occupied"]) {
        const h = environment();
        h.run();
        await h.completePrefix(index - 1);
        await h.complete(index - 1, "real", () => {
          Object.defineProperty(inherited ? h.prototype : h.target, names[index], {
            value, configurable: true, writable: true
          });
        });
        await h.state("error");
        assert.equal(h.requested.length, index);
        assert.equal(Object.getOwnPropertyDescriptor(
          inherited ? h.prototype : h.target, names[index]).value, value);
        assert.equal(Object.hasOwn(h.target, names[index]), !inherited);
        negative += 1;
      }
    }
  }
  for (let index = 0; index < 3; index += 1) {
    for (const failure of ["missing", "network", "timeout", "wrong", "getter", "mutable"]) {
      const h = environment();
      h.run();
      await h.completePrefix(index);
      const script = h.requested[index];
      const lateLoad = script.onload;
      const lateError = script.onerror;
      if (failure === "network") {
        script.onerror({message: "SYNTHETIC_PRIVATE_DETAIL"});
      } else if (failure === "timeout") {
        assert.equal(h.timers.size, 1);
        [...h.timers.values()][0]();
      } else if (failure === "missing") {
        await h.complete(index, "skip");
      } else if (failure === "wrong") {
        await h.complete(index, () => h.define(index, "undefined"));
      } else if (failure === "getter") {
        await h.complete(index, () => Object.defineProperty(h.target, names[index], {
          get: privateError, enumerable: true, configurable: false
        }));
      } else {
        await h.complete(index, () => h.define(index, index < 2 ? "() => {}"
          : "Object.freeze({resolveSession(){},signIn(){},signOut(){}})",
          {writable: true, configurable: true}));
      }
      await flush();
      const error = await h.state("error");
      assert.equal(h.requested.length, index + 1);
      lateLoad();
      lateError({message: "SYNTHETIC_PRIVATE_DETAIL"});
      h.run();
      await flush();
      assert.equal(await h.target[readyName], error, "late callback cannot reopen terminal error");
      assert.equal(h.requested.length, index + 1);
      assert.equal(h.timers.size, 0);
      negative += 1;
    }
  }
  for (const expression of [
    "null", "Object.freeze([])", "Object.freeze({})",
    "({resolveSession(){},signIn(){},signOut(){}})",
    "Object.freeze({resolveSession(){},signIn(){},signOut: 1})",
    "Object.freeze({resolveSession(){},signIn(){},signOut(){},extra: true})",
    "Object.freeze({get resolveSession(){__countCall()},signIn(){},signOut(){}})",
    "Object.freeze(Object.create({resolveSession(){},signIn(){},signOut(){}}))",
    "Object.freeze({resolveSession(){},signIn(){},signOut(){},[Symbol('extra')]: true})"
  ]) {
    const h = environment();
    h.run();
    await h.completePrefix(2);
    await h.complete(2, () => h.define(2, expression));
    await h.state("error");
    negative += 1;
  }
  for (const options of [
    {parentMissing: true}, {insertMissing: true}, {createThrow: true},
    {srcThrow: true}, {rewriteSrc: true}, {handlerThrow: true}, {timerThrow: true},
    {insertThrow: 0}, {urlThrow: true},
    {page: "file:///local/index.html"}, {page: "not-a-url"},
    {page: "https://user:password@local.test/app/index.html"}
  ]) {
    const h = environment(options);
    h.run();
    await h.state("error");
    assert.equal(h.requested.length, 0);
    negative += 1;
  }
  for (const index of [1, 2]) {
    const h = environment({insertThrow: index});
    h.run();
    await h.completePrefix(index);
    await h.state("error");
    assert.equal(h.requested.length, index);
    negative += 1;
  }
  {
    const h = environment({clearTimerThrow: true});
    h.run();
    await h.complete(0);
    await h.state("error");
    assert.equal(h.requested.length, 1);
    negative += 1;
  }
  {
    const h = environment({removeThrow: true});
    h.run();
    h.requested[0].onerror();
    await h.state("error");
    negative += 1;
  }
  for (const name of [readyName, names[0]]) {
    const h = environment({proxy: {
      has(target, key) { if (key === name) return privateError(); return Reflect.has(target, key); }
    }});
    h.run();
    if (name === readyName) h.idle(); else await h.state("error");
    assert.equal(h.requested.length, 0);
    negative += 1;
  }
  {
    const h = environment({proxy: {
      getOwnPropertyDescriptor(target, key) {
        if (key === names[0]) return privateError();
        return Reflect.getOwnPropertyDescriptor(target, key);
      }
    }});
    h.run();
    await h.complete(0, () => h.define(0, "() => {}"));
    await h.state("error");
    assert.equal(h.requested.length, 1);
    negative += 1;
  }
  {
    const h = environment();
    h.run();
    const repeatLoad = h.requested[0].onload;
    const lateError = h.requested[0].onerror;
    await h.complete(0);
    repeatLoad();
    lateError();
    await flush();
    assert.equal(h.requested.length, 2);
    await h.complete(1);
    await h.complete(2);
    await h.state("ready");
    assert.equal(h.requested.length, 3);
    positive += 1;
  }
  console.log("v27.37e Loader: " + positive + " Positivtests / PASS; " +
    negative + " Negativtests / vollständig blockiert; echte lokale Module / PASS");
}
main().catch(error => {
  console.error(error && error.stack ? error.stack : error);
  process.exitCode = 1;
});
'''


def require(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    try:
        control = runpy.run_path(str(ROOT / "tools/check-project-continuity-control.py"))
        phase = control["detect_v2737e_phase"]()
        require(phase in {
            "v2737e_implementation_prepared", "v2737e_implementation_committed",
            "v2737e_closure_prepared", "v2737e_closure_committed",
        }, "Loader-Checker benötigt den autorisierten Implementierungs-/Abschlusszustand")
        source = LOADER.read_text(encoding="utf-8")
        document = DOCUMENT.read_text(encoding="utf-8")
        require(not source.startswith("\ufeff") and source.endswith("\n"),
                "Loader benötigt UTF-8 ohne BOM und abschließenden Zeilenumbruch")
        for pattern in (
            r"\b(?:fetch|XMLHttpRequest|WebSocket|importScripts|eval)\s*\(",
            r"\b(?:localStorage|sessionStorage|indexedDB)\b",
            r"\b(?:initializeClient|createClient|getClient|getState|getSession|signInWithPassword)\s*\(",
            r"\.(?:resolveSession|signIn|signOut|from)\s*\(",
            r"\b(?:import|require)\s*\(", r"\bconsole\s*\.",
            r"\b(?:innerHTML|outerHTML|document\.write)\b",
        ):
            require(re.search(pattern, source) is None,
                    "Loader enthält verbotene Operation: " + pattern)
        for marker in (
            "# v27.37e", 'data-enabled="true"', 'data-enabled="false"',
            "ACCAOUI_PARTICIPANT_AUTH_SESSION_BROWSER_LOADER_READY",
            "Supabase bleibt NICHT LIVE.", "15000", "authorization_committed",
            "implementation_prepared", "Keine Auth-, Session- oder Clientoperation",
        ):
            require(marker in document, "Loader-Dokumentation unvollständig: " + marker)
        node = shutil.which("node")
        require(node is not None, "Node.js fehlt")

        def execute(text):
            return subprocess.run(
                [node, "-e", HARNESS, str(ROOT)], input=text, cwd=ROOT,
                capture_output=True, text=True, encoding="utf-8",
                errors="replace", timeout=40, check=False,
            )

        result = execute(source)
        if result.stdout:
            print(result.stdout.strip())
        require(result.returncode == 0, "Synthetischer Loader-Test fehlgeschlagen:\n"
                + result.stderr.strip())
        mutations = (
            ('getAttribute("data-enabled") !== "true"', 'getAttribute("data-enabled") !== "false"'),
            ("readinessName in browserRoot", "browserRoot[readinessName] !== undefined"),
            ("if (boundaries[pending] in browserRoot)", "if (false)"),
            ("if (!await loadLocalScript(source))", "if (!loadLocalScript(source))"),
            ('Object.freeze({ requested: true, ready: false, status: "error" })',
             '({ requested: true, ready: false, status: "error" })'),
            ('Object.freeze({ requested: true, ready: true, status: "ready" })',
             '({ requested: true, ready: true, status: "ready" })'),
        )
        for before, after in mutations:
            require(source.count(before) == 1, "Mutationsanker uneindeutig: " + before)
            changed = execute(source.replace(before, after, 1))
            require(changed.returncode != 0,
                    "Semantische Loader-Manipulation nicht erkannt: " + before)
        print(f"v27.37e semantische Manipulationen: {len(mutations)} / vollständig blockiert")
        print("v27.37e Lifecycle-Phase:", phase)
        print("PASS: Loader, passive Auth-/Session-Kette, Kollisionsschutz und exakter Dateiscope.")
        print("Supabase NICHT LIVE; keine Git-Mutation; keine echten Daten.")
        return 0
    except (ValueError, OSError, subprocess.SubprocessError) as exc:
        print("STOPP: v27.37e Loader-Checker: " + str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
