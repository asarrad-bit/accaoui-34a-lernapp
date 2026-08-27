// Accaoui §34a Lern-App – Browser-Komposition des Teilnehmerzugangs
// Stand: v27.36e

(function installParticipantAccessBrowserProvider(browserRoot) {
  "use strict";

  if (!browserRoot) {
    return;
  }

  // fail-closed: technische Fehler liefern ausschließlich sichere Codes.
  function blocked(code) {
    return Object.freeze({ allowed: false, code });
  }

  function isRecord(value) {
    return value !== null && typeof value === "object" && !Array.isArray(value);
  }

  function isValidResult(value) {
    if (!isRecord(value)) {
      return false;
    }

    let allowed;
    let code;

    try {
      allowed = value.allowed;
      code = value.code;
    } catch (_error) {
      return false;
    }

    if (typeof allowed !== "boolean") {
      return false;
    }
    if (typeof code !== "string" || code.length === 0) {
      return false;
    }
    if (allowed) {
      return code === "access_allowed";
    }
    return code !== "access_allowed";
  }

  function utcNow() {
    return new Date().toISOString();
  }

  async function resolveAccess() {
    let bootstrap;
    let adapterFactory;
    let bridgeFactory;

    try {
      bootstrap = browserRoot.ACCAOUI_SUPABASE_BOOTSTRAP;
      adapterFactory =
        browserRoot.ACCAOUI_PARTICIPANT_ACCESS_ADAPTER_FACTORY;
      bridgeFactory =
        browserRoot.ACCAOUI_PARTICIPANT_ACCESS_BOOTSTRAP_BRIDGE_FACTORY;
    } catch (_error) {
      return blocked("provider_dependency_read_failed");
    }

    if (bootstrap === null || bootstrap === undefined) {
      return blocked("provider_bootstrap_missing");
    }
    if (!isRecord(bootstrap)) {
      return blocked("provider_bootstrap_invalid");
    }
    if (adapterFactory === null || adapterFactory === undefined) {
      return blocked("provider_adapter_factory_missing");
    }
    if (typeof adapterFactory !== "function") {
      return blocked("provider_adapter_factory_invalid");
    }
    if (bridgeFactory === null || bridgeFactory === undefined) {
      return blocked("provider_bridge_factory_missing");
    }
    if (typeof bridgeFactory !== "function") {
      return blocked("provider_bridge_factory_invalid");
    }

    const bridgeDependencies = Object.freeze({
      bootstrap,
      createParticipantAccessAdapter: adapterFactory,
      utcNow
    });

    let bridge;
    try {
      bridge = bridgeFactory(bridgeDependencies);
    } catch (_error) {
      return blocked("provider_bridge_factory_failed");
    }

    if (!isRecord(bridge)) {
      return blocked("provider_bridge_invalid");
    }

    let bridgeResolveAccess;
    try {
      bridgeResolveAccess = bridge.resolveAccess;
    } catch (_error) {
      return blocked("provider_bridge_resolve_access_failed");
    }

    if (typeof bridgeResolveAccess !== "function") {
      return blocked("provider_bridge_resolve_access_invalid");
    }

    let result;
    try {
      result = await bridgeResolveAccess.call(bridge);
    } catch (_error) {
      return blocked("provider_bridge_resolve_access_failed");
    }

    if (!isValidResult(result)) {
      return blocked("provider_bridge_result_invalid");
    }

    return result;
  }

  const provider = Object.freeze({ resolveAccess });
  let existingProvider;

  try {
    existingProvider =
      browserRoot.ACCAOUI_PARTICIPANT_ACCESS_APP_PROVIDER;
  } catch (_error) {
    return;
  }

  if (existingProvider !== undefined) {
    return;
  }

  try {
    Object.defineProperty(
      browserRoot,
      "ACCAOUI_PARTICIPANT_ACCESS_APP_PROVIDER",
      {
        value: provider,
        enumerable: true,
        configurable: false,
        writable: false
      }
    );
  } catch (_error) {
    // Fremde oder nicht beschreibbare Provider-Grenzen bleiben unverändert.
  }
})(typeof window !== "undefined" ? window : null);
