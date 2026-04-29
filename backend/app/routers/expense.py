from fastapi import APIRouter, Depends

from backend.app.schemas.expense import ExpenseCreate
from backend.app.services import expense_service
from backend.app.dependencies.auth import get_current_user

router = APIRouter(prefix="/expenses", tags=["expenses"])


@router.post("/")
def create_expense(data: ExpenseCreate, user=Depends(get_current_user)):
    return expense_service.create_expense(user["uid"], data)


@router.get("/")
def get_expenses(user=Depends(get_current_user)):
    return expense_service.get_expenses(user["uid"])