from datetime import datetime
from pydantic import BaseModel


class MessageRead(BaseModel):
    id: str
    content: str
    user_id: str
    room_id: str
    created_at: datetime
    username: str | None = None
