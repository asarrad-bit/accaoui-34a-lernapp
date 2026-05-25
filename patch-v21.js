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