from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.auth.domain.auth import Auth, User
from app.auth.application.auth_service import AuthResponse
from app.auth.application.auth_errors import CredentialsError
from app.user.application.user_errors import UserNotFoundError
from app.common.container import auth_service, user_service

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)
oauth2 = OAuth2PasswordBearer(tokenUrl="auth/login")


async def current_user(token: str = Depends(oauth2)):
    try:
        user = user_service.get_by_email(token)
        if user.disabled:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")

        return user
    except UserNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication credentials are not valid",
            headers={"WWW-Authenticate": "Bearer"}
        )


@router.post("/login", response_model=AuthResponse)
async def login(form: OAuth2PasswordRequestForm = Depends()):
    try:
        return auth_service.get_auth(Auth(email=form.username, password=form.password))
    except CredentialsError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))


@router.get("/me")
async def me(user: User = Depends(current_user)):
    return user
