from pathlib import Path
import json
import sys

CANONICAL_CATEGORIES = [
    "Recht der öffentlichen Sicherheit und Ordnung",
    "Gewerberecht",
    "Datenschutzrecht",
    "Bürgerliches Gesetzbuch",
    "Strafgesetzbuch und Strafverfahrensrecht",
    "Unfallverhütungsvorschriften Wach- und Sicherungsdienste",
    "Umgang mit Waffen",
    "Umgang mit Menschen",
    "Grundzüge der Sicherheitstechnik",
]

LEGACY_CATEGORIES = [
    "Bürgerliches Recht",
    "Straf- und Strafverfahrensrecht",
    "Unfallverhütungsvorschrift",
    "Unfallverhütungsvorschrift Wach- und Sicherungsdienste",
    "Grundzüge des Waffenrechts",
]

FILES_THAT_MUST_NOT_CONTAIN_LEGACY = [
    "questions.json",
    "patch-v21.js",
    "oral-sheets-v23.js",
    "data/oral-question-bank.js",
    "data/oral-sheets-bank.js",
]

errors = []

def read_text(path):
    return Path(path).read_text(encoding="utf-8")

def check_no_legacy_terms():
    for file_path in FILES_THAT_MUST_NOT_CONTAIN_LEGACY:
        path = Path(file_path)
        if not path.exists():
            errors.append(f"Datei fehlt: {file_path}")
            continue

        text = read_text(path)
        for legacy in LEGACY_CATEGORIES:
            exact_patterns = [
                f'"category": "{legacy}"',
                f'category: "{legacy}"',
                f'"topic": "{legacy}"',
                f'topic: "{legacy}"',
                f'"{legacy}",',
            ]

            for pattern in exact_patterns:
                if pattern in text:
                    errors.append(f"Alte Kategorie gefunden in {file_path}: {legacy}")
                    break

def check_questions_json():
    path = Path("questions.json")
    if not path.exists():
        errors.append("questions.json fehlt")
        return

    try:
        questions = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"questions.json ist kein gültiges JSON: {exc}")
        return

    if not isinstance(questions, list):
        errors.append("questions.json muss eine Liste sein")
        return

    counts = {category: 0 for category in CANONICAL_CATEGORIES}

    for index, question in enumerate(questions, start=1):
        category = question.get("category")
        if category not in CANONICAL_CATEGORIES:
            errors.append(f"questions.json Eintrag {index}: ungültige Kategorie: {category!r}")
        else:
            counts[category] += 1

    print("Kategorie-Verteilung in questions.json:")
    for category in CANONICAL_CATEGORIES:
        print(f"- {category}: {counts[category]}")

def check_app_mapping_exists():
    path = Path("app.js")
    if not path.exists():
        errors.append("app.js fehlt")
        return

    text = read_text(path)

    required_mappings = [
        '"Bürgerliches Recht": "Bürgerliches Gesetzbuch"',
        '"Straf- und Strafverfahrensrecht": "Strafgesetzbuch und Strafverfahrensrecht"',
        '"Grundzüge des Waffenrechts": "Umgang mit Waffen"',
        '"Unfallverhütungsvorschrift Wach- und Sicherungsdienste": "Unfallverhütungsvorschriften Wach- und Sicherungsdienste"',
    ]

    for mapping in required_mappings:
        if mapping not in text:
            errors.append(f"Mapping fehlt in app.js: {mapping}")

def main():
    check_no_legacy_terms()
    check_questions_json()
    check_app_mapping_exists()

    if errors:
        print("\nFEHLER GEFUNDEN:")
        for error in errors:
            print(f"- {error}")
        sys.exit(1)

    print("\nOK: Kategorien-Audit bestanden.")

if __name__ == "__main__":
    main()
