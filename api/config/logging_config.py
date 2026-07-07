"""Configuración de logging estructurado para la API."""

import json
import logging
from contextvars import ContextVar
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from api.core.request_context import request_id_var

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

request_id_var: ContextVar[str] = ContextVar("request_id", default="N/A")


class RequestIdFilter(logging.Filter):
    """Añade el identificador de petición a cada registro de log."""

    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = request_id_var.get()
        return True


class JsonFormatter(logging.Formatter):
    """Genera mensajes de log en formato JSON con metadatos útiles."""

    def format(self, record: logging.LogRecord) -> str:
        log_obj: dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
            "request_id": getattr(record, "request_id", "N/A"),
            "message": record.getMessage(),
        }
        if record.exc_info:
            log_obj["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_obj, default=str)


LOGGING_CONFIG: dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {"request_id": {"()": "api.config.logging_config.RequestIdFilter"}},
    "formatters": {
        "json": {"()": "api.config.logging_config.JsonFormatter"},
        "console": {
            "format": "[%(asctime)s] %(levelname)s [%(request_id)s] %(module)s:%(lineno)d - %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "console",
            "filters": ["request_id"],
        },
        "access_file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": str(LOG_DIR / "access.log"),
            "when": "midnight",
            "backupCount": 30,
            "formatter": "json",
            "filters": ["request_id"],
            "level": "INFO",
        },
        "app_file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": str(LOG_DIR / "app.log"),
            "when": "midnight",
            "backupCount": 30,
            "formatter": "json",
            "filters": ["request_id"],
            "level": "INFO",
        },
        "error_file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": str(LOG_DIR / "error.log"),
            "when": "midnight",
            "backupCount": 30,
            "formatter": "json",
            "filters": ["request_id"],
            "level": "ERROR",
        },
    },
    "loggers": {
        "uvicorn": {
            "handlers": ["console", "app_file"],
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn.error": {
            "handlers": ["console", "error_file"],
            "level": "ERROR",
            "propagate": False,
        },
        "uvicorn.access": {
            "handlers": ["console", "access_file"],
            "level": "INFO",
            "propagate": False,
        },
        "api": {
            "handlers": ["console", "app_file", "error_file", "access_file"],
            "level": "INFO",
            "propagate": False,
        },
        "sqlalchemy.engine": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
    },
    "root": {"handlers": ["console", "app_file", "error_file"], "level": "INFO"},
}
