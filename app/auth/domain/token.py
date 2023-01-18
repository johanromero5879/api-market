from pydantic import BaseModel
from app.common.domain import ValueID


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: ValueID | None = None
