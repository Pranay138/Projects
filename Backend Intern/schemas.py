from pydantic import BaseModel
from typing import List, Optional

class ExpenseSplitBase(BaseModel):
    user_id: int
    type: str
    amount: Optional[float] = None
    percentage: Optional[float] = None

class ExpenseCreate(BaseModel):
    description: str
    amount: float
    split_type: str
    splits: List[ExpenseSplitBase]
    user_id: int
