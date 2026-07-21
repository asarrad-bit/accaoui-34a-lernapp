"use strict";

// Accaoui §34a Lern-App
// Lokale Prüfungshistorie-Fixtures
// Stand: v27.30h

const fs = require("fs");
const path = require("path");
const vm = require("vm");

function fail(message) {
  console.error(`FEHLER: ${message}`);
  process.exit(1);
}

function assert(condition, message) {
  if (!condition) {
    fail(message);
  }
}

function expectEqual(actual, expected, message) {
  if (actual !== expected) {
    fail(
      `${message}: erwartet ${JSON.stringify(expected)}, ` +
      `erhalten ${JSON.stringify(actual)}`
    );
  }
}

function expectJson(actual, expected, message) {
  if (JSON.stringify(actual) !== JSON.stringify(expected)) {
    fail(
      `${message}: erwartet ${JSON.stringify(expected)}, ` +
      `erhalten ${JSON.stringify(actual)}`
    );
  }
}

const root = path.resolve(__dirname, "..");
const adapterPath = path.join(
  root,
  "data",
  "supabase-client-adapter.js"
);

const source = fs.readFileSync(
  adapterPath,
  "utf8"
);

const windowMock = {
  ACCAOUI_SUPABASE_LIVE_ENABLED: false
};

Object.defineProperty(
  windowMock,
  "supabase",
  {
    configurable: false,
    get() {
      throw new Error(
        "Fixture-Test darf Supabase nicht aufrufen."
      );
    }
  }
);

const context = {
  window: windowMock,
  console: {
    info() {},
    log() {},
    warn() {},
    error() {}
  },
  fetch() {
    throw new Error(
      "Fixture-Test darf kein Netzwerk aufrufen."
    );
  },
  XMLHttpRequest: class {
    constructor() {
      throw new Error(
        "Fixture-Test darf kein XMLHttpRequest verwenden."
      );
    }
  }
};

vm.createContext(context);

try {
  vm.runInContext(
    source,
    context,
    {
      filename: adapterPath
    }
  );
} catch (error) {
  fail(`Adapter konnte nicht geladen werden: ${error.message}`);
}

const adapter =
  windowMock.ACCAOUI_SUPABASE_ADAPTER;

assert(
  adapter &&
  typeof adapter === "object",
  "Öffentlicher Adapter fehlt"
);

expectEqual(
  adapter.version,
  "v27.30h",
  "Adapterversion"
);

for (const functionName of [
  "normalizeParticipantFullExamResultRow",
  "normalizeParticipantFullExamResultRows",
  "aggregateParticipantFullExamResultRows",
  "mapParticipantFullExamResultHistoryResponse",
  "mapParticipantFullExamResultHistoryLoadState",
  "mapParticipantFullExamResultHistoryPaginationState",
  "orchestrateParticipantFullExamResultHistoryDataSourceState",
  "mapParticipantFullExamResultHistoryNavigationIntent",
  "mapParticipantFullExamResultHistoryRequestIdentity",
  "mapParticipantFullExamResultHistoryRequestLifecycle",
  "mapParticipantFullExamResultHistoryRequestControllerState",
  "normalizeParticipantFullExamResultHistoryControllerSnapshot",
  "mapParticipantFullExamResultHistorySnapshotResumeState",
  "mapParticipantFullExamResultHistorySnapshotCreationState",
  "mapParticipantFullExamResultHistorySnapshotSerializationState",
  "mapParticipantFullExamResultHistorySnapshotDeserializationState",
  "mapParticipantFullExamResultHistorySnapshotPersistenceContract",
  "mapParticipantFullExamResultHistorySnapshotStorageAdapterReadiness",
  "mapParticipantFullExamResultHistorySnapshotPersistenceOperationPlan",
  "mapParticipantFullExamResultHistorySnapshotPersistenceOperationReleaseState",
  "guardParticipantFullExamResultHistorySnapshotPersistenceExecution",
  "mapParticipantFullExamResultHistorySnapshotPersistenceInvocationContract",
  "mapParticipantFullExamResultHistorySnapshotPersistenceInvocationPackageState",
  "mapParticipantFullExamResultHistorySnapshotPersistenceResultContract",
  "guardParticipantFullExamResultHistorySnapshotPersistenceResultAcceptance",
  "mapParticipantFullExamResultHistorySnapshotPersistenceCompletionState",
  "mapParticipantFullExamResultHistorySnapshotPersistenceCycleState",
  "guardParticipantFullExamResultHistorySnapshotPersistenceCycleRepetition",
  "guardParticipantFullExamResultHistoryRequestLifecycleTransition",
  "guardParticipantFullExamResultHistoryResponseAcceptance"
]) {
  assert(
    typeof adapter[functionName] === "function",
    `Adapterfunktion fehlt: ${functionName}`
  );
}

function makeRow(overrides = {}) {
  return {
    exam_attempt_id:
      "11111111-1111-4111-8111-111111111111",
    course_id:
      "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa",
    course_title: "Sachkunde §34a",
    score_points: 90,
    max_points: 120,
    passed: true,
    started_at: "2026-07-17T08:00:00.000Z",
    finished_at: "2026-07-17T09:30:00.000Z",
    total_count: "2",
    ...overrides
  };
}

const firstRow = makeRow({
  correct_answers: 77,
  selected_answers: [0, 1],
  unknown_private_field: "nicht übernehmen"
});

const secondRow = makeRow({
  exam_attempt_id:
    "22222222-2222-4222-8222-222222222222",
  course_id: null,
  course_title: null,
  score_points: 30,
  passed: false,
  started_at: "2026-07-18T08:00:00.000Z",
  finished_at: "2026-07-18T09:00:00.000Z"
});

const normalizedRow =
  adapter.normalizeParticipantFullExamResultRow(
    firstRow
  );

assert(
  normalizedRow.isValid === true,
  "Gültige Ergebniszeile wurde abgelehnt"
);

expectEqual(
  normalizedRow.entry.totalCount,
  2,
  "total_count-Zeichenkette wurde nicht normalisiert"
);

expectJson(
  Object.keys(normalizedRow.entry).sort(),
  [
    "courseId",
    "courseTitle",
    "examAttemptId",
    "finishedAt",
    "maxPoints",
    "passed",
    "scorePoints",
    "startedAt",
    "totalCount"
  ].sort(),
  "Erlaubte Ergebnisfelder"
);

assert(
  !Object.prototype.hasOwnProperty.call(
    normalizedRow.entry,
    "correctAnswers"
  ),
  "Private Antwortzahl wurde übernommen"
);

const invalidPassed =
  adapter.normalizeParticipantFullExamResultRow(
    makeRow({
      passed: false
    })
  );

expectEqual(
  invalidPassed.reason,
  "passed_status_invalid",
  "Ungültiger Bestehensstatus"
);

const invalidMaxPoints =
  adapter.normalizeParticipantFullExamResultRow(
    makeRow({
      max_points: 119
    })
  );

expectEqual(
  invalidMaxPoints.reason,
  "max_points_must_equal_120",
  "Ungültige Maximalpunkte"
);

const normalizedList =
  adapter.normalizeParticipantFullExamResultRows(
    [firstRow, secondRow]
  );

assert(
  normalizedList.isValid === true,
  "Gültige Ergebnisliste wurde abgelehnt"
);

expectEqual(
  normalizedList.entries.length,
  2,
  "Anzahl normalisierter Ergebniszeilen"
);

expectEqual(
  normalizedList.totalCount,
  2,
  "Normalisierte Gesamtzahl"
);

const duplicateList =
  adapter.normalizeParticipantFullExamResultRows(
    [
      firstRow,
      makeRow({
        exam_attempt_id:
          firstRow.exam_attempt_id,
        score_points: 30,
        passed: false
      })
    ]
  );

expectEqual(
  duplicateList.reason,
  "duplicate_exam_attempt_id",
  "Doppelte Prüfungsversuchs-ID"
);

const inconsistentTotal =
  adapter.normalizeParticipantFullExamResultRows(
    [
      firstRow,
      {
        ...secondRow,
        total_count: 3
      }
    ]
  );

expectEqual(
  inconsistentTotal.reason,
  "total_count_inconsistent",
  "Inkonsistentes total_count"
);

const smallerTotal =
  adapter.normalizeParticipantFullExamResultRows(
    [
      {
        ...firstRow,
        total_count: 1
      },
      {
        ...secondRow,
        total_count: 1
      }
    ]
  );

expectEqual(
  smallerTotal.reason,
  "total_count_smaller_than_rows",
  "Zu kleines total_count"
);

const emptyList =
  adapter.normalizeParticipantFullExamResultRows(
    []
  );

assert(
  emptyList.isValid === true &&
  emptyList.isEmpty === true &&
  emptyList.entries.length === 0 &&
  emptyList.totalCount === null,
  "Leere Ergebnisliste ist nicht stabil"
);

const aggregate =
  adapter.aggregateParticipantFullExamResultRows(
    [firstRow, secondRow]
  );

assert(
  aggregate.isValid === true,
  "Gültige Ergebnisliste konnte nicht aggregiert werden"
);

expectEqual(
  aggregate.metricsScope,
  "page_only",
  "Kennzahlenumfang"
);

expectEqual(
  aggregate.pageEntryCount,
  2,
  "Seitenanzahl"
);

expectEqual(
  aggregate.pagePassedCount,
  1,
  "Bestandene Seiteneinträge"
);

expectEqual(
  aggregate.pageFailedCount,
  1,
  "Nicht bestandene Seiteneinträge"
);

expectEqual(
  aggregate.pageBestScore,
  90,
  "Seitenbestwert"
);

expectEqual(
  aggregate.pageAverageScore,
  60,
  "Seitendurchschnitt"
);

expectEqual(
  aggregate.pagePassRatePercent,
  50,
  "Seitenbestehensquote"
);

expectEqual(
  aggregate.pageLatestExamAttemptId,
  secondRow.exam_attempt_id,
  "Neuester Seiteneintrag"
);

assert(
  aggregate.canPopulateGlobalOutcomeCounts === false &&
  aggregate.globalPassedCount === null &&
  aggregate.globalFailedCount === null,
  "Globale Werte wurden unzulässig aus Pagination abgeleitet"
);

const emptyAggregate =
  adapter.aggregateParticipantFullExamResultRows(
    []
  );

assert(
  emptyAggregate.isValid === true &&
  emptyAggregate.isEmpty === true &&
  emptyAggregate.pageBestScore === null &&
  emptyAggregate.pageAverageScore === null,
  "Leerer Aggregatorzustand ist nicht stabil"
);

const invalidAggregate =
  adapter.aggregateParticipantFullExamResultRows(
    [
      makeRow({
        passed: false
      })
    ]
  );

assert(
  invalidAggregate.isValid === false &&
  invalidAggregate.entries.length === 0 &&
  invalidAggregate.reason ===
    "passed_status_invalid",
  "Ungültige Liste wurde nicht geschlossen verworfen"
);

const mappedSuccess =
  adapter.mapParticipantFullExamResultHistoryResponse({
    data: [firstRow, secondRow],
    error: null,
    privateTransportField: "nicht übernehmen"
  });

assert(
  mappedSuccess.ok === true &&
  mappedSuccess.isEmpty === false,
  "Gültige RPC-Antwort wurde nicht gemappt"
);

expectEqual(
  mappedSuccess.status,
  "exam_result_history_response_ready",
  "Response-Mapper-Erfolgsstatus"
);

expectEqual(
  mappedSuccess.results.length,
  2,
  "Gemappte Ergebnisanzahl"
);

expectEqual(
  mappedSuccess.totalCount,
  2,
  "Gemappte Gesamtzahl"
);

expectEqual(
  mappedSuccess.pageMetrics.pageAverageScore,
  60,
  "Gemappter Seitendurchschnitt"
);

assert(
  !Object.prototype.hasOwnProperty.call(
    mappedSuccess,
    "privateTransportField"
  ),
  "Unbekanntes Transportfeld wurde übernommen"
);

const mappedEmpty =
  adapter.mapParticipantFullExamResultHistoryResponse({
    data: [],
    error: null
  });

assert(
  mappedEmpty.ok === true &&
  mappedEmpty.isEmpty === true &&
  mappedEmpty.results.length === 0,
  "Leere RPC-Antwort ist nicht stabil"
);

const mappedInvalid =
  adapter.mapParticipantFullExamResultHistoryResponse({
    data: [
      makeRow({
        passed: false
      })
    ],
    error: null
  });

expectEqual(
  mappedInvalid.reason,
  "passed_status_invalid",
  "Ungültige RPC-Ergebniszeile"
);

expectEqual(
  mappedInvalid.invalidIndex,
  0,
  "Ungültiger Zeilenindex"
);

const mappedError =
  adapter.mapParticipantFullExamResultHistoryResponse({
    data: null,
    error: {
      message: "sensitive database message",
      details: "sensitive database details",
      hint: "sensitive database hint"
    }
  });

expectEqual(
  mappedError.status,
  "exam_result_history_response_error",
  "Sicherer RPC-Fehlerstatus"
);

expectEqual(
  mappedError.reason,
  "rpc_response_error",
  "Sicherer RPC-Fehlergrund"
);

assert(
  !JSON.stringify(mappedError).includes("sensitive"),
  "Rohe RPC-Fehlerdetails wurden offengelegt"
);

const mappedMalformed =
  adapter.mapParticipantFullExamResultHistoryResponse({
    data: {},
    error: null
  });

expectEqual(
  mappedMalformed.reason,
  "rpc_response_data_must_be_array",
  "Ungültige RPC-Datenstruktur"
);

const mappedNonObject =
  adapter.mapParticipantFullExamResultHistoryResponse(
    null
  );

expectEqual(
  mappedNonObject.reason,
  "rpc_response_must_be_object",
  "Ungültige RPC-Antwortstruktur"
);

const loadPrepared =
  adapter.mapParticipantFullExamResultHistoryLoadState({
    phase: "prepared"
  });

expectEqual(
  loadPrepared.status,
  "exam_result_history_load_prepared",
  "Vorbereiteter Ladezustand"
);

assert(
  loadPrepared.isPrepared === true &&
  loadPrepared.isLoading === false &&
  loadPrepared.hasError === false,
  "Vorbereiteter Ladezustand ist unstabil"
);

const loadLoading =
  adapter.mapParticipantFullExamResultHistoryLoadState({
    phase: "loading"
  });

assert(
  loadLoading.status ===
    "exam_result_history_load_loading" &&
  loadLoading.isLoading === true &&
  loadLoading.results.length === 0,
  "Aktiver Ladezustand ist unstabil"
);

const loadSuccess =
  adapter.mapParticipantFullExamResultHistoryLoadState({
    phase: "resolved",
    response: {
      data: [firstRow, secondRow],
      error: null
    }
  });

assert(
  loadSuccess.status ===
    "exam_result_history_load_success" &&
  loadSuccess.isSuccess === true &&
  loadSuccess.results.length === 2 &&
  loadSuccess.totalCount === 2,
  "Erfolgreicher Ladezustand ist unstabil"
);

expectEqual(
  loadSuccess.pageMetrics.pageAverageScore,
  60,
  "Ladezustands-Seitendurchschnitt"
);

const loadEmpty =
  adapter.mapParticipantFullExamResultHistoryLoadState({
    phase: "resolved",
    response: {
      data: [],
      error: null
    }
  });

assert(
  loadEmpty.status ===
    "exam_result_history_load_empty" &&
  loadEmpty.isSuccess === true &&
  loadEmpty.isEmpty === true &&
  loadEmpty.results.length === 0,
  "Leerer Ladezustand ist unstabil"
);

const loadInvalidResponse =
  adapter.mapParticipantFullExamResultHistoryLoadState({
    phase: "resolved",
    response: {
      data: [
        makeRow({
          passed: false
        })
      ],
      error: null
    }
  });

assert(
  loadInvalidResponse.status ===
    "exam_result_history_load_error" &&
  loadInvalidResponse.hasError === true &&
  loadInvalidResponse.canRetry === true &&
  loadInvalidResponse.reason ===
    "passed_status_invalid" &&
  loadInvalidResponse.invalidIndex === 0,
  "Ungültige Ergebnisdaten wurden nicht sicher gemappt"
);

const loadRejected =
  adapter.mapParticipantFullExamResultHistoryLoadState({
    phase: "rejected",
    error: {
      message: "sensitive request message",
      details: "sensitive request details"
    }
  });

assert(
  loadRejected.status ===
    "exam_result_history_load_error" &&
  loadRejected.hasError === true &&
  loadRejected.canRetry === true &&
  loadRejected.reason ===
    "rpc_request_failed",
  "Abgelehnter Ladezustand ist unstabil"
);

assert(
  !JSON.stringify(loadRejected).includes("sensitive"),
  "Rohe Ladefehlerdetails wurden offengelegt"
);

const loadInvalidPhase =
  adapter.mapParticipantFullExamResultHistoryLoadState({
    phase: "unknown"
  });

assert(
  loadInvalidPhase.status ===
    "exam_result_history_load_error" &&
  loadInvalidPhase.hasError === true &&
  loadInvalidPhase.canRetry === false &&
  loadInvalidPhase.reason ===
    "load_phase_invalid",
  "Ungültige Ladephase wurde nicht geschlossen verworfen"
);

const paginationPrepared =
  adapter.mapParticipantFullExamResultHistoryPaginationState({
    limit: 20,
    offset: 20,
    totalCount: null,
    pageEntryCount: 0
  });

assert(
  paginationPrepared.status ===
    "exam_result_history_pagination_prepared" &&
  paginationPrepared.currentPage === 2 &&
  paginationPrepared.canGoPrevious === true &&
  paginationPrepared.previousOffset === 0 &&
  paginationPrepared.canGoNext === false,
  "Pagination mit unbekannter Gesamtzahl ist unstabil"
);

const paginationFirst =
  adapter.mapParticipantFullExamResultHistoryPaginationState({
    limit: 20,
    offset: 0,
    totalCount: 45,
    pageEntryCount: 20
  });

assert(
  paginationFirst.status ===
    "exam_result_history_pagination_ready" &&
  paginationFirst.currentPage === 1 &&
  paginationFirst.totalPages === 3 &&
  paginationFirst.isFirstPage === true &&
  paginationFirst.canGoPrevious === false &&
  paginationFirst.canGoNext === true &&
  paginationFirst.nextOffset === 20,
  "Erste Pagination-Seite ist unstabil"
);

const paginationMiddle =
  adapter.mapParticipantFullExamResultHistoryPaginationState({
    limit: 20,
    offset: 20,
    totalCount: 45,
    pageEntryCount: 20
  });

assert(
  paginationMiddle.currentPage === 2 &&
  paginationMiddle.canGoPrevious === true &&
  paginationMiddle.previousOffset === 0 &&
  paginationMiddle.canGoNext === true &&
  paginationMiddle.nextOffset === 40,
  "Mittlere Pagination-Seite ist unstabil"
);

const paginationLast =
  adapter.mapParticipantFullExamResultHistoryPaginationState({
    limit: 20,
    offset: 40,
    totalCount: 45,
    pageEntryCount: 5
  });

assert(
  paginationLast.currentPage === 3 &&
  paginationLast.totalPages === 3 &&
  paginationLast.isLastPage === true &&
  paginationLast.canGoNext === false &&
  paginationLast.nextOffset === null,
  "Letzte Pagination-Seite ist unstabil"
);

const paginationEmpty =
  adapter.mapParticipantFullExamResultHistoryPaginationState({
    limit: 20,
    offset: 0,
    totalCount: 0,
    pageEntryCount: 0
  });

assert(
  paginationEmpty.status ===
    "exam_result_history_pagination_empty" &&
  paginationEmpty.currentPage === 0 &&
  paginationEmpty.totalPages === 0 &&
  paginationEmpty.isFirstPage === true &&
  paginationEmpty.isLastPage === true,
  "Leere Pagination ist unstabil"
);

const paginationMisaligned =
  adapter.mapParticipantFullExamResultHistoryPaginationState({
    limit: 20,
    offset: 10,
    totalCount: 45,
    pageEntryCount: 20
  });

expectEqual(
  paginationMisaligned.reason,
  "offset_must_align_to_limit",
  "Nicht ausgerichteter Offset"
);

const paginationInvalidCount =
  adapter.mapParticipantFullExamResultHistoryPaginationState({
    limit: 20,
    offset: 0,
    totalCount: 45,
    pageEntryCount: 21
  });

expectEqual(
  paginationInvalidCount.reason,
  "page_entry_count_invalid",
  "Ungültige Seiteneintragszahl"
);

const paginationCapped =
  adapter.mapParticipantFullExamResultHistoryPaginationState({
    limit: 50,
    offset: 10000,
    totalCount: 10051,
    pageEntryCount: 50
  });

assert(
  paginationCapped.isValid === true &&
  paginationCapped.isNavigationCapped === true &&
  paginationCapped.canGoNext === false &&
  paginationCapped.isLastPage === false &&
  paginationCapped.reason ===
    "maximum_offset_reached",
  "Maximaler Pagination-Offset ist unstabil"
);

const orchestratedPrepared =
  adapter.orchestrateParticipantFullExamResultHistoryDataSourceState({
    phase: "prepared",
    limit: 20,
    offset: 0
  });

assert(
  orchestratedPrepared.status ===
    "exam_result_history_data_source_prepared" &&
  orchestratedPrepared.isPrepared === true &&
  orchestratedPrepared.isLoading === false &&
  orchestratedPrepared.paginationState.status ===
    "exam_result_history_pagination_prepared",
  "Vorbereiteter Datenquellen-Gesamtzustand ist unstabil"
);

const orchestratedLoading =
  adapter.orchestrateParticipantFullExamResultHistoryDataSourceState({
    phase: "loading",
    limit: 20,
    offset: 20
  });

assert(
  orchestratedLoading.status ===
    "exam_result_history_data_source_loading" &&
  orchestratedLoading.isLoading === true &&
  orchestratedLoading.hasData === false &&
  orchestratedLoading.results.length === 0,
  "Ladender Datenquellen-Gesamtzustand ist unstabil"
);

const orchestratedSuccess =
  adapter.orchestrateParticipantFullExamResultHistoryDataSourceState({
    phase: "resolved",
    limit: 20,
    offset: 0,
    response: {
      data: [
        {
          ...firstRow,
          total_count: 45
        },
        {
          ...secondRow,
          total_count: 45
        }
      ],
      error: null
    }
  });

assert(
  orchestratedSuccess.status ===
    "exam_result_history_data_source_success" &&
  orchestratedSuccess.isSuccess === true &&
  orchestratedSuccess.hasData === true &&
  orchestratedSuccess.results.length === 2 &&
  orchestratedSuccess.totalCount === 45 &&
  orchestratedSuccess.paginationState.canGoNext === true &&
  orchestratedSuccess.paginationState.nextOffset === 20,
  "Erfolgreicher Datenquellen-Gesamtzustand ist unstabil"
);

assert(
  !Object.prototype.hasOwnProperty.call(
    orchestratedSuccess,
    "response"
  ),
  "Rohe RPC-Antwort wurde in den Gesamtzustand übernommen"
);

const orchestratedEmpty =
  adapter.orchestrateParticipantFullExamResultHistoryDataSourceState({
    phase: "resolved",
    limit: 20,
    offset: 0,
    response: {
      data: [],
      error: null
    }
  });

assert(
  orchestratedEmpty.status ===
    "exam_result_history_data_source_empty" &&
  orchestratedEmpty.isSuccess === true &&
  orchestratedEmpty.isEmpty === true &&
  orchestratedEmpty.totalCount === 0 &&
  orchestratedEmpty.paginationState.status ===
    "exam_result_history_pagination_empty",
  "Leerer Datenquellen-Gesamtzustand ist unstabil"
);

const orchestratedStaleEmpty =
  adapter.orchestrateParticipantFullExamResultHistoryDataSourceState({
    phase: "resolved",
    limit: 20,
    offset: 20,
    response: {
      data: [],
      error: null
    }
  });

assert(
  orchestratedStaleEmpty.status ===
    "exam_result_history_data_source_error" &&
  orchestratedStaleEmpty.hasError === true &&
  orchestratedStaleEmpty.canRetry === true &&
  orchestratedStaleEmpty.reason ===
    "empty_page_after_nonzero_offset",
  "Leere Folgeseite wurde nicht sicher abgefangen"
);

const orchestratedInvalidResponse =
  adapter.orchestrateParticipantFullExamResultHistoryDataSourceState({
    phase: "resolved",
    limit: 20,
    offset: 0,
    response: {
      data: [
        makeRow({
          passed: false
        })
      ],
      error: null
    }
  });

assert(
  orchestratedInvalidResponse.status ===
    "exam_result_history_data_source_error" &&
  orchestratedInvalidResponse.hasError === true &&
  orchestratedInvalidResponse.reason ===
    "passed_status_invalid",
  "Ungültige RPC-Ergebnisdaten wurden nicht sicher abgefangen"
);

const orchestratedInvalidRequest =
  adapter.orchestrateParticipantFullExamResultHistoryDataSourceState({
    phase: "prepared",
    limit: 20,
    offset: 10
  });

assert(
  orchestratedInvalidRequest.status ===
    "exam_result_history_data_source_error" &&
  orchestratedInvalidRequest.hasError === true &&
  orchestratedInvalidRequest.canRetry === false &&
  orchestratedInvalidRequest.reason ===
    "offset_must_align_to_limit",
  "Ungültige Pagination-Anfrage wurde nicht geschlossen verworfen"
);

const orchestratedRejected =
  adapter.orchestrateParticipantFullExamResultHistoryDataSourceState({
    phase: "rejected",
    limit: 20,
    offset: 0,
    error: {
      message: "sensitive transport error"
    }
  });

assert(
  orchestratedRejected.status ===
    "exam_result_history_data_source_error" &&
  orchestratedRejected.reason ===
    "rpc_request_failed" &&
  !JSON.stringify(orchestratedRejected).includes("sensitive"),
  "Abgelehnter Datenquellenzustand enthält unsichere Fehlerdetails"
);

const orchestratedMiddle =
  adapter.orchestrateParticipantFullExamResultHistoryDataSourceState({
    phase: "resolved",
    limit: 20,
    offset: 20,
    response: {
      data: [
        {
          ...firstRow,
          total_count: 45
        },
        {
          ...secondRow,
          total_count: 45
        }
      ],
      error: null
    }
  });

const firstIntent =
  adapter.mapParticipantFullExamResultHistoryNavigationIntent({
    intent: "first",
    currentState: orchestratedMiddle
  });

assert(
  firstIntent.status ===
    "exam_result_history_navigation_intent_ready" &&
  firstIntent.canNavigate === true &&
  firstIntent.request.limit === 20 &&
  firstIntent.request.offset === 0,
  "Navigation zur ersten Seite ist unstabil"
);

const previousIntent =
  adapter.mapParticipantFullExamResultHistoryNavigationIntent({
    intent: "previous",
    currentState: orchestratedMiddle
  });

assert(
  previousIntent.canNavigate === true &&
  previousIntent.request.offset === 0,
  "Navigation zur vorherigen Seite ist unstabil"
);

const nextIntent =
  adapter.mapParticipantFullExamResultHistoryNavigationIntent({
    intent: "next",
    currentState: orchestratedSuccess
  });

assert(
  nextIntent.canNavigate === true &&
  nextIntent.request.limit === 20 &&
  nextIntent.request.offset === 20,
  "Navigation zur nächsten Seite ist unstabil"
);

const orchestratedLast =
  adapter.orchestrateParticipantFullExamResultHistoryDataSourceState({
    phase: "resolved",
    limit: 20,
    offset: 20,
    response: {
      data: [
        {
          ...firstRow,
          total_count: 22
        },
        {
          ...secondRow,
          total_count: 22
        }
      ],
      error: null
    }
  });

const blockedNextIntent =
  adapter.mapParticipantFullExamResultHistoryNavigationIntent({
    intent: "next",
    currentState: orchestratedLast
  });

assert(
  blockedNextIntent.canNavigate === false &&
  blockedNextIntent.reason ===
    "next_page_unavailable",
  "Navigation hinter die letzte Seite wurde nicht blockiert"
);

const retryIntent =
  adapter.mapParticipantFullExamResultHistoryNavigationIntent({
    intent: "retry",
    currentState: orchestratedRejected
  });

assert(
  retryIntent.canNavigate === true &&
  retryIntent.isRetry === true &&
  retryIntent.request.offset === 0,
  "Wiederholungsanfrage ist unstabil"
);

const blockedRetryIntent =
  adapter.mapParticipantFullExamResultHistoryNavigationIntent({
    intent: "retry",
    currentState: orchestratedSuccess
  });

expectEqual(
  blockedRetryIntent.reason,
  "retry_not_available",
  "Unzulässige Wiederholungsanfrage"
);

const blockedLoadingIntent =
  adapter.mapParticipantFullExamResultHistoryNavigationIntent({
    intent: "next",
    currentState: orchestratedLoading
  });

expectEqual(
  blockedLoadingIntent.reason,
  "navigation_while_loading",
  "Navigation während des Ladens"
);

const invalidNavigationIntent =
  adapter.mapParticipantFullExamResultHistoryNavigationIntent({
    intent: "unknown",
    currentState: orchestratedSuccess
  });

assert(
  invalidNavigationIntent.isValid === false &&
  invalidNavigationIntent.reason ===
    "navigation_intent_invalid",
  "Ungültiger Navigations-Intent wurde nicht verworfen"
);

const missingNavigationState =
  adapter.mapParticipantFullExamResultHistoryNavigationIntent({
    intent: "first"
  });

expectEqual(
  missingNavigationState.reason,
  "current_state_must_be_object",
  "Fehlender Navigations-Ausgangszustand"
);

const activeRequestIdentity =
  adapter.mapParticipantFullExamResultHistoryRequestIdentity({
    mode: "create",
    requestSequence: 7,
    request: {
      limit: 20,
      offset: 20
    },
    privateField: "nicht übernehmen"
  });

assert(
  activeRequestIdentity.status ===
    "exam_result_history_request_identity_ready" &&
  activeRequestIdentity.isValid === true &&
  activeRequestIdentity.requestIdentity ===
    "exam_history_request:7:20:20",
  "Aktive Anfrage-Identität ist unstabil"
);

assert(
  !Object.prototype.hasOwnProperty.call(
    activeRequestIdentity,
    "privateField"
  ),
  "Unbekanntes Identitätsfeld wurde übernommen"
);

const currentResponseIdentity =
  adapter.mapParticipantFullExamResultHistoryRequestIdentity({
    mode: "compare",
    requestSequence: 7,
    request: {
      limit: 20,
      offset: 20
    },
    responseIdentity:
      activeRequestIdentity.requestIdentity
  });

assert(
  currentResponseIdentity.status ===
    "exam_result_history_response_identity_current" &&
  currentResponseIdentity.canApplyResponse === true &&
  currentResponseIdentity.isCurrentResponse === true &&
  currentResponseIdentity.isStaleResponse === false,
  "Aktuelle Seitenantwort wurde nicht erkannt"
);

const staleSequenceIdentity =
  adapter.mapParticipantFullExamResultHistoryRequestIdentity({
    mode: "compare",
    requestSequence: 7,
    request: {
      limit: 20,
      offset: 20
    },
    responseIdentity:
      "exam_history_request:6:20:20"
  });

assert(
  staleSequenceIdentity.status ===
    "exam_result_history_response_identity_stale" &&
  staleSequenceIdentity.canApplyResponse === false &&
  staleSequenceIdentity.isCurrentResponse === false &&
  staleSequenceIdentity.isStaleResponse === true,
  "Veraltete Anfragefolge wurde nicht verworfen"
);

const stalePageIdentity =
  adapter.mapParticipantFullExamResultHistoryRequestIdentity({
    mode: "compare",
    requestSequence: 7,
    request: {
      limit: 20,
      offset: 20
    },
    responseIdentity:
      "exam_history_request:7:20:0"
  });

assert(
  stalePageIdentity.isStaleResponse === true &&
  stalePageIdentity.reason ===
    "response_identity_does_not_match_active_request",
  "Veraltete Seitenantwort wurde nicht verworfen"
);

const invalidSequenceIdentity =
  adapter.mapParticipantFullExamResultHistoryRequestIdentity({
    mode: "create",
    requestSequence: 0,
    request: {
      limit: 20,
      offset: 0
    }
  });

expectEqual(
  invalidSequenceIdentity.reason,
  "request_sequence_invalid",
  "Ungültige Anfragefolge"
);

const invalidRequestIdentity =
  adapter.mapParticipantFullExamResultHistoryRequestIdentity({
    mode: "create",
    requestSequence: 1,
    request: {
      limit: 20,
      offset: 10
    }
  });

expectEqual(
  invalidRequestIdentity.reason,
  "request_identity_request_invalid",
  "Nicht ausgerichtete Identitätsanfrage"
);

const noncanonicalResponseIdentity =
  adapter.mapParticipantFullExamResultHistoryRequestIdentity({
    mode: "compare",
    requestSequence: 7,
    request: {
      limit: 20,
      offset: 20
    },
    responseIdentity:
      "exam_history_request:07:20:20"
  });

expectEqual(
  noncanonicalResponseIdentity.reason,
  "response_identity_noncanonical",
  "Nicht kanonische Response-Identität"
);

const malformedResponseIdentity =
  adapter.mapParticipantFullExamResultHistoryRequestIdentity({
    mode: "compare",
    requestSequence: 7,
    request: {
      limit: 20,
      offset: 20
    },
    responseIdentity:
      "falsches-format"
  });

expectEqual(
  malformedResponseIdentity.reason,
  "response_identity_format_invalid",
  "Ungültiges Response-Identitätsformat"
);

const acceptedResponseGuard =
  adapter.guardParticipantFullExamResultHistoryResponseAcceptance({
    requestSequence: 7,
    request: {
      limit: 20,
      offset: 20
    },
    responseIdentity:
      activeRequestIdentity.requestIdentity,
    response: {
      data: [
        {
          ...firstRow,
          total_count: 45
        },
        {
          ...secondRow,
          total_count: 45
        }
      ],
      error: null
    }
  });

assert(
  acceptedResponseGuard.status ===
    "exam_result_history_response_acceptance_accepted" &&
  acceptedResponseGuard.isValid === true &&
  acceptedResponseGuard.canAcceptResponse === true &&
  acceptedResponseGuard.didAcceptResponse === true &&
  acceptedResponseGuard.results.length === 2 &&
  acceptedResponseGuard.totalCount === 45,
  "Aktuelle Seitenantwort wurde nicht angenommen"
);

assert(
  !Object.prototype.hasOwnProperty.call(
    acceptedResponseGuard,
    "response"
  ),
  "Rohe RPC-Antwort wurde vom Annahme-Guard übernommen"
);

let staleResponseWasRead = false;

const staleGuardInput = {
  requestSequence: 7,
  request: {
    limit: 20,
    offset: 20
  },
  responseIdentity:
    "exam_history_request:6:20:20"
};

Object.defineProperty(
  staleGuardInput,
  "response",
  {
    enumerable: true,
    get() {
      staleResponseWasRead = true;
      throw new Error(
        "Veraltete Antwort darf nicht gelesen werden."
      );
    }
  }
);

const staleResponseGuard =
  adapter.guardParticipantFullExamResultHistoryResponseAcceptance(
    staleGuardInput
  );

assert(
  staleResponseGuard.status ===
    "exam_result_history_response_acceptance_stale_ignored" &&
  staleResponseGuard.shouldIgnoreResponse === true &&
  staleResponseGuard.didAcceptResponse === false &&
  staleResponseWasRead === false,
  "Veraltete Seitenantwort wurde nicht vor dem Lesen ignoriert"
);

const emptyResponseGuard =
  adapter.guardParticipantFullExamResultHistoryResponseAcceptance({
    requestSequence: 8,
    request: {
      limit: 20,
      offset: 0
    },
    responseIdentity:
      "exam_history_request:8:20:0",
    response: {
      data: [],
      error: null
    }
  });

assert(
  emptyResponseGuard.status ===
    "exam_result_history_response_acceptance_accepted_empty" &&
  emptyResponseGuard.didAcceptResponse === true &&
  emptyResponseGuard.totalCount === 0 &&
  emptyResponseGuard.results.length === 0,
  "Aktuelle leere Antwort wurde nicht sicher angenommen"
);

const erroredResponseGuard =
  adapter.guardParticipantFullExamResultHistoryResponseAcceptance({
    requestSequence: 9,
    request: {
      limit: 20,
      offset: 0
    },
    responseIdentity:
      "exam_history_request:9:20:0",
    response: {
      data: null,
      error: {
        message: "sensitive database message",
        details: "sensitive database details",
        hint: "sensitive database hint"
      }
    }
  });

assert(
  erroredResponseGuard.status ===
    "exam_result_history_response_acceptance_error" &&
  erroredResponseGuard.hasError === true &&
  erroredResponseGuard.reason ===
    "rpc_response_error" &&
  !JSON.stringify(erroredResponseGuard).includes("sensitive"),
  "RPC-Fehler wurde vom Annahme-Guard nicht sicher reduziert"
);

const invalidIdentityGuard =
  adapter.guardParticipantFullExamResultHistoryResponseAcceptance({
    requestSequence: 7,
    request: {
      limit: 20,
      offset: 20
    },
    responseIdentity:
      "falsches-format",
    response: {
      data: [firstRow],
      error: null
    }
  });

assert(
  invalidIdentityGuard.status ===
    "exam_result_history_response_acceptance_invalid" &&
  invalidIdentityGuard.didAcceptResponse === false &&
  invalidIdentityGuard.reason ===
    "response_identity_format_invalid",
  "Ungültige Antwortidentität wurde nicht verworfen"
);

const staleEmptyPageGuard =
  adapter.guardParticipantFullExamResultHistoryResponseAcceptance({
    requestSequence: 10,
    request: {
      limit: 20,
      offset: 20
    },
    responseIdentity:
      "exam_history_request:10:20:20",
    response: {
      data: [],
      error: null
    }
  });

assert(
  staleEmptyPageGuard.status ===
    "exam_result_history_response_acceptance_error" &&
  staleEmptyPageGuard.reason ===
    "empty_page_after_nonzero_offset",
  "Leere aktive Folgeseite wurde nicht sicher behandelt"
);

const lifecyclePrepared =
  adapter.mapParticipantFullExamResultHistoryRequestLifecycle({
    phase: "prepared",
    requestSequence: 11,
    request: {
      limit: 20,
      offset: 0
    }
  });

assert(
  lifecyclePrepared.status ===
    "exam_result_history_request_lifecycle_prepared" &&
  lifecyclePrepared.isPrepared === true &&
  lifecyclePrepared.canStart === true,
  "Vorbereiteter Anfrage-Lebenszyklus ist unstabil"
);

const lifecyclePending =
  adapter.mapParticipantFullExamResultHistoryRequestLifecycle({
    phase: "pending",
    requestSequence: 11,
    request: {
      limit: 20,
      offset: 0
    }
  });

assert(
  lifecyclePending.status ===
    "exam_result_history_request_lifecycle_pending" &&
  lifecyclePending.isPending === true &&
  lifecyclePending.canComplete === true &&
  lifecyclePending.canDiscard === true,
  "Ausstehender Anfrage-Lebenszyklus ist unstabil"
);

const lifecycleCompleted =
  adapter.mapParticipantFullExamResultHistoryRequestLifecycle({
    phase: "completed",
    requestSequence: 7,
    request: {
      limit: 20,
      offset: 20
    },
    acceptanceState:
      acceptedResponseGuard
  });

assert(
  lifecycleCompleted.status ===
    "exam_result_history_request_lifecycle_completed" &&
  lifecycleCompleted.isCompleted === true &&
  lifecycleCompleted.acceptedEntryCount === 2 &&
  lifecycleCompleted.totalCount === 45,
  "Abgeschlossener Anfrage-Lebenszyklus ist unstabil"
);

assert(
  !Object.prototype.hasOwnProperty.call(
    lifecycleCompleted,
    "acceptanceState"
  ),
  "Roher Annahme-State wurde im Lebenszyklus offengelegt"
);

const lifecycleMismatch =
  adapter.mapParticipantFullExamResultHistoryRequestLifecycle({
    phase: "completed",
    requestSequence: 8,
    request: {
      limit: 20,
      offset: 0
    },
    acceptanceState:
      acceptedResponseGuard
  });

expectEqual(
  lifecycleMismatch.reason,
  "request_lifecycle_acceptance_identity_mismatch",
  "Abweichende Annahme-Identität"
);

const lifecycleDiscarded =
  adapter.mapParticipantFullExamResultHistoryRequestLifecycle({
    phase: "discarded",
    requestSequence: 12,
    request: {
      limit: 20,
      offset: 20
    },
    discardReason:
      "superseded_by_new_request"
  });

assert(
  lifecycleDiscarded.status ===
    "exam_result_history_request_lifecycle_discarded" &&
  lifecycleDiscarded.isDiscarded === true &&
  lifecycleDiscarded.discardReason ===
    "superseded_by_new_request",
  "Verworfener Anfrage-Lebenszyklus ist unstabil"
);

const lifecycleInvalidDiscard =
  adapter.mapParticipantFullExamResultHistoryRequestLifecycle({
    phase: "discarded",
    requestSequence: 12,
    request: {
      limit: 20,
      offset: 20
    },
    discardReason: "beliebig"
  });

expectEqual(
  lifecycleInvalidDiscard.reason,
  "request_lifecycle_discard_reason_invalid",
  "Ungültiger Verwerfungsgrund"
);

const lifecycleStaleAcceptance =
  adapter.mapParticipantFullExamResultHistoryRequestLifecycle({
    phase: "completed",
    requestSequence: 7,
    request: {
      limit: 20,
      offset: 20
    },
    acceptanceState:
      staleResponseGuard
  });

expectEqual(
  lifecycleStaleAcceptance.reason,
  "request_lifecycle_acceptance_state_invalid",
  "Veralteter Annahme-State"
);

const transitionPreparedToPending =
  adapter.guardParticipantFullExamResultHistoryRequestLifecycleTransition({
    currentState:
      lifecyclePrepared,
    targetPhase: "pending"
  });

assert(
  transitionPreparedToPending.status ===
    "exam_result_history_request_transition_ready" &&
  transitionPreparedToPending.canTransition === true &&
  transitionPreparedToPending.didTransition === true &&
  transitionPreparedToPending.fromPhase ===
    "prepared" &&
  transitionPreparedToPending.toPhase ===
    "pending" &&
  transitionPreparedToPending.nextState.isPending ===
    true,
  "Übergang vorbereitet zu ausstehend ist unstabil"
);

const transitionPendingToCompleted =
  adapter.guardParticipantFullExamResultHistoryRequestLifecycleTransition({
    currentState:
      adapter.mapParticipantFullExamResultHistoryRequestLifecycle({
        phase: "pending",
        requestSequence: 7,
        request: {
          limit: 20,
          offset: 20
        }
      }),
    targetPhase: "completed",
    acceptanceState:
      acceptedResponseGuard
  });

assert(
  transitionPendingToCompleted.status ===
    "exam_result_history_request_transition_ready" &&
  transitionPendingToCompleted.isTerminalTransition ===
    true &&
  transitionPendingToCompleted.nextState.isCompleted ===
    true &&
  transitionPendingToCompleted.nextState.acceptedEntryCount ===
    2,
  "Übergang ausstehend zu abgeschlossen ist unstabil"
);

const transitionPendingToDiscarded =
  adapter.guardParticipantFullExamResultHistoryRequestLifecycleTransition({
    currentState:
      lifecyclePending,
    targetPhase: "discarded",
    discardReason:
      "superseded_by_new_request"
  });

assert(
  transitionPendingToDiscarded.canTransition ===
    true &&
  transitionPendingToDiscarded.nextState.isDiscarded ===
    true &&
  transitionPendingToDiscarded.nextState.discardReason ===
    "superseded_by_new_request",
  "Übergang ausstehend zu verworfen ist unstabil"
);

const blockedPreparedToCompleted =
  adapter.guardParticipantFullExamResultHistoryRequestLifecycleTransition({
    currentState:
      lifecyclePrepared,
    targetPhase: "completed",
    acceptanceState:
      acceptedResponseGuard
  });

expectEqual(
  blockedPreparedToCompleted.reason,
  "request_transition_not_allowed",
  "Direkter Übergang vorbereitet zu abgeschlossen"
);

const blockedCompletedToPending =
  adapter.guardParticipantFullExamResultHistoryRequestLifecycleTransition({
    currentState:
      lifecycleCompleted,
    targetPhase: "pending"
  });

assert(
  blockedCompletedToPending.status ===
    "exam_result_history_request_transition_blocked" &&
  blockedCompletedToPending.canTransition ===
    false &&
  blockedCompletedToPending.reason ===
    "request_transition_terminal_state",
  "Übergang aus abgeschlossenem Endzustand wurde nicht blockiert"
);

const blockedSamePhase =
  adapter.guardParticipantFullExamResultHistoryRequestLifecycleTransition({
    currentState:
      lifecyclePending,
    targetPhase: "pending"
  });

expectEqual(
  blockedSamePhase.reason,
  "request_transition_not_allowed",
  "Übergang in denselben Zustand"
);

const invalidTransitionAcceptance =
  adapter.guardParticipantFullExamResultHistoryRequestLifecycleTransition({
    currentState:
      adapter.mapParticipantFullExamResultHistoryRequestLifecycle({
        phase: "pending",
        requestSequence: 7,
        request: {
          limit: 20,
          offset: 20
        }
      }),
    targetPhase: "completed",
    acceptanceState:
      staleResponseGuard
  });

expectEqual(
  invalidTransitionAcceptance.reason,
  "request_lifecycle_acceptance_state_invalid",
  "Übergang mit veralteter Antwortannahme"
);

const invalidTransitionState =
  adapter.guardParticipantFullExamResultHistoryRequestLifecycleTransition({
    currentState: {
      ...lifecyclePending,
      requestIdentity:
        "exam_history_request:999:20:0"
    },
    targetPhase: "discarded",
    discardReason:
      "cancelled_before_response"
  });

expectEqual(
  invalidTransitionState.reason,
  "request_transition_current_identity_invalid",
  "Manipulierte aktuelle Anfrageidentität"
);

const controllerInitialized =
  adapter.mapParticipantFullExamResultHistoryRequestControllerState({
    action: "initialize",
    requestSequence: 21,
    request: {
      limit: 20,
      offset: 0
    }
  });

assert(
  controllerInitialized.status ===
    "exam_result_history_request_controller_prepared" &&
  controllerInitialized.isPrepared === true &&
  controllerInitialized.requestIdentity ===
    "exam_history_request:21:20:0",
  "Initialisierter Anfrage-Controller ist unstabil"
);

const controllerStarted =
  adapter.mapParticipantFullExamResultHistoryRequestControllerState({
    action: "start",
    currentLifecycleState:
      controllerInitialized.lifecycleState
  });

assert(
  controllerStarted.status ===
    "exam_result_history_request_controller_pending" &&
  controllerStarted.isPending === true &&
  controllerStarted.lifecycleState.isPending ===
    true,
  "Gestarteter Anfrage-Controller ist unstabil"
);

const controllerAccepted =
  adapter.mapParticipantFullExamResultHistoryRequestControllerState({
    action: "accept",
    currentLifecycleState:
      controllerStarted.lifecycleState,
    responseIdentity:
      "exam_history_request:21:20:0",
    response: {
      data: [
        {
          ...firstRow,
          total_count: 45
        },
        {
          ...secondRow,
          total_count: 45
        }
      ],
      error: null
    }
  });

assert(
  controllerAccepted.status ===
    "exam_result_history_request_controller_completed" &&
  controllerAccepted.isCompleted === true &&
  controllerAccepted.didAcceptResponse === true &&
  controllerAccepted.results.length === 2 &&
  controllerAccepted.totalCount === 45,
  "Abgeschlossener Anfrage-Controller ist unstabil"
);

assert(
  !Object.prototype.hasOwnProperty.call(
    controllerAccepted,
    "response"
  ),
  "Rohe Response wurde im Anfrage-Controller offengelegt"
);

const controllerNavigation =
  adapter.mapParticipantFullExamResultHistoryRequestControllerState({
    action: "navigate",
    currentLifecycleState:
      controllerAccepted.lifecycleState,
    currentDataSourceState:
      orchestratedSuccess,
    navigationIntent: "next",
    nextRequestSequence: 22
  });

assert(
  controllerNavigation.status ===
    "exam_result_history_request_controller_navigation_ready" &&
  controllerNavigation.isNavigationReady === true &&
  controllerNavigation.isPrepared === true &&
  controllerNavigation.request.offset === 20 &&
  controllerNavigation.requestSequence === 22 &&
  controllerNavigation.previousRequestIdentity ===
    "exam_history_request:21:20:0",
  "Controller-Navigation ist unstabil"
);

let controllerStaleResponseWasRead = false;

const controllerStaleInput = {
  action: "accept",
  currentLifecycleState:
    controllerStarted.lifecycleState,
  responseIdentity:
    "exam_history_request:20:20:0"
};

Object.defineProperty(
  controllerStaleInput,
  "response",
  {
    enumerable: true,
    get() {
      controllerStaleResponseWasRead = true;
      throw new Error(
        "Veraltete Controller-Response darf nicht gelesen werden."
      );
    }
  }
);

const controllerStale =
  adapter.mapParticipantFullExamResultHistoryRequestControllerState(
    controllerStaleInput
  );

assert(
  controllerStale.status ===
    "exam_result_history_request_controller_stale_ignored" &&
  controllerStale.shouldIgnoreResponse === true &&
  controllerStaleResponseWasRead === false,
  "Veraltete Controller-Response wurde nicht ungelesen ignoriert"
);

const controllerDiscarded =
  adapter.mapParticipantFullExamResultHistoryRequestControllerState({
    action: "discard",
    currentLifecycleState:
      controllerStarted.lifecycleState,
    discardReason:
      "cancelled_before_response"
  });

assert(
  controllerDiscarded.status ===
    "exam_result_history_request_controller_discarded" &&
  controllerDiscarded.isDiscarded === true &&
  controllerDiscarded.lifecycleState.discardReason ===
    "cancelled_before_response",
  "Verworfener Anfrage-Controller ist unstabil"
);

const controllerBlockedRestart =
  adapter.mapParticipantFullExamResultHistoryRequestControllerState({
    action: "start",
    currentLifecycleState:
      controllerAccepted.lifecycleState
  });

expectEqual(
  controllerBlockedRestart.reason,
  "request_transition_terminal_state",
  "Neustart aus abgeschlossenem Controller"
);

const controllerInvalidSequence =
  adapter.mapParticipantFullExamResultHistoryRequestControllerState({
    action: "navigate",
    currentLifecycleState:
      controllerAccepted.lifecycleState,
    currentDataSourceState:
      orchestratedSuccess,
    navigationIntent: "next",
    nextRequestSequence: 21
  });

expectEqual(
  controllerInvalidSequence.reason,
  "request_controller_next_request_sequence_invalid",
  "Ungültige nächste Controller-Anfragefolge"
);

const preparedSnapshot =
  adapter.normalizeParticipantFullExamResultHistoryControllerSnapshot({
    snapshotVersion: 1,
    controllerState:
      controllerInitialized,
    privateField:
      "nicht übernehmen"
  });

assert(
  preparedSnapshot.status ===
    "exam_result_history_controller_snapshot_resumable" &&
  preparedSnapshot.canResume === true &&
  preparedSnapshot.resumeAction ===
    "start_prepared_request" &&
  preparedSnapshot.requestIdentity ===
    "exam_history_request:21:20:0",
  "Vorbereiteter Controller-Snapshot ist unstabil"
);

assert(
  !Object.prototype.hasOwnProperty.call(
    preparedSnapshot,
    "privateField"
  ),
  "Unbekanntes Snapshot-Feld wurde übernommen"
);

const pendingSnapshot =
  adapter.normalizeParticipantFullExamResultHistoryControllerSnapshot({
    snapshotVersion: 1,
    controllerState:
      controllerStarted
  });

assert(
  pendingSnapshot.canResume === true &&
  pendingSnapshot.phase === "pending" &&
  pendingSnapshot.resumeAction ===
    "retry_pending_request",
  "Ausstehender Controller-Snapshot ist unstabil"
);

const completedSnapshot =
  adapter.normalizeParticipantFullExamResultHistoryControllerSnapshot({
    snapshotVersion: 1,
    controllerState:
      controllerAccepted
  });

assert(
  completedSnapshot.status ===
    "exam_result_history_controller_snapshot_terminal" &&
  completedSnapshot.isTerminal === true &&
  completedSnapshot.canResume === false &&
  completedSnapshot.acceptedEntryCount === 2 &&
  completedSnapshot.totalCount === 45 &&
  completedSnapshot.paginationState.isValid ===
    true,
  "Abgeschlossener Controller-Snapshot ist unstabil"
);

assert(
  !Object.prototype.hasOwnProperty.call(
    completedSnapshot,
    "results"
  ),
  "Ergebniszeilen wurden im Snapshot offengelegt"
);

const navigationSnapshot =
  adapter.normalizeParticipantFullExamResultHistoryControllerSnapshot({
    snapshotVersion: 1,
    controllerState:
      controllerNavigation
  });

assert(
  navigationSnapshot.canResume === true &&
  navigationSnapshot.phase === "prepared" &&
  navigationSnapshot.navigationIntent ===
    "next" &&
  navigationSnapshot.previousRequestIdentity ===
    "exam_history_request:21:20:0" &&
  navigationSnapshot.requestSequence === 22,
  "Navigations-Snapshot ist unstabil"
);

const discardedSnapshot =
  adapter.normalizeParticipantFullExamResultHistoryControllerSnapshot({
    snapshotVersion: 1,
    controllerState:
      controllerDiscarded
  });

assert(
  discardedSnapshot.isTerminal === true &&
  discardedSnapshot.canResume === false &&
  discardedSnapshot.discardReason ===
    "cancelled_before_response",
  "Verworfener Controller-Snapshot ist unstabil"
);

const tamperedIdentitySnapshot =
  adapter.normalizeParticipantFullExamResultHistoryControllerSnapshot({
    snapshotVersion: 1,
    controllerState: {
      ...controllerStarted,
      requestIdentity:
        "exam_history_request:999:20:0"
    }
  });

expectEqual(
  tamperedIdentitySnapshot.reason,
  "controller_snapshot_identity_invalid",
  "Manipulierte Snapshot-Identität"
);

const tamperedPaginationSnapshot =
  adapter.normalizeParticipantFullExamResultHistoryControllerSnapshot({
    snapshotVersion: 1,
    controllerState: {
      ...controllerAccepted,
      totalCount: 1
    }
  });

assert(
  tamperedPaginationSnapshot.isValid === false &&
  tamperedPaginationSnapshot.reason ===
    "controller_snapshot_total_count_invalid",
  "Manipulierter Snapshot-Gesamtwert wurde nicht verworfen"
);

const invalidVersionSnapshot =
  adapter.normalizeParticipantFullExamResultHistoryControllerSnapshot({
    snapshotVersion: 2,
    controllerState:
      controllerInitialized
  });

expectEqual(
  invalidVersionSnapshot.reason,
  "controller_snapshot_version_invalid",
  "Ungültige Snapshot-Version"
);

const resumePrepared =
  adapter.mapParticipantFullExamResultHistorySnapshotResumeState({
    snapshot: {
      snapshotVersion: 1,
      controllerState:
        controllerInitialized
    },
    privateField:
      "nicht übernehmen"
  });

assert(
  resumePrepared.status ===
    "exam_result_history_snapshot_resume_prepared" &&
  resumePrepared.canResume === true &&
  resumePrepared.isPrepared === true &&
  resumePrepared.resumeAction ===
    "start_prepared_request" &&
  resumePrepared.reconstructedControllerState.isPrepared ===
    true,
  "Vorbereiteter Snapshot wurde nicht sicher rekonstruiert"
);

assert(
  !Object.prototype.hasOwnProperty.call(
    resumePrepared,
    "snapshot"
  ) &&
  !Object.prototype.hasOwnProperty.call(
    resumePrepared,
    "privateField"
  ),
  "Roher Snapshot-Inhalt wurde übernommen"
);

const resumePending =
  adapter.mapParticipantFullExamResultHistorySnapshotResumeState({
    snapshot: {
      snapshotVersion: 1,
      controllerState:
        controllerStarted
    }
  });

assert(
  resumePending.status ===
    "exam_result_history_snapshot_resume_pending_retry" &&
  resumePending.canResume === true &&
  resumePending.isPending === true &&
  resumePending.resumeAction ===
    "retry_pending_request" &&
  resumePending.reconstructedControllerState.isPending ===
    true,
  "Ausstehender Snapshot wurde nicht sicher rekonstruiert"
);

const resumeNavigation =
  adapter.mapParticipantFullExamResultHistorySnapshotResumeState({
    snapshot: {
      snapshotVersion: 1,
      controllerState:
        controllerNavigation
    }
  });

assert(
  resumeNavigation.status ===
    "exam_result_history_snapshot_resume_navigation_prepared" &&
  resumeNavigation.canResume === true &&
  resumeNavigation.isNavigationResume === true &&
  resumeNavigation.navigationIntent ===
    "next" &&
  resumeNavigation.previousRequestIdentity ===
    "exam_history_request:21:20:0" &&
  resumeNavigation.reconstructedControllerState.requestSequence ===
    22,
  "Navigations-Snapshot wurde nicht sicher rekonstruiert"
);

const resumeCompleted =
  adapter.mapParticipantFullExamResultHistorySnapshotResumeState({
    snapshot: {
      snapshotVersion: 1,
      controllerState:
        controllerAccepted
    }
  });

assert(
  resumeCompleted.status ===
    "exam_result_history_snapshot_resume_terminal_blocked" &&
  resumeCompleted.canResume === false &&
  resumeCompleted.isTerminal === true &&
  resumeCompleted.reconstructedControllerState ===
    null,
  "Abgeschlossener Snapshot wurde nicht blockiert"
);

const resumeDiscarded =
  adapter.mapParticipantFullExamResultHistorySnapshotResumeState({
    snapshot: {
      snapshotVersion: 1,
      controllerState:
        controllerDiscarded
    }
  });

assert(
  resumeDiscarded.status ===
    "exam_result_history_snapshot_resume_terminal_blocked" &&
  resumeDiscarded.canResume === false &&
  resumeDiscarded.isTerminal === true,
  "Verworfener Snapshot wurde nicht blockiert"
);

const resumeInvalid =
  adapter.mapParticipantFullExamResultHistorySnapshotResumeState({
    snapshot: {
      snapshotVersion: 2,
      controllerState:
        controllerInitialized
    }
  });

expectEqual(
  resumeInvalid.reason,
  "controller_snapshot_version_invalid",
  "Ungültiger Snapshot im Wiederaufnahme-State"
);

const createdPreparedSnapshot =
  adapter.mapParticipantFullExamResultHistorySnapshotCreationState({
    controllerState: {
      ...controllerInitialized,
      privateField:
        "nicht übernehmen"
    }
  });

assert(
  createdPreparedSnapshot.status ===
    "exam_result_history_snapshot_creation_ready" &&
  createdPreparedSnapshot.canCreateSnapshot === true &&
  createdPreparedSnapshot.canPersistLater === true &&
  createdPreparedSnapshot.canWriteStorage === false &&
  createdPreparedSnapshot.snapshotPayload.snapshotVersion ===
    1,
  "Vorbereiteter Snapshot wurde nicht sicher erstellt"
);

assert(
  !Object.prototype.hasOwnProperty.call(
    createdPreparedSnapshot.snapshotPayload.controllerState,
    "privateField"
  ) &&
  !Object.prototype.hasOwnProperty.call(
    createdPreparedSnapshot.snapshotPayload.controllerState,
    "results"
  ),
  "Unzulässige Controllerdaten wurden im Snapshot gespeichert"
);

const createdPreparedResume =
  adapter.mapParticipantFullExamResultHistorySnapshotResumeState({
    snapshot:
      createdPreparedSnapshot.snapshotPayload
  });

assert(
  createdPreparedResume.canResume === true &&
  createdPreparedResume.isPrepared === true &&
  createdPreparedResume.requestIdentity ===
    createdPreparedSnapshot.requestIdentity,
  "Erstellter vorbereiteter Snapshot ist nicht wiederaufnehmbar"
);

const createdPendingSnapshot =
  adapter.mapParticipantFullExamResultHistorySnapshotCreationState({
    controllerState:
      controllerStarted
  });

const createdPendingResume =
  adapter.mapParticipantFullExamResultHistorySnapshotResumeState({
    snapshot:
      createdPendingSnapshot.snapshotPayload
  });

assert(
  createdPendingSnapshot.canCreateSnapshot === true &&
  createdPendingResume.canResume === true &&
  createdPendingResume.isPending === true &&
  createdPendingResume.resumeAction ===
    "retry_pending_request",
  "Ausstehender Snapshot wurde nicht sicher erstellt"
);

const createdNavigationSnapshot =
  adapter.mapParticipantFullExamResultHistorySnapshotCreationState({
    controllerState:
      controllerNavigation
  });

const createdNavigationResume =
  adapter.mapParticipantFullExamResultHistorySnapshotResumeState({
    snapshot:
      createdNavigationSnapshot.snapshotPayload
  });

assert(
  createdNavigationSnapshot.canCreateSnapshot === true &&
  createdNavigationResume.isNavigationResume === true &&
  createdNavigationResume.navigationIntent ===
    "next" &&
  createdNavigationResume.previousRequestIdentity ===
    "exam_history_request:21:20:0",
  "Navigations-Snapshot wurde nicht sicher erstellt"
);

const repeatedPreparedSnapshot =
  adapter.mapParticipantFullExamResultHistorySnapshotCreationState({
    controllerState:
      controllerInitialized
  });

expectEqual(
  JSON.stringify(
    repeatedPreparedSnapshot.snapshotPayload
  ),
  JSON.stringify(
    createdPreparedSnapshot.snapshotPayload
  ),
  "Deterministische Snapshot-Erstellung"
);

const blockedCompletedCreation =
  adapter.mapParticipantFullExamResultHistorySnapshotCreationState({
    controllerState:
      controllerAccepted
  });

assert(
  blockedCompletedCreation.status ===
    "exam_result_history_snapshot_creation_blocked" &&
  blockedCompletedCreation.canCreateSnapshot === false &&
  blockedCompletedCreation.isTerminal === true &&
  blockedCompletedCreation.snapshotPayload ===
    null,
  "Abgeschlossener Controller wurde als Snapshot vorbereitet"
);

const blockedDiscardedCreation =
  adapter.mapParticipantFullExamResultHistorySnapshotCreationState({
    controllerState:
      controllerDiscarded
  });

assert(
  blockedDiscardedCreation.status ===
    "exam_result_history_snapshot_creation_blocked" &&
  blockedDiscardedCreation.isTerminal === true,
  "Verworfener Controller wurde als Snapshot vorbereitet"
);

const invalidSnapshotCreation =
  adapter.mapParticipantFullExamResultHistorySnapshotCreationState({
    controllerState: {
      ...controllerStarted,
      requestIdentity:
        "exam_history_request:999:20:0"
    }
  });

expectEqual(
  invalidSnapshotCreation.reason,
  "controller_snapshot_identity_invalid",
  "Manipulierter Controller im Snapshot-Erstellungsstate"
);

const serializedPreparedSnapshot =
  adapter.mapParticipantFullExamResultHistorySnapshotSerializationState({
    creationState:
      createdPreparedSnapshot,
    privateField:
      "nicht übernehmen"
  });

assert(
  serializedPreparedSnapshot.status ===
    "exam_result_history_snapshot_serialization_ready" &&
  serializedPreparedSnapshot.isValid === true &&
  serializedPreparedSnapshot.canSerialize === true &&
  serializedPreparedSnapshot.canPersistLater === true &&
  serializedPreparedSnapshot.canWriteStorage === false &&
  typeof serializedPreparedSnapshot.serializedJson ===
    "string" &&
  serializedPreparedSnapshot.serializedByteLength > 0 &&
  serializedPreparedSnapshot.serializedByteLength <=
    serializedPreparedSnapshot.maximumSerializedBytes,
  "Vorbereiteter Snapshot wurde nicht sicher serialisiert"
);

assert(
  !serializedPreparedSnapshot.serializedJson.includes(
    "privateField"
  ) &&
  !serializedPreparedSnapshot.serializedJson.includes(
    "results"
  ),
  "Unzulässige Felder wurden serialisiert"
);

const parsedPreparedSnapshot =
  JSON.parse(
    serializedPreparedSnapshot.serializedJson
  );

const serializedPreparedResume =
  adapter.mapParticipantFullExamResultHistorySnapshotResumeState({
    snapshot:
      parsedPreparedSnapshot
  });

assert(
  serializedPreparedResume.canResume === true &&
  serializedPreparedResume.isPrepared === true &&
  serializedPreparedResume.requestIdentity ===
    serializedPreparedSnapshot.requestIdentity,
  "Serialisierter vorbereiteter Snapshot ist nicht wiederaufnehmbar"
);

const serializedPendingSnapshot =
  adapter.mapParticipantFullExamResultHistorySnapshotSerializationState({
    creationState:
      createdPendingSnapshot
  });

const serializedPendingResume =
  adapter.mapParticipantFullExamResultHistorySnapshotResumeState({
    snapshot:
      JSON.parse(
        serializedPendingSnapshot.serializedJson
      )
  });

assert(
  serializedPendingSnapshot.canSerialize === true &&
  serializedPendingResume.canResume === true &&
  serializedPendingResume.isPending === true,
  "Ausstehender Snapshot wurde nicht sicher serialisiert"
);

const serializedNavigationSnapshot =
  adapter.mapParticipantFullExamResultHistorySnapshotSerializationState({
    creationState:
      createdNavigationSnapshot
  });

const serializedNavigationResume =
  adapter.mapParticipantFullExamResultHistorySnapshotResumeState({
    snapshot:
      JSON.parse(
        serializedNavigationSnapshot.serializedJson
      )
  });

assert(
  serializedNavigationSnapshot.canSerialize === true &&
  serializedNavigationResume.isNavigationResume === true &&
  serializedNavigationResume.navigationIntent ===
    "next",
  "Navigations-Snapshot wurde nicht sicher serialisiert"
);

const repeatedSerializedSnapshot =
  adapter.mapParticipantFullExamResultHistorySnapshotSerializationState({
    creationState:
      repeatedPreparedSnapshot
  });

expectEqual(
  repeatedSerializedSnapshot.serializedJson,
  serializedPreparedSnapshot.serializedJson,
  "Kanonische Snapshot-Serialisierung"
);

const blockedSnapshotSerialization =
  adapter.mapParticipantFullExamResultHistorySnapshotSerializationState({
    creationState:
      blockedCompletedCreation
  });

assert(
  blockedSnapshotSerialization.status ===
    "exam_result_history_snapshot_serialization_blocked" &&
  blockedSnapshotSerialization.canSerialize === false &&
  blockedSnapshotSerialization.serializedJson === null &&
  blockedSnapshotSerialization.reason ===
    "snapshot_serialization_creation_state_not_ready",
  "Blockierter Erstellungsstate wurde serialisiert"
);

const invalidSnapshotSerialization =
  adapter.mapParticipantFullExamResultHistorySnapshotSerializationState({
    creationState:
      invalidSnapshotCreation
  });

assert(
  invalidSnapshotSerialization.isValid === false &&
  invalidSnapshotSerialization.serializedJson === null &&
  invalidSnapshotSerialization.reason ===
    "controller_snapshot_identity_invalid",
  "Ungültiger Erstellungsstate wurde serialisiert"
);

const deserializedPreparedSnapshot =
  adapter.mapParticipantFullExamResultHistorySnapshotDeserializationState({
    serializedJson:
      serializedPreparedSnapshot.serializedJson,
    privateField:
      "nicht übernehmen"
  });

assert(
  deserializedPreparedSnapshot.status ===
    "exam_result_history_snapshot_deserialization_ready" &&
  deserializedPreparedSnapshot.isValid === true &&
  deserializedPreparedSnapshot.canDeserialize === true &&
  deserializedPreparedSnapshot.canResume === true &&
  deserializedPreparedSnapshot.canWriteStorage === false &&
  deserializedPreparedSnapshot.resumeState.isPrepared ===
    true &&
  deserializedPreparedSnapshot.requestIdentity ===
    serializedPreparedSnapshot.requestIdentity,
  "Vorbereiteter Snapshot wurde nicht sicher deserialisiert"
);

assert(
  !Object.prototype.hasOwnProperty.call(
    deserializedPreparedSnapshot,
    "serializedJson"
  ) &&
  !Object.prototype.hasOwnProperty.call(
    deserializedPreparedSnapshot,
    "privateField"
  ),
  "Roher Serialisierungsinhalt wurde übernommen"
);

const deserializedPendingSnapshot =
  adapter.mapParticipantFullExamResultHistorySnapshotDeserializationState({
    serializedJson:
      serializedPendingSnapshot.serializedJson
  });

assert(
  deserializedPendingSnapshot.canDeserialize === true &&
  deserializedPendingSnapshot.canResume === true &&
  deserializedPendingSnapshot.resumeState.isPending ===
    true &&
  deserializedPendingSnapshot.resumeState.resumeAction ===
    "retry_pending_request",
  "Ausstehender Snapshot wurde nicht sicher deserialisiert"
);

const deserializedNavigationSnapshot =
  adapter.mapParticipantFullExamResultHistorySnapshotDeserializationState({
    serializedJson:
      serializedNavigationSnapshot.serializedJson
  });

assert(
  deserializedNavigationSnapshot.canDeserialize === true &&
  deserializedNavigationSnapshot.resumeState.isNavigationResume ===
    true &&
  deserializedNavigationSnapshot.resumeState.navigationIntent ===
    "next",
  "Navigations-Snapshot wurde nicht sicher deserialisiert"
);

const nonCanonicalDeserialization =
  adapter.mapParticipantFullExamResultHistorySnapshotDeserializationState({
    serializedJson:
      serializedPreparedSnapshot.serializedJson + " "
  });

expectEqual(
  nonCanonicalDeserialization.reason,
  "snapshot_deserialization_json_not_canonical",
  "Nicht kanonisches Snapshot-JSON"
);

const oversizedDeserialization =
  adapter.mapParticipantFullExamResultHistorySnapshotDeserializationState({
    serializedJson:
      "x".repeat(4097)
  });

assert(
  oversizedDeserialization.status ===
    "exam_result_history_snapshot_deserialization_too_large" &&
  oversizedDeserialization.canDeserialize === false &&
  oversizedDeserialization.serializedByteLength ===
    4097 &&
  oversizedDeserialization.reason ===
    "snapshot_deserialization_size_limit_exceeded",
  "Zu großer Snapshot wurde vor dem Parsing nicht blockiert"
);

const malformedDeserialization =
  adapter.mapParticipantFullExamResultHistorySnapshotDeserializationState({
    serializedJson:
      '{"snapshotVersion":1'
  });

expectEqual(
  malformedDeserialization.reason,
  "snapshot_deserialization_json_parse_failed",
  "Fehlerhaftes Snapshot-JSON"
);

const tamperedDeserializationPayload =
  JSON.parse(
    serializedPreparedSnapshot.serializedJson
  );

tamperedDeserializationPayload.controllerState.requestIdentity =
  "exam_history_request:999:20:0";

const tamperedDeserialization =
  adapter.mapParticipantFullExamResultHistorySnapshotDeserializationState({
    serializedJson:
      JSON.stringify(
        tamperedDeserializationPayload
      )
  });

expectEqual(
  tamperedDeserialization.reason,
  "controller_snapshot_identity_invalid",
  "Manipulierte deserialisierte Anfrageidentität"
);

const persistenceSave =
  adapter.mapParticipantFullExamResultHistorySnapshotPersistenceContract({
    intent: "save",
    serializationState:
      serializedPreparedSnapshot,
    privateField:
      "nicht übernehmen"
  });

assert(
  persistenceSave.status ===
    "exam_result_history_snapshot_persistence_save_ready" &&
  persistenceSave.isValid === true &&
  persistenceSave.canPrepareSave === true &&
  persistenceSave.canExecuteStorage === false &&
  persistenceSave.canWriteStorage === false &&
  persistenceSave.storageKey ===
    persistenceSave.storageKeyPrefix +
    serializedPreparedSnapshot.requestIdentity &&
  persistenceSave.serializedJson ===
    serializedPreparedSnapshot.serializedJson,
  "Snapshot-Save-Intent wurde nicht sicher vorbereitet"
);

assert(
  !Object.prototype.hasOwnProperty.call(
    persistenceSave,
    "privateField"
  ),
  "Unbekanntes Persistenzfeld wurde übernommen"
);

const persistenceLoad =
  adapter.mapParticipantFullExamResultHistorySnapshotPersistenceContract({
    intent: "load",
    storageKey:
      persistenceSave.storageKey,
    serializedJson:
      persistenceSave.serializedJson
  });

assert(
  persistenceLoad.status ===
    "exam_result_history_snapshot_persistence_load_ready" &&
  persistenceLoad.canPrepareLoad === true &&
  persistenceLoad.canExecuteStorage === false &&
  persistenceLoad.requestIdentity ===
    persistenceSave.requestIdentity &&
  persistenceLoad.deserializationState.canResume ===
    true &&
  persistenceLoad.deserializationState.resumeState.isPrepared ===
    true,
  "Snapshot-Load-Intent wurde nicht sicher vorbereitet"
);

assert(
  persistenceLoad.serializedJson === null,
  "Roher Load-Wert wurde im Persistenzstate offengelegt"
);

const persistenceDelete =
  adapter.mapParticipantFullExamResultHistorySnapshotPersistenceContract({
    intent: "delete",
    storageKey:
      persistenceSave.storageKey
  });

assert(
  persistenceDelete.status ===
    "exam_result_history_snapshot_persistence_delete_ready" &&
  persistenceDelete.canPrepareDelete === true &&
  persistenceDelete.canExecuteStorage === false &&
  persistenceDelete.storageKey ===
    persistenceSave.storageKey,
  "Snapshot-Delete-Intent wurde nicht sicher vorbereitet"
);

const persistenceMismatchedLoad =
  adapter.mapParticipantFullExamResultHistorySnapshotPersistenceContract({
    intent: "load",
    storageKey:
      persistenceSave.storageKeyPrefix +
      "exam_history_request:999:20:0",
    serializedJson:
      persistenceSave.serializedJson
  });

expectEqual(
  persistenceMismatchedLoad.reason,
  "snapshot_persistence_storage_key_identity_mismatch",
  "Abweichende Storage-Key-Identität"
);

const persistenceBlockedSave =
  adapter.mapParticipantFullExamResultHistorySnapshotPersistenceContract({
    intent: "save",
    serializationState:
      blockedSnapshotSerialization
  });

assert(
  persistenceBlockedSave.status ===
    "exam_result_history_snapshot_persistence_save_blocked" &&
  persistenceBlockedSave.canPrepareSave === false &&
  persistenceBlockedSave.serializedJson === null,
  "Blockierter Serialisierungsstate wurde zum Speichern vorbereitet"
);

const persistenceInvalidKey =
  adapter.mapParticipantFullExamResultHistorySnapshotPersistenceContract({
    intent: "delete",
    storageKey:
      "falscher-schluessel"
  });

expectEqual(
  persistenceInvalidKey.reason,
  "snapshot_persistence_storage_key_invalid",
  "Ungültiger Persistenzschlüssel"
);

const persistenceInvalidIntent =
  adapter.mapParticipantFullExamResultHistorySnapshotPersistenceContract({
    intent: "write"
  });

expectEqual(
  persistenceInvalidIntent.reason,
  "snapshot_persistence_intent_invalid",
  "Ungültiger Persistenz-Intent"
);

let storageAdapterOperationCalls = 0;

const fullStorageAdapter = {
  adapterKind:
    "accaoui_exam_history_snapshot_storage_adapter_v1",
  contractVersion: 1,
  read() {
    storageAdapterOperationCalls += 1;
    throw new Error(
      "Readiness darf read nicht aufrufen."
    );
  },
  write() {
    storageAdapterOperationCalls += 1;
    throw new Error(
      "Readiness darf write nicht aufrufen."
    );
  },
  delete() {
    storageAdapterOperationCalls += 1;
    throw new Error(
      "Readiness darf delete nicht aufrufen."
    );
  }
};

const fullStorageReadiness =
  adapter.mapParticipantFullExamResultHistorySnapshotStorageAdapterReadiness({
    storageAdapter:
      fullStorageAdapter,
    privateField:
      "nicht übernehmen"
  });

assert(
  fullStorageReadiness.status ===
    "exam_result_history_storage_adapter_readiness_ready" &&
  fullStorageReadiness.isValid === true &&
  fullStorageReadiness.isAdapterReady === true &&
  fullStorageReadiness.canRead === true &&
  fullStorageReadiness.canWrite === true &&
  fullStorageReadiness.canDelete === true &&
  fullStorageReadiness.availableCapabilityCount ===
    3 &&
  fullStorageReadiness.canExecuteStorage === false &&
  storageAdapterOperationCalls === 0,
  "Vollständiger Storage-Adapter wurde nicht sicher geprüft"
);

assert(
  !Object.prototype.hasOwnProperty.call(
    fullStorageReadiness,
    "storageAdapter"
  ) &&
  !Object.prototype.hasOwnProperty.call(
    fullStorageReadiness,
    "privateField"
  ),
  "Storage-Adapter wurde im Readiness-State offengelegt"
);

const partialStorageReadiness =
  adapter.mapParticipantFullExamResultHistorySnapshotStorageAdapterReadiness({
    storageAdapter: {
      adapterKind:
        "accaoui_exam_history_snapshot_storage_adapter_v1",
      contractVersion: 1,
      read() {}
    }
  });

assert(
  partialStorageReadiness.status ===
    "exam_result_history_storage_adapter_readiness_partial" &&
  partialStorageReadiness.isPartiallyReady === true &&
  partialStorageReadiness.canRead === true &&
  partialStorageReadiness.canWrite === false &&
  partialStorageReadiness.canDelete === false,
  "Teilweiser Storage-Adapter wurde nicht erkannt"
);

const unavailableStorageReadiness =
  adapter.mapParticipantFullExamResultHistorySnapshotStorageAdapterReadiness({
    storageAdapter: {
      adapterKind:
        "accaoui_exam_history_snapshot_storage_adapter_v1",
      contractVersion: 1
    }
  });

assert(
  unavailableStorageReadiness.status ===
    "exam_result_history_storage_adapter_readiness_unavailable" &&
  unavailableStorageReadiness.isAdapterReady === false &&
  unavailableStorageReadiness.availableCapabilityCount ===
    0,
  "Storage-Adapter ohne Fähigkeiten wurde nicht erkannt"
);

let storageAccessorReads = 0;

const accessorStorageAdapter = {
  adapterKind:
    "accaoui_exam_history_snapshot_storage_adapter_v1",
  contractVersion: 1,
  write() {},
  delete() {}
};

Object.defineProperty(
  accessorStorageAdapter,
  "read",
  {
    enumerable: true,
    get() {
      storageAccessorReads += 1;
      throw new Error(
        "Readiness darf Capability-Getter nicht ausführen."
      );
    }
  }
);

const accessorStorageReadiness =
  adapter.mapParticipantFullExamResultHistorySnapshotStorageAdapterReadiness({
    storageAdapter:
      accessorStorageAdapter
  });

assert(
  accessorStorageReadiness.isValid === false &&
  accessorStorageReadiness.reason ===
    "storage_adapter_capability_accessor_not_allowed" &&
  storageAccessorReads === 0,
  "Capability-Accessor wurde nicht geschlossen abgelehnt"
);

const invalidStorageReadiness =
  adapter.mapParticipantFullExamResultHistorySnapshotStorageAdapterReadiness({
    storageAdapter: {
      adapterKind:
        "falscher_adapter",
      contractVersion: 1,
      read() {},
      write() {},
      delete() {}
    }
  });

expectEqual(
  invalidStorageReadiness.reason,
  "storage_adapter_kind_invalid",
  "Ungültiger Storage-Adapter-Marker"
);

const persistenceWritePlan =
  adapter.mapParticipantFullExamResultHistorySnapshotPersistenceOperationPlan({
    persistenceState:
      persistenceSave,
    adapterReadinessState:
      fullStorageReadiness,
    privateField:
      "nicht übernehmen"
  });

assert(
  persistenceWritePlan.status ===
    "exam_result_history_persistence_operation_plan_ready" &&
  persistenceWritePlan.canPlanOperation === true &&
  persistenceWritePlan.canExecuteStorage === false &&
  persistenceWritePlan.operation ===
    "write" &&
  persistenceWritePlan.requiredCapability ===
    "write" &&
  persistenceWritePlan.serializedJson ===
    persistenceSave.serializedJson &&
  storageAdapterOperationCalls === 0,
  "Write-Operationsplan wurde nicht sicher erstellt"
);

assert(
  !Object.prototype.hasOwnProperty.call(
    persistenceWritePlan,
    "privateField"
  ),
  "Unbekanntes Operationsplan-Feld wurde übernommen"
);

const readOnlyStorageReadiness =
  adapter.mapParticipantFullExamResultHistorySnapshotStorageAdapterReadiness({
    storageAdapter: {
      adapterKind:
        "accaoui_exam_history_snapshot_storage_adapter_v1",
      contractVersion: 1,
      read() {
        storageAdapterOperationCalls += 1;
      }
    }
  });

const persistenceReadPlan =
  adapter.mapParticipantFullExamResultHistorySnapshotPersistenceOperationPlan({
    persistenceState:
      persistenceLoad,
    adapterReadinessState:
      readOnlyStorageReadiness
  });

assert(
  persistenceReadPlan.status ===
    "exam_result_history_persistence_operation_plan_ready" &&
  persistenceReadPlan.operation ===
    "read" &&
  persistenceReadPlan.requiredCapability ===
    "read" &&
  persistenceReadPlan.hasValidatedLoadState ===
    true &&
  persistenceReadPlan.serializedJson ===
    null &&
  storageAdapterOperationCalls === 0,
  "Read-Operationsplan wurde nicht sicher erstellt"
);

const persistenceDeletePlan =
  adapter.mapParticipantFullExamResultHistorySnapshotPersistenceOperationPlan({
    persistenceState:
      persistenceDelete,
    adapterReadinessState:
      fullStorageReadiness
  });

assert(
  persistenceDeletePlan.canPlanOperation ===
    true &&
  persistenceDeletePlan.operation ===
    "delete" &&
  persistenceDeletePlan.requiredCapability ===
    "delete" &&
  storageAdapterOperationCalls === 0,
  "Delete-Operationsplan wurde nicht sicher erstellt"
);

const blockedDeletePlan =
  adapter.mapParticipantFullExamResultHistorySnapshotPersistenceOperationPlan({
    persistenceState:
      persistenceDelete,
    adapterReadinessState:
      readOnlyStorageReadiness
  });

assert(
  blockedDeletePlan.status ===
    "exam_result_history_persistence_operation_plan_blocked" &&
  blockedDeletePlan.canPlanOperation ===
    false &&
  blockedDeletePlan.operation ===
    "delete" &&
  blockedDeletePlan.reason ===
    "persistence_operation_plan_capability_unavailable",
  "Fehlende Delete-Fähigkeit wurde nicht blockiert"
);

const invalidPersistencePlan =
  adapter.mapParticipantFullExamResultHistorySnapshotPersistenceOperationPlan({
    persistenceState:
      persistenceInvalidKey,
    adapterReadinessState:
      fullStorageReadiness
  });

expectEqual(
  invalidPersistencePlan.reason,
  "persistence_operation_plan_persistence_state_invalid",
  "Ungültiger Persistenzstate im Operationsplan"
);

const invalidReadinessPlan =
  adapter.mapParticipantFullExamResultHistorySnapshotPersistenceOperationPlan({
    persistenceState:
      persistenceSave,
    adapterReadinessState:
      invalidStorageReadiness
  });

expectEqual(
  invalidReadinessPlan.reason,
  "persistence_operation_plan_readiness_state_invalid",
  "Ungültiger Readiness-State im Operationsplan"
);

const persistenceWriteRelease =
  adapter.mapParticipantFullExamResultHistorySnapshotPersistenceOperationReleaseState({
    operationPlanState:
      persistenceWritePlan,
    persistenceState:
      persistenceSave,
    adapterReadinessState:
      fullStorageReadiness,
    privateField:
      "nicht übernehmen"
  });

assert(
  persistenceWriteRelease.status ===
    "exam_result_history_persistence_operation_release_ready" &&
  persistenceWriteRelease.isValid === true &&
  persistenceWriteRelease.canReleaseOperation ===
    true &&
  persistenceWriteRelease.canExecuteStorage ===
    false &&
  persistenceWriteRelease.operation ===
    "write" &&
  persistenceWriteRelease.serializedJson ===
    persistenceSave.serializedJson &&
  typeof persistenceWriteRelease.adapterReadinessFingerprint ===
    "string" &&
  storageAdapterOperationCalls === 0,
  "Write-Operationsfreigabe wurde nicht sicher erstellt"
);

assert(
  !Object.prototype.hasOwnProperty.call(
    persistenceWriteRelease,
    "privateField"
  ),
  "Unbekanntes Freigabefeld wurde übernommen"
);

const persistenceReadRelease =
  adapter.mapParticipantFullExamResultHistorySnapshotPersistenceOperationReleaseState({
    operationPlanState:
      persistenceReadPlan,
    persistenceState:
      persistenceLoad,
    adapterReadinessState:
      readOnlyStorageReadiness
  });

assert(
  persistenceReadRelease.canReleaseOperation ===
    true &&
  persistenceReadRelease.operation ===
    "read" &&
  persistenceReadRelease.hasValidatedLoadState ===
    true &&
  persistenceReadRelease.serializedJson ===
    null &&
  storageAdapterOperationCalls === 0,
  "Read-Operationsfreigabe wurde nicht sicher erstellt"
);

const persistenceDeleteRelease =
  adapter.mapParticipantFullExamResultHistorySnapshotPersistenceOperationReleaseState({
    operationPlanState:
      persistenceDeletePlan,
    persistenceState:
      persistenceDelete,
    adapterReadinessState:
      fullStorageReadiness
  });

assert(
  persistenceDeleteRelease.canReleaseOperation ===
    true &&
  persistenceDeleteRelease.operation ===
    "delete" &&
  storageAdapterOperationCalls === 0,
  "Delete-Operationsfreigabe wurde nicht sicher erstellt"
);

const writeOnlyStorageReadiness =
  adapter.mapParticipantFullExamResultHistorySnapshotStorageAdapterReadiness({
    storageAdapter: {
      adapterKind:
        "accaoui_exam_history_snapshot_storage_adapter_v1",
      contractVersion: 1,
      write() {
        storageAdapterOperationCalls += 1;
      }
    }
  });

const changedReadinessRelease =
  adapter.mapParticipantFullExamResultHistorySnapshotPersistenceOperationReleaseState({
    operationPlanState:
      persistenceWritePlan,
    persistenceState:
      persistenceSave,
    adapterReadinessState:
      writeOnlyStorageReadiness
  });

assert(
  changedReadinessRelease.status ===
    "exam_result_history_persistence_operation_release_blocked" &&
  changedReadinessRelease.canReleaseOperation ===
    false &&
  changedReadinessRelease.reason ===
    "persistence_operation_release_readiness_changed" &&
  storageAdapterOperationCalls === 0,
  "Veränderte Adapter-Readiness wurde nicht blockiert"
);

const tamperedWritePlan = {
  ...persistenceWritePlan,
  serializedByteLength:
    persistenceWritePlan.serializedByteLength + 1
};

const tamperedPlanRelease =
  adapter.mapParticipantFullExamResultHistorySnapshotPersistenceOperationReleaseState({
    operationPlanState:
      tamperedWritePlan,
    persistenceState:
      persistenceSave,
    adapterReadinessState:
      fullStorageReadiness
  });

assert(
  tamperedPlanRelease.status ===
    "exam_result_history_persistence_operation_release_blocked" &&
  tamperedPlanRelease.reason ===
    "persistence_operation_release_plan_mismatch",
  "Manipulierter Operationsplan wurde nicht blockiert"
);

const invalidOperationRelease =
  adapter.mapParticipantFullExamResultHistorySnapshotPersistenceOperationReleaseState({
    operationPlanState:
      blockedDeletePlan,
    persistenceState:
      persistenceDelete,
    adapterReadinessState:
      readOnlyStorageReadiness
  });

expectEqual(
  invalidOperationRelease.reason,
  "persistence_operation_release_plan_invalid",
  "Ungültiger Operationsplan in Freigabe"
);

const persistenceWriteExecution =
  adapter.guardParticipantFullExamResultHistorySnapshotPersistenceExecution({
    releaseState:
      persistenceWriteRelease,
    persistenceState:
      persistenceSave,
    storageAdapter:
      fullStorageAdapter,
    privateField:
      "nicht übernehmen"
  });

assert(
  persistenceWriteExecution.status ===
    "exam_result_history_persistence_execution_guard_ready" &&
  persistenceWriteExecution.isValid === true &&
  persistenceWriteExecution.canPrepareExecution ===
    true &&
  persistenceWriteExecution.canInvokeLater ===
    true &&
  persistenceWriteExecution.canExecuteStorage ===
    false &&
  persistenceWriteExecution.isMethodReferenceValidated ===
    true &&
  persistenceWriteExecution.operation ===
    "write" &&
  persistenceWriteExecution.operationArgumentCount ===
    2 &&
  persistenceWriteExecution.serializedJson ===
    persistenceSave.serializedJson &&
  storageAdapterOperationCalls === 0,
  "Write-Ausführung wurde nicht sicher vorbereitet"
);

assert(
  !Object.prototype.hasOwnProperty.call(
    persistenceWriteExecution,
    "storageAdapter"
  ) &&
  !Object.prototype.hasOwnProperty.call(
    persistenceWriteExecution,
    "privateField"
  ),
  "Adapter oder unbekanntes Feld wurde offengelegt"
);

const readExecutionAdapter = {
  adapterKind:
    "accaoui_exam_history_snapshot_storage_adapter_v1",
  contractVersion: 1,
  read() {
    storageAdapterOperationCalls += 1;
  }
};

const persistenceReadExecution =
  adapter.guardParticipantFullExamResultHistorySnapshotPersistenceExecution({
    releaseState:
      persistenceReadRelease,
    persistenceState:
      persistenceLoad,
    storageAdapter:
      readExecutionAdapter
  });

assert(
  persistenceReadExecution.canPrepareExecution ===
    true &&
  persistenceReadExecution.operation ===
    "read" &&
  persistenceReadExecution.operationArgumentCount ===
    1 &&
  persistenceReadExecution.serializedJson ===
    null &&
  persistenceReadExecution.hasValidatedLoadState ===
    true &&
  storageAdapterOperationCalls === 0,
  "Read-Ausführung wurde nicht sicher vorbereitet"
);

const persistenceDeleteExecution =
  adapter.guardParticipantFullExamResultHistorySnapshotPersistenceExecution({
    releaseState:
      persistenceDeleteRelease,
    persistenceState:
      persistenceDelete,
    storageAdapter:
      fullStorageAdapter
  });

assert(
  persistenceDeleteExecution.canPrepareExecution ===
    true &&
  persistenceDeleteExecution.operation ===
    "delete" &&
  persistenceDeleteExecution.operationArgumentCount ===
    1 &&
  storageAdapterOperationCalls === 0,
  "Delete-Ausführung wurde nicht sicher vorbereitet"
);

const changedExecutionAdapter = {
  adapterKind:
    "accaoui_exam_history_snapshot_storage_adapter_v1",
  contractVersion: 1,
  write() {
    storageAdapterOperationCalls += 1;
  }
};

const changedExecution =
  adapter.guardParticipantFullExamResultHistorySnapshotPersistenceExecution({
    releaseState:
      persistenceWriteRelease,
    persistenceState:
      persistenceSave,
    storageAdapter:
      changedExecutionAdapter
  });

expectEqual(
  changedExecution.reason,
  "persistence_execution_readiness_changed",
  "Veränderte Readiness im Ausführungs-Guard"
);

let executionAccessorReads = 0;

const accessorExecutionAdapter = {
  adapterKind:
    "accaoui_exam_history_snapshot_storage_adapter_v1",
  contractVersion: 1,
  read() {},
  delete() {}
};

Object.defineProperty(
  accessorExecutionAdapter,
  "write",
  {
    enumerable: true,
    get() {
      executionAccessorReads += 1;
      throw new Error(
        "Ausführungs-Guard darf Getter nicht ausführen."
      );
    }
  }
);

const accessorExecution =
  adapter.guardParticipantFullExamResultHistorySnapshotPersistenceExecution({
    releaseState:
      persistenceWriteRelease,
    persistenceState:
      persistenceSave,
    storageAdapter:
      accessorExecutionAdapter
  });

assert(
  accessorExecution.isValid === false &&
  accessorExecution.reason ===
    "storage_adapter_capability_accessor_not_allowed" &&
  executionAccessorReads === 0 &&
  storageAdapterOperationCalls === 0,
  "Accessor-Methode wurde nicht geschlossen blockiert"
);

const tamperedExecutionRelease = {
  ...persistenceWriteRelease,
  releaseIdentity:
    "exam_history_persistence_release:write:manipuliert"
};

const tamperedExecution =
  adapter.guardParticipantFullExamResultHistorySnapshotPersistenceExecution({
    releaseState:
      tamperedExecutionRelease,
    persistenceState:
      persistenceSave,
    storageAdapter:
      fullStorageAdapter
  });

expectEqual(
  tamperedExecution.reason,
  "persistence_execution_release_mismatch",
  "Manipulierte Freigabe im Ausführungs-Guard"
);

const persistenceWriteInvocation =
  adapter.mapParticipantFullExamResultHistorySnapshotPersistenceInvocationContract({
    executionState:
      persistenceWriteExecution,
    privateField:
      "nicht übernehmen"
  });

assert(
  persistenceWriteInvocation.status ===
    "exam_result_history_persistence_invocation_contract_ready" &&
  persistenceWriteInvocation.isValid === true &&
  persistenceWriteInvocation.canBuildInvocation ===
    true &&
  persistenceWriteInvocation.canInvokeLater ===
    true &&
  persistenceWriteInvocation.canExecuteStorage ===
    false &&
  persistenceWriteInvocation.methodName ===
    "write" &&
  persistenceWriteInvocation.invocationArgumentCount ===
    2 &&
  persistenceWriteInvocation.serializedByteLength ===
    persistenceWriteExecution.serializedByteLength &&
  storageAdapterOperationCalls === 0,
  "Write-Aufrufvertrag wurde nicht sicher erstellt"
);

expectJson(
  persistenceWriteInvocation.invocationArgumentNames,
  [
    "storageKey",
    "serializedJson"
  ],
  "Write-Argumentnamen"
);

expectJson(
  persistenceWriteInvocation.invocationArguments,
  [
    {
      position: 0,
      name: "storageKey",
      valueType: "string",
      value:
        persistenceSave.storageKey
    },
    {
      position: 1,
      name: "serializedJson",
      valueType: "string",
      value:
        persistenceSave.serializedJson
    }
  ],
  "Write-Argumenteschema"
);

assert(
  !Object.prototype.hasOwnProperty.call(
    persistenceWriteInvocation,
    "executionState"
  ) &&
  !Object.prototype.hasOwnProperty.call(
    persistenceWriteInvocation,
    "privateField"
  ),
  "Ausführungsstate oder unbekanntes Feld wurde übernommen"
);

const persistenceReadInvocation =
  adapter.mapParticipantFullExamResultHistorySnapshotPersistenceInvocationContract({
    executionState:
      persistenceReadExecution
  });

assert(
  persistenceReadInvocation.canBuildInvocation ===
    true &&
  persistenceReadInvocation.methodName ===
    "read" &&
  persistenceReadInvocation.invocationArgumentCount ===
    1 &&
  persistenceReadInvocation.hasValidatedLoadState ===
    true &&
  persistenceReadInvocation.serializedByteLength ===
    null &&
  storageAdapterOperationCalls === 0,
  "Read-Aufrufvertrag wurde nicht sicher erstellt"
);

expectJson(
  persistenceReadInvocation.invocationArgumentNames,
  [
    "storageKey"
  ],
  "Read-Argumentnamen"
);

const persistenceDeleteInvocation =
  adapter.mapParticipantFullExamResultHistorySnapshotPersistenceInvocationContract({
    executionState:
      persistenceDeleteExecution
  });

assert(
  persistenceDeleteInvocation.canBuildInvocation ===
    true &&
  persistenceDeleteInvocation.methodName ===
    "delete" &&
  persistenceDeleteInvocation.invocationArgumentCount ===
    1 &&
  persistenceDeleteInvocation.hasValidatedLoadState ===
    false &&
  storageAdapterOperationCalls === 0,
  "Delete-Aufrufvertrag wurde nicht sicher erstellt"
);

const tamperedInvocationExecution = {
  ...persistenceWriteExecution,
  operationArgumentCount: 1
};

const tamperedInvocation =
  adapter.mapParticipantFullExamResultHistorySnapshotPersistenceInvocationContract({
    executionState:
      tamperedInvocationExecution
  });

expectEqual(
  tamperedInvocation.reason,
  "persistence_invocation_contract_argument_count_invalid",
  "Manipulierte Argumentanzahl"
);

const invalidInvocation =
  adapter.mapParticipantFullExamResultHistorySnapshotPersistenceInvocationContract({
    executionState:
      changedExecution
  });

expectEqual(
  invalidInvocation.reason,
  "persistence_invocation_contract_execution_state_invalid",
  "Ungültiger Ausführungsstate im Aufrufvertrag"
);

const persistenceWritePackage =
  adapter.mapParticipantFullExamResultHistorySnapshotPersistenceInvocationPackageState({
    releaseState:
      persistenceWriteRelease,
    persistenceState:
      persistenceSave,
    storageAdapter:
      fullStorageAdapter,
    executionState:
      persistenceWriteExecution,
    invocationContractState:
      persistenceWriteInvocation,
    privateField:
      "nicht übernehmen"
  });

assert(
  persistenceWritePackage.status ===
    "exam_result_history_persistence_invocation_package_ready" &&
  persistenceWritePackage.isValid === true &&
  persistenceWritePackage.canPrepareInvocationPackage ===
    true &&
  persistenceWritePackage.canInvokeLater ===
    true &&
  persistenceWritePackage.canExecuteStorage ===
    false &&
  persistenceWritePackage.isMethodReferenceValidated ===
    true &&
  persistenceWritePackage.methodName ===
    "write" &&
  persistenceWritePackage.invocationArgumentCount ===
    2 &&
  storageAdapterOperationCalls === 0,
  "Write-Aufrufpaket wurde nicht sicher erstellt"
);

expectJson(
  persistenceWritePackage.invocationArguments,
  persistenceWriteInvocation.invocationArguments,
  "Write-Aufrufpaket-Argumente"
);

assert(
  !Object.prototype.hasOwnProperty.call(
    persistenceWritePackage,
    "storageAdapter"
  ) &&
  !Object.prototype.hasOwnProperty.call(
    persistenceWritePackage,
    "executionState"
  ) &&
  !Object.prototype.hasOwnProperty.call(
    persistenceWritePackage,
    "invocationContractState"
  ) &&
  !Object.prototype.hasOwnProperty.call(
    persistenceWritePackage,
    "privateField"
  ),
  "Adapter oder interne Aufrufpaket-Felder wurden übernommen"
);

const persistenceReadPackage =
  adapter.mapParticipantFullExamResultHistorySnapshotPersistenceInvocationPackageState({
    releaseState:
      persistenceReadRelease,
    persistenceState:
      persistenceLoad,
    storageAdapter:
      readExecutionAdapter,
    executionState:
      persistenceReadExecution,
    invocationContractState:
      persistenceReadInvocation
  });

assert(
  persistenceReadPackage.canPrepareInvocationPackage ===
    true &&
  persistenceReadPackage.methodName ===
    "read" &&
  persistenceReadPackage.invocationArgumentCount ===
    1 &&
  persistenceReadPackage.hasValidatedLoadState ===
    true &&
  persistenceReadPackage.serializedByteLength ===
    null &&
  storageAdapterOperationCalls === 0,
  "Read-Aufrufpaket wurde nicht sicher erstellt"
);

const persistenceDeletePackage =
  adapter.mapParticipantFullExamResultHistorySnapshotPersistenceInvocationPackageState({
    releaseState:
      persistenceDeleteRelease,
    persistenceState:
      persistenceDelete,
    storageAdapter:
      fullStorageAdapter,
    executionState:
      persistenceDeleteExecution,
    invocationContractState:
      persistenceDeleteInvocation
  });

assert(
  persistenceDeletePackage.canPrepareInvocationPackage ===
    true &&
  persistenceDeletePackage.methodName ===
    "delete" &&
  persistenceDeletePackage.invocationArgumentCount ===
    1 &&
  persistenceDeletePackage.hasValidatedLoadState ===
    false &&
  storageAdapterOperationCalls === 0,
  "Delete-Aufrufpaket wurde nicht sicher erstellt"
);

const changedAdapterPackage =
  adapter.mapParticipantFullExamResultHistorySnapshotPersistenceInvocationPackageState({
    releaseState:
      persistenceWriteRelease,
    persistenceState:
      persistenceSave,
    storageAdapter:
      changedExecutionAdapter,
    executionState:
      persistenceWriteExecution,
    invocationContractState:
      persistenceWriteInvocation
  });

expectEqual(
  changedAdapterPackage.reason,
  "persistence_invocation_package_recomputed_execution_invalid",
  "Veränderter Adapter im Aufrufpaket"
);

const tamperedPackageInvocation = {
  ...persistenceWriteInvocation,
  invocationIdentity:
    "exam_history_persistence_invocation:write:manipuliert"
};

const tamperedInvocationPackage =
  adapter.mapParticipantFullExamResultHistorySnapshotPersistenceInvocationPackageState({
    releaseState:
      persistenceWriteRelease,
    persistenceState:
      persistenceSave,
    storageAdapter:
      fullStorageAdapter,
    executionState:
      persistenceWriteExecution,
    invocationContractState:
      tamperedPackageInvocation
  });

expectEqual(
  tamperedInvocationPackage.reason,
  "persistence_invocation_package_contract_mismatch",
  "Manipulierter Aufrufvertrag im Aufrufpaket"
);

const tamperedPackageExecution = {
  ...persistenceWriteExecution,
  executionIdentity:
    "exam_history_persistence_execution:write:manipuliert"
};

const tamperedExecutionPackage =
  adapter.mapParticipantFullExamResultHistorySnapshotPersistenceInvocationPackageState({
    releaseState:
      persistenceWriteRelease,
    persistenceState:
      persistenceSave,
    storageAdapter:
      fullStorageAdapter,
    executionState:
      tamperedPackageExecution,
    invocationContractState:
      persistenceWriteInvocation
  });

expectEqual(
  tamperedExecutionPackage.reason,
  "persistence_invocation_package_execution_state_mismatch",
  "Manipulierter Ausführungsstate im Aufrufpaket"
);

const persistenceReadResult =
  adapter.mapParticipantFullExamResultHistorySnapshotPersistenceResultContract({
    invocationPackageState:
      persistenceReadPackage,
    operationResult:
      persistenceSave.serializedJson,
    privateField:
      "nicht übernehmen"
  });

assert(
  persistenceReadResult.status ===
    "exam_result_history_persistence_result_read_ready" &&
  persistenceReadResult.isValid === true &&
  persistenceReadResult.canAcceptResult ===
    true &&
  persistenceReadResult.canResumeSnapshot ===
    true &&
  persistenceReadResult.didRead === true &&
  persistenceReadResult.snapshotPayload &&
  persistenceReadResult.resumeState.canResume ===
    true &&
  persistenceReadResult.requestIdentity ===
    persistenceReadPackage.requestIdentity &&
  storageAdapterOperationCalls === 0,
  "Read-Ergebnis wurde nicht sicher normalisiert"
);

assert(
  !Object.prototype.hasOwnProperty.call(
    persistenceReadResult,
    "operationResult"
  ) &&
  !Object.prototype.hasOwnProperty.call(
    persistenceReadResult,
    "serializedJson"
  ) &&
  !Object.prototype.hasOwnProperty.call(
    persistenceReadResult,
    "privateField"
  ),
  "Roher Rückgabewert oder unbekanntes Ergebnisfeld wurde übernommen"
);

const persistenceReadEmptyResult =
  adapter.mapParticipantFullExamResultHistorySnapshotPersistenceResultContract({
    invocationPackageState:
      persistenceReadPackage,
    operationResult:
      null
  });

assert(
  persistenceReadEmptyResult.status ===
    "exam_result_history_persistence_result_read_empty" &&
  persistenceReadEmptyResult.didRead ===
    true &&
  persistenceReadEmptyResult.isEmpty ===
    true &&
  persistenceReadEmptyResult.canResumeSnapshot ===
    false,
  "Leeres Read-Ergebnis wurde nicht sicher normalisiert"
);

const persistenceWriteResult =
  adapter.mapParticipantFullExamResultHistorySnapshotPersistenceResultContract({
    invocationPackageState:
      persistenceWritePackage,
    operationResult:
      true
  });

assert(
  persistenceWriteResult.status ===
    "exam_result_history_persistence_result_write_confirmed" &&
  persistenceWriteResult.didWrite ===
    true &&
  persistenceWriteResult.serializedByteLength ===
    persistenceWritePackage.serializedByteLength &&
  persistenceWriteResult.canExecuteStorage ===
    false &&
  storageAdapterOperationCalls === 0,
  "Write-Ergebnis wurde nicht sicher bestätigt"
);

const persistenceDeleteResult =
  adapter.mapParticipantFullExamResultHistorySnapshotPersistenceResultContract({
    invocationPackageState:
      persistenceDeletePackage,
    operationResult:
      true
  });

assert(
  persistenceDeleteResult.status ===
    "exam_result_history_persistence_result_delete_confirmed" &&
  persistenceDeleteResult.didDelete ===
    true &&
  persistenceDeleteResult.wasAlreadyAbsent ===
    false &&
  storageAdapterOperationCalls === 0,
  "Delete-Ergebnis wurde nicht sicher bestätigt"
);

const persistenceDeleteAbsentResult =
  adapter.mapParticipantFullExamResultHistorySnapshotPersistenceResultContract({
    invocationPackageState:
      persistenceDeletePackage,
    operationResult:
      false
  });

assert(
  persistenceDeleteAbsentResult.status ===
    "exam_result_history_persistence_result_delete_absent" &&
  persistenceDeleteAbsentResult.didDelete ===
    false &&
  persistenceDeleteAbsentResult.wasAlreadyAbsent ===
    true &&
  persistenceDeleteAbsentResult.isEmpty ===
    true,
  "Bereits fehlender Snapshot wurde nicht idempotent normalisiert"
);

const invalidWriteResult =
  adapter.mapParticipantFullExamResultHistorySnapshotPersistenceResultContract({
    invocationPackageState:
      persistenceWritePackage,
    operationResult:
      false
  });

expectEqual(
  invalidWriteResult.reason,
  "persistence_result_write_confirmation_invalid",
  "Ungültige Write-Bestätigung"
);

const invalidReadResult =
  adapter.mapParticipantFullExamResultHistorySnapshotPersistenceResultContract({
    invocationPackageState:
      persistenceReadPackage,
    operationResult:
      persistenceSave.serializedJson + " "
  });

expectEqual(
  invalidReadResult.reason,
  "snapshot_deserialization_json_not_canonical",
  "Nicht kanonischer Read-Rückgabewert"
);

const tamperedResultPackage = {
  ...persistenceReadPackage,
  invocationPackageIdentity:
    "exam_history_persistence_invocation_package:read:manipuliert"
};

const tamperedPackageResult =
  adapter.mapParticipantFullExamResultHistorySnapshotPersistenceResultContract({
    invocationPackageState:
      tamperedResultPackage,
    operationResult:
      persistenceSave.serializedJson
  });

expectEqual(
  tamperedPackageResult.reason,
  "persistence_result_identity_invalid",
  "Manipuliertes Aufrufpaket im Ergebnisvertrag"
);

const acceptedReadResult =
  adapter.guardParticipantFullExamResultHistorySnapshotPersistenceResultAcceptance({
    activeInvocationPackageState:
      persistenceReadPackage,
    resultContractState:
      persistenceReadResult,
    privateField:
      "nicht übernehmen"
  });

assert(
  acceptedReadResult.status ===
    "exam_result_history_persistence_result_acceptance_ready" &&
  acceptedReadResult.isValid === true &&
  acceptedReadResult.canApplyResult ===
    true &&
  acceptedReadResult.didAcceptResult ===
    true &&
  acceptedReadResult.isStaleResult ===
    false &&
  acceptedReadResult.canResumeSnapshot ===
    true &&
  acceptedReadResult.resumeState.canResume ===
    true &&
  acceptedReadResult.requestIdentity ===
    persistenceReadPackage.requestIdentity &&
  storageAdapterOperationCalls === 0,
  "Aktuelles Read-Ergebnis wurde nicht sicher angenommen"
);

assert(
  !Object.prototype.hasOwnProperty.call(
    acceptedReadResult,
    "activeInvocationPackageState"
  ) &&
  !Object.prototype.hasOwnProperty.call(
    acceptedReadResult,
    "resultContractState"
  ) &&
  !Object.prototype.hasOwnProperty.call(
    acceptedReadResult,
    "privateField"
  ),
  "Interne Ergebnisannahme-Felder wurden übernommen"
);

const acceptedEmptyReadResult =
  adapter.guardParticipantFullExamResultHistorySnapshotPersistenceResultAcceptance({
    activeInvocationPackageState:
      persistenceReadPackage,
    resultContractState:
      persistenceReadEmptyResult
  });

assert(
  acceptedEmptyReadResult.canApplyResult ===
    true &&
  acceptedEmptyReadResult.didAcceptResult ===
    true &&
  acceptedEmptyReadResult.didRead ===
    true &&
  acceptedEmptyReadResult.isEmpty ===
    true &&
  acceptedEmptyReadResult.canResumeSnapshot ===
    false,
  "Leeres aktuelles Read-Ergebnis wurde nicht angenommen"
);

const acceptedWriteResult =
  adapter.guardParticipantFullExamResultHistorySnapshotPersistenceResultAcceptance({
    activeInvocationPackageState:
      persistenceWritePackage,
    resultContractState:
      persistenceWriteResult
  });

assert(
  acceptedWriteResult.canApplyResult ===
    true &&
  acceptedWriteResult.didWrite ===
    true &&
  acceptedWriteResult.serializedByteLength ===
    persistenceWritePackage.serializedByteLength &&
  storageAdapterOperationCalls === 0,
  "Aktuelles Write-Ergebnis wurde nicht sicher angenommen"
);

const acceptedDeleteAbsentResult =
  adapter.guardParticipantFullExamResultHistorySnapshotPersistenceResultAcceptance({
    activeInvocationPackageState:
      persistenceDeletePackage,
    resultContractState:
      persistenceDeleteAbsentResult
  });

assert(
  acceptedDeleteAbsentResult.canApplyResult ===
    true &&
  acceptedDeleteAbsentResult.didDelete ===
    false &&
  acceptedDeleteAbsentResult.wasAlreadyAbsent ===
    true &&
  acceptedDeleteAbsentResult.isEmpty ===
    true,
  "Idempotentes Delete-Ergebnis wurde nicht angenommen"
);

const stalePersistenceResult =
  adapter.guardParticipantFullExamResultHistorySnapshotPersistenceResultAcceptance({
    activeInvocationPackageState:
      persistenceDeletePackage,
    resultContractState:
      persistenceReadResult
  });

assert(
  stalePersistenceResult.status ===
    "exam_result_history_persistence_result_acceptance_stale_ignored" &&
  stalePersistenceResult.isValid === true &&
  stalePersistenceResult.canApplyResult ===
    false &&
  stalePersistenceResult.didAcceptResult ===
    false &&
  stalePersistenceResult.isStaleResult ===
    true &&
  stalePersistenceResult.reason ===
    "persistence_result_acceptance_stale_package",
  "Veraltetes Persistenzergebnis wurde nicht ignoriert"
);

const tamperedAcceptedResultState = {
  ...persistenceReadResult,
  requestIdentity:
    "exam_history_request:999:20:0"
};

const tamperedAcceptedResult =
  adapter.guardParticipantFullExamResultHistorySnapshotPersistenceResultAcceptance({
    activeInvocationPackageState:
      persistenceReadPackage,
    resultContractState:
      tamperedAcceptedResultState
  });

expectEqual(
  tamperedAcceptedResult.reason,
  "persistence_result_acceptance_result_identity_mismatch",
  "Manipulierte Ergebnisidentität"
);

const invalidResultAcceptance =
  adapter.guardParticipantFullExamResultHistorySnapshotPersistenceResultAcceptance({
    activeInvocationPackageState:
      persistenceWritePackage,
    resultContractState:
      invalidWriteResult
  });

expectEqual(
  invalidResultAcceptance.reason,
  "persistence_result_acceptance_result_state_invalid",
  "Ungültiger Ergebnisvertrag in Ergebnisannahme"
);

const persistenceReadCompletion =
  adapter.mapParticipantFullExamResultHistorySnapshotPersistenceCompletionState({
    acceptanceState:
      acceptedReadResult,
    privateField:
      "nicht übernehmen"
  });

assert(
  persistenceReadCompletion.status ===
    "exam_result_history_persistence_completion_read_ready" &&
  persistenceReadCompletion.isValid === true &&
  persistenceReadCompletion.canFinalizePersistence ===
    true &&
  persistenceReadCompletion.isTerminal ===
    true &&
  persistenceReadCompletion.isSuccessful ===
    true &&
  persistenceReadCompletion.terminalOutcome ===
    "read_ready" &&
  persistenceReadCompletion.canResumeSnapshot ===
    true &&
  persistenceReadCompletion.resumeState.canResume ===
    true &&
  persistenceReadCompletion.canExecuteStorage ===
    false &&
  storageAdapterOperationCalls === 0,
  "Read-Ergebnis wurde nicht sicher abgeschlossen"
);

assert(
  !Object.prototype.hasOwnProperty.call(
    persistenceReadCompletion,
    "acceptanceState"
  ) &&
  !Object.prototype.hasOwnProperty.call(
    persistenceReadCompletion,
    "privateField"
  ),
  "Interne Abschlussfelder wurden übernommen"
);

const persistenceReadEmptyCompletion =
  adapter.mapParticipantFullExamResultHistorySnapshotPersistenceCompletionState({
    acceptanceState:
      acceptedEmptyReadResult
  });

assert(
  persistenceReadEmptyCompletion.status ===
    "exam_result_history_persistence_completion_read_empty" &&
  persistenceReadEmptyCompletion.isTerminal ===
    true &&
  persistenceReadEmptyCompletion.didRead ===
    true &&
  persistenceReadEmptyCompletion.isEmpty ===
    true &&
  persistenceReadEmptyCompletion.canResumeSnapshot ===
    false,
  "Leeres Read-Ergebnis wurde nicht terminal abgeschlossen"
);

const persistenceWriteCompletion =
  adapter.mapParticipantFullExamResultHistorySnapshotPersistenceCompletionState({
    acceptanceState:
      acceptedWriteResult
  });

assert(
  persistenceWriteCompletion.status ===
    "exam_result_history_persistence_completion_write_confirmed" &&
  persistenceWriteCompletion.terminalOutcome ===
    "write_confirmed" &&
  persistenceWriteCompletion.didWrite ===
    true &&
  persistenceWriteCompletion.serializedByteLength ===
    persistenceWritePackage.serializedByteLength &&
  storageAdapterOperationCalls === 0,
  "Write-Ergebnis wurde nicht terminal abgeschlossen"
);

const acceptedDeleteResult =
  adapter.guardParticipantFullExamResultHistorySnapshotPersistenceResultAcceptance({
    activeInvocationPackageState:
      persistenceDeletePackage,
    resultContractState:
      persistenceDeleteResult
  });

const persistenceDeleteCompletion =
  adapter.mapParticipantFullExamResultHistorySnapshotPersistenceCompletionState({
    acceptanceState:
      acceptedDeleteResult
  });

assert(
  persistenceDeleteCompletion.status ===
    "exam_result_history_persistence_completion_delete_confirmed" &&
  persistenceDeleteCompletion.terminalOutcome ===
    "delete_confirmed" &&
  persistenceDeleteCompletion.didDelete ===
    true &&
  persistenceDeleteCompletion.wasAlreadyAbsent ===
    false,
  "Delete-Ergebnis wurde nicht terminal abgeschlossen"
);

const persistenceDeleteAbsentCompletion =
  adapter.mapParticipantFullExamResultHistorySnapshotPersistenceCompletionState({
    acceptanceState:
      acceptedDeleteAbsentResult
  });

assert(
  persistenceDeleteAbsentCompletion.status ===
    "exam_result_history_persistence_completion_delete_absent" &&
  persistenceDeleteAbsentCompletion.terminalOutcome ===
    "delete_absent" &&
  persistenceDeleteAbsentCompletion.didDelete ===
    false &&
  persistenceDeleteAbsentCompletion.wasAlreadyAbsent ===
    true &&
  persistenceDeleteAbsentCompletion.isEmpty ===
    true,
  "Idempotentes Delete-Ergebnis wurde nicht terminal abgeschlossen"
);

const stalePersistenceCompletion =
  adapter.mapParticipantFullExamResultHistorySnapshotPersistenceCompletionState({
    acceptanceState:
      stalePersistenceResult
  });

expectEqual(
  stalePersistenceCompletion.reason,
  "persistence_completion_acceptance_state_invalid",
  "Veraltetes Ergebnis im Abschlussstate"
);

const tamperedCompletionAcceptance = {
  ...acceptedReadResult,
  resultStatus:
    "exam_result_history_persistence_result_read_empty"
};

const tamperedPersistenceCompletion =
  adapter.mapParticipantFullExamResultHistorySnapshotPersistenceCompletionState({
    acceptanceState:
      tamperedCompletionAcceptance
  });

expectEqual(
  tamperedPersistenceCompletion.reason,
  "persistence_completion_read_empty_invalid",
  "Manipulierter Read-Abschlussstate"
);

const persistenceReadCycle =
  adapter.mapParticipantFullExamResultHistorySnapshotPersistenceCycleState({
    invocationPackageState:
      persistenceReadPackage,
    resultContractState:
      persistenceReadResult,
    acceptanceState:
      acceptedReadResult,
    completionState:
      persistenceReadCompletion,
    privateField:
      "nicht übernehmen"
  });

assert(
  persistenceReadCycle.status ===
    "exam_result_history_persistence_cycle_completed" &&
  persistenceReadCycle.isValid === true &&
  persistenceReadCycle.canFinalizeCycle ===
    true &&
  persistenceReadCycle.isTerminal ===
    true &&
  persistenceReadCycle.isSuccessful ===
    true &&
  persistenceReadCycle.terminalOutcome ===
    "read_ready" &&
  persistenceReadCycle.canResumeSnapshot ===
    true &&
  persistenceReadCycle.resumeState.canResume ===
    true &&
  persistenceReadCycle.canExecuteStorage ===
    false &&
  storageAdapterOperationCalls === 0,
  "Read-Persistenzzyklus wurde nicht sicher abgeschlossen"
);

assert(
  !Object.prototype.hasOwnProperty.call(
    persistenceReadCycle,
    "invocationPackageState"
  ) &&
  !Object.prototype.hasOwnProperty.call(
    persistenceReadCycle,
    "resultContractState"
  ) &&
  !Object.prototype.hasOwnProperty.call(
    persistenceReadCycle,
    "acceptanceState"
  ) &&
  !Object.prototype.hasOwnProperty.call(
    persistenceReadCycle,
    "completionState"
  ) &&
  !Object.prototype.hasOwnProperty.call(
    persistenceReadCycle,
    "privateField"
  ),
  "Interne Persistenzzyklus-Felder wurden übernommen"
);

const persistenceReadEmptyCycle =
  adapter.mapParticipantFullExamResultHistorySnapshotPersistenceCycleState({
    invocationPackageState:
      persistenceReadPackage,
    resultContractState:
      persistenceReadEmptyResult,
    acceptanceState:
      acceptedEmptyReadResult,
    completionState:
      persistenceReadEmptyCompletion
  });

assert(
  persistenceReadEmptyCycle.terminalOutcome ===
    "read_empty" &&
  persistenceReadEmptyCycle.didRead ===
    true &&
  persistenceReadEmptyCycle.isEmpty ===
    true &&
  persistenceReadEmptyCycle.canResumeSnapshot ===
    false,
  "Leerer Read-Zyklus wurde nicht sicher abgeschlossen"
);

const persistenceWriteCycle =
  adapter.mapParticipantFullExamResultHistorySnapshotPersistenceCycleState({
    invocationPackageState:
      persistenceWritePackage,
    resultContractState:
      persistenceWriteResult,
    acceptanceState:
      acceptedWriteResult,
    completionState:
      persistenceWriteCompletion
  });

assert(
  persistenceWriteCycle.terminalOutcome ===
    "write_confirmed" &&
  persistenceWriteCycle.didWrite ===
    true &&
  persistenceWriteCycle.serializedByteLength ===
    persistenceWritePackage.serializedByteLength &&
  storageAdapterOperationCalls === 0,
  "Write-Persistenzzyklus wurde nicht sicher abgeschlossen"
);

const persistenceDeleteCycle =
  adapter.mapParticipantFullExamResultHistorySnapshotPersistenceCycleState({
    invocationPackageState:
      persistenceDeletePackage,
    resultContractState:
      persistenceDeleteResult,
    acceptanceState:
      acceptedDeleteResult,
    completionState:
      persistenceDeleteCompletion
  });

assert(
  persistenceDeleteCycle.terminalOutcome ===
    "delete_confirmed" &&
  persistenceDeleteCycle.didDelete ===
    true &&
  persistenceDeleteCycle.wasAlreadyAbsent ===
    false,
  "Delete-Persistenzzyklus wurde nicht sicher abgeschlossen"
);

const persistenceDeleteAbsentCycle =
  adapter.mapParticipantFullExamResultHistorySnapshotPersistenceCycleState({
    invocationPackageState:
      persistenceDeletePackage,
    resultContractState:
      persistenceDeleteAbsentResult,
    acceptanceState:
      acceptedDeleteAbsentResult,
    completionState:
      persistenceDeleteAbsentCompletion
  });

assert(
  persistenceDeleteAbsentCycle.terminalOutcome ===
    "delete_absent" &&
  persistenceDeleteAbsentCycle.didDelete ===
    false &&
  persistenceDeleteAbsentCycle.wasAlreadyAbsent ===
    true &&
  persistenceDeleteAbsentCycle.isEmpty ===
    true,
  "Idempotenter Delete-Zyklus wurde nicht sicher abgeschlossen"
);

const tamperedCycleAcceptance = {
  ...acceptedReadResult,
  didRead: false
};

const tamperedAcceptanceCycle =
  adapter.mapParticipantFullExamResultHistorySnapshotPersistenceCycleState({
    invocationPackageState:
      persistenceReadPackage,
    resultContractState:
      persistenceReadResult,
    acceptanceState:
      tamperedCycleAcceptance,
    completionState:
      persistenceReadCompletion
  });

expectEqual(
  tamperedAcceptanceCycle.reason,
  "persistence_cycle_acceptance_state_mismatch",
  "Manipulierter Ergebnisannahme-State im Zyklus"
);

const tamperedCycleCompletion = {
  ...persistenceReadCompletion,
  terminalOutcome:
    "read_empty"
};

const tamperedCompletionCycle =
  adapter.mapParticipantFullExamResultHistorySnapshotPersistenceCycleState({
    invocationPackageState:
      persistenceReadPackage,
    resultContractState:
      persistenceReadResult,
    acceptanceState:
      acceptedReadResult,
    completionState:
      tamperedCycleCompletion
  });

expectEqual(
  tamperedCompletionCycle.reason,
  "persistence_cycle_completion_state_mismatch",
  "Manipulierter Abschlussstate im Zyklus"
);

const stalePersistenceCycle =
  adapter.mapParticipantFullExamResultHistorySnapshotPersistenceCycleState({
    invocationPackageState:
      persistenceDeletePackage,
    resultContractState:
      persistenceReadResult,
    acceptanceState:
      stalePersistenceResult,
    completionState:
      persistenceDeleteAbsentCompletion
  });

expectEqual(
  stalePersistenceCycle.reason,
  "persistence_cycle_acceptance_state_invalid",
  "Veraltetes Ergebnis im Persistenzzyklus"
);

const persistenceReadRepetition =
  adapter.guardParticipantFullExamResultHistorySnapshotPersistenceCycleRepetition({
    cycleState:
      persistenceReadCycle,
    completedCycleIdentities: [],
    privateField:
      "nicht übernehmen"
  });

assert(
  persistenceReadRepetition.status ===
    "exam_result_history_persistence_cycle_repetition_ready" &&
  persistenceReadRepetition.isValid === true &&
  persistenceReadRepetition.canAcceptCycleOnce ===
    true &&
  persistenceReadRepetition.canRegisterCycleIdentityLater ===
    true &&
  persistenceReadRepetition.isDuplicateCycle ===
    false &&
  persistenceReadRepetition.nextCompletedCycleCount ===
    1 &&
  persistenceReadRepetition.nextCompletedCycleIdentities[0] ===
    persistenceReadCycle.cycleIdentity &&
  persistenceReadRepetition.canExecuteStorage ===
    false &&
  storageAdapterOperationCalls === 0,
  "Neuer Persistenzzyklus wurde nicht einmalig freigegeben"
);

assert(
  !Object.prototype.hasOwnProperty.call(
    persistenceReadRepetition,
    "cycleState"
  ) &&
  !Object.prototype.hasOwnProperty.call(
    persistenceReadRepetition,
    "privateField"
  ),
  "Interne Wiederholungsfelder wurden übernommen"
);

const duplicateReadRepetition =
  adapter.guardParticipantFullExamResultHistorySnapshotPersistenceCycleRepetition({
    cycleState:
      persistenceReadCycle,
    completedCycleIdentities:
      persistenceReadRepetition.nextCompletedCycleIdentities
  });

assert(
  duplicateReadRepetition.status ===
    "exam_result_history_persistence_cycle_repetition_blocked" &&
  duplicateReadRepetition.isValid === true &&
  duplicateReadRepetition.canAcceptCycleOnce ===
    false &&
  duplicateReadRepetition.canRegisterCycleIdentityLater ===
    false &&
  duplicateReadRepetition.isDuplicateCycle ===
    true &&
  duplicateReadRepetition.reason ===
    "persistence_cycle_repetition_already_completed" &&
  duplicateReadRepetition.nextCompletedCycleCount ===
    1 &&
  storageAdapterOperationCalls === 0,
  "Doppelter Persistenzzyklus wurde nicht blockiert"
);

const persistenceWriteRepetition =
  adapter.guardParticipantFullExamResultHistorySnapshotPersistenceCycleRepetition({
    cycleState:
      persistenceWriteCycle,
    completedCycleIdentities:
      persistenceReadRepetition.nextCompletedCycleIdentities
  });

assert(
  persistenceWriteRepetition.canAcceptCycleOnce ===
    true &&
  persistenceWriteRepetition.isDuplicateCycle ===
    false &&
  persistenceWriteRepetition.completedCycleCount ===
    1 &&
  persistenceWriteRepetition.nextCompletedCycleCount ===
    2 &&
  persistenceWriteRepetition.nextCompletedCycleIdentities[1] ===
    persistenceWriteCycle.cycleIdentity,
  "Zweiter unterschiedlicher Persistenzzyklus wurde nicht registriert"
);

const duplicateRegistryRepetition =
  adapter.guardParticipantFullExamResultHistorySnapshotPersistenceCycleRepetition({
    cycleState:
      persistenceReadCycle,
    completedCycleIdentities: [
      persistenceReadCycle.cycleIdentity,
      persistenceReadCycle.cycleIdentity
    ]
  });

expectEqual(
  duplicateRegistryRepetition.reason,
  "persistence_cycle_repetition_registry_duplicate",
  "Doppelte Identität im Zyklusregister"
);

const invalidRegistryRepetition =
  adapter.guardParticipantFullExamResultHistorySnapshotPersistenceCycleRepetition({
    cycleState:
      persistenceReadCycle,
    completedCycleIdentities: [
      "ungueltige-identitaet"
    ]
  });

expectEqual(
  invalidRegistryRepetition.reason,
  "persistence_cycle_repetition_registry_identity_invalid",
  "Ungültige Zyklusregister-Identität"
);

const tamperedRepetitionCycle = {
  ...persistenceReadCycle,
  terminalOutcome:
    "read_empty"
};

const tamperedCycleRepetition =
  adapter.guardParticipantFullExamResultHistorySnapshotPersistenceCycleRepetition({
    cycleState:
      tamperedRepetitionCycle,
    completedCycleIdentities: []
  });

expectEqual(
  tamperedCycleRepetition.reason,
  "persistence_cycle_repetition_outcome_invalid",
  "Manipulierter Zyklus im Wiederholungs-Guard"
);

console.log(
  "Supabase-Ergebnishistorie-Fixtures: OK"
);
console.log(
  "Normalizer-Fixtures: gültig, ungültig, Duplikat und total_count"
);
console.log(
  "Aggregator-Fixtures: Seitenwerte, leerer Zustand und Fehlerfall"
);
console.log(
  "Response-Mapper-Fixtures: Erfolg, leer, ungültig und RPC-Fehler"
);
console.log(
  "Ladezustands-Fixtures: vorbereitet, lädt, Erfolg, leer und Fehler"
);
console.log(
  "Pagination-Fixtures: unbekannt, erste, mittlere, letzte, leer und begrenzt"
);
console.log(
  "Orchestrator-Fixtures: vorbereitet, lädt, Erfolg, leer und Fehler"
);
console.log(
  "Navigations-Fixtures: erste, vorherige, nächste, blockiert und Retry"
);
console.log(
  "Identitäts-Fixtures: aktiv, aktuell, veraltet und ungültig"
);
console.log(
  "Annahme-Guard-Fixtures: aktuell, leer, veraltet, ungültig und Fehler"
);
console.log(
  "Lebenszyklus-Fixtures: vorbereitet, ausstehend, abgeschlossen und verworfen"
);
console.log(
  "Übergangs-Fixtures: zulässig, blockiert, terminal und manipuliert"
);
console.log(
  "Controller-Fixtures: initialisiert, gestartet, angenommen, navigiert und verworfen"
);
console.log(
  "Snapshot-Fixtures: vorbereitet, ausstehend, abgeschlossen, navigiert und verworfen"
);
console.log(
  "Wiederaufnahme-Fixtures: vorbereitet, ausstehend, navigiert und terminal"
);
console.log(
  "Erstellungs-Fixtures: vorbereitet, ausstehend, navigiert, terminal und manipuliert"
);
console.log(
  "Serialisierungs-Fixtures: kanonisch, begrenzt, wiederaufnehmbar und blockiert"
);
console.log(
  "Deserialisierungs-Fixtures: gültig, kanonisch, begrenzt, fehlerhaft und manipuliert"
);
console.log(
  "Persistenz-Fixtures: Save, Load, Delete, blockiert und ungültig"
);
console.log(
  "Storage-Readiness-Fixtures: vollständig, teilweise, nicht verfügbar und ungültig"
);
console.log(
  "Operationsplan-Fixtures: Write, Read, Delete, blockiert und ungültig"
);
console.log(
  "Freigabe-Fixtures: Write, Read, Delete, veränderte Readiness und manipuliert"
);
console.log(
  "Ausführungs-Guard-Fixtures: Write, Read, Delete, verändert, Accessor und manipuliert"
);
console.log(
  "Aufrufvertrag-Fixtures: Write, Read, Delete, kanonisch und manipuliert"
);
console.log(
  "Aufrufpaket-Fixtures: Write, Read, Delete, veränderter Adapter und manipuliert"
);
console.log(
  "Ergebnisvertrag-Fixtures: Read, leer, Write, Delete, nicht vorhanden und manipuliert"
);
console.log(
  "Ergebnisannahme-Fixtures: Read, leer, Write, Delete, veraltet und manipuliert"
);
console.log(
  "Abschluss-Fixtures: Read, leer, Write, Delete, idempotent, veraltet und manipuliert"
);
console.log(
  "Zyklus-Fixtures: Read, leer, Write, Delete, idempotent, veraltet und manipuliert"
);
console.log(
  "Zyklus-Wiederholungs-Fixtures: neu, doppelt, Register und manipuliert"
);
console.log(
  "Rohe RPC-Fehlerdetails: ausgeschlossen"
);
console.log(
  "Live-RPC- oder Netzwerkaufrufe: keine"
);
