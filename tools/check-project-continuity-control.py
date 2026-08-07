#!/usr/bin/env python3
"""Prüft Autorisierung und Implementierungs-Gate des Dokumentationstasks v27.35f.

v27.35g bleibt der letzte abgeschlossene funktionale Stand. Der
Vorautorisierungsstand, der historische Autorisierungscommit und der
bekannte legitime Gate-Fix-Commit werden getrennt geprüft. Der aktuelle
HEAD darf ein späterer Gate-Commit sein, wenn die Autorisierungsbasis ein
Vorfahr bleibt und der gesamte committete Bereich ausschließlich die
fünf Gate-Dateien enthält. Im Working Tree sind entweder exakt diese
fünf Dateien oder keine getrackte Datei verändert; die finale
Wettbewerbsnotiz bleibt als einzige ungetrackte Datei per SHA-256
unverändert. App- und Funktionsdateien bleiben gesperrt.
"""

from __future__ import annotations

import hashlib
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


def validate_v2735f_committed_gate_files(committed_files: set[str]) -> None:
    """Blockiert jede committete Datei außerhalb der fünf Gate-Dateien."""
    unexpected_files = committed_files - set(V2735F_GATE_CONTROL_FILES)
    require(
        not unexpected_files,
        (
            "Seit der v27.35f-Autorisierungsbasis wurden unzulässige Dateien "
            f"committet: {sorted(unexpected_files)}"
        ),
    )


def validate_v2735f_working_tree_snapshot(
    diff_files: set[str],
    staged_files: set[str],
    untracked_files: set[str],
    status_lines: set[str],
) -> None:
    """Akzeptiert exakt den Zustand vor oder nach einem legitimen Gate-Commit."""
    expected_gate_files = set(V2735F_GATE_CONTROL_FILES)
    require(
        diff_files in (set(), expected_gate_files),
        (
            "Im v27.35f-Gate sind lokal entweder exakt die fünf Gate-Dateien "
            "oder nach deren Commit keine getrackten Dateien verändert: "
            f"{sorted(diff_files)}"
        ),
    )
    require(
        not staged_files,
        (
            "Im v27.35f-Gate dürfen keine Änderungen gestaged sein: "
            f"{sorted(staged_files)}"
        ),
    )
    require(
        untracked_files == {V2735F_NOTE_FILE},
        (
            "Im v27.35f-Gate muss die Wettbewerbsnotiz die einzige "
            f"ungetrackte Datei sein: {sorted(untracked_files)}"
        ),
    )

    note_status = f"?? {V2735F_NOTE_FILE}"
    status_before_commit = {
        *(f" M {path}" for path in expected_gate_files),
        note_status,
    }
    status_after_commit = {note_status}
    require(
        status_lines in (status_before_commit, status_after_commit),
        (
            "git status muss exakt den v27.35f-Gate-Zustand vor oder nach "
            f"dem Gate-Commit zeigen: {sorted(status_lines)}"
        ),
    )


def validate_v2735f_implementation_gate_working_tree() -> None:
    """Prüft ancestry-/Diff-basiert Commitbereich und Working Tree."""
    require(
        (ROOT / ".git").exists(),
        "Kein Git-Repository unter ROOT gefunden",
    )
    require(
        run_git(["branch", "--show-current"]).strip() == "main",
        "v27.35f-Implementierungs-Gate muss auf Branch main laufen",
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

    committed_files = {
        line.strip().replace("\\", "/")
        for line in run_git(
            [
                "diff",
                "--name-only",
                V2735F_AUTHORIZATION_SHA,
                current_head,
            ]
        ).splitlines()
        if line.strip()
    }
    validate_v2735f_committed_gate_files(committed_files)
    require(
        run_git(
            [
                "ls-tree",
                "-r",
                "--name-only",
                current_head,
                "--",
                V2735F_NOTE_FILE,
            ]
        ).strip()
        == "",
        "Die Wettbewerbsnotiz muss bis zum aktuellen HEAD ungetrackt bleiben",
    )

    note_path = ROOT / V2735F_NOTE_FILE
    require(
        sha256_file(note_path) == V2735F_NOTE_SHA256,
        f"{V2735F_NOTE_FILE} wurde während des Gate-Korrekturschritts verändert",
    )

    diff_files = {
        line.strip().replace("\\", "/")
        for line in run_git(["diff", "--name-only"]).splitlines()
        if line.strip()
    }
    staged_files = {
        line.strip().replace("\\", "/")
        for line in run_git(["diff", "--cached", "--name-only"]).splitlines()
        if line.strip()
    }

    untracked_files = {
        line.strip().replace("\\", "/")
        for line in run_git(
            ["ls-files", "--others", "--exclude-standard"]
        ).splitlines()
        if line.strip()
    }
    status_lines = {
        line.replace("\\", "/")
        for line in run_git(
            ["status", "--porcelain=v1", "--untracked-files=all"]
        ).splitlines()
        if line
    }
    validate_v2735f_working_tree_snapshot(
        diff_files,
        staged_files,
        untracked_files,
        status_lines,
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
                    V2735F_AUTHORIZATION_SHA,
                    current_head,
                    "--",
                    relative_path,
                ]
            ).strip()
            == "",
            f"App-, Funktions- oder historische Berichtsdatei verändert: {relative_path}",
        )


def run_v2735f_authorization_manipulation_matrix(
    state_text: str,
    task_text: str,
    cursor_context_text: str,
    masterlist_text: str,
) -> int:
    """Bestätigt die verbindlichen Blockierungen des v27.35f-Vertrags."""
    checks = 0

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

    expected_gate_files = set(V2735F_GATE_CONTROL_FILES)
    note_status = f"?? {V2735F_NOTE_FILE}"
    status_before_commit = {
        *(f" M {path}" for path in expected_gate_files),
        note_status,
    }
    status_after_commit = {note_status}

    validate_v2735f_committed_gate_files(set())
    validate_v2735f_committed_gate_files(expected_gate_files)
    validate_v2735f_working_tree_snapshot(
        expected_gate_files,
        set(),
        {V2735F_NOTE_FILE},
        status_before_commit,
    )
    validate_v2735f_working_tree_snapshot(
        set(),
        set(),
        {V2735F_NOTE_FILE},
        status_after_commit,
    )

    gate_state_manipulations = (
        (
            lambda _text: validate_v2735f_committed_gate_files(
                expected_gate_files | {"app.js"}
            ),
            "committete App-Datei seit Autorisierungsbasis",
        ),
        (
            lambda _text: validate_v2735f_committed_gate_files(
                expected_gate_files | {V2735F_NOTE_FILE}
            ),
            "committete Wettbewerbsnotiz seit Autorisierungsbasis",
        ),
        (
            lambda _text: validate_v2735f_working_tree_snapshot(
                {CHECKER_RELATIVE_PATH},
                set(),
                {V2735F_NOTE_FILE},
                {f" M {CHECKER_RELATIVE_PATH}", note_status},
            ),
            "unvollständiger lokaler Gate-Dateisatz",
        ),
        (
            lambda _text: validate_v2735f_working_tree_snapshot(
                expected_gate_files | {"app.js"},
                set(),
                {V2735F_NOTE_FILE},
                status_before_commit | {" M app.js"},
            ),
            "zusätzliche lokale App-Datei",
        ),
        (
            lambda _text: validate_v2735f_working_tree_snapshot(
                expected_gate_files,
                {CHECKER_RELATIVE_PATH},
                {V2735F_NOTE_FILE},
                status_before_commit,
            ),
            "gestagte Gate-Datei",
        ),
        (
            lambda _text: validate_v2735f_working_tree_snapshot(
                expected_gate_files,
                set(),
                {V2735F_NOTE_FILE, "unexpected.txt"},
                status_before_commit | {"?? unexpected.txt"},
            ),
            "zusätzliche ungetrackte Datei",
        ),
        (
            lambda _text: validate_v2735f_working_tree_snapshot(
                set(),
                set(),
                set(),
                set(),
            ),
            "fehlende ungetrackte Wettbewerbsnotiz",
        ),
    )
    for validator, label in gate_state_manipulations:
        must_reject(validator, "", label)
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

        validate_v2735f_authorized_state_text(state_text)
        validate_v2735f_authorized_task_text(task_text)
        validate_agents_text(agents_text)
        validate_v2735f_cursor_context_text(cursor_context_text)
        validate_v2735f_masterlist_text(masterlist_text)
        validate_preflight_text(preflight_text)
        validate_v2735c_control_commit_history()
        validate_v2735d_completion_commit_history()
        validate_v2735e_closure_commit_history()
        validate_v2735g_authorization_commit_history()
        validate_v2735g_gate_fix_commit_history()
        validate_v2735g_completion_commit_history()
        validate_v2735f_authorization_commit_history()
        validate_v2735f_implementation_gate_working_tree()
        manipulation_checks = run_v2735f_authorization_manipulation_matrix(
            state_text,
            task_text,
            cursor_context_text,
            masterlist_text,
        )
    except ValidationError as exc:
        print(f"FEHLER: {exc}")
        print("STOPP: Projektkontinuität oder Task-Steuerung verletzt.")
        return 1

    print("Projektkontinuität und v27.35f-Implementierungs-Gate: OK")
    print(
        "PROJECT_STATE_CURRENT: letzter funktionaler Stand v27.35g / "
        "einziger autorisierter Dokumentationstask v27.35f"
    )
    print(
        "CURRENT_TASK: v27.35f / AUTHORIZED / Autorisiert JA / "
        f"Umsetzung nur {V2735F_NOTE_FILE} / kein Commit, kein Push"
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
        "v27.35f-Implementierungs-Gate: Autorisierungsbasis ist Vorfahr des "
        "aktuellen HEAD; committeter Bereich enthält ausschließlich Gate-Dateien; "
        "Working Tree entspricht dem Zustand vor oder nach dem Gate-Commit; "
        "Wettbewerbsnotiz ist einzige ungetrackte Datei und finaler SHA-256 "
        f"{V2735F_NOTE_SHA256}; App- und Funktionsdateien unverändert"
    )
    print(f"Manipulationsmatrix: {manipulation_checks} Blockierungen bestätigt")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
