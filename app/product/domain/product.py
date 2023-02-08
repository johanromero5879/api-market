from app.common.domain import ValueId, Model
from app.user.domain import BaseUser


class BaseProduct(Model):
    name: str
    description: str
    unit_price: float
    stock: int


class ProductIn(BaseProduct):
    owner: ValueId | None


class ProductOut(BaseProduct):
    id: ValueId
    owner: ValueId | BaseUser | None


class ProductPatch(BaseProduct):
    name: str | None
    description: str | None
    unit_price: float | None
    stock: int | None
