/* =====================================================
   ACCAOUI §34a LERN-APP
   oral-sheets-v23.js
   v23.0 MÜNDLICHE PRÜFUNG – TRAININGSBOGEN-DATENSTRUKTUR
   Hinweis:
   - noch nicht in die App eingebunden
   - keine offiziellen IHK-Fragen
   - nur Platzhalter für zukünftige Accaoui-Trainingsbögen
===================================================== */

const ACCAOUI_ORAL_SHEETS_V23 = {
  meta: {
    version: "v23.0",
    app: "Accaoui §34a Lern-App",
    module: "oral_exam",
    legalNotice: "Trainingsbeispiele. Keine offizielle IHK-Prüfung.",
    ratingNotice: "Trainingsbewertung. Keine offizielle IHK-Bewertung.",
    sourceStyle: "accaoui_original",
    storageReady: true,
    supabaseReady: true
  },

  examinerRoles: [
    {
      id: "examiner_1",
      name: "Prüfer 1",
      focus: "Recht / Gewerberecht"
    },
    {
      id: "chair",
      name: "Vorsitz",
      focus: "Umgang mit Menschen"
    },
    {
      id: "examiner_3",
      name: "Prüfer 3",
      focus: "Mischblock"
    }
  ],

  sheets: [
    {
      id: "oral_sheet_a_v23",
      title: "Prüfungsbogen A",
      status: "active",
      questions: []
    },
    {
      id: "oral_sheet_b_v23",
      title: "Prüfungsbogen B",
      status: "draft",
      questions: [
        {
          id: "oral-b-001",
          mode: "oral",
          sheet: "B",
          order: 1,
          examinerBlock: 1,
          examinerRole: "Prüfer 1",
          topic: "Recht der öffentlichen Sicherheit und Ordnung",
          subtopic: "Öffentliches Recht / Privatrecht",
          examinerQuestion: "Stellen Sie sich vor: Sie stehen am Eingang eines Einkaufszentrums. Ein Besucher fragt, warum Sie ihn ansprechen dürfen, obwohl Sie kein Polizist sind. Erklären Sie mir den Unterschied zwischen öffentlichem Recht und Privatrecht – und wo der Bewachungsmitarbeiter rechtlich einzuordnen ist.",
          modelAnswer: "Öffentliches Recht regelt das Verhältnis zwischen Staat und Bürger, etwa Polizei- und Ordnungsrecht. Privatrecht regelt das Verhältnis zwischen Privaten untereinander, vor allem im BGB. Der Bewachungsmitarbeiter handelt grundsätzlich im privaten Auftrag des Hausrechtsinhabers. Er hat keine hoheitlichen Befugnisse wie die Polizei, sondern nur die Rechte, die ihm der Auftraggeber im Rahmen des Hausrechts überträgt.",
          followUpQuestions: [
            "Darf ein Sicherheitsmitarbeiter allein wegen Hausordnungsverstoßes festhalten?",
            "Was ist der wichtigste Unterschied zu polizeilichen Maßnahmen?",
            "Nennen Sie ein Beispiel für eine rein private Rechtsbeziehung im Einsatz."
          ],
          examinerNotes: "Prüfen, ob der Kandidat Staat/Bürger von Privat/Privat trennt und keine hoheitlichen Befugnisse zuschreibt.",
          criticalMistakes: [
            "Sicherheitsmitarbeiter mit Polizeibefugnissen gleichsetzen",
            "Hausrecht als öffentlich-rechtliche Vollmacht darstellen",
            "Ohne Auftraggebervorgabe eigenmächtig hoheitlich handeln wollen",
            "Privatrechtliche Maßnahmen ohne rechtliche Grenze erklären"
          ],
          difficulty: "medium",
          examRelevance: "high",
          ihkSimilarityRisk: "low",
          sourceStyle: "accaoui_original"
        },
        {
          id: "oral-b-002",
          mode: "oral",
          sheet: "B",
          order: 2,
          examinerBlock: 1,
          examinerRole: "Prüfer 1",
          topic: "Recht der öffentlichen Sicherheit und Ordnung",
          subtopic: "Grundrechte / Gewaltmonopol",
          examinerQuestion: "Im Objekt wird eine Person lautstark kontrolliert. Sie beruft sich auf die Freiheit der Person. Wie erklären Sie mir, welche Grundrechte hier relevant sein können – und warum das staatliche Gewaltmonopol für Ihr Handeln als Bewacher wichtig ist?",
          modelAnswer: "Relevant können vor allem Art. 2 Abs. 2 GG (körperliche Unversehrtheit), Art. 1 GG (Menschenwürde) und Art. 5 GG (Meinungsfreiheit) sein. Das Gewaltmonopol liegt beim Staat: physische Zwangsmaßnahmen sind grundsätzlich Polizei vorbehalten. Der Bewacher darf nur im engen Rahmen privatrechtlich und strafrechtlich zulässiger Notwehr oder bei frischer Tat festhalten – nicht eigenmächtig „Strafe“ durchsetzen.",
          followUpQuestions: [
            "Darf ein Bewacher jemanden wegen Beleidigung festbinden?",
            "Was bedeutet Gewaltmonopol praktisch im Alltagseinsatz?",
            "Welches Grundrecht schützt vor willkürlicher Körperkontrolle?"
          ],
          examinerNotes: "Grundrechte benennen und Grenzen privater Gewaltanwendung klar darstellen.",
          criticalMistakes: [
            "Eigenmächtige Strafen oder Bestrafung im Objekt",
            "Grundrechte als für Bewacher irrelevant abtun",
            "Gewaltmonopol missverstehen und polizeiliche Befugnisse übernehmen",
            "Freiheitsentziehung ohne rechtfertigenden Tatbestand"
          ],
          difficulty: "medium",
          examRelevance: "high",
          ihkSimilarityRisk: "low",
          sourceStyle: "accaoui_original"
        },
        {
          id: "oral-b-003",
          mode: "oral",
          sheet: "B",
          order: 3,
          examinerBlock: 1,
          examinerRole: "Prüfer 1",
          topic: "Gewerberecht",
          subtopic: "§ 34a GewO / Bewachungsgewerbe",
          examinerQuestion: "Sie möchten als Unternehmer Wach- und Sicherheitsdienste anbieten. Was regelt § 34a GewO für dieses Gewerbe – und welche grundlegenden Pflichten ergeben sich daraus für den Betrieb?",
          modelAnswer: "§ 34a GewO regelt das Bewachungsgewerbe. Wer gewerbsmäßig Leben oder Eigentum fremder Personen bewachen will, braucht eine Erlaubnis der zuständigen Behörde. Dafür werden unter anderem Zuverlässigkeit, geordnete wirtschaftliche Verhältnisse und fachliche Voraussetzungen geprüft. Der Betrieb muss nur geeignete und entsprechend qualifizierte Wachpersonen einsetzen und die gesetzlichen Vorgaben einhalten.",
          followUpQuestions: [
            "Wer braucht die Erlaubnis nach § 34a GewO: der Unternehmer oder die einzelne Wachperson?",
            "Welche Rolle spielt die Zuverlässigkeit bei der Erlaubnis?",
            "Was passiert bei fehlender Erlaubnis?"
          ],
          examinerNotes: "Erlaubnispflicht, Zuverlässigkeit und gewerbsmäßige Beaufsichtigung verknüpfen.",
          criticalMistakes: [
            "Bewachung ohne erforderliche Erlaubnis anbieten",
            "§ 34a GewO mit Sachkundeprüfung verwechseln",
            "Unzuverlässige Personen einsetzen",
            "Kontroll-/Beaufsichtigungstätigkeit als „normaler Job“ ohne Gewerbeerlaubnis behandeln"
          ],
          difficulty: "medium",
          examRelevance: "high",
          ihkSimilarityRisk: "low",
          sourceStyle: "accaoui_original"
        },
        {
          id: "oral-b-004",
          mode: "oral",
          sheet: "B",
          order: 4,
          examinerBlock: 1,
          examinerRole: "Prüfer 1",
          topic: "Gewerberecht",
          subtopic: "Sachkunde / Unterrichtung / Einsatzbereiche",
          examinerQuestion: "In Ihrem Team arbeiten Mitarbeiter in unterschiedlichen Bereichen: Revierdienst, Einzelhandel und Veranstaltungsschutz. Erklären Sie den Unterschied zwischen Sachkundeprüfung und Unterrichtung – und welche Qualifikation für welchen Einsatzbereich typischerweise nötig ist.",
          modelAnswer: "Die Unterrichtung vermittelt grundlegende Rechte, Pflichten und Befugnisse für Bewachungsaufgaben. Die Sachkundeprüfung ist der strengere Nachweis und wird für bestimmte Tätigkeiten verlangt, zum Beispiel Kontrollgänge im öffentlichen Verkehrsraum oder in Hausrechtsbereichen mit tatsächlich öffentlichem Verkehr, Schutz vor Ladendieben, Eingangskontrollen bei gastgewerblichen Diskotheken sowie bestimmte leitende Tätigkeiten. Entscheidend ist immer der konkrete Einsatzbereich.",
          followUpQuestions: [
            "Welche Tätigkeiten verlangen zwingend die Sachkundeprüfung statt nur Unterrichtung?",
            "Wer entscheidet, welche Qualifikation im Objekt nötig ist?",
            "Was ist der Zweck der Sachkundeprüfung?"
          ],
          examinerNotes: "Qualifikationsstufen und Einsatzbezug erklären, nicht pauschal „reicht Unterrichtung“.",
          criticalMistakes: [
            "Unqualifiziertes Personal in anspruchsvollen Einsätzen einsetzen",
            "Sachkunde und Unterrichtung verwechseln",
            "Qualifikation nicht an Einsatzart anpassen",
            "Ausbildungsnachweis im Einsatz nicht mitführen bzw. nicht vorlegen können"
          ],
          difficulty: "medium",
          examRelevance: "high",
          ihkSimilarityRisk: "low",
          sourceStyle: "accaoui_original"
        },
        {
          id: "oral-b-005",
          mode: "oral",
          sheet: "B",
          order: 5,
          examinerBlock: 1,
          examinerRole: "Prüfer 1",
          topic: "Bürgerliches Gesetzbuch",
          subtopic: "Hausrecht / Besitzdiener / Befugnisse",
          examinerQuestion: "Ein Besucher weigert sich, das Gelände zu verlassen, obwohl der Filialleiter ihn aus dem Markt verweisen ließ. Was ist Hausrecht – und welche Befugnisse haben Sie als Besitzdiener in dieser Situation?",
          modelAnswer: "Hausrecht ist das Recht des Inhabers der tatsächlichen Gewalt über ein Grundstück oder Geschäft, über Zutritt und Verweilen zu bestimmen. Als Besitzdiener handele ich im Auftrag des Hausrechtsinhabers. Ich darf Personen zutrittsverweigern oder verweisen und bei Notwehr oder frischer Tat bis zum Eintreffen der Polizei festhalten. Ich darf nicht eigenmächtig durchsuchen, bestrafen oder Gewalt anwenden, wenn keine rechtfertigende Situation vorliegt.",
          followUpQuestions: [
            "Dürfen Sie die Tasche einer Person kontrollieren?",
            "Was tun Sie, wenn der Verwiesene physisch Widerstand leistet?",
            "Wer erteilt Ihnen die Weisung zum Hausverweis?"
          ],
          examinerNotes: "Hausrecht von Strafrecht und polizeilichen Befugnissen abgrenzen.",
          criticalMistakes: [
            "Eigenmächtige Durchsuchung von Taschen oder Fahrzeugen",
            "Verweis ohne Weisung des Hausrechtsinhabers",
            "Gewaltanwendung außerhalb von Notwehr oder Zuführung",
            "Festhalten ohne rechtfertigenden Anlass über längere Zeit"
          ],
          difficulty: "medium",
          examRelevance: "high",
          ihkSimilarityRisk: "low",
          sourceStyle: "accaoui_original"
        },
        {
          id: "oral-b-006",
          mode: "oral",
          sheet: "B",
          order: 6,
          examinerBlock: 2,
          examinerRole: "Vorsitz",
          topic: "Umgang mit Menschen",
          subtopic: "Deeskalation",
          examinerQuestion: "Stellen Sie sich vor: Vor dem Eingang eines Clubs wird ein Gast laut, schreit und droht Ihnen. Wie gehen Sie in den ersten zwei Minuten vor, um die Situation zu deeskalieren?",
          modelAnswer: "Ich halte Abstand, bleibe ruhig und stelle eine klare, respektvolle Kommunikation her. Ich spiegle das Anliegen kurz, setze eine Grenze und biete eine Lösung an, z. B. kurzes Gespräch abseits oder Einholung der Leitung. Ich vermeide Drohungen, Beleidigungen und unnötige Körpernähe. Parallel informiere ich die Einsatzleitung und bereite bei Gefahr die Alarmierung der Polizei vor.",
          followUpQuestions: [
            "Wann brechen Sie das Gespräch ab?",
            "Welche Körpersprache vermeiden Sie bewusst?",
            "Wie dokumentieren Sie die Situation?"
          ],
          examinerNotes: "Strukturierte Deeskalation: Abstand, Ruhe, Grenze, Eskalationsstopp, Meldeweg.",
          criticalMistakes: [
            "Provokatives oder herablassendes Verhalten",
            "Sofortige körperliche Auseinandersetzung ohne Vorwarnung",
            "Allein in unübersichtliche Situation gehen",
            "Keine Weisung oder Dokumentation bei drohender Gewalt"
          ],
          difficulty: "medium",
          examRelevance: "high",
          ihkSimilarityRisk: "low",
          sourceStyle: "accaoui_original"
        },
        {
          id: "oral-b-007",
          mode: "oral",
          sheet: "B",
          order: 7,
          examinerBlock: 2,
          examinerRole: "Vorsitz",
          topic: "Umgang mit Menschen",
          subtopic: "Kommunikation",
          examinerQuestion: "Sie sollen eine ältere Besucherin ansprechen, die den Notausgang blockiert. Wie sprechen Sie sie an – und worauf achten Sie bei Ihrer Kommunikation?",
          modelAnswer: "Ich spreche die Person höflich und klar an, nenne meinen Dienst und den konkreten Grund: Sicherheitsregel am Notausgang. Ich verwende einfache Sprache, halte Blickkontakt auf Augenhöhe und gebe eine kurze Handlungsanweisung, z. B. „Bitte treten Sie einen Schritt zur Seite.“ Danach bedanke ich mich und prüfe, ob sie Hilfe braucht.",
          followUpQuestions: [
            "Wie reagieren Sie, wenn die Person genervt reagiert?",
            "Warum ist der konkrete Grund wichtig?",
            "Was vermeiden Sie in der Ansprache?"
          ],
          examinerNotes: "Höflich, sachlich, lösungsorientiert – keine Belehrung oder Herabsetzung.",
          criticalMistakes: [
            "Beleidigende oder autoritäre Ansprache",
            "Keinen Grund für die Anweisung nennen",
            "Lautstarkes Anfahren vor Publikum",
            "Kommunikation ohne deeskalierende Körpersprache"
          ],
          difficulty: "easy",
          examRelevance: "high",
          ihkSimilarityRisk: "low",
          sourceStyle: "accaoui_original"
        },
        {
          id: "oral-b-008",
          mode: "oral",
          sheet: "B",
          order: 8,
          examinerBlock: 2,
          examinerRole: "Vorsitz",
          topic: "Umgang mit Menschen",
          subtopic: "Aggressives Verhalten",
          examinerQuestion: "Ein Mann schlägt mit der Faust gegen eine Glasscheibe und schreit Mitarbeiter an. Beschreiben Sie mir Ihr Vorgehen bei aggressivem Verhalten – von der ersten Wahrnehmung bis zur Übergabe an die Polizei.",
          modelAnswer: "Ich sichere zuerst meine eigene Sicherheit und die der Anwesenden, halte Abstand und alarmiere die Einsatzleitung sowie bei Bedarf die Polizei. Ich setze klare verbale Grenzen und versuche Deeskalation. Wenn eine Straftat oder unmittelbare Gefahr vorliegt, darf ich bei frischer Tat festhalten oder in Notwehr handeln. Ich dokumentiere Beobachtungen sachlich und übergebe die Person unverzüglich der Polizei.",
          followUpQuestions: [
            "Wann ist Festhalten bei frischer Tat gerechtfertigt?",
            "Was tun Sie, wenn mehrere aggressive Personen beteiligt sind?",
            "Welche Angaben sind für die Polizei wichtig?"
          ],
          examinerNotes: "Eigenschutz, Meldeweg, rechtmäßige Grenzen der Festhaltung betonen.",
          criticalMistakes: [
            "Unnötige Eskalation durch Provokation",
            "Festhalten ohne frische Tat oder Notwehrsituation",
            "Fehlende Alarmierung bei Gefahr",
            "Keine Dokumentation von Tatzeit, Ort und Verhalten"
          ],
          difficulty: "medium",
          examRelevance: "high",
          ihkSimilarityRisk: "low",
          sourceStyle: "accaoui_original"
        },
        {
          id: "oral-b-009",
          mode: "oral",
          sheet: "B",
          order: 9,
          examinerBlock: 2,
          examinerRole: "Vorsitz",
          topic: "Umgang mit Menschen",
          subtopic: "Interkulturelles Verhalten",
          examinerQuestion: "Eine Besucherin trägt Kopftuch, spricht gebrochen Deutsch und wirkt unsicher an der Kontrolle. Wie gehen Sie interkulturell sensibel vor, ohne Sicherheitsstandards aufzuweichen?",
          modelAnswer: "Ich bleibe respektvoll, geduldig und sachlich. Ich erkläre den Kontrollgrund einfach, spreche langsam und deutlich und nutze bei Bedarf eine verständliche Geste oder hole Hilfe einer Kollegin. Religiöse oder kulturelle Merkmale bewerte ich nicht negativ. Sicherheitsregeln gelten für alle gleich, aber der Umgang bleibt würdevoll und diskriminierungsfrei.",
          followUpQuestions: [
            "Was wäre diskriminierendes Verhalten?",
            "Wie holen Sie eine Dolmetschhilfe?",
            "Wie erklären Sie eine Regel ohne Belehrungston?"
          ],
          examinerNotes: "Gleiche Sicherheitsstandards plus respektvoller, würdevoller Umgang.",
          criticalMistakes: [
            "Diskriminierende Kommentare oder Auswahl bei Kontrollen",
            "Sicherheitsregeln wegen kultureller Symbole aussetzen",
            "Herablassende Körpersprache oder Hohn",
            "Unnötige öffentliche Bloßstellung"
          ],
          difficulty: "medium",
          examRelevance: "medium",
          ihkSimilarityRisk: "low",
          sourceStyle: "accaoui_original"
        },
        {
          id: "oral-b-010",
          mode: "oral",
          sheet: "B",
          order: 10,
          examinerBlock: 2,
          examinerRole: "Vorsitz",
          topic: "Umgang mit Menschen",
          subtopic: "Beschwerde / professionelle Rolle",
          examinerQuestion: "Ein Kunde beschwert sich lautstark, dass Sie ihn „bevormundet“ haben. Wie reagieren Sie professionell – und wann ziehen Sie die Einsatzleitung hinzu?",
          modelAnswer: "Ich lasse den Kunden ausreden, bleibe sachlich und erkläre kurz meinen Sicherheitsauftrag. Ich entschuldige mich nicht für rechtmäßiges Handeln, aber ich bleibe höflich. Bei wiederholter Beleidigung, Drohung oder wenn keine Lösung möglich ist, ziehe ich die Einsatzleitung oder den Auftraggeber hinzu und dokumentiere den Vorfall.",
          followUpQuestions: [
            "Was schreiben Sie in den Einsatzbericht?",
            "Wann beenden Sie das Gespräch?",
            "Wie bleiben Sie neutral, ohne schwach zu wirken?"
          ],
          examinerNotes: "Professionelle Rolle: ruhig, dokumentiert, Weisungskette nutzen.",
          criticalMistakes: [
            "Beleidigender Gegenangriff",
            "Privates Diskussionsniveau statt Dienstrolle",
            "Keine Dokumentation bei Konflikten",
            "Einsatzleitung zu spät informieren"
          ],
          difficulty: "medium",
          examRelevance: "high",
          ihkSimilarityRisk: "low",
          sourceStyle: "accaoui_original"
        },
        {
          id: "oral-b-011",
          mode: "oral",
          sheet: "B",
          order: 11,
          examinerBlock: 3,
          examinerRole: "Prüfer 3",
          topic: "Datenschutzrecht",
          subtopic: "Personenbezogene Daten / DSGVO",
          examinerQuestion: "Sie filmen am Empfang zur Diebstahlprävention und speichern Besucherlisten mit Namen und Kennzeichen. Welche datenschutzrechtlichen Grundsätze müssen Sie beachten?",
          modelAnswer: "Personenbezogene Daten dürfen nur mit Rechtsgrundlage, zweckgebunden und datensparsam verarbeitet werden. Videoüberwachung braucht eine Hinweisbeschilderung und muss verhältnismäßig sein. Besucherlisten dürfen nur so lange gespeichert werden, wie es für den Zweck nötig ist. Betroffene haben Rechte, z. B. Auskunft. Der Auftraggeber ist in der Regel Verantwortlicher, ich handle nach Weisung und internen Vorgaben.",
          followUpQuestions: [
            "Dürfen Sie Aufnahmen privat weiterleiten?",
            "Was bedeutet Datensparsamkeit im Schichtbetrieb?",
            "Wer ist typischerweise Verantwortlicher?"
          ],
          examinerNotes: "Zweckbindung, Rechtsgrundlage, Löschfristen und Weisungsbindung nennen.",
          criticalMistakes: [
            "Weitergabe von Kamera- oder Listendaten an Dritte",
            "Speicherung ohne Zweck und Löschkonzept",
            "Fehlende Hinweise bei Videoüberwachung",
            "Daten auf privaten Handys sichern"
          ],
          difficulty: "medium",
          examRelevance: "high",
          ihkSimilarityRisk: "low",
          sourceStyle: "accaoui_original"
        },
        {
          id: "oral-b-012",
          mode: "oral",
          sheet: "B",
          order: 12,
          examinerBlock: 3,
          examinerRole: "Prüfer 3",
          topic: "Straf- und Strafverfahrensrecht",
          subtopic: "Notwehr / Festnahme / Straftat",
          examinerQuestion: "Sie sehen, wie jemand im Laden eine Flasche in die Tasche steckt und zur Tür geht. Was ist eine frische Tat – und wann dürfen Sie die Person festhalten? Was ist Notwehr in diesem Zusammenhang?",
          modelAnswer: "Eine frische Tat liegt vor, wenn die Person bei der Tat oder unmittelbar danach betroffen oder verfolgt wird. Nach § 127 Abs. 1 StPO darf eine Person nur vorläufig festgehalten werden, wenn zusätzlich Fluchtverdacht besteht oder die Identität nicht sofort festgestellt werden kann. Die Polizei ist unverzüglich zu informieren. Notwehr ist die erforderliche Verteidigung gegen einen gegenwärtigen rechtswidrigen Angriff. Beim Ladendiebstahl muss ich Festnahme, Notwehr und bloßen Verdacht klar trennen: Bei bloßem Verdacht ohne frische Tat darf ich niemanden eigenmächtig festhalten.",
          followUpQuestions: [
            "Wie lange darf die Festhaltung dauern?",
            "Was tun Sie bei Widerstand?",
            "Welche Straftat kann Ladendiebstahl sein?"
          ],
          examinerNotes: "Frische Tat, Zuführungsrecht und Notwehr sauber trennen.",
          criticalMistakes: [
            "Festhalten Stunden später ohne Polizei",
            "Durchsuchung oder Beschlagnahme eigenmächtig",
            "Körperliche Gewalt ohne Notwehrgrund",
            "Verwechslung von Verdacht und frischer Tat"
          ],
          difficulty: "hard",
          examRelevance: "high",
          ihkSimilarityRisk: "low",
          sourceStyle: "accaoui_original"
        },
        {
          id: "oral-b-013",
          mode: "oral",
          sheet: "B",
          order: 13,
          examinerBlock: 3,
          examinerRole: "Prüfer 3",
          topic: "Unfallverhütungsvorschrift Wach- und Sicherungsdienste",
          subtopic: "Eigenschutz / Dienstverhalten / Arbeitssicherheit",
          examinerQuestion: "Bei einer nächtlichen Kontrolle auf dem Werksgelände stolpern Sie fast über lose Kabel am Weg. Welche Pflichten aus der UVV für Wach- und Sicherungsdienste betreffen Eigenschutz und sicheres Dienstverhalten?",
          modelAnswer: "Ich muss Gefahren für mich und andere erkennen, melden und wenn möglich beseitigen oder absichern. Dazu gehören sichere Wege, Beleuchtung, PSA nach Vorgabe und Einhaltung der Betriebsanweisungen. Eigenschutz heißt: nicht allein in unklare Gefahrenlagen gehen, Funk bereithalten und Weisungen der Einsatzleitung befolgen. Unfälle und Beinahe-Unfälle dokumentiere ich und melde sie.",
          followUpQuestions: [
            "Welche PSA kann im Revierdienst nötig sein?",
            "Was tun Sie bei Beinahe-Unfall?",
            "Dürfen Sie allein in einen gesperrten Bereich?"
          ],
          examinerNotes: "UVV-Grundhaltung: erkennen, melden, absichern, dokumentieren.",
          criticalMistakes: [
            "Gefahrenlage ohne Meldung betreten",
            "Fehlende PSA trotz Vorgabe",
            "Beinahe-Unfall nicht dokumentieren",
            "Alleinige Gefahrenbereinigung ohne Absicherung"
          ],
          difficulty: "medium",
          examRelevance: "high",
          ihkSimilarityRisk: "low",
          sourceStyle: "accaoui_original"
        },
        {
          id: "oral-b-014",
          mode: "oral",
          sheet: "B",
          order: 14,
          examinerBlock: 3,
          examinerRole: "Prüfer 3",
          topic: "Grundzüge des Waffenrechts",
          subtopic: "Verbotene Gegenstände / Waffenfund",
          examinerQuestion: "Bei der Einlasskontrolle entdecken Sie ein Klappmesser mit feststellbarer Klinge in der Tasche eines Gastes. Wie gehen Sie rechtlich und praktisch vor, ohne Ihre Befugnisse zu überschreiten?",
          modelAnswer: "Ich behandle den Gegenstand zunächst als sicherheitsrelevant und beachte Hausordnung, Veranstaltungsregeln und Gefahrenlage. Ich weise den Gast sachlich darauf hin, dass der Zutritt mit diesem Gegenstand verweigert werden kann. Eigenmächtig beschlagnahmen oder weiter durchsuchen darf ich nicht. Bei konkreter Gefahr oder Verdacht auf einen verbotenen Gegenstand informiere ich Einsatzleitung und Polizei. Den Vorgang dokumentiere ich.",
          followUpQuestions: [
            "Darf das Messer einbehalten werden?",
            "Was ist der Unterschied zu erlaubten Gebrauchsmessern?",
            "Wann ist Polizei sofort nötig?"
          ],
          examinerNotes: "Zutrittsverweigerung ja – eigenmächtige Beschlagnahme nein.",
          criticalMistakes: [
            "Eigenmächtige Beschlagnahme des Messers",
            "Zutritt trotz sicherheitsrelevantem oder laut Hausordnung untersagtem Gegenstand erlauben",
            "Gegenstand ohne Dokumentation behalten",
            "Unnötige Körperkontrolle über Hausrecht hinaus"
          ],
          difficulty: "medium",
          examRelevance: "medium",
          ihkSimilarityRisk: "low",
          sourceStyle: "accaoui_original"
        },
        {
          id: "oral-b-015",
          mode: "oral",
          sheet: "B",
          order: 15,
          examinerBlock: 3,
          examinerRole: "Prüfer 3",
          topic: "Grundzüge der Sicherheitstechnik",
          subtopic: "Zutrittskontrolle / Gefahrenmeldeanlage / Fluchtwege",
          examinerQuestion: "Im Objekt fällt die Zutrittskontrolle aus, gleichzeitig ertönt ein Brandmeldealarm. Beschreiben Sie mir die wichtigsten Schritte bei Zutrittskontrolle, Gefahrenmeldeanlage und freizuhaltenden Fluchtwegen.",
          modelAnswer: "Bei Zutrittsausfall sichere ich manuell nach Vorgabe: nur berechtigte Personen einlassen und dokumentieren. Bei Brandalarm befolge ich den Objektalarmplan: Bereiche prüfen, Fluchtwege und Notausgänge freihalten, Personen zur Evakuierung anleiten und die Leitstelle informieren. Fluchtwege dürfen nie blockiert werden. Technische Störungen melde ich sofort an Auftraggeber und Einsatzleitung.",
          followUpQuestions: [
            "Was tun Sie, wenn der Notausgang blockiert ist?",
            "Dürfen Sie den Alarm ohne Prüfung zurücksetzen?",
            "Wie unterstützen Sie die Feuerwehr?"
          ],
          examinerNotes: "Alarmplan, Fluchtwege freihalten, technische Störung melden.",
          criticalMistakes: [
            "Alarm ohne Prüfung zurücksetzen",
            "Fluchtwege durch Gegenstände blockieren lassen",
            "Zutritt bei Ausfall unkontrolliert öffnen",
            "Evakuierung ohne Meldung an Leitstelle"
          ],
          difficulty: "medium",
          examRelevance: "medium",
          ihkSimilarityRisk: "low",
          sourceStyle: "accaoui_original"
        }
      ]
    }
  ]
};

window.ACCAOUI_ORAL_SHEETS_V23 = ACCAOUI_ORAL_SHEETS_V23;
