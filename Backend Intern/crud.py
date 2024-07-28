from sqlalchemy.orm import Session
from models import Expense, ExpenseSplit, User
from models import Expense as DBExpense, ExpenseSplit as DBExpenseSplit, User


def create_expense(db: Session, expense_data: dict):
    expense = Expense(
        description=expense_data["description"],
        amount=expense_data["amount"],
        split_type=expense_data["split_type"],
        creator_id=expense_data["user_id"]
    )
    db.add(expense)
    db.commit()
    db.refresh(expense)

    for split in expense_data["splits"]:
        expense_split = ExpenseSplit(
            expense_id=expense.id,
            user_id=split["user_id"],
            type=split["type"],
            amount=split.get("amount"),
            percentage=split.get("percentage")
        )
        db.add(expense_split)

    db.commit()

def get_balance_sheet(db: Session):
    users = db.query(User).all()
    expenses = db.query(Expense).all()
    expense_splits = db.query(ExpenseSplit).all()

    balances = {user.id: 0 for user in users}

    for expense in expenses:
        total_amount = expense.amount
        splits = [s for s in expense_splits if s.expense_id == expense.id]

        if expense.split_type == "equal":
            split_amount = total_amount / len(splits)
            for split in splits:
                balances[split.user_id] -= split_amount

        elif expense.split_type == "exact":
            for split in splits:
                if split.amount is not None:
                    balances[split.user_id] -= split.amount

        elif expense.split_type == "percentage":
            for split in splits:
                if split.percentage is not None:
                    balances[split.user_id] -= (total_amount * split.percentage / 100)

    balance_sheet = {user.id: {"name": user.name, "balance": balances[user.id]} for user in users}
    return balance_sheet

def save_amount(db: Session, user_id: int, expense_id: int, amount: float, split_type: str):
    db_split = ExpenseSplit(user_id=user_id, expense_id=expense_id, amount=amount, split_type=split_type)
    db.add(db_split)
    db.commit()