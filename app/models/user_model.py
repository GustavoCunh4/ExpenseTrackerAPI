from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from pydantic import EmailStr
from sqlalchemy.orm import relationship
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.expense_model import Category, Expense


class UserBase(SQLModel):
    email: EmailStr


class User(UserBase, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    categories: list["Category"] = Relationship(
        back_populates="owner", sa_relationship=relationship("Category", back_populates="owner")
    )
    expenses: list["Expense"] = Relationship(
        back_populates="owner", sa_relationship=relationship("Expense", back_populates="owner")
    )
