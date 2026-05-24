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
