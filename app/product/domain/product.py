from pydantic import BaseModel
from app.common.domain import ValueID
from app.user.domain import BaseUser


class Product(BaseModel):
    id: ValueID | None
    name: str | None
    description: str | None
    price: float | None
    quantity: int | None
    owner: ValueID | None


class ProductSchema(Product):
    owner: ValueID | BaseUser | None


class ProductCreate(Product):
    name: str
    description: str
    price: float
    quantity: int


