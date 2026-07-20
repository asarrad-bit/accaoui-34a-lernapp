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
    "// stand: v27.29r",
    'version: "v27.29b"',
    'version: "v27.29c"',
    'version: "v27.29d"',
    'version: "v27.29e"',
    'version: "v27.29h"',
    'version: "v27.29i"',
    'version: "v27.29j"',
    'version: "v27.29k"',
    'version: "v27.29l"',
    'version: "v27.29m"',
    'version: "v27.29n"',
    'version: "v27.29o"',
    'version: "v27.29p"',
    'version: "v27.29q"',
    'version: "v27.29r"',
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
    "function mapparticipantfullexamresulthistoryresponse(response)",
    '"exam_result_history_response_error"',
    '"exam_result_history_response_invalid"',
    '"exam_result_history_response_empty"',
    '"exam_result_history_response_ready"',
    "ismapperonly: true",
    "responsemappername:",
    "isresponsemapperprepared: true",
    "canmapresponses: true",
    "datasourceresponsemappername:",
    "isdatasourceresponsemapperprepared:",
    "canmapdatasourceresponses:",
    "mapparticipantfullexamresulthistoryresponse,",
    "function mapparticipantfullexamresulthistoryloadstate(input)",
    '"exam_result_history_load_prepared"',
    '"exam_result_history_load_loading"',
    '"exam_result_history_load_success"',
    '"exam_result_history_load_empty"',
    '"exam_result_history_load_error"',
    "isloadstatemapperonly: true",
    "isloading: false",
    "issuccess: false",
    "haserror: false",
    "canretry: false",
    'loadstatemappername: "mapparticipantfullexamresulthistoryloadstate"',
    "isloadstatemapperprepared: true",
    "canmaploadstates: true",
    "datasourceloadstatemappername:",
    "isdatasourceloadstatemapperprepared:",
    "canmapdatasourceloadstates:",
    "datasourceinitialloadstate:",
    "mapparticipantfullexamresulthistoryloadstate,",
    "function mapparticipantfullexamresulthistorypaginationstate(input)",
    '"exam_result_history_pagination_prepared"',
    '"exam_result_history_pagination_empty"',
    '"exam_result_history_pagination_ready"',
    '"exam_result_history_pagination_invalid"',
    "ispaginationstatemapperonly: true",
    "currentpage:",
    "totalpages:",
    "cangoprevious:",
    "cangonext:",
    "previousoffset:",
    "nextoffset:",
    "istotalcountknown:",
    "isnavigationcapped:",
    'paginationstatemappername:',
    "ispaginationstatemapperprepared: true",
    "canmappaginationstates: true",
    "datasourcepaginationstatemappername:",
    "isdatasourcepaginationstatemapperprepared:",
    "canmapdatasourcepaginationstates:",
    "datasourceinitialpaginationstate:",
    "mapparticipantfullexamresulthistorypaginationstate,",
    "function orchestrateparticipantfullexamresulthistorydatasourcestate(input)",
    '"exam_result_history_data_source_prepared"',
    '"exam_result_history_data_source_loading"',
    '"exam_result_history_data_source_success"',
    '"exam_result_history_data_source_empty"',
    '"exam_result_history_data_source_error"',
    "isdatasourceorchestratoronly: true",
    "hasdata: false",
    "datasourceorchestratorname:",
    "isdatasourceorchestratorprepared: true",
    "canorchestratedatasourcestates: true",
    "datasourceinitialorchestratedstate:",
    "orchestrateparticipantfullexamresulthistorydatasourcestate,",
    "function mapparticipantfullexamresulthistorynavigationintent(input)",
    '"first"',
    '"previous"',
    '"next"',
    '"retry"',
    '"exam_result_history_navigation_intent_ready"',
    '"exam_result_history_navigation_intent_blocked"',
    '"exam_result_history_navigation_intent_invalid"',
    "isnavigationintentmapperonly: true",
    "cannavigate: false",
    "isretry: false",
    "issamerequest: false",
    "navigationintentmappername:",
    "isnavigationintentmapperprepared: true",
    "canmapnavigationintents: true",
    "datasourcenavigationintentmappername:",
    "isdatasourcenavigationintentmapperprepared:",
    "canmapdatasourcenavigationintents:",
    "datasourceinitialnavigationintentstate:",
    "mapparticipantfullexamresulthistorynavigationintent,",
    "function mapparticipantfullexamresulthistoryrequestidentity(input)",
    '"create"',
    '"compare"',
    '"exam_result_history_request_identity_ready"',
    '"exam_result_history_request_identity_invalid"',
    '"exam_result_history_response_identity_current"',
    '"exam_result_history_response_identity_stale"',
    "isrequestidentitymapperonly: true",
    "canapplyresponse: false",
    "iscurrentresponse: false",
    "isstaleresponse: false",
    "requestidentitymappername:",
    "isrequestidentitymapperprepared: true",
    "canmaprequestidentities: true",
    "datasourcerequestidentitymappername:",
    "isdatasourcerequestidentitymapperprepared:",
    "canmapdatasourcerequestidentities:",
    "datasourceinitialrequestidentitystate:",
    "mapparticipantfullexamresulthistoryrequestidentity,",
    "function guardparticipantfullexamresulthistoryresponseacceptance(input)",
    '"exam_result_history_response_acceptance_invalid"',
    '"exam_result_history_response_acceptance_stale_ignored"',
    '"exam_result_history_response_acceptance_accepted"',
    '"exam_result_history_response_acceptance_accepted_empty"',
    '"exam_result_history_response_acceptance_error"',
    "isresponseacceptanceguardonly: true",
    "canacceptresponse: false",
    "didacceptresponse: false",
    "shouldignoreresponse: false",
    "responseacceptanceguardname:",
    "isresponseacceptanceguardprepared: true",
    "canguardresponseacceptance: true",
    "datasourceresponseacceptanceguardname:",
    "isdatasourceresponseacceptanceguardprepared:",
    "canguarddatasourceresponseacceptance:",
    "datasourceinitialresponseacceptancestate:",
    "guardparticipantfullexamresulthistoryresponseacceptance,",
    "function mapparticipantfullexamresulthistoryrequestlifecycle(input)",
    '"exam_result_history_request_lifecycle_prepared"',
    '"exam_result_history_request_lifecycle_pending"',
    '"exam_result_history_request_lifecycle_completed"',
    '"exam_result_history_request_lifecycle_discarded"',
    '"exam_result_history_request_lifecycle_invalid"',
    "isrequestlifecyclemapperonly: true",
    "requestlifecyclemappername:",
    "isrequestlifecyclemapperprepared: true",
    "canmaprequestlifecycles: true",
    "datasourcerequestlifecyclemappername:",
    "isdatasourcerequestlifecyclemapperprepared:",
    "canmapdatasourcerequestlifecycles:",
    "datasourceinitialrequestlifecyclestate:",
    "mapparticipantfullexamresulthistoryrequestlifecycle,",
    "function guardparticipantfullexamresulthistoryrequestlifecycletransition(input)",
    '"exam_result_history_request_transition_ready"',
    '"exam_result_history_request_transition_blocked"',
    '"exam_result_history_request_transition_invalid"',
    "isrequestlifecycletransitionguardonly: true",
    "requestlifecycletransitionguardname:",
    "isrequestlifecycletransitionguardprepared: true",
    "canguardrequestlifecycletransitions: true",
    "datasourcerequestlifecycletransitionguardname:",
    "isdatasourcerequestlifecycletransitionguardprepared:",
    "canguarddatasourcerequestlifecycletransitions:",
    "datasourceinitialrequestlifecycletransitionstate:",
    "guardparticipantfullexamresulthistoryrequestlifecycletransition,",
    "function mapparticipantfullexamresulthistoryrequestcontrollerstate(input)",
    '"initialize"',
    '"start"',
    '"accept"',
    '"navigate"',
    '"discard"',
    '"exam_result_history_request_controller_prepared"',
    '"exam_result_history_request_controller_pending"',
    '"exam_result_history_request_controller_completed"',
    '"exam_result_history_request_controller_navigation_ready"',
    '"exam_result_history_request_controller_discarded"',
    '"exam_result_history_request_controller_stale_ignored"',
    '"exam_result_history_request_controller_blocked"',
    '"exam_result_history_request_controller_error"',
    '"exam_result_history_request_controller_invalid"',
    "isrequestcontrollermapperonly: true",
    "requestcontrollermappername:",
    "isrequestcontrollermapperprepared: true",
    "canmaprequestcontrollerstates: true",
    "datasourcerequestcontrollermappername:",
    "isdatasourcerequestcontrollermapperprepared:",
    "canmapdatasourcerequestcontrollerstates:",
    "datasourceinitialrequestcontrollerstate:",
    "mapparticipantfullexamresulthistoryrequestcontrollerstate,",
    "function normalizeparticipantfullexamresulthistorycontrollersnapshot(input)",
    '"exam_result_history_controller_snapshot_resumable"',
    '"exam_result_history_controller_snapshot_terminal"',
    '"exam_result_history_controller_snapshot_invalid"',
    "iscontrollersnapshotnormalizeronly: true",
    "controllersnapshotnormalizername:",
    "iscontrollersnapshotnormalizerprepared: true",
    "cannormalizecontrollersnapshots: true",
    "datasourcecontrollersnapshotnormalizername:",
    "isdatasourcecontrollersnapshotnormalizerprepared:",
    "cannormalizedatasourcecontrollersnapshots:",
    "datasourceinitialcontrollersnapshotstate:",
    "normalizeparticipantfullexamresulthistorycontrollersnapshot,",
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
    "return invalid(normalized.reason, index)",
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
    'metricsscope: "page_only"',
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


if text.count(
    "function mapParticipantFullExamResultHistoryResponse(response)"
) != 1:
    fail(
        "Ergebnislisten-Response-Mapper muss genau einmal "
        "vorhanden sein."
    )

mapper_start = lower.index(
    "function mapparticipantfullexamresulthistoryresponse(response)"
)
mapper_end = lower.index(
    "function normalizeparticipantexamresulthistorypagination(options)",
    mapper_start,
)
mapper_block = lower[
    mapper_start:mapper_end
]

for required in (
    "aggregateparticipantfullexamresultrows(",
    "response.data",
    "rpc_response_must_be_object",
    "rpc_response_error",
    "rpc_response_data_must_be_array",
    "exam_result_history_response_empty",
    "exam_result_history_response_ready",
    "results: aggregate.entries",
    "totalcount: aggregate.totalcount",
    "canpopulateglobaloutcomecounts: false",
    "globalpassedcount: null",
    "globalfailedcount: null",
):
    if required not in mapper_block:
        fail(
            "Response-Mapper-Anweisung fehlt: "
            f"{required}"
        )

for forbidden in (
    ".rpc(",
    "createclient(",
    "window.supabase",
    "fetch(",
    "xmlhttprequest",
    "participant_id",
    "service_role",
    "response.error.message",
    "response.error.details",
    "response.error.hint",
    "...response",
):
    if forbidden in mapper_block:
        fail(
            "Unzulässiger Inhalt im Response-Mapper: "
            f"{forbidden}"
        )


if text.count(
    "function mapParticipantFullExamResultHistoryLoadState(input)"
) != 1:
    fail(
        "Ergebnislisten-Ladezustands-Mapper muss genau einmal "
        "vorhanden sein."
    )

load_mapper_start = lower.index(
    "function mapparticipantfullexamresulthistoryloadstate(input)"
)
load_mapper_end = lower.index(
    "function normalizeparticipantexamresulthistorypagination(options)",
    load_mapper_start,
)
load_mapper_block = lower[
    load_mapper_start:load_mapper_end
]

for required in (
    'phase === "prepared"',
    'phase === "loading"',
    'phase === "resolved"',
    'phase === "rejected"',
    "mapparticipantfullexamresulthistoryresponse(",
    "exam_result_history_load_prepared",
    "exam_result_history_load_loading",
    "exam_result_history_load_success",
    "exam_result_history_load_empty",
    "exam_result_history_load_error",
    "rpc_request_failed",
    "load_phase_invalid",
    "isloadstatemapperonly: true",
    "islivecall: false",
    "results: mappedresponse.results",
    "totalcount: mappedresponse.totalcount",
    "pagemetrics: mappedresponse.pagemetrics",
):
    if required not in load_mapper_block:
        fail(
            "Ladezustands-Mapper-Anweisung fehlt: "
            f"{required}"
        )

for forbidden in (
    ".rpc(",
    "createclient(",
    "window.supabase",
    "fetch(",
    "xmlhttprequest",
    "participant_id",
    "service_role",
    "source.error.message",
    "source.error.details",
    "source.error.hint",
    "...source",
    "...input",
):
    if forbidden in load_mapper_block:
        fail(
            "Unzulässiger Inhalt im Ladezustands-Mapper: "
            f"{forbidden}"
        )


if text.count(
    "function mapParticipantFullExamResultHistoryPaginationState(input)"
) != 1:
    fail(
        "Pagination-Navigationsstate-Mapper muss genau einmal "
        "vorhanden sein."
    )

pagination_mapper_start = lower.index(
    "function mapparticipantfullexamresulthistorypaginationstate(input)"
)
pagination_mapper_end = lower.index(
    "function normalizeparticipantexamresulthistorypagination(options)",
    pagination_mapper_start,
)
pagination_mapper_block = lower[
    pagination_mapper_start:pagination_mapper_end
]

for required in (
    "normalizeparticipantexamresulthistorypagination({",
    "pagination.offset %",
    "pagination.limit !== 0",
    "number.isinteger(pageentrycount)",
    "number.issafeinteger(totalcount)",
    "math.ceil(",
    "totalcount / pagination.limit",
    "rawnextoffset > 10000",
    "offset_must_align_to_limit",
    "page_entry_count_invalid",
    "total_count_invalid",
    "offset_out_of_range_for_total_count",
    "maximum_offset_reached",
    "exam_result_history_pagination_prepared",
    "exam_result_history_pagination_empty",
    "exam_result_history_pagination_ready",
    "exam_result_history_pagination_invalid",
    "islivecall: false",
):
    if required not in pagination_mapper_block:
        fail(
            "Pagination-Navigationsstate-Anweisung fehlt: "
            f"{required}"
        )

for forbidden in (
    ".rpc(",
    "createclient(",
    "window.supabase",
    "fetch(",
    "xmlhttprequest",
    "participant_id",
    "service_role",
    "source.error",
    "...source",
    "...input",
):
    if forbidden in pagination_mapper_block:
        fail(
            "Unzulässiger Inhalt im Pagination-Navigationsstate: "
            f"{forbidden}"
        )


if text.count(
    "function orchestrateParticipantFullExamResultHistoryDataSourceState(input)"
) != 1:
    fail(
        "Datenquellen-Orchestrator muss genau einmal "
        "vorhanden sein."
    )

orchestrator_start = lower.index(
    "function orchestrateparticipantfullexamresulthistorydatasourcestate(input)"
)
orchestrator_end = lower.index(
    "function normalizeparticipantexamresulthistorypagination(options)",
    orchestrator_start,
)
orchestrator_block = lower[
    orchestrator_start:orchestrator_end
]

for required in (
    "mapparticipantfullexamresulthistorypaginationstate({",
    "mapparticipantfullexamresulthistoryloadstate({",
    "exam_result_history_data_source_prepared",
    "exam_result_history_data_source_loading",
    "exam_result_history_data_source_success",
    "exam_result_history_data_source_empty",
    "exam_result_history_data_source_error",
    "empty_page_after_nonzero_offset",
    "page_metrics_entry_count_invalid",
    "load_state_unhandled",
    "pageentrycount !==",
    "loadstate.results.length",
    "results: loadstate.results",
    "totalcount: loadstate.totalcount",
    "pagemetrics: loadstate.pagemetrics",
    "isdatasourceorchestratoronly: true",
    "islivecall: false",
    "isvisible: false",
    "canrender: false",
):
    if required not in orchestrator_block:
        fail(
            "Datenquellen-Orchestrator-Anweisung fehlt: "
            f"{required}"
        )

for forbidden in (
    ".rpc(",
    "createclient(",
    "window.supabase",
    "fetch(",
    "xmlhttprequest",
    "participant_id",
    "service_role",
    "source.error",
    "response.error.message",
    "response.error.details",
    "response.error.hint",
    "...source",
    "...input",
):
    if forbidden in orchestrator_block:
        fail(
            "Unzulässiger Inhalt im Datenquellen-Orchestrator: "
            f"{forbidden}"
        )


if text.count(
    "function mapParticipantFullExamResultHistoryNavigationIntent(input)"
) != 1:
    fail(
        "Navigations-Intent-Mapper muss genau einmal "
        "vorhanden sein."
    )

navigation_start = lower.index(
    "function mapparticipantfullexamresulthistorynavigationintent(input)"
)
navigation_end = lower.index(
    "function normalizeparticipantexamresulthistorypagination(options)",
    navigation_start,
)
navigation_block = lower[
    navigation_start:navigation_end
]

for required in (
    'allowedintents = [',
    '"first"',
    '"previous"',
    '"next"',
    '"retry"',
    "normalizeparticipantexamresulthistorypagination({",
    "navigation_intent_invalid",
    "current_state_must_be_object",
    "current_request_missing",
    "current_request_invalid",
    "navigation_target_invalid",
    "navigation_while_loading",
    "retry_not_available",
    "previous_page_unavailable",
    "next_page_unavailable",
    "pagination_state_invalid",
    "exam_result_history_navigation_intent_ready",
    "exam_result_history_navigation_intent_blocked",
    "exam_result_history_navigation_intent_invalid",
    "paginationstate.previousoffset",
    "paginationstate.nextoffset",
    "isnavigationintentmapperonly: true",
    "islivecall: false",
):
    if required not in navigation_block:
        fail(
            "Navigations-Intent-Anweisung fehlt: "
            f"{required}"
        )

for forbidden in (
    ".rpc(",
    "createclient(",
    "window.supabase",
    "fetch(",
    "xmlhttprequest",
    "participant_id",
    "service_role",
    "source.error",
    "currentstate.error",
    "...source",
    "...input",
):
    if forbidden in navigation_block:
        fail(
            "Unzulässiger Inhalt im Navigations-Intent-State: "
            f"{forbidden}"
        )


if text.count(
    "function mapParticipantFullExamResultHistoryRequestIdentity(input)"
) != 1:
    fail(
        "Anfrage-Identitätsstate-Mapper muss genau einmal "
        "vorhanden sein."
    )

identity_start = lower.index(
    "function mapparticipantfullexamresulthistoryrequestidentity(input)"
)
identity_end = lower.index(
    "function normalizeparticipantexamresulthistorypagination(options)",
    identity_start,
)
identity_block = lower[
    identity_start:identity_end
]

for required in (
    'allowedmodes = [',
    '"create"',
    '"compare"',
    "normalizeparticipantexamresulthistorypagination({",
    "number.issafeinteger(",
    "source.requestsequence < 1",
    "source.requestsequence > 1000000000",
    '"exam_history_request:"',
    "responseidentity === requestidentity",
    "request_identity_mode_invalid",
    "request_identity_request_missing",
    "request_identity_request_invalid",
    "request_sequence_invalid",
    "response_identity_format_invalid",
    "response_identity_sequence_invalid",
    "response_identity_request_invalid",
    "response_identity_noncanonical",
    "response_identity_does_not_match_active_request",
    "exam_result_history_request_identity_ready",
    "exam_result_history_request_identity_invalid",
    "exam_result_history_response_identity_current",
    "exam_result_history_response_identity_stale",
    "canapplyresponse: iscurrentresponse",
    "isrequestidentitymapperonly: true",
    "islivecall: false",
):
    if required not in identity_block:
        fail(
            "Anfrage-Identitätsstate-Anweisung fehlt: "
            f"{required}"
        )

for forbidden in (
    ".rpc(",
    "createclient(",
    "window.supabase",
    "fetch(",
    "xmlhttprequest",
    "participant_id",
    "service_role",
    "source.response.",
    "source.response[",
    "source.response &&",
    "source.response ||",
    "date.now(",
    "math.random(",
    "crypto.",
    "randomuuid",
    "...source",
    "...input",
):
    if forbidden in identity_block:
        fail(
            "Unzulässiger Inhalt im Anfrage-Identitätsstate: "
            f"{forbidden}"
        )


if text.count(
    "function guardParticipantFullExamResultHistoryResponseAcceptance(input)"
) != 1:
    fail(
        "Response-Annahme-Guard muss genau einmal "
        "vorhanden sein."
    )

guard_start = lower.index(
    "function guardparticipantfullexamresulthistoryresponseacceptance(input)"
)
guard_end = lower.index(
    "function mapparticipantfullexamresulthistoryrequestidentity(input)",
    guard_start,
)
guard_block = lower[
    guard_start:guard_end
]

for required in (
    "mapparticipantfullexamresulthistoryrequestidentity({",
    'mode: "compare"',
    "orchestrateparticipantfullexamresulthistorydatasourcestate({",
    'phase: "resolved"',
    "response: source.response",
    "identitystate.isstaleresponse",
    "identitystate.canapplyresponse !== true",
    "identitystate.iscurrentresponse !== true",
    "datasourcestate.haserror",
    "datasourcestate.isempty",
    "datasourcestate.issuccess",
    "datasourcestate.hasdata",
    "stale_response_ignored",
    "response_identity_not_applicable",
    "data_source_state_not_acceptable",
    "exam_result_history_response_acceptance_invalid",
    "exam_result_history_response_acceptance_stale_ignored",
    "exam_result_history_response_acceptance_accepted",
    "exam_result_history_response_acceptance_accepted_empty",
    "exam_result_history_response_acceptance_error",
    "isresponseacceptanceguardonly: true",
    "islivecall: false",
    "canacceptresponse: true",
    "didacceptresponse: true",
):
    if required not in guard_block:
        fail(
            "Response-Annahme-Guard-Anweisung fehlt: "
            f"{required}"
        )

stale_position = guard_block.index(
    "if (identitystate.isstaleresponse)"
)
response_read_position = guard_block.index(
    "response: source.response"
)

if stale_position > response_read_position:
    fail(
        "Veraltete Antwort wird vor der Sperrprüfung gelesen."
    )

for forbidden in (
    ".rpc(",
    "createclient(",
    "window.supabase",
    "fetch(",
    "xmlhttprequest",
    "participant_id",
    "service_role",
    "source.response.error",
    "source.response.message",
    "source.response.details",
    "source.response.hint",
    "response.error.message",
    "response.error.details",
    "response.error.hint",
    "...source",
    "...input",
    "...response",
):
    if forbidden in guard_block:
        fail(
            "Unzulässiger Inhalt im Response-Annahme-Guard: "
            f"{forbidden}"
        )


if text.count(
    "function mapParticipantFullExamResultHistoryRequestLifecycle(input)"
) != 1:
    fail(
        "Anfrage-Lebenszyklus-Mapper muss genau einmal "
        "vorhanden sein."
    )

lifecycle_start = lower.index(
    "function mapparticipantfullexamresulthistoryrequestlifecycle(input)"
)
lifecycle_end = lower.index(
    "function guardparticipantfullexamresulthistoryresponseacceptance(input)",
    lifecycle_start,
)
lifecycle_block = lower[
    lifecycle_start:lifecycle_end
]

for required in (
    'allowedphases = [',
    '"prepared"',
    '"pending"',
    '"completed"',
    '"discarded"',
    "mapparticipantfullexamresulthistoryrequestidentity({",
    'mode: "create"',
    "alloweddiscardreasons = [",
    "cancelled_before_response",
    "superseded_by_new_request",
    "stale_response_ignored",
    "acceptancestate.didacceptresponse !== true",
    "acceptancestate.canacceptresponse !== true",
    "acceptancestate.requestidentity !==",
    "identitystate.requestidentity",
    "request_lifecycle_phase_invalid",
    "request_lifecycle_discard_reason_invalid",
    "request_lifecycle_acceptance_state_missing",
    "request_lifecycle_acceptance_state_invalid",
    "request_lifecycle_acceptance_identity_mismatch",
    "request_lifecycle_acceptance_status_invalid",
    "request_lifecycle_total_count_invalid",
    "exam_result_history_request_lifecycle_prepared",
    "exam_result_history_request_lifecycle_pending",
    "exam_result_history_request_lifecycle_completed",
    "exam_result_history_request_lifecycle_discarded",
    "exam_result_history_request_lifecycle_invalid",
    "isrequestlifecyclemapperonly: true",
    "islivecall: false",
):
    if required not in lifecycle_block:
        fail(
            "Anfrage-Lebenszyklus-Anweisung fehlt: "
            f"{required}"
        )

for forbidden in (
    ".rpc(",
    "createclient(",
    "window.supabase",
    "fetch(",
    "xmlhttprequest",
    "participant_id",
    "service_role",
    "source.response",
    "date.now(",
    "math.random(",
    "crypto.",
    "...source",
    "...input",
):
    if forbidden in lifecycle_block:
        fail(
            "Unzulässiger Inhalt im Anfrage-Lebenszyklus: "
            f"{forbidden}"
        )


if text.count(
    "function guardParticipantFullExamResultHistoryRequestLifecycleTransition(input)"
) != 1:
    fail(
        "Lebenszyklus-Übergangs-Guard muss genau einmal "
        "vorhanden sein."
    )

transition_start = lower.index(
    "function guardparticipantfullexamresulthistoryrequestlifecycletransition(input)"
)
transition_end = lower.index(
    "function mapparticipantfullexamresulthistoryrequestlifecycle(input)",
    transition_start,
)
transition_block = lower[
    transition_start:transition_end
]

for required in (
    "mapparticipantfullexamresulthistoryrequestidentity({",
    'mode: "create"',
    "mapparticipantfullexamresulthistoryrequestlifecycle(",
    "allowedtransitions = {",
    'prepared: [',
    '"pending"',
    '"completed"',
    '"discarded"',
    "request_transition_current_state_missing",
    "request_transition_current_state_invalid",
    "request_transition_current_identity_invalid",
    "request_transition_phase_invalid",
    "request_transition_current_flags_invalid",
    "request_transition_terminal_state",
    "request_transition_not_allowed",
    "request_transition_next_identity_mismatch",
    "exam_result_history_request_transition_ready",
    "exam_result_history_request_transition_blocked",
    "exam_result_history_request_transition_invalid",
    "isrequestlifecycletransitionguardonly: true",
    "islivecall: false",
    "cantransition: true",
    "didtransition: true",
):
    if required not in transition_block:
        fail(
            "Lebenszyklus-Übergangs-Anweisung fehlt: "
            f"{required}"
        )

for forbidden in (
    ".rpc(",
    "createclient(",
    "window.supabase",
    "fetch(",
    "xmlhttprequest",
    "participant_id",
    "service_role",
    "source.response",
    "date.now(",
    "math.random(",
    "crypto.",
    "...source",
    "...input",
):
    if forbidden in transition_block:
        fail(
            "Unzulässiger Inhalt im Lebenszyklus-Übergangs-Guard: "
            f"{forbidden}"
        )


if text.count(
    "function mapParticipantFullExamResultHistoryRequestControllerState(input)"
) != 1:
    fail(
        "Anfrage-Controller-State muss genau einmal "
        "vorhanden sein."
    )

controller_start = lower.index(
    "function mapparticipantfullexamresulthistoryrequestcontrollerstate(input)"
)
controller_end = lower.index(
    "function guardparticipantfullexamresulthistoryrequestlifecycletransition(input)",
    controller_start,
)
controller_block = lower[
    controller_start:controller_end
]

for required in (
    'allowedactions = [',
    '"initialize"',
    '"start"',
    '"accept"',
    '"navigate"',
    '"discard"',
    "mapparticipantfullexamresulthistoryrequestlifecycle({",
    "mapparticipantfullexamresulthistoryrequestidentity({",
    "guardparticipantfullexamresulthistoryrequestlifecycletransition({",
    "guardparticipantfullexamresulthistoryresponseacceptance(",
    "mapparticipantfullexamresulthistorynavigationintent({",
    "object.defineproperty(",
    '"response"',
    "request_controller_action_invalid",
    "request_controller_lifecycle_state_missing",
    "request_controller_lifecycle_state_invalid",
    "request_controller_lifecycle_identity_invalid",
    "request_controller_accept_requires_pending",
    "request_controller_navigation_requires_completed",
    "request_controller_data_source_request_mismatch",
    "request_controller_next_request_sequence_invalid",
    "exam_result_history_request_controller_prepared",
    "exam_result_history_request_controller_pending",
    "exam_result_history_request_controller_completed",
    "exam_result_history_request_controller_navigation_ready",
    "exam_result_history_request_controller_discarded",
    "exam_result_history_request_controller_stale_ignored",
    "exam_result_history_request_controller_blocked",
    "exam_result_history_request_controller_error",
    "exam_result_history_request_controller_invalid",
    "isrequestcontrollermapperonly: true",
    "islivecall: false",
):
    if required not in controller_block:
        fail(
            "Anfrage-Controller-Anweisung fehlt: "
            f"{required}"
        )

for forbidden in (
    ".rpc(",
    "createclient(",
    "window.supabase",
    "fetch(",
    "xmlhttprequest",
    "participant_id",
    "service_role",
    "source.response.error",
    "source.response.message",
    "source.response.details",
    "source.response.hint",
    "date.now(",
    "math.random(",
    "crypto.",
    "...source",
    "...input",
):
    if forbidden in controller_block:
        fail(
            "Unzulässiger Inhalt im Anfrage-Controller: "
            f"{forbidden}"
        )


if text.count(
    "function normalizeParticipantFullExamResultHistoryControllerSnapshot(input)"
) != 1:
    fail(
        "Controller-Snapshot-Normalizer muss genau einmal "
        "vorhanden sein."
    )

snapshot_start = lower.index(
    "function normalizeparticipantfullexamresulthistorycontrollersnapshot(input)"
)
snapshot_end = lower.index(
    "function mapparticipantfullexamresulthistoryrequestcontrollerstate(input)",
    snapshot_start,
)
snapshot_block = lower[
    snapshot_start:snapshot_end
]

for required in (
    "source.snapshotversion !== 1",
    "mapparticipantfullexamresulthistoryrequestidentity({",
    'mode: "create"',
    "mapparticipantfullexamresulthistoryrequestlifecycle(",
    "mapparticipantfullexamresulthistorypaginationstate({",
    "normalizeparticipantexamresulthistorypagination({",
    "controller_snapshot_version_invalid",
    "controller_snapshot_state_missing",
    "controller_snapshot_state_invalid",
    "controller_snapshot_status_not_resumable",
    "controller_snapshot_identity_invalid",
    "controller_snapshot_lifecycle_invalid",
    "controller_snapshot_flags_invalid",
    "controller_snapshot_completion_invalid",
    "controller_snapshot_total_count_invalid",
    "controller_snapshot_pagination_mismatch",
    "controller_snapshot_navigation_invalid",
    "controller_snapshot_previous_identity_invalid",
    "controller_snapshot_lifecycle_mismatch",
    "controller_snapshot_completion_mismatch",
    "exam_result_history_controller_snapshot_resumable",
    "exam_result_history_controller_snapshot_terminal",
    "exam_result_history_controller_snapshot_invalid",
    "retrypendingrequest".replace("pending", "_pending_"),
    "start_prepared_request",
    "iscontrollersnapshotnormalizeronly: true",
    "islivecall: false",
):
    if required not in snapshot_block:
        fail(
            "Controller-Snapshot-Anweisung fehlt: "
            f"{required}"
        )

for forbidden in (
    ".rpc(",
    "createclient(",
    "window.supabase",
    "fetch(",
    "xmlhttprequest",
    "participant_id",
    "service_role",
    "source.response",
    "date.now(",
    "math.random(",
    "crypto.",
    "...source",
    "...input",
    "controllerstate,",
):
    if forbidden in snapshot_block:
        fail(
            "Unzulässiger Inhalt im Controller-Snapshot: "
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
print("Response-Mapper: Erfolg, leer, ungültig und Fehler sicher getrennt")
print("Ladezustands-Mapper: vorbereitet, lädt, Erfolg, leer und Fehler")
print("Pagination-Navigationsstate: erste, mittlere, letzte und unbekannte Seite")
print("Datenquellen-Orchestrator: Ladezustand, Response und Pagination sicher verbunden")
print("Navigations-Intent-State: erste, vorherige, nächste und Retry-Anfrage")
print("Anfrage-Identitätsstate: aktuelle und veraltete Antworten getrennt")
print("Response-Annahme-Guard: nur aktive Anfrageantworten werden verarbeitet")
print("Anfrage-Lebenszyklus: vorbereitet, ausstehend, abgeschlossen und verworfen")
print("Lebenszyklus-Übergangs-Guard: nur zulässige Zustandswechsel")
print("Anfrage-Controller: Navigation, Identität, Lebenszyklus und Annahme verbunden")
print("Controller-Snapshot: gespeicherte Zustände sicher normalisiert")
print("Rohe RPC-Fehlerdetails: werden nicht übernommen")
print("Globale Bestanden-/Nicht-bestanden-Zahlen: bewusst nicht abgeleitet")
print("Private Prüfungsfelder in Normalizer: ausgeschlossen")
print("Sichtbare Prüfungshistorie: unverändert verborgen")
print("Lokaler Modus: sicher und nicht blockierend")
