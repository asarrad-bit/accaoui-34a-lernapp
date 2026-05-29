/* =====================================================
   v23.4.0 MÜNDLICHE PRÜFUNG – PRÜFUNGSBOGEN-MODUL
   Ziel:
   - Prüfungsbögen als eigenes Modul
   - 3 Prüfer × 5 Fragen
   - eigene Accaoui-Trainingsfragen, keine Original-IHK-Fragen
===================================================== */

const ORAL_EXAM_SHEET_A_V2340 = {
  id: "oral_sheet_a_v2340",
  title: "Prüfungsbogen A",
  durationMinutes: 15,
  note: "Trainingsbogen. Keine offizielle IHK-Prüfung.",
  blocks: [
    {
      examinerIndex: 0,
      examinerName: "Prüfer 1",
      title: "Öffentliches Recht / Gewerberecht",
      questions: [
        {
          id: "oral_a_001",
          category: "Recht der öffentlichen Sicherheit und Ordnung",
          question: "Welche Rechte hat ein privater Sicherheitsmitarbeiter im Vergleich zur Polizei grundsätzlich nicht?",
          sampleAnswer: "Ein privater Sicherheitsmitarbeiter hat grundsätzlich keine hoheitlichen Polizeibefugnisse. Er darf nicht wie ein Polizeibeamter Platzverweise im öffentlichen Raum aussprechen, Personen ohne Rechtsgrund durchsuchen oder staatliche Zwangsmaßnahmen durchführen. Er handelt vor allem auf Grundlage von Hausrecht, Jedermannsrechten und privatrechtlichen Befugnissen.",
          examinerNote: "Wichtig ist die klare Trennung zwischen staatlicher Hoheitsgewalt und privatem Sicherheitsdienst."
        },
        {
          id: "oral_a_002",
          category: "Recht der öffentlichen Sicherheit und Ordnung",
          question: "Was versteht man unter öffentlicher Sicherheit?",
          sampleAnswer: "Öffentliche Sicherheit umfasst den Schutz der Rechtsordnung, des Staates und seiner Einrichtungen sowie den Schutz individueller Rechtsgüter wie Leben, Gesundheit, Freiheit und Eigentum.",
          examinerNote: "Gute Antwort nennt Rechtsordnung, Staat und Individualrechtsgüter."
        },
        {
          id: "oral_a_003",
          category: "Gewerberecht",
          question: "Warum ist § 34a GewO für das Bewachungsgewerbe wichtig?",
          sampleAnswer: "§ 34a GewO regelt den gewerberechtlichen Zugang zum Bewachungsgewerbe. Er betrifft insbesondere die Erlaubnis, die Zuverlässigkeit und die erforderlichen Nachweise wie Unterrichtung oder Sachkundeprüfung je nach Tätigkeit.",
          examinerNote: "Wichtig: § 34a GewO ist keine Polizeibefugnis, sondern eine gewerberechtliche Vorschrift."
        },
        {
          id: "oral_a_004",
          category: "Gewerberecht",
          question: "Welche Bedeutung hat die Zuverlässigkeit im Bewachungsgewerbe?",
          sampleAnswer: "Zuverlässigkeit ist eine zentrale Voraussetzung. Wer unzuverlässig ist, kann von der Tätigkeit ausgeschlossen werden oder eine Erlaubnis kann versagt beziehungsweise widerrufen werden. Hintergrund ist, dass Sicherheitsmitarbeiter mit fremden Rechtsgütern und sensiblen Situationen umgehen.",
          examinerNote: "Gute Antwort verbindet Zuverlässigkeit mit Vertrauen, Gefahrennähe und behördlicher Kontrolle."
        },
        {
          id: "oral_a_005",
          category: "Gewerberecht",
          question: "Welche Pflichten bestehen beim Dienstausweis im Bewachungsgewerbe?",
          sampleAnswer: "Der Dienstausweis dient der Legitimation im Dienst. Je nach Tätigkeit muss er mitgeführt und zuständigen Personen oder Behörden auf Verlangen vorgezeigt werden. Er darf nicht den Eindruck eines amtlichen oder hoheitlichen Ausweises erwecken.",
          examinerNote: "Wichtig ist: Dienstausweis ja, aber keine Verwechslung mit Polizei oder Behörde."
        }
      ]
    },
    {
      examinerIndex: 1,
      examinerName: "Vorsitz",
      title: "Umgang mit Menschen",
      questions: [
        {
          id: "oral_a_006",
          category: "Umgang mit Menschen",
          question: "Warum ist professioneller Umgang mit Menschen im Sicherheitsdienst besonders wichtig?",
          sampleAnswer: "Sicherheitsmitarbeiter haben häufig Kontakt mit Menschen in angespannten Situationen. Professionelles Verhalten hilft, Konflikte zu vermeiden, deeskalierend zu handeln, den Auftrag sicher zu erfüllen und das Ansehen des Auftraggebers zu schützen.",
          examinerNote: "Gute Antwort nennt Professionalität, Deeskalation, Auftraggeber und Eigenschutz."
        },
        {
          id: "oral_a_007",
          category: "Umgang mit Menschen",
          question: "Wie reagieren Sie, wenn eine Person Sie provoziert oder beleidigt?",
          sampleAnswer: "Ich bleibe ruhig, lasse mich nicht provozieren, halte Sicherheitsabstand, spreche sachlich und klar. Ich setze Grenzen, hole bei Bedarf Unterstützung und handle nach Dienstanweisung. Ich antworte nicht mit Beleidigungen.",
          examinerNote: "Prüfer achten auf Ruhe, Distanz, klare Kommunikation und keine Gegenprovokation."
        },
        {
          id: "oral_a_008",
          category: "Umgang mit Menschen",
          question: "Was bedeutet Deeskalation in der Praxis?",
          sampleAnswer: "Deeskalation bedeutet, eine angespannte Situation durch ruhiges, kontrolliertes und respektvolles Verhalten zu beruhigen. Dazu gehören Abstand, klare Sprache, aktives Zuhören, keine Provokation und rechtzeitiges Hinzuziehen von Unterstützung.",
          examinerNote: "Wichtig ist praktisches Verhalten, nicht nur das Wort Deeskalation."
        },
        {
          id: "oral_a_009",
          category: "Umgang mit Menschen",
          question: "Welche Rolle spielt Körpersprache im Sicherheitsdienst?",
          sampleAnswer: "Körpersprache wirkt auf andere Menschen oft stärker als Worte. Eine offene, ruhige und sichere Haltung kann deeskalierend wirken. Drohende Gesten, zu nahes Herantreten oder hektische Bewegungen können dagegen eskalieren.",
          examinerNote: "Gute Antwort nennt Wirkung, Distanz, Haltung und Eskalationsgefahr."
        },
        {
          id: "oral_a_010",
          category: "Umgang mit Menschen",
          question: "Was beachten Sie bei Jugendlichen in Konfliktsituationen?",
          sampleAnswer: "Ich bleibe sachlich, respektvoll und klar. Ich vermeide Bloßstellung, behandle Jugendliche nicht herablassend und achte auf Gruppendynamik. Gleichzeitig setze ich klare Grenzen und sichere mich ab.",
          examinerNote: "Wichtig sind Gruppendynamik, Respekt, klare Grenzen und Eigensicherung."
        }
      ]
    },
    {
      examinerIndex: 2,
      examinerName: "Prüfer 3",
      title: "Mischblock Datenschutz / BGB / Strafrecht / UVV / Waffen / Technik",
      questions: [
        {
          id: "oral_a_011",
          category: "Datenschutzrecht",
          question: "Was sind personenbezogene Daten?",
          sampleAnswer: "Personenbezogene Daten sind Informationen, die sich auf eine identifizierte oder identifizierbare natürliche Person beziehen. Beispiele sind Name, Anschrift, Telefonnummer, Ausweisnummer, Bildaufnahmen oder Besucherdaten.",
          examinerNote: "Gute Antwort nennt die identifizierte oder identifizierbare Person und Beispiele."
        },
        {
          id: "oral_a_012",
          category: "Bürgerliches Gesetzbuch",
          question: "Was kann ein Sicherheitsmitarbeiter auf Grundlage des Hausrechts tun?",
          sampleAnswer: "Er kann im Auftrag des Hausrechtsinhabers Personen ansprechen, auf Regeln hinweisen, zum Verlassen auffordern oder ein Hausverbot durchsetzen, soweit dies rechtlich zulässig und verhältnismäßig ist.",
          examinerNote: "Wichtig: Hausrecht ist nicht grenzenlos und ersetzt keine Polizeibefugnisse."
        },
        {
          id: "oral_a_013",
          category: "Straf- und Strafverfahrensrecht",
          question: "Wann kann eine vorläufige Festnahme durch Jedermann in Betracht kommen?",
          sampleAnswer: "Sie kann in Betracht kommen, wenn jemand auf frischer Tat betroffen oder verfolgt wird und Fluchtverdacht besteht oder die Identität nicht sofort festgestellt werden kann. Die Polizei muss unverzüglich hinzugezogen werden.",
          examinerNote: "Wichtig sind frische Tat, Fluchtverdacht oder Identitätsfeststellung und unverzügliche Polizei."
        },
        {
          id: "oral_a_014",
          category: "Unfallverhütungsvorschrift",
          question: "Warum ist Eigenschutz im Sicherheitsdienst so wichtig?",
          sampleAnswer: "Eigenschutz ist wichtig, weil Sicherheitsmitarbeiter Gefahren erkennen, vermeiden und kontrolliert handeln müssen. Sie sollen sich nicht unnötig selbst gefährden und bei Bedarf Unterstützung anfordern.",
          examinerNote: "Gute Antwort verbindet Eigenschutz, Gefährdung, Unterstützung und professionelles Verhalten."
        },
        {
          id: "oral_a_015",
          category: "Grundzüge der Sicherheitstechnik",
          question: "Was prüfen Sie bei einem Funkgerät vor Dienstbeginn?",
          sampleAnswer: "Ich prüfe den äußeren Zustand, Akku oder Stromversorgung, Antenne, Kanal beziehungsweise Einstellung, Lautstärke, Funktionstest und Erreichbarkeit. Störungen melde ich nach Dienstanweisung.",
          examinerNote: "Praktische Antwort: Akku, Antenne, Kanal, Funktionstest, Meldung bei Störung."
        }
      ]
    }
  ]
};

function getOralSheetAQuestionsV2340() {
  return ORAL_EXAM_SHEET_A_V2340.blocks.flatMap(block => {
    return block.questions.map(question => ({
      ...question,
      sheetId: ORAL_EXAM_SHEET_A_V2340.id,
      sheetTitle: ORAL_EXAM_SHEET_A_V2340.title,
      examinerIndex: block.examinerIndex,
      examinerName: block.examinerName,
      examinerBlockTitle: block.title
    }));
  });
}

function listSheetsV2340() {
  const sheet = ORAL_EXAM_SHEET_A_V2340;
  return [{
    id: sheet.id,
    title: sheet.title,
    durationMinutes: sheet.durationMinutes,
    note: sheet.note,
    questionCount: getOralSheetAQuestionsV2340().length
  }];
}

window.AccaouiOralSheets = {
  getSheetA() {
    return ORAL_EXAM_SHEET_A_V2340;
  },

  getSheetAQuestions() {
    return getOralSheetAQuestionsV2340();
  },

  listSheets() {
    return listSheetsV2340();
  }
};

window.ORAL_EXAM_SHEET_A_V2340 = ORAL_EXAM_SHEET_A_V2340;
window.getOralSheetAQuestionsV2340 = getOralSheetAQuestionsV2340;
