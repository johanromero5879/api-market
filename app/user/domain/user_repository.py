from abc import abstractmethod
from app.common.domain import Repository, ValueId
from app.user.domain import UserOut, UserBudget, UserPatch


class UserRepository(Repository):
    @abstractmethod
    def find_all(self, limit: int, skip: int) -> list[UserOut]:
        pass

    @abstractmethod
    def find_by(self, field: str, value) -> UserOut | None:
        pass

    @abstractmethod
    def update_one(self, id: ValueId, user: UserPatch) -> UserOut:
        pass

    @abstractmethod
    def delete(self, id: ValueId):
        pass

    @abstractmethod
    def exists_by(self, field: str, value) -> bool:
        pass

    @abstractmethod
    def find_budget(self, id: ValueId) -> UserBudget | None:
        pass

    @abstractmethod
    def raise_budget(self, id: ValueId, cost: float, session):
        pass

    @abstractmethod
    def reduce_budget(self, id: ValueId, cost: float, session):
        pass
