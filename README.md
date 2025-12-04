Module 14: Full-Stack FastAPI Calculator

This project transforms the FastAPI Calculator into a complete full-stack application. It integrates secure user authentication, a persistent PostgreSQL database, and a frontend dashboard for managing calculations via BREAD (Browse, Read, Edit, Add, Delete) operations.

🚀 Project Features

Backend (FastAPI)

User Authentication: Secure POST /users/register and /users/login endpoints using JWT (JSON Web Tokens).

BREAD Operations: Full REST API to manage user-specific calculations.

Database: PostgreSQL integration using SQLAlchemy with relational models (Users -> Calculations).

Security: Password hashing using bcrypt (via passlib).

Frontend (HTML/JS)

Auth Pages: Functional Registration and Login forms.

Dashboard: A protected interface that lists calculations, allows adding new ones, and deleting history.

Dynamic UI: Uses Vanilla JavaScript fetch API to interact with the backend securely using Bearer tokens.

CI/CD & Testing

Automated Testing: 15+ tests covering Unit logic, API integration, and E2E browser flows using Playwright.

GitHub Actions: Automates testing and Docker Hub deployment on every push.

🐳 How to Run with Docker

The application is containerized for easy deployment.

Clone the repository:

git clone [https://github.com/sm3777-max/module14-fastapi-bread.git](https://github.com/sm3777-max/module14-fastapi-bread.git)
cd module14-fastapi-bread


Start the containers:

docker compose up --build -d


Access the Application:

Frontend Dashboard: http://localhost:8000/static/login.html

API Documentation: http://localhost:8000/docs

pgAdmin: http://localhost:5050

🧪 How to Run Tests Locally

Due to environmental differences in password hashing libraries across platforms, this project uses a TEST_MODE flag. This ensures tests run reliably by bypassing complex hashing during validation steps.

1. Setup Environment

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt


2. Start the Server (Terminal 1)

You must run the server manually for the E2E tests to connect.

export POSTGRES_HOST=localhost
export POSTGRES_USER=postgres
export POSTGRES_PASSWORD=password
export POSTGRES_DB=fastapi_db
# Enables stable testing environment
export TEST_MODE=true
uvicorn main:app --host 0.0.0.0 --port 8000 --reload


3. Run the Tests (Terminal 2)

In a second terminal, run the full test suite.

POSTGRES_HOST=localhost pytest --base-url http://localhost:8000


🚢 Docker Hub Repository

The CI/CD pipeline automatically builds and pushes the Docker image to Docker Hub upon successful testing.

Repository Link: https://hub.docker.com/r/sm3777/module14-fastapi-bread