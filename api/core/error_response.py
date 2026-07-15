"""
Helper functions for standardized error responses.
"""

from fastapi import status
from fastapi.responses import JSONResponse


def build_error_response(
    status_code: int,
    message: str,
    error_type: str,
    field_name: str = "global",
) -> JSONResponse:
    """
    Build a standardized JSON error response.

    Args:
        status_code: HTTP status code
        message: Error message
        error_type: Type/class name of the error
        field_name: Field that caused the error (default: "global")

    Returns:
        JSONResponse: Standardized error response
    """

    return JSONResponse(
        status_code=status_code,
        content={
            "errors": [
                {
                    "field_name": field_name,
                    "message": message,
                    "type": error_type,
                }
            ]
        },
    )


def build_validation_error_response(
    errors: list[dict[str, str]],
) -> JSONResponse:
    """
    Build a validation error response with multiple field errors.

    Args:
        errors: List of error dictionaries with field_name, message, and type

    Returns:
        JSONResponse: Validation error response
    """

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"errors": errors},
    )
