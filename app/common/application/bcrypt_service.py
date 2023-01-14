from passlib.context import CryptContext


class BCryptService:
    __crypt: CryptContext

    def __init__(self):
        self.__crypt = CryptContext(schemes=["bcrypt"])

    def compare(self, text: str, hash: str) -> bool:
        return bool(self.__crypt.verify(text, hash))

