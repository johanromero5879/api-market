from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from dependency_injector.wiring import Provide, inject

from app.auth.application import Token, CredentialsError, AuthService

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/login", response_model=Token)
@inject
async def login(
    form: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(Provide["services.auth"])
):
    """
    :param auth_service: service given by dependency injection
    :param form: username value is email, it is called username in the form by OAuth2 specification
    """
    try:
        return auth_service.authenticate_user(email=form.username, password=form.password)
    except CredentialsError as error:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(error))

