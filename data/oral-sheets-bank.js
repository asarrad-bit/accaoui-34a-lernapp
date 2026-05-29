/* =====================================================
   v23.5.0 MÜNDLICHE PRÜFUNG – ZENTRALE PRÜFUNGSBOGEN-BANK
   Ziel:
   - zentrale Datenstruktur für mündliche Prüfungsbögen
   - Frage-IDs später über AccaouiOralQuestionBank auflösen
===================================================== */

const ORAL_SHEETS_BANK_V2350 = [];

window.ACCAOUI_ORAL_SHEETS_BANK_V2350 = true;

window.AccaouiOralSheetBank = {
  listSheets() {
    return ORAL_SHEETS_BANK_V2350.slice();
  },

  getSheetById(id) {
    if (id == null || id === "") {
      return null;
    }

    return ORAL_SHEETS_BANK_V2350.find(sheet => sheet.id === id) || null;
  },

  getSheetQuestions(sheetId) {
    const sheet = this.getSheetById(sheetId);

    if (!sheet || !Array.isArray(sheet.questionIds) || !sheet.questionIds.length) {
      return [];
    }

    if (
      !window.AccaouiOralQuestionBank ||
      typeof window.AccaouiOralQuestionBank.getQuestionsByIds !== "function"
    ) {
      return [];
    }

    return window.AccaouiOralQuestionBank.getQuestionsByIds(sheet.questionIds);
  }
};
