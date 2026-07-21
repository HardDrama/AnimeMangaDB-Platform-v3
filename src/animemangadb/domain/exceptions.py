class DomainError(Exception):
    """Base exception for all domain errors."""


class ValidationError(DomainError):
    """Raised when a domain validation rule is violated."""