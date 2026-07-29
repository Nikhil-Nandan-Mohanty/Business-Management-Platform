class BusinessException(Exception):
    """Base class for business exceptions."""


class EmailAlreadyExistsError(BusinessException):
    """Raised when the email is already registered."""