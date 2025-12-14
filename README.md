Final Project: Full-Stack FastAPI Calculator

This is the final project for the Python Web API Development course. It represents a complete full-stack web application built with FastAPI, PostgreSQL, and vanilla JavaScript, featuring advanced calculation capabilities and user statistics.

🚀 Project Features

Backend (FastAPI)

User Authentication: Secure registration and login using JWT (JSON Web Tokens).

BREAD Operations: Full REST API to Browse, Read, Edit, Add, and Delete calculations.

Advanced Calculation: Includes a new Power (^) operation (Feature A).

History/Reports: A /stats endpoint that returns the total count of calculations per user (Feature B).

Database: PostgreSQL integration using SQLAlchemy with relational models (Users -> Calculations).

Security: Password hashing using bcrypt (via passlib wrapper).

Frontend (HTML/JS)

Auth Pages: Functional Registration and Login forms.

Dashboard: A protected interface that lists calculations, allows adding new ones, and deleting history.

User Statistics: Displays the total number of calculations performed by the user in a dedicated stats box.

Dynamic UI: Uses Vanilla JavaScript fetch API to interact with the backend securely using Bearer tokens.

CI/CD & Testing

Automated Testing: Comprehensive suite including:

Unit Tests: Logic validation (including Power function) and schema validation.

API Integration Tests: Verifying backend endpoints (including /stats) using TestClient.

E2E Tests: Browser automation using Playwright to test the full user flow (Register -> Login -> Dashboard -> Add Calc -> Delete).

GitHub Actions: Automates testing and deployment to Docker Hub on every push.

🐳 How to Run with Docker

The application is fully containerized for easy deployment.

Clone the repository:

git clone [https://github.com/sm3777-max/final-project-fastapi.git](https://github.com/sm3777-max/final-project-fastapi.git)
cd final-project-fastapi


Start the containers:

docker compose up --build -d


Access the Application:

Frontend Dashboard: http://localhost:8000/static/login.html

API Documentation: http://localhost:8000/docs

pgAdmin (Database UI): http://localhost:5050

🧪 How to Run Tests Locally

Due to environmental differences in password hashing libraries across platforms, this project uses a special TEST_MODE flag. This ensures tests run reliably by bypassing complex hashing during validation steps.

1. Setup Environment

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt


2. Start the Server (Terminal 1)

You must run the server manually for the E2E tests to connect. Use the TEST_MODE flag to bypass hash complexity during testing.

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

Repository Link: https://hub.docker.com/r/sm3777/final-project-fastapi 