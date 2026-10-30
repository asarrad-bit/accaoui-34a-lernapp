"use strict";
// Actual existing root app/local source UI. No AI service, DB/Auth or physical-device acceptance.
const fs = require("node:fs"), path = require("node:path"), http = require("node:http"), crypto = require("node:crypto"), assert = require("node:assert/strict");
const cfg = JSON.parse(fs.readFileSync(process.argv[2], "utf8"));
const root = path.resolve(cfg.root), out = path.resolve(cfg.output), origin = "http://127.0.0.1:8786";
const hash = bytes => crypto.createHash("sha256").update(bytes).digest("hex");
const pin = file => { const bytes = fs.readFileSync(file); return { bytes: bytes.length, sha256: hash(bytes) }; };
assert.equal(root.toLowerCase(), "c:\\xampp\\htdocs\\accaoui\\v4-dashboard");
assert.equal(cfg.task, "ACCAOUI_DEVELOPMENT_SEQUENCE_W07");
assert.ok(out.toLowerCase().startsWith(path.resolve(cfg.evidenceDirectory).toLowerCase() + path.sep));
assert.ok(!fs.existsSync(out), "preserve every earlier attempt");
const manifest = JSON.parse(fs.readFileSync(cfg.manifestPath));
assert.equal(hash(fs.readFileSync(cfg.manifestPath)), cfg.manifestSHA256);
assert.equal(manifest.task, cfg.task); assert.equal(manifest.base, "96cf711cf1718aa75036ae3b87dbb047283107d6");
const written = JSON.parse(fs.readFileSync(path.join(root, "questions.json")));
const firstWritten = written.find(row => row.id === "roso_001"); assert.ok(firstWritten?.explanation);
const save = (name, value) => fs.writeFileSync(path.join(out, name), JSON.stringify(value, null, 2) + "\n", { flag: "wx" });
const transportQualification = manifest.browserVisibleFocusRepair.transportDiagnostic;
assert.deepEqual(pin(transportQualification.path), { bytes: transportQualification.bytes, sha256: transportQualification.sha256 });
const qualifiedColdRoot = JSON.parse(fs.readFileSync(transportQualification.path));
assert.equal(qualifiedColdRoot.failure, null); assert.equal(qualifiedColdRoot.fabricatedResponses, 0);
assert.deepEqual(qualifiedColdRoot.pageErrors, []); assert.deepEqual(qualifiedColdRoot.externalRequests, []);
assert.equal(qualifiedColdRoot.boot.configState.isConfigured, false); assert.equal(qualifiedColdRoot.boot.autoload, false); assert.equal(qualifiedColdRoot.boot.clientPresent, false);
assert.ok(qualifiedColdRoot.failures.some(row => row.phase === "cold-root-before-any-helper-action" && row.path === "/data/supabase-config.local.js" && row.method === "GET" && row.resourceType === "fetch" && row.responseStatus === 404 && row.error === "net::ERR_ABORTED"));
assert.ok(qualifiedColdRoot.nativeCdpEvents.some(row => row.kind === "response" && row.status === 404));
assert.ok(qualifiedColdRoot.nativeCdpEvents.some(row => row.kind === "loadingFailed" && row.canceled === true && row.blockedReason === null && row.corsErrorStatus === null));
const rows = [], pageErrors = [], externalRequests = [], requests = [], failures = [], serviceWorkers = [], requestFailureReads = [];
let qualifiedMissingConfigCancellations = [], actualOfflineSourceFailures = [], unexpectedRequestFailures = [];
let browser, server, phase = "setup", failure = null;
function exact() {
  assert.equal(hash(fs.readFileSync(cfg.manifestPath)), cfg.manifestSHA256);
  for (const [rel, expected] of Object.entries(manifest.candidate)) assert.deepEqual(pin(path.join(root, rel)), expected, rel);
  for (const [rel, expected] of Object.entries(cfg.servedFiles)) assert.deepEqual(pin(path.join(root, rel)), expected, rel);
  assert.deepEqual(pin(cfg.browserExecutable), cfg.browserPin);
  assert.deepEqual(pin(process.execPath), cfg.nodePin);
}
async function check(id, fn) {
  exact(); phase = id;
  const row = { id, status: "RUNNING", startedUtc: new Date().toISOString() }; rows.push(row);
  try { row.evidence = await fn(); row.status = "PASS"; }
  catch (error) { row.status = "FAIL"; row.error = { type: error.name, message: error.message.slice(0, 500) }; throw error; }
  finally {
    row.endedUtc = new Date().toISOString();
    const fd = fs.openSync(path.join(out, "checkpoints.jsonl"), "a");
    try { fs.writeSync(fd, JSON.stringify({ id, status: row.status, endedUtc: row.endedUtc, manifestSHA256: cfg.manifestSHA256 }) + "\n"); fs.fsyncSync(fd); }
    finally { fs.closeSync(fd); }
  }
}
const storage = page => page.evaluate(() => Object.fromEntries(Object.keys(localStorage).sort().map(key => [key, localStorage.getItem(key)])));
async function home(page) {
  await page.goto(origin, { waitUntil: "networkidle" });
  await page.waitForFunction(() => typeof allQuestions !== "undefined" && allQuestions.length === 86 && document.querySelector("#mobileBottomNavV227") && document.querySelector("#learningAssistanceOpenV1"));
  await page.evaluate(async () => { if (typeof participantAppBootPromiseV2737F !== "undefined" && participantAppBootPromiseV2737F) await participantAppBootPromiseV2737F; });
  await page.waitForLoadState("networkidle");
}
async function open(page, mobile) {
  if (mobile) {
    await page.locator('[data-mobile-target="more"]').click();
    await page.locator("#learningAssistanceMobileOpenV1").click();
  } else await page.locator("#learningAssistanceOpenV1").click();
  await page.locator("#learningAssistanceDialogV1").waitFor({ state: "visible" });
  await ready(page);
}
async function ready(page) {
  await page.waitForFunction(() => document.querySelector("#learningAssistanceSearchV1")?.disabled === false && !document.querySelector("#learningAssistanceStatusV1").textContent.includes("werden geprüft"));
}
async function query(page, value, kind = "written") {
  await page.locator("#learningAssistanceKindV1").selectOption(kind);
  await page.locator("#learningAssistanceQueryV1").fill(value);
  await page.locator("#learningAssistanceSearchV1").click();
}
async function clearClose(page) {
  if (await page.locator("#learningAssistanceDialogV1").evaluate(node => node.open)) {
    await page.locator("#learningAssistanceClearV1").click();
    await page.locator("#learningAssistanceCloseV1").click();
  }
}
function observe(page, profile) {
  page.setDefaultTimeout(12000);
  page.on("pageerror", error => pageErrors.push({ profile, phase, error: String(error) }));
  page.on("requestfailed", request => {
    const row = { profile, phase, path: new URL(request.url()).pathname, failure: request.failure()?.errorText, method: request.method(), resourceType: request.resourceType(), responseStatus: null };
    failures.push(row);
    requestFailureReads.push(request.response().then(response => { row.responseStatus = response?.status() ?? null; }, error => { row.responseReadError = String(error); }));
  });
}
async function profileFlow(profile) {
  const ctx = await browser.newContext({ viewport: profile.viewport, isMobile: profile.mobile, locale: "de-DE", timezoneId: "Europe/Berlin" });
  ctx.on("serviceworker", worker => serviceWorkers.push(worker.url()));
  await ctx.route("**/*", route => {
    if (new URL(route.request().url()).origin === origin) return route.continue();
    externalRequests.push({ profile: profile.id, phase, url: route.request().url() }); return route.abort("blockedbyclient");
  });
  const page = await ctx.newPage(); observe(page, profile.id);
  try {
    await home(page);
    // Create a real anonymous learning answer through existing UI before the read-only source workflow.
    await page.locator("#openQuestionsCard").click();
    await page.locator("#questionArea .answer-btn").first().waitFor({ state: "visible" });
    const graded = await page.evaluate(() => ({ id: currentQuestions[currentQuestionIndex].id, correct: [...currentQuestions[currentQuestionIndex].correct] }));
    for (const index of graded.correct) await page.locator('#questionArea .answer-btn[data-index="' + index + '"]').click();
    await home(page);
    const previousStorage = await storage(page);
    assert.ok(Object.keys(previousStorage).length > 0, "real previous learning storage exists");
    assert.ok(Object.hasOwn(JSON.parse(previousStorage.accaoui_answered_questions), graded.id), "native learning answer really persisted");
    const prefix = profile.id + ":";
    await check(prefix + "original-root-and-real-learning-state-loaded", async () => {
      const data = await page.evaluate(() => ({ questions: allQuestions.length, oral: AccaouiOralQuestionBank.listQuestions().length, flags: [...document.querySelectorAll('script[data-enabled="false"]')].length, configState: getSupabaseConfigState(), autoload: ACCAOUI_SUPABASE_CONFIG_LOADER.isAutoLoadEnabled(), liveEnabled: window.ACCAOUI_SUPABASE_LIVE_ENABLED === true, initConfirmed: window.ACCAOUI_SUPABASE_CLIENT_INIT_CONFIRMED === true, clientPresent: !!window.ACCAOUI_SUPABASE_CLIENT }));
      assert.equal(data.questions, 86); assert.equal(data.oral, 15); assert.ok(data.flags >= 2);
      assert.equal(data.configState.isConfigured, false); assert.equal(data.autoload, false); assert.equal(data.liveEnabled, false); assert.equal(data.initConfirmed, false); assert.equal(data.clientPresent, false);
      return { ...data, previousRealGradedQuestionId: graded.id, existingStorageKeys: Object.keys(previousStorage) };
    });
    await check(prefix + "native-source-entry-loads-exact-current-files", async () => {
      await open(page, profile.mobile);
      assert.match(await page.locator("#learningAssistanceStatusV1").innerText(), /86 schriftliche und 15 mündliche/);
      return { actualNativeButton: profile.mobile ? "existing mobile More menu entry" : "existing desktop account tools entry", sourceFileHashes: { written: cfg.servedFiles["questions.json"].sha256, oral: cfg.servedFiles["data/oral-question-bank.js"].sha256 } };
    });
    await check(prefix + "written-explanation-remains-literal-source", async () => {
      await query(page, firstWritten.id); assert.equal(await page.locator("#learningAssistanceResultsV1 button").count(), 1);
      await page.locator('[data-source-id="' + firstWritten.id + '"]').click();
      const answer = await page.locator("#learningAssistanceAnswerV1").innerText();
      assert.ok(answer.includes(firstWritten.question) && answer.includes(firstWritten.explanation));
      assert.ok(answer.includes("Keine amtliche Bewertung oder Bestehensprognose"));
      return { sourceId: firstWritten.id, exactExplanationSHA256: hash(Buffer.from(firstWritten.explanation)) };
    });
    await check(prefix + "citation-displays-actual-type-id-file-and-revision", async () => {
      await page.locator("#learningAssistanceAnswerV1 summary").click();
      const text = await page.locator("#learningAssistanceAnswerV1 details").innerText();
      assert.ok(text.includes("Schriftlich") && text.includes(firstWritten.id) && text.includes("questions.json") && text.includes(cfg.servedFiles["questions.json"].sha256));
      return { displayedSourceSHA256: cfg.servedFiles["questions.json"].sha256 };
    });
    await check(prefix + "oral-bank-stays-distinct-and-literal", async () => {
      await query(page, "oral_a_001", "oral"); assert.equal(await page.locator("#learningAssistanceResultsV1 button").count(), 1);
      await page.locator('[data-source-id="oral_a_001"]').click();
      const original = await page.evaluate(() => AccaouiOralQuestionBank.getQuestionById("oral_a_001").sampleAnswer);
      assert.ok((await page.locator("#learningAssistanceAnswerV1").innerText()).includes(original));
      assert.match(await page.locator("#learningAssistanceAnswerV1").innerText(), /Vorhandene Musterantwort/);
      await query(page, firstWritten.id, "oral"); assert.equal(await page.locator("#learningAssistanceResultsV1 button").count(), 0);
      return { sourceId: "oral_a_001", sampleAnswerSHA256: hash(Buffer.from(original)), writtenIdNotMergedIntoOral: true };
    });
    await check(prefix + "unknown-query-never-creates-answer-or-citation", async () => {
      await query(page, "missing-source-" + cfg.runId);
      assert.equal(await page.locator("#learningAssistanceResultsV1 button").count(), 0);
      assert.equal(await page.locator("#learningAssistanceAnswerV1").textContent(), "");
      assert.match(await page.locator("#learningAssistanceStatusV1").innerText(), /Es wird keine Erklärung erfunden/);
    });
    await check(prefix + "native-query-input-is-bounded-and-inert", async () => {
      assert.equal(await page.locator("#learningAssistanceQueryV1").getAttribute("maxlength"), "240");
      await query(page, '<img src="x" onerror="window.unwanted=true">');
      assert.equal(await page.evaluate(() => window.unwanted), undefined);
      assert.equal(await page.locator("#learningAssistanceDialogV1 img").count(), 0);
      assert.equal(await page.locator("#learningAssistanceAnswerV1").textContent(), "");
    });
    await check(prefix + "close-reopen-preserves-query-and-rechecks-sources", async () => {
      await query(page, firstWritten.id); await page.locator("#learningAssistanceCloseV1").click();
      await open(page, profile.mobile);
      assert.equal(await page.locator("#learningAssistanceQueryV1").inputValue(), firstWritten.id);
      assert.equal(await page.locator('[data-source-id="' + firstWritten.id + '"]').count(), 1);
    });
    await check(prefix + "existing-root-scope-guard-retains-unsent-input", async () => {
      const denied = await page.evaluate(() => { try { prepareParticipantScopeChangeV1(); return null; } catch (error) { return error.code; } });
      assert.equal(denied, "pending_form_input"); assert.equal(await page.locator("#learningAssistanceQueryV1").inputValue(), firstWritten.id);
      await page.locator("#learningAssistanceClearV1").click();
      assert.equal(await page.evaluate(() => { try { prepareParticipantScopeChangeV1(); return "allowed"; } catch (error) { return error.code; } }), "allowed");
      assert.equal(await page.locator("#learningAssistanceDialogV1").evaluate(node => node.open), false);
      await open(page, profile.mobile);
      return { actualOriginalRootTransitionGuardInvoked: true, realAuthAccountSwitchClaim: false };
    });
    await check(prefix + "actual-offline-source-failure-and-reconnect-retain-query", async () => {
      await query(page, firstWritten.id); await ctx.setOffline(true);
      await page.locator("#learningAssistanceReloadV1").click(); await ready(page);
      assert.match(await page.locator("#learningAssistanceStatusV1").innerText(), /konnten nicht geladen/);
      assert.equal(await page.locator("#learningAssistanceQueryV1").inputValue(), firstWritten.id);
      assert.equal(await page.locator("#learningAssistanceAnswerV1").textContent(), "");
      await ctx.setOffline(false); await page.locator("#learningAssistanceReloadV1").click(); await ready(page);
      assert.equal(await page.locator('[data-source-id="' + firstWritten.id + '"]').count(), 1);
      await page.waitForLoadState("networkidle");
      return { actualBrowserOfflineSwitch: true, fabricatedHttpResponses: 0 };
    });
    await check(prefix + "corrupted-real-runtime-oral-snapshot-is-rejected", async () => {
      await page.evaluate(() => { AccaouiOralQuestionBank.getQuestionById("oral_a_001").question += " synthetic runtime drift"; });
      await page.locator("#learningAssistanceReloadV1").click(); await ready(page);
      assert.match(await page.locator("#learningAssistanceStatusV1").innerText(), /passt nicht zum geprüften Dateistand/);
      assert.equal(await page.locator("#learningAssistanceAnswerV1").textContent(), "");
      assert.equal(await page.locator("#learningAssistanceQueryV1").inputValue(), firstWritten.id);
      await clearClose(page); await home(page); await open(page, profile.mobile);
      assert.match(await page.locator("#learningAssistanceStatusV1").innerText(), /86 schriftliche und 15 mündliche/);
      return { controlledRuntimeDataCorruption: true, sourceFileChanges: 0, restoredByOriginalRootReload: true };
    });
    await check(prefix + "all-previous-real-native-learning-storage-bytes-preserved", async () => {
      assert.deepEqual(await storage(page), previousStorage);
      return { originalStorageValuesSHA256: hash(Buffer.from(JSON.stringify(previousStorage))), keys: Object.keys(previousStorage) };
    });
    await check(prefix + "native-keyboard-search-escape-and-visible-focus-return", async () => {
      await page.locator("#learningAssistanceKindV1").selectOption("written");
      await page.locator("#learningAssistanceQueryV1").fill(firstWritten.id); await page.locator("#learningAssistanceQueryV1").focus();
      await page.keyboard.press("Enter"); assert.equal(await page.locator('[data-source-id="' + firstWritten.id + '"]').count(), 1);
      await page.keyboard.press("Tab"); assert.equal(await page.evaluate(() => document.querySelector("#learningAssistanceDialogV1").contains(document.activeElement)), true);
      await page.keyboard.press("Escape");
      await page.waitForFunction(mobile => mobile ? document.activeElement?.getAttribute("data-mobile-target") === "more" : document.activeElement?.id === "learningAssistanceOpenV1", profile.mobile);
      await open(page, profile.mobile);
      assert.equal(await page.locator("#learningAssistanceQueryV1").inputValue(), firstWritten.id);
    });
    await check(prefix + "native-viewport-labels-close-text-and-screenshot", async () => {
      await page.locator('[data-source-id="' + firstWritten.id + '"]').click();
      const geometry = await page.evaluate(() => {
        const dialog = document.querySelector("#learningAssistanceDialogV1"), close = document.querySelector("#learningAssistanceCloseV1"), rect = close.getBoundingClientRect(), range = document.createRange(); range.selectNodeContents(close);
        return { pageWidth: document.documentElement.scrollWidth, viewportWidth: innerWidth, dialogWidth: dialog.clientWidth, dialogScrollWidth: dialog.scrollWidth, close: { width: rect.width, height: rect.height, text: close.textContent, textLines: new Set([...range.getClientRects()].map(rect => Math.round(rect.top))).size }, queryLabel: document.querySelector('label[for="learningAssistanceQueryV1"]').textContent };
      });
      assert.ok(geometry.pageWidth <= geometry.viewportWidth + 1 && geometry.dialogScrollWidth <= geometry.dialogWidth + 1);
      assert.ok(geometry.close.height >= 44 && geometry.close.width >= 44); assert.equal(geometry.close.textLines, 1);
      assert.match(geometry.queryLabel, /Fragenummer/);
      await page.locator("#learningAssistanceDialogV1").evaluate(node => { node.scrollTop = 0; });
      await page.locator("#learningAssistanceDialogV1").screenshot({ path: path.join(out, profile.id + "-source-help.png") });
      save(profile.id + "-source-help-geometry.json", geometry); return geometry;
    });
    await check(prefix + "disabled-provider-ui-and-zero-native-serviceworkers", async () => {
      assert.match(await page.locator("#learningAssistanceProviderV1").innerText(), /KI-Dienst ist ausgeschaltet/);
      const data = await page.evaluate(async () => ({ provider: await ACCAOUI_LEARNING_ASSISTANCE_V1.requestAi({ prompt: "synthetic local input" }), serviceWorkers: navigator.serviceWorker ? (await navigator.serviceWorker.getRegistrations()).length : 0 }));
      assert.equal(data.provider.state, "BLOCKED_EXTERNAL"); assert.equal(data.provider.enabled, false);
      assert.equal(data.provider.providerCalls, 0); assert.equal(data.provider.externalTransfers, 0); assert.equal(data.serviceWorkers, 0);
      await clearClose(page); return data;
    });
    if (!profile.mobile) {
      await home(page);
      await page.locator("#examCard").click(); await page.locator("[onclick*=\"startExamMode\"][onclick*=\"'full'\"]").click();
      const before = await page.evaluate(() => ({ attempt: writtenExamAttemptV2737G.id, status: writtenExamAttemptV2737G.status, questions: examQuestions.map(row => row.id), answers: JSON.stringify(examAnswers), history: JSON.stringify(examHistory) }));
      assert.match(before.attempt, /^[0-9a-f]{8}-[0-9a-f-]{27}$/); assert.equal(before.status, "active");
      await check("written-exam:actual-running-exam-blocks-source-answers", async () => {
        // Explicit attempt through the actual public UI entry point also covers hidden focus-mode navigation.
        await page.evaluate(() => ACCAOUI_LEARNING_ASSISTANCE_UI_V1.open()); await ready(page);
        assert.match(await page.locator("#learningAssistanceStatusV1").innerText(), /laufenden schriftlichen Prüfung/);
        assert.equal(await page.locator("#learningAssistanceAnswerV1").textContent(), "");
        const after = await page.evaluate(() => ({ attempt: writtenExamAttemptV2737G.id, status: writtenExamAttemptV2737G.status, questions: examQuestions.map(row => row.id), answers: JSON.stringify(examAnswers), history: JSON.stringify(examHistory) }));
        assert.deepEqual(after, before); await clearClose(page); return { attemptId: before.attempt, actualNativeExamStarted: true, actualPublicUiEntryPointInvoked: true, newNaturalTimeoutRun: false, assessmentChanged: false };
      });
      await check("written-exam:actual-saved-exam-blocks-source-answers-in-second-tab", async () => {
        const second = await ctx.newPage(); observe(second, "second-exam-tab");
        try {
          await home(second); assert.equal(await second.evaluate(() => hasActiveExamSession()), true);
          await open(second, false); assert.match(await second.locator("#learningAssistanceStatusV1").innerText(), /laufenden schriftlichen Prüfung/);
          assert.equal(await second.locator("#learningAssistanceAnswerV1").textContent(), "");
          const saved = await second.evaluate(() => JSON.parse(localStorage.getItem("accaoui_active_session")));
          assert.equal(saved.attemptId, before.attempt); assert.equal(saved.attemptStatus, "active");
          await clearClose(second); return { sameSavedAttempt: saved.attemptId, actualSecondTab: true, newNaturalTimeoutRun: false };
        } finally { await second.close(); }
      });
    }
  } finally { await ctx.close(); }
}
(async () => {
  try {
    exact(); fs.mkdirSync(out);
    server = http.createServer((req, res) => {
      try {
        const url = new URL(req.url, origin), rel = url.pathname === "/" ? "index.html" : decodeURIComponent(url.pathname).slice(1);
        if (req.method !== "GET" || !Object.hasOwn(cfg.servedFiles, rel)) { requests.push({ kind: "unserved-local", path: rel, status: 404 }); res.writeHead(404); res.end(); return; }
        const bytes = fs.readFileSync(path.join(root, rel)); assert.deepEqual({ bytes: bytes.length, sha256: hash(bytes) }, cfg.servedFiles[rel]);
        const mime = rel.endsWith(".js") ? "application/javascript" : rel.endsWith(".css") ? "text/css" : rel.endsWith(".json") ? "application/json" : "text/html";
        requests.push({ kind: "actual-repository-file", path: rel, bytes: bytes.length, sha256: hash(bytes), status: 200 });
        res.writeHead(200, { "Content-Type": mime + "; charset=utf-8", "Cache-Control": "no-store" }); res.end(bytes);
      } catch (error) { requests.push({ kind: "server-error", error: String(error) }); res.writeHead(500); res.end(); }
    });
    await new Promise((resolve, reject) => { server.once("error", reject); server.listen({ host: "127.0.0.1", port: 8786, exclusive: true }, resolve); });
    const { chromium } = require(cfg.playwrightModule);
    browser = await chromium.launch({ executablePath: cfg.browserExecutable, headless: true, chromiumSandbox: true, args: ["--no-first-run", "--no-default-browser-check"] });
    for (const profile of [{ id: "desktop", viewport: { width: 1440, height: 1000 }, mobile: false }, { id: "mobile", viewport: { width: 390, height: 844 }, mobile: true }]) await profileFlow(profile);
    await Promise.all(requestFailureReads);
    assert.equal(rows.length, 32); assert.ok(rows.every(row => row.status === "PASS"));
    assert.deepEqual(pageErrors, []); assert.deepEqual(externalRequests, []); assert.deepEqual(serviceWorkers, []);
    const offlineSource = row => row.phase.endsWith("actual-offline-source-failure-and-reconnect-retain-query") && ["/questions.json", "/data/oral-question-bank.js"].includes(row.path) && row.method === "GET" && row.resourceType === "fetch" && row.failure === "net::ERR_INTERNET_DISCONNECTED" && row.responseStatus === null && !row.responseReadError;
    const originalMissingConfig = row => row.path === "/data/supabase-config.local.js" && row.method === "GET" && row.resourceType === "fetch" && row.responseStatus === 404 && row.failure === "net::ERR_ABORTED" && !row.responseReadError;
    actualOfflineSourceFailures = failures.filter(offlineSource);
    qualifiedMissingConfigCancellations = failures.filter(originalMissingConfig);
    unexpectedRequestFailures = failures.filter(row => !offlineSource(row) && !originalMissingConfig(row));
    assert.ok(actualOfflineSourceFailures.length >= 4, "both actual source files failed only during explicit offline in both viewports");
    assert.deepEqual(unexpectedRequestFailures, [], "every other request failure remains a failure");
    assert.ok(requests.filter(row => row.kind === "unserved-local" && row.path === "data/supabase-config.local.js" && row.status === 404).length >= qualifiedMissingConfigCancellations.length);
    assert.ok(requests.filter(row => row.kind === "unserved-local").every(row => ["data/supabase-config.local.js", "favicon.ico"].includes(row.path)));
    assert.ok(!requests.some(row => row.kind === "server-error")); exact();
  } catch (error) { failure = { type: error.name, message: error.message.slice(0, 800) }; }
  finally { if (browser) await browser.close(); if (server) await new Promise(resolve => server.close(resolve)); await Promise.all(requestFailureReads); }
  const result = { state: failure ? "W07_ACTUAL_LOCAL_BROWSER_NOT_PASSED" : "W07_ACTUAL_LOCAL_SOURCE_BROWSER_32_CASES_QUALIFIED_REAL_AI_BLOCKED", task: cfg.task, manifestSHA256: cfg.manifestSHA256, cases: rows, failure, pageErrors, externalRequests, requestFailures: failures, actualOfflineSourceFailures, qualifiedMissingConfigCancellations, unexpectedRequestFailures, originalMissingConfigQualification: transportQualification, requests, serviceWorkers, actualExistingRootApp: true, actualSourceResponsesFromPinnedRepositoryFiles: true, fabricatedHttpResponses: 0, deliberateFaults: ["native browser offline/reconnect", "controlled actual oral runtime object drift; source files unchanged"], actualAiAcceptance: false, actualBackendAuthAcceptance: false, physicalDeviceAcceptance: false, fullW07Acceptance: false, newW01NaturalRuns: 0, at: new Date().toISOString() };
  if (fs.existsSync(out)) save("result.json", result);
  console.log(JSON.stringify({ state: result.state, passed: rows.filter(row => row.status === "PASS").length, started: rows.length, failure }));
  if (failure) process.exitCode = 1;
})();
