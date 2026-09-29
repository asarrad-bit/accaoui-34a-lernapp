#!/usr/bin/env python3
"""Strict v27.37i oral-mistake empty-state and mutation checker."""

from __future__ import annotations

import json
import runpy
import shutil
import subprocess
import sys
from pathlib import Path


sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
BASE_SHA = "31cf29845af3c15ebe68fc14bb339f4717c3168b"
ORAL_PATH = "oral-exam.js"
DOC_PATH = "docs/ORAL_MISTAKE_EMPTY_STATE_V2737I.md"
PREFLIGHT_PATH = "tools/preflight.py"
MARKER = (
    "/* =====================================================\n"
    "   v23.4.0 MÜNDLICHER FEHLERTRAINER – SAUBERER RENDERER\n"
)
CHECKER_PLACEHOLDER = "V2737I_IMPLEMENTATION_CHECKER = None\n"
CHECKER_REGISTRATION = (
    'V2737I_IMPLEMENTATION_CHECKER = '
    '"tools/check-oral-mistake-empty-state-v2737i.py"\n'
)
P3_TEXT = "Diese Fragen wurden in der 15-Minuten-Simulation mit „Noch üben“"
FROZEN_PATHS = (
    "app.js",
    "index.html",
    "style.css",
    "patch-v21.js",
    "oral-exam.css",
    "oral-sheets.js",
    "oral-sheets-v23.js",
    "questions.json",
    "data/oral-question-bank.js",
    "data/oral-sheets-bank.js",
    "test/oral-exam.js",
    "test/oral-exam.css",
    "test/oral-sheets.js",
    "test/app.js",
    "test/patch-v21.js",
    "test/index.html",
    "test/style.css",
    "test/questions.json",
    "test/data/oral-question-bank.js",
    "test/data/oral-sheets-bank.js",
)


class ContractError(RuntimeError):
    """The v27.37i implementation contract was violated."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ContractError(message)


def git_blob(path: str) -> bytes:
    result = subprocess.run(
        ["git", "show", f"{BASE_SHA}:{path}"],
        cwd=ROOT,
        capture_output=True,
        check=False,
    )
    require(result.returncode == 0, "Basis-Blob nicht lesbar: " + path)
    return result.stdout


def snapshot() -> dict[str, bytes]:
    paths = (ORAL_PATH, *FROZEN_PATHS)
    result = {}
    for path in paths:
        target = ROOT / path
        require(target.is_file(), "Pflichtdatei fehlt: " + path)
        result[path] = target.read_bytes()
    return result


def baselines() -> dict[str, bytes]:
    return {path: git_blob(path) for path in (ORAL_PATH, *FROZEN_PATHS)}


def validate_snapshot(current: dict[str, bytes], base: dict[str, bytes], scope_validator) -> None:
    expected = {ORAL_PATH, *FROZEN_PATHS}
    require(set(current) == expected and set(base) == expected, "Snapshot-Scope unvollständig")
    for path in FROZEN_PATHS:
        require(current[path] == base[path], "Frozen-Datei verändert: " + path)

    oral = current[ORAL_PATH]
    base_oral = base[ORAL_PATH]
    require(oral != base_oral, "oral-exam.js enthält keine Implementation")
    try:
        oral_text = oral.decode("utf-8")
        base_text = base_oral.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ContractError("oral-exam.js ist kein striktes UTF-8") from exc
    require(not oral_text.startswith("\ufeff") and oral_text.endswith("\n"),
            "oral-exam.js benötigt UTF-8 ohne BOM und finalen Zeilenumbruch")
    require(oral_text.count(MARKER) == 1 and base_text.count(MARKER) == 1,
            "v23.4.0-Blockmarker fehlt oder ist doppelt")
    try:
        oral_prefix = scope_validator(oral)
        base_prefix = scope_validator(base_oral)
    except Exception as exc:
        raise ContractError("v23.4.0-Blockgrenze verletzt: " + str(exc)) from exc
    require(oral_prefix == base_prefix,
            "oral-exam.js außerhalb des v23.4.0-Blocks verändert")


def validate_document_and_preflight() -> None:
    document_path = ROOT / DOC_PATH
    require(document_path.is_file(), "v27.37i-Dokumentation fehlt")
    document_bytes = document_path.read_bytes()
    try:
        document = document_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ContractError("v27.37i-Dokumentation ist kein striktes UTF-8") from exc
    require(not document.startswith("\ufeff") and document.endswith("\n"),
            "v27.37i-Dokumentation benötigt UTF-8 ohne BOM und finalen Zeilenumbruch")
    for marker in (
        "# v27.37i",
        "Ursache",
        "Reparatur",
        "Leerzustand",
        "Bei 0 Fehlern",
        "Bei 1 Fehler",
        "Bei mehreren Fehlern",
        "Storage-Semantik",
        "accaoui_oral_exam_mistakes_v2324",
        "P3 ist ausdrücklich ausgeschlossen",
        "Fragen,\nPrüfungsbögen, Timer und Bewertung bleiben unverändert",
        "Supabase bleibt\nNICHT LIVE.",
        "Exakter Vier-Dateien-Scope",
        "tools/check-oral-mistake-empty-state-v2737i.py",
    ):
        require(marker in document, "Dokumentationsvertrag fehlt: " + marker)

    base_preflight = git_blob(PREFLIGHT_PATH).decode("utf-8")
    current_preflight = (ROOT / PREFLIGHT_PATH).read_text(encoding="utf-8")
    require(base_preflight.count(CHECKER_PLACEHOLDER) == 1,
            "Checker-Platzhalter ist in der Basis nicht eindeutig")
    expected_preflight = base_preflight.replace(
        CHECKER_PLACEHOLDER, CHECKER_REGISTRATION, 1
    )
    require(current_preflight == expected_preflight,
            "tools/preflight.py enthält mehr als die vorbereitete Checker-Registrierung")


def replace_once(source: str, before: str, after: str, label: str) -> str:
    require(source.count(before) == 1, "Mutationsanker uneindeutig: " + label)
    return source.replace(before, after, 1)


def changed(
    source: dict[str, bytes], path: str, before: bytes, after: bytes, label: str
) -> dict[str, bytes]:
    require(source[path].count(before) == 1, "Mutationsanker uneindeutig: " + label)
    result = dict(source)
    result[path] = source[path].replace(before, after, 1)
    return result


HARNESS = r'''
"use strict";
const assert = require("node:assert/strict");
const vm = require("node:vm");
const source = require("node:fs").readFileSync(0, "utf8");
const KEY = "accaoui_oral_exam_mistakes_v2324";
const STALE =
  '<article class="oral-mistake-card-v2324" data-oral-mistake-key-v2340="stale"></article>' +
  '<div class="oral-mistake-count-v2324"><strong>9</strong></div>';

function parseAttributes(text) {
  const attributes = {};
  const pattern = /([A-Za-z_:][A-Za-z0-9_:.-]*)(?:="([^"]*)")?/g;
  let match;
  while ((match = pattern.exec(text)) !== null) {
    attributes[match[1]] = match[2] === undefined ? "" : match[2];
  }
  return attributes;
}

class SyntheticElement {
  constructor(tagName, attributes, state) {
    this.tagName = tagName;
    this.attributes = {...attributes};
    this.state = state;
    this.children = [];
    this.listeners = new Map();
    this.style = {};
    const style = this.attributes.style || "";
    const display = /(?:^|;)\s*display\s*:\s*([^;]+)/.exec(style);
    if (display) this.style.display = display[1].trim();
    const classes = new Set((this.attributes.class || "").split(/\s+/).filter(Boolean));
    this.classList = {
      add: (...names) => names.forEach(name => classes.add(name)),
      remove: (...names) => names.forEach(name => classes.delete(name)),
      contains: name => classes.has(name)
    };
    this._classes = classes;
    this._html = "";
    this.textContent = "";
  }
  set innerHTML(value) {
    this._html = String(value);
    this.children = [];
    parseHtmlInto(this, this._html);
    this.state.renderCalls += 1;
  }
  get innerHTML() {
    return this._html;
  }
  getAttribute(name) {
    return Object.prototype.hasOwnProperty.call(this.attributes, name)
      ? this.attributes[name]
      : null;
  }
  setAttribute(name, value) {
    this.attributes[name] = String(value);
  }
  addEventListener(type, listener) {
    if (!this.listeners.has(type)) this.listeners.set(type, []);
    this.listeners.get(type).push(listener);
  }
  click() {
    for (const listener of this.listeners.get("click") || []) listener.call(this);
  }
  matches(selector) {
    if (selector.startsWith(".")) return this._classes.has(selector.slice(1));
    const attribute = /^\[([^\]]+)\]$/.exec(selector);
    return Boolean(attribute && Object.prototype.hasOwnProperty.call(
      this.attributes, attribute[1]
    ));
  }
  querySelectorAll(selector) {
    const result = [];
    for (const child of this.children) {
      if (child.matches(selector)) result.push(child);
      result.push(...child.querySelectorAll(selector));
    }
    return result;
  }
  querySelector(selector) {
    return this.querySelectorAll(selector)[0] || null;
  }
}

function parseHtmlInto(root, html) {
  const articlePattern = /<article\b([^>]*)>([\s\S]*?)<\/article>/g;
  let articleMatch;
  while ((articleMatch = articlePattern.exec(html)) !== null) {
    const card = new SyntheticElement(
      "article", parseAttributes(articleMatch[1]), root.state
    );
    const body = articleMatch[2];
    for (const className of [
      "oral-mistake-answer-v2324",
      "oral-mistake-note-v2324"
    ]) {
      if (body.includes('class="' + className + '"')) {
        card.children.push(new SyntheticElement(
          "div", {class: className, style: "display:none;"}, root.state
        ));
      }
    }
    const buttonPattern = /<button\b([^>]*)>([\s\S]*?)<\/button>/g;
    let buttonMatch;
    while ((buttonMatch = buttonPattern.exec(body)) !== null) {
      const button = new SyntheticElement(
        "button", parseAttributes(buttonMatch[1]), root.state
      );
      button.textContent = buttonMatch[2].replace(/<[^>]*>/g, "").trim();
      card.children.push(button);
    }
    root.children.push(card);
  }
}

function mistake(key, question) {
  return {
    key,
    question,
    sampleAnswer: "Muster " + key,
    examinerNote: "Hinweis " + key,
    examinerName: "Prüfer",
    examinerBlockTitle: "Prüfungsbogen A"
  };
}

function fixture(raw) {
  const state = {
    renderCalls: 0,
    reloadCalls: 0,
    overviewCalls: 0,
    simulationCalls: 0,
    notices: [],
    writes: []
  };
  const storage = new Map();
  if (raw !== undefined) storage.set(KEY, raw);
  const main = new SyntheticElement("main", {class: "main-content"}, state);
  main.innerHTML = STALE;
  state.renderCalls = 0;
  const windowObject = {};
  const documentObject = {
    querySelector(selector) {
      return selector === ".main-content" ? main : null;
    },
    querySelectorAll(selector) {
      return main.querySelectorAll(selector);
    }
  };
  const localStorageObject = {
    getItem(key) {
      return storage.has(String(key)) ? storage.get(String(key)) : null;
    },
    setItem(key, value) {
      const normalizedKey = String(key);
      const normalizedValue = String(value);
      state.writes.push([normalizedKey, normalizedValue]);
      storage.set(normalizedKey, normalizedValue);
    },
    removeItem(key) {
      storage.delete(String(key));
    },
    key(index) {
      return [...storage.keys()][index] || null;
    },
    get length() {
      return storage.size;
    }
  };
  const context = {
    window: windowObject,
    document: documentObject,
    localStorage: localStorageObject,
    location: {reload() { state.reloadCalls += 1; }},
    showMistakeOverview() { state.overviewCalls += 1; },
    startOralSimulation15V2314() { state.simulationCalls += 1; },
    showSmallNotice(message) { state.notices.push(String(message)); },
    console: {log() {}, info() {}, warn() {}, error() {}}
  };
  vm.createContext(context);
  vm.runInContext(source, context, {filename: "oral-exam-v23.4.0.js"});
  return {
    state,
    storage,
    main,
    open() {
      windowObject.showOralMistakeTrainingV2340();
    }
  };
}

function assertOnlyStorageKey(test, label) {
  assert.deepEqual([...test.storage.keys()].sort(), [KEY], label + ": zusätzlicher Storage-Key");
}

function assertEmpty(test, label) {
  const html = test.main.innerHTML;
  assert(html.includes("Mündliche Fehler"), label + ": Titel fehlt");
  assert(html.includes("Keine offenen mündlichen Fehler"), label + ": Leerüberschrift fehlt");
  assert(
    html.includes("Alle aktuell gespeicherten mündlichen Fehler wurden bearbeitet."),
    label + ": Erklärung fehlt"
  );
  assert(html.includes("Zur Fehlerübersicht"), label + ": Fehlerübersicht fehlt");
  assert(html.includes("Zurück zum Dashboard"), label + ": Dashboard-Aktion fehlt");
  assert(!html.includes("oral-mistake-card-v2324"), label + ": alte Karte sichtbar");
  assert(!html.includes("oral-mistake-count-v2324"), label + ": alter Zähler sichtbar");
  assert.equal(
    test.main.querySelectorAll("[data-oral-mistake-key-v2340]").length,
    0,
    label + ": synthetischer DOM enthält Fehlerkarte"
  );
  assert.equal(test.state.reloadCalls, 0, label + ": erzwungener Reload");
  assert.equal(test.state.overviewCalls, 0, label + ": erzwungene Navigation");
}

function assertCount(test, expected, label) {
  const cards = test.main.querySelectorAll("[data-oral-mistake-key-v2340]");
  assert.equal(cards.length, expected, label + ": falsche Kartenanzahl");
  assert(
    test.main.innerHTML.includes("<strong>" + expected + "</strong>"),
    label + ": falscher Zähler"
  );
  assert(
    test.main.innerHTML.includes("oral-mistake-count-v2324"),
    label + ": Zähler fehlt"
  );
  assert(
    !test.main.innerHTML.includes("Keine offenen mündlichen Fehler"),
    label + ": Leerzustand trotz Fehlern"
  );
  for (const card of cards) {
    assert(card.classList.contains("is-normalized-v2335"), label + ": Karte nicht normalisiert");
  }
}

function action(card, name) {
  const button = card.querySelectorAll("[data-oral-action-v2340]").find(
    candidate => candidate.getAttribute("data-oral-action-v2340") === name
  );
  assert(button, "Aktion fehlt: " + name);
  return button;
}

function main() {
  let positive = 0;

  const empty = fixture("[]");
  empty.open();
  assertEmpty(empty, "0 Fehler");
  assert.equal(empty.storage.get(KEY), "[]", "0 Fehler: Storage verändert");
  assertOnlyStorageKey(empty, "0 Fehler");
  positive += 1;

  const oneRaw = JSON.stringify([mistake("a", "Frage A")]);
  const one = fixture(oneRaw);
  one.open();
  assertCount(one, 1, "1 Fehler");
  assert.equal(one.storage.get(KEY), oneRaw, "1 Fehler: Storage verändert");
  positive += 1;

  const twoRaw = JSON.stringify([
    mistake("a", "Frage A"),
    mistake("b", "Frage B")
  ]);
  const two = fixture(twoRaw);
  two.open();
  assertCount(two, 2, "2 Fehler");
  assert.equal(two.storage.get(KEY), twoRaw, "2 Fehler: Storage verändert");
  positive += 1;

  let firstCard = two.main.querySelectorAll("[data-oral-mistake-key-v2340]")[0];
  action(firstCard, "reveal").click();
  assert.equal(firstCard.getAttribute("data-oral-mistake-open-v2340"), "true");
  assert.equal(firstCard.querySelector(".oral-mistake-answer-v2324").style.display, "block");
  assert.equal(firstCard.querySelector(".oral-mistake-note-v2324").style.display, "block");
  assert.equal(action(firstCard, "resolve").style.display, "inline-flex");
  assert.equal(action(firstCard, "collapse").style.display, "inline-flex");
  positive += 1;

  const practice = action(firstCard, "collapse");
  assert.equal(practice.textContent, "Noch üben");
  practice.click();
  assert.equal(firstCard.getAttribute("data-oral-mistake-open-v2340"), "false");
  assert.equal(firstCard.querySelector(".oral-mistake-answer-v2324").style.display, "none");
  assert.equal(action(firstCard, "reveal").style.display, "inline-flex");
  positive += 1;

  action(firstCard, "reveal").click();
  action(firstCard, "resolve").click();
  assertCount(two, 1, "erster von 2 gelöst");
  let stored = JSON.parse(two.storage.get(KEY));
  assert.deepEqual(stored.map(item => item.key), ["b"]);
  positive += 1;

  const lastCard = two.main.querySelectorAll("[data-oral-mistake-key-v2340]")[0];
  action(lastCard, "reveal").click();
  action(lastCard, "resolve").click();
  assertEmpty(two, "letzter Fehler gelöst");
  positive += 1;

  assert.equal(two.storage.get(KEY), "[]", "Storage nach letztem Fehler nicht exakt []");
  positive += 1;

  const reopened = fixture(two.storage.get(KEY));
  reopened.open();
  assertEmpty(reopened, "erneutes Öffnen bei []");
  assert.equal(reopened.storage.get(KEY), "[]");
  positive += 1;

  const broken = fixture("{kaputtes-json");
  broken.open();
  assertEmpty(broken, "beschädigtes JSON");
  assert.equal(broken.storage.get(KEY), "{kaputtes-json", "beschädigtes JSON wurde verändert");
  assert.equal(broken.state.writes.length, 0, "beschädigtes JSON wurde überschrieben");
  positive += 1;

  assertOnlyStorageKey(two, "Interaktionsfolge");
  assertOnlyStorageKey(reopened, "erneutes Öffnen");
  assertOnlyStorageKey(broken, "beschädigtes JSON");
  positive += 1;

  process.stdout.write(JSON.stringify({positive}));
}

try {
  main();
} catch (error) {
  process.stderr.write(String(error && error.stack ? error.stack : error));
  process.exit(1);
}
'''


def target_block(source: str) -> str:
    require(source.count(MARKER) == 1, "v23.4.0-Zielblock nicht eindeutig")
    return source[source.index(MARKER):]


def syntax_check(node: str, source: str, label: str) -> None:
    result = subprocess.run(
        [node, "--check"],
        input=source,
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="strict",
        timeout=30,
        check=False,
    )
    require(result.returncode == 0, "Mutation ist kein gültiges JavaScript: " + label)


def execute(node: str, source: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [node, "-e", HARNESS],
        input=target_block(source),
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="strict",
        timeout=60,
        check=False,
    )


def main() -> int:
    try:
        control = runpy.run_path(
            str(ROOT / "tools/check-project-continuity-control.py")
        )
        phase = control["detect_v2737i_phase"]()
        require(
            phase in {
                "v2737i_implementation_prepared",
                "v2737i_implementation_committed",
                "v2737i_closure_prepared",
                "v2737i_closure_committed",
            },
            "Kein autorisierter v27.37i-Implementierungs-/Abschlusszustand",
        )
        scope_validator = control.get("v2737i_oral_remainder")
        require(callable(scope_validator), "v27.37i-Blockgrenzenvalidator fehlt")

        base = baselines()
        good = snapshot()
        validate_snapshot(good, base, scope_validator)
        validate_document_and_preflight()

        node = shutil.which("node")
        require(node is not None, "Node.js fehlt")
        oral_source = good[ORAL_PATH].decode("utf-8")
        syntax_check(node, oral_source, "aktuelle oral-exam.js")
        result = execute(node, oral_source)
        require(
            result.returncode == 0,
            "synthetischer DOM-/Storage-Harness fehlgeschlagen:\n" + result.stderr,
        )
        summary = json.loads(result.stdout)
        require(summary == {"positive": 11}, "Unvollständige Positivmatrix")
        print(
            "Positivfälle: 11 / PASS "
            "(0/1/2 Fehler, Reveal, Collapse/Noch üben, erstes/letztes Entfernen, "
            "Storage [], erneutes Öffnen, beschädigtes JSON, kein Zusatz-Key)"
        )

        js_mutations = (
            (
                "alter Return ohne Neurendern",
                replace_once(
                    oral_source,
                    "    if (!mistakes.length) {\n      mainContent.innerHTML =",
                    "    if (!mistakes.length) {\n      const ignoredEmptyState =",
                    "alter Return ohne Neurendern",
                ),
            ),
            (
                "alte Karte bleibt sichtbar",
                replace_once(
                    oral_source,
                    '        "<p>Alle aktuell gespeicherten mündlichen Fehler wurden bearbeitet.</p>" +',
                    '        "<p>Alle aktuell gespeicherten mündlichen Fehler wurden bearbeitet.</p>" +\n'
                    '        \'<article class="oral-mistake-card-v2324">Alt</article>\' +',
                    "stale Karte",
                ),
            ),
            (
                "alter Zähler bleibt sichtbar",
                replace_once(
                    oral_source,
                    '        "<p>Alle aktuell gespeicherten mündlichen Fehler wurden bearbeitet.</p>" +',
                    '        "<p>Alle aktuell gespeicherten mündlichen Fehler wurden bearbeitet.</p>" +\n'
                    '        \'<div class="oral-mistake-count-v2324"><strong>1</strong></div>\' +',
                    "stale Zähler",
                ),
            ),
            (
                "letzter Fehler wird nicht entfernt",
                replace_once(
                    oral_source,
                    "    removeOralMistakeV2340(key);",
                    "    readOralMistakesV2340();",
                    "fehlendes Entfernen",
                ),
            ),
            (
                "Fehler wird wieder angelegt",
                replace_once(
                    oral_source,
                    "    removeOralMistakeV2340(key);",
                    "    removeOralMistakeV2340(key);\n"
                    '    writeOralMistakesV2340([{ key: key, question: "wieder angelegt" }]);',
                    "Wiederanlegen",
                ),
            ),
            (
                "zusätzlicher Storage-Key",
                replace_once(
                    oral_source,
                    "  function writeOralMistakesV2340(list) {\n"
                    "    localStorage.setItem(",
                    "  function writeOralMistakesV2340(list) {\n"
                    '    localStorage.setItem("accaoui_oral_exam_mistakes_v2737i_shadow", "[]");\n'
                    "    localStorage.setItem(",
                    "zusätzlicher Storage-Key",
                ),
            ),
        )
        blocked = 0
        for label, mutation in js_mutations:
            require(mutation != oral_source, "Mutation änderte keine Quelle: " + label)
            syntax_check(node, mutation, label)
            mutated_result = execute(node, mutation)
            require(
                mutated_result.returncode != 0,
                "Semantische Mutation nicht erkannt: " + label,
            )
            print("MUTATION BLOCKIERT: " + label)
            blocked += 1

        structural_mutations = []
        structural_mutations.append((
            "Änderung an app.js",
            {**good, "app.js": good["app.js"] + b"\n// v27.37i unerlaubte App-Aenderung\n"},
            "app.js",
        ))
        structural_mutations.append((
            "Änderung an patch-v21.js",
            {**good, "patch-v21.js": good["patch-v21.js"] + b"\n// v27.37i unerlaubte Patch-Aenderung\n"},
            "patch-v21.js",
        ))
        structural_mutations.append((
            "Änderung außerhalb des v23.4.0-Blocks",
            {**good, ORAL_PATH: b"// v27.37i unerlaubter Prefix\n" + good[ORAL_PATH]},
            ORAL_PATH,
        ))
        structural_mutations.append((
            "P3-Text verändert",
            changed(
                good,
                "patch-v21.js",
                P3_TEXT.encode("utf-8"),
                "Diese Fragen wurden in einer Themenübung mit „Noch üben“".encode("utf-8"),
                "P3-Text",
            ),
            "patch-v21.js",
        ))
        for label, mutation, javascript_path in structural_mutations:
            syntax_check(
                node,
                mutation[javascript_path].decode("utf-8"),
                label,
            )
            try:
                validate_snapshot(mutation, base, scope_validator)
            except ContractError:
                print("MUTATION BLOCKIERT: " + label)
                blocked += 1
            else:
                raise ContractError("Scope-Mutation nicht erkannt: " + label)

        require(blocked == 10, "Unvollständige semantische Mutationsmatrix")
        print("v27.37i mündlicher Fehlertrainer-Leerzustand: PASS")
        print("Tatsächliche v23.4.0-JavaScript-Logik im synthetischen DOM/Storage: PASS")
        print("Storage nach letztem Fehler exakt [] und kein zusätzlicher Key: PASS")
        print("Beschädigtes JSON fail-safe und unverändert: PASS")
        print(f"Frozen-Dateien: {len(FROZEN_PATHS)} / byte-identisch")
        print("oral-exam.js außerhalb v23.4.0: byte-identisch")
        print(f"Semantische Mutationen: {blocked} / vollständig blockiert")
        print("Historische Checks und Preflight-Registrierung: unverändert streng")
        print("P3 und Herkunftsbezeichnung 15-Minuten-Simulation: unverändert")
        print("Supabase NICHT LIVE")
        print("Phase: " + phase)
        return 0
    except (
        ContractError,
        json.JSONDecodeError,
        OSError,
        subprocess.SubprocessError,
        UnicodeDecodeError,
    ) as exc:
        print("STOPP: v27.37i-Checker: " + str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
