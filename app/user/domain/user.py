from pydantic import BaseModel


class User(BaseModel):
    id: str | None
    first_name: str | None
    last_name: str | None
    email: str | None
    disabled: bool = False


class UserCreate(User):
    first_name: str
    last_name: str
    email: str
