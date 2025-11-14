# in app/logic.py

import enum

# 1. Use an Enum for strong typing of operation types
class OperationType(str, enum.Enum):
    ADD = "add"
    SUBTRACT = "subtract"
    MULTIPLY = "multiply"
    DIVIDE = "divide"

# 2. Define the individual logic functions
def add(a: float, b: float) -> float:
    return a + b

def subtract(a: float, b: float) -> float:
    return a - b

def multiply(a: float, b: float) -> float:
    return a * b

def divide(a: float, b: float) -> float:
    if b == 0:
        # This check is good, but we'll also enforce it in schemas
        raise ValueError("Cannot divide by zero")
    return a / b

# 3. Create the "Factory" - a simple dictionary mapping
OPERATION_FACTORY = {
    OperationType.ADD: add,
    OperationType.SUBTRACT: subtract,
    OperationType.MULTIPLY: multiply,
    OperationType.DIVIDE: divide,
}

def get_operation_func(op_type: OperationType):
    """
    Factory function to get the correct calculation function
    based on the operation type.
    """
    func = OPERATION_FACTORY.get(op_type)
    if func is None:
        raise ValueError(f"Invalid operation type: {op_type}")
    return func