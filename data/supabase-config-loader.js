// Accaoui §34a Lern-App – Supabase Config Loader
// Stand: v26.16a
//
// Sicherer Vorbereitungs-Loader.
// Keine echten Keys.
// Keine automatische Live-Verbindung.
// Kein Supabase-Client.
// Kein Login-Zwang.

(function () {
  const VERSION = "v26.16a";
  const LOCAL_CONFIG_PATH = "data/supabase-config.local.js";
  const EXAMPLE_CONFIG_PATH = "data/supabase-config.example.js";
  const LOCAL_CONFIG_SCRIPT_ID = "accaoui-supabase-local-config-script";

  function getWindowConfig() {
    return window.ACCAOUI_SUPABASE_CONFIG;
  }

  function isAutoLoadEnabled() {
    return window.ACCAOUI_SUPABASE_CONFIG_AUTO_LOAD_LOCAL === true;
  }

  function getConfigValueState() {
    const config = getWindowConfig();

    if (!config) {
      return {
        status: "no_config_loaded",
        isConfigured: false,
        isPlaceholder: false,
        reason: "window_config_missing"
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
        isPlaceholder: true,
        reason: "placeholder_or_missing_values"
      };
    }

    return {
      status: "config_available",
      isConfigured: true,
      isPlaceholder: false,
      reason: "public_config_present"
    };
  }

  function getConfigLoaderState() {
    const configState = getConfigValueState();
    const autoLoadEnabled = isAutoLoadEnabled();

    let status = "local_config_autoload_disabled";
    let reason = "autoload_flag_not_enabled";

    if (configState.status === "config_available") {
      status = "config_available_from_window";
      reason = "window_config_available";
    } else if (configState.status === "placeholder_config") {
      status = "placeholder_config_from_window";
      reason = "window_config_is_placeholder";
    } else if (autoLoadEnabled) {
      status = "local_config_autoload_armed";
      reason = "autoload_flag_enabled_but_not_started";
    }

    return {
      version: VERSION,
      status,
      isSafeLocalMode: true,
      isAutoLoadEnabled: autoLoadEnabled,
      canAttemptLocalConfigLoad: autoLoadEnabled,
      localConfigPath: LOCAL_CONFIG_PATH,
      exampleConfigPath: EXAMPLE_CONFIG_PATH,
      reason,
      configState
    };
  }

  function loadLocalConfigIfEnabled() {
    if (!isAutoLoadEnabled()) {
      return Promise.resolve({
        ...getConfigLoaderState(),
        loadStatus: "skipped",
        reason: "autoload_flag_not_enabled"
      });
    }

    if (typeof document === "undefined") {
      return Promise.resolve({
        ...getConfigLoaderState(),
        loadStatus: "skipped",
        reason: "document_missing"
      });
    }

    const existingScript = document.getElementById(LOCAL_CONFIG_SCRIPT_ID);
    if (existingScript) {
      return Promise.resolve({
        ...getConfigLoaderState(),
        loadStatus: "already_requested",
        reason: "local_config_script_already_exists"
      });
    }

    return new Promise((resolve) => {
      const script = document.createElement("script");
      script.id = LOCAL_CONFIG_SCRIPT_ID;
      script.src = LOCAL_CONFIG_PATH;
      script.async = false;

      script.onload = function () {
        resolve({
          ...getConfigLoaderState(),
          loadStatus: "loaded",
          reason: "local_config_script_loaded"
        });
      };

      script.onerror = function () {
        resolve({
          ...getConfigLoaderState(),
          loadStatus: "failed_safe",
          reason: "local_config_script_missing_or_blocked"
        });
      };

      document.head.appendChild(script);
    });
  }

  window.ACCAOUI_SUPABASE_CONFIG_LOADER = {
    version: VERSION,
    localConfigPath: LOCAL_CONFIG_PATH,
    exampleConfigPath: EXAMPLE_CONFIG_PATH,
    isAutoLoadEnabled,
    getWindowConfig,
    getConfigValueState,
    getConfigLoaderState,
    loadLocalConfigIfEnabled
  };

  console.info(
    "Accaoui Supabase Config Loader geladen:",
    VERSION,
    getConfigLoaderState().status
  );
})();
