from app.common.application.service import Service
from app.user.domain.user_repository import UserRepository
from app.user.domain.user import UserCreate, User
from app.user.application.user_errors import UserNotFoundError
from app.common.domain.value_id import ValueID
from app.common.application.bcrypt_service import BCryptService


class UserService(Service):
    _repository: UserRepository
    __bcrypt_service: BCryptService

    def __init__(self, repository: UserRepository):
        super().__init__(repository)
        self.__bcrypt_service = BCryptService()

    def get_all(self, limit: int, skip: int):
        return self._repository.find_all(limit, skip)

    def get_by_id(self, id: ValueID):
        user = self._repository.find_by_id(id)

        if not user:
            raise UserNotFoundError(id=id)

        return user

    def get_by_email(self, email: str):
        user = self._repository.find_by_email(email)

        if not user:
            raise UserNotFoundError(email=email)

        return user

    def create_one(self, user: UserCreate) -> User:
        return self._repository.insert_one(user)

    def update_one(self, id: ValueID, user: User):
        if not self._repository.exists_id(id):
            raise UserNotFoundError(id=id)

        return self._repository.update_one(id, user)

    def delete(self, id: ValueID):
        if not self._repository.exists_id(id):
            raise UserNotFoundError(id=id)

        self._repository.delete(id)
