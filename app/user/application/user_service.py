from app.common.application.service import Service
from app.user.domain.user_repository import UserRepository
from app.user.domain.user import User
from app.user.application.user_errors import UserNotFoundError, UserFoundError
from app.common.domain.value_id import ValueID


class UserService(Service):
    _repository: UserRepository

    def __init__(self, repository: UserRepository):
        super().__init__(repository)

    def get_all(self, limit: int, page: int):
        if limit <= 0 or limit > 20:
            raise ValueError("Limit parameter must be between 1 and 20")

        if page <= 0:
            raise ValueError("Page parameter must be greater than 1")

        skip = (page - 1) * limit

        return self._repository.find_all(limit, skip)

    def get_by(self, field: str, value):
        user = self._repository.find_by(field, value)

        if not user:
            raise UserNotFoundError()

        return user

    def update_one(self, id: ValueID, user: User):
        user.id = None
        if not self._repository.exists_by("id", id):
            raise UserNotFoundError(id=id)

        if bool(user.email):
            user_found = self._repository.find_by("email", user.email)
            if bool(user_found) and user_found.id != id:
                raise UserFoundError(email=user.email)

        return self._repository.update_one(id, user)

    def delete(self, id: ValueID):
        if not self._repository.exists_by("id", id):
            raise UserNotFoundError(id=id)

        self._repository.delete(id)
