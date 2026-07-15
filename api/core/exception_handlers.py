"""
Centralized exception handlers for the FastAPI application.
"""

import logging
import traceback
from typing import Any

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from api.core.error_response import (
    build_error_response,
    build_validation_error_response,
)
from api.exceptions.exceptions import APIException

logger: logging.Logger = logging.getLogger(__name__)


def _log_error(
    request: Request,
    exc: Exception,
    level: int = logging.WARNING,
    extra_context: str = "",
) -> None:
    """
    Log an error with standardized format.

    Args:
        request: The FastAPI request object
        exc: The exception that occurred
        level: Logging level (default: WARNING)
        extra_context: Additional context to include in log
    """

    req_id = request.state.request_id if hasattr(request.state, "request_id") else "N/A"
    logger.log(
        level,
        f"API Error at {request.method} {request.url.path} - Request ID: {req_id} - "
        f"{extra_context}Message: {str(exc)}",
        exc_info=level >= logging.ERROR,
    )


async def api_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    """
    Handle custom API exceptions.

    Args:
        request: The FastAPI request object
        exc: The API exception

    Returns:
        JSONResponse: Standardized error response
    """

    _log_error(request, exc)
    return build_error_response(
        status_code=exc.status_code if isinstance(exc, APIException) else 500,
        message=exc.message if isinstance(exc, APIException) else str(exc),
        error_type=exc.__class__.__name__,
    )


async def value_error_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    """
    Handle ValueError exceptions.

    Args:
        request: The FastAPI request object
        exc: The ValueError exception

    Returns:
        JSONResponse: Standardized error response
    """

    _log_error(request, exc, level=logging.ERROR)
    return build_error_response(
        status_code=500,
        message="Internal server error",
        error_type="ValueError",
    )


async def generic_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    """
    Handle all unhandled exceptions.

    Args:
        request: The FastAPI request object
        exc: The unhandled exception

    Returns:
        JSONResponse: Standardized error response
    """

    _log_error(
        request,
        exc,
        level=logging.ERROR,
    )
    traceback.print_exc()

    return build_error_response(
        status_code=500,
        message=str(exc),
        error_type=type(exc).__name__,
    )


async def validation_error_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    """
    Handle Pydantic validation errors.

    Args:
        request: The FastAPI request object
        exc: The validation error

    Returns:
        JSONResponse: Standardized validation error response
    """

    assert isinstance(
        exc,
        RequestValidationError,
    )
    custom_errors: list[dict[str, str]] = []

    for error in exc.errors():
        loc = error.get("loc", [])
        error_type = error.get("type", "")

        # Handle JSON parsing errors
        if error_type == "json_invalid":
            position = str(loc[-1] if loc else "unknown")
            custom_errors.append(
                {
                    "field_name": "body_json",
                    "message": f"Invalid JSON format (error near character {position})",
                    "type": "json_invalid",
                }
            )
            continue

        # Extract field name from location
        field_name: str = _extract_field_name(loc)
        custom_errors.append(
            {
                "field_name": field_name,
                "message": error.get("msg", "unknown error"),
                "type": error_type,
            }
        )

    _log_error(
        request,
        exc,
        level=logging.WARNING,
    )
    return build_validation_error_response(custom_errors)


def _extract_field_name(
    loc: tuple[Any, ...] | list[Any],
) -> str:
    """
    Extract field name from Pydantic error location.

    Args:
        loc: Location tuple/list from Pydantic error

    Returns:
        str: Field name or "unknown_field"
    """

    if not loc:
        return "unknown_field"

    # Try to get the last element (usually the field name)
    if len(loc) > 1:
        return str(loc[-1])

    return str(loc[0]) if loc else "unknown_field"
