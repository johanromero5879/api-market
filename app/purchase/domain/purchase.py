from datetime import datetime

from pydantic import Field

from app.common.domain import ValueId, Model
from app.user.domain import BaseUser


class BaseDetail(Model):
    product_id: ValueId
    quantity: int


class Detail(BaseDetail):
    name: str
    unit_price: float
    total: float


class BasePurchase(Model):
    customer: ValueId
    detail: list[BaseDetail]


class PurchaseIn(BasePurchase):
    detail: list[Detail]
    total: float
    created_at: datetime = Field(default_factory=datetime.utcnow)


class PurchaseOut(PurchaseIn):
    id: ValueId
    customer: ValueId | BaseUser
