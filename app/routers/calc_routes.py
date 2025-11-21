from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import schemas, models, database, crud
from app.logic import get_operation_func # Import factory for updates

# Create the router
router = APIRouter(prefix="/calculations", tags=["Calculations"])

# 1. BROWSE (List all calculations)
@router.get("/", response_model=List[schemas.CalculationRead])
def read_calculations(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    return db.query(models.Calculation).offset(skip).limit(limit).all()

# 2. READ (Get one calculation by ID)
@router.get("/{calc_id}", response_model=schemas.CalculationRead)
def read_calculation(calc_id: int, db: Session = Depends(database.get_db)):
    # Search for the calculation
    calc = db.query(models.Calculation).filter(models.Calculation.id == calc_id).first()
    if calc is None:
        raise HTTPException(status_code=404, detail="Calculation not found")
    return calc

# 3. ADD (Create a new calculation)
@router.post("/", response_model=schemas.CalculationRead)
def create_calculation(calc: schemas.CalculationCreate, db: Session = Depends(database.get_db)):
    # For this assignment, we default to user_id=1 to keep it simple
    # (In a real app, you'd get this from the logged-in user)
    return crud.create_calculation(db=db, calc=calc, user_id=1)

# 4. EDIT (Update a calculation)
@router.put("/{calc_id}", response_model=schemas.CalculationRead)
def update_calculation(calc_id: int, calc_update: schemas.CalculationCreate, db: Session = Depends(database.get_db)):
    # Find the record
    db_calc = db.query(models.Calculation).filter(models.Calculation.id == calc_id).first()
    if db_calc is None:
        raise HTTPException(status_code=404, detail="Calculation not found")
    
    # Update the fields
    db_calc.a = calc_update.a
    db_calc.b = calc_update.b
    db_calc.type = calc_update.type
    
    # IMPORTANT: Recalculate the result using your Logic Factory
    op_func = get_operation_func(calc_update.type)
    db_calc.result = op_func(calc_update.a, calc_update.b)
    
    # Save changes
    db.commit()
    db.refresh(db_calc)
    return db_calc

# 5. DELETE (Remove a calculation)
@router.delete("/{calc_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_calculation(calc_id: int, db: Session = Depends(database.get_db)):
    # Find the record
    db_calc = db.query(models.Calculation).filter(models.Calculation.id == calc_id).first()
    if db_calc is None:
        raise HTTPException(status_code=404, detail="Calculation not found")
    
    # Delete it
    db.delete(db_calc)
    db.commit()
    return None