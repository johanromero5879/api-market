from datetime import datetime

from app.common.domain import ValueID
from app.common.application import Service
from app.product.domain import ProductRepository
from app.product.application import ProductNotFoundError
from app.purchase.domain import PurchaseRepository, PurchaseIn, Purchase, ItemDetail
from app.purchase.application import EmptyDetailError, NotEnoughStockError, NoCustomerError, NotEnoughBudgetError
from app.user.domain import UserRepository


class PurchaseService(Service):
    _repository: PurchaseRepository
    __product_repository: ProductRepository

    def __init__(self,
                 repository: PurchaseRepository,
                 product_repository: ProductRepository,
                 user_repository: UserRepository
                 ):
        super().__init__(repository)
        self.__product_repository = product_repository
        self.__user_repository = user_repository

    def purchase(self, purchase: PurchaseIn) -> Purchase:
        purchase.id = None

        # Check if a customer id is associated to the purchase
        if not purchase.customer:
            raise NoCustomerError()

        try:
            # Start transaction in product, purchase and user repositories
            self.__product_repository.start_transaction()
            self._repository.start_transaction()
            self.__user_repository.start_transaction()

            # Extract a detail list of items and total of products
            purchase.total, purchase.detail = self.__process_detail(purchase.detail)

            # Process payment from user budget
            self.__process_payment(purchase.customer, purchase.total)

            purchase.created_at = datetime.now()

            # Make a record of the purchase
            purchase = self._repository.insert_one(purchase)

            # IMPORTANT: commit transactions in all repositories implied
            # Commit transaction to send changes to database
            self.__product_repository.commit_transaction()
            self._repository.commit_transaction()
            self.__user_repository.commit_transaction()

            return purchase
        except Exception as error:
            # If anything fails, database operations will be rollback and there will be no changes on it
            self.__product_repository.rollback_transaction()
            self._repository.rollback_transaction()
            self.__user_repository.rollback_transaction()

            raise error

    def __process_detail(self, detail: list[ItemDetail]) -> (float, list[ItemDetail]):
        """
        :param detail: list of items
        :return: tuple when first parameter is total of all items, second one the detail list with additional info
        """
        if len(detail) == 0:
            raise EmptyDetailError()

        total: float = 0

        for index, item in enumerate(detail):
            product = self.__product_repository.find_by("id", item.id, owner_schema=False)

            if not product:
                raise ProductNotFoundError(id=item.id)

            if item.quantity > product.stock:
                raise NotEnoughStockError(item_name=product.name)

            # Retrieve product info at the moment of purchasing into the item detail
            item.name = product.name
            item.unit_price = product.unit_price

            # Works out total price
            item.total = item.unit_price * item.quantity
            total += item.total

            detail[index] = item

            # Decrease stock from product
            self.__product_repository.decrease_stock(product.id, item.quantity)

        return total, detail

    def __process_payment(self, user_id: ValueID, cost: float):
        user = self.__user_repository.find_budget(user_id)

        if not user or user.budget < cost:
            raise NotEnoughBudgetError()

        # Reduce cost purchase from user budget
        self.__user_repository.reduce_budget(user.id, cost)

