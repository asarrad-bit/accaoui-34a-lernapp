# Disposable PostgreSQL-Treiber-Readiness

Stand: v27.32d
Status: metadatenbasiert implementiert, nicht live ausgeführt

## Ziel

Der Resolver prüft ausschließlich über
`importlib.metadata.version("psycopg")`, ob die ausgewählte
Distribution vorhanden ist und exakt Version 3.3.4 besitzt.

## Entscheidungen

- fehlend: `driver_not_installed`
- Metadatenfehler: `driver_metadata_unavailable`
- falsche Version: `driver_version_mismatch`
- exakte Version: `metadata_ready_import_locked`

Auch bei exakter Version bleiben Treiberimport und Verbindung
gesperrt.

## Sicherheitsgrenze

Keine Installation, kein Treiberimport, kein Netzwerkzugriff,
keine Datenbankverbindung, keine SQL-Migration und keine
Frontend-Anbindung.
