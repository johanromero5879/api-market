from typing import TypeVar, Generic, Mapping, Any
from abc import ABC
from bson import ObjectId

from pymongo import MongoClient
from pymongo.cursor import Cursor
from pymongo.database import Database, Collection

Model = TypeVar("Model")


class MongoAdapter(Generic[Model], ABC):
    __client: MongoClient
    __db: Database
    _collection: Collection

    def __init__(self, collection_name: str, client: MongoClient | None = None):
        self.__client = client or MongoClient()
        self.__db = self.__client.get_database()
        self._collection = self.__db.get_collection(collection_name)

    def _get_model_list(self, items: Cursor) -> list[Model]:
        """
        :param items: Iterator over mongo query results
        :return: List of model instances
        """
        return [self._get_model_instance(item) for item in items]

    def _get_model_instance(self, document: Mapping[str, Any]) -> Model:
        """
        :param document: Object mapped over a mongo query result
        :return: Model instance
        """
        pass

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

        if ObjectId.is_valid(value):
            value = ObjectId(value)

        return field, value

    def disconnect(self):
        self.__client.close()
