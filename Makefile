# --------------------
# Variables
# --------------------

project_name ?= vocode-telephony-app


# --------------------
# Formatting & helpers
# --------------------

bold=$(shell echo "\033[1;35m")
highlight=$(shell echo "\033[36m")
normal=$(shell echo "\033[0m")
print = @printf "\n$(bold)$(1)$(normal)\n"

.PHONY: default
default: clean format lint test help

.PHONY: help
help: ## Display this help screen
	$(call print,Available make targets:\n)
	@grep -h -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "$(highlight)%-30s$(normal) %s\n", $$1, $$2}'
	@printf "\n"


# --------------------
# Docker
# --------------------

.PHONY: up
up: ## Create & start all containers
	$(call print,Starting containers...\n)
	docker compose -f docker-compose.yml up --build --remove-orphans

.PHONY: watch-logs
watch-logs: ## Watch the app container logs
	$(call print,Watching app container logs...)
	docker logs -f $(project_name)

.PHONY: stop
stop: ## Stop all containers
	$(call print,Stopping containers...\n)
	docker compose -f docker-compose.yml stop

.PHONY: down
down: stop ## Stop and remove all containers
	$(call print,Closing containers...\n)
	docker compose -f docker-compose.yml down

.PHONY: prune
prune: prunecheck down ## Spin down this project's Docker containers and run a Docker system/volume prune
	$(call print,Pruning Docker system and volumes...\n)
	docker system prune -a
	docker volume prune

.PHONY: prunecheck
prunecheck:
	@printf "\n$(bold)WARNING! This will spin down this project's Docker containers and run a Docker system/volume prune."
	@printf "\n$(normal)Are you sure you want to continue? [y/N] " && read ans && [ $${ans:-N} = y ]


# --------------------
# Docker - specific containers
# --------------------

.PHONY: enter
enter: ## Start local app environment
	$(call print,Running app env for bash...\n)
	docker compose -f docker-compose.yml run app /bin/bash

.PHONY: enter-app
enter-app: ## Enter the app container
	$(call print,Entering app container...)
	docker exec -it $(project_name) /bin/bash
