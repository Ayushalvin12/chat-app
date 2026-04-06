from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class RoomCreate(BaseModel):
    name: str
    description: str | None = None


class RoomRead(BaseModel):
    id: UUID
    name: str
    description: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}