from typing import TypeVar, Generic
from abc import ABC, abstractmethod
from pymongo import MongoClient
from pymongo.database import Database, Collection
from pymongo.collection import ObjectId

from app.config import MONGO_URI

Entity = TypeVar("Entity")


class MongoRepository(Generic[Entity], ABC):
    __client: MongoClient = MongoClient(MONGO_URI)
    __db: Database = __client.get_database()
    _collection: str

    @property
    def collection(self) -> Collection[Entity]:
        return self.__db.get_collection(self._collection)

    @abstractmethod
    def _get_object(self, object: dict) -> Entity:
        pass

    def is_object_id(self, id: str) -> bool:
        return ObjectId.is_valid(id)

    def get_object_id(self, id: str) -> ObjectId:
        return ObjectId(id)

    def disconnect(self):
        self.__client.close()
