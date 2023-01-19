from abc import abstractmethod
from app.common.domain import Repository
from app.auth.domain import Auth


class AuthRepository(Repository):
    @abstractmethod
    def find_by(self, field: str, value) -> Auth | None:
        pass
