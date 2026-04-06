import json
from uuid import UUID
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query

from app.database import AsyncSessionLocal
from app.repositories.message_repository import MessageRepository
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.services.message_service import MessageService
from app.schemas.message import MessageRead
from app.websocket.manager import manager

router = APIRouter(tags=["websocket"])


async def _authenticate(token: str):
    try:
        payload = AuthService.decode_token(token)
        username = payload.get("sub")
    except Exception:
        return None
    async with AsyncSessionLocal() as db:
        return await UserRepository(db).get_by_username(username)


@router.websocket("/ws/{room_id}")
async def websocket_endpoint(room_id: UUID, ws: WebSocket, token: str = Query(...)):
    user = await _authenticate(token)
    if not user:
        await ws.close(code=1008)
        return

    await manager.connect(room_id, ws)

    async with AsyncSessionLocal() as db:
        repo = MessageRepository(db)
        service = MessageService(db=db, message_repo=repo)
        messages = await service.get_recent(room_id)

    history = [
        {
            **MessageRead(
                id=str(m.id),
                content=m.content,
                user_id=str(m.user_id),
                room_id=str(m.room_id),
                created_at=m.created_at,
                username=m.author.username if m.author else None,
            ).model_dump(mode="json")
        }
        for m in messages
    ]
    await ws.send_text(json.dumps({"type": "history", "messages": history}))

    try:
        while True:
            data = await ws.receive_text()
            body = json.loads(data)
            content = body.get("content", "").strip()
            if not content:
                continue

            async with AsyncSessionLocal() as db:
                repo = MessageRepository(db)
                service = MessageService(db=db, message_repo=repo)
                msg = await service.save_message(content, user.id, room_id)

            await manager.broadcast(
                room_id,
                json.dumps(
                    {
                        "type": "message",
                        "id": str(msg.id),
                        "content": msg.content,
                        "user_id": str(msg.user_id),
                        "username": user.username,
                        "room_id": str(room_id),
                        "created_at": msg.created_at.isoformat(),
                    }
                ),
            )

    except WebSocketDisconnect:
        manager.disconnect(room_id, ws)
