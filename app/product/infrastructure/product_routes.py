from fastapi import APIRouter, status, HTTPException, Depends
from dependency_injector.wiring import Provide, inject

from app.auth.infrastructure import get_current_user
from app.product.infrastructure.product_middlewares import verify_product_ownership
from app.product.domain import ProductPatch, ProductOut, ProductIn
from app.user.domain import UserOut
from app.product.application import ProductFoundError, ProductNotFoundError, ProductService

from app.common.domain import ValueId

router = APIRouter(
    prefix="/products",
    tags=["products"]
)


@router.get("/", response_model=list[ProductOut])
@inject
async def get_products(
    limit: int = 10,
    page: int = 1,
    product_service: ProductService = Depends(Provide["services.product"])
):
    try:
        return product_service.get_all(limit, page)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))


@router.get("/{id}", response_model=ProductOut)
@inject
async def get_product(
    id: ValueId,
    product_service: ProductService = Depends(Provide["services.product"])
):
    try:
        return product_service.get_by("id", id)
    except ProductNotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))


@router.post("/", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
@inject
async def register(
    product: ProductIn,
    user: UserOut = Depends(get_current_user),
    product_service: ProductService = Depends(Provide["services.product"])
):
    """
    Register a new product.
    :param product_service: service given by dependency injection
    :param product: product data
    :param user: logged user who will register the new product
    """
    try:
        # Set product owner as logged user id
        product.owner = user.id

        return product_service.create_one(product)
    except (ProductFoundError, ProductNotFoundError) as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))


@router.patch(
    path="/{id}",
    dependencies=[Depends(verify_product_ownership)],
    response_model=ProductOut
)
@inject
async def update(
    id: ValueId,
    product: ProductPatch,
    product_service: ProductService = Depends(Provide["services.product"])
):
    try:
        return product_service.update_one(id, product)
    except ProductFoundError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))


@router.delete(
    path="/{id}",
    dependencies=[Depends(verify_product_ownership)],
    status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete(
    id: ValueId,
    product_service: ProductService = Depends(Provide["services.product"])
):
    try:
        product_service.delete_one(id)
    except ProductNotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
