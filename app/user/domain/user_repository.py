from abc import abstractmethod
from app.common.domain import Repository, ValueID
from app.user.domain import User, UserCreate


class UserRepository(Repository):
    @abstractmethod
    def find_all(self, limit: int, skip: int) -> list[User]:
        pass

    @abstractmethod
    def find_by(self, field: str, value) -> User | None:
        pass

    @abstractmethod
    def exists_by(self, field: str, value) -> bool:
        pass

    @abstractmethod
    def insert_one(self, user: UserCreate) -> User:
        pass

    @abstractmethod
    def update_one(self, id: ValueID, user: User) -> User:
        pass

    @abstractmethod
    def delete(self, id: ValueID):
        pass
