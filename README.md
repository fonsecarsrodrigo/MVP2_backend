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

Equivalent Make targets: `make create_venv`, then run the command printed by `make activate_venv`, then `make install_dependencies`.

## Run the server

From the repository root (with the venv active and dependencies installed):

```bash
make run
```

This runs `flask run` inside `bora-be-service` on port **5001** (process is started in the background). Open the app in a browser:

- [http://127.0.0.1:5001](http://127.0.0.1:5001) — redirects to OpenAPI UI
- [http://127.0.0.1:5001/openapi](http://127.0.0.1:5001/openapi) — Swagger / OpenAPI docs

The API exposes JSON endpoints for customers and travel plans (for example `/add_customer`, `/get_customers`, `/add_travel_plan`, and related GET/DELETE routes). CORS is enabled for browser clients.

## Reset database

Stops Flask processes matching `flask` and removes `*.sqlite3` files in `bora-be-service/database_model/database/`:

```bash
make clear
```

## Seed sample data

The seed script calls the running API. Start the server first, then:

```bash
make seed
```

By default it targets `http://0.0.0.0:5001`. Override with `SEED_API_BASE` if needed:

```bash
SEED_API_BASE=http://127.0.0.1:5001 make seed
```

## Lint

```bash
make ruff
```

## Docker

From the repository root (build context must be the root so `requirements.txt` and `bora-be-service/` are available):

```bash
make docker-be-build
make docker-be-run
```

The container listens on port **5001** and mounts `./bora-be-service/database_model/database` so the SQLite file persists on the host.

Stop running containers:

```bash
make docker-stop
```

## Makefile reference

| Target | Description |
|--------|-------------|
| `run` | Start Flask on port 5001 from `bora-be-service` |
| `clear` | Kill matching Flask processes; remove `*.sqlite3` under `database_model/database/` |
| `seed` | Run `scripts/seed_database.py` against the API |
| `install_dependencies` | `pip3 install -r requirements.txt` |
| `create_venv` / `clear_venv` / `delete_venv` | Manage `venv/` at repo root |
| `activate_venv` / `deactivate_venv` | Print reminders (venv cannot be activated from Make alone) |
| `ruff` | Run Ruff on the repository |
| `docker-be-build` | Build image `bora-be` |
| `docker-be-run` | Run container on port 5001 with DB volume mount |
| `docker-stop` | Stop all running Docker containers |
