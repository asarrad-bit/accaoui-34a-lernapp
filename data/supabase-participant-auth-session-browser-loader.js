// Accaoui §34a Lern-App – kontrollierter Auth-/Session-Browser-Loader
// Stand: v27.37e

(function installParticipantAuthSessionBrowserLoader(browserRoot, documentRef) {
  "use strict";

  const loaderId = "accaoui-participant-auth-session-browser-loader";
  const readinessName = "ACCAOUI_PARTICIPANT_AUTH_SESSION_BROWSER_LOADER_READY";
  const boundaries = [
    "ACCAOUI_PARTICIPANT_AUTH_SESSION_ADAPTER_FACTORY",
    "ACCAOUI_PARTICIPANT_AUTH_SESSION_BOOTSTRAP_BRIDGE_FACTORY",
    "ACCAOUI_PARTICIPANT_AUTH_SESSION_APP_PROVIDER"
  ];
  const sources = [
    "data/supabase-participant-auth-session-adapter.js",
    "data/supabase-participant-auth-session-bootstrap-bridge.js",
    "data/supabase-participant-auth-session-browser-provider.js"
  ];
  const methods = ["resolveSession", "signIn", "signOut"];

  if (!browserRoot || !documentRef) {
    return;
  }

  let loaderElement;
  let settleReadiness;

  try {
    loaderElement = documentRef.getElementById(loaderId);
    if (
      !loaderElement ||
      documentRef.currentScript !== loaderElement ||
      loaderElement.tagName !== "SCRIPT" ||
      loaderElement.getAttribute("data-enabled") !== "true" ||
      readinessName in browserRoot
    ) {
      return;
    }

    // Publish the one-shot reservation before any asynchronous work.
    const readiness = Object.freeze(new Promise((resolve) => {
      settleReadiness = resolve;
    }));
    Object.defineProperty(browserRoot, readinessName, {
      value: readiness,
      enumerable: true,
      configurable: false,
      writable: false
    });
  } catch (_error) {
    // A blocked readiness boundary cannot be replaced to report an error.
    return;
  }

  const failed = Object.freeze({ requested: true, ready: false, status: "error" });
  const ready = Object.freeze({ requested: true, ready: true, status: "ready" });
  const installed = [];

  function readExport(index) {
    const field = Object.getOwnPropertyDescriptor(browserRoot, boundaries[index]);
    if (
      !field || !Object.prototype.hasOwnProperty.call(field, "value") ||
      field.configurable || field.writable || !field.enumerable
    ) {
      return null;
    }
    const value = field.value;
    if (index < 2) {
      return typeof value === "function" ? value : null;
    }
    if (
      value === null || typeof value !== "object" ||
      Object.getPrototypeOf(value) !== Object.prototype || !Object.isFrozen(value)
    ) {
      return null;
    }
    const keys = Reflect.ownKeys(value);
    if (keys.length !== methods.length || !methods.every((key) => keys.includes(key))) {
      return null;
    }
    for (const name of methods) {
      const method = Object.getOwnPropertyDescriptor(value, name);
      if (
        !method || !Object.prototype.hasOwnProperty.call(method, "value") ||
        !method.enumerable || method.configurable || method.writable ||
        typeof method.value !== "function"
      ) {
        return null;
      }
    }
    return value;
  }

  function loadLocalScript(source) {
    return new Promise((resolve) => {
      let script;
      let parent;
      let timer;
      let timerStarted = false;
      let finished = false;

      function finish(ok) {
        if (finished) {
          return;
        }
        finished = true;
        try {
          if (timerStarted) {
            browserRoot.clearTimeout(timer);
          }
        } catch (_error) {
          ok = false;
        }
        try {
          if (script) {
            script.onload = null;
            script.onerror = null;
            if (!ok && parent && script.parentNode === parent) {
              parent.removeChild(script);
            }
          }
        } catch (_error) {
          ok = false;
        }
        resolve(ok);
      }

      try {
        parent = loaderElement.parentNode;
        if (!parent || typeof parent.insertBefore !== "function") {
          finish(false);
          return;
        }
        script = documentRef.createElement("script");
        script.async = false;
        script.src = source;
        if (script.src !== source) {
          finish(false);
          return;
        }
        script.onload = () => finish(true);
        script.onerror = () => finish(false);
        timer = browserRoot.setTimeout(() => finish(false), 15000);
        timerStarted = true;
        if (finished) {
          browserRoot.clearTimeout(timer);
          return;
        }
        parent.insertBefore(script, loaderElement);
      } catch (_error) {
        finish(false);
      }
    });
  }

  async function installRequestedChain() {
    try {
      // Bind resources to the document URL, not to a possibly foreign <base>.
      const page = new URL(documentRef.URL);
      if (
        (page.protocol !== "http:" && page.protocol !== "https:") ||
        page.username !== "" || page.password !== ""
      ) {
        settleReadiness(failed);
        return;
      }
      for (let index = 0; index < sources.length; index += 1) {
        for (let pending = index; pending < boundaries.length; pending += 1) {
          // Presence, not value: own/inherited undefined is occupied as well.
          if (boundaries[pending] in browserRoot) {
            settleReadiness(failed);
            return;
          }
        }
        for (let previous = 0; previous < index; previous += 1) {
          if (readExport(previous) !== installed[previous]) {
            settleReadiness(failed);
            return;
          }
        }
        const source = new URL(sources[index], page).href;
        if (!await loadLocalScript(source)) {
          settleReadiness(failed);
          return;
        }
        const value = readExport(index);
        if (value === null) {
          settleReadiness(failed);
          return;
        }
        installed.push(value);
      }
      // Readiness means that all exports exist; no factory or auth method is called.
      for (let index = 0; index < boundaries.length; index += 1) {
        if (readExport(index) !== installed[index]) {
          settleReadiness(failed);
          return;
        }
      }
      settleReadiness(ready);
    } catch (_error) {
      settleReadiness(failed);
    }
  }

  installRequestedChain();
})(
  typeof window !== "undefined" ? window : null,
  typeof document !== "undefined" ? document : null
);
