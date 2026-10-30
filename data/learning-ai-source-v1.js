/* W07 local source assistance. No provider, network, storage or assessment side effects. */
(function (root, common) {
  "use strict";
  const KINDS = Object.freeze(["written", "oral"]);
  const FILES = Object.freeze({ written: "questions.json", oral: "data/oral-question-bank.js" });
  const record = value => value !== null && typeof value === "object" && !Array.isArray(value);
  const text = (value, maximum) => typeof value === "string" && value.trim().length > 0 && value.length <= maximum;
  const id = value => typeof value === "string" && /^[A-Za-z0-9_.:-]{1,100}$/.test(value);
  const digest = value => typeof value === "string" && /^[0-9a-f]{64}$/.test(value);
  const freeze = value => {
    if (value !== null && typeof value === "object") {
      Object.values(value).forEach(freeze);
      Object.freeze(value);
    }
    return value;
  };
  const normalize = value => value.normalize("NFKC").toLocaleLowerCase("de-DE").trim().replace(/\s+/gu, " ");
  const uncertainty = "Vorhandener App-Inhalt. Eine vollständige fachliche Prüfung und aktuelle externe Quellenfreigabe sind hier nicht belegt. Keine amtliche Bewertung oder Bestehensprognose.";

  function sourceOf(kind, sources) {
    const entry = sources[kind];
    if (!record(entry) || entry.path !== FILES[kind] || !digest(entry.sha256)) throw Error("invalid_source_identity");
    return freeze({ path: entry.path, sha256: entry.sha256, review: "not_independently_verified" });
  }

  function convert(kind, row, source) {
    if (!record(row) || !id(row.id) || !text(row.question, 12000) || !text(row.category, 500)) throw Error("invalid_source_item");
    let answer = null;
    let choices = [];
    if (kind === "written") {
      if (!Array.isArray(row.answers) || row.answers.length < 2 || row.answers.length > 12 ||
          !row.answers.every(value => text(value, 6000)) || !Array.isArray(row.correct) || row.correct.length === 0 ||
          new Set(row.correct).size !== row.correct.length ||
          !row.correct.every(value => Number.isInteger(value) && value >= 0 && value < row.answers.length)) throw Error("invalid_written_source_item");
      if (row.explanation !== undefined && row.explanation !== "" && !text(row.explanation, 30000)) throw Error("invalid_source_explanation");
      answer = text(row.explanation, 30000) ? row.explanation : null;
      choices = row.answers.map((value, index) => ({ text: value, markedCorrectInSource: row.correct.includes(index) }));
    } else {
      if (row.sampleAnswer !== undefined && row.sampleAnswer !== "" && !text(row.sampleAnswer, 30000)) throw Error("invalid_source_explanation");
      answer = text(row.sampleAnswer, 30000) ? row.sampleAnswer : null;
    }
    return freeze({
      kind, id: row.id, question: row.question, category: row.category,
      answer, choices, citation: { ...source, kind, itemId: row.id },
      answerLabel: kind === "written" ? "Vorhandene App-Erklärung" : "Vorhandene Musterantwort",
      uncertainty, generatedByAi: false, assessmentChanged: false
    });
  }

  function create(input) {
    if (!record(input) || !record(input.sources)) throw Error("invalid_source_bundle");
    const maps = new Map();
    const rows = [];
    for (const kind of KINDS) {
      const source = sourceOf(kind, input.sources);
      if (!Array.isArray(input[kind]) || input[kind].length > 10000) throw Error("invalid_source_bundle");
      const map = new Map();
      for (const raw of input[kind]) {
        const row = convert(kind, raw, source);
        if (map.has(row.id)) throw Error("duplicate_source_identity");
        map.set(row.id, row);
        rows.push(row);
      }
      maps.set(kind, map);
    }
    function find(kind, itemId) {
      if (!KINDS.includes(kind) || !id(itemId)) return { ok: false, code: "unknown_source" };
      const row = maps.get(kind).get(itemId);
      if (!row) return { ok: false, code: "unknown_source" };
      return { ok: true, item: row };
    }
    function search(query, options = {}) {
      if (!text(query, 240) || !record(options) || !KINDS.includes(options.kind) ||
          (options.limit !== undefined && (!Number.isInteger(options.limit) || options.limit < 1 || options.limit > 30))) return { ok: false, code: "invalid_search" };
      const terms = normalize(query).split(" ").filter(Boolean);
      const limit = options.limit ?? 10;
      const matches = rows.filter(row => row.kind === options.kind && terms.every(term =>
        normalize(row.id + " " + row.category + " " + row.question).includes(term)));
      return { ok: true, total: matches.length, items: matches.slice(0, limit), sourceKind: options.kind, generatedByAi: false };
    }
    function explain(kind, itemId, expectedSHA256) {
      const found = find(kind, itemId);
      if (!found.ok) return found;
      if (!digest(expectedSHA256) || expectedSHA256 !== found.item.citation.sha256) return { ok: false, code: "source_revision_mismatch" };
      if (found.item.answer === null) return { ok: false, code: "source_explanation_missing", citation: found.item.citation, uncertainty };
      return { ok: true, item: found.item, answer: found.item.answer, citation: found.item.citation, uncertainty, generatedByAi: false, assessmentChanged: false };
    }
    return Object.freeze({ find, search, explain, counts: Object.freeze(Object.fromEntries(KINDS.map(kind => [kind, maps.get(kind).size]))) });
  }

  function providerStatus() {
    return freeze({
      state: "BLOCKED_EXTERNAL", enabled: false, actualAiAcceptance: false,
      code: "owner_provider_budget_data_decision_missing",
      message: "Der KI-Dienst ist ausgeschaltet. Anbieter, Kostenlimit und erlaubte Datenübermittlung müssen noch festgelegt werden.",
      requiredDecision: ["provider_and_model", "concrete_cost_ceiling", "permitted_data_and_retention"],
      providerCalls: 0, externalTransfers: 0
    });
  }

  function requestAi() {
    return Promise.resolve({ ok: false, ...providerStatus() });
  }

  const api = Object.freeze({ create, providerStatus, requestAi, kinds: KINDS, sourcePaths: FILES });
  if (common) common.exports = api;
  else root.ACCAOUI_LEARNING_ASSISTANCE_V1 = api;
})(typeof globalThis !== "undefined" ? globalThis : this, typeof module !== "undefined" ? module : null);
