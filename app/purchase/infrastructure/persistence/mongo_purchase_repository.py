from typing import Mapping, Any

from pymongo import MongoClient
from pymongo.client_session import ClientSession

from app.purchase.domain import PurchaseRepository, PurchaseOut, PurchaseIn
from app.common.infrastructure import MongoAdapter


class MongoPurchaseRepository(MongoAdapter[PurchaseOut], PurchaseRepository):

    def __init__(self, client: MongoClient | None = None):
        super().__init__("purchases", client)

    def _get_model_instance(self, document: Mapping[str, Any]) -> PurchaseOut:
        return PurchaseOut(**document)

    def insert_one(self, purchase: PurchaseIn, session: ClientSession) -> PurchaseOut:

        purchase_id = self._collection.insert_one(
            purchase.dict(exclude_none=True),
            session=session
        ).inserted_id

        return PurchaseOut(
            id=purchase_id,
            **purchase.dict(),
        )

    def find_by(self, field: str, value) -> PurchaseOut:
        pass

    def find(self, field: str, value) -> list[PurchaseOut]:
        pass
