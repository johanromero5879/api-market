from pydantic import BaseModel
from app.common.domain import ValueID


class BaseUser(BaseModel):
    id: ValueID | None
    first_name: str | None
    last_name: str | None
    email: str | None


class User(BaseUser):
    disabled: bool | None


class UserBudget(BaseModel):
    id: ValueID
    budget: float
