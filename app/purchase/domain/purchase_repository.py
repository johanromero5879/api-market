from abc import abstractmethod

from app.common.domain import Repository
from app.purchase.domain import PurchaseIn, PurchaseOut


class PurchaseRepository(Repository):
    @abstractmethod
    def insert_one(self, purchase: PurchaseIn, session) -> PurchaseOut:
        pass

    @abstractmethod
    def find_by(self, field, value) -> PurchaseOut:
        pass

    @abstractmethod
    def find(self, field, value) -> list[PurchaseOut]:
        pass
