# v27.37f – Auth-/Session-Anbindung an den App-Start

Die Anbindung verwendet ausschließlich den bereits autorisierten Auth-Modus. Supabase bleibt NICHT LIVE.

## Startvertrag

Die feste Loader-ID ist `accaoui-participant-auth-session-browser-loader`. Ausschließlich das exakte Attribut `data-enabled="true"` fordert den Auth-Modus an. Vorhandene Auth-Globals allein aktivieren ihn nicht. Beide vorhandenen Loader bleiben in index.html unverändert mit `data-enabled="false"` eingebunden.

Der angeforderte Pfad lautet: lokale Sperrprüfung → Auth-Readiness → `resolveSession()` → erforderliche Teilnehmerzugangsprüfung → App-Start.

Lokale Test-/Sperrzustände behalten Vorrang vor Readiness und Provideroperationen. Bestehende Hinweisansichten werden wiederverwendet. Nur ein gültiges eingefrorenes Sessionergebnis mit exakt `ok=true` und `code="session_available"` erlaubt die Fortsetzung zur Zugangsprüfung. Es erlaubt allein keinen App-Start. Gültige fehlende/ungültige Sessionergebnisse führen zu `login_required`; technische Fehler zu `access_error`.

Der bestehende `resolveParticipantAccessAppProviderV2736D()` bleibt unverändert. Er entscheidet weiterhin anhand der bestehenden Teilnehmer-/Enrollment-/Kurskette. Ein fehlender Zugangsprovider im angeforderten Auth-Modus führt zu einer Sperre, auch wenn der Zugangs-Loader nicht aktiviert ist. Keine frei übergebene userId und keine duplizierte Fachlogik.

## Vier Schalterkombinationen

A steht für die Auth-/Session-Anforderung, Z für die Teilnehmerzugangs-Loader-Anforderung.

| Kombination | Verhalten |
| --- | --- |
| A=false, Z=false | Bisheriger lokaler Start einschließlich vorhandener injizierter Zugangsprovider; kein Auth-Aufruf. |
| A=false, Z=true | Bisherige Zugangs-Readiness und Zugangsprüfung; kein Auth-Aufruf. |
| A=true, Z=false | Auth-Readiness und Sessionprüfung, anschließend vorhandene Zugangsprüfung; ohne gültigen Zugangsprovider gesperrt. |
| A=true, Z=true | Auth-Readiness, Sessionprüfung, Zugangs-Readiness, Zugangsprüfung; erst access_allowed startet die App. |

Fehlende Elemente, fehlende Attribute und andere Werte aktivieren nicht. Auch Boolean true, Großschreibung, Leerzeichen und "1" sind kein exaktes "true". Eine strukturell fehlende Lookup-Funktion erhält den lokalen Testpfad. Geworfene Fehler beim Lesen einer vorhandenen Aktivierungsgrenze führen nach der vorrangigen lokalen Sperrprüfung generisch zur Sperre. Die Aktivierung wird einmal erfasst und während asynchroner Wartezeiten nicht herabgestuft.

## Grenzen und Parallelität

Der Auth-Start wartet auf `ACCAOUI_PARTICIPANT_AUTH_SESSION_BROWSER_LOADER_READY`. Nur der eingefrorene einfache Datensatz mit exakt eigenen Datenfeldern requested=true, ready=true und status="ready" erlaubt den Providerzugriff. Fehler, Rejects, ungültige Ergebnisse und ausstehende Readiness geben nicht frei.

Der vorhandene Auth-/Session-Provider muss seine unveränderliche eigene Browser-Grenze und seine eingefrorene Oberfläche resolveSession/signIn/signOut erfüllen. Aufgerufen wird ausschließlich resolveSession(), einmal mit Provider als this und ohne Argumente. Getter, geerbte oder zusätzliche Ergebnisfelder, mutable Ergebnisse und widersprüchliche Codes werden abgewiesen. Exceptions werden nicht in UI oder Logs ausgegeben.

Boot und Auth-Flow reservieren jeweils vor asynchroner Arbeit ihren einmaligen Promise. Alle wiederholten und parallelen Aufrufe teilen den Startversuch; Fehler öffnen ihn nicht erneut. Die Hinweisansicht wird höchstens einmal aufgerufen. Provider-/Readiness-Globals werden nicht überschrieben. Eine ausstehende Promise führt zu keiner Freigabe; die tatsächliche Auth-Loader-Kette behält ihre vorhandenen Stufen-Timeouts.

Keine Client-Erzeugung. Keine SDK-/Config-Nachladung durch den neuen Auth-Startpfad. initAppBoot() verzweigt vor loadOptionalSupabaseConfig() direkt zur Auth-Prüfung. Der bisherige lokale Config-/Health-Pfad bleibt für den normalen lokalen Boot erhalten. Nach einem bereits gestarteten Auth-Flow wird kein zusätzlicher Boot-Nachladepfad begonnen.

Keine Anmeldung/Abmeldung, kein Loginformular, keine automatische Anmeldung, kein Logout-Flow, kein neuer Live-Schalter, keine SQL-/Migrationsänderung.

## Änderungsgrenze und Prüfungen

In app.js wurden nur initAppBoot(), initAuthFlow() und der explizit begrenzte Hilfsblock unmittelbar vor initAppBoot() geändert. Hinweisansichten, startLocalApp(), Lernlogik, Config-/Health-Funktionen und Zugangsresolver bleiben unverändert. preflight.py registriert ausschließlich den neuen Checker.

Der neue Checker prüft alle vier Kombinationen, Readiness-Verzögerung, Session- und Zugangsfehler, fehlende Provider, Frozen-/Property-Verträge, lokale Vorränge, tatsächlichen DOMContentLoaded-/Boot-Einstieg, Aufrufreihenfolge und -zahlen sowie parallelen und wiederholten Start. Die unveränderten lokalen Auth-/Session- und Zugangsmodule werden zusätzlich mit einem bereits vorhandenen synthetischen Client geprüft, einschließlich verweigertem Teilnehmer-, Enrollment- oder Kurszugang und zwischenzeitlich verschwundener Session. Es werden keine echten Daten verwendet.

Zehn syntaktisch gültige semantische Manipulationen prüfen insbesondere gelockertes true, übersprungene Readiness/Session/Zugangsprüfung, widersprüchliche Sessionwerte, fehlenden Provider-Fallback, entfernte Einmalreservierungen, Config-Nachladung und verlorenen Sperrvorrang. Historische Einzelchecker und ihre Harnesses bleiben unverändert und laufen im autorisierten zentralen Nachfolgeprofil.

Erwartete Arbeitsphase: `v2737f_implementation_prepared`. Kontinuitätschecker, isolierte Lifecycle-Tests, vollständiger Preflight mit Regressionen, git diff --check und exakter Vier-Dateien-Scope sind verpflichtend.

Nicht committet. Nicht gepusht. Supabase bleibt NICHT LIVE.
