from app.auth.domain import AuthRepository, Auth
from app.user.infrastructure import users_list


class InMemoryAuthRepository(AuthRepository):
    def find_by_email(self, email: str) -> Auth:
        return next(filter(lambda user: user.email == email, users_list), None)
