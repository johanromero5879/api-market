from copy import deepcopy

from pymongo import MongoClient
from pymongo.client_session import ClientSession

from app.purchase.domain import PurchaseRepository, PurchaseOut, PurchaseIn, ItemDetail
from app.common.infrastructure import MongoRepository


class MongoPurchaseRepository(MongoRepository[PurchaseOut], PurchaseRepository):
    def __init__(self, client: MongoClient | None = None):
        super().__init__("purchases", client)

    def _get_model_instance(self, purchase: dict) -> PurchaseOut:
        purchase["id"] = str(purchase["id"])

        if "customer" in purchase and self.is_object_id(purchase["customer"]):
            purchase["customer"] = str(purchase["customer"])

        return PurchaseOut(**purchase)

    def insert_one(self, purchase: PurchaseIn, session: ClientSession) -> PurchaseOut:
        if self.is_object_id(purchase.customer):
            purchase.customer = self.get_object_id(purchase.customer)

        original_detail, purchase.detail = self.__transform_detail(purchase.detail)

        # Insert in db with all id as ObjectID
        purchase_id = self._collection.insert_one(
            purchase.dict(exclude_none=True),
            session=session
        ).inserted_id

        # Set ObjectID to str before to return
        purchase.customer = str(purchase.customer)
        purchase.detail = original_detail

        return PurchaseOut(
            id=str(purchase_id),
            **purchase.dict(),
        )

    def __transform_detail(self, original_detail: list[ItemDetail]) -> tuple[list[ItemDetail], list]:
        """
        Transform all products id into ObjectId before are inserted in db
        :param original_detail: detail to be copied
        :return: original and copied detail with products id transformation
        """
        #
        copy = deepcopy(original_detail)

        def item_id_to_object(item: ItemDetail):
            item.id = self.get_object_id(item.id)
            return item

        return original_detail, list(map(item_id_to_object, copy))

    def find_by(self, field, value) -> PurchaseOut:
        pass

    def find(self, field, value) -> list[PurchaseOut]:
        pass
