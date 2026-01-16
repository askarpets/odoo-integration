HOST := 0.0.0.0
PORT := 8080

.PHONY: format
format:
	@ poetry run black app
	@ poetry run isort app

.PHONY: lint
lint:
	@ poetry run flake8 app
	@ poetry run isort -c --diff app
	@ poetry run black --check --diff app
	@ poetry run mypy app

.PHONY: start
start:
	poetry run uvicorn app.main:app --host $(HOST) --port $(PORT) --reload

.PHONY: build
build:
	@ docker-compose build

.PHONY: up
up:
	@ docker-compose up --force-recreate
