from fastapi import APIRouter, HTTPException, status, Depends

from app.user.domain import User, UserCreate
from app.user.application import UserNotFoundError
from app.auth.infrastructure import get_current_user
from app.common.domain import ValueID
from app.common.container import user_service

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.get("/me", response_model=User)
async def me(user: User = Depends(get_current_user)):
    return user


@router.get("/", response_model=list[User])
async def users(limit: int = 10, skip: int = 0):
    return user_service.get_all(limit, skip)


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create(user: UserCreate):
    return user_service.create_one(user)


@router.get("/{id}", response_model=User)
async def user(id: ValueID):
    try:
        print(type(id))
        return user_service.get_by_id(id)
    except UserNotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))


@router.patch("/{id}", response_model=User)
async def update(id: ValueID, user: User):
    try:
        return user_service.update_one(id, user)
    except UserNotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: ValueID):
    try:
        user_service.delete(id)
    except UserNotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
