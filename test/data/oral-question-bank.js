/* =====================================================
   v23.5.0 MÜNDLICHE PRÜFUNG – ZENTRALE FRAGENBANK
   Ziel:
   - zentrale Datenstruktur für mündliche Prüfungsfragen
   - vorbereitet für spätere Befüllung
===================================================== */

const ORAL_QUESTION_BANK_V2350 = [];

window.ACCAOUI_ORAL_QUESTION_BANK_V2350 = true;

window.AccaouiOralQuestionBank = {
  listQuestions() {
    return ORAL_QUESTION_BANK_V2350.slice();
  },

  getQuestionById(id) {
    if (id == null || id === "") {
      return null;
    }

    return ORAL_QUESTION_BANK_V2350.find(question => question.id === id) || null;
  },

  getQuestionsByIds(ids) {
    if (!Array.isArray(ids) || !ids.length) {
      return [];
    }

    return ids
      .map(id => this.getQuestionById(id))
      .filter(Boolean);
  },

  listCategories() {
    const categories = new Set();

    ORAL_QUESTION_BANK_V2350.forEach(question => {
      if (question && question.category) {
        categories.add(question.category);
      }
    });

    return Array.from(categories).sort();
  },

  getStats() {
    const categories = this.listCategories();

    return {
      total: ORAL_QUESTION_BANK_V2350.length,
      categories: categories.length,
      categoryList: categories
    };
  }
};
