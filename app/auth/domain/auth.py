from app.user.domain import User


class Auth(User):
    email: str
    password: str

