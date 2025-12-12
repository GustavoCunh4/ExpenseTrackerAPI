from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.security import get_current_user
from app.models.schemas import Token, UserCreate, UserRead
from app.models.user_model import User
from app.services.auth_service import AuthService

router = APIRouter()


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(payload: UserCreate, service: AuthService = Depends(AuthService)):
    return await service.register(payload)


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), service: AuthService = Depends(AuthService)):
    user = await service.authenticate(form_data.username, form_data.password)
    return service.build_token(user)


@router.get("/me", response_model=UserRead)
async def me(current_user: User = Depends(get_current_user)):
    return UserRead.from_orm(current_user)
