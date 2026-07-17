from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
ADAPTER = ROOT / "data" / "supabase-client-adapter.js"


def fail(message: str) -> None:
    print(f"FEHLER: {message}")
    sys.exit(1)


if not ADAPTER.is_file():
    fail("Supabase-Client-Adapter fehlt.")

text = ADAPTER.read_text(encoding="utf-8")
lower = text.lower()

required_markers = (
    "// stand: v27.29e",
    'version: "v27.29b"',
    'version: "v27.29c"',
    'version: "v27.29d"',
    'version: "v27.29e"',
    "function getparticipantexamresulthistoryrpcstate()",
    "function normalizeparticipantexamresulthistorypagination(options)",
    "function listparticipantfullexamresults(options)",
    'rpcname: "accaoui_list_full_exam_results"',
    'rpcparameternames: ["p_limit", "p_offset"]',
    "defaultlimit: 20",
    "maxlimit: 50",
    "maxoffset: 10000",
    "cancallrpc: false",
    "islivecallimplemented: false",
    "isblockedsafely: true",
    "number.isinteger(limit)",
    "number.isinteger(offset)",
    "p_limit: pagination.limit",
    "p_offset: pagination.offset",
    'status: "exam_result_history_rpc_blocked_safe_local_mode"',
    "promise.resolve({",
    "participantexamresulthistoryrpcstatus:",
    "isparticipantexamresulthistoryrpcprepared:",
    "cancallparticipantexamresulthistoryrpc:",
    "participantexamresulthistoryrpcstate,",
    "getparticipantexamresulthistoryrpcstate,",
    "listparticipantfullexamresults,",
    'status: "local_dashboard_exam_history_hidden"',
    "function getparticipantdashboardexamhistorydatasourcestate()",
    'status: "local_dashboard_exam_history_data_source_blocked"',
    'sourcetype: "supabase_rpc"',
    "isprepared: true",
    "canload: false",
    "hasdata: false",
    "islivecall: false",
    "isblockedsafely: true",
    "datasourcestatus:",
    "datasourcetype:",
    "datasourcerpcname:",
    "isdatasourceprepared:",
    "canloadfromdatasource:",
    "isdatasourceblockedsafely:",
    "participantdashboardexamhistorydatasourcestatus:",
    "getparticipantdashboardexamhistorydatasourcestate,",
    "participantdashboardexamhistorydatasourcestate,",
    "function normalizeparticipantfullexamresultrow(row)",
    "function normalizeparticipantfullexamresultrows(rows)",
    "row.exam_attempt_id",
    "row.course_id",
    "row.course_title",
    "row.score_points",
    "row.max_points",
    "row.passed",
    "row.started_at",
    "row.finished_at",
    "row.total_count",
    "maxpoints !== 120",
    "passed !== (scorepoints >= 60)",
    "finishedatms < startedatms",
    "number.issafeinteger(totalcount)",
    "totalcount < 1",
    "seenattemptids.has(entry.examattemptid)",
    "entry.totalcount !== expectedtotalcount",
    "expectedtotalcount < entries.length",
    'normalizername: "normalizeparticipantfullexamresultrows"',
    "isnormalizerprepared: true",
    "cannormalizerows: true",
    "normalizedentries: []",
    "datasourcenormalizername:",
    "isdatasourcenormalizerprepared:",
    "cannormalizedatasourcerows:",
    "participantdashboardexamhistorydatasourcenormalizername:",
    "isparticipantdashboardexamhistorydatasourcenormalizerprepared:",
    "cannormalizeparticipantdashboardexamhistoryrows:",
    "normalizeparticipantfullexamresultrow,",
    "normalizeparticipantfullexamresultrows,",
    "function aggregateparticipantfullexamresultrows(rows)",
    'metricsscope: "page_only"',
    "pageentrycount",
    "pagepassedcount",
    "pagefailedcount",
    "pagebestscore",
    "pageaveragescore",
    "pagepassratepercent",
    "pagelatestfinishedat",
    "pagelatestexamattemptid",
    "canpopulateglobaloutcomecounts: false",
    "globalpassedcount: null",
    "globalfailedcount: null",
    'aggregatorname: "aggregateparticipantfullexamresultrows"',
    "isaggregatorprepared: true",
    "canaggregaterows: true",
    "datasourceaggregatorname:",
    "isdatasourceaggregatorprepared:",
    "canaggregatedatasourcerows:",
    "datasourcemetricsscope:",
    "participantdashboardexamhistorydatasourceaggregatorname:",
    "canaggregateparticipantdashboardexamhistoryrows:",
    "canpopulateparticipantdashboardglobalexamoutcomecounts: false",
    "aggregateparticipantfullexamresultrows,",
)

for marker in required_markers:
    if marker not in lower:
        fail(f"Adapter-Marker fehlt: {marker}")

if text.count(
    "function getParticipantExamResultHistoryRpcState()"
) != 1:
    fail("RPC-State-Funktion muss genau einmal vorhanden sein.")

if text.count(
    "function listParticipantFullExamResults(options)"
) != 1:
    fail("Ergebnislisten-Funktion muss genau einmal vorhanden sein.")

if text.count(
    "function getParticipantDashboardExamHistoryDataSourceState()"
) != 1:
    fail(
        "Dashboard-Datenquellen-State muss genau einmal "
        "vorhanden sein."
    )

if text.count(
    "function normalizeParticipantFullExamResultRow(row)"
) != 1:
    fail("Ergebniszeilen-Normalizer muss genau einmal vorhanden sein.")

if text.count(
    "function normalizeParticipantFullExamResultRows(rows)"
) != 1:
    fail("Ergebnislisten-Normalizer muss genau einmal vorhanden sein.")

row_normalizer_start = lower.index(
    "function normalizeparticipantfullexamresultrow(row)"
)
row_normalizer_end = lower.index(
    "function normalizeparticipantfullexamresultrows(rows)",
    row_normalizer_start,
)
row_normalizer_block = lower[
    row_normalizer_start:row_normalizer_end
]

for forbidden in (
    "correct_answers",
    "selected_answers",
    "answer_options",
    "question_text",
    "explanation",
    "answer_hash",
    "participant_id",
    "service_role",
    "...row",
):
    if forbidden in row_normalizer_block:
        fail(
            "Unzulässiger oder privater Inhalt "
            f"im Ergebniszeilen-Normalizer: {forbidden}"
        )

rows_normalizer_start = lower.index(
    "function normalizeparticipantfullexamresultrows(rows)"
)
rows_normalizer_end = lower.index(
    "function normalizeparticipantexamresulthistorypagination(options)",
    rows_normalizer_start,
)
rows_normalizer_block = lower[
    rows_normalizer_start:rows_normalizer_end
]

for required in (
    "normalizeparticipantfullexamresultrow(rows[index])",
    "duplicate_exam_attempt_id",
    "total_count_inconsistent",
    "total_count_smaller_than_rows",
    "entries: []",
    "invalidindex: index",
):
    if required not in rows_normalizer_block:
        fail(
            "Listen-Normalizer-Anweisung fehlt: "
            f"{required}"
        )


if text.count(
    "function aggregateParticipantFullExamResultRows(rows)"
) != 1:
    fail(
        "Ergebnislisten-Aggregator muss genau einmal "
        "vorhanden sein."
    )

aggregator_start = lower.index(
    "function aggregateparticipantfullexamresultrows(rows)"
)
aggregator_end = lower.index(
    "function normalizeparticipantexamresulthistorypagination(options)",
    aggregator_start,
)
aggregator_block = lower[
    aggregator_start:aggregator_end
]

for required in (
    "normalizeparticipantfullexamresultrows(rows)",
    "pagepassedcount + pagefailedcount !==",
    "scorepoints > pagebestscore",
    "scoreSum / pageEntryCount".lower(),
    "pagepassedcount /",
    "metricsscope: "page_only"",
    "canpopulateglobaloutcomecounts: false",
    "globalpassedcount: null",
    "globalfailedcount: null",
):
    if required not in aggregator_block:
        fail(
            "Aggregator-Anweisung fehlt: "
            f"{required}"
        )

for forbidden in (
    "participant_id",
    "correct_answers",
    "selected_answers",
    "question_text",
    "explanation",
    "answer_hash",
    ".rpc(",
    "fetch(",
    "window.supabase",
    "service_role",
):
    if forbidden in aggregator_block:
        fail(
            "Unzulässiger Inhalt im Ergebnislisten-Aggregator: "
            f"{forbidden}"
        )


data_source_start = lower.index(
    "function getparticipantdashboardexamhistorydatasourcestate()"
)
data_source_end = lower.index(
    "function getparticipantdashboardexamhistorystate()",
    data_source_start,
)
data_source_block = lower[
    data_source_start:data_source_end
]

for forbidden in (
    ".rpc(",
    "listparticipantfullexamresults(",
    "createclient(",
    "window.supabase",
    "fetch(",
    "xmlhttprequest",
    "participant_id",
    "service_role",
):
    if forbidden in data_source_block:
        fail(
            "Unzulässiger Live- oder Identitätsinhalt "
            f"in Dashboard-Datenquelle: {forbidden}"
        )

start = lower.index(
    "function getparticipantexamresulthistoryrpcstate()"
)
end = lower.index(
    "function getparticipantdashboardcertificatehistorystate()",
    start,
)
rpc_block = lower[start:end]

for forbidden in (
    ".rpc(",
    "createclient(",
    "window.supabase",
    "fetch(",
    "xmlhttprequest",
    "p_participant_id",
    "participant_id",
    "service_role",
):
    if forbidden in rpc_block:
        fail(
            "Unzulässiger Live- oder Identitätsinhalt "
            f"im Ergebnislisten-Adapter: {forbidden}"
        )

print("Supabase-Ergebnislisten-Adapterprüfung: OK")
print("RPC-Name: accaoui_list_full_exam_results")
print("Pagination: Limit 1–50, Offset 0–10000")
print("Teilnehmer-ID als Browserparameter: nein")
print("Live-RPC-Aufruf: nein")
print("Dashboard-Datenquelle: vorbereitet und lokal gesperrt")
print("Ergebniszeilen-Normalizer: 120/60-, UUID- und Zeitprüfung")
print("Ergebnislisten-Normalizer: Duplikate und total_count geprüft")
print("Ergebnislisten-Aggregator: sichere Seitenkennzahlen")
print("Globale Bestanden-/Nicht-bestanden-Zahlen: bewusst nicht abgeleitet")
print("Private Prüfungsfelder in Normalizer: ausgeschlossen")
print("Sichtbare Prüfungshistorie: unverändert verborgen")
print("Lokaler Modus: sicher und nicht blockierend")
