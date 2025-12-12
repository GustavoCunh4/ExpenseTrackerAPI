from datetime import timedelta

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.db import get_session
from app.core.security import create_access_token, get_password_hash, verify_password
from app.models.schemas import Token, UserCreate, UserRead
from app.models.user_model import User
from app.repositories.user_repository import UserRepository


class AuthService:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session
        self.repo = UserRepository(session)
        self.settings = get_settings()

    async def register(self, payload: UserCreate) -> UserRead:
        existing = await self.repo.get_by_email(payload.email)
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email já cadastrado")

        hashed = get_password_hash(payload.password)
        user = await self.repo.create(email=payload.email, hashed_password=hashed)
        return UserRead.from_orm(user)

    async def authenticate(self, email: str, password: str) -> User:
        user = await self.repo.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")
        return user

    def build_token(self, user: User) -> Token:
        expires_delta = timedelta(minutes=self.settings.access_token_expire_minutes)
        token = create_access_token({"sub": user.id}, expires_delta=expires_delta)
        return Token(access_token=token, token_type="bearer")
