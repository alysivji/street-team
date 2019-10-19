.PHONY: help

help: ## This help
	@echo "Makefile for managing application:\n"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

up: ## start local dev environment; run migrations
	python streetteam/manage.py runserver
	make migrate-up

migration: ## create migration app="app" msg="msg"
	python streetteam/manage.py makemigrations $(app) $(msg)

migrate-up: ## run all migration
	python streetteam/manage.py migrate
