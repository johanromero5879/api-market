from fastapi import APIRouter, Depends, HTTPException, status, Response, Cookie
from fastapi.security import OAuth2PasswordRequestForm
from dependency_injector.wiring import Provide, inject

from app.common.application import JWTService
from app.user.application import UserFoundError
from app.auth.application import CredentialsError, AuthService
from app.auth.domain import BaseAuth, Token

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/token", response_model=Token)
@inject
async def login(
    response: Response,
    form: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(Provide["services.auth"])
):
    """
    :param response:
    :param auth_service: service given by dependency injection
    :param form: username value is email, it is called username in the form by OAuth2 specification
    """
    try:
        user_id = auth_service.authenticate_user(email=form.username, password=form.password)
        access_token, refresh_token = auth_service.generate_user_tokens(user_id)

        return generate_token_response(response, access_token, refresh_token)
    except CredentialsError as error:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(error))


@router.post("/signup", response_model=Token, status_code=status.HTTP_201_CREATED)
@inject
async def signup(
    response: Response,
    user: BaseAuth,
    auth_service: AuthService = Depends(Provide["services.auth"])
):
    try:
        user_id = auth_service.register_user(user)
        access_token, refresh_token = auth_service.generate_user_tokens(user_id)

        return generate_token_response(response, access_token, refresh_token)
    except UserFoundError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))


@router.post("/refresh-token")
@inject
async def refresh(
    response: Response,
    refresh_token: str = Cookie(None),
    auth_service: AuthService = Depends(Provide["services.auth"])
):
    if not refresh_token:
        raise_token_error("Missing refresh token")

    user_id = auth_service.get_user_payload(refresh_token).user_id

    if not auth_service.exists_by("id", user_id):
        raise_token_error("Invalid refresh token")

    access_token, refresh_token = auth_service.generate_user_tokens(user_id)

    return generate_token_response(response, access_token, refresh_token)


def generate_token_response(response: Response, access_token: str, refresh_token: str) -> Token:
    refresh_token_expire_seconds = JWTService.REFRESH_TOKEN_EXPIRE_MINUTES * 60

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        max_age=refresh_token_expire_seconds
    )

    return Token(
        access_token=access_token,
        token_type="bearer"
    )


def raise_token_error(detail: str):
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"}
    )


@router.delete(path="/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(response: Response):
    response.delete_cookie(key="refresh_token", httponly=True)
