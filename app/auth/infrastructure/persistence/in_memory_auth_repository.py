from app.auth.domain.auth_repository import AuthRepository
from app.auth.domain.auth import Auth
from app.user.infrastructure.persistence.in_memory_data import users_list


class InMemoryAuthRepository(AuthRepository):
    def find_by_email(self, email: str) -> Auth:
        return next(filter(lambda user: user.email == email, users_list), None)
