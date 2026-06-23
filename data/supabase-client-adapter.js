// Accaoui §34a Lern-App – Supabase Client Adapter
// Stand: v26.10a
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

  function getClientReadinessState() {
    const configState = getConfigState();
    const sdkState = getSdkState();

    if (configState.status === "local_mode") {
      return {
        status: "local_mode",
        isReady: false,
        canCreateClient: false,
        hasSdk: sdkState.hasSdk,
        reason: "no_config_loaded",
        configState,
        sdkState
      };
    }

    if (configState.status === "placeholder_config") {
      return {
        status: "placeholder_config",
        isReady: false,
        canCreateClient: false,
        hasSdk: sdkState.hasSdk,
        reason: "placeholder_or_missing_values",
        configState,
        sdkState
      };
    }

    if (sdkState.status === "sdk_missing") {
      return {
        status: "sdk_missing",
        isReady: false,
        canCreateClient: false,
        hasSdk: false,
        reason: "window_supabase_missing",
        configState,
        sdkState
      };
    }

    if (sdkState.status === "sdk_invalid") {
      return {
        status: "sdk_invalid",
        isReady: false,
        canCreateClient: false,
        hasSdk: false,
        reason: "createClient_missing",
        configState,
        sdkState
      };
    }

    return {
      status: "client_ready_later",
      isReady: false,
      canCreateClient: false,
      wouldCreateClientWhenEnabled: true,
      hasSdk: true,
      reason: "sdk_and_config_available_client_creation_disabled_in_stub",
      configState,
      sdkState
    };
  }

  function getClientState() {
    return getClientReadinessState();
  }

  function getAuthReadinessState() {
    const clientState = getClientReadinessState();

    if (!clientState.isReady) {
      return {
        status: "client_not_ready",
        canCheckSession: false,
        hasSession: false,
        reason: clientState.reason,
        clientState
      };
    }

    return {
      status: "auth_ready_later",
      canCheckSession: false,
      hasSession: false,
      reason: "auth_check_disabled_in_stub",
      futureStatuses: [
        "session_available_later",
        "no_session_later",
        "auth_error_later"
      ],
      clientState
    };
  }

  function getCurrentSession() {
    const authState = getAuthReadinessState();

    return Promise.resolve({
      status: "no_session_client_not_ready",
      session: null,
      authState
    });
  }

  function getParticipantAccessState() {
    return Promise.resolve({
      isAllowed: true,
      status: "local_access_granted",
      source: "supabase-client-adapter-stub-v26.10a"
    });
  }

  window.ACCAOUI_SUPABASE_ADAPTER = {
    version: "v26.10a",
    getConfigState,
    getSdkState,
    getClientReadinessState,
    getClientState,
    getAuthReadinessState,
    getCurrentSession,
    getParticipantAccessState
  };

  console.info("Accaoui Supabase Adapter geladen:", window.ACCAOUI_SUPABASE_ADAPTER.version);
})();
