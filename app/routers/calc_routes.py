from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import schemas, models, database, crud, security # <-- Import security

router = APIRouter(prefix="/calculations", tags=["Calculations"])

# Helper to get the actual User object from the email
def get_current_user(db: Session = Depends(database.get_db), email: str = Depends(security.get_current_user_email)):
    user = crud.get_user_by_email(db, email=email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# 1. BROWSE (List User's Calculations)
@router.get("/", response_model=List[schemas.CalculationRead])
def read_calculations(skip: int = 0, limit: int = 100, 
                      db: Session = Depends(database.get_db),
                      current_user: models.User = Depends(get_current_user)): # <-- dependency
    # Filter by current_user.id
    return db.query(models.Calculation).filter(models.Calculation.user_id == current_user.id).offset(skip).limit(limit).all()

# 2. READ (One)
@router.get("/{calc_id}", response_model=schemas.CalculationRead)
def read_calculation(calc_id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    # Ensure it belongs to the user
    calc = db.query(models.Calculation).filter(models.Calculation.id == calc_id, models.Calculation.user_id == current_user.id).first()
    if calc is None:
        raise HTTPException(status_code=404, detail="Calculation not found")
    return calc

# 3. ADD
@router.post("/", response_model=schemas.CalculationRead)
def create_calculation(calc: schemas.CalculationCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    # Use current_user.id instead of hardcoded 1
    return crud.create_calculation(db=db, calc=calc, user_id=current_user.id)

# 4. EDIT
@router.put("/{calc_id}", response_model=schemas.CalculationRead)
def update_calculation(calc_id: int, calc_update: schemas.CalculationCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    # Find user's calculation
    db_calc = db.query(models.Calculation).filter(models.Calculation.id == calc_id, models.Calculation.user_id == current_user.id).first()
    if db_calc is None:
        raise HTTPException(status_code=404, detail="Calculation not found")
    
    # Recalculate
    from app.logic import get_operation_func
    op_func = get_operation_func(calc_update.type)
    
    db_calc.a = calc_update.a
    db_calc.b = calc_update.b
    db_calc.type = calc_update.type
    db_calc.result = op_func(calc_update.a, calc_update.b)
    
    db.commit()
    db.refresh(db_calc)
    return db_calc

# 5. DELETE
@router.delete("/{calc_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_calculation(calc_id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    db_calc = db.query(models.Calculation).filter(models.Calculation.id == calc_id, models.Calculation.user_id == current_user.id).first()
    if db_calc is None:
        raise HTTPException(status_code=404, detail="Calculation not found")
    
    db.delete(db_calc)
    db.commit()
    return None