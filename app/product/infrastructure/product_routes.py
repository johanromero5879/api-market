from fastapi import APIRouter, status, HTTPException, Depends
from app.auth.infrastructure import get_current_user
from app.product.infrastructure import verify_product_ownership
from app.product.domain import Product, ProductCreate, ProductSchema
from app.user.domain import User
from app.product.application import ProductFoundError, ProductNotFoundError

from app.common.domain import ValueID
from app.common.container import product_service

router = APIRouter(
    prefix="/products",
    tags=["products"]
)


@router.get("/", response_model=list[ProductSchema])
async def get_products(limit: int = 10, page: int = 1):
    try:
        return product_service.get_all(limit, page)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))


@router.get("/{id}", response_model=ProductSchema)
async def get_product(id: ValueID):
    try:
        return product_service.get_by("id", id)
    except ProductNotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))


@router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
async def register(product: ProductCreate, user: User = Depends(get_current_user)):
    """
    Register a new product.
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
    response_model=Product
)
async def update(id: ValueID, product: Product):
    try:
        return product_service.update_one(id, product)
    except ProductFoundError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))


@router.delete(
    path="/{id}",
    dependencies=[Depends(verify_product_ownership)],
    status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: ValueID):
    try:
        product_service.delete_one(id)
    except ProductNotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
