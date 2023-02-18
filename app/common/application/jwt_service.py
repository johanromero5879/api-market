from datetime import datetime, timedelta
from jose import jwt


class JWTService:
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 1440  # 1 day
    __JWT_SECRET_KEY: str

    def __init__(self, jwt_secret: str):
        self.__JWT_SECRET_KEY = jwt_secret

    def create_access_token(self, identifier: str) -> str:
        return self.__create_token(identifier, self.ACCESS_TOKEN_EXPIRE_MINUTES)

    def create_refresh_token(self, identifier: str) -> str:
        return self.__create_token(identifier, self.REFRESH_TOKEN_EXPIRE_MINUTES)

    def __create_token(self, identifier: str, expires_in: int) -> str:
        """
        :param identifier: A string that identifies certain resource
        :param expires_in: Time expiration given in minutes
        :return: JWT Token
        """
        payload = {
            "sub": identifier,
            "exp": datetime.utcnow() + timedelta(minutes=expires_in)
        }

        return jwt.encode(payload, self.__JWT_SECRET_KEY)

    def decode(self, token: str) -> dict:
        return jwt.decode(token, self.__JWT_SECRET_KEY)
