.PHONY: help

help: ## This help
	@echo "Makefile for managing application:\n"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

build:  ## rebuild app
	docker-compose build

up: ## start local dev environment; run migrations
	docker-compose up -d
	make migrate-up

attach: ## attach to process for debugging purposes
	docker attach `docker-compose ps -q app`

migration: ## create migration app="app" msg="msg"
	docker-compose exec app python streetteam/manage.py makemigrations $(app) $(msg)

migrate-up: ## run all migration
	docker-compose exec app python streetteam/manage.py migrate

shell: ## log into into app container -- bash-shell
	docker-compose exec app bash

startapp: ## create an app="app"
	mkdir streetteam/apps/$(app)
	docker-compose exec app python streetteam/manage.py startapp $(app) streetteam/apps/$(app)

ngrok: ## start ngrok to forward port
	ngrok http 8000
