from fastapi import APIRouter, Body, HTTPException, Response, status
from src.models.auth import LoginPayload, UserModel
from src.services import authentication

router = APIRouter()


@router.get(
    "/health",
    summary="Simple route for health check.",
)
async def health():
    return Response(status_code=200)


@router.post(
    "/oauth",
    response_model=str,
    summary="Generate a JWT from a login attempt",
)
async def login(payload: LoginPayload = Body(..., title="User login payload")):
    user: UserModel = authentication.authenticate(payload.username, payload.password)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return authentication.create_token({"identity": user.id})
