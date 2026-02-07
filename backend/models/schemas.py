"""
Pydantic schemas for API request/response models
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date


class TrustedSource(BaseModel):
    """Schema for a trusted source"""
    title: str = Field(..., description="Title of the source article")
    url: str = Field(..., description="URL of the source")
    publisher: str = Field(..., description="Publisher name")


class VerificationRequest(BaseModel):
    """Schema for verification request"""
    claim: str = Field(..., description="News headline, paragraph, or claim to verify", min_length=5)


class VerificationResponse(BaseModel):
    """Schema for verification response"""
    verdict: str = Field(..., description="REAL | FAKE | PARTIALLY TRUE | UNVERIFIED")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Confidence score between 0 and 1")
    summary: str = Field(..., description="One-paragraph explanation in simple language")
    verified_facts: List[str] = Field(default_factory=list, description="List of verified facts")
    incorrect_or_misleading_parts: List[str] = Field(default_factory=list, description="List of misleading claims")
    trusted_sources: List[TrustedSource] = Field(default_factory=list, description="List of 5 trusted sources")
    last_verified_date: str = Field(..., description="Date in YYYY-MM-DD format")


class ErrorResponse(BaseModel):
    """Schema for error response"""
    error: str
    detail: Optional[str] = None
