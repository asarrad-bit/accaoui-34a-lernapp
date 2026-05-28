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

    button.textContent = "Antwort angezeigt";
    button.disabled = true;

    const resolveButton = card.querySelector(".oral-mistake-resolve-btn-v2324");

    if (resolveButton) {
      resolveButton.style.display = "inline-flex";
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

      const hint = document.createElement("div");
      hint.className = "oral-mistake-training-hint-v2335";
      hint.innerHTML = `
        <span>Übungsauftrag</span>
        <p>
          Antworten Sie zuerst laut. Danach Musterantwort anzeigen und vergleichen.
        </p>
      `;

      const actions = document.createElement("div");
      actions.className = "oral-mistake-card-actions-v2335";

      const revealButton = document.createElement("button");
      revealButton.type = "button";
      revealButton.className = "next-btn oral-mistake-reveal-btn-v2335";
      revealButton.textContent = "Musterantwort anzeigen";
      revealButton.onclick = function () {
        revealOralMistakeCardV2335(revealButton);
      };

      actions.appendChild(revealButton);

      if (resolveButton) {
        resolveButton.style.display = "none";
        actions.appendChild(resolveButton);
      }

      const questionTitle = card.querySelector("h3");

      if (questionTitle) {
        questionTitle.insertAdjacentElement("afterend", hint);
      }

      if (noteBox) {
        noteBox.insertAdjacentElement("afterend", actions);
      } else if (answerBox) {
        answerBox.insertAdjacentElement("afterend", actions);
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
