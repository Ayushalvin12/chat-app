from fastapi import APIRouter, Depends

from app.dependencies import get_auth_service
from app.schemas.user import UserCreate, UserRead, LoginRequest, Token
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/signup",
    response_model=UserRead,
    status_code=201,
    summary="Register a new user",
    description="Create a new user account with a username and password. Returns the created user details.",
)
async def signup(
    payload: UserCreate,
    service: AuthService = Depends(get_auth_service),
):
    return await service.signup(payload)


@router.post(
    "/login",
    response_model=Token,
    summary="Authenticate user",
    description="Authenticate a user using username and password. Returns a JWT access token upon successful login.",
)
async def login(
    payload: LoginRequest,
    service: AuthService = Depends(get_auth_service),
):
    return await service.login(payload.username, payload.password)
