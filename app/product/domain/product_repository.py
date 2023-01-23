from abc import abstractmethod
from app.common.domain import Repository, ValueID
from app.product.domain import Product, ProductCreate


class ProductRepository(Repository):
    @abstractmethod
    def insert_one(self, product: ProductCreate) -> Product:
        pass

    @abstractmethod
    def update_one(self, id: ValueID, product: Product) -> Product:
        pass

    @abstractmethod
    def delete_one(self, id: ValueID):
        pass

    @abstractmethod
    def find_all(self, limit: int, skip: int, owner_schema: bool = True) -> list[Product]:
        pass

    @abstractmethod
    def find_by(self, field: str, value, owner_schema: bool = True) -> Product:
        pass

    @abstractmethod
    def exists_by(self, field: str, value) -> bool:
        pass
