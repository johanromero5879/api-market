from dependency_injector.wiring import Provide, inject

from app.common.domain import ValueId
from app.common.application import Service, Transaction
from app.product.domain import ProductRepository
from app.product.application import ProductNotFoundError
from app.purchase.domain import PurchaseRepository, BasePurchase, BaseDetail, Detail, PurchaseIn
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

    @inject
    def purchase(self, purchase: BasePurchase, transaction: Transaction = Provide["services.transaction"]):
        # Check if a customer id is associated to the purchase
        if not purchase.customer:
            raise NoCustomerError()

        try:
            # Start injected transaction
            transaction.start()

            # Extract a detail list of items and total of products
            total, purchase.detail = self.__process_detail(purchase.detail, transaction.get_session())

            # Process payment from user budget
            self.__process_payment(purchase.customer, total, transaction.get_session())

            purchase = PurchaseIn(
                customer=purchase.customer,
                detail=purchase.detail,
                total=total
            )

            # Make a record of the purchase
            purchase = self._repository.insert_one(purchase, transaction.get_session())

            # Commit transaction to send changes to database
            transaction.commit()

            return purchase
        except Exception as error:
            # If anything fails, database operations will be rollback and there will be no changes on it
            transaction.rollback()

            raise error

    def __process_detail(self, detail: list[BaseDetail], session) -> (float, list[Detail]):
        """
        :param detail: list of items
        :return: tuple when first parameter is total of all items, second one the detail list with additional info
        """
        if len(detail) == 0:
            raise EmptyDetailError()

        total: float = 0

        for index, item in enumerate(detail):
            product = self.__product_repository.find_by("id", item.product_id, owner_schema=False)

            if not product:
                raise ProductNotFoundError(id=item.product_id)

            if product.stock == 0 or item.quantity > product.stock:
                raise NotEnoughStockError(item_name=product.name)

            item = Detail(
                **item.dict(),
                name=product.name,
                unit_price=product.unit_price,
                total=product.unit_price * item.quantity  # Works out total price
            )

            total += item.total
            detail[index] = item

            # Decrease stock from product
            self.__product_repository.decrease_stock(product.id, item.quantity, session)

        return total, detail

    def __process_payment(self, user_id: ValueId, cost: float, session):
        user = self.__user_repository.find_budget(user_id)

        if not user or user.budget < cost:
            raise NotEnoughBudgetError()

        # Reduce cost purchase from user budget
        self.__user_repository.reduce_budget(user.id, cost, session)

