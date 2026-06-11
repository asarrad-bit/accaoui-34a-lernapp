console.log("Accaoui §34a System gestartet");

/* =====================================================
   ACCAOUI §34a LERN-APP
   v15 MASTER app.js CLEAN
   Ziel:
   - saubere Lernlogik
   - offene Fragen stabil
   - Fehlertraining stabil
   - Prüfungsabgabe ohne automatisches Springen
   - vorbereitet für Online-Version / Login / PWA / App Store
===================================================== */


/* =========================
   GRUNDVARIABLEN
========================= */

let allQuestions = [];

let currentQuestions = [];
let currentQuestionIndex = 0;
let selectedAnswers = [];

let correctAnswersCount = 0;
let wrongAnswersCount = 0;

let examQuestions = [];
let examQuestionIndex = 0;
let examAnswers = {};
let examFocusQuestionIndexes = null;
let examFocusQuestionPosition = 0;
let examTimer = null;
let examSecondsLeft = 120 * 60;

let lastExamMistakes = [];
let examHistory = [];
let topicStats = {};
let topicMistakes = {};
let answeredQuestions = {};

let currentMode = "dashboard";
let currentTrainingTitle = "";

const APP_VERSION = "v21-lernkarten-modus-vorbereiten";

const DEFAULT_QUESTION_POINTS = 1;

// Technische Bestehensgrenze.
// Aktuell 50 %, später sauber an echte IHK-/Punkte-Logik anpassbar.
const EXAM_PASS_PERCENT = 50;

const EXAM_QUESTION_LIMIT = 10;
// Später für echte Simulation auf 82 ändern.
const EXAM_DURATION_SECONDS = 120 * 60;

const STORAGE_KEYS = {
  examHistory: "accaoui_exam_history",
  topicStats: "accaoui_topic_stats",
  topicMistakes: "accaoui_topic_mistakes",
  answeredQuestions: "accaoui_answered_questions",
  activeSession: "accaoui_active_session"
};

let examSessionTimerSaveTimeout = null;

const categories = [
  "Recht der öffentlichen Sicherheit und Ordnung",
  "Gewerberecht",
  "Datenschutzrecht",
  "Bürgerliches Gesetzbuch",
  "Strafgesetzbuch und Strafverfahrensrecht",
  "Umgang mit Waffen",
  "Unfallverhütungsvorschriften Wach- und Sicherungsdienste",
  "Umgang mit Menschen",
  "Grundzüge der Sicherheitstechnik"
];

const categoryIcons = {
  "Recht der öffentlichen Sicherheit und Ordnung": "⚖️",
  "Gewerberecht": "🏢",
  "Datenschutzrecht": "🔐",
  "Bürgerliches Gesetzbuch": "📄",
  "Strafgesetzbuch und Strafverfahrensrecht": "🚨",
  "Umgang mit Waffen": "🛡️",
  "Unfallverhütungsvorschriften Wach- und Sicherungsdienste": "🦺",
  "Umgang mit Menschen": "🗣️",
  "Grundzüge der Sicherheitstechnik": "📹"
};

const categoryAccentColor = "#2344c6";


/* =========================
   START
========================= */

document.addEventListener("DOMContentLoaded", () => {
  console.log("App-Version:", APP_VERSION);

  loadAllLocalData();
  activateDashboardButtons();
  renderDashboardResumeExamCard();
  loadQuestions();
});

async function loadQuestions() {
  try {
    const response = await fetch("questions.json?v=" + Date.now());

    if (!response.ok) {
      throw new Error("questions.json konnte nicht geladen werden.");
    }

    const data = await response.json();

    const rawQuestions = Array.isArray(data)
      ? data
      : Array.isArray(data.questions)
        ? data.questions
        : [];

    if (!Array.isArray(rawQuestions) || rawQuestions.length === 0) {
      throw new Error("questions.json enthält keine gültige Fragenliste.");
    }

    allQuestions = rawQuestions.map((question, index) => {
      return normalizeQuestion(question, index);
    });

    console.log("Fragen geladen:", allQuestions.length);

    buildCategoryCards();
    updateDashboardNumbers();
    renderDashboardResumeExamCard();

  } catch (error) {
    console.error("Fehler beim Laden der Fragen:", error);
    showSmallNotice("Fehler beim Laden der Fragenbank.");
  }
}


/* =========================
   LOKALE SPEICHERUNG
========================= */

function loadAllLocalData() {
  loadExamHistory();
  loadTopicStats();
  loadTopicMistakes();
  loadAnsweredQuestions();
}

function readStorage(key, fallbackValue) {
  const saved = localStorage.getItem(key);

  if (!saved) {
    return fallbackValue;
  }

  try {
    return JSON.parse(saved);
  } catch (error) {
    console.error("Fehler beim Lesen aus localStorage:", key, error);
    return fallbackValue;
  }
}

function writeStorage(key, value) {
  localStorage.setItem(key, JSON.stringify(value));
}

function getActiveSession() {
  return readStorage(STORAGE_KEYS.activeSession, null);
}

function saveActiveSession(session) {
  if (!session) {
    return;
  }

  writeStorage(STORAGE_KEYS.activeSession, session);
}

function clearActiveSession() {
  localStorage.removeItem(STORAGE_KEYS.activeSession);
}

function hasActiveExamSession() {
  const session = getActiveSession();

  return Boolean(
    session &&
    session.sessionType === "exam" &&
    Array.isArray(session.questions) &&
    session.questions.length > 0
  );
}

function saveActiveExamSession() {
  if (currentMode !== "exam" || !Array.isArray(examQuestions) || examQuestions.length === 0) {
    return;
  }

  const existing = getActiveSession();
  const now = new Date().toISOString();

  saveActiveSession({
    version: "v24.6c",
    sessionType: "exam",
    title: currentExamTitle,
    examType: currentExamType,
    examLimit: currentExamLimit,
    questions: examQuestions,
    currentIndex: examQuestionIndex,
    answers: examAnswers,
    secondsLeft: examSecondsLeft,
    focusQuestionIndexes: examFocusQuestionIndexes,
    focusQuestionPosition: examFocusQuestionPosition,
    createdAt: existing && existing.createdAt ? existing.createdAt : now,
    updatedAt: now
  });
}

function scheduleExamSessionTimerSave() {
  if (examSessionTimerSaveTimeout) {
    return;
  }

  examSessionTimerSaveTimeout = setTimeout(() => {
    examSessionTimerSaveTimeout = null;

    if (currentMode === "exam") {
      saveActiveExamSession();
    }
  }, 10000);
}

function resumeActiveExamSession() {
  const session = getActiveSession();

  if (!session || session.sessionType !== "exam") {
    showSmallNotice("Keine gespeicherte Prüfung gefunden.");
    return false;
  }

  if (!Array.isArray(session.questions) || session.questions.length === 0) {
    showSmallNotice("Gespeicherte Prüfung ist ungültig.");
    clearActiveSession();
    renderDashboardResumeExamCard();
    return false;
  }

  currentMode = "exam";
  examQuestions = session.questions;
  examQuestionIndex = Number(session.currentIndex) || 0;
  examAnswers = session.answers || {};
  examSecondsLeft =
    Number.isFinite(Number(session.secondsLeft))
      ? Number(session.secondsLeft)
      : EXAM_DURATION_SECONDS;
  examFocusQuestionIndexes = Array.isArray(session.focusQuestionIndexes)
    ? session.focusQuestionIndexes
    : null;
  examFocusQuestionPosition = Number(session.focusQuestionPosition) || 0;
  currentExamTitle = session.title || "§34a Kurzprüfung";
  currentExamType = session.examType || "short";
  currentExamLimit = Number(session.examLimit) || examQuestions.length;

  showExamView(true);

  if (examHasTimer()) {
    startExamTimer();
  } else {
    clearExamTimer();
  }

  renderExamQuestion();
  return true;
}

function pauseExam() {
  saveActiveExamSession();
  clearExamTimer();
  showExamPausedNotice();
}

function showExamPausedNotice() {
  const mainContent = document.querySelector(".main-content");

  if (!mainContent) return;

  const session = getActiveSession();
  const title = session && session.title ? session.title : currentExamTitle;

  mainContent.innerHTML = `
    <section class="review-wrapper">
      <div class="review-header">
        <p class="eyebrow">Prüfung pausiert</p>
        <h1>${escapeHtml(title)}</h1>
        <p>
          Ihre Prüfung wurde gespeichert. Sie können sie jederzeit vom Dashboard
          oder hier fortsetzen.
        </p>
      </div>

      <div class="last-exam-box">
        <span>Gespeichert</span>
        <strong>Fortsetzen jederzeit möglich</strong>
        <p>Es wurde keine Auswertung gestartet und keine Fehler gespeichert.</p>

        <div class="result-actions">
          <button class="next-btn" onclick="resumeActiveExamSession()">
            Prüfung fortsetzen
          </button>

          <button class="next-btn secondary-btn" onclick="location.reload()">
            Zum Dashboard
          </button>
        </div>
      </div>
    </section>
  `;
}

function discardSavedExamSession() {
  if (!hasActiveExamSession()) {
    return;
  }

  if (!confirm("Gespeicherte Prüfung wirklich löschen?")) {
    return;
  }

  clearActiveSession();
  renderDashboardResumeExamCard();
  showSmallNotice("Gespeicherte Prüfung wurde gelöscht.");
}

function renderDashboardResumeExamCard() {
  const existing = document.getElementById("examResumeCard");

  if (existing) {
    existing.remove();
  }

  if (!hasActiveExamSession()) {
    return;
  }

  const session = getActiveSession();
  const mainContent = document.querySelector(".main-content");
  const heroGrid = document.querySelector(".hero-grid");

  if (!mainContent || !heroGrid) {
    return;
  }

  const title = session.title || "Gespeicherte Prüfung";
  const questionLabel =
    Number.isFinite(Number(session.currentIndex)) && Array.isArray(session.questions)
      ? "Frage " + (Number(session.currentIndex) + 1) + "/" + session.questions.length
      : "Fortsetzen möglich";

  const card = document.createElement("section");
  card.id = "examResumeCard";
  card.className = "last-exam-box";
  card.innerHTML = `
    <span>Angefangene Prüfung</span>
    <strong>${escapeHtml(title)}</strong>
    <p>${escapeHtml(questionLabel)} · gespeichert am ${escapeHtml(formatSessionDate(session.updatedAt))}</p>

    <div class="result-actions">
      <button class="next-btn" onclick="resumeActiveExamSession()">
        Prüfung fortsetzen
      </button>

      <button class="next-btn secondary-btn" onclick="discardSavedExamSession()">
        Gespeicherte Prüfung löschen
      </button>
    </div>
  `;

  heroGrid.parentNode.insertBefore(card, heroGrid);
}

function formatSessionDate(isoDate) {
  if (!isoDate) {
    return "unbekannt";
  }

  const date = new Date(isoDate);

  if (Number.isNaN(date.getTime())) {
    return "unbekannt";
  }

  return date.toLocaleString("de-DE");
}


/* =========================
   FRAGEN NORMALISIEREN
========================= */

function normalizeQuestion(question, index) {
  const category = normalizeCategoryName(
    question.category ||
    question.topic ||
    question.thema ||
    "Ohne Kategorie"
  );

  const questionText =
    question.question ||
    question.text ||
    question.frage ||
    "";

  const answers = normalizeAnswers(question);
  const correct = normalizeCorrectIndexes(question, answers);

  const explanation =
    question.explanation ||
    question.erklaerung ||
    question.erklärung ||
    "";

  const id =
    question.id !== undefined && question.id !== null
      ? String(question.id)
      : createGeneratedQuestionId(category, questionText, index);

  return {
    ...question,
    id,
    category,
    question: String(questionText),
    answers,
    correct,
    explanation: String(explanation)
  };
}

function normalizeCategoryName(categoryName) {
  const value = String(categoryName || "").trim();

  const categoryMap = {
    "Bürgerliches Recht": "Bürgerliches Gesetzbuch",
    "Bürgerliches Gesetzbuch": "Bürgerliches Gesetzbuch",

    "Straf- und Strafverfahrensrecht": "Strafgesetzbuch und Strafverfahrensrecht",
    "Strafgesetzbuch und Strafverfahrensrecht": "Strafgesetzbuch und Strafverfahrensrecht",

    "Grundzüge des Waffenrechts": "Umgang mit Waffen",
    "Waffenrecht": "Umgang mit Waffen",
    "Umgang mit Waffen": "Umgang mit Waffen",

    "Unfallverhütungsvorschrift": "Unfallverhütungsvorschriften Wach- und Sicherungsdienste",
    "Unfallverhütungsvorschrift Wach- und Sicherungsdienste": "Unfallverhütungsvorschriften Wach- und Sicherungsdienste",
    "Unfallverhütungsvorschriften Wach- und Sicherungsdienste": "Unfallverhütungsvorschriften Wach- und Sicherungsdienste"
  };

  return categoryMap[value] || value;
}

function normalizeAnswers(question) {
  const rawAnswers =
    question.answers ||
    question.options ||
    question.antworten ||
    [];

  if (!Array.isArray(rawAnswers)) {
    return [];
  }

  return rawAnswers.map(answer => {
    if (typeof answer === "object" && answer !== null) {
      return String(
        answer.text ||
        answer.answer ||
        answer.label ||
        answer.value ||
        ""
      );
    }

    return String(answer);
  });
}

function normalizeCorrectIndexes(question, answers) {
  let rawCorrect = [];

  if (Array.isArray(question.correct)) {
    rawCorrect = question.correct;
  } else if (Array.isArray(question.correctAnswers)) {
    rawCorrect = question.correctAnswers;
  } else if (Array.isArray(question.correctAnswer)) {
    rawCorrect = question.correctAnswer;
  } else if (Array.isArray(question.correctIndexes)) {
    rawCorrect = question.correctIndexes;
  } else if (question.correct !== undefined && question.correct !== null) {
    rawCorrect = [question.correct];
  } else if (question.correctAnswer !== undefined && question.correctAnswer !== null) {
    rawCorrect = [question.correctAnswer];
  } else {
    const rawAnswers =
      question.answers ||
      question.options ||
      question.antworten ||
      [];

    rawAnswers.forEach((answer, index) => {
      if (
        typeof answer === "object" &&
        answer !== null &&
        answer.correct === true
      ) {
        rawCorrect.push(index);
      }
    });
  }

  const indexes = rawCorrect
    .map(value => {
      if (typeof value === "number") {
        return value;
      }

      const textValue = String(value).trim();

      if (/^\d+$/.test(textValue)) {
        return Number(textValue);
      }

      return answers.findIndex(answer => answer.trim() === textValue);
    })
    .filter(index => Number.isInteger(index) && index >= 0);

  return [...new Set(indexes)].sort((a, b) => a - b);
}

function createGeneratedQuestionId(category, questionText, index) {
  const base = category + "|" + questionText + "|" + index;
  return "q_" + simpleHash(base);
}

function simpleHash(text) {
  let hash = 0;

  for (let i = 0; i < text.length; i++) {
    hash = ((hash << 5) - hash) + text.charCodeAt(i);
    hash |= 0;
  }

  return Math.abs(hash).toString(36);
}


/* =========================
   DASHBOARD
========================= */

function activateDashboardButtons() {
  activateSidebarButtons();
  activateHeroCards();
}



function activateSidebarButtons() {
  const menuItems = document.querySelectorAll(".menu-item");

  menuItems.forEach(item => {
    const text = item.innerText.trim();

    item.style.cursor = "pointer";

    if (text.includes("Dashboard")) {
      item.onclick = () => location.reload();
    }

    if (text.includes("Statistik")) {
      item.onclick = () => showStatsPage();
    }

    if (text.includes("Alle Fragen")) {
      item.onclick = () => showAllQuestions();
    }

if (text.includes("Lernkarten")) {
  item.onclick = () => showFlashcardsPage();
}
    if (text.includes("Prüfung") && !text.includes("Mündliche")) {
      item.onclick = () => startExamMode();
    }

    if (text.includes("Fehlertraining")) {
      item.onclick = () => showMistakeOverview();
    }

    if (text.includes("Mündliche Prüfung")) {
      item.onclick = () => showOralExamPage();
    }
  });
}

function activateHeroCards() {
  const allQuestionsCard = document.getElementById("allQuestionsCard");
  const openQuestionsCard = document.getElementById("openQuestionsCard");
  const examCard = document.getElementById("examCard");
  const mistakeTrainingCard = document.getElementById("mistakeTrainingCard");

  if (allQuestionsCard) {
    allQuestionsCard.style.cursor = "pointer";
    allQuestionsCard.onclick = () => {
      console.log("Alle Fragen geklickt");
      showAllQuestions();
    };
  }

  if (openQuestionsCard) {
    openQuestionsCard.style.cursor = "pointer";
    openQuestionsCard.onclick = () => {
      console.log("Offene Fragen geklickt");
      startOpenQuestionsTraining();
    };
  }

  if (examCard) {
    examCard.style.cursor = "pointer";
    examCard.onclick = () => {
      console.log("Prüfung geklickt");
      startExamMode();
    };
  }

  if (mistakeTrainingCard) {
    mistakeTrainingCard.style.cursor = "pointer";
    mistakeTrainingCard.onclick = () => {
      console.log("Fehlertraining geklickt");
      showMistakeOverview();
    };
  }

  // Fallback, falls IDs in index.html fehlen
  const heroCards = document.querySelectorAll(".hero-card");

  heroCards.forEach(card => {
    const text = card.innerText || "";

    if (!openQuestionsCard && text.includes("Offene Fragen")) {
      card.style.cursor = "pointer";
      card.onclick = () => startOpenQuestionsTraining();
    }
  });
}

function updateDashboardNumbers() {
  const heroCards = document.querySelectorAll(".hero-card");

  const allQuestionsCard = document.getElementById("allQuestionsCard") || heroCards[0];
  const openQuestionsCard = document.getElementById("openQuestionsCard") || heroCards[1];
  const mistakeTrainingCard = document.getElementById("mistakeTrainingCard") || heroCards[3];

  if (allQuestionsCard) {
    const p = allQuestionsCard.querySelector("p");
    if (p) p.innerText = allQuestions.length + " Fragen verfügbar";
  }

  if (openQuestionsCard) {
    const p = openQuestionsCard.querySelector("p");
    if (p) p.innerText = getOpenQuestionsCount() + " unbeantwortet";
  }

  if (mistakeTrainingCard) {
    const p = mistakeTrainingCard.querySelector("p");
    if (p) p.innerText = getTotalTopicMistakeCount() + " Fragen wiederholen";
  }
}

function showAllQuestions() {
  currentMode = "all-questions";

  const mainContent = document.querySelector(".main-content");

  if (!mainContent) return;

  mainContent.innerHTML = `
    <button class="back-btn" onclick="location.reload()">
      ← Zurück zum Dashboard
    </button>

    <section class="review-wrapper">

      <div class="review-header">
        <p class="eyebrow">Alle Fragen</p>
        <h1>Fragen nach Themenbereichen</h1>
        <p>Wählen Sie ein Thema aus, um den Lernmodus zu starten.</p>
      </div>

      <div class="category-grid">
        ${categories.map(categoryName => {
          const questionCount = getCategoryQuestions(categoryName).length;
          const mistakeCount = getTopicMistakeCount(categoryName);
          const openCount = getCategoryOpenQuestions(categoryName).length;

          return `
            <div class="category-card clickable-card" onclick='openCategory(${JSON.stringify(categoryName)})'>

              <div class="category-icon" style="color:${categoryAccentColor};">
                ${categoryIcons[categoryName] || "📘"}
              </div>

              <h3>${escapeHtml(categoryName)}</h3>

              <span>${questionCount} Fragen</span>

              <small style="
                display:block;
                margin-top:6px;
                color:#64748b;
                font-weight:500;
              ">
                ${openCount} offen
              </small>

              <small style="
                display:block;
                margin-top:4px;
                color:${mistakeCount > 0 ? "#991b1b" : "#64748b"};
                font-weight:${mistakeCount > 0 ? "700" : "500"};
              ">
                ${mistakeCount} Fehler gespeichert
              </small>

            </div>
          `;
        }).join("")}
      </div>

    </section>
  `;
}

function showOpenQuestions() {
  startOpenQuestionsTraining();
}

function showOralExamPage() {
  currentMode = "oral-exam";

  const mainContent = document.querySelector(".main-content");

  if (!mainContent) return;

  mainContent.innerHTML = `
    <button class="back-btn" onclick="location.reload()">
      ← Zurück zum Dashboard
    </button>

    <section class="result-wrapper">

      <div class="review-header">
        <p class="eyebrow">Mündliche Prüfung</p>
        <h1>Mündliche Prüfung wird vorbereitet</h1>
        <p>
          Hier entsteht später der mündliche Prüfungsmodus mit typischen Fragen,
          Musterantworten, Prüfermodus und Bewertungslogik.
        </p>
      </div>

    </section>
  `;
}


/* =========================
   LERNMODUS
========================= */

function openCategory(categoryName) {
  const questions = getCategoryQuestions(categoryName);

  if (questions.length === 0) {
    alert("Für diese Kategorie sind noch keine Fragen vorhanden.");
    return;
  }

  startLearningSession(questions, categoryName, "category");
}

function startLearningSession(questions, title, mode) {
  clearExamTimer();

  currentMode = mode || "learning";
  currentTrainingTitle = title || "Lernmodus";

  currentQuestions = shuffleArray([...questions]).map(question =>
    createShuffledQuestion(question)
  );
  currentQuestionIndex = 0;
  selectedAnswers = [];

  correctAnswersCount = 0;
  wrongAnswersCount = 0;

  showLearningView(currentTrainingTitle);
}

function showLearningView(title) {
  const mainContent = document.querySelector(".main-content");

  if (!mainContent) return;

  mainContent.innerHTML = `
    <button class="back-btn" onclick="location.reload()">
      ← Zurück zum Dashboard
    </button>

    <div class="learning-header">
      <div>
        <p class="eyebrow">Lernmodus</p>
        <h1>${escapeHtml(title)}</h1>
      </div>

      <div class="score-box">
        <span>Frage</span>
        <strong id="questionCounter">1/${currentQuestions.length}</strong>
      </div>
    </div>

    <div class="progress-wrapper">
      <div class="progress-info">
        <span id="progressText">0%</span>
        <span id="resultStats">0 richtig · 0 falsch</span>
      </div>

      <div class="progress-bar">
        <div class="progress-fill" id="progressFill"></div>
      </div>
    </div>

    <section class="question-card" id="questionArea"></section>
  `;

  renderQuestion();
}

function renderQuestion() {
  selectedAnswers = [];

  const question = currentQuestions[currentQuestionIndex];
  const questionArea = document.getElementById("questionArea");

  if (!question || !questionArea) {
    return;
  }

  const correctCount = question.correct.length;

  questionArea.innerHTML = `
    ${formatQuestionText(question.question)}

    <div class="exam-hint-box">
      <strong>
        ${
          correctCount === 1
            ? "Es ist 1 Antwort richtig."
            : "Es sind " + correctCount + " Antworten richtig."
        }
      </strong>
    </div>

    <div class="answers">
      ${question.answers.map((answer, index) => `
        <button class="answer-btn" data-index="${index}">
          ${escapeHtml(answer)}
        </button>
      `).join("")}
    </div>

    <div class="explanation" id="explanationBox" style="display:none;"></div>

    <button class="next-btn" id="nextBtn" style="display:none;">
      Nächste Frage
    </button>
  `;

  document.querySelectorAll(".answer-btn").forEach(button => {
    button.onclick = () => selectAnswer(button);
  });

  const nextBtn = document.getElementById("nextBtn");

  if (nextBtn) {
    nextBtn.onclick = nextQuestion;
  }
}

function selectAnswer(button) {
  const question = currentQuestions[currentQuestionIndex];

  if (!question) return;

  const maxAnswers = question.correct.length;
  const index = Number(button.dataset.index);

  if (selectedAnswers.includes(index)) {
    selectedAnswers = selectedAnswers.filter(i => i !== index);
    button.classList.remove("selected");
  } else {
    if (selectedAnswers.length >= maxAnswers) {
      showSmallNotice(
        maxAnswers === 1
          ? "Bei dieser Frage ist nur 1 Antwort möglich."
          : "Bei dieser Frage sind maximal " + maxAnswers + " Antworten möglich."
      );
      return;
    }

    selectedAnswers.push(index);
    button.classList.add("selected");
  }

  checkAnswerWhenComplete();
}

function checkAnswerWhenComplete() {
  const question = currentQuestions[currentQuestionIndex];

  if (!question) return;

  if (selectedAnswers.length !== question.correct.length) {
    return;
  }

  checkLearningAnswer();
}

function checkLearningAnswer() {
  const question = currentQuestions[currentQuestionIndex];

  if (!question) return;

  const correct = question.correct;

  const selectedSorted = [...selectedAnswers].sort((a, b) => a - b).join(",");
  const correctSorted = [...correct].sort((a, b) => a - b).join(",");

  const isCorrect = selectedSorted === correctSorted;

  if (isCorrect) {
    correctAnswersCount++;
  } else {
    wrongAnswersCount++;
  }

  saveTopicResult(question.category, isCorrect);
  markQuestionAsAnswered(question);

  if (isCorrect) {
    removeTopicMistake(question);
  } else {
    saveTopicMistake(question);
  }

  updateProgress();
  updateDashboardNumbers();

  document.querySelectorAll(".answer-btn").forEach(button => {
    const index = Number(button.dataset.index);

    button.disabled = true;

    if (correct.includes(index)) {
      button.classList.add("correct");
    }

    if (selectedAnswers.includes(index) && !correct.includes(index)) {
      button.classList.add("wrong");
    }
  });

  const explanationBox = document.getElementById("explanationBox");

  if (explanationBox) {
    explanationBox.style.display = "block";
    explanationBox.innerHTML = `
      <h3>${isCorrect ? "Richtig" : "Falsch"}</h3>
      <p>${escapeHtml(question.explanation || "")}</p>
    `;
  }

  const nextBtn = document.getElementById("nextBtn");

  if (nextBtn) {
    nextBtn.style.display = "inline-block";
  }
}

function nextQuestion() {
  currentQuestionIndex++;

  if (currentQuestionIndex >= currentQuestions.length) {
    showFinishScreen();
    return;
  }

  const questionCounter = document.getElementById("questionCounter");

  if (questionCounter) {
    questionCounter.innerText =
      `${currentQuestionIndex + 1}/${currentQuestions.length}`;
  }

  renderQuestion();
}

function updateProgress() {
  const total = currentQuestions.length;
  const answered = correctAnswersCount + wrongAnswersCount;
  const percent = total > 0 ? Math.round((answered / total) * 100) : 0;

  const progressFill = document.getElementById("progressFill");
  const progressText = document.getElementById("progressText");
  const resultStats = document.getElementById("resultStats");

  if (progressFill) progressFill.style.width = percent + "%";
  if (progressText) progressText.innerText = percent + "%";

  if (resultStats) {
    resultStats.innerText =
      correctAnswersCount + " richtig · " + wrongAnswersCount + " falsch";
  }
}

function showFinishScreen() {
  const total = currentQuestions.length;
  const percent = total > 0
    ? Math.round((correctAnswersCount / total) * 100)
    : 0;

  const passed = percent >= 50;

  const mainContent = document.querySelector(".main-content");

  if (!mainContent) return;

  mainContent.innerHTML = `
    <button class="back-btn" onclick="location.reload()">
      ← Zurück zum Dashboard
    </button>

    <div class="finish-card">
      <h1>${passed ? "Lerneinheit bestanden" : "Lerneinheit nicht bestanden"}</h1>

      <p>Ergebnis: ${percent}%</p>

      <p>${correctAnswersCount} richtig · ${wrongAnswersCount} falsch</p>

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
    </div>
  `;
}


/* =========================
   OFFENE FRAGEN / LERNFORTSCHRITT
========================= */

function loadAnsweredQuestions() {
  answeredQuestions = readStorage(STORAGE_KEYS.answeredQuestions, {});
}

function saveAnsweredQuestions() {
  writeStorage(STORAGE_KEYS.answeredQuestions, answeredQuestions);
}

function markQuestionAsAnswered(question) {
  if (!question) return;

  const questionKey = getQuestionKey(question);

  answeredQuestions[questionKey] = {
    id: question.id || questionKey,
    category: question.category || "Ohne Kategorie",
    answeredAt: new Date().toISOString()
  };

  saveAnsweredQuestions();
}

function isQuestionAnswered(question) {
  if (!question) return false;

  const questionKey = getQuestionKey(question);

  return Boolean(answeredQuestions[questionKey]);
}

function getAnsweredQuestionsCount() {
  return Object.keys(answeredQuestions).length;
}

function getOpenQuestions() {
  return allQuestions.filter(question => !isQuestionAnswered(question));
}

function getOpenQuestionsCount() {
  return getOpenQuestions().length;
}

function getCategoryOpenQuestions(categoryName) {
  return getCategoryQuestions(categoryName).filter(question => {
    return !isQuestionAnswered(question);
  });
}

function startOpenQuestionsTraining() {
  loadAnsweredQuestions();

  console.log("startOpenQuestionsTraining wurde gestartet");

  if (!allQuestions || allQuestions.length === 0) {
    showSmallNotice("Fragenbank wurde noch nicht geladen.");
    return;
  }

  const openQuestions = getOpenQuestions();

  console.log("Offene Fragen gefunden:", openQuestions.length);

  if (openQuestions.length === 0) {
    showSmallNotice("Sehr gut. Es gibt aktuell keine offenen Fragen.");
    return;
  }

  startLearningSession(
    openQuestions,
    "Offene Fragen beantworten",
    "open-questions"
  );
}

/* =========================
   LERNKARTEN-MODUS
========================= */

let flashcardQuestions = [];
let flashcardIndex = 0;
let flashcardFlipped = false;
let flashcardKnownCount = 0;
let flashcardUnknownCount = 0;

function startFlashcardSessionByCategory(categoryName) {
  const questions = getCategoryQuestions(categoryName);

  if (questions.length === 0) {
    showSmallNotice("Für dieses Thema sind noch keine Lernkarten vorhanden.");
    return;
  }

  startFlashcardSession(questions, categoryName);
}

function startFlashcardsFromMistakes() {
  let mistakes = [];

  Object.values(topicMistakes).forEach(list => {
    if (Array.isArray(list)) {
      mistakes = mistakes.concat(list);
    }
  });

  if (mistakes.length === 0) {
    showSmallNotice("Keine Fehler für Lernkarten vorhanden.");
    return;
  }

  startFlashcardSession(mistakes, "Fehler-Lernkarten");
}

function startFlashcardSession(questions, title) {
  currentMode = "flashcards";

  flashcardQuestions = shuffleArray([...questions]);
  flashcardIndex = 0;
  flashcardFlipped = false;
  flashcardKnownCount = 0;
  flashcardUnknownCount = 0;

  showFlashcardView(title || "Lernkarten");
}

function showFlashcardView(title) {
  const mainContent = document.querySelector(".main-content");

  if (!mainContent) return;

  mainContent.innerHTML = `
    <button class="back-btn" onclick="showFlashcardsPage()">
      ← Zurück zu den Lernkarten
    </button>

    <div class="learning-header">
      <div>
        <p class="eyebrow">Lernkarten-Modus</p>
        <h1>${escapeHtml(title)}</h1>
      </div>

      <div class="score-box">
        <span>Karte</span>
        <strong id="flashcardCounter">1/${flashcardQuestions.length}</strong>
      </div>
    </div>

    <div class="progress-wrapper">
      <div class="progress-info">
        <span id="flashcardProgressText">0%</span>
        <span id="flashcardStats">0 gewusst · 0 nicht gewusst</span>
      </div>

      <div class="progress-bar">
        <div class="progress-fill" id="flashcardProgressFill"></div>
      </div>
    </div>

    <section class="flashcard-wrapper" id="flashcardArea"></section>
  `;

  renderFlashcard();
}

function flipFlashcard() {
  const inner = document.getElementById("flashcardInner");
  const rating = document.getElementById("flashcardRating");
  const button = document.getElementById("showFlashcardAnswerBtn");

  if (!inner) return;

  flashcardFlipped = true;

  inner.classList.add("flipped");

  if (rating) {
    rating.style.display = "flex";
  }

  if (button) {
    button.disabled = true;
    button.innerText = "Antwort angezeigt";
  }
}

// Duplicate simple mark functions removed here in favor of the
// v21.5 progress-tracking implementations later in this file.
// The v21.5 implementations perform the same actions and also
// persist flashcard progress (see definitions near FLASHCARD_PROGRESS_KEY).

function nextFlashcard() {
  if (flashcardIndex >= flashcardQuestions.length - 1) {
    showFlashcardFinishScreen();
    return;
  }

  flashcardIndex++;
  renderFlashcard();
}

function previousFlashcard() {
  if (flashcardIndex <= 0) {
    showSmallNotice("Sie sind bereits bei der ersten Karte.");
    return;
  }

  flashcardIndex--;
  renderFlashcard();
}

function updateFlashcardProgress() {
  const total = flashcardQuestions.length;
  const seen = flashcardIndex + 1;
  const percent = total > 0 ? Math.round((seen / total) * 100) : 0;

  const counter = document.getElementById("flashcardCounter");
  const progressText = document.getElementById("flashcardProgressText");
  const progressFill = document.getElementById("flashcardProgressFill");
  const stats = document.getElementById("flashcardStats");

  if (counter) {
    counter.innerText = `${seen}/${total}`;
  }

  if (progressText) {
    progressText.innerText = percent + "%";
  }

  if (progressFill) {
    progressFill.style.width = percent + "%";
  }

  if (stats) {
    stats.innerText =
      flashcardKnownCount + " gewusst · " +
      flashcardUnknownCount + " nicht gewusst";
  }
}

function showFlashcardFinishScreen() {
  const totalRated = flashcardKnownCount + flashcardUnknownCount;
  const percent =
    totalRated > 0
      ? Math.round((flashcardKnownCount / totalRated) * 100)
      : 0;

  const mainContent = document.querySelector(".main-content");

  if (!mainContent) return;

  mainContent.innerHTML = `
    <button class="back-btn" onclick="showFlashcardsPage()">
      ← Zurück zu den Lernkarten
    </button>

    <div class="finish-card">
      <h1>Lernkarten beendet</h1>

      <p>Ergebnis: ${percent}% gewusst</p>

      <p>${flashcardKnownCount} gewusst · ${flashcardUnknownCount} nicht gewusst</p>

      <div class="result-actions">
        <button class="next-btn" onclick="showFlashcardsPage()">
          Lernkartenübersicht
        </button>

        ${
          getTotalTopicMistakeCount() > 0
            ? `<button class="next-btn danger-training-btn" onclick="startFlashcardsFromMistakes()">Fehler-Lernkarten starten</button>`
            : ""
        }

        <button class="next-btn secondary-btn" onclick="location.reload()">
          Zurück zum Dashboard
        </button>
      </div>
    </div>
  `;
}

function getCorrectAnswerText(question) {
  if (!question || !Array.isArray(question.correct)) {
    return "Keine richtige Antwort hinterlegt.";
  }

  return question.correct
    .map(index => question.answers[index])
    .filter(Boolean)
    .map(answer => escapeHtml(answer))
    .join("<br>");
}

/* =========================
   FEHLERTRAINING NACH THEMEN
========================= */

function loadTopicMistakes() {
  const saved = readStorage(STORAGE_KEYS.topicMistakes, {});

  topicMistakes = {};

  Object.keys(saved).forEach(categoryName => {
    const normalizedCategory = normalizeCategoryName(categoryName);
    const list = Array.isArray(saved[categoryName]) ? saved[categoryName] : [];

    topicMistakes[normalizedCategory] = list.map((question, index) => {
      return normalizeQuestion(question, index);
    });
  });
}

function saveTopicMistakes() {
  writeStorage(STORAGE_KEYS.topicMistakes, topicMistakes);
}

function saveTopicMistake(question) {
  if (!question || !question.category) {
    return;
  }

  const categoryName = question.category;
  const questionKey = getQuestionKey(question);

  if (!topicMistakes[categoryName]) {
    topicMistakes[categoryName] = [];
  }

  const alreadySaved = topicMistakes[categoryName].some(savedQuestion => {
    return getQuestionKey(savedQuestion) === questionKey;
  });

  if (!alreadySaved) {
    topicMistakes[categoryName].push(question);
  }

  saveTopicMistakes();
}

function removeTopicMistake(question) {
  if (!question || !question.category) {
    return;
  }

  const categoryName = question.category;
  const questionKey = getQuestionKey(question);

  if (!topicMistakes[categoryName]) {
    return;
  }

  topicMistakes[categoryName] = topicMistakes[categoryName].filter(savedQuestion => {
    return getQuestionKey(savedQuestion) !== questionKey;
  });

  if (topicMistakes[categoryName].length === 0) {
    delete topicMistakes[categoryName];
  }

  saveTopicMistakes();
}

function getTopicMistakeCount(categoryName) {
  if (!topicMistakes[categoryName]) {
    return 0;
  }

  return topicMistakes[categoryName].length;
}

function getTotalTopicMistakeCount() {
  let total = 0;

  Object.values(topicMistakes).forEach(list => {
    if (Array.isArray(list)) {
      total += list.length;
    }
  });

  return total;
}

function startTopicMistakeTraining(categoryName) {
  const mistakes = topicMistakes[categoryName] || [];

  if (mistakes.length === 0) {
    showSmallNotice("Keine Fehler in diesem Thema vorhanden.");
    return;
  }

  startLearningSession(
    mistakes,
    "Fehlertraining: " + categoryName,
    "topic-mistakes"
  );
}

function startAllTopicMistakeTraining() {
  let allMistakes = [];

  Object.values(topicMistakes).forEach(list => {
    if (Array.isArray(list)) {
      allMistakes = allMistakes.concat(list);
    }
  });

  if (allMistakes.length === 0) {
    showSmallNotice("Keine gespeicherten Fehler vorhanden.");
    return;
  }

  startLearningSession(
    allMistakes,
    "Fehlertraining alle Themen",
    "all-mistakes"
  );
}

function showMistakeOverview() {
  currentMode = "mistake-overview";

  const mainContent = document.querySelector(".main-content");

  if (!mainContent) return;

  const totalMistakes = getTotalTopicMistakeCount();

  let strongestMistakeCategory = null;
  let highestMistakeCount = 0;

  categories.forEach(categoryName => {
    const count = getTopicMistakeCount(categoryName);

    if (count > highestMistakeCount) {
      highestMistakeCount = count;
      strongestMistakeCategory = categoryName;
    }
  });

  const topicsWithMistakes = categories.filter(categoryName => {
    return getTopicMistakeCount(categoryName) > 0;
  }).length;

  const topicRows = categories.map(categoryName => {
    const mistakeCount = getTopicMistakeCount(categoryName);
    const icon = categoryIcons[categoryName] || "📘";

    let statusText = "OK";
    let statusClass = "topic-neutral";

    if (mistakeCount >= 5) {
      statusText = "Kritisch";
      statusClass = "topic-weak";
    } else if (mistakeCount >= 3) {
      statusText = "Wiederholen";
      statusClass = "topic-medium";
    } else if (mistakeCount >= 1) {
      statusText = "Nacharbeiten";
      statusClass = "topic-medium";
    }

    return `
      <div class="topic-stat-row">

        <div class="topic-name">
          <span>Thema</span>
          <strong>${icon} ${escapeHtml(categoryName)}</strong>
        </div>

        <div>
          <span>Fehler</span>
          <strong>${mistakeCount > 0 ? mistakeCount : "keine"}</strong>
        </div>

        <div>
          <span>Status</span>
          <strong class="${statusClass}">${statusText}</strong>
        </div>

        <div>
          ${
            mistakeCount > 0
              ? `<button class="next-btn danger-training-btn" onclick='startTopicMistakeTraining(${JSON.stringify(categoryName)})'>Trainieren</button>`
              : ""
          }
        </div>

      </div>
    `;
  }).join("");

  mainContent.innerHTML = `
    <button class="back-btn" onclick="location.reload()">
      ← Zurück zum Dashboard
    </button>

    <section class="result-wrapper">

      <div class="review-header">
        <p class="eyebrow">Fehlertraining</p>
        <h1>Fehler nach Themenbereichen</h1>
        <p>
          Trainieren Sie gezielt die Themen, in denen falsche Antworten gespeichert wurden.
        </p>
      </div>

      <div class="stats-grid">

        <div class="stats-card danger">
          <span>Gespeicherte Fehler</span>
          <strong>${totalMistakes}</strong>
        </div>

        <div class="stats-card">
          <span>Themen mit Fehlern</span>
          <strong>${topicsWithMistakes}</strong>
        </div>

        <div class="stats-card gold-stat">
          <span>Schwerpunkt</span>
          <strong>
            ${
              strongestMistakeCategory
                ? highestMistakeCount + " Fehler"
                : "Keine"
            }
          </strong>
        </div>

      </div>

      ${
        strongestMistakeCategory
          ? `
            <div class="last-exam-box">
              <span>Empfehlung</span>
              <strong>${escapeHtml(strongestMistakeCategory)}</strong>
              <p>
                Dieses Thema hat aktuell die meisten gespeicherten Fehler.
                Beginnen Sie hier mit dem Training.
              </p>

              <button class="next-btn danger-training-btn" onclick='startTopicMistakeTraining(${JSON.stringify(strongestMistakeCategory)})'>
                Schwerpunkt trainieren
              </button>
            </div>
          `
          : `
            <div class="last-exam-box">
              <span>Sehr gut</span>
              <strong>Keine gespeicherten Fehler</strong>
              <p>
                Aktuell sind keine Fehler gespeichert. Starten Sie eine Prüfung oder trainieren Sie ein Thema.
              </p>
            </div>
          `
      }

      <div class="topic-stats-section">

        <div class="section-head">
          <h2>Fehlerübersicht nach Themen</h2>
          <p>Jedes Thema kann separat trainiert werden.</p>
        </div>

        <div class="topic-stats-list">
          ${topicRows}
        </div>

      </div>

      <div class="result-actions">

        ${
          totalMistakes > 0
            ? `<button class="next-btn danger-training-btn" onclick="startAllTopicMistakeTraining()">Alle Fehler trainieren</button>`
            : ""
        }

        <button class="next-btn" onclick="showAllQuestions()">
          Themen trainieren
        </button>

        <button class="next-btn secondary-btn" onclick="location.reload()">
          Zurück zum Dashboard
        </button>

      </div>

    </section>
  `;
}




function renderExamQuestion() {
  const question = examQuestions[examQuestionIndex];
  const examQuestionArea = document.getElementById("examQuestionArea");

  if (!question || !examQuestionArea) return;

  const savedAnswers = examAnswers[examQuestionIndex] || [];
  const correctCount = question.correct.length;

  examQuestionArea.innerHTML = `
    ${formatQuestionText(question.question)}

    <div class="exam-hint-box">
      <p>Prüfungsmodus: Antworten werden erst am Ende ausgewertet.</p>
      <strong>
        ${
          correctCount === 1
            ? "Es ist 1 Antwort richtig."
            : "Es sind " + correctCount + " Antworten richtig."
        }
      </strong>
    </div>

    <div class="answers">
      ${question.answers.map((answer, index) => `
        <button
          class="answer-btn ${savedAnswers.includes(index) ? "selected" : ""}"
          data-index="${index}"
        >
          ${escapeHtml(answer)}
        </button>
      `).join("")}
    </div>

    <div class="exam-actions">
      <button class="next-btn secondary-btn" id="prevExamBtn">
        Zurück
      </button>

      <button class="next-btn" id="nextExamBtn">
        ${examQuestionIndex === examQuestions.length - 1 ? "Prüfung abgeben" : "Nächste Frage"}
      </button>

      <button class="next-btn danger-warning-btn" id="finishExamNowBtn">
        Prüfung jetzt abgeben
      </button>
    </div>
  `;

  document.querySelectorAll(".answer-btn").forEach(button => {
    button.onclick = () => toggleExamAnswer(button);
  });

  const prevBtn = document.getElementById("prevExamBtn");
  const nextBtn = document.getElementById("nextExamBtn");
  const finishExamNowBtn = document.getElementById("finishExamNowBtn");
  const disablePrev = examFocusQuestionIndexes
    ? examFocusQuestionPosition === 0
    : examQuestionIndex === 0;
  const isLastInFocus =
    examFocusQuestionIndexes &&
    examFocusQuestionPosition >= examFocusQuestionIndexes.length - 1;
  const isLastQuestion = examQuestionIndex === examQuestions.length - 1;
  const nextLabel =
    isLastInFocus || isLastQuestion ? "Prüfung abgeben" : "Nächste Frage";

  if (prevBtn) {
    prevBtn.onclick = previousExamQuestion;
    prevBtn.disabled = disablePrev;
  }

  if (nextBtn) {
    nextBtn.innerText = nextLabel;
    nextBtn.onclick = nextExamQuestion;
  }

  if (finishExamNowBtn) {
    finishExamNowBtn.onclick = () => {
      if (
        Array.isArray(examFocusQuestionIndexes) &&
        examFocusQuestionIndexes.length > 0
      ) {
        finishExamMode();
      } else {
        handleExamSubmitRequest();
      }
    };
  }

  updateExamProgress();
  renderExamNavigation();
}

function toggleExamAnswer(button) {
  const question = examQuestions[examQuestionIndex];

  if (!question) return;

  const maxAnswers = question.correct.length;
  const index = Number(button.dataset.index);

  if (!examAnswers[examQuestionIndex]) {
    examAnswers[examQuestionIndex] = [];
  }

  if (examAnswers[examQuestionIndex].includes(index)) {
    examAnswers[examQuestionIndex] =
      examAnswers[examQuestionIndex].filter(i => i !== index);

    button.classList.remove("selected");
  } else {
    if (examAnswers[examQuestionIndex].length >= maxAnswers) {
      showSmallNotice(
        maxAnswers === 1
          ? "Bei dieser Frage ist nur 1 Antwort möglich."
          : "Bei dieser Frage sind maximal " + maxAnswers + " Antworten möglich."
      );
      return;
    }

    examAnswers[examQuestionIndex].push(index);
    button.classList.add("selected");
  }

  renderExamNavigation();
}

function previousExamQuestion() {
  if (examFocusQuestionIndexes) {
    if (examFocusQuestionPosition > 0) {
      examFocusQuestionPosition--;
      examQuestionIndex = examFocusQuestionIndexes[examFocusQuestionPosition];
      renderExamQuestion();
    }
    return;
  }

  if (examQuestionIndex > 0) {
    examQuestionIndex--;
    renderExamQuestion();
  }
}

function nextExamQuestion() {
  if (examFocusQuestionIndexes) {
    if (examFocusQuestionPosition < examFocusQuestionIndexes.length - 1) {
      examFocusQuestionPosition++;
      examQuestionIndex = examFocusQuestionIndexes[examFocusQuestionPosition];
      renderExamQuestion();
      return;
    }

    examFocusQuestionIndexes = null;
    examFocusQuestionPosition = 0;
    handleExamSubmitRequest();
    return;
  }

  if (examQuestionIndex >= examQuestions.length - 1) {
    handleExamSubmitRequest();
    return;
  }

  examQuestionIndex++;
  renderExamQuestion();
}

function handleExamSubmitRequest() {
  const firstUnansweredIndex = getFirstUnansweredQuestionIndex();

  if (firstUnansweredIndex !== -1) {
    const unansweredCount = getUnansweredQuestionsCount();
    showExamSubmitWarning(firstUnansweredIndex, unansweredCount);
    return;
  }

  finishExamMode();
}

function showExamSubmitWarning(firstUnansweredIndex, unansweredCount) {
  const examQuestionArea = document.getElementById("examQuestionArea");

  if (!examQuestionArea) return;

  let warning = document.getElementById("examWarningBox");

  if (!warning) {
    warning = document.createElement("div");
    warning.id = "examWarningBox";
    warning.className = "exam-warning-box";
    examQuestionArea.prepend(warning);
  }

  warning.innerHTML = `
    <strong>Achtung</strong>

    <p>
      Es gibt noch ${unansweredCount} unbeantwortete Prüfungsfrage(n).
      Sie können offene Fragen nachholen oder die Prüfung trotzdem abgeben.
    </p>

    <p class="warning-small">
      Unbeantwortete Prüfungsfragen werden bei der Auswertung als unbeantwortet gezählt.
    </p>

    <div class="warning-actions">
      <button class="warning-btn primary-warning-btn" onclick="startUnansweredExamFocus()">
        Offene Fragen nachholen
      </button>

      <button class="warning-btn danger-warning-btn" onclick="finishExamMode()">
        Trotzdem abgeben
      </button>
    </div>
  `;

  warning.scrollIntoView({
    behavior: "smooth",
    block: "start"
  });
}

function goToExamQuestion(index) {
  if (index < 0 || index >= examQuestions.length) {
    return;
  }

  examFocusQuestionIndexes = null;
  examFocusQuestionPosition = 0;
  examQuestionIndex = index;
  renderExamQuestion();
}

function updateExamProgress() {
  const percent = Math.round(
    ((examQuestionIndex + 1) / examQuestions.length) * 100
  );

  const examProgressText = document.getElementById("examProgressText");
  const examProgressFill = document.getElementById("examProgressFill");

  if (examProgressText) {
    examProgressText.innerText =
      `Frage ${examQuestionIndex + 1}/${examQuestions.length}`;
  }

  if (examProgressFill) {
    examProgressFill.style.width = percent + "%";
  }
}

function renderExamNavigation() {
  const examNav = document.getElementById("examNav");

  if (!examNav) return;

  examNav.innerHTML = "";

  examQuestions.forEach((question, index) => {
    const button = document.createElement("button");

    button.innerText = index + 1;
    button.className = "exam-nav-btn";

    if (index === examQuestionIndex) {
      button.classList.add("active");
    }

    if (examAnswers[index] && examAnswers[index].length > 0) {
      button.classList.add("answered");
    }

    button.onclick = () => {
      examQuestionIndex = index;
      renderExamQuestion();
    };

    examNav.appendChild(button);
  });
}

function getUnansweredQuestionsCount() {
  let count = 0;

  for (let i = 0; i < examQuestions.length; i++) {
    if (!examAnswers[i] || examAnswers[i].length === 0) {
      count++;
    }
  }

  return count;
}

function getFirstUnansweredQuestionIndex() {
  for (let i = 0; i < examQuestions.length; i++) {
    if (!examAnswers[i] || examAnswers[i].length === 0) {
      return i;
    }
  }

  return -1;
}

function getUnansweredQuestionIndexes() {
  const indexes = [];

  for (let i = 0; i < examQuestions.length; i++) {
    if (!examAnswers[i] || examAnswers[i].length === 0) {
      indexes.push(i);
    }
  }

  return indexes;
}

function startUnansweredExamFocus() {
  const unansweredIndexes = getUnansweredQuestionIndexes();

  if (unansweredIndexes.length === 0) {
    finishExamMode();
    return;
  }

  examFocusQuestionIndexes = unansweredIndexes;
  examFocusQuestionPosition = 0;
  examQuestionIndex = examFocusQuestionIndexes[0];
  renderExamQuestion();
  saveActiveExamSession();
}

function scrollToAnswers() {
  const answers = document.querySelector(".answers");

  if (answers) {
    answers.scrollIntoView({
      behavior: "smooth",
      block: "center"
    });
  }
}

function startExamTimer() {
  clearExamTimer();

  examTimer = setInterval(() => {
    examSecondsLeft--;

    updateExamTimerDisplay();

    if (examSecondsLeft <= 0) {
      clearExamTimer();
      finishExamMode();
    }
  }, 1000);
}

function clearExamTimer() {
  if (examTimer) {
    clearInterval(examTimer);
    examTimer = null;
  }
}

function updateExamTimerDisplay() {
  const timerElement = document.getElementById("examTimer");

  if (!timerElement) return;

  timerElement.innerText = formatSeconds(examSecondsLeft);
}

function finishExamMode() {
  clearExamTimer();

  let correctCount = 0;
  let wrongCount = 0;
  let unansweredCount = 0;

  lastExamMistakes = [];

  examQuestions.forEach((question, index) => {
    const selected = examAnswers[index] || [];

    if (selected.length === 0) {
      unansweredCount++;
      lastExamMistakes.push(question);
      saveTopicMistake(question);
      return;
    }

    markQuestionAsAnswered(question);

    const isCorrect = isExamAnswerCorrect(question, selected);

    saveTopicResult(question.category, isCorrect);

    if (isCorrect) {
      correctCount++;
      removeTopicMistake(question);
    } else {
      wrongCount++;
      lastExamMistakes.push(question);
      saveTopicMistake(question);
    }
  });

  const total = examQuestions.length;
  const percent = total > 0 ? Math.round((correctCount / total) * 100) : 0;
  const passed = percent >= 50;

  const topicBreakdown = buildExamTopicBreakdown();

  saveExamResult({
    total,
    correct: correctCount,
    wrong: wrongCount,
    unanswered: unansweredCount,
    percent,
    passed,
    topicBreakdown,
    date: new Date().toLocaleString("de-DE")
  });

  updateDashboardNumbers();

  const mainContent = document.querySelector(".main-content");

  if (!mainContent) return;

  mainContent.innerHTML = `
    <button class="back-btn" onclick="location.reload()">
      ← Zurück zum Dashboard
    </button>

    <section class="result-wrapper">

      <div class="result-hero ${passed ? "passed" : "failed"}">

        <p class="eyebrow">Prüfungsergebnis</p>

        <h1>${passed ? "Bestanden" : "Nicht bestanden"}</h1>

        <div class="result-percent">
          ${percent}%
        </div>

        <p class="result-message">
          ${
            passed
              ? "Die Prüfungssimulation wurde erfolgreich bestanden."
              : "Die Prüfungssimulation wurde nicht bestanden. Wiederholen Sie gezielt Ihre Schwächen."
          }
        </p>

      </div>

      <div class="result-stats-grid">

        <div class="result-stat-card">
          <span>Gesamtfragen</span>
          <strong>${total}</strong>
        </div>

        <div class="result-stat-card success">
          <span>Richtig</span>
          <strong>${correctCount}</strong>
        </div>

        <div class="result-stat-card danger">
          <span>Falsch</span>
          <strong>${wrongCount}</strong>
        </div>

        <div class="result-stat-card warning">
          <span>Unbeantwortet</span>
          <strong>${unansweredCount}</strong>
        </div>

      </div>

      ${buildExamFocusRecommendationHtml(topicBreakdown)}

      ${buildExamTopicBreakdownHtml(topicBreakdown)}

      <div class="result-actions">

        <button class="next-btn" onclick="showExamReview()">
          Fehler ansehen
        </button>

        <button class="next-btn danger-training-btn" onclick="startMistakeTraining()">
          Fehlertraining starten
        </button>

        <button class="next-btn" onclick="startExamMode()">
          Prüfung wiederholen
        </button>

        <button class="next-btn secondary-btn" onclick="location.reload()">
          Zurück zum Dashboard
        </button>

      </div>

    </section>
  `;
}

/* =========================
   PRÜFUNGSMODUS
========================= */

const EXAM_SHORT_QUESTION_LIMIT_V20 = EXAM_QUESTION_LIMIT;
const EXAM_FULL_QUESTION_LIMIT_V20 = 82;

const EXAM_CORE_QUESTION_IDS_V244 = [
  "roso_001", "roso_002", "roso_003", "roso_005", "v23_roso_006", "v23_roso_007", "v23_roso_008",
  "gewo_002", "gewo_004", "v23_gewo_006", "v23_gewo_007", "v23_gewo_008",
  "ds_001", "ds_002", "ds_003", "ds_004", "ds_005",
  "bgb_001", "bgb_002", "bgb_003", "bgb_004", "bgb_005", "bgb_006", "bgb_007", "bgb_008", "bgb_009", "bgb_010", "bgb_011", "bgb_012", "bgb_013",
  "straf_001", "straf_002", "straf_003", "straf_004", "straf_005", "straf_006", "straf_007", "straf_008", "straf_009", "straf_010", "straf_011", "straf_012", "straf_013",
  "uvv_001", "uvv_002", "uvv_003", "uvv_004", "uvv_005", "uvv_006", "uvv_007", "uvv_008",
  "waffen_001", "waffen_002", "waffen_003", "waffen_004", "waffen_005",
  "umgang_001", "umgang_002", "umgang_003", "umgang_004", "umgang_005", "umgang_006", "umgang_007", "umgang_008", "umgang_009", "umgang_010", "umgang_011", "umgang_012", "umgang_013", "umgang_014", "umgang_015", "umgang_016", "umgang_017", "umgang_018", "umgang_019",
  "technik_001", "technik_002", "technik_003", "technik_004", "technik_005", "technik_006", "technik_007"
];

let currentExamLimit = EXAM_SHORT_QUESTION_LIMIT_V20;
let currentExamTitle = "§34a Kurzprüfung";
let currentExamType = "short";

function showExamStartPage() {
  currentMode = "exam-start";
  clearExamTimer();

  const mainContent = document.querySelector(".main-content");

  if (!mainContent) return;

  if (!allQuestions || allQuestions.length === 0) {
    showSmallNotice("Fragenbank wurde noch nicht geladen.");
    return;
  }

  const availableQuestions = allQuestions.length;
  const shortSimulationCount = Math.min(EXAM_SHORT_QUESTION_LIMIT_V20, availableQuestions);
  const fullSimulationCount = Math.min(EXAM_FULL_QUESTION_LIMIT_V20, availableQuestions);

  mainContent.innerHTML = `
    <button class="back-btn" onclick="location.reload()">
      ← Zurück zum Dashboard
    </button>

    <section class="review-wrapper">

      <div class="review-header">
        <p class="eyebrow">Prüfungsmodus</p>
        <h1>Prüfung auswählen</h1>
        <p>
          Wählen Sie zwischen einer kurzen Trainingsprüfung und einer vorbereiteten Vollsimulation.
        </p>
      </div>

      <div class="hero-grid">

        <div class="hero-card gold" onclick="startExamMode(${EXAM_SHORT_QUESTION_LIMIT_V20}, '§34a Kurzprüfung', 'short')" style="cursor:pointer;">
          <div class="card-icon">⏱️</div>
          <h2>Kurzprüfung</h2>
          <p>${shortSimulationCount} Fragen · schnelle Kontrolle</p>
        </div>

        <div class="hero-card blue" onclick="startExamMode(${EXAM_FULL_QUESTION_LIMIT_V20}, '§34a Vollsimulation', 'full')" style="cursor:pointer;">
          <div class="card-icon">📝</div>
          <h2>Vollsimulation</h2>
          <p>${fullSimulationCount} Fragen · vorbereitet auf 82 Fragen</p>
        </div>

      </div>

      <div class="last-exam-box">
        <span>Hinweis</span>
        <strong>Aktuell verfügbare Fragen: ${availableQuestions}</strong>
        <p>
          Die echte 82-Fragen-Struktur ist vorbereitet. Solange weniger als 82 Fragen vorhanden sind,
          nutzt die App automatisch alle verfügbaren Fragen.
        </p>
      </div>

    </section>
  `;
}

function examHasTimer() {
  return currentExamType === "full";
}

function startExamMode(questionLimit, examTitle, examType) {
  if (arguments.length === 0) {
    showExamStartPage();
    return;
  }

  if (allQuestions.length === 0) {
    alert("Noch keine Fragen geladen.");
    return;
  }

  clearActiveSession();
  renderDashboardResumeExamCard();

  currentMode = "exam";

  currentExamLimit = Number(questionLimit) || EXAM_SHORT_QUESTION_LIMIT_V20;
  currentExamTitle = examTitle || "§34a Kurzprüfung";
  currentExamType = examType || "short";

  if (currentExamType === "full") {
    const questionById = new Map(
      allQuestions.map(question => [String(question.id), question])
    );

    const missingIds = [];
    const coreQuestions = [];

    EXAM_CORE_QUESTION_IDS_V244.forEach(coreId => {
      const question = questionById.get(coreId);

      if (!question) {
        missingIds.push(coreId);
        return;
      }

      coreQuestions.push(question);
    });

    if (missingIds.length > 0) {
      console.error(
        "Vollsimulation: Core-Fragen fehlen in der Fragenbank:",
        missingIds
      );
      alert(
        "Die Vollsimulation kann nicht gestartet werden. Fehlende Core-Fragen: " +
          missingIds.join(", ")
      );
      return;
    }

    examQuestions = shuffleArray(coreQuestions).map(question =>
      createShuffledQuestion(question)
    );
    currentExamLimit = examQuestions.length;
  } else {
    examQuestions = shuffleArray([...allQuestions])
      .slice(0, Math.min(currentExamLimit, allQuestions.length))
      .map(question => createShuffledQuestion(question));
  }

  examQuestionIndex = 0;
  examAnswers = {};
  examSecondsLeft = EXAM_DURATION_SECONDS;
  lastExamMistakes = [];

  showExamView();

  if (examHasTimer()) {
    startExamTimer();
  } else {
    clearExamTimer();
  }

  renderExamQuestion();
  saveActiveExamSession();
}

function repeatCurrentExamMode() {
  startExamMode(currentExamLimit, currentExamTitle, currentExamType);
}

function showExamView(preserveFocusState) {
  const mainContent = document.querySelector(".main-content");

  if (!mainContent) return;

  if (!preserveFocusState) {
    examFocusQuestionIndexes = null;
    examFocusQuestionPosition = 0;
  }

  mainContent.innerHTML = `
    <button class="back-btn" onclick="pauseExam()">
      ← Prüfung pausieren
    </button>

    <div class="learning-header">
      <div>
        <p class="eyebrow">Prüfungsmodus</p>
        <h1>${escapeHtml(currentExamTitle)}</h1>
      </div>

      ${
        examHasTimer()
          ? `
            <div class="score-box exam-timer-box">
              <span>Restzeit</span>
              <strong id="examTimer">${formatSeconds(examSecondsLeft)}</strong>
            </div>
          `
          : ""
      }
    </div>

    <div class="progress-wrapper">
      <div class="progress-info">
        <span id="examProgressText">Frage 1/${examQuestions.length}</span>

        <span>
          ${
            examHasTimer()
              ? examQuestions.length + " Fragen · 120 Minuten · Auswertung erst am Ende"
              : examQuestions.length + " Fragen · Auswertung erst am Ende"
          }
        </span>
      </div>

      <div class="progress-bar">
        <div class="progress-fill" id="examProgressFill"></div>
      </div>
    </div>

    <section class="question-card" id="examQuestionArea"></section>

    <div class="exam-nav" id="examNav"></div>

    <div class="exam-actions" style="margin-top:16px;">
      <button class="next-btn secondary-btn" onclick="pauseExam()">
        Prüfung pausieren
      </button>
    </div>
  `;
}

function renderExamQuestion() {
  const question = examQuestions[examQuestionIndex];
  const examQuestionArea = document.getElementById("examQuestionArea");

  if (!question || !examQuestionArea) return;

  const savedAnswers = examAnswers[examQuestionIndex] || [];
  const correctCount = question.correct.length;

  examQuestionArea.innerHTML = `
    ${formatQuestionText(question.question)}

    <div class="exam-hint-box">
      <p>Prüfungsmodus: Antworten werden erst am Ende ausgewertet.</p>
      <strong>
        ${
          correctCount === 1
            ? "Es ist 1 Antwort richtig."
            : "Es sind " + correctCount + " Antworten richtig."
        }
      </strong>
    </div>

    <div class="answers">
      ${question.answers.map((answer, index) => `
        <button
          class="answer-btn ${savedAnswers.includes(index) ? "selected" : ""}"
          data-index="${index}"
        >
          ${escapeHtml(answer)}
        </button>
      `).join("")}
    </div>

    <div class="exam-actions">
      <button class="next-btn secondary-btn" id="prevExamBtn">
        Zurück
      </button>

      <button class="next-btn" id="nextExamBtn">
        ${examQuestionIndex === examQuestions.length - 1 ? "Prüfung abgeben" : "Nächste Frage"}
      </button>

      <button class="next-btn danger-warning-btn" id="finishExamNowBtn">
        Prüfung jetzt abgeben
      </button>

      <button class="next-btn secondary-btn" onclick="pauseExam()">
        Prüfung pausieren
      </button>
    </div>
  `;

  document.querySelectorAll(".answer-btn").forEach(button => {
    button.onclick = () => toggleExamAnswer(button);
  });

  const prevBtn = document.getElementById("prevExamBtn");
  const nextBtn = document.getElementById("nextExamBtn");
  const finishExamNowBtn = document.getElementById("finishExamNowBtn");
  const disablePrev = examFocusQuestionIndexes
    ? examFocusQuestionPosition === 0
    : examQuestionIndex === 0;
  const isLastInFocus =
    examFocusQuestionIndexes &&
    examFocusQuestionPosition >= examFocusQuestionIndexes.length - 1;
  const isLastQuestion = examQuestionIndex === examQuestions.length - 1;
  const nextLabel =
    isLastInFocus || isLastQuestion ? "Prüfung abgeben" : "Nächste Frage";

  if (prevBtn) {
    prevBtn.onclick = previousExamQuestion;
    prevBtn.disabled = disablePrev;
  }

  if (nextBtn) {
    nextBtn.innerText = nextLabel;
    nextBtn.onclick = nextExamQuestion;
  }

  if (finishExamNowBtn) {
    finishExamNowBtn.onclick = () => {
      if (
        Array.isArray(examFocusQuestionIndexes) &&
        examFocusQuestionIndexes.length > 0
      ) {
        finishExamMode();
      } else {
        handleExamSubmitRequest();
      }
    };
  }

  updateExamProgress();
  renderExamNavigation();
  saveActiveExamSession();
}

function toggleExamAnswer(button) {
  const question = examQuestions[examQuestionIndex];

  if (!question) return;

  const maxAnswers = question.correct.length;
  const index = Number(button.dataset.index);

  if (!examAnswers[examQuestionIndex]) {
    examAnswers[examQuestionIndex] = [];
  }

  if (examAnswers[examQuestionIndex].includes(index)) {
    examAnswers[examQuestionIndex] =
      examAnswers[examQuestionIndex].filter(i => i !== index);

    button.classList.remove("selected");
  } else {
    if (examAnswers[examQuestionIndex].length >= maxAnswers) {
      showSmallNotice(
        maxAnswers === 1
          ? "Bei dieser Frage ist nur 1 Antwort möglich."
          : "Bei dieser Frage sind maximal " + maxAnswers + " Antworten möglich."
      );
      return;
    }

    examAnswers[examQuestionIndex].push(index);
    button.classList.add("selected");
  }

  renderExamNavigation();
  saveActiveExamSession();
}

function previousExamQuestion() {
  if (examFocusQuestionIndexes) {
    if (examFocusQuestionPosition > 0) {
      examFocusQuestionPosition--;
      examQuestionIndex = examFocusQuestionIndexes[examFocusQuestionPosition];
      renderExamQuestion();
      saveActiveExamSession();
    }
    return;
  }

  if (examQuestionIndex > 0) {
    examQuestionIndex--;
    renderExamQuestion();
    saveActiveExamSession();
  }
}

function nextExamQuestion() {
  if (examFocusQuestionIndexes) {
    if (examFocusQuestionPosition < examFocusQuestionIndexes.length - 1) {
      examFocusQuestionPosition++;
      examQuestionIndex = examFocusQuestionIndexes[examFocusQuestionPosition];
      renderExamQuestion();
      saveActiveExamSession();
      return;
    }

    examFocusQuestionIndexes = null;
    examFocusQuestionPosition = 0;
    handleExamSubmitRequest();
    return;
  }

  if (examQuestionIndex >= examQuestions.length - 1) {
    handleExamSubmitRequest();
    return;
  }

  examQuestionIndex++;
  renderExamQuestion();
  saveActiveExamSession();
}

function handleExamSubmitRequest() {
  const firstUnansweredIndex = getFirstUnansweredQuestionIndex();

  if (firstUnansweredIndex !== -1) {
    const unansweredCount = getUnansweredQuestionsCount();
    showExamSubmitWarning(firstUnansweredIndex, unansweredCount);
    return;
  }

  finishExamMode();
}

function showExamSubmitWarning(firstUnansweredIndex, unansweredCount) {
  const examQuestionArea = document.getElementById("examQuestionArea");

  if (!examQuestionArea) return;

  let warning = document.getElementById("examWarningBox");

  if (!warning) {
    warning = document.createElement("div");
    warning.id = "examWarningBox";
    warning.className = "exam-warning-box";
    examQuestionArea.prepend(warning);
  }

  warning.innerHTML = `
    <strong>Achtung</strong>

    <p>
      Es gibt noch ${unansweredCount} unbeantwortete Prüfungsfrage(n).
      Sie können offene Fragen nachholen oder die Prüfung trotzdem abgeben.
    </p>

    <p class="warning-small">
      Unbeantwortete Prüfungsfragen werden bei der Auswertung als unbeantwortet gezählt.
    </p>

    <div class="warning-actions">
      <button class="warning-btn primary-warning-btn" onclick="startUnansweredExamFocus()">
        Offene Fragen nachholen
      </button>

      <button class="warning-btn danger-warning-btn" onclick="finishExamMode()">
        Trotzdem abgeben
      </button>
    </div>
  `;

  warning.scrollIntoView({
    behavior: "smooth",
    block: "start"
  });
}

function goToExamQuestion(index) {
  if (index < 0 || index >= examQuestions.length) {
    return;
  }

  examFocusQuestionIndexes = null;
  examFocusQuestionPosition = 0;
  examQuestionIndex = index;
  renderExamQuestion();
  saveActiveExamSession();
}

function updateExamProgress() {
  const percent = Math.round(
    ((examQuestionIndex + 1) / examQuestions.length) * 100
  );

  const examProgressText = document.getElementById("examProgressText");
  const examProgressFill = document.getElementById("examProgressFill");

  if (examProgressText) {
    examProgressText.innerText =
      `Frage ${examQuestionIndex + 1}/${examQuestions.length}`;
  }

  if (examProgressFill) {
    examProgressFill.style.width = percent + "%";
  }
}

function renderExamNavigation() {
  const examNav = document.getElementById("examNav");

  if (!examNav) return;

  examNav.innerHTML = "";

  examQuestions.forEach((question, index) => {
    const button = document.createElement("button");

    button.innerText = index + 1;
    button.className = "exam-nav-btn";

    if (index === examQuestionIndex) {
      button.classList.add("active");
    }

    if (examAnswers[index] && examAnswers[index].length > 0) {
      button.classList.add("answered");
    }

    button.onclick = () => {
      examQuestionIndex = index;
      renderExamQuestion();
      saveActiveExamSession();
    };

    examNav.appendChild(button);
  });
}

function getUnansweredQuestionsCount() {
  let count = 0;

  for (let i = 0; i < examQuestions.length; i++) {
    if (!examAnswers[i] || examAnswers[i].length === 0) {
      count++;
    }
  }

  return count;
}

function getFirstUnansweredQuestionIndex() {
  for (let i = 0; i < examQuestions.length; i++) {
    if (!examAnswers[i] || examAnswers[i].length === 0) {
      return i;
    }
  }

  return -1;
}

function scrollToAnswers() {
  const answers = document.querySelector(".answers");

  if (answers) {
    answers.scrollIntoView({
      behavior: "smooth",
      block: "center"
    });
  }
}

function startExamTimer() {
  clearExamTimer();

  examTimer = setInterval(() => {
    examSecondsLeft--;

    updateExamTimerDisplay();
    scheduleExamSessionTimerSave();

    if (examSecondsLeft <= 0) {
      clearExamTimer();
      finishExamMode();
    }
  }, 1000);
}

function clearExamTimer() {
  if (examTimer) {
    clearInterval(examTimer);
    examTimer = null;
  }
}

function updateExamTimerDisplay() {
  const timerElement = document.getElementById("examTimer");

  if (!timerElement) return;

  timerElement.innerText = formatSeconds(examSecondsLeft);
}

function finishExamMode() {
  clearExamTimer();
  clearActiveSession();

  let correctCount = 0;
  let wrongCount = 0;
  let unansweredCount = 0;

  lastExamMistakes = [];

  examQuestions.forEach((question, index) => {
    const selected = examAnswers[index] || [];

    if (selected.length === 0) {
      unansweredCount++;
      lastExamMistakes.push(question);
      saveTopicMistake(question);
      return;
    }

    markQuestionAsAnswered(question);

    const isCorrect = isExamAnswerCorrect(question, selected);

    saveTopicResult(question.category, isCorrect);

    if (isCorrect) {
      correctCount++;
      removeTopicMistake(question);
    } else {
      wrongCount++;
      lastExamMistakes.push(question);
      saveTopicMistake(question);
    }
  });

  const total = examQuestions.length;

  const questionPercent =
    total > 0
      ? Math.round((correctCount / total) * 100)
      : 0;

  const maxPoints = getExamMaxPoints();
  const reachedPoints = getExamReachedPoints();
  const passPoints = getExamPassPoints(maxPoints);

  const percent =
    maxPoints > 0
      ? Math.round((reachedPoints / maxPoints) * 100)
      : 0;

  const passed = reachedPoints >= passPoints;

  const topicBreakdown = buildExamTopicBreakdown();

  saveExamResult({
    total,
    correct: correctCount,
    wrong: wrongCount,
    unanswered: unansweredCount,

    percent,
    questionPercent,

    points: {
      reached: reachedPoints,
      max: maxPoints,
      pass: passPoints,
      passPercent: EXAM_PASS_PERCENT
    },

    passed,
    topicBreakdown,
    examType: currentExamType,
    examTitle: currentExamTitle,
    examLimit: currentExamLimit,
    date: new Date().toLocaleString("de-DE")
  });

  updateDashboardNumbers();

  const mainContent = document.querySelector(".main-content");

  if (!mainContent) return;

  mainContent.innerHTML = `
    <button class="back-btn" onclick="location.reload()">
      ← Zurück zum Dashboard
    </button>

    <section class="result-wrapper">

      <div class="result-hero ${passed ? "passed" : "failed"}">

        <p class="eyebrow"${passed ? "" : ' style="color:#F8FAFC;"'}>Prüfungsergebnis · ${escapeHtml(currentExamTitle)}</p>

        <h1>${passed ? "Bestanden" : "Nicht bestanden"}</h1>

        <div class="result-percent">
          ${percent}%
        </div>

        <p class="result-message">
          ${
            passed
              ? "Die Prüfungssimulation wurde erfolgreich bestanden. Die Punktebewertung wurde berücksichtigt."
              : "Die Prüfungssimulation wurde nicht bestanden. Wiederholen Sie gezielt Ihre Schwächen und achten Sie auf die Punktebewertung."
          }
        </p>

      </div>

      <div class="result-stats-grid">

        <div class="result-stat-card">
          <span>Gesamtfragen</span>
          <strong>${total}</strong>
        </div>

        <div class="result-stat-card success">
          <span>Richtig</span>
          <strong>${correctCount}</strong>
        </div>

        <div class="result-stat-card danger">
          <span>Falsch</span>
          <strong>${wrongCount}</strong>
        </div>

        <div class="result-stat-card warning">
          <span>Unbeantwortet</span>
          <strong>${unansweredCount}</strong>
        </div>

        <div class="result-stat-card gold-stat">
          <span>Punkte</span>
          <strong>${reachedPoints}/${maxPoints}</strong>
        </div>

        <div class="result-stat-card">
          <span>Bestehensgrenze</span>
          <strong>${passPoints} Punkte</strong>
        </div>

      </div>

      ${buildExamFocusRecommendationHtml(topicBreakdown)}

      ${buildExamTopicBreakdownHtml(topicBreakdown)}

      <div class="result-actions">

        <button class="next-btn" onclick="showExamReview()">
          Fehler ansehen
        </button>

        <button class="next-btn danger-training-btn" onclick="startMistakeTraining()">
          Fehlertraining starten
        </button>

        <button class="next-btn" onclick="repeatCurrentExamMode()">
          Prüfung wiederholen
        </button>

        <button class="next-btn secondary-btn" onclick="location.reload()">
          Zurück zum Dashboard
        </button>

      </div>

    </section>
  `;
}

function isExamAnswerCorrect(question, selectedAnswersForQuestion) {
  if (!question || !Array.isArray(selectedAnswersForQuestion)) {
    return false;
  }

  const selectedSorted = [...selectedAnswersForQuestion]
    .sort((a, b) => a - b)
    .join(",");

  const correctSorted = [...question.correct]
    .sort((a, b) => a - b)
    .join(",");

  return selectedSorted === correctSorted;
}

function getExamQuestionReachedPoints(question, selectedAnswersForQuestion) {
  if (!question || !Array.isArray(selectedAnswersForQuestion) || selectedAnswersForQuestion.length === 0) {
    return 0;
  }

  const correctIndexes = new Set(question.correct);
  const selectedUnique = [...new Set(selectedAnswersForQuestion)];
  let reached = 0;

  selectedUnique.forEach(index => {
    if (correctIndexes.has(index)) {
      reached += 1;
    }
  });

  return Math.min(reached, getQuestionPoints(question));
}

function getQuestionPoints(question) {
  if (!question) {
    return DEFAULT_QUESTION_POINTS;
  }

  const rawPoints =
    question.points ??
    question.punkte ??
    question.score ??
    DEFAULT_QUESTION_POINTS;

  const points = Number(rawPoints);

  if (!Number.isFinite(points) || points <= 0) {
    return DEFAULT_QUESTION_POINTS;
  }

  return points;
}

function getExamMaxPoints() {
  return examQuestions.reduce((sum, question) => {
    return sum + getQuestionPoints(question);
  }, 0);
}

function getExamReachedPoints() {
  let reachedPoints = 0;

  examQuestions.forEach((question, index) => {
    const selected = examAnswers[index] || [];
    reachedPoints += getExamQuestionReachedPoints(question, selected);
  });

  return reachedPoints;
}

function getExamPassPoints(maxPoints) {
  if (!Number.isFinite(maxPoints) || maxPoints <= 0) {
    return 0;
  }

  return Math.ceil((maxPoints * EXAM_PASS_PERCENT) / 100);
}

function buildExamTopicBreakdown() {
  const breakdown = {};

  categories.forEach(categoryName => {
    breakdown[categoryName] = {
      total: 0,
      correct: 0,
      wrong: 0,
      unanswered: 0,
      percent: 0
    };
  });

  examQuestions.forEach((question, index) => {
    const categoryName = normalizeCategoryName(question.category || "Ohne Kategorie");

    if (!breakdown[categoryName]) {
      breakdown[categoryName] = {
        total: 0,
        correct: 0,
        wrong: 0,
        unanswered: 0,
        percent: 0
      };
    }

    const selected = examAnswers[index] || [];

    breakdown[categoryName].total++;

    if (selected.length === 0) {
      breakdown[categoryName].unanswered++;
      return;
    }

    if (isExamAnswerCorrect(question, selected)) {
      breakdown[categoryName].correct++;
    } else {
      breakdown[categoryName].wrong++;
    }
  });

  Object.keys(breakdown).forEach(categoryName => {
    const stats = breakdown[categoryName];

    stats.percent =
      stats.total === 0
        ? 0
        : Math.round((stats.correct / stats.total) * 100);
  });

  return breakdown;
}

function buildExamFocusRecommendationHtml(topicBreakdown) {
  let focusCategory = null;
  let highestProblemCount = 0;
  let lowestPercent = 101;

  Object.keys(topicBreakdown).forEach(categoryName => {
    const stats = topicBreakdown[categoryName];

    if (!stats || stats.total === 0) {
      return;
    }

    const problemCount = stats.wrong + stats.unanswered;

    if (
      problemCount > highestProblemCount ||
      (problemCount === highestProblemCount && stats.percent < lowestPercent)
    ) {
      highestProblemCount = problemCount;
      lowestPercent = stats.percent;
      focusCategory = categoryName;
    }
  });

  if (!focusCategory || highestProblemCount === 0) {
    return `
      <div class="last-exam-box">
        <span>Empfehlung</span>
        <strong>Sehr stark</strong>
        <p>
          In dieser Prüfung wurden keine fachlichen Schwächen erkannt.
          Wiederholen Sie trotzdem regelmäßig alle Themenbereiche.
        </p>
      </div>
    `;
  }

  const focusStats = topicBreakdown[focusCategory];

  return `
    <div class="last-exam-box">
      <span>Empfehlung</span>
      <strong>${escapeHtml(focusCategory)}</strong>
      <p>
        Dieses Thema hatte in dieser Prüfung die meisten Probleme:
        ${focusStats.wrong} falsch · ${focusStats.unanswered} unbeantwortet · ${focusStats.percent}% Quote.
      </p>

      <button class="next-btn danger-training-btn" onclick='openCategory(${JSON.stringify(focusCategory)})'>
        Thema gezielt trainieren
      </button>
    </div>
  `;
}

function buildExamTopicBreakdownHtml(topicBreakdown) {
  const rows = categories
    .filter(categoryName => {
      return topicBreakdown[categoryName] && topicBreakdown[categoryName].total > 0;
    })
    .map(categoryName => {
      const stats = topicBreakdown[categoryName];
      const problemCount = stats.wrong + stats.unanswered;
      const answeredCount = stats.total - stats.unanswered;
      const coveragePercent =
        stats.total > 0
          ? Math.round((answeredCount / stats.total) * 100)
          : 0;

      let statusClass = "topic-neutral";
      let statusText = "Nicht geprüft";

      if (answeredCount === 0) {
        statusClass = "topic-neutral";
        statusText = "Nicht geprüft";
      } else if (coveragePercent < 50) {
        statusClass = "topic-neutral";
        statusText = "Teilweise offen";
      } else if (problemCount === 0 && stats.total > 0) {
        statusClass = "topic-strong";
        statusText = "Sicher";
      } else if (stats.percent >= 70) {
        statusClass = "topic-medium";
        statusText = "Fast sicher";
      } else if (stats.percent >= 50) {
        statusClass = "topic-medium";
        statusText = "Nacharbeiten";
      } else {
        statusClass = "topic-weak";
        statusText = "Schwach";
      }

      const actionHtml = problemCount > 0
        ? `<button class="next-btn topic-analysis-btn danger-training-btn" onclick='openCategory(${JSON.stringify(categoryName)})'>Thema trainieren</button>`
        : `<button class="next-btn topic-analysis-btn" disabled>Sicher</button>`;

      return `
        <article class="topic-analysis-card">

          <div class="topic-analysis-main">
            <div class="topic-analysis-title">
              <span>Thema</span>
              <strong>${categoryIcons[categoryName] || "📘"} ${escapeHtml(categoryName)}</strong>
            </div>

            <div class="topic-analysis-action">
              ${actionHtml}
            </div>
          </div>

          <div class="topic-analysis-metrics">
            <div class="topic-analysis-metric">
              <span>Fragen</span>
              <strong>${stats.total}</strong>
            </div>

            <div class="topic-analysis-metric">
              <span>Richtig</span>
              <strong>${stats.correct}</strong>
            </div>

            <div class="topic-analysis-metric">
              <span>Falsch</span>
              <strong>${stats.wrong}</strong>
            </div>

            <div class="topic-analysis-metric">
              <span>Offen</span>
              <strong>${stats.unanswered}</strong>
            </div>

            <div class="topic-analysis-metric">
              <span>Quote</span>
              <strong>${stats.percent}%</strong>
            </div>

            <div class="topic-analysis-metric">
              <span>Status</span>
              <strong class="${statusClass}">${statusText}</strong>
            </div>
          </div>

        </article>
      `;
    })
    .join("");

  return `
    <div class="topic-stats-section topic-analysis-section">

      <div class="section-head">
        <h2>Prüfungsanalyse nach Themen</h2>
        <p>
          Hier sehen Sie, welche Themen in dieser Prüfung stark waren und welche gezielt wiederholt werden sollten.
        </p>
      </div>

      <div class="topic-analysis-list">
        ${rows}
      </div>

    </div>
  `;
}

function showExamReview() {
  const mainContent = document.querySelector(".main-content");

  if (!mainContent) return;

  let reviewItems = "";

  examQuestions.forEach((question, index) => {
    const selected = examAnswers[index] || [];
    const correct = question.correct;

    const selectedSorted = [...selected].sort((a, b) => a - b).join(",");
    const correctSorted = [...correct].sort((a, b) => a - b).join(",");

    const isUnanswered = selected.length === 0;
    const isCorrect = selectedSorted === correctSorted;

    if (isCorrect) return;

    const selectedText = isUnanswered
      ? "Keine Antwort ausgewählt"
      : selected.map(i => question.answers[i]).join(", ");

    const correctText = correct
      .map(i => question.answers[i])
      .join(", ");

    reviewItems += `
      <div class="review-card ${isUnanswered ? "unanswered" : "wrong"}">

        <div class="review-topline">
          <span>Frage ${index + 1}</span>
          <strong>${isUnanswered ? "Unbeantwortet" : "Falsch beantwortet"}</strong>
        </div>

        ${formatQuestionText(question.question)}

        <div class="review-answer-box wrong-answer">
          <span>Ihre Antwort:</span>
          <p>${escapeHtml(selectedText)}</p>
        </div>

        <div class="review-answer-box correct-answer">
          <span>Richtige Antwort:</span>
          <p>${escapeHtml(correctText)}</p>
        </div>

        <div class="review-explanation">
          <span>Erklärung:</span>
          <p>${escapeHtml(question.explanation || "")}</p>
        </div>

      </div>
    `;
  });

  if (reviewItems === "") {
    reviewItems = `
      <div class="review-card">
        <h2>Sehr gut</h2>
        <p>Alle Fragen wurden richtig beantwortet. Es gibt keine Fehler zur Nacharbeit.</p>
      </div>
    `;
  }

  mainContent.innerHTML = `
    <button class="back-btn" onclick="location.reload()">
      ← Zurück zum Dashboard
    </button>

    <section class="review-wrapper">

      <div class="review-header">
        <p class="eyebrow">Fehleranalyse</p>
        <h1>Prüfung nacharbeiten</h1>
        <p>
          Hier sehen Sie alle falschen und unbeantworteten Fragen mit richtiger Lösung und Erklärung.
        </p>
      </div>

      <div class="review-list">
        ${reviewItems}
      </div>

      <div class="result-actions">
        <button class="next-btn danger-training-btn" onclick="showMistakeOverview()">
          Fehlertraining
        </button>

        <button class="next-btn" onclick="repeatCurrentExamMode()">
          Prüfung wiederholen
        </button>

        <button class="next-btn secondary-btn" onclick="location.reload()">
          Zurück zum Dashboard
        </button>
      </div>

    </section>
  `;
}

function startMistakeTraining() {
  if (!lastExamMistakes || lastExamMistakes.length === 0) {
    showSmallNotice("Keine Fehler aus der letzten Prüfung vorhanden.");
    return;
  }

  startLearningSession(
    lastExamMistakes,
    "Fehlertraining aus der Prüfung",
    "last-exam-mistakes"
  );
}


/* =========================
   STATISTIK
========================= */

function loadTopicStats() {
  const saved = readStorage(STORAGE_KEYS.topicStats, {});
  topicStats = {};

  Object.keys(saved).forEach(categoryName => {
    const normalizedCategory = normalizeCategoryName(categoryName);
    const stats = saved[categoryName] || {};

    if (!topicStats[normalizedCategory]) {
      topicStats[normalizedCategory] = {
        answered: 0,
        correct: 0,
        wrong: 0
      };
    }

    topicStats[normalizedCategory].answered += Number(stats.answered || 0);
    topicStats[normalizedCategory].correct += Number(stats.correct || 0);
    topicStats[normalizedCategory].wrong += Number(stats.wrong || 0);
  });
}

function saveTopicStats() {
  writeStorage(STORAGE_KEYS.topicStats, topicStats);
}

function saveTopicResult(categoryName, isCorrect) {
  const category = normalizeCategoryName(categoryName);

  if (!topicStats[category]) {
    topicStats[category] = {
      answered: 0,
      correct: 0,
      wrong: 0
    };
  }

  topicStats[category].answered++;

  if (isCorrect) {
    topicStats[category].correct++;
  } else {
    topicStats[category].wrong++;
  }

  saveTopicStats();
}

function loadExamHistory() {
  examHistory = readStorage(STORAGE_KEYS.examHistory, []);
}

function saveExamResult(result) {
  examHistory.push(result);
  writeStorage(STORAGE_KEYS.examHistory, examHistory);
}

function showStatsPage() {
  currentMode = "statistics";

  loadAllLocalData();

  const mainContent = document.querySelector(".main-content");

  if (!mainContent) return;

  const totalExams = examHistory.length;
  const passedExams = examHistory.filter(exam => exam.passed).length;
  const failedExams = totalExams - passedExams;

  const averagePercent =
    totalExams === 0
      ? 0
      : Math.round(
          examHistory.reduce((sum, exam) => sum + exam.percent, 0) / totalExams
        );

  const bestPercent =
    totalExams === 0
      ? 0
      : Math.max(...examHistory.map(exam => exam.percent));

  const lastExam =
    totalExams === 0
      ? null
      : examHistory[examHistory.length - 1];

  const historyRows =
    totalExams === 0
      ? `<div class="empty-history">Noch keine Prüfungen gespeichert.</div>`
      : examHistory
          .slice()
          .reverse()
          .map((exam, index) => `
            <div class="history-row">

              <div>
                <span>Prüfung ${totalExams - index}</span>
                <strong>${escapeHtml(exam.date)}</strong>
              </div>

              <div>
                <span>Ergebnis</span>
                <strong>${exam.percent}%</strong>
              </div>

              <div>
                <span>Status</span>
                <strong class="${exam.passed ? "status-passed" : "status-failed"}">
                  ${exam.passed ? "Bestanden" : "Nicht bestanden"}
                </strong>
              </div>

              <div>
                <span>Details</span>
                <strong>
                  ${exam.correct} richtig · ${exam.wrong} falsch · ${exam.unanswered} offen
                </strong>
              </div>

            </div>
          `)
          .join("");

  mainContent.innerHTML = `
    <button class="back-btn" onclick="location.reload()">
      ← Zurück zum Dashboard
    </button>

    <section class="result-wrapper">

      <div class="review-header">
        <p class="eyebrow">Gesamtstatistik</p>
        <h1>Ihre Prüfungsentwicklung</h1>
        <p>
          Hier sehen Sie Prüfungssimulationen, Fehler, offene Fragen und Fortschritt.
        </p>
      </div>

      <div class="stats-grid">

        <div class="stats-card">
          <span>Prüfungen gesamt</span>
          <strong>${totalExams}</strong>
        </div>

        <div class="stats-card success">
          <span>Bestanden</span>
          <strong>${passedExams}</strong>
        </div>

        <div class="stats-card danger">
          <span>Nicht bestanden</span>
          <strong>${failedExams}</strong>
        </div>

        <div class="stats-card">
          <span>Durchschnitt</span>
          <strong>${averagePercent}%</strong>
        </div>

        <div class="stats-card gold-stat">
          <span>Bestes Ergebnis</span>
          <strong>${bestPercent}%</strong>
        </div>

        <div class="stats-card">
          <span>Offene Fragen</span>
          <strong>${getOpenQuestionsCount()}</strong>
        </div>

        <div class="stats-card danger">
          <span>Gespeicherte Fehler</span>
          <strong>${getTotalTopicMistakeCount()}</strong>
        </div>

      </div>

      <div class="last-exam-box">

        <span>Letzte Prüfung</span>

        <strong>
          ${
            lastExam
              ? lastExam.percent + "% · " + (lastExam.passed ? "bestanden" : "nicht bestanden")
              : "Noch keine Prüfung vorhanden"
          }
        </strong>

        <p>
          ${
            lastExam
              ? escapeHtml(lastExam.date) + " · " +
                lastExam.correct + " richtig · " +
                lastExam.wrong + " falsch · " +
                lastExam.unanswered + " unbeantwortet"
              : "Starten Sie eine Prüfung, damit hier Daten erscheinen."
          }
        </p>

      </div>

      ${buildTopicStatsHtml()}

      <div class="reset-stats-box">

        <div>
          <h2>Statistik zurücksetzen</h2>
          <p>
            Alle lokal gespeicherten Prüfungsergebnisse, Themenstatistiken,
            offenen Fragen und Fehlerlisten werden gelöscht.
          </p>
        </div>

        <button class="reset-stats-btn" onclick="resetExamHistory()">
          Statistik zurücksetzen
        </button>

      </div>

      <div class="history-section">

        <div class="section-head">
          <h2>Prüfungsverlauf</h2>
          <p>Alle bisher gespeicherten Prüfungssimulationen</p>
        </div>

        <div class="history-list">
          ${historyRows}
        </div>

      </div>

    </section>
  `;
}

function buildTopicStatsHtml() {
  const rows = categories.map(categoryName => {
    const stats = topicStats[categoryName] || {
      answered: 0,
      correct: 0,
      wrong: 0
    };

    const percent =
      stats.answered === 0
        ? 0
        : Math.round((stats.correct / stats.answered) * 100);

    const mistakeCount = getTopicMistakeCount(categoryName);
    const openCount = getCategoryOpenQuestions(categoryName).length;
    const totalCategoryQuestions = getCategoryQuestions(categoryName).length;
    const answeredUniqueCount =
      totalCategoryQuestions > 0 ? totalCategoryQuestions - openCount : 0;
    const coveragePercent =
      totalCategoryQuestions > 0
        ? Math.round((answeredUniqueCount / totalCategoryQuestions) * 100)
        : 0;

    let statusClass = "topic-neutral";
    let statusText = "Noch nicht bearbeitet";

    if (answeredUniqueCount === 0) {
      statusClass = "topic-neutral";
      statusText = "Noch nicht bearbeitet";
    } else if (coveragePercent < 50) {
      statusClass = "topic-neutral";
      statusText = "Teilweise offen";
    } else if (percent < 50) {
      statusClass = "topic-weak";
      statusText = "Nicht bestanden";
    } else if (percent >= 50 && percent < 70) {
      statusClass = "topic-medium";
      statusText = "Bestanden · Ausbaufähig";
    } else if (percent >= 70 && percent < 85) {
      statusClass = "topic-solid";
      statusText = "Solide";
    } else if (percent >= 85) {
      statusClass = "topic-strong";
      statusText = "Stark";
    }

    return `
      <div class="topic-stat-row">

        <div class="topic-name">
          <strong>${categoryIcons[categoryName] || "📘"} ${escapeHtml(categoryName)}</strong>
        </div>

        <div>
          <span>Fragen</span>
          <strong>${totalCategoryQuestions}</strong>
        </div>

        <div>
          <span>Offen</span>
          <strong>${openCount}</strong>
        </div>

        <div>
          <span>Geübt</span>
          <strong>${stats.answered}x</strong>
        </div>

        <div>
          <span>Richtig</span>
          <strong>${stats.correct}</strong>
        </div>

        <div>
          <span>Falsche Versuche</span>
          <strong>${stats.wrong}</strong>
        </div>

        <div class="quote-column ${statusClass}">
          <span>Quote</span>
          <strong>${percent}%</strong>
        </div>

        <div>
          <span>Aktive Fehler</span>
          <strong>${mistakeCount}</strong>
        </div>

        <div>
          <span>Status</span>
          <strong class="${statusClass}">${statusText}</strong>
        </div>

        <div>
          ${
            mistakeCount > 0
              ? `<button class="next-btn danger-training-btn" onclick='startTopicMistakeTraining(${JSON.stringify(categoryName)})'>Fehler trainieren</button>`
              : `<button class="next-btn secondary-btn" onclick='openCategory(${JSON.stringify(categoryName)})'>Trainieren</button>`
          }
        </div>

      </div>
    `;
  }).join("");

  return `
    <div class="topic-stats-section">

      <div class="section-head">
        <h2>Themenstatistik</h2>
        <p>Kompakte Übersicht nach Sachgebieten: Quote, Fortschritt und aktive Fehler.</p>
      </div>

      <div class="topic-stats-list">
        ${rows}
      </div>

    </div>
  `;
}

function toggleTopicDetails(detailsId) {
  const detailsBox = document.getElementById(detailsId);
  const button = document.querySelector(`[data-details-target="${detailsId}"]`);

  if (!detailsBox) return;

  const isHidden = detailsBox.style.display === "none";

  detailsBox.style.display = isHidden ? "grid" : "none";

  if (button) {
    button.innerText = isHidden
      ? "Details ausblenden ▲"
      : "Details anzeigen ▼";
  }
}

function resetExamHistory() {
  showConfirmModal(
    "Statistik zurücksetzen?",
    "Alle lokal gespeicherten Prüfungsergebnisse, Themenstatistiken, offenen Fragen und Fehlerlisten werden gelöscht. Diese Aktion kann nicht rückgängig gemacht werden.",
    () => {
      localStorage.removeItem(STORAGE_KEYS.examHistory);
      localStorage.removeItem(STORAGE_KEYS.topicStats);
      localStorage.removeItem(STORAGE_KEYS.topicMistakes);
      localStorage.removeItem(STORAGE_KEYS.answeredQuestions);

      examHistory = [];
      topicStats = {};
      topicMistakes = {};
      answeredQuestions = {};
      lastExamMistakes = [];

      closeConfirmModal();
      showSmallNotice("Statistik wurde zurückgesetzt.");
      showStatsPage();
    }
  );
}


/* =========================
   HELFERFUNKTIONEN
========================= */

function getCategoryQuestions(categoryName) {
  return allQuestions.filter(question => {
    return question.category === categoryName;
  });
}

function getQuestionKey(question) {
  if (!question) return "";

  return String(
    question.id ||
    question.question ||
    JSON.stringify(question)
  );
}

function formatQuestionText(text) {
  if (!text) {
    return "";
  }

  const rawText = String(text).trim();

  const hasCombinationNumbers =
    rawText.includes("1.") &&
    rawText.includes("2.") &&
    rawText.includes("3.") &&
    rawText.includes("4.");

  if (!hasCombinationNumbers) {
    return `<h2 class="question-title">${escapeHtml(rawText)}</h2>`;
  }

  const firstNumberIndex = rawText.indexOf("1.");

  const title = rawText
    .slice(0, firstNumberIndex)
    .trim();

  const statementsRaw = rawText
    .slice(firstNumberIndex)
    .replace(/\r/g, "")
    .replace(/\n/g, " ")
    .replace(/\s+/g, " ")
    .trim();

  const statementMatches = statementsRaw.match(/\d\.\s.*?(?=\s\d\.|$)/g);

  if (!statementMatches || statementMatches.length < 4) {
    return `<h2 class="question-title">${escapeHtml(rawText)}</h2>`;
  }

  return `
    <div class="combo-question">

      <h2 class="question-title">
        ${escapeHtml(title)}
      </h2>

      <div class="statement-box">
        ${statementMatches.map(statement => `
          <div class="statement-line">
            ${escapeHtml(statement.trim())}
          </div>
        `).join("")}
      </div>

    </div>
  `;
}

function shuffleArray(array) {
  return [...array].sort(() => Math.random() - 0.5);
}

function createShuffledQuestion(question) {
  if (!question) {
    return question;
  }

  if (!Array.isArray(question.answers) || question.answers.length === 0) {
    return { ...question };
  }

  const originalCorrect = Array.isArray(question.correct) ? question.correct : [];
  const indexedAnswers = question.answers.map((answer, originalIndex) => ({
    answer,
    originalIndex
  }));
  const shuffledEntries = shuffleArray(indexedAnswers);
  const newAnswers = shuffledEntries.map(entry => entry.answer);
  const newCorrect = [];

  shuffledEntries.forEach((entry, newIndex) => {
    if (originalCorrect.includes(entry.originalIndex)) {
      newCorrect.push(newIndex);
    }
  });

  newCorrect.sort((a, b) => a - b);

  return {
    ...question,
    answers: newAnswers,
    correct: newCorrect
  };
}

function formatSeconds(totalSeconds) {
  const minutes = Math.floor(totalSeconds / 60);
  const seconds = totalSeconds % 60;

  return (
    String(minutes).padStart(2, "0") +
    ":" +
    String(seconds).padStart(2, "0")
  );
}

function escapeHtml(value) {
  if (value === undefined || value === null) return "";

  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}


/* =========================
   MODAL / HINWEISE
========================= */

function showConfirmModal(title, message, onConfirm) {
  let modal = document.getElementById("confirmModal");

  if (modal) {
    modal.remove();
  }

  modal = document.createElement("div");
  modal.id = "confirmModal";
  modal.className = "confirm-modal-backdrop";

  modal.innerHTML = `
    <div class="confirm-modal">

      <h2>${escapeHtml(title)}</h2>
      <p>${escapeHtml(message)}</p>

      <div class="confirm-modal-actions">

        <button class="modal-cancel-btn" id="cancelConfirmBtn">
          Abbrechen
        </button>

        <button class="modal-danger-btn" id="confirmActionBtn">
          Ja, zurücksetzen
        </button>

      </div>

    </div>
  `;

  document.body.appendChild(modal);

  const cancelBtn = document.getElementById("cancelConfirmBtn");
  const confirmBtn = document.getElementById("confirmActionBtn");

  if (cancelBtn) {
    cancelBtn.onclick = closeConfirmModal;
  }

  if (confirmBtn) {
    confirmBtn.onclick = onConfirm;
  }
}

function closeConfirmModal() {
  const modal = document.getElementById("confirmModal");

  if (modal) {
    modal.remove();
  }
}

function showSmallNotice(message) {
  let notice = document.getElementById("smallNotice");

  if (!notice) {
    notice = document.createElement("div");
    notice.id = "smallNotice";
    notice.className = "small-notice";
    document.body.appendChild(notice);
  }

  notice.innerText = message;
  notice.classList.add("show");

  setTimeout(() => {
    notice.classList.remove("show");
  }, 2200);
}


/* =========================
   GLOBALE FUNKTIONEN
========================= */

window.showAllQuestions = showAllQuestions;
window.showOpenQuestions = showOpenQuestions;
window.startOpenQuestionsTraining = startOpenQuestionsTraining;

window.showOralExamPage = showOralExamPage;
window.openCategory = openCategory;

window.startExamMode = startExamMode;
window.showExamReview = showExamReview;
window.scrollToAnswers = scrollToAnswers;
window.finishExamMode = finishExamMode;
window.goToExamQuestion = goToExamQuestion;
window.startUnansweredExamFocus = startUnansweredExamFocus;
window.showExamSubmitWarning = showExamSubmitWarning;
window.pauseExam = pauseExam;
window.resumeActiveExamSession = resumeActiveExamSession;
window.discardSavedExamSession = discardSavedExamSession;

window.startMistakeTraining = startMistakeTraining;
window.showMistakeOverview = showMistakeOverview;
window.startTopicMistakeTraining = startTopicMistakeTraining;
window.startAllTopicMistakeTraining = startAllTopicMistakeTraining;

window.showStatsPage = showStatsPage;
window.resetExamHistory = resetExamHistory;

window.showExamStartPage = showExamStartPage;
window.repeatCurrentExamMode = repeatCurrentExamMode;

window.toggleTopicDetails = toggleTopicDetails;

window.startFlashcardSession = startFlashcardSession;
window.startFlashcardSessionByCategory = startFlashcardSessionByCategory;
window.startFlashcardsFromMistakes = startFlashcardsFromMistakes;
window.flipFlashcard = flipFlashcard;
window.nextFlashcard = nextFlashcard;
window.previousFlashcard = previousFlashcard;
window.markFlashcardKnown = markFlashcardKnown;
window.markFlashcardUnknown = markFlashcardUnknown;

/* =====================================================
   v21.5 LERNKARTEN – FORTSCHRITT SPEICHERN
===================================================== */

const FLASHCARD_PROGRESS_KEY = "accaoui_flashcard_progress";

let flashcardProgressStore = {};

function loadFlashcardProgressStore() {
  if (typeof readStorage === "function") {
    flashcardProgressStore = readStorage(FLASHCARD_PROGRESS_KEY, {});
  } else {
    const saved = localStorage.getItem(FLASHCARD_PROGRESS_KEY);
    flashcardProgressStore = saved ? JSON.parse(saved) : {};
  }
}

function saveFlashcardProgressStore() {
  if (typeof writeStorage === "function") {
    writeStorage(FLASHCARD_PROGRESS_KEY, flashcardProgressStore);
  } else {
    localStorage.setItem(FLASHCARD_PROGRESS_KEY, JSON.stringify(flashcardProgressStore));
  }
}

function getFlashcardProgressKey(question) {
  if (!question) return "";

  if (typeof getQuestionKey === "function") {
    return getQuestionKey(question);
  }

  return String(question.id || question.question || JSON.stringify(question));
}

function saveFlashcardProgress(question, status) {
  if (!question) return;

  loadFlashcardProgressStore();

  const key = getFlashcardProgressKey(question);
  const oldEntry = flashcardProgressStore[key] || {
    knownCount: 0,
    unknownCount: 0
  };

  const category = typeof normalizeCategoryName === "function"
    ? normalizeCategoryName(question.category || "")
    : String(question.category || "");

  const newEntry = {
    id: question.id || key,
    category,
    question: question.question || "",
    lastStatus: status,
    knownCount: Number(oldEntry.knownCount || 0) + (status === "known" ? 1 : 0),
    unknownCount: Number(oldEntry.unknownCount || 0) + (status === "unknown" ? 1 : 0),
    updatedAt: new Date().toISOString()
  };

  flashcardProgressStore[key] = newEntry;
  saveFlashcardProgressStore();
}

function getFlashcardCategoryProgress(categoryName) {
  loadFlashcardProgressStore();

  const questions = getCategoryQuestions(categoryName);
  let known = 0;
  let unknown = 0;
  let untouched = 0;

  questions.forEach(question => {
    const key = getFlashcardProgressKey(question);
    const entry = flashcardProgressStore[key];

    if (!entry) {
      untouched++;
      return;
    }

    if (entry.lastStatus === "known") {
      known++;
    } else if (entry.lastStatus === "unknown") {
      unknown++;
    } else {
      untouched++;
    }
  });

  return {
    total: questions.length,
    known,
    unknown,
    untouched
  };
}

function getTotalFlashcardProgress() {
  loadFlashcardProgressStore();

  let known = 0;
  let unknown = 0;

  Object.values(flashcardProgressStore).forEach(entry => {
    if (entry.lastStatus === "known") known++;
    if (entry.lastStatus === "unknown") unknown++;
  });

  return {
    known,
    unknown
  };
}

/* Überschreibt die bisherige Gewusst-Funktion */
function markFlashcardKnown() {
  const question = flashcardQuestions[flashcardIndex];

  if (question) {
    markQuestionAsAnswered(question);
    removeTopicMistake(question);
    saveFlashcardProgress(question, "known");
  }

  flashcardKnownCount++;
  updateFlashcardProgress();
  nextFlashcard();
}

/* Überschreibt die bisherige Nicht-gewusst-Funktion */
function markFlashcardUnknown() {
  const question = flashcardQuestions[flashcardIndex];

  if (question) {
    saveTopicMistake(question);
    saveFlashcardProgress(question, "unknown");
  }

  flashcardUnknownCount++;
  updateFlashcardProgress();
  nextFlashcard();
}

window.markFlashcardKnown = markFlashcardKnown;
window.markFlashcardUnknown = markFlashcardUnknown;
window.saveFlashcardProgress = saveFlashcardProgress;
window.getFlashcardCategoryProgress = getFlashcardCategoryProgress;
window.getTotalFlashcardProgress = getTotalFlashcardProgress;

/* =====================================================
   v22.3 MÜNDLICHE PRÜFUNG – FRAGE/ANTWORT ALS FLIP IN SZENE
   Ziel:
   - keine doppelte Frage mehr
   - Frage sitzt in der Prüfungsszene
   - Musterantwort erscheint in derselben Markierung
   - untere Karte dient nur noch als Bedienpanel
===================================================== */

if (!window.ACCAOUI_V223_ORAL_SCENE_FLIP_PATCH) {
  window.ACCAOUI_V223_ORAL_SCENE_FLIP_PATCH = true;

  function getOralExamUserDisplayNameV223() {
    if (typeof getOralExamUserDisplayNameV222 === "function") {
      return getOralExamUserDisplayNameV222();
    }

    return "Sie";
  }

  function getCurrentOralExamQuestionV223() {
    if (
      typeof oralExamQuestionsV220 !== "undefined" &&
      Array.isArray(oralExamQuestionsV220) &&
      typeof oralExamIndexV220 !== "undefined"
    ) {
      return oralExamQuestionsV220[oralExamIndexV220];
    }

    return null;
  }

  function markOralQuestionCardAsSceneDrivenV223() {
    const card = document.querySelector(".oral-question-card");

    if (!card) return;

    card.classList.add("oral-scene-driven-v223");
  }

  function syncOralRoomFlipCardV223(showAnswer) {
    const scene = document.querySelector(".oral-room-scene-v221.is-session");

    if (!scene) return;

    const table = scene.querySelector(".oral-table-v221");

    if (!table) return;

    const question = getCurrentOralExamQuestionV223();
    const userName = getOralExamUserDisplayNameV223();

    const questionText = question && question.question
      ? String(question.question)
      : "Die aktuelle Prüferfrage wird hier angezeigt.";

    const sampleAnswer = question && question.sampleAnswer
      ? String(question.sampleAnswer)
      : "Keine Musterantwort hinterlegt.";

    const examinerNote = question && question.examinerNote
      ? String(question.examinerNote)
      : "Kein Prüfer-Hinweis hinterlegt.";

    let prompt = scene.querySelector(".oral-room-question-prompt-v222");

    if (!prompt) {
      prompt = document.createElement("div");
      prompt.className = "oral-room-question-prompt-v222";
      table.insertAdjacentElement("afterend", prompt);
    }

    prompt.classList.add("oral-room-flip-v223");

    if (showAnswer) {
      prompt.classList.add("is-answer-visible");
    } else {
      prompt.classList.remove("is-answer-visible");
    }

    prompt.innerHTML = `
      <div class="oral-room-flip-front-v223">
        <span>Prüferfrage an ${escapeHtml(userName)}</span>
        <strong>${escapeHtml(questionText)}</strong>
      </div>

      <div class="oral-room-flip-back-v223">
        <span>Musterantwort</span>
        <strong>${escapeHtml(sampleAnswer)}</strong>

        <div class="oral-room-examiner-note-v223">
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

    markOralQuestionCardAsSceneDrivenV223();
  }

  window.accaouiOriginalRenderOralExamQuestionV223 =
    window.accaouiOriginalRenderOralExamQuestionV223 ||
    window.renderOralExamQuestionV220;

  if (typeof window.accaouiOriginalRenderOralExamQuestionV223 === "function") {
    window.renderOralExamQuestionV220 = function patchedRenderOralExamQuestionV223() {
      const result = window.accaouiOriginalRenderOralExamQuestionV223();

      setTimeout(() => {
        syncOralRoomFlipCardV223(false);
      }, 0);

      return result;
    };
  }

  window.accaouiOriginalShowOralExamAnswerV223 =
    window.accaouiOriginalShowOralExamAnswerV223 ||
    window.showOralExamAnswerV220;

  window.showOralExamAnswerV220 = function patchedShowOralExamAnswerV223() {
    if (typeof window.accaouiOriginalShowOralExamAnswerV223 === "function") {
      const result = window.accaouiOriginalShowOralExamAnswerV223();

      setTimeout(() => {
        syncOralRoomFlipCardV223(true);
      }, 0);

      return result;
    }

    syncOralRoomFlipCardV223(true);
  };

  window.accaouiOriginalStartOralExamSessionV223 =
    window.accaouiOriginalStartOralExamSessionV223 ||
    window.startOralExamSessionV220;

  window.startOralExamSessionV220 = function patchedStartOralExamSessionV223(questions, title) {
    if (typeof window.accaouiOriginalStartOralExamSessionV223 === "function") {
      const result = window.accaouiOriginalStartOralExamSessionV223(questions, title);

      setTimeout(() => {
        syncOralRoomFlipCardV223(false);
      }, 120);

      return result;
    }

    showSmallNotice("Mündliche Prüfungsrunde konnte nicht gestartet werden.");
  };

  window.syncOralRoomFlipCardV223 = syncOralRoomFlipCardV223;
}