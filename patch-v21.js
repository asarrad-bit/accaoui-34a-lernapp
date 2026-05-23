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
              <strong>${getCorrectAnswerText(question)}</strong>
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