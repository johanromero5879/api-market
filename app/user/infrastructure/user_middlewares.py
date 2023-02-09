from fastapi import Depends, HTTPException, status
from dependency_injector.wiring import inject

from app.common.domain import ValueId
from app.user.domain import UserOut
from app.auth.infrastructure import get_current_user


@inject
async def verify_same_user(
    id: ValueId,
    user: UserOut = Depends(get_current_user)
):
    if id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unauthorized to modify or remove this user"
        )
