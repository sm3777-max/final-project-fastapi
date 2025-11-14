import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.database import SessionLocal, engine, Base
from app.models import User, Calculation
from app.schemas import CalculationCreate
from app.logic import OperationType
from app import crud

# Create a test client that talks to our app
client = TestClient(app)

@pytest.fixture(scope="module")
def db():
    """
    Fixture to set up a clean database for this test module.
    It creates all tables before tests run and drops them after.
    """
    # Create all tables (User, Calculation)
    Base.metadata.create_all(bind=engine)
    
    # Yield a new session for the tests to use
    db_session = SessionLocal()
    yield db_session
    
    # Clean up: close session and drop all tables
    db_session.close()
    Base.metadata.drop_all(bind=engine)

# --- User Integration Tests (from Module 10) ---

def test_create_user_success(db: Session):
    """Test creating a new user successfully via the /users/ endpoint."""
    response = client.post("/users/", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["username"] == "testuser"
    assert "id" in data
    assert "password_hash" not in data # Check that hash isn't returned

def test_create_user_duplicate_email(db: Session):
    """Test creating a user with a duplicate email."""
    # This user was created in the previous test
    response = client.post("/users/", json={
        "username": "newuser",
        "email": "test@example.com", # Duplicate email
        "password": "password123"
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered."

def test_create_user_duplicate_username(db: Session):
    """Test creating a user with a duplicate username."""
    response = client.post("/users/", json={
        "username": "testuser", # Duplicate username
        "email": "new@example.com",
        "password": "password123"
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Username already taken."

# --- Calculation Integration Test (NEW for Module 11) ---

def test_crud_create_calculation_for_user(db: Session):
    """
    Test creating a calculation record linked to a user.
    This test calls the CRUD function directly, as per assignment instructions.
    """
    # 1. Get the user we created in the first test
    user = crud.get_user_by_username(db, username="testuser")
    assert user is not None, "User 'testuser' not found in database"
    
    # 2. Define the calculation data
    calc_data = CalculationCreate(
        a=20,
        b=5,
        type=OperationType.DIVIDE
    )
    
    # 3. Use the CRUD function to create the calculation
    db_calc = crud.create_calculation(db=db, calc=calc_data, user_id=user.id)
    
    # 4. Verify the result is stored correctly in the database
    assert db_calc.id is not None
    assert db_calc.a == 20
    assert db_calc.b == 5
    assert db_calc.type == "divide"
    assert db_calc.result == 4.0
    assert db_calc.user_id == user.id
    
    # 5. Verify the relationship from the user side is working
    db.refresh(user)
    assert len(user.calculations) == 1
    assert user.calculations[0].result == 4.0