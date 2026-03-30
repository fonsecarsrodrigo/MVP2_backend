# Bora Orneles — Customer Area API

Backend service for customer and travel-plan data. It is a **Flask** application with **OpenAPI** documentation (**flask-openapi3**), **SQLAlchemy** models, and a **SQLite** database under `bora-be-service/database_model/database/`.

## Repository layout

| Path | Purpose |
|------|---------|
| `requirements.txt` | Python dependencies (install from repository root) |
| `Makefile` | Common tasks: run server, seed DB, Docker, venv helpers, lint |
| `bora-be-service/customer_area.py` | Flask app entrypoint (`FLASK_APP`) |
| `bora-be-service/database_model/` | SQLAlchemy models, engine, and SQLite file location |
| `bora-be-service/schemas/` | Pydantic/OpenAPI request and response schemas |
| `bora-be-service/scripts/seed_database.py` | Seeds data via the HTTP API |
| `bora-be-service/bora-be.docker` | Docker image for the backend |

## Prerequisites

- Python 3 (Dockerfile uses 3.11)
- `pip`
- Optional: `make`, Docker (for container workflow)

## Local setup

Create and activate a virtual environment at the repository root, then install dependencies:

```bash
python3 -m venv venv
source venv/bin/activate   # macOS / Linux
pip install -r requirements.txt
```

Equivalent Make targets: `make venv-create`, then run the command printed by `make venv-activate`, then `make venv-install-dependencies`.

## Run the server

From the repository root (with the venv active and dependencies installed):

```bash
make server-run
```

This runs `flask run` inside `bora-be-service` on port **5001** (process is started in the background). Open the app in a browser:

- [http://127.0.0.1:5001](http://127.0.0.1:5001) — redirects to OpenAPI UI
- [http://127.0.0.1:5001/openapi](http://127.0.0.1:5001/openapi) — Swagger / OpenAPI docs

The API exposes JSON endpoints for customers and travel plans (for example `/add_customer`, `/get_customers`, `/add_travel_plan`, and related GET/DELETE routes). CORS is enabled for browser clients.

## Reset database

Stops Flask processes matching `flask` and removes `*.sqlite3` files in `bora-be-service/database_model/database/`:

```bash
make server-clear
```

## Seed sample data

The seed script calls the running API. Start the server first, then:

```bash
make server-seed
```

By default it targets `http://0.0.0.0:5001`. Override with `SEED_API_BASE` if needed:

```bash
SEED_API_BASE=http://127.0.0.1:5001 make server-seed
```

## Lint

```bash
make server-lint
```

## Docker

From the repository root (build context must be the root so `requirements.txt` and `bora-be-service/` are available):

```bash
make docker-build
make docker-run
```

The container listens on port **5001** and mounts `./bora-be-service/database_model/database` so the SQLite file persists on the host.

Stop running containers:

```bash
make docker-stop
```

## Makefile reference

Targets are listed in alphabetical order (same as the `Makefile`).

| Target | Description |
|--------|-------------|
| `docker-build` | Build Docker image `bora-be` (context: repo root) |
| `docker-run` | Run container on port 5001 with DB volume mount |
| `docker-stop` | Stop all running Docker containers |
| `server-clear` | Kill matching Flask processes; remove `*.sqlite3` under `database_model/database/` |
| `server-lint` | Run Ruff on the repository |
| `server-run` | Start Flask on port 5001 from `bora-be-service` |
| `server-seed` | Run `scripts/seed_database.py` against the API |
| `venv-activate` | Print the `source …/venv/bin/activate` command |
| `venv-clear` | Remove `venv/` |
| `venv-create` | Create `venv/` with `python3 -m venv` |
| `venv-deactivate` | Reminder to run `deactivate` in your shell |
| `venv-delete` | Remove `venv/` (same as `venv-clear`) |
| `venv-install-dependencies` | `pip3 install -r requirements.txt` |
