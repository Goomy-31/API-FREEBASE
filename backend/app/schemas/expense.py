from pydantic import BaseModel
from datetime import datetime

class ExpenseCreate(BaseModel):
    amount: float
    category: str
    note: str | None = None

class ExpenseResponse(BaseModel):
    id: str
    amount: float
    category: str
    note: str | None
    created_at: datetime