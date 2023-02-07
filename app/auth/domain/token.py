from pydantic import BaseModel
from app.common.domain import ValueId


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: ValueId | None = None
