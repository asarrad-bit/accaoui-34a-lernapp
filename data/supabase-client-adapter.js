// Accaoui §34a Lern-App – Supabase Client Adapter
// Stand: v26.8c
//
// Aktuell bewusst OHNE aktiven Supabase-Client.
// Keine echte Verbindung.
// Keine echten Keys.
// Kein Login-Zwang.

(function () {
  function getConfigState() {
    const config = window.ACCAOUI_SUPABASE_CONFIG;

    if (!config) {
      return {
        status: "local_mode",
        isConfigured: false,
        reason: "no_config_loaded"
      };
    }

    const url = typeof config.url === "string" ? config.url.trim() : "";
    const anonKey = typeof config.anonKey === "string" ? config.anonKey.trim() : "";

    const hasPlaceholder =
      !url ||
      !anonKey ||
      url.includes("YOUR-PROJECT") ||
      anonKey.includes("YOUR_PUBLIC_ANON_KEY");

    if (hasPlaceholder) {
      return {
        status: "placeholder_config",
        isConfigured: false,
        reason: "placeholder_or_missing_values"
      };
    }

    return {
      status: "config_available",
      isConfigured: true,
      reason: "public_config_present"
    };
  }

  function getSdkState() {
    const supabaseGlobal = window.supabase;

    if (!supabaseGlobal) {
      return {
        status: "sdk_missing",
        hasSdk: false,
        reason: "window_supabase_missing"
      };
    }

    if (typeof supabaseGlobal.createClient !== "function") {
      return {
        status: "sdk_invalid",
        hasSdk: false,
        reason: "createClient_missing"
      };
    }

    return {
      status: "sdk_available",
      hasSdk: true,
      reason: "createClient_available"
    };
  }

  function getClientState() {
    const configState = getConfigState();
    const sdkState = getSdkState();

    if (!configState.isConfigured) {
      return {
        status: "local_mode",
        isReady: false,
        hasSdk: sdkState.hasSdk,
        configState,
        sdkState
      };
    }

    if (!sdkState.hasSdk) {
      return {
        status: "sdk_missing",
        isReady: false,
        hasSdk: false,
        configState,
        sdkState
      };
    }

    return {
      status: "client_ready_later",
      isReady: false,
      hasSdk: true,
      configState,
      sdkState
    };
  }

  function getCurrentSession() {
    return Promise.resolve({
      status: "no_session_adapter_stub",
      session: null
    });
  }

  function getParticipantAccessState() {
    return Promise.resolve({
      isAllowed: true,
      status: "local_access_granted",
      source: "supabase-client-adapter-stub-v26.8c"
    });
  }

  window.ACCAOUI_SUPABASE_ADAPTER = {
    version: "v26.8c",
    getConfigState,
    getSdkState,
    getClientState,
    getCurrentSession,
    getParticipantAccessState
  };

  console.info("Accaoui Supabase Adapter geladen:", window.ACCAOUI_SUPABASE_ADAPTER.version);
})();
