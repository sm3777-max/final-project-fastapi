from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
import pytest

from main import app
from app.database import SessionLocal, engine, Base
from app import crud, models

client = TestClient(app)

@pytest.fixture(scope="function", autouse=True)
def setup_database_state():
    """Fixture to create and drop database tables for every test function."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_user_flow(setup_database_state):
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
    assert "access_token" in login_response.json()

def test_calculation_crud_flow(setup_database_state):
    # 1. Register User
    client.post("/users/register", json={
        "username": "calc_user",
        "email": "calc@test.com",
        "password": "password123"
    })

    # 2. Login to get Token
    login_res = client.post("/users/login", data={
        "username": "calc@test.com",
        "password": "password123"
    })
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"} # <--- KEY FIX: Headers

    # 3. ADD (Create) - WITH HEADERS
    create_res = client.post("/calculations/", json={
        "a": 10, 
        "b": 5, 
        "type": "add"
    }, headers=headers)
    assert create_res.status_code == 200
    data = create_res.json()
    calc_id = data["id"]
    assert data["result"] == 15.0

    # 4. READ (Get One)
    read_res = client.get(f"/calculations/{calc_id}", headers=headers)
    assert read_res.status_code == 200

    # 5. EDIT (Update)
    update_res = client.put(f"/calculations/{calc_id}", json={
        "a": 10, 
        "b": 2, 
        "type": "divide"
    }, headers=headers)
    assert update_res.status_code == 200
    assert update_res.json()["result"] == 5.0

    # 6. DELETE
    del_res = client.delete(f"/calculations/{calc_id}", headers=headers)
    assert del_res.status_code == 204