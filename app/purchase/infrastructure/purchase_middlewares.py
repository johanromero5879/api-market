from fastapi import Depends, HTTPException, status
from dependency_injector.wiring import Provide, inject

from app.common.domain import ValueId
from app.auth.infrastructure import get_current_user
from app.user.domain import UserOut
from app.purchase.application import PurchaseService, PurchaseNotFoundError


@inject
async def verify_purchase_ownership(
    id: ValueId,
    customer: UserOut = Depends(get_current_user),
    purchase_service: PurchaseService = Depends(Provide["services.purchase"])
):
    try:
        purchase = purchase_service.find_by("id", id)

        if purchase.customer != customer.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Unauthorized to modify or delete this purchase"
            )

    except PurchaseNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )
