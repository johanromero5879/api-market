from typing import Mapping, Any

from bson import ObjectId
from pymongo import MongoClient
from pymongo.client_session import ClientSession

from app.purchase.domain import PurchaseRepository, PurchaseOut, PurchaseIn
from app.common.infrastructure import MongoAdapter


class MongoPurchaseRepository(MongoAdapter[PurchaseOut], PurchaseRepository):
    __project = {
        "_id": 0,
        "id": "$_id",
        "customer": 1,
        "detail": 1,
        "total": 1,
        "created_at": 1
    }

    def __init__(self, client: MongoClient | None = None):
        super().__init__("purchases", client)

    def find(self, field: str, value) -> list[PurchaseOut]:
        field, value = self._get_format_filter(field, value)

        purchases = self._collection.find_one({field: value}, self.__project)

        return self._get_model_list(purchases)

    def find_by(self, field: str, value) -> PurchaseOut | None:
        field, value = self._get_format_filter(field, value)

        purchase = self._collection.find_one({field: value}, self.__project)

        if purchase:
            return self._get_model_instance(purchase)

    def insert_one(self, purchase: PurchaseIn, session: ClientSession) -> PurchaseOut:

        purchase_id = self._collection.insert_one(
            purchase.dict(exclude_none=True),
            session=session
        ).inserted_id

        return PurchaseOut(
            id=purchase_id,
            **purchase.dict(),
        )

    def delete_one(self, id: ObjectId, session: ClientSession):
        self._collection.delete_one(
            filter={"_id": id},
            session=session
        )

    def _get_model_instance(self, document: Mapping[str, Any]) -> PurchaseOut:
        return PurchaseOut(**document)
