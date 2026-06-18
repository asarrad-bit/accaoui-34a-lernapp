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
          topic: "Strafgesetzbuch und Strafverfahrensrecht",
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
          topic: "Unfallverhütungsvorschriften Wach- und Sicherungsdienste",
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
          topic: "Umgang mit Waffen",
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
    },
    {
      id: "oral_sheet_c_v25",
      title: "Prüfungsbogen C",
      status: "draft",
      questions: [
        {
          id: "oral-c-001",
          mode: "oral",
          sheet: "C",
          order: 1,
          examinerBlock: 1,
          examinerRole: "Prüfer 1",
          topic: "Recht der öffentlichen Sicherheit und Ordnung",
          subtopic: "Öffentliches Recht / Privatrecht / Rolle des Sicherheitsmitarbeiters",
          examinerQuestion: "Ein Besucher sagt zu Ihnen: „Sie sind keine Polizei, Sie dürfen hier gar nichts.“ Erklären Sie, auf welcher rechtlichen Grundlage Sie trotzdem handeln dürfen und wo Ihre Grenzen liegen.",
          modelAnswer: "Ich handle nicht hoheitlich wie die Polizei, sondern privatrechtlich im Auftrag des Hausrechtsinhabers. Grundlage sind vor allem Hausrecht, Dienstanweisung und die allgemein zulässigen Jedermannsrechte. Ich darf Personen ansprechen, Zutritt verweigern oder zum Verlassen auffordern, wenn Auftrag und Hausordnung das hergeben. Ich darf aber keine Polizeibefugnisse vortäuschen, keine Strafen verhängen und nur in rechtfertigenden Ausnahmesituationen, etwa Notwehr oder vorläufige Festnahme bei frischer Tat, körperlich eingreifen.",
          followUpQuestions: [
            "Was ist der Unterschied zwischen privatrechtlichem Handeln und hoheitlichem Handeln?",
            "Wann muss die Polizei eingeschaltet werden?",
            "Warum ist es gefährlich, sich als Sicherheitsmitarbeiter wie eine Amtsperson zu verhalten?"
          ],
          examinerNotes: "Der Prüfling muss private Befugnisse klar von staatlicher Hoheitsgewalt trennen.",
          criticalMistakes: [
            "Sicherheitsmitarbeiter mit Polizeibeamten gleichsetzen",
            "Hausrecht als grenzenlose Befugnis darstellen",
            "Polizeiliche Maßnahmen vortäuschen",
            "Keine Grenzen der eigenen Rolle nennen"
          ],
          difficulty: "medium",
          examRelevance: "high",
          ihkSimilarityRisk: "low",
          sourceStyle: "accaoui_original"
        },
        {
          id: "oral-c-002",
          mode: "oral",
          sheet: "C",
          order: 2,
          examinerBlock: 1,
          examinerRole: "Prüfer 1",
          topic: "Bürgerliches Gesetzbuch",
          subtopic: "Hausrecht / Besitzdiener / Besitzschutz",
          examinerQuestion: "Sie werden vom Betreiber eines Einkaufszentrums beauftragt, das Hausrecht durchzusetzen. Was bedeutet Hausrecht und welche Rolle haben Sie als Sicherheitsmitarbeiter dabei?",
          modelAnswer: "Hausrecht bedeutet, dass der Berechtigte bestimmen darf, wer ein Grundstück, Gebäude oder Geschäft betreten und dort bleiben darf. Als Sicherheitsmitarbeiter übe ich dieses Recht nicht aus eigenem Recht aus, sondern im Auftrag des Hausrechtsinhabers. Ich darf auf Hausordnung und Anweisungen hinweisen, Zutritt verweigern oder Personen auffordern, den Bereich zu verlassen. Dabei muss ich verhältnismäßig, sachlich und diskriminierungsfrei handeln.",
          followUpQuestions: [
            "Was ist ein Besitzdiener?",
            "Darf ein Sicherheitsmitarbeiter immer körperlich eingreifen?",
            "Was tun Sie, wenn eine Person trotz Hausverbot nicht geht?"
          ],
          examinerNotes: "Hausrecht, Auftrag, Besitzdienerstellung und Grenzen müssen sauber erklärt werden.",
          criticalMistakes: [
            "Hausrecht als eigenes Recht des Mitarbeiters darstellen",
            "Körperlichen Zwang ohne Rechtfertigung erlauben",
            "Diskriminierende Zutrittsverweigerung akzeptieren",
            "Polizei bei Eskalation nicht erwähnen"
          ],
          difficulty: "medium",
          examRelevance: "high",
          ihkSimilarityRisk: "low",
          sourceStyle: "accaoui_original"
        },
        {
          id: "oral-c-003",
          mode: "oral",
          sheet: "C",
          order: 3,
          examinerBlock: 1,
          examinerRole: "Prüfer 1",
          topic: "Strafgesetzbuch und Strafverfahrensrecht",
          subtopic: "Vorläufige Festnahme / § 127 Abs. 1 StPO",
          examinerQuestion: "Sie beobachten, wie eine Person Ware einsteckt und ohne zu bezahlen den Kassenbereich verlässt. Wann dürfen Sie diese Person nach § 127 Abs. 1 StPO vorläufig festhalten?",
          modelAnswer: "Eine vorläufige Festnahme durch jedermann ist nur möglich, wenn die Person auf frischer Tat betroffen oder verfolgt wird und zusätzlich Fluchtverdacht besteht oder die Identität nicht sofort festgestellt werden kann. Ein bloßer Verdacht reicht nicht. Das Festhalten muss verhältnismäßig sein, die Polizei ist unverzüglich zu informieren und die Maßnahme dient nicht der Bestrafung.",
          followUpQuestions: [
            "Was bedeutet frische Tat?",
            "Reicht ein bloßer Verdacht?",
            "Was ist nach dem Festhalten sofort zu tun?"
          ],
          examinerNotes: "Frische Tat, Fluchtverdacht oder ungeklärte Identität und unverzügliche Polizei müssen genannt werden.",
          criticalMistakes: [
            "Bloßen Verdacht als ausreichend ansehen",
            "Festhalten als Strafe darstellen",
            "Polizei nicht informieren",
            "Unverhältnismäßige Gewalt erlauben"
          ],
          difficulty: "medium",
          examRelevance: "high",
          ihkSimilarityRisk: "low",
          sourceStyle: "accaoui_original"
        },
        {
          id: "oral-c-004",
          mode: "oral",
          sheet: "C",
          order: 4,
          examinerBlock: 1,
          examinerRole: "Prüfer 1",
          topic: "Strafgesetzbuch und Strafverfahrensrecht",
          subtopic: "Notwehr / Nothilfe / Verhältnismäßigkeit",
          examinerQuestion: "Ein Besucher schlägt plötzlich nach Ihnen. Was ist Notwehr und wie muss Ihre Reaktion rechtlich bewertet werden?",
          modelAnswer: "Notwehr ist die erforderliche Verteidigung gegen einen gegenwärtigen rechtswidrigen Angriff. Wenn der Besucher gerade angreift, darf ich mich verteidigen. Die Abwehr muss geeignet und erforderlich sein, also den Angriff beenden und darf nicht unnötig überzogen sein. Wenn ich eine andere Person schütze, spricht man von Nothilfe. Sobald der Angriff beendet ist, endet auch die Notwehrlage.",
          followUpQuestions: [
            "Was bedeutet gegenwärtiger Angriff?",
            "Was ist Nothilfe?",
            "Darf man nach Ende des Angriffs noch zurückschlagen?"
          ],
          examinerNotes: "Erforderlichkeit, Gegenwärtigkeit und Ende der Notwehrlage sind entscheidend.",
          criticalMistakes: [
            "Rache als Notwehr darstellen",
            "Vergangenen Angriff als Notwehrlage behandeln",
            "Unverhältnismäßige Gewalt erlauben",
            "Nothilfe nicht erklären können"
          ],
          difficulty: "medium",
          examRelevance: "high",
          ihkSimilarityRisk: "low",
          sourceStyle: "accaoui_original"
        },
        {
          id: "oral-c-005",
          mode: "oral",
          sheet: "C",
          order: 5,
          examinerBlock: 1,
          examinerRole: "Prüfer 1",
          topic: "Bürgerliches Gesetzbuch",
          subtopic: "Besitzwehr / Besitzkehr / verbotene Eigenmacht",
          examinerQuestion: "Ein Besucher nimmt ein Absperrschild des Objekts weg und will damit das Gelände verlassen. Welche zivilrechtlichen Begriffe und Möglichkeiten sind hier wichtig?",
          modelAnswer: "Wichtig sind Besitz, verbotene Eigenmacht und Besitzschutz. Wenn jemand ohne Willen des Berechtigten den Besitz entzieht oder stört, liegt verbotene Eigenmacht vor. Der Besitzer oder Besitzdiener kann im engen Rahmen Besitzwehr oder Besitzkehr ausüben. Als Sicherheitsmitarbeiter muss ich verhältnismäßig handeln, den Auftrag beachten und bei Streit oder Gefahr die Polizei hinzuziehen.",
          followUpQuestions: [
            "Was ist verbotene Eigenmacht?",
            "Was ist Besitzwehr?",
            "Warum muss auch hier verhältnismäßig gehandelt werden?"
          ],
          examinerNotes: "BGB-Begriffe sollen praxisnah und nicht polizeilich erklärt werden.",
          criticalMistakes: [
            "Besitz und Eigentum verwechseln",
            "Jede körperliche Gewalt erlauben",
            "Besitzschutz mit Strafe verwechseln",
            "Keine Verhältnismäßigkeit nennen"
          ],
          difficulty: "medium",
          examRelevance: "medium",
          ihkSimilarityRisk: "low",
          sourceStyle: "accaoui_original"
        },
        {
          id: "oral-c-006",
          mode: "oral",
          sheet: "C",
          order: 6,
          examinerBlock: 2,
          examinerRole: "Vorsitz",
          topic: "Umgang mit Menschen",
          subtopic: "Aggression / Deeskalation / Eigensicherung",
          examinerQuestion: "Eine Person wird laut, beleidigt Sie und kommt immer näher. Beschreiben Sie Ihr Vorgehen in den ersten zwei Minuten.",
          modelAnswer: "Ich halte Abstand, achte auf meinen Fluchtweg und bleibe ruhig. Ich spreche klar, langsam und respektvoll. Ich setze eine Grenze, zum Beispiel: „Bitte bleiben Sie auf Abstand, dann können wir sprechen.“ Ich vermeide Gegenbeleidigungen und provozierende Körpersprache. Gleichzeitig fordere ich Unterstützung an und informiere die Einsatzleitung. Bei Angriff oder konkreter Gefahr geht Eigenschutz vor und die Polizei wird gerufen.",
          followUpQuestions: [
            "Warum ist Abstand wichtig?",
            "Welche Formulierung wäre deeskalierend?",
            "Wann brechen Sie das Gespräch ab?"
          ],
          examinerNotes: "Der Prüfling soll Abstand, Ruhe, Grenze, Unterstützung und Eigenschutz strukturiert nennen.",
          criticalMistakes: [
            "Zurückbeleidigen",
            "Unnötig körperlich nah herangehen",
            "Allein in eine gefährliche Lage gehen",
            "Eigenschutz vergessen"
          ],
          difficulty: "medium",
          examRelevance: "high",
          ihkSimilarityRisk: "low",
          sourceStyle: "accaoui_original"
        },
        {
          id: "oral-c-007",
          mode: "oral",
          sheet: "C",
          order: 7,
          examinerBlock: 2,
          examinerRole: "Vorsitz",
          topic: "Umgang mit Menschen",
          subtopic: "Alkoholisierte Person / Hausverbot",
          examinerQuestion: "Eine alkoholisierte Person mit Hausverbot möchte in den Club. Sie wird laut und diskutiert. Wie gehen Sie vor?",
          modelAnswer: "Ich bleibe ruhig, halte Abstand und spreche klar. Ich erkläre kurz, dass wegen Hausverbot kein Zutritt möglich ist. Ich lasse mich nicht in lange Diskussionen ziehen und achte darauf, andere Gäste zu schützen. Bei Aggression fordere ich Unterstützung an. Bei Drohung, Angriff oder Straftat informiere ich die Polizei. Der Vorfall wird sachlich dokumentiert.",
          followUpQuestions: [
            "Warum ist Alkohol ein Risikofaktor?",
            "Was vermeiden Sie in der Kommunikation?",
            "Welche Punkte gehören in die Dokumentation?"
          ],
          examinerNotes: "Klare Grenze, keine Provokation, Unterstützung und Dokumentation sind wichtig.",
          criticalMistakes: [
            "Alkoholisierte Person verspotten",
            "Körperlich allein entfernen wollen",
            "Hausverbot ignorieren",
            "Keine Dokumentation erwähnen"
          ],
          difficulty: "medium",
          examRelevance: "high",
          ihkSimilarityRisk: "low",
          sourceStyle: "accaoui_original"
        },
        {
          id: "oral-c-008",
          mode: "oral",
          sheet: "C",
          order: 8,
          examinerBlock: 2,
          examinerRole: "Vorsitz",
          topic: "Umgang mit Menschen",
          subtopic: "Gruppe / Provokation / Kommunikation",
          examinerQuestion: "Eine Gruppe Jugendlicher provoziert am Eingang, filmt Sie mit dem Handy und macht sich über Sie lustig. Wie bleiben Sie professionell?",
          modelAnswer: "Ich lasse mich nicht provozieren und bleibe sachlich. Ich spreche möglichst eine Person als Ansprechpartner an, halte Abstand und behalte die Gruppe im Blick. Ich erkläre kurz die Regel oder den Grund der Maßnahme. Ich drohe nicht unnötig und vermeide Machtkämpfe. Wenn die Lage kippt, ziehe ich Kollegen oder Einsatzleitung hinzu und dokumentiere den Vorfall.",
          followUpQuestions: [
            "Warum sollte man eine Gruppe nicht frontal herausfordern?",
            "Was ist professionelle Distanz?",
            "Wann holen Sie Unterstützung?"
          ],
          examinerNotes: "Der Prüfling soll Gruppendynamik, Selbstkontrolle und klare Kommunikation erkennen.",
          criticalMistakes: [
            "Sich provozieren lassen",
            "Die ganze Gruppe aggressiv konfrontieren",
            "Handyaufnahme mit Gewalt verhindern wollen",
            "Keine Unterstützung anfordern"
          ],
          difficulty: "medium",
          examRelevance: "high",
          ihkSimilarityRisk: "low",
          sourceStyle: "accaoui_original"
        },
        {
          id: "oral-c-009",
          mode: "oral",
          sheet: "C",
          order: 9,
          examinerBlock: 2,
          examinerRole: "Vorsitz",
          topic: "Umgang mit Menschen",
          subtopic: "Interkulturelle Kommunikation / Sprachbarriere",
          examinerQuestion: "Bei einer Kontrolle versteht eine Person kaum Deutsch, wirkt unsicher und wird nervös. Wie handeln Sie respektvoll und trotzdem sicher?",
          modelAnswer: "Ich spreche langsam, einfach und freundlich. Ich erkläre den Kontrollgrund kurz und nutze klare Gesten. Ich bleibe geduldig, achte auf Würde und vermeide abwertende Aussagen. Die Sicherheitsregeln gelten weiter für alle, aber die Kommunikation wird angepasst. Wenn nötig, hole ich Unterstützung zur Verständigung hinzu.",
          followUpQuestions: [
            "Was bedeutet diskriminierungsfreier Umgang?",
            "Wie vermeiden Sie Missverständnisse?",
            "Warum dürfen Sicherheitsstandards trotzdem nicht aufgeweicht werden?"
          ],
          examinerNotes: "Respekt, Gleichbehandlung und klare Sicherheitsstandards müssen zusammen genannt werden.",
          criticalMistakes: [
            "Person wegen Sprache oder Herkunft abwerten",
            "Kontrolle komplett unterlassen",
            "Unklare oder aggressive Körpersprache nutzen",
            "Regeln willkürlich anwenden"
          ],
          difficulty: "medium",
          examRelevance: "high",
          ihkSimilarityRisk: "low",
          sourceStyle: "accaoui_original"
        },
        {
          id: "oral-c-010",
          mode: "oral",
          sheet: "C",
          order: 10,
          examinerBlock: 2,
          examinerRole: "Vorsitz",
          topic: "Umgang mit Menschen",
          subtopic: "Panik / Menschenmenge / Eigenschutz",
          examinerQuestion: "Bei einer Veranstaltung entsteht plötzlich Gedränge, mehrere Personen werden unruhig und ein Ausgang ist blockiert. Was tun Sie?",
          modelAnswer: "Ich bewahre Ruhe, informiere sofort Einsatzleitung und Kollegen und achte auf meinen Eigenschutz. Ich leite Personen ruhig zu freien Flucht- oder Ausweichwegen, vermeide panikauslösende Rufe und halte Fluchtwege frei. Wenn Menschen gefährdet sind, wird nach Alarm- oder Sicherheitskonzept gehandelt. Feuerwehr, Rettungsdienst oder Polizei werden je nach Lage informiert. Blockaden werden, soweit sicher möglich, entfernt oder abgesichert.",
          followUpQuestions: [
            "Warum ist ruhige Kommunikation in Menschenmengen wichtig?",
            "Was tun Sie, wenn ein Fluchtweg blockiert ist?",
            "Wann informieren Sie Rettungskräfte oder Polizei?"
          ],
          examinerNotes: "Der Prüfling soll Panik vermeiden, Meldekette nutzen und Fluchtwege sichern.",
          criticalMistakes: [
            "Panik verursachen",
            "Blockierten Ausgang ignorieren",
            "Allein unkoordiniert handeln",
            "Eigenschutz und Meldekette vergessen"
          ],
          difficulty: "hard",
          examRelevance: "high",
          ihkSimilarityRisk: "low",
          sourceStyle: "accaoui_original"
        },
        {
          id: "oral-c-011",
          mode: "oral",
          sheet: "C",
          order: 11,
          examinerBlock: 3,
          examinerRole: "Prüfer 3",
          topic: "Gewerberecht",
          subtopic: "Dienstanweisung / Dienstausweis / Dienstkleidung",
          examinerQuestion: "Welche Bedeutung haben Dienstanweisung, Dienstausweis und Dienstkleidung im Bewachungsgewerbe?",
          modelAnswer: "Die Dienstanweisung enthält verbindliche Vorgaben für Verhalten, Aufgaben und Grenzen der Tätigkeit. Der Dienstausweis dient der Legitimation und muss nach Vorgaben mitgeführt werden. Dienstkleidung darf nicht mit Uniformen von Polizei oder Behörden verwechselt werden. Sicherheitsmitarbeiter müssen klar erkennbar sein, dürfen aber keine amtliche Stellung vortäuschen.",
          followUpQuestions: [
            "Warum darf Dienstkleidung nicht wie Polizei aussehen?",
            "Welche Rolle hat die Dienstanweisung im Alltag?",
            "Wann muss ein Ausweis vorgezeigt oder mitgeführt werden?"
          ],
          examinerNotes: "Gewerberechtliche Pflichten und Abgrenzung zu hoheitlichem Auftreten prüfen.",
          criticalMistakes: [
            "Polizeiähnliche Uniform als unproblematisch darstellen",
            "Dienstanweisung als unverbindlich erklären",
            "Dienstausweis nicht erwähnen",
            "Amtliche Befugnisse vortäuschen"
          ],
          difficulty: "medium",
          examRelevance: "medium",
          ihkSimilarityRisk: "low",
          sourceStyle: "accaoui_original"
        },
        {
          id: "oral-c-012",
          mode: "oral",
          sheet: "C",
          order: 12,
          examinerBlock: 3,
          examinerRole: "Prüfer 3",
          topic: "Datenschutzrecht",
          subtopic: "Besucherlisten / Videoüberwachung / Datenminimierung",
          examinerQuestion: "Sie arbeiten am Empfang, führen Besucherlisten und der Eingangsbereich wird videoüberwacht. Welche Datenschutzgrundsätze müssen Sie beachten?",
          modelAnswer: "Es handelt sich um personenbezogene Daten. Diese dürfen nur mit Rechtsgrundlage und für einen bestimmten Zweck verarbeitet werden. Es gilt Datenminimierung: nur notwendige Daten erfassen. Besucherlisten müssen vor Einsicht durch Unbefugte geschützt und nach Ablauf der Aufbewahrungsfrist gelöscht werden. Videoüberwachung muss kenntlich gemacht, verhältnismäßig und zweckgebunden sein. Ich handle nach Vorgaben des Verantwortlichen.",
          followUpQuestions: [
            "Warum dürfen Besucherlisten nicht offen liegen?",
            "Was bedeutet Zweckbindung?",
            "Was ist bei Videoüberwachung wichtig?"
          ],
          examinerNotes: "Zweckbindung, Datenminimierung, Schutz vor Einsicht, Löschung und Hinweis auf Videoüberwachung müssen genannt werden.",
          criticalMistakes: [
            "Daten offen liegen lassen",
            "Private Weitergabe erlauben",
            "Keine Löschung erwähnen",
            "Videoüberwachung ohne Hinweis als unproblematisch darstellen"
          ],
          difficulty: "medium",
          examRelevance: "medium",
          ihkSimilarityRisk: "low",
          sourceStyle: "accaoui_original"
        },
        {
          id: "oral-c-013",
          mode: "oral",
          sheet: "C",
          order: 13,
          examinerBlock: 3,
          examinerRole: "Prüfer 3",
          topic: "Unfallverhütungsvorschriften Wach- und Sicherungsdienste",
          subtopic: "Nachtdienst / Gefahrenstelle / Eigenschutz",
          examinerQuestion: "Während einer Nachtschicht bemerken Sie eine schlecht beleuchtete Treppe und lose Kabel im Kontrollbereich. Wie handeln Sie nach UVV-Grundsätzen?",
          modelAnswer: "Ich gefährde mich nicht unnötig, nutze sichere Wege und melde die Gefahrenstelle sofort nach Dienstweg. Wenn möglich und zumutbar, sichere ich den Bereich ab oder warne andere Personen. Ich dokumentiere die Feststellung. Gefährliche Reparaturen führe ich nicht eigenmächtig aus, sondern informiere Auftraggeber, Einsatzleitung oder zuständige Stelle.",
          followUpQuestions: [
            "Warum ist Eigenschutz im Nachtdienst wichtig?",
            "Was dokumentieren Sie?",
            "Wann dürfen Sie eine Gefahr selbst beseitigen?"
          ],
          examinerNotes: "Erkennen, melden, absichern, dokumentieren und Eigenschutz sollen vorkommen.",
          criticalMistakes: [
            "Gefahr ignorieren",
            "Riskante Reparatur eigenmächtig durchführen",
            "Keine Meldung oder Dokumentation",
            "Andere Personen weiter in die Gefahr laufen lassen"
          ],
          difficulty: "medium",
          examRelevance: "medium",
          ihkSimilarityRisk: "low",
          sourceStyle: "accaoui_original"
        },
        {
          id: "oral-c-014",
          mode: "oral",
          sheet: "C",
          order: 14,
          examinerBlock: 3,
          examinerRole: "Prüfer 3",
          topic: "Umgang mit Waffen",
          subtopic: "Gefährlicher Gegenstand / Einlasskontrolle",
          examinerQuestion: "Bei einer Einlasskontrolle entdecken Sie bei einem Gast ein Messer. Wie reagieren Sie rechtlich und praktisch?",
          modelAnswer: "Ich bleibe ruhig, halte Abstand und bewerte die Situation nach Hausordnung, Gefahrenlage und Art des Gegenstands. Ich darf den Zutritt verweigern und die Einsatzleitung informieren. Eigenmächtige Beschlagnahme oder Durchsuchung gegen den Willen ist nicht zulässig. Bei konkreter Gefahr oder Verdacht auf einen verbotenen Gegenstand informiere ich die Polizei. Der Vorgang wird dokumentiert.",
          followUpQuestions: [
            "Dürfen Sie das Messer einfach behalten?",
            "Was tun Sie bei akuter Bedrohung?",
            "Welche Rolle spielt die Hausordnung?"
          ],
          examinerNotes: "Zutrittsverweigerung ja, eigenmächtige Beschlagnahme nein, Polizei bei konkreter Gefahr.",
          criticalMistakes: [
            "Messer ohne Grundlage behalten",
            "Körperliche Durchsuchung erzwingen",
            "Akute Gefahr unterschätzen",
            "Keine Dokumentation"
          ],
          difficulty: "medium",
          examRelevance: "medium",
          ihkSimilarityRisk: "low",
          sourceStyle: "accaoui_original"
        },
        {
          id: "oral-c-015",
          mode: "oral",
          sheet: "C",
          order: 15,
          examinerBlock: 3,
          examinerRole: "Prüfer 3",
          topic: "Grundzüge der Sicherheitstechnik",
          subtopic: "Brandalarm / Fluchtwege / Feuerwehrzufahrt",
          examinerQuestion: "Ein Brandalarm läuft auf, gleichzeitig stehen Kartons im Fluchtweg und eine Feuerwehrzufahrt ist teilweise blockiert. Was tun Sie?",
          modelAnswer: "Ich befolge den Alarm- und Objektplan. Ich melde die Lage an Leitstelle oder Einsatzleitung und sorge dafür, dass Fluchtwege und Notausgänge freigehalten werden. Personen werden ruhig zur Evakuierung angeleitet. Die Feuerwehrzufahrt ist freizumachen oder abzusichern. Den Alarm setze ich nicht eigenmächtig zurück. Ich unterstütze Feuerwehr und Einsatzleitung mit klaren Informationen.",
          followUpQuestions: [
            "Warum dürfen Fluchtwege nie blockiert sein?",
            "Dürfen Sie den Alarm selbst zurücksetzen?",
            "Welche Informationen sind für Feuerwehr oder Einsatzleitung wichtig?"
          ],
          examinerNotes: "Alarmplan, Evakuierung, freie Fluchtwege, Feuerwehrzufahrt und keine eigenmächtige Rückstellung müssen genannt werden.",
          criticalMistakes: [
            "Kartons im Fluchtweg stehen lassen",
            "Alarm ohne Prüfung zurücksetzen",
            "Panik verursachen",
            "Feuerwehrzufahrt ignorieren"
          ],
          difficulty: "medium",
          examRelevance: "medium",
          ihkSimilarityRisk: "low",
          sourceStyle: "accaoui_original"
        }
      ]
    },
    {
      id: "oral_sheet_d_v253a",
      title: "Prüfungsbogen D",
      description: "15 Accaoui-original Fallfragen für die mündliche §34a-Prüfung mit Fokus auf Befugnisse, Deeskalation, Dokumentation, Datenschutz, UVV, Waffen und Sicherheitstechnik.",
      status: "draft",
      questions: [
        {
          id: "oral-d-001",
          mode: "oral",
          sheet: "D",
          order: 1,
          examinerBlock: 1,
          examinerRole: "Prüfer 1",
          topic: "Bürgerliches Gesetzbuch",
          subtopic: "Taschenkontrolle / Einwilligung / Hausrecht",
          examinerQuestion: "Ein Kunde soll am Ausgang seine Tasche öffnen. Darf ein Sicherheitsmitarbeiter eine Taschenkontrolle erzwingen? Erklären Sie die rechtlichen Grenzen.",
          modelAnswer: "Eine Taschenkontrolle darf grundsätzlich nicht gegen den Willen der Person erzwungen werden. Der Sicherheitsmitarbeiter kann auf Grundlage des Hausrechts und der Hausordnung um eine freiwillige Kontrolle bitten. Verweigert die Person die Kontrolle, kann der Zutritt künftig verweigert oder die Polizei hinzugezogen werden, wenn ein konkreter Verdacht besteht. Eine körperliche Durchsuchung oder gewaltsame Taschenöffnung ist ohne rechtliche Grundlage nicht zulässig. Wichtig sind Freiwilligkeit, Verhältnismäßigkeit und klare Kommunikation.",
          followUpQuestions: [
            "Was bedeutet freiwillige Einwilligung?",
            "Was tun Sie bei konkretem Diebstahlsverdacht?",
            "Warum ist eine erzwungene Durchsuchung rechtlich gefährlich?"
          ],
          examinerNotes: "Der Prüfling muss Freiwilligkeit, Hausrecht, Verdacht, Polizei und Grenzen privater Befugnisse sauber trennen.",
          criticalMistakes: [
            "Taschenkontrolle gegen den Willen erlauben",
            "Hausrecht als Durchsuchungsrecht darstellen",
            "Polizei bei konkretem Verdacht nicht erwähnen",
            "Verhältnismäßigkeit vergessen"
          ],
          difficulty: "hard",
          examRelevance: "high",
          ihkSimilarityRisk: "low",
          sourceStyle: "accaoui_original"
        },
        {
          id: "oral-d-002",
          mode: "oral",
          sheet: "D",
          order: 2,
          examinerBlock: 1,
          examinerRole: "Prüfer 1",
          topic: "Recht der öffentlichen Sicherheit und Ordnung",
          subtopic: "Identitätsfeststellung / private Befugnisse / Polizeiabgrenzung",
          examinerQuestion: "Eine Person weigert sich, ihren Ausweis zu zeigen. Welche Möglichkeiten haben Sie als Sicherheitsmitarbeiter – und wo enden Ihre Befugnisse?",
          modelAnswer: "Ein Sicherheitsmitarbeiter darf eine Person ansprechen und um das Vorzeigen eines Ausweises bitten, wenn es dafür einen sachlichen Grund gibt, zum Beispiel Zutrittskontrolle oder Hausordnung. Er darf die Identitätsfeststellung aber nicht wie die Polizei erzwingen. Verweigert die Person die Mitwirkung, kann je nach Auftrag der Zutritt verweigert oder die Person zum Verlassen aufgefordert werden. Bei Straftatverdacht oder Gefahr muss die Polizei eingeschaltet werden. Polizeibefugnisse dürfen nicht vorgetäuscht werden.",
          followUpQuestions: [
            "Darf ein Sicherheitsmitarbeiter einen Ausweis verlangen wie die Polizei?",
            "Was ist der Unterschied zwischen Bitten und Erzwingen?",
            "Wann rufen Sie die Polizei?"
          ],
          examinerNotes: "Private Kontrolle und polizeiliche Identitätsfeststellung müssen klar abgegrenzt werden.",
          criticalMistakes: [
            "Polizeiliche Identitätsfeststellung behaupten",
            "Ausweis zwangsweise wegnehmen wollen",
            "Keine Grenze privater Befugnisse nennen",
            "Keine Polizei bei Gefahr oder Straftatverdacht erwähnen"
          ],
          difficulty: "hard",
          examRelevance: "high",
          ihkSimilarityRisk: "low",
          sourceStyle: "accaoui_original"
        },
        {
          id: "oral-d-003",
          mode: "oral",
          sheet: "D",
          order: 3,
          examinerBlock: 1,
          examinerRole: "Prüfer 1",
          topic: "Strafgesetzbuch und Strafverfahrensrecht",
          subtopic: "Rechtfertigender Notstand / Hilfeleistung / Gefahrabwehr",
          examinerQuestion: "In einem Objekt liegt eine bewusstlose Person hinter einer verschlossenen Tür. Welche rechtlichen Gedanken spielen bei Notstand und Hilfeleistung eine Rolle?",
          modelAnswer: "Hier geht es nicht um Notwehr, sondern um eine Gefahr für Leben oder Gesundheit. Wichtig sind Hilfeleistung, Notruf und möglicherweise rechtfertigender Notstand, wenn ein geschütztes Rechtsgut nur durch Eingriff in ein anderes Rechtsgut gerettet werden kann. Ich informiere sofort Rettungsdienst, Einsatzleitung und je nach Lage Feuerwehr oder Polizei. Wenn akute Lebensgefahr besteht und keine mildere Möglichkeit vorhanden ist, kann ein verhältnismäßiger Eingriff gerechtfertigt sein. Eigengefährdung ist zu vermeiden, und der Vorfall muss dokumentiert werden.",
          followUpQuestions: [
            "Warum ist das keine klassische Notwehrlage?",
            "Was bedeutet rechtfertigender Notstand?",
            "Warum muss der Eingriff verhältnismäßig bleiben?"
          ],
          examinerNotes: "Notwehr und Notstand dürfen nicht verwechselt werden. Hilfeleistung, Notruf, Verhältnismäßigkeit und Eigenschutz sind Pflichtpunkte.",
          criticalMistakes: [
            "Notstand mit Notwehr verwechseln",
            "Keine Rettungskräfte informieren",
            "Türöffnung ohne Gefahr und ohne Verhältnismäßigkeit erlauben",
            "Eigenschutz vergessen"
          ],
          difficulty: "hard",
          examRelevance: "high",
          ihkSimilarityRisk: "low",
          sourceStyle: "accaoui_original"
        },
        {
          id: "oral-d-004",
          mode: "oral",
          sheet: "D",
          order: 4,
          examinerBlock: 1,
          examinerRole: "Prüfer 1",
          topic: "Strafgesetzbuch und Strafverfahrensrecht",
          subtopic: "Beleidigung / Bedrohung / Nötigung / professionelles Verhalten",
          examinerQuestion: "Ein Gast beleidigt Sie schwer und droht, Sie später „abzufangen“. Welche Straftatbestände können berührt sein und wie reagieren Sie professionell?",
          modelAnswer: "Je nach Wortlaut und Situation können Beleidigung, Bedrohung oder Nötigung berührt sein. Ich bleibe ruhig, provoziere nicht zurück und halte Abstand. Ich sichere mich selbst, informiere Kollegen oder Einsatzleitung und beende die Situation nach Möglichkeit deeskalierend. Bei konkreter Drohung, Gefahr oder Straftatverdacht wird die Polizei informiert. Wichtig ist, den Vorfall sachlich zu dokumentieren, mit Uhrzeit, Ort, Beteiligten, Wortlaut und Zeugen.",
          followUpQuestions: [
            "Warum dürfen Sie nicht zurückbeleidigen?",
            "Wann wird aus einer Drohung eine ernsthafte Gefahr?",
            "Was dokumentieren Sie genau?"
          ],
          examinerNotes: "Der Prüfling soll Straftatbestände vorsichtig einordnen und professionelles Verhalten beschreiben.",
          criticalMistakes: [
            "Zurückbeleidigen",
            "Drohung ignorieren",
            "Straftatbestände pauschal oder falsch sicher behaupten",
            "Keine Dokumentation oder Meldung erwähnen"
          ],
          difficulty: "medium",
          examRelevance: "high",
          ihkSimilarityRisk: "low",
          sourceStyle: "accaoui_original"
        },
        {
          id: "oral-d-005",
          mode: "oral",
          sheet: "D",
          order: 5,
          examinerBlock: 1,
          examinerRole: "Prüfer 1",
          topic: "Bürgerliches Gesetzbuch",
          subtopic: "Hausverbot / Hausrecht / Verhältnismäßigkeit",
          examinerQuestion: "Eine Person mit Hausverbot betritt ein Geschäft, bleibt aber ruhig stehen und sagt: „Ich gehe nicht.“ Wie setzen Sie das Hausrecht rechtssicher durch?",
          modelAnswer: "Ich spreche die Person ruhig an und weise sachlich auf das bestehende Hausverbot hin. Ich fordere sie eindeutig auf, das Objekt zu verlassen. Ich bleibe verhältnismäßig und setze nicht sofort körperliche Gewalt ein. Wenn die Person nicht geht, informiere ich die Einsatzleitung und je nach Lage die Polizei. Das Verhalten kann Hausfriedensbruch darstellen, wenn die Person trotz Aufforderung bleibt. Der Vorfall wird mit Zeit, Ort, Aufforderung, Reaktion und Zeugen dokumentiert.",
          followUpQuestions: [
            "Wann kann Hausfriedensbruch vorliegen?",
            "Warum ist eine klare Aufforderung wichtig?",
            "Wann darf körperliches Eingreifen überhaupt in Betracht kommen?"
          ],
          examinerNotes: "Hausrecht, klare Aufforderung, Hausfriedensbruch, Verhältnismäßigkeit und Dokumentation müssen genannt werden.",
          criticalMistakes: [
            "Sofort körperlich entfernen wollen",
            "Hausfriedensbruch nicht erkennen",
            "Keine klare Aufforderung aussprechen",
            "Polizei und Dokumentation vergessen"
          ],
          difficulty: "medium",
          examRelevance: "high",
          ihkSimilarityRisk: "low",
          sourceStyle: "accaoui_original"
        },
        {
          id: "oral-d-006",
          mode: "oral",
          sheet: "D",
          order: 6,
          examinerBlock: 2,
          examinerRole: "Vorsitz",
          topic: "Umgang mit Menschen",
          subtopic: "Verwirrte Person / Orientierungslosigkeit / Eigensicherung",
          examinerQuestion: "Eine verwirrte Person läuft orientierungslos durch ein Objekt und reagiert kaum auf Ansprache. Wie handeln Sie menschlich, sicher und verhältnismäßig?",
          modelAnswer: "Ich bleibe ruhig, halte Abstand und spreche die Person langsam, freundlich und einfach an. Ich vermeide Druck, hektische Bewegungen und laute Befehle. Gleichzeitig achte ich auf Eigenschutz und darauf, ob die Person sich selbst oder andere gefährdet. Wenn die Person hilflos wirkt, informiere ich Einsatzleitung, Rettungsdienst oder Polizei, je nach Lage. Ich begleite die Person nicht allein in abgelegene Bereiche und dokumentiere den Vorfall sachlich.",
          followUpQuestions: [
            "Warum ist ruhige Kommunikation hier besonders wichtig?",
            "Wann informieren Sie Rettungsdienst oder Polizei?",
            "Warum darf man die Person nicht einfach grob wegschicken?"
          ],
          examinerNotes: "Menschlichkeit und Eigensicherung müssen zusammen genannt werden.",
          criticalMistakes: [
            "Verwirrte Person auslachen oder abwerten",
            "Zu nah herangehen und Eigenschutz vergessen",
            "Hilflose Lage ignorieren",
            "Keine Unterstützung anfordern"
          ],
          difficulty: "medium",
          examRelevance: "high",
          ihkSimilarityRisk: "low",
          sourceStyle: "accaoui_original"
        },
        {
          id: "oral-d-007",
          mode: "oral",
          sheet: "D",
          order: 7,
          examinerBlock: 2,
          examinerRole: "Vorsitz",
          topic: "Umgang mit Menschen",
          subtopic: "Schutz von Personen / sexuelle Belästigung / Deeskalation",
          examinerQuestion: "Eine Besucherin meldet, dass sie von einem Gast belästigt wurde. Wie reagieren Sie als Sicherheitsmitarbeiter?",
          modelAnswer: "Ich nehme die Meldung ernst, bleibe ruhig und bringe die betroffene Person, wenn nötig, aus der unmittelbaren Gefahrensituation. Ich höre sachlich zu, ohne sie zu bedrängen oder zu beschuldigen. Ich informiere Kollegen oder Einsatzleitung und trenne die beteiligten Personen räumlich, soweit dies sicher möglich ist. Bei konkretem Verdacht auf eine Straftat oder Gefahr wird die Polizei informiert. Der Vorfall wird sorgfältig dokumentiert, mit Zeit, Ort, Beteiligten, Zeugen und wahrgenommenem Verhalten.",
          followUpQuestions: [
            "Warum darf man die Meldung nicht verharmlosen?",
            "Warum sollten beteiligte Personen getrennt werden?",
            "Welche Informationen gehören in die Dokumentation?"
          ],
          examinerNotes: "Schutz der betroffenen Person, Trennung der Beteiligten, Polizei bei Straftatverdacht und Dokumentation sind entscheidend.",
          criticalMistakes: [
            "Betroffene Person nicht ernst nehmen",
            "Täter und betroffene Person weiter zusammenstehen lassen",
            "Selbst Ermittler spielen",
            "Keine Polizei bei konkretem Straftatverdacht erwähnen"
          ],
          difficulty: "medium",
          examRelevance: "high",
          ihkSimilarityRisk: "low",
          sourceStyle: "accaoui_original"
        },
        {
          id: "oral-d-008",
          mode: "oral",
          sheet: "D",
          order: 8,
          examinerBlock: 2,
          examinerRole: "Vorsitz",
          topic: "Umgang mit Menschen",
          subtopic: "Konflikt zwischen Personen / Trennung / Eskalationsvermeidung",
          examinerQuestion: "Zwei Gäste streiten laut, schubsen sich aber noch nicht. Wie verhindern Sie eine Eskalation?",
          modelAnswer: "Ich beobachte kurz die Lage, halte Abstand und spreche ruhig und klar. Ich stelle mich nicht ungeschützt zwischen die Personen, sondern versuche, Abstand zwischen ihnen herzustellen und Unterstützung anzufordern. Ich spreche nach Möglichkeit eine Person direkt an und setze klare Grenzen: keine Beleidigungen, kein körperlicher Kontakt. Wenn die Situation kippt oder eine Gefahr entsteht, wird die Einsatzleitung oder Polizei informiert. Ziel ist, die Lage zu beruhigen, nicht einen Machtkampf zu gewinnen.",
          followUpQuestions: [
            "Warum ist es gefährlich, sich einfach zwischen zwei aggressive Personen zu stellen?",
            "Welche Formulierung wäre deeskalierend?",
            "Wann holen Sie Kollegen dazu?"
          ],
          examinerNotes: "Der Prüfling muss Gruppendynamik, Abstand, Unterstützung und klare Grenze beherrschen.",
          criticalMistakes: [
            "Allein körperlich dazwischengehen",
            "Partei ergreifen und Streit verstärken",
            "Keine Unterstützung holen",
            "Aggression durch Drohungen erhöhen"
          ],
          difficulty: "medium",
          examRelevance: "high",
          ihkSimilarityRisk: "low",
          sourceStyle: "accaoui_original"
        },
        {
          id: "oral-d-009",
          mode: "oral",
          sheet: "D",
          order: 9,
          examinerBlock: 2,
          examinerRole: "Vorsitz",
          topic: "Umgang mit Menschen",
          subtopic: "Angst / Stressreaktion / Erste Hilfe / Kommunikation",
          examinerQuestion: "Eine Person bekommt bei einer Kontrolle Angst, zittert und sagt, sie bekomme keine Luft. Wie gehen Sie vor?",
          modelAnswer: "Ich unterbreche die Situation, reduziere Druck und spreche ruhig mit der Person. Ich halte Abstand, sorge für Luft und Platz und frage, ob medizinische Hilfe benötigt wird. Wenn der Zustand ernst wirkt oder sich verschlechtert, informiere ich Rettungsdienst und Einsatzleitung. Ich bleibe bei der Person, soweit es sicher ist, und lasse sie nicht allein. Die Kontrolle wird nicht mit Zwang fortgesetzt, wenn eine gesundheitliche Gefahr erkennbar ist. Der Vorfall wird dokumentiert.",
          followUpQuestions: [
            "Warum muss hier Druck reduziert werden?",
            "Wann rufen Sie den Rettungsdienst?",
            "Warum darf die Kontrolle nicht stur fortgesetzt werden?"
          ],
          examinerNotes: "Gesundheitliche Lage, Deeskalation, Erste Hilfe, Rettungsdienst und Dokumentation müssen erkannt werden.",
          criticalMistakes: [
            "Angstreaktion als Schauspiel abtun",
            "Kontrolle trotz möglicher gesundheitlicher Gefahr erzwingen",
            "Rettungsdienst nicht erwähnen",
            "Person ohne Beobachtung alleinlassen"
          ],
          difficulty: "medium",
          examRelevance: "high",
          ihkSimilarityRisk: "low",
          sourceStyle: "accaoui_original"
        },
        {
          id: "oral-d-010",
          mode: "oral",
          sheet: "D",
          order: 10,
          examinerBlock: 2,
          examinerRole: "Vorsitz",
          topic: "Umgang mit Menschen",
          subtopic: "Vorfalldokumentation / Bericht / Nachvollziehbarkeit",
          examinerQuestion: "Nach einem Vorfall verlangt Ihr Auftraggeber eine schriftliche Meldung. Welche Punkte gehören in eine professionelle Dokumentation?",
          modelAnswer: "Eine professionelle Dokumentation muss sachlich, vollständig und nachvollziehbar sein. Dazu gehören Datum, Uhrzeit, Ort, beteiligte Personen, Zeugen, genaue Beobachtungen, getroffene Maßnahmen, informierte Stellen und das Ergebnis. Wichtig ist, zwischen Tatsachen und persönlichen Einschätzungen zu unterscheiden. Beleidigungen, Vermutungen oder übertriebene Formulierungen gehören nicht in den Bericht. Datenschutz ist zu beachten, und die Meldung wird nur an berechtigte Stellen weitergegeben.",
          followUpQuestions: [
            "Warum muss man Tatsachen und Vermutungen trennen?",
            "Welche Fehler machen Berichte unbrauchbar?",
            "Warum ist Datenschutz auch bei Vorfallberichten wichtig?"
          ],
          examinerNotes: "Sachlichkeit, Vollständigkeit, Tatsachen/Einschätzungen und Datenschutz müssen genannt werden.",
          criticalMistakes: [
            "Vermutungen als Fakten darstellen",
            "Unsachliche oder beleidigende Sprache verwenden",
            "Uhrzeit, Ort oder Beteiligte vergessen",
            "Bericht an unberechtigte Personen weitergeben"
          ],
          difficulty: "medium",
          examRelevance: "high",
          ihkSimilarityRisk: "low",
          sourceStyle: "accaoui_original"
        },
        {
          id: "oral-d-011",
          mode: "oral",
          sheet: "D",
          order: 11,
          examinerBlock: 3,
          examinerRole: "Prüfer 3",
          topic: "Datenschutzrecht",
          subtopic: "Vertraulichkeit / personenbezogene Daten / berufliche Verschwiegenheit",
          examinerQuestion: "Ein Bekannter fragt Sie privat, welche Personen regelmäßig ein bestimmtes Objekt besuchen. Was ist datenschutzrechtlich und beruflich zu beachten?",
          modelAnswer: "Ich darf solche Informationen nicht weitergeben. Es handelt sich um personenbezogene oder objektbezogene Informationen, die ich nur im Rahmen meines Dienstauftrags verwenden darf. Private Weitergabe ist unzulässig und kann datenschutzrechtliche, arbeitsrechtliche und vertragsrechtliche Folgen haben. Ich verweise darauf, dass ich zu dienstlichen Informationen keine Auskunft geben darf. Auffällige Anfragen oder Verdachtsmomente melde ich an die zuständige Stelle oder Einsatzleitung.",
          followUpQuestions: [
            "Warum sind Besuchsinformationen personenbezogen?",
            "Was bedeutet Zweckbindung?",
            "Welche Folgen kann eine unbefugte Weitergabe haben?"
          ],
          examinerNotes: "Datenschutz ist auch mündlich und privat relevant. Zweckbindung und Verschwiegenheit sind Kernpunkte.",
          criticalMistakes: [
            "Private Weitergabe als unproblematisch darstellen",
            "Datenschutz nur auf Computerdateien beschränken",
            "Zweckbindung nicht nennen",
            "Keine Meldung bei auffälliger Anfrage erwähnen"
          ],
          difficulty: "medium",
          examRelevance: "high",
          ihkSimilarityRisk: "low",
          sourceStyle: "accaoui_original"
        },
        {
          id: "oral-d-012",
          mode: "oral",
          sheet: "D",
          order: 12,
          examinerBlock: 3,
          examinerRole: "Prüfer 3",
          topic: "Grundzüge der Sicherheitstechnik",
          subtopic: "Schlüsselverwaltung / Schließanlage / Objektsicherheit",
          examinerQuestion: "Während des Dienstes bemerken Sie, dass ein Generalschlüssel fehlt. Wie handeln Sie?",
          modelAnswer: "Ich informiere sofort die Einsatzleitung oder die zuständige objektverantwortliche Stelle. Ein Generalschlüsselverlust ist ein erheblicher Sicherheitsvorfall, weil unbefugter Zugang möglich sein kann. Ich suche nicht heimlich allein weiter, sondern halte den Dienstweg ein. Der letzte bekannte Besitz, Zeitpunkt, Einsatzbereich und mögliche Übergaben müssen dokumentiert werden. Je nach Objektanweisung können Schließbereiche gesperrt, Kontrollen verstärkt oder weitere Sicherheitsmaßnahmen eingeleitet werden.",
          followUpQuestions: [
            "Warum ist ein Generalschlüssel besonders kritisch?",
            "Was muss dokumentiert werden?",
            "Warum darf der Verlust nicht verschwiegen werden?"
          ],
          examinerNotes: "Schlüsselverlust ist sicherheitsrelevant und muss sofort gemeldet und dokumentiert werden.",
          criticalMistakes: [
            "Schlüsselverlust verschweigen",
            "Erst lange allein suchen und niemanden informieren",
            "Keine Dokumentation erstellen",
            "Risiko für das Objekt unterschätzen"
          ],
          difficulty: "medium",
          examRelevance: "high",
          ihkSimilarityRisk: "low",
          sourceStyle: "accaoui_original"
        },
        {
          id: "oral-d-013",
          mode: "oral",
          sheet: "D",
          order: 13,
          examinerBlock: 3,
          examinerRole: "Prüfer 3",
          topic: "Unfallverhütungsvorschriften Wach- und Sicherungsdienste",
          subtopic: "Kontrollgang / Alleinarbeit / Kommunikationsmittel",
          examinerQuestion: "Beim nächtlichen Kontrollgang fällt Ihr Funkgerät aus. Wie verhalten Sie sich nach UVV- und Sicherheitsgrundsätzen?",
          modelAnswer: "Ich beachte den Eigenschutz und setze den Kontrollgang nicht blind fort, wenn dadurch meine Sicherheit gefährdet wird. Ich versuche, über ein Ersatzgerät, Telefon oder vereinbarte Meldewege Kontakt zur Leitstelle oder Einsatzleitung aufzunehmen. Wenn keine Kommunikation möglich ist, halte ich mich an die Dienstanweisung und begebe mich in einen sicheren Bereich. Der Ausfall wird gemeldet und dokumentiert. Kommunikationsmittel sind im Sicherheitsdienst wichtig, besonders bei Alleinarbeit und in Gefahrbereichen.",
          followUpQuestions: [
            "Warum ist Kommunikation beim Kontrollgang so wichtig?",
            "Was tun Sie, wenn kein Ersatzgerät vorhanden ist?",
            "Warum ist Alleinarbeit besonders riskant?"
          ],
          examinerNotes: "Eigenschutz, Meldewege, Ersatzkommunikation und keine riskante Alleinarbeit sind entscheidend.",
          criticalMistakes: [
            "Kontrollgang trotz fehlender Kommunikation riskant fortsetzen",
            "Ausfall nicht melden",
            "Keine Ersatzkommunikation versuchen",
            "Eigenschutz vergessen"
          ],
          difficulty: "medium",
          examRelevance: "high",
          ihkSimilarityRisk: "low",
          sourceStyle: "accaoui_original"
        },
        {
          id: "oral-d-014",
          mode: "oral",
          sheet: "D",
          order: 14,
          examinerBlock: 3,
          examinerRole: "Prüfer 3",
          topic: "Umgang mit Waffen",
          subtopic: "Reizstoffsprühgerät / gefährlicher Gegenstand / Einlasskontrolle",
          examinerQuestion: "Bei einer Kontrolle finden Sie ein Pfefferspray. Wie bewerten Sie die Lage und was tun Sie?",
          modelAnswer: "Ich bleibe ruhig, halte Abstand und bewerte die Situation nach Hausordnung, Objektvorgaben und konkreter Gefahrenlage. Ich darf den Zutritt verweigern, wenn das Mitführen solcher Gegenstände im Objekt nicht erlaubt ist oder eine Gefahr besteht. Ich nehme das Pfefferspray nicht eigenmächtig mit Gewalt weg und führe keine erzwungene Durchsuchung durch. Bei akuter Bedrohung, Straftatverdacht oder unklarer Rechtslage informiere ich Einsatzleitung und Polizei. Der Vorgang wird sachlich dokumentiert.",
          followUpQuestions: [
            "Dürfen Sie das Pfefferspray einfach wegnehmen?",
            "Welche Rolle spielt die Hausordnung?",
            "Wann informieren Sie die Polizei?"
          ],
          examinerNotes: "Zutrittsverweigerung kann zulässig sein, eigenmächtige Wegnahme oder erzwungene Durchsuchung nicht.",
          criticalMistakes: [
            "Gegenstand eigenmächtig mit Gewalt wegnehmen",
            "Gefahr unterschätzen",
            "Hausordnung und Objektvorgaben ignorieren",
            "Keine Polizei bei konkreter Bedrohung erwähnen"
          ],
          difficulty: "medium",
          examRelevance: "medium",
          ihkSimilarityRisk: "low",
          sourceStyle: "accaoui_original"
        },
        {
          id: "oral-d-015",
          mode: "oral",
          sheet: "D",
          order: 15,
          examinerBlock: 3,
          examinerRole: "Prüfer 3",
          topic: "Grundzüge der Sicherheitstechnik",
          subtopic: "Stromausfall / Notbeleuchtung / Evakuierung / Meldekette",
          examinerQuestion: "Im Objekt fällt der Strom aus, die Beleuchtung ist gestört und Besucher werden unruhig. Was sind Ihre wichtigsten Maßnahmen?",
          modelAnswer: "Ich bleibe ruhig, informiere sofort Einsatzleitung oder Leitstelle und halte mich an den Alarm- oder Notfallplan des Objekts. Ich achte auf Fluchtwege, Notausgänge und mögliche Gefahrenstellen. Besucher werden ruhig informiert und, falls erforderlich, zu sicheren Bereichen oder Ausgängen geleitet. Ich prüfe nicht eigenmächtig technische Anlagen, wenn ich dafür nicht zuständig bin. Bei Gefahr für Personen werden Feuerwehr, Rettungsdienst oder Polizei informiert. Alle Maßnahmen und Beobachtungen werden dokumentiert.",
          followUpQuestions: [
            "Warum ist Ruhe in dieser Lage besonders wichtig?",
            "Welche Bedeutung haben Fluchtwege und Notbeleuchtung?",
            "Wann müssen externe Stellen informiert werden?"
          ],
          examinerNotes: "Notfallplan, Meldekette, freie Fluchtwege, keine Technikarbeiten ohne Zuständigkeit und Dokumentation müssen genannt werden.",
          criticalMistakes: [
            "Panik verstärken",
            "Fluchtwege und Notausgänge nicht beachten",
            "Eigenmächtig an technischen Anlagen arbeiten",
            "Keine Meldekette und Dokumentation nennen"
          ],
          difficulty: "medium",
          examRelevance: "medium",
          ihkSimilarityRisk: "low",
          sourceStyle: "accaoui_original"
        }
      ]
    },
    {
      id: "oral_sheet_e_v254a",
      title: "Prüfungsbogen E",
      description: "15 Accaoui-original Fallfragen für die mündliche §34a-Prüfung mit Fokus auf Auftrag, Hausordnung, Meldekette, schwierige Personensituationen, Brandschutz, Objektschutz und Kollegen-Fehlverhalten.",
      status: "draft",
      questions: [
        {
          id: "oral-e-001",
          mode: "oral",
          sheet: "E",
          order: 1,
          examinerBlock: 1,
          examinerRole: "Prüfer 1",
          topic: "Gewerberecht",
          subtopic: "Dienstanweisung / Auftrag / rechtmäßiges Handeln",
          examinerQuestion: "Ein Auftraggeber verlangt von Ihnen, eine Person „mit allen Mitteln“ aus dem Gebäude zu entfernen. Wie gehen Sie mit einer solchen Anweisung um?",
          modelAnswer: "Ich darf keine rechtswidrige oder unverhältnismäßige Anweisung ausführen. Auch wenn der Auftraggeber das Hausrecht hat, muss ich als Sicherheitsmitarbeiter rechtmäßig, verhältnismäßig und nach Dienstanweisung handeln. Ich würde die Situation prüfen, die Person zunächst ruhig ansprechen und sie zum Verlassen auffordern. Körperliches Eingreifen kommt nur in engen rechtlichen Grenzen in Betracht, zum Beispiel bei Gefahr, Notwehr oder wenn andere rechtliche Voraussetzungen vorliegen. Bei Unsicherheit informiere ich Einsatzleitung oder Polizei und dokumentiere den Vorgang.",
          followUpQuestions: [
            "Müssen Sie jede Anweisung des Auftraggebers befolgen?",
            "Was bedeutet Verhältnismäßigkeit?",
            "Wann darf körperliches Eingreifen überhaupt in Betracht kommen?"
          ],
          examinerNotes: "Der Prüfling muss erkennen, dass auch Auftraggeberanweisungen rechtmäßig und verhältnismäßig sein müssen.",
          criticalMistakes: [
            "Rechtswidrige Anweisung blind ausführen",
            "„Mit allen Mitteln“ als Freibrief verstehen",
            "Keine Verhältnismäßigkeit nennen",
            "Keine Einsatzleitung oder Polizei bei Unsicherheit erwähnen"
          ],
          difficulty: "hard",
          examRelevance: "high",
          ihkSimilarityRisk: "low",
          sourceStyle: "accaoui_original"
        },
        {
          id: "oral-e-002",
          mode: "oral",
          sheet: "E",
          order: 2,
          examinerBlock: 1,
          examinerRole: "Prüfer 1",
          topic: "Bürgerliches Gesetzbuch",
          subtopic: "Hausrecht / Hausordnung / Zutrittsverweigerung",
          examinerQuestion: "Eine Person möchte ein Objekt betreten, obwohl sie die Hausordnung nicht akzeptiert. Welche Möglichkeiten haben Sie?",
          modelAnswer: "Wenn die Hausordnung Voraussetzung für den Zutritt ist, kann der Zutritt verweigert werden. Ich erkläre ruhig und sachlich, welche Regeln gelten und dass der Zutritt nur bei Einhaltung dieser Regeln möglich ist. Ich darf die Person nicht diskriminieren oder willkürlich behandeln. Wenn die Person aggressiv wird oder versucht, trotzdem einzudringen, fordere ich Unterstützung an und informiere je nach Lage die Polizei. Grundlage ist das Hausrecht des Berechtigten, nicht eine eigene polizeiliche Befugnis.",
          followUpQuestions: [
            "Warum ist die Hausordnung für den Zutritt wichtig?",
            "Was wäre eine unzulässige Zutrittsverweigerung?",
            "Wann muss die Polizei eingeschaltet werden?"
          ],
          examinerNotes: "Hausordnung und Hausrecht müssen sachlich, nicht willkürlich oder diskriminierend angewendet werden.",
          criticalMistakes: [
            "Hausordnung willkürlich anwenden",
            "Diskriminierende Auswahl treffen",
            "Polizeibefugnisse behaupten",
            "Aggressives Eindringen nicht melden"
          ],
          difficulty: "medium",
          examRelevance: "high",
          ihkSimilarityRisk: "low",
          sourceStyle: "accaoui_original"
        },
        {
          id: "oral-e-003",
          mode: "oral",
          sheet: "E",
          order: 3,
          examinerBlock: 1,
          examinerRole: "Prüfer 1",
          topic: "Grundzüge der Sicherheitstechnik",
          subtopic: "Verdächtiger Gegenstand / Absicherung / Meldekette",
          examinerQuestion: "Sie finden im Objekt eine herrenlose Tasche. Wie verhalten Sie sich sicher und rechtlich korrekt?",
          modelAnswer: "Ich fasse die Tasche nicht unüberlegt an und öffne sie nicht eigenmächtig. Zuerst sichere ich den Bereich ab, halte Personen fern und informiere Einsatzleitung oder Leitstelle. Je nach Objektanweisung und Gefahrenlage wird die Polizei hinzugezogen. Ich beobachte die Umgebung und frage, wenn gefahrlos möglich, ob jemand die Tasche zuordnen kann. Wichtig sind Eigenschutz, Absicherung, Meldekette und Dokumentation.",
          followUpQuestions: [
            "Warum darf man die Tasche nicht einfach öffnen?",
            "Welche Stellen informieren Sie?",
            "Was dokumentieren Sie?"
          ],
          examinerNotes: "Verdächtige Gegenstände dürfen nicht unkontrolliert bewegt oder geöffnet werden. Meldekette und Eigenschutz sind entscheidend.",
          criticalMistakes: [
            "Tasche öffnen oder herumtragen",
            "Bereich nicht absichern",
            "Meldekette nicht einhalten",
            "Gefahr unterschätzen"
          ],
          difficulty: "hard",
          examRelevance: "high",
          ihkSimilarityRisk: "low",
          sourceStyle: "accaoui_original"
        },
        {
          id: "oral-e-004",
          mode: "oral",
          sheet: "E",
          order: 4,
          examinerBlock: 1,
          examinerRole: "Prüfer 1",
          topic: "Datenschutzrecht",
          subtopic: "Videoüberwachung / Weitergabe / Zweckbindung",
          examinerQuestion: "Ein Mitarbeiter des Auftraggebers fordert Sie auf, eine Videoaufnahme privat an ihn weiterzuleiten. Was ist zu beachten?",
          modelAnswer: "Videoaufnahmen enthalten personenbezogene Daten und dürfen nicht privat weitergegeben werden. Eine Weitergabe ist nur zulässig, wenn es dafür eine rechtliche Grundlage, einen berechtigten Zweck und eine befugte Stelle gibt. Ich verweise auf den offiziellen Dienstweg und informiere die zuständige verantwortliche Stelle. Private Weiterleitung per Handy, Messenger oder E-Mail ist unzulässig. Datenschutz, Zweckbindung, Zugriffsbeschränkung und Dokumentation müssen beachtet werden.",
          followUpQuestions: [
            "Warum sind Videoaufnahmen personenbezogene Daten?",
            "Was bedeutet Zweckbindung?",
            "Warum ist private Weiterleitung gefährlich?"
          ],
          examinerNotes: "Der Prüfling muss Datenschutz auch gegenüber Auftraggebermitarbeitern sauber begrenzen.",
          criticalMistakes: [
            "Video privat versenden",
            "Auftraggeberwunsch automatisch als Rechtsgrundlage ansehen",
            "Datenschutz nicht beachten",
            "Keine zuständige Stelle einschalten"
          ],
          difficulty: "hard",
          examRelevance: "high",
          ihkSimilarityRisk: "low",
          sourceStyle: "accaoui_original"
        },
        {
          id: "oral-e-005",
          mode: "oral",
          sheet: "E",
          order: 5,
          examinerBlock: 1,
          examinerRole: "Prüfer 1",
          topic: "Umgang mit Menschen",
          subtopic: "Professionelle Kommunikation / Beschwerde / Konfliktkontrolle",
          examinerQuestion: "Ein Besucher behauptet, er sei Anwalt und droht Ihnen sofort mit Anzeige. Wie bleiben Sie professionell?",
          modelAnswer: "Ich bleibe ruhig, sachlich und höflich. Ich lasse mich nicht einschüchtern und provoziere nicht zurück. Ich erkläre kurz die Grundlage meiner Maßnahme, zum Beispiel Hausordnung, Auftrag oder Sicherheitsregel. Wenn die Person eine Beschwerde einreichen möchte, verweise ich an die zuständige Stelle. Ich diskutiere nicht endlos über Rechtsfragen vor Ort. Bei weiterer Eskalation hole ich Unterstützung und dokumentiere den Vorfall sachlich.",
          followUpQuestions: [
            "Warum sollten Sie nicht emotional reagieren?",
            "Wie erklären Sie Ihre Maßnahme kurz und sachlich?",
            "Wann ziehen Sie Einsatzleitung oder Kollegen hinzu?"
          ],
          examinerNotes: "Professionelle Distanz und sachliche Kommunikation sind wichtiger als eine Rechtsdiskussion vor Ort.",
          criticalMistakes: [
            "Sich einschüchtern lassen und Regeln aufgeben",
            "Zurückdrohen oder beleidigen",
            "Endlose Rechtsdiskussion führen",
            "Vorfall nicht dokumentieren"
          ],
          difficulty: "medium",
          examRelevance: "high",
          ihkSimilarityRisk: "low",
          sourceStyle: "accaoui_original"
        },
        {
          id: "oral-e-006",
          mode: "oral",
          sheet: "E",
          order: 6,
          examinerBlock: 2,
          examinerRole: "Vorsitz",
          topic: "Umgang mit Menschen",
          subtopic: "Distanz / Körpersprache / Eigensicherung",
          examinerQuestion: "Ein aggressiver Gast steht sehr nah vor Ihnen, berührt Sie aber noch nicht. Welche Maßnahmen sind angemessen?",
          modelAnswer: "Ich achte zuerst auf meinen Eigenschutz und halte oder schaffe Abstand. Ich spreche ruhig, klar und bestimmt, ohne selbst aggressiv zu wirken. Ich setze eine deutliche Grenze, zum Beispiel: „Bitte treten Sie einen Schritt zurück, dann können wir sprechen.“ Ich positioniere mich so, dass ich einen Ausweichweg habe, und fordere bei Bedarf Unterstützung an. Körperliches Eingreifen ist nicht automatisch gerechtfertigt, nur weil jemand nah steht. Bei konkreter Gefahr, Angriff oder Drohung informiere ich Kollegen, Einsatzleitung oder Polizei.",
          followUpQuestions: [
            "Warum ist Abstand in dieser Lage wichtig?",
            "Welche Formulierung wäre deeskalierend?",
            "Wann wird aus Nähe eine konkrete Gefahr?"
          ],
          examinerNotes: "Nähe allein rechtfertigt nicht automatisch körperliches Eingreifen. Abstand, Grenze und Eigensicherung sind Pflichtpunkte.",
          criticalMistakes: [
            "Sofort körperlich schubsen",
            "Ohne Ausweichweg stehen bleiben",
            "Selbst aggressiv auftreten",
            "Keine Unterstützung anfordern"
          ],
          difficulty: "medium",
          examRelevance: "high",
          ihkSimilarityRisk: "low",
          sourceStyle: "accaoui_original"
        },
        {
          id: "oral-e-007",
          mode: "oral",
          sheet: "E",
          order: 7,
          examinerBlock: 2,
          examinerRole: "Vorsitz",
          topic: "Umgang mit Menschen",
          subtopic: "Gruppendynamik / Zutrittskontrolle / Unterstützung",
          examinerQuestion: "Eine Gruppe versucht, gemeinsam durch eine Zutrittskontrolle zu drängen. Wie handeln Sie?",
          modelAnswer: "Ich bleibe ruhig und versuche, die Gruppe nicht allein körperlich aufzuhalten. Ich spreche klar und deutlich, dass der Zutritt nur einzeln und nach Kontrolle möglich ist. Ich fordere sofort Unterstützung an und informiere die Einsatzleitung. Wenn möglich, spreche ich eine führende Person der Gruppe direkt an. Ich achte auf Fluchtwege, Eigenschutz und darauf, keine Panik oder Eskalation auszulösen. Bei Gewalt, Drohung oder Durchbruch wird die Polizei informiert und der Vorfall dokumentiert.",
          followUpQuestions: [
            "Warum ist Gruppendynamik gefährlich?",
            "Warum sollte man nicht allein körperlich blockieren?",
            "Wann wird die Polizei eingeschaltet?"
          ],
          examinerNotes: "Der Prüfling muss Gruppendynamik erkennen und darf keine Alleinlösung mit Körperkraft beschreiben.",
          criticalMistakes: [
            "Allein gegen die Gruppe körperlich vorgehen",
            "Gruppe beleidigen oder provozieren",
            "Keine Unterstützung anfordern",
            "Durchbruch oder Gewalt nicht melden"
          ],
          difficulty: "hard",
          examRelevance: "high",
          ihkSimilarityRisk: "low",
          sourceStyle: "accaoui_original"
        },
        {
          id: "oral-e-008",
          mode: "oral",
          sheet: "E",
          order: 8,
          examinerBlock: 2,
          examinerRole: "Vorsitz",
          topic: "Umgang mit Menschen",
          subtopic: "Kinderschutz / hilflose Lage / Kommunikation",
          examinerQuestion: "Ein Kind hat seine Eltern im Einkaufszentrum verloren und weint. Wie reagieren Sie?",
          modelAnswer: "Ich spreche das Kind ruhig, freundlich und kindgerecht an und bringe es, wenn möglich, an einen sicheren, gut einsehbaren Ort. Ich informiere Kollegen, Einsatzleitung oder die zuständige Stelle im Objekt. Ich lasse das Kind nicht allein und übergebe es nicht einfach an irgendeine fremde Person. Die Eltern werden über sichere Wege gesucht, zum Beispiel über die Information oder Durchsage nach Objektvorgabe. Bei Verdacht auf Gefahr, Vernachlässigung oder wenn die Eltern nicht auffindbar sind, wird die Polizei informiert. Der Vorgang wird dokumentiert.",
          followUpQuestions: [
            "Warum darf das Kind nicht allein gelassen werden?",
            "Warum darf man es nicht einfach einer fremden Person übergeben?",
            "Wann informieren Sie die Polizei?"
          ],
          examinerNotes: "Kinderschutz verlangt ruhiges Handeln, sichere Übergabe und klare Meldekette.",
          criticalMistakes: [
            "Kind allein lassen",
            "Kind an unbekannte Person übergeben",
            "Keine Meldung an Einsatzleitung oder Objektstelle",
            "Keine Dokumentation"
          ],
          difficulty: "medium",
          examRelevance: "high",
          ihkSimilarityRisk: "low",
          sourceStyle: "accaoui_original"
        },
        {
          id: "oral-e-009",
          mode: "oral",
          sheet: "E",
          order: 9,
          examinerBlock: 2,
          examinerRole: "Vorsitz",
          topic: "Umgang mit Menschen",
          subtopic: "Würde / Hausrecht / Deeskalation",
          examinerQuestion: "Eine Person wirkt obdachlos, sitzt im Eingangsbereich und wird von Kunden beschimpft. Wie gehen Sie menschlich und rechtssicher vor?",
          modelAnswer: "Ich behandle die Person respektvoll und ohne abwertende Sprache. Zuerst prüfe ich die Lage: Liegt eine Störung, Gefahr oder ein Verstoß gegen die Hausordnung vor? Ich spreche die Person ruhig an und erkläre, falls nötig, die Regeln des Objekts. Gleichzeitig verhindere ich, dass Kunden die Person weiter beschimpfen oder die Situation eskaliert. Wenn die Person hilfsbedürftig wirkt, kann je nach Lage Unterstützung, Sozialdienst, Rettungsdienst oder Polizei informiert werden. Hausrecht darf nicht willkürlich oder diskriminierend angewendet werden. Der Vorfall wird sachlich dokumentiert.",
          followUpQuestions: [
            "Warum ist respektvolle Sprache wichtig?",
            "Wann kann Hausrecht angewendet werden?",
            "Was tun Sie, wenn Kunden die Person beleidigen?"
          ],
          examinerNotes: "Der Prüfling muss Würde, Hausrecht und Hilfebedarf zusammen denken.",
          criticalMistakes: [
            "Obdachlose Person abwerten",
            "Hausrecht diskriminierend anwenden",
            "Beschimpfungen durch Kunden ignorieren",
            "Hilfebedarf nicht erkennen"
          ],
          difficulty: "medium",
          examRelevance: "high",
          ihkSimilarityRisk: "low",
          sourceStyle: "accaoui_original"
        },
        {
          id: "oral-e-010",
          mode: "oral",
          sheet: "E",
          order: 10,
          examinerBlock: 2,
          examinerRole: "Vorsitz",
          topic: "Umgang mit Menschen",
          subtopic: "Neutralität / Konfliktklärung / Dokumentation",
          examinerQuestion: "Nach einem Streit behaupten beide Beteiligten, der jeweils andere habe angefangen. Wie vermeiden Sie falsche Parteinahme?",
          modelAnswer: "Ich bleibe neutral und bewerte nur, was ich selbst wahrgenommen habe oder was durch Zeugen nachvollziehbar ist. Ich trenne die Beteiligten räumlich, beruhige die Lage und höre die Angaben sachlich an, ohne vorschnell Schuld zuzuweisen. Wenn eine Straftat, Verletzung oder konkrete Gefahr im Raum steht, informiere ich Einsatzleitung und gegebenenfalls Polizei oder Rettungsdienst. In der Dokumentation trenne ich eigene Beobachtungen, Aussagen der Beteiligten und Aussagen von Zeugen klar voneinander. Ich entscheide nicht wie ein Gericht, sondern sichere die Lage.",
          followUpQuestions: [
            "Warum ist Neutralität wichtig?",
            "Wie trennen Sie eigene Wahrnehmung von Aussagen anderer?",
            "Wann informieren Sie Polizei oder Rettungsdienst?"
          ],
          examinerNotes: "Neutralität und saubere Dokumentation sind hier wichtiger als Schuldzuweisung.",
          criticalMistakes: [
            "Vorschnell Partei ergreifen",
            "Vermutungen als Tatsachen dokumentieren",
            "Beteiligte weiter zusammen streiten lassen",
            "Sich als Richter aufspielen"
          ],
          difficulty: "medium",
          examRelevance: "high",
          ihkSimilarityRisk: "low",
          sourceStyle: "accaoui_original"
        },
        {
          id: "oral-e-011",
          mode: "oral",
          sheet: "E",
          order: 11,
          examinerBlock: 3,
          examinerRole: "Prüfer 3",
          topic: "Grundzüge der Sicherheitstechnik",
          subtopic: "Brandverdacht / Meldekette / Gefahrenprüfung",
          examinerQuestion: "Sie bemerken Rauchgeruch, aber es wurde noch kein Brandalarm ausgelöst. Was tun Sie?",
          modelAnswer: "Ich nehme Rauchgeruch ernst und ignoriere ihn nicht. Ich informiere sofort Einsatzleitung, Leitstelle oder die zuständige Objektstelle und handle nach Alarm- oder Brandschutzordnung. Wenn es gefahrlos möglich ist, prüfe ich aus sicherer Entfernung die Lage, ohne mich selbst zu gefährden. Ich halte Fluchtwege frei und achte darauf, ob Personen gefährdet sind. Bei konkretem Brandverdacht oder sichtbarem Rauch werden Feuerwehr und weitere zuständige Stellen informiert. Alle Beobachtungen und Maßnahmen werden dokumentiert.",
          followUpQuestions: [
            "Warum darf Rauchgeruch nicht ignoriert werden?",
            "Wann informieren Sie die Feuerwehr?",
            "Warum ist Eigenschutz wichtig?"
          ],
          examinerNotes: "Rauchgeruch ist als mögliche Gefahr zu behandeln. Meldekette und Eigenschutz müssen genannt werden.",
          criticalMistakes: [
            "Rauchgeruch ignorieren",
            "Allein in gefährliche Bereiche gehen",
            "Keine Meldekette einhalten",
            "Fluchtwege und Personen im Objekt nicht beachten"
          ],
          difficulty: "medium",
          examRelevance: "high",
          ihkSimilarityRisk: "low",
          sourceStyle: "accaoui_original"
        },
        {
          id: "oral-e-012",
          mode: "oral",
          sheet: "E",
          order: 12,
          examinerBlock: 3,
          examinerRole: "Prüfer 3",
          topic: "Grundzüge der Sicherheitstechnik",
          subtopic: "Notausgang / Fluchtweg / Brandschutz",
          examinerQuestion: "Die Notausgangstür ist verschlossen, obwohl Personen im Gebäude sind. Wie handeln Sie?",
          modelAnswer: "Eine verschlossene Notausgangstür kann eine erhebliche Gefahr darstellen. Ich informiere sofort Einsatzleitung oder die zuständige Objektstelle und sichere den Bereich, damit niemand im Notfall gefährdet wird. Wenn möglich, wird die Tür nach Objektvorgabe sofort freigegeben oder ein alternativer Fluchtweg klar kenntlich gemacht. Ich dokumentiere die Feststellung und die getroffenen Maßnahmen. Bei akuter Gefahr oder wenn der Mangel nicht sofort beseitigt werden kann, werden weitere zuständige Stellen informiert, zum Beispiel Feuerwehr oder Betreiber.",
          followUpQuestions: [
            "Warum sind Notausgänge besonders wichtig?",
            "Was tun Sie, wenn die Tür nicht sofort geöffnet werden kann?",
            "Warum muss der Mangel dokumentiert werden?"
          ],
          examinerNotes: "Fluchtwege und Notausgänge haben hohe Sicherheitsrelevanz und dürfen nicht ignoriert werden.",
          criticalMistakes: [
            "Verschlossene Notausgangstür ignorieren",
            "Keine Meldung machen",
            "Personen im Gebäude nicht berücksichtigen",
            "Fluchtwegproblem nicht dokumentieren"
          ],
          difficulty: "hard",
          examRelevance: "high",
          ihkSimilarityRisk: "low",
          sourceStyle: "accaoui_original"
        },
        {
          id: "oral-e-013",
          mode: "oral",
          sheet: "E",
          order: 13,
          examinerBlock: 3,
          examinerRole: "Prüfer 3",
          topic: "Grundzüge der Sicherheitstechnik",
          subtopic: "Zutrittssicherung / Kontrollgang / Objektschutz",
          examinerQuestion: "Bei einem Kontrollgang sehen Sie eine offene Außentür in einem sensiblen Objektbereich. Was sind Ihre nächsten Schritte?",
          modelAnswer: "Ich bewerte die Lage vorsichtig und achte zuerst auf Eigenschutz. Eine offene Außentür kann auf unbefugten Zutritt, Einbruch, technischen Defekt oder Nachlässigkeit hinweisen. Ich informiere Einsatzleitung oder Leitstelle, sichere den Bereich nach Dienstanweisung und prüfe, ob Personen oder Spuren erkennbar sind, ohne Beweise zu verändern oder mich zu gefährden. Je nach Lage wird die Polizei oder eine zuständige Objektstelle informiert. Die Feststellung, Uhrzeit, Ort und Maßnahmen werden dokumentiert.",
          followUpQuestions: [
            "Warum darf man nicht einfach unvorsichtig hineingehen?",
            "Welche Informationen melden Sie?",
            "Wann rufen Sie die Polizei?"
          ],
          examinerNotes: "Der Prüfling muss eine mögliche Einbruchslage erkennen und Eigenschutz beachten.",
          criticalMistakes: [
            "Ohne Meldung allein in den Bereich gehen",
            "Mögliche Einbruchslage unterschätzen",
            "Keine Dokumentation erstellen",
            "Spuren verändern oder Beweise anfassen"
          ],
          difficulty: "medium",
          examRelevance: "high",
          ihkSimilarityRisk: "low",
          sourceStyle: "accaoui_original"
        },
        {
          id: "oral-e-014",
          mode: "oral",
          sheet: "E",
          order: 14,
          examinerBlock: 3,
          examinerRole: "Prüfer 3",
          topic: "Gewerberecht",
          subtopic: "Dienstanweisung / Objektunterweisung / Verantwortlichkeit",
          examinerQuestion: "Sie sollen einen Dienst übernehmen, obwohl Sie keine klare Einweisung zum Objekt erhalten haben. Was tun Sie?",
          modelAnswer: "Ich darf einen sicherheitsrelevanten Dienst nicht blind übernehmen, wenn mir wesentliche Informationen fehlen. Ich frage nach Dienstanweisung, Objektbesonderheiten, Ansprechpartnern, Notfallwegen, Meldekette, Schlüsseln, Alarmanlagen und besonderen Gefahren. Wenn wichtige Informationen fehlen, informiere ich Einsatzleitung oder Vorgesetzte und lasse mir die Einweisung geben. Ich dokumentiere, wenn eine Einweisung nicht oder nur unvollständig erfolgt ist. Ziel ist, den Dienst sicher und fachgerecht auszuführen, nicht einfach unvorbereitet zu handeln.",
          followUpQuestions: [
            "Welche Informationen brauchen Sie vor Dienstbeginn?",
            "Warum ist eine Objektunterweisung wichtig?",
            "Was tun Sie, wenn niemand eine Einweisung geben kann?"
          ],
          examinerNotes: "Dienstanweisung und Objektunterweisung sind für sichere Dienstausführung wesentlich.",
          criticalMistakes: [
            "Dienst ohne Wissen über Objekt und Notfallwege blind übernehmen",
            "Keine Rückfrage stellen",
            "Meldekette und Ansprechpartner nicht kennen",
            "Fehlende Einweisung nicht melden oder dokumentieren"
          ],
          difficulty: "medium",
          examRelevance: "high",
          ihkSimilarityRisk: "low",
          sourceStyle: "accaoui_original"
        },
        {
          id: "oral-e-015",
          mode: "oral",
          sheet: "E",
          order: 15,
          examinerBlock: 3,
          examinerRole: "Prüfer 3",
          topic: "Umgang mit Menschen",
          subtopic: "Kollegiales Fehlverhalten / Befugnisüberschreitung / Meldepflicht",
          examinerQuestion: "Ein Kollege überschreitet seine Befugnisse und behandelt eine Person grob. Wie reagieren Sie?",
          modelAnswer: "Ich schaue nicht weg. Wenn eine Person gefährdet ist oder der Kollege rechtswidrig handelt, muss die Situation gestoppt oder entschärft werden, soweit das sicher möglich ist. Ich bleibe ruhig, spreche den Kollegen sachlich an und versuche, die Lage zu deeskalieren. Bei Gefahr, Gewalt oder Straftatverdacht informiere ich sofort Einsatzleitung und gegebenenfalls Polizei. Der Vorfall wird sachlich dokumentiert. Kollegialität bedeutet nicht, rechtswidriges Verhalten zu decken.",
          followUpQuestions: [
            "Warum darf man Fehlverhalten eines Kollegen nicht decken?",
            "Wann informieren Sie Einsatzleitung oder Polizei?",
            "Wie bleiben Sie dabei professionell?"
          ],
          examinerNotes: "Der Prüfling muss Loyalität von rechtswidrigem Decken unterscheiden.",
          criticalMistakes: [
            "Wegschauen oder Fehlverhalten decken",
            "Selbst aggressiv in den Konflikt einsteigen",
            "Keine Meldung an Einsatzleitung",
            "Rechtswidrige Gewalt verharmlosen"
          ],
          difficulty: "hard",
          examRelevance: "high",
          ihkSimilarityRisk: "low",
          sourceStyle: "accaoui_original"
        }
      ]
    }
  ]
};

window.ACCAOUI_ORAL_SHEETS_V23 = ACCAOUI_ORAL_SHEETS_V23;
