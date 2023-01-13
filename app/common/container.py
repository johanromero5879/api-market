# user
from app.user.application.user_service import UserService
from app.user.infrastructure.persistence.in_memory_user_repository import InMemoryUserRepository

# instances
# user
user_service = UserService(InMemoryUserRepository())
