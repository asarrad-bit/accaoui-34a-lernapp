// Accaoui §34a Lern-App – isolierte Teilnehmer-Auth-/Session-Bootstrap-Brücke
// Stand: v27.37b

(function exposeParticipantAuthSessionBootstrapBridge(
  browserRoot,
  commonJsModule
) {
"use strict";

function isRecord(value) {
  return value !== null && typeof value === "object" && !Array.isArray(value);
}

function authError() {
  return Object.freeze({ ok: false, code: "auth_error" });
}

function hasExactKeys(value, expected) {
  const keys = Reflect.ownKeys(value);
  return keys.length === expected.length &&
    expected.every((key) => keys.includes(key));
}

function isValidAdapterResult(value, methodName) {
  if (
    !isRecord(value) ||
    Object.getPrototypeOf(value) !== Object.prototype ||
    !hasExactKeys(value, ["ok", "code"]) ||
    !Object.isFrozen(value)
  ) {
    return false;
  }

  // Feste eigene Datenfelder; eingefrorene Accessor-Felder bleiben dynamisch.
  const okField = Object.getOwnPropertyDescriptor(value, "ok");
  const codeField = Object.getOwnPropertyDescriptor(value, "code");
  if (
    !okField || !codeField ||
    !Object.prototype.hasOwnProperty.call(okField, "value") ||
    !Object.prototype.hasOwnProperty.call(codeField, "value") ||
    !okField.enumerable || !codeField.enumerable
  ) {
    return false;
  }

  const ok = value.ok;
  const code = value.code;
  if (
    typeof ok !== "boolean" || typeof code !== "string" ||
    ok !== okField.value || code !== codeField.value
  ) {
    return false;
  }

  if (methodName === "resolveSession") {
    return (ok === true && code === "session_available") ||
      (ok === false && (
        code === "session_missing" || code === "session_invalid" ||
        code === "auth_error"
      ));
  }
  if (methodName === "signIn") {
    return (ok === true && code === "signed_in") ||
      (ok === false && (
        code === "credentials_invalid" || code === "sign_in_failed" ||
        code === "auth_error"
      ));
  }
  if (methodName === "signOut") {
    return (ok === true && code === "signed_out") ||
      (ok === false && (
        code === "sign_out_failed" || code === "auth_error"
      ));
  }
  return false;
}

function createParticipantAuthSessionBootstrapBridge(dependencies) {
  async function invoke(methodName, args) {
    try {
      if (
        !isRecord(dependencies) ||
        !hasExactKeys(dependencies, [
          "bootstrap", "createParticipantAuthSessionAdapter"
        ])
      ) {
        return authError();
      }

      const bootstrap = dependencies.bootstrap;
      const createParticipantAuthSessionAdapter =
        dependencies.createParticipantAuthSessionAdapter;
      if (
        !isRecord(bootstrap) ||
        typeof createParticipantAuthSessionAdapter !== "function"
      ) {
        return authError();
      }

      const getClient = bootstrap.getClient;
      if (typeof getClient !== "function") {
        return authError();
      }
      const client = getClient.call(bootstrap);
      if (!isRecord(client)) {
        return authError();
      }

      const auth = client.auth;
      if (!isRecord(auth)) {
        return authError();
      }
      const adapter = createParticipantAuthSessionAdapter({ auth });
      if (!isRecord(adapter)) {
        return authError();
      }

      const adapterMethod = adapter[methodName];
      if (typeof adapterMethod !== "function") {
        return authError();
      }
      const adapterResult = await adapterMethod.apply(adapter, args);
      if (!isValidAdapterResult(adapterResult, methodName)) {
        return authError();
      }
      return adapterResult;
    } catch (_error) {
      return authError();
    }
  }

  function resolveSession() {
    return invoke("resolveSession", []);
  }

  function signIn(credentials) {
    return invoke("signIn", [credentials]);
  }

  function signOut() {
    return invoke("signOut", []);
  }

  return Object.freeze({ resolveSession, signIn, signOut });
}

const participantAuthSessionBootstrapBridgeApi = Object.freeze({
  createParticipantAuthSessionBootstrapBridge
});

if (commonJsModule && typeof commonJsModule === "object") {
  commonJsModule.exports = participantAuthSessionBootstrapBridgeApi;
}

if (browserRoot) {
  let existingFactory;

  try {
    existingFactory =
      browserRoot.ACCAOUI_PARTICIPANT_AUTH_SESSION_BOOTSTRAP_BRIDGE_FACTORY;
  } catch (_error) {
    return;
  }

  if (existingFactory === undefined) {
    try {
      Object.defineProperty(
        browserRoot,
        "ACCAOUI_PARTICIPANT_AUTH_SESSION_BOOTSTRAP_BRIDGE_FACTORY",
        {
          value: createParticipantAuthSessionBootstrapBridge,
          enumerable: true,
          configurable: false,
          writable: false
        }
      );
    } catch (_error) {
      // Bestehende oder nicht beschreibbare Grenze niemals überschreiben.
    }
  }
}
})(
  typeof window !== "undefined" ? window : null,
  typeof module !== "undefined" ? module : null
);
