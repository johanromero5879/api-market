from pydantic import BaseModel

from app.common.domain import ValueID


class BaseUser(BaseModel):
    first_name: str
    last_name: str
    email: str


class UserPatch(BaseUser):
    first_name: str | None
    last_name: str | None
    email: str | None


class UserIn(BaseUser):
    budget: float = 0
    disabled: bool = False


class UserOut(BaseUser):
    id: ValueID
    disabled: bool


class UserBudget(BaseModel):
    id: ValueID
    budget: float
