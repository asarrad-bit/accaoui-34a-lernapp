"use strict";

// Accaoui §34a Lern-App
// Lokale Prüfungshistorie-Fixtures
// Stand: v27.29g

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
  "v27.29e",
  "Adapterversion"
);

for (const functionName of [
  "normalizeParticipantFullExamResultRow",
  "normalizeParticipantFullExamResultRows",
  "aggregateParticipantFullExamResultRows"
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
  "Live-RPC- oder Netzwerkaufrufe: keine"
);
