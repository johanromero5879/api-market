from datetime import datetime, timedelta
from jose import jwt


class JWTService:
    __access_token_expiration: int = 1  # minutes
    __jwt_secret: str

    def __init__(self, jwt_secret: str):
        self.__jwt_secret = jwt_secret

    def __create_token(self, payload: dict, expiration: int):
        # Set time expiration based on current datetime plus n minutes
        payload["exp"] = datetime.utcnow() + timedelta(minutes=expiration)

        return jwt.encode(payload, self.__jwt_secret)

    def create_access_token(self, payload: dict) -> str:
        return self.__create_token(payload, self.__access_token_expiration)

    def decode(self, token: str) -> dict:
        return jwt.decode(token, self.__jwt_secret)
