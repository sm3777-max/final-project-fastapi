from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
import pytest

from main import app
from app.database import SessionLocal, engine, Base
from app import crud, models

# Create a test client
client = TestClient(app)

@pytest.fixture(scope="function", autouse=True) # <-- FIX: Changed scope to 'function'
def setup_database_state():
    """
    Fixture to create and drop database tables for every test function.
    This ensures clean isolation and prevents foreign key errors.
    """
    # Create all tables before the test runs
    Base.metadata.create_all(bind=engine)
    yield
    # Drop all tables after the test finishes
    Base.metadata.drop_all(bind=engine)

def test_user_flow(setup_database_state): # Fixture runs automatically
    """
    Test 1: Register a User
    Test 2: Login to get a token
    """
    # 1. Register
    reg_response = client.post("/users/register", json={
        "username": "integration_user",
        "email": "integration@test.com",
        "password": "securepassword"
    })
    assert reg_response.status_code == 200
    
    # 2. Login
    login_response = client.post("/users/login", data={
        "username": "integration@test.com", 
        "password": "securepassword"
    })
    assert login_response.status_code == 200
    
def test_calculation_crud_flow(setup_database_state): # Fixture runs automatically
    """
    Test the full lifecycle of a calculation (BREAD).
    This test will fail if test_user_flow didn't leave User ID 1. 
    We will register a user inside this test to be safe.
    """
    
    # SETUP: Register a clean user with ID 1
    client.post("/users/register", json={
        "username": "calc_user",
        "email": "calc@test.com",
        "password": "password123"
    })
    
    # 1. ADD (Create) - Use ID 1 (which calc_user should be)
    create_res = client.post("/calculations/", json={
        "a": 10, 
        "b": 5, 
        "type": "add"
    })
    assert create_res.status_code == 200
    calc_id = create_res.json()["id"]
    assert create_res.json()["result"] == 15.0

    # 2. READ (Get One)
    read_res = client.get(f"/calculations/{calc_id}")
    assert read_res.status_code == 200

    # 3. EDIT (Update)
    update_res = client.put(f"/calculations/{calc_id}", json={
        "a": 10, 
        "b": 2, 
        "type": "divide"
    })
    assert update_res.status_code == 200
    assert update_res.json()["result"] == 5.0

    # 4. DELETE
    del_res = client.delete(f"/calculations/{calc_id}")
    assert del_res.status_code == 204