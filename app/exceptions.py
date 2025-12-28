class NotFoundError(Exception):
    """Raised when a requested resource does not exist."""
    pass


class DuplicateError(Exception):
    """Raised when attempting to create a resource that already exists."""
    pass


class ValidationError(Exception):
    """Raised when provided data is invalid."""
    pass


class PermissionError(Exception):
    """Raised when a user does not have permission to perform an action."""
    pass


class BusinessLogicError(Exception):
    """Raised when a business rule prevents the action."""
    pass
