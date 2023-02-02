from pydantic import BaseModel

from app.common.domain import ValueID
from app.user.domain import BaseUser


class AuthOut(BaseModel):
    id: ValueID
    email: str
    password: str


class AuthIn(BaseUser):
    password: str
