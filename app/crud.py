# in app/crud.py

from sqlalchemy.orm import Session
from . import models, schemas, security
from .logic import get_operation_func # Import our factory

# --- User CRUD (from Module 10) ---

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = security.get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        password_hash=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- Calculation CRUD (NEW for Module 11) ---

def create_calculation(db: Session, calc: schemas.CalculationCreate, user_id: int):
    """
    Create a new calculation record for a user.
    """
    # 1. Get the correct math function from our factory
    operation_func = get_operation_func(calc.type)
    
    # 2. Calculate the result
    result = operation_func(calc.a, calc.b)
    
    # 3. Create the SQLAlchemy model instance
    db_calculation = models.Calculation(
        a=calc.a,
        b=calc.b,
        type=calc.type,
        result=result,
        user_id=user_id
    )
    
    db.add(db_calculation)
    db.commit()
    db.refresh(db_calculation)
    return db_calculation