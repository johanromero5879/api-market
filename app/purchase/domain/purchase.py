from datetime import datetime
from pydantic import BaseModel
from app.common.domain import ValueID
from app.user.domain import BaseUser


class ItemDetail(BaseModel):
    id: ValueID
    quantity: int
    name: str | None
    unit_price: float | None
    total: float | None


class Purchase(BaseModel):
    id: ValueID | None
    customer: ValueID | None
    detail: list[ItemDetail] | None
    total: float | None
    created_at: datetime | None


class PurchaseIn(Purchase):
    detail: list[ItemDetail]


class PurchaseOut(Purchase):
    customer: ValueID | BaseUser | None
