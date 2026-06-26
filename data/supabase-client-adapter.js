// Accaoui §34a Lern-App – Supabase Client Adapter
// Stand: v26.27a
//
// Aktuell bewusst OHNE aktiven Supabase-Client.
// Keine echte Verbindung.
// Keine echten Keys.
// Kein Login-Zwang.
// Supabase-Live-Modus nur mit bewusstem Schalter:
// window.ACCAOUI_SUPABASE_LIVE_ENABLED === true

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

  function isSupabaseLiveEnabled() {
    return window.ACCAOUI_SUPABASE_LIVE_ENABLED === true;
  }

  function getSupabaseFailSafeState() {
    const configState = getConfigState();
    const sdkState = getSdkState();
    const isLiveEnabled = isSupabaseLiveEnabled();

    if (!isLiveEnabled && configState.isConfigured && sdkState.hasSdk) {
      return {
        status: "live_switch_disabled_with_config_and_sdk",
        isSafe: true,
        isLiveEnabled,
        reason: "live_switch_required_before_client_creation",
        configState,
        sdkState
      };
    }

    if (!isLiveEnabled && configState.isConfigured) {
      return {
        status: "live_switch_disabled_with_config",
        isSafe: true,
        isLiveEnabled,
        reason: "live_switch_required_before_supabase_use",
        configState,
        sdkState
      };
    }

    if (!isLiveEnabled && sdkState.hasSdk) {
      return {
        status: "live_switch_disabled_with_sdk",
        isSafe: true,
        isLiveEnabled,
        reason: "live_switch_required_before_sdk_use",
        configState,
        sdkState
      };
    }

    if (isLiveEnabled && !configState.isConfigured && !sdkState.hasSdk) {
      return {
        status: "live_switch_enabled_but_config_and_sdk_missing",
        isSafe: true,
        isLiveEnabled,
        reason: "missing_config_and_sdk",
        configState,
        sdkState
      };
    }

    if (isLiveEnabled && !configState.isConfigured) {
      return {
        status: "live_switch_enabled_but_config_missing",
        isSafe: true,
        isLiveEnabled,
        reason: "missing_config",
        configState,
        sdkState
      };
    }

    if (isLiveEnabled && !sdkState.hasSdk) {
      return {
        status: "live_switch_enabled_but_sdk_missing",
        isSafe: true,
        isLiveEnabled,
        reason: "missing_sdk",
        configState,
        sdkState
      };
    }

    return {
      status: isLiveEnabled ? "live_prerequisites_available_client_still_disabled" : "local_mode_safe",
      isSafe: true,
      isLiveEnabled,
      reason: isLiveEnabled ? "client_creation_still_disabled_in_stub" : "local_mode_without_live_switch",
      configState,
      sdkState
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
    const isLiveEnabled = isSupabaseLiveEnabled();
    const failSafeState = getSupabaseFailSafeState();

    if (configState.status === "local_mode") {
      return {
        status: "local_mode",
        isReady: false,
        canCreateClient: false,
        isLiveEnabled,
        hasSdk: sdkState.hasSdk,
        reason: "no_config_loaded",
        configState,
        sdkState,
        failSafeState
      };
    }

    if (configState.status === "placeholder_config") {
      return {
        status: "placeholder_config",
        isReady: false,
        canCreateClient: false,
        isLiveEnabled,
        hasSdk: sdkState.hasSdk,
        reason: "placeholder_or_missing_values",
        configState,
        sdkState,
        failSafeState
      };
    }

    if (sdkState.status === "sdk_missing") {
      return {
        status: "sdk_missing",
        isReady: false,
        canCreateClient: false,
        isLiveEnabled,
        hasSdk: false,
        reason: "window_supabase_missing",
        configState,
        sdkState,
        failSafeState
      };
    }

    if (sdkState.status === "sdk_invalid") {
      return {
        status: "sdk_invalid",
        isReady: false,
        canCreateClient: false,
        isLiveEnabled,
        hasSdk: false,
        reason: "createClient_missing",
        configState,
        sdkState,
        failSafeState
      };
    }

    if (!isLiveEnabled) {
      return {
        status: "live_switch_disabled",
        isReady: false,
        canCreateClient: false,
        isLiveEnabled,
        wouldCreateClientWhenEnabled: true,
        hasSdk: true,
        reason: "supabase_live_switch_disabled",
        configState,
        sdkState,
        failSafeState
      };
    }

    return {
      status: "live_switch_enabled_client_creation_disabled_in_stub",
      isReady: false,
      canCreateClient: false,
      isLiveEnabled,
      wouldCreateClientWhenEnabled: true,
      hasSdk: true,
      reason: "live_switch_enabled_but_client_creation_disabled_in_stub",
      configState,
      sdkState,
      failSafeState
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

  function getParticipantSessionState() {
    const authState = getAuthReadinessState();
    const clientState = getClientReadinessState();

    return {
      version: "v26.27a",
      status: "local_session_stub",
      hasSession: false,
      canCheckSession: false,
      isSessionRequired: false,
      isLocalAccessAllowed: true,
      isSupabaseLive: false,
      isLiveEnabled: isSupabaseLiveEnabled(),
      reason: "participant_session_check_prepared_but_disabled",
      futureStatuses: [
        "session_available_later",
        "no_session_later",
        "session_expired_later",
        "session_error_later"
      ],
      clientState,
      authState
    };
  }

  function getParticipantProfileState() {
    const participantSessionState = getParticipantSessionState();

    return {
      version: "v26.27a",
      status: "local_profile_stub",
      hasProfile: false,
      canLoadProfile: false,
      isProfileRequired: false,
      isLocalAccessAllowed: true,
      isSupabaseLive: false,
      isLiveEnabled: isSupabaseLiveEnabled(),
      profile: null,
      reason: "participant_profile_load_prepared_but_disabled",
      futureStatuses: [
        "profile_available_later",
        "profile_missing_later",
        "profile_inactive_later",
        "profile_error_later"
      ],
      participantSessionState
    };
  }

  function getParticipantCourseState() {
    const participantProfileState = getParticipantProfileState();

    return {
      version: "v26.27a",
      status: "local_course_stub",
      hasCourse: false,
      canLoadCourse: false,
      isCourseRequired: false,
      isCourseExpired: false,
      isLocalAccessAllowed: true,
      isSupabaseLive: false,
      isLiveEnabled: isSupabaseLiveEnabled(),
      course: null,
      reason: "participant_course_load_prepared_but_disabled",
      futureStatuses: [
        "course_active_later",
        "course_expired_later",
        "course_missing_later",
        "course_error_later"
      ],
      participantProfileState
    };
  }

  function getParticipantAccessReadinessState() {
    const authState = getAuthReadinessState();
    const participantSessionState = getParticipantSessionState();
    const participantProfileState = getParticipantProfileState();
    const participantCourseState = getParticipantCourseState();

    if (authState.status === "client_not_ready") {
      return {
        isAllowed: true,
        status: "local_access_granted",
        mode: "local_mode",
        reason: "supabase_not_ready_local_access",
        source: "supabase-client-adapter-stub-v26.27a",
        participantSessionState,
        participantProfileState,
        participantCourseState,
        futureStatuses: [
          "participant_active_later",
          "course_expired_later",
          "participant_blocked_later",
          "no_course_later",
          "no_session_later"
        ],
        authState
      };
    }

    if (!authState.hasSession) {
      return {
        isAllowed: false,
        status: "no_session_later",
        mode: "supabase_mode_later",
        reason: "session_required_later",
        source: "supabase-client-adapter-stub-v26.27a",
        participantSessionState,
        participantProfileState,
        participantCourseState,
        authState
      };
    }

    return {
      isAllowed: false,
      status: "access_check_later",
      mode: "supabase_mode_later",
      reason: "participant_access_check_disabled_in_stub",
      source: "supabase-client-adapter-stub-v26.27a",
      participantSessionState,
      participantProfileState,
      participantCourseState,
      futureStatuses: [
        "participant_active_later",
        "course_expired_later",
        "participant_blocked_later",
        "no_course_later"
      ],
      authState
    };
  }

  function getParticipantAccessDecisionState() {
    const participantAccessState = getParticipantAccessReadinessState();
    const participantSessionState = getParticipantSessionState();
    const participantProfileState = getParticipantProfileState();
    const participantCourseState = getParticipantCourseState();

    const isLocalAccessAllowed =
      participantAccessState.isAllowed === true &&
      participantAccessState.mode === "local_mode" &&
      participantSessionState.isLocalAccessAllowed === true &&
      participantProfileState.isLocalAccessAllowed === true &&
      participantCourseState.isLocalAccessAllowed === true;

    return {
      version: "v26.27a",
      status: isLocalAccessAllowed ? "local_access_decision_allowed" : "access_decision_blocked_later",
      isAllowed: isLocalAccessAllowed,
      isLocalAccessAllowed,
      isLoginRequired: false,
      isSupabaseLive: false,
      isLiveEnabled: isSupabaseLiveEnabled(),
      requiresSession: false,
      requiresProfile: false,
      requiresCourse: false,
      reason: isLocalAccessAllowed ? "local_mode_allows_access_without_login" : "future_supabase_access_decision_blocked",
      blockingReasons: isLocalAccessAllowed ? [] : ["future_access_state_not_allowed"],
      futureStatuses: [
        "access_allowed_later",
        "login_required_later",
        "course_expired_later",
        "profile_blocked_later",
        "access_denied_later"
      ],
      participantAccessState,
      participantSessionState,
      participantProfileState,
      participantCourseState
    };
  }

  function getLoginGateState() {
    const participantAccessDecisionState = getParticipantAccessDecisionState();

    return {
      version: "v26.27a",
      status: "local_login_gate_disabled",
      isGateEnabled: false,
      isLoginRequired: false,
      canRenderLoginGate: false,
      canBlockAccess: false,
      isLocalAccessAllowed: true,
      isSupabaseLive: false,
      isLiveEnabled: isSupabaseLiveEnabled(),
      reason: "login_gate_prepared_but_disabled_in_local_mode",
      futureStatuses: [
        "login_gate_enabled_later",
        "login_required_later",
        "login_optional_later",
        "access_blocked_by_gate_later"
      ],
      participantAccessDecisionState
    };
  }

  function getLoginGateUiState() {
    const loginGateState = getLoginGateState();

    return {
      version: "v26.27a",
      status: "local_login_gate_ui_hidden",
      isVisible: false,
      canRender: false,
      canBlockAccess: false,
      isLoginRequired: false,
      isLocalAccessAllowed: true,
      title: "Login vorbereitet",
      message: "Der Login-Bereich ist vorbereitet, aber im lokalen Modus deaktiviert.",
      primaryAction: null,
      reason: "login_gate_ui_prepared_but_hidden_in_local_mode",
      futureStatuses: [
        "login_gate_ui_visible_later",
        "login_gate_ui_hidden_later",
        "login_gate_ui_blocking_later",
        "login_gate_ui_error_later"
      ],
      loginGateState
    };
  }

  function getLoginFormState() {
    const loginGateUiState = getLoginGateUiState();

    return {
      version: "v26.27a",
      status: "local_login_form_disabled",
      isVisible: false,
      canRender: false,
      canSubmit: false,
      canValidateInput: false,
      canAuthenticate: false,
      isLoginRequired: false,
      isLocalAccessAllowed: true,
      fields: {
        email: "",
        password: ""
      },
      error: null,
      reason: "login_form_prepared_but_disabled_in_local_mode",
      futureStatuses: [
        "login_form_visible_later",
        "login_form_ready_later",
        "login_form_invalid_later",
        "login_form_authenticating_later",
        "login_form_error_later"
      ],
      loginGateUiState
    };
  }

  function getLoginErrorState() {
    const loginFormState = getLoginFormState();

    return {
      version: "v26.27a",
      status: "local_login_error_none",
      hasError: false,
      canShowError: false,
      errorCode: null,
      errorMessage: null,
      isRecoverable: true,
      isLoginRequired: false,
      isLocalAccessAllowed: true,
      reason: "login_error_state_prepared_but_no_error_in_local_mode",
      futureStatuses: [
        "login_error_invalid_credentials_later",
        "login_error_network_later",
        "login_error_session_expired_later",
        "login_error_unknown_later"
      ],
      loginFormState
    };
  }

  function getParticipantAccessState() {
    return Promise.resolve(getParticipantAccessReadinessState());
  }

  function getSupabaseConfigLoaderState() {
    const loader = window.ACCAOUI_SUPABASE_CONFIG_LOADER;

    if (!loader) {
      return {
        status: "config_loader_missing",
        isAvailable: false,
        isSafe: true,
        reason: "config_loader_not_loaded"
      };
    }

    if (typeof loader.getConfigLoaderState !== "function") {
      return {
        status: "config_loader_invalid",
        isAvailable: false,
        isSafe: true,
        reason: "getConfigLoaderState_missing"
      };
    }

    const loaderState = loader.getConfigLoaderState();

    return {
      status: loaderState.status || "config_loader_state_available",
      isAvailable: true,
      isSafe: loaderState.isSafeLocalMode === true,
      reason: loaderState.reason || "config_loader_state_read",
      loaderState
    };
  }

  function getSupabaseConfigLoaderBootState() {
    const loader = window.ACCAOUI_SUPABASE_CONFIG_LOADER;

    if (!loader) {
      return {
        status: "config_loader_boot_state_missing",
        loadStatus: "unknown",
        isAvailable: false,
        isSafe: true,
        isAutoLoadEnabled: false,
        reason: "config_loader_not_loaded"
      };
    }

    if (typeof loader.getBootLoadState !== "function") {
      return {
        status: "config_loader_boot_state_invalid",
        loadStatus: "unknown",
        isAvailable: false,
        isSafe: true,
        isAutoLoadEnabled: false,
        reason: "getBootLoadState_missing"
      };
    }

    const bootState = loader.getBootLoadState();

    return {
      status: bootState.status || "config_loader_boot_state_available",
      loadStatus: bootState.loadStatus || "unknown",
      isAvailable: true,
      isSafe: bootState.isSafeLocalMode === true,
      isAutoLoadEnabled: bootState.isAutoLoadEnabled === true,
      reason: bootState.reason || "config_loader_boot_state_read",
      bootState
    };
  }

  function getSupabaseSafetySummary() {
    const configState = getConfigState();
    const sdkState = getSdkState();
    const clientState = getClientReadinessState();
    const authState = getAuthReadinessState();
    const participantAccessState = getParticipantAccessReadinessState();
    const participantSessionState = getParticipantSessionState();
    const participantProfileState = getParticipantProfileState();
    const participantCourseState = getParticipantCourseState();
    const participantAccessDecisionState = getParticipantAccessDecisionState();
    const loginGateState = getLoginGateState();
    const loginGateUiState = getLoginGateUiState();
    const loginFormState = getLoginFormState();
    const loginErrorState = getLoginErrorState();
    const failSafeState = getSupabaseFailSafeState();
    const configLoaderState = getSupabaseConfigLoaderState();
    const configLoaderBootState = getSupabaseConfigLoaderBootState();
    const isLiveEnabled = isSupabaseLiveEnabled();

    const blockingReasons = [];

    if (!isLiveEnabled) blockingReasons.push("live_switch_disabled");
    if (!configState.isConfigured) blockingReasons.push(configState.status);
    if (!sdkState.hasSdk) blockingReasons.push(sdkState.status);
    if (!clientState.canCreateClient) blockingReasons.push(clientState.status);
    if (!authState.canCheckSession) blockingReasons.push(authState.status);
    if (failSafeState.status) blockingReasons.push(failSafeState.status);

    return {
      version: "v26.27a",
      status: isLiveEnabled ? "supabase_live_requested_but_blocked_safe" : "supabase_local_safe",
      isSafeLocalMode: true,
      isSupabaseLive: false,
      isLiveEnabled,
      isLocalAccessAllowed: participantAccessState.isAllowed === true,
      canCreateClient: false,
      canCheckSession: false,
      canAccessParticipantData: false,
      configStatus: configState.status,
      sdkStatus: sdkState.status,
      clientStatus: clientState.status,
      authStatus: authState.status,
      participantAccessStatus: participantAccessState.status,
      participantSessionStatus: participantSessionState.status,
      isParticipantSessionRequired: participantSessionState.isSessionRequired === true,
      participantProfileStatus: participantProfileState.status,
      isParticipantProfileRequired: participantProfileState.isProfileRequired === true,
      canLoadParticipantProfile: participantProfileState.canLoadProfile === true,
      isParticipantProfileLoaded: participantProfileState.hasProfile === true,
      participantCourseStatus: participantCourseState.status,
      isParticipantCourseRequired: participantCourseState.isCourseRequired === true,
      canLoadParticipantCourse: participantCourseState.canLoadCourse === true,
      isParticipantCourseLoaded: participantCourseState.hasCourse === true,
      isParticipantCourseExpired: participantCourseState.isCourseExpired === true,
      participantAccessDecisionStatus: participantAccessDecisionState.status,
      isParticipantAccessDecisionAllowed: participantAccessDecisionState.isAllowed === true,
      isParticipantLoginRequired: participantAccessDecisionState.isLoginRequired === true,
      accessDecisionBlockingReasons: participantAccessDecisionState.blockingReasons,
      loginGateStatus: loginGateState.status,
      isLoginGateEnabled: loginGateState.isGateEnabled === true,
      isLoginRequiredByGate: loginGateState.isLoginRequired === true,
      canRenderLoginGate: loginGateState.canRenderLoginGate === true,
      canLoginGateBlockAccess: loginGateState.canBlockAccess === true,
      loginGateUiStatus: loginGateUiState.status,
      isLoginGateUiVisible: loginGateUiState.isVisible === true,
      canRenderLoginGateUi: loginGateUiState.canRender === true,
      canLoginGateUiBlockAccess: loginGateUiState.canBlockAccess === true,
      loginFormStatus: loginFormState.status,
      isLoginFormVisible: loginFormState.isVisible === true,
      canRenderLoginForm: loginFormState.canRender === true,
      canSubmitLoginForm: loginFormState.canSubmit === true,
      canValidateLoginFormInput: loginFormState.canValidateInput === true,
      canAuthenticateWithLoginForm: loginFormState.canAuthenticate === true,
      isLoginRequiredByForm: loginFormState.isLoginRequired === true,
      loginErrorStatus: loginErrorState.status,
      hasLoginError: loginErrorState.hasError === true,
      canShowLoginError: loginErrorState.canShowError === true,
      loginErrorCode: loginErrorState.errorCode,
      loginErrorMessage: loginErrorState.errorMessage,
      isLoginErrorRecoverable: loginErrorState.isRecoverable === true,
      failSafeStatus: failSafeState.status,
      configLoaderStatus: configLoaderState.status,
      configLoaderBootStatus: configLoaderBootState.status,
      configLoaderBootLoadStatus: configLoaderBootState.loadStatus,
      blockingReasons: Array.from(new Set(blockingReasons)),
      nextRequiredSteps: [
        "provide_local_config_later",
        "load_supabase_sdk_later",
        "enable_live_switch_later",
        "create_client_later",
        "check_session_later",
        "check_participant_access_later"
      ]
    };
  }

  function getAdapterHealthState() {
    const configState = getConfigState();
    const sdkState = getSdkState();
    const clientState = getClientReadinessState();
    const authState = getAuthReadinessState();
    const participantAccessState = getParticipantAccessReadinessState();
    const participantSessionState = getParticipantSessionState();
    const participantProfileState = getParticipantProfileState();
    const participantCourseState = getParticipantCourseState();
    const participantAccessDecisionState = getParticipantAccessDecisionState();
    const loginGateState = getLoginGateState();
    const loginGateUiState = getLoginGateUiState();
    const loginFormState = getLoginFormState();
    const loginErrorState = getLoginErrorState();
    const failSafeState = getSupabaseFailSafeState();
    const configLoaderState = getSupabaseConfigLoaderState();
    const configLoaderBootState = getSupabaseConfigLoaderBootState();
    const safetySummary = getSupabaseSafetySummary();

    return {
      version: "v26.27a",
      status: participantAccessState.status,
      isSupabaseLive: false,
      isLiveEnabled: isSupabaseLiveEnabled(),
      safetySummaryStatus: safetySummary.status,
      isSafeLocalMode: safetySummary.isSafeLocalMode === true,
      failSafeStatus: failSafeState.status,
      isFailSafeSafe: failSafeState.isSafe === true,
      configLoaderStatus: configLoaderState.status,
      isConfigLoaderAvailable: configLoaderState.isAvailable === true,
      configLoaderBootStatus: configLoaderBootState.status,
      configLoaderBootLoadStatus: configLoaderBootState.loadStatus,
      isConfigLoaderBootSafe: configLoaderBootState.isSafe === true,
      isConfigLoaderAutoLoadEnabled: configLoaderBootState.isAutoLoadEnabled === true,
      isLocalAccessAllowed: participantAccessState.isAllowed === true,
      hasConfig: configState.isConfigured === true,
      hasSdk: sdkState.hasSdk === true,
      canCreateClient: clientState.canCreateClient === true,
      canCheckSession: authState.canCheckSession === true,
      configState,
      sdkState,
      clientState,
      authState,
      participantAccessState,
      participantSessionState,
      participantProfileState,
      participantCourseState,
      participantAccessDecisionState,
      loginGateState,
      loginGateUiState,
      loginFormState,
      loginErrorState,
      failSafeState,
      configLoaderState,
      configLoaderBootState,
      safetySummary
    };
  }

  window.ACCAOUI_SUPABASE_ADAPTER = {
    version: "v26.27a",
    isSupabaseLiveEnabled,
    getSupabaseFailSafeState,
    getSupabaseConfigLoaderState,
    getSupabaseConfigLoaderBootState,
    getSupabaseSafetySummary,
    getConfigState,
    getSdkState,
    getClientReadinessState,
    getClientState,
    getAuthReadinessState,
    getCurrentSession,
    getParticipantSessionState,
    getParticipantProfileState,
    getParticipantCourseState,
    getParticipantAccessDecisionState,
    getLoginGateState,
    getLoginGateUiState,
    getLoginFormState,
    getLoginErrorState,
    getParticipantAccessReadinessState,
    getParticipantAccessState,
    getAdapterHealthState
  };

  console.info("Accaoui Supabase Adapter geladen:", window.ACCAOUI_SUPABASE_ADAPTER.version);
})();
