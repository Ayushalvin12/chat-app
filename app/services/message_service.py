from sqlalchemy.ext.asyncio import AsyncSession

from app.models.message import Message
from app.repositories.message_repository import MessageRepository


class MessageService:
    def __init__(self, db: AsyncSession, message_repo: MessageRepository):
        self.db = db
        self.message_repo = message_repo

    async def get_recent(
        self, room_id: int, limit: int = 50, cursor: int | None = None
    ) -> list[Message]:
        return await self.message_repo.get_recent(room_id, limit, cursor)

    async def save_message(self, content: str, user_id: int, room_id: int) -> Message:
        message = Message(content=content, user_id=user_id, room_id=room_id)
        await self.message_repo.create(message)
        await self.db.commit()
        await self.db.refresh(message)
        return message
