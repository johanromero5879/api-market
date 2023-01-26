from fastapi import APIRouter, HTTPException, status, Depends
from dependency_injector.wiring import Provide, inject

from app.user.domain import User, UserCreate
from app.user.application import UserNotFoundError, UserFoundError, UserService
from app.auth.infrastructure import get_current_user
from app.common.domain import ValueID

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.get("/me", response_model=User)
async def me(user: User = Depends(get_current_user)):
    return user


@router.get("/", response_model=list[User])
@inject
async def users(
    limit: int = 10,
    page: int = 1,
    user_service: UserService = Depends(Provide["services.user"])
):
    try:
        return user_service.get_all(limit, page)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
@inject
async def create(
    user: UserCreate,
    user_service: UserService = Depends(Provide["services.user"])
):
    try:
        return user_service.create_one(user)
    except UserFoundError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))


@router.get("/{id}", response_model=User)
@inject
async def user(
    id: ValueID,
    user_service: UserService = Depends(Provide["services.user"])
):
    try:
        return user_service.get_by("id", id)
    except UserNotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))


@router.patch("/{id}", response_model=User)
@inject
async def update(
    id: ValueID,
    user: User,
    user_service: UserService = Depends(Provide["services.user"])
):
    try:
        return user_service.update_one(id, user)
    except UserNotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
    except UserFoundError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete(
    id: ValueID,
    user_service: UserService = Depends(Provide["services.user"])
):
    try:
        user_service.delete(id)
    except UserNotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
