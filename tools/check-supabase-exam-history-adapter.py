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
    "// stand: v27.29b",
    'version: "v27.29b"',
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
print("Lokaler Modus: sicher und nicht blockierend")
