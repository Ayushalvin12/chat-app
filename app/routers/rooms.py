from fastapi import APIRouter, Depends
from uuid import UUID

from app.dependencies import get_room_service, get_current_user
from app.models.user import User
from app.schemas.room import RoomCreate, RoomRead
from app.services.room_service import RoomService

router = APIRouter(prefix="/rooms", tags=["rooms"])


@router.post(
    "/",
    response_model=RoomRead,
    status_code=201,
    summary="Create a new chat room",
    description="Create a new chat room with a unique name and optional description.",
)
async def create_room(
    payload: RoomCreate,
    service: RoomService = Depends(get_room_service),
    _: User = Depends(get_current_user),
):
    return await service.create_room(payload)


@router.get(
    "/",
    response_model=list[RoomRead],
    summary="List all chat rooms",
    description="Retrieve a list of all available chat rooms accessible to the authenticated user.",
)
async def list_rooms(
    service: RoomService = Depends(get_room_service),
    _: User = Depends(get_current_user),
):
    return await service.get_all_rooms()


@router.get(
    "/{room_id}",
    response_model=RoomRead,
    summary="Get room details",
    description="Retrieve detailed information about a specific chat room using its unique ID.",
)
async def get_room(
    room_id: UUID,
    service: RoomService = Depends(get_room_service),
    _: User = Depends(get_current_user),
):
    return await service.get_room(room_id)
