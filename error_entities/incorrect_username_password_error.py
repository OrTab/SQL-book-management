class IncorrectUsernamePassword(ValueError):
    def __init__(self, message="Incorrect username or password."):
        super().__init__(message)
        self.status_code = 401
