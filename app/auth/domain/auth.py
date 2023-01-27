from pydantic import BaseModel

from app.common.domain import ValueID


class Auth(BaseModel):
    id: ValueID | None
    email: str
    password: str


class AuthIn(Auth):
    first_name: str
    last_name: str


class UserIn(AuthIn):
    budget: float = 0
    disabled: bool = False
