from datetime import datetime, timedelta
from jose import jwt
from app.config import JWT_SECRET


class JWTService:
    __ALGORITHM: str = "HS256"
    __EXPIRATION: int = 1  # minutes

    def encrypt(self, payload: dict) -> str:
        # Set time expiration based on current datetime
        payload["exp"] = datetime.utcnow() + timedelta(minutes=self.__EXPIRATION)

        return jwt.encode(payload, JWT_SECRET, algorithm=self.__ALGORITHM)
