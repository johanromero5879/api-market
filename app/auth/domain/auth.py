from app.common.domain import ValueId, Model
from app.user.domain import BaseUser, UserIn


class AuthOut(Model):
    id: ValueId
    email: str
    password: str


class BaseAuth(BaseUser):
    password: str


class AuthIn(UserIn):
    password: str
