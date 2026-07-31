#!/usr/bin/env python3
"""Prüft die verbindliche Projektkontinuität für den autorisierten Task v27.35g."""

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
INDEX_HTML_PATH = ROOT / "index.html"
STYLE_CSS_PATH = ROOT / "style.css"

GATE_SHA = "e4b6929af552e4245290d3eb5db97815365162e6"
COMPLETION_SHA = "f168b96ff26c88e5baca212902081932b8986e85"
CONTROL_COMMIT_SHA = "7b0e110d20e97f0bc8487fe6537e0683d9e25940"
CHECKER_FIX_SHA = "d83869308a277e077b3da6d7e2c1a23001374a48"
V2735D_COMPLETION_SHA = "b4d2de5002918766bb45fe001cbbfdb333a6d7c5"
V2735E_GATE_SHA = "260e6527208769f18018d1db6e6e3b7fbe9d7d7e"
V2735G_GATE_SHA = "db2f12a1af7792c59e9e6411bb127b2f68401713"
CHECKER_RELATIVE_PATH = "tools/check-project-continuity-control.py"
PROTECTED_RUNTIME_FILES = ("app.js", "index.html", "style.css")
EXPECTED_CONTROL_FILES = (
    "docs/CURSOR_MASTER_CONTEXT_ACCAOUI.md",
    "docs/PROJECT_MASTERLIST.md",
    "docs/PROJECT_STATE_CURRENT.md",
    "docs/tasks/CURRENT_TASK.md",
    "tools/check-project-continuity-control.py",
)
EXPECTED_V2735D_CHANGED_FILES = ("app.js", "style.css")
V2735E_TEST_REPORT_FILE = "docs/WRITTEN_EXAM_REGRESSION_V2735E.md"
EXPECTED_V2735E_CLOSURE_CHANGED_FILES = EXPECTED_CONTROL_FILES + (
    V2735E_TEST_REPORT_FILE,
)
V2735G_SCORING_FIX_REPORT_FILE = "docs/WRITTEN_EXAM_SCORING_FIX_V2735G.md"
V2735G_LATER_ALLOWED_FILES = ("app.js", V2735G_SCORING_FIX_REPORT_FILE)
V2735G_LATER_ALLOWED_FIELD_VALUE = (
    f"`app.js`, `{V2735G_SCORING_FIX_REPORT_FILE}`"
)

V2735G_REGRESSION_QUESTION_IDS = (
    "straf_009",
    "bgb_009",
    "waffen_004",
    "straf_004",
    "v23_roso_007",
    "technik_004",
    "straf_006",
    "bgb_012",
    "bgb_004",
    "straf_013",
    "bgb_006",
    "uvv_004",
    "uvv_008",
)

V2735F_RESERVATION_SENTENCE = (
    "`v27.35f` ist nicht autorisiert und wird jetzt nicht bearbeitet."
)
V2735F_ACTIVE_FORBIDDEN_PATTERNS = (
    "Task-ID: v27.35f",
    "Aktuell autorisierter Task: v27.35f",
    "CURRENT_TASK ist `v27.35f`",
    "CURRENT_TASK` ist `v27.35f`",
    "v27.35f / AUTHORIZED",
    "v27.35f wird automatisch",
    "v27.35f wird jetzt bearbeitet",
    "v27.35f ist autorisiert",
    "v27.35f wird bearbeitet",
)

# Keine zukünftige Task-ID als aktiven Task einführen.
# v27.35f darf ausdrücklich als reservierter, nicht autorisierter Kandidat
# erwähnt werden (siehe V2735F_RESERVATION_SENTENCE); v27.36 bleibt
# vollständig gesperrt.
FORBIDDEN_FUTURE_TASK_MARKERS = ("v27.36",)

WORK_PATH = r"C:\a34a"
HOME_PATH = r"C:\xampp\htdocs\accaoui\v4-dashboard"
WORK_PATH_GIT_BASH = "/c/a34a"
HOME_PATH_GIT_BASH = "/c/xampp/htdocs/accaoui/v4-dashboard"

EXPECTED_STATE_FIELDS = {
    "Stand": "v27.35g",
    "Repository": "`asarrad-bit/accaoui-34a-lernapp`",
    "Branch": "`main`",
    "Letzter abgeschlossener funktionaler Stand": "v27.35d",
    "Abschlusscommit": f"`{V2735D_COMPLETION_SHA}`",
    "Aktueller HEAD": "DYNAMISCH ZU PRÜFEN",
    "Funktionsstatus": "v27.35d abgeschlossen",
    "Weiterer funktionaler Schritt autorisiert": "JA",
    "Aktuell autorisierter Task": "v27.35g",
    "Aktueller Blocker": "KEINER für v27.35g; jeder weitere Schritt bleibt gesperrt",
}

EXPECTED_TASK_FIELDS = {
    "Task-ID": "v27.35g",
    "Status": "AUTHORIZED",
    "Autorisiert": "JA",
    "Titel": "Punkteberechnung schriftliche Prüfung korrigieren",
    "Funktionaler Ausgangsstand": "v27.35d",
    "Erwarteter Ausgangscommit": f"`{V2735G_GATE_SHA}`",
    "Erlaubte Dateien": V2735G_LATER_ALLOWED_FIELD_VALUE,
    "Commit erlaubt": "NEIN",
    "Push erlaubt": "NEIN",
}

STATE_CONTRADICTORY_VALUES = (
    "Stand: v27.35e",
    "Stand: v27.35f",
    "Aktuell autorisierter Task: v27.35e",
    "Aktuell autorisierter Task: v27.35f",
    "Aktuell autorisierter Task: NONE",
    "Weiterer funktionaler Schritt autorisiert: NEIN",
)

STATE_REQUIRED_MARKERS = (
    "## Abgeschlossener Regressionstest v27.35e (FAIL)",
    "erwarteter Ausgangscommit `260e6527208769f18018d1db6e6e3b7fbe9d7d7e`",
    f"erlaubte Datei `{V2735E_TEST_REPORT_FILE}`",
    "wurde vollständig durchgeführt und mit Gesamtergebnis FAIL abgeschlossen",
    f"Testbericht-Commit: `{V2735G_GATE_SHA}`.",
    "Es wurde in v27.35e keine Codekorrektur vorgenommen",
    "## Autorisierter Task v27.35g",
    f"erwarteter Ausgangscommit `{V2735G_GATE_SHA}`",
    "für die spätere Umsetzung ausschließlich erlaubte Dateien `app.js` und "
    f"`{V2735G_SCORING_FIX_REPORT_FILE}`",
    "Ziel von v27.35g: Die Punkteberechnung der schriftlichen Prüfung so korrigieren,",
    "Verbindlicher Bewertungsvertrag:",
    "In diesem Steuerungsschritt wird `app.js` noch nicht verändert;",
    V2735F_RESERVATION_SENTENCE,
    "Der funktionale Stand bleibt v27.35d, bis v27.35g abgeschlossen ist.",
    "Kein Folgeschritt nach v27.35g ist ausgewählt oder autorisiert.",
    "## Abgeschlossener funktionaler Stand v27.35d",
    "Lernmodus eindeutig als „Lernmodus – Wissen prüfen“ gekennzeichnet.",
    "Lernkarten eindeutig als „Lernkarten – Wissen selbst einschätzen“ gekennzeichnet.",
    "Gemeinsame kompakte CSS-Klasse `mode-guidance-v2735d` für beide Führungshinweise.",
    "Keine neue Speicherung, keine neuen Storage-Keys, keine Fragenänderung.",
    "Keine Supabase-, SQL-, Datenbank- oder Netzwerkänderung.",
    "Bestehende Navigation, Pause/Fortsetzen und localStorage-Logik unverändert.",
    f"Funktionaler Abschlusscommit von v27.35d: `{V2735D_COMPLETION_SHA}`.",
    f"Historisch: Der v27.35c-Steuerungscommit `{CONTROL_COMMIT_SHA}`",
    f"Der nichtfunktionale Checker-Fix `{CHECKER_FIX_SHA}`",
    "## Historisch: Nichtfunktionale Task-Steuerung v27.35c",
    "Die Projektsteuerung wurde von Task-ID NONE, Status BLOCKED und",
    "Autorisiert NEIN verbindlich auf den einzigen autorisierten Folgetask",
    "v27.35d umgestellt.",
    "Der letzte abgeschlossene funktionale Stand blieb",
    "zu diesem Zeitpunkt unverändert v27.35b.",
    "Der Kontinuitäts-Checker erzwang diese v27.35c-Pflichtaussagen und",
    "die automatische Auswahl eines weiteren Tasks.",
    "während v27.35c gegenüber dem Ausgangscommit unverändert blieben.",
    "Der funktionale Folgeschritt v27.35d wurde erst danach umgesetzt und",
    "## Abgeschlossener funktionaler Stand v27.35b",
    "Dashboard „Ihr nächster Lernschritt“ ist abgeschlossen.",
    f"Der v27.35b-Abschlusscommit lautet `{COMPLETION_SHA}`.",
    "„Letzter abgeschlossener funktionaler Stand: v27.34b“.",
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
    "## Ziel von v27.35g",
    "Die Punkteberechnung der schriftlichen Prüfung so korrigieren, dass",
    "## Verbindlicher Bewertungsvertrag",
    "Keine Antwort: 0 Punkte.",
    "Zwei-Punkte-Frage mit nur einer richtigen Antwort: vollständig richtig",
    "## Akzeptanzkriterien",
    "Alle 82 Core-Fragen vollständig richtig: exakt 120/120 Punkte.",
    "muss nach der",
    "Korrektur rechnerisch exakt 114/120 ergeben.",
    f"Der bestehende Bericht `{V2735E_TEST_REPORT_FILE}` darf",
    "## Verboten",
    "`questions.json`",
    "`tools/preflight.py`",
    "## Hinweis zu v27.35f",
    V2735F_RESERVATION_SENTENCE,
    "## Abgeschlossener Regressionstest v27.35e (FAIL)",
    "wurde durchgeführt und mit",
    "Gesamtergebnis FAIL abgeschlossen.",
    "Es wurde keine Codekorrektur vorgenommen;",
    "## Verbindliche Sperre",
    "Kein Folgeschritt nach v27.35g wird automatisch gewählt oder autorisiert.",
    "`v27.35f` ist nicht autorisiert und wird jetzt nicht bearbeitet.",
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
    "Stand: v27.35g",
    "Arbeit: `C:\\a34a`",
    "Zuhause: `C:\\xampp\\htdocs\\accaoui\\v4-dashboard`",
    "Letzter abgeschlossener funktionaler Stand: v27.35d",
    f"Abschlusscommit: `{V2735D_COMPLETION_SHA}`",
    "| v24.6c | Pausieren/Fortsetzen Prüfung und Lernen | **erledigt** |",
    "**Erledigt:** v24.6b (Wiederholung/offene Fragen), v24.6c (Pausieren/Fortsetzen),",
    "## 14. Nächster sinnvoller Schritt",
    "`CURRENT_TASK` ist `v27.35g` / `AUTHORIZED`.",
    "Der Regressionstest v27.35e ist mit Gesamtergebnis FAIL abgeschlossen",
    V2735F_RESERVATION_SENTENCE,
    "Kein nächster funktionaler Task ist über v27.35g hinaus ausgewählt oder automatisch abgeleitet.",
    "## 15. Wenn ein neuer Chat beginnt",
    "Zuerst vollständig lesen:",
    REQUIRED_CHAT_READING_BLOCK,
    "docs/CURSOR_MASTER_CONTEXT_ACCAOUI.md",
    "docs/SUPABASE_EXAM_QUESTION_DATABASE_PLAN.md",
)

CURSOR_V2735G_EXACT_MARKERS = (
    "Stand: v27.35g\nProjekt:",
    "Arbeit: `C:\\a34a`",
    "Zuhause: `C:\\xampp\\htdocs\\accaoui\\v4-dashboard`",
    "Letzter abgeschlossener funktionaler Stand: v27.35d",
    f"Abschlusscommit: `{V2735D_COMPLETION_SHA}`",
    "| v24.6c | Pausieren/Fortsetzen Prüfung und Lernen | **erledigt** |",
    "## 14. Nächster sinnvoller Schritt",
    "`CURRENT_TASK` ist `v27.35g` / `AUTHORIZED`.",
    "Kein nächster funktionaler Task ist über v27.35g hinaus ausgewählt oder automatisch abgeleitet.",
    REQUIRED_CHAT_READING_BLOCK,
)

CURSOR_NEW_CHAT_LOCAL_HEAD_MARKERS = (
    "git rev-parse HEAD",
    "Lokalen und GitHub-HEAD direkt vergleichen",
)

STATE_V2735G_EXACT_MARKERS = (
    "Stand: v27.35g\nRepository:",
    f"Abschlusscommit: `{V2735D_COMPLETION_SHA}`",
    "## Abgeschlossener Regressionstest v27.35e (FAIL)",
    "## Autorisierter Task v27.35g",
    "Aktuell autorisierter Task: v27.35g",
    "Weiterer funktionaler Schritt autorisiert: JA",
)

TASK_V2735G_EXACT_MARKERS = (
    "Task-ID: v27.35g",
    "Status: AUTHORIZED",
    "Autorisiert: JA",
    f"Erlaubte Dateien: {V2735G_LATER_ALLOWED_FIELD_VALUE}",
    "## Ziel von v27.35g",
    "## Verbindlicher Bewertungsvertrag",
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
    "| v27.35c |",
    "### Nichtfunktionale Task-Steuerung v27.35c",
    "- `docs/PROJECT_STATE_CURRENT.md` steht auf v27.35c und dokumentiert v27.35b als unveränderten letzten funktionalen Stand sowie v27.35d als einzigen autorisierten Task.",
    "Backlog-Kandidaten B (Regressionstest) und C (Quellen/mündliche Musterfragen) sind ausdrücklich nicht autorisiert.",
    "`CURRENT_TASK` stand während v27.35c auf `AUTHORIZED` für `v27.35d`; v27.35d ist inzwischen abgeschlossen (siehe unten).",
    "`CURRENT_TASK` steht jetzt auf `Task-ID: NONE`, `Status: BLOCKED`, `Autorisiert: NEIN`; kein weiterer Folgeschritt nach v27.35d ist ausgewählt oder autorisiert.",
    "| v27.35d |",
    "### Abgeschlossener funktionaler Stand v27.35d",
    f"Abschlusscommit: `{V2735D_COMPLETION_SHA}`.",
    f"Historisch: Der nichtfunktionale Checker-Fix `{CHECKER_FIX_SHA}`",
    "| v27.35e |",
    "| v27.35f |",
    "| v27.35g |",
    "### Abgeschlossener Regressionstest v27.35e (FAIL)",
    "### Autorisierter Task v27.35g",
    f"Testbericht-Commit `{V2735G_GATE_SHA}`",
    "Gesamtergebnis: **FAIL**.",
    "Gemäß Fehlerregel wurde sofort gestoppt: keine Codekorrektur, kein zusätzlicher Dateiumfang, kein Commit, kein Push in v27.35e.",
    "Ziel von v27.35g: Die Punkteberechnung der schriftlichen Prüfung so korrigieren,",
    "Verbindlicher Bewertungsvertrag: keine Antwort ergibt 0 Punkte;",
    V2735F_RESERVATION_SENTENCE,
    "Diese Bestands- und Backlogliste ist keine Task-Autorisierung.",
    "`CURRENT_TASK` ist aktuell `v27.35g` / `AUTHORIZED` (Punkteberechnung schriftliche Prüfung korrigieren); v27.35d bleibt der letzte abgeschlossene funktionale Stand, bis v27.35g abgeschlossen ist.",
    "Backlog-Kandidat C (Quellen/mündliche Musterfragen) ist nicht autorisiert.",
    "`v27.35f` (Wettbewerbsbeobachtungsnotiz) bleibt vorgemerkt und ausdrücklich nicht autorisiert.",
    REQUIRED_CHAT_READING_BLOCK,
)

MASTERLIST_V2735G_EXACT_MARKERS = (
    "Stand: v27.35g\nBranch:",
    f"Arbeits-Laptop: `{WORK_PATH}`",
    f"Zuhause-Laptop: `{HOME_PATH}`",
    "| v27.35g |",
    "### Autorisierter Task v27.35g",
    "`CURRENT_TASK` ist aktuell `v27.35g` / `AUTHORIZED` (Punkteberechnung schriftliche Prüfung korrigieren); v27.35d bleibt der letzte abgeschlossene funktionale Stand, bis v27.35g abgeschlossen ist.",
    "Backlog-Kandidat C (Quellen/mündliche Musterfragen) ist nicht autorisiert.",
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


def validate_v2735f_not_active(text: str, document_name: str) -> None:
    for forbidden_pattern in V2735F_ACTIVE_FORBIDDEN_PATTERNS:
        require(
            forbidden_pattern not in text,
            (
                f"{document_name}: v27.35f darf nicht als aktiv oder "
                f"autorisiert erscheinen: {forbidden_pattern}"
            ),
        )


def validate_v2735g_regression_ids(text: str, document_name: str) -> None:
    for question_id in V2735G_REGRESSION_QUESTION_IDS:
        marker = f"`{question_id}`"
        require(
            marker in text,
            f"{document_name}: betroffene Fragen-ID der v27.35e-Regression fehlt: {question_id}",
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
        STATE_V2735G_EXACT_MARKERS,
        "PROJECT_STATE_CURRENT",
    )
    validate_v2735g_regression_ids(text, "PROJECT_STATE_CURRENT")
    validate_v2735f_not_active(text, "PROJECT_STATE_CURRENT")

    for contradictory_value in STATE_CONTRADICTORY_VALUES:
        require(
            contradictory_value not in text,
            f"PROJECT_STATE_CURRENT enthält widersprüchlichen Wert: {contradictory_value}",
        )

    commit_shas = set(re.findall(r"\b[0-9a-f]{40}\b", text))
    require(
        commit_shas
        == {
            GATE_SHA,
            COMPLETION_SHA,
            CONTROL_COMMIT_SHA,
            CHECKER_FIX_SHA,
            V2735D_COMPLETION_SHA,
            V2735E_GATE_SHA,
            V2735G_GATE_SHA,
        },
        (
            "PROJECT_STATE_CURRENT darf nur die historisch bekannten Commits "
            "(Gate, v27.35b-Abschluss, v27.35c-Steuerung, Checker-Fix, "
            "v27.35d-Abschluss, v27.35e-Ausgangscommit, v27.35e-FAIL-Bericht/"
            "v27.35g-Ausgangscommit) enthalten"
        ),
    )
    for forbidden_marker in FORBIDDEN_FUTURE_TASK_MARKERS:
        require(
            forbidden_marker not in text,
            "PROJECT_STATE_CURRENT darf keinen weiteren Folgeschritt auswählen oder nennen",
        )


TASK_CONTRADICTORY_GRANTS = (
    "Status: BLOCKED",
    "Autorisiert: NEIN",
    "Commit erlaubt: JA",
    "Push erlaubt: JA",
    "Task-ID: NONE",
    "Task-ID: v27.35d",
    "Task-ID: v27.35e",
    "Task-ID: v27.35f",
    "Task-ID: v27.36",
)


def validate_task_text(text: str) -> None:
    validate_exact_fields(text, EXPECTED_TASK_FIELDS)
    validate_required_markers(text, TASK_REQUIRED_MARKERS, "CURRENT_TASK")
    validate_exact_markers(text, TASK_V2735G_EXACT_MARKERS, "CURRENT_TASK")
    validate_v2735g_regression_ids(text, "CURRENT_TASK")
    validate_v2735f_not_active(text, "CURRENT_TASK")

    require(
        f"`{V2735E_TEST_REPORT_FILE}` darf" in text
        or f"`{V2735E_TEST_REPORT_FILE}` bleibt" in text,
        "CURRENT_TASK: Schutz des bestehenden v27.35e-Testberichts fehlt",
    )

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
    for contradictory_grant in TASK_CONTRADICTORY_GRANTS:
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


def validate_cursor_context_text(text: str) -> None:
    validate_required_markers(
        text,
        CURSOR_REQUIRED_MARKERS,
        "CURSOR_MASTER_CONTEXT_ACCAOUI",
    )
    validate_exact_markers(
        text,
        CURSOR_V2735G_EXACT_MARKERS,
        "CURSOR_MASTER_CONTEXT_ACCAOUI",
    )
    validate_project_paths(text, "CURSOR_MASTER_CONTEXT_ACCAOUI")
    validate_v2735f_not_active(text, "CURSOR_MASTER_CONTEXT_ACCAOUI")
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
        V2735F_RESERVATION_SENTENCE in next_task_section,
        "CURSOR_MASTER_CONTEXT_ACCAOUI: v27.35f-Reservierungshinweis fehlt im nächsten Schritt",
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
        exact_field(text, "Stand") == "v27.35g",
        "Masterliste muss exakt auf Stand v27.35g stehen",
    )
    validate_required_markers(
        text,
        MASTERLIST_REQUIRED_MARKERS,
        "PROJECT_MASTERLIST",
    )
    validate_exact_markers(
        text,
        MASTERLIST_V2735G_EXACT_MARKERS,
        "PROJECT_MASTERLIST",
    )
    validate_project_paths(text, "PROJECT_MASTERLIST")
    validate_v2735g_regression_ids(text, "PROJECT_MASTERLIST")
    validate_v2735f_not_active(text, "PROJECT_MASTERLIST")

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


def validate_v2735c_control_commit_history() -> None:
    """Prüft den v27.35c-Steuerungscommit ausschließlich historisch.

    Geprüft wird nur der abgeschlossene Bereich zwischen dem
    Ausgangscommit (GATE_SHA) und dem abgeschlossenen
    Steuerungscommit (CONTROL_COMMIT_SHA). Diese Prüfung vergleicht
    weder gegen den aktuellen HEAD nach dem Steuerungscommit noch
    gegen den aktuellen Arbeitsbaum, damit für v27.35d ausdrücklich
    autorisierte Arbeitsbaumänderungen an app.js, index.html und
    style.css dadurch nicht blockiert werden.
    """
    require(
        (ROOT / ".git").exists(),
        "Kein Git-Repository unter ROOT gefunden; Dateiprüfung nicht möglich",
    )
    for relative_path, absolute_path in (
        ("app.js", APP_JS_PATH),
        ("index.html", INDEX_HTML_PATH),
        ("style.css", STYLE_CSS_PATH),
    ):
        require(
            absolute_path.is_file(),
            f"{relative_path} fehlt; erwartete Kern-Datei nicht gefunden",
        )

    run_git(["merge-base", "--is-ancestor", GATE_SHA, CONTROL_COMMIT_SHA])
    run_git(["merge-base", "--is-ancestor", CONTROL_COMMIT_SHA, "HEAD"])

    control_changed_files = {
        line.strip()
        for line in run_git(
            ["diff", "--name-only", GATE_SHA, CONTROL_COMMIT_SHA]
        ).splitlines()
        if line.strip()
    }
    require(
        control_changed_files == set(EXPECTED_CONTROL_FILES),
        (
            "v27.35c-Steuerungscommit veränderte zwischen Ausgangscommit "
            f"{GATE_SHA} und Steuerungscommit {CONTROL_COMMIT_SHA} nicht "
            f"exakt die erwarteten Steuerungsdateien: {sorted(control_changed_files)}"
        ),
    )

    for relative_path in PROTECTED_RUNTIME_FILES:
        historical_diff = run_git(
            [
                "diff",
                "--name-only",
                GATE_SHA,
                CONTROL_COMMIT_SHA,
                "--",
                relative_path,
            ]
        ).strip()
        require(
            historical_diff == "",
            (
                f"{relative_path} wurde im historisch abgeschlossenen "
                f"v27.35c-Steuerungsbereich zwischen {GATE_SHA} und "
                f"{CONTROL_COMMIT_SHA} verändert"
            ),
        )


def validate_v2735d_completion_commit_history() -> None:
    """Prüft den funktionalen v27.35d-Abschluss ausschließlich historisch.

    Geprüft wird der abgeschlossene Bereich zwischen dem
    nichtfunktionalen Checker-Fix (CHECKER_FIX_SHA) und dem
    funktionalen Abschlusscommit von v27.35d (V2735D_COMPLETION_SHA).
    """
    require(
        (ROOT / ".git").exists(),
        "Kein Git-Repository unter ROOT gefunden; Dateiprüfung nicht möglich",
    )

    run_git(["merge-base", "--is-ancestor", CHECKER_FIX_SHA, V2735D_COMPLETION_SHA])
    run_git(["merge-base", "--is-ancestor", V2735D_COMPLETION_SHA, V2735E_GATE_SHA])
    run_git(["merge-base", "--is-ancestor", V2735E_GATE_SHA, V2735G_GATE_SHA])

    completion_changed_files = {
        line.strip()
        for line in run_git(
            ["diff", "--name-only", CHECKER_FIX_SHA, V2735D_COMPLETION_SHA]
        ).splitlines()
        if line.strip()
    }
    require(
        completion_changed_files == set(EXPECTED_V2735D_CHANGED_FILES),
        (
            "v27.35d-Abschlusscommit veränderte zwischen Checker-Fix "
            f"{CHECKER_FIX_SHA} und Abschlusscommit {V2735D_COMPLETION_SHA} "
            f"nicht exakt die erwarteten Dateien: {sorted(completion_changed_files)}"
        ),
    )

    for relative_path in PROTECTED_RUNTIME_FILES:
        historical_diff = run_git(
            [
                "diff",
                "--name-only",
                V2735D_COMPLETION_SHA,
                V2735E_GATE_SHA,
                "--",
                relative_path,
            ]
        ).strip()
        require(
            historical_diff == "",
            (
                f"{relative_path} wurde zwischen dem v27.35d-Abschlusscommit "
                f"{V2735D_COMPLETION_SHA} und dem v27.35e-Ausgangscommit "
                f"{V2735E_GATE_SHA} verändert"
            ),
        )


def validate_v2735e_closure_commit_history() -> None:
    """Prüft den abgeschlossenen v27.35e-Regressionstest ausschließlich historisch.

    Geprüft wird der abgeschlossene Bereich zwischen dem v27.35e-
    Ausgangscommit (V2735E_GATE_SHA) und dem FAIL-Testbericht-Commit,
    der zugleich der erwartete Ausgangscommit von v27.35g ist
    (V2735G_GATE_SHA).
    """
    require(
        (ROOT / ".git").exists(),
        "Kein Git-Repository unter ROOT gefunden; Dateiprüfung nicht möglich",
    )

    run_git(["merge-base", "--is-ancestor", V2735E_GATE_SHA, V2735G_GATE_SHA])
    run_git(["merge-base", "--is-ancestor", V2735G_GATE_SHA, "HEAD"])

    closure_changed_files = {
        line.strip()
        for line in run_git(
            ["diff", "--name-only", V2735E_GATE_SHA, V2735G_GATE_SHA]
        ).splitlines()
        if line.strip()
    }
    require(
        closure_changed_files == set(EXPECTED_V2735E_CLOSURE_CHANGED_FILES),
        (
            "v27.35e-Abschluss veränderte zwischen Ausgangscommit "
            f"{V2735E_GATE_SHA} und FAIL-Bericht/v27.35g-Ausgangscommit "
            f"{V2735G_GATE_SHA} nicht exakt die erwarteten Dateien: "
            f"{sorted(closure_changed_files)}"
        ),
    )

    for relative_path in PROTECTED_RUNTIME_FILES:
        historical_diff = run_git(
            [
                "diff",
                "--name-only",
                V2735E_GATE_SHA,
                V2735G_GATE_SHA,
                "--",
                relative_path,
            ]
        ).strip()
        require(
            historical_diff == "",
            (
                f"{relative_path} wurde zwischen dem v27.35e-Ausgangscommit "
                f"{V2735E_GATE_SHA} und dem v27.35g-Ausgangscommit "
                f"{V2735G_GATE_SHA} verändert"
            ),
        )


def validate_v2735g_gate_working_tree() -> None:
    """Prüft, dass Funktionsdateien seit dem v27.35g-Ausgangscommit unverändert sind."""
    require(
        (ROOT / ".git").exists(),
        "Kein Git-Repository unter ROOT gefunden; Dateiprüfung nicht möglich",
    )
    run_git(["merge-base", "--is-ancestor", V2735G_GATE_SHA, "HEAD"])

    for relative_path in PROTECTED_RUNTIME_FILES:
        committed_diff = run_git(
            ["diff", "--name-only", V2735G_GATE_SHA, "HEAD", "--", relative_path]
        ).strip()
        require(
            committed_diff == "",
            (
                f"{relative_path} wurde seit dem v27.35g-Ausgangscommit "
                f"{V2735G_GATE_SHA} in committeten Änderungen verändert"
            ),
        )
        working_tree_diff = run_git(
            ["diff", "--name-only", "HEAD", "--", relative_path]
        ).strip()
        require(
            working_tree_diff == "",
            (
                f"{relative_path} wurde im Arbeitsbaum gegenüber HEAD verändert; "
                "in diesem v27.35g-Steuerungsschritt sind Funktionsdateien "
                "noch nicht erlaubt"
            ),
        )

    changed_report_diff = run_git(
        ["diff", "--name-only", "HEAD", "--", V2735E_TEST_REPORT_FILE]
    ).strip()
    require(
        changed_report_diff == "",
        (
            f"{V2735E_TEST_REPORT_FILE} wurde im Arbeitsbaum verändert; der "
            "bestehende v27.35e-Testbericht darf nicht verändert werden"
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
        "Stand": "v27.35f",
        "Repository": "`anderes/repository`",
        "Branch": "`anderer-branch`",
        "Letzter abgeschlossener funktionaler Stand": "v27.35b",
        "Abschlusscommit": f"`{'0' * 40}`",
        "Aktueller HEAD": GATE_SHA,
        "Funktionsstatus": "v27.35g abgeschlossen",
        "Weiterer funktionaler Schritt autorisiert": "NEIN",
        "Aktuell autorisierter Task": "v27.35f",
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
        state_text + "v27.36 wird als Folgeschritt vorgemerkt.\n",
        "PROJECT_STATE_CURRENT automatische Auswahl eines weiteren Tasks",
    )
    checks += 1

    must_reject(
        validate_state_text,
        state_text + "v27.35f wird jetzt bearbeitet.\n",
        "PROJECT_STATE_CURRENT v27.35f wird unzulässig aktiviert",
    )
    checks += 1

    for contradictory_value in STATE_CONTRADICTORY_VALUES:
        must_reject(
            validate_state_text,
            state_text + f"{contradictory_value}\n",
            f"PROJECT_STATE_CURRENT widersprüchlicher Wert: {contradictory_value}",
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
        "Task-ID": "v27.35f",
        "Status": "BLOCKED",
        "Autorisiert": "NEIN",
        "Titel": "Anderer Task",
        "Funktionaler Ausgangsstand": "v27.35c",
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
            f"Erlaubte Dateien: {V2735G_LATER_ALLOWED_FIELD_VALUE}",
            f"Erlaubte Dateien: {V2735G_LATER_ALLOWED_FIELD_VALUE}, `index.html`",
            "CURRENT_TASK erlaubte Dateien unzulässig erweitert",
        ),
        "CURRENT_TASK erlaubte Dateien unzulässig erweitert",
    )
    checks += 1

    for contradictory_grant in TASK_CONTRADICTORY_GRANTS:
        must_reject(
            validate_task_text,
            task_text + f"{contradictory_grant}\n",
            f"CURRENT_TASK widersprüchliche Freigabe: {contradictory_grant}",
        )
        checks += 1

    must_reject(
        validate_task_text,
        task_text + "v27.35f wird jetzt bearbeitet.\n",
        "CURRENT_TASK v27.35f wird unzulässig aktiviert",
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
            "Kein Folgeschritt nach v27.35g wird automatisch gewählt oder autorisiert.",
            "`v27.35f` wird automatisch gewählt und autorisiert.",
            "automatische Auswahl eines Folgeschritts",
        ),
        "automatische Auswahl eines Folgeschritts",
    )
    checks += 1

    for question_id in V2735G_REGRESSION_QUESTION_IDS:
        marker = f"`{question_id}`"
        require(
            marker in task_text,
            f"Manipulationsmatrix kann Ausgangswert nicht finden: {question_id}",
        )
        fully_removed_task_text = task_text.replace(marker, "")
        require(
            fully_removed_task_text != task_text,
            f"Manipulationsmatrix blieb wirkungslos: {question_id}",
        )
        must_reject(
            validate_task_text,
            fully_removed_task_text,
            f"CURRENT_TASK betroffene Fragen-ID entfernt: {question_id}",
        )
        checks += 1

    checks += exercise_exact_marker_manipulations(
        validate_state_text,
        state_text,
        STATE_V2735G_EXACT_MARKERS,
        "PROJECT_STATE_CURRENT",
    )
    checks += exercise_exact_marker_manipulations(
        validate_task_text,
        task_text,
        TASK_V2735G_EXACT_MARKERS,
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
        CURSOR_V2735G_EXACT_MARKERS,
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
        "Kein nächster funktionaler Task ist über v27.35g hinaus ausgewählt oder automatisch abgeleitet.",
        (
            "Kein nächster funktionaler Task ist über v27.35g hinaus ausgewählt oder automatisch abgeleitet.\n"
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
        "Kein nächster funktionaler Task ist über v27.35g hinaus ausgewählt oder automatisch abgeleitet.",
        (
            "Kein nächster funktionaler Task ist über v27.35g hinaus ausgewählt oder automatisch abgeleitet.\n"
            "**v27.35f wird automatisch fortgesetzt.**"
        ),
        "Cursor unzulässige weitere Task-Auswahl v27.35f",
    )
    must_reject(
        validate_cursor_context_text,
        manipulated_cursor_future_task_text,
        "Cursor unzulässige weitere Task-Auswahl v27.35f",
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
        MASTERLIST_V2735G_EXACT_MARKERS,
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
        validate_v2735c_control_commit_history()
        validate_v2735d_completion_commit_history()
        validate_v2735e_closure_commit_history()
        validate_v2735g_gate_working_tree()
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

    print("Projektkontinuität und Task-Steuerung v27.35g: OK")
    print("PROJECT_STATE_CURRENT: v27.35g / letzter funktionaler Stand v27.35d")
    print(
        "CURRENT_TASK: v27.35g / AUTHORIZED / kein Commit, kein Push, "
        "app.js noch nicht verändert"
    )
    print("AGENTS-Regeln, Cursor-Kontext und Chatwechsel-Protokoll: OK")
    print("Projektpfade Arbeit und Zuhause: OK")
    print("Preflight-Einbindung: OK")
    print(
        "v27.35c-Steuerungscommit historisch sauber: app.js, index.html und "
        f"style.css zwischen {GATE_SHA} und {CONTROL_COMMIT_SHA} unverändert"
    )
    print(
        "v27.35d-Abschlusscommit historisch sauber: app.js und style.css "
        f"zwischen {CHECKER_FIX_SHA} und {V2735D_COMPLETION_SHA} verändert"
    )
    print(
        "v27.35e-Regressionstest historisch sauber abgeschlossen (FAIL) "
        f"zwischen {V2735E_GATE_SHA} und {V2735G_GATE_SHA}: nur Steuerungs- "
        "und Testberichtsdateien geändert, keine Funktionsdatei"
    )
    print(
        "v27.35g-Arbeitsbaum sauber: app.js, index.html, style.css und der "
        f"bestehende v27.35e-Testbericht seit {V2735G_GATE_SHA} unverändert"
    )
    print(f"Manipulationsmatrix: {manipulation_checks} Blockierungen bestätigt")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
