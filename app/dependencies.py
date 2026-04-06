from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import (
    InvalidTokenError,
    JWTAuthenticationError,
    PermissionDeniedError,
)
from app.database import get_db
from app.models.user import User, UserRole
from app.repositories.message_repository import MessageRepository
from app.repositories.room_repository import RoomRepository
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.services.room_service import RoomService
from app.services.message_service import MessageService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_user_repo(db: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepository(db)


def get_room_repo(db: AsyncSession = Depends(get_db)) -> RoomRepository:
    return RoomRepository(db)


def get_message_repo(db: AsyncSession = Depends(get_db)) -> MessageRepository:
    return MessageRepository(db)


def get_auth_service(
    db: AsyncSession = Depends(get_db),
    user_repo: UserRepository = Depends(get_user_repo),
) -> AuthService:
    return AuthService(db=db, user_repo=user_repo)


def get_room_service(
    db: AsyncSession = Depends(get_db),
    room_repo: RoomRepository = Depends(get_room_repo),
) -> RoomService:
    return RoomService(db=db, room_repo=room_repo)


def get_message_service(
    db: AsyncSession = Depends(get_db),
    message_repo: MessageRepository = Depends(get_message_repo),
) -> MessageService:
    return MessageService(db=db, message_repo=message_repo)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_repo: UserRepository = Depends(get_user_repo),
) -> User:
    payload = AuthService.decode_token(token)

    username: str | None = payload.get("sub")
    if not username:
        raise InvalidTokenError()

    user = await user_repo.get_by_username(username)
    if not user:
        raise JWTAuthenticationError(detail="User not found")

    return user


def require_role(*roles: UserRole):
    async def _enforce(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in roles:
            raise PermissionDeniedError()
        return current_user

    return _enforce
