from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from dependency_injector.wiring import Provide, inject

from app.user.domain import User
from app.user.application import UserNotFoundError, UserService
from app.auth.application import CredentialsError, AuthService

oauth2 = OAuth2PasswordBearer(tokenUrl="auth/login")


@inject
async def authenticate_user(
    token: str = Depends(oauth2),
    user_service: UserService = Depends(Provide["services.user"]),
    auth_service: AuthService = Depends(Provide["services.auth"])
):
    try:
        user_id = auth_service.get_user_payload(token).user_id
        user = user_service.get_by("id", user_id)
        return user
    except (UserNotFoundError, CredentialsError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )


async def get_current_user(user: User = Depends(authenticate_user)):
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")

    return user
