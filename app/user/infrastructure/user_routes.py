from fastapi import APIRouter, HTTPException, status, Depends
from dependency_injector.wiring import Provide, inject

from app.user.domain import UserOut, UserPatch
from app.user.application import UserNotFoundError, UserFoundError, UserService
from app.user.infrastructure import verify_same_user
from app.auth.infrastructure import get_current_user
from app.common.domain import ValueId

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.get("/me", response_model=UserOut)
async def me(user: UserOut = Depends(get_current_user)):
    return user


@router.get("/", response_model=list[UserOut])
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


@router.get(path="/{id}", response_model=UserOut)
@inject
async def user(
    id: ValueId,
    user_service: UserService = Depends(Provide["services.user"])
):
    try:
        return user_service.get_by("id", id)
    except UserNotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))


@router.patch(
    path="/{id}",
    response_model=UserOut,
    dependencies=[Depends(verify_same_user)]
)
@inject
async def update(
    id: ValueId,
    user: UserPatch,
    user_service: UserService = Depends(Provide["services.user"])
):
    try:
        return user_service.update_one(id, user)
    except UserNotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
    except UserFoundError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))


@router.delete(
    path="/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(verify_same_user)]
)
@inject
async def delete(
    id: ValueId,
    user_service: UserService = Depends(Provide["services.user"])
):
    try:
        user_service.delete(id)
    except UserNotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
