"""
Middleware for adding request ID tracking to all requests.
"""

import logging
from typing import Awaitable, Callable
from uuid import uuid4

from fastapi import Request
from fastapi.responses import Response

logger: logging.Logger = logging.getLogger(__name__)


async def request_id_middleware(
    request: Request,
    call_next: Callable[
        ...,
        Awaitable[Response],
    ],
) -> Response:
    """
    Add a unique request ID to each request for tracing.

    If the client provides an X-Request-ID header, use it.
    Otherwise, generate a new UUID.

    Args:
        request: The FastAPI request object
        call_next: The next middleware/route in the chain

    Returns:
        Response: The response from the next middleware/route
    """

    # Get or generate request ID
    request_id: str = request.headers.get(
        "x-request-id",
        str(uuid4()),
    )

    # Store in request state for access in handlers/routes
    request.state.request_id = request_id

    # Add request ID to response headers
    response: Response = await call_next(request)
    response.headers["x-request-id"] = request_id

    return response
