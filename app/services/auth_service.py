from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.core.exceptions import (
    EmailAlreadyExistsError,
    InvalidCredentialsError,
    TokenExpiredOrInvalidError,
    UsernameAlreadyExistsError,
)
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, Token

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def __init__(self, db: AsyncSession, user_repo: UserRepository):
        self.db = db
        self.user_repo = user_repo

    async def signup(self, payload: UserCreate) -> User:
        if await self.user_repo.get_by_username(payload.username):
            raise UsernameAlreadyExistsError()

        if await self.user_repo.get_by_email(payload.email):
            raise EmailAlreadyExistsError()

        user = User(
            username=payload.username,
            email=payload.email,
            hashed_password=pwd_ctx.hash(payload.password),
            role=payload.role,
        )
        await self.user_repo.create(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def login(self, username: str, password: str) -> Token:
        user = await self.user_repo.get_by_username(username)
        if not user or not pwd_ctx.verify(password, user.hashed_password):
            if not user or not pwd_ctx.verify(password, user.hashed_password):
                raise InvalidCredentialsError()
        token = self._create_token({"sub": user.username, "role": user.role.value})
        return Token(access_token=token)

    @staticmethod
    def _create_token(data: dict) -> str:
        payload = data.copy()
        payload["exp"] = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    @staticmethod
    def decode_token(token: str) -> dict:
        try:
            return jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
        except JWTError:
            raise TokenExpiredOrInvalidError()
