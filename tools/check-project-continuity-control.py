#!/usr/bin/env python3
"""Prüft die verbindliche Projektkontinuität und Task-Steuerung v27.34c."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Callable


ROOT = Path(__file__).resolve().parents[1]
AGENTS_PATH = ROOT / "AGENTS.md"
MASTERLIST_PATH = ROOT / "docs" / "PROJECT_MASTERLIST.md"
STATE_PATH = ROOT / "docs" / "PROJECT_STATE_CURRENT.md"
TASK_PATH = ROOT / "docs" / "tasks" / "CURRENT_TASK.md"
PREFLIGHT_PATH = ROOT / "tools" / "preflight.py"

PREDECESSOR_SHA = "1bc29a7d522c4c2d67134a946ac5d3f9b1199f11"
CHECKER_RELATIVE_PATH = "tools/check-project-continuity-control.py"

EXPECTED_STATE_FIELDS = {
    "Stand": "v27.34c",
    "Repository": "`asarrad-bit/accaoui-34a-lernapp`",
    "Branch": "`main`",
    "Letzter abgeschlossener funktionaler Stand": "v27.34b",
    "Letzter direkt bestätigter Vorgänger-Commit": f"`{PREDECESSOR_SHA}`",
    "Aktueller HEAD": "DYNAMISCH ZU PRÜFEN",
    "Funktionsstatus": "v27.34b abgeschlossen",
    "Weiterer funktionaler Schritt autorisiert": "NEIN",
    "Aktueller Blocker": (
        "Auswahl durch Projekteigentümer und verbindlichen Projektchat"
    ),
}

EXPECTED_TASK_FIELDS = {
    "Task-ID": "NONE",
    "Status": "BLOCKED",
    "Autorisiert": "NEIN",
    "Funktionaler Ausgangsstand": "v27.34b",
    "Erlaubte Dateien": "KEINE",
    "Commit erlaubt": "NEIN",
    "Push erlaubt": "NEIN",
}

STATE_REQUIRED_MARKERS = (
    "## Dynamische Prüfung bei jedem Arbeitsbeginn",
    "Der aktuelle HEAD muss bei jedem Arbeitsbeginn mit Git neu ermittelt werden.",
    "Der GitHub-Stand von `refs/heads/main` muss direkt geprüft werden.",
    "Lokaler HEAD und GitHub-HEAD müssen vor Änderungen übereinstimmen.",
    "Ein zukünftiger oder selbstreferenzieller Commit-SHA darf nicht vorab eingetragen werden.",
    "## Weiterhin verboten",
    "echter Registry-Adapter",
    "PostgreSQL",
    "Datenbank",
    "SQL",
    "Supabase und Live-Supabase",
    "Netzwerk",
    "`authorizationGrant`",
    "`authorizationToken`",
    "`executionGrant`",
    "## Verbindliches Verfahren beim Chatwechsel",
    "`docs/PROJECT_STATE_CURRENT.md`",
    "`docs/PROJECT_MASTERLIST.md`",
    "`docs/tasks/CURRENT_TASK.md`",
    "GitHub-HEAD für `refs/heads/main` direkt prüfen.",
    "Bei Abweichung oder Widerspruch sofort STOPP.",
    "## Aktualisierungspflicht nach jedem Versionsabschluss",
    "Nach jedem Versionsabschluss müssen Projektzustand, Masterliste und Task-Steuerung",
)

TASK_REQUIRED_MARKERS = (
    "## Verbindliche Sperre",
    "Es ist kein weiterer funktionaler Schritt autorisiert.",
    "Der nächste Task darf ausschließlich durch den Projekteigentümer und den verbindlichen Projektchat ausgewählt werden.",
    "`v27.34d` wird nicht automatisch gewählt oder autorisiert.",
    "Aus Versionsfolgen, früheren Chats oder Erinnerung darf kein Task abgeleitet werden.",
    "## Pflichtfelder eines später autorisierten Tasks",
)

LATER_TASK_TEMPLATE_FIELDS = (
    "Task-ID",
    "Ziel",
    "Erwarteter Ausgangsstand",
    "Erlaubte Dateien",
    "Verbotene Dateien",
    "Akzeptanzkriterien",
    "Tests",
    "Commit-Freigabe",
    "Push-Freigabe",
)

AGENTS_REQUIRED_MARKERS = (
    "Vor jeder Arbeit müssen vollständig gelesen werden:",
    "  - `docs/PROJECT_STATE_CURRENT.md`",
    "  - `docs/PROJECT_MASTERLIST.md`",
    "  - `docs/tasks/CURRENT_TASK.md`",
    "Kein Task darf aus Versionsfolgen, früheren Chats oder Erinnerung abgeleitet werden.",
    "Eine Umsetzung ist nur zulässig, wenn `docs/tasks/CURRENT_TASK.md` den Task ausdrücklich autorisiert.",
    "Bei einem Widerspruch zwischen den verbindlichen Projektdateien sofort STOPP.",
    "Bei einem Chatwechsel muss der neue Chat den GitHub-HEAD direkt prüfen.",
    "Lokaler Arbeitsbaum und GitHub-Stand müssen vor Änderungen bestätigt werden.",
)

MASTERLIST_REQUIRED_MARKERS = (
    "| v27.34c |",
    "Projektkontinuität und verbindliche Task-Steuerung v27.34c",
    "- Verbindlicher Projektzustand: `docs/PROJECT_STATE_CURRENT.md`",
    "- Verbindliche Task-Steuerung: `docs/tasks/CURRENT_TASK.md`",
    "`CURRENT_TASK` ist aktuell `BLOCKED`",
    "`Task-ID` ist `NONE`",
    "`Autorisiert` ist `NEIN`",
    "Es ist kein funktionaler Folgeschritt ausgewählt oder autorisiert.",
    "Diese Bestands- und Backlogliste ist keine Task-Autorisierung.",
)


class ValidationError(RuntimeError):
    """Ein verbindlicher Kontinuitätsvertrag ist verletzt."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def read_required_text(path: Path) -> str:
    require(path.is_file(), f"Pflichtdatei fehlt: {path.relative_to(ROOT)}")
    raw = path.read_bytes()
    require(not raw.startswith(b"\xef\xbb\xbf"), f"UTF-8-BOM unzulässig: {path}")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValidationError(f"Datei ist nicht gültig UTF-8: {path}: {exc}") from exc
    require(text.endswith("\n"), f"Abschließender Zeilenumbruch fehlt: {path}")
    return text


def exact_field(text: str, field_name: str) -> str:
    matches = re.findall(
        rf"(?m)^{re.escape(field_name)}: ([^\r\n]+)$",
        text,
    )
    require(
        len(matches) == 1,
        f"Feld muss exakt einmal vorhanden sein: {field_name}",
    )
    return matches[0]


def validate_exact_fields(text: str, expected_fields: dict[str, str]) -> None:
    for field_name, expected_value in expected_fields.items():
        actual_value = exact_field(text, field_name)
        require(
            actual_value == expected_value,
            (
                f"Feldwert abweichend: {field_name}; "
                f"erwartet {expected_value!r}, erhalten {actual_value!r}"
            ),
        )


def validate_required_markers(
    text: str,
    markers: tuple[str, ...],
    document_name: str,
) -> None:
    for marker in markers:
        require(
            marker in text,
            f"{document_name}: Pflichtaussage fehlt: {marker}",
        )


def validate_state_text(text: str) -> None:
    validate_exact_fields(text, EXPECTED_STATE_FIELDS)
    validate_required_markers(text, STATE_REQUIRED_MARKERS, "PROJECT_STATE_CURRENT")

    commit_shas = set(re.findall(r"\b[0-9a-f]{40}\b", text))
    require(
        commit_shas == {PREDECESSOR_SHA},
        "PROJECT_STATE_CURRENT darf nur den direkt bestätigten Vorgänger-Commit enthalten",
    )
    require(
        "Weiterer funktionaler Schritt autorisiert: JA" not in text,
        "PROJECT_STATE_CURRENT enthält eine widersprüchliche Funktionsfreigabe",
    )


def validate_task_text(text: str) -> None:
    validate_exact_fields(text, EXPECTED_TASK_FIELDS)
    validate_required_markers(text, TASK_REQUIRED_MARKERS, "CURRENT_TASK")

    for field_name in LATER_TASK_TEMPLATE_FIELDS:
        require(
            f"- {field_name}" in text,
            f"CURRENT_TASK: Pflichtfeld der späteren Task-Vorlage fehlt: {field_name}",
        )

    require(
        text.count("v27.34d") == 1,
        "CURRENT_TASK darf v27.34d ausschließlich in der Nichtauswahl-Regel nennen",
    )
    contradictory_grants = (
        "Autorisiert: JA",
        "Commit erlaubt: JA",
        "Push erlaubt: JA",
    )
    for contradictory_grant in contradictory_grants:
        require(
            contradictory_grant not in text,
            f"CURRENT_TASK enthält widersprüchliche Freigabe: {contradictory_grant}",
        )


def validate_agents_text(text: str) -> None:
    validate_required_markers(text, AGENTS_REQUIRED_MARKERS, "AGENTS.md")


def validate_masterlist_text(text: str) -> None:
    require(
        exact_field(text, "Stand") == "v27.34c",
        "Masterliste muss exakt auf Stand v27.34c stehen",
    )
    validate_required_markers(
        text,
        MASTERLIST_REQUIRED_MARKERS,
        "PROJECT_MASTERLIST",
    )
    require(
        "v27.34d" not in text,
        "Masterliste darf keinen funktionalen Schritt v27.34d auswählen",
    )


def validate_preflight_text(text: str) -> None:
    require(
        text.count(CHECKER_RELATIVE_PATH) >= 2,
        "Preflight muss den Kontinuitäts-Checker ausführen und als Pflichtdatei führen",
    )
    require(
        "def check_project_continuity_control():" in text,
        "Preflight-Funktion für den Kontinuitäts-Checker fehlt",
    )
    require(
        text.count("check_project_continuity_control()") == 2,
        "Kontinuitäts-Checker muss im Preflight exakt einmal aufgerufen werden",
    )
    for required_path in (
        "docs/PROJECT_STATE_CURRENT.md",
        "docs/tasks/CURRENT_TASK.md",
        CHECKER_RELATIVE_PATH,
    ):
        require(
            required_path in text,
            f"Preflight-Pflichtdatei fehlt: {required_path}",
        )


def changed_once(text: str, old: str, new: str, label: str) -> str:
    require(old in text, f"Manipulationsmatrix kann Ausgangswert nicht finden: {label}")
    changed = text.replace(old, new, 1)
    require(changed != text, f"Manipulationsmatrix blieb wirkungslos: {label}")
    return changed


def must_reject(
    validator: Callable[[str], None],
    manipulated_text: str,
    label: str,
) -> None:
    try:
        validator(manipulated_text)
    except ValidationError:
        return
    raise ValidationError(f"Manipulation wurde nicht blockiert: {label}")


def run_manipulation_matrix(
    state_text: str,
    task_text: str,
    agents_text: str,
    masterlist_text: str,
) -> int:
    checks = 0

    for field_name, expected_value in EXPECTED_STATE_FIELDS.items():
        exact_line = f"{field_name}: {expected_value}\n"
        must_reject(
            validate_state_text,
            changed_once(
                state_text,
                exact_line,
                "",
                f"PROJECT_STATE_CURRENT Feld fehlt: {field_name}",
            ),
            f"PROJECT_STATE_CURRENT Feld fehlt: {field_name}",
        )
        checks += 1

    state_value_manipulations = {
        "Stand": "v27.34d",
        "Repository": "`anderes/repository`",
        "Branch": "`anderer-branch`",
        "Letzter abgeschlossener funktionaler Stand": "v27.34c",
        "Letzter direkt bestätigter Vorgänger-Commit": f"`{'0' * 40}`",
        "Aktueller HEAD": PREDECESSOR_SHA,
        "Funktionsstatus": "v27.34b offen",
        "Weiterer funktionaler Schritt autorisiert": "JA",
        "Aktueller Blocker": "KEINER",
    }
    for field_name, manipulated_value in state_value_manipulations.items():
        expected_value = EXPECTED_STATE_FIELDS[field_name]
        must_reject(
            validate_state_text,
            changed_once(
                state_text,
                f"{field_name}: {expected_value}",
                f"{field_name}: {manipulated_value}",
                f"PROJECT_STATE_CURRENT Feld manipuliert: {field_name}",
            ),
            f"PROJECT_STATE_CURRENT Feld manipuliert: {field_name}",
        )
        checks += 1

    for field_name, expected_value in EXPECTED_TASK_FIELDS.items():
        exact_line = f"{field_name}: {expected_value}\n"
        must_reject(
            validate_task_text,
            changed_once(
                task_text,
                exact_line,
                "",
                f"CURRENT_TASK Feld fehlt: {field_name}",
            ),
            f"CURRENT_TASK Feld fehlt: {field_name}",
        )
        checks += 1

    task_value_manipulations = {
        "Task-ID": "v27.34d",
        "Status": "AUTHORIZED",
        "Autorisiert": "JA",
        "Funktionaler Ausgangsstand": "v27.34c",
        "Erlaubte Dateien": "AGENTS.md",
        "Commit erlaubt": "JA",
        "Push erlaubt": "JA",
    }
    for field_name, manipulated_value in task_value_manipulations.items():
        expected_value = EXPECTED_TASK_FIELDS[field_name]
        must_reject(
            validate_task_text,
            changed_once(
                task_text,
                f"{field_name}: {expected_value}",
                f"{field_name}: {manipulated_value}",
                f"CURRENT_TASK Feld manipuliert: {field_name}",
            ),
            f"CURRENT_TASK Feld manipuliert: {field_name}",
        )
        checks += 1

    for contradictory_grant in (
        "Autorisiert: JA",
        "Commit erlaubt: JA",
        "Push erlaubt: JA",
        "Erlaubte Dateien: AGENTS.md",
    ):
        must_reject(
            validate_task_text,
            task_text + f"{contradictory_grant}\n",
            f"CURRENT_TASK widersprüchliche Freigabe: {contradictory_grant}",
        )
        checks += 1

    for field_name in LATER_TASK_TEMPLATE_FIELDS:
        must_reject(
            validate_task_text,
            changed_once(
                task_text,
                f"- {field_name}\n",
                "",
                f"CURRENT_TASK Vorlagenfeld fehlt: {field_name}",
            ),
            f"CURRENT_TASK Vorlagenfeld fehlt: {field_name}",
        )
        checks += 1

    must_reject(
        validate_task_text,
        changed_once(
            task_text,
            "`v27.34d` wird nicht automatisch gewählt oder autorisiert.",
            "`v27.34d` wird automatisch gewählt und autorisiert.",
            "automatische Auswahl v27.34d",
        ),
        "automatische Auswahl v27.34d",
    )
    checks += 1

    agents_newline = "\r\n" if "\r\n" in agents_text else "\n"
    agents_required_control_block = agents_newline.join(
        (
            "- Vor jeder Arbeit müssen vollständig gelesen werden:",
            "  - `docs/PROJECT_STATE_CURRENT.md`",
            "  - `docs/PROJECT_MASTERLIST.md`",
            "  - `docs/tasks/CURRENT_TASK.md`",
            "- Kein Task darf aus Versionsfolgen, früheren Chats oder Erinnerung abgeleitet werden.",
            "- Eine Umsetzung ist nur zulässig, wenn `docs/tasks/CURRENT_TASK.md` den Task ausdrücklich autorisiert.",
            "- Bei einem Widerspruch zwischen den verbindlichen Projektdateien sofort STOPP.",
            "- Bei einem Chatwechsel muss der neue Chat den GitHub-HEAD direkt prüfen.",
            "- Lokaler Arbeitsbaum und GitHub-Stand müssen vor Änderungen bestätigt werden.",
            "- `docs/PROJECT_MASTERLIST.md` ist die verbindliche Projektquelle.",
            "- Vor jeder Arbeit müssen vollständig gelesen werden:",
            "  - `docs/PROJECT_STATE_CURRENT.md`",
            "  - `docs/PROJECT_MASTERLIST.md`",
            "  - `docs/tasks/CURRENT_TASK.md`",
            "- Kein Task darf aus Versionsfolgen, früheren Chats oder Erinnerung abgeleitet werden.",
            "- Eine Umsetzung ist nur zulässig, wenn `docs/tasks/CURRENT_TASK.md` den Task ausdrücklich autorisiert.",
            "- Bei einem Widerspruch zwischen den verbindlichen Projektdateien sofort STOPP.",
            "- Bei einem Chatwechsel muss der neue Chat den GitHub-HEAD direkt prüfen.",
            "- Lokaler Arbeitsbaum und GitHub-Stand müssen vor Änderungen bestätigt werden.",
        )
    )
    require(
        agents_text.count(agents_required_control_block) == 1,
        "AGENTS.md: vollständiger verbindlicher Kontrollblock muss exakt einmal vorkommen",
    )
    manipulated_agents_text = agents_text.replace(
        agents_required_control_block,
        "",
        1,
    )
    require(
        manipulated_agents_text != agents_text,
        "AGENTS.md: Entfernung des verbindlichen Kontrollblocks blieb wirkungslos",
    )
    must_reject(
        validate_agents_text,
        manipulated_agents_text,
        "AGENTS.md vollständiger verbindlicher Kontrollblock fehlt",
    )
    checks += 1

    for marker in MASTERLIST_REQUIRED_MARKERS:
        if marker == "`CURRENT_TASK` ist aktuell `BLOCKED`":
            masterlist_current_task_line = (
                "- `CURRENT_TASK` ist aktuell `BLOCKED`, "
                "`Task-ID` ist `NONE` und `Autorisiert` ist `NEIN`."
            )
            require(
                masterlist_text.count(masterlist_current_task_line) == 1,
                "Masterliste: vollständige CURRENT_TASK-Pflichtzeile muss exakt einmal vorkommen",
            )
            manipulated_masterlist_text = masterlist_text.replace(
                masterlist_current_task_line,
                "",
                1,
            )
            require(
                manipulated_masterlist_text != masterlist_text,
                "Masterliste: Entfernung der CURRENT_TASK-Pflichtzeile blieb wirkungslos",
            )
        else:
            manipulated_masterlist_text = changed_once(
                masterlist_text,
                marker,
                "",
                f"Masterliste Pflichtaussage fehlt: {marker}",
            )
        must_reject(
            validate_masterlist_text,
            manipulated_masterlist_text,
            f"Masterliste Pflichtaussage fehlt: {marker}",
        )
        checks += 1

    return checks


def main() -> int:
    try:
        state_text = read_required_text(STATE_PATH)
        task_text = read_required_text(TASK_PATH)
        agents_text = read_required_text(AGENTS_PATH)
        masterlist_text = read_required_text(MASTERLIST_PATH)
        preflight_text = read_required_text(PREFLIGHT_PATH)

        validate_state_text(state_text)
        validate_task_text(task_text)
        validate_agents_text(agents_text)
        validate_masterlist_text(masterlist_text)
        validate_preflight_text(preflight_text)
        manipulation_checks = run_manipulation_matrix(
            state_text,
            task_text,
            agents_text,
            masterlist_text,
        )
    except ValidationError as exc:
        print(f"FEHLER: {exc}")
        print("STOPP: Projektkontinuität oder Task-Steuerung verletzt.")
        return 1

    print("Projektkontinuitäts- und Task-Steuerungsprüfung v27.34c: OK")
    print("PROJECT_STATE_CURRENT: v27.34c / funktionaler Stand v27.34b")
    print("CURRENT_TASK: NONE / BLOCKED / nicht autorisiert")
    print("AGENTS-Regeln und Chatwechsel-Protokoll: OK")
    print("Preflight-Einbindung: OK")
    print(f"Manipulationsmatrix: {manipulation_checks} Blockierungen bestätigt")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
