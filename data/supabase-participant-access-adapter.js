// Accaoui §34a Lern-App – lokaler Teilnehmerzugangs-Adapter
// Stand: v27.36b
//
// Isoliertes CommonJS-Modul ohne App-, Config-, Bootstrap- oder Live-Anbindung.
// Ein Supabase-kompatibler Client und eine UTC-Zeitquelle werden ausschließlich
// über createParticipantAccessAdapter({ client, utcNow }) injiziert.

"use strict";

const VERSION = "v27.36b";

const PARTICIPANT_COLUMNS = "id,auth_user_id,status";
const ENROLLMENT_COLUMNS =
  "id,participant_id,course_id,access_starts_at,access_ends_at,access_status";
const COURSE_COLUMNS = "id,start_date,end_date,status";

const PARTICIPANT_STATUSES = new Set([
  "active",
  "blocked",
  "expired",
  "completed"
]);
const ENROLLMENT_STATUSES = new Set([
  "allowed",
  "blocked",
  "expired",
  "completed"
]);
const COURSE_STATUSES = new Set(["active", "inactive", "archived"]);

const UUID_PATTERN =
  /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
const UTC_INSTANT_PATTERN =
  /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,3})?(?:Z|[+-]\d{2}:\d{2})$/;
const UTC_DATE_PATTERN = /^\d{4}-\d{2}-\d{2}$/;

function blocked(code) {
  return Object.freeze({ allowed: false, code });
}

function isRecord(value) {
  return value !== null && typeof value === "object" && !Array.isArray(value);
}

function isUuid(value) {
  return typeof value === "string" && UUID_PATTERN.test(value);
}

function parseUtcInstant(value) {
  if (value instanceof Date) {
    const copiedDate = new Date(value.getTime());
    return Number.isFinite(copiedDate.getTime()) ? copiedDate : null;
  }

  if (typeof value !== "string" || !UTC_INSTANT_PATTERN.test(value)) {
    return null;
  }

  const parsed = new Date(value);
  return Number.isFinite(parsed.getTime()) ? parsed : null;
}

function parseUtcDate(value) {
  if (typeof value !== "string" || !UTC_DATE_PATTERN.test(value)) {
    return null;
  }

  const [year, month, day] = value.split("-").map(Number);
  const parsed = new Date(Date.UTC(year, month - 1, day));
  if (
    parsed.getUTCFullYear() !== year ||
    parsed.getUTCMonth() !== month - 1 ||
    parsed.getUTCDate() !== day
  ) {
    return null;
  }

  return value;
}

function participantStatusCode(status) {
  if (!PARTICIPANT_STATUSES.has(status)) {
    return "participant_status_invalid";
  }
  return status === "active" ? null : `participant_${status}`;
}

function enrollmentStatusCode(status) {
  if (!ENROLLMENT_STATUSES.has(status)) {
    return "enrollment_status_invalid";
  }
  return status === "allowed" ? null : `enrollment_${status}`;
}

function courseStatusCode(status) {
  if (!COURSE_STATUSES.has(status)) {
    return "course_status_invalid";
  }
  return status === "active" ? null : `course_${status}`;
}

function createParticipantAccessAdapter(dependencies) {
  let dependencyCode = null;
  let client = null;
  let utcNow = null;

  if (!isRecord(dependencies)) {
    dependencyCode = "client_missing";
  } else {
    let dependencyKeys;
    try {
      dependencyKeys = Object.keys(dependencies);
      client = dependencies.client;
      utcNow = dependencies.utcNow;
    } catch (_error) {
      dependencyCode = "dependencies_invalid";
    }

    if (
      !dependencyCode &&
      dependencyKeys.some((key) => key !== "client" && key !== "utcNow")
    ) {
      dependencyCode = "dependency_fields_invalid";
    } else if (!dependencyCode && (client === null || client === undefined)) {
      dependencyCode = "client_missing";
    } else if (
      !dependencyCode &&
      (!isRecord(client) ||
        !isRecord(client.auth) ||
        typeof client.auth.getSession !== "function" ||
        typeof client.from !== "function")
    ) {
      dependencyCode = "client_invalid";
    } else if (!dependencyCode && typeof utcNow !== "function") {
      dependencyCode = "utc_source_invalid";
    }
  }

  async function queryRows(table, columns, matchColumn, matchValue, stage) {
    let tableQuery;
    let selectQuery;
    let response;

    try {
      tableQuery = client.from(table);
      if (!isRecord(tableQuery) || typeof tableQuery.select !== "function") {
        return { code: `${stage}_query_interface_invalid` };
      }

      selectQuery = tableQuery.select(columns);
      if (!isRecord(selectQuery) || typeof selectQuery.eq !== "function") {
        return { code: `${stage}_query_interface_invalid` };
      }

      response = await selectQuery.eq(matchColumn, matchValue);
    } catch (_error) {
      return { code: `${stage}_query_failed` };
    }

    if (
      isRecord(response) &&
      response.error !== null &&
      response.error !== undefined
    ) {
      return { code: `${stage}_query_failed` };
    }
    if (!isRecord(response) || !Array.isArray(response.data)) {
      return { code: `${stage}_result_invalid` };
    }

    return { rows: response.data.slice() };
  }

  async function resolveAccess() {
    if (dependencyCode) {
      return blocked(dependencyCode);
    }

    let now;
    try {
      now = parseUtcInstant(utcNow());
    } catch (_error) {
      return blocked("utc_source_failed");
    }
    if (!now) {
      return blocked("utc_now_invalid");
    }

    let sessionResponse;
    try {
      sessionResponse = await client.auth.getSession();
    } catch (_error) {
      return blocked("session_query_failed");
    }

    if (!isRecord(sessionResponse)) {
      return blocked("session_result_invalid");
    }
    if (
      sessionResponse.error !== null &&
      sessionResponse.error !== undefined
    ) {
      return blocked("session_query_failed");
    }
    if (!isRecord(sessionResponse.data)) {
      return blocked("session_result_invalid");
    }

    const session = sessionResponse.data.session;
    if (session === null || session === undefined) {
      return blocked("session_missing");
    }
    if (!isRecord(session)) {
      return blocked("session_invalid");
    }
    if (!isRecord(session.user)) {
      return blocked("session_user_missing");
    }

    // Einzige Nutzerautorität: session.user.id. Es gibt keine frei injizierte ID.
    const userId = session.user.id;
    if (!isUuid(userId)) {
      return blocked("session_user_id_invalid");
    }

    const participantResult = await queryRows(
      "participants",
      PARTICIPANT_COLUMNS,
      "auth_user_id",
      userId,
      "participant"
    );
    if (participantResult.code) {
      return blocked(participantResult.code);
    }
    if (participantResult.rows.length === 0) {
      return blocked("participant_missing");
    }
    if (participantResult.rows.length !== 1) {
      return blocked("participant_ambiguous");
    }

    const participant = participantResult.rows[0];
    if (!isRecord(participant)) {
      return blocked("participant_invalid");
    }
    if (!isUuid(participant.id)) {
      return blocked("participant_id_invalid");
    }
    if (participant.auth_user_id !== userId) {
      return blocked("participant_user_mismatch");
    }
    const participantBlock = participantStatusCode(participant.status);
    if (participantBlock) {
      return blocked(participantBlock);
    }

    const enrollmentResult = await queryRows(
      "enrollments",
      ENROLLMENT_COLUMNS,
      "participant_id",
      participant.id,
      "enrollment"
    );
    if (enrollmentResult.code) {
      return blocked(enrollmentResult.code);
    }
    if (enrollmentResult.rows.length === 0) {
      return blocked("enrollment_missing");
    }
    if (enrollmentResult.rows.length !== 1) {
      return blocked("enrollment_ambiguous");
    }

    const enrollment = enrollmentResult.rows[0];
    if (!isRecord(enrollment)) {
      return blocked("enrollment_invalid");
    }
    if (!isUuid(enrollment.id)) {
      return blocked("enrollment_id_invalid");
    }
    if (!isUuid(enrollment.course_id)) {
      return blocked("enrollment_course_id_invalid");
    }
    if (enrollment.participant_id !== participant.id) {
      return blocked("enrollment_participant_mismatch");
    }
    const enrollmentBlock = enrollmentStatusCode(enrollment.access_status);
    if (enrollmentBlock) {
      return blocked(enrollmentBlock);
    }

    const accessStart =
      enrollment.access_starts_at === null
        ? null
        : parseUtcInstant(enrollment.access_starts_at);
    const accessEnd =
      enrollment.access_ends_at === null
        ? null
        : parseUtcInstant(enrollment.access_ends_at);
    if (enrollment.access_starts_at !== null && !accessStart) {
      return blocked("enrollment_access_start_invalid");
    }
    if (enrollment.access_ends_at !== null && !accessEnd) {
      return blocked("enrollment_access_end_invalid");
    }
    if (accessStart && accessEnd && accessStart.getTime() > accessEnd.getTime()) {
      return blocked("enrollment_access_range_invalid");
    }
    if (accessStart && now.getTime() < accessStart.getTime()) {
      return blocked("enrollment_access_not_started");
    }
    if (accessEnd && now.getTime() > accessEnd.getTime()) {
      return blocked("enrollment_access_ended");
    }

    const courseResult = await queryRows(
      "courses",
      COURSE_COLUMNS,
      "id",
      enrollment.course_id,
      "course"
    );
    if (courseResult.code) {
      return blocked(courseResult.code);
    }
    if (courseResult.rows.length === 0) {
      return blocked("course_missing");
    }
    if (courseResult.rows.length !== 1) {
      return blocked("course_ambiguous");
    }

    const course = courseResult.rows[0];
    if (!isRecord(course)) {
      return blocked("course_invalid");
    }
    if (!isUuid(course.id)) {
      return blocked("course_id_invalid");
    }
    if (course.id !== enrollment.course_id) {
      return blocked("course_enrollment_mismatch");
    }
    const courseBlock = courseStatusCode(course.status);
    if (courseBlock) {
      return blocked(courseBlock);
    }

    const courseStart =
      course.start_date === null ? null : parseUtcDate(course.start_date);
    const courseEnd =
      course.end_date === null ? null : parseUtcDate(course.end_date);
    if (course.start_date !== null && !courseStart) {
      return blocked("course_start_date_invalid");
    }
    if (course.end_date !== null && !courseEnd) {
      return blocked("course_end_date_invalid");
    }
    if (courseStart && courseEnd && courseStart > courseEnd) {
      return blocked("course_date_range_invalid");
    }

    const todayUtc = now.toISOString().slice(0, 10);
    if (courseStart && todayUtc < courseStart) {
      return blocked("course_not_started");
    }
    if (courseEnd && todayUtc > courseEnd) {
      return blocked("course_ended");
    }

    return Object.freeze({
      allowed: true,
      code: "access_allowed",
      participantId: participant.id,
      enrollmentId: enrollment.id,
      courseId: course.id,
      accessStartsAt: accessStart ? accessStart.toISOString() : null,
      accessEndsAt: accessEnd ? accessEnd.toISOString() : null
    });
  }

  return Object.freeze({
    version: VERSION,
    resolveAccess
  });
}

module.exports = Object.freeze({
  version: VERSION,
  createParticipantAccessAdapter
});
