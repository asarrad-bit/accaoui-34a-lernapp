"use strict";

// Accaoui §34a Lern-App
// Lokale Prüfungshistorie-Fixtures
// Stand: v27.29p

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
  "v27.29p",
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
  "Rohe RPC-Fehlerdetails: ausgeschlossen"
);
console.log(
  "Live-RPC- oder Netzwerkaufrufe: keine"
);
