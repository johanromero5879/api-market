from app.user.application import UserService
from app.user.infrastructure import MongoUserRepository

from app.auth.application import AuthService
from app.auth.infrastructure import MongoAuthRepository

from app.product.application import ProductService
from app.product.infrastructure import MongoProductRepository

# user
user_service = UserService(MongoUserRepository())

# auth
auth_service = AuthService(MongoAuthRepository())

# product
product_service = ProductService(MongoProductRepository())
