/* W07 local source viewer. External AI remains disabled; existing assessment/storage stays unchanged. */
(function (root, doc) {
  "use strict";
  if (!root || !doc || root.ACCAOUI_LEARNING_ASSISTANCE_UI_V1 !== undefined) return;
  const A = root.ACCAOUI_LEARNING_ASSISTANCE_V1;
  if (!A) return;
  const expected = {"written":{"bytes":73275,"sha256":"7698da5f08c33276a31d85b8003537a762574e728310cef7739bc44a37ddf780"},"oral":{"bytes":12400,"sha256":"f5ae181d44e30a55b9ca4d705ce4e56ff1311bdcc0a79c68fa2a85095cb99ebd"},"oralFieldsSHA256":"8c1bf6e0d9b1d55b30ddf6126c538c2afdf9422f8e9de251d043715e2768461c"};
  let dialog, model = null, busy = false, generation = 0, opener, lastOpener;
  const nodes = {};
  function element(tag, value, attributes = {}) {
    const node = doc.createElement(tag);
    if (value !== null && value !== undefined) node.textContent = value;
    for (const [name, text] of Object.entries(attributes)) node.setAttribute(name, text);
    return node;
  }
  function status(value, bad = false) {
    nodes.status.textContent = value;
    nodes.status.setAttribute("role", bad ? "alert" : "status");
  }
  function checkExam() {
    try {
      if (typeof hasActiveExamSession !== "function") throw Error("exam_guard_unavailable");
      if ((typeof currentMode !== "undefined" && currentMode === "exam") || hasActiveExamSession()) throw Error("active_written_exam");
    } catch (error) {
      if (error.message === "active_written_exam") throw error;
      throw Error("exam_guard_unavailable");
    }
  }
  function message(error) {
    return ({ active_written_exam: "Während einer laufenden schriftlichen Prüfung bleibt die Quellenhilfe gesperrt. Ihre Prüfung wird unverändert fortgesetzt.",
      exam_guard_unavailable: "Der Prüfungsstand konnte nicht sicher gelesen werden. Die Quellenhilfe bleibt gesperrt; Ihre gespeicherten Daten bleiben erhalten.",
      source_revision_mismatch: "Die Quelle passt nicht zum geprüften Dateistand. Es wird keine Erklärung angezeigt. Ihr Suchtext bleibt erhalten.",
      source_unavailable: "Die vorhandenen Quellen konnten nicht geladen werden. Ihr Suchtext bleibt erhalten. Bitte versuchen Sie Quellen neu laden.",
      source_explanation_missing: "Für diese Frage enthält die Quelle keine Erklärung. Es wird keine Antwort ergänzt.",
      unknown_source: "Diese Quellenkennung ist nicht vorhanden. Es wird keine Erklärung erfunden.",
      invalid_search: "Bitte wählen Sie die Fragenart und geben Sie bis zu 240 Zeichen ein." })[error.message] || "Die Quellen konnten nicht sicher geprüft werden. Ihr Suchtext bleibt erhalten.";
  }
  function clearResults() { nodes.results.replaceChildren(); nodes.answer.replaceChildren(); }
  function guardView() {
    try { checkExam(); return true; }
    catch (error) { model = null; clearResults(); status(message(error), true); return false; }
  }
  async function digest(value) {
    if (!root.crypto?.subtle) throw Error("source_unavailable");
    const raw = typeof value === "string" ? new TextEncoder().encode(value) : value;
    return Array.from(new Uint8Array(await root.crypto.subtle.digest("SHA-256", raw)), byte => byte.toString(16).padStart(2, "0")).join("");
  }
  async function source(path, pin) {
    const target = new URL(path, root.location.href);
    if (target.origin !== root.location.origin) throw Error("source_unavailable");
    let response, bytes;
    try {
      response = await root.fetch(target.href, { cache: "no-store", credentials: "same-origin", redirect: "error" });
      if (!response.ok || new URL(response.url).origin !== root.location.origin) throw Error();
      bytes = new Uint8Array(await response.arrayBuffer());
    } catch (_) { throw Error("source_unavailable"); }
    if (bytes.length !== pin.bytes || await digest(bytes) !== pin.sha256) throw Error("source_revision_mismatch");
    return new TextDecoder("utf-8", { fatal: true }).decode(bytes);
  }
  async function reload() {
    const epoch = ++generation;
    model = null; clearResults();
    if (!guardView()) return;
    busy = true; nodes.searchButton.disabled = true; nodes.reload.disabled = true;
    status("Vorhandene App-Quellen werden geprüft …");
    try {
      const [writtenText] = await Promise.all([
        source(A.sourcePaths.written, expected.written), source(A.sourcePaths.oral, expected.oral)
      ]);
      if (typeof root.AccaouiOralQuestionBank?.listQuestions !== "function") throw Error("source_unavailable");
      const oral = JSON.parse(JSON.stringify(root.AccaouiOralQuestionBank.listQuestions()));
      const oralFields = oral.map(row => ({ id: row.id, category: row.category, question: row.question, sampleAnswer: row.sampleAnswer }));
      if (await digest(JSON.stringify(oralFields)) !== expected.oralFieldsSHA256) throw Error("source_revision_mismatch");
      const next = A.create({ written: JSON.parse(writtenText), oral, sources: {
        written: { path: A.sourcePaths.written, sha256: expected.written.sha256 },
        oral: { path: A.sourcePaths.oral, sha256: expected.oral.sha256 }
      } });
      if (epoch !== generation || !dialog.open) return;
      checkExam(); model = next;
      status(next.counts.written + " schriftliche und " + next.counts.oral + " mündliche App-Fragen geladen. Fachliche Prüfung bleibt offen.");
    } catch (error) {
      if (epoch === generation && dialog.open) { model = null; clearResults(); status(message(error), true); }
    } finally {
      if (epoch === generation) {
        busy = false; nodes.searchButton.disabled = false; nodes.reload.disabled = false;
        if (model && nodes.query.value.trim() && dialog.open) search();
      }
    }
  }
  function select(kind, id) {
    if (!guardView() || !model) return;
    nodes.answer.replaceChildren();
    const result = model.explain(kind, id, expected[kind].sha256);
    if (!result.ok) { status(message(Error(result.code)), true); return; }
    const item = result.item;
    nodes.answer.append(element("h3", item.question), element("h4", item.answerLabel), element("p", result.answer));
    if (item.choices.length) {
      const list = element("ul");
      for (const choice of item.choices) list.appendChild(element("li", choice.text + (choice.markedCorrectInSource ? " — im App-Bestand als richtig markiert" : "")));
      nodes.answer.appendChild(list);
    }
    nodes.answer.appendChild(element("p", result.uncertainty, { class: "source-help-note-v1" }));
    const details = element("details"), summary = element("summary", "Quelle und Prüfbarkeit");
    details.append(summary, element("p", (kind === "written" ? "Schriftlich" : "Mündlich") + " · " + item.citation.itemId),
      element("p", item.citation.path), element("code", "SHA256: " + item.citation.sha256));
    nodes.answer.appendChild(details);
    status("Vorhandene Quellenerklärung angezeigt. Keine KI-Antwort und keine neue Prüfungsbewertung.");
  }
  function search() {
    if (busy || !guardView() || !model) return;
    clearResults();
    const result = model.search(nodes.query.value, { kind: nodes.kind.value, limit: 30 });
    if (!result.ok) { status(message(Error(result.code)), true); return; }
    for (const item of result.items) {
      const row = element("li"), button = element("button", item.id + " · " + item.question, { type: "button", "data-source-id": item.id });
      button.addEventListener("click", () => select(item.kind, item.id)); row.appendChild(button); nodes.results.appendChild(row);
    }
    status(result.total ? result.total + " passende App-Fragen; höchstens 30 angezeigt. Bitte wählen Sie eine Frage." : "Keine passende Frage im ausgewählten App-Bestand. Es wird keine Erklärung erfunden.");
  }
  function mobileEntry() {
    const grid = doc.querySelector("#mobileMoreSheetV227 .mobile-more-grid-v227");
    if (!grid) return false;
    if (!doc.getElementById("learningAssistanceMobileOpenV1")) {
      const button = element("button", null, { type: "button", id: "learningAssistanceMobileOpenV1" });
      button.append(element("span", "📖"), element("strong", "Quellenhilfe"));
      button.addEventListener("click", open); grid.appendChild(button);
    }
    return true;
  }
  function mount() {
    if (dialog) return;
    const tools = doc.getElementById("participantAccountToolsV1") || doc.querySelector(".sidebar") || doc.body;
    opener = element("button", "Quellenhilfe", { type: "button", id: "learningAssistanceOpenV1", class: "source-help-open-v1" });
    opener.addEventListener("click", open); tools.appendChild(opener);
    dialog = element("dialog", null, { id: "learningAssistanceDialogV1", "aria-labelledby": "learningAssistanceTitleV1", class: "source-help-v1" });
    const head = element("header"), close = element("button", "Schließen", { type: "button", id: "learningAssistanceCloseV1" });
    head.append(element("h2", "Lokale Quellenhilfe", { id: "learningAssistanceTitleV1" }), close);
    close.addEventListener("click", () => dialog.close()); dialog.appendChild(head);
    dialog.append(element("p", A.providerStatus().message, { id: "learningAssistanceProviderV1" }),
      element("p", "Hier werden vorhandene App-Erklärungen angezeigt. Ihr Suchtext bleibt in diesem geöffneten Browser; er wird nicht an einen KI-Dienst gesendet."));
    nodes.status = element("p", "Quellen noch nicht geladen.", { id: "learningAssistanceStatusV1", "aria-live": "polite", role: "status" }); dialog.appendChild(nodes.status);
    const form = element("form"), kindLabel = element("label", "Fragenart", { for: "learningAssistanceKindV1" });
    nodes.kind = element("select", null, { id: "learningAssistanceKindV1" });
    nodes.kind.append(element("option", "Schriftliche Fragen", { value: "written" }), element("option", "Mündliche Fragen", { value: "oral" }));
    kindLabel.appendChild(nodes.kind);
    const queryLabel = element("label", "Fragenummer, Thema oder Wörter aus der Frage", { for: "learningAssistanceQueryV1" });
    nodes.query = element("input", null, { id: "learningAssistanceQueryV1", type: "search", maxlength: "240", autocomplete: "off" }); queryLabel.appendChild(nodes.query);
    nodes.searchButton = element("button", "Im App-Bestand suchen", { type: "submit", id: "learningAssistanceSearchV1" });
    nodes.reload = element("button", "Quellen neu laden", { type: "button", id: "learningAssistanceReloadV1" }); nodes.reload.addEventListener("click", reload);
    const clear = element("button", "Suche leeren", { type: "button", id: "learningAssistanceClearV1" });
    clear.addEventListener("click", () => { nodes.query.value = ""; clearResults(); status("Suchtext geleert. Konto- oder Kurswechsel ist wieder möglich."); nodes.query.focus(); });
    form.append(kindLabel, queryLabel, nodes.searchButton, nodes.reload, clear); form.addEventListener("submit", event => { event.preventDefault(); search(); });
    nodes.kind.addEventListener("change", () => { clearResults(); if (nodes.query.value.trim()) search(); });
    nodes.results = element("ul", null, { id: "learningAssistanceResultsV1" });
    nodes.answer = element("section", null, { id: "learningAssistanceAnswerV1", "aria-label": "Vorhandene Quellenerklärung" });
    dialog.append(form, nodes.results, nodes.answer); doc.body.appendChild(dialog);
    dialog.addEventListener("close", () => {
      generation++; busy = false; model = null; clearResults(); nodes.searchButton.disabled = false; nodes.reload.disabled = false;
      const mobileEntryClosed = lastOpener?.id === "learningAssistanceMobileOpenV1";
      const target = !mobileEntryClosed && lastOpener?.getClientRects().length ? lastOpener : doc.querySelector('[data-mobile-target="more"]') || opener;
      target.focus();
    });
    if (!mobileEntry()) {
      const observer = new MutationObserver(() => { if (mobileEntry()) observer.disconnect(); });
      observer.observe(doc.body, { childList: true, subtree: true });
    }
  }
  async function open(event) {
    mount();
    lastOpener = event?.currentTarget instanceof HTMLElement ? event.currentTarget : opener;
    if (typeof root.closeMobileMoreMenuV227 === "function") root.closeMobileMoreMenuV227();
    if (!dialog.open) dialog.showModal();
    await reload();
  }
  function prepareScopeChange() {
    if (nodes.query?.value.trim()) {
      status("Ihr Suchtext ist noch offen. Bitte sichern oder leeren Sie ihn vor einem Konto- oder Kurswechsel.", true);
      const error = Error("pending_form_input"); error.code = "pending_form_input"; throw error;
    }
    if (dialog?.open) dialog.close();
  }
  Object.defineProperty(root, "ACCAOUI_LEARNING_ASSISTANCE_UI_V1", { value: Object.freeze({ open, prepareScopeChange, hasUnsavedInput: () => !!nodes.query?.value.trim() }), enumerable: true, writable: false, configurable: false });
  if (doc.readyState === "loading") doc.addEventListener("DOMContentLoaded", mount, { once: true }); else mount();
  root.addEventListener("beforeunload", event => { if (nodes.query?.value.trim()) { event.preventDefault(); event.returnValue = ""; } });
})(typeof window !== "undefined" ? window : null, typeof document !== "undefined" ? document : null);

/* Private local synthetic pilot. No question-bank or participant input. */
(function (root, doc) {
  "use strict";
  if (!root || !doc || root.location.hostname !== "127.0.0.1" ||
      new URLSearchParams(root.location.search).get("synthetic-ai-pilot") !== "1" ||
      root.ACCAOUI_SYNTHETIC_AI_UI_V1 !== undefined) return;
  let config, dialog, entry, lastEntry, busy = false, generation = 0, selected;
  const nodes = {};
  function el(tag, text, attrs = {}) {
    const node = doc.createElement(tag);
    if (text !== undefined && text !== null) node.textContent = text;
    for (const [key, value] of Object.entries(attrs)) node.setAttribute(key, value);
    return node;
  }
  function examSafe() {
    try {
      return typeof hasActiveExamSession === "function" &&
        !(typeof currentMode !== "undefined" && currentMode === "exam") && !hasActiveExamSession();
    } catch (_) { return false; }
  }
  function status(text, bad = false) {
    nodes.status.textContent = text;
    nodes.status.setAttribute("role", bad ? "alert" : "status");
  }
  function sourceView(item) {
    selected = item; generation++; nodes.answer.replaceChildren(); nodes.sources.replaceChildren();
    nodes.question.textContent = item.question;
    nodes.kind.textContent = item.bank === "oral" ? "Mündliches Beispiel" : "Schriftliches Beispiel";
    for (const source of item.sources) {
      const details = el("details"), summary = el("summary", source.id + " · " + source.title + " · " + source.revision);
      details.append(summary, el("p", source.text)); nodes.sources.appendChild(details);
    }
    if (!item.sources.length) nodes.sources.appendChild(el("p", "Zu diesem Beispiel liegt kein Quellblatt vor."));
    nodes.send.disabled = busy || !examSafe();
    status("Nur dieses künstliche Beispiel und seine angezeigten Quellen werden gesendet.");
  }
  async function send() {
    if (busy || !selected) return;
    if (!examSafe()) { nodes.answer.replaceChildren(); nodes.send.disabled = true; status("Während einer schriftlichen Prüfung bleibt die KI-Übung gesperrt.", true); return; }
    const epoch = ++generation, item = selected;
    busy = true; nodes.send.disabled = true; nodes.choose.disabled = true; nodes.answer.replaceChildren();
    status("Antwort wird angefragt. Bitte kurz warten …");
    try {
      const response = await root.fetch("/__w07/answer", {
        method: "POST", credentials: "same-origin", cache: "no-store", redirect: "error",
        headers: { "Content-Type": "application/json", "X-W07-Nonce": config.nonce },
        body: JSON.stringify({ caseId: item.id })
      });
      if (!response.ok) throw Error("provider_unavailable");
      const result = await response.json();
      if (result.caseId !== item.id || typeof result.answer !== "string" || result.answer.length > 32768 || ![true, false].includes(result.saved)) throw Error("response_mismatch");
      if (epoch !== generation || !dialog.open) return;
      if (!examSafe()) { nodes.answer.replaceChildren(); status("Die Prüfung ist aktiv. Die Antwort wird nicht angezeigt.", true); return; }
      nodes.answer.append(el("h3", "Antwort der KI"), el("p", result.answer),
        el("p", "Künstliche Übung. Keine fachliche §34a-Freigabe und keine Prüfungsbewertung.", { class: "synthetic-ai-note-v1" }));
      status(result.saved ? "Gespeicherte Antwort erneut angezeigt. Keine weitere KI-Anfrage." : "Echte KI-Antwort erhalten. Die angezeigten Quellen bleiben zur Prüfung verfügbar.");
    } catch (_) {
      if (epoch === generation && dialog.open) status("Die Antwort konnte nicht sicher abgeschlossen werden. Es wird keine Anfrage automatisch wiederholt.", true);
    } finally {
      busy = false; nodes.choose.disabled = false;
      nodes.send.disabled = !examSafe();
    }
  }
  function close() { generation++; if (dialog?.open) dialog.close(); }
  async function open(event) {
    lastEntry = event?.currentTarget || entry;
    if (typeof root.closeMobileMoreMenuV227 === "function") root.closeMobileMoreMenuV227();
    if (!dialog.open) dialog.showModal();
    if (!examSafe()) { nodes.send.disabled = true; nodes.answer.replaceChildren(); status("Während einer schriftlichen Prüfung bleibt die KI-Übung gesperrt.", true); return; }
    if (!config) {
      nodes.send.disabled = true; status("Künstliche Beispiele werden geladen …");
      try {
        const response = await root.fetch("/__w07/config", { credentials: "same-origin", cache: "no-store", redirect: "error" });
        if (!response.ok) throw Error();
        const result = await response.json();
        if (typeof result.nonce !== "string" || !/^[a-f0-9]{64}$/.test(result.nonce) || !Array.isArray(result.cases) || result.cases.length !== 6) throw Error();
        config = result; nodes.choose.replaceChildren();
        for (const item of config.cases) nodes.choose.appendChild(el("option", item.label, { value: item.id }));
        nodes.choose.disabled = busy;
      } catch (_) { status("Die lokale KI-Übung ist nicht verfügbar. Bitte keine Zugangsdaten eingeben.", true); return; }
    }
    if (dialog.open) sourceView(config.cases.find(item => item.id === nodes.choose.value) || config.cases[0]);
  }
  function mobileEntry() {
    const grid = doc.querySelector("#mobileMoreSheetV227 .mobile-more-grid-v227");
    if (!grid) return false;
    if (!doc.getElementById("syntheticAiMobileV1")) {
      const button = el("button", null, { type: "button", id: "syntheticAiMobileV1" });
      button.append(el("span", "✦"), el("strong", "KI-Übung")); button.addEventListener("click", open); grid.appendChild(button);
    }
    return true;
  }
  function mount() {
    const tools = doc.getElementById("participantAccountToolsV1") || doc.querySelector(".sidebar") || doc.body;
    entry = el("button", "KI-Übung", { type: "button", id: "syntheticAiOpenV1", class: "source-help-open-v1" });
    entry.addEventListener("click", open); tools.appendChild(entry);
    dialog = el("dialog", null, { id: "syntheticAiDialogV1", "aria-labelledby": "syntheticAiTitleV1", class: "synthetic-ai-v1" });
    const head = el("header"), shut = el("button", "Schließen", { type: "button", id: "syntheticAiCloseV1" });
    shut.addEventListener("click", close); head.append(el("h2", "KI-Übung mit künstlichen Beispielen", { id: "syntheticAiTitleV1" }), shut);
    dialog.append(head, el("p", "Hier werden ausschließlich neu geschriebene, fiktive Aufgaben an OpenAI gesendet. Vorhandene App-Fragen, Suchtexte und persönliche Daten werden dafür nicht verwendet."));
    const label = el("label", "Beispiel auswählen", { for: "syntheticAiCaseV1" });
    nodes.choose = el("select", null, { id: "syntheticAiCaseV1", disabled: "" }); label.appendChild(nodes.choose);
    nodes.choose.addEventListener("change", () => { if (!busy) sourceView(config.cases.find(item => item.id === nodes.choose.value)); });
    nodes.kind = el("p", ""); nodes.question = el("h3", ""); nodes.sources = el("section", null, { id: "syntheticAiSourcesV1", "aria-label": "Künstliche Quellen" });
    nodes.send = el("button", "KI-Antwort anfordern", { type: "button", id: "syntheticAiSendV1", disabled: "" }); nodes.send.addEventListener("click", send);
    nodes.status = el("p", "", { id: "syntheticAiStatusV1", role: "status", "aria-live": "polite" });
    nodes.answer = el("section", null, { id: "syntheticAiAnswerV1", "aria-label": "Antwort der KI" });
    dialog.append(label, nodes.kind, nodes.question, nodes.sources, nodes.send, nodes.status, nodes.answer); doc.body.appendChild(dialog);
    dialog.addEventListener("close", () => {
      generation++; nodes.answer.replaceChildren();
      const mobileEntryClosed = lastEntry?.id === "syntheticAiMobileV1";
      const target = !mobileEntryClosed && lastEntry?.getClientRects().length ? lastEntry : doc.querySelector('[data-mobile-target="more"]') || entry;
      target.focus();
    });
    if (!mobileEntry()) {
      const observer = new MutationObserver(() => { if (mobileEntry()) observer.disconnect(); });
      observer.observe(doc.body, { childList: true, subtree: true });
    }
  }
  Object.defineProperty(root, "ACCAOUI_SYNTHETIC_AI_UI_V1", { value: Object.freeze({ open, prepareScopeChange: close }), enumerable: true, writable: false, configurable: false });
  if (doc.readyState === "loading") doc.addEventListener("DOMContentLoaded", mount, { once: true }); else mount();
})(typeof window !== "undefined" ? window : null, typeof document !== "undefined" ? document : null);
