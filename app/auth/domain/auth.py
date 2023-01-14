from app.user.domain.user import User


class Auth(User):
    email: str
    password: str

