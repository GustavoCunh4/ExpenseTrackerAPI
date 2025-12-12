from datetime import datetime
from typing import List, Optional

from sqlalchemy import func
from sqlmodel import select

from app.models.expense_model import Category, Expense
from app.models.schemas import ExpenseCreate, ExpenseUpdate
from app.repositories.base_repository import BaseRepository


class ExpenseRepository(BaseRepository):
    async def create(self, owner_id: int, data: ExpenseCreate) -> Expense:
        expense = Expense(
            title=data.title,
            amount=data.amount,
            date=data.date,
            description=data.description,
            category_id=data.category_id,
            owner_id=owner_id,
        )
        return await self.save(expense)

    async def list_by_owner(self, owner_id: int) -> List[Expense]:
        result = await self.session.execute(
            select(Expense)
            .where(Expense.owner_id == owner_id)
            .order_by(Expense.date.desc(), Expense.created_at.desc())
        )
        return list(result.scalars().all())

    async def get_owned(self, expense_id: int, owner_id: int) -> Optional[Expense]:
        result = await self.session.execute(
            select(Expense).where(Expense.id == expense_id, Expense.owner_id == owner_id)
        )
        return result.scalars().first()

    async def update(self, expense: Expense, data: ExpenseUpdate) -> Expense:
        if data.title is not None:
            expense.title = data.title
        if data.amount is not None:
            expense.amount = data.amount
        if data.date is not None:
            expense.date = data.date
        if data.category_id is not None:
            expense.category_id = data.category_id
        if data.description is not None:
            expense.description = data.description
        return await self.save(expense)

    async def delete(self, expense: Expense) -> None:
        await self.session.delete(expense)
        await self.session.commit()

    async def monthly_summary(self, owner_id: int, month: int, year: int):
        start_date = datetime(year, month, 1)
        end_month = month + 1 if month < 12 else 1
        end_year = year if month < 12 else year + 1
        end_date = datetime(end_year, end_month, 1)

        total_stmt = select(func.coalesce(func.sum(Expense.amount), 0)).where(
            Expense.owner_id == owner_id,
            Expense.date >= start_date,
            Expense.date < end_date,
        )
        total_result = await self.session.execute(total_stmt)
        total = float(total_result.scalar() or 0)

        breakdown_stmt = (
            select(Category.name.label("category"), func.sum(Expense.amount).label("total"))
            .join(Category, Category.id == Expense.category_id)
            .where(Expense.owner_id == owner_id, Expense.date >= start_date, Expense.date < end_date)
            .group_by(Category.name)
        )
        breakdown_result = await self.session.execute(breakdown_stmt)
        breakdown = [{"category": row.category, "total": float(row.total or 0)} for row in breakdown_result.all()]

        return {"total": total, "breakdown": breakdown}
