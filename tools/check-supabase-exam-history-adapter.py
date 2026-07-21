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
    "// stand: v27.30q",
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
    'version: "v27.29s"',
    'version: "v27.29t"',
    'version: "v27.29u"',
    'version: "v27.29v"',
    'version: "v27.29w"',
    'version: "v27.29x"',
    'version: "v27.29y"',
    'version: "v27.29z"',
    'version: "v27.30a"',
    'version: "v27.30b"',
    'version: "v27.30c"',
    'version: "v27.30d"',
    'version: "v27.30e"',
    'version: "v27.30f"',
    'version: "v27.30g"',
    'version: "v27.30h"',
    'version: "v27.30i"',
    'version: "v27.30j"',
    'version: "v27.30k"',
    'version: "v27.30l"',
    'version: "v27.30m"',
    'version: "v27.30n"',
    'version: "v27.30o"',
    'version: "v27.30p"',
    'version: "v27.30q"',
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
    "function mapparticipantfullexamresulthistorysnapshotresumestate(input)",
    '"exam_result_history_snapshot_resume_prepared"',
    '"exam_result_history_snapshot_resume_pending_retry"',
    '"exam_result_history_snapshot_resume_navigation_prepared"',
    '"exam_result_history_snapshot_resume_terminal_blocked"',
    '"exam_result_history_snapshot_resume_invalid"',
    "issnapshotresumemapperonly: true",
    "snapshotresumemappername:",
    "issnapshotresumemapperprepared: true",
    "canmapsnapshotresumestates: true",
    "datasourcesnapshotresumemappername:",
    "isdatasourcesnapshotresumemapperprepared:",
    "canmapdatasourcesnapshotresumestates:",
    "datasourceinitialsnapshotresumestate:",
    "mapparticipantfullexamresulthistorysnapshotresumestate,",
    "function mapparticipantfullexamresulthistorysnapshotcreationstate(input)",
    '"exam_result_history_snapshot_creation_ready"',
    '"exam_result_history_snapshot_creation_blocked"',
    '"exam_result_history_snapshot_creation_invalid"',
    "issnapshotcreationmapperonly: true",
    "snapshotcreationmappername:",
    "issnapshotcreationmapperprepared: true",
    "canmapsnapshotcreationstates: true",
    "datasourcesnapshotcreationmappername:",
    "isdatasourcesnapshotcreationmapperprepared:",
    "canmapdatasourcesnapshotcreationstates:",
    "datasourceinitialsnapshotcreationstate:",
    "mapparticipantfullexamresulthistorysnapshotcreationstate,",
    "function mapparticipantfullexamresulthistorysnapshotserializationstate(input)",
    '"exam_result_history_snapshot_serialization_ready"',
    '"exam_result_history_snapshot_serialization_blocked"',
    '"exam_result_history_snapshot_serialization_too_large"',
    '"exam_result_history_snapshot_serialization_invalid"',
    "issnapshotserializationmapperonly: true",
    "snapshotserializationmappername:",
    "issnapshotserializationmapperprepared: true",
    "canmapsnapshotserializationstates: true",
    "datasourcesnapshotserializationmappername:",
    "isdatasourcesnapshotserializationmapperprepared:",
    "canmapdatasourcesnapshotserializationstates:",
    "datasourceinitialsnapshotserializationstate:",
    "mapparticipantfullexamresulthistorysnapshotserializationstate,",
    "function mapparticipantfullexamresulthistorysnapshotdeserializationstate(input)",
    '"exam_result_history_snapshot_deserialization_ready"',
    '"exam_result_history_snapshot_deserialization_too_large"',
    '"exam_result_history_snapshot_deserialization_invalid"',
    "issnapshotdeserializationmapperonly: true",
    "snapshotdeserializationmappername:",
    "issnapshotdeserializationmapperprepared: true",
    "canmapsnapshotdeserializationstates: true",
    "datasourcesnapshotdeserializationmappername:",
    "isdatasourcesnapshotdeserializationmapperprepared:",
    "canmapdatasourcesnapshotdeserializationstates:",
    "datasourceinitialsnapshotdeserializationstate:",
    "mapparticipantfullexamresulthistorysnapshotdeserializationstate,",
    "function mapparticipantfullexamresulthistorysnapshotpersistencecontract(input)",
    '"exam_result_history_snapshot_persistence_save_ready"',
    '"exam_result_history_snapshot_persistence_load_ready"',
    '"exam_result_history_snapshot_persistence_delete_ready"',
    '"exam_result_history_snapshot_persistence_save_blocked"',
    '"exam_result_history_snapshot_persistence_load_blocked"',
    '"exam_result_history_snapshot_persistence_invalid"',
    "issnapshotpersistencecontractonly: true",
    "snapshotpersistencecontractname:",
    "issnapshotpersistencecontractprepared: true",
    "canmapsnapshotpersistenceintents: true",
    "datasourcesnapshotpersistencecontractname:",
    "isdatasourcesnapshotpersistencecontractprepared:",
    "canmapdatasourcesnapshotpersistenceintents:",
    "datasourceinitialsnapshotpersistencestate:",
    "mapparticipantfullexamresulthistorysnapshotpersistencecontract,",
    "function mapparticipantfullexamresulthistorysnapshotstorageadapterreadiness(input)",
    '"exam_result_history_storage_adapter_readiness_ready"',
    '"exam_result_history_storage_adapter_readiness_partial"',
    '"exam_result_history_storage_adapter_readiness_unavailable"',
    '"exam_result_history_storage_adapter_readiness_invalid"',
    "issnapshotstorageadapterreadinessonly: true",
    "snapshotstorageadapterreadinessmappername:",
    "issnapshotstorageadapterreadinessprepared: true",
    "caninspectsnapshotstorageadapters: true",
    "datasourcesnapshotstorageadapterreadinessmappername:",
    "isdatasourcesnapshotstorageadapterreadinessprepared:",
    "caninspectdatasourcesnapshotstorageadapters:",
    "datasourceinitialsnapshotstorageadapterreadinessstate:",
    "mapparticipantfullexamresulthistorysnapshotstorageadapterreadiness,",
    "function mapparticipantfullexamresulthistorysnapshotpersistenceoperationplan(input)",
    '"exam_result_history_persistence_operation_plan_ready"',
    '"exam_result_history_persistence_operation_plan_blocked"',
    '"exam_result_history_persistence_operation_plan_invalid"',
    "issnapshotpersistenceoperationplanonly: true",
    "snapshotpersistenceoperationplanmappername:",
    "issnapshotpersistenceoperationplanprepared: true",
    "canmapsnapshotpersistenceoperationplans: true",
    "datasourcesnapshotpersistenceoperationplanmappername:",
    "isdatasourcesnapshotpersistenceoperationplanprepared:",
    "canmapdatasourcesnapshotpersistenceoperationplans:",
    "datasourceinitialsnapshotpersistenceoperationplanstate:",
    "mapparticipantfullexamresulthistorysnapshotpersistenceoperationplan,",
    "function mapparticipantfullexamresulthistorysnapshotpersistenceoperationreleasestate(input)",
    '"exam_result_history_persistence_operation_release_ready"',
    '"exam_result_history_persistence_operation_release_blocked"',
    '"exam_result_history_persistence_operation_release_invalid"',
    "issnapshotpersistenceoperationreleaseonly: true",
    "snapshotpersistenceoperationreleasemappername:",
    "issnapshotpersistenceoperationreleaseprepared: true",
    "canmapsnapshotpersistenceoperationreleases: true",
    "datasourcesnapshotpersistenceoperationreleasemappername:",
    "isdatasourcesnapshotpersistenceoperationreleaseprepared:",
    "canmapdatasourcesnapshotpersistenceoperationreleases:",
    "datasourceinitialsnapshotpersistenceoperationreleasestate:",
    "mapparticipantfullexamresulthistorysnapshotpersistenceoperationreleasestate,",
    "function guardparticipantfullexamresulthistorysnapshotpersistenceexecution(input)",
    '"exam_result_history_persistence_execution_guard_ready"',
    '"exam_result_history_persistence_execution_guard_invalid"',
    "issnapshotpersistenceexecutionguardonly: true",
    "snapshotpersistenceexecutionguardname:",
    "issnapshotpersistenceexecutionguardprepared: true",
    "canguardsnapshotpersistenceexecutions: true",
    "datasourcesnapshotpersistenceexecutionguardname:",
    "isdatasourcesnapshotpersistenceexecutionguardprepared:",
    "canguarddatasourcesnapshotpersistenceexecutions:",
    "datasourceinitialsnapshotpersistenceexecutionstate:",
    "guardparticipantfullexamresulthistorysnapshotpersistenceexecution,",
    "function mapparticipantfullexamresulthistorysnapshotpersistenceinvocationcontract(input)",
    '"exam_result_history_persistence_invocation_contract_ready"',
    '"exam_result_history_persistence_invocation_contract_invalid"',
    "issnapshotpersistenceinvocationcontractonly: true",
    "snapshotpersistenceinvocationcontractname:",
    "issnapshotpersistenceinvocationcontractprepared: true",
    "canmapsnapshotpersistenceinvocationcontracts: true",
    "datasourcesnapshotpersistenceinvocationcontractname:",
    "isdatasourcesnapshotpersistenceinvocationcontractprepared:",
    "canmapdatasourcesnapshotpersistenceinvocationcontracts:",
    "datasourceinitialsnapshotpersistenceinvocationcontractstate:",
    "mapparticipantfullexamresulthistorysnapshotpersistenceinvocationcontract,",
    "function mapparticipantfullexamresulthistorysnapshotpersistenceinvocationpackagestate(input)",
    '"exam_result_history_persistence_invocation_package_ready"',
    '"exam_result_history_persistence_invocation_package_invalid"',
    "issnapshotpersistenceinvocationpackageonly: true",
    "snapshotpersistenceinvocationpackagemappername:",
    "issnapshotpersistenceinvocationpackageprepared: true",
    "canmapsnapshotpersistenceinvocationpackages: true",
    "datasourcesnapshotpersistenceinvocationpackagemappername:",
    "isdatasourcesnapshotpersistenceinvocationpackageprepared:",
    "canmapdatasourcesnapshotpersistenceinvocationpackages:",
    "datasourceinitialsnapshotpersistenceinvocationpackagestate:",
    "mapparticipantfullexamresulthistorysnapshotpersistenceinvocationpackagestate,",
    "function mapparticipantfullexamresulthistorysnapshotpersistenceresultcontract(input)",
    '"exam_result_history_persistence_result_read_ready"',
    '"exam_result_history_persistence_result_read_empty"',
    '"exam_result_history_persistence_result_write_confirmed"',
    '"exam_result_history_persistence_result_delete_confirmed"',
    '"exam_result_history_persistence_result_delete_absent"',
    '"exam_result_history_persistence_result_contract_invalid"',
    "issnapshotpersistenceresultcontractonly: true",
    "snapshotpersistenceresultcontractname:",
    "issnapshotpersistenceresultcontractprepared: true",
    "canmapsnapshotpersistenceresults: true",
    "datasourcesnapshotpersistenceresultcontractname:",
    "isdatasourcesnapshotpersistenceresultcontractprepared:",
    "canmapdatasourcesnapshotpersistenceresults:",
    "datasourceinitialsnapshotpersistenceresultstate:",
    "mapparticipantfullexamresulthistorysnapshotpersistenceresultcontract,",
    "function guardparticipantfullexamresulthistorysnapshotpersistenceresultacceptance(input)",
    '"exam_result_history_persistence_result_acceptance_ready"',
    '"exam_result_history_persistence_result_acceptance_stale_ignored"',
    '"exam_result_history_persistence_result_acceptance_invalid"',
    "issnapshotpersistenceresultacceptanceguardonly: true",
    "snapshotpersistenceresultacceptanceguardname:",
    "issnapshotpersistenceresultacceptanceguardprepared: true",
    "canguardsnapshotpersistenceresultacceptance: true",
    "datasourcesnapshotpersistenceresultacceptanceguardname:",
    "isdatasourcesnapshotpersistenceresultacceptanceguardprepared:",
    "canguarddatasourcesnapshotpersistenceresultacceptance:",
    "datasourceinitialsnapshotpersistenceresultacceptancestate:",
    "guardparticipantfullexamresulthistorysnapshotpersistenceresultacceptance,",
    "function mapparticipantfullexamresulthistorysnapshotpersistencecompletionstate(input)",
    '"exam_result_history_persistence_completion_read_ready"',
    '"exam_result_history_persistence_completion_read_empty"',
    '"exam_result_history_persistence_completion_write_confirmed"',
    '"exam_result_history_persistence_completion_delete_confirmed"',
    '"exam_result_history_persistence_completion_delete_absent"',
    '"exam_result_history_persistence_completion_invalid"',
    "issnapshotpersistencecompletionmapperonly: true",
    "snapshotpersistencecompletionmappername:",
    "issnapshotpersistencecompletionmapperprepared: true",
    "canmapsnapshotpersistencecompletionstates: true",
    "datasourcesnapshotpersistencecompletionmappername:",
    "isdatasourcesnapshotpersistencecompletionmapperprepared:",
    "canmapdatasourcesnapshotpersistencecompletionstates:",
    "datasourceinitialsnapshotpersistencecompletionstate:",
    "mapparticipantfullexamresulthistorysnapshotpersistencecompletionstate,",
    "function mapparticipantfullexamresulthistorysnapshotpersistencecyclestate(input)",
    '"exam_result_history_persistence_cycle_completed"',
    '"exam_result_history_persistence_cycle_invalid"',
    "issnapshotpersistencecyclemapperonly: true",
    "snapshotpersistencecyclemappername:",
    "issnapshotpersistencecyclemapperprepared: true",
    "canmapsnapshotpersistencecyclestates: true",
    "datasourcesnapshotpersistencecyclemappername:",
    "isdatasourcesnapshotpersistencecyclemapperprepared:",
    "canmapdatasourcesnapshotpersistencecyclestates:",
    "datasourceinitialsnapshotpersistencecyclestate:",
    "mapparticipantfullexamresulthistorysnapshotpersistencecyclestate,",
    "function guardparticipantfullexamresulthistorysnapshotpersistencecyclerepetition(input)",
    '"exam_result_history_persistence_cycle_repetition_ready"',
    '"exam_result_history_persistence_cycle_repetition_blocked"',
    '"exam_result_history_persistence_cycle_repetition_invalid"',
    "issnapshotpersistencecyclerepetitionguardonly: true",
    "snapshotpersistencecyclerepetitionguardname:",
    "issnapshotpersistencecyclerepetitionguardprepared: true",
    "canguardsnapshotpersistencecyclerepetitions: true",
    "datasourcesnapshotpersistencecyclerepetitionguardname:",
    "isdatasourcesnapshotpersistencecyclerepetitionguardprepared:",
    "canguarddatasourcesnapshotpersistencecyclerepetitions:",
    "datasourceinitialsnapshotpersistencecyclerepetitionstate:",
    "guardparticipantfullexamresulthistorysnapshotpersistencecyclerepetition,",
    "function mapparticipantfullexamresulthistorysnapshotpersistencecycleregistrystate(input)",
    '"exam_result_history_persistence_cycle_registry_empty"',
    '"exam_result_history_persistence_cycle_registry_ready"',
    '"exam_result_history_persistence_cycle_registry_updated"',
    '"exam_result_history_persistence_cycle_registry_duplicate_unchanged"',
    '"exam_result_history_persistence_cycle_registry_invalid"',
    "issnapshotpersistencecycleregistrymapperonly: true",
    "snapshotpersistencecycleregistrymappername:",
    "issnapshotpersistencecycleregistrymapperprepared: true",
    "canmapsnapshotpersistencecycleregistrystates: true",
    "datasourcesnapshotpersistencecycleregistrymappername:",
    "isdatasourcesnapshotpersistencecycleregistrymapperprepared:",
    "canmapdatasourcesnapshotpersistencecycleregistrystates:",
    "datasourceinitialsnapshotpersistencecycleregistrystate:",
    "mapparticipantfullexamresulthistorysnapshotpersistencecycleregistrystate,",
    "function mapparticipantfullexamresulthistorysnapshotpersistencecycleregistryserializationstate(input)",
    '"exam_result_history_persistence_cycle_registry_serialization_ready"',
    '"exam_result_history_persistence_cycle_registry_serialization_invalid"',
    "issnapshotpersistencecycleregistryserializationmapperonly: true",
    "snapshotpersistencecycleregistryserializationmappername:",
    "issnapshotpersistencecycleregistryserializationmapperprepared: true",
    "canmapsnapshotpersistencecycleregistryserializationstates: true",
    "datasourcesnapshotpersistencecycleregistryserializationmappername:",
    "isdatasourcesnapshotpersistencecycleregistryserializationmapperprepared:",
    "canmapdatasourcesnapshotpersistencecycleregistryserializationstates:",
    "datasourceinitialsnapshotpersistencecycleregistryserializationstate:",
    "mapparticipantfullexamresulthistorysnapshotpersistencecycleregistryserializationstate,",
    "function mapparticipantfullexamresulthistorysnapshotpersistencecycleregistrydeserializationstate(input)",
    '"exam_result_history_persistence_cycle_registry_deserialization_ready"',
    '"exam_result_history_persistence_cycle_registry_deserialization_invalid"',
    "issnapshotpersistencecycleregistrydeserializationmapperonly: true",
    "snapshotpersistencecycleregistrydeserializationmappername:",
    "issnapshotpersistencecycleregistrydeserializationmapperprepared: true",
    "canmapsnapshotpersistencecycleregistrydeserializationstates: true",
    "datasourcesnapshotpersistencecycleregistrydeserializationmappername:",
    "isdatasourcesnapshotpersistencecycleregistrydeserializationmapperprepared:",
    "canmapdatasourcesnapshotpersistencecycleregistrydeserializationstates:",
    "datasourceinitialsnapshotpersistencecycleregistrydeserializationstate:",
    "mapparticipantfullexamresulthistorysnapshotpersistencecycleregistrydeserializationstate,",
    "function mapparticipantfullexamresulthistorysnapshotpersistencecycleregistrycontract(input)",
    '"exam_result_history_persistence_cycle_registry_contract_save_ready"',
    '"exam_result_history_persistence_cycle_registry_contract_load_ready"',
    '"exam_result_history_persistence_cycle_registry_contract_delete_ready"',
    '"exam_result_history_persistence_cycle_registry_contract_invalid"',
    "issnapshotpersistencecycleregistrycontractonly: true",
    "snapshotpersistencecycleregistrycontractname:",
    "issnapshotpersistencecycleregistrycontractprepared: true",
    "canmapsnapshotpersistencecycleregistryintents: true",
    "datasourcesnapshotpersistencecycleregistrycontractname:",
    "isdatasourcesnapshotpersistencecycleregistrycontractprepared:",
    "canmapdatasourcesnapshotpersistencecycleregistryintents:",
    "datasourceinitialsnapshotpersistencecycleregistrycontractstate:",
    "mapparticipantfullexamresulthistorysnapshotpersistencecycleregistrycontract,",
    "function mapparticipantfullexamresulthistorysnapshotpersistencecycleregistrystorageadapterreadinessstate(input)",
    '"exam_result_history_persistence_cycle_registry_storage_adapter_ready"',
    '"exam_result_history_persistence_cycle_registry_storage_adapter_partial"',
    '"exam_result_history_persistence_cycle_registry_storage_adapter_unavailable"',
    '"exam_result_history_persistence_cycle_registry_storage_adapter_invalid"',
    "issnapshotpersistencecycleregistrystorageadapterreadinessmapperonly: true",
    "snapshotpersistencecycleregistrystorageadapterreadinessmappername:",
    "issnapshotpersistencecycleregistrystorageadapterreadinessmapperprepared: true",
    "canmapsnapshotpersistencecycleregistrystorageadapterreadinessstates: true",
    "datasourcesnapshotpersistencecycleregistrystorageadapterreadinessmappername:",
    "isdatasourcesnapshotpersistencecycleregistrystorageadapterreadinessmapperprepared:",
    "canmapdatasourcesnapshotpersistencecycleregistrystorageadapterreadinessstates:",
    "datasourceinitialsnapshotpersistencecycleregistrystorageadapterreadinessstate:",
    "mapparticipantfullexamresulthistorysnapshotpersistencecycleregistrystorageadapterreadinessstate,",
    "function mapparticipantfullexamresulthistorysnapshotpersistencecycleregistryoperationplanstate(input)",
    '"exam_result_history_persistence_cycle_registry_operation_plan_ready"',
    '"exam_result_history_persistence_cycle_registry_operation_plan_blocked"',
    '"exam_result_history_persistence_cycle_registry_operation_plan_invalid"',
    "issnapshotpersistencecycleregistryoperationplanmapperonly: true",
    "snapshotpersistencecycleregistryoperationplanmappername:",
    "issnapshotpersistencecycleregistryoperationplanmapperprepared: true",
    "canmapsnapshotpersistencecycleregistryoperationplanstates: true",
    "datasourcesnapshotpersistencecycleregistryoperationplanmappername:",
    "isdatasourcesnapshotpersistencecycleregistryoperationplanmapperprepared:",
    "canmapdatasourcesnapshotpersistencecycleregistryoperationplanstates:",
    "datasourceinitialsnapshotpersistencecycleregistryoperationplanstate:",
    "mapparticipantfullexamresulthistorysnapshotpersistencecycleregistryoperationplanstate,",
    "function mapparticipantfullexamresulthistorysnapshotpersistencecycleregistryoperationreleasestate(input)",
    '"exam_result_history_persistence_cycle_registry_operation_release_ready"',
    '"exam_result_history_persistence_cycle_registry_operation_release_blocked"',
    '"exam_result_history_persistence_cycle_registry_operation_release_invalid"',
    "issnapshotpersistencecycleregistryoperationreleasemapperonly: true",
    "snapshotpersistencecycleregistryoperationreleasemappername:",
    "issnapshotpersistencecycleregistryoperationreleasemapperprepared: true",
    "canmapsnapshotpersistencecycleregistryoperationreleasestates: true",
    "datasourcesnapshotpersistencecycleregistryoperationreleasemappername:",
    "isdatasourcesnapshotpersistencecycleregistryoperationreleasemapperprepared:",
    "canmapdatasourcesnapshotpersistencecycleregistryoperationreleasestates:",
    "datasourceinitialsnapshotpersistencecycleregistryoperationreleasestate:",
    "mapparticipantfullexamresulthistorysnapshotpersistencecycleregistryoperationreleasestate,",
    "function guardparticipantfullexamresulthistorysnapshotpersistencecycleregistryexecution(input)",
    '"exam_result_history_persistence_cycle_registry_execution_guard_ready"',
    '"exam_result_history_persistence_cycle_registry_execution_guard_blocked"',
    '"exam_result_history_persistence_cycle_registry_execution_guard_invalid"',
    "issnapshotpersistencecycleregistryexecutionguardonly: true",
    "snapshotpersistencecycleregistryexecutionguardname:",
    "issnapshotpersistencecycleregistryexecutionguardprepared: true",
    "canguardsnapshotpersistencecycleregistryexecutions: true",
    "datasourcesnapshotpersistencecycleregistryexecutionguardname:",
    "isdatasourcesnapshotpersistencecycleregistryexecutionguardprepared:",
    "canguarddatasourcesnapshotpersistencecycleregistryexecutions:",
    "datasourceinitialsnapshotpersistencecycleregistryexecutionstate:",
    "guardparticipantfullexamresulthistorysnapshotpersistencecycleregistryexecution,",
    "function mapparticipantfullexamresulthistorysnapshotpersistencecycleregistryinvocationcontract(input)",
    '"exam_result_history_persistence_cycle_registry_invocation_contract_ready"',
    '"exam_result_history_persistence_cycle_registry_invocation_contract_blocked"',
    '"exam_result_history_persistence_cycle_registry_invocation_contract_invalid"',
    "issnapshotpersistencecycleregistryinvocationcontractonly: true",
    "snapshotpersistencecycleregistryinvocationcontractname:",
    "issnapshotpersistencecycleregistryinvocationcontractprepared: true",
    "canmapsnapshotpersistencecycleregistryinvocationcontracts: true",
    "datasourcesnapshotpersistencecycleregistryinvocationcontractname:",
    "isdatasourcesnapshotpersistencecycleregistryinvocationcontractprepared:",
    "canmapdatasourcesnapshotpersistencecycleregistryinvocationcontracts:",
    "datasourceinitialsnapshotpersistencecycleregistryinvocationcontractstate:",
    "mapparticipantfullexamresulthistorysnapshotpersistencecycleregistryinvocationcontract,",
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


if text.count(
    "function mapParticipantFullExamResultHistorySnapshotResumeState(input)"
) != 1:
    fail(
        "Snapshot-Wiederaufnahme-State muss genau einmal "
        "vorhanden sein."
    )

resume_start = lower.index(
    "function mapparticipantfullexamresulthistorysnapshotresumestate(input)"
)
resume_end = lower.index(
    "function normalizeparticipantfullexamresulthistorycontrollersnapshot(input)",
    resume_start,
)
resume_block = lower[
    resume_start:resume_end
]

for required in (
    "normalizeparticipantfullexamresulthistorycontrollersnapshot(",
    "source.snapshot",
    "mapparticipantfullexamresulthistoryrequestcontrollerstate({",
    'action: "initialize"',
    'action: "start"',
    "snapshotstate.isterminal",
    "snapshotstate.canresume !== true",
    "snapshotstate.phase !==",
    "snapshot_resume_terminal_state",
    "snapshot_resume_phase_invalid",
    "snapshot_resume_controller_reconstruction_invalid",
    "snapshot_resume_pending_reconstruction_invalid",
    "snapshot_resume_action_invalid",
    "start_prepared_request",
    "retry_pending_request",
    "exam_result_history_snapshot_resume_prepared",
    "exam_result_history_snapshot_resume_pending_retry",
    "exam_result_history_snapshot_resume_navigation_prepared",
    "exam_result_history_snapshot_resume_terminal_blocked",
    "exam_result_history_snapshot_resume_invalid",
    "issnapshotresumemapperonly: true",
    "islivecall: false",
    "canexecuteliverequest: false",
):
    if required not in resume_block:
        fail(
            "Snapshot-Wiederaufnahme-Anweisung fehlt: "
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
    "snapshotstate.results",
    "source.snapshot.controllerstate",
):
    if forbidden in resume_block:
        fail(
            "Unzulässiger Inhalt im Snapshot-Wiederaufnahme-State: "
            f"{forbidden}"
        )


if text.count(
    "function mapParticipantFullExamResultHistorySnapshotCreationState(input)"
) != 1:
    fail(
        "Snapshot-Erstellungsstate muss genau einmal "
        "vorhanden sein."
    )

creation_start = lower.index(
    "function mapparticipantfullexamresulthistorysnapshotcreationstate(input)"
)
creation_end = lower.index(
    "function mapparticipantfullexamresulthistorysnapshotresumestate(input)",
    creation_start,
)
creation_block = lower[
    creation_start:creation_end
]

for required in (
    "normalizeparticipantfullexamresulthistorycontrollersnapshot({",
    "snapshotversion: 1",
    "mapparticipantfullexamresulthistoryrequestcontrollerstate({",
    'action: "initialize"',
    'action: "start"',
    "snapshot_creation_controller_state_missing",
    "snapshot_creation_state_not_resumable",
    "snapshot_creation_controller_reconstruction_invalid",
    "snapshot_creation_pending_reconstruction_invalid",
    "snapshot_creation_phase_invalid",
    "snapshot_creation_round_trip_invalid",
    "exam_result_history_snapshot_creation_ready",
    "exam_result_history_snapshot_creation_blocked",
    "exam_result_history_snapshot_creation_invalid",
    "issnapshotcreationmapperonly: true",
    "canpersistlater: true",
    "canwritestorage: false",
    "snapshotpayload",
):
    if required not in creation_block:
        fail(
            "Snapshot-Erstellungs-Anweisung fehlt: "
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
    "localstorage",
    "sessionstorage",
):
    if forbidden in creation_block:
        fail(
            "Unzulässiger Inhalt im Snapshot-Erstellungsstate: "
            f"{forbidden}"
        )


if text.count(
    "function mapParticipantFullExamResultHistorySnapshotSerializationState(input)"
) != 1:
    fail(
        "Snapshot-Serialisierungsstate muss genau einmal "
        "vorhanden sein."
    )

if text.count(
    "function getParticipantFullExamResultHistorySnapshotUtf8ByteLength(value)"
) != 1:
    fail(
        "UTF-8-Byte-Längen-Hilfsfunktion muss genau einmal "
        "vorhanden sein."
    )

serialization_start = lower.index(
    "function mapparticipantfullexamresulthistorysnapshotserializationstate(input)"
)
serialization_end = lower.index(
    "function mapparticipantfullexamresulthistorysnapshotcreationstate(input)",
    serialization_start,
)
serialization_block = lower[
    serialization_start:serialization_end
]

for required in (
    "const maximumserializedbytes = 4096",
    "mapparticipantfullexamresulthistorysnapshotcreationstate({",
    "normalizeparticipantfullexamresulthistorycontrollersnapshot(",
    "json.stringify(",
    "json.parse(",
    "snapshot_serialization_creation_state_missing",
    "snapshot_serialization_creation_state_invalid",
    "snapshot_serialization_creation_state_not_ready",
    "snapshot_serialization_canonical_creation_invalid",
    "snapshot_serialization_creation_identity_mismatch",
    "snapshot_serialization_json_stringify_failed",
    "snapshot_serialization_json_invalid",
    "snapshot_serialization_byte_length_invalid",
    "snapshot_serialization_size_limit_exceeded",
    "snapshot_serialization_json_parse_failed",
    "snapshot_serialization_json_not_canonical",
    "snapshot_serialization_structure_invalid",
    "snapshot_serialization_round_trip_mismatch",
    "exam_result_history_snapshot_serialization_ready",
    "exam_result_history_snapshot_serialization_blocked",
    "exam_result_history_snapshot_serialization_too_large",
    "exam_result_history_snapshot_serialization_invalid",
    "issnapshotserializationmapperonly: true",
    "canwritestorage: false",
):
    if required not in serialization_block:
        fail(
            "Snapshot-Serialisierungs-Anweisung fehlt: "
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
    "localstorage",
    "sessionstorage",
    "indexeddb",
    "document.cookie",
    "eval(",
):
    if forbidden in serialization_block:
        fail(
            "Unzulässiger Inhalt im Snapshot-Serialisierungsstate: "
            f"{forbidden}"
        )


if text.count(
    "function mapParticipantFullExamResultHistorySnapshotDeserializationState(input)"
) != 1:
    fail(
        "Snapshot-Deserialisierungsstate muss genau einmal "
        "vorhanden sein."
    )

deserialization_start = lower.index(
    "function mapparticipantfullexamresulthistorysnapshotdeserializationstate(input)"
)
deserialization_end = lower.index(
    "function getparticipantfullexamresulthistorysnapshotutf8bytelength(value)",
    deserialization_start,
)
deserialization_block = lower[
    deserialization_start:deserialization_end
]

for required in (
    "const maximumserializedbytes = 4096",
    "getparticipantfullexamresulthistorysnapshotutf8bytelength(",
    "json.parse(",
    "json.stringify(",
    "serializedjson.trim() !== serializedjson",
    "normalizeparticipantfullexamresulthistorycontrollersnapshot(",
    "mapparticipantfullexamresulthistorysnapshotcreationstate({",
    "mapparticipantfullexamresulthistorysnapshotserializationstate({",
    "mapparticipantfullexamresulthistorysnapshotresumestate({",
    "snapshot_deserialization_input_invalid",
    "snapshot_deserialization_json_invalid",
    "snapshot_deserialization_byte_length_invalid",
    "snapshot_deserialization_size_limit_exceeded",
    "snapshot_deserialization_json_not_canonical",
    "snapshot_deserialization_json_parse_failed",
    "snapshot_deserialization_structure_invalid",
    "snapshot_deserialization_canonical_creation_invalid",
    "snapshot_deserialization_round_trip_mismatch",
    "snapshot_deserialization_identity_mismatch",
    "snapshot_deserialization_resume_state_invalid",
    "exam_result_history_snapshot_deserialization_ready",
    "exam_result_history_snapshot_deserialization_too_large",
    "exam_result_history_snapshot_deserialization_invalid",
    "issnapshotdeserializationmapperonly: true",
    "canwritestorage: false",
):
    if required not in deserialization_block:
        fail(
            "Snapshot-Deserialisierungs-Anweisung fehlt: "
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
    "localstorage",
    "sessionstorage",
    "indexeddb",
    "document.cookie",
    "eval(",
    "new function(",
):
    if forbidden in deserialization_block:
        fail(
            "Unzulässiger Inhalt im Snapshot-Deserialisierungsstate: "
            f"{forbidden}"
        )


if text.count(
    "function mapParticipantFullExamResultHistorySnapshotPersistenceContract(input)"
) != 1:
    fail(
        "Snapshot-Persistenzvertrag muss genau einmal "
        "vorhanden sein."
    )

persistence_start = lower.index(
    "function mapparticipantfullexamresulthistorysnapshotpersistencecontract(input)"
)
persistence_end = lower.index(
    "function mapparticipantfullexamresulthistorysnapshotdeserializationstate(input)",
    persistence_start,
)
persistence_block = lower[
    persistence_start:persistence_end
]

for required in (
    'allowedintents = [',
    '"save"',
    '"load"',
    '"delete"',
    '"accaoui.exam_history.snapshot.v1"',
    "const maximumstoragekeylength = 128",
    "mapparticipantfullexamresulthistoryrequestidentity({",
    'mode: "create"',
    "mapparticipantfullexamresulthistorysnapshotdeserializationstate({",
    "snapshot_persistence_intent_invalid",
    "snapshot_persistence_storage_key_invalid",
    "snapshot_persistence_storage_key_format_invalid",
    "snapshot_persistence_storage_key_noncanonical",
    "snapshot_persistence_serialization_state_missing",
    "snapshot_persistence_serialization_state_invalid",
    "snapshot_persistence_serialization_state_not_ready",
    "snapshot_persistence_save_identity_mismatch",
    "snapshot_persistence_load_value_missing",
    "snapshot_persistence_storage_key_identity_mismatch",
    "exam_result_history_snapshot_persistence_save_ready",
    "exam_result_history_snapshot_persistence_load_ready",
    "exam_result_history_snapshot_persistence_delete_ready",
    "exam_result_history_snapshot_persistence_save_blocked",
    "exam_result_history_snapshot_persistence_load_blocked",
    "exam_result_history_snapshot_persistence_invalid",
    "issnapshotpersistencecontractonly: true",
    "canexecutestorage: false",
    "canwritestorage: false",
):
    if required not in persistence_block:
        fail(
            "Snapshot-Persistenz-Anweisung fehlt: "
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
    "date.now(",
    "math.random(",
    "crypto.",
    "...source",
    "...input",
    "localstorage",
    "sessionstorage",
    "indexeddb",
    "document.cookie",
    ".setitem(",
    ".getitem(",
    ".removeitem(",
):
    if forbidden in persistence_block:
        fail(
            "Unzulässiger Inhalt im Snapshot-Persistenzvertrag: "
            f"{forbidden}"
        )


if text.count(
    "function mapParticipantFullExamResultHistorySnapshotStorageAdapterReadiness(input)"
) != 1:
    fail(
        "Persistenz-Adapter-Readiness-State muss genau einmal "
        "vorhanden sein."
    )

readiness_start = lower.index(
    "function mapparticipantfullexamresulthistorysnapshotstorageadapterreadiness(input)"
)
readiness_end = lower.index(
    "function mapparticipantfullexamresulthistorysnapshotpersistencecontract(input)",
    readiness_start,
)
readiness_block = lower[
    readiness_start:readiness_end
]

for required in (
    '"accaoui_exam_history_snapshot_storage_adapter_v1"',
    "const expectedcontractversion = 1",
    'requiredcapabilities = [',
    '"read"',
    '"write"',
    '"delete"',
    "object.getownpropertydescriptor(",
    "object.prototype.hasownproperty.call(",
    "storage_adapter_missing",
    "storage_adapter_must_be_object",
    "storage_adapter_kind_invalid",
    "storage_adapter_contract_version_invalid",
    "storage_adapter_capability_inspection_failed",
    "storage_adapter_capability_accessor_not_allowed",
    "storage_adapter_capabilities_partial",
    "storage_adapter_capabilities_unavailable",
    "exam_result_history_storage_adapter_readiness_ready",
    "exam_result_history_storage_adapter_readiness_partial",
    "exam_result_history_storage_adapter_readiness_unavailable",
    "exam_result_history_storage_adapter_readiness_invalid",
    "issnapshotstorageadapterreadinessonly: true",
    "canexecutestorage: false",
    "canread",
    "canwrite",
    "candelete",
):
    if required not in readiness_block:
        fail(
            "Persistenz-Adapter-Readiness-Anweisung fehlt: "
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
    "date.now(",
    "math.random(",
    "crypto.",
    "...source",
    "...input",
    "localstorage",
    "sessionstorage",
    "indexeddb",
    "document.cookie",
    "storageadapter.read(",
    "storageadapter.write(",
    "storageadapter.delete(",
    ".setitem(",
    ".getitem(",
    ".removeitem(",
):
    if forbidden in readiness_block:
        fail(
            "Unzulässiger Inhalt im Persistenz-Adapter-Readiness-State: "
            f"{forbidden}"
        )


if text.count(
    "function mapParticipantFullExamResultHistorySnapshotPersistenceOperationPlan(input)"
) != 1:
    fail(
        "Persistenz-Operationsplan-State muss genau einmal "
        "vorhanden sein."
    )

operation_start = lower.index(
    "function mapparticipantfullexamresulthistorysnapshotpersistenceoperationplan(input)"
)
operation_end = lower.index(
    "function mapparticipantfullexamresulthistorysnapshotstorageadapterreadiness(input)",
    operation_start,
)
operation_block = lower[
    operation_start:operation_end
]

for required in (
    "mapparticipantfullexamresulthistorysnapshotpersistencecontract({",
    "mapparticipantfullexamresulthistorysnapshotdeserializationstate({",
    '"write"',
    '"read"',
    '"delete"',
    "persistence_operation_plan_persistence_state_missing",
    "persistence_operation_plan_persistence_state_invalid",
    "persistence_operation_plan_readiness_state_missing",
    "persistence_operation_plan_readiness_state_invalid",
    "persistence_operation_plan_intent_invalid",
    "persistence_operation_plan_contract_not_ready",
    "persistence_operation_plan_storage_key_invalid",
    "persistence_operation_plan_save_payload_invalid",
    "persistence_operation_plan_load_state_invalid",
    "persistence_operation_plan_capability_unavailable",
    "exam_result_history_persistence_operation_plan_ready",
    "exam_result_history_persistence_operation_plan_blocked",
    "exam_result_history_persistence_operation_plan_invalid",
    "issnapshotpersistenceoperationplanonly: true",
    "canexecutestorage: false",
):
    if required not in operation_block:
        fail(
            "Persistenz-Operationsplan-Anweisung fehlt: "
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
    "date.now(",
    "math.random(",
    "crypto.",
    "...source",
    "...input",
    "localstorage",
    "sessionstorage",
    "indexeddb",
    "document.cookie",
    "storageadapter.read(",
    "storageadapter.write(",
    "storageadapter.delete(",
    ".setitem(",
    ".getitem(",
    ".removeitem(",
):
    if forbidden in operation_block:
        fail(
            "Unzulässiger Inhalt im Persistenz-Operationsplan: "
            f"{forbidden}"
        )


if text.count(
    "function getParticipantFullExamResultHistorySnapshotStorageAdapterReadinessFingerprint(input)"
) != 1:
    fail(
        "Adapter-Readiness-Fingerprint-Helfer muss genau einmal "
        "vorhanden sein."
    )

if text.count(
    "function mapParticipantFullExamResultHistorySnapshotPersistenceOperationReleaseState(input)"
) != 1:
    fail(
        "Persistenz-Operationsfreigabe-State muss genau einmal "
        "vorhanden sein."
    )

fingerprint_start = lower.index(
    "function getparticipantfullexamresulthistorysnapshotstorageadapterreadinessfingerprint(input)"
)
release_start = lower.index(
    "function mapparticipantfullexamresulthistorysnapshotpersistenceoperationreleasestate(input)",
    fingerprint_start,
)
operation_start = lower.index(
    "function mapparticipantfullexamresulthistorysnapshotpersistenceoperationplan(input)",
    release_start,
)

fingerprint_block = lower[
    fingerprint_start:release_start
]

release_block = lower[
    release_start:operation_start
]

for required in (
    '"accaoui_exam_history_snapshot_storage_adapter_v1"',
    "state.contractversion !== 1",
    'requiredcapabilities = [',
    "state.availablecapabilitycount !==",
    "state.isadapterready !==",
    "state.ispartiallyready !==",
    "availablecapabilities.join",
    "missingcapabilities.join",
):
    if required not in fingerprint_block:
        fail(
            "Adapter-Readiness-Fingerprint-Anweisung fehlt: "
            f"{required}"
        )

for required in (
    "getparticipantfullexamresulthistorysnapshotstorageadapterreadinessfingerprint(",
    "mapparticipantfullexamresulthistorysnapshotpersistenceoperationplan({",
    "persistence_operation_release_plan_missing",
    "persistence_operation_release_plan_invalid",
    "persistence_operation_release_persistence_state_invalid",
    "persistence_operation_release_readiness_state_invalid",
    "persistence_operation_release_readiness_fingerprint_invalid",
    "persistence_operation_release_readiness_changed",
    "persistence_operation_release_recomputed_plan_not_ready",
    "persistence_operation_release_plan_mismatch",
    "exam_history_persistence_release:",
    "exam_result_history_persistence_operation_release_ready",
    "exam_result_history_persistence_operation_release_blocked",
    "exam_result_history_persistence_operation_release_invalid",
    "issnapshotpersistenceoperationreleaseonly: true",
    "canexecutestorage: false",
):
    if required not in release_block:
        fail(
            "Persistenz-Operationsfreigabe-Anweisung fehlt: "
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
    "date.now(",
    "math.random(",
    "crypto.",
    "...source",
    "...input",
    "localstorage",
    "sessionstorage",
    "indexeddb",
    "document.cookie",
    "storageadapter.read(",
    "storageadapter.write(",
    "storageadapter.delete(",
    ".setitem(",
    ".getitem(",
    ".removeitem(",
):
    if (
      forbidden in fingerprint_block or
      forbidden in release_block
    ):
        fail(
            "Unzulässiger Inhalt in Persistenz-Freigabe: "
            f"{forbidden}"
        )


if text.count(
    "function guardParticipantFullExamResultHistorySnapshotPersistenceExecution(input)"
) != 1:
    fail(
        "Persistenz-Ausführungs-Guard muss genau einmal "
        "vorhanden sein."
    )

execution_start = lower.index(
    "function guardparticipantfullexamresulthistorysnapshotpersistenceexecution(input)"
)
fingerprint_start = lower.index(
    "function getparticipantfullexamresulthistorysnapshotstorageadapterreadinessfingerprint(input)",
    execution_start,
)
execution_block = lower[
    execution_start:fingerprint_start
]

for required in (
    "object.getownpropertydescriptor(",
    "object.prototype.hasownproperty.call(",
    "mapparticipantfullexamresulthistorysnapshotstorageadapterreadiness({",
    "getparticipantfullexamresulthistorysnapshotstorageadapterreadinessfingerprint(",
    "mapparticipantfullexamresulthistorysnapshotpersistenceoperationplan({",
    "mapparticipantfullexamresulthistorysnapshotpersistenceoperationreleasestate({",
    "persistence_execution_release_state_missing",
    "persistence_execution_persistence_state_missing",
    "persistence_execution_storage_adapter_missing",
    "persistence_execution_release_state_invalid",
    "persistence_execution_persistence_state_invalid",
    "persistence_execution_storage_adapter_invalid",
    "persistence_execution_readiness_changed",
    "persistence_execution_recomputed_plan_invalid",
    "persistence_execution_recomputed_release_invalid",
    "persistence_execution_release_mismatch",
    "persistence_execution_operation_invalid",
    "persistence_execution_method_invalid",
    "persistence_execution_write_payload_invalid",
    "persistence_execution_unexpected_payload",
    "persistence_execution_load_state_invalid",
    "exam_history_persistence_execution:",
    "exam_result_history_persistence_execution_guard_ready",
    "exam_result_history_persistence_execution_guard_invalid",
    "issnapshotpersistenceexecutionguardonly: true",
    "caninvokelater: true",
    "canexecutestorage: false",
    "ismethodreferencevalidated: true",
):
    if required not in execution_block:
        fail(
            "Persistenz-Ausführungs-Anweisung fehlt: "
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
    "date.now(",
    "math.random(",
    "crypto.",
    "...source",
    "...input",
    "localstorage",
    "sessionstorage",
    "indexeddb",
    "document.cookie",
    "storageadapter.read(",
    "storageadapter.write(",
    "storageadapter.delete(",
    "methodproperty.value(",
    ".setitem(",
    ".getitem(",
    ".removeitem(",
):
    if forbidden in execution_block:
        fail(
            "Unzulässiger Inhalt im Persistenz-Ausführungs-Guard: "
            f"{forbidden}"
        )


if text.count(
    "function mapParticipantFullExamResultHistorySnapshotPersistenceInvocationContract(input)"
) != 1:
    fail(
        "Persistenz-Aufrufvertrag muss genau einmal "
        "vorhanden sein."
    )

invocation_start = lower.index(
    "function mapparticipantfullexamresulthistorysnapshotpersistenceinvocationcontract(input)"
)
execution_start = lower.index(
    "function guardparticipantfullexamresulthistorysnapshotpersistenceexecution(input)",
    invocation_start,
)
invocation_block = lower[
    invocation_start:execution_start
]

for required in (
    "mapparticipantfullexamresulthistorysnapshotpersistencecontract({",
    "getparticipantfullexamresulthistorysnapshotutf8bytelength(",
    "mapparticipantfullexamresulthistorysnapshotdeserializationstate({",
    'invocationschemaversion: 1',
    'methodname',
    'invocationarguments.push({',
    'name: "storagekey"',
    'name: "serializedjson"',
    "persistence_invocation_contract_execution_state_missing",
    "persistence_invocation_contract_execution_state_invalid",
    "persistence_invocation_contract_operation_invalid",
    "persistence_invocation_contract_capability_mismatch",
    "persistence_invocation_contract_argument_count_invalid",
    "persistence_invocation_contract_load_state_invalid",
    "persistence_invocation_contract_readiness_fingerprint_invalid",
    "persistence_invocation_contract_storage_key_invalid",
    "persistence_invocation_contract_release_identity_invalid",
    "persistence_invocation_contract_execution_identity_invalid",
    "persistence_invocation_contract_write_payload_invalid",
    "persistence_invocation_contract_write_size_mismatch",
    "persistence_invocation_contract_write_payload_validation_failed",
    "persistence_invocation_contract_unexpected_payload",
    "persistence_invocation_contract_argument_schema_invalid",
    "exam_history_persistence_invocation:",
    "exam_result_history_persistence_invocation_contract_ready",
    "exam_result_history_persistence_invocation_contract_invalid",
    "issnapshotpersistenceinvocationcontractonly: true",
    "caninvokelater: true",
    "canexecutestorage: false",
):
    if required not in invocation_block:
        fail(
            "Persistenz-Aufrufvertrag-Anweisung fehlt: "
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
    "date.now(",
    "math.random(",
    "crypto.",
    "...source",
    "...input",
    "localstorage",
    "sessionstorage",
    "indexeddb",
    "document.cookie",
    "storageadapter.read(",
    "storageadapter.write(",
    "storageadapter.delete(",
    "methodproperty.value(",
    ".setitem(",
    ".getitem(",
    ".removeitem(",
):
    if forbidden in invocation_block:
        fail(
            "Unzulässiger Inhalt im Persistenz-Aufrufvertrag: "
            f"{forbidden}"
        )


if text.count(
    "function mapParticipantFullExamResultHistorySnapshotPersistenceInvocationPackageState(input)"
) != 1:
    fail(
        "Persistenz-Aufrufpaket-State muss genau einmal "
        "vorhanden sein."
    )

package_start = lower.index(
    "function mapparticipantfullexamresulthistorysnapshotpersistenceinvocationpackagestate(input)"
)
invocation_start = lower.index(
    "function mapparticipantfullexamresulthistorysnapshotpersistenceinvocationcontract(input)",
    package_start,
)
package_block = lower[
    package_start:invocation_start
]

for required in (
    "object.getownpropertydescriptor(",
    "object.prototype.hasownproperty.call(",
    "guardparticipantfullexamresulthistorysnapshotpersistenceexecution({",
    "mapparticipantfullexamresulthistorysnapshotpersistenceinvocationcontract({",
    "json.stringify(",
    "invocationarguments.push({",
    "persistence_invocation_package_release_state_missing",
    "persistence_invocation_package_persistence_state_missing",
    "persistence_invocation_package_storage_adapter_missing",
    "persistence_invocation_package_execution_state_missing",
    "persistence_invocation_package_contract_missing",
    "persistence_invocation_package_execution_state_invalid",
    "persistence_invocation_package_contract_invalid",
    "persistence_invocation_package_storage_adapter_invalid",
    "persistence_invocation_package_recomputed_execution_invalid",
    "persistence_invocation_package_execution_state_mismatch",
    "persistence_invocation_package_recomputed_contract_invalid",
    "persistence_invocation_package_contract_mismatch",
    "persistence_invocation_package_method_invalid",
    "persistence_invocation_package_argument_schema_invalid",
    "exam_history_persistence_invocation_package:",
    "exam_result_history_persistence_invocation_package_ready",
    "exam_result_history_persistence_invocation_package_invalid",
    "issnapshotpersistenceinvocationpackageonly: true",
    "invocationpackageschemaversion: 1",
    "caninvokelater: true",
    "canexecutestorage: false",
    "ismethodreferencevalidated: true",
):
    if required not in package_block:
        fail(
            "Persistenz-Aufrufpaket-Anweisung fehlt: "
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
    "date.now(",
    "math.random(",
    "crypto.",
    "...source",
    "...input",
    "localstorage",
    "sessionstorage",
    "indexeddb",
    "document.cookie",
    "storageadapter.read(",
    "storageadapter.write(",
    "storageadapter.delete(",
    "methodproperty.value(",
    ".setitem(",
    ".getitem(",
    ".removeitem(",
):
    if forbidden in package_block:
        fail(
            "Unzulässiger Inhalt im Persistenz-Aufrufpaket: "
            f"{forbidden}"
        )


if text.count(
    "function mapParticipantFullExamResultHistorySnapshotPersistenceResultContract(input)"
) != 1:
    fail(
        "Persistenz-Ergebnisvertrag muss genau einmal "
        "vorhanden sein."
    )

result_start = lower.index(
    "function mapparticipantfullexamresulthistorysnapshotpersistenceresultcontract(input)"
)
package_start = lower.index(
    "function mapparticipantfullexamresulthistorysnapshotpersistenceinvocationpackagestate(input)",
    result_start,
)
result_block = lower[
    result_start:package_start
]

for required in (
    "object.getownpropertydescriptor(",
    "object.prototype.hasownproperty.call(",
    "mapparticipantfullexamresulthistorysnapshotpersistencecontract({",
    "getparticipantfullexamresulthistorysnapshotutf8bytelength(",
    "mapparticipantfullexamresulthistorysnapshotdeserializationstate({",
    "const maximumresultbytes = 4096",
    "resultschemaversion: 1",
    "persistence_result_package_missing",
    "persistence_result_value_missing",
    "persistence_result_package_invalid",
    "persistence_result_operation_invalid",
    "persistence_result_storage_key_invalid",
    "persistence_result_identity_invalid",
    "persistence_result_argument_schema_invalid",
    "persistence_result_storage_key_argument_invalid",
    "persistence_result_write_payload_size_invalid",
    "persistence_result_write_payload_invalid",
    "persistence_result_unexpected_payload_size",
    "persistence_result_read_value_invalid",
    "persistence_result_read_size_invalid",
    "persistence_result_read_identity_mismatch",
    "persistence_result_write_confirmation_invalid",
    "persistence_result_delete_confirmation_invalid",
    "exam_result_history_persistence_result_read_ready",
    "exam_result_history_persistence_result_read_empty",
    "exam_result_history_persistence_result_write_confirmed",
    "exam_result_history_persistence_result_delete_confirmed",
    "exam_result_history_persistence_result_delete_absent",
    "exam_result_history_persistence_result_contract_invalid",
    "issnapshotpersistenceresultcontractonly: true",
    "canexecutestorage: false",
    "canresumesnapshot: true",
    "snapshotpayload:",
    "resumestate:",
):
    if required not in result_block:
        fail(
            "Persistenz-Ergebnisvertrag-Anweisung fehlt: "
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
    "date.now(",
    "math.random(",
    "crypto.",
    "...source",
    "...input",
    "localstorage",
    "sessionstorage",
    "indexeddb",
    "document.cookie",
    "storageadapter.read(",
    "storageadapter.write(",
    "storageadapter.delete(",
    "methodproperty.value(",
    ".setitem(",
    ".getitem(",
    ".removeitem(",
    "operationresult.error",
    "operationresult.message",
    "operationresult.details",
):
    if forbidden in result_block:
        fail(
            "Unzulässiger Inhalt im Persistenz-Ergebnisvertrag: "
            f"{forbidden}"
        )


if text.count(
    "function guardParticipantFullExamResultHistorySnapshotPersistenceResultAcceptance(input)"
) != 1:
    fail(
        "Persistenz-Ergebnisannahme-Guard muss genau einmal "
        "vorhanden sein."
    )

acceptance_start = lower.index(
    "function guardparticipantfullexamresulthistorysnapshotpersistenceresultacceptance(input)"
)
result_start = lower.index(
    "function mapparticipantfullexamresulthistorysnapshotpersistenceresultcontract(input)",
    acceptance_start,
)
acceptance_block = lower[
    acceptance_start:result_start
]

for required in (
    "object.getownpropertydescriptor(",
    "object.prototype.hasownproperty.call(",
    "mapparticipantfullexamresulthistorysnapshotpersistencecontract({",
    "getparticipantfullexamresulthistorysnapshotutf8bytelength(",
    "mapparticipantfullexamresulthistorysnapshotdeserializationstate({",
    "normalizeparticipantfullexamresulthistorycontrollersnapshot(",
    "mapparticipantfullexamresulthistorysnapshotresumestate({",
    "persistence_result_acceptance_active_package_missing",
    "persistence_result_acceptance_result_state_missing",
    "persistence_result_acceptance_active_package_invalid",
    "persistence_result_acceptance_active_operation_invalid",
    "persistence_result_acceptance_active_identity_invalid",
    "persistence_result_acceptance_storage_key_invalid",
    "persistence_result_acceptance_active_arguments_invalid",
    "persistence_result_acceptance_active_write_payload_invalid",
    "persistence_result_acceptance_result_state_invalid",
    "persistence_result_acceptance_stale_package",
    "persistence_result_acceptance_result_identity_mismatch",
    "persistence_result_acceptance_read_empty_invalid",
    "persistence_result_acceptance_read_result_invalid",
    "persistence_result_acceptance_read_snapshot_invalid",
    "persistence_result_acceptance_write_result_invalid",
    "persistence_result_acceptance_delete_result_invalid",
    "exam_result_history_persistence_result_acceptance_ready",
    "exam_result_history_persistence_result_acceptance_stale_ignored",
    "exam_result_history_persistence_result_acceptance_invalid",
    "issnapshotpersistenceresultacceptanceguardonly: true",
    "didacceptresult: true",
    "isstaleresult: true",
    "canexecutestorage: false",
):
    if required not in acceptance_block:
        fail(
            "Persistenz-Ergebnisannahme-Anweisung fehlt: "
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
    "date.now(",
    "math.random(",
    "crypto.",
    "...source",
    "...input",
    "localstorage",
    "sessionstorage",
    "indexeddb",
    "document.cookie",
    "storageadapter.read(",
    "storageadapter.write(",
    "storageadapter.delete(",
    ".setitem(",
    ".getitem(",
    ".removeitem(",
    "resultstate.error",
    "resultstate.message",
    "resultstate.details",
):
    if forbidden in acceptance_block:
        fail(
            "Unzulässiger Inhalt im Persistenz-Ergebnisannahme-Guard: "
            f"{forbidden}"
        )


if text.count(
    "function mapParticipantFullExamResultHistorySnapshotPersistenceCompletionState(input)"
) != 1:
    fail(
        "Persistenz-Abschlussstate muss genau einmal "
        "vorhanden sein."
    )

completion_start = lower.index(
    "function mapparticipantfullexamresulthistorysnapshotpersistencecompletionstate(input)"
)
acceptance_start = lower.index(
    "function guardparticipantfullexamresulthistorysnapshotpersistenceresultacceptance(input)",
    completion_start,
)
completion_block = lower[
    completion_start:acceptance_start
]

for required in (
    "mapparticipantfullexamresulthistorysnapshotpersistencecontract({",
    "normalizeparticipantfullexamresulthistorycontrollersnapshot(",
    "mapparticipantfullexamresulthistorysnapshotresumestate({",
    "persistence_completion_acceptance_state_missing",
    "persistence_completion_acceptance_state_invalid",
    "persistence_completion_operation_invalid",
    "persistence_completion_package_identity_invalid",
    "persistence_completion_storage_key_invalid",
    "persistence_completion_identity_invalid",
    "persistence_completion_read_empty_invalid",
    "persistence_completion_read_result_invalid",
    "persistence_completion_read_snapshot_invalid",
    "persistence_completion_write_result_invalid",
    "persistence_completion_delete_result_invalid",
    "exam_history_persistence_completion:",
    "exam_result_history_persistence_completion_read_ready",
    "exam_result_history_persistence_completion_read_empty",
    "exam_result_history_persistence_completion_write_confirmed",
    "exam_result_history_persistence_completion_delete_confirmed",
    "exam_result_history_persistence_completion_delete_absent",
    "exam_result_history_persistence_completion_invalid",
    "issnapshotpersistencecompletionmapperonly: true",
    "canfinalizepersistence: true",
    "isterminal: true",
    "issuccessful: true",
    "canresumesnapshot: true",
    "canexecutestorage: false",
):
    if required not in completion_block:
        fail(
            "Persistenz-Abschluss-Anweisung fehlt: "
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
    "date.now(",
    "math.random(",
    "crypto.",
    "...source",
    "...input",
    "localstorage",
    "sessionstorage",
    "indexeddb",
    "document.cookie",
    "storageadapter.read(",
    "storageadapter.write(",
    "storageadapter.delete(",
    ".setitem(",
    ".getitem(",
    ".removeitem(",
    "acceptancestate.error",
    "acceptancestate.message",
    "acceptancestate.details",
):
    if forbidden in completion_block:
        fail(
            "Unzulässiger Inhalt im Persistenz-Abschlussstate: "
            f"{forbidden}"
        )


if text.count(
    "function mapParticipantFullExamResultHistorySnapshotPersistenceCycleState(input)"
) != 1:
    fail(
        "Persistenz-Zyklusstate muss genau einmal "
        "vorhanden sein."
    )

cycle_start = lower.index(
    "function mapparticipantfullexamresulthistorysnapshotpersistencecyclestate(input)"
)
completion_start = lower.index(
    "function mapparticipantfullexamresulthistorysnapshotpersistencecompletionstate(input)",
    cycle_start,
)
cycle_block = lower[
    cycle_start:completion_start
]

for required in (
    "object.getownpropertydescriptor(",
    "object.prototype.hasownproperty.call(",
    "guardparticipantfullexamresulthistorysnapshotpersistenceresultacceptance({",
    "mapparticipantfullexamresulthistorysnapshotpersistencecompletionstate({",
    "json.stringify(",
    "persistence_cycle_invocation_package_missing",
    "persistence_cycle_result_contract_missing",
    "persistence_cycle_acceptance_state_missing",
    "persistence_cycle_completion_state_missing",
    "persistence_cycle_invocation_package_invalid",
    "persistence_cycle_result_contract_invalid",
    "persistence_cycle_acceptance_state_invalid",
    "persistence_cycle_completion_state_invalid",
    "persistence_cycle_recomputed_acceptance_not_ready",
    "persistence_cycle_acceptance_state_mismatch",
    "persistence_cycle_recomputed_completion_invalid",
    "persistence_cycle_completion_state_mismatch",
    "persistence_cycle_identity_mismatch",
    "exam_history_persistence_cycle:",
    "exam_result_history_persistence_cycle_completed",
    "exam_result_history_persistence_cycle_invalid",
    "issnapshotpersistencecyclemapperonly: true",
    "cycleschemaversion: 1",
    "canfinalizecycle: true",
    "isterminal: true",
    "issuccessful: true",
    "canexecutestorage: false",
):
    if required not in cycle_block:
        fail(
            "Persistenz-Zyklus-Anweisung fehlt: "
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
    "date.now(",
    "math.random(",
    "crypto.",
    "...source",
    "...input",
    "localstorage",
    "sessionstorage",
    "indexeddb",
    "document.cookie",
    "storageadapter.read(",
    "storageadapter.write(",
    "storageadapter.delete(",
    ".setitem(",
    ".getitem(",
    ".removeitem(",
    "resultcontractstate.error",
    "resultcontractstate.message",
    "resultcontractstate.details",
):
    if forbidden in cycle_block:
        fail(
            "Unzulässiger Inhalt im Persistenz-Zyklusstate: "
            f"{forbidden}"
        )


if text.count(
    "function guardParticipantFullExamResultHistorySnapshotPersistenceCycleRepetition(input)"
) != 1:
    fail(
        "Persistenz-Zyklus-Wiederholungs-Guard muss genau "
        "einmal vorhanden sein."
    )

repetition_start = lower.index(
    "function guardparticipantfullexamresulthistorysnapshotpersistencecyclerepetition(input)"
)
cycle_start = lower.index(
    "function mapparticipantfullexamresulthistorysnapshotpersistencecyclestate(input)",
    repetition_start,
)
repetition_block = lower[
    repetition_start:cycle_start
]

for required in (
    "object.getownpropertydescriptor(",
    "object.prototype.hasownproperty.call(",
    "new set()",
    "mapparticipantfullexamresulthistorysnapshotpersistencecontract({",
    "normalizeparticipantfullexamresulthistorycontrollersnapshot(",
    "mapparticipantfullexamresulthistorysnapshotresumestate({",
    "const maximumcompletedcycleidentities =",
    "persistence_cycle_repetition_cycle_state_missing",
    "persistence_cycle_repetition_registry_missing",
    "persistence_cycle_repetition_cycle_state_invalid",
    "persistence_cycle_repetition_registry_invalid",
    "persistence_cycle_repetition_registry_identity_invalid",
    "persistence_cycle_repetition_registry_duplicate",
    "persistence_cycle_repetition_outcome_invalid",
    "persistence_cycle_repetition_storage_key_invalid",
    "persistence_cycle_repetition_identity_invalid",
    "persistence_cycle_repetition_read_snapshot_invalid",
    "persistence_cycle_repetition_registry_limit_reached",
    "persistence_cycle_repetition_already_completed",
    "exam_result_history_persistence_cycle_repetition_ready",
    "exam_result_history_persistence_cycle_repetition_blocked",
    "exam_result_history_persistence_cycle_repetition_invalid",
    "issnapshotpersistencecyclerepetitionguardonly: true",
    "canacceptcycleonce: true",
    "canregistercycleidentitylater: true",
    "isduplicatecycle: true",
    "canexecutestorage: false",
):
    if required not in repetition_block:
        fail(
            "Persistenz-Zyklus-Wiederholungs-Anweisung fehlt: "
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
    "date.now(",
    "math.random(",
    "crypto.",
    "...source",
    "...input",
    "localstorage",
    "sessionstorage",
    "indexeddb",
    "document.cookie",
    "storageadapter.read(",
    "storageadapter.write(",
    "storageadapter.delete(",
    ".setitem(",
    ".getitem(",
    ".removeitem(",
):
    if forbidden in repetition_block:
        fail(
            "Unzulässiger Inhalt im Zyklus-Wiederholungs-Guard: "
            f"{forbidden}"
        )


if text.count(
    "function mapParticipantFullExamResultHistorySnapshotPersistenceCycleRegistryState(input)"
) != 1:
    fail(
        "Persistenz-Zyklusregister-State muss genau einmal "
        "vorhanden sein."
    )

registry_start = lower.index(
    "function mapparticipantfullexamresulthistorysnapshotpersistencecycleregistrystate(input)"
)
repetition_start = lower.index(
    "function guardparticipantfullexamresulthistorysnapshotpersistencecyclerepetition(input)",
    registry_start,
)
registry_block = lower[
    registry_start:repetition_start
]

for required in (
    "object.getownpropertydescriptor(",
    "object.prototype.hasownproperty.call(",
    "new set()",
    "identities.sort()",
    "registryversion = 1",
    "maximumcompletedcycleidentities =",
    '"exam_history_persistence_cycle_registry:v1"',
    "exam_result_history_persistence_cycle_registry_empty",
    "exam_result_history_persistence_cycle_registry_ready",
    "exam_result_history_persistence_cycle_registry_updated",
    "exam_result_history_persistence_cycle_registry_duplicate_unchanged",
    "exam_result_history_persistence_cycle_registry_invalid",
    "persistence_cycle_registry_identities_missing",
    "persistence_cycle_registry_identity_invalid",
    "persistence_cycle_registry_duplicate",
    "persistence_cycle_registry_repetition_state_invalid",
    "persistence_cycle_registry_repetition_source_mismatch",
    "persistence_cycle_registry_repetition_update_invalid",
    "persistence_cycle_registry_duplicate_state_invalid",
    "issnapshotpersistencecycleregistrymapperonly: true",
    "canuseregistry: true",
    "canregistermorecycleidentities:",
    "iscanonicalorder: true",
    "registryPayload",
    "canexecutestorage: false",
):
    if required.lower() not in registry_block:
        fail(
            "Persistenz-Zyklusregister-Anweisung fehlt: "
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
    "date.now(",
    "math.random(",
    "crypto.",
    "...source",
    "...input",
    "localstorage",
    "sessionstorage",
    "indexeddb",
    "document.cookie",
    "storageadapter.read(",
    "storageadapter.write(",
    "storageadapter.delete(",
    ".setitem(",
    ".getitem(",
    ".removeitem(",
):
    if forbidden in registry_block:
        fail(
            "Unzulässiger Inhalt im Persistenz-Zyklusregister: "
            f"{forbidden}"
        )


if text.count(
    "function mapParticipantFullExamResultHistorySnapshotPersistenceCycleRegistrySerializationState(input)"
) != 1:
    fail(
        "Persistenz-Zyklusregister-Serialisierungsstate muss "
        "genau einmal vorhanden sein."
    )

registry_serialization_start = lower.index(
    "function mapparticipantfullexamresulthistorysnapshotpersistencecycleregistryserializationstate(input)"
)
registry_start = lower.index(
    "function mapparticipantfullexamresulthistorysnapshotpersistencecycleregistrystate(input)",
    registry_serialization_start,
)
registry_serialization_block = lower[
    registry_serialization_start:registry_start
]

for required in (
    "object.getownpropertydescriptor(",
    "object.prototype.hasownproperty.call(",
    "object.keys(",
    "json.stringify(",
    "json.parse(",
    "getparticipantfullexamresulthistorysnapshotutf8bytelength(",
    "mapparticipantfullexamresulthistorysnapshotpersistencecycleregistrystate({",
    "const serializationSchemaVersion".lower(),
    "const maximumserializedbytes = 32768",
    "persistence_cycle_registry_serialization_registry_state_missing",
    "persistence_cycle_registry_serialization_registry_accessor_not_allowed",
    "persistence_cycle_registry_serialization_registry_state_invalid",
    "persistence_cycle_registry_serialization_registry_field_invalid",
    "persistence_cycle_registry_serialization_registry_status_invalid",
    "persistence_cycle_registry_serialization_identities_invalid",
    "persistence_cycle_registry_serialization_registry_flags_invalid",
    "persistence_cycle_registry_serialization_identity_order_invalid",
    "persistence_cycle_registry_serialization_payload_invalid",
    "persistence_cycle_registry_serialization_payload_mismatch",
    "persistence_cycle_registry_serialization_canonical_state_invalid",
    "persistence_cycle_registry_serialization_size_invalid",
    "persistence_cycle_registry_serialization_round_trip_invalid",
    "exam_result_history_persistence_cycle_registry_serialization_ready",
    "exam_result_history_persistence_cycle_registry_serialization_invalid",
    "issnapshotpersistencecycleregistryserializationmapperonly: true",
    "canserializeregistry: true",
    "canpersistlater: true",
    "canwritestorage: false",
    "canexecutestorage: false",
):
    if required not in registry_serialization_block:
        fail(
            "Persistenz-Zyklusregister-Serialisierungsanweisung "
            f"fehlt: {required}"
        )

for forbidden in (
    ".rpc(",
    "createclient(",
    "window.supabase",
    "fetch(",
    "xmlhttprequest",
    "participant_id",
    "service_role",
    "date.now(",
    "math.random(",
    "crypto.",
    "...source",
    "...input",
    "localstorage",
    "sessionstorage",
    "indexeddb",
    "document.cookie",
    "storageadapter.read(",
    "storageadapter.write(",
    "storageadapter.delete(",
    ".setitem(",
    ".getitem(",
    ".removeitem(",
):
    if forbidden in registry_serialization_block:
        fail(
            "Unzulässiger Inhalt in der "
            "Zyklusregister-Serialisierung: "
            f"{forbidden}"
        )


if text.count(
    "function mapParticipantFullExamResultHistorySnapshotPersistenceCycleRegistryDeserializationState(input)"
) != 1:
    fail(
        "Persistenz-Zyklusregister-Deserialisierungsstate muss "
        "genau einmal vorhanden sein."
    )

registry_deserialization_start = lower.index(
    "function mapparticipantfullexamresulthistorysnapshotpersistencecycleregistrydeserializationstate(input)"
)
registry_serialization_start = lower.index(
    "function mapparticipantfullexamresulthistorysnapshotpersistencecycleregistryserializationstate(input)",
    registry_deserialization_start,
)
registry_deserialization_block = lower[
    registry_deserialization_start:
    registry_serialization_start
]

for required in (
    "object.getownpropertydescriptor(",
    "object.prototype.hasownproperty.call(",
    "object.keys(",
    "json.parse(",
    "json.stringify(",
    "getparticipantfullexamresulthistorysnapshotutf8bytelength(",
    "mapparticipantfullexamresulthistorysnapshotpersistencecycleregistrystate({",
    "mapparticipantfullexamresulthistorysnapshotpersistencecycleregistryserializationstate({",
    "const deserializationschemaversion = 1",
    "const maximumserializedbytes = 32768",
    "persistence_cycle_registry_deserialization_json_missing",
    "persistence_cycle_registry_deserialization_json_accessor_not_allowed",
    "persistence_cycle_registry_deserialization_json_invalid",
    "persistence_cycle_registry_deserialization_size_invalid",
    "persistence_cycle_registry_deserialization_json_parse_failed",
    "persistence_cycle_registry_deserialization_payload_invalid",
    "persistence_cycle_registry_deserialization_payload_fields_invalid",
    "persistence_cycle_registry_deserialization_version_invalid",
    "persistence_cycle_registry_deserialization_identities_invalid",
    "persistence_cycle_registry_deserialization_json_not_canonical",
    "persistence_cycle_registry_deserialization_registry_state_invalid",
    "persistence_cycle_registry_deserialization_payload_not_canonical",
    "persistence_cycle_registry_deserialization_round_trip_invalid",
    "exam_result_history_persistence_cycle_registry_deserialization_ready",
    "exam_result_history_persistence_cycle_registry_deserialization_invalid",
    "issnapshotpersistencecycleregistrydeserializationmapperonly: true",
    "candeserializeregistry: true",
    "canuseregistry: true",
    "canpersistlater: true",
    "canexecutestorage: false",
):
    if required not in registry_deserialization_block:
        fail(
            "Persistenz-Zyklusregister-Deserialisierungsanweisung "
            f"fehlt: {required}"
        )

for forbidden in (
    ".rpc(",
    "createclient(",
    "window.supabase",
    "fetch(",
    "xmlhttprequest",
    "participant_id",
    "service_role",
    "date.now(",
    "math.random(",
    "crypto.",
    "...source",
    "...input",
    "localstorage",
    "sessionstorage",
    "indexeddb",
    "document.cookie",
    "storageadapter.read(",
    "storageadapter.write(",
    "storageadapter.delete(",
    ".setitem(",
    ".getitem(",
    ".removeitem(",
):
    if forbidden in registry_deserialization_block:
        fail(
            "Unzulässiger Inhalt in der "
            "Zyklusregister-Deserialisierung: "
            f"{forbidden}"
        )


if text.count(
    "function mapParticipantFullExamResultHistorySnapshotPersistenceCycleRegistryContract(input)"
) != 1:
    fail(
        "Persistenz-Zyklusregister-Vertrag muss genau "
        "einmal vorhanden sein."
    )

registry_contract_start = lower.index(
    "function mapparticipantfullexamresulthistorysnapshotpersistencecycleregistrycontract(input)"
)
registry_deserialization_start = lower.index(
    "function mapparticipantfullexamresulthistorysnapshotpersistencecycleregistrydeserializationstate(input)",
    registry_contract_start,
)
registry_contract_block = lower[
    registry_contract_start:
    registry_deserialization_start
]

for required in (
    "object.getownpropertydescriptor(",
    "object.prototype.hasownproperty.call(",
    "getparticipantfullexamresulthistorysnapshotutf8bytelength(",
    "mapparticipantfullexamresulthistorysnapshotpersistencecycleregistrydeserializationstate({",
    "const contractversion = 1",
    '"accaoui:exam_history:persistence_cycle_registry"',
    '"exam_history_persistence_cycle_registry:v1"',
    "persistence_cycle_registry_contract_intent_missing",
    "persistence_cycle_registry_contract_intent_accessor_not_allowed",
    "persistence_cycle_registry_contract_intent_invalid",
    "persistence_cycle_registry_contract_serialization_state_missing",
    "persistence_cycle_registry_contract_serialization_state_invalid",
    "persistence_cycle_registry_contract_serialization_size_mismatch",
    "persistence_cycle_registry_contract_serialization_round_trip_invalid",
    "persistence_cycle_registry_contract_serialization_unexpected",
    "exam_result_history_persistence_cycle_registry_contract_save_ready",
    "exam_result_history_persistence_cycle_registry_contract_load_ready",
    "exam_result_history_persistence_cycle_registry_contract_delete_ready",
    "exam_result_history_persistence_cycle_registry_contract_invalid",
    "issnapshotpersistencecycleregistrycontractonly: true",
    "canpreparesave:",
    "canprepareload:",
    "canpreparedelete:",
    "canpersistlater: true",
    "canexecutestorage: false",
):
    if required not in registry_contract_block:
        fail(
            "Persistenz-Zyklusregister-Vertragsanweisung "
            f"fehlt: {required}"
        )

for forbidden in (
    ".rpc(",
    "createclient(",
    "window.supabase",
    "fetch(",
    "xmlhttprequest",
    "participant_id",
    "service_role",
    "date.now(",
    "math.random(",
    "crypto.",
    "...source",
    "...input",
    "localstorage",
    "sessionstorage",
    "indexeddb",
    "document.cookie",
    "storageadapter.read(",
    "storageadapter.write(",
    "storageadapter.delete(",
    ".setitem(",
    ".getitem(",
    ".removeitem(",
):
    if forbidden in registry_contract_block:
        fail(
            "Unzulässiger Inhalt im "
            "Zyklusregister-Vertrag: "
            f"{forbidden}"
        )


if text.count(
    "function mapParticipantFullExamResultHistorySnapshotPersistenceCycleRegistryStorageAdapterReadinessState(input)"
) != 1:
    fail(
        "Persistenz-Zyklusregister-Storage-Adapter-Readiness-"
        "State muss genau einmal vorhanden sein."
    )

registry_readiness_start = lower.index(
    "function mapparticipantfullexamresulthistorysnapshotpersistencecycleregistrystorageadapterreadinessstate(input)"
)
registry_contract_start = lower.index(
    "function mapparticipantfullexamresulthistorysnapshotpersistencecycleregistrycontract(input)",
    registry_readiness_start,
)
registry_readiness_block = lower[
    registry_readiness_start:
    registry_contract_start
]

for required in (
    "object.getownpropertydescriptor(",
    "object.prototype.hasownproperty.call(",
    "const readinessversion = 1",
    '"own_data_methods_only"',
    'const capabilitynames = [',
    '"read"',
    '"write"',
    '"delete"',
    "typeof property.value !==",
    "availablecapabilities.push(",
    "unavailablecapabilities.push(",
    "persistence_cycle_registry_storage_adapter_missing",
    "persistence_cycle_registry_storage_adapter_accessor_not_allowed",
    "persistence_cycle_registry_storage_adapter_invalid",
    "_accessor_not_allowed",
    "_method_invalid",
    "exam_result_history_persistence_cycle_registry_storage_adapter_ready",
    "exam_result_history_persistence_cycle_registry_storage_adapter_partial",
    "exam_result_history_persistence_cycle_registry_storage_adapter_unavailable",
    "exam_result_history_persistence_cycle_registry_storage_adapter_invalid",
    "exam_history_persistence_cycle_registry_storage_adapter_readiness:v1:",
    "issnapshotpersistencecycleregistrystorageadapterreadinessmapperonly: true",
    "canuseadapter",
    "isfullyready",
    "canprepareread:",
    "canpreparewrite:",
    "canpreparedelete:",
    "canexecutestorage: false",
):
    if required not in registry_readiness_block:
        fail(
            "Persistenz-Zyklusregister-Storage-Adapter-"
            f"Readiness-Anweisung fehlt: {required}"
        )

for forbidden in (
    ".rpc(",
    "createclient(",
    "window.supabase",
    "fetch(",
    "xmlhttprequest",
    "participant_id",
    "service_role",
    "date.now(",
    "math.random(",
    "crypto.",
    "...source",
    "...input",
    "localstorage",
    "sessionstorage",
    "indexeddb",
    "document.cookie",
    "storageadapter.read(",
    "storageadapter.write(",
    "storageadapter.delete(",
    "property.value(",
    ".setitem(",
    ".getitem(",
    ".removeitem(",
):
    if forbidden in registry_readiness_block:
        fail(
            "Unzulässiger Inhalt im Zyklusregister-"
            "Storage-Adapter-Readiness-State: "
            f"{forbidden}"
        )


if text.count(
    "function mapParticipantFullExamResultHistorySnapshotPersistenceCycleRegistryOperationPlanState(input)"
) != 1:
    fail(
        "Persistenz-Zyklusregister-Operationsplan-State muss "
        "genau einmal vorhanden sein."
    )

registry_operation_plan_start = lower.index(
    "function mapparticipantfullexamresulthistorysnapshotpersistencecycleregistryoperationplanstate(input)"
)
registry_readiness_start = lower.index(
    "function mapparticipantfullexamresulthistorysnapshotpersistencecycleregistrystorageadapterreadinessstate(input)",
    registry_operation_plan_start,
)
registry_operation_plan_block = lower[
    registry_operation_plan_start:
    registry_readiness_start
]

for required in (
    "object.getownpropertydescriptor(",
    "object.prototype.hasownproperty.call(",
    "object.keys(",
    "json.stringify(",
    "getparticipantfullexamresulthistorysnapshotutf8bytelength(",
    "mapparticipantfullexamresulthistorysnapshotpersistencecycleregistrydeserializationstate({",
    "const operationplanversion = 1",
    "persistence_cycle_registry_operation_plan_contract_missing",
    "persistence_cycle_registry_operation_plan_readiness_missing",
    "persistence_cycle_registry_operation_plan_contract_invalid",
    "persistence_cycle_registry_operation_plan_save_payload_invalid",
    "persistence_cycle_registry_operation_plan_save_size_mismatch",
    "persistence_cycle_registry_operation_plan_save_round_trip_invalid",
    "persistence_cycle_registry_operation_plan_payload_unexpected",
    "persistence_cycle_registry_operation_plan_readiness_invalid",
    "persistence_cycle_registry_operation_plan_capability_unavailable",
    "exam_result_history_persistence_cycle_registry_operation_plan_ready",
    "exam_result_history_persistence_cycle_registry_operation_plan_blocked",
    "exam_result_history_persistence_cycle_registry_operation_plan_invalid",
    "exam_history_persistence_cycle_registry_operation_plan:",
    "issnapshotpersistencecycleregistryoperationplanmapperonly: true",
    "canprepareoperation",
    "caninvokelater:",
    "iscapabilityavailable",
    "canplansave:",
    "canplanload:",
    "canplandelete:",
    "canexecutestorage: false",
):
    if required not in registry_operation_plan_block:
        fail(
            "Persistenz-Zyklusregister-Operationsplan-"
            f"Anweisung fehlt: {required}"
        )

for forbidden in (
    ".rpc(",
    "createclient(",
    "window.supabase",
    "fetch(",
    "xmlhttprequest",
    "participant_id",
    "service_role",
    "date.now(",
    "math.random(",
    "crypto.",
    "...source",
    "...input",
    "localstorage",
    "sessionstorage",
    "indexeddb",
    "document.cookie",
    "storageadapter.read(",
    "storageadapter.write(",
    "storageadapter.delete(",
    "property.value(",
    ".setitem(",
    ".getitem(",
    ".removeitem(",
):
    if forbidden in registry_operation_plan_block:
        fail(
            "Unzulässiger Inhalt im Zyklusregister-"
            "Operationsplan-State: "
            f"{forbidden}"
        )


if text.count(
    "function mapParticipantFullExamResultHistorySnapshotPersistenceCycleRegistryOperationReleaseState(input)"
) != 1:
    fail(
        "Persistenz-Zyklusregister-Operationsfreigabe-State "
        "muss genau einmal vorhanden sein."
    )

registry_operation_release_start = lower.index(
    "function mapparticipantfullexamresulthistorysnapshotpersistencecycleregistryoperationreleasestate(input)"
)
registry_operation_plan_start = lower.index(
    "function mapparticipantfullexamresulthistorysnapshotpersistencecycleregistryoperationplanstate(input)",
    registry_operation_release_start,
)
registry_operation_release_block = lower[
    registry_operation_release_start:
    registry_operation_plan_start
]

for required in (
    "object.getownpropertydescriptor(",
    "object.prototype.hasownproperty.call(",
    "getparticipantfullexamresulthistorysnapshotutf8bytelength(",
    "mapparticipantfullexamresulthistorysnapshotpersistencecycleregistrydeserializationstate({",
    "mapparticipantfullexamresulthistorysnapshotpersistencecycleregistrystorageadapterreadinessstate({",
    "const operationreleaseversion = 1",
    "persistence_cycle_registry_operation_release_plan_missing",
    "persistence_cycle_registry_operation_release_adapter_missing",
    "persistence_cycle_registry_operation_release_plan_invalid",
    "persistence_cycle_registry_operation_release_save_payload_invalid",
    "persistence_cycle_registry_operation_release_save_size_mismatch",
    "persistence_cycle_registry_operation_release_save_round_trip_invalid",
    "persistence_cycle_registry_operation_release_payload_unexpected",
    "persistence_cycle_registry_operation_release_adapter_readiness_invalid",
    "persistence_cycle_registry_operation_release_readiness_mismatch",
    "persistence_cycle_registry_operation_release_plan_state_invalid",
    "persistence_cycle_registry_operation_release_capability_unavailable",
    "persistence_cycle_registry_operation_release_method_invalid",
    "exam_result_history_persistence_cycle_registry_operation_release_ready",
    "exam_result_history_persistence_cycle_registry_operation_release_blocked",
    "exam_result_history_persistence_cycle_registry_operation_release_invalid",
    "exam_history_persistence_cycle_registry_operation_release:",
    "issnapshotpersistencecycleregistryoperationreleasemapperonly: true",
    "canreleaseoperation",
    "caninvokelater:",
    "ismethodreferencevalidated",
    "canreleasesave:",
    "canreleaseload:",
    "canreleasedelete:",
    "canexecutestorage: false",
):
    if required not in registry_operation_release_block:
        fail(
            "Persistenz-Zyklusregister-Operationsfreigabe-"
            f"Anweisung fehlt: {required}"
        )

for forbidden in (
    ".rpc(",
    "createclient(",
    "window.supabase",
    "fetch(",
    "xmlhttprequest",
    "participant_id",
    "service_role",
    "date.now(",
    "math.random(",
    "crypto.",
    "...source",
    "...input",
    "localstorage",
    "sessionstorage",
    "indexeddb",
    "document.cookie",
    "storageadapter.read(",
    "storageadapter.write(",
    "storageadapter.delete(",
    "methodproperty.value(",
    ".setitem(",
    ".getitem(",
    ".removeitem(",
):
    if forbidden in registry_operation_release_block:
        fail(
            "Unzulässiger Inhalt im Zyklusregister-"
            "Operationsfreigabe-State: "
            f"{forbidden}"
        )


if text.count(
    "function guardParticipantFullExamResultHistorySnapshotPersistenceCycleRegistryExecution(input)"
) != 1:
    fail(
        "Persistenz-Zyklusregister-Ausführungs-Guard muss "
        "genau einmal vorhanden sein."
    )

registry_execution_start = lower.index(
    "function guardparticipantfullexamresulthistorysnapshotpersistencecycleregistryexecution(input)"
)
registry_operation_release_start = lower.index(
    "function mapparticipantfullexamresulthistorysnapshotpersistencecycleregistryoperationreleasestate(input)",
    registry_execution_start,
)
registry_execution_block = lower[
    registry_execution_start:
    registry_operation_release_start
]

for required in (
    "object.getownpropertydescriptor(",
    "object.prototype.hasownproperty.call(",
    "getparticipantfullexamresulthistorysnapshotutf8bytelength(",
    "mapparticipantfullexamresulthistorysnapshotpersistencecycleregistrydeserializationstate({",
    "mapparticipantfullexamresulthistorysnapshotpersistencecycleregistrystorageadapterreadinessstate({",
    "const executionguardversion = 1",
    "persistence_cycle_registry_execution_guard_release_missing",
    "persistence_cycle_registry_execution_guard_adapter_missing",
    "persistence_cycle_registry_execution_guard_release_invalid",
    "persistence_cycle_registry_execution_guard_save_payload_invalid",
    "persistence_cycle_registry_execution_guard_save_size_mismatch",
    "persistence_cycle_registry_execution_guard_save_round_trip_invalid",
    "persistence_cycle_registry_execution_guard_payload_unexpected",
    "persistence_cycle_registry_execution_guard_adapter_readiness_invalid",
    "persistence_cycle_registry_execution_guard_readiness_mismatch",
    "persistence_cycle_registry_execution_guard_release_state_invalid",
    "persistence_cycle_registry_execution_guard_capability_unavailable",
    "persistence_cycle_registry_execution_guard_method_invalid",
    "exam_result_history_persistence_cycle_registry_execution_guard_ready",
    "exam_result_history_persistence_cycle_registry_execution_guard_blocked",
    "exam_result_history_persistence_cycle_registry_execution_guard_invalid",
    "exam_history_persistence_cycle_registry_execution_guard:",
    "issnapshotpersistencecycleregistryexecutionguardonly: true",
    "canproceedtoinvocation",
    "caninvokelater:",
    "isexecutionboundaryvalidated",
    "ismethodreferencevalidated",
    "canguardsave:",
    "canguardload:",
    "canguarddelete:",
    "canexecutestorage: false",
):
    if required not in registry_execution_block:
        fail(
            "Persistenz-Zyklusregister-Ausführungs-"
            f"Anweisung fehlt: {required}"
        )

for forbidden in (
    ".rpc(",
    "createclient(",
    "window.supabase",
    "fetch(",
    "xmlhttprequest",
    "participant_id",
    "service_role",
    "date.now(",
    "math.random(",
    "crypto.",
    "...source",
    "...input",
    "localstorage",
    "sessionstorage",
    "indexeddb",
    "document.cookie",
    "storageadapter.read(",
    "storageadapter.write(",
    "storageadapter.delete(",
    "methodproperty.value(",
    ".setitem(",
    ".getitem(",
    ".removeitem(",
):
    if forbidden in registry_execution_block:
        fail(
            "Unzulässiger Inhalt im Zyklusregister-"
            "Ausführungs-Guard: "
            f"{forbidden}"
        )


if text.count(
    "function mapParticipantFullExamResultHistorySnapshotPersistenceCycleRegistryInvocationContract(input)"
) != 1:
    fail(
        "Persistenz-Zyklusregister-Aufrufvertrag muss "
        "genau einmal vorhanden sein."
    )

registry_invocation_contract_start = lower.index(
    "function mapparticipantfullexamresulthistorysnapshotpersistencecycleregistryinvocationcontract(input)"
)
registry_execution_start = lower.index(
    "function guardparticipantfullexamresulthistorysnapshotpersistencecycleregistryexecution(input)",
    registry_invocation_contract_start,
)
registry_invocation_contract_block = lower[
    registry_invocation_contract_start:
    registry_execution_start
]

for required in (
    "object.getownpropertydescriptor(",
    "object.prototype.hasownproperty.call(",
    "getparticipantfullexamresulthistorysnapshotutf8bytelength(",
    "mapparticipantfullexamresulthistorysnapshotpersistencecycleregistrydeserializationstate({",
    "const invocationcontractversion = 1",
    "persistence_cycle_registry_invocation_contract_execution_guard_missing",
    "persistence_cycle_registry_invocation_contract_execution_guard_invalid",
    "persistence_cycle_registry_invocation_contract_readiness_invalid",
    "persistence_cycle_registry_invocation_contract_save_payload_invalid",
    "persistence_cycle_registry_invocation_contract_save_size_mismatch",
    "persistence_cycle_registry_invocation_contract_save_round_trip_invalid",
    "persistence_cycle_registry_invocation_contract_payload_unexpected",
    "persistence_cycle_registry_invocation_contract_execution_guard_state_invalid",
    "persistence_cycle_registry_invocation_contract_capability_mismatch",
    "persistence_cycle_registry_invocation_contract_capability_unavailable",
    "persistence_cycle_registry_invocation_contract_arguments_invalid",
    "exam_result_history_persistence_cycle_registry_invocation_contract_ready",
    "exam_result_history_persistence_cycle_registry_invocation_contract_blocked",
    "exam_result_history_persistence_cycle_registry_invocation_contract_invalid",
    "exam_history_persistence_cycle_registry_invocation_contract:",
    "issnapshotpersistencecycleregistryinvocationcontractonly: true",
    "canprepareinvocation",
    "caninvokelater:",
    "isinvocationshapevalidated",
    "invocationargumentcount:",
    "invocationarguments",
    "canpreparesave:",
    "canprepareload:",
    "canpreparedelete:",
    "canexecutestorage: false",
):
    if required not in registry_invocation_contract_block:
        fail(
            "Persistenz-Zyklusregister-Aufrufvertrags-"
            f"Anweisung fehlt: {required}"
        )

for forbidden in (
    ".rpc(",
    "createclient(",
    "window.supabase",
    "fetch(",
    "xmlhttprequest",
    "participant_id",
    "service_role",
    "date.now(",
    "math.random(",
    "crypto.",
    "...source",
    "...input",
    "localstorage",
    "sessionstorage",
    "indexeddb",
    "document.cookie",
    "storageadapter.read(",
    "storageadapter.write(",
    "storageadapter.delete(",
    ".setitem(",
    ".getitem(",
    ".removeitem(",
):
    if forbidden in registry_invocation_contract_block:
        fail(
            "Unzulässiger Inhalt im Zyklusregister-"
            "Aufrufvertrag: "
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
print("Snapshot-Wiederaufnahme: nur normalisierte Zustände rekonstruiert")
print("Snapshot-Erstellung: nur wiederaufnehmbare Zustände datensparsam versioniert")
print("Snapshot-Serialisierung: kanonisches JSON, Größenlimit und Strukturprüfung")
print("Snapshot-Deserialisierung: Größe vor Parsing begrenzt und Struktur erneut geprüft")
print("Snapshot-Persistenzvertrag: Save, Load und Delete sicher vorbereitet")
print("Persistenz-Adapter-Readiness: Read, Write und Delete ohne Aufruf geprüft")
print("Persistenz-Operationsplan: Vertrag und Adapterfähigkeit ohne Aufruf verbunden")
print("Persistenz-Operationsfreigabe: unveränderte Readiness und Plan erneut geprüft")
print("Persistenz-Ausführungs-Guard: Adapter und Methode ohne Aufruf erneut geprüft")
print("Persistenz-Aufrufvertrag: kanonisches Methoden- und Argumenteschema erstellt")
print("Persistenz-Aufrufpaket: Guard, Vertrag und Adapter erneut geschlossen verbunden")
print("Persistenz-Ergebnisvertrag: Read, Write und Delete getrennt normalisiert")
print("Persistenz-Ergebnisannahme: nur Ergebnisse des aktuellen Aufrufpakets akzeptiert")
print("Persistenz-Abschlussstate: angenommene Ergebnisse terminal und sicher abgeschlossen")
print("Persistenz-Zyklusstate: Aufrufpaket bis Abschluss zusammenhängend geprüft")
print("Persistenz-Zyklus-Wiederholung: doppelte terminale Ergebnisse blockiert")
print("Persistenz-Zyklusregister: begrenzte Identitäten kanonisch normalisiert")
print("Persistenz-Zyklusregister-Serialisierung: kanonisches JSON größenbegrenzt erstellt")
print("Persistenz-Zyklusregister-Deserialisierung: Größe vor Parsing begrenzt und Register rekonstruiert")
print("Persistenz-Zyklusregister-Vertrag: Save, Load und Delete im eigenen Namensraum vorbereitet")
print("Persistenz-Zyklusregister-Adapter-Readiness: nur eigene Datenmethoden geprüft")
print("Persistenz-Zyklusregister-Operationsplan: Save, Load und Delete mit Adapterfähigkeiten verbunden")
print("Persistenz-Zyklusregister-Operationsfreigabe: Operationsplan mit derselben Adapter-Readiness verbunden")
print("Persistenz-Zyklusregister-Ausführungs-Guard: Freigabe unmittelbar vor späterem Aufruf erneut geprüft")
print("Persistenz-Zyklusregister-Aufrufvertrag: kanonische Read-, Write- und Delete-Argumente erstellt")
print("Rohe RPC-Fehlerdetails: werden nicht übernommen")
print("Globale Bestanden-/Nicht-bestanden-Zahlen: bewusst nicht abgeleitet")
print("Private Prüfungsfelder in Normalizer: ausgeschlossen")
print("Sichtbare Prüfungshistorie: unverändert verborgen")
print("Lokaler Modus: sicher und nicht blockierend")
