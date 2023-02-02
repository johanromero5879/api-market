from datetime import datetime

from pydantic import BaseModel

from app.common.domain import ValueID
from app.user.domain import BaseUser


class BaseItemDetail(BaseModel):
    id: ValueID
    quantity: int


class ItemDetail(BaseItemDetail):
    name: str
    unit_price: float
    total: float


class BasePurchase(BaseModel):
    customer: ValueID | None
    detail: list[BaseItemDetail]


class PurchaseIn(BasePurchase):
    customer: ValueID
    detail: list[ItemDetail]
    total: float
    created_at: datetime


class PurchaseOut(PurchaseIn):
    id: ValueID
    customer: ValueID | BaseUser
