"""Utilidades para compartir información de contexto por petición."""

import contextvars

request_id_var: contextvars.ContextVar[str] = contextvars.ContextVar(
    "request_id", default="N/A"
)
