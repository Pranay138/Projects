# balance_sheet.py
import pandas as pd
from sqlalchemy.orm import Session
from models import User, Expense
from database import SessionLocal

def generate_balance_sheet(db: Session):
    users = db.query(User).all()
    expenses = db.query(Expense).all()
    
    data = []
    for user in users:
        user_expenses = [expense for expense in expenses if expense.user_id == user.id]
        for expense in user_expenses:
            data.append({
                "User": user.name,
                "Expense Description": expense.description,
                "Amount": expense.amount,
                "Split Type": expense.split_type,
                "Split Details": expense.split_details
            })

    df = pd.DataFrame(data)
    df.to_csv("balance_sheet.csv", index=False)

if __name__ == "__main__":
    db = SessionLocal()
    generate_balance_sheet(db)
