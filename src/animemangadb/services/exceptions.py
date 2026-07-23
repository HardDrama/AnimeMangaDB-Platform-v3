"""
Application-layer exceptions.

These exceptions describe failures in application use cases without
exposing infrastructure or transport-specific details.
"""


class ApplicationServiceError(Exception):
    """
    Base exception for application-service failures.
    """