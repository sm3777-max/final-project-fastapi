import pytest
from pydantic import ValidationError

# Import all the things we need to test
from app.security import get_password_hash, verify_password
from app.logic import OperationType, get_operation_func
from app.schemas import CalculationCreate

# --- Security Unit Tests (from Module 10) ---

def test_password_hashing():
    """
    Tests the password hashing and verification functions.
    """
    password = "mysecretpassword123"
    
    # Test that a hash is created
    hashed_password = get_password_hash(password)
    assert hashed_password is not None
    
    # Test that the hash is not the same as the original password
    assert hashed_password != password
    
    # Test that verification works for the correct password
    assert verify_password(password, hashed_password) == True
    
    # Test that verification fails for an incorrect password
    assert verify_password("wrongpassword", hashed_password) == False

# --- Calculation Unit Tests (NEW for Module 11) ---

def test_logic_factory():
    """Test that the factory returns the correct functions."""
    add_func = get_operation_func(OperationType.ADD)
    assert add_func(2, 3) == 5
    
    sub_func = get_operation_func(OperationType.SUBTRACT)
    assert sub_func(10, 5) == 5
    
    mul_func = get_operation_func(OperationType.MULTIPLY)
    assert mul_func(5, 5) == 25
    
    div_func = get_operation_func(OperationType.DIVIDE)
    assert div_func(10, 2) == 5

def test_logic_divide_by_zero_exception():
    """Test that the core logic function raises a ValueError."""
    div_func = get_operation_func(OperationType.DIVIDE)
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        div_func(10, 0)

def test_schema_validation_divide_by_zero():
    """Test that the Pydantic schema validation catches division by zero."""
    with pytest.raises(ValidationError) as e:
        # Pydantic will raise a ValidationError
        CalculationCreate(a=10, b=0, type=OperationType.DIVIDE)
    
    # Check that our custom error message is in the validation error
    assert "Cannot divide by zero" in str(e.value)

def test_schema_validation_good_data():
    """Test that good data passes schema validation."""
    # Test a valid division
    calc = CalculationCreate(a=10, b=5, type=OperationType.DIVIDE)
    assert calc.a == 10
    assert calc.b == 5
    
    # Test that adding zero is still allowed
    calc_add = CalculationCreate(a=10, b=0, type=OperationType.ADD)
    assert calc_add.b == 0

def test_schema_validation_invalid_type():
    """Test that an invalid operation string fails validation."""
    with pytest.raises(ValidationError):
        CalculationCreate(a=10, b=5, type="power") # "power" is not a valid OperationType