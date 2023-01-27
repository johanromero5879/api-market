from pymongo import MongoClient

from app.purchase.domain import PurchaseRepository, Purchase, PurchaseIn
from app.common.infrastructure import MongoRepository


class MongoPurchaseRepository(MongoRepository[Purchase], PurchaseRepository):
    def __init__(self, client: MongoClient | None = None):
        super().__init__("purchases", client)

    def _get_model_instance(self, purchase: dict) -> Purchase:
        purchase["id"] = str(purchase["id"])
        return Purchase(**purchase)

    def insert_one(self, purchase: PurchaseIn) -> Purchase:
        if self.is_object_id(purchase.customer):
            purchase.customer = self.get_object_id(purchase.customer)

        purchase_id = self._collection.insert_one(purchase.dict(exclude_none=True)).inserted_id
        purchase.id = str(purchase_id)
        purchase.customer = str(purchase.customer)

        return purchase

    def find_by(self, field, value) -> Purchase:
        pass

    def find(self, field, value) -> list[Purchase]:
        pass
