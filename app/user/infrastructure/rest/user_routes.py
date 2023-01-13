from typing import List
from fastapi import APIRouter, HTTPException, status
from app.common.container import user_service
from app.user.domain.user import User, UserCreate

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.get("/", response_model=List[User])
async def users(limit: int = 10, skip: int = 0):
    return user_service.get_all(limit, skip)


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create(user: UserCreate):
    return user_service.create_one(user)


@router.get("/{id}", response_model=User)
async def user(id: str):
    try:
        return user_service.get_by_id(id)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.patch("/{id}", response_model=User)
async def update(id: str, user: User):
    try:
        return user_service.update_one(id, user)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: str):
    try:
        user_service.delete(id)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))
