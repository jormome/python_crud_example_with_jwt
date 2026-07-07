"""Excepciones de negocio utilizadas por la API."""

from typing import Any


class BussinessError(Exception):
    """Base para errores controlados de la aplicación."""

    def __init__(self, message: str, detail: Any = None) -> None:
        super().__init__(message)
        self.message: str = message
        self.detail: Any = detail


class NotFoundError(BussinessError):
    """Se lanza cuando un recurso solicitado no existe."""

    def __init__(self, message: str = "Resource not found") -> None:
        super().__init__(message)


class ConflictError(BussinessError):
    """Se lanza cuando hay un conflicto con el estado actual de los datos."""

    def __init__(self, message: str = "Conflict") -> None:
        super().__init__(message)


class UnauthorizedError(BussinessError):
    """Se lanza cuando una operación requiere autenticación o permisos."""

    def __init__(self, message: str = "Unauthorized") -> None:
        super().__init__(message)
