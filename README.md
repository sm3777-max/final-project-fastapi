Module 14: Full-Stack FastAPI Calculator

This project is the culmination of the FastAPI Calculator series. It transforms the backend API into a full-stack web application with secure user authentication, a persistent PostgreSQL database, and a frontend dashboard for managing calculations.

🚀 Project Features

Backend (FastAPI)

User Authentication: Secure registration and login using JWT (JSON Web Tokens).

BREAD Operations: Full Browse, Read, Edit, Add, and Delete endpoints for calculation data.

Database: PostgreSQL integration using SQLAlchemy with a One-to-Many relationship (Users -> Calculations).

Security: Password hashing using bcrypt (via passlib wrapper).

Frontend (HTML/JS)

Login & Register Pages: Client-side forms that consume the API and store JWTs.

Dashboard: A protected interface that lists user-specific calculations and allows adding/deleting records.

Validation: Client-side checks for input formats and error handling for API failures.

CI/CD & Testing

Automated Testing: Comprehensive suite including:

Unit Tests: Logic and schema validation.

API Integration Tests: Verifying backend endpoints using TestClient.

E2E Tests: Browser automation using Playwright.

GitHub Actions: Automates testing and deployment to Docker Hub on every push.

🐳 How to Run with Docker

The application is fully containerized. To run it:

Clone the repository:

git clone [https://github.com/sm3777-max/module14-fastapi-bread.git](https://github.com/sm3777-max/module14-fastapi-bread.git)
cd module14-fastapi-bread


Start the containers:

docker compose up --build -d


Access the Application:

Frontend Dashboard: http://localhost:8000/static/login.html

API Documentation: http://localhost:8000/docs

pgAdmin (Database UI): http://localhost:5050

🧪 How to Run Tests Locally

Because this project uses complex dependencies like passlib and bcrypt, we use a special TEST_MODE flag to ensure tests run smoothly across different environments (local vs. CI runner).

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
export TEST_MODE=true
uvicorn main:app --host 0.0.0.0 --port 8000 --reload


3. Run the Tests (Terminal 2)

In a second terminal, run the test suite.

POSTGRES_HOST=localhost pytest --base-url http://localhost:8000


🚢 Docker Hub Repository

The CI/CD pipeline automatically builds and pushes the Docker image to Docker Hub upon successful testing.

Repository Link: https://hub.docker.com/r/sm3777/module14-fastapi-bread