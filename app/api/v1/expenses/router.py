from fastapi import APIRouter, Depends, Query, status

from app.core.security import get_current_user
from app.models.schemas import ExpenseCreate, ExpenseRead, ExpenseUpdate, MonthlySummary
from app.models.user_model import User
from app.services.expense_service import ExpenseService

router = APIRouter()


@router.get("/", response_model=list[ExpenseRead])
async def list_expenses(
    service: ExpenseService = Depends(ExpenseService), current_user: User = Depends(get_current_user)
):
    return await service.list(current_user.id)


@router.post("/", response_model=ExpenseRead, status_code=status.HTTP_201_CREATED)
async def create_expense(
    payload: ExpenseCreate,
    service: ExpenseService = Depends(ExpenseService),
    current_user: User = Depends(get_current_user),
):
    return await service.create(current_user.id, payload)


@router.get("/summary/monthly", response_model=MonthlySummary)
async def monthly_summary(
    month: int = Query(..., ge=1, le=12),
    year: int = Query(..., ge=1970),
    service: ExpenseService = Depends(ExpenseService),
    current_user: User = Depends(get_current_user),
):
    return await service.monthly_summary(current_user.id, month, year)


@router.get("/{expense_id}", response_model=ExpenseRead)
async def get_expense(
    expense_id: int,
    service: ExpenseService = Depends(ExpenseService),
    current_user: User = Depends(get_current_user),
):
    return await service.get(current_user.id, expense_id)


@router.put("/{expense_id}", response_model=ExpenseRead)
async def update_expense(
    expense_id: int,
    payload: ExpenseUpdate,
    service: ExpenseService = Depends(ExpenseService),
    current_user: User = Depends(get_current_user),
):
    return await service.update(current_user.id, expense_id, payload)


@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_expense(
    expense_id: int,
    service: ExpenseService = Depends(ExpenseService),
    current_user: User = Depends(get_current_user),
):
    await service.delete(current_user.id, expense_id)
