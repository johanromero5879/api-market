from app.common.domain.value_id import ValueID


class UserNotFoundError(Exception):
    def __init__(self, id: ValueID | None = None, email: str | None = None):
        self.message = "User not found"
        if bool(id):
            self.message = f"User with id '{id}' not found"

        if bool(email):
            self.message = f"Email '{email}' not found"

        super().__init__(self.message)
