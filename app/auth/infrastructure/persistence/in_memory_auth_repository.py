from app.auth.domain.auth_repository import AuthRepository
from app.auth.domain.auth import Auth

default_password = "$2a$12$Gn.iYPtWr9bSXnWjNa8YveCVSZ2djZ0XXq7naDm7TUICPUxmbA/QS" # 123456
users_list = [
    Auth(id='1', first_name="John", last_name="Titor", email="john.titor@cern.gov", password=default_password),
    Auth(id='2', first_name="Rachell", last_name="", email="rachell@outlook.com", password=default_password),
    Auth(id='3', first_name="Sara", last_name="Claire", email="sara.claire@cern.gov", password=default_password),
    Auth(id='4', first_name="Johan", last_name="Romero", email="johan.romero@gmail.com",
         password=default_password, disabled=True),
    Auth(id='5', first_name="Camila", last_name="Torres", email="camila.torres@gmail.com", password=default_password)
]


class InMemoryAuthRepository(AuthRepository):
    def find_by_email(self, email: str) -> Auth:
        return next(filter(lambda user: user.email == email, users_list), None)
