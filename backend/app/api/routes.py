# app/api/routes.py
from fastapi import APIRouter, HTTPException, Request, status

from backend.app.models.schemas import (
    PasswordRequest,
    PasswordAnalysisResponse
)
from backend.app.core.analyze import analyze_password
from backend.app.core.rate_limiter import RateLimiter

router = APIRouter()

# 5 requests per minute per IP
rate_limiter = RateLimiter(max_requests=30, window_seconds=60)


@router.post(
    "/analyze-password",
    response_model=PasswordAnalysisResponse
)
def analyze_password_endpoint(
    request: Request,
    payload: PasswordRequest
):
    client_ip = request.client.host

    if not rate_limiter.is_allowed(client_ip):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many requests. Please try again later."
        )

    try:
        return analyze_password(payload.password)
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Password analysis failed"
        )
