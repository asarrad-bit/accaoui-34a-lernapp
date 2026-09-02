#!/usr/bin/env python3
"""Prüft die Historie bis v27.36e und den vollständigen v27.36f-Lebenszyklus.

v27.35g bleibt der letzte abgeschlossene funktionale Stand. Ab der
historischen Autorisierungsbasis werden lineare Commits anhand ihrer
tatsächlichen Dateimenge, ihres Taskzustands und des Notiz-Blob-SHA als
GATE, einmalige IMPLEMENTATION oder CLOSURE klassifiziert. Der Checker
akzeptiert die vier Phasen vor Implementation, nach Implementation,
während lokaler Closure-Vorbereitung und nach committeter Closure, ohne
einen zukünftigen Commit-SHA vorwegzunehmen. App- und Funktionsdateien,
zusätzliche Working-Tree-Dateien und unzulässige Taskübergänge bleiben
geschlossen gesperrt. Darauf aufbauend klassifiziert v27.36a alle Commits
nach der stabilen Autorisierungsbasis dynamisch als GATE, einmaligen AUDIT
oder CLOSURE und akzeptiert sechs Phasen bis zum späteren Abschluss, ohne
einen zukünftigen Commit-SHA oder den Inhalt der Audit-Datei vorwegzunehmen.
Der abgeschlossene v27.36a-Zustand wird an der stabilen v27.36b-Basis
belegt. Danach werden GATE, genau eine IMPLEMENTATION und die spätere
CLOSURE von v27.36b und v27.36c sowie alle Phasen von v27.36d dynamisch
erkannt, ohne künftige Commit-SHAs hartzucodieren. Darauf aufbauend wird
v27.36e als vollständig geschlossen belegt und v27.36f in sechs dynamischen
Phasen vom Autorisierungs-GATE bis zur späteren CLOSURE kontrolliert.
"""

from __future__ import annotations

import hashlib
import re
import subprocess
from dataclasses import dataclass, replace
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
V2735G_AUTHORIZATION_SHA = "0018334aba07e3098111e80b4eb6218b2ca898c0"
V2735G_GATE_FIX_SHA = "bbe5f6ea5366e026327c3fc0c866e1ef37ead6f0"
V2735G_COMPLETION_SHA = "f5f261fee67fc17c170ee714ae23761ff1668f17"
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
EXPECTED_V2735G_COMPLETION_CHANGED_FILES = (
    "app.js",
    V2735G_SCORING_FIX_REPORT_FILE,
)

V2735F_PREAUTHORIZATION_SHA = "003112eaeb9a071a6396634b6da92fa11ae8921a"
V2735F_AUTHORIZATION_SHA = "601dc6f751b6a603a27c4b3405150bf1d75e09fd"
V2735F_FIRST_GATE_FIX_SHA = "d4e46edc48e967509e09ddd1096b54eb0bed5971"
V2735F_NOTE_FILE = "docs/COMPETITOR_POSITIONING_NOTE_V2735F.md"
V2735F_NOTE_SHA256 = "983af73fb711cb2b77eb69b51d38ae5f4cf2991d1d976274eee0b4379ef9b023"
V2735F_GATE_CONTROL_FILES = EXPECTED_CONTROL_FILES
V2735F_TASK_RELATIVE_PATH = "docs/tasks/CURRENT_TASK.md"

V2736A_AUTHORIZATION_BASE_SHA = "d69290f9de2921886566b1bb398231bf009fc433"
V2736A_AUDIT_FILE = "docs/SUPABASE_LOGIN_CURRENT_STATE_AUDIT_V2736A.md"
V2736A_TITLE = (
    "Supabase/Login-Bestandsaudit und nächsten sicheren "
    "Umsetzungsbaustein festlegen"
)
V2736A_EXPECTED_STATE_FIELDS = {
    "Stand": "v27.35g",
    "Repository": "`asarrad-bit/accaoui-34a-lernapp`",
    "Branch": "`main`",
    "Letzter abgeschlossener funktionaler Stand": "v27.35g",
    "Abschlusscommit": f"`{V2735G_COMPLETION_SHA}`",
    "Aktueller HEAD": "DYNAMISCH ZU PRÜFEN",
    "Funktionsstatus": "v27.35g abgeschlossen",
    "Weiterer funktionaler Schritt autorisiert": "NEIN",
    "Aktuell autorisierter Task": "v27.36a",
    "Aktuelle Taskart": "Dokumentations-/Bestandsaudit",
    "Aktueller Blocker": (
        "KEINER für den ausschließlich dokumentarischen "
        "v27.36a-Bestandsaudit; jede funktionale Umsetzung und jeder "
        "Folgetask bleiben gesperrt"
    ),
}
V2736A_EXPECTED_TASK_FIELDS = {
    "Task-ID": "v27.36a",
    "Status": "AUTHORIZED",
    "Autorisiert": "JA",
    "Titel": V2736A_TITLE,
    "Funktionaler Ausgangsstand": "v27.35g",
    "Erwarteter Ausgangscommit": f"`{V2736A_AUTHORIZATION_BASE_SHA}`",
    "Erlaubte Dateien": f"`{V2736A_AUDIT_FILE}`",
    "Commit erlaubt": "NEIN",
    "Push erlaubt": "NEIN",
}
V2736A_STATE_REQUIRED_MARKERS = (
    "## Autorisierter Dokumentations-/Bestandsaudit v27.36a",
    "v27.36a ist der einzige autorisierte Task.",
    "Titel: Supabase/Login-Bestandsaudit und nächsten sicheren\nUmsetzungsbaustein festlegen.",
    f"`{V2736A_AUTHORIZATION_BASE_SHA}`.",
    f"`{V2736A_AUDIT_FILE}` erlaubt.",
    "Autorisierungsschritt führt den Audit noch nicht aus",
    "Der letzte abgeschlossene funktionale Stand bleibt v27.35g.",
    "v27.35f\nbleibt abgeschlossen.",
    "Supabase bleibt nicht live",
    "Folgetask nach v27.36a wird weder ausgewählt noch autorisiert.",
    "Commit und Push bleiben gesperrt.",
)
V2736A_TASK_REQUIRED_MARKERS = (
    "## Autorisierter Dokumentations-/Bestandsaudit v27.36a",
    "v27.36a ist der einzige autorisierte Task.",
    "führt den Audit noch nicht aus und erstellt oder verändert die spätere\nAudit-Datei noch nicht.",
    "genau\neinen kleinsten, sicher begrenzten nächsten Umsetzungsbaustein",
    "Auth-/Login-Planungen, lokale\nAuth-Guards, Config-Platzhalter und Loader, Adapter- und SDK-Readiness",
    "Geplante, lokal simulierte, vorbereitete und tatsächlich\nimplementierte Teile",
    f"`{V2736A_AUDIT_FILE}` erlaubt.",
    "weder automatisch\nauswählen noch autorisieren.",
    "Verboten bleiben App-Code-, UI-, Fragenbank-, SQL-, Migrations-,",
    "Live-Supabase",
    "echte Schlüssel",
    "Netzwerk- und Datenbankzugriffe",
    "echte\nTeilnehmerdaten",
    "Commit und Push bleiben gesperrt.",
)
V2736A_CURSOR_REQUIRED_MARKERS = (
    "`CURRENT_TASK` ist `v27.36a` / `AUTHORIZED` / `Autorisiert: JA`.",
    "Einziger autorisierter Task: Supabase/Login-Bestandsaudit und nächsten\nsicheren Umsetzungsbaustein festlegen.",
    "Taskart: Dokumentations-/Bestandsaudit.",
    f"`{V2736A_AUTHORIZATION_BASE_SHA}`.",
    f"`{V2736A_AUDIT_FILE}` erlaubt.",
    "Audit-Datei noch nicht erstellt oder\nverändert",
    "v27.35f bleibt abgeschlossen",
    "Supabase bleibt nicht live.",
    "keinen Folgetask automatisch auswählen oder\nautorisieren.",
    "Commit und Push bleiben gesperrt.",
)
V2736A_MASTERLIST_ROW = (
    "| v27.36a | Supabase/Login-Bestandsaudit und nächsten sicheren "
    "Umsetzungsbaustein festlegen: einziger autorisierter "
    "Dokumentations-/Bestandsaudit;"
)
V2736A_CLOSED_MASTERLIST_ROW = (
    "| v27.36a | Supabase/Login-Bestandsaudit abgeschlossen: Audit-Commit "
    "`f545a6c2b14a64a5bcb7bf60a2932315e571ef01`, Audit-Datei "
    "`docs/SUPABASE_LOGIN_CURRENT_STATE_AUDIT_V2736A.md`; Supabase/Login "
    "umfangreich lokal vorbereitet, aber NICHT live; genau eine nicht "
    "autorisierende Empfehlung für eine lokale injizierbare "
    "Auth-/Teilnehmerzugangs-Komponente mit lokalem Fake-Client; funktionaler "
    "Stand bleibt v27.35g, kein Folgetask ausgewählt oder autorisiert – "
    "**erledigt** |"
)
V2736A_MASTERLIST_REQUIRED_MARKERS = (
    V2736A_MASTERLIST_ROW,
    "### Autorisierter Dokumentations-/Bestandsaudit v27.36a",
    "v27.36a ist der einzige autorisierte und noch offene Task.",
    f"Titel: {V2736A_TITLE}.",
    f"Erwarteter Ausgangscommit: `{V2736A_AUTHORIZATION_BASE_SHA}`.",
    f"`{V2736A_AUDIT_FILE}` erlaubt.",
    "Supabase/Login bleibt der nächste Hauptblock.",
    "genau einen kleinsten, sicher begrenzten tatsächlichen Implementierungsschritt",
    "keinen Folgetask automatisch auswählen oder autorisieren.",
    "keinen Code, keinen Commit und keinen Push.",
)

V2736A_TASK_AUTHORIZED = "authorized"
V2736A_TASK_CLOSED = "closed"
V2736A_HISTORY_BEFORE_AUTHORIZATION = "before_authorization_commit"
V2736A_HISTORY_AUTHORIZED = "authorization_committed"
V2736A_HISTORY_AUDITED = "audit_committed"
V2736A_HISTORY_CLOSED = "closure_committed"
V2736A_PHASE_1_AUTHORIZATION_PREPARED = "phase_1_authorization_prepared"
V2736A_PHASE_2_AUTHORIZATION_COMMITTED = "phase_2_authorization_committed"
V2736A_PHASE_2_GATE_PREPARED = "phase_2_gate_correction_prepared"
V2736A_PHASE_3_AUDIT_PREPARED = "phase_3_audit_prepared"
V2736A_PHASE_4_AUDIT_COMMITTED = "phase_4_audit_committed"
V2736A_PHASE_5_CLOSURE_PREPARED = "phase_5_closure_prepared"
V2736A_PHASE_6_CLOSURE_COMMITTED = "phase_6_closure_committed"
V2736A_ROLE_GATE = "GATE"
V2736A_ROLE_AUDIT = "IMPLEMENTATION/AUDIT"
V2736A_ROLE_CLOSURE = "CLOSURE"
V2736A_CLOSED_TASK_FIELDS = {
    "Task-ID": "NONE",
    "Status": "BLOCKED",
    "Autorisiert": "NEIN",
    "Titel": "Kein Task autorisiert",
    "Funktionaler Ausgangsstand": "v27.35g",
    "Letzter abgeschlossener Kontrollschritt": "v27.36a",
    "Erlaubte Dateien": "KEINE",
    "Commit erlaubt": "NEIN",
    "Push erlaubt": "NEIN",
}
V2736A_CLOSED_STATE_FIELDS = {
    "Stand": "v27.36a",
    "Repository": "`asarrad-bit/accaoui-34a-lernapp`",
    "Branch": "`main`",
    "Letzter abgeschlossener funktionaler Stand": "v27.35g",
    "Abschlusscommit": f"`{V2735G_COMPLETION_SHA}`",
    "Aktueller HEAD": "DYNAMISCH ZU PRÜFEN",
    "Funktionsstatus": "v27.35g abgeschlossen",
    "Weiterer funktionaler Schritt autorisiert": "NEIN",
    "Aktuell autorisierter Task": "NONE",
    "Aktuelle Taskart": "Kein Task autorisiert",
    "Aktueller Blocker": (
        "Neue Taskauswahl und ausdrückliche Autorisierung durch "
        "Projekteigentümer und verbindlichen Projektchat"
    ),
}
V2736A_CLOSURE_CONTENT_MARKERS = (
    "v27.36a abgeschlossen.",
    f"Audit-Datei: `{V2736A_AUDIT_FILE}`",
    "Ergebnis: Supabase/Login ist umfangreich lokal vorbereitet, aber NICHT live.",
    "Zentrale Lücken:",
    "- kanonisches Auth-/Teilnehmerzugangsschema",
    "- SDK/öffentliche Dev-Config noch nicht aktiv",
    "- Auth-/Access-Adapter noch nicht an realen Client angebunden",
    "- keine ausgeführten echten RLS-/Datenbanktests",
    "Technische Schulden:",
    "- doppelte Config-Ladewege",
    "- isolierter Bootstrap",
    "- übergroßer zentraler Adapter",
    "- fragmentierte historische Vertrags-/Readiness-Kette",
    "Audit-Empfehlung: lokale injizierbare Auth-/Teilnehmerzugangs-Komponente\n"
    "mit lokalem Fake-Client.",
    "Diese Audit-Empfehlung ist KEINE Autorisierung.",
    "Kein Folgetask wurde ausgewählt oder autorisiert.",
    "Kein Live-Supabase.",
    "Keine echten Keys.",
    "Keine echten Teilnehmerdaten.",
    "Der letzte abgeschlossene funktionale Stand bleibt v27.35g.",
)
V2736A_STATE_LIFECYCLE_MARKERS = (
    "### Permanenter v27.36a-Lebenszyklus",
    f"`{V2736A_AUTHORIZATION_BASE_SHA}` ist die stabile",
    "muss Vorfahr jedes legitimen späteren\nHEAD bleiben",
    "Der legitime Autorisierungs-GATE-Commit der Phase 2 wird dynamisch aus",
    "dauerhaft erforderliche HEAD-Gleichheit.",
    "Git-Historie, tatsächlicher\nDateimenge, Taskstatus und Working Tree",
    "Genau ein späterer\nIMPLEMENTATION-/AUDIT-Commit",
    "Die sechs Phasen sind:",
    "Rückkehr aus der Closure bleiben gesperrt.",
    "Die Audit-Datei\nist weiterhin nicht erstellt",
    "kein Folgetask wurde ausgewählt oder\nautorisiert.",
)
V2736A_TASK_LIFECYCLE_MARKERS = (
    "## Permanenter v27.36a-Lebenszyklus",
    "Die stabile Autorisierungsbasis ist",
    f"`{V2736A_AUTHORIZATION_BASE_SHA}`",
    "Der legitime Autorisierungs-GATE-Commit der Phase 2 wird dynamisch aus der",
    "dauerhafte HEAD-Vorgabe.",
    "GATE ist eine nichtleere\nTeilmenge der fünf Gate-Dateien",
    "IMPLEMENTATION/AUDIT ist exakt nur",
    "Der Lifecycle umfasst sechs Phasen:",
    "ein\nautomatischer Folgetask und eine Rückkehr aus der Closure bleiben\ngesperrt.",
    "nicht erstellt oder inhaltlich vorweggenommen.",
    "Kein Folgetask ist\nausgewählt oder autorisiert.",
)
V2736A_CURSOR_LIFECYCLE_MARKERS = (
    "### Permanenter v27.36a-Lebenszyklus",
    f"`{V2736A_AUTHORIZATION_BASE_SHA}` ist die stabile",
    "Der legitime Autorisierungs-GATE-Commit der Phase 2 wird dynamisch aus",
    "dauerhafte HEAD-Vorgabe.",
    "Git-Historie,\nDateimenge und Taskstatus",
    "sechs Phasen:",
    "mehr als ein Audit-Commit",
    "Die Audit-Datei ist aktuell\nweiterhin nicht erstellt.",
    "Kein Folgetask ist ausgewählt oder\nautorisiert",
)
V2736A_MASTERLIST_LIFECYCLE_MARKERS = (
    "#### Permanenter v27.36a-Lebenszyklus",
    f"`{V2736A_AUTHORIZATION_BASE_SHA}` ist die stabile Autorisierungsbasis",
    "Der legitime Phase-2-Autorisierungs-GATE-Commit wird dynamisch aus",
    "Zukünftige Commit-SHAs werden nicht hartcodiert",
    "IMPLEMENTATION/AUDIT enthält exakt nur",
    "Die sechs Phasen sind:",
    "ein zweiter Audit-Commit",
    "Die Audit-Datei ist weiterhin nicht erstellt.",
)

V2735F_TASK_AUTHORIZED = "authorized"
V2735F_TASK_CLOSED = "closed"
V2735F_HISTORY_BEFORE_IMPLEMENTATION = "before_implementation"
V2735F_HISTORY_IMPLEMENTED = "implementation_committed"
V2735F_HISTORY_CLOSED = "closure_committed"
V2735F_PHASE_BEFORE_IMPLEMENTATION = "phase_1_before_implementation"
V2735F_PHASE_IMPLEMENTATION_COMMITTED = "phase_2_implementation_committed"
V2735F_PHASE_CLOSURE_PREPARED = "phase_3_closure_prepared"
V2735F_PHASE_CLOSURE_COMMITTED = "phase_4_closure_committed"
V2735F_ROLE_GATE = "GATE"
V2735F_ROLE_IMPLEMENTATION = "IMPLEMENTATION"
V2735F_ROLE_CLOSURE = "CLOSURE"

V2735F_EXPECTED_STATE_FIELDS = {
    "Stand": "v27.35g",
    "Repository": "`asarrad-bit/accaoui-34a-lernapp`",
    "Branch": "`main`",
    "Letzter abgeschlossener funktionaler Stand": "v27.35g",
    "Abschlusscommit": f"`{V2735G_COMPLETION_SHA}`",
    "Aktueller HEAD": "DYNAMISCH ZU PRÜFEN",
    "Funktionsstatus": "v27.35g abgeschlossen",
    "Weiterer funktionaler Schritt autorisiert": "NEIN",
    "Aktuell autorisierter Task": "v27.35f",
    "Aktuelle Taskart": "Dokumentation",
    "Aktueller Blocker": (
        "KEINER; v27.35f ist als einziger Dokumentationstask autorisiert, "
        "Umsetzung offen"
    ),
}

V2735F_EXPECTED_TASK_FIELDS = {
    "Task-ID": "v27.35f",
    "Status": "AUTHORIZED",
    "Autorisiert": "JA",
    "Titel": "Wettbewerbsbeobachtung und Accaoui-Positionierung dokumentieren",
    "Funktionaler Ausgangsstand": "v27.35g",
    "Erwarteter Ausgangscommit": f"`{V2735F_AUTHORIZATION_SHA}`",
    "Erlaubte Dateien": f"`{V2735F_NOTE_FILE}`",
    "Commit erlaubt": "NEIN",
    "Push erlaubt": "NEIN",
}

V2735F_CLOSED_TASK_FIELDS = {
    "Task-ID": "NONE",
    "Status": "BLOCKED",
    "Autorisiert": "NEIN",
    "Titel": "Kein Task autorisiert",
    "Erlaubte Dateien": "KEINE",
    "Commit erlaubt": "NEIN",
    "Push erlaubt": "NEIN",
}

V2735F_CLOSED_STATE_FIELDS = {
    "Stand": "v27.35g",
    "Repository": "`asarrad-bit/accaoui-34a-lernapp`",
    "Branch": "`main`",
    "Letzter abgeschlossener funktionaler Stand": "v27.35g",
    "Abschlusscommit": f"`{V2735G_COMPLETION_SHA}`",
    "Aktueller HEAD": "DYNAMISCH ZU PRÜFEN",
    "Funktionsstatus": "v27.35g abgeschlossen",
    "Weiterer funktionaler Schritt autorisiert": "NEIN",
    "Aktuell autorisierter Task": "NONE",
}


@dataclass(frozen=True)
class V2735FCommitFact:
    commit_sha: str
    changed_files: frozenset[str]
    task_state: str
    note_sha256: str | None = None


@dataclass(frozen=True)
class V2735FHistoryState:
    state: str
    implementation_commit: str | None
    roles: tuple[str, ...]


@dataclass(frozen=True)
class V2735FWorkingTreeFact:
    diff_files: frozenset[str]
    staged_files: frozenset[str]
    untracked_files: frozenset[str]
    status_lines: frozenset[str]
    note_sha256: str


@dataclass(frozen=True)
class V2736ACommitFact:
    commit_sha: str
    changed_files: frozenset[str]
    task_state: str


@dataclass(frozen=True)
class V2736AHistoryState:
    state: str
    audit_commit: str | None
    roles: tuple[str, ...]
    gate_commits: tuple[str, ...]


@dataclass(frozen=True)
class V2736AWorkingTreeFact:
    branch: str
    head: str
    origin_main: str
    diff_files: frozenset[str]
    staged_files: frozenset[str]
    untracked_files: frozenset[str]
    status_lines: frozenset[str]
    audit_file_exists: bool
    audit_file_tracked_at_base: bool
    audit_file_tracked_at_head: bool
    base_is_head_ancestor: bool
    base_is_origin_ancestor: bool
    origin_is_head_ancestor: bool

V2735F_STATE_REQUIRED_MARKERS = (
    "## Autorisierter Dokumentationstask v27.35f",
    "`docs/tasks/CURRENT_TASK.md` steht auf `Task-ID: v27.35f`",
    "`Status: AUTHORIZED`, `Autorisiert: JA`",
    "`Funktionaler Ausgangsstand: v27.35g`",
    "funktionaler Ausgangs- und\nVorautorisierungsstand",
    f"`{V2735F_PREAUTHORIZATION_SHA}`",
    "v27.35f-Autorisierungscommit\nund Umsetzungsbasis",
    f"`{V2735F_AUTHORIZATION_SHA}`",
    f"`{V2735F_NOTE_FILE}`",
    "v27.35g bleibt der letzte abgeschlossene funktionale Stand.",
    "der einzige autorisierte Dokumentationstask; seine Umsetzung ist offen.",
    "beobachtete, nicht extern verifizierte",
    "„Mit dieser App habe ich es endlich verstanden.“",
    "Im abgeschlossenen Autorisierungsschritt wurde",
    "noch nicht erstellt oder",
    "In diesem Schritt wurde keine Wettbewerbsnotiz erstellt,",
    "kein Folgetask automatisch ausgewählt.",
    "Commit und Push blieben gesperrt.",
    "### Separater nichtfunktionaler v27.35f-Implementierungs-Gate-Korrekturschritt",
    f"`{V2735F_FIRST_GATE_FIX_SHA}` ist ein legitimer",
    "starre Gleichheitsprüfung auf",
    "begrenzt den gesamten committeten Diff",
    "Der Working Tree darf entweder exakt die fünf modifizierten Gate-Dateien",
    f"SHA-256\n`{V2735F_NOTE_SHA256}`",
    "### Verbindliche v27.35f-Lebenszyklus-State-Machine",
    "Die State-Machine akzeptiert vier Zustände",
    "dynamisch aus Git ermittelten",
    "Closure ist erst nach dynamischem Nachweis des Implementation-Commits",
    "v27.35f bleibt der einzige aktive Task",
    "Commit und Push bleiben\nverboten; ein Folgetask wird nicht ausgewählt oder autorisiert.",
)

V2735F_TASK_REQUIRED_MARKERS = (
    "# Verbindlicher aktueller Task",
    "## Ziel",
    "interne strategische Dokumentation",
    "## Verbindliche Grundlage",
    "beobachtete und nicht",
    "extern verifizierte Wettbewerber-Werbeaussagen",
    "niedriger Einmalpreis",
    "zeitlich unbegrenzte Prüfungssimulationen",
    "behauptete Abdeckung aller IHK-Fragen",
    "behauptetes KI-basiertes Erkennen von Schwächen",
    "Rückerstattungs- oder Risikoumkehr-Versprechen",
    "dauerhafter Besitz beziehungsweise unbegrenzter Zugang",
    "Nutzerzahlen, Bewertungen oder sonstiger Social Proof",
    "## Zulässige allgemeine Marketingmechanismen",
    "Preisanker",
    "Verlustvermeidung",
    "klare Nutzenkommunikation",
    "Risikoumkehr",
    "Social Proof",
    "Einfachheit des Angebots",
    "persönliche Schwächenanalyse",
    "Prüfungssimulation als konkretes Leistungsversprechen",
    "## Verbindliche Accaoui-Differenzierung",
    "Wissen verständlich vermitteln",
    "typische Fehler erkennen und gezielt bearbeiten",
    "Inhalte langfristig festigen",
    "realistische schriftliche und mündliche Prüfungsvorbereitung",
    "nachvollziehbare persönliche Lernführung",
    "Teilnehmer bis zur Prüfungsreife begleiten",
    "echte Unterrichts- und Prüfungsvorbereitungserfahrung",
    "nicht nur Fragen beantworten, sondern Inhalte verstehen",
    "## Qualitätsmaßstab",
    "„Mit dieser App habe ich es endlich verstanden.“",
    "Die Leitidee aus `docs/PROJECT_MASTERLIST.md` bleibt verbindlich.",
    "## Verboten",
    "Wettbewerbertexte kopieren",
    "geschützte Formulierungen nachahmen",
    "behaupten, der Wettbewerber lüge oder handle rechtswidrig",
    "nicht belegte Nutzerzahlen oder Bewertungen als Tatsachen darstellen",
    "behaupten, Accaoui besitze alle originalen IHK-Fragen",
    "Bestehensgarantien",
    "unbelegte KI-Versprechen",
    "unbelegte Rückerstattungsversprechen",
    "konkrete Preise verbindlich festlegen",
    "App-Code, UI, Fragenbanken oder Marketingmaterial verändern",
    "Webrecherche oder externe Behauptungen ohne gesonderten Auftrag",
    "Funktions-, Fragen-, UI-, Supabase-, SQL- oder Netzwerkänderungen",
    "automatische Auswahl oder Autorisierung eines Folgetasks",
    "## Akzeptanzkriterien",
    "1. Beobachtung, Bewertung und Accaoui-Empfehlung sind klar getrennt.",
    "2. Wettbewerberaussagen sind ausdrücklich als nicht verifiziert markiert.",
    "3. Keine Formulierung wird vom Wettbewerber übernommen.",
    "4. Chancen und Risiken der Marketingmechanismen werden sachlich erklärt.",
    "5. Eine eigenständige Accaoui-Kernpositionierung wird formuliert.",
    "6. Zulässige und unzulässige Werbeaussagen werden getrennt dokumentiert.",
    "7. Die Leitidee aus `docs/PROJECT_MASTERLIST.md` bleibt verbindlich.",
    "8. Keine Funktions-, Fragen-, UI-, Supabase-, SQL- oder Netzwerkänderung.",
    f"9. Ausschließlich `{V2735F_NOTE_FILE}` wird im späteren Umsetzungsschritt verändert.",
    "10. Kein Commit und kein Push ohne gesonderte Freigabe.",
    "## Verbindliche Committrennung und Gate-Korrektur",
    f"`{V2735F_PREAUTHORIZATION_SHA}` ist der funktionale",
    f"`{V2735F_AUTHORIZATION_SHA}` ist die verbindliche",
    f"`{V2735F_FIRST_GATE_FIX_SHA}` ist ein legitimer",
    "separate nichtfunktionale v27.35f-Implementierungs-Gate-",
    "unzulässige starre Checker-Forderung",
    "ein Vorfahr des aktuellen",
    "zwei Zustände zulässig",
    f"`{V2735F_NOTE_SHA256}`",
    "## Verbindliche v27.35f-Lebenszyklus-State-Machine",
    "- **GATE:**",
    "- **IMPLEMENTATION:**",
    "- **CLOSURE:**",
    "Die vier zulässigen Phasen sind:",
    "Closure ohne Implementation, ein zweiter",
    "sie darf ungetrackt\nvorliegen. Keine weitere ungetrackte Datei ist zulässig.",
    "v27.35f bleibt der einzige aktive Task. Commit und Push bleiben verboten,",
    "## Historische Grenze des Autorisierungsschritts",
    "noch nicht erstellt oder verändert.",
    "In diesem\nSchritt wurde keine Wettbewerbsnotiz erstellt und keine App-Datei\nverändert.",
    "ausschließlich diesen `CURRENT_TASK`",
    "Nach Abschluss wird kein Folgetask automatisch ausgewählt.",
)

V2735F_CURSOR_REQUIRED_MARKERS = (
    "Stand: v27.35g",
    "Letzter abgeschlossener funktionaler Stand: v27.35g",
    f"Abschlusscommit: `{V2735G_COMPLETION_SHA}`",
    "Codex darf ebenfalls ausschließlich den in",
    "`docs/tasks/CURRENT_TASK.md` ausdrücklich autorisierten Task",
    "### Codex-Auftragsregel",
    "Codex muss vor jeder Änderung `docs/tasks/CURRENT_TASK.md` vollständig",
    "andere Dateien als die in `CURRENT_TASK` erlaubten Dateien verändern",
    "einen Commit oder Push ohne ausdrückliche Freigabe ausführen",
    "## 12. Cursor-Auftragsregel",
    "NUR FÜR CURSOR – NICHT IN GIT BASH",
    "NUR IN GIT BASH AUSFÜHREN",
    "Cursor darf **keinen Commit** und **keinen Push** ausführen",
    "`CURRENT_TASK` ist `v27.35f` / `AUTHORIZED` /",
    "`Autorisiert: JA`.",
    "Der einzige autorisierte Task ist v27.35f:",
    "Funktionaler Ausgangsstand ist v27.35g",
    f"`{V2735F_PREAUTHORIZATION_SHA}`",
    f"`{V2735F_AUTHORIZATION_SHA}`",
    f"`{V2735F_FIRST_GATE_FIX_SHA}`",
    f"`{V2735F_NOTE_FILE}`",
    "separaten nichtfunktionalen v27.35f-Implementierungs-Gate-",
    "ancestry-/Diff-basierte Gate-Regel",
    "finaler v27.35f-Notiz-Snapshot",
    f"`{V2735F_NOTE_SHA256}`",
    "vierphasige Lebenszyklus-",
    "Closure setzt einen dynamisch aus Git",
    "Eine Rückkehr aus dem abgeschlossenen Zustand zu v27.35f",
    "Sie darf als einzige ungetrackte Datei vorliegen.",
    "Commit und Push bleiben verboten.",
    "Codex darf ebenso wie Cursor ausschließlich diesen `CURRENT_TASK`",
    "Kein funktionaler oder sonstiger Folgetask wird",
)

V2735F_MASTERLIST_ROW = (
    "| v27.35f | Wettbewerbsbeobachtung und Accaoui-Positionierung "
    "dokumentieren; funktionaler Ausgangsstand v27.35g, funktionaler "
    "Ausgangs- und Vorautorisierungsstand "
    f"`{V2735F_PREAUTHORIZATION_SHA}`, v27.35f-Autorisierungscommit und "
    f"Umsetzungsbasis `{V2735F_AUTHORIZATION_SHA}`, Umsetzung ausschließlich "
    f"in `{V2735F_NOTE_FILE}`, kein Commit und kein Push – "
    "**autorisiert, Umsetzung offen** |"
)

V2735F_MASTERLIST_REQUIRED_MARKERS = (
    V2735F_MASTERLIST_ROW,
    "### Autorisierter Dokumentationstask v27.35f (Umsetzung offen)",
    "`docs/tasks/CURRENT_TASK.md` steht auf `Task-ID: v27.35f`, `Status: AUTHORIZED`, `Autorisiert: JA`.",
    "Funktionaler Ausgangsstand: v27.35g.",
    f"Funktionaler Ausgangs- und Vorautorisierungsstand: `{V2735F_PREAUTHORIZATION_SHA}`.",
    f"v27.35f-Autorisierungscommit und Umsetzungsbasis: `{V2735F_AUTHORIZATION_SHA}`.",
    f"`{V2735F_FIRST_GATE_FIX_SHA}` ein legitimer nichtfunktionaler v27.35f-Gate-Fix-Commit.",
    f"Für die Umsetzung ist ausschließlich `{V2735F_NOTE_FILE}` erlaubt.",
    "beobachtete und nicht extern verifizierte Marketingaussagen",
    "Beobachtung, Bewertung und Accaoui-Empfehlung müssen klar getrennt bleiben.",
    "„Mit dieser App habe ich es endlich verstanden.“",
    "Im abgeschlossenen Autorisierungsschritt wurde die Wettbewerbsnotiz noch nicht erstellt.",
    "`Commit erlaubt: NEIN` und `Push erlaubt: NEIN`.",
    "Nach Abschluss wird kein Folgetask automatisch ausgewählt oder autorisiert.",
    "### Separater nichtfunktionaler v27.35f-Implementierungs-Gate-Korrekturschritt",
    "Der ursprüngliche Checkerfehler war die starre Forderung",
    "Die neue Gate-Regel verlangt die Autorisierungsbasis als Vorfahren des aktuellen HEAD",
    "Vor einem Gate-Commit sind exakt fünf modifizierte Gate-Dateien",
    "Der aktuelle finale v27.35f-Notiz-Snapshot bleibt während des Gate-Schritts",
    f"SHA-256 `{V2735F_NOTE_SHA256}` unverändert.",
    "### Verbindliche v27.35f-Lebenszyklus-State-Machine",
    "Phase 1 akzeptiert den autorisierten Task vor Implementation",
    "Phase 2 akzeptiert nach genau einem IMPLEMENTATION-Commit",
    "Phase 3 akzeptiert erst danach die lokal vorbereitete Closure",
    "Phase 4 akzeptiert die committete Closure",
    "Sie darf als einzige ungetrackte Datei vorliegen; jede zusätzliche Datei bleibt gesperrt.",
    "v27.35f bleibt der einzige aktive Task; Commit und Push bleiben verboten, und ein Folgetask wird nicht ausgewählt oder autorisiert.",
    "`CURRENT_TASK` ist aktuell `v27.35f` /",
    "`AUTHORIZED` / `Autorisiert: JA`",
    "v27.35g bleibt der letzte abgeschlossene",
    f"`{V2735F_PREAUTHORIZATION_SHA}`; der historische",
    f"`{V2735F_AUTHORIZATION_SHA}`. Ausschließlich",
    "Notiz ist lokal erstellt und bleibt im getrennten Gate-Korrekturschritt\nals finaler v27.35f-Notiz-Snapshot per SHA-256",
    "Kein funktionaler oder sonstiger Folgetask wird automatisch",
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
V2736C_VERIFIED_WORK_PATH = r"C:\xampp\htdocs\accaoui\v4-dashboard"
V2736C_VERIFIED_WORK_PATH_GIT_BASH = "/c/xampp/htdocs/accaoui/v4-dashboard"

EXPECTED_STATE_FIELDS = {
    "Stand": "v27.35g",
    "Repository": "`asarrad-bit/accaoui-34a-lernapp`",
    "Branch": "`main`",
    "Letzter abgeschlossener funktionaler Stand": "v27.35g",
    "Abschlusscommit": f"`{V2735G_COMPLETION_SHA}`",
    "Aktueller HEAD": "DYNAMISCH ZU PRÜFEN",
    "Funktionsstatus": "v27.35g abgeschlossen",
    "Weiterer funktionaler Schritt autorisiert": "NEIN",
    "Aktuell autorisierter Task": "NONE",
    "Aktueller Blocker": (
        "Kein Task autorisiert; jeder weitere funktionale Schritt bleibt "
        "gesperrt, bis ein neuer Task ausdrücklich autorisiert wird"
    ),
}

EXPECTED_TASK_FIELDS = {
    "Task-ID": "NONE",
    "Status": "BLOCKED",
    "Autorisiert": "NEIN",
    "Titel": "Kein Task autorisiert",
    "Letzter abgeschlossener funktionaler Stand": "v27.35g",
    "Abschlusscommit": f"`{V2735G_COMPLETION_SHA}`",
    "Erlaubte Dateien": "KEINE",
    "Commit erlaubt": "NEIN",
    "Push erlaubt": "NEIN",
}

STATE_CONTRADICTORY_VALUES = (
    "Stand: v27.35e",
    "Stand: v27.35f",
    "Aktuell autorisierter Task: v27.35e",
    "Aktuell autorisierter Task: v27.35f",
    "Aktuell autorisierter Task: v27.35g",
    "Weiterer funktionaler Schritt autorisiert: JA",
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
    "## Nichtfunktionaler v27.35g-Implementierungs-Gate-Korrekturschritt",
    "## Abgeschlossener funktionaler Stand v27.35g",
    "Die Punkteberechnung der schriftlichen Prüfung wurde korrigiert: eine vollständig richtige Antwort",
    "die im v27.35e-Bericht verwendete Testkonstellation ergibt jetzt exakt 114/120 statt vormals 101/120",
    "alle 82 Fragen vollständig richtig ergeben jetzt exakt 120/120",
    f"Testbericht: `{V2735G_SCORING_FIX_REPORT_FILE}`. Funktionaler Abschlusscommit: `{V2735G_COMPLETION_SHA}`.",
    f"Implementierungs-Gate-Korrekturschritt (Commit `{V2735G_GATE_FIX_SHA}`) durchgeführt",
    f"Der bestehende v27.35e-FAIL-Bericht `{V2735E_TEST_REPORT_FILE}` bleibt unverändert als historische Fehlerdokumentation erhalten.",
    V2735F_RESERVATION_SENTENCE,
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
    "## Abgeschlossener funktionaler Stand v27.35g",
    "Die Punkteberechnung der schriftlichen Prüfung wurde korrigiert: eine vollständig richtige Antwort",
    "Alle 82 Fragen vollständig korrekt beantwortet ergeben jetzt exakt 120/120.",
    "Die im v27.35e-Bericht verwendete Testkonstellation ergibt jetzt exakt 114/120 statt vormals 101/120.",
    f"Testbericht: `{V2735G_SCORING_FIX_REPORT_FILE}`. Funktionaler Abschlusscommit: `{V2735G_COMPLETION_SHA}`.",
    f"Implementierungs-Gate-Korrekturschritt (Commit `{V2735G_GATE_FIX_SHA}`) durchgeführt",
    f"Der bestehende v27.35e-FAIL-Bericht `{V2735E_TEST_REPORT_FILE}` bleibt unverändert als historische Fehlerdokumentation erhalten.",
    V2735F_RESERVATION_SENTENCE,
    "## Verbindliche Sperre",
    "Kein neuer funktionaler oder nichtfunktionaler Task wird automatisch ausgewählt oder autorisiert.",
    "Aus Versionsfolgen, früheren Chats oder Erinnerung darf kein weiterer Task abgeleitet werden.",
    "Commit und Push bleiben bis zu einer gesonderten ausdrücklichen Freigabe gesperrt.",
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
    "Letzter abgeschlossener funktionaler Stand: v27.35g",
    f"Abschlusscommit: `{V2735G_COMPLETION_SHA}`",
    "| v24.6c | Pausieren/Fortsetzen Prüfung und Lernen | **erledigt** |",
    "**Erledigt:** v24.6b (Wiederholung/offene Fragen), v24.6c (Pausieren/Fortsetzen),",
    "## 14. Nächster sinnvoller Schritt",
    "`CURRENT_TASK` ist `NONE` / `BLOCKED`.",
    "Der Regressionstest v27.35e bleibt mit Gesamtergebnis FAIL abgeschlossen",
    V2735F_RESERVATION_SENTENCE,
    "Kein neuer funktionaler oder nichtfunktionaler Task ist ausgewählt oder automatisch abgeleitet.",
    "## 15. Wenn ein neuer Chat beginnt",
    "Zuerst vollständig lesen:",
    REQUIRED_CHAT_READING_BLOCK,
    "docs/CURSOR_MASTER_CONTEXT_ACCAOUI.md",
    "docs/SUPABASE_EXAM_QUESTION_DATABASE_PLAN.md",
)

CURSOR_CLOSURE_EXACT_MARKERS = (
    "Stand: v27.35g\nProjekt:",
    "Arbeit: `C:\\a34a`",
    "Zuhause: `C:\\xampp\\htdocs\\accaoui\\v4-dashboard`",
    "Letzter abgeschlossener funktionaler Stand: v27.35g",
    f"Abschlusscommit: `{V2735G_COMPLETION_SHA}`",
    "| v24.6c | Pausieren/Fortsetzen Prüfung und Lernen | **erledigt** |",
    "## 14. Nächster sinnvoller Schritt",
    "`CURRENT_TASK` ist `NONE` / `BLOCKED`.",
    "Kein neuer funktionaler oder nichtfunktionaler Task ist ausgewählt oder automatisch abgeleitet.",
    REQUIRED_CHAT_READING_BLOCK,
)

CURSOR_NEW_CHAT_LOCAL_HEAD_MARKERS = (
    "git rev-parse HEAD",
    "Lokalen und GitHub-HEAD direkt vergleichen",
)

STATE_CLOSURE_EXACT_MARKERS = (
    "Stand: v27.35g\nRepository:",
    f"\nAbschlusscommit: `{V2735G_COMPLETION_SHA}`\n",
    "## Abgeschlossener Regressionstest v27.35e (FAIL)",
    "## Autorisierter Task v27.35g",
    "## Abgeschlossener funktionaler Stand v27.35g",
    "Aktuell autorisierter Task: NONE",
    "Weiterer funktionaler Schritt autorisiert: NEIN",
)

TASK_CLOSURE_EXACT_MARKERS = (
    "Task-ID: NONE",
    "Status: BLOCKED",
    "Autorisiert: NEIN",
    "Titel: Kein Task autorisiert",
    "Erlaubte Dateien: KEINE",
    "## Abgeschlossener funktionaler Stand v27.35g",
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
    f"Nichtfunktionaler Implementierungs-Gate-Korrekturschritt (Commit `{V2735G_GATE_FIX_SHA}`) ergänzte danach ausschließlich",
    f"Funktionale Umsetzung (Commit `{V2735G_COMPLETION_SHA}`) veränderte ausschließlich `app.js` und `{V2735G_SCORING_FIX_REPORT_FILE}`",
    "`CURRENT_TASK` steht danach wieder auf `Task-ID: NONE`, `Status: BLOCKED`, `Autorisiert: NEIN`",
    "### Abgeschlossener funktionaler Stand v27.35g",
    f"Funktionaler Abschlusscommit: `{V2735G_COMPLETION_SHA}`. Dieser Commit veränderte ausschließlich `app.js` und `{V2735G_SCORING_FIX_REPORT_FILE}`.",
    "`docs/tasks/CURRENT_TASK.md` steht danach wieder auf `Task-ID: NONE`, `Status: BLOCKED`, `Autorisiert: NEIN`, `Erlaubte Dateien: KEINE`, `Commit erlaubt: NEIN`, `Push erlaubt: NEIN`.",
    "Diese Bestands- und Backlogliste ist keine Task-Autorisierung.",
    f"`CURRENT_TASK` ist aktuell `NONE` / `BLOCKED`; v27.35g ist der letzte abgeschlossene funktionale Stand (Abschlusscommit `{V2735G_COMPLETION_SHA}`).",
    "Backlog-Kandidat C (Quellen/mündliche Musterfragen) ist nicht autorisiert.",
    "`v27.35f` (Wettbewerbsbeobachtungsnotiz) bleibt vorgemerkt und ausdrücklich nicht autorisiert.",
    REQUIRED_CHAT_READING_BLOCK,
)

MASTERLIST_CLOSURE_EXACT_MARKERS = (
    "Stand: v27.35g\nBranch:",
    f"Arbeits-Laptop: `{WORK_PATH}`",
    f"Zuhause-Laptop: `{HOME_PATH}`",
    "| v27.35g |",
    "### Autorisierter Task v27.35g",
    "### Abgeschlossener funktionaler Stand v27.35g",
    f"`CURRENT_TASK` ist aktuell `NONE` / `BLOCKED`; v27.35g ist der letzte abgeschlossene funktionale Stand (Abschlusscommit `{V2735G_COMPLETION_SHA}`).",
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


def sha256_file(path: Path) -> str:
    require(path.is_file(), f"Pflichtdatei fehlt: {path.relative_to(ROOT)}")
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


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
        STATE_CLOSURE_EXACT_MARKERS,
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
            V2735G_GATE_FIX_SHA,
            V2735G_COMPLETION_SHA,
        },
        (
            "PROJECT_STATE_CURRENT darf nur die historisch bekannten Commits "
            "(Gate, v27.35b-Abschluss, v27.35c-Steuerung, Checker-Fix, "
            "v27.35d-Abschluss, v27.35e-Ausgangscommit, v27.35e-FAIL-Bericht/"
            "v27.35g-Ausgangscommit, v27.35g-Gate-Korrektur, "
            "v27.35g-Abschlusscommit) enthalten"
        ),
    )
    for forbidden_marker in FORBIDDEN_FUTURE_TASK_MARKERS:
        require(
            forbidden_marker not in text,
            "PROJECT_STATE_CURRENT darf keinen weiteren Folgeschritt auswählen oder nennen",
        )


TASK_CONTRADICTORY_GRANTS = (
    "Status: AUTHORIZED",
    "Autorisiert: JA",
    "Commit erlaubt: JA",
    "Push erlaubt: JA",
    "Task-ID: v27.35d",
    "Task-ID: v27.35e",
    "Task-ID: v27.35f",
    "Task-ID: v27.35g",
    "Task-ID: v27.36",
)


def validate_task_text(text: str) -> None:
    validate_exact_fields(text, EXPECTED_TASK_FIELDS)
    validate_required_markers(text, TASK_REQUIRED_MARKERS, "CURRENT_TASK")
    validate_exact_markers(text, TASK_CLOSURE_EXACT_MARKERS, "CURRENT_TASK")
    validate_v2735g_regression_ids(text, "CURRENT_TASK")
    validate_v2735f_not_active(text, "CURRENT_TASK")

    require(
        f"`{V2735E_TEST_REPORT_FILE}` bleibt" in text,
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
        CURSOR_CLOSURE_EXACT_MARKERS,
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
        MASTERLIST_CLOSURE_EXACT_MARKERS,
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
            check=False,
        )
    except (FileNotFoundError, OSError) as exc:
        raise ValidationError(f"git ist nicht ausführbar: {exc}") from exc
    require(
        completed.returncode == 0,
        (
            f"git-Befehl fehlgeschlagen (git {' '.join(args)}): "
            f"{decode_git_stderr(completed.stderr).strip()}"
        ),
    )
    return decode_git_stdout(completed.stdout)


def decode_git_stdout(data: bytes) -> str:
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValidationError(
            "Git-stdout ist kein gültiger UTF-8-Repository-Inhalt"
        ) from exc


def decode_git_stderr(data: bytes) -> str:
    return data.decode("utf-8", errors="replace")


def run_git_bytes(args: list[str]) -> bytes:
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=ROOT,
            capture_output=True,
            check=False,
        )
    except (FileNotFoundError, OSError) as exc:
        raise ValidationError(f"git ist nicht ausführbar: {exc}") from exc
    require(
        completed.returncode == 0,
        (
            f"git-Befehl fehlgeschlagen (git {' '.join(args)}): "
            f"{decode_git_stderr(completed.stderr).strip()}"
        ),
    )
    return completed.stdout


def validate_git_utf8_probe_text(text: str) -> None:
    require(
        text == "DYNAMISCH ZU PRÜFEN",
        "Git-UTF-8-Probetext wurde nicht exakt erkannt",
    )


def run_git_utf8_self_checks() -> tuple[int, int, int]:
    expected = "DYNAMISCH ZU PRÜFEN"
    repository_bytes = expected.encode("utf-8")
    decoded = decode_git_stdout(repository_bytes)
    validate_git_utf8_probe_text(decoded)
    require(
        repository_bytes.decode("cp1252") != decoded,
        "Git-UTF-8-Selbstprüfung bildet die Windows-Codepage-Abweichung nicht ab",
    )
    require(
        "�" in decode_git_stderr(b"stderr:\xff"),
        "Git-stderr muss auch bei ungültigen Bytes robust lesbar bleiben",
    )

    manipulations = 0
    must_reject(
        decode_git_stdout,
        expected.encode("cp1252"),
        "als Windows-Codepage-Bytes manipulierter Git-Inhalt",
    )
    manipulations += 1
    must_reject(
        validate_git_utf8_probe_text,
        repository_bytes.decode("cp1252"),
        "historisches Windows-Mojibake",
    )
    manipulations += 1
    return manipulations, 3, 2


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
    run_git(["merge-base", "--is-ancestor", V2735G_GATE_SHA, V2735G_AUTHORIZATION_SHA])

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


def validate_v2735g_authorization_commit_history() -> None:
    """Prüft den v27.35g-Autorisierungscommit ausschließlich historisch.

    Geprüft wird der abgeschlossene Bereich zwischen dem v27.35g-
    Ausgangscommit (V2735G_GATE_SHA, zugleich FAIL-Bericht-Commit von
    v27.35e) und dem Autorisierungscommit (V2735G_AUTHORIZATION_SHA). In
    diesem Bereich wurden ausschließlich die fünf Steuerungsdateien
    verändert; app.js, index.html und style.css blieben unverändert.
    """
    require(
        (ROOT / ".git").exists(),
        "Kein Git-Repository unter ROOT gefunden; Dateiprüfung nicht möglich",
    )
    run_git(
        ["merge-base", "--is-ancestor", V2735G_GATE_SHA, V2735G_AUTHORIZATION_SHA]
    )
    run_git(
        ["merge-base", "--is-ancestor", V2735G_AUTHORIZATION_SHA, V2735G_GATE_FIX_SHA]
    )

    authorization_changed_files = {
        line.strip()
        for line in run_git(
            ["diff", "--name-only", V2735G_GATE_SHA, V2735G_AUTHORIZATION_SHA]
        ).splitlines()
        if line.strip()
    }
    require(
        authorization_changed_files == set(EXPECTED_CONTROL_FILES),
        (
            "v27.35g-Autorisierungscommit veränderte zwischen Ausgangscommit "
            f"{V2735G_GATE_SHA} und Autorisierungscommit "
            f"{V2735G_AUTHORIZATION_SHA} nicht exakt die erwarteten "
            f"Steuerungsdateien: {sorted(authorization_changed_files)}"
        ),
    )

    for relative_path in PROTECTED_RUNTIME_FILES:
        historical_diff = run_git(
            [
                "diff",
                "--name-only",
                V2735G_GATE_SHA,
                V2735G_AUTHORIZATION_SHA,
                "--",
                relative_path,
            ]
        ).strip()
        require(
            historical_diff == "",
            (
                f"{relative_path} wurde im historisch abgeschlossenen "
                f"v27.35g-Autorisierungsbereich zwischen {V2735G_GATE_SHA} "
                f"und {V2735G_AUTHORIZATION_SHA} verändert"
            ),
        )


def validate_v2735g_gate_fix_commit_history() -> None:
    """Prüft den nichtfunktionalen v27.35g-Gate-Korrekturcommit ausschließlich historisch.

    Geprüft wird der abgeschlossene Bereich zwischen dem
    Autorisierungscommit (V2735G_AUTHORIZATION_SHA) und dem
    Gate-Korrekturcommit (V2735G_GATE_FIX_SHA). In diesem Bereich wurden
    ausschließlich die fünf Steuerungsdateien verändert; app.js,
    index.html und style.css blieben unverändert.
    """
    require(
        (ROOT / ".git").exists(),
        "Kein Git-Repository unter ROOT gefunden; Dateiprüfung nicht möglich",
    )
    run_git(
        ["merge-base", "--is-ancestor", V2735G_AUTHORIZATION_SHA, V2735G_GATE_FIX_SHA]
    )
    run_git(
        ["merge-base", "--is-ancestor", V2735G_GATE_FIX_SHA, V2735G_COMPLETION_SHA]
    )

    gate_fix_changed_files = {
        line.strip()
        for line in run_git(
            ["diff", "--name-only", V2735G_AUTHORIZATION_SHA, V2735G_GATE_FIX_SHA]
        ).splitlines()
        if line.strip()
    }
    require(
        gate_fix_changed_files == set(EXPECTED_CONTROL_FILES),
        (
            "v27.35g-Gate-Korrekturcommit veränderte zwischen "
            f"Autorisierungscommit {V2735G_AUTHORIZATION_SHA} und "
            f"Gate-Korrekturcommit {V2735G_GATE_FIX_SHA} nicht exakt die "
            f"erwarteten Steuerungsdateien: {sorted(gate_fix_changed_files)}"
        ),
    )

    for relative_path in PROTECTED_RUNTIME_FILES:
        historical_diff = run_git(
            [
                "diff",
                "--name-only",
                V2735G_AUTHORIZATION_SHA,
                V2735G_GATE_FIX_SHA,
                "--",
                relative_path,
            ]
        ).strip()
        require(
            historical_diff == "",
            (
                f"{relative_path} wurde im historisch abgeschlossenen "
                f"v27.35g-Gate-Korrekturbereich zwischen "
                f"{V2735G_AUTHORIZATION_SHA} und {V2735G_GATE_FIX_SHA} verändert"
            ),
        )


def validate_v2735g_completion_commit_history() -> None:
    """Prüft den funktionalen v27.35g-Abschlusscommit ausschließlich historisch.

    Geprüft wird der abgeschlossene Bereich zwischen dem
    Gate-Korrekturcommit (V2735G_GATE_FIX_SHA) und dem funktionalen
    Abschlusscommit (V2735G_COMPLETION_SHA). In diesem Bereich wurden
    ausschließlich app.js und der neue v27.35g-Testbericht verändert;
    index.html und style.css blieben unverändert.
    """
    require(
        (ROOT / ".git").exists(),
        "Kein Git-Repository unter ROOT gefunden; Dateiprüfung nicht möglich",
    )
    run_git(
        ["merge-base", "--is-ancestor", V2735G_GATE_FIX_SHA, V2735G_COMPLETION_SHA]
    )
    run_git(["merge-base", "--is-ancestor", V2735G_COMPLETION_SHA, "HEAD"])

    completion_changed_files = {
        line.strip()
        for line in run_git(
            ["diff", "--name-only", V2735G_GATE_FIX_SHA, V2735G_COMPLETION_SHA]
        ).splitlines()
        if line.strip()
    }
    require(
        completion_changed_files == set(EXPECTED_V2735G_COMPLETION_CHANGED_FILES),
        (
            "v27.35g-Abschlusscommit veränderte zwischen Gate-Korrekturcommit "
            f"{V2735G_GATE_FIX_SHA} und Abschlusscommit {V2735G_COMPLETION_SHA} "
            f"nicht exakt die erwarteten Dateien: {sorted(completion_changed_files)}"
        ),
    )

    for relative_path in ("index.html", "style.css"):
        historical_diff = run_git(
            [
                "diff",
                "--name-only",
                V2735G_GATE_FIX_SHA,
                V2735G_COMPLETION_SHA,
                "--",
                relative_path,
            ]
        ).strip()
        require(
            historical_diff == "",
            (
                f"{relative_path} wurde zwischen dem v27.35g-Gate-"
                f"Korrekturcommit {V2735G_GATE_FIX_SHA} und dem "
                f"v27.35g-Abschlusscommit {V2735G_COMPLETION_SHA} verändert"
            ),
        )


def validate_v2735g_closure_working_tree() -> None:
    """Prüft, dass nach dem v27.35g-Abschluss alle Kern-Dateien wieder vollständig gesperrt sind.

    Nach dem funktionalen Abschlusscommit (V2735G_COMPLETION_SHA) sind
    app.js, index.html und style.css sowie beide bestehenden
    Testberichte im Arbeitsbaum wieder vollständig gesperrt; es ist
    ausdrücklich keine Datei mehr für eine laufende Umsetzung
    freigegeben (siehe `Erlaubte Dateien: KEINE` in
    `docs/tasks/CURRENT_TASK.md`).
    """
    require(
        (ROOT / ".git").exists(),
        "Kein Git-Repository unter ROOT gefunden; Dateiprüfung nicht möglich",
    )
    run_git(["merge-base", "--is-ancestor", V2735G_COMPLETION_SHA, "HEAD"])

    for relative_path in PROTECTED_RUNTIME_FILES:
        committed_diff = run_git(
            ["diff", "--name-only", V2735G_COMPLETION_SHA, "HEAD", "--", relative_path]
        ).strip()
        require(
            committed_diff == "",
            (
                f"{relative_path} wurde seit dem v27.35g-Abschlusscommit "
                f"{V2735G_COMPLETION_SHA} in committeten Änderungen verändert"
            ),
        )

        working_tree_diff = run_git(
            ["diff", "--name-only", "HEAD", "--", relative_path]
        ).strip()
        require(
            working_tree_diff == "",
            (
                f"{relative_path} wurde im Arbeitsbaum gegenüber HEAD "
                "verändert; nach dem Abschluss von v27.35g ist im "
                "Arbeitsbaum keine Funktionsdatei mehr freigegeben"
            ),
        )

    for report_file in (V2735E_TEST_REPORT_FILE, V2735G_SCORING_FIX_REPORT_FILE):
        changed_report_diff = run_git(
            ["diff", "--name-only", "HEAD", "--", report_file]
        ).strip()
        require(
            changed_report_diff == "",
            (
                f"{report_file} wurde im Arbeitsbaum verändert; die "
                "bestehenden Testberichte dürfen nach dem Abschluss von "
                "v27.35g nicht mehr verändert werden"
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
        "Letzter abgeschlossener funktionaler Stand": "v27.35d",
        "Abschlusscommit": f"`{'0' * 40}`",
        "Aktueller HEAD": GATE_SHA,
        "Funktionsstatus": "v27.35d abgeschlossen",
        "Weiterer funktionaler Schritt autorisiert": "JA",
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
        "Status": "AUTHORIZED",
        "Autorisiert": "JA",
        "Titel": "Anderer Task",
        "Letzter abgeschlossener funktionaler Stand": "v27.35d",
        "Abschlusscommit": f"`{'0' * 40}`",
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
            "Erlaubte Dateien: KEINE",
            "Erlaubte Dateien: KEINE, `app.js`",
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
            "Kein neuer funktionaler oder nichtfunktionaler Task wird automatisch ausgewählt oder autorisiert.",
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
        STATE_CLOSURE_EXACT_MARKERS,
        "PROJECT_STATE_CURRENT",
    )
    checks += exercise_exact_marker_manipulations(
        validate_task_text,
        task_text,
        TASK_CLOSURE_EXACT_MARKERS,
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
        CURSOR_CLOSURE_EXACT_MARKERS,
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
        "Kein neuer funktionaler oder nichtfunktionaler Task ist ausgewählt oder automatisch abgeleitet.",
        (
            "Kein neuer funktionaler oder nichtfunktionaler Task ist ausgewählt oder automatisch abgeleitet.\n"
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
        "Kein neuer funktionaler oder nichtfunktionaler Task ist ausgewählt oder automatisch abgeleitet.",
        (
            "Kein neuer funktionaler oder nichtfunktionaler Task ist ausgewählt oder automatisch abgeleitet.\n"
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
        MASTERLIST_CLOSURE_EXACT_MARKERS,
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


def validate_v2735f_authorized_state_text(text: str) -> None:
    """Prüft den aktuellen Projektzustand für die v27.35f-Autorisierung."""
    validate_exact_fields(text, V2735F_EXPECTED_STATE_FIELDS)
    validate_required_markers(
        text,
        V2735F_STATE_REQUIRED_MARKERS,
        "PROJECT_STATE_CURRENT / v27.35f",
    )
    require(
        text.count("## Autorisierter Dokumentationstask v27.35f") == 1,
        "PROJECT_STATE_CURRENT: v27.35f-Autorisierungsabschnitt muss exakt einmal vorkommen",
    )
    require(
        "Aktuell autorisierter Task: NONE" not in text,
        "PROJECT_STATE_CURRENT: aktueller Task darf nicht NONE sein",
    )
    require(
        "Weiterer funktionaler Schritt autorisiert: JA" not in text,
        "PROJECT_STATE_CURRENT: kein funktionaler Schritt darf autorisiert sein",
    )
    for forbidden_marker in FORBIDDEN_FUTURE_TASK_MARKERS:
        require(
            forbidden_marker not in text,
            "PROJECT_STATE_CURRENT darf keinen Folgetask auswählen oder nennen",
        )


def validate_v2735f_authorized_task_text(text: str) -> None:
    """Prüft den vollständigen verbindlichen v27.35f-Taskvertrag."""
    validate_exact_fields(text, V2735F_EXPECTED_TASK_FIELDS)
    validate_required_markers(
        text,
        V2735F_TASK_REQUIRED_MARKERS,
        "CURRENT_TASK / v27.35f",
    )
    require(
        text.count("# Verbindlicher aktueller Task") == 1,
        "CURRENT_TASK: Hauptüberschrift muss exakt einmal vorkommen",
    )
    require(
        text.count(f"Erlaubte Dateien: `{V2735F_NOTE_FILE}`") == 1,
        "CURRENT_TASK: exakt eine erlaubte spätere Umsetzungsdatei erforderlich",
    )
    for forbidden_runtime_file in (
        "app.js",
        "index.html",
        "style.css",
        "questions.json",
        "patch-v21.js",
    ):
        require(
            forbidden_runtime_file not in text,
            f"CURRENT_TASK darf keine App-Datei erlauben oder nennen: {forbidden_runtime_file}",
        )
    for contradictory_grant in (
        "Status: BLOCKED",
        "Autorisiert: NEIN",
        "Commit erlaubt: JA",
        "Push erlaubt: JA",
    ):
        require(
            contradictory_grant not in text,
            f"CURRENT_TASK enthält widersprüchlichen Zustand: {contradictory_grant}",
        )
    for forbidden_marker in FORBIDDEN_FUTURE_TASK_MARKERS:
        require(
            forbidden_marker not in text,
            "CURRENT_TASK darf keinen Folgetask auswählen oder nennen",
        )


def validate_v2735f_cursor_context_text(text: str) -> None:
    """Prüft Cursor- und Codex-Regeln sowie den aktuellen v27.35f-Status."""
    validate_required_markers(
        text,
        V2735F_CURSOR_REQUIRED_MARKERS,
        "CURSOR_MASTER_CONTEXT_ACCAOUI / v27.35f",
    )
    validate_project_paths(text, "CURSOR_MASTER_CONTEXT_ACCAOUI")

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
    for marker in (
        "`CURRENT_TASK` ist `v27.35f` / `AUTHORIZED` /",
        f"`{V2735F_PREAUTHORIZATION_SHA}`",
        f"`{V2735F_AUTHORIZATION_SHA}`",
        f"`{V2735F_FIRST_GATE_FIX_SHA}`",
        f"`{V2735F_NOTE_FILE}`",
        "separaten nichtfunktionalen v27.35f-Implementierungs-Gate-",
        f"`{V2735F_NOTE_SHA256}`",
        "Sie darf als einzige ungetrackte Datei vorliegen.",
        "Codex darf ebenso wie Cursor ausschließlich diesen `CURRENT_TASK`",
    ):
        require(
            marker in next_task_section,
            f"CURSOR_MASTER_CONTEXT_ACCAOUI / nächster Schritt fehlt: {marker}",
        )
    require(
        "v24.6c" not in next_task_section,
        "CURSOR_MASTER_CONTEXT_ACCAOUI: alte aktive Task-Auswahl v24.6c",
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
    require(
        REQUIRED_CHAT_READING_BLOCK in new_chat_section,
        "CURSOR_MASTER_CONTEXT_ACCAOUI: Pflichtlektüre ist unvollständig",
    )
    for marker in CURSOR_NEW_CHAT_LOCAL_HEAD_MARKERS:
        require(
            new_chat_section.count(marker) == 1,
            f"CURSOR_MASTER_CONTEXT_ACCAOUI: Chatwechsel-Pflicht fehlt oder ist doppelt: {marker}",
        )
    for forbidden_marker in FORBIDDEN_FUTURE_TASK_MARKERS:
        require(
            forbidden_marker not in next_task_section,
            "CURSOR_MASTER_CONTEXT_ACCAOUI darf keinen Folgetask auswählen",
        )


def validate_v2735f_masterlist_text(text: str) -> None:
    """Prüft Leitidee, v27.35f-Status und die unveränderten Startregeln."""
    require(
        exact_field(text, "Stand") == "v27.35g",
        "PROJECT_MASTERLIST muss auf dem funktionalen Stand v27.35g bleiben",
    )
    validate_required_markers(
        text,
        V2735F_MASTERLIST_REQUIRED_MARKERS,
        "PROJECT_MASTERLIST / v27.35f",
    )
    validate_project_paths(text, "PROJECT_MASTERLIST")
    require(
        text.count(V2735F_MASTERLIST_ROW) == 1,
        "PROJECT_MASTERLIST: v27.35f-Zeile muss exakt einmal vorkommen",
    )
    require(
        text.count("### Autorisierter Dokumentationstask v27.35f (Umsetzung offen)") == 1,
        "PROJECT_MASTERLIST: aktueller v27.35f-Abschnitt muss exakt einmal vorkommen",
    )
    require(
        "## Leitidee der Accaoui §34a Lern-App" in text,
        "PROJECT_MASTERLIST: Leitidee fehlt",
    )
    require(
        "Jede Funktion muss mindestens eines dieser Ziele erfüllen:" in text,
        "PROJECT_MASTERLIST: verbindliche Leitidee wurde verändert",
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
    for forbidden_marker in FORBIDDEN_FUTURE_TASK_MARKERS:
        require(
            forbidden_marker not in text,
            "PROJECT_MASTERLIST darf keinen Folgetask auswählen oder nennen",
        )


def v2735f_closure_markers(implementation_commit: str) -> tuple[str, ...]:
    return (
        "v27.35f abgeschlossen",
        "Taskart: interne strategische Dokumentation.",
        f"Finale Notiz: `{V2735F_NOTE_FILE}`",
        f"Finaler Notiz-SHA-256: `{V2735F_NOTE_SHA256}`",
        f"Implementierungscommit: `{implementation_commit}`",
        (
            "Wettbewerbsbeobachtung, Accaoui-Differenzierung und "
            "Reaktivierung nach\nLernunterbrechung sind dokumentiert."
        ),
        "Kein App-Code wurde durch v27.35f verändert.",
        "Der letzte abgeschlossene funktionale Stand bleibt v27.35g.",
        "Kein Folgetask wurde ausgewählt oder autorisiert.",
    )


def validate_v2735f_closed_state_text(
    text: str,
    implementation_commit: str,
) -> None:
    validate_exact_fields(text, V2735F_CLOSED_STATE_FIELDS)
    validate_required_markers(
        text,
        (
            "## Abgeschlossener Dokumentationstask v27.35f",
            *v2735f_closure_markers(implementation_commit),
        ),
        "PROJECT_STATE_CURRENT / v27.35f-Abschluss",
    )
    for forbidden_marker in FORBIDDEN_FUTURE_TASK_MARKERS:
        require(
            forbidden_marker not in text,
            "PROJECT_STATE_CURRENT darf keinen Folgetask auswählen",
        )


def validate_v2735f_closed_task_text(
    text: str,
    implementation_commit: str,
) -> None:
    validate_exact_fields(text, V2735F_CLOSED_TASK_FIELDS)
    validate_required_markers(
        text,
        (
            "# Verbindlicher aktueller Task",
            "## Abgeschlossener Dokumentationstask v27.35f",
            *v2735f_closure_markers(implementation_commit),
        ),
        "CURRENT_TASK / v27.35f-Abschluss",
    )
    require(
        text.count("Erlaubte Dateien: KEINE") == 1,
        "CURRENT_TASK-Abschluss muss exakt Erlaubte Dateien: KEINE enthalten",
    )
    for forbidden_marker in FORBIDDEN_FUTURE_TASK_MARKERS:
        require(
            forbidden_marker not in text,
            "CURRENT_TASK-Abschluss darf keinen Folgetask auswählen",
        )


def validate_v2735f_closed_cursor_text(
    text: str,
    implementation_commit: str,
) -> None:
    validate_project_paths(text, "CURSOR_MASTER_CONTEXT_ACCAOUI")
    next_task_section = section_between(
        text,
        "## 14. Nächster sinnvoller Schritt",
        "## 15. Wenn ein neuer Chat beginnt",
        "CURSOR_MASTER_CONTEXT_ACCAOUI",
    )
    validate_required_markers(
        next_task_section,
        (
            "`CURRENT_TASK` ist `NONE` / `BLOCKED` / `Autorisiert: NEIN`",
            *v2735f_closure_markers(implementation_commit),
        ),
        "CURSOR_MASTER_CONTEXT_ACCAOUI / v27.35f-Abschluss",
    )
    for forbidden_marker in FORBIDDEN_FUTURE_TASK_MARKERS:
        require(
            forbidden_marker not in next_task_section,
            "CURSOR_MASTER_CONTEXT_ACCAOUI darf keinen Folgetask auswählen",
        )


def validate_v2735f_closed_masterlist_text(
    text: str,
    implementation_commit: str,
) -> None:
    require(
        exact_field(text, "Stand") == "v27.35g",
        "PROJECT_MASTERLIST muss funktional auf v27.35g bleiben",
    )
    validate_project_paths(text, "PROJECT_MASTERLIST")
    current_section = section_between(
        text,
        "## 14. Nächste sinnvolle Aufgaben",
        "## 15. Start in neuem Chat",
        "PROJECT_MASTERLIST",
    )
    validate_required_markers(
        current_section,
        (
            "`CURRENT_TASK` ist aktuell `NONE` / `BLOCKED` / `Autorisiert: NEIN`",
            *v2735f_closure_markers(implementation_commit),
        ),
        "PROJECT_MASTERLIST / v27.35f-Abschluss",
    )
    for forbidden_marker in FORBIDDEN_FUTURE_TASK_MARKERS:
        require(
            forbidden_marker not in current_section,
            "PROJECT_MASTERLIST darf keinen Folgetask auswählen",
        )


def validate_v2735f_closed_documents(
    state_text: str,
    task_text: str,
    cursor_context_text: str,
    masterlist_text: str,
    implementation_commit: str,
) -> None:
    validate_v2735f_closed_state_text(state_text, implementation_commit)
    validate_v2735f_closed_task_text(task_text, implementation_commit)
    validate_v2735f_closed_cursor_text(cursor_context_text, implementation_commit)
    validate_v2735f_closed_masterlist_text(masterlist_text, implementation_commit)


def validate_v2735f_authorization_commit_history() -> None:
    """Prüft Autorisierung und bekannten ersten Gate-Fix historisch."""
    require(
        (ROOT / ".git").exists(),
        "Kein Git-Repository unter ROOT gefunden",
    )
    run_git(
        [
            "merge-base",
            "--is-ancestor",
            V2735F_PREAUTHORIZATION_SHA,
            V2735F_AUTHORIZATION_SHA,
        ]
    )
    run_git(
        [
            "merge-base",
            "--is-ancestor",
            V2735F_AUTHORIZATION_SHA,
            V2735F_FIRST_GATE_FIX_SHA,
        ]
    )
    run_git(["merge-base", "--is-ancestor", V2735F_FIRST_GATE_FIX_SHA, "HEAD"])

    authorization_changed_files = {
        line.strip().replace("\\", "/")
        for line in run_git(
            [
                "diff",
                "--name-only",
                V2735F_PREAUTHORIZATION_SHA,
                V2735F_AUTHORIZATION_SHA,
            ]
        ).splitlines()
        if line.strip()
    }
    require(
        authorization_changed_files == set(V2735F_GATE_CONTROL_FILES),
        (
            "v27.35f-Autorisierungscommit veränderte zwischen dem funktionalen "
            f"Vorautorisierungsstand {V2735F_PREAUTHORIZATION_SHA} und dem "
            f"Autorisierungscommit {V2735F_AUTHORIZATION_SHA} nicht exakt die "
            f"fünf Steuerungsdateien: {sorted(authorization_changed_files)}"
        ),
    )

    authorization_tree_files = {
        line.strip().replace("\\", "/")
        for line in run_git(
            ["ls-tree", "-r", "--name-only", V2735F_AUTHORIZATION_SHA]
        ).splitlines()
        if line.strip()
    }
    require(
        V2735F_NOTE_FILE not in authorization_tree_files,
        "Die Wettbewerbsnotiz darf nicht Teil des v27.35f-Autorisierungscommits sein",
    )

    first_gate_fix_changed_files = {
        line.strip().replace("\\", "/")
        for line in run_git(
            [
                "diff",
                "--name-only",
                V2735F_AUTHORIZATION_SHA,
                V2735F_FIRST_GATE_FIX_SHA,
            ]
        ).splitlines()
        if line.strip()
    }
    require(
        first_gate_fix_changed_files == set(V2735F_GATE_CONTROL_FILES),
        (
            "Der bekannte v27.35f-Gate-Fix-Commit muss gegenüber der "
            "Autorisierungsbasis exakt die fünf Gate-Dateien verändern: "
            f"{sorted(first_gate_fix_changed_files)}"
        ),
    )

    first_gate_fix_tree_files = {
        line.strip().replace("\\", "/")
        for line in run_git(
            ["ls-tree", "-r", "--name-only", V2735F_FIRST_GATE_FIX_SHA]
        ).splitlines()
        if line.strip()
    }
    require(
        V2735F_NOTE_FILE not in first_gate_fix_tree_files,
        "Die Wettbewerbsnotiz darf nicht Teil des v27.35f-Gate-Fix-Commits sein",
    )

    for relative_path in PROTECTED_RUNTIME_FILES + (
        "questions.json",
        "patch-v21.js",
        "oral-exam.js",
        V2735E_TEST_REPORT_FILE,
        V2735G_SCORING_FIX_REPORT_FILE,
    ):
        require(
            run_git(
                [
                    "diff",
                    "--name-only",
                    V2735F_PREAUTHORIZATION_SHA,
                    V2735F_AUTHORIZATION_SHA,
                    "--",
                    relative_path,
                ]
            ).strip()
            == "",
            (
                "App-, Funktions- oder historische Berichtsdatei wurde im "
                f"v27.35f-Autorisierungscommit verändert: {relative_path}"
            ),
        )


def detect_v2735f_task_state_text(text: str) -> str:
    """Erkennt ausschließlich den autorisierten oder abgeschlossenen Taskzustand."""
    for forbidden_marker in FORBIDDEN_FUTURE_TASK_MARKERS:
        require(
            forbidden_marker not in text,
            "CURRENT_TASK darf keinen Folgetask auswählen oder nennen",
        )

    task_id = exact_field(text, "Task-ID")
    if task_id == V2735F_EXPECTED_TASK_FIELDS["Task-ID"]:
        validate_exact_fields(text, V2735F_EXPECTED_TASK_FIELDS)
        return V2735F_TASK_AUTHORIZED
    if task_id == V2735F_CLOSED_TASK_FIELDS["Task-ID"]:
        validate_exact_fields(text, V2735F_CLOSED_TASK_FIELDS)
        return V2735F_TASK_CLOSED
    raise ValidationError(f"Unzulässiger CURRENT_TASK-Zustand: Task-ID {task_id}")


def validate_v2735f_history_facts(
    commit_facts: tuple[V2735FCommitFact, ...],
) -> V2735FHistoryState:
    """Klassifiziert die lineare Historie als GATE, IMPLEMENTATION oder CLOSURE."""
    gate_files = set(V2735F_GATE_CONTROL_FILES)
    implementation_commit: str | None = None
    closure_seen = False
    roles: list[str] = []

    for fact in commit_facts:
        changed_files = set(fact.changed_files)
        require(
            changed_files,
            f"Leerer Commit im v27.35f-Lebenszyklus ist unzulässig: {fact.commit_sha}",
        )

        if changed_files == {V2735F_NOTE_FILE}:
            require(
                implementation_commit is None,
                "Mehr als ein v27.35f-IMPLEMENTATION-Commit ist unzulässig",
            )
            require(
                not closure_seen,
                "IMPLEMENTATION nach einer v27.35f-CLOSURE ist unzulässig",
            )
            require(
                fact.task_state == V2735F_TASK_AUTHORIZED,
                "IMPLEMENTATION ist nur bei autorisiertem v27.35f zulässig",
            )
            require(
                fact.note_sha256 == V2735F_NOTE_SHA256,
                (
                    "IMPLEMENTATION-Commit enthält nicht den finalen Notiz-SHA: "
                    f"{fact.note_sha256}"
                ),
            )
            implementation_commit = fact.commit_sha
            roles.append(V2735F_ROLE_IMPLEMENTATION)
            continue

        require(
            changed_files <= gate_files,
            (
                "Commit enthält Dateien außerhalb der v27.35f-Gate- oder "
                f"Implementation-Grenze: {fact.commit_sha}: {sorted(changed_files)}"
            ),
        )

        if fact.task_state == V2735F_TASK_AUTHORIZED:
            require(
                not closure_seen,
                "Rückkehr von NONE/BLOCKED zu v27.35f ohne neue Autorisierung",
            )
            roles.append(V2735F_ROLE_GATE)
            continue

        require(
            fact.task_state == V2735F_TASK_CLOSED,
            f"Unbekannter Taskzustand in Commit {fact.commit_sha}",
        )
        require(
            implementation_commit is not None,
            "CLOSURE ohne vorherigen IMPLEMENTATION-Commit ist unzulässig",
        )
        closure_seen = True
        roles.append(V2735F_ROLE_CLOSURE)

    if closure_seen:
        history_state = V2735F_HISTORY_CLOSED
    elif implementation_commit is not None:
        history_state = V2735F_HISTORY_IMPLEMENTED
    else:
        history_state = V2735F_HISTORY_BEFORE_IMPLEMENTATION
    return V2735FHistoryState(
        state=history_state,
        implementation_commit=implementation_commit,
        roles=tuple(roles),
    )


def validate_v2735f_lifecycle_working_tree(
    history_state: V2735FHistoryState,
    current_task_state: str,
    working_tree: V2735FWorkingTreeFact,
) -> str:
    """Ordnet Historie, aktuellen Task und Working Tree einer der vier Phasen zu."""
    gate_files = frozenset(V2735F_GATE_CONTROL_FILES)
    gate_status = frozenset(f" M {path}" for path in gate_files)
    note_status = f"?? {V2735F_NOTE_FILE}"

    require(
        not working_tree.staged_files,
        f"Gestagte Dateien sind unzulässig: {sorted(working_tree.staged_files)}",
    )
    require(
        working_tree.note_sha256 == V2735F_NOTE_SHA256,
        "Der aktuelle Notiz-SHA weicht vom finalen v27.35f-Snapshot ab",
    )

    if history_state.state == V2735F_HISTORY_BEFORE_IMPLEMENTATION:
        require(
            current_task_state == V2735F_TASK_AUTHORIZED,
            "Vor IMPLEMENTATION muss v27.35f autorisiert bleiben",
        )
        require(
            working_tree.diff_files in (frozenset(), gate_files),
            "Vor IMPLEMENTATION sind lokal nur null oder exakt fünf Gate-Dateien zulässig",
        )
        require(
            working_tree.untracked_files == frozenset({V2735F_NOTE_FILE}),
            "Vor IMPLEMENTATION muss ausschließlich die finale Notiz ungetrackt sein",
        )
        expected_status = (
            frozenset({note_status})
            if not working_tree.diff_files
            else gate_status | frozenset({note_status})
        )
        require(
            working_tree.status_lines == expected_status,
            "Working Tree entspricht nicht Phase 1 vor IMPLEMENTATION",
        )
        return V2735F_PHASE_BEFORE_IMPLEMENTATION

    if history_state.state == V2735F_HISTORY_IMPLEMENTED:
        require(
            history_state.implementation_commit is not None,
            "Phase nach IMPLEMENTATION benötigt den dynamischen Commitnachweis",
        )
        if current_task_state == V2735F_TASK_AUTHORIZED:
            require(
                not working_tree.diff_files
                and not working_tree.untracked_files
                and not working_tree.status_lines,
                "Phase 2 nach IMPLEMENTATION benötigt einen sauberen Working Tree",
            )
            return V2735F_PHASE_IMPLEMENTATION_COMMITTED
        require(
            current_task_state == V2735F_TASK_CLOSED,
            "Nach IMPLEMENTATION ist nur autorisierter oder abgeschlossener Taskzustand zulässig",
        )
        require(
            working_tree.diff_files == gate_files,
            "Lokal vorbereitete CLOSURE muss exakt fünf Gate-Dateien verändern",
        )
        require(
            not working_tree.untracked_files,
            "Lokal vorbereitete CLOSURE darf keine ungetrackte Datei enthalten",
        )
        require(
            working_tree.status_lines == gate_status,
            "Working Tree entspricht nicht Phase 3 der lokal vorbereiteten CLOSURE",
        )
        return V2735F_PHASE_CLOSURE_PREPARED

    require(
        history_state.state == V2735F_HISTORY_CLOSED,
        f"Unbekannter v27.35f-Historienzustand: {history_state.state}",
    )
    require(
        current_task_state == V2735F_TASK_CLOSED,
        "Nach CLOSURE darf v27.35f nicht erneut autorisiert erscheinen",
    )
    require(
        not working_tree.diff_files
        and not working_tree.untracked_files
        and not working_tree.status_lines,
        "Phase 4 nach CLOSURE benötigt einen sauberen Working Tree",
    )
    return V2735F_PHASE_CLOSURE_COMMITTED


def read_v2735f_commit_facts(current_head: str) -> tuple[V2735FCommitFact, ...]:
    """Liest eine lineare Commitfolge ab der Autorisierungsbasis aus Git."""
    commit_shas = tuple(
        line.strip()
        for line in run_git(
            [
                "rev-list",
                "--reverse",
                "--ancestry-path",
                f"{V2735F_AUTHORIZATION_SHA}..{current_head}",
            ]
        ).splitlines()
        if line.strip()
    )
    previous_commit = V2735F_AUTHORIZATION_SHA
    facts: list[V2735FCommitFact] = []

    for commit_sha in commit_shas:
        parent_line = run_git(
            ["rev-list", "--parents", "-n", "1", commit_sha]
        ).strip().split()
        require(
            len(parent_line) == 2 and parent_line[1] == previous_commit,
            (
                "Der v27.35f-Lebenszyklus muss ab der Autorisierungsbasis "
                f"linear bleiben; unzulässiger Commit: {commit_sha}"
            ),
        )
        changed_files = frozenset(
            line.strip().replace("\\", "/")
            for line in run_git(
                ["diff", "--name-only", previous_commit, commit_sha]
            ).splitlines()
            if line.strip()
        )
        task_text = run_git(
            ["show", f"{commit_sha}:{V2735F_TASK_RELATIVE_PATH}"]
        ).replace("\r\n", "\n").replace("\r", "\n")
        task_state = detect_v2735f_task_state_text(task_text)
        note_sha256 = None
        if changed_files == frozenset({V2735F_NOTE_FILE}):
            note_blob = run_git_bytes(
                ["show", f"{commit_sha}:{V2735F_NOTE_FILE}"]
            )
            note_sha256 = hashlib.sha256(note_blob).hexdigest()
        facts.append(
            V2735FCommitFact(
                commit_sha=commit_sha,
                changed_files=changed_files,
                task_state=task_state,
                note_sha256=note_sha256,
            )
        )
        previous_commit = commit_sha

    require(
        previous_commit == current_head,
        "HEAD liegt nicht auf einer linearen Historie ab der v27.35f-Autorisierungsbasis",
    )
    return tuple(facts)


def read_v2735f_working_tree_fact() -> V2735FWorkingTreeFact:
    note_path = ROOT / V2735F_NOTE_FILE
    return V2735FWorkingTreeFact(
        diff_files=frozenset(
            line.strip().replace("\\", "/")
            for line in run_git(["diff", "--name-only"]).splitlines()
            if line.strip()
        ),
        staged_files=frozenset(
            line.strip().replace("\\", "/")
            for line in run_git(["diff", "--cached", "--name-only"]).splitlines()
            if line.strip()
        ),
        untracked_files=frozenset(
            line.strip().replace("\\", "/")
            for line in run_git(
                ["ls-files", "--others", "--exclude-standard"]
            ).splitlines()
            if line.strip()
        ),
        status_lines=frozenset(
            line.replace("\\", "/")
            for line in run_git(
                ["status", "--porcelain=v1", "--untracked-files=all"]
            ).splitlines()
            if line
        ),
        note_sha256=sha256_file(note_path),
    )


def read_v2735f_commit_document(commit_sha: str, relative_path: str) -> str:
    return run_git(["show", f"{commit_sha}:{relative_path}"]).replace(
        "\r\n", "\n"
    ).replace("\r", "\n")


def validate_v2735f_committed_closure_documents(
    commit_facts: tuple[V2735FCommitFact, ...],
    history_state: V2735FHistoryState,
) -> None:
    if V2735F_ROLE_CLOSURE not in history_state.roles:
        return
    require(
        history_state.implementation_commit is not None,
        "CLOSURE-Dokumentprüfung benötigt einen IMPLEMENTATION-Commit",
    )
    for fact, role in zip(commit_facts, history_state.roles):
        if role != V2735F_ROLE_CLOSURE:
            continue
        validate_v2735f_closed_documents(
            read_v2735f_commit_document(
                fact.commit_sha, "docs/PROJECT_STATE_CURRENT.md"
            ),
            read_v2735f_commit_document(
                fact.commit_sha, V2735F_TASK_RELATIVE_PATH
            ),
            read_v2735f_commit_document(
                fact.commit_sha, "docs/CURSOR_MASTER_CONTEXT_ACCAOUI.md"
            ),
            read_v2735f_commit_document(
                fact.commit_sha, "docs/PROJECT_MASTERLIST.md"
            ),
            history_state.implementation_commit,
        )


def validate_v2735f_lifecycle(
    state_text: str,
    task_text: str,
    cursor_context_text: str,
    masterlist_text: str,
) -> tuple[str, V2735FHistoryState]:
    """Validiert reale Historie, Dokumentzustand und Working Tree gemeinsam."""
    require(
        (ROOT / ".git").exists(),
        "Kein Git-Repository unter ROOT gefunden",
    )
    require(
        run_git(["branch", "--show-current"]).strip() == "main",
        "v27.35f-Lebenszyklus muss auf Branch main laufen",
    )
    current_head = run_git(["rev-parse", "HEAD"]).strip()
    origin_main = run_git(["rev-parse", "origin/main"]).strip()
    run_git(
        [
            "merge-base",
            "--is-ancestor",
            V2735F_AUTHORIZATION_SHA,
            current_head,
        ]
    )
    run_git(
        [
            "merge-base",
            "--is-ancestor",
            V2735F_AUTHORIZATION_SHA,
            origin_main,
        ]
    )
    run_git(["merge-base", "--is-ancestor", origin_main, current_head])

    commit_facts = read_v2735f_commit_facts(current_head)
    history_state = validate_v2735f_history_facts(commit_facts)
    validate_v2735f_committed_closure_documents(commit_facts, history_state)

    note_in_head = run_git(
        ["ls-tree", "-r", "--name-only", current_head, "--", V2735F_NOTE_FILE]
    ).strip()
    if history_state.state == V2735F_HISTORY_BEFORE_IMPLEMENTATION:
        require(
            note_in_head == "",
            "Vor IMPLEMENTATION darf die Wettbewerbsnotiz nicht getrackt sein",
        )
    else:
        require(
            note_in_head == V2735F_NOTE_FILE,
            "Nach IMPLEMENTATION muss exakt die Wettbewerbsnotiz getrackt sein",
        )

    current_task_state = detect_v2735f_task_state_text(task_text)
    if current_task_state == V2735F_TASK_AUTHORIZED:
        validate_v2735f_authorized_state_text(state_text)
        validate_v2735f_authorized_task_text(task_text)
        validate_v2735f_cursor_context_text(cursor_context_text)
        validate_v2735f_masterlist_text(masterlist_text)
    else:
        require(
            history_state.implementation_commit is not None,
            "Abschlussdokumente sind erst nach IMPLEMENTATION zulässig",
        )
        validate_v2735f_closed_documents(
            state_text,
            task_text,
            cursor_context_text,
            masterlist_text,
            history_state.implementation_commit,
        )

    phase = validate_v2735f_lifecycle_working_tree(
        history_state,
        current_task_state,
        read_v2735f_working_tree_fact(),
    )
    return phase, history_state


def run_v2735f_authorization_manipulation_matrix(
    state_text: str,
    task_text: str,
    cursor_context_text: str,
    masterlist_text: str,
    implementation_commit: str | None,
) -> tuple[int, int, int]:
    """Bestätigt die verbindlichen Blockierungen des v27.35f-Vertrags."""
    checks = 0

    if detect_v2735f_task_state_text(task_text) == V2735F_TASK_CLOSED:
        require(
            implementation_commit is not None,
            "Abschluss-Manipulationsmatrix benötigt den IMPLEMENTATION-Commit",
        )
        state_text = read_v2735f_commit_document(
            implementation_commit, "docs/PROJECT_STATE_CURRENT.md"
        )
        task_text = read_v2735f_commit_document(
            implementation_commit, V2735F_TASK_RELATIVE_PATH
        )
        cursor_context_text = read_v2735f_commit_document(
            implementation_commit, "docs/CURSOR_MASTER_CONTEXT_ACCAOUI.md"
        )
        masterlist_text = read_v2735f_commit_document(
            implementation_commit, "docs/PROJECT_MASTERLIST.md"
        )

    state_manipulations = {
        "Stand": "v27.35f",
        "Repository": "`anderes/repository`",
        "Branch": "`anderer-branch`",
        "Letzter abgeschlossener funktionaler Stand": "v27.35d",
        "Abschlusscommit": f"`{'0' * 40}`",
        "Aktueller HEAD": V2735G_COMPLETION_SHA,
        "Funktionsstatus": "v27.35d abgeschlossen",
        "Weiterer funktionaler Schritt autorisiert": "JA",
        "Aktuell autorisierter Task": "v27.35g",
        "Aktuelle Taskart": "Funktion",
        "Aktueller Blocker": "Kein Task autorisiert",
    }
    for field_name, expected_value in V2735F_EXPECTED_STATE_FIELDS.items():
        must_reject(
            validate_v2735f_authorized_state_text,
            changed_once(
                state_text,
                f"{field_name}: {expected_value}\n",
                "",
                f"PROJECT_STATE_CURRENT Feld fehlt: {field_name}",
            ),
            f"PROJECT_STATE_CURRENT Feld fehlt: {field_name}",
        )
        checks += 1
        must_reject(
            validate_v2735f_authorized_state_text,
            changed_once(
                state_text,
                f"{field_name}: {expected_value}",
                f"{field_name}: {state_manipulations[field_name]}",
                f"PROJECT_STATE_CURRENT Feld manipuliert: {field_name}",
            ),
            f"PROJECT_STATE_CURRENT Feld manipuliert: {field_name}",
        )
        checks += 1

    task_manipulations = {
        "Task-ID": "v27.35g",
        "Status": "BLOCKED",
        "Autorisiert": "NEIN",
        "Titel": "Anderer Task",
        "Funktionaler Ausgangsstand": "v27.35d",
        "Erwarteter Ausgangscommit": f"`{V2735F_PREAUTHORIZATION_SHA}`",
        "Erlaubte Dateien": f"`{V2735F_NOTE_FILE}`, `app.js`",
        "Commit erlaubt": "JA",
        "Push erlaubt": "JA",
    }
    for field_name, expected_value in V2735F_EXPECTED_TASK_FIELDS.items():
        must_reject(
            validate_v2735f_authorized_task_text,
            changed_once(
                task_text,
                f"{field_name}: {expected_value}\n",
                "",
                f"CURRENT_TASK Feld fehlt: {field_name}",
            ),
            f"CURRENT_TASK Feld fehlt: {field_name}",
        )
        checks += 1
        must_reject(
            validate_v2735f_authorized_task_text,
            changed_once(
                task_text,
                f"{field_name}: {expected_value}",
                f"{field_name}: {task_manipulations[field_name]}",
                f"CURRENT_TASK Feld manipuliert: {field_name}",
            ),
            f"CURRENT_TASK Feld manipuliert: {field_name}",
        )
        checks += 1

    for marker in V2735F_TASK_REQUIRED_MARKERS:
        manipulated_task_text = task_text.replace(marker, "")
        require(
            manipulated_task_text != task_text,
            f"Manipulationsmatrix kann Pflichtaussage nicht finden: {marker}",
        )
        must_reject(
            validate_v2735f_authorized_task_text,
            manipulated_task_text,
            f"CURRENT_TASK Pflichtaussage fehlt: {marker}",
        )
        checks += 1

    must_reject(
        validate_v2735f_authorized_task_text,
        changed_once(
            task_text,
            "Nach Abschluss wird kein Folgetask automatisch ausgewählt.",
            "Nach Abschluss wird v27.36 automatisch ausgewählt.",
            "automatische Auswahl eines Folgetasks",
        ),
        "automatische Auswahl eines Folgetasks",
    )
    checks += 1

    must_reject(
        validate_v2735f_cursor_context_text,
        changed_once(
            cursor_context_text,
            "Codex darf ebenfalls ausschließlich den in",
            "Codex darf beliebige Tasks bearbeiten und",
            "Codex darf nur CURRENT_TASK bearbeiten",
        ),
        "Codex darf nur CURRENT_TASK bearbeiten",
    )
    checks += 1

    must_reject(
        validate_v2735f_masterlist_text,
        changed_once(
            masterlist_text,
            V2735F_MASTERLIST_ROW,
            V2735F_MASTERLIST_ROW.replace(
                "**autorisiert, Umsetzung offen**",
                "**vorgemerkt, nicht autorisiert**",
            ),
            "PROJECT_MASTERLIST v27.35f-Autorisierungsstatus",
        ),
        "PROJECT_MASTERLIST v27.35f-Autorisierungsstatus",
    )
    checks += 1

    gate_rule_document_markers = (
        (
            validate_v2735f_authorized_state_text,
            state_text,
            "starre Gleichheitsprüfung auf",
            "PROJECT_STATE_CURRENT dokumentiert den ursprünglichen Checkerfehler",
        ),
        (
            validate_v2735f_authorized_task_text,
            task_text,
            "unzulässige starre Checker-Forderung",
            "CURRENT_TASK dokumentiert den ursprünglichen Checkerfehler",
        ),
        (
            validate_v2735f_cursor_context_text,
            cursor_context_text,
            "ancestry-/Diff-basierte Gate-Regel",
            "Cursor-Kontext dokumentiert die ancestry-/Diff-Gate-Regel",
        ),
        (
            validate_v2735f_masterlist_text,
            masterlist_text,
            "Die neue Gate-Regel verlangt die Autorisierungsbasis als Vorfahren",
            "Masterliste dokumentiert die ancestry-/Diff-Gate-Regel",
        ),
    )
    for validator, document_text, marker, label in gate_rule_document_markers:
        must_reject(
            validator,
            changed_once(document_text, marker, "", label),
            label,
        )
        checks += 1

    gate_files = frozenset(V2735F_GATE_CONTROL_FILES)
    gate_status = frozenset(f" M {path}" for path in gate_files)
    note_status = f"?? {V2735F_NOTE_FILE}"
    gate_commit = V2735FCommitFact(
        commit_sha="1" * 40,
        changed_files=gate_files,
        task_state=V2735F_TASK_AUTHORIZED,
    )
    implementation_commit = V2735FCommitFact(
        commit_sha="2" * 40,
        changed_files=frozenset({V2735F_NOTE_FILE}),
        task_state=V2735F_TASK_AUTHORIZED,
        note_sha256=V2735F_NOTE_SHA256,
    )
    closure_commit = V2735FCommitFact(
        commit_sha="3" * 40,
        changed_files=gate_files,
        task_state=V2735F_TASK_CLOSED,
    )

    before_implementation = validate_v2735f_history_facts((gate_commit,))
    phase_1 = validate_v2735f_lifecycle_working_tree(
        before_implementation,
        V2735F_TASK_AUTHORIZED,
        V2735FWorkingTreeFact(
            diff_files=gate_files,
            staged_files=frozenset(),
            untracked_files=frozenset({V2735F_NOTE_FILE}),
            status_lines=gate_status | frozenset({note_status}),
            note_sha256=V2735F_NOTE_SHA256,
        ),
    )
    implemented = validate_v2735f_history_facts(
        (gate_commit, implementation_commit)
    )
    phase_2 = validate_v2735f_lifecycle_working_tree(
        implemented,
        V2735F_TASK_AUTHORIZED,
        V2735FWorkingTreeFact(
            diff_files=frozenset(),
            staged_files=frozenset(),
            untracked_files=frozenset(),
            status_lines=frozenset(),
            note_sha256=V2735F_NOTE_SHA256,
        ),
    )
    phase_3 = validate_v2735f_lifecycle_working_tree(
        implemented,
        V2735F_TASK_CLOSED,
        V2735FWorkingTreeFact(
            diff_files=gate_files,
            staged_files=frozenset(),
            untracked_files=frozenset(),
            status_lines=gate_status,
            note_sha256=V2735F_NOTE_SHA256,
        ),
    )
    closed = validate_v2735f_history_facts(
        (gate_commit, implementation_commit, closure_commit)
    )
    phase_4 = validate_v2735f_lifecycle_working_tree(
        closed,
        V2735F_TASK_CLOSED,
        V2735FWorkingTreeFact(
            diff_files=frozenset(),
            staged_files=frozenset(),
            untracked_files=frozenset(),
            status_lines=frozenset(),
            note_sha256=V2735F_NOTE_SHA256,
        ),
    )
    positive_phases = (
        phase_1,
        phase_2,
        phase_3,
        phase_4,
    )
    require(
        positive_phases
        == (
            V2735F_PHASE_BEFORE_IMPLEMENTATION,
            V2735F_PHASE_IMPLEMENTATION_COMMITTED,
            V2735F_PHASE_CLOSURE_PREPARED,
            V2735F_PHASE_CLOSURE_COMMITTED,
        ),
        f"Vierphasige Lebenszyklus-Simulation abweichend: {positive_phases}",
    )

    second_implementation = V2735FCommitFact(
        commit_sha="4" * 40,
        changed_files=frozenset({V2735F_NOTE_FILE}),
        task_state=V2735F_TASK_AUTHORIZED,
        note_sha256=V2735F_NOTE_SHA256,
    )
    implementation_with_foreign_file = V2735FCommitFact(
        commit_sha="5" * 40,
        changed_files=frozenset({V2735F_NOTE_FILE, "unexpected.txt"}),
        task_state=V2735F_TASK_AUTHORIZED,
    )
    wrong_note_sha = V2735FCommitFact(
        commit_sha="6" * 40,
        changed_files=frozenset({V2735F_NOTE_FILE}),
        task_state=V2735F_TASK_AUTHORIZED,
        note_sha256="0" * 64,
    )
    closure_without_implementation = V2735FCommitFact(
        commit_sha="7" * 40,
        changed_files=gate_files,
        task_state=V2735F_TASK_CLOSED,
    )
    function_commit = V2735FCommitFact(
        commit_sha="8" * 40,
        changed_files=frozenset({"app.js"}),
        task_state=V2735F_TASK_AUTHORIZED,
    )
    return_to_authorized = V2735FCommitFact(
        commit_sha="9" * 40,
        changed_files=gate_files,
        task_state=V2735F_TASK_AUTHORIZED,
    )

    lifecycle_manipulations = (
        (
            lambda _text: validate_v2735f_history_facts(
                (gate_commit, implementation_commit, second_implementation)
            ),
            "zweiter IMPLEMENTATION-Commit",
        ),
        (
            lambda _text: validate_v2735f_history_facts(
                (gate_commit, implementation_with_foreign_file)
            ),
            "IMPLEMENTATION mit fremder Datei",
        ),
        (
            lambda _text: validate_v2735f_history_facts(
                (gate_commit, wrong_note_sha)
            ),
            "falscher Notiz-SHA",
        ),
        (
            lambda _text: validate_v2735f_history_facts(
                (gate_commit, closure_without_implementation)
            ),
            "CLOSURE ohne IMPLEMENTATION",
        ),
        (
            lambda _text: validate_v2735f_history_facts(
                (gate_commit, function_commit)
            ),
            "Funktionsdatei im Lebenszyklus",
        ),
        (
            lambda _text: detect_v2735f_task_state_text(
                changed_once(
                    task_text,
                    "Task-ID: v27.35f",
                    "Task-ID: v27.36",
                    "automatisch gesetzter Folgetask",
                )
            ),
            "automatisch gesetzter Folgetask",
        ),
        (
            lambda _text: validate_v2735f_history_facts(
                (
                    gate_commit,
                    implementation_commit,
                    closure_commit,
                    return_to_authorized,
                )
            ),
            "Rückkehr zu v27.35f nach CLOSURE",
        ),
        (
            lambda _text: validate_v2735f_lifecycle_working_tree(
                before_implementation,
                V2735F_TASK_AUTHORIZED,
                V2735FWorkingTreeFact(
                    diff_files=gate_files,
                    staged_files=frozenset(),
                    untracked_files=frozenset(
                        {V2735F_NOTE_FILE, "unexpected.txt"}
                    ),
                    status_lines=gate_status
                    | frozenset({note_status, "?? unexpected.txt"}),
                    note_sha256=V2735F_NOTE_SHA256,
                ),
            ),
            "zusätzliche ungetrackte Datei",
        ),
    )
    for validator, label in lifecycle_manipulations:
        must_reject(validator, "", label)
        checks += 1

    return checks, len(positive_phases), len(lifecycle_manipulations)


def validate_v2735f_completed_base() -> tuple[V2735FHistoryState, tuple[str, str, str, str]]:
    """Belegt den vollständig abgeschlossenen v27.35f-Stand am v27.36a-Start."""
    run_git(
        [
            "merge-base",
            "--is-ancestor",
            V2735F_AUTHORIZATION_SHA,
            V2736A_AUTHORIZATION_BASE_SHA,
        ]
    )
    commit_facts = read_v2735f_commit_facts(V2736A_AUTHORIZATION_BASE_SHA)
    history_state = validate_v2735f_history_facts(commit_facts)
    require(
        history_state.state == V2735F_HISTORY_CLOSED,
        "v27.35f muss am v27.36a-Ausgangscommit vollständig geschlossen sein",
    )
    require(
        history_state.implementation_commit is not None,
        "v27.35f-Abschluss benötigt den dynamischen IMPLEMENTATION-Commit",
    )
    validate_v2735f_committed_closure_documents(commit_facts, history_state)
    require(
        run_git(
            [
                "ls-tree",
                "-r",
                "--name-only",
                V2736A_AUTHORIZATION_BASE_SHA,
                "--",
                V2735F_NOTE_FILE,
            ]
        ).strip()
        == V2735F_NOTE_FILE,
        "Finale v27.35f-Notiz fehlt am v27.36a-Ausgangscommit",
    )
    base_documents = (
        read_v2735f_commit_document(
            V2736A_AUTHORIZATION_BASE_SHA,
            "docs/PROJECT_STATE_CURRENT.md",
        ),
        read_v2735f_commit_document(
            V2736A_AUTHORIZATION_BASE_SHA,
            V2735F_TASK_RELATIVE_PATH,
        ),
        read_v2735f_commit_document(
            V2736A_AUTHORIZATION_BASE_SHA,
            "docs/CURSOR_MASTER_CONTEXT_ACCAOUI.md",
        ),
        read_v2735f_commit_document(
            V2736A_AUTHORIZATION_BASE_SHA,
            "docs/PROJECT_MASTERLIST.md",
        ),
    )
    validate_v2735f_closed_documents(
        *base_documents,
        history_state.implementation_commit,
    )
    return history_state, base_documents


def validate_v2736a_state_text(text: str) -> None:
    validate_exact_fields(text, V2736A_EXPECTED_STATE_FIELDS)
    validate_required_markers(
        text,
        V2736A_STATE_REQUIRED_MARKERS + V2736A_STATE_LIFECYCLE_MARKERS,
        "PROJECT_STATE_CURRENT / v27.36a",
    )


def validate_v2736a_task_text(text: str) -> None:
    validate_exact_fields(text, V2736A_EXPECTED_TASK_FIELDS)
    validate_required_markers(
        text,
        V2736A_TASK_REQUIRED_MARKERS + V2736A_TASK_LIFECYCLE_MARKERS,
        "CURRENT_TASK / v27.36a",
    )
    require(
        text.count(f"Erlaubte Dateien: `{V2736A_AUDIT_FILE}`") == 1,
        "CURRENT_TASK muss exakt eine v27.36a-Erlaubte-Dateien-Zeile enthalten",
    )


def validate_v2736a_cursor_text(text: str) -> None:
    validate_project_paths(text, "CURSOR_MASTER_CONTEXT_ACCAOUI")
    section = section_between(
        text,
        "## 14. Nächster sinnvoller Schritt",
        "## 15. Wenn ein neuer Chat beginnt",
        "CURSOR_MASTER_CONTEXT_ACCAOUI",
    )
    validate_required_markers(
        section,
        V2736A_CURSOR_REQUIRED_MARKERS + V2736A_CURSOR_LIFECYCLE_MARKERS,
        "CURSOR_MASTER_CONTEXT_ACCAOUI / v27.36a",
    )
    require(
        re.search(r"\bv27\.(?:36[b-z]|3[7-9])\b", section, re.IGNORECASE) is None,
        "CURSOR_MASTER_CONTEXT_ACCAOUI darf keinen Folgetask autorisieren",
    )


def validate_v2736a_masterlist_text(text: str) -> None:
    require(
        exact_field(text, "Stand") == "v27.35g",
        "PROJECT_MASTERLIST muss funktional auf v27.35g bleiben",
    )
    validate_project_paths(text, "PROJECT_MASTERLIST")
    validate_required_markers(
        text,
        V2736A_MASTERLIST_REQUIRED_MARKERS + V2736A_MASTERLIST_LIFECYCLE_MARKERS,
        "PROJECT_MASTERLIST / v27.36a",
    )
    require(
        text.count(V2736A_MASTERLIST_ROW) == 1,
        "PROJECT_MASTERLIST muss v27.36a exakt einmal als Tabellenzeile führen",
    )
    section = section_between(
        text,
        "## 14. Nächste sinnvolle Aufgaben",
        "## 15. Start in neuem Chat",
        "PROJECT_MASTERLIST",
    )
    validate_required_markers(
        section,
        (
            "`CURRENT_TASK` ist aktuell `v27.36a` / `AUTHORIZED` /",
            f"`{V2736A_AUDIT_FILE}` verändern.",
            "Supabase/Login bleibt der nächste Hauptblock.",
            "nur empfehlen und nicht\nautomatisch auswählen oder autorisieren.",
            "Kein Code, kein Live-Supabase,\nkein Folgetask, kein Commit und kein Push.",
        ),
        "PROJECT_MASTERLIST / aktuelle v27.36a-Steuerung",
    )


def git_is_ancestor(ancestor: str, descendant: str) -> bool:
    completed = subprocess.run(
        ["git", "merge-base", "--is-ancestor", ancestor, descendant],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    require(
        completed.returncode in (0, 1),
        "Git-Abstammungsprüfung konnte nicht ausgeführt werden: "
        + decode_git_stderr(completed.stderr).strip(),
    )
    return completed.returncode == 0


def read_v2736a_working_tree_fact() -> V2736AWorkingTreeFact:
    head = run_git(["rev-parse", "HEAD"]).strip()
    origin_main = run_git(["rev-parse", "origin/main"]).strip()
    audit_tree_entry = run_git(
        [
            "ls-tree",
            "-r",
            "--name-only",
            V2736A_AUTHORIZATION_BASE_SHA,
            "--",
            V2736A_AUDIT_FILE,
        ]
    ).strip()
    audit_head_entry = run_git(
        ["ls-tree", "-r", "--name-only", head, "--", V2736A_AUDIT_FILE]
    ).strip()
    return V2736AWorkingTreeFact(
        branch=run_git(["branch", "--show-current"]).strip(),
        head=head,
        origin_main=origin_main,
        diff_files=frozenset(
            line.strip().replace("\\", "/")
            for line in run_git(["diff", "--name-only"]).splitlines()
            if line.strip()
        ),
        staged_files=frozenset(
            line.strip().replace("\\", "/")
            for line in run_git(["diff", "--cached", "--name-only"]).splitlines()
            if line.strip()
        ),
        untracked_files=frozenset(
            line.strip().replace("\\", "/")
            for line in run_git(
                ["ls-files", "--others", "--exclude-standard"]
            ).splitlines()
            if line.strip()
        ),
        status_lines=frozenset(
            line.replace("\\", "/")
            for line in run_git(
                ["status", "--porcelain=v1", "--untracked-files=all"]
            ).splitlines()
            if line
        ),
        audit_file_exists=(ROOT / V2736A_AUDIT_FILE).exists(),
        audit_file_tracked_at_base=(audit_tree_entry == V2736A_AUDIT_FILE),
        audit_file_tracked_at_head=(audit_head_entry == V2736A_AUDIT_FILE),
        base_is_head_ancestor=git_is_ancestor(
            V2736A_AUTHORIZATION_BASE_SHA, head
        ),
        base_is_origin_ancestor=git_is_ancestor(
            V2736A_AUTHORIZATION_BASE_SHA, origin_main
        ),
        origin_is_head_ancestor=git_is_ancestor(origin_main, head),
    )


def validate_v2736a_working_tree_fact(fact: V2736AWorkingTreeFact) -> None:
    require(fact.branch == "main", "v27.36a-Lebenszyklus muss auf main laufen")
    require(
        fact.base_is_head_ancestor,
        "Die stabile v27.36a-Autorisierungsbasis ist kein Vorfahr von HEAD",
    )
    require(
        fact.base_is_origin_ancestor,
        "Die stabile v27.36a-Autorisierungsbasis ist kein Vorfahr von origin/main",
    )
    require(
        fact.origin_is_head_ancestor,
        "origin/main ist kein Vorfahr des lokalen v27.36a-HEAD",
    )
    require(
        not fact.audit_file_tracked_at_base,
        "Die v27.36a-Audit-Datei darf an der stabilen Basis nicht existieren",
    )
    require(not fact.staged_files, "v27.36a-Lebenszyklus darf nichts stagen")


def detect_v2736a_task_state_text(text: str) -> str:
    task_id = exact_field(text, "Task-ID")
    if task_id == V2736A_EXPECTED_TASK_FIELDS["Task-ID"]:
        validate_exact_fields(text, V2736A_EXPECTED_TASK_FIELDS)
        return V2736A_TASK_AUTHORIZED
    if task_id == V2736A_CLOSED_TASK_FIELDS["Task-ID"]:
        validate_exact_fields(text, V2736A_CLOSED_TASK_FIELDS)
        return V2736A_TASK_CLOSED
    raise ValidationError(f"Unzulässiger v27.36a-Taskzustand: {task_id}")


def v2736a_closure_markers(audit_commit: str) -> tuple[str, ...]:
    return (
        f"Audit-Commit: `{audit_commit}`",
        *V2736A_CLOSURE_CONTENT_MARKERS,
    )


def validate_v2736a_closed_state_text(text: str, audit_commit: str) -> None:
    validate_exact_fields(text, V2736A_CLOSED_STATE_FIELDS)
    section = section_between(
        text,
        "## Abgeschlossener Dokumentations-/Bestandsaudit v27.36a",
        "## Abgeschlossener Dokumentationstask v27.35f",
        "PROJECT_STATE_CURRENT",
    )
    validate_exact_markers(
        section,
        v2736a_closure_markers(audit_commit),
        "PROJECT_STATE_CURRENT / v27.36a-Abschluss",
    )
    validate_required_markers(
        section,
        (
            "### Permanenter v27.36a-Lebenszyklus",
            f"`{V2736A_AUTHORIZATION_BASE_SHA}` ist die stabile",
            "Die lokale\nClosure verändert exakt die fünf Gate-Dateien",
            "Ein späterer CLOSURE-Commit\nwird weiterhin dynamisch erkannt; sein SHA wird nicht hartcodiert.",
            "Rückkehr zu `v27.36a / AUTHORIZED` ohne\nneue ausdrückliche Autorisierung geschlossen blockiert.",
        ),
        "PROJECT_STATE_CURRENT / v27.36a-Closure-Lebenszyklus",
    )


def validate_v2736a_closed_task_text(text: str, audit_commit: str) -> None:
    validate_exact_fields(text, V2736A_CLOSED_TASK_FIELDS)
    section = section_between(
        text,
        "## Abgeschlossener Dokumentations-/Bestandsaudit v27.36a",
        "## Abgeschlossener Dokumentationstask v27.35f",
        "CURRENT_TASK",
    )
    validate_exact_markers(
        section,
        v2736a_closure_markers(audit_commit),
        "CURRENT_TASK / v27.36a-Abschluss",
    )
    validate_required_markers(
        section,
        (
            "## Permanenter v27.36a-Lebenszyklus",
            f"`{V2736A_AUTHORIZATION_BASE_SHA}`",
            "Die lokale\nClosure verändert exakt die fünf Gate-Dateien.",
            "CLOSURE-Commit wird dynamisch erkannt; sein SHA wird nicht hartcodiert.",
            "Rückkehr zu `v27.36a / AUTHORIZED` ohne\nneue ausdrückliche Autorisierung geschlossen blockiert.",
        ),
        "CURRENT_TASK / v27.36a-Closure-Lebenszyklus",
    )


def validate_v2736a_closed_cursor_text(text: str, audit_commit: str) -> None:
    require(
        exact_field(text, "Stand") == "v27.36a",
        "CURSOR_MASTER_CONTEXT_ACCAOUI muss auf v27.36a stehen",
    )
    validate_project_paths(text, "CURSOR_MASTER_CONTEXT_ACCAOUI")
    section = section_between(
        text,
        "## 14. Nächster sinnvoller Schritt",
        "## 15. Wenn ein neuer Chat beginnt",
        "CURSOR_MASTER_CONTEXT_ACCAOUI",
    )
    validate_exact_markers(
        section,
        (
            "`CURRENT_TASK` ist `NONE` / `BLOCKED` / `Autorisiert: NEIN`.",
            *v2736a_closure_markers(audit_commit),
        ),
        "CURSOR_MASTER_CONTEXT_ACCAOUI / v27.36a-Abschluss",
    )
    validate_required_markers(
        section,
        (
            "### Permanenter v27.36a-Lebenszyklus",
            f"`{V2736A_AUTHORIZATION_BASE_SHA}` ist die stabile",
            "Die lokale\nClosure verändert exakt die fünf Gate-Dateien",
            "CLOSURE-Commit wird ohne hartcodierten zukünftigen SHA erkannt.",
            "Rückkehr zu `v27.36a / AUTHORIZED` ohne\nneue ausdrückliche Autorisierung geschlossen blockiert.",
        ),
        "CURSOR_MASTER_CONTEXT_ACCAOUI / v27.36a-Closure-Lebenszyklus",
    )
    require(
        re.search(r"\bv27\.(?:36[b-z]|3[7-9])\b", section, re.IGNORECASE)
        is None,
        "CURSOR_MASTER_CONTEXT_ACCAOUI darf nach v27.36a keinen Folgetask autorisieren",
    )


def validate_v2736a_closed_masterlist_text(text: str, audit_commit: str) -> None:
    require(
        exact_field(text, "Stand") == "v27.36a",
        "PROJECT_MASTERLIST muss auf v27.36a stehen",
    )
    validate_project_paths(text, "PROJECT_MASTERLIST")
    require(
        text.count(V2736A_CLOSED_MASTERLIST_ROW) == 1,
        "PROJECT_MASTERLIST muss den abgeschlossenen v27.36a-Tabelleneintrag exakt einmal führen",
    )
    section = section_between(
        text,
        "## 14. Nächste sinnvolle Aufgaben",
        "## 15. Start in neuem Chat",
        "PROJECT_MASTERLIST",
    )
    validate_exact_markers(
        section,
        (
            "`CURRENT_TASK` ist aktuell `NONE` / `BLOCKED` / `Autorisiert: NEIN`.",
            *v2736a_closure_markers(audit_commit),
        ),
        "PROJECT_MASTERLIST / v27.36a-Abschluss",
    )
    validate_required_markers(
        section,
        (
            f"Die stabile Basis `{V2736A_AUTHORIZATION_BASE_SHA}`",
            "exakt ein\nIMPLEMENTATION-/AUDIT-Commit",
            "späterer CLOSURE-Commit werden dynamisch",
            "Ein zukünftiger Closure-SHA wird\nnicht hartcodiert.",
            "Rückkehr zu `v27.36a / AUTHORIZED` bleibt ohne\nneue ausdrückliche Autorisierung geschlossen blockiert.",
        ),
        "PROJECT_MASTERLIST / v27.36a-Closure-Lebenszyklus",
    )
    require(
        re.search(r"\bv27\.(?:36[b-z]|3[7-9])\b", section, re.IGNORECASE)
        is None,
        "PROJECT_MASTERLIST darf nach v27.36a keinen Folgetask autorisieren",
    )


def validate_v2736a_closed_documents(
    state_text: str,
    task_text: str,
    cursor_text: str,
    masterlist_text: str,
    audit_commit: str,
) -> None:
    validate_v2736a_closed_state_text(state_text, audit_commit)
    validate_v2736a_closed_task_text(task_text, audit_commit)
    validate_v2736a_closed_cursor_text(cursor_text, audit_commit)
    validate_v2736a_closed_masterlist_text(masterlist_text, audit_commit)


def read_v2736a_commit_facts(current_head: str) -> tuple[V2736ACommitFact, ...]:
    commit_shas = tuple(
        line.strip()
        for line in run_git(
            ["rev-list", "--reverse", f"{V2736A_AUTHORIZATION_BASE_SHA}..{current_head}"]
        ).splitlines()
        if line.strip()
    )
    previous_commit = V2736A_AUTHORIZATION_BASE_SHA
    facts: list[V2736ACommitFact] = []
    for commit_sha in commit_shas:
        lineage = run_git(["rev-list", "--parents", "-n", "1", commit_sha]).split()
        require(
            len(lineage) == 2 and lineage[1] == previous_commit,
            "v27.36a-Lebenszyklus erlaubt nur eine lineare Historie ohne Merge-Commit",
        )
        changed_files = frozenset(
            line.strip().replace("\\", "/")
            for line in run_git(
                ["diff", "--name-only", previous_commit, commit_sha]
            ).splitlines()
            if line.strip()
        )
        require(changed_files, f"Leerer v27.36a-Commit unzulässig: {commit_sha}")
        task_text = read_v2735f_commit_document(
            commit_sha, V2735F_TASK_RELATIVE_PATH
        )
        facts.append(
            V2736ACommitFact(
                commit_sha=commit_sha,
                changed_files=changed_files,
                task_state=detect_v2736a_task_state_text(task_text),
            )
        )
        previous_commit = commit_sha
    return tuple(facts)


def validate_v2736a_history_facts(
    commit_facts: tuple[V2736ACommitFact, ...],
) -> V2736AHistoryState:
    gate_files = frozenset(EXPECTED_CONTROL_FILES)
    roles: list[str] = []
    gate_commits: list[str] = []
    audit_commit: str | None = None
    closed = False
    for fact in commit_facts:
        changed_files = fact.changed_files
        if changed_files == frozenset({V2736A_AUDIT_FILE}):
            require(gate_commits, "v27.36a-Audit vor Autorisierungs-GATE unzulässig")
            require(audit_commit is None, "Mehr als ein v27.36a-Audit-Commit unzulässig")
            require(not closed, "v27.36a-Audit nach CLOSURE unzulässig")
            require(
                fact.task_state == V2736A_TASK_AUTHORIZED,
                "v27.36a-Audit-Commit benötigt AUTHORIZED / Autorisiert JA",
            )
            audit_commit = fact.commit_sha
            roles.append(V2736A_ROLE_AUDIT)
            continue

        require(
            changed_files.issubset(gate_files),
            f"Fremde Datei in v27.36a-Commit {fact.commit_sha}: {sorted(changed_files - gate_files)}",
        )
        require(changed_files, f"Leere v27.36a-GATE-Dateimenge: {fact.commit_sha}")
        if fact.task_state == V2736A_TASK_AUTHORIZED:
            require(not closed, "Rückkehr zu v27.36a nach CLOSURE unzulässig")
            gate_commits.append(fact.commit_sha)
            roles.append(V2736A_ROLE_GATE)
            continue
        require(
            fact.task_state == V2736A_TASK_CLOSED,
            f"Unbekannter Taskzustand in v27.36a-Commit {fact.commit_sha}",
        )
        require(audit_commit is not None, "v27.36a-CLOSURE vor Audit unzulässig")
        require(not closed, "Mehr als ein v27.36a-CLOSURE-Commit unzulässig")
        closed = True
        roles.append(V2736A_ROLE_CLOSURE)

    if closed:
        state = V2736A_HISTORY_CLOSED
    elif audit_commit is not None:
        state = V2736A_HISTORY_AUDITED
    elif gate_commits:
        state = V2736A_HISTORY_AUTHORIZED
    else:
        state = V2736A_HISTORY_BEFORE_AUTHORIZATION
    return V2736AHistoryState(
        state=state,
        audit_commit=audit_commit,
        roles=tuple(roles),
        gate_commits=tuple(gate_commits),
    )


def validate_v2736a_committed_closure_documents(
    commit_facts: tuple[V2736ACommitFact, ...],
    history_state: V2736AHistoryState,
) -> None:
    if V2736A_ROLE_CLOSURE not in history_state.roles:
        return
    require(
        history_state.audit_commit is not None,
        "v27.36a-CLOSURE-Dokumentprüfung benötigt einen Audit-Commit",
    )
    for fact, role in zip(commit_facts, history_state.roles):
        if role != V2736A_ROLE_CLOSURE:
            continue
        validate_v2736a_closed_documents(
            read_v2735f_commit_document(fact.commit_sha, "docs/PROJECT_STATE_CURRENT.md"),
            read_v2735f_commit_document(fact.commit_sha, V2735F_TASK_RELATIVE_PATH),
            read_v2735f_commit_document(fact.commit_sha, "docs/CURSOR_MASTER_CONTEXT_ACCAOUI.md"),
            read_v2735f_commit_document(fact.commit_sha, "docs/PROJECT_MASTERLIST.md"),
            history_state.audit_commit,
        )


def validate_v2736a_lifecycle_working_tree(
    history_state: V2736AHistoryState,
    task_state: str,
    fact: V2736AWorkingTreeFact,
) -> str:
    validate_v2736a_working_tree_fact(fact)
    gate_files = frozenset(EXPECTED_CONTROL_FILES)
    clean = not fact.diff_files and not fact.untracked_files and not fact.status_lines

    if history_state.state == V2736A_HISTORY_BEFORE_AUTHORIZATION:
        expected_status = frozenset(f" M {path}" for path in gate_files)
        require(fact.head == V2736A_AUTHORIZATION_BASE_SHA, "Phase 1 benötigt die stabile Basis als HEAD")
        require(task_state == V2736A_TASK_AUTHORIZED, "Phase 1 benötigt v27.36a AUTHORIZED")
        require(fact.diff_files == gate_files, "Phase 1 muss exakt fünf Gate-Dateien ändern")
        require(not fact.untracked_files and fact.status_lines == expected_status, "Working Tree entspricht nicht Phase 1")
        require(not fact.audit_file_exists and not fact.audit_file_tracked_at_head, "Audit-Datei in Phase 1 unzulässig")
        return V2736A_PHASE_1_AUTHORIZATION_PREPARED

    if history_state.state == V2736A_HISTORY_AUTHORIZED:
        require(fact.head != V2736A_AUTHORIZATION_BASE_SHA, "Phase 2 benötigt mindestens einen GATE-Commit")
        require(task_state == V2736A_TASK_AUTHORIZED, "Phase 2/3 benötigt v27.36a AUTHORIZED")
        require(not fact.audit_file_tracked_at_head, "Audit darf vor Phase 4 nicht getrackt sein")
        if clean:
            require(not fact.audit_file_exists, "Audit-Datei darf in Phase 2 noch nicht existieren")
            return V2736A_PHASE_2_AUTHORIZATION_COMMITTED
        if fact.diff_files and fact.diff_files.issubset(gate_files) and not fact.untracked_files:
            expected_status = frozenset(f" M {path}" for path in fact.diff_files)
            require(fact.status_lines == expected_status, "Lokale Phase-2-Gate-Korrektur enthält fremden Status")
            require(not fact.audit_file_exists, "Audit-Datei während lokaler Gate-Korrektur unzulässig")
            return V2736A_PHASE_2_GATE_PREPARED
        audit_status = frozenset({f"?? {V2736A_AUDIT_FILE}"})
        require(not fact.diff_files, "Phase 3 darf keine getrackte Datei verändern")
        require(fact.untracked_files == frozenset({V2736A_AUDIT_FILE}), "Phase 3 darf nur die Audit-Datei enthalten")
        require(fact.status_lines == audit_status and fact.audit_file_exists, "Working Tree entspricht nicht Phase 3")
        return V2736A_PHASE_3_AUDIT_PREPARED

    require(history_state.audit_commit is not None, "Phase nach Audit benötigt dynamischen Audit-Commit")
    require(fact.audit_file_tracked_at_head and fact.audit_file_exists, "Nach Audit muss die Audit-Datei getrackt vorhanden sein")
    if history_state.state == V2736A_HISTORY_AUDITED:
        if task_state == V2736A_TASK_AUTHORIZED:
            require(clean, "Phase 4 benötigt einen sauberen Working Tree")
            return V2736A_PHASE_4_AUDIT_COMMITTED
        require(task_state == V2736A_TASK_CLOSED, "Phase 5 benötigt den geschlossenen Taskzustand")
        expected_status = frozenset(f" M {path}" for path in gate_files)
        require(fact.diff_files == gate_files and not fact.untracked_files, "Phase 5 muss exakt fünf Gate-Dateien ändern")
        require(fact.status_lines == expected_status, "Working Tree entspricht nicht Phase 5")
        return V2736A_PHASE_5_CLOSURE_PREPARED

    require(history_state.state == V2736A_HISTORY_CLOSED, "Unbekannter v27.36a-Historienzustand")
    require(task_state == V2736A_TASK_CLOSED, "Nach CLOSURE darf v27.36a nicht erneut autorisiert sein")
    require(clean, "Phase 6 benötigt einen sauberen Working Tree")
    return V2736A_PHASE_6_CLOSURE_COMMITTED


def validate_v2736a_lifecycle(
    state_text: str,
    task_text: str,
    cursor_text: str,
    masterlist_text: str,
) -> tuple[str, V2736AHistoryState, V2736AWorkingTreeFact]:
    fact = read_v2736a_working_tree_fact()
    validate_v2736a_working_tree_fact(fact)
    commit_facts = read_v2736a_commit_facts(fact.head)
    history_state = validate_v2736a_history_facts(commit_facts)
    validate_v2736a_committed_closure_documents(commit_facts, history_state)
    task_state = detect_v2736a_task_state_text(task_text)
    if task_state == V2736A_TASK_AUTHORIZED:
        validate_v2736a_state_text(state_text)
        validate_v2736a_task_text(task_text)
        validate_v2736a_cursor_text(cursor_text)
        validate_v2736a_masterlist_text(masterlist_text)
    else:
        require(history_state.audit_commit is not None, "v27.36a-Abschluss vor Audit unzulässig")
        validate_v2736a_closed_documents(
            state_text,
            task_text,
            cursor_text,
            masterlist_text,
            history_state.audit_commit,
        )
    phase = validate_v2736a_lifecycle_working_tree(history_state, task_state, fact)
    return phase, history_state, fact


def exercise_v2736a_section_marker_manipulations(
    validator: Callable[[str], None],
    text: str,
    start_heading: str,
    end_heading: str,
    markers: tuple[str, ...],
    document_name: str,
) -> int:
    section = section_between(text, start_heading, end_heading, document_name)
    checks = 0
    for marker in markers:
        require(
            section.count(marker) == 1,
            f"{document_name}: Closure-Pflichtaussage muss für die Manipulation exakt einmal im aktiven Abschnitt vorkommen: {marker}",
        )
        removed_section = section.replace(marker, "", 1)
        must_reject(
            validator,
            text.replace(section, removed_section, 1),
            f"{document_name}: Closure-Pflichtaussage entfernt: {marker}",
        )
        checks += 1
        duplicated_section = section.replace(marker, marker + "\n" + marker, 1)
        must_reject(
            validator,
            text.replace(section, duplicated_section, 1),
            f"{document_name}: Closure-Pflichtaussage dupliziert: {marker}",
        )
        checks += 1
    return checks


def run_v2736a_lifecycle_manipulation_matrix(
    state_text: str,
    task_text: str,
    cursor_text: str,
    masterlist_text: str,
    current_history: V2736AHistoryState,
    current_fact: V2736AWorkingTreeFact,
) -> tuple[int, int, int]:
    checks = 0
    task_state = detect_v2736a_task_state_text(task_text)
    if task_state == V2736A_TASK_AUTHORIZED:
        field_groups = (
            (state_text, validate_v2736a_state_text, V2736A_EXPECTED_STATE_FIELDS, "PROJECT_STATE_CURRENT"),
            (task_text, validate_v2736a_task_text, V2736A_EXPECTED_TASK_FIELDS, "CURRENT_TASK"),
        )
        marker_groups = (
            (state_text, validate_v2736a_state_text, V2736A_STATE_REQUIRED_MARKERS + V2736A_STATE_LIFECYCLE_MARKERS, "PROJECT_STATE_CURRENT"),
            (task_text, validate_v2736a_task_text, V2736A_TASK_REQUIRED_MARKERS + V2736A_TASK_LIFECYCLE_MARKERS, "CURRENT_TASK"),
            (cursor_text, validate_v2736a_cursor_text, V2736A_CURSOR_REQUIRED_MARKERS + V2736A_CURSOR_LIFECYCLE_MARKERS, "CURSOR_MASTER_CONTEXT_ACCAOUI"),
            (masterlist_text, validate_v2736a_masterlist_text, V2736A_MASTERLIST_REQUIRED_MARKERS + V2736A_MASTERLIST_LIFECYCLE_MARKERS, "PROJECT_MASTERLIST"),
        )
    else:
        require(
            current_history.audit_commit is not None,
            "v27.36a-Closure-Manipulationsmatrix benötigt den Audit-Commit",
        )
        audit_commit = current_history.audit_commit
        closed_state_validator = lambda value: validate_v2736a_closed_state_text(value, audit_commit)
        closed_task_validator = lambda value: validate_v2736a_closed_task_text(value, audit_commit)
        closed_cursor_validator = lambda value: validate_v2736a_closed_cursor_text(value, audit_commit)
        closed_masterlist_validator = lambda value: validate_v2736a_closed_masterlist_text(value, audit_commit)
        field_groups = (
            (state_text, closed_state_validator, V2736A_CLOSED_STATE_FIELDS, "PROJECT_STATE_CURRENT"),
            (task_text, closed_task_validator, V2736A_CLOSED_TASK_FIELDS, "CURRENT_TASK"),
        )
        marker_groups = tuple()

    for text, validator, expected_fields, document_name in field_groups:
        for field_name, expected_value in expected_fields.items():
            manipulated = changed_once(text, f"{field_name}: {expected_value}", f"{field_name}: MANIPULIERT", f"{document_name} / {field_name}")
            must_reject(validator, manipulated, f"{document_name}: manipuliertes Feld {field_name}")
            checks += 1

    for text, validator, markers, document_name in marker_groups:
        for marker in markers:
            require(marker in text, f"Manipulationsmatrix kann Pflichtaussage nicht finden: {document_name} / {marker}")
            must_reject(validator, text.replace(marker, ""), f"{document_name}: Pflichtaussage entfernt: {marker}")
            checks += 1

    if task_state == V2736A_TASK_CLOSED:
        closure_markers = v2736a_closure_markers(audit_commit)
        checks += exercise_v2736a_section_marker_manipulations(
            closed_state_validator,
            state_text,
            "## Abgeschlossener Dokumentations-/Bestandsaudit v27.36a",
            "## Abgeschlossener Dokumentationstask v27.35f",
            closure_markers,
            "PROJECT_STATE_CURRENT",
        )
        checks += exercise_v2736a_section_marker_manipulations(
            closed_task_validator,
            task_text,
            "## Abgeschlossener Dokumentations-/Bestandsaudit v27.36a",
            "## Abgeschlossener Dokumentationstask v27.35f",
            closure_markers,
            "CURRENT_TASK",
        )
        checks += exercise_v2736a_section_marker_manipulations(
            closed_cursor_validator,
            cursor_text,
            "## 14. Nächster sinnvoller Schritt",
            "## 15. Wenn ein neuer Chat beginnt",
            ("`CURRENT_TASK` ist `NONE` / `BLOCKED` / `Autorisiert: NEIN`.", *closure_markers),
            "CURSOR_MASTER_CONTEXT_ACCAOUI",
        )
        checks += exercise_v2736a_section_marker_manipulations(
            closed_masterlist_validator,
            masterlist_text,
            "## 14. Nächste sinnvolle Aufgaben",
            "## 15. Start in neuem Chat",
            ("`CURRENT_TASK` ist aktuell `NONE` / `BLOCKED` / `Autorisiert: NEIN`.", *closure_markers),
            "PROJECT_MASTERLIST",
        )
        removed_row = changed_once(
            masterlist_text,
            V2736A_CLOSED_MASTERLIST_ROW,
            "",
            "PROJECT_MASTERLIST / abgeschlossener v27.36a-Tabelleneintrag",
        )
        must_reject(
            closed_masterlist_validator,
            removed_row,
            "PROJECT_MASTERLIST: abgeschlossener v27.36a-Tabelleneintrag entfernt",
        )
        checks += 1
        duplicated_row = changed_once(
            masterlist_text,
            V2736A_CLOSED_MASTERLIST_ROW,
            V2736A_CLOSED_MASTERLIST_ROW + "\n" + V2736A_CLOSED_MASTERLIST_ROW,
            "PROJECT_MASTERLIST / duplizierter v27.36a-Tabelleneintrag",
        )
        must_reject(
            closed_masterlist_validator,
            duplicated_row,
            "PROJECT_MASTERLIST: abgeschlossener v27.36a-Tabelleneintrag dupliziert",
        )
        checks += 1

    gate = V2736ACommitFact("1" * 40, frozenset({EXPECTED_CONTROL_FILES[0]}), V2736A_TASK_AUTHORIZED)
    audit = V2736ACommitFact("2" * 40, frozenset({V2736A_AUDIT_FILE}), V2736A_TASK_AUTHORIZED)
    closure = V2736ACommitFact("3" * 40, frozenset({EXPECTED_CONTROL_FILES[1]}), V2736A_TASK_CLOSED)
    histories = (
        validate_v2736a_history_facts(tuple()),
        validate_v2736a_history_facts((gate,)),
        validate_v2736a_history_facts((gate, audit)),
        validate_v2736a_history_facts((gate, audit, closure)),
    )
    gate_files = frozenset(EXPECTED_CONTROL_FILES)
    clean_fact = replace(
        current_fact,
        head="1" * 40,
        diff_files=frozenset(), staged_files=frozenset(), untracked_files=frozenset(), status_lines=frozenset(),
        audit_file_exists=False, audit_file_tracked_at_base=False, audit_file_tracked_at_head=False,
        base_is_head_ancestor=True, base_is_origin_ancestor=True, origin_is_head_ancestor=True,
    )
    phase_fixtures = (
        (histories[0], V2736A_TASK_AUTHORIZED, replace(clean_fact, head=V2736A_AUTHORIZATION_BASE_SHA, diff_files=gate_files, status_lines=frozenset(f" M {p}" for p in gate_files)), V2736A_PHASE_1_AUTHORIZATION_PREPARED),
        (histories[1], V2736A_TASK_AUTHORIZED, clean_fact, V2736A_PHASE_2_AUTHORIZATION_COMMITTED),
        (histories[1], V2736A_TASK_AUTHORIZED, replace(clean_fact, diff_files=frozenset({EXPECTED_CONTROL_FILES[0]}), status_lines=frozenset({f" M {EXPECTED_CONTROL_FILES[0]}"})), V2736A_PHASE_2_GATE_PREPARED),
        (histories[1], V2736A_TASK_AUTHORIZED, replace(clean_fact, untracked_files=frozenset({V2736A_AUDIT_FILE}), status_lines=frozenset({f"?? {V2736A_AUDIT_FILE}"}), audit_file_exists=True), V2736A_PHASE_3_AUDIT_PREPARED),
        (histories[2], V2736A_TASK_AUTHORIZED, replace(clean_fact, audit_file_exists=True, audit_file_tracked_at_head=True), V2736A_PHASE_4_AUDIT_COMMITTED),
        (histories[2], V2736A_TASK_CLOSED, replace(clean_fact, diff_files=gate_files, status_lines=frozenset(f" M {p}" for p in gate_files), audit_file_exists=True, audit_file_tracked_at_head=True), V2736A_PHASE_5_CLOSURE_PREPARED),
        (histories[3], V2736A_TASK_CLOSED, replace(clean_fact, audit_file_exists=True, audit_file_tracked_at_head=True), V2736A_PHASE_6_CLOSURE_COMMITTED),
    )
    for history, task_state, fact, expected_phase in phase_fixtures:
        require(validate_v2736a_lifecycle_working_tree(history, task_state, fact) == expected_phase, f"Positivsimulation fehlgeschlagen: {expected_phase}")
    positive_tests = len(phase_fixtures)

    bad_history_fixtures = (
        ((audit,), "Audit vor Autorisierung"),
        ((gate, audit, audit), "zweiter Audit"),
        ((V2736ACommitFact("4" * 40, frozenset({"app.js"}), V2736A_TASK_AUTHORIZED),), "App-Code"),
        ((V2736ACommitFact("5" * 40, frozenset({"unexpected.txt"}), V2736A_TASK_AUTHORIZED),), "fremde Datei"),
        ((gate, closure), "Closure vor Audit"),
        ((gate, V2736ACommitFact("6" * 40, frozenset({V2736A_AUDIT_FILE}), V2736A_TASK_CLOSED)), "Audit mit geschlossenem Task"),
        ((gate, audit, closure, gate), "Rückkehr aus Closure"),
        ((gate, audit, closure, closure), "zweiter Closure-Commit"),
        ((gate, V2736ACommitFact("7" * 40, frozenset({V2736A_AUDIT_FILE, "app.js"}), V2736A_TASK_AUTHORIZED)), "Audit mit Zusatzdatei"),
    )
    for facts, label in bad_history_fixtures:
        try:
            validate_v2736a_history_facts(facts)
        except ValidationError:
            checks += 1
            continue
        raise ValidationError(f"v27.36a-Historienmanipulation wurde nicht blockiert: {label}")

    bad_working_fixtures = (
        (current_history, V2736A_TASK_AUTHORIZED, replace(current_fact, staged_files=frozenset({EXPECTED_CONTROL_FILES[0]})), "gestagte Datei"),
        (current_history, V2736A_TASK_AUTHORIZED, replace(current_fact, diff_files=frozenset((*current_fact.diff_files, "app.js")), status_lines=frozenset((*current_fact.status_lines, " M app.js"))), "App-Datei lokal"),
        (current_history, V2736A_TASK_AUTHORIZED, replace(current_fact, untracked_files=frozenset({"unexpected.txt"}), status_lines=frozenset((*current_fact.status_lines, "?? unexpected.txt"))), "zusätzliche ungetrackte Datei"),
        (current_history, V2736A_TASK_AUTHORIZED, replace(current_fact, base_is_head_ancestor=False), "Basis nicht HEAD-Vorfahr"),
        (current_history, V2736A_TASK_AUTHORIZED, replace(current_fact, origin_is_head_ancestor=False), "origin nicht HEAD-Vorfahr"),
        (current_history, V2736A_TASK_AUTHORIZED, replace(current_fact, audit_file_tracked_at_base=True), "Audit an Basis"),
        (histories[0], V2736A_TASK_AUTHORIZED, replace(clean_fact, head=V2736A_AUTHORIZATION_BASE_SHA, untracked_files=frozenset({V2736A_AUDIT_FILE}), status_lines=frozenset({f"?? {V2736A_AUDIT_FILE}"}), audit_file_exists=True), "Audit lokal vor Autorisierung"),
        (histories[1], V2736A_TASK_CLOSED, replace(clean_fact, diff_files=gate_files, status_lines=frozenset(f" M {p}" for p in gate_files)), "Closure lokal vor Audit"),
        (histories[2], V2736A_TASK_AUTHORIZED, replace(clean_fact, diff_files=gate_files, status_lines=frozenset(f" M {p}" for p in gate_files), audit_file_exists=True, audit_file_tracked_at_head=True), "Rückkehr zu AUTHORIZED während lokaler Closure"),
    )
    for history, task_state, fact, label in bad_working_fixtures:
        try:
            validate_v2736a_lifecycle_working_tree(history, task_state, fact)
        except ValidationError:
            checks += 1
            continue
        raise ValidationError(f"v27.36a-Working-Tree-Manipulation wurde nicht blockiert: {label}")
    negative_tests = len(bad_history_fixtures) + len(bad_working_fixtures)
    return checks, positive_tests, negative_tests


V2736A_AUDIT_COMMIT_SHA = "f545a6c2b14a64a5bcb7bf60a2932315e571ef01"
V2736B_AUTHORIZATION_BASE_SHA = "f7672c98a1368dec501416853830ac03e0de2d41"
V2736B_TITLE = (
    "Lokale injizierbare Auth-/Teilnehmerzugangs-Komponente mit "
    "Fake-Client umsetzen"
)
V2736B_IMPLEMENTATION_FILES = frozenset(
    {
        "data/supabase-participant-access-adapter.js",
        "tools/check-supabase-participant-access-adapter.py",
        "docs/SUPABASE_PARTICIPANT_ACCESS_ADAPTER_V2736B.md",
        "tools/preflight.py",
    }
)
V2736B_NEW_IMPLEMENTATION_FILES = frozenset(
    {
        "data/supabase-participant-access-adapter.js",
        "tools/check-supabase-participant-access-adapter.py",
        "docs/SUPABASE_PARTICIPANT_ACCESS_ADAPTER_V2736B.md",
    }
)
V2736B_ALLOWED_FILES_VALUE = (
    "`data/supabase-participant-access-adapter.js`, "
    "`tools/check-supabase-participant-access-adapter.py`, "
    "`docs/SUPABASE_PARTICIPANT_ACCESS_ADAPTER_V2736B.md`, "
    "`tools/preflight.py`"
)
V2736B_EXPECTED_STATE_FIELDS = {
    "Stand": "v27.36b",
    "Repository": "`asarrad-bit/accaoui-34a-lernapp`",
    "Branch": "`main`",
    "Letzter abgeschlossener funktionaler Stand": "v27.35g",
    "Abschlusscommit": f"`{V2735G_COMPLETION_SHA}`",
    "Aktueller HEAD": "DYNAMISCH ZU PRÜFEN",
    "Funktionsstatus": "v27.35g abgeschlossen",
    "Weiterer funktionaler Schritt autorisiert": "JA",
    "Aktuell autorisierter Task": "v27.36b",
    "Aktuelle Taskart": "Lokale Auth-/Teilnehmerzugangs-Komponente",
    "Aktueller Blocker": (
        "KEINER für die ausdrücklich autorisierte spätere v27.36b-Umsetzung; "
        "in diesem Autorisierungsschritt erfolgt noch keine Implementierung"
    ),
}
V2736B_EXPECTED_TASK_FIELDS = {
    "Task-ID": "v27.36b",
    "Status": "AUTHORIZED",
    "Autorisiert": "JA",
    "Titel": V2736B_TITLE,
    "Funktionaler Ausgangsstand": "v27.35g",
    "Erwarteter Ausgangscommit": f"`{V2736B_AUTHORIZATION_BASE_SHA}`",
    "Erlaubte Dateien": V2736B_ALLOWED_FILES_VALUE,
    "Commit erlaubt": "NEIN",
    "Push erlaubt": "NEIN",
}
V2736B_CLOSED_STATE_FIELDS = {
    "Stand": "v27.36b",
    "Repository": "`asarrad-bit/accaoui-34a-lernapp`",
    "Branch": "`main`",
    "Letzter abgeschlossener funktionaler Stand": "v27.35g",
    "Abschlusscommit": f"`{V2735G_COMPLETION_SHA}`",
    "Aktueller HEAD": "DYNAMISCH ZU PRÜFEN",
    "Funktionsstatus": "v27.35g abgeschlossen",
    "Weiterer funktionaler Schritt autorisiert": "NEIN",
    "Aktuell autorisierter Task": "NONE",
    "Aktuelle Taskart": "Kein Task autorisiert",
    "Aktueller Blocker": (
        "Neue Taskauswahl und ausdrückliche Autorisierung durch "
        "Projekteigentümer und verbindlichen Projektchat"
    ),
}
V2736B_CLOSED_TASK_FIELDS = {
    "Task-ID": "NONE",
    "Status": "BLOCKED",
    "Autorisiert": "NEIN",
    "Titel": "Kein Task autorisiert",
    "Funktionaler Ausgangsstand": "v27.35g",
    "Letzter abgeschlossener Kontrollschritt": "v27.36b",
    "Erlaubte Dateien": "KEINE",
    "Commit erlaubt": "NEIN",
    "Push erlaubt": "NEIN",
}
V2736B_STATE_MARKERS = (
    "## Autorisierter Task v27.36b",
    "v27.36a ist vollständig abgeschlossen.",
    "wird jetzt ausdrücklich als v27.36b autorisiert.",
    "v27.36b ist der einzige autorisierte Task.",
    "Für die spätere Umsetzung sind genau vier Dateien erlaubt:",
    "In diesem Autorisierungsschritt wird die Komponente noch nicht implementiert.",
    "Supabase bleibt NICHT LIVE.",
    "Kein Folgetask nach v27.36b wurde ausgewählt oder autorisiert.",
    "### Permanenter v27.36b-Lebenszyklus",
    "mindestens sechs Phasen",
    "Rückkehr aus der abgeschlossenen v27.36b-Closure",
)
V2736B_TASK_MARKERS = (
    "## Autorisierter Task v27.36b",
    "Dieser Codex-Schritt autorisiert v27.36b nur.",
    "## Verbindliches Funktionsziel",
    "einen explizit injizierten Supabase-kompatiblen Client",
    "eine explizit injizierte UTC-Zeitquelle",
    "`session.user.id`",
    "`participants`, `enrollments` und `courses`",
    "## Fail-closed Access-State",
    "## Lokaler Fake-Client und Testgrenze",
    "lokalen synthetischen\nIn-Memory-Fake-Client",
    "## Ausdrücklich verboten",
    "Supabase bleibt NICHT LIVE.",
    "## Permanenter v27.36b-Lebenszyklus",
    "Mindestens sechs Phasen werden dynamisch erkannt",
    "Rückkehr aus einer abgeschlossenen v27.36b-Closure",
)
V2736B_CURSOR_MARKERS = (
    "`CURRENT_TASK` ist `v27.36b` / `AUTHORIZED` / `Autorisiert: JA`.",
    "Einziger autorisierter Task: Lokale injizierbare",
    "In diesem Autorisierungsschritt wird die Komponente noch nicht implementiert.",
    "Supabase bleibt NICHT LIVE.",
    "### Permanenter v27.36b-Lebenszyklus",
    "Mindestens sechs Phasen werden erkannt",
    "Rückkehr aus der\nabgeschlossenen v27.36b-Closure",
)
V2736B_MASTERLIST_ROW_PREFIX = "| v27.36b | Lokale injizierbare Auth-/Teilnehmerzugangs-Komponente"
V2736B_MASTERLIST_MARKERS = (
    "`CURRENT_TASK` ist aktuell `v27.36b` / `AUTHORIZED` / `Autorisiert: JA`.",
    "v27.36b ist der einzige autorisierte Task.",
    "In diesem Autorisierungsschritt wird die Komponente noch nicht implementiert.",
    "Supabase bleibt NICHT LIVE.",
    "### Permanenter v27.36b-Lebenszyklus",
    "mindestens sechs Phasen",
    "Rückkehr aus abgeschlossener v27.36b-Closure",
)
V2736B_CLOSURE_MARKERS = (
    "v27.36b abgeschlossen.",
    "Der letzte abgeschlossene funktionale Stand bleibt v27.35g.",
    "Der permanente Preflight enthält den Adapter-Checker.",
    "Mindestprüfungen plus 26 Manipulationsprüfungen = 75 PASS.",
    "einen explizit injizierten\nSupabase-kompatiblen Client und eine explizit injizierte UTC-Zeitquelle.",
    "`session.user.id` ist die einzige Autorität",
    "`participants`, `enrollments` und `courses`.",
    "fail-closed",
    "In-Memory-Fake-Client.",
    "Keine App-Integration. Kein SDK. Kein realer Client. Kein Netzwerkzugriff.",
    "Kein Datenbankzugriff. Keine SQL-Ausführung. Keine Migrationsausführung.",
    "Supabase bleibt NICHT LIVE.",
    "Keine echten Keys.",
    "Keine echten Teilnehmerdaten.",
    "Kein Folgetask wurde ausgewählt oder autorisiert.",
    "Die nächste Umsetzung\nbleibt vollständig BLOCKED, bis sie ausdrücklich autorisiert wird.",
    "Keine zukünftige\nClosure-SHA wird hartcodiert.",
    "Rückkehr zu einem autorisierten v27.36b-Zustand bleibt ohne neue\nausdrückliche Autorisierung blockiert.",
)
V2736B_TASK_AUTHORIZED = "authorized"
V2736B_TASK_CLOSED = "closed"
V2736B_HISTORY_BEFORE_AUTHORIZATION = "before_authorization_commit"
V2736B_HISTORY_AUTHORIZED = "authorization_committed"
V2736B_HISTORY_IMPLEMENTED = "implementation_committed"
V2736B_HISTORY_CLOSED = "closure_committed"
V2736B_PHASE_1_AUTHORIZATION_PREPARED = "phase_1_authorization_prepared"
V2736B_PHASE_2_AUTHORIZATION_COMMITTED = "phase_2_authorization_committed"
V2736B_PHASE_2_GATE_PREPARED = "phase_2_gate_correction_prepared"
V2736B_PHASE_3_IMPLEMENTATION_PREPARED = "phase_3_implementation_prepared"
V2736B_PHASE_4_IMPLEMENTATION_COMMITTED = "phase_4_implementation_committed"
V2736B_PHASE_4_GATE_PREPARED = "phase_4_gate_correction_prepared"
V2736B_PHASE_5_CLOSURE_PREPARED = "phase_5_closure_prepared"
V2736B_PHASE_6_CLOSURE_COMMITTED = "phase_6_closure_committed"
V2736B_ROLE_GATE = "GATE"
V2736B_ROLE_IMPLEMENTATION = "IMPLEMENTATION"
V2736B_ROLE_CLOSURE = "CLOSURE"


@dataclass(frozen=True)
class V2736BCommitFact:
    commit_sha: str
    changed_files: frozenset[str]
    task_state: str


@dataclass(frozen=True)
class V2736BHistoryState:
    state: str
    implementation_commit: str | None
    roles: tuple[str, ...]
    gate_commits: tuple[str, ...]


@dataclass(frozen=True)
class V2736BWorkingTreeFact:
    branch: str
    head: str
    origin_main: str
    diff_files: frozenset[str]
    staged_files: frozenset[str]
    untracked_files: frozenset[str]
    status_lines: frozenset[str]
    implementation_files_existing: frozenset[str]
    implementation_files_tracked_at_base: frozenset[str]
    implementation_files_tracked_at_head: frozenset[str]
    base_is_head_ancestor: bool
    base_is_origin_ancestor: bool
    origin_is_head_ancestor: bool


def validate_no_future_v2736b_sha(
    section: str,
    allowed_shas: frozenset[str],
    document_name: str,
) -> None:
    shas = frozenset(re.findall(r"\b[0-9a-f]{40}\b", section))
    require(
        shas.issubset(allowed_shas),
        f"{document_name}: zukünftige v27.36b-Commit-SHA hartcodiert: {sorted(shas - allowed_shas)}",
    )
    require(
        re.search(r"\bv27\.(?:36[c-z]|3[7-9])\b", section, re.IGNORECASE) is None,
        f"{document_name}: automatischer Folgetask nach v27.36b unzulässig",
    )


def validate_v2736b_state_text(text: str) -> None:
    validate_exact_fields(text, V2736B_EXPECTED_STATE_FIELDS)
    section = section_between(
        text,
        "## Autorisierter Task v27.36b",
        "## Abgeschlossener Dokumentations-/Bestandsaudit v27.36a",
        "PROJECT_STATE_CURRENT",
    )
    validate_required_markers(section, V2736B_STATE_MARKERS, "PROJECT_STATE_CURRENT / v27.36b")
    validate_no_future_v2736b_sha(
        section,
        frozenset({V2736B_AUTHORIZATION_BASE_SHA}),
        "PROJECT_STATE_CURRENT / v27.36b",
    )
    for path in V2736B_IMPLEMENTATION_FILES:
        require(section.count(f"`{path}`") == 1, f"PROJECT_STATE_CURRENT: v27.36b-Datei fehlt oder ist doppelt: {path}")


def validate_v2736b_task_text(text: str) -> None:
    validate_exact_fields(text, V2736B_EXPECTED_TASK_FIELDS)
    require(
        text.count(f"Erlaubte Dateien: {V2736B_ALLOWED_FILES_VALUE}") == 1,
        "CURRENT_TASK muss exakt eine verbindliche v27.36b-Dateifreigabe enthalten",
    )
    section = section_between(
        text,
        "## Autorisierter Task v27.36b",
        "## Abgeschlossener Dokumentations-/Bestandsaudit v27.36a",
        "CURRENT_TASK",
    )
    validate_required_markers(section, V2736B_TASK_MARKERS, "CURRENT_TASK / v27.36b")
    validate_no_future_v2736b_sha(
        section,
        frozenset({V2736B_AUTHORIZATION_BASE_SHA}),
        "CURRENT_TASK / v27.36b",
    )
    for path in V2736B_IMPLEMENTATION_FILES:
        require(section.count(f"`{path}`") >= 1, f"CURRENT_TASK: v27.36b-Datei fehlt: {path}")


def validate_v2736b_cursor_text(text: str) -> None:
    require(exact_field(text, "Stand") == "v27.36b", "CURSOR-Kontext muss auf v27.36b stehen")
    validate_project_paths(text, "CURSOR_MASTER_CONTEXT_ACCAOUI")
    section = section_between(
        text,
        "## 14. Nächster sinnvoller Schritt",
        "## 15. Wenn ein neuer Chat beginnt",
        "CURSOR_MASTER_CONTEXT_ACCAOUI",
    )
    validate_required_markers(section, V2736B_CURSOR_MARKERS, "CURSOR_MASTER_CONTEXT_ACCAOUI / v27.36b")
    validate_no_future_v2736b_sha(
        section,
        frozenset({V2736A_AUDIT_COMMIT_SHA, V2736B_AUTHORIZATION_BASE_SHA}),
        "CURSOR_MASTER_CONTEXT_ACCAOUI / v27.36b",
    )
    for path in V2736B_IMPLEMENTATION_FILES:
        require(section.count(f"`{path}`") == 1, f"CURSOR-Kontext: v27.36b-Datei fehlt oder ist doppelt: {path}")


def validate_v2736b_masterlist_text(text: str) -> None:
    require(exact_field(text, "Stand") == "v27.36b", "PROJECT_MASTERLIST muss auf v27.36b stehen")
    validate_project_paths(text, "PROJECT_MASTERLIST")
    require(
        text.count(V2736B_MASTERLIST_ROW_PREFIX) == 1,
        "PROJECT_MASTERLIST muss v27.36b exakt einmal als autorisierte Tabellenzeile führen",
    )
    section = section_between(
        text,
        "## 14. Nächste sinnvolle Aufgaben",
        "## 15. Start in neuem Chat",
        "PROJECT_MASTERLIST",
    )
    validate_required_markers(section, V2736B_MASTERLIST_MARKERS, "PROJECT_MASTERLIST / v27.36b")
    validate_no_future_v2736b_sha(
        section,
        frozenset({V2736A_AUDIT_COMMIT_SHA, V2736B_AUTHORIZATION_BASE_SHA}),
        "PROJECT_MASTERLIST / v27.36b",
    )
    for path in V2736B_IMPLEMENTATION_FILES:
        require(section.count(f"`{path}`") == 1, f"PROJECT_MASTERLIST: v27.36b-Datei fehlt oder ist doppelt: {path}")


def detect_v2736b_task_state_text(text: str) -> str:
    task_id = exact_field(text, "Task-ID")
    if task_id == "v27.36b":
        validate_exact_fields(text, V2736B_EXPECTED_TASK_FIELDS)
        return V2736B_TASK_AUTHORIZED
    if task_id == "NONE":
        validate_exact_fields(text, V2736B_CLOSED_TASK_FIELDS)
        return V2736B_TASK_CLOSED
    raise ValidationError(f"Unzulässiger v27.36b-Taskzustand: {task_id}")


def validate_v2736b_closed_documents(
    state_text: str,
    task_text: str,
    cursor_text: str,
    masterlist_text: str,
    implementation_commit: str,
) -> None:
    require(
        re.fullmatch(r"[0-9a-f]{40}", implementation_commit) is not None,
        "v27.36b-Closure benötigt einen dynamisch erkannten Implementierungscommit",
    )
    validate_exact_fields(state_text, V2736B_CLOSED_STATE_FIELDS)
    validate_exact_fields(task_text, V2736B_CLOSED_TASK_FIELDS)
    require(exact_field(cursor_text, "Stand") == "v27.36b", "CURSOR-Kontext muss nach v27.36b-Closure auf v27.36b stehen")
    require(exact_field(masterlist_text, "Stand") == "v27.36b", "PROJECT_MASTERLIST muss nach v27.36b-Closure auf v27.36b stehen")
    validate_project_paths(cursor_text, "CURSOR_MASTER_CONTEXT_ACCAOUI")
    validate_project_paths(masterlist_text, "PROJECT_MASTERLIST")
    state_section = section_between(state_text, "## Abgeschlossener isolierter Technikschritt v27.36b", "## Abgeschlossener Dokumentations-/Bestandsaudit v27.36a", "PROJECT_STATE_CURRENT")
    task_section = section_between(task_text, "## Abgeschlossener isolierter Technikschritt v27.36b", "## Abgeschlossener Dokumentations-/Bestandsaudit v27.36a", "CURRENT_TASK")
    cursor_section = section_between(cursor_text, "## 14. Nächster sinnvoller Schritt", "## 15. Wenn ein neuer Chat beginnt", "CURSOR_MASTER_CONTEXT_ACCAOUI")
    master_section = section_between(masterlist_text, "## 14. Nächste sinnvolle Aufgaben", "## 15. Start in neuem Chat", "PROJECT_MASTERLIST")
    for text, name in (
        (state_section, "PROJECT_STATE_CURRENT"),
        (task_section, "CURRENT_TASK"),
        (cursor_section, "CURSOR_MASTER_CONTEXT_ACCAOUI"),
        (master_section, "PROJECT_MASTERLIST"),
    ):
        validate_required_markers(text, V2736B_CLOSURE_MARKERS, f"{name} / v27.36b-Closure")
        require("v27.36b / AUTHORIZED" not in text, f"{name}: Rückkehr zu v27.36b / AUTHORIZED nach Closure")
        require(
            text.count(f"Implementierungscommit: `{implementation_commit}`") == 1,
            f"{name}: dynamisch erkannter v27.36b-Implementierungscommit fehlt oder ist doppelt",
        )
        validate_no_future_v2736b_sha(
            text,
            frozenset({V2736A_AUDIT_COMMIT_SHA, V2736B_AUTHORIZATION_BASE_SHA, implementation_commit}),
            f"{name} / v27.36b-Closure",
        )
        for path in V2736B_IMPLEMENTATION_FILES:
            require(text.count(f"`{path}`") == 1, f"{name}: v27.36b-Implementierungsdatei fehlt oder ist doppelt: {path}")
    require("`CURRENT_TASK` ist `NONE` / `BLOCKED` / `Autorisiert: NEIN`." in cursor_section, "CURSOR-Kontext muss v27.36b geschlossen blockieren")
    require("`CURRENT_TASK` ist aktuell `NONE` / `BLOCKED` / `Autorisiert: NEIN`." in master_section, "PROJECT_MASTERLIST muss v27.36b geschlossen blockieren")
    rows = re.findall(r"(?m)^\| v27\.36b \|.*$", masterlist_text)
    require(
        len(rows) == 1
        and "**erledigt**" in rows[0]
        and implementation_commit in rows[0],
        "PROJECT_MASTERLIST muss v27.36b nach Closure exakt einmal mit dynamischem Implementierungscommit als erledigt führen",
    )


def validate_v2736a_completed_base() -> tuple[V2736AHistoryState, tuple[str, str, str, str]]:
    require(
        git_is_ancestor(V2736A_AUTHORIZATION_BASE_SHA, V2736B_AUTHORIZATION_BASE_SHA),
        "v27.36a-Autorisierungsbasis ist kein Vorfahr der stabilen v27.36b-Basis",
    )
    commit_facts = read_v2736a_commit_facts(V2736B_AUTHORIZATION_BASE_SHA)
    history = validate_v2736a_history_facts(commit_facts)
    require(history.state == V2736A_HISTORY_CLOSED, "v27.36a muss an der v27.36b-Basis vollständig geschlossen sein")
    require(history.audit_commit == V2736A_AUDIT_COMMIT_SHA, "Der belegte v27.36a-Audit-Commit weicht ab")
    require(history.roles.count(V2736A_ROLE_AUDIT) == 1, "v27.36a benötigt exakt einen Audit-Commit")
    validate_v2736a_committed_closure_documents(commit_facts, history)
    base_documents = (
        read_v2735f_commit_document(V2736B_AUTHORIZATION_BASE_SHA, "docs/PROJECT_STATE_CURRENT.md"),
        read_v2735f_commit_document(V2736B_AUTHORIZATION_BASE_SHA, V2735F_TASK_RELATIVE_PATH),
        read_v2735f_commit_document(V2736B_AUTHORIZATION_BASE_SHA, "docs/CURSOR_MASTER_CONTEXT_ACCAOUI.md"),
        read_v2735f_commit_document(V2736B_AUTHORIZATION_BASE_SHA, "docs/PROJECT_MASTERLIST.md"),
    )
    validate_v2736a_closed_documents(*base_documents, V2736A_AUDIT_COMMIT_SHA)
    require(
        run_git(["ls-tree", "-r", "--name-only", V2736B_AUTHORIZATION_BASE_SHA, "--", V2736A_AUDIT_FILE]).strip() == V2736A_AUDIT_FILE,
        "v27.36a-Audit-Datei fehlt an der stabilen v27.36b-Basis",
    )
    return history, base_documents


def read_v2736b_commit_facts(current_head: str) -> tuple[V2736BCommitFact, ...]:
    commit_shas = tuple(
        line.strip()
        for line in run_git(["rev-list", "--reverse", f"{V2736B_AUTHORIZATION_BASE_SHA}..{current_head}"]).splitlines()
        if line.strip()
    )
    previous = V2736B_AUTHORIZATION_BASE_SHA
    facts: list[V2736BCommitFact] = []
    for commit_sha in commit_shas:
        lineage = run_git(["rev-list", "--parents", "-n", "1", commit_sha]).split()
        require(len(lineage) == 2 and lineage[1] == previous, "v27.36b erlaubt nur eine lineare Historie ohne Merge-Commit")
        changed_files = frozenset(
            line.strip().replace("\\", "/")
            for line in run_git(["diff", "--name-only", previous, commit_sha]).splitlines()
            if line.strip()
        )
        require(changed_files, f"Leerer v27.36b-Commit unzulässig: {commit_sha}")
        commit_task = read_v2735f_commit_document(commit_sha, V2735F_TASK_RELATIVE_PATH)
        facts.append(V2736BCommitFact(commit_sha, changed_files, detect_v2736b_task_state_text(commit_task)))
        previous = commit_sha
    return tuple(facts)


def validate_v2736b_history_facts(
    commit_facts: tuple[V2736BCommitFact, ...],
) -> V2736BHistoryState:
    gate_files = frozenset(EXPECTED_CONTROL_FILES)
    roles: list[str] = []
    gate_commits: list[str] = []
    implementation_commit: str | None = None
    closed = False
    for fact in commit_facts:
        files = fact.changed_files
        if files == V2736B_IMPLEMENTATION_FILES:
            require(gate_commits, "v27.36b-IMPLEMENTATION vor Autorisierungs-GATE unzulässig")
            require(implementation_commit is None, "Mehr als ein v27.36b-IMPLEMENTATION-Commit unzulässig")
            require(not closed, "v27.36b-IMPLEMENTATION nach CLOSURE unzulässig")
            require(fact.task_state == V2736B_TASK_AUTHORIZED, "v27.36b-IMPLEMENTATION benötigt AUTHORIZED / Autorisiert JA")
            implementation_commit = fact.commit_sha
            roles.append(V2736B_ROLE_IMPLEMENTATION)
            continue
        require(files.issubset(gate_files), f"Fremde Datei in v27.36b-Commit {fact.commit_sha}: {sorted(files - gate_files)}")
        require(files, f"Leere v27.36b-GATE-Dateimenge: {fact.commit_sha}")
        if fact.task_state == V2736B_TASK_AUTHORIZED:
            require(not closed, "Rückkehr zu v27.36b / AUTHORIZED nach CLOSURE unzulässig")
            gate_commits.append(fact.commit_sha)
            roles.append(V2736B_ROLE_GATE)
            continue
        require(implementation_commit is not None, "v27.36b-CLOSURE vor IMPLEMENTATION unzulässig")
        require(not closed, "Mehr als ein v27.36b-CLOSURE-Commit unzulässig")
        closed = True
        roles.append(V2736B_ROLE_CLOSURE)
    if closed:
        state = V2736B_HISTORY_CLOSED
    elif implementation_commit is not None:
        state = V2736B_HISTORY_IMPLEMENTED
    elif gate_commits:
        state = V2736B_HISTORY_AUTHORIZED
    else:
        state = V2736B_HISTORY_BEFORE_AUTHORIZATION
    return V2736BHistoryState(state, implementation_commit, tuple(roles), tuple(gate_commits))


def read_v2736b_working_tree_fact() -> V2736BWorkingTreeFact:
    head = run_git(["rev-parse", "HEAD"]).strip()
    origin_main = run_git(["rev-parse", "origin/main"]).strip()

    def tracked_at(revision: str) -> frozenset[str]:
        return frozenset(
            line.strip().replace("\\", "/")
            for line in run_git(["ls-tree", "-r", "--name-only", revision, "--", *sorted(V2736B_NEW_IMPLEMENTATION_FILES)]).splitlines()
            if line.strip()
        )

    return V2736BWorkingTreeFact(
        branch=run_git(["branch", "--show-current"]).strip(),
        head=head,
        origin_main=origin_main,
        diff_files=frozenset(line.strip().replace("\\", "/") for line in run_git(["diff", "--name-only"]).splitlines() if line.strip()),
        staged_files=frozenset(line.strip().replace("\\", "/") for line in run_git(["diff", "--cached", "--name-only"]).splitlines() if line.strip()),
        untracked_files=frozenset(line.strip().replace("\\", "/") for line in run_git(["ls-files", "--others", "--exclude-standard"]).splitlines() if line.strip()),
        status_lines=frozenset(line.replace("\\", "/") for line in run_git(["status", "--porcelain=v1", "--untracked-files=all"]).splitlines() if line),
        implementation_files_existing=frozenset(path for path in V2736B_NEW_IMPLEMENTATION_FILES if (ROOT / path).is_file()),
        implementation_files_tracked_at_base=tracked_at(V2736B_AUTHORIZATION_BASE_SHA),
        implementation_files_tracked_at_head=tracked_at(head),
        base_is_head_ancestor=git_is_ancestor(V2736B_AUTHORIZATION_BASE_SHA, head),
        base_is_origin_ancestor=git_is_ancestor(V2736B_AUTHORIZATION_BASE_SHA, origin_main),
        origin_is_head_ancestor=git_is_ancestor(origin_main, head),
    )


def validate_v2736b_working_tree_fact(fact: V2736BWorkingTreeFact) -> None:
    require(fact.branch == "main", "v27.36b-Lebenszyklus muss auf main laufen")
    require(fact.base_is_head_ancestor, "Die stabile v27.36b-Basis ist kein Vorfahr von HEAD")
    require(fact.base_is_origin_ancestor, "Die stabile v27.36b-Basis ist kein Vorfahr von origin/main")
    require(fact.origin_is_head_ancestor, "origin/main ist kein Vorfahr des lokalen v27.36b-HEAD")
    require(not fact.implementation_files_tracked_at_base, "Neue v27.36b-Implementierungsdateien dürfen an der Basis nicht existieren")
    require(not fact.staged_files, "v27.36b-Lebenszyklus darf nichts stagen")


def validate_v2736b_source_contract(
    adapter_text: str,
    checker_text: str,
    report_text: str,
    preflight_text: str,
) -> None:
    for marker in ("session.user.id", "participants", "enrollments", "courses"):
        require(marker in adapter_text, f"v27.36b-Adapterbindung fehlt: {marker}")
    adapter_forbidden = (
        "window.supabase", "globalThis.supabase", "createClient(", "fetch(",
        "XMLHttpRequest", "WebSocket", "http://", "https://", "process.env",
        "Deno.env", "Bun.env", "service_role", "anonKey",
    )
    checker_forbidden = (
        "subprocess", "os.system", "socket", "requests", "urllib", "httpx",
        "fetch(", "http://", "https://", "os.environ",
    )
    for token in adapter_forbidden:
        require(token not in adapter_text, f"v27.36b-Adapter verletzt lokale Sicherheitsgrenze: {token}")
    for token in checker_forbidden:
        require(token not in checker_text, f"v27.36b-Fake-Client-Checker verletzt lokale Sicherheitsgrenze: {token}")
    for marker in (
        "Ziel", "Sicherheitsgrenze", "injizierte Dependencies",
        "kanonische Tabellen-/Spaltenbindung", "Queryreihenfolge",
        "Access-State-Vertrag", "Fail-closed-Regeln", "Fake-Client",
        "getestete Fälle", "ausdrücklich nicht umgesetzte Live-Funktionen",
        "Supabase live: NEIN", "echte Keys: NEIN",
        "echte Teilnehmerdaten: NEIN",
    ):
        require(marker in report_text, f"v27.36b-Umsetzungsbericht fehlt: {marker}")
    require("Fake" in checker_text and "supabase-participant-access-adapter" in checker_text, "Lokaler v27.36b-Fake-Client-Checker ist nicht verbindlich an den Adapter gebunden")
    require("check-supabase-participant-access-adapter.py" in preflight_text, "v27.36b-Checker fehlt im Preflight")
    require("check-project-continuity-control.py" in preflight_text, "Kontinuitäts-Checker darf im Preflight nicht entfernt werden")


def validate_v2736b_local_source_contract() -> None:
    validate_v2736b_source_contract(
        read_required_text(ROOT / "data/supabase-participant-access-adapter.js"),
        read_required_text(ROOT / "tools/check-supabase-participant-access-adapter.py"),
        read_required_text(ROOT / "docs/SUPABASE_PARTICIPANT_ACCESS_ADAPTER_V2736B.md"),
        read_required_text(PREFLIGHT_PATH),
    )


def validate_v2736b_source_contract_at_revision(revision: str) -> None:
    validate_v2736b_source_contract(
        read_v2735f_commit_document(revision, "data/supabase-participant-access-adapter.js"),
        read_v2735f_commit_document(revision, "tools/check-supabase-participant-access-adapter.py"),
        read_v2735f_commit_document(revision, "docs/SUPABASE_PARTICIPANT_ACCESS_ADAPTER_V2736B.md"),
        read_v2735f_commit_document(revision, "tools/preflight.py"),
    )


def validate_v2736b_lifecycle_working_tree(
    history: V2736BHistoryState,
    task_state: str,
    fact: V2736BWorkingTreeFact,
) -> str:
    validate_v2736b_working_tree_fact(fact)
    gate_files = frozenset(EXPECTED_CONTROL_FILES)
    clean = not fact.diff_files and not fact.untracked_files and not fact.status_lines
    if history.state == V2736B_HISTORY_BEFORE_AUTHORIZATION:
        require(fact.head == V2736B_AUTHORIZATION_BASE_SHA, "Phase 1 benötigt die stabile v27.36b-Basis als HEAD")
        require(task_state == V2736B_TASK_AUTHORIZED, "Phase 1 benötigt v27.36b / AUTHORIZED")
        require(fact.diff_files == gate_files, "Phase 1 muss exakt fünf Gate-Dateien ändern")
        require(not fact.untracked_files and fact.status_lines == frozenset(f" M {path}" for path in gate_files), "Working Tree entspricht nicht v27.36b-Phase 1")
        require(not fact.implementation_files_existing, "v27.36b-Implementation vor Autorisierungscommit unzulässig")
        return V2736B_PHASE_1_AUTHORIZATION_PREPARED
    if history.state == V2736B_HISTORY_AUTHORIZED:
        require(fact.head != V2736B_AUTHORIZATION_BASE_SHA, "Phase 2 benötigt mindestens einen GATE-Commit")
        require(task_state == V2736B_TASK_AUTHORIZED, "Phase 2/3 benötigt v27.36b / AUTHORIZED")
        require(not fact.implementation_files_tracked_at_head, "Neue v27.36b-Dateien dürfen vor IMPLEMENTATION nicht getrackt sein")
        if clean:
            require(not fact.implementation_files_existing, "Implementation darf in sauberer Phase 2 nicht lokal existieren")
            return V2736B_PHASE_2_AUTHORIZATION_COMMITTED
        if fact.diff_files and fact.diff_files.issubset(gate_files) and not fact.untracked_files:
            require(fact.status_lines == frozenset(f" M {path}" for path in fact.diff_files), "Lokale v27.36b-Gate-Korrektur enthält fremden Status")
            require(not fact.implementation_files_existing, "Implementation während Gate-Korrektur unzulässig")
            return V2736B_PHASE_2_GATE_PREPARED
        require(fact.diff_files == frozenset({"tools/preflight.py"}), "Phase 3 darf als getrackte Datei nur tools/preflight.py ändern")
        require(fact.untracked_files == V2736B_NEW_IMPLEMENTATION_FILES, "Phase 3 benötigt exakt die drei neuen Implementierungsdateien")
        require(fact.implementation_files_existing == V2736B_NEW_IMPLEMENTATION_FILES, "Phase 3 benötigt alle drei neuen lokalen Dateien")
        expected_status = frozenset({" M tools/preflight.py", *(f"?? {path}" for path in V2736B_NEW_IMPLEMENTATION_FILES)})
        require(fact.status_lines == expected_status, "Working Tree entspricht nicht v27.36b-Phase 3")
        return V2736B_PHASE_3_IMPLEMENTATION_PREPARED
    require(history.implementation_commit is not None, "Phase nach IMPLEMENTATION benötigt den dynamischen Implementierungscommit")
    require(fact.implementation_files_tracked_at_head == V2736B_NEW_IMPLEMENTATION_FILES, "Nach IMPLEMENTATION müssen alle drei neuen Dateien getrackt sein")
    require(fact.implementation_files_existing == V2736B_NEW_IMPLEMENTATION_FILES, "Nach IMPLEMENTATION müssen alle drei neuen Dateien vorhanden sein")
    if history.state == V2736B_HISTORY_IMPLEMENTED:
        if task_state == V2736B_TASK_AUTHORIZED:
            if clean:
                return V2736B_PHASE_4_IMPLEMENTATION_COMMITTED
            require(fact.diff_files and fact.diff_files.issubset(gate_files) and not fact.untracked_files, "Nach IMPLEMENTATION sind lokal nur Gate-Korrekturen oder Closure zulässig")
            require(fact.status_lines == frozenset(f" M {path}" for path in fact.diff_files), "Lokale Phase-4-Gate-Korrektur enthält fremden Status")
            return V2736B_PHASE_4_GATE_PREPARED
        require(task_state == V2736B_TASK_CLOSED, "Phase 5 benötigt den geschlossenen v27.36b-Taskzustand")
        require(fact.diff_files == gate_files and not fact.untracked_files, "Phase 5 muss exakt fünf Gate-Dateien ändern")
        require(fact.status_lines == frozenset(f" M {path}" for path in gate_files), "Working Tree entspricht nicht v27.36b-Phase 5")
        return V2736B_PHASE_5_CLOSURE_PREPARED
    require(history.state == V2736B_HISTORY_CLOSED, "Unbekannter v27.36b-Historienzustand")
    require(task_state == V2736B_TASK_CLOSED, "Nach v27.36b-CLOSURE darf keine Rückkehr zu AUTHORIZED erfolgen")
    require(clean, "Phase 6 benötigt einen sauberen Working Tree")
    return V2736B_PHASE_6_CLOSURE_COMMITTED


def validate_v2736b_committed_closure_documents(
    facts: tuple[V2736BCommitFact, ...],
    history: V2736BHistoryState,
) -> None:
    if V2736B_ROLE_CLOSURE not in history.roles:
        return
    require(history.implementation_commit is not None, "v27.36b-CLOSURE benötigt einen dynamisch erkannten Implementierungscommit")
    for fact, role in zip(facts, history.roles):
        if role == V2736B_ROLE_CLOSURE:
            validate_v2736b_closed_documents(
                read_v2735f_commit_document(fact.commit_sha, "docs/PROJECT_STATE_CURRENT.md"),
                read_v2735f_commit_document(fact.commit_sha, V2735F_TASK_RELATIVE_PATH),
                read_v2735f_commit_document(fact.commit_sha, "docs/CURSOR_MASTER_CONTEXT_ACCAOUI.md"),
                read_v2735f_commit_document(fact.commit_sha, "docs/PROJECT_MASTERLIST.md"),
                history.implementation_commit,
            )


def validate_v2736b_lifecycle(
    state_text: str,
    task_text: str,
    cursor_text: str,
    masterlist_text: str,
) -> tuple[str, V2736BHistoryState, V2736BWorkingTreeFact]:
    fact = read_v2736b_working_tree_fact()
    validate_v2736b_working_tree_fact(fact)
    commit_facts = read_v2736b_commit_facts(fact.head)
    history = validate_v2736b_history_facts(commit_facts)
    validate_v2736b_committed_closure_documents(commit_facts, history)
    task_state = detect_v2736b_task_state_text(task_text)
    if task_state == V2736B_TASK_AUTHORIZED:
        validate_v2736b_state_text(state_text)
        validate_v2736b_task_text(task_text)
        validate_v2736b_cursor_text(cursor_text)
        validate_v2736b_masterlist_text(masterlist_text)
    else:
        require(history.implementation_commit is not None, "v27.36b-Abschluss vor IMPLEMENTATION unzulässig")
        validate_v2736b_closed_documents(
            state_text,
            task_text,
            cursor_text,
            masterlist_text,
            history.implementation_commit,
        )
    phase = validate_v2736b_lifecycle_working_tree(history, task_state, fact)
    if phase == V2736B_PHASE_3_IMPLEMENTATION_PREPARED:
        validate_v2736b_local_source_contract()
    if history.implementation_commit is not None:
        validate_v2736b_source_contract_at_revision(history.implementation_commit)
    return phase, history, fact


def run_v2736b_manipulation_matrix(
    state_text: str,
    task_text: str,
    cursor_text: str,
    masterlist_text: str,
    current_history: V2736BHistoryState,
    current_fact: V2736BWorkingTreeFact,
) -> tuple[int, int, int]:
    checks = 0
    current_task_state = detect_v2736b_task_state_text(task_text)
    if current_task_state == V2736B_TASK_AUTHORIZED:
        for text, validator, fields, name in (
            (state_text, validate_v2736b_state_text, V2736B_EXPECTED_STATE_FIELDS, "PROJECT_STATE_CURRENT"),
            (task_text, validate_v2736b_task_text, V2736B_EXPECTED_TASK_FIELDS, "CURRENT_TASK"),
        ):
            for field, value in fields.items():
                manipulated = changed_once(text, f"{field}: {value}", f"{field}: MANIPULIERT", f"{name} / {field}")
                must_reject(validator, manipulated, f"{name}: manipuliertes Feld {field}")
                checks += 1
        for text, validator, markers, name in (
            (state_text, validate_v2736b_state_text, V2736B_STATE_MARKERS, "PROJECT_STATE_CURRENT"),
            (task_text, validate_v2736b_task_text, V2736B_TASK_MARKERS, "CURRENT_TASK"),
            (cursor_text, validate_v2736b_cursor_text, V2736B_CURSOR_MARKERS, "CURSOR_MASTER_CONTEXT_ACCAOUI"),
            (masterlist_text, validate_v2736b_masterlist_text, V2736B_MASTERLIST_MARKERS, "PROJECT_MASTERLIST"),
        ):
            for marker in markers:
                require(marker in text, f"Manipulationsmatrix kann v27.36b-Pflichtaussage nicht finden: {name} / {marker}")
                must_reject(validator, text.replace(marker, ""), f"{name}: v27.36b-Pflichtaussage entfernt: {marker}")
                checks += 1
        must_reject(
            validate_v2736b_task_text,
            task_text.replace("## Abgeschlossener Dokumentations-/Bestandsaudit v27.36a", "Zukünftiger Commit: `aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa`\n\n## Abgeschlossener Dokumentations-/Bestandsaudit v27.36a", 1),
            "zukünftige IMPLEMENTATION-/Closure-SHA hartcodiert",
        )
        checks += 1
        must_reject(
            validate_v2736b_task_text,
            task_text.replace("Kein Folgetask\nnach v27.36b", "v27.36c / AUTHORIZED\n\nKein Folgetask\nnach v27.36b", 1),
            "automatischer Folgetask v27.36c",
        )
        checks += 1
    else:
        require(current_history.implementation_commit is not None, "v27.36b-Closure-Matrix benötigt den dynamischen Implementierungscommit")
        closed_documents = (state_text, task_text, cursor_text, masterlist_text)

        def validate_closed_mutation(document_index: int, manipulated_text: str) -> None:
            documents = list(closed_documents)
            documents[document_index] = manipulated_text
            validate_v2736b_closed_documents(
                documents[0],
                documents[1],
                documents[2],
                documents[3],
                current_history.implementation_commit,
            )

        closure_boundaries = (
            ("## Abgeschlossener isolierter Technikschritt v27.36b", "## Abgeschlossener Dokumentations-/Bestandsaudit v27.36a"),
            ("## Abgeschlossener isolierter Technikschritt v27.36b", "## Abgeschlossener Dokumentations-/Bestandsaudit v27.36a"),
            ("## 14. Nächster sinnvoller Schritt", "## 15. Wenn ein neuer Chat beginnt"),
            ("## 14. Nächste sinnvolle Aufgaben", "## 15. Start in neuem Chat"),
        )

        def replaced_in_closure(document_index: int, text: str, marker: str, replacement: str, label: str) -> str:
            start_marker, end_marker = closure_boundaries[document_index]
            start_index = text.find(start_marker)
            end_index = text.find(end_marker, start_index + len(start_marker))
            require(start_index >= 0 and end_index > start_index, f"Manipulationsmatrix kann v27.36b-Closure-Abschnitt nicht finden: {label}")
            marker_index = text.find(marker, start_index, end_index)
            require(marker_index >= 0, f"Manipulationsmatrix kann v27.36b-Closure-Wert nicht finden: {label}")
            return text[:marker_index] + replacement + text[marker_index + len(marker):]

        for document_index, text, fields, name in (
            (0, state_text, V2736B_CLOSED_STATE_FIELDS, "PROJECT_STATE_CURRENT"),
            (1, task_text, V2736B_CLOSED_TASK_FIELDS, "CURRENT_TASK"),
        ):
            for field, value in fields.items():
                manipulated = changed_once(text, f"{field}: {value}", f"{field}: MANIPULIERT", f"{name} / {field}")
                must_reject(
                    lambda changed, index=document_index: validate_closed_mutation(index, changed),
                    manipulated,
                    f"{name}: manipuliertes Closure-Feld {field}",
                )
                checks += 1
        implementation_marker = f"Implementierungscommit: `{current_history.implementation_commit}`"
        for document_index, text, name in (
            (0, state_text, "PROJECT_STATE_CURRENT"),
            (1, task_text, "CURRENT_TASK"),
            (2, cursor_text, "CURSOR_MASTER_CONTEXT_ACCAOUI"),
            (3, masterlist_text, "PROJECT_MASTERLIST"),
        ):
            for marker in (*V2736B_CLOSURE_MARKERS, implementation_marker):
                require(marker in text, f"Manipulationsmatrix kann v27.36b-Closure-Aussage nicht finden: {name} / {marker}")
                must_reject(
                    lambda changed, index=document_index: validate_closed_mutation(index, changed),
                    replaced_in_closure(document_index, text, marker, "", f"{name} / {marker}"),
                    f"{name}: v27.36b-Closure-Aussage entfernt: {marker}",
                )
                checks += 1
            for path in V2736B_IMPLEMENTATION_FILES:
                marker = f"`{path}`"
                must_reject(
                    lambda changed, index=document_index: validate_closed_mutation(index, changed),
                    replaced_in_closure(document_index, text, marker, "", f"{name} / {path}"),
                    f"{name}: v27.36b-Implementierungsdatei entfernt: {path}",
                )
                checks += 1
        must_reject(
            lambda changed: validate_closed_mutation(1, changed),
            task_text.replace(
                "## Abgeschlossener Dokumentations-/Bestandsaudit v27.36a",
                "Zukünftiger Closure-Commit: `aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa`\n\n## Abgeschlossener Dokumentations-/Bestandsaudit v27.36a",
                1,
            ),
            "zukünftige Closure-SHA hartcodiert",
        )
        checks += 1
        must_reject(
            lambda changed: validate_closed_mutation(1, changed),
            replaced_in_closure(
                1,
                task_text,
                "Kein Folgetask wurde ausgewählt oder autorisiert.",
                "v27.36c / AUTHORIZED",
                "CURRENT_TASK / Folgetask",
            ),
            "automatischer Folgetask v27.36c nach Closure",
        )
        checks += 1

    gate = V2736BCommitFact("1" * 40, frozenset({EXPECTED_CONTROL_FILES[0]}), V2736B_TASK_AUTHORIZED)
    implementation = V2736BCommitFact("2" * 40, V2736B_IMPLEMENTATION_FILES, V2736B_TASK_AUTHORIZED)
    closure = V2736BCommitFact("3" * 40, frozenset({EXPECTED_CONTROL_FILES[1]}), V2736B_TASK_CLOSED)
    histories = (
        validate_v2736b_history_facts(tuple()),
        validate_v2736b_history_facts((gate,)),
        validate_v2736b_history_facts((gate, implementation)),
        validate_v2736b_history_facts((gate, implementation, closure)),
    )
    clean_fact = replace(
        current_fact,
        head="1" * 40,
        diff_files=frozenset(), staged_files=frozenset(), untracked_files=frozenset(), status_lines=frozenset(),
        implementation_files_existing=frozenset(),
        implementation_files_tracked_at_base=frozenset(),
        implementation_files_tracked_at_head=frozenset(),
        base_is_head_ancestor=True, base_is_origin_ancestor=True, origin_is_head_ancestor=True,
    )
    gate_files = frozenset(EXPECTED_CONTROL_FILES)
    implemented_fact = replace(
        clean_fact,
        head="2" * 40,
        implementation_files_existing=V2736B_NEW_IMPLEMENTATION_FILES,
        implementation_files_tracked_at_head=V2736B_NEW_IMPLEMENTATION_FILES,
    )
    phase_fixtures = (
        (histories[0], V2736B_TASK_AUTHORIZED, replace(clean_fact, head=V2736B_AUTHORIZATION_BASE_SHA, diff_files=gate_files, status_lines=frozenset(f" M {p}" for p in gate_files)), V2736B_PHASE_1_AUTHORIZATION_PREPARED),
        (histories[1], V2736B_TASK_AUTHORIZED, clean_fact, V2736B_PHASE_2_AUTHORIZATION_COMMITTED),
        (histories[1], V2736B_TASK_AUTHORIZED, replace(clean_fact, diff_files=frozenset({EXPECTED_CONTROL_FILES[0]}), status_lines=frozenset({f" M {EXPECTED_CONTROL_FILES[0]}"})), V2736B_PHASE_2_GATE_PREPARED),
        (histories[1], V2736B_TASK_AUTHORIZED, replace(clean_fact, diff_files=frozenset({"tools/preflight.py"}), untracked_files=V2736B_NEW_IMPLEMENTATION_FILES, status_lines=frozenset({" M tools/preflight.py", *(f"?? {p}" for p in V2736B_NEW_IMPLEMENTATION_FILES)}), implementation_files_existing=V2736B_NEW_IMPLEMENTATION_FILES), V2736B_PHASE_3_IMPLEMENTATION_PREPARED),
        (histories[2], V2736B_TASK_AUTHORIZED, implemented_fact, V2736B_PHASE_4_IMPLEMENTATION_COMMITTED),
        (histories[2], V2736B_TASK_CLOSED, replace(implemented_fact, diff_files=gate_files, status_lines=frozenset(f" M {p}" for p in gate_files)), V2736B_PHASE_5_CLOSURE_PREPARED),
        (histories[3], V2736B_TASK_CLOSED, implemented_fact, V2736B_PHASE_6_CLOSURE_COMMITTED),
    )
    for history, task_state, fact, expected in phase_fixtures:
        require(validate_v2736b_lifecycle_working_tree(history, task_state, fact) == expected, f"v27.36b-Positivsimulation fehlgeschlagen: {expected}")
    positive_tests = len(phase_fixtures)

    bad_histories = (
        ((implementation,), "Implementation vor Autorisierung"),
        ((gate, implementation, implementation), "zweite Implementation"),
        ((V2736BCommitFact("4" * 40, frozenset({"app.js"}), V2736B_TASK_AUTHORIZED),), "App-Datei"),
        ((V2736BCommitFact("5" * 40, frozenset({"index.html"}), V2736B_TASK_AUTHORIZED),), "UI-Datei"),
        ((V2736BCommitFact("6" * 40, frozenset({"data/supabase-client-adapter.js"}), V2736B_TASK_AUTHORIZED),), "zentraler Adapter"),
        ((V2736BCommitFact("7" * 40, frozenset({"data/supabase-client-bootstrap.js"}), V2736B_TASK_AUTHORIZED),), "Bootstrap"),
        ((V2736BCommitFact("8" * 40, frozenset({"data/supabase-config.js"}), V2736B_TASK_AUTHORIZED),), "Config"),
        ((V2736BCommitFact("9" * 40, frozenset({"supabase/migrations/unsafe.sql"}), V2736B_TASK_AUTHORIZED),), "Migration/SQL"),
        ((gate, closure), "Closure vor Implementation"),
        ((gate, implementation, closure, gate), "Rückkehr nach Closure"),
        ((gate, implementation, closure, closure), "zweite Closure"),
        ((gate, V2736BCommitFact("a" * 40, frozenset(set(V2736B_IMPLEMENTATION_FILES) - {"tools/preflight.py"}), V2736B_TASK_AUTHORIZED)), "partielle Implementation"),
        ((gate, V2736BCommitFact("b" * 40, V2736B_IMPLEMENTATION_FILES | {"app.js"}, V2736B_TASK_AUTHORIZED)), "Implementation mit Zusatzdatei"),
    )
    for facts, label in bad_histories:
        try:
            validate_v2736b_history_facts(facts)
        except ValidationError:
            checks += 1
            continue
        raise ValidationError(f"v27.36b-Historienmanipulation wurde nicht blockiert: {label}")

    bad_working = (
        (current_history, V2736B_TASK_AUTHORIZED, replace(current_fact, staged_files=frozenset({EXPECTED_CONTROL_FILES[0]})), "gestagte Datei"),
        (current_history, V2736B_TASK_AUTHORIZED, replace(current_fact, diff_files=current_fact.diff_files | {"app.js"}, status_lines=current_fact.status_lines | {" M app.js"}), "App-Datei lokal"),
        (current_history, V2736B_TASK_AUTHORIZED, replace(current_fact, untracked_files={"unexpected.txt"}, status_lines=current_fact.status_lines | {"?? unexpected.txt"}), "fremde ungetrackte Datei"),
        (current_history, V2736B_TASK_AUTHORIZED, replace(current_fact, base_is_head_ancestor=False), "falsche Basis"),
        (current_history, V2736B_TASK_AUTHORIZED, replace(current_fact, origin_is_head_ancestor=False), "origin nicht Vorfahr"),
        (current_history, V2736B_TASK_AUTHORIZED, replace(current_fact, implementation_files_tracked_at_base=V2736B_NEW_IMPLEMENTATION_FILES), "Implementierungsdateien bereits an Basis"),
        (histories[0], V2736B_TASK_AUTHORIZED, replace(clean_fact, head=V2736B_AUTHORIZATION_BASE_SHA, untracked_files=V2736B_NEW_IMPLEMENTATION_FILES, status_lines=frozenset(f"?? {p}" for p in V2736B_NEW_IMPLEMENTATION_FILES), implementation_files_existing=V2736B_NEW_IMPLEMENTATION_FILES), "Implementation lokal vor Autorisierung"),
        (histories[1], V2736B_TASK_CLOSED, replace(clean_fact, diff_files=gate_files, status_lines=frozenset(f" M {p}" for p in gate_files)), "Closure lokal vor Implementation"),
        (histories[3], V2736B_TASK_AUTHORIZED, implemented_fact, "Rückkehr zu AUTHORIZED nach Closure"),
    )
    for history, task_state, fact, label in bad_working:
        try:
            validate_v2736b_lifecycle_working_tree(history, task_state, fact)
        except ValidationError:
            checks += 1
            continue
        raise ValidationError(f"v27.36b-Working-Tree-Manipulation wurde nicht blockiert: {label}")

    valid_adapter = "session.user.id participants enrollments courses"
    valid_checker = "Fake supabase-participant-access-adapter"
    valid_report = "\n".join((
        "Ziel", "Sicherheitsgrenze", "injizierte Dependencies",
        "kanonische Tabellen-/Spaltenbindung", "Queryreihenfolge",
        "Access-State-Vertrag", "Fail-closed-Regeln", "Fake-Client",
        "getestete Fälle", "ausdrücklich nicht umgesetzte Live-Funktionen",
        "Supabase live: NEIN", "echte Keys: NEIN", "echte Teilnehmerdaten: NEIN",
    ))
    valid_preflight = "check-project-continuity-control.py check-supabase-participant-access-adapter.py"
    validate_v2736b_source_contract(valid_adapter, valid_checker, valid_report, valid_preflight)
    source_manipulations = (
        (valid_adapter + " fetch(", valid_checker, valid_report, valid_preflight, "Netzwerk im Adapter"),
        (valid_adapter + " createClient(", valid_checker, valid_report, valid_preflight, "echter Client"),
        (valid_adapter, valid_checker + " subprocess", valid_report, valid_preflight, "Prozess im Fake-Checker"),
        (valid_adapter, valid_checker, valid_report.replace("Fail-closed-Regeln", ""), valid_preflight, "Fail-closed-Bericht entfernt"),
        (valid_adapter, valid_checker, valid_report, "check-project-continuity-control.py", "neuer Checker nicht im Preflight"),
        (valid_adapter, valid_checker, valid_report, "check-supabase-participant-access-adapter.py", "Kontinuitäts-Checker aus Preflight entfernt"),
    )
    for adapter, checker, report, preflight, label in source_manipulations:
        try:
            validate_v2736b_source_contract(adapter, checker, report, preflight)
        except ValidationError:
            checks += 1
            continue
        raise ValidationError(f"v27.36b-Sicherheitsmanipulation wurde nicht blockiert: {label}")
    negative_tests = len(bad_histories) + len(bad_working) + len(source_manipulations) + 2
    return checks, positive_tests, negative_tests


V2736C_AUTHORIZATION_BASE_SHA = "d28f3710d6f3e4b9abc427dec8589d3ea98c09be"
V2736C_TITLE = "Lokale Teilnehmerzugangs-Brücke zum bestehenden Supabase-Bootstrap-Pfad vorbereiten"
V2736C_IMPLEMENTATION_FILES = frozenset(
    {
        "data/supabase-participant-access-bootstrap-bridge.js",
        "tools/check-supabase-participant-access-bootstrap-bridge.py",
        "docs/SUPABASE_PARTICIPANT_ACCESS_BOOTSTRAP_BRIDGE_V2736C.md",
        "tools/preflight.py",
    }
)
V2736C_NEW_IMPLEMENTATION_FILES = frozenset(V2736C_IMPLEMENTATION_FILES - {"tools/preflight.py"})
V2736C_ALLOWED_FILES_VALUE = (
    "`data/supabase-participant-access-bootstrap-bridge.js`, "
    "`tools/check-supabase-participant-access-bootstrap-bridge.py`, "
    "`docs/SUPABASE_PARTICIPANT_ACCESS_BOOTSTRAP_BRIDGE_V2736C.md`, "
    "`tools/preflight.py`"
)
V2736C_EXPECTED_STATE_FIELDS = {
    "Stand": "v27.36c",
    "Repository": "`asarrad-bit/accaoui-34a-lernapp`",
    "Branch": "`main`",
    "Letzter abgeschlossener funktionaler Stand": "v27.35g",
    "Abschlusscommit": f"`{V2735G_COMPLETION_SHA}`",
    "Aktueller HEAD": "DYNAMISCH ZU PRÜFEN",
    "Funktionsstatus": "v27.35g abgeschlossen",
    "Weiterer funktionaler Schritt autorisiert": "JA",
    "Aktuell autorisierter Task": "v27.36c",
    "Aktuelle Taskart": "Lokale Teilnehmerzugangs-Brücke",
    "Aktueller Blocker": (
        "KEINER für die ausdrücklich autorisierte spätere v27.36c-Umsetzung; "
        "in diesem Autorisierungsschritt erfolgt noch keine Implementierung"
    ),
}
V2736C_EXPECTED_TASK_FIELDS = {
    "Task-ID": "v27.36c",
    "Status": "AUTHORIZED",
    "Autorisiert": "JA",
    "Titel": V2736C_TITLE,
    "Funktionaler Ausgangsstand": "v27.35g",
    "Erwarteter Ausgangscommit": f"`{V2736C_AUTHORIZATION_BASE_SHA}`",
    "Erlaubte Dateien": V2736C_ALLOWED_FILES_VALUE,
    "Commit erlaubt": "NEIN",
    "Push erlaubt": "NEIN",
}
V2736C_CLOSED_STATE_FIELDS = {
    "Stand": "v27.36c",
    "Repository": "`asarrad-bit/accaoui-34a-lernapp`",
    "Branch": "`main`",
    "Letzter abgeschlossener funktionaler Stand": "v27.35g",
    "Abschlusscommit": f"`{V2735G_COMPLETION_SHA}`",
    "Aktueller HEAD": "DYNAMISCH ZU PRÜFEN",
    "Funktionsstatus": "v27.35g abgeschlossen",
    "Weiterer funktionaler Schritt autorisiert": "NEIN",
    "Aktuell autorisierter Task": "NONE",
    "Aktuelle Taskart": "Kein Task autorisiert",
    "Aktueller Blocker": (
        "Neue Taskauswahl und ausdrückliche Autorisierung durch "
        "Projekteigentümer und verbindlichen Projektchat"
    ),
}
V2736C_CLOSED_TASK_FIELDS = {
    "Task-ID": "NONE",
    "Status": "BLOCKED",
    "Autorisiert": "NEIN",
    "Titel": "Kein Task autorisiert",
    "Funktionaler Ausgangsstand": "v27.35g",
    "Letzter abgeschlossener Kontrollschritt": "v27.36c",
    "Erlaubte Dateien": "KEINE",
    "Commit erlaubt": "NEIN",
    "Push erlaubt": "NEIN",
}
V2736C_STATE_MARKERS = (
    "## Autorisierter Task v27.36c",
    "v27.36b ist vollständig abgeschlossen.",
    "Der einzige autorisierte Task ist v27.36c:",
    "Dieser Autorisierungsschritt autorisiert v27.36c nur.",
    "Für die spätere Umsetzung sind genau vier Dateien erlaubt:",
    "`bootstrap.getClient()`",
    "fehlendem oder werfendem `getClient()`-Pfad",
    "nicht\nmit duplizierter Fachlogik",
    "`initializeClient()`, `createClient()`",
    "`getState()` als Voraussetzung",
    "Bootstrap-, Config-, SDK- oder\nLive-State-Schalter",
    "`data/supabase-client-bootstrap.js`, `data/supabase-client-adapter.js` und",
    "Kein Folgetask nach v27.36c wurde ausgewählt oder autorisiert.",
    "### Permanenter v27.36c-Lebenszyklus",
    "Der Lifecycle erkennt dynamisch sechs Phasen",
    "Rückkehr zu v27.36c / AUTHORIZED nach abgeschlossener Closure",
)
V2736C_TASK_MARKERS = (
    "## Autorisierter Task v27.36c",
    "Dieser Codex-Schritt autorisiert v27.36c nur.",
    "## Verbindliches Funktionsziel",
    "bootstrap-kompatiblen Provider",
    "Factory des bestehenden v27.36b-Teilnehmerzugangs-Adapters",
    "`bootstrap.getClient()`",
    "## Fail-closed Brückenverhalten",
    "fehlendem oder werfendem `getClient()`-Pfad",
    "nicht durch duplizierte\nFachlogik der Brücke bewertet",
    "## Lokaler Fake-Bootstrap und Testgrenze",
    "## Ausdrücklich verboten",
    "`initializeClient()` oder `createClient()`",
    "`getState()` als Voraussetzung der Brücke",
    "Bootstrap-, Config-, SDK- oder Live-State-Schalter",
    "Kein Folgetask nach v27.36c wurde ausgewählt oder",
    "## Permanenter v27.36c-Lebenszyklus",
    "Sechs Phasen werden dynamisch erkannt:",
    "Rückkehr aus abgeschlossener v27.36c-Closure",
)
V2736C_CURSOR_MARKERS = (
    "v27.36b abgeschlossen.",
    "Closure-HEAD: `d28f3710d6f3e4b9abc427dec8589d3ea98c09be`.",
    "`CURRENT_TASK` ist `v27.36c` / `AUTHORIZED` / `Autorisiert: JA`.",
    "Einziger autorisierter Task:",
    "keine Brücke implementiert",
    "`bootstrap.getClient()`",
    "fehlendem oder werfendem `getClient()`-Pfad",
    "nicht\nmit duplizierter Fachlogik",
    "`getState()`\nals Voraussetzung",
    "Bootstrap, zentraler Adapter und v27.36b-Teilnehmerzugangs-Adapter bleiben",
    "Kein Folgetask nach v27.36c wurde ausgewählt oder autorisiert.",
    "### Permanenter v27.36c-Lebenszyklus",
    "Der Lifecycle erkennt sechs Phasen dynamisch",
    "Rückkehr aus der abgeschlossenen v27.36c-Closure",
)
V2736C_MASTERLIST_ROW_PREFIX = "| v27.36c | Lokale Teilnehmerzugangs-Brücke"
V2736C_MASTERLIST_MARKERS = (
    "v27.36b abgeschlossen.",
    "Closure-HEAD: `d28f3710d6f3e4b9abc427dec8589d3ea98c09be`.",
    "`CURRENT_TASK` ist aktuell `v27.36c` / `AUTHORIZED` / `Autorisiert: JA`.",
    "v27.36c ist der einzige autorisierte Task.",
    "keine Brücke implementiert",
    "`bootstrap.getClient()`",
    "fehlender oder werfender `getClient()`-Pfad",
    "nicht durch duplizierte\nFachlogik der Brücke bewertet",
    "`getState()`\nals Brückenvoraussetzung",
    "Bootstrap, zentraler Adapter und v27.36b-Teilnehmerzugangs-Adapter bleiben",
    "Kein Folgetask nach v27.36c wurde ausgewählt oder autorisiert.",
    "### Permanenter v27.36c-Lebenszyklus",
    "Der Lifecycle erkennt sechs Phasen dynamisch",
    "Rückkehr aus abgeschlossener v27.36c-Closure",
)
V2736C_PERMANENT_MASTERLIST_MODE_MARKERS = (
    "### Arbeits-, Produkt- und Übergabemodus",
    "Projekteigentümer/Product Owner ist fachlicher Entscheider",
    "§34a-Fachexperte",
    "technische Führung umfasst Architektur, technische Beratung",
    "Produktberatung, Konkurrenzanalyse und die kritische Nutzerperspektive",
    "Teilnehmer-,\n  Lernwirkungs-, Konkurrenz-, UX-, Technik- und Geschäftsperspektive",
    "Bei relevanten Produktentscheidungen wird die Konkurrenz aktuell geprüft",
    "fremde Inhalte oder Versprechen werden nicht kopiert",
    "Ziel ist die bestmögliche §34a-Lern-App",
    "echten Lernerfolg\n  oder Produktnutzen erzeugen",
    "`READ-ONLY` bedeutet Analyse ohne Dateiänderung",
    "`IMPLEMENTATION` bedeutet ausschließlich die Umsetzung des exakt",
    "autorisierten `CURRENT_TASK`",
    "`CHECKPOINT` bedeutet prüfen; Commit und Push erfolgen nur nach Freigabe",
    "anschließend auf GitHub verifiziert",
    "keine offenen\n  lokalen Änderungen zurückbleiben",
    "sichere GitHub-Checkpoints sind zu\n  bevorzugen",
    "GitHub ist die technische Wahrheit für den gemeinsamen synchronisierten",
    "`PROJECT_MASTERLIST.md` ist die dauerhafte Projektchronik",
    "Entscheidungen, Architektur, Regeln, Erkenntnisse und\n  abgeschlossene Schritte",
    "`CURRENT_TASK.md` bleibt die einzige konkrete Implementierungsfreigabe",
    "überlangen oder langsamen Chat",
    "HEAD, Task, Phase, Dateien, Tests und nächstem Schritt",
    "kürzesten\n  sinnvollen Weg zu einem nutzbaren, konkurrenzfähigen Produkt",
    "nicht unnötig mit internen Implementierungsdetails belastet",
    "technische Entscheidungen werden fachlich verständlich erklärt",
    "### Commit-/Push-Freigabe bei autorisierten Lifecycle-Schritten",
    "bereits fachlich autorisierten IMPLEMENTATION- oder CLOSURE-Schritt",
    "keine zusätzliche Nutzerfreigabe nur für Commit/Push erforderlich",
    "technische Lead darf Commit und Push für einen solchen Schritt auslösen oder empfehlen",
    "alle verbindlichen Checker PASS",
    "der Preflight PASS",
    "`git diff --check` PASS",
    "keine unerwarteten Änderungen",
    "keine offene Sicherheits- oder Architekturabweichung",
    "Bei jeder Abweichung gilt sofort STOPP.",
    "Diese Regel ersetzt nicht die fachliche Autorisierung eines neuen Tasks.",
    "Nach einer Closure bleibt jede neue Implementierung vollständig BLOCKED",
)
V2736C_CLOSURE_MARKERS = (
    "v27.36c abgeschlossen.",
    "Der letzte abgeschlossene funktionale Stand bleibt v27.35g.",
    "Bootstrap, zentraler Adapter und v27.36b-Teilnehmerzugangs-Adapter bleiben unverändert.",
    "Keine echten Keys.",
    "Keine echten Teilnehmerdaten.",
    "Kein Folgetask wurde ausgewählt oder autorisiert.",
    "vollständig BLOCKED, bis sie ausdrücklich autorisiert wird.",
    "Keine zukünftige Closure-SHA wird hartcodiert.",
    "Rückkehr zu einem autorisierten v27.36c-Zustand bleibt ohne neue ausdrückliche Autorisierung blockiert.",
)
V2736C_SUPABASE_NOT_LIVE_PATTERN = re.compile(
    r"Supabase\s+bleibt\s+NICHT\s+LIVE\."
)
V2736C_TASK_AUTHORIZED = "authorized"
V2736C_TASK_CLOSED = "closed"
V2736C_HISTORY_BEFORE_AUTHORIZATION = "before_authorization_commit"
V2736C_HISTORY_AUTHORIZED = "authorization_committed"
V2736C_HISTORY_IMPLEMENTED = "implementation_committed"
V2736C_HISTORY_CLOSED = "closure_committed"
V2736C_PHASE_AUTHORIZATION_PREPARED = "authorization_prepared"
V2736C_PHASE_AUTHORIZATION_COMMITTED = "authorization_committed"
V2736C_PHASE_IMPLEMENTATION_PREPARED = "implementation_prepared"
V2736C_PHASE_IMPLEMENTATION_COMMITTED = "implementation_committed"
V2736C_PHASE_CLOSURE_PREPARED = "closure_prepared"
V2736C_PHASE_CLOSURE_COMMITTED = "closure_committed"
V2736C_ROLE_GATE = "GATE"
V2736C_ROLE_IMPLEMENTATION = "IMPLEMENTATION"
V2736C_ROLE_CLOSURE = "CLOSURE"


@dataclass(frozen=True)
class V2736CCommitFact:
    commit_sha: str
    changed_files: frozenset[str]
    task_state: str


@dataclass(frozen=True)
class V2736CHistoryState:
    state: str
    implementation_commit: str | None
    roles: tuple[str, ...]
    gate_commits: tuple[str, ...]


@dataclass(frozen=True)
class V2736CWorkingTreeFact:
    branch: str
    head: str
    origin_main: str
    diff_files: frozenset[str]
    staged_files: frozenset[str]
    untracked_files: frozenset[str]
    status_lines: frozenset[str]
    implementation_files_existing: frozenset[str]
    implementation_files_tracked_at_base: frozenset[str]
    implementation_files_tracked_at_head: frozenset[str]
    base_is_head_ancestor: bool
    base_is_origin_ancestor: bool
    origin_is_head_ancestor: bool


def validate_no_future_v2736c_sha(
    section: str,
    allowed_shas: frozenset[str],
    document_name: str,
) -> None:
    shas = frozenset(re.findall(r"\b[0-9a-f]{40}\b", section))
    require(
        shas.issubset(allowed_shas),
        f"{document_name}: zukünftige v27.36c-Commit-SHA hartcodiert: {sorted(shas - allowed_shas)}",
    )
    require(
        re.search(r"\bv27\.(?:36[d-z]|3[7-9])\b", section, re.IGNORECASE) is None,
        f"{document_name}: automatischer Folgetask nach v27.36c unzulässig",
    )


def validate_v2736c_supabase_not_live_statement(text: str) -> None:
    require(
        V2736C_SUPABASE_NOT_LIVE_PATTERN.search(text) is not None,
        "v27.36c-Pflichtaussage fehlt oder wurde verändert: Supabase bleibt NICHT LIVE.",
    )


def validate_v2736c_permanent_masterlist_contract(text: str) -> None:
    require(
        exact_field(text, "Arbeits-Laptop")
        == f"`{V2736C_VERIFIED_WORK_PATH}`",
        "PROJECT_MASTERLIST: verifizierter Arbeits-Laptop-Pfad fehlt",
    )
    require(
        exact_field(text, "Git Bash Arbeits-Laptop")
        == f"`{V2736C_VERIFIED_WORK_PATH_GIT_BASH}`",
        "PROJECT_MASTERLIST: verifizierter Git-Bash-Arbeits-Laptop-Pfad fehlt",
    )
    require(
        text.count("### Arbeits-, Produkt- und Übergabemodus") == 1,
        "PROJECT_MASTERLIST: Arbeits-, Produkt- und Übergabemodus muss exakt einmal vorkommen",
    )
    require(
        text.count("### Commit-/Push-Freigabe bei autorisierten Lifecycle-Schritten") == 1,
        "PROJECT_MASTERLIST: Commit-/Push-Freigaberegel muss exakt einmal vorkommen",
    )
    validate_required_markers(
        text,
        V2736C_PERMANENT_MASTERLIST_MODE_MARKERS,
        "PROJECT_MASTERLIST / Arbeits-, Produkt- und Übergabemodus",
    )


def validate_v2736c_state_text(text: str) -> None:
    validate_exact_fields(text, V2736C_EXPECTED_STATE_FIELDS)
    section = section_between(
        text,
        "## Autorisierter Task v27.36c",
        "## Abgeschlossener isolierter Technikschritt v27.36b",
        "PROJECT_STATE_CURRENT",
    )
    validate_required_markers(section, V2736C_STATE_MARKERS, "PROJECT_STATE_CURRENT / v27.36c")
    validate_v2736c_supabase_not_live_statement(section)
    validate_no_future_v2736c_sha(section, frozenset({V2736C_AUTHORIZATION_BASE_SHA}), "PROJECT_STATE_CURRENT / v27.36c")
    for path in V2736C_IMPLEMENTATION_FILES:
        require(section.count(f"`{path}`") == 1, f"PROJECT_STATE_CURRENT: v27.36c-Datei fehlt oder ist doppelt: {path}")


def validate_v2736c_task_text(text: str) -> None:
    validate_exact_fields(text, V2736C_EXPECTED_TASK_FIELDS)
    require(
        text.count(f"Erlaubte Dateien: {V2736C_ALLOWED_FILES_VALUE}") == 1,
        "CURRENT_TASK muss exakt eine verbindliche v27.36c-Dateifreigabe enthalten",
    )
    section = section_between(
        text,
        "## Autorisierter Task v27.36c",
        "## Abgeschlossener isolierter Technikschritt v27.36b",
        "CURRENT_TASK",
    )
    validate_required_markers(section, V2736C_TASK_MARKERS, "CURRENT_TASK / v27.36c")
    validate_v2736c_supabase_not_live_statement(section)
    validate_no_future_v2736c_sha(section, frozenset({V2736C_AUTHORIZATION_BASE_SHA}), "CURRENT_TASK / v27.36c")
    for path in V2736C_IMPLEMENTATION_FILES:
        require(section.count(f"`{path}`") >= 1, f"CURRENT_TASK: v27.36c-Datei fehlt: {path}")


def validate_v2736c_cursor_text(text: str) -> None:
    require(exact_field(text, "Stand") == "v27.36c", "CURSOR-Kontext muss auf v27.36c stehen")
    validate_project_paths(text, "CURSOR_MASTER_CONTEXT_ACCAOUI")
    section = section_between(text, "## 14. Nächster sinnvoller Schritt", "## 15. Wenn ein neuer Chat beginnt", "CURSOR_MASTER_CONTEXT_ACCAOUI")
    validate_required_markers(section, V2736C_CURSOR_MARKERS, "CURSOR_MASTER_CONTEXT_ACCAOUI / v27.36c")
    validate_v2736c_supabase_not_live_statement(section)
    validate_no_future_v2736c_sha(section, frozenset({V2736C_AUTHORIZATION_BASE_SHA}), "CURSOR_MASTER_CONTEXT_ACCAOUI / v27.36c")
    for path in V2736C_IMPLEMENTATION_FILES:
        require(section.count(f"`{path}`") == 1, f"CURSOR-Kontext: v27.36c-Datei fehlt oder ist doppelt: {path}")


def validate_v2736c_masterlist_text(text: str) -> None:
    require(exact_field(text, "Stand") == "v27.36c", "PROJECT_MASTERLIST muss auf v27.36c stehen")
    validate_v2736c_permanent_masterlist_contract(text)
    rows = re.findall(r"(?m)^\| v27\.36c \|.*$", text)
    require(
        len(rows) == 1 and rows[0].startswith(V2736C_MASTERLIST_ROW_PREFIX) and "**autorisiert**" in rows[0],
        "PROJECT_MASTERLIST muss v27.36c exakt einmal als autorisiert führen",
    )
    section = section_between(text, "## 14. Nächste sinnvolle Aufgaben", "## 15. Start in neuem Chat", "PROJECT_MASTERLIST")
    validate_required_markers(section, V2736C_MASTERLIST_MARKERS, "PROJECT_MASTERLIST / v27.36c")
    validate_v2736c_supabase_not_live_statement(section)
    validate_no_future_v2736c_sha(section, frozenset({V2736C_AUTHORIZATION_BASE_SHA}), "PROJECT_MASTERLIST / v27.36c")
    for path in V2736C_IMPLEMENTATION_FILES:
        require(section.count(f"`{path}`") == 1, f"PROJECT_MASTERLIST: v27.36c-Datei fehlt oder ist doppelt: {path}")


def detect_v2736c_task_state_text(text: str) -> str:
    task_id = exact_field(text, "Task-ID")
    if task_id == "v27.36c":
        validate_exact_fields(text, V2736C_EXPECTED_TASK_FIELDS)
        return V2736C_TASK_AUTHORIZED
    if task_id == "NONE":
        validate_exact_fields(text, V2736C_CLOSED_TASK_FIELDS)
        return V2736C_TASK_CLOSED
    raise ValidationError(f"Unzulässiger v27.36c-Taskzustand: {task_id}")


def validate_v2736c_closed_documents(
    state_text: str,
    task_text: str,
    cursor_text: str,
    masterlist_text: str,
    implementation_commit: str,
) -> None:
    require(re.fullmatch(r"[0-9a-f]{40}", implementation_commit) is not None, "v27.36c-Closure benötigt einen dynamisch erkannten Implementierungscommit")
    validate_exact_fields(state_text, V2736C_CLOSED_STATE_FIELDS)
    validate_exact_fields(task_text, V2736C_CLOSED_TASK_FIELDS)
    require(exact_field(cursor_text, "Stand") == "v27.36c", "CURSOR-Kontext muss nach v27.36c-Closure auf v27.36c stehen")
    require(exact_field(masterlist_text, "Stand") == "v27.36c", "PROJECT_MASTERLIST muss nach v27.36c-Closure auf v27.36c stehen")
    validate_project_paths(cursor_text, "CURSOR_MASTER_CONTEXT_ACCAOUI")
    validate_v2736c_permanent_masterlist_contract(masterlist_text)
    sections = (
        section_between(state_text, "## Abgeschlossener isolierter Technikschritt v27.36c", "## Abgeschlossener isolierter Technikschritt v27.36b", "PROJECT_STATE_CURRENT"),
        section_between(task_text, "## Abgeschlossener isolierter Technikschritt v27.36c", "## Abgeschlossener isolierter Technikschritt v27.36b", "CURRENT_TASK"),
        section_between(cursor_text, "## 14. Nächster sinnvoller Schritt", "## 15. Wenn ein neuer Chat beginnt", "CURSOR_MASTER_CONTEXT_ACCAOUI"),
        section_between(masterlist_text, "## 14. Nächste sinnvolle Aufgaben", "## 15. Start in neuem Chat", "PROJECT_MASTERLIST"),
    )
    names = ("PROJECT_STATE_CURRENT", "CURRENT_TASK", "CURSOR_MASTER_CONTEXT_ACCAOUI", "PROJECT_MASTERLIST")
    for section, name in zip(sections, names):
        validate_required_markers(section, V2736C_CLOSURE_MARKERS, f"{name} / v27.36c-Closure")
        validate_v2736c_supabase_not_live_statement(section)
        require("v27.36c / AUTHORIZED" not in section, f"{name}: Rückkehr zu v27.36c / AUTHORIZED nach Closure")
        require(section.count(f"Implementierungscommit: `{implementation_commit}`") == 1, f"{name}: dynamischer v27.36c-Implementierungscommit fehlt oder ist doppelt")
        validate_no_future_v2736c_sha(section, frozenset({V2736C_AUTHORIZATION_BASE_SHA, implementation_commit}), f"{name} / v27.36c-Closure")
        for path in V2736C_IMPLEMENTATION_FILES:
            require(section.count(f"`{path}`") == 1, f"{name}: v27.36c-Implementierungsdatei fehlt oder ist doppelt: {path}")
    require("`CURRENT_TASK` ist `NONE` / `BLOCKED` / `Autorisiert: NEIN`." in sections[2], "CURSOR-Kontext muss v27.36c geschlossen blockieren")
    require("`CURRENT_TASK` ist aktuell `NONE` / `BLOCKED` / `Autorisiert: NEIN`." in sections[3], "PROJECT_MASTERLIST muss v27.36c geschlossen blockieren")
    rows = re.findall(r"(?m)^\| v27\.36c \|.*$", masterlist_text)
    require(len(rows) == 1 and "**erledigt**" in rows[0] and implementation_commit in rows[0], "PROJECT_MASTERLIST muss v27.36c nach Closure exakt einmal als erledigt führen")


def validate_v2736b_completed_base() -> tuple[V2736BHistoryState, tuple[str, str, str, str]]:
    require(git_is_ancestor(V2736B_AUTHORIZATION_BASE_SHA, V2736C_AUTHORIZATION_BASE_SHA), "v27.36b-Basis ist kein Vorfahr des v27.36b-Closure-HEAD")
    commit_facts = read_v2736b_commit_facts(V2736C_AUTHORIZATION_BASE_SHA)
    history = validate_v2736b_history_facts(commit_facts)
    require(history.state == V2736B_HISTORY_CLOSED, "v27.36b muss an der v27.36c-Basis vollständig geschlossen sein")
    require(history.implementation_commit is not None, "v27.36b benötigt an der v27.36c-Basis exakt eine IMPLEMENTATION")
    require(history.roles.count(V2736B_ROLE_IMPLEMENTATION) == 1, "v27.36b benötigt exakt einen IMPLEMENTATION-Commit")
    require(history.roles.count(V2736B_ROLE_CLOSURE) == 1 and history.roles[-1] == V2736B_ROLE_CLOSURE, "v27.36b-Closure muss exakt einmal und zuletzt vorliegen")
    require(commit_facts[-1].commit_sha == V2736C_AUTHORIZATION_BASE_SHA, "Verbindlicher v27.36b-Closure-HEAD wurde nicht erkannt")
    require(commit_facts[-1].changed_files == frozenset(EXPECTED_CONTROL_FILES), "v27.36b-Closure-HEAD muss exakt die fünf Gate-Dateien ändern")
    validate_v2736b_committed_closure_documents(commit_facts, history)
    base_documents = (
        read_v2735f_commit_document(V2736C_AUTHORIZATION_BASE_SHA, "docs/PROJECT_STATE_CURRENT.md"),
        read_v2735f_commit_document(V2736C_AUTHORIZATION_BASE_SHA, V2735F_TASK_RELATIVE_PATH),
        read_v2735f_commit_document(V2736C_AUTHORIZATION_BASE_SHA, "docs/CURSOR_MASTER_CONTEXT_ACCAOUI.md"),
        read_v2735f_commit_document(V2736C_AUTHORIZATION_BASE_SHA, "docs/PROJECT_MASTERLIST.md"),
    )
    validate_v2736b_closed_documents(*base_documents, history.implementation_commit)
    return history, base_documents


def read_v2736c_commit_facts(current_head: str) -> tuple[V2736CCommitFact, ...]:
    commit_shas = tuple(line.strip() for line in run_git(["rev-list", "--reverse", f"{V2736C_AUTHORIZATION_BASE_SHA}..{current_head}"]).splitlines() if line.strip())
    previous = V2736C_AUTHORIZATION_BASE_SHA
    facts: list[V2736CCommitFact] = []
    for commit_sha in commit_shas:
        lineage = run_git(["rev-list", "--parents", "-n", "1", commit_sha]).split()
        require(len(lineage) == 2 and lineage[1] == previous, "v27.36c erlaubt nur eine lineare Historie ohne Merge-Commit")
        changed_files = frozenset(line.strip().replace("\\", "/") for line in run_git(["diff", "--name-only", previous, commit_sha]).splitlines() if line.strip())
        require(changed_files, f"Leerer v27.36c-Commit unzulässig: {commit_sha}")
        commit_task = read_v2735f_commit_document(commit_sha, V2735F_TASK_RELATIVE_PATH)
        facts.append(V2736CCommitFact(commit_sha, changed_files, detect_v2736c_task_state_text(commit_task)))
        previous = commit_sha
    return tuple(facts)


def validate_v2736c_history_facts(commit_facts: tuple[V2736CCommitFact, ...]) -> V2736CHistoryState:
    gate_files = frozenset(EXPECTED_CONTROL_FILES)
    roles: list[str] = []
    gate_commits: list[str] = []
    implementation_commit: str | None = None
    closed = False
    for fact in commit_facts:
        files = fact.changed_files
        if files == V2736C_IMPLEMENTATION_FILES:
            require(gate_commits, "v27.36c-IMPLEMENTATION vor Autorisierungs-GATE unzulässig")
            require(implementation_commit is None, "Mehr als ein v27.36c-IMPLEMENTATION-Commit unzulässig")
            require(not closed, "v27.36c-IMPLEMENTATION nach CLOSURE unzulässig")
            require(fact.task_state == V2736C_TASK_AUTHORIZED, "v27.36c-IMPLEMENTATION benötigt AUTHORIZED / Autorisiert JA")
            implementation_commit = fact.commit_sha
            roles.append(V2736C_ROLE_IMPLEMENTATION)
            continue
        require(files and files.issubset(gate_files), f"Fremde Datei in v27.36c-Commit {fact.commit_sha}: {sorted(files - gate_files)}")
        if fact.task_state == V2736C_TASK_AUTHORIZED:
            require(not closed, "Rückkehr zu v27.36c / AUTHORIZED nach CLOSURE unzulässig")
            gate_commits.append(fact.commit_sha)
            roles.append(V2736C_ROLE_GATE)
            continue
        require(implementation_commit is not None, "v27.36c-CLOSURE vor IMPLEMENTATION unzulässig")
        require(not closed, "Mehr als ein v27.36c-CLOSURE-Commit unzulässig")
        closed = True
        roles.append(V2736C_ROLE_CLOSURE)
    state = (
        V2736C_HISTORY_CLOSED if closed else
        V2736C_HISTORY_IMPLEMENTED if implementation_commit is not None else
        V2736C_HISTORY_AUTHORIZED if gate_commits else
        V2736C_HISTORY_BEFORE_AUTHORIZATION
    )
    return V2736CHistoryState(state, implementation_commit, tuple(roles), tuple(gate_commits))


def read_v2736c_working_tree_fact() -> V2736CWorkingTreeFact:
    head = run_git(["rev-parse", "HEAD"]).strip()
    origin_main = run_git(["rev-parse", "origin/main"]).strip()

    def tracked_at(revision: str) -> frozenset[str]:
        return frozenset(line.strip().replace("\\", "/") for line in run_git(["ls-tree", "-r", "--name-only", revision, "--", *sorted(V2736C_NEW_IMPLEMENTATION_FILES)]).splitlines() if line.strip())

    return V2736CWorkingTreeFact(
        branch=run_git(["branch", "--show-current"]).strip(),
        head=head,
        origin_main=origin_main,
        diff_files=frozenset(line.strip().replace("\\", "/") for line in run_git(["diff", "--name-only"]).splitlines() if line.strip()),
        staged_files=frozenset(line.strip().replace("\\", "/") for line in run_git(["diff", "--cached", "--name-only"]).splitlines() if line.strip()),
        untracked_files=frozenset(line.strip().replace("\\", "/") for line in run_git(["ls-files", "--others", "--exclude-standard"]).splitlines() if line.strip()),
        status_lines=frozenset(line.replace("\\", "/") for line in run_git(["status", "--porcelain=v1", "--untracked-files=all"]).splitlines() if line),
        implementation_files_existing=frozenset(path for path in V2736C_NEW_IMPLEMENTATION_FILES if (ROOT / path).is_file()),
        implementation_files_tracked_at_base=tracked_at(V2736C_AUTHORIZATION_BASE_SHA),
        implementation_files_tracked_at_head=tracked_at(head),
        base_is_head_ancestor=git_is_ancestor(V2736C_AUTHORIZATION_BASE_SHA, head),
        base_is_origin_ancestor=git_is_ancestor(V2736C_AUTHORIZATION_BASE_SHA, origin_main),
        origin_is_head_ancestor=git_is_ancestor(origin_main, head),
    )


def validate_v2736c_working_tree_fact(fact: V2736CWorkingTreeFact) -> None:
    require(fact.branch == "main", "v27.36c-Lebenszyklus muss auf main laufen")
    require(fact.base_is_head_ancestor, "Die stabile v27.36c-Basis ist kein Vorfahr von HEAD")
    require(fact.base_is_origin_ancestor, "Die stabile v27.36c-Basis ist kein Vorfahr von origin/main")
    require(fact.origin_is_head_ancestor, "origin/main ist kein Vorfahr des lokalen v27.36c-HEAD")
    require(not fact.implementation_files_tracked_at_base, "Neue v27.36c-Implementierungsdateien dürfen an der Basis nicht existieren")
    require(not fact.staged_files, "v27.36c-Lebenszyklus darf nichts stagen")


def validate_v2736c_source_contract(bridge_text: str, checker_text: str, report_text: str, preflight_text: str) -> None:
    for marker in ("getClient", "resolveAccess", "participant-access", "factory", "utc"):
        require(marker.lower() in bridge_text.lower(), f"v27.36c-Brückenbindung fehlt: {marker}")
    bridge_forbidden = (
        "window.", "globalThis", "global.", "createClient(", "initializeClient(",
        "getState(", "getConfig", "getSdk", "isLive", "liveEnabled",
        "configEnabled", "sdkEnabled", ".from(", "participants", "enrollments",
        "courses",
        "fetch(", "XMLHttpRequest", "WebSocket", "http://", "https://", "process.env",
        "Deno.env", "Bun.env", "service_role", "anonKey",
    )
    checker_forbidden = ("subprocess", "os.system", "socket", "requests", "urllib", "httpx", "fetch(", "http://", "https://", "os.environ")
    bridge_folded = bridge_text.casefold()
    checker_folded = checker_text.casefold()
    for token in bridge_forbidden:
        require(token.casefold() not in bridge_folded, f"v27.36c-Brücke verletzt lokale Sicherheitsgrenze: {token}")
    for token in checker_forbidden:
        require(token.casefold() not in checker_folded, f"v27.36c-Fake-Bootstrap-Checker verletzt lokale Sicherheitsgrenze: {token}")
    for marker in (
        "Ziel", "Sicherheitsgrenze", "injizierte Dependencies",
        "bootstrap.getClient()", "keine duplizierte Fachlogik",
        "Fail-closed-Regeln", "Fake-Bootstrap", "getestete Fälle",
        "unveränderte Bestandsmodule", "Supabase live: NEIN", "echte Keys: NEIN",
        "echte Teilnehmerdaten: NEIN",
    ):
        require(marker in report_text, f"v27.36c-Umsetzungsbericht fehlt: {marker}")
    require("Fake" in checker_text and "supabase-participant-access-bootstrap-bridge" in checker_text, "Lokaler v27.36c-Fake-Bootstrap-Checker ist nicht verbindlich an die Brücke gebunden")
    require("check-supabase-participant-access-bootstrap-bridge.py" in preflight_text, "v27.36c-Checker fehlt im Preflight")
    require("check-supabase-participant-access-adapter.py" in preflight_text, "v27.36b-Adapter-Checker darf aus dem Preflight nicht entfernt werden")
    require("check-project-continuity-control.py" in preflight_text, "Kontinuitäts-Checker darf im Preflight nicht entfernt werden")


def validate_v2736c_local_source_contract() -> None:
    validate_v2736c_source_contract(
        read_required_text(ROOT / "data/supabase-participant-access-bootstrap-bridge.js"),
        read_required_text(ROOT / "tools/check-supabase-participant-access-bootstrap-bridge.py"),
        read_required_text(ROOT / "docs/SUPABASE_PARTICIPANT_ACCESS_BOOTSTRAP_BRIDGE_V2736C.md"),
        read_required_text(PREFLIGHT_PATH),
    )


def validate_v2736c_source_contract_at_revision(revision: str) -> None:
    validate_v2736c_source_contract(
        read_v2735f_commit_document(revision, "data/supabase-participant-access-bootstrap-bridge.js"),
        read_v2735f_commit_document(revision, "tools/check-supabase-participant-access-bootstrap-bridge.py"),
        read_v2735f_commit_document(revision, "docs/SUPABASE_PARTICIPANT_ACCESS_BOOTSTRAP_BRIDGE_V2736C.md"),
        read_v2735f_commit_document(revision, "tools/preflight.py"),
    )


def validate_v2736c_lifecycle_working_tree(history: V2736CHistoryState, task_state: str, fact: V2736CWorkingTreeFact) -> str:
    validate_v2736c_working_tree_fact(fact)
    gate_files = frozenset(EXPECTED_CONTROL_FILES)
    clean = not fact.diff_files and not fact.untracked_files and not fact.status_lines
    if history.state == V2736C_HISTORY_BEFORE_AUTHORIZATION:
        require(fact.head == V2736C_AUTHORIZATION_BASE_SHA, "Autorisierungsvorbereitung benötigt die stabile v27.36c-Basis als HEAD")
        require(task_state == V2736C_TASK_AUTHORIZED, "Autorisierungsvorbereitung benötigt v27.36c / AUTHORIZED")
        require(fact.diff_files == gate_files, "Autorisierungsvorbereitung muss exakt fünf Gate-Dateien ändern")
        require(not fact.untracked_files and fact.status_lines == frozenset(f" M {path}" for path in gate_files), "Working Tree entspricht nicht authorization_prepared")
        require(not fact.implementation_files_existing, "v27.36c-Implementation vor Autorisierungscommit unzulässig")
        return V2736C_PHASE_AUTHORIZATION_PREPARED
    if history.state == V2736C_HISTORY_AUTHORIZED:
        require(fact.head != V2736C_AUTHORIZATION_BASE_SHA, "Autorisierungscommit fehlt")
        require(task_state == V2736C_TASK_AUTHORIZED, "Autorisierte Phasen benötigen v27.36c / AUTHORIZED")
        require(not fact.implementation_files_tracked_at_head, "Neue v27.36c-Dateien dürfen vor IMPLEMENTATION nicht getrackt sein")
        if clean:
            require(not fact.implementation_files_existing, "Implementation darf vor preparation nicht lokal existieren")
            return V2736C_PHASE_AUTHORIZATION_COMMITTED
        if fact.diff_files and fact.diff_files.issubset(gate_files) and not fact.untracked_files:
            require(fact.status_lines == frozenset(f" M {path}" for path in fact.diff_files), "Lokale v27.36c-Gate-Korrektur enthält fremden Status")
            require(not fact.implementation_files_existing, "Implementation während Gate-Korrektur unzulässig")
            return V2736C_PHASE_AUTHORIZATION_COMMITTED
        require(fact.diff_files == frozenset({"tools/preflight.py"}), "implementation_prepared darf getrackt nur tools/preflight.py ändern")
        require(fact.untracked_files == V2736C_NEW_IMPLEMENTATION_FILES, "implementation_prepared benötigt exakt drei neue Implementierungsdateien")
        require(fact.implementation_files_existing == V2736C_NEW_IMPLEMENTATION_FILES, "implementation_prepared benötigt alle drei neuen Dateien")
        expected_status = frozenset({" M tools/preflight.py", *(f"?? {path}" for path in V2736C_NEW_IMPLEMENTATION_FILES)})
        require(fact.status_lines == expected_status, "Working Tree entspricht nicht implementation_prepared")
        return V2736C_PHASE_IMPLEMENTATION_PREPARED
    require(history.implementation_commit is not None, "Phase nach IMPLEMENTATION benötigt den dynamischen Implementierungscommit")
    require(fact.implementation_files_tracked_at_head == V2736C_NEW_IMPLEMENTATION_FILES, "Nach IMPLEMENTATION müssen alle drei neuen Dateien getrackt sein")
    require(fact.implementation_files_existing == V2736C_NEW_IMPLEMENTATION_FILES, "Nach IMPLEMENTATION müssen alle drei neuen Dateien vorhanden sein")
    if history.state == V2736C_HISTORY_IMPLEMENTED:
        if task_state == V2736C_TASK_AUTHORIZED:
            if clean:
                return V2736C_PHASE_IMPLEMENTATION_COMMITTED
            require(fact.diff_files and fact.diff_files.issubset(gate_files) and not fact.untracked_files, "Nach IMPLEMENTATION sind lokal nur Gate-Korrekturen oder Closure zulässig")
            require(fact.status_lines == frozenset(f" M {path}" for path in fact.diff_files), "Lokale Gate-Korrektur nach IMPLEMENTATION enthält fremden Status")
            return V2736C_PHASE_IMPLEMENTATION_COMMITTED
        require(task_state == V2736C_TASK_CLOSED, "closure_prepared benötigt den geschlossenen v27.36c-Taskzustand")
        require(fact.diff_files == gate_files and not fact.untracked_files, "closure_prepared muss exakt fünf Gate-Dateien ändern")
        require(fact.status_lines == frozenset(f" M {path}" for path in gate_files), "Working Tree entspricht nicht closure_prepared")
        return V2736C_PHASE_CLOSURE_PREPARED
    require(history.state == V2736C_HISTORY_CLOSED, "Unbekannter v27.36c-Historienzustand")
    require(task_state == V2736C_TASK_CLOSED, "Nach v27.36c-CLOSURE darf keine Rückkehr zu AUTHORIZED erfolgen")
    require(clean, "closure_committed benötigt einen sauberen Working Tree")
    return V2736C_PHASE_CLOSURE_COMMITTED


def validate_v2736c_committed_closure_documents(facts: tuple[V2736CCommitFact, ...], history: V2736CHistoryState) -> None:
    if V2736C_ROLE_CLOSURE not in history.roles:
        return
    require(history.implementation_commit is not None, "v27.36c-CLOSURE benötigt einen dynamischen Implementierungscommit")
    for fact, role in zip(facts, history.roles):
        if role == V2736C_ROLE_CLOSURE:
            validate_v2736c_closed_documents(
                read_v2735f_commit_document(fact.commit_sha, "docs/PROJECT_STATE_CURRENT.md"),
                read_v2735f_commit_document(fact.commit_sha, V2735F_TASK_RELATIVE_PATH),
                read_v2735f_commit_document(fact.commit_sha, "docs/CURSOR_MASTER_CONTEXT_ACCAOUI.md"),
                read_v2735f_commit_document(fact.commit_sha, "docs/PROJECT_MASTERLIST.md"),
                history.implementation_commit,
            )


def validate_v2736c_lifecycle(state_text: str, task_text: str, cursor_text: str, masterlist_text: str) -> tuple[str, V2736CHistoryState, V2736CWorkingTreeFact]:
    fact = read_v2736c_working_tree_fact()
    validate_v2736c_working_tree_fact(fact)
    commit_facts = read_v2736c_commit_facts(fact.head)
    history = validate_v2736c_history_facts(commit_facts)
    validate_v2736c_committed_closure_documents(commit_facts, history)
    task_state = detect_v2736c_task_state_text(task_text)
    if task_state == V2736C_TASK_AUTHORIZED:
        validate_v2736c_state_text(state_text)
        validate_v2736c_task_text(task_text)
        validate_v2736c_cursor_text(cursor_text)
        validate_v2736c_masterlist_text(masterlist_text)
    else:
        require(history.implementation_commit is not None, "v27.36c-Abschluss vor IMPLEMENTATION unzulässig")
        validate_v2736c_closed_documents(state_text, task_text, cursor_text, masterlist_text, history.implementation_commit)
    phase = validate_v2736c_lifecycle_working_tree(history, task_state, fact)
    if phase == V2736C_PHASE_IMPLEMENTATION_PREPARED:
        validate_v2736c_local_source_contract()
    if history.implementation_commit is not None:
        validate_v2736c_source_contract_at_revision(history.implementation_commit)
    return phase, history, fact


def run_v2736c_manipulation_matrix(
    state_text: str,
    task_text: str,
    cursor_text: str,
    masterlist_text: str,
    current_history: V2736CHistoryState,
    current_fact: V2736CWorkingTreeFact,
) -> tuple[int, int, int]:
    checks = 0
    for variant in (
        "Supabase bleibt NICHT LIVE.",
        "Supabase bleibt\nNICHT LIVE.",
        "Supabase\n\nbleibt\tNICHT   LIVE.",
    ):
        validate_v2736c_supabase_not_live_statement(variant)
    must_reject(
        validate_v2736c_supabase_not_live_statement,
        "",
        "v27.36c-Supabase-NICHT-LIVE-Aussage entfernt",
    )
    checks += 1
    must_reject(
        validate_v2736c_supabase_not_live_statement,
        "Supabase bleibt LIVE.",
        "v27.36c-Supabase-NICHT-LIVE-Aussage inhaltlich geändert",
    )
    checks += 1
    current_task_state = detect_v2736c_task_state_text(task_text)
    validate_v2736c_permanent_masterlist_contract(masterlist_text)
    for marker in V2736C_PERMANENT_MASTERLIST_MODE_MARKERS:
        require(
            marker in masterlist_text,
            f"Manipulationsmatrix kann permanente Masterlisten-Regel nicht finden: {marker}",
        )
        must_reject(
            validate_v2736c_permanent_masterlist_contract,
            masterlist_text.replace(marker, "", 1),
            f"PROJECT_MASTERLIST: permanente Regel entfernt: {marker}",
        )
        checks += 1
    for field, value in (
        ("Arbeits-Laptop", V2736C_VERIFIED_WORK_PATH),
        ("Git Bash Arbeits-Laptop", V2736C_VERIFIED_WORK_PATH_GIT_BASH),
    ):
        must_reject(
            validate_v2736c_permanent_masterlist_contract,
            changed_once(
                masterlist_text,
                f"{field}: `{value}`",
                f"{field}: `MANIPULIERT`",
                f"PROJECT_MASTERLIST / {field}",
            ),
            f"PROJECT_MASTERLIST: manipulierter Pfad {field}",
        )
        checks += 1
    if current_task_state == V2736C_TASK_AUTHORIZED:
        for text, validator, fields, name in (
            (state_text, validate_v2736c_state_text, V2736C_EXPECTED_STATE_FIELDS, "PROJECT_STATE_CURRENT"),
            (task_text, validate_v2736c_task_text, V2736C_EXPECTED_TASK_FIELDS, "CURRENT_TASK"),
        ):
            for field, value in fields.items():
                must_reject(validator, changed_once(text, f"{field}: {value}", f"{field}: MANIPULIERT", f"{name} / {field}"), f"{name}: manipuliertes Feld {field}")
                checks += 1
        for text, validator, markers, name in (
            (state_text, validate_v2736c_state_text, V2736C_STATE_MARKERS, "PROJECT_STATE_CURRENT"),
            (task_text, validate_v2736c_task_text, V2736C_TASK_MARKERS, "CURRENT_TASK"),
            (cursor_text, validate_v2736c_cursor_text, V2736C_CURSOR_MARKERS, "CURSOR_MASTER_CONTEXT_ACCAOUI"),
            (masterlist_text, validate_v2736c_masterlist_text, V2736C_MASTERLIST_MARKERS, "PROJECT_MASTERLIST"),
        ):
            for marker in markers:
                require(marker in text, f"Manipulationsmatrix kann v27.36c-Pflichtaussage nicht finden: {name} / {marker}")
                must_reject(validator, text.replace(marker, "", 1), f"{name}: v27.36c-Pflichtaussage entfernt: {marker}")
                checks += 1
        for text, validator, name in (
            (state_text, validate_v2736c_state_text, "PROJECT_STATE_CURRENT"),
            (task_text, validate_v2736c_task_text, "CURRENT_TASK"),
            (cursor_text, validate_v2736c_cursor_text, "CURSOR_MASTER_CONTEXT_ACCAOUI"),
            (masterlist_text, validate_v2736c_masterlist_text, "PROJECT_MASTERLIST"),
        ):
            match = V2736C_SUPABASE_NOT_LIVE_PATTERN.search(text)
            require(match is not None, f"Manipulationsmatrix kann Supabase-NICHT-LIVE-Aussage nicht finden: {name}")
            validator(
                text[: match.start()]
                + "Supabase\n\nbleibt\tNICHT   LIVE."
                + text[match.end() :]
            )
            must_reject(
                validator,
                text[: match.start()] + "Supabase bleibt LIVE." + text[match.end() :],
                f"{name}: Supabase-NICHT-LIVE-Aussage inhaltlich geändert",
            )
            checks += 1
        must_reject(validate_v2736c_task_text, task_text.replace("## Abgeschlossener isolierter Technikschritt v27.36b", "Zukünftiger Commit: `aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa`\n\n## Abgeschlossener isolierter Technikschritt v27.36b", 1), "zukünftige SHA hartcodiert")
        checks += 1
        must_reject(validate_v2736c_task_text, task_text.replace("Kein Folgetask nach v27.36c", "v27.36d / AUTHORIZED\n\nKein Folgetask nach v27.36c", 1), "automatischer Folgetask v27.36d")
        checks += 1

    gate = V2736CCommitFact("1" * 40, frozenset({EXPECTED_CONTROL_FILES[0]}), V2736C_TASK_AUTHORIZED)
    implementation = V2736CCommitFact("2" * 40, V2736C_IMPLEMENTATION_FILES, V2736C_TASK_AUTHORIZED)
    closure = V2736CCommitFact("3" * 40, frozenset({EXPECTED_CONTROL_FILES[1]}), V2736C_TASK_CLOSED)
    histories = (
        validate_v2736c_history_facts(tuple()),
        validate_v2736c_history_facts((gate,)),
        validate_v2736c_history_facts((gate, implementation)),
        validate_v2736c_history_facts((gate, implementation, closure)),
    )
    clean_fact = replace(
        current_fact,
        head="1" * 40,
        diff_files=frozenset(), staged_files=frozenset(), untracked_files=frozenset(), status_lines=frozenset(),
        implementation_files_existing=frozenset(), implementation_files_tracked_at_base=frozenset(), implementation_files_tracked_at_head=frozenset(),
        base_is_head_ancestor=True, base_is_origin_ancestor=True, origin_is_head_ancestor=True,
    )
    gate_files = frozenset(EXPECTED_CONTROL_FILES)
    implemented_fact = replace(clean_fact, head="2" * 40, implementation_files_existing=V2736C_NEW_IMPLEMENTATION_FILES, implementation_files_tracked_at_head=V2736C_NEW_IMPLEMENTATION_FILES)
    phase_fixtures = (
        (histories[0], V2736C_TASK_AUTHORIZED, replace(clean_fact, head=V2736C_AUTHORIZATION_BASE_SHA, diff_files=gate_files, status_lines=frozenset(f" M {p}" for p in gate_files)), V2736C_PHASE_AUTHORIZATION_PREPARED),
        (histories[1], V2736C_TASK_AUTHORIZED, clean_fact, V2736C_PHASE_AUTHORIZATION_COMMITTED),
        (histories[1], V2736C_TASK_AUTHORIZED, replace(clean_fact, diff_files=frozenset({"tools/preflight.py"}), untracked_files=V2736C_NEW_IMPLEMENTATION_FILES, status_lines=frozenset({" M tools/preflight.py", *(f"?? {p}" for p in V2736C_NEW_IMPLEMENTATION_FILES)}), implementation_files_existing=V2736C_NEW_IMPLEMENTATION_FILES), V2736C_PHASE_IMPLEMENTATION_PREPARED),
        (histories[2], V2736C_TASK_AUTHORIZED, implemented_fact, V2736C_PHASE_IMPLEMENTATION_COMMITTED),
        (histories[2], V2736C_TASK_CLOSED, replace(implemented_fact, diff_files=gate_files, status_lines=frozenset(f" M {p}" for p in gate_files)), V2736C_PHASE_CLOSURE_PREPARED),
        (histories[3], V2736C_TASK_CLOSED, implemented_fact, V2736C_PHASE_CLOSURE_COMMITTED),
    )
    for history, task_state, fact, expected in phase_fixtures:
        require(validate_v2736c_lifecycle_working_tree(history, task_state, fact) == expected, f"v27.36c-Positivsimulation fehlgeschlagen: {expected}")
    positive_tests = len(phase_fixtures)

    forbidden_history_files = (
        "app.js", "index.html", "style.css", "data/supabase-client-bootstrap.js",
        "data/supabase-client-adapter.js", "data/supabase-participant-access-adapter.js",
        "data/supabase-config.js", "supabase/migrations/unsafe.sql", "data/supabase-live-client.js",
    )
    bad_histories: list[tuple[tuple[V2736CCommitFact, ...], str]] = [
        ((implementation,), "Implementation vor Autorisierung"),
        ((gate, implementation, implementation), "zweite Implementation"),
        ((gate, closure), "Closure vor Implementation"),
        ((gate, implementation, closure, gate), "Rückkehr nach Closure"),
        ((gate, implementation, closure, closure), "zweite Closure"),
        ((gate, V2736CCommitFact("a" * 40, frozenset(set(V2736C_IMPLEMENTATION_FILES) - {"tools/preflight.py"}), V2736C_TASK_AUTHORIZED)), "partielle Implementation"),
        ((gate, V2736CCommitFact("b" * 40, V2736C_IMPLEMENTATION_FILES | {"app.js"}, V2736C_TASK_AUTHORIZED)), "Implementation mit Zusatzdatei"),
    ]
    bad_histories.extend(((V2736CCommitFact(f"{index:x}" * 40, frozenset({path}), V2736C_TASK_AUTHORIZED),), f"verbotene Datei {path}") for index, path in enumerate(forbidden_history_files, 4))
    for facts, label in bad_histories:
        try:
            validate_v2736c_history_facts(facts)
        except ValidationError:
            checks += 1
            continue
        raise ValidationError(f"v27.36c-Historienmanipulation wurde nicht blockiert: {label}")

    bad_working = (
        (current_history, V2736C_TASK_AUTHORIZED, replace(current_fact, staged_files=frozenset({EXPECTED_CONTROL_FILES[0]})), "gestagte Datei"),
        (current_history, V2736C_TASK_AUTHORIZED, replace(current_fact, diff_files=current_fact.diff_files | {"app.js"}, status_lines=current_fact.status_lines | {" M app.js"}), "fremde lokale Datei"),
        (current_history, V2736C_TASK_AUTHORIZED, replace(current_fact, untracked_files=frozenset({"unexpected.txt"}), status_lines=current_fact.status_lines | {"?? unexpected.txt"}), "fremde ungetrackte Datei"),
        (current_history, V2736C_TASK_AUTHORIZED, replace(current_fact, base_is_head_ancestor=False), "falsche Basis"),
        (current_history, V2736C_TASK_AUTHORIZED, replace(current_fact, origin_is_head_ancestor=False), "origin nicht Vorfahr"),
        (current_history, V2736C_TASK_AUTHORIZED, replace(current_fact, implementation_files_tracked_at_base=V2736C_NEW_IMPLEMENTATION_FILES), "Implementierungsdateien bereits an Basis"),
        (histories[0], V2736C_TASK_AUTHORIZED, replace(clean_fact, head=V2736C_AUTHORIZATION_BASE_SHA, untracked_files=V2736C_NEW_IMPLEMENTATION_FILES, status_lines=frozenset(f"?? {p}" for p in V2736C_NEW_IMPLEMENTATION_FILES), implementation_files_existing=V2736C_NEW_IMPLEMENTATION_FILES), "Implementation lokal vor Autorisierung"),
        (histories[1], V2736C_TASK_CLOSED, replace(clean_fact, diff_files=gate_files, status_lines=frozenset(f" M {p}" for p in gate_files)), "Closure lokal vor Implementation"),
        (histories[3], V2736C_TASK_AUTHORIZED, implemented_fact, "Rückkehr zu AUTHORIZED nach Closure"),
    )
    for history, task_state, fact, label in bad_working:
        try:
            validate_v2736c_lifecycle_working_tree(history, task_state, fact)
        except ValidationError:
            checks += 1
            continue
        raise ValidationError(f"v27.36c-Working-Tree-Manipulation wurde nicht blockiert: {label}")

    valid_bridge = "bootstrap.getClient() resolveAccess participant-access factory utc"
    valid_checker = "Fake fake-bootstrap supabase-participant-access-bootstrap-bridge"
    valid_report = "\n".join(("Ziel", "Sicherheitsgrenze", "injizierte Dependencies", "bootstrap.getClient()", "keine duplizierte Fachlogik", "Fail-closed-Regeln", "Fake-Bootstrap", "getestete Fälle", "unveränderte Bestandsmodule", "Supabase live: NEIN", "echte Keys: NEIN", "echte Teilnehmerdaten: NEIN"))
    valid_preflight = "check-project-continuity-control.py check-supabase-participant-access-adapter.py check-supabase-participant-access-bootstrap-bridge.py"
    validate_v2736c_source_contract(valid_bridge, valid_checker, valid_report, valid_preflight)
    source_manipulations = (
        (valid_bridge + " fetch(", valid_checker, valid_report, valid_preflight, "Netzwerk in Brücke"),
        (valid_bridge + " createClient(", valid_checker, valid_report, valid_preflight, "Client-Erzeugung"),
        (valid_bridge + " initializeClient(", valid_checker, valid_report, valid_preflight, "Bootstrap-Initialisierung"),
        (valid_bridge + " getState(", valid_checker, valid_report, valid_preflight, "Bootstrap-State-Abhängigkeit"),
        (valid_bridge + " getSdkState(", valid_checker, valid_report, valid_preflight, "SDK-State-Schalter"),
        (valid_bridge + " .from('participants')", valid_checker, valid_report, valid_preflight, "duplizierte Teilnehmer-Fachlogik"),
        (valid_bridge, valid_checker + " subprocess", valid_report, valid_preflight, "Prozess im Fake-Checker"),
        (valid_bridge, valid_checker, valid_report.replace("Fail-closed-Regeln", ""), valid_preflight, "Fail-closed-Bericht entfernt"),
        (valid_bridge, valid_checker, valid_report, valid_preflight.replace("check-supabase-participant-access-bootstrap-bridge.py", ""), "neuer Checker aus Preflight entfernt"),
        (valid_bridge, valid_checker, valid_report, valid_preflight.replace("check-supabase-participant-access-adapter.py", ""), "v27.36b-Checker aus Preflight entfernt"),
    )
    for bridge, checker, report, preflight, label in source_manipulations:
        try:
            validate_v2736c_source_contract(bridge, checker, report, preflight)
        except ValidationError:
            checks += 1
            continue
        raise ValidationError(f"v27.36c-Sicherheitsmanipulation wurde nicht blockiert: {label}")
    negative_tests = len(bad_histories) + len(bad_working) + len(source_manipulations) + (2 if current_task_state == V2736C_TASK_AUTHORIZED else 0)
    return checks, positive_tests, negative_tests


V2736D_AUTHORIZATION_BASE_SHA = "f2f40389a22ea4a40acd7ebdf7ca672add4baf8e"
V2736D_TITLE = "Teilnehmerzugangs-Entscheidung lokal an den bestehenden App-Auth-Einstieg anbinden"
V2736D_IMPLEMENTATION_FILES = frozenset(
    {
        "app.js",
        "tools/check-participant-access-app-entry-v2736d.py",
        "docs/PARTICIPANT_ACCESS_APP_ENTRY_V2736D.md",
        "tools/preflight.py",
    }
)
V2736D_NEW_IMPLEMENTATION_FILES = frozenset(
    V2736D_IMPLEMENTATION_FILES - {"app.js", "tools/preflight.py"}
)
V2736D_ALLOWED_FILES_VALUE = (
    "`app.js`, `tools/check-participant-access-app-entry-v2736d.py`, "
    "`docs/PARTICIPANT_ACCESS_APP_ENTRY_V2736D.md`, `tools/preflight.py`"
)
V2736D_EXPECTED_STATE_FIELDS = {
    "Stand": "v27.36d",
    "Repository": "`asarrad-bit/accaoui-34a-lernapp`",
    "Branch": "`main`",
    "Letzter abgeschlossener funktionaler Stand": "v27.35g",
    "Abschlusscommit": f"`{V2735G_COMPLETION_SHA}`",
    "Aktueller HEAD": "DYNAMISCH ZU PRÜFEN",
    "Funktionsstatus": "v27.35g abgeschlossen",
    "Weiterer funktionaler Schritt autorisiert": "JA",
    "Aktuell autorisierter Task": "v27.36d",
    "Aktuelle Taskart": "Teilnehmerzugangs-Entscheidung am App-Auth-Einstieg",
    "Aktueller Blocker": "KEINER – v27.36d ist autorisiert; die Umsetzung ist noch nicht begonnen",
}
V2736D_EXPECTED_TASK_FIELDS = {
    "Task-ID": "v27.36d",
    "Status": "AUTHORIZED",
    "Autorisiert": "JA",
    "Titel": V2736D_TITLE,
    "Funktionaler Ausgangsstand": "v27.35g",
    "Technischer Ausgangsstand": "v27.36c abgeschlossen",
    "Stabile Autorisierungsbasis": f"`{V2736D_AUTHORIZATION_BASE_SHA}`",
    "Erlaubte Implementierungsdateien": V2736D_ALLOWED_FILES_VALUE,
    "Commit erlaubt": "NEIN",
    "Push erlaubt": "NEIN",
}
V2736D_CLOSED_STATE_FIELDS = {
    "Stand": "v27.36d",
    "Repository": "`asarrad-bit/accaoui-34a-lernapp`",
    "Branch": "`main`",
    "Letzter abgeschlossener funktionaler Stand": "v27.35g",
    "Abschlusscommit": f"`{V2735G_COMPLETION_SHA}`",
    "Aktueller HEAD": "DYNAMISCH ZU PRÜFEN",
    "Funktionsstatus": "v27.35g abgeschlossen",
    "Weiterer funktionaler Schritt autorisiert": "NEIN",
    "Aktuell autorisierter Task": "NONE",
    "Aktuelle Taskart": "Kein Task autorisiert",
    "Aktueller Blocker": (
        "Neue Taskauswahl und ausdrückliche Autorisierung durch "
        "Projekteigentümer und verbindlichen Projektchat"
    ),
}
V2736D_CLOSED_TASK_FIELDS = {
    "Task-ID": "NONE",
    "Status": "BLOCKED",
    "Autorisiert": "NEIN",
    "Titel": "Kein Task autorisiert",
    "Funktionaler Ausgangsstand": "v27.35g",
    "Letzter abgeschlossener Kontrollschritt": "v27.36d",
    "Erlaubte Implementierungsdateien": "KEINE",
    "Commit erlaubt": "NEIN",
    "Push erlaubt": "NEIN",
}
V2736D_AUTHORIZATION_MARKERS = (
    "v27.36c ist vollständig abgeschlossen.",
    "v27.36d ist der einzige autorisierte",
    "Teilnehmerzugangs-Entscheidung lokal an den bestehenden",
    "App-Auth-Einstieg anbinden",
    "Dieser GATE-Schritt autorisiert nur die spätere Umsetzung.",
    "window.ACCAOUI_PARTICIPANT_ACCESS_APP_PROVIDER",
    "resolveAccess()",
    "lokale Standardstart unverändert",
    "access_allowed",
    "startLocalApp()",
    "fail-closed",
    "rohe interne Fehlerausgabe",
    "niemals ein Rückfall auf den",
    "Auth-Guard-Testzustände",
    "Bestehender Bootstrap",
    "v27.36b-/v27.36c-CommonJS-Module",
    "lokalen synthetischen Provider",
    "Supabase bleibt NICHT LIVE.",
    "Keine echten Keys.",
    "Keine echten Teilnehmerdaten.",
    "Kein Folgetask nach v27.36d wurde ausgewählt oder",
    "### Permanenter v27.36d-Lebenszyklus",
    "authorization_prepared",
    "authorization_committed",
    "implementation_prepared",
    "implementation_committed",
    "closure_prepared",
    "closure_committed",
    "GATE enthält ausschließlich eine nichtleere Teilmenge der fünf Gate-Dateien.",
    "IMPLEMENTATION enthält exakt die vier autorisierten Implementierungsdateien",
    "CLOSURE ist erst nach IMPLEMENTATION zulässig",
    "Keine zukünftige GATE-, IMPLEMENTATION-",
    "ausdrücklichen fachlichen Autorisierung BLOCKED",
)
V2736D_DETAILED_CODE_MARKERS = (
    "session_missing",
    "session_invalid",
    "session_user_missing",
    "session_user_id_invalid",
    "participant_blocked",
    "enrollment_blocked",
    "participant_expired",
    "enrollment_expired",
    "enrollment_access_ended",
    "course_ended",
    "participant_completed",
    "enrollment_missing",
    "enrollment_completed",
    "enrollment_access_not_started",
    "course_missing",
    "course_inactive",
    "course_archived",
    "course_not_started",
)
V2736D_PERMANENT_MASTERLIST_MODE_MARKERS = (
    "### Commit-/Push-Freigabe bei autorisierten Lifecycle-Schritten",
    "Für einen fachlich autorisierten Task ist bei einem legitimen GATE-, IMPLEMENTATION- oder CLOSURE-Schritt keine zusätzliche Nutzerfreigabe nur für Commit/Push erforderlich.",
    "technische Lead darf Commit und Push für einen solchen Schritt auslösen oder empfehlen",
    "Task und Lifecycle korrekt",
    "ausschließlich erlaubte Dateien geändert",
    "alle verbindlichen Checker PASS",
    "der Preflight PASS",
    "`git diff --check` PASS",
    "keine unerwarteten Änderungen",
    "keine offene Sicherheits- oder Architekturabweichung",
    "Bei jeder Abweichung gilt sofort STOPP.",
    "Diese Regel ersetzt nicht die fachliche Autorisierung eines neuen Tasks.",
    "Nach einer Closure bleibt jede neue Implementierung vollständig BLOCKED",
)
V2736D_CLOSURE_MARKERS = (
    "v27.36d abgeschlossen.",
    "window.ACCAOUI_PARTICIPANT_ACCESS_APP_PROVIDER",
    "Schnittstelle bleibt ausschließlich `resolveAccess()`.",
    "Ohne Provider bleibt der lokale Standardbetrieb unverändert.",
    "Lokale Auth-Guard-Testzustände behalten Vorrang.",
    "Nur `allowed=true` zusammen mit `code=\"access_allowed\"` startet die lokale App.",
    "Providerfehler und ungültige Ergebnisse bleiben fail-closed.",
    "Nach einem erkannten Providerfehler gibt es keinen lokalen Fallback.",
    "Ablehnungscodes werden auf die vorhandenen Zugangsansichten abgebildet.",
    "Unbekannte und technische Fehler bleiben generisch fail-closed.",
    "In app.js gibt es keine direkten Supabase- oder Datenbankabfragen.",
    "Der letzte abgeschlossene funktionale Stand bleibt v27.35g.",
    "Bestehender Bootstrap, zentraler Adapter, v27.36b-Teilnehmerzugangs-Adapter und v27.36c-Brücke bleiben unverändert.",
    "keine Browser-Verbindung zu den CommonJS-v27.36b/v27.36c-Modulen.",
    "Supabase bleibt NICHT LIVE.",
    "Keine echten Keys.",
    "Keine echten Teilnehmerdaten.",
    "v27.36d-Checker: PASS (Positiv: 2; Negativ: 36; Manipulation: 10).",
    "Kontinuitätschecker: PASS.",
    "Preflight: PASS.",
    "`git diff --check`: PASS.",
    "Der allgemeine Protected-Core-Schutz bleibt aktiv.",
    "v27.36d-Ausnahme war ausschließlich auf den autorisierten app.js-Scope begrenzt.",
    "Keine generelle Freigabe von app.js oder anderen Protected-Core-Dateien.",
    "Kein Folgetask wurde ausgewählt oder autorisiert.",
    "vollständig BLOCKED, bis sie ausdrücklich autorisiert wird.",
    "Keine zukünftige CLOSURE-SHA wird hartcodiert.",
    "Rückkehr zu einem autorisierten v27.36d-Zustand bleibt ohne neue ausdrückliche Autorisierung blockiert.",
)
V2736D_SUPABASE_NOT_LIVE_PATTERN = re.compile(r"Supabase\s+bleibt\s+NICHT\s+LIVE\.")
V2736D_TASK_AUTHORIZED = "authorized"
V2736D_TASK_CLOSED = "closed"
V2736D_HISTORY_BEFORE_AUTHORIZATION = "before_authorization_commit"
V2736D_HISTORY_AUTHORIZED = "authorization_committed"
V2736D_HISTORY_IMPLEMENTED = "implementation_committed"
V2736D_HISTORY_CLOSED = "closure_committed"
V2736D_PHASE_AUTHORIZATION_PREPARED = "authorization_prepared"
V2736D_PHASE_AUTHORIZATION_COMMITTED = "authorization_committed"
V2736D_PHASE_IMPLEMENTATION_PREPARED = "implementation_prepared"
V2736D_PHASE_IMPLEMENTATION_COMMITTED = "implementation_committed"
V2736D_PHASE_CLOSURE_PREPARED = "closure_prepared"
V2736D_PHASE_CLOSURE_COMMITTED = "closure_committed"
V2736D_ROLE_GATE = "GATE"
V2736D_ROLE_IMPLEMENTATION = "IMPLEMENTATION"
V2736D_ROLE_CLOSURE = "CLOSURE"


@dataclass(frozen=True)
class V2736DCommitFact:
    commit_sha: str
    changed_files: frozenset[str]
    task_state: str


@dataclass(frozen=True)
class V2736DHistoryState:
    state: str
    implementation_commit: str | None
    roles: tuple[str, ...]
    gate_commits: tuple[str, ...]


@dataclass(frozen=True)
class V2736DWorkingTreeFact:
    branch: str
    head: str
    origin_main: str
    diff_files: frozenset[str]
    staged_files: frozenset[str]
    untracked_files: frozenset[str]
    status_lines: frozenset[str]
    implementation_files_existing: frozenset[str]
    implementation_files_tracked_at_base: frozenset[str]
    implementation_files_tracked_at_head: frozenset[str]
    base_is_head_ancestor: bool
    base_is_origin_ancestor: bool
    origin_is_head_ancestor: bool


def validate_v2736c_completed_base() -> tuple[V2736CHistoryState, tuple[str, str, str, str]]:
    require(
        git_is_ancestor(V2736C_AUTHORIZATION_BASE_SHA, V2736D_AUTHORIZATION_BASE_SHA),
        "v27.36c-Basis ist kein Vorfahr des v27.36c-Closure-HEAD",
    )
    commit_facts = read_v2736c_commit_facts(V2736D_AUTHORIZATION_BASE_SHA)
    history = validate_v2736c_history_facts(commit_facts)
    require(history.state == V2736C_HISTORY_CLOSED, "v27.36c muss an der v27.36d-Basis vollständig geschlossen sein")
    require(history.implementation_commit is not None, "v27.36c benötigt an der v27.36d-Basis exakt eine IMPLEMENTATION")
    require(history.roles.count(V2736C_ROLE_IMPLEMENTATION) == 1, "v27.36c benötigt exakt einen IMPLEMENTATION-Commit")
    require(history.roles.count(V2736C_ROLE_CLOSURE) == 1 and history.roles[-1] == V2736C_ROLE_CLOSURE, "v27.36c-Closure muss exakt einmal und zuletzt vorliegen")
    require(commit_facts[-1].commit_sha == V2736D_AUTHORIZATION_BASE_SHA, "Verbindlicher v27.36c-Closure-HEAD wurde nicht erkannt")
    require(commit_facts[-1].changed_files == frozenset(EXPECTED_CONTROL_FILES), "v27.36c-Closure-HEAD muss exakt die fünf Gate-Dateien ändern")
    validate_v2736c_committed_closure_documents(commit_facts, history)
    validate_v2736c_source_contract_at_revision(history.implementation_commit)
    base_documents = (
        read_v2735f_commit_document(V2736D_AUTHORIZATION_BASE_SHA, "docs/PROJECT_STATE_CURRENT.md"),
        read_v2735f_commit_document(V2736D_AUTHORIZATION_BASE_SHA, V2735F_TASK_RELATIVE_PATH),
        read_v2735f_commit_document(V2736D_AUTHORIZATION_BASE_SHA, "docs/CURSOR_MASTER_CONTEXT_ACCAOUI.md"),
        read_v2735f_commit_document(V2736D_AUTHORIZATION_BASE_SHA, "docs/PROJECT_MASTERLIST.md"),
    )
    validate_v2736c_closed_documents(*base_documents, history.implementation_commit)
    return history, base_documents


def synthetic_v2736c_closed_working_fact() -> V2736CWorkingTreeFact:
    return V2736CWorkingTreeFact(
        branch="main",
        head=V2736D_AUTHORIZATION_BASE_SHA,
        origin_main=V2736D_AUTHORIZATION_BASE_SHA,
        diff_files=frozenset(),
        staged_files=frozenset(),
        untracked_files=frozenset(),
        status_lines=frozenset(),
        implementation_files_existing=V2736C_NEW_IMPLEMENTATION_FILES,
        implementation_files_tracked_at_base=frozenset(),
        implementation_files_tracked_at_head=V2736C_NEW_IMPLEMENTATION_FILES,
        base_is_head_ancestor=True,
        base_is_origin_ancestor=True,
        origin_is_head_ancestor=True,
    )


def validate_no_future_v2736d_sha(section: str, allowed_shas: frozenset[str], document_name: str) -> None:
    shas = frozenset(re.findall(r"\b[0-9a-f]{40}\b", section))
    require(
        shas.issubset(allowed_shas),
        f"{document_name}: zukünftige v27.36d-Commit-SHA hartcodiert: {sorted(shas - allowed_shas)}",
    )
    require(
        re.search(r"\bv27\.(?:36[e-z]|3[7-9])\b", section, re.IGNORECASE) is None,
        f"{document_name}: automatischer Folgetask nach v27.36d unzulässig",
    )


def validate_v2736d_supabase_not_live_statement(text: str) -> None:
    require(
        V2736D_SUPABASE_NOT_LIVE_PATTERN.search(text) is not None,
        "v27.36d-Pflichtaussage fehlt oder wurde verändert: Supabase bleibt NICHT LIVE.",
    )


def validate_v2736d_permanent_masterlist_contract(text: str) -> None:
    require(exact_field(text, "Arbeits-Laptop") == f"`{V2736C_VERIFIED_WORK_PATH}`", "PROJECT_MASTERLIST: verifizierter Arbeits-Laptop-Pfad fehlt")
    require(exact_field(text, "Git Bash Arbeits-Laptop") == f"`{V2736C_VERIFIED_WORK_PATH_GIT_BASH}`", "PROJECT_MASTERLIST: verifizierter Git-Bash-Arbeits-Laptop-Pfad fehlt")
    require(text.count("### Arbeits-, Produkt- und Übergabemodus") == 1, "PROJECT_MASTERLIST: Arbeits-, Produkt- und Übergabemodus muss exakt einmal vorkommen")
    require(text.count("### Commit-/Push-Freigabe bei autorisierten Lifecycle-Schritten") == 1, "PROJECT_MASTERLIST: Commit-/Push-Freigaberegel muss exakt einmal vorkommen")
    permanent_section = section_between(
        text,
        "### Commit-/Push-Freigabe bei autorisierten Lifecycle-Schritten",
        "## 2. Cursor-Regel",
        "PROJECT_MASTERLIST / Commit-/Push-Regel",
    )
    validate_required_markers(permanent_section, V2736D_PERMANENT_MASTERLIST_MODE_MARKERS, "PROJECT_MASTERLIST / Commit-/Push-Regel")


def remove_v2736d_permanent_masterlist_marker(text: str, marker: str) -> str:
    start_heading = "### Commit-/Push-Freigabe bei autorisierten Lifecycle-Schritten"
    end_heading = "## 2. Cursor-Regel"
    start = text.find(start_heading)
    end = text.find(end_heading, start + len(start_heading))
    require(start >= 0 and end > start, "Manipulationsmatrix kann permanenten v27.36d-Vertragsbereich nicht abgrenzen")
    section = text[start:end]
    require(marker in section, f"Manipulationsmatrix kann permanente Pflichtregel im Vertragsbereich nicht finden: {marker}")
    manipulated_section = section.replace(marker, "")
    require(marker not in manipulated_section, f"Manipulationsmatrix konnte permanente Pflichtregel im Vertragsbereich nicht vollständig entfernen: {marker}")
    return text[:start] + manipulated_section + text[end:]


def validate_v2736d_authorization_section(section: str, document_name: str, detailed_codes: bool = False) -> None:
    validate_required_markers(section, V2736D_AUTHORIZATION_MARKERS, f"{document_name} / v27.36d")
    if detailed_codes:
        validate_required_markers(section, V2736D_DETAILED_CODE_MARKERS, f"{document_name} / v27.36d-Codeabbildung")
    validate_v2736d_supabase_not_live_statement(section)
    validate_no_future_v2736d_sha(section, frozenset({V2736D_AUTHORIZATION_BASE_SHA}), f"{document_name} / v27.36d")
    for path in V2736D_IMPLEMENTATION_FILES:
        require(section.count(f"`{path}`") == 1, f"{document_name}: v27.36d-Datei fehlt oder ist doppelt: {path}")


def validate_v2736d_state_text(text: str) -> None:
    validate_exact_fields(text, V2736D_EXPECTED_STATE_FIELDS)
    section = section_between(text, "## Autorisierter Task v27.36d", "## Abgeschlossener isolierter Technikschritt v27.36c", "PROJECT_STATE_CURRENT")
    validate_v2736d_authorization_section(section, "PROJECT_STATE_CURRENT", detailed_codes=True)


def validate_v2736d_task_text(text: str) -> None:
    validate_exact_fields(text, V2736D_EXPECTED_TASK_FIELDS)
    require(text.count(f"Erlaubte Implementierungsdateien: {V2736D_ALLOWED_FILES_VALUE}") == 1, "CURRENT_TASK muss exakt eine verbindliche v27.36d-Dateifreigabe enthalten")
    section = section_between(text, "## Autorisierter Task v27.36d", "## Abgeschlossener isolierter Technikschritt v27.36c", "CURRENT_TASK")
    validate_v2736d_authorization_section(section, "CURRENT_TASK", detailed_codes=True)


def validate_v2736d_cursor_text(text: str) -> None:
    require(exact_field(text, "Stand") == "v27.36d", "CURSOR-Kontext muss auf v27.36d stehen")
    validate_project_paths(text, "CURSOR_MASTER_CONTEXT_ACCAOUI")
    section = section_between(text, "## 14. Nächster sinnvoller Schritt", "## 15. Wenn ein neuer Chat beginnt", "CURSOR_MASTER_CONTEXT_ACCAOUI")
    validate_v2736d_authorization_section(section, "CURSOR_MASTER_CONTEXT_ACCAOUI")


def validate_v2736d_masterlist_text(text: str) -> None:
    require(exact_field(text, "Stand") == "v27.36d", "PROJECT_MASTERLIST muss auf v27.36d stehen")
    validate_v2736d_permanent_masterlist_contract(text)
    rows = re.findall(r"(?m)^\| v27\.36d \|.*$", text)
    require(len(rows) == 1 and "**autorisiert**" in rows[0], "PROJECT_MASTERLIST muss v27.36d exakt einmal als autorisiert führen")
    section = section_between(text, "## 14. Nächste sinnvolle Aufgaben", "## 15. Start in neuem Chat", "PROJECT_MASTERLIST")
    validate_v2736d_authorization_section(section, "PROJECT_MASTERLIST")


def detect_v2736d_task_state_text(text: str) -> str:
    task_id = exact_field(text, "Task-ID")
    if task_id == "v27.36d":
        validate_exact_fields(text, V2736D_EXPECTED_TASK_FIELDS)
        return V2736D_TASK_AUTHORIZED
    if task_id == "NONE":
        validate_exact_fields(text, V2736D_CLOSED_TASK_FIELDS)
        return V2736D_TASK_CLOSED
    raise ValidationError(f"Unzulässiger v27.36d-Taskzustand: {task_id}")


def validate_v2736d_closed_documents(
    state_text: str,
    task_text: str,
    cursor_text: str,
    masterlist_text: str,
    implementation_commit: str,
) -> None:
    require(re.fullmatch(r"[0-9a-f]{40}", implementation_commit) is not None, "v27.36d-Closure benötigt einen dynamisch erkannten Implementierungscommit")
    validate_exact_fields(state_text, V2736D_CLOSED_STATE_FIELDS)
    validate_exact_fields(task_text, V2736D_CLOSED_TASK_FIELDS)
    require(exact_field(cursor_text, "Stand") == "v27.36d", "CURSOR-Kontext muss nach v27.36d-Closure auf v27.36d stehen")
    require(exact_field(masterlist_text, "Stand") == "v27.36d", "PROJECT_MASTERLIST muss nach v27.36d-Closure auf v27.36d stehen")
    validate_project_paths(cursor_text, "CURSOR_MASTER_CONTEXT_ACCAOUI")
    validate_v2736d_permanent_masterlist_contract(masterlist_text)
    sections = (
        section_between(state_text, "## Abgeschlossener technischer Schritt v27.36d", "## Abgeschlossener isolierter Technikschritt v27.36c", "PROJECT_STATE_CURRENT"),
        section_between(task_text, "## Abgeschlossener technischer Schritt v27.36d", "## Abgeschlossener isolierter Technikschritt v27.36c", "CURRENT_TASK"),
        section_between(cursor_text, "## 14. Nächster sinnvoller Schritt", "## 15. Wenn ein neuer Chat beginnt", "CURSOR_MASTER_CONTEXT_ACCAOUI"),
        section_between(masterlist_text, "## 14. Nächste sinnvolle Aufgaben", "## 15. Start in neuem Chat", "PROJECT_MASTERLIST"),
    )
    for section, name in zip(sections, ("PROJECT_STATE_CURRENT", "CURRENT_TASK", "CURSOR_MASTER_CONTEXT_ACCAOUI", "PROJECT_MASTERLIST")):
        validate_required_markers(section, V2736D_CLOSURE_MARKERS, f"{name} / v27.36d-Closure")
        validate_v2736d_supabase_not_live_statement(section)
        require(section.count(f"Implementierungscommit: `{implementation_commit}`") == 1, f"{name}: dynamischer v27.36d-Implementierungscommit fehlt oder ist doppelt")
        validate_no_future_v2736d_sha(section, frozenset({V2736D_AUTHORIZATION_BASE_SHA, implementation_commit}), f"{name} / v27.36d-Closure")
        for path in V2736D_IMPLEMENTATION_FILES:
            require(section.count(f"`{path}`") == 1, f"{name}: v27.36d-Implementierungsdatei fehlt oder ist doppelt: {path}")
    rows = re.findall(r"(?m)^\| v27\.36d \|.*$", masterlist_text)
    require(len(rows) == 1 and "**erledigt**" in rows[0] and implementation_commit in rows[0], "PROJECT_MASTERLIST muss v27.36d nach Closure exakt einmal als erledigt führen")


def read_v2736d_commit_facts(current_head: str) -> tuple[V2736DCommitFact, ...]:
    commit_shas = tuple(line.strip() for line in run_git(["rev-list", "--reverse", f"{V2736D_AUTHORIZATION_BASE_SHA}..{current_head}"]).splitlines() if line.strip())
    previous = V2736D_AUTHORIZATION_BASE_SHA
    facts: list[V2736DCommitFact] = []
    for commit_sha in commit_shas:
        lineage = run_git(["rev-list", "--parents", "-n", "1", commit_sha]).split()
        require(len(lineage) == 2 and lineage[1] == previous, "v27.36d erlaubt nur eine lineare Historie ohne Merge-Commit")
        changed_files = frozenset(line.strip().replace("\\", "/") for line in run_git(["diff", "--name-only", previous, commit_sha]).splitlines() if line.strip())
        require(changed_files, f"Leerer v27.36d-Commit unzulässig: {commit_sha}")
        commit_task = read_v2735f_commit_document(commit_sha, V2735F_TASK_RELATIVE_PATH)
        facts.append(V2736DCommitFact(commit_sha, changed_files, detect_v2736d_task_state_text(commit_task)))
        previous = commit_sha
    return tuple(facts)


def validate_v2736d_history_facts(commit_facts: tuple[V2736DCommitFact, ...]) -> V2736DHistoryState:
    gate_files = frozenset(EXPECTED_CONTROL_FILES)
    roles: list[str] = []
    gate_commits: list[str] = []
    implementation_commit: str | None = None
    closed = False
    for fact in commit_facts:
        files = fact.changed_files
        if files == V2736D_IMPLEMENTATION_FILES:
            require(gate_commits, "v27.36d-IMPLEMENTATION vor Autorisierungs-GATE unzulässig")
            require(implementation_commit is None, "Mehr als ein v27.36d-IMPLEMENTATION-Commit unzulässig")
            require(not closed, "v27.36d-IMPLEMENTATION nach CLOSURE unzulässig")
            require(fact.task_state == V2736D_TASK_AUTHORIZED, "v27.36d-IMPLEMENTATION benötigt AUTHORIZED / Autorisiert JA")
            implementation_commit = fact.commit_sha
            roles.append(V2736D_ROLE_IMPLEMENTATION)
            continue
        require(files and files.issubset(gate_files), f"Fremde Datei in v27.36d-Commit {fact.commit_sha}: {sorted(files - gate_files)}")
        if fact.task_state == V2736D_TASK_AUTHORIZED:
            require(not closed, "Rückkehr zu v27.36d / AUTHORIZED nach CLOSURE unzulässig")
            gate_commits.append(fact.commit_sha)
            roles.append(V2736D_ROLE_GATE)
            continue
        require(implementation_commit is not None, "v27.36d-CLOSURE vor IMPLEMENTATION unzulässig")
        require(not closed, "Mehr als ein v27.36d-CLOSURE-Commit unzulässig")
        require(files == gate_files, "v27.36d-CLOSURE muss exakt die fünf Gate-Dateien ändern")
        closed = True
        roles.append(V2736D_ROLE_CLOSURE)
    state = (
        V2736D_HISTORY_CLOSED if closed else
        V2736D_HISTORY_IMPLEMENTED if implementation_commit is not None else
        V2736D_HISTORY_AUTHORIZED if gate_commits else
        V2736D_HISTORY_BEFORE_AUTHORIZATION
    )
    return V2736DHistoryState(state, implementation_commit, tuple(roles), tuple(gate_commits))


def read_v2736d_working_tree_fact() -> V2736DWorkingTreeFact:
    head = run_git(["rev-parse", "HEAD"]).strip()
    origin_main = run_git(["rev-parse", "origin/main"]).strip()

    def tracked_at(revision: str) -> frozenset[str]:
        return frozenset(line.strip().replace("\\", "/") for line in run_git(["ls-tree", "-r", "--name-only", revision, "--", *sorted(V2736D_NEW_IMPLEMENTATION_FILES)]).splitlines() if line.strip())

    return V2736DWorkingTreeFact(
        branch=run_git(["branch", "--show-current"]).strip(),
        head=head,
        origin_main=origin_main,
        diff_files=frozenset(line.strip().replace("\\", "/") for line in run_git(["diff", "--name-only"]).splitlines() if line.strip()),
        staged_files=frozenset(line.strip().replace("\\", "/") for line in run_git(["diff", "--cached", "--name-only"]).splitlines() if line.strip()),
        untracked_files=frozenset(line.strip().replace("\\", "/") for line in run_git(["ls-files", "--others", "--exclude-standard"]).splitlines() if line.strip()),
        status_lines=frozenset(line.replace("\\", "/") for line in run_git(["status", "--porcelain=v1", "--untracked-files=all"]).splitlines() if line),
        implementation_files_existing=frozenset(path for path in V2736D_NEW_IMPLEMENTATION_FILES if (ROOT / path).is_file()),
        implementation_files_tracked_at_base=tracked_at(V2736D_AUTHORIZATION_BASE_SHA),
        implementation_files_tracked_at_head=tracked_at(head),
        base_is_head_ancestor=git_is_ancestor(V2736D_AUTHORIZATION_BASE_SHA, head),
        base_is_origin_ancestor=git_is_ancestor(V2736D_AUTHORIZATION_BASE_SHA, origin_main),
        origin_is_head_ancestor=git_is_ancestor(origin_main, head),
    )


def validate_v2736d_working_tree_fact(fact: V2736DWorkingTreeFact) -> None:
    require(fact.branch == "main", "v27.36d-Lebenszyklus muss auf main laufen")
    require(fact.base_is_head_ancestor, "Die stabile v27.36d-Basis ist kein Vorfahr von HEAD")
    require(fact.base_is_origin_ancestor, "Die stabile v27.36d-Basis ist kein Vorfahr von origin/main")
    require(fact.origin_is_head_ancestor, "origin/main ist kein Vorfahr des lokalen v27.36d-HEAD")
    require(not fact.implementation_files_tracked_at_base, "Neue v27.36d-Implementierungsdateien dürfen an der Basis nicht existieren")
    require(not fact.staged_files, "v27.36d-Lebenszyklus darf nichts stagen")


def extract_added_lines(diff_text: str) -> str:
    return "\n".join(
        line[1:]
        for line in diff_text.splitlines()
        if line.startswith("+") and not line.startswith("+++")
    )


def validate_v2736d_source_contract(app_text: str, app_added_text: str, checker_text: str, report_text: str, preflight_text: str) -> None:
    for marker in (
        "ACCAOUI_PARTICIPANT_ACCESS_APP_PROVIDER", "resolveAccess", "access_allowed",
        "startLocalApp", "login_required", "blocked", "expired", "no_course",
    ):
        require(marker in app_text, f"v27.36d-App-Anbindung fehlt: {marker}")
    for marker in V2736D_DETAILED_CODE_MARKERS:
        require(marker in app_text, f"v27.36d-App-Codeabbildung fehlt: {marker}")
    forbidden_added_tokens = (
        ".from(", "getSession(", "createClient(", "initializeClient(",
        "getClient(", "getState(", "getConfig(", "fetch(", "XMLHttpRequest",
        "WebSocket", "globalThis", "global.", "require(", "module.exports",
        "supabase-participant-access-adapter", "supabase-participant-access-bootstrap-bridge",
        "supabase-client-bootstrap", "userId", "console.error", ".message",
    )
    added_folded = app_added_text.casefold()
    for token in forbidden_added_tokens:
        require(token.casefold() not in added_folded, f"v27.36d-App-Diff verletzt Anbindungsgrenze: {token}")
    for marker in (
        "synthet", "ACCAOUI_PARTICIPANT_ACCESS_APP_PROVIDER", "resolveAccess",
        "access_allowed", "startLocalApp", "login_required", "blocked",
        "expired", "no_course", "fail-closed", "Auth-Guard",
    ):
        require(marker.casefold() in checker_text.casefold(), f"v27.36d-Checker fehlt Testbindung: {marker}")
    for marker in (
        "Ziel", "Sicherheitsgrenze", "optionaler Provider", "resolveAccess()",
        "fail-closed", "lokaler synthetischer Provider", "getestete Fälle",
        "unveränderte Bestandsmodule", "Supabase live: NEIN",
        "echte Keys: NEIN", "echte Teilnehmerdaten: NEIN",
    ):
        require(marker in report_text, f"v27.36d-Umsetzungsbericht fehlt: {marker}")
    for required_checker in (
        "check-project-continuity-control.py",
        "check-supabase-participant-access-adapter.py",
        "check-supabase-participant-access-bootstrap-bridge.py",
        "check-participant-access-app-entry-v2736d.py",
    ):
        require(required_checker in preflight_text, f"Preflight-Pflichtchecker fehlt: {required_checker}")


def validate_v2736d_local_source_contract() -> None:
    app_diff = run_git(["diff", "--unified=0", V2736D_AUTHORIZATION_BASE_SHA, "--", "app.js"])
    validate_v2736d_source_contract(
        read_required_text(APP_JS_PATH),
        extract_added_lines(app_diff),
        read_required_text(ROOT / "tools/check-participant-access-app-entry-v2736d.py"),
        read_required_text(ROOT / "docs/PARTICIPANT_ACCESS_APP_ENTRY_V2736D.md"),
        read_required_text(PREFLIGHT_PATH),
    )


def validate_v2736d_source_contract_at_revision(revision: str) -> None:
    parent = run_git(["rev-parse", f"{revision}^"]).strip()
    app_diff = run_git(["diff", "--unified=0", parent, revision, "--", "app.js"])
    validate_v2736d_source_contract(
        read_v2735f_commit_document(revision, "app.js"),
        extract_added_lines(app_diff),
        read_v2735f_commit_document(revision, "tools/check-participant-access-app-entry-v2736d.py"),
        read_v2735f_commit_document(revision, "docs/PARTICIPANT_ACCESS_APP_ENTRY_V2736D.md"),
        read_v2735f_commit_document(revision, "tools/preflight.py"),
    )


def validate_v2736d_lifecycle_working_tree(history: V2736DHistoryState, task_state: str, fact: V2736DWorkingTreeFact) -> str:
    validate_v2736d_working_tree_fact(fact)
    gate_files = frozenset(EXPECTED_CONTROL_FILES)
    clean = not fact.diff_files and not fact.untracked_files and not fact.status_lines
    if history.state == V2736D_HISTORY_BEFORE_AUTHORIZATION:
        require(fact.head == V2736D_AUTHORIZATION_BASE_SHA, "Autorisierungsvorbereitung benötigt die stabile v27.36d-Basis als HEAD")
        require(task_state == V2736D_TASK_AUTHORIZED, "Autorisierungsvorbereitung benötigt v27.36d / AUTHORIZED")
        require(fact.diff_files == gate_files, "Autorisierungsvorbereitung muss exakt fünf Gate-Dateien ändern")
        require(not fact.untracked_files and fact.status_lines == frozenset(f" M {path}" for path in gate_files), "Working Tree entspricht nicht authorization_prepared")
        require(not fact.implementation_files_existing, "v27.36d-Implementation vor Autorisierungscommit unzulässig")
        return V2736D_PHASE_AUTHORIZATION_PREPARED
    if history.state == V2736D_HISTORY_AUTHORIZED:
        require(fact.head != V2736D_AUTHORIZATION_BASE_SHA, "Autorisierungscommit fehlt")
        require(task_state == V2736D_TASK_AUTHORIZED, "Autorisierte Phasen benötigen v27.36d / AUTHORIZED")
        require(not fact.implementation_files_tracked_at_head, "Neue v27.36d-Dateien dürfen vor IMPLEMENTATION nicht getrackt sein")
        if clean:
            require(not fact.implementation_files_existing, "Implementation darf vor preparation nicht lokal existieren")
            return V2736D_PHASE_AUTHORIZATION_COMMITTED
        if fact.diff_files and fact.diff_files.issubset(gate_files) and not fact.untracked_files:
            require(fact.status_lines == frozenset(f" M {path}" for path in fact.diff_files), "Lokale v27.36d-Gate-Korrektur enthält fremden Status")
            require(not fact.implementation_files_existing, "Implementation während Gate-Korrektur unzulässig")
            return V2736D_PHASE_AUTHORIZATION_COMMITTED
        require(fact.diff_files == frozenset({"app.js", "tools/preflight.py"}), "implementation_prepared muss exakt app.js und tools/preflight.py ändern")
        require(fact.untracked_files == V2736D_NEW_IMPLEMENTATION_FILES, "implementation_prepared benötigt exakt zwei neue Implementierungsdateien")
        require(fact.implementation_files_existing == V2736D_NEW_IMPLEMENTATION_FILES, "implementation_prepared benötigt beide neuen Dateien")
        expected_status = frozenset({" M app.js", " M tools/preflight.py", *(f"?? {path}" for path in V2736D_NEW_IMPLEMENTATION_FILES)})
        require(fact.status_lines == expected_status, "Working Tree entspricht nicht implementation_prepared")
        return V2736D_PHASE_IMPLEMENTATION_PREPARED
    require(history.implementation_commit is not None, "Phase nach IMPLEMENTATION benötigt den dynamischen Implementierungscommit")
    require(fact.implementation_files_tracked_at_head == V2736D_NEW_IMPLEMENTATION_FILES, "Nach IMPLEMENTATION müssen beide neuen Dateien getrackt sein")
    require(fact.implementation_files_existing == V2736D_NEW_IMPLEMENTATION_FILES, "Nach IMPLEMENTATION müssen beide neuen Dateien vorhanden sein")
    if history.state == V2736D_HISTORY_IMPLEMENTED:
        if task_state == V2736D_TASK_AUTHORIZED:
            if clean:
                return V2736D_PHASE_IMPLEMENTATION_COMMITTED
            require(fact.diff_files and fact.diff_files.issubset(gate_files) and not fact.untracked_files, "Nach IMPLEMENTATION sind lokal nur Gate-Korrekturen oder Closure zulässig")
            require(fact.status_lines == frozenset(f" M {path}" for path in fact.diff_files), "Lokale Gate-Korrektur nach IMPLEMENTATION enthält fremden Status")
            return V2736D_PHASE_IMPLEMENTATION_COMMITTED
        require(task_state == V2736D_TASK_CLOSED, "closure_prepared benötigt den geschlossenen v27.36d-Taskzustand")
        require(fact.diff_files == gate_files and not fact.untracked_files, "closure_prepared muss exakt fünf Gate-Dateien ändern")
        require(fact.status_lines == frozenset(f" M {path}" for path in gate_files), "Working Tree entspricht nicht closure_prepared")
        return V2736D_PHASE_CLOSURE_PREPARED
    require(history.state == V2736D_HISTORY_CLOSED, "Unbekannter v27.36d-Historienzustand")
    require(task_state == V2736D_TASK_CLOSED, "Nach v27.36d-CLOSURE darf keine Rückkehr zu AUTHORIZED erfolgen")
    require(clean, "closure_committed benötigt einen sauberen Working Tree")
    return V2736D_PHASE_CLOSURE_COMMITTED


def validate_v2736d_committed_closure_documents(facts: tuple[V2736DCommitFact, ...], history: V2736DHistoryState) -> None:
    if V2736D_ROLE_CLOSURE not in history.roles:
        return
    require(history.implementation_commit is not None, "v27.36d-CLOSURE benötigt einen dynamischen Implementierungscommit")
    for fact, role in zip(facts, history.roles):
        if role == V2736D_ROLE_CLOSURE:
            validate_v2736d_closed_documents(
                read_v2735f_commit_document(fact.commit_sha, "docs/PROJECT_STATE_CURRENT.md"),
                read_v2735f_commit_document(fact.commit_sha, V2735F_TASK_RELATIVE_PATH),
                read_v2735f_commit_document(fact.commit_sha, "docs/CURSOR_MASTER_CONTEXT_ACCAOUI.md"),
                read_v2735f_commit_document(fact.commit_sha, "docs/PROJECT_MASTERLIST.md"),
                history.implementation_commit,
            )


def validate_v2736d_lifecycle(state_text: str, task_text: str, cursor_text: str, masterlist_text: str) -> tuple[str, V2736DHistoryState, V2736DWorkingTreeFact]:
    fact = read_v2736d_working_tree_fact()
    validate_v2736d_working_tree_fact(fact)
    commit_facts = read_v2736d_commit_facts(fact.head)
    history = validate_v2736d_history_facts(commit_facts)
    validate_v2736d_committed_closure_documents(commit_facts, history)
    task_state = detect_v2736d_task_state_text(task_text)
    if task_state == V2736D_TASK_AUTHORIZED:
        validate_v2736d_state_text(state_text)
        validate_v2736d_task_text(task_text)
        validate_v2736d_cursor_text(cursor_text)
        validate_v2736d_masterlist_text(masterlist_text)
    else:
        require(history.implementation_commit is not None, "v27.36d-Abschluss vor IMPLEMENTATION unzulässig")
        validate_v2736d_closed_documents(state_text, task_text, cursor_text, masterlist_text, history.implementation_commit)
    phase = validate_v2736d_lifecycle_working_tree(history, task_state, fact)
    if phase == V2736D_PHASE_IMPLEMENTATION_PREPARED:
        validate_v2736d_local_source_contract()
    if history.implementation_commit is not None:
        validate_v2736d_source_contract_at_revision(history.implementation_commit)
    return phase, history, fact


def run_v2736d_manipulation_matrix(
    state_text: str,
    task_text: str,
    cursor_text: str,
    masterlist_text: str,
    current_history: V2736DHistoryState,
    current_fact: V2736DWorkingTreeFact,
) -> tuple[int, int, int]:
    checks = 0

    def must_reject(validator: Callable[[str], None], manipulated: str, label: str) -> None:
        nonlocal checks
        try:
            validator(manipulated)
        except ValidationError:
            checks += 1
            return
        raise ValidationError(f"v27.36d-Dokumentmanipulation wurde nicht blockiert: {label}")

    def remove_authorization_marker(text: str, marker: str, name: str) -> str:
        boundaries = {
            "PROJECT_STATE_CURRENT": (
                "## Autorisierter Task v27.36d",
                "## Abgeschlossener isolierter Technikschritt v27.36c",
            ),
            "CURRENT_TASK": (
                "## Autorisierter Task v27.36d",
                "## Abgeschlossener isolierter Technikschritt v27.36c",
            ),
            "CURSOR_MASTER_CONTEXT_ACCAOUI": (
                "## 14. Nächster sinnvoller Schritt",
                "## 15. Wenn ein neuer Chat beginnt",
            ),
            "PROJECT_MASTERLIST": (
                "## 14. Nächste sinnvolle Aufgaben",
                "## 15. Start in neuem Chat",
            ),
        }
        start_marker, end_marker = boundaries[name]
        start = text.find(start_marker)
        end = text.find(end_marker, start + len(start_marker))
        require(start >= 0 and end > start, f"Manipulationsmatrix kann v27.36d-Vertragsbereich nicht abgrenzen: {name}")
        section = text[start:end]
        require(marker in section, f"Manipulationsmatrix kann v27.36d-Pflichtaussage im Vertragsbereich nicht finden: {name} / {marker}")
        manipulated_section = section.replace(marker, "")
        require(marker not in manipulated_section, f"Manipulationsmatrix konnte v27.36d-Pflichtaussage nicht vollständig entfernen: {name} / {marker}")
        return text[:start] + manipulated_section + text[end:]

    current_task_state = detect_v2736d_task_state_text(task_text)
    authorization_documents = (state_text, task_text, cursor_text, masterlist_text)
    if current_task_state == V2736D_TASK_CLOSED:
        require(current_history.gate_commits, "v27.36d-Closure benötigt einen historischen Autorisierungs-GATE")
        authorization_revision = current_history.gate_commits[-1]
        authorization_documents = (
            read_v2735f_commit_document(authorization_revision, "docs/PROJECT_STATE_CURRENT.md"),
            read_v2735f_commit_document(authorization_revision, V2735F_TASK_RELATIVE_PATH),
            read_v2735f_commit_document(authorization_revision, "docs/CURSOR_MASTER_CONTEXT_ACCAOUI.md"),
            read_v2735f_commit_document(authorization_revision, "docs/PROJECT_MASTERLIST.md"),
        )
    auth_state_text, auth_task_text, auth_cursor_text, auth_masterlist_text = authorization_documents

    for text, validator, fields, name in (
        (auth_state_text, validate_v2736d_state_text, V2736D_EXPECTED_STATE_FIELDS, "PROJECT_STATE_CURRENT"),
        (auth_task_text, validate_v2736d_task_text, V2736D_EXPECTED_TASK_FIELDS, "CURRENT_TASK"),
    ):
        for field, expected in fields.items():
            must_reject(validator, text.replace(f"{field}: {expected}", f"{field}: MANIPULIERT", 1), f"{name}: Feld {field}")
    for text, validator, name in (
        (auth_state_text, validate_v2736d_state_text, "PROJECT_STATE_CURRENT"),
        (auth_task_text, validate_v2736d_task_text, "CURRENT_TASK"),
        (auth_cursor_text, validate_v2736d_cursor_text, "CURSOR_MASTER_CONTEXT_ACCAOUI"),
        (auth_masterlist_text, validate_v2736d_masterlist_text, "PROJECT_MASTERLIST"),
    ):
        for marker in V2736D_AUTHORIZATION_MARKERS:
            manipulated = remove_authorization_marker(text, marker, name)
            must_reject(validator, manipulated, f"{name}: Pflichtaussage {marker}")
    for marker in V2736D_PERMANENT_MASTERLIST_MODE_MARKERS:
        require(marker in auth_masterlist_text, f"Manipulationsmatrix kann permanente Pflichtregel nicht finden: {marker}")
        must_reject(
            validate_v2736d_masterlist_text,
            remove_v2736d_permanent_masterlist_marker(auth_masterlist_text, marker),
            f"PROJECT_MASTERLIST: permanente Regel {marker}",
        )

    if current_task_state == V2736D_TASK_CLOSED:
        require(current_history.implementation_commit is not None, "v27.36d-Closure-Manipulationsprüfung benötigt den Implementierungscommit")
        closure_documents = (state_text, task_text, cursor_text, masterlist_text)
        closure_names = (
            "PROJECT_STATE_CURRENT",
            "CURRENT_TASK",
            "CURSOR_MASTER_CONTEXT_ACCAOUI",
            "PROJECT_MASTERLIST",
        )
        closure_boundaries = {
            "PROJECT_STATE_CURRENT": (
                "## Abgeschlossener technischer Schritt v27.36d",
                "## Abgeschlossener isolierter Technikschritt v27.36c",
            ),
            "CURRENT_TASK": (
                "## Abgeschlossener technischer Schritt v27.36d",
                "## Abgeschlossener isolierter Technikschritt v27.36c",
            ),
            "CURSOR_MASTER_CONTEXT_ACCAOUI": (
                "## 14. Nächster sinnvoller Schritt",
                "## 15. Wenn ein neuer Chat beginnt",
            ),
            "PROJECT_MASTERLIST": (
                "## 14. Nächste sinnvolle Aufgaben",
                "## 15. Start in neuem Chat",
            ),
        }

        def validate_closed_variant(index: int, manipulated: str) -> None:
            documents = list(closure_documents)
            documents[index] = manipulated
            validate_v2736d_closed_documents(
                *documents,
                current_history.implementation_commit,
            )

        def remove_closure_marker(text: str, marker: str, name: str) -> str:
            start_marker, end_marker = closure_boundaries[name]
            start = text.find(start_marker)
            end = text.find(end_marker, start + len(start_marker))
            require(start >= 0 and end > start, f"Manipulationsmatrix kann v27.36d-Closure-Bereich nicht abgrenzen: {name}")
            section = text[start:end]
            require(marker in section, f"Manipulationsmatrix kann v27.36d-Closure-Pflichtaussage nicht finden: {name} / {marker}")
            manipulated_section = section.replace(marker, "")
            require(marker not in manipulated_section, f"Manipulationsmatrix konnte v27.36d-Closure-Pflichtaussage nicht vollständig entfernen: {name} / {marker}")
            return text[:start] + manipulated_section + text[end:]

        for index, (text, fields, name) in enumerate((
            (state_text, V2736D_CLOSED_STATE_FIELDS, "PROJECT_STATE_CURRENT"),
            (task_text, V2736D_CLOSED_TASK_FIELDS, "CURRENT_TASK"),
        )):
            for field, expected in fields.items():
                marker = f"{field}: {expected}"
                require(marker in text, f"Manipulationsmatrix kann geschlossenes v27.36d-Feld nicht finden: {name} / {field}")
                must_reject(
                    lambda manipulated, index=index: validate_closed_variant(index, manipulated),
                    text.replace(marker, f"{field}: MANIPULIERT", 1),
                    f"{name}: geschlossenes Feld {field}",
                )
        closure_commit_marker = f"Implementierungscommit: `{current_history.implementation_commit}`"
        for index, (text, name) in enumerate(zip(closure_documents, closure_names)):
            for marker in (*V2736D_CLOSURE_MARKERS, closure_commit_marker, *(f"`{path}`" for path in V2736D_IMPLEMENTATION_FILES)):
                manipulated = remove_closure_marker(text, marker, name)
                must_reject(
                    lambda candidate, index=index: validate_closed_variant(index, candidate),
                    manipulated,
                    f"{name}: Closure-Pflichtaussage {marker}",
                )
        for marker in V2736D_PERMANENT_MASTERLIST_MODE_MARKERS:
            require(marker in masterlist_text, f"Manipulationsmatrix kann permanente Closure-Pflichtregel nicht finden: {marker}")
            must_reject(
                lambda manipulated: validate_closed_variant(3, manipulated),
                remove_v2736d_permanent_masterlist_marker(masterlist_text, marker),
                f"PROJECT_MASTERLIST: permanente Closure-Regel {marker}",
            )

    gate = V2736DCommitFact("1" * 40, frozenset({EXPECTED_CONTROL_FILES[0]}), V2736D_TASK_AUTHORIZED)
    implementation = V2736DCommitFact("2" * 40, V2736D_IMPLEMENTATION_FILES, V2736D_TASK_AUTHORIZED)
    closure = V2736DCommitFact("3" * 40, frozenset(EXPECTED_CONTROL_FILES), V2736D_TASK_CLOSED)
    histories = (
        validate_v2736d_history_facts(tuple()),
        validate_v2736d_history_facts((gate,)),
        validate_v2736d_history_facts((gate, implementation)),
        validate_v2736d_history_facts((gate, implementation, closure)),
    )
    clean_fact = replace(
        current_fact,
        head="1" * 40,
        diff_files=frozenset(), staged_files=frozenset(), untracked_files=frozenset(), status_lines=frozenset(),
        implementation_files_existing=frozenset(), implementation_files_tracked_at_base=frozenset(), implementation_files_tracked_at_head=frozenset(),
        base_is_head_ancestor=True, base_is_origin_ancestor=True, origin_is_head_ancestor=True,
    )
    gate_files = frozenset(EXPECTED_CONTROL_FILES)
    implemented_fact = replace(clean_fact, head="2" * 40, implementation_files_existing=V2736D_NEW_IMPLEMENTATION_FILES, implementation_files_tracked_at_head=V2736D_NEW_IMPLEMENTATION_FILES)
    implementation_status = frozenset({" M app.js", " M tools/preflight.py", *(f"?? {path}" for path in V2736D_NEW_IMPLEMENTATION_FILES)})
    phase_fixtures = (
        (histories[0], V2736D_TASK_AUTHORIZED, replace(clean_fact, head=V2736D_AUTHORIZATION_BASE_SHA, diff_files=gate_files, status_lines=frozenset(f" M {p}" for p in gate_files)), V2736D_PHASE_AUTHORIZATION_PREPARED),
        (histories[1], V2736D_TASK_AUTHORIZED, clean_fact, V2736D_PHASE_AUTHORIZATION_COMMITTED),
        (histories[1], V2736D_TASK_AUTHORIZED, replace(clean_fact, diff_files=frozenset({"app.js", "tools/preflight.py"}), untracked_files=V2736D_NEW_IMPLEMENTATION_FILES, status_lines=implementation_status, implementation_files_existing=V2736D_NEW_IMPLEMENTATION_FILES), V2736D_PHASE_IMPLEMENTATION_PREPARED),
        (histories[2], V2736D_TASK_AUTHORIZED, implemented_fact, V2736D_PHASE_IMPLEMENTATION_COMMITTED),
        (histories[2], V2736D_TASK_CLOSED, replace(implemented_fact, diff_files=gate_files, status_lines=frozenset(f" M {p}" for p in gate_files)), V2736D_PHASE_CLOSURE_PREPARED),
        (histories[3], V2736D_TASK_CLOSED, implemented_fact, V2736D_PHASE_CLOSURE_COMMITTED),
    )
    for history, task_state, fact, expected in phase_fixtures:
        require(validate_v2736d_lifecycle_working_tree(history, task_state, fact) == expected, f"v27.36d-Positivsimulation fehlgeschlagen: {expected}")
    positive_tests = len(phase_fixtures)

    bad_histories = (
        ((implementation,), "Implementation vor Autorisierung"),
        ((gate, implementation, implementation), "zweite Implementation"),
        ((gate, closure), "Closure vor Implementation"),
        ((gate, implementation, closure, gate), "Rückkehr nach Closure"),
        ((gate, implementation, V2736DCommitFact("4" * 40, frozenset({EXPECTED_CONTROL_FILES[0]}), V2736D_TASK_CLOSED)), "partielle Closure"),
        ((gate, V2736DCommitFact("5" * 40, frozenset(set(V2736D_IMPLEMENTATION_FILES) - {"tools/preflight.py"}), V2736D_TASK_AUTHORIZED)), "partielle Implementation"),
        ((gate, V2736DCommitFact("6" * 40, V2736D_IMPLEMENTATION_FILES | {"index.html"}, V2736D_TASK_AUTHORIZED)), "Implementation mit Zusatzdatei"),
        ((V2736DCommitFact("7" * 40, frozenset({"data/supabase-participant-access-adapter.js"}), V2736D_TASK_AUTHORIZED),), "Bestandsadapter geändert"),
        ((V2736DCommitFact("8" * 40, frozenset({"data/supabase-participant-access-bootstrap-bridge.js"}), V2736D_TASK_AUTHORIZED),), "Bestandsbrücke geändert"),
        ((V2736DCommitFact("9" * 40, frozenset({"index.html"}), V2736D_TASK_AUTHORIZED),), "index.html geändert"),
    )
    for facts, label in bad_histories:
        try:
            validate_v2736d_history_facts(facts)
        except ValidationError:
            checks += 1
            continue
        raise ValidationError(f"v27.36d-Historienmanipulation wurde nicht blockiert: {label}")

    bad_working = (
        (current_history, V2736D_TASK_AUTHORIZED, replace(current_fact, staged_files=frozenset({EXPECTED_CONTROL_FILES[0]})), "gestagte Datei"),
        (current_history, V2736D_TASK_AUTHORIZED, replace(current_fact, diff_files=current_fact.diff_files | {"index.html"}, status_lines=current_fact.status_lines | {" M index.html"}), "fremde lokale Datei"),
        (current_history, V2736D_TASK_AUTHORIZED, replace(current_fact, untracked_files=frozenset({"unexpected.txt"}), status_lines=current_fact.status_lines | {"?? unexpected.txt"}), "fremde ungetrackte Datei"),
        (current_history, V2736D_TASK_AUTHORIZED, replace(current_fact, base_is_head_ancestor=False), "falsche Basis"),
        (current_history, V2736D_TASK_AUTHORIZED, replace(current_fact, origin_is_head_ancestor=False), "origin nicht Vorfahr"),
        (current_history, V2736D_TASK_AUTHORIZED, replace(current_fact, implementation_files_tracked_at_base=V2736D_NEW_IMPLEMENTATION_FILES), "Implementierungsdateien bereits an Basis"),
        (histories[0], V2736D_TASK_AUTHORIZED, replace(clean_fact, head=V2736D_AUTHORIZATION_BASE_SHA, untracked_files=V2736D_NEW_IMPLEMENTATION_FILES, status_lines=frozenset(f"?? {p}" for p in V2736D_NEW_IMPLEMENTATION_FILES), implementation_files_existing=V2736D_NEW_IMPLEMENTATION_FILES), "Implementation lokal vor Autorisierung"),
        (histories[1], V2736D_TASK_CLOSED, replace(clean_fact, diff_files=gate_files, status_lines=frozenset(f" M {p}" for p in gate_files)), "Closure lokal vor Implementation"),
        (histories[3], V2736D_TASK_AUTHORIZED, implemented_fact, "Rückkehr zu AUTHORIZED nach Closure"),
    )
    for history, task_state, fact, label in bad_working:
        try:
            validate_v2736d_lifecycle_working_tree(history, task_state, fact)
        except ValidationError:
            checks += 1
            continue
        raise ValidationError(f"v27.36d-Working-Tree-Manipulation wurde nicht blockiert: {label}")

    valid_app = "ACCAOUI_PARTICIPANT_ACCESS_APP_PROVIDER resolveAccess access_allowed startLocalApp login_required blocked expired no_course " + " ".join(V2736D_DETAILED_CODE_MARKERS)
    valid_checker = "synthetischer ACCAOUI_PARTICIPANT_ACCESS_APP_PROVIDER resolveAccess access_allowed startLocalApp login_required blocked expired no_course fail-closed Auth-Guard"
    valid_report = "\n".join(("Ziel", "Sicherheitsgrenze", "optionaler Provider", "resolveAccess()", "fail-closed", "lokaler synthetischer Provider", "getestete Fälle", "unveränderte Bestandsmodule", "Supabase live: NEIN", "echte Keys: NEIN", "echte Teilnehmerdaten: NEIN"))
    valid_preflight = "check-project-continuity-control.py check-supabase-participant-access-adapter.py check-supabase-participant-access-bootstrap-bridge.py check-participant-access-app-entry-v2736d.py"
    validate_v2736d_source_contract(valid_app, "window.ACCAOUI_PARTICIPANT_ACCESS_APP_PROVIDER resolveAccess", valid_checker, valid_report, valid_preflight)
    for token in (".from(", "getSession(", "createClient(", "getClient(", "fetch(", "require(", "userId", "console.error"):
        try:
            validate_v2736d_source_contract(valid_app, f"window.ACCAOUI_PARTICIPANT_ACCESS_APP_PROVIDER {token}", valid_checker, valid_report, valid_preflight)
        except ValidationError:
            checks += 1
            continue
        raise ValidationError(f"v27.36d-Quellmanipulation wurde nicht blockiert: {token}")
    negative_tests = len(bad_histories) + len(bad_working) + 8
    return checks, positive_tests, negative_tests


V2736E_AUTHORIZATION_BASE_SHA = "1f7d8b0bf6784227b7211d3fb56d714d73c58d4c"
V2736E_TITLE = "Browser-Anbindungsweg für die bestehende Teilnehmerzugangskette lokal vorbereiten"
V2736E_IMPLEMENTATION_FILES = frozenset(
    {
        "data/supabase-participant-access-adapter.js",
        "data/supabase-participant-access-bootstrap-bridge.js",
        "data/supabase-participant-access-browser-provider.js",
        "tools/check-participant-access-browser-provider-v2736e.py",
        "docs/PARTICIPANT_ACCESS_BROWSER_PROVIDER_V2736E.md",
        "tools/preflight.py",
    }
)
V2736E_NEW_IMPLEMENTATION_FILES = frozenset(
    {
        "data/supabase-participant-access-browser-provider.js",
        "tools/check-participant-access-browser-provider-v2736e.py",
        "docs/PARTICIPANT_ACCESS_BROWSER_PROVIDER_V2736E.md",
    }
)
V2736E_EXISTING_IMPLEMENTATION_FILES = frozenset(
    V2736E_IMPLEMENTATION_FILES - V2736E_NEW_IMPLEMENTATION_FILES
)
V2736E_ALLOWED_FILES_VALUE = (
    "`data/supabase-participant-access-adapter.js`, "
    "`data/supabase-participant-access-bootstrap-bridge.js`, "
    "`data/supabase-participant-access-browser-provider.js`, "
    "`tools/check-participant-access-browser-provider-v2736e.py`, "
    "`docs/PARTICIPANT_ACCESS_BROWSER_PROVIDER_V2736E.md`, `tools/preflight.py`"
)
V2736E_EXPECTED_STATE_FIELDS = {
    "Stand": "v27.36e",
    "Repository": "`asarrad-bit/accaoui-34a-lernapp`",
    "Branch": "`main`",
    "Letzter abgeschlossener funktionaler Stand": "v27.35g",
    "Abschlusscommit": f"`{V2735G_COMPLETION_SHA}`",
    "Aktueller HEAD": "DYNAMISCH ZU PRÜFEN",
    "Funktionsstatus": "v27.35g abgeschlossen",
    "Weiterer funktionaler Schritt autorisiert": "JA",
    "Aktuell autorisierter Task": "v27.36e",
    "Aktuelle Taskart": "Lokaler Browser-Anbindungsweg der Teilnehmerzugangskette",
    "Aktueller Blocker": (
        "KEINER für die ausdrücklich autorisierte spätere v27.36e-Umsetzung; "
        "in diesem Autorisierungs-GATE erfolgt noch keine Implementierung"
    ),
}
V2736E_EXPECTED_TASK_FIELDS = {
    "Task-ID": "v27.36e",
    "Status": "AUTHORIZED",
    "Autorisiert": "JA",
    "Titel": V2736E_TITLE,
    "Funktionaler Ausgangsstand": "v27.35g",
    "Technischer Ausgangsstand": "v27.36d vollständig abgeschlossen",
    "Stabile Autorisierungsbasis": f"`{V2736E_AUTHORIZATION_BASE_SHA}`",
    "Erlaubte Implementierungsdateien": V2736E_ALLOWED_FILES_VALUE,
    "Commit erlaubt": "NEIN",
    "Push erlaubt": "NEIN",
}
V2736E_CLOSED_STATE_FIELDS = {
    "Stand": "v27.36e",
    "Repository": "`asarrad-bit/accaoui-34a-lernapp`",
    "Branch": "`main`",
    "Letzter abgeschlossener funktionaler Stand": "v27.35g",
    "Abschlusscommit": f"`{V2735G_COMPLETION_SHA}`",
    "Aktueller HEAD": "DYNAMISCH ZU PRÜFEN",
    "Funktionsstatus": "v27.35g abgeschlossen",
    "Weiterer funktionaler Schritt autorisiert": "NEIN",
    "Aktuell autorisierter Task": "NONE",
    "Aktuelle Taskart": "Kein Task autorisiert",
    "Aktueller Blocker": (
        "Neue Taskauswahl und ausdrückliche Autorisierung durch "
        "Projekteigentümer und verbindlichen Projektchat"
    ),
}
V2736E_CLOSED_TASK_FIELDS = {
    "Task-ID": "NONE",
    "Status": "BLOCKED",
    "Autorisiert": "NEIN",
    "Titel": "Kein Task autorisiert",
    "Funktionaler Ausgangsstand": "v27.35g",
    "Letzter abgeschlossener Kontrollschritt": "v27.36e",
    "Erlaubte Implementierungsdateien": "KEINE",
    "Commit erlaubt": "NEIN",
    "Push erlaubt": "NEIN",
}
V2736E_AUTHORIZATION_MARKERS = (
    "v27.36e ist der einzige autorisierte Task",
    V2736E_TITLE,
    "Dieser GATE-Schritt autorisiert nur die spätere Umsetzung",
    "Funktionaler Ausgangsstand: v27.35g.",
    "Technischer Ausgangsstand: v27.36d vollständig abgeschlossen.",
    f"Stabile Autorisierungsbasis: `{V2736E_AUTHORIZATION_BASE_SHA}`.",
    "Für die spätere IMPLEMENTATION sind exakt sechs Dateien erlaubt:",
    "App -> `window.ACCAOUI_PARTICIPANT_ACCESS_APP_PROVIDER`",
    "bestehende v27.36c-Brücke",
    "v27.36b-Adapter-Factory",
    "CommonJS-Kompatibilität",
    "kleine kontrollierte browserkompatible Exportoberfläche",
    "`window.ACCAOUI_PARTICIPANT_ACCESS_ADAPTER_FACTORY`",
    "`window.ACCAOUI_PARTICIPANT_ACCESS_BOOTSTRAP_BRIDGE_FACTORY`",
    "Keine Fachlogik wird dupliziert.",
    "ausschließlich `resolveAccess()`",
    "`window.ACCAOUI_SUPABASE_BOOTSTRAP`",
    "lokale UTC-Zeitquelle",
    "`bootstrap.getClient()` wird ausschließlich durch die bestehende Brücke verwendet.",
    "fail-closed",
    "interne Rohfehler werden nicht ausgegeben",
    "`bootstrap.initializeClient()`",
    "`bootstrap.getState()`",
    "`supabase.createClient()`",
    "frei injizierte `userId`",
    "`index.html`, `app.js` und `style.css` bleiben unverändert",
    "Der lokale App-Start bleibt unverändert.",
    "Supabase bleibt NICHT LIVE.",
    "Keine echten Keys.",
    "Keine echten Teilnehmerdaten.",
    "ausschließlich lokal mit synthetischen Abhängigkeiten",
    "fehlenden externen Zugriff",
    "v27.36b-/v27.36c-Checker",
    "Kein anderer Task und kein Folgetask ist ausgewählt oder autorisiert.",
    "Commit und Push bleiben NEIN.",
    "### Permanenter v27.36e-Lebenszyklus",
    "authorization_prepared",
    "authorization_committed",
    "implementation_prepared",
    "implementation_committed",
    "closure_prepared",
    "closure_committed",
    "GATE enthält ausschließlich eine nichtleere Teilmenge der fünf Gate-Dateien.",
    "IMPLEMENTATION enthält exakt die sechs autorisierten Implementierungsdateien",
    "CLOSURE ist erst nach IMPLEMENTATION zulässig",
    "Keine zukünftige GATE-, IMPLEMENTATION- oder CLOSURE-SHA wird hartcodiert.",
    "Rückkehr zu einem autorisierten v27.36e-Zustand bleibt nach der Closure ohne neue ausdrückliche Autorisierung blockiert.",
)
V2736E_CLOSURE_MARKERS = (
    "v27.36e abgeschlossen.",
    "CommonJS-Kompatibilität der v27.36b-/v27.36c-Bestandsmodule bleibt erhalten.",
    "Kontrollierte Browser-Exports verbinden die bestehenden Factories.",
    "Browser-Factory-Exports sind `window.ACCAOUI_PARTICIPANT_ACCESS_ADAPTER_FACTORY` und `window.ACCAOUI_PARTICIPANT_ACCESS_BOOTSTRAP_BRIDGE_FACTORY`.",
    "Der Browser-App-Provider ist `window.ACCAOUI_PARTICIPANT_ACCESS_APP_PROVIDER`.",
    "Der Browser-Provider stellt ausschließlich `resolveAccess()` bereit.",
    "Keine Fachlogik wird dupliziert.",
    "Fehlende oder ungültige Dependencies sowie Throw, Reject und ungültige Ergebnisse bleiben fail-closed.",
    "Der Kollisionsschutz überschreibt keine inkompatiblen vorhandenen Globals.",
    "Es gibt keine automatische Client-Erzeugung.",
    "Es gibt keine direkten Supabase-, Auth- oder Tabellenabfragen im Provider.",
    "`index.html`, `app.js` und `style.css` bleiben unverändert.",
    "Die Browser-Kette ist noch NICHT über `index.html` aktiviert.",
    "Der lokale App-Start bleibt unverändert.",
    "Supabase bleibt NICHT LIVE.",
    "Keine echten Keys.",
    "Keine echten Teilnehmerdaten.",
    "v27.36e-Checker: PASS (Positiv: 22; Negativ: 31; Manipulation: 16).",
    "v27.36b-Checker: PASS.",
    "v27.36c-Checker: PASS.",
    "v27.36d-Regressionsprofil: PASS.",
    "Kontinuitätschecker: PASS.",
    "Preflight: PASS.",
    "`git diff --check`: PASS.",
    "Kein Folgetask wurde ausgewählt oder autorisiert.",
    "### Permanenter v27.36e-Lebenszyklus",
    "authorization_prepared",
    "authorization_committed",
    "implementation_prepared",
    "implementation_committed",
    "closure_prepared",
    "closure_committed",
    "Der Implementierungscommit ist historisch dokumentiert.",
    "Die Closure wird weiterhin dynamisch aus Git-Historie, Dateiumfang und geschlossenem Taskzustand erkannt.",
    "Keine zukünftige CLOSURE-SHA wird hartcodiert.",
    "Rückkehr zu einem autorisierten v27.36e-Zustand bleibt ohne neue ausdrückliche Autorisierung blockiert.",
)
V2736E_TASK_AUTHORIZED = "authorized"
V2736E_TASK_CLOSED = "closed"
V2736E_HISTORY_BEFORE_AUTHORIZATION = "before_authorization_commit"
V2736E_HISTORY_AUTHORIZED = "authorization_committed"
V2736E_HISTORY_IMPLEMENTED = "implementation_committed"
V2736E_HISTORY_CLOSED = "closure_committed"
V2736E_PHASE_AUTHORIZATION_PREPARED = "authorization_prepared"
V2736E_PHASE_AUTHORIZATION_COMMITTED = "authorization_committed"
V2736E_PHASE_IMPLEMENTATION_PREPARED = "implementation_prepared"
V2736E_PHASE_IMPLEMENTATION_COMMITTED = "implementation_committed"
V2736E_PHASE_CLOSURE_PREPARED = "closure_prepared"
V2736E_PHASE_CLOSURE_COMMITTED = "closure_committed"
V2736E_ROLE_GATE = "GATE"
V2736E_ROLE_IMPLEMENTATION = "IMPLEMENTATION"
V2736E_ROLE_CLOSURE = "CLOSURE"


@dataclass(frozen=True)
class V2736ECommitFact:
    commit_sha: str
    changed_files: frozenset[str]
    task_state: str


@dataclass(frozen=True)
class V2736EHistoryState:
    state: str
    implementation_commit: str | None
    roles: tuple[str, ...]
    gate_commits: tuple[str, ...]


@dataclass(frozen=True)
class V2736EWorkingTreeFact:
    branch: str
    head: str
    origin_main: str
    diff_files: frozenset[str]
    staged_files: frozenset[str]
    untracked_files: frozenset[str]
    status_lines: frozenset[str]
    new_files_existing: frozenset[str]
    new_files_tracked_at_base: frozenset[str]
    new_files_tracked_at_head: frozenset[str]
    base_is_head_ancestor: bool
    base_is_origin_ancestor: bool
    origin_is_head_ancestor: bool


def validate_v2736d_completed_base() -> tuple[V2736DHistoryState, tuple[str, str, str, str]]:
    require(
        git_is_ancestor(V2736D_AUTHORIZATION_BASE_SHA, V2736E_AUTHORIZATION_BASE_SHA),
        "v27.36d-Basis ist kein Vorfahr des v27.36d-Closure-HEAD",
    )
    facts = read_v2736d_commit_facts(V2736E_AUTHORIZATION_BASE_SHA)
    history = validate_v2736d_history_facts(facts)
    require(history.state == V2736D_HISTORY_CLOSED, "v27.36d muss an der v27.36e-Basis vollständig geschlossen sein")
    require(history.implementation_commit is not None, "v27.36d benötigt an der v27.36e-Basis exakt eine IMPLEMENTATION")
    require(history.roles.count(V2736D_ROLE_IMPLEMENTATION) == 1, "v27.36d benötigt exakt einen IMPLEMENTATION-Commit")
    require(history.roles.count(V2736D_ROLE_CLOSURE) == 1 and history.roles[-1] == V2736D_ROLE_CLOSURE, "v27.36d-Closure muss exakt einmal und zuletzt vorliegen")
    require(facts[-1].commit_sha == V2736E_AUTHORIZATION_BASE_SHA, "Verbindlicher v27.36d-Closure-HEAD wurde nicht erkannt")
    require(facts[-1].changed_files == frozenset(EXPECTED_CONTROL_FILES), "v27.36d-Closure-HEAD muss exakt die fünf Gate-Dateien ändern")
    validate_v2736d_committed_closure_documents(facts, history)
    validate_v2736d_source_contract_at_revision(history.implementation_commit)
    documents = (
        read_v2735f_commit_document(V2736E_AUTHORIZATION_BASE_SHA, "docs/PROJECT_STATE_CURRENT.md"),
        read_v2735f_commit_document(V2736E_AUTHORIZATION_BASE_SHA, V2735F_TASK_RELATIVE_PATH),
        read_v2735f_commit_document(V2736E_AUTHORIZATION_BASE_SHA, "docs/CURSOR_MASTER_CONTEXT_ACCAOUI.md"),
        read_v2735f_commit_document(V2736E_AUTHORIZATION_BASE_SHA, "docs/PROJECT_MASTERLIST.md"),
    )
    validate_v2736d_closed_documents(*documents, history.implementation_commit)
    return history, documents


def synthetic_v2736d_closed_working_fact() -> V2736DWorkingTreeFact:
    return V2736DWorkingTreeFact(
        branch="main",
        head=V2736E_AUTHORIZATION_BASE_SHA,
        origin_main=V2736E_AUTHORIZATION_BASE_SHA,
        diff_files=frozenset(),
        staged_files=frozenset(),
        untracked_files=frozenset(),
        status_lines=frozenset(),
        implementation_files_existing=V2736D_NEW_IMPLEMENTATION_FILES,
        implementation_files_tracked_at_base=frozenset(),
        implementation_files_tracked_at_head=V2736D_NEW_IMPLEMENTATION_FILES,
        base_is_head_ancestor=True,
        base_is_origin_ancestor=True,
        origin_is_head_ancestor=True,
    )


def validate_no_future_v2736e_sha(section: str, allowed_shas: frozenset[str], document_name: str) -> None:
    shas = frozenset(re.findall(r"\b[0-9a-f]{40}\b", section))
    require(shas.issubset(allowed_shas), f"{document_name}: zukünftige v27.36e-Commit-SHA hartcodiert: {sorted(shas - allowed_shas)}")
    require(re.search(r"\bv27\.(?:36[f-z]|3[7-9])\b", section, re.IGNORECASE) is None, f"{document_name}: automatischer Folgetask nach v27.36e unzulässig")


def validate_v2736e_authorization_section(section: str, document_name: str) -> None:
    validate_required_markers(section, V2736E_AUTHORIZATION_MARKERS, f"{document_name} / v27.36e")
    validate_no_future_v2736e_sha(section, frozenset({V2736E_AUTHORIZATION_BASE_SHA}), f"{document_name} / v27.36e")
    for path in V2736E_IMPLEMENTATION_FILES:
        require(section.count(f"`{path}`") == 1, f"{document_name}: v27.36e-Datei fehlt oder ist doppelt: {path}")


def extract_v2736e_authorization_section(text: str, document_name: str) -> str:
    boundaries = {
        "PROJECT_STATE_CURRENT": (
            "## Autorisierter Task v27.36e",
            "## Abgeschlossener technischer Schritt v27.36d",
        ),
        "CURRENT_TASK": (
            "## Autorisierter Task v27.36e",
            "## Abgeschlossener technischer Schritt v27.36d",
        ),
        "CURSOR_MASTER_CONTEXT_ACCAOUI": (
            "### Autorisierter Task v27.36e",
            "### Abgeschlossener technischer Schritt v27.36d",
        ),
        "PROJECT_MASTERLIST": (
            "### Autorisierter Task v27.36e",
            "### Abgeschlossener technischer Schritt v27.36d",
        ),
    }
    require(document_name in boundaries, f"Unbekanntes v27.36e-Vertragsdokument: {document_name}")
    start_heading, end_heading = boundaries[document_name]
    return section_between(text, start_heading, end_heading, document_name)


def extract_v2736e_closure_section(text: str, document_name: str) -> str:
    heading_prefix = "##" if document_name in {"PROJECT_STATE_CURRENT", "CURRENT_TASK"} else "###"
    return section_between(
        text,
        f"{heading_prefix} Abgeschlossener technischer Schritt v27.36e",
        f"{heading_prefix} Abgeschlossener technischer Schritt v27.36d",
        document_name,
    )


def validate_v2736e_state_text(text: str) -> None:
    validate_exact_fields(text, V2736E_EXPECTED_STATE_FIELDS)
    section = extract_v2736e_authorization_section(text, "PROJECT_STATE_CURRENT")
    validate_v2736e_authorization_section(section, "PROJECT_STATE_CURRENT")


def validate_v2736e_task_text(text: str) -> None:
    validate_exact_fields(text, V2736E_EXPECTED_TASK_FIELDS)
    require(text.count(f"Erlaubte Implementierungsdateien: {V2736E_ALLOWED_FILES_VALUE}") == 1, "CURRENT_TASK muss exakt eine verbindliche v27.36e-Dateifreigabe enthalten")
    section = extract_v2736e_authorization_section(text, "CURRENT_TASK")
    validate_v2736e_authorization_section(section, "CURRENT_TASK")


def validate_v2736e_cursor_text(text: str) -> None:
    require(exact_field(text, "Stand") == "v27.36e", "CURSOR-Kontext muss auf v27.36e stehen")
    validate_project_paths(text, "CURSOR_MASTER_CONTEXT_ACCAOUI")
    section = extract_v2736e_authorization_section(text, "CURSOR_MASTER_CONTEXT_ACCAOUI")
    validate_v2736e_authorization_section(section, "CURSOR_MASTER_CONTEXT_ACCAOUI")


def validate_v2736e_masterlist_text(text: str) -> None:
    require(exact_field(text, "Stand") == "v27.36e", "PROJECT_MASTERLIST muss auf v27.36e stehen")
    validate_v2736d_permanent_masterlist_contract(text)
    rows = re.findall(r"(?m)^\| v27\.36e \|.*$", text)
    require(len(rows) == 1 and "**autorisiert**" in rows[0], "PROJECT_MASTERLIST muss v27.36e exakt einmal als autorisiert führen")
    section = extract_v2736e_authorization_section(text, "PROJECT_MASTERLIST")
    validate_v2736e_authorization_section(section, "PROJECT_MASTERLIST")


def detect_v2736e_task_state_text(text: str) -> str:
    task_id = exact_field(text, "Task-ID")
    if task_id == "v27.36e":
        validate_exact_fields(text, V2736E_EXPECTED_TASK_FIELDS)
        return V2736E_TASK_AUTHORIZED
    if task_id == "NONE":
        validate_exact_fields(text, V2736E_CLOSED_TASK_FIELDS)
        return V2736E_TASK_CLOSED
    raise ValidationError(f"Unzulässiger v27.36e-Taskzustand: {task_id}")


def validate_v2736e_closed_documents(state_text: str, task_text: str, cursor_text: str, masterlist_text: str, implementation_commit: str) -> None:
    require(re.fullmatch(r"[0-9a-f]{40}", implementation_commit) is not None, "v27.36e-Closure benötigt einen dynamisch erkannten Implementierungscommit")
    validate_exact_fields(state_text, V2736E_CLOSED_STATE_FIELDS)
    validate_exact_fields(task_text, V2736E_CLOSED_TASK_FIELDS)
    require(exact_field(cursor_text, "Stand") == "v27.36e", "CURSOR-Kontext muss nach v27.36e-Closure auf v27.36e stehen")
    require(exact_field(masterlist_text, "Stand") == "v27.36e", "PROJECT_MASTERLIST muss nach v27.36e-Closure auf v27.36e stehen")
    validate_project_paths(cursor_text, "CURSOR_MASTER_CONTEXT_ACCAOUI")
    validate_v2736d_permanent_masterlist_contract(masterlist_text)
    sections = (
        extract_v2736e_closure_section(state_text, "PROJECT_STATE_CURRENT"),
        extract_v2736e_closure_section(task_text, "CURRENT_TASK"),
        extract_v2736e_closure_section(cursor_text, "CURSOR_MASTER_CONTEXT_ACCAOUI"),
        extract_v2736e_closure_section(masterlist_text, "PROJECT_MASTERLIST"),
    )
    for section, name in zip(sections, ("PROJECT_STATE_CURRENT", "CURRENT_TASK", "CURSOR_MASTER_CONTEXT_ACCAOUI", "PROJECT_MASTERLIST")):
        validate_required_markers(section, V2736E_CLOSURE_MARKERS, f"{name} / v27.36e-Closure")
        require(section.count(f"Implementierungscommit: `{implementation_commit}`") == 1, f"{name}: dynamischer v27.36e-Implementierungscommit fehlt oder ist doppelt")
        validate_no_future_v2736e_sha(section, frozenset({V2736E_AUTHORIZATION_BASE_SHA, implementation_commit}), f"{name} / v27.36e-Closure")
        for path in V2736E_IMPLEMENTATION_FILES:
            require(section.count(f"`{path}`") == 1, f"{name}: v27.36e-Implementierungsdatei fehlt oder ist doppelt: {path}")
    rows = re.findall(r"(?m)^\| v27\.36e \|.*$", masterlist_text)
    require(len(rows) == 1 and "**erledigt**" in rows[0] and implementation_commit in rows[0], "PROJECT_MASTERLIST muss v27.36e nach Closure exakt einmal als erledigt führen")


def read_v2736e_commit_facts(current_head: str) -> tuple[V2736ECommitFact, ...]:
    shas = tuple(line.strip() for line in run_git(["rev-list", "--reverse", f"{V2736E_AUTHORIZATION_BASE_SHA}..{current_head}"]).splitlines() if line.strip())
    previous = V2736E_AUTHORIZATION_BASE_SHA
    facts: list[V2736ECommitFact] = []
    for sha in shas:
        lineage = run_git(["rev-list", "--parents", "-n", "1", sha]).split()
        require(len(lineage) == 2 and lineage[1] == previous, "v27.36e erlaubt nur eine lineare Historie ohne Merge-Commit")
        files = frozenset(line.strip().replace("\\", "/") for line in run_git(["diff", "--name-only", previous, sha]).splitlines() if line.strip())
        require(files, f"Leerer v27.36e-Commit unzulässig: {sha}")
        commit_task = read_v2735f_commit_document(sha, V2735F_TASK_RELATIVE_PATH)
        facts.append(V2736ECommitFact(sha, files, detect_v2736e_task_state_text(commit_task)))
        previous = sha
    return tuple(facts)


def validate_v2736e_history_facts(facts: tuple[V2736ECommitFact, ...]) -> V2736EHistoryState:
    gate_files = frozenset(EXPECTED_CONTROL_FILES)
    roles: list[str] = []
    gate_commits: list[str] = []
    implementation_commit: str | None = None
    closed = False
    for fact in facts:
        files = fact.changed_files
        if files == V2736E_IMPLEMENTATION_FILES:
            require(gate_commits, "v27.36e-IMPLEMENTATION vor Autorisierungs-GATE unzulässig")
            require(implementation_commit is None, "Mehr als ein v27.36e-IMPLEMENTATION-Commit unzulässig")
            require(not closed, "v27.36e-IMPLEMENTATION nach CLOSURE unzulässig")
            require(fact.task_state == V2736E_TASK_AUTHORIZED, "v27.36e-IMPLEMENTATION benötigt AUTHORIZED / Autorisiert JA")
            implementation_commit = fact.commit_sha
            roles.append(V2736E_ROLE_IMPLEMENTATION)
            continue
        require(files and files.issubset(gate_files), f"Fremde Datei in v27.36e-Commit {fact.commit_sha}: {sorted(files - gate_files)}")
        if fact.task_state == V2736E_TASK_AUTHORIZED:
            require(not closed, "Rückkehr zu v27.36e / AUTHORIZED nach CLOSURE unzulässig")
            gate_commits.append(fact.commit_sha)
            roles.append(V2736E_ROLE_GATE)
            continue
        require(implementation_commit is not None, "v27.36e-CLOSURE vor IMPLEMENTATION unzulässig")
        require(not closed, "Mehr als ein v27.36e-CLOSURE-Commit unzulässig")
        require(files == gate_files, "v27.36e-CLOSURE muss exakt die fünf Gate-Dateien ändern")
        closed = True
        roles.append(V2736E_ROLE_CLOSURE)
    state = V2736E_HISTORY_CLOSED if closed else V2736E_HISTORY_IMPLEMENTED if implementation_commit else V2736E_HISTORY_AUTHORIZED if gate_commits else V2736E_HISTORY_BEFORE_AUTHORIZATION
    return V2736EHistoryState(state, implementation_commit, tuple(roles), tuple(gate_commits))


def read_v2736e_working_tree_fact() -> V2736EWorkingTreeFact:
    head = run_git(["rev-parse", "HEAD"]).strip()
    origin_main = run_git(["rev-parse", "origin/main"]).strip()

    def tracked_at(revision: str) -> frozenset[str]:
        return frozenset(line.strip().replace("\\", "/") for line in run_git(["ls-tree", "-r", "--name-only", revision, "--", *sorted(V2736E_NEW_IMPLEMENTATION_FILES)]).splitlines() if line.strip())

    return V2736EWorkingTreeFact(
        branch=run_git(["branch", "--show-current"]).strip(),
        head=head,
        origin_main=origin_main,
        diff_files=frozenset(line.strip().replace("\\", "/") for line in run_git(["diff", "--name-only"]).splitlines() if line.strip()),
        staged_files=frozenset(line.strip().replace("\\", "/") for line in run_git(["diff", "--cached", "--name-only"]).splitlines() if line.strip()),
        untracked_files=frozenset(line.strip().replace("\\", "/") for line in run_git(["ls-files", "--others", "--exclude-standard"]).splitlines() if line.strip()),
        status_lines=frozenset(line.replace("\\", "/") for line in run_git(["status", "--porcelain=v1", "--untracked-files=all"]).splitlines() if line),
        new_files_existing=frozenset(path for path in V2736E_NEW_IMPLEMENTATION_FILES if (ROOT / path).is_file()),
        new_files_tracked_at_base=tracked_at(V2736E_AUTHORIZATION_BASE_SHA),
        new_files_tracked_at_head=tracked_at(head),
        base_is_head_ancestor=git_is_ancestor(V2736E_AUTHORIZATION_BASE_SHA, head),
        base_is_origin_ancestor=git_is_ancestor(V2736E_AUTHORIZATION_BASE_SHA, origin_main),
        origin_is_head_ancestor=git_is_ancestor(origin_main, head),
    )


def validate_v2736e_working_tree_fact(fact: V2736EWorkingTreeFact) -> None:
    require(fact.branch == "main", "v27.36e-Lebenszyklus muss auf main laufen")
    require(fact.base_is_head_ancestor, "Die stabile v27.36e-Basis ist kein Vorfahr von HEAD")
    require(fact.base_is_origin_ancestor, "Die stabile v27.36e-Basis ist kein Vorfahr von origin/main")
    require(fact.origin_is_head_ancestor, "origin/main ist kein Vorfahr des lokalen v27.36e-HEAD")
    require(not fact.new_files_tracked_at_base, "Neue v27.36e-Implementierungsdateien dürfen an der Basis nicht existieren")
    require(not fact.staged_files, "v27.36e-Lebenszyklus darf nichts stagen")


def validate_v2736e_source_contract(adapter_text: str, adapter_added: str, bridge_text: str, bridge_added: str, provider_text: str, checker_text: str, report_text: str, preflight_text: str) -> None:
    for text, factory, browser_export, name in (
        (adapter_text, "createParticipantAccessAdapter", "ACCAOUI_PARTICIPANT_ACCESS_ADAPTER_FACTORY", "v27.36b-Adapter"),
        (bridge_text, "createParticipantAccessBootstrapBridge", "ACCAOUI_PARTICIPANT_ACCESS_BOOTSTRAP_BRIDGE_FACTORY", "v27.36c-Brücke"),
    ):
        require("module.exports" in text and factory in text, f"{name}: CommonJS-Kompatibilität fehlt")
        require(browser_export in text, f"{name}: kontrollierter Browser-Export fehlt")
    for added, name in ((adapter_added, "v27.36b-Adapter-Diff"), (bridge_added, "v27.36c-Brücken-Diff")):
        for token in (".from(", "getSession(", "createClient(", "initializeClient(", "getState(", "fetch(", "userId"):
            require(token.casefold() not in added.casefold(), f"{name} dupliziert Fach- oder Live-Logik: {token}")
    for marker in (
        "ACCAOUI_PARTICIPANT_ACCESS_APP_PROVIDER",
        "ACCAOUI_SUPABASE_BOOTSTRAP",
        "ACCAOUI_PARTICIPANT_ACCESS_ADAPTER_FACTORY",
        "ACCAOUI_PARTICIPANT_ACCESS_BOOTSTRAP_BRIDGE_FACTORY",
        "resolveAccess",
    ):
        require(marker in provider_text, f"v27.36e-Browser-Provider fehlt Bindung: {marker}")
    for token in ("initializeClient(", "getState(", "createClient(", "getSession(", ".from(", "fetch(", "XMLHttpRequest", "WebSocket", "userId", "http://", "https://"):
        require(token.casefold() not in provider_text.casefold(), f"v27.36e-Browser-Provider verletzt Sicherheitsgrenze: {token}")
    for marker in ("synthet", "CommonJS", "Browser", "resolveAccess", "fail-closed", "access_allowed", "participant_blocked", "keine Fachlogik"):
        require(marker.casefold() in checker_text.casefold(), f"v27.36e-Checker fehlt Testbindung: {marker}")
    for marker in ("Ziel", "Sicherheitsgrenze", "CommonJS-Kompatibilität", "kontrollierte Browser-Exports", "ausschließlich resolveAccess()", "keine duplizierte Fachlogik", "lokale synthetische Tests", "Supabase live: NEIN", "echte Keys: NEIN", "echte Teilnehmerdaten: NEIN"):
        require(marker in report_text, f"v27.36e-Umsetzungsbericht fehlt: {marker}")
    for required_checker in ("check-project-continuity-control.py", "check-supabase-participant-access-adapter.py", "check-supabase-participant-access-bootstrap-bridge.py", "check-participant-access-app-entry-v2736d.py", "check-participant-access-browser-provider-v2736e.py"):
        require(required_checker in preflight_text, f"Preflight-Pflichtchecker fehlt: {required_checker}")


def validate_v2736e_local_source_contract() -> None:
    validate_v2736e_source_contract(
        read_required_text(ROOT / "data/supabase-participant-access-adapter.js"),
        extract_added_lines(run_git(["diff", "--unified=0", V2736E_AUTHORIZATION_BASE_SHA, "--", "data/supabase-participant-access-adapter.js"])),
        read_required_text(ROOT / "data/supabase-participant-access-bootstrap-bridge.js"),
        extract_added_lines(run_git(["diff", "--unified=0", V2736E_AUTHORIZATION_BASE_SHA, "--", "data/supabase-participant-access-bootstrap-bridge.js"])),
        read_required_text(ROOT / "data/supabase-participant-access-browser-provider.js"),
        read_required_text(ROOT / "tools/check-participant-access-browser-provider-v2736e.py"),
        read_required_text(ROOT / "docs/PARTICIPANT_ACCESS_BROWSER_PROVIDER_V2736E.md"),
        read_required_text(PREFLIGHT_PATH),
    )


def validate_v2736e_source_contract_at_revision(revision: str) -> None:
    parent = run_git(["rev-parse", f"{revision}^"]).strip()
    validate_v2736e_source_contract(
        read_v2735f_commit_document(revision, "data/supabase-participant-access-adapter.js"),
        extract_added_lines(run_git(["diff", "--unified=0", parent, revision, "--", "data/supabase-participant-access-adapter.js"])),
        read_v2735f_commit_document(revision, "data/supabase-participant-access-bootstrap-bridge.js"),
        extract_added_lines(run_git(["diff", "--unified=0", parent, revision, "--", "data/supabase-participant-access-bootstrap-bridge.js"])),
        read_v2735f_commit_document(revision, "data/supabase-participant-access-browser-provider.js"),
        read_v2735f_commit_document(revision, "tools/check-participant-access-browser-provider-v2736e.py"),
        read_v2735f_commit_document(revision, "docs/PARTICIPANT_ACCESS_BROWSER_PROVIDER_V2736E.md"),
        read_v2735f_commit_document(revision, "tools/preflight.py"),
    )


def validate_v2736e_lifecycle_working_tree(history: V2736EHistoryState, task_state: str, fact: V2736EWorkingTreeFact) -> str:
    validate_v2736e_working_tree_fact(fact)
    gate_files = frozenset(EXPECTED_CONTROL_FILES)
    clean = not fact.diff_files and not fact.untracked_files and not fact.status_lines
    if history.state == V2736E_HISTORY_BEFORE_AUTHORIZATION:
        require(fact.head == V2736E_AUTHORIZATION_BASE_SHA, "Autorisierungsvorbereitung benötigt die stabile v27.36e-Basis als HEAD")
        require(task_state == V2736E_TASK_AUTHORIZED, "Autorisierungsvorbereitung benötigt v27.36e / AUTHORIZED")
        require(fact.diff_files and fact.diff_files.issubset(gate_files), "Autorisierungsvorbereitung darf nur eine nichtleere Teilmenge der fünf Gate-Dateien ändern")
        require(not fact.untracked_files and fact.status_lines == frozenset(f" M {path}" for path in fact.diff_files), "Working Tree entspricht nicht authorization_prepared")
        require(not fact.new_files_existing, "v27.36e-Implementation vor Autorisierungscommit unzulässig")
        return V2736E_PHASE_AUTHORIZATION_PREPARED
    if history.state == V2736E_HISTORY_AUTHORIZED:
        require(fact.head != V2736E_AUTHORIZATION_BASE_SHA, "Autorisierungscommit fehlt")
        require(task_state == V2736E_TASK_AUTHORIZED, "Autorisierte Phasen benötigen v27.36e / AUTHORIZED")
        require(not fact.new_files_tracked_at_head, "Neue v27.36e-Dateien dürfen vor IMPLEMENTATION nicht getrackt sein")
        if clean:
            require(not fact.new_files_existing, "Implementation darf vor preparation nicht lokal existieren")
            return V2736E_PHASE_AUTHORIZATION_COMMITTED
        if fact.diff_files and fact.diff_files.issubset(gate_files) and not fact.untracked_files:
            require(fact.status_lines == frozenset(f" M {path}" for path in fact.diff_files), "Lokale v27.36e-Gate-Korrektur enthält fremden Status")
            require(not fact.new_files_existing, "Implementation während Gate-Korrektur unzulässig")
            return V2736E_PHASE_AUTHORIZATION_COMMITTED
        require(fact.diff_files == V2736E_EXISTING_IMPLEMENTATION_FILES, "implementation_prepared muss exakt die drei bestehenden Implementierungsdateien ändern")
        require(fact.untracked_files == V2736E_NEW_IMPLEMENTATION_FILES, "implementation_prepared benötigt exakt die drei neuen Implementierungsdateien")
        require(fact.new_files_existing == V2736E_NEW_IMPLEMENTATION_FILES, "implementation_prepared benötigt alle drei neuen Dateien")
        expected_status = frozenset({*(f" M {path}" for path in V2736E_EXISTING_IMPLEMENTATION_FILES), *(f"?? {path}" for path in V2736E_NEW_IMPLEMENTATION_FILES)})
        require(fact.status_lines == expected_status, "Working Tree entspricht nicht implementation_prepared")
        return V2736E_PHASE_IMPLEMENTATION_PREPARED
    require(history.implementation_commit is not None, "Phase nach IMPLEMENTATION benötigt den dynamischen Implementierungscommit")
    require(fact.new_files_tracked_at_head == V2736E_NEW_IMPLEMENTATION_FILES, "Nach IMPLEMENTATION müssen alle drei neuen Dateien getrackt sein")
    require(fact.new_files_existing == V2736E_NEW_IMPLEMENTATION_FILES, "Nach IMPLEMENTATION müssen alle drei neuen Dateien vorhanden sein")
    if history.state == V2736E_HISTORY_IMPLEMENTED:
        if task_state == V2736E_TASK_AUTHORIZED:
            if clean:
                return V2736E_PHASE_IMPLEMENTATION_COMMITTED
            require(fact.diff_files and fact.diff_files.issubset(gate_files) and not fact.untracked_files, "Nach IMPLEMENTATION sind lokal nur Gate-Korrekturen zulässig")
            require(fact.status_lines == frozenset(f" M {path}" for path in fact.diff_files), "Lokale Gate-Korrektur nach IMPLEMENTATION enthält fremden Status")
            return V2736E_PHASE_IMPLEMENTATION_COMMITTED
        require(task_state == V2736E_TASK_CLOSED, "closure_prepared benötigt den geschlossenen v27.36e-Taskzustand")
        require(fact.diff_files == gate_files and not fact.untracked_files, "closure_prepared muss exakt fünf Gate-Dateien ändern")
        require(fact.status_lines == frozenset(f" M {path}" for path in gate_files), "Working Tree entspricht nicht closure_prepared")
        return V2736E_PHASE_CLOSURE_PREPARED
    require(history.state == V2736E_HISTORY_CLOSED, "Unbekannter v27.36e-Historienzustand")
    require(task_state == V2736E_TASK_CLOSED, "Nach v27.36e-CLOSURE darf keine Rückkehr zu AUTHORIZED erfolgen")
    require(clean, "closure_committed benötigt einen sauberen Working Tree")
    return V2736E_PHASE_CLOSURE_COMMITTED


def validate_v2736e_committed_closure_documents(facts: tuple[V2736ECommitFact, ...], history: V2736EHistoryState) -> None:
    if V2736E_ROLE_CLOSURE not in history.roles:
        return
    require(history.implementation_commit is not None, "v27.36e-CLOSURE benötigt einen dynamischen Implementierungscommit")
    for fact, role in zip(facts, history.roles):
        if role == V2736E_ROLE_CLOSURE:
            validate_v2736e_closed_documents(
                read_v2735f_commit_document(fact.commit_sha, "docs/PROJECT_STATE_CURRENT.md"),
                read_v2735f_commit_document(fact.commit_sha, V2735F_TASK_RELATIVE_PATH),
                read_v2735f_commit_document(fact.commit_sha, "docs/CURSOR_MASTER_CONTEXT_ACCAOUI.md"),
                read_v2735f_commit_document(fact.commit_sha, "docs/PROJECT_MASTERLIST.md"),
                history.implementation_commit,
            )


def validate_v2736e_lifecycle(state_text: str, task_text: str, cursor_text: str, masterlist_text: str) -> tuple[str, V2736EHistoryState, V2736EWorkingTreeFact]:
    fact = read_v2736e_working_tree_fact()
    facts = read_v2736e_commit_facts(fact.head)
    history = validate_v2736e_history_facts(facts)
    validate_v2736e_committed_closure_documents(facts, history)
    task_state = detect_v2736e_task_state_text(task_text)
    if task_state == V2736E_TASK_AUTHORIZED:
        validate_v2736e_state_text(state_text)
        validate_v2736e_task_text(task_text)
        validate_v2736e_cursor_text(cursor_text)
        validate_v2736e_masterlist_text(masterlist_text)
    else:
        require(history.implementation_commit is not None, "v27.36e-Abschluss vor IMPLEMENTATION unzulässig")
        validate_v2736e_closed_documents(state_text, task_text, cursor_text, masterlist_text, history.implementation_commit)
    phase = validate_v2736e_lifecycle_working_tree(history, task_state, fact)
    if phase == V2736E_PHASE_IMPLEMENTATION_PREPARED:
        validate_v2736e_local_source_contract()
    if history.implementation_commit is not None:
        validate_v2736e_source_contract_at_revision(history.implementation_commit)
    return phase, history, fact


def run_v2736e_manipulation_matrix(state_text: str, task_text: str, cursor_text: str, masterlist_text: str, current_history: V2736EHistoryState, current_fact: V2736EWorkingTreeFact) -> tuple[int, int, int]:
    checks = 0

    def rejected(validator: Callable[[str], None], manipulated: str, label: str) -> None:
        nonlocal checks
        try:
            validator(manipulated)
        except ValidationError:
            checks += 1
            return
        raise ValidationError(f"v27.36e-Manipulation wurde nicht blockiert: {label}")

    current_task_state = detect_v2736e_task_state_text(task_text)
    if current_task_state == V2736E_TASK_CLOSED:
        require(current_history.gate_commits, "v27.36e-Closure benötigt einen historischen Autorisierungscommit")
        authorization_revision = current_history.gate_commits[-1]
        authorization_documents = (
            read_v2735f_commit_document(authorization_revision, "docs/PROJECT_STATE_CURRENT.md"),
            read_v2735f_commit_document(authorization_revision, V2735F_TASK_RELATIVE_PATH),
            read_v2735f_commit_document(authorization_revision, "docs/CURSOR_MASTER_CONTEXT_ACCAOUI.md"),
            read_v2735f_commit_document(authorization_revision, "docs/PROJECT_MASTERLIST.md"),
        )
    else:
        authorization_documents = (state_text, task_text, cursor_text, masterlist_text)
    authorization_state, authorization_task, authorization_cursor, authorization_masterlist = authorization_documents

    for text, validator, fields, name in (
        (authorization_state, validate_v2736e_state_text, V2736E_EXPECTED_STATE_FIELDS, "PROJECT_STATE_CURRENT"),
        (authorization_task, validate_v2736e_task_text, V2736E_EXPECTED_TASK_FIELDS, "CURRENT_TASK"),
    ):
        for field, value in fields.items():
            rejected(validator, text.replace(f"{field}: {value}", f"{field}: MANIPULIERT", 1), f"{name}: Feld {field}")
    boundaries = (
        (authorization_state, validate_v2736e_state_text, "PROJECT_STATE_CURRENT"),
        (authorization_task, validate_v2736e_task_text, "CURRENT_TASK"),
        (authorization_cursor, validate_v2736e_cursor_text, "CURSOR_MASTER_CONTEXT_ACCAOUI"),
        (authorization_masterlist, validate_v2736e_masterlist_text, "PROJECT_MASTERLIST"),
    )
    for text, validator, name in boundaries:
        section = extract_v2736e_authorization_section(text, name)
        for marker in V2736E_AUTHORIZATION_MARKERS:
            require(marker in section, f"Manipulationsmatrix kann v27.36e-Pflichtaussage nicht finden: {name} / {marker}")
            changed_section = section.replace(marker, "")
            require(marker not in changed_section, f"Manipulationsmatrix konnte v27.36e-Pflichtaussage nicht vollständig entfernen: {name} / {marker}")
            rejected(validator, text.replace(section, changed_section, 1), f"{name}: Pflichtaussage {marker}")
        manipulated_section = section + "\nZukünftiger v27.36e-Commit: `" + ("a" * 40) + "`\n"
        rejected(
            validator,
            text.replace(section, manipulated_section, 1),
            f"{name}: unbekannte zukünftige v27.36e-SHA",
        )
    if current_task_state == V2736E_TASK_CLOSED:
        require(current_history.implementation_commit is not None, "v27.36e-Closure-Manipulation benötigt den dynamischen Implementierungscommit")
        closure_documents = (state_text, task_text, cursor_text, masterlist_text)
        closure_names = ("PROJECT_STATE_CURRENT", "CURRENT_TASK", "CURSOR_MASTER_CONTEXT_ACCAOUI", "PROJECT_MASTERLIST")

        def closure_validator(index: int) -> Callable[[str], None]:
            def validate(manipulated: str) -> None:
                documents = list(closure_documents)
                documents[index] = manipulated
                validate_v2736e_closed_documents(*documents, current_history.implementation_commit)

            return validate

        for index, fields in ((0, V2736E_CLOSED_STATE_FIELDS), (1, V2736E_CLOSED_TASK_FIELDS)):
            text = closure_documents[index]
            validator = closure_validator(index)
            for field, value in fields.items():
                rejected(validator, text.replace(f"{field}: {value}", f"{field}: MANIPULIERT", 1), f"{closure_names[index]}: Closure-Feld {field}")
        for index, (text, name) in enumerate(zip(closure_documents, closure_names)):
            validator = closure_validator(index)
            section = extract_v2736e_closure_section(text, name)
            for marker in V2736E_CLOSURE_MARKERS:
                require(marker in section, f"Manipulationsmatrix kann v27.36e-Closure-Pflichtaussage nicht finden: {name} / {marker}")
                changed_section = section.replace(marker, "")
                rejected(validator, text.replace(section, changed_section, 1), f"{name}: Closure-Pflichtaussage {marker}")
            for path in V2736E_IMPLEMENTATION_FILES:
                changed_section = section.replace(f"`{path}`", "")
                rejected(validator, text.replace(section, changed_section, 1), f"{name}: Closure-Implementierungsdatei {path}")
            commit_marker = f"Implementierungscommit: `{current_history.implementation_commit}`"
            changed_section = section.replace(commit_marker, "")
            rejected(validator, text.replace(section, changed_section, 1), f"{name}: dynamischer Implementierungscommit")
            manipulated_section = section + "\nZukünftiger v27.36e-Commit: `" + ("a" * 40) + "`\n"
            rejected(validator, text.replace(section, manipulated_section, 1), f"{name}: unbekannte zukünftige v27.36e-Closure-SHA")
        v2736e_rows = re.findall(r"(?m)^\| v27\.36e \|.*$", masterlist_text)
        require(len(v2736e_rows) == 1, "Manipulationsmatrix benötigt exakt eine v27.36e-Masterlistenzeile")
        v2736e_row = v2736e_rows[0]
        manipulated_v2736e_row = v2736e_row.replace("**erledigt**", "**autorisiert**", 1)
        require(manipulated_v2736e_row != v2736e_row, "Manipulationsmatrix konnte den v27.36e-Abschlussstatus nicht verändern")
        rejected(
            closure_validator(3),
            masterlist_text.replace(v2736e_row, manipulated_v2736e_row, 1),
            "PROJECT_MASTERLIST: v27.36e nach Closure wieder autorisiert",
        )
    gate = V2736ECommitFact("1" * 40, frozenset({EXPECTED_CONTROL_FILES[0]}), V2736E_TASK_AUTHORIZED)
    implementation = V2736ECommitFact("2" * 40, V2736E_IMPLEMENTATION_FILES, V2736E_TASK_AUTHORIZED)
    closure = V2736ECommitFact("3" * 40, frozenset(EXPECTED_CONTROL_FILES), V2736E_TASK_CLOSED)
    histories = (
        validate_v2736e_history_facts(tuple()),
        validate_v2736e_history_facts((gate,)),
        validate_v2736e_history_facts((gate, implementation)),
        validate_v2736e_history_facts((gate, implementation, closure)),
    )
    clean_fact = replace(
        current_fact,
        head="1" * 40,
        diff_files=frozenset(), staged_files=frozenset(), untracked_files=frozenset(), status_lines=frozenset(),
        new_files_existing=frozenset(), new_files_tracked_at_base=frozenset(), new_files_tracked_at_head=frozenset(),
        base_is_head_ancestor=True, base_is_origin_ancestor=True, origin_is_head_ancestor=True,
    )
    gate_files = frozenset(EXPECTED_CONTROL_FILES)
    implemented_fact = replace(clean_fact, head="2" * 40, new_files_existing=V2736E_NEW_IMPLEMENTATION_FILES, new_files_tracked_at_head=V2736E_NEW_IMPLEMENTATION_FILES)
    implementation_status = frozenset({*(f" M {path}" for path in V2736E_EXISTING_IMPLEMENTATION_FILES), *(f"?? {path}" for path in V2736E_NEW_IMPLEMENTATION_FILES)})
    phase_fixtures = (
        (histories[0], V2736E_TASK_AUTHORIZED, replace(clean_fact, head=V2736E_AUTHORIZATION_BASE_SHA, diff_files=gate_files, status_lines=frozenset(f" M {path}" for path in gate_files)), V2736E_PHASE_AUTHORIZATION_PREPARED),
        (histories[1], V2736E_TASK_AUTHORIZED, clean_fact, V2736E_PHASE_AUTHORIZATION_COMMITTED),
        (histories[1], V2736E_TASK_AUTHORIZED, replace(clean_fact, diff_files=V2736E_EXISTING_IMPLEMENTATION_FILES, untracked_files=V2736E_NEW_IMPLEMENTATION_FILES, status_lines=implementation_status, new_files_existing=V2736E_NEW_IMPLEMENTATION_FILES), V2736E_PHASE_IMPLEMENTATION_PREPARED),
        (histories[2], V2736E_TASK_AUTHORIZED, implemented_fact, V2736E_PHASE_IMPLEMENTATION_COMMITTED),
        (histories[2], V2736E_TASK_CLOSED, replace(implemented_fact, diff_files=gate_files, status_lines=frozenset(f" M {path}" for path in gate_files)), V2736E_PHASE_CLOSURE_PREPARED),
        (histories[3], V2736E_TASK_CLOSED, implemented_fact, V2736E_PHASE_CLOSURE_COMMITTED),
    )
    for history, task_state, fact, expected in phase_fixtures:
        require(validate_v2736e_lifecycle_working_tree(history, task_state, fact) == expected, f"v27.36e-Positivsimulation fehlgeschlagen: {expected}")
    bad_histories = (
        ((implementation,), "Implementation vor Autorisierung"),
        ((gate, implementation, implementation), "zweite Implementation"),
        ((gate, closure), "Closure vor Implementation"),
        ((gate, implementation, closure, gate), "Rückkehr nach Closure"),
        ((gate, implementation, V2736ECommitFact("4" * 40, frozenset({EXPECTED_CONTROL_FILES[0]}), V2736E_TASK_CLOSED)), "partielle Closure"),
        ((gate, V2736ECommitFact("5" * 40, frozenset(set(V2736E_IMPLEMENTATION_FILES) - {"tools/preflight.py"}), V2736E_TASK_AUTHORIZED)), "partielle Implementation"),
        ((gate, V2736ECommitFact("6" * 40, V2736E_IMPLEMENTATION_FILES | {"index.html"}, V2736E_TASK_AUTHORIZED)), "Implementation mit index.html"),
        ((V2736ECommitFact("7" * 40, frozenset({"app.js"}), V2736E_TASK_AUTHORIZED),), "app.js geändert"),
        ((V2736ECommitFact("8" * 40, frozenset({"index.html"}), V2736E_TASK_AUTHORIZED),), "index.html geändert"),
        ((V2736ECommitFact("9" * 40, frozenset({"style.css"}), V2736E_TASK_AUTHORIZED),), "style.css geändert"),
    )
    for facts, label in bad_histories:
        try:
            validate_v2736e_history_facts(facts)
        except ValidationError:
            checks += 1
            continue
        raise ValidationError(f"v27.36e-Historienmanipulation wurde nicht blockiert: {label}")
    bad_working = (
        (current_history, V2736E_TASK_AUTHORIZED, replace(current_fact, staged_files=frozenset({EXPECTED_CONTROL_FILES[0]})), "gestagte Datei"),
        (current_history, V2736E_TASK_AUTHORIZED, replace(current_fact, diff_files=current_fact.diff_files | {"app.js"}, status_lines=current_fact.status_lines | {" M app.js"}), "fremde lokale Datei"),
        (current_history, V2736E_TASK_AUTHORIZED, replace(current_fact, untracked_files=frozenset({"unexpected.txt"}), status_lines=current_fact.status_lines | {"?? unexpected.txt"}), "fremde ungetrackte Datei"),
        (current_history, V2736E_TASK_AUTHORIZED, replace(current_fact, base_is_head_ancestor=False), "falsche Basis"),
        (current_history, V2736E_TASK_AUTHORIZED, replace(current_fact, origin_is_head_ancestor=False), "origin nicht Vorfahr"),
        (current_history, V2736E_TASK_AUTHORIZED, replace(current_fact, new_files_tracked_at_base=V2736E_NEW_IMPLEMENTATION_FILES), "neue Dateien bereits an Basis"),
        (histories[0], V2736E_TASK_AUTHORIZED, replace(clean_fact, head=V2736E_AUTHORIZATION_BASE_SHA, untracked_files=V2736E_NEW_IMPLEMENTATION_FILES, status_lines=frozenset(f"?? {path}" for path in V2736E_NEW_IMPLEMENTATION_FILES), new_files_existing=V2736E_NEW_IMPLEMENTATION_FILES), "Implementation lokal vor Autorisierung"),
        (histories[1], V2736E_TASK_CLOSED, replace(clean_fact, diff_files=gate_files, status_lines=frozenset(f" M {path}" for path in gate_files)), "Closure lokal vor Implementation"),
        (histories[3], V2736E_TASK_AUTHORIZED, implemented_fact, "Rückkehr zu AUTHORIZED nach Closure"),
    )
    for history, task_state, fact, label in bad_working:
        try:
            validate_v2736e_lifecycle_working_tree(history, task_state, fact)
        except ValidationError:
            checks += 1
            continue
        raise ValidationError(f"v27.36e-Working-Tree-Manipulation wurde nicht blockiert: {label}")
    valid_adapter = "module.exports createParticipantAccessAdapter ACCAOUI_PARTICIPANT_ACCESS_ADAPTER_FACTORY"
    valid_bridge = "module.exports createParticipantAccessBootstrapBridge ACCAOUI_PARTICIPANT_ACCESS_BOOTSTRAP_BRIDGE_FACTORY"
    valid_provider = "ACCAOUI_PARTICIPANT_ACCESS_APP_PROVIDER ACCAOUI_SUPABASE_BOOTSTRAP ACCAOUI_PARTICIPANT_ACCESS_ADAPTER_FACTORY ACCAOUI_PARTICIPANT_ACCESS_BOOTSTRAP_BRIDGE_FACTORY resolveAccess"
    valid_checker = "synthetische CommonJS Browser resolveAccess fail-closed access_allowed participant_blocked keine Fachlogik"
    valid_report = "\n".join(("Ziel", "Sicherheitsgrenze", "CommonJS-Kompatibilität", "kontrollierte Browser-Exports", "ausschließlich resolveAccess()", "keine duplizierte Fachlogik", "lokale synthetische Tests", "Supabase live: NEIN", "echte Keys: NEIN", "echte Teilnehmerdaten: NEIN"))
    valid_preflight = "check-project-continuity-control.py check-supabase-participant-access-adapter.py check-supabase-participant-access-bootstrap-bridge.py check-participant-access-app-entry-v2736d.py check-participant-access-browser-provider-v2736e.py"
    validate_v2736e_source_contract(valid_adapter, "browser export", valid_bridge, "browser export", valid_provider, valid_checker, valid_report, valid_preflight)
    source_cases = (
        (valid_adapter.replace("module.exports", ""), "browser export", valid_bridge, "browser export", valid_provider, valid_checker, valid_report, valid_preflight, "CommonJS-Adapter entfernt"),
        (valid_adapter, ".from(", valid_bridge, "browser export", valid_provider, valid_checker, valid_report, valid_preflight, "Fachlogik im Adapter-Diff"),
        (valid_adapter, "browser export", valid_bridge, "getState(", valid_provider, valid_checker, valid_report, valid_preflight, "State-Logik im Brücken-Diff"),
        (valid_adapter, "browser export", valid_bridge, "browser export", valid_provider + " initializeClient(", valid_checker, valid_report, valid_preflight, "Initialisierung im Provider"),
        (valid_adapter, "browser export", valid_bridge, "browser export", valid_provider.replace("resolveAccess", ""), valid_checker, valid_report, valid_preflight, "resolveAccess entfernt"),
        (valid_adapter, "browser export", valid_bridge, "browser export", valid_provider, valid_checker, valid_report, valid_preflight.replace("check-participant-access-browser-provider-v2736e.py", ""), "Checker aus Preflight entfernt"),
    )
    for args in source_cases:
        try:
            validate_v2736e_source_contract(*args[:-1])
        except ValidationError:
            checks += 1
            continue
        raise ValidationError(f"v27.36e-Quellmanipulation wurde nicht blockiert: {args[-1]}")
    negative_tests = len(bad_histories) + len(bad_working) + len(source_cases)
    return checks, len(phase_fixtures), negative_tests


V2736F_AUTHORIZATION_BASE_SHA = "dc0d3fc87bde407cfac94fd598601ce4e80dfad7"
V2736F_TITLE = "Kontrollierten Browser-Aktivierungsweg für den Teilnehmerzugang hinter explizitem Schalter vorbereiten"
V2736F_LOADER_ID = "accaoui-participant-access-browser-loader"
V2736F_IMPLEMENTATION_FILE_ORDER = (
    "index.html",
    "app.js",
    "data/supabase-participant-access-browser-loader.js",
    "tools/check-participant-access-browser-loader-v2736f.py",
    "docs/PARTICIPANT_ACCESS_BROWSER_LOADER_V2736F.md",
    "tools/preflight.py",
)
V2736F_IMPLEMENTATION_FILES = frozenset(V2736F_IMPLEMENTATION_FILE_ORDER)
V2736F_NEW_IMPLEMENTATION_FILES = frozenset(
    {
        "data/supabase-participant-access-browser-loader.js",
        "tools/check-participant-access-browser-loader-v2736f.py",
        "docs/PARTICIPANT_ACCESS_BROWSER_LOADER_V2736F.md",
    }
)
V2736F_EXISTING_IMPLEMENTATION_FILES = frozenset(
    V2736F_IMPLEMENTATION_FILES - V2736F_NEW_IMPLEMENTATION_FILES
)
V2736F_ALLOWED_FILES_VALUE = (
    "`index.html`, `app.js`, "
    "`data/supabase-participant-access-browser-loader.js`, "
    "`tools/check-participant-access-browser-loader-v2736f.py`, "
    "`docs/PARTICIPANT_ACCESS_BROWSER_LOADER_V2736F.md`, `tools/preflight.py`"
)
V2736F_EXPECTED_STATE_FIELDS = {
    "Stand": "v27.36f",
    "Repository": "`asarrad-bit/accaoui-34a-lernapp`",
    "Branch": "`main`",
    "Letzter abgeschlossener funktionaler Stand": "v27.35g",
    "Abschlusscommit": f"`{V2735G_COMPLETION_SHA}`",
    "Aktueller HEAD": "DYNAMISCH ZU PRÜFEN",
    "Funktionsstatus": "v27.35g abgeschlossen",
    "Weiterer funktionaler Schritt autorisiert": "JA",
    "Aktuell autorisierter Task": "v27.36f",
    "Aktuelle Taskart": "Kontrollierter Browser-Aktivierungsweg des Teilnehmerzugangs",
    "Aktueller Blocker": (
        "KEINER für die ausdrücklich autorisierte spätere v27.36f-Umsetzung; "
        "in diesem Autorisierungs-GATE erfolgt noch keine Implementierung"
    ),
}
V2736F_EXPECTED_TASK_FIELDS = {
    "Task-ID": "v27.36f",
    "Status": "AUTHORIZED",
    "Autorisiert": "JA",
    "Titel": V2736F_TITLE,
    "Funktionaler Ausgangsstand": "v27.35g",
    "Technischer Ausgangsstand": "v27.36e vollständig abgeschlossen",
    "Stabile Autorisierungsbasis": f"`{V2736F_AUTHORIZATION_BASE_SHA}`",
    "Erlaubte Implementierungsdateien": V2736F_ALLOWED_FILES_VALUE,
    "Commit erlaubt": "NEIN",
    "Push erlaubt": "NEIN",
}
V2736F_CLOSED_STATE_FIELDS = {
    "Stand": "v27.36f",
    "Repository": "`asarrad-bit/accaoui-34a-lernapp`",
    "Branch": "`main`",
    "Letzter abgeschlossener funktionaler Stand": "v27.35g",
    "Abschlusscommit": f"`{V2735G_COMPLETION_SHA}`",
    "Aktueller HEAD": "DYNAMISCH ZU PRÜFEN",
    "Funktionsstatus": "v27.35g abgeschlossen",
    "Weiterer funktionaler Schritt autorisiert": "NEIN",
    "Aktuell autorisierter Task": "NONE",
    "Aktuelle Taskart": "Kein Task autorisiert",
    "Aktueller Blocker": (
        "Neue Taskauswahl und ausdrückliche Autorisierung durch "
        "Projekteigentümer und verbindlichen Projektchat"
    ),
}
V2736F_CLOSED_TASK_FIELDS = {
    "Task-ID": "NONE",
    "Status": "BLOCKED",
    "Autorisiert": "NEIN",
    "Titel": "Kein Task autorisiert",
    "Funktionaler Ausgangsstand": "v27.35g",
    "Letzter abgeschlossener Kontrollschritt": "v27.36f",
    "Erlaubte Implementierungsdateien": "KEINE",
    "Commit erlaubt": "NEIN",
    "Push erlaubt": "NEIN",
}
V2736F_AUTHORIZATION_MARKERS = (
    "v27.36f ist der einzige autorisierte Task.",
    V2736F_TITLE + ".",
    "Dieser GATE-Schritt autorisiert nur die spätere Umsetzung",
    "Die funktionale Grundlage bleibt v27.35g.",
    "Die technische Grundlage ist der vollständig abgeschlossene Stand v27.36e.",
    f"Die stabile Autorisierungsbasis ist `{V2736F_AUTHORIZATION_BASE_SHA}`.",
    "Für die spätere IMPLEMENTATION sind exakt sechs Dateien erlaubt:",
    f"stabilen ID `{V2736F_LOADER_ID}`",
    "`data-enabled=\"false\"`",
    "Ausschließlich der exakte Attributwert `\"true\"` fordert die Aktivierung an.",
    "Storage-, Query-, Cookie- oder frei steuerbare Nutzerwerte",
    "Bei `data-enabled=\"false\"`",
    "der lokale Standardbetrieb bleibt unverändert und nicht blockierend.",
    "Bei `data-enabled=\"true\"` lädt der Loader in fester Reihenfolge Adapter, Brücke und Browser-Provider",
    "`window.ACCAOUI_PARTICIPANT_ACCESS_APP_PROVIDER`",
    "`window.ACCAOUI_PARTICIPANT_ACCESS_BROWSER_LOADER_READY`",
    "weder Client, `userId`, Session-, Teilnehmer-, Kurs-, Key- noch Configdaten offen.",
    "`app.js` prüft ausschließlich die Loader-Readiness",
    "bestehenden v27.36d-Providervertrag mit `resolveAccess()`",
    "fehlender oder nicht ausgeführter Loader",
    "fail-closed",
    "keinen lokalen Fallback",
    "`access_error` ohne interne Rohfehler",
    "Loader-Script-Tag mit `data-enabled=\"true\"`",
    "Keine Fachlogik aus v27.36b, v27.36c, v27.36d oder v27.36e wird dupliziert.",
    "Keine Live-Aktivierung",
    "`bootstrap.initializeClient()`",
    "`supabase.createClient()`",
    "keine direkten Auth- oder Tabellenabfragen",
    "Supabase bleibt NICHT LIVE.",
    "Keine echten Keys.",
    "Keine echten Teilnehmerdaten.",
    "Die vorhandenen v27.36b-/v27.36c-/v27.36d-/v27.36e-Module",
    "ausschließlich lokal mit synthetischen Browserzuständen",
    "Default-off, exaktes `true`, Ladefolge, Readiness, fail-closed",
    "Kein anderer Task und kein Folgetask ist ausgewählt oder autorisiert.",
    "Commit und Push bleiben NEIN.",
    "### Permanenter v27.36f-Lebenszyklus",
    "authorization_prepared",
    "authorization_committed",
    "implementation_prepared",
    "implementation_committed",
    "closure_prepared",
    "closure_committed",
    "GATE enthält ausschließlich eine nichtleere Teilmenge der fünf Gate-Dateien.",
    "IMPLEMENTATION enthält exakt die sechs autorisierten Implementierungsdateien",
    "CLOSURE ist erst nach IMPLEMENTATION zulässig",
    "Keine zukünftige GATE-, IMPLEMENTATION- oder CLOSURE-SHA wird hartcodiert.",
    "Rückkehr zu einem autorisierten v27.36f-Zustand bleibt nach der Closure ohne neue ausdrückliche Autorisierung blockiert.",
)
V2736F_CLOSURE_MARKERS = (
    "v27.36f abgeschlossen.",
    f"Loader-ID: `{V2736F_LOADER_ID}`.",
    "Der finale Default bleibt `data-enabled=\"false\"`.",
    "Nur der exakte Attributwert `\"true\"` fordert die Aktivierung an.",
    "Bei deaktiviertem Schalter bleibt der lokale Standardbetrieb unverändert und nicht blockierend.",
    "Bei angeforderter Aktivierung werden Adapter, Brücke und Browser-Provider in fester Reihenfolge geladen.",
    "Die Readiness-Oberfläche ist `window.ACCAOUI_PARTICIPANT_ACCESS_BROWSER_LOADER_READY`.",
    "`app.js` verwendet weiterhin den v27.36d-Providervertrag mit `resolveAccess()`.",
    "Fehler bei angeforderter Aktivierung bleiben fail-closed ohne lokalen Fallback.",
    "Keine Fachlogik wurde dupliziert.",
    "Supabase bleibt NICHT LIVE.",
    "Keine echten Keys.",
    "Keine echten Teilnehmerdaten.",
    "v27.36f-Checker: PASS.",
    "v27.36b-/v27.36c-/v27.36d-/v27.36e-Regressionen: PASS.",
    "Kontinuitätschecker: PASS.",
    "Preflight: PASS.",
    "`git diff --check`: PASS.",
    "Kein Folgetask wurde ausgewählt oder autorisiert.",
    "### Permanenter v27.36f-Lebenszyklus",
    "authorization_prepared",
    "authorization_committed",
    "implementation_prepared",
    "implementation_committed",
    "closure_prepared",
    "closure_committed",
    "Keine zukünftige CLOSURE-SHA wird hartcodiert.",
    "Rückkehr zu einem autorisierten v27.36f-Zustand bleibt ohne neue ausdrückliche Autorisierung blockiert.",
)
V2736F_POST_REPAIR_CLOSURE_MARKERS = (
    "Der technische Stand ist v27.36f vollständig abgeschlossen.",
    "Zusätzlicher enger Prüfpfad-Repair: v27.36f-REPAIR.",
    "v27.36f-REPAIR vollständig abgeschlossen.",
    "`closure_prepared` wird korrekt geprüft.",
    "`closure_committed` wird dynamisch geprüft.",
    "Die v27.36e-Regression bleibt über das enge v27.36f-Profil geschützt.",
    "Der Repair-Lifecycle ist vollständig geschlossen.",
    "Es gibt keinen pauschalen Bypass.",
    "Rückkehr zu `v27.36f-REPAIR / AUTHORIZED` bleibt ohne neue ausdrückliche Autorisierung blockiert.",
    "Eine erneute v27.36f-IMPLEMENTATION ist nach `closure_committed` unzulässig.",
)
V2736F_TASK_AUTHORIZED = "authorized"
V2736F_TASK_CLOSED = "closed"
V2736F_HISTORY_BEFORE_AUTHORIZATION = "before_authorization_commit"
V2736F_HISTORY_AUTHORIZED = "authorization_committed"
V2736F_HISTORY_IMPLEMENTED = "implementation_committed"
V2736F_HISTORY_CLOSED = "closure_committed"
V2736F_PHASE_AUTHORIZATION_PREPARED = "authorization_prepared"
V2736F_PHASE_AUTHORIZATION_COMMITTED = "authorization_committed"
V2736F_PHASE_IMPLEMENTATION_PREPARED = "implementation_prepared"
V2736F_PHASE_IMPLEMENTATION_COMMITTED = "implementation_committed"
V2736F_PHASE_CLOSURE_PREPARED = "closure_prepared"
V2736F_PHASE_CLOSURE_COMMITTED = "closure_committed"
V2736F_ROLE_GATE = "GATE"
V2736F_ROLE_IMPLEMENTATION = "IMPLEMENTATION"
V2736F_ROLE_CLOSURE = "CLOSURE"


@dataclass(frozen=True)
class V2736FCommitFact:
    commit_sha: str
    changed_files: frozenset[str]
    task_state: str


@dataclass(frozen=True)
class V2736FHistoryState:
    state: str
    implementation_commit: str | None
    roles: tuple[str, ...]
    gate_commits: tuple[str, ...]


@dataclass(frozen=True)
class V2736FWorkingTreeFact:
    branch: str
    head: str
    origin_main: str
    diff_files: frozenset[str]
    staged_files: frozenset[str]
    untracked_files: frozenset[str]
    status_lines: frozenset[str]
    new_files_existing: frozenset[str]
    new_files_tracked_at_base: frozenset[str]
    new_files_tracked_at_head: frozenset[str]
    base_is_head_ancestor: bool
    base_is_origin_ancestor: bool
    origin_is_head_ancestor: bool


def validate_v2736e_completed_base() -> tuple[V2736EHistoryState, tuple[str, str, str, str]]:
    require(
        git_is_ancestor(V2736E_AUTHORIZATION_BASE_SHA, V2736F_AUTHORIZATION_BASE_SHA),
        "v27.36e-Basis ist kein Vorfahr des v27.36e-Closure-HEAD",
    )
    facts = read_v2736e_commit_facts(V2736F_AUTHORIZATION_BASE_SHA)
    history = validate_v2736e_history_facts(facts)
    require(history.state == V2736E_HISTORY_CLOSED, "v27.36e muss an der v27.36f-Basis vollständig geschlossen sein")
    require(history.implementation_commit is not None, "v27.36e benötigt an der v27.36f-Basis exakt eine IMPLEMENTATION")
    require(history.roles.count(V2736E_ROLE_IMPLEMENTATION) == 1, "v27.36e benötigt exakt einen IMPLEMENTATION-Commit")
    require(history.roles.count(V2736E_ROLE_CLOSURE) == 1 and history.roles[-1] == V2736E_ROLE_CLOSURE, "v27.36e-Closure muss exakt einmal und zuletzt vorliegen")
    require(facts and facts[-1].commit_sha == V2736F_AUTHORIZATION_BASE_SHA, "Verbindlicher v27.36e-Closure-HEAD wurde nicht erkannt")
    require(facts[-1].changed_files == frozenset(EXPECTED_CONTROL_FILES), "v27.36e-Closure-HEAD muss exakt die fünf Gate-Dateien ändern")
    validate_v2736e_committed_closure_documents(facts, history)
    validate_v2736e_source_contract_at_revision(history.implementation_commit)
    documents = (
        read_v2735f_commit_document(V2736F_AUTHORIZATION_BASE_SHA, "docs/PROJECT_STATE_CURRENT.md"),
        read_v2735f_commit_document(V2736F_AUTHORIZATION_BASE_SHA, V2735F_TASK_RELATIVE_PATH),
        read_v2735f_commit_document(V2736F_AUTHORIZATION_BASE_SHA, "docs/CURSOR_MASTER_CONTEXT_ACCAOUI.md"),
        read_v2735f_commit_document(V2736F_AUTHORIZATION_BASE_SHA, "docs/PROJECT_MASTERLIST.md"),
    )
    validate_v2736e_closed_documents(*documents, history.implementation_commit)
    return history, documents


def synthetic_v2736e_closed_working_fact() -> V2736EWorkingTreeFact:
    return V2736EWorkingTreeFact(
        branch="main",
        head=V2736F_AUTHORIZATION_BASE_SHA,
        origin_main=V2736F_AUTHORIZATION_BASE_SHA,
        diff_files=frozenset(),
        staged_files=frozenset(),
        untracked_files=frozenset(),
        status_lines=frozenset(),
        new_files_existing=V2736E_NEW_IMPLEMENTATION_FILES,
        new_files_tracked_at_base=frozenset(),
        new_files_tracked_at_head=V2736E_NEW_IMPLEMENTATION_FILES,
        base_is_head_ancestor=True,
        base_is_origin_ancestor=True,
        origin_is_head_ancestor=True,
    )


def validate_no_future_v2736f_sha(section: str, allowed_shas: frozenset[str], document_name: str) -> None:
    shas = frozenset(re.findall(r"\b[0-9a-f]{40}\b", section))
    require(shas.issubset(allowed_shas), f"{document_name}: zukünftige v27.36f-Commit-SHA hartcodiert: {sorted(shas - allowed_shas)}")
    require(re.search(r"\bv27\.(?:36[g-z]|3[7-9])\b", section, re.IGNORECASE) is None, f"{document_name}: automatischer Folgetask nach v27.36f unzulässig")


def extract_v2736f_authorization_section(text: str, document_name: str) -> str:
    heading_prefix = "##" if document_name in {"PROJECT_STATE_CURRENT", "CURRENT_TASK"} else "###"
    return section_between(
        text,
        f"{heading_prefix} Autorisierter Task v27.36f",
        f"{heading_prefix} Abgeschlossener technischer Schritt v27.36e",
        document_name,
    )


def extract_v2736f_closure_section(text: str, document_name: str) -> str:
    heading_prefix = "##" if document_name in {"PROJECT_STATE_CURRENT", "CURRENT_TASK"} else "###"
    return section_between(
        text,
        f"{heading_prefix} Abgeschlossener technischer Schritt v27.36f",
        f"{heading_prefix} Abgeschlossener technischer Schritt v27.36e",
        document_name,
    )


def validate_v2736f_implementation_file_list(
    section: str,
    document_name: str,
    start_marker: str,
    end_marker: str,
) -> None:
    require(section.count(start_marker) == 1, f"{document_name}: v27.36f-Dateilistenanfang fehlt oder ist doppelt")
    require(section.count(end_marker) == 1, f"{document_name}: v27.36f-Dateilistenende fehlt oder ist doppelt")
    list_text = section.split(start_marker, 1)[1].split(end_marker, 1)[0].strip()
    expected_text = "\n".join(f"- `{path}`" for path in V2736F_IMPLEMENTATION_FILE_ORDER)
    require(list_text == expected_text, f"{document_name}: v27.36f-Dateiliste muss exakt sechs eindeutige kanonische Listenzeilen enthalten")
    listed_paths = tuple(re.findall(r"(?m)^- `([^`\r\n]+)`$", list_text))
    require(len(listed_paths) == 6, f"{document_name}: v27.36f-Dateiliste muss exakt sechs Zeilen enthalten")
    require(len(set(listed_paths)) == 6, f"{document_name}: v27.36f-Dateiliste enthält eine doppelte Zeile")
    require(listed_paths == V2736F_IMPLEMENTATION_FILE_ORDER, f"{document_name}: v27.36f-Dateiliste ist unvollständig, erweitert oder falsch geordnet")


def replace_v2736f_implementation_file_list(
    section: str,
    start_marker: str,
    end_marker: str,
    replacement_lines: tuple[str, ...],
) -> str:
    require(section.count(start_marker) == 1, "v27.36f-Manipulation benötigt einen eindeutigen Dateilistenanfang")
    require(section.count(end_marker) == 1, "v27.36f-Manipulation benötigt ein eindeutiges Dateilistenende")
    list_start = section.index(start_marker) + len(start_marker)
    list_end = section.index(end_marker, list_start)
    current_lines = tuple(line.strip() for line in section[list_start:list_end].splitlines() if line.strip())
    expected_lines = tuple(f"- `{path}`" for path in V2736F_IMPLEMENTATION_FILE_ORDER)
    require(current_lines == expected_lines, "v27.36f-Manipulation benötigt die unveränderte kanonische Dateiliste")
    replacement_block = "\n\n" + "\n".join(replacement_lines) + "\n\n"
    return section[:list_start] + replacement_block + section[list_end:]


def replace_v2736f_document_section(document: str, section: str, replacement: str) -> str:
    require(document.count(section) == 1, "v27.36f-Manipulation benötigt einen eindeutig abgegrenzten Vertragsabschnitt")
    section_start = document.index(section)
    return document[:section_start] + replacement + document[section_start + len(section):]


def validate_v2736f_authorization_section(section: str, document_name: str) -> None:
    validate_required_markers(section, V2736F_AUTHORIZATION_MARKERS, f"{document_name} / v27.36f")
    validate_no_future_v2736f_sha(section, frozenset({V2736F_AUTHORIZATION_BASE_SHA}), f"{document_name} / v27.36f")
    validate_v2736f_implementation_file_list(
        section,
        document_name,
        "Für die spätere IMPLEMENTATION sind exakt sechs Dateien erlaubt:",
        "Verbindlicher Aktivierungsvertrag:",
    )


def validate_v2736f_state_text(text: str) -> None:
    validate_exact_fields(text, V2736F_EXPECTED_STATE_FIELDS)
    validate_v2736f_authorization_section(
        extract_v2736f_authorization_section(text, "PROJECT_STATE_CURRENT"),
        "PROJECT_STATE_CURRENT",
    )


def validate_v2736f_task_text(text: str) -> None:
    validate_exact_fields(text, V2736F_EXPECTED_TASK_FIELDS)
    require(text.count(f"Erlaubte Implementierungsdateien: {V2736F_ALLOWED_FILES_VALUE}") == 1, "CURRENT_TASK muss exakt eine verbindliche v27.36f-Dateifreigabe enthalten")
    validate_v2736f_authorization_section(
        extract_v2736f_authorization_section(text, "CURRENT_TASK"),
        "CURRENT_TASK",
    )


def validate_v2736f_cursor_text(text: str) -> None:
    require(exact_field(text, "Stand") == "v27.36f", "CURSOR-Kontext muss auf v27.36f stehen")
    validate_project_paths(text, "CURSOR_MASTER_CONTEXT_ACCAOUI")
    validate_v2736f_authorization_section(
        extract_v2736f_authorization_section(text, "CURSOR_MASTER_CONTEXT_ACCAOUI"),
        "CURSOR_MASTER_CONTEXT_ACCAOUI",
    )


def validate_v2736f_masterlist_text(text: str) -> None:
    require(exact_field(text, "Stand") == "v27.36f", "PROJECT_MASTERLIST muss auf v27.36f stehen")
    validate_v2736d_permanent_masterlist_contract(text)
    rows = re.findall(r"(?m)^\| v27\.36f \|.*$", text)
    require(len(rows) == 1 and "**autorisiert**" in rows[0], "PROJECT_MASTERLIST muss v27.36f exakt einmal als autorisiert führen")
    validate_v2736f_authorization_section(
        extract_v2736f_authorization_section(text, "PROJECT_MASTERLIST"),
        "PROJECT_MASTERLIST",
    )


def validate_v2736e_historical_sections_unchanged(
    current_documents: tuple[str, str, str, str],
    base_documents: tuple[str, str, str, str],
) -> None:
    names = ("PROJECT_STATE_CURRENT", "CURRENT_TASK", "CURSOR_MASTER_CONTEXT_ACCAOUI", "PROJECT_MASTERLIST")
    for current, base, name in zip(current_documents, base_documents, names):
        require(
            extract_v2736e_closure_section(current, name) == extract_v2736e_closure_section(base, name),
            f"{name}: abgeschlossener v27.36e-Vertragsbereich wurde verändert",
        )
    current_rows = re.findall(r"(?m)^\| v27\.36e \|.*$", current_documents[3])
    base_rows = re.findall(r"(?m)^\| v27\.36e \|.*$", base_documents[3])
    require(current_rows == base_rows and len(current_rows) == 1, "PROJECT_MASTERLIST: historischer v27.36e-Abschluss wurde verändert")


def detect_v2736f_task_state_text(text: str) -> str:
    task_id = exact_field(text, "Task-ID")
    if task_id == "v27.36f":
        validate_exact_fields(text, V2736F_EXPECTED_TASK_FIELDS)
        return V2736F_TASK_AUTHORIZED
    if task_id == "NONE":
        validate_exact_fields(text, V2736F_CLOSED_TASK_FIELDS)
        return V2736F_TASK_CLOSED
    raise ValidationError(f"Unzulässiger v27.36f-Taskzustand: {task_id}")


def validate_v2736f_closed_documents(
    state_text: str,
    task_text: str,
    cursor_text: str,
    masterlist_text: str,
    implementation_commit: str,
    additional_allowed_shas: frozenset[str] = frozenset(),
) -> None:
    require(re.fullmatch(r"[0-9a-f]{40}", implementation_commit) is not None, "v27.36f-Closure benötigt einen dynamisch erkannten Implementierungscommit")
    validate_exact_fields(state_text, V2736F_CLOSED_STATE_FIELDS)
    validate_exact_fields(task_text, V2736F_CLOSED_TASK_FIELDS)
    require(exact_field(cursor_text, "Stand") == "v27.36f", "CURSOR-Kontext muss nach v27.36f-Closure auf v27.36f stehen")
    require(exact_field(masterlist_text, "Stand") == "v27.36f", "PROJECT_MASTERLIST muss nach v27.36f-Closure auf v27.36f stehen")
    validate_project_paths(cursor_text, "CURSOR_MASTER_CONTEXT_ACCAOUI")
    validate_v2736d_permanent_masterlist_contract(masterlist_text)
    documents = (state_text, task_text, cursor_text, masterlist_text)
    names = ("PROJECT_STATE_CURRENT", "CURRENT_TASK", "CURSOR_MASTER_CONTEXT_ACCAOUI", "PROJECT_MASTERLIST")
    for text, name in zip(documents, names):
        section = extract_v2736f_closure_section(text, name)
        validate_required_markers(section, V2736F_CLOSURE_MARKERS, f"{name} / v27.36f-Closure")
        require(section.count(f"Implementierungscommit: `{implementation_commit}`") == 1, f"{name}: dynamischer v27.36f-Implementierungscommit fehlt oder ist doppelt")
        validate_no_future_v2736f_sha(
            section,
            frozenset({V2736F_AUTHORIZATION_BASE_SHA, implementation_commit})
            | additional_allowed_shas,
            f"{name} / v27.36f-Closure",
        )
        validate_v2736f_implementation_file_list(section, name, "Umgesetzte Dateien:", "Ergebnis:")
    rows = re.findall(r"(?m)^\| v27\.36f \|.*$", masterlist_text)
    require(len(rows) == 1 and "**erledigt**" in rows[0] and implementation_commit in rows[0], "PROJECT_MASTERLIST muss v27.36f nach Closure exakt einmal als erledigt führen")


def read_v2736f_commit_facts(current_head: str) -> tuple[V2736FCommitFact, ...]:
    shas = tuple(line.strip() for line in run_git(["rev-list", "--reverse", f"{V2736F_AUTHORIZATION_BASE_SHA}..{current_head}"]).splitlines() if line.strip())
    previous = V2736F_AUTHORIZATION_BASE_SHA
    facts: list[V2736FCommitFact] = []
    for sha in shas:
        lineage = run_git(["rev-list", "--parents", "-n", "1", sha]).split()
        require(len(lineage) == 2 and lineage[1] == previous, "v27.36f erlaubt nur eine lineare Historie ohne Merge-Commit")
        files = frozenset(line.strip().replace("\\", "/") for line in run_git(["diff", "--name-only", previous, sha]).splitlines() if line.strip())
        require(files, f"Leerer v27.36f-Commit unzulässig: {sha}")
        task_text = read_v2735f_commit_document(sha, V2735F_TASK_RELATIVE_PATH)
        facts.append(V2736FCommitFact(sha, files, detect_v2736f_task_state_text(task_text)))
        previous = sha
    return tuple(facts)


def validate_v2736f_history_facts(facts: tuple[V2736FCommitFact, ...]) -> V2736FHistoryState:
    gate_files = frozenset(EXPECTED_CONTROL_FILES)
    roles: list[str] = []
    gate_commits: list[str] = []
    implementation_commit: str | None = None
    closed = False
    for fact in facts:
        files = fact.changed_files
        if files == V2736F_IMPLEMENTATION_FILES:
            require(gate_commits, "v27.36f-IMPLEMENTATION vor Autorisierungs-GATE unzulässig")
            require(implementation_commit is None, "Mehr als ein v27.36f-IMPLEMENTATION-Commit unzulässig")
            require(not closed, "v27.36f-IMPLEMENTATION nach CLOSURE unzulässig")
            require(fact.task_state == V2736F_TASK_AUTHORIZED, "v27.36f-IMPLEMENTATION benötigt AUTHORIZED / Autorisiert JA")
            implementation_commit = fact.commit_sha
            roles.append(V2736F_ROLE_IMPLEMENTATION)
            continue
        require(files and files.issubset(gate_files), f"Fremde Datei in v27.36f-Commit {fact.commit_sha}: {sorted(files - gate_files)}")
        if fact.task_state == V2736F_TASK_AUTHORIZED:
            require(not closed, "Rückkehr zu v27.36f / AUTHORIZED nach CLOSURE unzulässig")
            gate_commits.append(fact.commit_sha)
            roles.append(V2736F_ROLE_GATE)
            continue
        require(implementation_commit is not None, "v27.36f-CLOSURE vor IMPLEMENTATION unzulässig")
        require(not closed, "Mehr als ein v27.36f-CLOSURE-Commit unzulässig")
        require(files == gate_files, "v27.36f-CLOSURE muss exakt die fünf Gate-Dateien ändern")
        closed = True
        roles.append(V2736F_ROLE_CLOSURE)
    state = V2736F_HISTORY_CLOSED if closed else V2736F_HISTORY_IMPLEMENTED if implementation_commit else V2736F_HISTORY_AUTHORIZED if gate_commits else V2736F_HISTORY_BEFORE_AUTHORIZATION
    return V2736FHistoryState(state, implementation_commit, tuple(roles), tuple(gate_commits))


def read_v2736f_working_tree_fact() -> V2736FWorkingTreeFact:
    head = run_git(["rev-parse", "HEAD"]).strip()
    origin_main = run_git(["rev-parse", "origin/main"]).strip()

    def tracked_at(revision: str) -> frozenset[str]:
        return frozenset(line.strip().replace("\\", "/") for line in run_git(["ls-tree", "-r", "--name-only", revision, "--", *sorted(V2736F_NEW_IMPLEMENTATION_FILES)]).splitlines() if line.strip())

    return V2736FWorkingTreeFact(
        branch=run_git(["branch", "--show-current"]).strip(),
        head=head,
        origin_main=origin_main,
        diff_files=frozenset(line.strip().replace("\\", "/") for line in run_git(["diff", "--name-only"]).splitlines() if line.strip()),
        staged_files=frozenset(line.strip().replace("\\", "/") for line in run_git(["diff", "--cached", "--name-only"]).splitlines() if line.strip()),
        untracked_files=frozenset(line.strip().replace("\\", "/") for line in run_git(["ls-files", "--others", "--exclude-standard"]).splitlines() if line.strip()),
        status_lines=frozenset(line.replace("\\", "/") for line in run_git(["status", "--porcelain=v1", "--untracked-files=all"]).splitlines() if line),
        new_files_existing=frozenset(path for path in V2736F_NEW_IMPLEMENTATION_FILES if (ROOT / path).is_file()),
        new_files_tracked_at_base=tracked_at(V2736F_AUTHORIZATION_BASE_SHA),
        new_files_tracked_at_head=tracked_at(head),
        base_is_head_ancestor=git_is_ancestor(V2736F_AUTHORIZATION_BASE_SHA, head),
        base_is_origin_ancestor=git_is_ancestor(V2736F_AUTHORIZATION_BASE_SHA, origin_main),
        origin_is_head_ancestor=git_is_ancestor(origin_main, head),
    )


def validate_v2736f_working_tree_fact(fact: V2736FWorkingTreeFact) -> None:
    require(fact.branch == "main", "v27.36f-Lebenszyklus muss auf main laufen")
    require(fact.base_is_head_ancestor, "Die stabile v27.36f-Basis ist kein Vorfahr von HEAD")
    require(fact.base_is_origin_ancestor, "Die stabile v27.36f-Basis ist kein Vorfahr von origin/main")
    require(fact.origin_is_head_ancestor, "origin/main ist kein Vorfahr des lokalen v27.36f-HEAD")
    require(not fact.new_files_tracked_at_base, "Neue v27.36f-Implementierungsdateien dürfen an der Basis nicht existieren")
    require(not fact.staged_files, "v27.36f-Lebenszyklus darf nichts stagen")


def validate_v2736f_source_contract(index_text: str, app_text: str, app_added: str, loader_text: str, checker_text: str, report_text: str, preflight_text: str) -> None:
    loader_pattern = re.compile(
        rf"<script\b(?=[^>]*\bid=[\"']{re.escape(V2736F_LOADER_ID)}[\"'])(?=[^>]*\bsrc=[\"']data/supabase-participant-access-browser-loader\.js[\"'])(?=[^>]*\bdata-enabled=[\"']false[\"'])[^>]*>\s*</script>",
        re.IGNORECASE,
    )
    loader_tags = tuple(loader_pattern.finditer(index_text))
    require(len(loader_tags) == 1, "v27.36f-index benötigt exakt einen Loader-Tag mit stabiler ID und Default false")
    require(index_text.count(V2736F_LOADER_ID) == 1, "v27.36f-Loader-ID muss in index.html exakt einmal vorkommen")
    require(index_text.count("data/supabase-participant-access-browser-loader.js") == 1, "v27.36f-Loader-Script muss in index.html exakt einmal vorkommen")
    app_tag = re.search(r"<script\b[^>]*\bsrc=[\"']app\.js[^\"']*[\"'][^>]*>", index_text, re.IGNORECASE)
    require(app_tag is not None and loader_tags[0].start() < app_tag.start(), "v27.36f-Loader muss unmittelbar vor der app.js-Ladephase liegen")
    require(not re.search(rf"id=[\"']{re.escape(V2736F_LOADER_ID)}[\"'][^>]*data-enabled=[\"']true[\"']", index_text, re.IGNORECASE), "v27.36f-Default darf nicht true sein")
    ordered_dependencies = (
        "data/supabase-participant-access-adapter.js",
        "data/supabase-participant-access-bootstrap-bridge.js",
        "data/supabase-participant-access-browser-provider.js",
    )
    positions = tuple(loader_text.find(path) for path in ordered_dependencies)
    require(all(position >= 0 for position in positions) and list(positions) == sorted(positions), "v27.36f-Loader muss Adapter, Brücke und Browser-Provider in fester Reihenfolge binden")
    for marker in (V2736F_LOADER_ID, "data-enabled", "true", "ACCAOUI_PARTICIPANT_ACCESS_BROWSER_LOADER_READY", "ACCAOUI_PARTICIPANT_ACCESS_APP_PROVIDER"):
        require(marker in loader_text, f"v27.36f-Loader fehlt Vertragsmarker: {marker}")
    for token in ("localStorage", "sessionStorage", "document.cookie", "location.search", "initializeClient(", "createClient(", "getSession(", ".from(", "fetch(", "XMLHttpRequest", "WebSocket", "userId"):
        require(token.casefold() not in loader_text.casefold(), f"v27.36f-Loader verletzt Sicherheitsgrenze: {token}")
    for marker in (V2736F_LOADER_ID, "ACCAOUI_PARTICIPANT_ACCESS_BROWSER_LOADER_READY", "access_error"):
        require(marker in app_added, f"v27.36f-app.js-Diff fehlt Loadervertrag: {marker}")
    for marker in ("ACCAOUI_PARTICIPANT_ACCESS_APP_PROVIDER", "resolveAccess"):
        require(marker in app_text, f"v27.36f-app.js fehlt bestehender Providervertrag: {marker}")
    for token in ("ACCAOUI_SUPABASE_BOOTSTRAP", "ACCAOUI_PARTICIPANT_ACCESS_ADAPTER_FACTORY", "ACCAOUI_PARTICIPANT_ACCESS_BOOTSTRAP_BRIDGE_FACTORY", "initializeClient(", "createClient(", "getSession(", ".from("):
        require(token.casefold() not in app_added.casefold(), f"v27.36f-app.js-Diff dupliziert verbotene Zugriffslogik: {token}")
    for marker in ("synthet", "data-enabled", "false", "true", "Ladefolge", "Readiness", "fail-closed", "kein Fallback", "v27.36e"):
        require(marker.casefold() in checker_text.casefold(), f"v27.36f-Checker fehlt Testbindung: {marker}")
    for marker in ("Ziel", "Schalter", "Ladefolge", "Readiness", "Fail-closed-Grenze", "lokale synthetische Tests", "Supabase live: NEIN", "echte Keys: NEIN", "echte Teilnehmerdaten: NEIN"):
        require(marker in report_text, f"v27.36f-Umsetzungsbericht fehlt: {marker}")
    require("check-participant-access-browser-loader-v2736f.py" in preflight_text, "v27.36f-Checker fehlt im Preflight")


def validate_v2736f_local_source_contract() -> None:
    validate_v2736f_source_contract(
        read_required_text(ROOT / "index.html"),
        read_required_text(ROOT / "app.js"),
        extract_added_lines(run_git(["diff", "--unified=0", V2736F_AUTHORIZATION_BASE_SHA, "--", "app.js"])),
        read_required_text(ROOT / "data/supabase-participant-access-browser-loader.js"),
        read_required_text(ROOT / "tools/check-participant-access-browser-loader-v2736f.py"),
        read_required_text(ROOT / "docs/PARTICIPANT_ACCESS_BROWSER_LOADER_V2736F.md"),
        read_required_text(PREFLIGHT_PATH),
    )


def validate_v2736f_source_contract_at_revision(revision: str) -> None:
    parent = run_git(["rev-parse", f"{revision}^"]).strip()
    validate_v2736f_source_contract(
        read_v2735f_commit_document(revision, "index.html"),
        read_v2735f_commit_document(revision, "app.js"),
        extract_added_lines(run_git(["diff", "--unified=0", parent, revision, "--", "app.js"])),
        read_v2735f_commit_document(revision, "data/supabase-participant-access-browser-loader.js"),
        read_v2735f_commit_document(revision, "tools/check-participant-access-browser-loader-v2736f.py"),
        read_v2735f_commit_document(revision, "docs/PARTICIPANT_ACCESS_BROWSER_LOADER_V2736F.md"),
        read_v2735f_commit_document(revision, "tools/preflight.py"),
    )


def validate_v2736f_lifecycle_working_tree(history: V2736FHistoryState, task_state: str, fact: V2736FWorkingTreeFact) -> str:
    validate_v2736f_working_tree_fact(fact)
    gate_files = frozenset(EXPECTED_CONTROL_FILES)
    clean = not fact.diff_files and not fact.untracked_files and not fact.status_lines
    if history.state == V2736F_HISTORY_BEFORE_AUTHORIZATION:
        require(fact.head == V2736F_AUTHORIZATION_BASE_SHA, "Autorisierungsvorbereitung benötigt die stabile v27.36f-Basis als HEAD")
        require(task_state == V2736F_TASK_AUTHORIZED, "Autorisierungsvorbereitung benötigt v27.36f / AUTHORIZED")
        require(fact.diff_files and fact.diff_files.issubset(gate_files), "Autorisierungsvorbereitung darf nur eine nichtleere Teilmenge der fünf Gate-Dateien ändern")
        require(not fact.untracked_files and fact.status_lines == frozenset(f" M {path}" for path in fact.diff_files), "Working Tree entspricht nicht authorization_prepared")
        require(not fact.new_files_existing, "v27.36f-Implementation vor Autorisierungscommit unzulässig")
        return V2736F_PHASE_AUTHORIZATION_PREPARED
    if history.state == V2736F_HISTORY_AUTHORIZED:
        require(fact.head != V2736F_AUTHORIZATION_BASE_SHA, "Autorisierungscommit fehlt")
        require(task_state == V2736F_TASK_AUTHORIZED, "Autorisierte Phasen benötigen v27.36f / AUTHORIZED")
        require(not fact.new_files_tracked_at_head, "Neue v27.36f-Dateien dürfen vor IMPLEMENTATION nicht getrackt sein")
        if clean:
            require(not fact.new_files_existing, "Implementation darf vor preparation nicht lokal existieren")
            return V2736F_PHASE_AUTHORIZATION_COMMITTED
        if fact.diff_files and fact.diff_files.issubset(gate_files) and not fact.untracked_files:
            require(fact.status_lines == frozenset(f" M {path}" for path in fact.diff_files), "Lokale v27.36f-Gate-Korrektur enthält fremden Status")
            require(not fact.new_files_existing, "Implementation während Gate-Korrektur unzulässig")
            return V2736F_PHASE_AUTHORIZATION_COMMITTED
        require(fact.diff_files == V2736F_EXISTING_IMPLEMENTATION_FILES, "implementation_prepared muss exakt die drei bestehenden Implementierungsdateien ändern")
        require(fact.untracked_files == V2736F_NEW_IMPLEMENTATION_FILES, "implementation_prepared benötigt exakt die drei neuen Implementierungsdateien")
        require(fact.new_files_existing == V2736F_NEW_IMPLEMENTATION_FILES, "implementation_prepared benötigt alle drei neuen Dateien")
        expected_status = frozenset({*(f" M {path}" for path in V2736F_EXISTING_IMPLEMENTATION_FILES), *(f"?? {path}" for path in V2736F_NEW_IMPLEMENTATION_FILES)})
        require(fact.status_lines == expected_status, "Working Tree entspricht nicht implementation_prepared")
        return V2736F_PHASE_IMPLEMENTATION_PREPARED
    require(history.implementation_commit is not None, "Phase nach IMPLEMENTATION benötigt den dynamischen Implementierungscommit")
    require(fact.new_files_tracked_at_head == V2736F_NEW_IMPLEMENTATION_FILES, "Nach IMPLEMENTATION müssen alle drei neuen Dateien getrackt sein")
    require(fact.new_files_existing == V2736F_NEW_IMPLEMENTATION_FILES, "Nach IMPLEMENTATION müssen alle drei neuen Dateien vorhanden sein")
    if history.state == V2736F_HISTORY_IMPLEMENTED:
        if task_state == V2736F_TASK_AUTHORIZED:
            if clean:
                return V2736F_PHASE_IMPLEMENTATION_COMMITTED
            require(fact.diff_files and fact.diff_files.issubset(gate_files) and not fact.untracked_files, "Nach IMPLEMENTATION sind lokal nur Gate-Korrekturen zulässig")
            require(fact.status_lines == frozenset(f" M {path}" for path in fact.diff_files), "Lokale Gate-Korrektur nach IMPLEMENTATION enthält fremden Status")
            return V2736F_PHASE_IMPLEMENTATION_COMMITTED
        require(task_state == V2736F_TASK_CLOSED, "closure_prepared benötigt den geschlossenen v27.36f-Taskzustand")
        require(fact.diff_files == gate_files and not fact.untracked_files, "closure_prepared muss exakt fünf Gate-Dateien ändern")
        require(fact.status_lines == frozenset(f" M {path}" for path in gate_files), "Working Tree entspricht nicht closure_prepared")
        return V2736F_PHASE_CLOSURE_PREPARED
    require(history.state == V2736F_HISTORY_CLOSED, "Unbekannter v27.36f-Historienzustand")
    require(task_state == V2736F_TASK_CLOSED, "Nach v27.36f-CLOSURE darf keine Rückkehr zu AUTHORIZED erfolgen")
    require(clean, "closure_committed benötigt einen sauberen Working Tree")
    return V2736F_PHASE_CLOSURE_COMMITTED


def validate_v2736f_committed_closure_documents(facts: tuple[V2736FCommitFact, ...], history: V2736FHistoryState) -> None:
    if V2736F_ROLE_CLOSURE not in history.roles:
        return
    require(history.implementation_commit is not None, "v27.36f-CLOSURE benötigt einen dynamischen Implementierungscommit")
    for fact, role in zip(facts, history.roles):
        if role == V2736F_ROLE_CLOSURE:
            validate_v2736f_closed_documents(
                read_v2735f_commit_document(fact.commit_sha, "docs/PROJECT_STATE_CURRENT.md"),
                read_v2735f_commit_document(fact.commit_sha, V2735F_TASK_RELATIVE_PATH),
                read_v2735f_commit_document(fact.commit_sha, "docs/CURSOR_MASTER_CONTEXT_ACCAOUI.md"),
                read_v2735f_commit_document(fact.commit_sha, "docs/PROJECT_MASTERLIST.md"),
                history.implementation_commit,
            )


def validate_v2736f_lifecycle(state_text: str, task_text: str, cursor_text: str, masterlist_text: str, v2736e_base_documents: tuple[str, str, str, str]) -> tuple[str, V2736FHistoryState, V2736FWorkingTreeFact]:
    current_documents = (state_text, task_text, cursor_text, masterlist_text)
    validate_v2736e_historical_sections_unchanged(current_documents, v2736e_base_documents)
    fact = read_v2736f_working_tree_fact()
    facts = read_v2736f_commit_facts(fact.head)
    history = validate_v2736f_history_facts(facts)
    validate_v2736f_committed_closure_documents(facts, history)
    task_state = detect_v2736f_task_state_text(task_text)
    if task_state == V2736F_TASK_AUTHORIZED:
        validate_v2736f_state_text(state_text)
        validate_v2736f_task_text(task_text)
        validate_v2736f_cursor_text(cursor_text)
        validate_v2736f_masterlist_text(masterlist_text)
    else:
        require(history.implementation_commit is not None, "v27.36f-Abschluss vor IMPLEMENTATION unzulässig")
        validate_v2736f_closed_documents(state_text, task_text, cursor_text, masterlist_text, history.implementation_commit)
    phase = validate_v2736f_lifecycle_working_tree(history, task_state, fact)
    if phase == V2736F_PHASE_IMPLEMENTATION_PREPARED:
        validate_v2736f_local_source_contract()
    if history.implementation_commit is not None:
        validate_v2736f_source_contract_at_revision(history.implementation_commit)
    return phase, history, fact


def run_v2736f_manipulation_matrix(state_text: str, task_text: str, cursor_text: str, masterlist_text: str, current_history: V2736FHistoryState, current_fact: V2736FWorkingTreeFact) -> tuple[int, int, int]:
    checks = 0

    def rejected(validator: Callable[[str], None], manipulated: str, label: str) -> None:
        nonlocal checks
        try:
            validator(manipulated)
        except ValidationError:
            checks += 1
            return
        raise ValidationError(f"v27.36f-Manipulation wurde nicht blockiert: {label}")

    current_task_state = detect_v2736f_task_state_text(task_text)
    if current_task_state == V2736F_TASK_CLOSED:
        require(current_history.gate_commits, "v27.36f-Closure benötigt einen historischen Autorisierungscommit")
        authorization_revision = current_history.gate_commits[-1]
        authorization_documents = (
            read_v2735f_commit_document(authorization_revision, "docs/PROJECT_STATE_CURRENT.md"),
            read_v2735f_commit_document(authorization_revision, V2735F_TASK_RELATIVE_PATH),
            read_v2735f_commit_document(authorization_revision, "docs/CURSOR_MASTER_CONTEXT_ACCAOUI.md"),
            read_v2735f_commit_document(authorization_revision, "docs/PROJECT_MASTERLIST.md"),
        )
    else:
        authorization_documents = (state_text, task_text, cursor_text, masterlist_text)
    authorization_state, authorization_task, authorization_cursor, authorization_masterlist = authorization_documents
    for text, validator, fields, name in (
        (authorization_state, validate_v2736f_state_text, V2736F_EXPECTED_STATE_FIELDS, "PROJECT_STATE_CURRENT"),
        (authorization_task, validate_v2736f_task_text, V2736F_EXPECTED_TASK_FIELDS, "CURRENT_TASK"),
    ):
        for field, value in fields.items():
            rejected(validator, text.replace(f"{field}: {value}", f"{field}: MANIPULIERT", 1), f"{name}: Feld {field}")
    boundaries = (
        (authorization_state, validate_v2736f_state_text, "PROJECT_STATE_CURRENT"),
        (authorization_task, validate_v2736f_task_text, "CURRENT_TASK"),
        (authorization_cursor, validate_v2736f_cursor_text, "CURSOR_MASTER_CONTEXT_ACCAOUI"),
        (authorization_masterlist, validate_v2736f_masterlist_text, "PROJECT_MASTERLIST"),
    )
    for text, validator, name in boundaries:
        section = extract_v2736f_authorization_section(text, name)
        for marker in V2736F_AUTHORIZATION_MARKERS:
            require(marker in section, f"Manipulationsmatrix kann v27.36f-Pflichtaussage nicht finden: {name} / {marker}")
            changed_section = section.replace(marker, "")
            rejected(validator, text.replace(section, changed_section, 1), f"{name}: Pflichtaussage {marker}")
        canonical_list_lines = tuple(f"- `{path}`" for path in V2736F_IMPLEMENTATION_FILE_ORDER)
        for index, path in enumerate(V2736F_IMPLEMENTATION_FILE_ORDER):
            changed_lines = canonical_list_lines[:index] + canonical_list_lines[index + 1:]
            changed_section = replace_v2736f_implementation_file_list(
                section,
                "Für die spätere IMPLEMENTATION sind exakt sechs Dateien erlaubt:",
                "Verbindlicher Aktivierungsvertrag:",
                changed_lines,
            )
            rejected(
                validator,
                replace_v2736f_document_section(text, section, changed_section),
                f"{name}: Implementierungsdatei {path}",
            )
        duplicate_lines = canonical_list_lines[:1] + canonical_list_lines
        duplicate_section = replace_v2736f_implementation_file_list(
            section,
            "Für die spätere IMPLEMENTATION sind exakt sechs Dateien erlaubt:",
            "Verbindlicher Aktivierungsvertrag:",
            duplicate_lines,
        )
        rejected(
            validator,
            replace_v2736f_document_section(text, section, duplicate_section),
            f"{name}: doppelte Implementierungsdatei",
        )
        extra_lines = canonical_list_lines + ("- `unexpected.txt`",)
        extra_section = replace_v2736f_implementation_file_list(
            section,
            "Für die spätere IMPLEMENTATION sind exakt sechs Dateien erlaubt:",
            "Verbindlicher Aktivierungsvertrag:",
            extra_lines,
        )
        rejected(
            validator,
            replace_v2736f_document_section(text, section, extra_section),
            f"{name}: zusätzliche Implementierungsdatei",
        )
        manipulated_section = section + "\nZukünftiger v27.36f-Commit: `" + ("a" * 40) + "`\n"
        rejected(validator, text.replace(section, manipulated_section, 1), f"{name}: unbekannte zukünftige v27.36f-SHA")
    row = re.findall(r"(?m)^\| v27\.36f \|.*$", authorization_masterlist)
    require(len(row) == 1, "Manipulationsmatrix benötigt exakt eine v27.36f-Masterlistenzeile")
    rejected(validate_v2736f_masterlist_text, authorization_masterlist.replace(row[0], row[0].replace("**autorisiert**", "**erledigt**", 1), 1), "PROJECT_MASTERLIST: v27.36f vorzeitig erledigt")

    gate = V2736FCommitFact("1" * 40, frozenset({EXPECTED_CONTROL_FILES[0]}), V2736F_TASK_AUTHORIZED)
    implementation = V2736FCommitFact("2" * 40, V2736F_IMPLEMENTATION_FILES, V2736F_TASK_AUTHORIZED)
    closure = V2736FCommitFact("3" * 40, frozenset(EXPECTED_CONTROL_FILES), V2736F_TASK_CLOSED)
    histories = (
        validate_v2736f_history_facts(tuple()),
        validate_v2736f_history_facts((gate,)),
        validate_v2736f_history_facts((gate, implementation)),
        validate_v2736f_history_facts((gate, implementation, closure)),
    )
    clean_fact = replace(
        current_fact,
        head="1" * 40,
        diff_files=frozenset(), staged_files=frozenset(), untracked_files=frozenset(), status_lines=frozenset(),
        new_files_existing=frozenset(), new_files_tracked_at_base=frozenset(), new_files_tracked_at_head=frozenset(),
        base_is_head_ancestor=True, base_is_origin_ancestor=True, origin_is_head_ancestor=True,
    )
    gate_files = frozenset(EXPECTED_CONTROL_FILES)
    implemented_fact = replace(clean_fact, head="2" * 40, new_files_existing=V2736F_NEW_IMPLEMENTATION_FILES, new_files_tracked_at_head=V2736F_NEW_IMPLEMENTATION_FILES)
    implementation_status = frozenset({*(f" M {path}" for path in V2736F_EXISTING_IMPLEMENTATION_FILES), *(f"?? {path}" for path in V2736F_NEW_IMPLEMENTATION_FILES)})
    phase_fixtures = (
        (histories[0], V2736F_TASK_AUTHORIZED, replace(clean_fact, head=V2736F_AUTHORIZATION_BASE_SHA, diff_files=gate_files, status_lines=frozenset(f" M {path}" for path in gate_files)), V2736F_PHASE_AUTHORIZATION_PREPARED),
        (histories[1], V2736F_TASK_AUTHORIZED, clean_fact, V2736F_PHASE_AUTHORIZATION_COMMITTED),
        (histories[1], V2736F_TASK_AUTHORIZED, replace(clean_fact, diff_files=V2736F_EXISTING_IMPLEMENTATION_FILES, untracked_files=V2736F_NEW_IMPLEMENTATION_FILES, status_lines=implementation_status, new_files_existing=V2736F_NEW_IMPLEMENTATION_FILES), V2736F_PHASE_IMPLEMENTATION_PREPARED),
        (histories[2], V2736F_TASK_AUTHORIZED, implemented_fact, V2736F_PHASE_IMPLEMENTATION_COMMITTED),
        (histories[2], V2736F_TASK_CLOSED, replace(implemented_fact, diff_files=gate_files, status_lines=frozenset(f" M {path}" for path in gate_files)), V2736F_PHASE_CLOSURE_PREPARED),
        (histories[3], V2736F_TASK_CLOSED, implemented_fact, V2736F_PHASE_CLOSURE_COMMITTED),
    )
    for history, task_state, fact, expected in phase_fixtures:
        require(validate_v2736f_lifecycle_working_tree(history, task_state, fact) == expected, f"v27.36f-Positivsimulation fehlgeschlagen: {expected}")
    bad_histories = (
        ((implementation,), "Implementation vor Autorisierung"),
        ((gate, implementation, implementation), "zweite Implementation"),
        ((gate, closure), "Closure vor Implementation"),
        ((gate, implementation, closure, gate), "Rückkehr nach Closure"),
        ((gate, implementation, V2736FCommitFact("4" * 40, frozenset({EXPECTED_CONTROL_FILES[0]}), V2736F_TASK_CLOSED)), "partielle Closure"),
        ((gate, V2736FCommitFact("5" * 40, frozenset(set(V2736F_IMPLEMENTATION_FILES) - {"tools/preflight.py"}), V2736F_TASK_AUTHORIZED)), "partielle Implementation"),
        ((gate, V2736FCommitFact("6" * 40, V2736F_IMPLEMENTATION_FILES | {"style.css"}, V2736F_TASK_AUTHORIZED)), "Implementation mit style.css"),
        ((V2736FCommitFact("7" * 40, frozenset({"app.js"}), V2736F_TASK_AUTHORIZED),), "fremder Gate-Commit"),
    )
    for facts, label in bad_histories:
        try:
            validate_v2736f_history_facts(facts)
        except ValidationError:
            checks += 1
            continue
        raise ValidationError(f"v27.36f-Historienmanipulation wurde nicht blockiert: {label}")
    bad_working = (
        (current_history, V2736F_TASK_AUTHORIZED, replace(current_fact, staged_files=frozenset({EXPECTED_CONTROL_FILES[0]})), "gestagte Datei"),
        (current_history, V2736F_TASK_AUTHORIZED, replace(current_fact, diff_files=current_fact.diff_files | {"style.css"}, status_lines=current_fact.status_lines | {" M style.css"}), "fremde lokale Datei"),
        (current_history, V2736F_TASK_AUTHORIZED, replace(current_fact, untracked_files=frozenset({"unexpected.txt"}), status_lines=current_fact.status_lines | {"?? unexpected.txt"}), "fremde ungetrackte Datei"),
        (current_history, V2736F_TASK_AUTHORIZED, replace(current_fact, base_is_head_ancestor=False), "falsche Basis"),
        (current_history, V2736F_TASK_AUTHORIZED, replace(current_fact, origin_is_head_ancestor=False), "origin nicht Vorfahr"),
        (current_history, V2736F_TASK_AUTHORIZED, replace(current_fact, new_files_tracked_at_base=V2736F_NEW_IMPLEMENTATION_FILES), "neue Dateien bereits an Basis"),
        (histories[0], V2736F_TASK_AUTHORIZED, replace(clean_fact, head=V2736F_AUTHORIZATION_BASE_SHA, untracked_files=V2736F_NEW_IMPLEMENTATION_FILES, status_lines=frozenset(f"?? {path}" for path in V2736F_NEW_IMPLEMENTATION_FILES), new_files_existing=V2736F_NEW_IMPLEMENTATION_FILES), "Implementation lokal vor Autorisierung"),
        (histories[1], V2736F_TASK_CLOSED, replace(clean_fact, diff_files=gate_files, status_lines=frozenset(f" M {path}" for path in gate_files)), "Closure lokal vor Implementation"),
        (histories[3], V2736F_TASK_AUTHORIZED, implemented_fact, "Rückkehr zu AUTHORIZED nach Closure"),
    )
    for history, task_state, fact, label in bad_working:
        try:
            validate_v2736f_lifecycle_working_tree(history, task_state, fact)
        except ValidationError:
            checks += 1
            continue
        raise ValidationError(f"v27.36f-Working-Tree-Manipulation wurde nicht blockiert: {label}")

    valid_index = f'<script id="{V2736F_LOADER_ID}" src="data/supabase-participant-access-browser-loader.js" data-enabled="false"></script>\n<script src="app.js"></script>'
    valid_app_added = f"{V2736F_LOADER_ID} ACCAOUI_PARTICIPANT_ACCESS_BROWSER_LOADER_READY access_error"
    valid_app = valid_app_added + " ACCAOUI_PARTICIPANT_ACCESS_APP_PROVIDER resolveAccess"
    valid_loader = " ".join((V2736F_LOADER_ID, "data-enabled true", "data/supabase-participant-access-adapter.js", "data/supabase-participant-access-bootstrap-bridge.js", "data/supabase-participant-access-browser-provider.js", "ACCAOUI_PARTICIPANT_ACCESS_BROWSER_LOADER_READY", "ACCAOUI_PARTICIPANT_ACCESS_APP_PROVIDER"))
    valid_checker = "synthetische data-enabled false true Ladefolge Readiness fail-closed kein Fallback v27.36e"
    valid_report = "\n".join(("Ziel", "Schalter", "Ladefolge", "Readiness", "Fail-closed-Grenze", "lokale synthetische Tests", "Supabase live: NEIN", "echte Keys: NEIN", "echte Teilnehmerdaten: NEIN"))
    valid_preflight = "check-participant-access-browser-loader-v2736f.py"
    validate_v2736f_source_contract(valid_index, valid_app, valid_app_added, valid_loader, valid_checker, valid_report, valid_preflight)
    source_cases = (
        (valid_index.replace('data-enabled="false"', 'data-enabled="true"'), valid_app, valid_app_added, valid_loader, valid_checker, valid_report, valid_preflight, "Default true"),
        (valid_index + valid_index.splitlines()[0], valid_app, valid_app_added, valid_loader, valid_checker, valid_report, valid_preflight, "doppelter Loader"),
        (valid_index, valid_app, valid_app_added, valid_loader + " localStorage", valid_checker, valid_report, valid_preflight, "Storage-Steuerung"),
        (valid_index, valid_app, valid_app_added, valid_loader.replace("data/supabase-participant-access-adapter.js", "missing.js"), valid_checker, valid_report, valid_preflight, "Adapter aus Ladefolge entfernt"),
        (valid_index, valid_app, valid_app_added, valid_loader.replace("ACCAOUI_PARTICIPANT_ACCESS_BROWSER_LOADER_READY", ""), valid_checker, valid_report, valid_preflight, "Readiness entfernt"),
        (valid_index, valid_app, valid_app_added.replace("access_error", ""), valid_loader, valid_checker, valid_report, valid_preflight, "generischer App-Fehler entfernt"),
        (valid_index, valid_app, valid_app_added + " .from(", valid_loader, valid_checker, valid_report, valid_preflight, "direkte Tabellenlogik in app.js"),
        (valid_index, valid_app, valid_app_added, valid_loader, valid_checker.replace("kein Fallback", ""), valid_report, valid_preflight, "Fallback-Prüfung entfernt"),
        (valid_index, valid_app, valid_app_added, valid_loader, valid_checker, valid_report.replace("Fail-closed-Grenze", ""), valid_preflight, "Berichtsgrenze entfernt"),
        (valid_index, valid_app, valid_app_added, valid_loader, valid_checker, valid_report, "", "Checker aus Preflight entfernt"),
    )
    for args in source_cases:
        try:
            validate_v2736f_source_contract(*args[:-1])
        except ValidationError:
            checks += 1
            continue
        raise ValidationError(f"v27.36f-Quellmanipulation wurde nicht blockiert: {args[-1]}")
    negative_tests = len(bad_histories) + len(bad_working) + len(source_cases)
    return checks, len(phase_fixtures), negative_tests


V2736F_REPAIR_BASE_SHA = "a68dd9e81f26c3a887e668b90e9f5e8973c7ddfa"
V2736F_REPAIR_TITLE = "Closure-Prüfpfad für v27.36f eng reparieren"
V2736F_REPAIR_IMPLEMENTATION_FILE_ORDER = (
    "tools/preflight.py",
    "tools/check-participant-access-browser-loader-v2736f.py",
)
V2736F_REPAIR_IMPLEMENTATION_FILES = frozenset(V2736F_REPAIR_IMPLEMENTATION_FILE_ORDER)
V2736F_REPAIR_ALLOWED_FILES_VALUE = (
    "`tools/preflight.py`, `tools/check-participant-access-browser-loader-v2736f.py`"
)
V2736F_REPAIR_EXPECTED_STATE_FIELDS = {
    "Stand": "v27.36f-REPAIR",
    "Repository": "`asarrad-bit/accaoui-34a-lernapp`",
    "Branch": "`main`",
    "Letzter abgeschlossener funktionaler Stand": "v27.35g",
    "Abschlusscommit": f"`{V2735G_COMPLETION_SHA}`",
    "Aktueller HEAD": "DYNAMISCH ZU PRÜFEN",
    "Funktionsstatus": "v27.35g abgeschlossen",
    "Weiterer funktionaler Schritt autorisiert": "NEIN",
    "Aktuell autorisierter Task": "v27.36f-REPAIR",
    "Aktuelle Taskart": "Eng begrenzte Reparatur der Closure-Prüfpfade",
    "Aktueller Blocker": (
        "KEINER für die ausdrücklich autorisierte spätere v27.36f-REPAIR-Umsetzung; "
        "in diesem Autorisierungs-GATE erfolgt noch keine Implementierung"
    ),
}
V2736F_REPAIR_EXPECTED_TASK_FIELDS = {
    "Task-ID": "v27.36f-REPAIR",
    "Status": "AUTHORIZED",
    "Autorisiert": "JA",
    "Titel": V2736F_REPAIR_TITLE,
    "Funktionaler Ausgangsstand": "v27.35g",
    "Technischer Ausgangsstand": "v27.36f-Implementierung abgeschlossen; ursprüngliche Closure ausstehend",
    "Technische Basis": f"`{V2736F_REPAIR_BASE_SHA}`",
    "Erlaubte Implementierungsdateien": V2736F_REPAIR_ALLOWED_FILES_VALUE,
    "Commit erlaubt": "NEIN",
    "Push erlaubt": "NEIN",
}
V2736F_REPAIR_CLOSED_STATE_FIELDS = {
    "Stand": "v27.36f-REPAIR",
    "Repository": "`asarrad-bit/accaoui-34a-lernapp`",
    "Branch": "`main`",
    "Letzter abgeschlossener funktionaler Stand": "v27.35g",
    "Abschlusscommit": f"`{V2735G_COMPLETION_SHA}`",
    "Aktueller HEAD": "DYNAMISCH ZU PRÜFEN",
    "Funktionsstatus": "v27.35g abgeschlossen",
    "Weiterer funktionaler Schritt autorisiert": "NEIN",
    "Aktuell autorisierter Task": "NONE",
    "Aktuelle Taskart": "Kein Task autorisiert",
    "Aktueller Blocker": (
        "Neue Taskauswahl und ausdrückliche Autorisierung durch "
        "Projekteigentümer und verbindlichen Projektchat"
    ),
}
V2736F_REPAIR_CLOSED_TASK_FIELDS = {
    "Task-ID": "NONE",
    "Status": "BLOCKED",
    "Autorisiert": "NEIN",
    "Titel": "Kein Task autorisiert",
    "Funktionaler Ausgangsstand": "v27.35g",
    "Letzter abgeschlossener Kontrollschritt": "v27.36f-REPAIR",
    "Erlaubte Implementierungsdateien": "KEINE",
    "Commit erlaubt": "NEIN",
    "Push erlaubt": "NEIN",
}
V2736F_REPAIR_AUTHORIZATION_MARKERS = (
    "v27.36f-REPAIR ist der einzige autorisierte Task.",
    V2736F_REPAIR_TITLE + ".",
    "Dieser GATE-Schritt autorisiert ausschließlich die spätere Repair-Implementierung",
    "Die funktionale Grundlage bleibt v27.35g.",
    f"Die v27.36f-Implementierung ist im Commit `{V2736F_REPAIR_BASE_SHA}` abgeschlossen und bleibt unverändert.",
    "Der ursprüngliche v27.36f-Closure-Schritt bleibt separat abzuschließen.",
    f"Die stabile Repair-Basis ist `{V2736F_REPAIR_BASE_SHA}`.",
    "Für die spätere REPAIR-IMPLEMENTATION sind exakt zwei Dateien erlaubt:",
    "Verbindlicher Repair-Vertrag:",
    "`tools/preflight.py` darf das bestehende enge v27.36f-Regressionsprofil für v27.36e ausschließlich um die legitimen Zustände `closure_prepared` und `closure_committed` erweitern.",
    "der legitime v27.36f-Implementierungscommit vorhanden ist",
    "die Implementierungsdateien unverändert sind",
    "der Closure-Scope exakt fünf Gate-Dateien beziehungsweise exakt einen legitimen Closure-Commit umfasst",
    "`CURRENT_TASK` auf `NONE / BLOCKED / Autorisiert NEIN` steht",
    "kein neuer Task autorisiert ist",
    "v27.36e-Provider, Adapter und Brücke unverändert sind",
    "`require_v2736e_regression`-Profil erhalten bleibt",
    "Es gibt kein pauschales PASS, und kein historischer Checker wird generell deaktiviert.",
    "`tools/check-participant-access-browser-loader-v2736f.py` darf ausschließlich um die legitimen Zustände `closure_prepared` und `closure_committed` erweitert werden.",
    "Default `data-enabled=false`",
    "ausschließlich exaktes `true`",
    "Ladefolge",
    "Readiness",
    "fail-closed",
    "`access_error`",
    "keinen lokalen Fallback bei `requested=true`",
    "lokale Standardfunktion bei `false`",
    "die v27.36d-/v27.36e-Verträge",
    "Frozen-Dateien",
    "Closure wird nur akzeptiert, wenn sie exakt dem v27.36f-Lifecycle entspricht.",
    "Eingefrorene Sicherheitsgrenze:",
    "Kein App-Code und kein Loader-Code wird geändert.",
    "`index.html`, `app.js` und `data/supabase-participant-access-browser-loader.js` bleiben unverändert.",
    "Kein Supabase-Modul wird geändert.",
    "`data/supabase-participant-access-adapter.js`",
    "`data/supabase-participant-access-bootstrap-bridge.js`",
    "`data/supabase-participant-access-browser-provider.js`",
    "`data/supabase-client-bootstrap.js`",
    "`data/supabase-client-adapter.js`",
    "Config-Dateien, SQL, Migrationen, `questions.json` und `style.css` bleiben unverändert.",
    "Supabase bleibt NICHT LIVE.",
    "Keine echten Keys.",
    "Keine echten Teilnehmerdaten.",
    "Kein echter Login wird aktiviert.",
    "Keine Live-Aktivierung",
    "kein `initializeClient()`",
    "kein `createClient()`",
    "keine Auth-Abfrage",
    "keine Tabellenabfrage",
    "keine neue Produktfunktion",
    "Der Repair betrifft ausschließlich Prüf- und Lifecycle-Kompatibilität für die Closure.",
    "Kein anderer Task und kein Folgetask ist ausgewählt oder autorisiert.",
    "Commit und Push bleiben NEIN.",
    "Permanenter v27.36f-REPAIR-Lebenszyklus",
    "repair_authorization_prepared",
    "repair_authorization_committed",
    "repair_implementation_prepared",
    "repair_implementation_committed",
    "repair_closure_prepared",
    "repair_closure_committed",
    "REPAIR-GATE enthält ausschließlich eine nichtleere Teilmenge der fünf Gate-Dateien.",
    "REPAIR-IMPLEMENTATION enthält exakt die zwei autorisierten Repair-Dateien",
    "REPAIR-CLOSURE ist erst nach REPAIR-IMPLEMENTATION zulässig",
    "Keine zukünftige Repair-GATE-, Repair-IMPLEMENTATION- oder Repair-CLOSURE-SHA wird hartcodiert.",
    "Nach `repair_closure_committed` bleibt eine Rückkehr zu `v27.36f-REPAIR / AUTHORIZED` ohne neue ausdrückliche Autorisierung blockiert.",
    "Der ursprüngliche v27.36f-Closure-Schritt bleibt danach noch separat abzuschließen.",
)
V2736F_REPAIR_CLOSURE_MARKERS = (
    "v27.36f-REPAIR abgeschlossen.",
    "Die v27.36f-Implementierung bleibt unverändert.",
    "Der ursprüngliche v27.36f-Closure-Schritt bleibt separat abzuschließen.",
    "Supabase bleibt NICHT LIVE.",
    "Keine echten Keys.",
    "Keine echten Teilnehmerdaten.",
    "Kein Folgetask wurde ausgewählt oder autorisiert.",
    "Permanenter v27.36f-REPAIR-Lebenszyklus",
    "repair_authorization_prepared",
    "repair_authorization_committed",
    "repair_implementation_prepared",
    "repair_implementation_committed",
    "repair_closure_prepared",
    "repair_closure_committed",
    "Keine zukünftige Repair-CLOSURE-SHA wird hartcodiert.",
    "Rückkehr zu `v27.36f-REPAIR / AUTHORIZED` bleibt ohne neue ausdrückliche Autorisierung blockiert.",
)
V2736F_REPAIR_TASK_AUTHORIZED = "repair_authorized"
V2736F_REPAIR_TASK_CLOSED = "repair_closed"
V2736F_REPAIR_HISTORY_BEFORE_AUTHORIZATION = "repair_before_authorization_commit"
V2736F_REPAIR_HISTORY_AUTHORIZED = "repair_authorization_committed"
V2736F_REPAIR_HISTORY_IMPLEMENTED = "repair_implementation_committed"
V2736F_REPAIR_HISTORY_CLOSED = "repair_closure_committed"
V2736F_REPAIR_HISTORY_ORIGINAL_CLOSED = "original_closure_committed"
V2736F_REPAIR_PHASE_AUTHORIZATION_PREPARED = "repair_authorization_prepared"
V2736F_REPAIR_PHASE_AUTHORIZATION_COMMITTED = "repair_authorization_committed"
V2736F_REPAIR_PHASE_IMPLEMENTATION_PREPARED = "repair_implementation_prepared"
V2736F_REPAIR_PHASE_IMPLEMENTATION_COMMITTED = "repair_implementation_committed"
V2736F_REPAIR_PHASE_CLOSURE_PREPARED = "repair_closure_prepared"
V2736F_REPAIR_PHASE_CLOSURE_COMMITTED = "repair_closure_committed"
V2736F_REPAIR_ROLE_GATE = "REPAIR_GATE"
V2736F_REPAIR_ROLE_IMPLEMENTATION = "REPAIR_IMPLEMENTATION"
V2736F_REPAIR_ROLE_CLOSURE = "REPAIR_CLOSURE"
V2736F_REPAIR_ROLE_ORIGINAL_CLOSURE = "ORIGINAL_CLOSURE"
V2736F_REPAIR_CLOSURE_KIND_REPAIR = "repair"
V2736F_REPAIR_CLOSURE_KIND_ORIGINAL = "original"


@dataclass(frozen=True)
class V2736FRepairCommitFact:
    commit_sha: str
    changed_files: frozenset[str]
    task_state: str
    closure_kind: str | None = None


@dataclass(frozen=True)
class V2736FRepairHistoryState:
    state: str
    implementation_commit: str | None
    roles: tuple[str, ...]
    gate_commits: tuple[str, ...]


@dataclass(frozen=True)
class V2736FRepairWorkingTreeFact:
    branch: str
    head: str
    origin_main: str
    diff_files: frozenset[str]
    staged_files: frozenset[str]
    untracked_files: frozenset[str]
    status_lines: frozenset[str]
    base_is_head_ancestor: bool
    base_is_origin_ancestor: bool
    origin_is_head_ancestor: bool


def extract_v2736f_repair_authorization_section(text: str, document_name: str) -> str:
    heading_prefix = "##" if document_name in {"PROJECT_STATE_CURRENT", "CURRENT_TASK"} else "###"
    return section_between(
        text,
        f"{heading_prefix} Autorisierter Repair-Task v27.36f-REPAIR",
        f"{heading_prefix} Abgeschlossener technischer Schritt v27.36e",
        document_name,
    )


def extract_v2736f_repair_closure_section(text: str, document_name: str) -> str:
    heading_prefix = "##" if document_name in {"PROJECT_STATE_CURRENT", "CURRENT_TASK"} else "###"
    return section_between(
        text,
        f"{heading_prefix} Abgeschlossener Repair-Task v27.36f-REPAIR",
        f"{heading_prefix} Abgeschlossener technischer Schritt v27.36e",
        document_name,
    )


def validate_no_future_v2736f_repair_sha(section: str, allowed_shas: frozenset[str], document_name: str) -> None:
    shas = frozenset(re.findall(r"\b[0-9a-f]{40}\b", section))
    require(
        shas.issubset(allowed_shas),
        f"{document_name}: zukünftige v27.36f-REPAIR-Commit-SHA hartcodiert: {sorted(shas - allowed_shas)}",
    )
    require(
        re.search(r"\bv27\.(?:36[g-z]|3[7-9])\b", section, re.IGNORECASE) is None,
        f"{document_name}: automatischer Folgetask nach v27.36f-REPAIR unzulässig",
    )


def validate_v2736f_repair_file_list(section: str, document_name: str) -> None:
    start_marker = "Für die spätere REPAIR-IMPLEMENTATION sind exakt zwei Dateien erlaubt:"
    end_marker = "Verbindlicher Repair-Vertrag:"
    require(section.count(start_marker) == 1, f"{document_name}: Repair-Dateilistenanfang fehlt oder ist doppelt")
    require(section.count(end_marker) == 1, f"{document_name}: Repair-Dateilistenende fehlt oder ist doppelt")
    list_text = section.split(start_marker, 1)[1].split(end_marker, 1)[0].strip()
    expected_text = "\n".join(f"- `{path}`" for path in V2736F_REPAIR_IMPLEMENTATION_FILE_ORDER)
    require(list_text == expected_text, f"{document_name}: Repair-Dateiliste muss exakt zwei eindeutige kanonische Listenzeilen enthalten")
    listed_paths = tuple(re.findall(r"(?m)^- `([^`\r\n]+)`$", list_text))
    require(listed_paths == V2736F_REPAIR_IMPLEMENTATION_FILE_ORDER, f"{document_name}: Repair-Dateiliste ist unvollständig, erweitert, doppelt oder falsch geordnet")


def replace_v2736f_repair_file_list(section: str, replacement_lines: tuple[str, ...]) -> str:
    start_marker = "Für die spätere REPAIR-IMPLEMENTATION sind exakt zwei Dateien erlaubt:"
    end_marker = "Verbindlicher Repair-Vertrag:"
    require(section.count(start_marker) == 1 and section.count(end_marker) == 1, "Repair-Manipulation benötigt eine eindeutig abgegrenzte Dateiliste")
    list_start = section.index(start_marker) + len(start_marker)
    list_end = section.index(end_marker, list_start)
    current_lines = tuple(line.strip() for line in section[list_start:list_end].splitlines() if line.strip())
    expected_lines = tuple(f"- `{path}`" for path in V2736F_REPAIR_IMPLEMENTATION_FILE_ORDER)
    require(current_lines == expected_lines, "Repair-Manipulation benötigt die unveränderte kanonische Dateiliste")
    replacement_block = "\n\n" + "\n".join(replacement_lines) + "\n\n"
    return section[:list_start] + replacement_block + section[list_end:]


def replace_v2736f_repair_document_section(document: str, section: str, replacement: str) -> str:
    require(document.count(section) == 1, "Repair-Manipulation benötigt einen eindeutig abgegrenzten Vertragsabschnitt")
    section_start = document.index(section)
    return document[:section_start] + replacement + document[section_start + len(section):]


def validate_v2736f_repair_authorization_section(section: str, document_name: str) -> None:
    validate_required_markers(section, V2736F_REPAIR_AUTHORIZATION_MARKERS, f"{document_name} / v27.36f-REPAIR")
    validate_no_future_v2736f_repair_sha(section, frozenset({V2736F_REPAIR_BASE_SHA}), f"{document_name} / v27.36f-REPAIR")
    validate_v2736f_repair_file_list(section, document_name)


def validate_v2736f_repair_state_text(text: str) -> None:
    validate_exact_fields(text, V2736F_REPAIR_EXPECTED_STATE_FIELDS)
    validate_v2736f_repair_authorization_section(
        extract_v2736f_repair_authorization_section(text, "PROJECT_STATE_CURRENT"),
        "PROJECT_STATE_CURRENT",
    )


def validate_v2736f_repair_task_text(text: str) -> None:
    validate_exact_fields(text, V2736F_REPAIR_EXPECTED_TASK_FIELDS)
    require(
        text.count(f"Erlaubte Implementierungsdateien: {V2736F_REPAIR_ALLOWED_FILES_VALUE}") == 1,
        "CURRENT_TASK muss exakt eine verbindliche v27.36f-REPAIR-Dateifreigabe enthalten",
    )
    validate_v2736f_repair_authorization_section(
        extract_v2736f_repair_authorization_section(text, "CURRENT_TASK"),
        "CURRENT_TASK",
    )


def validate_v2736f_repair_cursor_text(text: str) -> None:
    require(exact_field(text, "Stand") == "v27.36f-REPAIR", "CURSOR-Kontext muss auf v27.36f-REPAIR stehen")
    validate_project_paths(text, "CURSOR_MASTER_CONTEXT_ACCAOUI")
    validate_v2736f_repair_authorization_section(
        extract_v2736f_repair_authorization_section(text, "CURSOR_MASTER_CONTEXT_ACCAOUI"),
        "CURSOR_MASTER_CONTEXT_ACCAOUI",
    )


def validate_v2736f_repair_masterlist_text(text: str) -> None:
    require(exact_field(text, "Stand") == "v27.36f-REPAIR", "PROJECT_MASTERLIST muss auf v27.36f-REPAIR stehen")
    validate_v2736d_permanent_masterlist_contract(text)
    original_rows = re.findall(r"(?m)^\| v27\.36f \|.*$", text)
    require(
        len(original_rows) == 1
        and V2736F_REPAIR_BASE_SHA in original_rows[0]
        and "**Implementierung abgeschlossen; Closure ausstehend**" in original_rows[0],
        "PROJECT_MASTERLIST muss v27.36f exakt einmal als implementiert mit ausstehender Closure führen",
    )
    repair_rows = re.findall(r"(?m)^\| v27\.36f-REPAIR \|.*$", text)
    require(
        len(repair_rows) == 1 and "**autorisiert**" in repair_rows[0],
        "PROJECT_MASTERLIST muss v27.36f-REPAIR exakt einmal als autorisiert führen",
    )
    validate_v2736f_repair_authorization_section(
        extract_v2736f_repair_authorization_section(text, "PROJECT_MASTERLIST"),
        "PROJECT_MASTERLIST",
    )


def detect_v2736f_repair_task_state_text(text: str) -> str:
    task_id = exact_field(text, "Task-ID")
    if task_id == "v27.36f-REPAIR":
        validate_exact_fields(text, V2736F_REPAIR_EXPECTED_TASK_FIELDS)
        return V2736F_REPAIR_TASK_AUTHORIZED
    if task_id == "NONE":
        last_control_step = exact_field(text, "Letzter abgeschlossener Kontrollschritt")
        if last_control_step == "v27.36f-REPAIR":
            validate_exact_fields(text, V2736F_REPAIR_CLOSED_TASK_FIELDS)
        elif last_control_step == "v27.36f":
            validate_exact_fields(text, V2736F_CLOSED_TASK_FIELDS)
        else:
            raise ValidationError(
                "Geschlossener v27.36f-REPAIR-Zustand benötigt v27.36f-REPAIR "
                "oder v27.36f als letzten abgeschlossenen Kontrollschritt"
            )
        return V2736F_REPAIR_TASK_CLOSED
    raise ValidationError(f"Unzulässiger v27.36f-REPAIR-Taskzustand: {task_id}")


def detect_v2736f_repair_closure_kind_text(text: str) -> str:
    repair_heading = "## Abgeschlossener Repair-Task v27.36f-REPAIR"
    original_heading = "## Abgeschlossener technischer Schritt v27.36f"
    repair_present = repair_heading in text
    original_present = original_heading in text
    require(
        repair_present != original_present,
        "Geschlossener v27.36f-Zustand muss exakt einen Repair- oder ursprünglichen Closure-Abschnitt enthalten",
    )
    return (
        V2736F_REPAIR_CLOSURE_KIND_REPAIR
        if repair_present
        else V2736F_REPAIR_CLOSURE_KIND_ORIGINAL
    )


def validate_v2736f_repair_closed_documents(
    state_text: str,
    task_text: str,
    cursor_text: str,
    masterlist_text: str,
    implementation_commit: str,
) -> None:
    require(re.fullmatch(r"[0-9a-f]{40}", implementation_commit) is not None, "Repair-Closure benötigt einen dynamisch erkannten Implementierungscommit")
    validate_exact_fields(state_text, V2736F_REPAIR_CLOSED_STATE_FIELDS)
    validate_exact_fields(task_text, V2736F_REPAIR_CLOSED_TASK_FIELDS)
    require(exact_field(cursor_text, "Stand") == "v27.36f-REPAIR", "CURSOR-Kontext muss nach Repair-Closure auf v27.36f-REPAIR stehen")
    require(exact_field(masterlist_text, "Stand") == "v27.36f-REPAIR", "PROJECT_MASTERLIST muss nach Repair-Closure auf v27.36f-REPAIR stehen")
    validate_project_paths(cursor_text, "CURSOR_MASTER_CONTEXT_ACCAOUI")
    validate_v2736d_permanent_masterlist_contract(masterlist_text)
    documents = (state_text, task_text, cursor_text, masterlist_text)
    names = ("PROJECT_STATE_CURRENT", "CURRENT_TASK", "CURSOR_MASTER_CONTEXT_ACCAOUI", "PROJECT_MASTERLIST")
    for text, name in zip(documents, names):
        section = extract_v2736f_repair_closure_section(text, name)
        validate_required_markers(section, V2736F_REPAIR_CLOSURE_MARKERS, f"{name} / v27.36f-REPAIR-Closure")
        require(section.count(f"Repair-Implementierungscommit: `{implementation_commit}`") == 1, f"{name}: dynamischer Repair-Implementierungscommit fehlt oder ist doppelt")
        validate_no_future_v2736f_repair_sha(section, frozenset({V2736F_REPAIR_BASE_SHA, implementation_commit}), f"{name} / v27.36f-REPAIR-Closure")
    original_rows = re.findall(r"(?m)^\| v27\.36f \|.*$", masterlist_text)
    require(len(original_rows) == 1 and "**Implementierung abgeschlossen; Closure ausstehend**" in original_rows[0], "PROJECT_MASTERLIST muss die ursprüngliche v27.36f-Closure weiter als ausstehend führen")
    repair_rows = re.findall(r"(?m)^\| v27\.36f-REPAIR \|.*$", masterlist_text)
    require(len(repair_rows) == 1 and "**erledigt**" in repair_rows[0] and implementation_commit in repair_rows[0], "PROJECT_MASTERLIST muss v27.36f-REPAIR nach Closure exakt einmal als erledigt führen")


def validate_v2736f_implemented_repair_base(
    v2736e_base_documents: tuple[str, str, str, str],
) -> tuple[V2736FHistoryState, tuple[str, str, str, str], V2736FWorkingTreeFact]:
    require(
        git_is_ancestor(V2736F_AUTHORIZATION_BASE_SHA, V2736F_REPAIR_BASE_SHA),
        "v27.36f-Autorisierungsbasis ist kein Vorfahr der stabilen Repair-Basis",
    )
    facts = read_v2736f_commit_facts(V2736F_REPAIR_BASE_SHA)
    history = validate_v2736f_history_facts(facts)
    require(history.state == V2736F_HISTORY_IMPLEMENTED, "v27.36f muss an der Repair-Basis implementation_committed sein")
    require(history.implementation_commit == V2736F_REPAIR_BASE_SHA, "Die stabile Repair-Basis muss der dynamisch erkannte v27.36f-Implementierungscommit sein")
    require(history.roles.count(V2736F_ROLE_IMPLEMENTATION) == 1, "v27.36f benötigt an der Repair-Basis exakt eine IMPLEMENTATION")
    require(V2736F_ROLE_CLOSURE not in history.roles, "Die ursprüngliche v27.36f-Closure darf an der Repair-Basis noch nicht vorliegen")
    require(facts and facts[-1].changed_files == V2736F_IMPLEMENTATION_FILES, "Die Repair-Basis muss exakt die sechs v27.36f-Implementierungsdateien enthalten")
    documents = (
        read_v2735f_commit_document(V2736F_REPAIR_BASE_SHA, "docs/PROJECT_STATE_CURRENT.md"),
        read_v2735f_commit_document(V2736F_REPAIR_BASE_SHA, V2735F_TASK_RELATIVE_PATH),
        read_v2735f_commit_document(V2736F_REPAIR_BASE_SHA, "docs/CURSOR_MASTER_CONTEXT_ACCAOUI.md"),
        read_v2735f_commit_document(V2736F_REPAIR_BASE_SHA, "docs/PROJECT_MASTERLIST.md"),
    )
    validate_v2736e_historical_sections_unchanged(documents, v2736e_base_documents)
    validate_v2736f_state_text(documents[0])
    validate_v2736f_task_text(documents[1])
    validate_v2736f_cursor_text(documents[2])
    validate_v2736f_masterlist_text(documents[3])
    validate_v2736f_source_contract_at_revision(V2736F_REPAIR_BASE_SHA)
    working_fact = V2736FWorkingTreeFact(
        branch="main",
        head=V2736F_REPAIR_BASE_SHA,
        origin_main=V2736F_REPAIR_BASE_SHA,
        diff_files=frozenset(),
        staged_files=frozenset(),
        untracked_files=frozenset(),
        status_lines=frozenset(),
        new_files_existing=V2736F_NEW_IMPLEMENTATION_FILES,
        new_files_tracked_at_base=frozenset(),
        new_files_tracked_at_head=V2736F_NEW_IMPLEMENTATION_FILES,
        base_is_head_ancestor=True,
        base_is_origin_ancestor=True,
        origin_is_head_ancestor=True,
    )
    return history, documents, working_fact


def read_v2736f_repair_commit_facts(current_head: str) -> tuple[V2736FRepairCommitFact, ...]:
    shas = tuple(
        line.strip()
        for line in run_git(["rev-list", "--reverse", f"{V2736F_REPAIR_BASE_SHA}..{current_head}"]).splitlines()
        if line.strip()
    )
    previous = V2736F_REPAIR_BASE_SHA
    facts: list[V2736FRepairCommitFact] = []
    for sha in shas:
        lineage = run_git(["rev-list", "--parents", "-n", "1", sha]).split()
        require(len(lineage) == 2 and lineage[1] == previous, "v27.36f-REPAIR erlaubt nur eine lineare Historie ohne Merge-Commit")
        files = frozenset(
            line.strip().replace("\\", "/")
            for line in run_git(["diff", "--name-only", previous, sha]).splitlines()
            if line.strip()
        )
        require(files, f"Leerer v27.36f-REPAIR-Commit unzulässig: {sha}")
        task_text = read_v2735f_commit_document(sha, V2735F_TASK_RELATIVE_PATH)
        task_state = detect_v2736f_repair_task_state_text(task_text)
        closure_kind = (
            detect_v2736f_repair_closure_kind_text(task_text)
            if task_state == V2736F_REPAIR_TASK_CLOSED
            else None
        )
        facts.append(V2736FRepairCommitFact(sha, files, task_state, closure_kind))
        previous = sha
    return tuple(facts)


def validate_v2736f_repair_history_facts(
    facts: tuple[V2736FRepairCommitFact, ...],
) -> V2736FRepairHistoryState:
    gate_files = frozenset(EXPECTED_CONTROL_FILES)
    roles: list[str] = []
    gate_commits: list[str] = []
    implementation_commit: str | None = None
    repair_closed = False
    original_closed = False
    for fact in facts:
        files = fact.changed_files
        if files == V2736F_REPAIR_IMPLEMENTATION_FILES:
            require(gate_commits, "REPAIR-IMPLEMENTATION vor REPAIR-Autorisierungs-GATE unzulässig")
            require(implementation_commit is None, "Mehr als ein REPAIR-IMPLEMENTATION-Commit unzulässig")
            require(not repair_closed and not original_closed, "REPAIR-IMPLEMENTATION nach REPAIR-CLOSURE unzulässig")
            require(fact.task_state == V2736F_REPAIR_TASK_AUTHORIZED, "REPAIR-IMPLEMENTATION benötigt v27.36f-REPAIR / AUTHORIZED")
            implementation_commit = fact.commit_sha
            roles.append(V2736F_REPAIR_ROLE_IMPLEMENTATION)
            continue
        require(files and files.issubset(gate_files), f"Fremde Datei in v27.36f-REPAIR-Commit {fact.commit_sha}: {sorted(files - gate_files)}")
        if fact.task_state == V2736F_REPAIR_TASK_AUTHORIZED:
            require(not repair_closed and not original_closed, "Rückkehr zu v27.36f-REPAIR / AUTHORIZED nach REPAIR-CLOSURE unzulässig")
            gate_commits.append(fact.commit_sha)
            roles.append(V2736F_REPAIR_ROLE_GATE)
            continue
        require(implementation_commit is not None, "REPAIR-CLOSURE vor REPAIR-IMPLEMENTATION unzulässig")
        require(files == gate_files, "REPAIR-CLOSURE muss exakt die fünf Gate-Dateien ändern")
        if fact.closure_kind == V2736F_REPAIR_CLOSURE_KIND_REPAIR:
            require(not repair_closed and not original_closed, "Mehr als ein REPAIR-CLOSURE-Commit unzulässig")
            repair_closed = True
            roles.append(V2736F_REPAIR_ROLE_CLOSURE)
            continue
        require(
            fact.closure_kind == V2736F_REPAIR_CLOSURE_KIND_ORIGINAL,
            "Geschlossener Gate-Commit benötigt einen eindeutig erkannten Closure-Vertrag",
        )
        require(repair_closed, "Ursprüngliche v27.36f-CLOSURE vor REPAIR-CLOSURE unzulässig")
        require(not original_closed, "Mehr als ein ursprünglicher v27.36f-CLOSURE-Commit unzulässig")
        original_closed = True
        roles.append(V2736F_REPAIR_ROLE_ORIGINAL_CLOSURE)
    state = (
        V2736F_REPAIR_HISTORY_ORIGINAL_CLOSED
        if original_closed
        else V2736F_REPAIR_HISTORY_CLOSED
        if repair_closed
        else V2736F_REPAIR_HISTORY_IMPLEMENTED
        if implementation_commit
        else V2736F_REPAIR_HISTORY_AUTHORIZED
        if gate_commits
        else V2736F_REPAIR_HISTORY_BEFORE_AUTHORIZATION
    )
    return V2736FRepairHistoryState(state, implementation_commit, tuple(roles), tuple(gate_commits))


def recognized_v2736f_repair_completion_commits(
    facts: tuple[V2736FRepairCommitFact, ...],
    history: V2736FRepairHistoryState,
) -> tuple[str, str]:
    require(
        history.implementation_commit is not None,
        "Ursprüngliche v27.36f-Closure benötigt den dynamisch erkannten Repair-Implementierungscommit",
    )
    repair_closure_commits = tuple(
        fact.commit_sha
        for fact, role in zip(facts, history.roles)
        if role == V2736F_REPAIR_ROLE_CLOSURE
    )
    require(
        len(repair_closure_commits) == 1,
        "Ursprüngliche v27.36f-Closure benötigt exakt einen dynamisch erkannten Repair-Closure-Commit",
    )
    return history.implementation_commit, repair_closure_commits[0]


def validate_v2736f_original_after_repair_documents(
    state_text: str,
    task_text: str,
    cursor_text: str,
    masterlist_text: str,
    facts: tuple[V2736FRepairCommitFact, ...],
    history: V2736FRepairHistoryState,
) -> None:
    repair_implementation_commit, repair_closure_commit = (
        recognized_v2736f_repair_completion_commits(facts, history)
    )
    validate_v2736f_closed_documents(
        state_text,
        task_text,
        cursor_text,
        masterlist_text,
        V2736F_REPAIR_BASE_SHA,
        frozenset({repair_implementation_commit, repair_closure_commit}),
    )
    documents = (state_text, task_text, cursor_text, masterlist_text)
    names = (
        "PROJECT_STATE_CURRENT",
        "CURRENT_TASK",
        "CURSOR_MASTER_CONTEXT_ACCAOUI",
        "PROJECT_MASTERLIST",
    )
    dynamic_markers = (
        f"Repair-Implementierungscommit: `{repair_implementation_commit}`",
        f"Repair-Closure: `{repair_closure_commit}`",
    )
    for text, name in zip(documents, names):
        section = extract_v2736f_closure_section(text, name)
        validate_required_markers(
            section,
            V2736F_POST_REPAIR_CLOSURE_MARKERS + dynamic_markers,
            f"{name} / v27.36f-Closure nach Repair",
        )
        require(
            section.count(dynamic_markers[0]) == 1
            and section.count(dynamic_markers[1]) == 1,
            f"{name}: Repair-Implementierungscommit oder Repair-Closure fehlt oder ist doppelt",
        )
    repair_rows = re.findall(r"(?m)^\| v27\.36f-REPAIR \|.*$", masterlist_text)
    require(
        len(repair_rows) == 1
        and "**erledigt**" in repair_rows[0]
        and repair_implementation_commit in repair_rows[0]
        and repair_closure_commit in repair_rows[0],
        "PROJECT_MASTERLIST muss den vollständig abgeschlossenen Repair-Verlauf erhalten",
    )


def read_v2736f_repair_working_tree_fact() -> V2736FRepairWorkingTreeFact:
    head = run_git(["rev-parse", "HEAD"]).strip()
    origin_main = run_git(["rev-parse", "origin/main"]).strip()
    return V2736FRepairWorkingTreeFact(
        branch=run_git(["branch", "--show-current"]).strip(),
        head=head,
        origin_main=origin_main,
        diff_files=frozenset(line.strip().replace("\\", "/") for line in run_git(["diff", "--name-only"]).splitlines() if line.strip()),
        staged_files=frozenset(line.strip().replace("\\", "/") for line in run_git(["diff", "--cached", "--name-only"]).splitlines() if line.strip()),
        untracked_files=frozenset(line.strip().replace("\\", "/") for line in run_git(["ls-files", "--others", "--exclude-standard"]).splitlines() if line.strip()),
        status_lines=frozenset(line.replace("\\", "/") for line in run_git(["status", "--porcelain=v1", "--untracked-files=all"]).splitlines() if line),
        base_is_head_ancestor=git_is_ancestor(V2736F_REPAIR_BASE_SHA, head),
        base_is_origin_ancestor=git_is_ancestor(V2736F_REPAIR_BASE_SHA, origin_main),
        origin_is_head_ancestor=git_is_ancestor(origin_main, head),
    )


def validate_v2736f_repair_working_tree_fact(fact: V2736FRepairWorkingTreeFact) -> None:
    require(fact.branch == "main", "v27.36f-REPAIR-Lebenszyklus muss auf main laufen")
    require(fact.base_is_head_ancestor, "Die stabile v27.36f-REPAIR-Basis ist kein Vorfahr von HEAD")
    require(fact.base_is_origin_ancestor, "Die stabile v27.36f-REPAIR-Basis ist kein Vorfahr von origin/main")
    require(fact.origin_is_head_ancestor, "origin/main ist kein Vorfahr des lokalen v27.36f-REPAIR-HEAD")
    require(not fact.staged_files, "v27.36f-REPAIR-Lebenszyklus darf nichts stagen")


def validate_v2736f_repair_lifecycle_working_tree(
    history: V2736FRepairHistoryState,
    task_state: str,
    fact: V2736FRepairWorkingTreeFact,
    closure_kind: str | None = None,
) -> str:
    validate_v2736f_repair_working_tree_fact(fact)
    gate_files = frozenset(EXPECTED_CONTROL_FILES)
    clean = not fact.diff_files and not fact.untracked_files and not fact.status_lines
    if history.state == V2736F_REPAIR_HISTORY_BEFORE_AUTHORIZATION:
        require(fact.head == V2736F_REPAIR_BASE_SHA, "Repair-Autorisierungsvorbereitung benötigt die stabile Repair-Basis als HEAD")
        require(task_state == V2736F_REPAIR_TASK_AUTHORIZED, "Repair-Autorisierungsvorbereitung benötigt v27.36f-REPAIR / AUTHORIZED")
        require(fact.diff_files and fact.diff_files.issubset(gate_files), "Repair-Autorisierungsvorbereitung darf nur eine nichtleere Teilmenge der fünf Gate-Dateien ändern")
        require(not fact.untracked_files and fact.status_lines == frozenset(f" M {path}" for path in fact.diff_files), "Working Tree entspricht nicht repair_authorization_prepared")
        return V2736F_REPAIR_PHASE_AUTHORIZATION_PREPARED
    if history.state == V2736F_REPAIR_HISTORY_AUTHORIZED:
        require(fact.head != V2736F_REPAIR_BASE_SHA, "Repair-Autorisierungscommit fehlt")
        require(task_state == V2736F_REPAIR_TASK_AUTHORIZED, "Autorisierte Repair-Phasen benötigen v27.36f-REPAIR / AUTHORIZED")
        if clean:
            return V2736F_REPAIR_PHASE_AUTHORIZATION_COMMITTED
        if fact.diff_files and fact.diff_files.issubset(gate_files) and not fact.untracked_files:
            require(fact.status_lines == frozenset(f" M {path}" for path in fact.diff_files), "Lokale Repair-Gate-Korrektur enthält fremden Status")
            return V2736F_REPAIR_PHASE_AUTHORIZATION_COMMITTED
        require(fact.diff_files == V2736F_REPAIR_IMPLEMENTATION_FILES and not fact.untracked_files, "repair_implementation_prepared muss exakt die zwei Repair-Implementierungsdateien ändern")
        require(fact.status_lines == frozenset(f" M {path}" for path in V2736F_REPAIR_IMPLEMENTATION_FILES), "Working Tree entspricht nicht repair_implementation_prepared")
        return V2736F_REPAIR_PHASE_IMPLEMENTATION_PREPARED
    require(history.implementation_commit is not None, "Phase nach REPAIR-IMPLEMENTATION benötigt den dynamischen Repair-Implementierungscommit")
    if history.state == V2736F_REPAIR_HISTORY_IMPLEMENTED:
        if task_state == V2736F_REPAIR_TASK_AUTHORIZED:
            if clean:
                return V2736F_REPAIR_PHASE_IMPLEMENTATION_COMMITTED
            require(fact.diff_files and fact.diff_files.issubset(gate_files) and not fact.untracked_files, "Nach REPAIR-IMPLEMENTATION sind lokal nur Gate-Korrekturen zulässig")
            require(fact.status_lines == frozenset(f" M {path}" for path in fact.diff_files), "Lokale Repair-Gate-Korrektur nach IMPLEMENTATION enthält fremden Status")
            return V2736F_REPAIR_PHASE_IMPLEMENTATION_COMMITTED
        require(task_state == V2736F_REPAIR_TASK_CLOSED, "repair_closure_prepared benötigt den geschlossenen Repair-Taskzustand")
        require(closure_kind == V2736F_REPAIR_CLOSURE_KIND_REPAIR, "repair_closure_prepared benötigt den Repair-Closure-Vertrag")
        require(fact.diff_files == gate_files and not fact.untracked_files, "repair_closure_prepared muss exakt fünf Gate-Dateien ändern")
        require(fact.status_lines == frozenset(f" M {path}" for path in gate_files), "Working Tree entspricht nicht repair_closure_prepared")
        return V2736F_REPAIR_PHASE_CLOSURE_PREPARED
    if history.state == V2736F_REPAIR_HISTORY_CLOSED:
        require(task_state == V2736F_REPAIR_TASK_CLOSED, "Nach REPAIR-CLOSURE darf keine Rückkehr zu v27.36f-REPAIR / AUTHORIZED erfolgen")
        if clean:
            require(closure_kind == V2736F_REPAIR_CLOSURE_KIND_REPAIR, "repair_closure_committed benötigt den Repair-Closure-Vertrag")
            return V2736F_REPAIR_PHASE_CLOSURE_COMMITTED
        require(closure_kind == V2736F_REPAIR_CLOSURE_KIND_ORIGINAL, "Nach REPAIR-CLOSURE sind nur die ursprünglichen v27.36f-Closure-Dokumente zulässig")
        require(fact.diff_files == gate_files and not fact.untracked_files, "closure_prepared muss nach Repair-Closure exakt fünf Gate-Dateien ändern")
        require(fact.status_lines == frozenset(f" M {path}" for path in gate_files), "Working Tree entspricht nach Repair-Closure nicht closure_prepared")
        return V2736F_PHASE_CLOSURE_PREPARED
    require(history.state == V2736F_REPAIR_HISTORY_ORIGINAL_CLOSED, "Unbekannter v27.36f-REPAIR-Historienzustand")
    require(task_state == V2736F_REPAIR_TASK_CLOSED, "Nach ursprünglicher v27.36f-CLOSURE darf keine Rückkehr zu AUTHORIZED erfolgen")
    require(closure_kind == V2736F_REPAIR_CLOSURE_KIND_ORIGINAL, "closure_committed benötigt den ursprünglichen v27.36f-Closure-Vertrag")
    require(clean, "closure_committed benötigt einen sauberen Working Tree")
    return V2736F_PHASE_CLOSURE_COMMITTED


def validate_v2736f_repair_committed_closure_documents(
    facts: tuple[V2736FRepairCommitFact, ...],
    history: V2736FRepairHistoryState,
) -> None:
    if not ({V2736F_REPAIR_ROLE_CLOSURE, V2736F_REPAIR_ROLE_ORIGINAL_CLOSURE} & set(history.roles)):
        return
    require(history.implementation_commit is not None, "REPAIR-CLOSURE benötigt einen dynamischen Repair-Implementierungscommit")
    for fact, role in zip(facts, history.roles):
        if role == V2736F_REPAIR_ROLE_CLOSURE:
            validate_v2736f_repair_closed_documents(
                read_v2735f_commit_document(fact.commit_sha, "docs/PROJECT_STATE_CURRENT.md"),
                read_v2735f_commit_document(fact.commit_sha, V2735F_TASK_RELATIVE_PATH),
                read_v2735f_commit_document(fact.commit_sha, "docs/CURSOR_MASTER_CONTEXT_ACCAOUI.md"),
                read_v2735f_commit_document(fact.commit_sha, "docs/PROJECT_MASTERLIST.md"),
                history.implementation_commit,
            )
        elif role == V2736F_REPAIR_ROLE_ORIGINAL_CLOSURE:
            validate_v2736f_original_after_repair_documents(
                read_v2735f_commit_document(fact.commit_sha, "docs/PROJECT_STATE_CURRENT.md"),
                read_v2735f_commit_document(fact.commit_sha, V2735F_TASK_RELATIVE_PATH),
                read_v2735f_commit_document(fact.commit_sha, "docs/CURSOR_MASTER_CONTEXT_ACCAOUI.md"),
                read_v2735f_commit_document(fact.commit_sha, "docs/PROJECT_MASTERLIST.md"),
                facts,
                history,
            )


def validate_v2736f_repair_lifecycle(
    state_text: str,
    task_text: str,
    cursor_text: str,
    masterlist_text: str,
    v2736f_base_documents: tuple[str, str, str, str],
) -> tuple[str, V2736FRepairHistoryState, V2736FRepairWorkingTreeFact]:
    current_documents = (state_text, task_text, cursor_text, masterlist_text)
    validate_v2736e_historical_sections_unchanged(current_documents, v2736f_base_documents)
    fact = read_v2736f_repair_working_tree_fact()
    facts = read_v2736f_repair_commit_facts(fact.head)
    history = validate_v2736f_repair_history_facts(facts)
    validate_v2736f_repair_committed_closure_documents(facts, history)
    task_state = detect_v2736f_repair_task_state_text(task_text)
    closure_kind = (
        detect_v2736f_repair_closure_kind_text(task_text)
        if task_state == V2736F_REPAIR_TASK_CLOSED
        else None
    )
    if task_state == V2736F_REPAIR_TASK_AUTHORIZED:
        validate_v2736f_repair_state_text(state_text)
        validate_v2736f_repair_task_text(task_text)
        validate_v2736f_repair_cursor_text(cursor_text)
        validate_v2736f_repair_masterlist_text(masterlist_text)
    else:
        require(history.implementation_commit is not None, "v27.36f-REPAIR-Abschluss vor REPAIR-IMPLEMENTATION unzulässig")
        if closure_kind == V2736F_REPAIR_CLOSURE_KIND_REPAIR:
            require(history.state in {V2736F_REPAIR_HISTORY_IMPLEMENTED, V2736F_REPAIR_HISTORY_CLOSED}, "Repair-Closure-Dokumente sind in dieser Historienphase unzulässig")
            validate_v2736f_repair_closed_documents(state_text, task_text, cursor_text, masterlist_text, history.implementation_commit)
        else:
            require(history.state in {V2736F_REPAIR_HISTORY_CLOSED, V2736F_REPAIR_HISTORY_ORIGINAL_CLOSED}, "Ursprüngliche v27.36f-Closure vor REPAIR-CLOSURE unzulässig")
            validate_v2736f_original_after_repair_documents(
                state_text,
                task_text,
                cursor_text,
                masterlist_text,
                facts,
                history,
            )
    phase = validate_v2736f_repair_lifecycle_working_tree(history, task_state, fact, closure_kind)
    return phase, history, fact


def run_v2736f_repair_manipulation_matrix(
    state_text: str,
    task_text: str,
    cursor_text: str,
    masterlist_text: str,
    current_history: V2736FRepairHistoryState,
    current_fact: V2736FRepairWorkingTreeFact,
) -> tuple[int, int, int]:
    checks = 0

    def rejected(validator: Callable[[str], None], manipulated: str, label: str) -> None:
        nonlocal checks
        try:
            validator(manipulated)
        except ValidationError:
            checks += 1
            return
        raise ValidationError(f"v27.36f-REPAIR-Manipulation wurde nicht blockiert: {label}")

    current_task_state = detect_v2736f_repair_task_state_text(task_text)
    if current_task_state == V2736F_REPAIR_TASK_CLOSED:
        require(current_history.gate_commits, "Repair-Closure benötigt einen historischen Repair-Autorisierungscommit")
        authorization_revision = current_history.gate_commits[-1]
        authorization_documents = (
            read_v2735f_commit_document(authorization_revision, "docs/PROJECT_STATE_CURRENT.md"),
            read_v2735f_commit_document(authorization_revision, V2735F_TASK_RELATIVE_PATH),
            read_v2735f_commit_document(authorization_revision, "docs/CURSOR_MASTER_CONTEXT_ACCAOUI.md"),
            read_v2735f_commit_document(authorization_revision, "docs/PROJECT_MASTERLIST.md"),
        )
    else:
        authorization_documents = (state_text, task_text, cursor_text, masterlist_text)
    authorization_state, authorization_task, authorization_cursor, authorization_masterlist = authorization_documents
    for text, validator, fields, name in (
        (authorization_state, validate_v2736f_repair_state_text, V2736F_REPAIR_EXPECTED_STATE_FIELDS, "PROJECT_STATE_CURRENT"),
        (authorization_task, validate_v2736f_repair_task_text, V2736F_REPAIR_EXPECTED_TASK_FIELDS, "CURRENT_TASK"),
    ):
        for field, value in fields.items():
            rejected(validator, text.replace(f"{field}: {value}", f"{field}: MANIPULIERT", 1), f"{name}: Feld {field}")
    boundaries = (
        (authorization_state, validate_v2736f_repair_state_text, "PROJECT_STATE_CURRENT"),
        (authorization_task, validate_v2736f_repair_task_text, "CURRENT_TASK"),
        (authorization_cursor, validate_v2736f_repair_cursor_text, "CURSOR_MASTER_CONTEXT_ACCAOUI"),
        (authorization_masterlist, validate_v2736f_repair_masterlist_text, "PROJECT_MASTERLIST"),
    )
    canonical_list_lines = tuple(f"- `{path}`" for path in V2736F_REPAIR_IMPLEMENTATION_FILE_ORDER)
    for text, validator, name in boundaries:
        section = extract_v2736f_repair_authorization_section(text, name)
        for marker in V2736F_REPAIR_AUTHORIZATION_MARKERS:
            require(marker in section, f"Repair-Manipulationsmatrix kann Pflichtaussage nicht finden: {name} / {marker}")
            changed_section = section.replace(marker, "")
            rejected(
                validator,
                replace_v2736f_repair_document_section(text, section, changed_section),
                f"{name}: Pflichtaussage {marker}",
            )
        for index, path in enumerate(V2736F_REPAIR_IMPLEMENTATION_FILE_ORDER):
            changed_lines = canonical_list_lines[:index] + canonical_list_lines[index + 1:]
            changed_section = replace_v2736f_repair_file_list(section, changed_lines)
            rejected(
                validator,
                replace_v2736f_repair_document_section(text, section, changed_section),
                f"{name}: Repair-Implementierungsdatei {path}",
            )
        duplicate_section = replace_v2736f_repair_file_list(section, canonical_list_lines[:1] + canonical_list_lines)
        rejected(
            validator,
            replace_v2736f_repair_document_section(text, section, duplicate_section),
            f"{name}: doppelte Repair-Implementierungsdatei",
        )
        extra_section = replace_v2736f_repair_file_list(section, canonical_list_lines + ("- `unexpected.txt`",))
        rejected(
            validator,
            replace_v2736f_repair_document_section(text, section, extra_section),
            f"{name}: zusätzliche Repair-Implementierungsdatei",
        )
        manipulated_section = section + "\nZukünftiger v27.36f-REPAIR-Commit: `" + ("a" * 40) + "`\n"
        rejected(
            validator,
            replace_v2736f_repair_document_section(text, section, manipulated_section),
            f"{name}: unbekannte zukünftige Repair-SHA",
        )
    repair_rows = re.findall(r"(?m)^\| v27\.36f-REPAIR \|.*$", authorization_masterlist)
    require(len(repair_rows) == 1, "Repair-Manipulationsmatrix benötigt exakt eine v27.36f-REPAIR-Masterlistenzeile")
    rejected(
        validate_v2736f_repair_masterlist_text,
        authorization_masterlist.replace(repair_rows[0], repair_rows[0].replace("**autorisiert**", "**erledigt**", 1), 1),
        "PROJECT_MASTERLIST: v27.36f-REPAIR vorzeitig erledigt",
    )

    gate = V2736FRepairCommitFact("1" * 40, frozenset({EXPECTED_CONTROL_FILES[0]}), V2736F_REPAIR_TASK_AUTHORIZED)
    implementation = V2736FRepairCommitFact("2" * 40, V2736F_REPAIR_IMPLEMENTATION_FILES, V2736F_REPAIR_TASK_AUTHORIZED)
    closure = V2736FRepairCommitFact(
        "3" * 40,
        frozenset(EXPECTED_CONTROL_FILES),
        V2736F_REPAIR_TASK_CLOSED,
        V2736F_REPAIR_CLOSURE_KIND_REPAIR,
    )
    original_closure = V2736FRepairCommitFact(
        "4" * 40,
        frozenset(EXPECTED_CONTROL_FILES),
        V2736F_REPAIR_TASK_CLOSED,
        V2736F_REPAIR_CLOSURE_KIND_ORIGINAL,
    )
    histories = (
        validate_v2736f_repair_history_facts(tuple()),
        validate_v2736f_repair_history_facts((gate,)),
        validate_v2736f_repair_history_facts((gate, implementation)),
        validate_v2736f_repair_history_facts((gate, implementation, closure)),
        validate_v2736f_repair_history_facts((gate, implementation, closure, original_closure)),
    )
    clean_fact = replace(
        current_fact,
        head="1" * 40,
        diff_files=frozenset(),
        staged_files=frozenset(),
        untracked_files=frozenset(),
        status_lines=frozenset(),
        base_is_head_ancestor=True,
        base_is_origin_ancestor=True,
        origin_is_head_ancestor=True,
    )
    gate_files = frozenset(EXPECTED_CONTROL_FILES)
    implementation_status = frozenset(f" M {path}" for path in V2736F_REPAIR_IMPLEMENTATION_FILES)
    phase_fixtures = (
        (histories[0], V2736F_REPAIR_TASK_AUTHORIZED, replace(clean_fact, head=V2736F_REPAIR_BASE_SHA, diff_files=gate_files, status_lines=frozenset(f" M {path}" for path in gate_files)), None, V2736F_REPAIR_PHASE_AUTHORIZATION_PREPARED),
        (histories[1], V2736F_REPAIR_TASK_AUTHORIZED, clean_fact, None, V2736F_REPAIR_PHASE_AUTHORIZATION_COMMITTED),
        (histories[1], V2736F_REPAIR_TASK_AUTHORIZED, replace(clean_fact, diff_files=V2736F_REPAIR_IMPLEMENTATION_FILES, status_lines=implementation_status), None, V2736F_REPAIR_PHASE_IMPLEMENTATION_PREPARED),
        (histories[2], V2736F_REPAIR_TASK_AUTHORIZED, clean_fact, None, V2736F_REPAIR_PHASE_IMPLEMENTATION_COMMITTED),
        (histories[2], V2736F_REPAIR_TASK_CLOSED, replace(clean_fact, diff_files=gate_files, status_lines=frozenset(f" M {path}" for path in gate_files)), V2736F_REPAIR_CLOSURE_KIND_REPAIR, V2736F_REPAIR_PHASE_CLOSURE_PREPARED),
        (histories[3], V2736F_REPAIR_TASK_CLOSED, clean_fact, V2736F_REPAIR_CLOSURE_KIND_REPAIR, V2736F_REPAIR_PHASE_CLOSURE_COMMITTED),
        (histories[3], V2736F_REPAIR_TASK_CLOSED, replace(clean_fact, diff_files=gate_files, status_lines=frozenset(f" M {path}" for path in gate_files)), V2736F_REPAIR_CLOSURE_KIND_ORIGINAL, V2736F_PHASE_CLOSURE_PREPARED),
        (histories[4], V2736F_REPAIR_TASK_CLOSED, clean_fact, V2736F_REPAIR_CLOSURE_KIND_ORIGINAL, V2736F_PHASE_CLOSURE_COMMITTED),
    )
    for history, task_state, fact, closure_kind, expected in phase_fixtures:
        require(
            validate_v2736f_repair_lifecycle_working_tree(history, task_state, fact, closure_kind) == expected,
            f"v27.36f-REPAIR-Positivsimulation fehlgeschlagen: {expected}",
        )
    bad_histories = (
        ((implementation,), "Repair-Implementation vor Autorisierung"),
        ((gate, implementation, implementation), "zweite Repair-Implementation"),
        ((gate, closure), "Repair-Closure vor Repair-Implementation"),
        ((gate, implementation, original_closure), "ursprüngliche Closure vor Repair-Closure"),
        ((gate, implementation, closure, closure), "zweite Repair-Closure"),
        ((gate, implementation, closure, original_closure, original_closure), "zweite ursprüngliche Closure"),
        ((gate, implementation, closure, gate), "Rückkehr nach Repair-Closure"),
        ((gate, implementation, V2736FRepairCommitFact("5" * 40, frozenset({EXPECTED_CONTROL_FILES[0]}), V2736F_REPAIR_TASK_CLOSED, V2736F_REPAIR_CLOSURE_KIND_REPAIR)), "partielle Repair-Closure"),
        ((gate, implementation, closure, V2736FRepairCommitFact("6" * 40, frozenset({EXPECTED_CONTROL_FILES[0]}), V2736F_REPAIR_TASK_CLOSED, V2736F_REPAIR_CLOSURE_KIND_ORIGINAL)), "partielle ursprüngliche Closure"),
        ((gate, V2736FRepairCommitFact("7" * 40, frozenset({"tools/preflight.py"}), V2736F_REPAIR_TASK_AUTHORIZED)), "partielle Repair-Implementation"),
        ((gate, V2736FRepairCommitFact("8" * 40, V2736F_REPAIR_IMPLEMENTATION_FILES | {"app.js"}, V2736F_REPAIR_TASK_AUTHORIZED)), "Repair-Implementation mit app.js"),
        ((V2736FRepairCommitFact("9" * 40, frozenset({"app.js"}), V2736F_REPAIR_TASK_AUTHORIZED),), "fremder Repair-Gate-Commit"),
    )
    for facts, label in bad_histories:
        try:
            validate_v2736f_repair_history_facts(facts)
        except ValidationError:
            checks += 1
            continue
        raise ValidationError(f"v27.36f-REPAIR-Historienmanipulation wurde nicht blockiert: {label}")
    bad_working = (
        (current_history, V2736F_REPAIR_TASK_AUTHORIZED, replace(current_fact, staged_files=frozenset({EXPECTED_CONTROL_FILES[0]})), "gestagte Datei"),
        (current_history, V2736F_REPAIR_TASK_AUTHORIZED, replace(current_fact, diff_files=current_fact.diff_files | {"app.js"}, status_lines=current_fact.status_lines | {" M app.js"}), "eingefrorene app.js"),
        (current_history, V2736F_REPAIR_TASK_AUTHORIZED, replace(current_fact, untracked_files=frozenset({"unexpected.txt"}), status_lines=current_fact.status_lines | {"?? unexpected.txt"}), "fremde ungetrackte Datei"),
        (current_history, V2736F_REPAIR_TASK_AUTHORIZED, replace(current_fact, base_is_head_ancestor=False), "falsche Repair-Basis"),
        (current_history, V2736F_REPAIR_TASK_AUTHORIZED, replace(current_fact, origin_is_head_ancestor=False), "origin nicht Vorfahr"),
        (histories[0], V2736F_REPAIR_TASK_AUTHORIZED, replace(clean_fact, head=V2736F_REPAIR_BASE_SHA, diff_files=V2736F_REPAIR_IMPLEMENTATION_FILES, status_lines=implementation_status), "Repair-Implementation lokal vor Autorisierung"),
        (histories[1], V2736F_REPAIR_TASK_CLOSED, replace(clean_fact, diff_files=gate_files, status_lines=frozenset(f" M {path}" for path in gate_files)), "Repair-Closure lokal vor Repair-Implementation"),
        (histories[3], V2736F_REPAIR_TASK_AUTHORIZED, clean_fact, "Rückkehr zu Repair-AUTHORIZED nach Closure"),
    )
    for history, task_state, fact, label in bad_working:
        try:
            validate_v2736f_repair_lifecycle_working_tree(history, task_state, fact)
        except ValidationError:
            checks += 1
            continue
        raise ValidationError(f"v27.36f-REPAIR-Working-Tree-Manipulation wurde nicht blockiert: {label}")
    negative_tests = len(bad_histories) + len(bad_working)
    return checks, len(phase_fixtures), negative_tests


V2737A_GATE_REPAIR_BASE_SHA = "ac997149fe9600d735dcc237b0a30232d279cc52"
V2737A_GATE_REPAIR_FOLLOWUP_BASE_SHA = "ec8f20216d8dcb13417cca27699febc998d6dcd9"
V2737A_GATE_REPAIR_HISTORICAL_SHAS = frozenset({
    "a68dd9e81f26c3a887e668b90e9f5e8973c7ddfa",
    "b035c62100b033dbce03a4ab016e4471b4ab54d4",
    "d2a303e3ca4cfd8b61a1e7b7f8e5c4b43682c712",
    V2737A_GATE_REPAIR_BASE_SHA,
})
V2737A_GATE_REPAIR_FILES = frozenset((*EXPECTED_CONTROL_FILES, "tools/preflight.py"))
V2737A_GATE_REPAIR_FILE_ORDER = (
    "docs/CURSOR_MASTER_CONTEXT_ACCAOUI.md",
    "docs/PROJECT_MASTERLIST.md",
    "docs/PROJECT_STATE_CURRENT.md",
    "docs/tasks/CURRENT_TASK.md",
    "tools/check-project-continuity-control.py",
    "tools/preflight.py",
)
V2737A_GATE_REPAIR_FROZEN_PRODUCT_FILES = (
    "index.html",
    "app.js",
    "data/supabase-client-bootstrap.js",
    "data/supabase-client-adapter.js",
    "data/supabase-participant-access-adapter.js",
    "data/supabase-participant-access-bootstrap-bridge.js",
    "data/supabase-participant-access-browser-provider.js",
    "data/supabase-participant-access-browser-loader.js",
    "questions.json",
    "style.css",
)
V2737A_GATE_REPAIR_PHASE_PREPARED = "v2737a_gate_repair_atomic_prepared"
V2737A_GATE_REPAIR_PHASE_COMMITTED = "v2737a_gate_repair_atomic_committed"
V2737A_GATE_REPAIR_FOLLOWUP_PHASE_PREPARED = "v2737a_gate_repair_followup_atomic_prepared"
V2737A_GATE_REPAIR_FOLLOWUP_PHASE_COMMITTED = "v2737a_gate_repair_followup_atomic_committed"
V2737A_GATE_FILES = frozenset(EXPECTED_CONTROL_FILES)
V2737A_IMPLEMENTATION_FILES = frozenset({
    "data/supabase-participant-auth-session-adapter.js",
    "tools/check-supabase-participant-auth-session-adapter.py",
    "docs/SUPABASE_PARTICIPANT_AUTH_SESSION_ADAPTER_V2737A.md",
    "tools/preflight.py",
})
V2737A_ALLOWED_STATE_CONTRACTS = frozenset({
    (
        V2737A_GATE_REPAIR_PHASE_PREPARED,
        "NONE",
        "BLOCKED",
        "NEIN",
        frozenset(),
        V2737A_GATE_REPAIR_FILES,
        (),
        "base_is_head",
        "repair_closed",
    ),
    (
        V2737A_GATE_REPAIR_PHASE_COMMITTED,
        "NONE",
        "BLOCKED",
        "NEIN",
        frozenset(),
        frozenset(),
        ("atomic_repair",),
        "repair_parent_is_base",
        "repair_closed",
    ),
    (
        V2737A_GATE_REPAIR_FOLLOWUP_PHASE_PREPARED,
        "NONE",
        "BLOCKED",
        "NEIN",
        frozenset(),
        V2737A_GATE_REPAIR_FILES,
        ("atomic_repair",),
        "head_is_atomic_repair",
        "followup_closed",
    ),
    (
        V2737A_GATE_REPAIR_FOLLOWUP_PHASE_COMMITTED,
        "NONE",
        "BLOCKED",
        "NEIN",
        frozenset(),
        frozenset(),
        ("atomic_repair", "atomic_followup"),
        "followup_parent_is_atomic_repair",
        "followup_closed",
    ),
    (
        "v2737a_authorization_prepared",
        "v27.37a",
        "AUTHORIZED",
        "JA",
        V2737A_IMPLEMENTATION_FILES,
        V2737A_GATE_FILES,
        ("atomic_repair", "atomic_followup"),
        "head_is_atomic_followup",
        "v2737a_authorized",
    ),
    (
        "v2737a_authorization_committed",
        "v27.37a",
        "AUTHORIZED",
        "JA",
        V2737A_IMPLEMENTATION_FILES,
        frozenset(),
        ("atomic_repair", "atomic_followup", "v2737a_gate"),
        "gate_parent_is_atomic_followup",
        "v2737a_authorized",
    ),
    (
        "v2737a_implementation_prepared",
        "v27.37a",
        "AUTHORIZED",
        "JA",
        V2737A_IMPLEMENTATION_FILES,
        V2737A_IMPLEMENTATION_FILES,
        ("atomic_repair", "atomic_followup", "v2737a_gate"),
        "head_is_v2737a_gate",
        "v2737a_authorized",
    ),
    (
        "v2737a_implementation_committed",
        "v27.37a",
        "AUTHORIZED",
        "JA",
        V2737A_IMPLEMENTATION_FILES,
        frozenset(),
        ("atomic_repair", "atomic_followup", "v2737a_gate", "v2737a_implementation"),
        "implementation_parent_is_gate",
        "v2737a_authorized",
    ),
    (
        "v2737a_closure_prepared",
        "NONE",
        "BLOCKED",
        "NEIN",
        frozenset(),
        V2737A_GATE_FILES,
        ("atomic_repair", "atomic_followup", "v2737a_gate", "v2737a_implementation"),
        "head_is_v2737a_implementation",
        "v2737a_closed",
    ),
    (
        "v2737a_closure_committed",
        "NONE",
        "BLOCKED",
        "NEIN",
        frozenset(),
        frozenset(),
        (
            "atomic_repair",
            "atomic_followup",
            "v2737a_gate",
            "v2737a_implementation",
            "v2737a_closure",
        ),
        "closure_parent_is_implementation",
        "v2737a_closed",
    ),
})
V2737A_GATE_REPAIR_SECTION_MARKERS = (
    "v27.37a-GATE-REPAIR abgeschlossen.",
    "Enges Preflight-Nachfolgeprofil nach abgeschlossenem v27.36f bootstrapen.",
    f"Stabile Ausgangsbasis: `{V2737A_GATE_REPAIR_BASE_SHA}`.",
    "Ein normaler separater Repair-Gate-Commit hätte deshalb wissentlich keinen verpflichtenden Preflight-PASS erreicht.",
    "Der ausdrücklich freigegebene einmalige atomare Bootstrap-Repair umfasst exakt:",
    "Unbekannte zukünftige Tasks werden nicht pauschal zugelassen.",
    "Es gibt keinen allgemeinen Bypass.",
    "Die lokale Sicherung `.git/v2737a-gate-preflight-blocked.patch` bleibt ausschließlich lokal, wird nicht verändert, nicht angewendet und nicht committet.",
    "Supabase bleibt NICHT LIVE.",
    "Keine echten Keys.",
    "Keine echten Teilnehmerdaten.",
    "Nach dem Repair ist v27.37a weder ausgewählt noch autorisiert.",
    "`CURRENT_TASK` bleibt `NONE / BLOCKED / Autorisiert NEIN`; Commit und Push bleiben `NEIN`.",
    V2737A_GATE_REPAIR_PHASE_PREPARED,
    V2737A_GATE_REPAIR_PHASE_COMMITTED,
    "Keine zukünftige Repair-, v27.37a-IMPLEMENTATION- oder v27.37a-CLOSURE-SHA wird hartcodiert.",
)
V2737A_GATE_REPAIR_FOLLOWUP_SECTION_MARKERS = (
    "v27.37a-GATE-REPAIR-FOLLOWUP abgeschlossen.",
    "Der Titel lautet: UTF-8-Historienleser und authorization_prepared-Scope im v27.37a-Nachfolgeprofil korrigieren.",
    f"Technische Basis: `{V2737A_GATE_REPAIR_FOLLOWUP_BASE_SHA}`.",
    "Der erste v27.37a-GATE-REPAIR bleibt vollständig abgeschlossen und wird nicht wiederholt.",
    "Windows-Codepage CP1252 statt strikt als UTF-8",
    "`authorization_prepared` akzeptiert ausschließlich eine nichtleere Teilmenge der fünf Gate-Dateien",
    "Die globale `run_command()`-Semantik bleibt unverändert.",
    V2737A_GATE_REPAIR_FOLLOWUP_PHASE_PREPARED,
    V2737A_GATE_REPAIR_FOLLOWUP_PHASE_COMMITTED,
    "v27.37a ist nach dem FOLLOWUP weiterhin nicht autorisiert",
    "ein frisches ausdrückliches v27.37a-Autorisierungs-Gate",
    ".git/v2737a-gate-preflight-blocked.patch",
    ".git/v2737a-gate-after-ec8f202.patch",
    "Supabase bleibt NICHT LIVE.",
    "Keine echten Keys.",
    "Keine echten Teilnehmerdaten.",
)


def extract_v2737a_gate_repair_section(text: str, document_name: str) -> str:
    heading_prefix = "##" if document_name in {"PROJECT_STATE_CURRENT", "CURRENT_TASK"} else "###"
    return section_between(
        text,
        f"{heading_prefix} Abgeschlossener atomarer Bootstrap-Repair v27.37a-GATE-REPAIR",
        f"{heading_prefix} Abgeschlossener technischer Schritt v27.36f",
        document_name,
    )


def extract_v2737a_gate_repair_followup_section(text: str, document_name: str) -> str:
    start_marker = "## Abgeschlossener atomarer Follow-up-Repair v27.37a-GATE-REPAIR-FOLLOWUP"
    require(
        text.count(start_marker) == 1,
        f"{document_name}: FOLLOWUP-Abschnitt fehlt oder ist doppelt",
    )
    tail = text.split(start_marker, 1)[1]
    next_heading = re.search(r"(?m)^#{1,6} ", tail)
    body = tail[:next_heading.start()] if next_heading else tail
    return start_marker + body


def v2737a_allowed_state_facts_are_valid(
    *,
    phase: str,
    task_id: str,
    status: str,
    authorized: str,
    allowed_implementation_files: frozenset[str],
    working_files: frozenset[str],
    history_roles: tuple[str, ...],
    parent_relation: str,
    current_task_state: str,
) -> bool:
    if phase == "v2737a_authorization_prepared":
        return (
            task_id == "v27.37a"
            and status == "AUTHORIZED"
            and authorized == "JA"
            and allowed_implementation_files == V2737A_IMPLEMENTATION_FILES
            and bool(working_files)
            and working_files <= V2737A_GATE_FILES
            and history_roles == ("atomic_repair", "atomic_followup")
            and parent_relation == "head_is_atomic_followup"
            and current_task_state == "v2737a_authorized"
        )
    state = (
        phase,
        task_id,
        status,
        authorized,
        allowed_implementation_files,
        working_files,
        history_roles,
        parent_relation,
        current_task_state,
    )
    return state in V2737A_ALLOWED_STATE_CONTRACTS


def validate_v2737a_gate_repair_section(section: str, document_name: str) -> None:
    validate_required_markers(
        section,
        V2737A_GATE_REPAIR_SECTION_MARKERS,
        f"{document_name} / v27.37a-GATE-REPAIR",
    )
    start_marker = "Der ausdrücklich freigegebene einmalige atomare Bootstrap-Repair umfasst exakt:"
    end_marker = "Das neue enge Preflight-Nachfolgeprofil"
    require(section.count(start_marker) == 1, f"{document_name}: atomarer Repair-Dateilistenanfang fehlt oder ist doppelt")
    require(section.count(end_marker) == 1, f"{document_name}: atomarer Repair-Dateilistenende fehlt oder ist doppelt")
    list_text = section.split(start_marker, 1)[1].split(end_marker, 1)[0].strip()
    expected_list = "\n".join(f"- `{path}`" for path in V2737A_GATE_REPAIR_FILE_ORDER)
    require(list_text == expected_list, f"{document_name}: atomarer Repair muss exakt sechs kanonische Dateizeilen enthalten")
    shas = frozenset(re.findall(r"\b[0-9a-f]{40}\b", section))
    require(
        shas == V2737A_GATE_REPAIR_HISTORICAL_SHAS,
        f"{document_name}: historische Basis fehlt oder zukünftige SHA ist hartcodiert",
    )


def validate_v2737a_gate_repair_documents(
    state_text: str,
    task_text: str,
    cursor_text: str,
    masterlist_text: str,
) -> None:
    validate_exact_fields(
        state_text,
        {
            "Stand": "v27.37a-GATE-REPAIR",
            "Weiterer funktionaler Schritt autorisiert": "NEIN",
            "Aktuell autorisierter Task": "NONE",
            "Aktuelle Taskart": "Kein Task autorisiert",
        },
    )
    validate_exact_fields(
        task_text,
        {
            "Task-ID": "NONE",
            "Status": "BLOCKED",
            "Autorisiert": "NEIN",
            "Titel": "Kein Task autorisiert",
            "Funktionaler Ausgangsstand": "v27.35g",
            "Letzter abgeschlossener Kontrollschritt": "v27.37a-GATE-REPAIR",
            "Erlaubte Implementierungsdateien": "KEINE",
            "Commit erlaubt": "NEIN",
            "Push erlaubt": "NEIN",
        },
    )
    require(exact_field(cursor_text, "Stand") == "v27.37a-GATE-REPAIR", "CURSOR-Kontext muss auf v27.37a-GATE-REPAIR stehen")
    require(exact_field(masterlist_text, "Stand") == "v27.37a-GATE-REPAIR", "PROJECT_MASTERLIST muss auf v27.37a-GATE-REPAIR stehen")
    validate_project_paths(cursor_text, "CURSOR_MASTER_CONTEXT_ACCAOUI")
    documents = (state_text, task_text, cursor_text, masterlist_text)
    names = ("PROJECT_STATE_CURRENT", "CURRENT_TASK", "CURSOR_MASTER_CONTEXT_ACCAOUI", "PROJECT_MASTERLIST")
    for text, name in zip(documents, names):
        validate_v2737a_gate_repair_section(
            extract_v2737a_gate_repair_section(text, name),
            name,
        )
    rows = re.findall(r"(?m)^\| v27\.37a-GATE-REPAIR \|.*$", masterlist_text)
    require(
        len(rows) == 1 and "**erledigt**" in rows[0] and "Supabase NICHT LIVE" in rows[0],
        "PROJECT_MASTERLIST muss v27.37a-GATE-REPAIR exakt einmal als erledigt führen",
    )


def validate_v2737a_gate_repair_followup_section(
    section: str,
    document_name: str,
) -> None:
    validate_required_markers(
        section,
        V2737A_GATE_REPAIR_FOLLOWUP_SECTION_MARKERS,
        f"{document_name} / v27.37a-GATE-REPAIR-FOLLOWUP",
    )
    start_marker = "Der ausdrücklich freigegebene einmalige atomare FOLLOWUP-Repair umfasst exakt:"
    end_marker = "Keine siebte Datei ist erlaubt."
    require(section.count(start_marker) == 1, f"{document_name}: FOLLOWUP-Dateilistenanfang fehlt oder ist doppelt")
    require(section.count(end_marker) == 1, f"{document_name}: FOLLOWUP-Dateilistenende fehlt oder ist doppelt")
    list_text = section.split(start_marker, 1)[1].split(end_marker, 1)[0].strip()
    expected_list = "\n".join(f"- `{path}`" for path in V2737A_GATE_REPAIR_FILE_ORDER)
    require(list_text == expected_list, f"{document_name}: FOLLOWUP muss exakt sechs kanonische Dateizeilen enthalten")
    shas = frozenset(re.findall(r"\b[0-9a-f]{40}\b", section))
    require(
        shas == frozenset({V2737A_GATE_REPAIR_FOLLOWUP_BASE_SHA}),
        f"{document_name}: FOLLOWUP-Basis fehlt oder zukünftige SHA ist hartcodiert",
    )


def validate_v2737a_gate_repair_followup_documents(
    state_text: str,
    task_text: str,
    cursor_text: str,
    masterlist_text: str,
) -> None:
    validate_exact_fields(
        state_text,
        {
            "Stand": "v27.37a-GATE-REPAIR-FOLLOWUP",
            "Weiterer funktionaler Schritt autorisiert": "NEIN",
            "Aktuell autorisierter Task": "NONE",
            "Aktuelle Taskart": "Kein Task autorisiert",
        },
    )
    validate_exact_fields(
        task_text,
        {
            "Task-ID": "NONE",
            "Status": "BLOCKED",
            "Autorisiert": "NEIN",
            "Titel": "Kein Task autorisiert",
            "Funktionaler Ausgangsstand": "v27.35g",
            "Letzter abgeschlossener Kontrollschritt": "v27.37a-GATE-REPAIR-FOLLOWUP",
            "Erlaubte Implementierungsdateien": "KEINE",
            "Commit erlaubt": "NEIN",
            "Push erlaubt": "NEIN",
        },
    )
    require(exact_field(cursor_text, "Stand") == "v27.37a-GATE-REPAIR-FOLLOWUP", "CURSOR-Kontext muss auf v27.37a-GATE-REPAIR-FOLLOWUP stehen")
    require(exact_field(masterlist_text, "Stand") == "v27.37a-GATE-REPAIR-FOLLOWUP", "PROJECT_MASTERLIST muss auf v27.37a-GATE-REPAIR-FOLLOWUP stehen")
    validate_project_paths(cursor_text, "CURSOR_MASTER_CONTEXT_ACCAOUI")
    documents = (state_text, task_text, cursor_text, masterlist_text)
    names = ("PROJECT_STATE_CURRENT", "CURRENT_TASK", "CURSOR_MASTER_CONTEXT_ACCAOUI", "PROJECT_MASTERLIST")
    for text, name in zip(documents, names):
        validate_v2737a_gate_repair_followup_section(
            extract_v2737a_gate_repair_followup_section(text, name),
            name,
        )
    rows = re.findall(r"(?m)^\| v27\.37a-GATE-REPAIR-FOLLOWUP \|.*$", masterlist_text)
    require(
        len(rows) == 1 and "**erledigt**" in rows[0] and "Supabase NICHT LIVE" in rows[0],
        "PROJECT_MASTERLIST muss v27.37a-GATE-REPAIR-FOLLOWUP exakt einmal als erledigt führen",
    )


def validate_v2737a_gate_repair_products_unchanged() -> None:
    for relative_path in V2737A_GATE_REPAIR_FROZEN_PRODUCT_FILES:
        current_path = ROOT / relative_path
        require(current_path.is_file(), f"Eingefrorene Produktdatei fehlt: {relative_path}")
        baseline = run_git_bytes(["show", f"{V2737A_GATE_REPAIR_BASE_SHA}:{relative_path}"])
        require(
            current_path.read_bytes() == baseline,
            f"v27.37a-GATE-REPAIR darf Produktdatei nicht ändern: {relative_path}",
        )


def validate_v2737a_gate_repair_followup_products_unchanged() -> None:
    for relative_path in V2737A_GATE_REPAIR_FROZEN_PRODUCT_FILES:
        current_path = ROOT / relative_path
        require(current_path.is_file(), f"Eingefrorene Produktdatei fehlt: {relative_path}")
        baseline = run_git_bytes([
            "show",
            f"{V2737A_GATE_REPAIR_FOLLOWUP_BASE_SHA}:{relative_path}",
        ])
        require(
            current_path.read_bytes() == baseline,
            f"v27.37a-GATE-REPAIR-FOLLOWUP darf Produktdatei nicht ändern: {relative_path}",
        )


def v2737a_gate_repair_scope_facts_are_valid(
    *,
    phase: str,
    branch: str,
    head_is_base: bool,
    parent_is_base: bool,
    task_closed: bool,
    working_files: frozenset[str],
    committed_files: frozenset[str] | None,
    staged_files: frozenset[str],
    untracked_files: frozenset[str],
    products_unchanged: bool,
    documents_valid: bool,
) -> bool:
    if not (
        branch == "main"
        and task_closed
        and not staged_files
        and not untracked_files
        and products_unchanged
        and documents_valid
    ):
        return False
    if phase == V2737A_GATE_REPAIR_PHASE_PREPARED:
        return (
            head_is_base
            and not parent_is_base
            and working_files == V2737A_GATE_REPAIR_FILES
            and committed_files is None
        )
    if phase == V2737A_GATE_REPAIR_PHASE_COMMITTED:
        return (
            not head_is_base
            and parent_is_base
            and not working_files
            and committed_files == V2737A_GATE_REPAIR_FILES
        )
    return False


def v2737a_gate_repair_followup_scope_facts_are_valid(
    *,
    phase: str,
    branch: str,
    head_is_base: bool,
    parent_is_base: bool,
    task_closed: bool,
    working_files: frozenset[str],
    committed_files: frozenset[str] | None,
    staged_files: frozenset[str],
    untracked_files: frozenset[str],
    products_unchanged: bool,
    documents_valid: bool,
    initial_repair_committed: bool,
) -> bool:
    if not (
        branch == "main"
        and task_closed
        and not staged_files
        and not untracked_files
        and products_unchanged
        and documents_valid
        and initial_repair_committed
    ):
        return False
    if phase == V2737A_GATE_REPAIR_FOLLOWUP_PHASE_PREPARED:
        return (
            head_is_base
            and not parent_is_base
            and working_files == V2737A_GATE_REPAIR_FILES
            and committed_files is None
        )
    if phase == V2737A_GATE_REPAIR_FOLLOWUP_PHASE_COMMITTED:
        return (
            not head_is_base
            and parent_is_base
            and not working_files
            and committed_files == V2737A_GATE_REPAIR_FILES
        )
    return False


def validate_v2736f_closed_at_v2737a_gate_repair_base(
    v2736f_base_documents: tuple[str, str, str, str],
) -> tuple[
    str,
    V2736FRepairHistoryState,
    V2736FRepairWorkingTreeFact,
    tuple[str, str, str, str],
]:
    facts = read_v2736f_repair_commit_facts(V2737A_GATE_REPAIR_BASE_SHA)
    history = validate_v2736f_repair_history_facts(facts)
    require(history.state == V2736F_REPAIR_HISTORY_ORIGINAL_CLOSED, "v27.36f muss an der v27.37a-GATE-REPAIR-Basis vollständig closure_committed sein")
    validate_v2736f_repair_committed_closure_documents(facts, history)
    documents = (
        read_v2735f_commit_document(V2737A_GATE_REPAIR_BASE_SHA, "docs/PROJECT_STATE_CURRENT.md"),
        read_v2735f_commit_document(V2737A_GATE_REPAIR_BASE_SHA, V2735F_TASK_RELATIVE_PATH),
        read_v2735f_commit_document(V2737A_GATE_REPAIR_BASE_SHA, "docs/CURSOR_MASTER_CONTEXT_ACCAOUI.md"),
        read_v2735f_commit_document(V2737A_GATE_REPAIR_BASE_SHA, "docs/PROJECT_MASTERLIST.md"),
    )
    validate_v2736e_historical_sections_unchanged(documents, v2736f_base_documents)
    validate_v2736f_original_after_repair_documents(*documents, facts, history)
    fact = V2736FRepairWorkingTreeFact(
        branch="main",
        head=V2737A_GATE_REPAIR_BASE_SHA,
        origin_main=V2737A_GATE_REPAIR_BASE_SHA,
        diff_files=frozenset(),
        staged_files=frozenset(),
        untracked_files=frozenset(),
        status_lines=frozenset(),
        base_is_head_ancestor=True,
        base_is_origin_ancestor=True,
        origin_is_head_ancestor=True,
    )
    phase = validate_v2736f_repair_lifecycle_working_tree(
        history,
        V2736F_REPAIR_TASK_CLOSED,
        fact,
        V2736F_REPAIR_CLOSURE_KIND_ORIGINAL,
    )
    return phase, history, fact, documents


def validate_v2737a_gate_repair_lifecycle(
    state_text: str,
    task_text: str,
    cursor_text: str,
    masterlist_text: str,
) -> str:
    initial_repair_documents = tuple(
        read_v2735f_commit_document(V2737A_GATE_REPAIR_FOLLOWUP_BASE_SHA, path)
        for path in (
            "docs/PROJECT_STATE_CURRENT.md",
            "docs/tasks/CURRENT_TASK.md",
            "docs/CURSOR_MASTER_CONTEXT_ACCAOUI.md",
            "docs/PROJECT_MASTERLIST.md",
        )
    )
    validate_v2737a_gate_repair_documents(*initial_repair_documents)
    repair_lineage = run_git([
        "rev-list",
        "--parents",
        "-n",
        "1",
        V2737A_GATE_REPAIR_FOLLOWUP_BASE_SHA,
    ]).split()
    require(
        len(repair_lineage) == 2
        and repair_lineage[1] == V2737A_GATE_REPAIR_BASE_SHA,
        "Erster v27.37a-GATE-REPAIR muss direkt und mergefrei auf seiner Basis liegen",
    )
    repair_files = frozenset(
        line.strip().replace("\\", "/")
        for line in run_git([
            "diff",
            "--name-only",
            V2737A_GATE_REPAIR_BASE_SHA,
            V2737A_GATE_REPAIR_FOLLOWUP_BASE_SHA,
        ]).splitlines()
        if line.strip()
    )
    require(
        repair_files == V2737A_GATE_REPAIR_FILES,
        "Erster v27.37a-GATE-REPAIR muss exakt sechs Repair-Dateien umfassen",
    )
    validate_v2737a_gate_repair_followup_documents(
        state_text,
        task_text,
        cursor_text,
        masterlist_text,
    )
    validate_v2737a_gate_repair_products_unchanged()
    validate_v2737a_gate_repair_followup_products_unchanged()
    branch = run_git(["branch", "--show-current"]).strip()
    head = run_git(["rev-parse", "HEAD"]).strip()
    origin_main = run_git(["rev-parse", "origin/main"]).strip()
    require(origin_main in {V2737A_GATE_REPAIR_FOLLOWUP_BASE_SHA, head}, "origin/main liegt außerhalb der engen atomaren FOLLOWUP-Grenze")
    require(git_is_ancestor(V2737A_GATE_REPAIR_FOLLOWUP_BASE_SHA, head), "Stabile v27.37a-GATE-REPAIR-FOLLOWUP-Basis ist kein Vorfahr von HEAD")
    diff_files = frozenset(line.strip().replace("\\", "/") for line in run_git(["diff", "--name-only"]).splitlines() if line.strip())
    staged_files = frozenset(line.strip().replace("\\", "/") for line in run_git(["diff", "--cached", "--name-only"]).splitlines() if line.strip())
    untracked_files = frozenset(line.strip().replace("\\", "/") for line in run_git(["ls-files", "--others", "--exclude-standard"]).splitlines() if line.strip())
    status_lines = frozenset(line.replace("\\", "/") for line in run_git(["status", "--porcelain=v1", "--untracked-files=all"]).splitlines() if line)
    if head == V2737A_GATE_REPAIR_FOLLOWUP_BASE_SHA:
        phase = V2737A_GATE_REPAIR_FOLLOWUP_PHASE_PREPARED
        require(
            status_lines == frozenset(f" M {path}" for path in V2737A_GATE_REPAIR_FILES),
            "Atomarer FOLLOWUP-Repair muss im Working Tree exakt sechs ungestagte Dateien ändern",
        )
        committed_files = None
        parent_is_base = False
    else:
        phase = V2737A_GATE_REPAIR_FOLLOWUP_PHASE_COMMITTED
        lineage = run_git(["rev-list", "--parents", "-n", "1", head]).split()
        require(len(lineage) == 2, "Atomarer FOLLOWUP-Repair-Commit muss linear und mergefrei sein")
        parent = lineage[1]
        parent_is_base = parent == V2737A_GATE_REPAIR_FOLLOWUP_BASE_SHA
        committed_files = frozenset(line.strip().replace("\\", "/") for line in run_git(["diff", "--name-only", parent, head]).splitlines() if line.strip())
        require(not status_lines, "Atomarer FOLLOWUP-Repair-Commit benötigt einen sauberen Working Tree")
    history_roles = (
        ("atomic_repair",)
        if phase == V2737A_GATE_REPAIR_FOLLOWUP_PHASE_PREPARED
        else ("atomic_repair", "atomic_followup")
    )
    parent_relation = (
        "head_is_atomic_repair"
        if phase == V2737A_GATE_REPAIR_FOLLOWUP_PHASE_PREPARED
        else "followup_parent_is_atomic_repair"
    )
    require(
        v2737a_allowed_state_facts_are_valid(
            phase=phase,
            task_id=exact_field(task_text, "Task-ID") or "",
            status=exact_field(task_text, "Status") or "",
            authorized=exact_field(task_text, "Autorisiert") or "",
            allowed_implementation_files=frozenset(),
            working_files=diff_files,
            history_roles=history_roles,
            parent_relation=parent_relation,
            current_task_state="followup_closed",
        ),
        "Aktueller Zustand liegt außerhalb der positiven v27.37a-Task-/Scope-/Phasen-Allowlist",
    )
    require(
        v2737a_gate_repair_followup_scope_facts_are_valid(
            phase=phase,
            branch=branch,
            head_is_base=head == V2737A_GATE_REPAIR_FOLLOWUP_BASE_SHA,
            parent_is_base=parent_is_base,
            task_closed=True,
            working_files=diff_files,
            committed_files=committed_files,
            staged_files=staged_files,
            untracked_files=untracked_files,
            products_unchanged=True,
            documents_valid=True,
            initial_repair_committed=True,
        ),
        "Working Tree oder Commit entspricht nicht dem engen atomaren v27.37a-GATE-REPAIR-FOLLOWUP",
    )
    return phase


def run_v2737a_gate_repair_manipulation_matrix(
    state_text: str,
    task_text: str,
    cursor_text: str,
    masterlist_text: str,
) -> tuple[int, int, int]:
    repair_scope_positive_cases = (
        (V2737A_GATE_REPAIR_PHASE_PREPARED, True, False, V2737A_GATE_REPAIR_FILES, None),
        (V2737A_GATE_REPAIR_PHASE_COMMITTED, False, True, frozenset(), V2737A_GATE_REPAIR_FILES),
    )
    positive_cases = tuple(
        {
            "phase": state[0],
            "task_id": state[1],
            "status": state[2],
            "authorized": state[3],
            "allowed_implementation_files": state[4],
            "working_files": state[5],
            "history_roles": state[6],
            "parent_relation": state[7],
            "current_task_state": state[8],
        }
        for state in V2737A_ALLOWED_STATE_CONTRACTS
    )
    require(
        len(positive_cases) == 10,
        "v27.37a-Allowlist muss exakt zehn bekannte Task-/Phasen-Zustände enthalten",
    )
    for facts in positive_cases:
        require(
            v2737a_allowed_state_facts_are_valid(**facts),
            f"v27.37a-Allowlist-Positivsimulation fehlgeschlagen: {facts['phase']}",
        )
    authorization_template = next(
        facts
        for facts in positive_cases
        if facts["phase"] == "v2737a_authorization_prepared"
    )
    gate_paths = tuple(sorted(V2737A_GATE_FILES))
    authorization_subset_cases = (
        frozenset({"docs/tasks/CURRENT_TASK.md"}),
        frozenset({"docs/PROJECT_STATE_CURRENT.md"}),
        frozenset(gate_paths[:2]),
        frozenset(gate_paths[:4]),
        V2737A_GATE_FILES,
    )
    for working_files in authorization_subset_cases:
        facts = {**authorization_template, "working_files": working_files}
        require(
            v2737a_allowed_state_facts_are_valid(**facts),
            "v27.37a-authorization_prepared muss jede nichtleere Gate-Dateiteilmenge akzeptieren",
        )
    for phase, head_is_base, parent_is_base, working_files, committed_files in repair_scope_positive_cases:
        require(
            v2737a_gate_repair_scope_facts_are_valid(
                phase=phase,
                branch="main",
                head_is_base=head_is_base,
                parent_is_base=parent_is_base,
                task_closed=True,
                working_files=working_files,
                committed_files=committed_files,
                staged_files=frozenset(),
                untracked_files=frozenset(),
                products_unchanged=True,
                documents_valid=True,
            ),
            f"v27.37a-GATE-REPAIR-Positivsimulation fehlgeschlagen: {phase}",
        )
    scope_negative_cases = (
        {"branch": "feature"},
        {"task_closed": False},
        {"working_files": V2737A_GATE_REPAIR_FILES | {"app.js"}},
        {"working_files": V2737A_GATE_REPAIR_FILES - {"tools/preflight.py"}},
        {"staged_files": frozenset({"tools/preflight.py"})},
        {"untracked_files": frozenset({"unexpected.txt"})},
        {"products_unchanged": False},
        {"documents_valid": False},
        {"head_is_base": False},
        {"committed_files": V2737A_GATE_REPAIR_FILES | {"index.html"}},
        {"committed_files": V2737A_GATE_REPAIR_FILES - {"tools/preflight.py"}},
        {"parent_is_base": False},
        {"phase": "unknown_future_task"},
    )
    for override in scope_negative_cases:
        facts = {
            "phase": V2737A_GATE_REPAIR_PHASE_PREPARED,
            "branch": "main",
            "head_is_base": True,
            "parent_is_base": False,
            "task_closed": True,
            "working_files": V2737A_GATE_REPAIR_FILES,
            "committed_files": None,
            "staged_files": frozenset(),
            "untracked_files": frozenset(),
            "products_unchanged": True,
            "documents_valid": True,
        }
        if "committed_files" in override or "parent_is_base" in override:
            facts.update({
                "phase": V2737A_GATE_REPAIR_PHASE_COMMITTED,
                "head_is_base": False,
                "parent_is_base": True,
                "working_files": frozenset(),
                "committed_files": V2737A_GATE_REPAIR_FILES,
            })
        facts.update(override)
        require(
            not v2737a_gate_repair_scope_facts_are_valid(**facts),
            f"v27.37a-GATE-REPAIR-Scope-Manipulation wurde nicht blockiert: {override}",
        )
    positive_facts_by_phase = {
        facts["phase"]: facts for facts in positive_cases
    }
    authorization_facts = dict(
        positive_facts_by_phase["v2737a_authorization_prepared"]
    )
    committed_repair_facts = dict(
        positive_facts_by_phase[V2737A_GATE_REPAIR_PHASE_COMMITTED]
    )
    state_negative_cases = (
        (authorization_facts, {"task_id": "v27.38a"}, "v27.38a"),
        (authorization_facts, {"task_id": "v27.37b"}, "v27.37b"),
        (authorization_facts, {"task_id": "v99.99"}, "v99.99"),
        (authorization_facts, {"task_id": "v99"}, "v99"),
        (authorization_facts, {"task_id": "99.99"}, "99.99"),
        (authorization_facts, {"task_id": "v1"}, "v1"),
        (authorization_facts, {"task_id": "UNKNOWN"}, "UNKNOWN"),
        (authorization_facts, {"task_id": "foo"}, "foo"),
        (authorization_facts, {"task_id": "test-task"}, "test-task"),
        (authorization_facts, {"task_id": "!random!"}, "zufällige Zeichenfolge"),
        (authorization_facts, {"task_id": ""}, "leere Task-ID"),
        (
            authorization_facts,
            {"task_id": "NONE", "status": "AUTHORIZED"},
            "NONE / AUTHORIZED",
        ),
        (authorization_facts, {"task_id": "beliebiger-task"}, "beliebige andere Task-ID"),
        (authorization_facts, {"status": "BLOCKED"}, "v27.37a mit falschem Status"),
        (authorization_facts, {"authorized": "NEIN"}, "v27.37a mit falscher Autorisierung"),
        (
            authorization_facts,
            {"allowed_implementation_files": frozenset({"tools/preflight.py"})},
            "v27.37a mit falschem Implementierungsdateiscope",
        ),
        (
            authorization_facts,
            {"working_files": V2737A_GATE_FILES | {"app.js"}},
            "v27.37a mit zusätzlicher Datei",
        ),
        (authorization_facts, {"working_files": frozenset()}, "v27.37a mit leerer Gate-Dateimenge"),
        (
            authorization_facts,
            {"working_files": frozenset({"data/supabase-participant-auth-session-adapter.js"})},
            "v27.37a mit Implementierungsdatei",
        ),
        (
            authorization_facts,
            {"working_files": frozenset({"tools/preflight.py"})},
            "v27.37a mit Preflight-Datei",
        ),
        (
            authorization_facts,
            {"working_files": frozenset({"unknown/future-task.txt"})},
            "v27.37a mit unbekannter Datei",
        ),
        (
            authorization_facts,
            {"working_files": frozenset({"docs/tasks/CURRENT_TASK.md", "index.html"})},
            "v27.37a mit Gate- und Produktdatei",
        ),
        (authorization_facts, {"phase": "unknown_future_task"}, "v27.37a mit falscher Phase"),
        (
            authorization_facts,
            {"history_roles": ("atomic_repair", "v2737a_gate")},
            "v27.37a mit falscher Historie",
        ),
        (
            authorization_facts,
            {"parent_relation": "gate_parent_is_atomic_repair"},
            "v27.37a mit falscher Parent-Beziehung",
        ),
        (
            authorization_facts,
            {"current_task_state": "repair_closed"},
            "v27.37a mit falschem CURRENT_TASK-Zustand",
        ),
        (
            committed_repair_facts,
            {"history_roles": ("atomic_repair", "atomic_repair")},
            "erneuter v27.37a-GATE-REPAIR nach committed",
        ),
    )
    for base_facts, override, label in state_negative_cases:
        facts = dict(base_facts)
        facts.update(override)
        require(
            facts != base_facts,
            f"v27.37a-Allowlist-Manipulation ist wirkungslos: {label}",
        )
        require(
            not v2737a_allowed_state_facts_are_valid(**facts),
            f"v27.37a-Allowlist-Manipulation wurde nicht blockiert: {label}",
        )
    document_manipulations = 0
    sections = (
        (extract_v2737a_gate_repair_section(state_text, "PROJECT_STATE_CURRENT"), "PROJECT_STATE_CURRENT"),
        (extract_v2737a_gate_repair_section(task_text, "CURRENT_TASK"), "CURRENT_TASK"),
        (extract_v2737a_gate_repair_section(cursor_text, "CURSOR_MASTER_CONTEXT_ACCAOUI"), "CURSOR_MASTER_CONTEXT_ACCAOUI"),
        (extract_v2737a_gate_repair_section(masterlist_text, "PROJECT_MASTERLIST"), "PROJECT_MASTERLIST"),
    )
    for section, name in sections:
        for marker in (
            "Supabase bleibt NICHT LIVE.",
            "Nach dem Repair ist v27.37a weder ausgewählt noch autorisiert.",
            "Unbekannte zukünftige Tasks werden nicht pauschal zugelassen.",
        ):
            require(section.count(marker) == 1, f"{name}: Manipulation benötigt eindeutigen Marker")
            mutated = section.replace(marker, "", 1)
            try:
                validate_v2737a_gate_repair_section(mutated, name)
            except ValidationError:
                document_manipulations += 1
                continue
            raise ValidationError(f"v27.37a-GATE-REPAIR-Dokumentmanipulation wurde nicht blockiert: {name} / {marker}")
    canonical_section, canonical_name = sections[0]
    for path in V2737A_GATE_REPAIR_FILE_ORDER:
        needle = f"- `{path}`\n"
        require(needle in canonical_section, f"Manipulation benötigt kanonische Dateizeile: {path}")
        mutated = canonical_section.replace(needle, "", 1)
        try:
            validate_v2737a_gate_repair_section(mutated, canonical_name)
        except ValidationError:
            document_manipulations += 1
            continue
        raise ValidationError(f"v27.37a-GATE-REPAIR-Dateimanipulation wurde nicht blockiert: {path}")
    future_sha_suffix = "\nZukünftige SHA: `" + ("a" * 40) + "`\n"
    try:
        validate_v2737a_gate_repair_section(
            canonical_section + future_sha_suffix,
            canonical_name,
        )
    except ValidationError:
        document_manipulations += 1
    else:
        raise ValidationError(
            "v27.37a-GATE-REPAIR-Dokumentmanipulation wurde nicht blockiert: zukünftige SHA"
        )

    def mutate_current_task_field(
        source_text: str,
        field_name: str,
        replacement_value: str,
    ) -> str:
        current_value = exact_field(source_text, field_name)
        require(
            current_value is not None,
            f"CURRENT_TASK-Manipulation benötigt kanonisches Feld: {field_name}",
        )
        needle = f"{field_name}: {current_value}"
        require(
            source_text.count(needle) == 1,
            f"CURRENT_TASK-Manipulation benötigt eindeutiges Feld: {field_name}",
        )
        return source_text.replace(
            needle,
            f"{field_name}: {replacement_value}",
            1,
        )

    current_task_manipulations = (
        ("Task-ID", "v27.38a", "v27.38a"),
        ("Task-ID", "v27.37b", "v27.37b"),
        ("Task-ID", "v99.99", "v99.99"),
        ("Task-ID", "v99", "v99"),
        ("Task-ID", "99.99", "99.99"),
        ("Task-ID", "v1", "v1"),
        ("Task-ID", "UNKNOWN", "UNKNOWN"),
        ("Task-ID", "foo", "foo"),
        ("Task-ID", "test-task", "test-task"),
        ("Task-ID", "!random!", "zufällige Zeichenfolge"),
        ("Task-ID", "", "leere Task-ID"),
        ("Status", "AUTHORIZED", "NONE / AUTHORIZED"),
    )
    for field_name, replacement_value, label in current_task_manipulations:
        mutated_task_text = mutate_current_task_field(
            task_text,
            field_name,
            replacement_value,
        )
        try:
            validate_v2737a_gate_repair_documents(
                state_text,
                mutated_task_text,
                cursor_text,
                masterlist_text,
            )
        except ValidationError:
            document_manipulations += 1
            continue
        raise ValidationError(
            "v27.37a-GATE-REPAIR-CURRENT_TASK-Manipulation wurde nicht blockiert: "
            + label
        )
    return (
        document_manipulations,
        len(positive_cases) + len(authorization_subset_cases),
        len(scope_negative_cases) + len(state_negative_cases),
    )


def run_v2737a_gate_repair_followup_manipulation_matrix(
    state_text: str,
    task_text: str,
    cursor_text: str,
    masterlist_text: str,
) -> tuple[int, int, int]:
    prepared = {
        "phase": V2737A_GATE_REPAIR_FOLLOWUP_PHASE_PREPARED,
        "branch": "main",
        "head_is_base": True,
        "parent_is_base": False,
        "task_closed": True,
        "working_files": V2737A_GATE_REPAIR_FILES,
        "committed_files": None,
        "staged_files": frozenset(),
        "untracked_files": frozenset(),
        "products_unchanged": True,
        "documents_valid": True,
        "initial_repair_committed": True,
    }
    committed = {
        **prepared,
        "phase": V2737A_GATE_REPAIR_FOLLOWUP_PHASE_COMMITTED,
        "head_is_base": False,
        "parent_is_base": True,
        "working_files": frozenset(),
        "committed_files": V2737A_GATE_REPAIR_FILES,
    }
    for facts in (prepared, committed):
        require(
            v2737a_gate_repair_followup_scope_facts_are_valid(**facts),
            f"v27.37a-GATE-REPAIR-FOLLOWUP-Positivsimulation fehlgeschlagen: {facts['phase']}",
        )
    negative_cases = (
        (prepared, {"branch": "feature"}, "falscher Branch"),
        (prepared, {"working_files": V2737A_GATE_REPAIR_FILES | {"app.js"}}, "siebte Datei"),
        (prepared, {"working_files": V2737A_GATE_REPAIR_FILES - {"tools/preflight.py"}}, "fehlende Repair-Datei"),
        (prepared, {"staged_files": frozenset({"tools/preflight.py"})}, "staged Datei"),
        (prepared, {"untracked_files": frozenset({"unexpected.txt"})}, "unbekannte Datei"),
        (prepared, {"products_unchanged": False}, "Produktänderung"),
        (prepared, {"documents_valid": False}, "ungültige Dokumente"),
        (prepared, {"initial_repair_committed": False}, "erster Repair nicht committed"),
        (prepared, {"head_is_base": False}, "falscher Prepared-HEAD"),
        (committed, {"parent_is_base": False}, "kein direkter Folgecommit"),
        (committed, {"working_files": V2737A_GATE_REPAIR_FILES}, "Committed-Tree nicht clean"),
        (committed, {"committed_files": V2737A_GATE_REPAIR_FILES | {"index.html"}}, "Produktdatei im Commit"),
        (committed, {"committed_files": V2737A_GATE_REPAIR_FILES - {"tools/preflight.py"}}, "unvollständiger Commit"),
        (committed, {"phase": "v2737a_gate_repair_followup_atomic_repeated"}, "FOLLOWUP-Wiederholung"),
    )
    for baseline, override, label in negative_cases:
        facts = {**baseline, **override}
        require(facts != baseline, f"FOLLOWUP-Scope-Manipulation ist wirkungslos: {label}")
        require(
            not v2737a_gate_repair_followup_scope_facts_are_valid(**facts),
            f"v27.37a-GATE-REPAIR-FOLLOWUP-Manipulation wurde nicht blockiert: {label}",
        )
    sections = (
        (extract_v2737a_gate_repair_followup_section(state_text, "PROJECT_STATE_CURRENT"), "PROJECT_STATE_CURRENT"),
        (extract_v2737a_gate_repair_followup_section(task_text, "CURRENT_TASK"), "CURRENT_TASK"),
        (extract_v2737a_gate_repair_followup_section(cursor_text, "CURSOR_MASTER_CONTEXT_ACCAOUI"), "CURSOR_MASTER_CONTEXT_ACCAOUI"),
        (extract_v2737a_gate_repair_followup_section(masterlist_text, "PROJECT_MASTERLIST"), "PROJECT_MASTERLIST"),
    )
    document_manipulations = 0
    for section, name in sections:
        for marker in (
            "Supabase bleibt NICHT LIVE.",
            "v27.37a ist nach dem FOLLOWUP weiterhin nicht autorisiert",
            "Die globale `run_command()`-Semantik bleibt unverändert.",
            V2737A_GATE_REPAIR_FOLLOWUP_PHASE_PREPARED,
            V2737A_GATE_REPAIR_FOLLOWUP_PHASE_COMMITTED,
        ):
            require(section.count(marker) == 1, f"{name}: FOLLOWUP-Manipulation benötigt eindeutigen Marker")
            mutated = section.replace(marker, "", 1)
            require(mutated != section, f"{name}: FOLLOWUP-Dokumentmanipulation ist wirkungslos")
            try:
                validate_v2737a_gate_repair_followup_section(mutated, name)
            except ValidationError:
                document_manipulations += 1
                continue
            raise ValidationError(f"v27.37a-GATE-REPAIR-FOLLOWUP-Dokumentmanipulation wurde nicht blockiert: {name} / {marker}")
    canonical_section, canonical_name = sections[0]
    for path in V2737A_GATE_REPAIR_FILE_ORDER:
        needle = f"- `{path}`\n"
        require(canonical_section.count(needle) == 1, f"FOLLOWUP-Manipulation benötigt kanonische Dateizeile: {path}")
        mutated = canonical_section.replace(needle, "", 1)
        require(mutated != canonical_section, f"FOLLOWUP-Dateimanipulation ist wirkungslos: {path}")
        try:
            validate_v2737a_gate_repair_followup_section(mutated, canonical_name)
        except ValidationError:
            document_manipulations += 1
            continue
        raise ValidationError(f"v27.37a-GATE-REPAIR-FOLLOWUP-Dateimanipulation wurde nicht blockiert: {path}")
    future_sha_suffix = "\nZukünftige FOLLOWUP-SHA: `" + ("a" * 40) + "`\n"
    try:
        validate_v2737a_gate_repair_followup_section(
            canonical_section + future_sha_suffix,
            canonical_name,
        )
    except ValidationError:
        document_manipulations += 1
    else:
        raise ValidationError("v27.37a-GATE-REPAIR-FOLLOWUP-Dokumentmanipulation wurde nicht blockiert: zukünftige SHA")
    return document_manipulations, 2, len(negative_cases)


def main() -> int:
    try:
        state_text = read_required_text(STATE_PATH)
        task_text = read_required_text(TASK_PATH)
        agents_text = read_required_text(AGENTS_PATH)
        cursor_context_text = read_required_text(CURSOR_CONTEXT_PATH)
        masterlist_text = read_required_text(MASTERLIST_PATH)
        preflight_text = read_required_text(PREFLIGHT_PATH)

        validate_agents_text(agents_text)
        validate_preflight_text(preflight_text)
        (
            git_utf8_manipulation_checks,
            git_utf8_positive_tests,
            git_utf8_negative_tests,
        ) = run_git_utf8_self_checks()
        validate_v2735c_control_commit_history()
        validate_v2735d_completion_commit_history()
        validate_v2735e_closure_commit_history()
        validate_v2735g_authorization_commit_history()
        validate_v2735g_gate_fix_commit_history()
        validate_v2735g_completion_commit_history()
        validate_v2735f_authorization_commit_history()
        lifecycle_history, v2735f_base_documents = validate_v2735f_completed_base()
        (
            v2736a_history,
            v2736a_base_documents,
        ) = validate_v2736a_completed_base()
        v2736a_working_tree = read_v2736a_working_tree_fact()
        (
            v2736b_history,
            v2736b_base_documents,
        ) = validate_v2736b_completed_base()
        v2736b_working_tree = read_v2736b_working_tree_fact()
        (
            v2736c_history,
            v2736c_base_documents,
        ) = validate_v2736c_completed_base()
        v2736c_working_tree = synthetic_v2736c_closed_working_fact()
        (
            v2736d_history,
            v2736d_base_documents,
        ) = validate_v2736d_completed_base()
        v2736d_working_tree = synthetic_v2736d_closed_working_fact()
        (
            v2736e_history,
            v2736e_base_documents,
        ) = validate_v2736e_completed_base()
        v2736e_working_tree = synthetic_v2736e_closed_working_fact()
        (
            v2736f_history,
            v2736f_base_documents,
            v2736f_working_tree,
        ) = validate_v2736f_implemented_repair_base(
            v2736e_base_documents,
        )
        (
            v2736f_repair_phase,
            v2736f_repair_history,
            v2736f_repair_working_tree,
            v2736f_closed_documents,
        ) = validate_v2736f_closed_at_v2737a_gate_repair_base(
            v2736f_base_documents,
        )
        v2737a_gate_repair_phase = validate_v2737a_gate_repair_lifecycle(
            state_text,
            task_text,
            cursor_context_text,
            masterlist_text,
        )
        v2737a_gate_repair_documents = tuple(
            read_v2735f_commit_document(
                V2737A_GATE_REPAIR_FOLLOWUP_BASE_SHA,
                path,
            )
            for path in (
                "docs/PROJECT_STATE_CURRENT.md",
                "docs/tasks/CURRENT_TASK.md",
                "docs/CURSOR_MASTER_CONTEXT_ACCAOUI.md",
                "docs/PROJECT_MASTERLIST.md",
            )
        )
        (
            manipulation_checks,
            positive_phase_tests,
            lifecycle_negative_tests,
        ) = run_v2735f_authorization_manipulation_matrix(
            *v2735f_base_documents,
            lifecycle_history.implementation_commit,
        )
        manipulation_checks += git_utf8_manipulation_checks
        (
            v2736a_manipulation_checks,
            v2736a_positive_tests,
            v2736a_negative_tests,
        ) = run_v2736a_lifecycle_manipulation_matrix(
            *v2736a_base_documents,
            v2736a_history,
            v2736a_working_tree,
        )
        manipulation_checks += v2736a_manipulation_checks
        (
            v2736b_manipulation_checks,
            v2736b_positive_tests,
            v2736b_negative_tests,
        ) = run_v2736b_manipulation_matrix(
            *v2736b_base_documents,
            v2736b_history,
            v2736b_working_tree,
        )
        manipulation_checks += v2736b_manipulation_checks
        (
            v2736c_manipulation_checks,
            v2736c_positive_tests,
            v2736c_negative_tests,
        ) = run_v2736c_manipulation_matrix(
            *v2736c_base_documents,
            v2736c_history,
            v2736c_working_tree,
        )
        manipulation_checks += v2736c_manipulation_checks
        (
            v2736d_manipulation_checks,
            v2736d_positive_tests,
            v2736d_negative_tests,
        ) = run_v2736d_manipulation_matrix(
            *v2736d_base_documents,
            v2736d_history,
            v2736d_working_tree,
        )
        manipulation_checks += v2736d_manipulation_checks
        (
            v2736e_manipulation_checks,
            v2736e_positive_tests,
            v2736e_negative_tests,
        ) = run_v2736e_manipulation_matrix(
            *v2736e_base_documents,
            v2736e_history,
            v2736e_working_tree,
        )
        manipulation_checks += v2736e_manipulation_checks
        (
            v2736f_manipulation_checks,
            v2736f_positive_tests,
            v2736f_negative_tests,
        ) = run_v2736f_manipulation_matrix(
            *v2736f_base_documents,
            v2736f_history,
            v2736f_working_tree,
        )
        manipulation_checks += v2736f_manipulation_checks
        (
            v2736f_repair_manipulation_checks,
            v2736f_repair_positive_tests,
            v2736f_repair_negative_tests,
        ) = run_v2736f_repair_manipulation_matrix(
            *v2736f_closed_documents,
            v2736f_repair_history,
            v2736f_repair_working_tree,
        )
        manipulation_checks += v2736f_repair_manipulation_checks
        (
            v2737a_gate_repair_manipulation_checks,
            v2737a_gate_repair_positive_tests,
            v2737a_gate_repair_negative_tests,
        ) = run_v2737a_gate_repair_manipulation_matrix(
            *v2737a_gate_repair_documents,
        )
        manipulation_checks += v2737a_gate_repair_manipulation_checks
        (
            v2737a_gate_repair_followup_manipulation_checks,
            v2737a_gate_repair_followup_positive_tests,
            v2737a_gate_repair_followup_negative_tests,
        ) = run_v2737a_gate_repair_followup_manipulation_matrix(
            state_text,
            task_text,
            cursor_context_text,
            masterlist_text,
        )
        manipulation_checks += v2737a_gate_repair_followup_manipulation_checks
    except ValidationError as exc:
        print(f"FEHLER: {exc}")
        print("STOPP: Projektkontinuität oder Task-Steuerung verletzt.")
        return 1

    print("Projektkontinuität, abgeschlossener v27.36f-Verlauf und v27.37a-GATE-REPAIR-FOLLOWUP: OK")
    task_summary = "NONE / BLOCKED / Autorisiert NEIN"
    print(
        "PROJECT_STATE_CURRENT: letzter funktionaler Stand v27.35g / "
        f"CURRENT_TASK {task_summary}"
    )
    print("Historische v27.35f-Phase am Ausgangscommit: phase_4_closure_committed")
    print(
        "Dynamischer IMPLEMENTATION-Commit: "
        f"{lifecycle_history.implementation_commit or 'noch nicht vorhanden'}"
    )
    print("AGENTS-Regeln, Cursor-Kontext und Chatwechsel-Protokoll: OK")
    print("Projektpfade Arbeit und Zuhause: OK")
    print("Preflight-Einbindung: OK")
    print(
        "Git-UTF-8-Selbstprüfung: "
        f"{git_utf8_positive_tests} / PASS; Negativtests: "
        f"{git_utf8_negative_tests} / vollständig blockiert"
    )
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
        "v27.35g-Autorisierung historisch sauber: nur Steuerungsdateien "
        f"zwischen {V2735G_GATE_SHA} und {V2735G_AUTHORIZATION_SHA} geändert, "
        "keine Funktionsdatei"
    )
    print(
        "v27.35g-Gate-Korrektur historisch sauber: nur Steuerungsdateien "
        f"zwischen {V2735G_AUTHORIZATION_SHA} und {V2735G_GATE_FIX_SHA} "
        "geändert, keine Funktionsdatei"
    )
    print(
        "v27.35g-Abschlusscommit historisch sauber: nur app.js und "
        f"{V2735G_SCORING_FIX_REPORT_FILE} zwischen {V2735G_GATE_FIX_SHA} und "
        f"{V2735G_COMPLETION_SHA} geändert, index.html/style.css unverändert"
    )
    print(
        "v27.35f-Autorisierung historisch sauber: exakt fünf Steuerungsdateien "
        f"zwischen {V2735F_PREAUTHORIZATION_SHA} und "
        f"{V2735F_AUTHORIZATION_SHA} geändert"
    )
    print(
        "v27.35f-erster Gate-Fix historisch sauber: exakt fünf Gate-Dateien "
        f"zwischen {V2735F_AUTHORIZATION_SHA} und "
        f"{V2735F_FIRST_GATE_FIX_SHA} geändert"
    )
    print(
        "v27.35f-Lebenszyklus: Commitrollen dynamisch aus Git-Historie, "
        "Dateiumfang, Taskzustand und Notiz-SHA klassifiziert; finaler SHA-256 "
        f"{V2735F_NOTE_SHA256}"
    )
    print(
        "v27.36a abgeschlossen: stabile Basis "
        f"{V2736A_AUTHORIZATION_BASE_SHA} ist Vorfahr von "
        f"{V2736B_AUTHORIZATION_BASE_SHA}; "
        f"{len(v2736a_history.gate_commits)} GATE-Commit(s); Audit-Commit "
        f"{v2736a_history.audit_commit}"
    )
    print(
        "v27.36b abgeschlossen: stabile Basis "
        f"{V2736B_AUTHORIZATION_BASE_SHA} ist Vorfahr von HEAD; "
        f"{len(v2736b_history.gate_commits)} GATE-Commit(s); "
        "IMPLEMENTATION-Commit "
        f"{v2736b_history.implementation_commit}; Closure-HEAD "
        f"{V2736C_AUTHORIZATION_BASE_SHA}"
    )
    print("Abgeschlossene v27.36c-Phase: closure_committed")
    print(
        "v27.36c abgeschlossen: stabile Basis "
        f"{V2736C_AUTHORIZATION_BASE_SHA} ist Vorfahr von "
        f"{V2736D_AUTHORIZATION_BASE_SHA}; "
        f"{len(v2736c_history.gate_commits)} GATE-Commit(s); "
        "IMPLEMENTATION-Commit "
        f"{v2736c_history.implementation_commit}; Closure-HEAD "
        f"{V2736D_AUTHORIZATION_BASE_SHA}"
    )
    print(
        "v27.36c-Sicherheitsgrenze: injizierter Bootstrap-Provider, "
        "v27.36b-Adapter-Factory und UTC-Zeit; nur bootstrap.getClient(), "
        "lokaler Fake-Bootstrap, fail-closed; bestehender Bootstrap und Adapter "
        "unverändert; keine Bootstrap-, Config-, SDK- oder Live-State-Schalter; "
        "kein App-, UI-, SQL-, Migrations-, "
        "Datenbank- oder Netzwerkzugriff; "
        "Live-Supabase NEIN"
    )
    print("Abgeschlossene v27.36d-Phase: closure_committed")
    print(
        "v27.36d abgeschlossen: stabile Basis "
        f"{V2736D_AUTHORIZATION_BASE_SHA} ist Vorfahr von "
        f"{V2736E_AUTHORIZATION_BASE_SHA}; "
        f"{len(v2736d_history.gate_commits)} GATE-Commit(s); "
        "IMPLEMENTATION-Commit "
        f"{v2736d_history.implementation_commit}; Closure-HEAD "
        f"{V2736E_AUTHORIZATION_BASE_SHA}"
    )
    print("Abgeschlossene v27.36e-Phase: closure_committed")
    print(
        "v27.36e abgeschlossen: stabile Basis "
        f"{V2736E_AUTHORIZATION_BASE_SHA} ist Vorfahr von "
        f"{V2736F_AUTHORIZATION_BASE_SHA}; "
        f"{len(v2736e_history.gate_commits)} GATE-Commit(s); "
        "IMPLEMENTATION-Commit "
        f"{v2736e_history.implementation_commit}; Closure-HEAD "
        f"{V2736F_AUTHORIZATION_BASE_SHA}"
    )
    print(
        "v27.36e-Sicherheitsgrenze: CommonJS-kompatible Bestandsmodule, "
        "kontrollierte Browser-Exports und ein lokaler Provider mit ausschließlich "
        "resolveAccess(); keine duplizierte Fachlogik, keine App-/UI-Änderung, "
        "keine Live-, Datenbank- oder Netzwerkaktivierung; Live-Supabase NEIN"
    )
    print("Abgeschlossene v27.36f-Implementierungsphase an der Repair-Basis: implementation_committed")
    print(f"Aktuelle v27.36f-REPAIR-Phase: {v2736f_repair_phase}")
    print(f"Aktuelle v27.37a-GATE-REPAIR-FOLLOWUP-Phase: {v2737a_gate_repair_phase}")
    print(
        "v27.36f-REPAIR-Synchronisation: lokaler HEAD "
        f"{v2736f_repair_working_tree.head}; origin/main "
        f"{v2736f_repair_working_tree.origin_main}; origin/main muss legitimer "
        "Vorfahr des lokalen HEAD sein"
    )
    print(
        "v27.36f-Sicherheitsgrenze: Default data-enabled=false; nur exaktes "
        "true fordert die lokale Browser-Komposition an; angeforderte Fehler "
        "bleiben fail-closed ohne lokalen Fallback; keine automatische "
        "Client-Erzeugung und keine Live-, Datenbank- oder Netzwerkaktivierung; "
        "Live-Supabase NEIN"
    )
    print(f"Vierphasige Positivsimulationen: {positive_phase_tests} / PASS")
    print(
        "Lebenszyklus-Negativtests: "
        f"{lifecycle_negative_tests} / vollständig blockiert"
    )
    print(
        "v27.36a-Phasensimulationen: "
        f"{v2736a_positive_tests} / PASS; Negativtests: "
        f"{v2736a_negative_tests} / vollständig blockiert"
    )
    print(
        "v27.36b-Phasensimulationen: "
        f"{v2736b_positive_tests} / PASS; Negativtests: "
        f"{v2736b_negative_tests} / vollständig blockiert"
    )
    print(
        "v27.36c-Phasensimulationen: "
        f"{v2736c_positive_tests} / PASS; Negativtests: "
        f"{v2736c_negative_tests} / vollständig blockiert"
    )
    print(
        "v27.36d-Phasensimulationen: "
        f"{v2736d_positive_tests} / PASS; Negativtests: "
        f"{v2736d_negative_tests} / vollständig blockiert"
    )
    print(
        "v27.36e-Phasensimulationen: "
        f"{v2736e_positive_tests} / PASS; Negativtests: "
        f"{v2736e_negative_tests} / vollständig blockiert"
    )
    print(
        "v27.36f-Phasensimulationen: "
        f"{v2736f_positive_tests} / PASS; Negativtests: "
        f"{v2736f_negative_tests} / vollständig blockiert"
    )
    print(
        "v27.36f-REPAIR-Phasensimulationen: "
        f"{v2736f_repair_positive_tests} / PASS; Negativtests: "
        f"{v2736f_repair_negative_tests} / vollständig blockiert"
    )
    print(
        "v27.37a-GATE-REPAIR-Phasensimulationen: "
        f"{v2737a_gate_repair_positive_tests} / PASS; Negativtests: "
        f"{v2737a_gate_repair_negative_tests} / vollständig blockiert"
    )
    print(
        "v27.37a-GATE-REPAIR-FOLLOWUP-Phasensimulationen: "
        f"{v2737a_gate_repair_followup_positive_tests} / PASS; Negativtests: "
        f"{v2737a_gate_repair_followup_negative_tests} / vollständig blockiert"
    )
    print(
        f"Manipulationsmatrix: {manipulation_checks} Blockierungen bestätigt "
        f"(davon v27.36a: {v2736a_manipulation_checks}; "
        f"v27.36b: {v2736b_manipulation_checks}; "
        f"v27.36c: {v2736c_manipulation_checks}; "
        f"v27.36d: {v2736d_manipulation_checks}; "
        f"v27.36e: {v2736e_manipulation_checks}; "
        f"v27.36f: {v2736f_manipulation_checks}; "
        f"v27.36f-REPAIR: {v2736f_repair_manipulation_checks}; "
        f"v27.37a-GATE-REPAIR: {v2737a_gate_repair_manipulation_checks}; "
        "v27.37a-GATE-REPAIR-FOLLOWUP: "
        f"{v2737a_gate_repair_followup_manipulation_checks})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
