from abc import abstractmethod
from app.common.domain.repository import Repository
from app.user.domain.user import User, UserCreate
from app.common.domain.value_id import ValueID


class UserRepository(Repository):
    @abstractmethod
    def find_all(self, limit: int, skip: int) -> list[User]:
        pass

    @abstractmethod
    def find_by_id(self, id: ValueID) -> User | None:
        pass

    @abstractmethod
    def exists_id(self, id: ValueID) -> bool:
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> User | None:
        pass

    @abstractmethod
    def exists_email(self, email: str) -> bool:
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
