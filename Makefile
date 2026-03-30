.PHONY: docker-build docker-run docker-stop server-clear server-lint server-run server-seed venv-activate venv-clear venv-create venv-deactivate venv-delete venv-install-dependencies

BE_DIR := bora-be-service

# Backend (Flask): context is repo root so requirements.txt + bora-be-service/ are available
docker-build:
	docker build -f $(BE_DIR)/bora-be.docker -t bora-be .

docker-run:
	docker run --rm -p 5001:5001 -v ./bora-be-service/database_model/database:/app/database_model/database bora-be &

# Stop every running container (no-op if none are running)
docker-stop:
	@ids=$$(docker ps -q); [ -n "$$ids" ] && docker stop $$ids || true

server-clear:
	@pkill -f flask || true
	@rm -f $(BE_DIR)/database_model/database/*.sqlite3

server-lint:
	@ruff check .

# Backend (Flask in bora-be-service)
server-run:
	@cd $(BE_DIR) && export FLASK_APP=customer_area.py && \
	export FLASK_ENV=development && \
	flask run --port=5001 &

server-seed:
	@python3 $(BE_DIR)/scripts/seed_database.py

# Make runs recipes in a subshell.
# Activating a venv here cannot affect your terminal.
# Run the printed command yourself in bash/zsh.
venv-activate:
	@echo "source $(CURDIR)/venv/bin/activate"

venv-clear:
	@rm -rf venv

venv-create:
	@python3 -m venv venv

venv-deactivate:
	@echo "Run \`deactivate\` in the shell where the venv is active (not via make)."

venv-delete:
	@rm -rf venv

venv-install-dependencies:
	@pip3 install -r requirements.txt
