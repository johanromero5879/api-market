from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.user.domain import User
from app.user.application import UserNotFoundError
from app.auth.application import CredentialsError
from app.common.container import auth_service, user_service

oauth2 = OAuth2PasswordBearer(tokenUrl="auth/login")


async def authenticate_user(token: str = Depends(oauth2)):
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
