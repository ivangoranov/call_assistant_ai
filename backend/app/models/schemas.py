"""
Pydantic schemas for API request/response validation.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


# Auth schemas
class LoginRequest(BaseModel):
    """Login request schema."""

    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Token response schema."""

    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    """User response schema."""

    id: str
    email: str
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


# Call schemas
class CallStartRequest(BaseModel):
    """Request to start a new call."""

    phone_number: str


class CallStartResponse(BaseModel):
    """Response after starting a call."""

    id: str
    phone_number: str
    status: str
    started_at: datetime


class CallEndRequest(BaseModel):
    """Request to end a call."""

    duration_seconds: Optional[int] = None


class CallResponse(BaseModel):
    """Full call response schema."""

    id: str
    phone_number: str
    status: str
    consent_given: bool
    duration_seconds: Optional[int]
    started_at: datetime
    ended_at: Optional[datetime]
    created_at: datetime

    model_config = {"from_attributes": True}


class CallListResponse(BaseModel):
    """List of calls response."""

    calls: list[CallResponse]
    total: int


# Task schema
class TaskSchema(BaseModel):
    """Task schema matching AI output."""

    task: str
    owner: Optional[str] = None
    deadline: Optional[str] = None


# Summary schema (matches AI output JSON schema from README)
class SummaryResponse(BaseModel):
    """AI Summary response schema."""

    summary: str
    topics: list[str]
    decisions: list[str]
    tasks: list[TaskSchema]
    dates: list[str]
    amounts: list[str]
    locations: list[str]
