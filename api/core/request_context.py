"""Util to share context between requests"""

from contextvars import ContextVar

request_id_var: ContextVar[int] = ContextVar("request_id", default=0)
