class CredentialsError(Exception):
    def __init__(self):
        self.message = "Authentication credentials are not valid"
        super().__init__(self.message)
