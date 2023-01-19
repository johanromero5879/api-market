from typing import TypeVar, Generic
from abc import ABC, abstractmethod
from pymongo import MongoClient
from pymongo.database import Database, Collection
from bson import ObjectId

from app.config import MONGO_URI

Entity = TypeVar("Entity")


class MongoRepository(Generic[Entity], ABC):
    __client: MongoClient = MongoClient(MONGO_URI)
    __db: Database = __client.get_database()
    _collection: str

    @property
    def collection(self) -> Collection:
        return self.__db.get_collection(self._collection)

    @abstractmethod
    def _get_object(self, object: dict) -> Entity:
        pass

    def _get_list(self, list: dict) -> list[Entity]:
        return [self._get_object(item) for item in list]

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
