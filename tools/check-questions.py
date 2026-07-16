from collections import Counter
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
QUESTIONS_FILE = ROOT / "questions.json"

CANONICAL_CATEGORIES = (
    "Recht der öffentlichen Sicherheit und Ordnung",
    "Gewerberecht",
    "Datenschutzrecht",
    "Bürgerliches Gesetzbuch",
    "Strafgesetzbuch und Strafverfahrensrecht",
    "Unfallverhütungsvorschriften Wach- und Sicherungsdienste",
    "Umgang mit Waffen",
    "Umgang mit Menschen",
    "Grundzüge der Sicherheitstechnik",
)

ALLOWED_QUESTION_TYPES = (
    "single",
    "multiple",
    "praxisfall",
    "combination",
)

SINGLE_ANSWER_TYPES = (
    "single",
    "combination",
)

CORE_IDS = """
roso_001 roso_002 roso_003 roso_005
v23_roso_006 v23_roso_007 v23_roso_008
gewo_002 gewo_004 v23_gewo_006 v23_gewo_007 v23_gewo_008
ds_001 ds_002 ds_003 ds_004 ds_005
bgb_001 bgb_002 bgb_003 bgb_004 bgb_005 bgb_006 bgb_007
bgb_008 bgb_009 bgb_010 bgb_011 bgb_012 bgb_013
straf_001 straf_002 straf_003 straf_004 straf_005 straf_006
straf_007 straf_008 straf_009 straf_010 straf_011 straf_012
straf_013
uvv_001 uvv_002 uvv_003 uvv_004 uvv_005 uvv_006 uvv_007
uvv_008
waffen_001 waffen_002 waffen_003 waffen_004 waffen_005
umgang_001 umgang_002 umgang_003 umgang_004 umgang_005
umgang_006 umgang_007 umgang_008 umgang_009 umgang_010
umgang_011 umgang_012 umgang_013 umgang_014 umgang_015
umgang_016 umgang_017 umgang_018 umgang_019
technik_001 technik_002 technik_003 technik_004 technik_005
technik_006 technik_007
""".split()

EXPECTED_CORE_COUNTS = {
    "Recht der öffentlichen Sicherheit und Ordnung": 7,
    "Gewerberecht": 5,
    "Datenschutzrecht": 5,
    "Bürgerliches Gesetzbuch": 13,
    "Strafgesetzbuch und Strafverfahrensrecht": 13,
    "Unfallverhütungsvorschriften Wach- und Sicherungsdienste": 8,
    "Umgang mit Waffen": 5,
    "Umgang mit Menschen": 19,
    "Grundzüge der Sicherheitstechnik": 7,
}

REQUIRED_FIELDS = (
    "id",
    "category",
    "type",
    "points",
    "question",
    "answers",
    "correct",
    "explanation",
)

errors = []


def add_error(message):
    errors.append(message)


def is_integer(value):
    return isinstance(value, int) and not isinstance(value, bool)


if not QUESTIONS_FILE.is_file():
    print("FEHLER: questions.json fehlt.")
    sys.exit(1)

try:
    questions = json.loads(
        QUESTIONS_FILE.read_text(encoding="utf-8")
    )
except Exception as exc:
    print(f"FEHLER: questions.json ist ungültig: {exc}")
    sys.exit(1)

if not isinstance(questions, list):
    print("FEHLER: questions.json muss eine Liste sein.")
    sys.exit(1)

questions_by_id = {}
pool_categories = Counter()
question_types = Counter()

for position, item in enumerate(questions, start=1):
    label = f"Eintrag {position}"

    if not isinstance(item, dict):
        add_error(f"{label}: muss ein Objekt sein")
        continue

    missing = [
        field for field in REQUIRED_FIELDS
        if field not in item
    ]

    if missing:
        add_error(f"{label}: Felder fehlen: {missing}")

    question_id = item.get("id")

    if not isinstance(question_id, str) or not question_id.strip():
        add_error(f"{label}: ungültige ID")
        question_id = label
    elif question_id in questions_by_id:
        add_error(f"Doppelte Fragen-ID: {question_id}")
    else:
        questions_by_id[question_id] = item

    category = item.get("category")

    if category not in CANONICAL_CATEGORIES:
        add_error(
            f"{question_id}: ungültige Kategorie: "
            f"{category!r}"
        )
    else:
        pool_categories[category] += 1

    question_type = item.get("type")

    if question_type not in ALLOWED_QUESTION_TYPES:
        add_error(
            f"{question_id}: ungültiger Typ: "
            f"{question_type!r}"
        )
    else:
        question_types[question_type] += 1

    points = item.get("points")

    if not is_integer(points) or points not in (1, 2):
        add_error(
            f"{question_id}: Punkte müssen 1 oder 2 sein"
        )

    question_text = item.get("question")

    if (
        not isinstance(question_text, str)
        or not question_text.strip()
    ):
        add_error(f"{question_id}: Fragetext fehlt")

    answers = item.get("answers")
    answers_valid = (
        isinstance(answers, list)
        and len(answers) >= 2
        and all(
            isinstance(answer, str) and answer.strip()
            for answer in answers
        )
    )

    if not answers_valid:
        add_error(
            f"{question_id}: mindestens zwei gültige "
            "Antworten erforderlich"
        )

    correct = item.get("correct")
    correct_valid = (
        isinstance(correct, list)
        and len(correct) >= 1
        and all(is_integer(index) for index in correct)
    )

    if not correct_valid:
        add_error(
            f"{question_id}: correct muss eine "
            "nichtleere Indexliste sein"
        )
    else:
        if len(correct) != len(set(correct)):
            add_error(
                f"{question_id}: doppelte richtige Indizes"
            )

        if answers_valid:
            invalid_indexes = [
                index for index in correct
                if index < 0 or index >= len(answers)
            ]

            if invalid_indexes:
                add_error(
                    f"{question_id}: ungültige "
                    f"Antwortindizes: {invalid_indexes}"
                )

        if (
            question_type in SINGLE_ANSWER_TYPES
            and len(correct) != 1
        ):
            add_error(
                f"{question_id}: {question_type} braucht "
                "genau eine richtige Antwort"
            )

    explanation = item.get("explanation")

    if not isinstance(explanation, str):
        add_error(
            f"{question_id}: Erklärung muss Text sein"
        )

if len(CORE_IDS) != 82:
    add_error(
        f"Interner Core-Plan enthält {len(CORE_IDS)} "
        "statt 82 IDs"
    )

if len(set(CORE_IDS)) != len(CORE_IDS):
    add_error("Interner Core-Plan enthält doppelte IDs")

missing_core_ids = [
    question_id for question_id in CORE_IDS
    if question_id not in questions_by_id
]

if missing_core_ids:
    add_error(
        f"Core-Fragen fehlen: {missing_core_ids}"
    )

core_points = 0
core_categories = Counter()

for question_id in CORE_IDS:
    question = questions_by_id.get(question_id)

    if not question:
        continue

    points = question.get("points")
    category = question.get("category")

    if is_integer(points):
        core_points += points

    if category in CANONICAL_CATEGORIES:
        core_categories[category] += 1

if core_points != 120:
    add_error(
        f"Core-Punkte: {core_points} statt 120"
    )

for category, expected_count in EXPECTED_CORE_COUNTS.items():
    actual_count = core_categories[category]

    if actual_count != expected_count:
        add_error(
            f"Core-Kategorie {category}: "
            f"{actual_count} statt {expected_count}"
        )

if errors:
    print("Fragenbankprüfung: FEHLER")

    for message in errors:
        print(f"- {message}")

    sys.exit(1)

reserve_count = len(questions) - len(CORE_IDS)

print("Fragenbankprüfung: OK")
print(f"Fragen gesamt: {len(questions)}")
print(f"Core-Fragen: {len(CORE_IDS)}")
print(f"Core-Punkte: {core_points}")
print(f"Reservefragen: {reserve_count}")
print(f"Kanonische Kategorien: {len(CANONICAL_CATEGORIES)}")
print("Fragetypen:")

for question_type in ALLOWED_QUESTION_TYPES:
    print(f"- {question_type}: {question_types[question_type]}")

print("Datenbankverbindung: nein")
print("Live-Import: nein")
