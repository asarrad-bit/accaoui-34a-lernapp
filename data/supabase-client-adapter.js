// Accaoui §34a Lern-App – Supabase Client Adapter
// Stand: v27.30r
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
      requestIdentityMapperName:
        "mapParticipantFullExamResultHistoryRequestIdentity",
      isRequestIdentityMapperPrepared: true,
      canMapRequestIdentities: true,
      initialRequestIdentityState:
        mapParticipantFullExamResultHistoryRequestIdentity({
          mode: "create",
          requestSequence: 1,
          request: {
            limit: rpcState.defaultLimit,
            offset: 0
          }
        }),
      responseAcceptanceGuardName:
        "guardParticipantFullExamResultHistoryResponseAcceptance",
      isResponseAcceptanceGuardPrepared: true,
      canGuardResponseAcceptance: true,
      initialResponseAcceptanceState: null,
      requestLifecycleMapperName:
        "mapParticipantFullExamResultHistoryRequestLifecycle",
      isRequestLifecycleMapperPrepared: true,
      canMapRequestLifecycles: true,
      initialRequestLifecycleState:
        mapParticipantFullExamResultHistoryRequestLifecycle({
          phase: "prepared",
          requestSequence: 1,
          request: {
            limit: rpcState.defaultLimit,
            offset: 0
          }
        }),
      requestLifecycleTransitionGuardName:
        "guardParticipantFullExamResultHistoryRequestLifecycleTransition",
      isRequestLifecycleTransitionGuardPrepared: true,
      canGuardRequestLifecycleTransitions: true,
      initialRequestLifecycleTransitionState: null,
      requestControllerMapperName:
        "mapParticipantFullExamResultHistoryRequestControllerState",
      isRequestControllerMapperPrepared: true,
      canMapRequestControllerStates: true,
      initialRequestControllerState:
        mapParticipantFullExamResultHistoryRequestControllerState({
          action: "initialize",
          requestSequence: 1,
          request: {
            limit: rpcState.defaultLimit,
            offset: 0
          }
        }),
      controllerSnapshotNormalizerName:
        "normalizeParticipantFullExamResultHistoryControllerSnapshot",
      isControllerSnapshotNormalizerPrepared: true,
      canNormalizeControllerSnapshots: true,
      initialControllerSnapshotState: null,
      snapshotResumeMapperName:
        "mapParticipantFullExamResultHistorySnapshotResumeState",
      isSnapshotResumeMapperPrepared: true,
      canMapSnapshotResumeStates: true,
      initialSnapshotResumeState: null,
      snapshotCreationMapperName:
        "mapParticipantFullExamResultHistorySnapshotCreationState",
      isSnapshotCreationMapperPrepared: true,
      canMapSnapshotCreationStates: true,
      initialSnapshotCreationState: null,
      snapshotSerializationMapperName:
        "mapParticipantFullExamResultHistorySnapshotSerializationState",
      isSnapshotSerializationMapperPrepared: true,
      canMapSnapshotSerializationStates: true,
      initialSnapshotSerializationState: null,
      snapshotDeserializationMapperName:
        "mapParticipantFullExamResultHistorySnapshotDeserializationState",
      isSnapshotDeserializationMapperPrepared: true,
      canMapSnapshotDeserializationStates: true,
      initialSnapshotDeserializationState: null,
      snapshotPersistenceContractName:
        "mapParticipantFullExamResultHistorySnapshotPersistenceContract",
      isSnapshotPersistenceContractPrepared: true,
      canMapSnapshotPersistenceIntents: true,
      initialSnapshotPersistenceState: null,
      snapshotStorageAdapterReadinessMapperName:
        "mapParticipantFullExamResultHistorySnapshotStorageAdapterReadiness",
      isSnapshotStorageAdapterReadinessPrepared: true,
      canInspectSnapshotStorageAdapters: true,
      initialSnapshotStorageAdapterReadinessState: null,
      snapshotPersistenceOperationPlanMapperName:
        "mapParticipantFullExamResultHistorySnapshotPersistenceOperationPlan",
      isSnapshotPersistenceOperationPlanPrepared: true,
      canMapSnapshotPersistenceOperationPlans: true,
      initialSnapshotPersistenceOperationPlanState: null,
      snapshotPersistenceOperationReleaseMapperName:
        "mapParticipantFullExamResultHistorySnapshotPersistenceOperationReleaseState",
      isSnapshotPersistenceOperationReleasePrepared: true,
      canMapSnapshotPersistenceOperationReleases: true,
      initialSnapshotPersistenceOperationReleaseState: null,
      snapshotPersistenceExecutionGuardName:
        "guardParticipantFullExamResultHistorySnapshotPersistenceExecution",
      isSnapshotPersistenceExecutionGuardPrepared: true,
      canGuardSnapshotPersistenceExecutions: true,
      initialSnapshotPersistenceExecutionState: null,
      snapshotPersistenceInvocationContractName:
        "mapParticipantFullExamResultHistorySnapshotPersistenceInvocationContract",
      isSnapshotPersistenceInvocationContractPrepared: true,
      canMapSnapshotPersistenceInvocationContracts: true,
      initialSnapshotPersistenceInvocationContractState: null,
      snapshotPersistenceInvocationPackageMapperName:
        "mapParticipantFullExamResultHistorySnapshotPersistenceInvocationPackageState",
      isSnapshotPersistenceInvocationPackagePrepared: true,
      canMapSnapshotPersistenceInvocationPackages: true,
      initialSnapshotPersistenceInvocationPackageState: null,
      snapshotPersistenceResultContractName:
        "mapParticipantFullExamResultHistorySnapshotPersistenceResultContract",
      isSnapshotPersistenceResultContractPrepared: true,
      canMapSnapshotPersistenceResults: true,
      initialSnapshotPersistenceResultState: null,
      snapshotPersistenceResultAcceptanceGuardName:
        "guardParticipantFullExamResultHistorySnapshotPersistenceResultAcceptance",
      isSnapshotPersistenceResultAcceptanceGuardPrepared: true,
      canGuardSnapshotPersistenceResultAcceptance: true,
      initialSnapshotPersistenceResultAcceptanceState: null,
      snapshotPersistenceCompletionMapperName:
        "mapParticipantFullExamResultHistorySnapshotPersistenceCompletionState",
      isSnapshotPersistenceCompletionMapperPrepared: true,
      canMapSnapshotPersistenceCompletionStates: true,
      initialSnapshotPersistenceCompletionState: null,
      snapshotPersistenceCycleMapperName:
        "mapParticipantFullExamResultHistorySnapshotPersistenceCycleState",
      isSnapshotPersistenceCycleMapperPrepared: true,
      canMapSnapshotPersistenceCycleStates: true,
      initialSnapshotPersistenceCycleState: null,
      snapshotPersistenceCycleRepetitionGuardName:
        "guardParticipantFullExamResultHistorySnapshotPersistenceCycleRepetition",
      isSnapshotPersistenceCycleRepetitionGuardPrepared: true,
      canGuardSnapshotPersistenceCycleRepetitions: true,
      initialSnapshotPersistenceCycleRepetitionState: null,
      snapshotPersistenceCycleRegistryMapperName:
        "mapParticipantFullExamResultHistorySnapshotPersistenceCycleRegistryState",
      isSnapshotPersistenceCycleRegistryMapperPrepared: true,
      canMapSnapshotPersistenceCycleRegistryStates: true,
      initialSnapshotPersistenceCycleRegistryState: null,
      snapshotPersistenceCycleRegistrySerializationMapperName:
        "mapParticipantFullExamResultHistorySnapshotPersistenceCycleRegistrySerializationState",
      isSnapshotPersistenceCycleRegistrySerializationMapperPrepared: true,
      canMapSnapshotPersistenceCycleRegistrySerializationStates: true,
      initialSnapshotPersistenceCycleRegistrySerializationState: null,
      snapshotPersistenceCycleRegistryDeserializationMapperName:
        "mapParticipantFullExamResultHistorySnapshotPersistenceCycleRegistryDeserializationState",
      isSnapshotPersistenceCycleRegistryDeserializationMapperPrepared: true,
      canMapSnapshotPersistenceCycleRegistryDeserializationStates: true,
      initialSnapshotPersistenceCycleRegistryDeserializationState: null,
      snapshotPersistenceCycleRegistryContractName:
        "mapParticipantFullExamResultHistorySnapshotPersistenceCycleRegistryContract",
      isSnapshotPersistenceCycleRegistryContractPrepared: true,
      canMapSnapshotPersistenceCycleRegistryIntents: true,
      initialSnapshotPersistenceCycleRegistryContractState: null,
      snapshotPersistenceCycleRegistryStorageAdapterReadinessMapperName:
        "mapParticipantFullExamResultHistorySnapshotPersistenceCycleRegistryStorageAdapterReadinessState",
      isSnapshotPersistenceCycleRegistryStorageAdapterReadinessMapperPrepared: true,
      canMapSnapshotPersistenceCycleRegistryStorageAdapterReadinessStates: true,
      initialSnapshotPersistenceCycleRegistryStorageAdapterReadinessState: null,
      snapshotPersistenceCycleRegistryOperationPlanMapperName:
        "mapParticipantFullExamResultHistorySnapshotPersistenceCycleRegistryOperationPlanState",
      isSnapshotPersistenceCycleRegistryOperationPlanMapperPrepared: true,
      canMapSnapshotPersistenceCycleRegistryOperationPlanStates: true,
      initialSnapshotPersistenceCycleRegistryOperationPlanState: null,
      snapshotPersistenceCycleRegistryOperationReleaseMapperName:
        "mapParticipantFullExamResultHistorySnapshotPersistenceCycleRegistryOperationReleaseState",
      isSnapshotPersistenceCycleRegistryOperationReleaseMapperPrepared: true,
      canMapSnapshotPersistenceCycleRegistryOperationReleaseStates: true,
      initialSnapshotPersistenceCycleRegistryOperationReleaseState: null,
      snapshotPersistenceCycleRegistryExecutionGuardName:
        "guardParticipantFullExamResultHistorySnapshotPersistenceCycleRegistryExecution",
      isSnapshotPersistenceCycleRegistryExecutionGuardPrepared: true,
      canGuardSnapshotPersistenceCycleRegistryExecutions: true,
      initialSnapshotPersistenceCycleRegistryExecutionState: null,
      snapshotPersistenceCycleRegistryInvocationContractName:
        "mapParticipantFullExamResultHistorySnapshotPersistenceCycleRegistryInvocationContract",
      isSnapshotPersistenceCycleRegistryInvocationContractPrepared: true,
      canMapSnapshotPersistenceCycleRegistryInvocationContracts: true,
      initialSnapshotPersistenceCycleRegistryInvocationContractState: null,
      snapshotPersistenceCycleRegistryInvocationPackageMapperName:
        "mapParticipantFullExamResultHistorySnapshotPersistenceCycleRegistryInvocationPackageState",
      isSnapshotPersistenceCycleRegistryInvocationPackageMapperPrepared: true,
      canMapSnapshotPersistenceCycleRegistryInvocationPackages: true,
      initialSnapshotPersistenceCycleRegistryInvocationPackageState: null,
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
      dataSourceRequestIdentityMapperName: participantDashboardExamHistoryDataSourceState.requestIdentityMapperName,
      isDataSourceRequestIdentityMapperPrepared: participantDashboardExamHistoryDataSourceState.isRequestIdentityMapperPrepared === true,
      canMapDataSourceRequestIdentities: participantDashboardExamHistoryDataSourceState.canMapRequestIdentities === true,
      dataSourceInitialRequestIdentityState: participantDashboardExamHistoryDataSourceState.initialRequestIdentityState,
      dataSourceResponseAcceptanceGuardName: participantDashboardExamHistoryDataSourceState.responseAcceptanceGuardName,
      isDataSourceResponseAcceptanceGuardPrepared: participantDashboardExamHistoryDataSourceState.isResponseAcceptanceGuardPrepared === true,
      canGuardDataSourceResponseAcceptance: participantDashboardExamHistoryDataSourceState.canGuardResponseAcceptance === true,
      dataSourceInitialResponseAcceptanceState: participantDashboardExamHistoryDataSourceState.initialResponseAcceptanceState,
      dataSourceRequestLifecycleMapperName: participantDashboardExamHistoryDataSourceState.requestLifecycleMapperName,
      isDataSourceRequestLifecycleMapperPrepared: participantDashboardExamHistoryDataSourceState.isRequestLifecycleMapperPrepared === true,
      canMapDataSourceRequestLifecycles: participantDashboardExamHistoryDataSourceState.canMapRequestLifecycles === true,
      dataSourceInitialRequestLifecycleState: participantDashboardExamHistoryDataSourceState.initialRequestLifecycleState,
      dataSourceRequestLifecycleTransitionGuardName: participantDashboardExamHistoryDataSourceState.requestLifecycleTransitionGuardName,
      isDataSourceRequestLifecycleTransitionGuardPrepared: participantDashboardExamHistoryDataSourceState.isRequestLifecycleTransitionGuardPrepared === true,
      canGuardDataSourceRequestLifecycleTransitions: participantDashboardExamHistoryDataSourceState.canGuardRequestLifecycleTransitions === true,
      dataSourceInitialRequestLifecycleTransitionState: participantDashboardExamHistoryDataSourceState.initialRequestLifecycleTransitionState,
      dataSourceRequestControllerMapperName: participantDashboardExamHistoryDataSourceState.requestControllerMapperName,
      isDataSourceRequestControllerMapperPrepared: participantDashboardExamHistoryDataSourceState.isRequestControllerMapperPrepared === true,
      canMapDataSourceRequestControllerStates: participantDashboardExamHistoryDataSourceState.canMapRequestControllerStates === true,
      dataSourceInitialRequestControllerState: participantDashboardExamHistoryDataSourceState.initialRequestControllerState,
      dataSourceControllerSnapshotNormalizerName: participantDashboardExamHistoryDataSourceState.controllerSnapshotNormalizerName,
      isDataSourceControllerSnapshotNormalizerPrepared: participantDashboardExamHistoryDataSourceState.isControllerSnapshotNormalizerPrepared === true,
      canNormalizeDataSourceControllerSnapshots: participantDashboardExamHistoryDataSourceState.canNormalizeControllerSnapshots === true,
      dataSourceInitialControllerSnapshotState: participantDashboardExamHistoryDataSourceState.initialControllerSnapshotState,
      dataSourceSnapshotResumeMapperName: participantDashboardExamHistoryDataSourceState.snapshotResumeMapperName,
      isDataSourceSnapshotResumeMapperPrepared: participantDashboardExamHistoryDataSourceState.isSnapshotResumeMapperPrepared === true,
      canMapDataSourceSnapshotResumeStates: participantDashboardExamHistoryDataSourceState.canMapSnapshotResumeStates === true,
      dataSourceInitialSnapshotResumeState: participantDashboardExamHistoryDataSourceState.initialSnapshotResumeState,
      dataSourceSnapshotCreationMapperName: participantDashboardExamHistoryDataSourceState.snapshotCreationMapperName,
      isDataSourceSnapshotCreationMapperPrepared: participantDashboardExamHistoryDataSourceState.isSnapshotCreationMapperPrepared === true,
      canMapDataSourceSnapshotCreationStates: participantDashboardExamHistoryDataSourceState.canMapSnapshotCreationStates === true,
      dataSourceInitialSnapshotCreationState: participantDashboardExamHistoryDataSourceState.initialSnapshotCreationState,
      dataSourceSnapshotSerializationMapperName: participantDashboardExamHistoryDataSourceState.snapshotSerializationMapperName,
      isDataSourceSnapshotSerializationMapperPrepared: participantDashboardExamHistoryDataSourceState.isSnapshotSerializationMapperPrepared === true,
      canMapDataSourceSnapshotSerializationStates: participantDashboardExamHistoryDataSourceState.canMapSnapshotSerializationStates === true,
      dataSourceInitialSnapshotSerializationState: participantDashboardExamHistoryDataSourceState.initialSnapshotSerializationState,
      dataSourceSnapshotDeserializationMapperName: participantDashboardExamHistoryDataSourceState.snapshotDeserializationMapperName,
      isDataSourceSnapshotDeserializationMapperPrepared: participantDashboardExamHistoryDataSourceState.isSnapshotDeserializationMapperPrepared === true,
      canMapDataSourceSnapshotDeserializationStates: participantDashboardExamHistoryDataSourceState.canMapSnapshotDeserializationStates === true,
      dataSourceInitialSnapshotDeserializationState: participantDashboardExamHistoryDataSourceState.initialSnapshotDeserializationState,
      dataSourceSnapshotPersistenceContractName: participantDashboardExamHistoryDataSourceState.snapshotPersistenceContractName,
      isDataSourceSnapshotPersistenceContractPrepared: participantDashboardExamHistoryDataSourceState.isSnapshotPersistenceContractPrepared === true,
      canMapDataSourceSnapshotPersistenceIntents: participantDashboardExamHistoryDataSourceState.canMapSnapshotPersistenceIntents === true,
      dataSourceInitialSnapshotPersistenceState: participantDashboardExamHistoryDataSourceState.initialSnapshotPersistenceState,
      dataSourceSnapshotStorageAdapterReadinessMapperName: participantDashboardExamHistoryDataSourceState.snapshotStorageAdapterReadinessMapperName,
      isDataSourceSnapshotStorageAdapterReadinessPrepared: participantDashboardExamHistoryDataSourceState.isSnapshotStorageAdapterReadinessPrepared === true,
      canInspectDataSourceSnapshotStorageAdapters: participantDashboardExamHistoryDataSourceState.canInspectSnapshotStorageAdapters === true,
      dataSourceInitialSnapshotStorageAdapterReadinessState: participantDashboardExamHistoryDataSourceState.initialSnapshotStorageAdapterReadinessState,
      dataSourceSnapshotPersistenceOperationPlanMapperName: participantDashboardExamHistoryDataSourceState.snapshotPersistenceOperationPlanMapperName,
      isDataSourceSnapshotPersistenceOperationPlanPrepared: participantDashboardExamHistoryDataSourceState.isSnapshotPersistenceOperationPlanPrepared === true,
      canMapDataSourceSnapshotPersistenceOperationPlans: participantDashboardExamHistoryDataSourceState.canMapSnapshotPersistenceOperationPlans === true,
      dataSourceInitialSnapshotPersistenceOperationPlanState: participantDashboardExamHistoryDataSourceState.initialSnapshotPersistenceOperationPlanState,
      dataSourceSnapshotPersistenceOperationReleaseMapperName: participantDashboardExamHistoryDataSourceState.snapshotPersistenceOperationReleaseMapperName,
      isDataSourceSnapshotPersistenceOperationReleasePrepared: participantDashboardExamHistoryDataSourceState.isSnapshotPersistenceOperationReleasePrepared === true,
      canMapDataSourceSnapshotPersistenceOperationReleases: participantDashboardExamHistoryDataSourceState.canMapSnapshotPersistenceOperationReleases === true,
      dataSourceInitialSnapshotPersistenceOperationReleaseState: participantDashboardExamHistoryDataSourceState.initialSnapshotPersistenceOperationReleaseState,
      dataSourceSnapshotPersistenceExecutionGuardName: participantDashboardExamHistoryDataSourceState.snapshotPersistenceExecutionGuardName,
      isDataSourceSnapshotPersistenceExecutionGuardPrepared: participantDashboardExamHistoryDataSourceState.isSnapshotPersistenceExecutionGuardPrepared === true,
      canGuardDataSourceSnapshotPersistenceExecutions: participantDashboardExamHistoryDataSourceState.canGuardSnapshotPersistenceExecutions === true,
      dataSourceInitialSnapshotPersistenceExecutionState: participantDashboardExamHistoryDataSourceState.initialSnapshotPersistenceExecutionState,
      dataSourceSnapshotPersistenceInvocationContractName: participantDashboardExamHistoryDataSourceState.snapshotPersistenceInvocationContractName,
      isDataSourceSnapshotPersistenceInvocationContractPrepared: participantDashboardExamHistoryDataSourceState.isSnapshotPersistenceInvocationContractPrepared === true,
      canMapDataSourceSnapshotPersistenceInvocationContracts: participantDashboardExamHistoryDataSourceState.canMapSnapshotPersistenceInvocationContracts === true,
      dataSourceInitialSnapshotPersistenceInvocationContractState: participantDashboardExamHistoryDataSourceState.initialSnapshotPersistenceInvocationContractState,
      dataSourceSnapshotPersistenceInvocationPackageMapperName: participantDashboardExamHistoryDataSourceState.snapshotPersistenceInvocationPackageMapperName,
      isDataSourceSnapshotPersistenceInvocationPackagePrepared: participantDashboardExamHistoryDataSourceState.isSnapshotPersistenceInvocationPackagePrepared === true,
      canMapDataSourceSnapshotPersistenceInvocationPackages: participantDashboardExamHistoryDataSourceState.canMapSnapshotPersistenceInvocationPackages === true,
      dataSourceInitialSnapshotPersistenceInvocationPackageState: participantDashboardExamHistoryDataSourceState.initialSnapshotPersistenceInvocationPackageState,
      dataSourceSnapshotPersistenceResultContractName: participantDashboardExamHistoryDataSourceState.snapshotPersistenceResultContractName,
      isDataSourceSnapshotPersistenceResultContractPrepared: participantDashboardExamHistoryDataSourceState.isSnapshotPersistenceResultContractPrepared === true,
      canMapDataSourceSnapshotPersistenceResults: participantDashboardExamHistoryDataSourceState.canMapSnapshotPersistenceResults === true,
      dataSourceInitialSnapshotPersistenceResultState: participantDashboardExamHistoryDataSourceState.initialSnapshotPersistenceResultState,
      dataSourceSnapshotPersistenceResultAcceptanceGuardName: participantDashboardExamHistoryDataSourceState.snapshotPersistenceResultAcceptanceGuardName,
      isDataSourceSnapshotPersistenceResultAcceptanceGuardPrepared: participantDashboardExamHistoryDataSourceState.isSnapshotPersistenceResultAcceptanceGuardPrepared === true,
      canGuardDataSourceSnapshotPersistenceResultAcceptance: participantDashboardExamHistoryDataSourceState.canGuardSnapshotPersistenceResultAcceptance === true,
      dataSourceInitialSnapshotPersistenceResultAcceptanceState: participantDashboardExamHistoryDataSourceState.initialSnapshotPersistenceResultAcceptanceState,
      dataSourceSnapshotPersistenceCompletionMapperName: participantDashboardExamHistoryDataSourceState.snapshotPersistenceCompletionMapperName,
      isDataSourceSnapshotPersistenceCompletionMapperPrepared: participantDashboardExamHistoryDataSourceState.isSnapshotPersistenceCompletionMapperPrepared === true,
      canMapDataSourceSnapshotPersistenceCompletionStates: participantDashboardExamHistoryDataSourceState.canMapSnapshotPersistenceCompletionStates === true,
      dataSourceInitialSnapshotPersistenceCompletionState: participantDashboardExamHistoryDataSourceState.initialSnapshotPersistenceCompletionState,
      dataSourceSnapshotPersistenceCycleMapperName: participantDashboardExamHistoryDataSourceState.snapshotPersistenceCycleMapperName,
      isDataSourceSnapshotPersistenceCycleMapperPrepared: participantDashboardExamHistoryDataSourceState.isSnapshotPersistenceCycleMapperPrepared === true,
      canMapDataSourceSnapshotPersistenceCycleStates: participantDashboardExamHistoryDataSourceState.canMapSnapshotPersistenceCycleStates === true,
      dataSourceInitialSnapshotPersistenceCycleState: participantDashboardExamHistoryDataSourceState.initialSnapshotPersistenceCycleState,
      dataSourceSnapshotPersistenceCycleRepetitionGuardName: participantDashboardExamHistoryDataSourceState.snapshotPersistenceCycleRepetitionGuardName,
      isDataSourceSnapshotPersistenceCycleRepetitionGuardPrepared: participantDashboardExamHistoryDataSourceState.isSnapshotPersistenceCycleRepetitionGuardPrepared === true,
      canGuardDataSourceSnapshotPersistenceCycleRepetitions: participantDashboardExamHistoryDataSourceState.canGuardSnapshotPersistenceCycleRepetitions === true,
      dataSourceInitialSnapshotPersistenceCycleRepetitionState: participantDashboardExamHistoryDataSourceState.initialSnapshotPersistenceCycleRepetitionState,
      dataSourceSnapshotPersistenceCycleRegistryMapperName: participantDashboardExamHistoryDataSourceState.snapshotPersistenceCycleRegistryMapperName,
      isDataSourceSnapshotPersistenceCycleRegistryMapperPrepared: participantDashboardExamHistoryDataSourceState.isSnapshotPersistenceCycleRegistryMapperPrepared === true,
      canMapDataSourceSnapshotPersistenceCycleRegistryStates: participantDashboardExamHistoryDataSourceState.canMapSnapshotPersistenceCycleRegistryStates === true,
      dataSourceInitialSnapshotPersistenceCycleRegistryState: participantDashboardExamHistoryDataSourceState.initialSnapshotPersistenceCycleRegistryState,
      dataSourceSnapshotPersistenceCycleRegistrySerializationMapperName: participantDashboardExamHistoryDataSourceState.snapshotPersistenceCycleRegistrySerializationMapperName,
      isDataSourceSnapshotPersistenceCycleRegistrySerializationMapperPrepared: participantDashboardExamHistoryDataSourceState.isSnapshotPersistenceCycleRegistrySerializationMapperPrepared === true,
      canMapDataSourceSnapshotPersistenceCycleRegistrySerializationStates: participantDashboardExamHistoryDataSourceState.canMapSnapshotPersistenceCycleRegistrySerializationStates === true,
      dataSourceInitialSnapshotPersistenceCycleRegistrySerializationState: participantDashboardExamHistoryDataSourceState.initialSnapshotPersistenceCycleRegistrySerializationState,
      dataSourceSnapshotPersistenceCycleRegistryDeserializationMapperName: participantDashboardExamHistoryDataSourceState.snapshotPersistenceCycleRegistryDeserializationMapperName,
      isDataSourceSnapshotPersistenceCycleRegistryDeserializationMapperPrepared: participantDashboardExamHistoryDataSourceState.isSnapshotPersistenceCycleRegistryDeserializationMapperPrepared === true,
      canMapDataSourceSnapshotPersistenceCycleRegistryDeserializationStates: participantDashboardExamHistoryDataSourceState.canMapSnapshotPersistenceCycleRegistryDeserializationStates === true,
      dataSourceInitialSnapshotPersistenceCycleRegistryDeserializationState: participantDashboardExamHistoryDataSourceState.initialSnapshotPersistenceCycleRegistryDeserializationState,
      dataSourceSnapshotPersistenceCycleRegistryContractName: participantDashboardExamHistoryDataSourceState.snapshotPersistenceCycleRegistryContractName,
      isDataSourceSnapshotPersistenceCycleRegistryContractPrepared: participantDashboardExamHistoryDataSourceState.isSnapshotPersistenceCycleRegistryContractPrepared === true,
      canMapDataSourceSnapshotPersistenceCycleRegistryIntents: participantDashboardExamHistoryDataSourceState.canMapSnapshotPersistenceCycleRegistryIntents === true,
      dataSourceInitialSnapshotPersistenceCycleRegistryContractState: participantDashboardExamHistoryDataSourceState.initialSnapshotPersistenceCycleRegistryContractState,
      dataSourceSnapshotPersistenceCycleRegistryStorageAdapterReadinessMapperName: participantDashboardExamHistoryDataSourceState.snapshotPersistenceCycleRegistryStorageAdapterReadinessMapperName,
      isDataSourceSnapshotPersistenceCycleRegistryStorageAdapterReadinessMapperPrepared: participantDashboardExamHistoryDataSourceState.isSnapshotPersistenceCycleRegistryStorageAdapterReadinessMapperPrepared === true,
      canMapDataSourceSnapshotPersistenceCycleRegistryStorageAdapterReadinessStates: participantDashboardExamHistoryDataSourceState.canMapSnapshotPersistenceCycleRegistryStorageAdapterReadinessStates === true,
      dataSourceInitialSnapshotPersistenceCycleRegistryStorageAdapterReadinessState: participantDashboardExamHistoryDataSourceState.initialSnapshotPersistenceCycleRegistryStorageAdapterReadinessState,
      dataSourceSnapshotPersistenceCycleRegistryOperationPlanMapperName: participantDashboardExamHistoryDataSourceState.snapshotPersistenceCycleRegistryOperationPlanMapperName,
      isDataSourceSnapshotPersistenceCycleRegistryOperationPlanMapperPrepared: participantDashboardExamHistoryDataSourceState.isSnapshotPersistenceCycleRegistryOperationPlanMapperPrepared === true,
      canMapDataSourceSnapshotPersistenceCycleRegistryOperationPlanStates: participantDashboardExamHistoryDataSourceState.canMapSnapshotPersistenceCycleRegistryOperationPlanStates === true,
      dataSourceInitialSnapshotPersistenceCycleRegistryOperationPlanState: participantDashboardExamHistoryDataSourceState.initialSnapshotPersistenceCycleRegistryOperationPlanState,
      dataSourceSnapshotPersistenceCycleRegistryOperationReleaseMapperName: participantDashboardExamHistoryDataSourceState.snapshotPersistenceCycleRegistryOperationReleaseMapperName,
      isDataSourceSnapshotPersistenceCycleRegistryOperationReleaseMapperPrepared: participantDashboardExamHistoryDataSourceState.isSnapshotPersistenceCycleRegistryOperationReleaseMapperPrepared === true,
      canMapDataSourceSnapshotPersistenceCycleRegistryOperationReleaseStates: participantDashboardExamHistoryDataSourceState.canMapSnapshotPersistenceCycleRegistryOperationReleaseStates === true,
      dataSourceInitialSnapshotPersistenceCycleRegistryOperationReleaseState: participantDashboardExamHistoryDataSourceState.initialSnapshotPersistenceCycleRegistryOperationReleaseState,
      dataSourceSnapshotPersistenceCycleRegistryExecutionGuardName: participantDashboardExamHistoryDataSourceState.snapshotPersistenceCycleRegistryExecutionGuardName,
      isDataSourceSnapshotPersistenceCycleRegistryExecutionGuardPrepared: participantDashboardExamHistoryDataSourceState.isSnapshotPersistenceCycleRegistryExecutionGuardPrepared === true,
      canGuardDataSourceSnapshotPersistenceCycleRegistryExecutions: participantDashboardExamHistoryDataSourceState.canGuardSnapshotPersistenceCycleRegistryExecutions === true,
      dataSourceInitialSnapshotPersistenceCycleRegistryExecutionState: participantDashboardExamHistoryDataSourceState.initialSnapshotPersistenceCycleRegistryExecutionState,
      dataSourceSnapshotPersistenceCycleRegistryInvocationContractName: participantDashboardExamHistoryDataSourceState.snapshotPersistenceCycleRegistryInvocationContractName,
      isDataSourceSnapshotPersistenceCycleRegistryInvocationContractPrepared: participantDashboardExamHistoryDataSourceState.isSnapshotPersistenceCycleRegistryInvocationContractPrepared === true,
      canMapDataSourceSnapshotPersistenceCycleRegistryInvocationContracts: participantDashboardExamHistoryDataSourceState.canMapSnapshotPersistenceCycleRegistryInvocationContracts === true,
      dataSourceInitialSnapshotPersistenceCycleRegistryInvocationContractState: participantDashboardExamHistoryDataSourceState.initialSnapshotPersistenceCycleRegistryInvocationContractState,
      dataSourceSnapshotPersistenceCycleRegistryInvocationPackageMapperName: participantDashboardExamHistoryDataSourceState.snapshotPersistenceCycleRegistryInvocationPackageMapperName,
      isDataSourceSnapshotPersistenceCycleRegistryInvocationPackageMapperPrepared: participantDashboardExamHistoryDataSourceState.isSnapshotPersistenceCycleRegistryInvocationPackageMapperPrepared === true,
      canMapDataSourceSnapshotPersistenceCycleRegistryInvocationPackages: participantDashboardExamHistoryDataSourceState.canMapSnapshotPersistenceCycleRegistryInvocationPackages === true,
      dataSourceInitialSnapshotPersistenceCycleRegistryInvocationPackageState: participantDashboardExamHistoryDataSourceState.initialSnapshotPersistenceCycleRegistryInvocationPackageState,
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

  function mapParticipantFullExamResultHistorySnapshotPersistenceCycleRegistryInvocationPackageState(input) {
    const source =
      input &&
      typeof input === "object" &&
      !Array.isArray(input)
        ? input
        : {};

    const invocationPackageVersion = 1;

    const storageNamespace =
      "accaoui:exam_history:persistence_cycle_registry";

    const storageKey =
      storageNamespace +
      ":v1";

    const registryIdentity =
      "exam_history_persistence_cycle_registry:v1";

    const maximumSerializedBytes = 32768;

    const maximumCompletedCycleIdentities =
      100;

    const inspectOwnDataProperty = (
      target,
      propertyName
    ) => {
      try {
        const descriptor =
          Object.getOwnPropertyDescriptor(
            target,
            propertyName
          );

        if (!descriptor) {
          return {
            isPresent: false,
            isValid: true,
            value: null
          };
        }

        if (
          !Object.prototype.hasOwnProperty.call(
            descriptor,
            "value"
          )
        ) {
          return {
            isPresent: true,
            isValid: false,
            value: null
          };
        }

        return {
          isPresent: true,
          isValid: true,
          value:
            descriptor.value
        };
      } catch (_error) {
        return {
          isPresent: true,
          isValid: false,
          value: null
        };
      }
    };

    const readRequiredFields = (
      target,
      fieldNames
    ) => {
      const fields = {};

      for (
        let index = 0;
        index < fieldNames.length;
        index += 1
      ) {
        const fieldName =
          fieldNames[index];

        const property =
          inspectOwnDataProperty(
            target,
            fieldName
          );

        if (
          !property.isPresent ||
          !property.isValid
        ) {
          return {
            isValid: false,
            fields: {}
          };
        }

        fields[fieldName] =
          property.value;
      }

      return {
        isValid: true,
        fields
      };
    };

    const cloneStringArray = (
      value
    ) => {
      try {
        if (!Array.isArray(value)) {
          return {
            isValid: false,
            values: []
          };
        }

        const values = [];
        const expectedKeys = [];

        for (
          let index = 0;
          index < value.length;
          index += 1
        ) {
          const propertyName =
            String(index);

          const descriptor =
            Object.getOwnPropertyDescriptor(
              value,
              propertyName
            );

          if (
            !descriptor ||
            !Object.prototype.hasOwnProperty.call(
              descriptor,
              "value"
            ) ||
            typeof descriptor.value !==
              "string"
          ) {
            return {
              isValid: false,
              values: []
            };
          }

          expectedKeys.push(
            propertyName
          );

          values.push(
            descriptor.value
          );
        }

        if (
          JSON.stringify(
            Object.keys(value)
          ) !==
          JSON.stringify(
            expectedKeys
          )
        ) {
          return {
            isValid: false,
            values: []
          };
        }

        return {
          isValid: true,
          values
        };
      } catch (_error) {
        return {
          isValid: false,
          values: []
        };
      }
    };

    const createState = ({
      status,
      isValid,
      canInvokeLater,
      isInvocationPackageValidated,
      isCapabilityAvailable,
      isMethodReferenceValidated,
      intent = null,
      operation = null,
      methodName = null,
      requiredCapability = null,
      readinessFingerprint = null,
      completedCycleCount = null,
      serializedByteLength = null,
      serializedJson = null,
      invocationArguments = [],
      contractIdentity = null,
      operationPlanIdentity = null,
      operationReleaseIdentity = null,
      executionGuardIdentity = null,
      invocationContractIdentity = null,
      invocationPackageIdentity = null,
      reason
    }) => ({
      version: "v27.30r",
      status,
      isValid,
      isSnapshotPersistenceCycleRegistryInvocationPackageOnly: true,
      isLiveCall: false,
      canInvokeLater,
      isInvocationPackageValidated,
      isCapabilityAvailable,
      isMethodReferenceValidated,
      canPackageSave:
        canInvokeLater &&
        intent === "save",
      canPackageLoad:
        canInvokeLater &&
        intent === "load",
      canPackageDelete:
        canInvokeLater &&
        intent === "delete",
      canExecuteStorage: false,
      invocationPackageVersion,
      intent,
      operation,
      methodName,
      requiredCapability,
      storageNamespace,
      storageKey,
      registryIdentity,
      maximumSerializedBytes,
      maximumCompletedCycleIdentities,
      readinessFingerprint,
      completedCycleCount,
      serializedByteLength,
      serializedJson,
      invocationArgumentCount:
        invocationArguments.length,
      invocationArguments,
      contractIdentity,
      operationPlanIdentity,
      operationReleaseIdentity,
      executionGuardIdentity,
      invocationContractIdentity,
      invocationPackageIdentity,
      reason
    });

    const invalid = (reason) =>
      createState({
        status:
          "exam_result_history_persistence_cycle_registry_invocation_package_invalid",
        isValid: false,
        canInvokeLater: false,
        isInvocationPackageValidated: false,
        isCapabilityAvailable: false,
        isMethodReferenceValidated: false,
        reason
      });

    const contractProperty =
      inspectOwnDataProperty(
        source,
        "invocationContractState"
      );

    const adapterProperty =
      inspectOwnDataProperty(
        source,
        "storageAdapter"
      );

    if (!contractProperty.isPresent) {
      return invalid(
        "persistence_cycle_registry_invocation_package_contract_missing"
      );
    }

    if (!contractProperty.isValid) {
      return invalid(
        "persistence_cycle_registry_invocation_package_contract_accessor_not_allowed"
      );
    }

    if (!adapterProperty.isPresent) {
      return invalid(
        "persistence_cycle_registry_invocation_package_adapter_missing"
      );
    }

    if (!adapterProperty.isValid) {
      return invalid(
        "persistence_cycle_registry_invocation_package_adapter_accessor_not_allowed"
      );
    }

    const invocationContractState =
      contractProperty.value;

    const storageAdapter =
      adapterProperty.value;

    if (
      !invocationContractState ||
      typeof invocationContractState !==
        "object" ||
      Array.isArray(
        invocationContractState
      )
    ) {
      return invalid(
        "persistence_cycle_registry_invocation_package_contract_invalid"
      );
    }

    if (
      !storageAdapter ||
      typeof storageAdapter !==
        "object" ||
      Array.isArray(storageAdapter)
    ) {
      return invalid(
        "persistence_cycle_registry_invocation_package_adapter_invalid"
      );
    }

    const fieldsState =
      readRequiredFields(
        invocationContractState,
        [
          "status",
          "isValid",
          "isSnapshotPersistenceCycleRegistryInvocationContractOnly",
          "isLiveCall",
          "canPrepareInvocation",
          "canInvokeLater",
          "isInvocationShapeValidated",
          "isCapabilityAvailable",
          "canPrepareSave",
          "canPrepareLoad",
          "canPrepareDelete",
          "canExecuteStorage",
          "invocationContractVersion",
          "intent",
          "operation",
          "methodName",
          "requiredCapability",
          "storageNamespace",
          "storageKey",
          "registryIdentity",
          "maximumSerializedBytes",
          "maximumCompletedCycleIdentities",
          "readinessFingerprint",
          "completedCycleCount",
          "serializedByteLength",
          "serializedJson",
          "invocationArgumentCount",
          "invocationArguments",
          "contractIdentity",
          "operationPlanIdentity",
          "operationReleaseIdentity",
          "executionGuardIdentity",
          "invocationContractIdentity",
          "reason"
        ]
      );

    if (!fieldsState.isValid) {
      return invalid(
        "persistence_cycle_registry_invocation_package_contract_fields_invalid"
      );
    }

    const fields =
      fieldsState.fields;

    const intentConfig = {
      save: {
        operation: "write",
        methodName: "write",
        requiredCapability: "write",
        argumentCount: 2
      },
      load: {
        operation: "read",
        methodName: "read",
        requiredCapability: "read",
        argumentCount: 1
      },
      delete: {
        operation: "delete",
        methodName: "delete",
        requiredCapability: "delete",
        argumentCount: 1
      }
    };

    const config =
      intentConfig[
        fields.intent
      ];

    if (
      !config ||
      fields.isValid !== true ||
      fields.isSnapshotPersistenceCycleRegistryInvocationContractOnly !==
        true ||
      fields.isLiveCall !== false ||
      fields.canExecuteStorage !== false ||
      fields.invocationContractVersion !==
        1 ||
      fields.operation !==
        config.operation ||
      fields.methodName !==
        config.methodName ||
      fields.requiredCapability !==
        config.requiredCapability ||
      fields.storageNamespace !==
        storageNamespace ||
      fields.storageKey !==
        storageKey ||
      fields.registryIdentity !==
        registryIdentity ||
      fields.maximumSerializedBytes !==
        maximumSerializedBytes ||
      fields.maximumCompletedCycleIdentities !==
        maximumCompletedCycleIdentities ||
      fields.contractIdentity !==
        (
          "exam_history_persistence_cycle_registry_contract:" +
          fields.intent +
          ":v1"
        ) ||
      fields.operationPlanIdentity !==
        (
          "exam_history_persistence_cycle_registry_operation_plan:" +
          fields.intent +
          ":v1"
        ) ||
      fields.operationReleaseIdentity !==
        (
          "exam_history_persistence_cycle_registry_operation_release:" +
          fields.intent +
          ":v1"
        ) ||
      fields.executionGuardIdentity !==
        (
          "exam_history_persistence_cycle_registry_execution_guard:" +
          fields.intent +
          ":v1"
        ) ||
      fields.invocationContractIdentity !==
        (
          "exam_history_persistence_cycle_registry_invocation_contract:" +
          fields.intent +
          ":v1"
        )
    ) {
      return invalid(
        "persistence_cycle_registry_invocation_package_contract_invalid"
      );
    }

    const argumentState =
      cloneStringArray(
        fields.invocationArguments
      );

    if (
      !argumentState.isValid ||
      !Number.isInteger(
        fields.invocationArgumentCount
      ) ||
      fields.invocationArgumentCount !==
        argumentState.values.length
    ) {
      return invalid(
        "persistence_cycle_registry_invocation_package_arguments_invalid"
      );
    }

    const readinessMatch =
      /^exam_history_persistence_cycle_registry_storage_adapter_readiness:v1:read=([01]):write=([01]):delete=([01])$/.exec(
        fields.readinessFingerprint
      );

    if (!readinessMatch) {
      return invalid(
        "persistence_cycle_registry_invocation_package_readiness_invalid"
      );
    }

    const readinessCapabilityState = {
      read:
        readinessMatch[1] === "1",
      write:
        readinessMatch[2] === "1",
      delete:
        readinessMatch[3] === "1"
    };

    const fingerprintCapabilityAvailable =
      readinessCapabilityState[
        config.requiredCapability
      ] === true;

    let completedCycleCount = null;
    let serializedByteLength = null;
    let serializedJson = null;

    if (fields.intent === "save") {
      if (
        !Number.isInteger(
          fields.completedCycleCount
        ) ||
        fields.completedCycleCount < 0 ||
        fields.completedCycleCount >
          maximumCompletedCycleIdentities ||
        !Number.isSafeInteger(
          fields.serializedByteLength
        ) ||
        fields.serializedByteLength < 1 ||
        fields.serializedByteLength >
          maximumSerializedBytes ||
        typeof fields.serializedJson !==
          "string"
      ) {
        return invalid(
          "persistence_cycle_registry_invocation_package_save_payload_invalid"
        );
      }

      const actualByteLength =
        getParticipantFullExamResultHistorySnapshotUtf8ByteLength(
          fields.serializedJson
        );

      if (
        actualByteLength !==
          fields.serializedByteLength
      ) {
        return invalid(
          "persistence_cycle_registry_invocation_package_save_size_mismatch"
        );
      }

      const deserializationState =
        mapParticipantFullExamResultHistorySnapshotPersistenceCycleRegistryDeserializationState({
          serializedJson:
            fields.serializedJson
        });

      if (
        !deserializationState.isValid ||
        deserializationState.canDeserializeRegistry !==
          true ||
        deserializationState.canUseRegistry !==
          true ||
        deserializationState.canPersistLater !==
          true ||
        deserializationState.canExecuteStorage !==
          false ||
        deserializationState.registryIdentity !==
          registryIdentity ||
        deserializationState.completedCycleCount !==
          fields.completedCycleCount ||
        deserializationState.serializedByteLength !==
          actualByteLength
      ) {
        return invalid(
          "persistence_cycle_registry_invocation_package_save_round_trip_invalid"
        );
      }

      completedCycleCount =
        fields.completedCycleCount;

      serializedByteLength =
        actualByteLength;

      serializedJson =
        fields.serializedJson;
    } else if (
      fields.completedCycleCount !== null ||
      fields.serializedByteLength !== null ||
      fields.serializedJson !== null
    ) {
      return invalid(
        "persistence_cycle_registry_invocation_package_payload_unexpected"
      );
    }

    const isReadyContract =
      fields.status ===
        "exam_result_history_persistence_cycle_registry_invocation_contract_ready" &&
      fields.canPrepareInvocation ===
        true &&
      fields.canInvokeLater ===
        true &&
      fields.isInvocationShapeValidated ===
        true &&
      fields.isCapabilityAvailable ===
        true &&
      fields.reason === null;

    const isBlockedContract =
      fields.status ===
        "exam_result_history_persistence_cycle_registry_invocation_contract_blocked" &&
      fields.canPrepareInvocation ===
        false &&
      fields.canInvokeLater ===
        false &&
      fields.isInvocationShapeValidated ===
        true &&
      fields.isCapabilityAvailable ===
        false &&
      fields.canPrepareSave === false &&
      fields.canPrepareLoad === false &&
      fields.canPrepareDelete ===
        false &&
      fields.invocationArgumentCount ===
        0 &&
      fields.reason ===
        "persistence_cycle_registry_invocation_contract_capability_unavailable";

    if (
      !isReadyContract &&
      !isBlockedContract
    ) {
      return invalid(
        "persistence_cycle_registry_invocation_package_contract_state_invalid"
      );
    }

    const expectedContractFlags = {
      save:
        fields.intent === "save",
      load:
        fields.intent === "load",
      delete:
        fields.intent === "delete"
    };

    if (
      isReadyContract &&
      (
        fields.canPrepareSave !==
          expectedContractFlags.save ||
        fields.canPrepareLoad !==
          expectedContractFlags.load ||
        fields.canPrepareDelete !==
          expectedContractFlags.delete
      )
    ) {
      return invalid(
        "persistence_cycle_registry_invocation_package_contract_flags_invalid"
      );
    }

    if (isReadyContract) {
      const expectedArguments =
        fields.intent === "save"
          ? [
              storageKey,
              serializedJson
            ]
          : [
              storageKey
            ];

      if (
        fields.invocationArgumentCount !==
          config.argumentCount ||
        JSON.stringify(
          argumentState.values
        ) !==
          JSON.stringify(
            expectedArguments
          )
      ) {
        return invalid(
          "persistence_cycle_registry_invocation_package_arguments_invalid"
        );
      }
    } else if (
      argumentState.values.length !== 0
    ) {
      return invalid(
        "persistence_cycle_registry_invocation_package_blocked_arguments_invalid"
      );
    }

    const recomputedReadiness =
      mapParticipantFullExamResultHistorySnapshotPersistenceCycleRegistryStorageAdapterReadinessState({
        storageAdapter
      });

    if (
      !recomputedReadiness.isValid ||
      recomputedReadiness.isSnapshotPersistenceCycleRegistryStorageAdapterReadinessMapperOnly !==
        true ||
      recomputedReadiness.isLiveCall !==
        false ||
      recomputedReadiness.canExecuteStorage !==
        false ||
      recomputedReadiness.readinessVersion !==
        1 ||
      recomputedReadiness.adapterMode !==
        "own_data_methods_only" ||
      typeof recomputedReadiness.readinessFingerprint !==
        "string" ||
      recomputedReadiness.reason !== null
    ) {
      return invalid(
        "persistence_cycle_registry_invocation_package_adapter_readiness_invalid"
      );
    }

    if (
      recomputedReadiness.readinessFingerprint !==
        fields.readinessFingerprint
    ) {
      return invalid(
        "persistence_cycle_registry_invocation_package_readiness_mismatch"
      );
    }

    const recomputedCapabilityState = {
      read:
        recomputedReadiness.canPrepareRead ===
        true,
      write:
        recomputedReadiness.canPrepareWrite ===
        true,
      delete:
        recomputedReadiness.canPrepareDelete ===
        true
    };

    const isCapabilityAvailable =
      recomputedCapabilityState[
        config.requiredCapability
      ] === true;

    if (
      isCapabilityAvailable !==
        fingerprintCapabilityAvailable
    ) {
      return invalid(
        "persistence_cycle_registry_invocation_package_capability_fingerprint_mismatch"
      );
    }

    const invocationPackageIdentity =
      "exam_history_persistence_cycle_registry_invocation_package:" +
      fields.intent +
      ":v1";

    if (isBlockedContract) {
      if (isCapabilityAvailable) {
        return invalid(
          "persistence_cycle_registry_invocation_package_blocked_capability_mismatch"
        );
      }

      return createState({
        status:
          "exam_result_history_persistence_cycle_registry_invocation_package_blocked",
        isValid: true,
        canInvokeLater: false,
        isInvocationPackageValidated:
          true,
        isCapabilityAvailable:
          false,
        isMethodReferenceValidated:
          false,
        intent:
          fields.intent,
        operation:
          fields.operation,
        methodName:
          fields.methodName,
        requiredCapability:
          fields.requiredCapability,
        readinessFingerprint:
          recomputedReadiness.readinessFingerprint,
        completedCycleCount,
        serializedByteLength,
        serializedJson,
        invocationArguments: [],
        contractIdentity:
          fields.contractIdentity,
        operationPlanIdentity:
          fields.operationPlanIdentity,
        operationReleaseIdentity:
          fields.operationReleaseIdentity,
        executionGuardIdentity:
          fields.executionGuardIdentity,
        invocationContractIdentity:
          fields.invocationContractIdentity,
        invocationPackageIdentity,
        reason:
          "persistence_cycle_registry_invocation_package_capability_unavailable"
      });
    }

    if (!isCapabilityAvailable) {
      return invalid(
        "persistence_cycle_registry_invocation_package_capability_mismatch"
      );
    }

    const methodProperty =
      inspectOwnDataProperty(
        storageAdapter,
        config.methodName
      );

    if (
      !methodProperty.isPresent ||
      !methodProperty.isValid ||
      typeof methodProperty.value !==
        "function"
    ) {
      return invalid(
        "persistence_cycle_registry_invocation_package_method_invalid"
      );
    }

    return createState({
      status:
        "exam_result_history_persistence_cycle_registry_invocation_package_ready",
      isValid: true,
      canInvokeLater: true,
      isInvocationPackageValidated:
        true,
      isCapabilityAvailable: true,
      isMethodReferenceValidated:
        true,
      intent:
        fields.intent,
      operation:
        fields.operation,
      methodName:
        fields.methodName,
      requiredCapability:
        fields.requiredCapability,
      readinessFingerprint:
        recomputedReadiness.readinessFingerprint,
      completedCycleCount,
      serializedByteLength,
      serializedJson,
      invocationArguments:
        argumentState.values.slice(),
      contractIdentity:
        fields.contractIdentity,
      operationPlanIdentity:
        fields.operationPlanIdentity,
      operationReleaseIdentity:
        fields.operationReleaseIdentity,
      executionGuardIdentity:
        fields.executionGuardIdentity,
      invocationContractIdentity:
        fields.invocationContractIdentity,
      invocationPackageIdentity,
      reason: null
    });
  }

  function mapParticipantFullExamResultHistorySnapshotPersistenceCycleRegistryInvocationContract(input) {
    const source =
      input &&
      typeof input === "object" &&
      !Array.isArray(input)
        ? input
        : {};

    const invocationContractVersion = 1;

    const storageNamespace =
      "accaoui:exam_history:persistence_cycle_registry";

    const storageKey =
      storageNamespace +
      ":v1";

    const registryIdentity =
      "exam_history_persistence_cycle_registry:v1";

    const maximumSerializedBytes = 32768;

    const maximumCompletedCycleIdentities =
      100;

    const inspectOwnDataProperty = (
      target,
      propertyName
    ) => {
      try {
        const descriptor =
          Object.getOwnPropertyDescriptor(
            target,
            propertyName
          );

        if (!descriptor) {
          return {
            isPresent: false,
            isValid: true,
            value: null
          };
        }

        if (
          !Object.prototype.hasOwnProperty.call(
            descriptor,
            "value"
          )
        ) {
          return {
            isPresent: true,
            isValid: false,
            value: null
          };
        }

        return {
          isPresent: true,
          isValid: true,
          value:
            descriptor.value
        };
      } catch (_error) {
        return {
          isPresent: true,
          isValid: false,
          value: null
        };
      }
    };

    const readRequiredFields = (
      target,
      fieldNames
    ) => {
      const fields = {};

      for (
        let index = 0;
        index < fieldNames.length;
        index += 1
      ) {
        const fieldName =
          fieldNames[index];

        const property =
          inspectOwnDataProperty(
            target,
            fieldName
          );

        if (
          !property.isPresent ||
          !property.isValid
        ) {
          return {
            isValid: false,
            fields: {}
          };
        }

        fields[fieldName] =
          property.value;
      }

      return {
        isValid: true,
        fields
      };
    };

    const createState = ({
      status,
      isValid,
      canPrepareInvocation,
      isInvocationShapeValidated,
      isCapabilityAvailable,
      intent = null,
      operation = null,
      methodName = null,
      requiredCapability = null,
      readinessFingerprint = null,
      completedCycleCount = null,
      serializedByteLength = null,
      serializedJson = null,
      invocationArguments = [],
      contractIdentity = null,
      operationPlanIdentity = null,
      operationReleaseIdentity = null,
      executionGuardIdentity = null,
      invocationContractIdentity = null,
      reason
    }) => ({
      version: "v27.30q",
      status,
      isValid,
      isSnapshotPersistenceCycleRegistryInvocationContractOnly: true,
      isLiveCall: false,
      canPrepareInvocation,
      canInvokeLater:
        canPrepareInvocation,
      isInvocationShapeValidated,
      isCapabilityAvailable,
      canPrepareSave:
        canPrepareInvocation &&
        intent === "save",
      canPrepareLoad:
        canPrepareInvocation &&
        intent === "load",
      canPrepareDelete:
        canPrepareInvocation &&
        intent === "delete",
      canExecuteStorage: false,
      invocationContractVersion,
      intent,
      operation,
      methodName,
      requiredCapability,
      storageNamespace,
      storageKey,
      registryIdentity,
      maximumSerializedBytes,
      maximumCompletedCycleIdentities,
      readinessFingerprint,
      completedCycleCount,
      serializedByteLength,
      serializedJson,
      invocationArgumentCount:
        invocationArguments.length,
      invocationArguments,
      contractIdentity,
      operationPlanIdentity,
      operationReleaseIdentity,
      executionGuardIdentity,
      invocationContractIdentity,
      reason
    });

    const invalid = (reason) =>
      createState({
        status:
          "exam_result_history_persistence_cycle_registry_invocation_contract_invalid",
        isValid: false,
        canPrepareInvocation: false,
        isInvocationShapeValidated: false,
        isCapabilityAvailable: false,
        reason
      });

    const executionProperty =
      inspectOwnDataProperty(
        source,
        "executionGuardState"
      );

    if (!executionProperty.isPresent) {
      return invalid(
        "persistence_cycle_registry_invocation_contract_execution_guard_missing"
      );
    }

    if (!executionProperty.isValid) {
      return invalid(
        "persistence_cycle_registry_invocation_contract_execution_guard_accessor_not_allowed"
      );
    }

    const executionGuardState =
      executionProperty.value;

    if (
      !executionGuardState ||
      typeof executionGuardState !==
        "object" ||
      Array.isArray(
        executionGuardState
      )
    ) {
      return invalid(
        "persistence_cycle_registry_invocation_contract_execution_guard_invalid"
      );
    }

    const fieldsState =
      readRequiredFields(
        executionGuardState,
        [
          "status",
          "isValid",
          "isSnapshotPersistenceCycleRegistryExecutionGuardOnly",
          "isLiveCall",
          "canProceedToInvocation",
          "canInvokeLater",
          "isExecutionBoundaryValidated",
          "isCapabilityAvailable",
          "isMethodReferenceValidated",
          "canGuardSave",
          "canGuardLoad",
          "canGuardDelete",
          "canExecuteStorage",
          "executionGuardVersion",
          "intent",
          "operation",
          "methodName",
          "requiredCapability",
          "storageNamespace",
          "storageKey",
          "registryIdentity",
          "maximumSerializedBytes",
          "maximumCompletedCycleIdentities",
          "readinessFingerprint",
          "completedCycleCount",
          "serializedByteLength",
          "serializedJson",
          "contractIdentity",
          "operationPlanIdentity",
          "operationReleaseIdentity",
          "executionGuardIdentity",
          "reason"
        ]
      );

    if (!fieldsState.isValid) {
      return invalid(
        "persistence_cycle_registry_invocation_contract_execution_guard_fields_invalid"
      );
    }

    const fields =
      fieldsState.fields;

    const intentConfig = {
      save: {
        operation: "write",
        methodName: "write",
        requiredCapability: "write",
        argumentCount: 2
      },
      load: {
        operation: "read",
        methodName: "read",
        requiredCapability: "read",
        argumentCount: 1
      },
      delete: {
        operation: "delete",
        methodName: "delete",
        requiredCapability: "delete",
        argumentCount: 1
      }
    };

    const config =
      intentConfig[
        fields.intent
      ];

    if (
      !config ||
      fields.isValid !== true ||
      fields.isSnapshotPersistenceCycleRegistryExecutionGuardOnly !==
        true ||
      fields.isLiveCall !== false ||
      fields.canExecuteStorage !== false ||
      fields.executionGuardVersion !==
        1 ||
      fields.operation !==
        config.operation ||
      fields.methodName !==
        config.methodName ||
      fields.requiredCapability !==
        config.requiredCapability ||
      fields.storageNamespace !==
        storageNamespace ||
      fields.storageKey !==
        storageKey ||
      fields.registryIdentity !==
        registryIdentity ||
      fields.maximumSerializedBytes !==
        maximumSerializedBytes ||
      fields.maximumCompletedCycleIdentities !==
        maximumCompletedCycleIdentities ||
      fields.contractIdentity !==
        (
          "exam_history_persistence_cycle_registry_contract:" +
          fields.intent +
          ":v1"
        ) ||
      fields.operationPlanIdentity !==
        (
          "exam_history_persistence_cycle_registry_operation_plan:" +
          fields.intent +
          ":v1"
        ) ||
      fields.operationReleaseIdentity !==
        (
          "exam_history_persistence_cycle_registry_operation_release:" +
          fields.intent +
          ":v1"
        ) ||
      fields.executionGuardIdentity !==
        (
          "exam_history_persistence_cycle_registry_execution_guard:" +
          fields.intent +
          ":v1"
        )
    ) {
      return invalid(
        "persistence_cycle_registry_invocation_contract_execution_guard_invalid"
      );
    }

    const readinessMatch =
      /^exam_history_persistence_cycle_registry_storage_adapter_readiness:v1:read=([01]):write=([01]):delete=([01])$/.exec(
        fields.readinessFingerprint
      );

    if (!readinessMatch) {
      return invalid(
        "persistence_cycle_registry_invocation_contract_readiness_invalid"
      );
    }

    const readinessCapabilityState = {
      read:
        readinessMatch[1] === "1",
      write:
        readinessMatch[2] === "1",
      delete:
        readinessMatch[3] === "1"
    };

    const isCapabilityAvailable =
      readinessCapabilityState[
        config.requiredCapability
      ] === true;

    let completedCycleCount = null;
    let serializedByteLength = null;
    let serializedJson = null;

    if (fields.intent === "save") {
      if (
        !Number.isInteger(
          fields.completedCycleCount
        ) ||
        fields.completedCycleCount < 0 ||
        fields.completedCycleCount >
          maximumCompletedCycleIdentities ||
        !Number.isSafeInteger(
          fields.serializedByteLength
        ) ||
        fields.serializedByteLength < 1 ||
        fields.serializedByteLength >
          maximumSerializedBytes ||
        typeof fields.serializedJson !==
          "string"
      ) {
        return invalid(
          "persistence_cycle_registry_invocation_contract_save_payload_invalid"
        );
      }

      const actualByteLength =
        getParticipantFullExamResultHistorySnapshotUtf8ByteLength(
          fields.serializedJson
        );

      if (
        actualByteLength !==
          fields.serializedByteLength
      ) {
        return invalid(
          "persistence_cycle_registry_invocation_contract_save_size_mismatch"
        );
      }

      const deserializationState =
        mapParticipantFullExamResultHistorySnapshotPersistenceCycleRegistryDeserializationState({
          serializedJson:
            fields.serializedJson
        });

      if (
        !deserializationState.isValid ||
        deserializationState.canDeserializeRegistry !==
          true ||
        deserializationState.canUseRegistry !==
          true ||
        deserializationState.canPersistLater !==
          true ||
        deserializationState.canExecuteStorage !==
          false ||
        deserializationState.registryIdentity !==
          registryIdentity ||
        deserializationState.completedCycleCount !==
          fields.completedCycleCount ||
        deserializationState.serializedByteLength !==
          actualByteLength
      ) {
        return invalid(
          "persistence_cycle_registry_invocation_contract_save_round_trip_invalid"
        );
      }

      completedCycleCount =
        fields.completedCycleCount;

      serializedByteLength =
        actualByteLength;

      serializedJson =
        fields.serializedJson;
    } else if (
      fields.completedCycleCount !== null ||
      fields.serializedByteLength !== null ||
      fields.serializedJson !== null
    ) {
      return invalid(
        "persistence_cycle_registry_invocation_contract_payload_unexpected"
      );
    }

    const isReadyGuard =
      fields.status ===
        "exam_result_history_persistence_cycle_registry_execution_guard_ready" &&
      fields.canProceedToInvocation ===
        true &&
      fields.canInvokeLater ===
        true &&
      fields.isExecutionBoundaryValidated ===
        true &&
      fields.isCapabilityAvailable ===
        true &&
      fields.isMethodReferenceValidated ===
        true &&
      fields.reason === null;

    const isBlockedGuard =
      fields.status ===
        "exam_result_history_persistence_cycle_registry_execution_guard_blocked" &&
      fields.canProceedToInvocation ===
        false &&
      fields.canInvokeLater ===
        false &&
      fields.isExecutionBoundaryValidated ===
        true &&
      fields.isCapabilityAvailable ===
        false &&
      fields.isMethodReferenceValidated ===
        false &&
      fields.canGuardSave === false &&
      fields.canGuardLoad === false &&
      fields.canGuardDelete === false &&
      fields.reason ===
        "persistence_cycle_registry_execution_guard_capability_unavailable";

    if (
      !isReadyGuard &&
      !isBlockedGuard
    ) {
      return invalid(
        "persistence_cycle_registry_invocation_contract_execution_guard_state_invalid"
      );
    }

    const expectedGuardFlags = {
      save:
        fields.intent === "save",
      load:
        fields.intent === "load",
      delete:
        fields.intent === "delete"
    };

    if (
      isReadyGuard &&
      (
        fields.canGuardSave !==
          expectedGuardFlags.save ||
        fields.canGuardLoad !==
          expectedGuardFlags.load ||
        fields.canGuardDelete !==
          expectedGuardFlags.delete
      )
    ) {
      return invalid(
        "persistence_cycle_registry_invocation_contract_guard_flags_invalid"
      );
    }

    if (
      isReadyGuard &&
      !isCapabilityAvailable
    ) {
      return invalid(
        "persistence_cycle_registry_invocation_contract_capability_mismatch"
      );
    }

    if (
      isBlockedGuard &&
      isCapabilityAvailable
    ) {
      return invalid(
        "persistence_cycle_registry_invocation_contract_blocked_capability_mismatch"
      );
    }

    const invocationContractIdentity =
      "exam_history_persistence_cycle_registry_invocation_contract:" +
      fields.intent +
      ":v1";

    if (isBlockedGuard) {
      return createState({
        status:
          "exam_result_history_persistence_cycle_registry_invocation_contract_blocked",
        isValid: true,
        canPrepareInvocation: false,
        isInvocationShapeValidated: true,
        isCapabilityAvailable: false,
        intent:
          fields.intent,
        operation:
          fields.operation,
        methodName:
          fields.methodName,
        requiredCapability:
          fields.requiredCapability,
        readinessFingerprint:
          fields.readinessFingerprint,
        completedCycleCount,
        serializedByteLength,
        serializedJson,
        invocationArguments: [],
        contractIdentity:
          fields.contractIdentity,
        operationPlanIdentity:
          fields.operationPlanIdentity,
        operationReleaseIdentity:
          fields.operationReleaseIdentity,
        executionGuardIdentity:
          fields.executionGuardIdentity,
        invocationContractIdentity,
        reason:
          "persistence_cycle_registry_invocation_contract_capability_unavailable"
      });
    }

    const invocationArguments =
      fields.intent === "save"
        ? [
            storageKey,
            serializedJson
          ]
        : [
            storageKey
          ];

    if (
      invocationArguments.length !==
        config.argumentCount
    ) {
      return invalid(
        "persistence_cycle_registry_invocation_contract_arguments_invalid"
      );
    }

    return createState({
      status:
        "exam_result_history_persistence_cycle_registry_invocation_contract_ready",
      isValid: true,
      canPrepareInvocation: true,
      isInvocationShapeValidated: true,
      isCapabilityAvailable: true,
      intent:
        fields.intent,
      operation:
        fields.operation,
      methodName:
        fields.methodName,
      requiredCapability:
        fields.requiredCapability,
      readinessFingerprint:
        fields.readinessFingerprint,
      completedCycleCount,
      serializedByteLength,
      serializedJson,
      invocationArguments,
      contractIdentity:
        fields.contractIdentity,
      operationPlanIdentity:
        fields.operationPlanIdentity,
      operationReleaseIdentity:
        fields.operationReleaseIdentity,
      executionGuardIdentity:
        fields.executionGuardIdentity,
      invocationContractIdentity,
      reason: null
    });
  }

  function guardParticipantFullExamResultHistorySnapshotPersistenceCycleRegistryExecution(input) {
    const source =
      input &&
      typeof input === "object" &&
      !Array.isArray(input)
        ? input
        : {};

    const executionGuardVersion = 1;

    const storageNamespace =
      "accaoui:exam_history:persistence_cycle_registry";

    const storageKey =
      storageNamespace +
      ":v1";

    const registryIdentity =
      "exam_history_persistence_cycle_registry:v1";

    const maximumSerializedBytes = 32768;

    const maximumCompletedCycleIdentities =
      100;

    const inspectOwnDataProperty = (
      target,
      propertyName
    ) => {
      try {
        const descriptor =
          Object.getOwnPropertyDescriptor(
            target,
            propertyName
          );

        if (!descriptor) {
          return {
            isPresent: false,
            isValid: true,
            value: null
          };
        }

        if (
          !Object.prototype.hasOwnProperty.call(
            descriptor,
            "value"
          )
        ) {
          return {
            isPresent: true,
            isValid: false,
            value: null
          };
        }

        return {
          isPresent: true,
          isValid: true,
          value:
            descriptor.value
        };
      } catch (_error) {
        return {
          isPresent: true,
          isValid: false,
          value: null
        };
      }
    };

    const readRequiredFields = (
      target,
      fieldNames
    ) => {
      const fields = {};

      for (
        let index = 0;
        index < fieldNames.length;
        index += 1
      ) {
        const fieldName =
          fieldNames[index];

        const property =
          inspectOwnDataProperty(
            target,
            fieldName
          );

        if (
          !property.isPresent ||
          !property.isValid
        ) {
          return {
            isValid: false,
            fields: {}
          };
        }

        fields[fieldName] =
          property.value;
      }

      return {
        isValid: true,
        fields
      };
    };

    const createState = ({
      status,
      isValid,
      canProceedToInvocation,
      isExecutionBoundaryValidated,
      isCapabilityAvailable,
      isMethodReferenceValidated,
      intent = null,
      operation = null,
      methodName = null,
      requiredCapability = null,
      readinessFingerprint = null,
      completedCycleCount = null,
      serializedByteLength = null,
      serializedJson = null,
      contractIdentity = null,
      operationPlanIdentity = null,
      operationReleaseIdentity = null,
      executionGuardIdentity = null,
      reason
    }) => ({
      version: "v27.30p",
      status,
      isValid,
      isSnapshotPersistenceCycleRegistryExecutionGuardOnly: true,
      isLiveCall: false,
      canProceedToInvocation,
      canInvokeLater:
        canProceedToInvocation,
      isExecutionBoundaryValidated,
      isCapabilityAvailable,
      isMethodReferenceValidated,
      canGuardSave:
        canProceedToInvocation &&
        intent === "save",
      canGuardLoad:
        canProceedToInvocation &&
        intent === "load",
      canGuardDelete:
        canProceedToInvocation &&
        intent === "delete",
      canExecuteStorage: false,
      executionGuardVersion,
      intent,
      operation,
      methodName,
      requiredCapability,
      storageNamespace,
      storageKey,
      registryIdentity,
      maximumSerializedBytes,
      maximumCompletedCycleIdentities,
      readinessFingerprint,
      completedCycleCount,
      serializedByteLength,
      serializedJson,
      contractIdentity,
      operationPlanIdentity,
      operationReleaseIdentity,
      executionGuardIdentity,
      reason
    });

    const invalid = (reason) =>
      createState({
        status:
          "exam_result_history_persistence_cycle_registry_execution_guard_invalid",
        isValid: false,
        canProceedToInvocation: false,
        isExecutionBoundaryValidated: false,
        isCapabilityAvailable: false,
        isMethodReferenceValidated: false,
        reason
      });

    const releaseProperty =
      inspectOwnDataProperty(
        source,
        "operationReleaseState"
      );

    const adapterProperty =
      inspectOwnDataProperty(
        source,
        "storageAdapter"
      );

    if (!releaseProperty.isPresent) {
      return invalid(
        "persistence_cycle_registry_execution_guard_release_missing"
      );
    }

    if (!releaseProperty.isValid) {
      return invalid(
        "persistence_cycle_registry_execution_guard_release_accessor_not_allowed"
      );
    }

    if (!adapterProperty.isPresent) {
      return invalid(
        "persistence_cycle_registry_execution_guard_adapter_missing"
      );
    }

    if (!adapterProperty.isValid) {
      return invalid(
        "persistence_cycle_registry_execution_guard_adapter_accessor_not_allowed"
      );
    }

    const operationReleaseState =
      releaseProperty.value;

    const storageAdapter =
      adapterProperty.value;

    if (
      !operationReleaseState ||
      typeof operationReleaseState !==
        "object" ||
      Array.isArray(
        operationReleaseState
      )
    ) {
      return invalid(
        "persistence_cycle_registry_execution_guard_release_invalid"
      );
    }

    if (
      !storageAdapter ||
      typeof storageAdapter !== "object" ||
      Array.isArray(storageAdapter)
    ) {
      return invalid(
        "persistence_cycle_registry_execution_guard_adapter_invalid"
      );
    }

    const fieldsState =
      readRequiredFields(
        operationReleaseState,
        [
          "status",
          "isValid",
          "isSnapshotPersistenceCycleRegistryOperationReleaseMapperOnly",
          "isLiveCall",
          "canReleaseOperation",
          "canInvokeLater",
          "isCapabilityAvailable",
          "isMethodReferenceValidated",
          "canReleaseSave",
          "canReleaseLoad",
          "canReleaseDelete",
          "canExecuteStorage",
          "operationReleaseVersion",
          "intent",
          "operation",
          "methodName",
          "requiredCapability",
          "storageNamespace",
          "storageKey",
          "registryIdentity",
          "maximumSerializedBytes",
          "maximumCompletedCycleIdentities",
          "readinessFingerprint",
          "completedCycleCount",
          "serializedByteLength",
          "serializedJson",
          "contractIdentity",
          "operationPlanIdentity",
          "operationReleaseIdentity",
          "reason"
        ]
      );

    if (!fieldsState.isValid) {
      return invalid(
        "persistence_cycle_registry_execution_guard_release_fields_invalid"
      );
    }

    const fields =
      fieldsState.fields;

    const intentConfig = {
      save: {
        operation: "write",
        methodName: "write",
        requiredCapability: "write"
      },
      load: {
        operation: "read",
        methodName: "read",
        requiredCapability: "read"
      },
      delete: {
        operation: "delete",
        methodName: "delete",
        requiredCapability: "delete"
      }
    };

    const config =
      intentConfig[
        fields.intent
      ];

    if (
      !config ||
      fields.isValid !== true ||
      fields.isSnapshotPersistenceCycleRegistryOperationReleaseMapperOnly !==
        true ||
      fields.isLiveCall !== false ||
      fields.canExecuteStorage !== false ||
      fields.operationReleaseVersion !==
        1 ||
      fields.operation !==
        config.operation ||
      fields.methodName !==
        config.methodName ||
      fields.requiredCapability !==
        config.requiredCapability ||
      fields.storageNamespace !==
        storageNamespace ||
      fields.storageKey !==
        storageKey ||
      fields.registryIdentity !==
        registryIdentity ||
      fields.maximumSerializedBytes !==
        maximumSerializedBytes ||
      fields.maximumCompletedCycleIdentities !==
        maximumCompletedCycleIdentities ||
      fields.contractIdentity !==
        (
          "exam_history_persistence_cycle_registry_contract:" +
          fields.intent +
          ":v1"
        ) ||
      fields.operationPlanIdentity !==
        (
          "exam_history_persistence_cycle_registry_operation_plan:" +
          fields.intent +
          ":v1"
        ) ||
      fields.operationReleaseIdentity !==
        (
          "exam_history_persistence_cycle_registry_operation_release:" +
          fields.intent +
          ":v1"
        )
    ) {
      return invalid(
        "persistence_cycle_registry_execution_guard_release_invalid"
      );
    }

    let completedCycleCount = null;
    let serializedByteLength = null;
    let serializedJson = null;

    if (fields.intent === "save") {
      if (
        !Number.isInteger(
          fields.completedCycleCount
        ) ||
        fields.completedCycleCount < 0 ||
        fields.completedCycleCount >
          maximumCompletedCycleIdentities ||
        !Number.isSafeInteger(
          fields.serializedByteLength
        ) ||
        fields.serializedByteLength < 1 ||
        fields.serializedByteLength >
          maximumSerializedBytes ||
        typeof fields.serializedJson !==
          "string"
      ) {
        return invalid(
          "persistence_cycle_registry_execution_guard_save_payload_invalid"
        );
      }

      const actualByteLength =
        getParticipantFullExamResultHistorySnapshotUtf8ByteLength(
          fields.serializedJson
        );

      if (
        actualByteLength !==
          fields.serializedByteLength
      ) {
        return invalid(
          "persistence_cycle_registry_execution_guard_save_size_mismatch"
        );
      }

      const deserializationState =
        mapParticipantFullExamResultHistorySnapshotPersistenceCycleRegistryDeserializationState({
          serializedJson:
            fields.serializedJson
        });

      if (
        !deserializationState.isValid ||
        deserializationState.canDeserializeRegistry !==
          true ||
        deserializationState.canUseRegistry !==
          true ||
        deserializationState.canPersistLater !==
          true ||
        deserializationState.canExecuteStorage !==
          false ||
        deserializationState.registryIdentity !==
          registryIdentity ||
        deserializationState.completedCycleCount !==
          fields.completedCycleCount ||
        deserializationState.serializedByteLength !==
          actualByteLength
      ) {
        return invalid(
          "persistence_cycle_registry_execution_guard_save_round_trip_invalid"
        );
      }

      completedCycleCount =
        fields.completedCycleCount;

      serializedByteLength =
        actualByteLength;

      serializedJson =
        fields.serializedJson;
    } else if (
      fields.completedCycleCount !== null ||
      fields.serializedByteLength !== null ||
      fields.serializedJson !== null
    ) {
      return invalid(
        "persistence_cycle_registry_execution_guard_payload_unexpected"
      );
    }

    const recomputedReadiness =
      mapParticipantFullExamResultHistorySnapshotPersistenceCycleRegistryStorageAdapterReadinessState({
        storageAdapter
      });

    if (
      !recomputedReadiness.isValid ||
      recomputedReadiness.isSnapshotPersistenceCycleRegistryStorageAdapterReadinessMapperOnly !==
        true ||
      recomputedReadiness.isLiveCall !==
        false ||
      recomputedReadiness.canExecuteStorage !==
        false ||
      recomputedReadiness.readinessVersion !==
        1 ||
      recomputedReadiness.adapterMode !==
        "own_data_methods_only" ||
      typeof recomputedReadiness.readinessFingerprint !==
        "string" ||
      recomputedReadiness.reason !== null
    ) {
      return invalid(
        "persistence_cycle_registry_execution_guard_adapter_readiness_invalid"
      );
    }

    if (
      recomputedReadiness.readinessFingerprint !==
        fields.readinessFingerprint
    ) {
      return invalid(
        "persistence_cycle_registry_execution_guard_readiness_mismatch"
      );
    }

    const capabilityState = {
      read:
        recomputedReadiness.canPrepareRead ===
        true,
      write:
        recomputedReadiness.canPrepareWrite ===
        true,
      delete:
        recomputedReadiness.canPrepareDelete ===
        true
    };

    const isCapabilityAvailable =
      capabilityState[
        config.requiredCapability
      ] === true;

    const isReadyRelease =
      fields.status ===
        "exam_result_history_persistence_cycle_registry_operation_release_ready" &&
      fields.canReleaseOperation ===
        true &&
      fields.canInvokeLater ===
        true &&
      fields.isCapabilityAvailable ===
        true &&
      fields.isMethodReferenceValidated ===
        true &&
      fields.reason === null;

    const isBlockedRelease =
      fields.status ===
        "exam_result_history_persistence_cycle_registry_operation_release_blocked" &&
      fields.canReleaseOperation ===
        false &&
      fields.canInvokeLater ===
        false &&
      fields.isCapabilityAvailable ===
        false &&
      fields.isMethodReferenceValidated ===
        false &&
      fields.canReleaseSave === false &&
      fields.canReleaseLoad === false &&
      fields.canReleaseDelete === false &&
      fields.reason ===
        "persistence_cycle_registry_operation_release_capability_unavailable";

    if (
      !isReadyRelease &&
      !isBlockedRelease
    ) {
      return invalid(
        "persistence_cycle_registry_execution_guard_release_state_invalid"
      );
    }

    const expectedReleaseFlags = {
      save:
        fields.intent === "save",
      load:
        fields.intent === "load",
      delete:
        fields.intent === "delete"
    };

    if (
      isReadyRelease &&
      (
        fields.canReleaseSave !==
          expectedReleaseFlags.save ||
        fields.canReleaseLoad !==
          expectedReleaseFlags.load ||
        fields.canReleaseDelete !==
          expectedReleaseFlags.delete
      )
    ) {
      return invalid(
        "persistence_cycle_registry_execution_guard_release_flags_invalid"
      );
    }

    const executionGuardIdentity =
      "exam_history_persistence_cycle_registry_execution_guard:" +
      fields.intent +
      ":v1";

    if (isBlockedRelease) {
      if (isCapabilityAvailable) {
        return invalid(
          "persistence_cycle_registry_execution_guard_blocked_capability_mismatch"
        );
      }

      return createState({
        status:
          "exam_result_history_persistence_cycle_registry_execution_guard_blocked",
        isValid: true,
        canProceedToInvocation: false,
        isExecutionBoundaryValidated: true,
        isCapabilityAvailable: false,
        isMethodReferenceValidated: false,
        intent:
          fields.intent,
        operation:
          fields.operation,
        methodName:
          fields.methodName,
        requiredCapability:
          fields.requiredCapability,
        readinessFingerprint:
          recomputedReadiness.readinessFingerprint,
        completedCycleCount,
        serializedByteLength,
        serializedJson,
        contractIdentity:
          fields.contractIdentity,
        operationPlanIdentity:
          fields.operationPlanIdentity,
        operationReleaseIdentity:
          fields.operationReleaseIdentity,
        executionGuardIdentity,
        reason:
          "persistence_cycle_registry_execution_guard_capability_unavailable"
      });
    }

    if (!isCapabilityAvailable) {
      return invalid(
        "persistence_cycle_registry_execution_guard_capability_mismatch"
      );
    }

    const methodProperty =
      inspectOwnDataProperty(
        storageAdapter,
        config.methodName
      );

    if (
      !methodProperty.isPresent ||
      !methodProperty.isValid ||
      typeof methodProperty.value !==
        "function"
    ) {
      return invalid(
        "persistence_cycle_registry_execution_guard_method_invalid"
      );
    }

    return createState({
      status:
        "exam_result_history_persistence_cycle_registry_execution_guard_ready",
      isValid: true,
      canProceedToInvocation: true,
      isExecutionBoundaryValidated: true,
      isCapabilityAvailable: true,
      isMethodReferenceValidated: true,
      intent:
        fields.intent,
      operation:
        fields.operation,
      methodName:
        fields.methodName,
      requiredCapability:
        fields.requiredCapability,
      readinessFingerprint:
        recomputedReadiness.readinessFingerprint,
      completedCycleCount,
      serializedByteLength,
      serializedJson,
      contractIdentity:
        fields.contractIdentity,
      operationPlanIdentity:
        fields.operationPlanIdentity,
      operationReleaseIdentity:
        fields.operationReleaseIdentity,
      executionGuardIdentity,
      reason: null
    });
  }

  function mapParticipantFullExamResultHistorySnapshotPersistenceCycleRegistryOperationReleaseState(input) {
    const source =
      input &&
      typeof input === "object" &&
      !Array.isArray(input)
        ? input
        : {};

    const operationReleaseVersion = 1;

    const storageNamespace =
      "accaoui:exam_history:persistence_cycle_registry";

    const storageKey =
      storageNamespace +
      ":v1";

    const registryIdentity =
      "exam_history_persistence_cycle_registry:v1";

    const maximumSerializedBytes = 32768;

    const maximumCompletedCycleIdentities =
      100;

    const inspectOwnDataProperty = (
      target,
      propertyName
    ) => {
      try {
        const descriptor =
          Object.getOwnPropertyDescriptor(
            target,
            propertyName
          );

        if (!descriptor) {
          return {
            isPresent: false,
            isValid: true,
            value: null
          };
        }

        if (
          !Object.prototype.hasOwnProperty.call(
            descriptor,
            "value"
          )
        ) {
          return {
            isPresent: true,
            isValid: false,
            value: null
          };
        }

        return {
          isPresent: true,
          isValid: true,
          value:
            descriptor.value
        };
      } catch (_error) {
        return {
          isPresent: true,
          isValid: false,
          value: null
        };
      }
    };

    const readRequiredFields = (
      target,
      fieldNames
    ) => {
      const fields = {};

      for (
        let index = 0;
        index < fieldNames.length;
        index += 1
      ) {
        const fieldName =
          fieldNames[index];

        const property =
          inspectOwnDataProperty(
            target,
            fieldName
          );

        if (
          !property.isPresent ||
          !property.isValid
        ) {
          return {
            isValid: false,
            fields: {}
          };
        }

        fields[fieldName] =
          property.value;
      }

      return {
        isValid: true,
        fields
      };
    };

    const createState = ({
      status,
      isValid,
      canReleaseOperation,
      isCapabilityAvailable,
      isMethodReferenceValidated,
      intent = null,
      operation = null,
      methodName = null,
      requiredCapability = null,
      readinessFingerprint = null,
      completedCycleCount = null,
      serializedByteLength = null,
      serializedJson = null,
      contractIdentity = null,
      operationPlanIdentity = null,
      operationReleaseIdentity = null,
      reason
    }) => ({
      version: "v27.30o",
      status,
      isValid,
      isSnapshotPersistenceCycleRegistryOperationReleaseMapperOnly: true,
      isLiveCall: false,
      canReleaseOperation,
      canInvokeLater:
        canReleaseOperation,
      isCapabilityAvailable,
      isMethodReferenceValidated,
      canReleaseSave:
        canReleaseOperation &&
        intent === "save",
      canReleaseLoad:
        canReleaseOperation &&
        intent === "load",
      canReleaseDelete:
        canReleaseOperation &&
        intent === "delete",
      canExecuteStorage: false,
      operationReleaseVersion,
      intent,
      operation,
      methodName,
      requiredCapability,
      storageNamespace,
      storageKey,
      registryIdentity,
      maximumSerializedBytes,
      maximumCompletedCycleIdentities,
      readinessFingerprint,
      completedCycleCount,
      serializedByteLength,
      serializedJson,
      contractIdentity,
      operationPlanIdentity,
      operationReleaseIdentity,
      reason
    });

    const invalid = (reason) =>
      createState({
        status:
          "exam_result_history_persistence_cycle_registry_operation_release_invalid",
        isValid: false,
        canReleaseOperation: false,
        isCapabilityAvailable: false,
        isMethodReferenceValidated: false,
        reason
      });

    const planProperty =
      inspectOwnDataProperty(
        source,
        "operationPlanState"
      );

    const adapterProperty =
      inspectOwnDataProperty(
        source,
        "storageAdapter"
      );

    if (!planProperty.isPresent) {
      return invalid(
        "persistence_cycle_registry_operation_release_plan_missing"
      );
    }

    if (!planProperty.isValid) {
      return invalid(
        "persistence_cycle_registry_operation_release_plan_accessor_not_allowed"
      );
    }

    if (!adapterProperty.isPresent) {
      return invalid(
        "persistence_cycle_registry_operation_release_adapter_missing"
      );
    }

    if (!adapterProperty.isValid) {
      return invalid(
        "persistence_cycle_registry_operation_release_adapter_accessor_not_allowed"
      );
    }

    const operationPlanState =
      planProperty.value;

    const storageAdapter =
      adapterProperty.value;

    if (
      !operationPlanState ||
      typeof operationPlanState !==
        "object" ||
      Array.isArray(
        operationPlanState
      )
    ) {
      return invalid(
        "persistence_cycle_registry_operation_release_plan_invalid"
      );
    }

    if (
      !storageAdapter ||
      typeof storageAdapter !== "object" ||
      Array.isArray(storageAdapter)
    ) {
      return invalid(
        "persistence_cycle_registry_operation_release_adapter_invalid"
      );
    }

    const fieldsState =
      readRequiredFields(
        operationPlanState,
        [
          "status",
          "isValid",
          "isSnapshotPersistenceCycleRegistryOperationPlanMapperOnly",
          "isLiveCall",
          "canPrepareOperation",
          "canInvokeLater",
          "isCapabilityAvailable",
          "canPlanSave",
          "canPlanLoad",
          "canPlanDelete",
          "canExecuteStorage",
          "operationPlanVersion",
          "intent",
          "operation",
          "methodName",
          "requiredCapability",
          "storageNamespace",
          "storageKey",
          "registryIdentity",
          "maximumSerializedBytes",
          "maximumCompletedCycleIdentities",
          "readinessFingerprint",
          "completedCycleCount",
          "serializedByteLength",
          "serializedJson",
          "contractIdentity",
          "operationPlanIdentity",
          "reason"
        ]
      );

    if (!fieldsState.isValid) {
      return invalid(
        "persistence_cycle_registry_operation_release_plan_fields_invalid"
      );
    }

    const fields =
      fieldsState.fields;

    const intentConfig = {
      save: {
        operation: "write",
        methodName: "write",
        requiredCapability: "write"
      },
      load: {
        operation: "read",
        methodName: "read",
        requiredCapability: "read"
      },
      delete: {
        operation: "delete",
        methodName: "delete",
        requiredCapability: "delete"
      }
    };

    const config =
      intentConfig[
        fields.intent
      ];

    if (
      !config ||
      fields.isValid !== true ||
      fields.isSnapshotPersistenceCycleRegistryOperationPlanMapperOnly !==
        true ||
      fields.isLiveCall !== false ||
      fields.canExecuteStorage !== false ||
      fields.operationPlanVersion !== 1 ||
      fields.operation !==
        config.operation ||
      fields.methodName !==
        config.methodName ||
      fields.requiredCapability !==
        config.requiredCapability ||
      fields.storageNamespace !==
        storageNamespace ||
      fields.storageKey !==
        storageKey ||
      fields.registryIdentity !==
        registryIdentity ||
      fields.maximumSerializedBytes !==
        maximumSerializedBytes ||
      fields.maximumCompletedCycleIdentities !==
        maximumCompletedCycleIdentities ||
      fields.contractIdentity !==
        (
          "exam_history_persistence_cycle_registry_contract:" +
          fields.intent +
          ":v1"
        ) ||
      fields.operationPlanIdentity !==
        (
          "exam_history_persistence_cycle_registry_operation_plan:" +
          fields.intent +
          ":v1"
        )
    ) {
      return invalid(
        "persistence_cycle_registry_operation_release_plan_invalid"
      );
    }

    let completedCycleCount = null;
    let serializedByteLength = null;
    let serializedJson = null;

    if (fields.intent === "save") {
      if (
        !Number.isInteger(
          fields.completedCycleCount
        ) ||
        fields.completedCycleCount < 0 ||
        fields.completedCycleCount >
          maximumCompletedCycleIdentities ||
        !Number.isSafeInteger(
          fields.serializedByteLength
        ) ||
        fields.serializedByteLength < 1 ||
        fields.serializedByteLength >
          maximumSerializedBytes ||
        typeof fields.serializedJson !==
          "string"
      ) {
        return invalid(
          "persistence_cycle_registry_operation_release_save_payload_invalid"
        );
      }

      const actualByteLength =
        getParticipantFullExamResultHistorySnapshotUtf8ByteLength(
          fields.serializedJson
        );

      if (
        actualByteLength !==
          fields.serializedByteLength
      ) {
        return invalid(
          "persistence_cycle_registry_operation_release_save_size_mismatch"
        );
      }

      const deserializationState =
        mapParticipantFullExamResultHistorySnapshotPersistenceCycleRegistryDeserializationState({
          serializedJson:
            fields.serializedJson
        });

      if (
        !deserializationState.isValid ||
        deserializationState.canDeserializeRegistry !==
          true ||
        deserializationState.canUseRegistry !==
          true ||
        deserializationState.canPersistLater !==
          true ||
        deserializationState.canExecuteStorage !==
          false ||
        deserializationState.registryIdentity !==
          registryIdentity ||
        deserializationState.completedCycleCount !==
          fields.completedCycleCount ||
        deserializationState.serializedByteLength !==
          actualByteLength
      ) {
        return invalid(
          "persistence_cycle_registry_operation_release_save_round_trip_invalid"
        );
      }

      completedCycleCount =
        fields.completedCycleCount;

      serializedByteLength =
        actualByteLength;

      serializedJson =
        fields.serializedJson;
    } else if (
      fields.completedCycleCount !== null ||
      fields.serializedByteLength !== null ||
      fields.serializedJson !== null
    ) {
      return invalid(
        "persistence_cycle_registry_operation_release_payload_unexpected"
      );
    }

    const recomputedReadiness =
      mapParticipantFullExamResultHistorySnapshotPersistenceCycleRegistryStorageAdapterReadinessState({
        storageAdapter
      });

    if (
      !recomputedReadiness.isValid ||
      recomputedReadiness.isSnapshotPersistenceCycleRegistryStorageAdapterReadinessMapperOnly !==
        true ||
      recomputedReadiness.isLiveCall !==
        false ||
      recomputedReadiness.canExecuteStorage !==
        false ||
      recomputedReadiness.readinessVersion !==
        1 ||
      recomputedReadiness.adapterMode !==
        "own_data_methods_only" ||
      typeof recomputedReadiness.readinessFingerprint !==
        "string" ||
      recomputedReadiness.reason !== null
    ) {
      return invalid(
        "persistence_cycle_registry_operation_release_adapter_readiness_invalid"
      );
    }

    if (
      recomputedReadiness.readinessFingerprint !==
        fields.readinessFingerprint
    ) {
      return invalid(
        "persistence_cycle_registry_operation_release_readiness_mismatch"
      );
    }

    const capabilityState = {
      read:
        recomputedReadiness.canPrepareRead ===
        true,
      write:
        recomputedReadiness.canPrepareWrite ===
        true,
      delete:
        recomputedReadiness.canPrepareDelete ===
        true
    };

    const isCapabilityAvailable =
      capabilityState[
        config.requiredCapability
      ] === true;

    const isReadyPlan =
      fields.status ===
        "exam_result_history_persistence_cycle_registry_operation_plan_ready" &&
      fields.canPrepareOperation ===
        true &&
      fields.canInvokeLater ===
        true &&
      fields.isCapabilityAvailable ===
        true &&
      fields.reason === null;

    const isBlockedPlan =
      fields.status ===
        "exam_result_history_persistence_cycle_registry_operation_plan_blocked" &&
      fields.canPrepareOperation ===
        false &&
      fields.canInvokeLater ===
        false &&
      fields.isCapabilityAvailable ===
        false &&
      fields.canPlanSave === false &&
      fields.canPlanLoad === false &&
      fields.canPlanDelete === false &&
      fields.reason ===
        "persistence_cycle_registry_operation_plan_capability_unavailable";

    if (!isReadyPlan && !isBlockedPlan) {
      return invalid(
        "persistence_cycle_registry_operation_release_plan_state_invalid"
      );
    }

    const expectedPlanFlags = {
      save:
        fields.intent === "save",
      load:
        fields.intent === "load",
      delete:
        fields.intent === "delete"
    };

    if (
      isReadyPlan &&
      (
        fields.canPlanSave !==
          expectedPlanFlags.save ||
        fields.canPlanLoad !==
          expectedPlanFlags.load ||
        fields.canPlanDelete !==
          expectedPlanFlags.delete
      )
    ) {
      return invalid(
        "persistence_cycle_registry_operation_release_plan_flags_invalid"
      );
    }

    const operationReleaseIdentity =
      "exam_history_persistence_cycle_registry_operation_release:" +
      fields.intent +
      ":v1";

    if (isBlockedPlan) {
      if (isCapabilityAvailable) {
        return invalid(
          "persistence_cycle_registry_operation_release_blocked_capability_mismatch"
        );
      }

      return createState({
        status:
          "exam_result_history_persistence_cycle_registry_operation_release_blocked",
        isValid: true,
        canReleaseOperation: false,
        isCapabilityAvailable: false,
        isMethodReferenceValidated: false,
        intent:
          fields.intent,
        operation:
          fields.operation,
        methodName:
          fields.methodName,
        requiredCapability:
          fields.requiredCapability,
        readinessFingerprint:
          recomputedReadiness.readinessFingerprint,
        completedCycleCount,
        serializedByteLength,
        serializedJson,
        contractIdentity:
          fields.contractIdentity,
        operationPlanIdentity:
          fields.operationPlanIdentity,
        operationReleaseIdentity,
        reason:
          "persistence_cycle_registry_operation_release_capability_unavailable"
      });
    }

    if (!isCapabilityAvailable) {
      return invalid(
        "persistence_cycle_registry_operation_release_capability_mismatch"
      );
    }

    const methodProperty =
      inspectOwnDataProperty(
        storageAdapter,
        config.methodName
      );

    if (
      !methodProperty.isPresent ||
      !methodProperty.isValid ||
      typeof methodProperty.value !==
        "function"
    ) {
      return invalid(
        "persistence_cycle_registry_operation_release_method_invalid"
      );
    }

    return createState({
      status:
        "exam_result_history_persistence_cycle_registry_operation_release_ready",
      isValid: true,
      canReleaseOperation: true,
      isCapabilityAvailable: true,
      isMethodReferenceValidated: true,
      intent:
        fields.intent,
      operation:
        fields.operation,
      methodName:
        fields.methodName,
      requiredCapability:
        fields.requiredCapability,
      readinessFingerprint:
        recomputedReadiness.readinessFingerprint,
      completedCycleCount,
      serializedByteLength,
      serializedJson,
      contractIdentity:
        fields.contractIdentity,
      operationPlanIdentity:
        fields.operationPlanIdentity,
      operationReleaseIdentity,
      reason: null
    });
  }

  function mapParticipantFullExamResultHistorySnapshotPersistenceCycleRegistryOperationPlanState(input) {
    const source =
      input &&
      typeof input === "object" &&
      !Array.isArray(input)
        ? input
        : {};

    const operationPlanVersion = 1;
    const storageNamespace =
      "accaoui:exam_history:persistence_cycle_registry";
    const storageKey =
      storageNamespace +
      ":v1";
    const registryIdentity =
      "exam_history_persistence_cycle_registry:v1";
    const maximumSerializedBytes = 32768;
    const maximumCompletedCycleIdentities =
      100;

    const inspectOwnDataProperty = (
      target,
      propertyName
    ) => {
      try {
        const descriptor =
          Object.getOwnPropertyDescriptor(
            target,
            propertyName
          );

        if (!descriptor) {
          return {
            isPresent: false,
            isValid: true,
            value: null
          };
        }

        if (
          !Object.prototype.hasOwnProperty.call(
            descriptor,
            "value"
          )
        ) {
          return {
            isPresent: true,
            isValid: false,
            value: null
          };
        }

        return {
          isPresent: true,
          isValid: true,
          value:
            descriptor.value
        };
      } catch (_error) {
        return {
          isPresent: true,
          isValid: false,
          value: null
        };
      }
    };

    const readRequiredFields = (
      target,
      fieldNames
    ) => {
      const fields = {};

      for (
        let index = 0;
        index < fieldNames.length;
        index += 1
      ) {
        const fieldName =
          fieldNames[index];

        const property =
          inspectOwnDataProperty(
            target,
            fieldName
          );

        if (
          !property.isPresent ||
          !property.isValid
        ) {
          return {
            isValid: false,
            fields: {}
          };
        }

        fields[fieldName] =
          property.value;
      }

      return {
        isValid: true,
        fields
      };
    };

    const cloneStringArray = (
      value
    ) => {
      try {
        if (!Array.isArray(value)) {
          return {
            isValid: false,
            values: []
          };
        }

        const values = [];
        const expectedKeys = [];

        for (
          let index = 0;
          index < value.length;
          index += 1
        ) {
          const propertyName =
            String(index);

          const descriptor =
            Object.getOwnPropertyDescriptor(
              value,
              propertyName
            );

          if (
            !descriptor ||
            !Object.prototype.hasOwnProperty.call(
              descriptor,
              "value"
            ) ||
            typeof descriptor.value !==
              "string"
          ) {
            return {
              isValid: false,
              values: []
            };
          }

          expectedKeys.push(
            propertyName
          );

          values.push(
            descriptor.value
          );
        }

        if (
          JSON.stringify(
            Object.keys(value)
          ) !==
          JSON.stringify(
            expectedKeys
          )
        ) {
          return {
            isValid: false,
            values: []
          };
        }

        return {
          isValid: true,
          values
        };
      } catch (_error) {
        return {
          isValid: false,
          values: []
        };
      }
    };

    const createState = ({
      status,
      isValid,
      canPrepareOperation,
      isCapabilityAvailable,
      intent = null,
      operation = null,
      methodName = null,
      requiredCapability = null,
      readinessFingerprint = null,
      completedCycleCount = null,
      serializedByteLength = null,
      serializedJson = null,
      contractIdentity = null,
      operationPlanIdentity = null,
      reason
    }) => ({
      version: "v27.30n",
      status,
      isValid,
      isSnapshotPersistenceCycleRegistryOperationPlanMapperOnly: true,
      isLiveCall: false,
      canPrepareOperation,
      canInvokeLater:
        canPrepareOperation,
      isCapabilityAvailable,
      canPlanSave:
        canPrepareOperation &&
        intent === "save",
      canPlanLoad:
        canPrepareOperation &&
        intent === "load",
      canPlanDelete:
        canPrepareOperation &&
        intent === "delete",
      canExecuteStorage: false,
      operationPlanVersion,
      intent,
      operation,
      methodName,
      requiredCapability,
      storageNamespace,
      storageKey,
      registryIdentity,
      maximumSerializedBytes,
      maximumCompletedCycleIdentities,
      readinessFingerprint,
      completedCycleCount,
      serializedByteLength,
      serializedJson,
      contractIdentity,
      operationPlanIdentity,
      reason
    });

    const invalid = (reason) =>
      createState({
        status:
          "exam_result_history_persistence_cycle_registry_operation_plan_invalid",
        isValid: false,
        canPrepareOperation: false,
        isCapabilityAvailable: false,
        reason
      });

    const contractProperty =
      inspectOwnDataProperty(
        source,
        "contractState"
      );

    const readinessProperty =
      inspectOwnDataProperty(
        source,
        "adapterReadinessState"
      );

    if (!contractProperty.isPresent) {
      return invalid(
        "persistence_cycle_registry_operation_plan_contract_missing"
      );
    }

    if (!contractProperty.isValid) {
      return invalid(
        "persistence_cycle_registry_operation_plan_contract_accessor_not_allowed"
      );
    }

    if (!readinessProperty.isPresent) {
      return invalid(
        "persistence_cycle_registry_operation_plan_readiness_missing"
      );
    }

    if (!readinessProperty.isValid) {
      return invalid(
        "persistence_cycle_registry_operation_plan_readiness_accessor_not_allowed"
      );
    }

    const contractState =
      contractProperty.value;

    const adapterReadinessState =
      readinessProperty.value;

    if (
      !contractState ||
      typeof contractState !== "object" ||
      Array.isArray(contractState)
    ) {
      return invalid(
        "persistence_cycle_registry_operation_plan_contract_invalid"
      );
    }

    if (
      !adapterReadinessState ||
      typeof adapterReadinessState !==
        "object" ||
      Array.isArray(
        adapterReadinessState
      )
    ) {
      return invalid(
        "persistence_cycle_registry_operation_plan_readiness_invalid"
      );
    }

    const contractFieldsState =
      readRequiredFields(
        contractState,
        [
          "status",
          "isValid",
          "isSnapshotPersistenceCycleRegistryContractOnly",
          "isLiveCall",
          "canPrepareSave",
          "canPrepareLoad",
          "canPrepareDelete",
          "canPersistLater",
          "canExecuteStorage",
          "contractVersion",
          "intent",
          "operation",
          "requiredCapability",
          "storageNamespace",
          "storageKey",
          "registryVersion",
          "registryIdentity",
          "maximumSerializedBytes",
          "maximumCompletedCycleIdentities",
          "completedCycleCount",
          "serializedByteLength",
          "serializedJson",
          "contractIdentity",
          "reason"
        ]
      );

    if (!contractFieldsState.isValid) {
      return invalid(
        "persistence_cycle_registry_operation_plan_contract_fields_invalid"
      );
    }

    const contractFields =
      contractFieldsState.fields;

    const intentConfig = {
      save: {
        contractStatus:
          "exam_result_history_persistence_cycle_registry_contract_save_ready",
        operation: "write",
        methodName: "write",
        requiredCapability:
          "write",
        canPrepareSave: true,
        canPrepareLoad: false,
        canPrepareDelete: false
      },
      load: {
        contractStatus:
          "exam_result_history_persistence_cycle_registry_contract_load_ready",
        operation: "read",
        methodName: "read",
        requiredCapability:
          "read",
        canPrepareSave: false,
        canPrepareLoad: true,
        canPrepareDelete: false
      },
      delete: {
        contractStatus:
          "exam_result_history_persistence_cycle_registry_contract_delete_ready",
        operation: "delete",
        methodName: "delete",
        requiredCapability:
          "delete",
        canPrepareSave: false,
        canPrepareLoad: false,
        canPrepareDelete: true
      }
    };

    const config =
      intentConfig[
        contractFields.intent
      ];

    if (
      !config ||
      contractFields.isValid !== true ||
      contractFields.isSnapshotPersistenceCycleRegistryContractOnly !==
        true ||
      contractFields.isLiveCall !== false ||
      contractFields.canPersistLater !==
        true ||
      contractFields.canExecuteStorage !==
        false ||
      contractFields.contractVersion !==
        1 ||
      contractFields.status !==
        config.contractStatus ||
      contractFields.operation !==
        config.operation ||
      contractFields.requiredCapability !==
        config.requiredCapability ||
      contractFields.canPrepareSave !==
        config.canPrepareSave ||
      contractFields.canPrepareLoad !==
        config.canPrepareLoad ||
      contractFields.canPrepareDelete !==
        config.canPrepareDelete ||
      contractFields.storageNamespace !==
        storageNamespace ||
      contractFields.storageKey !==
        storageKey ||
      contractFields.registryVersion !==
        1 ||
      contractFields.registryIdentity !==
        registryIdentity ||
      contractFields.maximumSerializedBytes !==
        maximumSerializedBytes ||
      contractFields.maximumCompletedCycleIdentities !==
        maximumCompletedCycleIdentities ||
      contractFields.contractIdentity !==
        (
          "exam_history_persistence_cycle_registry_contract:" +
          contractFields.intent +
          ":v1"
        ) ||
      contractFields.reason !== null
    ) {
      return invalid(
        "persistence_cycle_registry_operation_plan_contract_invalid"
      );
    }

    let completedCycleCount = null;
    let serializedByteLength = null;
    let serializedJson = null;

    if (contractFields.intent === "save") {
      if (
        !Number.isInteger(
          contractFields.completedCycleCount
        ) ||
        contractFields.completedCycleCount <
          0 ||
        contractFields.completedCycleCount >
          maximumCompletedCycleIdentities ||
        !Number.isSafeInteger(
          contractFields.serializedByteLength
        ) ||
        contractFields.serializedByteLength <
          1 ||
        contractFields.serializedByteLength >
          maximumSerializedBytes ||
        typeof contractFields.serializedJson !==
          "string"
      ) {
        return invalid(
          "persistence_cycle_registry_operation_plan_save_payload_invalid"
        );
      }

      const actualByteLength =
        getParticipantFullExamResultHistorySnapshotUtf8ByteLength(
          contractFields.serializedJson
        );

      if (
        actualByteLength !==
          contractFields.serializedByteLength
      ) {
        return invalid(
          "persistence_cycle_registry_operation_plan_save_size_mismatch"
        );
      }

      const deserializationState =
        mapParticipantFullExamResultHistorySnapshotPersistenceCycleRegistryDeserializationState({
          serializedJson:
            contractFields.serializedJson
        });

      if (
        !deserializationState.isValid ||
        deserializationState.canDeserializeRegistry !==
          true ||
        deserializationState.canUseRegistry !==
          true ||
        deserializationState.canPersistLater !==
          true ||
        deserializationState.canExecuteStorage !==
          false ||
        deserializationState.registryIdentity !==
          registryIdentity ||
        deserializationState.completedCycleCount !==
          contractFields.completedCycleCount ||
        deserializationState.serializedByteLength !==
          actualByteLength
      ) {
        return invalid(
          "persistence_cycle_registry_operation_plan_save_round_trip_invalid"
        );
      }

      completedCycleCount =
        contractFields.completedCycleCount;

      serializedByteLength =
        actualByteLength;

      serializedJson =
        contractFields.serializedJson;
    } else if (
      contractFields.completedCycleCount !==
        null ||
      contractFields.serializedByteLength !==
        null ||
      contractFields.serializedJson !==
        null
    ) {
      return invalid(
        "persistence_cycle_registry_operation_plan_payload_unexpected"
      );
    }

    const readinessFieldsState =
      readRequiredFields(
        adapterReadinessState,
        [
          "status",
          "isValid",
          "isSnapshotPersistenceCycleRegistryStorageAdapterReadinessMapperOnly",
          "isLiveCall",
          "canUseAdapter",
          "isFullyReady",
          "canPrepareRead",
          "canPrepareWrite",
          "canPrepareDelete",
          "canExecuteStorage",
          "readinessVersion",
          "adapterMode",
          "availableCapabilityCount",
          "availableCapabilities",
          "unavailableCapabilities",
          "readinessFingerprint",
          "reason"
        ]
      );

    if (!readinessFieldsState.isValid) {
      return invalid(
        "persistence_cycle_registry_operation_plan_readiness_fields_invalid"
      );
    }

    const readinessFields =
      readinessFieldsState.fields;

    const availableState =
      cloneStringArray(
        readinessFields.availableCapabilities
      );

    const unavailableState =
      cloneStringArray(
        readinessFields.unavailableCapabilities
      );

    if (
      !availableState.isValid ||
      !unavailableState.isValid
    ) {
      return invalid(
        "persistence_cycle_registry_operation_plan_readiness_capabilities_invalid"
      );
    }

    const capabilityNames = [
      "read",
      "write",
      "delete"
    ];

    const capabilityState = {
      read:
        readinessFields.canPrepareRead ===
        true,
      write:
        readinessFields.canPrepareWrite ===
        true,
      delete:
        readinessFields.canPrepareDelete ===
        true
    };

    const expectedAvailable = [];
    const expectedUnavailable = [];

    for (
      let index = 0;
      index < capabilityNames.length;
      index += 1
    ) {
      const capabilityName =
        capabilityNames[index];

      if (
        capabilityState[
          capabilityName
        ]
      ) {
        expectedAvailable.push(
          capabilityName
        );
      } else {
        expectedUnavailable.push(
          capabilityName
        );
      }
    }

    const expectedCapabilityCount =
      expectedAvailable.length;

    const expectedFullyReady =
      expectedCapabilityCount ===
      capabilityNames.length;

    const expectedCanUseAdapter =
      expectedCapabilityCount > 0;

    const expectedReadinessStatus =
      expectedFullyReady
        ? "exam_result_history_persistence_cycle_registry_storage_adapter_ready"
        : expectedCanUseAdapter
          ? "exam_result_history_persistence_cycle_registry_storage_adapter_partial"
          : "exam_result_history_persistence_cycle_registry_storage_adapter_unavailable";

    const expectedReadinessFingerprint =
      "exam_history_persistence_cycle_registry_storage_adapter_readiness:v1:" +
      "read=" +
      (
        capabilityState.read
          ? "1"
          : "0"
      ) +
      ":write=" +
      (
        capabilityState.write
          ? "1"
          : "0"
      ) +
      ":delete=" +
      (
        capabilityState.delete
          ? "1"
          : "0"
      );

    if (
      readinessFields.isValid !== true ||
      readinessFields.isSnapshotPersistenceCycleRegistryStorageAdapterReadinessMapperOnly !==
        true ||
      readinessFields.isLiveCall !== false ||
      readinessFields.canExecuteStorage !==
        false ||
      readinessFields.readinessVersion !==
        1 ||
      readinessFields.adapterMode !==
        "own_data_methods_only" ||
      readinessFields.status !==
        expectedReadinessStatus ||
      readinessFields.canUseAdapter !==
        expectedCanUseAdapter ||
      readinessFields.isFullyReady !==
        expectedFullyReady ||
      readinessFields.availableCapabilityCount !==
        expectedCapabilityCount ||
      JSON.stringify(
        availableState.values
      ) !==
        JSON.stringify(
          expectedAvailable
        ) ||
      JSON.stringify(
        unavailableState.values
      ) !==
        JSON.stringify(
          expectedUnavailable
        ) ||
      readinessFields.readinessFingerprint !==
        expectedReadinessFingerprint ||
      readinessFields.reason !== null
    ) {
      return invalid(
        "persistence_cycle_registry_operation_plan_readiness_invalid"
      );
    }

    const isCapabilityAvailable =
      capabilityState[
        config.requiredCapability
      ] === true;

    const operationPlanIdentity =
      "exam_history_persistence_cycle_registry_operation_plan:" +
      contractFields.intent +
      ":v1";

    if (!isCapabilityAvailable) {
      return createState({
        status:
          "exam_result_history_persistence_cycle_registry_operation_plan_blocked",
        isValid: true,
        canPrepareOperation: false,
        isCapabilityAvailable: false,
        intent:
          contractFields.intent,
        operation:
          config.operation,
        methodName:
          config.methodName,
        requiredCapability:
          config.requiredCapability,
        readinessFingerprint:
          expectedReadinessFingerprint,
        completedCycleCount,
        serializedByteLength,
        serializedJson,
        contractIdentity:
          contractFields.contractIdentity,
        operationPlanIdentity,
        reason:
          "persistence_cycle_registry_operation_plan_capability_unavailable"
      });
    }

    return createState({
      status:
        "exam_result_history_persistence_cycle_registry_operation_plan_ready",
      isValid: true,
      canPrepareOperation: true,
      isCapabilityAvailable: true,
      intent:
        contractFields.intent,
      operation:
        config.operation,
      methodName:
        config.methodName,
      requiredCapability:
        config.requiredCapability,
      readinessFingerprint:
        expectedReadinessFingerprint,
      completedCycleCount,
      serializedByteLength,
      serializedJson,
      contractIdentity:
        contractFields.contractIdentity,
      operationPlanIdentity,
      reason: null
    });
  }

  function mapParticipantFullExamResultHistorySnapshotPersistenceCycleRegistryStorageAdapterReadinessState(input) {
    const source =
      input &&
      typeof input === "object" &&
      !Array.isArray(input)
        ? input
        : {};

    const readinessVersion = 1;

    const inspectOwnDataProperty = (
      target,
      propertyName
    ) => {
      try {
        const descriptor =
          Object.getOwnPropertyDescriptor(
            target,
            propertyName
          );

        if (!descriptor) {
          return {
            isPresent: false,
            isValid: true,
            value: null
          };
        }

        if (
          !Object.prototype.hasOwnProperty.call(
            descriptor,
            "value"
          )
        ) {
          return {
            isPresent: true,
            isValid: false,
            value: null
          };
        }

        return {
          isPresent: true,
          isValid: true,
          value:
            descriptor.value
        };
      } catch (_error) {
        return {
          isPresent: true,
          isValid: false,
          value: null
        };
      }
    };

    const invalid = (reason) => ({
      version: "v27.30m",
      status:
        "exam_result_history_persistence_cycle_registry_storage_adapter_invalid",
      isValid: false,
      isSnapshotPersistenceCycleRegistryStorageAdapterReadinessMapperOnly: true,
      isLiveCall: false,
      canUseAdapter: false,
      isFullyReady: false,
      canPrepareRead: false,
      canPrepareWrite: false,
      canPrepareDelete: false,
      canExecuteStorage: false,
      readinessVersion,
      adapterMode:
        "own_data_methods_only",
      availableCapabilityCount: 0,
      availableCapabilities: [],
      unavailableCapabilities: [
        "read",
        "write",
        "delete"
      ],
      readinessFingerprint: null,
      reason
    });

    const adapterProperty =
      inspectOwnDataProperty(
        source,
        "storageAdapter"
      );

    if (!adapterProperty.isPresent) {
      return invalid(
        "persistence_cycle_registry_storage_adapter_missing"
      );
    }

    if (!adapterProperty.isValid) {
      return invalid(
        "persistence_cycle_registry_storage_adapter_accessor_not_allowed"
      );
    }

    const storageAdapter =
      adapterProperty.value;

    if (
      !storageAdapter ||
      typeof storageAdapter !== "object" ||
      Array.isArray(storageAdapter)
    ) {
      return invalid(
        "persistence_cycle_registry_storage_adapter_invalid"
      );
    }

    const capabilityNames = [
      "read",
      "write",
      "delete"
    ];

    const capabilityState = {
      read: false,
      write: false,
      delete: false
    };

    const availableCapabilities = [];
    const unavailableCapabilities = [];

    for (
      let index = 0;
      index < capabilityNames.length;
      index += 1
    ) {
      const capabilityName =
        capabilityNames[index];

      const property =
        inspectOwnDataProperty(
          storageAdapter,
          capabilityName
        );

      if (!property.isValid) {
        return invalid(
          "persistence_cycle_registry_storage_adapter_" +
          capabilityName +
          "_accessor_not_allowed"
        );
      }

      if (
        property.isPresent &&
        typeof property.value !==
          "function"
      ) {
        return invalid(
          "persistence_cycle_registry_storage_adapter_" +
          capabilityName +
          "_method_invalid"
        );
      }

      const isAvailable =
        property.isPresent &&
        typeof property.value ===
          "function";

      capabilityState[
        capabilityName
      ] = isAvailable;

      if (isAvailable) {
        availableCapabilities.push(
          capabilityName
        );
      } else {
        unavailableCapabilities.push(
          capabilityName
        );
      }
    }

    const availableCapabilityCount =
      availableCapabilities.length;

    const isFullyReady =
      availableCapabilityCount ===
      capabilityNames.length;

    const canUseAdapter =
      availableCapabilityCount > 0;

    const status =
      isFullyReady
        ? "exam_result_history_persistence_cycle_registry_storage_adapter_ready"
        : canUseAdapter
          ? "exam_result_history_persistence_cycle_registry_storage_adapter_partial"
          : "exam_result_history_persistence_cycle_registry_storage_adapter_unavailable";

    const readinessFingerprint =
      "exam_history_persistence_cycle_registry_storage_adapter_readiness:v1:" +
      "read=" +
      (
        capabilityState.read
          ? "1"
          : "0"
      ) +
      ":write=" +
      (
        capabilityState.write
          ? "1"
          : "0"
      ) +
      ":delete=" +
      (
        capabilityState.delete
          ? "1"
          : "0"
      );

    return {
      version: "v27.30m",
      status,
      isValid: true,
      isSnapshotPersistenceCycleRegistryStorageAdapterReadinessMapperOnly: true,
      isLiveCall: false,
      canUseAdapter,
      isFullyReady,
      canPrepareRead:
        capabilityState.read,
      canPrepareWrite:
        capabilityState.write,
      canPrepareDelete:
        capabilityState.delete,
      canExecuteStorage: false,
      readinessVersion,
      adapterMode:
        "own_data_methods_only",
      availableCapabilityCount,
      availableCapabilities,
      unavailableCapabilities,
      readinessFingerprint,
      reason: null
    };
  }

  function mapParticipantFullExamResultHistorySnapshotPersistenceCycleRegistryContract(input) {
    const source =
      input &&
      typeof input === "object" &&
      !Array.isArray(input)
        ? input
        : {};

    const contractVersion = 1;
    const registryVersion = 1;
    const maximumSerializedBytes = 32768;
    const maximumCompletedCycleIdentities =
      100;

    const storageNamespace =
      "accaoui:exam_history:persistence_cycle_registry";

    const storageKey =
      storageNamespace +
      ":v1";

    const registryIdentity =
      "exam_history_persistence_cycle_registry:v1";

    const inspectOwnDataProperty = (
      target,
      propertyName
    ) => {
      try {
        const descriptor =
          Object.getOwnPropertyDescriptor(
            target,
            propertyName
          );

        if (!descriptor) {
          return {
            isPresent: false,
            isValid: true,
            value: null
          };
        }

        if (
          !Object.prototype.hasOwnProperty.call(
            descriptor,
            "value"
          )
        ) {
          return {
            isPresent: true,
            isValid: false,
            value: null
          };
        }

        return {
          isPresent: true,
          isValid: true,
          value:
            descriptor.value
        };
      } catch (_error) {
        return {
          isPresent: true,
          isValid: false,
          value: null
        };
      }
    };

    const invalid = (reason) => ({
      version: "v27.30l",
      status:
        "exam_result_history_persistence_cycle_registry_contract_invalid",
      isValid: false,
      isSnapshotPersistenceCycleRegistryContractOnly: true,
      isLiveCall: false,
      canPrepareSave: false,
      canPrepareLoad: false,
      canPrepareDelete: false,
      canPersistLater: false,
      canExecuteStorage: false,
      contractVersion,
      intent: null,
      operation: null,
      requiredCapability: null,
      storageNamespace,
      storageKey,
      registryVersion,
      registryIdentity,
      maximumSerializedBytes,
      maximumCompletedCycleIdentities,
      completedCycleCount: null,
      serializedByteLength: null,
      serializedJson: null,
      contractIdentity: null,
      reason
    });

    const intentProperty =
      inspectOwnDataProperty(
        source,
        "intent"
      );

    const serializationProperty =
      inspectOwnDataProperty(
        source,
        "serializationState"
      );

    if (!intentProperty.isPresent) {
      return invalid(
        "persistence_cycle_registry_contract_intent_missing"
      );
    }

    if (!intentProperty.isValid) {
      return invalid(
        "persistence_cycle_registry_contract_intent_accessor_not_allowed"
      );
    }

    if (!serializationProperty.isValid) {
      return invalid(
        "persistence_cycle_registry_contract_serialization_accessor_not_allowed"
      );
    }

    const intent =
      intentProperty.value;

    const intentConfig = {
      save: {
        status:
          "exam_result_history_persistence_cycle_registry_contract_save_ready",
        operation: "write",
        requiredCapability: "write"
      },
      load: {
        status:
          "exam_result_history_persistence_cycle_registry_contract_load_ready",
        operation: "read",
        requiredCapability: "read"
      },
      delete: {
        status:
          "exam_result_history_persistence_cycle_registry_contract_delete_ready",
        operation: "delete",
        requiredCapability: "delete"
      }
    };

    const config =
      intentConfig[intent];

    if (!config) {
      return invalid(
        "persistence_cycle_registry_contract_intent_invalid"
      );
    }

    let completedCycleCount = null;
    let serializedByteLength = null;
    let serializedJson = null;

    if (intent === "save") {
      if (
        !serializationProperty.isPresent
      ) {
        return invalid(
          "persistence_cycle_registry_contract_serialization_state_missing"
        );
      }

      const serializationState =
        serializationProperty.value;

      if (
        !serializationState ||
        typeof serializationState !==
          "object" ||
        Array.isArray(
          serializationState
        ) ||
        serializationState.isSnapshotPersistenceCycleRegistrySerializationMapperOnly !==
          true ||
        serializationState.isValid !==
          true ||
        serializationState.status !==
          "exam_result_history_persistence_cycle_registry_serialization_ready" ||
        serializationState.canSerializeRegistry !==
          true ||
        serializationState.canPersistLater !==
          true ||
        serializationState.canWriteStorage !==
          false ||
        serializationState.canExecuteStorage !==
          false ||
        serializationState.serializationSchemaVersion !==
          1 ||
        serializationState.maximumSerializedBytes !==
          maximumSerializedBytes ||
        serializationState.registryVersion !==
          registryVersion ||
        serializationState.registryIdentity !==
          registryIdentity ||
        serializationState.maximumCompletedCycleIdentities !==
          maximumCompletedCycleIdentities ||
        !Number.isInteger(
          serializationState.completedCycleCount
        ) ||
        serializationState.completedCycleCount <
          0 ||
        serializationState.completedCycleCount >
          maximumCompletedCycleIdentities ||
        serializationState.isEmpty !==
          (
            serializationState.completedCycleCount ===
            0
          ) ||
        serializationState.isAtCapacity !==
          (
            serializationState.completedCycleCount ===
            maximumCompletedCycleIdentities
          ) ||
        typeof serializationState.serializedJson !==
          "string" ||
        !Number.isSafeInteger(
          serializationState.serializedByteLength
        ) ||
        serializationState.serializedByteLength <
          1 ||
        serializationState.serializedByteLength >
          maximumSerializedBytes ||
        serializationState.reason !==
          null
      ) {
        return invalid(
          "persistence_cycle_registry_contract_serialization_state_invalid"
        );
      }

      const actualByteLength =
        getParticipantFullExamResultHistorySnapshotUtf8ByteLength(
          serializationState.serializedJson
        );

      if (
        actualByteLength !==
        serializationState.serializedByteLength
      ) {
        return invalid(
          "persistence_cycle_registry_contract_serialization_size_mismatch"
        );
      }

      const deserializationState =
        mapParticipantFullExamResultHistorySnapshotPersistenceCycleRegistryDeserializationState({
          serializedJson:
            serializationState.serializedJson
        });

      if (
        !deserializationState.isValid ||
        deserializationState.canDeserializeRegistry !==
          true ||
        deserializationState.canUseRegistry !==
          true ||
        deserializationState.canPersistLater !==
          true ||
        deserializationState.canExecuteStorage !==
          false ||
        deserializationState.registryVersion !==
          registryVersion ||
        deserializationState.registryIdentity !==
          registryIdentity ||
        deserializationState.maximumCompletedCycleIdentities !==
          maximumCompletedCycleIdentities ||
        deserializationState.completedCycleCount !==
          serializationState.completedCycleCount ||
        deserializationState.serializedByteLength !==
          actualByteLength
      ) {
        return invalid(
          "persistence_cycle_registry_contract_serialization_round_trip_invalid"
        );
      }

      completedCycleCount =
        serializationState.completedCycleCount;

      serializedByteLength =
        actualByteLength;

      serializedJson =
        serializationState.serializedJson;
    } else if (
      serializationProperty.isPresent &&
      serializationProperty.value !==
        null &&
      serializationProperty.value !==
        undefined
    ) {
      return invalid(
        "persistence_cycle_registry_contract_serialization_unexpected"
      );
    }

    const contractIdentity =
      "exam_history_persistence_cycle_registry_contract:" +
      intent +
      ":v1";

    return {
      version: "v27.30l",
      status:
        config.status,
      isValid: true,
      isSnapshotPersistenceCycleRegistryContractOnly: true,
      isLiveCall: false,
      canPrepareSave:
        intent === "save",
      canPrepareLoad:
        intent === "load",
      canPrepareDelete:
        intent === "delete",
      canPersistLater: true,
      canExecuteStorage: false,
      contractVersion,
      intent,
      operation:
        config.operation,
      requiredCapability:
        config.requiredCapability,
      storageNamespace,
      storageKey,
      registryVersion,
      registryIdentity,
      maximumSerializedBytes,
      maximumCompletedCycleIdentities,
      completedCycleCount,
      serializedByteLength,
      serializedJson,
      contractIdentity,
      reason: null
    };
  }

  function mapParticipantFullExamResultHistorySnapshotPersistenceCycleRegistryDeserializationState(input) {
    const source =
      input &&
      typeof input === "object" &&
      !Array.isArray(input)
        ? input
        : {};

    const deserializationSchemaVersion = 1;
    const maximumSerializedBytes = 32768;
    const maximumCompletedCycleIdentities =
      100;

    const inspectOwnDataProperty = (
      target,
      propertyName
    ) => {
      try {
        const descriptor =
          Object.getOwnPropertyDescriptor(
            target,
            propertyName
          );

        if (!descriptor) {
          return {
            isPresent: false,
            isValid: true,
            value: null
          };
        }

        if (
          !Object.prototype.hasOwnProperty.call(
            descriptor,
            "value"
          )
        ) {
          return {
            isPresent: true,
            isValid: false,
            value: null
          };
        }

        return {
          isPresent: true,
          isValid: true,
          value:
            descriptor.value
        };
      } catch (_error) {
        return {
          isPresent: true,
          isValid: false,
          value: null
        };
      }
    };

    const invalid = (reason) => ({
      version: "v27.30k",
      status:
        "exam_result_history_persistence_cycle_registry_deserialization_invalid",
      isValid: false,
      isSnapshotPersistenceCycleRegistryDeserializationMapperOnly: true,
      isLiveCall: false,
      canDeserializeRegistry: false,
      canUseRegistry: false,
      canPersistLater: false,
      canExecuteStorage: false,
      deserializationSchemaVersion,
      maximumSerializedBytes,
      registryVersion: null,
      registryIdentity: null,
      maximumCompletedCycleIdentities,
      completedCycleCount: null,
      isEmpty: false,
      isAtCapacity: false,
      serializedByteLength: null,
      completedCycleIdentities: [],
      registryPayload: null,
      registryState: null,
      reason
    });

    const serializedProperty =
      inspectOwnDataProperty(
        source,
        "serializedJson"
      );

    if (!serializedProperty.isPresent) {
      return invalid(
        "persistence_cycle_registry_deserialization_json_missing"
      );
    }

    if (!serializedProperty.isValid) {
      return invalid(
        "persistence_cycle_registry_deserialization_json_accessor_not_allowed"
      );
    }

    const serializedJson =
      serializedProperty.value;

    if (
      typeof serializedJson !== "string"
    ) {
      return invalid(
        "persistence_cycle_registry_deserialization_json_invalid"
      );
    }

    const serializedByteLength =
      getParticipantFullExamResultHistorySnapshotUtf8ByteLength(
        serializedJson
      );

    if (
      !Number.isSafeInteger(
        serializedByteLength
      ) ||
      serializedByteLength < 1 ||
      serializedByteLength >
        maximumSerializedBytes
    ) {
      return invalid(
        "persistence_cycle_registry_deserialization_size_invalid"
      );
    }

    let parsedPayload;

    try {
      parsedPayload =
        JSON.parse(
          serializedJson
        );
    } catch (_error) {
      return invalid(
        "persistence_cycle_registry_deserialization_json_parse_failed"
      );
    }

    if (
      !parsedPayload ||
      typeof parsedPayload !== "object" ||
      Array.isArray(parsedPayload)
    ) {
      return invalid(
        "persistence_cycle_registry_deserialization_payload_invalid"
      );
    }

    let payloadKeys;

    try {
      payloadKeys =
        Object.keys(
          parsedPayload
        );
    } catch (_error) {
      return invalid(
        "persistence_cycle_registry_deserialization_payload_invalid"
      );
    }

    if (
      JSON.stringify(payloadKeys) !==
      JSON.stringify([
        "registryVersion",
        "completedCycleIdentities"
      ])
    ) {
      return invalid(
        "persistence_cycle_registry_deserialization_payload_fields_invalid"
      );
    }

    const registryVersionProperty =
      inspectOwnDataProperty(
        parsedPayload,
        "registryVersion"
      );

    const identitiesProperty =
      inspectOwnDataProperty(
        parsedPayload,
        "completedCycleIdentities"
      );

    if (
      !registryVersionProperty.isPresent ||
      !registryVersionProperty.isValid ||
      registryVersionProperty.value !== 1
    ) {
      return invalid(
        "persistence_cycle_registry_deserialization_version_invalid"
      );
    }

    if (
      !identitiesProperty.isPresent ||
      !identitiesProperty.isValid ||
      !Array.isArray(
        identitiesProperty.value
      ) ||
      identitiesProperty.value.length >
        maximumCompletedCycleIdentities
    ) {
      return invalid(
        "persistence_cycle_registry_deserialization_identities_invalid"
      );
    }

    if (
      JSON.stringify(
        parsedPayload
      ) !==
      serializedJson
    ) {
      return invalid(
        "persistence_cycle_registry_deserialization_json_not_canonical"
      );
    }

    const registryState =
      mapParticipantFullExamResultHistorySnapshotPersistenceCycleRegistryState({
        completedCycleIdentities:
          identitiesProperty.value
      });

    if (
      !registryState.isValid ||
      registryState.canUseRegistry !==
        true ||
      registryState.canExecuteStorage !==
        false ||
      registryState.registryVersion !==
        1 ||
      registryState.registryIdentity !==
        "exam_history_persistence_cycle_registry:v1" ||
      registryState.maximumCompletedCycleIdentities !==
        maximumCompletedCycleIdentities
    ) {
      return invalid(
        "persistence_cycle_registry_deserialization_registry_state_invalid"
      );
    }

    if (
      JSON.stringify(
        registryState.registryPayload
      ) !==
      serializedJson
    ) {
      return invalid(
        "persistence_cycle_registry_deserialization_payload_not_canonical"
      );
    }

    const serializationState =
      mapParticipantFullExamResultHistorySnapshotPersistenceCycleRegistrySerializationState({
        registryState
      });

    if (
      !serializationState.isValid ||
      serializationState.canSerializeRegistry !==
        true ||
      serializationState.canPersistLater !==
        true ||
      serializationState.canWriteStorage !==
        false ||
      serializationState.canExecuteStorage !==
        false ||
      serializationState.serializedJson !==
        serializedJson ||
      serializationState.serializedByteLength !==
        serializedByteLength
    ) {
      return invalid(
        "persistence_cycle_registry_deserialization_round_trip_invalid"
      );
    }

    const completedCycleIdentities =
      registryState
        .completedCycleIdentities
        .slice();

    const registryPayload = {
      registryVersion: 1,
      completedCycleIdentities:
        completedCycleIdentities.slice()
    };

    return {
      version: "v27.30k",
      status:
        "exam_result_history_persistence_cycle_registry_deserialization_ready",
      isValid: true,
      isSnapshotPersistenceCycleRegistryDeserializationMapperOnly: true,
      isLiveCall: false,
      canDeserializeRegistry: true,
      canUseRegistry: true,
      canPersistLater: true,
      canExecuteStorage: false,
      deserializationSchemaVersion,
      maximumSerializedBytes,
      registryVersion: 1,
      registryIdentity:
        "exam_history_persistence_cycle_registry:v1",
      maximumCompletedCycleIdentities,
      completedCycleCount:
        completedCycleIdentities.length,
      isEmpty:
        registryState.isEmpty,
      isAtCapacity:
        registryState.isAtCapacity,
      serializedByteLength,
      completedCycleIdentities,
      registryPayload,
      registryState,
      reason: null
    };
  }

  function mapParticipantFullExamResultHistorySnapshotPersistenceCycleRegistrySerializationState(input) {
    const source =
      input &&
      typeof input === "object" &&
      !Array.isArray(input)
        ? input
        : {};

    const serializationSchemaVersion = 1;
    const maximumSerializedBytes = 32768;
    const maximumCompletedCycleIdentities =
      100;

    const inspectOwnDataProperty = (
      target,
      propertyName
    ) => {
      try {
        const descriptor =
          Object.getOwnPropertyDescriptor(
            target,
            propertyName
          );

        if (!descriptor) {
          return {
            isPresent: false,
            isValid: true,
            value: null
          };
        }

        if (
          !Object.prototype.hasOwnProperty.call(
            descriptor,
            "value"
          )
        ) {
          return {
            isPresent: true,
            isValid: false,
            value: null
          };
        }

        return {
          isPresent: true,
          isValid: true,
          value:
            descriptor.value
        };
      } catch (_error) {
        return {
          isPresent: true,
          isValid: false,
          value: null
        };
      }
    };

    const invalid = (reason) => ({
      version: "v27.30j",
      status:
        "exam_result_history_persistence_cycle_registry_serialization_invalid",
      isValid: false,
      isSnapshotPersistenceCycleRegistrySerializationMapperOnly: true,
      isLiveCall: false,
      canSerializeRegistry: false,
      canPersistLater: false,
      canWriteStorage: false,
      canExecuteStorage: false,
      serializationSchemaVersion,
      maximumSerializedBytes,
      registryVersion: null,
      registryIdentity: null,
      maximumCompletedCycleIdentities,
      completedCycleCount: null,
      isEmpty: false,
      isAtCapacity: false,
      serializedByteLength: null,
      serializedJson: null,
      reason
    });

    const cloneIdentityArray = (
      value,
      reason
    ) => {
      try {
        if (
          !Array.isArray(value) ||
          value.length >
            maximumCompletedCycleIdentities
        ) {
          return {
            isValid: false,
            identities: [],
            reason
          };
        }

        const identities = [];
        const expectedKeys = [];

        for (
          let index = 0;
          index < value.length;
          index += 1
        ) {
          const propertyName =
            String(index);

          const descriptor =
            Object.getOwnPropertyDescriptor(
              value,
              propertyName
            );

          if (
            !descriptor ||
            !Object.prototype.hasOwnProperty.call(
              descriptor,
              "value"
            ) ||
            typeof descriptor.value !==
              "string"
          ) {
            return {
              isValid: false,
              identities: [],
              reason
            };
          }

          expectedKeys.push(
            propertyName
          );

          identities.push(
            descriptor.value
          );
        }

        if (
          JSON.stringify(
            Object.keys(value)
          ) !==
          JSON.stringify(
            expectedKeys
          )
        ) {
          return {
            isValid: false,
            identities: [],
            reason
          };
        }

        return {
          isValid: true,
          identities,
          reason: null
        };
      } catch (_error) {
        return {
          isValid: false,
          identities: [],
          reason
        };
      }
    };

    const registryProperty =
      inspectOwnDataProperty(
        source,
        "registryState"
      );

    if (!registryProperty.isPresent) {
      return invalid(
        "persistence_cycle_registry_serialization_registry_state_missing"
      );
    }

    if (!registryProperty.isValid) {
      return invalid(
        "persistence_cycle_registry_serialization_registry_accessor_not_allowed"
      );
    }

    const registryState =
      registryProperty.value;

    if (
      !registryState ||
      typeof registryState !== "object" ||
      Array.isArray(registryState)
    ) {
      return invalid(
        "persistence_cycle_registry_serialization_registry_state_invalid"
      );
    }

    const requiredFieldNames = [
      "status",
      "isValid",
      "isSnapshotPersistenceCycleRegistryMapperOnly",
      "isLiveCall",
      "canUseRegistry",
      "canRegisterMoreCycleIdentities",
      "wasUpdated",
      "wasDuplicateIgnored",
      "isCanonicalOrder",
      "canExecuteStorage",
      "registryVersion",
      "registryIdentity",
      "maximumCompletedCycleIdentities",
      "completedCycleCount",
      "isEmpty",
      "isAtCapacity",
      "updateKind",
      "completedCycleIdentities",
      "registryPayload",
      "reason"
    ];

    const fields = {};

    for (
      let index = 0;
      index < requiredFieldNames.length;
      index += 1
    ) {
      const fieldName =
        requiredFieldNames[index];

      const property =
        inspectOwnDataProperty(
          registryState,
          fieldName
        );

      if (
        !property.isPresent ||
        !property.isValid
      ) {
        return invalid(
          "persistence_cycle_registry_serialization_registry_field_invalid"
        );
      }

      fields[fieldName] =
        property.value;
    }

    if (
      fields.isValid !== true ||
      fields.isSnapshotPersistenceCycleRegistryMapperOnly !==
        true ||
      fields.isLiveCall !== false ||
      fields.canUseRegistry !== true ||
      fields.isCanonicalOrder !== true ||
      fields.canExecuteStorage !== false ||
      fields.registryVersion !== 1 ||
      fields.registryIdentity !==
        "exam_history_persistence_cycle_registry:v1" ||
      fields.maximumCompletedCycleIdentities !==
        maximumCompletedCycleIdentities ||
      fields.reason !== null
    ) {
      return invalid(
        "persistence_cycle_registry_serialization_registry_state_invalid"
      );
    }

    const statusConfig = {
      exam_result_history_persistence_cycle_registry_empty: {
        updateKind: "empty",
        minimumCount: 0,
        maximumCount: 0,
        wasUpdated: false,
        wasDuplicateIgnored: false
      },
      exam_result_history_persistence_cycle_registry_ready: {
        updateKind: "normalized",
        minimumCount: 1,
        maximumCount:
          maximumCompletedCycleIdentities,
        wasUpdated: false,
        wasDuplicateIgnored: false
      },
      exam_result_history_persistence_cycle_registry_updated: {
        updateKind: "registered",
        minimumCount: 1,
        maximumCount:
          maximumCompletedCycleIdentities,
        wasUpdated: true,
        wasDuplicateIgnored: false
      },
      exam_result_history_persistence_cycle_registry_duplicate_unchanged: {
        updateKind:
          "duplicate_unchanged",
        minimumCount: 1,
        maximumCount:
          maximumCompletedCycleIdentities,
        wasUpdated: false,
        wasDuplicateIgnored: true
      }
    };

    const config =
      statusConfig[
        fields.status
      ];

    if (
      !config ||
      fields.updateKind !==
        config.updateKind ||
      fields.wasUpdated !==
        config.wasUpdated ||
      fields.wasDuplicateIgnored !==
        config.wasDuplicateIgnored ||
      !Number.isInteger(
        fields.completedCycleCount
      ) ||
      fields.completedCycleCount <
        config.minimumCount ||
      fields.completedCycleCount >
        config.maximumCount
    ) {
      return invalid(
        "persistence_cycle_registry_serialization_registry_status_invalid"
      );
    }

    const clonedStateIdentities =
      cloneIdentityArray(
        fields.completedCycleIdentities,
        "persistence_cycle_registry_serialization_identities_invalid"
      );

    if (
      !clonedStateIdentities.isValid ||
      clonedStateIdentities.identities.length !==
        fields.completedCycleCount
    ) {
      return invalid(
        clonedStateIdentities.reason ||
          "persistence_cycle_registry_serialization_identities_invalid"
      );
    }

    const isEmpty =
      fields.completedCycleCount === 0;

    const isAtCapacity =
      fields.completedCycleCount ===
      maximumCompletedCycleIdentities;

    if (
      fields.isEmpty !== isEmpty ||
      fields.isAtCapacity !==
        isAtCapacity ||
      fields.canRegisterMoreCycleIdentities !==
        !isAtCapacity
    ) {
      return invalid(
        "persistence_cycle_registry_serialization_registry_flags_invalid"
      );
    }

    const sortedStateIdentities =
      clonedStateIdentities.identities
        .slice()
        .sort();

    if (
      JSON.stringify(
        clonedStateIdentities.identities
      ) !==
      JSON.stringify(
        sortedStateIdentities
      )
    ) {
      return invalid(
        "persistence_cycle_registry_serialization_identity_order_invalid"
      );
    }

    const registryPayload =
      fields.registryPayload;

    if (
      !registryPayload ||
      typeof registryPayload !==
        "object" ||
      Array.isArray(registryPayload)
    ) {
      return invalid(
        "persistence_cycle_registry_serialization_payload_invalid"
      );
    }

    let payloadKeys;

    try {
      payloadKeys =
        Object.keys(
          registryPayload
        );
    } catch (_error) {
      return invalid(
        "persistence_cycle_registry_serialization_payload_invalid"
      );
    }

    if (
      JSON.stringify(payloadKeys) !==
      JSON.stringify([
        "registryVersion",
        "completedCycleIdentities"
      ])
    ) {
      return invalid(
        "persistence_cycle_registry_serialization_payload_invalid"
      );
    }

    const payloadVersionProperty =
      inspectOwnDataProperty(
        registryPayload,
        "registryVersion"
      );

    const payloadIdentitiesProperty =
      inspectOwnDataProperty(
        registryPayload,
        "completedCycleIdentities"
      );

    if (
      !payloadVersionProperty.isPresent ||
      !payloadVersionProperty.isValid ||
      payloadVersionProperty.value !== 1 ||
      !payloadIdentitiesProperty.isPresent ||
      !payloadIdentitiesProperty.isValid
    ) {
      return invalid(
        "persistence_cycle_registry_serialization_payload_invalid"
      );
    }

    const clonedPayloadIdentities =
      cloneIdentityArray(
        payloadIdentitiesProperty.value,
        "persistence_cycle_registry_serialization_payload_invalid"
      );

    if (
      !clonedPayloadIdentities.isValid ||
      JSON.stringify(
        clonedPayloadIdentities.identities
      ) !==
      JSON.stringify(
        clonedStateIdentities.identities
      )
    ) {
      return invalid(
        "persistence_cycle_registry_serialization_payload_mismatch"
      );
    }

    const canonicalRegistryState =
      mapParticipantFullExamResultHistorySnapshotPersistenceCycleRegistryState({
        completedCycleIdentities:
          clonedStateIdentities.identities
      });

    if (
      !canonicalRegistryState.isValid ||
      canonicalRegistryState.canUseRegistry !==
        true ||
      canonicalRegistryState.canExecuteStorage !==
        false ||
      canonicalRegistryState.registryVersion !==
        1 ||
      canonicalRegistryState.registryIdentity !==
        "exam_history_persistence_cycle_registry:v1" ||
      canonicalRegistryState.maximumCompletedCycleIdentities !==
        maximumCompletedCycleIdentities ||
      canonicalRegistryState.completedCycleCount !==
        fields.completedCycleCount ||
      canonicalRegistryState.isEmpty !==
        isEmpty ||
      canonicalRegistryState.isAtCapacity !==
        isAtCapacity ||
      canonicalRegistryState.canRegisterMoreCycleIdentities !==
        !isAtCapacity
    ) {
      return invalid(
        "persistence_cycle_registry_serialization_canonical_state_invalid"
      );
    }

    const canonicalPayload = {
      registryVersion: 1,
      completedCycleIdentities:
        canonicalRegistryState
          .completedCycleIdentities
          .slice()
    };

    if (
      JSON.stringify(
        canonicalRegistryState.registryPayload
      ) !==
        JSON.stringify(
          canonicalPayload
        ) ||
      JSON.stringify(
        canonicalPayload
          .completedCycleIdentities
      ) !==
        JSON.stringify(
          clonedStateIdentities.identities
        )
    ) {
      return invalid(
        "persistence_cycle_registry_serialization_payload_mismatch"
      );
    }

    const serializedJson =
      JSON.stringify(
        canonicalPayload
      );

    const serializedByteLength =
      getParticipantFullExamResultHistorySnapshotUtf8ByteLength(
        serializedJson
      );

    if (
      !Number.isSafeInteger(
        serializedByteLength
      ) ||
      serializedByteLength < 1 ||
      serializedByteLength >
        maximumSerializedBytes
    ) {
      return invalid(
        "persistence_cycle_registry_serialization_size_invalid"
      );
    }

    let parsedPayload;

    try {
      parsedPayload =
        JSON.parse(
          serializedJson
        );
    } catch (_error) {
      return invalid(
        "persistence_cycle_registry_serialization_round_trip_invalid"
      );
    }

    if (
      !parsedPayload ||
      typeof parsedPayload !== "object" ||
      Array.isArray(parsedPayload) ||
      JSON.stringify(
        parsedPayload
      ) !==
        serializedJson
    ) {
      return invalid(
        "persistence_cycle_registry_serialization_round_trip_invalid"
      );
    }

    const roundTripRegistryState =
      mapParticipantFullExamResultHistorySnapshotPersistenceCycleRegistryState({
        completedCycleIdentities:
          parsedPayload.completedCycleIdentities
      });

    if (
      !roundTripRegistryState.isValid ||
      roundTripRegistryState.canUseRegistry !==
        true ||
      roundTripRegistryState.completedCycleCount !==
        fields.completedCycleCount ||
      JSON.stringify(
        roundTripRegistryState.registryPayload
      ) !==
        serializedJson
    ) {
      return invalid(
        "persistence_cycle_registry_serialization_round_trip_invalid"
      );
    }

    return {
      version: "v27.30j",
      status:
        "exam_result_history_persistence_cycle_registry_serialization_ready",
      isValid: true,
      isSnapshotPersistenceCycleRegistrySerializationMapperOnly: true,
      isLiveCall: false,
      canSerializeRegistry: true,
      canPersistLater: true,
      canWriteStorage: false,
      canExecuteStorage: false,
      serializationSchemaVersion,
      maximumSerializedBytes,
      registryVersion: 1,
      registryIdentity:
        "exam_history_persistence_cycle_registry:v1",
      maximumCompletedCycleIdentities,
      completedCycleCount:
        fields.completedCycleCount,
      isEmpty,
      isAtCapacity,
      serializedByteLength,
      serializedJson,
      reason: null
    };
  }

  function mapParticipantFullExamResultHistorySnapshotPersistenceCycleRegistryState(input) {
    const source =
      input &&
      typeof input === "object" &&
      !Array.isArray(input)
        ? input
        : {};

    const registryVersion = 1;
    const maximumCompletedCycleIdentities =
      100;

    const cycleIdentityPrefix =
      "exam_history_persistence_cycle:";

    const inspectOwnDataProperty = (
      target,
      propertyName
    ) => {
      try {
        const descriptor =
          Object.getOwnPropertyDescriptor(
            target,
            propertyName
          );

        if (!descriptor) {
          return {
            isPresent: false,
            isValid: true,
            value: null
          };
        }

        if (
          !Object.prototype.hasOwnProperty.call(
            descriptor,
            "value"
          )
        ) {
          return {
            isPresent: true,
            isValid: false,
            value: null
          };
        }

        return {
          isPresent: true,
          isValid: true,
          value:
            descriptor.value
        };
      } catch (_error) {
        return {
          isPresent: true,
          isValid: false,
          value: null
        };
      }
    };

    const invalid = (reason) => ({
      version: "v27.30i",
      status:
        "exam_result_history_persistence_cycle_registry_invalid",
      isValid: false,
      isSnapshotPersistenceCycleRegistryMapperOnly: true,
      isLiveCall: false,
      canUseRegistry: false,
      canRegisterMoreCycleIdentities: false,
      wasUpdated: false,
      wasDuplicateIgnored: false,
      isCanonicalOrder: false,
      canExecuteStorage: false,
      registryVersion,
      registryIdentity:
        "exam_history_persistence_cycle_registry:v1",
      maximumCompletedCycleIdentities,
      completedCycleCount: 0,
      isEmpty: true,
      isAtCapacity: false,
      updateKind: null,
      completedCycleIdentities: [],
      registryPayload: null,
      reason
    });

    const normalizeCycleIdentities = (
      value,
      invalidReason,
      duplicateReason
    ) => {
      if (
        !Array.isArray(value) ||
        value.length >
          maximumCompletedCycleIdentities
      ) {
        return {
          isValid: false,
          identities: [],
          reason:
            invalidReason
        };
      }

      const identities = [];
      const seenIdentities =
        new Set();

      for (
        let index = 0;
        index < value.length;
        index += 1
      ) {
        const identity =
          value[index];

        if (
          typeof identity !== "string" ||
          identity.length < 40 ||
          identity.length > 256 ||
          identity.trim() !== identity ||
          !identity.startsWith(
            cycleIdentityPrefix
          )
        ) {
          return {
            isValid: false,
            identities: [],
            reason:
              invalidReason
          };
        }

        const remainder =
          identity.slice(
            cycleIdentityPrefix.length
          );

        const operationSeparatorIndex =
          remainder.indexOf(":");

        if (
          operationSeparatorIndex < 1
        ) {
          return {
            isValid: false,
            identities: [],
            reason:
              invalidReason
          };
        }

        const operation =
          remainder.slice(
            0,
            operationSeparatorIndex
          );

        const requestIdentity =
          remainder.slice(
            operationSeparatorIndex + 1
          );

        if (
          operation !== "read" &&
          operation !== "write" &&
          operation !== "delete"
        ) {
          return {
            isValid: false,
            identities: [],
            reason:
              invalidReason
          };
        }

        const requestParts =
          requestIdentity.split(":");

        if (
          requestParts.length !== 4 ||
          requestParts[0] !==
            "exam_history_request"
        ) {
          return {
            isValid: false,
            identities: [],
            reason:
              invalidReason
          };
        }

        const requestSequence =
          Number(requestParts[1]);

        const limit =
          Number(requestParts[2]);

        const offset =
          Number(requestParts[3]);

        if (
          !Number.isSafeInteger(
            requestSequence
          ) ||
          requestSequence < 1 ||
          String(requestSequence) !==
            requestParts[1] ||
          !Number.isInteger(limit) ||
          limit < 1 ||
          limit > 50 ||
          String(limit) !==
            requestParts[2] ||
          !Number.isInteger(offset) ||
          offset < 0 ||
          offset > 10000 ||
          String(offset) !==
            requestParts[3] ||
          offset % limit !== 0
        ) {
          return {
            isValid: false,
            identities: [],
            reason:
              invalidReason
          };
        }

        const expectedIdentity =
          cycleIdentityPrefix +
          operation +
          ":" +
          requestIdentity;

        if (
          identity !==
          expectedIdentity
        ) {
          return {
            isValid: false,
            identities: [],
            reason:
              invalidReason
          };
        }

        if (
          seenIdentities.has(identity)
        ) {
          return {
            isValid: false,
            identities: [],
            reason:
              duplicateReason
          };
        }

        seenIdentities.add(identity);
        identities.push(identity);
      }

      identities.sort();

      return {
        isValid: true,
        identities,
        reason: null
      };
    };

    const completedProperty =
      inspectOwnDataProperty(
        source,
        "completedCycleIdentities"
      );

    const repetitionProperty =
      inspectOwnDataProperty(
        source,
        "repetitionState"
      );

    if (
      !completedProperty.isPresent
    ) {
      return invalid(
        "persistence_cycle_registry_identities_missing"
      );
    }

    if (
      !completedProperty.isValid
    ) {
      return invalid(
        "persistence_cycle_registry_identities_accessor_not_allowed"
      );
    }

    if (
      !repetitionProperty.isValid
    ) {
      return invalid(
        "persistence_cycle_registry_repetition_accessor_not_allowed"
      );
    }

    const normalizedSource =
      normalizeCycleIdentities(
        completedProperty.value,
        "persistence_cycle_registry_identity_invalid",
        "persistence_cycle_registry_duplicate"
      );

    if (!normalizedSource.isValid) {
      return invalid(
        normalizedSource.reason
      );
    }

    let selectedIdentities =
      normalizedSource.identities.slice();

    let status =
      selectedIdentities.length === 0
        ? "exam_result_history_persistence_cycle_registry_empty"
        : "exam_result_history_persistence_cycle_registry_ready";

    let updateKind =
      selectedIdentities.length === 0
        ? "empty"
        : "normalized";

    let wasUpdated = false;
    let wasDuplicateIgnored = false;

    if (
      repetitionProperty.isPresent &&
      repetitionProperty.value !== null &&
      repetitionProperty.value !==
        undefined
    ) {
      const repetitionState =
        repetitionProperty.value;

      if (
        !repetitionState ||
        typeof repetitionState !==
          "object" ||
        Array.isArray(repetitionState) ||
        repetitionState.isSnapshotPersistenceCycleRepetitionGuardOnly !==
          true ||
        repetitionState.isValid !== true ||
        repetitionState.canExecuteStorage !==
          false ||
        repetitionState.maximumCompletedCycleIdentities !==
          maximumCompletedCycleIdentities ||
        !Number.isInteger(
          repetitionState.completedCycleCount
        ) ||
        !Number.isInteger(
          repetitionState.nextCompletedCycleCount
        ) ||
        typeof repetitionState.cycleIdentity !==
          "string"
      ) {
        return invalid(
          "persistence_cycle_registry_repetition_state_invalid"
        );
      }

      const normalizedRepetitionCompleted =
        normalizeCycleIdentities(
          repetitionState.completedCycleIdentities,
          "persistence_cycle_registry_repetition_completed_invalid",
          "persistence_cycle_registry_repetition_completed_duplicate"
        );

      const normalizedRepetitionNext =
        normalizeCycleIdentities(
          repetitionState.nextCompletedCycleIdentities,
          "persistence_cycle_registry_repetition_next_invalid",
          "persistence_cycle_registry_repetition_next_duplicate"
        );

      if (
        !normalizedRepetitionCompleted.isValid
      ) {
        return invalid(
          normalizedRepetitionCompleted.reason
        );
      }

      if (
        !normalizedRepetitionNext.isValid
      ) {
        return invalid(
          normalizedRepetitionNext.reason
        );
      }

      if (
        repetitionState.completedCycleCount !==
          normalizedRepetitionCompleted.identities.length ||
        repetitionState.nextCompletedCycleCount !==
          normalizedRepetitionNext.identities.length ||
        JSON.stringify(
          normalizedSource.identities
        ) !==
          JSON.stringify(
            normalizedRepetitionCompleted.identities
          )
      ) {
        return invalid(
          "persistence_cycle_registry_repetition_source_mismatch"
        );
      }

      const isReadyRepetition =
        repetitionState.status ===
          "exam_result_history_persistence_cycle_repetition_ready" &&
        repetitionState.canAcceptCycleOnce ===
          true &&
        repetitionState.canRegisterCycleIdentityLater ===
          true &&
        repetitionState.isDuplicateCycle ===
          false &&
        repetitionState.reason === null;

      const isBlockedDuplicate =
        repetitionState.status ===
          "exam_result_history_persistence_cycle_repetition_blocked" &&
        repetitionState.canAcceptCycleOnce ===
          false &&
        repetitionState.canRegisterCycleIdentityLater ===
          false &&
        repetitionState.isDuplicateCycle ===
          true &&
        repetitionState.reason ===
          "persistence_cycle_repetition_already_completed";

      if (
        !isReadyRepetition &&
        !isBlockedDuplicate
      ) {
        return invalid(
          "persistence_cycle_registry_repetition_state_invalid"
        );
      }

      if (isReadyRepetition) {
        if (
          normalizedRepetitionNext.identities.length !==
            normalizedRepetitionCompleted.identities.length +
              1 ||
          normalizedRepetitionCompleted.identities.includes(
            repetitionState.cycleIdentity
          ) ||
          !normalizedRepetitionNext.identities.includes(
            repetitionState.cycleIdentity
          )
        ) {
          return invalid(
            "persistence_cycle_registry_repetition_update_invalid"
          );
        }

        selectedIdentities =
          normalizedRepetitionNext.identities.slice();

        status =
          "exam_result_history_persistence_cycle_registry_updated";

        updateKind =
          "registered";

        wasUpdated = true;
      } else {
        if (
          JSON.stringify(
            normalizedRepetitionCompleted.identities
          ) !==
            JSON.stringify(
              normalizedRepetitionNext.identities
            ) ||
          !normalizedRepetitionCompleted.identities.includes(
            repetitionState.cycleIdentity
          )
        ) {
          return invalid(
            "persistence_cycle_registry_duplicate_state_invalid"
          );
        }

        selectedIdentities =
          normalizedRepetitionCompleted.identities.slice();

        status =
          "exam_result_history_persistence_cycle_registry_duplicate_unchanged";

        updateKind =
          "duplicate_unchanged";

        wasDuplicateIgnored = true;
      }
    }

    const isEmpty =
      selectedIdentities.length === 0;

    const isAtCapacity =
      selectedIdentities.length ===
      maximumCompletedCycleIdentities;

    const completedCycleIdentities =
      selectedIdentities.slice();

    const registryPayload = {
      registryVersion,
      completedCycleIdentities:
        completedCycleIdentities.slice()
    };

    return {
      version: "v27.30i",
      status,
      isValid: true,
      isSnapshotPersistenceCycleRegistryMapperOnly: true,
      isLiveCall: false,
      canUseRegistry: true,
      canRegisterMoreCycleIdentities:
        !isAtCapacity,
      wasUpdated,
      wasDuplicateIgnored,
      isCanonicalOrder: true,
      canExecuteStorage: false,
      registryVersion,
      registryIdentity:
        "exam_history_persistence_cycle_registry:v1",
      maximumCompletedCycleIdentities,
      completedCycleCount:
        completedCycleIdentities.length,
      isEmpty,
      isAtCapacity,
      updateKind,
      completedCycleIdentities,
      registryPayload,
      reason: null
    };
  }

  function guardParticipantFullExamResultHistorySnapshotPersistenceCycleRepetition(input) {
    const source =
      input &&
      typeof input === "object" &&
      !Array.isArray(input)
        ? input
        : {};

    const maximumCompletedCycleIdentities =
      100;

    const inspectOwnDataProperty = (
      target,
      propertyName
    ) => {
      try {
        const descriptor =
          Object.getOwnPropertyDescriptor(
            target,
            propertyName
          );

        if (
          !descriptor ||
          !Object.prototype.hasOwnProperty.call(
            descriptor,
            "value"
          )
        ) {
          return {
            isValid: false,
            value: null
          };
        }

        return {
          isValid: true,
          value:
            descriptor.value
        };
      } catch (_error) {
        return {
          isValid: false,
          value: null
        };
      }
    };

    const createState = ({
      status,
      isValid,
      canAcceptCycleOnce,
      canRegisterCycleIdentityLater,
      isDuplicateCycle,
      cycleState = null,
      completedCycleIdentities = [],
      nextCompletedCycleIdentities = [],
      reason
    }) => ({
      version: "v27.30h",
      status,
      isValid,
      isSnapshotPersistenceCycleRepetitionGuardOnly: true,
      isLiveCall: false,
      canAcceptCycleOnce,
      canRegisterCycleIdentityLater,
      isDuplicateCycle,
      canExecuteStorage: false,
      maximumCompletedCycleIdentities,
      completedCycleCount:
        completedCycleIdentities.length,
      nextCompletedCycleCount:
        nextCompletedCycleIdentities.length,
      operation:
        cycleState
          ? cycleState.operation
          : null,
      methodName:
        cycleState
          ? cycleState.methodName
          : null,
      storageKey:
        cycleState
          ? cycleState.storageKey
          : null,
      requestIdentity:
        cycleState
          ? cycleState.requestIdentity
          : null,
      cycleIdentity:
        cycleState
          ? cycleState.cycleIdentity
          : null,
      terminalOutcome:
        cycleState
          ? cycleState.terminalOutcome
          : null,
      completedCycleIdentities,
      nextCompletedCycleIdentities,
      reason
    });

    const invalid = (reason) =>
      createState({
        status:
          "exam_result_history_persistence_cycle_repetition_invalid",
        isValid: false,
        canAcceptCycleOnce: false,
        canRegisterCycleIdentityLater: false,
        isDuplicateCycle: false,
        reason
      });

    const cycleProperty =
      inspectOwnDataProperty(
        source,
        "cycleState"
      );

    const identitiesProperty =
      inspectOwnDataProperty(
        source,
        "completedCycleIdentities"
      );

    if (!cycleProperty.isValid) {
      return invalid(
        "persistence_cycle_repetition_cycle_state_missing"
      );
    }

    if (!identitiesProperty.isValid) {
      return invalid(
        "persistence_cycle_repetition_registry_missing"
      );
    }

    const cycleState =
      cycleProperty.value;

    const registryInput =
      identitiesProperty.value;

    if (
      !cycleState ||
      typeof cycleState !== "object" ||
      Array.isArray(cycleState) ||
      cycleState.isSnapshotPersistenceCycleMapperOnly !==
        true ||
      cycleState.isValid !== true ||
      cycleState.status !==
        "exam_result_history_persistence_cycle_completed" ||
      cycleState.canFinalizeCycle !== true ||
      cycleState.isTerminal !== true ||
      cycleState.isSuccessful !== true ||
      cycleState.canExecuteStorage !== false ||
      cycleState.cycleSchemaVersion !== 1
    ) {
      return invalid(
        "persistence_cycle_repetition_cycle_state_invalid"
      );
    }

    if (
      !Array.isArray(registryInput) ||
      registryInput.length >
        maximumCompletedCycleIdentities
    ) {
      return invalid(
        "persistence_cycle_repetition_registry_invalid"
      );
    }

    const completedCycleIdentities = [];
    const seenCycleIdentities =
      new Set();

    for (
      let index = 0;
      index < registryInput.length;
      index += 1
    ) {
      const identity =
        registryInput[index];

      if (
        typeof identity !== "string" ||
        identity.length < 20 ||
        identity.length > 256 ||
        identity.trim() !== identity ||
        !identity.startsWith(
          "exam_history_persistence_cycle:"
        )
      ) {
        return invalid(
          "persistence_cycle_repetition_registry_identity_invalid"
        );
      }

      if (
        seenCycleIdentities.has(identity)
      ) {
        return invalid(
          "persistence_cycle_repetition_registry_duplicate"
        );
      }

      seenCycleIdentities.add(identity);
      completedCycleIdentities.push(
        identity
      );
    }

    const operationConfig = {
      read: {
        methodName: "read",
        outcomes: {
          read_ready: {
            resultStatus:
              "exam_result_history_persistence_result_read_ready",
            completionStatus:
              "exam_result_history_persistence_completion_read_ready"
          },
          read_empty: {
            resultStatus:
              "exam_result_history_persistence_result_read_empty",
            completionStatus:
              "exam_result_history_persistence_completion_read_empty"
          }
        }
      },
      write: {
        methodName: "write",
        outcomes: {
          write_confirmed: {
            resultStatus:
              "exam_result_history_persistence_result_write_confirmed",
            completionStatus:
              "exam_result_history_persistence_completion_write_confirmed"
          }
        }
      },
      delete: {
        methodName: "delete",
        outcomes: {
          delete_confirmed: {
            resultStatus:
              "exam_result_history_persistence_result_delete_confirmed",
            completionStatus:
              "exam_result_history_persistence_completion_delete_confirmed"
          },
          delete_absent: {
            resultStatus:
              "exam_result_history_persistence_result_delete_absent",
            completionStatus:
              "exam_result_history_persistence_completion_delete_absent"
          }
        }
      }
    };

    const operationState =
      operationConfig[
        cycleState.operation
      ];

    const outcomeState =
      operationState &&
      operationState.outcomes[
        cycleState.terminalOutcome
      ];

    if (
      !operationState ||
      !outcomeState ||
      cycleState.methodName !==
        operationState.methodName ||
      cycleState.resultStatus !==
        outcomeState.resultStatus ||
      cycleState.completionStatus !==
        outcomeState.completionStatus ||
      cycleState.acceptanceStatus !==
        "exam_result_history_persistence_result_acceptance_ready"
    ) {
      return invalid(
        "persistence_cycle_repetition_outcome_invalid"
      );
    }

    const canonicalKeyState =
      mapParticipantFullExamResultHistorySnapshotPersistenceContract({
        intent: "delete",
        storageKey:
          cycleState.storageKey
      });

    if (
      !canonicalKeyState.isValid ||
      canonicalKeyState.canPrepareDelete !==
        true ||
      canonicalKeyState.storageKey !==
        cycleState.storageKey ||
      canonicalKeyState.requestIdentity !==
        cycleState.requestIdentity
    ) {
      return invalid(
        "persistence_cycle_repetition_storage_key_invalid"
      );
    }

    const expectedInvocationIdentity =
      "exam_history_persistence_invocation:" +
      cycleState.operation +
      ":" +
      canonicalKeyState.requestIdentity;

    const expectedPackageIdentity =
      "exam_history_persistence_invocation_package:" +
      cycleState.operation +
      ":" +
      canonicalKeyState.requestIdentity;

    const expectedCompletionIdentity =
      "exam_history_persistence_completion:" +
      cycleState.operation +
      ":" +
      canonicalKeyState.requestIdentity;

    const expectedCycleIdentity =
      "exam_history_persistence_cycle:" +
      cycleState.operation +
      ":" +
      canonicalKeyState.requestIdentity;

    if (
      cycleState.invocationIdentity !==
        expectedInvocationIdentity ||
      cycleState.invocationPackageIdentity !==
        expectedPackageIdentity ||
      cycleState.completionIdentity !==
        expectedCompletionIdentity ||
      cycleState.cycleIdentity !==
        expectedCycleIdentity
    ) {
      return invalid(
        "persistence_cycle_repetition_identity_invalid"
      );
    }

    if (
      cycleState.terminalOutcome ===
        "read_ready"
    ) {
      if (
        cycleState.didRead !== true ||
        cycleState.didWrite !== false ||
        cycleState.didDelete !== false ||
        cycleState.wasAlreadyAbsent !==
          false ||
        cycleState.isEmpty !== false ||
        cycleState.canResumeSnapshot !==
          true ||
        !Number.isSafeInteger(
          cycleState.serializedByteLength
        ) ||
        cycleState.serializedByteLength < 1 ||
        cycleState.serializedByteLength >
          4096 ||
        !cycleState.snapshotPayload ||
        typeof cycleState.snapshotPayload !==
          "object" ||
        Array.isArray(
          cycleState.snapshotPayload
        ) ||
        !cycleState.resumeState ||
        typeof cycleState.resumeState !==
          "object" ||
        Array.isArray(
          cycleState.resumeState
        )
      ) {
        return invalid(
          "persistence_cycle_repetition_read_ready_invalid"
        );
      }

      const normalizedSnapshot =
        normalizeParticipantFullExamResultHistoryControllerSnapshot(
          cycleState.snapshotPayload
        );

      const recomputedResumeState =
        mapParticipantFullExamResultHistorySnapshotResumeState({
          snapshot:
            cycleState.snapshotPayload
        });

      if (
        !normalizedSnapshot.isValid ||
        normalizedSnapshot.canResume !==
          true ||
        normalizedSnapshot.requestIdentity !==
          canonicalKeyState.requestIdentity ||
        !recomputedResumeState.isValid ||
        recomputedResumeState.canResume !==
          true ||
        recomputedResumeState.requestIdentity !==
          canonicalKeyState.requestIdentity ||
        JSON.stringify(
          recomputedResumeState
        ) !==
          JSON.stringify(
            cycleState.resumeState
          )
      ) {
        return invalid(
          "persistence_cycle_repetition_read_snapshot_invalid"
        );
      }
    } else if (
      cycleState.terminalOutcome ===
        "read_empty"
    ) {
      if (
        cycleState.didRead !== true ||
        cycleState.didWrite !== false ||
        cycleState.didDelete !== false ||
        cycleState.wasAlreadyAbsent !==
          false ||
        cycleState.isEmpty !== true ||
        cycleState.canResumeSnapshot !==
          false ||
        cycleState.serializedByteLength !==
          null ||
        cycleState.snapshotPayload !==
          null ||
        cycleState.resumeState !== null
      ) {
        return invalid(
          "persistence_cycle_repetition_read_empty_invalid"
        );
      }
    } else if (
      cycleState.terminalOutcome ===
        "write_confirmed"
    ) {
      if (
        cycleState.didRead !== false ||
        cycleState.didWrite !== true ||
        cycleState.didDelete !== false ||
        cycleState.wasAlreadyAbsent !==
          false ||
        cycleState.isEmpty !== false ||
        cycleState.canResumeSnapshot !==
          false ||
        !Number.isSafeInteger(
          cycleState.serializedByteLength
        ) ||
        cycleState.serializedByteLength < 1 ||
        cycleState.serializedByteLength >
          4096 ||
        cycleState.snapshotPayload !==
          null ||
        cycleState.resumeState !== null
      ) {
        return invalid(
          "persistence_cycle_repetition_write_invalid"
        );
      }
    } else {
      const isConfirmed =
        cycleState.terminalOutcome ===
          "delete_confirmed";

      if (
        cycleState.didRead !== false ||
        cycleState.didWrite !== false ||
        cycleState.canResumeSnapshot !==
          false ||
        cycleState.serializedByteLength !==
          null ||
        cycleState.snapshotPayload !==
          null ||
        cycleState.resumeState !== null ||
        (
          isConfirmed &&
          (
            cycleState.didDelete !== true ||
            cycleState.wasAlreadyAbsent !==
              false ||
            cycleState.isEmpty !== false
          )
        ) ||
        (
          !isConfirmed &&
          (
            cycleState.didDelete !== false ||
            cycleState.wasAlreadyAbsent !==
              true ||
            cycleState.isEmpty !== true
          )
        )
      ) {
        return invalid(
          "persistence_cycle_repetition_delete_invalid"
        );
      }
    }

    const isDuplicateCycle =
      seenCycleIdentities.has(
        expectedCycleIdentity
      );

    if (isDuplicateCycle) {
      return createState({
        status:
          "exam_result_history_persistence_cycle_repetition_blocked",
        isValid: true,
        canAcceptCycleOnce: false,
        canRegisterCycleIdentityLater: false,
        isDuplicateCycle: true,
        cycleState,
        completedCycleIdentities,
        nextCompletedCycleIdentities:
          completedCycleIdentities.slice(),
        reason:
          "persistence_cycle_repetition_already_completed"
      });
    }

    if (
      completedCycleIdentities.length >=
      maximumCompletedCycleIdentities
    ) {
      return invalid(
        "persistence_cycle_repetition_registry_limit_reached"
      );
    }

    const nextCompletedCycleIdentities =
      completedCycleIdentities.slice();

    nextCompletedCycleIdentities.push(
      expectedCycleIdentity
    );

    return createState({
      status:
        "exam_result_history_persistence_cycle_repetition_ready",
      isValid: true,
      canAcceptCycleOnce: true,
      canRegisterCycleIdentityLater: true,
      isDuplicateCycle: false,
      cycleState,
      completedCycleIdentities,
      nextCompletedCycleIdentities,
      reason: null
    });
  }

  function mapParticipantFullExamResultHistorySnapshotPersistenceCycleState(input) {
    const source =
      input &&
      typeof input === "object" &&
      !Array.isArray(input)
        ? input
        : {};

    const inspectOwnDataProperty = (
      target,
      propertyName
    ) => {
      try {
        const descriptor =
          Object.getOwnPropertyDescriptor(
            target,
            propertyName
          );

        if (
          !descriptor ||
          !Object.prototype.hasOwnProperty.call(
            descriptor,
            "value"
          )
        ) {
          return {
            isValid: false,
            value: null
          };
        }

        return {
          isValid: true,
          value:
            descriptor.value
        };
      } catch (_error) {
        return {
          isValid: false,
          value: null
        };
      }
    };

    const invalid = (reason) => ({
      version: "v27.30g",
      status:
        "exam_result_history_persistence_cycle_invalid",
      isValid: false,
      isSnapshotPersistenceCycleMapperOnly: true,
      isLiveCall: false,
      canFinalizeCycle: false,
      isTerminal: false,
      isSuccessful: false,
      canResumeSnapshot: false,
      canExecuteStorage: false,
      cycleSchemaVersion: 1,
      operation: null,
      methodName: null,
      storageKey: null,
      requestIdentity: null,
      invocationIdentity: null,
      invocationPackageIdentity: null,
      resultStatus: null,
      acceptanceStatus: null,
      completionStatus: null,
      completionIdentity: null,
      cycleIdentity: null,
      terminalOutcome: null,
      didRead: false,
      didWrite: false,
      didDelete: false,
      wasAlreadyAbsent: false,
      isEmpty: false,
      serializedByteLength: null,
      snapshotPayload: null,
      resumeState: null,
      reason
    });

    const packageProperty =
      inspectOwnDataProperty(
        source,
        "invocationPackageState"
      );

    const resultProperty =
      inspectOwnDataProperty(
        source,
        "resultContractState"
      );

    const acceptanceProperty =
      inspectOwnDataProperty(
        source,
        "acceptanceState"
      );

    const completionProperty =
      inspectOwnDataProperty(
        source,
        "completionState"
      );

    if (!packageProperty.isValid) {
      return invalid(
        "persistence_cycle_invocation_package_missing"
      );
    }

    if (!resultProperty.isValid) {
      return invalid(
        "persistence_cycle_result_contract_missing"
      );
    }

    if (!acceptanceProperty.isValid) {
      return invalid(
        "persistence_cycle_acceptance_state_missing"
      );
    }

    if (!completionProperty.isValid) {
      return invalid(
        "persistence_cycle_completion_state_missing"
      );
    }

    const invocationPackageState =
      packageProperty.value;

    const resultContractState =
      resultProperty.value;

    const acceptanceState =
      acceptanceProperty.value;

    const completionState =
      completionProperty.value;

    if (
      !invocationPackageState ||
      typeof invocationPackageState !==
        "object" ||
      Array.isArray(
        invocationPackageState
      ) ||
      invocationPackageState.isSnapshotPersistenceInvocationPackageOnly !==
        true ||
      invocationPackageState.isValid !== true ||
      invocationPackageState.status !==
        "exam_result_history_persistence_invocation_package_ready" ||
      invocationPackageState.canPrepareInvocationPackage !==
        true ||
      invocationPackageState.canInvokeLater !==
        true ||
      invocationPackageState.canExecuteStorage !==
        false ||
      invocationPackageState.isMethodReferenceValidated !==
        true ||
      invocationPackageState.invocationPackageSchemaVersion !==
        1
    ) {
      return invalid(
        "persistence_cycle_invocation_package_invalid"
      );
    }

    if (
      !resultContractState ||
      typeof resultContractState !==
        "object" ||
      Array.isArray(
        resultContractState
      ) ||
      resultContractState.isSnapshotPersistenceResultContractOnly !==
        true ||
      resultContractState.isValid !== true ||
      resultContractState.canAcceptResult !==
        true ||
      resultContractState.canExecuteStorage !==
        false ||
      resultContractState.resultSchemaVersion !==
        1 ||
      resultContractState.maximumResultBytes !==
        4096
    ) {
      return invalid(
        "persistence_cycle_result_contract_invalid"
      );
    }

    if (
      !acceptanceState ||
      typeof acceptanceState !== "object" ||
      Array.isArray(acceptanceState) ||
      acceptanceState.isSnapshotPersistenceResultAcceptanceGuardOnly !==
        true ||
      acceptanceState.isValid !== true ||
      acceptanceState.status !==
        "exam_result_history_persistence_result_acceptance_ready" ||
      acceptanceState.canApplyResult !==
        true ||
      acceptanceState.didAcceptResult !==
        true ||
      acceptanceState.isStaleResult !==
        false ||
      acceptanceState.canExecuteStorage !==
        false
    ) {
      return invalid(
        "persistence_cycle_acceptance_state_invalid"
      );
    }

    if (
      !completionState ||
      typeof completionState !== "object" ||
      Array.isArray(completionState) ||
      completionState.isSnapshotPersistenceCompletionMapperOnly !==
        true ||
      completionState.isValid !== true ||
      completionState.canFinalizePersistence !==
        true ||
      completionState.isTerminal !== true ||
      completionState.isSuccessful !==
        true ||
      completionState.canExecuteStorage !==
        false
    ) {
      return invalid(
        "persistence_cycle_completion_state_invalid"
      );
    }

    const recomputedAcceptance =
      guardParticipantFullExamResultHistorySnapshotPersistenceResultAcceptance({
        activeInvocationPackageState:
          invocationPackageState,
        resultContractState
      });

    if (
      !recomputedAcceptance.isValid ||
      recomputedAcceptance.status !==
        "exam_result_history_persistence_result_acceptance_ready" ||
      recomputedAcceptance.canApplyResult !==
        true ||
      recomputedAcceptance.didAcceptResult !==
        true ||
      recomputedAcceptance.isStaleResult !==
        false ||
      recomputedAcceptance.canExecuteStorage !==
        false
    ) {
      return invalid(
        "persistence_cycle_recomputed_acceptance_not_ready"
      );
    }

    if (
      JSON.stringify(
        recomputedAcceptance
      ) !==
      JSON.stringify(
        acceptanceState
      )
    ) {
      return invalid(
        "persistence_cycle_acceptance_state_mismatch"
      );
    }

    const recomputedCompletion =
      mapParticipantFullExamResultHistorySnapshotPersistenceCompletionState({
        acceptanceState:
          recomputedAcceptance
      });

    if (
      !recomputedCompletion.isValid ||
      recomputedCompletion.canFinalizePersistence !==
        true ||
      recomputedCompletion.isTerminal !==
        true ||
      recomputedCompletion.isSuccessful !==
        true ||
      recomputedCompletion.canExecuteStorage !==
        false
    ) {
      return invalid(
        "persistence_cycle_recomputed_completion_invalid"
      );
    }

    if (
      JSON.stringify(
        recomputedCompletion
      ) !==
      JSON.stringify(
        completionState
      )
    ) {
      return invalid(
        "persistence_cycle_completion_state_mismatch"
      );
    }

    if (
      recomputedCompletion.operation !==
        invocationPackageState.operation ||
      recomputedCompletion.methodName !==
        invocationPackageState.methodName ||
      recomputedCompletion.storageKey !==
        invocationPackageState.storageKey ||
      recomputedCompletion.requestIdentity !==
        invocationPackageState.requestIdentity ||
      recomputedCompletion.invocationIdentity !==
        invocationPackageState.invocationIdentity ||
      recomputedCompletion.activeInvocationPackageIdentity !==
        invocationPackageState.invocationPackageIdentity ||
      recomputedCompletion.resultInvocationPackageIdentity !==
        invocationPackageState.invocationPackageIdentity ||
      recomputedCompletion.resultStatus !==
        resultContractState.status
    ) {
      return invalid(
        "persistence_cycle_identity_mismatch"
      );
    }

    const cycleIdentity =
      "exam_history_persistence_cycle:" +
      recomputedCompletion.operation +
      ":" +
      recomputedCompletion.requestIdentity;

    return {
      version: "v27.30g",
      status:
        "exam_result_history_persistence_cycle_completed",
      isValid: true,
      isSnapshotPersistenceCycleMapperOnly: true,
      isLiveCall: false,
      canFinalizeCycle: true,
      isTerminal: true,
      isSuccessful: true,
      canResumeSnapshot:
        recomputedCompletion.canResumeSnapshot ===
          true,
      canExecuteStorage: false,
      cycleSchemaVersion: 1,
      operation:
        recomputedCompletion.operation,
      methodName:
        recomputedCompletion.methodName,
      storageKey:
        recomputedCompletion.storageKey,
      requestIdentity:
        recomputedCompletion.requestIdentity,
      invocationIdentity:
        recomputedCompletion.invocationIdentity,
      invocationPackageIdentity:
        recomputedCompletion.activeInvocationPackageIdentity,
      resultStatus:
        recomputedCompletion.resultStatus,
      acceptanceStatus:
        recomputedAcceptance.status,
      completionStatus:
        recomputedCompletion.status,
      completionIdentity:
        recomputedCompletion.completionIdentity,
      cycleIdentity,
      terminalOutcome:
        recomputedCompletion.terminalOutcome,
      didRead:
        recomputedCompletion.didRead === true,
      didWrite:
        recomputedCompletion.didWrite === true,
      didDelete:
        recomputedCompletion.didDelete === true,
      wasAlreadyAbsent:
        recomputedCompletion.wasAlreadyAbsent ===
          true,
      isEmpty:
        recomputedCompletion.isEmpty === true,
      serializedByteLength:
        recomputedCompletion.serializedByteLength,
      snapshotPayload:
        recomputedCompletion.snapshotPayload,
      resumeState:
        recomputedCompletion.resumeState,
      reason: null
    };
  }

  function mapParticipantFullExamResultHistorySnapshotPersistenceCompletionState(input) {
    const source =
      input &&
      typeof input === "object" &&
      !Array.isArray(input)
        ? input
        : {};

    const acceptanceState =
      source.acceptanceState &&
      typeof source.acceptanceState === "object" &&
      !Array.isArray(source.acceptanceState)
        ? source.acceptanceState
        : null;

    const invalid = (reason) => ({
      version: "v27.30f",
      status:
        "exam_result_history_persistence_completion_invalid",
      isValid: false,
      isSnapshotPersistenceCompletionMapperOnly: true,
      isLiveCall: false,
      canFinalizePersistence: false,
      isTerminal: false,
      isSuccessful: false,
      terminalOutcome: null,
      canResumeSnapshot: false,
      canExecuteStorage: false,
      operation: null,
      methodName: null,
      storageKey: null,
      requestIdentity: null,
      invocationIdentity: null,
      activeInvocationPackageIdentity: null,
      resultInvocationPackageIdentity: null,
      resultStatus: null,
      completionIdentity: null,
      didRead: false,
      didWrite: false,
      didDelete: false,
      wasAlreadyAbsent: false,
      isEmpty: false,
      serializedByteLength: null,
      snapshotPayload: null,
      resumeState: null,
      reason
    });

    if (!acceptanceState) {
      return invalid(
        "persistence_completion_acceptance_state_missing"
      );
    }

    if (
      acceptanceState.isSnapshotPersistenceResultAcceptanceGuardOnly !==
        true ||
      acceptanceState.isValid !== true ||
      acceptanceState.status !==
        "exam_result_history_persistence_result_acceptance_ready" ||
      acceptanceState.canApplyResult !== true ||
      acceptanceState.didAcceptResult !== true ||
      acceptanceState.isStaleResult !== false ||
      acceptanceState.canExecuteStorage !== false
    ) {
      return invalid(
        "persistence_completion_acceptance_state_invalid"
      );
    }

    const operationConfig = {
      read: {
        methodName: "read",
        allowedResultStatuses: [
          "exam_result_history_persistence_result_read_ready",
          "exam_result_history_persistence_result_read_empty"
        ]
      },
      write: {
        methodName: "write",
        allowedResultStatuses: [
          "exam_result_history_persistence_result_write_confirmed"
        ]
      },
      delete: {
        methodName: "delete",
        allowedResultStatuses: [
          "exam_result_history_persistence_result_delete_confirmed",
          "exam_result_history_persistence_result_delete_absent"
        ]
      }
    };

    const config =
      operationConfig[
        acceptanceState.operation
      ];

    if (
      !config ||
      acceptanceState.methodName !==
        config.methodName ||
      !config.allowedResultStatuses.includes(
        acceptanceState.resultStatus
      )
    ) {
      return invalid(
        "persistence_completion_operation_invalid"
      );
    }

    if (
      typeof acceptanceState.activeInvocationPackageIdentity !==
        "string" ||
      typeof acceptanceState.resultInvocationPackageIdentity !==
        "string" ||
      acceptanceState.activeInvocationPackageIdentity !==
        acceptanceState.resultInvocationPackageIdentity
    ) {
      return invalid(
        "persistence_completion_package_identity_invalid"
      );
    }

    const canonicalKeyState =
      mapParticipantFullExamResultHistorySnapshotPersistenceContract({
        intent: "delete",
        storageKey:
          acceptanceState.storageKey
      });

    if (
      !canonicalKeyState.isValid ||
      canonicalKeyState.canPrepareDelete !==
        true ||
      canonicalKeyState.storageKey !==
        acceptanceState.storageKey ||
      canonicalKeyState.requestIdentity !==
        acceptanceState.requestIdentity
    ) {
      return invalid(
        "persistence_completion_storage_key_invalid"
      );
    }

    const expectedPackageIdentity =
      "exam_history_persistence_invocation_package:" +
      acceptanceState.operation +
      ":" +
      canonicalKeyState.requestIdentity;

    const expectedInvocationIdentity =
      "exam_history_persistence_invocation:" +
      acceptanceState.operation +
      ":" +
      canonicalKeyState.requestIdentity;

    if (
      acceptanceState.activeInvocationPackageIdentity !==
        expectedPackageIdentity ||
      acceptanceState.resultInvocationPackageIdentity !==
        expectedPackageIdentity ||
      acceptanceState.invocationIdentity !==
        expectedInvocationIdentity
    ) {
      return invalid(
        "persistence_completion_identity_invalid"
      );
    }

    const completionIdentity =
      "exam_history_persistence_completion:" +
      acceptanceState.operation +
      ":" +
      canonicalKeyState.requestIdentity;

    const completed = (
      status,
      terminalOutcome,
      overrides = {}
    ) => ({
      version: "v27.30f",
      status,
      isValid: true,
      isSnapshotPersistenceCompletionMapperOnly: true,
      isLiveCall: false,
      canFinalizePersistence: true,
      isTerminal: true,
      isSuccessful: true,
      terminalOutcome,
      canResumeSnapshot: false,
      canExecuteStorage: false,
      operation:
        acceptanceState.operation,
      methodName:
        acceptanceState.methodName,
      storageKey:
        canonicalKeyState.storageKey,
      requestIdentity:
        canonicalKeyState.requestIdentity,
      invocationIdentity:
        expectedInvocationIdentity,
      activeInvocationPackageIdentity:
        expectedPackageIdentity,
      resultInvocationPackageIdentity:
        expectedPackageIdentity,
      resultStatus:
        acceptanceState.resultStatus,
      completionIdentity,
      didRead: false,
      didWrite: false,
      didDelete: false,
      wasAlreadyAbsent: false,
      isEmpty: false,
      serializedByteLength: null,
      snapshotPayload: null,
      resumeState: null,
      reason: null,
      ...overrides
    });

    if (acceptanceState.operation === "read") {
      if (
        acceptanceState.resultStatus ===
          "exam_result_history_persistence_result_read_empty"
      ) {
        if (
          acceptanceState.didRead !== true ||
          acceptanceState.didWrite !== false ||
          acceptanceState.didDelete !== false ||
          acceptanceState.wasAlreadyAbsent !==
            false ||
          acceptanceState.isEmpty !== true ||
          acceptanceState.canResumeSnapshot !==
            false ||
          acceptanceState.serializedByteLength !==
            null ||
          acceptanceState.snapshotPayload !==
            null ||
          acceptanceState.resumeState !== null
        ) {
          return invalid(
            "persistence_completion_read_empty_invalid"
          );
        }

        return completed(
          "exam_result_history_persistence_completion_read_empty",
          "read_empty",
          {
            didRead: true,
            isEmpty: true
          }
        );
      }

      if (
        acceptanceState.didRead !== true ||
        acceptanceState.didWrite !== false ||
        acceptanceState.didDelete !== false ||
        acceptanceState.wasAlreadyAbsent !==
          false ||
        acceptanceState.isEmpty !== false ||
        acceptanceState.canResumeSnapshot !==
          true ||
        !Number.isSafeInteger(
          acceptanceState.serializedByteLength
        ) ||
        acceptanceState.serializedByteLength < 1 ||
        acceptanceState.serializedByteLength >
          4096 ||
        !acceptanceState.snapshotPayload ||
        typeof acceptanceState.snapshotPayload !==
          "object" ||
        Array.isArray(
          acceptanceState.snapshotPayload
        ) ||
        !acceptanceState.resumeState ||
        typeof acceptanceState.resumeState !==
          "object" ||
        Array.isArray(
          acceptanceState.resumeState
        )
      ) {
        return invalid(
          "persistence_completion_read_result_invalid"
        );
      }

      const normalizedSnapshot =
        normalizeParticipantFullExamResultHistoryControllerSnapshot(
          acceptanceState.snapshotPayload
        );

      const recomputedResumeState =
        mapParticipantFullExamResultHistorySnapshotResumeState({
          snapshot:
            acceptanceState.snapshotPayload
        });

      if (
        !normalizedSnapshot.isValid ||
        normalizedSnapshot.canResume !==
          true ||
        normalizedSnapshot.requestIdentity !==
          canonicalKeyState.requestIdentity ||
        !recomputedResumeState.isValid ||
        recomputedResumeState.canResume !==
          true ||
        recomputedResumeState.requestIdentity !==
          canonicalKeyState.requestIdentity ||
        JSON.stringify(
          recomputedResumeState
        ) !==
          JSON.stringify(
            acceptanceState.resumeState
          )
      ) {
        return invalid(
          "persistence_completion_read_snapshot_invalid"
        );
      }

      return completed(
        "exam_result_history_persistence_completion_read_ready",
        "read_ready",
        {
          canResumeSnapshot: true,
          didRead: true,
          serializedByteLength:
            acceptanceState.serializedByteLength,
          snapshotPayload:
            acceptanceState.snapshotPayload,
          resumeState:
            recomputedResumeState
        }
      );
    }

    if (acceptanceState.operation === "write") {
      if (
        acceptanceState.didRead !== false ||
        acceptanceState.didWrite !== true ||
        acceptanceState.didDelete !== false ||
        acceptanceState.wasAlreadyAbsent !==
          false ||
        acceptanceState.isEmpty !== false ||
        acceptanceState.canResumeSnapshot !==
          false ||
        !Number.isSafeInteger(
          acceptanceState.serializedByteLength
        ) ||
        acceptanceState.serializedByteLength < 1 ||
        acceptanceState.serializedByteLength >
          4096 ||
        acceptanceState.snapshotPayload !==
          null ||
        acceptanceState.resumeState !== null
      ) {
        return invalid(
          "persistence_completion_write_result_invalid"
        );
      }

      return completed(
        "exam_result_history_persistence_completion_write_confirmed",
        "write_confirmed",
        {
          didWrite: true,
          serializedByteLength:
            acceptanceState.serializedByteLength
        }
      );
    }

    if (
      acceptanceState.didRead !== false ||
      acceptanceState.didWrite !== false ||
      acceptanceState.canResumeSnapshot !==
        false ||
      acceptanceState.serializedByteLength !==
        null ||
      acceptanceState.snapshotPayload !==
        null ||
      acceptanceState.resumeState !== null
    ) {
      return invalid(
        "persistence_completion_delete_result_invalid"
      );
    }

    if (
      acceptanceState.resultStatus ===
        "exam_result_history_persistence_result_delete_confirmed"
    ) {
      if (
        acceptanceState.didDelete !== true ||
        acceptanceState.wasAlreadyAbsent !==
          false ||
        acceptanceState.isEmpty !== false
      ) {
        return invalid(
          "persistence_completion_delete_result_invalid"
        );
      }

      return completed(
        "exam_result_history_persistence_completion_delete_confirmed",
        "delete_confirmed",
        {
          didDelete: true
        }
      );
    }

    if (
      acceptanceState.didDelete !== false ||
      acceptanceState.wasAlreadyAbsent !==
        true ||
      acceptanceState.isEmpty !== true
    ) {
      return invalid(
        "persistence_completion_delete_result_invalid"
      );
    }

    return completed(
      "exam_result_history_persistence_completion_delete_absent",
      "delete_absent",
      {
        wasAlreadyAbsent: true,
        isEmpty: true
      }
    );
  }

  function guardParticipantFullExamResultHistorySnapshotPersistenceResultAcceptance(input) {
    const source =
      input &&
      typeof input === "object" &&
      !Array.isArray(input)
        ? input
        : {};

    const inspectOwnDataProperty = (
      target,
      propertyName
    ) => {
      try {
        const descriptor =
          Object.getOwnPropertyDescriptor(
            target,
            propertyName
          );

        if (
          !descriptor ||
          !Object.prototype.hasOwnProperty.call(
            descriptor,
            "value"
          )
        ) {
          return {
            isValid: false,
            value: null
          };
        }

        return {
          isValid: true,
          value:
            descriptor.value
        };
      } catch (_error) {
        return {
          isValid: false,
          value: null
        };
      }
    };

    const invalid = (reason) => ({
      version: "v27.30e",
      status:
        "exam_result_history_persistence_result_acceptance_invalid",
      isValid: false,
      isSnapshotPersistenceResultAcceptanceGuardOnly: true,
      isLiveCall: false,
      canApplyResult: false,
      didAcceptResult: false,
      isStaleResult: false,
      canResumeSnapshot: false,
      canExecuteStorage: false,
      activeInvocationPackageIdentity: null,
      resultInvocationPackageIdentity: null,
      resultStatus: null,
      operation: null,
      methodName: null,
      storageKey: null,
      requestIdentity: null,
      invocationIdentity: null,
      didRead: false,
      didWrite: false,
      didDelete: false,
      wasAlreadyAbsent: false,
      isEmpty: false,
      serializedByteLength: null,
      snapshotPayload: null,
      resumeState: null,
      reason
    });

    const packageProperty =
      inspectOwnDataProperty(
        source,
        "activeInvocationPackageState"
      );

    const resultProperty =
      inspectOwnDataProperty(
        source,
        "resultContractState"
      );

    if (!packageProperty.isValid) {
      return invalid(
        "persistence_result_acceptance_active_package_missing"
      );
    }

    if (!resultProperty.isValid) {
      return invalid(
        "persistence_result_acceptance_result_state_missing"
      );
    }

    const activePackage =
      packageProperty.value;

    const resultState =
      resultProperty.value;

    if (
      !activePackage ||
      typeof activePackage !== "object" ||
      Array.isArray(activePackage) ||
      activePackage.isSnapshotPersistenceInvocationPackageOnly !==
        true ||
      activePackage.isValid !== true ||
      activePackage.status !==
        "exam_result_history_persistence_invocation_package_ready" ||
      activePackage.canPrepareInvocationPackage !==
        true ||
      activePackage.canInvokeLater !== true ||
      activePackage.canExecuteStorage !== false ||
      activePackage.isMethodReferenceValidated !==
        true ||
      activePackage.invocationPackageSchemaVersion !==
        1
    ) {
      return invalid(
        "persistence_result_acceptance_active_package_invalid"
      );
    }

    const operationConfig = {
      read: {
        methodName: "read",
        requiredCapability: "read",
        argumentNames: [
          "storageKey"
        ],
        hasValidatedLoadState: true
      },
      write: {
        methodName: "write",
        requiredCapability: "write",
        argumentNames: [
          "storageKey",
          "serializedJson"
        ],
        hasValidatedLoadState: false
      },
      delete: {
        methodName: "delete",
        requiredCapability: "delete",
        argumentNames: [
          "storageKey"
        ],
        hasValidatedLoadState: false
      }
    };

    const config =
      operationConfig[
        activePackage.operation
      ];

    if (
      !config ||
      activePackage.methodName !==
        config.methodName ||
      activePackage.requiredCapability !==
        config.requiredCapability ||
      activePackage.hasValidatedLoadState !==
        config.hasValidatedLoadState
    ) {
      return invalid(
        "persistence_result_acceptance_active_operation_invalid"
      );
    }

    if (
      typeof activePackage.adapterReadinessFingerprint !==
        "string" ||
      activePackage.adapterReadinessFingerprint.length <
        10 ||
      typeof activePackage.invocationPackageIdentity !==
        "string"
    ) {
      return invalid(
        "persistence_result_acceptance_active_identity_invalid"
      );
    }

    const canonicalKeyState =
      mapParticipantFullExamResultHistorySnapshotPersistenceContract({
        intent: "delete",
        storageKey:
          activePackage.storageKey
      });

    if (
      !canonicalKeyState.isValid ||
      canonicalKeyState.canPrepareDelete !==
        true ||
      canonicalKeyState.storageKey !==
        activePackage.storageKey ||
      canonicalKeyState.requestIdentity !==
        activePackage.requestIdentity
    ) {
      return invalid(
        "persistence_result_acceptance_storage_key_invalid"
      );
    }

    const expectedReleaseIdentity =
      "exam_history_persistence_release:" +
      activePackage.operation +
      ":" +
      canonicalKeyState.requestIdentity;

    const expectedExecutionIdentity =
      "exam_history_persistence_execution:" +
      activePackage.operation +
      ":" +
      canonicalKeyState.requestIdentity;

    const expectedInvocationIdentity =
      "exam_history_persistence_invocation:" +
      activePackage.operation +
      ":" +
      canonicalKeyState.requestIdentity;

    const expectedPackageIdentity =
      "exam_history_persistence_invocation_package:" +
      activePackage.operation +
      ":" +
      canonicalKeyState.requestIdentity;

    if (
      activePackage.releaseIdentity !==
        expectedReleaseIdentity ||
      activePackage.executionIdentity !==
        expectedExecutionIdentity ||
      activePackage.invocationIdentity !==
        expectedInvocationIdentity ||
      activePackage.invocationPackageIdentity !==
        expectedPackageIdentity
    ) {
      return invalid(
        "persistence_result_acceptance_active_identity_invalid"
      );
    }

    if (
      !Array.isArray(
        activePackage.invocationArgumentNames
      ) ||
      !Array.isArray(
        activePackage.invocationArguments
      ) ||
      activePackage.invocationArgumentCount !==
        config.argumentNames.length ||
      activePackage.invocationArguments.length !==
        config.argumentNames.length ||
      JSON.stringify(
        activePackage.invocationArgumentNames
      ) !==
        JSON.stringify(
          config.argumentNames
        )
    ) {
      return invalid(
        "persistence_result_acceptance_active_arguments_invalid"
      );
    }

    for (
      let index = 0;
      index <
        activePackage.invocationArguments.length;
      index += 1
    ) {
      const argument =
        activePackage.invocationArguments[
          index
        ];

      if (
        !argument ||
        typeof argument !== "object" ||
        Array.isArray(argument) ||
        argument.position !== index ||
        argument.name !==
          config.argumentNames[index] ||
        argument.valueType !== "string" ||
        typeof argument.value !== "string"
      ) {
        return invalid(
          "persistence_result_acceptance_active_arguments_invalid"
        );
      }
    }

    if (
      activePackage.invocationArguments[0].value !==
      canonicalKeyState.storageKey
    ) {
      return invalid(
        "persistence_result_acceptance_active_key_argument_invalid"
      );
    }

    if (activePackage.operation === "write") {
      const serializedJson =
        activePackage.invocationArguments[1].value;

      const actualByteLength =
        getParticipantFullExamResultHistorySnapshotUtf8ByteLength(
          serializedJson
        );

      if (
        !Number.isSafeInteger(
          activePackage.serializedByteLength
        ) ||
        activePackage.serializedByteLength < 1 ||
        actualByteLength !==
          activePackage.serializedByteLength
      ) {
        return invalid(
          "persistence_result_acceptance_active_write_size_invalid"
        );
      }

      const deserializationState =
        mapParticipantFullExamResultHistorySnapshotDeserializationState({
          serializedJson
        });

      if (
        !deserializationState.isValid ||
        deserializationState.canDeserialize !==
          true ||
        deserializationState.canResume !== true ||
        deserializationState.requestIdentity !==
          canonicalKeyState.requestIdentity
      ) {
        return invalid(
          "persistence_result_acceptance_active_write_payload_invalid"
        );
      }
    } else if (
      activePackage.serializedByteLength !==
        null
    ) {
      return invalid(
        "persistence_result_acceptance_active_payload_unexpected"
      );
    }

    if (
      !resultState ||
      typeof resultState !== "object" ||
      Array.isArray(resultState) ||
      resultState.isSnapshotPersistenceResultContractOnly !==
        true ||
      resultState.isValid !== true ||
      resultState.canAcceptResult !== true ||
      resultState.canExecuteStorage !== false ||
      resultState.resultSchemaVersion !== 1 ||
      resultState.maximumResultBytes !== 4096 ||
      typeof resultState.invocationPackageIdentity !==
        "string"
    ) {
      return invalid(
        "persistence_result_acceptance_result_state_invalid"
      );
    }

    if (
      resultState.invocationPackageIdentity !==
      activePackage.invocationPackageIdentity
    ) {
      return {
        version: "v27.30e",
        status:
          "exam_result_history_persistence_result_acceptance_stale_ignored",
        isValid: true,
        isSnapshotPersistenceResultAcceptanceGuardOnly: true,
        isLiveCall: false,
        canApplyResult: false,
        didAcceptResult: false,
        isStaleResult: true,
        canResumeSnapshot: false,
        canExecuteStorage: false,
        activeInvocationPackageIdentity:
          activePackage.invocationPackageIdentity,
        resultInvocationPackageIdentity:
          resultState.invocationPackageIdentity,
        resultStatus: null,
        operation: null,
        methodName: null,
        storageKey: null,
        requestIdentity: null,
        invocationIdentity: null,
        didRead: false,
        didWrite: false,
        didDelete: false,
        wasAlreadyAbsent: false,
        isEmpty: false,
        serializedByteLength: null,
        snapshotPayload: null,
        resumeState: null,
        reason:
          "persistence_result_acceptance_stale_package"
      };
    }

    if (
      resultState.operation !==
        activePackage.operation ||
      resultState.methodName !==
        activePackage.methodName ||
      resultState.storageKey !==
        activePackage.storageKey ||
      resultState.requestIdentity !==
        activePackage.requestIdentity ||
      resultState.invocationIdentity !==
        activePackage.invocationIdentity
    ) {
      return invalid(
        "persistence_result_acceptance_result_identity_mismatch"
      );
    }

    const accepted = (overrides) => ({
      version: "v27.30e",
      status:
        "exam_result_history_persistence_result_acceptance_ready",
      isValid: true,
      isSnapshotPersistenceResultAcceptanceGuardOnly: true,
      isLiveCall: false,
      canApplyResult: true,
      didAcceptResult: true,
      isStaleResult: false,
      canResumeSnapshot:
        resultState.canResumeSnapshot === true,
      canExecuteStorage: false,
      activeInvocationPackageIdentity:
        activePackage.invocationPackageIdentity,
      resultInvocationPackageIdentity:
        resultState.invocationPackageIdentity,
      resultStatus:
        resultState.status,
      operation:
        activePackage.operation,
      methodName:
        activePackage.methodName,
      storageKey:
        activePackage.storageKey,
      requestIdentity:
        activePackage.requestIdentity,
      invocationIdentity:
        activePackage.invocationIdentity,
      didRead:
        resultState.didRead === true,
      didWrite:
        resultState.didWrite === true,
      didDelete:
        resultState.didDelete === true,
      wasAlreadyAbsent:
        resultState.wasAlreadyAbsent === true,
      isEmpty:
        resultState.isEmpty === true,
      serializedByteLength:
        resultState.serializedByteLength,
      snapshotPayload: null,
      resumeState: null,
      reason: null,
      ...overrides
    });

    if (activePackage.operation === "read") {
      if (
        resultState.status ===
          "exam_result_history_persistence_result_read_empty"
      ) {
        if (
          resultState.didRead !== true ||
          resultState.didWrite !== false ||
          resultState.didDelete !== false ||
          resultState.wasAlreadyAbsent !==
            false ||
          resultState.isEmpty !== true ||
          resultState.canResumeSnapshot !==
            false ||
          resultState.serializedByteLength !==
            null ||
          resultState.snapshotPayload !== null ||
          resultState.resumeState !== null
        ) {
          return invalid(
            "persistence_result_acceptance_read_empty_invalid"
          );
        }

        return accepted({});
      }

      if (
        resultState.status !==
          "exam_result_history_persistence_result_read_ready" ||
        resultState.didRead !== true ||
        resultState.didWrite !== false ||
        resultState.didDelete !== false ||
        resultState.wasAlreadyAbsent !==
          false ||
        resultState.isEmpty !== false ||
        resultState.canResumeSnapshot !==
          true ||
        !Number.isSafeInteger(
          resultState.serializedByteLength
        ) ||
        resultState.serializedByteLength < 1 ||
        resultState.serializedByteLength >
          4096 ||
        !resultState.snapshotPayload ||
        typeof resultState.snapshotPayload !==
          "object" ||
        Array.isArray(
          resultState.snapshotPayload
        ) ||
        !resultState.resumeState ||
        typeof resultState.resumeState !==
          "object" ||
        Array.isArray(
          resultState.resumeState
        )
      ) {
        return invalid(
          "persistence_result_acceptance_read_result_invalid"
        );
      }

      const normalizedSnapshot =
        normalizeParticipantFullExamResultHistoryControllerSnapshot(
          resultState.snapshotPayload
        );

      const recomputedResumeState =
        mapParticipantFullExamResultHistorySnapshotResumeState({
          snapshot:
            resultState.snapshotPayload
        });

      if (
        !normalizedSnapshot.isValid ||
        normalizedSnapshot.canResume !==
          true ||
        normalizedSnapshot.requestIdentity !==
          activePackage.requestIdentity ||
        !recomputedResumeState.isValid ||
        recomputedResumeState.canResume !==
          true ||
        recomputedResumeState.requestIdentity !==
          activePackage.requestIdentity ||
        JSON.stringify(
          recomputedResumeState
        ) !==
          JSON.stringify(
            resultState.resumeState
          )
      ) {
        return invalid(
          "persistence_result_acceptance_read_snapshot_invalid"
        );
      }

      return accepted({
        snapshotPayload:
          resultState.snapshotPayload,
        resumeState:
          recomputedResumeState
      });
    }

    if (activePackage.operation === "write") {
      if (
        resultState.status !==
          "exam_result_history_persistence_result_write_confirmed" ||
        resultState.didRead !== false ||
        resultState.didWrite !== true ||
        resultState.didDelete !== false ||
        resultState.wasAlreadyAbsent !==
          false ||
        resultState.isEmpty !== false ||
        resultState.canResumeSnapshot !==
          false ||
        resultState.serializedByteLength !==
          activePackage.serializedByteLength ||
        resultState.snapshotPayload !== null ||
        resultState.resumeState !== null
      ) {
        return invalid(
          "persistence_result_acceptance_write_result_invalid"
        );
      }

      return accepted({});
    }

    const isDeleteConfirmed =
      resultState.status ===
        "exam_result_history_persistence_result_delete_confirmed";

    const isDeleteAbsent =
      resultState.status ===
        "exam_result_history_persistence_result_delete_absent";

    if (
      (!isDeleteConfirmed &&
        !isDeleteAbsent) ||
      resultState.didRead !== false ||
      resultState.didWrite !== false ||
      resultState.canResumeSnapshot !==
        false ||
      resultState.serializedByteLength !==
        null ||
      resultState.snapshotPayload !== null ||
      resultState.resumeState !== null
    ) {
      return invalid(
        "persistence_result_acceptance_delete_result_invalid"
      );
    }

    if (
      isDeleteConfirmed &&
      (
        resultState.didDelete !== true ||
        resultState.wasAlreadyAbsent !==
          false ||
        resultState.isEmpty !== false
      )
    ) {
      return invalid(
        "persistence_result_acceptance_delete_result_invalid"
      );
    }

    if (
      isDeleteAbsent &&
      (
        resultState.didDelete !== false ||
        resultState.wasAlreadyAbsent !==
          true ||
        resultState.isEmpty !== true
      )
    ) {
      return invalid(
        "persistence_result_acceptance_delete_result_invalid"
      );
    }

    return accepted({});
  }

  function mapParticipantFullExamResultHistorySnapshotPersistenceResultContract(input) {
    const source =
      input &&
      typeof input === "object" &&
      !Array.isArray(input)
        ? input
        : {};

    const maximumResultBytes = 4096;

    const inspectOwnDataProperty = (
      target,
      propertyName
    ) => {
      try {
        const descriptor =
          Object.getOwnPropertyDescriptor(
            target,
            propertyName
          );

        if (
          !descriptor ||
          !Object.prototype.hasOwnProperty.call(
            descriptor,
            "value"
          )
        ) {
          return {
            isValid: false,
            value: null
          };
        }

        return {
          isValid: true,
          value:
            descriptor.value
        };
      } catch (_error) {
        return {
          isValid: false,
          value: null
        };
      }
    };

    const invalid = (reason) => ({
      version: "v27.30d",
      status:
        "exam_result_history_persistence_result_contract_invalid",
      isValid: false,
      isSnapshotPersistenceResultContractOnly: true,
      isLiveCall: false,
      canAcceptResult: false,
      canResumeSnapshot: false,
      canExecuteStorage: false,
      resultSchemaVersion: 1,
      maximumResultBytes,
      operation: null,
      methodName: null,
      storageKey: null,
      requestIdentity: null,
      invocationIdentity: null,
      invocationPackageIdentity: null,
      didRead: false,
      didWrite: false,
      didDelete: false,
      wasAlreadyAbsent: false,
      isEmpty: false,
      serializedByteLength: null,
      snapshotPayload: null,
      resumeState: null,
      reason
    });

    const ready = (
      status,
      packageState,
      overrides = {}
    ) => ({
      version: "v27.30d",
      status,
      isValid: true,
      isSnapshotPersistenceResultContractOnly: true,
      isLiveCall: false,
      canAcceptResult: true,
      canResumeSnapshot: false,
      canExecuteStorage: false,
      resultSchemaVersion: 1,
      maximumResultBytes,
      operation:
        packageState.operation,
      methodName:
        packageState.methodName,
      storageKey:
        packageState.storageKey,
      requestIdentity:
        packageState.requestIdentity,
      invocationIdentity:
        packageState.invocationIdentity,
      invocationPackageIdentity:
        packageState.invocationPackageIdentity,
      didRead: false,
      didWrite: false,
      didDelete: false,
      wasAlreadyAbsent: false,
      isEmpty: false,
      serializedByteLength: null,
      snapshotPayload: null,
      resumeState: null,
      reason: null,
      ...overrides
    });

    const packageProperty =
      inspectOwnDataProperty(
        source,
        "invocationPackageState"
      );

    const resultProperty =
      inspectOwnDataProperty(
        source,
        "operationResult"
      );

    if (!packageProperty.isValid) {
      return invalid(
        "persistence_result_package_missing"
      );
    }

    if (!resultProperty.isValid) {
      return invalid(
        "persistence_result_value_missing"
      );
    }

    const packageState =
      packageProperty.value;

    const operationResult =
      resultProperty.value;

    if (
      !packageState ||
      typeof packageState !== "object" ||
      Array.isArray(packageState) ||
      packageState.isSnapshotPersistenceInvocationPackageOnly !==
        true ||
      packageState.isValid !== true ||
      packageState.status !==
        "exam_result_history_persistence_invocation_package_ready" ||
      packageState.canPrepareInvocationPackage !==
        true ||
      packageState.canInvokeLater !== true ||
      packageState.canExecuteStorage !== false ||
      packageState.isMethodReferenceValidated !==
        true ||
      packageState.invocationPackageSchemaVersion !==
        1
    ) {
      return invalid(
        "persistence_result_package_invalid"
      );
    }

    const operationConfig = {
      read: {
        methodName: "read",
        requiredCapability: "read",
        argumentNames: [
          "storageKey"
        ],
        hasValidatedLoadState: true
      },
      write: {
        methodName: "write",
        requiredCapability: "write",
        argumentNames: [
          "storageKey",
          "serializedJson"
        ],
        hasValidatedLoadState: false
      },
      delete: {
        methodName: "delete",
        requiredCapability: "delete",
        argumentNames: [
          "storageKey"
        ],
        hasValidatedLoadState: false
      }
    };

    const config =
      operationConfig[
        packageState.operation
      ];

    if (
      !config ||
      packageState.methodName !==
        config.methodName ||
      packageState.requiredCapability !==
        config.requiredCapability ||
      packageState.hasValidatedLoadState !==
        config.hasValidatedLoadState
    ) {
      return invalid(
        "persistence_result_operation_invalid"
      );
    }

    if (
      typeof packageState.adapterReadinessFingerprint !==
        "string" ||
      packageState.adapterReadinessFingerprint.length <
        10
    ) {
      return invalid(
        "persistence_result_readiness_fingerprint_invalid"
      );
    }

    const canonicalKeyState =
      mapParticipantFullExamResultHistorySnapshotPersistenceContract({
        intent: "delete",
        storageKey:
          packageState.storageKey
      });

    if (
      !canonicalKeyState.isValid ||
      canonicalKeyState.canPrepareDelete !==
        true ||
      canonicalKeyState.storageKey !==
        packageState.storageKey ||
      canonicalKeyState.requestIdentity !==
        packageState.requestIdentity
    ) {
      return invalid(
        "persistence_result_storage_key_invalid"
      );
    }

    const expectedReleaseIdentity =
      "exam_history_persistence_release:" +
      packageState.operation +
      ":" +
      canonicalKeyState.requestIdentity;

    const expectedExecutionIdentity =
      "exam_history_persistence_execution:" +
      packageState.operation +
      ":" +
      canonicalKeyState.requestIdentity;

    const expectedInvocationIdentity =
      "exam_history_persistence_invocation:" +
      packageState.operation +
      ":" +
      canonicalKeyState.requestIdentity;

    const expectedPackageIdentity =
      "exam_history_persistence_invocation_package:" +
      packageState.operation +
      ":" +
      canonicalKeyState.requestIdentity;

    if (
      packageState.releaseIdentity !==
        expectedReleaseIdentity ||
      packageState.executionIdentity !==
        expectedExecutionIdentity ||
      packageState.invocationIdentity !==
        expectedInvocationIdentity ||
      packageState.invocationPackageIdentity !==
        expectedPackageIdentity
    ) {
      return invalid(
        "persistence_result_identity_invalid"
      );
    }

    if (
      !Array.isArray(
        packageState.invocationArgumentNames
      ) ||
      !Array.isArray(
        packageState.invocationArguments
      ) ||
      packageState.invocationArgumentCount !==
        config.argumentNames.length ||
      packageState.invocationArguments.length !==
        config.argumentNames.length ||
      JSON.stringify(
        packageState.invocationArgumentNames
      ) !==
        JSON.stringify(
          config.argumentNames
        )
    ) {
      return invalid(
        "persistence_result_argument_schema_invalid"
      );
    }

    const canonicalArguments = [];

    for (
      let index = 0;
      index <
        packageState.invocationArguments.length;
      index += 1
    ) {
      const argument =
        packageState.invocationArguments[
          index
        ];

      if (
        !argument ||
        typeof argument !== "object" ||
        Array.isArray(argument) ||
        argument.position !== index ||
        argument.name !==
          config.argumentNames[index] ||
        argument.valueType !==
          "string" ||
        typeof argument.value !==
          "string"
      ) {
        return invalid(
          "persistence_result_argument_schema_invalid"
        );
      }

      canonicalArguments.push({
        position:
          argument.position,
        name:
          argument.name,
        valueType:
          argument.valueType,
        value:
          argument.value
      });
    }

    if (
      canonicalArguments[0].value !==
      canonicalKeyState.storageKey
    ) {
      return invalid(
        "persistence_result_storage_key_argument_invalid"
      );
    }

    let writeSerializedByteLength = null;

    if (packageState.operation === "write") {
      const serializedJson =
        canonicalArguments[1].value;

      const actualByteLength =
        getParticipantFullExamResultHistorySnapshotUtf8ByteLength(
          serializedJson
        );

      if (
        !Number.isSafeInteger(
          packageState.serializedByteLength
        ) ||
        packageState.serializedByteLength < 1 ||
        actualByteLength !==
          packageState.serializedByteLength
      ) {
        return invalid(
          "persistence_result_write_payload_size_invalid"
        );
      }

      const deserializationState =
        mapParticipantFullExamResultHistorySnapshotDeserializationState({
          serializedJson
        });

      if (
        !deserializationState.isValid ||
        deserializationState.canDeserialize !==
          true ||
        deserializationState.canResume !== true ||
        deserializationState.requestIdentity !==
          canonicalKeyState.requestIdentity ||
        deserializationState.serializedByteLength !==
          actualByteLength
      ) {
        return invalid(
          "persistence_result_write_payload_invalid"
        );
      }

      writeSerializedByteLength =
        actualByteLength;
    } else if (
      packageState.serializedByteLength !==
        null
    ) {
      return invalid(
        "persistence_result_unexpected_payload_size"
      );
    }

    if (packageState.operation === "read") {
      if (operationResult === null) {
        return ready(
          "exam_result_history_persistence_result_read_empty",
          packageState,
          {
            didRead: true,
            isEmpty: true
          }
        );
      }

      if (
        typeof operationResult !== "string"
      ) {
        return invalid(
          "persistence_result_read_value_invalid"
        );
      }

      const resultByteLength =
        getParticipantFullExamResultHistorySnapshotUtf8ByteLength(
          operationResult
        );

      if (
        !Number.isSafeInteger(
          resultByteLength
        ) ||
        resultByteLength < 1 ||
        resultByteLength >
          maximumResultBytes
      ) {
        return invalid(
          "persistence_result_read_size_invalid"
        );
      }

      const deserializationState =
        mapParticipantFullExamResultHistorySnapshotDeserializationState({
          serializedJson:
            operationResult
        });

      if (
        !deserializationState.isValid ||
        deserializationState.canDeserialize !==
          true ||
        deserializationState.canResume !== true
      ) {
        return invalid(
          deserializationState.reason ||
            "persistence_result_read_snapshot_invalid"
        );
      }

      if (
        deserializationState.requestIdentity !==
        canonicalKeyState.requestIdentity
      ) {
        return invalid(
          "persistence_result_read_identity_mismatch"
        );
      }

      return ready(
        "exam_result_history_persistence_result_read_ready",
        packageState,
        {
          canResumeSnapshot: true,
          didRead: true,
          serializedByteLength:
            deserializationState.serializedByteLength,
          snapshotPayload:
            deserializationState.snapshotPayload,
          resumeState:
            deserializationState.resumeState
        }
      );
    }

    if (packageState.operation === "write") {
      if (operationResult !== true) {
        return invalid(
          "persistence_result_write_confirmation_invalid"
        );
      }

      return ready(
        "exam_result_history_persistence_result_write_confirmed",
        packageState,
        {
          didWrite: true,
          serializedByteLength:
            writeSerializedByteLength
        }
      );
    }

    if (
      typeof operationResult !==
        "boolean"
    ) {
      return invalid(
        "persistence_result_delete_confirmation_invalid"
      );
    }

    if (operationResult) {
      return ready(
        "exam_result_history_persistence_result_delete_confirmed",
        packageState,
        {
          didDelete: true
        }
      );
    }

    return ready(
      "exam_result_history_persistence_result_delete_absent",
      packageState,
      {
        wasAlreadyAbsent: true,
        isEmpty: true
      }
    );
  }

  function mapParticipantFullExamResultHistorySnapshotPersistenceInvocationPackageState(input) {
    const source =
      input &&
      typeof input === "object" &&
      !Array.isArray(input)
        ? input
        : {};

    const inspectOwnDataProperty = (
      target,
      propertyName
    ) => {
      try {
        const descriptor =
          Object.getOwnPropertyDescriptor(
            target,
            propertyName
          );

        if (
          !descriptor ||
          !Object.prototype.hasOwnProperty.call(
            descriptor,
            "value"
          )
        ) {
          return {
            isValid: false,
            value: null
          };
        }

        return {
          isValid: true,
          value:
            descriptor.value
        };
      } catch (_error) {
        return {
          isValid: false,
          value: null
        };
      }
    };

    const invalid = (reason) => ({
      version: "v27.30c",
      status:
        "exam_result_history_persistence_invocation_package_invalid",
      isValid: false,
      isSnapshotPersistenceInvocationPackageOnly: true,
      isLiveCall: false,
      canPrepareInvocationPackage: false,
      canInvokeLater: false,
      canExecuteStorage: false,
      isMethodReferenceValidated: false,
      invocationPackageSchemaVersion: 1,
      operation: null,
      methodName: null,
      requiredCapability: null,
      adapterReadinessFingerprint: null,
      storageKey: null,
      requestIdentity: null,
      releaseIdentity: null,
      executionIdentity: null,
      invocationIdentity: null,
      invocationPackageIdentity: null,
      invocationArgumentCount: null,
      invocationArgumentNames: [],
      invocationArguments: [],
      serializedByteLength: null,
      hasValidatedLoadState: false,
      reason
    });

    const releaseProperty =
      inspectOwnDataProperty(
        source,
        "releaseState"
      );

    const persistenceProperty =
      inspectOwnDataProperty(
        source,
        "persistenceState"
      );

    const adapterProperty =
      inspectOwnDataProperty(
        source,
        "storageAdapter"
      );

    const executionProperty =
      inspectOwnDataProperty(
        source,
        "executionState"
      );

    const invocationProperty =
      inspectOwnDataProperty(
        source,
        "invocationContractState"
      );

    if (!releaseProperty.isValid) {
      return invalid(
        "persistence_invocation_package_release_state_missing"
      );
    }

    if (!persistenceProperty.isValid) {
      return invalid(
        "persistence_invocation_package_persistence_state_missing"
      );
    }

    if (!adapterProperty.isValid) {
      return invalid(
        "persistence_invocation_package_storage_adapter_missing"
      );
    }

    if (!executionProperty.isValid) {
      return invalid(
        "persistence_invocation_package_execution_state_missing"
      );
    }

    if (!invocationProperty.isValid) {
      return invalid(
        "persistence_invocation_package_contract_missing"
      );
    }

    const releaseState =
      releaseProperty.value;

    const persistenceState =
      persistenceProperty.value;

    const storageAdapter =
      adapterProperty.value;

    const executionState =
      executionProperty.value;

    const invocationContractState =
      invocationProperty.value;

    if (
      !executionState ||
      typeof executionState !== "object" ||
      Array.isArray(executionState) ||
      executionState.isSnapshotPersistenceExecutionGuardOnly !==
        true ||
      executionState.isValid !== true ||
      executionState.status !==
        "exam_result_history_persistence_execution_guard_ready" ||
      executionState.canPrepareExecution !== true ||
      executionState.canInvokeLater !== true ||
      executionState.canExecuteStorage !== false ||
      executionState.isMethodReferenceValidated !==
        true
    ) {
      return invalid(
        "persistence_invocation_package_execution_state_invalid"
      );
    }

    if (
      !invocationContractState ||
      typeof invocationContractState !==
        "object" ||
      Array.isArray(invocationContractState) ||
      invocationContractState.isSnapshotPersistenceInvocationContractOnly !==
        true ||
      invocationContractState.isValid !== true ||
      invocationContractState.status !==
        "exam_result_history_persistence_invocation_contract_ready" ||
      invocationContractState.canBuildInvocation !==
        true ||
      invocationContractState.canInvokeLater !==
        true ||
      invocationContractState.canExecuteStorage !==
        false ||
      invocationContractState.invocationSchemaVersion !==
        1
    ) {
      return invalid(
        "persistence_invocation_package_contract_invalid"
      );
    }

    if (
      !storageAdapter ||
      typeof storageAdapter !== "object" ||
      Array.isArray(storageAdapter)
    ) {
      return invalid(
        "persistence_invocation_package_storage_adapter_invalid"
      );
    }

    const recomputedExecution =
      guardParticipantFullExamResultHistorySnapshotPersistenceExecution({
        releaseState,
        persistenceState,
        storageAdapter
      });

    if (
      !recomputedExecution.isValid ||
      recomputedExecution.canPrepareExecution !==
        true ||
      recomputedExecution.canInvokeLater !==
        true ||
      recomputedExecution.canExecuteStorage !==
        false
    ) {
      return invalid(
        "persistence_invocation_package_recomputed_execution_invalid"
      );
    }

    const executionMatches =
      recomputedExecution.operation ===
        executionState.operation &&
      recomputedExecution.operationMethodName ===
        executionState.operationMethodName &&
      recomputedExecution.requiredCapability ===
        executionState.requiredCapability &&
      recomputedExecution.adapterReadinessFingerprint ===
        executionState.adapterReadinessFingerprint &&
      recomputedExecution.storageKey ===
        executionState.storageKey &&
      recomputedExecution.requestIdentity ===
        executionState.requestIdentity &&
      recomputedExecution.releaseIdentity ===
        executionState.releaseIdentity &&
      recomputedExecution.executionIdentity ===
        executionState.executionIdentity &&
      recomputedExecution.operationArgumentCount ===
        executionState.operationArgumentCount &&
      recomputedExecution.serializedByteLength ===
        executionState.serializedByteLength &&
      recomputedExecution.serializedJson ===
        executionState.serializedJson &&
      recomputedExecution.hasValidatedLoadState ===
        executionState.hasValidatedLoadState;

    if (!executionMatches) {
      return invalid(
        "persistence_invocation_package_execution_state_mismatch"
      );
    }

    const recomputedInvocation =
      mapParticipantFullExamResultHistorySnapshotPersistenceInvocationContract({
        executionState:
          recomputedExecution
      });

    if (
      !recomputedInvocation.isValid ||
      recomputedInvocation.canBuildInvocation !==
        true ||
      recomputedInvocation.canInvokeLater !==
        true ||
      recomputedInvocation.canExecuteStorage !==
        false
    ) {
      return invalid(
        "persistence_invocation_package_recomputed_contract_invalid"
      );
    }

    const contractMatches =
      recomputedInvocation.invocationSchemaVersion ===
        invocationContractState.invocationSchemaVersion &&
      recomputedInvocation.operation ===
        invocationContractState.operation &&
      recomputedInvocation.methodName ===
        invocationContractState.methodName &&
      recomputedInvocation.requiredCapability ===
        invocationContractState.requiredCapability &&
      recomputedInvocation.adapterReadinessFingerprint ===
        invocationContractState.adapterReadinessFingerprint &&
      recomputedInvocation.storageKey ===
        invocationContractState.storageKey &&
      recomputedInvocation.requestIdentity ===
        invocationContractState.requestIdentity &&
      recomputedInvocation.releaseIdentity ===
        invocationContractState.releaseIdentity &&
      recomputedInvocation.executionIdentity ===
        invocationContractState.executionIdentity &&
      recomputedInvocation.invocationIdentity ===
        invocationContractState.invocationIdentity &&
      recomputedInvocation.invocationArgumentCount ===
        invocationContractState.invocationArgumentCount &&
      JSON.stringify(
        recomputedInvocation.invocationArgumentNames
      ) ===
        JSON.stringify(
          invocationContractState.invocationArgumentNames
        ) &&
      JSON.stringify(
        recomputedInvocation.invocationArguments
      ) ===
        JSON.stringify(
          invocationContractState.invocationArguments
        ) &&
      recomputedInvocation.serializedByteLength ===
        invocationContractState.serializedByteLength &&
      recomputedInvocation.hasValidatedLoadState ===
        invocationContractState.hasValidatedLoadState;

    if (!contractMatches) {
      return invalid(
        "persistence_invocation_package_contract_mismatch"
      );
    }

    const methodProperty =
      inspectOwnDataProperty(
        storageAdapter,
        recomputedInvocation.methodName
      );

    if (
      !methodProperty.isValid ||
      typeof methodProperty.value !==
        "function"
    ) {
      return invalid(
        "persistence_invocation_package_method_invalid"
      );
    }

    const invocationArguments = [];

    for (
      let index = 0;
      index <
        recomputedInvocation.invocationArguments.length;
      index += 1
    ) {
      const argument =
        recomputedInvocation.invocationArguments[index];

      if (
        !argument ||
        typeof argument !== "object" ||
        Array.isArray(argument) ||
        argument.position !== index ||
        typeof argument.name !== "string" ||
        typeof argument.valueType !== "string" ||
        argument.valueType !== "string" ||
        typeof argument.value !== "string"
      ) {
        return invalid(
          "persistence_invocation_package_argument_schema_invalid"
        );
      }

      invocationArguments.push({
        position:
          argument.position,
        name:
          argument.name,
        valueType:
          argument.valueType,
        value:
          argument.value
      });
    }

    const invocationArgumentNames =
      invocationArguments.map(
        (argument) => argument.name
      );

    if (
      JSON.stringify(invocationArgumentNames) !==
      JSON.stringify(
        recomputedInvocation.invocationArgumentNames
      ) ||
      invocationArguments.length !==
        recomputedInvocation.invocationArgumentCount
    ) {
      return invalid(
        "persistence_invocation_package_argument_schema_invalid"
      );
    }

    const invocationPackageIdentity =
      "exam_history_persistence_invocation_package:" +
      recomputedInvocation.operation +
      ":" +
      recomputedInvocation.requestIdentity;

    return {
      version: "v27.30c",
      status:
        "exam_result_history_persistence_invocation_package_ready",
      isValid: true,
      isSnapshotPersistenceInvocationPackageOnly: true,
      isLiveCall: false,
      canPrepareInvocationPackage: true,
      canInvokeLater: true,
      canExecuteStorage: false,
      isMethodReferenceValidated: true,
      invocationPackageSchemaVersion: 1,
      operation:
        recomputedInvocation.operation,
      methodName:
        recomputedInvocation.methodName,
      requiredCapability:
        recomputedInvocation.requiredCapability,
      adapterReadinessFingerprint:
        recomputedInvocation.adapterReadinessFingerprint,
      storageKey:
        recomputedInvocation.storageKey,
      requestIdentity:
        recomputedInvocation.requestIdentity,
      releaseIdentity:
        recomputedInvocation.releaseIdentity,
      executionIdentity:
        recomputedInvocation.executionIdentity,
      invocationIdentity:
        recomputedInvocation.invocationIdentity,
      invocationPackageIdentity,
      invocationArgumentCount:
        invocationArguments.length,
      invocationArgumentNames,
      invocationArguments,
      serializedByteLength:
        recomputedInvocation.serializedByteLength,
      hasValidatedLoadState:
        recomputedInvocation.hasValidatedLoadState,
      reason: null
    };
  }

  function mapParticipantFullExamResultHistorySnapshotPersistenceInvocationContract(input) {
    const source =
      input &&
      typeof input === "object" &&
      !Array.isArray(input)
        ? input
        : {};

    const executionState =
      source.executionState &&
      typeof source.executionState === "object" &&
      !Array.isArray(source.executionState)
        ? source.executionState
        : null;

    const invalid = (reason) => ({
      version: "v27.30b",
      status:
        "exam_result_history_persistence_invocation_contract_invalid",
      isValid: false,
      isSnapshotPersistenceInvocationContractOnly: true,
      isLiveCall: false,
      canBuildInvocation: false,
      canInvokeLater: false,
      canExecuteStorage: false,
      invocationSchemaVersion: 1,
      operation: null,
      methodName: null,
      requiredCapability: null,
      adapterReadinessFingerprint: null,
      storageKey: null,
      requestIdentity: null,
      releaseIdentity: null,
      executionIdentity: null,
      invocationIdentity: null,
      invocationArgumentCount: null,
      invocationArgumentNames: [],
      invocationArguments: [],
      serializedByteLength: null,
      hasValidatedLoadState: false,
      reason
    });

    if (!executionState) {
      return invalid(
        "persistence_invocation_contract_execution_state_missing"
      );
    }

    if (
      executionState.isSnapshotPersistenceExecutionGuardOnly !==
        true ||
      executionState.isValid !== true ||
      executionState.status !==
        "exam_result_history_persistence_execution_guard_ready" ||
      executionState.canPrepareExecution !== true ||
      executionState.canInvokeLater !== true ||
      executionState.canExecuteStorage !== false ||
      executionState.isMethodReferenceValidated !==
        true
    ) {
      return invalid(
        "persistence_invocation_contract_execution_state_invalid"
      );
    }

    const operation =
      executionState.operation;

    const methodName =
      executionState.operationMethodName;

    const operationConfig = {
      read: {
        requiredCapability: "read",
        argumentNames: [
          "storageKey"
        ],
        requiresValidatedLoadState: true
      },
      write: {
        requiredCapability: "write",
        argumentNames: [
          "storageKey",
          "serializedJson"
        ],
        requiresValidatedLoadState: false
      },
      delete: {
        requiredCapability: "delete",
        argumentNames: [
          "storageKey"
        ],
        requiresValidatedLoadState: false
      }
    };

    const config =
      operationConfig[operation];

    if (
      !config ||
      methodName !== operation
    ) {
      return invalid(
        "persistence_invocation_contract_operation_invalid"
      );
    }

    if (
      executionState.requiredCapability !==
      config.requiredCapability
    ) {
      return invalid(
        "persistence_invocation_contract_capability_mismatch"
      );
    }

    if (
      executionState.operationArgumentCount !==
      config.argumentNames.length
    ) {
      return invalid(
        "persistence_invocation_contract_argument_count_invalid"
      );
    }

    if (
      executionState.hasValidatedLoadState !==
      config.requiresValidatedLoadState
    ) {
      return invalid(
        "persistence_invocation_contract_load_state_invalid"
      );
    }

    if (
      typeof executionState.adapterReadinessFingerprint !==
        "string" ||
      executionState.adapterReadinessFingerprint.length <
        10
    ) {
      return invalid(
        "persistence_invocation_contract_readiness_fingerprint_invalid"
      );
    }

    const canonicalKeyState =
      mapParticipantFullExamResultHistorySnapshotPersistenceContract({
        intent: "delete",
        storageKey:
          executionState.storageKey
      });

    if (
      !canonicalKeyState.isValid ||
      canonicalKeyState.canPrepareDelete !== true ||
      canonicalKeyState.storageKey !==
        executionState.storageKey ||
      canonicalKeyState.requestIdentity !==
        executionState.requestIdentity
    ) {
      return invalid(
        "persistence_invocation_contract_storage_key_invalid"
      );
    }

    const expectedReleaseIdentity =
      "exam_history_persistence_release:" +
      operation +
      ":" +
      canonicalKeyState.requestIdentity;

    if (
      executionState.releaseIdentity !==
      expectedReleaseIdentity
    ) {
      return invalid(
        "persistence_invocation_contract_release_identity_invalid"
      );
    }

    const expectedExecutionIdentity =
      "exam_history_persistence_execution:" +
      operation +
      ":" +
      canonicalKeyState.requestIdentity;

    if (
      executionState.executionIdentity !==
      expectedExecutionIdentity
    ) {
      return invalid(
        "persistence_invocation_contract_execution_identity_invalid"
      );
    }

    const invocationArguments = [
      {
        position: 0,
        name: "storageKey",
        valueType: "string",
        value:
          canonicalKeyState.storageKey
      }
    ];

    let serializedByteLength = null;

    if (operation === "write") {
      if (
        typeof executionState.serializedJson !==
          "string" ||
        !Number.isSafeInteger(
          executionState.serializedByteLength
        ) ||
        executionState.serializedByteLength < 1
      ) {
        return invalid(
          "persistence_invocation_contract_write_payload_invalid"
        );
      }

      const actualByteLength =
        getParticipantFullExamResultHistorySnapshotUtf8ByteLength(
          executionState.serializedJson
        );

      if (
        actualByteLength !==
        executionState.serializedByteLength
      ) {
        return invalid(
          "persistence_invocation_contract_write_size_mismatch"
        );
      }

      const deserializationState =
        mapParticipantFullExamResultHistorySnapshotDeserializationState({
          serializedJson:
            executionState.serializedJson
        });

      if (
        !deserializationState.isValid ||
        deserializationState.canDeserialize !==
          true ||
        deserializationState.canResume !== true ||
        deserializationState.requestIdentity !==
          canonicalKeyState.requestIdentity ||
        deserializationState.serializedByteLength !==
          actualByteLength
      ) {
        return invalid(
          "persistence_invocation_contract_write_payload_validation_failed"
        );
      }

      invocationArguments.push({
        position: 1,
        name: "serializedJson",
        valueType: "string",
        value:
          executionState.serializedJson
      });

      serializedByteLength =
        actualByteLength;
    } else if (
      executionState.serializedJson !== null ||
      executionState.serializedByteLength !==
        null
    ) {
      return invalid(
        "persistence_invocation_contract_unexpected_payload"
      );
    }

    const invocationArgumentNames =
      invocationArguments.map(
        (argument) => argument.name
      );

    if (
      JSON.stringify(invocationArgumentNames) !==
      JSON.stringify(config.argumentNames)
    ) {
      return invalid(
        "persistence_invocation_contract_argument_schema_invalid"
      );
    }

    const invocationIdentity =
      "exam_history_persistence_invocation:" +
      operation +
      ":" +
      canonicalKeyState.requestIdentity;

    return {
      version: "v27.30b",
      status:
        "exam_result_history_persistence_invocation_contract_ready",
      isValid: true,
      isSnapshotPersistenceInvocationContractOnly: true,
      isLiveCall: false,
      canBuildInvocation: true,
      canInvokeLater: true,
      canExecuteStorage: false,
      invocationSchemaVersion: 1,
      operation,
      methodName,
      requiredCapability:
        config.requiredCapability,
      adapterReadinessFingerprint:
        executionState.adapterReadinessFingerprint,
      storageKey:
        canonicalKeyState.storageKey,
      requestIdentity:
        canonicalKeyState.requestIdentity,
      releaseIdentity:
        expectedReleaseIdentity,
      executionIdentity:
        expectedExecutionIdentity,
      invocationIdentity,
      invocationArgumentCount:
        invocationArguments.length,
      invocationArgumentNames,
      invocationArguments,
      serializedByteLength,
      hasValidatedLoadState:
        config.requiresValidatedLoadState,
      reason: null
    };
  }

  function guardParticipantFullExamResultHistorySnapshotPersistenceExecution(input) {
    const source =
      input &&
      typeof input === "object" &&
      !Array.isArray(input)
        ? input
        : {};

    const inspectOwnDataProperty = (
      target,
      propertyName
    ) => {
      try {
        const descriptor =
          Object.getOwnPropertyDescriptor(
            target,
            propertyName
          );

        if (
          !descriptor ||
          !Object.prototype.hasOwnProperty.call(
            descriptor,
            "value"
          )
        ) {
          return {
            isValid: false,
            value: null
          };
        }

        return {
          isValid: true,
          value:
            descriptor.value
        };
      } catch (_error) {
        return {
          isValid: false,
          value: null
        };
      }
    };

    const invalid = (reason) => ({
      version: "v27.30a",
      status:
        "exam_result_history_persistence_execution_guard_invalid",
      isValid: false,
      isSnapshotPersistenceExecutionGuardOnly: true,
      isLiveCall: false,
      canPrepareExecution: false,
      canInvokeLater: false,
      canExecuteStorage: false,
      isMethodReferenceValidated: false,
      operation: null,
      operationMethodName: null,
      requiredCapability: null,
      adapterReadinessFingerprint: null,
      storageKey: null,
      requestIdentity: null,
      releaseIdentity: null,
      executionIdentity: null,
      operationArgumentCount: null,
      serializedByteLength: null,
      serializedJson: null,
      hasValidatedLoadState: false,
      reason
    });

    const releaseProperty =
      inspectOwnDataProperty(
        source,
        "releaseState"
      );

    const persistenceProperty =
      inspectOwnDataProperty(
        source,
        "persistenceState"
      );

    const adapterProperty =
      inspectOwnDataProperty(
        source,
        "storageAdapter"
      );

    if (!releaseProperty.isValid) {
      return invalid(
        "persistence_execution_release_state_missing"
      );
    }

    if (!persistenceProperty.isValid) {
      return invalid(
        "persistence_execution_persistence_state_missing"
      );
    }

    if (!adapterProperty.isValid) {
      return invalid(
        "persistence_execution_storage_adapter_missing"
      );
    }

    const releaseState =
      releaseProperty.value;

    const persistenceState =
      persistenceProperty.value;

    const storageAdapter =
      adapterProperty.value;

    if (
      !releaseState ||
      typeof releaseState !== "object" ||
      Array.isArray(releaseState) ||
      releaseState.isSnapshotPersistenceOperationReleaseOnly !==
        true ||
      releaseState.isValid !== true ||
      releaseState.status !==
        "exam_result_history_persistence_operation_release_ready" ||
      releaseState.canReleaseOperation !== true ||
      releaseState.canExecuteStorage !== false ||
      typeof releaseState.releaseIdentity !==
        "string" ||
      typeof releaseState.adapterReadinessFingerprint !==
        "string"
    ) {
      return invalid(
        "persistence_execution_release_state_invalid"
      );
    }

    if (
      !persistenceState ||
      typeof persistenceState !== "object" ||
      Array.isArray(persistenceState) ||
      persistenceState.isSnapshotPersistenceContractOnly !==
        true ||
      persistenceState.isValid !== true ||
      persistenceState.canExecuteStorage !== false ||
      persistenceState.canWriteStorage !== false
    ) {
      return invalid(
        "persistence_execution_persistence_state_invalid"
      );
    }

    if (
      !storageAdapter ||
      typeof storageAdapter !== "object" ||
      Array.isArray(storageAdapter)
    ) {
      return invalid(
        "persistence_execution_storage_adapter_invalid"
      );
    }

    const currentReadiness =
      mapParticipantFullExamResultHistorySnapshotStorageAdapterReadiness({
        storageAdapter
      });

    if (
      !currentReadiness.isValid ||
      currentReadiness.canInspectAdapter !== true ||
      currentReadiness.canExecuteStorage !== false
    ) {
      return invalid(
        currentReadiness.reason ||
          "persistence_execution_readiness_invalid"
      );
    }

    const currentFingerprint =
      getParticipantFullExamResultHistorySnapshotStorageAdapterReadinessFingerprint(
        currentReadiness
      );

    if (
      typeof currentFingerprint !==
        "string"
    ) {
      return invalid(
        "persistence_execution_readiness_fingerprint_invalid"
      );
    }

    if (
      currentFingerprint !==
      releaseState.adapterReadinessFingerprint
    ) {
      return invalid(
        "persistence_execution_readiness_changed"
      );
    }

    const recomputedPlan =
      mapParticipantFullExamResultHistorySnapshotPersistenceOperationPlan({
        persistenceState,
        adapterReadinessState:
          currentReadiness
      });

    if (
      !recomputedPlan.isValid ||
      recomputedPlan.canPlanOperation !== true ||
      recomputedPlan.canExecuteStorage !== false
    ) {
      return invalid(
        "persistence_execution_recomputed_plan_invalid"
      );
    }

    const recomputedRelease =
      mapParticipantFullExamResultHistorySnapshotPersistenceOperationReleaseState({
        operationPlanState:
          recomputedPlan,
        persistenceState,
        adapterReadinessState:
          currentReadiness
      });

    if (
      !recomputedRelease.isValid ||
      recomputedRelease.canReleaseOperation !==
        true ||
      recomputedRelease.canExecuteStorage !==
        false
    ) {
      return invalid(
        "persistence_execution_recomputed_release_invalid"
      );
    }

    const releaseMatches =
      recomputedRelease.operation ===
        releaseState.operation &&
      recomputedRelease.requiredCapability ===
        releaseState.requiredCapability &&
      recomputedRelease.adapterReadinessFingerprint ===
        releaseState.adapterReadinessFingerprint &&
      recomputedRelease.storageKey ===
        releaseState.storageKey &&
      recomputedRelease.requestIdentity ===
        releaseState.requestIdentity &&
      recomputedRelease.releaseIdentity ===
        releaseState.releaseIdentity &&
      recomputedRelease.serializedByteLength ===
        releaseState.serializedByteLength &&
      recomputedRelease.serializedJson ===
        releaseState.serializedJson &&
      recomputedRelease.hasValidatedLoadState ===
        releaseState.hasValidatedLoadState;

    if (!releaseMatches) {
      return invalid(
        "persistence_execution_release_mismatch"
      );
    }

    const operationMethodName =
      releaseState.operation;

    if (
      operationMethodName !== "read" &&
      operationMethodName !== "write" &&
      operationMethodName !== "delete"
    ) {
      return invalid(
        "persistence_execution_operation_invalid"
      );
    }

    const methodProperty =
      inspectOwnDataProperty(
        storageAdapter,
        operationMethodName
      );

    if (
      !methodProperty.isValid ||
      typeof methodProperty.value !==
        "function"
    ) {
      return invalid(
        "persistence_execution_method_invalid"
      );
    }

    let operationArgumentCount = 1;
    let serializedJson = null;
    let serializedByteLength = null;

    if (operationMethodName === "write") {
      if (
        typeof releaseState.serializedJson !==
          "string" ||
        !Number.isSafeInteger(
          releaseState.serializedByteLength
        ) ||
        releaseState.serializedByteLength < 1
      ) {
        return invalid(
          "persistence_execution_write_payload_invalid"
        );
      }

      operationArgumentCount = 2;
      serializedJson =
        releaseState.serializedJson;
      serializedByteLength =
        releaseState.serializedByteLength;
    } else if (
      releaseState.serializedJson !== null
    ) {
      return invalid(
        "persistence_execution_unexpected_payload"
      );
    }

    if (
      operationMethodName === "read" &&
      releaseState.hasValidatedLoadState !==
        true
    ) {
      return invalid(
        "persistence_execution_load_state_invalid"
      );
    }

    const executionIdentity =
      "exam_history_persistence_execution:" +
      operationMethodName +
      ":" +
      releaseState.requestIdentity;

    return {
      version: "v27.30a",
      status:
        "exam_result_history_persistence_execution_guard_ready",
      isValid: true,
      isSnapshotPersistenceExecutionGuardOnly: true,
      isLiveCall: false,
      canPrepareExecution: true,
      canInvokeLater: true,
      canExecuteStorage: false,
      isMethodReferenceValidated: true,
      operation:
        operationMethodName,
      operationMethodName,
      requiredCapability:
        releaseState.requiredCapability,
      adapterReadinessFingerprint:
        currentFingerprint,
      storageKey:
        releaseState.storageKey,
      requestIdentity:
        releaseState.requestIdentity,
      releaseIdentity:
        releaseState.releaseIdentity,
      executionIdentity,
      operationArgumentCount,
      serializedByteLength,
      serializedJson,
      hasValidatedLoadState:
        releaseState.hasValidatedLoadState,
      reason: null
    };
  }

  function getParticipantFullExamResultHistorySnapshotStorageAdapterReadinessFingerprint(input) {
    const state =
      input &&
      typeof input === "object" &&
      !Array.isArray(input)
        ? input
        : null;

    if (
      !state ||
      state.isSnapshotStorageAdapterReadinessOnly !== true ||
      state.isValid !== true ||
      state.canInspectAdapter !== true ||
      state.canExecuteStorage !== false ||
      state.adapterKind !==
        "accaoui_exam_history_snapshot_storage_adapter_v1" ||
      state.contractVersion !== 1
    ) {
      return null;
    }

    const requiredCapabilities = [
      "read",
      "write",
      "delete"
    ];

    const capabilityFlags = {
      read:
        state.canRead === true,
      write:
        state.canWrite === true,
      delete:
        state.canDelete === true
    };

    const availableCapabilities =
      requiredCapabilities.filter(
        (capability) =>
          capabilityFlags[capability]
      );

    const missingCapabilities =
      requiredCapabilities.filter(
        (capability) =>
          !capabilityFlags[capability]
      );

    const isAdapterReady =
      availableCapabilities.length ===
      requiredCapabilities.length;

    const isPartiallyReady =
      !isAdapterReady &&
      availableCapabilities.length > 0;

    const expectedStatus =
      isAdapterReady
        ? "exam_result_history_storage_adapter_readiness_ready"
        : isPartiallyReady
          ? "exam_result_history_storage_adapter_readiness_partial"
          : "exam_result_history_storage_adapter_readiness_unavailable";

    const expectedReason =
      isAdapterReady
        ? null
        : isPartiallyReady
          ? "storage_adapter_capabilities_partial"
          : "storage_adapter_capabilities_unavailable";

    if (
      JSON.stringify(
        state.requiredCapabilities
      ) !==
        JSON.stringify(
          requiredCapabilities
        ) ||
      JSON.stringify(
        state.availableCapabilities
      ) !==
        JSON.stringify(
          availableCapabilities
        ) ||
      JSON.stringify(
        state.missingCapabilities
      ) !==
        JSON.stringify(
          missingCapabilities
        ) ||
      state.availableCapabilityCount !==
        availableCapabilities.length ||
      state.isAdapterReady !==
        isAdapterReady ||
      state.isPartiallyReady !==
        isPartiallyReady ||
      state.status !==
        expectedStatus ||
      state.reason !==
        expectedReason
    ) {
      return null;
    }

    return [
      state.adapterKind,
      String(state.contractVersion),
      state.status,
      capabilityFlags.read ? "1" : "0",
      capabilityFlags.write ? "1" : "0",
      capabilityFlags.delete ? "1" : "0",
      availableCapabilities.join(","),
      missingCapabilities.join(",")
    ].join("|");
  }

  function mapParticipantFullExamResultHistorySnapshotPersistenceOperationReleaseState(input) {
    const source =
      input &&
      typeof input === "object" &&
      !Array.isArray(input)
        ? input
        : {};

    const operationPlanState =
      source.operationPlanState &&
      typeof source.operationPlanState === "object" &&
      !Array.isArray(source.operationPlanState)
        ? source.operationPlanState
        : null;

    const persistenceState =
      source.persistenceState &&
      typeof source.persistenceState === "object" &&
      !Array.isArray(source.persistenceState)
        ? source.persistenceState
        : null;

    const adapterReadinessState =
      source.adapterReadinessState &&
      typeof source.adapterReadinessState === "object" &&
      !Array.isArray(source.adapterReadinessState)
        ? source.adapterReadinessState
        : null;

    const invalid = (reason) => ({
      version: "v27.29z",
      status:
        "exam_result_history_persistence_operation_release_invalid",
      isValid: false,
      isSnapshotPersistenceOperationReleaseOnly: true,
      isLiveCall: false,
      canReleaseOperation: false,
      canExecuteStorage: false,
      operation: null,
      requiredCapability: null,
      adapterReadinessFingerprint: null,
      storageKey: null,
      requestIdentity: null,
      releaseIdentity: null,
      serializedByteLength: null,
      serializedJson: null,
      hasValidatedLoadState: false,
      reason
    });

    const blocked = (
      reason,
      operation = null,
      requiredCapability = null,
      storageKey = null,
      requestIdentity = null
    ) => ({
      version: "v27.29z",
      status:
        "exam_result_history_persistence_operation_release_blocked",
      isValid: true,
      isSnapshotPersistenceOperationReleaseOnly: true,
      isLiveCall: false,
      canReleaseOperation: false,
      canExecuteStorage: false,
      operation,
      requiredCapability,
      adapterReadinessFingerprint: null,
      storageKey,
      requestIdentity,
      releaseIdentity: null,
      serializedByteLength: null,
      serializedJson: null,
      hasValidatedLoadState: false,
      reason
    });

    if (!operationPlanState) {
      return invalid(
        "persistence_operation_release_plan_missing"
      );
    }

    if (
      operationPlanState.isSnapshotPersistenceOperationPlanOnly !== true ||
      operationPlanState.isValid !== true ||
      operationPlanState.status !==
        "exam_result_history_persistence_operation_plan_ready" ||
      operationPlanState.canPlanOperation !== true ||
      operationPlanState.canExecuteStorage !== false ||
      operationPlanState.isRequiredCapabilityAvailable !==
        true ||
      typeof operationPlanState.adapterReadinessFingerprint !==
        "string" ||
      operationPlanState.adapterReadinessFingerprint.length <
        10
    ) {
      return invalid(
        "persistence_operation_release_plan_invalid"
      );
    }

    if (
      !persistenceState ||
      persistenceState.isSnapshotPersistenceContractOnly !==
        true ||
      persistenceState.isValid !== true ||
      persistenceState.canExecuteStorage !== false ||
      persistenceState.canWriteStorage !== false
    ) {
      return invalid(
        "persistence_operation_release_persistence_state_invalid"
      );
    }

    if (
      !adapterReadinessState ||
      adapterReadinessState.isSnapshotStorageAdapterReadinessOnly !==
        true ||
      adapterReadinessState.isValid !== true ||
      adapterReadinessState.canInspectAdapter !== true ||
      adapterReadinessState.canExecuteStorage !== false
    ) {
      return invalid(
        "persistence_operation_release_readiness_state_invalid"
      );
    }

    const currentReadinessFingerprint =
      getParticipantFullExamResultHistorySnapshotStorageAdapterReadinessFingerprint(
        adapterReadinessState
      );

    if (
      typeof currentReadinessFingerprint !==
        "string"
    ) {
      return invalid(
        "persistence_operation_release_readiness_fingerprint_invalid"
      );
    }

    if (
      currentReadinessFingerprint !==
      operationPlanState.adapterReadinessFingerprint
    ) {
      return blocked(
        "persistence_operation_release_readiness_changed",
        operationPlanState.operation,
        operationPlanState.requiredCapability,
        operationPlanState.storageKey,
        operationPlanState.requestIdentity
      );
    }

    const recomputedPlan =
      mapParticipantFullExamResultHistorySnapshotPersistenceOperationPlan({
        persistenceState,
        adapterReadinessState
      });

    if (
      !recomputedPlan.isValid ||
      recomputedPlan.status !==
        "exam_result_history_persistence_operation_plan_ready" ||
      recomputedPlan.canPlanOperation !== true ||
      recomputedPlan.canExecuteStorage !== false
    ) {
      return blocked(
        "persistence_operation_release_recomputed_plan_not_ready",
        operationPlanState.operation,
        operationPlanState.requiredCapability,
        operationPlanState.storageKey,
        operationPlanState.requestIdentity
      );
    }

    const planMatches =
      recomputedPlan.operation ===
        operationPlanState.operation &&
      recomputedPlan.requiredCapability ===
        operationPlanState.requiredCapability &&
      recomputedPlan.isRequiredCapabilityAvailable ===
        operationPlanState.isRequiredCapabilityAvailable &&
      recomputedPlan.adapterReadinessFingerprint ===
        operationPlanState.adapterReadinessFingerprint &&
      recomputedPlan.storageKey ===
        operationPlanState.storageKey &&
      recomputedPlan.requestIdentity ===
        operationPlanState.requestIdentity &&
      recomputedPlan.serializedByteLength ===
        operationPlanState.serializedByteLength &&
      recomputedPlan.serializedJson ===
        operationPlanState.serializedJson &&
      recomputedPlan.hasValidatedLoadState ===
        operationPlanState.hasValidatedLoadState;

    if (!planMatches) {
      return blocked(
        "persistence_operation_release_plan_mismatch",
        operationPlanState.operation,
        operationPlanState.requiredCapability,
        operationPlanState.storageKey,
        operationPlanState.requestIdentity
      );
    }

    const releaseIdentity =
      "exam_history_persistence_release:" +
      recomputedPlan.operation +
      ":" +
      recomputedPlan.requestIdentity;

    return {
      version: "v27.29z",
      status:
        "exam_result_history_persistence_operation_release_ready",
      isValid: true,
      isSnapshotPersistenceOperationReleaseOnly: true,
      isLiveCall: false,
      canReleaseOperation: true,
      canExecuteStorage: false,
      operation:
        recomputedPlan.operation,
      requiredCapability:
        recomputedPlan.requiredCapability,
      adapterReadinessFingerprint:
        currentReadinessFingerprint,
      storageKey:
        recomputedPlan.storageKey,
      requestIdentity:
        recomputedPlan.requestIdentity,
      releaseIdentity,
      serializedByteLength:
        recomputedPlan.serializedByteLength,
      serializedJson:
        recomputedPlan.serializedJson,
      hasValidatedLoadState:
        recomputedPlan.hasValidatedLoadState,
      reason: null
    };
  }

  function mapParticipantFullExamResultHistorySnapshotPersistenceOperationPlan(input) {
    const source =
      input &&
      typeof input === "object" &&
      !Array.isArray(input)
        ? input
        : {};

    const persistenceState =
      source.persistenceState &&
      typeof source.persistenceState === "object" &&
      !Array.isArray(source.persistenceState)
        ? source.persistenceState
        : null;

    const adapterReadinessState =
      source.adapterReadinessState &&
      typeof source.adapterReadinessState === "object" &&
      !Array.isArray(source.adapterReadinessState)
        ? source.adapterReadinessState
        : null;

    const invalid = (reason) => ({
      version: "v27.29y",
      status:
        "exam_result_history_persistence_operation_plan_invalid",
      isValid: false,
      isSnapshotPersistenceOperationPlanOnly: true,
      isLiveCall: false,
      canPlanOperation: false,
      canExecuteStorage: false,
      operation: null,
      requiredCapability: null,
      isRequiredCapabilityAvailable: false,
      storageKey: null,
      requestIdentity: null,
      serializedByteLength: null,
      serializedJson: null,
      hasValidatedLoadState: false,
      adapterReadinessFingerprint: null,
      reason
    });

    if (!persistenceState) {
      return invalid(
        "persistence_operation_plan_persistence_state_missing"
      );
    }

    if (
      persistenceState.isSnapshotPersistenceContractOnly !== true ||
      persistenceState.isValid !== true ||
      persistenceState.canExecuteStorage !== false ||
      persistenceState.canWriteStorage !== false
    ) {
      return invalid(
        "persistence_operation_plan_persistence_state_invalid"
      );
    }

    if (!adapterReadinessState) {
      return invalid(
        "persistence_operation_plan_readiness_state_missing"
      );
    }

    if (
      adapterReadinessState.isSnapshotStorageAdapterReadinessOnly !== true ||
      adapterReadinessState.isValid !== true ||
      adapterReadinessState.canInspectAdapter !== true ||
      adapterReadinessState.canExecuteStorage !== false ||
      adapterReadinessState.adapterKind !==
        "accaoui_exam_history_snapshot_storage_adapter_v1" ||
      adapterReadinessState.contractVersion !== 1
    ) {
      return invalid(
        "persistence_operation_plan_readiness_state_invalid"
      );
    }

    const adapterReadinessFingerprint =
      getParticipantFullExamResultHistorySnapshotStorageAdapterReadinessFingerprint(
        adapterReadinessState
      );

    if (
      typeof adapterReadinessFingerprint !==
        "string"
    ) {
      return invalid(
        "persistence_operation_plan_readiness_fingerprint_invalid"
      );
    }

    const intent =
      typeof persistenceState.intent === "string"
        ? persistenceState.intent.trim()
        : "";

    const operationConfig = {
      save: {
        operation: "write",
        requiredCapability: "write",
        capabilityFlag: "canWrite",
        expectedStatus:
          "exam_result_history_snapshot_persistence_save_ready",
        preparationFlag:
          "canPrepareSave"
      },
      load: {
        operation: "read",
        requiredCapability: "read",
        capabilityFlag: "canRead",
        expectedStatus:
          "exam_result_history_snapshot_persistence_load_ready",
        preparationFlag:
          "canPrepareLoad"
      },
      delete: {
        operation: "delete",
        requiredCapability: "delete",
        capabilityFlag: "canDelete",
        expectedStatus:
          "exam_result_history_snapshot_persistence_delete_ready",
        preparationFlag:
          "canPrepareDelete"
      }
    };

    const config =
      operationConfig[intent];

    if (!config) {
      return invalid(
        "persistence_operation_plan_intent_invalid"
      );
    }

    if (
      persistenceState.status !==
        config.expectedStatus ||
      persistenceState[
        config.preparationFlag
      ] !== true
    ) {
      return invalid(
        "persistence_operation_plan_contract_not_ready"
      );
    }

    const canonicalKeyState =
      mapParticipantFullExamResultHistorySnapshotPersistenceContract({
        intent: "delete",
        storageKey:
          persistenceState.storageKey
      });

    if (
      !canonicalKeyState.isValid ||
      canonicalKeyState.canPrepareDelete !== true ||
      canonicalKeyState.storageKey !==
        persistenceState.storageKey ||
      canonicalKeyState.requestIdentity !==
        persistenceState.requestIdentity
    ) {
      return invalid(
        "persistence_operation_plan_storage_key_invalid"
      );
    }

    let serializedJson = null;
    let serializedByteLength = null;
    let hasValidatedLoadState = false;

    if (intent === "save") {
      if (
        typeof persistenceState.serializedJson !==
          "string" ||
        !Number.isSafeInteger(
          persistenceState.serializedByteLength
        ) ||
        persistenceState.serializedByteLength < 1
      ) {
        return invalid(
          "persistence_operation_plan_save_payload_invalid"
        );
      }

      const deserializationState =
        mapParticipantFullExamResultHistorySnapshotDeserializationState({
          serializedJson:
            persistenceState.serializedJson
        });

      if (
        !deserializationState.isValid ||
        deserializationState.canDeserialize !== true ||
        deserializationState.canResume !== true ||
        deserializationState.requestIdentity !==
          persistenceState.requestIdentity ||
        deserializationState.serializedByteLength !==
          persistenceState.serializedByteLength
      ) {
        return invalid(
          "persistence_operation_plan_save_payload_validation_failed"
        );
      }

      serializedJson =
        persistenceState.serializedJson;

      serializedByteLength =
        persistenceState.serializedByteLength;
    }

    if (intent === "load") {
      const deserializationState =
        persistenceState.deserializationState &&
        typeof persistenceState.deserializationState ===
          "object" &&
        !Array.isArray(
          persistenceState.deserializationState
        )
          ? persistenceState.deserializationState
          : null;

      if (
        !deserializationState ||
        deserializationState.isSnapshotDeserializationMapperOnly !==
          true ||
        !deserializationState.isValid ||
        deserializationState.canDeserialize !== true ||
        deserializationState.canResume !== true ||
        deserializationState.requestIdentity !==
          persistenceState.requestIdentity
      ) {
        return invalid(
          "persistence_operation_plan_load_state_invalid"
        );
      }

      hasValidatedLoadState = true;

      serializedByteLength =
        deserializationState.serializedByteLength;
    }

    const isRequiredCapabilityAvailable =
      adapterReadinessState[
        config.capabilityFlag
      ] === true;

    if (!isRequiredCapabilityAvailable) {
      return {
        version: "v27.29y",
        status:
          "exam_result_history_persistence_operation_plan_blocked",
        isValid: true,
        isSnapshotPersistenceOperationPlanOnly: true,
        isLiveCall: false,
        canPlanOperation: false,
        canExecuteStorage: false,
        operation:
          config.operation,
        requiredCapability:
          config.requiredCapability,
        isRequiredCapabilityAvailable: false,
        storageKey:
          canonicalKeyState.storageKey,
        requestIdentity:
          canonicalKeyState.requestIdentity,
        serializedByteLength: null,
        serializedJson: null,
        hasValidatedLoadState: false,
        adapterReadinessFingerprint,
        reason:
          "persistence_operation_plan_capability_unavailable"
      };
    }

    return {
      version: "v27.29y",
      status:
        "exam_result_history_persistence_operation_plan_ready",
      isValid: true,
      isSnapshotPersistenceOperationPlanOnly: true,
      isLiveCall: false,
      canPlanOperation: true,
      canExecuteStorage: false,
      operation:
        config.operation,
      requiredCapability:
        config.requiredCapability,
      isRequiredCapabilityAvailable: true,
      storageKey:
        canonicalKeyState.storageKey,
      requestIdentity:
        canonicalKeyState.requestIdentity,
      serializedByteLength,
      serializedJson,
      hasValidatedLoadState,
      adapterReadinessFingerprint,
      reason: null
    };
  }

  function mapParticipantFullExamResultHistorySnapshotStorageAdapterReadiness(input) {
    const source =
      input &&
      typeof input === "object" &&
      !Array.isArray(input)
        ? input
        : {};

    const expectedAdapterKind =
      "accaoui_exam_history_snapshot_storage_adapter_v1";

    const expectedContractVersion = 1;

    const requiredCapabilities = [
      "read",
      "write",
      "delete"
    ];

    const invalid = (reason) => ({
      version: "v27.29x",
      status:
        "exam_result_history_storage_adapter_readiness_invalid",
      isValid: false,
      isSnapshotStorageAdapterReadinessOnly: true,
      isLiveCall: false,
      canInspectAdapter: false,
      canExecuteStorage: false,
      isAdapterReady: false,
      isPartiallyReady: false,
      adapterKind: null,
      contractVersion: null,
      requiredCapabilities:
        requiredCapabilities.slice(),
      availableCapabilities: [],
      missingCapabilities:
        requiredCapabilities.slice(),
      availableCapabilityCount: 0,
      canRead: false,
      canWrite: false,
      canDelete: false,
      reason
    });

    const inspectOwnDataProperty = (
      target,
      propertyName
    ) => {
      try {
        const descriptor =
          Object.getOwnPropertyDescriptor(
            target,
            propertyName
          );

        if (!descriptor) {
          return {
            isSafe: true,
            exists: false,
            isAccessor: false,
            value: null
          };
        }

        if (
          !Object.prototype.hasOwnProperty.call(
            descriptor,
            "value"
          )
        ) {
          return {
            isSafe: true,
            exists: true,
            isAccessor: true,
            value: null
          };
        }

        return {
          isSafe: true,
          exists: true,
          isAccessor: false,
          value:
            descriptor.value
        };
      } catch (_error) {
        return {
          isSafe: false,
          exists: false,
          isAccessor: false,
          value: null
        };
      }
    };

    const adapterProperty =
      inspectOwnDataProperty(
        source,
        "storageAdapter"
      );

    if (!adapterProperty.isSafe) {
      return invalid(
        "storage_adapter_property_inspection_failed"
      );
    }

    if (!adapterProperty.exists) {
      return invalid(
        "storage_adapter_missing"
      );
    }

    if (adapterProperty.isAccessor) {
      return invalid(
        "storage_adapter_property_accessor_not_allowed"
      );
    }

    const storageAdapter =
      adapterProperty.value;

    if (
      !storageAdapter ||
      typeof storageAdapter !== "object" ||
      Array.isArray(storageAdapter)
    ) {
      return invalid(
        "storage_adapter_must_be_object"
      );
    }

    const kindProperty =
      inspectOwnDataProperty(
        storageAdapter,
        "adapterKind"
      );

    const versionProperty =
      inspectOwnDataProperty(
        storageAdapter,
        "contractVersion"
      );

    if (
      !kindProperty.isSafe ||
      !versionProperty.isSafe
    ) {
      return invalid(
        "storage_adapter_metadata_inspection_failed"
      );
    }

    if (
      !kindProperty.exists ||
      kindProperty.isAccessor ||
      kindProperty.value !==
        expectedAdapterKind
    ) {
      return invalid(
        "storage_adapter_kind_invalid"
      );
    }

    if (
      !versionProperty.exists ||
      versionProperty.isAccessor ||
      versionProperty.value !==
        expectedContractVersion
    ) {
      return invalid(
        "storage_adapter_contract_version_invalid"
      );
    }

    const capabilityStates =
      requiredCapabilities.map(
        (capabilityName) => {
          const capabilityProperty =
            inspectOwnDataProperty(
              storageAdapter,
              capabilityName
            );

          return {
            name:
              capabilityName,
            isSafe:
              capabilityProperty.isSafe,
            isAccessor:
              capabilityProperty.isAccessor,
            isAvailable:
              capabilityProperty.isSafe &&
              capabilityProperty.exists &&
              !capabilityProperty.isAccessor &&
              typeof capabilityProperty.value ===
                "function"
          };
        }
      );

    if (
      capabilityStates.some(
        (state) => !state.isSafe
      )
    ) {
      return invalid(
        "storage_adapter_capability_inspection_failed"
      );
    }

    if (
      capabilityStates.some(
        (state) => state.isAccessor
      )
    ) {
      return invalid(
        "storage_adapter_capability_accessor_not_allowed"
      );
    }

    const availableCapabilities =
      capabilityStates
        .filter(
          (state) => state.isAvailable
        )
        .map(
          (state) => state.name
        );

    const missingCapabilities =
      capabilityStates
        .filter(
          (state) => !state.isAvailable
        )
        .map(
          (state) => state.name
        );

    const canRead =
      availableCapabilities.includes(
        "read"
      );

    const canWrite =
      availableCapabilities.includes(
        "write"
      );

    const canDelete =
      availableCapabilities.includes(
        "delete"
      );

    const isAdapterReady =
      canRead &&
      canWrite &&
      canDelete;

    const isPartiallyReady =
      !isAdapterReady &&
      availableCapabilities.length > 0;

    const status =
      isAdapterReady
        ? "exam_result_history_storage_adapter_readiness_ready"
        : isPartiallyReady
          ? "exam_result_history_storage_adapter_readiness_partial"
          : "exam_result_history_storage_adapter_readiness_unavailable";

    const reason =
      isAdapterReady
        ? null
        : isPartiallyReady
          ? "storage_adapter_capabilities_partial"
          : "storage_adapter_capabilities_unavailable";

    return {
      version: "v27.29x",
      status,
      isValid: true,
      isSnapshotStorageAdapterReadinessOnly: true,
      isLiveCall: false,
      canInspectAdapter: true,
      canExecuteStorage: false,
      isAdapterReady,
      isPartiallyReady,
      adapterKind:
        expectedAdapterKind,
      contractVersion:
        expectedContractVersion,
      requiredCapabilities:
        requiredCapabilities.slice(),
      availableCapabilities,
      missingCapabilities,
      availableCapabilityCount:
        availableCapabilities.length,
      canRead,
      canWrite,
      canDelete,
      reason
    };
  }

  function mapParticipantFullExamResultHistorySnapshotPersistenceContract(input) {
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
      "save",
      "load",
      "delete"
    ];

    const storageNamespace =
      "accaoui.exam_history.snapshot.v1";

    const storageKeyPrefix =
      storageNamespace + ":";

    const maximumStorageKeyLength = 128;

    const invalid = (reason) => ({
      version: "v27.29w",
      status:
        "exam_result_history_snapshot_persistence_invalid",
      intent,
      isValid: false,
      isSnapshotPersistenceContractOnly: true,
      isLiveCall: false,
      canExecuteStorage: false,
      canWriteStorage: false,
      canPrepareSave: false,
      canPrepareLoad: false,
      canPrepareDelete: false,
      storageNamespace,
      storageKeyPrefix,
      storageKey: null,
      requestIdentity: null,
      serializedByteLength: null,
      serializedJson: null,
      deserializationState: null,
      reason
    });

    if (!allowedIntents.includes(intent)) {
      return invalid(
        "snapshot_persistence_intent_invalid"
      );
    }

    const createState = (overrides) => ({
      version: "v27.29w",
      status:
        "exam_result_history_snapshot_persistence_blocked",
      intent,
      isValid: true,
      isSnapshotPersistenceContractOnly: true,
      isLiveCall: false,
      canExecuteStorage: false,
      canWriteStorage: false,
      canPrepareSave: false,
      canPrepareLoad: false,
      canPrepareDelete: false,
      storageNamespace,
      storageKeyPrefix,
      storageKey: null,
      requestIdentity: null,
      serializedByteLength: null,
      serializedJson: null,
      deserializationState: null,
      reason: null,
      ...overrides
    });

    const parseStorageKey = (storageKey) => {
      if (
        typeof storageKey !== "string" ||
        storageKey.length <= storageKeyPrefix.length ||
        storageKey.length > maximumStorageKeyLength ||
        !storageKey.startsWith(storageKeyPrefix)
      ) {
        return {
          isValid: false,
          reason:
            "snapshot_persistence_storage_key_invalid"
        };
      }

      const requestIdentity =
        storageKey.slice(storageKeyPrefix.length);

      const identityParts =
        requestIdentity.split(":");

      if (
        identityParts.length !== 4 ||
        identityParts[0] !==
          "exam_history_request"
      ) {
        return {
          isValid: false,
          reason:
            "snapshot_persistence_storage_key_format_invalid"
        };
      }

      const identityState =
        mapParticipantFullExamResultHistoryRequestIdentity({
          mode: "create",
          requestSequence:
            Number(identityParts[1]),
          request: {
            limit:
              Number(identityParts[2]),
            offset:
              Number(identityParts[3])
          }
        });

      if (
        !identityState.isValid ||
        identityState.requestIdentity !==
          requestIdentity ||
        storageKeyPrefix +
          identityState.requestIdentity !==
          storageKey
      ) {
        return {
          isValid: false,
          reason:
            "snapshot_persistence_storage_key_noncanonical"
        };
      }

      return {
        isValid: true,
        storageKey,
        requestIdentity:
          identityState.requestIdentity,
        reason: null
      };
    };

    if (intent === "save") {
      const serializationState =
        source.serializationState &&
        typeof source.serializationState === "object" &&
        !Array.isArray(source.serializationState)
          ? source.serializationState
          : null;

      if (!serializationState) {
        return invalid(
          "snapshot_persistence_serialization_state_missing"
        );
      }

      if (
        serializationState.isSnapshotSerializationMapperOnly !==
          true
      ) {
        return invalid(
          "snapshot_persistence_serialization_state_invalid"
        );
      }

      if (
        !serializationState.isValid ||
        serializationState.status !==
          "exam_result_history_snapshot_serialization_ready" ||
        serializationState.canSerialize !== true ||
        serializationState.canPersistLater !== true ||
        serializationState.canWriteStorage !== false ||
        typeof serializationState.serializedJson !==
          "string"
      ) {
        return createState({
          status:
            "exam_result_history_snapshot_persistence_save_blocked",
          reason:
            "snapshot_persistence_serialization_state_not_ready"
        });
      }

      const deserializationState =
        mapParticipantFullExamResultHistorySnapshotDeserializationState({
          serializedJson:
            serializationState.serializedJson
        });

      if (
        !deserializationState.isValid ||
        deserializationState.canDeserialize !== true ||
        deserializationState.canResume !== true
      ) {
        return invalid(
          deserializationState.reason ||
            "snapshot_persistence_save_validation_failed"
        );
      }

      if (
        deserializationState.requestIdentity !==
          serializationState.requestIdentity ||
        deserializationState.serializedByteLength !==
          serializationState.serializedByteLength
      ) {
        return invalid(
          "snapshot_persistence_save_identity_mismatch"
        );
      }

      const storageKey =
        storageKeyPrefix +
        serializationState.requestIdentity;

      const parsedKey =
        parseStorageKey(storageKey);

      if (!parsedKey.isValid) {
        return invalid(parsedKey.reason);
      }

      return createState({
        status:
          "exam_result_history_snapshot_persistence_save_ready",
        canPrepareSave: true,
        storageKey:
          parsedKey.storageKey,
        requestIdentity:
          parsedKey.requestIdentity,
        serializedByteLength:
          serializationState.serializedByteLength,
        serializedJson:
          serializationState.serializedJson
      });
    }

    const parsedKey =
      parseStorageKey(source.storageKey);

    if (!parsedKey.isValid) {
      return invalid(parsedKey.reason);
    }

    if (intent === "delete") {
      return createState({
        status:
          "exam_result_history_snapshot_persistence_delete_ready",
        canPrepareDelete: true,
        storageKey:
          parsedKey.storageKey,
        requestIdentity:
          parsedKey.requestIdentity
      });
    }

    if (
      typeof source.serializedJson !== "string"
    ) {
      return invalid(
        "snapshot_persistence_load_value_missing"
      );
    }

    const deserializationState =
      mapParticipantFullExamResultHistorySnapshotDeserializationState({
        serializedJson:
          source.serializedJson
      });

    if (
      !deserializationState.isValid ||
      deserializationState.canDeserialize !== true ||
      deserializationState.canResume !== true
    ) {
      return invalid(
        deserializationState.reason ||
          "snapshot_persistence_load_validation_failed"
      );
    }

    if (
      deserializationState.requestIdentity !==
      parsedKey.requestIdentity
    ) {
      return createState({
        status:
          "exam_result_history_snapshot_persistence_load_blocked",
        storageKey:
          parsedKey.storageKey,
        requestIdentity:
          parsedKey.requestIdentity,
        reason:
          "snapshot_persistence_storage_key_identity_mismatch"
      });
    }

    return createState({
      status:
        "exam_result_history_snapshot_persistence_load_ready",
      canPrepareLoad: true,
      storageKey:
        parsedKey.storageKey,
      requestIdentity:
        parsedKey.requestIdentity,
      serializedByteLength:
        deserializationState.serializedByteLength,
      deserializationState
    });
  }

  function mapParticipantFullExamResultHistorySnapshotDeserializationState(input) {
    const source =
      input &&
      typeof input === "object" &&
      !Array.isArray(input)
        ? input
        : {};

    const maximumSerializedBytes = 4096;

    const invalid = (
      reason,
      overrides = {}
    ) => ({
      version: "v27.29v",
      status:
        "exam_result_history_snapshot_deserialization_invalid",
      isValid: false,
      isSnapshotDeserializationMapperOnly: true,
      isLiveCall: false,
      canDeserialize: false,
      canResume: false,
      canWriteStorage: false,
      maximumSerializedBytes,
      serializedByteLength: null,
      snapshotVersion: null,
      controllerStatus: null,
      phase: null,
      requestIdentity: null,
      snapshotPayload: null,
      resumeState: null,
      reason,
      ...overrides
    });

    const serializedJson =
      typeof source.serializedJson === "string"
        ? source.serializedJson
        : null;

    if (serializedJson === null) {
      return invalid(
        "snapshot_deserialization_input_invalid"
      );
    }

    if (serializedJson.length < 2) {
      return invalid(
        "snapshot_deserialization_json_invalid"
      );
    }

    const serializedByteLength =
      getParticipantFullExamResultHistorySnapshotUtf8ByteLength(
        serializedJson
      );

    if (
      !Number.isSafeInteger(serializedByteLength) ||
      serializedByteLength < 1
    ) {
      return invalid(
        "snapshot_deserialization_byte_length_invalid"
      );
    }

    if (
      serializedByteLength >
      maximumSerializedBytes
    ) {
      return invalid(
        "snapshot_deserialization_size_limit_exceeded",
        {
          status:
            "exam_result_history_snapshot_deserialization_too_large",
          serializedByteLength
        }
      );
    }

    if (serializedJson.trim() !== serializedJson) {
      return invalid(
        "snapshot_deserialization_json_not_canonical",
        {
          serializedByteLength
        }
      );
    }

    let parsedSnapshot;

    try {
      parsedSnapshot =
        JSON.parse(serializedJson);
    } catch (_error) {
      return invalid(
        "snapshot_deserialization_json_parse_failed",
        {
          serializedByteLength
        }
      );
    }

    if (
      !parsedSnapshot ||
      typeof parsedSnapshot !== "object" ||
      Array.isArray(parsedSnapshot)
    ) {
      return invalid(
        "snapshot_deserialization_structure_invalid",
        {
          serializedByteLength
        }
      );
    }

    if (
      JSON.stringify(parsedSnapshot) !==
      serializedJson
    ) {
      return invalid(
        "snapshot_deserialization_json_not_canonical",
        {
          serializedByteLength
        }
      );
    }

    const normalizedSnapshot =
      normalizeParticipantFullExamResultHistoryControllerSnapshot(
        parsedSnapshot
      );

    if (
      !normalizedSnapshot.isValid ||
      normalizedSnapshot.canResume !== true
    ) {
      return invalid(
        normalizedSnapshot.reason ||
          "snapshot_deserialization_snapshot_invalid",
        {
          serializedByteLength
        }
      );
    }

    const canonicalCreationState =
      mapParticipantFullExamResultHistorySnapshotCreationState({
        controllerState:
          parsedSnapshot.controllerState
      });

    if (
      !canonicalCreationState.isValid ||
      canonicalCreationState.canCreateSnapshot !== true ||
      canonicalCreationState.canPersistLater !== true ||
      canonicalCreationState.canWriteStorage !== false ||
      !canonicalCreationState.snapshotPayload
    ) {
      return invalid(
        "snapshot_deserialization_canonical_creation_invalid",
        {
          serializedByteLength
        }
      );
    }

    const canonicalSerializationState =
      mapParticipantFullExamResultHistorySnapshotSerializationState({
        creationState:
          canonicalCreationState
      });

    if (
      !canonicalSerializationState.isValid ||
      canonicalSerializationState.canSerialize !== true ||
      canonicalSerializationState.serializedJson !==
        serializedJson ||
      canonicalSerializationState.serializedByteLength !==
        serializedByteLength
    ) {
      return invalid(
        "snapshot_deserialization_round_trip_mismatch",
        {
          serializedByteLength
        }
      );
    }

    if (
      canonicalCreationState.requestIdentity !==
        normalizedSnapshot.requestIdentity ||
      canonicalCreationState.controllerStatus !==
        normalizedSnapshot.controllerStatus ||
      canonicalCreationState.phase !==
        normalizedSnapshot.phase
    ) {
      return invalid(
        "snapshot_deserialization_identity_mismatch",
        {
          serializedByteLength
        }
      );
    }

    const resumeState =
      mapParticipantFullExamResultHistorySnapshotResumeState({
        snapshot:
          canonicalCreationState.snapshotPayload
      });

    if (
      !resumeState.isValid ||
      resumeState.canResume !== true ||
      resumeState.requestIdentity !==
        normalizedSnapshot.requestIdentity
    ) {
      return invalid(
        "snapshot_deserialization_resume_state_invalid",
        {
          serializedByteLength
        }
      );
    }

    return {
      version: "v27.29v",
      status:
        "exam_result_history_snapshot_deserialization_ready",
      isValid: true,
      isSnapshotDeserializationMapperOnly: true,
      isLiveCall: false,
      canDeserialize: true,
      canResume: true,
      canWriteStorage: false,
      maximumSerializedBytes,
      serializedByteLength,
      snapshotVersion:
        normalizedSnapshot.snapshotVersion,
      controllerStatus:
        normalizedSnapshot.controllerStatus,
      phase:
        normalizedSnapshot.phase,
      requestIdentity:
        normalizedSnapshot.requestIdentity,
      snapshotPayload:
        canonicalCreationState.snapshotPayload,
      resumeState,
      reason: null
    };
  }

  function getParticipantFullExamResultHistorySnapshotUtf8ByteLength(value) {
    let byteLength = 0;

    for (
      let index = 0;
      index < value.length;
      index += 1
    ) {
      const code = value.charCodeAt(index);

      if (code < 0x80) {
        byteLength += 1;
      } else if (code < 0x800) {
        byteLength += 2;
      } else if (
        code >= 0xd800 &&
        code <= 0xdbff &&
        index + 1 < value.length
      ) {
        const nextCode =
          value.charCodeAt(index + 1);

        if (
          nextCode >= 0xdc00 &&
          nextCode <= 0xdfff
        ) {
          byteLength += 4;
          index += 1;
        } else {
          byteLength += 3;
        }
      } else {
        byteLength += 3;
      }
    }

    return byteLength;
  }

  function mapParticipantFullExamResultHistorySnapshotSerializationState(input) {
    const source =
      input &&
      typeof input === "object" &&
      !Array.isArray(input)
        ? input
        : {};

    const maximumSerializedBytes = 4096;

    const invalid = (reason) => ({
      version: "v27.29u",
      status: "exam_result_history_snapshot_serialization_invalid",
      isValid: false,
      isSnapshotSerializationMapperOnly: true,
      isLiveCall: false,
      canSerialize: false,
      canPersistLater: false,
      canWriteStorage: false,
      snapshotVersion: null,
      controllerStatus: null,
      phase: null,
      requestIdentity: null,
      maximumSerializedBytes,
      serializedByteLength: null,
      serializedJson: null,
      reason
    });

    const creationState =
      source.creationState &&
      typeof source.creationState === "object" &&
      !Array.isArray(source.creationState)
        ? source.creationState
        : null;

    if (!creationState) {
      return invalid(
        "snapshot_serialization_creation_state_missing"
      );
    }

    if (
      creationState.isSnapshotCreationMapperOnly !== true
    ) {
      return invalid(
        "snapshot_serialization_creation_state_invalid"
      );
    }

    if (!creationState.isValid) {
      return invalid(
        typeof creationState.reason === "string"
          ? creationState.reason
          : "snapshot_serialization_creation_state_invalid"
      );
    }

    const createState = (overrides) => ({
      version: "v27.29u",
      status: "exam_result_history_snapshot_serialization_ready",
      isValid: true,
      isSnapshotSerializationMapperOnly: true,
      isLiveCall: false,
      canSerialize: false,
      canPersistLater: false,
      canWriteStorage: false,
      snapshotVersion:
        creationState.snapshotVersion,
      controllerStatus:
        creationState.controllerStatus,
      phase:
        creationState.phase,
      requestIdentity:
        creationState.requestIdentity,
      maximumSerializedBytes,
      serializedByteLength: null,
      serializedJson: null,
      reason: null,
      ...overrides
    });

    if (
      creationState.status !==
        "exam_result_history_snapshot_creation_ready" ||
      creationState.canCreateSnapshot !== true ||
      creationState.canPersistLater !== true ||
      creationState.canWriteStorage !== false ||
      !creationState.snapshotPayload ||
      typeof creationState.snapshotPayload !== "object" ||
      Array.isArray(creationState.snapshotPayload)
    ) {
      return createState({
        status:
          "exam_result_history_snapshot_serialization_blocked",
        reason:
          "snapshot_serialization_creation_state_not_ready"
      });
    }

    const canonicalCreationState =
      mapParticipantFullExamResultHistorySnapshotCreationState({
        controllerState:
          creationState.snapshotPayload.controllerState
      });

    if (
      !canonicalCreationState.isValid ||
      canonicalCreationState.canCreateSnapshot !== true ||
      canonicalCreationState.canPersistLater !== true ||
      canonicalCreationState.canWriteStorage !== false ||
      !canonicalCreationState.snapshotPayload
    ) {
      return invalid(
        "snapshot_serialization_canonical_creation_invalid"
      );
    }

    if (
      canonicalCreationState.requestIdentity !==
        creationState.requestIdentity ||
      canonicalCreationState.controllerStatus !==
        creationState.controllerStatus ||
      canonicalCreationState.phase !==
        creationState.phase
    ) {
      return invalid(
        "snapshot_serialization_creation_identity_mismatch"
      );
    }

    let serializedJson;

    try {
      serializedJson = JSON.stringify(
        canonicalCreationState.snapshotPayload
      );
    } catch (_error) {
      return invalid(
        "snapshot_serialization_json_stringify_failed"
      );
    }

    if (
      typeof serializedJson !== "string" ||
      serializedJson.length < 2
    ) {
      return invalid(
        "snapshot_serialization_json_invalid"
      );
    }

    const serializedByteLength =
      getParticipantFullExamResultHistorySnapshotUtf8ByteLength(
        serializedJson
      );

    if (
      !Number.isSafeInteger(serializedByteLength) ||
      serializedByteLength < 1
    ) {
      return invalid(
        "snapshot_serialization_byte_length_invalid"
      );
    }

    if (
      serializedByteLength >
      maximumSerializedBytes
    ) {
      return createState({
        status:
          "exam_result_history_snapshot_serialization_too_large",
        serializedByteLength,
        reason:
          "snapshot_serialization_size_limit_exceeded"
      });
    }

    let parsedSnapshot;

    try {
      parsedSnapshot =
        JSON.parse(serializedJson);
    } catch (_error) {
      return invalid(
        "snapshot_serialization_json_parse_failed"
      );
    }

    if (
      JSON.stringify(parsedSnapshot) !==
      serializedJson
    ) {
      return invalid(
        "snapshot_serialization_json_not_canonical"
      );
    }

    const normalizedParsedSnapshot =
      normalizeParticipantFullExamResultHistoryControllerSnapshot(
        parsedSnapshot
      );

    if (
      !normalizedParsedSnapshot.isValid ||
      normalizedParsedSnapshot.canResume !== true
    ) {
      return invalid(
        "snapshot_serialization_structure_invalid"
      );
    }

    if (
      normalizedParsedSnapshot.requestIdentity !==
        canonicalCreationState.requestIdentity ||
      normalizedParsedSnapshot.controllerStatus !==
        canonicalCreationState.controllerStatus ||
      normalizedParsedSnapshot.phase !==
        canonicalCreationState.phase
    ) {
      return invalid(
        "snapshot_serialization_round_trip_mismatch"
      );
    }

    return createState({
      status:
        "exam_result_history_snapshot_serialization_ready",
      canSerialize: true,
      canPersistLater: true,
      snapshotVersion:
        normalizedParsedSnapshot.snapshotVersion,
      controllerStatus:
        normalizedParsedSnapshot.controllerStatus,
      phase:
        normalizedParsedSnapshot.phase,
      requestIdentity:
        normalizedParsedSnapshot.requestIdentity,
      serializedByteLength,
      serializedJson
    });
  }

  function mapParticipantFullExamResultHistorySnapshotCreationState(input) {
    const source =
      input &&
      typeof input === "object" &&
      !Array.isArray(input)
        ? input
        : {};

    const controllerState =
      source.controllerState &&
      typeof source.controllerState === "object" &&
      !Array.isArray(source.controllerState)
        ? source.controllerState
        : null;

    const invalid = (reason) => ({
      version: "v27.29t",
      status: "exam_result_history_snapshot_creation_invalid",
      isValid: false,
      isSnapshotCreationMapperOnly: true,
      isLiveCall: false,
      canCreateSnapshot: false,
      canPersistLater: false,
      canWriteStorage: false,
      isTerminal: false,
      snapshotVersion: null,
      controllerStatus: null,
      phase: null,
      requestIdentity: null,
      snapshotPayload: null,
      reason
    });

    if (!controllerState) {
      return invalid(
        "snapshot_creation_controller_state_missing"
      );
    }

    const normalizedSnapshot =
      normalizeParticipantFullExamResultHistoryControllerSnapshot({
        snapshotVersion: 1,
        controllerState
      });

    if (!normalizedSnapshot.isValid) {
      return invalid(normalizedSnapshot.reason);
    }

    const createState = (overrides) => ({
      version: "v27.29t",
      status: "exam_result_history_snapshot_creation_ready",
      isValid: true,
      isSnapshotCreationMapperOnly: true,
      isLiveCall: false,
      canCreateSnapshot: false,
      canPersistLater: false,
      canWriteStorage: false,
      isTerminal: false,
      snapshotVersion: 1,
      controllerStatus:
        normalizedSnapshot.controllerStatus,
      phase:
        normalizedSnapshot.phase,
      requestIdentity:
        normalizedSnapshot.requestIdentity,
      snapshotPayload: null,
      reason: null,
      ...overrides
    });

    if (
      normalizedSnapshot.isTerminal ||
      normalizedSnapshot.canResume !== true
    ) {
      return createState({
        status:
          "exam_result_history_snapshot_creation_blocked",
        isTerminal: true,
        reason:
          "snapshot_creation_state_not_resumable"
      });
    }

    const initializedControllerState =
      mapParticipantFullExamResultHistoryRequestControllerState({
        action: "initialize",
        requestSequence:
          normalizedSnapshot.requestSequence,
        request:
          normalizedSnapshot.request
      });

    if (
      !initializedControllerState.isValid ||
      initializedControllerState.isPrepared !== true ||
      initializedControllerState.requestIdentity !==
        normalizedSnapshot.requestIdentity
    ) {
      return invalid(
        "snapshot_creation_controller_reconstruction_invalid"
      );
    }

    let reconstructedControllerState =
      initializedControllerState;

    if (normalizedSnapshot.phase === "pending") {
      reconstructedControllerState =
        mapParticipantFullExamResultHistoryRequestControllerState({
          action: "start",
          currentLifecycleState:
            initializedControllerState.lifecycleState
        });

      if (
        !reconstructedControllerState.isValid ||
        reconstructedControllerState.isPending !== true ||
        reconstructedControllerState.requestIdentity !==
          normalizedSnapshot.requestIdentity
      ) {
        return invalid(
          "snapshot_creation_pending_reconstruction_invalid"
        );
      }
    } else if (normalizedSnapshot.phase !== "prepared") {
      return invalid(
        "snapshot_creation_phase_invalid"
      );
    }

    const isNavigationSnapshot =
      normalizedSnapshot.controllerStatus ===
      "exam_result_history_request_controller_navigation_ready";

    const storedControllerState = {
      status:
        normalizedSnapshot.controllerStatus,
      isValid: true,
      isRequestControllerMapperOnly: true,
      isPrepared:
        normalizedSnapshot.phase === "prepared",
      isPending:
        normalizedSnapshot.phase === "pending",
      isCompleted: false,
      isDiscarded: false,
      isNavigationReady:
        isNavigationSnapshot,
      request:
        reconstructedControllerState.request,
      requestSequence:
        reconstructedControllerState.requestSequence,
      requestIdentity:
        reconstructedControllerState.requestIdentity,
      lifecycleState:
        reconstructedControllerState.lifecycleState
    };

    if (isNavigationSnapshot) {
      storedControllerState.previousRequestIdentity =
        normalizedSnapshot.previousRequestIdentity;
      storedControllerState.navigationIntent =
        normalizedSnapshot.navigationIntent;
    }

    const snapshotPayload = {
      snapshotVersion: 1,
      controllerState:
        storedControllerState
    };

    const roundTripState =
      normalizeParticipantFullExamResultHistoryControllerSnapshot(
        snapshotPayload
      );

    if (
      !roundTripState.isValid ||
      roundTripState.canResume !== true ||
      roundTripState.requestIdentity !==
        normalizedSnapshot.requestIdentity ||
      roundTripState.controllerStatus !==
        normalizedSnapshot.controllerStatus ||
      roundTripState.phase !==
        normalizedSnapshot.phase
    ) {
      return invalid(
        "snapshot_creation_round_trip_invalid"
      );
    }

    return createState({
      status:
        "exam_result_history_snapshot_creation_ready",
      canCreateSnapshot: true,
      canPersistLater: true,
      snapshotPayload
    });
  }

  function mapParticipantFullExamResultHistorySnapshotResumeState(input) {
    const source =
      input &&
      typeof input === "object" &&
      !Array.isArray(input)
        ? input
        : {};

    const snapshotState =
      normalizeParticipantFullExamResultHistoryControllerSnapshot(
        source.snapshot
      );

    const invalid = (reason) => ({
      version: "v27.29s",
      status: "exam_result_history_snapshot_resume_invalid",
      isValid: false,
      isSnapshotResumeMapperOnly: true,
      isLiveCall: false,
      canResume: false,
      canExecuteLiveRequest: false,
      requiresFutureLiveRequest: false,
      isPrepared: false,
      isPending: false,
      isNavigationResume: false,
      isTerminal: false,
      resumeAction: null,
      snapshotStatus:
        snapshotState &&
        typeof snapshotState.status === "string"
          ? snapshotState.status
          : null,
      originControllerStatus: null,
      request: null,
      requestSequence: null,
      requestIdentity: null,
      previousRequestIdentity: null,
      navigationIntent: null,
      reconstructedControllerState: null,
      reason
    });

    if (!snapshotState.isValid) {
      return invalid(snapshotState.reason);
    }

    const createState = (overrides) => ({
      version: "v27.29s",
      status: "exam_result_history_snapshot_resume_prepared",
      isValid: true,
      isSnapshotResumeMapperOnly: true,
      isLiveCall: false,
      canResume: false,
      canExecuteLiveRequest: false,
      requiresFutureLiveRequest: false,
      isPrepared: false,
      isPending: false,
      isNavigationResume: false,
      isTerminal: false,
      resumeAction: null,
      snapshotStatus:
        snapshotState.status,
      originControllerStatus:
        snapshotState.controllerStatus,
      request:
        snapshotState.request,
      requestSequence:
        snapshotState.requestSequence,
      requestIdentity:
        snapshotState.requestIdentity,
      previousRequestIdentity:
        snapshotState.previousRequestIdentity,
      navigationIntent:
        snapshotState.navigationIntent,
      reconstructedControllerState: null,
      reason: null,
      ...overrides
    });

    if (
      snapshotState.isTerminal ||
      snapshotState.canResume !== true
    ) {
      return createState({
        status:
          "exam_result_history_snapshot_resume_terminal_blocked",
        isTerminal: true,
        reason:
          "snapshot_resume_terminal_state"
      });
    }

    if (
      snapshotState.phase !== "prepared" &&
      snapshotState.phase !== "pending"
    ) {
      return invalid(
        "snapshot_resume_phase_invalid"
      );
    }

    const preparedControllerState =
      mapParticipantFullExamResultHistoryRequestControllerState({
        action: "initialize",
        requestSequence:
          snapshotState.requestSequence,
        request:
          snapshotState.request
      });

    if (
      !preparedControllerState.isValid ||
      preparedControllerState.isPrepared !== true ||
      preparedControllerState.requestIdentity !==
        snapshotState.requestIdentity
    ) {
      return invalid(
        "snapshot_resume_controller_reconstruction_invalid"
      );
    }

    const isNavigationResume =
      snapshotState.controllerStatus ===
      "exam_result_history_request_controller_navigation_ready";

    if (snapshotState.phase === "prepared") {
      if (
        snapshotState.resumeAction !==
        "start_prepared_request"
      ) {
        return invalid(
          "snapshot_resume_action_invalid"
        );
      }

      return createState({
        status:
          isNavigationResume
            ? "exam_result_history_snapshot_resume_navigation_prepared"
            : "exam_result_history_snapshot_resume_prepared",
        canResume: true,
        requiresFutureLiveRequest: true,
        isPrepared: true,
        isNavigationResume,
        resumeAction:
          "start_prepared_request",
        reconstructedControllerState:
          preparedControllerState
      });
    }

    if (
      snapshotState.resumeAction !==
      "retry_pending_request"
    ) {
      return invalid(
        "snapshot_resume_action_invalid"
      );
    }

    const pendingControllerState =
      mapParticipantFullExamResultHistoryRequestControllerState({
        action: "start",
        currentLifecycleState:
          preparedControllerState.lifecycleState
      });

    if (
      !pendingControllerState.isValid ||
      pendingControllerState.isPending !== true ||
      pendingControllerState.requestIdentity !==
        snapshotState.requestIdentity
    ) {
      return invalid(
        "snapshot_resume_pending_reconstruction_invalid"
      );
    }

    return createState({
      status:
        "exam_result_history_snapshot_resume_pending_retry",
      canResume: true,
      requiresFutureLiveRequest: true,
      isPending: true,
      resumeAction:
        "retry_pending_request",
      reconstructedControllerState:
        pendingControllerState
    });
  }

  function normalizeParticipantFullExamResultHistoryControllerSnapshot(input) {
    const source =
      input &&
      typeof input === "object" &&
      !Array.isArray(input)
        ? input
        : {};

    const invalid = (reason) => ({
      version: "v27.29r",
      status: "exam_result_history_controller_snapshot_invalid",
      snapshotVersion: null,
      isValid: false,
      isControllerSnapshotNormalizerOnly: true,
      isLiveCall: false,
      canResume: false,
      isTerminal: false,
      resumeAction: null,
      controllerStatus: null,
      phase: null,
      request: null,
      requestSequence: null,
      requestIdentity: null,
      previousRequestIdentity: null,
      lifecycleState: null,
      navigationIntent: null,
      acceptedEntryCount: 0,
      totalCount: null,
      paginationState: null,
      discardReason: null,
      reason
    });

    if (source.snapshotVersion !== 1) {
      return invalid(
        "controller_snapshot_version_invalid"
      );
    }

    const controllerState =
      source.controllerState &&
      typeof source.controllerState === "object" &&
      !Array.isArray(source.controllerState)
        ? source.controllerState
        : null;

    if (!controllerState) {
      return invalid(
        "controller_snapshot_state_missing"
      );
    }

    if (
      controllerState.isRequestControllerMapperOnly !== true ||
      controllerState.isValid !== true
    ) {
      return invalid(
        "controller_snapshot_state_invalid"
      );
    }

    const allowedStatuses = [
      "exam_result_history_request_controller_prepared",
      "exam_result_history_request_controller_pending",
      "exam_result_history_request_controller_completed",
      "exam_result_history_request_controller_navigation_ready",
      "exam_result_history_request_controller_discarded"
    ];

    if (!allowedStatuses.includes(controllerState.status)) {
      return invalid(
        "controller_snapshot_status_not_resumable"
      );
    }

    const identityState =
      mapParticipantFullExamResultHistoryRequestIdentity({
        mode: "create",
        requestSequence:
          controllerState.requestSequence,
        request:
          controllerState.request
      });

    if (
      !identityState.isValid ||
      identityState.requestIdentity !==
        controllerState.requestIdentity
    ) {
      return invalid(
        "controller_snapshot_identity_invalid"
      );
    }

    const storedLifecycleState =
      controllerState.lifecycleState &&
      typeof controllerState.lifecycleState === "object" &&
      !Array.isArray(controllerState.lifecycleState)
        ? controllerState.lifecycleState
        : null;

    if (
      !storedLifecycleState ||
      storedLifecycleState.isRequestLifecycleMapperOnly !== true ||
      storedLifecycleState.isValid !== true ||
      storedLifecycleState.requestIdentity !==
        identityState.requestIdentity
    ) {
      return invalid(
        "controller_snapshot_lifecycle_invalid"
      );
    }

    const isPreparedStatus =
      controllerState.status ===
      "exam_result_history_request_controller_prepared";

    const isPendingStatus =
      controllerState.status ===
      "exam_result_history_request_controller_pending";

    const isCompletedStatus =
      controllerState.status ===
      "exam_result_history_request_controller_completed";

    const isNavigationStatus =
      controllerState.status ===
      "exam_result_history_request_controller_navigation_ready";

    const isDiscardedStatus =
      controllerState.status ===
      "exam_result_history_request_controller_discarded";

    const flagsAreValid =
      (
        isPreparedStatus &&
        controllerState.isPrepared === true &&
        controllerState.isPending === false &&
        controllerState.isCompleted === false &&
        controllerState.isDiscarded === false &&
        controllerState.isNavigationReady === false
      ) ||
      (
        isPendingStatus &&
        controllerState.isPrepared === false &&
        controllerState.isPending === true &&
        controllerState.isCompleted === false &&
        controllerState.isDiscarded === false &&
        controllerState.isNavigationReady === false
      ) ||
      (
        isCompletedStatus &&
        controllerState.isPrepared === false &&
        controllerState.isPending === false &&
        controllerState.isCompleted === true &&
        controllerState.isDiscarded === false &&
        controllerState.isNavigationReady === false
      ) ||
      (
        isNavigationStatus &&
        controllerState.isPrepared === true &&
        controllerState.isPending === false &&
        controllerState.isCompleted === false &&
        controllerState.isDiscarded === false &&
        controllerState.isNavigationReady === true
      ) ||
      (
        isDiscardedStatus &&
        controllerState.isPrepared === false &&
        controllerState.isPending === false &&
        controllerState.isCompleted === false &&
        controllerState.isDiscarded === true &&
        controllerState.isNavigationReady === false
      );

    if (!flagsAreValid) {
      return invalid(
        "controller_snapshot_flags_invalid"
      );
    }

    const phase =
      isPreparedStatus || isNavigationStatus
        ? "prepared"
        : isPendingStatus
          ? "pending"
          : isCompletedStatus
            ? "completed"
            : "discarded";

    let lifecycleInput = {
      phase,
      requestSequence:
        identityState.requestSequence,
      request:
        identityState.request
    };

    let acceptedEntryCount = 0;
    let totalCount = null;
    let paginationState = null;
    let discardReason = null;
    let previousRequestIdentity = null;
    let navigationIntent = null;

    if (isCompletedStatus) {
      const allowedAcceptanceStatuses = [
        "exam_result_history_response_acceptance_accepted",
        "exam_result_history_response_acceptance_accepted_empty"
      ];

      if (
        controllerState.didAcceptResponse !== true ||
        !allowedAcceptanceStatuses.includes(
          controllerState.acceptanceStatus
        ) ||
        !Array.isArray(controllerState.results)
      ) {
        return invalid(
          "controller_snapshot_completion_invalid"
        );
      }

      acceptedEntryCount =
        controllerState.results.length;

      totalCount =
        controllerState.totalCount;

      if (
        !Number.isSafeInteger(totalCount) ||
        totalCount < 0 ||
        totalCount < acceptedEntryCount
      ) {
        return invalid(
          "controller_snapshot_total_count_invalid"
        );
      }

      if (
        controllerState.acceptanceStatus ===
          "exam_result_history_response_acceptance_accepted_empty" &&
        (
          acceptedEntryCount !== 0 ||
          totalCount !== 0
        )
      ) {
        return invalid(
          "controller_snapshot_empty_completion_invalid"
        );
      }

      if (
        controllerState.acceptanceStatus ===
          "exam_result_history_response_acceptance_accepted" &&
        acceptedEntryCount < 1
      ) {
        return invalid(
          "controller_snapshot_result_count_invalid"
        );
      }

      paginationState =
        mapParticipantFullExamResultHistoryPaginationState({
          limit:
            identityState.request.limit,
          offset:
            identityState.request.offset,
          totalCount,
          pageEntryCount:
            acceptedEntryCount
        });

      if (!paginationState.isValid) {
        return invalid(
          "controller_snapshot_" +
          paginationState.reason
        );
      }

      const storedPaginationState =
        controllerState.paginationState &&
        typeof controllerState.paginationState === "object" &&
        !Array.isArray(controllerState.paginationState)
          ? controllerState.paginationState
          : null;

      if (
        !storedPaginationState ||
        storedPaginationState.isValid !== true ||
        storedPaginationState.limit !==
          paginationState.limit ||
        storedPaginationState.offset !==
          paginationState.offset ||
        storedPaginationState.totalCount !==
          paginationState.totalCount ||
        storedPaginationState.pageEntryCount !==
          paginationState.pageEntryCount
      ) {
        return invalid(
          "controller_snapshot_pagination_mismatch"
        );
      }

      lifecycleInput.acceptanceState = {
        isResponseAcceptanceGuardOnly: true,
        didAcceptResponse: true,
        canAcceptResponse: true,
        requestIdentity:
          identityState.requestIdentity,
        responseIdentity:
          identityState.requestIdentity,
        status:
          controllerState.acceptanceStatus,
        results:
          controllerState.results,
        totalCount
      };
    }

    if (isDiscardedStatus) {
      discardReason =
        storedLifecycleState.discardReason;

      if (
        typeof discardReason !== "string" ||
        controllerState.reason !== discardReason
      ) {
        return invalid(
          "controller_snapshot_discard_reason_mismatch"
        );
      }

      lifecycleInput.discardReason =
        discardReason;
    }

    if (isNavigationStatus) {
      previousRequestIdentity =
        typeof controllerState.previousRequestIdentity === "string"
          ? controllerState.previousRequestIdentity.trim()
          : "";

      navigationIntent =
        typeof controllerState.navigationIntent === "string"
          ? controllerState.navigationIntent.trim()
          : "";

      const allowedNavigationIntents = [
        "first",
        "previous",
        "next",
        "retry"
      ];

      const previousParts =
        previousRequestIdentity.split(":");

      if (
        !allowedNavigationIntents.includes(
          navigationIntent
        ) ||
        previousParts.length !== 4 ||
        previousParts[0] !==
          "exam_history_request"
      ) {
        return invalid(
          "controller_snapshot_navigation_invalid"
        );
      }

      const previousSequence =
        Number(previousParts[1]);

      const previousPagination =
        normalizeParticipantExamResultHistoryPagination({
          limit:
            Number(previousParts[2]),
          offset:
            Number(previousParts[3])
        });

      const canonicalPreviousIdentity =
        "exam_history_request:" +
        previousSequence +
        ":" +
        previousPagination.limit +
        ":" +
        previousPagination.offset;

      if (
        !Number.isSafeInteger(previousSequence) ||
        previousSequence < 1 ||
        previousSequence >=
          identityState.requestSequence ||
        !previousPagination.isValid ||
        previousPagination.offset %
          previousPagination.limit !== 0 ||
        canonicalPreviousIdentity !==
          previousRequestIdentity
      ) {
        return invalid(
          "controller_snapshot_previous_identity_invalid"
        );
      }
    }

    const lifecycleState =
      mapParticipantFullExamResultHistoryRequestLifecycle(
        lifecycleInput
      );

    if (
      !lifecycleState.isValid ||
      lifecycleState.phase !== phase ||
      lifecycleState.requestIdentity !==
        identityState.requestIdentity ||
      lifecycleState.status !==
        storedLifecycleState.status
    ) {
      return invalid(
        "controller_snapshot_lifecycle_mismatch"
      );
    }

    if (
      isCompletedStatus &&
      (
        lifecycleState.acceptedEntryCount !==
          acceptedEntryCount ||
        lifecycleState.totalCount !==
          totalCount
      )
    ) {
      return invalid(
        "controller_snapshot_completion_mismatch"
      );
    }

    const canResume =
      isPreparedStatus ||
      isPendingStatus ||
      isNavigationStatus;

    const isTerminal =
      isCompletedStatus ||
      isDiscardedStatus;

    return {
      version: "v27.29r",
      status:
        canResume
          ? "exam_result_history_controller_snapshot_resumable"
          : "exam_result_history_controller_snapshot_terminal",
      snapshotVersion: 1,
      isValid: true,
      isControllerSnapshotNormalizerOnly: true,
      isLiveCall: false,
      canResume,
      isTerminal,
      resumeAction:
        isPendingStatus
          ? "retry_pending_request"
          : canResume
            ? "start_prepared_request"
            : null,
      controllerStatus:
        controllerState.status,
      phase,
      request:
        identityState.request,
      requestSequence:
        identityState.requestSequence,
      requestIdentity:
        identityState.requestIdentity,
      previousRequestIdentity,
      lifecycleState,
      navigationIntent,
      acceptedEntryCount,
      totalCount,
      paginationState,
      discardReason,
      reason: null
    };
  }

  function mapParticipantFullExamResultHistoryRequestControllerState(input) {
    const source =
      input &&
      typeof input === "object" &&
      !Array.isArray(input)
        ? input
        : {};

    const action =
      typeof source.action === "string"
        ? source.action.trim()
        : "";

    const allowedActions = [
      "initialize",
      "start",
      "accept",
      "navigate",
      "discard"
    ];

    const invalid = (reason) => ({
      version: "v27.29q",
      status: "exam_result_history_request_controller_invalid",
      action,
      isValid: false,
      isRequestControllerMapperOnly: true,
      isLiveCall: false,
      isPrepared: false,
      isPending: false,
      isCompleted: false,
      isDiscarded: false,
      isNavigationReady: false,
      didAcceptResponse: false,
      shouldIgnoreResponse: false,
      hasError: false,
      canRetry: false,
      request: null,
      requestSequence: null,
      requestIdentity: null,
      previousRequestIdentity: null,
      lifecycleState: null,
      transitionStatus: null,
      acceptanceStatus: null,
      navigationStatus: null,
      navigationIntent: null,
      results: [],
      totalCount: null,
      pageMetrics: null,
      paginationState: null,
      reason
    });

    if (!allowedActions.includes(action)) {
      return invalid(
        "request_controller_action_invalid"
      );
    }

    const createState = (overrides) => ({
      version: "v27.29q",
      status: "exam_result_history_request_controller_prepared",
      action,
      isValid: true,
      isRequestControllerMapperOnly: true,
      isLiveCall: false,
      isPrepared: false,
      isPending: false,
      isCompleted: false,
      isDiscarded: false,
      isNavigationReady: false,
      didAcceptResponse: false,
      shouldIgnoreResponse: false,
      hasError: false,
      canRetry: false,
      request: null,
      requestSequence: null,
      requestIdentity: null,
      previousRequestIdentity: null,
      lifecycleState: null,
      transitionStatus: null,
      acceptanceStatus: null,
      navigationStatus: null,
      navigationIntent: null,
      results: [],
      totalCount: null,
      pageMetrics: null,
      paginationState: null,
      reason: null,
      ...overrides
    });

    if (action === "initialize") {
      const lifecycleState =
        mapParticipantFullExamResultHistoryRequestLifecycle({
          phase: "prepared",
          requestSequence:
            source.requestSequence,
          request:
            source.request
        });

      if (!lifecycleState.isValid) {
        return invalid(lifecycleState.reason);
      }

      return createState({
        status:
          "exam_result_history_request_controller_prepared",
        isPrepared: true,
        request:
          lifecycleState.request,
        requestSequence:
          lifecycleState.requestSequence,
        requestIdentity:
          lifecycleState.requestIdentity,
        lifecycleState
      });
    }

    const currentLifecycleState =
      source.currentLifecycleState &&
      typeof source.currentLifecycleState === "object" &&
      !Array.isArray(source.currentLifecycleState)
        ? source.currentLifecycleState
        : null;

    if (!currentLifecycleState) {
      return invalid(
        "request_controller_lifecycle_state_missing"
      );
    }

    if (
      currentLifecycleState.isRequestLifecycleMapperOnly !== true ||
      currentLifecycleState.isValid !== true
    ) {
      return invalid(
        "request_controller_lifecycle_state_invalid"
      );
    }

    const currentIdentityState =
      mapParticipantFullExamResultHistoryRequestIdentity({
        mode: "create",
        requestSequence:
          currentLifecycleState.requestSequence,
        request:
          currentLifecycleState.request
      });

    if (
      !currentIdentityState.isValid ||
      currentIdentityState.requestIdentity !==
        currentLifecycleState.requestIdentity
    ) {
      return invalid(
        "request_controller_lifecycle_identity_invalid"
      );
    }

    const currentBase = {
      request:
        currentIdentityState.request,
      requestSequence:
        currentIdentityState.requestSequence,
      requestIdentity:
        currentIdentityState.requestIdentity,
      lifecycleState:
        currentLifecycleState
    };

    if (action === "start") {
      const transitionState =
        guardParticipantFullExamResultHistoryRequestLifecycleTransition({
          currentState:
            currentLifecycleState,
          targetPhase: "pending"
        });

      if (!transitionState.isValid) {
        return invalid(transitionState.reason);
      }

      if (!transitionState.canTransition) {
        return createState({
          ...currentBase,
          status:
            "exam_result_history_request_controller_blocked",
          transitionStatus:
            transitionState.status,
          reason:
            transitionState.reason
        });
      }

      return createState({
        status:
          "exam_result_history_request_controller_pending",
        isPending: true,
        request:
          transitionState.nextState.request,
        requestSequence:
          transitionState.nextState.requestSequence,
        requestIdentity:
          transitionState.nextState.requestIdentity,
        lifecycleState:
          transitionState.nextState,
        transitionStatus:
          transitionState.status
      });
    }

    if (action === "discard") {
      const transitionState =
        guardParticipantFullExamResultHistoryRequestLifecycleTransition({
          currentState:
            currentLifecycleState,
          targetPhase: "discarded",
          discardReason:
            source.discardReason
        });

      if (!transitionState.isValid) {
        return invalid(transitionState.reason);
      }

      if (!transitionState.canTransition) {
        return createState({
          ...currentBase,
          status:
            "exam_result_history_request_controller_blocked",
          transitionStatus:
            transitionState.status,
          reason:
            transitionState.reason
        });
      }

      return createState({
        status:
          "exam_result_history_request_controller_discarded",
        isDiscarded: true,
        request:
          transitionState.nextState.request,
        requestSequence:
          transitionState.nextState.requestSequence,
        requestIdentity:
          transitionState.nextState.requestIdentity,
        lifecycleState:
          transitionState.nextState,
        transitionStatus:
          transitionState.status,
        reason:
          transitionState.nextState.discardReason
      });
    }

    if (action === "accept") {
      if (currentLifecycleState.isPending !== true) {
        return createState({
          ...currentBase,
          status:
            "exam_result_history_request_controller_blocked",
          reason:
            "request_controller_accept_requires_pending"
        });
      }

      const guardInput = {
        requestSequence:
          currentIdentityState.requestSequence,
        request:
          currentIdentityState.request,
        responseIdentity:
          source.responseIdentity
      };

      Object.defineProperty(
        guardInput,
        "response",
        {
          enumerable: true,
          get() {
            return source.response;
          }
        }
      );

      const acceptanceState =
        guardParticipantFullExamResultHistoryResponseAcceptance(
          guardInput
        );

      if (acceptanceState.shouldIgnoreResponse) {
        return createState({
          ...currentBase,
          status:
            "exam_result_history_request_controller_stale_ignored",
          shouldIgnoreResponse: true,
          acceptanceStatus:
            acceptanceState.status,
          reason:
            acceptanceState.reason
        });
      }

      if (
        !acceptanceState.isValid ||
        acceptanceState.hasError ||
        acceptanceState.didAcceptResponse !== true
      ) {
        return createState({
          ...currentBase,
          status:
            "exam_result_history_request_controller_error",
          hasError: true,
          canRetry:
            acceptanceState.canRetry === true,
          acceptanceStatus:
            acceptanceState.status,
          reason:
            acceptanceState.reason
        });
      }

      const transitionState =
        guardParticipantFullExamResultHistoryRequestLifecycleTransition({
          currentState:
            currentLifecycleState,
          targetPhase: "completed",
          acceptanceState
        });

      if (
        !transitionState.isValid ||
        !transitionState.canTransition
      ) {
        return createState({
          ...currentBase,
          status:
            "exam_result_history_request_controller_error",
          hasError: true,
          transitionStatus:
            transitionState.status,
          acceptanceStatus:
            acceptanceState.status,
          reason:
            transitionState.reason
        });
      }

      return createState({
        status:
          "exam_result_history_request_controller_completed",
        isCompleted: true,
        didAcceptResponse: true,
        request:
          transitionState.nextState.request,
        requestSequence:
          transitionState.nextState.requestSequence,
        requestIdentity:
          transitionState.nextState.requestIdentity,
        lifecycleState:
          transitionState.nextState,
        transitionStatus:
          transitionState.status,
        acceptanceStatus:
          acceptanceState.status,
        results:
          acceptanceState.results,
        totalCount:
          acceptanceState.totalCount,
        pageMetrics:
          acceptanceState.pageMetrics,
        paginationState:
          acceptanceState.paginationState
      });
    }

    if (currentLifecycleState.isCompleted !== true) {
      return createState({
        ...currentBase,
        status:
          "exam_result_history_request_controller_blocked",
        reason:
          "request_controller_navigation_requires_completed"
      });
    }

    const currentDataSourceState =
      source.currentDataSourceState &&
      typeof source.currentDataSourceState === "object" &&
      !Array.isArray(source.currentDataSourceState)
        ? source.currentDataSourceState
        : null;

    if (
      !currentDataSourceState ||
      !currentDataSourceState.request ||
      currentDataSourceState.request.limit !==
        currentIdentityState.request.limit ||
      currentDataSourceState.request.offset !==
        currentIdentityState.request.offset
    ) {
      return invalid(
        "request_controller_data_source_request_mismatch"
      );
    }

    const navigationState =
      mapParticipantFullExamResultHistoryNavigationIntent({
        intent:
          source.navigationIntent,
        currentState:
          currentDataSourceState
      });

    if (!navigationState.isValid) {
      return invalid(navigationState.reason);
    }

    if (!navigationState.canNavigate) {
      return createState({
        ...currentBase,
        status:
          "exam_result_history_request_controller_blocked",
        navigationStatus:
          navigationState.status,
        navigationIntent:
          source.navigationIntent,
        reason:
          navigationState.reason
      });
    }

    if (
      !Number.isSafeInteger(
        source.nextRequestSequence
      ) ||
      source.nextRequestSequence <=
        currentIdentityState.requestSequence ||
      source.nextRequestSequence > 1000000000
    ) {
      return invalid(
        "request_controller_next_request_sequence_invalid"
      );
    }

    const nextLifecycleState =
      mapParticipantFullExamResultHistoryRequestLifecycle({
        phase: "prepared",
        requestSequence:
          source.nextRequestSequence,
        request:
          navigationState.request
      });

    if (!nextLifecycleState.isValid) {
      return invalid(nextLifecycleState.reason);
    }

    return createState({
      status:
        "exam_result_history_request_controller_navigation_ready",
      isPrepared: true,
      isNavigationReady: true,
      request:
        nextLifecycleState.request,
      requestSequence:
        nextLifecycleState.requestSequence,
      requestIdentity:
        nextLifecycleState.requestIdentity,
      previousRequestIdentity:
        currentIdentityState.requestIdentity,
      lifecycleState:
        nextLifecycleState,
      navigationStatus:
        navigationState.status,
      navigationIntent:
        source.navigationIntent
    });
  }

  function guardParticipantFullExamResultHistoryRequestLifecycleTransition(input) {
    const source =
      input &&
      typeof input === "object" &&
      !Array.isArray(input)
        ? input
        : {};

    const targetPhase =
      typeof source.targetPhase === "string"
        ? source.targetPhase.trim()
        : "";

    const invalid = (reason) => ({
      version: "v27.29p",
      status: "exam_result_history_request_transition_invalid",
      isValid: false,
      isRequestLifecycleTransitionGuardOnly: true,
      isLiveCall: false,
      canTransition: false,
      didTransition: false,
      isTerminalTransition: false,
      fromPhase: null,
      toPhase: targetPhase || null,
      requestIdentity: null,
      nextState: null,
      reason
    });

    const currentState =
      source.currentState &&
      typeof source.currentState === "object" &&
      !Array.isArray(source.currentState)
        ? source.currentState
        : null;

    if (!currentState) {
      return invalid(
        "request_transition_current_state_missing"
      );
    }

    if (
      currentState.isRequestLifecycleMapperOnly !== true ||
      currentState.isValid !== true
    ) {
      return invalid(
        "request_transition_current_state_invalid"
      );
    }

    const identityState =
      mapParticipantFullExamResultHistoryRequestIdentity({
        mode: "create",
        requestSequence:
          currentState.requestSequence,
        request:
          currentState.request
      });

    if (
      !identityState.isValid ||
      identityState.requestIdentity !==
        currentState.requestIdentity
    ) {
      return invalid(
        "request_transition_current_identity_invalid"
      );
    }

    const fromPhase =
      typeof currentState.phase === "string"
        ? currentState.phase.trim()
        : "";

    const allowedPhases = [
      "prepared",
      "pending",
      "completed",
      "discarded"
    ];

    if (
      !allowedPhases.includes(fromPhase) ||
      !allowedPhases.includes(targetPhase)
    ) {
      return invalid(
        "request_transition_phase_invalid"
      );
    }

    const phaseFlagsAreValid =
      (
        fromPhase === "prepared" &&
        currentState.isPrepared === true &&
        currentState.isPending === false &&
        currentState.isCompleted === false &&
        currentState.isDiscarded === false
      ) ||
      (
        fromPhase === "pending" &&
        currentState.isPrepared === false &&
        currentState.isPending === true &&
        currentState.isCompleted === false &&
        currentState.isDiscarded === false
      ) ||
      (
        fromPhase === "completed" &&
        currentState.isPrepared === false &&
        currentState.isPending === false &&
        currentState.isCompleted === true &&
        currentState.isDiscarded === false
      ) ||
      (
        fromPhase === "discarded" &&
        currentState.isPrepared === false &&
        currentState.isPending === false &&
        currentState.isCompleted === false &&
        currentState.isDiscarded === true
      );

    if (!phaseFlagsAreValid) {
      return invalid(
        "request_transition_current_flags_invalid"
      );
    }

    const allowedTransitions = {
      prepared: [
        "pending",
        "discarded"
      ],
      pending: [
        "completed",
        "discarded"
      ],
      completed: [],
      discarded: []
    };

    if (
      !allowedTransitions[fromPhase].includes(
        targetPhase
      )
    ) {
      return {
        version: "v27.29p",
        status: "exam_result_history_request_transition_blocked",
        isValid: true,
        isRequestLifecycleTransitionGuardOnly: true,
        isLiveCall: false,
        canTransition: false,
        didTransition: false,
        isTerminalTransition:
          fromPhase === "completed" ||
          fromPhase === "discarded",
        fromPhase,
        toPhase: targetPhase,
        requestIdentity:
          identityState.requestIdentity,
        nextState: null,
        reason:
          fromPhase === "completed" ||
          fromPhase === "discarded"
            ? "request_transition_terminal_state"
            : "request_transition_not_allowed"
      };
    }

    const lifecycleInput = {
      phase: targetPhase,
      requestSequence:
        identityState.requestSequence,
      request:
        identityState.request
    };

    if (targetPhase === "completed") {
      lifecycleInput.acceptanceState =
        source.acceptanceState;
    }

    if (targetPhase === "discarded") {
      lifecycleInput.discardReason =
        source.discardReason;
    }

    const nextState =
      mapParticipantFullExamResultHistoryRequestLifecycle(
        lifecycleInput
      );

    if (!nextState.isValid) {
      return invalid(nextState.reason);
    }

    if (
      nextState.requestIdentity !==
      identityState.requestIdentity
    ) {
      return invalid(
        "request_transition_next_identity_mismatch"
      );
    }

    return {
      version: "v27.29p",
      status: "exam_result_history_request_transition_ready",
      isValid: true,
      isRequestLifecycleTransitionGuardOnly: true,
      isLiveCall: false,
      canTransition: true,
      didTransition: true,
      isTerminalTransition:
        targetPhase === "completed" ||
        targetPhase === "discarded",
      fromPhase,
      toPhase: targetPhase,
      requestIdentity:
        identityState.requestIdentity,
      nextState,
      reason: null
    };
  }

  function mapParticipantFullExamResultHistoryRequestLifecycle(input) {
    const source =
      input &&
      typeof input === "object" &&
      !Array.isArray(input)
        ? input
        : {};

    const phase =
      typeof source.phase === "string"
        ? source.phase.trim()
        : "";

    const allowedPhases = [
      "prepared",
      "pending",
      "completed",
      "discarded"
    ];

    const invalid = (reason) => ({
      version: "v27.29o",
      status: "exam_result_history_request_lifecycle_invalid",
      phase,
      isValid: false,
      isRequestLifecycleMapperOnly: true,
      isLiveCall: false,
      isPrepared: false,
      isPending: false,
      isCompleted: false,
      isDiscarded: false,
      canStart: false,
      canComplete: false,
      canDiscard: false,
      request: null,
      requestSequence: null,
      requestIdentity: null,
      acceptanceStatus: null,
      acceptedEntryCount: 0,
      totalCount: null,
      discardReason: null,
      reason
    });

    if (!allowedPhases.includes(phase)) {
      return invalid(
        "request_lifecycle_phase_invalid"
      );
    }

    const identityState =
      mapParticipantFullExamResultHistoryRequestIdentity({
        mode: "create",
        requestSequence: source.requestSequence,
        request: source.request
      });

    if (!identityState.isValid) {
      return invalid(identityState.reason);
    }

    const createState = (overrides) => ({
      version: "v27.29o",
      status: "exam_result_history_request_lifecycle_prepared",
      phase,
      isValid: true,
      isRequestLifecycleMapperOnly: true,
      isLiveCall: false,
      isPrepared: false,
      isPending: false,
      isCompleted: false,
      isDiscarded: false,
      canStart: false,
      canComplete: false,
      canDiscard: false,
      request: identityState.request,
      requestSequence:
        identityState.requestSequence,
      requestIdentity:
        identityState.requestIdentity,
      acceptanceStatus: null,
      acceptedEntryCount: 0,
      totalCount: null,
      discardReason: null,
      reason: null,
      ...overrides
    });

    if (phase === "prepared") {
      return createState({
        status:
          "exam_result_history_request_lifecycle_prepared",
        isPrepared: true,
        canStart: true
      });
    }

    if (phase === "pending") {
      return createState({
        status:
          "exam_result_history_request_lifecycle_pending",
        isPending: true,
        canComplete: true,
        canDiscard: true
      });
    }

    if (phase === "discarded") {
      const discardReason =
        typeof source.discardReason === "string"
          ? source.discardReason.trim()
          : "";

      const allowedDiscardReasons = [
        "cancelled_before_response",
        "superseded_by_new_request",
        "stale_response_ignored"
      ];

      if (
        !allowedDiscardReasons.includes(
          discardReason
        )
      ) {
        return invalid(
          "request_lifecycle_discard_reason_invalid"
        );
      }

      return createState({
        status:
          "exam_result_history_request_lifecycle_discarded",
        isDiscarded: true,
        discardReason
      });
    }

    const acceptanceState =
      source.acceptanceState &&
      typeof source.acceptanceState === "object" &&
      !Array.isArray(source.acceptanceState)
        ? source.acceptanceState
        : null;

    if (!acceptanceState) {
      return invalid(
        "request_lifecycle_acceptance_state_missing"
      );
    }

    if (
      acceptanceState.isResponseAcceptanceGuardOnly !== true ||
      acceptanceState.didAcceptResponse !== true ||
      acceptanceState.canAcceptResponse !== true
    ) {
      return invalid(
        "request_lifecycle_acceptance_state_invalid"
      );
    }

    if (
      acceptanceState.requestIdentity !==
        identityState.requestIdentity ||
      acceptanceState.responseIdentity !==
        identityState.requestIdentity
    ) {
      return invalid(
        "request_lifecycle_acceptance_identity_mismatch"
      );
    }

    const allowedAcceptanceStatuses = [
      "exam_result_history_response_acceptance_accepted",
      "exam_result_history_response_acceptance_accepted_empty"
    ];

    if (
      !allowedAcceptanceStatuses.includes(
        acceptanceState.status
      )
    ) {
      return invalid(
        "request_lifecycle_acceptance_status_invalid"
      );
    }

    const acceptedEntryCount =
      Array.isArray(acceptanceState.results)
        ? acceptanceState.results.length
        : 0;

    const totalCount =
      acceptanceState.totalCount === null ||
      Number.isSafeInteger(
        acceptanceState.totalCount
      )
        ? acceptanceState.totalCount
        : null;

    if (
      acceptanceState.totalCount !== null &&
      totalCount === null
    ) {
      return invalid(
        "request_lifecycle_total_count_invalid"
      );
    }

    return createState({
      status:
        "exam_result_history_request_lifecycle_completed",
      isCompleted: true,
      acceptanceStatus:
        acceptanceState.status,
      acceptedEntryCount,
      totalCount
    });
  }

  function guardParticipantFullExamResultHistoryResponseAcceptance(input) {
    const source =
      input &&
      typeof input === "object" &&
      !Array.isArray(input)
        ? input
        : {};

    const identityState =
      mapParticipantFullExamResultHistoryRequestIdentity({
        mode: "compare",
        requestSequence: source.requestSequence,
        request: source.request,
        responseIdentity: source.responseIdentity
      });

    const createState = (overrides) => ({
      version: "v27.29n",
      status: "exam_result_history_response_acceptance_invalid",
      isValid: false,
      isResponseAcceptanceGuardOnly: true,
      isLiveCall: false,
      canAcceptResponse: false,
      didAcceptResponse: false,
      shouldIgnoreResponse: false,
      hasError: false,
      canRetry: false,
      request: identityState.request,
      requestIdentity:
        identityState.requestIdentity,
      responseIdentity:
        identityState.responseIdentity,
      identityStatus: identityState.status,
      dataSourceStatus: null,
      results: [],
      totalCount: null,
      pageMetrics: null,
      paginationState: null,
      reason: null,
      ...overrides
    });

    if (!identityState.isValid) {
      return createState({
        reason: identityState.reason
      });
    }

    if (identityState.isStaleResponse) {
      return createState({
        status:
          "exam_result_history_response_acceptance_stale_ignored",
        isValid: true,
        shouldIgnoreResponse: true,
        reason:
          "stale_response_ignored"
      });
    }

    if (
      identityState.canApplyResponse !== true ||
      identityState.isCurrentResponse !== true
    ) {
      return createState({
        reason:
          "response_identity_not_applicable"
      });
    }

    const dataSourceState =
      orchestrateParticipantFullExamResultHistoryDataSourceState({
        phase: "resolved",
        limit: identityState.request.limit,
        offset: identityState.request.offset,
        response: source.response
      });

    if (dataSourceState.hasError) {
      return createState({
        status:
          "exam_result_history_response_acceptance_error",
        hasError: true,
        canRetry: dataSourceState.canRetry,
        dataSourceStatus:
          dataSourceState.status,
        reason:
          dataSourceState.reason
      });
    }

    if (dataSourceState.isEmpty) {
      return createState({
        status:
          "exam_result_history_response_acceptance_accepted_empty",
        isValid: true,
        canAcceptResponse: true,
        didAcceptResponse: true,
        dataSourceStatus:
          dataSourceState.status,
        results: [],
        totalCount:
          dataSourceState.totalCount,
        pageMetrics:
          dataSourceState.pageMetrics,
        paginationState:
          dataSourceState.paginationState
      });
    }

    if (
      dataSourceState.isSuccess &&
      dataSourceState.hasData
    ) {
      return createState({
        status:
          "exam_result_history_response_acceptance_accepted",
        isValid: true,
        canAcceptResponse: true,
        didAcceptResponse: true,
        dataSourceStatus:
          dataSourceState.status,
        results:
          dataSourceState.results,
        totalCount:
          dataSourceState.totalCount,
        pageMetrics:
          dataSourceState.pageMetrics,
        paginationState:
          dataSourceState.paginationState
      });
    }

    return createState({
      status:
        "exam_result_history_response_acceptance_error",
      hasError: true,
      canRetry: false,
      dataSourceStatus:
        dataSourceState.status,
      reason:
        "data_source_state_not_acceptable"
    });
  }

  function mapParticipantFullExamResultHistoryRequestIdentity(input) {
    const source =
      input &&
      typeof input === "object" &&
      !Array.isArray(input)
        ? input
        : {};

    const mode =
      typeof source.mode === "string"
        ? source.mode.trim()
        : "create";

    const allowedModes = [
      "create",
      "compare"
    ];

    const invalid = (reason) => ({
      version: "v27.29m",
      status: "exam_result_history_request_identity_invalid",
      mode,
      isValid: false,
      isRequestIdentityMapperOnly: true,
      isLiveCall: false,
      canApplyResponse: false,
      isCurrentResponse: false,
      isStaleResponse: false,
      request: null,
      requestSequence: null,
      requestIdentity: null,
      responseIdentity: null,
      reason
    });

    if (!allowedModes.includes(mode)) {
      return invalid(
        "request_identity_mode_invalid"
      );
    }

    const request =
      source.request &&
      typeof source.request === "object" &&
      !Array.isArray(source.request)
        ? source.request
        : null;

    if (!request) {
      return invalid(
        "request_identity_request_missing"
      );
    }

    const normalizedRequest =
      normalizeParticipantExamResultHistoryPagination({
        limit: request.limit,
        offset: request.offset
      });

    if (
      !normalizedRequest.isValid ||
      normalizedRequest.offset %
        normalizedRequest.limit !== 0
    ) {
      return invalid(
        "request_identity_request_invalid"
      );
    }

    if (
      !Number.isSafeInteger(
        source.requestSequence
      ) ||
      source.requestSequence < 1 ||
      source.requestSequence > 1000000000
    ) {
      return invalid(
        "request_sequence_invalid"
      );
    }

    const requestSequence =
      source.requestSequence;

    const requestIdentity =
      "exam_history_request:" +
      requestSequence +
      ":" +
      normalizedRequest.limit +
      ":" +
      normalizedRequest.offset;

    if (mode === "create") {
      return {
        version: "v27.29m",
        status: "exam_result_history_request_identity_ready",
        mode,
        isValid: true,
        isRequestIdentityMapperOnly: true,
        isLiveCall: false,
        canApplyResponse: false,
        isCurrentResponse: false,
        isStaleResponse: false,
        request: {
          limit: normalizedRequest.limit,
          offset: normalizedRequest.offset
        },
        requestSequence,
        requestIdentity,
        responseIdentity: null,
        reason: null
      };
    }

    const responseIdentity =
      typeof source.responseIdentity === "string"
        ? source.responseIdentity.trim()
        : "";

    const responseIdentityMatch =
      /^exam_history_request:(\d{1,10}):(\d{1,2}):(\d{1,5})$/
        .exec(responseIdentity);

    if (!responseIdentityMatch) {
      return invalid(
        "response_identity_format_invalid"
      );
    }

    const responseSequence =
      Number(responseIdentityMatch[1]);

    const responseLimit =
      Number(responseIdentityMatch[2]);

    const responseOffset =
      Number(responseIdentityMatch[3]);

    if (
      !Number.isSafeInteger(responseSequence) ||
      responseSequence < 1 ||
      responseSequence > 1000000000
    ) {
      return invalid(
        "response_identity_sequence_invalid"
      );
    }

    const normalizedResponseRequest =
      normalizeParticipantExamResultHistoryPagination({
        limit: responseLimit,
        offset: responseOffset
      });

    if (
      !normalizedResponseRequest.isValid ||
      normalizedResponseRequest.offset %
        normalizedResponseRequest.limit !== 0
    ) {
      return invalid(
        "response_identity_request_invalid"
      );
    }

    const canonicalResponseIdentity =
      "exam_history_request:" +
      responseSequence +
      ":" +
      normalizedResponseRequest.limit +
      ":" +
      normalizedResponseRequest.offset;

    if (
      canonicalResponseIdentity !==
      responseIdentity
    ) {
      return invalid(
        "response_identity_noncanonical"
      );
    }

    const isCurrentResponse =
      responseIdentity === requestIdentity;

    return {
      version: "v27.29m",
      status:
        isCurrentResponse
          ? "exam_result_history_response_identity_current"
          : "exam_result_history_response_identity_stale",
      mode,
      isValid: true,
      isRequestIdentityMapperOnly: true,
      isLiveCall: false,
      canApplyResponse: isCurrentResponse,
      isCurrentResponse,
      isStaleResponse: !isCurrentResponse,
      request: {
        limit: normalizedRequest.limit,
        offset: normalizedRequest.offset
      },
      requestSequence,
      requestIdentity,
      responseIdentity,
      reason:
        isCurrentResponse
          ? null
          : "response_identity_does_not_match_active_request"
    };
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
    version: "v27.30r",
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
    mapParticipantFullExamResultHistoryRequestIdentity,
    mapParticipantFullExamResultHistoryRequestLifecycle,
    mapParticipantFullExamResultHistoryRequestControllerState,
    normalizeParticipantFullExamResultHistoryControllerSnapshot,
    mapParticipantFullExamResultHistorySnapshotResumeState,
    mapParticipantFullExamResultHistorySnapshotCreationState,
    mapParticipantFullExamResultHistorySnapshotSerializationState,
    mapParticipantFullExamResultHistorySnapshotDeserializationState,
    mapParticipantFullExamResultHistorySnapshotPersistenceContract,
    mapParticipantFullExamResultHistorySnapshotStorageAdapterReadiness,
    mapParticipantFullExamResultHistorySnapshotPersistenceOperationPlan,
    mapParticipantFullExamResultHistorySnapshotPersistenceOperationReleaseState,
    guardParticipantFullExamResultHistorySnapshotPersistenceExecution,
    mapParticipantFullExamResultHistorySnapshotPersistenceInvocationContract,
    mapParticipantFullExamResultHistorySnapshotPersistenceInvocationPackageState,
    mapParticipantFullExamResultHistorySnapshotPersistenceResultContract,
    guardParticipantFullExamResultHistorySnapshotPersistenceResultAcceptance,
    mapParticipantFullExamResultHistorySnapshotPersistenceCompletionState,
    mapParticipantFullExamResultHistorySnapshotPersistenceCycleState,
    guardParticipantFullExamResultHistorySnapshotPersistenceCycleRepetition,
    mapParticipantFullExamResultHistorySnapshotPersistenceCycleRegistryState,
    mapParticipantFullExamResultHistorySnapshotPersistenceCycleRegistrySerializationState,
    mapParticipantFullExamResultHistorySnapshotPersistenceCycleRegistryDeserializationState,
    mapParticipantFullExamResultHistorySnapshotPersistenceCycleRegistryContract,
    mapParticipantFullExamResultHistorySnapshotPersistenceCycleRegistryStorageAdapterReadinessState,
    mapParticipantFullExamResultHistorySnapshotPersistenceCycleRegistryOperationPlanState,
    mapParticipantFullExamResultHistorySnapshotPersistenceCycleRegistryOperationReleaseState,
    guardParticipantFullExamResultHistorySnapshotPersistenceCycleRegistryExecution,
    mapParticipantFullExamResultHistorySnapshotPersistenceCycleRegistryInvocationContract,
    mapParticipantFullExamResultHistorySnapshotPersistenceCycleRegistryInvocationPackageState,
    guardParticipantFullExamResultHistoryRequestLifecycleTransition,
    guardParticipantFullExamResultHistoryResponseAcceptance,
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
