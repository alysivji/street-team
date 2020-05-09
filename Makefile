.PHONY: help logs

help: ## This help
	@echo "Makefile for managing application:\n"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

build:  ## rebuild app
	docker-compose build

up: ## start local dev environment; run migrations
	docker-compose up -d
	make migrate-up
	make superuser

down: ## stop local dev environment
	docker-compose down

attach: ## attach to process for debugging purposes
	docker attach `docker-compose ps -q app`

migration: ## create migration app="app" msg="msg"
	docker-compose exec app python streetteam/manage.py makemigrations -n "$(msg)" $(app)

migration-empty: ## create empty migration app="app" msg="msg"
	docker-compose exec app python streetteam/manage.py makemigrations --empty -n "$(msg)" $(app)

migrate-up: ## run all migration
	docker-compose exec app python streetteam/manage.py migrate $(app)

migration-sql: ## generate sql for migrations app="app" migration="migration"
	docker-compose exec app python streetteam/manage.py sqlmigrate $(app) $(migration)

dropdb:  ## drop all tables in development database
	psql -d postgresql://streetteam_user:streetteam_password@localhost:9432/streetteam -f ./scripts/drop_all_tables.sql

shell: ## log into into app container -- bash-shell
	docker-compose exec app bash

startapp: ## create an app="app"
	mkdir streetteam/apps/$(app)
	docker-compose exec app python streetteam/manage.py startapp $(app) streetteam/apps/$(app)

superuser:  ## add superuser to database
	docker-compose exec app python streetteam/manage.py createsuperuser_parameterized --noinput --email admin@dev.com --password password

ngrok: ## start ngrok to forward port
	ngrok http 8000

test: ## run tests
	docker-compose exec app pytest $(args)

test-cov: ## run tests with coverage.py
	docker-compose exec app pytest --cov ./streetteam $(args)

test-covhtml: ## run tests and load html coverage report
	docker-compose exec app pytest --cov ./streetteam --cov-report html && open ./htmlcov/index.html

requirements: ## generate requirements.txt using piptools
	pip-compile --output-file=requirements.txt requirements.in

shell-db:  ## log into database container -- psql
	docker-compose exec db psql -w --username "streetteam_user" --dbname "streetteam"

devshell: ## open ipython shell with application context
	docker-compose exec app python streetteam/manage.py shell_plus

prod-up: ## start prod environment
	docker-compose -f docker-compose.prod.yml up -d

prod-down: ## stop prod environment
	docker-compose -f docker-compose.prod.yml down

prod-build: ## build prod containers
	docker-compose -f docker-compose.prod.yml build

logs: ## attach to logs
	docker logs `docker-compose ps -q app`
