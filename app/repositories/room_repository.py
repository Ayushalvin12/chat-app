from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.room import Room


class RoomRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> list[Room]:
        result = await self.db.execute(select(Room).order_by(Room.created_at))
        return list(result.scalars().all())

    async def get_by_id(self, room_id: int) -> Room | None:
        result = await self.db.execute(select(Room).where(Room.id == room_id))
        return result.scalar_one_or_none()

    async def get_by_name(self, name: str) -> Room | None:
        result = await self.db.execute(select(Room).where(Room.name == name))
        return result.scalar_one_or_none()

    async def create(self, room: Room) -> Room:
        self.db.add(room)
        return room