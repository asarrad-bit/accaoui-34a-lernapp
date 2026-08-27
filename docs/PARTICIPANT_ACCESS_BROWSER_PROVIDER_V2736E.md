# Teilnehmerzugangs-Browser-Provider v27.36e

## Ziel

v27.36e bereitet die vorhandene Teilnehmerzugangskette browserfähig vor,
ohne sie in `index.html` oder `app.js` zu aktivieren. Die App nutzt diese
Kette noch nicht.

## CommonJS-Kompatibilität und kontrollierte Browser-Exports

Die CommonJS-Verträge der Bestandsmodule bleiben erhalten:

- `require(...).createParticipantAccessAdapter`
- `require(...).createParticipantAccessBootstrapBridge`

Zusätzlich stellen sie kontrollierte Browser-Exports bereit:

- `window.ACCAOUI_PARTICIPANT_ACCESS_ADAPTER_FACTORY`
- `window.ACCAOUI_PARTICIPANT_ACCESS_BOOTSTRAP_BRIDGE_FACTORY`

Vorhandene inkompatible Globalwerte werden nicht überschrieben. Die Änderung
betrifft ausschließlich die Export- und Packaging-Grenze; die Bestandslogik
bleibt unverändert.

## Provider und Kompositionskette

Der neue Browser-Provider installiert ausschließlich
`window.ACCAOUI_PARTICIPANT_ACCESS_APP_PROVIDER`. Seine eigene öffentliche
Oberfläche besitzt ausschließlich resolveAccess().

Intern verbindet er ausschließlich den vorhandenen
`window.ACCAOUI_SUPABASE_BOOTSTRAP`, die beiden kontrollierten Factory-Globals
und eine lokale UTC-Zeitquelle. Die Brücken-Factory erhält exakt `bootstrap`,
`createParticipantAccessAdapter` und `utcNow`. Die Entscheidung wird an
`resolveAccess()` der bestehenden Brücke delegiert; es gibt keine duplizierte Fachlogik.

## Sicherheitsgrenze und Fail-closed-Regeln

Fehlende oder ungültige Dependencies, werfende Getter oder Factories,
ungültige Brücken, Throw/Reject sowie ungültige Ergebnisse werden fail-closed
als sicherer technischer Blockierungszustand ausgegeben. Nur
`allowed: true` zusammen mit `code: "access_allowed"` ist zulässig.
Ein Blockierungsergebnis darf nie `access_allowed` tragen. Rohfehler,
automatische Client-Erzeugung und lokaler Fallback sind ausgeschlossen.

Der Provider ruft keine Client-, Auth- oder Tabellen-API direkt auf und kennt
keine Teilnehmer-, Einschreibungs-, Kurs- oder frei injizierte Nutzerlogik.
Ein vorhandener kompatibler oder fremder App-Provider wird nicht überschrieben.

## Unveränderte App-Grenze

`app.js`, `index.html` und `style.css` bleiben unverändert. Es gibt keine
Aktivierung im Browser-HTML und keine Behauptung einer bereits genutzten
Browser-Verbindung.

## Lokale Prüfung

Der Checker verwendet ausschließlich lokale synthetische Tests in Node/VM.
Er prüft CommonJS und Browser, Komposition, Delegation, Fail-closed-Fälle,
Kollisionsschutz, Frozen-Dateien und echte Manipulationen. Testergebnis:

- Positivprüfungen: 22 PASS
- Negativprüfungen: 31 PASS
- Manipulationsprüfungen: 16 PASS
- v27.36b-, v27.36c- und v27.36d-Regressionsprüfungen: PASS

Supabase live: NEIN

Supabase NICHT LIVE. echte Keys: NEIN. echte Teilnehmerdaten: NEIN.
