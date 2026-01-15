# app/api/routes.py
from fastapi import APIRouter, HTTPException

from app.models.schemas import (
    PasswordRequest,
    PasswordAnalysisResponse
)
from app.core.analyze import analyze_password

router = APIRouter()


@router.post(
    "/analyze-password",
    response_model=PasswordAnalysisResponse
)
def analyze_password_endpoint(request: PasswordRequest):
    try:
        result = analyze_password(request.password)
        return result
    except Exception:
        # Never leak internal errors
        raise HTTPException(
            status_code=500,
            detail="Password analysis failed"
        )
