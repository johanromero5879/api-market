from typing import Mapping, Any

from bson import ObjectId
from pymongo import MongoClient
from pymongo.client_session import ClientSession


from app.common.infrastructure import MongoAdapter
from app.product.domain import ProductRepository, ProductOut, ProductIn, ProductPatch


class MongoProductRepository(MongoAdapter[ProductOut], ProductRepository):
    __project = {
        "_id": 0,
        "id": "$_id",
        "name": 1,
        "description": 1,
        "unit_price": 1,
        "stock": 1,
        "owner": 1
    }

    __lookup_owner = {
        "from": "users",
        "localField": "owner",
        "foreignField": "_id",
        "as": "owner",
        "pipeline": [
            {"$project": {
                "id": "$_id",
                "_id": 0,
                "first_name": 1,
                "last_name": 1,
                "email": 1
            }}
        ]
    }

    __unwind_owner = {
        "path": "$owner",
        "preserveNullAndEmptyArrays": True
    }

    def __init__(self, client: MongoClient | None = None):
        super().__init__("products", client)

    def _get_model_instance(self, product: Mapping[str, Any]) -> ProductOut:
        return ProductOut(**product)

    def insert_one(self, product: ProductIn) -> ProductOut:
        product_id = self._collection.insert_one(product.dict(exclude_none=True)).inserted_id

        return ProductOut(
            id=product_id,
            **product.dict()
        )

    def update_one(self, id: ObjectId, product: ProductPatch) -> ProductOut:

        product_updated = self._collection.find_one_and_update(
            {"_id": id},
            {"$set": product.dict(exclude_none=True)},
            self.__project,
            return_document=True
        )

        return self._get_model_instance(product_updated)

    def decrease_stock(self, id: ObjectId, quantity: float, session: ClientSession):
        self._collection.update_one(
            {"_id": id},
            {"$inc": {"stock": -quantity}},
            session=session
        )

    def delete_one(self, id: ObjectId):
        self._collection.delete_one({"_id": id})

    def find_all(self, limit: int, skip: int, owner_schema: bool = True) -> list[ProductOut]:
        if owner_schema:
            products = self._collection.aggregate([
                {"$project": self.__project},
                {"$lookup": self.__lookup_owner},
                {"$unwind": self.__unwind_owner},
                {"$sort": {"name": 1}},
                {"$skip": skip},
                {"$limit": limit}
            ])
        else:
            products = self._collection.find(projection=self.__project)\
                        .sort("name", 1).skip(skip).limit(limit)

        return self._get_model_list(products)

    def find_by(self, field: str, value, owner_schema: bool = True) -> ProductOut | None:
        field, value = self._get_format_filter(field, value)

        if owner_schema:
            product = self._collection.aggregate([
                {"$match": {field: value}},
                {"$project": self.__project},
                {"$lookup": self.__lookup_owner},
                {"$unwind": self.__unwind_owner},
                {"$limit": 1}
            ])

            product = product.next()
        else:
            product = self._collection.find_one({field: value}, self.__project)

        if product:
            return self._get_model_instance(product)

    def exists_by(self, field: str, value) -> bool:
        field, value = self._get_format_filter(field, value)

        product = self._collection.find_one({field: value}, {"_id": 1})

        return bool(product)
