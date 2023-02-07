from typing import Mapping, Any

from pymongo import MongoClient

from app.common.domain import PyObjectId
from app.common.infrastructure import MongoAdapter
from app.auth.domain import AuthRepository, AuthOut, AuthIn


class MongoAuthRepository(MongoAdapter[AuthOut], AuthRepository):
    __project = {
        "_id": 1,
        "email": 1,
        "password": 1
    }

    def __init__(self, client: MongoClient | None = None):
        super().__init__("users", client)

    def _get_model_instance(self, user: Mapping[str, Any]) -> AuthOut:
        return AuthOut(**user)

    def find_by(self, field: str, value) -> AuthOut | None:
        field, value = self._get_format_filter(field, value)

        user = self._collection.find_one({field: value}, self.__project)

        if user:
            return self._get_model_instance(user)

    def exists_by(self, field: str, value) -> bool:
        field, value = self._get_format_filter(field, value)

        user = self._collection.find_one({field: value}, {"_id": 1})

        return bool(user)

    def insert_one(self, user: AuthIn) -> PyObjectId:
        user_id = self._collection\
                        .insert_one(user.dict(exclude_none=True)).inserted_id
        return user_id
