from fastapi import APIRouter, Depends, status, HTTPException
from dependency_injector.wiring import Provide, inject

from app.product.application import ProductNotFoundError
from app.purchase.domain import PurchaseOut, BasePurchase, BaseDetail
from app.purchase.application import PurchaseService, NotEnoughStockError, EmptyDetailError, NotEnoughBudgetError
from app.user.domain import UserOut

from app.auth.infrastructure import get_current_user

router = APIRouter(
    prefix="/purchases",
    tags=["purchases"]
)


@router.post(path="/", response_model=PurchaseOut, status_code=status.HTTP_201_CREATED)
@inject
def purchase_products(
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
