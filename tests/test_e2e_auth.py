import pytest
from playwright.sync_api import Page, expect
import random
import time
import requests 
from app.database import engine, Base

# Helper to generate unique user data
def get_random_user():
    rand_id = random.randint(100000, 999999) 
    return {
        "email": f"e2e_{rand_id}@test.com",
        "username": f"e2e_user_{rand_id}",
        "password": "securepass"
    }

# --- SERVER WAIT LOGIC ---
def wait_for_app_startup(url, timeout=25):
    """Polls the given URL until it returns a 200 status."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(1)
    raise TimeoutError(f"Server did not start up at {url} within {timeout} seconds.")

@pytest.fixture(scope="session", autouse=True)
def wait_for_server_start(base_url):
    """Fixture that runs once per session to wait for the app service."""
    wait_for_app_startup("http://localhost:8000/") 

# --- DATABASE SETUP FIXTURE (CRITICAL FIX) ---
@pytest.fixture(scope="function", autouse=True)
def setup_database():
    """
    Forces table creation before every test function.
    This fixes the issue where previous integration tests dropped the tables.
    """
    Base.metadata.create_all(bind=engine)
    yield
    # We don't drop here to ensure state persists for manual inspection if needed
# ---------------------------------------------

# --- TEST 1: REGISTRATION ---
def test_frontend_register(page: Page, base_url):
    user = get_random_user()
    
    page.goto(f"{base_url}/static/register.html")
    
    page.fill("#email", user["email"])
    page.fill("#username", user["username"])
    page.fill("#password", user["password"])
    
    page.click("button[type=submit]")
    
    message = page.locator("#message")
    expect(message).to_contain_text("Registration Successful", timeout=15000)

# --- TEST 2: LOGIN ---
def test_frontend_login(page: Page, base_url):
    user = get_random_user()
    
    # Register first via UI
    page.goto(f"{base_url}/static/register.html")
    page.fill("#email", user["email"])
    page.fill("#username", user["username"])
    page.fill("#password", user["password"])
    page.click("button[type=submit]")
    expect(page.locator("#message")).to_contain_text("Registration Successful", timeout=15000)
    
    # Then Login
    page.goto(f"{base_url}/static/login.html")
    page.fill("#username", user["email"]) 
    page.fill("#password", user["password"])
    page.click("button[type=submit]")
    
    message = page.locator("#message")
    expect(message).to_contain_text("Login Successful", timeout=15000)

# --- TEST 3: LOGIN FAIL ---
def test_frontend_login_fail(page: Page, base_url):
    page.goto(f"{base_url}/static/login.html")
    
    page.fill("#username", "nonexistent@user.com")
    page.fill("#password", "wrongpass")
    page.click("button[type=submit]")
    
    message = page.locator("#message")
    expect(message).to_contain_text("Invalid credentials", timeout=15000)