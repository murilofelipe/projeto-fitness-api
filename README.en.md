[Leia em Português](README.md)

# Data Engineering Platform for Performance Analysis and Retention in the Fitness Sector

This project, developed as an Applied Project for a Data Engineering post-graduate course, consists of creating a complete platform for monitoring gym workouts. The solution involves a backend API, an ETL data pipeline, a Data Warehouse for analysis, and an automated test suite, all orchestrated in a containerized environment with Docker.

## 🎯 Table of Contents
1.  [Technologies Used](#-technologies-used)
2.  [Project Structure](#-project-structure)
3.  [Local Environment Setup](#-local-environment-setup)
4.  [Main Commands (Makefile)](#️-main-commands-makefile)
5.  [Code Quality and Testing](#-code-quality-and-testing)
6.  [Accessing the Database](#-accessing-the-database)
7.  [Next Steps](#-next-steps)

## ✨ Technologies Used

- **Backend:** Python, FastAPI
- **Database:** PostgreSQL (for both OLTP and OLAP)
- **Data Pipeline:** Python with Pandas
- **Containerization:** Docker and Docker Compose
- **Testing:** Pytest, pytest-cov
- **Code Quality:** Black, isort, Flake8, Mypy
- **Frontend (Planned):** Vue.js

## 📂 Project Structure

The project is organized with the following directory structure in its root:

```
/project-fitness-api/
|
|-- /backend/
|   |-- /src/
|   |-- /scripts/
|   |-- /tests/
|   |-- .flake8
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

### API Documentation
With the environment running, the interactive API documentation (Swagger UI) is available at:
- **[http://localhost:8000/docs](http://localhost:8000/docs)**

## 🗄️ Accessing the Database

You can connect to the PostgreSQL database using your preferred client (DBeaver, DataGrip, etc.) with the following credentials:
-   **Host:** `localhost`
-   **Port:** `5432`
-   **Database:** `fitness_db`
-   **User:** `myuser`
-   **Password:** `mypassword`

## 🔮 Next Steps

-   **Sprint 1:** Completed ✅
-   **Sprint 2:** Completed ✅
-   **Sprint 3 (Current):** Develop the Vue.js dashboard for data visualization and prepare the final project presentation.