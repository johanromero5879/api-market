from typing import List, Optional

from app.user.domain.user import User
from app.user.domain.user_repository import UserRepository


users_list = [
    User(id='1', first_name="John", last_name="Titor", email="john.titor@cern.gov"),
    User(id='2', first_name="Rachell", last_name="", email="rachell@outlook.com"),
    User(id='3', first_name="Sara", last_name="Claire", email="sara.claire@cern.gov"),
    User(id='4', first_name="Johan", last_name="Romero", email="johan.romero@gmail.com", disabled=True),
    User(id='5', first_name="Camila", last_name="Torres", email="camila.torres@gmail.com")
]


class InMemoryUserRepository(UserRepository):
    def find_all(self, limit: int, skip: int) -> List[User]:
        users = users_list[skip:]

        while len(users) > limit:
            users.pop(-1)

        return users

    def find_by_id(self, id: str) -> Optional[User]:
        return next(filter(lambda user: user.id == id, users_list), None)

    def exists_id(self, id: str) -> bool:
        return any(user.id == id for user in users_list)

    def find_by_email(self, email: str) -> Optional[User]:
        return next(filter(lambda user: user.email == email, users_list), None)

    def exists_email(self, email: str) -> bool:
        return any(user.email == email for user in users_list)

    def insert_one(self, user: User) -> User:
        if len(users_list) > 0:
            user.id = str(int(users_list[-1].id) + 1)
        else:
            user.id = 1

        users_list.append(user)

        return user

    def update_one(self, id: str, user: User) -> User:
        for index in range(len(users_list)):
            if users_list[index].id == id:
                if bool(user.first_name):
                    users_list[index].first_name = user.first_name

                if bool(user.last_name):
                    users_list[index].last_name = user.last_name

                if bool(user.email):
                    users_list[index].email = user.email

                return users_list[index]

    def delete(self, id: str):
        for index in range(len(users_list)):
            if users_list[index].id == id:
                del users_list[index]
                return
