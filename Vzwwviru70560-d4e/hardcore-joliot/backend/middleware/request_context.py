"""
CHE·NU™ V75 Backend - Request Context Middleware

Adds request_id, timing, and other context to each request.

@version 75.0.0
"""

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import uuid
import time
import logging

logger = logging.getLogger("chenu.request")


class RequestContextMiddleware(BaseHTTPMiddleware):
    """
    Middleware that adds context to each request:
    - request_id: Unique identifier for the request
    - start_time: Request start time for timing
    """
    
    async def dispatch(self, request: Request, call_next):
        """Add context and process request."""
        
        # Generate or use provided request ID
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        
        # Store in request state
        request.state.request_id = request_id
        request.state.start_time = time.time()
        
        # Process request
        response = await call_next(request)
        
        # Calculate duration
        duration = time.time() - request.state.start_time
        
        # Add headers
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Response-Time"] = f"{duration:.3f}s"
        
        # Log request
        logger.info(
            f"{request.method} {request.url.path} - "
            f"{response.status_code} - {duration:.3f}s - "
            f"[{request_id}]"
        )
        
        return response
