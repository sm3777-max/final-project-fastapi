import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from main import app
from app.database import SessionLocal, engine, Base
from app import crud
from app.schemas import CalculationCreate
from app.logic import OperationType

client = TestClient(app)

@pytest.fixture(scope="function") # <-- FIX: Changed scope to 'function'
def db():
    """Fixture to set up a clean session and database for each test function."""
    Base.metadata.create_all(bind=engine)
    db_session = SessionLocal()
    yield db_session
    db_session.close()
    Base.metadata.drop_all(bind=engine)

# --- USER TESTS ---

def test_create_user_success(db: Session):
    """Test creating a new user successfully via the /users/register endpoint."""
    response = client.post("/users/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"

def test_create_user_duplicate_email(db: Session):
    """Test creating a user with a duplicate email."""
    # Register the user first
    client.post("/users/register", json={
        "username": "original_user",
        "email": "duplicate@test.com",
        "password": "password123"
    })
    
    # Attempt to register the duplicate email
    response = client.post("/users/register", json={
        "username": "newuser",
        "email": "duplicate@test.com", # Duplicate email
        "password": "password123"
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

# --- CALCULATION TEST ---

def test_crud_create_calculation_for_user(db: Session):
    """
    Test creating a calculation record linked to a user.
    """
    # SETUP: Register a user for the foreign key
    user_data = client.post("/users/register", json={
        "username": "calc_user",
        "email": "calc@test.com",
        "password": "password123"
    }).json()
    
    user = crud.get_user_by_username(db, username="calc_user")
    assert user is not None
    
    # 2. Define the calculation data
    calc_data = CalculationCreate(
        a=20,
        b=5,
        type=OperationType.DIVIDE
    )
    
    # 3. Use the CRUD function
    db_calc = crud.create_calculation(db=db, calc=calc_data, user_id=user.id)
    
    # 4. Verify result
    assert db_calc.id is not None
    assert db_calc.result == 4.0
    assert db_calc.user_id == user.id