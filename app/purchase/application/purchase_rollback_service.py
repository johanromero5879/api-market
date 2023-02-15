from dependency_injector.wiring import Provide, inject

from app.common.domain import ValueId
from app.common.application import Service, Transaction
from app.purchase.domain import PurchaseRepository, Detail
from app.product.domain import ProductRepository
from app.user.domain import UserRepository
from app.purchase.application import PurchaseNotFoundError


class PurchaseRollbackService(Service):
    __purchase_repository: PurchaseRepository
    __product_repository: ProductRepository
    __user_repository: UserRepository

    def __init__(self,
                 purchase_repository: PurchaseRepository,
                 product_repository: ProductRepository,
                 user_repository: UserRepository
                 ):
        self.__purchase_repository = purchase_repository
        self.__product_repository = product_repository
        self.__user_repository = user_repository

    @inject
    def rollback(self, id: ValueId, transaction: Transaction = Provide["services.transaction"]):
        purchase = self.__purchase_repository.find_by("id", id)
        if not purchase:
            raise PurchaseNotFoundError()

        try:
            transaction.start()

            self.__return_products_to_stock(
                details=purchase.detail,
                session=transaction.get_session()
            )

            self.__refund_total_to_user(
                user_id=purchase.customer,
                total=purchase.total,
                session=transaction.get_session()
            )

            self.__purchase_repository.delete_one(purchase.id, transaction.get_session())

            transaction.commit()
        except Exception as error:
            transaction.rollback()
            raise error

    def __return_products_to_stock(self, details: list[Detail], session):
        for item in details:
            self.__product_repository.increase_stock(
                id=item.product_id,
                quantity=item.quantity,
                session=session
            )

    def __refund_total_to_user(self, user_id: ValueId, total: float, session):
        self.__user_repository.raise_budget(
            id=user_id,
            cost=total,
            session=session
        )
