from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.models.schemas import (
    CategorySummary,
    ExpenseCreate,
    ExpenseRead,
    ExpenseUpdate,
    MonthlySummary,
)
from app.repositories.category_repository import CategoryRepository
from app.repositories.expense_repository import ExpenseRepository


class ExpenseService:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session
        self.repo = ExpenseRepository(session)
        self.category_repo = CategoryRepository(session)

    async def _validate_category(self, user_id: int, category_id: int) -> None:
        category = await self.category_repo.get_owned(category_id, user_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Categoria não encontrada ou não pertence ao usuário",
            )

    async def create(self, user_id: int, payload: ExpenseCreate) -> ExpenseRead:
        await self._validate_category(user_id, payload.category_id)
        expense = await self.repo.create(owner_id=user_id, data=payload)
        return ExpenseRead.from_orm(expense)

    async def list(self, user_id: int):
        expenses = await self.repo.list_by_owner(user_id)
        return [ExpenseRead.from_orm(exp) for exp in expenses]

    async def get(self, user_id: int, expense_id: int) -> ExpenseRead:
        expense = await self.repo.get_owned(expense_id, user_id)
        if not expense:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Despesa não encontrada")
        return ExpenseRead.from_orm(expense)

    async def update(self, user_id: int, expense_id: int, payload: ExpenseUpdate) -> ExpenseRead:
        expense = await self.repo.get_owned(expense_id, user_id)
        if not expense:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Despesa não encontrada")
        if payload.category_id is not None:
            await self._validate_category(user_id, payload.category_id)
        updated = await self.repo.update(expense, payload)
        return ExpenseRead.from_orm(updated)

    async def delete(self, user_id: int, expense_id: int) -> None:
        expense = await self.repo.get_owned(expense_id, user_id)
        if not expense:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Despesa não encontrada")
        await self.repo.delete(expense)

    async def monthly_summary(self, user_id: int, month: int, year: int) -> MonthlySummary:
        summary = await self.repo.monthly_summary(user_id, month, year)
        breakdown = [
            CategorySummary(category=item["category"], total=item["total"]) for item in summary["breakdown"]
        ]

        return MonthlySummary(month=month, year=year, total=summary["total"], by_category=breakdown)
