"""Middleware package for custom Django middleware components."""

from .error_handler import ErrorHandlerMiddleware

__all__ = ["ErrorHandlerMiddleware"]
