# Manual validation plan
1. Run `bash scripts/setup.sh` then `python3 -m app.generate 20` (from the repository root).
2. Allow a few seconds for ingestion and processing; use `bash scripts/healthcheck.sh` to verify records in PostgreSQL.
3. Append the line `{bad json` to `data/application.jsonl`; verify ingestion logs report a rejected record and processing continues.
4. Stop the database (`podman compose stop db` or `docker compose stop db`), append new generated logs, then start the database again. Verify the queue empties and the database count increases.
5. Restart ingestion and worker; verify they resume processing newly appended log lines. Note: ingestion offsets are in-memory, so restarting ingestion can re-ingest existing source lines. This is a lab limitation, not exactly-once delivery.
6. Run `python3 -m unittest discover -s tests -v`.

**Known limitations:** File-backed queue is shared storage rather than a production message broker. A crash between database insert and queue-file deletion can duplicate an event. Queue writes are not atomic. Database passwords in the default local Compose configuration are for disposable local testing only.
