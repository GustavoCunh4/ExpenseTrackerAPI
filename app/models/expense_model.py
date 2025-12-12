from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy.orm import relationship
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.user_model import User


class CategoryBase(SQLModel):
    name: str


class Category(CategoryBase, table=True):
    __tablename__ = "categories"

    id: Optional[int] = Field(default=None, primary_key=True)
    owner_id: int = Field(foreign_key="users.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    expenses: list["Expense"] = Relationship(
        back_populates="category", sa_relationship=relationship("Expense", back_populates="category")
    )
    owner: Optional["User"] = Relationship(
        back_populates="categories", sa_relationship=relationship("User", back_populates="categories")
    )


class ExpenseBase(SQLModel):
    title: str
    amount: float
    date: datetime
    description: Optional[str] = None


class Expense(ExpenseBase, table=True):
    __tablename__ = "expenses"

    id: Optional[int] = Field(default=None, primary_key=True)
    category_id: int = Field(foreign_key="categories.id")
    owner_id: int = Field(foreign_key="users.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    category: Optional[Category] = Relationship(
        back_populates="expenses", sa_relationship=relationship("Category", back_populates="expenses")
    )
    owner: Optional["User"] = Relationship(
        back_populates="expenses", sa_relationship=relationship("User", back_populates="expenses")
    )
