"""
Custom exceptions for the API
"""

from http import HTTPStatus


class APIException(Exception):
    """
    Base exception for all API exceptions

    Permits to middleware to catch all API exceptions
    """

    # al usar HTTPStatus desacoplo las excepciones de FastApi
    status_code: int = HTTPStatus.INTERNAL_SERVER_ERROR
    default_message: str = "Internal server error"

    def __init__(
        self,
        message: str | None = None,
    ) -> None:
        self.message: str = message or self.default_message
        super().__init__(self.message)


class ConnectionException(APIException):
    """
    Exception raised when there is a connection error
    """

    status_code = HTTPStatus.SERVICE_UNAVAILABLE
    default_message = "Connection error"


class BusinessException(APIException):
    """
    Exception raised when there is a business error
    """

    status_code = HTTPStatus.BAD_REQUEST
    default_message = "Business error"


class NotFoundException(APIException):
    """
    Exception raised when a resource is not found
    """

    status_code = HTTPStatus.NOT_FOUND
    default_message = "Resource not found"


class ConflictException(APIException):
    """
    Exception raised when there is a conflict
    """

    status_code = HTTPStatus.CONFLICT
    default_message = "Conflict"


class AuthorizationException(APIException):
    """
    Exception raised when there is an authorization error
    """

    status_code = HTTPStatus.UNAUTHORIZED
    default_message = "Unauthorized"


class AuthenticationException(APIException):
    """
    Exception raised when there is an authentication error
    """

    status_code = HTTPStatus.FORBIDDEN
    default_message = "Authentication error"
