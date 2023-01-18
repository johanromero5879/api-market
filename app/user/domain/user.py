from pydantic import BaseModel
from app.common.domain.value_id import ValueID


class User(BaseModel):
    id: ValueID | None
    first_name: str | None
    last_name: str | None
    email: str | None
    disabled: bool = False


class UserCreate(User):
    first_name: str
    last_name: str
    email: str
