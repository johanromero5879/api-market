from fastapi import APIRouter, Depends, status, HTTPException
from dependency_injector.wiring import Provide, inject

from app.common.domain import ValueId
from app.product.application import ProductNotFoundError
from app.purchase.domain import PurchaseOut, BasePurchase, BaseDetail
from app.purchase.application import PurchaseService, PurchaseRollbackService, NotEnoughStockError, EmptyDetailError, NotEnoughBudgetError, PurchaseNotFoundError
from app.purchase.infrastructure import verify_purchase_ownership
from app.user.domain import UserOut

from app.auth.infrastructure import get_current_user

router = APIRouter(
    prefix="/purchases",
    tags=["purchases"]
)


@router.post(path="/", response_model=PurchaseOut, status_code=status.HTTP_201_CREATED)
@inject
async def purchase_products(
    detail: list[BaseDetail],
    customer: UserOut = Depends(get_current_user),
    purchase_service: PurchaseService = Depends(Provide["services.purchase"])
):

    purchase = BasePurchase(
        customer=customer.id,  # Set customer id into customer property of the purchase
        detail=detail
    )

    try:
        return purchase_service.purchase(purchase)
    except (NotEnoughStockError, EmptyDetailError, ProductNotFoundError) as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    except NotEnoughBudgetError as error:
        raise HTTPException(status_code=status.HTTP_402_PAYMENT_REQUIRED, detail=str(error))


@router.delete(
    path="/{id}/rollback",
    dependencies=[Depends(verify_purchase_ownership)],
    status_code=status.HTTP_204_NO_CONTENT
)
@inject
async def rollback(
    id: ValueId,
    purchase_service: PurchaseRollbackService = Depends(Provide["services.purchase_rollback"])
):
    try:
        purchase_service.rollback(id)
    except PurchaseNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )
