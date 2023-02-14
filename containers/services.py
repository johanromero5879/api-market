from dependency_injector import containers, providers

from app.common.application import JWTService, BCryptService
from app.common.infrastructure import MongoTransaction
from app.purchase.application import PurchaseService
from app.product.application import ProductService
from app.user.application import UserService
from app.auth.application import AuthService


class Services(containers.DeclarativeContainer):

    config = providers.Configuration(strict=True)
    gateways = providers.DependenciesContainer()
    repositories = providers.DependenciesContainer()

    jwt = providers.Singleton(JWTService, jwt_secret=config.jwt.secret)
    bcrypt = providers.Singleton(BCryptService)
    transaction = providers.Factory(MongoTransaction, client=gateways.database_client)

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
        purchase_repository=repositories.purchase,
        product_repository=repositories.product,
        user_repository=repositories.user
    )
