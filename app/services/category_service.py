from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.models.schemas import CategoryCreate, CategoryRead, CategoryUpdate
from app.repositories.category_repository import CategoryRepository


class CategoryService:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.repo = CategoryRepository(session)

    async def create(self, user_id: int, payload: CategoryCreate) -> CategoryRead:
        category = await self.repo.create(owner_id=user_id, data=payload)
        return CategoryRead.from_orm(category)

    async def list(self, user_id: int):
        categories = await self.repo.list_by_owner(user_id)
        return [CategoryRead.from_orm(cat) for cat in categories]

    async def update(self, user_id: int, category_id: int, payload: CategoryUpdate) -> CategoryRead:
        category = await self.repo.get_owned(category_id, user_id)
        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoria não encontrada")
        updated = await self.repo.update(category, payload)
        return CategoryRead.from_orm(updated)

    async def delete(self, user_id: int, category_id: int) -> None:
        category = await self.repo.get_owned(category_id, user_id)
        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoria não encontrada")
        await self.repo.delete(category)
