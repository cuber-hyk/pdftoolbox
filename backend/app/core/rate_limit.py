"""Rate limiting middleware."""
from fastapi import Request, HTTPException
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Dict


class RateLimiter:
    """Simple in-memory rate limiter."""

    def __init__(self, requests_per_minute: int = 60):
        """Initialize rate limiter.

        Args:
            requests_per_minute: Maximum requests per minute per IP
        """
        self.requests_per_minute = requests_per_minute
        self.requests: Dict[str, list[datetime]] = defaultdict(list)

    def is_allowed(self, client_ip: str) -> bool:
        """Check if request is allowed.

        Args:
            client_ip: Client IP address

        Returns:
            True if request is allowed
        """
        now = datetime.now()
        minute_ago = now - timedelta(minutes=1)

        # Clean old requests
        self.requests[client_ip] = [
            req_time for req_time in self.requests[client_ip]
            if req_time > minute_ago
        ]

        # Check limit
        if len(self.requests[client_ip]) >= self.requests_per_minute:
            return False

        # Add current request
        self.requests[client_ip].append(now)
        return True

    def reset(self, client_ip: str) -> None:
        """Reset rate limit for client.

        Args:
            client_ip: Client IP address
        """
        if client_ip in self.requests:
            del self.requests[client_ip]


# Global rate limiter instance
rate_limiter = RateLimiter(requests_per_minute=60)


async def check_rate_limit(request: Request) -> None:
    """Check rate limit for request.

    Args:
        request: FastAPI request

    Raises:
        HTTPException: Rate limit exceeded
    """
    from app.core.security import get_client_ip

    client_ip = get_client_ip(request)

    if not rate_limiter.is_allowed(client_ip):
        raise HTTPException(
            status_code=429,
            detail="Too many requests. Please try again later.",
            headers={
                "Retry-After": "60",
                "X-RateLimit-Limit": str(rate_limiter.requests_per_minute),
                "X-RateLimit-Remaining": "0",
            }
        )
