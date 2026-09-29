[Read this in English](README.en.md)

# Plataforma de Engenharia de Dados para Análise de Performance e Retenção no Setor Fitness

Este projeto, desenvolvido como Projeto Aplicado para o curso de Engenharia de Dados, consiste na criação de uma plataforma completa para o monitoramento de treinos de academia. A solução envolve uma API backend, um pipeline de dados ETL, um Data Warehouse para análises, uma suíte de testes automatizados e um dashboard interativo, tudo orquestrado em um ambiente containerizado com Docker.

## 🎯 Tabela de Conteúdos
1.  [Principais Funcionalidades](#-principais-funcionalidades)
2.  [Tecnologias Utilizadas](#-tecnologias-utilizadas)
3.  [Estrutura do Projeto](#-estrutura-do-projeto)
4.  [Configuração do Ambiente Local](#-configuração-do-ambiente-local)
5.  [Comandos Principais (Makefile)](#️-comandos-principais-makefile)
6.  [Qualidade de Código e Testes](#-qualidade-de-código-e-testes)
7.  [Acessando os Serviços](#-acessando-os-serviços)
8.  [Próximos Passos](#-próximos-passos)

## ✨ Principais Funcionalidades

* **API Robusta:** Backend desenvolvido em Python com FastAPI, servindo dados operacionais (do OLTP) e analíticos (do OLAP/DWH).
* **Pipeline ETL:** Processo de Extração, Transformação e Carga com Pandas que move e modela dados de um banco OLTP para um Data Warehouse (DWH) em Star Schema.
* **Ambiente Containerizado:** Aplicação full-stack (Backend, Frontend, Banco de Dados) totalmente gerenciada com Docker e Docker Compose para fácil configuração.
* **Qualidade de Código Garantida:** Suíte de testes automatizados com `pytest`, verificação de tipos com `mypy` e padronização de código com `flake8`, `black` e `isort`.
* **Dashboard Interativo:** Frontend desenvolvido em Vue.js 3 com TypeScript, apresentando visualizações de dados dinâmicas, como:
    * Frequência de treinos (semanal, mensal e anual).
    * Evolução de performance (volume e carga máxima).
    * Calendário de treinos com status (planejado, executado, não executado).
    * Filtros dinâmicos por aluno e por exercício.

## 🛠️ Tecnologias Utilizadas

- **Backend:** Python, FastAPI
- **Banco de Dados:** PostgreSQL (OLTP & OLAP)
- **ETL:** Pandas
- **Containerização:** Docker, Docker Compose
- **Frontend:** Vue.js 3, TypeScript, Vite, Pinia
- **Gráficos:** Chart.js
- **Testes:** Pytest, Vitest
- **Qualidade de Código:** Black, isort, Flake8, Mypy

## 📂 Estrutura do Projeto

O projeto está organizado com a seguinte estrutura de pastas na sua raiz:

```
/projeto-fitness-api/
|
|-- /.github/ (CI de qualidade)
|-- /backend/
|-- /frontend/
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
    git clone git@github.com:murilofelipe/projeto-fitness-api.git
    cd projeto-fitness-api
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
5.  **Execute o Pipeline ETL para popular o Data Warehouse:**
    ```bash
    make etl-run
    ```
Ao final, o ambiente estará 100% funcional.

## 🛠️ Comandos Principais (Makefile)

O `Makefile` é o painel de controle do projeto. Use `make help` para ver todos os comandos.

| Comando | Descrição |
| :--- | :--- |
| `make up` | Inicia todos os serviços em background. |
| `make down` | Para e remove todos os contêineres. |
| `make clean`| Para tudo e apaga os volumes de dados (zera o banco). |
| `make db-init` | Cria as tabelas no banco de dados. |
| `make db-seed` | Popula o banco OLTP com dados de teste. |
| `make etl-run`| Executa o pipeline de ETL completo para o DWH. |
| `make sh-backend` | Acessa o terminal do contêiner da API. |
| `make sh-db`| Acessa o terminal do contêiner do banco de dados. |

## 🧪 Qualidade de Código e Testes

A qualidade do código é garantida por uma suíte de formatação, linting, checagem de tipos e testes.

| Comando | Descrição |
| :--- | :--- |
| `make format-check` | Verifica a formatação sem alterar arquivos. |
| `make format` | Formata automaticamente todo o código com `isort` e `black`. |
| `make lint` | Procura por erros e problemas de estilo com `flake8`. |
| `make typecheck` | Verifica a consistência dos tipos com `mypy`. |
| `make test` | Roda a suíte de testes automatizados com `pytest`. |
| `make test-cov` | Roda os testes e exibe a cobertura no terminal. |
| `make test-cov-html` | Roda os testes e gera o relatório de cobertura em HTML. |
| `make test-all` | **(Recomendado)** Roda todas as verificações de qualidade em sequência. |

## 🖥️ Acessando os Serviços

* **Frontend (Dashboard):**
    * [http://localhost:5173](http://localhost:5173)

* **Backend (Documentação da API):**
    * [http://localhost:8000/docs](http://localhost:8000/docs)

* **Banco de Dados (via cliente de BD):**
    * **Host:** `localhost`
    * **Porta:** `5432`
    * **Banco de Dados:** `fitness_db`
    * **Usuário:** `myuser`
    * **Senha:** `mypassword`

## 🔮 Próximos Passos

Com o MVP concluído, as futuras evoluções do projeto podem incluir:
-   **Orquestração do Pipeline ETL:** Substituir a execução manual do script ETL por um orquestrador de mercado como o **Apache Airflow**.
-   **Testes End-to-End (E2E):** Adicionar uma suíte de testes com **Cypress** ou **Playwright** para validar os fluxos do usuário na interface do frontend.
-   **Otimização para Produção:** Criar um `Dockerfile` multi-estágio para gerar uma imagem final otimizada, menor e mais segura.
-   **Segurança:** Implementar um sistema de autenticação e autorização completo (ex: com JWT) para proteger os dados dos usuários.