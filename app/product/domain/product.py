from pydantic import BaseModel
from app.common.domain import ValueID
from app.user.domain import BaseUser


class Product(BaseModel):
    id: ValueID | None
    name: str | None
    description: str | None
    unit_price: float | None
    stock: int | None
    owner: ValueID | None


class ProductSchema(Product):
    owner: ValueID | BaseUser | None


class ProductCreate(Product):
    name: str
    description: str
    unit_price: float
    stock: int


