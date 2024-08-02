from error_entities.database_operation_error import DatabaseOperationError


class DatabaseDuplicationEntryError(DatabaseOperationError):
    def __init__(self, message):
        super().__init__(message)
        self.message = message
        self.status_code = 409
