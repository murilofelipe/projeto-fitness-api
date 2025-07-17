[Read this in English](README.en.md)

# Plataforma de Engenharia de Dados para Análise de Performance e Retenção no Setor Fitness

Este projeto, desenvolvido como Projeto Aplicado para o curso de Engenharia de Dados, consiste na criação de uma plataforma completa para o monitoramento de treinos de academia. A solução envolve uma API backend, um pipeline de dados ETL, um Data Warehouse para análises e uma suíte de testes automatizados, tudo orquestrado em um ambiente containerizado com Docker.

## 🎯 Tabela de Conteúdos
1.  [Tecnologias Utilizadas](#-tecnologias-utilizadas)
2.  [Estrutura do Projeto](#-estrutura-do-projeto)
3.  [Configuração do Ambiente Local](#-configuração-do-ambiente-local)
4.  [Comandos Principais (Makefile)](#️-comandos-principais-makefile)
5.  [Testando a Aplicação](#-testando-a-aplicação)
6.  [Acessando o Banco de Dados](#-acessando-o-banco-de-dados)
7.  [Próximos Passos](#-próximos-passos)

## ✨ Tecnologias Utilizadas

- **Backend:** Python, FastAPI
- **Banco de Dados:** PostgreSQL (para OLTP e OLAP)
- **Pipeline de Dados:** Python com Pandas
- **Containerização:** Docker e Docker Compose
- **Testes:** Pytest, pytest-cov, pytest-asyncio
- **Qualidade de Código:** Black, isort, Flake8, Mypy
- **Frontend (Planejado):** Vue.js

## 📂 Estrutura do Projeto

O projeto está organizado com a seguinte estrutura de pastas na sua raiz:

```
/projeto-fitness/
|
|-- /backend/
|   |-- /src/
|   |-- /scripts/
|   |-- /tests/
|   |-- Dockerfile
|   |-- pyproject.toml
|   |-- requirements.txt
|
|-- .gitignore
|-- docker-compose.yml
|-- Makefile
|-- README.md
|-- README.en.md
```

## 🚀 Configuração do Ambiente Local

Siga estes passos para configurar e executar o projeto em uma nova máquina.

### Pré-requisitos
-   Git
-   Docker e Docker Compose

### Instalação

1.  **Clone o repositório:**
    ```bash
    git clone git@github.com:murilofelipe/projeto-fitness.git
    cd projeto-fitness
    ```

2.  **Suba os contêineres:**
    Este comando irá construir as imagens Docker e iniciar os serviços da API e do banco de dados.
    ```bash
    make up
    ```

3.  **Crie a estrutura do banco de dados:**
    ```bash
    make db-init
    ```

4.  **Popule o banco com dados de teste:**
    ```bash
    make db-seed
    ```
Ao final, o ambiente estará 100% funcional.

## 🛠️ Comandos Principais (Makefile)

O `Makefile` é o painel de controle do projeto. Use `make help` para ver todos os comandos.

| Comando | Descrição |
| :--- | :--- |
| `make up` | Inicia todos os serviços em background. |
| `make down` | Para e remove todos os contêineres. |
| `make clean`| Para tudo e apaga os volumes de dados (zera o banco). |
| `make ps` | Mostra o status dos contêineres. |
| `make logs` | Mostra os logs dos serviços em tempo real. |
| `make sh-backend` | Acessa o terminal do contêiner da API. |
| `make sh-db`| Acessa o terminal do contêiner do banco de dados. |
| `make db-init` | Cria as tabelas no banco de dados. |
| `make db-seed` | Popula o banco com dados de teste. |
| `make etl:run`| Executa o pipeline de ETL completo. |
| `make sh-backend` | Acessa o terminal do contêiner da API. |
| `make sh-db`| Acessa o terminal do contêiner do banco de dados. |

## 🧪 Qualidade de Código e Testes

A qualidade do código é garantida por uma suíte de formatação, linting, checagem de tipos e testes.

| Comando | Descrição |
| :--- | :--- |
| `make format` | Formata automaticamente todo o código com `isort` e `black`. |
| `make lint` | Procura por erros e problemas de estilo com `flake8`. |
| `make typecheck` | Verifica a consistência dos tipos com `mypy`. |
| `make test` | Roda a suíte de testes automatizados com `pytest`. |
| `make test:cov-html` | Roda os testes e gera o relatório de cobertura em HTML. |
| `make test:all` | **(Recomendado)** Roda todas as verificações de qualidade em sequência. |

### Documentação da API
Com o ambiente no ar, a documentação interativa (Swagger UI) está disponível em:
- **[http://localhost:8000/docs](http://localhost:8000/docs)**

## 🗄️ Acessando o Banco de Dados

Use um cliente de sua preferência (DBeaver, DataGrip, etc.) com as seguintes credenciais:
-   **Host:** `localhost`
-   **Porta:** `5432`
-   **Banco de Dados:** `fitness_db`
-   **Usuário:** `myuser`
-   **Senha:** `mypassword`

## 🔮 Próximos Passos

-   **Sprint 1:** Concluída ✅
-   **Sprint 2:** Concluída ✅
-   **Sprint 3:** Desenvolver o dashboard em Vue.js para visualização dos dados e preparar a apresentação final do projeto.