#!/usr/bin/env python3
"""Execute both real oral-mistake blocks; protect the text-only v27.37j scope."""

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
BASE_SHA = "45cd7cf523c3ff93b7bab2b28311233f888b4221"
PATCH = "patch-v21.js"
ORAL = "oral-exam.js"
PREFLIGHT = "tools/preflight.py"
DOC = "docs/ORAL_MISTAKE_ORIGIN_LABEL_V2737J.md"
SELF = "tools/check-oral-mistake-origin-label-v2737j.py"
SCOPE = frozenset((PATCH, ORAL, PREFLIGHT, DOC, SELF))
PATCH_START = (
    "/* =====================================================\n"
    "   v23.2.4 MÜNDLICHE PRÜFUNGSFEHLER TRAINIEREN\n"
)
PATCH_END = (
    "/* =====================================================\n"
    "   v23.2.5 MÜNDLICHE FEHLERTRAINER – ANTWORT AUFDECKEN\n"
)
ORAL_START = (
    "/* =====================================================\n"
    "   v23.4.0 MÜNDLICHER FEHLERTRAINER – SAUBERER RENDERER\n"
)


class ContractError(RuntimeError):
    """A real implementation, runtime or mutation assertion failed."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ContractError(message)


def git(*arguments: str) -> bytes:
    result = subprocess.run(
        ["git", *arguments], cwd=ROOT, capture_output=True, check=False,
    )
    require(result.returncode == 0, "Git-Prüfung fehlgeschlagen: " + " ".join(arguments))
    return result.stdout


def target_block(source: bytes, path: str) -> str:
    text = source.decode("utf-8")
    start = PATCH_START if path == PATCH else ORAL_START
    require(text.count(start) == 1, "Zielblock nicht eindeutig: " + path)
    offset = text.index(start)
    if path == PATCH:
        require(text.count(PATCH_END) == 1, "Patch-Blockende nicht eindeutig")
        end = text.index(PATCH_END)
        require(offset < end, "Patch-Blockgrenzen vertauscht")
        return text[offset:end]
    return text[offset:]


def expected_product(base: dict[str, bytes]) -> dict[str, bytes]:
    """Independent exact-byte contract: only the three authorized text edits."""
    result = dict(base)
    substitutions = (
        (PATCH, "Diese Fragen wurden in der 15-Minuten-Simulation mit",
         "Diese Fragen wurden in der mündlichen Vorbereitung mit"),
        (PATCH, "Hier erscheinen nur Fragen, die in der mündlichen Simulation mit",
         "Hier erscheinen Fragen, die in der mündlichen Vorbereitung mit"),
        (ORAL, "Hier erscheinen nur Fragen, die in der mündlichen Simulation mit",
         "Hier erscheinen Fragen, die in der mündlichen Vorbereitung mit"),
    )
    for path, before, after in substitutions:
        block = target_block(result[path], path).encode("utf-8")
        require(block.count(before.encode("utf-8")) == 1,
                "Basis-Herkunftstext nicht eindeutig: " + path)
        replacement = block.replace(before.encode("utf-8"), after.encode("utf-8"), 1)
        require(result[path].count(block) == 1, "Basisblock nicht eindeutig")
        result[path] = result[path].replace(block, replacement, 1)
    return result


def validate_snapshot(current: dict[str, bytes], base: dict[str, bytes], control: dict) -> None:
    require(set(current) == set(base), "Frozen-/Produktsnapshot unvollständig")
    require(control["v2737j_patch_frozen_parts"](current[PATCH])
            == control["v2737j_patch_frozen_parts"](base[PATCH]),
            "patch-v21.js außerhalb v23.2.4 verändert")
    require(control["v2737i_oral_remainder"](current[ORAL])
            == control["v2737i_oral_remainder"](base[ORAL]),
            "oral-exam.js außerhalb v23.4.0 verändert")
    expected = expected_product(base)
    for path in base:
        require(current[path] == expected[path],
                "Unerlaubte Produkt-/Frozen-Änderung: " + path)


def validate_document_and_preflight() -> None:
    data = (ROOT / DOC).read_bytes()
    document = data.decode("utf-8")
    require(not document.startswith("\ufeff") and document.endswith("\n"),
            "Dokument benötigt UTF-8 ohne BOM und finalen Zeilenumbruch")
    normalized = " ".join(document.split())
    for marker in (
        "# v27.37j", "Ursache", "keine belastbare Provenienz",
        "mündliche Vorbereitung", "Keine neue Persistenz", "Keine Migration",
        "accaoui_oral_exam_mistakes_v2324", "Storage-/UI-Verhalten",
        "Fragen, Prüfungsbögen, Timer und Bewertung bleiben unverändert",
        "v27.37i-Leerzustand", "Supabase bleibt NICHT LIVE.",
        "Exakter Fünf-Dateien-Scope", *sorted(SCOPE),
    ):
        require(marker in normalized, "Dokumentationsvertrag fehlt: " + marker)
    base = git("show", f"{BASE_SHA}:{PREFLIGHT}")
    placeholder = b"V2737J_IMPLEMENTATION_CHECKER = None\n"
    registration = (
        b'V2737J_IMPLEMENTATION_CHECKER = '
        b'"tools/check-oral-mistake-origin-label-v2737j.py"\n'
    )
    require(base.count(placeholder) == 1, "Registrierung in Basis nicht eindeutig")
    require((ROOT / PREFLIGHT).read_bytes() == base.replace(placeholder, registration, 1),
            "Preflight enthält mehr als die vorbereitete Checker-Registrierung")


HARNESS = r'''
"use strict";
const assert = require("node:assert/strict");
const vm = require("node:vm");
const input = JSON.parse(require("node:fs").readFileSync(0, "utf8"));
const KEY = "accaoui_oral_exam_mistakes_v2324";
const OVERVIEW = 'Diese Fragen wurden in der mündlichen Vorbereitung mit „Noch üben“ bewertet.';
const TRAINING = 'Hier erscheinen Fragen, die in der mündlichen Vorbereitung mit „Noch üben“ bewertet wurden.';
const text = html => html.replace(/<[^>]*>/g, " ").replace(/\s+/g, " ").trim();
function hint(html, expected) {
  // Inspect the actual paragraph rendered by the executed product function.
  const paragraphs = [...html.matchAll(/<p(?:\s[^>]*)?>([\s\S]*?)<\/p>/g)].map(m => text(m[1]));
  assert.equal(paragraphs.filter(p => p === expected).length, 1, "neutraler Herkunftshinweis fehlt/falsch");
}
function mistake(key) {
  return {key, id:key, question:"Frage " + key, category:"Umgang mit Menschen",
    sampleAnswer:"Muster " + key, examinerNote:"Hinweis " + key, legacy:"beibehalten"};
}
function fixture(raw, leading) {
  const storage = new Map(raw === undefined ? [] : [[KEY, raw]]);
  const writes = [], timers = [], rates = [], notices = [];
  let navigation = 0;
  class Element {
    constructor() { this.innerHTML = ""; this.children = []; this.classList = {add(){}}; }
    appendChild(child) { this.children.push(child); }
    querySelectorAll() { return []; }
  }
  const main = new Element(), wrapper = new Element(), review = new Element();
  const context = {
    document: {
      querySelector(selector) {
        return selector === ".main-content" ? main : selector === ".result-wrapper" ? wrapper : null;
      },
      querySelectorAll() { return []; },
      getElementById(id) {
        return id === "oralReviewButtonV2323" ? review : wrapper.children.find(e => e.id === id) || null;
      },
      createElement() { return new Element(); }
    },
    localStorage: {
      getItem(key) { return storage.has(String(key)) ? storage.get(String(key)) : null; },
      setItem(key,value) { writes.push([String(key),String(value)]); storage.set(String(key),String(value)); },
      removeItem(key) { writes.push([String(key),null]); storage.delete(String(key)); },
      key(index) { return [...storage.keys()][index] || null; },
      get length() { return storage.size; }
    },
    oralExamQuestionsV220: [{id:"q",question:"Synthetische Frage",sampleAnswer:"Antwort"}],
    oralExamIndexV220: 0,
    Date: class extends Date { constructor(...args) { super(...(args.length ? args : ["2026-01-01T00:00:00Z"])); } },
    setTimeout(callback) { timers.push(callback); },
    escapeHtml(value) { return String(value).replace(/&/g,"&amp;").replace(/</g,"&lt;"); },
    showSmallNotice(message) { notices.push(message); },
    showMistakeOverview() { wrapper.children = []; return "overview"; },
    showOralExamFinishScreenV220() { return "finished"; },
    rateOralExamQuestionV220(status) { rates.push(status); return "rated:" + status; },
    startOralSimulation15V2314() { navigation += 1; },
    location: {reload() { navigation += 1; }},
    console: {log(){},info(){},warn(){},error(){}}
  };
  context.window = context;
  vm.createContext(context);
  vm.runInContext(input.patch, context, {filename:"patch-v21-v23.2.4.js"});
  if (leading) vm.runInContext(input.oral, context, {filename:"oral-exam-v23.4.0.js"});
  return {context,storage,writes,main,wrapper,review,rates,notices,
    open() { context.showOralMistakeTrainingV2324(); },
    overview() { assert.equal(context.showMistakeOverview(),"overview"); while(timers.length) timers.shift()(); },
    navigation() { return navigation; }};
}
let positive = 0;
for (const leading of [false,true]) {
  for (const count of [1,2]) {
    const raw = JSON.stringify(Array.from({length:count},(_,i) => mistake("m" + i)));
    const test = fixture(raw,leading);
    test.open();
    hint(test.main.innerHTML, TRAINING + (leading ? " Die Musterantwort bleibt zuerst verdeckt." : ""));
    assert.equal([...test.main.innerHTML.matchAll(/<article\b/g)].length,count);
    assert(new RegExp("<strong>\\s*" + count + "\\s*</strong>").test(test.main.innerHTML));
    assert.equal(test.storage.get(KEY),raw,"Öffnen darf Altdaten nicht ändern");
    assert.equal(test.writes.length,0,"Öffnen darf nicht migrieren");
    test.overview();
    assert.equal(test.wrapper.children.length,1,"Übersichtsbox fehlt oder doppelt");
    hint(test.wrapper.children[0].innerHTML,OVERVIEW);
    assert(text(test.wrapper.children[0].innerHTML).includes(count + " mündliche Prüfungsfehler"));
    assert.equal(test.review.textContent,"Mündliche Fehler trainieren (" + count + ")");
    assert.equal(test.storage.get(KEY),raw);
    assert.equal(test.writes.length,0);
    assert.equal(test.navigation(),0);
    assert.deepEqual([...test.storage.keys()],[KEY]);
    positive += 1;
  }
  for (const raw of [undefined,"[]","{kaputtes-json",'{"keine":"Liste"}']) {
    const test = fixture(raw,leading);
    test.overview();
    assert.equal(test.wrapper.children.length,0,"Übersichtsbox ohne offene Fehler");
    test.open();
    if (leading) {
      assert(text(test.main.innerHTML).includes("Keine offenen mündlichen Fehler"));
      assert(!test.main.innerHTML.includes("oral-mistake-card-v2324"));
      assert(!test.main.innerHTML.includes("oral-mistake-count-v2324"));
    }
    assert.equal(test.writes.length,0,"Lesen darf nicht migrieren/überschreiben");
    assert.equal(test.storage.get(KEY),raw);
    assert.equal(test.navigation(),0);
    positive += 1;
  }
}
const stored = fixture(JSON.stringify([mistake("alt")]),true);
assert.equal(stored.context.rateOralExamQuestionV220("practice"),"rated:practice");
let entries = JSON.parse(stored.storage.get(KEY));
assert.deepEqual(entries[0],mistake("alt"),"Fremde Alt-Felder verloren");
const expected = {key:"q",id:"q",category:"Mündliche Prüfung",question:"Synthetische Frage",
  sampleAnswer:"Antwort",examinerNote:"",examinerName:"",examinerBlockTitle:"",sheetId:"",
  sheetTitle:"Prüfungsbogen A",savedAt:"2026-01-01T00:00:00.000Z"};
assert.deepEqual(entries[1],expected,"neue Herkunftsdaten oder verändertes Datenformat");
positive += 1;
stored.context.rateOralExamQuestionV220("practice");
entries = JSON.parse(stored.storage.get(KEY));
assert.equal(entries.length,2,"Wiederbewertung legt Duplikat an");
assert.deepEqual(entries[1],expected);
positive += 1;
stored.context.rateOralExamQuestionV220("known");
assert.deepEqual(JSON.parse(stored.storage.get(KEY)),[mistake("alt")]);
assert.deepEqual(stored.rates,["practice","practice","known"]);
assert.deepEqual([...stored.storage.keys()],[KEY]);
assert(stored.writes.every(([key]) => key === KEY));
assert.equal(stored.navigation(),0);
positive += 1;
process.stdout.write(JSON.stringify({positive}));
'''


def syntax_check(node: str, source: bytes, label: str) -> None:
    result = subprocess.run(
        [node, "--check"], input=source, cwd=ROOT, capture_output=True,
        timeout=30, check=False,
    )
    require(result.returncode == 0, "Kein gültiges JavaScript (kein Mutations-PASS): " + label)


def execute(node: str, current: dict[str, bytes], historical: dict) -> tuple[bool, str]:
    result = subprocess.run(
        [node, "-e", HARNESS], cwd=ROOT, capture_output=True, text=True,
        input=json.dumps({"patch": target_block(current[PATCH], PATCH),
                          "oral": target_block(current[ORAL], ORAL)}, ensure_ascii=False),
        encoding="utf-8", errors="strict", timeout=60, check=False,
    )
    if result.returncode != 0:
        return False, result.stderr
    require(json.loads(result.stdout) == {"positive": 15}, "Herkunfts-/Storage-Matrix unvollständig")
    # Execute the unchanged historical harness on the actual current source.
    # No snapshot, phase, runpy, globals or result is replaced.
    result = historical["execute"](node, current[ORAL].decode("utf-8"))
    if result.returncode != 0:
        return False, result.stderr
    require(json.loads(result.stdout) == {"positive": 11}, "Aktuelle Leerzustandsmatrix unvollständig")
    return True, "15 Herkunfts-/Storage-Fälle und 11 aktuelle v27.37i-UI-Fälle PASS"


def mutation(current: dict[str, bytes], path: str, before: str, after: str) -> dict[str, bytes]:
    old = before.encode("utf-8")
    require(current[path].count(old) == 1, "Mutationsanker uneindeutig: " + before)
    return {**current, path: current[path].replace(old, after.encode("utf-8"), 1)}


def main() -> int:
    try:
        control = runpy.run_path(str(ROOT / "tools/check-project-continuity-control.py"))
        phase = control["detect_v2737j_phase"]()
        require(phase in {"v2737j_implementation_prepared", "v2737j_implementation_committed",
                          "v2737j_closure_prepared", "v2737j_closure_committed"},
                "Kein autorisierter v27.37j-Implementierungs-/Abschlusszustand")
        allowed = SCOPE | (frozenset(control["V2737J_DOCUMENT_PATHS"])
                           if "closure" in phase else frozenset())
        changed = set(git("diff", "--name-only", BASE_SHA).decode("utf-8").splitlines())
        untracked = set(git("ls-files", "--others", "--exclude-standard").decode("utf-8").splitlines())
        require(changed | untracked <= allowed, "Datei außerhalb des exakten Phasenscopes verändert")
        require(not git("diff", "--cached", "--name-only").strip(), "Index muss leer bleiben")
        frozen = tuple(sorted({*control["v2737j_frozen_product_paths"](),
                               "tools/check-project-continuity-control.py"}))
        paths = (PATCH, ORAL, *frozen)
        base = {path: git("show", f"{BASE_SHA}:{path}") for path in paths}
        current = {path: (ROOT / path).read_bytes() for path in paths}
        validate_snapshot(current, base, control)
        validate_document_and_preflight()
        node = shutil.which("node")
        require(node is not None, "Node.js fehlt")
        for path in (PATCH, ORAL):
            syntax_check(node, current[path], path)
        historical = runpy.run_path(str(ROOT / "tools/check-oral-mistake-empty-state-v2737i.py"))
        passed, detail = execute(node, current, historical)
        require(passed, "Reale DOM-/Storage-Logik fehlgeschlagen:\n" + detail)
        print("Positivfälle: " + detail)

        overview = "Diese Fragen wurden in der mündlichen Vorbereitung mit"
        renderer = "Hier erscheinen Fragen, die in der mündlichen Vorbereitung mit"
        cases = []
        for label, path, anchor, replacement in (
            ("alte 15-Minuten-Simulation", PATCH, overview,
             "Diese Fragen wurden in der 15-Minuten-Simulation mit"),
            ("alte mündliche Simulation / Patch", PATCH, renderer,
             "Hier erscheinen nur Fragen, die in der mündlichen Simulation mit"),
            ("alte mündliche Simulation / Oral", ORAL, renderer,
             "Hier erscheinen nur Fragen, die in der mündlichen Simulation mit"),
            ("erfundene Themenübung", ORAL, renderer,
             "Hier erscheinen Fragen, die in einer Themenübung mit"),
            ("erfundener Prüfungsbogen", PATCH, overview,
             "Diese Fragen wurden in einem Prüfungsbogen mit"),
        ):
            cases.append((label, mutation(current, path, anchor, replacement), path, True))
        for field in ("source", "mode", "provenance"):
            cases.append(("neues " + field + "-Feld", mutation(
                current, PATCH, "      key,\n      id: question.id || key,",
                '      key,\n      ' + field + ': "simulation",\n      id: question.id || key,'
            ), PATCH, True))
        for path, version in ((PATCH, "2324"), (ORAL, "2340")):
            anchor = "  function writeOralMistakesV" + version + "(list) {"
            cases.append(("neuer Storage-Key / " + path, mutation(
                current, path, anchor,
                anchor + '\n    localStorage.setItem("accaoui_oral_shadow", "[]");'
            ), path, True))
            read_prefix = (
                '      const raw = localStorage.getItem(ORAL_MISTAKE_STORAGE_KEY_V' + version + ');\n'
                '      const parsed = JSON.parse(raw || "[]");'
            )
            anchor = read_prefix + '\n      return Array.isArray(parsed) ? parsed : [];'
            require(target_block(current[path], path).count(anchor) == 1,
                    "Migrationsanker im erlaubten Zielblock nicht eindeutig: " + path)
            cases.append(("Migration beim Lesen / " + path, mutation(
                current, path, anchor,
                read_prefix + '\n      localStorage.setItem(ORAL_MISTAKE_STORAGE_KEY_V' + version
                + ', JSON.stringify(parsed));\n      return Array.isArray(parsed) ? parsed : [];'
            ), path, True))
        cases.append(("Als sicher entfernt Fehler nicht", mutation(
            current, ORAL, "    removeOralMistakeV2340(key);", "    readOralMistakesV2340();"
        ), ORAL, True))
        cases.append(("Reveal bleibt verdeckt", mutation(
            current, ORAL, '    card.setAttribute("data-oral-mistake-open-v2340", "true");',
            '    card.setAttribute("data-oral-mistake-open-v2340", "false");'
        ), ORAL, True))
        cases.append(("v27.37i-Leerzustand ohne Neurendern", mutation(
            current, ORAL, "    if (!mistakes.length) {\n      mainContent.innerHTML =",
            "    if (!mistakes.length) {\n      const ignoredEmptyState ="
        ), ORAL, True))
        for path in (PATCH, ORAL):
            cases.append(("Änderung außerhalb Zielblock / " + path,
                          {**current, path: b"// unerlaubter Prefix\n" + current[path]}, path, False))
        cases.append(("ausgeschlossenes app.js verändert",
                      {**current, "app.js": current["app.js"] + b"\n// unerlaubte Aenderung\n"},
                      "app.js", False))
        for label, candidate, path, runtime_required in cases:
            syntax_check(node, candidate[path], label)
            if runtime_required:
                accepted, _ = execute(node, candidate, historical)
                require(not accepted, "Semantische Mutation nicht erkannt: " + label)
            try:
                validate_snapshot(candidate, base, control)
            except (ContractError, control["ValidationError"]):
                pass
            else:
                raise ContractError("Byte-/Scope-Mutation nicht erkannt: " + label)
            print("MUTATION BLOCKIERT: " + label + (" / Laufzeit" if runtime_required else " / Byte-Scope"))
        require(len(cases) == 18, "Mutationsmatrix unvollständig")
        print("v27.37j mündlicher Fehlertrainer-Herkunftshinweis: PASS")
        print("Semantische Mutationen: 18 / vollständig blockiert (15 Laufzeit, 3 Byte-Scope)")
        print(f"Frozen-Dateien: {len(frozen)} / byte-identisch zur Repair-Basis")
        print("Beide Zielblöcke: nur drei autorisierte Herkunftstexte geändert")
        print("Keine Provenienzfelder, Zusatz-Keys oder Migration; UI/Storage unverändert")
        print("Gate-Repair und historische Checker unverändert; Supabase NICHT LIVE")
        print("Phase: " + phase)
        return 0
    except (ContractError, OSError, ValueError, subprocess.SubprocessError) as exc:
        print("STOPP: v27.37j-Checker: " + str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
