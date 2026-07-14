// Accaoui §34a Lern-App – Supabase Client Bootstrap
// Stand: v27.23a
//
// Manueller MVP-Live-Einstieg.
// Keine automatische Client-Erstellung.
// Erforderlich:
// 1. gültige öffentliche Konfiguration
// 2. geladenes Supabase-SDK
// 3. ACCAOUI_SUPABASE_LIVE_ENABLED === true
// 4. ACCAOUI_SUPABASE_CLIENT_INIT_CONFIRMED === true
// 5. ausdrücklicher Aufruf von initializeClient()

(function () {
  "use strict";

  const VERSION = "v27.23a";
  const CLIENT_GLOBAL_NAME = "ACCAOUI_SUPABASE_CLIENT";

  let client = null;
  let lastError = null;

  function getAdapter() {
    return window.ACCAOUI_SUPABASE_ADAPTER || null;
  }

  function getConfigState() {
    const adapter = getAdapter();

    if (adapter && typeof adapter.getConfigState === "function") {
      return adapter.getConfigState();
    }

    return {
      status: "adapter_missing",
      isConfigured: false,
      reason: "supabase_adapter_missing"
    };
  }

  function getSdkState() {
    const adapter = getAdapter();

    if (adapter && typeof adapter.getSdkState === "function") {
      return adapter.getSdkState();
    }

    return {
      status: "adapter_missing",
      hasSdk: false,
      reason: "supabase_adapter_missing"
    };
  }

  function getStoredClient() {
    return client || window[CLIENT_GLOBAL_NAME] || null;
  }

  function getState() {
    const adapter = getAdapter();
    const configState = getConfigState();
    const sdkState = getSdkState();
    const storedClient = getStoredClient();

    const isLiveEnabled =
      window.ACCAOUI_SUPABASE_LIVE_ENABLED === true;

    const isInitializationConfirmed =
      window.ACCAOUI_SUPABASE_CLIENT_INIT_CONFIRMED === true;

    const prerequisitesReady =
      Boolean(adapter) &&
      configState.isConfigured === true &&
      sdkState.hasSdk === true &&
      isLiveEnabled &&
      isInitializationConfirmed;

    let status = "local_safe_mode";
    let reason = "live_bootstrap_not_requested";

    if (storedClient) {
      status = "client_initialized";
      reason = "supabase_client_available";
    } else if (!adapter) {
      status = "adapter_missing";
      reason = "supabase_adapter_missing";
    } else if (!isLiveEnabled) {
      status = "live_switch_disabled";
      reason = "explicit_live_switch_required";
    } else if (configState.isConfigured !== true) {
      status = "config_missing";
      reason = configState.reason || "valid_public_config_required";
    } else if (sdkState.hasSdk !== true) {
      status = "sdk_missing";
      reason = sdkState.reason || "supabase_sdk_required";
    } else if (!isInitializationConfirmed) {
      status = "initialization_confirmation_missing";
      reason = "second_explicit_confirmation_required";
    } else if (lastError) {
      status = "initialization_failed";
      reason = "create_client_failed";
    } else {
      status = "ready_for_manual_initialization";
      reason = "all_prerequisites_available";
    }

    return {
      version: VERSION,
      status,
      reason,
      isManualOnly: true,
      isLiveEnabled,
      isInitializationConfirmed,
      hasAdapter: Boolean(adapter),
      hasConfig: configState.isConfigured === true,
      hasSdk: sdkState.hasSdk === true,
      hasClient: Boolean(storedClient),
      canInitializeClient:
        prerequisitesReady && !storedClient,
      autoInitializationAttempted: false,
      configState,
      sdkState,
      lastError
    };
  }

  function initializeClient() {
    const state = getState();

    if (state.hasClient) {
      return {
        ...state,
        status: "client_already_initialized",
        reason: "existing_client_reused"
      };
    }

    if (!state.canInitializeClient) {
      return state;
    }

    try {
      const config = window.ACCAOUI_SUPABASE_CONFIG;
      const supabaseSdk = window.supabase;

      const createdClient = supabaseSdk.createClient(
        config.url.trim(),
        config.anonKey.trim(),
        {
          auth: {
            persistSession: true,
            autoRefreshToken: true,
            detectSessionInUrl: true
          },
          global: {
            headers: {
              "X-Client-Info": "accaoui-34a-web-v27.23a"
            }
          }
        }
      );

      if (
        !createdClient ||
        typeof createdClient.from !== "function" ||
        !createdClient.auth
      ) {
        throw new Error("Supabase createClient lieferte keinen gültigen Client.");
      }

      client = createdClient;
      window[CLIENT_GLOBAL_NAME] = createdClient;
      lastError = null;

      return getState();
    } catch (error) {
      lastError = {
        name: error && error.name ? error.name : "Error",
        message:
          error && error.message
            ? error.message
            : "Unbekannter Initialisierungsfehler"
      };

      return getState();
    }
  }

  function clearInitializationError() {
    lastError = null;
    return getState();
  }

  window.ACCAOUI_SUPABASE_BOOTSTRAP = {
    version: VERSION,
    getState,
    getClient: getStoredClient,
    initializeClient,
    clearInitializationError
  };

  console.info(
    "Accaoui Supabase Bootstrap geladen:",
    VERSION,
    getState().status
  );
})();
