from app.common.infrastructure import MongoRepository
from app.user.domain import UserRepository, User, UserCreate
from app.user.application import UserNotFoundError


class MongoUserRepository(MongoRepository[User], UserRepository):

    def __init__(self):
        self._collection = "users"
        self.__project = {
            "_id": 0,
            "id": "$_id",
            "first_name": 1,
            "last_name": 1,
            "email": 1,
            "disabled": 1
        }

    def _get_object(self, user: dict) -> User:
        user["id"] = str(user["id"])
        return User(**user)

    def find_all(self, limit: int, skip: int) -> list[User]:
        results = self.collection.find({}, self.__project).skip(skip).limit(limit)
        users: list[User] = []

        for user in results:
            users.append(self._get_object(user))

        return users

    def find_by_id(self, id: str) -> User | None:
        if not self.is_object_id(id):
            return

        user = self.collection.find_one(
            {"_id": self.get_object_id(id)},
            self.__project
        )

        if bool(user):
            return self._get_object(user)

    def exists_id(self, id: str) -> bool:
        if not self.is_object_id(id):
            return False

        user = self.collection.find_one({"_id": self.get_object_id(id)}, {"_id": 1})

        return bool(user)

    def find_by_email(self, email: str) -> User | None:
        user = self.collection.find_one({"email": email}, self.__project)

        if bool(user):
            return self._get_object(user)

    def exists_email(self, email: str) -> bool:
        user = self.collection.find_one({"email": email}, {"_id": 1})

        return bool(user)

    def insert_one(self, user: UserCreate) -> User:
        user.id = str(self.collection.insert_one(user.dict(exclude_none=True)).inserted_id)
        return user

    def update_one(self, id: str, user: User) -> User:
        if not self.is_object_id(id):
            raise UserNotFoundError(id=id)

        user_updated = self.collection.find_one_and_update(
            {"_id": self.get_object_id(id)},
            {"$set": user.dict(exclude_none=True)},
            self.__project,
            return_document=True
        )

        return self._get_object(user_updated)

    def delete(self, id: str):
        if not self.is_object_id(id):
            raise UserNotFoundError(id=id)

        self.collection.delete_one({"_id": self.get_object_id(id)})
