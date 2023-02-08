from app.common.domain import ValueId, Model


class BaseUser(Model):
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
    id: ValueId
    disabled: bool


class UserBudget(Model):
    id: ValueId
    budget: float
