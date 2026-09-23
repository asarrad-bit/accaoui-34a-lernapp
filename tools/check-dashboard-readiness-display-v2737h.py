#!/usr/bin/env python3
"""Strict v27.37h dashboard-readiness implementation checker."""

from __future__ import annotations

import ast
import re
import runpy
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path


sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
BASE_SHA = "f39b2708421ce85e7fe9e45fe2482af2fad0f255"
OLD_BOX = (
    b'      <div class="score-box">\n'
    b'        <span>Bereitschaft</span>\n'
    b'        <strong>72%</strong>\n'
    b'      </div>\n'
)
EXPECTED_BOX = (
    b'      <div class="score-box">\n'
    b'        <span>Bereitschaft</span>\n'
    b'        <strong>Nicht berechnet</strong>\n'
    b'      </div>\n'
)
FROZEN_PATHS = (
    "app.js", "style.css", "patch-v21.js", "test/index.html",
    "data/supabase-participant-access-browser-loader.js",
    "data/supabase-participant-auth-session-browser-loader.js",
)
ACCESS_LOADER_ID = "accaoui-participant-access-browser-loader"
AUTH_LOADER_ID = "accaoui-participant-auth-session-browser-loader"


class ContractError(RuntimeError):
    pass


class StructureParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.boxes = []
        self.active = None
        self.depth = 0
        self.scripts = []

    def handle_starttag(self, tag, attrs):
        attrs_tuple = tuple(attrs)
        attrs_map = dict(attrs)
        if tag == "script":
            self.scripts.append(attrs_tuple)
        classes = (attrs_map.get("class") or "").split()
        if tag == "div" and "score-box" in classes:
            if self.active is not None:
                raise ContractError("verschachtelte score-box")
            self.active = {"attrs": attrs_tuple, "events": []}
            self.depth = 1
            self.boxes.append(self.active)
            return
        if self.active is not None:
            self.active["events"].append(("start", tag, attrs_tuple))
            self.depth += 1

    def handle_endtag(self, tag):
        if self.active is None:
            return
        if tag == "div" and self.depth == 1:
            self.active = None
            self.depth = 0
            return
        self.active["events"].append(("end", tag))
        self.depth -= 1

    def handle_data(self, data):
        if self.active is not None and data.strip():
            self.active["events"].append(("text", data.strip()))


def git_blob(path: str) -> bytes:
    result = subprocess.run(
        ["git", "show", f"{BASE_SHA}:{path}"], cwd=ROOT,
        capture_output=True, check=False,
    )
    if result.returncode:
        raise ContractError("Basis-Blob nicht lesbar: " + path)
    return result.stdout


def snapshot() -> dict[str, bytes]:
    paths = ("index.html", *FROZEN_PATHS)
    return {path: (ROOT / path).read_bytes() for path in paths}


def baselines() -> dict[str, bytes]:
    paths = ("index.html", *FROZEN_PATHS)
    return {path: git_blob(path) for path in paths}


def parse_index(data: bytes) -> StructureParser:
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ContractError("index.html ist kein striktes UTF-8") from exc
    parser = StructureParser()
    parser.feed(text)
    parser.close()
    return parser


def loader_attributes(parser: StructureParser, loader_id: str):
    matches = [attrs for attrs in parser.scripts if dict(attrs).get("id") == loader_id]
    if len(matches) != 1:
        raise ContractError("Loader-Script nicht exakt einmal: " + loader_id)
    attrs = dict(matches[0])
    if attrs.get("data-enabled") != "false":
        raise ContractError("Loader nicht exakt deaktiviert: " + loader_id)
    return matches[0]


def validate(current: dict[str, bytes], base: dict[str, bytes]) -> None:
    if set(current) != set(base) or set(current) != {"index.html", *FROZEN_PATHS}:
        raise ContractError("Snapshot-Scope unvollständig")
    for path in FROZEN_PATHS:
        if current[path] != base[path]:
            raise ContractError("Frozen-Datei verändert: " + path)

    base_index = base["index.html"]
    current_index = current["index.html"]
    if base_index.count(OLD_BOX) != 1 or EXPECTED_BOX in base_index:
        raise ContractError("Implementierungsbasis enthält keinen eindeutigen 72-%-Block")
    expected_index = base_index.replace(OLD_BOX, EXPECTED_BOX, 1)
    if current_index != expected_index:
        raise ContractError("index.html außerhalb der exakten score-box-Änderung verändert")
    if current_index.count(EXPECTED_BOX) != 1 or OLD_BOX in current_index:
        raise ContractError("Bereitschaftsblock nicht exakt ersetzt")

    parser = parse_index(current_index)
    base_parser = parse_index(base_index)
    if len(parser.boxes) != 1:
        raise ContractError("score-box existiert nicht exakt einmal")
    box = parser.boxes[0]
    if box["attrs"] != (("class", "score-box"),):
        raise ContractError("score-box-Attribute verändert")
    expected_events = [
        ("start", "span", ()), ("text", "Bereitschaft"), ("end", "span"),
        ("start", "strong", ()), ("text", "Nicht berechnet"), ("end", "strong"),
    ]
    if box["events"] != expected_events:
        raise ContractError("score-box-Struktur, Label oder Wert verletzt")
    if any("%" in event[1] for event in box["events"] if event[0] == "text"):
        raise ContractError("Prozentwert im Bereitschaftsbereich")
    if parser.scripts != base_parser.scripts:
        raise ContractError("Script-Reihenfolge, Attribute oder Querystring verändert")
    for loader_id in (ACCESS_LOADER_ID, AUTH_LOADER_ID):
        if loader_attributes(parser, loader_id) != loader_attributes(base_parser, loader_id):
            raise ContractError("Loader-Einbindung verändert: " + loader_id)


def changed(source: dict[str, bytes], path: str, before: bytes, after: bytes) -> dict[str, bytes]:
    if source[path].count(before) != 1:
        raise RuntimeError("Mutationsanker uneindeutig: " + path + " / " + repr(before))
    result = dict(source)
    result[path] = source[path].replace(before, after, 1)
    return result


def enable_loader(index: bytes, loader_id: str) -> bytes:
    pattern = (
        rb'<script\b[^>]*\bid="' + re.escape(loader_id.encode("ascii"))
        + rb'"[^>]*></script>'
    )
    matches = list(re.finditer(pattern, index))
    if len(matches) != 1:
        raise RuntimeError(
            f"Loader-Tag nicht eindeutig für Mutation: {loader_id} / {len(matches)} Treffer"
        )
    match = matches[0]
    tag = match.group(0)
    disabled = b'data-enabled="false"'
    if tag.count(disabled) != 1 or b'data-enabled="true"' in tag:
        raise RuntimeError("Loader-Aktivierungsattribut nicht eindeutig: " + loader_id)
    changed_tag = tag.replace(disabled, b'data-enabled="true"', 1)
    return index[:match.start()] + changed_tag + index[match.end():]


def mutation_cases(good: dict[str, bytes], base: dict[str, bytes]):
    yield "72 percent remains", {**good, "index.html": base["index.html"]}
    yield "50 percent", changed(good, "index.html", b"Nicht berechnet", b"50%")
    yield "missing neutral value", changed(good, "index.html", b"Nicht berechnet", b"")
    yield "missing readiness label", changed(good, "index.html", b"Bereitschaft", b"Status")
    yield "dynamic calculation", changed(
        good, "index.html", b"<strong>Nicht berechnet</strong>",
        b'<strong id="readiness"></strong><script>readiness.textContent="50%"</script>')
    yield "outside score box", {**good, "index.html": good["index.html"] + b"<!-- drift -->\n"}
    yield "app changed", {**good, "app.js": good["app.js"] + b"\n// drift"}
    yield "style changed", {**good, "style.css": good["style.css"] + b"\n/* drift */"}
    yield "patch changed", {**good, "patch-v21.js": good["patch-v21.js"] + b"\n// drift"}
    yield "test index changed", {**good, "test/index.html": good["test/index.html"] + b"\x00"}
    yield "access loader enabled", {
        **good, "index.html": enable_loader(good["index.html"], ACCESS_LOADER_ID)
    }
    yield "auth loader enabled", {
        **good, "index.html": enable_loader(good["index.html"], AUTH_LOADER_ID)
    }
    yield "app query changed", changed(good, "index.html", b"app.js?v=24.8", b"app.js?v=24.9")


def main() -> None:
    control = runpy.run_path(str(ROOT / "tools/check-project-continuity-control.py"))
    phase = control["detect_v2737h_phase"]()
    if phase not in {
        "v2737h_implementation_prepared", "v2737h_implementation_committed",
        "v2737h_closure_prepared", "v2737h_closure_committed",
    }:
        raise RuntimeError("Unerwartete v27.37h-Phase: " + str(phase))
    base = baselines()
    good = snapshot()
    validate(good, base)
    blocked = 0
    for name, mutation in mutation_cases(good, base):
        try:
            validate(mutation, base)
        except ContractError:
            blocked += 1
            print("MUTATION BLOCKIERT: " + name)
        else:
            raise RuntimeError("Mutation nicht erkannt: " + name)
    if blocked != 13:
        raise RuntimeError("Unvollständige Mutationsmatrix")
    print("v27.37h Dashboard-Bereitschaftsanzeige: PASS")
    print("Strukturprüfung: score-box exakt einmal, Label/Wert exakt / PASS")
    print("Frozen-Dateien: byte-identisch / PASS")
    print("Script-Reihenfolge, Querystrings und beide deaktivierten Loader / PASS")
    print(f"Semantische Mutationen: {blocked} / vollständig blockiert")
    print("Keine Bereitschaftsberechnung, Storage-, Netzwerk-, Auth- oder Supabase-Logik")
    print("Phase: " + phase)


if __name__ == "__main__":
    main()
