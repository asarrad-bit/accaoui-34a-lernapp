// Accaoui §34a Lern-App – isolierter Browser-Provider für Teilnehmer-Auth-/Session-Kette
// Stand: v27.37d

(function installParticipantAuthSessionBrowserProvider(browserRoot) {
  "use strict";

  if (!browserRoot) {
    return;
  }

  function authError() {
    return Object.freeze({ ok: false, code: "auth_error" });
  }

  function isRecord(value) {
    return value !== null &&
      typeof value === "object" &&
      !Array.isArray(value);
  }

  function isValidBridgeResult(value, methodName) {
    try {
      if (
        !isRecord(value) ||
        Object.getPrototypeOf(value) !== Object.prototype ||
        !Object.isFrozen(value)
      ) {
        return false;
      }

      const keys = Reflect.ownKeys(value);
      if (
        keys.length !== 2 ||
        !keys.includes("ok") ||
        !keys.includes("code")
      ) {
        return false;
      }

      const okField =
        Object.getOwnPropertyDescriptor(value, "ok");
      const codeField =
        Object.getOwnPropertyDescriptor(value, "code");

      if (
        !okField ||
        !codeField ||
        !Object.prototype.hasOwnProperty.call(okField, "value") ||
        !Object.prototype.hasOwnProperty.call(codeField, "value") ||
        !okField.enumerable ||
        !codeField.enumerable
      ) {
        return false;
      }

      const ok = value.ok;
      const code = value.code;

      if (
        typeof ok !== "boolean" ||
        typeof code !== "string" ||
        ok !== okField.value ||
        code !== codeField.value
      ) {
        return false;
      }

      if (methodName === "resolveSession") {
        return (
          (ok === true && code === "session_available") ||
          (
            ok === false &&
            (
              code === "session_missing" ||
              code === "session_invalid" ||
              code === "auth_error"
            )
          )
        );
      }

      if (methodName === "signIn") {
        return (
          (ok === true && code === "signed_in") ||
          (
            ok === false &&
            (
              code === "credentials_invalid" ||
              code === "sign_in_failed" ||
              code === "auth_error"
            )
          )
        );
      }

      if (methodName === "signOut") {
        return (
          (ok === true && code === "signed_out") ||
          (
            ok === false &&
            (
              code === "sign_out_failed" ||
              code === "auth_error"
            )
          )
        );
      }

      return false;
    } catch (_error) {
      return false;
    }
  }

  async function invoke(methodName, args) {
    let bootstrap;
    let adapterFactory;
    let bridgeFactory;

    try {
      bootstrap = browserRoot.ACCAOUI_SUPABASE_BOOTSTRAP;
      adapterFactory =
        browserRoot.ACCAOUI_PARTICIPANT_AUTH_SESSION_ADAPTER_FACTORY;
      bridgeFactory =
        browserRoot
          .ACCAOUI_PARTICIPANT_AUTH_SESSION_BOOTSTRAP_BRIDGE_FACTORY;
    } catch (_error) {
      return authError();
    }

    if (
      !isRecord(bootstrap) ||
      typeof adapterFactory !== "function" ||
      typeof bridgeFactory !== "function"
    ) {
      return authError();
    }

    const dependencies = Object.freeze({
      bootstrap,
      createParticipantAuthSessionAdapter: adapterFactory
    });

    let bridge;

    try {
      bridge = bridgeFactory(dependencies);
    } catch (_error) {
      return authError();
    }

    if (!isRecord(bridge)) {
      return authError();
    }

    let method;

    try {
      method = bridge[methodName];
    } catch (_error) {
      return authError();
    }

    if (typeof method !== "function") {
      return authError();
    }

    let result;

    try {
      result = await method.apply(bridge, args);
    } catch (_error) {
      return authError();
    }

    if (!isValidBridgeResult(result, methodName)) {
      return authError();
    }

    return result;
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

  const provider = Object.freeze({
    resolveSession,
    signIn,
    signOut
  });

  let providerBoundaryOccupied;

  try {
    providerBoundaryOccupied =
      "ACCAOUI_PARTICIPANT_AUTH_SESSION_APP_PROVIDER" in browserRoot;
  } catch (_error) {
    return;
  }

  if (providerBoundaryOccupied) {
    return;
  }

  try {
    Object.defineProperty(
      browserRoot,
      "ACCAOUI_PARTICIPANT_AUTH_SESSION_APP_PROVIDER",
      {
        value: provider,
        enumerable: true,
        configurable: false,
        writable: false
      }
    );
  } catch (_error) {
    // Bestehende oder nicht beschreibbare Browser-Grenzen bleiben unverändert.
  }
})(typeof window !== "undefined" ? window : null);
