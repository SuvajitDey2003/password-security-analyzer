# app/models/schemas.py
from pydantic import BaseModel, Field


class PasswordRequest(BaseModel):
    password: str = Field(
        ...,
        min_length=1,
        max_length=128,
        description="Password to analyze"
    )


class PasswordAnalysisResponse(BaseModel):
    score: int
    entropy: float
    strength: str
    issues: list[str]
    breach_count: int
