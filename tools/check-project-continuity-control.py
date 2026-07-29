#!/usr/bin/env python3
"""Prüft die verbindliche Projektkontinuität nach abgeschlossenem v27.35b."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path
from typing import Callable


ROOT = Path(__file__).resolve().parents[1]
AGENTS_PATH = ROOT / "AGENTS.md"
CURSOR_CONTEXT_PATH = ROOT / "docs" / "CURSOR_MASTER_CONTEXT_ACCAOUI.md"
MASTERLIST_PATH = ROOT / "docs" / "PROJECT_MASTERLIST.md"
STATE_PATH = ROOT / "docs" / "PROJECT_STATE_CURRENT.md"
TASK_PATH = ROOT / "docs" / "tasks" / "CURRENT_TASK.md"
PREFLIGHT_PATH = ROOT / "tools" / "preflight.py"
APP_JS_PATH = ROOT / "app.js"

FUNCTIONAL_START_SHA = "a9a18e68ce09a29b375ecd4a44c5cb94fb6794f6"
COMPLETION_SHA = "f168b96ff26c88e5baca212902081932b8986e85"
CHECKER_RELATIVE_PATH = "tools/check-project-continuity-control.py"

# Keine zukünftige Task-ID als aktiven Task einführen.
FORBIDDEN_FUTURE_TASK_MARKERS = ("v27.35c", "v27.36")

WORK_PATH = r"C:\a34a"
HOME_PATH = r"C:\xampp\htdocs\accaoui\v4-dashboard"
WORK_PATH_GIT_BASH = "/c/a34a"
HOME_PATH_GIT_BASH = "/c/xampp/htdocs/accaoui/v4-dashboard"

EXPECTED_STATE_FIELDS = {
    "Stand": "v27.35b",
    "Repository": "`asarrad-bit/accaoui-34a-lernapp`",
    "Branch": "`main`",
    "Letzter abgeschlossener funktionaler Stand": "v27.35b",
    "Direkt bestätigter Abschlusscommit": f"`{COMPLETION_SHA}`",
    "Aktueller HEAD": "DYNAMISCH ZU PRÜFEN",
    "Funktionsstatus": "v27.35b abgeschlossen",
    "Weiterer funktionaler Schritt autorisiert": "NEIN",
    "Aktuell autorisierter Task": "NONE",
    "Aktueller Blocker": "Kein weiterer Task durch CURRENT_TASK autorisiert",
}

EXPECTED_TASK_FIELDS = {
    "Task-ID": "NONE",
    "Status": "BLOCKED",
    "Autorisiert": "NEIN",
    "Letzter abgeschlossener funktionaler Stand": "v27.35b",
    "Letzter abgeschlossener Task": "v27.35b",
    "Abschlusscommit": f"`{COMPLETION_SHA}`",
    "Erwarteter Ausgangscommit": f"`{COMPLETION_SHA}`",
    "Erlaubte Dateien": "keine",
    "Commit erlaubt": "NEIN",
    "Push erlaubt": "NEIN",
}

STATE_REQUIRED_MARKERS = (
    "## Abgeschlossener funktionaler Stand v27.35b",
    "Dashboard „Ihr nächster Lernschritt“ ist abgeschlossen.",
    "Das Dashboard\nzeigt genau einen nächsten Lernschritt.",
    "1. neueste gültige aktive Sitzung",
    "2. Fehlerfragen",
    "3. schwächstes ausreichend belegtes Sachgebiet",
    "4. unbekannte Lernkarten",
    "5. neue Prüfung",
    "Ausschließlich vorhandene localStorage-Daten werden defensiv gelesen.",
    "Es gibt keine neue Speicherung und keine neuen Storage-Keys.",
    "Ungültige Sitzungen und Statistikwerte werden ignoriert.",
    "Prüfung, Lerneinheit und Lernkarten wurden im Browser bestätigt.",
    "Automatisierte Browserprüfung: 6/6 bestanden.",
    "Ausschließlich `app.js` wurde im funktionalen Commit verändert.",
    "Kein Folgetask ist ausgewählt oder autorisiert.",
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
    "`AGENTS.md`",
    "GitHub-HEAD für `refs/heads/main` direkt prüfen.",
    "Bei Abweichung oder Widerspruch sofort STOPP.",
    "Synchronisation nur nach gesonderter Freigabe ausführen.",
    "## Aktualisierungspflicht nach jedem Versionsabschluss",
    "Nach jedem Versionsabschluss müssen Projektzustand, Masterliste und Task-Steuerung",
)

TASK_REQUIRED_MARKERS = (
    "## Verbindliche Sperre",
    "v27.35b ist abgeschlossen.",
    "Kein Folgetask ist ausgewählt.",
    "Kein Task darf aus Versionsfolge, Erinnerung oder früheren Chats",
    "Ein neuer Task muss ausdrücklich durch Projekteigentümer,",
    "verbindlichen Projektchat und CURRENT_TASK autorisiert werden.",
    "## Abgeschlossener funktionaler Task v27.35b",
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

AGENTS_REQUIRED_CONTROL_LINES = (
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
AGENTS_REQUIRED_CONTROL_BLOCK = "\n".join(AGENTS_REQUIRED_CONTROL_LINES)

REQUIRED_CHAT_READING_BLOCK = "\n".join(
    (
        "AGENTS.md",
        "docs/PROJECT_STATE_CURRENT.md",
        "docs/PROJECT_MASTERLIST.md",
        "docs/tasks/CURRENT_TASK.md",
    )
)

CURSOR_REQUIRED_MARKERS = (
    "Stand: v27.35b",
    "Arbeit: `C:\\a34a`",
    "Zuhause: `C:\\xampp\\htdocs\\accaoui\\v4-dashboard`",
    "Letzter abgeschlossener funktionaler Stand: v27.35b",
    f"Abschlusscommit: `{COMPLETION_SHA}`",
    "| v24.6c | Pausieren/Fortsetzen Prüfung und Lernen | **erledigt** |",
    "**Erledigt:** v24.6b (Wiederholung/offene Fragen), v24.6c (Pausieren/Fortsetzen),",
    "## 14. Nächster sinnvoller Schritt",
    "`CURRENT_TASK` ist `NONE` / `BLOCKED` / nicht autorisiert.",
    "Kein nächster funktionaler Task ist ausgewählt.",
    "Keine automatische Task-Auswahl.",
    "## 15. Wenn ein neuer Chat beginnt",
    "Zuerst vollständig lesen:",
    REQUIRED_CHAT_READING_BLOCK,
    "docs/CURSOR_MASTER_CONTEXT_ACCAOUI.md",
    "docs/SUPABASE_EXAM_QUESTION_DATABASE_PLAN.md",
)

CURSOR_V2735B_EXACT_MARKERS = (
    "Stand: v27.35b\nProjekt:",
    "Arbeit: `C:\\a34a`",
    "Zuhause: `C:\\xampp\\htdocs\\accaoui\\v4-dashboard`",
    "Letzter abgeschlossener funktionaler Stand: v27.35b",
    f"Abschlusscommit: `{COMPLETION_SHA}`",
    "| v24.6c | Pausieren/Fortsetzen Prüfung und Lernen | **erledigt** |",
    "## 14. Nächster sinnvoller Schritt",
    "`CURRENT_TASK` ist `NONE` / `BLOCKED` / nicht autorisiert.",
    "Kein nächster funktionaler Task ist ausgewählt.",
    "Keine automatische Task-Auswahl.",
    REQUIRED_CHAT_READING_BLOCK,
)

CURSOR_NEW_CHAT_LOCAL_HEAD_MARKERS = (
    "git rev-parse HEAD",
    "Lokalen und GitHub-HEAD direkt vergleichen",
)

STATE_V2735B_EXACT_MARKERS = (
    "Stand: v27.35b\nRepository:",
    f"Direkt bestätigter Abschlusscommit: `{COMPLETION_SHA}`",
    "## Abgeschlossener funktionaler Stand v27.35b",
    "Aktuell autorisierter Task: NONE",
    "Weiterer funktionaler Schritt autorisiert: NEIN",
)

TASK_V2735B_EXACT_MARKERS = (
    "Task-ID: NONE",
    "Status: BLOCKED",
    "Autorisiert: NEIN",
    "Erlaubte Dateien: keine",
    "v27.35b ist abgeschlossen.",
    "Kein Folgetask ist ausgewählt.",
)

MASTERLIST_REQUIRED_MARKERS = (
    f"Arbeits-Laptop: `{WORK_PATH}`",
    f"Git Bash Arbeits-Laptop: `{WORK_PATH_GIT_BASH}`",
    f"Zuhause-Laptop: `{HOME_PATH}`",
    f"Git Bash Zuhause-Laptop: `{HOME_PATH_GIT_BASH}`",
    "| v27.34c |",
    "### Historisch: Projektkontinuität und verbindliche Task-Steuerung v27.34c",
    "| v27.34d |",
    "### Historisch: Nicht funktionaler Korrektur- und Härtungsschritt v27.34d",
    "- Der doppelte AGENTS-Kontinuitäts-Regelblock wurde auf exakt eine vollständige Kopie reduziert.",
    "| v27.34e |",
    "### Vollständig gesperrter lokaler Adapter-Verhaltensvertrag v27.34e",
    "Das NO-GO-Audit wurde durch einen kanonisch gebundenen, maschinenlesbaren Verhaltensvertrag",
    "Exakt 28 historische Adapter-Sperrchecker sind mit SHA-256-Dateifingerprints inventarisiert",
    "Kein Adapter wurde implementiert, importiert, instanziiert oder aufgerufen.",
    "Der letzte abgeschlossene funktionale Stand bleibt v27.34b.",
    "`v27.34f` wird nicht automatisch ausgewählt oder autorisiert.",
    "| v27.34f |",
    "### Historisch: Nichtfunktionale Projektkontinuitätsbereinigung v27.34f",
    "v24.6c ist ausschließlich als erledigter historischer Schritt dokumentiert",
    "Die vier aktiven automatischen `git pull --ff-only`-Vorgaben wurden entfernt.",
    "| v27.35a |",
    "### Historisch: Nichtfunktionale Task-Steuerung v27.35a",
    "| v27.35b |",
    "### Abgeschlossener funktionaler Stand v27.35b",
    f"Abschlusscommit: `{COMPLETION_SHA}`.",
    "- Verbindlicher Projektzustand: `docs/PROJECT_STATE_CURRENT.md`",
    "- Verbindliche Task-Steuerung: `docs/tasks/CURRENT_TASK.md`",
    (
        "- `CURRENT_TASK` ist aktuell `BLOCKED`, "
        "`Task-ID` ist `NONE` und `Autorisiert` ist `NEIN`."
    ),
    "Es ist kein funktionaler Folgeschritt ausgewählt oder autorisiert.",
    "Diese Bestands- und Backlogliste ist keine Task-Autorisierung.",
    "`CURRENT_TASK` ist aktuell `BLOCKED`; `Task-ID` ist `NONE` und `Autorisiert` ist `NEIN`",
    REQUIRED_CHAT_READING_BLOCK,
)

MASTERLIST_V2735B_EXACT_MARKERS = (
    "Stand: v27.35b\nBranch:",
    f"Arbeits-Laptop: `{WORK_PATH}`",
    f"Zuhause-Laptop: `{HOME_PATH}`",
    "| v27.35b |",
    "### Abgeschlossener funktionaler Stand v27.35b",
    "`CURRENT_TASK` ist aktuell `BLOCKED`; `Task-ID` ist `NONE` und `Autorisiert` ist `NEIN`",
    f"Abschlusscommit: `{COMPLETION_SHA}`.",
    REQUIRED_CHAT_READING_BLOCK,
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
    text = text.replace("\r\n", "\n").replace("\r", "\n")
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


def validate_exact_markers(
    text: str,
    markers: tuple[str, ...],
    document_name: str,
) -> None:
    for marker in markers:
        require(
            text.count(marker) == 1,
            (
                f"{document_name}: Pflichtaussage muss exakt einmal vorkommen: "
                f"{marker}"
            ),
        )


def section_between(
    text: str,
    start_heading: str,
    end_heading: str | None,
    document_name: str,
) -> str:
    require(
        text.count(start_heading) == 1,
        f"{document_name}: Abschnitt muss exakt einmal vorkommen: {start_heading}",
    )
    start_index = text.index(start_heading)
    if end_heading is None:
        return text[start_index:]
    require(
        text.count(end_heading) == 1,
        f"{document_name}: Folgeabschnitt muss exakt einmal vorkommen: {end_heading}",
    )
    end_index = text.index(end_heading, start_index + len(start_heading))
    require(
        end_index > start_index,
        f"{document_name}: Abschnittsreihenfolge ist ungültig: {start_heading}",
    )
    return text[start_index:end_index]


def validate_state_text(text: str) -> None:
    validate_exact_fields(text, EXPECTED_STATE_FIELDS)
    validate_required_markers(text, STATE_REQUIRED_MARKERS, "PROJECT_STATE_CURRENT")
    validate_exact_markers(
        text,
        STATE_V2735B_EXACT_MARKERS,
        "PROJECT_STATE_CURRENT",
    )

    commit_shas = set(re.findall(r"\b[0-9a-f]{40}\b", text))
    require(
        commit_shas == {COMPLETION_SHA},
        "PROJECT_STATE_CURRENT darf nur den direkt bestätigten Abschlusscommit enthalten",
    )
    for forbidden_marker in FORBIDDEN_FUTURE_TASK_MARKERS:
        require(
            forbidden_marker not in text,
            "PROJECT_STATE_CURRENT darf keinen weiteren Folgeschritt auswählen oder nennen",
        )


def validate_task_text(text: str) -> None:
    validate_exact_fields(text, EXPECTED_TASK_FIELDS)
    validate_required_markers(text, TASK_REQUIRED_MARKERS, "CURRENT_TASK")
    validate_exact_markers(text, TASK_V2735B_EXACT_MARKERS, "CURRENT_TASK")

    for field_name in LATER_TASK_TEMPLATE_FIELDS:
        require(
            f"- {field_name}" in text,
            f"CURRENT_TASK: Pflichtfeld der späteren Task-Vorlage fehlt: {field_name}",
        )

    for forbidden_marker in FORBIDDEN_FUTURE_TASK_MARKERS:
        require(
            forbidden_marker not in text,
            "CURRENT_TASK darf keinen weiteren Folgeschritt auswählen oder nennen",
        )
    contradictory_grants = (
        "Status: AUTHORIZED",
        "Autorisiert: JA",
        "Commit erlaubt: JA",
        "Push erlaubt: JA",
        "Erlaubte Dateien: `app.js`",
        "Erlaubte Dateien: app.js",
        "Task-ID: v27.35b",
    )
    for contradictory_grant in contradictory_grants:
        require(
            contradictory_grant not in text,
            f"CURRENT_TASK enthält widersprüchliche Freigabe: {contradictory_grant}",
        )


def validate_agents_text(text: str) -> None:
    normalized_text = text.replace("\r\n", "\n").replace("\r", "\n")
    normalized_lines = normalized_text.splitlines()
    require(
        normalized_text.count(AGENTS_REQUIRED_CONTROL_BLOCK) == 1,
        "AGENTS.md: vollständiger verbindlicher Kontrollblock muss exakt einmal vorkommen",
    )
    for required_line in AGENTS_REQUIRED_CONTROL_LINES:
        require(
            normalized_lines.count(required_line) == 1,
            (
                "AGENTS.md: vollständige Pflichtzeile muss exakt einmal vorkommen: "
                f"{required_line}"
            ),
        )


def validate_sync_section(
    section_text: str,
    document_name: str,
    section_name: str,
) -> None:
    for marker in (
        "git status --short",
        "Branch",
        "GitHub-HEAD",
        "sofort STOPP",
        "Synchronisation nur nach gesonderter Freigabe",
        "Commit und Push",
    ):
        require(
            marker.casefold() in section_text.casefold(),
            f"{document_name} / {section_name}: Pflichtaussage fehlt: {marker}",
        )
    require(
        re.search(
            r"(?im)\blokal(?:e|en|er|es)?\b[^\r\n]{0,80}\bHEAD\b",
            section_text,
        )
        is not None,
        f"{document_name} / {section_name}: lokale HEAD-Prüfung fehlt",
    )
    require(
        "git pull --ff-only" not in section_text,
        (
            f"{document_name} / {section_name}: automatisches "
            "git pull --ff-only ist unzulässig"
        ),
    )


def validate_project_paths(text: str, document_name: str) -> None:
    require(
        WORK_PATH in text,
        f"{document_name}: Arbeits-Pfad fehlt: {WORK_PATH}",
    )
    require(
        HOME_PATH in text,
        f"{document_name}: Zuhause-Pfad fehlt: {HOME_PATH}",
    )
    require(
        text.count(WORK_PATH) >= 1,
        f"{document_name}: Arbeits-Pfad muss vorhanden sein",
    )
    require(
        text.count(HOME_PATH) >= 1,
        f"{document_name}: Zuhause-Pfad muss vorhanden sein",
    )


def validate_cursor_context_text(text: str) -> None:
    validate_required_markers(
        text,
        CURSOR_REQUIRED_MARKERS,
        "CURSOR_MASTER_CONTEXT_ACCAOUI",
    )
    validate_exact_markers(
        text,
        CURSOR_V2735B_EXACT_MARKERS,
        "CURSOR_MASTER_CONTEXT_ACCAOUI",
    )
    validate_project_paths(text, "CURSOR_MASTER_CONTEXT_ACCAOUI")
    require(
        "| v24.6c | Pausieren/Fortsetzen Prüfung und Lernen | **offen** |"
        not in text,
        "CURSOR_MASTER_CONTEXT_ACCAOUI: v24.6c darf nicht offen sein",
    )

    workflow_section = section_between(
        text,
        "### Arbeitsworkflow / Git-Synchronisation",
        "## 2. Ziel der App",
        "CURSOR_MASTER_CONTEXT_ACCAOUI",
    )
    validate_sync_section(
        workflow_section,
        "CURSOR_MASTER_CONTEXT_ACCAOUI",
        "Arbeitsworkflow / Git-Synchronisation",
    )

    next_task_section = section_between(
        text,
        "## 14. Nächster sinnvoller Schritt",
        "## 15. Wenn ein neuer Chat beginnt",
        "CURSOR_MASTER_CONTEXT_ACCAOUI",
    )
    require(
        "v24.6c" not in next_task_section,
        "CURSOR_MASTER_CONTEXT_ACCAOUI: alte aktive Task-Auswahl v24.6c",
    )
    require(
        "AUTHORIZED" not in next_task_section,
        "CURSOR_MASTER_CONTEXT_ACCAOUI: CURRENT_TASK darf nicht AUTHORIZED sein",
    )
    for forbidden_marker in FORBIDDEN_FUTURE_TASK_MARKERS:
        require(
            forbidden_marker not in next_task_section,
            "CURSOR_MASTER_CONTEXT_ACCAOUI: unzulässige weitere Task-Auswahl",
        )

    new_chat_section = section_between(
        text,
        "## 15. Wenn ein neuer Chat beginnt",
        None,
        "CURSOR_MASTER_CONTEXT_ACCAOUI",
    )
    validate_sync_section(
        new_chat_section,
        "CURSOR_MASTER_CONTEXT_ACCAOUI",
        "Wenn ein neuer Chat beginnt",
    )
    validate_exact_markers(
        new_chat_section,
        CURSOR_NEW_CHAT_LOCAL_HEAD_MARKERS,
        "CURSOR_MASTER_CONTEXT_ACCAOUI / Wenn ein neuer Chat beginnt",
    )
    require(
        REQUIRED_CHAT_READING_BLOCK in new_chat_section,
        "CURSOR_MASTER_CONTEXT_ACCAOUI: Pflichtlektüre ist unvollständig",
    )
    require(
        "Kein Task darf aus Versionsfolgen, früheren Chats oder"
        in new_chat_section,
        "CURSOR_MASTER_CONTEXT_ACCAOUI: Ableitungssperre fehlt",
    )


def validate_masterlist_text(text: str) -> None:
    require(
        exact_field(text, "Stand") == "v27.35b",
        "Masterliste muss exakt auf Stand v27.35b stehen",
    )
    validate_required_markers(
        text,
        MASTERLIST_REQUIRED_MARKERS,
        "PROJECT_MASTERLIST",
    )
    validate_exact_markers(
        text,
        MASTERLIST_V2735B_EXACT_MARKERS,
        "PROJECT_MASTERLIST",
    )
    validate_project_paths(text, "PROJECT_MASTERLIST")
    require(
        f"Arbeits-Laptop: `{WORK_PATH}`" in text,
        "PROJECT_MASTERLIST: Arbeits-Laptop-Pfad fehlt",
    )
    require(
        f"Zuhause-Laptop: `{HOME_PATH}`" in text,
        "PROJECT_MASTERLIST: Zuhause-Laptop-Pfad fehlt",
    )
    require(
        "Projektordner:" not in text.split("## Leitidee", 1)[0],
        "PROJECT_MASTERLIST: veraltete einzelne Projektordner-Angabe im Kopf",
    )

    workflow_section = section_between(
        text,
        "### Projektarbeitsregel: Arbeit / Zuhause",
        "## 2. Cursor-Regel",
        "PROJECT_MASTERLIST",
    )
    validate_sync_section(
        workflow_section,
        "PROJECT_MASTERLIST",
        "Projektarbeitsregel: Arbeit / Zuhause",
    )

    new_chat_section = section_between(
        text,
        "## 15. Start in neuem Chat",
        None,
        "PROJECT_MASTERLIST",
    )
    validate_sync_section(
        new_chat_section,
        "PROJECT_MASTERLIST",
        "Start in neuem Chat",
    )
    require(
        REQUIRED_CHAT_READING_BLOCK in new_chat_section,
        "PROJECT_MASTERLIST: Pflichtlektüre ist unvollständig",
    )
    require(
        "Kein Task darf aus Versionsfolgen, früheren Chats oder"
        in new_chat_section,
        "PROJECT_MASTERLIST: Ableitungssperre fehlt",
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


def run_git(args: list[str]) -> str:
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
    except (FileNotFoundError, OSError) as exc:
        raise ValidationError(f"git ist nicht ausführbar: {exc}") from exc
    require(
        completed.returncode == 0,
        (
            f"git-Befehl fehlgeschlagen (git {' '.join(args)}): "
            f"{completed.stderr.strip()}"
        ),
    )
    return completed.stdout


def validate_v2735b_git_history() -> None:
    require(
        (ROOT / ".git").exists(),
        "Kein Git-Repository unter ROOT gefunden; Git-Historienprüfung nicht möglich",
    )
    require(APP_JS_PATH.is_file(), "app.js fehlt; erwartete Kern-Datei nicht gefunden")

    run_git(["merge-base", "--is-ancestor", COMPLETION_SHA, "HEAD"])

    changed_between = [
        line.strip()
        for line in run_git(
            ["diff", "--name-only", FUNCTIONAL_START_SHA, COMPLETION_SHA]
        ).splitlines()
        if line.strip()
    ]
    require(
        changed_between == ["app.js"],
        (
            "Zwischen funktionalem Ausgangscommit und Abschlusscommit "
            "darf ausschließlich app.js verändert worden sein; "
            f"gefunden: {changed_between!r}"
        ),
    )

    app_js_since_completion = run_git(
        ["diff", "--name-only", COMPLETION_SHA, "HEAD", "--", "app.js"]
    ).strip()
    require(
        app_js_since_completion == "",
        (
            f"app.js wurde seit Abschlusscommit {COMPLETION_SHA} "
            "gegenüber HEAD erneut verändert"
        ),
    )

    app_js_working_tree = run_git(
        ["diff", "--name-only", COMPLETION_SHA, "--", "app.js"]
    ).strip()
    require(
        app_js_working_tree == "",
        (
            f"app.js wurde seit Abschlusscommit {COMPLETION_SHA} "
            "im Arbeitsbaum erneut verändert"
        ),
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


def exercise_exact_marker_manipulations(
    validator: Callable[[str], None],
    text: str,
    markers: tuple[str, ...],
    document_name: str,
) -> int:
    checks = 0
    for marker in markers:
        require(
            text.count(marker) == 1,
            (
                f"{document_name}: Ausgangs-Pflichtaussage muss für die "
                f"Manipulation exakt einmal vorkommen: {marker}"
            ),
        )

        removed_text = text.replace(marker, "", 1)
        require(
            removed_text != text,
            f"{document_name}: Entfernung blieb wirkungslos: {marker}",
        )
        must_reject(
            validator,
            removed_text,
            f"{document_name}: Pflichtaussage entfernt: {marker}",
        )
        checks += 1

        duplicated_text = text.replace(marker, marker + "\n" + marker, 1)
        require(
            duplicated_text != text,
            f"{document_name}: Duplikation blieb wirkungslos: {marker}",
        )
        must_reject(
            validator,
            duplicated_text,
            f"{document_name}: Pflichtaussage dupliziert: {marker}",
        )
        checks += 1

    return checks


def run_manipulation_matrix(
    state_text: str,
    task_text: str,
    agents_text: str,
    cursor_context_text: str,
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
        "Stand": "v27.35a",
        "Repository": "`anderes/repository`",
        "Branch": "`anderer-branch`",
        "Letzter abgeschlossener funktionaler Stand": "v27.34b",
        "Direkt bestätigter Abschlusscommit": f"`{'0' * 40}`",
        "Aktueller HEAD": COMPLETION_SHA,
        "Funktionsstatus": "v27.35b offen",
        "Weiterer funktionaler Schritt autorisiert": "JA",
        "Aktuell autorisierter Task": "v27.35b",
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

    must_reject(
        validate_state_text,
        state_text + "v27.35c wird als Folgeschritt vorgemerkt.\n",
        "PROJECT_STATE_CURRENT automatische Auswahl eines weiteren Tasks",
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
        "Task-ID": "v27.35b",
        "Status": "AUTHORIZED",
        "Autorisiert": "JA",
        "Letzter abgeschlossener funktionaler Stand": "v27.34b",
        "Letzter abgeschlossener Task": "v27.35a",
        "Abschlusscommit": f"`{'0' * 40}`",
        "Erwarteter Ausgangscommit": f"`{'0' * 40}`",
        "Erlaubte Dateien": "`app.js`",
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

    must_reject(
        validate_task_text,
        changed_once(
            task_text,
            "Erlaubte Dateien: keine",
            "Erlaubte Dateien: `app.js`, `index.html`",
            "CURRENT_TASK zusätzliche erlaubte Dateien",
        ),
        "CURRENT_TASK zusätzliche erlaubte Dateien",
    )
    checks += 1

    for contradictory_grant in (
        "Status: AUTHORIZED",
        "Autorisiert: JA",
        "Commit erlaubt: JA",
        "Push erlaubt: JA",
        "Erlaubte Dateien: `app.js`",
        "Task-ID: v27.35b",
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
            "Kein Folgetask ist ausgewählt.",
            "`v27.35c` wird automatisch gewählt und autorisiert.",
            "automatische Auswahl eines Folgeschritts",
        ),
        "automatische Auswahl eines Folgeschritts",
    )
    checks += 1

    checks += exercise_exact_marker_manipulations(
        validate_state_text,
        state_text,
        STATE_V2735B_EXACT_MARKERS,
        "PROJECT_STATE_CURRENT",
    )
    checks += exercise_exact_marker_manipulations(
        validate_task_text,
        task_text,
        TASK_V2735B_EXACT_MARKERS,
        "CURRENT_TASK",
    )

    agents_newline = "\r\n" if "\r\n" in agents_text else "\n"
    agents_required_control_block = agents_newline.join(
        AGENTS_REQUIRED_CONTROL_LINES
    )

    validate_agents_text(agents_text)
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

    validate_agents_text(agents_text)
    require(
        agents_text.count(agents_required_control_block) == 1,
        "AGENTS.md: vollständiger verbindlicher Kontrollblock muss vor Duplikation exakt einmal vorkommen",
    )
    duplicated_agents_block_text = agents_text.replace(
        agents_required_control_block,
        (
            agents_required_control_block
            + agents_newline
            + agents_required_control_block
        ),
        1,
    )
    require(
        duplicated_agents_block_text != agents_text,
        "AGENTS.md: Duplikation des verbindlichen Kontrollblocks blieb wirkungslos",
    )
    must_reject(
        validate_agents_text,
        duplicated_agents_block_text,
        "AGENTS.md vollständiger verbindlicher Kontrollblock dupliziert",
    )
    checks += 1

    for required_line in AGENTS_REQUIRED_CONTROL_LINES:
        target_line = required_line + agents_newline

        validate_agents_text(agents_text)
        require(
            agents_text.count(target_line) == 1,
            (
                "AGENTS.md: vollständige Pflichtzeile muss vor Entfernung "
                f"exakt einmal vorkommen: {required_line}"
            ),
        )
        removed_agents_line_text = agents_text.replace(target_line, "", 1)
        require(
            removed_agents_line_text != agents_text,
            (
                "AGENTS.md: Entfernung der vollständigen Pflichtzeile blieb "
                f"wirkungslos: {required_line}"
            ),
        )
        must_reject(
            validate_agents_text,
            removed_agents_line_text,
            f"AGENTS.md vollständige Pflichtzeile fehlt: {required_line}",
        )
        checks += 1

        validate_agents_text(agents_text)
        require(
            agents_text.count(target_line) == 1,
            (
                "AGENTS.md: vollständige Pflichtzeile muss vor Duplikation "
                f"exakt einmal vorkommen: {required_line}"
            ),
        )
        duplicated_agents_line_text = agents_text.replace(
            target_line,
            target_line + target_line,
            1,
        )
        require(
            duplicated_agents_line_text != agents_text,
            (
                "AGENTS.md: Duplikation der vollständigen Pflichtzeile blieb "
                f"wirkungslos: {required_line}"
            ),
        )
        must_reject(
            validate_agents_text,
            duplicated_agents_line_text,
            f"AGENTS.md vollständige Pflichtzeile dupliziert: {required_line}",
        )
        checks += 1

    validate_cursor_context_text(cursor_context_text)
    checks += exercise_exact_marker_manipulations(
        validate_cursor_context_text,
        cursor_context_text,
        CURSOR_V2735B_EXACT_MARKERS,
        "CURSOR_MASTER_CONTEXT_ACCAOUI",
    )

    cursor_new_chat_section = section_between(
        cursor_context_text,
        "## 15. Wenn ein neuer Chat beginnt",
        None,
        "CURSOR_MASTER_CONTEXT_ACCAOUI",
    )
    for marker in CURSOR_NEW_CHAT_LOCAL_HEAD_MARKERS:
        require(
            cursor_new_chat_section.count(marker) == 1,
            (
                "Cursor-Chatwechsel: lokale HEAD-Pflicht muss vor der "
                f"Manipulation exakt einmal vorkommen: {marker}"
            ),
        )

        removed_section = cursor_new_chat_section.replace(marker, "", 1)
        removed_cursor_text = cursor_context_text.replace(
            cursor_new_chat_section,
            removed_section,
            1,
        )
        require(
            removed_cursor_text != cursor_context_text,
            f"Cursor-Chatwechsel: Entfernung blieb wirkungslos: {marker}",
        )
        must_reject(
            validate_cursor_context_text,
            removed_cursor_text,
            f"Cursor-Chatwechsel: lokale HEAD-Pflicht entfernt: {marker}",
        )
        checks += 1

        duplicated_section = cursor_new_chat_section.replace(
            marker,
            marker + "\n" + marker,
            1,
        )
        duplicated_cursor_text = cursor_context_text.replace(
            cursor_new_chat_section,
            duplicated_section,
            1,
        )
        require(
            duplicated_cursor_text != cursor_context_text,
            f"Cursor-Chatwechsel: Duplikation blieb wirkungslos: {marker}",
        )
        must_reject(
            validate_cursor_context_text,
            duplicated_cursor_text,
            f"Cursor-Chatwechsel: lokale HEAD-Pflicht dupliziert: {marker}",
        )
        checks += 1

    for missing_path in (
        "docs/PROJECT_STATE_CURRENT.md",
        "docs/tasks/CURRENT_TASK.md",
    ):
        manipulated_reading_block = "\n".join(
            line
            for line in REQUIRED_CHAT_READING_BLOCK.splitlines()
            if line != missing_path
        )
        manipulated_cursor_text = changed_once(
            cursor_context_text,
            REQUIRED_CHAT_READING_BLOCK,
            manipulated_reading_block,
            f"Cursor-Pflichtlektüre fehlt: {missing_path}",
        )
        must_reject(
            validate_cursor_context_text,
            manipulated_cursor_text,
            f"Cursor-Pflichtlektüre fehlt: {missing_path}",
        )
        checks += 1

    for heading in (
        "### Arbeitsworkflow / Git-Synchronisation",
        "## 15. Wenn ein neuer Chat beginnt",
    ):
        manipulated_cursor_text = changed_once(
            cursor_context_text,
            heading,
            heading + "\n\n`git pull --ff-only`",
            f"Cursor automatisches git pull in {heading}",
        )
        must_reject(
            validate_cursor_context_text,
            manipulated_cursor_text,
            f"Cursor automatisches git pull in {heading}",
        )
        checks += 1

    manipulated_cursor_task_text = changed_once(
        cursor_context_text,
        "Keine automatische Task-Auswahl.",
        (
            "Keine automatische Task-Auswahl.\n"
            "**v24.6c – Prüfung/Lernen pausieren und später fortsetzen**"
        ),
        "Cursor alte aktive Task-Auswahl v24.6c",
    )
    must_reject(
        validate_cursor_context_text,
        manipulated_cursor_task_text,
        "Cursor alte aktive Task-Auswahl v24.6c",
    )
    checks += 1

    manipulated_cursor_future_task_text = changed_once(
        cursor_context_text,
        "Keine automatische Task-Auswahl.",
        (
            "Keine automatische Task-Auswahl.\n"
            "**v27.35c wird automatisch fortgesetzt.**"
        ),
        "Cursor unzulässige weitere Task-Auswahl v27.35c",
    )
    must_reject(
        validate_cursor_context_text,
        manipulated_cursor_future_task_text,
        "Cursor unzulässige weitere Task-Auswahl v27.35c",
    )
    checks += 1

    must_reject(
        validate_cursor_context_text,
        changed_once(
            cursor_context_text,
            "Arbeit: `C:\\a34a`",
            "Arbeit: `C:\\falscher\\arbeitspfad`",
            "Cursor fehlender/falscher Arbeits-Pfad",
        ),
        "Cursor fehlender/falscher Arbeits-Pfad",
    )
    checks += 1

    must_reject(
        validate_cursor_context_text,
        changed_once(
            cursor_context_text,
            "Zuhause: `C:\\xampp\\htdocs\\accaoui\\v4-dashboard`",
            "Zuhause: `C:\\falscher\\zuhausepfad`",
            "Cursor fehlender/falscher Zuhause-Pfad",
        ),
        "Cursor fehlender/falscher Zuhause-Pfad",
    )
    checks += 1

    must_reject(
        validate_cursor_context_text,
        changed_once(
            cursor_context_text,
            "Arbeit: `C:\\a34a`\nZuhause: `C:\\xampp\\htdocs\\accaoui\\v4-dashboard`",
            "Arbeit: `C:\\xampp\\htdocs\\accaoui\\v4-dashboard`\nZuhause: `C:\\a34a`",
            "Cursor vertauschte Projektpfade",
        ),
        "Cursor vertauschte Projektpfade",
    )
    checks += 1

    for marker in MASTERLIST_REQUIRED_MARKERS:
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

    checks += exercise_exact_marker_manipulations(
        validate_masterlist_text,
        masterlist_text,
        MASTERLIST_V2735B_EXACT_MARKERS,
        "PROJECT_MASTERLIST",
    )

    for missing_path in (
        "docs/PROJECT_STATE_CURRENT.md",
        "docs/tasks/CURRENT_TASK.md",
    ):
        manipulated_reading_block = "\n".join(
            line
            for line in REQUIRED_CHAT_READING_BLOCK.splitlines()
            if line != missing_path
        )
        manipulated_masterlist_text = changed_once(
            masterlist_text,
            REQUIRED_CHAT_READING_BLOCK,
            manipulated_reading_block,
            f"Masterlisten-Pflichtlektüre fehlt: {missing_path}",
        )
        must_reject(
            validate_masterlist_text,
            manipulated_masterlist_text,
            f"Masterlisten-Pflichtlektüre fehlt: {missing_path}",
        )
        checks += 1

    for heading in (
        "### Projektarbeitsregel: Arbeit / Zuhause",
        "## 15. Start in neuem Chat",
    ):
        manipulated_masterlist_text = changed_once(
            masterlist_text,
            heading,
            heading + "\n\n`git pull --ff-only`",
            f"Masterliste automatisches git pull in {heading}",
        )
        must_reject(
            validate_masterlist_text,
            manipulated_masterlist_text,
            f"Masterliste automatisches git pull in {heading}",
        )
        checks += 1

    must_reject(
        validate_masterlist_text,
        changed_once(
            masterlist_text,
            f"Arbeits-Laptop: `{WORK_PATH}`",
            "Arbeits-Laptop: `C:\\falscher\\arbeitspfad`",
            "Masterliste fehlender/falscher Arbeits-Pfad",
        ),
        "Masterliste fehlender/falscher Arbeits-Pfad",
    )
    checks += 1

    must_reject(
        validate_masterlist_text,
        changed_once(
            masterlist_text,
            f"Zuhause-Laptop: `{HOME_PATH}`",
            "Zuhause-Laptop: `C:\\falscher\\zuhausepfad`",
            "Masterliste fehlender/falscher Zuhause-Pfad",
        ),
        "Masterliste fehlender/falscher Zuhause-Pfad",
    )
    checks += 1

    must_reject(
        validate_masterlist_text,
        changed_once(
            masterlist_text,
            (
                f"Arbeits-Laptop: `{WORK_PATH}`\n"
                f"Git Bash Arbeits-Laptop: `{WORK_PATH_GIT_BASH}`\n"
                f"Zuhause-Laptop: `{HOME_PATH}`\n"
                f"Git Bash Zuhause-Laptop: `{HOME_PATH_GIT_BASH}`"
            ),
            (
                f"Arbeits-Laptop: `{HOME_PATH}`\n"
                f"Git Bash Arbeits-Laptop: `{HOME_PATH_GIT_BASH}`\n"
                f"Zuhause-Laptop: `{WORK_PATH}`\n"
                f"Git Bash Zuhause-Laptop: `{WORK_PATH_GIT_BASH}`"
            ),
            "Masterliste vertauschte Projektpfade",
        ),
        "Masterliste vertauschte Projektpfade",
    )
    checks += 1

    return checks


def main() -> int:
    try:
        state_text = read_required_text(STATE_PATH)
        task_text = read_required_text(TASK_PATH)
        agents_text = read_required_text(AGENTS_PATH)
        cursor_context_text = read_required_text(CURSOR_CONTEXT_PATH)
        masterlist_text = read_required_text(MASTERLIST_PATH)
        preflight_text = read_required_text(PREFLIGHT_PATH)

        validate_state_text(state_text)
        validate_task_text(task_text)
        validate_agents_text(agents_text)
        validate_cursor_context_text(cursor_context_text)
        validate_masterlist_text(masterlist_text)
        validate_preflight_text(preflight_text)
        validate_v2735b_git_history()
        manipulation_checks = run_manipulation_matrix(
            state_text,
            task_text,
            agents_text,
            cursor_context_text,
            masterlist_text,
        )
    except ValidationError as exc:
        print(f"FEHLER: {exc}")
        print("STOPP: Projektkontinuität oder Task-Steuerung verletzt.")
        return 1

    print("Projektkontinuität und Task-Steuerung v27.35b: OK")
    print("PROJECT_STATE_CURRENT: v27.35b abgeschlossen / Task NONE")
    print("CURRENT_TASK: NONE / BLOCKED / Autorisiert NEIN / keine Dateien")
    print("AGENTS-Regeln, Cursor-Kontext und Chatwechsel-Protokoll: OK")
    print("Projektpfade Arbeit und Zuhause: OK")
    print("Preflight-Einbindung: OK")
    print("Git-Historie v27.35b und app.js unverändert seit Abschluss: OK")
    print(f"Manipulationsmatrix: {manipulation_checks} Blockierungen bestätigt")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
