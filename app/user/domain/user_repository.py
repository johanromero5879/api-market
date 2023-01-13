from abc import abstractmethod
from typing import List, Optional
from app.common.domain.repository import Repository
from app.user.domain.user import User, UserCreate


class UserRepository(Repository):
    @abstractmethod
    def find_all(self, limit: int, skip: int) -> List[User]:
        pass

    @abstractmethod
    def find_by_id(self, id: str) -> Optional[User]:
        pass

    @abstractmethod
    def exists_id(self, id: str) -> bool:
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    def exists_email(self, email: str) -> bool:
        pass

    @abstractmethod
    def insert_one(self, user: User) -> User:
        pass

    @abstractmethod
    def update_one(self, id: str, user: User) -> User:
        pass

    @abstractmethod
    def delete(self, id: str):
        pass
