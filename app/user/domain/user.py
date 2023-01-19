from pydantic import BaseModel
from app.common.domain import ValueID


class User(BaseModel):
    id: ValueID | None
    first_name: str | None
    last_name: str | None
    email: str | None
    disabled: bool | None


class UserCreate(User):
    first_name: str
    last_name: str
    email: str
    disabled: bool = False
