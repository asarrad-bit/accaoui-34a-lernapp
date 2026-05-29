 /* =====================================================
   ACCAOUI §34a LERN-APP
   PATCH v21.2 – Lernkarten & Kategorien stabil
   Zweck:
   - Kategorien unabhängig von lokalen Einfügefehlern stabil halten
   - Lernkarten als echte Flip-Karten darstellen
   - Themenfarben für Lernkarten bereitstellen
===================================================== */

console.log("Accaoui Patch v21.2 geladen");

const ACCAOUI_CATEGORY_LIST = [
  "Recht der öffentlichen Sicherheit und Ordnung",
  "Gewerberecht",
  "Datenschutzrecht",
  "Bürgerliches Gesetzbuch",
  "Straf- und Strafverfahrensrecht",
  "Umgang mit Waffen",
  "Unfallverhütungsvorschrift",
  "Umgang mit Menschen",
  "Grundzüge der Sicherheitstechnik"
];

function getSafeCategories() {
  return ACCAOUI_CATEGORY_LIST;
}

function getCategoryThemeClass(categoryName) {
  const category = typeof normalizeCategoryName === "function"
    ? normalizeCategoryName(categoryName)
    : String(categoryName || "").trim();

  const themeMap = {
    "Recht der öffentlichen Sicherheit und Ordnung": "theme-public-order",
    "Gewerberecht": "theme-trade-law",
    "Datenschutzrecht": "theme-data-protection",
    "Bürgerliches Gesetzbuch": "theme-civil-law",
    "Straf- und Strafverfahrensrecht": "theme-criminal-law",
    "Umgang mit Waffen": "theme-weapons",
    "Unfallverhütungsvorschrift": "theme-safety",
    "Umgang mit Menschen": "theme-people",
    "Grundzüge der Sicherheitstechnik": "theme-security-tech"
  };

  return themeMap[category] || "theme-default";
}

function buildCategoryCards() {
  const categoryContainer = document.getElementById("categories");

  if (!categoryContainer) {
    console.warn("Container #categories wurde nicht gefunden.");
    return;
  }

  categoryContainer.innerHTML = "";

  getSafeCategories().forEach(categoryName => {
    const questionCount = getCategoryQuestions(categoryName).length;
    const mistakeCount = getTopicMistakeCount(categoryName);
    const openCount = getCategoryOpenQuestions(categoryName).length;

    const card = document.createElement("div");
    card.className = "category-card clickable-card";
    card.style.cursor = "pointer";

    card.innerHTML = `
      <div class="category-icon" style="color:${categoryAccentColor};">
        ${categoryIcons[categoryName] || "📘"}
      </div>

      <h3>${escapeHtml(categoryName)}</h3>

      <span>${questionCount} Fragen</span>

      <small style="display:block;margin-top:6px;color:#64748b;font-weight:500;">
        ${openCount} offen
      </small>

      <small style="display:block;margin-top:4px;color:${mistakeCount > 0 ? "#991b1b" : "#64748b"};font-weight:${mistakeCount > 0 ? "700" : "500"};">
        ${mistakeCount} Fehler gespeichert
      </small>
    `;

    card.onclick = () => openCategory(categoryName);
    categoryContainer.appendChild(card);
  });
}

function showFlashcardsPage() {
  currentMode = "flashcards-overview";
  clearExamTimer();

  const mainContent = document.querySelector(".main-content");

  if (!mainContent) return;

  if (!allQuestions || allQuestions.length === 0) {
    showSmallNotice("Fragenbank wurde noch nicht geladen.");
    return;
  }

  const totalProgress = typeof getTotalFlashcardProgress === "function"
    ? getTotalFlashcardProgress()
    : { known: 0, unknown: 0 };

  const totalKnown = Number(totalProgress.known || 0);
  const totalUnknown = Number(totalProgress.unknown || 0);
  const totalOpen = Math.max(0, allQuestions.length - totalKnown - totalUnknown);

  const cardsHtml = getSafeCategories().map(categoryName => {
    const questions = getCategoryQuestions(categoryName);
    const questionCount = questions.length;
    const mistakeCount = getTopicMistakeCount(categoryName);
    const themeClass = getCategoryThemeClass(categoryName);

    const progress = typeof getFlashcardCategoryProgress === "function"
      ? getFlashcardCategoryProgress(categoryName)
      : {
          total: questionCount,
          known: 0,
          unknown: 0,
          untouched: questionCount
        };

    const known = Number(progress.known || 0);
    const unknown = Number(progress.unknown || 0);
    const untouched = Number(progress.untouched || Math.max(0, questionCount - known - unknown));
    const percent = questionCount === 0 ? 0 : Math.round((known / questionCount) * 100);

    return `
      <div class="category-card clickable-card flashcard-category-card ${themeClass}" data-category="${escapeHtml(categoryName)}" style="cursor:pointer;">
        <div class="category-icon" style="color:${categoryAccentColor};">
          ${categoryIcons[categoryName] || "🃏"}
        </div>

        <h3>${escapeHtml(categoryName)}</h3>

        <span>${questionCount} Lernkarten</span>

        <div class="flashcard-progress-row">
          <div class="flashcard-progress-main">
            <strong>${percent}%</strong>
            <span>gewusst</span>
          </div>

          <div class="flashcard-progress-details">
            <span>${known} gewusst</span>
            <span>${unknown} wiederholen</span>
            <span>${untouched} offen</span>
          </div>
        </div>

        <div class="flashcard-progress-track" aria-hidden="true">
          <div class="flashcard-progress-fill" style="width:${percent}%;"></div>
        </div>

        ${
          mistakeCount > 0
            ? `<button
                type="button"
                class="flashcard-mistake-chip"
                onclick='event.stopPropagation(); startTopicMistakeTraining(${JSON.stringify(categoryName)})'
              >
                ${mistakeCount} aktive Fehler trainieren
              </button>`
            : `<small class="flashcard-no-mistakes">Keine aktiven Fehler</small>`
        }
      </div>
    `;
  }).join("");

  mainContent.innerHTML = `
    <button class="back-btn" onclick="location.reload()">
      ← Zurück zum Dashboard
    </button>

    <section class="review-wrapper">
      <div class="review-header">
        <p class="eyebrow">Lernkarten</p>
        <h1>§34a Lernkarten-Modus</h1>
        <p>
          Wiederholen Sie Prüfungswissen mit digitalen Lernkarten.
          Ihr Fortschritt wird lokal im Browser gespeichert.
        </p>
      </div>

      <div class="stats-grid flashcard-overview-stats" style="margin-bottom:22px;">
        <div class="stats-card success">
          <span>Gewusst</span>
          <strong>${totalKnown}</strong>
        </div>

        <div class="stats-card danger">
          <span>Wiederholen</span>
          <strong>${totalUnknown}</strong>
        </div>

        <div class="stats-card">
          <span>Offen</span>
          <strong>${totalOpen}</strong>
        </div>
      </div>

      <div class="result-actions" style="margin-bottom:22px;">
        <button class="next-btn" onclick="startFlashcardSession(allQuestions, 'Alle Lernkarten')">
          Alle Lernkarten starten
        </button>

        ${getTotalTopicMistakeCount() > 0 ? `<button class="next-btn danger-training-btn" onclick="startFlashcardsFromMistakes()">Fehler als Lernkarten</button>` : ""}
      </div>

      <div class="category-grid">
        ${cardsHtml}
      </div>
    </section>
  `;

  document.querySelectorAll(".flashcard-category-card").forEach(card => {
    card.addEventListener("click", () => {
      startFlashcardSessionByCategory(card.dataset.category);
    });
  });
}

/* =====================================================
   v21.10 LERNKARTEN – ANTWORTTEXT FORMATIEREN
   Ziel:
   - Lange Antworten besser lesbar darstellen
   - Mehrteilige Antworten optisch trennen
   - Originaldaten bleiben unverändert
===================================================== */

/* =====================================================
   v21.10.2 LERNKARTEN – ANTWORTTEXT STABIL FORMATIEREN
   Ziel:
   - <br> aus Datenquelle korrekt als Zeilentrennung behandeln
   - lange Antworten besser lesbar darstellen
   - mehrere Antwortbestandteile optisch trennen
   - Originaldaten bleiben unverändert
===================================================== */

function splitFlashcardAnswerParts(answerText) {
  const raw = String(answerText || "").trim();

  if (!raw) {
    return ["Keine Antwort hinterlegt."];
  }

  let normalized = raw
    .replace(/<br\s*\/?>/gi, " | ")
    .replace(/&lt;br\s*\/?>/gi, " | ")
    .replace(/\s+/g, " ")
    .replace(/\s*;\s*/g, " | ")
    .replace(/\s+\|\s+/g, " | ")
    .trim();

  /*
    Lesbarkeitsregeln:
    Nur an klaren zweiten Antwortbestandteilen trennen.
    Nicht aggressiv an jedem Begriff trennen.
  */
  normalized = normalized
    .replace(/\s+(Vorbeugendes\s+Handeln\s+)/gi, " | $1")
    .replace(/\s+(Tätigkeit\s+im\s+)/gi, " | $1")
    .replace(/\s+(Tätigkeit\s+als\s+)/gi, " | $1")
    .replace(/\s+(Bewachung\s+von\s+)/gi, " | $1")
    .replace(/\s+(Schutz\s+vor\s+)/gi, " | $1");

  const parts = normalized
    .split("|")
    .map(part => part.trim())
    .filter(Boolean);

  if (parts.length <= 1) {
    return [normalized];
  }

  return parts;
}

function formatFlashcardAnswerText(question) {
  const answerText = typeof getCorrectAnswerText === "function"
    ? getCorrectAnswerText(question)
    : "";

  const parts = splitFlashcardAnswerParts(answerText);

  return parts
    .map(part => `<span class="flashcard-answer-line">${escapeHtml(part)}</span>`)
    .join("");
}

window.splitFlashcardAnswerParts = splitFlashcardAnswerParts;
window.formatFlashcardAnswerText = formatFlashcardAnswerText;

function renderFlashcard() {
  const flashcardArea = document.getElementById("flashcardArea");
  const question = flashcardQuestions[flashcardIndex];

  if (!flashcardArea || !question) return;

  flashcardFlipped = false;
  const themeClass = getCategoryThemeClass(question.category);

  flashcardArea.innerHTML = `
    <div class="flashcard-study-box ${themeClass}">
      <div class="flashcard-topline">
        <span>${escapeHtml(question.category || "§34a")}</span>
        <strong>${flashcardIndex + 1}/${flashcardQuestions.length}</strong>
      </div>

      <div class="flashcard-scene">
        <div class="flashcard-inner" id="flashcardInner">
          <div class="flashcard-side flashcard-front-side">
            <div class="flashcard-question-content">
              ${formatQuestionText(question.question)}
            </div>

            <div class="flashcard-hint">
              Denken Sie zuerst selbst nach. Danach Antwort aufdecken.
            </div>
          </div>

          <div class="flashcard-side flashcard-back-side">
            <div class="flashcard-answer-block">
              <span>Richtige Antwort</span>
              <strong class="flashcard-answer-text">${formatFlashcardAnswerText(question)}</strong>
            </div>

            <div class="flashcard-explanation-block">
              <span>Erklärung</span>
              <p>${escapeHtml(question.explanation || "Keine Erklärung hinterlegt.")}</p>
            </div>
          </div>
        </div>
      </div>

      <div class="flashcard-actions" id="flashcardFrontActions">
        <button class="next-btn" id="showFlashcardAnswerBtn" onclick="flipFlashcard()">
          Antwort anzeigen
        </button>
      </div>

      <div class="flashcard-rating" id="flashcardRating" style="display:none;">
        <button class="next-btn" onclick="markFlashcardKnown()">
          Gewusst
        </button>

        <button class="next-btn danger-training-btn" onclick="markFlashcardUnknown()">
          Nicht gewusst
        </button>
      </div>

      <div class="flashcard-shared-back">
        <button class="next-btn secondary-btn" onclick="previousFlashcard()">
          Zurück
        </button>
      </div>
    </div>
  `;

  updateFlashcardProgress();
}

function flipFlashcard() {
  const inner = document.getElementById("flashcardInner");
  const frontActions = document.getElementById("flashcardFrontActions");
  const rating = document.getElementById("flashcardRating");

  if (!inner) return;

  const studyBox = inner.closest(".flashcard-study-box");

  flashcardFlipped = true;
  inner.classList.add("flipped");

  if (studyBox) {
    studyBox.classList.add("is-flipped");
  }

  if (frontActions) {
    frontActions.style.setProperty("display", "none", "important");
  }

  if (rating) {
    rating.style.setProperty("display", "flex", "important");
  }
}

window.getSafeCategories = getSafeCategories;
window.getCategoryThemeClass = getCategoryThemeClass;
window.buildCategoryCards = buildCategoryCards;
window.showFlashcardsPage = showFlashcardsPage;
window.renderFlashcard = renderFlashcard;
window.flipFlashcard = flipFlashcard;

/* =====================================================
   v21.6.1 LERNKARTEN – MENÜKLICK SICHERN
===================================================== */

function bindFlashcardsMenuPatch() {
  const flashcardsMenu = document.getElementById("flashcardsMenu");

  if (!flashcardsMenu) {
    console.warn("Menüpunkt Lernkarten wurde nicht gefunden.");
    return;
  }

  flashcardsMenu.style.cursor = "pointer";

  flashcardsMenu.onclick = event => {
    event.preventDefault();
    showFlashcardsPage();
  };
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", bindFlashcardsMenuPatch);
} else {
  bindFlashcardsMenuPatch();
}

window.bindFlashcardsMenuPatch = bindFlashcardsMenuPatch;

/* =====================================================
   v21.11 LERNKARTEN – ABSCHLUSSBILDSCHIRM
   Ziel:
   - Lernkartenrunde professionell abschließen
   - Ergebnis klar anzeigen
   - Runde wiederholen ermöglichen
   - bestehende Speicherlogik unverändert lassen
===================================================== */

if (!window.ACCAOUI_V2111_FLASHCARD_FINISH_PATCH) {
  window.ACCAOUI_V2111_FLASHCARD_FINISH_PATCH = true;

  window.accaouiOriginalStartFlashcardSessionV2111 =
    window.accaouiOriginalStartFlashcardSessionV2111 ||
    window.startFlashcardSession;

  window.accaouiFlashcardSessionTitleV2111 = "Lernkarten";

  window.startFlashcardSession = function patchedStartFlashcardSessionV2111(questions, title) {
    window.accaouiFlashcardSessionTitleV2111 = title || "Lernkarten";

    if (typeof window.accaouiOriginalStartFlashcardSessionV2111 === "function") {
      return window.accaouiOriginalStartFlashcardSessionV2111(questions, title);
    }

    showSmallNotice("Lernkarten konnten nicht gestartet werden.");
  };

  window.repeatCurrentFlashcardSession = function repeatCurrentFlashcardSession() {
    if (!Array.isArray(flashcardQuestions) || flashcardQuestions.length === 0) {
      showSmallNotice("Keine Lernkartenrunde zum Wiederholen vorhanden.");
      showFlashcardsPage();
      return;
    }

    window.startFlashcardSession(
      flashcardQuestions,
      window.accaouiFlashcardSessionTitleV2111 || "Lernkarten"
    );
  };

  window.showFlashcardFinishScreen = function showFlashcardFinishScreen() {
    const total = Array.isArray(flashcardQuestions) ? flashcardQuestions.length : 0;
    const known = Number(flashcardKnownCount || 0);
    const unknown = Number(flashcardUnknownCount || 0);
    const rated = known + unknown;
    const open = Math.max(0, total - rated);

    const percent = rated > 0
      ? Math.round((known / rated) * 100)
      : 0;

    const sessionTitle = window.accaouiFlashcardSessionTitleV2111 || "Lernkarten";

    if (typeof updateDashboardNumbers === "function") {
      updateDashboardNumbers();
    }

    const mainContent = document.querySelector(".main-content");

    if (!mainContent) return;

    mainContent.innerHTML = `
      <button class="back-btn" onclick="showFlashcardsPage()">
        ← Zurück zu den Lernkarten
      </button>

      <section class="result-wrapper flashcard-finish-wrapper">

        <div class="flashcard-finish-hero">
          <p class="eyebrow">Lernkarten abgeschlossen</p>

          <h1>Lernrunde abgeschlossen</h1>

          <p>
            ${escapeHtml(sessionTitle)} wurde ausgewertet.
            Ihr Fortschritt wurde lokal im Browser gespeichert.
          </p>

          <div class="flashcard-finish-percent">
            ${percent}%
          </div>

          <span class="flashcard-finish-label">
            Gewusst-Quote dieser Runde
          </span>
        </div>

        <div class="result-stats-grid flashcard-finish-stats">

          <div class="result-stat-card">
            <span>Bearbeitet</span>
            <strong>${rated}</strong>
          </div>

          <div class="result-stat-card success">
            <span>Gewusst</span>
            <strong>${known}</strong>
          </div>

          <div class="result-stat-card danger">
            <span>Wiederholen</span>
            <strong>${unknown}</strong>
          </div>

          <div class="result-stat-card">
            <span>Offen</span>
            <strong>${open}</strong>
          </div>

        </div>

        <div class="last-exam-box flashcard-finish-note">
          <span>Empfehlung</span>
          <strong>${unknown > 0 ? "Wiederholung einplanen" : "Sehr gute Runde"}</strong>
          <p>
            ${
              unknown > 0
                ? "Bearbeiten Sie die markierten Wiederholen-Karten später erneut. Wiederholung ist entscheidend für sichere Prüfungsleistung."
                : "Alle bewerteten Karten wurden als gewusst markiert. Halten Sie den Stand durch regelmäßige Wiederholung stabil."
            }
          </p>
        </div>

        <div class="result-actions flashcard-finish-actions">

          <button class="next-btn" onclick="repeatCurrentFlashcardSession()">
            Runde nochmal starten
          </button>

          <button class="next-btn" onclick="showFlashcardsPage()">
            Zur Lernkarten-Übersicht
          </button>

          ${
            unknown > 0 && typeof getTotalTopicMistakeCount === "function" && getTotalTopicMistakeCount() > 0
              ? `<button class="next-btn danger-training-btn" onclick="startFlashcardsFromMistakes()">Fehler-Lernkarten starten</button>`
              : ""
          }

          <button class="next-btn secondary-btn" onclick="location.reload()">
            Zurück zum Dashboard
          </button>

        </div>

      </section>
    `;
  };
}

/* =====================================================
   v21.12 LERNKARTEN – WIEDERHOLEN-KARTEN DIESER RUNDE
   Ziel:
   - Nicht-gewusst-Karten der aktuellen Sitzung sammeln
   - direkte Wiederholungsrunde starten
   - keine Änderung an localStorage-Struktur
===================================================== */

if (!window.ACCAOUI_V2112_FLASHCARD_REPEAT_PATCH) {
  window.ACCAOUI_V2112_FLASHCARD_REPEAT_PATCH = true;

  window.accaouiFlashcardSessionRepeatCardsV2112 = [];
  window.accaouiFlashcardSessionRepeatKeysV2112 = new Set();

  function getFlashcardSessionKeyV2112(question) {
    if (!question) return "";

    if (typeof getFlashcardProgressKey === "function") {
      return getFlashcardProgressKey(question);
    }

    if (typeof getQuestionKey === "function") {
      return getQuestionKey(question);
    }

    return String(question.id || question.question || JSON.stringify(question));
  }

  function addFlashcardRepeatCardV2112(question) {
    if (!question) return;

    const key = getFlashcardSessionKeyV2112(question);

    if (!key || window.accaouiFlashcardSessionRepeatKeysV2112.has(key)) {
      return;
    }

    window.accaouiFlashcardSessionRepeatKeysV2112.add(key);
    window.accaouiFlashcardSessionRepeatCardsV2112.push(question);
  }

  function removeFlashcardRepeatCardV2112(question) {
    if (!question) return;

    const key = getFlashcardSessionKeyV2112(question);

    if (!key || !window.accaouiFlashcardSessionRepeatKeysV2112.has(key)) {
      return;
    }

    window.accaouiFlashcardSessionRepeatKeysV2112.delete(key);

    window.accaouiFlashcardSessionRepeatCardsV2112 =
      window.accaouiFlashcardSessionRepeatCardsV2112.filter(savedQuestion => {
        return getFlashcardSessionKeyV2112(savedQuestion) !== key;
      });
  }

  function resetFlashcardRepeatCardsV2112() {
    window.accaouiFlashcardSessionRepeatCardsV2112 = [];
    window.accaouiFlashcardSessionRepeatKeysV2112 = new Set();
  }

  window.accaouiPreviousStartFlashcardSessionV2112 =
    window.accaouiPreviousStartFlashcardSessionV2112 ||
    window.startFlashcardSession;

  window.startFlashcardSession = function patchedStartFlashcardSessionV2112(questions, title) {
    resetFlashcardRepeatCardsV2112();

    if (typeof window.accaouiPreviousStartFlashcardSessionV2112 === "function") {
      return window.accaouiPreviousStartFlashcardSessionV2112(questions, title);
    }

    showSmallNotice("Lernkarten konnten nicht gestartet werden.");
  };

  window.accaouiPreviousMarkFlashcardUnknownV2112 =
    window.accaouiPreviousMarkFlashcardUnknownV2112 ||
    window.markFlashcardUnknown;

  window.markFlashcardUnknown = function patchedMarkFlashcardUnknownV2112() {
    const question = Array.isArray(flashcardQuestions)
      ? flashcardQuestions[flashcardIndex]
      : null;

    addFlashcardRepeatCardV2112(question);

    if (typeof window.accaouiPreviousMarkFlashcardUnknownV2112 === "function") {
      return window.accaouiPreviousMarkFlashcardUnknownV2112();
    }

    showSmallNotice("Bewertung konnte nicht gespeichert werden.");
  };

  window.accaouiPreviousMarkFlashcardKnownV2112 =
    window.accaouiPreviousMarkFlashcardKnownV2112 ||
    window.markFlashcardKnown;

  window.markFlashcardKnown = function patchedMarkFlashcardKnownV2112() {
    const question = Array.isArray(flashcardQuestions)
      ? flashcardQuestions[flashcardIndex]
      : null;

    removeFlashcardRepeatCardV2112(question);

    if (typeof window.accaouiPreviousMarkFlashcardKnownV2112 === "function") {
      return window.accaouiPreviousMarkFlashcardKnownV2112();
    }

    showSmallNotice("Bewertung konnte nicht gespeichert werden.");
  };

  window.startCurrentFlashcardRepeatCards = function startCurrentFlashcardRepeatCards() {
    const repeatCards = Array.isArray(window.accaouiFlashcardSessionRepeatCardsV2112)
      ? [...window.accaouiFlashcardSessionRepeatCardsV2112]
      : [];

    if (repeatCards.length === 0) {
      showSmallNotice("Keine Wiederholen-Karten aus dieser Runde vorhanden.");
      return;
    }

    window.startFlashcardSession(
      repeatCards,
      "Wiederholen-Karten dieser Runde"
    );
  };

  window.showFlashcardFinishScreen = function showFlashcardFinishScreen() {
    const total = Array.isArray(flashcardQuestions) ? flashcardQuestions.length : 0;
    const known = Number(flashcardKnownCount || 0);
    const unknown = Number(flashcardUnknownCount || 0);
    const rated = known + unknown;
    const open = Math.max(0, total - rated);

    const repeatCards = Array.isArray(window.accaouiFlashcardSessionRepeatCardsV2112)
      ? window.accaouiFlashcardSessionRepeatCardsV2112
      : [];

    const repeatCount = repeatCards.length;

    const percent = rated > 0
      ? Math.round((known / rated) * 100)
      : 0;

    const sessionTitle = window.accaouiFlashcardSessionTitleV2111 || "Lernkarten";

    if (typeof updateDashboardNumbers === "function") {
      updateDashboardNumbers();
    }

    const mainContent = document.querySelector(".main-content");

    if (!mainContent) return;

    mainContent.innerHTML = `
      <button class="back-btn" onclick="showFlashcardsPage()">
        ← Zurück zu den Lernkarten
      </button>

      <section class="result-wrapper flashcard-finish-wrapper">

        <div class="flashcard-finish-hero">
          <p class="eyebrow">Lernkarten abgeschlossen</p>

          <h1>Lernrunde abgeschlossen</h1>

          <p>
            ${escapeHtml(sessionTitle)} wurde ausgewertet.
            Ihr Fortschritt wurde lokal im Browser gespeichert.
          </p>

          <div class="flashcard-finish-percent">
            ${percent}%
          </div>

          <span class="flashcard-finish-label">
            Gewusst-Quote dieser Runde
          </span>
        </div>

        <div class="result-stats-grid flashcard-finish-stats">

          <div class="result-stat-card">
            <span>Bearbeitet</span>
            <strong>${rated}</strong>
          </div>

          <div class="result-stat-card success">
            <span>Gewusst</span>
            <strong>${known}</strong>
          </div>

          <div class="result-stat-card danger">
            <span>Wiederholen</span>
            <strong>${unknown}</strong>
          </div>

          <div class="result-stat-card">
            <span>Offen</span>
            <strong>${open}</strong>
          </div>

        </div>

        <div class="last-exam-box flashcard-finish-note">
          <span>Empfehlung</span>
          <strong>${repeatCount > 0 ? "Wiederholen-Karten direkt nacharbeiten" : "Sehr gute Runde"}</strong>
          <p>
            ${
              repeatCount > 0
                ? "In dieser Runde wurden " + repeatCount + " Karte(n) als Wiederholen markiert. Sie können genau diese Karten jetzt direkt nochmal lernen."
                : "Alle bewerteten Karten wurden als gewusst markiert. Halten Sie den Stand durch regelmäßige Wiederholung stabil."
            }
          </p>
        </div>

        <div class="result-actions flashcard-finish-actions">

          ${
            repeatCount > 0
              ? `<button class="next-btn flashcard-repeat-session-btn" onclick="startCurrentFlashcardRepeatCards()">Diese Wiederholen-Karten nochmal lernen</button>`
              : ""
          }

          <button class="next-btn" onclick="repeatCurrentFlashcardSession()">
            Ganze Runde nochmal starten
          </button>

          <button class="next-btn" onclick="showFlashcardsPage()">
            Zur Lernkarten-Übersicht
          </button>

          <button class="next-btn secondary-btn" onclick="location.reload()">
            Zurück zum Dashboard
          </button>

        </div>

      </section>
    `;
  };

  window.getCurrentFlashcardRepeatCards = function getCurrentFlashcardRepeatCards() {
    return Array.isArray(window.accaouiFlashcardSessionRepeatCardsV2112)
      ? [...window.accaouiFlashcardSessionRepeatCardsV2112]
      : [];
  };
}

/* =====================================================
   v21.12.3 LERNKARTEN – FORTSCHRITT MOBIL SAUBER
   Ziel:
   - Position und Bewertung klar trennen
   - keine unschöne lange Textzeile auf Handy
   - Bewertet / Gewusst / Wiederholen als kompakte Chips
===================================================== */

function updateFlashcardProgress() {
  const total = Array.isArray(flashcardQuestions) ? flashcardQuestions.length : 0;
  const seen = total > 0 ? flashcardIndex + 1 : 0;
  const known = Number(flashcardKnownCount || 0);
  const unknown = Number(flashcardUnknownCount || 0);
  const answered = known + unknown;

  const positionPercent = total > 0
    ? Math.round((seen / total) * 100)
    : 0;

  const counter = document.getElementById("flashcardCounter");
  const progressText = document.getElementById("flashcardProgressText");
  const progressFill = document.getElementById("flashcardProgressFill");
  const stats = document.getElementById("flashcardStats");

  if (counter) {
    counter.innerText = `${seen}/${total}`;
  }

  if (progressText) {
    progressText.innerText = `Position: ${seen}/${total}`;
  }

  if (progressFill) {
    progressFill.style.width = positionPercent + "%";
  }

  if (stats) {
    stats.innerHTML = `
      <span class="flashcard-progress-chip">
        <small>Bewertet</small>
        <strong>${answered}/${total}</strong>
      </span>

      <span class="flashcard-progress-chip success">
        <small>Gewusst</small>
        <strong>${known}</strong>
      </span>

      <span class="flashcard-progress-chip danger">
        <small>Wiederholen</small>
        <strong>${unknown}</strong>
      </span>
    `;
  }
}

window.updateFlashcardProgress = updateFlashcardProgress;

/* =====================================================
   v22.0 MÜNDLICHE PRÜFUNG – GRUNDSTRUKTUR
   Ziel:
   - Menüpunkt "Mündliche Prüfung" mit echtem Trainingsmodus füllen
   - typische mündliche Fragen, Musterantworten und Prüferhinweise
   - keine Änderung an app.js, questions.json oder localStorage
===================================================== */

const ORAL_EXAM_QUESTIONS_V220 = [
  {
    category: "Gewerberecht",
    question: "Welche Bedeutung hat §34a GewO für das Bewachungsgewerbe?",
    sampleAnswer: "§34a GewO regelt den Zugang zum Bewachungsgewerbe. Er legt fest, wer Bewachungstätigkeiten ausüben darf und welche Voraussetzungen erfüllt sein müssen, zum Beispiel Zuverlässigkeit, geordnete Vermögensverhältnisse und je nach Tätigkeit Unterrichtung oder Sachkundeprüfung.",
    examinerNote: "Wichtig ist: §34a GewO ist keine Polizeibefugnis, sondern eine gewerberechtliche Zugangsvorschrift."
  },
  {
    category: "Recht der öffentlichen Sicherheit und Ordnung",
    question: "Darf ein privater Sicherheitsmitarbeiter polizeiliche Maßnahmen durchführen?",
    sampleAnswer: "Nein. Private Sicherheitsmitarbeiter haben grundsätzlich keine polizeilichen Hoheitsrechte. Sie handeln auf Grundlage von Jedermannsrechten, Hausrecht, Besitzrecht oder privatrechtlichen Befugnissen.",
    examinerNote: "Der Prüfling muss klar zwischen Staat/Polizei und privatem Sicherheitsdienst unterscheiden."
  },
  {
    category: "Straf- und Strafverfahrensrecht",
    question: "Was bedeutet vorläufige Festnahme nach §127 Absatz 1 StPO?",
    sampleAnswer: "Nach §127 Absatz 1 StPO darf jedermann eine Person vorläufig festnehmen, wenn sie auf frischer Tat betroffen oder verfolgt wird und Fluchtverdacht besteht oder die Identität nicht sofort festgestellt werden kann.",
    examinerNote: "Wichtig sind die Voraussetzungen: frische Tat, Fluchtverdacht oder Identität nicht feststellbar."
  },
  {
    category: "Bürgerliches Gesetzbuch",
    question: "Was ist der Unterschied zwischen Hausrecht und Notwehr?",
    sampleAnswer: "Das Hausrecht erlaubt dem Berechtigten zu bestimmen, wer eine private Fläche betreten oder dort bleiben darf. Notwehr ist die Verteidigung gegen einen gegenwärtigen rechtswidrigen Angriff. Hausrecht regelt also den Zutritt, Notwehr die Abwehr eines Angriffs.",
    examinerNote: "Gute Antwort trennt Zweck, Rechtsnatur und praktische Anwendung."
  },
  {
    category: "Umgang mit Menschen",
    question: "Wie verhalten Sie sich bei einem aggressiven Besucher im Eingangsbereich?",
    sampleAnswer: "Ich bleibe ruhig, halte Abstand, spreche klar und deeskalierend, vermeide Provokationen und sichere den Eigenschutz. Wenn nötig hole ich Unterstützung, setze das Hausrecht durch und informiere bei Gefahr die Polizei.",
    examinerNote: "Prüfer achten auf Deeskalation, Eigenschutz, klare Kommunikation und keine unnötige Gewalt."
  },
  {
    category: "Datenschutzrecht",
    question: "Dürfen Sicherheitsmitarbeiter personenbezogene Daten beliebig weitergeben?",
    sampleAnswer: "Nein. Personenbezogene Daten dürfen nur verarbeitet oder weitergegeben werden, wenn dafür eine rechtliche Grundlage besteht oder es zur Aufgabenerfüllung erforderlich und zulässig ist. Der Grundsatz der Verhältnismäßigkeit und Zweckbindung ist zu beachten.",
    examinerNote: "Wichtig: keine private Weitergabe, keine Neugier-Abfragen, Zweckbindung beachten."
  },
  {
    category: "Unfallverhütungsvorschrift",
    question: "Warum ist Eigenschutz im Sicherheitsdienst besonders wichtig?",
    sampleAnswer: "Eigenschutz ist wichtig, weil Sicherheitsmitarbeiter Gefahren erkennen und vermeiden müssen. Sie sollen sich nicht unnötig selbst gefährden, müssen auf sichere Arbeitsweise achten und bei Gefahr Unterstützung holen.",
    examinerNote: "Gute Antwort verbindet UVV, Gefährdungsbeurteilung, Verhalten und praktische Sicherheit."
  },
  {
    category: "Umgang mit Waffen",
    question: "Darf ein Sicherheitsmitarbeiter grundsätzlich Waffen führen?",
    sampleAnswer: "Nein, nicht grundsätzlich. Das Führen von Waffen unterliegt strengen gesetzlichen Voraussetzungen. Erforderlich sind je nach Fall Erlaubnisse, Eignung, Zuverlässigkeit und ein konkreter dienstlicher Bedarf.",
    examinerNote: "Wichtig ist: keine pauschale Waffenbefugnis im Sicherheitsdienst."
  },
  {
    category: "Grundzüge der Sicherheitstechnik",
    question: "Wozu dient Sicherheitstechnik im Bewachungsgewerbe?",
    sampleAnswer: "Sicherheitstechnik dient der Unterstützung der Bewachungsaufgabe. Beispiele sind Videoüberwachung, Einbruchmeldeanlagen, Zutrittskontrolle und Brandmeldetechnik. Sie ersetzt nicht die rechtliche Bewertung und nicht das richtige Verhalten des Sicherheitsmitarbeiters.",
    examinerNote: "Wichtig ist der Zusammenhang zwischen Technik, Kontrolle, Datenschutz und Reaktion."
  }
];

let oralExamQuestionsV220 = [];
let oralExamIndexV220 = 0;
let oralExamKnownV220 = 0;
let oralExamPracticeV220 = 0;
let oralExamTitleV220 = "Mündliche Prüfung";

function getOralExamCategoriesV220() {
  return [...new Set(ORAL_EXAM_QUESTIONS_V220.map(item => item.category))];
}

function getOralExamQuestionsByCategoryV220(categoryName) {
  return ORAL_EXAM_QUESTIONS_V220.filter(item => item.category === categoryName);
}

function showOralExamPage() {
  currentMode = "oral-exam";

  if (typeof clearExamTimer === "function") {
    clearExamTimer();
  }

  const mainContent = document.querySelector(".main-content");

  if (!mainContent) return;

  const totalQuestions = ORAL_EXAM_QUESTIONS_V220.length;
  const categories = getOralExamCategoriesV220();

  const categoryCards = categories.map(categoryName => {
    const count = getOralExamQuestionsByCategoryV220(categoryName).length;
    const themeClass = typeof getCategoryThemeClass === "function"
      ? getCategoryThemeClass(categoryName)
      : "theme-default";

    return `
      <div class="oral-topic-card ${themeClass}" onclick='startOralExamSessionV220(getOralExamQuestionsByCategoryV220(${JSON.stringify(categoryName)}), ${JSON.stringify(categoryName)})'>
        <div class="oral-topic-icon">
          ${categoryIcons[categoryName] || "🎤"}
        </div>

        <div>
          <h3>${escapeHtml(categoryName)}</h3>
          <p>${count} mündliche Frage(n)</p>
        </div>
      </div>
    `;
  }).join("");

  mainContent.innerHTML = `
    <button class="back-btn" onclick="location.reload()">
      ← Zurück zum Dashboard
    </button>

    <section class="review-wrapper oral-exam-wrapper">

      <div class="oral-exam-hero">
        <p class="eyebrow">Mündliche Prüfung</p>

        <h1>Prüfermodus vorbereiten</h1>

        <p>
          Trainieren Sie typische mündliche Prüfungssituationen mit Frage,
          Musterantwort und Prüfer-Hinweis. Die Fragen sind Trainingsbeispiele
          und ersetzen keine offizielle IHK-Prüfung.
        </p>

        <div class="oral-hero-actions">
          <button class="next-btn" onclick="startOralExamSessionV220(ORAL_EXAM_QUESTIONS_V220, 'Alle mündlichen Fragen')">
            Alle mündlichen Fragen starten
          </button>
        </div>
      </div>

      <div class="stats-grid oral-exam-stats">
        <div class="stats-card">
          <span>Fragen</span>
          <strong>${totalQuestions}</strong>
        </div>

        <div class="stats-card">
          <span>Themen</span>
          <strong>${categories.length}</strong>
        </div>

        <div class="stats-card gold-stat">
          <span>Modus</span>
          <strong>Prüfer</strong>
        </div>
      </div>

      <div class="topic-stats-section oral-topic-section">
        <div class="section-head">
          <h2>Themen für die mündliche Prüfung</h2>
          <p>Wählen Sie ein Thema oder starten Sie alle mündlichen Fragen.</p>
        </div>

        <div class="oral-topic-grid">
          ${categoryCards}
        </div>
      </div>

    </section>
  `;
}

function startOralExamSessionV220(questions, title) {
  if (!Array.isArray(questions) || questions.length === 0) {
    showSmallNotice("Keine mündlichen Fragen vorhanden.");
    return;
  }

  currentMode = "oral-exam-session";

  oralExamQuestionsV220 = [...questions];
  oralExamIndexV220 = 0;
  oralExamKnownV220 = 0;
  oralExamPracticeV220 = 0;
  oralExamTitleV220 = title || "Mündliche Prüfung";

  showOralExamSessionViewV220();
}

function showOralExamSessionViewV220() {
  const mainContent = document.querySelector(".main-content");

  if (!mainContent) return;

  mainContent.innerHTML = `
    <button class="back-btn" onclick="showOralExamPage()">
      ← Zurück zur mündlichen Prüfung
    </button>

    <div class="learning-header oral-session-header">
      <div>
        <p class="eyebrow">Mündliche Prüfung</p>
        <h1>${escapeHtml(oralExamTitleV220)}</h1>
      </div>

      <div class="score-box">
        <span>Frage</span>
        <strong id="oralExamCounterV220">1/${oralExamQuestionsV220.length}</strong>
      </div>
    </div>

    <div class="progress-wrapper oral-progress-wrapper">
      <div class="progress-info">
        <span id="oralExamProgressTextV220">Frage 1/${oralExamQuestionsV220.length}</span>
        <span id="oralExamStatsV220">0 sicher · 0 üben</span>
      </div>

      <div class="progress-bar">
        <div class="progress-fill" id="oralExamProgressFillV220"></div>
      </div>
    </div>

    <section class="oral-question-area" id="oralQuestionAreaV220"></section>
  `;

  renderOralExamQuestionV220();
}

function renderOralExamQuestionV220() {
  const question = oralExamQuestionsV220[oralExamIndexV220];
  const area = document.getElementById("oralQuestionAreaV220");

  if (!question || !area) return;

  const themeClass = typeof getCategoryThemeClass === "function"
    ? getCategoryThemeClass(question.category)
    : "theme-default";

  area.innerHTML = `
    <div class="oral-question-card ${themeClass}">

      <div class="oral-question-topline">
        <span>${escapeHtml(question.category)}</span>
        <strong>${oralExamIndexV220 + 1}/${oralExamQuestionsV220.length}</strong>
      </div>

      <div class="oral-question-main">
        <span>Prüferfrage</span>
        <h2>${escapeHtml(question.question)}</h2>
      </div>

      <div class="oral-answer-box" id="oralAnswerBoxV220" style="display:none;">
        <div class="oral-answer-section">
          <span>Musterantwort</span>
          <p>${escapeHtml(question.sampleAnswer)}</p>
        </div>

        <div class="oral-examiner-note">
          <span>Prüfer-Hinweis</span>
          <p>${escapeHtml(question.examinerNote)}</p>
        </div>
      </div>

      <div class="oral-actions" id="oralRevealActionsV220">
        <button class="next-btn" onclick="showOralExamAnswerV220()">
          Musterantwort anzeigen
        </button>
      </div>

      <div class="oral-actions oral-rating-actions" id="oralRatingActionsV220" style="display:none;">
        <button class="next-btn" onclick="rateOralExamQuestionV220('known')">
          Sicher beantwortet
        </button>

        <button class="next-btn danger-training-btn" onclick="rateOralExamQuestionV220('practice')">
          Noch üben
        </button>
      </div>

      <div class="oral-actions oral-nav-actions">
        <button class="next-btn secondary-btn" onclick="previousOralExamQuestionV220()">
          Zurück
        </button>
      </div>

    </div>
  `;

  updateOralExamProgressV220();
}

function showOralExamAnswerV220() {
  const answerBox = document.getElementById("oralAnswerBoxV220");
  const revealActions = document.getElementById("oralRevealActionsV220");
  const ratingActions = document.getElementById("oralRatingActionsV220");

  if (answerBox) {
    answerBox.style.display = "grid";
  }

  if (revealActions) {
    revealActions.style.display = "none";
  }

  if (ratingActions) {
    ratingActions.style.display = "flex";
  }
}

function rateOralExamQuestionV220(status) {
  if (status === "known") {
    oralExamKnownV220++;
  } else {
    oralExamPracticeV220++;
  }

  if (oralExamIndexV220 >= oralExamQuestionsV220.length - 1) {
    showOralExamFinishScreenV220();
    return;
  }

  oralExamIndexV220++;
  renderOralExamQuestionV220();
}

function previousOralExamQuestionV220() {
  if (oralExamIndexV220 <= 0) {
    showSmallNotice("Sie sind bereits bei der ersten mündlichen Frage.");
    return;
  }

  oralExamIndexV220--;
  renderOralExamQuestionV220();
}

function updateOralExamProgressV220() {
  const total = oralExamQuestionsV220.length;
  const seen = oralExamIndexV220 + 1;
  const answered = oralExamKnownV220 + oralExamPracticeV220;
  const percent = total > 0 ? Math.round((seen / total) * 100) : 0;

  const counter = document.getElementById("oralExamCounterV220");
  const progressText = document.getElementById("oralExamProgressTextV220");
  const progressFill = document.getElementById("oralExamProgressFillV220");
  const stats = document.getElementById("oralExamStatsV220");

  if (counter) {
    counter.innerText = `${seen}/${total}`;
  }

  if (progressText) {
    progressText.innerText = `Frage ${seen}/${total}`;
  }

  if (progressFill) {
    progressFill.style.width = percent + "%";
  }

  if (stats) {
    stats.innerText =
      answered + "/" + total + " bewertet · " +
      oralExamKnownV220 + " sicher · " +
      oralExamPracticeV220 + " üben";
  }
}

function showOralExamFinishScreenV220() {
  const total = oralExamQuestionsV220.length;
  const percent = total > 0
    ? Math.round((oralExamKnownV220 / total) * 100)
    : 0;

  const mainContent = document.querySelector(".main-content");

  if (!mainContent) return;

  mainContent.innerHTML = `
    <button class="back-btn" onclick="showOralExamPage()">
      ← Zurück zur mündlichen Prüfung
    </button>

    <section class="result-wrapper oral-finish-wrapper">

      <div class="oral-finish-hero">
        <p class="eyebrow">Mündliche Prüfung</p>

        <h1>Trainingsrunde abgeschlossen</h1>

        <p>
          ${escapeHtml(oralExamTitleV220)} wurde abgeschlossen.
          Nutzen Sie die Auswertung, um unsichere Antworten gezielt zu wiederholen.
        </p>

        <div class="oral-finish-percent">
          ${percent}%
        </div>

        <span class="oral-finish-label">
          Sicher beantwortet
        </span>
      </div>

      <div class="result-stats-grid oral-finish-stats">

        <div class="result-stat-card">
          <span>Fragen</span>
          <strong>${total}</strong>
        </div>

        <div class="result-stat-card success">
          <span>Sicher</span>
          <strong>${oralExamKnownV220}</strong>
        </div>

        <div class="result-stat-card danger">
          <span>Noch üben</span>
          <strong>${oralExamPracticeV220}</strong>
        </div>

      </div>

      <div class="last-exam-box oral-finish-note">
        <span>Empfehlung</span>
        <strong>${oralExamPracticeV220 > 0 ? "Antworten nacharbeiten" : "Sehr gute mündliche Runde"}</strong>
        <p>
          ${
            oralExamPracticeV220 > 0
              ? "Wiederholen Sie die unsicheren Antworten laut. In der mündlichen Prüfung zählt nicht nur Wissen, sondern auch klare, ruhige und rechtlich saubere Formulierung."
              : "Die Antworten wurden sicher bewertet. Wiederholen Sie regelmäßig, damit die Formulierungen prüfungssicher bleiben."
          }
        </p>
      </div>

      <div class="result-actions oral-finish-actions">
        <button class="next-btn" onclick="startOralExamSessionV220(oralExamQuestionsV220, oralExamTitleV220)">
          Runde nochmal starten
        </button>

        <button class="next-btn" onclick="showOralExamPage()">
          Zur Themenübersicht
        </button>

        <button class="next-btn secondary-btn" onclick="location.reload()">
          Zurück zum Dashboard
        </button>
      </div>

    </section>
  `;
}

function bindOralExamMenuPatchV220() {
  const menuItems = document.querySelectorAll(".menu-item");

  menuItems.forEach(item => {
    const text = item.innerText || "";

    if (text.includes("Mündliche Prüfung")) {
      item.style.cursor = "pointer";
      item.onclick = () => showOralExamPage();
    }
  });
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", bindOralExamMenuPatchV220);
} else {
  bindOralExamMenuPatchV220();
}

window.showOralExamPage = showOralExamPage;
window.startOralExamSessionV220 = startOralExamSessionV220;
window.getOralExamQuestionsByCategoryV220 = getOralExamQuestionsByCategoryV220;
window.showOralExamAnswerV220 = showOralExamAnswerV220;
window.rateOralExamQuestionV220 = rateOralExamQuestionV220;
window.previousOralExamQuestionV220 = previousOralExamQuestionV220;
window.showOralExamFinishScreenV220 = showOralExamFinishScreenV220;

/* =====================================================
   v22.1 MÜNDLICHE PRÜFUNG – REALISTISCHE PRÜFUNGSRAUM-SZENE
   Ziel:
   - reale mündliche Prüfung optisch simulieren
   - 3 Prüfer hinter Tisch, 3 Prüflinge gegenüber
   - Unterlagen / Bewertungsbögen / Stifte darstellen
   - keine Änderung an app.js, questions.json oder localStorage
===================================================== */

if (!window.ACCAOUI_V221_ORAL_ROOM_SCENE_PATCH) {
  window.ACCAOUI_V221_ORAL_ROOM_SCENE_PATCH = true;

  function buildOralExamRoomSceneV221(mode) {
    const isSession = mode === "session";

    return `
      <section class="oral-room-scene-v221 ${isSession ? "is-session" : "is-overview"}" aria-label="Realistische mündliche Prüfungssituation">

        <div class="oral-room-header-v221">
          <div>
            <span>Prüfungsraum-Simulation</span>
            <strong>${isSession ? "Aktive mündliche Prüfung" : "Realistische IHK-Prüfungssituation"}</strong>
          </div>

          <div class="oral-room-status-v221">
            ${isSession ? "Prüfung läuft" : "Vorbereitung"}
          </div>
        </div>

        <div class="oral-room-stage-v221">

          <div class="oral-room-wall-v221">
            <div class="oral-room-board-v221">
              <span>Mündliche Sachkundeprüfung §34a</span>
              <small>Prüfungsausschuss · Bewertungsbogen · Fallfragen</small>
            </div>
          </div>

          <div class="oral-examiner-row-v221">

            <div class="oral-person-v221 examiner-v221">
              <div class="oral-person-head-v221"></div>
              <div class="oral-person-body-v221"></div>
              <strong>Prüfer 1</strong>
              <span>Fragen</span>
            </div>

            <div class="oral-person-v221 examiner-v221 lead-v221">
              <div class="oral-person-head-v221"></div>
              <div class="oral-person-body-v221"></div>
              <strong>Vorsitz</strong>
              <span>Bewertung</span>
            </div>

            <div class="oral-person-v221 examiner-v221">
              <div class="oral-person-head-v221"></div>
              <div class="oral-person-body-v221"></div>
              <strong>Prüfer 3</strong>
              <span>Notizen</span>
            </div>

          </div>

          <div class="oral-table-v221">

            <div class="oral-documents-v221">
              <div class="oral-doc-v221">
                <span></span>
                <span></span>
                <span></span>
              </div>

              <div class="oral-doc-v221 marked-v221">
                <span></span>
                <span></span>
                <span></span>
              </div>

              <div class="oral-pen-v221"></div>

              <div class="oral-nameplate-v221">
                Prüfungsausschuss
              </div>
            </div>

          </div>

          <div class="oral-candidate-row-v221">

            <div class="oral-person-v221 candidate-v221">
              <div class="oral-person-head-v221"></div>
              <div class="oral-person-body-v221"></div>
              <strong>Prüfling 1</strong>
              <span>wartet</span>
            </div>

            <div class="oral-person-v221 candidate-v221 active-v221">
              <div class="oral-person-head-v221"></div>
              <div class="oral-person-body-v221"></div>
              <strong>Sie</strong>
              <span>${isSession ? "antwortet" : "bereit"}</span>
            </div>

            <div class="oral-person-v221 candidate-v221">
              <div class="oral-person-head-v221"></div>
              <div class="oral-person-body-v221"></div>
              <strong>Prüfling 3</strong>
              <span>hört zu</span>
            </div>

          </div>

        </div>

        <div class="oral-room-caption-v221">
          <strong>Realitätsnahes Training:</strong>
          Drei Prüfer, mehrere Prüflinge, Unterlagen auf dem Tisch und eine klare Prüfungssituation.
        </div>

      </section>
    `;
  }

  function enhanceOralExamOverviewV221() {
    const hero = document.querySelector(".oral-exam-hero");

    if (!hero) return;

    if (document.querySelector(".oral-room-scene-v221.is-overview")) {
      return;
    }

    hero.insertAdjacentHTML("afterend", buildOralExamRoomSceneV221("overview"));
  }

  function enhanceOralExamSessionV221() {
    const header = document.querySelector(".oral-session-header");

    if (!header) return;

    if (document.querySelector(".oral-room-scene-v221.is-session")) {
      return;
    }

    header.insertAdjacentHTML("afterend", buildOralExamRoomSceneV221("session"));
  }

  window.accaouiOriginalShowOralExamPageV221 =
    window.accaouiOriginalShowOralExamPageV221 ||
    window.showOralExamPage;

  window.showOralExamPage = function patchedShowOralExamPageV221() {
    if (typeof window.accaouiOriginalShowOralExamPageV221 === "function") {
      window.accaouiOriginalShowOralExamPageV221();
      setTimeout(enhanceOralExamOverviewV221, 0);
      return;
    }

    showSmallNotice("Mündliche Prüfung konnte nicht geöffnet werden.");
  };

  window.accaouiOriginalStartOralExamSessionV221 =
    window.accaouiOriginalStartOralExamSessionV221 ||
    window.startOralExamSessionV220;

  window.startOralExamSessionV220 = function patchedStartOralExamSessionV221(questions, title) {
    if (typeof window.accaouiOriginalStartOralExamSessionV221 === "function") {
      const result = window.accaouiOriginalStartOralExamSessionV221(questions, title);
      setTimeout(enhanceOralExamSessionV221, 0);
      return result;
    }

    showSmallNotice("Mündliche Prüfungsrunde konnte nicht gestartet werden.");
  };

  function bindOralExamMenuPatchV221() {
    const menuItems = document.querySelectorAll(".menu-item");

    menuItems.forEach(item => {
      const text = item.innerText || "";

      if (text.includes("Mündliche Prüfung")) {
        item.style.cursor = "pointer";
        item.onclick = () => window.showOralExamPage();
      }
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", bindOralExamMenuPatchV221);
  } else {
    bindOralExamMenuPatchV221();
  }

  window.buildOralExamRoomSceneV221 = buildOralExamRoomSceneV221;
  window.enhanceOralExamOverviewV221 = enhanceOralExamOverviewV221;
  window.enhanceOralExamSessionV221 = enhanceOralExamSessionV221;
}

/* =====================================================
   v22.2 MÜNDLICHE PRÜFUNG – FRAGE IN PRÜFUNGSRAUM-SZENE
   Ziel:
   - aktuelle Prüferfrage zwischen Prüfertisch und Prüfling anzeigen
   - aktiver Prüfling später mit Login-Namen möglich
   - keine Änderung an app.js, questions.json oder localStorage-Struktur
===================================================== */

if (!window.ACCAOUI_V222_ORAL_SCENE_QUESTION_PATCH) {
  window.ACCAOUI_V222_ORAL_SCENE_QUESTION_PATCH = true;

  function getOralExamUserDisplayNameV222() {
    const directWindowName = String(window.accaouiCurrentUserName || "").trim();

    if (directWindowName) {
      return directWindowName;
    }

    const directStorageName =
      String(localStorage.getItem("accaoui_user_name") || "").trim() ||
      String(localStorage.getItem("accaoui_current_user_name") || "").trim();

    if (directStorageName) {
      return directStorageName;
    }

    try {
      const profile = JSON.parse(localStorage.getItem("accaoui_user_profile") || "{}");
      const profileName = String(profile.name || profile.fullName || "").trim();

      if (profileName) {
        return profileName;
      }
    } catch (error) {
      // Kein Problem: Login-System ist noch nicht aktiv.
    }

    return "Sie";
  }

  function getCurrentOralExamQuestionV222() {
    if (
      Array.isArray(window.oralExamQuestionsV220) &&
      Number.isInteger(window.oralExamIndexV220)
    ) {
      return window.oralExamQuestionsV220[window.oralExamIndexV220];
    }

    if (
      typeof oralExamQuestionsV220 !== "undefined" &&
      Array.isArray(oralExamQuestionsV220) &&
      typeof oralExamIndexV220 !== "undefined"
    ) {
      return oralExamQuestionsV220[oralExamIndexV220];
    }

    return null;
  }

  function syncOralRoomQuestionPromptV222() {
    const scene = document.querySelector(".oral-room-scene-v221.is-session");

    if (!scene) return;

    const table = scene.querySelector(".oral-table-v221");

    if (!table) return;

    const question = getCurrentOralExamQuestionV222();
    const userName = getOralExamUserDisplayNameV222();

    const questionText = question && question.question
      ? String(question.question)
      : "Die aktuelle Prüferfrage wird hier angezeigt.";

    let prompt = scene.querySelector(".oral-room-question-prompt-v222");

    if (!prompt) {
      prompt = document.createElement("div");
      prompt.className = "oral-room-question-prompt-v222";
      table.insertAdjacentElement("afterend", prompt);
    }

    prompt.innerHTML = `
      <span>Prüferfrage an ${escapeHtml(userName)}</span>
      <strong>${escapeHtml(questionText)}</strong>
    `;

    const activeCandidate = scene.querySelector(".candidate-v221.active-v221");

    if (activeCandidate) {
      const nameElement = activeCandidate.querySelector("strong");
      const statusElement = activeCandidate.querySelector("span");

      if (nameElement) {
        nameElement.textContent = userName;
      }

      if (statusElement) {
        statusElement.textContent = "antwortet";
      }
    }
  }

  window.accaouiOriginalStartOralExamSessionV222 =
    window.accaouiOriginalStartOralExamSessionV222 ||
    window.startOralExamSessionV220;

  window.startOralExamSessionV220 = function patchedStartOralExamSessionV222(questions, title) {
    if (typeof window.accaouiOriginalStartOralExamSessionV222 === "function") {
      const result = window.accaouiOriginalStartOralExamSessionV222(questions, title);

      setTimeout(syncOralRoomQuestionPromptV222, 80);
      setTimeout(syncOralRoomQuestionPromptV222, 250);

      return result;
    }

    showSmallNotice("Mündliche Prüfungsrunde konnte nicht gestartet werden.");
  };

  const originalRenderOralExamQuestionV222 =
    typeof window.renderOralExamQuestionV220 === "function"
      ? window.renderOralExamQuestionV220
      : typeof renderOralExamQuestionV220 === "function"
        ? renderOralExamQuestionV220
        : null;

  if (typeof originalRenderOralExamQuestionV222 === "function") {
    window.renderOralExamQuestionV220 = function patchedRenderOralExamQuestionV222() {
      const result = originalRenderOralExamQuestionV222();

      setTimeout(syncOralRoomQuestionPromptV222, 0);

      return result;
    };
  }

  window.syncOralRoomQuestionPromptV222 = syncOralRoomQuestionPromptV222;
  window.getOralExamUserDisplayNameV222 = getOralExamUserDisplayNameV222;
}

/* =====================================================
   v22.5 MÜNDLICHE PRÜFUNG – FRAGE/ANTWORT KOMPAKT IN SZENE
   Ziel:
   - Frage bleibt als Sprechblase in der Prüfungsszene
   - Musterantwort erscheint nach Klick in derselben Sprechblase
   - untere Karte wird nur Bedienpanel
   - keine Änderung an app.js, questions.json oder localStorage
===================================================== */

if (!window.ACCAOUI_V225_ORAL_SCENE_QA_PATCH) {
  window.ACCAOUI_V225_ORAL_SCENE_QA_PATCH = true;

  function getOralExamUserDisplayNameV225() {
    if (typeof getOralExamUserDisplayNameV222 === "function") {
      return getOralExamUserDisplayNameV222();
    }

    const storedName =
      String(localStorage.getItem("accaoui_user_name") || "").trim() ||
      String(localStorage.getItem("accaoui_current_user_name") || "").trim();

    return storedName || "Sie";
  }

  function getCurrentOralExamQuestionV225() {
    if (
      typeof oralExamQuestionsV220 !== "undefined" &&
      Array.isArray(oralExamQuestionsV220) &&
      typeof oralExamIndexV220 !== "undefined"
    ) {
      return oralExamQuestionsV220[oralExamIndexV220];
    }

    return null;
  }

  function markOralControlPanelV225() {
    const card = document.querySelector(".oral-question-card");

    if (!card) return;

    card.classList.add("oral-control-panel-v225");
  }

  function syncOralSceneQAV225(showAnswer) {
    const scene = document.querySelector(".oral-room-scene-v221.is-session");

    if (!scene) return;

    const table = scene.querySelector(".oral-table-v221");

    if (!table) return;

    const question = getCurrentOralExamQuestionV225();
    const userName = getOralExamUserDisplayNameV225();

    const questionText = question && question.question
      ? String(question.question)
      : "Die aktuelle Prüferfrage wird hier angezeigt.";

    const sampleAnswer = question && question.sampleAnswer
      ? String(question.sampleAnswer)
      : "Keine Musterantwort hinterlegt.";

    const examinerNote = question && question.examinerNote
      ? String(question.examinerNote)
      : "Kein Prüfer-Hinweis hinterlegt.";

    let bubble = scene.querySelector(".oral-room-question-prompt-v222");

    if (!bubble) {
      bubble = document.createElement("div");
      bubble.className = "oral-room-question-prompt-v222";
      table.insertAdjacentElement("afterend", bubble);
    }

    bubble.classList.add("oral-room-qa-bubble-v225");

    if (showAnswer) {
      bubble.classList.add("is-answer-visible");
    } else {
      bubble.classList.remove("is-answer-visible");
    }

    bubble.innerHTML = `
      <div class="oral-room-question-view-v225">
        <span>Prüferfrage an ${escapeHtml(userName)}</span>
        <strong>${escapeHtml(questionText)}</strong>
      </div>

      <div class="oral-room-answer-view-v225">
        <span>Musterantwort</span>
        <strong>${escapeHtml(sampleAnswer)}</strong>

        <div class="oral-room-note-v225">
          <small>Prüfer-Hinweis</small>
          <p>${escapeHtml(examinerNote)}</p>
        </div>
      </div>
    `;

    const activeCandidate = scene.querySelector(".candidate-v221.active-v221");

    if (activeCandidate) {
      const nameElement = activeCandidate.querySelector("strong");
      const statusElement = activeCandidate.querySelector("span");

      if (nameElement) {
        nameElement.textContent = userName;
      }

      if (statusElement) {
        statusElement.textContent = showAnswer ? "antwort geprüft" : "antwortet";
      }
    }

    markOralControlPanelV225();
  }

  function scheduleOralSceneQASyncV225(showAnswer) {
    setTimeout(() => syncOralSceneQAV225(showAnswer), 40);
    setTimeout(() => syncOralSceneQAV225(showAnswer), 160);
    setTimeout(() => syncOralSceneQAV225(showAnswer), 360);
  }

  window.accaouiPreviousStartOralExamSessionV225 =
    window.accaouiPreviousStartOralExamSessionV225 ||
    window.startOralExamSessionV220;

  window.startOralExamSessionV220 = function patchedStartOralExamSessionV225(questions, title) {
    if (typeof window.accaouiPreviousStartOralExamSessionV225 === "function") {
      const result = window.accaouiPreviousStartOralExamSessionV225(questions, title);
      scheduleOralSceneQASyncV225(false);
      return result;
    }

    showSmallNotice("Mündliche Prüfungsrunde konnte nicht gestartet werden.");
  };

  window.accaouiPreviousShowOralExamAnswerV225 =
    window.accaouiPreviousShowOralExamAnswerV225 ||
    window.showOralExamAnswerV220;

  window.showOralExamAnswerV220 = function patchedShowOralExamAnswerV225() {
    if (typeof window.accaouiPreviousShowOralExamAnswerV225 === "function") {
      const result = window.accaouiPreviousShowOralExamAnswerV225();
      scheduleOralSceneQASyncV225(true);
      return result;
    }

    syncOralSceneQAV225(true);
  };

  window.accaouiPreviousRateOralExamQuestionV225 =
    window.accaouiPreviousRateOralExamQuestionV225 ||
    window.rateOralExamQuestionV220;

  window.rateOralExamQuestionV220 = function patchedRateOralExamQuestionV225(status) {
    if (typeof window.accaouiPreviousRateOralExamQuestionV225 === "function") {
      const result = window.accaouiPreviousRateOralExamQuestionV225(status);
      scheduleOralSceneQASyncV225(false);
      return result;
    }

    showSmallNotice("Bewertung konnte nicht gespeichert werden.");
  };

  window.accaouiPreviousPreviousOralExamQuestionV225 =
    window.accaouiPreviousPreviousOralExamQuestionV225 ||
    window.previousOralExamQuestionV220;

  window.previousOralExamQuestionV220 = function patchedPreviousOralExamQuestionV225() {
    if (typeof window.accaouiPreviousPreviousOralExamQuestionV225 === "function") {
      const result = window.accaouiPreviousPreviousOralExamQuestionV225();
      scheduleOralSceneQASyncV225(false);
      return result;
    }

    showSmallNotice("Zurück nicht möglich.");
  };

  window.syncOralSceneQAV225 = syncOralSceneQAV225;
}

/* =====================================================
   v22.6 MÜNDLICHE PRÜFUNG – BEDIENUNG IN PRÜFUNGSRAUM
   Ziel:
   - Hinweistext unter der Szene entfernen
   - Buttons in die Prüfungsszene integrieren
   - Fortschritt direkt darunter anzeigen
   - externe Bedienkarte ausblenden
   - keine Änderung an app.js oder questions.json
===================================================== */

if (!window.ACCAOUI_V226_ORAL_SCENE_CONTROLS_PATCH) {
  window.ACCAOUI_V226_ORAL_SCENE_CONTROLS_PATCH = true;

  function getOralSceneProgressTextV226() {
    const total = typeof oralExamQuestionsV220 !== "undefined" && Array.isArray(oralExamQuestionsV220)
      ? oralExamQuestionsV220.length
      : 0;

    const index = typeof oralExamIndexV220 !== "undefined"
      ? oralExamIndexV220 + 1
      : 0;

    const known = Number(typeof oralExamKnownV220 !== "undefined" ? oralExamKnownV220 : 0);
    const practice = Number(typeof oralExamPracticeV220 !== "undefined" ? oralExamPracticeV220 : 0);
    const answered = known + practice;

    return {
      title: `Frage ${index}/${total}`,
      stats: `${answered}/${total} bewertet · ${known} sicher · ${practice} üben`
    };
  }

  function isOralAnswerVisibleV226() {
    const answerBox = document.getElementById("oralAnswerBoxV220");

    if (!answerBox) return false;

    return answerBox.style.display !== "none";
  }

  function renderOralSceneControlsV226() {
    const scene = document.querySelector(".oral-room-scene-v221.is-session");

    if (!scene) return;

    const caption = scene.querySelector(".oral-room-caption-v221");

    if (caption) {
      caption.remove();
    }

    let controls = scene.querySelector(".oral-room-controls-v226");

    if (!controls) {
      controls = document.createElement("div");
      controls.className = "oral-room-controls-v226";
      scene.appendChild(controls);
    }

    const progress = getOralSceneProgressTextV226();
    const answerVisible = isOralAnswerVisibleV226();

    controls.innerHTML = `
      <div class="oral-room-action-row-v226">
        ${
          answerVisible
            ? `
              <button class="next-btn oral-scene-btn-v226" onclick="rateOralExamQuestionV220('known')">
                Sicher beantwortet
              </button>

              <button class="next-btn danger-training-btn oral-scene-btn-v226" onclick="rateOralExamQuestionV220('practice')">
                Noch üben
              </button>
            `
            : `
              <button class="next-btn oral-scene-btn-v226" onclick="showOralExamAnswerV220()">
                Musterantwort anzeigen
              </button>
            `
        }

        <button class="next-btn secondary-btn oral-scene-btn-v226" onclick="previousOralExamQuestionV220()">
          Zurück
        </button>
      </div>

      <div class="oral-room-progress-v226">
        <span>${escapeHtml(progress.title)}</span>
        <strong>${escapeHtml(progress.stats)}</strong>
      </div>
    `;

    document.body.classList.add("oral-scene-controls-active-v226");
  }

  function scheduleOralSceneControlsV226() {
    setTimeout(renderOralSceneControlsV226, 60);
    setTimeout(renderOralSceneControlsV226, 180);
    setTimeout(renderOralSceneControlsV226, 360);
  }

  window.accaouiPreviousStartOralExamSessionV226 =
    window.accaouiPreviousStartOralExamSessionV226 ||
    window.startOralExamSessionV220;

  window.startOralExamSessionV220 = function patchedStartOralExamSessionV226(questions, title) {
    if (typeof window.accaouiPreviousStartOralExamSessionV226 === "function") {
      const result = window.accaouiPreviousStartOralExamSessionV226(questions, title);
      scheduleOralSceneControlsV226();
      return result;
    }

    showSmallNotice("Mündliche Prüfungsrunde konnte nicht gestartet werden.");
  };

  window.accaouiPreviousShowOralExamAnswerV226 =
    window.accaouiPreviousShowOralExamAnswerV226 ||
    window.showOralExamAnswerV220;

  window.showOralExamAnswerV220 = function patchedShowOralExamAnswerV226() {
    if (typeof window.accaouiPreviousShowOralExamAnswerV226 === "function") {
      const result = window.accaouiPreviousShowOralExamAnswerV226();
      scheduleOralSceneControlsV226();
      return result;
    }

    showSmallNotice("Musterantwort konnte nicht angezeigt werden.");
  };

  window.accaouiPreviousRateOralExamQuestionV226 =
    window.accaouiPreviousRateOralExamQuestionV226 ||
    window.rateOralExamQuestionV220;

  window.rateOralExamQuestionV220 = function patchedRateOralExamQuestionV226(status) {
    if (typeof window.accaouiPreviousRateOralExamQuestionV226 === "function") {
      const result = window.accaouiPreviousRateOralExamQuestionV226(status);
      scheduleOralSceneControlsV226();
      return result;
    }

    showSmallNotice("Bewertung konnte nicht gespeichert werden.");
  };

  window.accaouiPreviousPreviousOralExamQuestionV226 =
    window.accaouiPreviousPreviousOralExamQuestionV226 ||
    window.previousOralExamQuestionV220;

  window.previousOralExamQuestionV220 = function patchedPreviousOralExamQuestionV226() {
    if (typeof window.accaouiPreviousPreviousOralExamQuestionV226 === "function") {
      const result = window.accaouiPreviousPreviousOralExamQuestionV226();
      scheduleOralSceneControlsV226();
      return result;
    }

    showSmallNotice("Zurück nicht möglich.");
  };

  window.renderOralSceneControlsV226 = renderOralSceneControlsV226;
}

/* =====================================================
   v22.7 MOBILE NAVIGATION – APP-TAUGLICHE HANDY-NAVIGATION
   Ziel:
   - Desktop-Sidebar bleibt unverändert
   - Mobile bekommt Bottom-Navigation
   - große Sidebar auf Handy wird ausgeblendet
   - aktive Lern-/Prüfungsrunden laufen im Fokusmodus
   - vorbereitet für spätere PWA / App Store / Google Play
===================================================== */

if (!window.ACCAOUI_V227_MOBILE_NAV_PATCH) {
  window.ACCAOUI_V227_MOBILE_NAV_PATCH = true;

  function getCurrentModeV227() {
    try {
      if (typeof currentMode !== "undefined") {
        return String(currentMode || "dashboard");
      }
    } catch (error) {
      return "dashboard";
    }

    return "dashboard";
  }

  function isFocusModeV227(mode) {
    return [
      "exam",
      "learning",
      "category",
      "open-questions",
      "flashcards",
      "oral-exam-session"
    ].includes(mode);
  }

  function closeMobileMoreMenuV227() {
    const sheet = document.getElementById("mobileMoreSheetV227");
    const backdrop = document.getElementById("mobileMoreBackdropV227");

    if (sheet) {
      sheet.classList.remove("is-open");
    }

    if (backdrop) {
      backdrop.classList.remove("is-open");
    }

    document.body.classList.remove("mobile-more-open-v227");
  }

  function toggleMobileMoreMenuV227() {
    const sheet = document.getElementById("mobileMoreSheetV227");
    const backdrop = document.getElementById("mobileMoreBackdropV227");

    if (!sheet || !backdrop) return;

    const willOpen = !sheet.classList.contains("is-open");

    sheet.classList.toggle("is-open", willOpen);
    backdrop.classList.toggle("is-open", willOpen);
    document.body.classList.toggle("mobile-more-open-v227", willOpen);
  }

  function navigateMobileV227(target) {
    closeMobileMoreMenuV227();

    if (target === "dashboard") {
      location.reload();
      return;
    }

    if (target === "questions" && typeof showAllQuestions === "function") {
      showAllQuestions();
      return;
    }

    if (target === "flashcards" && typeof showFlashcardsPage === "function") {
      showFlashcardsPage();
      return;
    }

    if (target === "exam" && typeof startExamMode === "function") {
      startExamMode();
      return;
    }

    if (target === "stats" && typeof showStatsPage === "function") {
      showStatsPage();
      return;
    }

    if (target === "mistakes" && typeof showMistakeOverview === "function") {
      showMistakeOverview();
      return;
    }

    if (target === "oral" && typeof showOralExamPage === "function") {
      showOralExamPage();
      return;
    }

    showSmallNotice("Dieser Bereich konnte nicht geöffnet werden.");
  }

  function createMobileNavigationV227() {
    if (document.getElementById("mobileBottomNavV227")) return;

    const navHtml = `
      <div class="mobile-more-backdrop-v227" id="mobileMoreBackdropV227" onclick="closeMobileMoreMenuV227()"></div>

      <nav class="mobile-bottom-nav-v227" id="mobileBottomNavV227" aria-label="Mobile Hauptnavigation">
        <button type="button" class="mobile-nav-btn-v227" data-mobile-target="dashboard" onclick="navigateMobileV227('dashboard')">
          <span>🏠</span>
          <strong>Start</strong>
        </button>

        <button type="button" class="mobile-nav-btn-v227" data-mobile-target="questions" onclick="navigateMobileV227('questions')">
          <span>📚</span>
          <strong>Fragen</strong>
        </button>

        <button type="button" class="mobile-nav-btn-v227" data-mobile-target="flashcards" onclick="navigateMobileV227('flashcards')">
          <span>🃏</span>
          <strong>Karten</strong>
        </button>

        <button type="button" class="mobile-nav-btn-v227" data-mobile-target="exam" onclick="navigateMobileV227('exam')">
          <span>📝</span>
          <strong>Prüfung</strong>
        </button>

        <button type="button" class="mobile-nav-btn-v227" data-mobile-target="more" onclick="toggleMobileMoreMenuV227()">
          <span>☰</span>
          <strong>Mehr</strong>
        </button>
      </nav>

      <section class="mobile-more-sheet-v227" id="mobileMoreSheetV227" aria-label="Weitere Bereiche">
        <div class="mobile-more-handle-v227"></div>

        <div class="mobile-more-head-v227">
          <span>Accaoui §34a</span>
          <strong>Weitere Bereiche</strong>
        </div>

        <div class="mobile-more-grid-v227">
          <button type="button" onclick="navigateMobileV227('stats')">
            <span>📊</span>
            <strong>Statistik</strong>
          </button>

          <button type="button" onclick="navigateMobileV227('mistakes')">
            <span>🎯</span>
            <strong>Fehlertraining</strong>
          </button>

          <button type="button" onclick="navigateMobileV227('oral')">
            <span>🎤</span>
            <strong>Mündliche Prüfung</strong>
          </button>

          <button type="button" onclick="navigateMobileV227('dashboard')">
            <span>🏠</span>
            <strong>Dashboard</strong>
          </button>
        </div>
      </section>
    `;

    document.body.insertAdjacentHTML("beforeend", navHtml);
  }

  function syncMobileNavigationV227() {
    const mode = getCurrentModeV227();
    const isFocus = isFocusModeV227(mode);

    document.body.classList.toggle("mobile-session-focus-v227", isFocus);

    const buttons = document.querySelectorAll(".mobile-nav-btn-v227");

    buttons.forEach(button => {
      const target = button.dataset.mobileTarget;
      let active = false;

      if (target === "dashboard" && mode === "dashboard") active = true;
      if (target === "questions" && ["all-questions"].includes(mode)) active = true;
      if (target === "flashcards" && ["flashcards-overview"].includes(mode)) active = true;
      if (target === "exam" && ["exam-start"].includes(mode)) active = true;
      if (target === "more" && ["stats", "mistake-overview", "oral-exam"].includes(mode)) active = true;

      button.classList.toggle("is-active", active);
    });
  }

  function initMobileNavigationV227() {
    createMobileNavigationV227();
    syncMobileNavigationV227();

    document.addEventListener("click", () => {
      setTimeout(syncMobileNavigationV227, 80);
    });

    setInterval(syncMobileNavigationV227, 700);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initMobileNavigationV227);
  } else {
    initMobileNavigationV227();
  }

  window.navigateMobileV227 = navigateMobileV227;
  window.toggleMobileMoreMenuV227 = toggleMobileMoreMenuV227;
  window.closeMobileMoreMenuV227 = closeMobileMoreMenuV227;
  window.syncMobileNavigationV227 = syncMobileNavigationV227;
}

/* =====================================================
   v22.7.6 MOBILE BACK GUARD
   Ziel:
   - Handy-Zurück-Button soll nicht auf externe Webseiten springen
   - App bleibt innerhalb der Accaoui-Lern-App
   - Aktive Prüfung wird vor versehentlichem Verlassen geschützt
===================================================== */

if (!window.ACCAOUI_V2276_MOBILE_BACK_GUARD_PATCH) {
  window.ACCAOUI_V2276_MOBILE_BACK_GUARD_PATCH = true;

  function isMobileBackGuardActiveV2276() {
    return window.matchMedia && window.matchMedia("(max-width: 820px)").matches;
  }

  function getCurrentModeV2276() {
    try {
      if (typeof currentMode !== "undefined") {
        return String(currentMode || "dashboard");
      }
    } catch (error) {
      return "dashboard";
    }

    return "dashboard";
  }

  function isActiveExamModeV2276(mode) {
    return mode === "exam";
  }

  function isActiveOralExamModeV2276(mode) {
    return mode === "oral-exam-session";
  }

  function isActiveLearningModeV2276(mode) {
    return [
      "learning",
      "category",
      "open-questions",
      "flashcards"
    ].includes(mode);
  }

  function goToDashboardV2276() {
    try {
      if (typeof clearExamTimer === "function") {
        clearExamTimer();
      }
    } catch (error) {
      /* bewusst still */
    }

    location.reload();
  }

  function closeMobileBackDialogV2276() {
    const dialog = document.getElementById("mobileBackDialogV2276");

    if (dialog) {
      dialog.remove();
    }

    document.body.classList.remove("mobile-back-dialog-open-v2276");
  }

  function showMobileBackDialogV2276(options) {
    closeMobileBackDialogV2276();

    const title = options && options.title
      ? options.title
      : "Bereich verlassen?";

    const message = options && options.message
      ? options.message
      : "Möchten Sie diesen Bereich wirklich verlassen?";

    const confirmText = options && options.confirmText
      ? options.confirmText
      : "Ja, verlassen";

    const cancelText = options && options.cancelText
      ? options.cancelText
      : "Abbrechen";

    const dialog = document.createElement("div");
    dialog.id = "mobileBackDialogV2276";
    dialog.className = "mobile-back-dialog-v2276";

    dialog.innerHTML = `
      <div class="mobile-back-dialog-card-v2276">
        <div class="mobile-back-dialog-icon-v2276">↩</div>

        <h2>${escapeHtml(title)}</h2>

        <p>${escapeHtml(message)}</p>

        <div class="mobile-back-dialog-actions-v2276">
          <button type="button" class="mobile-back-cancel-v2276" id="mobileBackCancelV2276">
            ${escapeHtml(cancelText)}
          </button>

          <button type="button" class="mobile-back-confirm-v2276" id="mobileBackConfirmV2276">
            ${escapeHtml(confirmText)}
          </button>
        </div>
      </div>
    `;

    document.body.appendChild(dialog);
    document.body.classList.add("mobile-back-dialog-open-v2276");

    const cancelButton = document.getElementById("mobileBackCancelV2276");
    const confirmButton = document.getElementById("mobileBackConfirmV2276");

    if (cancelButton) {
      cancelButton.onclick = closeMobileBackDialogV2276;
    }

    if (confirmButton) {
      confirmButton.onclick = function () {
        closeMobileBackDialogV2276();

        if (options && typeof options.onConfirm === "function") {
          options.onConfirm();
        }
      };
    }
  }

  function handleMobileBackV2276() {
    const mode = getCurrentModeV2276();

    if (isActiveExamModeV2276(mode)) {
      showMobileBackDialogV2276({
        title: "Prüfung wirklich verlassen?",
        message: "Ihre laufende Prüfung wird beendet. Nicht abgegebene Antworten können verloren gehen.",
        confirmText: "Prüfung verlassen",
        cancelText: "Weiter prüfen",
        onConfirm: goToDashboardV2276
      });

      return;
    }

    if (isActiveOralExamModeV2276(mode)) {
      showMobileBackDialogV2276({
        title: "Mündliche Prüfung verlassen?",
        message: "Die aktuelle mündliche Prüfungsrunde wird beendet.",
        confirmText: "Runde verlassen",
        cancelText: "Weiter üben",
        onConfirm: goToDashboardV2276
      });

      return;
    }

    if (isActiveLearningModeV2276(mode)) {
      showMobileBackDialogV2276({
        title: "Lernrunde verlassen?",
        message: "Sie kehren zur Startseite zurück. Ihr gespeicherter Fortschritt bleibt erhalten.",
        confirmText: "Zur Startseite",
        cancelText: "Weiter lernen",
        onConfirm: goToDashboardV2276
      });

      return;
    }

    if (mode !== "dashboard") {
      goToDashboardV2276();
      return;
    }

    if (typeof showSmallNotice === "function") {
      showSmallNotice("Sie sind bereits auf der Startseite.");
    }
  }

  function installMobileBackGuardV2276() {
    if (window.ACCAOUI_V2276_BACK_GUARD_INSTALLED) return;

    window.ACCAOUI_V2276_BACK_GUARD_INSTALLED = true;

    try {
      history.replaceState(
        { accaouiApp: true },
        "",
        location.href
      );

      history.pushState(
        { accaouiBackGuard: true },
        "",
        location.href
      );
    } catch (error) {
      console.warn("Mobile Back Guard konnte nicht initialisiert werden.", error);
    }

    window.addEventListener("popstate", function () {
      if (!isMobileBackGuardActiveV2276()) {
        return;
      }

      try {
        history.pushState(
          { accaouiBackGuard: true },
          "",
          location.href
        );
      } catch (error) {
        /* bewusst still */
      }

      handleMobileBackV2276();
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", installMobileBackGuardV2276);
  } else {
    installMobileBackGuardV2276();
  }

  window.showMobileBackDialogV2276 = showMobileBackDialogV2276;
  window.closeMobileBackDialogV2276 = closeMobileBackDialogV2276;
  window.handleMobileBackV2276 = handleMobileBackV2276;
}

/* =====================================================
   v23.1.1 LERNMODUS – VORZEITIGE AUSWERTUNG
   Ziel:
   - Themenrunde kann vorzeitig beendet werden
   - Nutzer sieht Zwischenergebnis
   - offene Fragen werden nicht automatisch als falsch gewertet
   - keine Änderung an app.js oder questions.json
===================================================== */

if (!window.ACCAOUI_V2311_LEARNING_PARTIAL_RESULT_PATCH) {
  window.ACCAOUI_V2311_LEARNING_PARTIAL_RESULT_PATCH = true;

  function isLearningSessionActiveV2311() {
    try {
      return [
        "learning",
        "category",
        "open-questions",
        "topic-mistakes",
        "all-mistakes"
      ].includes(String(currentMode || ""));
    } catch (error) {
      return false;
    }
  }

  function getLearningSessionStatsV2311() {
    const total = Array.isArray(currentQuestions) ? currentQuestions.length : 0;
    const correct = Number(correctAnswersCount || 0);
    const wrong = Number(wrongAnswersCount || 0);
    const answered = correct + wrong;
    const open = Math.max(0, total - answered);
    const percent = answered > 0 ? Math.round((correct / answered) * 100) : 0;

    return {
      total,
      correct,
      wrong,
      answered,
      open,
      percent
    };
  }

  function renderLearningAbortControlsV2311() {
    if (!isLearningSessionActiveV2311()) return;

    const progressWrapper = document.querySelector(".progress-wrapper");
    const questionArea = document.getElementById("questionArea");

    if (!progressWrapper || !questionArea) return;

    let controls = document.getElementById("learningAbortControlsV2311");

    if (!controls) {
      controls = document.createElement("div");
      controls.id = "learningAbortControlsV2311";
      controls.className = "learning-abort-controls-v2311";

      progressWrapper.insertAdjacentElement("afterend", controls);
    }

    const stats = getLearningSessionStatsV2311();

    controls.innerHTML = `
      <button type="button" class="learning-finish-btn-v2311" onclick="showLearningPartialResultV2311()">
        Auswertung anzeigen
      </button>

      <span>
        ${stats.answered}/${stats.total} bearbeitet
      </span>
    `;
  }

  function showLearningPartialResultV2311() {
    if (!isLearningSessionActiveV2311()) {
      return;
    }

    const stats = getLearningSessionStatsV2311();

    if (stats.answered === 0) {
      if (typeof showSmallNotice === "function") {
        showSmallNotice("Beantworten Sie zuerst mindestens eine Frage.");
      }
      return;
    }

    const title = currentTrainingTitle || "Lernrunde";

    const mainContent = document.querySelector(".main-content");

    if (!mainContent) return;

    mainContent.innerHTML = `
      <button class="back-btn" onclick="location.reload()">
        ← Zurück zum Dashboard
      </button>

      <section class="finish-card learning-partial-result-v2311">

        <p class="eyebrow">Zwischenauswertung</p>

        <h1>${escapeHtml(title)}</h1>

        <div class="learning-partial-percent-v2311">
          ${stats.percent}%
        </div>

        <p class="learning-partial-subline-v2311">
          Ergebnis bezogen auf die bearbeiteten Fragen.
        </p>

        <div class="learning-partial-grid-v2311">

          <div>
            <span>Bearbeitet</span>
            <strong>${stats.answered}/${stats.total}</strong>
          </div>

          <div class="success">
            <span>Richtig</span>
            <strong>${stats.correct}</strong>
          </div>

          <div class="danger">
            <span>Falsch</span>
            <strong>${stats.wrong}</strong>
          </div>

          <div>
            <span>Offen</span>
            <strong>${stats.open}</strong>
          </div>

        </div>

        <div class="result-actions">

          <button class="next-btn" onclick="showMistakeOverview()">
            Fehlertraining
          </button>

          <button class="next-btn" onclick="showAllQuestions()">
            Themenübersicht
          </button>

          <button class="next-btn secondary-btn" onclick="location.reload()">
            Zurück zum Dashboard
          </button>

        </div>

      </section>
    `;
  }

  const originalShowLearningViewV2311 =
    typeof window.showLearningView === "function"
      ? window.showLearningView
      : typeof showLearningView === "function"
        ? showLearningView
        : null;

  if (typeof originalShowLearningViewV2311 === "function") {
    window.showLearningView = function patchedShowLearningViewV2311(title) {
      const result = originalShowLearningViewV2311(title);

      setTimeout(renderLearningAbortControlsV2311, 40);
      setTimeout(renderLearningAbortControlsV2311, 160);

      return result;
    };
  }

  const originalUpdateProgressV2311 =
    typeof window.updateProgress === "function"
      ? window.updateProgress
      : typeof updateProgress === "function"
        ? updateProgress
        : null;

  if (typeof originalUpdateProgressV2311 === "function") {
    window.updateProgress = function patchedUpdateProgressV2311() {
      const result = originalUpdateProgressV2311();

      setTimeout(renderLearningAbortControlsV2311, 40);

      return result;
    };
  }

  window.renderLearningAbortControlsV2311 = renderLearningAbortControlsV2311;
  window.showLearningPartialResultV2311 = showLearningPartialResultV2311;
}

/* =====================================================
   v23.1.2 MÜNDLICHE PRÜFUNG – KOMPAKTE MOBILE ÜBERSICHT
   Ziel:
   - große Einführungskarte reduzieren
   - Prüfungsszene stärker nach oben holen
   - "Vorbereitung" durch Startbutton ersetzen
   - große Statistik-Karten als kompakte Statuszeile anzeigen
   - rechtlich sauber: Simulation / Trainingsbeispiele
===================================================== */

if (!window.ACCAOUI_V2312_ORAL_COMPACT_OVERVIEW_PATCH) {
  window.ACCAOUI_V2312_ORAL_COMPACT_OVERVIEW_PATCH = true;

  function buildCompactOralRoomSceneV2312() {
    let sceneHtml = "";

    if (typeof window.buildOralExamRoomSceneV221 === "function") {
      sceneHtml = window.buildOralExamRoomSceneV221("overview");
    }

    if (!sceneHtml) {
      return "";
    }

    sceneHtml = sceneHtml
      .replace(
        "Realistische IHK-Prüfungssituation",
        "Mündliche Prüfungssimulation § 34a"
      )
      .replace(
        /<div class="oral-room-status-v221">\s*Vorbereitung\s*<\/div>/,
        `<button type="button" class="oral-room-start-btn-v2312" onclick="startOralExamSessionV220(ORAL_EXAM_QUESTIONS_V220, 'Alle mündlichen Fragen')">
          Mündliche Prüfung starten
        </button>`
      )
      .replace(
        `aria-label="Realistische mündliche Prüfungssituation"`,
        `aria-label="Mündliche Prüfungssimulation § 34a"`
      );

    return sceneHtml;
  }

  function showCompactOralExamPageV2312() {
    currentMode = "oral-exam";

    if (typeof clearExamTimer === "function") {
      clearExamTimer();
    }

    const mainContent = document.querySelector(".main-content");

    if (!mainContent) return;

    const totalQuestions = ORAL_EXAM_QUESTIONS_V220.length;
    const oralCategories = getOralExamCategoriesV220();

    const categoryCards = oralCategories.map(categoryName => {
      const count = getOralExamQuestionsByCategoryV220(categoryName).length;
      const themeClass = typeof getCategoryThemeClass === "function"
        ? getCategoryThemeClass(categoryName)
        : "theme-default";

      return `
        <div class="oral-topic-card ${themeClass}" onclick='startOralExamSessionV220(getOralExamQuestionsByCategoryV220(${JSON.stringify(categoryName)}), ${JSON.stringify(categoryName)})'>
          <div class="oral-topic-icon">
            ${categoryIcons[categoryName] || "🎤"}
          </div>

          <div>
            <h3>${escapeHtml(categoryName)}</h3>
            <p>${count} mündliche Frage(n)</p>
          </div>
        </div>
      `;
    }).join("");

    mainContent.innerHTML = `
      <button class="back-btn" onclick="location.reload()">
        ← Zurück zum Dashboard
      </button>

      <section class="review-wrapper oral-exam-wrapper oral-compact-overview-v2312">

        <div class="oral-compact-hero-v2312">
          <p class="eyebrow">Mündliche Prüfung</p>

          <h1>Prüfermodus trainieren</h1>

          <p>
            Üben Sie typische mündliche Prüfungssituationen mit Frage,
            Musterantwort und Prüfer-Hinweis.
          </p>

          <button class="next-btn oral-compact-start-v2312" onclick="startOralExamSessionV220(ORAL_EXAM_QUESTIONS_V220, 'Alle mündlichen Fragen')">
            Alle mündlichen Fragen starten
          </button>
        </div>

        ${buildCompactOralRoomSceneV2312()}

        <div class="oral-compact-status-v2312">
          <span><strong>${totalQuestions}</strong> Fragen</span>
          <span><strong>${oralCategories.length}</strong> Themen</span>
          <span><strong>Prüfermodus</strong></span>
        </div>

        <p class="oral-compact-legal-note-v2312">
          Trainingsbeispiele. Keine offizielle IHK-Prüfung.
        </p>

        <div class="topic-stats-section oral-topic-section oral-topic-section-compact-v2312">
          <div class="section-head">
            <h2>Themen für die mündliche Prüfung</h2>
            <p>Wählen Sie ein Thema oder starten Sie alle mündlichen Fragen.</p>
          </div>

          <div class="oral-topic-grid">
            ${categoryCards}
          </div>
        </div>

      </section>
    `;
  }

  window.showOralExamPage = showCompactOralExamPageV2312;

  try {
    showOralExamPage = window.showOralExamPage;
  } catch (error) {
    /* globales Rebinding ist nicht in jeder Umgebung nötig */
  }
}

/* =====================================================
   v23.1.4 MÜNDLICHE PRÜFUNG – MODUSAUSWAHL
   Ziel:
   - Startbutton öffnet Auswahl statt sofort zu starten
   - Training / 15-Minuten-Simulation / Volltraining
   - Grundlage für spätere Accaoui-Trainingsbewertung
===================================================== */

if (!window.ACCAOUI_V2314_ORAL_MODE_SELECTION_PATCH) {
  window.ACCAOUI_V2314_ORAL_MODE_SELECTION_PATCH = true;

  function closeOralModeSheetV2314() {
    const sheet = document.getElementById("oralModeSheetV2314");
    const backdrop = document.getElementById("oralModeBackdropV2314");

    if (sheet) sheet.remove();
    if (backdrop) backdrop.remove();

    document.body.classList.remove("oral-mode-sheet-open-v2314");
  }

  function getRandomOralQuestionsV2314(count) {
    const questions = Array.isArray(ORAL_EXAM_QUESTIONS_V220)
      ? [...ORAL_EXAM_QUESTIONS_V220]
      : [];

    for (let i = questions.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [questions[i], questions[j]] = [questions[j], questions[i]];
    }

    return questions.slice(0, count);
  }

  function scrollToOralTopicsV2314() {
    closeOralModeSheetV2314();

    const section =
      document.querySelector(".oral-topic-section") ||
      document.querySelector(".oral-topic-section-compact-v2312");

    if (section) {
      section.scrollIntoView({
        behavior: "smooth",
        block: "start"
      });
      return;
    }

    showSmallNotice("Themenübersicht wurde nicht gefunden.");
  }

  function startOralSimulation15V2314() {
    closeOralModeSheetV2314();

    const questions = getRandomOralQuestionsV2314(15);

    if (!questions.length) {
      showSmallNotice("Keine mündlichen Fragen vorhanden.");
      return;
    }

    startOralExamSessionV220(
      questions,
      "15-Minuten-Prüfungssimulation"
    );
  }

  function startOralFullTrainingV2314() {
    closeOralModeSheetV2314();

    startOralExamSessionV220(
      ORAL_EXAM_QUESTIONS_V220,
      "Volltraining mündliche Prüfung"
    );
  }

  function showOralExamModeSelectV2314() {
    closeOralModeSheetV2314();

    const backdrop = document.createElement("div");
    backdrop.id = "oralModeBackdropV2314";
    backdrop.className = "oral-mode-backdrop-v2314";
    backdrop.onclick = closeOralModeSheetV2314;

    const sheet = document.createElement("section");
    sheet.id = "oralModeSheetV2314";
    sheet.className = "oral-mode-sheet-v2314";

    sheet.innerHTML = `
      <div class="oral-mode-handle-v2314"></div>

      <div class="oral-mode-head-v2314">
        <span>Mündliche Prüfung</span>
        <h2>Modus auswählen</h2>
        <p>Wählen Sie, wie Sie die mündliche Prüfung trainieren möchten.</p>
      </div>

      <div class="oral-mode-grid-v2314">

        <button type="button" class="oral-mode-card-v2314" onclick="scrollToOralTopicsV2314()">
          <span>🎤</span>
          <strong>Training nach Themen</strong>
          <small>Thema auswählen · mit Musterantwort · ohne Zeitdruck</small>
        </button>

        <button type="button" class="oral-mode-card-v2314 is-primary" onclick="startOralSimulation15V2314()">
          <span>⏱️</span>
          <strong>15-Minuten-Simulation</strong>
         <small>3 Prüfer · 15 Fragen · Auswertung am Ende</small>
        </button>

        <button type="button" class="oral-mode-card-v2314" onclick="startOralFullTrainingV2314()">
          <span>📚</span>
          <strong>Volltraining</strong>
          <small>Alle mündlichen Fragen · IHK-Themenreihenfolge · ohne Zeitdruck</small>
        </button>

      </div>

      <p class="oral-mode-note-v2314">
        Trainingsbeispiele. Keine offizielle IHK-Prüfung.
      </p>
    `;

    document.body.appendChild(backdrop);
    document.body.appendChild(sheet);
    document.body.classList.add("oral-mode-sheet-open-v2314");
  }

  function bindOralModeStartButtonsV2314() {
    const buttons = document.querySelectorAll(
      ".oral-room-start-btn-v2312, .oral-compact-start-v2312"
    );

    buttons.forEach(button => {
      button.onclick = showOralExamModeSelectV2314;
      button.setAttribute("onclick", "showOralExamModeSelectV2314()");
      button.textContent = "Mündliche Prüfung starten";
    });
  }

  window.accaouiPreviousShowOralExamPageV2314 =
    window.accaouiPreviousShowOralExamPageV2314 ||
    window.showOralExamPage;

  window.showOralExamPage = function patchedShowOralExamPageV2314() {
    if (typeof window.accaouiPreviousShowOralExamPageV2314 === "function") {
      const result = window.accaouiPreviousShowOralExamPageV2314();

      setTimeout(bindOralModeStartButtonsV2314, 40);
      setTimeout(bindOralModeStartButtonsV2314, 180);
      setTimeout(bindOralModeStartButtonsV2314, 420);

      return result;
    }

    showSmallNotice("Mündliche Prüfung konnte nicht geöffnet werden.");
  };

  window.showOralExamModeSelectV2314 = showOralExamModeSelectV2314;
  window.closeOralModeSheetV2314 = closeOralModeSheetV2314;
  window.scrollToOralTopicsV2314 = scrollToOralTopicsV2314;
  window.startOralSimulation15V2314 = startOralSimulation15V2314;
  window.startOralFullTrainingV2314 = startOralFullTrainingV2314;
}

/* =====================================================
   v23.1.5 MÜNDLICHE PRÜFUNG – MODUSAUSWAHL HOTFIX & SZENE POLISH
   Ziel:
   - Prüfer 1 optisch als fragender Prüfer hervorheben
   - kleine Textkorrektur § 34a
   - nach Rendering sauber nachpolieren
===================================================== */

if (!window.ACCAOUI_V2315_ORAL_POLISH_PATCH) {
  window.ACCAOUI_V2315_ORAL_POLISH_PATCH = true;

  function polishOralExamSceneV2315() {
    const scenes = document.querySelectorAll(".oral-room-scene-v221");

    scenes.forEach(scene => {
      const firstExaminer = scene.querySelector(".oral-examiner-row-v221 .oral-person-v221:first-child");

      if (firstExaminer) {
        firstExaminer.classList.add("is-active-examiner-v2315");
      }

      const boardTitle = scene.querySelector(".oral-room-board-v221 span");

      if (boardTitle && boardTitle.textContent.includes("§34a")) {
        boardTitle.textContent = boardTitle.textContent.replace("§34a", "§ 34a");
      }

      const headerTitle = scene.querySelector(".oral-room-header-v221 strong");

      if (headerTitle && headerTitle.textContent.includes("§ 34a")) {
        headerTitle.textContent = headerTitle.textContent.replace("§ 34a", "§ 34a");
      }
    });
  }

  function scheduleOralPolishV2315() {
    setTimeout(polishOralExamSceneV2315, 40);
    setTimeout(polishOralExamSceneV2315, 180);
    setTimeout(polishOralExamSceneV2315, 420);
  }

  window.accaouiPreviousShowOralExamPageV2315 =
    window.accaouiPreviousShowOralExamPageV2315 ||
    window.showOralExamPage;

  window.showOralExamPage = function patchedShowOralExamPageV2315() {
    if (typeof window.accaouiPreviousShowOralExamPageV2315 === "function") {
      const result = window.accaouiPreviousShowOralExamPageV2315();
      scheduleOralPolishV2315();
      return result;
    }

    showSmallNotice("Mündliche Prüfung konnte nicht geöffnet werden.");
  };

  window.accaouiPreviousStartOralExamSessionV2315 =
    window.accaouiPreviousStartOralExamSessionV2315 ||
    window.startOralExamSessionV220;

  window.startOralExamSessionV220 = function patchedStartOralExamSessionV2315(questions, title) {
    if (typeof window.accaouiPreviousStartOralExamSessionV2315 === "function") {
      const result = window.accaouiPreviousStartOralExamSessionV2315(questions, title);
      scheduleOralPolishV2315();
      return result;
    }

    showSmallNotice("Mündliche Prüfungsrunde konnte nicht gestartet werden.");
  };
}

/* =====================================================
   v23.1.7 MÜNDLICHE PRÜFUNG – 15-MINUTEN-SIMULATION MIT 3 PRÜFERN
   Ziel:
   - 15 mündliche Trainingsfragen sicherstellen
   - 15-Minuten-Simulation startet 15 Fragen
   - Frage 1–5: Prüfer 1 aktiv
   - Frage 6–10: Vorsitz aktiv
   - Frage 11–15: Prüfer 3 aktiv
   - Timer 15:00 Minuten
   - eigene Accaoui-Trainingslogik, keine offizielle IHK-Bewertung
===================================================== */

if (!window.ACCAOUI_V2317_ORAL_THREE_EXAMINER_SIM_PATCH) {
  window.ACCAOUI_V2317_ORAL_THREE_EXAMINER_SIM_PATCH = true;

  const IHK_ORAL_CATEGORY_ORDER_V2317 = [
    "Recht der öffentlichen Sicherheit und Ordnung",
    "Gewerberecht",
    "Datenschutzrecht",
    "Bürgerliches Gesetzbuch",
    "Straf- und Strafverfahrensrecht",
    "Unfallverhütungsvorschrift",
    "Umgang mit Waffen",
    "Umgang mit Menschen",
    "Grundzüge der Sicherheitstechnik"
  ];

  const ORAL_EXAM_EXTRA_QUESTIONS_V2317 = [
    {
      id: "oral_v2317_roso_002",
      category: "Recht der öffentlichen Sicherheit und Ordnung",
      question: "Welche Grenze besteht zwischen privatem Sicherheitsdienst und staatlicher Gefahrenabwehr?",
      sampleAnswer: "Private Sicherheitsmitarbeiter handeln grundsätzlich nicht hoheitlich. Sie dürfen im Rahmen von Hausrecht, Besitzrecht, Jedermannsrechten oder privatrechtlichen Befugnissen tätig werden. Staatliche Gefahrenabwehr und hoheitliche Maßnahmen bleiben grundsätzlich Aufgabe der zuständigen Behörden.",
      examinerNote: "Wichtig ist die klare Abgrenzung: privat handeln, keine automatische Polizeibefugnis."
    },
    {
      id: "oral_v2317_gewo_002",
      category: "Gewerberecht",
      question: "Welche Bedeutung haben Zuverlässigkeit und geeigneter Nachweis im Bewachungsgewerbe?",
      sampleAnswer: "Zuverlässigkeit ist eine zentrale Voraussetzung im Bewachungsgewerbe. Je nach Tätigkeit ist außerdem ein geeigneter Nachweis erforderlich, zum Beispiel Unterrichtung oder Sachkundeprüfung. Ohne diese Voraussetzungen kann eine Tätigkeit untersagt oder nicht erlaubt werden.",
      examinerNote: "Gute Antwort nennt Zuverlässigkeit, Unterrichtung/Sachkunde und behördliche Kontrolle."
    },
    {
      id: "oral_v2317_ds_002",
      category: "Datenschutzrecht",
      question: "Was muss ein Sicherheitsmitarbeiter beim Umgang mit personenbezogenen Daten besonders beachten?",
      sampleAnswer: "Personenbezogene Daten dürfen nur zweckgebunden, vertraulich und auf einer zulässigen Grundlage verarbeitet werden. Sie dürfen nicht aus Neugier eingesehen, privat weitergegeben oder länger als erforderlich gespeichert werden.",
      examinerNote: "Wichtig sind Zweckbindung, Vertraulichkeit, Datenminimierung und keine private Weitergabe."
    },
    {
      id: "oral_v2317_bgb_002",
      category: "Bürgerliches Gesetzbuch",
      question: "Welche Rolle spielt das Hausrecht in der praktischen Arbeit eines Sicherheitsmitarbeiters?",
      sampleAnswer: "Das Hausrecht erlaubt dem Berechtigten oder Beauftragten zu bestimmen, wer ein Objekt betreten oder dort bleiben darf. Sicherheitsmitarbeiter können im Auftrag des Hausrechtsinhabers Personen ansprechen, zum Verlassen auffordern oder ein Hausverbot durchsetzen, soweit dies rechtlich zulässig und verhältnismäßig ist.",
      examinerNote: "Wichtig: Hausrecht ist privatrechtlich, aber nicht grenzenlos."
    },
    {
      id: "oral_v2317_straf_002",
      category: "Straf- und Strafverfahrensrecht",
      question: "Welche Voraussetzungen müssen bei einer vorläufigen Festnahme durch Jedermann besonders geprüft werden?",
      sampleAnswer: "Es muss eine Person auf frischer Tat betroffen oder verfolgt sein. Zusätzlich muss Fluchtverdacht bestehen oder die Identität darf nicht sofort feststellbar sein. Die Polizei ist unverzüglich zu informieren und die Maßnahme muss verhältnismäßig bleiben.",
      examinerNote: "Prüfer achten auf frische Tat, Fluchtverdacht oder Identitätsfeststellung und sofortige Polizei."
    },
    {
      id: "oral_v2317_umm_002",
      category: "Umgang mit Menschen",
      question: "Wie sprechen Sie eine provozierende Person professionell an?",
      sampleAnswer: "Ich bleibe ruhig, halte Sicherheitsabstand, spreche klar und respektvoll, vermeide Gegenprovokationen und setze eindeutige Grenzen. Wenn die Situation eskaliert, hole ich Unterstützung und handle nach Dienstanweisung.",
      examinerNote: "Wichtig sind Deeskalation, Eigensicherung, klare Sprache und keine Eskalation durch den Sicherheitsmitarbeiter."
    }
  ];

  let oralSimulationTimerV2317 = null;
  let oralSimulationSecondsLeftV2317 = 15 * 60;

  function installExtraOralQuestionsV2317() {
    if (!Array.isArray(ORAL_EXAM_QUESTIONS_V220)) return;

    ORAL_EXAM_EXTRA_QUESTIONS_V2317.forEach(extraQuestion => {
      const exists = ORAL_EXAM_QUESTIONS_V220.some(existingQuestion => {
        return (
          existingQuestion.id === extraQuestion.id ||
          existingQuestion.question === extraQuestion.question
        );
      });

      if (!exists) {
        ORAL_EXAM_QUESTIONS_V220.push(extraQuestion);
      }
    });
  }

  function getIhkOrderedOralQuestionsV2317() {
    installExtraOralQuestionsV2317();

    const questions = Array.isArray(ORAL_EXAM_QUESTIONS_V220)
      ? [...ORAL_EXAM_QUESTIONS_V220]
      : [];

    return questions.sort((a, b) => {
      const categoryA = String(a.category || "");
      const categoryB = String(b.category || "");

      const indexA = IHK_ORAL_CATEGORY_ORDER_V2317.indexOf(categoryA);
      const indexB = IHK_ORAL_CATEGORY_ORDER_V2317.indexOf(categoryB);

      const safeA = indexA >= 0 ? indexA : 999;
      const safeB = indexB >= 0 ? indexB : 999;

      return safeA - safeB;
    });
  }

  function getFifteenMinuteOralQuestionsV2317() {
    const orderedQuestions = getIhkOrderedOralQuestionsV2317();

    return orderedQuestions.slice(0, 15);
  }

  function clearOralSimulationTimerV2317() {
    if (oralSimulationTimerV2317) {
      clearInterval(oralSimulationTimerV2317);
      oralSimulationTimerV2317 = null;
    }
  }

  function formatOralSimulationTimeV2317(seconds) {
    const safeSeconds = Math.max(0, Number(seconds || 0));
    const minutes = Math.floor(safeSeconds / 60);
    const restSeconds = safeSeconds % 60;

    return String(minutes).padStart(2, "0") + ":" + String(restSeconds).padStart(2, "0");
  }

  function renderOralSimulationTimerV2317() {
    if (window.ACCAOUI_V2317_ORAL_SIMULATION_MODE !== "15") return;

    const header = document.querySelector(".oral-session-header");

    if (!header) return;

    let timer = document.getElementById("oralSimulationTimerV2317");

    if (!timer) {
      timer = document.createElement("div");
      timer.id = "oralSimulationTimerV2317";
      timer.className = "oral-simulation-timer-v2317";
      header.appendChild(timer);
    }

    timer.innerHTML = `
      <span>Prüfungszeit</span>
      <strong>${formatOralSimulationTimeV2317(oralSimulationSecondsLeftV2317)}</strong>
    `;
  }

  function startOralSimulationTimerV2317() {
    clearOralSimulationTimerV2317();

    oralSimulationSecondsLeftV2317 = 15 * 60;

    renderOralSimulationTimerV2317();

    oralSimulationTimerV2317 = setInterval(() => {
      oralSimulationSecondsLeftV2317--;

      renderOralSimulationTimerV2317();

      if (oralSimulationSecondsLeftV2317 <= 0) {
        clearOralSimulationTimerV2317();

        if (typeof showSmallNotice === "function") {
          showSmallNotice("Die 15 Minuten sind abgelaufen.");
        }

        if (typeof showOralExamFinishScreenV220 === "function") {
          showOralExamFinishScreenV220();
        }
      }
    }, 1000);
  }

  function getActiveExaminerIndexV2317() {
    const currentIndex = typeof oralExamIndexV220 !== "undefined"
      ? Number(oralExamIndexV220 || 0)
      : 0;

    if (currentIndex < 5) return 0;
    if (currentIndex < 10) return 1;
    return 2;
  }

  function getActiveExaminerLabelV2317(index) {
    if (index === 0) return "Prüfer 1 fragt";
    if (index === 1) return "Vorsitz fragt";
    return "Prüfer 3 fragt";
  }

  function updateActiveExaminerV2317() {
    const scenes = document.querySelectorAll(".oral-room-scene-v221.is-session");

    scenes.forEach(scene => {
      const examiners = scene.querySelectorAll(".oral-examiner-row-v221 .oral-person-v221");

      if (!examiners.length) return;

      const isSimulation = window.ACCAOUI_V2317_ORAL_SIMULATION_MODE === "15";
      const activeIndex = isSimulation ? getActiveExaminerIndexV2317() : 0;

      scene.classList.toggle("oral-three-examiner-simulation-v2317", isSimulation);

      examiners.forEach((examiner, index) => {
        examiner.classList.remove("is-active-examiner-v2317");

        const status = examiner.querySelector("span");

        if (isSimulation) {
          if (index === 0 && status) status.textContent = "Frage 1–5";
          if (index === 1 && status) status.textContent = "Frage 6–10";
          if (index === 2 && status) status.textContent = "Frage 11–15";
        }

        if (index === activeIndex) {
  examiner.classList.add("is-active-examiner-v2317");

  if (status) {
    if (index === 0) status.textContent = "Frage 1–5";
    if (index === 1) status.textContent = "Frage 6–10";
    if (index === 2) status.textContent = "Frage 11–15";
  }
}
      });

      const roomStatus = scene.querySelector(".oral-room-status-v221");

      if (roomStatus && isSimulation) {
        roomStatus.textContent = getActiveExaminerLabelV2317(activeIndex);
      }
    });
  }

  function scheduleOralSimulationPolishV2317() {
    setTimeout(updateActiveExaminerV2317, 40);
    setTimeout(updateActiveExaminerV2317, 180);
    setTimeout(updateActiveExaminerV2317, 420);
    setTimeout(renderOralSimulationTimerV2317, 420);
  }

  installExtraOralQuestionsV2317();

  window.accaouiPreviousStartOralSimulation15V2317 =
    window.startOralSimulation15V2314;

  window.startOralSimulation15V2314 = function patchedStartOralSimulation15V2317() {
    if (typeof closeOralModeSheetV2314 === "function") {
      closeOralModeSheetV2314();
    }

    const questions = getFifteenMinuteOralQuestionsV2317();

    if (questions.length < 15 && typeof showSmallNotice === "function") {
      showSmallNotice("Es sind aktuell weniger als 15 mündliche Fragen vorhanden.");
    }

    window.ACCAOUI_V2317_STARTING_15_SIMULATION = true;

    startOralExamSessionV220(
      questions,
      "15-Minuten-Prüfungssimulation"
    );

    window.ACCAOUI_V2317_STARTING_15_SIMULATION = false;

    startOralSimulationTimerV2317();
    scheduleOralSimulationPolishV2317();
  };

  window.accaouiPreviousStartOralExamSessionV2317 =
    window.accaouiPreviousStartOralExamSessionV2317 ||
    window.startOralExamSessionV220;

  window.startOralExamSessionV220 = function patchedStartOralExamSessionV2317(questions, title) {
    const isStarting15 = window.ACCAOUI_V2317_STARTING_15_SIMULATION === true;

    if (!isStarting15) {
      window.ACCAOUI_V2317_ORAL_SIMULATION_MODE = "training";
      clearOralSimulationTimerV2317();
    } else {
      window.ACCAOUI_V2317_ORAL_SIMULATION_MODE = "15";
    }

    if (typeof window.accaouiPreviousStartOralExamSessionV2317 === "function") {
      const result = window.accaouiPreviousStartOralExamSessionV2317(questions, title);

      scheduleOralSimulationPolishV2317();

      return result;
    }

    showSmallNotice("Mündliche Prüfungsrunde konnte nicht gestartet werden.");
  };

  window.accaouiPreviousRateOralExamQuestionV2317 =
    window.accaouiPreviousRateOralExamQuestionV2317 ||
    window.rateOralExamQuestionV220;

  window.rateOralExamQuestionV220 = function patchedRateOralExamQuestionV2317(status) {
    if (typeof window.accaouiPreviousRateOralExamQuestionV2317 === "function") {
      const result = window.accaouiPreviousRateOralExamQuestionV2317(status);

      scheduleOralSimulationPolishV2317();

      return result;
    }

    showSmallNotice("Bewertung konnte nicht gespeichert werden.");
  };

  window.accaouiPreviousPreviousOralExamQuestionV2317 =
    window.accaouiPreviousPreviousOralExamQuestionV2317 ||
    window.previousOralExamQuestionV220;

  window.previousOralExamQuestionV220 = function patchedPreviousOralExamQuestionV2317() {
    if (typeof window.accaouiPreviousPreviousOralExamQuestionV2317 === "function") {
      const result = window.accaouiPreviousPreviousOralExamQuestionV2317();

      scheduleOralSimulationPolishV2317();

      return result;
    }

    showSmallNotice("Zurück nicht möglich.");
  };

  window.accaouiPreviousShowOralExamFinishScreenV2317 =
    window.accaouiPreviousShowOralExamFinishScreenV2317 ||
    window.showOralExamFinishScreenV220;

  window.showOralExamFinishScreenV220 = function patchedShowOralExamFinishScreenV2317() {
    clearOralSimulationTimerV2317();

    if (typeof window.accaouiPreviousShowOralExamFinishScreenV2317 === "function") {
      return window.accaouiPreviousShowOralExamFinishScreenV2317();
    }
  };

  window.getFifteenMinuteOralQuestionsV2317 = getFifteenMinuteOralQuestionsV2317;
  window.updateActiveExaminerV2317 = updateActiveExaminerV2317;
}

/* =====================================================
   v23.2.0 MÜNDLICHE PRÜFUNG – PRÜFUNGSBOGEN A
   Ziel:
   - 15-Minuten-Simulation nutzt festen Prüfungsbogen
   - 3 Prüfer × 5 Fragen
   - keine Zufallslogik mehr für diesen Modus
   - eigene Accaoui-Trainingsfragen, keine Original-IHK-Fragen
===================================================== */

if (!window.ACCAOUI_V2320_ORAL_EXAM_SHEET_A_PATCH) {
  window.ACCAOUI_V2320_ORAL_EXAM_SHEET_A_PATCH = true;

  function getOralExamSheetAQuestionsV2320() {
    if (
      !window.AccaouiOralSheets ||
      typeof window.AccaouiOralSheets.getSheetAQuestions !== "function"
    ) {
      return [];
    }

    const questions = window.AccaouiOralSheets.getSheetAQuestions();

    if (!Array.isArray(questions) || questions.length !== 15) {
      return [];
    }

    return questions;
  }

  function getCurrentOralSheetQuestionV2320() {
    if (
      typeof oralExamQuestionsV220 !== "undefined" &&
      Array.isArray(oralExamQuestionsV220) &&
      typeof oralExamIndexV220 !== "undefined"
    ) {
      return oralExamQuestionsV220[oralExamIndexV220];
    }

    return null;
  }

  function updateOralSheetLabelsV2320() {
    if (window.ACCAOUI_V2317_ORAL_SIMULATION_MODE !== "15") return;

    const question = getCurrentOralSheetQuestionV2320();
    const scene = document.querySelector(".oral-room-scene-v221.is-session");

    if (!scene || !question) return;

    const status = scene.querySelector(".oral-room-status-v221");

    if (status && question.examinerName) {
      status.textContent = question.examinerName + " fragt";
    }

    const bubble = scene.querySelector(".oral-room-question-prompt-v222");

    if (bubble && question.examinerBlockTitle) {
      bubble.dataset.examinerBlock = question.examinerBlockTitle;
    }
  }

  function scheduleOralSheetLabelsV2320() {
    setTimeout(updateOralSheetLabelsV2320, 60);
    setTimeout(updateOralSheetLabelsV2320, 220);
    setTimeout(updateOralSheetLabelsV2320, 460);
  }

  window.startOralSimulation15V2314 = function startOralSimulationSheetAV2320() {
    if (typeof closeOralModeSheetV2314 === "function") {
      closeOralModeSheetV2314();
    }

    const questions = getOralExamSheetAQuestionsV2320();

    if (questions.length !== 15) {
      showSmallNotice("Prüfungsbogen A konnte nicht geladen werden.");
      return;
    }

    window.ACCAOUI_V2317_STARTING_15_SIMULATION = true;

    startOralExamSessionV220(
      questions,
      "15-Minuten-Simulation · Prüfungsbogen A"
    );

    window.ACCAOUI_V2317_STARTING_15_SIMULATION = false;

    if (typeof startOralSimulationTimerV2317 === "function") {
      startOralSimulationTimerV2317();
    }

    if (typeof updateActiveExaminerV2317 === "function") {
      updateActiveExaminerV2317();
    }

    scheduleOralSheetLabelsV2320();
  };

  window.accaouiPreviousRateOralExamQuestionV2320 =
    window.accaouiPreviousRateOralExamQuestionV2320 ||
    window.rateOralExamQuestionV220;

  window.rateOralExamQuestionV220 = function patchedRateOralExamQuestionV2320(status) {
    if (typeof window.accaouiPreviousRateOralExamQuestionV2320 === "function") {
      const result = window.accaouiPreviousRateOralExamQuestionV2320(status);

      scheduleOralSheetLabelsV2320();

      return result;
    }

    showSmallNotice("Bewertung konnte nicht gespeichert werden.");
  };

  window.accaouiPreviousPreviousOralExamQuestionV2320 =
    window.accaouiPreviousPreviousOralExamQuestionV2320 ||
    window.previousOralExamQuestionV220;

  window.previousOralExamQuestionV220 = function patchedPreviousOralExamQuestionV2320() {
    if (typeof window.accaouiPreviousPreviousOralExamQuestionV2320 === "function") {
      const result = window.accaouiPreviousPreviousOralExamQuestionV2320();

      scheduleOralSheetLabelsV2320();

      return result;
    }

    showSmallNotice("Zurück nicht möglich.");
  };

  window.getOralExamSheetAQuestionsV2320 = getOralExamSheetAQuestionsV2320;
}

/* =====================================================
   v23.2.1 MÜNDLICHE PRÜFUNG – AUSWERTUNG NACH PRÜFERBLÖCKEN
   Ziel:
   - 15-Minuten-Simulation wird nach 3 Prüferblöcken ausgewertet
   - Prüfer 1 / Vorsitz / Prüfer 3 getrennt anzeigen
   - offene Fragen werden nicht als falsch gewertet
   - eigene Accaoui-Trainingsbewertung, keine offizielle IHK-Bewertung
===================================================== */

if (!window.ACCAOUI_V2321_ORAL_BLOCK_RESULT_PATCH) {
  window.ACCAOUI_V2321_ORAL_BLOCK_RESULT_PATCH = true;

  let oralExamRatingsV2321 = [];

  function isOralSheetASessionV2321() {
    try {
      return (
        window.ACCAOUI_V2317_ORAL_SIMULATION_MODE === "15" &&
        Array.isArray(oralExamQuestionsV220) &&
        oralExamQuestionsV220.some(question => question && question.sheetId === "oral_sheet_a_v2320")
      );
    } catch (error) {
      return false;
    }
  }

  function resetOralRatingsV2321() {
    oralExamRatingsV2321 = [];
  }

  function getCurrentOralQuestionIndexV2321() {
    try {
      return Number(oralExamIndexV220 || 0);
    } catch (error) {
      return 0;
    }
  }

  function getCurrentOralQuestionV2321() {
    try {
      if (Array.isArray(oralExamQuestionsV220)) {
        return oralExamQuestionsV220[getCurrentOralQuestionIndexV2321()];
      }
    } catch (error) {
      return null;
    }

    return null;
  }

  function getExaminerIndexForQuestionV2321(question, fallbackIndex) {
    if (question && Number.isInteger(question.examinerIndex)) {
      return question.examinerIndex;
    }

    if (fallbackIndex < 5) return 0;
    if (fallbackIndex < 10) return 1;
    return 2;
  }

  function saveOralRatingV2321(status) {
    if (!isOralSheetASessionV2321()) return;

    const questionIndex = getCurrentOralQuestionIndexV2321();
    const question = getCurrentOralQuestionV2321();

    oralExamRatingsV2321[questionIndex] = {
      index: questionIndex,
      status: status === "known" ? "known" : "practice",
      questionId: question && question.id ? question.id : "oral_question_" + questionIndex,
      category: question && question.category ? question.category : "Ohne Kategorie",
      examinerIndex: getExaminerIndexForQuestionV2321(question, questionIndex),
      examinerName: question && question.examinerName ? question.examinerName : "",
      blockTitle: question && question.examinerBlockTitle ? question.examinerBlockTitle : ""
    };
  }

  function getOralBlockDefinitionsV2321() {
    return [
      {
        examinerIndex: 0,
        examinerName: "Prüfer 1",
        title: "Öffentliches Recht / Gewerberecht",
        range: "Frage 1–5"
      },
      {
        examinerIndex: 1,
        examinerName: "Vorsitz",
        title: "Umgang mit Menschen",
        range: "Frage 6–10"
      },
      {
        examinerIndex: 2,
        examinerName: "Prüfer 3",
        title: "Mischblock",
        range: "Frage 11–15"
      }
    ];
  }

  function getOralBlockResultStatsV2321() {
    const questions = Array.isArray(oralExamQuestionsV220)
      ? oralExamQuestionsV220
      : [];

    const blocks = getOralBlockDefinitionsV2321();

    return blocks.map(block => {
      const blockQuestions = questions.filter((question, index) => {
        return getExaminerIndexForQuestionV2321(question, index) === block.examinerIndex;
      });

      const blockRatings = oralExamRatingsV2321.filter(rating => {
        return rating && rating.examinerIndex === block.examinerIndex;
      });

      const known = blockRatings.filter(rating => rating.status === "known").length;
      const practice = blockRatings.filter(rating => rating.status === "practice").length;
      const answered = known + practice;
      const total = blockQuestions.length || 5;
      const open = Math.max(0, total - answered);
      const percent = answered > 0 ? Math.round((known / answered) * 100) : 0;

      return {
        ...block,
        total,
        answered,
        known,
        practice,
        open,
        percent
      };
    });
  }

  function getOverallOralResultV2321(blockStats) {
    const total = blockStats.reduce((sum, block) => sum + block.total, 0);
    const known = blockStats.reduce((sum, block) => sum + block.known, 0);
    const practice = blockStats.reduce((sum, block) => sum + block.practice, 0);
    const answered = known + practice;
    const open = Math.max(0, total - answered);
    const percent = answered > 0 ? Math.round((known / answered) * 100) : 0;

    return {
      total,
      known,
      practice,
      answered,
      open,
      percent
    };
  }

  function getOralTrainingLabelV2321(percent) {
    if (percent >= 90) return "Sehr sicher";
    if (percent >= 75) return "Sicher";
    if (percent >= 60) return "Teilweise sicher";
    if (percent >= 40) return "Unsicher";
    return "Deutlich nacharbeiten";
  }

  function renderOralExamBlockFinishV2321() {
    const mainContent = document.querySelector(".main-content");

    if (!mainContent) return;

    const blockStats = getOralBlockResultStatsV2321();
    const overall = getOverallOralResultV2321(blockStats);
    const label = getOralTrainingLabelV2321(overall.percent);

    const blockCards = blockStats.map(block => {
      return `
        <div class="oral-block-result-card-v2321">
          <div class="oral-block-result-head-v2321">
            <span>${escapeHtml(block.examinerName)}</span>
            <strong>${escapeHtml(block.range)}</strong>
          </div>

          <h3>${escapeHtml(block.title)}</h3>

          <div class="oral-block-result-percent-v2321">
            ${block.percent}%
          </div>

          <div class="oral-block-result-mini-v2321">
            <div class="success">
              <span>Sicher</span>
              <strong>${block.known}</strong>
            </div>

            <div class="danger">
              <span>Noch üben</span>
              <strong>${block.practice}</strong>
            </div>

            <div>
              <span>Offen</span>
              <strong>${block.open}</strong>
            </div>
          </div>
        </div>
      `;
    }).join("");

    mainContent.innerHTML = `
      <button class="back-btn" onclick="showOralExamPage()">
        ← Zurück zur mündlichen Prüfung
      </button>

      <section class="result-wrapper oral-block-result-wrapper-v2321">

        <div class="oral-block-result-hero-v2321">
          <p class="eyebrow">15-Minuten-Simulation</p>

          <h1>Prüfungsbogen A abgeschlossen</h1>

          <p>
            Die Auswertung zeigt Ihre Trainingsleistung nach Prüferblöcken.
            Offene Fragen werden nicht als falsch gewertet.
          </p>

          <div class="oral-block-overall-v2321">
            <strong>${overall.percent}%</strong>
            <span>${escapeHtml(label)}</span>
          </div>

          <p class="oral-block-legal-note-v2321">
            Trainingsbewertung. Keine offizielle IHK-Bewertung.
          </p>
        </div>

        <div class="oral-block-result-grid-v2321">
          ${blockCards}
        </div>

        <div class="oral-block-summary-v2321">
          <div>
            <span>Bearbeitet</span>
            <strong>${overall.answered}/${overall.total}</strong>
          </div>

          <div class="success">
            <span>Sicher</span>
            <strong>${overall.known}</strong>
          </div>

          <div class="danger">
            <span>Noch üben</span>
            <strong>${overall.practice}</strong>
          </div>

          <div>
            <span>Offen</span>
            <strong>${overall.open}</strong>
          </div>
        </div>

        <div class="result-actions oral-block-actions-v2321">
          <button class="next-btn" onclick="startOralSimulation15V2314()">
            Prüfungsbogen A wiederholen
          </button>

          <button class="next-btn" onclick="showOralExamPage()">
            Zur Modusauswahl
          </button>

          <button class="next-btn secondary-btn" onclick="location.reload()">
            Zurück zum Dashboard
          </button>
        </div>

      </section>
    `;
  }

  window.accaouiPreviousStartOralExamSessionV2321 =
    window.accaouiPreviousStartOralExamSessionV2321 ||
    window.startOralExamSessionV220;

  window.startOralExamSessionV220 = function patchedStartOralExamSessionV2321(questions, title) {
    const isSheetA =
      Array.isArray(questions) &&
      questions.some(question => question && question.sheetId === "oral_sheet_a_v2320");

    if (isSheetA) {
      resetOralRatingsV2321();
    }

    if (typeof window.accaouiPreviousStartOralExamSessionV2321 === "function") {
      return window.accaouiPreviousStartOralExamSessionV2321(questions, title);
    }

    showSmallNotice("Mündliche Prüfungsrunde konnte nicht gestartet werden.");
  };

  window.accaouiPreviousRateOralExamQuestionV2321 =
    window.accaouiPreviousRateOralExamQuestionV2321 ||
    window.rateOralExamQuestionV220;

  window.rateOralExamQuestionV220 = function patchedRateOralExamQuestionV2321(status) {
    saveOralRatingV2321(status);

    if (typeof window.accaouiPreviousRateOralExamQuestionV2321 === "function") {
      return window.accaouiPreviousRateOralExamQuestionV2321(status);
    }

    showSmallNotice("Bewertung konnte nicht gespeichert werden.");
  };

  window.accaouiPreviousShowOralExamFinishScreenV2321 =
    window.accaouiPreviousShowOralExamFinishScreenV2321 ||
    window.showOralExamFinishScreenV220;

  window.showOralExamFinishScreenV220 = function patchedShowOralExamFinishScreenV2321() {
    if (isOralSheetASessionV2321()) {
      if (typeof window.accaouiPreviousShowOralExamFinishScreenV2321 === "function") {
        window.accaouiPreviousShowOralExamFinishScreenV2321();
      }

      renderOralExamBlockFinishV2321();
      return;
    }

    if (typeof window.accaouiPreviousShowOralExamFinishScreenV2321 === "function") {
      return window.accaouiPreviousShowOralExamFinishScreenV2321();
    }
  };

  try {
    startOralExamSessionV220 = window.startOralExamSessionV220;
    rateOralExamQuestionV220 = window.rateOralExamQuestionV220;
    showOralExamFinishScreenV220 = window.showOralExamFinishScreenV220;
  } catch (error) {
    /* Rebinding ist je nach Browser nicht notwendig */
  }

  window.renderOralExamBlockFinishV2321 = renderOralExamBlockFinishV2321;
  window.getOralBlockResultStatsV2321 = getOralBlockResultStatsV2321;
}

/* =====================================================
   v23.2.2 MÜNDLICHE PRÜFUNG – AUSWERTUNG VEREDLUNG
   Ziel:
   - Ergebnis-Auswertung verständlicher machen
   - Mischblock erklären
   - Empfehlung anzeigen
   - weiterhin Accaoui-Trainingsbewertung, keine IHK-Bewertung
===================================================== */

if (!window.ACCAOUI_V2322_ORAL_RESULT_POLISH_PATCH) {
  window.ACCAOUI_V2322_ORAL_RESULT_POLISH_PATCH = true;

  function getOralResultRecommendationV2322(overall) {
    const percent = Number(overall && overall.percent ? overall.percent : 0);
    const practice = Number(overall && overall.practice ? overall.practice : 0);

    if (percent >= 90 && practice === 0) {
      return {
        title: "Sehr starke mündliche Runde",
        text: "Die Antworten wurden sehr sicher bewertet. Wiederholen Sie die Formulierungen regelmäßig laut, damit sie in der Prüfung ruhig und klar abrufbar bleiben."
      };
    }

    if (percent >= 75) {
      return {
        title: "Gute Grundlage",
        text: "Die mündliche Struktur ist vorhanden. Arbeiten Sie gezielt an den Antworten, die mit „Noch üben“ bewertet wurden."
      };
    }

    if (percent >= 60) {
      return {
        title: "Teilweise sicher",
        text: "Einige Antworten sitzen bereits. Wiederholen Sie die schwächeren Prüferblöcke laut und achten Sie auf rechtlich saubere Begriffe."
      };
    }

    return {
      title: "Gezielt nacharbeiten",
      text: "Die mündliche Prüfung braucht klare, ruhige und vollständige Antworten. Beginnen Sie mit dem Prüferblock, in dem die meisten Antworten mit „Noch üben“ bewertet wurden."
    };
  }

  function getOralBlockDisplayTitleV2322(block) {
    const title = String(block && block.title ? block.title : "");

    if (title === "Mischblock") {
      return "Mischblock – weitere Sachgebiete";
    }

    return title;
  }

  function getOralBlockDescriptionV2322(block) {
    const title = String(block && block.title ? block.title : "");

    if (title.includes("Öffentliches Recht") || title.includes("Gewerberecht")) {
      return "Abgrenzung privater Sicherheitsdienst, § 34a GewO, Zuverlässigkeit und Pflichten.";
    }

    if (title.includes("Umgang mit Menschen")) {
      return "Kommunikation, Deeskalation, Eigensicherung und professionelles Auftreten.";
    }

    if (title === "Mischblock") {
      return "Datenschutz, BGB, Strafrecht, UVV, Waffenrecht und Sicherheitstechnik.";
    }

    return "Zusammenfassung dieses Prüferblocks.";
  }

  function renderOralExamBlockFinishV2322() {
    if (typeof getOralBlockResultStatsV2321 !== "function") {
      if (typeof window.renderOralExamBlockFinishV2321 === "function") {
        window.renderOralExamBlockFinishV2321();
      }
      return;
    }

    const mainContent = document.querySelector(".main-content");

    if (!mainContent) return;

    const blockStats = getOralBlockResultStatsV2321();

    const total = blockStats.reduce((sum, block) => sum + block.total, 0);
    const known = blockStats.reduce((sum, block) => sum + block.known, 0);
    const practice = blockStats.reduce((sum, block) => sum + block.practice, 0);
    const answered = known + practice;
    const open = Math.max(0, total - answered);
    const percent = answered > 0 ? Math.round((known / answered) * 100) : 0;

    const overall = {
      total,
      known,
      practice,
      answered,
      open,
      percent
    };

    const label =
      percent >= 90 ? "Sehr sicher" :
      percent >= 75 ? "Sicher" :
      percent >= 60 ? "Teilweise sicher" :
      percent >= 40 ? "Unsicher" :
      "Deutlich nacharbeiten";

    const recommendation = getOralResultRecommendationV2322(overall);

    const blockCards = blockStats.map(block => {
      return `
        <div class="oral-block-result-card-v2321 oral-block-result-card-v2322">
          <div class="oral-block-result-head-v2321">
            <span>${escapeHtml(block.examinerName)}</span>
            <strong>${escapeHtml(block.range)}</strong>
          </div>

          <h3>${escapeHtml(getOralBlockDisplayTitleV2322(block))}</h3>

          <p class="oral-block-description-v2322">
            ${escapeHtml(getOralBlockDescriptionV2322(block))}
          </p>

          <div class="oral-block-result-percent-v2321">
            ${block.percent}%
          </div>

          <div class="oral-block-result-mini-v2321">
            <div class="success">
              <span>Sicher</span>
              <strong>${block.known}</strong>
            </div>

            <div class="danger">
              <span>Noch üben</span>
              <strong>${block.practice}</strong>
            </div>

            <div>
              <span>Offen</span>
              <strong>${block.open}</strong>
            </div>
          </div>
        </div>
      `;
    }).join("");

    mainContent.innerHTML = `
      <button class="back-btn" onclick="showOralExamPage()">
        ← Zurück zur mündlichen Prüfung
      </button>

      <section class="result-wrapper oral-block-result-wrapper-v2321 oral-block-result-wrapper-v2322">

        <div class="oral-block-result-hero-v2321 oral-block-result-hero-v2322">
          <p class="eyebrow">15-Minuten-Simulation</p>

          <h1>Prüfungsbogen A abgeschlossen</h1>

          <p>
            Die Auswertung zeigt Ihre Trainingsleistung nach Prüferblöcken.
            Offene Fragen werden nicht als falsch gewertet.
          </p>

          <div class="oral-block-overall-v2321">
            <strong>${overall.percent}%</strong>
            <span>${escapeHtml(label)}</span>
          </div>

          <p class="oral-block-legal-note-v2321">
            Trainingsbewertung. Keine offizielle IHK-Bewertung.
          </p>
        </div>

        <div class="oral-block-result-grid-v2321">
          ${blockCards}
        </div>

        <div class="oral-result-recommendation-v2322">
          <span>Empfehlung</span>
          <strong>${escapeHtml(recommendation.title)}</strong>
          <p>${escapeHtml(recommendation.text)}</p>
        </div>

        <div class="oral-block-summary-v2321">
          <div>
            <span>Bearbeitet</span>
            <strong>${overall.answered}/${overall.total}</strong>
          </div>

          <div class="success">
            <span>Sicher</span>
            <strong>${overall.known}</strong>
          </div>

          <div class="danger">
            <span>Noch üben</span>
            <strong>${overall.practice}</strong>
          </div>

          <div>
            <span>Offen</span>
            <strong>${overall.open}</strong>
          </div>
        </div>

        <div class="result-actions oral-block-actions-v2321">
          <button class="next-btn" onclick="startOralSimulation15V2314()">
            Prüfungsbogen A wiederholen
          </button>

          <button class="next-btn" onclick="showOralExamPage()">
            Zur Modusauswahl
          </button>

          <button class="next-btn secondary-btn" onclick="location.reload()">
            Zurück zum Dashboard
          </button>
        </div>

      </section>
    `;
  }

  window.accaouiPreviousShowOralExamFinishScreenV2322 =
    window.accaouiPreviousShowOralExamFinishScreenV2322 ||
    window.showOralExamFinishScreenV220;

  window.showOralExamFinishScreenV220 = function patchedShowOralExamFinishScreenV2322() {
    try {
      if (
        window.ACCAOUI_V2317_ORAL_SIMULATION_MODE === "15" &&
        typeof oralExamQuestionsV220 !== "undefined" &&
        Array.isArray(oralExamQuestionsV220) &&
        oralExamQuestionsV220.some(question => question && question.sheetId === "oral_sheet_a_v2320")
      ) {
        renderOralExamBlockFinishV2322();
        return;
      }
    } catch (error) {
      console.warn("v23.2.2 Ergebnis-Patch konnte Prüfungsbogen nicht erkennen:", error);
    }

    if (typeof window.accaouiPreviousShowOralExamFinishScreenV2322 === "function") {
      return window.accaouiPreviousShowOralExamFinishScreenV2322();
    }
  };

  try {
    showOralExamFinishScreenV220 = window.showOralExamFinishScreenV220;
  } catch (error) {
    /* Rebinding ist je nach Browser nicht nötig */
  }

  window.renderOralExamBlockFinishV2322 = renderOralExamBlockFinishV2322;
}

/* =====================================================
   v23.2.3 AUSWERTUNG NACHARBEITEN + THEMENWERTE RUHIGER
   Ziel:
   - Nach Prüfung: Prüfungsbogen A nacharbeiten
   - 15 Fragen mit Musterantwort und Prüfer-Hinweis anzeigen
   - Themenkarten-Werte kompakter als ruhige Statistikzeile darstellen
===================================================== */

if (!window.ACCAOUI_V2323_REVIEW_AND_TOPIC_STATS_PATCH) {
  window.ACCAOUI_V2323_REVIEW_AND_TOPIC_STATS_PATCH = true;

  function getOralSheetAQuestionsForReviewV2323() {
    if (typeof getOralExamSheetAQuestionsV2320 === "function") {
      return getOralExamSheetAQuestionsV2320();
    }

    try {
      if (Array.isArray(oralExamQuestionsV220)) {
        const sheetQuestions = oralExamQuestionsV220.filter(question => {
          return question && question.sheetId === "oral_sheet_a_v2320";
        });

        if (sheetQuestions.length) return sheetQuestions;
      }
    } catch (error) {
      return [];
    }

    return [];
  }

  function showOralSheetAReviewV2323() {
    const mainContent = document.querySelector(".main-content");

    if (!mainContent) return;

    const questions = getOralSheetAQuestionsForReviewV2323();

    if (!questions.length) {
      showSmallNotice("Prüfungsbogen A konnte nicht geladen werden.");
      return;
    }

    const blocks = [
      {
        examinerIndex: 0,
        examinerName: "Prüfer 1",
        range: "Frage 1–5",
        title: "Öffentliches Recht / Gewerberecht"
      },
      {
        examinerIndex: 1,
        examinerName: "Vorsitz",
        range: "Frage 6–10",
        title: "Umgang mit Menschen"
      },
      {
        examinerIndex: 2,
        examinerName: "Prüfer 3",
        range: "Frage 11–15",
        title: "Mischblock – weitere Sachgebiete"
      }
    ];

    const blockHtml = blocks.map(block => {
      const blockQuestions = questions.filter((question, index) => {
        const examinerIndex = Number.isInteger(question.examinerIndex)
          ? question.examinerIndex
          : index < 5 ? 0 : index < 10 ? 1 : 2;

        return examinerIndex === block.examinerIndex;
      });

      return `
        <section class="oral-review-block-v2323">
          <div class="oral-review-block-head-v2323">
            <div>
              <span>${escapeHtml(block.examinerName)}</span>
              <h2>${escapeHtml(block.title)}</h2>
            </div>

            <strong>${escapeHtml(block.range)}</strong>
          </div>

          <div class="oral-review-question-list-v2323">
            ${blockQuestions.map((question, questionIndex) => {
              const absoluteNumber = block.examinerIndex * 5 + questionIndex + 1;

              return `
                <article class="oral-review-question-v2323">
                  <div class="oral-review-question-top-v2323">
                    <span>Frage ${absoluteNumber}</span>
                    <strong>${escapeHtml(question.category || "Sachgebiet")}</strong>
                  </div>

                  <h3>${escapeHtml(question.question || "")}</h3>

                  <div class="oral-review-answer-v2323">
                    <span>Musterantwort</span>
                    <p>${escapeHtml(question.sampleAnswer || "Keine Musterantwort hinterlegt.")}</p>
                  </div>

                  <div class="oral-review-note-v2323">
                    <span>Prüfer-Hinweis</span>
                    <p>${escapeHtml(question.examinerNote || "Kein Prüfer-Hinweis hinterlegt.")}</p>
                  </div>
                </article>
              `;
            }).join("")}
          </div>
        </section>
      `;
    }).join("");

    mainContent.innerHTML = `
      <button class="back-btn" onclick="renderOralExamBlockFinishV2322 ? renderOralExamBlockFinishV2322() : showOralExamPage()">
        ← Zurück zur Auswertung
      </button>

      <section class="result-wrapper oral-review-wrapper-v2323">

        <div class="oral-review-hero-v2323">
          <p class="eyebrow">Nacharbeit</p>
          <h1>Prüfungsbogen A nacharbeiten</h1>
          <p>
            Wiederholen Sie die Fragen mit Musterantwort und Prüfer-Hinweis.
            Ziel ist nicht Auswendiglernen, sondern eine ruhige, vollständige und rechtlich saubere Antwort.
          </p>
        </div>

        ${blockHtml}

        <div class="result-actions oral-review-actions-v2323">
          <button class="next-btn" onclick="startOralSimulation15V2314()">
            Prüfungsbogen A wiederholen
          </button>

          <button class="next-btn" onclick="showOralExamPage()">
            Zur Modusauswahl
          </button>

          <button class="next-btn secondary-btn" onclick="location.reload()">
            Zurück zum Dashboard
          </button>
        </div>

      </section>
    `;
  }

  function injectOralReviewButtonV2323() {
    const actions = document.querySelector(".oral-block-actions-v2321");

    if (!actions || document.getElementById("oralReviewButtonV2323")) {
      return;
    }

    const button = document.createElement("button");
    button.id = "oralReviewButtonV2323";
    button.className = "next-btn oral-review-result-btn-v2323";
    button.type = "button";
    button.textContent = "Prüfungsbogen A nacharbeiten";
    button.onclick = showOralSheetAReviewV2323;

    const firstButton = actions.querySelector("button");

    if (firstButton && firstButton.nextSibling) {
      actions.insertBefore(button, firstButton.nextSibling);
    } else {
      actions.appendChild(button);
    }
  }

  function scheduleOralReviewButtonV2323() {
    setTimeout(injectOralReviewButtonV2323, 60);
    setTimeout(injectOralReviewButtonV2323, 220);
    setTimeout(injectOralReviewButtonV2323, 520);
  }

  window.accaouiPreviousShowOralExamFinishScreenV2323 =
    window.accaouiPreviousShowOralExamFinishScreenV2323 ||
    window.showOralExamFinishScreenV220;

  window.showOralExamFinishScreenV220 = function patchedShowOralExamFinishScreenV2323() {
    if (typeof window.accaouiPreviousShowOralExamFinishScreenV2323 === "function") {
      const result = window.accaouiPreviousShowOralExamFinishScreenV2323();
      scheduleOralReviewButtonV2323();
      return result;
    }
  };

  try {
    showOralExamFinishScreenV220 = window.showOralExamFinishScreenV220;
  } catch (error) {
    /* Rebinding ist je nach Browser nicht notwendig */
  }

  function compactCategoryStatsV2323() {
    const cards = document.querySelectorAll(".category-card");

    cards.forEach(card => {
      if (card.querySelector(".category-inline-stats-v2323")) return;

      const title = card.querySelector("h3");
      const statElements = Array.from(card.children).filter(child => {
        return child.tagName === "SPAN" || child.tagName === "SMALL";
      });

      if (!title || statElements.length < 2) return;

      const statRow = document.createElement("div");
      statRow.className = "category-inline-stats-v2323";

      statElements.forEach(element => {
        const text = String(element.textContent || "").trim();

        if (!text) return;

        const item = document.createElement("span");
        item.textContent = text;

        if (text.toLowerCase().includes("fehler") && !text.startsWith("0")) {
          item.classList.add("has-warning-v2323");
        }

        statRow.appendChild(item);
        element.classList.add("category-old-stat-v2323");
      });

      title.insertAdjacentElement("afterend", statRow);
    });
  }

  function scheduleCompactCategoryStatsV2323() {
    setTimeout(compactCategoryStatsV2323, 60);
    setTimeout(compactCategoryStatsV2323, 220);
    setTimeout(compactCategoryStatsV2323, 520);
  }

  window.accaouiPreviousShowAllQuestionsV2323 =
    window.accaouiPreviousShowAllQuestionsV2323 ||
    window.showAllQuestions;

  window.showAllQuestions = function patchedShowAllQuestionsV2323() {
    if (typeof window.accaouiPreviousShowAllQuestionsV2323 === "function") {
      const result = window.accaouiPreviousShowAllQuestionsV2323();
      scheduleCompactCategoryStatsV2323();
      return result;
    }
  };

  try {
    showAllQuestions = window.showAllQuestions;
  } catch (error) {
    /* Rebinding ist je nach Browser nicht notwendig */
  }

  window.showOralSheetAReviewV2323 = showOralSheetAReviewV2323;
  window.compactCategoryStatsV2323 = compactCategoryStatsV2323;
}

/* =====================================================
   v23.2.4 MÜNDLICHE PRÜFUNGSFEHLER TRAINIEREN
   Ziel:
   - "Nacharbeiten" durch echten mündlichen Fehlertrainer ersetzen
   - nur Fragen mit "Noch üben" speichern
   - bei "Sicher beantwortet" wieder entfernen
   - mündliche Fehler im normalen Fehlertraining anzeigen
===================================================== */

if (!window.ACCAOUI_V2324_ORAL_MISTAKE_TRAINER_PATCH) {
  window.ACCAOUI_V2324_ORAL_MISTAKE_TRAINER_PATCH = true;

  const ORAL_MISTAKE_STORAGE_KEY_V2324 = "accaoui_oral_exam_mistakes_v2324";

  function readOralMistakesV2324() {
    try {
      const raw = localStorage.getItem(ORAL_MISTAKE_STORAGE_KEY_V2324);
      const parsed = JSON.parse(raw || "[]");
      return Array.isArray(parsed) ? parsed : [];
    } catch (error) {
      return [];
    }
  }

  function writeOralMistakesV2324(list) {
    localStorage.setItem(
      ORAL_MISTAKE_STORAGE_KEY_V2324,
      JSON.stringify(Array.isArray(list) ? list : [])
    );
  }

  function getOralMistakeKeyV2324(question) {
    if (!question) return "";

    return String(
      question.id ||
      question.question ||
      ""
    ).trim();
  }

  function getCurrentOralQuestionV2324() {
    try {
      if (
        typeof oralExamQuestionsV220 !== "undefined" &&
        Array.isArray(oralExamQuestionsV220) &&
        typeof oralExamIndexV220 !== "undefined"
      ) {
        return oralExamQuestionsV220[oralExamIndexV220];
      }
    } catch (error) {
      return null;
    }

    return null;
  }

  function saveOralMistakeV2324(question) {
    if (!question) return;

    const key = getOralMistakeKeyV2324(question);

    if (!key) return;

    const mistakes = readOralMistakesV2324();

    const exists = mistakes.some(item => item && item.key === key);

    const entry = {
      key,
      id: question.id || key,
      category: question.category || "Mündliche Prüfung",
      question: question.question || "",
      sampleAnswer: question.sampleAnswer || "",
      examinerNote: question.examinerNote || "",
      examinerName: question.examinerName || "",
      examinerBlockTitle: question.examinerBlockTitle || "",
      sheetId: question.sheetId || "",
      sheetTitle: question.sheetTitle || "Prüfungsbogen A",
      savedAt: new Date().toISOString()
    };

    if (exists) {
      const updated = mistakes.map(item => item.key === key ? entry : item);
      writeOralMistakesV2324(updated);
      return;
    }

    mistakes.push(entry);
    writeOralMistakesV2324(mistakes);
  }

  function removeOralMistakeV2324(questionOrKey) {
    const key = typeof questionOrKey === "string"
      ? questionOrKey
      : getOralMistakeKeyV2324(questionOrKey);

    if (!key) return;

    const mistakes = readOralMistakesV2324().filter(item => item && item.key !== key);
    writeOralMistakesV2324(mistakes);
  }

  function getOralMistakeCountV2324() {
    return readOralMistakesV2324().length;
  }

  function markOralMistakeResolvedV2324(key) {
    removeOralMistakeV2324(key);
    showOralMistakeTrainingV2324();
  }

  function showOralMistakeTrainingV2324() {
    const mainContent = document.querySelector(".main-content");

    if (!mainContent) return;

    const mistakes = readOralMistakesV2324();

    if (!mistakes.length) {
      showSmallNotice("Keine mündlichen Prüfungsfehler gespeichert.");
      return;
    }

    const cards = mistakes.map((item, index) => {
      return `
        <article class="oral-mistake-card-v2324">
          <div class="oral-mistake-top-v2324">
            <span>Frage ${index + 1}</span>
            <strong>${escapeHtml(item.examinerName || item.category || "Mündliche Prüfung")}</strong>
          </div>

          <p class="oral-mistake-category-v2324">
            ${escapeHtml(item.examinerBlockTitle || item.category || "Prüfungsbogen A")}
          </p>

          <h3>${escapeHtml(item.question || "")}</h3>

          <div class="oral-mistake-answer-v2324">
            <span>Musterantwort</span>
            <p>${escapeHtml(item.sampleAnswer || "Keine Musterantwort hinterlegt.")}</p>
          </div>

          <div class="oral-mistake-note-v2324">
            <span>Prüfer-Hinweis</span>
            <p>${escapeHtml(item.examinerNote || "Kein Prüfer-Hinweis hinterlegt.")}</p>
          </div>

          <button class="next-btn oral-mistake-resolve-btn-v2324" onclick='markOralMistakeResolvedV2324(${JSON.stringify(item.key)})'>
            Als sicher markieren
          </button>
        </article>
      `;
    }).join("");

    mainContent.innerHTML = `
      <button class="back-btn" onclick="showMistakeOverview()">
        ← Zurück zum Fehlertraining
      </button>

      <section class="result-wrapper oral-mistake-wrapper-v2324">

        <div class="oral-mistake-hero-v2324">
          <p class="eyebrow">Mündliche Prüfung</p>

          <h1>Mündliche Fehler trainieren</h1>

          <p>
            Hier erscheinen nur Fragen, die in der mündlichen Simulation mit
            „Noch üben“ bewertet wurden.
          </p>

          <div class="oral-mistake-count-v2324">
            <strong>${mistakes.length}</strong>
            <span>offene mündliche Fehler</span>
          </div>
        </div>

        <div class="oral-mistake-list-v2324">
          ${cards}
        </div>

        <div class="result-actions oral-mistake-actions-v2324">
          <button class="next-btn" onclick="startOralSimulation15V2314()">
            Prüfungsbogen A wiederholen
          </button>

          <button class="next-btn" onclick="showMistakeOverview()">
            Zur Fehlerübersicht
          </button>

          <button class="next-btn secondary-btn" onclick="location.reload()">
            Zurück zum Dashboard
          </button>
        </div>

      </section>
    `;
  }

  window.accaouiPreviousRateOralExamQuestionV2324 =
    window.accaouiPreviousRateOralExamQuestionV2324 ||
    window.rateOralExamQuestionV220;

  window.rateOralExamQuestionV220 = function patchedRateOralExamQuestionV2324(status) {
    const currentQuestion = getCurrentOralQuestionV2324();

    if (status === "practice") {
      saveOralMistakeV2324(currentQuestion);
    }

    if (status === "known") {
      removeOralMistakeV2324(currentQuestion);
    }

    if (typeof window.accaouiPreviousRateOralExamQuestionV2324 === "function") {
      return window.accaouiPreviousRateOralExamQuestionV2324(status);
    }

    showSmallNotice("Mündliche Bewertung konnte nicht gespeichert werden.");
  };

  try {
    rateOralExamQuestionV220 = window.rateOralExamQuestionV220;
  } catch (error) {
    /* Rebinding je nach Browser nicht notwendig */
  }

  function replaceOralReviewButtonV2324() {
    const button = document.getElementById("oralReviewButtonV2323");

    if (!button) return;

    button.textContent = "Mündliche Fehler trainieren";
    button.onclick = showOralMistakeTrainingV2324;
    button.classList.add("oral-mistake-result-btn-v2324");

    const count = getOralMistakeCountV2324();

    if (count > 0) {
      button.textContent = `Mündliche Fehler trainieren (${count})`;
    }
  }

  function injectOralMistakeBoxIntoOverviewV2324() {
    const wrapper = document.querySelector(".result-wrapper");
    const topicSection = document.querySelector(".topic-stats-section");

    if (!wrapper || document.getElementById("oralMistakeOverviewBoxV2324")) return;

    const count = getOralMistakeCountV2324();

    if (count <= 0) return;

    const box = document.createElement("div");
    box.id = "oralMistakeOverviewBoxV2324";
    box.className = "oral-mistake-overview-box-v2324";

    box.innerHTML = `
      <span>Mündliche Prüfung</span>
      <strong>${count} mündliche Prüfungsfehler</strong>
      <p>
        Diese Fragen wurden in der 15-Minuten-Simulation mit „Noch üben“
        bewertet.
      </p>

      <button class="next-btn oral-mistake-result-btn-v2324" onclick="showOralMistakeTrainingV2324()">
        Mündliche Fehler trainieren
      </button>
    `;

    if (topicSection) {
      topicSection.insertAdjacentElement("beforebegin", box);
    } else {
      wrapper.appendChild(box);
    }
  }

  function scheduleOralMistakeUiV2324() {
    setTimeout(replaceOralReviewButtonV2324, 60);
    setTimeout(replaceOralReviewButtonV2324, 220);
    setTimeout(replaceOralReviewButtonV2324, 520);

    setTimeout(injectOralMistakeBoxIntoOverviewV2324, 60);
    setTimeout(injectOralMistakeBoxIntoOverviewV2324, 220);
    setTimeout(injectOralMistakeBoxIntoOverviewV2324, 520);
  }

  window.accaouiPreviousShowOralExamFinishScreenV2324 =
    window.accaouiPreviousShowOralExamFinishScreenV2324 ||
    window.showOralExamFinishScreenV220;

  window.showOralExamFinishScreenV220 = function patchedShowOralExamFinishScreenV2324() {
    if (typeof window.accaouiPreviousShowOralExamFinishScreenV2324 === "function") {
      const result = window.accaouiPreviousShowOralExamFinishScreenV2324();
      scheduleOralMistakeUiV2324();
      return result;
    }
  };

  window.accaouiPreviousShowMistakeOverviewV2324 =
    window.accaouiPreviousShowMistakeOverviewV2324 ||
    window.showMistakeOverview;

  window.showMistakeOverview = function patchedShowMistakeOverviewV2324() {
    if (typeof window.accaouiPreviousShowMistakeOverviewV2324 === "function") {
      const result = window.accaouiPreviousShowMistakeOverviewV2324();
      scheduleOralMistakeUiV2324();
      return result;
    }
  };

  try {
    showOralExamFinishScreenV220 = window.showOralExamFinishScreenV220;
    showMistakeOverview = window.showMistakeOverview;
  } catch (error) {
    /* Rebinding je nach Browser nicht notwendig */
  }

  window.showOralMistakeTrainingV2324 = showOralMistakeTrainingV2324;
  window.markOralMistakeResolvedV2324 = markOralMistakeResolvedV2324;
  window.getOralMistakeCountV2324 = getOralMistakeCountV2324;
}

/* =====================================================
   v23.2.5 MÜNDLICHE FEHLERTRAINER – ANTWORT AUFDECKEN
   Ziel:
   - Frage zuerst ohne Musterantwort anzeigen
   - Musterantwort + Prüfer-Hinweis erst nach Klick anzeigen
   - "Als sicher markieren" erst nach Antwortanzeige
===================================================== */

if (!window.ACCAOUI_V2325_ORAL_MISTAKE_REVEAL_PATCH) {
  window.ACCAOUI_V2325_ORAL_MISTAKE_REVEAL_PATCH = true;

  const ORAL_MISTAKE_STORAGE_KEY_V2325 = "accaoui_oral_exam_mistakes_v2324";

  function readOralMistakesV2325() {
    try {
      const raw = localStorage.getItem(ORAL_MISTAKE_STORAGE_KEY_V2325);
      const parsed = JSON.parse(raw || "[]");
      return Array.isArray(parsed) ? parsed : [];
    } catch (error) {
      return [];
    }
  }

  function writeOralMistakesV2325(list) {
    localStorage.setItem(
      ORAL_MISTAKE_STORAGE_KEY_V2325,
      JSON.stringify(Array.isArray(list) ? list : [])
    );
  }

  function removeOralMistakeV2325(key) {
    const mistakes = readOralMistakesV2325().filter(item => {
      return item && item.key !== key;
    });

    writeOralMistakesV2325(mistakes);
  }

  function revealOralMistakeAnswerV2325(index) {
    const card = document.querySelector(`[data-oral-mistake-index-v2325="${index}"]`);

    if (!card) return;

    card.classList.add("is-answer-visible-v2325");

    const revealButton = card.querySelector(".oral-mistake-reveal-btn-v2325");
    const resolveButton = card.querySelector(".oral-mistake-resolve-btn-v2325");

    if (revealButton) {
      revealButton.textContent = "Antwort angezeigt";
      revealButton.disabled = true;
    }

    if (resolveButton) {
      resolveButton.style.display = "inline-flex";
    }
  }

  function markOralMistakeResolvedV2325(key) {
    removeOralMistakeV2325(key);

    if (typeof showSmallNotice === "function") {
      showSmallNotice("Mündlicher Fehler wurde als sicher markiert.");
    }

    showOralMistakeTrainingV2325();
  }

  function showOralMistakeTrainingV2325() {
    const mainContent = document.querySelector(".main-content");

    if (!mainContent) return;

    const mistakes = readOralMistakesV2325();

    if (!mistakes.length) {
      showSmallNotice("Keine mündlichen Prüfungsfehler gespeichert.");
      return;
    }

    const cards = mistakes.map((item, index) => {
      return `
        <article class="oral-mistake-card-v2324 oral-mistake-card-v2325" data-oral-mistake-index-v2325="${index}">
          <div class="oral-mistake-top-v2324">
            <span>Frage ${index + 1}</span>
            <strong>${escapeHtml(item.examinerName || item.category || "Mündliche Prüfung")}</strong>
          </div>

          <p class="oral-mistake-category-v2324">
            ${escapeHtml(item.examinerBlockTitle || item.category || "Prüfungsbogen A")}
          </p>

          <h3>${escapeHtml(item.question || "")}</h3>

          <div class="oral-mistake-training-hint-v2325">
            <span>Übungsauftrag</span>
            <p>
              Antworten Sie zuerst laut und vollständig. Danach Musterantwort anzeigen und vergleichen.
            </p>
          </div>

          <div class="oral-mistake-hidden-content-v2325">
            <div class="oral-mistake-answer-v2324">
              <span>Musterantwort</span>
              <p>${escapeHtml(item.sampleAnswer || "Keine Musterantwort hinterlegt.")}</p>
            </div>

            <div class="oral-mistake-note-v2324">
              <span>Prüfer-Hinweis</span>
              <p>${escapeHtml(item.examinerNote || "Kein Prüfer-Hinweis hinterlegt.")}</p>
            </div>
          </div>

          <div class="oral-mistake-card-actions-v2325">
            <button class="next-btn oral-mistake-reveal-btn-v2325" onclick="revealOralMistakeAnswerV2325(${index})">
              Musterantwort anzeigen
            </button>

            <button class="next-btn oral-mistake-resolve-btn-v2324 oral-mistake-resolve-btn-v2325" style="display:none;" onclick='markOralMistakeResolvedV2325(${JSON.stringify(item.key)})'>
              Als sicher markieren
            </button>
          </div>
        </article>
      `;
    }).join("");

    mainContent.innerHTML = `
      <button class="back-btn" onclick="showMistakeOverview()">
        ← Zurück zum Fehlertraining
      </button>

      <section class="result-wrapper oral-mistake-wrapper-v2324 oral-mistake-wrapper-v2325">

        <div class="oral-mistake-hero-v2324">
          <p class="eyebrow">Mündliche Prüfung</p>

          <h1>Mündliche Fehler trainieren</h1>

          <p>
            Hier erscheinen nur Fragen, die in der mündlichen Simulation mit
            „Noch üben“ bewertet wurden. Die Musterantwort bleibt zuerst verdeckt.
          </p>

          <div class="oral-mistake-count-v2324">
            <strong>${mistakes.length}</strong>
            <span>offene mündliche Fehler</span>
          </div>
        </div>

        <div class="oral-mistake-list-v2324">
          ${cards}
        </div>

        <div class="result-actions oral-mistake-actions-v2324">
          <button class="next-btn" onclick="startOralSimulation15V2314()">
            Prüfungsbogen A wiederholen
          </button>

          <button class="next-btn" onclick="showMistakeOverview()">
            Zur Fehlerübersicht
          </button>

          <button class="next-btn secondary-btn" onclick="location.reload()">
            Zurück zum Dashboard
          </button>
        </div>

      </section>
    `;
  }

  window.showOralMistakeTrainingV2324 = showOralMistakeTrainingV2325;
  window.showOralMistakeTrainingV2325 = showOralMistakeTrainingV2325;
  window.revealOralMistakeAnswerV2325 = revealOralMistakeAnswerV2325;
  window.markOralMistakeResolvedV2325 = markOralMistakeResolvedV2325;

  try {
    showOralMistakeTrainingV2324 = window.showOralMistakeTrainingV2324;
  } catch (error) {
    /* Rebinding je nach Browser nicht notwendig */
  }
}

/* =====================================================
   v23.2.6 MÜNDLICHE FEHLERTRAINER – AUFDECKUNG ERZWINGEN
   Ziel:
   - alte v23.2.4 Ansicht sicher überschreiben
   - Musterantwort zuerst verstecken
   - Button "Musterantwort anzeigen" erzwingen
===================================================== */

if (!window.ACCAOUI_V2326_ORAL_MISTAKE_FORCE_REVEAL_PATCH) {
  window.ACCAOUI_V2326_ORAL_MISTAKE_FORCE_REVEAL_PATCH = true;

  const ORAL_MISTAKE_STORAGE_KEY_V2326 = "accaoui_oral_exam_mistakes_v2324";

  function readOralMistakesV2326() {
    try {
      const raw = localStorage.getItem(ORAL_MISTAKE_STORAGE_KEY_V2326);
      const parsed = JSON.parse(raw || "[]");
      return Array.isArray(parsed) ? parsed : [];
    } catch (error) {
      return [];
    }
  }

  function writeOralMistakesV2326(list) {
    localStorage.setItem(
      ORAL_MISTAKE_STORAGE_KEY_V2326,
      JSON.stringify(Array.isArray(list) ? list : [])
    );
  }

  function removeOralMistakeV2326(key) {
    const mistakes = readOralMistakesV2326().filter(item => {
      return item && item.key !== key;
    });

    writeOralMistakesV2326(mistakes);
  }

  function revealOralMistakeAnswerV2326(index) {
    const card = document.querySelector(`[data-oral-mistake-index-v2326="${index}"]`);

    if (!card) return;

    card.classList.add("is-answer-visible-v2326");

    const revealButton = card.querySelector(".oral-mistake-reveal-btn-v2326");
    const resolveButton = card.querySelector(".oral-mistake-resolve-btn-v2326");

    if (revealButton) {
      revealButton.textContent = "Antwort angezeigt";
      revealButton.disabled = true;
    }

    if (resolveButton) {
      resolveButton.style.display = "inline-flex";
    }
  }

  function markOralMistakeResolvedV2326(key) {
    removeOralMistakeV2326(key);

    if (typeof showSmallNotice === "function") {
      showSmallNotice("Mündlicher Fehler wurde als sicher markiert.");
    }

    showOralMistakeTrainingV2326();
  }

  function showOralMistakeTrainingV2326() {
    const mainContent = document.querySelector(".main-content");

    if (!mainContent) return;

    const mistakes = readOralMistakesV2326();

    if (!mistakes.length) {
      showSmallNotice("Keine mündlichen Prüfungsfehler gespeichert.");
      return;
    }

    const cards = mistakes.map((item, index) => {
      return `
        <article class="oral-mistake-card-v2324 oral-mistake-card-v2326" data-oral-mistake-index-v2326="${index}">
          <div class="oral-mistake-top-v2324">
            <span>Frage ${index + 1}</span>
            <strong>${escapeHtml(item.examinerName || item.category || "Mündliche Prüfung")}</strong>
          </div>

          <p class="oral-mistake-category-v2324">
            ${escapeHtml(item.examinerBlockTitle || item.category || "Prüfungsbogen A")}
          </p>

          <h3>${escapeHtml(item.question || "")}</h3>

          <div class="oral-mistake-training-hint-v2326">
            <span>Übungsauftrag</span>
            <p>
              Antworten Sie zuerst laut und vollständig. Danach klicken Sie auf
              „Musterantwort anzeigen“ und vergleichen Ihre Antwort.
            </p>
          </div>

          <div class="oral-mistake-hidden-content-v2326">
            <div class="oral-mistake-answer-v2324">
              <span>Musterantwort</span>
              <p>${escapeHtml(item.sampleAnswer || "Keine Musterantwort hinterlegt.")}</p>
            </div>

            <div class="oral-mistake-note-v2324">
              <span>Prüfer-Hinweis</span>
              <p>${escapeHtml(item.examinerNote || "Kein Prüfer-Hinweis hinterlegt.")}</p>
            </div>
          </div>

          <div class="oral-mistake-card-actions-v2326">
            <button class="next-btn oral-mistake-reveal-btn-v2326" onclick="revealOralMistakeAnswerV2326(${index})">
              Musterantwort anzeigen
            </button>

            <button class="next-btn oral-mistake-resolve-btn-v2324 oral-mistake-resolve-btn-v2326" style="display:none;" onclick='markOralMistakeResolvedV2326(${JSON.stringify(item.key)})'>
              Als sicher markieren
            </button>
          </div>
        </article>
      `;
    }).join("");

    mainContent.innerHTML = `
      <button class="back-btn" onclick="showMistakeOverview()">
        ← Zurück zum Fehlertraining
      </button>

      <section class="result-wrapper oral-mistake-wrapper-v2324 oral-mistake-wrapper-v2326">

        <div class="oral-mistake-hero-v2324">
          <p class="eyebrow">Mündliche Prüfung</p>

          <h1>Mündliche Fehler trainieren</h1>

          <p>
            Hier erscheinen nur Fragen, die in der mündlichen Simulation mit
            „Noch üben“ bewertet wurden. Die Musterantwort bleibt zuerst verdeckt.
          </p>

          <div class="oral-mistake-count-v2324">
            <strong>${mistakes.length}</strong>
            <span>offene mündliche Fehler</span>
          </div>
        </div>

        <div class="oral-mistake-list-v2324">
          ${cards}
        </div>

        <div class="result-actions oral-mistake-actions-v2324">
          <button class="next-btn" onclick="startOralSimulation15V2314()">
            Prüfungsbogen A wiederholen
          </button>

          <button class="next-btn" onclick="showMistakeOverview()">
            Zur Fehlerübersicht
          </button>

          <button class="next-btn secondary-btn" onclick="location.reload()">
            Zurück zum Dashboard
          </button>
        </div>

      </section>
    `;
  }

  window.showOralMistakeTrainingV2324 = showOralMistakeTrainingV2326;
  window.showOralMistakeTrainingV2325 = showOralMistakeTrainingV2326;
  window.showOralMistakeTrainingV2326 = showOralMistakeTrainingV2326;

  window.revealOralMistakeAnswerV2326 = revealOralMistakeAnswerV2326;
  window.markOralMistakeResolvedV2326 = markOralMistakeResolvedV2326;

  try {
    showOralMistakeTrainingV2324 = window.showOralMistakeTrainingV2326;
    showOralMistakeTrainingV2325 = window.showOralMistakeTrainingV2326;
  } catch (error) {
    /* Rebinding je nach Browser nicht notwendig */
  }
}

/* =====================================================
   v23.3.3 MÜNDLICHE PRÜFUNG – ANTWORT IN SIMULATION VERDECKEN
   Ziel:
   - in der 15-Minuten-Simulation ist die Musterantwort zuerst verdeckt
   - Antwort erscheint erst nach Klick auf „Musterantwort anzeigen“
===================================================== */

if (!window.ACCAOUI_V2333_FORCE_ORAL_SESSION_ANSWER_HIDDEN) {
  window.ACCAOUI_V2333_FORCE_ORAL_SESSION_ANSWER_HIDDEN = true;

  function forceOralSessionAnswerHiddenV2333() {
    const answerBox = document.getElementById("oralAnswerBoxV220");
    const revealActions = document.getElementById("oralRevealActionsV220");
    const ratingActions = document.getElementById("oralRatingActionsV220");

    if (answerBox && !answerBox.classList.contains("is-manually-revealed-v2333")) {
      answerBox.style.display = "none";
    }

    if (revealActions && !answerBox?.classList.contains("is-manually-revealed-v2333")) {
      revealActions.style.display = "flex";
    }

    if (ratingActions && !answerBox?.classList.contains("is-manually-revealed-v2333")) {
      ratingActions.style.display = "none";
    }
  }

  window.accaouiPreviousRenderOralExamQuestionV2333 =
    window.accaouiPreviousRenderOralExamQuestionV2333 ||
    window.renderOralExamQuestionV220;

  window.renderOralExamQuestionV220 = function patchedRenderOralExamQuestionV2333() {
    if (typeof window.accaouiPreviousRenderOralExamQuestionV2333 === "function") {
      const result = window.accaouiPreviousRenderOralExamQuestionV2333();

      setTimeout(forceOralSessionAnswerHiddenV2333, 20);
      setTimeout(forceOralSessionAnswerHiddenV2333, 120);

      return result;
    }
  };

  window.accaouiPreviousShowOralExamAnswerV2333 =
    window.accaouiPreviousShowOralExamAnswerV2333 ||
    window.showOralExamAnswerV220;

  window.showOralExamAnswerV220 = function patchedShowOralExamAnswerV2333() {
    const answerBox = document.getElementById("oralAnswerBoxV220");

    if (answerBox) {
      answerBox.classList.add("is-manually-revealed-v2333");
    }

    if (typeof window.accaouiPreviousShowOralExamAnswerV2333 === "function") {
      return window.accaouiPreviousShowOralExamAnswerV2333();
    }
  };

  try {
    renderOralExamQuestionV220 = window.renderOralExamQuestionV220;
    showOralExamAnswerV220 = window.showOralExamAnswerV220;
  } catch (error) {
    /* Rebinding je nach Browser nicht notwendig */
  }
}

/* =====================================================
   v23.2 MÜNDLICHE PRÜFUNG – PRÜFUNGSBOGEN B
   Ziel:
   - Prüfungsbogen B aus oral-sheets-v23.js in 15-Min-Simulation
   - Prüfungsbogen A bleibt unverändert
===================================================== */

if (!window.ACCAOUI_V232_ORAL_SHEET_B_PATCH) {
  window.ACCAOUI_V232_ORAL_SHEET_B_PATCH = true;

  const ORAL_SHEET_B_ID_V232 = "oral_sheet_b_v23";
  let oralSheetBRatingsV232 = [];

  function getOralSheetBBlockTitleV232(examinerBlock) {
    const block = Number(examinerBlock);

    if (block === 1) {
      return "Öffentliches Recht / Gewerberecht";
    }

    if (block === 2) {
      return "Umgang mit Menschen";
    }

    if (block === 3) {
      return "Mischblock";
    }

    return "Prüferblock";
  }

  function mapOralSheetBQuestionV232(question) {
    if (!question) {
      return null;
    }

    return {
      id: question.id,
      question: question.examinerQuestion,
      answer: question.modelAnswer,
      examinerNote: question.examinerNotes,
      category: question.topic,
      examinerIndex: Number(question.examinerBlock) - 1,
      examinerName: question.examinerRole,
      examinerBlockTitle: getOralSheetBBlockTitleV232(question.examinerBlock),
      sheetId: ORAL_SHEET_B_ID_V232,
      sheetTitle: "Prüfungsbogen B"
    };
  }

  function getOralExamSheetBQuestionsV232() {
    const sheetsData = window.ACCAOUI_ORAL_SHEETS_V23;

    if (!sheetsData || !Array.isArray(sheetsData.sheets)) {
      return [];
    }

    const sheet = sheetsData.sheets.find(item => item && item.id === ORAL_SHEET_B_ID_V232);

    if (!sheet || !Array.isArray(sheet.questions)) {
      return [];
    }

    return sheet.questions
      .map(mapOralSheetBQuestionV232)
      .filter(Boolean);
  }

  function isOralSheetBSessionV232() {
    try {
      return (
        window.ACCAOUI_V2317_ORAL_SIMULATION_MODE === "15" &&
        Array.isArray(oralExamQuestionsV220) &&
        oralExamQuestionsV220.some(question => question && question.sheetId === ORAL_SHEET_B_ID_V232)
      );
    } catch (error) {
      return false;
    }
  }

  function isOralSheet15BlockSessionV232() {
    try {
      if (window.ACCAOUI_V2317_ORAL_SIMULATION_MODE !== "15") {
        return false;
      }

      if (!Array.isArray(oralExamQuestionsV220)) {
        return false;
      }

      return oralExamQuestionsV220.some(question => {
        if (!question || !question.sheetId) {
          return false;
        }

        return (
          question.sheetId === "oral_sheet_a_v2320" ||
          question.sheetId === "oral_sheet_a_v2340" ||
          question.sheetId === ORAL_SHEET_B_ID_V232
        );
      });
    } catch (error) {
      return false;
    }
  }

  function getOralSheetBQuestionIndexV232() {
    try {
      return Number(oralExamIndexV220 || 0);
    } catch (error) {
      return 0;
    }
  }

  function getOralSheetBCurrentQuestionV232() {
    try {
      if (Array.isArray(oralExamQuestionsV220)) {
        return oralExamQuestionsV220[getOralSheetBQuestionIndexV232()];
      }
    } catch (error) {
      return null;
    }

    return null;
  }

  function getOralSheetBExaminerIndexV232(question, fallbackIndex) {
    if (question && Number.isInteger(question.examinerIndex)) {
      return question.examinerIndex;
    }

    if (fallbackIndex < 5) return 0;
    if (fallbackIndex < 10) return 1;
    return 2;
  }

  function resetOralSheetBRatingsV232() {
    oralSheetBRatingsV232 = [];
  }

  function saveOralSheetBRatingV232(status) {
    if (!isOralSheetBSessionV232()) {
      return;
    }

    const questionIndex = getOralSheetBQuestionIndexV232();
    const question = getOralSheetBCurrentQuestionV232();

    oralSheetBRatingsV232[questionIndex] = {
      index: questionIndex,
      status: status === "known" ? "known" : "practice",
      questionId: question && question.id ? question.id : "oral_question_" + questionIndex,
      category: question && question.category ? question.category : "Ohne Kategorie",
      examinerIndex: getOralSheetBExaminerIndexV232(question, questionIndex),
      examinerName: question && question.examinerName ? question.examinerName : "",
      blockTitle: question && question.examinerBlockTitle ? question.examinerBlockTitle : ""
    };
  }

  function getOralSheetBBlockResultStatsV232() {
    const questions = Array.isArray(oralExamQuestionsV220)
      ? oralExamQuestionsV220
      : [];

    const blocks = [
      {
        examinerIndex: 0,
        examinerName: "Prüfer 1",
        title: "Öffentliches Recht / Gewerberecht",
        range: "Frage 1–5"
      },
      {
        examinerIndex: 1,
        examinerName: "Vorsitz",
        title: "Umgang mit Menschen",
        range: "Frage 6–10"
      },
      {
        examinerIndex: 2,
        examinerName: "Prüfer 3",
        title: "Mischblock",
        range: "Frage 11–15"
      }
    ];

    return blocks.map(block => {
      const blockQuestions = questions.filter((question, index) => {
        return getOralSheetBExaminerIndexV232(question, index) === block.examinerIndex;
      });

      const blockRatings = oralSheetBRatingsV232.filter(rating => {
        return rating && rating.examinerIndex === block.examinerIndex;
      });

      const known = blockRatings.filter(rating => rating.status === "known").length;
      const practice = blockRatings.filter(rating => rating.status === "practice").length;
      const answered = known + practice;
      const total = blockQuestions.length || 5;
      const open = Math.max(0, total - answered);
      const percent = answered > 0 ? Math.round((known / answered) * 100) : 0;

      return {
        ...block,
        total,
        answered,
        known,
        practice,
        open,
        percent
      };
    });
  }

  function applyOralSheetBResultTextsV232() {
    if (!isOralSheetBSessionV232()) {
      return;
    }

    const root = document.querySelector(".main-content");

    if (!root) {
      return;
    }

    const replacements = [
      ["Prüfungsbogen A abgeschlossen", "Prüfungsbogen B abgeschlossen"],
      ["Prüfungsbogen A wurde abgeschlossen", "Prüfungsbogen B wurde abgeschlossen"],
      ["Prüfungsbogen A wiederholen", "Prüfungsbogen B wiederholen"]
    ];

    root.querySelectorAll("h1, h2, h3, p, span, strong, button").forEach(element => {
      replacements.forEach(([from, to]) => {
        const text = (element.textContent || "").replace(/\s+/g, " ").trim();

        if (text === from) {
          element.textContent = to;
        }
      });
    });

    root.querySelectorAll("button").forEach(button => {
      const label = (button.textContent || "").replace(/\s+/g, " ").trim();

      if (label === "Prüfungsbogen B wiederholen" || label === "Prüfungsbogen A wiederholen") {
        button.textContent = "Prüfungsbogen B wiederholen";
        button.setAttribute("onclick", "startOralSimulationSheetBV232()");
      }
    });
  }

  function renderOralSheetBBlockFinishV232() {
    if (typeof window.renderOralExamBlockFinishV2322 === "function") {
      window.accaouiPreviousGetOralBlockResultStatsV232 =
        window.accaouiPreviousGetOralBlockResultStatsV232 ||
        window.getOralBlockResultStatsV2321;

      window.getOralBlockResultStatsV2321 = function patchedGetOralBlockResultStatsForSheetBV232() {
        if (isOralSheetBSessionV232()) {
          return getOralSheetBBlockResultStatsV232();
        }

        if (typeof window.accaouiPreviousGetOralBlockResultStatsV232 === "function") {
          return window.accaouiPreviousGetOralBlockResultStatsV232();
        }

        return [];
      };

      window.renderOralExamBlockFinishV2322();

      window.getOralBlockResultStatsV2321 = window.accaouiPreviousGetOralBlockResultStatsV232;

      applyOralSheetBResultTextsV232();

      return;
    }

    if (typeof window.renderOralExamBlockFinishV2321 === "function") {
      window.renderOralExamBlockFinishV2321();
      applyOralSheetBResultTextsV232();
    }
  }

  function scheduleOralSheetBLabelsV232() {
    if (typeof scheduleOralSheetLabelsV2320 === "function") {
      scheduleOralSheetLabelsV2320();
    }
  }

  window.startOralSimulationSheetBV232 = function startOralSimulationSheetBV232() {
    if (typeof closeOralModeSheetV2314 === "function") {
      closeOralModeSheetV2314();
    }

    const questions = getOralExamSheetBQuestionsV232();

    if (questions.length !== 15) {
      showSmallNotice("Prüfungsbogen B konnte nicht geladen werden.");
      return;
    }

    resetOralSheetBRatingsV232();

    window.ACCAOUI_V2317_STARTING_15_SIMULATION = true;
    window.ACCAOUI_V2317_ORAL_SIMULATION_MODE = "15";

    startOralExamSessionV220(
      questions,
      "15-Minuten-Simulation · Prüfungsbogen B"
    );

    window.ACCAOUI_V2317_STARTING_15_SIMULATION = false;

    if (typeof startOralSimulationTimerV2317 === "function") {
      startOralSimulationTimerV2317();
    }

    if (typeof updateActiveExaminerV2317 === "function") {
      updateActiveExaminerV2317();
    }

    scheduleOralSheetBLabelsV232();
  };

  window.getOralExamSheetBQuestionsV232 = getOralExamSheetBQuestionsV232;

  window.accaouiPreviousShowOralExamModeSelectV232 =
    window.showOralExamModeSelectV2314;

  window.showOralExamModeSelectV2314 = function patchedShowOralExamModeSelectV232() {
    if (typeof window.accaouiPreviousShowOralExamModeSelectV232 === "function") {
      window.accaouiPreviousShowOralExamModeSelectV232();
    }

    const grid = document.querySelector(".oral-mode-grid-v2314");

    if (!grid || document.getElementById("oralModeSheetBBtnV232")) {
      return;
    }

    const button = document.createElement("button");
    button.type = "button";
    button.id = "oralModeSheetBBtnV232";
    button.className = "oral-mode-card-v2314";
    button.setAttribute("onclick", "startOralSimulationSheetBV232()");
    button.innerHTML = `
      <span>⏱️</span>
      <strong>15-Minuten-Simulation B</strong>
      <small>Neuer Accaoui-Trainingsbogen · 3 Prüfer · 15 Fragen</small>
    `;

    const primaryButton = grid.querySelector(".oral-mode-card-v2314.is-primary");

    if (primaryButton && primaryButton.nextElementSibling) {
      grid.insertBefore(button, primaryButton.nextElementSibling);
    } else if (primaryButton) {
      primaryButton.insertAdjacentElement("afterend", button);
    } else {
      grid.appendChild(button);
    }
  };

  window.accaouiPreviousStartOralExamSessionV232 =
    window.startOralExamSessionV220;

  window.startOralExamSessionV220 = function patchedStartOralExamSessionV232(questions, title) {
    const isSheetB =
      Array.isArray(questions) &&
      questions.some(question => question && question.sheetId === ORAL_SHEET_B_ID_V232);

    if (isSheetB) {
      resetOralSheetBRatingsV232();
    }

    if (typeof window.accaouiPreviousStartOralExamSessionV232 === "function") {
      return window.accaouiPreviousStartOralExamSessionV232(questions, title);
    }

    showSmallNotice("Mündliche Prüfungsrunde konnte nicht gestartet werden.");
  };

  window.accaouiPreviousRateOralExamQuestionV232 =
    window.rateOralExamQuestionV220;

  window.rateOralExamQuestionV220 = function patchedRateOralExamQuestionV232(status) {
    saveOralSheetBRatingV232(status);

    if (typeof window.accaouiPreviousRateOralExamQuestionV232 === "function") {
      const result = window.accaouiPreviousRateOralExamQuestionV232(status);

      if (isOralSheetBSessionV232()) {
        scheduleOralSheetBLabelsV232();
      }

      return result;
    }

    showSmallNotice("Bewertung konnte nicht gespeichert werden.");
  };

  window.accaouiPreviousShowOralExamFinishScreenV232 =
    window.showOralExamFinishScreenV220;

  window.showOralExamFinishScreenV220 = function patchedShowOralExamFinishScreenV232() {
    if (isOralSheetBSessionV232()) {
      renderOralSheetBBlockFinishV232();
      return;
    }

    if (isOralSheet15BlockSessionV232()) {
      if (typeof window.accaouiPreviousShowOralExamFinishScreenV232 === "function") {
        return window.accaouiPreviousShowOralExamFinishScreenV232();
      }

      return;
    }

    if (typeof window.accaouiPreviousShowOralExamFinishScreenV232 === "function") {
      return window.accaouiPreviousShowOralExamFinishScreenV232();
    }
  };

  try {
    showOralExamModeSelectV2314 = window.showOralExamModeSelectV2314;
    startOralExamSessionV220 = window.startOralExamSessionV220;
    rateOralExamQuestionV220 = window.rateOralExamQuestionV220;
    showOralExamFinishScreenV220 = window.showOralExamFinishScreenV220;
  } catch (error) {
    /* Rebinding je nach Browser nicht notwendig */
  }
}