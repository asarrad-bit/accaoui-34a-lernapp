/* =====================================================
   v23.5.1 MÜNDLICHE PRÜFUNG – ZENTRALE FRAGENBANK
   Ziel:
   - zentrale Datenstruktur für mündliche Prüfungsfragen
   - Prüfungsbogen A gespiegelt aus oral-sheets.js
===================================================== */

const ORAL_QUESTION_BANK_V2350 = [
  {
    id: "oral_a_001",
    examType: "oral",
    category: "Recht der öffentlichen Sicherheit und Ordnung",
    topic: "Öffentliches Recht",
    difficulty: "grundlegend",
    question: "Welche Rechte hat ein privater Sicherheitsmitarbeiter im Vergleich zur Polizei grundsätzlich nicht?",
    sampleAnswer: "Ein privater Sicherheitsmitarbeiter hat grundsätzlich keine hoheitlichen Polizeibefugnisse. Er darf nicht wie ein Polizeibeamter Platzverweise im öffentlichen Raum aussprechen, Personen ohne Rechtsgrund durchsuchen oder staatliche Zwangsmaßnahmen durchführen. Er handelt vor allem auf Grundlage von Hausrecht, Jedermannsrechten und privatrechtlichen Befugnissen.",
    examinerNote: "Wichtig ist die klare Trennung zwischen staatlicher Hoheitsgewalt und privatem Sicherheitsdienst.",
    tags: ["polizei", "befugnisse", "privater sicherheitsdienst"],
    sourceType: "accaoui_original",
    sheetRefs: ["oral_sheet_a_v2340"]
  },
  {
    id: "oral_a_002",
    examType: "oral",
    category: "Recht der öffentlichen Sicherheit und Ordnung",
    topic: "Öffentliches Recht",
    difficulty: "grundlegend",
    question: "Was versteht man unter öffentlicher Sicherheit?",
    sampleAnswer: "Öffentliche Sicherheit umfasst den Schutz der Rechtsordnung, des Staates und seiner Einrichtungen sowie den Schutz individueller Rechtsgüter wie Leben, Gesundheit, Freiheit und Eigentum.",
    examinerNote: "Gute Antwort nennt Rechtsordnung, Staat und Individualrechtsgüter.",
    tags: ["öffentliche sicherheit", "rechtsgüter"],
    sourceType: "accaoui_original",
    sheetRefs: ["oral_sheet_a_v2340"]
  },
  {
    id: "oral_a_003",
    examType: "oral",
    category: "Gewerberecht",
    topic: "Gewerberecht",
    difficulty: "grundlegend",
    question: "Warum ist § 34a GewO für das Bewachungsgewerbe wichtig?",
    sampleAnswer: "§ 34a GewO regelt den gewerberechtlichen Zugang zum Bewachungsgewerbe. Er betrifft insbesondere die Erlaubnis, die Zuverlässigkeit und die erforderlichen Nachweise wie Unterrichtung oder Sachkundeprüfung je nach Tätigkeit.",
    examinerNote: "Wichtig: § 34a GewO ist keine Polizeibefugnis, sondern eine gewerberechtliche Vorschrift.",
    tags: ["34a", "gewo", "bewachungsgewerbe"],
    sourceType: "accaoui_original",
    sheetRefs: ["oral_sheet_a_v2340"]
  },
  {
    id: "oral_a_004",
    examType: "oral",
    category: "Gewerberecht",
    topic: "Gewerberecht",
    difficulty: "mittel",
    question: "Welche Bedeutung hat die Zuverlässigkeit im Bewachungsgewerbe?",
    sampleAnswer: "Zuverlässigkeit ist eine zentrale Voraussetzung. Wer unzuverlässig ist, kann von der Tätigkeit ausgeschlossen werden oder eine Erlaubnis kann versagt beziehungsweise widerrufen werden. Hintergrund ist, dass Sicherheitsmitarbeiter mit fremden Rechtsgütern und sensiblen Situationen umgehen.",
    examinerNote: "Gute Antwort verbindet Zuverlässigkeit mit Vertrauen, Gefahrennähe und behördlicher Kontrolle.",
    tags: ["zuverlässigkeit", "erlaubnis"],
    sourceType: "accaoui_original",
    sheetRefs: ["oral_sheet_a_v2340"]
  },
  {
    id: "oral_a_005",
    examType: "oral",
    category: "Gewerberecht",
    topic: "Gewerberecht",
    difficulty: "mittel",
    question: "Welche Pflichten bestehen beim Dienstausweis im Bewachungsgewerbe?",
    sampleAnswer: "Der Dienstausweis dient der Legitimation im Dienst. Je nach Tätigkeit muss er mitgeführt und zuständigen Personen oder Behörden auf Verlangen vorgezeigt werden. Er darf nicht den Eindruck eines amtlichen oder hoheitlichen Ausweises erwecken.",
    examinerNote: "Wichtig ist: Dienstausweis ja, aber keine Verwechslung mit Polizei oder Behörde.",
    tags: ["dienstausweis", "legitimation"],
    sourceType: "accaoui_original",
    sheetRefs: ["oral_sheet_a_v2340"]
  },
  {
    id: "oral_a_006",
    examType: "oral",
    category: "Umgang mit Menschen",
    topic: "Umgang mit Menschen",
    difficulty: "grundlegend",
    question: "Warum ist professioneller Umgang mit Menschen im Sicherheitsdienst besonders wichtig?",
    sampleAnswer: "Sicherheitsmitarbeiter haben häufig Kontakt mit Menschen in angespannten Situationen. Professionelles Verhalten hilft, Konflikte zu vermeiden, deeskalierend zu handeln, den Auftrag sicher zu erfüllen und das Ansehen des Auftraggebers zu schützen.",
    examinerNote: "Gute Antwort nennt Professionalität, Deeskalation, Auftraggeber und Eigenschutz.",
    tags: ["professionalität", "deeskalation", "auftraggeber"],
    sourceType: "accaoui_original",
    sheetRefs: ["oral_sheet_a_v2340"]
  },
  {
    id: "oral_a_007",
    examType: "oral",
    category: "Umgang mit Menschen",
    topic: "Umgang mit Menschen",
    difficulty: "mittel",
    question: "Wie reagieren Sie, wenn eine Person Sie provoziert oder beleidigt?",
    sampleAnswer: "Ich bleibe ruhig, lasse mich nicht provozieren, halte Sicherheitsabstand, spreche sachlich und klar. Ich setze Grenzen, hole bei Bedarf Unterstützung und handle nach Dienstanweisung. Ich antworte nicht mit Beleidigungen.",
    examinerNote: "Prüfer achten auf Ruhe, Distanz, klare Kommunikation und keine Gegenprovokation.",
    tags: ["provokation", "kommunikation", "sicherheitsabstand"],
    sourceType: "accaoui_original",
    sheetRefs: ["oral_sheet_a_v2340"]
  },
  {
    id: "oral_a_008",
    examType: "oral",
    category: "Umgang mit Menschen",
    topic: "Umgang mit Menschen",
    difficulty: "mittel",
    question: "Was bedeutet Deeskalation in der Praxis?",
    sampleAnswer: "Deeskalation bedeutet, eine angespannte Situation durch ruhiges, kontrolliertes und respektvolles Verhalten zu beruhigen. Dazu gehören Abstand, klare Sprache, aktives Zuhören, keine Provokation und rechtzeitiges Hinzuziehen von Unterstützung.",
    examinerNote: "Wichtig ist praktisches Verhalten, nicht nur das Wort Deeskalation.",
    tags: ["deeskalation", "kommunikation", "konflikt"],
    sourceType: "accaoui_original",
    sheetRefs: ["oral_sheet_a_v2340"]
  },
  {
    id: "oral_a_009",
    examType: "oral",
    category: "Umgang mit Menschen",
    topic: "Umgang mit Menschen",
    difficulty: "mittel",
    question: "Welche Rolle spielt Körpersprache im Sicherheitsdienst?",
    sampleAnswer: "Körpersprache wirkt auf andere Menschen oft stärker als Worte. Eine offene, ruhige und sichere Haltung kann deeskalierend wirken. Drohende Gesten, zu nahes Herantreten oder hektische Bewegungen können dagegen eskalieren.",
    examinerNote: "Gute Antwort nennt Wirkung, Distanz, Haltung und Eskalationsgefahr.",
    tags: ["körpersprache", "deeskalation", "eskalation"],
    sourceType: "accaoui_original",
    sheetRefs: ["oral_sheet_a_v2340"]
  },
  {
    id: "oral_a_010",
    examType: "oral",
    category: "Umgang mit Menschen",
    topic: "Umgang mit Menschen",
    difficulty: "mittel",
    question: "Was beachten Sie bei Jugendlichen in Konfliktsituationen?",
    sampleAnswer: "Ich bleibe sachlich, respektvoll und klar. Ich vermeide Bloßstellung, behandle Jugendliche nicht herablassend und achte auf Gruppendynamik. Gleichzeitig setze ich klare Grenzen und sichere mich ab.",
    examinerNote: "Wichtig sind Gruppendynamik, Respekt, klare Grenzen und Eigensicherung.",
    tags: ["jugendliche", "gruppendynamik", "konflikt"],
    sourceType: "accaoui_original",
    sheetRefs: ["oral_sheet_a_v2340"]
  },
  {
    id: "oral_a_011",
    examType: "oral",
    category: "Datenschutzrecht",
    topic: "Datenschutz",
    difficulty: "grundlegend",
    question: "Was sind personenbezogene Daten?",
    sampleAnswer: "Personenbezogene Daten sind Informationen, die sich auf eine identifizierte oder identifizierbare natürliche Person beziehen. Beispiele sind Name, Anschrift, Telefonnummer, Ausweisnummer, Bildaufnahmen oder Besucherdaten.",
    examinerNote: "Gute Antwort nennt die identifizierte oder identifizierbare Person und Beispiele.",
    tags: ["datenschutz", "personenbezogene daten"],
    sourceType: "accaoui_original",
    sheetRefs: ["oral_sheet_a_v2340"]
  },
  {
    id: "oral_a_012",
    examType: "oral",
    category: "Bürgerliches Gesetzbuch",
    topic: "Hausrecht",
    difficulty: "grundlegend",
    question: "Was kann ein Sicherheitsmitarbeiter auf Grundlage des Hausrechts tun?",
    sampleAnswer: "Er kann im Auftrag des Hausrechtsinhabers Personen ansprechen, auf Regeln hinweisen, zum Verlassen auffordern oder ein Hausverbot durchsetzen, soweit dies rechtlich zulässig und verhältnismäßig ist.",
    examinerNote: "Wichtig: Hausrecht ist nicht grenzenlos und ersetzt keine Polizeibefugnisse.",
    tags: ["hausrecht", "bgb", "hausverbot"],
    sourceType: "accaoui_original",
    sheetRefs: ["oral_sheet_a_v2340"]
  },
  {
    id: "oral_a_013",
    examType: "oral",
    category: "Strafgesetzbuch und Strafverfahrensrecht",
    topic: "Strafrecht",
    difficulty: "mittel",
    question: "Wann kann eine vorläufige Festnahme durch Jedermann in Betracht kommen?",
    sampleAnswer: "Sie kann in Betracht kommen, wenn jemand auf frischer Tat betroffen oder verfolgt wird und Fluchtverdacht besteht oder die Identität nicht sofort festgestellt werden kann. Die Polizei muss unverzüglich hinzugezogen werden.",
    examinerNote: "Wichtig sind frische Tat, Fluchtverdacht oder Identitätsfeststellung und unverzügliche Polizei.",
    tags: ["festnahme", "jedermann", "strafrecht"],
    sourceType: "accaoui_original",
    sheetRefs: ["oral_sheet_a_v2340"]
  },
  {
    id: "oral_a_014",
    examType: "oral",
    category: "Unfallverhütungsvorschriften Wach- und Sicherungsdienste",
    topic: "Arbeitssicherheit",
    difficulty: "grundlegend",
    question: "Warum ist Eigenschutz im Sicherheitsdienst so wichtig?",
    sampleAnswer: "Eigenschutz ist wichtig, weil Sicherheitsmitarbeiter Gefahren erkennen, vermeiden und kontrolliert handeln müssen. Sie sollen sich nicht unnötig selbst gefährden und bei Bedarf Unterstützung anfordern.",
    examinerNote: "Gute Antwort verbindet Eigenschutz, Gefährdung, Unterstützung und professionelles Verhalten.",
    tags: ["eigenschutz", "uvv", "gefährdung"],
    sourceType: "accaoui_original",
    sheetRefs: ["oral_sheet_a_v2340"]
  },
  {
    id: "oral_a_015",
    examType: "oral",
    category: "Grundzüge der Sicherheitstechnik",
    topic: "Sicherheitstechnik",
    difficulty: "mittel",
    question: "Was prüfen Sie bei einem Funkgerät vor Dienstbeginn?",
    sampleAnswer: "Ich prüfe den äußeren Zustand, Akku oder Stromversorgung, Antenne, Kanal beziehungsweise Einstellung, Lautstärke, Funktionstest und Erreichbarkeit. Störungen melde ich nach Dienstanweisung.",
    examinerNote: "Praktische Antwort: Akku, Antenne, Kanal, Funktionstest, Meldung bei Störung.",
    tags: ["funkgerät", "technik", "dienstbeginn"],
    sourceType: "accaoui_original",
    sheetRefs: ["oral_sheet_a_v2340"]
  }
];

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
