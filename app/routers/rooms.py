from fastapi import APIRouter, Depends
from uuid import UUID

from app.dependencies import get_room_service, get_current_user
from app.models.user import User
from app.schemas.room import RoomCreate, RoomRead
from app.services.room_service import RoomService

router = APIRouter(prefix="/rooms", tags=["rooms"])


@router.post("/", response_model=RoomRead, status_code=201)
async def create_room(
    payload: RoomCreate,
    service: RoomService = Depends(get_room_service),
    _: User = Depends(get_current_user),
):
    return await service.create_room(payload)


@router.get("/", response_model=list[RoomRead])
async def list_rooms(
    service: RoomService = Depends(get_room_service),
    _: User = Depends(get_current_user),
):
    return await service.get_all_rooms()


@router.get("/{room_id}", response_model=RoomRead)
async def get_room(
    room_id: UUID,
    service: RoomService = Depends(get_room_service),
    _: User = Depends(get_current_user),
):
    return await service.get_room(room_id)
