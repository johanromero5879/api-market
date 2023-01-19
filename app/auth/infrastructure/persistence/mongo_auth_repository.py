from app.common.infrastructure import MongoRepository
from app.auth.domain import AuthRepository, Auth


class MongoAuthRepository(MongoRepository[Auth], AuthRepository):
    def __init__(self):
        self._collection = "users"
        self.__project = {
            "_id": 0,
            "id": "$_id",
            "email": 1,
            "password": 1
        }

    def _get_object(self, user: dict) -> Auth:
        user["id"] = str(user["id"])
        if "password" not in user:
            user["password"] = ""

        return Auth(**user)

    def find_by(self, field: str, value) -> Auth | None:
        field, value = self._get_format_filter(field, value)
        user = self.collection.find_one({field: value}, self.__project)

        if bool(user):
            return self._get_object(user)
