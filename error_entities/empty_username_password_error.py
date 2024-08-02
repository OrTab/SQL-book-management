class EmptyUsernamePassword(ValueError):
    def __init__(self, message="Username or password cannot be empty."):
        super().__init__(message)
        self.status_code = 400
