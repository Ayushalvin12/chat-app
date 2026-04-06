from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.core.exceptions import RoomAlreadyExistsError, RoomNotFoundError
from app.models.room import Room
from app.repositories.room_repository import RoomRepository
from app.schemas.room import RoomCreate


class RoomService:
    def __init__(self, db: AsyncSession, room_repo: RoomRepository):
        self.db = db
        self.room_repo = room_repo

    async def create_room(self, payload: RoomCreate) -> Room:
        if await self.room_repo.get_by_name(payload.name):
            raise RoomAlreadyExistsError()
        room = Room(name=payload.name, description=payload.description)
        await self.room_repo.create(room)
        await self.db.commit()
        await self.db.refresh(room)
        return room

    async def get_all_rooms(self) -> list[Room]:
        return await self.room_repo.get_all()

    async def get_room(self, room_id: UUID) -> Room:
        room = await self.room_repo.get_by_id(room_id)
        if not room:
            raise RoomNotFoundError()
        return room
