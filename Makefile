# Makefile para o Projeto Fitness (usando Docker Compose v2)

.PHONY: help up down ps logs sh-backend sh-db clean
.DEFAULT_GOAL := help

help:
	@echo "------------------------------------------------------------------------"
	@echo " Comandos disponíveis para o projeto:"
	@echo "------------------------------------------------------------------------"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'
	@echo "------------------------------------------------------------------------"

up: ## Inicia todos os serviços em background (usando o plugin Compose v2).
	docker compose up --build -d

down: ## Para e remove todos os contêineres (usando o plugin Compose v2).
	docker compose down

ps: ## Lista os contêineres em execução (usando o plugin Compose v2).
	docker compose ps

logs: ## Exibe os logs dos serviços. Use 'make logs service=backend'.
	docker compose logs -f $(service)

sh-backend: ## Acessa o terminal do contêiner da API backend.
	docker compose exec backend /bin/sh

sh-db: ## Acessa o terminal do contêiner do banco de dados.
	docker compose exec db /bin/sh

clean: ## ATENÇÃO: Para tudo, remove contêineres, volumes e imagens.
	docker compose down -v --rmi all --remove-orphans