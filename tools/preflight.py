from pathlib import Path
import json
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
    code, stdout, stderr = run_command("python tools/audit-categories.py")

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

    if errors:
        print("\nPRE-FLIGHT FEHLER:")
        for error in errors:
            print(f"- {error}")
        sys.exit(1)

    print("\nOK: Preflight bestanden.")

if __name__ == "__main__":
    main()
