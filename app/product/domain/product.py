from pydantic import BaseModel

from app.common.domain import ValueID
from app.user.domain import BaseUser


class BaseProduct(BaseModel):
    name: str
    description: str
    unit_price: float
    stock: int


class ProductIn(BaseProduct):
    owner: ValueID | None


class ProductOut(BaseProduct):
    id: ValueID
    owner: ValueID | BaseUser | None


class ProductPatch(BaseProduct):
    name: str | None
    description: str | None
    unit_price: float | None
    stock: int | None
