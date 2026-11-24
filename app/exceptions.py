class AppError(Exception):
    """Base class for business errors. Each subclass maps to an HTTP status."""

    status_code = 400
    error = "BAD_REQUEST"

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class NotFoundError(AppError):
    status_code = 404
    error = "NOT_FOUND"


class ConflictError(AppError):
    status_code = 409
    error = "CONFLICT"


class ValidationError(AppError):
    status_code = 400
    error = "BAD_REQUEST"
