from fastapi import Depends, HTTPException, status

from app.common.domain import ValueID
from app.user.domain import User
from app.auth.infrastructure import get_current_user
from app.product.application import ProductNotFoundError
from app.common.container import product_service


async def verify_product_ownership(
        id: ValueID,
        user: User = Depends(get_current_user)):
    try:

        product_found = product_service.get_by("id", id, owner_schema=False)

        if not product_found.owner or product_found.owner != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Unauthorized to modify or remove this product"
            )

    except ProductNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )