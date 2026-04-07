from datetime import datetime

from fastapi import APIRouter, Depends, Query
from uuid import UUID

from app.dependencies import get_message_service, get_current_user
from app.models.user import User
from app.schemas.message import MessageRead
from app.services.message_service import MessageService

router = APIRouter(prefix="/messages", tags=["messages"])


@router.get(
    "/{room_id}",
    response_model=list[MessageRead],
    summary="Get messages in a room",
    description=(
        "Retrieve messages for a specific chat room using cursor-based pagination. "
        "Provide a `cursor` (timestamp of the oldest message received) to fetch older messages. "
        "Messages are returned in descending order of creation time."
    ),
)
async def get_messages(
    room_id: UUID,
    cursor: datetime | None = Query(
        None,
        description="created_at of the oldest message you received — fetch messages older than this",
    ),
    limit: int = Query(50, le=100),
    service: MessageService = Depends(get_message_service),
    _: User = Depends(get_current_user),
):
    messages = await service.get_recent(room_id, limit, cursor)
    return [
        MessageRead(
            id=str(m.id),
            content=m.content,
            user_id=str(m.user_id),
            room_id=str(m.room_id),
            created_at=m.created_at,
            username=m.author.username if m.author else None,
        )
        for m in messages
    ]
