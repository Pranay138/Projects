from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, conlist
from typing import List, Union
from database import SessionLocal, engine
from models import Expense
from models import Expense as DBExpense, ExpenseSplit as DBExpenseSplit, User
from pydantic import BaseModel, ValidationError, validator
from typing import List
import models 
import logging
import pdb; pdb.set_trace()
import crud 

app = FastAPI()

logging.basicConfig(level=logging.DEBUG)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class SplitDetail(BaseModel):
    user_id: int
    amount: float

class Expense(BaseModel):
    description: str
    amount: float
    split_type: str
    splits: List[SplitDetail]
    user_id: int

    @validator('splits')
    def check_min_items(cls, value):
        if len(value) < 1:
            raise ValueError('At least one split detail must be provided')
        return value

@app.post("/expenses/")
async def create_expense(expense: Expense, db: Session = Depends(get_db)):
    try:
        db_expense = DBExpense(
            description=expense.description,
            amount=expense.amount,
            user_id=expense.user_id,
            split_type=expense.split_type
        )
        db.add(db_expense)
        db.commit()
        db.refresh(db_expense)

        if expense.split_type == "equal":
            if len(expense.splits) == 0:
                raise HTTPException(status_code=400, detail="No users provided for splitting")
            amount_per_user = expense.amount / len(expense.splits)
            for split in expense.splits:
                crud.save_amount(db, split.user_id, db_expense.id, amount_per_user, "equal")

        elif expense.split_type == "exact":
            total_amount = sum(split.amount for split in expense.splits)
            if total_amount != expense.amount:
                raise HTTPException(status_code=400, detail="Exact amounts do not sum up to total expense amount")
            for split in expense.splits:
                crud.save_amount(db, split.user_id, db_expense.id, split.amount, "exact")

        elif expense.split_type == "percentage":
            total_percentage = sum(split.amount for split in expense.splits)
            if total_percentage != 100:
                raise HTTPException(status_code=400, detail="Percentages do not sum up to 100%")
            for split in expense.splits:
                amount_due = expense.amount * (split.amount / 100)
                crud.save_amount(db, split.user_id, db_expense.id, amount_due, "percentage")

        else:
            raise HTTPException(status_code=400, detail="Invalid split type")

        return {"message": "Expense created", "data": expense}

    except HTTPException as e:
        raise e
    except Exception as e:
        # Print the error for debugging purposes
        print(f"An error occurred: {str(e)}")
        # Return a 500 error with a generic message
        raise HTTPException(status_code=500, detail="An internal error occurred")
@app.get("/balance-sheet/")
def get_balance_sheet(db: Session = Depends(get_db)):
    return crud.get_balance_sheet(db)



