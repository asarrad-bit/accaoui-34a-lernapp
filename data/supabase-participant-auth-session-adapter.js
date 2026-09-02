// Accaoui §34a Lern-App – isolierter Teilnehmer-Auth-/Session-Adapter
// Stand: v27.37a

"use strict";

const UUID_PATTERN =
  /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;

function isRecord(value) {
  return value !== null && typeof value === "object" && !Array.isArray(value);
}

function hasOwn(value, key) {
  return Object.prototype.hasOwnProperty.call(value, key);
}

function result(ok, code) {
  return Object.freeze({ ok, code });
}

function isUsableSession(session) {
  return (
    isRecord(session) &&
    isRecord(session.user) &&
    typeof session.user.id === "string" &&
    UUID_PATTERN.test(session.user.id)
  );
}

function createParticipantAuthSessionAdapter(dependencies) {
  let auth = null;
  let dependencyValid = false;

  try {
    const dependencyKeys = isRecord(dependencies)
      ? Object.keys(dependencies)
      : [];
    if (
      dependencyKeys.length === 1 &&
      dependencyKeys[0] === "auth" &&
      isRecord(dependencies.auth)
    ) {
      auth = dependencies.auth;
      dependencyValid = true;
    }
  } catch (_error) {
    dependencyValid = false;
  }

  async function resolveSession() {
    if (!dependencyValid) {
      return result(false, "auth_error");
    }

    try {
      if (typeof auth.getSession !== "function") {
        return result(false, "auth_error");
      }
      const response = await auth.getSession();
      if (!isRecord(response) || !hasOwn(response, "error")) {
        return result(false, "session_invalid");
      }
      if (response.error !== null && response.error !== undefined) {
        return result(false, "auth_error");
      }
      if (!isRecord(response.data) || !hasOwn(response.data, "session")) {
        return result(false, "session_invalid");
      }
      const session = response.data.session;
      if (session === null || session === undefined) {
        return result(false, "session_missing");
      }
      return isUsableSession(session)
        ? result(true, "session_available")
        : result(false, "session_invalid");
    } catch (_error) {
      return result(false, "auth_error");
    }
  }

  async function signIn(credentials) {
    if (!dependencyValid) {
      return result(false, "auth_error");
    }
    if (
      !isRecord(credentials) ||
      typeof credentials.email !== "string" ||
      credentials.email.trim() === "" ||
      typeof credentials.password !== "string" ||
      credentials.password === ""
    ) {
      return result(false, "credentials_invalid");
    }

    try {
      if (typeof auth.signInWithPassword !== "function") {
        return result(false, "auth_error");
      }
      const response = await auth.signInWithPassword({
        email: credentials.email.trim(),
        password: credentials.password
      });
      if (!isRecord(response) || !hasOwn(response, "error")) {
        return result(false, "sign_in_failed");
      }
      if (response.error !== null && response.error !== undefined) {
        return result(false, "sign_in_failed");
      }
      if (
        !isRecord(response.data) ||
        !hasOwn(response.data, "session") ||
        !isUsableSession(response.data.session)
      ) {
        return result(false, "sign_in_failed");
      }
      return result(true, "signed_in");
    } catch (_error) {
      return result(false, "auth_error");
    }
  }

  async function signOut() {
    if (!dependencyValid) {
      return result(false, "auth_error");
    }

    try {
      if (typeof auth.signOut !== "function") {
        return result(false, "auth_error");
      }
      const response = await auth.signOut();
      if (!isRecord(response) || !hasOwn(response, "error")) {
        return result(false, "sign_out_failed");
      }
      if (response.error !== null && response.error !== undefined) {
        return result(false, "sign_out_failed");
      }
      return result(true, "signed_out");
    } catch (_error) {
      return result(false, "auth_error");
    }
  }

  return Object.freeze({ resolveSession, signIn, signOut });
}

module.exports = Object.freeze({ createParticipantAuthSessionAdapter });
