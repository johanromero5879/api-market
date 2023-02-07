from typing import Mapping, Any

from bson import ObjectId
from pymongo import MongoClient
from pymongo.client_session import ClientSession

from app.common.infrastructure import MongoAdapter
from app.user.domain import UserRepository, UserBudget, UserOut, UserPatch


class MongoUserRepository(MongoAdapter[UserOut], UserRepository):

    __project = {
        "_id": 1,
        "first_name": 1,
        "last_name": 1,
        "email": 1,
        "disabled": 1
    }

    def __init__(self, client: MongoClient | None = None):
        super().__init__("users", client)

    def _get_model_instance(self, user: Mapping[str, Any]) -> UserOut:
        return UserOut(**user)

    def find_all(self, limit: int, skip: int) -> list[UserOut]:
        users = self._collection.find({}, self.__project)\
            .skip(skip).limit(limit)

        return self._get_model_list(users)

    def find_by(self, field: str, value) -> UserOut | None:
        field, value = self._get_format_filter(field, value)

        user = self._collection.find_one({field: value}, self.__project)

        if bool(user):
            return self._get_model_instance(user)

    def exists_by(self, field: str, value) -> bool:
        field, value = self._get_format_filter(field, value)

        user = self._collection.find_one({field: value}, {"_id": 1})
        return bool(user)

    def update_one(self, id: ObjectId, user: UserPatch) -> UserOut:
        user_updated = self._collection.find_one_and_update(
            {"_id": id},
            {"$set": user.dict(exclude_none=True)},
            self.__project,
            return_document=True
        )

        return self._get_model_instance(user_updated)

    def delete(self, id: ObjectId):
        self._collection.delete_one({"_id": id})

    def find_budget(self, id: ObjectId) -> UserBudget | None:
        user = self._collection.find_one(
            {"_id": id},
            {"_id": 1, "budget": 1}
        )

        if user:
            return UserBudget(**user)

    def reduce_budget(self, id: ObjectId, cost: float, session: ClientSession):
        self._collection.update_one(
            filter={"_id": id},
            update={"$inc": {"budget": -cost}},
            session=session
        )
