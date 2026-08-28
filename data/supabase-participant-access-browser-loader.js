// Accaoui §34a Lern-App – kontrollierter Browser-Loader des Teilnehmerzugangs
// Stand: v27.36f

(function installParticipantAccessBrowserLoader(browserRoot, documentRef) {
  "use strict";

  const loaderId = "accaoui-participant-access-browser-loader";
  const readinessName =
    "ACCAOUI_PARTICIPANT_ACCESS_BROWSER_LOADER_READY";

  if (!browserRoot || !documentRef) {
    return;
  }

  let loaderElement;

  try {
    loaderElement = documentRef.getElementById(loaderId);
  } catch (_error) {
    return;
  }

  if (!loaderElement) {
    return;
  }

  let enabled;

  try {
    enabled = loaderElement.getAttribute("data-enabled");
  } catch (_error) {
    return;
  }

  if (enabled !== "true") {
    return;
  }

  let existingReadiness;

  try {
    existingReadiness = browserRoot[readinessName];
  } catch (_error) {
    return;
  }

  if (existingReadiness !== undefined) {
    return;
  }

  let settleReadiness;
  const readiness = new Promise((resolve) => {
    settleReadiness = resolve;
  });

  try {
    Object.defineProperty(browserRoot, readinessName, {
      value: readiness,
      enumerable: true,
      configurable: false,
      writable: false
    });
  } catch (_error) {
    return;
  }

  function loadLocalScript(source) {
    return new Promise((resolve, reject) => {
      try {
        const script = documentRef.createElement("script");
        script.src = source;
        script.async = false;
        script.onload = () => resolve();
        script.onerror = () => reject(new Error("resource_load_failed"));

        const parent =
          loaderElement.parentNode ||
          documentRef.head ||
          documentRef.documentElement;

        if (!parent || typeof parent.insertBefore !== "function") {
          reject(new Error("resource_parent_missing"));
          return;
        }

        parent.insertBefore(script, loaderElement);
      } catch (_error) {
        reject(new Error("resource_install_failed"));
      }
    });
  }

  async function installRequestedChain() {
    try {
      await loadLocalScript(
        "data/supabase-participant-access-adapter.js"
      );

      if (
        typeof browserRoot.ACCAOUI_PARTICIPANT_ACCESS_ADAPTER_FACTORY !==
        "function"
      ) {
        throw new Error("adapter_factory_invalid");
      }

      await loadLocalScript(
        "data/supabase-participant-access-bootstrap-bridge.js"
      );

      if (
        typeof browserRoot
          .ACCAOUI_PARTICIPANT_ACCESS_BOOTSTRAP_BRIDGE_FACTORY !==
        "function"
      ) {
        throw new Error("bridge_factory_invalid");
      }

      await loadLocalScript(
        "data/supabase-participant-access-browser-provider.js"
      );

      const provider = browserRoot.ACCAOUI_PARTICIPANT_ACCESS_APP_PROVIDER;

      if (
        provider === null ||
        typeof provider !== "object" ||
        Array.isArray(provider) ||
        typeof provider.resolveAccess !== "function"
      ) {
        throw new Error("provider_invalid");
      }

      settleReadiness(Object.freeze({
        requested: true,
        ready: true,
        status: "ready"
      }));
    } catch (_error) {
      settleReadiness(Object.freeze({
        requested: true,
        ready: false,
        status: "error"
      }));
    }
  }

  installRequestedChain();
})(
  typeof window !== "undefined" ? window : null,
  typeof document !== "undefined" ? document : null
);
