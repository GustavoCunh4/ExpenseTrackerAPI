from fastapi import APIRouter, Depends, status

from app.core.security import get_current_user
from app.models.schemas import CategoryCreate, CategoryRead, CategoryUpdate
from app.models.user_model import User
from app.services.category_service import CategoryService

router = APIRouter()


@router.get("/", response_model=list[CategoryRead])
async def list_categories(
    service: CategoryService = Depends(CategoryService), current_user: User = Depends(get_current_user)
):
    return await service.list(current_user.id)


@router.post("/", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
async def create_category(
    payload: CategoryCreate,
    service: CategoryService = Depends(CategoryService),
    current_user: User = Depends(get_current_user),
):
    return await service.create(current_user.id, payload)


@router.put("/{category_id}", response_model=CategoryRead)
async def update_category(
    category_id: int,
    payload: CategoryUpdate,
    service: CategoryService = Depends(CategoryService),
    current_user: User = Depends(get_current_user),
):
    return await service.update(current_user.id, category_id, payload)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: int,
    service: CategoryService = Depends(CategoryService),
    current_user: User = Depends(get_current_user),
):
    await service.delete(current_user.id, category_id)
