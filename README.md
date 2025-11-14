# Module 11: FastAPI Calculator Model & Validation

This project defines the database models and business logic for a FastAPI calculator. It builds on Module 10 by adding a SQLAlchemy `Calculation` model, Pydantic validation (including for division by zero), and a factory pattern for the core logic.

## Project Features
* **Secure User Model**: SQLAlchemy `User` model with `username`, `email`, and `password_hash`.
* **Calculation Model**: SQLAlchemy `Calculation` model linked to users via a foreign key.
* **Pydantic Schemas**: Validates all incoming data, including a custom check to prevent division by zero.
* **Factory Pattern**: Uses a factory to easily select the correct mathematical operation (add, subtract, etc.).
* **CI/CD Pipeline**: Automates testing and deployment to Docker Hub.
* **Docker Compose**: Runs the full stack (FastAPI, PostgreSQL, pgAdmin).

---

## 🐳 How to Run with Docker
This is the easiest way to run the full application stack, including the database.

1.  Make sure you have Docker Desktop running.
2.  Clone this repository.
3.  From the project's root directory, run:
    ```bash
    docker-compose up --build
    ```
4.  The application will be running at **`http://127.0.0.1:8000`**.
5.  pgAdmin (database manager) will be available at **`http://127.0.0.1:5050`**.

---

## 🧪 How to Run Tests Locally
You can run the unit and integration tests on your local machine.

1.  Create and activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
2.  Install all dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Run `pytest`:
    ```bash
    pytest
    ```
    *(Note: Integration tests require a running PostgreSQL database. The CI pipeline handles this automatically.)*

---

## 🚢 Docker Hub Repository

The CI/CD pipeline automatically builds and pushes the Docker image for this project to Docker Hub.

You can find the repository here:
**[https://hub.docker.com/r/sm3777/module11-fastapi-calculator](https://hub.docker.com/r/sm3777/module11-fastapi-calculator)**

---

## 🐍 How to Run Locally (Original Setup)
This method runs the app directly on your machine using a Python virtual environment.

1.  Clone the repository.
2.  Create and activate a virtual environment.
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  Run the application:
    ```bash
    uvicorn app.main:app --reload
    ```