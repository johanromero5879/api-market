from app.common.domain import ValueID
from app.common.infrastructure import MongoRepository
from app.product.domain import ProductRepository, Product, ProductCreate, ProductSchema
from app.product.application import ProductNotFoundError


class MongoProductRepository(MongoRepository[Product], ProductRepository):
    @property
    def collection_name(self) -> str:
        return "products"

    __project = {
        "id": "$_id",
        "_id": 0,
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

    def _get_model_instance(self, product: dict) -> Product:
        product["id"] = str(product["id"])

        if "owner" in product:
            if self.is_object_id(product["owner"]):
                product["owner"] = str(product["owner"])
            else:
                product["owner"]["id"] = str(product["owner"]["id"])
                return ProductSchema(**product)

        return Product(**product)

    def insert_one(self, product: ProductCreate) -> Product:
        if self.is_object_id(product.owner):
            product.owner = self.get_object_id(product.owner)

        product_id = self.collection().insert_one(product.dict(exclude_none=True)).inserted_id
        product.id = str(product_id)
        product.owner = str(product.owner)

        return product

    def update_one(self, id: ValueID, product: Product) -> Product:
        if not self.is_object_id(id):
            raise ProductNotFoundError()

        product_updated = self.collection().find_one_and_update(
            {"_id": self.get_object_id(id)},
            {"$set": product.dict(exclude_none=True)},
            self.__project,
            return_document=True
        )

        return self._get_model_instance(product_updated)

    def delete_one(self, id: ValueID):
        if not self.is_object_id(id):
            raise ProductNotFoundError()

        self.collection().delete_one({"_id": self.get_object_id(id)})

    def find_all(self, limit: int, skip: int, owner_schema: bool = True) -> list[Product]:
        if owner_schema:
            products = self.collection().aggregate([
                {"$project": self.__project},
                {"$lookup": self.__lookup_owner},
                {"$unwind": self.__unwind_owner},
                {"$sort": {"name": 1}},
                {"$skip": skip},
                {"$limit": limit}
            ])
        else:
            products = self.collection().find(projection=self.__project)\
                        .sort("name", 1).skip(skip).limit(limit)

        return self._get_model_list(products)

    def find_by(self, field: str, value, owner_schema: bool = True) -> Product | None:
        field, value = self._get_format_filter(field, value)

        if owner_schema:
            product = self.collection().aggregate([
                {"$match": {field: value}},
                {"$project": self.__project},
                {"$lookup": self.__lookup_owner},
                {"$unwind": self.__unwind_owner},
                {"$limit": 1}
            ])

            product = product.next()
        else:
            product = self.collection().find_one({field: value}, self.__project)

        if bool(product):
            return self._get_model_instance(product)

    def exists_by(self, field: str, value) -> bool:
        field, value = self._get_format_filter(field, value)

        product = self.collection().find_one({field: value}, {"_id": 1})

        return bool(product)
