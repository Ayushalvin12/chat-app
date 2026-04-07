from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.database import engine, Base
from app.models import user, room, message
from app.routers import auth, rooms, messages
from app.routers.ws_router import router as ws_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title="Chat App", lifespan=lifespan)


@app.get("/")
async def root():
    return {"status": "ok", "message": "Chat App is running "}


app.include_router(auth.router)
app.include_router(rooms.router)
app.include_router(messages.router)
app.include_router(ws_router)
