from pymongo import MongoClient

from app.common.infrastructure import MongoRepository
from app.user.domain import UserRepository, User
from app.user.application import UserNotFoundError


class MongoUserRepository(MongoRepository[User], UserRepository):

    __project = {
        "_id": 0,
        "id": "$_id",
        "first_name": 1,
        "last_name": 1,
        "email": 1,
        "disabled": 1
    }

    def __init__(self, client: MongoClient | None = None):
        super().__init__("users", client)

    def _get_model_instance(self, user: dict) -> User:
        user["id"] = str(user["id"])
        return User(**user)

    def find_all(self, limit: int, skip: int) -> list[User]:
        users = self._collection.find({}, self.__project).skip(skip).limit(limit)
        return self._get_model_list(users)

    def find_by(self, field: str, value) -> User | None:
        field, value = self._get_format_filter(field, value)

        user = self._collection.find_one({field: value}, self.__project)

        if bool(user):
            return self._get_model_instance(user)

    def exists_by(self, field: str, value) -> bool:
        field, value = self._get_format_filter(field, value)

        user = self._collection.find_one({field: value}, {"_id": 1})
        return bool(user)

    def update_one(self, id: str, user: User) -> User:
        if not self.is_object_id(id):
            raise UserNotFoundError(id=id)

        user_updated = self._collection.find_one_and_update(
            {"_id": self.get_object_id(id)},
            {"$set": user.dict(exclude_none=True)},
            self.__project,
            return_document=True
        )

        return self._get_model_instance(user_updated)

    def delete(self, id: str):
        if not self.is_object_id(id):
            raise UserNotFoundError(id=id)

        self._collection.delete_one({"_id": self.get_object_id(id)})
