from fastapi import APIRouter, Depends, Query

from app.dependencies import get_message_service, get_current_user
from app.models.user import User
from app.schemas.message import MessageRead
from app.services.message_service import MessageService

router = APIRouter(prefix="/messages", tags=["messages"])


@router.get("/{room_id}", response_model=list[MessageRead])
async def get_messages(
    room_id: int,
    cursor: int | None = Query(None),
    limit: int = Query(50, le=100),
    service: MessageService = Depends(get_message_service),
    _: User = Depends(get_current_user),
):
    messages = await service.get_recent(room_id, limit, cursor)
    return [
        MessageRead(
            id=m.id,
            content=m.content,
            user_id=m.user_id,
            room_id=m.room_id,
            created_at=m.created_at,
            username=m.author.username if m.author else None,
        )
        for m in messages
    ]
