# Module 13: JWT Authentication & Frontend E2E

This module implements secure JWT-based user authentication and integrates a simple frontend (Login/Register pages) to complete the full-stack core.

## Project Features
* **JWT Authentication**: Secure endpoints for `/users/register` and `/users/login` return a valid access token.
* **Front-End Forms**: Functional `register.html` and `login.html` pages using vanilla JavaScript for client-side API interaction.
* **Playwright E2E Tests**: Automated browser tests to validate registration, login, and error handling.
* **Database Integration**: Uses SQLAlchemy with User and Calculation models.
* **CI/CD**: GitHub Actions pipeline automates E2E testing and Docker Hub deployment.

---

## 🐳 How to Run with Docker
The following steps start all necessary services (PostgreSQL, FastAPI, pgAdmin).

1.  Make sure you have Docker Desktop running.
2.  Clone this repository.
3.  From the project's root directory, run:
    ```bash
    docker compose up --build -d
    ```

4.  **Manual Check (OpenAPI):**
    Verify the endpoints exist by opening your browser to **[http://localhost:8000/docs](http://localhost:8000/docs)**.

---

## 🧪 How to Run E2E Tests Locally
Integration tests require a running database (started in Step 1).

1.  **Activate your environment:** `source venv/bin/activate`
2.  **Run the tests:**
    ```bash
    POSTGRES_HOST=localhost pytest --base-url http://localhost:8000
    ```

## 🚢 Docker Hub Repository

The CI/CD pipeline automatically builds and pushes the image upon test success.

**Repository Link:** [https://hub.docker.com/r/sm3777/module13-fastapi-frontend](https://hub.docker.com/r/sm3777/module13-fastapi-frontend)

---

### Final Submission Action

1.  **Save** both of these files.
2.  **Commit and push** the changes to your GitHub repository.
3.  Wait for the final green checkmark in GitHub Actions (which should happen now!).