[Leia em Português](README.md)

# Data Engineering Platform for Performance Analysis and Retention in the Fitness Sector

This project, developed as an Applied Project for a Data Engineering post-graduate course, consists of creating a complete platform for monitoring gym workouts. The solution involves a backend API, an ETL data pipeline, a Data Warehouse for analysis, an automated test suite, and an interactive dashboard, all orchestrated in a containerized environment with Docker.

## 🎯 Table of Contents
1.  [Key Features](#-key-features)
2.  [Technologies Used](#-technologies-used)
3.  [Project Structure](#-project-structure)
4.  [Local Environment Setup](#-local-environment-setup)
5.  [Main Commands (Makefile)](#️-main-commands-makefile)
6.  [Code Quality and Testing](#-code-quality-and-testing)
7.  [Accessing the Services](#-accessing-the-services)
8.  [Next Steps](#-next-steps)

## ✨ Key Features

* **Robust API:** Backend developed in Python with FastAPI, serving both operational (from OLTP) and analytical (from OLAP/DWH) data.
* **ETL Pipeline:** An Extract, Transform, Load process with Pandas that moves and models data from an OLTP database to a Star Schema Data Warehouse (DWH).
* **Containerized Environment:** Full-stack application (Backend, Frontend, Database) fully managed with Docker and Docker Compose for easy setup.
* **Guaranteed Code Quality:** Automated test suite with `pytest`, type checking with `mypy`, and code standardization with `flake8`, `black`, and `isort`.
* **Interactive Dashboard:** Frontend developed in Vue.js 3 with TypeScript, featuring dynamic data visualizations, such as:
    * Workout frequency (weekly, monthly, and yearly).
    * Performance evolution (total volume and max load).
    * Workout calendar with status (planned, executed, not executed).
    * Dynamic filtering by student and by exercise.

## 🛠️ Technologies Used

- **Backend:** Python, FastAPI
- **Database:** PostgreSQL (OLTP & OLAP)
- **ETL:** Pandas
- **Containerization:** Docker, Docker Compose
- **Frontend:** Vue.js 3, TypeScript, Vite, Pinia
- **Charts:** Chart.js
- **Testing:** Pytest, Vitest
- **Code Quality:** Black, isort, Flake8, Mypy

## 📂 Project Structure

The project is organized with the following directory structure in its root:

```
/project-fitness-api/
|
|-- /backend/
|-- /frontend/
|-- .gitignore
|-- docker-compose.yml
|-- Makefile
|-- README.md
|-- README.en.md
```

## 🚀 Local Environment Setup

Follow these steps to set up and run the project on a new machine.

### Prerequisites
-   Git
-   Docker & Docker Compose

### Installation

1.  **Clone the repository:**
    ```bash
    git clone git@github.com:murilofelipe/projeto-fitness-api.git
    cd projeto-fitness-api
    ```

2.  **Start the containers:**
    This command will build the Docker images and start the API and database services in the background.
    ```bash
    make up
    ```

3.  **Initialize the database schema:**
    This command runs the script that creates all tables (OLTP and OLAP) in the database.
    ```bash
    make db-init
    ```

4.  **Seed the database with test data:**
    This command runs the script that populates the OLTP database with users, exercises, and 500 test workouts.
    ```bash
    make db-seed
    ```
5.  **Run the ETL Pipeline to populate the Data Warehouse:**
    ```bash
    make etl-run
    ```

## 🛠️ Main Commands (Makefile)

The `Makefile` serves as the project's control panel. Use `make help` to see all available commands.

| Command | Description |
| :--- | :--- |
| `make up` | Starts all services in the background. |
| `make down` | Stops and removes all containers. |
| `make clean`| Stops everything and deletes the data volumes (resets the DB). |
| `make db-init` | Creates the tables in the database. |
| `make db-seed` | Populates the OLTP database with test data. |
| `make etl-run`| Runs the complete ETL pipeline to the DWH. |
| `make sh-backend` | Accesses the terminal of the API container. |
| `make sh-db`| Accesses the terminal of the database container. |

## 🧪 Code Quality and Testing

| Command | Description |
| :--- | :--- |
| `make format` | **(Corrective)** Automatically formats all code with `isort` and `black`. |
| `make lint` | **(Preventive)** Checks for errors and style issues with `flake8`. |
| `make typecheck` | **(Preventive)** Checks for type consistency with `mypy`. |
| `make test` | **(Validation)** Runs the automated test suite with `pytest`. |
| `make test:cov-html` | Runs tests and generates an HTML coverage report. |
| `make test:all` | **(Full Cycle)** Runs all quality checks in sequence. |

## 🖥️ Accessing the Services

* **Frontend (Dashboard):**
    * [http://localhost:5173](http://localhost:5173)

* **Backend (API Documentation):**
    * [http://localhost:8000/docs](http://localhost:8000/docs)

* **Database (via DB client):**
    * **Host:** `localhost`
    * **Port:** `5432`
    * **Database:** `fitness_db`
    * **User:** `myuser`
    * **Password:** `mypassword`

## 🔮 Next Steps

With the MVP completed, future evolutions for the project could include:
-   **Professional ETL Orchestration:** Replace the manual ETL script execution with an orchestrator like **Apache Airflow**.
-   **End-to-End (E2E) Testing:** Add a test suite with **Cypress** or **Playwright** to validate user flows in the frontend interface.
-   **Production Optimization:** Implement a multi-stage `Dockerfile` to create a smaller and more secure final production image.
-   **Security:** Implement a full authentication and authorization system (e.g., with JWT) to protect user data.