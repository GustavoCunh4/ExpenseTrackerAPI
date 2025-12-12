from typing import List, Optional

from sqlmodel import select

from app.models.expense_model import Category
from app.models.schemas import CategoryCreate, CategoryUpdate
from app.repositories.base_repository import BaseRepository


class CategoryRepository(BaseRepository):
    async def create(self, owner_id: int, data: CategoryCreate) -> Category:
        category = Category(name=data.name, owner_id=owner_id)
        return await self.save(category)

    async def list_by_owner(self, owner_id: int) -> List[Category]:
        result = await self.session.execute(
            select(Category).where(Category.owner_id == owner_id).order_by(Category.created_at.desc())
        )
        return list(result.scalars().all())

    async def get_owned(self, category_id: int, owner_id: int) -> Optional[Category]:
        result = await self.session.execute(
            select(Category).where(Category.id == category_id, Category.owner_id == owner_id)
        )
        return result.scalars().first()

    async def update(self, category: Category, data: CategoryUpdate) -> Category:
        if data.name is not None:
            category.name = data.name
        return await self.save(category)

    async def delete(self, category: Category) -> None:
        await self.session.delete(category)
        await self.session.commit()
