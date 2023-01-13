from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    id: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]


class UserCreate(User):
    first_name: str
    last_name: str
    email: str

