from app.user.domain import User, UserCreate, UserRepository
from app.user.infrastructure import users_list


class InMemoryUserRepository(UserRepository):
    def find_all(self, limit: int, skip: int) -> list[User]:
        users = users_list[skip:]

        while len(users) > limit:
            users.pop(-1)

        return users

    def find_by_id(self, id: int) -> User | None:
        return next(filter(lambda user: user.id == id, users_list), None)

    def exists_id(self, id: int) -> bool:
        return any(user.id == id for user in users_list)

    def find_by_email(self, email: str) -> User | None:
        return next(filter(lambda user: user.email == email, users_list), None)

    def exists_email(self, email: str) -> bool:
        return any(user.email == email for user in users_list)

    def insert_one(self, user: UserCreate) -> User:
        if len(users_list) > 0:
            user.id = int(users_list[-1].id) + 1
        else:
            user.id = 1

        users_list.append(user)

        return user

    def update_one(self, id: int, user: User) -> User:
        for index in range(len(users_list)):
            if users_list[index].id == id:
                if bool(user.first_name):
                    users_list[index].first_name = user.first_name

                if bool(user.last_name):
                    users_list[index].last_name = user.last_name

                if bool(user.email):
                    users_list[index].email = user.email

                return users_list[index]

    def delete(self, id: int):
        for index in range(len(users_list)):
            if users_list[index].id == id:
                del users_list[index]
                return
