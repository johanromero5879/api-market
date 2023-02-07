from dependency_injector import containers, providers

from app.purchase.infrastructure import MongoPurchaseRepository
from app.product.infrastructure import MongoProductRepository
from app.user.infrastructure import MongoUserRepository
from app.auth.infrastructure import MongoAuthRepository


class Repositories(containers.DeclarativeContainer):

    gateways = providers.DependenciesContainer()

    user = providers.Singleton(MongoUserRepository, client=gateways.database_client)
    auth = providers.Singleton(MongoAuthRepository, client=gateways.database_client)
    product = providers.Singleton(MongoProductRepository, client=gateways.database_client)
    purchase = providers.Singleton(MongoPurchaseRepository, client=gateways.database_client)
