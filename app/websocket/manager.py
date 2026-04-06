from collections import defaultdict
from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self._rooms: dict[int, set[WebSocket]] = defaultdict(set)

    async def connect(self, room_id: int, ws: WebSocket):
        await ws.accept()
        self._rooms[room_id].add(ws)

    def disconnect(self, room_id: int, ws: WebSocket):
        self._rooms[room_id].discard(ws)

    async def broadcast(self, room_id: int, text: str):
        dead = set()
        for ws in self._rooms[room_id]:
            try:
                await ws.send_text(text)
            except Exception:
                dead.add(ws)
        self._rooms[room_id] -= dead


manager = ConnectionManager()
