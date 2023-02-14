from app.common.domain import ValueId
from app.common.application import Service
from app.product.domain import ProductIn, ProductRepository, ProductPatch
from app.product.application import ProductFoundError, ProductNotFoundError


class ProductService(Service):
    __repository: ProductRepository

    def __init__(self, repository: ProductRepository):
        self.__repository = repository

    def get_all(self, limit: int, page: int, owner_schema: bool = True):
        if limit <= 0 or limit > 20:
            raise ValueError("Limit parameter must be between 1 and 20")

        if page <= 0:
            raise ValueError("Page parameter must be greater than 1")

        skip = (page - 1) * limit
        return self.__repository.find_all(limit, skip, owner_schema)

    def get_by(self, field, value, owner_schema: bool = True):
        product = self.__repository.find_by(field, value, owner_schema)

        if not product:
            raise ProductNotFoundError()

        return product

    def create_one(self, product: ProductIn):
        if self.__repository.exists_by("name", product.name):
            raise ProductFoundError()

        return self.__repository.insert_one(product)

    def update_one(self, id: ValueId, product: ProductPatch):
        if product.name:
            product_found = self.__repository.find_by("name", product.name, owner_schema=False)
            if product_found and id != product_found.id:
                raise ProductFoundError()

        return self.__repository.update_one(id, product)

    def delete_one(self, id: ValueId):
        if not self.__repository.exists_by("id", id):
            raise ProductNotFoundError()

        self.__repository.delete_one(id)
