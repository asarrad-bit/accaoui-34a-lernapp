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

  const cardsHtml = getSafeCategories().map(categoryName => {
    const questionCount = getCategoryQuestions(categoryName).length;
    const mistakeCount = getTopicMistakeCount(categoryName);
    const themeClass = getCategoryThemeClass(categoryName);

    return `
      <div class="category-card clickable-card flashcard-category-card ${themeClass}" data-category="${escapeHtml(categoryName)}" style="cursor:pointer;">
        <div class="category-icon" style="color:${categoryAccentColor};">
          ${categoryIcons[categoryName] || "🃏"}
        </div>

        <h3>${escapeHtml(categoryName)}</h3>
        <span>${questionCount} Lernkarten</span>

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
          Vorderseite: Frage. Rückseite: richtige Antwort und Erklärung.
        </p>
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

        <button class="next-btn secondary-btn" onclick="previousFlashcard()">
          Zurück
        </button>
      </div>

      <div class="flashcard-rating" id="flashcardRating" style="display:none;">
        <button class="next-btn" onclick="markFlashcardKnown()">
          Gewusst
        </button>

        <button class="next-btn danger-training-btn" onclick="markFlashcardUnknown()">
          Nicht gewusst
        </button>

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

  flashcardFlipped = true;
  inner.classList.add("flipped");

  if (frontActions) {
    frontActions.style.display = "none";
  }

  if (rating) {
    rating.style.display = "flex";
  }
}

window.getSafeCategories = getSafeCategories;
window.getCategoryThemeClass = getCategoryThemeClass;
window.buildCategoryCards = buildCategoryCards;
window.showFlashcardsPage = showFlashcardsPage;
window.renderFlashcard = renderFlashcard;
window.flipFlashcard = flipFlashcard;

/* =====================================================
   v21.5 LERNKARTEN – FORTSCHRITT SPEICHERN
===================================================== */

const FLASHCARD_PROGRESS_KEY = "accaoui_flashcard_progress";

function loadFlashcardProgress() {
  const saved = localStorage.getItem(FLASHCARD_PROGRESS_KEY);

  if (!saved) {
    return {};
  }

  try {
    return JSON.parse(saved);
  } catch (error) {
    console.error("Fehler beim Laden des Lernkarten-Fortschritts:", error);
    return {};
  }
}

function saveFlashcardProgressData(progressData) {
  localStorage.setItem(FLASHCARD_PROGRESS_KEY, JSON.stringify(progressData));
}

function saveSingleFlashcardProgress(question, status) {
  if (!question) return;

  const progressData = loadFlashcardProgress();
  const questionKey = typeof getQuestionKey === "function"
    ? getQuestionKey(question)
    : String(question.id || question.question || "");

  const oldEntry = progressData[questionKey] || {
    knownCount: 0,
    unknownCount: 0
  };

  progressData[questionKey] = {
    id: question.id || questionKey,
    category: question.category || "Ohne Kategorie",
    question: question.question || "",
    lastStatus: status,
    knownCount: Number(oldEntry.knownCount || 0) + (status === "known" ? 1 : 0),
    unknownCount: Number(oldEntry.unknownCount || 0) + (status === "unknown" ? 1 : 0),
    updatedAt: new Date().toISOString()
  };

  saveFlashcardProgressData(progressData);
}

/* Gewusst speichern */
function markFlashcardKnown() {
  const question = flashcardQuestions[flashcardIndex];

  if (question) {
    markQuestionAsAnswered(question);
    removeTopicMistake(question);
    saveSingleFlashcardProgress(question, "known");
  }

  flashcardKnownCount++;
  updateFlashcardProgress();
  nextFlashcard();
}

/* Nicht gewusst speichern */
function markFlashcardUnknown() {
  const question = flashcardQuestions[flashcardIndex];

  if (question) {
    saveTopicMistake(question);
    saveSingleFlashcardProgress(question, "unknown");
  }

  flashcardUnknownCount++;
  updateFlashcardProgress();
  nextFlashcard();
}

window.markFlashcardKnown = markFlashcardKnown;
window.markFlashcardUnknown = markFlashcardUnknown;
window.saveSingleFlashcardProgress = saveSingleFlashcardProgress;
window.loadFlashcardProgress = loadFlashcardProgress;
