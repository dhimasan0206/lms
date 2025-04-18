from fastapi import Request, status
from fastapi.responses import JSONResponse
import logging
from starlette.middleware.base import BaseHTTPMiddleware

from application.exceptions.auth_exceptions import AuthException

logger = logging.getLogger(__name__)


async def error_handler_middleware(request: Request, call_next):
    """Middleware for handling errors from the application"""
    try:
        return await call_next(request)
    except AuthException as exc:
        logger.warning(f"Authentication error: {exc}")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "status": "error",
                "message": exc.message,
                "details": exc.details,
            },
        )
    except Exception as exc:
        logger.exception(f"Unhandled exception: {exc}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "status": "error",
                "message": "Internal server error",
                "details": str(exc) if request.app.debug else None,
            },
        ) 