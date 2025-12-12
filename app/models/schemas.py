from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import EmailStr, conint, constr
from sqlmodel import Field, SQLModel


class ORMModel(SQLModel):
    class Config:
        orm_mode = True


class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(SQLModel):
    sub: Optional[int] = None


class UserCreate(SQLModel):
    email: EmailStr
    password: constr(min_length=6)


class UserRead(ORMModel):
    id: int
    email: EmailStr
    created_at: datetime


class CategoryCreate(SQLModel):
    name: constr(min_length=2, max_length=100)


class CategoryUpdate(SQLModel):
    name: Optional[constr(min_length=2, max_length=100)] = None


class CategoryRead(ORMModel):
    id: int
    name: str
    created_at: datetime


class ExpenseCreate(SQLModel):
    title: constr(min_length=2, max_length=200)
    amount: float
    date: datetime
    category_id: int
    description: Optional[str] = None


class ExpenseUpdate(SQLModel):
    title: Optional[constr(min_length=2, max_length=200)] = None
    amount: Optional[float] = None
    date: Optional[datetime] = None
    category_id: Optional[int] = None
    description: Optional[str] = None


class ExpenseRead(ORMModel):
    id: int
    title: str
    amount: float
    date: datetime
    category_id: int
    description: Optional[str] = None
    created_at: datetime


class CategorySummary(SQLModel):
    category: str
    total: float


class MonthlySummary(SQLModel):
    month: conint(ge=1, le=12)
    year: conint(ge=1970)
    total: float
    by_category: List[CategorySummary] = Field(default_factory=list)
