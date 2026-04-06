from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class MessageRead(BaseModel):
    id: UUID
    content: str
    user_id: int
    room_id: int
    created_at: datetime
    username: str | None = None

    model_config = {"from_attributes": True}
