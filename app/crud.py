from sqlalchemy.orm import Session
from app import models, schemas, security 
from app.logic import get_operation_func # Imports the calculation factory
import os # Required for the CI_SKIP_HASH check in security.py

# --- User CRUD ---

def get_user_by_email(db: Session, email: str):
    """Fetches a user by their email (used for login/registration checks)."""
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_username(db: Session, username: str):
    """Fetches a user by their username."""
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    """Hashes the password and creates a new user record."""
    
    # Calls the hashing function which contains the CI bypass logic
    hashed_password = security.get_password_hash(user.password)
    
    db_user = models.User(
        username=user.username,
        email=user.email,
        password_hash=hashed_password # Store the hash (either real or bypass hash)
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- Calculation CRUD ---

def create_calculation(db: Session, calc: schemas.CalculationCreate, user_id: int):
    """
    Computes the result using the factory and saves the calculation record.
    """
    # 1. Get the correct math function from the logic factory
    operation_func = get_operation_func(calc.type)
    
    # 2. Calculate the result
    result = operation_func(calc.a, calc.b)
    
    # 3. Create the model instance
    db_calculation = models.Calculation(
        a=calc.a,
        b=calc.b,
        type=calc.type,
        result=result,
        user_id=user_id # Foreign key link
    )
    
    db.add(db_calculation)
    db.commit()
    db.refresh(db_calculation)
    return db_calculation