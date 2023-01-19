from passlib.context import CryptContext


class BCryptService:
    __crypt: CryptContext

    def __init__(self):
        self.__crypt = CryptContext(schemes=["bcrypt"])

    def compare(self, text: str, hash: str) -> bool:
        try:
            return bool(self.__crypt.verify(text, hash))
        except Exception:
            return False
        
    def create_hash(self, text: str) -> str:
        return self.__crypt.hash(text)
