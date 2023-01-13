from typing import Optional


class UserNotFoundError(Exception):
    def __init__(self, id: Optional[str] = None, email: Optional[str] = None):
        self.message = "User not found"
        if bool(id):
            self.message = f"User with id '{id}' not found"

        if bool(email):
            self.message = f"Email '{email}' not found"

        super().__init__(self.message)
