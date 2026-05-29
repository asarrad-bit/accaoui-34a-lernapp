/* =====================================================
   v23.5.1 MÜNDLICHE PRÜFUNG – ZENTRALE PRÜFUNGSBOGEN-BANK
   Ziel:
   - zentrale Datenstruktur für mündliche Prüfungsbögen
   - Frage-IDs über AccaouiOralQuestionBank auflösen
===================================================== */

const ORAL_SHEETS_BANK_V2350 = [
  {
    id: "oral_sheet_a_v2340",
    title: "Prüfungsbogen A",
    durationMinutes: 15,
    note: "Trainingsbogen. Keine offizielle IHK-Prüfung.",
    sourceType: "accaoui_original",
    blocks: [
      {
        examinerIndex: 0,
        examinerName: "Prüfer 1",
        title: "Öffentliches Recht / Gewerberecht",
        questionIds: [
          "oral_a_001",
          "oral_a_002",
          "oral_a_003",
          "oral_a_004",
          "oral_a_005"
        ]
      },
      {
        examinerIndex: 1,
        examinerName: "Vorsitz",
        title: "Umgang mit Menschen",
        questionIds: [
          "oral_a_006",
          "oral_a_007",
          "oral_a_008",
          "oral_a_009",
          "oral_a_010"
        ]
      },
      {
        examinerIndex: 2,
        examinerName: "Prüfer 3",
        title: "Mischblock Datenschutz / BGB / Strafrecht / UVV / Waffen / Technik",
        questionIds: [
          "oral_a_011",
          "oral_a_012",
          "oral_a_013",
          "oral_a_014",
          "oral_a_015"
        ]
      }
    ]
  }
];

window.ACCAOUI_ORAL_SHEETS_BANK_V2350 = true;

function collectSheetQuestionIdsV2351(sheet) {
  if (!sheet) {
    return [];
  }

  if (Array.isArray(sheet.questionIds) && sheet.questionIds.length) {
    return sheet.questionIds.slice();
  }

  if (!Array.isArray(sheet.blocks)) {
    return [];
  }

  return sheet.blocks.flatMap(block => {
    return Array.isArray(block.questionIds) ? block.questionIds : [];
  });
}

window.AccaouiOralSheetBank = {
  listSheets() {
    return ORAL_SHEETS_BANK_V2350.map(sheet => ({
      id: sheet.id,
      title: sheet.title,
      durationMinutes: sheet.durationMinutes,
      note: sheet.note,
      sourceType: sheet.sourceType,
      questionCount: collectSheetQuestionIdsV2351(sheet).length
    }));
  },

  getSheetById(id) {
    if (id == null || id === "") {
      return null;
    }

    return ORAL_SHEETS_BANK_V2350.find(sheet => sheet.id === id) || null;
  },

  getSheetQuestions(sheetId) {
    const sheet = this.getSheetById(sheetId);
    const questionIds = collectSheetQuestionIdsV2351(sheet);

    if (!questionIds.length) {
      return [];
    }

    if (
      !window.AccaouiOralQuestionBank ||
      typeof window.AccaouiOralQuestionBank.getQuestionsByIds !== "function"
    ) {
      return [];
    }

    return window.AccaouiOralQuestionBank.getQuestionsByIds(questionIds);
  }
};
