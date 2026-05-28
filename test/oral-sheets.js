/* =====================================================
   ACCAOUI §34a LERN-APP
   oral-sheets.js
   v23.3.1 – Modul-Brücke für mündliche Prüfungsbögen

   Zweck:
   - zentrale Schnittstelle für mündliche Prüfungsbögen vorbereiten
   - Prüfungsbogen A aktuell noch aus patch-v21.js lesen
   - später wandern die echten Bogen-Daten vollständig hierher
===================================================== */

console.log("Accaoui oral-sheets.js geladen");

if (!window.ACCAOUI_ORAL_SHEETS_MODULE) {
  window.ACCAOUI_ORAL_SHEETS_MODULE = true;
}

if (!window.ACCAOUI_ORAL_SHEETS_V2331) {
  window.ACCAOUI_ORAL_SHEETS_V2331 = true;

  function getOralSheetAFromLegacyV2331() {
    return window.ORAL_EXAM_SHEET_A_V2320 || null;
  }

  function getOralSheetAQuestionsV2331() {
    if (typeof window.getOralExamSheetAQuestionsV2320 === "function") {
      return window.getOralExamSheetAQuestionsV2320();
    }

    const sheet = getOralSheetAFromLegacyV2331();

    if (!sheet || !Array.isArray(sheet.blocks)) {
      return [];
    }

    return sheet.blocks.flatMap(block => {
      return block.questions.map(question => ({
        ...question,
        sheetId: sheet.id,
        sheetTitle: sheet.title,
        examinerIndex: block.examinerIndex,
        examinerName: block.examinerName,
        examinerBlockTitle: block.title
      }));
    });
  }

  function getOralSheetByIdV2331(sheetId) {
    if (sheetId === "oral_sheet_a_v2320" || sheetId === "oral_sheet_a") {
      return getOralSheetAFromLegacyV2331();
    }

    return null;
  }

  function getAvailableOralSheetsV2331() {
    const sheetA = getOralSheetAFromLegacyV2331();

    if (!sheetA) {
      return [];
    }

    return [
      {
        id: sheetA.id,
        title: sheetA.title || "Prüfungsbogen A",
        durationMinutes: sheetA.durationMinutes || 15,
        note: sheetA.note || "Trainingsbogen. Keine offizielle IHK-Prüfung.",
        questionCount: getOralSheetAQuestionsV2331().length
      }
    ];
  }

  window.AccaouiOralSheets = {
    getSheetA: getOralSheetAFromLegacyV2331,
    getSheetAQuestions: getOralSheetAQuestionsV2331,
    getSheetById: getOralSheetByIdV2331,
    listSheets: getAvailableOralSheetsV2331
  };

  window.getOralSheetAQuestionsV2331 = getOralSheetAQuestionsV2331;
  window.getAvailableOralSheetsV2331 = getAvailableOralSheetsV2331;
}