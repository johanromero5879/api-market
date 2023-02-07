from abc import abstractmethod
from app.common.domain import Repository, ValueId
from app.product.domain import ProductIn, ProductOut, ProductPatch


class ProductRepository(Repository):
    @abstractmethod
    def insert_one(self, product: ProductIn) -> ProductOut:
        pass

    @abstractmethod
    def update_one(self, id: ValueId, product: ProductPatch) -> ProductOut:
        pass

    @abstractmethod
    def decrease_stock(self, id: ValueId, quantity: float, session):
        pass

    @abstractmethod
    def delete_one(self, id: ValueId):
        pass

    @abstractmethod
    def find_all(self, limit: int, skip: int, owner_schema: bool = True) -> list[ProductOut]:
        pass

    @abstractmethod
    def find_by(self, field: str, value, owner_schema: bool = True) -> ProductOut:
        pass

    @abstractmethod
    def exists_by(self, field: str, value) -> bool:
        pass
