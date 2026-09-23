# Dashboard-Bereitschaftsanzeige v27.37h

## Ursache

Das produktive Dashboard zeigte statisch `72%` Bereitschaft, obwohl keine fachlich freigegebene Prüfungsreife- oder Bereitschaftsberechnung existiert. Die feste Prozentangabe konnte daher einen nicht belegten Lernstand vermitteln.

## Lösung

Der bestehende Bereitschaftsbereich zeigt neutral:

```text
Bereitschaft
Nicht berechnet
```

v27.37h führt keine neue Prüfungsreifeformel ein und wertet keine Nutzer-, Prüfungs-, Lernstands-, Lernkarten- oder Fehlertrainingsdaten aus. Es entstehen keine neuen Storage-Keys und keine Netzwerk-, Auth-, Teilnehmer-, Supabase- oder Datenbankoperationen. Die Anzeige enthält keine Unterrichts-, Bestehens- oder Prüfungsreifeaussage.

## Exakter Implementierungsscope

- `index.html`: ausschließlich `72%` im bestehenden Bereitschafts-`score-box` durch `Nicht berechnet` ersetzt
- `tools/check-dashboard-readiness-display-v2737h.py`: strukturelle, bytegenaue und semantische Prüfung einschließlich Manipulationsfällen
- `docs/DASHBOARD_READINESS_DISPLAY_V2737H.md`: dieser Vertrag
- `tools/preflight.py`: ausschließlich Registrierung des neuen Checkers

Der übrige Inhalt von `index.html`, `app.js`, `style.css`, `patch-v21.js` und `test/index.html` bleibt gegenüber der Implementierungsbasis byte-identisch. Beide Browser-Loader bleiben unverändert deaktiviert. Cache-Busting und der beobachtete Browser-Cache-Effekt sind ausdrücklich nicht Teil dieses Tasks. Supabase bleibt NICHT LIVE.
