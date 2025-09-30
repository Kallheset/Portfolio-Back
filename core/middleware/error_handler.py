"""
Custom error handler middleware for Django.

Provides centralized error handling with logging and custom error pages.
"""

import logging

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)


class ErrorHandlerMiddleware(MiddlewareMixin):
    """
    Middleware para manejo centralizado de errores HTTP.

    Captura errores 404, 500 y otras excepciones, registra logs
    y proporciona respuestas apropiadas según el tipo de request.
    """

    def process_exception(self, request, exception):
        """
        Procesa excepciones no capturadas en las vistas.

        Args:
            request: HttpRequest object
            exception: Exception object

        Returns:
            HttpResponse: Respuesta de error apropiada
        """
        # Log the exception
        logger.error(
            f"Exception occurred: {type(exception).__name__}",
            exc_info=True,
            extra={
                "path": request.path,
                "method": request.method,
                "user": request.user.username if request.user.is_authenticated else "Anonymous",
                "ip_address": self._get_client_ip(request),
            },
        )

        # Return JSON response for API requests
        if request.path.startswith("/api/") or request.content_type == "application/json":
            return JsonResponse(
                {
                    "success": False,
                    "error": "Internal server error",
                    "message": str(exception)
                    if settings.DEBUG
                    else "An error occurred processing your request",
                },
                status=500,
            )

        # Return HTML response for regular requests
        if settings.DEBUG:
            # Let Django's debug page handle it in development
            return None

        # Custom 500 page in production
        return render(
            request,
            "500.html",
            {"error_message": "Lo sentimos, ha ocurrido un error interno."},
            status=500,
        )

    def process_response(self, request, response):
        """
        Procesa la respuesta antes de devolverla al cliente.

        Args:
            request: HttpRequest object
            response: HttpResponse object

        Returns:
            HttpResponse: Respuesta procesada
        """
        # Handle 404 errors
        if response.status_code == 404:
            logger.warning(
                f"404 Not Found: {request.path}",
                extra={
                    "path": request.path,
                    "method": request.method,
                    "user": request.user.username if request.user.is_authenticated else "Anonymous",
                    "ip_address": self._get_client_ip(request),
                },
            )

            # Return JSON for API requests
            if request.path.startswith("/api/"):
                return JsonResponse(
                    {
                        "success": False,
                        "error": "Not found",
                        "message": "The requested resource was not found",
                    },
                    status=404,
                )

            # Custom 404 page for regular requests
            if not settings.DEBUG:
                return render(
                    request,
                    "404.html",
                    {"error_message": "La página que buscas no existe."},
                    status=404,
                )

        # Handle 403 errors (Forbidden)
        if response.status_code == 403:
            logger.warning(
                f"403 Forbidden: {request.path}",
                extra={
                    "path": request.path,
                    "method": request.method,
                    "user": request.user.username if request.user.is_authenticated else "Anonymous",
                },
            )

            if request.path.startswith("/api/"):
                return JsonResponse(
                    {
                        "success": False,
                        "error": "Forbidden",
                        "message": "You do not have permission to access this resource",
                    },
                    status=403,
                )

        return response

    @staticmethod
    def _get_client_ip(request):
        """
        Obtiene la IP del cliente desde el request.

        Args:
            request: HttpRequest object

        Returns:
            str: IP address del cliente
        """
        x_forwarded_for = request.headers.get("x-forwarded-for")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip
