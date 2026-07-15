"""Logging configuration"""

import json
import logging
from typing import Any

from api.core.request_context import request_id_var

# config PRO empresarial está optimizada para escribir únicamente en consola (StreamHandler)


class RequestIdFilter(logging.Filter):
    """Add request ID to log record"""

    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = request_id_var.get()
        return True


#   transformar las líneas de texto tradicionales de tu consola en objetos JSON puros
class JsonFormatter(logging.Formatter):
    """Format log records as JSON."""

    def format(self, record: logging.LogRecord) -> str:
        log_data: dict[str, str | int] = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
            "request_id": getattr(record, "request_id", ""),
            "message": record.getMessage(),
        }
        return json.dumps(log_data)


# Configuración de Logs optimizada para entornos Cloud / Producción.
# TODOs va a la consola (stdout) en formato JSON a máxima velocidad.
LOGGING_CONFIG_PRO: dict[str, Any] = {
    # === 1. CONFIGURACIÓN ESTRUCTURAL ===
    "version": 1,
    "disable_existing_loggers": False,
    # === 2. SECCIÓN DE FILTROS ===
    "filters": {
        "request_id": {
            "()": "api.config.logging_config.RequestIdFilter",
        },
    },
    # === 3. SECCIÓN DE FORMATEADORES ===
    "formatters": {
        "json": {
            "()": "api.config.logging_config.JsonFormatter",
        },
    },
    # === 4. SECCIÓN DE HANDLERS ===
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "json",
            "filters": ["request_id"],
        },
    },
    # === 5. SECCIÓN DE LOGGERS ===
    "loggers": {
        "uvicorn": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn.error": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": False,
        },
        "uvicorn.access": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "api": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "sqlalchemy.engine": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
    },
    # === 6. EL LOGGER RAÍZ (RED DE SEGURIDAD) ===
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}
