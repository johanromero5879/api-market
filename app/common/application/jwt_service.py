from datetime import datetime, timedelta
from jose import jwt
from app.config import JWT_SECRET


class JWTService:
    __ALGORITHM: str = "HS256"
    __ACCESS_TOKEN_EXPIRATION: int = 1  # minutes

    def __create_token(self, payload: dict, expiration: int):
        # Set time expiration based on current datetime plus n minutes
        payload["exp"] = datetime.utcnow() + timedelta(minutes=expiration)

        return jwt.encode(payload, JWT_SECRET, algorithm=self.__ALGORITHM)

    def create_access_token(self, payload: dict) -> str:
        return self.__create_token(payload, self.__ACCESS_TOKEN_EXPIRATION)

    def decode(self, token: str) -> dict:
        return jwt.decode(token, JWT_SECRET, algorithms=[self.__ALGORITHM])
