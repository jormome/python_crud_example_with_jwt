"""Punto de entrada principal de la aplicación FastAPI.

Este módulo inicializa la app, registra los routers, configura los middlewares
 y define los manejadores globales de errores para ofrecer una API consistente.
"""

import logging
import uuid

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

import api.entities  # type: ignore # noqa: F401
from api.config.db import Base, engine
from api.exceptions.exceptions import BussinessError, ConflictError, NotFoundError
from api.middlewares.timing_middleware import timing_middleware
from api.routers import auth_router, user_router

logger: logging.Logger = logging.getLogger(__name__)

app = FastAPI()


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError) -> JSONResponse:
    """Devuelve un error 400 para excepciones ValueError lanzadas en la app."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST, content={"detail": str(exc)}
    )


@app.exception_handler(BussinessError)
async def bussiness_error_handler(
    request: Request, exc: BussinessError
) -> JSONResponse:
    """Convierte las excepciones de negocio en respuestas HTTP claras."""
    status_code = status.HTTP_400_BAD_REQUEST
    if isinstance(exc, NotFoundError):
        status_code = status.HTTP_404_NOT_FOUND
    elif isinstance(exc, ConflictError):
        status_code = status.HTTP_409_CONFLICT

    return JSONResponse(
        status_code=status_code, content={"detail": exc.message, "extra": exc.detail}
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """Captura errores inesperados y los registra para diagnóstico."""
    req_id: str = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    logger.error(
        f"ERROR {request.method} {request.url.path} -> {req_id} {status.HTTP_500_INTERNAL_SERVER_ERROR}"
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"},
    )


Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root() -> dict[str, str]:
    """Endpoint de comprobación rápida del servicio."""
    return {"Hello": "World"}


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    """Da formato más claro a los errores de validación de entrada."""
    custom_errors: list[dict[str, str]] = []

    for error in exc.errors():
        loc = error.get("loc", [])
        error_type = error.get("type", "")

        if error_type == "json_invalid":
            position: str = str(loc[-1]) if loc else "desconocida"
            custom_errors.append(
                {
                    "field_name": "body_json",
                    "message": f"El JSON enviado está mal formado o incompleto (error cerca del carácter {position})",
                    "type": "json_invalid",
                }
            )
            continue

        if loc and len(loc) > 1:
            field_name = str(loc[-1])
        elif loc:
            field_name = str(loc[0])
        else:
            field_name = "unknown_field"

        custom_errors.append(
            {
                "field_name": field_name,
                "message": error.get("msg", "Unknown error"),
                "type": error.get("type", "validation_error"),
            }
        )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={"Errors": custom_errors},
    )


app.middleware("http")(timing_middleware)

app.include_router(router=auth_router, prefix="/oauth", tags=["oauth"])
app.include_router(router=user_router, prefix="/users", tags=["users"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)
