from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from uuid import UUID

from app.models.message import Message


class MessageRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_recent(
        self,
        room_id: UUID,
        limit: int = 50,
        cursor: datetime | None = None,
    ) -> list[Message]:
        query = (
            select(Message)
            .where(Message.room_id == room_id)
            .options(selectinload(Message.author))
        )
        if cursor:
            query = query.where(Message.created_at < cursor)
        query = query.order_by(Message.id.desc()).limit(limit)
        result = await self.db.execute(query)
        return list(reversed(result.scalars().all()))

    async def create(self, message: Message) -> Message:
        self.db.add(message)
        return message
