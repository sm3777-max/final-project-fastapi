# in app/schemas.py

from pydantic import BaseModel, EmailStr, field_validator, ConfigDict
from datetime import datetime
from .logic import OperationType # Import our new Enum

# --- User Schemas (from Module 10) ---

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int
    created_at: datetime
    
    # Use ConfigDict for modern Pydantic
    model_config = ConfigDict(from_attributes=True)


# --- Calculation Schemas (NEW for Module 11) ---

class CalculationBase(BaseModel):
    a: float
    b: float
    type: OperationType # Use the Enum for validation

class CalculationCreate(CalculationBase):
    
    # This is the Pydantic validator
    @field_validator('b')
    def check_division_by_zero(cls, b, values):
        """
        Check if the operation is 'divide' and if 'b' is zero.
        """
        # 'values.data' holds the values already validated
        if 'type' in values.data and values.data['type'] == OperationType.DIVIDE and b == 0:
            raise ValueError("Cannot divide by zero")
        return b

class CalculationRead(CalculationBase):
    id: int
    result: float
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)