from abc import abstractmethod

from app.common.domain import Repository, ValueId
from app.purchase.domain import PurchaseIn, PurchaseOut


class PurchaseRepository(Repository):
    @abstractmethod
    def find(self, field: str, value) -> list[PurchaseOut]:
        pass

    @abstractmethod
    def find_by(self, field: str, value) -> PurchaseOut | None:
        pass

    @abstractmethod
    def insert_one(self, purchase: PurchaseIn, session) -> PurchaseOut:
        pass

    @abstractmethod
    def delete_one(self, id: ValueId, session):
        pass
