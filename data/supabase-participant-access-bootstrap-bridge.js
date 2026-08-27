// Accaoui §34a Lern-App – lokale Teilnehmerzugangs-Bootstrap-Brücke
// Stand: v27.36c
//
// Isoliertes CommonJS-Modul. Die Brücke liest pro Aufruf ausschließlich den
// bereits vorhandenen Client des injizierten Bootstrap-Providers und delegiert
// die Zugangsentscheidung an die injizierte bestehende v27.36b-
// "participant-access"-Adapter-Factory.

(function exposeParticipantAccessBootstrapBridge(browserRoot, commonJsModule) {
"use strict";

const VERSION = "v27.36c";

function blocked(code) {
  return Object.freeze({ allowed: false, code });
}

function isRecord(value) {
  return value !== null && typeof value === "object" && !Array.isArray(value);
}

function isValidAdapterResult(value) {
  if (!isRecord(value)) {
    return false;
  }

  if (typeof value.allowed !== "boolean") {
    return false;
  }

  if (typeof value.code !== "string" || value.code.length === 0) {
    return false;
  }

  if (value.allowed) {
    return value.code === "access_allowed";
  }

  return value.code !== "access_allowed";
}

function createParticipantAccessBootstrapBridge(dependencies) {
  let dependencyCode = null;
  let bootstrap = null;
  let createParticipantAccessAdapter = null;
  let utcNow = null;

  if (!isRecord(dependencies)) {
    dependencyCode = "dependencies_invalid";
  } else {
    let dependencyKeys;

    try {
      dependencyKeys = Object.keys(dependencies);
      bootstrap = dependencies.bootstrap;
      createParticipantAccessAdapter =
        dependencies.createParticipantAccessAdapter;
      utcNow = dependencies.utcNow;
    } catch (_error) {
      dependencyCode = "dependencies_invalid";
    }

    if (
      !dependencyCode &&
      dependencyKeys.some(
        (key) =>
          key !== "bootstrap" &&
          key !== "createParticipantAccessAdapter" &&
          key !== "utcNow"
      )
    ) {
      dependencyCode = "dependency_fields_invalid";
    } else if (
      !dependencyCode &&
      (bootstrap === null || bootstrap === undefined)
    ) {
      dependencyCode = "bootstrap_missing";
    } else if (!dependencyCode && !isRecord(bootstrap)) {
      dependencyCode = "bootstrap_invalid";
    } else if (
      !dependencyCode &&
      (createParticipantAccessAdapter === null ||
        createParticipantAccessAdapter === undefined)
    ) {
      dependencyCode = "adapter_factory_missing";
    } else if (
      !dependencyCode &&
      typeof createParticipantAccessAdapter !== "function"
    ) {
      dependencyCode = "adapter_factory_invalid";
    } else if (!dependencyCode && typeof utcNow !== "function") {
      dependencyCode = "utc_source_invalid";
    }
  }

  async function resolveAccess() {
    if (dependencyCode) {
      return blocked(dependencyCode);
    }

    let getClient;
    let client;

    try {
      getClient = bootstrap.getClient;
    } catch (_error) {
      return blocked("bootstrap_get_client_failed");
    }

    if (typeof getClient !== "function") {
      return blocked("bootstrap_get_client_invalid");
    }

    try {
      client = getClient.call(bootstrap);
    } catch (_error) {
      return blocked("bootstrap_get_client_failed");
    }

    if (client === null || client === undefined) {
      return blocked("client_missing");
    }

    let adapter;

    try {
      adapter = createParticipantAccessAdapter({ client, utcNow });
    } catch (_error) {
      return blocked("adapter_factory_failed");
    }

    if (!isRecord(adapter)) {
      return blocked("adapter_invalid");
    }

    let adapterResolveAccess;

    try {
      adapterResolveAccess = adapter.resolveAccess;
    } catch (_error) {
      return blocked("adapter_resolve_access_failed");
    }

    if (typeof adapterResolveAccess !== "function") {
      return blocked("adapter_resolve_access_invalid");
    }

    let result;

    try {
      result = await adapterResolveAccess.call(adapter);
    } catch (_error) {
      return blocked("adapter_resolve_access_failed");
    }

    try {
      if (!isValidAdapterResult(result)) {
        return blocked("adapter_result_invalid");
      }
    } catch (_error) {
      return blocked("adapter_result_invalid");
    }

    return result;
  }

  return Object.freeze({
    version: VERSION,
    resolveAccess
  });
}

// CommonJS-Vertrag: module.exports.
const participantAccessBootstrapBridgeApi = Object.freeze({
  version: VERSION,
  createParticipantAccessBootstrapBridge
});

if (commonJsModule && typeof commonJsModule === "object") {
  commonJsModule.exports = participantAccessBootstrapBridgeApi;
}

if (browserRoot) {
  let existingFactory;

  try {
    existingFactory =
      browserRoot.ACCAOUI_PARTICIPANT_ACCESS_BOOTSTRAP_BRIDGE_FACTORY;
  } catch (_error) {
    return;
  }

  if (existingFactory === undefined) {
    try {
      browserRoot.ACCAOUI_PARTICIPANT_ACCESS_BOOTSTRAP_BRIDGE_FACTORY =
        createParticipantAccessBootstrapBridge;
    } catch (_error) {
      // Eine nicht beschreibbare bestehende Grenze wird nicht überschrieben.
    }
  }
}
})(
  typeof self !== "undefined" ? self : null,
  typeof module !== "undefined" ? module : null
);
