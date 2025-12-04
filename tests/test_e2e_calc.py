import pytest
from playwright.sync_api import Page, expect
import random
import time
import requests
# --- NEW IMPORTS ---
from app.database import engine, Base
# -------------------

def get_random_user():
    rand = random.randint(1000,9999)
    return {"email": f"bread_{rand}@test.com", "pass": "secure"}

def wait_for_app_startup(url, timeout=20):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            if requests.get(url).status_code == 200:
                return
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(1)
    raise TimeoutError(f"Server did not start at {url}")

@pytest.fixture(scope="module", autouse=True)
def wait_for_server(base_url):
    wait_for_app_startup(f"{base_url}/")

# --- NEW FIXTURE: Re-create tables ---
@pytest.fixture(scope="function", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
# -------------------------------------

def test_dashboard_flow(page: Page, base_url):
    # 1. Register & Login
    user = get_random_user()
    page.goto(f"{base_url}/static/register.html")
    page.fill("#email", user["email"])
    page.fill("#username", "user1")
    page.fill("#password", user["pass"])
    page.click("button[type=submit]")
    expect(page.locator("#message")).to_contain_text("Registration Successful", timeout=15000)

    page.goto(f"{base_url}/static/login.html")
    page.fill("#username", user["email"])
    page.fill("#password", user["pass"])
    page.click("button[type=submit]")
    expect(page.locator("#message")).to_contain_text("Login Successful", timeout=15000)

    # 2. Go to Dashboard
    page.goto(f"{base_url}/static/dashboard.html")
    
    # 3. Add Calculation
    page.fill("#a", "10")
    page.fill("#b", "5")
    page.select_option("#type", "add")
    page.click("text=Calculate")
    
    # 4. Verify in Table (Result 15)
    expect(page.locator("td", has_text="15")).to_be_visible(timeout=10000)

    # 5. Delete Calculation
    page.on("dialog", lambda dialog: dialog.accept()) 
    page.locator("tr", has_text="15").locator(".delete-btn").click()
    
    # 6. Verify Removal
    expect(page.locator("td", has_text="15")).not_to_be_visible(timeout=10000)