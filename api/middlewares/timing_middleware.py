import logging
import time
import uuid
from contextvars import Token
from typing import Awaitable, Callable

from fastapi import Request, Response

from api.config.logging_config import request_id_var

logger: logging.Logger = logging.getLogger(__name__)


async def timing_middleware(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    # Obtener o generar el ID
    req_id: str = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    # Establecer en el contexto para este request
    token: Token[str] = request_id_var.set(req_id)

    start: float = time.perf_counter()
    try:
        response: Response = await call_next(request)
    except Exception as e:
        elapsed: float = time.perf_counter() - start
        # El log ya tendrá el request_id gracias al filtro
        logger.error(
            f"ERROR {request.method} {request.url.path} -> {e} ({elapsed:.6f}s)"
        )
        raise
    else:
        elapsed = time.perf_counter() - start
        response.headers["X-Process-Time"] = f"{elapsed:.6f}s"
        response.headers["X-Request-ID"] = req_id
        logger.info(
            f"{request.method} {request.url.path} -> {response.status_code} ({elapsed:.6f}s)"
        )
    finally:
        # Restaurar el valor anterior del contexto (buena práctica)
        request_id_var.reset(token)

    return response
