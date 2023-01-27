from abc import abstractmethod
from app.common.domain import Repository
from app.purchase.domain import PurchaseIn, Purchase


class PurchaseRepository(Repository):
    @abstractmethod
    def insert_one(self, purchase: PurchaseIn) -> Purchase:
        pass

    @abstractmethod
    def find_by(self, field, value) -> Purchase:
        pass

    @abstractmethod
    def find(self, field, value) -> list[Purchase]:
        pass
