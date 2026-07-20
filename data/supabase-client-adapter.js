// Accaoui §34a Lern-App – Supabase Client Adapter
// Stand: v27.29l
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
      version: "v26.63a",
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
      version: "v26.63a",
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
      version: "v26.63a",
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
        source: "supabase-client-adapter-stub-v26.63a",
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
        source: "supabase-client-adapter-stub-v26.63a",
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
      source: "supabase-client-adapter-stub-v26.63a",
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
      version: "v26.63a",
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
      version: "v26.63a",
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
      version: "v26.63a",
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
      version: "v26.63a",
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
      version: "v26.63a",
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

  function getLoginSuccessState() {
    const loginErrorState = getLoginErrorState();

    return {
      version: "v26.63a",
      status: "local_login_success_none",
      hasSuccess: false,
      hasSession: false,
      canFinalizeLogin: false,
      canRedirectAfterLogin: false,
      redirectTarget: null,
      isLoginRequired: false,
      isLocalAccessAllowed: true,
      reason: "login_success_state_prepared_but_no_login_in_local_mode",
      futureStatuses: [
        "login_success_session_available_later",
        "login_success_redirect_ready_later",
        "login_success_profile_pending_later",
        "login_success_course_pending_later"
      ],
      loginErrorState
    };
  }

  function getLogoutState() {
    const loginSuccessState = getLoginSuccessState();

    return {
      version: "v26.63a",
      status: "local_logout_disabled",
      isAvailable: false,
      canLogout: false,
      canClearSession: false,
      hasActiveSession: false,
      isLogoutRequired: false,
      isLocalAccessAllowed: true,
      reason: "logout_state_prepared_but_disabled_in_local_mode",
      futureStatuses: [
        "logout_available_later",
        "logout_running_later",
        "logout_success_later",
        "logout_error_later"
      ],
      loginSuccessState
    };
  }

  function getParticipantDashboardAuthState() {
    const logoutState = getLogoutState();

    return {
      version: "v26.63a",
      status: "local_dashboard_auth_disabled",
      isVisible: false,
      canRender: false,
      isAuthRequired: false,
      canBlockDashboardAccess: false,
      hasActiveSession: false,
      canShowParticipantIdentity: false,
      canShowLogoutAction: false,
      isLocalDashboardAccessAllowed: true,
      reason: "dashboard_auth_state_prepared_but_disabled_in_local_mode",
      futureStatuses: [
        "dashboard_auth_visible_later",
        "dashboard_auth_session_ready_later",
        "dashboard_auth_login_required_later",
        "dashboard_auth_blocking_later",
        "dashboard_auth_error_later"
      ],
      logoutState
    };
  }

  function getParticipantDashboardCourseAccessState() {
    const participantDashboardAuthState = getParticipantDashboardAuthState();
    const participantCourseState = getParticipantCourseState();

    return {
      version: "v26.63a",
      status: "local_dashboard_course_access_allowed",
      isCourseAccessRequired: false,
      canCheckCourseAccess: false,
      canBlockCourseAccess: false,
      hasAssignedCourse: false,
      canShowCourseLock: false,
      canShowCourseAccessWarning: false,
      isLocalDashboardCourseAccessAllowed: true,
      isLocalDashboardAccessAllowed: true,
      reason: "dashboard_course_access_state_prepared_but_allowed_in_local_mode",
      futureStatuses: [
        "dashboard_course_access_check_ready_later",
        "dashboard_course_access_allowed_later",
        "dashboard_course_access_blocked_later",
        "dashboard_course_access_expired_later",
        "dashboard_course_access_error_later"
      ],
      participantDashboardAuthState,
      participantCourseState
    };
  }

  function getParticipantDashboardExpiryState() {
    const participantDashboardCourseAccessState = getParticipantDashboardCourseAccessState();

    return {
      version: "v26.63a",
      status: "local_dashboard_expiry_check_disabled",
      isExpiryCheckRequired: false,
      canCheckExpiry: false,
      canBlockOnExpiry: false,
      hasExpiryDate: false,
      expiresAt: null,
      isExpired: false,
      daysRemaining: null,
      canShowExpiryWarning: false,
      isLocalDashboardExpiryAccessAllowed: true,
      reason: "dashboard_expiry_state_prepared_but_disabled_in_local_mode",
      futureStatuses: [
        "dashboard_expiry_check_ready_later",
        "dashboard_expiry_valid_later",
        "dashboard_expiry_warning_later",
        "dashboard_expiry_expired_later",
        "dashboard_expiry_error_later"
      ],
      participantDashboardCourseAccessState
    };
  }

  function getParticipantDashboardAccessDecisionState() {
    const participantDashboardAuthState = getParticipantDashboardAuthState();
    const participantDashboardCourseAccessState = getParticipantDashboardCourseAccessState();
    const participantDashboardExpiryState = getParticipantDashboardExpiryState();

    return {
      version: "v26.63a",
      status: "local_dashboard_access_decision_allowed",
      isDecisionAvailable: true,
      isDashboardAccessAllowed: true,
      canBlockDashboardAccess: false,
      blockReason: null,
      requiredChecks: {
        auth: false,
        courseAccess: false,
        expiry: false
      },
      passedChecks: {
        auth: true,
        courseAccess: true,
        expiry: true
      },
      isLocalDashboardAccessAllowed: true,
      reason: "dashboard_access_decision_prepared_but_allowed_in_local_mode",
      futureStatuses: [
        "dashboard_access_decision_allowed_later",
        "dashboard_access_decision_blocked_auth_later",
        "dashboard_access_decision_blocked_course_later",
        "dashboard_access_decision_blocked_expiry_later",
        "dashboard_access_decision_error_later"
      ],
      participantDashboardAuthState,
      participantDashboardCourseAccessState,
      participantDashboardExpiryState
    };
  }

  function getParticipantDashboardReadinessState() {
    const participantDashboardAccessDecisionState = getParticipantDashboardAccessDecisionState();

    return {
      version: "v26.63a",
      status: "local_dashboard_readiness_ready",
      isReadinessAvailable: true,
      isReady: true,
      canRenderDashboard: true,
      canStartLocalDashboard: true,
      isLoginRequired: false,
      canBlockDashboardAccess: false,
      blockReason: null,
      requiredChecks: {
        auth: false,
        courseAccess: false,
        expiry: false,
        accessDecision: false
      },
      passedChecks: {
        auth: true,
        courseAccess: true,
        expiry: true,
        accessDecision: true
      },
      isLocalDashboardAccessAllowed: true,
      reason: "dashboard_readiness_prepared_and_ready_in_local_mode",
      futureStatuses: [
        "dashboard_readiness_ready_later",
        "dashboard_readiness_pending_auth_later",
        "dashboard_readiness_pending_course_later",
        "dashboard_readiness_blocked_later",
        "dashboard_readiness_error_later"
      ],
      participantDashboardAccessDecisionState
    };
  }

  function getParticipantDashboardStatusBadgeState() {
    const participantDashboardReadinessState = getParticipantDashboardReadinessState();

    return {
      version: "v26.63a",
      status: "local_dashboard_status_badge_hidden",
      isAvailable: true,
      isVisible: false,
      canRender: false,
      label: "Lokaler Modus",
      tone: "neutral",
      message: "Das Teilnehmer-Dashboard ist lokal vorbereitet und ohne Login-Zwang nutzbar.",
      canBlockDashboardAccess: false,
      isLoginRequired: false,
      isLocalDashboardAccessAllowed: true,
      reason: "dashboard_status_badge_state_prepared_but_hidden_in_local_mode",
      futureStatuses: [
        "dashboard_status_badge_visible_later",
        "dashboard_status_badge_ready_later",
        "dashboard_status_badge_warning_later",
        "dashboard_status_badge_blocked_later",
        "dashboard_status_badge_error_later"
      ],
      participantDashboardReadinessState
    };
  }

  function getParticipantDashboardNoticeBannerState() {
    const participantDashboardStatusBadgeState = getParticipantDashboardStatusBadgeState();

    return {
      version: "v26.63a",
      status: "local_dashboard_notice_banner_hidden",
      isAvailable: true,
      isVisible: false,
      canRender: false,
      title: "Lokaler Modus aktiv",
      message: "Das Teilnehmer-Dashboard ist vorbereitet und lokal ohne Login-Zwang nutzbar.",
      tone: "info",
      canDismiss: false,
      canBlockDashboardAccess: false,
      isLoginRequired: false,
      isLocalDashboardAccessAllowed: true,
      reason: "dashboard_notice_banner_state_prepared_but_hidden_in_local_mode",
      futureStatuses: [
        "dashboard_notice_banner_visible_later",
        "dashboard_notice_banner_info_later",
        "dashboard_notice_banner_warning_later",
        "dashboard_notice_banner_blocking_later",
        "dashboard_notice_banner_error_later"
      ],
      participantDashboardStatusBadgeState
    };
  }

  function getParticipantDashboardProfileHeaderState() {
    const participantDashboardNoticeBannerState = getParticipantDashboardNoticeBannerState();
    const participantProfileState = getParticipantProfileState();
    const participantCourseState = getParticipantCourseState();

    return {
      version: "v26.63a",
      status: "local_dashboard_profile_header_hidden",
      isAvailable: true,
      isVisible: false,
      canRender: false,
      canShowParticipantIdentity: false,
      canShowCourseInfo: false,
      displayName: null,
      participantEmail: null,
      participantNumber: null,
      courseTitle: null,
      courseStatus: null,
      canBlockDashboardAccess: false,
      isLoginRequired: false,
      isLocalDashboardAccessAllowed: true,
      reason: "dashboard_profile_header_state_prepared_but_hidden_in_local_mode",
      futureStatuses: [
        "dashboard_profile_header_visible_later",
        "dashboard_profile_header_profile_ready_later",
        "dashboard_profile_header_course_ready_later",
        "dashboard_profile_header_warning_later",
        "dashboard_profile_header_error_later"
      ],
      participantDashboardNoticeBannerState,
      participantProfileState,
      participantCourseState
    };
  }

  function getParticipantDashboardCourseCardState() {
    const participantDashboardProfileHeaderState = getParticipantDashboardProfileHeaderState();
    const participantCourseState = getParticipantCourseState();
    const participantDashboardExpiryState = getParticipantDashboardExpiryState();

    return {
      version: "v26.63a",
      status: "local_dashboard_course_card_hidden",
      isAvailable: true,
      isVisible: false,
      canRender: false,
      canShowCourseTitle: false,
      canShowCourseStatus: false,
      canShowCourseProgress: false,
      canShowExpiryInfo: false,
      courseTitle: null,
      courseStatus: null,
      progressPercent: null,
      expiresAt: null,
      canBlockDashboardAccess: false,
      isLoginRequired: false,
      isLocalDashboardAccessAllowed: true,
      reason: "dashboard_course_card_state_prepared_but_hidden_in_local_mode",
      futureStatuses: [
        "dashboard_course_card_visible_later",
        "dashboard_course_card_course_ready_later",
        "dashboard_course_card_progress_ready_later",
        "dashboard_course_card_warning_later",
        "dashboard_course_card_error_later"
      ],
      participantDashboardProfileHeaderState,
      participantCourseState,
      participantDashboardExpiryState
    };
  }

  function getParticipantDashboardProgressState() {
    const participantDashboardCourseCardState = getParticipantDashboardCourseCardState();
    const participantSessionState = getParticipantSessionState();

    return {
      version: "v26.63a",
      status: "local_dashboard_progress_hidden",
      isAvailable: true,
      isVisible: false,
      canRender: false,
      canCalculateProgress: false,
      hasProgressData: false,
      completedItems: null,
      totalItems: null,
      progressPercent: null,
      canShowProgressBar: false,
      canShowProgressText: false,
      canBlockDashboardAccess: false,
      isLoginRequired: false,
      isLocalDashboardAccessAllowed: true,
      reason: "dashboard_progress_state_prepared_but_hidden_in_local_mode",
      futureStatuses: [
        "dashboard_progress_visible_later",
        "dashboard_progress_data_ready_later",
        "dashboard_progress_empty_later",
        "dashboard_progress_warning_later",
        "dashboard_progress_error_later"
      ],
      participantDashboardCourseCardState,
      participantSessionState
    };
  }

  function getParticipantDashboardActivityListState() {
    const participantDashboardProgressState = getParticipantDashboardProgressState();
    const participantSessionState = getParticipantSessionState();

    return {
      version: "v26.63a",
      status: "local_dashboard_activity_list_hidden",
      isAvailable: true,
      isVisible: false,
      canRender: false,
      canLoadActivities: false,
      hasActivityData: false,
      activities: [],
      totalActivityCount: null,
      canShowActivityList: false,
      canShowEmptyState: false,
      canBlockDashboardAccess: false,
      isLoginRequired: false,
      isLocalDashboardAccessAllowed: true,
      reason: "dashboard_activity_list_state_prepared_but_hidden_in_local_mode",
      futureStatuses: [
        "dashboard_activity_list_visible_later",
        "dashboard_activity_list_loading_later",
        "dashboard_activity_list_ready_later",
        "dashboard_activity_list_empty_later",
        "dashboard_activity_list_error_later"
      ],
      participantDashboardProgressState,
      participantSessionState
    };
  }

  function getParticipantDashboardRecommendationsState() {
    const participantDashboardActivityListState = getParticipantDashboardActivityListState();
    const participantDashboardProgressState = getParticipantDashboardProgressState();

    return {
      version: "v26.63a",
      status: "local_dashboard_recommendations_hidden",
      isAvailable: true,
      isVisible: false,
      canRender: false,
      canLoadRecommendations: false,
      hasRecommendationData: false,
      recommendations: [],
      totalRecommendationCount: null,
      canShowRecommendationList: false,
      canShowEmptyState: false,
      canBlockDashboardAccess: false,
      isLoginRequired: false,
      isLocalDashboardAccessAllowed: true,
      reason: "dashboard_recommendations_state_prepared_but_hidden_in_local_mode",
      futureStatuses: [
        "dashboard_recommendations_visible_later",
        "dashboard_recommendations_loading_later",
        "dashboard_recommendations_ready_later",
        "dashboard_recommendations_empty_later",
        "dashboard_recommendations_error_later"
      ],
      participantDashboardActivityListState,
      participantDashboardProgressState
    };
  }

  function getParticipantDashboardExamStatusState() {
    const participantDashboardRecommendationsState = getParticipantDashboardRecommendationsState();
    const participantDashboardProgressState = getParticipantDashboardProgressState();

    return {
      version: "v26.63a",
      status: "local_dashboard_exam_status_hidden",
      isAvailable: true,
      isVisible: false,
      canRender: false,
      canLoadExamStatus: false,
      hasExamStatusData: false,
      writtenExamStatus: null,
      oralExamStatus: null,
      lastExamResult: null,
      passed: null,
      canShowWrittenExamStatus: false,
      canShowOralExamStatus: false,
      canShowLastExamResult: false,
      canBlockDashboardAccess: false,
      isLoginRequired: false,
      isLocalDashboardAccessAllowed: true,
      reason: "dashboard_exam_status_state_prepared_but_hidden_in_local_mode",
      futureStatuses: [
        "dashboard_exam_status_visible_later",
        "dashboard_exam_status_loading_later",
        "dashboard_exam_status_ready_later",
        "dashboard_exam_status_empty_later",
        "dashboard_exam_status_error_later"
      ],
      participantDashboardRecommendationsState,
      participantDashboardProgressState
    };
  }

  function getParticipantDashboardCertificateState() {
    const participantDashboardExamStatusState = getParticipantDashboardExamStatusState();
    const participantDashboardProfileHeaderState = getParticipantDashboardProfileHeaderState();

    return {
      version: "v26.63a",
      status: "local_dashboard_certificate_hidden",
      isAvailable: true,
      isVisible: false,
      canRender: false,
      canLoadCertificate: false,
      hasCertificateData: false,
      certificateStatus: null,
      certificateNumber: null,
      issuedAt: null,
      expiresAt: null,
      canShowCertificateCard: false,
      canDownloadCertificate: false,
      canBlockDashboardAccess: false,
      isLoginRequired: false,
      isLocalDashboardAccessAllowed: true,
      reason: "dashboard_certificate_state_prepared_but_hidden_in_local_mode",
      futureStatuses: [
        "dashboard_certificate_visible_later",
        "dashboard_certificate_loading_later",
        "dashboard_certificate_ready_later",
        "dashboard_certificate_not_available_later",
        "dashboard_certificate_error_later"
      ],
      participantDashboardExamStatusState,
      participantDashboardProfileHeaderState
    };
  }

  function getParticipantDashboardDocumentsState() {
    const participantDashboardCertificateState = getParticipantDashboardCertificateState();
    const participantDashboardProfileHeaderState = getParticipantDashboardProfileHeaderState();

    return {
      version: "v26.63a",
      status: "local_dashboard_documents_hidden",
      isAvailable: true,
      isVisible: false,
      canRender: false,
      canLoadDocuments: false,
      hasDocumentData: false,
      documents: [],
      totalDocumentCount: null,
      canShowDocumentList: false,
      canShowEmptyState: false,
      canDownloadDocuments: false,
      canBlockDashboardAccess: false,
      isLoginRequired: false,
      isLocalDashboardAccessAllowed: true,
      reason: "dashboard_documents_state_prepared_but_hidden_in_local_mode",
      futureStatuses: [
        "dashboard_documents_visible_later",
        "dashboard_documents_loading_later",
        "dashboard_documents_ready_later",
        "dashboard_documents_empty_later",
        "dashboard_documents_error_later"
      ],
      participantDashboardCertificateState,
      participantDashboardProfileHeaderState
    };
  }

  function getParticipantDashboardMessagesState() {
    const participantDashboardDocumentsState = getParticipantDashboardDocumentsState();
    const participantDashboardProfileHeaderState = getParticipantDashboardProfileHeaderState();

    return {
      version: "v26.63a",
      status: "local_dashboard_messages_hidden",
      isAvailable: true,
      isVisible: false,
      canRender: false,
      canLoadMessages: false,
      hasMessageData: false,
      messages: [],
      totalMessageCount: null,
      unreadMessageCount: null,
      canShowMessageList: false,
      canShowEmptyState: false,
      canSendMessage: false,
      canBlockDashboardAccess: false,
      isLoginRequired: false,
      isLocalDashboardAccessAllowed: true,
      reason: "dashboard_messages_state_prepared_but_hidden_in_local_mode",
      futureStatuses: [
        "dashboard_messages_visible_later",
        "dashboard_messages_loading_later",
        "dashboard_messages_ready_later",
        "dashboard_messages_empty_later",
        "dashboard_messages_error_later"
      ],
      participantDashboardDocumentsState,
      participantDashboardProfileHeaderState
    };
  }

  function getParticipantDashboardSupportState() {
    const participantDashboardMessagesState = getParticipantDashboardMessagesState();
    const participantDashboardProfileHeaderState = getParticipantDashboardProfileHeaderState();

    return {
      version: "v26.63a",
      status: "local_dashboard_support_hidden",
      isAvailable: true,
      isVisible: false,
      canRender: false,
      canLoadSupportOptions: false,
      hasSupportData: false,
      supportOptions: [],
      supportEmail: null,
      supportPhone: null,
      canShowSupportCard: false,
      canCreateSupportRequest: false,
      canBlockDashboardAccess: false,
      isLoginRequired: false,
      isLocalDashboardAccessAllowed: true,
      reason: "dashboard_support_state_prepared_but_hidden_in_local_mode",
      futureStatuses: [
        "dashboard_support_visible_later",
        "dashboard_support_loading_later",
        "dashboard_support_ready_later",
        "dashboard_support_empty_later",
        "dashboard_support_error_later"
      ],
      participantDashboardMessagesState,
      participantDashboardProfileHeaderState
    };
  }

  function getParticipantDashboardAppointmentsState() {
    const participantDashboardSupportState = getParticipantDashboardSupportState();
    const participantDashboardCourseCardState = getParticipantDashboardCourseCardState();

    return {
      version: "v26.63a",
      status: "local_dashboard_appointments_hidden",
      isAvailable: true,
      isVisible: false,
      canRender: false,
      canLoadAppointments: false,
      hasAppointmentData: false,
      appointments: [],
      totalAppointmentCount: null,
      nextAppointmentAt: null,
      canShowAppointmentList: false,
      canShowAppointmentCard: false,
      canBookAppointment: false,
      canCancelAppointment: false,
      canBlockDashboardAccess: false,
      isLoginRequired: false,
      isLocalDashboardAccessAllowed: true,
      reason: "dashboard_appointments_state_prepared_but_hidden_in_local_mode",
      futureStatuses: [
        "dashboard_appointments_visible_later",
        "dashboard_appointments_loading_later",
        "dashboard_appointments_ready_later",
        "dashboard_appointments_empty_later",
        "dashboard_appointments_error_later"
      ],
      participantDashboardSupportState,
      participantDashboardCourseCardState
    };
  }

  function getParticipantDashboardPaymentStatusState() {
    const participantDashboardAppointmentsState = getParticipantDashboardAppointmentsState();
    const participantDashboardCourseAccessState = getParticipantDashboardCourseAccessState();

    return {
      version: "v26.63a",
      status: "local_dashboard_payment_status_hidden",
      isAvailable: true,
      isVisible: false,
      canRender: false,
      canLoadPaymentStatus: false,
      hasPaymentData: false,
      paymentStatus: null,
      paymentPlan: null,
      outstandingAmount: null,
      currency: null,
      dueDate: null,
      canShowPaymentCard: false,
      canShowOutstandingBadge: false,
      canStartPayment: false,
      canBlockDashboardAccess: false,
      isLoginRequired: false,
      isLocalDashboardAccessAllowed: true,
      reason: "dashboard_payment_status_state_prepared_but_hidden_in_local_mode",
      futureStatuses: [
        "dashboard_payment_status_visible_later",
        "dashboard_payment_status_loading_later",
        "dashboard_payment_status_ready_later",
        "dashboard_payment_status_paid_later",
        "dashboard_payment_status_open_later",
        "dashboard_payment_status_overdue_later",
        "dashboard_payment_status_error_later"
      ],
      participantDashboardAppointmentsState,
      participantDashboardCourseAccessState
    };
  }

  function getParticipantDashboardContractStatusState() {
    const participantDashboardPaymentStatusState = getParticipantDashboardPaymentStatusState();
    const participantDashboardCourseAccessState = getParticipantDashboardCourseAccessState();

    return {
      version: "v26.63a",
      status: "local_dashboard_contract_status_hidden",
      isAvailable: true,
      isVisible: false,
      canRender: false,
      canLoadContractStatus: false,
      hasContractData: false,
      contractStatus: null,
      contractNumber: null,
      contractSignedAt: null,
      contractStartsAt: null,
      contractEndsAt: null,
      canShowContractCard: false,
      canShowSignatureStatus: false,
      canStartContractSigning: false,
      canDownloadContract: false,
      canBlockDashboardAccess: false,
      isLoginRequired: false,
      isLocalDashboardAccessAllowed: true,
      reason: "dashboard_contract_status_state_prepared_but_hidden_in_local_mode",
      futureStatuses: [
        "dashboard_contract_status_visible_later",
        "dashboard_contract_status_loading_later",
        "dashboard_contract_status_ready_later",
        "dashboard_contract_status_signed_later",
        "dashboard_contract_status_unsigned_later",
        "dashboard_contract_status_expired_later",
        "dashboard_contract_status_error_later"
      ],
      participantDashboardPaymentStatusState,
      participantDashboardCourseAccessState
    };
  }

  function getParticipantDashboardInvoicesState() {
    const participantDashboardContractStatusState = getParticipantDashboardContractStatusState();
    const participantDashboardPaymentStatusState = getParticipantDashboardPaymentStatusState();

    return {
      version: "v26.63a",
      status: "local_dashboard_invoices_hidden",
      isAvailable: true,
      isVisible: false,
      canRender: false,
      canLoadInvoices: false,
      hasInvoiceData: false,
      invoices: [],
      totalInvoiceCount: null,
      openInvoiceCount: null,
      latestInvoiceNumber: null,
      latestInvoiceIssuedAt: null,
      canShowInvoiceList: false,
      canShowInvoiceCard: false,
      canDownloadInvoice: false,
      canStartInvoicePayment: false,
      canBlockDashboardAccess: false,
      isLoginRequired: false,
      isLocalDashboardAccessAllowed: true,
      reason: "dashboard_invoices_state_prepared_but_hidden_in_local_mode",
      futureStatuses: [
        "dashboard_invoices_visible_later",
        "dashboard_invoices_loading_later",
        "dashboard_invoices_ready_later",
        "dashboard_invoices_empty_later",
        "dashboard_invoices_open_later",
        "dashboard_invoices_paid_later",
        "dashboard_invoices_error_later"
      ],
      participantDashboardContractStatusState,
      participantDashboardPaymentStatusState
    };
  }

  function getParticipantDashboardAttendanceState() {
    const participantDashboardInvoicesState = getParticipantDashboardInvoicesState();
    const participantDashboardCourseAccessState = getParticipantDashboardCourseAccessState();

    return {
      version: "v26.63a",
      status: "local_dashboard_attendance_hidden",
      isAvailable: true,
      isVisible: false,
      canRender: false,
      canLoadAttendance: false,
      hasAttendanceData: false,
      attendanceRecords: [],
      totalAttendanceCount: null,
      presentCount: null,
      absentCount: null,
      excusedAbsenceCount: null,
      attendanceRatePercent: null,
      lastAttendanceAt: null,
      canShowAttendanceList: false,
      canShowAttendanceCard: false,
      canShowAttendanceRate: false,
      canBlockDashboardAccess: false,
      isLoginRequired: false,
      isLocalDashboardAccessAllowed: true,
      reason: "dashboard_attendance_state_prepared_but_hidden_in_local_mode",
      futureStatuses: [
        "dashboard_attendance_visible_later",
        "dashboard_attendance_loading_later",
        "dashboard_attendance_ready_later",
        "dashboard_attendance_empty_later",
        "dashboard_attendance_warning_later",
        "dashboard_attendance_error_later"
      ],
      participantDashboardInvoicesState,
      participantDashboardCourseAccessState
    };
  }

  function getParticipantDashboardLessonPlanState() {
    const participantDashboardAttendanceState = getParticipantDashboardAttendanceState();
    const participantDashboardCourseAccessState = getParticipantDashboardCourseAccessState();

    return {
      version: "v26.63a",
      status: "local_dashboard_lesson_plan_hidden",
      isAvailable: true,
      isVisible: false,
      canRender: false,
      canLoadLessonPlan: false,
      hasLessonPlanData: false,
      lessons: [],
      totalLessonCount: null,
      nextLessonAt: null,
      currentTopic: null,
      currentModule: null,
      canShowLessonPlanList: false,
      canShowLessonPlanCard: false,
      canShowNextLessonHint: false,
      canBlockDashboardAccess: false,
      isLoginRequired: false,
      isLocalDashboardAccessAllowed: true,
      reason: "dashboard_lesson_plan_state_prepared_but_hidden_in_local_mode",
      futureStatuses: [
        "dashboard_lesson_plan_visible_later",
        "dashboard_lesson_plan_loading_later",
        "dashboard_lesson_plan_ready_later",
        "dashboard_lesson_plan_empty_later",
        "dashboard_lesson_plan_today_later",
        "dashboard_lesson_plan_error_later"
      ],
      participantDashboardAttendanceState,
      participantDashboardCourseAccessState
    };
  }

  function getParticipantDashboardCourseMaterialsState() {
    const participantDashboardLessonPlanState = getParticipantDashboardLessonPlanState();
    const participantDashboardCourseAccessState = getParticipantDashboardCourseAccessState();

    return {
      version: "v26.63a",
      status: "local_dashboard_course_materials_hidden",
      isAvailable: true,
      isVisible: false,
      canRender: false,
      canLoadCourseMaterials: false,
      hasCourseMaterialData: false,
      courseMaterials: [],
      totalCourseMaterialCount: null,
      latestCourseMaterialTitle: null,
      latestCourseMaterialAddedAt: null,
      canShowCourseMaterialList: false,
      canShowCourseMaterialCard: false,
      canOpenCourseMaterial: false,
      canDownloadCourseMaterial: false,
      canMarkCourseMaterialAsRead: false,
      canBlockDashboardAccess: false,
      isLoginRequired: false,
      isLocalDashboardAccessAllowed: true,
      reason: "dashboard_course_materials_state_prepared_but_hidden_in_local_mode",
      futureStatuses: [
        "dashboard_course_materials_visible_later",
        "dashboard_course_materials_loading_later",
        "dashboard_course_materials_ready_later",
        "dashboard_course_materials_empty_later",
        "dashboard_course_materials_updated_later",
        "dashboard_course_materials_error_later"
      ],
      participantDashboardLessonPlanState,
      participantDashboardCourseAccessState
    };
  }

  function getParticipantDashboardLearningProgressDetailsState() {
    const participantDashboardProgressState = getParticipantDashboardProgressState();
    const participantDashboardCourseMaterialsState = getParticipantDashboardCourseMaterialsState();

    return {
      version: "v26.63a",
      status: "local_dashboard_learning_progress_details_hidden",
      isAvailable: true,
      isVisible: false,
      canRender: false,
      canLoadLearningProgressDetails: false,
      hasLearningProgressDetailsData: false,
      learningProgressDetails: [],
      totalLearningItemCount: null,
      completedLearningItemCount: null,
      openLearningItemCount: null,
      learningProgressPercent: null,
      currentLearningTopic: null,
      lastLearningActivityAt: null,
      canShowLearningProgressDetailsList: false,
      canShowLearningProgressDetailsCard: false,
      canShowLearningProgressPercent: false,
      canShowCurrentLearningTopic: false,
      canBlockDashboardAccess: false,
      isLoginRequired: false,
      isLocalDashboardAccessAllowed: true,
      reason: "dashboard_learning_progress_details_state_prepared_but_hidden_in_local_mode",
      futureStatuses: [
        "dashboard_learning_progress_details_visible_later",
        "dashboard_learning_progress_details_loading_later",
        "dashboard_learning_progress_details_ready_later",
        "dashboard_learning_progress_details_empty_later",
        "dashboard_learning_progress_details_updated_later",
        "dashboard_learning_progress_details_error_later"
      ],
      participantDashboardProgressState,
      participantDashboardCourseMaterialsState
    };
  }

  function getParticipantDashboardMistakeTrainingDetailsState() {
    const participantDashboardLearningProgressDetailsState = getParticipantDashboardLearningProgressDetailsState();
    const participantDashboardProgressState = getParticipantDashboardProgressState();

    return {
      version: "v26.63a",
      status: "local_dashboard_mistake_training_details_hidden",
      isAvailable: true,
      isVisible: false,
      canRender: false,
      canLoadMistakeTrainingDetails: false,
      hasMistakeTrainingDetailsData: false,
      mistakeTrainingDetails: [],
      totalMistakeCount: null,
      openMistakeCount: null,
      resolvedMistakeCount: null,
      repeatedMistakeCount: null,
      latestMistakeTopic: null,
      lastMistakeTrainingAt: null,
      recommendedReviewMode: null,
      canShowMistakeTrainingDetailsList: false,
      canShowMistakeTrainingDetailsCard: false,
      canShowOpenMistakeCount: false,
      canShowRecommendedReviewMode: false,
      canStartMistakeReview: false,
      canBlockDashboardAccess: false,
      isLoginRequired: false,
      isLocalDashboardAccessAllowed: true,
      reason: "dashboard_mistake_training_details_state_prepared_but_hidden_in_local_mode",
      futureStatuses: [
        "dashboard_mistake_training_details_visible_later",
        "dashboard_mistake_training_details_loading_later",
        "dashboard_mistake_training_details_ready_later",
        "dashboard_mistake_training_details_empty_later",
        "dashboard_mistake_training_details_review_due_later",
        "dashboard_mistake_training_details_error_later"
      ],
      participantDashboardLearningProgressDetailsState,
      participantDashboardProgressState
    };
  }

  function getParticipantDashboardExamSimulationDetailsState() {
    const participantDashboardExamStatusState = getParticipantDashboardExamStatusState();
    const participantDashboardMistakeTrainingDetailsState = getParticipantDashboardMistakeTrainingDetailsState();

    return {
      version: "v26.63a",
      status: "local_dashboard_exam_simulation_details_hidden",
      isAvailable: true,
      isVisible: false,
      canRender: false,
      canLoadExamSimulationDetails: false,
      hasExamSimulationDetailsData: false,
      examSimulationDetails: [],
      totalExamSimulationCount: null,
      passedExamSimulationCount: null,
      failedExamSimulationCount: null,
      latestExamSimulationScore: null,
      latestExamSimulationPassed: null,
      latestExamSimulationAt: null,
      bestExamSimulationScore: null,
      recommendedExamSimulationMode: null,
      canShowExamSimulationDetailsList: false,
      canShowExamSimulationDetailsCard: false,
      canShowExamSimulationScore: false,
      canShowExamSimulationRecommendation: false,
      canStartExamSimulationReview: false,
      canBlockDashboardAccess: false,
      isLoginRequired: false,
      isLocalDashboardAccessAllowed: true,
      reason: "dashboard_exam_simulation_details_state_prepared_but_hidden_in_local_mode",
      futureStatuses: [
        "dashboard_exam_simulation_details_visible_later",
        "dashboard_exam_simulation_details_loading_later",
        "dashboard_exam_simulation_details_ready_later",
        "dashboard_exam_simulation_details_empty_later",
        "dashboard_exam_simulation_details_review_due_later",
        "dashboard_exam_simulation_details_error_later"
      ],
      participantDashboardExamStatusState,
      participantDashboardMistakeTrainingDetailsState
    };
  }

  function getParticipantDashboardOralExamDetailsState() {
    const participantDashboardExamSimulationDetailsState = getParticipantDashboardExamSimulationDetailsState();
    const participantDashboardCourseAccessState = getParticipantDashboardCourseAccessState();

    return {
      version: "v26.63a",
      status: "local_dashboard_oral_exam_details_hidden",
      isAvailable: true,
      isVisible: false,
      canRender: false,
      canLoadOralExamDetails: false,
      hasOralExamDetailsData: false,
      oralExamDetails: [],
      totalOralQuestionCount: null,
      practicedOralQuestionCount: null,
      openOralQuestionCount: null,
      confidentOralAnswerCount: null,
      uncertainOralAnswerCount: null,
      latestOralExamTopic: null,
      lastOralPracticeAt: null,
      recommendedOralPracticeMode: null,
      canShowOralExamDetailsList: false,
      canShowOralExamDetailsCard: false,
      canShowOpenOralQuestionCount: false,
      canShowOralPracticeRecommendation: false,
      canStartOralExamPracticeReview: false,
      canBlockDashboardAccess: false,
      isLoginRequired: false,
      isLocalDashboardAccessAllowed: true,
      reason: "dashboard_oral_exam_details_state_prepared_but_hidden_in_local_mode",
      futureStatuses: [
        "dashboard_oral_exam_details_visible_later",
        "dashboard_oral_exam_details_loading_later",
        "dashboard_oral_exam_details_ready_later",
        "dashboard_oral_exam_details_empty_later",
        "dashboard_oral_exam_details_practice_due_later",
        "dashboard_oral_exam_details_error_later"
      ],
      participantDashboardExamSimulationDetailsState,
      participantDashboardCourseAccessState
    };
  }

  function getParticipantDashboardFlashcardsDetailsState() {
    const participantDashboardOralExamDetailsState = getParticipantDashboardOralExamDetailsState();
    const participantDashboardLearningProgressDetailsState = getParticipantDashboardLearningProgressDetailsState();

    return {
      version: "v26.63a",
      status: "local_dashboard_flashcards_details_hidden",
      isAvailable: true,
      isVisible: false,
      canRender: false,
      canLoadFlashcardsDetails: false,
      hasFlashcardsDetailsData: false,
      flashcardsDetails: [],
      totalFlashcardCount: null,
      practicedFlashcardCount: null,
      masteredFlashcardCount: null,
      weakFlashcardCount: null,
      dueFlashcardCount: null,
      latestFlashcardTopic: null,
      lastFlashcardPracticeAt: null,
      recommendedFlashcardPracticeMode: null,
      canShowFlashcardsDetailsList: false,
      canShowFlashcardsDetailsCard: false,
      canShowDueFlashcardCount: false,
      canShowFlashcardPracticeRecommendation: false,
      canStartFlashcardPracticeReview: false,
      canBlockDashboardAccess: false,
      isLoginRequired: false,
      isLocalDashboardAccessAllowed: true,
      reason: "dashboard_flashcards_details_state_prepared_but_hidden_in_local_mode",
      futureStatuses: [
        "dashboard_flashcards_details_visible_later",
        "dashboard_flashcards_details_loading_later",
        "dashboard_flashcards_details_ready_later",
        "dashboard_flashcards_details_empty_later",
        "dashboard_flashcards_details_review_due_later",
        "dashboard_flashcards_details_error_later"
      ],
      participantDashboardOralExamDetailsState,
      participantDashboardLearningProgressDetailsState
    };
  }

  function getParticipantDashboardSampleQuestionsDetailsState() {
    const participantDashboardFlashcardsDetailsState = getParticipantDashboardFlashcardsDetailsState();
    const participantDashboardExamSimulationDetailsState = getParticipantDashboardExamSimulationDetailsState();

    return {
      version: "v26.63a",
      status: "local_dashboard_sample_questions_details_hidden",
      isAvailable: true,
      isVisible: false,
      canRender: false,
      canLoadSampleQuestionsDetails: false,
      hasSampleQuestionsDetailsData: false,
      sampleQuestionsDetails: [],
      totalSampleQuestionCount: null,
      practicedSampleQuestionCount: null,
      correctSampleQuestionCount: null,
      incorrectSampleQuestionCount: null,
      openSampleQuestionCount: null,
      latestSampleQuestionTopic: null,
      lastSampleQuestionPracticeAt: null,
      recommendedSampleQuestionPracticeMode: null,
      canShowSampleQuestionsDetailsList: false,
      canShowSampleQuestionsDetailsCard: false,
      canShowOpenSampleQuestionCount: false,
      canShowSampleQuestionPracticeRecommendation: false,
      canStartSampleQuestionPracticeReview: false,
      canBlockDashboardAccess: false,
      isLoginRequired: false,
      isLocalDashboardAccessAllowed: true,
      reason: "dashboard_sample_questions_details_state_prepared_but_hidden_in_local_mode",
      futureStatuses: [
        "dashboard_sample_questions_details_visible_later",
        "dashboard_sample_questions_details_loading_later",
        "dashboard_sample_questions_details_ready_later",
        "dashboard_sample_questions_details_empty_later",
        "dashboard_sample_questions_details_practice_due_later",
        "dashboard_sample_questions_details_error_later"
      ],
      participantDashboardFlashcardsDetailsState,
      participantDashboardExamSimulationDetailsState
    };
  }

  function getParticipantDashboardExamHistoryDataSourceState() {
    const rpcState = getParticipantExamResultHistoryRpcState();

    return {
      version: "v27.29c",
      status: "local_dashboard_exam_history_data_source_blocked",
      isAvailable: true,
      isPrepared: true,
      isVisible: false,
      canRender: false,
      canLoad: false,
      hasData: false,
      sourceType: "supabase_rpc",
      rpcName: rpcState.rpcName,
      normalizerName: "normalizeParticipantFullExamResultRows",
      isNormalizerPrepared: true,
      canNormalizeRows: true,
      aggregatorName: "aggregateParticipantFullExamResultRows",
      isAggregatorPrepared: true,
      canAggregateRows: true,
      responseMapperName: "mapParticipantFullExamResultHistoryResponse",
      isResponseMapperPrepared: true,
      canMapResponses: true,
      loadStateMapperName: "mapParticipantFullExamResultHistoryLoadState",
      isLoadStateMapperPrepared: true,
      canMapLoadStates: true,
      initialLoadState:
        mapParticipantFullExamResultHistoryLoadState({
          phase: "prepared"
        }),
      paginationStateMapperName:
        "mapParticipantFullExamResultHistoryPaginationState",
      isPaginationStateMapperPrepared: true,
      canMapPaginationStates: true,
      initialPaginationState:
        mapParticipantFullExamResultHistoryPaginationState({
          limit: rpcState.defaultLimit,
          offset: 0,
          totalCount: null,
          pageEntryCount: 0
        }),
      dataSourceOrchestratorName:
        "orchestrateParticipantFullExamResultHistoryDataSourceState",
      isDataSourceOrchestratorPrepared: true,
      canOrchestrateDataSourceStates: true,
      initialOrchestratedState:
        orchestrateParticipantFullExamResultHistoryDataSourceState({
          phase: "prepared",
          limit: rpcState.defaultLimit,
          offset: 0
        }),
      navigationIntentMapperName:
        "mapParticipantFullExamResultHistoryNavigationIntent",
      isNavigationIntentMapperPrepared: true,
      canMapNavigationIntents: true,
      initialNavigationIntentState:
        mapParticipantFullExamResultHistoryNavigationIntent({
          intent: "first",
          currentState:
            orchestrateParticipantFullExamResultHistoryDataSourceState({
              phase: "prepared",
              limit: rpcState.defaultLimit,
              offset: 0
            })
        }),
      normalizedEntries: [],
      aggregate: null,
      mappedResponse: null,
      normalizationError: null,
      responseMappingError: null,
      request: {
        limit: rpcState.defaultLimit,
        offset: 0
      },
      entries: [],
      totalCount: null,
      isLiveCall: false,
      isBlockedSafely: true,
      isLoginRequired: false,
      isLocalAccessAllowed: true,
      reason: "exam_result_history_rpc_prepared_but_local_mode_blocks_loading",
      futureStatuses: [
        "dashboard_exam_history_data_source_ready_later",
        "dashboard_exam_history_data_source_loading_later",
        "dashboard_exam_history_data_source_success_later",
        "dashboard_exam_history_data_source_empty_later",
        "dashboard_exam_history_data_source_error_later"
      ],
      rpcState
    };
  }

  function getParticipantDashboardExamHistoryState() {
    const participantDashboardSampleQuestionsDetailsState = getParticipantDashboardSampleQuestionsDetailsState();
    const participantDashboardExamSimulationDetailsState = getParticipantDashboardExamSimulationDetailsState();
    const participantDashboardExamHistoryDataSourceState = getParticipantDashboardExamHistoryDataSourceState();

    return {
      version: "v26.63a",
      status: "local_dashboard_exam_history_hidden",
      isAvailable: true,
      isVisible: false,
      canRender: false,
      canLoadExamHistory: false,
      hasExamHistoryData: false,
      examHistoryEntries: [],
      dataSourceStatus: participantDashboardExamHistoryDataSourceState.status,
      dataSourceType: participantDashboardExamHistoryDataSourceState.sourceType,
      dataSourceRpcName: participantDashboardExamHistoryDataSourceState.rpcName,
      dataSourceNormalizerName: participantDashboardExamHistoryDataSourceState.normalizerName,
      isDataSourceNormalizerPrepared: participantDashboardExamHistoryDataSourceState.isNormalizerPrepared === true,
      canNormalizeDataSourceRows: participantDashboardExamHistoryDataSourceState.canNormalizeRows === true,
      dataSourceAggregatorName: participantDashboardExamHistoryDataSourceState.aggregatorName,
      isDataSourceAggregatorPrepared: participantDashboardExamHistoryDataSourceState.isAggregatorPrepared === true,
      canAggregateDataSourceRows: participantDashboardExamHistoryDataSourceState.canAggregateRows === true,
      dataSourceResponseMapperName: participantDashboardExamHistoryDataSourceState.responseMapperName,
      isDataSourceResponseMapperPrepared: participantDashboardExamHistoryDataSourceState.isResponseMapperPrepared === true,
      canMapDataSourceResponses: participantDashboardExamHistoryDataSourceState.canMapResponses === true,
      dataSourceLoadStateMapperName: participantDashboardExamHistoryDataSourceState.loadStateMapperName,
      isDataSourceLoadStateMapperPrepared: participantDashboardExamHistoryDataSourceState.isLoadStateMapperPrepared === true,
      canMapDataSourceLoadStates: participantDashboardExamHistoryDataSourceState.canMapLoadStates === true,
      dataSourceInitialLoadState: participantDashboardExamHistoryDataSourceState.initialLoadState,
      dataSourcePaginationStateMapperName: participantDashboardExamHistoryDataSourceState.paginationStateMapperName,
      isDataSourcePaginationStateMapperPrepared: participantDashboardExamHistoryDataSourceState.isPaginationStateMapperPrepared === true,
      canMapDataSourcePaginationStates: participantDashboardExamHistoryDataSourceState.canMapPaginationStates === true,
      dataSourceInitialPaginationState: participantDashboardExamHistoryDataSourceState.initialPaginationState,
      dataSourceOrchestratorName: participantDashboardExamHistoryDataSourceState.dataSourceOrchestratorName,
      isDataSourceOrchestratorPrepared: participantDashboardExamHistoryDataSourceState.isDataSourceOrchestratorPrepared === true,
      canOrchestrateDataSourceStates: participantDashboardExamHistoryDataSourceState.canOrchestrateDataSourceStates === true,
      dataSourceInitialOrchestratedState: participantDashboardExamHistoryDataSourceState.initialOrchestratedState,
      dataSourceNavigationIntentMapperName: participantDashboardExamHistoryDataSourceState.navigationIntentMapperName,
      isDataSourceNavigationIntentMapperPrepared: participantDashboardExamHistoryDataSourceState.isNavigationIntentMapperPrepared === true,
      canMapDataSourceNavigationIntents: participantDashboardExamHistoryDataSourceState.canMapNavigationIntents === true,
      dataSourceInitialNavigationIntentState: participantDashboardExamHistoryDataSourceState.initialNavigationIntentState,
      dataSourceMetricsScope: "page_only",
      dataSourceRequest: participantDashboardExamHistoryDataSourceState.request,
      isDataSourcePrepared: participantDashboardExamHistoryDataSourceState.isPrepared === true,
      canLoadFromDataSource: participantDashboardExamHistoryDataSourceState.canLoad === true,
      isDataSourceBlockedSafely: participantDashboardExamHistoryDataSourceState.isBlockedSafely === true,
      totalExamHistoryCount: null,
      passedExamHistoryCount: null,
      failedExamHistoryCount: null,
      latestExamHistoryScore: null,
      latestExamHistoryPassed: null,
      latestExamHistoryAt: null,
      bestExamHistoryScore: null,
      averageExamHistoryScore: null,
      recommendedExamHistoryAction: null,
      canShowExamHistoryList: false,
      canShowExamHistoryCard: false,
      canShowExamHistoryScoreTrend: false,
      canShowExamHistoryBestScore: false,
      canOpenExamHistoryAttemptReview: false,
      canBlockDashboardAccess: false,
      isLoginRequired: false,
      isLocalDashboardAccessAllowed: true,
      reason: "dashboard_exam_history_state_prepared_but_hidden_in_local_mode",
      futureStatuses: [
        "dashboard_exam_history_visible_later",
        "dashboard_exam_history_loading_later",
        "dashboard_exam_history_ready_later",
        "dashboard_exam_history_empty_later",
        "dashboard_exam_history_review_due_later",
        "dashboard_exam_history_error_later"
      ],
      participantDashboardSampleQuestionsDetailsState,
      participantDashboardExamSimulationDetailsState,
      participantDashboardExamHistoryDataSourceState
    };
  }

  function getParticipantExamResultHistoryRpcState() {
    const clientState = getClientReadinessState();
    const authState = getAuthReadinessState();
    const participantSessionState = getParticipantSessionState();

    return {
      version: "v27.29b",
      status: "exam_result_history_rpc_prepared_local_blocked",
      isAvailable: true,
      isRpcPrepared: true,
      rpcName: "accaoui_list_full_exam_results",
      rpcParameterNames: ["p_limit", "p_offset"],
      defaultLimit: 20,
      maxLimit: 50,
      maxOffset: 10000,
      canCallRpc: false,
      isLiveCallImplemented: false,
      isBlockedSafely: true,
      isLoginRequired: false,
      isLocalAccessAllowed: true,
      reason: "supabase_client_not_ready_live_call_disabled",
      futureStatuses: [
        "exam_result_history_rpc_ready_later",
        "exam_result_history_rpc_loading_later",
        "exam_result_history_rpc_success_later",
        "exam_result_history_rpc_empty_later",
        "exam_result_history_rpc_error_later"
      ],
      clientState,
      authState,
      participantSessionState
    };
  }

  function normalizeParticipantFullExamResultRow(row) {
    const invalid = (reason) => ({
      version: "v27.29d",
      isValid: false,
      entry: null,
      reason
    });

    if (
      !row ||
      typeof row !== "object" ||
      Array.isArray(row)
    ) {
      return invalid("result_row_must_be_object");
    }

    const uuidPattern =
      /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;

    const examAttemptId =
      typeof row.exam_attempt_id === "string"
        ? row.exam_attempt_id.trim()
        : "";

    const courseId =
      row.course_id === null
        ? null
        : typeof row.course_id === "string"
          ? row.course_id.trim()
          : "";

    const courseTitle =
      row.course_title === null
        ? null
        : typeof row.course_title === "string"
          ? row.course_title.trim()
          : "";

    const scorePoints = row.score_points;
    const maxPoints = row.max_points;
    const passed = row.passed;

    const startedAt =
      typeof row.started_at === "string"
        ? row.started_at.trim()
        : "";

    const finishedAt =
      typeof row.finished_at === "string"
        ? row.finished_at.trim()
        : "";

    const rawTotalCount = row.total_count;

    const totalCount =
      typeof rawTotalCount === "string" &&
      /^[0-9]+$/.test(rawTotalCount.trim())
        ? Number(rawTotalCount.trim())
        : rawTotalCount;

    if (!uuidPattern.test(examAttemptId)) {
      return invalid("exam_attempt_id_invalid");
    }

    if (
      courseId !== null &&
      !uuidPattern.test(courseId)
    ) {
      return invalid("course_id_invalid");
    }

    if (
      courseTitle !== null &&
      (
        courseTitle.length < 1 ||
        courseTitle.length > 300
      )
    ) {
      return invalid("course_title_invalid");
    }

    if (
      !Number.isInteger(scorePoints) ||
      scorePoints < 0 ||
      scorePoints > 120
    ) {
      return invalid("score_points_invalid");
    }

    if (maxPoints !== 120) {
      return invalid("max_points_must_equal_120");
    }

    if (
      typeof passed !== "boolean" ||
      passed !== (scorePoints >= 60)
    ) {
      return invalid("passed_status_invalid");
    }

    const startedAtMs = Date.parse(startedAt);
    const finishedAtMs = Date.parse(finishedAt);

    if (
      !startedAt ||
      Number.isNaN(startedAtMs)
    ) {
      return invalid("started_at_invalid");
    }

    if (
      !finishedAt ||
      Number.isNaN(finishedAtMs)
    ) {
      return invalid("finished_at_invalid");
    }

    if (finishedAtMs < startedAtMs) {
      return invalid("finished_at_before_started_at");
    }

    if (
      !Number.isSafeInteger(totalCount) ||
      totalCount < 1
    ) {
      return invalid("total_count_invalid");
    }

    return {
      version: "v27.29d",
      isValid: true,
      entry: {
        examAttemptId,
        courseId,
        courseTitle,
        scorePoints,
        maxPoints,
        passed,
        startedAt,
        finishedAt,
        totalCount
      },
      reason: null
    };
  }

  function normalizeParticipantFullExamResultRows(rows) {
    const invalid = (
      reason,
      invalidIndex = null
    ) => ({
      version: "v27.29d",
      isValid: false,
      isEmpty: false,
      entries: [],
      totalCount: null,
      invalidIndex,
      reason
    });

    if (!Array.isArray(rows)) {
      return invalid("result_rows_must_be_array");
    }

    if (rows.length === 0) {
      return {
        version: "v27.29d",
        isValid: true,
        isEmpty: true,
        entries: [],
        totalCount: null,
        invalidIndex: null,
        reason: null
      };
    }

    const entries = [];
    const seenAttemptIds = new Set();
    let expectedTotalCount = null;

    for (let index = 0; index < rows.length; index += 1) {
      const normalized =
        normalizeParticipantFullExamResultRow(rows[index]);

      if (!normalized.isValid) {
        return invalid(normalized.reason, index);
      }

      const entry = normalized.entry;

      if (seenAttemptIds.has(entry.examAttemptId)) {
        return invalid(
          "duplicate_exam_attempt_id",
          index
        );
      }

      seenAttemptIds.add(entry.examAttemptId);

      if (expectedTotalCount === null) {
        expectedTotalCount = entry.totalCount;
      } else if (
        entry.totalCount !== expectedTotalCount
      ) {
        return invalid(
          "total_count_inconsistent",
          index
        );
      }

      entries.push(entry);
    }

    if (expectedTotalCount < entries.length) {
      return invalid("total_count_smaller_than_rows");
    }

    return {
      version: "v27.29d",
      isValid: true,
      isEmpty: false,
      entries,
      totalCount: expectedTotalCount,
      invalidIndex: null,
      reason: null
    };
  }

  function aggregateParticipantFullExamResultRows(rows) {
    const normalized =
      normalizeParticipantFullExamResultRows(rows);

    if (!normalized.isValid) {
      return {
        version: "v27.29e",
        isValid: false,
        isEmpty: false,
        metricsScope: "page_only",
        entries: [],
        totalCount: null,
        pageEntryCount: 0,
        pagePassedCount: 0,
        pageFailedCount: 0,
        pageBestScore: null,
        pageAverageScore: null,
        pagePassRatePercent: null,
        pageLatestFinishedAt: null,
        pageLatestExamAttemptId: null,
        canPopulateGlobalOutcomeCounts: false,
        globalPassedCount: null,
        globalFailedCount: null,
        invalidIndex: normalized.invalidIndex,
        reason: normalized.reason
      };
    }

    if (normalized.isEmpty) {
      return {
        version: "v27.29e",
        isValid: true,
        isEmpty: true,
        metricsScope: "page_only",
        entries: [],
        totalCount: null,
        pageEntryCount: 0,
        pagePassedCount: 0,
        pageFailedCount: 0,
        pageBestScore: null,
        pageAverageScore: null,
        pagePassRatePercent: null,
        pageLatestFinishedAt: null,
        pageLatestExamAttemptId: null,
        canPopulateGlobalOutcomeCounts: false,
        globalPassedCount: null,
        globalFailedCount: null,
        invalidIndex: null,
        reason: null
      };
    }

    let pagePassedCount = 0;
    let pageFailedCount = 0;
    let scoreSum = 0;
    let pageBestScore = null;
    let latestEntry = null;

    for (const entry of normalized.entries) {
      if (entry.passed) {
        pagePassedCount += 1;
      } else {
        pageFailedCount += 1;
      }

      scoreSum += entry.scorePoints;

      if (
        pageBestScore === null ||
        entry.scorePoints > pageBestScore
      ) {
        pageBestScore = entry.scorePoints;
      }

      if (
        latestEntry === null ||
        Date.parse(entry.finishedAt) >
          Date.parse(latestEntry.finishedAt) ||
        (
          Date.parse(entry.finishedAt) ===
            Date.parse(latestEntry.finishedAt) &&
          entry.examAttemptId >
            latestEntry.examAttemptId
        )
      ) {
        latestEntry = entry;
      }
    }

    const pageEntryCount = normalized.entries.length;

    if (
      pagePassedCount + pageFailedCount !==
      pageEntryCount
    ) {
      return {
        version: "v27.29e",
        isValid: false,
        isEmpty: false,
        metricsScope: "page_only",
        entries: [],
        totalCount: null,
        pageEntryCount: 0,
        pagePassedCount: 0,
        pageFailedCount: 0,
        pageBestScore: null,
        pageAverageScore: null,
        pagePassRatePercent: null,
        pageLatestFinishedAt: null,
        pageLatestExamAttemptId: null,
        canPopulateGlobalOutcomeCounts: false,
        globalPassedCount: null,
        globalFailedCount: null,
        invalidIndex: null,
        reason: "page_outcome_counts_inconsistent"
      };
    }

    return {
      version: "v27.29e",
      isValid: true,
      isEmpty: false,
      metricsScope: "page_only",
      entries: normalized.entries,
      totalCount: normalized.totalCount,
      pageEntryCount,
      pagePassedCount,
      pageFailedCount,
      pageBestScore,
      pageAverageScore: Number(
        (scoreSum / pageEntryCount).toFixed(2)
      ),
      pagePassRatePercent: Number(
        (
          pagePassedCount /
          pageEntryCount *
          100
        ).toFixed(2)
      ),
      pageLatestFinishedAt: latestEntry.finishedAt,
      pageLatestExamAttemptId:
        latestEntry.examAttemptId,
      canPopulateGlobalOutcomeCounts: false,
      globalPassedCount: null,
      globalFailedCount: null,
      invalidIndex: null,
      reason: null
    };
  }

  function mapParticipantFullExamResultHistoryResponse(response) {
    const invalid = (
      status,
      reason,
      invalidIndex = null
    ) => ({
      version: "v27.29h",
      status,
      ok: false,
      isEmpty: false,
      isMapperOnly: true,
      isLiveCall: false,
      results: [],
      totalCount: null,
      pageMetrics: null,
      invalidIndex,
      reason
    });

    if (
      !response ||
      typeof response !== "object" ||
      Array.isArray(response)
    ) {
      return invalid(
        "exam_result_history_response_invalid",
        "rpc_response_must_be_object"
      );
    }

    if (
      response.error !== null &&
      response.error !== undefined
    ) {
      return invalid(
        "exam_result_history_response_error",
        "rpc_response_error"
      );
    }

    if (!Array.isArray(response.data)) {
      return invalid(
        "exam_result_history_response_invalid",
        "rpc_response_data_must_be_array"
      );
    }

    const aggregate =
      aggregateParticipantFullExamResultRows(
        response.data
      );

    if (!aggregate.isValid) {
      return invalid(
        "exam_result_history_response_invalid",
        aggregate.reason,
        aggregate.invalidIndex
      );
    }

    const pageMetrics = {
      metricsScope: aggregate.metricsScope,
      pageEntryCount: aggregate.pageEntryCount,
      pagePassedCount: aggregate.pagePassedCount,
      pageFailedCount: aggregate.pageFailedCount,
      pageBestScore: aggregate.pageBestScore,
      pageAverageScore: aggregate.pageAverageScore,
      pagePassRatePercent:
        aggregate.pagePassRatePercent,
      pageLatestFinishedAt:
        aggregate.pageLatestFinishedAt,
      pageLatestExamAttemptId:
        aggregate.pageLatestExamAttemptId,
      canPopulateGlobalOutcomeCounts: false,
      globalPassedCount: null,
      globalFailedCount: null
    };

    if (aggregate.isEmpty) {
      return {
        version: "v27.29h",
        status: "exam_result_history_response_empty",
        ok: true,
        isEmpty: true,
        isMapperOnly: true,
        isLiveCall: false,
        results: [],
        totalCount: null,
        pageMetrics,
        invalidIndex: null,
        reason: null
      };
    }

    return {
      version: "v27.29h",
      status: "exam_result_history_response_ready",
      ok: true,
      isEmpty: false,
      isMapperOnly: true,
      isLiveCall: false,
      results: aggregate.entries,
      totalCount: aggregate.totalCount,
      pageMetrics,
      invalidIndex: null,
      reason: null
    };
  }

  function mapParticipantFullExamResultHistoryLoadState(input) {
    const source =
      input &&
      typeof input === "object" &&
      !Array.isArray(input)
        ? input
        : {};

    const phase =
      typeof source.phase === "string"
        ? source.phase.trim()
        : "prepared";

    const createState = (overrides) => ({
      version: "v27.29i",
      status: "exam_result_history_load_prepared",
      phase,
      isLoadStateMapperOnly: true,
      isLiveCall: false,
      isPrepared: true,
      isLoading: false,
      isSuccess: false,
      isEmpty: false,
      hasError: false,
      canRetry: false,
      results: [],
      totalCount: null,
      pageMetrics: null,
      mappedResponseStatus: null,
      invalidIndex: null,
      reason: null,
      ...overrides
    });

    if (phase === "prepared") {
      return createState({
        status: "exam_result_history_load_prepared"
      });
    }

    if (phase === "loading") {
      return createState({
        status: "exam_result_history_load_loading",
        isLoading: true
      });
    }

    if (phase === "resolved") {
      const mappedResponse =
        mapParticipantFullExamResultHistoryResponse(
          source.response
        );

      if (
        mappedResponse.ok === true &&
        mappedResponse.isEmpty === true
      ) {
        return createState({
          status: "exam_result_history_load_empty",
          isSuccess: true,
          isEmpty: true,
          results: [],
          totalCount: mappedResponse.totalCount,
          pageMetrics: mappedResponse.pageMetrics,
          mappedResponseStatus:
            mappedResponse.status
        });
      }

      if (mappedResponse.ok === true) {
        return createState({
          status: "exam_result_history_load_success",
          isSuccess: true,
          results: mappedResponse.results,
          totalCount: mappedResponse.totalCount,
          pageMetrics: mappedResponse.pageMetrics,
          mappedResponseStatus:
            mappedResponse.status
        });
      }

      return createState({
        status: "exam_result_history_load_error",
        hasError: true,
        canRetry: true,
        mappedResponseStatus:
          mappedResponse.status,
        invalidIndex:
          mappedResponse.invalidIndex,
        reason:
          mappedResponse.reason
      });
    }

    if (phase === "rejected") {
      return createState({
        status: "exam_result_history_load_error",
        hasError: true,
        canRetry: true,
        reason: "rpc_request_failed"
      });
    }

    return createState({
      status: "exam_result_history_load_error",
      hasError: true,
      canRetry: false,
      reason: "load_phase_invalid"
    });
  }

  function mapParticipantFullExamResultHistoryPaginationState(input) {
    const source =
      input &&
      typeof input === "object" &&
      !Array.isArray(input)
        ? input
        : {};

    const pagination =
      normalizeParticipantExamResultHistoryPagination({
        limit: source.limit,
        offset: source.offset
      });

    const invalid = (reason) => ({
      version: "v27.29j",
      status: "exam_result_history_pagination_invalid",
      isValid: false,
      isPaginationStateMapperOnly: true,
      isLiveCall: false,
      limit: pagination.limit,
      offset: pagination.offset,
      totalCount: null,
      pageEntryCount: 0,
      currentPage: null,
      totalPages: null,
      isFirstPage: false,
      isLastPage: false,
      canGoPrevious: false,
      canGoNext: false,
      previousOffset: null,
      nextOffset: null,
      isTotalCountKnown: false,
      isNavigationCapped: false,
      reason
    });

    if (!pagination.isValid) {
      return invalid(
        !pagination.isLimitValid
          ? "limit_must_be_integer_between_1_and_50"
          : "offset_must_be_integer_between_0_and_10000"
      );
    }

    if (
      pagination.offset %
      pagination.limit !== 0
    ) {
      return invalid(
        "offset_must_align_to_limit"
      );
    }

    const totalCount =
      source.totalCount === null ||
      source.totalCount === undefined
        ? null
        : source.totalCount;

    const pageEntryCount =
      source.pageEntryCount === undefined
        ? 0
        : source.pageEntryCount;

    if (
      !Number.isInteger(pageEntryCount) ||
      pageEntryCount < 0 ||
      pageEntryCount > pagination.limit
    ) {
      return invalid(
        "page_entry_count_invalid"
      );
    }

    const previousOffset =
      pagination.offset > 0
        ? Math.max(
            0,
            pagination.offset - pagination.limit
          )
        : null;

    const currentPage =
      Math.floor(
        pagination.offset / pagination.limit
      ) + 1;

    if (totalCount === null) {
      return {
        version: "v27.29j",
        status: "exam_result_history_pagination_prepared",
        isValid: true,
        isPaginationStateMapperOnly: true,
        isLiveCall: false,
        limit: pagination.limit,
        offset: pagination.offset,
        totalCount: null,
        pageEntryCount,
        currentPage,
        totalPages: null,
        isFirstPage: pagination.offset === 0,
        isLastPage: false,
        canGoPrevious: pagination.offset > 0,
        canGoNext: false,
        previousOffset,
        nextOffset: null,
        isTotalCountKnown: false,
        isNavigationCapped: false,
        reason: "total_count_not_loaded"
      };
    }

    if (
      !Number.isSafeInteger(totalCount) ||
      totalCount < 0
    ) {
      return invalid(
        "total_count_invalid"
      );
    }

    if (totalCount === 0) {
      if (
        pagination.offset !== 0 ||
        pageEntryCount !== 0
      ) {
        return invalid(
          "empty_result_pagination_invalid"
        );
      }

      return {
        version: "v27.29j",
        status: "exam_result_history_pagination_empty",
        isValid: true,
        isPaginationStateMapperOnly: true,
        isLiveCall: false,
        limit: pagination.limit,
        offset: 0,
        totalCount: 0,
        pageEntryCount: 0,
        currentPage: 0,
        totalPages: 0,
        isFirstPage: true,
        isLastPage: true,
        canGoPrevious: false,
        canGoNext: false,
        previousOffset: null,
        nextOffset: null,
        isTotalCountKnown: true,
        isNavigationCapped: false,
        reason: null
      };
    }

    if (pagination.offset >= totalCount) {
      return invalid(
        "offset_out_of_range_for_total_count"
      );
    }

    const maximumPageEntryCount =
      Math.min(
        pagination.limit,
        totalCount - pagination.offset
      );

    if (
      pageEntryCount < 1 ||
      pageEntryCount > maximumPageEntryCount
    ) {
      return invalid(
        "page_entry_count_invalid_for_total_count"
      );
    }

    const totalPages =
      Math.ceil(
        totalCount / pagination.limit
      );

    const hasMoreEntries =
      pagination.offset + pageEntryCount <
      totalCount;

    const rawNextOffset =
      pagination.offset + pagination.limit;

    const isNavigationCapped =
      hasMoreEntries &&
      rawNextOffset > 10000;

    const canGoNext =
      hasMoreEntries &&
      !isNavigationCapped;

    return {
      version: "v27.29j",
      status: "exam_result_history_pagination_ready",
      isValid: true,
      isPaginationStateMapperOnly: true,
      isLiveCall: false,
      limit: pagination.limit,
      offset: pagination.offset,
      totalCount,
      pageEntryCount,
      currentPage,
      totalPages,
      isFirstPage: pagination.offset === 0,
      isLastPage: !hasMoreEntries,
      canGoPrevious: pagination.offset > 0,
      canGoNext,
      previousOffset,
      nextOffset:
        canGoNext
          ? rawNextOffset
          : null,
      isTotalCountKnown: true,
      isNavigationCapped,
      reason:
        isNavigationCapped
          ? "maximum_offset_reached"
          : null
    };
  }

  function orchestrateParticipantFullExamResultHistoryDataSourceState(input) {
    const source =
      input &&
      typeof input === "object" &&
      !Array.isArray(input)
        ? input
        : {};

    const phase =
      typeof source.phase === "string"
        ? source.phase.trim()
        : "prepared";

    const requestPaginationState =
      mapParticipantFullExamResultHistoryPaginationState({
        limit: source.limit,
        offset: source.offset,
        totalCount: null,
        pageEntryCount: 0
      });

    const createState = (overrides) => ({
      version: "v27.29k",
      status: "exam_result_history_data_source_prepared",
      phase,
      isDataSourceOrchestratorOnly: true,
      isLiveCall: false,
      isVisible: false,
      canRender: false,
      isPrepared: true,
      isLoading: false,
      isSuccess: false,
      isEmpty: false,
      hasError: false,
      hasData: false,
      canRetry: false,
      request: {
        limit: requestPaginationState.limit,
        offset: requestPaginationState.offset
      },
      loadState: null,
      paginationState: requestPaginationState,
      results: [],
      totalCount: null,
      pageMetrics: null,
      reason: null,
      ...overrides
    });

    if (!requestPaginationState.isValid) {
      return createState({
        status: "exam_result_history_data_source_error",
        hasError: true,
        canRetry: false,
        reason: requestPaginationState.reason
      });
    }

    const loadState =
      mapParticipantFullExamResultHistoryLoadState({
        phase,
        response: source.response
      });

    if (loadState.hasError) {
      return createState({
        status: "exam_result_history_data_source_error",
        hasError: true,
        canRetry: loadState.canRetry,
        loadState,
        reason: loadState.reason
      });
    }

    if (loadState.isLoading) {
      return createState({
        status: "exam_result_history_data_source_loading",
        isLoading: true,
        loadState
      });
    }

    if (
      loadState.status ===
      "exam_result_history_load_prepared"
    ) {
      return createState({
        status: "exam_result_history_data_source_prepared",
        loadState
      });
    }

    if (loadState.isEmpty) {
      if (requestPaginationState.offset !== 0) {
        return createState({
          status: "exam_result_history_data_source_error",
          hasError: true,
          canRetry: true,
          loadState,
          reason: "empty_page_after_nonzero_offset"
        });
      }

      const paginationState =
        mapParticipantFullExamResultHistoryPaginationState({
          limit: requestPaginationState.limit,
          offset: 0,
          totalCount: 0,
          pageEntryCount: 0
        });

      if (!paginationState.isValid) {
        return createState({
          status: "exam_result_history_data_source_error",
          hasError: true,
          canRetry: false,
          loadState,
          paginationState,
          reason: paginationState.reason
        });
      }

      return createState({
        status: "exam_result_history_data_source_empty",
        isSuccess: true,
        isEmpty: true,
        loadState,
        paginationState,
        results: [],
        totalCount: 0,
        pageMetrics: loadState.pageMetrics
      });
    }

    if (loadState.isSuccess) {
      const pageEntryCount =
        loadState.pageMetrics &&
        Number.isInteger(
          loadState.pageMetrics.pageEntryCount
        )
          ? loadState.pageMetrics.pageEntryCount
          : null;

      if (
        pageEntryCount === null ||
        pageEntryCount !==
          loadState.results.length
      ) {
        return createState({
          status: "exam_result_history_data_source_error",
          hasError: true,
          canRetry: false,
          loadState,
          reason: "page_metrics_entry_count_invalid"
        });
      }

      const paginationState =
        mapParticipantFullExamResultHistoryPaginationState({
          limit: requestPaginationState.limit,
          offset: requestPaginationState.offset,
          totalCount: loadState.totalCount,
          pageEntryCount
        });

      if (!paginationState.isValid) {
        return createState({
          status: "exam_result_history_data_source_error",
          hasError: true,
          canRetry: false,
          loadState,
          paginationState,
          reason: paginationState.reason
        });
      }

      return createState({
        status: "exam_result_history_data_source_success",
        isSuccess: true,
        hasData: loadState.results.length > 0,
        loadState,
        paginationState,
        results: loadState.results,
        totalCount: loadState.totalCount,
        pageMetrics: loadState.pageMetrics
      });
    }

    return createState({
      status: "exam_result_history_data_source_error",
      hasError: true,
      canRetry: false,
      loadState,
      reason: "load_state_unhandled"
    });
  }

  function mapParticipantFullExamResultHistoryNavigationIntent(input) {
    const source =
      input &&
      typeof input === "object" &&
      !Array.isArray(input)
        ? input
        : {};

    const intent =
      typeof source.intent === "string"
        ? source.intent.trim()
        : "";

    const allowedIntents = [
      "first",
      "previous",
      "next",
      "retry"
    ];

    const invalid = (reason) => ({
      version: "v27.29l",
      status: "exam_result_history_navigation_intent_invalid",
      intent,
      isValid: false,
      isNavigationIntentMapperOnly: true,
      isLiveCall: false,
      canNavigate: false,
      isRetry: false,
      isSameRequest: false,
      sourceStatus: null,
      request: null,
      reason
    });

    if (!allowedIntents.includes(intent)) {
      return invalid("navigation_intent_invalid");
    }

    const currentState =
      source.currentState &&
      typeof source.currentState === "object" &&
      !Array.isArray(source.currentState)
        ? source.currentState
        : null;

    if (!currentState) {
      return invalid("current_state_must_be_object");
    }

    const currentRequest =
      currentState.request &&
      typeof currentState.request === "object" &&
      !Array.isArray(currentState.request)
        ? currentState.request
        : null;

    if (!currentRequest) {
      return invalid("current_request_missing");
    }

    const normalizedRequest =
      normalizeParticipantExamResultHistoryPagination({
        limit: currentRequest.limit,
        offset: currentRequest.offset
      });

    if (
      !normalizedRequest.isValid ||
      normalizedRequest.offset %
        normalizedRequest.limit !== 0
    ) {
      return invalid("current_request_invalid");
    }

    const sourceStatus =
      typeof currentState.status === "string"
        ? currentState.status
        : null;

    const createState = (overrides) => ({
      version: "v27.29l",
      status: "exam_result_history_navigation_intent_blocked",
      intent,
      isValid: true,
      isNavigationIntentMapperOnly: true,
      isLiveCall: false,
      canNavigate: false,
      isRetry: false,
      isSameRequest: false,
      sourceStatus,
      request: null,
      reason: null,
      ...overrides
    });

    const ready = (targetOffset, overrides = {}) => {
      const targetRequest =
        normalizeParticipantExamResultHistoryPagination({
          limit: normalizedRequest.limit,
          offset: targetOffset
        });

      if (
        !targetRequest.isValid ||
        targetRequest.offset %
          targetRequest.limit !== 0
      ) {
        return invalid("navigation_target_invalid");
      }

      return createState({
        status: "exam_result_history_navigation_intent_ready",
        canNavigate: true,
        isSameRequest:
          targetRequest.offset ===
          normalizedRequest.offset,
        request: {
          limit: targetRequest.limit,
          offset: targetRequest.offset
        },
        ...overrides
      });
    };

    if (currentState.isLoading === true) {
      return createState({
        reason: "navigation_while_loading"
      });
    }

    if (intent === "first") {
      return ready(0);
    }

    if (intent === "retry") {
      if (
        currentState.hasError !== true ||
        currentState.canRetry !== true
      ) {
        return createState({
          reason: "retry_not_available"
        });
      }

      return ready(
        normalizedRequest.offset,
        {
          isRetry: true
        }
      );
    }

    const paginationState =
      currentState.paginationState &&
      typeof currentState.paginationState === "object" &&
      !Array.isArray(currentState.paginationState)
        ? currentState.paginationState
        : null;

    if (
      !paginationState ||
      paginationState.isValid !== true
    ) {
      return invalid("pagination_state_invalid");
    }

    if (intent === "previous") {
      if (
        paginationState.canGoPrevious !== true ||
        !Number.isInteger(
          paginationState.previousOffset
        )
      ) {
        return createState({
          reason: "previous_page_unavailable"
        });
      }

      return ready(
        paginationState.previousOffset
      );
    }

    if (
      paginationState.canGoNext !== true ||
      !Number.isInteger(
        paginationState.nextOffset
      )
    ) {
      return createState({
        reason: "next_page_unavailable"
      });
    }

    return ready(
      paginationState.nextOffset
    );
  }

  function normalizeParticipantExamResultHistoryPagination(options) {
    const source =
      options && typeof options === "object"
        ? options
        : {};

    const limit =
      source.limit === undefined
        ? 20
        : Number(source.limit);

    const offset =
      source.offset === undefined
        ? 0
        : Number(source.offset);

    const isLimitValid =
      Number.isInteger(limit) &&
      limit >= 1 &&
      limit <= 50;

    const isOffsetValid =
      Number.isInteger(offset) &&
      offset >= 0 &&
      offset <= 10000;

    return {
      isValid: isLimitValid && isOffsetValid,
      limit,
      offset,
      isLimitValid,
      isOffsetValid
    };
  }

  function listParticipantFullExamResults(options) {
    const rpcState = getParticipantExamResultHistoryRpcState();
    const pagination =
      normalizeParticipantExamResultHistoryPagination(options);

    if (!pagination.isValid) {
      return Promise.resolve({
        version: "v27.29b",
        status: "exam_result_history_pagination_invalid",
        ok: false,
        isLiveCall: false,
        results: [],
        totalCount: null,
        request: null,
        reason: !pagination.isLimitValid
          ? "limit_must_be_integer_between_1_and_50"
          : "offset_must_be_integer_between_0_and_10000",
        rpcState
      });
    }

    return Promise.resolve({
      version: "v27.29b",
      status: "exam_result_history_rpc_blocked_safe_local_mode",
      ok: false,
      isLiveCall: false,
      results: [],
      totalCount: null,
      request: {
        rpcName: rpcState.rpcName,
        parameters: {
          p_limit: pagination.limit,
          p_offset: pagination.offset
        }
      },
      reason: rpcState.reason,
      rpcState
    });
  }

  function getParticipantDashboardCertificateHistoryState() {
    const participantDashboardExamHistoryState = getParticipantDashboardExamHistoryState();
    const participantDashboardCourseAccessState = getParticipantDashboardCourseAccessState();

    return {
      version: "v26.63a",
      status: "local_dashboard_certificate_history_hidden",
      isAvailable: true,
      isVisible: false,
      canRender: false,
      canLoadCertificateHistory: false,
      hasCertificateHistoryData: false,
      certificateHistoryEntries: [],
      totalCertificateHistoryCount: null,
      issuedCertificateCount: null,
      pendingCertificateCount: null,
      failedCertificateCount: null,
      latestCertificateTitle: null,
      latestCertificateStatus: null,
      latestCertificateIssuedAt: null,
      latestCertificateDownloadUrl: null,
      recommendedCertificateHistoryAction: null,
      canShowCertificateHistoryList: false,
      canShowCertificateHistoryCard: false,
      canShowCertificateIssueStatus: false,
      canShowCertificateDownloadAction: false,
      canOpenCertificateHistoryEntry: false,
      canDownloadCertificateFromHistory: false,
      canBlockDashboardAccess: false,
      isLoginRequired: false,
      isLocalDashboardAccessAllowed: true,
      reason: "dashboard_certificate_history_state_prepared_but_hidden_in_local_mode",
      futureStatuses: [
        "dashboard_certificate_history_visible_later",
        "dashboard_certificate_history_loading_later",
        "dashboard_certificate_history_ready_later",
        "dashboard_certificate_history_empty_later",
        "dashboard_certificate_history_download_ready_later",
        "dashboard_certificate_history_error_later"
      ],
      participantDashboardExamHistoryState,
      participantDashboardCourseAccessState
    };
  }

  function getParticipantDashboardCertificateDownloadState() {
    const participantDashboardCertificateHistoryState = getParticipantDashboardCertificateHistoryState();
    const participantDashboardCourseAccessState = getParticipantDashboardCourseAccessState();

    return {
      version: "v26.63a",
      status: "local_dashboard_certificate_download_hidden",
      isAvailable: true,
      isVisible: false,
      canRender: false,
      canLoadCertificateDownload: false,
      hasCertificateDownloadData: false,
      certificateDownloadEntries: [],
      certificateDownloadQueue: [],
      totalCertificateDownloadCount: null,
      availableCertificateDownloadCount: null,
      pendingCertificateDownloadCount: null,
      expiredCertificateDownloadCount: null,
      latestCertificateDownloadTitle: null,
      latestCertificateDownloadStatus: null,
      latestCertificateDownloadUrl: null,
      latestCertificateDownloadAvailableUntil: null,
      recommendedCertificateDownloadAction: null,
      canShowCertificateDownloadList: false,
      canShowCertificateDownloadCard: false,
      canShowCertificateDownloadButton: false,
      canShowCertificateDownloadStatus: false,
      canStartCertificateDownload: false,
      canOpenCertificateDownloadPreview: false,
      canTrackCertificateDownload: false,
      canBlockDashboardAccess: false,
      isLoginRequired: false,
      isLocalDashboardAccessAllowed: true,
      reason: "dashboard_certificate_download_state_prepared_but_hidden_in_local_mode",
      futureStatuses: [
        "dashboard_certificate_download_visible_later",
        "dashboard_certificate_download_loading_later",
        "dashboard_certificate_download_ready_later",
        "dashboard_certificate_download_empty_later",
        "dashboard_certificate_download_available_later",
        "dashboard_certificate_download_error_later"
      ],
      participantDashboardCertificateHistoryState,
      participantDashboardCourseAccessState
    };
  }

  function getParticipantDashboardCertificatePreviewState() {
    const participantDashboardCertificateDownloadState = getParticipantDashboardCertificateDownloadState();
    const participantDashboardCertificateHistoryState = getParticipantDashboardCertificateHistoryState();

    return {
      version: "v26.63a",
      status: "local_dashboard_certificate_preview_hidden",
      isAvailable: true,
      isVisible: false,
      canRender: false,
      canLoadCertificatePreview: false,
      hasCertificatePreviewData: false,
      certificatePreviewEntries: [],
      activeCertificatePreviewId: null,
      totalCertificatePreviewCount: null,
      availableCertificatePreviewCount: null,
      latestCertificatePreviewTitle: null,
      latestCertificatePreviewStatus: null,
      latestCertificatePreviewUrl: null,
      latestCertificatePreviewMimeType: null,
      latestCertificatePreviewGeneratedAt: null,
      latestCertificatePreviewExpiresAt: null,
      recommendedCertificatePreviewAction: null,
      canShowCertificatePreviewList: false,
      canShowCertificatePreviewCard: false,
      canShowCertificatePreviewButton: false,
      canShowCertificatePreviewStatus: false,
      canOpenCertificatePreview: false,
      canRenderCertificatePreviewFrame: false,
      canRefreshCertificatePreview: false,
      canPrintCertificatePreview: false,
      canBlockDashboardAccess: false,
      isLoginRequired: false,
      isLocalDashboardAccessAllowed: true,
      reason: "dashboard_certificate_preview_state_prepared_but_hidden_in_local_mode",
      futureStatuses: [
        "dashboard_certificate_preview_visible_later",
        "dashboard_certificate_preview_loading_later",
        "dashboard_certificate_preview_ready_later",
        "dashboard_certificate_preview_empty_later",
        "dashboard_certificate_preview_expired_later",
        "dashboard_certificate_preview_error_later"
      ],
      participantDashboardCertificateDownloadState,
      participantDashboardCertificateHistoryState
    };
  }

  function getParticipantDashboardCertificatePrintState() {
    const participantDashboardCertificatePreviewState = getParticipantDashboardCertificatePreviewState();
    const participantDashboardCertificateDownloadState = getParticipantDashboardCertificateDownloadState();

    return {
      version: "v26.66a",
      status: "local_dashboard_certificate_print_hidden",
      isAvailable: true,
      isVisible: false,
      canRender: false,
      canLoadCertificatePrint: false,
      hasCertificatePrintData: false,
      certificatePrintEntries: [],
      activeCertificatePrintId: null,
      totalCertificatePrintCount: null,
      latestCertificatePrintTitle: null,
      latestCertificatePrintStatus: null,
      latestCertificatePrintUrl: null,
      latestCertificatePrintGeneratedAt: null,
      latestCertificatePrintExpiresAt: null,
      recommendedCertificatePrintAction: null,
      canShowCertificatePrintList: false,
      canShowCertificatePrintCard: false,
      canShowCertificatePrintButton: false,
      canShowCertificatePrintStatus: false,
      canOpenCertificatePrintDialog: false,
      canRenderCertificatePrintView: false,
      canStartCertificatePrint: false,
      canRefreshCertificatePrint: false,
      canBlockDashboardAccess: false,
      isLoginRequired: false,
      isLocalDashboardAccessAllowed: true,
      reason: "dashboard_certificate_print_state_prepared_but_hidden_in_local_mode",
      futureStatuses: [
        "dashboard_certificate_print_visible_later",
        "dashboard_certificate_print_loading_later",
        "dashboard_certificate_print_ready_later",
        "dashboard_certificate_print_empty_later",
        "dashboard_certificate_print_expired_later",
        "dashboard_certificate_print_error_later"
      ],
      participantDashboardCertificatePreviewState,
      participantDashboardCertificateDownloadState
    };
  }

  function getParticipantDashboardCertificateShareState() {
    const participantDashboardCertificatePrintState = getParticipantDashboardCertificatePrintState();
    const participantDashboardCertificatePreviewState = getParticipantDashboardCertificatePreviewState();

    return {
      version: "v26.66a",
      status: "local_dashboard_certificate_share_hidden",
      isAvailable: true,
      isVisible: false,
      canRender: false,
      canLoadCertificateShare: false,
      hasCertificateShareData: false,
      certificateShareEntries: [],
      activeCertificateShareId: null,
      latestCertificateShareTitle: null,
      latestCertificateShareStatus: null,
      latestCertificateShareUrl: null,
      latestCertificateShareExpiresAt: null,
      recommendedCertificateShareAction: null,
      canShowCertificateShareCard: false,
      canShowCertificateShareButton: false,
      canShowCertificateShareStatus: false,
      canOpenCertificateShareDialog: false,
      canCreateCertificateShareLink: false,
      canCopyCertificateShareLink: false,
      canSendCertificateShareEmail: false,
      canRevokeCertificateShareLink: false,
      canBlockDashboardAccess: false,
      isLoginRequired: false,
      isLocalDashboardAccessAllowed: true,
      reason: "dashboard_certificate_share_state_prepared_but_hidden_in_local_mode",
      futureStatuses: [
        "dashboard_certificate_share_visible_later",
        "dashboard_certificate_share_loading_later",
        "dashboard_certificate_share_ready_later",
        "dashboard_certificate_share_empty_later",
        "dashboard_certificate_share_revoked_later",
        "dashboard_certificate_share_error_later"
      ],
      participantDashboardCertificatePrintState,
      participantDashboardCertificatePreviewState
    };
  }

  function getParticipantDashboardCertificateVerificationState() {
    const participantDashboardCertificateShareState = getParticipantDashboardCertificateShareState();
    const participantDashboardCertificatePrintState = getParticipantDashboardCertificatePrintState();

    return {
      version: "v26.67a",
      status: "local_dashboard_certificate_verification_hidden",
      isAvailable: true,
      isVisible: false,
      canRender: false,
      canLoadCertificateVerification: false,
      hasCertificateVerificationData: false,
      certificateVerificationEntries: [],
      activeCertificateVerificationId: null,
      latestCertificateVerificationCode: null,
      latestCertificateVerificationUrl: null,
      latestCertificateVerificationStatus: null,
      latestCertificateVerificationExpiresAt: null,
      recommendedCertificateVerificationAction: null,
      canShowCertificateVerificationCard: false,
      canShowCertificateVerificationButton: false,
      canShowCertificateVerificationStatus: false,
      canOpenCertificateVerificationDialog: false,
      canCreateCertificateVerificationCode: false,
      canCopyCertificateVerificationCode: false,
      canOpenCertificateVerificationPage: false,
      canVerifyCertificateOnline: false,
      canBlockDashboardAccess: false,
      isLoginRequired: false,
      isLocalDashboardAccessAllowed: true,
      reason: "dashboard_certificate_verification_state_prepared_but_hidden_in_local_mode",
      futureStatuses: [
        "dashboard_certificate_verification_visible_later",
        "dashboard_certificate_verification_loading_later",
        "dashboard_certificate_verification_ready_later",
        "dashboard_certificate_verification_empty_later",
        "dashboard_certificate_verification_expired_later",
        "dashboard_certificate_verification_error_later"
      ],
      participantDashboardCertificateShareState,
      participantDashboardCertificatePrintState
    };
  }

  function getParticipantDashboardCertificateQrCodeState() {
    const participantDashboardCertificateVerificationState = getParticipantDashboardCertificateVerificationState();
    const participantDashboardCertificateShareState = getParticipantDashboardCertificateShareState();

    return {
      version: "v26.68a",
      status: "local_dashboard_certificate_qr_code_hidden",
      isAvailable: true,
      isVisible: false,
      canRender: false,
      canLoadCertificateQrCode: false,
      hasCertificateQrCodeData: false,
      certificateQrCodeEntries: [],
      activeCertificateQrCodeId: null,
      latestCertificateQrCodeValue: null,
      latestCertificateQrCodeImageUrl: null,
      latestCertificateQrCodeStatus: null,
      latestCertificateQrCodeExpiresAt: null,
      recommendedCertificateQrCodeAction: null,
      canShowCertificateQrCodeCard: false,
      canShowCertificateQrCodeButton: false,
      canShowCertificateQrCodeStatus: false,
      canOpenCertificateQrCodeDialog: false,
      canCreateCertificateQrCode: false,
      canRenderCertificateQrCodeImage: false,
      canDownloadCertificateQrCode: false,
      canPrintCertificateQrCode: false,
      canBlockDashboardAccess: false,
      isLoginRequired: false,
      isLocalDashboardAccessAllowed: true,
      reason: "dashboard_certificate_qr_code_state_prepared_but_hidden_in_local_mode",
      futureStatuses: [
        "dashboard_certificate_qr_code_visible_later",
        "dashboard_certificate_qr_code_loading_later",
        "dashboard_certificate_qr_code_ready_later",
        "dashboard_certificate_qr_code_empty_later",
        "dashboard_certificate_qr_code_expired_later",
        "dashboard_certificate_qr_code_error_later"
      ],
      participantDashboardCertificateVerificationState,
      participantDashboardCertificateShareState
    };
  }

  function getParticipantDashboardCertificateValidityState() {
    const participantDashboardCertificateQrCodeState = getParticipantDashboardCertificateQrCodeState();
    const participantDashboardCertificateVerificationState = getParticipantDashboardCertificateVerificationState();

    return {
      version: "v26.69a",
      status: "local_dashboard_certificate_validity_hidden",
      isAvailable: true,
      isVisible: false,
      canRender: false,
      canLoadCertificateValidity: false,
      hasCertificateValidityData: false,
      certificateValidityEntries: [],
      activeCertificateValidityId: null,
      latestCertificateValidityStatus: null,
      latestCertificateValidityCheckedAt: null,
      latestCertificateValidityExpiresAt: null,
      latestCertificateValidityRevokedAt: null,
      latestCertificateValidityReason: null,
      recommendedCertificateValidityAction: null,
      canShowCertificateValidityCard: false,
      canShowCertificateValidityButton: false,
      canShowCertificateValidityStatus: false,
      canOpenCertificateValidityDialog: false,
      canCheckCertificateValidity: false,
      canRefreshCertificateValidity: false,
      canShowCertificateValidBadge: false,
      canShowCertificateExpiredBadge: false,
      canShowCertificateRevokedBadge: false,
      canBlockDashboardAccess: false,
      isLoginRequired: false,
      isLocalDashboardAccessAllowed: true,
      reason: "dashboard_certificate_validity_state_prepared_but_hidden_in_local_mode",
      futureStatuses: [
        "dashboard_certificate_validity_visible_later",
        "dashboard_certificate_validity_loading_later",
        "dashboard_certificate_validity_valid_later",
        "dashboard_certificate_validity_expired_later",
        "dashboard_certificate_validity_revoked_later",
        "dashboard_certificate_validity_missing_later",
        "dashboard_certificate_validity_error_later"
      ],
      participantDashboardCertificateQrCodeState,
      participantDashboardCertificateVerificationState
    };
  }

  function getParticipantDashboardCertificateRevocationState() {
    const participantDashboardCertificateValidityState = getParticipantDashboardCertificateValidityState();
    const participantDashboardCertificateVerificationState = getParticipantDashboardCertificateVerificationState();

    return {
      version: "v26.70a",
      status: "local_dashboard_certificate_revocation_hidden",
      isAvailable: true,
      isVisible: false,
      canRender: false,
      canLoadCertificateRevocation: false,
      hasCertificateRevocationData: false,
      certificateRevocationEntries: [],
      activeCertificateRevocationId: null,
      latestCertificateRevocationStatus: null,
      latestCertificateRevocationReason: null,
      latestCertificateRevocationRequestedAt: null,
      latestCertificateRevocationConfirmedAt: null,
      latestCertificateRevocationActor: null,
      recommendedCertificateRevocationAction: null,
      canShowCertificateRevocationCard: false,
      canShowCertificateRevocationButton: false,
      canShowCertificateRevocationStatus: false,
      canOpenCertificateRevocationDialog: false,
      canRequestCertificateRevocation: false,
      canConfirmCertificateRevocation: false,
      canCancelCertificateRevocation: false,
      canShowCertificateRevokedNotice: false,
      canBlockDashboardAccess: false,
      isLoginRequired: false,
      isLocalDashboardAccessAllowed: true,
      reason: "dashboard_certificate_revocation_state_prepared_but_hidden_in_local_mode",
      futureStatuses: [
        "dashboard_certificate_revocation_visible_later",
        "dashboard_certificate_revocation_loading_later",
        "dashboard_certificate_revocation_requested_later",
        "dashboard_certificate_revocation_confirmed_later",
        "dashboard_certificate_revocation_cancelled_later",
        "dashboard_certificate_revocation_error_later"
      ],
      participantDashboardCertificateValidityState,
      participantDashboardCertificateVerificationState
    };
  }

  function getParticipantDashboardCertificateAuditLogState() {
    const participantDashboardCertificateRevocationState = getParticipantDashboardCertificateRevocationState();
    const participantDashboardCertificateValidityState = getParticipantDashboardCertificateValidityState();

    return {
      version: "v26.71a",
      status: "local_dashboard_certificate_audit_log_hidden",
      isAvailable: true,
      isVisible: false,
      canRender: false,
      canLoadCertificateAuditLog: false,
      hasCertificateAuditLogData: false,
      certificateAuditLogEntries: [],
      activeCertificateAuditLogId: null,
      latestCertificateAuditLogAction: null,
      latestCertificateAuditLogActor: null,
      latestCertificateAuditLogCreatedAt: null,
      latestCertificateAuditLogIpHint: null,
      recommendedCertificateAuditLogAction: null,
      canShowCertificateAuditLogCard: false,
      canShowCertificateAuditLogButton: false,
      canShowCertificateAuditLogList: false,
      canOpenCertificateAuditLogDialog: false,
      canRefreshCertificateAuditLog: false,
      canExportCertificateAuditLog: false,
      canBlockDashboardAccess: false,
      isLoginRequired: false,
      isLocalDashboardAccessAllowed: true,
      reason: "dashboard_certificate_audit_log_state_prepared_but_hidden_in_local_mode",
      futureStatuses: [
        "dashboard_certificate_audit_log_visible_later",
        "dashboard_certificate_audit_log_loading_later",
        "dashboard_certificate_audit_log_ready_later",
        "dashboard_certificate_audit_log_empty_later",
        "dashboard_certificate_audit_log_error_later"
      ],
      plannedAuditActions: [
        "certificate_issued_later",
        "certificate_downloaded_later",
        "certificate_shared_later",
        "certificate_verified_later",
        "certificate_revoked_later"
      ],
      participantDashboardCertificateRevocationState,
      participantDashboardCertificateValidityState
    };
  }

  function getParticipantDashboardCertificateConsentState() {
    const participantDashboardCertificateAuditLogState = getParticipantDashboardCertificateAuditLogState();
    const participantDashboardCertificateShareState = getParticipantDashboardCertificateShareState();

    return {
      version: "v26.72a",
      status: "local_dashboard_certificate_consent_hidden",
      isAvailable: true,
      isVisible: false,
      canRender: false,
      canLoadCertificateConsent: false,
      hasCertificateConsentData: false,
      certificateConsentEntries: [],
      activeCertificateConsentId: null,
      latestCertificateConsentStatus: null,
      latestCertificateConsentGrantedAt: null,
      latestCertificateConsentRevokedAt: null,
      latestCertificateConsentTextVersion: null,
      latestCertificateConsentScope: null,
      recommendedCertificateConsentAction: null,
      canShowCertificateConsentCard: false,
      canShowCertificateConsentButton: false,
      canShowCertificateConsentStatus: false,
      canOpenCertificateConsentDialog: false,
      canGrantCertificateConsent: false,
      canRevokeCertificateConsent: false,
      canRefreshCertificateConsent: false,
      canBlockDashboardAccess: false,
      isLoginRequired: false,
      isLocalDashboardAccessAllowed: true,
      reason: "dashboard_certificate_consent_state_prepared_but_hidden_in_local_mode",
      futureStatuses: [
        "dashboard_certificate_consent_visible_later",
        "dashboard_certificate_consent_loading_later",
        "dashboard_certificate_consent_granted_later",
        "dashboard_certificate_consent_declined_later",
        "dashboard_certificate_consent_revoked_later",
        "dashboard_certificate_consent_missing_later",
        "dashboard_certificate_consent_error_later"
      ],
      plannedConsentScopes: [
        "certificate_display_later",
        "certificate_download_later",
        "certificate_share_later",
        "certificate_online_verification_later"
      ],
      participantDashboardCertificateAuditLogState,
      participantDashboardCertificateShareState
    };
  }

  function getParticipantDashboardCertificatePrivacyNoticeState() {
    const participantDashboardCertificateConsentState = getParticipantDashboardCertificateConsentState();
    const participantDashboardCertificateAuditLogState = getParticipantDashboardCertificateAuditLogState();

    return {
      version: "v26.73a",
      status: "local_dashboard_certificate_privacy_notice_hidden",
      isAvailable: true,
      isVisible: false,
      canRender: false,
      canLoadCertificatePrivacyNotice: false,
      hasCertificatePrivacyNoticeData: false,
      certificatePrivacyNoticeEntries: [],
      activeCertificatePrivacyNoticeId: null,
      latestCertificatePrivacyNoticeVersion: null,
      latestCertificatePrivacyNoticeTitle: null,
      latestCertificatePrivacyNoticeText: null,
      latestCertificatePrivacyNoticePublishedAt: null,
      latestCertificatePrivacyNoticeAcceptedAt: null,
      recommendedCertificatePrivacyNoticeAction: null,
      canShowCertificatePrivacyNoticeCard: false,
      canShowCertificatePrivacyNoticeButton: false,
      canShowCertificatePrivacyNoticeText: false,
      canOpenCertificatePrivacyNoticeDialog: false,
      canAcceptCertificatePrivacyNotice: false,
      canRefreshCertificatePrivacyNotice: false,
      canBlockDashboardAccess: false,
      isLoginRequired: false,
      isLocalDashboardAccessAllowed: true,
      reason: "dashboard_certificate_privacy_notice_state_prepared_but_hidden_in_local_mode",
      futureStatuses: [
        "dashboard_certificate_privacy_notice_visible_later",
        "dashboard_certificate_privacy_notice_loading_later",
        "dashboard_certificate_privacy_notice_ready_later",
        "dashboard_certificate_privacy_notice_accepted_later",
        "dashboard_certificate_privacy_notice_missing_later",
        "dashboard_certificate_privacy_notice_error_later"
      ],
      plannedPrivacyNoticeScopes: [
        "certificate_display_privacy_notice_later",
        "certificate_download_privacy_notice_later",
        "certificate_share_privacy_notice_later",
        "certificate_online_verification_privacy_notice_later"
      ],
      participantDashboardCertificateConsentState,
      participantDashboardCertificateAuditLogState
    };
  }

  function getParticipantDashboardCertificateRetentionState() {
    const participantDashboardCertificatePrivacyNoticeState = getParticipantDashboardCertificatePrivacyNoticeState();
    const participantDashboardCertificateAuditLogState = getParticipantDashboardCertificateAuditLogState();

    return {
      version: "v26.74a",
      status: "local_dashboard_certificate_retention_hidden",
      isAvailable: true,
      isVisible: false,
      canRender: false,
      canLoadCertificateRetention: false,
      hasCertificateRetentionData: false,
      certificateRetentionEntries: [],
      activeCertificateRetentionPolicyId: null,
      latestCertificateRetentionStatus: null,
      latestCertificateRetentionRuleVersion: null,
      latestCertificateRetentionUntil: null,
      latestCertificateRetentionDeletionRequestedAt: null,
      latestCertificateRetentionDeletionConfirmedAt: null,
      recommendedCertificateRetentionAction: null,
      canShowCertificateRetentionCard: false,
      canShowCertificateRetentionButton: false,
      canShowCertificateRetentionStatus: false,
      canOpenCertificateRetentionDialog: false,
      canRequestCertificateDeletion: false,
      canConfirmCertificateDeletion: false,
      canRefreshCertificateRetention: false,
      canBlockDashboardAccess: false,
      isLoginRequired: false,
      isLocalDashboardAccessAllowed: true,
      reason: "dashboard_certificate_retention_state_prepared_but_hidden_in_local_mode",
      futureStatuses: [
        "dashboard_certificate_retention_visible_later",
        "dashboard_certificate_retention_loading_later",
        "dashboard_certificate_retention_ready_later",
        "dashboard_certificate_deletion_requested_later",
        "dashboard_certificate_deletion_confirmed_later",
        "dashboard_certificate_anonymized_later",
        "dashboard_certificate_retention_error_later"
      ],
      plannedRetentionActions: [
        "certificate_retention_policy_later",
        "certificate_deletion_request_later",
        "certificate_deletion_confirmation_later",
        "certificate_anonymization_later"
      ],
      participantDashboardCertificatePrivacyNoticeState,
      participantDashboardCertificateAuditLogState
    };
  }

  function getParticipantDashboardCertificateDataAccessState() {
    const participantDashboardCertificateRetentionState = getParticipantDashboardCertificateRetentionState();
    const participantDashboardCertificatePrivacyNoticeState = getParticipantDashboardCertificatePrivacyNoticeState();

    return {
      version: "v26.75a",
      status: "local_dashboard_certificate_data_access_hidden",
      isAvailable: true,
      isVisible: false,
      canRender: false,
      canLoadCertificateDataAccess: false,
      hasCertificateDataAccessData: false,
      certificateDataAccessEntries: [],
      activeCertificateDataAccessRequestId: null,
      latestCertificateDataAccessStatus: null,
      latestCertificateDataAccessRequestedAt: null,
      latestCertificateDataAccessPreparedAt: null,
      latestCertificateDataAccessDownloadedAt: null,
      latestCertificateDataAccessExpiresAt: null,
      recommendedCertificateDataAccessAction: null,
      canShowCertificateDataAccessCard: false,
      canShowCertificateDataAccessButton: false,
      canShowCertificateDataAccessStatus: false,
      canOpenCertificateDataAccessDialog: false,
      canRequestCertificateDataAccess: false,
      canPrepareCertificateDataExport: false,
      canDownloadCertificateDataExport: false,
      canRefreshCertificateDataAccess: false,
      canBlockDashboardAccess: false,
      isLoginRequired: false,
      isLocalDashboardAccessAllowed: true,
      reason: "dashboard_certificate_data_access_state_prepared_but_hidden_in_local_mode",
      futureStatuses: [
        "dashboard_certificate_data_access_visible_later",
        "dashboard_certificate_data_access_loading_later",
        "dashboard_certificate_data_access_requested_later",
        "dashboard_certificate_data_access_prepared_later",
        "dashboard_certificate_data_access_download_ready_later",
        "dashboard_certificate_data_access_expired_later",
        "dashboard_certificate_data_access_error_later"
      ],
      plannedDataAccessActions: [
        "certificate_data_access_request_later",
        "certificate_data_export_prepare_later",
        "certificate_data_export_download_later",
        "certificate_data_export_expiry_later"
      ],
      participantDashboardCertificateRetentionState,
      participantDashboardCertificatePrivacyNoticeState
    };
  }

  function getParticipantDashboardCertificateDataCorrectionState() {
    const participantDashboardCertificateDataAccessState = getParticipantDashboardCertificateDataAccessState();
    const participantDashboardCertificatePrivacyNoticeState = getParticipantDashboardCertificatePrivacyNoticeState();

    return {
      version: "v26.76a",
      status: "local_dashboard_certificate_data_correction_hidden",
      isAvailable: true,
      isVisible: false,
      canRender: false,
      canLoadCertificateDataCorrection: false,
      hasCertificateDataCorrectionData: false,
      certificateDataCorrectionEntries: [],
      activeCertificateDataCorrectionRequestId: null,
      latestCertificateDataCorrectionStatus: null,
      latestCertificateDataCorrectionRequestedAt: null,
      latestCertificateDataCorrectionReviewedAt: null,
      latestCertificateDataCorrectionApprovedAt: null,
      latestCertificateDataCorrectionRejectedAt: null,
      latestCertificateDataCorrectionReason: null,
      recommendedCertificateDataCorrectionAction: null,
      canShowCertificateDataCorrectionCard: false,
      canShowCertificateDataCorrectionButton: false,
      canShowCertificateDataCorrectionStatus: false,
      canOpenCertificateDataCorrectionDialog: false,
      canRequestCertificateDataCorrection: false,
      canReviewCertificateDataCorrection: false,
      canApproveCertificateDataCorrection: false,
      canRejectCertificateDataCorrection: false,
      canRefreshCertificateDataCorrection: false,
      canBlockDashboardAccess: false,
      isLoginRequired: false,
      isLocalDashboardAccessAllowed: true,
      reason: "dashboard_certificate_data_correction_state_prepared_but_hidden_in_local_mode",
      futureStatuses: [
        "dashboard_certificate_data_correction_visible_later",
        "dashboard_certificate_data_correction_loading_later",
        "dashboard_certificate_data_correction_requested_later",
        "dashboard_certificate_data_correction_reviewed_later",
        "dashboard_certificate_data_correction_approved_later",
        "dashboard_certificate_data_correction_rejected_later",
        "dashboard_certificate_data_correction_error_later"
      ],
      plannedDataCorrectionActions: [
        "certificate_data_correction_request_later",
        "certificate_data_correction_review_later",
        "certificate_data_correction_approval_later",
        "certificate_data_correction_rejection_later"
      ],
      participantDashboardCertificateDataAccessState,
      participantDashboardCertificatePrivacyNoticeState
    };
  }

  function getParticipantDashboardCertificateDataDeletionRequestState() {
    const participantDashboardCertificateDataCorrectionState = getParticipantDashboardCertificateDataCorrectionState();
    const participantDashboardCertificateRetentionState = getParticipantDashboardCertificateRetentionState();

    return {
      version: "v26.77a",
      status: "local_dashboard_certificate_data_deletion_request_hidden",
      isAvailable: true,
      isVisible: false,
      canRender: false,
      canLoadCertificateDataDeletionRequest: false,
      hasCertificateDataDeletionRequestData: false,
      certificateDataDeletionRequestEntries: [],
      activeCertificateDataDeletionRequestId: null,
      latestCertificateDataDeletionRequestStatus: null,
      latestCertificateDataDeletionRequestedAt: null,
      latestCertificateDataDeletionReviewedAt: null,
      latestCertificateDataDeletionApprovedAt: null,
      latestCertificateDataDeletionRejectedAt: null,
      latestCertificateDataDeletionCompletedAt: null,
      latestCertificateDataDeletionReason: null,
      recommendedCertificateDataDeletionRequestAction: null,
      canShowCertificateDataDeletionRequestCard: false,
      canShowCertificateDataDeletionRequestButton: false,
      canShowCertificateDataDeletionRequestStatus: false,
      canOpenCertificateDataDeletionRequestDialog: false,
      canRequestCertificateDataDeletion: false,
      canReviewCertificateDataDeletionRequest: false,
      canApproveCertificateDataDeletionRequest: false,
      canRejectCertificateDataDeletionRequest: false,
      canCompleteCertificateDataDeletionRequest: false,
      canRefreshCertificateDataDeletionRequest: false,
      canBlockDashboardAccess: false,
      isLoginRequired: false,
      isLocalDashboardAccessAllowed: true,
      reason: "dashboard_certificate_data_deletion_request_state_prepared_but_hidden_in_local_mode",
      futureStatuses: [
        "dashboard_certificate_data_deletion_request_visible_later",
        "dashboard_certificate_data_deletion_request_loading_later",
        "dashboard_certificate_data_deletion_requested_later",
        "dashboard_certificate_data_deletion_reviewed_later",
        "dashboard_certificate_data_deletion_approved_later",
        "dashboard_certificate_data_deletion_rejected_later",
        "dashboard_certificate_data_deletion_completed_later",
        "dashboard_certificate_data_deletion_error_later"
      ],
      plannedDataDeletionRequestActions: [
        "certificate_data_deletion_request_later",
        "certificate_data_deletion_review_later",
        "certificate_data_deletion_approval_later",
        "certificate_data_deletion_rejection_later",
        "certificate_data_deletion_completion_later"
      ],
      participantDashboardCertificateDataCorrectionState,
      participantDashboardCertificateRetentionState
    };
  }

  function getParticipantDashboardCertificateDataDeletionConfirmationState() {
    const participantDashboardCertificateDataDeletionRequestState = getParticipantDashboardCertificateDataDeletionRequestState();
    const participantDashboardCertificateRetentionState = getParticipantDashboardCertificateRetentionState();

    return {
      version: "v26.78a",
      status: "local_dashboard_certificate_data_deletion_confirmation_hidden",
      isAvailable: true,
      isVisible: false,
      canRender: false,
      canLoadCertificateDataDeletionConfirmation: false,
      hasCertificateDataDeletionConfirmationData: false,
      certificateDataDeletionConfirmationEntries: [],
      activeCertificateDataDeletionConfirmationId: null,
      latestCertificateDataDeletionConfirmationStatus: null,
      latestCertificateDataDeletionConfirmedAt: null,
      latestCertificateDataDeletionConfirmedBy: null,
      latestCertificateDataDeletionConfirmationReason: null,
      recommendedCertificateDataDeletionConfirmationAction: null,
      canShowCertificateDataDeletionConfirmationCard: false,
      canShowCertificateDataDeletionConfirmationButton: false,
      canShowCertificateDataDeletionConfirmationStatus: false,
      canOpenCertificateDataDeletionConfirmationDialog: false,
      canConfirmCertificateDataDeletion: false,
      canDownloadCertificateDataDeletionConfirmation: false,
      canRefreshCertificateDataDeletionConfirmation: false,
      canBlockDashboardAccess: false,
      isLoginRequired: false,
      isLocalDashboardAccessAllowed: true,
      reason: "dashboard_certificate_data_deletion_confirmation_state_prepared_but_hidden_in_local_mode",
      futureStatuses: [
        "dashboard_certificate_data_deletion_confirmation_visible_later",
        "dashboard_certificate_data_deletion_confirmation_loading_later",
        "dashboard_certificate_data_deletion_confirmed_later",
        "dashboard_certificate_data_deletion_confirmation_download_ready_later",
        "dashboard_certificate_data_deletion_confirmation_error_later"
      ],
      plannedDataDeletionConfirmationActions: [
        "certificate_data_deletion_confirmation_later",
        "certificate_data_deletion_confirmation_download_later",
        "certificate_data_deletion_confirmation_refresh_later"
      ],
      participantDashboardCertificateDataDeletionRequestState,
      participantDashboardCertificateRetentionState
    };
  }

  function getParticipantDashboardCertificateDataExportFileState() {
    const participantDashboardCertificateDataAccessState = getParticipantDashboardCertificateDataAccessState();
    const participantDashboardCertificatePrivacyNoticeState = getParticipantDashboardCertificatePrivacyNoticeState();

    return {
      version: "v26.79a",
      status: "local_dashboard_certificate_data_export_file_hidden",
      isAvailable: true,
      isVisible: false,
      canRender: false,
      canLoadCertificateDataExportFile: false,
      hasCertificateDataExportFileData: false,
      certificateDataExportFileEntries: [],
      activeCertificateDataExportFileId: null,
      latestCertificateDataExportFileStatus: null,
      latestCertificateDataExportFilePreparedAt: null,
      latestCertificateDataExportFileGeneratedAt: null,
      latestCertificateDataExportFileDownloadedAt: null,
      latestCertificateDataExportFileExpiresAt: null,
      recommendedCertificateDataExportFileAction: null,
      canShowCertificateDataExportFileCard: false,
      canShowCertificateDataExportFileButton: false,
      canShowCertificateDataExportFileStatus: false,
      canPrepareCertificateDataExportFile: false,
      canGenerateCertificateDataExportFile: false,
      canDownloadCertificateDataExportFile: false,
      canRefreshCertificateDataExportFile: false,
      canBlockDashboardAccess: false,
      isLoginRequired: false,
      isLocalDashboardAccessAllowed: true,
      reason: "dashboard_certificate_data_export_file_state_prepared_but_hidden_in_local_mode",
      futureStatuses: [
        "dashboard_certificate_data_export_file_visible_later",
        "dashboard_certificate_data_export_file_loading_later",
        "dashboard_certificate_data_export_file_prepared_later",
        "dashboard_certificate_data_export_file_generated_later",
        "dashboard_certificate_data_export_file_download_ready_later",
        "dashboard_certificate_data_export_file_expired_later",
        "dashboard_certificate_data_export_file_error_later"
      ],
      plannedDataExportFileActions: [
        "certificate_data_export_file_prepare_later",
        "certificate_data_export_file_generate_later",
        "certificate_data_export_file_download_later",
        "certificate_data_export_file_expiry_later"
      ],
      participantDashboardCertificateDataAccessState,
      participantDashboardCertificatePrivacyNoticeState
    };
  }

  function getParticipantDashboardCertificateDataExportExpiryState() {
    const participantDashboardCertificateDataExportFileState = getParticipantDashboardCertificateDataExportFileState();
    const participantDashboardCertificateDataAccessState = getParticipantDashboardCertificateDataAccessState();

    return {
      version: "v26.80a",
      status: "local_dashboard_certificate_data_export_expiry_hidden",
      isAvailable: true,
      isVisible: false,
      canRender: false,
      canLoadCertificateDataExportExpiry: false,
      hasCertificateDataExportExpiryData: false,
      activeCertificateDataExportFileId: null,
      latestCertificateDataExportExpiryStatus: null,
      latestCertificateDataExportPreparedAt: null,
      latestCertificateDataExportExpiresAt: null,
      latestCertificateDataExportExpiredAt: null,
      recommendedCertificateDataExportExpiryAction: null,
      canShowCertificateDataExportExpiryCard: false,
      canShowCertificateDataExportExpiryWarning: false,
      canShowCertificateDataExportExpiredNotice: false,
      canCheckCertificateDataExportExpiry: false,
      canMarkCertificateDataExportExpired: false,
      canRefreshCertificateDataExportExpiry: false,
      canBlockDashboardAccess: false,
      isLoginRequired: false,
      isLocalDashboardAccessAllowed: true,
      reason: "dashboard_certificate_data_export_expiry_state_prepared_but_hidden_in_local_mode",
      futureStatuses: [
        "dashboard_certificate_data_export_expiry_visible_later",
        "dashboard_certificate_data_export_expiry_loading_later",
        "dashboard_certificate_data_export_expiry_valid_later",
        "dashboard_certificate_data_export_expiry_warning_later",
        "dashboard_certificate_data_export_expired_later",
        "dashboard_certificate_data_export_expiry_error_later"
      ],
      plannedDataExportExpiryActions: [
        "certificate_data_export_expiry_check_later",
        "certificate_data_export_expiry_warning_later",
        "certificate_data_export_expired_mark_later",
        "certificate_data_export_expiry_refresh_later"
      ],
      participantDashboardCertificateDataExportFileState,
      participantDashboardCertificateDataAccessState
    };
  }

  function getParticipantDashboardCertificateDataExportDownloadLogState() {
    const participantDashboardCertificateDataExportFileState = getParticipantDashboardCertificateDataExportFileState();
    const participantDashboardCertificateDataExportExpiryState = getParticipantDashboardCertificateDataExportExpiryState();

    return {
      version: "v26.81a",
      status: "local_dashboard_certificate_data_export_download_log_hidden",
      isAvailable: true,
      isVisible: false,
      canRender: false,
      canLoadCertificateDataExportDownloadLog: false,
      hasCertificateDataExportDownloadLogData: false,
      certificateDataExportDownloadLogEntries: [],
      activeCertificateDataExportDownloadLogId: null,
      latestCertificateDataExportDownloadStatus: null,
      latestCertificateDataExportDownloadedAt: null,
      latestCertificateDataExportDownloadedBy: null,
      latestCertificateDataExportDownloadFileId: null,
      latestCertificateDataExportDownloadReason: null,
      recommendedCertificateDataExportDownloadLogAction: null,
      canShowCertificateDataExportDownloadLogCard: false,
      canShowCertificateDataExportDownloadLogList: false,
      canRecordCertificateDataExportDownload: false,
      canRefreshCertificateDataExportDownloadLog: false,
      canBlockDashboardAccess: false,
      isLoginRequired: false,
      isLocalDashboardAccessAllowed: true,
      reason: "dashboard_certificate_data_export_download_log_state_prepared_but_hidden_in_local_mode",
      futureStatuses: [
        "dashboard_certificate_data_export_download_log_visible_later",
        "dashboard_certificate_data_export_download_log_loading_later",
        "dashboard_certificate_data_export_download_logged_later",
        "dashboard_certificate_data_export_download_log_empty_later",
        "dashboard_certificate_data_export_download_log_error_later"
      ],
      plannedDataExportDownloadLogActions: [
        "certificate_data_export_download_log_record_later",
        "certificate_data_export_download_log_list_later",
        "certificate_data_export_download_log_refresh_later"
      ],
      participantDashboardCertificateDataExportFileState,
      participantDashboardCertificateDataExportExpiryState
    };
  }

  function getParticipantDashboardCertificateDataExportErrorState() {
    const participantDashboardCertificateDataExportFileState = getParticipantDashboardCertificateDataExportFileState();
    const participantDashboardCertificateDataExportDownloadLogState = getParticipantDashboardCertificateDataExportDownloadLogState();

    return {
      version: "v26.82a",
      status: "local_dashboard_certificate_data_export_error_hidden",
      isAvailable: true,
      isVisible: false,
      canRender: false,
      canLoadCertificateDataExportError: false,
      hasCertificateDataExportErrorData: false,
      certificateDataExportErrorEntries: [],
      activeCertificateDataExportErrorId: null,
      latestCertificateDataExportErrorStatus: null,
      latestCertificateDataExportErrorCode: null,
      latestCertificateDataExportErrorMessage: null,
      latestCertificateDataExportErrorAt: null,
      latestCertificateDataExportErrorResolvedAt: null,
      recommendedCertificateDataExportErrorAction: null,
      canShowCertificateDataExportErrorCard: false,
      canShowCertificateDataExportErrorNotice: false,
      canRecordCertificateDataExportError: false,
      canResolveCertificateDataExportError: false,
      canRefreshCertificateDataExportError: false,
      canBlockDashboardAccess: false,
      isLoginRequired: false,
      isLocalDashboardAccessAllowed: true,
      reason: "dashboard_certificate_data_export_error_state_prepared_but_hidden_in_local_mode",
      futureStatuses: [
        "dashboard_certificate_data_export_error_visible_later",
        "dashboard_certificate_data_export_error_loading_later",
        "dashboard_certificate_data_export_error_recorded_later",
        "dashboard_certificate_data_export_error_resolved_later",
        "dashboard_certificate_data_export_error_empty_later"
      ],
      plannedDataExportErrorActions: [
        "certificate_data_export_error_record_later",
        "certificate_data_export_error_resolve_later",
        "certificate_data_export_error_refresh_later"
      ],
      participantDashboardCertificateDataExportFileState,
      participantDashboardCertificateDataExportDownloadLogState
    };
  }

  function getParticipantDashboardCertificateDataExportRetryState() {
    const participantDashboardCertificateDataExportFileState = getParticipantDashboardCertificateDataExportFileState();
    const participantDashboardCertificateDataExportErrorState = getParticipantDashboardCertificateDataExportErrorState();

    return {
      version: "v26.83a",
      status: "local_dashboard_certificate_data_export_retry_hidden",
      isAvailable: true,
      isVisible: false,
      canRender: false,
      canLoadCertificateDataExportRetry: false,
      hasCertificateDataExportRetryData: false,
      certificateDataExportRetryEntries: [],
      activeCertificateDataExportRetryId: null,
      latestCertificateDataExportRetryStatus: null,
      latestCertificateDataExportRetryReason: null,
      latestCertificateDataExportRetriedAt: null,
      latestCertificateDataExportRetryResolvedAt: null,
      recommendedCertificateDataExportRetryAction: null,
      canShowCertificateDataExportRetryCard: false,
      canShowCertificateDataExportRetryButton: false,
      canRequestCertificateDataExportRetry: false,
      canResolveCertificateDataExportRetry: false,
      canRefreshCertificateDataExportRetry: false,
      canBlockDashboardAccess: false,
      isLoginRequired: false,
      isLocalDashboardAccessAllowed: true,
      reason: "dashboard_certificate_data_export_retry_state_prepared_but_hidden_in_local_mode",
      futureStatuses: [
        "dashboard_certificate_data_export_retry_visible_later",
        "dashboard_certificate_data_export_retry_loading_later",
        "dashboard_certificate_data_export_retry_requested_later",
        "dashboard_certificate_data_export_retry_completed_later",
        "dashboard_certificate_data_export_retry_error_later"
      ],
      plannedDataExportRetryActions: [
        "certificate_data_export_retry_request_later",
        "certificate_data_export_retry_resolve_later",
        "certificate_data_export_retry_refresh_later"
      ],
      participantDashboardCertificateDataExportFileState,
      participantDashboardCertificateDataExportErrorState
    };
  }

  function getParticipantDashboardCertificateDataExportStatusSummaryState() {
    return {
      version: "v26.84a",
      status: "local_dashboard_certificate_data_export_status_summary_hidden",
      isAvailable: true,
      isVisible: false,
      canRender: false,
      canLoadCertificateDataExportStatusSummary: false,
      hasCertificateDataExportStatusSummaryData: false,
      certificateDataExportStatusSummaryItems: [],
      activeCertificateDataExportStatusSummaryId: null,
      latestCertificateDataExportOverallStatus: null,
      latestCertificateDataExportSummaryStatus: null,
      latestCertificateDataExportSummaryUpdatedAt: null,
      recommendedCertificateDataExportSummaryAction: null,
      canShowCertificateDataExportStatusSummaryCard: false,
      canShowCertificateDataExportStatusSummaryBadge: false,
      canComputeCertificateDataExportStatusSummary: false,
      canRefreshCertificateDataExportStatusSummary: false,
      canBlockDashboardAccess: false,
      isLoginRequired: false,
      isLocalDashboardAccessAllowed: true,
      reason: "dashboard_certificate_data_export_status_summary_state_prepared_but_hidden_in_local_mode",
      dependencyStatusMode: "reference_only_no_nested_state_execution",
      plannedSummarySources: [
        "certificate_data_export_file_state_later",
        "certificate_data_export_expiry_state_later",
        "certificate_data_export_download_log_state_later",
        "certificate_data_export_error_state_later",
        "certificate_data_export_retry_state_later"
      ],
      futureStatuses: [
        "dashboard_certificate_data_export_status_summary_visible_later",
        "dashboard_certificate_data_export_status_summary_loading_later",
        "dashboard_certificate_data_export_status_summary_ready_later",
        "dashboard_certificate_data_export_status_summary_empty_later",
        "dashboard_certificate_data_export_status_summary_error_later"
      ],
      plannedDataExportStatusSummaryActions: [
        "certificate_data_export_status_summary_compute_later",
        "certificate_data_export_status_summary_refresh_later",
        "certificate_data_export_status_summary_show_later"
      ]
    };
  }

  function getParticipantDashboardCertificateDataExportNotificationState() {
    return {
      version: "v26.85a",
      status: "local_dashboard_certificate_data_export_notification_hidden",
      isAvailable: true,
      isVisible: false,
      canRender: false,
      canLoadCertificateDataExportNotification: false,
      hasCertificateDataExportNotificationData: false,
      certificateDataExportNotificationEntries: [],
      activeCertificateDataExportNotificationId: null,
      latestCertificateDataExportNotificationStatus: null,
      latestCertificateDataExportNotificationChannel: null,
      latestCertificateDataExportNotificationSentAt: null,
      canShowCertificateDataExportNotificationCard: false,
      canSendCertificateDataExportNotification: false,
      canRefreshCertificateDataExportNotification: false,
      canBlockDashboardAccess: false,
      isLoginRequired: false,
      isLocalDashboardAccessAllowed: true,
      dependencyStatusMode: "reference_only_no_nested_state_execution",
      reason: "dashboard_certificate_data_export_notification_state_prepared_but_hidden_in_local_mode",
      plannedDataExportNotificationActions: [
        "certificate_data_export_notification_prepare_later",
        "certificate_data_export_notification_send_later",
        "certificate_data_export_notification_refresh_later"
      ]
    };
  }

  function getParticipantDashboardCertificateDataExportDeliveryStatusState() {
    return {
      version: "v26.86a",
      status: "local_dashboard_certificate_data_export_delivery_status_hidden",
      isAvailable: true,
      isVisible: false,
      canRender: false,
      canLoadCertificateDataExportDeliveryStatus: false,
      hasCertificateDataExportDeliveryStatusData: false,
      certificateDataExportDeliveryStatusEntries: [],
      activeCertificateDataExportDeliveryStatusId: null,
      latestCertificateDataExportDeliveryStatus: null,
      latestCertificateDataExportDeliveryChannel: null,
      latestCertificateDataExportDeliveredAt: null,
      canShowCertificateDataExportDeliveryStatusCard: false,
      canTrackCertificateDataExportDeliveryStatus: false,
      canRefreshCertificateDataExportDeliveryStatus: false,
      canBlockDashboardAccess: false,
      isLoginRequired: false,
      isLocalDashboardAccessAllowed: true,
      dependencyStatusMode: "reference_only_no_nested_state_execution",
      reason: "dashboard_certificate_data_export_delivery_status_state_prepared_but_hidden_in_local_mode",
      plannedDataExportDeliveryStatusActions: [
        "certificate_data_export_delivery_status_track_later",
        "certificate_data_export_delivery_status_refresh_later",
        "certificate_data_export_delivery_status_show_later"
      ]
    };
  }

  function getParticipantDashboardCertificateDataExportReadReceiptState() {
    return {
      version: "v26.87a",
      status: "local_dashboard_certificate_data_export_read_receipt_hidden",
      isAvailable: true,
      isVisible: false,
      canRender: false,
      canLoadCertificateDataExportReadReceipt: false,
      hasCertificateDataExportReadReceiptData: false,
      certificateDataExportReadReceiptEntries: [],
      activeCertificateDataExportReadReceiptId: null,
      latestCertificateDataExportReadReceiptStatus: null,
      latestCertificateDataExportReadAt: null,
      canShowCertificateDataExportReadReceiptCard: false,
      canTrackCertificateDataExportReadReceipt: false,
      canRefreshCertificateDataExportReadReceipt: false,
      canBlockDashboardAccess: false,
      isLoginRequired: false,
      isLocalDashboardAccessAllowed: true,
      dependencyStatusMode: "reference_only_no_nested_state_execution",
      reason: "dashboard_certificate_data_export_read_receipt_state_prepared_but_hidden_in_local_mode",
      plannedDataExportReadReceiptActions: [
        "certificate_data_export_read_receipt_track_later",
        "certificate_data_export_read_receipt_refresh_later",
        "certificate_data_export_read_receipt_show_later"
      ]
    };
  }

  function getParticipantDashboardCertificateDataExportCompletionStatusState() {
    return {
      version: "v26.88a",
      status: "local_dashboard_certificate_data_export_completion_status_hidden",
      isAvailable: true,
      isVisible: false,
      canRender: false,
      canLoadCertificateDataExportCompletionStatus: false,
      hasCertificateDataExportCompletionStatusData: false,
      certificateDataExportCompletionStatusEntries: [],
      activeCertificateDataExportCompletionStatusId: null,
      latestCertificateDataExportCompletionStatus: null,
      latestCertificateDataExportCompletedAt: null,
      canShowCertificateDataExportCompletionStatusCard: false,
      canTrackCertificateDataExportCompletionStatus: false,
      canRefreshCertificateDataExportCompletionStatus: false,
      canBlockDashboardAccess: false,
      isLoginRequired: false,
      isLocalDashboardAccessAllowed: true,
      dependencyStatusMode: "reference_only_no_nested_state_execution",
      reason: "dashboard_certificate_data_export_completion_status_state_prepared_but_hidden_in_local_mode",
      plannedDataExportCompletionStatusActions: [
        "certificate_data_export_completion_status_track_later",
        "certificate_data_export_completion_status_refresh_later",
        "certificate_data_export_completion_status_show_later"
      ]
    };
  }

  function getParticipantDashboardCertificateDataExportArchiveStatusState() {
    return {
      version: "v26.89a",
      status: "local_dashboard_certificate_data_export_archive_status_hidden",
      isAvailable: true,
      isVisible: false,
      canRender: false,
      canLoadCertificateDataExportArchiveStatus: false,
      hasCertificateDataExportArchiveStatusData: false,
      certificateDataExportArchiveStatusEntries: [],
      activeCertificateDataExportArchiveStatusId: null,
      latestCertificateDataExportArchiveStatus: null,
      latestCertificateDataExportArchivedAt: null,
      canShowCertificateDataExportArchiveStatusCard: false,
      canTrackCertificateDataExportArchiveStatus: false,
      canRefreshCertificateDataExportArchiveStatus: false,
      canBlockDashboardAccess: false,
      isLoginRequired: false,
      isLocalDashboardAccessAllowed: true,
      dependencyStatusMode: "reference_only_no_nested_state_execution",
      reason: "dashboard_certificate_data_export_archive_status_state_prepared_but_hidden_in_local_mode",
      plannedDataExportArchiveStatusActions: [
        "certificate_data_export_archive_status_track_later",
        "certificate_data_export_archive_status_refresh_later",
        "certificate_data_export_archive_status_show_later"
      ]
    };
  }

  function getParticipantDashboardCertificateDataExportDeletionStatusState() {
    return {
      version: "v26.90a",
      status: "local_dashboard_certificate_data_export_deletion_status_hidden",
      isAvailable: true,
      isVisible: false,
      canRender: false,
      canLoadCertificateDataExportDeletionStatus: false,
      hasCertificateDataExportDeletionStatusData: false,
      certificateDataExportDeletionStatusEntries: [],
      activeCertificateDataExportDeletionStatusId: null,
      latestCertificateDataExportDeletionStatus: null,
      latestCertificateDataExportDeletedAt: null,
      canShowCertificateDataExportDeletionStatusCard: false,
      canTrackCertificateDataExportDeletionStatus: false,
      canRefreshCertificateDataExportDeletionStatus: false,
      canBlockDashboardAccess: false,
      isLoginRequired: false,
      isLocalDashboardAccessAllowed: true,
      dependencyStatusMode: "reference_only_no_nested_state_execution",
      reason: "dashboard_certificate_data_export_deletion_status_state_prepared_but_hidden_in_local_mode",
      plannedDataExportDeletionStatusActions: [
        "certificate_data_export_deletion_status_track_later",
        "certificate_data_export_deletion_status_refresh_later",
        "certificate_data_export_deletion_status_show_later"
      ]
    };
  }

  function getParticipantDashboardCertificateDataExportRetentionStatusState() {
    return {
      version: "v26.91a",
      status: "local_dashboard_certificate_data_export_retention_status_hidden",
      isAvailable: true,
      isVisible: false,
      canRender: false,
      canLoadCertificateDataExportRetentionStatus: false,
      hasCertificateDataExportRetentionStatusData: false,
      certificateDataExportRetentionStatusEntries: [],
      activeCertificateDataExportRetentionStatusId: null,
      latestCertificateDataExportRetentionStatus: null,
      latestCertificateDataExportRetainedUntil: null,
      canShowCertificateDataExportRetentionStatusCard: false,
      canTrackCertificateDataExportRetentionStatus: false,
      canRefreshCertificateDataExportRetentionStatus: false,
      canBlockDashboardAccess: false,
      isLoginRequired: false,
      isLocalDashboardAccessAllowed: true,
      dependencyStatusMode: "reference_only_no_nested_state_execution",
      reason: "dashboard_certificate_data_export_retention_status_state_prepared_but_hidden_in_local_mode",
      plannedDataExportRetentionStatusActions: [
        "certificate_data_export_retention_status_track_later",
        "certificate_data_export_retention_status_refresh_later",
        "certificate_data_export_retention_status_show_later"
      ]
    };
  }

  function getParticipantDashboardCertificateDataExportSecurityStatusState() {
    return {
      version: "v26.92a",
      status: "local_dashboard_certificate_data_export_security_status_hidden",
      isAvailable: true,
      isVisible: false,
      canRender: false,
      canLoadCertificateDataExportSecurityStatus: false,
      hasCertificateDataExportSecurityStatusData: false,
      certificateDataExportSecurityStatusEntries: [],
      activeCertificateDataExportSecurityStatusId: null,
      latestCertificateDataExportSecurityStatus: null,
      latestCertificateDataExportSecurityCheckedAt: null,
      canShowCertificateDataExportSecurityStatusCard: false,
      canTrackCertificateDataExportSecurityStatus: false,
      canRefreshCertificateDataExportSecurityStatus: false,
      canBlockDashboardAccess: false,
      isLoginRequired: false,
      isLocalDashboardAccessAllowed: true,
      dependencyStatusMode: "reference_only_no_nested_state_execution",
      reason: "dashboard_certificate_data_export_security_status_state_prepared_but_hidden_in_local_mode",
      plannedDataExportSecurityStatusActions: [
        "certificate_data_export_security_status_track_later",
        "certificate_data_export_security_status_refresh_later",
        "certificate_data_export_security_status_show_later"
      ]
    };
  }

  function getParticipantDashboardCertificateDataExportIntegrityStatusState() {
    return {
      version: "v26.93a",
      status: "local_dashboard_certificate_data_export_integrity_status_hidden",
      isAvailable: true,
      isVisible: false,
      canRender: false,
      canLoadCertificateDataExportIntegrityStatus: false,
      hasCertificateDataExportIntegrityStatusData: false,
      certificateDataExportIntegrityStatusEntries: [],
      activeCertificateDataExportIntegrityStatusId: null,
      latestCertificateDataExportIntegrityStatus: null,
      latestCertificateDataExportIntegrityCheckedAt: null,
      canShowCertificateDataExportIntegrityStatusCard: false,
      canTrackCertificateDataExportIntegrityStatus: false,
      canRefreshCertificateDataExportIntegrityStatus: false,
      canBlockDashboardAccess: false,
      isLoginRequired: false,
      isLocalDashboardAccessAllowed: true,
      dependencyStatusMode: "reference_only_no_nested_state_execution",
      reason: "dashboard_certificate_data_export_integrity_status_state_prepared_but_hidden_in_local_mode",
      plannedDataExportIntegrityStatusActions: [
        "certificate_data_export_integrity_status_track_later",
        "certificate_data_export_integrity_status_refresh_later",
        "certificate_data_export_integrity_status_show_later"
      ]
    };
  }

  function getParticipantDashboardCertificateDataExportAuditStatusState() {
    return {
      version: "v26.94a",
      status: "local_dashboard_certificate_data_export_audit_status_hidden",
      isAvailable: true,
      isVisible: false,
      canRender: false,
      canLoadCertificateDataExportAuditStatus: false,
      hasCertificateDataExportAuditStatusData: false,
      certificateDataExportAuditStatusEntries: [],
      activeCertificateDataExportAuditStatusId: null,
      latestCertificateDataExportAuditStatus: null,
      latestCertificateDataExportAuditedAt: null,
      canShowCertificateDataExportAuditStatusCard: false,
      canTrackCertificateDataExportAuditStatus: false,
      canRefreshCertificateDataExportAuditStatus: false,
      canBlockDashboardAccess: false,
      isLoginRequired: false,
      isLocalDashboardAccessAllowed: true,
      dependencyStatusMode: "reference_only_no_nested_state_execution",
      reason: "dashboard_certificate_data_export_audit_status_state_prepared_but_hidden_in_local_mode",
      plannedDataExportAuditStatusActions: [
        "certificate_data_export_audit_status_track_later",
        "certificate_data_export_audit_status_refresh_later",
        "certificate_data_export_audit_status_show_later"
      ]
    };
  }

  function getParticipantDashboardCertificateDataExportAuditTrailStatusState() {
    return {
      version: "v26.95a",
      status: "local_dashboard_certificate_data_export_audit_trail_status_hidden",
      isAvailable: true,
      isVisible: false,
      canRender: false,
      canLoadCertificateDataExportAuditTrailStatus: false,
      hasCertificateDataExportAuditTrailStatusData: false,
      certificateDataExportAuditTrailStatusEntries: [],
      activeCertificateDataExportAuditTrailStatusId: null,
      latestCertificateDataExportAuditTrailStatus: null,
      latestCertificateDataExportAuditTrailCheckedAt: null,
      canShowCertificateDataExportAuditTrailStatusCard: false,
      canTrackCertificateDataExportAuditTrailStatus: false,
      canRefreshCertificateDataExportAuditTrailStatus: false,
      canBlockDashboardAccess: false,
      isLoginRequired: false,
      isLocalDashboardAccessAllowed: true,
      dependencyStatusMode: "reference_only_no_nested_state_execution",
      reason: "dashboard_certificate_data_export_audit_trail_status_state_prepared_but_hidden_in_local_mode",
      plannedDataExportAuditTrailStatusActions: [
        "certificate_data_export_audit_trail_status_track_later",
        "certificate_data_export_audit_trail_status_refresh_later",
        "certificate_data_export_audit_trail_status_show_later"
      ]
    };
  }

  function getParticipantDashboardCertificateDataExportApprovalStatusState() {
    return {
      version: "v26.96a",
      status: "local_dashboard_certificate_data_export_approval_status_hidden",
      isAvailable: true,
      isVisible: false,
      canRender: false,
      canLoadCertificateDataExportApprovalStatus: false,
      hasCertificateDataExportApprovalStatusData: false,
      certificateDataExportApprovalStatusEntries: [],
      activeCertificateDataExportApprovalStatusId: null,
      latestCertificateDataExportApprovalStatus: null,
      latestCertificateDataExportApprovedAt: null,
      canShowCertificateDataExportApprovalStatusCard: false,
      canTrackCertificateDataExportApprovalStatus: false,
      canRefreshCertificateDataExportApprovalStatus: false,
      canBlockDashboardAccess: false,
      isLoginRequired: false,
      isLocalDashboardAccessAllowed: true,
      dependencyStatusMode: "reference_only_no_nested_state_execution",
      reason: "dashboard_certificate_data_export_approval_status_state_prepared_but_hidden_in_local_mode",
      plannedDataExportApprovalStatusActions: [
        "certificate_data_export_approval_status_track_later",
        "certificate_data_export_approval_status_refresh_later",
        "certificate_data_export_approval_status_show_later"
      ]
    };
  }

  function getParticipantDashboardCertificateDataExportRejectionStatusState() {
    return {
      version: "v26.97a",
      status: "local_dashboard_certificate_data_export_rejection_status_hidden",
      isAvailable: true,
      isVisible: false,
      canRender: false,
      canLoadCertificateDataExportRejectionStatus: false,
      hasCertificateDataExportRejectionStatusData: false,
      certificateDataExportRejectionStatusEntries: [],
      activeCertificateDataExportRejectionStatusId: null,
      latestCertificateDataExportRejectionStatus: null,
      latestCertificateDataExportRejectedAt: null,
      canShowCertificateDataExportRejectionStatusCard: false,
      canTrackCertificateDataExportRejectionStatus: false,
      canRefreshCertificateDataExportRejectionStatus: false,
      canBlockDashboardAccess: false,
      isLoginRequired: false,
      isLocalDashboardAccessAllowed: true,
      dependencyStatusMode: "reference_only_no_nested_state_execution",
      reason: "dashboard_certificate_data_export_rejection_status_state_prepared_but_hidden_in_local_mode",
      plannedDataExportRejectionStatusActions: [
        "certificate_data_export_rejection_status_track_later",
        "certificate_data_export_rejection_status_refresh_later",
        "certificate_data_export_rejection_status_show_later"
      ]
    };
  }

  function getParticipantDashboardCertificateDataExportPendingStatusState() {
    return {
      version: "v26.98a",
      status: "local_dashboard_certificate_data_export_pending_status_hidden",
      isAvailable: true,
      isVisible: false,
      canRender: false,
      canLoadCertificateDataExportPendingStatus: false,
      hasCertificateDataExportPendingStatusData: false,
      certificateDataExportPendingStatusEntries: [],
      activeCertificateDataExportPendingStatusId: null,
      latestCertificateDataExportPendingStatus: null,
      latestCertificateDataExportPendingAt: null,
      canShowCertificateDataExportPendingStatusCard: false,
      canTrackCertificateDataExportPendingStatus: false,
      canRefreshCertificateDataExportPendingStatus: false,
      canBlockDashboardAccess: false,
      isLoginRequired: false,
      isLocalDashboardAccessAllowed: true,
      dependencyStatusMode: "reference_only_no_nested_state_execution",
      reason: "dashboard_certificate_data_export_pending_status_state_prepared_but_hidden_in_local_mode",
      plannedDataExportPendingStatusActions: [
        "certificate_data_export_pending_status_track_later",
        "certificate_data_export_pending_status_refresh_later",
        "certificate_data_export_pending_status_show_later"
      ]
    };
  }

  function getParticipantDashboardCertificateDataExportReviewStatusState() {
    return {
      version: "v26.99a",
      status: "local_dashboard_certificate_data_export_review_status_hidden",
      isAvailable: true,
      isVisible: false,
      canRender: false,
      canLoadCertificateDataExportReviewStatus: false,
      hasCertificateDataExportReviewStatusData: false,
      certificateDataExportReviewStatusEntries: [],
      activeCertificateDataExportReviewStatusId: null,
      latestCertificateDataExportReviewStatus: null,
      latestCertificateDataExportReviewedAt: null,
      canShowCertificateDataExportReviewStatusCard: false,
      canTrackCertificateDataExportReviewStatus: false,
      canRefreshCertificateDataExportReviewStatus: false,
      canBlockDashboardAccess: false,
      isLoginRequired: false,
      isLocalDashboardAccessAllowed: true,
      dependencyStatusMode: "reference_only_no_nested_state_execution",
      reason: "dashboard_certificate_data_export_review_status_state_prepared_but_hidden_in_local_mode",
      plannedDataExportReviewStatusActions: [
        "certificate_data_export_review_status_track_later",
        "certificate_data_export_review_status_refresh_later",
        "certificate_data_export_review_status_show_later"
      ]
    };
  }

  function getParticipantDashboardCertificateDataExportFinalStatusState() {
    return {
      version: "v27.00a",
      status: "local_dashboard_certificate_data_export_final_status_hidden",
      isAvailable: true,
      isVisible: false,
      canRender: false,
      canLoadCertificateDataExportFinalStatus: false,
      hasCertificateDataExportFinalStatusData: false,
      certificateDataExportFinalStatusEntries: [],
      activeCertificateDataExportFinalStatusId: null,
      latestCertificateDataExportFinalStatus: null,
      latestCertificateDataExportFinalizedAt: null,
      canShowCertificateDataExportFinalStatusCard: false,
      canTrackCertificateDataExportFinalStatus: false,
      canRefreshCertificateDataExportFinalStatus: false,
      canBlockDashboardAccess: false,
      isLoginRequired: false,
      isLocalDashboardAccessAllowed: true,
      dependencyStatusMode: "reference_only_no_nested_state_execution",
      reason: "dashboard_certificate_data_export_final_status_state_prepared_but_hidden_in_local_mode",
      plannedDataExportFinalStatusActions: [
        "certificate_data_export_final_status_track_later",
        "certificate_data_export_final_status_refresh_later",
        "certificate_data_export_final_status_show_later"
      ]
    };
  }

  function getParticipantDashboardCertificateDataExportHandoverStatusState() {
    return {
      version: "v27.01a",
      status: "local_dashboard_certificate_data_export_handover_status_hidden",
      isAvailable: true,
      isVisible: false,
      canRender: false,
      canLoadCertificateDataExportHandoverStatus: false,
      hasCertificateDataExportHandoverStatusData: false,
      certificateDataExportHandoverStatusEntries: [],
      activeCertificateDataExportHandoverStatusId: null,
      latestCertificateDataExportHandoverStatus: null,
      latestCertificateDataExportHandedOverAt: null,
      canShowCertificateDataExportHandoverStatusCard: false,
      canTrackCertificateDataExportHandoverStatus: false,
      canRefreshCertificateDataExportHandoverStatus: false,
      canBlockDashboardAccess: false,
      isLoginRequired: false,
      isLocalDashboardAccessAllowed: true,
      dependencyStatusMode: "reference_only_no_nested_state_execution",
      reason: "dashboard_certificate_data_export_handover_status_state_prepared_but_hidden_in_local_mode",
      plannedDataExportHandoverStatusActions: [
        "certificate_data_export_handover_status_track_later",
        "certificate_data_export_handover_status_refresh_later",
        "certificate_data_export_handover_status_show_later"
      ]
    };
  }

  function getParticipantDashboardCertificateDataExportReceptionStatusState() {
    return {
      version: "v27.02a",
      status: "local_dashboard_certificate_data_export_reception_status_hidden",
      isAvailable: true,
      isVisible: false,
      canRender: false,
      canLoadCertificateDataExportReceptionStatus: false,
      hasCertificateDataExportReceptionStatusData: false,
      certificateDataExportReceptionStatusEntries: [],
      activeCertificateDataExportReceptionStatusId: null,
      latestCertificateDataExportReceptionStatus: null,
      latestCertificateDataExportReceivedAt: null,
      canShowCertificateDataExportReceptionStatusCard: false,
      canTrackCertificateDataExportReceptionStatus: false,
      canRefreshCertificateDataExportReceptionStatus: false,
      canBlockDashboardAccess: false,
      isLoginRequired: false,
      isLocalDashboardAccessAllowed: true,
      dependencyStatusMode: "reference_only_no_nested_state_execution",
      reason: "dashboard_certificate_data_export_reception_status_state_prepared_but_hidden_in_local_mode",
      plannedDataExportReceptionStatusActions: [
        "certificate_data_export_reception_status_track_later",
        "certificate_data_export_reception_status_refresh_later",
        "certificate_data_export_reception_status_show_later"
      ]
    };
  }

  function getParticipantDashboardCertificateDataExportConfirmationStatusState() {
    return {
      version: "v27.03a",
      status: "local_dashboard_certificate_data_export_confirmation_status_hidden",
      isAvailable: true,
      isVisible: false,
      canRender: false,
      canLoadCertificateDataExportConfirmationStatus: false,
      hasCertificateDataExportConfirmationStatusData: false,
      certificateDataExportConfirmationStatusEntries: [],
      activeCertificateDataExportConfirmationStatusId: null,
      latestCertificateDataExportConfirmationStatus: null,
      latestCertificateDataExportConfirmedAt: null,
      canShowCertificateDataExportConfirmationStatusCard: false,
      canTrackCertificateDataExportConfirmationStatus: false,
      canRefreshCertificateDataExportConfirmationStatus: false,
      canBlockDashboardAccess: false,
      isLoginRequired: false,
      isLocalDashboardAccessAllowed: true,
      dependencyStatusMode: "reference_only_no_nested_state_execution",
      reason: "dashboard_certificate_data_export_confirmation_status_state_prepared_but_hidden_in_local_mode",
      plannedDataExportConfirmationStatusActions: [
        "certificate_data_export_confirmation_status_track_later",
        "certificate_data_export_confirmation_status_refresh_later",
        "certificate_data_export_confirmation_status_show_later"
      ]
    };
  }

  function getParticipantDashboardCertificateDataExportReleaseStatusState() {
    return {
      version: "v27.04a",
      status: "local_dashboard_certificate_data_export_release_status_hidden",
      isAvailable: true,
      isVisible: false,
      canRender: false,
      canLoadCertificateDataExportReleaseStatus: false,
      hasCertificateDataExportReleaseStatusData: false,
      certificateDataExportReleaseStatusEntries: [],
      activeCertificateDataExportReleaseStatusId: null,
      latestCertificateDataExportReleaseStatus: null,
      latestCertificateDataExportReleasedAt: null,
      canShowCertificateDataExportReleaseStatusCard: false,
      canTrackCertificateDataExportReleaseStatus: false,
      canRefreshCertificateDataExportReleaseStatus: false,
      canBlockDashboardAccess: false,
      isLoginRequired: false,
      isLocalDashboardAccessAllowed: true,
      dependencyStatusMode: "reference_only_no_nested_state_execution",
      reason: "dashboard_certificate_data_export_release_status_state_prepared_but_hidden_in_local_mode",
      plannedDataExportReleaseStatusActions: [
        "certificate_data_export_release_status_track_later",
        "certificate_data_export_release_status_refresh_later",
        "certificate_data_export_release_status_show_later"
      ]
    };
  }

  function getParticipantDashboardCertificateDataExportRetrievalStatusState() {
    return {
      version: "v27.05a",
      status: "local_dashboard_certificate_data_export_retrieval_status_hidden",
      isAvailable: true,
      isVisible: false,
      canRender: false,
      canLoadCertificateDataExportRetrievalStatus: false,
      hasCertificateDataExportRetrievalStatusData: false,
      certificateDataExportRetrievalStatusEntries: [],
      activeCertificateDataExportRetrievalStatusId: null,
      latestCertificateDataExportRetrievalStatus: null,
      latestCertificateDataExportRetrievedAt: null,
      canShowCertificateDataExportRetrievalStatusCard: false,
      canTrackCertificateDataExportRetrievalStatus: false,
      canRefreshCertificateDataExportRetrievalStatus: false,
      canBlockDashboardAccess: false,
      isLoginRequired: false,
      isLocalDashboardAccessAllowed: true,
      dependencyStatusMode: "reference_only_no_nested_state_execution",
      reason: "dashboard_certificate_data_export_retrieval_status_state_prepared_but_hidden_in_local_mode",
      plannedDataExportRetrievalStatusActions: [
        "certificate_data_export_retrieval_status_track_later",
        "certificate_data_export_retrieval_status_refresh_later",
        "certificate_data_export_retrieval_status_show_later"
      ]
    };
  }

  function getParticipantDashboardCertificateDataExportProtocolStatusState() {
    return {
      version: "v27.06a",
      status: "local_dashboard_certificate_data_export_protocol_status_hidden",
      isAvailable: true,
      isVisible: false,
      canRender: false,
      canLoadCertificateDataExportProtocolStatus: false,
      hasCertificateDataExportProtocolStatusData: false,
      certificateDataExportProtocolStatusEntries: [],
      activeCertificateDataExportProtocolStatusId: null,
      latestCertificateDataExportProtocolStatus: null,
      latestCertificateDataExportProtocolUpdatedAt: null,
      canShowCertificateDataExportProtocolStatusCard: false,
      canTrackCertificateDataExportProtocolStatus: false,
      canRefreshCertificateDataExportProtocolStatus: false,
      canBlockDashboardAccess: false,
      isLoginRequired: false,
      isLocalDashboardAccessAllowed: true,
      dependencyStatusMode: "reference_only_no_nested_state_execution",
      reason: "dashboard_certificate_data_export_protocol_status_state_prepared_but_hidden_in_local_mode",
      plannedDataExportProtocolStatusActions: [
        "certificate_data_export_protocol_status_track_later",
        "certificate_data_export_protocol_status_refresh_later",
        "certificate_data_export_protocol_status_show_later"
      ]
    };
  }

  function getParticipantDashboardCertificateDataExportHandoverProtocolStatusState() {
    return {
      version: "v27.07a",
      status: "local_dashboard_certificate_data_export_handover_protocol_status_hidden",
      isAvailable: true,
      isVisible: false,
      canRender: false,
      canLoadCertificateDataExportHandoverProtocolStatus: false,
      hasCertificateDataExportHandoverProtocolStatusData: false,
      certificateDataExportHandoverProtocolStatusEntries: [],
      activeCertificateDataExportHandoverProtocolStatusId: null,
      latestCertificateDataExportHandoverProtocolStatus: null,
      latestCertificateDataExportHandoverProtocolUpdatedAt: null,
      canShowCertificateDataExportHandoverProtocolStatusCard: false,
      canTrackCertificateDataExportHandoverProtocolStatus: false,
      canRefreshCertificateDataExportHandoverProtocolStatus: false,
      canBlockDashboardAccess: false,
      isLoginRequired: false,
      isLocalDashboardAccessAllowed: true,
      dependencyStatusMode: "reference_only_no_nested_state_execution",
      reason: "dashboard_certificate_data_export_handover_protocol_status_state_prepared_but_hidden_in_local_mode",
      plannedDataExportHandoverProtocolStatusActions: [
        "certificate_data_export_handover_protocol_status_track_later",
        "certificate_data_export_handover_protocol_status_refresh_later",
        "certificate_data_export_handover_protocol_status_show_later"
      ]
    };
  }

  function getParticipantDashboardCertificateDataExportCompletionProtocolStatusState() {
    return {
      version: "v27.08a",
      status: "local_dashboard_certificate_data_export_completion_protocol_status_hidden",
      isAvailable: true,
      isVisible: false,
      canRender: false,
      canLoadCertificateDataExportCompletionProtocolStatus: false,
      hasCertificateDataExportCompletionProtocolStatusData: false,
      certificateDataExportCompletionProtocolStatusEntries: [],
      activeCertificateDataExportCompletionProtocolStatusId: null,
      latestCertificateDataExportCompletionProtocolStatus: null,
      latestCertificateDataExportCompletionProtocolUpdatedAt: null,
      canShowCertificateDataExportCompletionProtocolStatusCard: false,
      canTrackCertificateDataExportCompletionProtocolStatus: false,
      canRefreshCertificateDataExportCompletionProtocolStatus: false,
      canBlockDashboardAccess: false,
      isLoginRequired: false,
      isLocalDashboardAccessAllowed: true,
      dependencyStatusMode: "reference_only_no_nested_state_execution",
      reason: "dashboard_certificate_data_export_completion_protocol_status_state_prepared_but_hidden_in_local_mode",
      plannedDataExportCompletionProtocolStatusActions: [
        "certificate_data_export_completion_protocol_status_track_later",
        "certificate_data_export_completion_protocol_status_refresh_later",
        "certificate_data_export_completion_protocol_status_show_later"
      ]
    };
  }

  function getParticipantDashboardCertificateDataExportFinalProofStatusState() {
    return {
      version: "v27.09a",
      status: "local_dashboard_certificate_data_export_final_proof_status_hidden",
      isAvailable: true,
      isVisible: false,
      canRender: false,
      canLoadCertificateDataExportFinalProofStatus: false,
      hasCertificateDataExportFinalProofStatusData: false,
      certificateDataExportFinalProofStatusEntries: [],
      activeCertificateDataExportFinalProofStatusId: null,
      latestCertificateDataExportFinalProofStatus: null,
      latestCertificateDataExportFinalProofUpdatedAt: null,
      canShowCertificateDataExportFinalProofStatusCard: false,
      canTrackCertificateDataExportFinalProofStatus: false,
      canRefreshCertificateDataExportFinalProofStatus: false,
      canBlockDashboardAccess: false,
      isLoginRequired: false,
      isLocalDashboardAccessAllowed: true,
      dependencyStatusMode: "reference_only_no_nested_state_execution",
      reason: "dashboard_certificate_data_export_final_proof_status_state_prepared_but_hidden_in_local_mode",
      plannedDataExportFinalProofStatusActions: [
        "certificate_data_export_final_proof_status_track_later",
        "certificate_data_export_final_proof_status_refresh_later",
        "certificate_data_export_final_proof_status_show_later"
      ]
    };
  }

  function getParticipantDashboardCertificateDataExportSubmissionConfirmationStatusState() {
    return {
      version: "v27.10a",
      status: "local_dashboard_certificate_data_export_submission_confirmation_status_hidden",
      isAvailable: true,
      isVisible: false,
      canRender: false,
      canLoadCertificateDataExportSubmissionConfirmationStatus: false,
      hasCertificateDataExportSubmissionConfirmationStatusData: false,
      certificateDataExportSubmissionConfirmationStatusEntries: [],
      activeCertificateDataExportSubmissionConfirmationStatusId: null,
      latestCertificateDataExportSubmissionConfirmationStatus: null,
      latestCertificateDataExportSubmissionConfirmationUpdatedAt: null,
      canShowCertificateDataExportSubmissionConfirmationStatusCard: false,
      canTrackCertificateDataExportSubmissionConfirmationStatus: false,
      canRefreshCertificateDataExportSubmissionConfirmationStatus: false,
      canBlockDashboardAccess: false,
      isLoginRequired: false,
      isLocalDashboardAccessAllowed: true,
      dependencyStatusMode: "reference_only_no_nested_state_execution",
      reason: "dashboard_certificate_data_export_submission_confirmation_status_state_prepared_but_hidden_in_local_mode",
      plannedDataExportSubmissionConfirmationStatusActions: [
        "certificate_data_export_submission_confirmation_status_track_later",
        "certificate_data_export_submission_confirmation_status_refresh_later",
        "certificate_data_export_submission_confirmation_status_show_later"
      ]
    };
  }

  function getParticipantDashboardCertificateDataExportReceiptConfirmationStatusState() {
    return {
      version: "v27.11a",
      status: "local_dashboard_certificate_data_export_receipt_confirmation_status_hidden",
      isAvailable: true,
      isVisible: false,
      canRender: false,
      canLoadCertificateDataExportReceiptConfirmationStatus: false,
      hasCertificateDataExportReceiptConfirmationStatusData: false,
      certificateDataExportReceiptConfirmationStatusEntries: [],
      activeCertificateDataExportReceiptConfirmationStatusId: null,
      latestCertificateDataExportReceiptConfirmationStatus: null,
      latestCertificateDataExportReceiptConfirmationUpdatedAt: null,
      canShowCertificateDataExportReceiptConfirmationStatusCard: false,
      canTrackCertificateDataExportReceiptConfirmationStatus: false,
      canRefreshCertificateDataExportReceiptConfirmationStatus: false,
      canBlockDashboardAccess: false,
      isLoginRequired: false,
      isLocalDashboardAccessAllowed: true,
      dependencyStatusMode: "reference_only_no_nested_state_execution",
      reason: "dashboard_certificate_data_export_receipt_confirmation_status_state_prepared_but_hidden_in_local_mode",
      plannedDataExportReceiptConfirmationStatusActions: [
        "certificate_data_export_receipt_confirmation_status_track_later",
        "certificate_data_export_receipt_confirmation_status_refresh_later",
        "certificate_data_export_receipt_confirmation_status_show_later"
      ]
    };
  }

  function getParticipantDashboardCertificateDataExportDeliveryProofStatusState() {
    return {
      version: "v27.12a",
      status: "local_dashboard_certificate_data_export_delivery_proof_status_hidden",
      isAvailable: true,
      isVisible: false,
      canRender: false,
      canLoadCertificateDataExportDeliveryProofStatus: false,
      hasCertificateDataExportDeliveryProofStatusData: false,
      certificateDataExportDeliveryProofStatusEntries: [],
      activeCertificateDataExportDeliveryProofStatusId: null,
      latestCertificateDataExportDeliveryProofStatus: null,
      latestCertificateDataExportDeliveryProofUpdatedAt: null,
      canShowCertificateDataExportDeliveryProofStatusCard: false,
      canTrackCertificateDataExportDeliveryProofStatus: false,
      canRefreshCertificateDataExportDeliveryProofStatus: false,
      canBlockDashboardAccess: false,
      isLoginRequired: false,
      isLocalDashboardAccessAllowed: true,
      dependencyStatusMode: "reference_only_no_nested_state_execution",
      reason: "dashboard_certificate_data_export_delivery_proof_status_state_prepared_but_hidden_in_local_mode",
      plannedDataExportDeliveryProofStatusActions: [
        "certificate_data_export_delivery_proof_status_track_later",
        "certificate_data_export_delivery_proof_status_refresh_later",
        "certificate_data_export_delivery_proof_status_show_later"
      ]
    };
  }

  function getParticipantDashboardCertificateDataExportProofArchiveStatusState() {
    return {
      version: "v27.13a",
      status: "local_dashboard_certificate_data_export_proof_archive_status_hidden",
      isAvailable: true,
      isVisible: false,
      canRender: false,
      canLoadCertificateDataExportProofArchiveStatus: false,
      hasCertificateDataExportProofArchiveStatusData: false,
      certificateDataExportProofArchiveStatusEntries: [],
      activeCertificateDataExportProofArchiveStatusId: null,
      latestCertificateDataExportProofArchiveStatus: null,
      latestCertificateDataExportProofArchiveUpdatedAt: null,
      canShowCertificateDataExportProofArchiveStatusCard: false,
      canTrackCertificateDataExportProofArchiveStatus: false,
      canRefreshCertificateDataExportProofArchiveStatus: false,
      canBlockDashboardAccess: false,
      isLoginRequired: false,
      isLocalDashboardAccessAllowed: true,
      dependencyStatusMode: "reference_only_no_nested_state_execution",
      reason: "dashboard_certificate_data_export_proof_archive_status_state_prepared_but_hidden_in_local_mode",
      plannedDataExportProofArchiveStatusActions: [
        "certificate_data_export_proof_archive_status_track_later",
        "certificate_data_export_proof_archive_status_refresh_later",
        "certificate_data_export_proof_archive_status_show_later"
      ]
    };
  }

  function getParticipantDashboardCertificateDataExportProofReleaseStatusState() {
    return {
      version: "v27.14a",
      status: "local_dashboard_certificate_data_export_proof_release_status_hidden",
      isAvailable: true,
      isVisible: false,
      canRender: false,
      canLoadCertificateDataExportProofReleaseStatus: false,
      hasCertificateDataExportProofReleaseStatusData: false,
      certificateDataExportProofReleaseStatusEntries: [],
      activeCertificateDataExportProofReleaseStatusId: null,
      latestCertificateDataExportProofReleaseStatus: null,
      latestCertificateDataExportProofReleaseUpdatedAt: null,
      canShowCertificateDataExportProofReleaseStatusCard: false,
      canTrackCertificateDataExportProofReleaseStatus: false,
      canRefreshCertificateDataExportProofReleaseStatus: false,
      canBlockDashboardAccess: false,
      isLoginRequired: false,
      isLocalDashboardAccessAllowed: true,
      dependencyStatusMode: "reference_only_no_nested_state_execution",
      reason: "dashboard_certificate_data_export_proof_release_status_state_prepared_but_hidden_in_local_mode",
      plannedDataExportProofReleaseStatusActions: [
        "certificate_data_export_proof_release_status_track_later",
        "certificate_data_export_proof_release_status_refresh_later",
        "certificate_data_export_proof_release_status_show_later"
      ]
    };
  }

  function getParticipantDashboardCertificateDataExportProofBlockStatusState() {
    return {
      version: "v27.15a",
      status: "local_dashboard_certificate_data_export_proof_block_status_hidden",
      isAvailable: true,
      isVisible: false,
      canRender: false,
      canLoadCertificateDataExportProofBlockStatus: false,
      hasCertificateDataExportProofBlockStatusData: false,
      certificateDataExportProofBlockStatusEntries: [],
      activeCertificateDataExportProofBlockStatusId: null,
      latestCertificateDataExportProofBlockStatus: null,
      latestCertificateDataExportProofBlockUpdatedAt: null,
      canShowCertificateDataExportProofBlockStatusCard: false,
      canTrackCertificateDataExportProofBlockStatus: false,
      canRefreshCertificateDataExportProofBlockStatus: false,
      canBlockDashboardAccess: false,
      isLoginRequired: false,
      isLocalDashboardAccessAllowed: true,
      dependencyStatusMode: "reference_only_no_nested_state_execution",
      reason: "dashboard_certificate_data_export_proof_block_status_state_prepared_but_hidden_in_local_mode",
      plannedDataExportProofBlockStatusActions: [
        "certificate_data_export_proof_block_status_track_later",
        "certificate_data_export_proof_block_status_refresh_later",
        "certificate_data_export_proof_block_status_show_later"
      ]
    };
  }

  function getParticipantDashboardCertificateDataExportProofCheckStatusState() {
    return {
      version: "v27.16a",
      status: "local_dashboard_certificate_data_export_proof_check_status_hidden",
      isAvailable: true,
      isVisible: false,
      canRender: false,
      canLoadCertificateDataExportProofCheckStatus: false,
      hasCertificateDataExportProofCheckStatusData: false,
      certificateDataExportProofCheckStatusEntries: [],
      activeCertificateDataExportProofCheckStatusId: null,
      latestCertificateDataExportProofCheckStatus: null,
      latestCertificateDataExportProofCheckUpdatedAt: null,
      canShowCertificateDataExportProofCheckStatusCard: false,
      canTrackCertificateDataExportProofCheckStatus: false,
      canRefreshCertificateDataExportProofCheckStatus: false,
      canBlockDashboardAccess: false,
      isLoginRequired: false,
      isLocalDashboardAccessAllowed: true,
      dependencyStatusMode: "reference_only_no_nested_state_execution",
      reason: "dashboard_certificate_data_export_proof_check_status_state_prepared_but_hidden_in_local_mode",
      plannedDataExportProofCheckStatusActions: [
        "certificate_data_export_proof_check_status_track_later",
        "certificate_data_export_proof_check_status_refresh_later",
        "certificate_data_export_proof_check_status_show_later"
      ]
    };
  }

  function getParticipantDashboardCertificateDataExportProofValidationStatusState() {
    return {
      version: "v27.17a",
      status: "local_dashboard_certificate_data_export_proof_validation_status_hidden",
      isAvailable: true,
      isVisible: false,
      canRender: false,
      canLoadCertificateDataExportProofValidationStatus: false,
      hasCertificateDataExportProofValidationStatusData: false,
      certificateDataExportProofValidationStatusEntries: [],
      activeCertificateDataExportProofValidationStatusId: null,
      latestCertificateDataExportProofValidationStatus: null,
      latestCertificateDataExportProofValidationUpdatedAt: null,
      canShowCertificateDataExportProofValidationStatusCard: false,
      canTrackCertificateDataExportProofValidationStatus: false,
      canRefreshCertificateDataExportProofValidationStatus: false,
      canBlockDashboardAccess: false,
      isLoginRequired: false,
      isLocalDashboardAccessAllowed: true,
      dependencyStatusMode: "reference_only_no_nested_state_execution",
      reason: "dashboard_certificate_data_export_proof_validation_status_state_prepared_but_hidden_in_local_mode",
      plannedDataExportProofValidationStatusActions: [
        "certificate_data_export_proof_validation_status_track_later",
        "certificate_data_export_proof_validation_status_refresh_later",
        "certificate_data_export_proof_validation_status_show_later"
      ]
    };
  }

  function getParticipantDashboardCertificateDataExportProofReleaseCheckStatusState() {
    return {
      version: "v27.18a",
      status: "local_dashboard_certificate_data_export_proof_release_check_status_hidden",
      isAvailable: true,
      isVisible: false,
      canRender: false,
      canLoadCertificateDataExportProofReleaseCheckStatus: false,
      hasCertificateDataExportProofReleaseCheckStatusData: false,
      certificateDataExportProofReleaseCheckStatusEntries: [],
      activeCertificateDataExportProofReleaseCheckStatusId: null,
      latestCertificateDataExportProofReleaseCheckStatus: null,
      latestCertificateDataExportProofReleaseCheckUpdatedAt: null,
      canShowCertificateDataExportProofReleaseCheckStatusCard: false,
      canTrackCertificateDataExportProofReleaseCheckStatus: false,
      canRefreshCertificateDataExportProofReleaseCheckStatus: false,
      canBlockDashboardAccess: false,
      isLoginRequired: false,
      isLocalDashboardAccessAllowed: true,
      dependencyStatusMode: "reference_only_no_nested_state_execution",
      reason: "dashboard_certificate_data_export_proof_release_check_status_state_prepared_but_hidden_in_local_mode",
      plannedDataExportProofReleaseCheckStatusActions: [
        "certificate_data_export_proof_release_check_status_track_later",
        "certificate_data_export_proof_release_check_status_refresh_later",
        "certificate_data_export_proof_release_check_status_show_later"
      ]
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
    const loginSuccessState = getLoginSuccessState();
    const logoutState = getLogoutState();
    const participantDashboardAuthState = getParticipantDashboardAuthState();
    const participantDashboardCourseAccessState = getParticipantDashboardCourseAccessState();
    const participantDashboardExpiryState = getParticipantDashboardExpiryState();
    const participantDashboardAccessDecisionState = getParticipantDashboardAccessDecisionState();
    const participantDashboardReadinessState = getParticipantDashboardReadinessState();
    const participantDashboardStatusBadgeState = getParticipantDashboardStatusBadgeState();
    const participantDashboardNoticeBannerState = getParticipantDashboardNoticeBannerState();
    const participantDashboardProfileHeaderState = getParticipantDashboardProfileHeaderState();
    const participantDashboardCourseCardState = getParticipantDashboardCourseCardState();
    const participantDashboardProgressState = getParticipantDashboardProgressState();
    const participantDashboardActivityListState = getParticipantDashboardActivityListState();
    const participantDashboardRecommendationsState = getParticipantDashboardRecommendationsState();
    const participantDashboardExamStatusState = getParticipantDashboardExamStatusState();
    const participantDashboardCertificateState = getParticipantDashboardCertificateState();
    const participantDashboardDocumentsState = getParticipantDashboardDocumentsState();
    const participantDashboardMessagesState = getParticipantDashboardMessagesState();
    const participantDashboardSupportState = getParticipantDashboardSupportState();
    const participantDashboardAppointmentsState = getParticipantDashboardAppointmentsState();
    const participantDashboardPaymentStatusState = getParticipantDashboardPaymentStatusState();
    const participantDashboardContractStatusState = getParticipantDashboardContractStatusState();
    const participantDashboardInvoicesState = getParticipantDashboardInvoicesState();
    const participantDashboardAttendanceState = getParticipantDashboardAttendanceState();
    const participantDashboardLessonPlanState = getParticipantDashboardLessonPlanState();
    const participantDashboardCourseMaterialsState = getParticipantDashboardCourseMaterialsState();
    const participantDashboardLearningProgressDetailsState = getParticipantDashboardLearningProgressDetailsState();
    const participantDashboardMistakeTrainingDetailsState = getParticipantDashboardMistakeTrainingDetailsState();
    const participantDashboardExamSimulationDetailsState = getParticipantDashboardExamSimulationDetailsState();
    const participantDashboardOralExamDetailsState = getParticipantDashboardOralExamDetailsState();
    const participantDashboardFlashcardsDetailsState = getParticipantDashboardFlashcardsDetailsState();
    const participantDashboardSampleQuestionsDetailsState = getParticipantDashboardSampleQuestionsDetailsState();
    const participantDashboardExamHistoryState = getParticipantDashboardExamHistoryState();
    const participantDashboardExamHistoryDataSourceState = getParticipantDashboardExamHistoryDataSourceState();
    const participantExamResultHistoryRpcState = getParticipantExamResultHistoryRpcState();
    const participantDashboardCertificateHistoryState = getParticipantDashboardCertificateHistoryState();
    const participantDashboardCertificateDownloadState = getParticipantDashboardCertificateDownloadState();
    const participantDashboardCertificatePreviewState = getParticipantDashboardCertificatePreviewState();
    const participantDashboardCertificatePrintState = getParticipantDashboardCertificatePrintState();
    const participantDashboardCertificateShareState = getParticipantDashboardCertificateShareState();
    const participantDashboardCertificateVerificationState = getParticipantDashboardCertificateVerificationState();
    const participantDashboardCertificateQrCodeState = getParticipantDashboardCertificateQrCodeState();
    const participantDashboardCertificateValidityState = getParticipantDashboardCertificateValidityState();
    const participantDashboardCertificateRevocationState = getParticipantDashboardCertificateRevocationState();
    const participantDashboardCertificateAuditLogState = getParticipantDashboardCertificateAuditLogState();
    const participantDashboardCertificateConsentState = getParticipantDashboardCertificateConsentState();
    const participantDashboardCertificatePrivacyNoticeState = getParticipantDashboardCertificatePrivacyNoticeState();
    const participantDashboardCertificateRetentionState = getParticipantDashboardCertificateRetentionState();
    const participantDashboardCertificateDataAccessState = getParticipantDashboardCertificateDataAccessState();
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
      version: "v26.63a",
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
      loginSuccessStatus: loginSuccessState.status,
      hasLoginSuccess: loginSuccessState.hasSuccess === true,
      hasLoginSuccessSession: loginSuccessState.hasSession === true,
      canFinalizeLogin: loginSuccessState.canFinalizeLogin === true,
      canRedirectAfterLogin: loginSuccessState.canRedirectAfterLogin === true,
      loginSuccessRedirectTarget: loginSuccessState.redirectTarget,
      logoutStatus: logoutState.status,
      isLogoutAvailable: logoutState.isAvailable === true,
      canLogout: logoutState.canLogout === true,
      canClearSessionOnLogout: logoutState.canClearSession === true,
      hasActiveSessionForLogout: logoutState.hasActiveSession === true,
      isLogoutRequired: logoutState.isLogoutRequired === true,
      participantDashboardAuthStatus: participantDashboardAuthState.status,
      isParticipantDashboardAuthVisible: participantDashboardAuthState.isVisible === true,
      canRenderParticipantDashboardAuth: participantDashboardAuthState.canRender === true,
      isParticipantDashboardAuthRequired: participantDashboardAuthState.isAuthRequired === true,
      canBlockParticipantDashboardAccess: participantDashboardAuthState.canBlockDashboardAccess === true,
      hasParticipantDashboardAuthSession: participantDashboardAuthState.hasActiveSession === true,
      canShowParticipantIdentity: participantDashboardAuthState.canShowParticipantIdentity === true,
      canShowLogoutAction: participantDashboardAuthState.canShowLogoutAction === true,
      isLocalDashboardAccessAllowed: participantDashboardAuthState.isLocalDashboardAccessAllowed === true,
      participantDashboardCourseAccessStatus: participantDashboardCourseAccessState.status,
      isParticipantDashboardCourseAccessRequired: participantDashboardCourseAccessState.isCourseAccessRequired === true,
      canCheckParticipantDashboardCourseAccess: participantDashboardCourseAccessState.canCheckCourseAccess === true,
      canBlockParticipantDashboardCourseAccess: participantDashboardCourseAccessState.canBlockCourseAccess === true,
      hasAssignedDashboardCourse: participantDashboardCourseAccessState.hasAssignedCourse === true,
      canShowDashboardCourseLock: participantDashboardCourseAccessState.canShowCourseLock === true,
      canShowDashboardCourseAccessWarning: participantDashboardCourseAccessState.canShowCourseAccessWarning === true,
      isLocalDashboardCourseAccessAllowed: participantDashboardCourseAccessState.isLocalDashboardCourseAccessAllowed === true,
      participantDashboardExpiryStatus: participantDashboardExpiryState.status,
      isParticipantDashboardExpiryCheckRequired: participantDashboardExpiryState.isExpiryCheckRequired === true,
      canCheckParticipantDashboardExpiry: participantDashboardExpiryState.canCheckExpiry === true,
      canBlockParticipantDashboardOnExpiry: participantDashboardExpiryState.canBlockOnExpiry === true,
      hasParticipantDashboardExpiryDate: participantDashboardExpiryState.hasExpiryDate === true,
      participantDashboardExpiresAt: participantDashboardExpiryState.expiresAt,
      isParticipantDashboardExpired: participantDashboardExpiryState.isExpired === true,
      participantDashboardDaysRemaining: participantDashboardExpiryState.daysRemaining,
      canShowParticipantDashboardExpiryWarning: participantDashboardExpiryState.canShowExpiryWarning === true,
      isLocalDashboardExpiryAccessAllowed: participantDashboardExpiryState.isLocalDashboardExpiryAccessAllowed === true,
      participantDashboardAccessDecisionStatus: participantDashboardAccessDecisionState.status,
      isParticipantDashboardAccessDecisionAvailable: participantDashboardAccessDecisionState.isDecisionAvailable === true,
      isParticipantDashboardAccessAllowed: participantDashboardAccessDecisionState.isDashboardAccessAllowed === true,
      canBlockParticipantDashboardByDecision: participantDashboardAccessDecisionState.canBlockDashboardAccess === true,
      participantDashboardAccessBlockReason: participantDashboardAccessDecisionState.blockReason,
      isParticipantDashboardAccessAuthCheckRequired: participantDashboardAccessDecisionState.requiredChecks.auth === true,
      isParticipantDashboardAccessCourseCheckRequired: participantDashboardAccessDecisionState.requiredChecks.courseAccess === true,
      isParticipantDashboardAccessExpiryCheckRequired: participantDashboardAccessDecisionState.requiredChecks.expiry === true,
      participantDashboardReadinessStatus: participantDashboardReadinessState.status,
      isParticipantDashboardReadinessAvailable: participantDashboardReadinessState.isReadinessAvailable === true,
      isParticipantDashboardReady: participantDashboardReadinessState.isReady === true,
      canRenderParticipantDashboard: participantDashboardReadinessState.canRenderDashboard === true,
      canStartLocalParticipantDashboard: participantDashboardReadinessState.canStartLocalDashboard === true,
      isParticipantDashboardLoginRequired: participantDashboardReadinessState.isLoginRequired === true,
      canBlockParticipantDashboardByReadiness: participantDashboardReadinessState.canBlockDashboardAccess === true,
      participantDashboardReadinessBlockReason: participantDashboardReadinessState.blockReason,
      isLocalParticipantDashboardReady: participantDashboardReadinessState.isLocalDashboardAccessAllowed === true,
      participantDashboardStatusBadgeStatus: participantDashboardStatusBadgeState.status,
      isParticipantDashboardStatusBadgeAvailable: participantDashboardStatusBadgeState.isAvailable === true,
      isParticipantDashboardStatusBadgeVisible: participantDashboardStatusBadgeState.isVisible === true,
      canRenderParticipantDashboardStatusBadge: participantDashboardStatusBadgeState.canRender === true,
      participantDashboardStatusBadgeLabel: participantDashboardStatusBadgeState.label,
      participantDashboardStatusBadgeTone: participantDashboardStatusBadgeState.tone,
      canBlockParticipantDashboardByStatusBadge: participantDashboardStatusBadgeState.canBlockDashboardAccess === true,
      participantDashboardNoticeBannerStatus: participantDashboardNoticeBannerState.status,
      isParticipantDashboardNoticeBannerAvailable: participantDashboardNoticeBannerState.isAvailable === true,
      isParticipantDashboardNoticeBannerVisible: participantDashboardNoticeBannerState.isVisible === true,
      canRenderParticipantDashboardNoticeBanner: participantDashboardNoticeBannerState.canRender === true,
      participantDashboardNoticeBannerTitle: participantDashboardNoticeBannerState.title,
      participantDashboardNoticeBannerMessage: participantDashboardNoticeBannerState.message,
      participantDashboardNoticeBannerTone: participantDashboardNoticeBannerState.tone,
      canDismissParticipantDashboardNoticeBanner: participantDashboardNoticeBannerState.canDismiss === true,
      canBlockParticipantDashboardByNoticeBanner: participantDashboardNoticeBannerState.canBlockDashboardAccess === true,
      participantDashboardProfileHeaderStatus: participantDashboardProfileHeaderState.status,
      isParticipantDashboardProfileHeaderAvailable: participantDashboardProfileHeaderState.isAvailable === true,
      isParticipantDashboardProfileHeaderVisible: participantDashboardProfileHeaderState.isVisible === true,
      canRenderParticipantDashboardProfileHeader: participantDashboardProfileHeaderState.canRender === true,
      canShowParticipantDashboardIdentity: participantDashboardProfileHeaderState.canShowParticipantIdentity === true,
      canShowParticipantDashboardCourseInfo: participantDashboardProfileHeaderState.canShowCourseInfo === true,
      participantDashboardProfileDisplayName: participantDashboardProfileHeaderState.displayName,
      participantDashboardProfileCourseTitle: participantDashboardProfileHeaderState.courseTitle,
      canBlockParticipantDashboardByProfileHeader: participantDashboardProfileHeaderState.canBlockDashboardAccess === true,
      participantDashboardCourseCardStatus: participantDashboardCourseCardState.status,
      isParticipantDashboardCourseCardAvailable: participantDashboardCourseCardState.isAvailable === true,
      isParticipantDashboardCourseCardVisible: participantDashboardCourseCardState.isVisible === true,
      canRenderParticipantDashboardCourseCard: participantDashboardCourseCardState.canRender === true,
      canShowParticipantDashboardCourseTitle: participantDashboardCourseCardState.canShowCourseTitle === true,
      canShowParticipantDashboardCourseStatus: participantDashboardCourseCardState.canShowCourseStatus === true,
      canShowParticipantDashboardCourseProgress: participantDashboardCourseCardState.canShowCourseProgress === true,
      canShowParticipantDashboardCourseExpiryInfo: participantDashboardCourseCardState.canShowExpiryInfo === true,
      participantDashboardCourseCardTitle: participantDashboardCourseCardState.courseTitle,
      participantDashboardCourseCardCourseStatus: participantDashboardCourseCardState.courseStatus,
      participantDashboardCourseCardProgressPercent: participantDashboardCourseCardState.progressPercent,
      canBlockParticipantDashboardByCourseCard: participantDashboardCourseCardState.canBlockDashboardAccess === true,
      participantDashboardProgressStatus: participantDashboardProgressState.status,
      isParticipantDashboardProgressAvailable: participantDashboardProgressState.isAvailable === true,
      isParticipantDashboardProgressVisible: participantDashboardProgressState.isVisible === true,
      canRenderParticipantDashboardProgress: participantDashboardProgressState.canRender === true,
      canCalculateParticipantDashboardProgress: participantDashboardProgressState.canCalculateProgress === true,
      hasParticipantDashboardProgressData: participantDashboardProgressState.hasProgressData === true,
      participantDashboardProgressPercent: participantDashboardProgressState.progressPercent,
      canShowParticipantDashboardProgressBar: participantDashboardProgressState.canShowProgressBar === true,
      canShowParticipantDashboardProgressText: participantDashboardProgressState.canShowProgressText === true,
      canBlockParticipantDashboardByProgress: participantDashboardProgressState.canBlockDashboardAccess === true,
      participantDashboardActivityListStatus: participantDashboardActivityListState.status,
      isParticipantDashboardActivityListAvailable: participantDashboardActivityListState.isAvailable === true,
      isParticipantDashboardActivityListVisible: participantDashboardActivityListState.isVisible === true,
      canRenderParticipantDashboardActivityList: participantDashboardActivityListState.canRender === true,
      canLoadParticipantDashboardActivities: participantDashboardActivityListState.canLoadActivities === true,
      hasParticipantDashboardActivityData: participantDashboardActivityListState.hasActivityData === true,
      participantDashboardTotalActivityCount: participantDashboardActivityListState.totalActivityCount,
      canShowParticipantDashboardActivityList: participantDashboardActivityListState.canShowActivityList === true,
      canShowParticipantDashboardActivityEmptyState: participantDashboardActivityListState.canShowEmptyState === true,
      canBlockParticipantDashboardByActivityList: participantDashboardActivityListState.canBlockDashboardAccess === true,
      participantDashboardRecommendationsStatus: participantDashboardRecommendationsState.status,
      isParticipantDashboardRecommendationsAvailable: participantDashboardRecommendationsState.isAvailable === true,
      isParticipantDashboardRecommendationsVisible: participantDashboardRecommendationsState.isVisible === true,
      canRenderParticipantDashboardRecommendations: participantDashboardRecommendationsState.canRender === true,
      canLoadParticipantDashboardRecommendations: participantDashboardRecommendationsState.canLoadRecommendations === true,
      hasParticipantDashboardRecommendationData: participantDashboardRecommendationsState.hasRecommendationData === true,
      participantDashboardTotalRecommendationCount: participantDashboardRecommendationsState.totalRecommendationCount,
      canShowParticipantDashboardRecommendationList: participantDashboardRecommendationsState.canShowRecommendationList === true,
      canShowParticipantDashboardRecommendationEmptyState: participantDashboardRecommendationsState.canShowEmptyState === true,
      canBlockParticipantDashboardByRecommendations: participantDashboardRecommendationsState.canBlockDashboardAccess === true,
      participantDashboardExamStatusStatus: participantDashboardExamStatusState.status,
      isParticipantDashboardExamStatusAvailable: participantDashboardExamStatusState.isAvailable === true,
      isParticipantDashboardExamStatusVisible: participantDashboardExamStatusState.isVisible === true,
      canRenderParticipantDashboardExamStatus: participantDashboardExamStatusState.canRender === true,
      canLoadParticipantDashboardExamStatus: participantDashboardExamStatusState.canLoadExamStatus === true,
      hasParticipantDashboardExamStatusData: participantDashboardExamStatusState.hasExamStatusData === true,
      participantDashboardWrittenExamStatus: participantDashboardExamStatusState.writtenExamStatus,
      participantDashboardOralExamStatus: participantDashboardExamStatusState.oralExamStatus,
      participantDashboardLastExamResult: participantDashboardExamStatusState.lastExamResult,
      canShowParticipantDashboardLastExamResult: participantDashboardExamStatusState.canShowLastExamResult === true,
      canBlockParticipantDashboardByExamStatus: participantDashboardExamStatusState.canBlockDashboardAccess === true,
      participantDashboardCertificateStatus: participantDashboardCertificateState.status,
      isParticipantDashboardCertificateAvailable: participantDashboardCertificateState.isAvailable === true,
      isParticipantDashboardCertificateVisible: participantDashboardCertificateState.isVisible === true,
      canRenderParticipantDashboardCertificate: participantDashboardCertificateState.canRender === true,
      canLoadParticipantDashboardCertificate: participantDashboardCertificateState.canLoadCertificate === true,
      hasParticipantDashboardCertificateData: participantDashboardCertificateState.hasCertificateData === true,
      participantDashboardCertificateNumber: participantDashboardCertificateState.certificateNumber,
      participantDashboardCertificateIssuedAt: participantDashboardCertificateState.issuedAt,
      participantDashboardCertificateExpiresAt: participantDashboardCertificateState.expiresAt,
      canShowParticipantDashboardCertificateCard: participantDashboardCertificateState.canShowCertificateCard === true,
      canDownloadParticipantDashboardCertificate: participantDashboardCertificateState.canDownloadCertificate === true,
      canBlockParticipantDashboardByCertificate: participantDashboardCertificateState.canBlockDashboardAccess === true,
      participantDashboardDocumentsStatus: participantDashboardDocumentsState.status,
      isParticipantDashboardDocumentsAvailable: participantDashboardDocumentsState.isAvailable === true,
      isParticipantDashboardDocumentsVisible: participantDashboardDocumentsState.isVisible === true,
      canRenderParticipantDashboardDocuments: participantDashboardDocumentsState.canRender === true,
      canLoadParticipantDashboardDocuments: participantDashboardDocumentsState.canLoadDocuments === true,
      hasParticipantDashboardDocumentData: participantDashboardDocumentsState.hasDocumentData === true,
      participantDashboardTotalDocumentCount: participantDashboardDocumentsState.totalDocumentCount,
      canShowParticipantDashboardDocumentList: participantDashboardDocumentsState.canShowDocumentList === true,
      canShowParticipantDashboardDocumentEmptyState: participantDashboardDocumentsState.canShowEmptyState === true,
      canDownloadParticipantDashboardDocuments: participantDashboardDocumentsState.canDownloadDocuments === true,
      canBlockParticipantDashboardByDocuments: participantDashboardDocumentsState.canBlockDashboardAccess === true,
      participantDashboardMessagesStatus: participantDashboardMessagesState.status,
      isParticipantDashboardMessagesAvailable: participantDashboardMessagesState.isAvailable === true,
      isParticipantDashboardMessagesVisible: participantDashboardMessagesState.isVisible === true,
      canRenderParticipantDashboardMessages: participantDashboardMessagesState.canRender === true,
      canLoadParticipantDashboardMessages: participantDashboardMessagesState.canLoadMessages === true,
      hasParticipantDashboardMessageData: participantDashboardMessagesState.hasMessageData === true,
      participantDashboardTotalMessageCount: participantDashboardMessagesState.totalMessageCount,
      participantDashboardUnreadMessageCount: participantDashboardMessagesState.unreadMessageCount,
      canShowParticipantDashboardMessageList: participantDashboardMessagesState.canShowMessageList === true,
      canShowParticipantDashboardMessageEmptyState: participantDashboardMessagesState.canShowEmptyState === true,
      canSendParticipantDashboardMessage: participantDashboardMessagesState.canSendMessage === true,
      canBlockParticipantDashboardByMessages: participantDashboardMessagesState.canBlockDashboardAccess === true,
      participantDashboardSupportStatus: participantDashboardSupportState.status,
      isParticipantDashboardSupportAvailable: participantDashboardSupportState.isAvailable === true,
      isParticipantDashboardSupportVisible: participantDashboardSupportState.isVisible === true,
      canRenderParticipantDashboardSupport: participantDashboardSupportState.canRender === true,
      canLoadParticipantDashboardSupportOptions: participantDashboardSupportState.canLoadSupportOptions === true,
      hasParticipantDashboardSupportData: participantDashboardSupportState.hasSupportData === true,
      participantDashboardSupportEmail: participantDashboardSupportState.supportEmail,
      participantDashboardSupportPhone: participantDashboardSupportState.supportPhone,
      canShowParticipantDashboardSupportCard: participantDashboardSupportState.canShowSupportCard === true,
      canCreateParticipantDashboardSupportRequest: participantDashboardSupportState.canCreateSupportRequest === true,
      canBlockParticipantDashboardBySupport: participantDashboardSupportState.canBlockDashboardAccess === true,
      participantDashboardAppointmentsStatus: participantDashboardAppointmentsState.status,
      isParticipantDashboardAppointmentsAvailable: participantDashboardAppointmentsState.isAvailable === true,
      isParticipantDashboardAppointmentsVisible: participantDashboardAppointmentsState.isVisible === true,
      canRenderParticipantDashboardAppointments: participantDashboardAppointmentsState.canRender === true,
      canLoadParticipantDashboardAppointments: participantDashboardAppointmentsState.canLoadAppointments === true,
      hasParticipantDashboardAppointmentData: participantDashboardAppointmentsState.hasAppointmentData === true,
      participantDashboardTotalAppointmentCount: participantDashboardAppointmentsState.totalAppointmentCount,
      participantDashboardNextAppointmentAt: participantDashboardAppointmentsState.nextAppointmentAt,
      canShowParticipantDashboardAppointmentList: participantDashboardAppointmentsState.canShowAppointmentList === true,
      canShowParticipantDashboardAppointmentCard: participantDashboardAppointmentsState.canShowAppointmentCard === true,
      canBookParticipantDashboardAppointment: participantDashboardAppointmentsState.canBookAppointment === true,
      canCancelParticipantDashboardAppointment: participantDashboardAppointmentsState.canCancelAppointment === true,
      canBlockParticipantDashboardByAppointments: participantDashboardAppointmentsState.canBlockDashboardAccess === true,
      participantDashboardPaymentStatus: participantDashboardPaymentStatusState.status,
      isParticipantDashboardPaymentStatusAvailable: participantDashboardPaymentStatusState.isAvailable === true,
      isParticipantDashboardPaymentStatusVisible: participantDashboardPaymentStatusState.isVisible === true,
      canRenderParticipantDashboardPaymentStatus: participantDashboardPaymentStatusState.canRender === true,
      canLoadParticipantDashboardPaymentStatus: participantDashboardPaymentStatusState.canLoadPaymentStatus === true,
      hasParticipantDashboardPaymentData: participantDashboardPaymentStatusState.hasPaymentData === true,
      participantDashboardPaymentStatusValue: participantDashboardPaymentStatusState.paymentStatus,
      participantDashboardPaymentPlan: participantDashboardPaymentStatusState.paymentPlan,
      participantDashboardOutstandingAmount: participantDashboardPaymentStatusState.outstandingAmount,
      participantDashboardPaymentCurrency: participantDashboardPaymentStatusState.currency,
      participantDashboardPaymentDueDate: participantDashboardPaymentStatusState.dueDate,
      canShowParticipantDashboardPaymentCard: participantDashboardPaymentStatusState.canShowPaymentCard === true,
      canShowParticipantDashboardOutstandingBadge: participantDashboardPaymentStatusState.canShowOutstandingBadge === true,
      canStartParticipantDashboardPayment: participantDashboardPaymentStatusState.canStartPayment === true,
      canBlockParticipantDashboardByPaymentStatus: participantDashboardPaymentStatusState.canBlockDashboardAccess === true,
      participantDashboardContractStatus: participantDashboardContractStatusState.status,
      isParticipantDashboardContractStatusAvailable: participantDashboardContractStatusState.isAvailable === true,
      isParticipantDashboardContractStatusVisible: participantDashboardContractStatusState.isVisible === true,
      canRenderParticipantDashboardContractStatus: participantDashboardContractStatusState.canRender === true,
      canLoadParticipantDashboardContractStatus: participantDashboardContractStatusState.canLoadContractStatus === true,
      hasParticipantDashboardContractData: participantDashboardContractStatusState.hasContractData === true,
      participantDashboardContractStatusValue: participantDashboardContractStatusState.contractStatus,
      participantDashboardContractNumber: participantDashboardContractStatusState.contractNumber,
      participantDashboardContractSignedAt: participantDashboardContractStatusState.contractSignedAt,
      participantDashboardContractStartsAt: participantDashboardContractStatusState.contractStartsAt,
      participantDashboardContractEndsAt: participantDashboardContractStatusState.contractEndsAt,
      canShowParticipantDashboardContractCard: participantDashboardContractStatusState.canShowContractCard === true,
      canShowParticipantDashboardSignatureStatus: participantDashboardContractStatusState.canShowSignatureStatus === true,
      canStartParticipantDashboardContractSigning: participantDashboardContractStatusState.canStartContractSigning === true,
      canDownloadParticipantDashboardContract: participantDashboardContractStatusState.canDownloadContract === true,
      canBlockParticipantDashboardByContractStatus: participantDashboardContractStatusState.canBlockDashboardAccess === true,
      participantDashboardInvoicesStatus: participantDashboardInvoicesState.status,
      isParticipantDashboardInvoicesAvailable: participantDashboardInvoicesState.isAvailable === true,
      isParticipantDashboardInvoicesVisible: participantDashboardInvoicesState.isVisible === true,
      canRenderParticipantDashboardInvoices: participantDashboardInvoicesState.canRender === true,
      canLoadParticipantDashboardInvoices: participantDashboardInvoicesState.canLoadInvoices === true,
      hasParticipantDashboardInvoiceData: participantDashboardInvoicesState.hasInvoiceData === true,
      participantDashboardTotalInvoiceCount: participantDashboardInvoicesState.totalInvoiceCount,
      participantDashboardOpenInvoiceCount: participantDashboardInvoicesState.openInvoiceCount,
      participantDashboardLatestInvoiceNumber: participantDashboardInvoicesState.latestInvoiceNumber,
      participantDashboardLatestInvoiceIssuedAt: participantDashboardInvoicesState.latestInvoiceIssuedAt,
      canShowParticipantDashboardInvoiceList: participantDashboardInvoicesState.canShowInvoiceList === true,
      canShowParticipantDashboardInvoiceCard: participantDashboardInvoicesState.canShowInvoiceCard === true,
      canDownloadParticipantDashboardInvoice: participantDashboardInvoicesState.canDownloadInvoice === true,
      canStartParticipantDashboardInvoicePayment: participantDashboardInvoicesState.canStartInvoicePayment === true,
      canBlockParticipantDashboardByInvoices: participantDashboardInvoicesState.canBlockDashboardAccess === true,
      participantDashboardAttendanceStatus: participantDashboardAttendanceState.status,
      isParticipantDashboardAttendanceAvailable: participantDashboardAttendanceState.isAvailable === true,
      isParticipantDashboardAttendanceVisible: participantDashboardAttendanceState.isVisible === true,
      canRenderParticipantDashboardAttendance: participantDashboardAttendanceState.canRender === true,
      canLoadParticipantDashboardAttendance: participantDashboardAttendanceState.canLoadAttendance === true,
      hasParticipantDashboardAttendanceData: participantDashboardAttendanceState.hasAttendanceData === true,
      participantDashboardTotalAttendanceCount: participantDashboardAttendanceState.totalAttendanceCount,
      participantDashboardPresentCount: participantDashboardAttendanceState.presentCount,
      participantDashboardAbsentCount: participantDashboardAttendanceState.absentCount,
      participantDashboardExcusedAbsenceCount: participantDashboardAttendanceState.excusedAbsenceCount,
      participantDashboardAttendanceRatePercent: participantDashboardAttendanceState.attendanceRatePercent,
      participantDashboardLastAttendanceAt: participantDashboardAttendanceState.lastAttendanceAt,
      canShowParticipantDashboardAttendanceList: participantDashboardAttendanceState.canShowAttendanceList === true,
      canShowParticipantDashboardAttendanceCard: participantDashboardAttendanceState.canShowAttendanceCard === true,
      canShowParticipantDashboardAttendanceRate: participantDashboardAttendanceState.canShowAttendanceRate === true,
      canBlockParticipantDashboardByAttendance: participantDashboardAttendanceState.canBlockDashboardAccess === true,
      participantDashboardLessonPlanStatus: participantDashboardLessonPlanState.status,
      isParticipantDashboardLessonPlanAvailable: participantDashboardLessonPlanState.isAvailable === true,
      isParticipantDashboardLessonPlanVisible: participantDashboardLessonPlanState.isVisible === true,
      canRenderParticipantDashboardLessonPlan: participantDashboardLessonPlanState.canRender === true,
      canLoadParticipantDashboardLessonPlan: participantDashboardLessonPlanState.canLoadLessonPlan === true,
      hasParticipantDashboardLessonPlanData: participantDashboardLessonPlanState.hasLessonPlanData === true,
      participantDashboardTotalLessonCount: participantDashboardLessonPlanState.totalLessonCount,
      participantDashboardNextLessonAt: participantDashboardLessonPlanState.nextLessonAt,
      participantDashboardCurrentTopic: participantDashboardLessonPlanState.currentTopic,
      participantDashboardCurrentModule: participantDashboardLessonPlanState.currentModule,
      canShowParticipantDashboardLessonPlanList: participantDashboardLessonPlanState.canShowLessonPlanList === true,
      canShowParticipantDashboardLessonPlanCard: participantDashboardLessonPlanState.canShowLessonPlanCard === true,
      canShowParticipantDashboardNextLessonHint: participantDashboardLessonPlanState.canShowNextLessonHint === true,
      canBlockParticipantDashboardByLessonPlan: participantDashboardLessonPlanState.canBlockDashboardAccess === true,
      participantDashboardCourseMaterialsStatus: participantDashboardCourseMaterialsState.status,
      isParticipantDashboardCourseMaterialsAvailable: participantDashboardCourseMaterialsState.isAvailable === true,
      isParticipantDashboardCourseMaterialsVisible: participantDashboardCourseMaterialsState.isVisible === true,
      canRenderParticipantDashboardCourseMaterials: participantDashboardCourseMaterialsState.canRender === true,
      canLoadParticipantDashboardCourseMaterials: participantDashboardCourseMaterialsState.canLoadCourseMaterials === true,
      hasParticipantDashboardCourseMaterialData: participantDashboardCourseMaterialsState.hasCourseMaterialData === true,
      participantDashboardTotalCourseMaterialCount: participantDashboardCourseMaterialsState.totalCourseMaterialCount,
      participantDashboardLatestCourseMaterialTitle: participantDashboardCourseMaterialsState.latestCourseMaterialTitle,
      participantDashboardLatestCourseMaterialAddedAt: participantDashboardCourseMaterialsState.latestCourseMaterialAddedAt,
      canShowParticipantDashboardCourseMaterialList: participantDashboardCourseMaterialsState.canShowCourseMaterialList === true,
      canShowParticipantDashboardCourseMaterialCard: participantDashboardCourseMaterialsState.canShowCourseMaterialCard === true,
      canOpenParticipantDashboardCourseMaterial: participantDashboardCourseMaterialsState.canOpenCourseMaterial === true,
      canDownloadParticipantDashboardCourseMaterial: participantDashboardCourseMaterialsState.canDownloadCourseMaterial === true,
      canMarkParticipantDashboardCourseMaterialAsRead: participantDashboardCourseMaterialsState.canMarkCourseMaterialAsRead === true,
      canBlockParticipantDashboardByCourseMaterials: participantDashboardCourseMaterialsState.canBlockDashboardAccess === true,
      participantDashboardLearningProgressDetailsStatus: participantDashboardLearningProgressDetailsState.status,
      isParticipantDashboardLearningProgressDetailsAvailable: participantDashboardLearningProgressDetailsState.isAvailable === true,
      isParticipantDashboardLearningProgressDetailsVisible: participantDashboardLearningProgressDetailsState.isVisible === true,
      canRenderParticipantDashboardLearningProgressDetails: participantDashboardLearningProgressDetailsState.canRender === true,
      canLoadParticipantDashboardLearningProgressDetails: participantDashboardLearningProgressDetailsState.canLoadLearningProgressDetails === true,
      hasParticipantDashboardLearningProgressDetailsData: participantDashboardLearningProgressDetailsState.hasLearningProgressDetailsData === true,
      participantDashboardTotalLearningItemCount: participantDashboardLearningProgressDetailsState.totalLearningItemCount,
      participantDashboardCompletedLearningItemCount: participantDashboardLearningProgressDetailsState.completedLearningItemCount,
      participantDashboardOpenLearningItemCount: participantDashboardLearningProgressDetailsState.openLearningItemCount,
      participantDashboardLearningProgressPercent: participantDashboardLearningProgressDetailsState.learningProgressPercent,
      participantDashboardCurrentLearningTopic: participantDashboardLearningProgressDetailsState.currentLearningTopic,
      participantDashboardLastLearningActivityAt: participantDashboardLearningProgressDetailsState.lastLearningActivityAt,
      canShowParticipantDashboardLearningProgressDetailsList: participantDashboardLearningProgressDetailsState.canShowLearningProgressDetailsList === true,
      canShowParticipantDashboardLearningProgressDetailsCard: participantDashboardLearningProgressDetailsState.canShowLearningProgressDetailsCard === true,
      canShowParticipantDashboardLearningProgressPercent: participantDashboardLearningProgressDetailsState.canShowLearningProgressPercent === true,
      canShowParticipantDashboardCurrentLearningTopic: participantDashboardLearningProgressDetailsState.canShowCurrentLearningTopic === true,
      canBlockParticipantDashboardByLearningProgressDetails: participantDashboardLearningProgressDetailsState.canBlockDashboardAccess === true,
      participantDashboardMistakeTrainingDetailsStatus: participantDashboardMistakeTrainingDetailsState.status,
      isParticipantDashboardMistakeTrainingDetailsAvailable: participantDashboardMistakeTrainingDetailsState.isAvailable === true,
      isParticipantDashboardMistakeTrainingDetailsVisible: participantDashboardMistakeTrainingDetailsState.isVisible === true,
      canRenderParticipantDashboardMistakeTrainingDetails: participantDashboardMistakeTrainingDetailsState.canRender === true,
      canLoadParticipantDashboardMistakeTrainingDetails: participantDashboardMistakeTrainingDetailsState.canLoadMistakeTrainingDetails === true,
      hasParticipantDashboardMistakeTrainingDetailsData: participantDashboardMistakeTrainingDetailsState.hasMistakeTrainingDetailsData === true,
      participantDashboardTotalMistakeCount: participantDashboardMistakeTrainingDetailsState.totalMistakeCount,
      participantDashboardOpenMistakeCount: participantDashboardMistakeTrainingDetailsState.openMistakeCount,
      participantDashboardResolvedMistakeCount: participantDashboardMistakeTrainingDetailsState.resolvedMistakeCount,
      participantDashboardRepeatedMistakeCount: participantDashboardMistakeTrainingDetailsState.repeatedMistakeCount,
      participantDashboardLatestMistakeTopic: participantDashboardMistakeTrainingDetailsState.latestMistakeTopic,
      participantDashboardLastMistakeTrainingAt: participantDashboardMistakeTrainingDetailsState.lastMistakeTrainingAt,
      participantDashboardRecommendedReviewMode: participantDashboardMistakeTrainingDetailsState.recommendedReviewMode,
      canShowParticipantDashboardMistakeTrainingDetailsList: participantDashboardMistakeTrainingDetailsState.canShowMistakeTrainingDetailsList === true,
      canShowParticipantDashboardMistakeTrainingDetailsCard: participantDashboardMistakeTrainingDetailsState.canShowMistakeTrainingDetailsCard === true,
      canShowParticipantDashboardOpenMistakeCount: participantDashboardMistakeTrainingDetailsState.canShowOpenMistakeCount === true,
      canShowParticipantDashboardRecommendedReviewMode: participantDashboardMistakeTrainingDetailsState.canShowRecommendedReviewMode === true,
      canStartParticipantDashboardMistakeReview: participantDashboardMistakeTrainingDetailsState.canStartMistakeReview === true,
      canBlockParticipantDashboardByMistakeTrainingDetails: participantDashboardMistakeTrainingDetailsState.canBlockDashboardAccess === true,
      participantDashboardExamSimulationDetailsStatus: participantDashboardExamSimulationDetailsState.status,
      isParticipantDashboardExamSimulationDetailsAvailable: participantDashboardExamSimulationDetailsState.isAvailable === true,
      isParticipantDashboardExamSimulationDetailsVisible: participantDashboardExamSimulationDetailsState.isVisible === true,
      canRenderParticipantDashboardExamSimulationDetails: participantDashboardExamSimulationDetailsState.canRender === true,
      canLoadParticipantDashboardExamSimulationDetails: participantDashboardExamSimulationDetailsState.canLoadExamSimulationDetails === true,
      hasParticipantDashboardExamSimulationDetailsData: participantDashboardExamSimulationDetailsState.hasExamSimulationDetailsData === true,
      participantDashboardTotalExamSimulationCount: participantDashboardExamSimulationDetailsState.totalExamSimulationCount,
      participantDashboardPassedExamSimulationCount: participantDashboardExamSimulationDetailsState.passedExamSimulationCount,
      participantDashboardFailedExamSimulationCount: participantDashboardExamSimulationDetailsState.failedExamSimulationCount,
      participantDashboardLatestExamSimulationScore: participantDashboardExamSimulationDetailsState.latestExamSimulationScore,
      participantDashboardLatestExamSimulationPassed: participantDashboardExamSimulationDetailsState.latestExamSimulationPassed,
      participantDashboardLatestExamSimulationAt: participantDashboardExamSimulationDetailsState.latestExamSimulationAt,
      participantDashboardBestExamSimulationScore: participantDashboardExamSimulationDetailsState.bestExamSimulationScore,
      participantDashboardRecommendedExamSimulationMode: participantDashboardExamSimulationDetailsState.recommendedExamSimulationMode,
      canShowParticipantDashboardExamSimulationDetailsList: participantDashboardExamSimulationDetailsState.canShowExamSimulationDetailsList === true,
      canShowParticipantDashboardExamSimulationDetailsCard: participantDashboardExamSimulationDetailsState.canShowExamSimulationDetailsCard === true,
      canShowParticipantDashboardExamSimulationScore: participantDashboardExamSimulationDetailsState.canShowExamSimulationScore === true,
      canShowParticipantDashboardExamSimulationRecommendation: participantDashboardExamSimulationDetailsState.canShowExamSimulationRecommendation === true,
      canStartParticipantDashboardExamSimulationReview: participantDashboardExamSimulationDetailsState.canStartExamSimulationReview === true,
      canBlockParticipantDashboardByExamSimulationDetails: participantDashboardExamSimulationDetailsState.canBlockDashboardAccess === true,
      participantDashboardOralExamDetailsStatus: participantDashboardOralExamDetailsState.status,
      isParticipantDashboardOralExamDetailsAvailable: participantDashboardOralExamDetailsState.isAvailable === true,
      isParticipantDashboardOralExamDetailsVisible: participantDashboardOralExamDetailsState.isVisible === true,
      canRenderParticipantDashboardOralExamDetails: participantDashboardOralExamDetailsState.canRender === true,
      canLoadParticipantDashboardOralExamDetails: participantDashboardOralExamDetailsState.canLoadOralExamDetails === true,
      hasParticipantDashboardOralExamDetailsData: participantDashboardOralExamDetailsState.hasOralExamDetailsData === true,
      participantDashboardTotalOralQuestionCount: participantDashboardOralExamDetailsState.totalOralQuestionCount,
      participantDashboardPracticedOralQuestionCount: participantDashboardOralExamDetailsState.practicedOralQuestionCount,
      participantDashboardOpenOralQuestionCount: participantDashboardOralExamDetailsState.openOralQuestionCount,
      participantDashboardConfidentOralAnswerCount: participantDashboardOralExamDetailsState.confidentOralAnswerCount,
      participantDashboardUncertainOralAnswerCount: participantDashboardOralExamDetailsState.uncertainOralAnswerCount,
      participantDashboardLatestOralExamTopic: participantDashboardOralExamDetailsState.latestOralExamTopic,
      participantDashboardLastOralPracticeAt: participantDashboardOralExamDetailsState.lastOralPracticeAt,
      participantDashboardRecommendedOralPracticeMode: participantDashboardOralExamDetailsState.recommendedOralPracticeMode,
      canShowParticipantDashboardOralExamDetailsList: participantDashboardOralExamDetailsState.canShowOralExamDetailsList === true,
      canShowParticipantDashboardOralExamDetailsCard: participantDashboardOralExamDetailsState.canShowOralExamDetailsCard === true,
      canShowParticipantDashboardOpenOralQuestionCount: participantDashboardOralExamDetailsState.canShowOpenOralQuestionCount === true,
      canShowParticipantDashboardOralPracticeRecommendation: participantDashboardOralExamDetailsState.canShowOralPracticeRecommendation === true,
      canStartParticipantDashboardOralExamPracticeReview: participantDashboardOralExamDetailsState.canStartOralExamPracticeReview === true,
      canBlockParticipantDashboardByOralExamDetails: participantDashboardOralExamDetailsState.canBlockDashboardAccess === true,
      participantDashboardFlashcardsDetailsStatus: participantDashboardFlashcardsDetailsState.status,
      isParticipantDashboardFlashcardsDetailsAvailable: participantDashboardFlashcardsDetailsState.isAvailable === true,
      isParticipantDashboardFlashcardsDetailsVisible: participantDashboardFlashcardsDetailsState.isVisible === true,
      canRenderParticipantDashboardFlashcardsDetails: participantDashboardFlashcardsDetailsState.canRender === true,
      canLoadParticipantDashboardFlashcardsDetails: participantDashboardFlashcardsDetailsState.canLoadFlashcardsDetails === true,
      hasParticipantDashboardFlashcardsDetailsData: participantDashboardFlashcardsDetailsState.hasFlashcardsDetailsData === true,
      participantDashboardTotalFlashcardCount: participantDashboardFlashcardsDetailsState.totalFlashcardCount,
      participantDashboardPracticedFlashcardCount: participantDashboardFlashcardsDetailsState.practicedFlashcardCount,
      participantDashboardMasteredFlashcardCount: participantDashboardFlashcardsDetailsState.masteredFlashcardCount,
      participantDashboardWeakFlashcardCount: participantDashboardFlashcardsDetailsState.weakFlashcardCount,
      participantDashboardDueFlashcardCount: participantDashboardFlashcardsDetailsState.dueFlashcardCount,
      participantDashboardLatestFlashcardTopic: participantDashboardFlashcardsDetailsState.latestFlashcardTopic,
      participantDashboardLastFlashcardPracticeAt: participantDashboardFlashcardsDetailsState.lastFlashcardPracticeAt,
      participantDashboardRecommendedFlashcardPracticeMode: participantDashboardFlashcardsDetailsState.recommendedFlashcardPracticeMode,
      canShowParticipantDashboardFlashcardsDetailsList: participantDashboardFlashcardsDetailsState.canShowFlashcardsDetailsList === true,
      canShowParticipantDashboardFlashcardsDetailsCard: participantDashboardFlashcardsDetailsState.canShowFlashcardsDetailsCard === true,
      canShowParticipantDashboardDueFlashcardCount: participantDashboardFlashcardsDetailsState.canShowDueFlashcardCount === true,
      canShowParticipantDashboardFlashcardPracticeRecommendation: participantDashboardFlashcardsDetailsState.canShowFlashcardPracticeRecommendation === true,
      canStartParticipantDashboardFlashcardPracticeReview: participantDashboardFlashcardsDetailsState.canStartFlashcardPracticeReview === true,
      canBlockParticipantDashboardByFlashcardsDetails: participantDashboardFlashcardsDetailsState.canBlockDashboardAccess === true,
      participantDashboardSampleQuestionsDetailsStatus: participantDashboardSampleQuestionsDetailsState.status,
      isParticipantDashboardSampleQuestionsDetailsAvailable: participantDashboardSampleQuestionsDetailsState.isAvailable === true,
      isParticipantDashboardSampleQuestionsDetailsVisible: participantDashboardSampleQuestionsDetailsState.isVisible === true,
      canRenderParticipantDashboardSampleQuestionsDetails: participantDashboardSampleQuestionsDetailsState.canRender === true,
      canLoadParticipantDashboardSampleQuestionsDetails: participantDashboardSampleQuestionsDetailsState.canLoadSampleQuestionsDetails === true,
      hasParticipantDashboardSampleQuestionsDetailsData: participantDashboardSampleQuestionsDetailsState.hasSampleQuestionsDetailsData === true,
      participantDashboardTotalSampleQuestionCount: participantDashboardSampleQuestionsDetailsState.totalSampleQuestionCount,
      participantDashboardPracticedSampleQuestionCount: participantDashboardSampleQuestionsDetailsState.practicedSampleQuestionCount,
      participantDashboardCorrectSampleQuestionCount: participantDashboardSampleQuestionsDetailsState.correctSampleQuestionCount,
      participantDashboardIncorrectSampleQuestionCount: participantDashboardSampleQuestionsDetailsState.incorrectSampleQuestionCount,
      participantDashboardOpenSampleQuestionCount: participantDashboardSampleQuestionsDetailsState.openSampleQuestionCount,
      participantDashboardLatestSampleQuestionTopic: participantDashboardSampleQuestionsDetailsState.latestSampleQuestionTopic,
      participantDashboardLastSampleQuestionPracticeAt: participantDashboardSampleQuestionsDetailsState.lastSampleQuestionPracticeAt,
      participantDashboardRecommendedSampleQuestionPracticeMode: participantDashboardSampleQuestionsDetailsState.recommendedSampleQuestionPracticeMode,
      canShowParticipantDashboardSampleQuestionsDetailsList: participantDashboardSampleQuestionsDetailsState.canShowSampleQuestionsDetailsList === true,
      canShowParticipantDashboardSampleQuestionsDetailsCard: participantDashboardSampleQuestionsDetailsState.canShowSampleQuestionsDetailsCard === true,
      canShowParticipantDashboardOpenSampleQuestionCount: participantDashboardSampleQuestionsDetailsState.canShowOpenSampleQuestionCount === true,
      canShowParticipantDashboardSampleQuestionPracticeRecommendation: participantDashboardSampleQuestionsDetailsState.canShowSampleQuestionPracticeRecommendation === true,
      canStartParticipantDashboardSampleQuestionPracticeReview: participantDashboardSampleQuestionsDetailsState.canStartSampleQuestionPracticeReview === true,
      canBlockParticipantDashboardBySampleQuestionsDetails: participantDashboardSampleQuestionsDetailsState.canBlockDashboardAccess === true,
      participantDashboardExamHistoryStatus: participantDashboardExamHistoryState.status,
      isParticipantDashboardExamHistoryAvailable: participantDashboardExamHistoryState.isAvailable === true,
      isParticipantDashboardExamHistoryVisible: participantDashboardExamHistoryState.isVisible === true,
      canRenderParticipantDashboardExamHistory: participantDashboardExamHistoryState.canRender === true,
      canLoadParticipantDashboardExamHistory: participantDashboardExamHistoryState.canLoadExamHistory === true,
      hasParticipantDashboardExamHistoryData: participantDashboardExamHistoryState.hasExamHistoryData === true,
      participantDashboardTotalExamHistoryCount: participantDashboardExamHistoryState.totalExamHistoryCount,
      participantDashboardPassedExamHistoryCount: participantDashboardExamHistoryState.passedExamHistoryCount,
      participantDashboardFailedExamHistoryCount: participantDashboardExamHistoryState.failedExamHistoryCount,
      participantDashboardLatestExamHistoryScore: participantDashboardExamHistoryState.latestExamHistoryScore,
      participantDashboardLatestExamHistoryPassed: participantDashboardExamHistoryState.latestExamHistoryPassed,
      participantDashboardLatestExamHistoryAt: participantDashboardExamHistoryState.latestExamHistoryAt,
      participantDashboardBestExamHistoryScore: participantDashboardExamHistoryState.bestExamHistoryScore,
      participantDashboardAverageExamHistoryScore: participantDashboardExamHistoryState.averageExamHistoryScore,
      participantDashboardRecommendedExamHistoryAction: participantDashboardExamHistoryState.recommendedExamHistoryAction,
      canShowParticipantDashboardExamHistoryList: participantDashboardExamHistoryState.canShowExamHistoryList === true,
      canShowParticipantDashboardExamHistoryCard: participantDashboardExamHistoryState.canShowExamHistoryCard === true,
      canShowParticipantDashboardExamHistoryScoreTrend: participantDashboardExamHistoryState.canShowExamHistoryScoreTrend === true,
      canShowParticipantDashboardExamHistoryBestScore: participantDashboardExamHistoryState.canShowExamHistoryBestScore === true,
      canOpenParticipantDashboardExamHistoryAttemptReview: participantDashboardExamHistoryState.canOpenExamHistoryAttemptReview === true,
      canBlockParticipantDashboardByExamHistory: participantDashboardExamHistoryState.canBlockDashboardAccess === true,
      participantDashboardExamHistoryDataSourceStatus: participantDashboardExamHistoryDataSourceState.status,
      isParticipantDashboardExamHistoryDataSourcePrepared: participantDashboardExamHistoryDataSourceState.isPrepared === true,
      canLoadParticipantDashboardExamHistoryDataSource: participantDashboardExamHistoryDataSourceState.canLoad === true,
      hasParticipantDashboardExamHistoryDataSourceData: participantDashboardExamHistoryDataSourceState.hasData === true,
      participantDashboardExamHistoryDataSourceType: participantDashboardExamHistoryDataSourceState.sourceType,
      participantDashboardExamHistoryDataSourceRpcName: participantDashboardExamHistoryDataSourceState.rpcName,
      participantDashboardExamHistoryDataSourceNormalizerName: participantDashboardExamHistoryDataSourceState.normalizerName,
      isParticipantDashboardExamHistoryDataSourceNormalizerPrepared: participantDashboardExamHistoryDataSourceState.isNormalizerPrepared === true,
      canNormalizeParticipantDashboardExamHistoryRows: participantDashboardExamHistoryDataSourceState.canNormalizeRows === true,
      participantDashboardExamHistoryDataSourceAggregatorName: participantDashboardExamHistoryDataSourceState.aggregatorName,
      isParticipantDashboardExamHistoryDataSourceAggregatorPrepared: participantDashboardExamHistoryDataSourceState.isAggregatorPrepared === true,
      canAggregateParticipantDashboardExamHistoryRows: participantDashboardExamHistoryDataSourceState.canAggregateRows === true,
      participantDashboardExamHistoryMetricsScope: "page_only",
      canPopulateParticipantDashboardGlobalExamOutcomeCounts: false,
      isParticipantDashboardExamHistoryDataSourceBlockedSafely: participantDashboardExamHistoryDataSourceState.isBlockedSafely === true,
      participantExamResultHistoryRpcStatus: participantExamResultHistoryRpcState.status,
      isParticipantExamResultHistoryRpcPrepared: participantExamResultHistoryRpcState.isRpcPrepared === true,
      canCallParticipantExamResultHistoryRpc: participantExamResultHistoryRpcState.canCallRpc === true,
      participantExamResultHistoryRpcName: participantExamResultHistoryRpcState.rpcName,
      participantExamResultHistoryDefaultLimit: participantExamResultHistoryRpcState.defaultLimit,
      participantExamResultHistoryMaxLimit: participantExamResultHistoryRpcState.maxLimit,
      participantExamResultHistoryMaxOffset: participantExamResultHistoryRpcState.maxOffset,
      isParticipantExamResultHistoryRpcBlockedSafely: participantExamResultHistoryRpcState.isBlockedSafely === true,
      participantDashboardCertificateHistoryStatus: participantDashboardCertificateHistoryState.status,
      isParticipantDashboardCertificateHistoryAvailable: participantDashboardCertificateHistoryState.isAvailable === true,
      isParticipantDashboardCertificateHistoryVisible: participantDashboardCertificateHistoryState.isVisible === true,
      canRenderParticipantDashboardCertificateHistory: participantDashboardCertificateHistoryState.canRender === true,
      canLoadParticipantDashboardCertificateHistory: participantDashboardCertificateHistoryState.canLoadCertificateHistory === true,
      hasParticipantDashboardCertificateHistoryData: participantDashboardCertificateHistoryState.hasCertificateHistoryData === true,
      participantDashboardTotalCertificateHistoryCount: participantDashboardCertificateHistoryState.totalCertificateHistoryCount,
      participantDashboardIssuedCertificateCount: participantDashboardCertificateHistoryState.issuedCertificateCount,
      participantDashboardPendingCertificateCount: participantDashboardCertificateHistoryState.pendingCertificateCount,
      participantDashboardFailedCertificateCount: participantDashboardCertificateHistoryState.failedCertificateCount,
      participantDashboardLatestCertificateTitle: participantDashboardCertificateHistoryState.latestCertificateTitle,
      participantDashboardLatestCertificateStatus: participantDashboardCertificateHistoryState.latestCertificateStatus,
      participantDashboardLatestCertificateIssuedAt: participantDashboardCertificateHistoryState.latestCertificateIssuedAt,
      participantDashboardLatestCertificateDownloadUrl: participantDashboardCertificateHistoryState.latestCertificateDownloadUrl,
      participantDashboardRecommendedCertificateHistoryAction: participantDashboardCertificateHistoryState.recommendedCertificateHistoryAction,
      canShowParticipantDashboardCertificateHistoryList: participantDashboardCertificateHistoryState.canShowCertificateHistoryList === true,
      canShowParticipantDashboardCertificateHistoryCard: participantDashboardCertificateHistoryState.canShowCertificateHistoryCard === true,
      canShowParticipantDashboardCertificateIssueStatus: participantDashboardCertificateHistoryState.canShowCertificateIssueStatus === true,
      canShowParticipantDashboardCertificateDownloadAction: participantDashboardCertificateHistoryState.canShowCertificateDownloadAction === true,
      canOpenParticipantDashboardCertificateHistoryEntry: participantDashboardCertificateHistoryState.canOpenCertificateHistoryEntry === true,
      canDownloadParticipantDashboardCertificateFromHistory: participantDashboardCertificateHistoryState.canDownloadCertificateFromHistory === true,
      canBlockParticipantDashboardByCertificateHistory: participantDashboardCertificateHistoryState.canBlockDashboardAccess === true,
      participantDashboardCertificateDownloadStatus: participantDashboardCertificateDownloadState.status,
      isParticipantDashboardCertificateDownloadAvailable: participantDashboardCertificateDownloadState.isAvailable === true,
      isParticipantDashboardCertificateDownloadVisible: participantDashboardCertificateDownloadState.isVisible === true,
      canRenderParticipantDashboardCertificateDownload: participantDashboardCertificateDownloadState.canRender === true,
      canLoadParticipantDashboardCertificateDownload: participantDashboardCertificateDownloadState.canLoadCertificateDownload === true,
      hasParticipantDashboardCertificateDownloadData: participantDashboardCertificateDownloadState.hasCertificateDownloadData === true,
      participantDashboardTotalCertificateDownloadCount: participantDashboardCertificateDownloadState.totalCertificateDownloadCount,
      participantDashboardAvailableCertificateDownloadCount: participantDashboardCertificateDownloadState.availableCertificateDownloadCount,
      participantDashboardPendingCertificateDownloadCount: participantDashboardCertificateDownloadState.pendingCertificateDownloadCount,
      participantDashboardExpiredCertificateDownloadCount: participantDashboardCertificateDownloadState.expiredCertificateDownloadCount,
      participantDashboardLatestCertificateDownloadTitle: participantDashboardCertificateDownloadState.latestCertificateDownloadTitle,
      participantDashboardLatestCertificateDownloadStatus: participantDashboardCertificateDownloadState.latestCertificateDownloadStatus,
      participantDashboardLatestCertificateDownloadUrl: participantDashboardCertificateDownloadState.latestCertificateDownloadUrl,
      participantDashboardLatestCertificateDownloadAvailableUntil: participantDashboardCertificateDownloadState.latestCertificateDownloadAvailableUntil,
      participantDashboardRecommendedCertificateDownloadAction: participantDashboardCertificateDownloadState.recommendedCertificateDownloadAction,
      canShowParticipantDashboardCertificateDownloadList: participantDashboardCertificateDownloadState.canShowCertificateDownloadList === true,
      canShowParticipantDashboardCertificateDownloadCard: participantDashboardCertificateDownloadState.canShowCertificateDownloadCard === true,
      canShowParticipantDashboardCertificateDownloadButton: participantDashboardCertificateDownloadState.canShowCertificateDownloadButton === true,
      canShowParticipantDashboardCertificateDownloadStatus: participantDashboardCertificateDownloadState.canShowCertificateDownloadStatus === true,
      canStartParticipantDashboardCertificateDownload: participantDashboardCertificateDownloadState.canStartCertificateDownload === true,
      canOpenParticipantDashboardCertificateDownloadPreview: participantDashboardCertificateDownloadState.canOpenCertificateDownloadPreview === true,
      canTrackParticipantDashboardCertificateDownload: participantDashboardCertificateDownloadState.canTrackCertificateDownload === true,
      canBlockParticipantDashboardByCertificateDownload: participantDashboardCertificateDownloadState.canBlockDashboardAccess === true,
      participantDashboardCertificatePreviewStatus: participantDashboardCertificatePreviewState.status,
      isParticipantDashboardCertificatePreviewAvailable: participantDashboardCertificatePreviewState.isAvailable === true,
      isParticipantDashboardCertificatePreviewVisible: participantDashboardCertificatePreviewState.isVisible === true,
      canRenderParticipantDashboardCertificatePreview: participantDashboardCertificatePreviewState.canRender === true,
      canLoadParticipantDashboardCertificatePreview: participantDashboardCertificatePreviewState.canLoadCertificatePreview === true,
      hasParticipantDashboardCertificatePreviewData: participantDashboardCertificatePreviewState.hasCertificatePreviewData === true,
      participantDashboardActiveCertificatePreviewId: participantDashboardCertificatePreviewState.activeCertificatePreviewId,
      participantDashboardTotalCertificatePreviewCount: participantDashboardCertificatePreviewState.totalCertificatePreviewCount,
      participantDashboardAvailableCertificatePreviewCount: participantDashboardCertificatePreviewState.availableCertificatePreviewCount,
      participantDashboardLatestCertificatePreviewTitle: participantDashboardCertificatePreviewState.latestCertificatePreviewTitle,
      participantDashboardLatestCertificatePreviewStatus: participantDashboardCertificatePreviewState.latestCertificatePreviewStatus,
      participantDashboardLatestCertificatePreviewUrl: participantDashboardCertificatePreviewState.latestCertificatePreviewUrl,
      participantDashboardLatestCertificatePreviewMimeType: participantDashboardCertificatePreviewState.latestCertificatePreviewMimeType,
      participantDashboardLatestCertificatePreviewGeneratedAt: participantDashboardCertificatePreviewState.latestCertificatePreviewGeneratedAt,
      participantDashboardLatestCertificatePreviewExpiresAt: participantDashboardCertificatePreviewState.latestCertificatePreviewExpiresAt,
      participantDashboardRecommendedCertificatePreviewAction: participantDashboardCertificatePreviewState.recommendedCertificatePreviewAction,
      canShowParticipantDashboardCertificatePreviewList: participantDashboardCertificatePreviewState.canShowCertificatePreviewList === true,
      canShowParticipantDashboardCertificatePreviewCard: participantDashboardCertificatePreviewState.canShowCertificatePreviewCard === true,
      canShowParticipantDashboardCertificatePreviewButton: participantDashboardCertificatePreviewState.canShowCertificatePreviewButton === true,
      canShowParticipantDashboardCertificatePreviewStatus: participantDashboardCertificatePreviewState.canShowCertificatePreviewStatus === true,
      canOpenParticipantDashboardCertificatePreview: participantDashboardCertificatePreviewState.canOpenCertificatePreview === true,
      canRenderParticipantDashboardCertificatePreviewFrame: participantDashboardCertificatePreviewState.canRenderCertificatePreviewFrame === true,
      canRefreshParticipantDashboardCertificatePreview: participantDashboardCertificatePreviewState.canRefreshCertificatePreview === true,
      canPrintParticipantDashboardCertificatePreview: participantDashboardCertificatePreviewState.canPrintCertificatePreview === true,
      canBlockParticipantDashboardByCertificatePreview: participantDashboardCertificatePreviewState.canBlockDashboardAccess === true,
      participantDashboardCertificatePrintStatus: participantDashboardCertificatePrintState.status,
      isParticipantDashboardCertificatePrintAvailable: participantDashboardCertificatePrintState.isAvailable === true,
      isParticipantDashboardCertificatePrintVisible: participantDashboardCertificatePrintState.isVisible === true,
      canRenderParticipantDashboardCertificatePrint: participantDashboardCertificatePrintState.canRender === true,
      canLoadParticipantDashboardCertificatePrint: participantDashboardCertificatePrintState.canLoadCertificatePrint === true,
      hasParticipantDashboardCertificatePrintData: participantDashboardCertificatePrintState.hasCertificatePrintData === true,
      canShowParticipantDashboardCertificatePrintButton: participantDashboardCertificatePrintState.canShowCertificatePrintButton === true,
      canOpenParticipantDashboardCertificatePrintDialog: participantDashboardCertificatePrintState.canOpenCertificatePrintDialog === true,
      canStartParticipantDashboardCertificatePrint: participantDashboardCertificatePrintState.canStartCertificatePrint === true,
      canBlockParticipantDashboardByCertificatePrint: participantDashboardCertificatePrintState.canBlockDashboardAccess === true,
      participantDashboardCertificateShareStatus: participantDashboardCertificateShareState.status,
      isParticipantDashboardCertificateShareAvailable: participantDashboardCertificateShareState.isAvailable === true,
      isParticipantDashboardCertificateShareVisible: participantDashboardCertificateShareState.isVisible === true,
      canRenderParticipantDashboardCertificateShare: participantDashboardCertificateShareState.canRender === true,
      canLoadParticipantDashboardCertificateShare: participantDashboardCertificateShareState.canLoadCertificateShare === true,
      hasParticipantDashboardCertificateShareData: participantDashboardCertificateShareState.hasCertificateShareData === true,
      canShowParticipantDashboardCertificateShareButton: participantDashboardCertificateShareState.canShowCertificateShareButton === true,
      canOpenParticipantDashboardCertificateShareDialog: participantDashboardCertificateShareState.canOpenCertificateShareDialog === true,
      canCreateParticipantDashboardCertificateShareLink: participantDashboardCertificateShareState.canCreateCertificateShareLink === true,
      canSendParticipantDashboardCertificateShareEmail: participantDashboardCertificateShareState.canSendCertificateShareEmail === true,
      canBlockParticipantDashboardByCertificateShare: participantDashboardCertificateShareState.canBlockDashboardAccess === true,
      participantDashboardCertificateVerificationStatus: participantDashboardCertificateVerificationState.status,
      isParticipantDashboardCertificateVerificationAvailable: participantDashboardCertificateVerificationState.isAvailable === true,
      isParticipantDashboardCertificateVerificationVisible: participantDashboardCertificateVerificationState.isVisible === true,
      canRenderParticipantDashboardCertificateVerification: participantDashboardCertificateVerificationState.canRender === true,
      canLoadParticipantDashboardCertificateVerification: participantDashboardCertificateVerificationState.canLoadCertificateVerification === true,
      hasParticipantDashboardCertificateVerificationData: participantDashboardCertificateVerificationState.hasCertificateVerificationData === true,
      canShowParticipantDashboardCertificateVerificationButton: participantDashboardCertificateVerificationState.canShowCertificateVerificationButton === true,
      canOpenParticipantDashboardCertificateVerificationDialog: participantDashboardCertificateVerificationState.canOpenCertificateVerificationDialog === true,
      canCreateParticipantDashboardCertificateVerificationCode: participantDashboardCertificateVerificationState.canCreateCertificateVerificationCode === true,
      canOpenParticipantDashboardCertificateVerificationPage: participantDashboardCertificateVerificationState.canOpenCertificateVerificationPage === true,
      canVerifyParticipantDashboardCertificateOnline: participantDashboardCertificateVerificationState.canVerifyCertificateOnline === true,
      canBlockParticipantDashboardByCertificateVerification: participantDashboardCertificateVerificationState.canBlockDashboardAccess === true,
      participantDashboardCertificateQrCodeStatus: participantDashboardCertificateQrCodeState.status,
      isParticipantDashboardCertificateQrCodeAvailable: participantDashboardCertificateQrCodeState.isAvailable === true,
      isParticipantDashboardCertificateQrCodeVisible: participantDashboardCertificateQrCodeState.isVisible === true,
      canRenderParticipantDashboardCertificateQrCode: participantDashboardCertificateQrCodeState.canRender === true,
      canLoadParticipantDashboardCertificateQrCode: participantDashboardCertificateQrCodeState.canLoadCertificateQrCode === true,
      hasParticipantDashboardCertificateQrCodeData: participantDashboardCertificateQrCodeState.hasCertificateQrCodeData === true,
      canShowParticipantDashboardCertificateQrCodeButton: participantDashboardCertificateQrCodeState.canShowCertificateQrCodeButton === true,
      canOpenParticipantDashboardCertificateQrCodeDialog: participantDashboardCertificateQrCodeState.canOpenCertificateQrCodeDialog === true,
      canCreateParticipantDashboardCertificateQrCode: participantDashboardCertificateQrCodeState.canCreateCertificateQrCode === true,
      canRenderParticipantDashboardCertificateQrCodeImage: participantDashboardCertificateQrCodeState.canRenderCertificateQrCodeImage === true,
      canDownloadParticipantDashboardCertificateQrCode: participantDashboardCertificateQrCodeState.canDownloadCertificateQrCode === true,
      canBlockParticipantDashboardByCertificateQrCode: participantDashboardCertificateQrCodeState.canBlockDashboardAccess === true,
      participantDashboardCertificateValidityStatus: participantDashboardCertificateValidityState.status,
      isParticipantDashboardCertificateValidityAvailable: participantDashboardCertificateValidityState.isAvailable === true,
      isParticipantDashboardCertificateValidityVisible: participantDashboardCertificateValidityState.isVisible === true,
      canRenderParticipantDashboardCertificateValidity: participantDashboardCertificateValidityState.canRender === true,
      canLoadParticipantDashboardCertificateValidity: participantDashboardCertificateValidityState.canLoadCertificateValidity === true,
      hasParticipantDashboardCertificateValidityData: participantDashboardCertificateValidityState.hasCertificateValidityData === true,
      canShowParticipantDashboardCertificateValidityButton: participantDashboardCertificateValidityState.canShowCertificateValidityButton === true,
      canOpenParticipantDashboardCertificateValidityDialog: participantDashboardCertificateValidityState.canOpenCertificateValidityDialog === true,
      canCheckParticipantDashboardCertificateValidity: participantDashboardCertificateValidityState.canCheckCertificateValidity === true,
      canRefreshParticipantDashboardCertificateValidity: participantDashboardCertificateValidityState.canRefreshCertificateValidity === true,
      canShowParticipantDashboardCertificateValidBadge: participantDashboardCertificateValidityState.canShowCertificateValidBadge === true,
      canShowParticipantDashboardCertificateExpiredBadge: participantDashboardCertificateValidityState.canShowCertificateExpiredBadge === true,
      canShowParticipantDashboardCertificateRevokedBadge: participantDashboardCertificateValidityState.canShowCertificateRevokedBadge === true,
      canBlockParticipantDashboardByCertificateValidity: participantDashboardCertificateValidityState.canBlockDashboardAccess === true,
      participantDashboardCertificateRevocationStatus: participantDashboardCertificateRevocationState.status,
      isParticipantDashboardCertificateRevocationAvailable: participantDashboardCertificateRevocationState.isAvailable === true,
      isParticipantDashboardCertificateRevocationVisible: participantDashboardCertificateRevocationState.isVisible === true,
      canRenderParticipantDashboardCertificateRevocation: participantDashboardCertificateRevocationState.canRender === true,
      canLoadParticipantDashboardCertificateRevocation: participantDashboardCertificateRevocationState.canLoadCertificateRevocation === true,
      hasParticipantDashboardCertificateRevocationData: participantDashboardCertificateRevocationState.hasCertificateRevocationData === true,
      canShowParticipantDashboardCertificateRevocationButton: participantDashboardCertificateRevocationState.canShowCertificateRevocationButton === true,
      canOpenParticipantDashboardCertificateRevocationDialog: participantDashboardCertificateRevocationState.canOpenCertificateRevocationDialog === true,
      canRequestParticipantDashboardCertificateRevocation: participantDashboardCertificateRevocationState.canRequestCertificateRevocation === true,
      canConfirmParticipantDashboardCertificateRevocation: participantDashboardCertificateRevocationState.canConfirmCertificateRevocation === true,
      canCancelParticipantDashboardCertificateRevocation: participantDashboardCertificateRevocationState.canCancelCertificateRevocation === true,
      canShowParticipantDashboardCertificateRevokedNotice: participantDashboardCertificateRevocationState.canShowCertificateRevokedNotice === true,
      canBlockParticipantDashboardByCertificateRevocation: participantDashboardCertificateRevocationState.canBlockDashboardAccess === true,
      participantDashboardCertificateAuditLogStatus: participantDashboardCertificateAuditLogState.status,
      isParticipantDashboardCertificateAuditLogAvailable: participantDashboardCertificateAuditLogState.isAvailable === true,
      isParticipantDashboardCertificateAuditLogVisible: participantDashboardCertificateAuditLogState.isVisible === true,
      canRenderParticipantDashboardCertificateAuditLog: participantDashboardCertificateAuditLogState.canRender === true,
      canLoadParticipantDashboardCertificateAuditLog: participantDashboardCertificateAuditLogState.canLoadCertificateAuditLog === true,
      hasParticipantDashboardCertificateAuditLogData: participantDashboardCertificateAuditLogState.hasCertificateAuditLogData === true,
      canShowParticipantDashboardCertificateAuditLogButton: participantDashboardCertificateAuditLogState.canShowCertificateAuditLogButton === true,
      canShowParticipantDashboardCertificateAuditLogList: participantDashboardCertificateAuditLogState.canShowCertificateAuditLogList === true,
      canOpenParticipantDashboardCertificateAuditLogDialog: participantDashboardCertificateAuditLogState.canOpenCertificateAuditLogDialog === true,
      canRefreshParticipantDashboardCertificateAuditLog: participantDashboardCertificateAuditLogState.canRefreshCertificateAuditLog === true,
      canExportParticipantDashboardCertificateAuditLog: participantDashboardCertificateAuditLogState.canExportCertificateAuditLog === true,
      canBlockParticipantDashboardByCertificateAuditLog: participantDashboardCertificateAuditLogState.canBlockDashboardAccess === true,
      participantDashboardCertificateConsentStatus: participantDashboardCertificateConsentState.status,
      isParticipantDashboardCertificateConsentAvailable: participantDashboardCertificateConsentState.isAvailable === true,
      isParticipantDashboardCertificateConsentVisible: participantDashboardCertificateConsentState.isVisible === true,
      canRenderParticipantDashboardCertificateConsent: participantDashboardCertificateConsentState.canRender === true,
      canLoadParticipantDashboardCertificateConsent: participantDashboardCertificateConsentState.canLoadCertificateConsent === true,
      hasParticipantDashboardCertificateConsentData: participantDashboardCertificateConsentState.hasCertificateConsentData === true,
      canShowParticipantDashboardCertificateConsentButton: participantDashboardCertificateConsentState.canShowCertificateConsentButton === true,
      canOpenParticipantDashboardCertificateConsentDialog: participantDashboardCertificateConsentState.canOpenCertificateConsentDialog === true,
      canGrantParticipantDashboardCertificateConsent: participantDashboardCertificateConsentState.canGrantCertificateConsent === true,
      canRevokeParticipantDashboardCertificateConsent: participantDashboardCertificateConsentState.canRevokeCertificateConsent === true,
      canRefreshParticipantDashboardCertificateConsent: participantDashboardCertificateConsentState.canRefreshCertificateConsent === true,
      canBlockParticipantDashboardByCertificateConsent: participantDashboardCertificateConsentState.canBlockDashboardAccess === true,
      participantDashboardCertificatePrivacyNoticeStatus: participantDashboardCertificatePrivacyNoticeState.status,
      isParticipantDashboardCertificatePrivacyNoticeAvailable: participantDashboardCertificatePrivacyNoticeState.isAvailable === true,
      isParticipantDashboardCertificatePrivacyNoticeVisible: participantDashboardCertificatePrivacyNoticeState.isVisible === true,
      canRenderParticipantDashboardCertificatePrivacyNotice: participantDashboardCertificatePrivacyNoticeState.canRender === true,
      canLoadParticipantDashboardCertificatePrivacyNotice: participantDashboardCertificatePrivacyNoticeState.canLoadCertificatePrivacyNotice === true,
      hasParticipantDashboardCertificatePrivacyNoticeData: participantDashboardCertificatePrivacyNoticeState.hasCertificatePrivacyNoticeData === true,
      canShowParticipantDashboardCertificatePrivacyNoticeButton: participantDashboardCertificatePrivacyNoticeState.canShowCertificatePrivacyNoticeButton === true,
      canShowParticipantDashboardCertificatePrivacyNoticeText: participantDashboardCertificatePrivacyNoticeState.canShowCertificatePrivacyNoticeText === true,
      canOpenParticipantDashboardCertificatePrivacyNoticeDialog: participantDashboardCertificatePrivacyNoticeState.canOpenCertificatePrivacyNoticeDialog === true,
      canAcceptParticipantDashboardCertificatePrivacyNotice: participantDashboardCertificatePrivacyNoticeState.canAcceptCertificatePrivacyNotice === true,
      canRefreshParticipantDashboardCertificatePrivacyNotice: participantDashboardCertificatePrivacyNoticeState.canRefreshCertificatePrivacyNotice === true,
      canBlockParticipantDashboardByCertificatePrivacyNotice: participantDashboardCertificatePrivacyNoticeState.canBlockDashboardAccess === true,
      participantDashboardCertificateRetentionStatus: participantDashboardCertificateRetentionState.status,
      isParticipantDashboardCertificateRetentionAvailable: participantDashboardCertificateRetentionState.isAvailable === true,
      isParticipantDashboardCertificateRetentionVisible: participantDashboardCertificateRetentionState.isVisible === true,
      canRenderParticipantDashboardCertificateRetention: participantDashboardCertificateRetentionState.canRender === true,
      canLoadParticipantDashboardCertificateRetention: participantDashboardCertificateRetentionState.canLoadCertificateRetention === true,
      hasParticipantDashboardCertificateRetentionData: participantDashboardCertificateRetentionState.hasCertificateRetentionData === true,
      canShowParticipantDashboardCertificateRetentionButton: participantDashboardCertificateRetentionState.canShowCertificateRetentionButton === true,
      canOpenParticipantDashboardCertificateRetentionDialog: participantDashboardCertificateRetentionState.canOpenCertificateRetentionDialog === true,
      canRequestParticipantDashboardCertificateDeletion: participantDashboardCertificateRetentionState.canRequestCertificateDeletion === true,
      canConfirmParticipantDashboardCertificateDeletion: participantDashboardCertificateRetentionState.canConfirmCertificateDeletion === true,
      canRefreshParticipantDashboardCertificateRetention: participantDashboardCertificateRetentionState.canRefreshCertificateRetention === true,
      canBlockParticipantDashboardByCertificateRetention: participantDashboardCertificateRetentionState.canBlockDashboardAccess === true,
      participantDashboardCertificateDataAccessStatus: participantDashboardCertificateDataAccessState.status,
      isParticipantDashboardCertificateDataAccessAvailable: participantDashboardCertificateDataAccessState.isAvailable === true,
      isParticipantDashboardCertificateDataAccessVisible: participantDashboardCertificateDataAccessState.isVisible === true,
      canRenderParticipantDashboardCertificateDataAccess: participantDashboardCertificateDataAccessState.canRender === true,
      canLoadParticipantDashboardCertificateDataAccess: participantDashboardCertificateDataAccessState.canLoadCertificateDataAccess === true,
      hasParticipantDashboardCertificateDataAccessData: participantDashboardCertificateDataAccessState.hasCertificateDataAccessData === true,
      canShowParticipantDashboardCertificateDataAccessButton: participantDashboardCertificateDataAccessState.canShowCertificateDataAccessButton === true,
      canOpenParticipantDashboardCertificateDataAccessDialog: participantDashboardCertificateDataAccessState.canOpenCertificateDataAccessDialog === true,
      canRequestParticipantDashboardCertificateDataAccess: participantDashboardCertificateDataAccessState.canRequestCertificateDataAccess === true,
      canPrepareParticipantDashboardCertificateDataExport: participantDashboardCertificateDataAccessState.canPrepareCertificateDataExport === true,
      canDownloadParticipantDashboardCertificateDataExport: participantDashboardCertificateDataAccessState.canDownloadCertificateDataExport === true,
      canRefreshParticipantDashboardCertificateDataAccess: participantDashboardCertificateDataAccessState.canRefreshCertificateDataAccess === true,
      canBlockParticipantDashboardByCertificateDataAccess: participantDashboardCertificateDataAccessState.canBlockDashboardAccess === true,
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
    const loginSuccessState = getLoginSuccessState();
    const logoutState = getLogoutState();
    const participantDashboardAuthState = getParticipantDashboardAuthState();
    const participantDashboardCourseAccessState = getParticipantDashboardCourseAccessState();
    const participantDashboardExpiryState = getParticipantDashboardExpiryState();
    const participantDashboardAccessDecisionState = getParticipantDashboardAccessDecisionState();
    const participantDashboardReadinessState = getParticipantDashboardReadinessState();
    const participantDashboardStatusBadgeState = getParticipantDashboardStatusBadgeState();
    const participantDashboardNoticeBannerState = getParticipantDashboardNoticeBannerState();
    const participantDashboardProfileHeaderState = getParticipantDashboardProfileHeaderState();
    const participantDashboardCourseCardState = getParticipantDashboardCourseCardState();
    const participantDashboardProgressState = getParticipantDashboardProgressState();
    const participantDashboardActivityListState = getParticipantDashboardActivityListState();
    const participantDashboardRecommendationsState = getParticipantDashboardRecommendationsState();
    const participantDashboardExamStatusState = getParticipantDashboardExamStatusState();
    const participantDashboardCertificateState = getParticipantDashboardCertificateState();
    const participantDashboardDocumentsState = getParticipantDashboardDocumentsState();
    const participantDashboardMessagesState = getParticipantDashboardMessagesState();
    const participantDashboardSupportState = getParticipantDashboardSupportState();
    const participantDashboardAppointmentsState = getParticipantDashboardAppointmentsState();
    const participantDashboardPaymentStatusState = getParticipantDashboardPaymentStatusState();
    const participantDashboardContractStatusState = getParticipantDashboardContractStatusState();
    const participantDashboardInvoicesState = getParticipantDashboardInvoicesState();
    const participantDashboardAttendanceState = getParticipantDashboardAttendanceState();
    const participantDashboardLessonPlanState = getParticipantDashboardLessonPlanState();
    const participantDashboardCourseMaterialsState = getParticipantDashboardCourseMaterialsState();
    const participantDashboardLearningProgressDetailsState = getParticipantDashboardLearningProgressDetailsState();
    const participantDashboardMistakeTrainingDetailsState = getParticipantDashboardMistakeTrainingDetailsState();
    const participantDashboardExamSimulationDetailsState = getParticipantDashboardExamSimulationDetailsState();
    const participantDashboardOralExamDetailsState = getParticipantDashboardOralExamDetailsState();
    const participantDashboardFlashcardsDetailsState = getParticipantDashboardFlashcardsDetailsState();
    const participantDashboardSampleQuestionsDetailsState = getParticipantDashboardSampleQuestionsDetailsState();
    const participantDashboardExamHistoryState = getParticipantDashboardExamHistoryState();
    const participantDashboardExamHistoryDataSourceState = getParticipantDashboardExamHistoryDataSourceState();
    const participantExamResultHistoryRpcState = getParticipantExamResultHistoryRpcState();
    const participantDashboardCertificateHistoryState = getParticipantDashboardCertificateHistoryState();
    const participantDashboardCertificateDownloadState = getParticipantDashboardCertificateDownloadState();
    const participantDashboardCertificatePreviewState = getParticipantDashboardCertificatePreviewState();
    const participantDashboardCertificatePrintState = getParticipantDashboardCertificatePrintState();
    const participantDashboardCertificateShareState = getParticipantDashboardCertificateShareState();
    const participantDashboardCertificateVerificationState = getParticipantDashboardCertificateVerificationState();
    const participantDashboardCertificateQrCodeState = getParticipantDashboardCertificateQrCodeState();
    const participantDashboardCertificateValidityState = getParticipantDashboardCertificateValidityState();
    const participantDashboardCertificateRevocationState = getParticipantDashboardCertificateRevocationState();
    const participantDashboardCertificateAuditLogState = getParticipantDashboardCertificateAuditLogState();
    const participantDashboardCertificateConsentState = getParticipantDashboardCertificateConsentState();
    const participantDashboardCertificatePrivacyNoticeState = getParticipantDashboardCertificatePrivacyNoticeState();
    const participantDashboardCertificateRetentionState = getParticipantDashboardCertificateRetentionState();
    const participantDashboardCertificateDataAccessState = getParticipantDashboardCertificateDataAccessState();
    const failSafeState = getSupabaseFailSafeState();
    const configLoaderState = getSupabaseConfigLoaderState();
    const configLoaderBootState = getSupabaseConfigLoaderBootState();
    const safetySummary = getSupabaseSafetySummary();

    return {
      version: "v26.75a",
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
      loginSuccessState,
      logoutState,
      participantDashboardAuthState,
      participantDashboardCourseAccessState,
      participantDashboardExpiryState,
      participantDashboardAccessDecisionState,
      participantDashboardReadinessState,
      participantDashboardStatusBadgeState,
      participantDashboardNoticeBannerState,
      participantDashboardProfileHeaderState,
      participantDashboardCourseCardState,
      participantDashboardProgressState,
      participantDashboardActivityListState,
      participantDashboardRecommendationsState,
      participantDashboardExamStatusState,
      participantDashboardCertificateState,
      participantDashboardDocumentsState,
      participantDashboardMessagesState,
      participantDashboardSupportState,
      participantDashboardAppointmentsState,
      participantDashboardPaymentStatusState,
      participantDashboardContractStatusState,
      participantDashboardInvoicesState,
      participantDashboardAttendanceState,
      participantDashboardLessonPlanState,
      participantDashboardCourseMaterialsState,
      participantDashboardLearningProgressDetailsState,
      participantDashboardMistakeTrainingDetailsState,
      participantDashboardExamSimulationDetailsState,
      participantDashboardOralExamDetailsState,
      participantDashboardFlashcardsDetailsState,
      participantDashboardSampleQuestionsDetailsState,
      participantDashboardExamHistoryState,
      participantDashboardExamHistoryDataSourceState,
      participantExamResultHistoryRpcState,
      participantDashboardCertificateHistoryState,
      participantDashboardCertificateDownloadState,
      participantDashboardCertificatePreviewState,
      participantDashboardCertificatePrintState,
      participantDashboardCertificateShareState,
      participantDashboardCertificateVerificationState,
      participantDashboardCertificateQrCodeState,
      participantDashboardCertificateValidityState,
      participantDashboardCertificateRevocationState,
      participantDashboardCertificateAuditLogState,
      participantDashboardCertificateConsentState,
      participantDashboardCertificatePrivacyNoticeState,
      participantDashboardCertificateRetentionState,
      participantDashboardCertificateDataAccessState,
      failSafeState,
      configLoaderState,
      configLoaderBootState,
      safetySummary
    };
  }

  window.ACCAOUI_SUPABASE_ADAPTER = {
    version: "v27.29l",
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
    getLoginSuccessState,
    getLogoutState,
    getParticipantDashboardAuthState,
    getParticipantDashboardCourseAccessState,
    getParticipantDashboardExpiryState,
    getParticipantDashboardAccessDecisionState,
    getParticipantDashboardReadinessState,
    getParticipantDashboardStatusBadgeState,
    getParticipantDashboardNoticeBannerState,
    getParticipantDashboardProfileHeaderState,
    getParticipantDashboardCourseCardState,
    getParticipantDashboardProgressState,
    getParticipantDashboardActivityListState,
    getParticipantDashboardRecommendationsState,
    getParticipantDashboardExamStatusState,
    getParticipantDashboardCertificateState,
    getParticipantDashboardDocumentsState,
    getParticipantDashboardMessagesState,
    getParticipantDashboardSupportState,
    getParticipantDashboardAppointmentsState,
    getParticipantDashboardPaymentStatusState,
    getParticipantDashboardContractStatusState,
    getParticipantDashboardInvoicesState,
    getParticipantDashboardAttendanceState,
    getParticipantDashboardLessonPlanState,
    getParticipantDashboardCourseMaterialsState,
    getParticipantDashboardLearningProgressDetailsState,
    getParticipantDashboardMistakeTrainingDetailsState,
    getParticipantDashboardExamSimulationDetailsState,
    getParticipantDashboardOralExamDetailsState,
    getParticipantDashboardFlashcardsDetailsState,
    getParticipantDashboardSampleQuestionsDetailsState,
    getParticipantDashboardExamHistoryDataSourceState,
    getParticipantDashboardExamHistoryState,
    getParticipantExamResultHistoryRpcState,
    normalizeParticipantFullExamResultRow,
    normalizeParticipantFullExamResultRows,
    aggregateParticipantFullExamResultRows,
    mapParticipantFullExamResultHistoryResponse,
    mapParticipantFullExamResultHistoryLoadState,
    mapParticipantFullExamResultHistoryPaginationState,
    orchestrateParticipantFullExamResultHistoryDataSourceState,
    mapParticipantFullExamResultHistoryNavigationIntent,
    listParticipantFullExamResults,
    getParticipantDashboardCertificateHistoryState,
    getParticipantDashboardCertificateDownloadState,
    getParticipantDashboardCertificatePreviewState,
    getParticipantDashboardCertificatePrintState,
    getParticipantDashboardCertificateShareState,
    getParticipantDashboardCertificateVerificationState,
    getParticipantDashboardCertificateQrCodeState,
    getParticipantDashboardCertificateValidityState,
    getParticipantDashboardCertificateRevocationState,
    getParticipantDashboardCertificateAuditLogState,
    getParticipantDashboardCertificateConsentState,
    getParticipantDashboardCertificatePrivacyNoticeState,
    getParticipantDashboardCertificateRetentionState,
    getParticipantDashboardCertificateDataAccessState,
    getParticipantDashboardCertificateDataCorrectionState,
    getParticipantDashboardCertificateDataDeletionRequestState,
    getParticipantDashboardCertificateDataDeletionConfirmationState,
    getParticipantDashboardCertificateDataExportFileState,
    getParticipantDashboardCertificateDataExportExpiryState,
    getParticipantDashboardCertificateDataExportDownloadLogState,
    getParticipantDashboardCertificateDataExportErrorState,
    getParticipantDashboardCertificateDataExportRetryState,
    getParticipantDashboardCertificateDataExportStatusSummaryState,
    getParticipantDashboardCertificateDataExportNotificationState,
    getParticipantDashboardCertificateDataExportDeliveryStatusState,
    getParticipantDashboardCertificateDataExportReadReceiptState,
    getParticipantDashboardCertificateDataExportCompletionStatusState,
    getParticipantDashboardCertificateDataExportArchiveStatusState,
    getParticipantDashboardCertificateDataExportDeletionStatusState,
    getParticipantDashboardCertificateDataExportRetentionStatusState,
    getParticipantDashboardCertificateDataExportSecurityStatusState,
    getParticipantDashboardCertificateDataExportIntegrityStatusState,
    getParticipantDashboardCertificateDataExportAuditStatusState,
    getParticipantDashboardCertificateDataExportAuditTrailStatusState,
    getParticipantDashboardCertificateDataExportApprovalStatusState,
    getParticipantDashboardCertificateDataExportRejectionStatusState,
    getParticipantDashboardCertificateDataExportPendingStatusState,
    getParticipantDashboardCertificateDataExportReviewStatusState,
    getParticipantDashboardCertificateDataExportFinalStatusState,
    getParticipantDashboardCertificateDataExportHandoverStatusState,
    getParticipantDashboardCertificateDataExportReceptionStatusState,
    getParticipantDashboardCertificateDataExportConfirmationStatusState,
    getParticipantDashboardCertificateDataExportReleaseStatusState,
    getParticipantDashboardCertificateDataExportRetrievalStatusState,
    getParticipantDashboardCertificateDataExportProtocolStatusState,
    getParticipantDashboardCertificateDataExportHandoverProtocolStatusState,
    getParticipantDashboardCertificateDataExportCompletionProtocolStatusState,
    getParticipantDashboardCertificateDataExportFinalProofStatusState,
    getParticipantDashboardCertificateDataExportSubmissionConfirmationStatusState,
    getParticipantDashboardCertificateDataExportReceiptConfirmationStatusState,
    getParticipantDashboardCertificateDataExportDeliveryProofStatusState,
    getParticipantDashboardCertificateDataExportProofArchiveStatusState,
    getParticipantDashboardCertificateDataExportProofReleaseStatusState,
    getParticipantDashboardCertificateDataExportProofBlockStatusState,
    getParticipantDashboardCertificateDataExportProofCheckStatusState,
    getParticipantDashboardCertificateDataExportProofValidationStatusState,
    getParticipantDashboardCertificateDataExportProofReleaseCheckStatusState,
    getParticipantAccessReadinessState,
    getParticipantAccessState,
    getAdapterHealthState
  };

  console.info("Accaoui Supabase Adapter geladen:", window.ACCAOUI_SUPABASE_ADAPTER.version);
})();
