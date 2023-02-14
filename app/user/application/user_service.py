from app.common.application.service import Service
from app.user.domain.user_repository import UserRepository
from app.user.domain.user import UserPatch
from app.user.application.user_errors import UserNotFoundError, UserFoundError
from app.common.domain.value_id import ValueId


class UserService(Service):
    __repository: UserRepository

    def __init__(self, repository: UserRepository):
        self.__repository = repository

    def get_all(self, limit: int, page: int):
        if limit <= 0 or limit > 20:
            raise ValueError("Limit parameter must be between 1 and 20")

        if page <= 0:
            raise ValueError("Page parameter must be greater than 1")

        skip = (page - 1) * limit

        return self.__repository.find_all(limit, skip)

    def get_by(self, field: str, value):
        user = self.__repository.find_by(field, value)

        if not user:
            raise UserNotFoundError()

        return user

    def update_one(self, id: ValueId, user: UserPatch):
        if not self.__repository.exists_by("id", id):
            raise UserNotFoundError(id=id)

        if bool(user.email):
            user_found = self.__repository.find_by("email", user.email)
            if user_found and user_found.id != id:
                raise UserFoundError(email=user.email)

        return self.__repository.update_one(id, user)

    def delete(self, id: ValueId):
        if not self.__repository.exists_by("id", id):
            raise UserNotFoundError(id=id)

        self.__repository.delete(id)
