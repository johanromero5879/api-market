from dependency_injector import containers, providers
from pymongo import MongoClient

from app.common.application import JWTService, BCryptService

from app.purchase.application import PurchaseService
from app.purchase.infrastructure import MongoPurchaseRepository

from app.product.application import ProductService
from app.product.infrastructure import MongoProductRepository

from app.user.application import UserService
from app.user.infrastructure import MongoUserRepository

from app.auth.application import AuthService
from app.auth.infrastructure import MongoAuthRepository


class Gateways(containers.DeclarativeContainer):

    config = providers.Configuration(strict=True)

    database_client = providers.Singleton(MongoClient, config.database.uri)


class Repositories(containers.DeclarativeContainer):

    gateways = providers.DependenciesContainer()

    user = providers.Singleton(MongoUserRepository, client=gateways.database_client)
    auth = providers.Singleton(MongoAuthRepository, client=gateways.database_client)
    product = providers.Singleton(MongoProductRepository, client=gateways.database_client)
    purchase = providers.Singleton(MongoPurchaseRepository, client=gateways.database_client)


class Services(containers.DeclarativeContainer):

    config = providers.Configuration(strict=True)
    repositories = providers.DependenciesContainer()

    jwt = providers.Singleton(JWTService, jwt_secret=config.jwt.secret)
    bcrypt = providers.Singleton(BCryptService)

    user = providers.Singleton(
        UserService,
        repository=repositories.user
    )

    auth = providers.Singleton(
        AuthService,
        repository=repositories.auth,
        jwt_service=jwt,
        bcrypt_service=bcrypt
    )

    product = providers.Singleton(
        ProductService,
        repository=repositories.product
    )

    purchase = providers.Singleton(
        PurchaseService,
        repository=repositories.purchase,
        product_repository=repositories.product
    )


class Container(containers.DeclarativeContainer):

    config = providers.Configuration(strict=True)

    wiring_config = containers.WiringConfiguration(
        packages=[
            "app.user.infrastructure",
            "app.auth.infrastructure",
            "app.product.infrastructure",
            "app.purchase.infrastructure"
        ]
    )

    gateways = providers.Container(Gateways, config=config.gateways)
    repositories = providers.Container(Repositories, gateways=gateways)
    services = providers.Container(Services, repositories=repositories, config=config.services)
