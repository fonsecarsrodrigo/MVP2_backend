.PHONY: run clear seed clear_venv create_venv activate_venv deactivate_venv delete_venv install_dependencies ruff docker-be-build docker-be-run docker-stop

BE_DIR := bora-be-service
# Backend (Flask): context is repo root so requirements.txt + bora-be-service/ are available
docker-be-build:
	docker build -f $(BE_DIR)/bora-be.docker -t bora-be .

docker-be-run:
	docker run --rm -p 5001:5001 -v ./bora-be-service/database_model/database:/app/database_model/database bora-be &

# Stop every running container (no-op if none are running)
docker-stop:
	@ids=$$(docker ps -q); [ -n "$$ids" ] && docker stop $$ids || true

# Backend (Flask in bora-be-service)
run :
	@cd $(BE_DIR) && export FLASK_APP=customer_area.py && \
	export FLASK_ENV=development && \
	flask run --port=5001 &

clear_venv:
	@rm -rf venv

create_venv:
	@python3 -m venv venv

# Make runs recipes in a subshell.
# ctivating a venv here cannot affect your terminal.
# Run the printed command yourself in bash/zsh.
activate_venv:
	@echo "source $(CURDIR)/venv/bin/activate"

deactivate_venv:
	@echo "Run \`deactivate\` in the shell where the venv is active (not via make)."

delete_venv:
	@rm -rf venv

install_dependencies:
	@pip3 install -r requirements.txt

clear:
	@pkill -f flask || true
	@rm -f $(BE_DIR)/database_model/database/*.sqlite3

seed:
	@python3 $(BE_DIR)/scripts/seed_database.py

ruff:
	@ruff check .
