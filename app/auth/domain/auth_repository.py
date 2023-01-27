from abc import abstractmethod

from app.common.domain import Repository, ValueID
from app.auth.domain import Auth, AuthIn


class AuthRepository(Repository):
    @abstractmethod
    def find_by(self, field: str, value) -> Auth | None:
        pass

    @abstractmethod
    def exists_by(self, field: str, value) -> Auth | None:
        pass

    @abstractmethod
    def insert_one(self, user: AuthIn) -> ValueID:
        pass
