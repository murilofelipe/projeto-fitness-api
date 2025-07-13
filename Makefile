# Makefile para o Projeto Fitness (v3 - Verificado)

SHELL := /bin/bash

# O .PHONY garante que o make execute o comando mesmo que já exista um arquivo com o mesmo nome do alvo.
.PHONY: help up down ps logs sh-backend sh-db db-init db-seed test test-cov test-cov-html lint typecheck format format-check test-all clean

# Define um alvo padrão, que será executado se você digitar apenas "make".
.DEFAULT_GOAL := help

# Comando para exibir a ajuda com todos os comandos disponíveis.
help:
	@echo "------------------------------------------------------------------------"
	@echo " Comandos disponíveis para o projeto:"
	@echo "------------------------------------------------------------------------"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'
	@echo "------------------------------------------------------------------------"


# --- Comandos do Docker Compose ---

up: .env ## Inicia todos os serviços em background e constrói as imagens se necessário.
		@echo "✅ Tudo pronto! Iniciando os contêineres..."
		docker compose up --build -d

# Cria o .env APENAS se ele não existir
.env:
	@echo "📄 Arquivo .env não encontrado. Criando..."
	@echo "UID=$$(id -u)" > .env
	@echo "GID=$$(id -g)" >> .env
	@echo "✨ Arquivo .env criado com UID/GID do usuário local."

down: ## Para e remove todos os contêineres definidos no docker-compose.
	@echo "🛑 Parando e removendo os contêineres..."
	docker compose down

ps: ## Lista os contêineres que estão rodando e seus status.
	docker compose ps

logs: ## Exibe os logs dos serviços. Use 'make logs service=backend'.
	docker compose logs -f $(service)

# --- Comandos de Acesso aos Contêineres ---

sh-backend: ## Acessa o terminal (shell) do contêiner da API backend.
	docker compose exec backend /bin/sh

sh-db: ## Acessa o terminal (shell) do contêiner do banco de dados PostgreSQL.
	docker compose exec db /bin/sh

# --- Comandos de Banco de Dados ---

db-init: ## [SETUP] Cria todas as tabelas no banco de dados a partir dos modelos.
	docker compose exec backend python -m scripts.init_db

db-seed: ## [SETUP] Popula o banco de dados com dados de teste através do seeder.
	docker compose exec backend python -m scripts.seed_data

# --- Comandos de Teste ---

test: ## Roda a suíte de testes padrão com pytest.
	docker compose exec backend pytest tests/

test-cov: ## Roda os testes e exibe o relatório de cobertura no terminal.
	docker compose exec backend pytest --cov=src tests/

test-cov-html: ## Roda os testes e gera o relatório de cobertura em HTML.
	docker compose exec backend pytest --cov=src --cov-report=html tests/
	docker compose exec backend chmod -R 755 htmlcov/
	docker compose exec -u root backend chown -R $(shell id -u):$(shell id -g) htmlcov/



# --- Comandos de Qualidade de Código ---

lint: ## Roda o linter (flake8) para encontrar erros e problemas de estilo.
	docker compose exec backend flake8 src tests scripts

typecheck: ## Roda o verificador de tipos (mypy) para checar a consistência dos tipos.
	docker compose exec backend mypy src

# --- Comandos de Formatação ---
format-check: ## Verifica se o código precisa de formatação, sem alterar os arquivos.
	docker compose exec backend isort . --check-only
	docker compose exec backend black . --check

format: ## Formata automaticamente todo o código com isort e black.
	docker compose exec backend isort .
	docker compose exec backend black .

test-all: ## [CICLO COMPLETO] Roda linter, type checker e os testes. O ideal antes de um commit.
	make format-check
	make lint
	make typecheck
	make test
	
# --- Comandos de Limpeza ---

clean: ## ATENÇÃO: Para tudo, remove contêineres, VOLUMES (apaga os dados) e imagens.
	@echo "🧹 Limpando o contêineres, VOLUMES (apaga os dados) e imagens."
	docker compose down -v --rmi all --remove-orphans