from typing import TypeVar, Generic
from abc import ABC, abstractmethod
from pymongo import MongoClient
from pymongo.database import Database, Collection
from bson import ObjectId

from app.config import MONGO_URI

Model = TypeVar("Model")


class MongoRepository(Generic[Model], ABC):
    __client: MongoClient = MongoClient(MONGO_URI)
    __db: Database = __client.get_database()

    @property
    @abstractmethod
    def collection_name(self) -> str:
        pass

    def collection(self, name: str | None = None) -> Collection:
        if bool(name):
            return self.__db.get_collection(name)

        return self.__db.get_collection(self.collection_name)

    @abstractmethod
    def _get_model_instance(self, object: dict) -> Model:
        pass

    def _get_model_list(self, list: dict) -> list[Model]:
        return [self._get_model_instance(item) for item in list]

    def _get_format_filter(self, field: str, value):
        if field == "id":
            field = "_id"

        if field == "_id" and self.is_object_id(value):
            value = self.get_object_id(value)

        return field, value

    def is_object_id(self, id: str) -> bool:
        return ObjectId.is_valid(id)

    def get_object_id(self, id: str) -> ObjectId:
        return ObjectId(id)

    def disconnect(self):
        self.__client.close()
