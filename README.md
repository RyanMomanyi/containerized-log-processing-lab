# Containerized Log Processing Lab
A **local learning lab** demonstrating log ingestion, a file-backed worker queue, PostgreSQL persistence, shell health checks, and failure recovery. Generates only synthetic records.

## Architecture
`synthetic JSONL logs -> Python ingestion -> shared queue -> Python worker -> PostgreSQL`

## Requirements
Python 3.10+, Podman + podman-compose (or Docker + Docker Compose). From the repository root:

```bash
bash scripts/setup.sh
python3 -m app.generate 20
bash scripts/healthcheck.sh
```

If using Podman on macOS, start your Podman machine first (`podman machine start`). If setup fails, inspect `podman compose logs` or `docker compose logs`.

## Run automated tests
```bash
python3 -m unittest discover -s tests -v
```

## Observe and clean up
```bash
podman compose logs -f ingestion worker   # or docker compose logs -f ingestion worker
podman compose down                       # or docker compose down
```
The first query may fail until the worker initializes the table; retry after records are processed.

## Configuration
See `.env.example`. Set variables using a local `.env` (excluded from Git). The shared `data/` folder is created on first run. The Docker image uses Python 3.12 and `psycopg`.

## Reliability tests and limitations
See [manual test plan](docs/test-plan.md). This educational design provides **at-least-once-like** processing rather than exactly-once guarantees; replayed source data or crashes can create duplicates. For production, add durable offsets, atomic queue writes, idempotency keys, secrets management, metrics, and an actual broker.

## Cloud deployment considerations
Use managed PostgreSQL, private networking, a managed queue, secret storage, least-privilege IAM roles, centralized monitoring, and container orchestration. This project does **not** deploy to the cloud.
