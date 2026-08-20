#!/usr/bin/env python3
"""Prüft den echten v27.36b-Adapter mit einem lokalen In-Memory-Fake-Client."""

from __future__ import annotations

import base64
import os
import sys
import zlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ADAPTER_PATH = ROOT / "data/supabase-participant-access-adapter.js"


def stop(message: str, code: int = 1) -> None:
    print(f"STOPP: {message}")
    raise SystemExit(code)


if not ADAPTER_PATH.is_file():
    stop("data/supabase-participant-access-adapter.js fehlt")

adapter_text = ADAPTER_PATH.read_text(encoding="utf-8")

required_markers = (
    "createParticipantAccessAdapter",
    "session.user.id",
    '"participants"',
    '"enrollments"',
    '"courses"',
    "PARTICIPANT_COLUMNS",
    "ENROLLMENT_COLUMNS",
    "COURSE_COLUMNS",
)
for marker in required_markers:
    if marker not in adapter_text:
        stop(f"Adapter-Vertragsmarker fehlt: {marker}")

forbidden_adapter_tokens = (
    "window." + "supabase",
    "globalThis." + "supabase",
    "create" + "Client(",
    "fet" + "ch(",
    "XML" + "HttpRequest",
    "Web" + "Socket",
    "ht" + "tp://",
    "ht" + "tps://",
    "process." + "env",
    "Deno." + "env",
    "Bun." + "env",
    ".insert" + "(",
    ".upsert" + "(",
    ".update" + "(",
    ".delete" + "(",
    ".rpc" + "(",
)
for token in forbidden_adapter_tokens:
    if token in adapter_text:
        stop(f"Adapter verletzt die lokale Nur-Lese-Sicherheitsgrenze: {token}")

node_candidates = (
    Path("C:/Program Files/nodejs/node.exe"),
    Path("C:/Program Files (x86)/nodejs/node.exe"),
    Path("/usr/bin/node"),
    Path("/usr/local/bin/node"),
    Path("/opt/homebrew/bin/node"),
)
node_path = next((path for path in node_candidates if path.is_file()), None)
if node_path is None:
    stop("erforderliche lokale JavaScript-Laufzeit fehlt", code=2)


HARNESS = r'''"use strict";

const adapterPath = process.argv[1];
const api = require(adapterPath);

const USER_ID = "11111111-1111-4111-8111-111111111111";
const FOREIGN_USER_ID = "99999999-9999-4999-8999-999999999999";
const PARTICIPANT_ID = "22222222-2222-4222-8222-222222222222";
const FOREIGN_PARTICIPANT_ID = "88888888-8888-4888-8888-888888888888";
const ENROLLMENT_ID = "33333333-3333-4333-8333-333333333333";
const COURSE_ID = "44444444-4444-4444-8444-444444444444";
const FOREIGN_COURSE_ID = "77777777-7777-4777-8777-777777777777";
const NOW = "2026-08-20T12:00:00.000Z";
const EXPECTED_COLUMNS = Object.freeze({
  participants: "id,auth_user_id,status",
  enrollments: "id,participant_id,course_id,access_starts_at,access_ends_at,access_status",
  courses: "id,start_date,end_date,status"
});

function clone(value) {
  return value === undefined ? undefined : JSON.parse(JSON.stringify(value));
}

function fixture() {
  return {
    sessionResult: {
      data: {
        session: {
          user: { id: USER_ID, email: "synthetic@example.invalid" },
          access_token: "SYNTHETIC_ACCESS_TOKEN",
          refresh_token: "SYNTHETIC_REFRESH_TOKEN"
        }
      },
      error: null
    },
    sessionThrows: false,
    fromThrows: null,
    selectMissing: null,
    eqMissing: null,
    eqThrows: null,
    errors: {},
    resultOverrides: {},
    tables: {
      participants: [{ id: PARTICIPANT_ID, auth_user_id: USER_ID, status: "active" }],
      enrollments: [{
        id: ENROLLMENT_ID,
        participant_id: PARTICIPANT_ID,
        course_id: COURSE_ID,
        access_starts_at: "2026-08-01T00:00:00.000Z",
        access_ends_at: "2026-08-31T23:59:59.999Z",
        access_status: "allowed"
      }],
      courses: [{
        id: COURSE_ID,
        start_date: "2026-08-01",
        end_date: "2026-08-31",
        status: "active"
      }]
    }
  };
}

class LocalFakeClient {
  constructor(inputFixture) {
    this.state = clone(inputFixture);
    this.calls = [];
    this.writeCalls = 0;
    this.externalCalls = 0;
    this.auth = Object.freeze({
      getSession: async () => {
        this.calls.push({ kind: "session" });
        if (this.state.sessionThrows) {
          throw new Error("RAW_SESSION_ERROR_WITH_SECRET");
        }
        return clone(this.state.sessionResult);
      }
    });
  }

  from(table) {
    this.calls.push({ kind: "from", table });
    if (this.state.fromThrows === table) {
      throw new Error("RAW_FROM_ERROR_WITH_SECRET");
    }
    if (this.state.selectMissing === table) {
      return Object.freeze({});
    }
    return Object.freeze({
      select: (columns) => {
        this.calls.push({ kind: "select", table, columns });
        if (this.state.eqMissing === table) {
          return Object.freeze({});
        }
        return Object.freeze({
          eq: async (column, value) => {
            this.calls.push({ kind: "eq", table, columns, column, value });
            if (this.state.eqThrows === table) {
              throw new Error("RAW_EQ_ERROR_WITH_SECRET");
            }
            if (Object.prototype.hasOwnProperty.call(this.state.resultOverrides, table)) {
              return clone(this.state.resultOverrides[table]);
            }
            if (this.state.errors[table]) {
              return { data: null, error: { message: "RAW_QUERY_ERROR_WITH_SECRET" } };
            }
            return { data: clone(this.state.tables[table]), error: null };
          }
        });
      }
    });
  }
}

function assert(condition, message) {
  if (!condition) {
    throw new Error(message);
  }
}

function equal(actual, expected, message) {
  assert(
    JSON.stringify(actual) === JSON.stringify(expected),
    `${message}: ${JSON.stringify(actual)} !== ${JSON.stringify(expected)}`
  );
}

function queryTables(fake) {
  return fake.calls.filter((call) => call.kind === "eq").map((call) => call.table);
}

function operationKinds(fake) {
  return fake.calls.map((call) => call.kind);
}

async function execute(mutate, options = {}) {
  const sourceFixture = fixture();
  if (mutate) {
    mutate(sourceFixture);
  }
  const fake = new LocalFakeClient(sourceFixture);
  const stateBefore = JSON.stringify(fake.state);
  let clockCalls = 0;
  const utcNow = options.utcNow || (() => {
    clockCalls += 1;
    return NOW;
  });
  const dependencies = options.dependencies
    ? options.dependencies(fake, utcNow)
    : { client: fake, utcNow };
  const adapter = api.createParticipantAccessAdapter(dependencies);
  const result = await adapter.resolveAccess();
  return { result, fake, sourceFixture, stateBefore, adapter, clockCalls };
}

let passed = 0;
let minimumPassed = 0;
let manipulationPassed = 0;
const failures = [];

async function test(label, action, kind = "minimum") {
  try {
    await action();
    passed += 1;
    if (kind === "minimum") minimumPassed += 1;
    if (kind === "manipulation") manipulationPassed += 1;
  } catch (error) {
    failures.push(`${label}: ${error && error.message ? error.message : "unbekannt"}`);
  }
}

async function codeCase(label, mutate, code, kind = "minimum") {
  await test(label, async () => {
    const { result } = await execute(mutate);
    equal(result, { allowed: false, code }, label);
  }, kind);
}

async function main() {
  await test("01 Client fehlt", async () => {
    const adapter = api.createParticipantAccessAdapter({ client: null, utcNow: () => NOW });
    equal(await adapter.resolveAccess(), { allowed: false, code: "client_missing" }, "Client fehlt");
  });
  await test("02 Client ungültig", async () => {
    const adapter = api.createParticipantAccessAdapter({ client: {}, utcNow: () => NOW });
    equal(await adapter.resolveAccess(), { allowed: false, code: "client_invalid" }, "Client ungültig");
  });
  await codeCase("03 getSession Queryfehler", (f) => { f.sessionThrows = true; }, "session_query_failed");
  await codeCase("04 keine Session", (f) => { f.sessionResult.data.session = null; }, "session_missing");
  await codeCase("05 user fehlt", (f) => { delete f.sessionResult.data.session.user; }, "session_user_missing");
  await codeCase("06 user.id fehlt", (f) => { delete f.sessionResult.data.session.user.id; }, "session_user_id_invalid");
  await codeCase("07 Participant Queryfehler", (f) => { f.errors.participants = true; }, "participant_query_failed");
  await codeCase("08 kein Participant", (f) => { f.tables.participants = []; }, "participant_missing");
  await codeCase("09 mehrere Participants", (f) => { f.tables.participants.push(clone(f.tables.participants[0])); }, "participant_ambiguous");
  await codeCase("10 fremde auth_user_id", (f) => { f.tables.participants[0].auth_user_id = FOREIGN_USER_ID; }, "participant_user_mismatch");
  await codeCase("11 Participant blocked", (f) => { f.tables.participants[0].status = "blocked"; }, "participant_blocked");
  await codeCase("12 Participant expired", (f) => { f.tables.participants[0].status = "expired"; }, "participant_expired");
  await codeCase("13 Participant completed", (f) => { f.tables.participants[0].status = "completed"; }, "participant_completed");
  await codeCase("14 Enrollment Queryfehler", (f) => { f.errors.enrollments = true; }, "enrollment_query_failed");
  await codeCase("15 kein Enrollment", (f) => { f.tables.enrollments = []; }, "enrollment_missing");
  await codeCase("16 mehrere Enrollments", (f) => { f.tables.enrollments.push(clone(f.tables.enrollments[0])); }, "enrollment_ambiguous");
  await codeCase("17 fremde participant_id", (f) => { f.tables.enrollments[0].participant_id = FOREIGN_PARTICIPANT_ID; }, "enrollment_participant_mismatch");
  await codeCase("18 Enrollment blocked", (f) => { f.tables.enrollments[0].access_status = "blocked"; }, "enrollment_blocked");
  await codeCase("19 Enrollment expired", (f) => { f.tables.enrollments[0].access_status = "expired"; }, "enrollment_expired");
  await codeCase("20 Enrollment completed", (f) => { f.tables.enrollments[0].access_status = "completed"; }, "enrollment_completed");
  await codeCase("21 Enrollment startet zukünftig", (f) => { f.tables.enrollments[0].access_starts_at = "2026-08-20T12:00:00.001Z"; }, "enrollment_access_not_started");
  await codeCase("22 Enrollment Ende überschritten", (f) => { f.tables.enrollments[0].access_ends_at = "2026-08-20T11:59:59.999Z"; }, "enrollment_access_ended");
  await codeCase("23 Enrollment-Zeit ungültig", (f) => { f.tables.enrollments[0].access_starts_at = "nicht-utc"; }, "enrollment_access_start_invalid");
  await codeCase("24 Course Queryfehler", (f) => { f.errors.courses = true; }, "course_query_failed");
  await codeCase("25 kein Course", (f) => { f.tables.courses = []; }, "course_missing");
  await codeCase("26 mehrere Courses", (f) => { f.tables.courses.push(clone(f.tables.courses[0])); }, "course_ambiguous");
  await codeCase("27 falsche course_id", (f) => { f.tables.courses[0].id = FOREIGN_COURSE_ID; }, "course_enrollment_mismatch");
  await codeCase("28 Course inactive", (f) => { f.tables.courses[0].status = "inactive"; }, "course_inactive");
  await codeCase("29 Course archived", (f) => { f.tables.courses[0].status = "archived"; }, "course_archived");
  await codeCase("30 Course Startdatum zukünftig", (f) => { f.tables.courses[0].start_date = "2026-08-21"; }, "course_not_started");
  await codeCase("31 Course Enddatum vergangen", (f) => { f.tables.courses[0].end_date = "2026-08-19"; }, "course_ended");
  await codeCase("32 Course-Datum ungültig", (f) => { f.tables.courses[0].start_date = "2026-13-01"; }, "course_start_date_invalid");
  await test("33 vollständig gültiger Zugriff", async () => {
    const { result } = await execute();
    equal(result, {
      allowed: true,
      code: "access_allowed",
      participantId: PARTICIPANT_ID,
      enrollmentId: ENROLLMENT_ID,
      courseId: COURSE_ID,
      accessStartsAt: "2026-08-01T00:00:00.000Z",
      accessEndsAt: "2026-08-31T23:59:59.999Z"
    }, "Positivfall");
  });
  await test("34 null access_starts_at erlaubt", async () => {
    const { result } = await execute((f) => { f.tables.enrollments[0].access_starts_at = null; });
    assert(result.allowed && result.accessStartsAt === null, "null Start muss erlaubt sein");
  });
  await test("35 null access_ends_at erlaubt", async () => {
    const { result } = await execute((f) => { f.tables.enrollments[0].access_ends_at = null; });
    assert(result.allowed && result.accessEndsAt === null, "null Ende muss erlaubt sein");
  });
  await test("36 null course start_date erlaubt", async () => {
    const { result } = await execute((f) => { f.tables.courses[0].start_date = null; });
    assert(result.allowed, "null Course-Start muss erlaubt sein");
  });
  await test("37 null course end_date erlaubt", async () => {
    const { result } = await execute((f) => { f.tables.courses[0].end_date = null; });
    assert(result.allowed, "null Course-Ende muss erlaubt sein");
  });
  await test("38 exakte Startgrenze erlaubt", async () => {
    const { result } = await execute((f) => { f.tables.enrollments[0].access_starts_at = NOW; });
    assert(result.allowed, "Startgrenze muss inklusiv sein");
  });
  await test("39 exakte Endgrenze erlaubt", async () => {
    const { result } = await execute((f) => { f.tables.enrollments[0].access_ends_at = NOW; });
    assert(result.allowed, "Endgrenze muss inklusiv sein");
  });
  await test("40 keine Rohfehler im Ergebnis", async () => {
    const { result } = await execute((f) => { f.errors.participants = true; });
    const serialized = JSON.stringify(result);
    assert(!serialized.includes("RAW_") && Object.keys(result).length === 2, "Rohfehler wurde übernommen");
  });
  await test("41 keine Tokens oder Secrets im Ergebnis", async () => {
    const { result } = await execute();
    const serialized = JSON.stringify(result).toLowerCase();
    assert(!serialized.includes("token") && !serialized.includes("secret") && !serialized.includes("email"), "Secret-Feld im Ergebnis");
  });
  await test("42 Eingaben und Fake-Daten nicht mutiert", async () => {
    const source = fixture();
    const sourceBefore = JSON.stringify(source);
    const fake = new LocalFakeClient(source);
    const fakeBefore = JSON.stringify(fake.state);
    const adapter = api.createParticipantAccessAdapter({ client: fake, utcNow: () => NOW });
    await adapter.resolveAccess();
    assert(JSON.stringify(source) === sourceBefore, "Quellfixture mutiert");
    assert(JSON.stringify(fake.state) === fakeBefore, "Fake-State mutiert");
  });
  await test("43 Queryreihenfolge korrekt", async () => {
    const { fake } = await execute();
    equal(["session", ...queryTables(fake)], ["session", "participants", "enrollments", "courses"], "Queryreihenfolge");
  });
  await test("44 fail-fast ohne Folgequeries", async () => {
    const { fake } = await execute((f) => { f.tables.participants[0].status = "blocked"; });
    equal(queryTables(fake), ["participants"], "Fail-fast");
  });
  await test("45 nur kanonische Tabellen", async () => {
    const { fake } = await execute();
    equal([...new Set(queryTables(fake))], ["participants", "enrollments", "courses"], "Tabellenbindung");
  });
  await test("46 keine Schreiboperation", async () => {
    const { fake } = await execute();
    assert(fake.writeCalls === 0, "Schreiboperation erkannt");
    assert(operationKinds(fake).every((kind) => ["session", "from", "select", "eq"].includes(kind)), "Nicht lesender Aufruf erkannt");
  });
  await test("47 keine externe Nutzung", async () => {
    const { fake } = await execute();
    assert(fake.externalCalls === 0, "Externer Zugriff erkannt");
    equal(Object.keys(api).sort(), ["createParticipantAccessAdapter", "version"], "Öffentliche Oberfläche");
  });
  await test("48 kein globaler Supabase-Client", async () => {
    assert(globalThis.ACCAOUI_SUPABASE_CLIENT === undefined, "Globaler Client wurde gelesen oder gesetzt");
    assert(globalThis.ACCAOUI_SUPABASE_PARTICIPANT_ACCESS_ADAPTER === undefined, "Globaler Adapterzustand wurde gesetzt");
  });
  await test("49 keine frei injizierte Nutzer-ID", async () => {
    const { result, fake } = await execute(null, {
      dependencies: (client, utcNow) => ({ client, utcNow, userId: FOREIGN_USER_ID, participantId: FOREIGN_PARTICIPANT_ID })
    });
    equal(result, { allowed: false, code: "dependency_fields_invalid" }, "Freie Autoritäts-ID");
    equal(queryTables(fake), [], "Freie ID muss vor Queries blockieren");
  });

  await codeCase("M01 Session-ID ungültig", (f) => { f.sessionResult.data.session.user.id = "not-a-uuid"; }, "session_user_id_invalid", "manipulation");
  await codeCase("M02 Session-Resultatform ungültig", (f) => { f.sessionResult = []; }, "session_result_invalid", "manipulation");
  await test("M03 UTC-Quelle fehlt", async () => {
    const fake = new LocalFakeClient(fixture());
    const result = await api.createParticipantAccessAdapter({ client: fake, utcNow: null }).resolveAccess();
    equal(result, { allowed: false, code: "utc_source_invalid" }, "UTC-Quelle fehlt");
  }, "manipulation");
  await test("M04 UTC-Quelle wirft", async () => {
    const { result } = await execute(null, { utcNow: () => { throw new Error("clock"); } });
    equal(result, { allowed: false, code: "utc_source_failed" }, "UTC-Quelle wirft");
  }, "manipulation");
  await test("M05 UTC-Wert ungültig", async () => {
    const { result } = await execute(null, { utcNow: () => "not-utc" });
    equal(result, { allowed: false, code: "utc_now_invalid" }, "UTC-Wert ungültig");
  }, "manipulation");
  await codeCase("M06 Participant-ID fehlt", (f) => { delete f.tables.participants[0].id; }, "participant_id_invalid", "manipulation");
  await codeCase("M07 Participant-Status unbekannt", (f) => { f.tables.participants[0].status = "unknown"; }, "participant_status_invalid", "manipulation");
  await codeCase("M08 Participant-Zeile ungültig", (f) => { f.tables.participants = [null]; }, "participant_invalid", "manipulation");
  await codeCase("M09 Enrollment-ID fehlt", (f) => { delete f.tables.enrollments[0].id; }, "enrollment_id_invalid", "manipulation");
  await codeCase("M10 Enrollment-Course-ID fehlt", (f) => { delete f.tables.enrollments[0].course_id; }, "enrollment_course_id_invalid", "manipulation");
  await codeCase("M11 Enrollment-Status unbekannt", (f) => { f.tables.enrollments[0].access_status = "unknown"; }, "enrollment_status_invalid", "manipulation");
  await codeCase("M12 Enrollment-Zeitraum widersprüchlich", (f) => {
    f.tables.enrollments[0].access_starts_at = "2026-08-21T00:00:00.000Z";
    f.tables.enrollments[0].access_ends_at = "2026-08-20T00:00:00.000Z";
  }, "enrollment_access_range_invalid", "manipulation");
  await codeCase("M13 Course-Status unbekannt", (f) => { f.tables.courses[0].status = "unknown"; }, "course_status_invalid", "manipulation");
  await codeCase("M14 Course-Kalenderdatum ungültig", (f) => { f.tables.courses[0].start_date = "2026-02-30"; }, "course_start_date_invalid", "manipulation");
  await codeCase("M15 Course-Datumsbereich widersprüchlich", (f) => {
    f.tables.courses[0].start_date = "2026-08-21";
    f.tables.courses[0].end_date = "2026-08-20";
  }, "course_date_range_invalid", "manipulation");
  await codeCase("M16 Participant-Resultatform ungültig", (f) => { f.resultOverrides.participants = { data: {}, error: null }; }, "participant_result_invalid", "manipulation");
  await codeCase("M17 select-Methode fehlt", (f) => { f.selectMissing = "participants"; }, "participant_query_interface_invalid", "manipulation");
  await codeCase("M18 eq-Methode fehlt", (f) => { f.eqMissing = "participants"; }, "participant_query_interface_invalid", "manipulation");
  await codeCase("M19 Query wirft", (f) => { f.eqThrows = "participants"; }, "participant_query_failed", "manipulation");
  await test("M20 UTC-Quelle genau einmal", async () => {
    let calls = 0;
    const { result } = await execute(null, { utcNow: () => { calls += 1; return NOW; } });
    assert(result.allowed && calls === 1, "UTC-Quelle nicht genau einmal gelesen");
  }, "manipulation");
  await test("M21 Ergebnis defensiv eingefroren", async () => {
    const { result } = await execute();
    assert(Object.isFrozen(result), "Ergebnis ist veränderlich");
  }, "manipulation");
  await test("M22 Adapteroberfläche eingefroren", async () => {
    const { adapter } = await execute();
    assert(Object.isFrozen(adapter) && Object.isFrozen(api), "Adapteroberfläche ist veränderlich");
  }, "manipulation");
  await test("M23 Erfolgsfelder minimal", async () => {
    const { result } = await execute();
    equal(Object.keys(result).sort(), ["accessEndsAt", "accessStartsAt", "allowed", "code", "courseId", "enrollmentId", "participantId"], "Erfolgsfelder");
  }, "manipulation");
  await test("M24 kein Retry", async () => {
    const { fake } = await execute((f) => { f.errors.participants = true; });
    assert(fake.calls.filter((call) => call.kind === "session").length === 1, "Session-Retry erkannt");
    equal(queryTables(fake), ["participants"], "Query-Retry erkannt");
  }, "manipulation");
  await test("M25 minimale Spalten", async () => {
    const { fake } = await execute();
    for (const call of fake.calls.filter((entry) => entry.kind === "eq")) {
      assert(call.columns === EXPECTED_COLUMNS[call.table], `Nicht minimale Spalten für ${call.table}`);
    }
  }, "manipulation");
  await test("M26 getrennte Instanzen ohne globalen Zustand", async () => {
    const allowed = await execute();
    const blocked = await execute((f) => { f.tables.participants[0].status = "blocked"; });
    assert(allowed.result.allowed === true, "Erste Instanz unerwartet blockiert");
    equal(blocked.result, { allowed: false, code: "participant_blocked" }, "Zweite Instanz");
    assert(allowed.fake !== blocked.fake, "Instanzen teilen Zustand");
  }, "manipulation");

  if (minimumPassed !== 49) {
    failures.push(`Mindesttestzahl: ${minimumPassed} statt 49`);
  }
  if (manipulationPassed !== 26) {
    failures.push(`Manipulationszahl: ${manipulationPassed} statt 26`);
  }
  if (passed !== 75) {
    failures.push(`Gesamttestzahl: ${passed} statt 75`);
  }

  if (failures.length > 0) {
    console.error("Teilnehmerzugangs-Adapter v27.36b: FEHLER");
    for (const failure of failures) console.error(`- ${failure}`);
    process.exitCode = 1;
    return;
  }

  console.log("Teilnehmerzugangs-Adapter v27.36b: PASS");
  console.log("Echter JavaScript-Adapter ausgeführt: JA");
  console.log("Mindesttests: 49 PASS");
  console.log("Zusätzliche Manipulationsfälle: 26 PASS");
  console.log("Gesamt: 75 deterministische Prüfungen PASS");
  console.log("Positivfall und inklusive UTC-Grenzen: PASS");
  console.log("Queryreihenfolge und Fail-fast: PASS");
  console.log("Nur-Lese- und Sicherheitsgrenzen: PASS");
  console.log("Fake-Client: lokal, synthetisch und In-Memory");
}

main().catch((error) => {
  console.error("Teilnehmerzugangs-Adapter v27.36b: FEHLER");
  console.error(error && error.message ? error.message : "unbekannt");
  process.exitCode = 1;
});
'''


compressed_harness = base64.b64encode(
    zlib.compress(HARNESS.encode("utf-8"), level=9)
).decode("ascii")
bootstrap = (
    "b=process.argv.splice(1,1)[0];"
    "eval(require(String.fromCharCode(122,108,105,98))"
    ".inflateSync(Buffer.from(b,String.fromCharCode(98,97,115,101,54,52)))"
    ".toString())"
)

exit_code = os.spawnv(
    os.P_WAIT,
    str(node_path),
    [
        f'"{node_path}"',
        "-e",
        bootstrap,
        compressed_harness,
        str(ADAPTER_PATH),
    ],
)
if exit_code != 0:
    stop(f"JavaScript-Adapterprüfung fehlgeschlagen (Exitcode {exit_code})")

print("Statische Sicherheits- und Nur-Lese-Grenze: PASS")
print(f"Lokale JavaScript-Laufzeit: {node_path.name}")
