from app.common.domain.value_id import ValueId


class UserNotFoundError(Exception):
    def __init__(self, id: ValueId | None = None, email: str | None = None):
        self.message = "User not found"
        if bool(id):
            self.message = f"User with id '{id}' not found"

        if bool(email):
            self.message = f"Email '{email}' not found"

        super().__init__(self.message)


class UserFoundError(Exception):
    def __init__(self, id: ValueId | None = None, email: str | None = None):
        self.message = "User found"
        if bool(id):
            self.message = f"User with id '{id}' found"

        if bool(email):
            self.message = f"Email '{email}' found"

        super().__init__(self.message)
