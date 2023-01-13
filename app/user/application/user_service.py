from app.common.application.service import Service
from app.user.domain.user_repository import UserRepository
from app.user.domain.user import User


class UserService(Service):
    _repository: UserRepository

    def __init__(self, repository: UserRepository):
        super().__init__(repository)

    def get_all(self, limit: int, skip: int):
        return self._repository.find_all(limit, skip)

    def get_by_id(self, id: str):
        user = self._repository.find_by_id(id)

        if not user:
            raise ValueError(f"User with id '{id}' not found")

        return user

    def get_by_email(self, email: str):
        user = self._repository.find_by_email(email)

        if not user:
            raise ValueError(f"Email '{email}' not found")

        return user

    def create_one(self, user: User) -> User:
        return self._repository.insert_one(user)

    def update_one(self, id: str, user: User):
        if not self._repository.exists_id(id):
            raise ValueError(f"User with id '{id}' not found")

        return self._repository.update_one(id, user)

    def delete(self, id: str):
        if not self._repository.exists_id(id):
            raise ValueError(f"User with id '{id}' not found")

        self._repository.delete(id)
