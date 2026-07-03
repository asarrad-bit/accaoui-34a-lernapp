from pathlib import Path
import json
import os
import subprocess
import sys

errors = []

def run_command(command):
    result = subprocess.run(
        command,
        shell=True,
        text=True,
        capture_output=True
    )
    return result.returncode, result.stdout.strip(), result.stderr.strip()

def check_file_exists(path):
    if not Path(path).exists():
        errors.append(f"Datei fehlt: {path}")

def check_json(path):
    try:
        json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"JSON ungültig: {path} – {exc}")

def check_index_versions():
    index = Path("index.html")
    if not index.exists():
        errors.append("index.html fehlt")
        return

    text = index.read_text(encoding="utf-8")

    required_scripts = [
        "app.js",
        "patch-v21.js",
        "data/oral-question-bank.js",
        "data/oral-sheets-bank.js",
        "oral-sheets.js",
        "oral-sheets-v23.js",
        "oral-exam.js",
    ]

    for script in required_scripts:
        if script not in text:
            errors.append(f"Script fehlt in index.html: {script}")

    required_styles = [
        "style.css",
        "oral-exam.css",
    ]

    for style in required_styles:
        if style not in text:
            errors.append(f"Stylesheet fehlt in index.html: {style}")

def check_category_audit():
    code, stdout, stderr = run_command(f'"{sys.executable}" tools/audit-categories.py')

    if stdout:
        print(stdout)

    if stderr:
        print(stderr)

    if code != 0:
        errors.append("Kategorien-Audit fehlgeschlagen")

def check_git_diff_check():
    code, stdout, stderr = run_command("git diff --check")

    if stdout:
        errors.append("git diff --check meldet Probleme:\n" + stdout)

    if stderr:
        errors.append("git diff --check Fehler:\n" + stderr)

PROTECTED_CORE_FILES_V2356 = [
    "app.js",
    "patch-v21.js",
    "index.html",
    "style.css",
    "oral-exam.css",
    "oral-exam.js",
    "oral-sheets.js",
    "oral-sheets-v23.js",
    "questions.json",
    "data/oral-question-bank.js",
    "data/oral-sheets-bank.js",
]

def _parse_allowed_protected_v2356():
    raw = os.environ.get("ACCAOUI_ALLOW_PROTECTED", "").strip()
    if not raw:
        return set()

    allowed = set()
    for part in raw.split(","):
        path = part.strip().strip('"').replace("\\", "/")
        if path:
            allowed.add(path)
    return allowed

def check_protected_core_files_v2356():
    code, stdout, stderr = run_command("git status --short")

    if code != 0:
        errors.append("git status --short fehlgeschlagen")
        if stderr:
            errors.append(stderr)
        return

    allowed_protected = _parse_allowed_protected_v2356()
    changed_protected = set()

    for line in stdout.splitlines():
        line = line.strip()
        if not line:
            continue

        parts = line.split(maxsplit=1)
        if len(parts) < 2:
            continue

        path_part = parts[1].strip().strip('"')
        if " -> " in path_part:
            path_part = path_part.split(" -> ", 1)[1].strip().strip('"')

        path_part = path_part.replace("\\", "/")

        for protected in PROTECTED_CORE_FILES_V2356:
            if path_part == protected:
                changed_protected.add(protected)

    for protected in sorted(changed_protected):
        if protected in allowed_protected:
            continue
        errors.append(
            "KRITISCH: Geschützte Datei geändert: " + protected + "\n"
            "Nur committen, wenn diese Datei ausdrücklich für den aktuellen Task freigegeben wurde."
        )

def main():
    print("Accaoui Preflight läuft...\n")

    required_files = [
        "index.html",
        "app.js",
        "patch-v21.js",
        "style.css",
        "oral-exam.css",
        "oral-exam.js",
        "questions.json",
        "oral-sheets.js",
        "oral-sheets-v23.js",
        "data/oral-question-bank.js",
        "data/oral-sheets-bank.js",
        "tools/audit-categories.py",
    ]

    for file_path in required_files:
        check_file_exists(file_path)

    check_json("questions.json")
    check_index_versions()
    check_category_audit()
    check_git_diff_check()
    check_protected_core_files_v2356()

    if errors:
        print("\nPRE-FLIGHT FEHLER:")
        for error in errors:
            print(f"- {error}")
        print("\nSTOPP: NICHT COMMITTEN UND NICHT PUSHEN.")
        sys.exit(1)

    print("\nOK: Preflight bestanden.")
    print("FREIGABE: JETZT COMMITTEN UND PUSHEN.")

if __name__ == "__main__":
    main()
