from typing import TypeVar, Generic
from abc import ABC, abstractmethod
from bson import ObjectId

from pymongo import MongoClient
from pymongo.cursor import Cursor
from pymongo.database import Database, Collection
from pymongo.client_session import ClientSession

Model = TypeVar("Model")


class MongoRepository(Generic[Model], ABC):
    __client: MongoClient
    __db: Database
    _session: ClientSession | None
    _collection: Collection

    def __init__(self, collection_name: str, client: MongoClient | None = None):
        self.__client = client or MongoClient()
        self.__db = self.__client.get_database()
        self._collection = self.__db.get_collection(collection_name)
        self._session = None

    @abstractmethod
    def _get_model_instance(self, object: dict) -> Model:
        """
        :param object: Object mapped over a mongo query result
        :return: Model instance
        """
        pass

    def _get_model_list(self, items: Cursor) -> list[Model]:
        """
        :param items: Iterator over mongo query results
        :return: List of model instances
        """
        return [self._get_model_instance(item) for item in items]

    def _get_format_filter(self, field: str, value):
        """
        Transforms value to ObjectID for _id and reference keys.
        Also changes id field by _id.
        :param field: key attribute
        :param value: value related to key given
        :return: field and value formatted to sent to MongoDB
        """
        if field == "id":
            field = "_id"

        if self.is_object_id(value):
            value = self.get_object_id(value)

        return field, value

    def is_object_id(self, id) -> bool:
        return ObjectId.is_valid(id)

    def get_object_id(self, id: str) -> ObjectId:
        return ObjectId(id)

    def start_transaction(self):
        self._session = self.__client.start_session()
        self._session.start_transaction()

    def commit_transaction(self):
        if self._session:
            self._session.commit_transaction()
            self._session = None

    def rollback_transaction(self):
        if self._session:
            self._session.abort_transaction()
            self._session = None

    def disconnect(self):
        self.__client.close()
