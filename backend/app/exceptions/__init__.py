"""Custom exceptions for the fittrack application."""

class NotFoundError(Exception):
    """Raised when a requested resource is not found."""
    pass


class DuplicateError(Exception):
    """Raised when attempting to create a duplicate resource."""
    pass


class ValidationError(Exception):
    """Raised when data validation fails."""
    pass


class PermissionError(Exception):
    """Raised when a user lacks permission for an operation."""
    pass


class BusinessLogicError(Exception):
    """Raised when business logic constraints are violated."""
    pass
