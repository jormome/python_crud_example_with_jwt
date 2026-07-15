"""
FastAPI application configuration with centralized exception handling and middleware.
"""

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

# Import entities to ensure SQLAlchemy models are registered
import api.entities  # type: ignore # noqa: F401
from api.core.exception_handlers import (
    api_exception_handler,
    generic_exception_handler,
    validation_error_handler,
    value_error_handler,
)
from api.exceptions.exceptions import APIException
from api.middlewares.request_id_middleware import request_id_middleware
from api.routers import auth_router, user_router

app = FastAPI()

# Middleware
_ = app.middleware("http")(request_id_middleware)

# Exception Handlers
app.add_exception_handler(APIException, api_exception_handler)
app.add_exception_handler(ValueError, value_error_handler)
app.add_exception_handler(Exception, generic_exception_handler)
app.add_exception_handler(RequestValidationError, validation_error_handler)

# Routers
app.include_router(router=auth_router, prefix="/oauth", tags=["oauth"])
app.include_router(router=user_router, prefix="/users", tags=["users"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)
