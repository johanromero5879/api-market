from app.user.application.user_service import UserService
from app.user.infrastructure.persistence.in_memory_user_repository import InMemoryUserRepository

from app.auth.application.auth_service import AuthService
from app.auth.infrastructure.persistence.in_memory_auth_repository import InMemoryAuthRepository

# user
user_service = UserService(InMemoryUserRepository())

# auth
auth_service = AuthService(InMemoryAuthRepository())
