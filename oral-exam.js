/* =====================================================
   ACCAOUI §34a LERN-APP
   oral-exam.js
   v23.3.5 MÜNDLICHE FEHLERTRAINER – ALTE KARTEN NORMALISIEREN
===================================================== */

console.log("Accaoui oral-exam.js geladen");

if (!window.ACCAOUI_ORAL_EXAM_MODULE) {
  window.ACCAOUI_ORAL_EXAM_MODULE = true;
}

if (!window.ACCAOUI_V2335_ORAL_MISTAKE_CARD_NORMALIZER) {
  window.ACCAOUI_V2335_ORAL_MISTAKE_CARD_NORMALIZER = true;

  function revealOralMistakeCardV2335(button) {
    const card = button.closest(".oral-mistake-card-v2324");

    if (!card) return;

    card.classList.add("is-answer-visible-v2335");

    const answerBox = card.querySelector(".oral-mistake-answer-v2324");
    const noteBox = card.querySelector(".oral-mistake-note-v2324");

    [answerBox, noteBox].forEach((element) => {
      if (!element) return;

      element.removeAttribute("hidden");
      element.setAttribute("aria-hidden", "false");
      element.style.setProperty("display", "block", "important");
      element.style.setProperty("visibility", "visible", "important");
      element.style.setProperty("opacity", "1", "important");
    });

    button.style.setProperty("display", "none", "important");
    button.disabled = true;

    const resolveButton = card.querySelector(".oral-mistake-resolve-btn-v2324");

    if (resolveButton) {
      resolveButton.removeAttribute("hidden");
      resolveButton.setAttribute("aria-hidden", "false");
      resolveButton.style.setProperty("display", "inline-flex", "important");
    }

    const practiceButton = card.querySelector(".oral-mistake-practice-btn-v2360");

    if (practiceButton) {
      practiceButton.style.setProperty("display", "inline-flex", "important");
    }
  }

  function normalizeOralMistakeCardsV2335() {
    const cards = document.querySelectorAll(".oral-mistake-card-v2324");

    cards.forEach((card) => {
      if (card.classList.contains("is-normalized-v2335")) return;

      const answerBox = card.querySelector(".oral-mistake-answer-v2324");
      const noteBox = card.querySelector(".oral-mistake-note-v2324");
      const resolveButton = card.querySelector(".oral-mistake-resolve-btn-v2324");

      if (!answerBox && !noteBox) return;

      card.classList.add("is-normalized-v2335");

      const existingHint = card.querySelector(
        ".oral-mistake-training-hint-v2335, .oral-mistake-training-hint-v2325, .oral-mistake-training-hint-v2326"
      );

      if (!existingHint) {
        const hint = document.createElement("div");
        hint.className = "oral-mistake-training-hint-v2335";
        hint.innerHTML = `
        <span>Übungsauftrag</span>
        <p>
          Antworten Sie zuerst laut. Danach Musterantwort anzeigen und vergleichen.
        </p>
      `;

        const questionTitle = card.querySelector("h3");

        if (questionTitle) {
          questionTitle.insertAdjacentElement("afterend", hint);
        }
      }

      let actions = card.querySelector(
        ".oral-mistake-card-actions-v2335, .oral-mistake-card-actions-v2325, .oral-mistake-card-actions-v2326"
      );

      if (!actions) {
        actions = document.createElement("div");
        actions.className = "oral-mistake-card-actions-v2335";

        if (noteBox) {
          noteBox.insertAdjacentElement("afterend", actions);
        } else if (answerBox) {
          answerBox.insertAdjacentElement("afterend", actions);
        }
      }

      let revealButton = actions.querySelector(
        ".oral-mistake-reveal-btn-v2335, .oral-mistake-reveal-btn-v2325, .oral-mistake-reveal-btn-v2326"
      );

      if (!revealButton) {
        revealButton = document.createElement("button");
        revealButton.type = "button";
        revealButton.className = "next-btn oral-mistake-reveal-btn-v2335";
        revealButton.textContent = "Musterantwort anzeigen";
        actions.appendChild(revealButton);
      }

      revealButton.onclick = function () {
        revealOralMistakeCardV2335(revealButton);
      };

      let practiceButton = actions.querySelector(".oral-mistake-practice-btn-v2360");

      if (!practiceButton) {
        practiceButton = document.createElement("button");
        practiceButton.type = "button";
        practiceButton.className = "next-btn secondary-btn oral-mistake-practice-btn-v2360";
        practiceButton.textContent = "Noch üben";
        practiceButton.style.display = "none";
        practiceButton.onclick = function () {
          card.classList.remove(
            "is-answer-visible-v2335",
            "is-answer-visible-v2325",
            "is-answer-visible-v2326"
          );

          [answerBox, noteBox].forEach((element) => {
            if (!element) return;

            element.setAttribute("hidden", "");
            element.setAttribute("aria-hidden", "true");
            element.style.removeProperty("display");
            element.style.removeProperty("visibility");
            element.style.removeProperty("opacity");
          });

          const currentRevealButton = card.querySelector(
            ".oral-mistake-reveal-btn-v2335, .oral-mistake-reveal-btn-v2325, .oral-mistake-reveal-btn-v2326"
          );

          if (currentRevealButton) {
            currentRevealButton.style.setProperty("display", "inline-flex", "important");
            currentRevealButton.disabled = false;
          }

          practiceButton.style.setProperty("display", "none", "important");

          const currentResolveButton = card.querySelector(".oral-mistake-resolve-btn-v2324");

          if (currentResolveButton) {
            currentResolveButton.style.setProperty("display", "none", "important");
          }
        };

        actions.appendChild(practiceButton);
      }

      if (resolveButton && !actions.contains(resolveButton)) {
        resolveButton.style.display = "none";
        actions.appendChild(resolveButton);
      } else if (resolveButton && !card.classList.contains("is-answer-visible-v2335")) {
        resolveButton.style.display = "none";
      }
    });
  }

  function scheduleNormalizeOralMistakeCardsV2335() {
    setTimeout(normalizeOralMistakeCardsV2335, 50);
    setTimeout(normalizeOralMistakeCardsV2335, 200);
    setTimeout(normalizeOralMistakeCardsV2335, 600);
  }

  const observerV2335 = new MutationObserver(() => {
    scheduleNormalizeOralMistakeCardsV2335();
  });

  if (document.body) {
    observerV2335.observe(document.body, {
      childList: true,
      subtree: true
    });
  }

  window.normalizeOralMistakeCardsV2335 = normalizeOralMistakeCardsV2335;
  window.revealOralMistakeCardV2335 = revealOralMistakeCardV2335;

  scheduleNormalizeOralMistakeCardsV2335();
}

/* =====================================================
   v23.3.6 MÜNDLICHE PRÜFUNG – SCROLL STABILISIEREN
   Ziel:
   - kein nerviges Hoch-/Runterspringen beim Antworten
   - aktuelle Frage/Karte bleibt sauber im Blick
===================================================== */

if (!window.ACCAOUI_V2336_ORAL_SCROLL_STABILITY) {
  window.ACCAOUI_V2336_ORAL_SCROLL_STABILITY = true;

  function getOralScrollOffsetV2336() {
    return window.innerWidth <= 640 ? 76 : 96;
  }

  function scrollToOralElementV2336(element, behavior) {
    if (!element) return;

    const rect = element.getBoundingClientRect();
    const targetTop = window.scrollY + rect.top - getOralScrollOffsetV2336();

    window.scrollTo({
      top: Math.max(0, targetTop),
      behavior: behavior || "smooth"
    });
  }

  function scrollToCurrentOralQuestionV2336(behavior) {
    const element =
      document.querySelector(".oral-question-card") ||
      document.getElementById("oralQuestionAreaV220") ||
      document.querySelector(".oral-session-header");

    scrollToOralElementV2336(element, behavior || "smooth");
  }

  function scheduleOralQuestionScrollV2336() {
    setTimeout(() => scrollToCurrentOralQuestionV2336("auto"), 40);
    setTimeout(() => scrollToCurrentOralQuestionV2336("smooth"), 160);
  }

  window.accaouiPreviousRateOralExamQuestionV2336 =
    window.accaouiPreviousRateOralExamQuestionV2336 ||
    window.rateOralExamQuestionV220;

  if (typeof window.accaouiPreviousRateOralExamQuestionV2336 === "function") {
    window.rateOralExamQuestionV220 = function patchedRateOralExamQuestionV2336(status) {
      const result = window.accaouiPreviousRateOralExamQuestionV2336(status);
      scheduleOralQuestionScrollV2336();
      return result;
    };
  }

  window.accaouiPreviousPreviousOralExamQuestionV2336 =
    window.accaouiPreviousPreviousOralExamQuestionV2336 ||
    window.previousOralExamQuestionV220;

  if (typeof window.accaouiPreviousPreviousOralExamQuestionV2336 === "function") {
    window.previousOralExamQuestionV220 = function patchedPreviousOralExamQuestionV2336() {
      const result = window.accaouiPreviousPreviousOralExamQuestionV2336();
      scheduleOralQuestionScrollV2336();
      return result;
    };
  }

  try {
    rateOralExamQuestionV220 = window.rateOralExamQuestionV220;
    previousOralExamQuestionV220 = window.previousOralExamQuestionV220;
  } catch (error) {
    /* Rebinding je nach Browser nicht notwendig */
  }

  window.scrollToCurrentOralQuestionV2336 = scrollToCurrentOralQuestionV2336;
}

/* =====================================================
   v23.4.0 MÜNDLICHER FEHLERTRAINER – SAUBERER RENDERER
   Ziel:
   - neuer führender Renderer für mündliche Fehlerkarten
   - alte Anzeige-Funktionen auf diesen Renderer umleiten
   - Speicherlogik localStorage beibehalten
===================================================== */

if (!window.ACCAOUI_V2340_ORAL_MISTAKE_RENDERER) {
  window.ACCAOUI_V2340_ORAL_MISTAKE_RENDERER = true;

  const ORAL_MISTAKE_STORAGE_KEY_V2340 = "accaoui_oral_exam_mistakes_v2324";

  function escapeHtmlV2340(value) {
    if (typeof escapeHtml === "function") {
      return escapeHtml(value);
    }

    return String(value == null ? "" : value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  function readOralMistakesV2340() {
    try {
      const raw = localStorage.getItem(ORAL_MISTAKE_STORAGE_KEY_V2340);
      const parsed = JSON.parse(raw || "[]");
      return Array.isArray(parsed) ? parsed : [];
    } catch (error) {
      return [];
    }
  }

  function writeOralMistakesV2340(list) {
    localStorage.setItem(
      ORAL_MISTAKE_STORAGE_KEY_V2340,
      JSON.stringify(Array.isArray(list) ? list : [])
    );
  }

  function removeOralMistakeV2340(key) {
    if (!key) return;

    const mistakes = readOralMistakesV2340().filter(function (item) {
      return item && item.key !== key;
    });

    writeOralMistakesV2340(mistakes);
  }

  function getOralMistakeCardV2340(key) {
    const cards = document.querySelectorAll("[data-oral-mistake-key-v2340]");

    for (let index = 0; index < cards.length; index++) {
      if (cards[index].getAttribute("data-oral-mistake-key-v2340") === String(key)) {
        return cards[index];
      }
    }

    return null;
  }

  function applyOralMistakeCardOpenStateV2340(card) {
    if (!card) return;

    const isOpen = card.getAttribute("data-oral-mistake-open-v2340") === "true";
    const answerBox = card.querySelector(".oral-mistake-answer-v2324");
    const noteBox = card.querySelector(".oral-mistake-note-v2324");
    const revealButton = card.querySelector(".oral-mistake-reveal-btn-v2335");
    const resolveButton = card.querySelector(".oral-mistake-resolve-btn-v2324");
    const practiceButton = card.querySelector(".oral-mistake-practice-btn-v2360");

    [answerBox, noteBox].forEach(function (element) {
      if (!element) return;
      element.style.display = isOpen ? "block" : "none";
    });

    if (revealButton) {
      revealButton.style.display = isOpen ? "none" : "inline-flex";
    }

    if (resolveButton) {
      resolveButton.style.display = isOpen ? "inline-flex" : "none";
    }

    if (practiceButton) {
      practiceButton.style.display = isOpen ? "inline-flex" : "none";
    }
  }

  function revealOralMistakeV2340(key) {
    const card = getOralMistakeCardV2340(key);

    if (!card) return;

    card.setAttribute("data-oral-mistake-open-v2340", "true");
    card.classList.add("is-answer-visible-v2335");
    applyOralMistakeCardOpenStateV2340(card);
  }

  function collapseOralMistakeV2340(key) {
    const card = getOralMistakeCardV2340(key);

    if (!card) return;

    card.setAttribute("data-oral-mistake-open-v2340", "false");
    card.classList.remove(
      "is-answer-visible-v2335",
      "is-answer-visible-v2325",
      "is-answer-visible-v2326"
    );
    applyOralMistakeCardOpenStateV2340(card);
  }

  function markOralMistakeResolvedV2340(key) {
    removeOralMistakeV2340(key);

    if (typeof showSmallNotice === "function") {
      showSmallNotice("Mündlicher Fehler wurde als sicher markiert.");
    }

    showOralMistakeTrainingV2340();
  }

  function showOralMistakeTrainingV2340() {
    const mainContent = document.querySelector(".main-content");

    if (!mainContent) return;

    const mistakes = readOralMistakesV2340();

    if (!mistakes.length) {
      if (typeof showSmallNotice === "function") {
        showSmallNotice("Keine mündlichen Prüfungsfehler gespeichert.");
      }

      return;
    }

    const cards = mistakes.map(function (item, index) {
      const itemKey = escapeHtmlV2340(item.key || "");

      return (
        '<article class="oral-mistake-card-v2324" data-oral-mistake-key-v2340="' +
        itemKey +
        '" data-oral-mistake-open-v2340="false">' +
        '<div class="oral-mistake-top-v2324">' +
        "<span>Frage " + (index + 1) + "</span>" +
        "<strong>" + escapeHtmlV2340(item.examinerName || item.category || "Mündliche Prüfung") + "</strong>" +
        "</div>" +
        '<p class="oral-mistake-category-v2324">' +
        escapeHtmlV2340(item.examinerBlockTitle || item.category || "Prüfungsbogen A") +
        "</p>" +
        "<h3>" + escapeHtmlV2340(item.question || "") + "</h3>" +
        '<div class="oral-mistake-training-hint-v2335">' +
        "<span>Übungsauftrag</span>" +
        "<p>Antworten Sie zuerst laut. Danach Musterantwort anzeigen und vergleichen.</p>" +
        "</div>" +
        '<div class="oral-mistake-answer-v2324" style="display:none;">' +
        "<span>Musterantwort</span>" +
        "<p>" + escapeHtmlV2340(item.sampleAnswer || "Keine Musterantwort hinterlegt.") + "</p>" +
        "</div>" +
        '<div class="oral-mistake-note-v2324" style="display:none;">' +
        "<span>Prüfer-Hinweis</span>" +
        "<p>" + escapeHtmlV2340(item.examinerNote || "Kein Prüfer-Hinweis hinterlegt.") + "</p>" +
        "</div>" +
        '<div class="oral-mistake-card-actions-v2335">' +
        '<button type="button" class="next-btn oral-mistake-reveal-btn-v2335" data-oral-action-v2340="reveal" data-oral-key-v2340="' +
        itemKey +
        '">' +
        "Musterantwort anzeigen" +
        "</button>" +
        '<button type="button" class="next-btn oral-mistake-resolve-btn-v2324" style="display:none;" data-oral-action-v2340="resolve" data-oral-key-v2340="' +
        itemKey +
        '">' +
        "Als sicher markieren" +
        "</button>" +
        '<button type="button" class="next-btn secondary-btn oral-mistake-practice-btn-v2360" style="display:none;" data-oral-action-v2340="collapse" data-oral-key-v2340="' +
        itemKey +
        '">' +
        "Noch üben" +
        "</button>" +
        "</div>" +
        "</article>"
      );
    }).join("");

    mainContent.innerHTML =
      '<button class="back-btn" onclick="showMistakeOverview()">' +
      "← Zurück zum Fehlertraining" +
      "</button>" +
      '<section class="result-wrapper oral-mistake-wrapper-v2324">' +
      '<div class="oral-mistake-hero-v2324">' +
      '<p class="eyebrow">Mündliche Prüfung</p>' +
      "<h1>Mündliche Fehler trainieren</h1>" +
      "<p>" +
      "Hier erscheinen nur Fragen, die in der mündlichen Simulation mit " +
      "„Noch üben“ bewertet wurden. Die Musterantwort bleibt zuerst verdeckt." +
      "</p>" +
      '<div class="oral-mistake-count-v2324">' +
      "<strong>" + mistakes.length + "</strong>" +
      "<span>offene mündliche Fehler</span>" +
      "</div>" +
      "</div>" +
      '<div class="oral-mistake-list-v2324">' +
      cards +
      "</div>" +
      '<div class="result-actions oral-mistake-actions-v2324">' +
      '<button class="next-btn" onclick="startOralSimulation15V2314()">' +
      "Prüfungsbogen A wiederholen" +
      "</button>" +
      '<button class="next-btn" onclick="showMistakeOverview()">' +
      "Zur Fehlerübersicht" +
      "</button>" +
      '<button class="next-btn secondary-btn" onclick="location.reload()">' +
      "Zurück zum Dashboard" +
      "</button>" +
      "</div>" +
      "</section>";

    mainContent.querySelectorAll("[data-oral-action-v2340]").forEach(function (button) {
      button.addEventListener("click", function () {
        const action = button.getAttribute("data-oral-action-v2340");
        const key = button.getAttribute("data-oral-key-v2340");

        if (action === "reveal") {
          revealOralMistakeV2340(key);
          return;
        }

        if (action === "resolve") {
          markOralMistakeResolvedV2340(key);
          return;
        }

        if (action === "collapse") {
          collapseOralMistakeV2340(key);
        }
      });
    });

    mainContent.querySelectorAll("[data-oral-mistake-key-v2340]").forEach(function (card) {
      card.classList.add("is-normalized-v2335");
      applyOralMistakeCardOpenStateV2340(card);
    });
  }

  window.showOralMistakeTrainingV2340 = showOralMistakeTrainingV2340;
  window.revealOralMistakeV2340 = revealOralMistakeV2340;
  window.collapseOralMistakeV2340 = collapseOralMistakeV2340;
  window.markOralMistakeResolvedV2340 = markOralMistakeResolvedV2340;

  window.showOralMistakeTrainingV2324 = showOralMistakeTrainingV2340;
  window.showOralMistakeTrainingV2325 = showOralMistakeTrainingV2340;
  window.showOralMistakeTrainingV2326 = showOralMistakeTrainingV2340;

  try {
    showOralMistakeTrainingV2324 = window.showOralMistakeTrainingV2340;
  } catch (error) {
    /* Rebinding je nach Browser nicht notwendig */
  }

  try {
    showOralMistakeTrainingV2325 = window.showOralMistakeTrainingV2340;
  } catch (error) {
    /* Rebinding je nach Browser nicht notwendig */
  }

  try {
    showOralMistakeTrainingV2326 = window.showOralMistakeTrainingV2340;
  } catch (error) {
    /* Rebinding je nach Browser nicht notwendig */
  }
}