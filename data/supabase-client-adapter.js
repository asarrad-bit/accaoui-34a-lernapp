// Accaoui §34a Lern-App – Supabase Client Adapter
// Stand: v26.7c
//
// Aktuell bewusst OHNE Supabase-SDK.
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

  function getClientState() {
    const configState = getConfigState();

    return {
      status: configState.isConfigured ? "client_ready_later" : "local_mode",
      isReady: false,
      hasSdk: false,
      configState
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
      source: "supabase-client-adapter-stub-v26.7c"
    });
  }

  window.ACCAOUI_SUPABASE_ADAPTER = {
    version: "v26.7c",
    getConfigState,
    getClientState,
    getCurrentSession,
    getParticipantAccessState
  };

  console.info("Accaoui Supabase Adapter geladen:", window.ACCAOUI_SUPABASE_ADAPTER.version);
})();
