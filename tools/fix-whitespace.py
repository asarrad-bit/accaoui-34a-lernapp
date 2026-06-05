#!/usr/bin/env python3
"""
Bereinigt trailing Whitespace und normalisiert Zeilenenden auf LF.

Standardbereiche (keine App-Kerndateien):
  - docs/**/*.md
  - README.md
  - questions.json
  - tools/**/*.py
"""

from __future__ import annotations

from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent

PROTECTED_FILENAMES = {
    "app.js",
    "patch-v21.js",
    "index.html",
    "style.css",
    "oral-exam.css",
    "oral-exam.js",
    "oral-sheets.js",
    "oral-sheets-v23.js",
}

PROTECTED_PREFIXES = (
    "data/",
    "test/",
)

DEFAULT_GLOBS = (
    "docs/**/*.md",
    "README.md",
    "questions.json",
    "tools/**/*.py",
)


def is_protected(relative_posix: str) -> bool:
    name = Path(relative_posix).name
    if name in PROTECTED_FILENAMES:
        return True
    for prefix in PROTECTED_PREFIXES:
        if relative_posix == prefix.rstrip("/") or relative_posix.startswith(prefix):
            return True
    return False


def collect_target_files(root: Path) -> list[Path]:
    found: set[Path] = set()
    for pattern in DEFAULT_GLOBS:
        for path in root.glob(pattern):
            if not path.is_file():
                continue
            rel = path.relative_to(root).as_posix()
            if is_protected(rel):
                continue
            found.add(path.resolve())
    return sorted(found)


def normalize_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    ends_with_newline = text.endswith("\n")
    lines = text.split("\n")
    if ends_with_newline and lines and lines[-1] == "":
        lines = lines[:-1]
    fixed_lines = [line.rstrip(" \t") for line in lines]
    result = "\n".join(fixed_lines)
    if ends_with_newline:
        result += "\n"
    return result


def needs_fix(original: str) -> bool:
    if "\r" in original:
        return True
    normalized = original.replace("\r\n", "\n").replace("\r", "\n")
    return any(line != line.rstrip(" \t") for line in normalized.split("\n"))


def fix_file(path: Path) -> bool:
    raw = path.read_bytes()
    try:
        original = raw.decode("utf-8")
    except UnicodeDecodeError:
        rel = path.relative_to(REPO_ROOT).as_posix()
        print(f"Übersprungen (kein UTF-8-Text): {rel}")
        return False

    if not needs_fix(original):
        return False

    fixed = normalize_text(original)
    path.write_text(fixed, encoding="utf-8", newline="\n")
    return True


def main() -> int:
    root = REPO_ROOT
    targets = collect_target_files(root)
    cleaned: list[str] = []

    for path in targets:
        if fix_file(path):
            cleaned.append(path.relative_to(root).as_posix())

    if not cleaned:
        print("OK: Keine Whitespace-Probleme gefunden.")
        return 0

    print("Bereinigt:")
    for rel in cleaned:
        print(f"- {rel}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
