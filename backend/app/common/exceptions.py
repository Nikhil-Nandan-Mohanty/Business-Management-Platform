class BusinessException(Exception):
    """Base class for business exceptions."""


class EmailAlreadyExistsError(BusinessException):
    """Raised when the email is already registered."""


class InvalidCredentialsError(Exception):
    """Raised when login credentials are invalid."""
