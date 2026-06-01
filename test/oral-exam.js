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