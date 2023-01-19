from app.user.application import UserService
from app.user.infrastructure import MongoUserRepository

from app.auth.application.auth_service import AuthService
from app.auth.infrastructure import InMemoryAuthRepository

# user
user_service = UserService(MongoUserRepository())

# auth
auth_service = AuthService(InMemoryAuthRepository())
