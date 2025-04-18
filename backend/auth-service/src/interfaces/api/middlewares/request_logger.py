import time
import logging
from fastapi import Request

logger = logging.getLogger(__name__)


async def request_logger_middleware(request: Request, call_next):
    """Middleware for logging requests and their processing time"""
    start_time = time.time()
    
    # Get request info
    path = request.url.path
    if request.query_params:
        path += f"?{request.query_params}"
    
    method = request.method
    
    # Log request start
    logger.info(f"Request started: {method} {path}")
    
    # Process request
    response = await call_next(request)
    
    # Log request completion
    process_time = time.time() - start_time
    status_code = response.status_code
    logger.info(f"Request completed: {method} {path} - Status: {status_code} - Time: {process_time:.3f}s")
    
    # Add processing time header
    response.headers["X-Process-Time"] = str(process_time)
    
    return response 